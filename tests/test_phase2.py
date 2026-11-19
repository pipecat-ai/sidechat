"""Phase 2: the planner, the writer prompt and checks, and the rows. No network."""

from __future__ import annotations

import random

from sidechat import guide
from sidechat.gen import planner, rows, world, writer
from sidechat.gen.planner import AGENT, Beat
from sidechat.schema import SidechatRecord


def _plans(n=300, seed=11):
    rng = random.Random(seed)
    for i in range(n):
        cast = world.make_cast(rng, test_only=i % 7 == 0)
        yield cast, planner.plan(rng, cast)


def test_rhythm_rules_hold():
    for cast, beats in _plans():
        partner, agent_last, asked = None, False, False
        for b in beats:
            if b.who == AGENT:
                partner, agent_last, asked = b.extra.get("partner"), True, b.act == "ask"
                continue
            assert b.kind in guide.KINDS
            if b.kind in ("follow_up", "correction", "command_no_name"):
                assert agent_last and b.who == partner
            if b.kind == "follow_up_by_other":
                assert agent_last and b.who != partner
            if b.kind == "answer_to_agent_question":
                assert agent_last and asked
            if b.kind in ("action_to_game_master", "question_only_agent_can_answer"):
                assert cast.setting.leads
            if b.target:
                assert b.target[0] != b.who and b.target[0] in cast.people
            agent_last = False


def test_heldout_only_in_test_casts():
    rng = random.Random(5)
    for _ in range(400):
        cast = world.make_cast(rng, test_only=False)
        assert not cast.heldout and not cast.setting.heldout and cast.agent not in world.HELDOUT_AGENTS


def test_prompt_and_checks():
    rng = random.Random(2)
    cast = world.make_cast(rng)
    cast.unnamed = False
    cast.agent, cast.aliases = "Nova", ("no va",)
    prompt = writer.user_prompt(
        cast, [Beat(cast.people[0], kind="name_first"), Beat(AGENT, act="answer", extra={"partner": cast.people[0]})]
    )
    assert "1. " in prompt and "2. Nova: Nova answers" in prompt
    b = Beat("Sam", kind="name_first")
    assert writer.check(b, "Nova, what's on today?", cast) == []
    assert "does not call the agent" in writer.check(b, "What's on today?", cast)
    f = Beat("Sam", kind="follow_up")
    assert "calls or names the agent" in writer.check(f, "And Nova, what about tomorrow?", cast)
    assert writer.check(f, "And tomorrow?", cast) == []
    q = Beat("Sam", kind="question_to_named_person", target=["Lucy"])
    assert writer.check(q, "Lucy, are you coming?", cast) == []
    assert "does not name Lucy" in writer.check(q, "Are you coming?", cast)
    d = Beat("Sam", kind="other_device", extra={"device": "Alexa"})
    assert writer.check(d, "Alexa, lights off.", cast) == [] and writer.check(d, "Lights off.", cast)
    cast.agent = "Max"
    w = Beat("Sam", kind="statement")
    assert writer.check(w, "That's two cups max.", cast) == []  # a word-like name in lower case is a word


def test_parse_lines():
    assert writer.parse_lines('{"lines": [{"beat": 1, "text": "Hi."}, {"beat": 2, "text": "Sam: Hello"}]}', 2) == [
        "Hi.",
        "Hello",
    ]
    try:
        writer.parse_lines('{"lines": [{"beat": 1, "text": "Hi."}]}', 2)
        raise AssertionError
    except ValueError:
        pass


def test_rows_from_a_conversation():
    rng = random.Random(9)
    cast = world.make_cast(rng)
    beats = planner.plan(rng, cast)
    texts = [f"line {i}" for i in range(len(beats))]
    out = rows.conversation_rows(
        "gen-t", "a01-00001", cast, beats, texts, [[] for _ in beats], "a", heldout_writer=False
    )
    human = [b for b in beats if b.who != AGENT]
    assert len(out) == len(human)
    for r, b in zip(out, human):
        rec = SidechatRecord(**r)
        assert rec.tags["kind"] == b.kind and rec.label.expect == guide.KINDS[b.kind].expect
        assert all(t.agent == (t.speaker == rec.request.agent.name) for t in rec.request.history)
    test_rows = rows.conversation_rows(
        "gen-t", "b01-00001", cast, beats, texts, [[] for _ in beats], "b", heldout_writer=True
    )
    assert {r["tags"]["split"] for r in test_rows} == {"test"}


def test_no_person_exchange_right_after_the_agent():
    for cast, beats in _plans(400, seed=21):
        prev = None
        for b in beats:
            if b.who != AGENT and prev is not None and prev.who == AGENT and prev.act == "ask":
                assert b.kind in planner.AFTER_ASK | planner.FORCED_ONLY | {"reply_to_person"} or b.over_agent, b.kind
            prev = b


def test_label_safe():
    assert rows.label_safe("about_judged", ["does not mention the agent"])
    assert rows.label_safe("question_to_named_person", ["does not name Lucy"])
    assert not rows.label_safe("follow_up", ["calls or names the agent"])
    assert not rows.label_safe("name_first", ["does not call the agent"])
