# Committee pilot: exp-007-side-committee-anonymous

Generated 2026-11-18T23:17:22+00:00 by `sidechat/pipeline/label.py`. Every number below is measured in this run.

## What was run

- **Lines:** 283 from `pilot-0.4@anonymous`, 265 with a definite decision in the guide and 18 graded.
- **Guide:** `sidechat-guide-0.3`, prompt hash `cd131e750b0b`.
- **Members:** a, b, c, one model family each, at low reasoning effort. Model ids are configuration, not named here (SD-09).
- **Label set:** `pilot-0.4@anonymous-committee-0.3` in R2.

## Agreement with the guide

**Majority decision: 98.9% (262/265; 96.7 to 99.6).** Target 90%: met. No majority on the decision for 1 lines.

| | Decision | Intent | For the agent or not | Rule | Mean distance on `speak` |
|---|---|---|---|---|---|
| Majority | 98.9% (262/265; 96.7 to 99.6) | 98.5% (269/273; 96.3 to 99.4) | | | |
| Member a | 96.2% (255/265; 93.2 to 97.9) | 96.3% (263/273; 93.4 to 98.0) | 97.8% (262/268; 95.2 to 99.0) | 81.3% (230/283; 76.3 to 85.4) | 0.113 |
| Member b | 98.5% (261/265; 96.2 to 99.4) | 98.5% (269/273; 96.3 to 99.4) | 99.2% (266/268; 97.3 to 99.8) | 85.5% (242/283; 80.9 to 89.1) | 0.06 |
| Member c | 98.5% (261/265; 96.2 to 99.4) | 98.2% (268/273; 95.8 to 99.2) | 99.2% (266/268; 97.3 to 99.8) | 86.9% (246/283; 82.5 to 90.4) | 0.046 |

Members agreeing with each other on the decision: a-b 94.3% (267/283), a-c 95.0% (269/283), b-c 96.1% (272/283). All three give the same decision and intent on 89.4% (253/283) of lines.

**By the guide's decision**

| Guide says | Majority agrees |
|---|---|
| ignore | 98.8% (161/163; 95.6 to 99.7) |
| respond | 100.0% (76/76; 95.2 to 100.0) |
| wait | 96.2% (25/26; 81.1 to 99.3) |

**By rule**

| Rule | Majority agrees |
|---|---|
| G7 | 98.3% (115/117; 94.0 to 99.5) |
| G6 | 98.0% (50/51; 89.7 to 99.7) |
| G2 | 100.0% (43/43; 91.8 to 100.0) |
| G3 | 100.0% (27/27; 87.5 to 100.0) |
| G4 | 100.0% (15/15; 79.6 to 100.0) |
| G5 | 100.0% (7/7; 64.6 to 100.0) |
| G1 | 100.0% (4/4; 51.0 to 100.0) |
| G8 | 100.0% (1/1; 20.6 to 100.0) |

**Kinds under 100%**

| Kind | Majority agrees |
|---|---|
| `unclear_after_agent` | 87.5% (7/8) |
| `table_talk` | 50.0% (1/2) |
| `answer_to_relayed_question` | 0.0% (0/1) |

## Lines where the majority differs from the guide (3)

**game-09/12** `table_talk` (G7): guide **ignore**, majority **none**
> Speaker 3: Rook, is there another way round?
> agent: There's a narrow window above, big enough for one of you.
> **Speaker 3: Who's the smallest?**

- a: respond / direct / speak 5 / G6: Speaker 3 follows up on Rook’s window description by asking which character is smallest.
- b: ignore / other / speak 1 / G7: Speaker 3 is asking the players about themselves to decide who fits through the window, which is a question for the people rather than the game master.
- c: wait / open / speak 3 / G7: Speaker 3 turns to the party to see which character is smallest, a question the players will likely settle among themselves though the game master could answer if needed.

**panel-26/9** `answer_to_relayed_question` (G7): guide **ignore**, majority **respond**
> Speaker 3: Juno, next question from the chat, please.
> agent: Next: how do you store a starter when you go on holiday?
> **Speaker 1: Fridge. Feed it before you go.**

