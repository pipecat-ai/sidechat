"""Turn a plan into a writer prompt, read the writer's lines back, and check each against its brief.

The writer model only supplies words. A line that breaks its brief (it calls the agent when it
should not, or leaves out the name it should use) is kept and flagged: the committee decides what
it is. Audience learned that dropping such lines makes the rules look better than they are.
"""

from __future__ import annotations

import json
import re

from sidechat.gen.planner import AGENT, Beat
from sidechat.gen.world import DEVICES, UNNAMED, Cast

# What each kind of line must do, for the writer. {agent} is how to call the agent; {target} the
# person named; {device}, {control} and {alias} come from the beat.
BRIEFS: dict[str, str] = {
    "other_device": "speaks to another device, starting with '{device}', and asks it for something. Not to {agent}",
    "name_first": "calls {agent} by name at the start and asks or tells it something",
    "name_mid": "says something to the others, then calls {agent} by name mid-line and asks it something",
    "name_last": "asks something and ends the line with {agent}'s name, calling it",
    "name_alone": "says only {agent}'s name, to get its attention (e.g. '{agent}?')",
    "name_misheard": "calls the agent using the misheard form '{alias}' as if it were its name, then asks something; write it in lower case without punctuation, as speech-to-text would",
    "wake_phrase": "starts with 'Hey {agent}' or 'OK {agent}' and gives a request",
    "role_address": "calls the agent by its role ('Assistant, ...' or 'Hey AI, ...'), not by name, and asks something",
    "named_after_aside": "makes a short remark to the others, then calls {agent} by name and asks it something",
    "name_first_over_agent": "cuts in while {agent} is talking: calls it by name and asks for something else",
    "thanks_named": "thanks {agent} by name for what it just did",
    "stop_named": "tells {agent}, by name, that's enough or to stop",
    "farewell_named": "says goodbye or goodnight to {agent} by name",
    "never_mind": "starts a request to {agent} by name, then takes it back ('actually, never mind')",
    "name_slip_corrected": "starts to call {agent} by name by mistake, corrects to {target}, and asks {target} something",
    "question_to_named_person": "asks {target} a question, calling them by name",
    "statement_to_named_person": "tells {target} something, calling them by name",
    "to_named_person_after_agent": "turns to {target} by name about what {agent} just said",
    "similar_name_person": "calls {target} by name (a name that sounds like the agent's) and asks them something",
    "about_to_named_person": "asks {target}, by name, something about {agent} (mention {agent} in the third person)",
    "role_request": "asks for {agent} to do or answer something, talking about it in the third person ('Can the assistant ...?', 'I'd like {agent} to ...')",
    "relayed_invite": "asks one of the others to get {agent} to do something for them",
    "invite": "suggests {agent} would know or tells someone to ask it (e.g. '{agent} would know.', 'Ask {agent}.')",
    "indirect_wish": "says aloud they'd like {agent}'s view on something, without asking it directly",
    "about_question": "asks the room a question about {agent} that it could answer itself (e.g. whether it is recording)",
    "about_hypothetical": "proposes asking {agent} later, as a question or suggestion to the others ('Should we ask {agent}?')",
    "about_judged": "gives an opinion about {agent} to the others",
    "about_pronoun": "comments on {agent} to the others as 'it', without its name",
    "about_quoted": "quotes something someone said to {agent} earlier, as a story to the others",
    "about_reported": "reports to the others something {agent} said or did earlier",
    "about_stated": "states a plain fact about {agent} to the others",
    "about_question_to_group": "asks the others whether they have used {agent} for something",
    "name_word_sense": "uses the word '{agent_lower}' in its ordinary meaning (not as a name, not calling the agent), talking to the others",
    "alias_false_match": "says something to the others containing the phrase '{alias}' in its ordinary meaning, in lower case without punctuation",
    "answer_to_agent_question": "answers the question {agent} just asked, briefly and without its name",
    "follow_up": "follows up on {agent}'s answer to them with a related question or request, without its name",
    "correction": "corrects what {agent} just did or said, without its name ('No, the other one')",
    "command_no_name": "gives {agent} a short command continuing what it is doing, without its name",
    "reply_then_request": "answers {agent}'s question, then asks it for more, without its name",
    "request_after_summon": "now says what they wanted from {agent}, without its name",
    "thanks": "thanks {agent} for its answer, without its name",
    "action_to_game_master": "carries on the session {agent} is running (an action, an answer, a request about it), without its name",
    "opener_to_agent": "opens the session with {agent}, saying why they are here, without its name",
    "question_only_agent_can_answer": "asks something about the session that only {agent} could know, without its name or 'you' to anyone else",
    "addressed_by_exclusion": "while another person is busy, carries on the session with {agent} for them, without its name",
    "you_after_invite": "now asks the agent directly as 'you', without its name",
    "resume_no_name": "tells {agent} to carry on ('Go on', 'Sorry, keep going'), without its name",
    "only_agent_can_do": "asks for something about the {control} the agent set up, without its name (e.g. turn it off, change it)",
    "you_to_person_after_agent": "says something to {target} with 'you', about {agent}'s answer, without any name",
    "unclear_after_agent": "questions or challenges {agent}'s answer in a way that could be for {agent} or for the others, without any name",
    "follow_up_by_other": "follows up on {agent}'s answer to someone else with a related question, without any name",
    "open_question": "asks the room a question anyone could answer ('Does anyone know ...?'), without any name",
    "open_factual": "asks a factual question to nobody in particular, without any name",
    "open_request": "asks for a lookup or small task from nobody in particular ('Can someone check ...?'), without any name",
    "unclear_you": "asks 'you' for something the agent could do, with no name, so it is unclear who is meant",
    "group_question_not_for_agent": "asks the others something about themselves (their plans, opinions, what they did), without any name",
    "remark_to_group": "makes a remark to the others about how things are for them right now",
    "request_to_people": "asks the others to do something only people can do",
    "proposal_to_group": "proposes something to the others",
    "table_talk": "talks to the other players about their own plan, without any name",
    "you_to_person": "says something to {target} with 'you', continuing their exchange, without any name",
    "unclear_you_person_task": "asks 'you' for something only a person could do (send a file, pass something), without any name",
    "statement": "says something to the others about the topic",
    "people_after_agent": "reacts to {agent}'s answer with a comment to the others that asks nothing",
    "reply_to_person": "replies to what {target} just said, without any name",
    "continuing_with_person": "carries on the exchange with {target}, without any name",
    "backchannel": "says only a short acknowledgement ('mm-hm', 'right', 'yeah')",
    "thinking_aloud": "thinks aloud, half to themselves, trailing off",
    "off_call": "speaks to someone who is not on the call (a child, a delivery, someone on the phone)",
    "statement_of_need": "says they don't understand or don't know something, without asking anyone",
    "aside_over_agent": "cuts in while {agent} is still talking, with a quick aside to {target} about something else",
    # gen-0.2
    "answer_after_aside": "now answers the question {agent} asked a few lines ago, using what the others just said, briefly and without its name",
    "imperative_to_person": "tells {target} to do something only they can do with their own hands, screen or turn (move on to their own next slide, carry on talking, hold or pass something, try it again), as a short bare instruction with no name and no 'you'; never a lookup, a note, music or anything an assistant could do",
    "steps_to_people": "explains to the others how to do something, as a few plain instructions ('open it, then press ...'), without any name",
    "host_to_group": "runs the meeting for the others: asks if they have questions, moves on to the next item, or wraps up a part, without any name",
    # gen-0.4
    "follow_up_after_reaction": "after the other person's quick reaction, carries on with {agent}: a related question, request or short command about its answer to them, without its name; plainly for {agent}, not a reply to the reaction",
    "relay_agent_answer": "tells {target} what {agent} just said or did, naming {agent} in the third person ('{agent} says ...', 'so {agent} reckons ...'); asks {agent} nothing",
}

