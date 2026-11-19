"""Plan a conversation as beats: who speaks, what kind of line, and who it is for.

The planner tracks the rhythm of the conversation as it goes: whom the agent last answered, whether
it asked something, whether it was cut off, what it controls. Each kind of line has preconditions
on that state, so a `follow_up` is only ever said by the person the agent just answered and a
`follow_up_by_other` only by someone else. The label of every line then comes from its kind
(`sidechat/guide.py`), right by construction. The writer model only puts words to the plan.
"""

from __future__ import annotations

import random
from dataclasses import asdict, dataclass, field

from sidechat.gen.world import DEVICES, WORDLIKE, Cast

AGENT = "@agent"


@dataclass
class Beat:
    who: str  # a person's name, or AGENT
    kind: str | None = None  # the guide kind, for a person's line
    act: str | None = None  # for the agent's line: answer, answer_open, ask, yes, ack, act, interrupted
    target: list[str] = field(default_factory=list)  # people the line is for or names
    over_agent: bool = False  # said while the agent was speaking
    extra: dict = field(default_factory=dict)  # device, control, partner, ...


@dataclass
class State:
    agent_act: str | None = None  # the agent's latest act
    agent_ago: int = 99  # people's lines since the agent's latest line; 0: it spoke last
    partner: str | None = None  # the person the agent's latest line answered or asked
    asked_room: bool = False  # the agent's latest question was to everyone
    control: str | None = None  # what the agent last set or played
    control_ago: int = 99
    interrupted: bool = False  # the agent's latest line was cut off
    last: Beat | None = None  # the previous person's line
    exchange: tuple[str, str] | None = None  # two people talking to each other
    lines: int = 0  # people's lines so far
    ask_pending: bool = False  # the agent asked something and nobody has answered it yet
    quiet_left: int = 0  # people's lines still to come before anyone may involve the agent


# kind -> base weight. Preconditions are in `_allowed`.
WEIGHTS: dict[str, float] = {
    "other_device": 1.0,
    "name_first": 6,
    "name_mid": 2.5,
    "name_last": 2.5,
    "name_alone": 1.0,
    "name_misheard": 1.2,
    "wake_phrase": 1.5,
    "role_address": 1.2,
    "named_after_aside": 2.5,
    "thanks_named": 1.2,
    "stop_named": 0.8,
    "farewell_named": 0.4,
    "never_mind": 0.8,
    "name_slip_corrected": 0.5,
    "question_to_named_person": 5,
    "statement_to_named_person": 2.5,
    "to_named_person_after_agent": 3,
    "similar_name_person": 2,
    "about_to_named_person": 1.5,
    "role_request": 2.5,
    "relayed_invite": 1.0,
    "invite": 2.0,
    "indirect_wish": 0.8,
    "about_question": 1.0,
    "about_hypothetical": 1.5,
    "about_judged": 1.5,
    "about_pronoun": 1.0,
    "about_quoted": 0.6,
    "about_reported": 1.5,
    "about_stated": 0.5,
    "about_question_to_group": 0.8,
    "name_word_sense": 1.5,
    "alias_false_match": 0.8,
    "answer_to_agent_question": 8,
    "follow_up": 7,
    "correction": 1.5,
    "command_no_name": 1.5,
    "reply_then_request": 1.5,
    "thanks": 1.2,
    "action_to_game_master": 4,
    "opener_to_agent": 0,
    "question_only_agent_can_answer": 2,
    "addressed_by_exclusion": 1.2,
    "only_agent_can_do": 3,
    "you_to_person_after_agent": 3,
    "unclear_after_agent": 3,
    "follow_up_by_other": 3.5,
    "open_question": 3,
    "open_factual": 3,
    "open_request": 1.5,
    "unclear_you": 2.5,
    "group_question_not_for_agent": 3,
    "remark_to_group": 1.5,
    "request_to_people": 1.5,
    "proposal_to_group": 1.5,
    "table_talk": 2.0,
    "you_to_person": 2,
    "unclear_you_person_task": 1.2,
    "statement": 4,
    "people_after_agent": 3,
    "reply_to_person": 3,
    "continuing_with_person": 2,
    "backchannel": 1.5,
    "thinking_aloud": 1.5,
    "off_call": 0.8,
    "statement_of_need": 0.8,
    # Added for gen-0.2 (guide 0.4): instructions between people, the meeting's host, and an answer
    # to the agent that comes after a quick check with someone else.
    "imperative_to_person": 2.5,
    "steps_to_people": 1.0,
    "host_to_group": 1.0,
}
# Kinds only reached through a forced next step.
FORCED_ONLY = {
    "request_after_summon",
    "you_after_invite",
    "resume_no_name",
    "aside_over_agent",
    "name_first_over_agent",
    "answer_after_aside",
}
# Kinds after which the agent answers.
ANSWERED = {
    "name_first",
    "name_mid",
    "name_last",
    "name_misheard",
    "wake_phrase",
    "role_address",
    "named_after_aside",
    "name_first_over_agent",
    "role_request",
    "answer_to_agent_question",
    "answer_after_aside",
    "follow_up",
    "correction",
    "command_no_name",
    "reply_then_request",
    "request_after_summon",
    "action_to_game_master",
    "opener_to_agent",
    "question_only_agent_can_answer",
    "addressed_by_exclusion",
    "only_agent_can_do",
    "you_after_invite",
    "resume_no_name",
}
WAITING = {
    "open_question",
    "open_factual",
    "open_request",
    "unclear_you",
    "about_question",
    "unclear_after_agent",
    "follow_up_by_other",
}
CLOSING = {"thanks_named", "stop_named", "farewell_named", "thanks"}
AFTER_ASK = {
    "answer_to_agent_question",
    "reply_then_request",
    "question_to_named_person",
    "statement_to_named_person",
    "other_device",
    "name_first",
    "never_mind",
}
PERSON_EXCHANGE = {"reply_to_person", "continuing_with_person", "you_to_person", "unclear_you_person_task"}
# Kinds for stretches where the people talk among themselves and nobody involves the agent: the
# start of some conversations, and the whole of a few (an agent that sits in on a meeting).
QUIET_KINDS = {
    "statement",
    "group_question_not_for_agent",
    "remark_to_group",
    "request_to_people",
    "proposal_to_group",
    "table_talk",
    "you_to_person",
    "unclear_you_person_task",
    "reply_to_person",
    "continuing_with_person",
    "backchannel",
    "thinking_aloud",
    "off_call",
    "statement_of_need",
    "question_to_named_person",
    "statement_to_named_person",
    "similar_name_person",
    "imperative_to_person",
    "steps_to_people",
    "host_to_group",
    "other_device",
    "about_judged",
    "about_reported",
    "about_stated",
    "about_hypothetical",
    "name_word_sense",
    "alias_false_match",
}
# Requests the agent could do, to nobody in particular, that can end a quiet opening (even calls).
OPENING_ASKS = {"unclear_you": 3.0, "open_request": 2.0, "open_factual": 1.0, "open_question": 1.0}
# Who settles a pending question from the agent.
SETTLES_ASK = {"answer_to_agent_question", "answer_after_aside", "reply_then_request", "never_mind"}


