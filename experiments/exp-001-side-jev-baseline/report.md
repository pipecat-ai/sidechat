# Jev baseline: exp-001-side-jev-baseline

Generated 2026-11-18T21:58:02+00:00 by `sidechat/pipeline/baseline.py`. Every number below is measured in this run.

## What was run

- **Model:** `jev-1.13.0`, asked with the daily-audience demo's two questions and state (commit `73171de`, wording hash `476c554866d6`), through Pipecat 1.16.0's `JevClassifier`.
- **Decision rule:** the demo's. Answer now when `addressed ≥ 0.8`, hold for silence when `question ≥ 0.5`, otherwise stay quiet.
- **Requests:** 57,434 distinct (0 reused from earlier runs, 57,434 asked now, 0 failed).
- **Tokens this run:** 48,333,777 in, 2,125,058 out. About $2.03 at $0.042 per million input tokens, a price recorded in Audience's repo and not confirmed with TypeSafe.
- **Baseline id:** `jev-demo-0.1`. Stored answers are reused, so later runs compare against these numbers.

A share is written `value (k/n; 95% interval)`. "For others" means lines the set marks as not for the agent.

## demo-lines-0.1

Source: `data/suites/demo-lines-0.1.yaml`. Use: test.

52 rows, 52 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 97.9% (47/48; 89.1 to 99.6) | 96.2% (25/26) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |
| Name said → answer | 60.4% (29/48; 46.3 to 73.0) | 53.8% (14/26) | 46.2% (12/26) | 0.0% (0/26) | 79.0% (15/19) | 21.1% (4/19) |

Jev latency from Modal: 154 ms at the median, 201 ms at the 95th percentile (52 answers, 12 requests at a time).

Jev's `addressed` number without a threshold: AUROC 1.0, average precision 1.0, calibration error 0.0623 (19 lines for the agent, 29 not).

**By code** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `D` | 17 | 100.0% (17/17) | n/a | n/a | 100.0% (17/17) | 0.0% (0/17) |
| `P` | 12 | 100.0% (12/12) | 0.0% (0/12) | 0.0% (0/12) | n/a | n/a |
| `A` | 12 | 91.7% (11/12) | 0.0% (0/12) | 8.3% (1/12) | n/a | n/a |
| `?` | 4 | n/a | n/a | n/a | n/a | n/a |
| `O` | 3 | 100.0% (3/3) | n/a | n/a | n/a | n/a |
| `G` | 2 | 100.0% (2/2) | 0.0% (0/2) | 0.0% (0/2) | n/a | n/a |
| `I` | 2 | 100.0% (2/2) | n/a | n/a | 100.0% (2/2) | 0.0% (0/2) |

**By style** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `clean` | 52 | 97.9% (47/48) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |

**By kind** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `name_first` | 8 | 100.0% (8/8) | n/a | n/a | 100.0% (8/8) | 0.0% (0/8) |
| `reply_to_person` | 7 | 100.0% (7/7) | 0.0% (0/7) | 0.0% (0/7) | n/a | n/a |
| `question_to_named_person` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `open_question` | 3 | 100.0% (3/3) | n/a | n/a | n/a | n/a |
| `about_judged` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `about_to_named_person` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `statement` | 2 | 100.0% (2/2) | 0.0% (0/2) | 0.0% (0/2) | n/a | n/a |
| `unclear_you` | 2 | n/a | n/a | n/a | n/a | n/a |
| `role_request` | 2 | 100.0% (2/2) | n/a | n/a | 100.0% (2/2) | 0.0% (0/2) |
| `follow_up` | 2 | 100.0% (2/2) | n/a | n/a | 100.0% (2/2) | 0.0% (0/2) |
| `name_mid` | 2 | 100.0% (2/2) | n/a | n/a | 100.0% (2/2) | 0.0% (0/2) |
| `about_reported` | 2 | 100.0% (2/2) | 0.0% (0/2) | 0.0% (0/2) | n/a | n/a |
| `about_stated` | 2 | 100.0% (2/2) | 0.0% (0/2) | 0.0% (0/2) | n/a | n/a |
| `about_hypothetical` | 2 | 50.0% (1/2) | 0.0% (0/2) | 50.0% (1/2) | n/a | n/a |
| `thanks` | 1 | n/a | n/a | n/a | n/a | n/a |
| `you_to_person_after_agent` | 1 | 100.0% (1/1) | 0.0% (0/1) | 0.0% (0/1) | n/a | n/a |
| `remark_to_group` | 1 | n/a | n/a | n/a | n/a | n/a |
| `name_last` | 1 | 100.0% (1/1) | n/a | n/a | 100.0% (1/1) | 0.0% (0/1) |
| `thanks_named` | 1 | 100.0% (1/1) | n/a | n/a | 100.0% (1/1) | 0.0% (0/1) |
| `name_alone` | 1 | 100.0% (1/1) | n/a | n/a | 100.0% (1/1) | 0.0% (0/1) |
| `stop_named` | 1 | 100.0% (1/1) | n/a | n/a | 100.0% (1/1) | 0.0% (0/1) |
| `aside_over_agent` | 1 | 100.0% (1/1) | 0.0% (0/1) | 0.0% (0/1) | n/a | n/a |
| `name_first_over_agent` | 1 | 100.0% (1/1) | n/a | n/a | 100.0% (1/1) | 0.0% (0/1) |

