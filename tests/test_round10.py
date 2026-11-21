"""Round 10: gen-0.5's kinds for the lines after the agent answers (exp-063's weak spot)."""

from __future__ import annotations

import random
from collections import Counter

from sidechat import guide
from sidechat.gen import planner, world
from sidechat.gen.writer import BRIEFS, MUST_CALL, MUST_MENTION

NEW = ("people_question_after_agent", "partner_to_people_after_agent", "follow_up_later")
ADD = {"people_question_after_agent": 3.0, "partner_to_people_after_agent": 2.5, "follow_up_later": 4.0}


def _plans(n: int, seed: str, **kw) -> list[list]:
    rng = random.Random(seed)
    return [planner.plan(rng, world.make_cast(rng), quiet=None, **kw) for _ in range(n)]


def test_new_kinds_have_labels_and_briefs_and_never_call_the_agent():
    assert guide.KINDS["people_question_after_agent"].expect == "ignore"
    assert guide.KINDS["partner_to_people_after_agent"].expect == "ignore"
    assert guide.KINDS["follow_up_later"].expect == "wait"
    assert guide.KINDS["follow_up_later"].speak == 3
    for k in NEW:
        assert k in BRIEFS and k in planner.ADDED
        assert k not in MUST_CALL and k not in MUST_MENTION  # the writer check flags any use of the name


def test_off_by_default():
    kinds = Counter(b.kind for p in _plans(300, "r10-off") for b in p)
    assert all(kinds[k] == 0 for k in NEW)


def test_after_agent_kinds_follow_an_answer_and_the_later_one_comes_from_the_partner():
    seen = Counter()
    for p in _plans(600, "r10-on", add=ADD):
        partner, ago = None, 99
        for i, b in enumerate(p):
            if b.who == planner.AGENT:
                partner, ago, act = b.extra.get("partner"), 0, b.act
                continue
            if b.kind in ("people_question_after_agent", "partner_to_people_after_agent"):
                assert p[i - 1].who == planner.AGENT and p[i - 1].act in ("answer", "answer_open", "act")
                if b.kind == "partner_to_people_after_agent":
                    assert b.who == partner
            if b.kind == "follow_up_later":
                assert b.who == partner and 2 <= ago <= 6 and act in ("answer", "answer_open", "act")
            if b.kind:
                seen[b.kind] += 1
            ago += 1
    assert all(seen[k] >= 30 for k in NEW), seen


def test_tcl_paired_and_the_gate():
    from sidechat.pipeline.student_gate import gate_r10, tcl_paired

    rows = [{"row_id": f"o{i}", "tags": {"kind": "people"}} for i in range(400)]
    rows += [{"row_id": f"c{i}", "tags": {"kind": "contextual"}} for i in range(40)]
    base = {r["row_id"]: "ignore" for r in rows}
    for i in range(30):
        base[f"o{i}"] = "respond"  # rc0.3 answers 30 people's lines outright
    new = dict(base)
    for i in range(25):
        new[f"o{i}"] = "wait"  # the new build holds 25 of them instead
    p = tcl_paired(new, base, rows)
    assert p["others_not_outright"]["diff"] > 0 and p["others_not_outright"]["ci95"][0] > 0
    share = {"value": 0.5, "k": 1, "n": 2}
    m = {k: share for k in ("tcl_direct", "slurp_unnamed_held_heard", "duplex", "ambient", "ami", "generated")}
    m |= {k: share for k in ("pilot", "explicit_t", "slurp_named_keyterm", "duplex_held", "ami_heard_held", "tcl_held")}
    m["duplex_outright"] = {"value": 0.002, "k": 1, "n": 500}
    assert gate_r10(m, m, p)["ships"]
    assert not gate_r10(m, m, tcl_paired(base, base, rows))["ships"]  # no fewer outright answers: no ship
    worse = m | {"tcl_held": {"value": 0.6, "k": 6, "n": 10}}
    assert not gate_r10(worse, m, p)["ships"]  # more holds on people's lines past the margin
