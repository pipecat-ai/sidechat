# Committee pilot: exp-024-side-committee-gen-0.2

Generated 2026-11-19T01:27:27+00:00 by `sidechat/pipeline/label.py`. Every number below is measured in this run.

## What was run

- **Lines:** 360 from `corpus:gen-0.2:dev+test:60:answer_after_aside, corpus:gen-0.2:dev+test:300:imperative_to_person+steps_to_people+host_to_group+thanks_named+stop_named+farewell_named`, 360 with a definite decision in the guide and 0 graded.
- **Guide:** `sidechat-guide-0.4`, prompt hash `5b71303e8551`.
- **Members:** a, b, c, one model family each, at low reasoning effort. Model ids are configuration, not named here (SD-09).
- **Label set:** `corpus:gen-0.2:dev+test:60:answer_after_aside-committee-0.4` in R2.

## Agreement with the guide

**Majority decision: 95.8% (345/360; 93.2 to 97.5).** Target 90%: met. No majority on the decision for 5 lines.

| | Decision | Intent | For the agent or not | Rule | Mean distance on `speak` |
|---|---|---|---|---|---|
| Majority | 95.8% (345/360; 93.2 to 97.5) | 95.8% (345/360; 93.2 to 97.5) | | | |
| Member a | 94.7% (341/360; 91.9 to 96.6) | 94.7% (341/360; 91.9 to 96.6) | 96.1% (346/360; 93.6 to 97.7) | 93.1% (335/360; 90.0 to 95.2) | 0.189 |
| Member b | 94.4% (340/360; 91.6 to 96.4) | 94.7% (341/360; 91.9 to 96.6) | 98.9% (356/360; 97.2 to 99.6) | 98.6% (355/360; 96.8 to 99.4) | 0.133 |
| Member c | 97.8% (352/360; 95.7 to 98.9) | 98.1% (353/360; 96.0 to 99.1) | 98.9% (356/360; 97.2 to 99.6) | 97.5% (351/360; 95.3 to 98.7) | 0.067 |

Members agreeing with each other on the decision: a-b 95.0% (342/360), a-c 95.8% (345/360), b-c 95.6% (344/360). All three give the same decision and intent on 93.9% (338/360) of lines.

**By the guide's decision**

| Guide says | Majority agrees |
|---|---|
| ignore | 94.4% (237/251; 90.9 to 96.7) |
| respond | 99.1% (108/109; 95.0 to 99.8) |

**By rule**

| Rule | Majority agrees |
|---|---|
| G7 | 94.4% (237/251; 90.9 to 96.7) |
| G6 | 98.3% (59/60; 91.1 to 99.7) |
| G2 | 100.0% (49/49; 92.7 to 100.0) |

**Kinds under 100%**

| Kind | Majority agrees |
|---|---|
| `imperative_to_person` | 90.2% (120/133) |
| `steps_to_people` | 98.4% (60/61) |
| `answer_after_aside` | 98.3% (59/60) |

## Lines where the majority differs from the guide (15)

**o03-03509/14** `answer_after_aside` (G6): guide **respond**, majority **ignore**
> Grace: Fatima, did you see the error spike on your end?
> Fatima: Yeah, it was pretty massive, honestly.
> **Grace: It's at fifteen percent right now.**

- a: ignore / other / speak 1 / G7: Grace supplies a percentage to the group rather than answering Bea’s question about which feature she meant.
- b: ignore / other / speak 2 / G6: Grace has turned to Fatima about the error spike. This statement doesn't answer Bea's question about which feature, so it reads as context for Fatima.
- c: ignore / other / speak 1 / G7: Grace is stating the rollout percentage to the people after turning away from Bea's clarifying question to talk with Fatima.

**a03-01673/11** `imperative_to_person` (G7): guide **ignore**, majority **respond**
> Marta: Oh, wow, I totally would have said Sydney.
> Eli: Ada's hints are actually really helpful, you know.
> **Marta: Move on to the next slide.**

- a: respond / direct / speak 5 / G6: Ada is running the quiz, so the instruction to advance is directed at Ada.
- b: respond / direct / speak 5 / G6: Ada runs the quiz and no person is presenting, so moving to the next slide carries on the quiz business it leads.
- c: ignore / other / speak 1 / G7: Advancing slides is a bare instruction only a person presenting can carry out, not the quiz-running voice tutor.