**Moving the `addressed` threshold**

| Threshold | For the agent: answers now | For others: answers now |
|---|---|---|
| 0.5 | 100.0% (19/19) | 0.0% (0/26) |
| 0.6 | 100.0% (19/19) | 0.0% (0/26) |
| 0.7 | 100.0% (19/19) | 0.0% (0/26) |
| 0.8 | 100.0% (19/19) | 0.0% (0/26) |
| 0.9 | 73.7% (14/19) | 0.0% (0/26) |

**Lines Jev decides differently from the label** (1 of 48)

| Line | Kind | Expected | Jev | addressed | question |
|---|---|---|---|---|---|
| Jon: Should we ask Atlas? | `about_hypothetical` | ignore | wait | 0.06 | 0.92 |

**Graded lines, no single right decision** (4)

| Line | Kind | Jev | addressed | question |
|---|---|---|---|---|
| Jon: Can you look up the weather in Paris for me? | `unclear_you` | wait | 0.50 | 0.92 |
| Sam: Thanks! | `thanks` | ignore | 0.71 | 0.02 |
| Sam: Could you send me that file after the call? | `unclear_you` | wait | 0.09 | 0.72 |
| Jon: Is it just me or is the audio a bit choppy? | `remark_to_group` | wait | 0.07 | 0.93 |

## pilot-0.1

Source: `data/suites/pilot-0.1.yaml`. Use: test.

283 rows, 283 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 81.8% (207/253; 76.6 to 86.1) | 84.1% (132/157) | 0.6% (1/157) | 15.3% (24/157) | 73.4% (58/79) | 13.9% (11/79) |
| Name said → answer | 70.4% (178/253; 64.5 to 75.6) | 87.3% (137/157) | 12.7% (20/157) | 0.0% (0/157) | 51.9% (41/79) | 48.1% (38/79) |

Jev latency from Modal: 144 ms at the median, 225 ms at the 95th percentile (283 answers, 12 requests at a time).

Jev's `addressed` number without a threshold: AUROC 0.9648, average precision 0.9405, calibration error 0.0658 (88 lines for the agent, 185 not).

**By code** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `P` | 92 | 88.0% (81/92) | 0.0% (0/92) | 12.0% (11/92) | n/a | n/a |
| `D` | 77 | 74.0% (57/77) | n/a | n/a | 74.0% (57/77) | 14.3% (11/77) |
| `G` | 29 | 72.4% (21/29) | 3.5% (1/29) | 24.1% (7/29) | n/a | n/a |
| `O` | 17 | 100.0% (17/17) | n/a | n/a | n/a | n/a |
| `N` | 17 | 88.2% (15/17) | 0.0% (0/17) | 11.8% (2/17) | n/a | n/a |
| `A` | 15 | 73.3% (11/15) | 0.0% (0/15) | 26.7% (4/15) | n/a | n/a |
| `I~` | 11 | n/a | n/a | n/a | n/a | n/a |
| `?` | 10 | n/a | n/a | n/a | n/a | n/a |
| `D~` | 9 | n/a | n/a | n/a | n/a | n/a |
| `X` | 4 | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |
| `I` | 2 | 50.0% (1/2) | n/a | n/a | 50.0% (1/2) | 0.0% (0/2) |

**By style** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `clean` | 265 | 82.1% (193/235) | 0.0% (0/145) | 15.9% (23/145) | 74.0% (54/73) | 15.1% (11/73) |
| `stt` | 18 | 77.8% (14/18) | 8.3% (1/12) | 8.3% (1/12) | 66.7% (4/6) | 0.0% (0/6) |

