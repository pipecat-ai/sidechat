"""Round 6: gen-0.4's planner options, and the shorter input for small, fast models."""

from __future__ import annotations

import random
from collections import Counter

from sidechat import guide
from sidechat.gen import planner, world
from sidechat.gen.writer import BRIEFS, MUST_MENTION

ADD = {"relay_agent_answer": 2.5}


def _plans(n: int, seed: str, **kw) -> list[list]:
    rng = random.Random(seed)
    return [planner.plan(rng, world.make_cast(rng), **kw) for _ in range(n)]


def test_round6_kinds_have_labels_and_briefs():
    assert guide.KINDS["follow_up_after_reaction"].expect == "respond"
    assert guide.KINDS["relay_agent_answer"].expect == "ignore"
    assert {"follow_up_after_reaction", "relay_agent_answer"} <= set(BRIEFS)
    assert "relay_agent_answer" in MUST_MENTION


def test_options_off_replay_earlier_plans():
    a = _plans(200, "r6", quiet=(0.0, 0.0))
    b = _plans(200, "r6", quiet=(0.0, 0.0), add=None, delayed=0.0)
    assert [planner.describe(x) for x in a] == [planner.describe(x) for x in b]
    kinds = Counter(beat.kind for p in a for beat in p)
    assert kinds["relay_agent_answer"] == 0 and kinds["follow_up_after_reaction"] == 0


def test_delayed_follow_up_comes_from_the_person_answered_after_a_reaction():
    seen = 0
    for p in _plans(400, "r6-delayed", delayed=0.5, add=ADD):
        for i, b in enumerate(p):
            if b.kind != "follow_up_after_reaction":
                continue
            seen += 1
            reaction, agent = p[i - 1], p[i - 2]
            assert reaction.kind in ("people_after_agent", "backchannel")
            assert agent.who == planner.AGENT and agent.act in ("answer", "act")
            assert b.who == agent.extra["partner"] != reaction.who
    assert seen >= 100


def test_relay_follows_the_agent_and_names_another_person():
    seen = 0
    for p in _plans(400, "r6-relay", delayed=0.3, add=ADD):
        for i, b in enumerate(p):
            if b.kind != "relay_agent_answer":
                continue
            seen += 1
            assert p[i - 1].who == planner.AGENT and p[i - 1].act in ("answer", "answer_open", "act")
            assert b.target and b.target[0] != b.who
    assert seen >= 50


# --- the short input and the two towers ---------------------------------------------------------

from sidechat.schema import Agent, SidechatRequest, Turn
from sidechat.train import features


def _req(n: int = 8, speaker: str = "Sam") -> SidechatRequest:
    people = ["Jon", "Sam", "Ana"]
    history = []
    for i in range(n):
        if i % 3 == 2:
            history.append(Turn(speaker="Atlas", text=f"Agent turn {i}.", agent=True))
        else:
            history.append(Turn(speaker=people[i % 2], text=f"Person turn {i} with a few more words in it."))
    return SidechatRequest(agent=Agent(name="Atlas"), text="And what about Tuesday?", speaker=speaker, history=history)


def _words(t: str) -> int:
    return len(t.split())


def test_fitted_keeps_the_line_and_the_newest_turns():
    req = _req()
    full, _ = features.text(req)
    t, start = features.fitted(req, 4, 10_000, _words)
    assert t.endswith("And what about Tuesday?") and t[start:].startswith(features.LINE_MARK)
    assert "Agent turn 5." in t and "Person turn 3" not in t  # the last 4 turns are 4 to 7
    tight, _ = features.fitted(req, 8, _words(features.text(req, 2)[0]), _words)
    assert tight == features.text(req, 2)[0]  # oldest turns dropped until it fits
    assert features.text(req, 0)[0] == full


def test_two_tower_history_does_not_depend_on_the_next_speaker():
    a, b = _req(speaker="Sam"), _req(speaker="Ana")
    assert features.context_text(a) == features.context_text(b)
    assert "[p1] Person turn 0" in features.context_text(a) and "[agent] Agent turn 2." in features.context_text(a)
    assert features.line_text(a).endswith(">> [p2] And what about Tuesday?")
    assert features.line_text(b).endswith(">> [new] And what about Tuesday?")
    assert features.line_text(a).startswith("agent: Atlas")
    empty = SidechatRequest(agent=Agent(name="Atlas"), text="Hi", speaker="Jon")
    assert features.context_text(empty).endswith("(start of the conversation)")


def test_context_fitted_drops_oldest_turns():
    req = _req()
    limit = _words(features.context_text(req, 3))
    assert features.context_fitted(req, limit, _words) == features.context_text(req, 3)
