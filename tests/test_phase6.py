"""Phase 6: lining up speech-to-text words with AMI's dialogue acts, and the gold-against-heard comparison."""

from __future__ import annotations

from sidechat.lib.stt_align import assign_words, match_speakers, wer


def _das() -> list[dict]:
    return [
        {"da_id": "m.1", "speaker": "A", "start_time": 0.0, "end_time": 2.0, "text": "shall we start"},
        {"da_id": "m.2", "speaker": "B", "start_time": 2.1, "end_time": 3.0, "text": "yeah"},
        {"da_id": "m.3", "speaker": "A", "start_time": 3.2, "end_time": 5.0, "text": "okay the budget"},
    ]


def test_speakers_match_by_overlap():
    segs = [
        {"speaker_id": "MEE1", "begin": 0.0, "end": 2.1},
        {"speaker_id": "MEE2", "begin": 2.0, "end": 3.1},
        {"speaker_id": "MEE1", "begin": 3.1, "end": 5.2},
    ]
    assert match_speakers(_das(), segs) == {"A": "MEE1", "B": "MEE2"}


def test_words_go_to_the_act_holding_their_midpoint():
    words = {
        "MEE1": [
            (0.1, 0.4, "Shall"),
            (0.5, 0.8, "we"),
            (0.9, 1.4, "start?"),
            (3.3, 3.8, "Okay,"),
            (3.9, 4.6, "the budget."),
        ],
        "MEE2": [(2.2, 2.6, "Yeah."), (2.9, 3.4, "bleed")],  # midpoint 3.15 falls in no act of B's
    }
    got = assign_words(_das(), words, {"A": "MEE1", "B": "MEE2"})
    assert got == {"m.1": "Shall we start?", "m.2": "Yeah.", "m.3": "Okay, the budget."}
    assert assign_words(_das(), words, {"A": "MEE1"})["m.2"] == ""  # an unmatched speaker hears nothing


def test_wer_ignores_case_and_punctuation():
    assert wer("shall we start", "Shall we start?") == (0, 3)
    assert wer("okay the budget", "okay budget") == (1, 3)
    assert wer("", "uh") == (1, 0)


def _ami() -> list[dict]:
    rows = []
    for m in ("TS3009a", "TS3009b"):
        for i in range(20):
            rows.append(
                {
                    "meeting": m,
                    "speaker": "ABCD"[i % 4],
                    "start": float(i),
                    "end": i + 0.9,
                    "labelled_meeting": False,
                    "gold": f"gold {m} {i}",
                    "stt": "" if i == 5 else f"heard {m} {i}",
                }
            )
    rows.append(
        {
            "meeting": "ES2008a",
            "speaker": "A",
            "start": 0.0,
            "end": 1.0,
            "labelled_meeting": True,
            "gold": "x",
            "stt": "x",
        }
    )
    return rows


def test_slurp_splices_match_between_written_and_heard():
    from sidechat.sources import slurp

    reqs = [
        {
            "slurp_id": "1",
            "sentence": "olly wake me up at seven",
            "stt": "Olly, wake me up at seven.",
            "scenario": "alarm",
            "intent": "alarm_set",
        },
        {
            "slurp_id": "2",
            "sentence": "what's the weather tomorrow",
            "stt": "What's the weather tomorrow?",
            "scenario": "weather",
            "intent": "weather_query",
        },
        {
            "slurp_id": "3",
            "sentence": "turn the lights off",
            "stt": "",
            "scenario": "iot",
            "intent": "iot_hue_lightoff",
        },
    ]
    written = {r["row_id"].split("/")[1]: r for r in slurp.convert(reqs, _ami(), heard=False)}
    heard = {r["row_id"].split("/")[1]: r for r in slurp.convert(reqs, _ami(), heard=True)}
    assert set(written) == {"1", "2", "3"} and set(heard) == {"1", "2"}  # heard as nothing: left out
    for i, h in heard.items():
        w = written[i]
        assert w["tags"]["meeting"] == h["tags"]["meeting"] != "ES2008a"  # never a labelled meeting
        assert w["request"]["speaker"] == h["request"]["speaker"]
        assert len(w["request"]["history"]) == 8 and all(t["text"].startswith("gold") for t in w["request"]["history"])
        assert all(t["text"].startswith("heard") for t in h["request"]["history"])
        assert w["request"]["agent"]["name"] == "Olly"
    assert written["1"]["label"]["expect"] == "respond" and written["1"]["tags"]["named"] == "1"
    assert written["2"]["label"]["expect"] == "wait" and written["2"]["label"]["respond"] == 0.5