def _allowed(kind: str, s: State, cast: Cast) -> bool:
    agent_just = s.agent_ago == 0
    answered = s.agent_act in ("answer", "answer_open", "act")
    leads = cast.setting.leads
    n = len(cast.people)
    if kind in FORCED_ONLY:
        return False
    if s.quiet_left > 0 and kind not in QUIET_KINDS:
        return False
    # Right after the agent asks something, a person's next line reads as an answer to it, whatever
    # the plan says. Only lines that plainly answer it, or plainly turn to a named person, fit.
    if agent_just and s.agent_act == "ask":
        return kind in AFTER_ASK
    # Right after the agent answers, a free "reply" between people reads as a reaction to the agent.
    if agent_just and kind in PERSON_EXCHANGE:
        return False
    if kind == "other_device":
        return cast.setting.devices or n >= 2
    if kind in ("name_misheard", "alias_false_match"):
        return bool(cast.aliases) and not cast.unnamed
    if kind == "name_word_sense":
        return cast.agent in WORDLIKE and not cast.unnamed
    if kind in ("name_slip_corrected", "similar_name_person"):
        return not cast.unnamed and n >= 2 and (kind == "name_slip_corrected" or cast.soundalike is not None)
    if kind in ("thanks_named", "stop_named", "thanks"):
        return s.agent_ago <= 1 and s.agent_act in ("answer", "answer_open", "act")
    if kind == "farewell_named":
        return s.lines >= 8
    if kind in ("to_named_person_after_agent", "people_after_agent"):
        return agent_just and answered and n >= 2
    if kind in ("you_to_person_after_agent", "unclear_after_agent", "follow_up_by_other"):
        return agent_just and answered and n >= 2
    if kind in ("follow_up", "correction", "command_no_name"):
        return agent_just and answered and s.partner is not None
    if kind in ("answer_to_agent_question", "reply_then_request"):
        return agent_just and s.agent_act == "ask"
    if kind in ("imperative_to_person", "steps_to_people"):
        # Not where the agent runs the session or controls things: there an instruction with no
        # name may well be for it (exp-024).
        return n >= 2 and s.agent_ago >= 2 and not leads and not cast.setting.controls
    if kind == "host_to_group":
        return n >= 2 and s.agent_ago >= 2
    if kind in ("action_to_game_master", "question_only_agent_can_answer"):
        return leads
    if kind == "addressed_by_exclusion":
        return leads and n >= 2 and s.agent_ago <= 3
    if kind == "only_agent_can_do":
        return s.control is not None and 1 <= s.control_ago <= 6
    if kind == "table_talk":
        return cast.setting.id == "tabletop_game"
    if kind in ("about_pronoun",):
        return s.agent_ago <= 3
    if kind in ("you_to_person", "continuing_with_person", "reply_to_person"):
        return s.exchange is not None or (s.last is not None and s.last.who != AGENT)
    if kind == "off_call":
        return cast.setting.id in ("family_kitchen", "car", "friends_call", "trip_planning", "telehealth_intake")
    if kind in (
        "question_to_named_person",
        "statement_to_named_person",
        "about_to_named_person",
        "you_to_person",
        "unclear_you_person_task",
        "group_question_not_for_agent",
        "request_to_people",
        "proposal_to_group",
    ):
        return n >= 2
    return True