**By kind** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `reply_to_person` | 54 | 92.6% (50/54) | 0.0% (0/54) | 7.4% (4/54) | n/a | n/a |
| `name_first` | 25 | 100.0% (25/25) | n/a | n/a | 100.0% (25/25) | 0.0% (0/25) |
| `question_to_named_person` | 17 | 100.0% (17/17) | 0.0% (0/17) | 0.0% (0/17) | n/a | n/a |
| `statement` | 10 | 100.0% (10/10) | 0.0% (0/10) | 0.0% (0/10) | n/a | n/a |
| `follow_up` | 9 | 55.6% (5/9) | n/a | n/a | 55.6% (5/9) | 0.0% (0/9) |
| `backchannel` | 9 | 100.0% (9/9) | 0.0% (0/9) | 0.0% (0/9) | n/a | n/a |
| `invite` | 8 | n/a | n/a | n/a | n/a | n/a |
| `answer_to_agent_question` | 8 | 25.0% (2/8) | n/a | n/a | 25.0% (2/8) | 62.5% (5/8) |
| `open_factual` | 8 | 100.0% (8/8) | n/a | n/a | n/a | n/a |
| `people_after_agent` | 7 | 100.0% (7/7) | 0.0% (0/7) | 0.0% (0/7) | n/a | n/a |
| `unclear_after_agent` | 7 | n/a | n/a | n/a | n/a | n/a |
| `you_to_person_after_agent` | 6 | 66.7% (4/6) | 0.0% (0/6) | 33.3% (2/6) | n/a | n/a |
| `name_word_sense` | 6 | 83.3% (5/6) | 0.0% (0/6) | 16.7% (1/6) | n/a | n/a |
| `named_after_aside` | 5 | 100.0% (5/5) | n/a | n/a | 100.0% (5/5) | 0.0% (0/5) |
| `open_question` | 4 | 100.0% (4/4) | n/a | n/a | n/a | n/a |
| `thinking_aloud` | 4 | 50.0% (2/4) | 0.0% (0/4) | 50.0% (2/4) | n/a | n/a |
| `about_judged` | 4 | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |
| `unclear_you` | 4 | 100.0% (3/3) | n/a | n/a | n/a | n/a |
| `other_device` | 4 | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |
| `group_question_not_for_agent` | 3 | 0.0% (0/3) | 0.0% (0/3) | 100.0% (3/3) | n/a | n/a |
| `to_named_person_after_agent` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `thanks` | 3 | n/a | n/a | n/a | n/a | n/a |
| `command_no_name` | 3 | 33.3% (1/3) | n/a | n/a | 33.3% (1/3) | 33.3% (1/3) |
| `off_call` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `about_to_named_person` | 3 | 66.7% (2/3) | 0.0% (0/3) | 33.3% (1/3) | n/a | n/a |
| `you_after_invite` | 3 | 100.0% (3/3) | n/a | n/a | 100.0% (3/3) | 0.0% (0/3) |
| `statement_to_named_person` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `wake_phrase` | 3 | 100.0% (3/3) | n/a | n/a | 100.0% (3/3) | 0.0% (0/3) |
| `addressed_by_exclusion` | 2 | 0.0% (0/2) | n/a | n/a | 0.0% (0/2) | 50.0% (1/2) |
| `reply_then_request` | 2 | 50.0% (1/2) | n/a | n/a | 50.0% (1/2) | 50.0% (1/2) |
| `action_to_game_master` | 2 | 0.0% (0/2) | n/a | n/a | 0.0% (0/2) | 100.0% (2/2) |
| `table_talk` | 2 | 0.0% (0/2) | 0.0% (0/2) | 100.0% (2/2) | n/a | n/a |
| `question_only_agent_can_answer` | 2 | 50.0% (1/2) | n/a | n/a | 50.0% (1/2) | 0.0% (0/2) |
| `about_reported` | 2 | 100.0% (2/2) | 0.0% (0/2) | 0.0% (0/2) | n/a | n/a |
| `about_hypothetical` | 2 | 50.0% (1/2) | 0.0% (0/2) | 50.0% (1/2) | n/a | n/a |
| `role_request` | 2 | 50.0% (1/2) | n/a | n/a | 50.0% (1/2) | 0.0% (0/2) |
| `role_address` | 2 | 100.0% (2/2) | n/a | n/a | 100.0% (2/2) | 0.0% (0/2) |
| `open_request` | 2 | 100.0% (2/2) | n/a | n/a | n/a | n/a |
| `stop_named` | 2 | n/a | n/a | n/a | n/a | n/a |
| `thanks_named` | 2 | n/a | n/a | n/a | n/a | n/a |

**Moving the `addressed` threshold**

