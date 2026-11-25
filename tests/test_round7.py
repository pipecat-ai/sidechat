"""Student round 2: people-only histories and the gate."""

from __future__ import annotations

from sidechat import conditions
from sidechat.schema import SidechatRequest


def _row() -> dict:
    return {
        "row_id": "x/1",
        "tags": {"kind": "follow_up"},
        "label": {},
        "request": {
            "agent": {"name": "Atlas"},
            "speaker": "Speaker 1",
            "text": "And Tuesday?",
            "history": [
                {"speaker": "Speaker 1", "text": "Atlas, flights to Lisbon on Monday?", "agent": False},
                {"speaker": "Atlas", "text": "Two direct ones, at 9 and at 14.", "agent": True},
            ],
            "facts": {"alone": False, "over_agent": True},
        },
    }


def test_people_only_drops_the_agent_side():
    row = _row()
    po = conditions.people_only(row)
    req = SidechatRequest(**po["request"])
    assert [t.agent for t in req.history] == [False]
    assert req.facts.over_agent is None and req.facts.alone is False
    assert po["tags"]["people_only"] == "1" and po["tags"]["kind"] == "follow_up"
    assert len(row["request"]["history"]) == 2 and "people_only" not in row["tags"]  # the row itself is untouched


def _m(**v) -> dict:
    base = {"duplex": 0.967, "ami": 0.999, "pilot": 0.874, "explicit_t": 0.995, "implicit_t": 0.388}
    base.update(v)
    return {k: {"value": x, "k": 0, "n": 1} for k, x in base.items()}


def test_gate():
    from sidechat.pipeline.student_gate import gate_one

    t = _m()
    assert gate_one(_m(duplex=0.960, implicit_t=0.30), t, 12.0, 60.0, 0.266, True)["ships"]
    assert not gate_one(_m(duplex=0.9563), t, 12.0, 60.0, 0.266, True)["ships"]  # 1.04 points behind
    assert not gate_one(_m(explicit_t=0.878, implicit_t=0.30), t, 12.0, 60.0, 0.266, True)["ships"]  # item 4
    assert not gate_one(_m(implicit_t=0.107), t, 12.0, 60.0, 0.266, True)["ships"]  # item 5
    assert not gate_one(_m(implicit_t=0.30), t, 70.0, 60.0, 0.266, True)["ships"]  # slower than Jev
    assert not gate_one(_m(implicit_t=0.30), t, None, 60.0, 0.266, True)["ships"]  # not timed
    assert not gate_one(_m(implicit_t=0.30), t, 12.0, 60.0, 0.266, False)["ships"]  # parity
