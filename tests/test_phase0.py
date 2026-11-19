"""Phase 0: the schema, the converters, the Jev wording and the scorecard. No network."""

from __future__ import annotations

import pathlib

import pytest

from sidechat.baselines import jev_demo, name_only
from sidechat.lib import score
from sidechat.pipeline import scorecard
from sidechat.schema import Agent, SidechatAnswer, SidechatRecord, SidechatRequest, Turn, window
from sidechat.sources import ambient_bench, duplex_mpe, suites

DEMO = pathlib.Path.home() / "Sites" / "daily-audience" / "server" / "addressing.py"


def test_answer_checks_probabilities():
    ok = SidechatAnswer(intent={"direct": 0.7, "indirect": 0.1, "open": 0.1, "about": 0.05, "other": 0.05}, respond=0.9)
    assert ok.addressed == pytest.approx(0.8) and ok.open_question == pytest.approx(0.1)
    with pytest.raises(ValueError):
        SidechatAnswer(intent={"direct": 0.7, "indirect": 0.1, "open": 0.1, "about": 0.05, "other": 0.5}, respond=0.9)
    with pytest.raises(ValueError):
        SidechatAnswer(intent={"direct": 1.0}, respond=0.9)


def test_history_is_capped():
    turns = [Turn(speaker="A", text=str(i)) for i in range(12)]
    assert [t.text for t in window(turns, 10)] == [str(i) for i in range(2, 10)]
    with pytest.raises(ValueError):
        SidechatRequest(agent=Agent(name="Atlas"), text="x", history=turns)


@pytest.mark.skipif(not DEMO.exists(), reason="the daily-audience demo is not on this machine")
def test_jev_wording_matches_the_demo():
    source = DEMO.read_text()
    for template in (jev_demo.ADDRESSED, jev_demo.QUESTION):
        for fragments in template.values():
            for fragment in fragments:
                assert fragment in source, fragment
    for fragment in jev_demo.CALL:
        assert fragment in source, fragment
    assert "respond_threshold: float = 0.8" in source and "question_threshold: float = 0.5" in source
    assert "history: int = 8" in source


def test_jev_state_is_the_demo_shape():
    req = SidechatRequest(
        agent=Agent(name="Atlas", aliases=["at last"]),
        text="hey at last, what time is it?",
        speaker="Jon",
        people=["Jon", "Sam"],
        history=[Turn(speaker="Sam", text="Hi."), Turn(speaker="Atlas", text="Hello.", agent=True)],
    )
    state = jev_demo.state(req)
    assert state["call"].startswith("A live video call. People on the call: Jon, Sam. Atlas is an AI voice assistant")
    assert state["earlier_messages"] == [{"speaker": "Sam", "said": "Hi."}, {"speaker": "Atlas", "said": "Hello."}]
    assert state["latest_message"] == {"speaker": "Jon", "said": "hey Atlas, what time is it?"}
    assert "Atlas" in jev_demo.questions("Atlas")["addressed"]["instructions"]
    assert jev_demo.key("m", req) == jev_demo.key("m", req.model_copy(deep=True)) != jev_demo.key("m2", req)
    assert [jev_demo.decision(a, q) for a, q in ((0.8, 0.0), (0.79, 0.5), (0.1, 0.49))] == ["respond", "wait", "ignore"]


def _duplex_scenario(condition: str) -> dict:
    turns = [
        ("A", "Option one is tacos.", "N2", "other_human", "statement"),
        (
            "D",
            "Aria, which is cheapest?" if condition == "explicit" else "You logged them, which is cheapest?",
            "T",
            "aria",
            "request",
        ),
        ("A", "This is why we keep Aria around.", "N1", "other_human", "statement"),
        ("B", "Hey Siri, how long is the bus?", "N2", "device", "request"),
        ("C", "Nine bucks, hmm.", "N3", "none", "self_talk"),
        ("A", "Aria, do they take card?", "N4_Q", "aria", "question"),
        ("A", "Never mind, they do.", "N4_R", "other_human", "statement"),
        ("B", "Odd one.", "N2", "aria", "statement"),
    ]
    return {
        "scenario_id": f"s0_{condition}",
        "pair_id": "s0",
        "addressing": condition,
        "trigger_index": 1,
        "n_speakers": 4,
        "turns": [
            {"turn_index": i, "speaker": s, "text": t, "event_type": e, "addressee": a, "speech_act": sa}
            for i, (s, t, e, a, sa) in enumerate(turns)
        ],
    }


def test_duplex_labels():
    rows = [SidechatRecord(**r) for r in duplex_mpe.convert([_duplex_scenario("explicit")])]
    assert [r.label.expect for r in rows] == [
        "ignore",
        "respond",
        "ignore",
        "ignore",
        "ignore",
        "respond",
        "ignore",
        "ignore",
    ]
    assert [r.label.to for r in rows] == ["person", "agent", "person", "device", "nobody", "agent", "person", "unknown"]
    assert rows[2].label.intent == "about" and rows[1].label.intent == "direct"
    assert [r.tags["conflict"] for r in rows] == ["0"] * 7 + ["1"]
    assert rows[5].request.people == ["A", "B", "C", "D"] and len(rows[5].request.history) == 5
    assert rows[0].conv_id == "s0"


