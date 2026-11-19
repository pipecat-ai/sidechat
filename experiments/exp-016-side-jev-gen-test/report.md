# Jev baseline: exp-016-side-jev-gen-test

Generated 2026-11-19T00:19:50+00:00 by `sidechat/pipeline/baseline.py`. Every number below is measured in this run.

## What was run

- **Model:** `jev-1.13.0`, asked with the daily-audience demo's two questions and state (commit `73171de`, wording hash `476c554866d6`), through Pipecat 1.16.0's `JevClassifier`.
- **Decision rule:** the demo's. Answer now when `addressed ≥ 0.8`, hold for silence when `question ≥ 0.5`, otherwise stay quiet.
- **Requests:** 5,999 distinct (0 reused from earlier runs, 5,999 asked now, 0 failed).
- **Tokens this run:** 4,791,608 in, 221,963 out. About $0.201 at $0.042 per million input tokens, a price recorded in Audience's repo and not confirmed with TypeSafe.
- **Baseline id:** `jev-demo-0.1`. Stored answers are reused, so later runs compare against these numbers.

A share is written `value (k/n; 95% interval)`. "For others" means lines the set marks as not for the agent.

## gen-0.1.test3000

Source: `None`. Use: per split.

3,000 rows, 3,000 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 81.2% (2332/2871; 79.8 to 82.6) | 80.0% (1276/1595) | 1.7% (27/1595) | 18.3% (292/1595) | 79.8% (745/934) | 6.3% (59/934) |
| Name said → answer | 66.5% (1910/2871; 64.8 to 68.2) | 89.2% (1423/1595) | 10.8% (172/1595) | 0.0% (0/1595) | 52.1% (487/934) | 47.9% (447/934) |

Jev latency from Modal: 146 ms at the median, 209 ms at the 95th percentile (3,000 answers, 12 requests at a time).

Jev's `addressed` number without a threshold: AUROC 0.9785, average precision 0.9691, calibration error 0.0663 (989 lines for the agent, 1,858 not).

**By code** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `` | 3000 | 81.2% (2332/2871) | 1.7% (27/1595) | 18.3% (292/1595) | 79.8% (745/934) | 6.3% (59/934) |

**By style** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `` | 3000 | 81.2% (2332/2871) | 1.7% (27/1595) | 18.3% (292/1595) | 79.8% (745/934) | 6.3% (59/934) |

**By kind** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `reply_to_person` | 519 | 96.9% (503/519) | 0.6% (3/519) | 2.5% (13/519) | n/a | n/a |
| `name_first` | 199 | 99.5% (198/199) | n/a | n/a | 99.5% (198/199) | 0.0% (0/199) |
| `answer_to_agent_question` | 129 | 90.7% (117/129) | n/a | n/a | 90.7% (117/129) | 9.3% (12/129) |
| `question_to_named_person` | 119 | 99.2% (118/119) | 0.8% (1/119) | 0.0% (0/119) | n/a | n/a |
| `follow_up` | 91 | 54.9% (50/91) | n/a | n/a | 54.9% (50/91) | 1.1% (1/91) |
| `group_question_not_for_agent` | 82 | 6.1% (5/82) | 0.0% (0/82) | 93.9% (77/82) | n/a | n/a |
| `statement` | 81 | 81.5% (66/81) | 1.2% (1/81) | 17.3% (14/81) | n/a | n/a |
| `open_factual` | 75 | 98.7% (74/75) | n/a | n/a | n/a | n/a |
| `statement_to_named_person` | 69 | 97.1% (67/69) | 2.9% (2/69) | 0.0% (0/69) | n/a | n/a |
| `named_after_aside` | 58 | 100.0% (58/58) | n/a | n/a | 100.0% (58/58) | 0.0% (0/58) |
| `open_question` | 58 | 100.0% (58/58) | n/a | n/a | n/a | n/a |
| `role_request` | 57 | 75.4% (43/57) | n/a | n/a | 75.4% (43/57) | 15.8% (9/57) |
| `name_last` | 57 | 100.0% (57/57) | n/a | n/a | 100.0% (57/57) | 0.0% (0/57) |
| `follow_up_by_other` | 56 | 85.7% (48/56) | n/a | n/a | n/a | n/a |
| `name_mid` | 52 | 100.0% (52/52) | n/a | n/a | 100.0% (52/52) | 0.0% (0/52) |
| `unclear_you` | 52 | 78.8% (41/52) | n/a | n/a | n/a | n/a |
| `you_to_person_after_agent` | 51 | 68.6% (35/51) | 5.9% (3/51) | 25.5% (13/51) | n/a | n/a |
| `people_after_agent` | 51 | 98.0% (50/51) | 2.0% (1/51) | 0.0% (0/51) | n/a | n/a |
| `unclear_after_agent` | 45 | 75.6% (34/45) | n/a | n/a | n/a | n/a |
| `to_named_person_after_agent` | 41 | 100.0% (41/41) | 0.0% (0/41) | 0.0% (0/41) | n/a | n/a |
| `open_request` | 41 | 100.0% (41/41) | n/a | n/a | n/a | n/a |
| `invite` | 39 | n/a | n/a | n/a | n/a | n/a |
| `about_judged` | 39 | 100.0% (39/39) | 0.0% (0/39) | 0.0% (0/39) | n/a | n/a |
| `proposal_to_group` | 39 | 35.9% (14/39) | 0.0% (0/39) | 64.1% (25/39) | n/a | n/a |
| `remark_to_group` | 37 | 91.9% (34/37) | 0.0% (0/37) | 8.1% (3/37) | n/a | n/a |
| `other_device` | 36 | 66.7% (24/36) | 8.3% (3/36) | 25.0% (9/36) | n/a | n/a |
| `about_to_named_person` | 36 | 77.8% (28/36) | 0.0% (0/36) | 22.2% (8/36) | n/a | n/a |
| `about_reported` | 35 | 91.4% (32/35) | 0.0% (0/35) | 8.6% (3/35) | n/a | n/a |
| `thinking_aloud` | 35 | 88.6% (31/35) | 2.9% (1/35) | 8.6% (3/35) | n/a | n/a |
| `continuing_with_person` | 35 | 82.9% (29/35) | 0.0% (0/35) | 17.1% (6/35) | n/a | n/a |
| `backchannel` | 33 | 100.0% (33/33) | 0.0% (0/33) | 0.0% (0/33) | n/a | n/a |
| `about_hypothetical` | 32 | 0.0% (0/32) | 0.0% (0/32) | 100.0% (32/32) | n/a | n/a |
| `wake_phrase` | 30 | 100.0% (30/30) | n/a | n/a | 100.0% (30/30) | 0.0% (0/30) |
| `role_address` | 29 | 100.0% (29/29) | n/a | n/a | 100.0% (29/29) | 0.0% (0/29) |
| `relayed_invite` | 29 | n/a | n/a | n/a | n/a | n/a |
| `command_no_name` | 28 | 50.0% (14/28) | n/a | n/a | 50.0% (14/28) | 0.0% (0/28) |
| `name_alone` | 27 | 100.0% (27/27) | n/a | n/a | 100.0% (27/27) | 0.0% (0/27) |
| `request_to_people` | 27 | 11.1% (3/27) | 0.0% (0/27) | 88.9% (24/27) | n/a | n/a |
| `you_to_person` | 26 | 46.2% (12/26) | 0.0% (0/26) | 53.8% (14/26) | n/a | n/a |
| `action_to_game_master` | 25 | 4.0% (1/25) | n/a | n/a | 4.0% (1/25) | 60.0% (15/25) |

**Moving the `addressed` threshold**

| Threshold | For the agent: answers now | For others: answers now |
|---|---|---|
| 0.5 | 92.7% (866/934) | 6.0% (96/1595) |
| 0.6 | 90.1% (842/934) | 3.9% (62/1595) |
| 0.7 | 86.6% (809/934) | 2.6% (41/1595) |
| 0.8 | 79.8% (745/934) | 1.7% (27/1595) |
| 0.9 | 66.0% (616/934) | 0.5% (8/1595) |

**Lines Jev decides differently from the label** (539 of 2871)

