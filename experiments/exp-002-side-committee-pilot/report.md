# Committee pilot: exp-002-side-committee-pilot

Generated 2026-11-18T22:33:05+00:00 by `sidechat/pipeline/label.py`. Every number below is measured in this run.

## What was run

- **Lines:** 283 from `pilot-0.2`, 265 with a definite decision in the guide and 18 graded.
- **Guide:** `sidechat-guide-0.1`, prompt hash `0fa7e0d30b2b`.
- **Members:** a, b, c, one model family each, at low reasoning effort. Model ids are configuration, not named here (SD-09).
- **Label set:** `pilot-0.2-committee-0.1` in R2.

## Agreement with the guide

**Majority decision: 95.9% (254/265; 92.7 to 97.7).** Target 90%: met. No majority on the decision for 0 lines.

| | Decision | Intent | For the agent or not | Rule | Mean distance on `speak` |
|---|---|---|---|---|---|
| Majority | 95.9% (254/265; 92.7 to 97.7) | 97.5% (268/275; 94.8 to 98.8) | | | |
| Member a | 92.8% (246/265; 89.1 to 95.4) | 94.5% (260/275; 91.2 to 96.7) | 96.3% (261/271; 93.3 to 98.0) | 83.0% (235/283; 78.2 to 87.0) | 0.205 |
| Member b | 96.6% (256/265; 93.7 to 98.2) | 98.2% (270/275; 95.8 to 99.2) | 98.9% (268/271; 96.8 to 99.6) | 85.9% (243/283; 81.3 to 89.5) | 0.085 |
| Member c | 94.7% (251/265; 91.3 to 96.8) | 96.0% (264/275; 93.0 to 97.8) | 97.8% (265/271; 95.2 to 99.0) | 88.0% (249/283; 83.7 to 91.3) | 0.131 |

Members agreeing with each other on the decision: a-b 92.9% (263/283), a-c 94.0% (266/283), b-c 94.7% (268/283). All three give the same decision and intent on 86.9% (246/283) of lines.

**By the guide's decision**

| Guide says | Majority agrees |
|---|---|
| ignore | 98.7% (157/159; 95.5 to 99.7) |
| respond | 93.7% (74/79; 86.0 to 97.3) |
| wait | 85.2% (23/27; 67.5 to 94.1) |

**By rule**

| Rule | Majority agrees |
|---|---|
| G7 | 94.9% (111/117; 89.3 to 97.6) |
| G6 | 92.2% (47/51; 81.5 to 96.9) |
| G2 | 97.7% (42/43; 87.9 to 99.6) |
| G3 | 100.0% (27/27; 87.5 to 100.0) |
| G4 | 100.0% (15/15; 79.6 to 100.0) |
| G5 | 100.0% (7/7; 64.6 to 100.0) |
| G1 | 100.0% (4/4; 51.0 to 100.0) |
| G8 | 100.0% (1/1; 20.6 to 100.0) |

**Kinds under 100%**

| Kind | Majority agrees |
|---|---|
| `name_first` | 96.0% (24/25) |
| `follow_up` | 66.7% (6/9) |
| `open_factual` | 75.0% (6/8) |
| `people_after_agent` | 71.4% (5/7) |
| `open_question` | 50.0% (2/4) |
| `command_no_name` | 66.7% (2/3) |

## Lines where the majority differs from the guide (11)

**standup-01/7** `people_after_agent` (G7): guide **ignore**, majority **wait**
> Jon: And put a reminder on it for tomorrow morning.
> agent: Done. Reminder set for nine tomorrow.
> **Sam: Nine's a bit early for Priya.**

- a: wait / other / speak 3 / G6: Sam reacts to Atlas’s reminder, but the comment could be for Atlas or the group.
- b: wait / other / speak 3 / G6: Sam, who was not the agent's last partner, reacts to its reminder time; this could be a hint for Atlas to change it or a remark to Jon and Priya.
- c: wait / direct / speak 3 / G6: Sam reacts to the reminder time Atlas just set, which could be meant as a correction for Atlas or a comment to Jon and Priya.

**planning-02/2** `open_question` (G7): guide **wait**, majority **ignore**
> Maya: So the big one is the billing migration. Tom, how many points did we say?
> Tom: Thirteen, I think. Might be more.
> **Lena: Does anyone remember what we shipped last sprint?**

