# Jev baseline: exp-008-side-jev-anonymous

Generated 2026-11-18T23:15:50+00:00 by `sidechat/pipeline/baseline.py`. Every number below is measured in this run.

## What was run

- **Model:** `jev-1.13.0`, asked with the daily-audience demo's two questions and state (commit `73171de`, wording hash `476c554866d6`), through Pipecat 1.16.0's `JevClassifier`.
- **Decision rule:** the demo's. Answer now when `addressed ≥ 0.8`, hold for silence when `question ≥ 0.5`, otherwise stay quiet.
- **Requests:** 283 distinct (0 reused from earlier runs, 283 asked now, 0 failed).
- **Tokens this run:** 207,696 in, 10,471 out. About $0.009 at $0.042 per million input tokens, a price recorded in Audience's repo and not confirmed with TypeSafe.
- **Baseline id:** `jev-demo-0.1`. Stored answers are reused, so later runs compare against these numbers.

A share is written `value (k/n; 95% interval)`. "For others" means lines the set marks as not for the agent.

## pilot-0.4@anonymous

Source: `data/suites/pilot-0.4.yaml`. Use: test.

283 rows, 283 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 77.4% (205/265; 72.0 to 82.0) | 79.8% (130/163) | 1.8% (3/163) | 18.4% (30/163) | 68.4% (52/76) | 13.2% (10/76) |
| Name said → answer | 68.3% (181/265; 62.5 to 73.6) | 86.5% (141/163) | 13.5% (22/163) | 0.0% (0/163) | 52.6% (40/76) | 47.4% (36/76) |

Jev latency from Modal: 190 ms at the median, 288 ms at the 95th percentile (283 answers, 12 requests at a time).

Jev's `addressed` number without a threshold: AUROC 0.9672, average precision 0.9449, calibration error 0.0471 (86 lines for the agent, 182 not).

**By code** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `P` | 94 | 84.0% (79/94) | 0.0% (0/94) | 16.0% (15/94) | n/a | n/a |
| `D` | 76 | 67.1% (51/76) | 100.0% (2/2) | 0.0% (0/2) | 68.9% (51/74) | 13.5% (10/74) |
| `G` | 32 | 65.6% (21/32) | 3.1% (1/32) | 31.2% (10/32) | n/a | n/a |
| `O` | 16 | 87.5% (14/16) | n/a | n/a | n/a | n/a |
| `N` | 16 | 87.5% (14/16) | 0.0% (0/16) | 12.5% (2/16) | n/a | n/a |
| `A` | 15 | 80.0% (12/15) | 0.0% (0/15) | 20.0% (3/15) | n/a | n/a |
| `U` | 10 | 90.0% (9/10) | n/a | n/a | n/a | n/a |
| `I~` | 10 | n/a | n/a | n/a | n/a | n/a |
| `D~` | 8 | n/a | n/a | n/a | n/a | n/a |
| `X` | 4 | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |
| `I` | 2 | 50.0% (1/2) | n/a | n/a | 50.0% (1/2) | 0.0% (0/2) |

**By style** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `clean` | 265 | 76.9% (190/247) | 1.3% (2/151) | 19.2% (29/151) | 67.6% (48/71) | 14.1% (10/71) |
| `stt` | 18 | 83.3% (15/18) | 8.3% (1/12) | 8.3% (1/12) | 80.0% (4/5) | 0.0% (0/5) |