| Threshold | For the agent: answers now | For others: answers now |
|---|---|---|
| 0.5 | 89.9% (71/79) | 6.4% (10/157) |
| 0.6 | 79.8% (63/79) | 4.5% (7/157) |
| 0.7 | 78.5% (62/79) | 3.8% (6/157) |
| 0.8 | 73.4% (58/79) | 0.6% (1/157) |
| 0.9 | 57.0% (45/79) | 0.6% (1/157) |

**Lines Jev decides differently from the label** (46 of 253)

| Line | Kind | Expected | Jev | addressed | question |
|---|---|---|---|---|---|
| Jon: Anything else before we wrap? | `group_question_not_for_agent` | ignore | wait | 0.08 | 0.93 |
| Chris: And what does that look like monthly instead of annual? | `follow_up` | respond | wait | 0.75 | 0.92 |
| Raj: Hi, we're calling about the router, it keeps dropping. | `opener_to_agent` | respond | wait | 0.16 | 0.50 |
| Anita: It's blinking orange. | `answer_to_agent_question` | respond | ignore | 0.50 | 0.04 |
| Raj: While she does that, is there an outage in our area? | `addressed_by_exclusion` | respond | wait | 0.55 | 0.93 |
| Anita: Okay, it's back on. Solid green. | `answer_to_agent_question` | respond | ignore | 0.14 | 0.03 |
| Karen: What's that for? | `you_to_person_after_agent` | ignore | wait | 0.31 | 0.87 |
| Ella: Okay, stop the timer, I'm draining it now. | `command_no_name` | respond | ignore | 0.10 | 0.08 |
| Theo: Can we stop for chips? | `request_to_people` | ignore | wait | 0.04 | 0.93 |
| Amy: But why does that work? | `reply_to_person` | ignore | wait | 0.08 | 0.92 |
| Chloe: Did you write that down? | `you_to_person_after_agent` | ignore | wait | 0.25 | 0.79 |
| Marco: How long does a starter take, roughly? | `continuing_with_person` | ignore | wait | 0.06 | 0.68 |
| Kit: I want to check the door for traps. | `action_to_game_master` | respond | ignore | 0.08 | 0.26 |
| Kit: Fourteen. | `answer_to_agent_question` | respond | ignore | 0.71 | 0.06 |
| Zoe: I try to disarm it. | `action_to_game_master` | respond | ignore | 0.18 | 0.09 |
| Finn: Wait, do we even need to go through this door? | `table_talk` | ignore | wait | 0.05 | 0.92 |
| Finn: Who's the smallest? | `table_talk` | ignore | wait | 0.18 | 0.92 |
| Zoe: Seventeen. | `answer_to_agent_question` | respond | ignore | 0.14 | 0.07 |
| Harold: Amlodipine, five milligrams, once a day. | `answer_to_agent_question` | respond | ignore | 0.52 | 0.05 |
| Harold: And the water tablet. | `answer_to_agent_question` | respond | wait | 0.57 | 0.69 |
| Kate: He means furosemide. | `addressed_by_exclusion` | respond | ignore | 0.51 | 0.06 |
| Harold: Oh yes. Penicillin. | `reply_then_request` | respond | ignore | 0.59 | 0.05 |
| Kate: Is the doctor running late? | `question_only_agent_can_answer` | respond | wait | 0.26 | 0.84 |
| Jon: at last a number that makes sense | `alias_false_match` | ignore | respond | 0.94 | 0.35 |
| Priya: and what about september | `follow_up` | respond | wait | 0.73 | 0.91 |
| Omar: Did anyone try the new assistant in the design review? | `about_question_to_group` | ignore | wait | 0.05 | 0.95 |
| Omar: Should we ask Atlas to take minutes today? | `about_hypothetical` | ignore | wait | 0.06 | 0.95 |
| Cal: Ooh. Spain? | `reply_to_person` | ignore | wait | 0.04 | 0.85 |
| Bea: Could you send me the quiz link? | `unclear_you_person_task` | ignore | wait | 0.22 | 0.88 |
| Bea: Is anyone else's video frozen? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Jon: Go on. | `resume_no_name` | respond | ignore | 0.36 | 0.32 |
| Karen: Two biscuits max, Paul. | `name_word_sense` | ignore | wait | 0.56 | 0.52 |
| Noah: This one? | `reply_to_person` | ignore | wait | 0.04 | 0.55 |
| Ines: Noah, did Nova get that right? | `about_to_named_person` | ignore | wait | 0.06 | 0.60 |
| Lou: I'd like the AI to send the invite as well. | `role_request` | respond | wait | 0.53 | 0.80 |
| Leo: Oh. Cancel that. | `command_no_name` | respond | wait | 0.73 | 0.62 |
| Jack: What do you want to do? | `you_to_person` | ignore | wait | 0.03 | 0.91 |
| Jack: Hmm, what was the name of that other place, the one by the canal... | `thinking_aloud` | ignore | wait | 0.05 | 0.87 |
| Karen: whats for dinner | `group_question_not_for_agent` | ignore | wait | 0.15 | 0.94 |
| Ella: and what about parsnips | `follow_up` | respond | wait | 0.58 | 0.93 |
| Greg: Where did I put that file... | `thinking_aloud` | ignore | wait | 0.08 | 0.82 |
| Hana: Is it in the shared drive? | `reply_to_person` | ignore | wait | 0.03 | 0.67 |
| Chris: Both ways, good. What about HubSpot? | `follow_up` | respond | wait | 0.68 | 0.91 |
| Karen: Well, write down what it said. | `people_discussing_agent_answer` | ignore | wait | 0.32 | 0.80 |
| Karen: It's clever, isn't it. | `about_pronoun` | ignore | wait | 0.30 | 0.71 |
| Wes: Roll it back? | `proposal_to_group` | ignore | wait | 0.08 | 0.92 |

