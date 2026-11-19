# Jev baseline: exp-003-side-jev-pilot-0.2

Generated 2026-11-18T22:31:54+00:00 by `sidechat/pipeline/baseline.py`. Every number below is measured in this run.

## What was run

- **Model:** `jev-1.13.0`, asked with the daily-audience demo's two questions and state (commit `73171de`, wording hash `476c554866d6`), through Pipecat 1.16.0's `JevClassifier`.
- **Decision rule:** the demo's. Answer now when `addressed ≥ 0.8`, hold for silence when `question ≥ 0.5`, otherwise stay quiet.
- **Requests:** 333 distinct (333 reused from earlier runs, 0 asked now, 0 failed).
- **Tokens this run:** 0 in, 0 out. About $0 at $0.042 per million input tokens, a price recorded in Audience's repo and not confirmed with TypeSafe.
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

## pilot-0.2

Source: `data/suites/pilot-0.2.yaml`. Use: test.

283 rows, 283 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 81.5% (216/265; 76.4 to 85.7) | 83.0% (132/159) | 1.3% (2/159) | 15.7% (25/159) | 73.4% (58/79) | 13.9% (11/79) |
| Name said → answer | 67.5% (179/265; 61.7 to 72.9) | 86.8% (138/159) | 13.2% (21/159) | 0.0% (0/159) | 51.9% (41/79) | 48.1% (38/79) |

Jev latency from Modal: 144 ms at the median, 225 ms at the 95th percentile (283 answers, 12 requests at a time).

Jev's `addressed` number without a threshold: AUROC 0.9665, average precision 0.943, calibration error 0.0616 (88 lines for the agent, 183 not).

**By code** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `P` | 92 | 88.0% (81/92) | 0.0% (0/92) | 12.0% (11/92) | n/a | n/a |
| `D` | 78 | 73.1% (57/78) | 100.0% (1/1) | 0.0% (0/1) | 74.0% (57/77) | 14.3% (11/77) |
| `G` | 31 | 71.0% (22/31) | 3.2% (1/31) | 25.8% (8/31) | n/a | n/a |
| `O` | 19 | 94.7% (18/19) | n/a | n/a | n/a | n/a |
| `N` | 16 | 87.5% (14/16) | 0.0% (0/16) | 12.5% (2/16) | n/a | n/a |
| `A` | 15 | 73.3% (11/15) | 0.0% (0/15) | 26.7% (4/15) | n/a | n/a |
| `I~` | 10 | n/a | n/a | n/a | n/a | n/a |
| `U` | 8 | 100.0% (8/8) | n/a | n/a | n/a | n/a |
| `D~` | 8 | n/a | n/a | n/a | n/a | n/a |
| `X` | 4 | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |
| `I` | 2 | 50.0% (1/2) | n/a | n/a | 50.0% (1/2) | 0.0% (0/2) |

**By style** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `clean` | 265 | 81.8% (202/247) | 0.7% (1/147) | 16.3% (24/147) | 74.0% (54/73) | 15.1% (11/73) |
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
| `unclear_after_agent` | 8 | 100.0% (8/8) | n/a | n/a | n/a | n/a |
| `answer_to_agent_question` | 8 | 25.0% (2/8) | n/a | n/a | 25.0% (2/8) | 62.5% (5/8) |
| `open_factual` | 8 | 100.0% (8/8) | n/a | n/a | n/a | n/a |
| `people_after_agent` | 7 | 100.0% (7/7) | 0.0% (0/7) | 0.0% (0/7) | n/a | n/a |
| `you_to_person_after_agent` | 7 | 57.1% (4/7) | 0.0% (0/7) | 42.9% (3/7) | n/a | n/a |
| `name_word_sense` | 6 | 83.3% (5/6) | 0.0% (0/6) | 16.7% (1/6) | n/a | n/a |
| `named_after_aside` | 5 | 100.0% (5/5) | n/a | n/a | 100.0% (5/5) | 0.0% (0/5) |
| `open_question` | 4 | 100.0% (4/4) | n/a | n/a | n/a | n/a |
| `thinking_aloud` | 4 | 50.0% (2/4) | 0.0% (0/4) | 50.0% (2/4) | n/a | n/a |
| `about_judged` | 4 | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |
| `unclear_you` | 4 | 100.0% (4/4) | n/a | n/a | n/a | n/a |
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
| 0.5 | 89.9% (71/79) | 6.9% (11/159) |
| 0.6 | 79.8% (63/79) | 5.0% (8/159) |
| 0.7 | 78.5% (62/79) | 4.4% (7/159) |
| 0.8 | 73.4% (58/79) | 1.3% (2/159) |
| 0.9 | 57.0% (45/79) | 0.6% (1/159) |