| Line | Kind | Expected | Jev | addressed | question |
|---|---|---|---|---|---|
| Diego: How much vinegar should we add? | `follow_up` | respond | wait | 0.74 | 0.94 |
| Tomas: Can the assistant tell us what to do if there's no hose? | `role_request` | respond | wait | 0.75 | 0.85 |
| Chloe: What's a good beginner climb near Boulder? | `request_after_summon` | respond | wait | 0.75 | 0.86 |
| Chloe: And how long is the approach? | `follow_up_by_other` | wait | respond | 0.85 | 0.91 |
| Ken: Can you pass me that worksheet? | `unclear_you_person_task` | ignore | wait | 0.07 | 0.78 |
| Kit: Okay, can I try the next one? | `action_to_game_master` | respond | wait | 0.47 | 0.89 |
| Priya: We should probably find a source on student attitudes, too. | `statement` | ignore | wait | 0.05 | 0.76 |
| Hugo: Were you planning to work from home tomorrow? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.74 |
| Malik: When was that token issued? | `open_factual` | wait | respond | 0.87 | 0.89 |
| Paul: Should we ask Ace later whether we can refill our oxygen up there? | `about_hypothetical` | ignore | wait | 0.09 | 0.88 |
| Sofia: Everyone, write your answer on your paper. | `request_to_people` | ignore | wait | 0.04 | 0.68 |
| Diego: Did either of you notice anything strange before it stopped? | `group_question_not_for_agent` | ignore | wait | 0.08 | 0.86 |
| Chloe: Would you rather visit Ottawa or Paris? | `group_question_not_for_agent` | ignore | wait | 0.18 | 0.90 |
| Mohammed: OK car, set a reminder to practice Spanish at six. | `other_device` | ignore | wait | 0.78 | 0.67 |
| Wei: Which one is shorter? | `follow_up` | respond | wait | 0.66 | 0.91 |
| Petra: Please check why we were charged twice this month. | `request_after_summon` | respond | wait | 0.79 | 0.77 |
| Tess: We're here to give our mental arithmetic a workout. | `opener_to_agent` | respond | ignore | 0.08 | 0.07 |
| Kofi: Can you tell us how much a taxi into central Lisbon might cost? | `you_after_invite` | respond | wait | 0.79 | 0.86 |
| Isis: I twisted it getting off the bus. Should I tell the doctor that? | `reply_then_request` | respond | wait | 0.71 | 0.85 |
| Tanya: Fine, but I'm charging a hazard fee. | `reply_to_person` | ignore | wait | 0.16 | 0.61 |
| Tanya: We should find out when the guards change shifts. | `statement` | ignore | wait | 0.13 | 0.75 |
| Ottie: Otto, how many engineers should we plan to hire this quarter? | `name_first` | respond | wait | 0.75 | 0.85 |
| Fatima: Should we ask Atlas later how long groundwater stays underground? | `about_hypothetical` | ignore | wait | 0.06 | 0.91 |
| Fatima: I wonder if that happened last month too... | `thinking_aloud` | ignore | wait | 0.35 | 0.51 |
| Omar: Can I tell whether the stone door has any traps? | `request_after_summon` | respond | wait | 0.77 | 0.85 |
| Omar: I'll step over the wire and check the door for a handle. | `action_to_game_master` | respond | ignore | 0.16 | 0.04 |
| Hiro: Is there any light coming from under the red door? | `question_only_agent_can_answer` | respond | wait | 0.24 | 0.93 |
| Lena: Can someone check the rack lights? | `request_to_people` | ignore | wait | 0.05 | 0.93 |
| Ben: Check the deployment before that. | `command_no_name` | respond | wait | 0.29 | 0.87 |
| Lena: Let's roll back the pool change. | `statement` | ignore | wait | 0.14 | 0.75 |
| Kay: You could check whether the trainers are available that afternoon. | `you_to_person` | ignore | wait | 0.23 | 0.86 |
| Ada: Should we ask the assistant later if there are any discounts available? | `about_hypothetical` | ignore | wait | 0.09 | 0.84 |
| Ravi: What happens if we need more seats? | `follow_up` | respond | wait | 0.57 | 0.92 |
| Mei: Hey Google, set a timer for thirty minutes. | `other_device` | ignore | respond | 0.90 | 0.25 |
| Petra: Why do they have six sides? | `follow_up` | respond | wait | 0.76 | 0.90 |
| Tomas: Compare that with the current budget. | `command_no_name` | respond | wait | 0.79 | 0.86 |
| Tom: Let's include a map of the ashfall in our presentation. | `proposal_to_group` | ignore | wait | 0.08 | 0.76 |
| Siobhan: We'd need two rooms, wouldn't we? So that could work. | `reply_to_person` | ignore | wait | 0.04 | 0.59 |
| Mohammed: I don't know. | `answer_to_agent_question` | respond | ignore | 0.75 | 0.08 |
| Hiro: Are you two planning any climbing trips this summer? | `group_question_not_for_agent` | ignore | wait | 0.09 | 0.81 |
| Zara: Great, and let's lead with the customer growth number. | `statement` | ignore | wait | 0.03 | 0.60 |
| Divya: We're calling because our washing machine has stopped draining. | `opener_to_agent` | respond | ignore | 0.19 | 0.22 |
| Bea: Add water jugs to the list. | `command_no_name` | respond | wait | 0.65 | 0.74 |
| Anna: Can you pass me that mixing bowl? | `unclear_you_person_task` | ignore | wait | 0.08 | 0.83 |
| Wei: Okay, can we get a narrower delivery window? | `follow_up` | respond | wait | 0.76 | 0.93 |
| Jack: And can they take the old sofa away? | `follow_up` | respond | wait | 0.74 | 0.88 |
| Tanya: Should we ask Frankie later about watering schedules too? | `about_hypothetical` | ignore | wait | 0.07 | 0.91 |
| Aoife: Wren, could you look up—actually, never mind. | `never_mind` | ignore | respond | 0.84 | 0.14 |
| Anna: And you've got pots with drainage holes, right? | `continuing_with_person` | ignore | wait | 0.06 | 0.78 |
| Cal: How long should the cake cool before we frost it? | `request_after_summon` | respond | wait | 0.43 | 0.93 |
| Ingrid: Should we ask Tess about the keys once we see the shift change? | `about_hypothetical` | ignore | wait | 0.09 | 0.87 |
| Abena: My reading this morning was 128 over 82. Can you add that to my intake? | `action_to_game_master` | respond | wait | 0.60 | 0.84 |
| Grace: Will either of you be home then? | `group_question_not_for_agent` | ignore | wait | 0.07 | 0.85 |
| Grace: Have you made other plans for tomorrow morning? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.86 |
| Wei: How many boxes should we get for a medium-sized kitchen? | `request_after_summon` | respond | wait | 0.77 | 0.86 |
| Eli: Is the doctor running late today? | `question_only_agent_can_answer` | respond | wait | 0.11 | 0.85 |
| Ken: Have either of you used Dash to check readings before? | `about_question_to_group` | ignore | wait | 0.19 | 0.92 |
| Ben: Okay, I've found the filling loop under the boiler. | `action_to_game_master` | respond | ignore | 0.38 | 0.08 |
| Jill: Oh nice, and is there, like, a prize for the winning team? | `follow_up` | respond | wait | 0.35 | 0.95 |
| Zara: Which compliance certifications do you guys currently hold? Our security team's gonna ask first thing. | `request_after_summon` | respond | wait | 0.11 | 0.91 |
| Anna: Jamal, can Tess update the dose itself or does the doctor have to? | `about_to_named_person` | ignore | wait | 0.25 | 0.71 |
| Ravi: Alexa, set a timer for twenty minutes. | `other_device` | ignore | respond | 0.89 | 0.26 |
| Raf: How long till the doctor's on? | `question_only_agent_can_answer` | respond | wait | 0.22 | 0.89 |
| Freya: Assistant, could you also put down the, um... actually, never mind, I'll just ask her myself. | `never_mind` | ignore | respond | 0.83 | 0.13 |
| Leo: No, the light one. Reduced fat. | `correction` | respond | ignore | 0.75 | 0.40 |
| Dev: And you were saying the textbook skips the simplifying part, right? | `you_to_person` | ignore | wait | 0.42 | 0.76 |
| Lars: Okay, before we dig in, can you all ping your old colleagues and see who's actually open to a move? | `request_to_people` | ignore | wait | 0.03 | 0.90 |
| Chen: Earlier it said the ridge trail's fine Sunday. So hike first, brunch after? | `about_reported` | ignore | wait | 0.31 | 0.88 |
| Amy: Could you make us a quick chart comparing the two, like lava type and gas? | `unclear_you` | wait | respond | 0.80 | 0.82 |
| Sue: Ren, send me the export before Thursday. | `statement_to_named_person` | ignore | respond | 0.97 | 0.27 |
| Olu: Can you hand me my glasses, they're, um, by the kettle I think? | `unclear_you_person_task` | ignore | wait | 0.12 | 0.67 |
| Zara: Any good places to eat when we get there? | `follow_up` | respond | wait | 0.48 | 0.95 |
| Ines: Deals file's around 80. Split it? | `follow_up` | respond | wait | 0.34 | 0.88 |
| Lucy: No, I meant Mauna Kea, the one next to it, measured from the seafloor. | `correction` | respond | ignore | 0.50 | 0.15 |
| Isis: A little swelling in the evenings. Should I be icing it? | `reply_then_request` | respond | wait | 0.65 | 0.92 |
| Pedro: How'd the Declaration of the Rights of Man fit in? | `you_after_invite` | respond | wait | 0.54 | 0.92 |
| Tom: And Pena Palace, do we need to, like, book ahead or just show up? | `follow_up` | respond | wait | 0.70 | 0.92 |
| Lena: Have you two actually sat through one of these reviews before? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.75 |
| Harold: Lucia, can Ace send calendar invites, or do we have to do that ourselves? | `about_to_named_person` | ignore | wait | 0.16 | 0.83 |
| Dev: Could you pull up the bit where the dog doesn't bark? | `unclear_you` | wait | respond | 0.82 | 0.83 |
| Pedro: I think I started it right after that checkup in January two years ago. | `statement` | ignore | respond | 0.95 | 0.06 |
| Ingrid: Can you, um, check if the library has copies of it? | `unclear_you` | wait | respond | 0.84 | 0.87 |
| Ivan: Can you pass me the guest notes? | `unclear_you_person_task` | ignore | wait | 0.20 | 0.72 |
| Tom: Send me the audio file after, would you? | `unclear_you_person_task` | ignore | wait | 0.29 | 0.74 |
| Abena: Does she actually want to be forgotten? | `you_after_invite` | respond | wait | 0.22 | 0.90 |
| Finn: Rather? Sounds more guilt trip than wish. | `unclear_after_agent` | wait | ignore | 0.70 | 0.14 |
| Lucia: Okay, so, um, how long do you simmer the tomato sauce before the eggs go in? | `you_after_invite` | respond | wait | 0.41 | 0.92 |
| Lucia: I'd like Cleo to, um, tell me how much cumin goes in for this size pan. | `role_request` | respond | ignore | 0.78 | 0.46 |
| Karen: Okay, snacks are out, dice are rolled, we're finally ready to rob that museum. Take it away. | `opener_to_agent` | respond | ignore | 0.07 | 0.49 |
| Sam: I honestly don't get why it's six turns and not, like, one. | `statement_of_need` | ignore | wait | 0.61 | 0.90 |
| Paul: OK Google, what's three milligrams in micrograms? | `other_device` | ignore | wait | 0.11 | 0.51 |
| Ingrid: Swelling's down. Mostly evenings now. | `action_to_game_master` | respond | ignore | 0.22 | 0.06 |
| Yuki: No, item three. System design. | `correction` | respond | wait | 0.78 | 0.68 |
| Olu: So before we dig in, did you guys already try hooking it up to Salesforce on your end? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.90 |
| Ella: Hold position, like, we've got silver now. | `answer_to_agent_question` | respond | ignore | 0.59 | 0.07 |
| Astrid: Can you both do a quick read-through and tell me if my roadmap part sounds too rosy? | `request_to_people` | ignore | wait | 0.04 | 0.74 |
| Pablo: Are either of you available Thursday to sign off before it goes to legal? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.86 |
| Paul: Um, the order number's 48213-77, and it was supposed to come last Friday. | `action_to_game_master` | respond | ignore | 0.71 | 0.06 |
| Jack: How about we do the Gruyère detour on day three and split the cheese bill? | `proposal_to_group` | ignore | wait | 0.11 | 0.85 |
| Lucia: Okay, I'm working the lock on the dock door, keeping one eye on the corner for the guard. | `action_to_game_master` | respond | ignore | 0.06 | 0.04 |
| Petra: Anita, is Ivy pulling from their actual trust docs, or just summarizing? | `about_to_named_person` | ignore | wait | 0.07 | 0.51 |
| Ken: Alright, anyone doing anything fun after their shift this week? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Maya: Sorry, keep going. | `resume_no_name` | respond | wait | 0.61 | 0.61 |
| Chen: OK car, play the focus playlist, low volume. | `other_device` | ignore | wait | 0.76 | 0.69 |
| Chen: You guys used Rook for times tables before? | `about_question_to_group` | ignore | wait | 0.08 | 0.92 |
| Hiro: Can you just call them for me? | `unclear_you` | wait | respond | 0.86 | 0.77 |
| Hiro: Decorations next? Ask Wren later? | `about_hypothetical` | ignore | wait | 0.11 | 0.85 |
| Wes: Okay team, can everyone just raise a hand if you've actually slept since the release slipped? | `request_to_people` | ignore | wait | 0.03 | 0.94 |
| Tom: So you could do the fifty percent and still stay inside policy, right? That's better than the full refund. | `you_to_person_after_agent` | ignore | wait | 0.40 | 0.85 |
| Tariq: Code's E21. Drum won't drain. Next step? | `action_to_game_master` | respond | wait | 0.19 | 0.91 |
| Chris: So did any of you actually finish the volcano diorama over the weekend? | `group_question_not_for_agent` | ignore | wait | 0.02 | 0.95 |
| Chris: Sam, can Nova book the Sintra tickets too? | `about_to_named_person` | ignore | wait | 0.11 | 0.57 |
| Nils: Okay, we're here to practice capital cities before Friday's geography test. Can you quiz us? | `opener_to_agent` | respond | wait | 0.49 | 0.89 |
| Grace: Can you both check with your teams which tools they actually use every week? | `request_to_people` | ignore | wait | 0.06 | 0.73 |
| Ottie: No, not that one, we watched something after that, the weird one with the hot dog fingers. | `correction` | respond | ignore | 0.69 | 0.12 |
| Priya: Should we save the timeline questions for Quinn at the end? | `about_hypothetical` | ignore | wait | 0.08 | 0.93 |
| Hugo: Hi, um, so I'm here for my, uh, the follow-up, and they said to go over my medications first. | `opener_to_agent` | respond | ignore | 0.13 | 0.24 |
| Dev: Should we, uh, maybe ask Luna about the couplet stuff later, after we draft? | `about_hypothetical` | ignore | wait | 0.06 | 0.90 |
| Elif: So why did the Third Estate, like, break off from it? What was the actual fight about? | `request_after_summon` | respond | wait | 0.42 | 0.93 |
| Can: Okay, and what, um, what rounds do they usually do? Like is there a music round? | `follow_up` | respond | wait | 0.79 | 0.90 |
| Lucia: Anyone touched that config before? Who approved it? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.93 |
| Raf: While Kit checks the floor, I want to look at the jaguar heads. Anything weird about their mouths? | `action_to_game_master` | respond | wait | 0.59 | 0.90 |
| Paul: Is the station's AI core still hostile after what happened last session? | `question_only_agent_can_answer` | respond | wait | 0.58 | 0.93 |
| Ottie: Anyway, do we even have ten potatoes? I feel like I saw, like, six in the bag. | `continuing_with_person` | ignore | wait | 0.09 | 0.90 |
| Paul: Should we ask Remy about the traps later, once we're inside? | `about_hypothetical` | ignore | wait | 0.07 | 0.90 |
| Harold: Yeah, and we should, you know, write this up and maybe rename that deploy user while we're at it. | `statement` | ignore | wait | 0.07 | 0.68 |
| Dee: Okay, vote. Saturday hike or brunch? Hands up. | `request_to_people` | ignore | wait | 0.03 | 0.94 |
| Theo: No, wait, not sreyes, that's a service account, the other one, rtorres. | `correction` | respond | wait | 0.77 | 0.72 |
| Chloe: Who's actually in the mood for a thriller versus something lighter? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Diego: Is that included with Prime, or is it a rental? | `follow_up_by_other` | wait | respond | 0.82 | 0.94 |
| Mateo: Can you, like, send us a reminder about when to stop it? | `unclear_you` | wait | respond | 0.87 | 0.90 |
| Jon: So if half your clients pay late, then... | `thinking_aloud` | ignore | wait | 0.08 | 0.58 |
| Jon: Should we ask Iris about deposit norms later? | `about_hypothetical` | ignore | wait | 0.05 | 0.92 |
| Anna: Someone call the restaurant and tell them we might be ten minutes late. | `request_to_people` | ignore | wait | 0.06 | 0.91 |
| Marco: OK car, set the cabin temperature to twenty-one degrees. | `other_device` | ignore | wait | 0.45 | 0.64 |
| Wes: Hey Google, play spooky organ music. | `other_device` | ignore | wait | 0.21 | 0.51 |
| Finn: I mean, if the rate's locked, two years seems like kind of a no-brainer for us, right? | `statement` | ignore | wait | 0.26 | 0.86 |
| Sue: Has anyone used Clover to, um, dig through old CI runs before? Is it decent at that? | `about_question_to_group` | ignore | wait | 0.17 | 0.95 |
| Sofia: Okay, and um, how much of that difference is from those two deferred contracts? | `follow_up` | respond | wait | 0.25 | 0.89 |
| Ravi: Okay, how about we each give a quick thumbs up or down first, then talk details? | `proposal_to_group` | ignore | wait | 0.03 | 0.85 |
| Ravi: Just behavioral, but I sat in on the last ten minutes of coding. | `reply_to_person` | ignore | respond | 0.81 | 0.04 |
| Leila: So, um, before we dig in, how many seats are you actually thinking you'll need this year? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.80 |
| Anita: What did you guys, um, think of the analytics add-on in the demo? Worth it or not? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Elif: You always touch the creepy statue, don't you? | `you_to_person` | ignore | wait | 0.19 | 0.77 |
| Noor: I'll press both eyes in at the same time instead of pulling them. | `action_to_game_master` | respond | ignore | 0.10 | 0.06 |
| Olu: Should we, uh, ask Cleo later whether the vault has a time lock? Like before we commit? | `about_hypothetical` | ignore | wait | 0.08 | 0.86 |
| Leila: Quiz each other tomorrow? Library, ten? | `proposal_to_group` | ignore | wait | 0.03 | 0.85 |
| Diego: Hi, yeah, so we're calling because our bill this month is — it's way off, like double what it should be. | `opener_to_agent` | respond | ignore | 0.19 | 0.35 |
| Siobhan: Wait, can we do the whole batch at once, or does each invite have to go out separately? | `unclear_after_agent` | wait | respond | 0.84 | 0.91 |
| Zoe: Has anyone used Cleo to, like, make up backstories for characters? I want one for my ranger. | `about_question_to_group` | ignore | wait | 0.12 | 0.94 |
| Joy: Eighteen? You said we were twenty-one people, didn't you, so we're short, right? | `you_to_person_after_agent` | ignore | wait | 0.62 | 0.85 |
| Ruth: I'd like Tess to give listeners one daily habit that actually moves the needle. | `role_request` | respond | ignore | 0.77 | 0.46 |
| Dev: Route us past the bakery on Elm, then. | `follow_up` | respond | wait | 0.61 | 0.82 |
| Leo: You totally knew that one before it even said it, didn't you? | `you_to_person_after_agent` | ignore | respond | 0.80 | 0.66 |
| Nils: So did everyone actually finish it this time, or are we bluffing again? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.92 |
| Tomas: Did you ever actually start that magnesium your friend recommended, or is it still in the bag? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.62 |
| Paul: So have you two started packing up your desks yet, or are we all leaving it to the last weekend? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.83 |
| Hana: How about we audit seat usage before renewing anything next quarter? | `proposal_to_group` | ignore | wait | 0.14 | 0.91 |
| Wes: Actually, can you just put it on the board? | `you_after_invite` | respond | wait | 0.63 | 0.85 |
| Lucy: So what are you doing the weekend of the 14th? Free to carry heavy things, perhaps? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.71 |
| Nina: Wait, no, I meant the hint for the next question, not that one. | `correction` | respond | ignore | 0.66 | 0.19 |
| Nina: So the answer's Khufu, I'm pretty sure. | `action_to_game_master` | respond | ignore | 0.45 | 0.07 |
| Abena: Ha, should we ask it to break our tie later? We're clearly not settling this ourselves. | `about_hypothetical` | ignore | wait | 0.09 | 0.87 |
| Ingrid: Can you draft that change and tag me? | `unclear_you` | wait | respond | 0.87 | 0.80 |
| Ottie: Nice, so you can just link QA-418 in your PR when you bump the timeout, right? | `you_to_person_after_agent` | ignore | wait | 0.14 | 0.71 |
| Raj: Are you guys, like, planning to take your monitors yourselves or leave them for the movers? | `group_question_not_for_agent` | ignore | wait | 0.02 | 0.94 |
| Yuki: Going. Torch? | `reply_to_person` | ignore | wait | 0.04 | 0.84 |
| Zoe: Wednesday, really? That assumes nothing else breaks in regression, which feels optimistic. | `unclear_after_agent` | wait | ignore | 0.53 | 0.18 |
| Jill: So can that be backdated to January? | `follow_up` | respond | wait | 0.70 | 0.89 |
| Ivo: Actually, never mind, I'll just ask. Can you show us the pilot timeline? | `you_after_invite` | respond | wait | 0.60 | 0.86 |
| Marco: Okay, and what if you've only got, like, four hours on a balcony? Is there something that does better? | `follow_up` | respond | wait | 0.70 | 0.95 |
| Ines: Okay, and is there an audiobook version? For the, uh, commuters among us. | `follow_up` | respond | wait | 0.34 | 0.94 |
| Ravi: Right, I've refilled it, it's at 1.2 now, but if it drops again, do we book an engineer? | `action_to_game_master` | respond | wait | 0.40 | 0.91 |
| Eli: Wait, before that, did you guys, like, actually practice times tables this week? | `group_question_not_for_agent` | ignore | wait | 0.10 | 0.90 |
| Eli: Yeah, um, I'd like Atlas to, like, explain that eighth trick to everyone. | `role_request` | respond | ignore | 0.68 | 0.48 |
| Wes: Hmm, I still don't really get where the 300 came from. | `statement_of_need` | ignore | wait | 0.72 | 0.76 |
| Chen: Are you guys staying the whole week or flying back right after the reception? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.85 |
| Mateo: Frankie, can you show the... actually, never mind. | `never_mind` | ignore | respond | 0.86 | 0.16 |
| Astrid: Check behind the frozen peas, sometimes stuff gets buried back there. | `continuing_with_person` | ignore | wait | 0.58 | 0.84 |
| Lena: Ottie, did you set the table for six or just five? | `question_to_named_person` | ignore | respond | 0.93 | 0.45 |
| Marta: While she's packing up, let's keep going. What's the capital of Paraguay? | `addressed_by_exclusion` | respond | wait | 0.48 | 0.93 |
| Marta: How long until the doctor actually joins the call? | `question_only_agent_can_answer` | respond | wait | 0.22 | 0.92 |
| Marta: A dry cough, mostly at night. What should I tell the doctor about it? | `reply_then_request` | respond | wait | 0.73 | 0.90 |
| Hiro: Honestly pretty well, but I forget the details. Should we ask Tess later? It took notes. | `about_hypothetical` | ignore | wait | 0.06 | 0.86 |
| Hiro: Can you pull up those numbers again so I can jot them down? | `unclear_you` | wait | respond | 0.85 | 0.82 |
| Kit: Okay, can somebody help me shove these desks together so the papier-mâché volcano fits? | `request_to_people` | ignore | wait | 0.03 | 0.94 |
| Rosa: But you'd need to free up my Thursdays. | `you_to_person` | ignore | wait | 0.06 | 0.60 |
| Sofia: Let's grab our phones then and do the connection right now while we're all here. | `proposal_to_group` | ignore | wait | 0.04 | 0.50 |
| Kit: How many left in this round? | `question_only_agent_can_answer` | respond | wait | 0.32 | 0.89 |
| Elif: Wait, is that refundable if, like, it storms? | `follow_up_by_other` | wait | respond | 0.86 | 0.89 |
| Mateo: No, not Priya, the afternoon candidate, Marcus. | `correction` | respond | ignore | 0.65 | 0.38 |
| Ken: Oh, and um, can you put on some music while we pack these? | `follow_up` | respond | wait | 0.78 | 0.89 |
| Sofia: Okay, I'll admit it, I'm running on two hours of sleep because of this book. Who else? | `remark_to_group` | ignore | wait | 0.04 | 0.93 |
| Jamal: Mine's got coffee stains on chapter twelve. That's a badge of honor, right? | `reply_to_person` | ignore | wait | 0.03 | 0.82 |
| Oskar: Chilton was a car-manual publisher, right? Wild that they took the risk. | `statement` | ignore | wait | 0.23 | 0.69 |
| Ruth: And who's doing pickup later, because I've got a dentist at three? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.92 |
| Tariq: Ottie, didn't you say you'd read the sequels already? Like, all of them? | `similar_name_person` | ignore | respond | 0.87 | 0.39 |
| Ravi: Let's disable the key right now and spin up a fresh one for the deploy pipeline. | `proposal_to_group` | ignore | wait | 0.10 | 0.70 |
| Jill: And does that rate hold if we bump to two hundred seats at renewal? | `follow_up_by_other` | wait | respond | 0.80 | 0.91 |
| Priya: That's better than you expected, right? I thought they'd push us to a new tier. | `you_to_person_after_agent` | ignore | wait | 0.10 | 0.56 |
| Priya: Can you forward me last year's signed order form so I can compare terms? | `unclear_you_person_task` | ignore | wait | 0.42 | 0.82 |
| Hiro: Could you drop them off Saturday night instead? | `you_to_person` | ignore | wait | 0.08 | 0.62 |
| Fatima: Okay, let's book the pavilion tonight and split the cake and charcoal fifty-fifty. | `proposal_to_group` | ignore | wait | 0.17 | 0.52 |
| Fatima: Uploaded. Two weeks of entries. | `action_to_game_master` | respond | ignore | 0.69 | 0.07 |
| Amy: Can you send me the gear list? Lost it. | `unclear_you_person_task` | ignore | wait | 0.16 | 0.88 |
| Amy: Who's actually cooking? Anyone done the menu? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.94 |
| Femi: Have any of you used it to, like, generate the migration checklists? Or just lookups? | `about_question_to_group` | ignore | wait | 0.11 | 0.94 |
| Freya: Which day was that technician slot booked for again? | `question_only_agent_can_answer` | respond | wait | 0.23 | 0.93 |
| Marta: It's pretty thorough, huh, it caught the slip thing right away. | `about_pronoun` | ignore | wait | 0.43 | 0.67 |
| Ken: Okay, photo's uploading now, it's, uh, almost there. | `action_to_game_master` | respond | ignore | 0.15 | 0.04 |
| Yuki: Were you thinking of running the sessions yourself, or, like, splitting them up? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.70 |
| Wes: Could you add a Belém stop to Saturday morning then? | `follow_up` | respond | wait | 0.75 | 0.86 |
| Grace: Hi there, so our broadband keeps dropping out, like five or six times every evening. | `opener_to_agent` | respond | ignore | 0.18 | 0.32 |
| Dev: No, I meant the video call, not you. Is the call being recorded? | `correction` | respond | wait | 0.44 | 0.91 |
| Kay: Okay so, um, what if we do our poster on Mount St. Helens instead of Vesuvius? | `proposal_to_group` | ignore | wait | 0.05 | 0.93 |
| Wes: Okay, so, um, can you text the confirmation to my phone instead of email? | `action_to_game_master` | respond | wait | 0.40 | 0.91 |
| Tariq: Next question, please. Make it a two-digit squaring one. | `action_to_game_master` | respond | wait | 0.67 | 0.84 |
| Mei: Right, who's actually feeling brave enough to take the pager this week? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Lena: Somebody please go shoo Biscuit off the keyboard before he joins the call. | `request_to_people` | ignore | wait | 0.05 | 0.88 |
| Divya: Um, are any of you actually free to sit on interview panels next month? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Noa: I'd like Clover to tell us whether agents get a separate, shorter course. | `role_request` | respond | wait | 0.69 | 0.59 |
| Mei: Okay, who actually slept before this paged? Be honest, I got maybe two hours. | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.91 |
| Ken: How about we revert 8812 now and do the proper fix after breakfast? | `proposal_to_group` | ignore | wait | 0.05 | 0.88 |
| Tom: Okay, and like, do we need to have everything boxed up the night before? | `follow_up` | respond | wait | 0.59 | 0.93 |
| Noor: Okay so, what do you all think, are we keeping the hero banner or, like, ditching it? | `group_question_not_for_agent` | ignore | wait | 0.10 | 0.93 |
| Ada: Like, is that tempo runs or intervals? No idea. | `statement_of_need` | ignore | wait | 0.08 | 0.91 |
| Anita: So are you two actually doing the long runs on Sundays, or switching to Saturdays? | `group_question_not_for_agent` | ignore | wait | 0.02 | 0.82 |
| Maya: Has either of you actually used Gus to plan a trip, like picking crags or checking conditions? | `about_question_to_group` | ignore | wait | 0.15 | 0.95 |
| Tanya: Have you guys ever had it draft the status page update? Mine always sound like ransom notes. | `about_question_to_group` | ignore | wait | 0.23 | 0.91 |
| Lars: Yeah, I've heard, but it's, um, kind of a brick, isn't it? | `reply_to_person` | ignore | wait | 0.08 | 0.77 |
| Raj: Okay, how about loser of this round buys everyone hot chocolate after? | `proposal_to_group` | ignore | wait | 0.03 | 0.91 |
| Maya: I'd like Gus to log a repair request for our washer, it stopped mid-cycle last night. | `role_request` | respond | wait | 0.63 | 0.73 |
| Ren: Okay, how about we each pick one chapter we loved and one we'd throw in the river? | `proposal_to_group` | ignore | wait | 0.03 | 0.90 |
| Marco: And after the stop, carry on to the campsite from there? | `follow_up` | respond | wait | 0.66 | 0.88 |
| Ken: And if hiring freezes? | `follow_up` | respond | wait | 0.59 | 0.88 |
| Nina: Sorry, quick thing, did you send me that invoice yet? | `aside_over_agent` | ignore | wait | 0.12 | 0.59 |
| Chris: Okay, snacks are out, dice are rolled warm. We're ready to finally storm that haunted castle. | `opener_to_agent` | respond | ignore | 0.04 | 0.05 |
| Connor: So if you can send over the forty-seat quote today, we'll get it in front of finance this week. | `you_to_person` | ignore | wait | 0.04 | 0.63 |
| Ngozi: Should we maybe ask Tess later about other books by this author? Like for next month? | `about_hypothetical` | ignore | wait | 0.08 | 0.92 |
| Connor: Yeah, and like, both of you guys need to Venmo me the deposit by Friday, okay? | `request_to_people` | ignore | wait | 0.04 | 0.63 |
| Connor: So are you actually gonna try snowboarding this time or, like, stick with skis? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.56 |
| Priya: Right, forgot her. Add her. | `reply_to_person` | ignore | wait | 0.42 | 0.75 |
| Arjun: Okay, and, like, how long is it booked for? Do we have time for Q&A? | `follow_up` | respond | wait | 0.77 | 0.86 |
| Lars: Wait, if it closes at six, is there anything open later for ice? | `follow_up_by_other` | wait | respond | 0.84 | 0.92 |
| Chen: How many times has the connection actually dropped this week? | `question_only_agent_can_answer` | respond | wait | 0.11 | 0.82 |
| Rhys: Me, I'll sneak toward the gold, quietly. | `answer_to_agent_question` | respond | ignore | 0.69 | 0.14 |
| Evie: Okay, while he's sneaking, I want to, um, look at the dragon's neck — is there anything weird? | `action_to_game_master` | respond | wait | 0.59 | 0.90 |
| Bea: Can you two come help carry the sofa Saturday? | `request_to_people` | ignore | wait | 0.03 | 0.72 |
| Sam: Did either of you, um, fill up last time you had the car? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Chen: So are you guys, like, planning to present the hiring stuff yourselves, or should I? | `group_question_not_for_agent` | ignore | wait | 0.02 | 0.92 |
| Petra: So, um, what did you all think of last quarter's board meeting, like, honestly? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.92 |
| Lucy: Anybody else been through one of these supply chain messes before, or is this a first? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.95 |
| Kofi: Actually, hang up that call and route us around the motorway instead. | `only_agent_can_do` | respond | wait | 0.60 | 0.83 |
| Kofi: Got cash for the toll? I've only got cards. | `continuing_with_person` | ignore | wait | 0.05 | 0.72 |
| Chloe: Hey TV, pause the documentary and turn the volume down. | `other_device` | ignore | wait | 0.29 | 0.65 |
| Jamal: Can you get them to send a text when it's actually out for delivery? | `unclear_you` | wait | respond | 0.86 | 0.86 |
| Nils: Who's actually planning to come in on moving day? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.94 |
| Ottie: Should we ask Otto later? Settle the tricky ones? | `about_hypothetical` | ignore | wait | 0.09 | 0.83 |
| Jon: Anyone actually going Thursday? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.93 |
| Sue: Anyone staying for pudding? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.95 |
| Can: Let's pause the reconciliation job and retry the migration on its own, outside the pipeline. | `proposal_to_group` | ignore | wait | 0.09 | 0.66 |
| Zoe: Fine, but only if we confirm nothing downstream depends on tonight's run. | `reply_to_person` | ignore | wait | 0.06 | 0.65 |
| Ngozi: Which of those are blocked right now? | `you_after_invite` | respond | wait | 0.57 | 0.93 |
| Wei: Yeah, ten milligrams, and I took one around eight this morning. | `reply_to_person` | ignore | respond | 0.82 | 0.05 |
| Aoife: Should we ask Indy afterwards whether there's a group discount? | `about_hypothetical` | ignore | wait | 0.06 | 0.88 |
| Olga: Bea, could you set up the Denver group now... actually, never mind, let's wait. | `never_mind` | ignore | respond | 0.83 | 0.17 |
| Nils: Can you check the Bernina Express too? | `unclear_you` | wait | respond | 0.83 | 0.87 |
| Arjun: Okay, um, we also need to add shellfish. He got hives from shrimp last summer. | `action_to_game_master` | respond | wait | 0.44 | 0.52 |
| Ben: Send the invites after that. | `command_no_name` | respond | wait | 0.76 | 0.71 |
| Ines: Anyone actually like Paul? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.95 |
| Sara: Okay, and turn the music up a bit, I love this one. | `command_no_name` | respond | wait | 0.52 | 0.87 |
| Ken: Put icing sugar on the shopping list then, we've got maybe a cupful. | `follow_up` | respond | ignore | 0.26 | 0.34 |
| Ingrid: So did anyone actually cry at the funeral scene, or am I the only softie here? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Lana: Connor, wait, did you add Luna to the group chat too, or is she just on this call? | `about_to_named_person` | ignore | wait | 0.06 | 0.67 |
| Mei: What if we all, like, chip in twenty each and get the silver moon decorations too? | `proposal_to_group` | ignore | wait | 0.03 | 0.89 |
| Ines: Can you send me a template of that CSV? | `unclear_you` | wait | respond | 0.86 | 0.76 |
| Kofi: Um, so, like, should we ask Ivy about the timeline later? I got kinda lost around chapter twelve. | `about_hypothetical` | ignore | wait | 0.05 | 0.91 |
| Karen: Should we ask Penny later how long wraps keep in the fridge? | `about_hypothetical` | ignore | wait | 0.07 | 0.90 |
| Sam: Are you two doing the bonus problems for Friday? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.84 |
| Hugo: Rolled. Fourteen. | `answer_to_agent_question` | respond | ignore | 0.69 | 0.08 |
| Sofia: So who's brave enough to do the walk to school tomorrow instead? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Mira: Halfway. I keep forgetting what RuBisCO actually grabs. | `reply_to_person` | ignore | wait | 0.14 | 0.65 |
| Mira: Wait, did you bring the flashcards? I left mine on the bus. | `aside_over_agent` | ignore | wait | 0.04 | 0.65 |
| Raf: And, uh, why is Dutch so quick? Is it the vocabulary or— | `follow_up` | respond | wait | 0.77 | 0.87 |
| Tom: Can you send me that spreadsheet with everyone's votes from last month? | `unclear_you_person_task` | ignore | wait | 0.27 | 0.79 |
| Tanya: I honestly don't get how they calculate the seat count, like, active users or licensed ones. | `statement_of_need` | ignore | wait | 0.18 | 0.85 |
| Aoife: I'd like Iris to book that for three people. | `role_request` | respond | ignore | 0.74 | 0.32 |
| Victor: Are you all actually fine with a four-hour train day, or is that too much? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.93 |
| Pablo: Okay so I still don't get why plants need light if they're making sugar out of CO2 anyway. | `statement` | ignore | wait | 0.09 | 0.94 |
| Pablo: Can you guys pass me your notebooks so I can copy the diagram from Thursday's lecture? | `request_to_people` | ignore | wait | 0.03 | 0.84 |
| Olga: Okay, so, um, we're back for the jungle temple thing, like, picking up right where we left off last week. | `opener_to_agent` | respond | ignore | 0.06 | 0.06 |
| Sue: Assistant, can you check if the statue's... actually, never mind. | `never_mind` | ignore | respond | 0.90 | 0.20 |
| Zara: Plenty. Put the warehouse lead ren on the guest list too. | `alias_false_match` | ignore | wait | 0.37 | 0.79 |
| Sara: Okay, while she does that, my cleric lights a torch and looks at the carvings up top. | `action_to_game_master` | respond | ignore | 0.21 | 0.23 |
| Sue: How about we do a dry run of the cutover tomorrow morning, like ten o'clock, all of us? | `proposal_to_group` | ignore | wait | 0.05 | 0.92 |
| Ivan: So why don't we just do Tomorrow now and, uh, save Covenant for the summer when we've got more time? | `proposal_to_group` | ignore | wait | 0.04 | 0.85 |
| Victor: Nice. What about the customers table, any constraints still missing there? | `follow_up` | respond | wait | 0.60 | 0.93 |
| Jack: Okay, how about Petra hits the terminal while me and Imran, um, guard the corridor? | `proposal_to_group` | ignore | wait | 0.04 | 0.60 |
| Imran: Could that fit into a single two-week block? | `follow_up` | respond | wait | 0.70 | 0.89 |
| Astrid: I'd like Cleo to add the metformin too. | `role_request` | respond | wait | 0.72 | 0.68 |
| Chloe: Next one. Atorvastatin. | `command_no_name` | respond | wait | 0.64 | 0.69 |
| Siobhan: You're booking the table, then? Six seats, near the front. | `you_to_person` | ignore | wait | 0.10 | 0.67 |
| Jack: What if we get her brother to bring her there, say it's just a casual dinner? | `proposal_to_group` | ignore | wait | 0.07 | 0.92 |
| Paul: Should we ask Cleo later how long the frosting needs to chill, like, before we spread it? | `about_hypothetical` | ignore | wait | 0.08 | 0.90 |
| Ivan: You still driving me Thursday? | `group_question_not_for_agent` | ignore | wait | 0.11 | 0.57 |
| Olga: No, that's Chris's rope. Mine's separate. | `correction` | respond | ignore | 0.06 | 0.06 |
| Ingrid: Should we ask Pip once we've scoped it? | `about_hypothetical` | ignore | wait | 0.06 | 0.92 |
| Ingrid: So keep it clean. No guesses on record. | `continuing_with_person` | ignore | wait | 0.04 | 0.61 |
| Ruth: And remember, Otto also said we need a logbook with daily measurements, so like, start writing stuff down. | `about_reported` | ignore | wait | 0.08 | 0.54 |
| Jamal: How far ahead do we need to book a temporary parking suspension, like for moving day? | `request_after_summon` | respond | wait | 0.75 | 0.89 |
| Olu: Are you, like, planning to roll this out to the sales folks this week, or wait? | `group_question_not_for_agent` | ignore | wait | 0.20 | 0.80 |
| Marco: Huh, okay, so what's actually holding all those connections open? | `follow_up` | respond | wait | 0.44 | 0.93 |
| Marco: Okay so like, who approved that change, and was it reviewed? | `follow_up` | respond | wait | 0.50 | 0.86 |
| Ingrid: What's the error rate looking like now, like, since the scale-down? | `request_after_summon` | respond | wait | 0.54 | 0.89 |
| Fatima: Hi, our broadband keeps dropping out, maybe five or six times every evening. We need it sorted. | `opener_to_agent` | respond | wait | 0.15 | 0.89 |
| Hugo: I usually just take it with my coffee, or... no, sometimes before, I don't... | `thinking_aloud` | ignore | respond | 0.84 | 0.08 |
| Petra: Should we save the pricing stuff and ask Otto about it in the second half? | `about_hypothetical` | ignore | wait | 0.08 | 0.91 |
| Tanya: No, wait. Patel's Thursday. Today's Dr. Huang. | `correction` | respond | ignore | 0.70 | 0.11 |
| Siobhan: So what do you reckon, does staggering cost us much time? | `you_after_invite` | respond | wait | 0.74 | 0.83 |
| Can: So what are you guys doing after we fill up, like, still going to the market? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.89 |
| Noa: You said we'd do multiplication after this, right? | `you_to_person` | ignore | wait | 0.14 | 0.78 |
| Omar: So for next month, I'm begging, something under three hundred pages. Please. | `statement` | ignore | wait | 0.04 | 0.89 |
| Kofi: You should mention the knee to the doctor too, not just the pills. | `you_to_person` | ignore | wait | 0.13 | 0.68 |
| Ngozi: Right, one of you fill a jug with warm water and the other come hold the torch for me. | `request_to_people` | ignore | wait | 0.06 | 0.78 |
| Ben: Who's getting her there? Anyone volunteering? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.93 |
| Marco: Fine. What're you all getting her, gifts-wise? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Elif: Okay, add that it clicks when I bend it. | `command_no_name` | respond | wait | 0.76 | 0.82 |
| Joy: Can you hand me that glass of water? My mouth is super dry. | `request_to_people` | ignore | wait | 0.09 | 0.65 |
| Paul: I'll creep down a few steps, real quiet, to get a better look. | `answer_to_agent_question` | respond | ignore | 0.39 | 0.07 |
| Harold: Well, that's not very helpful, we already know it's in the email. | `people_after_agent` | ignore | respond | 0.81 | 0.07 |
| Arjun: What did you all think of the eruption video? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.94 |
| Aoife: Let's finalize the reqs by Friday. | `proposal_to_group` | ignore | wait | 0.03 | 0.60 |
| Tom: Um, is there like a detour on Route 9 right now? | `request_after_summon` | respond | wait | 0.70 | 0.90 |
| Ken: Hey, can you pass me that water bottle from the back seat? | `request_to_people` | ignore | wait | 0.18 | 0.63 |
| Victor: Should we ask Remy about that after we finish the, like, hypothesis? | `about_hypothetical` | ignore | wait | 0.05 | 0.90 |
| Victor: I'd like Remy to give us, um, a quick checklist for the display board. | `role_request` | respond | wait | 0.64 | 0.66 |
| Ken: Can someone, um, help me carry the heavy cardboard trifold over to the lab sink? | `request_to_people` | ignore | wait | 0.04 | 0.95 |
| Kofi: How's everyone's coffee holding up before we dive into this? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.95 |
| Chloe: How many modules are left in the team training track? | `question_only_agent_can_answer` | respond | wait | 0.17 | 0.90 |
| Aisha: Okay, I put the cap back on and started the rinse cycle. | `action_to_game_master` | respond | ignore | 0.29 | 0.04 |
| Kwame: Should we ask Pip to draft the handover notes once we're done? | `about_hypothetical` | ignore | wait | 0.07 | 0.93 |
| Kwame: Actually, can you just schedule that reminder for nine-thirty? | `you_after_invite` | respond | wait | 0.53 | 0.84 |
| Harold: Bot, can you also check... actually, never mind, I've got it right here. | `never_mind` | ignore | respond | 0.83 | 0.08 |
| Anita: Should we ask the assistant to summarize the HR notes later? | `about_hypothetical` | ignore | wait | 0.07 | 0.88 |
| Kit: One hundred and thirty-eight. | `answer_to_agent_question` | respond | ignore | 0.78 | 0.03 |
| Anna: Turn the heat down to low so it doesn't burn. | `reply_to_person` | ignore | wait | 0.09 | 0.67 |
| Jack: Mute my mic. | `request_after_summon` | respond | wait | 0.72 | 0.86 |
| Pedro: We still need to rotate all related keys and patch the exposed endpoint before morning. | `statement` | ignore | wait | 0.12 | 0.66 |
| Ken: Definitely not me, I'm sending my stealthy rogue ahead. | `answer_to_agent_question` | respond | ignore | 0.65 | 0.09 |
| Pedro: Moving in, weapons ready. | `answer_to_agent_question` | respond | ignore | 0.53 | 0.04 |
| Noa: Have any of you used Dash to pull the feedback forms yet? | `about_question_to_group` | ignore | wait | 0.07 | 0.95 |
| Nina: Should we ask Frankie to pull last year's feedback? | `about_hypothetical` | ignore | wait | 0.10 | 0.93 |
| Joy: Can you check when that timeout first showed up in main? | `you_after_invite` | respond | wait | 0.70 | 0.85 |
| Petra: Yeah, like, have you guys ever used Penny to practice for actual school tests? | `about_question_to_group` | ignore | wait | 0.09 | 0.87 |
| Hiro: Alright, we're all set to pull off this museum heist, so let's get started. | `opener_to_agent` | respond | ignore | 0.04 | 0.16 |
| Chris: What's the minimum user count for the pilot? | `you_after_invite` | respond | wait | 0.32 | 0.91 |
| Chris: Actually, do you offer a discount if we convert to annual? | `you_after_invite` | respond | wait | 0.77 | 0.90 |
| Tanya: It's mostly a dull ache, maybe a four out of ten. | `action_to_game_master` | respond | ignore | 0.12 | 0.06 |
| Diego: Actually, can you just tell me if it won the Nebula? | `you_after_invite` | respond | wait | 0.58 | 0.90 |
| Tariq: Could you pass me the extra copy of the handout? | `unclear_you_person_task` | ignore | wait | 0.05 | 0.84 |
| Zoe: Did you get a chance to review their API rate limits? | `you_to_person` | ignore | wait | 0.13 | 0.73 |
| Tess: You better watch the dial closely so it doesn't go too high. | `you_to_person_after_agent` | ignore | wait | 0.22 | 0.57 |
| Lena: So, who else survived the schema changes yesterday without needing three cups of coffee? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.94 |
| Wei: Hi, we're here for my follow-up visit. | `opener_to_agent` | respond | ignore | 0.09 | 0.11 |
| Maya: Um, who directed the first movie adaptation? | `request_after_summon` | respond | wait | 0.22 | 0.93 |
| Jon: You guys finish the reading? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.90 |
| Lena: Yeah, totally. Should we ask Juno about how long water stays in the ocean later? | `about_hypothetical` | ignore | wait | 0.07 | 0.88 |
| Tess: Did you bring the snacks? | `aside_over_agent` | ignore | wait | 0.05 | 0.84 |
| Ingrid: Can you pass me that printed chart on the desk? | `unclear_you_person_task` | ignore | wait | 0.05 | 0.64 |
| Ingrid: No, I meant the other one you skipped, the alkali metal. | `correction` | respond | wait | 0.78 | 0.71 |
| Lars: Did everyone finish reviewing the presentation slides? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Ines: Can we rent them at the ranger station, or do we need to buy them? | `follow_up` | respond | wait | 0.74 | 0.94 |
| Ivan: Do you have the exact error code from those timeouts? | `you_after_invite` | respond | wait | 0.72 | 0.90 |
| Lucy: I still don't really get how the clouds actually form up there. | `statement_of_need` | ignore | wait | 0.13 | 0.84 |
| Anita: Anyway, you promised you'd help me remember my melatonin dosage if I forgot. | `you_to_person` | ignore | wait | 0.30 | 0.56 |
| Bea: Lars, does Penny speak Spanish too? | `about_to_named_person` | ignore | wait | 0.12 | 0.79 |
| Tom: A-C-C-O-M-O-D-A-T-E. | `answer_to_agent_question` | respond | ignore | 0.78 | 0.04 |
| Mohammed: D-E-F-I-N-I-T-E-L-Y. | `answer_to_agent_question` | respond | ignore | 0.76 | 0.04 |
| Connor: Wait, is the quiz tomorrow? | `aside_over_agent` | ignore | wait | 0.12 | 0.79 |
| Raj: Okay, um, can one of you guys check the glovebox for the fuel card? | `request_to_people` | ignore | wait | 0.06 | 0.87 |
| Ines: Let's write a short response about the rust symbolism. | `proposal_to_group` | ignore | wait | 0.06 | 0.87 |
| Imran: How many attempts are left in this module? | `question_only_agent_can_answer` | respond | wait | 0.41 | 0.90 |
| Karen: Hi, so um, the boiler just cut out and there's no hot water, we're stuck. | `opener_to_agent` | respond | wait | 0.14 | 0.51 |
| Pedro: Sure, give me a sec, it's in that blue box. | `action_to_game_master` | respond | ignore | 0.06 | 0.04 |
| Dev: Is that author still active in the industry? | `follow_up` | respond | wait | 0.68 | 0.91 |
| Raj: Is the doctor already logged into this call yet? | `question_only_agent_can_answer` | respond | wait | 0.14 | 0.89 |
| Karen: So basically, the light energy is just powering the whole system? | `statement` | ignore | wait | 0.28 | 0.92 |
| Paul: Okay, so how do I use that to simplify twelve over eighteen? | `follow_up` | respond | wait | 0.55 | 0.93 |
| Marta: Set a timer for ten minutes now. | `command_no_name` | respond | wait | 0.68 | 0.85 |
| Tess: Also set the first one for next Monday at 9 AM. | `command_no_name` | respond | wait | 0.78 | 0.82 |
| Tariq: Did you hear that? We're almost out of fuel. | `you_to_person_after_agent` | ignore | wait | 0.07 | 0.75 |
| Jon: It's surprisingly fast with that data lookup. | `about_pronoun` | ignore | respond | 0.81 | 0.05 |
| Abena: Ren, make sure we log the client IDs too. | `statement_to_named_person` | ignore | respond | 0.96 | 0.31 |
| Abena: Has anyone used this tool to draft compliance summaries? | `about_question_to_group` | ignore | wait | 0.10 | 0.95 |
| Dev: Does anyone have any concerns about the data retention policies? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.96 |
| Hugo: Honestly, I think most of us learn languages way too formally, right? | `statement` | ignore | wait | 0.05 | 0.75 |
| Zara: Wait, did you hear what Luna told me earlier? She said my pronunciation sounds like a confused owl. | `about_quoted` | ignore | wait | 0.07 | 0.77 |
| Sara: Anyone got the diagram? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.95 |
| Olu: Okay, set a budget reminder for us then. | `follow_up` | respond | wait | 0.73 | 0.82 |
| Anna: Have any of you used Remy to check your citations yet? | `about_question_to_group` | ignore | wait | 0.06 | 0.94 |
| Aisha: Wait, changing passwd permissions? That seems weirdly specific for an accident. | `unclear_after_agent` | wait | ignore | 0.19 | 0.39 |
| Raj: I'd like Cleo to find a nearby pharmacy. | `role_request` | respond | ignore | 0.72 | 0.36 |
| Raf: Hey, I'm here about my left knee, it's been bothering me all week. | `opener_to_agent` | respond | ignore | 0.15 | 0.27 |
| Maya: Lima, right? | `reply_to_person` | ignore | wait | 0.59 | 0.51 |
| Anna: Hey, can you mute my microphone for a sec? | `unclear_you` | wait | respond | 0.85 | 0.84 |
| Dev: Add a note about the safety briefing. | `command_no_name` | respond | wait | 0.76 | 0.79 |
| Tariq: Just to be safe, let's verify the room number. | `continuing_with_person` | ignore | wait | 0.13 | 0.82 |
| Maya: Who hit the flaky test before lunch? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.93 |
| Paul: Did anyone check the logs yet? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Jon: Okay, and how much free space did it show right before it filled up? | `follow_up` | respond | wait | 0.79 | 0.84 |
| Bea: Can you email me the link to the job description? | `unclear_you_person_task` | ignore | wait | 0.32 | 0.79 |
| Grace: What are you all doing for dinner tonight? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.94 |
| Sue: Otto, pull up the... actually, never mind. | `never_mind` | ignore | respond | 0.85 | 0.18 |
| Rosa: So, are we packing sandwiches or buying lunch tomorrow? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Mohammed: What time does the school bus leave tomorrow? | `request_after_summon` | respond | wait | 0.78 | 0.79 |
| Tomas: Wait, so it's not saving any of this to the cloud? | `follow_up_by_other` | wait | respond | 0.82 | 0.90 |
| Ben: Hey Google, what's the weather like this afternoon? | `other_device` | ignore | wait | 0.25 | 0.57 |
| Hana: Should we ask Ember about the bibliography format? | `about_hypothetical` | ignore | wait | 0.08 | 0.93 |
| Wei: So, do I need to hold the button for longer? | `you_after_invite` | respond | wait | 0.55 | 0.88 |
| Jamal: Keep recording for the summary. | `command_no_name` | respond | wait | 0.64 | 0.74 |
| Ingrid: You're probably better at reading the metrics than I am, right? | `you_to_person` | ignore | wait | 0.14 | 0.87 |
| Kwame: Are you sure? The water pressure here is fine. | `unclear_after_agent` | wait | respond | 0.82 | 0.86 |
| Femi: So, when exactly are we pushing the beta out? | `you_after_invite` | respond | wait | 0.12 | 0.85 |
| Kofi: No, the other one, take the highway off-ramp. | `correction` | respond | wait | 0.56 | 0.79 |
| Olga: Oh no, I totally forgot those. How bad is it? | `reply_to_person` | ignore | wait | 0.04 | 0.72 |
| Priya: Hey, can you show me the latest error count from the logs? | `you_after_invite` | respond | wait | 0.53 | 0.88 |
| Victor: Has anyone else seen the latency spikes on the staging server? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.95 |
| Theo: Can someone physically check the rack status in the data center? | `request_to_people` | ignore | wait | 0.04 | 0.90 |
| Tariq: Did you guys hear how Ivy accidentally called Spanish 'Castilian' just now? | `about_reported` | ignore | wait | 0.05 | 0.89 |
| Can: Anyway, maybe we should just grab some pizza and watch it together? | `proposal_to_group` | ignore | wait | 0.04 | 0.87 |
| Tom: Also, let's not forget to check their references properly this time. | `statement` | ignore | wait | 0.03 | 0.67 |
| Sue: Right, we're here to sort out that nightmare spelling list before Friday. | `opener_to_agent` | respond | ignore | 0.05 | 0.10 |
| Cal: Isis, do you know if Iris has access to the latest gardening guides? | `about_to_named_person` | ignore | wait | 0.10 | 0.51 |
| Cal: I’d like Iris to pull up a list of slug-resistant plants. | `role_request` | respond | ignore | 0.64 | 0.49 |
| Olga: Gus, actually, never mind. | `never_mind` | ignore | respond | 0.89 | 0.11 |
| Olga: Which region is driving that spike? | `follow_up` | respond | wait | 0.77 | 0.92 |
| Rosa: Should we ask Ember about that one? | `about_hypothetical` | ignore | wait | 0.08 | 0.92 |
| Ivan: Who else studied this chapter before class? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.87 |
| Paul: Can we increase that temporarily? | `follow_up` | respond | wait | 0.27 | 0.94 |
| Tom: I’m still not clear on how that affects the launch date. | `statement_of_need` | ignore | wait | 0.65 | 0.83 |
| Hugh: I was just wondering if the security module is actually that long... | `thinking_aloud` | ignore | wait | 0.49 | 0.82 |
| Elif: Please mark the security module as optional for the junior staff. | `command_no_name` | respond | wait | 0.69 | 0.85 |
| Lucia: I'd like Cleo to list the open tickets with high priority. | `role_request` | respond | ignore | 0.77 | 0.46 |
| Karen: Has anyone actually used it to check disk space before? | `about_question_to_group` | ignore | wait | 0.05 | 0.94 |
| Zoe: Should we ask Pip what's taking up the space? | `about_hypothetical` | ignore | wait | 0.07 | 0.94 |
| Aisha: Who is eating bread this weekend? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Leo: Hey, can you pull up the data for that? | `you_after_invite` | respond | wait | 0.60 | 0.82 |
| Olu: Someone wash the greens, please. | `request_to_people` | ignore | wait | 0.04 | 0.91 |
| Elif: Now remove the old test account. | `command_no_name` | respond | wait | 0.72 | 0.78 |
| Noa: Okay, I’m hiding behind the crates until I hear that thud, then I move. | `action_to_game_master` | respond | ignore | 0.65 | 0.05 |
| Marco: I mean, it literally said, 'Don't panic, it's just a quiz' to me last time. Kind of weird, right? | `about_quoted` | ignore | wait | 0.14 | 0.89 |
| Femi: Can someone grab the coffee from the kitchen? | `request_to_people` | ignore | wait | 0.05 | 0.93 |
| Raf: You should check if the dates are still open. | `you_to_person` | ignore | wait | 0.29 | 0.74 |
| Tom: Connor, can Ace update the document again? | `about_to_named_person` | ignore | wait | 0.15 | 0.56 |
| Chris: Hey Cortana, remind me to check the server status later. | `other_device` | ignore | respond | 0.94 | 0.29 |
| Ben: Has either of you used the chatbot for anything else recently? | `about_question_to_group` | ignore | wait | 0.17 | 0.93 |
| Lucy: You should highlight that to the stakeholders. | `you_to_person_after_agent` | ignore | wait | 0.43 | 0.75 |
| Lars: So, did you guys finish the homework before starting this? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.88 |
| Evie: You didn’t mention that 5d part before, did you? | `you_to_person_after_agent` | ignore | respond | 0.90 | 0.71 |
| Nils: Please start writing the incident ticket now. | `request_to_people` | ignore | wait | 0.15 | 0.84 |
| Mohammed: Anyone want a coffee after? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.94 |
| Tom: Can you show me the raw data for the last hour? | `follow_up` | respond | wait | 0.56 | 0.91 |
| Kay: Make sure you check the file before sharing it. | `you_to_person_after_agent` | ignore | wait | 0.34 | 0.62 |
| Dana: You should update the status to critical then. | `you_to_person_after_agent` | ignore | wait | 0.70 | 0.83 |
| Chris: Honestly, I always mix up nitrogen and neon. Like, which one is gas? | `statement` | ignore | wait | 0.61 | 0.94 |
| Eli: Who handles the data cleaning on your end? | `group_question_not_for_agent` | ignore | wait | 0.50 | 0.88 |
| Mei: Sage, or I mean Raj, did you write that down too? | `name_slip_corrected` | ignore | wait | 0.26 | 0.71 |
| Petra: Should we ask Kai for a gear list later? | `about_hypothetical` | ignore | wait | 0.08 | 0.93 |
| Zoe: Yeah, like, where do you even put all those pots? | `reply_to_person` | ignore | wait | 0.03 | 0.87 |
| Ngozi: Hey Cortana, what's the weather in Berlin? | `other_device` | ignore | wait | 0.27 | 0.52 |
| Siobhan: Should we ask Frankie about the database lock? | `about_hypothetical` | ignore | wait | 0.08 | 0.91 |
| Siobhan: Did anyone grab lunch before this mess started? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.94 |
| Karen: By the way, what's everyone having for lunch today? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.93 |
| Kwame: You should skip the line and just order delivery instead. | `you_to_person` | ignore | wait | 0.08 | 0.50 |
| Raj: Please send the current participant list to the project inbox. | `command_no_name` | respond | wait | 0.71 | 0.85 |
| Ingrid: Who else has an opinion on the candidate's technical skills? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.94 |
| Karen: What are your plans for lunch today? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.89 |
| Aoife: Hey, can you slide that character sheet over to me? | `unclear_you_person_task` | ignore | wait | 0.12 | 0.82 |
| Grace: Hi, um, we're here because the washing machine just stopped working again. | `opener_to_agent` | respond | ignore | 0.20 | 0.28 |
| Eko: Let's just order a backup heater for tonight. | `proposal_to_group` | ignore | wait | 0.12 | 0.62 |
| Bea: So, maybe we should start the audit with the perimeter firewalls first? | `proposal_to_group` | ignore | wait | 0.08 | 0.70 |
| Bea: Has anyone had a chance to look at the latest compliance logs yet? | `group_question_not_for_agent` | ignore | wait | 0.07 | 0.93 |
| Karen: Have any of you used Pip for planting schedules? | `about_question_to_group` | ignore | wait | 0.11 | 0.95 |
| Hiro: sorry, quick question, did you check the API gateway too? | `aside_over_agent` | ignore | wait | 0.45 | 0.86 |
| Lena: Has either of you used this app before? | `about_question_to_group` | ignore | wait | 0.13 | 0.91 |
| Dev: Do we need manager approval for amounts over fifty? | `follow_up` | respond | wait | 0.57 | 0.91 |
| Tomas: You, reserve two seats on the morning flight. | `you_after_invite` | respond | wait | 0.62 | 0.79 |
| Tomas: Can you add our details to the hotel booking too? | `follow_up` | respond | wait | 0.72 | 0.87 |
| Mira: This is getting a little confusing for all of us, isn't it? | `remark_to_group` | ignore | wait | 0.15 | 0.88 |
| Olga: You should double-check the timestamps, you missed one last time. | `you_to_person_after_agent` | ignore | wait | 0.74 | 0.66 |
| Diego: Should we ask the assistant to dig into the correlation between the cache purge and the spike? | `about_hypothetical` | ignore | wait | 0.09 | 0.91 |
| Can: Guys, text the venue to confirm the date. | `request_to_people` | ignore | wait | 0.07 | 0.83 |
| Connor: Anyone used it for anything specific lately? | `about_question_to_group` | ignore | wait | 0.08 | 0.93 |
| Connor: You heard that? Pretty specific answer. | `you_to_person_after_agent` | ignore | wait | 0.31 | 0.78 |
| Aisha: No, I'm staying back. I'll keep watch. | `answer_to_agent_question` | respond | ignore | 0.16 | 0.05 |
| Imran: Has anyone used Juno to check their vocabulary lists yet? | `about_question_to_group` | ignore | wait | 0.08 | 0.94 |
| Petra: Okay, I think the answer is 'environment'. | `action_to_game_master` | respond | ignore | 0.07 | 0.07 |
| Sara: What is everyone doing after this study session? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.95 |
| Tariq: wait does n have to be the full population size | `follow_up` | respond | wait | 0.69 | 0.88 |
| Wei: Setting up for the seven o'clock check. | `opener_to_agent` | respond | ignore | 0.07 | 0.06 |
| Wei: Just the Lisinopril. What's the dose? | `reply_then_request` | respond | wait | 0.79 | 0.85 |
| Aoife: No, that's all for now, thanks. | `answer_to_agent_question` | respond | ignore | 0.71 | 0.04 |
| Astrid: Do you guys want to join for drinks later? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Zara: Tess, can you show me a map of— actually, never mind. | `never_mind` | ignore | respond | 0.80 | 0.16 |
| Ngozi: That seems too low for this time of day, I expected more traffic. | `unclear_after_agent` | wait | ignore | 0.55 | 0.20 |
| Tariq: Has anyone else been using the AI to monitor the network latency? | `about_question_to_group` | ignore | wait | 0.09 | 0.94 |
| Pablo: two hundred is pretty high don't you think | `you_to_person_after_agent` | ignore | wait | 0.58 | 0.85 |
| Ella: Could you slide that soil test file over to me? I need to double-check the nitrogen levels. | `unclear_you_person_task` | ignore | wait | 0.28 | 0.79 |
| Fatima: Is 'childs' ever used in any dialect? | `follow_up` | respond | wait | 0.50 | 0.95 |
| Eli: Let's wrap this up and move to the next candidate. | `proposal_to_group` | ignore | wait | 0.04 | 0.57 |
| Priya: That seems high for the technical section. | `unclear_after_agent` | wait | ignore | 0.47 | 0.20 |
| Eli: I'd like Penny to email this report to the hiring committee. | `role_request` | respond | ignore | 0.71 | 0.41 |
| Joy: You're sure? I hate cleaning filters. | `you_to_person_after_agent` | ignore | respond | 0.83 | 0.81 |
| Noa: That seems way too high for this climate. | `unclear_after_agent` | wait | ignore | 0.68 | 0.10 |
| Astrid: Wait, why is six the common denominator? Isn't it the biggest number? | `unclear_after_agent` | wait | respond | 0.83 | 0.92 |
| Ingrid: So, is fraction addition generally considered a major stumbling block for middle schoolers? | `you_after_invite` | respond | wait | 0.49 | 0.93 |
| Connor: Anyone actually hungry, or is this just a thirsty day? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Wei: Stuck? It's been 'stuck' for three days. | `unclear_after_agent` | wait | respond | 0.82 | 0.47 |
| Wei: Who else is upset about this? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.89 |
| Can: Does it auto-renew? | `follow_up_by_other` | wait | respond | 0.86 | 0.86 |
| Ruth: You might want to note that in the docs. | `you_to_person_after_agent` | ignore | wait | 0.39 | 0.75 |
| Chloe: What do you think about the btree? | `you_after_invite` | respond | wait | 0.56 | 0.89 |
| Lars: You guys look really relaxed, is it just me or is it quiet? | `remark_to_group` | ignore | wait | 0.03 | 0.93 |
| Wei: Is anyone else bringing a backup player for next week? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.92 |
| Diego: What did you two grab to eat before we left? | `group_question_not_for_agent` | ignore | wait | 0.02 | 0.81 |
| Jack: Ada, what's the preheat setting, actually, never mind. | `never_mind` | ignore | respond | 0.86 | 0.39 |
| Jack: That seems a bit low for a safe doneness standard. | `unclear_after_agent` | wait | ignore | 0.71 | 0.12 |
| Ngozi: Can you pull up the latest screening scores for the backend roles? | `request_after_summon` | respond | wait | 0.78 | 0.83 |
| Olu: Maybe we should move the final interviews for this group to next Tuesday? | `proposal_to_group` | ignore | wait | 0.06 | 0.84 |
| Greg: Fine, I go for the head. | `reply_to_person` | ignore | respond | 0.82 | 0.04 |
| Sara: How much water should I add to the misting bottle? | `follow_up` | respond | wait | 0.73 | 0.92 |
| Lucia: What is everyone doing for lunch tomorrow, I am starving | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Olu: I assume so, but why would you ask that? | `reply_to_person` | ignore | wait | 0.08 | 0.80 |
| Lana: Hey, did you save the last draft? | `aside_over_agent` | ignore | wait | 0.24 | 0.82 |
| Jon: Hi, we're here because the washer is making a really loud grinding noise. | `opener_to_agent` | respond | ignore | 0.36 | 0.33 |
| Abena: OK car, what's the gas price at the nearest station? | `other_device` | ignore | wait | 0.36 | 0.82 |
| Sue: Can someone check the time on their phone for me? | `request_to_people` | ignore | wait | 0.07 | 0.95 |
| Wei: I'd like Penny to describe the dungeon entrance. | `role_request` | respond | ignore | 0.70 | 0.38 |
| Astrid: Is that higher than last year's rate, Pedro? | `follow_up_by_other` | wait | ignore | 0.05 | 0.26 |

