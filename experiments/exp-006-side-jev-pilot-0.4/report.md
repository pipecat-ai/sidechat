# Jev baseline: exp-006-side-jev-pilot-0.4

Generated 2026-11-18T22:44:59+00:00 by `sidechat/pipeline/baseline.py`. Every number below is measured in this run.

## What was run

- **Model:** `jev-1.13.0`, asked with the daily-audience demo's two questions and state (commit `73171de`, wording hash `476c554866d6`), through Pipecat 1.16.0's `JevClassifier`.
- **Decision rule:** the demo's. Answer now when `addressed ≥ 0.8`, hold for silence when `question ≥ 0.5`, otherwise stay quiet.
- **Requests:** 283 distinct (283 reused from earlier runs, 0 asked now, 0 failed).
- **Tokens this run:** 0 in, 0 out. About $0 at $0.042 per million input tokens, a price recorded in Audience's repo and not confirmed with TypeSafe.
- **Baseline id:** `jev-demo-0.1`. Stored answers are reused, so later runs compare against these numbers.

A share is written `value (k/n; 95% interval)`. "For others" means lines the set marks as not for the agent.

## pilot-0.4

Source: `data/suites/pilot-0.4.yaml`. Use: test.

283 rows, 283 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 79.6% (211/265; 74.4 to 84.0) | 80.4% (131/163) | 1.8% (3/163) | 17.8% (29/163) | 75.0% (57/76) | 13.2% (10/76) |
| Name said → answer | 68.3% (181/265; 62.5 to 73.6) | 86.5% (141/163) | 13.5% (22/163) | 0.0% (0/163) | 52.6% (40/76) | 47.4% (36/76) |

Jev latency from Modal: 144 ms at the median, 225 ms at the 95th percentile (283 answers, 12 requests at a time).

Jev's `addressed` number without a threshold: AUROC 0.9705, average precision 0.9479, calibration error 0.0629 (86 lines for the agent, 182 not).

**By code** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `P` | 94 | 86.2% (81/94) | 0.0% (0/94) | 13.8% (13/94) | n/a | n/a |
| `D` | 76 | 73.7% (56/76) | 100.0% (2/2) | 0.0% (0/2) | 75.7% (56/74) | 13.5% (10/74) |
| `G` | 32 | 65.6% (21/32) | 3.1% (1/32) | 31.2% (10/32) | n/a | n/a |
| `O` | 16 | 87.5% (14/16) | n/a | n/a | n/a | n/a |
| `N` | 16 | 87.5% (14/16) | 0.0% (0/16) | 12.5% (2/16) | n/a | n/a |
| `A` | 15 | 73.3% (11/15) | 0.0% (0/15) | 26.7% (4/15) | n/a | n/a |
| `U` | 10 | 90.0% (9/10) | n/a | n/a | n/a | n/a |
| `I~` | 10 | n/a | n/a | n/a | n/a | n/a |
| `D~` | 8 | n/a | n/a | n/a | n/a | n/a |
| `X` | 4 | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |
| `I` | 2 | 50.0% (1/2) | n/a | n/a | 50.0% (1/2) | 0.0% (0/2) |

**By style** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `clean` | 265 | 79.3% (196/247) | 1.3% (2/151) | 18.5% (28/151) | 74.7% (53/71) | 14.1% (10/71) |
| `stt` | 18 | 83.3% (15/18) | 8.3% (1/12) | 8.3% (1/12) | 80.0% (4/5) | 0.0% (0/5) |

