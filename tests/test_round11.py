"""Round 11: gen-0.6's kinds and settings for a device in a room."""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter

from sidechat import guide
from sidechat.gen import planner, world
from sidechat.gen.rows import conversation_rows
from sidechat.gen.writer import AGENT_BRIEFS, BRIEFS, MUST_CALL, MUST_MENTION, beat_text, check, user_prompt

NEW = ("device_request", "device_feedback", "device_repair", "room_request_physical", "room_talk_after_device")
ADD = {
    "device_request": 20.0,
    "device_feedback": 5.0,
    "device_repair": 4.0,
    "room_request_physical": 4.0,
    "room_talk_after_device": 8.0,
}
ROOM = {"quiet": (0.05, 0.3), "after_quiet": 0.6, "add": ADD, "handoff": 0.3}


def _room_plans(n: int, seed: str, test_only: bool = False) -> list[tuple]:
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        cast = world.make_cast(rng, test_only=test_only, pool=world.ROOM_POOL)
        out.append((cast, planner.plan(rng, cast, **ROOM)))
    return out


def test_new_kinds_have_labels_and_briefs_and_never_call_the_agent():
    for k in ("device_request", "device_feedback", "device_repair"):
        assert guide.KINDS[k].expect == "respond" and guide.KINDS[k].rule == "G6"
    for k in ("room_request_physical", "room_talk_after_device"):
        assert guide.KINDS[k].expect == "ignore" and guide.KINDS[k].rule == "G7"
    for k in NEW:
        assert k in BRIEFS and k in planner.ADDED
        assert k not in MUST_CALL and k not in MUST_MENTION  # the writer check flags any use of the name
    assert "working" in AGENT_BRIEFS
    assert guide.GUIDE_FILE.endswith("0.5.md")


def test_open_requests_keep_their_even_call():
    """SD-32: what a person could also do stays a hold, for a device in a room as anywhere."""
    for k in ("open_request", "open_factual", "open_question", "unclear_you"):
        assert guide.KINDS[k].expect == "wait" and guide.KINDS[k].speak == 3


def test_earlier_corpora_plans_replay_unchanged():
    """Digests of 400 plans per earlier corpus's arguments, taken from the planner at d4d883f."""
    configs = {
        "gen-0.1": ({}, "69ad7d70fbad944c"),
        "gen-0.2": ({"quiet": None}, "e731807b1b26599c"),
        "gen-0.3": ({"quiet": (0.08, 0.25), "after_quiet": 0.6}, "3f8b5c1cf82da7d9"),
        "gen-0.4": ({"quiet": (0.08, 0.25), "add": {"relay_agent_answer": 2.0}, "delayed": 0.15}, "4b907b7c5264709c"),
        "gen-0.5": (
            {
                "boost": {"follow_up_by_other": 1.5, "people_after_agent": 1.3, "follow_up": 1.2},
                "add": {
                    "people_question_after_agent": 7,
                    "partner_to_people_after_agent": 6,
                    "follow_up_later": 12,
                    "relay_agent_answer": 2,
                },
                "delayed": 0.15,
            },
            "f15692c949e5b5b9",
        ),
    }
    for name, (kw, want) in configs.items():
        rng = random.Random(f"replay-{name}")
        h = hashlib.sha256()
        for i in range(400):
            cast = world.make_cast(rng, test_only=i % 9 == 0)
            beats = planner.plan(rng, cast, **kw)
            h.update(
                json.dumps([cast.setting.id, cast.agent, cast.people, planner.describe(beats)], sort_keys=True).encode()
            )
        assert h.hexdigest()[:16] == want, name


def test_new_kinds_stay_out_of_the_earlier_settings():
    rng = random.Random("r11-default-pool")
    for _ in range(300):
        cast = world.make_cast(rng)
        for b in planner.plan(rng, cast, quiet=None, add=ADD):
            if b.kind in planner.DEVICE_KINDS:
                raise AssertionError(f"{b.kind} in {cast.setting.id}")
            if b.kind in planner.ROOM_KINDS:
                assert cast.setting.id in world.ROOM_IDS


def test_held_out_settings_stay_out_of_training_plans_and_the_pool_is_room_settings():
    held = {s.id for s in world.ROOM_DEVICES if s.heldout}
    train = Counter(cast.setting.id for cast, _ in _room_plans(400, "r11-pool"))
    assert set(train) <= world.ROOM_IDS and not held & set(train)
    assert all(s.abilities and s.controls for s in world.ROOM_DEVICES)
    assert not any(s.abilities for s in world.SETTINGS)
    # The settings this repository defines are the ones a public dataset may carry.
    assert {s.id for s in world.SETTINGS} <= world.OWN_IDS and world.ROOM_IDS - world.OWN_IDS <= held