AGENT_BRIEFS = {
    "answer": "{agent} answers {partner} in one or two short sentences, with a concrete, plausible answer",
    "answer_open": "after a pause in which nobody answered, {agent} answers the question briefly",
    "ask": "{agent} asks {who} a short question that moves its session on",
    "clarify": "{agent} asks {partner} a short clarifying question",
    "yes": "{agent} says only 'Yes?' or a two-word equivalent",
    "ack": "{agent} gives a two- or three-word acknowledgement",
    "act": "{agent} confirms in a few words that it did what {partner} asked with the {control}",
    "interrupted": "{agent} starts a long answer to {partner} and is cut off mid-sentence: end the line with '—'",
}

SYSTEM = """You write realistic transcripts of spoken conversations between several people and an AI agent that is with them. The transcripts train a model that decides whether each line was meant for the agent, so every line must do exactly what its beat says.

Rules:
- One line per beat, in order, said by the speaker given, doing what the beat says.
- Write speech, not prose: natural, varied, usually 3 to 25 words, in the register given. No stage directions, no narration.
- People rarely use each other's names. Use a name only where the beat says to call someone by name.
- Never say the agent's name or call it (by name, or as 'assistant', 'AI', 'bot') unless the beat says to.
- Keep the conversation coherent and on the topic. Invent concrete details (numbers, places, times) freely.
- Never mention beats, plans, rules or labels.

Answer with JSON only: {"lines": [{"beat": 1, "text": "..."}, ...]}"""

OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["lines"],
    "properties": {
        "lines": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["beat", "text"],
                "properties": {"beat": {"type": "integer"}, "text": {"type": "string"}},
            },
        }
    },
}


def _agent_word(cast: Cast) -> str:
    return "the assistant" if cast.unnamed else cast.agent


def beat_text(b: Beat, cast: Cast) -> str:
    agent = _agent_word(cast)
    if b.who == AGENT:
        act = "clarify" if b.act == "ask" and b.extra.get("clarify") else b.act
        who = "everyone" if b.extra.get("room") or not b.extra.get("partner") else b.extra.get("partner")
        return AGENT_BRIEFS[act].format(
            agent=agent, partner=b.extra.get("partner") or "them", who=who, control=b.extra.get("control", "thing")
        )
    brief = BRIEFS[b.kind].format(
        agent=agent,
        agent_lower=cast.agent.lower(),
        target=(b.target[0] if b.target else "someone"),
        device=b.extra.get("device", DEVICES[0]),
        control=b.extra.get("control", "timer"),
        alias=b.extra.get("alias", ""),
    )
    return ("(while the agent is still speaking) " if b.over_agent else "") + brief


def user_prompt(cast: Cast, beats: list[Beat]) -> str:
    agent = _agent_word(cast)
    if cast.unnamed:
        calls = "it has no name; people call it 'the assistant', 'the AI' or 'the bot'"
    else:
        calls = f"its name is {cast.agent}"
    lines = [
        f"Setting: {cast.setting.scene}. Topic: {cast.topic}.",
        f"The agent: {cast.setting.role}; {calls}.",
        f"People: {', '.join(cast.people)}.",
        f"Register: {cast.register}.",
        "",
        "Beats:",
    ]
    for n, b in enumerate(beats, start=1):
        who = agent if b.who == AGENT else b.who
        lines.append(f"{n}. {who}: {beat_text(b, cast)}.")
    return "\n".join(lines)


def parse_lines(text: str, n: int) -> list[str]:
    """The writer's lines, one per beat. Raises ValueError when they do not fit the plan."""
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("no JSON object")
    data = json.loads(text[start : end + 1])
    got = {int(x["beat"]): str(x["text"]).strip() for x in data.get("lines", []) if str(x.get("text", "")).strip()}
    missing = [i for i in range(1, n + 1) if i not in got]
    if missing:
        raise ValueError(f"missing beats {missing[:5]}")
    return [_unquote(got[i]) for i in range(1, n + 1)]


