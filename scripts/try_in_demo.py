"""Run the daily-audience demo's own decision code with Sidechat in Jev's place, on its sample lines.

Uses the demo's `AddressingMonitor.classify` and its thresholds unchanged; only the classifier
differs. Nothing in the demo is edited. Run it with the demo's Python, so Pipecat is there:

    PYTHONPATH=. ~/Sites/daily-audience/server/.venv/bin/python scripts/try_in_demo.py models/<run_id>

Add `--int8` to use the int8 build, if the export made one.
"""

from __future__ import annotations

import asyncio
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEMO = pathlib.Path.home() / "Sites" / "daily-audience" / "server"
sys.path[:0] = [str(ROOT), str(DEMO)]

from addressing import AddressingConfig, AddressingMonitor, Roster  # noqa: E402
from pipecat.processors.aggregators.llm_context import LLMContext  # noqa: E402

from sidechat.integrations.pipecat_classifier import SidechatClassifier  # noqa: E402

B = "Atlas"
SAMPLES = [  # the demo's scripts/try_addressing.py list
    ([], "Jon: Sam, did you get a chance to look at the Q3 numbers?"),
    ([], "Jon: I think we should ship on Friday."),
    (["Jon: I think we should ship on Friday."], "Sam: Yeah, that makes sense."),
    ([], "Jon: What do you think, Sam?"),
    ([], "Jon: What's the population of Tokyo?"),
    ([], "Jon: Does anyone know when the next release is?"),
    ([], "Jon: Can you look up the weather in Paris for me?"),
    ([], "Jon: Can the assistant summarize what we just discussed?"),
    ([f"Jon: {B}, what's the capital of Australia?", f"{B}: It's Canberra."], "Jon: And how many people live there?"),
    ([f"Jon: {B}, how tall is the Eiffel Tower?", f"{B}: About 330 meters."], "Sam: Thanks!"),
    ([f"Jon: {B}, how tall is the Eiffel Tower?", f"{B}: About 330 meters."], "Sam: Wow, taller than I thought. Jon, have you ever been?"),
    (["Jon: How tall is the Eiffel Tower?", "Sam: No idea."], "Jon: Hmm, me neither."),
    ([], "Sam: Could you send me that file after the call?"),
    (["Jon: Sam, are you free on Thursday?"], "Sam: Thursday works. What time?"),
    ([], "Jon: Is it just me or is the audio a bit choppy?"),
    ([], f"Jon: Hey {B}, what time is it in London?"),
    ([], f"Jon: {B}, what's the capital of France?"),
    ([], f"Sam: What do you think, {B}?"),
    ([], f"Jon: {B}, can you summarize what we decided?"),
    ([], f"Sam: I'm not sure about that one. {B}, what is the capital of Japan?"),
    ([f"Jon: {B}, how tall is the Eiffel Tower?", f"{B}: About 330 meters."], f"Jon: Thanks, {B}."),
    ([], f"Sam: {B}?"),
    ([], f"Jon: Okay {B}, that's enough."),
    ([], f"Sam: I asked {B} about that yesterday and it had no clue."),
    ([], f"Jon: {B} got that wrong last time."),
    ([], f"Sam: Jon, did you hear what {B} said?"),
    ([], f"Jon: I don't think {B} can help with that."),
    ([], f"Sam: The bot's name is {B}."),
    ([], f"Jon: Should we ask {B}?"),
    ([], f"Sam: Let's see if {B} knows."),
    ([], f"Jon: Sam, can you add {B} to tomorrow's meeting?"),
    ([], f"Sam: {B} is pretty fast today."),
    ([], f"Jon: We named it {B} after the mountains."),
]


def split(line: str) -> dict[str, str]:
    speaker, _, said = line.partition(": ")
    return {"speaker": speaker, "said": said}


async def main() -> None:
    model_dir = sys.argv[1]
    int8 = "--int8" in sys.argv[2:]
    config = AddressingConfig(bot_name=B)
    roster = Roster()
    roster.join({"id": "jon", "info": {"userName": "Jon"}})
    roster.join({"id": "sam", "info": {"userName": "Sam"}})
    classifier = SidechatClassifier(model_dir, bot_name=B, int8=int8)
    monitor = AddressingMonitor(classifier=classifier, context=LLMContext(), roster=roster, config=config)
    print(f"{'addressed':>9} {'question':>8} {'ms':>5}  decision  latest message")
    for earlier, latest in SAMPLES:
        m = split(latest)
        v = await monitor.classify([split(x) for x in earlier], m["speaker"], m["said"])
        d = "respond" if v.addressed >= config.respond_threshold else "wait" if v.question >= config.question_threshold else "ignore"
        print(f"{v.addressed:9.2f} {v.question:8.2f} {v.classifier_ms:5.0f}  {d:<8}  {latest}")


if __name__ == "__main__":
    asyncio.run(main())
