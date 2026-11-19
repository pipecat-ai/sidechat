"""Labelling guide 0.3 as code: one label per kind of line.

The prose is `contracts/sidechat-guide-0.3.md`, which the labelling committee reads. This module is
the same rules for code: a hand-written suite or a generated conversation names each line's kind,
and its label comes from here. Every kind cites the rule (G1 to G8) that decides it. A test checks
that every kind used in a guide-labelled suite is defined here.

`speak` is the guide's 1-to-5 scale. It becomes the `respond` target as (speak - 1) / 4, so 1 is
0.0, 3 is 0.5 and 5 is 1.0.
"""

from __future__ import annotations

from dataclasses import dataclass

from sidechat.schema import SidechatLabel

GUIDE_VERSION = "sidechat-guide-0.4"
GUIDE_FILE = "contracts/sidechat-guide-0.4.md"
# 0.3 added how to read anonymous speaker labels; no kind changed.
# 0.2 added `follow_up_by_other` and `only_agent_can_do` and changed no existing kind, so a suite
# labelled under 0.1 gets the same labels here.

RULES = {
    "G1": "another device",
    "G2": "the agent is called",
    "G3": "a person is called",
    "G4": "the agent is mentioned, not called",
    "G5": "the name is an ordinary word",
    "G6": "nobody is called, the agent is in the conversation",
    "G7": "nobody is called, the agent is not in play",
    "G8": "spoken over the agent",
}


def speak_to_respond(speak: float) -> float:
    return round((speak - 1) / 4, 4)


@dataclass(frozen=True)
class KindRule:
    rule: str
    to: str  # agent, person, group, device, nobody, unclear
    intent: str | None  # None: whichever is likelier (unclear lines)
    expect: str | None  # respond, wait, ignore; None: either decision is reasonable
    speak: int
    about: str

    def label(self, people: list[str] | None = None) -> SidechatLabel:
        to = self.to
        if people and to in ("group", "person"):
            to = "person"
        return SidechatLabel(
            to="unknown" if to == "unclear" else to,
            to_people=list(people or []),
            intent=self.intent,
            expect=self.expect,
            respond=speak_to_respond(self.speak),
            unclear=to == "unclear",
            source="guide",
        )


def _k(rule, to, intent, expect, speak, about) -> KindRule:
    return KindRule(rule, to, intent, expect, speak, about)