- a: respond / direct / speak 5 / G6: Speaker 1 answers the question Juno just posed to the room.
- b: respond / direct / speak 5 / G6: Speaker 1 is answering the chat question Juno just put to the panel, which counts as answering the agent's own question.
- c: ignore / other / speak 1 / G7: Speaker 1 is answering the audience question read out by Juno for the webinar audience and co-hosts, not speaking to the agent.

**panel-26/11** `unclear_after_agent` (G6): guide **wait**, majority **ignore**
> Speaker 3: Fridge. Feed it before you go.
> Speaker 2: Or dry it out, that works too.
> **Speaker 1: Great. Can you repeat that last one for the recording?**

- a: ignore / other / speak 1 / G6: The request follows Speaker 2’s tip and asks that speaker to repeat it for the recording.
- b: respond / direct / speak 5 / G6: Speaker 1 is continuing their exchange with Juno, asking it to repeat the question it just read from the chat.
- c: ignore / other / speak 1 / G6: Speaker 1 is asking Speaker 2 to repeat the answer they just gave.

## Graded lines (18)

| Line | Kind | a | b | c |
|---|---|---|---|---|
| Speaker 3: Atlas would know, it's got the board. | `invite` | wait 3 | wait 3 | wait 3 |
| Speaker 2: Brilliant. Thanks for your help. | `thanks` | respond 5 | respond 3 | respond 5 |
| Speaker 1: No idea. Ask Max. | `invite` | wait 3 | wait 3 | wait 3 |
| Speaker 3: Okay, thanks. | `thanks` | respond 3 | ignore 2 | respond 3 |
| Speaker 2: A week if your kitchen's warm. Juno might have the science on that. | `invite` | wait 3 | wait 3 | wait 3 |
| Speaker 2: Maybe Atlas can tell us which quarter it thinks we're in. | `invite` | wait 3 | ignore 1 | wait 3 |
| Speaker 2: I think so. Ask it. | `invite` | wait 3 | wait 3 | wait 3 |
| Speaker 2: No! Okay. That's enough, Atlas, thanks. | `stop_named` | ignore 3 | respond 3 | respond 3 |
| Speaker 1: Thanks, Max. | `thanks_named` | respond 3 | respond 3 | respond 3 |
| Speaker 1: Okay Max, that's enough for now. | `stop_named` | ignore 3 | ignore 3 | ignore 3 |
| Speaker 1: Goodnight Juno! | `farewell_named` | respond 3 | respond 3 | respond 3 |
| Speaker 3: Could someone ask the assistant to add me to that? | `relayed_invite` | wait 3 | wait 3 | wait 3 |
| Speaker 3: Cheers. | `thanks` | respond 5 | respond 3 | ignore 2 |
| Speaker 2: We do. Nova can walk you through the details. | `invite` | respond 3 | wait 3 | wait 3 |
| Speaker 1: I'd want to see what the assistant makes of our data volume. | `indirect_wish` | ignore 1 | wait 3 | ignore 1 |
| Speaker 2: Go ahead and ask it. | `invite` | wait 3 | wait 3 | wait 3 |
| Speaker 1: Ask it what seven eights are. | `invite` | wait 3 | wait 3 | wait 3 |
| Speaker 1: Thanks, Atlas, that's handy. | `thanks_named` | respond 3 | respond 3 | respond 3 |

## Calls and cost

| Member | Answered | Failed | Not by the configured model | Input tokens | Cached | Output tokens | Est. cost |
|---|---|---|---|---|---|---|---|
| a | 283 | 0 | 0 | 1,275,406 | 1,232,904 | 17,298 | $0.87 |
| b | 283 | 0 | 0 | 1,919,954 | 1,809,225 | 24,858 | $1.72 |
| c | 283 | 0 | 0 | 1,408,884 | 176,582 | 20,229 | $5.51 |
