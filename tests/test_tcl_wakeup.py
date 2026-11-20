"""The TCL Intelligent Wakeup converter, on made-up sessions (none of the set's text is in git, SD-27)."""

from __future__ import annotations

import pytest

from sidechat.sources import tcl_wakeup as TW


def _session(sid: str, turns: list[tuple[str, str]], has_va: bool = True, multi: bool = True) -> dict:
    speakers = sorted({s for s, _ in turns} | ({"Sigma"} if has_va else set()))
    return {
        "id": sid,
        "category": "Made",
        "conversation_type": "multi_user" if multi else "single_user",
        "has_va": has_va,
        "speakers": speakers,
        "turns": [{"speaker": s, "content": c, "time": float(i)} for i, (s, c) in enumerate(turns)],
        "group_key": sid.replace("no_va_", ""),
        "duration_seconds": 60.0,
        "split": "test",
    }


SESSIONS = [
    _session(
        "Made/couple/kettle",
        [
            ("Ann", "[sighs] Is the kettle on?"),
            ("Bo", "It is. *Really* this time."),
            ("Ann", "Sigma, how long do eggs boil?"),
            ("Sigma", "About seven minutes."),
            ("Bo", "And soft ones?"),
            ("Sigma", "Five or six."),
            ("Ann", "Thanks, Sigma."),
            ("Bo", "Toast too?"),
        ],
    ),
    _session("Made/couple/no_va_kettle", [("Ann", "Is the kettle on?"), ("Bo", "It is.")], has_va=False),
    _session(
        "Made/single/plant",
        [("Cy", "Where did I put it?"), ("Cy", "Sigma, water the plant?"), ("Sigma", "Done.")],
        multi=False,
    ),
]


def test_kinds_follow_tcls_own_label():
    rows = TW.convert(SESSIONS)
    kinds = [r["tags"]["kind"] for r in rows]
    assert kinds == [
        "people",
        "people",
        "direct",
        "contextual",
        "named_other",
        "people",
        "no_va",
        "no_va",
        "people",
        "direct",
    ]
    assert all(r["request"]["speaker"] != "Sigma" for r in rows)  # Sigma's own turns are not scored
    by = {r["row_id"]: r for r in rows}
    assert by["tcl-wakeup-0.1/Made/couple/kettle/2"]["label"]["expect"] == "respond"
    assert by["tcl-wakeup-0.1/Made/couple/kettle/6"]["label"]["expect"] == "ignore"
    assert by["tcl-wakeup-0.1/Made/couple/kettle/6"]["label"]["to"] == "unknown"
    assert by["tcl-wakeup-0.1/Made/couple/kettle/0"]["label"]["to"] == "person"
    assert by["tcl-wakeup-0.1/Made/single/plant/0"]["label"]["to"] == "unknown"  # alone: not "person"


def test_directions_removed_and_agent_turns_kept():
    rows = TW.convert(SESSIONS)
    first, second = rows[0], rows[1]
    assert first["request"]["text"] == "Is the kettle on?"
    assert second["request"]["text"] == "It is. Really this time."
    follow = rows[3]  # "And soft ones?"
    hist = follow["request"]["history"]
    assert hist[-1] == {"speaker": "Sigma", "text": "About seven minutes.", "agent": True}
    assert follow["tags"]["after_agent"] == "1" and rows[0]["tags"]["after_agent"] == "0"
    assert first["request"]["people"] == ["Ann", "Bo"]
    assert first["conv_id"] == rows[6]["conv_id"]  # a session and its no-assistant twin stay together


def test_only_the_test_split():
    with pytest.raises(ValueError):
        TW.convert([{**SESSIONS[0], "split": "train"}])


def test_measures():
    rows = TW.convert(SESSIONS)
    dec = {r["row_id"]: "ignore" for r in rows}
    dec[rows[2]["row_id"]] = "respond"  # direct, answered
    dec[rows[3]["row_id"]] = "wait"  # contextual, held
    dec[rows[0]["row_id"]] = "respond"  # a person's line, answered
    m = TW.measures(rows, dec, hours=0.5)
    assert (m["now"]["tp"], m["now"]["fp"], m["now"]["fn"]) == (1, 1, 2)
    assert m["now"]["precision"] == 0.5 and m["now"]["fa_per_hour"] == 2.0
    assert (m["now_or_held"]["tp"], m["now_or_held"]["fn"]) == (2, 1)
    assert m["contextual"]["wait"]["k"] == 1 and m["direct"]["respond"]["k"] == 1
    assert m["missing"] == 0 and m["n"] == len(rows)