def _pick_speaker(rng: random.Random, cast: Cast, s: State, exclude: str | None = None) -> str:
    pool = [p for p in cast.people if p != exclude] or list(cast.people)
    if s.last and len(pool) > 1 and rng.random() < 0.7:
        pool = [p for p in pool if p != s.last.who] or pool
    return rng.choice(pool)


def _other(rng: random.Random, cast: Cast, not_: str, prefer: str | None = None) -> str:
    if prefer and prefer != not_ and prefer in cast.people:
        return prefer
    pool = [p for p in cast.people if p != not_]
    return rng.choice(pool) if pool else not_


def _speaker_and_target(kind: str, rng: random.Random, cast: Cast, s: State) -> tuple[str, list[str]]:
    """Who says a line of this kind, and whom it names or is for."""
    if kind in ("follow_up", "correction", "command_no_name", "reply_then_request"):
        return s.partner, []
    if kind in ("answer_to_agent_question", "answer_after_aside"):
        return (s.partner if (s.partner and not s.asked_room) else _pick_speaker(rng, cast, s)), []
    if kind == "imperative_to_person":
        if s.last and s.last.who != AGENT:
            return _other(rng, cast, s.last.who), [s.last.who]
        sp = _pick_speaker(rng, cast, s)
        return sp, [_other(rng, cast, sp)]
    if kind in ("follow_up_by_other", "unclear_after_agent", "people_after_agent"):
        return _pick_speaker(rng, cast, s, exclude=s.partner), []
    if kind == "you_to_person_after_agent":
        sp = _pick_speaker(rng, cast, s, exclude=s.partner)
        return sp, [_other(rng, cast, sp, prefer=s.partner)]
    if kind in ("thanks", "thanks_named", "stop_named"):
        return (s.partner or _pick_speaker(rng, cast, s)), []
    if kind == "question_to_named_person" and s.ask_pending and s.agent_ago == 0 and s.partner and not s.asked_room:
        # Asked something by the agent, the person checks with someone else first.
        return s.partner, [_other(rng, cast, s.partner)]
    if kind in (
        "question_to_named_person",
        "statement_to_named_person",
        "to_named_person_after_agent",
        "about_to_named_person",
        "name_slip_corrected",
    ):
        sp = _pick_speaker(rng, cast, s)
        return sp, [_other(rng, cast, sp)]
    if kind == "similar_name_person":
        sp = _pick_speaker(rng, cast, s, exclude=cast.soundalike)
        return sp, [cast.soundalike]
    if kind in ("reply_to_person", "continuing_with_person", "you_to_person"):
        if s.last and s.last.who != AGENT:
            asker = s.last.who
            if kind == "reply_to_person":
                sp = s.last.target[0] if s.last.target and s.last.target[0] != asker else _other(rng, cast, asker)
                return sp, [asker]
            if s.exchange and asker in s.exchange:
                sp = asker
                return sp, [s.exchange[0] if s.exchange[1] == asker else s.exchange[1]]
            return asker, [_other(rng, cast, asker)]
        sp = _pick_speaker(rng, cast, s)
        return sp, [_other(rng, cast, sp)]
    if kind == "unclear_you_person_task":
        sp = _pick_speaker(rng, cast, s)
        return sp, [_other(rng, cast, sp)]
    return _pick_speaker(rng, cast, s), []


