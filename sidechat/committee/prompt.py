"""What every committee member reads: the guide, the answer format, and one line in its conversation.

The system prompt is the same for every line, so each provider can cache it. The guide's worked
examples are in the guide itself and are not drawn from any test set.
"""

from __future__ import annotations

import hashlib
import json
import pathlib

from sidechat.guide import GUIDE_FILE, GUIDE_VERSION
from sidechat.schema import SidechatRequest

ROOT = pathlib.Path(__file__).resolve().parents[2]

TO = ("agent", "person", "group", "device", "nobody", "unclear")
INTENT = ("direct", "indirect", "open", "about", "other")
DECISION = ("respond", "wait", "ignore")
RULE = ("G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8")

SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["to", "people", "intent", "decision", "speak", "rule", "reason"],
    "properties": {
        "to": {"type": "string", "enum": list(TO)},
        "people": {"type": "array", "items": {"type": "string"}},
        "intent": {"type": "string", "enum": list(INTENT)},
        "decision": {"type": "string", "enum": list(DECISION)},
        "speak": {"type": "integer", "enum": [1, 2, 3, 4, 5]},
        "rule": {"type": "string", "enum": list(RULE)},
        "reason": {"type": "string"},
    },
}

INSTRUCTIONS = """## How to answer

You will get one line to label, with the agent, the people present and the conversation before it.
Label only that line. Follow the guide above, applying its rules in order.

Answer with one JSON object:

- `to`, `people`, `intent`, `decision`, `speak`: as the guide defines them. `people` is an empty
  list unless `to` is `person`.
- `rule`: the guide rule (G1 to G8) that decided your answer.
- `reason`: one short sentence saying why.
"""


def guide_text() -> str:
    return (ROOT / GUIDE_FILE).read_text()


def system_prompt() -> str:
    return guide_text().rstrip() + "\n\n" + INSTRUCTIONS


def prompt_sha() -> str:
    """Changes whenever the guide, the instructions or the answer format change."""
    payload = json.dumps({"system": system_prompt(), "schema": SCHEMA}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:12]


def user_message(req: SidechatRequest) -> str:
    agent = req.agent
    names = f" Other names it answers to: {', '.join(agent.aliases)}." if agent.aliases else ""
    role = f" Role: {agent.role}." if agent.role else ""
    people = ", ".join(req.people) if req.people else "not known"
    lines = [
        f"Agent: {agent.name}.{names}{role}",
        f"People present: {people}.",
        "",
        "Conversation so far, oldest first:",
    ]
    if req.history:
        for n, t in enumerate(req.history, start=1):
            who = f"{agent.name} (the agent)" if t.agent else (t.speaker or "Someone")
            lines.append(f"{n}. {who}: {json.dumps(t.text, ensure_ascii=False)}")
    else:
        lines.append("(nothing yet)")
    speaker = req.speaker or "an unknown speaker"
    lines += ["", f"Line to label, said by {speaker}:", json.dumps(req.text, ensure_ascii=False)]
    if req.facts and req.facts.over_agent:
        lines.append("(Said while the agent was speaking.)")
    return "\n".join(lines)


def parse_answer(text: str) -> dict:
    """A member's reply as a checked answer. Raises ValueError when it does not fit the format."""
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("no JSON object in the reply")
    raw = json.loads(text[start : end + 1])
    answer = {
        "to": str(raw.get("to", "")).strip().lower(),
        "people": [str(p).strip() for p in (raw.get("people") or []) if str(p).strip()],
        "intent": str(raw.get("intent", "")).strip().lower(),
        "decision": str(raw.get("decision", "")).strip().lower(),
        "speak": int(raw.get("speak", 0)),
        "rule": str(raw.get("rule", "")).strip().upper(),
        "reason": str(raw.get("reason", "")).strip()[:400],
    }
    for field, allowed in (("to", TO), ("intent", INTENT), ("decision", DECISION)):
        if answer[field] not in allowed:
            raise ValueError(f"{field} {answer[field]!r} is not one of {allowed}")
    if not 1 <= answer["speak"] <= 5:
        raise ValueError(f"speak {answer['speak']} is not 1 to 5")
    if answer["to"] != "person":
        answer["people"] = []
    return answer


__all__ = ["GUIDE_VERSION", "SCHEMA", "parse_answer", "prompt_sha", "system_prompt", "user_message"]
