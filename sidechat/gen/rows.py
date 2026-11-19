"""A written conversation becomes labelled rows: one per person's line, label from its kind.

Splits are by conversation. A conversation goes to `test` when its writer is held out, its setting
is held out, or its agent's name is held out. Otherwise a hash of its id puts it in train (84%),
dev (8%) or test (8%).
"""

from __future__ import annotations

import hashlib

from sidechat import guide
from sidechat.gen.planner import AGENT, Beat
from sidechat.gen.world import Cast
from sidechat.schema import Agent, Facts, SidechatRecord, SidechatRequest, Turn, window

PERSON_KINDS = {k for k, r in guide.KINDS.items() if r.to in ("person", "group")}


# Brief problems that leave the kind's label right: a remark about the agent that says "it" instead of
# its name is still for the people, and a question to a person that leaves out their name is still
# for a person. Anything else (the agent called when it should not be, or not called when it should)
# may change who the line is for, so the line is left out of training until the committee decides.
SAFE_PROBLEMS = {"does not mention the agent", "does not point at the agent", "word missing", "alias phrase missing"}


def label_safe(kind: str, problems: list[str]) -> bool:
    if not problems:
        return True
    rule = guide.KINDS[kind]
    for p in problems:
        if p in SAFE_PROBLEMS and rule.expect == "ignore":
            continue
        if p.startswith("does not name ") and rule.to in ("person", "group"):
            continue
        return False
    return True


def split_for(conv_id: str, heldout: list[str]) -> str:
    if heldout:
        return "test"
    h = int(hashlib.sha256(conv_id.encode()).hexdigest()[:8], 16) % 100
    return "train" if h < 84 else "dev" if h < 92 else "test"


def agent_card(cast: Cast) -> Agent:
    if cast.unnamed:
        return Agent(name="Assistant", aliases=["the assistant", "the AI", "the bot"], role=cast.setting.role)
    return Agent(name=cast.agent, aliases=list(cast.aliases), role=cast.setting.role)


def conversation_rows(
    set_name: str,
    conv_id: str,
    cast: Cast,
    beats: list[Beat],
    texts: list[str],
    problems: list[list[str]],
    writer: str,
    heldout_writer: bool,
) -> list[dict]:
    agent = agent_card(cast)
    turns = [
        Turn(speaker=agent.name if b.who == AGENT else b.who, text=t, agent=b.who == AGENT)
        for b, t in zip(beats, texts)
    ]
    heldout = list(cast.heldout) + (["writer"] if heldout_writer else [])
    split = split_for(conv_id, heldout)
    rows = []
    for i, (b, text, why) in enumerate(zip(beats, texts, problems)):
        if b.who == AGENT:
            continue
        label = guide.label_for(b.kind, b.target if b.kind in PERSON_KINDS else None)
        rec = SidechatRecord(
            row_id=f"{set_name}/{conv_id}/{i}",
            set=set_name,
            conv_id=conv_id,
            turn_index=i,
            request=SidechatRequest(
                agent=agent,
                text=text,
                speaker=b.who,
                history=window(turns, i),
                people=list(cast.people),
                facts=Facts(over_agent=True) if b.over_agent else None,
            ),
            label=label,
            tags={
                "kind": b.kind,
                "rule": guide.KINDS[b.kind].rule,
                "setting": cast.setting.id,
                "writer": writer,
                "register": cast.register,
                "split": split,
                "heldout": ",".join(heldout),
                "brief_ok": "0" if why else "1",
                "label_safe": "1" if label_safe(b.kind, why) else "0",
                "brief_problems": "; ".join(why),
                "agent_name": agent.name,
                "unnamed_agent": "1" if cast.unnamed else "0",
            },
        )
        rows.append(rec.model_dump(mode="json"))
    return rows