def test_who_says_the_new_kinds_and_when():
    seen, where = Counter(), Counter()
    for cast, beats in _room_plans(800, "r11-on"):
        partner, ago, act = None, None, None
        for i, b in enumerate(beats):
            if b.who == planner.AGENT:
                if b.act == "working":
                    # It reports in its next line, or after one line of the people's own talk.
                    nxt = beats[i + 1]
                    if nxt.who != planner.AGENT:
                        assert nxt.kind == "room_talk_after_device" and len(cast.people) >= 2
                        seen["talk while it works"] += 1
                        nxt = beats[i + 2]
                    assert cast.setting.abilities and nxt.who == planner.AGENT and nxt.act in ("answer", "act")
                    seen["working"] += 1
                partner, ago, act = b.extra.get("partner"), 0, b.act
                continue
            if b.kind in planner.DEVICE_KINDS:
                assert cast.setting.abilities
            if b.kind in ("device_feedback", "device_repair"):
                assert ago == 0 and act in ("answer", "answer_open", "act") and b.who == partner
            if b.kind == "room_talk_after_device":
                assert ago == 0 and act in ("answer", "answer_open", "act", "working")
                assert len(cast.people) >= 2 and b.target and b.target[0] != b.who
            if b.kind == "room_request_physical":
                assert len(cast.people) >= 2 and b.target and b.target[0] != b.who
            if b.kind == "device_request":
                where["none" if ago is None else min(ago, 2)] += 1
            seen[b.kind] += 1
            ago = None if ago is None else ago + 1
    assert all(seen[k] >= 100 for k in NEW), seen
    assert seen["working"] >= 100 and seen["talk while it works"] >= 30
    # Asked before the agent has spoken, straight after it, and after the people's own talk.
    assert where["none"] >= 100 and where[0] >= 100 and where[2] >= 200, where


def test_one_person_alone_says_nothing_that_needs_someone_else():
    solo = [(cast, beats) for cast, beats in _room_plans(1200, "r11-solo") if len(cast.people) == 1]
    assert len(solo) >= 100
    kinds = Counter()
    for cast, beats in solo:
        for b in beats:
            if b.who == planner.AGENT:
                continue
            assert b.who == cast.people[0]
            assert b.kind not in planner.NEEDS_OTHERS and b.kind not in planner.ROOM_KINDS, b.kind
            assert not b.target, (b.kind, b.target)
            kinds[b.kind] += 1
    assert kinds["device_request"] >= 100 and kinds["open_factual"] >= 10  # the second stays a hold


def test_briefs_fill_in_and_checks_flag_breaks():
    rng = random.Random("r11-brief")
    cast = world.make_cast(rng, setting=world.ROOM_DEVICES[0])
    cast.people[:] = ["Ines", "Wes"]
    req = planner.Beat("Ines", kind="device_request")
    assert "bring photos up on the screen" in beat_text(req, cast)
    assert "{" not in user_prompt(cast, planner.plan(rng, cast, **ROOM))
    assert check(req, "Bring up the ones from the wedding.", cast) == []
    assert "calls or names the agent" in check(req, f"{cast.agent}, bring up the ones from the wedding.", cast)
    assert "put to the people" in check(req, "Can someone bring up the ones from the wedding?", cast)
    fix = planner.Beat("Ines", kind="device_repair")
    assert check(fix, "No, the left one.", cast) == []
    assert "not a fragment" in check(fix, "No, I meant the one on the left side of the screen there.", cast)
    said = planner.Beat("Ines", kind="device_feedback")
    assert check(said, "That one's still upside down.", cast) == []
    assert "asks a question" in check(said, "Why is that one upside down?", cast)


def test_rows_carry_where_the_line_falls():
    board = next(s for s in world.ROOM_DEVICES if s.id == "whiteboard")
    cast = world.make_cast(random.Random("r11-rows"), setting=board)
    cast.people[:] = ["Ines", "Wes"]
    beats = [
        planner.Beat("Ines", kind="device_request"),
        planner.Beat(planner.AGENT, act="working", extra={"partner": "Ines"}),
        planner.Beat(planner.AGENT, act="act", extra={"partner": "Ines", "control": "the diagram on the board"}),
        planner.Beat("Wes", kind="room_talk_after_device", target=["Ines"]),
        planner.Beat("Ines", kind="reply_to_person", target=["Wes"]),
        planner.Beat("Ines", kind="device_request"),
    ]
    texts = [
        "Draw a ring of dots.",
        "On it.",
        "There's a ring of twelve dots.",
        "Is the oven off?",
        "Yes.",
        "Now a star.",
    ]
    rows = conversation_rows("gen-x", "a01-00001", cast, beats, texts, [[] for _ in beats], "a", heldout_writer=False)
    assert [r["tags"]["kind"] for r in rows] == [
        "device_request",
        "room_talk_after_device",
        "reply_to_person",
        "device_request",
    ]
    assert [r["tags"]["since_agent"] for r in rows] == ["none", "0", "1", "2"]
    assert all(r["tags"]["setting"] == "whiteboard" and r["tags"]["people_n"] == "2" for r in rows)
    assert len({r["tags"]["split"] for r in rows}) == 1  # a conversation is in one split
    assert [r["label"]["expect"] for r in rows] == ["respond", "ignore", "ignore", "respond"]
    assert rows[1]["label"]["to_people"] == ["Ines"]
    # Two agent turns in a row reach the history as they were said.
    assert [t["agent"] for t in rows[1]["request"]["history"]] == [False, True, True]
