"""What the model reads for one line: text for the encoder, and a small vector of numbers.

The text is the agent's card, then the earlier turns tagged by role, then the line:

    agent: Atlas | also: at last | AI assistant on the call
    [other1] Morning.
    [speaker] Atlas, how far is Leeds from York?
    [agent] About twenty-five miles.
    >> [speaker] And by train?

The numbers are the rhythm of the turns (`sidechat/context.py`, SD-13) and a few word cues the
encoder could learn but learns faster when told: whether the agent's name is called, whether a
person's name is called, whether another device is addressed. Version `sidechat-input-0.1`. No
torch here, so the runtime and the tests can use it.
"""

from __future__ import annotations

import re

from sidechat import context
from sidechat.schema import SidechatRequest

INPUT_VERSION = "sidechat-input-0.2"  # 0.2 added the trailing vocative
LINE_MARK = ">> "
DEVICE_WORDS = ("siri", "ok google", "hey google", "alexa", "cortana", "hey tv", "ok car")
ROLE_RE = re.compile(r"\b(assistant|ai|bot)\b", re.IGNORECASE)
OPEN_RE = re.compile(r"\b(anyone|anybody|someone|somebody|everyone|everybody|you guys|you all|y'all)\b", re.IGNORECASE)
YOU_RE = re.compile(r"\byou(r|rs|'re|'ll|'ve|'d)?\b", re.IGNORECASE)
VOCATIVE_RE = re.compile(r"^\W*(?:hey |ok |okay |oh |so |right |well )?([A-Z][a-z]+)\s*[,!?]")
TRAILING_VOCATIVE_RE = re.compile(r",\s*([A-Z][a-z]+)\s*[?.!]*\s*$")


def text(req: SidechatRequest) -> tuple[str, int]:
    """The encoder's text, and where the line itself starts in it (a character offset)."""
    a = req.agent
    card = f"agent: {a.name}"
    if a.aliases:
        card += f" | also: {', '.join(a.aliases)}"
    if a.role:
        card += f" | {a.role}"
    body = context.render(req)
    full = card + "\n" + body
    return full, full.rfind(LINE_MARK)


def _calls(line: str, req: SidechatRequest) -> tuple[bool, bool, bool]:
    """(the agent is named anywhere, named at the start, named at the end)."""
    a = req.agent
    pats = [re.compile(rf"(?<!\w){re.escape(a.name)}(?!\w)")] + [
        re.compile(rf"(?<!\w){re.escape(x)}(?!\w)", re.IGNORECASE) for x in a.aliases
    ]
    hits = [m for p in pats for m in p.finditer(line)]
    if not hits:
        return False, False, False
    start = min(m.start() for m in hits) <= 12
    end = max(m.end() for m in hits) >= len(line.rstrip(" ?.!,")) - 2
    return True, start, end


def numbers(req: SidechatRequest) -> list[float]:
    r = context.rhythm(req)
    line = req.text
    low = line.lower()
    since = r.turns_since_agent
    out: list[float] = []
    out += [float(since == k) for k in (0, 1, 2)] + [float(since is not None and since >= 3), float(since is None)]
    out += [float(r.agent_last_asked)]
    p = r.speaker_was_agent_partner
    out += [float(p is True), float(p is False), float(p is None)]
    out += [
        float(r.speaker_spoke_last),
        min(r.speaker_turns, 8) / 8,
        min(r.agent_turns, 8) / 8,
        min(r.others, 5) / 5,
        min(r.turns, 8) / 8,
    ]
    o = r.over_agent
    out += [float(o is True), float(o is False), float(o is None)]
    out += [float(req.speaker is not None), float(bool(req.people))]
    called, at_start, at_end = _calls(line, req)
    out += [float(called), float(at_start), float(at_end)]
    out += [float(bool(ROLE_RE.search(line))), float(any(w in low for w in DEVICE_WORDS)), float("?" in line)]
    out += [float(bool(YOU_RE.search(line))), float(bool(OPEN_RE.search(line))), min(len(line.split()), 30) / 30]
    names = [n for n in (req.people or []) if n and n != req.speaker]
    out += [float(any(re.search(rf"(?<!\w){re.escape(n)}(?!\w)", line) for n in names))]
    m = VOCATIVE_RE.match(line)
    out += [float(bool(m) and m.group(1) != req.agent.name)]
    m = TRAILING_VOCATIVE_RE.search(line)
    out += [float(bool(m) and m.group(1) != req.agent.name)]
    return out


NUM_DIM = len(numbers(SidechatRequest(agent={"name": "X"}, text="x")))