def _agent_after(kind: str, rng: random.Random, cast: Cast, speaker: str, s: State) -> Beat | None:
    """The agent's reply to a person's line, if it gives one."""
    leads = cast.setting.leads
    if kind == "name_alone":
        return Beat(AGENT, act="yes", extra={"partner": speaker})
    if kind in ANSWERED:
        roll = rng.random()
        if leads and roll < 0.45:
            return Beat(AGENT, act="ask", extra={"partner": speaker, "room": rng.random() < 0.3})
        if not leads and roll < 0.12:
            return Beat(AGENT, act="ask", extra={"partner": speaker, "room": False, "clarify": True})
        if cast.setting.controls and roll < 0.35:
            return Beat(AGENT, act="act", extra={"partner": speaker, "control": rng.choice(cast.setting.controls)})
        if roll < 0.08 + (0.12 if not leads else 0):
            return Beat(AGENT, act="interrupted", extra={"partner": speaker})
        return Beat(AGENT, act="answer", extra={"partner": speaker})
    if kind in CLOSING and rng.random() < (0.8 if kind != "thanks" else 0.5):
        return Beat(AGENT, act="ack", extra={"partner": speaker})
    return None


def plan(
    rng: random.Random,
    cast: Cast,
    lines: tuple[int, int] = (11, 17),
    boost: dict[str, float] | None = None,
    quiet: tuple[float, float] | None = (0.0, 0.0),
    after_quiet: float = 0.0,
) -> list[Beat]:
    """A plan: people's lines and the agent's replies, in order. `boost` multiplies kinds' weights.

    `quiet` is (share of conversations where nobody involves the agent, share that open with 3 to 8
    lines of people among themselves). The default keeps gen-0.1's plans; None gives gen-0.2's
    (0.08, 0.25). `after_quiet` is the chance that a quiet opening ends with a request the agent
    could do, put to nobody in particular (an even call): an agent that has not spoken yet can
    still be wanted (round 2 learned the opposite, exp-022)."""
    boost = boost or {}
    target_lines = rng.randint(*lines)
    s = State()
    beats: list[Beat] = []
    queue: list[Beat] = []  # forced next steps
    if quiet is None:
        quiet = (0.08, 0.25)
    opening_ask = False
    if quiet[0] or quiet[1]:  # draws nothing otherwise, so gen-0.1's plans replay
        roll = rng.random()
        if len(cast.people) >= 2 and roll < quiet[0]:
            s.quiet_left = target_lines  # the agent is never involved
        elif len(cast.people) >= 2 and roll < quiet[0] + quiet[1]:
            s.quiet_left = rng.randint(3, 8)  # the people talk among themselves first
            opening_ask = after_quiet > 0 and rng.random() < after_quiet

    if cast.setting.leads and not s.quiet_left and rng.random() < 0.6:
        first = cast.people[0]
        if rng.random() < 0.5:
            beats.append(Beat(first, kind="opener_to_agent"))
            beats.append(Beat(AGENT, act="ask", extra={"partner": first, "room": False}))
        else:
            beats.append(Beat(AGENT, act="ask", extra={"partner": None, "room": True, "opening": True}))

    def apply_agent(b: Beat) -> None:
        s.agent_act, s.agent_ago, s.partner = b.act, 0, b.extra.get("partner")
        s.ask_pending = b.act == "ask"
        s.asked_room = bool(b.extra.get("room"))
        s.interrupted = b.act == "interrupted"
        if b.act == "act":
            s.control, s.control_ago = b.extra["control"], 0

    for b in beats:
        if b.who == AGENT:
            apply_agent(b)
        else:
            s.lines += 1

    guard = 0
    while s.lines < target_lines and guard < 200:
        guard += 1
        if queue:
            beat = queue.pop(0)
        else:
            kinds = [k for k, w in WEIGHTS.items() if w > 0 and _allowed(k, s, cast)]
            weights = [WEIGHTS[k] * boost.get(k, 1.0) for k in kinds]
            if s.agent_ago == 0 and s.agent_act in ("answer", "answer_open", "act", "ask"):
                # Right after the agent speaks, lean on the rhythm-dependent kinds.
                weights = [
                    w
                    * (
                        3
                        if k
                        in (
                            "follow_up",
                            "follow_up_by_other",
                            "unclear_after_agent",
                            "people_after_agent",
                            "you_to_person_after_agent",
                            "to_named_person_after_agent",
                            "answer_to_agent_question",
                            "thanks",
                            "correction",
                            "command_no_name",
                            "reply_then_request",
                        )
                        else 1
                    )
                    for k, w in zip(kinds, weights)
                ]
            kind = rng.choices(kinds, weights)[0]
            speaker, target = _speaker_and_target(kind, rng, cast, s)
            beat = Beat(speaker, kind=kind, target=[t for t in target if t])
            if kind == "other_device":
                beat.extra["device"] = rng.choice(DEVICES)
            if kind == "only_agent_can_do":
                beat.extra["control"] = s.control
            if kind == "name_misheard" or kind == "alias_false_match":
                beat.extra["alias"] = rng.choice(cast.aliases)

        beats.append(beat)
        s.lines += 1
        was_quiet = s.quiet_left > 0
        s.quiet_left = max(0, s.quiet_left - 1)
        if was_quiet and s.quiet_left == 0 and opening_ask and not queue:
            ask = rng.choices(list(OPENING_ASKS), list(OPENING_ASKS.values()))[0]
            queue.append(Beat(_pick_speaker(rng, cast, s), kind=ask))
        if beat.kind in SETTLES_ASK:
            s.ask_pending = False
        prev_agent_ago = s.agent_ago
        s.agent_ago += 1
        s.control_ago += 1

        # What happens next.
        k = beat.kind
        reply = _agent_after(k, rng, cast, beat.who, s)
        if k == "name_alone":
            queue.insert(0, Beat(beat.who, kind="request_after_summon"))
        elif k in WAITING:
            if rng.random() < 0.5 and len(cast.people) >= 2:
                queue.insert(
                    0,
                    Beat(
                        _other(
                            rng,
                            cast,
                            beat.who,
                            prefer=s.partner if k in ("unclear_after_agent", "follow_up_by_other") else None,
                        ),
                        kind="reply_to_person",
                        target=[beat.who],
                    ),
                )
            else:
                reply = Beat(AGENT, act="answer_open", extra={"partner": beat.who})
        elif k in ("invite", "relayed_invite", "indirect_wish"):
            roll = rng.random()
            if roll < 0.35:
                reply = Beat(AGENT, act="answer", extra={"partner": beat.who})
            elif roll < 0.75:
                asker = _other(rng, cast, beat.who) if k == "invite" else beat.who
                queue.insert(0, Beat(asker, kind="you_after_invite"))
        elif (
            k
            in (
                "question_to_named_person",
                "statement_to_named_person",
                "to_named_person_after_agent",
                "similar_name_person",
            )
            and rng.random() < 0.75
        ):
            queue.insert(0, Beat(beat.target[0], kind="reply_to_person", target=[beat.who]))
            s.exchange = (beat.who, beat.target[0])
            if k == "question_to_named_person" and s.ask_pending and prev_agent_ago == 0 and rng.random() < 0.7:
                # ... then answers the agent's question with what they were told.
                queue.insert(1, Beat(beat.who, kind="answer_after_aside"))
        elif (
            k in ("group_question_not_for_agent", "proposal_to_group", "request_to_people", "statement")
            and rng.random() < 0.5
        ):
            queue.insert(0, Beat(_other(rng, cast, beat.who), kind="reply_to_person", target=[beat.who]))
        if k in ("reply_to_person",) and beat.target:
            s.exchange = (beat.who, beat.target[0])

        if reply is not None:
            beats.append(reply)
            apply_agent(reply)
            if reply.act == "interrupted":
                roll = rng.random()
                partner = reply.extra["partner"]
                if roll < 0.4 and len(cast.people) >= 2:
                    other = _other(rng, cast, partner)
                    queue.insert(0, Beat(other, kind="aside_over_agent", target=[partner], over_agent=True))
                    if rng.random() < 0.6:
                        queue.insert(1, Beat(partner, kind="reply_to_person", target=[other]))
                        queue.insert(2, Beat(partner, kind="resume_no_name"))
                elif roll < 0.65:
                    queue.insert(0, Beat(rng.choice(cast.people), kind="name_first_over_agent", over_agent=True))
                elif roll < 0.85:
                    queue.insert(0, Beat(partner, kind="stop_named", over_agent=True))
                else:
                    queue.insert(0, Beat(_other(rng, cast, partner), kind="backchannel", over_agent=True))
        else:
            if prev_agent_ago == 0 and s.interrupted:
                s.interrupted = False
        s.last = beat
    return beats


def describe(beats: list[Beat]) -> list[dict]:
    return [asdict(b) for b in beats]