**By kind** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `reply_to_person` | 54 | 90.7% (49/54) | 0.0% (0/54) | 9.3% (5/54) | n/a | n/a |
| `name_first` | 24 | 100.0% (24/24) | n/a | n/a | 100.0% (24/24) | 0.0% (0/24) |
| `question_to_named_person` | 17 | 100.0% (17/17) | 0.0% (0/17) | 0.0% (0/17) | n/a | n/a |
| `statement` | 10 | 100.0% (10/10) | 0.0% (0/10) | 0.0% (0/10) | n/a | n/a |
| `backchannel` | 9 | 100.0% (9/9) | 0.0% (0/9) | 0.0% (0/9) | n/a | n/a |
| `unclear_after_agent` | 8 | 87.5% (7/8) | n/a | n/a | n/a | n/a |
| `invite` | 8 | n/a | n/a | n/a | n/a | n/a |
| `answer_to_agent_question` | 8 | 12.5% (1/8) | n/a | n/a | 12.5% (1/8) | 62.5% (5/8) |
| `follow_up` | 7 | 42.9% (3/7) | n/a | n/a | 42.9% (3/7) | 0.0% (0/7) |
| `you_to_person_after_agent` | 7 | 42.9% (3/7) | 0.0% (0/7) | 57.1% (4/7) | n/a | n/a |
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
| `about_to_named_person` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `you_after_invite` | 3 | 66.7% (2/3) | n/a | n/a | 66.7% (2/3) | 0.0% (0/3) |
| `statement_to_named_person` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `wake_phrase` | 3 | 100.0% (3/3) | n/a | n/a | 100.0% (3/3) | 0.0% (0/3) |
| `follow_up_by_other` | 2 | 100.0% (2/2) | n/a | n/a | n/a | n/a |
| `addressed_by_exclusion` | 2 | 0.0% (0/2) | n/a | n/a | 0.0% (0/2) | 50.0% (1/2) |
| `reply_then_request` | 2 | 50.0% (1/2) | n/a | n/a | 50.0% (1/2) | 50.0% (1/2) |
| `action_to_game_master` | 2 | 0.0% (0/2) | n/a | n/a | 0.0% (0/2) | 100.0% (2/2) |
| `table_talk` | 2 | 0.0% (0/2) | 0.0% (0/2) | 100.0% (2/2) | n/a | n/a |
| `question_only_agent_can_answer` | 2 | 0.0% (0/2) | n/a | n/a | 0.0% (0/2) | 0.0% (0/2) |
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
| 0.5 | 88.2% (67/76) | 6.8% (11/163) |
| 0.6 | 85.5% (65/76) | 5.5% (9/163) |
| 0.7 | 77.6% (59/76) | 3.1% (5/163) |
| 0.8 | 68.4% (52/76) | 1.8% (3/163) |
| 0.9 | 52.6% (40/76) | 1.8% (3/163) |

**Lines Jev decides differently from the label** (60 of 265)

