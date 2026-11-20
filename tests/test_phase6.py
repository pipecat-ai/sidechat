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


def test_real_requests_are_formatted_and_kept_off_the_test_split():
    from sidechat.sources import realreq

    assert realreq.formatted("what's the weather like in london") == "What's the weather like in london?"
    assert realreq.formatted("i'm hungry order me a pizza") == "I'm hungry order me a pizza."
    assert (
        realreq.after_name("How far is it?") == "how far is it?"
        and realreq.after_name("I need a cab.") == "I need a cab."
    )
    slurp = {
        "train": [{"slurp_id": 1, "sentence": "olly set an alarm"}, {"slurp_id": 2, "sentence": "play some jazz"}],
        "devel": [{"slurp_id": 3, "sentence": "what time is it"}],
    }
    clinc = {"train": [["tell me a joke", "tell_joke"]], "val": [["how do i say hi in french", "translate"]]}
    got = realreq.requests(slurp, clinc, [{"sentence": "Play some jazz!"}])
    assert {r["id"] for r in got} == {"slurp-1", "slurp-3", "clinc-train-0", "clinc-val-0"}  # the test request is out
    assert {r["split"] for r in got if r["source"] == "slurp"} == {"train", "dev"}


def test_hold_bar_on_real_lines_moves_the_thresholds():
    from sidechat.train.evaluate import choose_thresholds

    def p(respond: float, open_: float = 0.0) -> dict:
        return {
            "respond": respond,
            "intent": {"direct": 0, "indirect": 0, "open": open_, "about": 0, "other": 1 - open_},
        }

    rows, preds = [], {}
    for i in range(40):  # held right at 0.42 (wait), quiet at 0.1, answered at 0.95
        for exp_, pr in (("wait", p(0.42)), ("ignore", p(0.1)), ("respond", p(0.95))):
            rid = f"g/{exp_}{i}"
            rows.append({"row_id": rid, "label": {"expect": exp_}})
            preds[rid] = pr
    real = []
    for i in range(100):  # real people's lines, 5 of them near the hold threshold
        rid = f"real/{i}"
        real.append({"row_id": rid, "label": {"expect": "ignore"}})
        preds[rid] = p(0.41 if i < 5 else 0.05)
    loose = choose_thresholds(preds, rows, real_rows=real)
    tight = choose_thresholds(preds, rows, real_rows=real, max_held_real=0.02)
    assert loose["real_held"] == 5 and tight["real_held"] <= 2
