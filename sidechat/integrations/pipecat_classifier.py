"""Sidechat as a Pipecat classifier: a drop-in for `JevClassifier` in the daily-audience demo.

In `daily-audience/server/bot.py`, replace

    classifier=JevClassifier(api_key=jev_api_key(), timeout=2.0)

with

    from sidechat.integrations.pipecat_classifier import SidechatClassifier
    classifier=SidechatClassifier("/path/to/pipecat-sidechat/models/<run_id>", bot_name=BOT_NAME)

after `uv pip install -e /path/to/pipecat-sidechat` in the demo's server environment.

It answers the demo's two yes/no questions by name, reading the demo's own state (the call, the
earlier messages, the latest message):

    addressed  Sidechat's `respond`, rescaled so the demo's threshold (0.8) falls on the model's own
               answer-now threshold
    question   the larger of `respond` and `intent.open`, each rescaled so the demo's threshold (0.5)
               falls on the model's hold thresholds

So the demo's gate makes Sidechat's decisions with no change to its thresholds. Any other question
name raises `ClassifierError`. Inference runs on CPU in a worker thread, on one ONNX thread by
default (a second was slower on every cloud profile under 1.5 vCPU, exp-033).

With a two-tower model the history is encoded apart from the line. After each line the adapter
starts encoding the history the next line will carry (this one included), in the background, so
when the next person stops talking only their line is left to encode. `prepare_history` does the
same for an integration that knows the history earlier (when the agent's own turn is logged).
"""

from __future__ import annotations

import asyncio
import re
from collections.abc import Mapping, Sequence
from typing import Any

from pipecat.classifiers.base_classifier import (
    BaseClassifier,
    ClassifierError,
    ClassifierQuestion,
    ClassifierResult,
    YesNoResult,
)

from sidechat.runtime import TwoTower, load
from sidechat.schema import Agent, SidechatRequest, Turn

PEOPLE_RE = re.compile(r"People on the call:\s*(.*?)\.\s")


def rescale(x: float, own: float, target: float) -> float:
    """A monotonic map that sends `own` to `target`, 0 to 0 and 1 to 1."""
    own = min(max(own, 1e-6), 1 - 1e-6)
    if x <= own:
        return target * x / own
    return target + (1 - target) * (x - own) / (1 - own)


class SidechatClassifier(BaseClassifier):
    def __init__(
        self,
        model_dir: str,
        *,
        bot_name: str,
        aliases: Sequence[str] = (),
        role: str | None = None,
        threads: int = 1,
        demo_respond: float = 0.8,
        demo_question: float = 0.5,
        int8: bool = False,
        speculate: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self._model = load(model_dir, threads=threads, int8=int8)
        self._speculate = speculate and isinstance(self._model, TwoTower)
        self._ahead: asyncio.Task | None = None
        self._agent = Agent(name=bot_name, aliases=list(aliases), role=role or "AI assistant on the call")
        self._demo = (demo_respond, demo_question)

    @property
    def model(self) -> str | None:
        return f"sidechat:{self._model.config['run_id']}"

    def _request(self, state: Any) -> SidechatRequest:
        if not isinstance(state, Mapping) or "latest_message" not in state:
            raise ClassifierError(
                "SidechatClassifier reads the daily-audience state: call, earlier_messages, latest_message"
            )
        people = None
        m = PEOPLE_RE.search(str(state.get("call", "")) + " ")
        if m and m.group(1).strip() and m.group(1).strip() != "unknown":
            people = [p.strip() for p in m.group(1).split(",") if p.strip()]
        history = [
            Turn(speaker=e.get("speaker"), text=str(e.get("said", "")), agent=e.get("speaker") == self._agent.name)
            for e in (state.get("earlier_messages") or [])[-8:]
        ]
        latest = state["latest_message"]
        return SidechatRequest(
            agent=self._agent,
            text=str(latest.get("said", "")),
            speaker=latest.get("speaker"),
            history=history,
            people=people,
        )

    def prepare_history(self, earlier_messages: Sequence[Mapping[str, Any]]) -> None:
        """Encode now the history the next line will carry (`{speaker, said}` dicts, oldest first).
        Only a two-tower model has anything to do; the line is not needed."""
        state = {"earlier_messages": list(earlier_messages), "latest_message": {"speaker": None, "said": ""}}
        self._model.prepare(self._request(state))

    async def _ask(
        self, state: Any, questions: Mapping[str, ClassifierQuestion], inputs: Sequence[Any] = (), **_: Any
    ) -> tuple[dict[str, ClassifierResult], None]:
        # Text only: images, audio or files (`inputs` since Pipecat 1.16, `images` before) are ignored.
        req = self._request(state)
        answer = await asyncio.to_thread(self._model.answer, req)
        if self._speculate:
            after = [*(state.get("earlier_messages") or []), state["latest_message"]]
            self._ahead = asyncio.create_task(asyncio.to_thread(self.prepare_history, after))
        t = self._model.thresholds
        respond_demo, question_demo = self._demo
        results: dict[str, ClassifierResult] = {}
        for name in questions:
            if name in ("addressed", "respond"):
                p = rescale(answer.respond, t["respond"], respond_demo)
            elif name in ("question", "open"):
                p = max(
                    rescale(answer.respond, t["wait"], question_demo) if answer.respond < t["respond"] else 0.0,
                    rescale(answer.intent["open"], t["open"], question_demo) if t["open"] <= 1 else 0.0,
                )
            else:
                raise ClassifierError(f"SidechatClassifier answers 'addressed' and 'question', not {name!r}")
            results[name] = YesNoResult(probability=round(min(1.0, max(0.0, p)), 6))
        return results, None