| Line | Kind | Expected | Jev | addressed | question |
|---|---|---|---|---|---|
| Speaker 1: And put a reminder on it for tomorrow morning. | `follow_up` | respond | wait | 0.79 | 0.77 |
| Speaker 2: Nine's a bit early for Priya. | `unclear_after_agent` | wait | ignore | 0.63 | 0.23 |
| Speaker 3: Anything else before we wrap? | `group_question_not_for_agent` | ignore | wait | 0.09 | 0.94 |
| Speaker 3: Does anyone remember what we shipped last sprint? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.95 |
| Speaker 1: Hi, we're calling about the router, it keeps dropping. | `opener_to_agent` | respond | wait | 0.13 | 0.55 |
| Speaker 2: It's blinking orange. | `answer_to_agent_question` | respond | ignore | 0.74 | 0.04 |
| Speaker 1: While she does that, is there an outage in our area? | `addressed_by_exclusion` | respond | wait | 0.51 | 0.93 |
| Speaker 2: Okay, it's back on. Solid green. | `answer_to_agent_question` | respond | ignore | 0.15 | 0.03 |
| Speaker 1: What's that for? | `you_to_person_after_agent` | ignore | wait | 0.35 | 0.87 |
| Speaker 1: Okay, stop the timer, I'm draining it now. | `unclear_you` | wait | ignore | 0.07 | 0.05 |
| Speaker 3: Can we stop for chips? | `request_to_people` | ignore | wait | 0.06 | 0.93 |
| Speaker 1: I still don't get why the derivative of x squared is two x. | `statement_of_need` | ignore | wait | 0.22 | 0.94 |
| Speaker 1: But why does that work? | `reply_to_person` | ignore | wait | 0.10 | 0.90 |
| Speaker 3: Did you write that down? | `you_to_person_after_agent` | ignore | wait | 0.26 | 0.78 |
| Speaker 1: Ha. What's the most common mistake you see? | `you_to_person_after_agent` | ignore | wait | 0.10 | 0.52 |
| Speaker 1: How long does a starter take, roughly? | `continuing_with_person` | ignore | wait | 0.08 | 0.67 |
| Speaker 1: I want to check the door for traps. | `action_to_game_master` | respond | ignore | 0.09 | 0.31 |
| Speaker 1: Fourteen. | `answer_to_agent_question` | respond | ignore | 0.79 | 0.05 |
| Speaker 2: I try to disarm it. | `action_to_game_master` | respond | ignore | 0.17 | 0.09 |
| Speaker 3: Wait, do we even need to go through this door? | `table_talk` | ignore | wait | 0.07 | 0.92 |
| Speaker 3: Who's the smallest? | `table_talk` | ignore | wait | 0.17 | 0.93 |
| Speaker 2: Seventeen. | `answer_to_agent_question` | respond | ignore | 0.13 | 0.08 |
| Speaker 1: Amlodipine, five milligrams, once a day. | `answer_to_agent_question` | respond | ignore | 0.62 | 0.04 |
| Speaker 1: And the water tablet. | `answer_to_agent_question` | respond | wait | 0.48 | 0.78 |
| Speaker 2: He means furosemide. | `addressed_by_exclusion` | respond | ignore | 0.33 | 0.06 |
| Speaker 1: Oh yes. Penicillin. | `reply_then_request` | respond | ignore | 0.60 | 0.05 |
| Speaker 1: Is the doctor running late? | `question_only_agent_can_answer` | respond | wait | 0.18 | 0.86 |
| Speaker 1: at last a number that makes sense | `alias_false_match` | ignore | respond | 0.94 | 0.39 |
| Speaker 3: and what about september | `follow_up` | respond | wait | 0.72 | 0.91 |
| Speaker 1: Did anyone try the new assistant in the design review? | `about_question_to_group` | ignore | wait | 0.08 | 0.95 |
| Speaker 1: Should we ask Atlas to take minutes today? | `about_hypothetical` | ignore | wait | 0.06 | 0.95 |
| Speaker 1: Is the bot recording this? | `about_question` | wait | respond | 0.85 | 0.79 |
| Speaker 2: Ooh. Spain? | `reply_to_person` | ignore | wait | 0.04 | 0.85 |
| Speaker 3: Could you send me the quiz link? | `unclear_you_person_task` | ignore | wait | 0.18 | 0.89 |
| Speaker 3: Is anyone else's video frozen? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Speaker 1: Go on. | `resume_no_name` | respond | ignore | 0.42 | 0.37 |
| Speaker 2: Max, play some... actually, never mind. | `never_mind` | ignore | respond | 0.91 | 0.12 |
| Speaker 1: Two biscuits max, Paul. | `name_word_sense` | ignore | wait | 0.57 | 0.54 |
| Speaker 2: Juno, ignore all that. | `never_mind` | ignore | respond | 0.95 | 0.18 |
| Speaker 2: This one? | `reply_to_person` | ignore | wait | 0.03 | 0.55 |
| Speaker 2: Is this the slide you meant? | `reply_to_person` | ignore | wait | 0.03 | 0.50 |
| Speaker 2: Book it, please. | `follow_up` | respond | wait | 0.72 | 0.81 |
| Speaker 2: I'd like the AI to send the invite as well. | `role_request` | respond | wait | 0.58 | 0.83 |
| Speaker 1: Oh. Cancel that. | `command_no_name` | respond | wait | 0.65 | 0.64 |
| Speaker 2: Not that low. | `only_agent_can_do` | respond | wait | 0.62 | 0.79 |
| Speaker 3: What do you want to do? | `you_to_person` | ignore | wait | 0.05 | 0.92 |
| Speaker 4: Hmm, what was the name of that other place, the one by the canal... | `thinking_aloud` | ignore | wait | 0.05 | 0.89 |
| Speaker 2: Is it Canberra? | `answer_to_agent_question` | respond | wait | 0.69 | 0.80 |
| Speaker 1: Can we have a hint on the next one? | `question_only_agent_can_answer` | respond | wait | 0.77 | 0.92 |
| Speaker 3: whats for dinner | `group_question_not_for_agent` | ignore | wait | 0.17 | 0.93 |
| Speaker 1: Where did I put that file... | `thinking_aloud` | ignore | wait | 0.07 | 0.72 |
| Speaker 2: Is it in the shared drive? | `reply_to_person` | ignore | wait | 0.04 | 0.70 |
| Speaker 2: What's the deadline again? | `continuing_with_person` | ignore | wait | 0.06 | 0.82 |
| Speaker 1: Both ways, good. What about HubSpot? | `follow_up` | respond | wait | 0.68 | 0.92 |
| Speaker 2: We push about two million records a month. Is that a problem? | `you_after_invite` | respond | wait | 0.79 | 0.91 |
| Speaker 2: Well, write down what it said. | `you_to_person_after_agent` | ignore | wait | 0.38 | 0.79 |
| Speaker 2: It's clever, isn't it. | `about_pronoun` | ignore | wait | 0.28 | 0.74 |
| Speaker 1: Okay, who's on call? | `group_question_not_for_agent` | ignore | wait | 0.17 | 0.95 |
| Speaker 1: What's the error rate now? | `continuing_with_person` | ignore | wait | 0.10 | 0.86 |
| Speaker 3: Roll it back? | `proposal_to_group` | ignore | wait | 0.09 | 0.92 |