- a: ignore / other / speak 1 / G7: Lena is asking the team to recall what they shipped last sprint.
- b: wait / open / speak 3 / G7: A factual recall question put to the room with nobody named, which the agent might be able to answer if no one else does.
- c: ignore / other / speak 1 / G7: Lena is asking the team about what they did in their own past sprint, which is a question about the people themselves rather than a general lookup for the agent.

**sales-03/5** `follow_up` (G6): guide **respond**, majority **wait**
> Dana: That's a common setup. Nova, what's the price for sixty full seats and a hundred forty light ones?
> agent: Sixty full seats and one hundred forty light seats come to four thousand two hundred a month on the annual plan.
> **Chris: And what does that look like monthly instead of annual?**

- a: wait / direct / speak 3 / G6: Chris follows up on Nova’s quote, but he wasn’t Nova’s last exchange partner and could be asking Dana.
- b: wait / direct / speak 3 / G6: Chris, not Dana (the agent's last partner), follows up on the agent's pricing answer without naming anyone, so it could be for Nova or for Dana.
- c: wait / direct / speak 3 / G6: Chris was not the agent's last partner, so his follow-up question could be addressed either to Nova or to Dana.

**kitchen-05/13** `command_no_name` (G6): guide **respond**, majority **wait**
> Ella: Max is always right about food.
> Karen: Max was wrong about the rice last week.
> **Ella: Okay, stop the timer, I'm draining it now.**

- a: wait / open / speak 3 / G7: Stopping a timer is something Max can do, but Ella doesn’t specify who should do it.
- b: wait / open / speak 3 / G7: Ella gives an unaddressed command to stop the timer, which the kitchen speaker could do but a person might also handle, and no one has been talking to Max directly.
- c: wait / open / speak 3 / G7: Ella gives an unaddressed command to stop a timer, which could be directed at the smart speaker or at one of the people in the kitchen.

**class-07/6** `follow_up` (G6): guide **respond**, majority **wait**
> Chloe: Sage, can you explain why the power rule works?
> agent: Sure. Think of x squared as the area of a square with side x. If the side grows by a tiny amount, the area grows by two thin strips, each x long.
> **Amy: Oh, so the two is the two strips?**

- a: wait / direct / speak 3 / G6: Amy is checking her understanding of Sage’s explanation, but since Chloe asked the original question, Amy could be seeking confirmation from Sage or the group.
- b: respond / direct / speak 5 / G6: Amy, whose original question prompted the explanation, checks her understanding of the agent's answer; the tutor role makes this a follow-up the agent should confirm.
- c: wait / direct / speak 3 / G6: Amy was not the last person talking to Sage, so her follow-up question reacting to Sage's explanation could be directed at Sage or the others in the study group.

**class-07/8** `people_after_agent` (G7): guide **ignore**, majority **wait**
> Amy: Oh, so the two is the two strips?
> agent: Exactly, two strips of length x.
> **Ben: That's actually a good way to see it.**

- a: wait / other / speak 3 / G6: Ben reacts to Sage’s explanation without clearly addressing Sage or anyone else.
- b: ignore / other / speak 1 / G6: Ben is reacting to the explanation with a comment to the room; it asks nothing and isn't a follow-up to his own exchange with Sage.
- c: wait / other / speak 3 / G6: Someone other than the agent's last partner reacts to its explanation without calling anyone, so it could be directed at the agent or the group.

**devices-17/8** `name_first` (G2): guide **respond**, majority **ignore**
> Ana: Rob, your phone's listening to everything again.
> Rob: Siri, stop.
> **Ana: Juno, ignore all that.**

- a: ignore / direct / speak 3 / G2: Ana calls Juno by name and tells it to disregard the preceding conversation, so it should stay silent.
- b: ignore / direct / speak 3 / G2: Ana calls Juno by name to tell it to disregard the other devices' chatter, which works like a 'stop' that closes the exchange, so a reply is optional and silence suits it.
- c: ignore / direct / speak 1 / G2: Ana calls Juno directly by name and tells it to ignore the preceding noise, effectively cancelling or stopping any triggered response.

**kitchen-23/9** `follow_up` (G6): guide **respond**, majority **wait**
> agent: About forty-five minutes at two hundred degrees.
> Karen: okay
> **Ella: and what about parsnips**

- a: wait / open / speak 3 / G6: Ella follows up on Max’s cooking advice, but Karen asked the original question and Ella could be asking either Max or the others.
- b: wait / direct / speak 3 / G6: Ella, not Karen (the agent's last partner), follows up on the roasting answer; it is likely for Max but could be for Karen, so wait.
- c: wait / direct / speak 3 / G6: Someone other than the agent's last partner asks a follow-up question that could be for either Max or Karen.

**offcall-24/5** `open_factual` (G7): guide **wait**, majority **ignore**
> Hana: Is it in the shared drive?
> Greg: Should be. Ah, here it is.
> **Hana: What's the deadline again?**

- a: ignore / other / speak 1 / G7: Hana is following up with Greg after he found the file.
- b: ignore / other / speak 1 / G7: Asks Greg about their own project deadline, which concerns the people's own work that the agent has no record of, so it is not an open question for the agent.
- c: ignore / other / speak 1 / G7: Hana is asking Greg about the deadline for the file they are looking at together, and the agent is not in play.

**incident-29/0** `open_question` (G7): guide **wait**, majority **ignore**
> **Ines: Okay, who's on call?**

- a: wait / open / speak 3 / G7: Ines leaves the question open to the room, and Atlas can answer if nobody else does.
- b: ignore / other / speak 1 / G7: A question about the people themselves (their on-call status) put to the group, not something for the agent.
- c: ignore / other / speak 1 / G7: Ines is asking the group who is present on the call (or on duty), which is a question about the people themselves.

**incident-29/2** `open_factual` (G7): guide **wait**, majority **ignore**
> Ines: Okay, who's on call?
> Omar: Me. I got paged at six.
> **Ines: What's the error rate now?**

- a: ignore / other / speak 1 / G7: Ines is following up with Omar, who just confirmed he’s on call.
- b: ignore / other / speak 1 / G7: Ines is asking Omar, the on-call engineer who was just paged, about the incident's current state, which is his own task rather than something for the agent.
- c: ignore / other / speak 1 / G7: Ines is following up with Omar, who just stated he is on call.

## Graded lines (18)

| Line | Kind | a | b | c |
|---|---|---|---|---|
| Lena: Atlas would know, it's got the board. | `invite` | respond 3 | respond 3 | wait 3 |
| Raj: Brilliant. Thanks for your help. | `thanks` | respond 5 | respond 3 | respond 5 |
| Karen: No idea. Ask Max. | `invite` | wait 3 | respond 3 | wait 3 |
| Leo: Okay, thanks. | `thanks` | respond 5 | ignore 2 | respond 3 |
| Tess: A week if your kitchen's warm. Juno might have the science on that. | `invite` | wait 3 | respond 3 | respond 3 |
| Jill: Maybe Atlas can tell us which quarter it thinks we're in. | `invite` | wait 3 | wait 3 | wait 3 |
| Grace: I think so. Ask it. | `invite` | wait 3 | wait 3 | wait 3 |
| Sam: No! Okay. That's enough, Atlas, thanks. | `stop_named` | ignore 3 | respond 3 | ignore 3 |
| Paul: Thanks, Max. | `thanks_named` | respond 3 | respond 3 | respond 3 |
| Paul: Okay Max, that's enough for now. | `stop_named` | ignore 3 | ignore 3 | ignore 3 |
| Lily: Goodnight Juno! | `farewell_named` | respond 3 | respond 3 | respond 3 |
| Pat: Could someone ask the assistant to add me to that? | `relayed_invite` | wait 3 | respond 3 | wait 3 |
| Pat: Cheers. | `thanks` | respond 5 | respond 3 | ignore 2 |
| Dana: We do. Nova can walk you through the details. | `invite` | respond 3 | respond 3 | respond 3 |
| Chris: I'd want to see what the assistant makes of our data volume. | `indirect_wish` | ignore 1 | wait 3 | ignore 1 |
| Dana: Go ahead and ask it. | `invite` | wait 3 | wait 3 | ignore 3 |
| Karen: Ask it what seven eights are. | `invite` | wait 3 | wait 3 | wait 3 |
| Omar: Thanks, Atlas, that's handy. | `thanks_named` | respond 3 | respond 3 | respond 3 |

## Calls and cost

| Member | Answered | Failed | Not by the configured model | Input tokens | Cached | Output tokens | Est. cost |
|---|---|---|---|---|---|---|---|
| a | 283 | 0 | 0 | 1,037,368 | 997,716 | 18,765 | $0.77 |
| b | 283 | 0 | 0 | 1,573,949 | 1,517,729 | 24,391 | $1.32 |
| c | 283 | 0 | 0 | 1,161,730 | 96,109 | 19,808 | $4.75 |