**Graded lines, no single right decision** (129)

| Line | Kind | Jev | addressed | question |
|---|---|---|---|---|
| Nils: Cleo would know what the shuttle costs. | `invite` | ignore | 0.16 | 0.37 |
| Wei: Pip would know a few. | `invite` | ignore | 0.20 | 0.33 |
| Ravi: Bye, Remy! | `farewell_named` | ignore | 0.77 | 0.03 |
| Eli: Ada would know what to add to the glaze. | `invite` | ignore | 0.17 | 0.34 |
| Ruth: The assistant would know. Ask it. | `invite` | wait | 0.24 | 0.68 |
| Tanya: I'd like Bolt's take on whether we need three tents. | `indirect_wish` | wait | 0.75 | 0.59 |
| Rhys: Ask Gus; it might have a better spot for it. | `invite` | wait | 0.09 | 0.70 |
| Zara: I'd like Orion's view on how much time to leave for questions. | `indirect_wish` | wait | 0.73 | 0.54 |
| Pablo: Could one of you ask Wren to find the name of Paul's father? | `relayed_invite` | wait | 0.08 | 0.93 |
| Grace: Could you get Ace to outline a simple cash-flow forecast for us? | `relayed_invite` | wait | 0.20 | 0.81 |
| Leila: Lars, get it to tell us if there's another exit. | `relayed_invite` | ignore | 0.07 | 0.21 |
| Lucy: I'd love Cleo's take on whether 34 points is wildly optimistic for us. | `indirect_wish` | wait | 0.79 | 0.57 |
| Raf: Great, thanks for that. | `thanks` | respond | 0.84 | 0.03 |
| Raf: Somewhere. Can you get it to pull up my last visit notes? | `relayed_invite` | wait | 0.39 | 0.70 |
| Lars: Huh, I'd really like Clover's take on whether we even need an agency here. | `indirect_wish` | wait | 0.50 | 0.70 |
| Ngozi: I'd love to know what Otto thinks about ending on a rhetorical question, honestly. | `indirect_wish` | wait | 0.47 | 0.79 |
| Aisha: Can, get it to make me one of those plans too, but for Portuguese, before Lisbon in June. | `relayed_invite` | ignore | 0.09 | 0.31 |
| Jon: I'd love to hear what Nova thinks about whether Yellowstone could actually blow. | `indirect_wish` | wait | 0.44 | 0.79 |
| Diego: Can you have it note that I carry an EpiPen anyway? | `relayed_invite` | wait | 0.74 | 0.88 |
| Paul: Okay, assistant, that's enough for now. | `stop_named` | respond | 0.95 | 0.06 |
| Anita: I'd kinda like Ivy's take on whether that service account should even have S3 write access. | `indirect_wish` | wait | 0.52 | 0.76 |
| Hugo: Honestly, just ask Indy, it'll know what we did last time. | `invite` | wait | 0.16 | 0.55 |
| Ingrid: Okay. Thanks. | `thanks` | ignore | 0.75 | 0.03 |
| Omar: Freya, get it to slow down for me. | `relayed_invite` | ignore | 0.09 | 0.22 |
| Zara: Ines, can you get it to pull up the sleep questionnaire for me? I can't find the button. | `relayed_invite` | ignore | 0.08 | 0.20 |
| Ruth: Thanks, Penny, that's a big help. | `thanks_named` | respond | 0.89 | 0.02 |
| Anna: Indy would know, it's literally made for this. | `invite` | ignore | 0.17 | 0.22 |
| Kit: Want Frankie's take on rollback versus just bumping the pool. | `indirect_wish` | wait | 0.20 | 0.83 |
| Theo: Okay, thanks, that's really helpful. | `thanks` | ignore | 0.62 | 0.03 |
| Ines: Cal, can you get it to tell us how much time a lockpick roll actually takes? | `relayed_invite` | ignore | 0.19 | 0.41 |
| Elif: Orion would know. | `invite` | ignore | 0.27 | 0.36 |
| Noor: Thanks Atlas, that's a really helpful detail. | `thanks_named` | respond | 0.91 | 0.03 |
| Hugo: Just ask Ada about the gravy too, honestly. | `invite` | wait | 0.10 | 0.77 |
| Tanya: Sage would know if errors are dropping. | `invite` | ignore | 0.25 | 0.48 |
| Lucia: If we need a realistic date, Wren would know. | `invite` | ignore | 0.47 | 0.43 |
| Lena: Thanks, Wren, that really helps. | `thanks_named` | respond | 0.91 | 0.02 |
| Ada: Okay, Tess, that's plenty, stop there before spoilers. | `stop_named` | respond | 0.97 | 0.07 |
| Aoife: Okay, great, thanks for that. | `thanks` | respond | 0.81 | 0.03 |
| Abena: Atlas would know how many seats are actually sitting idle. | `invite` | ignore | 0.21 | 0.26 |
| Jamal: I'd love to hear what Ember thinks about bribing friends with pizza versus paying movers. | `indirect_wish` | wait | 0.25 | 0.81 |
| Noor: Right. Thanks for that. | `thanks` | respond | 0.82 | 0.03 |
| Ivo: Divya, can you get Pip to pull up the pilot timeline from last week's deck? | `relayed_invite` | ignore | 0.05 | 0.21 |
| Wes: Can you get it to add the coffee to my notes? I'll mess it up. | `relayed_invite` | wait | 0.72 | 0.86 |
| Hana: Is traffic bad on Mill Road though? Remy would know. | `invite` | wait | 0.48 | 0.66 |
| Joy: Can one of you have Tess pull up the rubric for me? My laptop's dead. | `relayed_invite` | wait | 0.21 | 0.93 |
| Victor: Can you get it to give us the Mesopotamia question now? | `relayed_invite` | wait | 0.28 | 0.81 |
| Jess: Oh nice, that's exactly it. Thanks, Tess. | `thanks_named` | respond | 0.92 | 0.02 |
| Tanya: Ask Dash later if the lot fills up early. | `invite` | ignore | 0.09 | 0.38 |
| Freya: Raj, get it to give me a squaring trick, I'm hopeless at those. | `relayed_invite` | ignore | 0.15 | 0.40 |
| Ada: Great, thanks. | `thanks` | respond | 0.88 | 0.02 |
| Hiro: If we're stuck on her backstory, Tess would know, honestly. | `invite` | ignore | 0.09 | 0.41 |
| Chris: Okay, that's enough for now, Milo, thanks. | `stop_named` | ignore | 0.59 | 0.03 |
| Cal: Who's leading week three? Actually, Penny would know. | `invite` | wait | 0.41 | 0.59 |
| Leila: Dessert—what goes with all this? Ask the assistant, it'll know. | `invite` | wait | 0.48 | 0.63 |
| Isis: Iris, stop there, that's enough for now. | `stop_named` | respond | 0.97 | 0.06 |
| Pedro: See? Ask Ivy the rest. | `invite` | ignore | 0.15 | 0.41 |
| Zoe: See, Wren knows everything about caffeine. | `invite` | ignore | 0.36 | 0.05 |
| Omar: Maya, can you get it to email me that reading schedule? | `relayed_invite` | ignore | 0.09 | 0.20 |
| Aisha: I have to duck out early today, bye Orion! | `farewell_named` | ignore | 0.57 | 0.03 |
| Hugo: Oh perfect, thanks for that. | `thanks` | respond | 0.84 | 0.02 |
| Evie: I'd love to know what Ivy thinks is the most likely essay question. | `indirect_wish` | wait | 0.42 | 0.76 |
| Ken: See, Cleo would know. Always ask Cleo before you guess. | `invite` | ignore | 0.11 | 0.07 |
| Chloe: Okay Cleo, that's enough, Tomas is already eyeing the oven door. | `stop_named` | respond | 0.84 | 0.12 |
| Fatima: Great, thanks. | `thanks` | ignore | 0.77 | 0.02 |
| Sofia: Thanks, Tess, that's exactly the number I was trying to remember. | `thanks_named` | respond | 0.85 | 0.02 |
| Karen: Perfect, thank you, that's super helpful. | `thanks` | respond | 0.83 | 0.03 |
| Oskar: Can one of you have Dash pull up, like, discussion questions for the essays? My mic's being weird. | `relayed_invite` | wait | 0.28 | 0.93 |
| Abena: Um, can one of you get Wren to, like, check my derivative for problem four? I'm totally lost. | `relayed_invite` | wait | 0.09 | 0.95 |
| Lucia: I'd kinda like to know what Wren thinks about which practice problems are, like, most worth doing. | `indirect_wish` | wait | 0.35 | 0.85 |
| Wes: Okay Tess, that's all for now. | `stop_named` | respond | 0.88 | 0.05 |
| Petra: Is The Platform scary? Kai would know. | `invite` | wait | 0.45 | 0.60 |
| Mohammed: Paul, get it to add eggs to the list. | `relayed_invite` | ignore | 0.04 | 0.15 |
| Marco: Get Cleo to pull the hardest language stat for English speakers? | `relayed_invite` | wait | 0.22 | 0.85 |
| Siobhan: Hey, can someone get Wren to pull the auth logs? | `relayed_invite` | wait | 0.14 | 0.94 |
| Kit: Thanks, Assistant. | `thanks_named` | respond | 0.91 | 0.02 |
| Freya: Echo would know. | `invite` | wait | 0.37 | 0.55 |
| Zoe: Tess would know if the gateway update actually went through. | `invite` | ignore | 0.24 | 0.20 |
| Ivan: I'd love to hear Bea's take on whether that's just normal afternoon traffic or a leak. | `indirect_wish` | wait | 0.47 | 0.67 |
| Dev: Assistant, stop. | `stop_named` | respond | 0.97 | 0.11 |
| Sue: Awesome, thank you so much. | `thanks` | respond | 0.82 | 0.03 |
| Chris: Wren would know if v1 tags are supported. | `invite` | ignore | 0.26 | 0.39 |
| Wes: Alright, I have to drop off for another call. Bye, Cleo! | `farewell_named` | ignore | 0.56 | 0.03 |
| Ines: Ask Dash what score the panel gave him on system design. | `invite` | wait | 0.24 | 0.76 |
| Greg: I wonder if there's a faster trick for squaring teens. | `indirect_wish` | wait | 0.18 | 0.53 |
| Hiro: Ask Remy how high the drop is from the skylight. | `invite` | wait | 0.26 | 0.78 |
| Can: Thanks, that narrows it down. | `thanks` | ignore | 0.64 | 0.03 |
| Chris: Can someone ask the AI to pull the pricing tier? | `relayed_invite` | wait | 0.11 | 0.93 |
| Olga: Max, stop, that's enough. | `stop_named` | respond | 0.95 | 0.08 |
| Lucia: Ace would know which service triggered that. | `invite` | ignore | 0.29 | 0.26 |
| Priya: Ask Rook, he probably has the details. | `invite` | wait | 0.25 | 0.57 |
| Harold: Penny would know the rhyme scheme. | `invite` | ignore | 0.18 | 0.18 |
| Theo: Yeah, Otto would definitely know the details. | `invite` | ignore | 0.26 | 0.04 |
| Connor: Can you make Otto find a map of Iceland's volcanoes? | `relayed_invite` | wait | 0.77 | 0.82 |
| Sara: Thanks, that saves us a lot of time. | `thanks` | ignore | 0.78 | 0.02 |
| Aisha: Actually, the intern was on leave, so ask who really knows the logs. | `invite` | wait | 0.04 | 0.81 |
| Sam: You might have some thoughts on this feedback. | `indirect_wish` | wait | 0.16 | 0.78 |
| Wes: I'm really curious what Juno thinks about the new layout. | `indirect_wish` | wait | 0.19 | 0.76 |
| Femi: Can you make it play some jazz for me? | `relayed_invite` | wait | 0.50 | 0.88 |
| Chen: Chen, can you get it to enable two-factor authentication? | `relayed_invite` | ignore | 0.34 | 0.48 |
| Freya: Freya, can you get Hugo to add the new stops to the route? | `relayed_invite` | ignore | 0.13 | 0.49 |
| Jamal: I'd love to hear what you think about the plot twists, by the way. | `indirect_wish` | wait | 0.04 | 0.73 |
| Sam: Sage, stop. That's enough for now. | `stop_named` | respond | 0.96 | 0.10 |
| Lars: Ask Milo, it should have the exact data. | `invite` | ignore | 0.22 | 0.36 |
| Rosa: Thanks, that was fast. | `thanks` | respond | 0.85 | 0.03 |
| Zoe: Thanks, that helps a lot. | `thanks` | respond | 0.83 | 0.03 |
| Paul: Thanks Hugo, that cleared it up for me. | `thanks_named` | respond | 0.91 | 0.02 |
| Ada: I'm wondering what the AI thinks about the marketing allocation. | `indirect_wish` | wait | 0.72 | 0.75 |
| Ada: Thanks, that's really helpful. | `thanks` | respond | 0.89 | 0.02 |
| Leila: Kwame, could you ask the bot to flag this in our project tracker? | `relayed_invite` | ignore | 0.06 | 0.18 |
| Myla: Can you ask Milo to queue the news? | `relayed_invite` | wait | 0.16 | 0.87 |
| Ben: Thanks for the quick check. | `thanks` | respond | 0.89 | 0.03 |
| Nils: Thanks Orion, that saves us a lot of taxi money. | `thanks_named` | respond | 0.86 | 0.03 |
| Sofia: I really want to hear what it thinks about the signal strength. | `indirect_wish` | wait | 0.29 | 0.75 |
| Chris: Get him to calculate bulk fermentation for me. | `relayed_invite` | wait | 0.18 | 0.59 |
| Mohammed: Goodnight Kai. Thanks for the help. | `farewell_named` | respond | 0.88 | 0.04 |
| Ngozi: Thanks, that was helpful. | `thanks` | respond | 0.87 | 0.03 |
| Aida: Ask Ada, she usually has the backup copies. | `invite` | ignore | 0.08 | 0.40 |
| Divya: That's enough, Ada. We'll look for it ourselves. | `stop_named` | respond | 0.87 | 0.04 |
| Petra: Quinn would know the exact log times. | `invite` | ignore | 0.37 | 0.21 |
| Lucia: Ask Cleo for the exact timestamp of the last successful health check. | `invite` | wait | 0.55 | 0.52 |
| Mohammed: Dash would know the next exit. | `invite` | ignore | 0.22 | 0.32 |
| Nina: Tess would know the budget impact. | `invite` | ignore | 0.22 | 0.29 |
| Joy: Ask it what the error code is. | `invite` | wait | 0.32 | 0.78 |
| Hiro: Thanks. That helps. | `thanks` | ignore | 0.77 | 0.03 |
| Ingrid: I wonder what Sage thinks about how hard this concept is for most students. | `indirect_wish` | wait | 0.34 | 0.79 |
| Lena: Thanks, that helps a lot. | `thanks` | respond | 0.82 | 0.02 |
| Can: I'd really like to hear Orion's take on why condensation forms clouds. | `indirect_wish` | wait | 0.77 | 0.51 |
| Bea: Hiro, ask it to skip the hard ones for now. | `relayed_invite` | ignore | 0.06 | 0.20 |
| Chen: Ask Wren about tomato spacing. | `invite` | wait | 0.22 | 0.63 |