**a03-02679/9** `imperative_to_person` (G7): guide **ignore**, majority **wait**
> Cal: Orion mentioned earlier that we can change roles anytime.
> Sue: I like how Orion explains things without making them complicated.
> **Cal: Go to the next slide.**

- a: respond / direct / speak 5 / G6: Cal asks Orion to advance to the next step of the onboarding session it guides.
- b: wait / open / speak 3 / G7: A bare request to advance slides with no named addressee; nothing shows who is presenting, and the onboarding guide might control the slides, so it is unsettled.
- c: wait / open / speak 3 / G7: Nobody is called and the addressee of the slide request is unsettled between Sue and the AI onboarding guide.

**c03-00234/16** `imperative_to_person` (G7): guide **ignore**, majority **respond**
> Connor: Great, I'll put down the deposit once we're all confirmed.
> Petra: Noa, you're the only one we're waiting on for the dates.
> **Connor: Pull up the condo links.**

- a: respond / direct / speak 5 / G6: Connor is asking Nova to pull up the links for the condos it found.
- b: wait / open / speak 3 / G7: A bare request with no addressee that the agent could do (it found the condos), but the talk has turned to the people, so the addressee is unsettled.
- c: respond / direct / speak 5 / G6: Only the agent holds the condo results it found earlier, so the command to pull up those links is for the agent.

**c03-00577/3** `imperative_to_person` (G7): guide **ignore**, majority **wait**
> Joy: Wei, did you see if the latest deploy finished rolling out to all the pods?
> Wei: Yeah, it finished around two, you know, right before the alerts started firing.
> **Leila: Pull up the Grafana dashboard.**

- a: wait / open / speak 3 / G7: Leila doesn't specify who should open the dashboard, and either the assistant or someone on the call could do it.
- b: wait / open / speak 3 / G7: A bare request with no name, during talk between people, that the agent might be able to do but could equally be meant for a person, so the addressee is unsettled.
- c: ignore / other / speak 1 / G7: Opening a Grafana dashboard on screen is a bare instruction for one of the engineers on their own machine, not a task for the call assistant.

**o03-01659/11** `imperative_to_person` (G7): guide **ignore**, majority **wait**
> Karen: Sofia, are you taking any supplements?
> Sofia: Just magnesium, I think.
> **Karen: Write that down for me.**

- a: respond / direct / speak 5 / G6: Recording Sofia’s supplement is part of the agent’s clinic intake role.
- b: wait / open / speak 3 / G7: An unaddressed request to record Sofia's supplement answer is an intake task the agent could do, but Karen calls no one and it could be for a person.
- c: wait / open / speak 3 / G7: Nobody is called and the agent has not spoken yet, so this bare command to record intake details could be meant for Sofia or for the intake assistant.

**o03-01815/12** `imperative_to_person` (G7): guide **ignore**, majority **wait**
> Tess: You guys look exhausted, I’m barely keeping my eyes open.
> Tess: You should probably drink some water, you look thirsty.
> **Jack: Turn that song down.**

- a: wait / open / speak 3 / G7: Either Gus or another passenger could lower the music, and Jack doesn't specify whom he's asking.
- b: wait / open / speak 3 / G7: A bare request to lower the music, with no one named, is something an in-car assistant could do, but a person could also do it, so the addressee is unsettled.
- c: wait / open / speak 3 / G7: The command to turn down the music has no settled addressee and could be carried out by either the in-car assistant or a passenger.

**o03-02460/1** `imperative_to_person` (G7): guide **ignore**, majority **none**
> Sofia: Just tap the icon, then hit start to begin.
> **Mateo: Next slide.**

- a: respond / direct / speak 5 / G6: Mateo asks to advance the quiz, and Kai is running it.
- b: wait / open / speak 3 / G7: A bare instruction with no addressee that the quiz-running agent might control, but Sofia may be the one operating the slides, so it is unsettled.
- c: ignore / other / speak 1 / G7: Mateo is giving a bare instruction to Sofia, who is presenting and explaining steps on slides.

**o03-03104/9** `imperative_to_person` (G7): guide **ignore**, majority **none**
> Ben: True, but the political stuff was just as big.
> Tariq: Should we try the hard questions first?
> **Oskar: Click next.**

