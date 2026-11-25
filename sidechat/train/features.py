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


def _last(req: SidechatRequest, n: int) -> SidechatRequest:
    """The request with only its last `n` earlier turns."""
    if n >= len(req.history):
        return req
    return req.model_copy(update={"history": req.history[len(req.history) - n :]})


def fitted(req: SidechatRequest, turns: int, max_len: int, count) -> tuple[str, int]:
    """The text with at most `turns` earlier turns, dropping the oldest until `count(text)` tokens
    fit in `max_len`, so the line and the agent's card are never cut. For the short-input models
    (config `text_turns`); the rhythm numbers still read the whole history."""
    keep = min(turns, len(req.history))
    while True:
        t, start = text(_last(req, keep))
        if keep == 0 or count(t) <= max_len:
            return t, start
        keep -= 1


def _card(req: SidechatRequest) -> str:
    a = req.agent
    card = f"agent: {a.name}"
    if a.aliases:
        card += f" | also: {', '.join(a.aliases)}"
    if a.role:
        card += f" | {a.role}"
    return card


def text(req: SidechatRequest, turns: int = 0) -> tuple[str, int]:
    """The encoder's text, and where the line itself starts in it (a character offset). `turns`
    keeps only the last so many earlier turns (0: all of them)."""
    if turns:
        req = _last(req, turns)
    full = _card(req) + "\n" + context.render(req)
    return full, full.rfind(LINE_MARK)


# --- two towers (sidechat-tt-0.1) ---------------------------------------------------------------
# The history and the line are encoded apart, so the history's encoding can be made while the next
# person is still talking and only the line is encoded when they stop. The history therefore cannot
# depend on who speaks next: its people get fixed slots by first appearance ([p1], [p2], ...), and
# the line carries its speaker's slot ([new] for someone not in the window). The rhythm numbers,
# cheap to compute at the end, still read the turns relative to the speaker.

TT_VERSION = "sidechat-tt-0.1"


def _slots(req: SidechatRequest) -> dict[str, int]:
    order: dict[str, int] = {}
    for t in req.history:
        if not t.agent and t.speaker is not None:
            order.setdefault(t.speaker, len(order) + 1)
    return order


def context_text(req: SidechatRequest, turns: int | None = None) -> str:
    """The history tower's text: the agent's card and the earlier turns (the last `turns` of them)."""
    if turns is not None:
        req = _last(req, turns)
    order = _slots(req)
    parts = []
    for t in req.history:
        tag = "agent" if t.agent else "unknown" if t.speaker is None else f"p{order[t.speaker]}"
        parts.append(f"[{tag}] {t.text}")
    return _card(req) + "\n" + ("\n".join(parts) if parts else "(start of the conversation)")


def context_fitted(req: SidechatRequest, max_len: int, count) -> str:
    """`context_text`, dropping the oldest turns until it fits `max_len` tokens."""
    keep = len(req.history)
    while True:
        t = context_text(req, keep)
        if keep == 0 or count(t) <= max_len:
            return t
        keep -= 1


def line_text(req: SidechatRequest) -> str:
    """The line tower's text: the agent's card and the line, tagged with its speaker's slot."""
    order = _slots(req)
    if req.speaker is None:
        tag = "unknown"
    else:
        tag = f"p{order[req.speaker]}" if req.speaker in order else "new"
    over = " (over the agent)" if req.facts and req.facts.over_agent else ""
    return f"{_card(req)}\n{LINE_MARK}[{tag}]{over} {req.text}"


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
