# Committee pilot: exp-005-side-committee-pilot-0.4

Generated 2026-11-18T22:43:14+00:00 by `sidechat/pipeline/label.py`. Every number below is measured in this run.

## What was run

- **Lines:** 283 from `pilot-0.4`, 265 with a definite decision in the guide and 18 graded.
- **Guide:** `sidechat-guide-0.2`, prompt hash `8b6452d7cbd5`.
- **Members:** a, b, c, one model family each, at low reasoning effort. Model ids are configuration, not named here (SD-09).
- **Label set:** `pilot-0.4-committee-0.2` in R2.

## Agreement with the guide

**Majority decision: 99.2% (263/265; 97.3 to 99.8).** Target 90%: met. No majority on the decision for 1 lines.

| | Decision | Intent | For the agent or not | Rule | Mean distance on `speak` |
|---|---|---|---|---|---|
| Majority | 99.2% (263/265; 97.3 to 99.8) | 98.9% (270/273; 96.8 to 99.6) | | | |
| Member a | 95.5% (253/265; 92.2 to 97.4) | 96.0% (262/273; 92.9 to 97.7) | 98.1% (263/268; 95.7 to 99.2) | 83.4% (236/283; 78.6 to 87.3) | 0.141 |
| Member b | 99.2% (263/265; 97.3 to 99.8) | 99.3% (271/273; 97.4 to 99.8) | 99.6% (267/268; 97.9 to 99.9) | 86.9% (246/283; 82.5 to 90.4) | 0.028 |
| Member c | 98.9% (262/265; 96.7 to 99.6) | 98.5% (269/273; 96.3 to 99.4) | 98.9% (265/268; 96.8 to 99.6) | 87.3% (247/283; 82.9 to 90.7) | 0.042 |

Members agreeing with each other on the decision: a-b 94.3% (267/283), a-c 94.3% (267/283), b-c 96.8% (274/283). All three give the same decision and intent on 90.5% (256/283) of lines.

**By the guide's decision**

| Guide says | Majority agrees |
|---|---|
| ignore | 98.8% (161/163; 95.6 to 99.7) |
| respond | 100.0% (76/76; 95.2 to 100.0) |
| wait | 100.0% (26/26; 87.1 to 100.0) |

**By rule**

| Rule | Majority agrees |
|---|---|
| G7 | 98.3% (115/117; 94.0 to 99.5) |
| G6 | 100.0% (51/51; 93.0 to 100.0) |
| G2 | 100.0% (43/43; 91.8 to 100.0) |
| G3 | 100.0% (27/27; 87.5 to 100.0) |
| G4 | 100.0% (15/15; 79.6 to 100.0) |
| G5 | 100.0% (7/7; 64.6 to 100.0) |
| G1 | 100.0% (4/4; 51.0 to 100.0) |
| G8 | 100.0% (1/1; 20.6 to 100.0) |

**Kinds under 100%**

| Kind | Majority agrees |
|---|---|
| `thinking_aloud` | 75.0% (3/4) |
| `table_talk` | 50.0% (1/2) |

## Lines where the majority differs from the guide (2)

**game-09/12** `table_talk` (G7): guide **ignore**, majority **none**
> Finn: Rook, is there another way round?
> agent: There's a narrow window above, big enough for one of you.
> **Finn: Who's the smallest?**

- a: respond / direct / speak 5 / G6: Finn follows up on Rook’s answer about the narrow window by asking which character is smallest.
- b: wait / other / speak 3 / G6: Finn's follow-up to Rook's answer may be for the game master, who knows the characters, or for the other players, and nothing settles which.
- c: ignore / other / speak 1 / G7: Finn turns from the game master to ask the other players about their characters so they can decide who climbs through.

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
| a | 283 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| b | 283 | 0 | 0 | 0 | 0 | 0 | $0.00 |
| c | 283 | 0 | 0 | 0 | 0 | 0 | $0.00 |
