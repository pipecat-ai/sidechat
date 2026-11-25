"""Jev, asked exactly as the daily-audience demo asks it.

The two questions, the state and the decision rule are copied from `server/addressing.py` in
`daily-audience` at commit `73171de` (`AddressingMonitor.__init__`, `.classify` and
`_Gate._decide`). `tests/test_jev_demo.py` checks the wording against that file when it is present.

Nothing here imports Pipecat: the job wraps these strings in `YesNoQuestion` and sends them through
the same `JevClassifier` the demo uses.
"""

from __future__ import annotations

import hashlib
import json
import re

from sidechat.schema import SidechatRequest

DEMO_REPO = "daily-audience"
DEMO_COMMIT = "73171de"
DEMO_PIPECAT = "1.16.0"
DEFAULT_MODEL = "jev-1.13.0"  # pipecat 1.16.0's pinned default, which the demo uses

RESPOND_THRESHOLD = 0.8  # AddressingConfig.respond_threshold
QUESTION_THRESHOLD = 0.5  # AddressingConfig.question_threshold
HISTORY = 8  # AddressingConfig.history
UNKNOWN_SPEAKER = "Someone"

# Each template is the demo's source text, fragment by fragment, with {bot} where it has {bot}.
ADDRESSED = {
    "instructions": (
        "Is the latest message spoken to {bot}, the AI assistant on the call, ",
        "so that {bot} is the one expected to reply?",
    ),
    "yes": (
        "The speaker talks to {bot}: calls it by name to ask or tell it ",
        "something, or just calls its name; speaks to 'the assistant', 'the AI' ",
        "or 'the bot'; or replies to or follows up on what {bot} just said.",
    ),
    "no": (
        "The speaker is talking to another person or to the group, or thinking ",
        "aloud. Saying {bot}'s name is not enough: talking about {bot} to ",
        "someone else ('I asked {bot} yesterday', '{bot} got that wrong', ",
        "'should we ask {bot}?') is not talking to it.",
    ),
}
QUESTION = {
    "instructions": (
        "Is the latest message a question or request that is still unanswered ",
        "and is open for anyone on the call to answer?",
    ),
    "yes": (
        "A question or request put to the group, to nobody in particular, or to ",
        "an unclear 'you', which {bot} could reasonably answer.",
    ),
    "no": (
        "Not a question or request, or one meant for one particular person ",
        "other than {bot}: it names them or continues a back-and-forth with them.",
    ),
}
CALL = (
    "A live video call. People on the call: {people}. {bot} is an AI voice ",
    "assistant that is also on the call and listens to everything.",
)


def _fill(fragments: tuple[str, ...], **values: str) -> str:
    return "".join(fragments).format(**values)


def questions(bot: str) -> dict[str, dict[str, str]]:
    """The demo's two yes/no questions, by the names the demo gives them."""
    return {
        name: {part: _fill(fragments, bot=bot) for part, fragments in template.items()}
        for name, template in (("addressed", ADDRESSED), ("question", QUESTION))
    }


def name_pattern(bot: str, aliases: list[str] | tuple[str, ...] = ()) -> re.Pattern[str]:
    names = "|".join(re.escape(n) for n in (bot, *aliases))
    return re.compile(rf"\b(?:{names})\b", re.IGNORECASE)


def state(req: SidechatRequest) -> dict:
    """What the demo sends as the state: the call, the earlier messages and the latest one."""
    bot = req.agent.name
    people = ", ".join(req.people or []) or "unknown"
    spelled = name_pattern(bot, req.agent.aliases).sub(bot, req.text)
    return {
        "call": _fill(CALL, people=people, bot=bot),
        "earlier_messages": [
            {"speaker": bot if t.agent else (t.speaker or UNKNOWN_SPEAKER), "said": t.text}
            for t in req.history[-HISTORY:]
        ],
        "latest_message": {"speaker": req.speaker or UNKNOWN_SPEAKER, "said": spelled},
    }


def key(model: str, req: SidechatRequest) -> str:
    """Identifies one question to Jev. Rows that would send the same request share an answer."""
    payload = {"model": model, "questions": questions(req.agent.name), "state": state(req)}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def decision(
    addressed: float,
    question: float,
    respond_threshold: float = RESPOND_THRESHOLD,
    question_threshold: float = QUESTION_THRESHOLD,
) -> str:
    """The gate's rule with other people on the call: answer now, hold for silence, or stay quiet."""
    if addressed >= respond_threshold:
        return "respond"
    if question >= question_threshold:
        return "wait"
    return "ignore"


def prompt_sha() -> str:
    """Changes whenever the wording above changes, so stored answers are never mixed across wordings."""
    payload = {"addressed": ADDRESSED, "question": QUESTION, "call": CALL, "history": HISTORY}
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()[:12]