def test_ambient_labels():
    scenario = {
        "id": "x1",
        "category": "direct_factual",
        "turns": [
            {"turn_index": 0, "speaker": "Alex", "message": "hi all", "expected_output": "SILENT"},
            {"turn_index": 1, "speaker": "Sam", "message": "alfi what year was it", "expected_output": "RESPOND"},
        ],
    }
    rows = [SidechatRecord(**r) for r in ambient_bench.convert([scenario])]
    assert [r.label.expect for r in rows] == ["ignore", None] and [r.tags["bench"] for r in rows] == [
        "SILENT",
        "RESPOND",
    ]
    assert rows[1].request.people == ["Alex", "Sam"] and rows[1].request.history[0].text == "hi all"


@pytest.mark.parametrize("which", sorted(suites.SUITE_FILES))
def test_suites_load(which):
    if not (suites.SUITES_DIR / suites.SUITE_FILES[which]).exists():
        pytest.skip(f"{which} suite not written yet")
    rows = [SidechatRecord(**r) for r in suites.convert(suites.load(which))]
    assert rows and len({r.row_id for r in rows}) == len(rows)
    for r in rows:
        assert r.tags["kind"] and r.request.speaker != r.request.agent.name
        if r.label.to == "person" and r.label.to_people:
            assert set(r.label.to_people) <= set(r.request.people or []), r.row_id


def test_suite_codes_and_context_lines():
    suite = {
        "suite": "t",
        "conversations": [
            {
                "id": "c",
                "people": ["Jon", "Sam"],
                "turns": [
                    ["Jon", "Atlas, capital of Australia?"],
                    ["Atlas", "Canberra."],
                    ["Jon", "And how many people live there?", "D", "follow_up"],
                    ["Sam", "I asked Atlas that yesterday.", "A:Jon", "about"],
                    ["Sam", "Thanks!", "D~", "thanks"],
                ],
            }
        ],
    }
    rows = [SidechatRecord(**r) for r in suites.convert(suite)]
    assert [r.turn_index for r in rows] == [2, 3, 4]
    assert rows[0].request.history[1].agent and rows[0].label.expect == "respond"
    assert rows[1].label.to == "person" and rows[1].label.to_people == ["Jon"] and rows[1].label.intent == "about"
    assert rows[2].label.expect is None and rows[2].label.respond == 0.5
    assert name_only.decision(rows[1].request) == "respond" and name_only.decision(rows[0].request) == "ignore"


def test_statistics():
    assert score.share(9, 10)["ci95"] == score.wilson(9, 10)
    p = score.paired([True, True, False, False], [True, False, True, True])
    assert p["diff"] == 0.25 and p["only_a"] == 1 and p["only_b"] == 2
    b = score.bootstrap_diff([False] * 40, [True] * 40)
    assert b["diff"] == 1.0 and b["better_beyond_noise"] and not b["worse_beyond_noise"]
    assert score.bootstrap_diff([True] * 10, [False] * 10)["counts"] is False  # under 30 lines
    assert score.auroc([(0.9, True), (0.8, True), (0.2, False), (0.1, False)])["value"] == 1.0
    assert score.auroc([(0.5, True), (0.5, False)])["value"] == 0.5
    assert score.average_precision([(0.9, True), (0.8, False), (0.7, True)])["value"] == pytest.approx(
        (1 + 2 / 3) / 2, abs=1e-4
    )
    assert score.ece([(1.0, 1.0), (0.0, 0.0)])["value"] == 0.0


def test_scorecard_and_report():
    rows = duplex_mpe.convert([_duplex_scenario("explicit"), _duplex_scenario("implicit")])
    # Jev answers the named request, holds on the unnamed one, and answers the "Hey Siri" line by mistake.
    scores = {}
    for r in rows:
        named = "Aria," in r["request"]["text"]
        a = 0.95 if named else (0.9 if "Siri" in r["request"]["text"] else 0.05)
        q = 0.9 if r["tags"]["event"] == "T" else 0.1
        scores[r["row_id"]] = {"addressed": a, "question": q, "ms": 150.0}
    manifest = {"rows_id": "duplex-mpe-0.1", "source": {"repo": "x/y", "revision": "abcdef1234567", "use": "test"}}
    meta = {
        "exp": "exp-test",
        "baseline_id": "b",
        "jev_model": "jev-test",
        "prompt_sha": "p",
        "concurrency": 2,
        "finished_at": "now",
        "usage": {
            "requests": 16,
            "reused": 0,
            "asked": 16,
            "failed": 0,
            "input_tokens": 1,
            "output_tokens": 1,
            "usd_estimate": 0.0,
            "usd_per_m_input": 0.042,
        },
    }
    card = scorecard.build(
        {"duplex-mpe-0.1": {"rows": rows, "scores": scores, "manifest": manifest, "extras": {}}}, meta
    )
    s = card["sets"]["duplex-mpe-0.1"]
    assert s["rows"] == 16 and s["scored"] == 14 and s["label_conflicts_left_out"] == 2
    jev = s["systems"]["jev_demo"]
    assert jev["answered_now"]["k"] == 3 and jev["answered_now"]["n"] == 4  # both N4_Q and the named T
    assert jev["held_instead"]["k"] == 1 and jev["answers_now_wrongly"]["k"] == 2  # "Hey Siri" twice
    assert s["named_vs_unnamed_request"]["n"] == 1 and s["named_vs_unnamed_request"]["diff"] == -1.0
    assert s["slices"]["condition/event"]["implicit/T"]["jev_demo"]["answered_now"]["k"] == 0
    text = scorecard.render(card)
    assert "## duplex-mpe-0.1" in text and "with and without the agent's name" in text