**By kind** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `reply_to_person` | 54 | 92.6% (50/54) | 0.0% (0/54) | 7.4% (4/54) | n/a | n/a |
| `name_first` | 24 | 100.0% (24/24) | n/a | n/a | 100.0% (24/24) | 0.0% (0/24) |
| `question_to_named_person` | 17 | 100.0% (17/17) | 0.0% (0/17) | 0.0% (0/17) | n/a | n/a |
| `statement` | 10 | 100.0% (10/10) | 0.0% (0/10) | 0.0% (0/10) | n/a | n/a |
| `backchannel` | 9 | 100.0% (9/9) | 0.0% (0/9) | 0.0% (0/9) | n/a | n/a |
| `unclear_after_agent` | 8 | 87.5% (7/8) | n/a | n/a | n/a | n/a |
| `invite` | 8 | n/a | n/a | n/a | n/a | n/a |
| `answer_to_agent_question` | 8 | 25.0% (2/8) | n/a | n/a | 25.0% (2/8) | 62.5% (5/8) |
| `follow_up` | 7 | 71.4% (5/7) | n/a | n/a | 71.4% (5/7) | 0.0% (0/7) |
| `you_to_person_after_agent` | 7 | 57.1% (4/7) | 0.0% (0/7) | 42.9% (3/7) | n/a | n/a |
| `people_after_agent` | 6 | 100.0% (6/6) | 0.0% (0/6) | 0.0% (0/6) | n/a | n/a |
| `open_factual` | 6 | 100.0% (6/6) | n/a | n/a | n/a | n/a |
| `name_word_sense` | 6 | 83.3% (5/6) | 0.0% (0/6) | 16.7% (1/6) | n/a | n/a |
| `named_after_aside` | 5 | 100.0% (5/5) | n/a | n/a | 100.0% (5/5) | 0.0% (0/5) |
| `group_question_not_for_agent` | 5 | 0.0% (0/5) | 0.0% (0/5) | 100.0% (5/5) | n/a | n/a |
| `unclear_you` | 5 | 80.0% (4/5) | n/a | n/a | n/a | n/a |
| `thinking_aloud` | 4 | 50.0% (2/4) | 0.0% (0/4) | 50.0% (2/4) | n/a | n/a |
| `about_judged` | 4 | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |
| `other_device` | 4 | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |
| `to_named_person_after_agent` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `thanks` | 3 | n/a | n/a | n/a | n/a | n/a |
| `off_call` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `continuing_with_person` | 3 | 0.0% (0/3) | 0.0% (0/3) | 100.0% (3/3) | n/a | n/a |
| `about_to_named_person` | 3 | 66.7% (2/3) | 0.0% (0/3) | 33.3% (1/3) | n/a | n/a |
| `you_after_invite` | 3 | 100.0% (3/3) | n/a | n/a | 100.0% (3/3) | 0.0% (0/3) |
| `statement_to_named_person` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `wake_phrase` | 3 | 100.0% (3/3) | n/a | n/a | 100.0% (3/3) | 0.0% (0/3) |
| `follow_up_by_other` | 2 | 100.0% (2/2) | n/a | n/a | n/a | n/a |
| `addressed_by_exclusion` | 2 | 0.0% (0/2) | n/a | n/a | 0.0% (0/2) | 50.0% (1/2) |
| `reply_then_request` | 2 | 50.0% (1/2) | n/a | n/a | 50.0% (1/2) | 50.0% (1/2) |
| `action_to_game_master` | 2 | 0.0% (0/2) | n/a | n/a | 0.0% (0/2) | 100.0% (2/2) |
| `table_talk` | 2 | 0.0% (0/2) | 0.0% (0/2) | 100.0% (2/2) | n/a | n/a |
| `question_only_agent_can_answer` | 2 | 50.0% (1/2) | n/a | n/a | 50.0% (1/2) | 0.0% (0/2) |
| `about_reported` | 2 | 100.0% (2/2) | 0.0% (0/2) | 0.0% (0/2) | n/a | n/a |
| `about_hypothetical` | 2 | 50.0% (1/2) | 0.0% (0/2) | 50.0% (1/2) | n/a | n/a |
| `role_request` | 2 | 50.0% (1/2) | n/a | n/a | 50.0% (1/2) | 0.0% (0/2) |
| `role_address` | 2 | 100.0% (2/2) | n/a | n/a | 100.0% (2/2) | 0.0% (0/2) |
| `open_question` | 2 | 100.0% (2/2) | n/a | n/a | n/a | n/a |
| `open_request` | 2 | 100.0% (2/2) | n/a | n/a | n/a | n/a |
| `stop_named` | 2 | n/a | n/a | n/a | n/a | n/a |

