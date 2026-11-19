"""Majority of three, field by field, and the committee's label.

A field takes the value at least two members gave. Without one, it has no majority: a line with
no majority on its decision has no committee decision, which counts as a disagreement with the
guide. `speak` is the mean of the members' 1-to-5 ratings.
"""

from __future__ import annotations

from collections import Counter

from sidechat.guide import speak_to_respond
from sidechat.schema import SidechatLabel

FIELDS = ("to", "intent", "decision", "rule")


def vote(answers: dict[str, dict | None], quorum: int = 2) -> dict:
    got = {m: a for m, a in answers.items() if a}
    out: dict = {"members": sorted(got), "n": len(got)}
    for f in FIELDS:
        if not got:
            out[f], out[f"{f}_votes"] = None, 0
            continue
        value, n = Counter(a[f] for a in got.values()).most_common(1)[0]
        out[f] = value if n >= quorum else None
        out[f"{f}_votes"] = n
    out["speak"] = round(sum(a["speak"] for a in got.values()) / len(got), 3) if got else None
    people = Counter(p for a in got.values() for p in a.get("people", []))
    out["people"] = sorted(p for p, n in people.items() if n >= quorum)
    out["unanimous"] = (
        bool(got)
        and len(got) == len(answers)
        and all(len({a[f] for a in got.values()}) == 1 for f in ("decision", "intent"))
    )
    return out


def committee_label(v: dict) -> SidechatLabel | None:
    """The committee's label, or None when no two members answered."""
    if v["n"] < 2:
        return None
    to = v["to"] or "unclear"
    return SidechatLabel(
        to="unknown" if to == "unclear" else to,
        to_people=v["people"] if to == "person" else [],
        intent=v["intent"],
        expect=v["decision"],
        respond=speak_to_respond(v["speak"]),
        unclear=to == "unclear",
        source="committee",
    )