def _unquote(text: str) -> str:
    text = (
        re.sub(r"^\s*[A-Z][\w ]{0,20}:\s+", "", text)
        if re.match(r"^\s*[A-Z][\w ]{0,20}:\s+\S", text) and ":" in text[:22]
        else text
    )
    return text.strip().strip('"').strip("“”").strip()


# --- checks -----------------------------------------------------------------------------------

MUST_CALL = {
    "name_first",
    "name_mid",
    "name_last",
    "name_alone",
    "wake_phrase",
    "named_after_aside",
    "name_first_over_agent",
    "thanks_named",
    "stop_named",
    "farewell_named",
    "never_mind",
    "name_slip_corrected",
}
MUST_MENTION = {
    "role_request",
    "relayed_invite",
    "invite",
    "indirect_wish",
    "about_hypothetical",
    "about_judged",
    "about_quoted",
    "about_reported",
    "about_stated",
    "about_question_to_group",
    "about_to_named_person",
    "relay_agent_answer",
}
MUST_NAME_TARGET = {
    "question_to_named_person",
    "statement_to_named_person",
    "to_named_person_after_agent",
    "similar_name_person",
    "about_to_named_person",
    "name_slip_corrected",
}
ROLE_WORDS = r"\b(assistant|the ai|hey ai|ai|bot)\b"


def _has(text: str, phrase: str) -> bool:
    return bool(re.search(rf"(?<!\w){re.escape(phrase.lower())}(?!\w)", text.lower()))


def check(b: Beat, text: str, cast: Cast) -> list[str]:
    """Reasons this line breaks its brief; empty when it keeps to it."""
    k, problems = b.kind, []
    words = len(text.split())
    if words == 0 or words > 70:
        problems.append(f"length {words} words")
    # The name as written with a capital: a word-like name ("Max", "Dash") in lower case is a word.
    called = (not cast.unnamed and bool(re.search(rf"(?<!\w){re.escape(cast.agent)}(?!\w)", text))) or any(
        _has(text, a) for a in cast.aliases
    )
    role = bool(re.search(ROLE_WORDS, text.lower()))
    if k in MUST_CALL and not (called or (cast.unnamed and role)):
        problems.append("does not call the agent")
    if k == "role_address" and not role:
        problems.append("does not call the agent by role")
    if k == "name_misheard" and not any(_has(text, a) for a in cast.aliases):
        problems.append("misheard name missing")
    if k in MUST_MENTION and not (called or role or (cast.unnamed and any(_has(text, u) for u in UNNAMED))):
        problems.append("does not mention the agent")
    if k == "about_pronoun" and called:
        problems.append("uses the agent's name")
    if k == "invite" and not (called or role or _has(text, "it")):
        problems.append("does not point at the agent")
    if k == "name_word_sense" and not _has(text, cast.agent.lower()):
        problems.append("word missing")
    if k == "alias_false_match" and not any(_has(text, a) for a in cast.aliases):
        problems.append("alias phrase missing")
    must_not = k not in MUST_CALL | MUST_MENTION | {
        "role_address",
        "name_misheard",
        "name_word_sense",
        "alias_false_match",
        "invite",
        "about_question",
        "about_pronoun",
    }
    if must_not and (called or (cast.unnamed and role)):
        problems.append("calls or names the agent")
    if k in MUST_NAME_TARGET and b.target and not _has(text, b.target[0]):
        problems.append(f"does not name {b.target[0]}")
    if k == "other_device" and not any(
        w in text.lower() for w in ("siri", "google", "alexa", "cortana", "hey tv", "ok car")
    ):
        problems.append("no device named")
    return problems
