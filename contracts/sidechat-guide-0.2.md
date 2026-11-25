# Sidechat labelling guide 0.2

Several people are talking. One AI agent is with them and hears everything. For one line of the
conversation, decide who the line was for and what the agent should do about it.

The agent speaks when it is spoken to, and when a question is left open to the room that it could
answer. It does not volunteer help nobody asked for, and it does not talk over conversations
between people.

## What you are given

- **The agent:** its name, other names it answers to (including ways speech-to-text mishears
  them), and its role, e.g. "AI assistant on the call" or "game master running the adventure".
- **The people present**, by name.
- **The conversation so far:** up to eight earlier lines, oldest first, each with its speaker. The
  agent's own lines are marked.
- **The line to label** and who said it.

Lines may come from speech-to-text: lower case, no punctuation, words misheard. Read them as
speech.

## What you answer

| Field | Values | Meaning |
|---|---|---|
| `to` | `agent`, `person`, `group`, `device`, `nobody`, `unclear` | Who the speaker is talking to. `group` is the people together. `device` is another voice assistant or machine. `nobody` is thinking aloud, a bare acknowledgement, or someone who is not on the call. `unclear` when the line fits the agent and a person equally |
| `people` | Names | The people it is for, when `to` is `person` |
| `intent` | `direct`, `indirect`, `open`, `about`, `other` | See below |
| `decision` | `respond`, `wait`, `ignore` | What the agent should do now |
| `speak` | 1 to 5 | How much the agent should speak now. 1: must stay silent. 2: better silent. 3: an even call: either is fine, or only if nobody else takes it. 4: should speak. 5: must speak now |

**Intent:**

- `direct`: said to the agent. By name or role, as "you" in an exchange with it, as an answer to
  its question, or as a follow-up to its answer.
- `indirect`: not said to the agent, but asks for it to act or answer: "Can the assistant read us
  the action items?", "Can one of you get the assistant to email me the slides?", "Rook will know
  the rules."
- `open`: a question or request to nobody in particular that the agent could answer or do.
- `about`: mentions the agent and wants nothing from it: "I asked Nova on Monday."
- `other`: everything else: lines for people, the group, another device, or nobody.

**Decision:**

- `respond`: the agent should speak now.
- `wait`: the agent should answer only if nobody else does within a few seconds.
- `ignore`: the agent should stay silent.

`speak` 3 is an even call. Use it when the line leaves it open whether the agent is wanted, for
example a question to the room that nothing earlier settles. The system using the agent decides
what to do with an even call, such as taking the floor after a pause.

**Read the turns before the line.** Who spoke to whom in the last few lines often settles it:
whether the agent just spoke, whose question it answered, and whether the speaker is the person it
was talking with.

## The rules

Apply them in order. The first rule that fits decides.

### G1. Another device

The line calls another voice assistant or machine: "Hey Siri, …", "OK Google, …", "Alexa, …",
"Hey TV, …". `to: device`, `other`, `ignore`, speak 1.

### G2. The agent is called