**Graded lines, no single right decision** (30)

| Line | Kind | Jev | addressed | question |
|---|---|---|---|---|
| Lena: Atlas would know, it's got the board. | `invite` | ignore | 0.18 | 0.35 |
| Maya: Is that counting the bug fixes? | `unclear_after_agent` | wait | 0.66 | 0.92 |
| Raj: Brilliant. Thanks for your help. | `thanks` | ignore | 0.62 | 0.03 |
| Karen: No idea. Ask Max. | `invite` | ignore | 0.16 | 0.35 |
| Theo: Does it have chips? | `unclear_after_agent` | wait | 0.69 | 0.89 |
| Leo: Okay, thanks. | `thanks` | ignore | 0.79 | 0.03 |
| Amy: I still don't get why the derivative of x squared is two x. | `statement_of_need` | wait | 0.13 | 0.94 |
| Tess: A week if your kitchen's warm. Juno might have the science on that. | `invite` | ignore | 0.24 | 0.29 |
| Jill: Maybe Atlas can tell us which quarter it thinks we're in. | `invite` | wait | 0.18 | 0.81 |
| Hugo: Is the bot recording this? | `about_question` | respond | 0.87 | 0.83 |
| Grace: I think so. Ask it. | `invite` | wait | 0.20 | 0.59 |
| Sam: Wait, the fourteenth? | `unclear_after_agent` | wait | 0.57 | 0.77 |
| Sam: No! Okay. That's enough, Atlas, thanks. | `stop_named` | respond | 0.85 | 0.08 |
| Paul: Thanks, Max. | `thanks_named` | respond | 0.89 | 0.02 |
| Karen: Max, play some... actually, never mind. | `never_mind` | respond | 0.88 | 0.11 |
| Paul: Okay Max, that's enough for now. | `stop_named` | respond | 0.95 | 0.11 |
| Lily: Goodnight Juno! | `farewell_named` | respond | 0.91 | 0.05 |
| Pat: Could someone ask the assistant to add me to that? | `relayed_invite` | wait | 0.19 | 0.92 |
| Pat: Cheers. | `thanks` | ignore | 0.15 | 0.03 |
| Nina: Not that low. | `unclear_after_agent` | wait | 0.63 | 0.77 |
| Olu: Can you look into the place on Mill Street? | `unclear_you` | wait | 0.14 | 0.80 |
| Olu: Book it before someone else does. | `unclear_after_agent` | wait | 0.21 | 0.79 |
| Dana: We do. Nova can walk you through the details. | `invite` | ignore | 0.10 | 0.04 |
| Chris: I'd want to see what the assistant makes of our data volume. | `indirect_wish` | wait | 0.33 | 0.83 |
| Dana: Go ahead and ask it. | `invite` | ignore | 0.14 | 0.35 |
| Marco: Great. Can you repeat that last one for the recording? | `unclear_after_agent` | wait | 0.45 | 0.81 |
| Ken: Sorry, I missed that, what's first? | `unclear_after_agent` | wait | 0.28 | 0.93 |
| Karen: Is that right? I thought it was just sunlight. | `people_discussing_agent_answer` | wait | 0.77 | 0.91 |
| Karen: Ask it what seven eights are. | `invite` | wait | 0.24 | 0.82 |
| Omar: Thanks, Atlas, that's handy. | `thanks_named` | respond | 0.82 | 0.03 |

