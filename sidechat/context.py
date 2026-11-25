"""The rhythm of the conversation before a line: who spoke, in what order, relative to its speaker.

Who a line is for often depends less on its words than on the turns before it: whether the agent
just spoke, whose question it answered, and whether the speaker is the person it was talking with.
The committee pilot (exp-002) showed this: most disagreements turned on "who was the agent's last
partner". The request already carries what is needed (each earlier turn's speaker, and `agent:
true` on the agent's own turns). This module turns that into the pattern "you spoke, they spoke,
you spoke" that the model reads, as roles and as a few numbers (SD-13).

Roles, relative to the speaker of the line being judged:

    agent    the agent
    speaker  the same person who says the line
    other    someone else; each other person gets a stable slot: other1, other2, ...
    unknown  a turn with no speaker tag (an undiarized transcript)
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

from sidechat.schema import SidechatRequest


def roles(req: SidechatRequest, slots: bool = False) -> list[str]:
    """Each earlier turn's role, oldest first. With `slots`, other people are other1, other2, ..."""
    order: dict[str, int] = {}
    out = []
    for t in req.history:
        if t.agent:
            out.append("agent")
        elif t.speaker is None or req.speaker is None:
            out.append("unknown")
        elif t.speaker == req.speaker:
            out.append("speaker")
        elif slots:
            order.setdefault(t.speaker, len(order) + 1)
            out.append(f"other{order[t.speaker]}")
        else:
            out.append("other")
    return out


@dataclass(frozen=True)
class Rhythm:
    """Numbers that summarise the turns before the line."""

    turns: int  # earlier turns in the window
    agent_turns: int  # how many of them are the agent's
    turns_since_agent: int | None  # 0: the agent spoke immediately before; None: not in the window
    agent_last_asked: bool  # the agent's latest turn ends in a question
    speaker_was_agent_partner: bool | None  # the agent's latest turn followed this speaker's line
    speaker_spoke_last: bool  # the line carries on the speaker's own previous turn
    speaker_turns: int  # the speaker's own earlier turns in the window
    others: int  # distinct other people in the window
    over_agent: bool | None  # said while the agent was speaking, when known

    def as_dict(self) -> dict:
        return asdict(self)


def rhythm(req: SidechatRequest) -> Rhythm:
    r = roles(req)
    last_agent = max((i for i, x in enumerate(r) if x == "agent"), default=None)
    partner = None
    if last_agent is not None and req.speaker is not None:
        before = [x for x in r[:last_agent] if x != "agent"]
        # The person whose line the agent's latest turn followed. An approximation: the agent may
        # have answered an earlier question, and the model also reads the words.
        partner = (before[-1] == "speaker") if before and before[-1] != "unknown" else None
    return Rhythm(
        turns=len(r),
        agent_turns=r.count("agent"),
        turns_since_agent=None if last_agent is None else len(r) - 1 - last_agent,
        agent_last_asked=bool(last_agent is not None and req.history[last_agent].text.rstrip().endswith("?")),
        speaker_was_agent_partner=partner,
        speaker_spoke_last=bool(r and r[-1] == "speaker"),
        speaker_turns=r.count("speaker"),
        others=len({t.speaker for t, x in zip(req.history, r) if x == "other"}),
        over_agent=req.facts.over_agent if req.facts else None,
    )


def render(req: SidechatRequest) -> str:
    """The turns and the line as the model's text input, newest last, with role tags for speakers.

    Names of earlier speakers are replaced by roles, so a name in the history is never mistaken for
    a name called in the line. The agent's own name stays in the
    words, because calling it by name is the strongest signal there is.
    """
    tags = roles(req, slots=True)
    parts = [f"[{tag}] {t.text}" for tag, t in zip(tags, req.history)]
    who = "speaker" if req.speaker is not None else "unknown"
    over = " (over the agent)" if req.facts and req.facts.over_agent else ""
    parts.append(f">> [{who}]{over} {req.text}")
    return "\n".join(parts)