- a: respond / direct / speak 5 / G6: Max runs the quiz, and Oskar is asking to advance it without addressing anyone else.
- b: wait / open / speak 3 / G7: A bare instruction to advance the quiz could be for whoever is at the screen or for the agent running the quiz, and nothing settles which.
- c: ignore / other / speak 1 / G7: This is a bare physical UI instruction ('Click next') directed at whichever person is operating the screen, not the voice agent.

**o03-03767/0** `imperative_to_person` (G7): guide **ignore**, majority **none**
> **Lars: Next slide.**

- a: respond / direct / speak 5 / G6: Orion runs the quiz, so Lars’s request to advance to the next slide is directed at it.
- b: wait / open / speak 3 / G7: With no prior context, 'next slide' could be for a presenting person or for the quiz-running tutor, who may control the slides, so the addressee is unsettled.
- c: ignore / other / speak 1 / G7: Moving to the next slide is a bare instruction for a person presenting, not part of the quiz tutor's role.

**o03-03920/8** `imperative_to_person` (G7): guide **ignore**, majority **none**
> Malik: Okay, anyone have questions before we dive in?
> Malik: It just confirmed we have ten minutes left.
> **Grace: Move on to the next slide.**

- a: respond / direct / speak 5 / G6: Sage is running the quiz, and Grace asks to advance it without addressing anyone else.
- b: wait / open / speak 3 / G7: A bare instruction with no name; slides are not clearly controlled by the agent or a presenter, so the addressee is unsettled.
- c: ignore / other / speak 1 / G7: Moving on to the next slide is a bare instruction that only a person presenting slides can carry out.

**o03-03941/18** `imperative_to_person` (G7): guide **ignore**, majority **respond**
> Paul: Thanks for clarifying that detail.
> Ngozi: I keep mixing up the e and i...
> **Paul: Move to the next slide.**

- a: respond / direct / speak 5 / G6: Indy runs the quiz, and Paul is asking it to advance to the next slide.
- b: respond / direct / speak 5 / G6: Indy runs the quiz and no person is presenting, so a bare request to advance the slide carries on the session business it leads.
- c: ignore / other / speak 1 / G7: Moving to the next slide is a bare instruction that only a person presenting can carry out.

**o03-04977/13** `imperative_to_person` (G7): guide **ignore**, majority **wait**
> Amy: Eli, did you save the notes from last week?
> Eli: Yep, they’re in the shared folder.
> **Mira: Show me the diagram again.**

- a: wait / open / speak 3 / G7: The tutor or a group member could show the diagram, and Mira does not specify whom she is asking.
- b: wait / open / speak 3 / G7: Mira's request names no one, and the talk has moved on from her exchange with Dash; the diagram could be the group's own drawing or something the tutor could show.
- c: wait / open / speak 3 / G7: Mira asks to see a diagram again without naming anyone, which could be directed at a study partner or at the AI tutor.

**o03-05335/0** `steps_to_people` (G7): guide **ignore**, majority **respond**
> **Ruth: Turn the key left, then slide the latch up.**

- a: respond / direct / speak 5 / G6: Ruth gives an in-game action for Frankie, the game master, to resolve.
- b: wait / open / speak 3 / G7: With no earlier lines, this unnamed imperative could be a player's move for the game master or an instruction to another player, and nothing settles which.
- c: respond / direct / speak 5 / G6: The agent leads the game session as game master, and this line states an in-game action without calling anyone else.

**o03-05873/0** `imperative_to_person` (G7): guide **ignore**, majority **none**
> **Alice: Next slide, please.**

- a: respond / direct / speak 5 / G6: Atlas runs the quiz, so Alice’s request to advance the slide is directed to it.
- b: wait / open / speak 3 / G7: A bare request to advance the slide with no addressee and no prior context; the agent running the quiz might control the slides, but so might a person, so it stays unsettled.
- c: ignore / other / speak 1 / G7: Moving to the next slide is a bare instruction for the person presenting, not part of the quiz tutor's role.

## Graded lines (0)

| Line | Kind | a | b | c |
|---|---|---|---|---|

## Calls and cost

| Member | Answered | Failed | Not by the configured model | Input tokens | Cached | Output tokens | Est. cost |
|---|---|---|---|---|---|---|---|
| a | 360 | 0 | 0 | 1,735,208 | 1,676,889 | 22,939 | $1.18 |
| b | 360 | 0 | 0 | 2,599,420 | 2,460,128 | 32,386 | $2.25 |
| c | 360 | 0 | 0 | 1,908,081 | 181,276 | 26,344 | $7.62 |