## ambient-bench-0.1

Source: `text-ai/social-ai-ambient-bench` at `5efda0b267d6`. Use: test only; the dataset forbids training on it.

16,222 rows, 16,222 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 85.4% (13479/15793; 84.8 to 85.9) | 85.4% (13479/15793) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |
| Name said → answer | 99.8% (15756/15793; 99.7 to 99.8) | 99.8% (15756/15793) | 0.2% (37/15793) | 0.0% (0/15793) | n/a | n/a |

Jev latency from Modal: 150 ms at the median, 213 ms at the 95th percentile (16,222 answers, 12 requests at a time).

**The benchmark's own metrics.** Its policy expects the assistant to offer help nobody asked for, so a model that speaks only when spoken to misses many RESPOND lines by design.

| Reading | Scenario pass rate | Macro F1 | False interruptions | Missed interventions | Turn accuracy |
|---|---|---|---|---|---|
| strict (speaks = answers now) | 72.8% (882/1212) | 0.5591 | 0.1% (13/15793) | 92.8% (398/429) | 97.5% (15811/16222) |
| lenient (speaks = answers now or holds) | 20.1% (244/1212) | 0.5864 | 14.6% (2314/15793) | 7.5% (32/429) | 85.5% (13876/16222) |
| name_only | 72.4% (877/1212) | 0.5612 | 0.2% (37/15793) | 92.1% (395/429) | 97.3% (15790/16222) |
| *Claude Opus 4.6, from the benchmark's own leaderboard* | 67.4% | | 4.5% | 25.6% | 94.9% |
| *Gemini 3.1 Pro Preview, from the benchmark's own leaderboard* | 63.6% | | 3.3% | 46.7% | 95.5% |
| *GPT-5.5, from the benchmark's own leaderboard* | 63.6% | | 4.1% | 30.8% | 95.2% |

AUROC of `max(addressed, question)` against RESPOND: 0.9416.

**By bench** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `SILENT` | 15793 | 85.4% (13479/15793) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |
| `RESPOND` | 429 | n/a | n/a | n/a | n/a | n/a |

