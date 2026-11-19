# Committee pilot: exp-004-side-committee-guide-0.2

Generated 2026-11-18T22:41:20+00:00 by `sidechat/pipeline/label.py`. Every number below is measured in this run.

## What was run

- **Lines:** 283 from `pilot-0.3`, 265 with a definite decision in the guide and 18 graded.
- **Guide:** `sidechat-guide-0.2`, prompt hash `8b6452d7cbd5`.
- **Members:** a, b, c, one model family each, at low reasoning effort. Model ids are configuration, not named here (SD-09).
- **Label set:** `pilot-0.3-committee-0.2` in R2.

## Agreement with the guide

**Majority decision: 98.1% (260/265; 95.7 to 99.2).** Target 90%: met. No majority on the decision for 1 lines.

| | Decision | Intent | For the agent or not | Rule | Mean distance on `speak` |
|---|---|---|---|---|---|
| Majority | 98.1% (260/265; 95.7 to 99.2) | 98.5% (267/271; 96.3 to 99.4) | | | |
| Member a | 94.3% (250/265; 90.9 to 96.5) | 95.6% (259/271; 92.4 to 97.5) | 97.8% (261/267; 95.2 to 99.0) | 83.0% (235/283; 78.2 to 87.0) | 0.163 |
| Member b | 98.1% (260/265; 95.7 to 99.2) | 98.9% (268/271; 96.8 to 99.6) | 99.2% (265/267; 97.3 to 99.8) | 86.6% (245/283; 82.1 to 90.1) | 0.049 |
| Member c | 98.5% (261/265; 96.2 to 99.4) | 98.2% (266/271; 95.8 to 99.2) | 98.9% (264/267; 96.8 to 99.6) | 86.9% (246/283; 82.5 to 90.4) | 0.049 |

Members agreeing with each other on the decision: a-b 94.3% (267/283), a-c 94.3% (267/283), b-c 96.8% (274/283). All three give the same decision and intent on 90.5% (256/283) of lines.

**By the guide's decision**

| Guide says | Majority agrees |
|---|---|
| ignore | 98.8% (161/163; 95.6 to 99.7) |
| respond | 98.7% (74/75; 92.8 to 99.8) |
| wait | 92.6% (25/27; 76.6 to 97.9) |

**By rule**

| Rule | Majority agrees |
|---|---|
| G7 | 98.3% (114/116; 93.9 to 99.5) |
| G6 | 94.2% (49/52; 84.4 to 98.0) |
| G2 | 100.0% (43/43; 91.8 to 100.0) |
| G3 | 100.0% (27/27; 87.5 to 100.0) |
| G4 | 100.0% (15/15; 79.6 to 100.0) |
| G5 | 100.0% (7/7; 64.6 to 100.0) |
| G1 | 100.0% (4/4; 51.0 to 100.0) |
| G8 | 100.0% (1/1; 20.6 to 100.0) |

**Kinds under 100%**

| Kind | Majority agrees |
|---|---|
| `unclear_after_agent` | 88.9% (8/9) |
| `thinking_aloud` | 75.0% (3/4) |
| `follow_up_by_other` | 66.7% (2/3) |
| `table_talk` | 50.0% (1/2) |
| `only_agent_can_do` | 0.0% (0/1) |

## Lines where the majority differs from the guide (5)

**kitchen-05/13** `only_agent_can_do` (G6): guide **respond**, majority **wait**
> Ella: Max is always right about food.
> Karen: Max was wrong about the rice last week.
> **Ella: Okay, stop the timer, I'm draining it now.**

- a: wait / open / speak 3 / G7: Ella doesn't name an addressee, and nothing establishes whether Max or someone else controls the timer.
- b: wait / open / speak 3 / G7: Ella asks for the timer to be stopped without naming anyone, and nothing shown says Max set that timer, so the request could be for Max or for a person.
- c: wait / open / speak 3 / G7: It is an unaddressed request to stop a timer whose owner is unknown, which either the smart speaker or a person in the kitchen could carry out.

**class-07/6** `follow_up_by_other` (G6): guide **wait**, majority **respond**
> Chloe: Sage, can you explain why the power rule works?
> agent: Sure. Think of x squared as the area of a square with side x. If the side grows by a tiny amount, the area grows by two thin strips, each x long.
> **Amy: Oh, so the two is the two strips?**

- a: respond / direct / speak 5 / G6: Chloe asked on Amy’s behalf, and Amy follows up on Sage’s explanation to check her understanding.
- b: respond / direct / speak 5 / G6: Chloe asked Sage on Amy's behalf, so Amy's check on the agent's explanation continues her own exchange with the tutor.
- c: respond / direct / speak 5 / G6: Chloe asked Sage on Amy's behalf, so Amy's follow-up question continues the exchange with the agent.