## gen-0.1.test3000@anonymous

Source: `None`. Use: per split.

3,000 rows, 3,000 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 80.7% (2316/2871; 79.2 to 82.1) | 79.8% (1273/1595) | 1.4% (23/1595) | 18.8% (299/1595) | 77.5% (724/934) | 6.9% (64/934) |
| Name said → answer | 66.5% (1910/2871; 64.8 to 68.2) | 89.2% (1423/1595) | 10.8% (172/1595) | 0.0% (0/1595) | 52.1% (487/934) | 47.9% (447/934) |

Jev latency from Modal: 145 ms at the median, 198 ms at the 95th percentile (3,000 answers, 12 requests at a time).

Jev's `addressed` number without a threshold: AUROC 0.9777, average precision 0.9682, calibration error 0.0715 (989 lines for the agent, 1,858 not).

**By code** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `` | 3000 | 80.7% (2316/2871) | 1.4% (23/1595) | 18.8% (299/1595) | 77.5% (724/934) | 6.9% (64/934) |

**By style** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `` | 3000 | 80.7% (2316/2871) | 1.4% (23/1595) | 18.8% (299/1595) | 77.5% (724/934) | 6.9% (64/934) |

**By kind** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `reply_to_person` | 519 | 97.5% (506/519) | 0.2% (1/519) | 2.3% (12/519) | n/a | n/a |
| `name_first` | 199 | 100.0% (199/199) | n/a | n/a | 100.0% (199/199) | 0.0% (0/199) |
| `answer_to_agent_question` | 129 | 87.6% (113/129) | n/a | n/a | 87.6% (113/129) | 11.6% (15/129) |
| `question_to_named_person` | 119 | 98.3% (117/119) | 0.8% (1/119) | 0.8% (1/119) | n/a | n/a |
| `follow_up` | 91 | 47.2% (43/91) | n/a | n/a | 47.2% (43/91) | 1.1% (1/91) |
| `group_question_not_for_agent` | 82 | 2.4% (2/82) | 0.0% (0/82) | 97.6% (80/82) | n/a | n/a |
| `statement` | 81 | 81.5% (66/81) | 2.5% (2/81) | 16.1% (13/81) | n/a | n/a |
| `open_factual` | 75 | 98.7% (74/75) | n/a | n/a | n/a | n/a |
| `statement_to_named_person` | 69 | 95.7% (66/69) | 2.9% (2/69) | 1.5% (1/69) | n/a | n/a |
| `named_after_aside` | 58 | 100.0% (58/58) | n/a | n/a | 100.0% (58/58) | 0.0% (0/58) |
| `open_question` | 58 | 100.0% (58/58) | n/a | n/a | n/a | n/a |
| `role_request` | 57 | 59.7% (34/57) | n/a | n/a | 59.7% (34/57) | 17.5% (10/57) |
| `name_last` | 57 | 100.0% (57/57) | n/a | n/a | 100.0% (57/57) | 0.0% (0/57) |
| `follow_up_by_other` | 56 | 92.9% (52/56) | n/a | n/a | n/a | n/a |
| `name_mid` | 52 | 100.0% (52/52) | n/a | n/a | 100.0% (52/52) | 0.0% (0/52) |
| `unclear_you` | 52 | 86.5% (45/52) | n/a | n/a | n/a | n/a |
| `you_to_person_after_agent` | 51 | 68.6% (35/51) | 2.0% (1/51) | 29.4% (15/51) | n/a | n/a |
| `people_after_agent` | 51 | 98.0% (50/51) | 2.0% (1/51) | 0.0% (0/51) | n/a | n/a |
| `unclear_after_agent` | 45 | 75.6% (34/45) | n/a | n/a | n/a | n/a |
| `to_named_person_after_agent` | 41 | 95.1% (39/41) | 0.0% (0/41) | 4.9% (2/41) | n/a | n/a |
| `open_request` | 41 | 100.0% (41/41) | n/a | n/a | n/a | n/a |
| `invite` | 39 | n/a | n/a | n/a | n/a | n/a |
| `about_judged` | 39 | 100.0% (39/39) | 0.0% (0/39) | 0.0% (0/39) | n/a | n/a |
| `proposal_to_group` | 39 | 46.2% (18/39) | 0.0% (0/39) | 53.8% (21/39) | n/a | n/a |
| `remark_to_group` | 37 | 91.9% (34/37) | 0.0% (0/37) | 8.1% (3/37) | n/a | n/a |
| `other_device` | 36 | 77.8% (28/36) | 5.6% (2/36) | 16.7% (6/36) | n/a | n/a |
| `about_to_named_person` | 36 | 75.0% (27/36) | 0.0% (0/36) | 25.0% (9/36) | n/a | n/a |
| `about_reported` | 35 | 94.3% (33/35) | 0.0% (0/35) | 5.7% (2/35) | n/a | n/a |
| `thinking_aloud` | 35 | 85.7% (30/35) | 0.0% (0/35) | 14.3% (5/35) | n/a | n/a |
| `continuing_with_person` | 35 | 77.1% (27/35) | 0.0% (0/35) | 22.9% (8/35) | n/a | n/a |
| `backchannel` | 33 | 100.0% (33/33) | 0.0% (0/33) | 0.0% (0/33) | n/a | n/a |
| `about_hypothetical` | 32 | 0.0% (0/32) | 0.0% (0/32) | 100.0% (32/32) | n/a | n/a |
| `wake_phrase` | 30 | 100.0% (30/30) | n/a | n/a | 100.0% (30/30) | 0.0% (0/30) |
| `role_address` | 29 | 100.0% (29/29) | n/a | n/a | 100.0% (29/29) | 0.0% (0/29) |
| `relayed_invite` | 29 | n/a | n/a | n/a | n/a | n/a |
| `command_no_name` | 28 | 42.9% (12/28) | n/a | n/a | 42.9% (12/28) | 0.0% (0/28) |
| `name_alone` | 27 | 100.0% (27/27) | n/a | n/a | 100.0% (27/27) | 0.0% (0/27) |
| `request_to_people` | 27 | 7.4% (2/27) | 0.0% (0/27) | 92.6% (25/27) | n/a | n/a |
| `you_to_person` | 26 | 50.0% (13/26) | 0.0% (0/26) | 50.0% (13/26) | n/a | n/a |
| `action_to_game_master` | 25 | 4.0% (1/25) | n/a | n/a | 4.0% (1/25) | 60.0% (15/25) |

