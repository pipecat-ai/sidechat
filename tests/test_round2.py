"""Round 2: guide 0.4, the planner's new kinds and quiet stretches, AMI's unlabelled meetings, and
the real-speech bar on thresholds."""

from __future__ import annotations

import random

from sidechat import guide
from sidechat.gen import planner, world
from sidechat.gen.writer import BRIEFS, user_prompt
from sidechat.sources import ami
from sidechat.train import evaluate as E


def test_named_closings_are_answered():
    for kind in ("thanks_named", "stop_named", "farewell_named"):
        label = guide.label_for(kind)
        assert label.expect == "respond" and label.respond == 0.75


def test_new_kinds_have_labels_and_briefs():
    for kind in ("answer_after_aside", "imperative_to_person", "steps_to_people", "host_to_group"):
        assert kind in guide.KINDS and kind in BRIEFS
    assert guide.label_for("answer_after_aside").expect == "respond"
    for kind in ("imperative_to_person", "steps_to_people", "host_to_group"):
        assert guide.label_for(kind).expect == "ignore"


def _plans(n: int, quiet):
    for i in range(n):
        rng = random.Random(i)
        cast = world.make_cast(rng)
        yield cast, planner.plan(rng, cast, quiet=quiet)


def test_quiet_plans():
    quiet_whole = quiet_start = 0
    for cast, beats in _plans(600, (0.08, 0.25)):
        assert all(b.kind in guide.KINDS for b in beats if b.who != planner.AGENT)
        user_prompt(cast, beats)  # every beat renders
        people = [b for b in beats if b.who != planner.AGENT]
        if all(b.kind in planner.QUIET_KINDS for b in people) and not any(b.who == planner.AGENT for b in beats):
            quiet_whole += 1
        elif beats[0].who != planner.AGENT and all(b.kind in planner.QUIET_KINDS for b in beats[:3]):
            quiet_start += 1
    assert 20 <= quiet_whole <= 120
    assert quiet_start >= 100


def test_default_plans_have_no_quiet_stretch_draw():
    a = [b.kind for _, beats in _plans(50, (0.0, 0.0)) for b in beats]
    b = [b.kind for _, beats in _plans(50, (0.0, 0.0)) for b in beats]
    assert a == b


def test_answer_after_aside_follows_a_check_with_a_person():
    seen = 0
    for _, beats in _plans(1500, (0.08, 0.25)):
        for i, b in enumerate(beats):
            if b.kind == "answer_after_aside":
                seen += 1
                ask, check, reply = beats[i - 3], beats[i - 2], beats[i - 1]
                assert ask.who == planner.AGENT and ask.act == "ask"
                assert check.kind == "question_to_named_person" and check.who == b.who
                assert reply.kind == "reply_to_person" and reply.target == [b.who]
    assert seen >= 20


def test_ami_silent_split_keeps_labelled_series_out():
    recs = [
        {"meeting_id": "ES2002a", "labeled": True, "addressee_raw": "A", "da_type": "sug"},
        {"meeting_id": "ES2003a", "labeled": False, "da_type": "sug"},
    ]
    base = {"speaker": "A", "da_id": "x", "start_time": 0.0, "end_time": 1.0, "n_words": 3, "text": "next one please"}
    recs = [{**base, **r, "da_id": f"d{i}"} for i, r in enumerate(recs)]
    rows = ami.convert_silent(recs, ["Juno"])
    assert all(r["conv_id"] != "ES2002a" for r in rows)
    assert all(r["label"]["expect"] == "ignore" for r in rows)
    assert {ami.silent_split(s) for s in ("ES2003", "TS3010", "IS1002")} <= {"train", "dev", "test"}


def test_thresholds_respect_the_real_speech_bar():
    rows, preds = [], {}
    for i in range(200):
        e = "respond" if i < 100 else "ignore"
        rows.append({"row_id": f"g{i}", "label": {"expect": e}})
        preds[f"g{i}"] = {"respond": 0.95 if e == "respond" else 0.05, "intent": {"open": 0.0}}
    real = []
    for i in range(100):
        real.append({"row_id": f"r{i}", "label": {"expect": "ignore"}})
        preds[f"r{i}"] = {"respond": 0.7 if i < 5 else 0.01, "intent": {"open": 0.0}}
    t = E.choose_thresholds(preds, rows, real_rows=real, max_wrong_now_real=0.01)
    assert t["respond"] > 0.7 and t["real_wrong_now"] == 0
    loose = E.choose_thresholds(preds, rows)
    assert "real_wrong_now" not in loose
