"""A voice bot for a room full of people that only speaks when it is spoken to.

    Deepgram Flux (STT) -> context -> Sidechat gate -> OpenAI -> Deepgram Flux (TTS)

The bot hears everything said in the room and keeps it in the LLM context. After each line,
Sidechat decides whether the bot should answer: "respond" lets the LLM run, "ignore" holds it
back, and "wait" (a question left open to the room) gives people a moment to answer it
themselves before the bot takes it.

    uv run bot.py              # then open http://localhost:7860/client
    uv run bot.py -t daily     # a Daily room that several people can join
"""

import asyncio
import os
from collections import deque
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger
from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.frames.frames import (
    Frame,
    LLMContextAssistantTurnFrame,
    LLMContextFrame,
    LLMContextUserTurnFrame,
    TTSSpeakFrame,
    UserStartedSpeakingFrame,
)
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.worker import PipelineParams, PipelineWorker
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport
from pipecat.services.deepgram.flux.stt import DeepgramFluxSTTService
from pipecat.services.deepgram.flux.tts import DeepgramFluxTTSService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.base_transport import BaseTransport, TransportParams
from pipecat.transports.daily.transport import DailyParams
from pipecat.workers.runner import WorkerRunner

from sidechat.runtime import Sidechat, load
from sidechat.schema import MAX_HISTORY, Agent, SidechatRequest, Turn

load_dotenv(override=True)

BOT_NAME = os.getenv("BOT_NAME", "Atlas")
# The exported model folder (model.onnx, tokenizer.json, config.json).
MODEL_DIR = os.getenv("SIDECHAT_MODEL", str(Path(__file__).parent.parent / "models" / "side-r3-ettin-150m-s0"))
# How long an open question waits for someone else to answer it before the bot does.
WAIT_SECS = 2.0

SYSTEM_INSTRUCTION = f"""\
You are {BOT_NAME}, a voice assistant in a room with several people. You hear everything, \
but you are only asked to speak when someone talks to you or leaves a question open. Answer the \
latest line, using the earlier conversation when it helps. Your words are spoken aloud: one to \
three short sentences, no lists, markdown or emojis."""

GREETING = f"Hi, I'm {BOT_NAME}. I'll stay quiet until you ask me something."


class SidechatGate(FrameProcessor):
    """Lets the LLM answer a line only when Sidechat says the line was for the bot.

    It sits between the user aggregator and the LLM. Every line still goes into the
    context, so when the bot does speak it knows what was said. The gate only decides
    whether the LLM runs.
    """

    def __init__(self, model: Sidechat, bot: Agent):
        super().__init__(name="SidechatGate")
        self._model = model
        self._bot = bot
        # The latest line plus the earlier ones Sidechat reads, oldest first.
        self._turns: deque[Turn] = deque(maxlen=MAX_HISTORY + 1)
        self._user_turn_ended = False
        # The LLM run for a "wait" decision, waiting for the room to stay quiet.
        self._waiting: asyncio.Task | None = None

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, LLMContextUserTurnFrame) and not frame.speculation:
            # Someone finished a line. One audio stream for the whole room can't say who
            # spoke, so the line has no speaker. Sidechat was trained on lines like that;
            # pass a name or a label such as "Speaker 1" if your transport knows it.
            self._turns.append(Turn(speaker=None, text=frame.text))
            self._user_turn_ended = True

        elif isinstance(frame, LLMContextAssistantTurnFrame):
            # What the bot said. Sidechat reads the rhythm: a reply straight after the
            # bot's question is usually for the bot, even without its name.
            self._turns.append(Turn(speaker=self._bot.name, text=frame.text, agent=True))

        elif isinstance(frame, UserStartedSpeakingFrame):
            # Someone took the floor, so an answer that was waiting for quiet is dropped.
            # Their new line is judged with the old one as context.
            await self._stop_waiting()

        elif isinstance(frame, LLMContextFrame) and self._user_turn_ended and not frame.speculation:
            # The user aggregator asks the LLM to answer the line. Decide whether it should.
            # Other context frames, such as a tool result, pass straight through.
            self._user_turn_ended = False
            await self._decide(frame)
            return

        await self.push_frame(frame, direction)

    async def _decide(self, frame: LLMContextFrame):
        await self._stop_waiting()
        *earlier, latest = self._turns
        request = SidechatRequest(agent=self._bot, text=latest.text, history=earlier)

        # 10 to 50 ms on a laptop CPU. Run it off the event loop so audio keeps flowing.
        answer = await asyncio.to_thread(self._model.answer, request)
        decision = self._model.decide(answer)  # thresholds from the model's config.json
        logger.info(f"Sidechat: {decision} (respond {answer.respond:.2f}) for {latest.text!r}")

        if decision == "respond":
            await self.push_frame(frame)
        elif decision == "wait":
            self._waiting = self.create_task(self._respond_after_quiet(frame))
        # "ignore": the frame is dropped. The line stays in the context.

    async def _respond_after_quiet(self, frame: LLMContextFrame):
        await asyncio.sleep(WAIT_SECS)
        self._waiting = None
        await self.push_frame(frame)

    async def _stop_waiting(self):
        if self._waiting:
            await self.cancel_task(self._waiting)
            self._waiting = None

    async def cleanup(self):
        await super().cleanup()
        await self._stop_waiting()