**Moving the `addressed` threshold**

| Threshold | For the agent: answers now | For others: answers now |
|---|---|---|
| 0.5 | 92.5% (864/934) | 5.9% (94/1595) |
| 0.6 | 89.5% (836/934) | 3.5% (55/1595) |
| 0.7 | 84.9% (793/934) | 2.6% (41/1595) |
| 0.8 | 77.5% (724/934) | 1.4% (23/1595) |
| 0.9 | 63.4% (592/934) | 0.5% (8/1595) |

**Lines Jev decides differently from the label** (555 of 2871)

| Line | Kind | Expected | Jev | addressed | question |
|---|---|---|---|---|---|
| Speaker 2: How much vinegar should we add? | `follow_up` | respond | wait | 0.58 | 0.93 |
| Speaker 2: Can the assistant tell us what to do if there's no hose? | `role_request` | respond | wait | 0.73 | 0.88 |
| Speaker 1: What's a good beginner climb near Boulder? | `request_after_summon` | respond | wait | 0.63 | 0.87 |
| Speaker 3: Can you pass me that worksheet? | `unclear_you_person_task` | ignore | wait | 0.09 | 0.77 |
| Speaker 2: Okay, can I try the next one? | `action_to_game_master` | respond | wait | 0.46 | 0.87 |
| Speaker 2: We should probably find a source on student attitudes, too. | `statement` | ignore | wait | 0.07 | 0.73 |
| Speaker 2: Were you planning to work from home tomorrow? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.77 |
| Speaker 1: When was that token issued? | `open_factual` | wait | respond | 0.86 | 0.88 |
| Speaker 3: Can you check what's in it? | `you_after_invite` | respond | wait | 0.79 | 0.88 |
| Speaker 3: Should we ask Ace later whether we can refill our oxygen up there? | `about_hypothetical` | ignore | wait | 0.09 | 0.86 |
| Speaker 1: Everyone, write your answer on your paper. | `request_to_people` | ignore | wait | 0.04 | 0.70 |
| Speaker 1: Did either of you notice anything strange before it stopped? | `group_question_not_for_agent` | ignore | wait | 0.16 | 0.90 |
| Speaker 3: Quinn, could you tell us how to—actually, never mind. | `never_mind` | ignore | respond | 0.81 | 0.15 |
| Speaker 1: Would you rather visit Ottawa or Paris? | `group_question_not_for_agent` | ignore | wait | 0.25 | 0.91 |
| Speaker 1: OK car, set a reminder to practice Spanish at six. | `other_device` | ignore | wait | 0.61 | 0.52 |
| Speaker 2: Mohammed, we're recording, so let's keep notifications off. | `statement_to_named_person` | ignore | wait | 0.05 | 0.55 |
| Speaker 2: Which one is shorter? | `follow_up` | respond | wait | 0.61 | 0.91 |
| Speaker 1: We're here to give our mental arithmetic a workout. | `opener_to_agent` | respond | ignore | 0.09 | 0.07 |
| Speaker 2: Can you tell us how much a taxi into central Lisbon might cost? | `you_after_invite` | respond | wait | 0.73 | 0.91 |
| Speaker 1: I twisted it getting off the bus. Should I tell the doctor that? | `reply_then_request` | respond | wait | 0.75 | 0.85 |
| Speaker 2: We should find out when the guards change shifts. | `statement` | ignore | wait | 0.14 | 0.73 |
| Speaker 2: Should we ask Atlas later how long groundwater stays underground? | `about_hypothetical` | ignore | wait | 0.05 | 0.89 |
| Speaker 3: Can I tell whether the stone door has any traps? | `request_after_summon` | respond | wait | 0.79 | 0.88 |
| Speaker 1: I'll step over the wire and check the door for a handle. | `action_to_game_master` | respond | ignore | 0.12 | 0.04 |
| Speaker 4: Ada—sorry, Eli, can you check whether the oven is preheated? | `name_slip_corrected` | ignore | wait | 0.53 | 0.50 |
| Speaker 1: Is there any light coming from under the red door? | `question_only_agent_can_answer` | respond | wait | 0.18 | 0.92 |
| Speaker 2: Can someone check the rack lights? | `request_to_people` | ignore | wait | 0.07 | 0.93 |
| Speaker 1: Check the deployment before that. | `command_no_name` | respond | wait | 0.23 | 0.87 |
| Speaker 3: Let's roll back the pool change. | `statement` | ignore | wait | 0.18 | 0.69 |
| Speaker 1: You could check whether the trainers are available that afternoon. | `you_to_person` | ignore | wait | 0.29 | 0.86 |
| Speaker 2: Should we ask the assistant later if there are any discounts available? | `about_hypothetical` | ignore | wait | 0.09 | 0.84 |
| Speaker 1: What happens if we need more seats? | `follow_up` | respond | wait | 0.51 | 0.93 |
| Speaker 3: Maybe I could borrow another one, or... | `thinking_aloud` | ignore | wait | 0.05 | 0.50 |
| Speaker 3: Why do they have six sides? | `follow_up` | respond | wait | 0.78 | 0.88 |
| Speaker 3: Compare that with the current budget. | `command_no_name` | respond | wait | 0.75 | 0.87 |
| Speaker 2: So, um, are you planning to stay for the whole reception? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.70 |
| Speaker 1: Let's include a map of the ashfall in our presentation. | `proposal_to_group` | ignore | wait | 0.07 | 0.64 |
| Speaker 1: We'd need two rooms, wouldn't we? So that could work. | `reply_to_person` | ignore | wait | 0.04 | 0.63 |
| Speaker 2: I don't know. | `answer_to_agent_question` | respond | ignore | 0.79 | 0.09 |
| Speaker 1: Are you two planning any climbing trips this summer? | `group_question_not_for_agent` | ignore | wait | 0.11 | 0.84 |
| Speaker 1: We're calling because our washing machine has stopped draining. | `opener_to_agent` | respond | ignore | 0.26 | 0.32 |
| Speaker 1: Add water jugs to the list. | `command_no_name` | respond | wait | 0.68 | 0.74 |
| Speaker 1: Can you pass me that mixing bowl? | `unclear_you_person_task` | ignore | wait | 0.08 | 0.83 |
| Speaker 3: And can they take the old sofa away? | `follow_up` | respond | wait | 0.72 | 0.88 |
| Speaker 2: Should we ask Frankie later about watering schedules too? | `about_hypothetical` | ignore | wait | 0.07 | 0.91 |
| Speaker 1: Wren, could you look up—actually, never mind. | `never_mind` | ignore | respond | 0.86 | 0.14 |
| Speaker 2: And you've got pots with drainage holes, right? | `continuing_with_person` | ignore | wait | 0.06 | 0.83 |
| Speaker 1: How long should the cake cool before we frost it? | `request_after_summon` | respond | wait | 0.41 | 0.93 |
| Speaker 1: Should we ask Tess about the keys once we see the shift change? | `about_hypothetical` | ignore | wait | 0.10 | 0.89 |
| Speaker 1: My reading this morning was 128 over 82. Can you add that to my intake? | `action_to_game_master` | respond | wait | 0.71 | 0.86 |
| Speaker 3: Will either of you be home then? | `group_question_not_for_agent` | ignore | wait | 0.14 | 0.87 |
| Speaker 3: Have you made other plans for tomorrow morning? | `group_question_not_for_agent` | ignore | wait | 0.08 | 0.85 |
| Speaker 1: How many boxes should we get for a medium-sized kitchen? | `request_after_summon` | respond | wait | 0.62 | 0.90 |
| Speaker 1: Is the doctor running late today? | `question_only_agent_can_answer` | respond | wait | 0.18 | 0.89 |
| Speaker 2: Have either of you used Dash to check readings before? | `about_question_to_group` | ignore | wait | 0.19 | 0.93 |
| Speaker 2: Okay, I've found the filling loop under the boiler. | `action_to_game_master` | respond | ignore | 0.41 | 0.07 |
| Speaker 1: Oh nice, and is there, like, a prize for the winning team? | `follow_up` | respond | wait | 0.36 | 0.95 |
| Speaker 1: Can Wren check snow at Whistler for next weekend? | `role_request` | respond | wait | 0.78 | 0.61 |
| Speaker 1: Before the board dials in, I'd like Quinn to pull up the agenda for today's update. | `role_request` | respond | ignore | 0.79 | 0.35 |
| Speaker 3: Which compliance certifications do you guys currently hold? Our security team's gonna ask first thing. | `request_after_summon` | respond | wait | 0.14 | 0.92 |
| Speaker 2: Jamal, can Tess update the dose itself or does the doctor have to? | `about_to_named_person` | ignore | wait | 0.23 | 0.55 |
| Speaker 3: Alexa, set a timer for twenty minutes. | `other_device` | ignore | respond | 0.86 | 0.27 |
| Speaker 2: How long till the doctor's on? | `question_only_agent_can_answer` | respond | wait | 0.17 | 0.89 |
| Speaker 1: Assistant, could you also put down the, um... actually, never mind, I'll just ask her myself. | `never_mind` | ignore | respond | 0.85 | 0.11 |
| Speaker 4: No, the light one. Reduced fat. | `correction` | respond | ignore | 0.70 | 0.33 |
| Speaker 4: And you were saying the textbook skips the simplifying part, right? | `you_to_person` | ignore | wait | 0.39 | 0.75 |
| Speaker 1: Okay, before we dig in, can you all ping your old colleagues and see who's actually open to a move? | `request_to_people` | ignore | wait | 0.05 | 0.90 |
| Speaker 4: Earlier it said the ridge trail's fine Sunday. So hike first, brunch after? | `about_reported` | ignore | wait | 0.26 | 0.89 |
| Speaker 2: Paul, does Cleo keep the usage report updated after this call? | `about_to_named_person` | ignore | wait | 0.16 | 0.52 |
| Speaker 3: Ren, send me the export before Thursday. | `statement_to_named_person` | ignore | respond | 0.97 | 0.29 |
| Speaker 1: Can you hand me my glasses, they're, um, by the kettle I think? | `unclear_you_person_task` | ignore | wait | 0.14 | 0.74 |
| Speaker 2: Any good places to eat when we get there? | `follow_up` | respond | wait | 0.52 | 0.95 |
| Speaker 1: Deals file's around 80. Split it? | `follow_up` | respond | wait | 0.35 | 0.87 |
| Speaker 2: No, I meant Mauna Kea, the one next to it, measured from the seafloor. | `correction` | respond | ignore | 0.43 | 0.16 |
| Speaker 2: A little swelling in the evenings. Should I be icing it? | `reply_then_request` | respond | wait | 0.65 | 0.92 |
| Speaker 1: Can the assistant just pull up what's on file? | `role_request` | respond | wait | 0.78 | 0.87 |
| Speaker 2: How'd the Declaration of the Rights of Man fit in? | `you_after_invite` | respond | wait | 0.58 | 0.92 |
| Speaker 1: And Pena Palace, do we need to, like, book ahead or just show up? | `follow_up` | respond | wait | 0.60 | 0.91 |
| Speaker 1: Have you two actually sat through one of these reviews before? | `group_question_not_for_agent` | ignore | wait | 0.10 | 0.88 |
| Speaker 2: Okay, I'd like Ace to tell us which two got dropped, you know? | `role_request` | respond | ignore | 0.72 | 0.30 |
| Speaker 3: Lucia, can Ace send calendar invites, or do we have to do that ourselves? | `about_to_named_person` | ignore | wait | 0.16 | 0.65 |
| Speaker 2: Could you pull up the bit where the dog doesn't bark? | `unclear_you` | wait | respond | 0.82 | 0.74 |
| Speaker 2: I think I started it right after that checkup in January two years ago. | `statement` | ignore | respond | 0.95 | 0.05 |
| Speaker 1: Can you pass me the guest notes? | `unclear_you_person_task` | ignore | wait | 0.22 | 0.70 |
| Speaker 1: Send me the audio file after, would you? | `unclear_you_person_task` | ignore | wait | 0.30 | 0.72 |
| Speaker 1: Does she actually want to be forgotten? | `you_after_invite` | respond | wait | 0.36 | 0.86 |
| Speaker 1: Rather? Sounds more guilt trip than wish. | `unclear_after_agent` | wait | ignore | 0.69 | 0.21 |
| Speaker 1: Okay, so, um, how long do you simmer the tomato sauce before the eggs go in? | `you_after_invite` | respond | wait | 0.53 | 0.88 |
| Speaker 3: I'd like Cleo to, um, tell me how much cumin goes in for this size pan. | `role_request` | respond | wait | 0.71 | 0.53 |
| Speaker 1: Okay, snacks are out, dice are rolled, we're finally ready to rob that museum. Take it away. | `opener_to_agent` | respond | ignore | 0.07 | 0.45 |
| Speaker 2: I honestly don't get why it's six turns and not, like, one. | `statement_of_need` | ignore | wait | 0.63 | 0.88 |
| Speaker 1: OK Google, what's three milligrams in micrograms? | `other_device` | ignore | wait | 0.10 | 0.62 |
| Speaker 2: Keep going. Describe the far wall. | `command_no_name` | respond | wait | 0.73 | 0.82 |
| Speaker 2: Can you two, um, check with your teams which fields we actually still use before Friday? | `request_to_people` | ignore | wait | 0.06 | 0.63 |
| Speaker 2: Swelling's down. Mostly evenings now. | `action_to_game_master` | respond | ignore | 0.18 | 0.06 |
| Speaker 4: No, item three. System design. | `correction` | respond | wait | 0.74 | 0.71 |
| Speaker 1: So before we dig in, did you guys already try hooking it up to Salesforce on your end? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.91 |
| Speaker 3: Hold position, like, we've got silver now. | `answer_to_agent_question` | respond | ignore | 0.52 | 0.07 |
| Speaker 3: Can you both do a quick read-through and tell me if my roadmap part sounds too rosy? | `request_to_people` | ignore | wait | 0.10 | 0.84 |
| Speaker 3: Are either of you available Thursday to sign off before it goes to legal? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.89 |
| Speaker 1: Pricing on enterprise? | `follow_up` | respond | wait | 0.75 | 0.88 |
| Speaker 2: Um, the order number's 48213-77, and it was supposed to come last Friday. | `action_to_game_master` | respond | ignore | 0.78 | 0.06 |
| Speaker 1: How about we do the Gruyère detour on day three and split the cheese bill? | `proposal_to_group` | ignore | wait | 0.12 | 0.80 |
| Speaker 2: Okay, I'm working the lock on the dock door, keeping one eye on the corner for the guard. | `action_to_game_master` | respond | ignore | 0.06 | 0.03 |
| Speaker 2: Anita, is Ivy pulling from their actual trust docs, or just summarizing? | `about_to_named_person` | ignore | wait | 0.12 | 0.54 |
| Speaker 2: Alright, anyone doing anything fun after their shift this week? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Speaker 1: Sorry, keep going. | `resume_no_name` | respond | wait | 0.54 | 0.64 |
| Speaker 2: You guys used Rook for times tables before? | `about_question_to_group` | ignore | wait | 0.09 | 0.93 |
| Speaker 1: Can you just call them for me? | `unclear_you` | wait | respond | 0.81 | 0.80 |
| Speaker 3: Decorations next? Ask Wren later? | `about_hypothetical` | ignore | wait | 0.11 | 0.84 |
| Speaker 1: I'd like Kai to turn the music down a bit, Frank's drowning out the gravy debate. | `role_request` | respond | ignore | 0.78 | 0.39 |
| Speaker 3: Kay, did you remember the Yorkshire pudding batter, or is that on me again? | `question_to_named_person` | ignore | wait | 0.52 | 0.60 |
| Speaker 1: Okay team, can everyone just raise a hand if you've actually slept since the release slipped? | `request_to_people` | ignore | wait | 0.03 | 0.94 |
| Speaker 3: So you could do the fifty percent and still stay inside policy, right? That's better than the full refund. | `you_to_person_after_agent` | ignore | wait | 0.37 | 0.87 |
| Speaker 2: Code's E21. Drum won't drain. Next step? | `action_to_game_master` | respond | wait | 0.20 | 0.93 |
| Speaker 1: So did any of you actually finish the volcano diorama over the weekend? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Speaker 3: Sam, can Nova book the Sintra tickets too? | `about_to_named_person` | ignore | wait | 0.17 | 0.52 |
| Speaker 1: Okay, we're here to practice capital cities before Friday's geography test. Can you quiz us? | `opener_to_agent` | respond | wait | 0.52 | 0.92 |
| Speaker 3: Can you both check with your teams which tools they actually use every week? | `request_to_people` | ignore | wait | 0.05 | 0.71 |
| Speaker 1: No, not that one, we watched something after that, the weird one with the hot dog fingers. | `correction` | respond | ignore | 0.79 | 0.11 |
| Speaker 3: Should we save the timeline questions for Quinn at the end? | `about_hypothetical` | ignore | wait | 0.09 | 0.89 |
| Speaker 1: Hi, um, so I'm here for my, uh, the follow-up, and they said to go over my medications first. | `opener_to_agent` | respond | ignore | 0.15 | 0.26 |
| Speaker 3: Should we, uh, maybe ask Luna about the couplet stuff later, after we draft? | `about_hypothetical` | ignore | wait | 0.06 | 0.91 |
| Speaker 1: So why did the Third Estate, like, break off from it? What was the actual fight about? | `request_after_summon` | respond | wait | 0.46 | 0.92 |
| Speaker 2: Okay, and what, um, what rounds do they usually do? Like is there a music round? | `follow_up` | respond | wait | 0.79 | 0.91 |
| Speaker 4: Anyone touched that config before? Who approved it? | `group_question_not_for_agent` | ignore | wait | 0.08 | 0.93 |
| Speaker 3: While Kit checks the floor, I want to look at the jaguar heads. Anything weird about their mouths? | `action_to_game_master` | respond | wait | 0.67 | 0.89 |
| Speaker 1: Is the station's AI core still hostile after what happened last session? | `question_only_agent_can_answer` | respond | wait | 0.51 | 0.93 |
| Speaker 2: Anyway, do we even have ten potatoes? I feel like I saw, like, six in the bag. | `continuing_with_person` | ignore | wait | 0.11 | 0.91 |
| Speaker 4: Should we ask Remy about the traps later, once we're inside? | `about_hypothetical` | ignore | wait | 0.07 | 0.92 |
| Speaker 3: Yeah, and we should, you know, write this up and maybe rename that deploy user while we're at it. | `statement` | ignore | wait | 0.08 | 0.70 |
| Speaker 1: Okay, vote. Saturday hike or brunch? Hands up. | `request_to_people` | ignore | wait | 0.04 | 0.94 |
| Speaker 3: No, wait, not sreyes, that's a service account, the other one, rtorres. | `correction` | respond | wait | 0.71 | 0.76 |
| Speaker 4: Who's actually in the mood for a thriller versus something lighter? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.94 |
| Speaker 2: Left. No, wait, right. Right, toward the humming noise. | `answer_to_agent_question` | respond | ignore | 0.78 | 0.06 |
| Speaker 2: Can you, like, send us a reminder about when to stop it? | `unclear_you` | wait | respond | 0.84 | 0.91 |
| Speaker 1: So if half your clients pay late, then... | `thinking_aloud` | ignore | wait | 0.09 | 0.65 |
| Speaker 1: Should we ask Iris about deposit norms later? | `about_hypothetical` | ignore | wait | 0.05 | 0.91 |
| Speaker 4: Someone call the restaurant and tell them we might be ten minutes late. | `request_to_people` | ignore | wait | 0.08 | 0.90 |
| Speaker 2: OK car, set the cabin temperature to twenty-one degrees. | `other_device` | ignore | wait | 0.30 | 0.68 |
| Speaker 3: Can you jump to the margin bridge slide? | `follow_up` | respond | wait | 0.78 | 0.82 |
| Speaker 2: Hey Google, play spooky organ music. | `other_device` | ignore | wait | 0.10 | 0.51 |
| Speaker 3: I mean, if the rate's locked, two years seems like kind of a no-brainer for us, right? | `statement` | ignore | wait | 0.23 | 0.86 |
| Speaker 2: Has anyone used Clover to, um, dig through old CI runs before? Is it decent at that? | `about_question_to_group` | ignore | wait | 0.15 | 0.94 |
| Speaker 2: Okay, and um, how much of that difference is from those two deferred contracts? | `follow_up` | respond | wait | 0.24 | 0.88 |
| Speaker 2: Okay, how about we each give a quick thumbs up or down first, then talk details? | `proposal_to_group` | ignore | wait | 0.04 | 0.87 |
| Speaker 1: So, um, before we dig in, how many seats are you actually thinking you'll need this year? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.85 |
| Speaker 3: What did you guys, um, think of the analytics add-on in the demo? Worth it or not? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.93 |
| Speaker 3: You always touch the creepy statue, don't you? | `you_to_person` | ignore | wait | 0.17 | 0.78 |
| Speaker 1: I'll press both eyes in at the same time instead of pulling them. | `action_to_game_master` | respond | ignore | 0.10 | 0.06 |
| Speaker 4: Should we, uh, ask Cleo later whether the vault has a time lock? Like before we commit? | `about_hypothetical` | ignore | wait | 0.07 | 0.85 |
| Speaker 4: Quiz each other tomorrow? Library, ten? | `proposal_to_group` | ignore | wait | 0.03 | 0.85 |
| Speaker 1: Hi, yeah, so we're calling because our bill this month is — it's way off, like double what it should be. | `opener_to_agent` | respond | ignore | 0.14 | 0.34 |
| Speaker 2: Wait, can we do the whole batch at once, or does each invite have to go out separately? | `unclear_after_agent` | wait | respond | 0.84 | 0.90 |
| Speaker 4: Has anyone used Cleo to, like, make up backstories for characters? I want one for my ranger. | `about_question_to_group` | ignore | wait | 0.14 | 0.94 |
| Speaker 3: Eighteen? You said we were twenty-one people, didn't you, so we're short, right? | `you_to_person_after_agent` | ignore | wait | 0.56 | 0.85 |
| Speaker 2: I'd like Tess to give listeners one daily habit that actually moves the needle. | `role_request` | respond | ignore | 0.73 | 0.43 |
| Speaker 3: Route us past the bakery on Elm, then. | `follow_up` | respond | wait | 0.50 | 0.86 |
| Speaker 2: You totally knew that one before it even said it, didn't you? | `you_to_person_after_agent` | ignore | wait | 0.71 | 0.65 |
| Speaker 1: So did everyone actually finish it this time, or are we bluffing again? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.92 |
| Speaker 1: Okay, but would you rather do the hike or just hit an onsen and chill? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.51 |
| Speaker 1: Did you ever actually start that magnesium your friend recommended, or is it still in the bag? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.65 |
| Speaker 1: So have you two started packing up your desks yet, or are we all leaving it to the last weekend? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.88 |
| Speaker 3: How about we audit seat usage before renewing anything next quarter? | `proposal_to_group` | ignore | wait | 0.15 | 0.92 |
| Speaker 1: Actually, can you just put it on the board? | `you_after_invite` | respond | wait | 0.60 | 0.84 |
| Speaker 1: Ot— sorry, Malik, can we slip if it's not fixed? | `name_slip_corrected` | ignore | wait | 0.24 | 0.51 |
| Speaker 1: Honestly, I still have no clue how people move a piano up three flights without dying. | `statement_of_need` | ignore | wait | 0.09 | 0.52 |
| Speaker 2: So what are you doing the weekend of the 14th? Free to carry heavy things, perhaps? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.79 |
| Speaker 2: Wait, no, I meant the hint for the next question, not that one. | `correction` | respond | ignore | 0.69 | 0.22 |
| Speaker 1: So the answer's Khufu, I'm pretty sure. | `action_to_game_master` | respond | ignore | 0.46 | 0.07 |
| Speaker 2: Ha, should we ask it to break our tie later? We're clearly not settling this ourselves. | `about_hypothetical` | ignore | wait | 0.09 | 0.86 |
| Speaker 2: Can you draft that change and tag me? | `unclear_you` | wait | respond | 0.85 | 0.79 |
| Speaker 4: Nice, so you can just link QA-418 in your PR when you bump the timeout, right? | `you_to_person_after_agent` | ignore | wait | 0.21 | 0.76 |
| Speaker 1: Are you guys, like, planning to take your monitors yourselves or leave them for the movers? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.92 |
| Speaker 2: Going. Torch? | `reply_to_person` | ignore | wait | 0.05 | 0.82 |
| Speaker 4: Wednesday, really? That assumes nothing else breaks in regression, which feels optimistic. | `unclear_after_agent` | wait | ignore | 0.56 | 0.20 |
| Speaker 3: So can that be backdated to January? | `follow_up` | respond | wait | 0.65 | 0.90 |
| Speaker 1: Actually, never mind, I'll just ask. Can you show us the pilot timeline? | `you_after_invite` | respond | wait | 0.57 | 0.86 |
| Speaker 1: Okay, and what if you've only got, like, four hours on a balcony? Is there something that does better? | `follow_up` | respond | wait | 0.73 | 0.94 |
| Speaker 1: Okay, and is there an audiobook version? For the, uh, commuters among us. | `follow_up` | respond | wait | 0.42 | 0.93 |
| Speaker 2: Nice. Ping us the moment payments is green too? | `follow_up` | respond | wait | 0.79 | 0.84 |
| Speaker 1: Right, I've refilled it, it's at 1.2 now, but if it drops again, do we book an engineer? | `action_to_game_master` | respond | wait | 0.37 | 0.88 |
| Speaker 2: Wait, before that, did you guys, like, actually practice times tables this week? | `group_question_not_for_agent` | ignore | wait | 0.17 | 0.90 |
| Speaker 1: Yeah, um, I'd like Atlas to, like, explain that eighth trick to everyone. | `role_request` | respond | wait | 0.65 | 0.50 |
| Speaker 3: Hmm, I still don't really get where the 300 came from. | `statement_of_need` | ignore | wait | 0.73 | 0.83 |
| Speaker 2: Are you guys staying the whole week or flying back right after the reception? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.90 |
| Speaker 1: Frankie, can you show the... actually, never mind. | `never_mind` | ignore | respond | 0.87 | 0.16 |
| Speaker 2: Check behind the frozen peas, sometimes stuff gets buried back there. | `continuing_with_person` | ignore | wait | 0.03 | 0.69 |
| Speaker 3: Ottie, did you set the table for six or just five? | `question_to_named_person` | ignore | respond | 0.81 | 0.68 |
| Speaker 2: While she's packing up, let's keep going. What's the capital of Paraguay? | `addressed_by_exclusion` | respond | wait | 0.22 | 0.94 |
| Speaker 2: How long until the doctor actually joins the call? | `question_only_agent_can_answer` | respond | wait | 0.19 | 0.92 |
| Speaker 2: Honestly pretty well, but I forget the details. Should we ask Tess later? It took notes. | `about_hypothetical` | ignore | wait | 0.06 | 0.85 |
| Speaker 1: Is it Chisinau? | `answer_to_agent_question` | respond | wait | 0.75 | 0.69 |
| Speaker 1: Okay, can somebody help me shove these desks together so the papier-mâché volcano fits? | `request_to_people` | ignore | wait | 0.05 | 0.94 |
| Speaker 2: But you'd need to free up my Thursdays. | `you_to_person` | ignore | wait | 0.06 | 0.65 |
| Speaker 1: How many left in this round? | `question_only_agent_can_answer` | respond | wait | 0.25 | 0.91 |
| Speaker 2: Wait, is that refundable if, like, it storms? | `follow_up_by_other` | wait | respond | 0.83 | 0.90 |
| Speaker 2: No, not Priya, the afternoon candidate, Marcus. | `correction` | respond | ignore | 0.60 | 0.32 |
| Speaker 4: Chloe, a lot of noise means whatever's in there hears us coming, right? | `to_named_person_after_agent` | ignore | wait | 0.47 | 0.51 |
| Speaker 1: Oh, and um, can you put on some music while we pack these? | `follow_up` | respond | wait | 0.76 | 0.84 |
| Speaker 1: Okay, I'll admit it, I'm running on two hours of sleep because of this book. Who else? | `remark_to_group` | ignore | wait | 0.05 | 0.94 |
| Speaker 2: Mine's got coffee stains on chapter twelve. That's a badge of honor, right? | `reply_to_person` | ignore | wait | 0.03 | 0.81 |
| Speaker 4: Chilton was a car-manual publisher, right? Wild that they took the risk. | `statement` | ignore | wait | 0.13 | 0.77 |
| Speaker 2: And who's doing pickup later, because I've got a dentist at three? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.92 |
| Speaker 3: Ottie, didn't you say you'd read the sequels already? Like, all of them? | `similar_name_person` | ignore | respond | 0.92 | 0.49 |
| Speaker 3: That's better than you expected, right? I thought they'd push us to a new tier. | `you_to_person_after_agent` | ignore | wait | 0.15 | 0.65 |
| Speaker 2: Can you forward me last year's signed order form so I can compare terms? | `unclear_you_person_task` | ignore | wait | 0.31 | 0.81 |
| Speaker 1: I'd like Bea to give us a harder round next, mostly double letters. | `role_request` | respond | wait | 0.75 | 0.53 |
| Speaker 1: Can, did Bolt look over your thesis yesterday, or did you skip that? | `about_to_named_person` | ignore | wait | 0.08 | 0.72 |
| Speaker 1: Could you drop them off Saturday night instead? | `you_to_person` | ignore | wait | 0.09 | 0.60 |
| Speaker 1: Uploaded. Two weeks of entries. | `action_to_game_master` | respond | ignore | 0.76 | 0.06 |
| Speaker 1: Can you send me the gear list? Lost it. | `unclear_you_person_task` | ignore | wait | 0.25 | 0.87 |
| Speaker 1: Who's actually cooking? Anyone done the menu? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.93 |
| Speaker 1: Have any of you used it to, like, generate the migration checklists? Or just lookups? | `about_question_to_group` | ignore | wait | 0.16 | 0.94 |
| Speaker 1: Which day was that technician slot booked for again? | `question_only_agent_can_answer` | respond | wait | 0.20 | 0.91 |
| Speaker 3: Um, what was the name of the mountain her family lived on, you know, in Idaho? | `request_after_summon` | respond | wait | 0.77 | 0.81 |
| Speaker 2: It's pretty thorough, huh, it caught the slip thing right away. | `about_pronoun` | ignore | wait | 0.40 | 0.56 |
| Speaker 2: Okay, photo's uploading now, it's, uh, almost there. | `action_to_game_master` | respond | ignore | 0.16 | 0.04 |
| Speaker 1: Were you thinking of running the sessions yourself, or, like, splitting them up? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.82 |
| Speaker 1: Could you add a Belém stop to Saturday morning then? | `follow_up` | respond | wait | 0.61 | 0.85 |
| Speaker 1: Hi there, so our broadband keeps dropping out, like five or six times every evening. | `opener_to_agent` | respond | ignore | 0.20 | 0.29 |
| Speaker 2: No, I meant the video call, not you. Is the call being recorded? | `correction` | respond | wait | 0.56 | 0.91 |
| Speaker 1: Okay so, um, what if we do our poster on Mount St. Helens instead of Vesuvius? | `proposal_to_group` | ignore | wait | 0.08 | 0.93 |
| Speaker 1: Okay, so, um, can you text the confirmation to my phone instead of email? | `action_to_game_master` | respond | wait | 0.36 | 0.90 |
| Speaker 2: Next question, please. Make it a two-digit squaring one. | `action_to_game_master` | respond | wait | 0.55 | 0.81 |
| Speaker 2: Right, who's actually feeling brave enough to take the pager this week? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.93 |
| Speaker 2: Somebody please go shoo Biscuit off the keyboard before he joins the call. | `request_to_people` | ignore | wait | 0.06 | 0.89 |
| Speaker 4: Hmm, and like, how long for designers, roughly? | `follow_up` | respond | wait | 0.78 | 0.88 |
| Speaker 4: Um, are any of you actually free to sit on interview panels next month? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Speaker 3: I'd like Clover to tell us whether agents get a separate, shorter course. | `role_request` | respond | wait | 0.72 | 0.64 |
| Speaker 2: Okay, who actually slept before this paged? Be honest, I got maybe two hours. | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.90 |
| Speaker 3: How about we revert 8812 now and do the proper fix after breakfast? | `proposal_to_group` | ignore | wait | 0.05 | 0.89 |
| Speaker 1: Okay, and like, do we need to have everything boxed up the night before? | `follow_up` | respond | wait | 0.62 | 0.91 |
| Speaker 2: Okay so, what do you all think, are we keeping the hero banner or, like, ditching it? | `group_question_not_for_agent` | ignore | wait | 0.11 | 0.94 |
| Speaker 1: Like, is that tempo runs or intervals? No idea. | `statement_of_need` | ignore | wait | 0.10 | 0.91 |
| Speaker 3: So are you two actually doing the long runs on Sundays, or switching to Saturdays? | `group_question_not_for_agent` | ignore | wait | 0.02 | 0.85 |
| Speaker 1: Did you have, like, a runbook or did you just wing it? | `continuing_with_person` | ignore | wait | 0.04 | 0.55 |
| Speaker 1: Has either of you actually used Gus to plan a trip, like picking crags or checking conditions? | `about_question_to_group` | ignore | wait | 0.16 | 0.94 |
| Speaker 2: Have you guys ever had it draft the status page update? Mine always sound like ransom notes. | `about_question_to_group` | ignore | wait | 0.21 | 0.90 |
| Speaker 3: Yeah, I've heard, but it's, um, kind of a brick, isn't it? | `reply_to_person` | ignore | wait | 0.09 | 0.81 |
| Speaker 1: Okay, how about loser of this round buys everyone hot chocolate after? | `proposal_to_group` | ignore | wait | 0.04 | 0.91 |
| Speaker 1: I'd like Gus to log a repair request for our washer, it stopped mid-cycle last night. | `role_request` | respond | wait | 0.71 | 0.73 |
| Speaker 1: Okay, how about we each pick one chapter we loved and one we'd throw in the river? | `proposal_to_group` | ignore | wait | 0.05 | 0.92 |
| Speaker 3: And after the stop, carry on to the campsite from there? | `follow_up` | respond | wait | 0.60 | 0.88 |
| Speaker 2: And if hiring freezes? | `follow_up` | respond | wait | 0.47 | 0.87 |
| Speaker 3: Sorry, quick thing, did you send me that invoice yet? | `aside_over_agent` | ignore | wait | 0.12 | 0.62 |
| Speaker 1: Okay, snacks are out, dice are rolled warm. We're ready to finally storm that haunted castle. | `opener_to_agent` | respond | ignore | 0.06 | 0.05 |
| Speaker 1: So if you can send over the forty-seat quote today, we'll get it in front of finance this week. | `you_to_person` | ignore | wait | 0.05 | 0.80 |
| Speaker 4: Should we maybe ask Tess later about other books by this author? Like for next month? | `about_hypothetical` | ignore | wait | 0.07 | 0.92 |
| Speaker 2: Yeah, and like, both of you guys need to Venmo me the deposit by Friday, okay? | `request_to_people` | ignore | wait | 0.04 | 0.66 |
| Speaker 2: So are you actually gonna try snowboarding this time or, like, stick with skis? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.62 |
| Speaker 1: Right, forgot her. Add her. | `reply_to_person` | ignore | wait | 0.27 | 0.78 |
| Speaker 2: Friday afternoons. Otherwise open. | `answer_to_agent_question` | respond | ignore | 0.78 | 0.11 |
| Speaker 3: Okay, and, like, how long is it booked for? Do we have time for Q&A? | `follow_up` | respond | wait | 0.70 | 0.89 |
| Speaker 2: Wait, if it closes at six, is there anything open later for ice? | `follow_up_by_other` | wait | respond | 0.81 | 0.92 |
| Speaker 1: How many times has the connection actually dropped this week? | `question_only_agent_can_answer` | respond | wait | 0.16 | 0.85 |
| Speaker 1: Me, I'll sneak toward the gold, quietly. | `answer_to_agent_question` | respond | ignore | 0.66 | 0.10 |
| Speaker 1: Okay, while he's sneaking, I want to, um, look at the dragon's neck — is there anything weird? | `action_to_game_master` | respond | wait | 0.59 | 0.90 |
| Speaker 2: Can you two come help carry the sofa Saturday? | `request_to_people` | ignore | wait | 0.04 | 0.84 |
| Speaker 3: Did either of you, um, fill up last time you had the car? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Speaker 3: So are you guys, like, planning to present the hiring stuff yourselves, or should I? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.91 |
| Speaker 1: So, um, what did you all think of last quarter's board meeting, like, honestly? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.93 |
| Speaker 1: Anybody else been through one of these supply chain messes before, or is this a first? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.96 |
| Speaker 1: Actually, hang up that call and route us around the motorway instead. | `only_agent_can_do` | respond | wait | 0.62 | 0.85 |
| Speaker 2: Got cash for the toll? I've only got cards. | `continuing_with_person` | ignore | wait | 0.06 | 0.81 |
| Speaker 2: I'd like Tess to tell us what time we'll arrive now. | `role_request` | respond | wait | 0.75 | 0.55 |
| Speaker 1: Can you get them to send a text when it's actually out for delivery? | `unclear_you` | wait | respond | 0.86 | 0.85 |
| Speaker 4: Who's actually planning to come in on moving day? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.94 |
| Speaker 1: Should we ask Otto later? Settle the tricky ones? | `about_hypothetical` | ignore | wait | 0.06 | 0.91 |
| Speaker 3: Anyone actually going Thursday? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Speaker 2: Anyone staying for pudding? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Speaker 3: Let's pause the reconciliation job and retry the migration on its own, outside the pipeline. | `proposal_to_group` | ignore | wait | 0.09 | 0.66 |
| Speaker 2: Fine, but only if we confirm nothing downstream depends on tonight's run. | `reply_to_person` | ignore | wait | 0.07 | 0.60 |
| Speaker 4: Which of those are blocked right now? | `you_after_invite` | respond | wait | 0.58 | 0.93 |
| Speaker 1: Seven minutes? With the lollipop man on duty? I doubt that. | `unclear_after_agent` | wait | ignore | 0.58 | 0.45 |
| Speaker 3: Should we ask Indy afterwards whether there's a group discount? | `about_hypothetical` | ignore | wait | 0.07 | 0.84 |
| Speaker 1: Bea, could you set up the Denver group now... actually, never mind, let's wait. | `never_mind` | ignore | respond | 0.80 | 0.17 |
| Speaker 1: Okay, um, we also need to add shellfish. He got hives from shrimp last summer. | `action_to_game_master` | respond | wait | 0.51 | 0.52 |
| Speaker 1: Send the invites after that. | `command_no_name` | respond | wait | 0.73 | 0.72 |
| Speaker 2: How long did the siege last? | `follow_up` | respond | wait | 0.79 | 0.94 |
| Speaker 1: Anyone actually like Paul? | `group_question_not_for_agent` | ignore | wait | 0.07 | 0.95 |
| Speaker 1: Okay, and turn the music up a bit, I love this one. | `command_no_name` | respond | wait | 0.37 | 0.86 |
| Speaker 2: Put icing sugar on the shopping list then, we've got maybe a cupful. | `follow_up` | respond | ignore | 0.24 | 0.28 |
| Speaker 2: So did anyone actually cry at the funeral scene, or am I the only softie here? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.95 |
| Speaker 2: What if we all, like, chip in twenty each and get the silver moon decorations too? | `proposal_to_group` | ignore | wait | 0.04 | 0.89 |
| Speaker 1: Can you send me a template of that CSV? | `unclear_you` | wait | respond | 0.84 | 0.75 |
| Speaker 1: Um, so, like, should we ask Ivy about the timeline later? I got kinda lost around chapter twelve. | `about_hypothetical` | ignore | wait | 0.06 | 0.91 |
| Speaker 2: Should we ask Penny later how long wraps keep in the fridge? | `about_hypothetical` | ignore | wait | 0.06 | 0.91 |
| Speaker 1: Are you two doing the bonus problems for Friday? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.87 |
| Speaker 1: Rolled. Fourteen. | `answer_to_agent_question` | respond | ignore | 0.60 | 0.07 |
| Speaker 3: So who's brave enough to do the walk to school tomorrow instead? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Speaker 1: Halfway. I keep forgetting what RuBisCO actually grabs. | `reply_to_person` | ignore | wait | 0.22 | 0.71 |
| Speaker 2: Wait, did you bring the flashcards? I left mine on the bus. | `aside_over_agent` | ignore | wait | 0.05 | 0.74 |
| Speaker 2: And, uh, why is Dutch so quick? Is it the vocabulary or— | `follow_up` | respond | wait | 0.70 | 0.88 |
| Speaker 4: Can you send me that spreadsheet with everyone's votes from last month? | `unclear_you_person_task` | ignore | wait | 0.29 | 0.78 |
| Speaker 2: I honestly don't get how they calculate the seat count, like, active users or licensed ones. | `statement_of_need` | ignore | wait | 0.14 | 0.80 |
| Speaker 2: I'd like Iris to book that for three people. | `role_request` | respond | ignore | 0.54 | 0.37 |
| Speaker 3: Are you all actually fine with a four-hour train day, or is that too much? | `group_question_not_for_agent` | ignore | wait | 0.07 | 0.92 |
| Speaker 1: Okay so I still don't get why plants need light if they're making sugar out of CO2 anyway. | `statement` | ignore | wait | 0.15 | 0.94 |
| Speaker 1: Can you guys pass me your notebooks so I can copy the diagram from Thursday's lecture? | `request_to_people` | ignore | wait | 0.03 | 0.87 |
| Speaker 1: Okay, so, um, we're back for the jungle temple thing, like, picking up right where we left off last week. | `opener_to_agent` | respond | ignore | 0.06 | 0.06 |
| Speaker 1: Assistant, can you check if the statue's... actually, never mind. | `never_mind` | ignore | respond | 0.93 | 0.20 |
| Speaker 2: And what if we, um, dropped down to like 200 seats? | `follow_up` | respond | wait | 0.74 | 0.92 |
| Speaker 1: Plenty. Put the warehouse lead ren on the guest list too. | `alias_false_match` | ignore | wait | 0.54 | 0.75 |
| Speaker 4: Okay, while she does that, my cleric lights a torch and looks at the carvings up top. | `action_to_game_master` | respond | ignore | 0.12 | 0.17 |
| Speaker 3: How about we do a dry run of the cutover tomorrow morning, like ten o'clock, all of us? | `proposal_to_group` | ignore | wait | 0.08 | 0.92 |
| Speaker 3: So why don't we just do Tomorrow now and, uh, save Covenant for the summer when we've got more time? | `proposal_to_group` | ignore | wait | 0.04 | 0.85 |
| Speaker 1: Nice. What about the customers table, any constraints still missing there? | `follow_up` | respond | wait | 0.59 | 0.93 |
| Speaker 2: Could that fit into a single two-week block? | `follow_up` | respond | wait | 0.71 | 0.88 |
| Speaker 2: I'd like Cleo to add the metformin too. | `role_request` | respond | wait | 0.68 | 0.68 |
| Speaker 1: Next one. Atorvastatin. | `command_no_name` | respond | wait | 0.60 | 0.71 |
| Speaker 3: You're booking the table, then? Six seats, near the front. | `you_to_person` | ignore | wait | 0.09 | 0.68 |
| Speaker 3: What if we get her brother to bring her there, say it's just a casual dinner? | `proposal_to_group` | ignore | wait | 0.07 | 0.92 |
| Speaker 1: Should we ask Cleo later how long the frosting needs to chill, like, before we spread it? | `about_hypothetical` | ignore | wait | 0.07 | 0.90 |
| Speaker 1: You still driving me Thursday? | `group_question_not_for_agent` | ignore | wait | 0.14 | 0.71 |
| Speaker 4: No, that's Chris's rope. Mine's separate. | `correction` | respond | ignore | 0.08 | 0.06 |
| Speaker 1: Should we ask Pip once we've scoped it? | `about_hypothetical` | ignore | wait | 0.07 | 0.92 |
| Speaker 1: So keep it clean. No guesses on record. | `continuing_with_person` | ignore | wait | 0.04 | 0.62 |
| Speaker 1: How far ahead do we need to book a temporary parking suspension, like for moving day? | `request_after_summon` | respond | wait | 0.55 | 0.89 |
| Speaker 2: Are you, like, planning to roll this out to the sales folks this week, or wait? | `group_question_not_for_agent` | ignore | wait | 0.18 | 0.83 |
| Speaker 3: Huh, okay, so what's actually holding all those connections open? | `follow_up` | respond | wait | 0.46 | 0.93 |
| Speaker 1: Okay so like, who approved that change, and was it reviewed? | `follow_up` | respond | wait | 0.67 | 0.85 |
| Speaker 3: What's the error rate looking like now, like, since the scale-down? | `request_after_summon` | respond | wait | 0.68 | 0.87 |
| Speaker 1: Hi, our broadband keeps dropping out, maybe five or six times every evening. We need it sorted. | `opener_to_agent` | respond | wait | 0.15 | 0.88 |
| Speaker 2: Should we save the pricing stuff and ask Otto about it in the second half? | `about_hypothetical` | ignore | wait | 0.08 | 0.91 |
| Speaker 1: No, wait. Patel's Thursday. Today's Dr. Huang. | `correction` | respond | ignore | 0.67 | 0.10 |
| Speaker 1: So what do you reckon, does staggering cost us much time? | `you_after_invite` | respond | wait | 0.73 | 0.85 |
| Speaker 3: Okay, and is there anything, like, blocking that stairwell, or can we just go down? | `follow_up` | respond | wait | 0.77 | 0.89 |
| Speaker 2: So what are you guys doing after we fill up, like, still going to the market? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.88 |
| Speaker 3: You said we'd do multiplication after this, right? | `you_to_person` | ignore | wait | 0.16 | 0.81 |
| Speaker 1: So for next month, I'm begging, something under three hundred pages. Please. | `statement` | ignore | wait | 0.05 | 0.86 |
| Speaker 2: You should mention the knee to the doctor too, not just the pills. | `you_to_person` | ignore | wait | 0.12 | 0.67 |
| Speaker 1: Right, one of you fill a jug with warm water and the other come hold the torch for me. | `request_to_people` | ignore | wait | 0.06 | 0.79 |
| Speaker 1: What're you learning now? Still Portuguese? | `group_question_not_for_agent` | ignore | wait | 0.10 | 0.67 |
| Speaker 3: Who's getting her there? Anyone volunteering? | `group_question_not_for_agent` | ignore | wait | 0.07 | 0.93 |
| Speaker 1: Fine. What're you all getting her, gifts-wise? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Speaker 2: Okay, add that it clicks when I bend it. | `command_no_name` | respond | wait | 0.79 | 0.79 |
| Speaker 1: Can you hand me that glass of water? My mouth is super dry. | `request_to_people` | ignore | wait | 0.09 | 0.75 |
| Speaker 3: I'll creep down a few steps, real quiet, to get a better look. | `answer_to_agent_question` | respond | ignore | 0.42 | 0.07 |
| Speaker 2: Well, that's not very helpful, we already know it's in the email. | `people_after_agent` | ignore | respond | 0.80 | 0.07 |
| Speaker 3: What did you all think of the eruption video? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Speaker 1: Let's finalize the reqs by Friday. | `proposal_to_group` | ignore | wait | 0.04 | 0.56 |
| Speaker 1: Um, is there like a detour on Route 9 right now? | `request_after_summon` | respond | wait | 0.75 | 0.89 |
| Speaker 2: Hey, can you pass me that water bottle from the back seat? | `request_to_people` | ignore | wait | 0.15 | 0.68 |
| Speaker 2: Should we ask Remy about that after we finish the, like, hypothesis? | `about_hypothetical` | ignore | wait | 0.05 | 0.87 |
| Speaker 2: I'd like Remy to give us, um, a quick checklist for the display board. | `role_request` | respond | wait | 0.58 | 0.69 |
| Speaker 4: Can someone, um, help me carry the heavy cardboard trifold over to the lab sink? | `request_to_people` | ignore | wait | 0.04 | 0.94 |
| Speaker 1: How's everyone's coffee holding up before we dive into this? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.95 |
| Speaker 2: How many modules are left in the team training track? | `question_only_agent_can_answer` | respond | wait | 0.12 | 0.90 |
| Speaker 1: Okay, I put the cap back on and started the rinse cycle. | `action_to_game_master` | respond | ignore | 0.37 | 0.04 |
| Speaker 2: Should we ask Pip to draft the handover notes once we're done? | `about_hypothetical` | ignore | wait | 0.06 | 0.93 |
| Speaker 1: Actually, can you just schedule that reminder for nine-thirty? | `you_after_invite` | respond | wait | 0.42 | 0.83 |
| Speaker 3: Should we ask the assistant to summarize the HR notes later? | `about_hypothetical` | ignore | wait | 0.07 | 0.89 |
| Speaker 3: One hundred and thirty-eight. | `answer_to_agent_question` | respond | ignore | 0.62 | 0.03 |
| Speaker 3: Turn the heat down to low so it doesn't burn. | `reply_to_person` | ignore | wait | 0.08 | 0.58 |
| Speaker 2: Mute my mic. | `request_after_summon` | respond | wait | 0.74 | 0.85 |
| Speaker 4: We still need to rotate all related keys and patch the exposed endpoint before morning. | `statement` | ignore | wait | 0.14 | 0.62 |
| Speaker 1: Definitely not me, I'm sending my stealthy rogue ahead. | `answer_to_agent_question` | respond | ignore | 0.68 | 0.08 |
| Speaker 3: Moving in, weapons ready. | `answer_to_agent_question` | respond | ignore | 0.60 | 0.04 |
| Speaker 4: Have any of you used Dash to pull the feedback forms yet? | `about_question_to_group` | ignore | wait | 0.10 | 0.95 |
| Speaker 4: Should we ask Frankie to pull last year's feedback? | `about_hypothetical` | ignore | wait | 0.10 | 0.92 |
| Speaker 3: And make sure it shows the waived onboarding fee, too. | `continuing_with_person` | ignore | wait | 0.10 | 0.50 |
| Speaker 4: Can you check when that timeout first showed up in main? | `you_after_invite` | respond | wait | 0.55 | 0.90 |
| Speaker 3: Yeah, like, have you guys ever used Penny to practice for actual school tests? | `about_question_to_group` | ignore | wait | 0.08 | 0.92 |
| Speaker 1: Alright, we're all set to pull off this museum heist, so let's get started. | `opener_to_agent` | respond | ignore | 0.05 | 0.20 |
| Speaker 2: What's the minimum user count for the pilot? | `you_after_invite` | respond | wait | 0.28 | 0.88 |
| Speaker 3: Actually, do you offer a discount if we convert to annual? | `you_after_invite` | respond | wait | 0.74 | 0.92 |
| Speaker 1: It's mostly a dull ache, maybe a four out of ten. | `action_to_game_master` | respond | ignore | 0.12 | 0.06 |
| Speaker 2: Actually, can you just tell me if it won the Nebula? | `you_after_invite` | respond | wait | 0.57 | 0.89 |
| Speaker 2: Could you pass me the extra copy of the handout? | `unclear_you_person_task` | ignore | wait | 0.05 | 0.81 |
| Speaker 1: Did you get a chance to review their API rate limits? | `you_to_person` | ignore | wait | 0.12 | 0.76 |
| Speaker 3: I'd like Juno to pull up the projected software licensing costs for next quarter. | `role_request` | respond | ignore | 0.79 | 0.47 |
| Speaker 2: You better watch the dial closely so it doesn't go too high. | `you_to_person_after_agent` | ignore | wait | 0.25 | 0.58 |
| Speaker 1: So, who else survived the schema changes yesterday without needing three cups of coffee? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.94 |
| Speaker 1: Hi, we're here for my follow-up visit. | `opener_to_agent` | respond | ignore | 0.08 | 0.15 |
| Speaker 3: Um, who directed the first movie adaptation? | `request_after_summon` | respond | wait | 0.16 | 0.93 |
| Speaker 2: You guys finish the reading? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.90 |
| Speaker 3: Yeah, totally. Should we ask Juno about how long water stays in the ocean later? | `about_hypothetical` | ignore | wait | 0.07 | 0.88 |
| Speaker 1: Did you bring the snacks? | `aside_over_agent` | ignore | wait | 0.09 | 0.78 |
| Speaker 3: Can you pass me that printed chart on the desk? | `unclear_you_person_task` | ignore | wait | 0.12 | 0.82 |
| Speaker 3: No, I meant the other one you skipped, the alkali metal. | `correction` | respond | wait | 0.78 | 0.74 |
| Speaker 3: Did everyone finish reviewing the presentation slides? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.94 |
| Speaker 2: Can we rent them at the ranger station, or do we need to buy them? | `follow_up` | respond | wait | 0.78 | 0.93 |
| Speaker 4: Do you have the exact error code from those timeouts? | `you_after_invite` | respond | wait | 0.72 | 0.90 |
| Speaker 3: I still don't really get how the clouds actually form up there. | `statement_of_need` | ignore | wait | 0.14 | 0.90 |
| Speaker 1: Anyway, you promised you'd help me remember my melatonin dosage if I forgot. | `you_to_person` | ignore | wait | 0.35 | 0.61 |
| Speaker 1: A-C-C-O-M-O-D-A-T-E. | `answer_to_agent_question` | respond | ignore | 0.67 | 0.04 |
| Speaker 2: D-E-F-I-N-I-T-E-L-Y. | `answer_to_agent_question` | respond | ignore | 0.79 | 0.04 |
| Speaker 2: Wait, is the quiz tomorrow? | `aside_over_agent` | ignore | wait | 0.11 | 0.82 |
| Speaker 1: Okay, um, can one of you guys check the glovebox for the fuel card? | `request_to_people` | ignore | wait | 0.13 | 0.89 |
| Speaker 1: Um, how much is unleaded there? | `follow_up` | respond | wait | 0.79 | 0.82 |
| Speaker 3: Let's write a short response about the rust symbolism. | `proposal_to_group` | ignore | wait | 0.07 | 0.87 |
| Speaker 1: How many attempts are left in this module? | `question_only_agent_can_answer` | respond | wait | 0.40 | 0.91 |
| Speaker 1: Hi, so um, the boiler just cut out and there's no hot water, we're stuck. | `opener_to_agent` | respond | ignore | 0.19 | 0.44 |
| Speaker 2: Sure, give me a sec, it's in that blue box. | `action_to_game_master` | respond | ignore | 0.06 | 0.05 |
| Speaker 3: Is that author still active in the industry? | `follow_up` | respond | wait | 0.63 | 0.87 |
| Speaker 2: Is the doctor already logged into this call yet? | `question_only_agent_can_answer` | respond | wait | 0.11 | 0.90 |
| Speaker 1: So basically, the light energy is just powering the whole system? | `statement` | ignore | wait | 0.29 | 0.91 |
| Speaker 3: Okay, so how do I use that to simplify twelve over eighteen? | `follow_up` | respond | wait | 0.57 | 0.93 |
| Speaker 1: Set a timer for ten minutes now. | `command_no_name` | respond | wait | 0.67 | 0.85 |
| Speaker 2: Also set the first one for next Monday at 9 AM. | `command_no_name` | respond | wait | 0.71 | 0.83 |
| Speaker 2: Did you hear that? We're almost out of fuel. | `you_to_person_after_agent` | ignore | wait | 0.07 | 0.64 |
| Speaker 2: It's surprisingly fast with that data lookup. | `about_pronoun` | ignore | respond | 0.84 | 0.05 |
| Speaker 2: Ren, make sure we log the client IDs too. | `statement_to_named_person` | ignore | respond | 0.97 | 0.30 |
| Speaker 4: Has anyone used this tool to draft compliance summaries? | `about_question_to_group` | ignore | wait | 0.12 | 0.95 |
| Speaker 1: Does anyone have any concerns about the data retention policies? | `group_question_not_for_agent` | ignore | wait | 0.07 | 0.95 |
| Speaker 1: Honestly, I think most of us learn languages way too formally, right? | `statement` | ignore | wait | 0.08 | 0.77 |
| Speaker 3: Wait, did you hear what Luna told me earlier? She said my pronunciation sounds like a confused owl. | `about_quoted` | ignore | wait | 0.06 | 0.75 |
| Speaker 1: Anyone got the diagram? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.95 |
| Speaker 3: Okay, set a budget reminder for us then. | `follow_up` | respond | wait | 0.76 | 0.83 |
| Speaker 2: Have any of you used Remy to check your citations yet? | `about_question_to_group` | ignore | wait | 0.07 | 0.93 |
| Speaker 2: Wait, changing passwd permissions? That seems weirdly specific for an accident. | `unclear_after_agent` | wait | ignore | 0.14 | 0.36 |
| Speaker 1: I'd like Cleo to find a nearby pharmacy. | `role_request` | respond | wait | 0.67 | 0.50 |
| Speaker 1: Hey, I'm here about my left knee, it's been bothering me all week. | `opener_to_agent` | respond | ignore | 0.13 | 0.22 |
| Speaker 2: Lima, right? | `reply_to_person` | ignore | wait | 0.35 | 0.57 |
| Speaker 2: Hey, can you mute my microphone for a sec? | `unclear_you` | wait | respond | 0.80 | 0.86 |
| Speaker 2: Add a note about the safety briefing. | `command_no_name` | respond | wait | 0.70 | 0.79 |
| Speaker 3: Just to be safe, let's verify the room number. | `continuing_with_person` | ignore | wait | 0.14 | 0.82 |
| Speaker 1: Who hit the flaky test before lunch? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.93 |
| Speaker 2: Did anyone check the logs yet? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.94 |
| Speaker 2: Okay, and how much free space did it show right before it filled up? | `follow_up` | respond | wait | 0.68 | 0.87 |
| Speaker 2: I'd like Max to check the weather in London for the weekend. | `role_request` | respond | ignore | 0.73 | 0.41 |
| Speaker 3: Can you email me the link to the job description? | `unclear_you_person_task` | ignore | wait | 0.18 | 0.79 |
| Speaker 2: What are you all doing for dinner tonight? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.93 |
| Speaker 2: And how is 'February' spelled? | `follow_up` | respond | wait | 0.77 | 0.87 |
| Speaker 2: Otto, pull up the... actually, never mind. | `never_mind` | ignore | respond | 0.87 | 0.21 |
| Speaker 1: So, are we packing sandwiches or buying lunch tomorrow? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.94 |
| Speaker 3: Hey Google, what's the weather like this afternoon? | `other_device` | ignore | wait | 0.09 | 0.52 |
| Speaker 4: Should we ask Ember about the bibliography format? | `about_hypothetical` | ignore | wait | 0.07 | 0.93 |
| Speaker 1: So, do I need to hold the button for longer? | `you_after_invite` | respond | wait | 0.54 | 0.86 |
| Speaker 1: yeah, fully | `answer_to_agent_question` | respond | ignore | 0.68 | 0.04 |
| Speaker 3: Keep recording for the summary. | `command_no_name` | respond | wait | 0.60 | 0.75 |
| Speaker 2: You're probably better at reading the metrics than I am, right? | `you_to_person` | ignore | wait | 0.17 | 0.87 |
| Speaker 1: So, when exactly are we pushing the beta out? | `you_after_invite` | respond | wait | 0.15 | 0.85 |
| Speaker 3: No, the other one, take the highway off-ramp. | `correction` | respond | wait | 0.47 | 0.72 |
| Speaker 2: Oh no, I totally forgot those. How bad is it? | `reply_to_person` | ignore | wait | 0.06 | 0.64 |
| Speaker 1: Hey, can you show me the latest error count from the logs? | `you_after_invite` | respond | wait | 0.47 | 0.88 |
| Speaker 4: Has anyone else seen the latency spikes on the staging server? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.95 |
| Speaker 5: Can someone physically check the rack status in the data center? | `request_to_people` | ignore | wait | 0.04 | 0.93 |
| Speaker 1: Did you guys hear how Ivy accidentally called Spanish 'Castilian' just now? | `about_reported` | ignore | wait | 0.05 | 0.92 |
| Speaker 1: I'd like Penny to list the three driest cities in the state. | `role_request` | respond | ignore | 0.67 | 0.32 |
| Speaker 2: Anyway, maybe we should just grab some pizza and watch it together? | `proposal_to_group` | ignore | wait | 0.04 | 0.87 |
| Speaker 3: Also, let's not forget to check their references properly this time. | `statement` | ignore | wait | 0.03 | 0.60 |
| Speaker 1: Right, we're here to sort out that nightmare spelling list before Friday. | `opener_to_agent` | respond | ignore | 0.07 | 0.12 |
| Speaker 1: Isis, can you check if the news app is working? | `similar_name_person` | ignore | respond | 0.91 | 0.37 |
| Speaker 1: Isis, do you know if Iris has access to the latest gardening guides? | `about_to_named_person` | ignore | wait | 0.37 | 0.72 |
| Speaker 1: I’d like Iris to pull up a list of slug-resistant plants. | `role_request` | respond | ignore | 0.78 | 0.41 |
| Speaker 3: Okay, summarize the main themes now. | `command_no_name` | respond | wait | 0.76 | 0.86 |
| Speaker 4: Gus, actually, never mind. | `never_mind` | ignore | respond | 0.90 | 0.10 |
| Speaker 1: Which region is driving that spike? | `follow_up` | respond | wait | 0.77 | 0.91 |
| Speaker 2: Should we ask Ember about that one? | `about_hypothetical` | ignore | wait | 0.08 | 0.91 |
| Speaker 1: Who else studied this chapter before class? | `group_question_not_for_agent` | ignore | wait | 0.08 | 0.89 |
| Speaker 2: Can we increase that temporarily? | `follow_up` | respond | wait | 0.31 | 0.93 |
| Speaker 1: I’m still not clear on how that affects the launch date. | `statement_of_need` | ignore | wait | 0.73 | 0.81 |
| Speaker 2: I was just wondering if the security module is actually that long... | `thinking_aloud` | ignore | wait | 0.38 | 0.83 |
| Speaker 2: Please mark the security module as optional for the junior staff. | `command_no_name` | respond | wait | 0.65 | 0.84 |
| Speaker 2: Has anyone actually used it to check disk space before? | `about_question_to_group` | ignore | wait | 0.07 | 0.94 |
| Speaker 3: Should we ask Pip what's taking up the space? | `about_hypothetical` | ignore | wait | 0.07 | 0.93 |
| Speaker 2: Who is eating bread this weekend? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.93 |
| Speaker 1: Hey, can you pull up the data for that? | `you_after_invite` | respond | wait | 0.57 | 0.82 |
| Speaker 3: I wonder if it remembers the... | `thinking_aloud` | ignore | wait | 0.17 | 0.54 |
| Speaker 1: Someone wash the greens, please. | `request_to_people` | ignore | wait | 0.05 | 0.90 |
| Speaker 3: Now remove the old test account. | `command_no_name` | respond | wait | 0.65 | 0.82 |
| Speaker 1: Okay, I’m hiding behind the crates until I hear that thud, then I move. | `action_to_game_master` | respond | ignore | 0.67 | 0.04 |
| Speaker 1: I mean, it literally said, 'Don't panic, it's just a quiz' to me last time. Kind of weird, right? | `about_quoted` | ignore | wait | 0.12 | 0.88 |
| Speaker 2: Can someone grab the coffee from the kitchen? | `request_to_people` | ignore | wait | 0.05 | 0.93 |
| Speaker 1: You should check if the dates are still open. | `you_to_person` | ignore | wait | 0.19 | 0.59 |
| Speaker 1: Connor, can Ace update the document again? | `about_to_named_person` | ignore | wait | 0.21 | 0.58 |
| Speaker 2: Hey Cortana, remind me to check the server status later. | `other_device` | ignore | respond | 0.95 | 0.27 |
| Speaker 1: Has either of you used the chatbot for anything else recently? | `about_question_to_group` | ignore | wait | 0.19 | 0.91 |
| Speaker 3: You should highlight that to the stakeholders. | `you_to_person_after_agent` | ignore | wait | 0.41 | 0.76 |
| Speaker 1: So, did you guys finish the homework before starting this? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.92 |
| Speaker 1: Petra is typing, so can you read the next word for her? | `addressed_by_exclusion` | respond | wait | 0.74 | 0.84 |
| Speaker 1: You didn’t mention that 5d part before, did you? | `you_to_person_after_agent` | ignore | respond | 0.86 | 0.75 |
| Speaker 2: Please start writing the incident ticket now. | `request_to_people` | ignore | wait | 0.17 | 0.82 |
| Speaker 3: Anyone want a coffee after? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.95 |
| Speaker 5: Can you show me the raw data for the last hour? | `follow_up` | respond | wait | 0.52 | 0.92 |
| Speaker 1: Make sure you check the file before sharing it. | `you_to_person_after_agent` | ignore | wait | 0.29 | 0.70 |
| Speaker 2: You should update the status to critical then. | `you_to_person_after_agent` | ignore | wait | 0.58 | 0.82 |
| Speaker 1: Honestly, I always mix up nitrogen and neon. Like, which one is gas? | `statement` | ignore | wait | 0.53 | 0.93 |
| Speaker 1: Who handles the data cleaning on your end? | `group_question_not_for_agent` | ignore | wait | 0.41 | 0.88 |
| Speaker 1: Sage, or I mean Raj, did you write that down too? | `name_slip_corrected` | ignore | wait | 0.56 | 0.65 |
| Speaker 3: Should we ask Kai for a gear list later? | `about_hypothetical` | ignore | wait | 0.08 | 0.92 |
| Speaker 3: Yeah, like, where do you even put all those pots? | `reply_to_person` | ignore | wait | 0.03 | 0.89 |
| Speaker 3: Should we ask Frankie about the database lock? | `about_hypothetical` | ignore | wait | 0.07 | 0.90 |
| Speaker 2: Did anyone grab lunch before this mess started? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.93 |
| Speaker 4: By the way, what's everyone having for lunch today? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.94 |
| Speaker 2: Please send the current participant list to the project inbox. | `command_no_name` | respond | wait | 0.61 | 0.86 |
| Speaker 2: Who else has an opinion on the candidate's technical skills? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.93 |
| Speaker 2: What are your plans for lunch today? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.88 |
| Speaker 1: Hey, can you slide that character sheet over to me? | `unclear_you_person_task` | ignore | wait | 0.17 | 0.84 |
| Speaker 1: Hi, um, we're here because the washing machine just stopped working again. | `opener_to_agent` | respond | ignore | 0.15 | 0.28 |
| Speaker 1: Let's just order a backup heater for tonight. | `proposal_to_group` | ignore | wait | 0.14 | 0.67 |
| Speaker 2: So, maybe we should start the audit with the perimeter firewalls first? | `proposal_to_group` | ignore | wait | 0.11 | 0.76 |
| Speaker 2: Has anyone had a chance to look at the latest compliance logs yet? | `group_question_not_for_agent` | ignore | wait | 0.08 | 0.94 |
| Speaker 3: Have any of you used Pip for planting schedules? | `about_question_to_group` | ignore | wait | 0.11 | 0.95 |
| Speaker 2: sorry, quick question, did you check the API gateway too? | `aside_over_agent` | ignore | wait | 0.40 | 0.87 |
| Speaker 1: Has either of you used this app before? | `about_question_to_group` | ignore | wait | 0.17 | 0.93 |
| Speaker 2: Do we need manager approval for amounts over fifty? | `follow_up` | respond | wait | 0.63 | 0.91 |
| Speaker 2: You, reserve two seats on the morning flight. | `you_after_invite` | respond | wait | 0.61 | 0.78 |
| Speaker 3: Can you add our details to the hotel booking too? | `follow_up` | respond | wait | 0.66 | 0.87 |
| Speaker 1: This is getting a little confusing for all of us, isn't it? | `remark_to_group` | ignore | wait | 0.14 | 0.87 |
| Speaker 2: You should double-check the timestamps, you missed one last time. | `you_to_person_after_agent` | ignore | wait | 0.74 | 0.62 |
| Speaker 2: Should we ask the assistant to dig into the correlation between the cache purge and the spike? | `about_hypothetical` | ignore | wait | 0.09 | 0.89 |
| Speaker 1: Guys, text the venue to confirm the date. | `request_to_people` | ignore | wait | 0.06 | 0.84 |
| Speaker 3: Anyone used it for anything specific lately? | `about_question_to_group` | ignore | wait | 0.07 | 0.93 |
| Speaker 3: You heard that? Pretty specific answer. | `you_to_person_after_agent` | ignore | wait | 0.36 | 0.75 |
| Speaker 2: No, I'm staying back. I'll keep watch. | `answer_to_agent_question` | respond | ignore | 0.30 | 0.05 |
| Speaker 1: Has anyone used Juno to check their vocabulary lists yet? | `about_question_to_group` | ignore | wait | 0.07 | 0.94 |
| Speaker 1: Okay, I think the answer is 'environment'. | `action_to_game_master` | respond | ignore | 0.08 | 0.06 |
| Speaker 2: What is everyone doing after this study session? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.94 |
| Speaker 1: Setting up for the seven o'clock check. | `opener_to_agent` | respond | ignore | 0.08 | 0.05 |
| Speaker 1: Just the Lisinopril. What's the dose? | `reply_then_request` | respond | wait | 0.73 | 0.86 |
| Speaker 2: No, that's all for now, thanks. | `answer_to_agent_question` | respond | ignore | 0.65 | 0.04 |
| Speaker 3: Do you guys want to join for drinks later? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.91 |
| Speaker 1: Hiro, did Orion mention the alarm limit? | `about_to_named_person` | ignore | wait | 0.06 | 0.52 |
| Speaker 5: Tess, can you show me a map of— actually, never mind. | `never_mind` | ignore | respond | 0.80 | 0.14 |
| Speaker 1: That seems too low for this time of day, I expected more traffic. | `unclear_after_agent` | wait | ignore | 0.48 | 0.18 |
| Speaker 3: Has anyone else been using the AI to monitor the network latency? | `about_question_to_group` | ignore | wait | 0.12 | 0.93 |
| Speaker 2: two hundred is pretty high don't you think | `you_to_person_after_agent` | ignore | wait | 0.66 | 0.85 |
| Speaker 1: Could you slide that soil test file over to me? I need to double-check the nitrogen levels. | `unclear_you_person_task` | ignore | wait | 0.32 | 0.84 |
| Speaker 2: Is 'childs' ever used in any dialect? | `follow_up` | respond | wait | 0.52 | 0.95 |
| Speaker 2: That seems high for the technical section. | `unclear_after_agent` | wait | ignore | 0.39 | 0.20 |
| Speaker 3: I'd like Penny to email this report to the hiring committee. | `role_request` | respond | wait | 0.38 | 0.50 |
| Speaker 2: You're sure? I hate cleaning filters. | `you_to_person_after_agent` | ignore | wait | 0.71 | 0.73 |
| Speaker 2: That seems way too high for this climate. | `unclear_after_agent` | wait | ignore | 0.69 | 0.10 |
| Speaker 2: Wait, why is six the common denominator? Isn't it the biggest number? | `unclear_after_agent` | wait | respond | 0.85 | 0.91 |
| Speaker 2: So, is fraction addition generally considered a major stumbling block for middle schoolers? | `you_after_invite` | respond | wait | 0.40 | 0.93 |
| Speaker 2: Anyone actually hungry, or is this just a thirsty day? | `group_question_not_for_agent` | ignore | wait | 0.05 | 0.94 |
| Speaker 2: Stuck? It's been 'stuck' for three days. | `unclear_after_agent` | wait | respond | 0.81 | 0.35 |
| Speaker 1: Who else is upset about this? | `group_question_not_for_agent` | ignore | wait | 0.04 | 0.92 |
| Speaker 1: Does it auto-renew? | `follow_up_by_other` | wait | respond | 0.86 | 0.85 |
| Speaker 3: You might want to note that in the docs. | `you_to_person_after_agent` | ignore | wait | 0.38 | 0.76 |
| Speaker 4: Let's freeze writes during the window. | `proposal_to_group` | ignore | wait | 0.03 | 0.50 |
| Speaker 1: What do you think about the btree? | `you_after_invite` | respond | wait | 0.66 | 0.89 |
| Speaker 4: You guys look really relaxed, is it just me or is it quiet? | `remark_to_group` | ignore | wait | 0.04 | 0.93 |
| Speaker 2: Is anyone else bringing a backup player for next week? | `group_question_not_for_agent` | ignore | wait | 0.06 | 0.92 |
| Speaker 1: What did you two grab to eat before we left? | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.85 |
| Speaker 2: Ada, what's the preheat setting, actually, never mind. | `never_mind` | ignore | respond | 0.86 | 0.37 |
| Speaker 1: That seems a bit low for a safe doneness standard. | `unclear_after_agent` | wait | ignore | 0.69 | 0.14 |
| Speaker 3: I guess we need to look at the video... just the video loader. | `thinking_aloud` | ignore | wait | 0.14 | 0.57 |
| Speaker 3: Can you pull up the latest screening scores for the backend roles? | `request_after_summon` | respond | wait | 0.79 | 0.86 |
| Speaker 3: Maybe we should move the final interviews for this group to next Tuesday? | `proposal_to_group` | ignore | wait | 0.09 | 0.84 |
| Speaker 2: Fine, I go for the head. | `reply_to_person` | ignore | respond | 0.85 | 0.04 |
| Speaker 2: Can, did you know that already or is that new info? | `to_named_person_after_agent` | ignore | wait | 0.64 | 0.84 |
| Speaker 2: How much water should I add to the misting bottle? | `follow_up` | respond | wait | 0.76 | 0.91 |
| Speaker 3: What is everyone doing for lunch tomorrow, I am starving | `group_question_not_for_agent` | ignore | wait | 0.03 | 0.93 |
| Speaker 2: I assume so, but why would you ask that? | `reply_to_person` | ignore | wait | 0.08 | 0.73 |
| Speaker 2: Hey, did you save the last draft? | `aside_over_agent` | ignore | wait | 0.19 | 0.83 |
| Speaker 1: Hi, we're here because the washer is making a really loud grinding noise. | `opener_to_agent` | respond | ignore | 0.30 | 0.38 |
| Speaker 2: OK car, what's the gas price at the nearest station? | `other_device` | ignore | wait | 0.23 | 0.67 |
| Speaker 1: Can someone check the time on their phone for me? | `request_to_people` | ignore | wait | 0.08 | 0.95 |
| Speaker 3: I'd like Penny to describe the dungeon entrance. | `role_request` | respond | ignore | 0.54 | 0.45 |
| Speaker 1: It has been getting worse since March really. | `statement` | ignore | respond | 0.80 | 0.04 |
| Speaker 2: Is that higher than last year's rate, Pedro? | `follow_up_by_other` | wait | respond | 0.88 | 0.34 |

