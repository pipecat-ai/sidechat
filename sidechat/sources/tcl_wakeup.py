"""TCL Research Europe's Intelligent Wakeup: conversations among people with a voice assistant,
"Sigma", in the room. The test split, text only.

Source: https://huggingface.co/datasets/TCLResearchEurope/intelligent_wakeup at v1.0.1 (CC BY-NC 4.0).
The conversations are written by a language model and spoken by text-to-speech; only the text is
used here. TEST ONLY (SD-27): never trained on, and neither its text nor the converted rows go into
git or onto the Hub. `sidechat.pipeline.tcl` keeps the test split's text columns in R2.

Its own label (`experiments/audio_experiments/dataset_lib/labels.py` in its code repo): a person's
turn is for the assistant when the assistant speaks next. It is `direct` if it contains "sigma"
(their substring rule) and `contextual` if not, a follow-up in an exchange with Sigma. Every other
person's turn is non-assistance. Sigma's own turns are not scored; they stay in the history as the
agent's.

Kinds, in `tags["kind"]`:

    direct       for Sigma, with its name
    contextual   for Sigma, without its name
    named_other  not followed by Sigma, but with its name (a thanks, a mention)
    people       the rest of a session in which Sigma is addressed
    no_va        a session in which Sigma never is (the twin of one in which it is)

The benchmark does not say whom other lines were for. `to` is "person" for the people's lines of a
session with two or more people, "unknown" for a single person's (talking to themselves, a pet, the
phone) and for lines that name Sigma without a reply.

The text carries directions for the voice ("[thoughtful]", "*really*"). They are not speech and are
removed.
"""

from __future__ import annotations

import re

from sidechat.schema import Agent, SidechatLabel, SidechatRecord, SidechatRequest, Turn, window

SET = "tcl-wakeup-0.1"
REPO = "TCLResearchEurope/intelligent_wakeup"
REVISION = "c4486633e6093e1be6933b62255d1029051c0491"  # tag v1.0.1, as TCL's own results
SPLIT = "test"
FILES = tuple(f"data/test-0000{i}-of-00005.parquet" for i in range(5))
COLUMNS = (
    "id",
    "scenario_name",
    "category",
    "variant_type",
    "conversation_type",
    "has_va",
    "num_turns",
    "duration_seconds",
    "speakers",
    "turns",
    "group_key",
    "split",
)
TEXT_PREFIX = "sources/tcl-wakeup-v1.0.1"  # under r2.PREFIX: test.jsonl and manifest.json
LICENCE = "CC BY-NC 4.0"
USE = "test only, never trained on; text and rows stay out of git and off the Hub (SD-27)"

AGENT_NAME = "Sigma"
AGENT = Agent(name=AGENT_NAME, role="voice assistant in the room")
WAKE = "sigma"
FOR_AGENT = ("direct", "contextual")
KINDS = ("direct", "contextual", "named_other", "people", "no_va")

_DIRECTION = re.compile(r"\[[^\]]*\]")


def clean(text: str) -> str:
    """The words as spoken: directions for the voice removed, spacing tidied."""
    return " ".join(_DIRECTION.sub(" ", text).replace("*", "").split())


def kind(turns: list[dict], i: int, has_va: bool) -> str:
    """The benchmark's trigger type for person's turn `i`, with its non-assistance turns split."""
    nxt = turns[i + 1] if i + 1 < len(turns) else None
    expected = nxt is not None and nxt["speaker"] == AGENT_NAME
    named = WAKE in (turns[i]["content"] or "").lower()
    if expected:
        return "direct" if named else "contextual"
    if named:
        return "named_other"
    return "people" if has_va else "no_va"


def label(k: str, multi: bool) -> SidechatLabel:
    if k in FOR_AGENT:
        return SidechatLabel(to="agent", intent="direct", expect="respond", respond=1.0, source="benchmark")
    if k == "named_other":
        return SidechatLabel(to="unknown", intent="about", expect="ignore", respond=0.0, source="benchmark")
    return SidechatLabel(
        to="person" if multi else "unknown", intent="other", expect="ignore", respond=0.0, source="benchmark"
    )


def convert(sessions: list[dict]) -> list[dict]:
    """One record per person's turn. `sessions` are the test split's rows without the audio."""
    rows = []
    for s in sessions:
        if s.get("split", SPLIT) != SPLIT:
            raise ValueError(f"{s['id']} is in {s['split']!r}: only the test split is used")
        raw = s["turns"]
        turns = [Turn(speaker=t["speaker"], text=clean(t["content"]), agent=t["speaker"] == AGENT_NAME) for t in raw]
        people = [p for p in s["speakers"] if p != AGENT_NAME]
        multi = s["conversation_type"] != "single_user"
        for i, t in enumerate(raw):
            if t["speaker"] == AGENT_NAME:
                continue
            k = kind(raw, i, bool(s["has_va"]))
            rec = SidechatRecord(
                row_id=f"{SET}/{s['id']}/{i}",
                set=SET,
                conv_id=s["group_key"],  # a session and its no-assistant twin stay together
                turn_index=i,
                request=SidechatRequest(
                    agent=AGENT, text=turns[i].text, speaker=t["speaker"], history=window(turns, i), people=people
                ),
                label=label(k, multi),
                tags={
                    "kind": k,
                    "trigger": k if k in FOR_AGENT else "non-assistance",
                    "conversation_type": s["conversation_type"],
                    "category": s["category"],
                    "has_va": "1" if s["has_va"] else "0",
                    "after_agent": "1" if any(x["speaker"] == AGENT_NAME for x in raw[:i]) else "0",
                },
            )
            rows.append(rec.model_dump(mode="json"))
    return rows


def measures(rows: list[dict], dec: dict[str, str], hours: float) -> dict:
    """TCL's measures and each kind's decisions, for one system's decisions (row_id -> respond, wait
    or ignore). Rows the system has no decision for are left out and counted in `missing`."""
    from sidechat.lib.score import share

    have = [r for r in rows if r["row_id"] in dec]
    out: dict = {"n": len(have), "missing": len(rows) - len(have)}
    for k in KINDS:
        d = [dec[r["row_id"]] for r in have if r["tags"]["kind"] == k]
        out[k] = {x: share(sum(y == x for y in d), len(d)) for x in ("respond", "wait", "ignore")}
    pos = [dec[r["row_id"]] for r in have if r["tags"]["kind"] in FOR_AGENT]
    neg = [dec[r["row_id"]] for r in have if r["tags"]["kind"] not in FOR_AGENT]
    for name, accept in (("now", ("respond",)), ("now_or_held", ("respond", "wait"))):
        tp = sum(d in accept for d in pos)
        fp = sum(d in accept for d in neg)
        precision = tp / (tp + fp) if tp + fp else None
        f1 = 2 * tp / (2 * tp + fp + len(pos) - tp) if pos or fp else None
        out[name] = {
            "tp": tp,
            "fp": fp,
            "fn": len(pos) - tp,
            "tn": len(neg) - fp,
            "precision": round(precision, 4) if precision is not None else None,
            "recall": share(tp, len(pos)),
            "f1": round(f1, 4) if f1 is not None else None,
            "false_accepts": share(fp, len(neg)),
            "fa_per_hour": round(fp / hours, 2) if hours else None,
        }
    return out