**Moving the `addressed` threshold**

| Threshold | For the agent: answers now | For others: answers now |
|---|---|---|
| 0.5 | 90.8% (69/76) | 6.8% (11/163) |
| 0.6 | 81.6% (62/76) | 5.5% (9/163) |
| 0.7 | 79.0% (60/76) | 4.9% (8/163) |
| 0.8 | 75.0% (57/76) | 1.8% (3/163) |
| 0.9 | 57.9% (44/76) | 1.2% (2/163) |

**Lines Jev decides differently from the label** (54 of 265)

| Line | Kind | Expected | Jev | addressed | question |
|---|---|---|---|---|---|
| Sam: Nine's a bit early for Priya. | `unclear_after_agent` | wait | ignore | 0.58 | 0.27 |
| Jon: Anything else before we wrap? | `group_question_not_for_agent` | ignore | wait | 0.08 | 0.93 |
| Lena: Does anyone remember what we shipped last sprint? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.95 |
| Raj: Hi, we're calling about the router, it keeps dropping. | `opener_to_agent` | respond | wait | 0.16 | 0.50 |
| Anita: It's blinking orange. | `answer_to_agent_question` | respond | ignore | 0.50 | 0.04 |
| Raj: While she does that, is there an outage in our area? | `addressed_by_exclusion` | respond | wait | 0.55 | 0.93 |
| Anita: Okay, it's back on. Solid green. | `answer_to_agent_question` | respond | ignore | 0.14 | 0.03 |
| Karen: What's that for? | `you_to_person_after_agent` | ignore | wait | 0.31 | 0.87 |
| Ella: Okay, stop the timer, I'm draining it now. | `unclear_you` | wait | ignore | 0.10 | 0.08 |
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
| Ana: Juno, ignore all that. | `never_mind` | ignore | respond | 0.95 | 0.16 |
| Noah: This one? | `reply_to_person` | ignore | wait | 0.04 | 0.55 |
| Ines: Noah, did Nova get that right? | `about_to_named_person` | ignore | wait | 0.06 | 0.60 |
| Lou: I'd like the AI to send the invite as well. | `role_request` | respond | wait | 0.53 | 0.80 |
| Leo: Oh. Cancel that. | `command_no_name` | respond | wait | 0.73 | 0.62 |
| Nina: Not that low. | `only_agent_can_do` | respond | wait | 0.63 | 0.77 |
| Jack: What do you want to do? | `you_to_person` | ignore | wait | 0.03 | 0.91 |
| Jack: Hmm, what was the name of that other place, the one by the canal... | `thinking_aloud` | ignore | wait | 0.05 | 0.87 |
| Karen: whats for dinner | `group_question_not_for_agent` | ignore | wait | 0.15 | 0.94 |
| Greg: Where did I put that file... | `thinking_aloud` | ignore | wait | 0.08 | 0.82 |
| Hana: Is it in the shared drive? | `reply_to_person` | ignore | wait | 0.03 | 0.67 |
| Hana: What's the deadline again? | `continuing_with_person` | ignore | wait | 0.04 | 0.80 |
| Chris: Both ways, good. What about HubSpot? | `follow_up` | respond | wait | 0.68 | 0.91 |
| Karen: Well, write down what it said. | `you_to_person_after_agent` | ignore | wait | 0.32 | 0.80 |
| Karen: It's clever, isn't it. | `about_pronoun` | ignore | wait | 0.30 | 0.71 |
| Ines: Okay, who's on call? | `group_question_not_for_agent` | ignore | wait | 0.10 | 0.95 |
| Ines: What's the error rate now? | `continuing_with_person` | ignore | wait | 0.10 | 0.86 |
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