# The runner picks the transport. Both take one audio stream for the whole room.
transport_params = {
    # Default: a browser tab at http://localhost:7860/client. Everyone talks into one microphone.
    "webrtc": lambda: TransportParams(audio_in_enabled=True, audio_out_enabled=True),
    # `-t daily`: a Daily room people join from their own browsers, mixed into one stream so
    # a single STT connection hears everyone.
    "daily": lambda: DailyParams(audio_in_enabled=True, audio_out_enabled=True, audio_in_user_tracks=False),
}


async def run_bot(transport: BaseTransport, runner_args: RunnerArguments):
    # Flux transcribes and decides when each person has finished speaking. The bot's name is
    # Sidechat's most reliable signal, so it is listed as a key term for the STT.
    stt = DeepgramFluxSTTService(
        api_key=os.environ["DEEPGRAM_API_KEY"],
        settings=DeepgramFluxSTTService.Settings(keyterm=[BOT_NAME]),
    )
    tts = DeepgramFluxTTSService(
        api_key=os.environ["DEEPGRAM_API_KEY"],
        settings=DeepgramFluxTTSService.Settings(voice="flux-cole-en"),
    )
    llm = OpenAILLMService(
        api_key=os.environ["OPENAI_API_KEY"],
        settings=OpenAILLMService.Settings(system_instruction=SYSTEM_INSTRUCTION),
    )

    context = LLMContext()
    user_aggregator, assistant_aggregator = LLMContextAggregatorPair(
        context,
        user_params=LLMUserAggregatorParams(vad_analyzer=SileroVADAnalyzer()),
    )

    gate = SidechatGate(
        model=load(MODEL_DIR, threads=2),
        bot=Agent(name=BOT_NAME, role="AI assistant in the room"),
    )

    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            user_aggregator,  # writes every line to the context
            gate,  # lets the LLM answer only lines meant for the bot
            llm,
            tts,
            transport.output(),
            assistant_aggregator,  # writes what the bot said to the context
        ]
    )

    worker = PipelineWorker(
        pipeline,
        params=PipelineParams(enable_metrics=True, enable_usage_metrics=True),
        idle_timeout_secs=runner_args.pipeline_idle_timeout_secs,
    )
    runner = WorkerRunner(handle_sigint=runner_args.handle_sigint)
    await runner.add_workers(worker)

    # Greet the first person to arrive, and leave when the last one goes.
    people = 0

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        nonlocal people
        people += 1
        if people == 1:
            await worker.queue_frames([TTSSpeakFrame(GREETING)])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        nonlocal people
        people -= 1
        if people == 0:
            await runner.cancel()

    await runner.run()


async def bot(runner_args: RunnerArguments):
    """Entry point for the Pipecat runner and Pipecat Cloud."""
    transport = await create_transport(runner_args, transport_params)
    await run_bot(transport, runner_args)


if __name__ == "__main__":
    from pipecat.runner.run import main

    main()