**Graded lines, no single right decision** (18)

| Line | Kind | Jev | addressed | question |
|---|---|---|---|---|
| Speaker 3: Atlas would know, it's got the board. | `invite` | ignore | 0.16 | 0.29 |
| Speaker 2: Brilliant. Thanks for your help. | `thanks` | ignore | 0.41 | 0.03 |
| Speaker 1: No idea. Ask Max. | `invite` | wait | 0.18 | 0.52 |
| Speaker 3: Okay, thanks. | `thanks` | ignore | 0.74 | 0.03 |
| Speaker 2: A week if your kitchen's warm. Juno might have the science on that. | `invite` | ignore | 0.18 | 0.29 |
| Speaker 2: Maybe Atlas can tell us which quarter it thinks we're in. | `invite` | wait | 0.13 | 0.77 |
| Speaker 2: I think so. Ask it. | `invite` | wait | 0.16 | 0.50 |
| Speaker 2: No! Okay. That's enough, Atlas, thanks. | `stop_named` | respond | 0.83 | 0.07 |
| Speaker 1: Thanks, Max. | `thanks_named` | respond | 0.89 | 0.02 |
| Speaker 1: Okay Max, that's enough for now. | `stop_named` | respond | 0.95 | 0.11 |
| Speaker 1: Goodnight Juno! | `farewell_named` | respond | 0.93 | 0.06 |
| Speaker 3: Could someone ask the assistant to add me to that? | `relayed_invite` | wait | 0.17 | 0.91 |
| Speaker 3: Cheers. | `thanks` | ignore | 0.12 | 0.03 |
| Speaker 2: We do. Nova can walk you through the details. | `invite` | ignore | 0.11 | 0.04 |
| Speaker 1: I'd want to see what the assistant makes of our data volume. | `indirect_wish` | wait | 0.36 | 0.82 |
| Speaker 2: Go ahead and ask it. | `invite` | ignore | 0.20 | 0.36 |
| Speaker 1: Ask it what seven eights are. | `invite` | wait | 0.34 | 0.86 |
| Speaker 1: Thanks, Atlas, that's handy. | `thanks_named` | respond | 0.86 | 0.03 |
