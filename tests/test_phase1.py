"""Phase 1: the guide as code, the committee prompt, answer parsing, the vote and agreement. No network."""

from __future__ import annotations

import json
import pathlib
import re

import pytest

from sidechat import guide
from sidechat.committee import agreement, members, prompt
from sidechat.committee.vote import committee_label, vote
from sidechat.schema import Agent, SidechatRecord, SidechatRequest, Turn
from sidechat.sources import suites

ROOT = pathlib.Path(__file__).resolve().parents[1]


def test_every_guide_suite_kind_is_defined():
    for which in ("pilot-0.2", "pilot-0.3", "pilot-0.4"):
        for r in suites.convert(suites.load(which)):
            assert r["tags"]["kind"] in guide.KINDS
            assert r["label"]["source"] == "guide"


def test_kind_rules_are_consistent():
    for kind, k in guide.KINDS.items():
        assert k.rule in guide.RULES, kind
        assert 1 <= k.speak <= 5, kind
        if k.expect == "respond":
            assert k.speak >= 4, kind
        if k.expect == "ignore":
            assert k.speak <= 2, kind
        if k.expect is None or k.expect == "wait":
            assert k.speak == 3, kind
        if k.to == "agent":
            assert k.intent in ("direct", "indirect"), kind


def test_guide_prose_names_every_rule_and_field():
    text = (ROOT / guide.GUIDE_FILE).read_text()
    for rule in guide.RULES:
        assert f"### {rule}." in text
    for field in ("`to`", "`people`", "`intent`", "`decision`", "`speak`"):
        assert field in text


def _norm(text: str) -> str:
    return " ".join(re.sub(r"[^\w\s]", " ", text.lower()).split())


def test_guide_quotes_no_test_line():
    """Nothing the committee reads may copy a test line, word for word or nearly."""
    text = re.sub(r"\s+", " ", (ROOT / guide.GUIDE_FILE).read_text())
    quoted = {_norm(q) for q in re.findall(r'"([^"]+)"', text)}
    quoted = {q for q in quoted if len(q.split()) >= 3}
    lines = {_norm(r["request"]["text"]) for w in ("pilot", "demo") for r in suites.convert(suites.load(w))}
    leaks = {
        (q, line)
        for q in quoted
        for line in lines
        if q == line or (min(len(q), len(line)) >= 15 and (q in line or line in q))
    }
    assert not leaks, sorted(leaks)


def test_label_for_people_and_unclear():
    lab = guide.label_for("reply_to_person", ["Sam"])
    assert lab.to == "person" and lab.to_people == ["Sam"] and lab.expect == "ignore" and lab.respond == 0.0
    lab = guide.label_for("unclear_after_agent")
    assert lab.to == "unknown" and lab.unclear and lab.expect == "wait" and lab.respond == 0.5 and lab.intent is None
    lab = guide.label_for("role_request")
    assert lab.to == "agent" and lab.intent == "indirect" and lab.respond == 0.75
    with pytest.raises(KeyError):
        guide.label_for("no_such_kind")


def test_pilot_02_keeps_pilot_01_lines():
    a, b = suites.convert(suites.load("pilot")), suites.convert(suites.load("pilot-0.2"))
    assert [r["request"] for r in a] == [r["request"] for r in b]


def test_user_message_shows_conversation_not_label():
    req = SidechatRequest(
        agent=Agent(name="Atlas", aliases=["at last"], role="AI assistant on the call"),
        text="And how many live there?",
        speaker="Jon",
        people=["Jon", "Sam"],
        history=[
            Turn(speaker="Jon", text="Atlas, capital of Australia?"),
            Turn(speaker="Atlas", text="Canberra.", agent=True),
        ],
    )
    msg = prompt.user_message(req)
    assert "Other names it answers to: at last." in msg and "People present: Jon, Sam." in msg
    assert '2. Atlas (the agent): "Canberra."' in msg
    assert msg.endswith('Line to label, said by Jon:\n"And how many live there?"')
    assert "follow_up" not in msg and "G6" not in msg
    assert (
        prompt.system_prompt().startswith(f"# Sidechat labelling guide {guide.GUIDE_VERSION.rsplit('-', 1)[-1]}")
        and "## How to answer" in prompt.system_prompt()
    )