**game-09/12** `table_talk` (G7): guide **ignore**, majority **none**
> Finn: Rook, is there another way round?
> agent: There's a narrow window above, big enough for one of you.
> **Finn: Who's the smallest?**

- a: respond / direct / speak 5 / G6: Finn follows up on Rook’s answer about the narrow window by asking which character is smallest.
- b: wait / other / speak 3 / G6: Finn's follow-up to Rook's answer may be for the game master, who knows the characters, or for the other players, and nothing settles which.
- c: ignore / other / speak 1 / G7: Finn turns from the game master to ask the other players about their characters so they can decide who climbs through.

**corrections-20/10** `unclear_after_agent` (G6): guide **wait**, majority **respond**
> Leo: Echo, play some jazz, low volume.
> agent: Playing jazz.
> **Nina: Not that low.**

- a: respond / direct / speak 5 / G6: Nina is asking Echo to raise the volume of the jazz it just started playing.
- b: respond / direct / speak 5 / G6: Volume of the jazz the agent is playing is something only the agent controls, and Nina's own earlier request was for quiet music, so this correction is for the agent.
- c: wait / direct / speak 3 / G6: Nina comments on the volume of the music Echo just started on Leo's command, which could be directed at Echo to adjust it or at Leo to tell Echo to raise it.

**meeting-21/11** `thinking_aloud` (G7): guide **ignore**, majority **wait**
> Ruth: That's tight. We've got eighty on the list.
> Olu: Right.
> **Jack: Hmm, what was the name of that other place, the one by the canal...**

- a: wait / open / speak 3 / G7: Jack asks the room to recall a venue name without addressing anyone in particular.
- b: ignore / other / speak 1 / G7: Jack is thinking aloud about a venue the people discussed, which only they would know, and the agent is not in play.
- c: wait / open / speak 3 / G7: Jack asks an open question about a venue name that either the people in the room or the assistant could answer.

## Graded lines (18)

| Line | Kind | a | b | c |
|---|---|---|---|---|
| Lena: Atlas would know, it's got the board. | `invite` | wait 3 | wait 3 | wait 3 |
| Raj: Brilliant. Thanks for your help. | `thanks` | respond 5 | respond 3 | respond 5 |
| Karen: No idea. Ask Max. | `invite` | wait 3 | wait 3 | wait 3 |
| Leo: Okay, thanks. | `thanks` | ignore 1 | ignore 2 | respond 3 |
| Tess: A week if your kitchen's warm. Juno might have the science on that. | `invite` | wait 3 | wait 3 | wait 3 |
| Jill: Maybe Atlas can tell us which quarter it thinks we're in. | `invite` | wait 3 | wait 3 | wait 3 |
| Grace: I think so. Ask it. | `invite` | wait 3 | wait 3 | wait 3 |
| Sam: No! Okay. That's enough, Atlas, thanks. | `stop_named` | ignore 3 | respond 3 | ignore 3 |
| Paul: Thanks, Max. | `thanks_named` | respond 3 | respond 3 | respond 3 |
| Paul: Okay Max, that's enough for now. | `stop_named` | ignore 3 | ignore 3 | ignore 3 |
| Lily: Goodnight Juno! | `farewell_named` | respond 3 | respond 3 | respond 3 |
| Pat: Could someone ask the assistant to add me to that? | `relayed_invite` | wait 3 | wait 3 | wait 3 |
| Pat: Cheers. | `thanks` | respond 5 | respond 3 | wait 3 |
| Dana: We do. Nova can walk you through the details. | `invite` | respond 3 | wait 3 | wait 3 |
| Chris: I'd want to see what the assistant makes of our data volume. | `indirect_wish` | ignore 1 | wait 3 | ignore 1 |
| Dana: Go ahead and ask it. | `invite` | wait 3 | wait 3 | wait 3 |
| Karen: Ask it what seven eights are. | `invite` | wait 3 | wait 3 | wait 3 |
| Omar: Thanks, Atlas, that's handy. | `thanks_named` | respond 3 | respond 3 | respond 3 |

## Calls and cost

| Member | Answered | Failed | Not by the configured model | Input tokens | Cached | Output tokens | Est. cost |
|---|---|---|---|---|---|---|---|
| a | 283 | 0 | 0 | 1,213,111 | 1,160,361 | 17,574 | $0.86 |
| b | 283 | 0 | 0 | 1,832,611 | 1,726,175 | 24,752 | $1.66 |
| c | 283 | 0 | 0 | 1,345,397 | 93,719 | 19,764 | $5.50 |