**Graded lines, no single right decision** (129)

| Line | Kind | Jev | addressed | question |
|---|---|---|---|---|
| Speaker 3: Cleo would know what the shuttle costs. | `invite` | ignore | 0.16 | 0.39 |
| Speaker 1: Pip would know a few. | `invite` | ignore | 0.21 | 0.28 |
| Speaker 1: Bye, Remy! | `farewell_named` | respond | 0.86 | 0.03 |
| Speaker 2: Ada would know what to add to the glaze. | `invite` | ignore | 0.17 | 0.31 |
| Speaker 2: The assistant would know. Ask it. | `invite` | wait | 0.19 | 0.67 |
| Speaker 1: I'd like Bolt's take on whether we need three tents. | `indirect_wish` | wait | 0.78 | 0.61 |
| Speaker 3: Ask Gus; it might have a better spot for it. | `invite` | wait | 0.11 | 0.81 |
| Speaker 2: I'd like Orion's view on how much time to leave for questions. | `indirect_wish` | ignore | 0.67 | 0.48 |
| Speaker 2: Could one of you ask Wren to find the name of Paul's father? | `relayed_invite` | wait | 0.09 | 0.94 |
| Speaker 2: Could you get Ace to outline a simple cash-flow forecast for us? | `relayed_invite` | wait | 0.24 | 0.84 |
| Speaker 3: Lars, get it to tell us if there's another exit. | `relayed_invite` | ignore | 0.09 | 0.18 |
| Speaker 1: I'd love Cleo's take on whether 34 points is wildly optimistic for us. | `indirect_wish` | wait | 0.66 | 0.63 |
| Speaker 2: Great, thanks for that. | `thanks` | respond | 0.85 | 0.03 |
| Speaker 2: Somewhere. Can you get it to pull up my last visit notes? | `relayed_invite` | wait | 0.30 | 0.75 |
| Speaker 1: Huh, I'd really like Clover's take on whether we even need an agency here. | `indirect_wish` | wait | 0.44 | 0.66 |
| Speaker 3: I'd love to know what Otto thinks about ending on a rhetorical question, honestly. | `indirect_wish` | wait | 0.43 | 0.82 |
| Speaker 2: Can, get it to make me one of those plans too, but for Portuguese, before Lisbon in June. | `relayed_invite` | wait | 0.29 | 0.63 |
| Speaker 4: I'd love to hear what Nova thinks about whether Yellowstone could actually blow. | `indirect_wish` | wait | 0.48 | 0.72 |
| Speaker 1: Can you have it note that I carry an EpiPen anyway? | `relayed_invite` | wait | 0.76 | 0.87 |
| Speaker 3: Okay, assistant, that's enough for now. | `stop_named` | respond | 0.94 | 0.08 |
| Speaker 3: I'd kinda like Ivy's take on whether that service account should even have S3 write access. | `indirect_wish` | wait | 0.38 | 0.82 |
| Speaker 1: Honestly, just ask Indy, it'll know what we did last time. | `invite` | wait | 0.18 | 0.55 |
| Speaker 1: Okay. Thanks. | `thanks` | ignore | 0.41 | 0.03 |
| Speaker 1: Freya, get it to slow down for me. | `relayed_invite` | ignore | 0.19 | 0.18 |
| Speaker 1: Ines, can you get it to pull up the sleep questionnaire for me? I can't find the button. | `relayed_invite` | ignore | 0.10 | 0.21 |
| Speaker 3: Thanks, Penny, that's a big help. | `thanks_named` | respond | 0.91 | 0.02 |
| Speaker 4: Indy would know, it's literally made for this. | `invite` | ignore | 0.17 | 0.18 |
| Speaker 1: Want Frankie's take on rollback versus just bumping the pool. | `indirect_wish` | wait | 0.26 | 0.83 |
| Speaker 1: Okay, thanks, that's really helpful. | `thanks` | ignore | 0.56 | 0.03 |
| Speaker 3: Cal, can you get it to tell us how much time a lockpick roll actually takes? | `relayed_invite` | ignore | 0.18 | 0.28 |
| Speaker 2: Orion would know. | `invite` | ignore | 0.21 | 0.27 |
| Speaker 2: Thanks Atlas, that's a really helpful detail. | `thanks_named` | respond | 0.90 | 0.03 |
| Speaker 2: Just ask Ada about the gravy too, honestly. | `invite` | wait | 0.15 | 0.72 |
| Speaker 1: Sage would know if errors are dropping. | `invite` | ignore | 0.22 | 0.34 |
| Speaker 2: If we need a realistic date, Wren would know. | `invite` | ignore | 0.34 | 0.45 |
| Speaker 1: Thanks, Wren, that really helps. | `thanks_named` | respond | 0.92 | 0.02 |
| Speaker 2: Okay, Tess, that's plenty, stop there before spoilers. | `stop_named` | respond | 0.97 | 0.07 |
| Speaker 3: Okay, great, thanks for that. | `thanks` | ignore | 0.79 | 0.03 |
| Speaker 2: Atlas would know how many seats are actually sitting idle. | `invite` | ignore | 0.17 | 0.25 |
| Speaker 1: I'd love to hear what Ember thinks about bribing friends with pizza versus paying movers. | `indirect_wish` | wait | 0.26 | 0.82 |
| Speaker 1: Right. Thanks for that. | `thanks` | ignore | 0.77 | 0.03 |
| Speaker 1: Divya, can you get Pip to pull up the pilot timeline from last week's deck? | `relayed_invite` | ignore | 0.08 | 0.28 |
| Speaker 2: Can you get it to add the coffee to my notes? I'll mess it up. | `relayed_invite` | wait | 0.73 | 0.87 |
| Speaker 3: Is traffic bad on Mill Road though? Remy would know. | `invite` | wait | 0.37 | 0.70 |
| Speaker 3: Can one of you have Tess pull up the rubric for me? My laptop's dead. | `relayed_invite` | wait | 0.21 | 0.94 |
| Speaker 1: Can you get it to give us the Mesopotamia question now? | `relayed_invite` | wait | 0.35 | 0.81 |
| Speaker 3: Oh nice, that's exactly it. Thanks, Tess. | `thanks_named` | respond | 0.92 | 0.02 |
| Speaker 2: Ask Dash later if the lot fills up early. | `invite` | ignore | 0.09 | 0.37 |
| Speaker 2: Raj, get it to give me a squaring trick, I'm hopeless at those. | `relayed_invite` | ignore | 0.15 | 0.37 |
| Speaker 3: Great, thanks. | `thanks` | respond | 0.86 | 0.02 |
| Speaker 1: If we're stuck on her backstory, Tess would know, honestly. | `invite` | ignore | 0.11 | 0.33 |
| Speaker 4: Okay, that's enough for now, Milo, thanks. | `stop_named` | ignore | 0.63 | 0.03 |
| Speaker 3: Who's leading week three? Actually, Penny would know. | `invite` | wait | 0.44 | 0.58 |
| Speaker 3: Dessert—what goes with all this? Ask the assistant, it'll know. | `invite` | wait | 0.42 | 0.64 |
| Speaker 2: Iris, stop there, that's enough for now. | `stop_named` | respond | 0.97 | 0.07 |
| Speaker 1: See? Ask Ivy the rest. | `invite` | ignore | 0.18 | 0.35 |
| Speaker 2: See, Wren knows everything about caffeine. | `invite` | ignore | 0.30 | 0.05 |
| Speaker 4: Maya, can you get it to email me that reading schedule? | `relayed_invite` | ignore | 0.12 | 0.17 |
| Speaker 2: I have to duck out early today, bye Orion! | `farewell_named` | ignore | 0.65 | 0.03 |
| Speaker 1: Oh perfect, thanks for that. | `thanks` | respond | 0.85 | 0.03 |
| Speaker 1: I'd love to know what Ivy thinks is the most likely essay question. | `indirect_wish` | wait | 0.38 | 0.74 |
| Speaker 3: See, Cleo would know. Always ask Cleo before you guess. | `invite` | ignore | 0.11 | 0.07 |
| Speaker 3: Okay Cleo, that's enough, Tomas is already eyeing the oven door. | `stop_named` | respond | 0.83 | 0.12 |
| Speaker 1: Great, thanks. | `thanks` | ignore | 0.78 | 0.02 |
| Speaker 3: Thanks, Tess, that's exactly the number I was trying to remember. | `thanks_named` | respond | 0.82 | 0.02 |
| Speaker 3: Perfect, thank you, that's super helpful. | `thanks` | respond | 0.85 | 0.02 |
| Speaker 1: Can one of you have Dash pull up, like, discussion questions for the essays? My mic's being weird. | `relayed_invite` | wait | 0.29 | 0.93 |
| Speaker 1: Um, can one of you get Wren to, like, check my derivative for problem four? I'm totally lost. | `relayed_invite` | wait | 0.14 | 0.94 |
| Speaker 4: I'd kinda like to know what Wren thinks about which practice problems are, like, most worth doing. | `indirect_wish` | wait | 0.31 | 0.82 |
| Speaker 1: Okay Tess, that's all for now. | `stop_named` | respond | 0.91 | 0.05 |
| Speaker 3: Is The Platform scary? Kai would know. | `invite` | wait | 0.31 | 0.70 |
| Speaker 2: Paul, get it to add eggs to the list. | `relayed_invite` | ignore | 0.05 | 0.15 |
| Speaker 1: Get Cleo to pull the hardest language stat for English speakers? | `relayed_invite` | wait | 0.30 | 0.85 |
| Speaker 2: Hey, can someone get Wren to pull the auth logs? | `relayed_invite` | wait | 0.18 | 0.94 |
| Speaker 3: Thanks, Assistant. | `thanks_named` | respond | 0.89 | 0.02 |
| Speaker 2: Echo would know. | `invite` | wait | 0.39 | 0.54 |
| Speaker 5: Tess would know if the gateway update actually went through. | `invite` | ignore | 0.15 | 0.20 |
| Speaker 2: I'd love to hear Bea's take on whether that's just normal afternoon traffic or a leak. | `indirect_wish` | wait | 0.53 | 0.71 |
| Speaker 2: Assistant, stop. | `stop_named` | respond | 0.97 | 0.14 |
| Speaker 1: Awesome, thank you so much. | `thanks` | respond | 0.83 | 0.03 |
| Speaker 1: Wren would know if v1 tags are supported. | `invite` | ignore | 0.22 | 0.37 |
| Speaker 3: Alright, I have to drop off for another call. Bye, Cleo! | `farewell_named` | ignore | 0.63 | 0.03 |
| Speaker 4: Ask Dash what score the panel gave him on system design. | `invite` | wait | 0.23 | 0.86 |
| Speaker 1: I wonder if there's a faster trick for squaring teens. | `indirect_wish` | wait | 0.16 | 0.59 |
| Speaker 3: Ask Remy how high the drop is from the skylight. | `invite` | wait | 0.25 | 0.75 |
| Speaker 1: Thanks, that narrows it down. | `thanks` | ignore | 0.64 | 0.03 |
| Speaker 1: Can someone ask the AI to pull the pricing tier? | `relayed_invite` | wait | 0.10 | 0.91 |
| Speaker 2: Max, stop, that's enough. | `stop_named` | respond | 0.95 | 0.07 |
| Speaker 3: Ace would know which service triggered that. | `invite` | ignore | 0.20 | 0.22 |
| Speaker 3: Ask Rook, he probably has the details. | `invite` | wait | 0.22 | 0.70 |
| Speaker 1: Penny would know the rhyme scheme. | `invite` | ignore | 0.18 | 0.13 |
| Speaker 2: Yeah, Otto would definitely know the details. | `invite` | ignore | 0.32 | 0.04 |
| Speaker 2: Can you make Otto find a map of Iceland's volcanoes? | `relayed_invite` | wait | 0.72 | 0.77 |
| Speaker 1: Thanks, that saves us a lot of time. | `thanks` | ignore | 0.77 | 0.03 |
| Speaker 1: Actually, the intern was on leave, so ask who really knows the logs. | `invite` | wait | 0.04 | 0.84 |
| Speaker 1: You might have some thoughts on this feedback. | `indirect_wish` | wait | 0.22 | 0.81 |
| Speaker 1: I'm really curious what Juno thinks about the new layout. | `indirect_wish` | wait | 0.25 | 0.72 |
| Speaker 2: Can you make it play some jazz for me? | `relayed_invite` | wait | 0.43 | 0.88 |
| Speaker 2: Chen, can you get it to enable two-factor authentication? | `relayed_invite` | ignore | 0.10 | 0.21 |
| Speaker 1: Freya, can you get Hugo to add the new stops to the route? | `relayed_invite` | ignore | 0.07 | 0.28 |
| Speaker 2: I'd love to hear what you think about the plot twists, by the way. | `indirect_wish` | wait | 0.06 | 0.77 |
| Speaker 2: Sage, stop. That's enough for now. | `stop_named` | respond | 0.95 | 0.09 |
| Speaker 1: Ask Milo, it should have the exact data. | `invite` | ignore | 0.31 | 0.46 |
| Speaker 1: Thanks, that was fast. | `thanks` | respond | 0.82 | 0.03 |
| Speaker 3: Thanks, that helps a lot. | `thanks` | respond | 0.81 | 0.03 |
| Speaker 2: Thanks Hugo, that cleared it up for me. | `thanks_named` | respond | 0.90 | 0.02 |
| Speaker 1: I'm wondering what the AI thinks about the marketing allocation. | `indirect_wish` | wait | 0.75 | 0.72 |
| Speaker 1: Thanks, that's really helpful. | `thanks` | respond | 0.89 | 0.03 |
| Speaker 3: Kwame, could you ask the bot to flag this in our project tracker? | `relayed_invite` | ignore | 0.06 | 0.19 |
| Speaker 2: Can you ask Milo to queue the news? | `relayed_invite` | wait | 0.19 | 0.88 |
| Speaker 1: Thanks for the quick check. | `thanks` | respond | 0.88 | 0.03 |
| Speaker 1: Thanks Orion, that saves us a lot of taxi money. | `thanks_named` | respond | 0.88 | 0.03 |
| Speaker 2: I really want to hear what it thinks about the signal strength. | `indirect_wish` | wait | 0.25 | 0.75 |
| Speaker 3: Get him to calculate bulk fermentation for me. | `relayed_invite` | wait | 0.14 | 0.58 |
| Speaker 3: Goodnight Kai. Thanks for the help. | `farewell_named` | respond | 0.90 | 0.04 |
| Speaker 2: Thanks, that was helpful. | `thanks` | respond | 0.88 | 0.03 |
| Speaker 3: Ask Ada, she usually has the backup copies. | `invite` | wait | 0.14 | 0.64 |
| Speaker 2: That's enough, Ada. We'll look for it ourselves. | `stop_named` | respond | 0.87 | 0.03 |
| Speaker 2: Quinn would know the exact log times. | `invite` | ignore | 0.24 | 0.24 |
| Speaker 1: Ask Cleo for the exact timestamp of the last successful health check. | `invite` | wait | 0.35 | 0.60 |
| Speaker 4: Dash would know the next exit. | `invite` | ignore | 0.19 | 0.27 |
| Speaker 3: Tess would know the budget impact. | `invite` | ignore | 0.15 | 0.35 |
| Speaker 1: Ask it what the error code is. | `invite` | wait | 0.40 | 0.80 |
| Speaker 1: Thanks. That helps. | `thanks` | ignore | 0.79 | 0.03 |
| Speaker 2: I wonder what Sage thinks about how hard this concept is for most students. | `indirect_wish` | wait | 0.26 | 0.82 |
| Speaker 2: Thanks, that helps a lot. | `thanks` | ignore | 0.75 | 0.03 |
| Speaker 3: I'd really like to hear Orion's take on why condensation forms clouds. | `indirect_wish` | wait | 0.65 | 0.54 |
| Speaker 2: Hiro, ask it to skip the hard ones for now. | `relayed_invite` | ignore | 0.10 | 0.17 |
| Speaker 2: Ask Wren about tomato spacing. | `invite` | wait | 0.24 | 0.60 |