def test_parse_answer():
    good = {
        "to": "person",
        "people": ["Sam"],
        "intent": "other",
        "decision": "ignore",
        "speak": 1,
        "rule": "G3",
        "reason": "x",
    }
    assert prompt.parse_answer("```json\n" + json.dumps(good) + "\n```")["people"] == ["Sam"]
    assert prompt.parse_answer(json.dumps({**good, "to": "group"}))["people"] == []
    for bad in ({**good, "decision": "maybe"}, {**good, "speak": 7}, {**good, "to": "bot"}):
        with pytest.raises(ValueError):
            prompt.parse_answer(json.dumps(bad))
    with pytest.raises(ValueError):
        prompt.parse_answer("no json here")


def test_schema_is_strict_compatible():
    s = prompt.SCHEMA
    assert s["additionalProperties"] is False and set(s["required"]) == set(s["properties"])
    assert "additionalProperties" not in members._gemini_schema(s)


def _a(decision, intent="direct", speak=5, to="agent", people=(), rule="G2"):
    return {
        "to": to,
        "people": list(people),
        "intent": intent,
        "decision": decision,
        "speak": speak,
        "rule": rule,
        "reason": "",
    }


def test_vote_majority_and_label():
    v = vote({"a": _a("respond"), "b": _a("respond", speak=4), "c": _a("wait", "open", 3, "group")})
    assert v["decision"] == "respond" and v["intent"] == "direct" and v["speak"] == 4.0 and not v["unanimous"]
    lab = committee_label(v)
    assert lab.expect == "respond" and lab.respond == 0.75 and lab.to == "agent"
    v = vote({"a": _a("respond"), "b": _a("wait", "open"), "c": _a("ignore", "other")})
    assert v["decision"] is None and committee_label(v).expect is None
    v = vote(
        {"a": _a("ignore", "other", 1, "person", ["Sam"]), "b": _a("ignore", "other", 1, "person", ["Sam"]), "c": None}
    )
    assert v["n"] == 2 and v["people"] == ["Sam"] and committee_label(v).to_people == ["Sam"]
    assert committee_label(vote({"a": _a("respond"), "b": None, "c": None})) is None


def test_cost_estimate():
    u = {"input": 1_000_000, "cached": 600_000, "cache_write": 0, "output": 100_000}
    assert members.cost_usd("b", u, (4.0, 20.0)) == pytest.approx(0.4 * 4 + 0.6 * 0.4 + 0.1 * 20)
    assert members.cost_usd("a", u, None) == 0.0


def test_agreement_card():
    rows = suites.convert(suites.load("pilot-0.2"))[:12]
    answers = {m: {} for m in ("a", "b", "c")}
    for n, r in enumerate(rows):
        lab = r["label"]
        right = lab["expect"] or "wait"
        to = "unclear" if lab["unclear"] else lab["to"]
        intent = lab["intent"] or "other"
        answers["a"][r["row_id"]] = _a(right, intent, 3, to)
        answers["b"][r["row_id"]] = _a(right if n % 4 else "respond", intent, 3, to)
        answers["c"][r["row_id"]] = None if n == 0 else _a(right, intent, 3, to)
    votes = {i: vote({m: answers[m][i] for m in answers}) for i in answers["a"]}
    meta = {
        "exp": "t",
        "label_id": "t",
        "sets": ["pilot-0.2"],
        "guide": guide.GUIDE_VERSION,
        "prompt_sha": "x",
        "members": ["a", "b", "c"],
        "finished_at": "now",
        "usage": {m: {"answered": 12, "failed": 0, "input": 1, "cached": 0, "output": 1, "usd": 0.0} for m in "abc"},
    }
    card = agreement.build(rows, answers, votes, meta)
    definite = [r for r in rows if r["label"]["expect"]]
    assert card["definite"] == len(definite) and card["majority"]["decision"]["n"] == len(definite)
    assert card["members"]["a"]["decision"]["value"] == 1.0
    assert card["members"]["c"]["answered"]["k"] == 11
    text = agreement.render(card)
    assert "## Agreement with the guide" in text and "Member b" in text
    SidechatRecord(**rows[0])  # rows stay valid records