**By category** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `stay_silent` | 7399 | 90.1% (6645/7371) | 0.0% (0/7371) | 9.8% (726/7371) | n/a | n/a |
| `offering_suggestions` | 3302 | 82.8% (2695/3253) | 0.0% (1/3253) | 17.1% (557/3253) | n/a | n/a |
| `knowledge_enrichment` | 2276 | 86.2% (1923/2232) | 0.0% (0/2232) | 13.8% (309/2232) | n/a | n/a |
| `fact_correction` | 688 | 85.7% (583/680) | 0.0% (0/680) | 14.3% (97/680) | n/a | n/a |
| `mixed_long` | 392 | 72.9% (256/351) | 0.3% (1/351) | 26.8% (94/351) | n/a | n/a |
| `multi_turn_respond` | 250 | 68.9% (133/193) | 5.2% (10/193) | 25.9% (50/193) | n/a | n/a |
| `direct_factual` | 232 | 82.6% (161/195) | 0.0% (0/195) | 17.4% (34/195) | n/a | n/a |
| `search_lookup` | 232 | 72.6% (143/197) | 0.0% (0/197) | 27.4% (54/197) | n/a | n/a |
| `translation_howto` | 144 | 79.8% (99/124) | 0.0% (0/124) | 20.2% (25/124) | n/a | n/a |
| `multilingual_respond` | 144 | 59.5% (75/126) | 0.8% (1/126) | 39.7% (50/126) | n/a | n/a |
| `multilingual_silent` | 144 | 75.7% (109/144) | 0.0% (0/144) | 24.3% (35/144) | n/a | n/a |
| `implicit_intervention` | 136 | 55.5% (66/119) | 0.0% (0/119) | 44.5% (53/119) | n/a | n/a |
| `milestone` | 76 | 79.7% (59/74) | 0.0% (0/74) | 20.3% (15/74) | n/a | n/a |
| `implicit_request_hard` | 72 | 64.5% (40/62) | 0.0% (0/62) | 35.5% (22/62) | n/a | n/a |
| `capability_request` | 68 | 59.3% (35/59) | 0.0% (0/59) | 40.7% (24/59) | n/a | n/a |
| `factual_confusion` | 68 | 71.2% (42/59) | 0.0% (0/59) | 28.8% (17/59) | n/a | n/a |
| `factual_gap` | 67 | 72.4% (42/58) | 0.0% (0/58) | 27.6% (16/58) | n/a | n/a |
| `group_discussion` | 66 | 75.4% (49/65) | 0.0% (0/65) | 24.6% (16/65) | n/a | n/a |
| `edge_case` | 65 | 69.2% (45/65) | 0.0% (0/65) | 30.8% (20/65) | n/a | n/a |
| `hobby` | 64 | 70.2% (40/57) | 0.0% (0/57) | 29.8% (17/57) | n/a | n/a |
| `opinion_debate` | 62 | 90.3% (56/62) | 0.0% (0/62) | 9.7% (6/62) | n/a | n/a |
| `family` | 47 | 67.4% (29/43) | 0.0% (0/43) | 32.6% (14/43) | n/a | n/a |
| `bystander_silence` | 46 | 84.8% (39/46) | 0.0% (0/46) | 15.2% (7/46) | n/a | n/a |
| `coordination` | 29 | 45.5% (10/22) | 0.0% (0/22) | 54.5% (12/22) | n/a | n/a |
| `simultaneous_threads` | 18 | 58.8% (10/17) | 0.0% (0/17) | 41.2% (7/17) | n/a | n/a |
| `stale_context` | 16 | 86.7% (13/15) | 0.0% (0/15) | 13.3% (2/15) | n/a | n/a |
| `casual_banter` | 14 | 85.7% (12/14) | 0.0% (0/14) | 14.3% (2/14) | n/a | n/a |
| `core` | 13 | 75.0% (6/8) | 0.0% (0/8) | 25.0% (2/8) | n/a | n/a |
| `topic_switch` | 13 | 66.7% (8/12) | 0.0% (0/12) | 33.3% (4/12) | n/a | n/a |
| `mixed_signals` | 12 | 54.5% (6/11) | 0.0% (0/11) | 45.5% (5/11) | n/a | n/a |
| `near_miss_request` | 11 | 80.0% (8/10) | 0.0% (0/10) | 20.0% (2/10) | n/a | n/a |
| `referenced_not_addressed` | 10 | 100.0% (10/10) | 0.0% (0/10) | 0.0% (0/10) | n/a | n/a |
| `sarcasm` | 10 | 87.5% (7/8) | 0.0% (0/8) | 12.5% (1/8) | n/a | n/a |
| `implicit_request` | 9 | 57.1% (4/7) | 0.0% (0/7) | 42.9% (3/7) | n/a | n/a |
| `emotional_factual` | 6 | 80.0% (4/5) | 0.0% (0/5) | 20.0% (1/5) | n/a | n/a |
| `capability_adjacent` | 6 | 100.0% (6/6) | 0.0% (0/6) | 0.0% (0/6) | n/a | n/a |
| `context_followup` | 5 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `rhetorical` | 5 | 80.0% (4/5) | 0.0% (0/5) | 20.0% (1/5) | n/a | n/a |
| `social_question` | 5 | 80.0% (4/5) | 0.0% (0/5) | 20.0% (1/5) | n/a | n/a |

## duplex-mpe-0.1

Source: `ChengqianMa/Duplex-MPE` at `6d5f59fab123`. Use: held-out benchmark; never train on it.

52,364 rows, 52,336 scored, 28 left out because the set's own labels disagree.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 83.1% (43495/52336; 82.8 to 83.4) | 83.6% (37215/44528) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |
| Name said → answer | 84.6% (44265/52336; 84.3 to 84.9) | 86.4% (38457/44528) | 13.6% (6071/44528) | 0.0% (0/44528) | 74.4% (5808/7808) | 25.6% (2000/7808) |

Jev latency from Modal: 152 ms at the median, 220 ms at the 95th percentile (52,336 answers, 12 requests at a time).

Jev's `addressed` number without a threshold: AUROC 0.9877, average precision 0.9579, calibration error 0.0728 (7,808 lines for the agent, 44,528 not).

**The same request with and without the agent's name** (2,000 pairs): answered now 99.2% with the name, 26.6% without. Difference -72.6 points (-74.6 to -70.6).

**By condition** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `explicit` | 26168 | 86.1% (22518/26168) | 0.3% (73/22264) | 15.9% (3538/22264) | 99.0% (3865/3904) | 0.0% (1/3904) |
| `implicit` | 26168 | 80.2% (20977/26168) | 0.5% (109/22264) | 16.1% (3593/22264) | 61.9% (2415/3904) | 0.1% (6/3904) |