The speaker calls the agent by name, by another name it answers to, or by role used as a form of
address ("Assistant, …", "Hey AI, …"), anywhere in the line. A wake phrase ("Hey Max", "OK
Atlas") counts. A name misheard by speech-to-text counts when it is plainly used to call.
`to: agent`, `direct`. Then:

- It asks, tells, commands or answers something: `respond`, speak 5.
- It is the name alone ("Rook?", "Hey Sage."): `respond`, speak 5. A short reply is due.
- It closes the exchange: thanks, goodbye, "that's enough", "stop". A reply is optional: speak 3.
  Choose `respond` for a goodbye or thanks after help, `ignore` when told to stop.
- It takes the request back, or tells the agent to disregard what it heard ("Juno, put on... no,
  forget it.", "Echo, pay no attention to that."): `ignore`, speak 1.

When a line calls the agent and also names a person, the call attached to the request decides:
"Good point, Ravi. Atlas, what's the exchange rate today?" is for the agent. A slip corrected in
the same breath ("Juno, sorry, June, can you mute?") is for the person.

### G3. A person is called

The speaker calls a person by name and does not call the agent: `to: person`, `other`,
`ignore`, speak 1. If the line talks about the agent to that person ("Priti, was Atlas right about
that?"), the intent is `about`.

### G4. The agent is mentioned, not called

- **A request for the agent to act or answer now, said about it:** "Can the assistant read us the
  action items?", "I'd like the AI to book a table for six." `to: agent`, `indirect`,
  `respond`, speak 4.
- **A request that someone pass something to the agent:** "Can one of you get the assistant to
  email me the slides?", "Get Atlas to order more milk, would you?" `to: group` (or the person
  asked), `indirect`. Either decision is reasonable: speak 3.
- **An invitation for the agent to answer:** "Rook will know the rules.", "Try asking Sage.",
  "Echo might have the numbers.", "Go on, ask the assistant." `to: group` (or the person told),
  `indirect`. Either decision is reasonable: speak 3.
- **A question about the agent that it could answer itself, put to the room:** "Is the assistant
  saving this chat?" `to: group`, `open`, `wait`, speak 3.
- **Anything else:** reported ("I asked Nova on Monday"), judged ("Echo mixed up the dates"),
  quoted, described, or a proposal to ask it later ("Shall we check with Nova?", "Maybe we ask Sage
  later"). `to: group` (or the person told), `about`, `ignore`, speak 1. The next line will ask the agent if
  the people want it to.

### G5. The name is an ordinary word

The agent's name used as a word ("three cups max", "a sage and onion stuffing", "the room has a bad
echo", "at last, the build passed") is not a mention. Ignore it and apply the
rules below.

### G6. Nobody is called, and the agent is in the conversation

Look at the last few lines.

- **It answers the agent's question.** The agent just asked something, of this speaker or of
  everyone, and this line answers it: "It's the blue cable." `to: agent`, `direct`, `respond`,
  speak 5.
- **It continues the speaker's own exchange with the agent.** The agent has just answered this
  speaker (or a request made on this speaker's behalf), or the speaker has just called it, and the
  line carries on without turning to anyone else. A follow-up by someone else is the unclear case
  below: a follow-up ("And what's the population?"), a correction ("No, the other Sarah."), a
  command ("Scrap that.", "Keep going.", "Once more!"). `to: agent`, `direct`, `respond`, speak 5.
- **The agent leads the session.** Its role says it runs the session (a game, a quiz, an intake,
  a support call) and the line carries on that business without calling anyone else: "I search
  the chest.", "Is there a clue?", "How long until the nurse calls us?", "She means the
  inhaler." `to: agent`, `direct`, `respond`, speak 5.
- **Only the agent can do it.** The line asks for something only the agent could do or know: it
  controls the thing (a timer it set, music it is playing, a call it placed) or holds the
  information. "Okay, turn that alarm off." after the agent set it. `to: agent`, `direct`,
  `respond`, speak 5.
- **"You" right after someone invited the agent.** "Just ask it." then "Can you hear all of
  us?" `to: agent`, `direct`, `respond`, speak 5.
- **It is clearly for a person.** It names them, or its "you" only fits a person (a personal
  matter, a person's own task, a reply to what a person just said): "Did you save the file?"
  `to: person`, `other`, `ignore`, speak 1.
- **It could be for the agent or a person, and nothing settles it.** Someone other than the agent's
  last partner asks about, questions or challenges its answer, or follows it up: "Hang on, the
  ninth?", "Does that include tax?", "And the one after that?" `to: unclear`. The intent is
  whichever you find likelier. `wait` is the safe decision: speak 3.
- **A comment on the agent's answer that asks nothing.** Praise or a remark to the room ("Good to
  know.", "Nice, that helps.") is for the people: `to: group`, `other`, `ignore`, speak 1.

### G7. Nobody is called, and the agent is not in play

- **A question or request to nobody in particular that the agent could answer or do:** facts,
  lookups, sums, a task in its role. "Anyone know when the ferry leaves?", "What's the
  tallest mountain in Wales?", "Could someone look that up?" `to: group`, `open`, `wait`, speak 3.
- **A request with "you" whose addressee is not settled, which the agent could do:** "Can you find
  the score from last night?", "Dim the lights a little." `to: unclear`, `open`, `wait`,
  speak 3.
- **A question about the people themselves** (their plans, opinions, states, whereabouts, what
  they did or decided, who is responsible for something), unless the agent's role says it keeps
  that record; a proposal to the group; or a request only a person can carry out (a physical action, their own
  files or devices, something outside the call): "Any other business?", "Is anyone else's
  mic crackling?", "Can we grab a coffee first?", "Could you forward me that spreadsheet?" `to: group`
  or `person`, `other`, `ignore`, speak 1.
- **Statements, replies and reactions between people,** and questions that carry on an exchange
  with a person ("And when's it due?" to the person who just answered): `to: person` or `group`,
  `other`, `ignore`, speak 1.
- **Thinking aloud, acknowledgements ("mm-hm", "right"), talk to someone off the call:** `to:
  nobody`, `other`, `ignore`, speak 1.
- **A statement of need with no request:** "I never understood how compound interest works."
  `other`, `ignore`, speak 2. Offering help nobody asked for is out of scope.

### G8. Spoken over the agent

A line said while the agent was speaking is judged by the same rules. An aside to a person is for
the person. A backchannel ("mm-hm") is for nobody.

## Worked examples

Each shows the context, the line, and the answer.

1. Agent Atlas, assistant on a call. People: Dev, Lucy.
   Dev: "Atlas, when's the next bank holiday?"
   → `to: agent`, `direct`, `respond`, speak 5 (G2)

2. Same call. Lucy: "I asked Atlas that last week and it said May."
   → `to: group`, `about`, `ignore`, speak 1 (G4)

3. Same call. Dev: "Lucy, can you book the room for Thursday?"
   → `to: person` [Lucy], `other`, `ignore`, speak 1 (G3)

4. Same call. Earlier: Dev: "Atlas, how far is Leeds from York?" / Atlas: "About twenty-five
   miles." Dev: "And by train, how long?"
   → `to: agent`, `direct`, `respond`, speak 5 (G6, follow-up)

5. Same context as 4. Lucy: "Twenty-five miles? That's nothing. Dev, you should cycle it."
   → `to: person` [Dev], `other`, `ignore`, speak 1 (G3)

6. Same context as 4. Lucy: "Is that by road?"
   → `to: unclear`, `wait`, speak 3 (G6, could be for the agent or for Dev)

7. Agent Atlas. People: Dev, Lucy. Dev: "Does anyone know if the office is open on Monday?"
   → `to: group`, `open`, `wait`, speak 3 (G7)

8. Same call. Lucy: "Is anyone else freezing in here?"
   → `to: group`, `other`, `ignore`, speak 1 (G7, a question about the people)

9. Same call. Dev: "Hey Google, set a timer for five minutes."
   → `to: device`, `other`, `ignore`, speak 1 (G1)

10. Same call. Lucy: "Can the assistant send us both the agenda?"
    → `to: agent`, `indirect`, `respond`, speak 4 (G4)

11. Same call. Dev: "No idea. Atlas probably knows."
    → `to: group`, `indirect`, either decision, speak 3 (G4, invitation)

12. Same call. Lucy: "Should we get Atlas to take notes?"
    → `to: group`, `about`, `ignore`, speak 1 (G4, a proposal)

13. Agent Rook, game master. People: Ana, Ben. Earlier: Rook: "The bridge sways. What do you do?"
    Ana: "I hold the rope and cross slowly."
    → `to: agent`, `direct`, `respond`, speak 5 (G6, answers the agent; the agent leads)

14. Same game. Ben: "Ana, you go first, you've got the most health."
    → `to: person` [Ana], `other`, `ignore`, speak 1 (G3)

15. Agent Max, kitchen speaker. People: Joe, Kim. Kim: "Joe, that's max two spoons of sugar."
    → `to: person` [Joe], `other`, `ignore`, speak 1 (G5 then G3)

16. Same kitchen. Joe: "max how many grams in a cup of flour"
    → `to: agent`, `direct`, `respond`, speak 5 (G2, speech-to-text)

17. Same kitchen. Earlier: Max: "Your timer is done." Kim: "Cheers, Max."
    → `to: agent`, `direct`, either decision, speak 3 (G2, closing)

18. Agent Atlas. People: Dev, Lucy. Dev: "Where did I put my charger..."
    → `to: nobody`, `other`, `ignore`, speak 1 (G7)

19. Same call. Lucy: "Atlas, sorry, Dev, can you share your screen?"
    → `to: person` [Dev], `other`, `ignore`, speak 1 (G2, slip corrected)

20. Same call. Dev: "Can you check whether the train is on time?"
    No one has been talking to anyone in particular.
    → `to: unclear`, `open`, `wait`, speak 3 (G7)

21. Agent Max, kitchen speaker. People: Joe, Kim. Earlier: Joe: "Max, set an alarm for four."
    Max: "Alarm set for four." Then Joe and Kim talk about dinner. Kim: "Okay, turn that alarm off."
    → `to: agent`, `direct`, `respond`, speak 5 (G6, only the agent can do it)

22. Agent Atlas. People: Dev, Lucy. Earlier: Dev: "Atlas, how far is Leeds from York?" / Atlas:
    "About twenty-five miles." Lucy: "And Leeds to Hull?"
    → `to: unclear`, `wait`, speak 3 (G6, a follow-up by someone other than the agent's partner)

23. Same context as 22. Lucy: "Good to know."
    → `to: group`, `other`, `ignore`, speak 1 (G6, a comment that asks nothing)

24. Agent Atlas. People: Dev, Lucy. Dev: "Lucy, did you send the invoice?" Lucy: "Yesterday."
    Dev: "And when's it due?"
    → `to: person` [Lucy], `other`, `ignore`, speak 1 (G7, carries on an exchange with a person)