**Lines Jev decides differently from the label** (49 of 265)

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
| Amy: I still don't get why the derivative of x squared is two x. | `statement_of_need` | ignore | wait | 0.13 | 0.94 |
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
| Hugo: Is the bot recording this? | `about_question` | wait | respond | 0.87 | 0.83 |
| Cal: Ooh. Spain? | `reply_to_person` | ignore | wait | 0.04 | 0.85 |
| Bea: Could you send me the quiz link? | `unclear_you_person_task` | ignore | wait | 0.22 | 0.88 |
| Bea: Is anyone else's video frozen? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Jon: Go on. | `resume_no_name` | respond | ignore | 0.36 | 0.32 |
| Karen: Max, play some... actually, never mind. | `never_mind` | ignore | respond | 0.88 | 0.11 |
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
| Karen: Well, write down what it said. | `you_to_person_after_agent` | ignore | wait | 0.32 | 0.80 |
| Karen: It's clever, isn't it. | `about_pronoun` | ignore | wait | 0.30 | 0.71 |
| Wes: Roll it back? | `proposal_to_group` | ignore | wait | 0.08 | 0.92 |

**Graded lines, no single right decision** (18)

| Line | Kind | Jev | addressed | question |
|---|---|---|---|---|
| Lena: Atlas would know, it's got the board. | `invite` | ignore | 0.18 | 0.35 |
| Raj: Brilliant. Thanks for your help. | `thanks` | ignore | 0.62 | 0.03 |
| Karen: No idea. Ask Max. | `invite` | ignore | 0.16 | 0.35 |
| Leo: Okay, thanks. | `thanks` | ignore | 0.79 | 0.03 |
| Tess: A week if your kitchen's warm. Juno might have the science on that. | `invite` | ignore | 0.24 | 0.29 |
| Jill: Maybe Atlas can tell us which quarter it thinks we're in. | `invite` | wait | 0.18 | 0.81 |
| Grace: I think so. Ask it. | `invite` | wait | 0.20 | 0.59 |
| Sam: No! Okay. That's enough, Atlas, thanks. | `stop_named` | respond | 0.85 | 0.08 |
| Paul: Thanks, Max. | `thanks_named` | respond | 0.89 | 0.02 |
| Paul: Okay Max, that's enough for now. | `stop_named` | respond | 0.95 | 0.11 |
| Lily: Goodnight Juno! | `farewell_named` | respond | 0.91 | 0.05 |
| Pat: Could someone ask the assistant to add me to that? | `relayed_invite` | wait | 0.19 | 0.92 |
| Pat: Cheers. | `thanks` | ignore | 0.15 | 0.03 |
| Dana: We do. Nova can walk you through the details. | `invite` | ignore | 0.10 | 0.04 |
| Chris: I'd want to see what the assistant makes of our data volume. | `indirect_wish` | wait | 0.33 | 0.83 |
| Dana: Go ahead and ask it. | `invite` | ignore | 0.14 | 0.35 |
| Karen: Ask it what seven eights are. | `invite` | wait | 0.24 | 0.82 |
| Omar: Thanks, Atlas, that's handy. | `thanks_named` | respond | 0.82 | 0.03 |