KINDS: dict[str, KindRule] = {
    # G1
    "other_device": _k("G1", "device", "other", "ignore", 1, "calls another voice assistant or machine"),
    # G2: the agent is called
    "name_first": _k("G2", "agent", "direct", "respond", 5, "calls the agent by name at the start"),
    "name_mid": _k("G2", "agent", "direct", "respond", 5, "calls the agent by name mid-line"),
    "name_last": _k("G2", "agent", "direct", "respond", 5, "calls the agent by name at the end"),
    "name_alone": _k("G2", "agent", "direct", "respond", 5, "the agent's name alone, a summons"),
    "name_misheard": _k("G2", "agent", "direct", "respond", 5, "calls the agent by a misheard name"),
    "wake_phrase": _k("G2", "agent", "direct", "respond", 5, "hey X / OK X"),
    "role_address": _k("G2", "agent", "direct", "respond", 5, "calls the agent by role: 'Assistant, ...'"),
    "named_after_aside": _k("G2", "agent", "direct", "respond", 5, "a remark to the room, then calls the agent"),
    "name_first_over_agent": _k("G2", "agent", "direct", "respond", 5, "calls the agent while it is speaking"),
    "thanks_named": _k("G2", "agent", "direct", "respond", 4, "thanks the agent by name"),
    "stop_named": _k("G2", "agent", "direct", "respond", 4, "tells the agent by name that's enough"),
    "farewell_named": _k("G2", "agent", "direct", "respond", 4, "says goodbye to the agent by name"),
    "never_mind": _k("G2", "agent", "direct", "ignore", 1, "calls the agent, then takes the request back"),
    "name_slip_corrected": _k(
        "G2", "person", "other", "ignore", 1, "says the agent's name by mistake, corrects to a person"
    ),
    # G3: a person is called
    "question_to_named_person": _k("G3", "person", "other", "ignore", 1, "a question to a named person"),
    "statement_to_named_person": _k("G3", "person", "other", "ignore", 1, "a statement to a named person"),
    "to_named_person_after_agent": _k(
        "G3", "person", "other", "ignore", 1, "right after the agent spoke, names a person"
    ),
    "similar_name_person": _k(
        "G3", "person", "other", "ignore", 1, "calls a person whose name sounds like the agent's"
    ),
    "about_to_named_person": _k("G3", "person", "about", "ignore", 1, "asks a named person about the agent"),
    # G4: the agent is mentioned, not called
    "role_request": _k("G4", "agent", "indirect", "respond", 4, "asks for the agent to act, said about it"),
    "relayed_invite": _k("G4", "group", "indirect", None, 3, "asks someone to pass a request to the agent"),
    "invite": _k("G4", "group", "indirect", None, 3, "invites the agent to answer: 'Atlas would know'"),
    "indirect_wish": _k("G4", "group", "indirect", None, 3, "wishes aloud for the agent's input"),
    "about_question": _k("G4", "group", "open", "wait", 3, "a question about the agent it could answer itself"),
    "about_hypothetical": _k("G4", "group", "about", "ignore", 1, "proposes asking the agent later"),
    "about_judged": _k("G4", "group", "about", "ignore", 1, "judges the agent"),
    "about_pronoun": _k("G4", "group", "about", "ignore", 1, "talks about the agent as 'it'"),
    "about_quoted": _k("G4", "group", "about", "ignore", 1, "quotes something said to the agent"),
    "about_reported": _k("G4", "group", "about", "ignore", 1, "reports an earlier exchange with the agent"),
    "about_stated": _k("G4", "group", "about", "ignore", 1, "states a fact about the agent"),
    "about_question_to_group": _k("G4", "group", "about", "ignore", 1, "asks the people about their use of the agent"),
    # G5: the name as an ordinary word
    "name_word_sense": _k("G5", "group", "other", "ignore", 1, "the agent's name used as an ordinary word"),
    "alias_false_match": _k("G5", "group", "other", "ignore", 1, "words that sound like the agent's name"),
    # G6: nobody is called, the agent is in the conversation
    "answer_to_agent_question": _k("G6", "agent", "direct", "respond", 5, "answers the agent's question"),
    "answer_after_aside": _k(
        "G6", "agent", "direct", "respond", 5, "answers the agent's question after checking with someone else"
    ),
    "follow_up": _k("G6", "agent", "direct", "respond", 5, "a follow-up in the speaker's exchange with the agent"),
    "correction": _k("G6", "agent", "direct", "respond", 5, "corrects what the agent just did"),
    "command_no_name": _k("G6", "agent", "direct", "respond", 5, "a command in the speaker's exchange with the agent"),
    "resume_no_name": _k("G6", "agent", "direct", "respond", 5, "asks the agent to carry on"),
    "reply_then_request": _k("G6", "agent", "direct", "respond", 5, "answers the agent, then asks for more"),
    "request_after_summon": _k("G6", "agent", "direct", "respond", 5, "the request after calling the agent's name"),
    "thanks": _k("G6", "agent", "direct", None, 3, "thanks the agent without its name"),
    "action_to_game_master": _k(
        "G6", "agent", "direct", "respond", 5, "declares an action to the agent running the game"
    ),
    "opener_to_agent": _k("G6", "agent", "direct", "respond", 5, "opens a session the agent leads"),
    "question_only_agent_can_answer": _k(
        "G6", "agent", "direct", "respond", 5, "a question about the session only the agent can answer"
    ),
    "addressed_by_exclusion": _k(
        "G6", "agent", "direct", "respond", 5, "carries on the session's business while others are busy"
    ),
    "you_after_invite": _k("G6", "agent", "direct", "respond", 5, "'you' right after the agent was invited"),
    "only_agent_can_do": _k("G6", "agent", "direct", "respond", 5, "asks for something only the agent can do or know"),
    "follow_up_by_other": _k(
        "G6",
        "unclear",
        None,
        "wait",
        3,
        "follows up the agent's answer to someone else; could be for the agent or a person",
    ),
    "you_to_person_after_agent": _k(
        "G6", "person", "other", "ignore", 1, "'you' that only fits a person, right after the agent spoke"
    ),
    "unclear_after_agent": _k(
        "G6", "unclear", None, "wait", 3, "reacts to the agent's answer; could be for the agent or a person"
    ),
    # G7: nobody is called, the agent is not in play
    "open_question": _k("G7", "group", "open", "wait", 3, "a question to the room the agent could answer"),
    "open_factual": _k("G7", "group", "open", "wait", 3, "a factual question to nobody in particular"),
    "open_request": _k("G7", "group", "open", "wait", 3, "a request to nobody in particular the agent could do"),
    "unclear_you": _k(
        "G7", "unclear", "open", "wait", 3, "a 'you' request with no settled addressee the agent could do"
    ),
    "group_question_not_for_agent": _k("G7", "group", "other", "ignore", 1, "a question about the people themselves"),
    "remark_to_group": _k("G7", "group", "other", "ignore", 1, "a remark about the people's own experience"),
    "request_to_people": _k("G7", "group", "other", "ignore", 1, "a request only the people can carry out"),
    "proposal_to_group": _k("G7", "group", "other", "ignore", 1, "proposes something to the group"),
    "table_talk": _k("G7", "group", "other", "ignore", 1, "players or colleagues talking among themselves"),
    "you_to_person": _k("G7", "person", "other", "ignore", 1, "'you' to a person in their exchange"),
    "unclear_you_person_task": _k("G7", "person", "other", "ignore", 1, "'you' asking for a task only a person can do"),
    "statement": _k("G7", "group", "other", "ignore", 1, "a statement to the group"),
    "imperative_to_person": _k(
        "G7", "person", "other", "ignore", 1, "a bare instruction only a person can carry out, no name, no 'you'"
    ),
    "steps_to_people": _k("G7", "group", "other", "ignore", 1, "explains steps to the people as instructions"),
    "host_to_group": _k("G7", "group", "other", "ignore", 1, "the person running the meeting manages it"),
    "people_after_agent": _k(
        "G7", "group", "other", "ignore", 1, "people react to the agent's answer among themselves"
    ),
    "answer_to_relayed_question": _k(
        "G7", "group", "other", "ignore", 1, "a person answers a question the agent relayed"
    ),
    "reply_to_person": _k("G7", "person", "other", "ignore", 1, "a reply to a person"),
    "continuing_with_person": _k("G7", "person", "other", "ignore", 1, "carries on an exchange with a person"),
    "backchannel": _k("G7", "nobody", "other", "ignore", 1, "an acknowledgement: mm-hm, right"),
    "thinking_aloud": _k("G7", "nobody", "other", "ignore", 1, "thinking aloud"),
    "off_call": _k("G7", "nobody", "other", "ignore", 1, "talks to someone not on the call"),
    "statement_of_need": _k("G7", "group", "other", "ignore", 2, "states a need without asking for anything"),
    # G8: spoken over the agent
    "aside_over_agent": _k("G8", "person", "other", "ignore", 1, "an aside to a person while the agent speaks"),
}


def label_for(kind: str, people: list[str] | None = None) -> SidechatLabel:
    if kind not in KINDS:
        raise KeyError(f"kind {kind!r} is not in {GUIDE_VERSION}")
    return KINDS[kind].label(people)