**By event** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `N2` | 28092 | 80.8% (22701/28092) | 0.6% (180/28092) | 18.6% (5211/28092) | n/a | n/a |
| `N3` | 6534 | 83.2% (5439/6534) | 0.0% (0/6534) | 16.8% (1095/6534) | n/a | n/a |
| `N1` | 6080 | 86.7% (5271/6080) | 0.0% (0/6080) | 13.3% (809/6080) | n/a | n/a |
| `T` | 4000 | 62.8% (2514/4000) | n/a | n/a | 62.8% (2514/4000) | 0.1% (6/4000) |
| `N4_R` | 3822 | 99.5% (3804/3822) | 0.1% (2/3822) | 0.4% (16/3822) | n/a | n/a |
| `N4_Q` | 3808 | 98.9% (3766/3808) | n/a | n/a | 98.9% (3766/3808) | 0.0% (1/3808) |

**By condition/event** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `implicit/N2` | 14047 | 80.5% (11311/14047) | 0.8% (108/14047) | 18.7% (2628/14047) | n/a | n/a |
| `explicit/N2` | 14045 | 81.1% (11390/14045) | 0.5% (72/14045) | 18.4% (2583/14045) | n/a | n/a |
| `explicit/N3` | 3267 | 83.2% (2717/3267) | 0.0% (0/3267) | 16.8% (550/3267) | n/a | n/a |
| `implicit/N3` | 3267 | 83.3% (2722/3267) | 0.0% (0/3267) | 16.7% (545/3267) | n/a | n/a |
| `explicit/N1` | 3041 | 87.0% (2644/3041) | 0.0% (0/3041) | 13.1% (397/3041) | n/a | n/a |
| `implicit/N1` | 3039 | 86.4% (2627/3039) | 0.0% (0/3039) | 13.6% (412/3039) | n/a | n/a |
| `explicit/T` | 2000 | 99.2% (1983/2000) | n/a | n/a | 99.2% (1983/2000) | 0.1% (1/2000) |
| `implicit/T` | 2000 | 26.6% (531/2000) | n/a | n/a | 26.6% (531/2000) | 0.2% (5/2000) |
| `explicit/N4_R` | 1911 | 99.5% (1902/1911) | 0.1% (1/1911) | 0.4% (8/1911) | n/a | n/a |
| `implicit/N4_R` | 1911 | 99.5% (1902/1911) | 0.1% (1/1911) | 0.4% (8/1911) | n/a | n/a |
| `explicit/N4_Q` | 1904 | 98.8% (1882/1904) | n/a | n/a | 98.8% (1882/1904) | 0.0% (0/1904) |
| `implicit/N4_Q` | 1904 | 99.0% (1884/1904) | n/a | n/a | 99.0% (1884/1904) | 0.1% (1/1904) |

**By addressee** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `other_human` | 32838 | 84.3% (27676/32838) | 0.0% (6/32838) | 15.7% (5156/32838) | n/a | n/a |
| `aria` | 7808 | 80.4% (6280/7808) | n/a | n/a | 80.4% (6280/7808) | 0.1% (7/7808) |
| `none` | 6540 | 83.3% (5445/6540) | 0.0% (0/6540) | 16.7% (1095/6540) | n/a | n/a |
| `device` | 5146 | 79.5% (4090/5146) | 3.4% (176/5146) | 17.1% (880/5146) | n/a | n/a |
| `animal` | 4 | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |

**By speech_act** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `statement` | 26144 | 87.6% (22900/26144) | 0.0% (5/26144) | 12.4% (3239/26144) | n/a | n/a |
| `request` | 13418 | 73.7% (9892/13418) | 2.1% (174/8365) | 22.2% (1861/8365) | 70.5% (3562/5053) | 0.1% (6/5053) |
| `self_talk` | 6444 | 83.0% (5349/6444) | 0.0% (0/6444) | 17.0% (1095/6444) | n/a | n/a |
| `question` | 6326 | 84.6% (5352/6326) | 0.1% (3/3571) | 26.2% (934/3571) | 98.7% (2718/2755) | 0.0% (1/2755) |
| `backchannel` | 4 | 50.0% (2/4) | 0.0% (0/4) | 50.0% (2/4) | n/a | n/a |

**Moving the `addressed` threshold**

| Threshold | For the agent: answers now | For others: answers now |
|---|---|---|
| 0.5 | 92.0% (7187/7808) | 4.0% (1764/44528) |
| 0.6 | 89.4% (6980/7808) | 2.5% (1120/44528) |
| 0.7 | 85.8% (6697/7808) | 1.3% (574/44528) |
| 0.8 | 80.4% (6280/7808) | 0.4% (182/44528) |
| 0.9 | 70.1% (5471/7808) | 0.0% (17/44528) |