def test_rhythm_roles_and_numbers():
    from sidechat import context
    from sidechat.schema import Facts

    req = SidechatRequest(
        agent=Agent(name="Atlas"),
        text="And by train?",
        speaker="Dev",
        people=["Dev", "Lucy"],
        history=[
            Turn(speaker="Lucy", text="Morning."),
            Turn(speaker="Dev", text="Atlas, how far is Leeds from York?"),
            Turn(speaker="Atlas", text="About twenty-five miles. Driving?", agent=True),
        ],
        facts=Facts(over_agent=False),
    )
    assert context.roles(req) == ["other", "speaker", "agent"]
    assert context.roles(req, slots=True) == ["other1", "speaker", "agent"]
    r = context.rhythm(req)
    assert r.turns_since_agent == 0 and r.agent_last_asked and r.speaker_was_agent_partner and not r.speaker_spoke_last
    assert r.others == 1 and r.speaker_turns == 1 and r.agent_turns == 1
    lucy = req.model_copy(update={"speaker": "Lucy"})
    assert context.rhythm(lucy).speaker_was_agent_partner is False
    text = context.render(req)
    assert text.splitlines() == [
        "[other1] Morning.",
        "[speaker] Atlas, how far is Leeds from York?",
        "[agent] About twenty-five miles. Driving?",
        ">> [speaker] And by train?",
    ]
    blind = req.model_copy(update={"speaker": None})
    assert (
        context.roles(blind) == ["unknown", "unknown", "agent"]
        and context.rhythm(blind).speaker_was_agent_partner is None
    )


def test_rhythm_separates_the_pilot_follow_ups():
    """The pilot's follow-ups by the agent's partner and by someone else differ in the rhythm."""
    from sidechat import context

    rows = {
        r["tags"]["kind"]: r
        for r in suites.convert(suites.load("pilot-0.3"))
        if r["tags"]["kind"] in ("follow_up", "follow_up_by_other")
    }
    by_other = context.rhythm(SidechatRequest(**rows["follow_up_by_other"]["request"]))
    own = context.rhythm(SidechatRequest(**rows["follow_up"]["request"]))
    assert by_other.speaker_was_agent_partner is False and own.speaker_was_agent_partner is True


def test_conditions():
    from sidechat import conditions

    rows = suites.convert(suites.load("pilot-0.4"))
    r = next(x for x in rows if x["tags"]["kind"] == "question_to_named_person" and len(x["request"]["history"]) >= 2)
    anon = conditions.apply(r, "anonymous")
    assert anon["set"] == "pilot-0.4@anonymous" and anon["row_id"].startswith("pilot-0.4@anonymous/")
    speakers = [t["speaker"] for t in anon["request"]["history"] if not t["agent"]] + [anon["request"]["speaker"]]
    assert all(s.startswith("Speaker ") for s in speakers) and anon["request"]["people"] is None
    assert anon["request"]["text"] == r["request"]["text"] and anon["label"]["to_people"] == []
    assert all(t["speaker"] == r["request"]["agent"]["name"] for t in anon["request"]["history"] if t["agent"])
    none = conditions.apply(r, "none")
    assert none["request"]["speaker"] is None and all(
        t["speaker"] is None for t in none["request"]["history"] if not t["agent"]
    )
    SidechatRecord(**anon), SidechatRecord(**none)
    from sidechat import context

    assert context.roles(SidechatRequest(**anon["request"])) == context.roles(SidechatRequest(**r["request"]))
