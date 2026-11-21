# Committee pilot: exp-065-side-committee-gen-0.5

Generated 2026-11-20T19:10:39+00:00 by `sidechat/pipeline/label.py`. Every number below is measured in this run.

## What was run

- **Lines:** 360 from `corpus:gen-0.5:dev+test:120:people_question_after_agent, corpus:gen-0.5:dev+test:120:partner_to_people_after_agent, corpus:gen-0.5:dev+test:120:follow_up_later`, 360 with a definite decision in the guide and 0 graded.
- **Guide:** `sidechat-guide-0.4`, prompt hash `5b71303e8551`.
- **Members:** a, b, c, one model family each, at low reasoning effort. Model ids are configuration, not named here (SD-09).
- **Label set:** `corpus:gen-0.5:dev+test:120:people_question_after_agent-committee-0.4` in R2.

## Agreement with the guide

**Majority decision: 73.3% (264/360; 68.5 to 77.6).** Target 90%: **not met**. No majority on the decision for 6 lines.

| | Decision | Intent | For the agent or not | Rule | Mean distance on `speak` |
|---|---|---|---|---|---|
| Majority | 73.3% (264/360; 68.5 to 77.6) | 90.8% (218/240; 86.5 to 93.9) | | | |
| Member a | 60.8% (219/360; 55.7 to 65.7) | 79.2% (190/240; 73.6 to 83.8) | 81.2% (195/240; 75.8 to 85.7) | 78.6% (283/360; 74.1 to 82.5) | 1.033 |
| Member b | 75.0% (270/360; 70.3 to 79.2) | 91.2% (219/240; 87.0 to 94.2) | 92.9% (223/240; 88.9 to 95.5) | 83.9% (302/360; 79.7 to 87.3) | 0.583 |
| Member c | 85.6% (308/360; 81.5 to 88.8) | 94.6% (227/240; 91.0 to 96.8) | 95.8% (230/240; 92.5 to 97.7) | 68.1% (245/360; 63.1 to 72.7) | 0.344 |

Members agreeing with each other on the decision: a-b 82.2% (296/360), a-c 73.1% (263/360), b-c 83.6% (301/360). All three give the same decision and intent on 69.4% (250/360) of lines.

**By the guide's decision**

| Guide says | Majority agrees |
|---|---|
| ignore | 90.4% (217/240; 86.0 to 93.5) |
| wait | 39.2% (47/120; 30.9 to 48.1) |

**By rule**

| Rule | Majority agrees |
|---|---|
| G6 | 63.3% (152/240; 57.1 to 69.2) |
| G7 | 93.3% (112/120; 87.4 to 96.6) |

**Kinds under 100%**

| Kind | Majority agrees |
|---|---|
| `follow_up_later` | 39.2% (47/120) |
| `partner_to_people_after_agent` | 87.5% (105/120) |
| `people_question_after_agent` | 93.3% (112/120) |

## Lines where the majority differs from the guide (96)

**o07-00666/19** `people_question_after_agent` (G7): guide **ignore**, majority **none**
> Noor: Can you check the lighting level down here?
> agent: It's dim, but the torch still works.
> **Noor: So are we still going deeper, then?**

- a: respond / direct / speak 5 / G6: Noor follows up on her ongoing exchange with Frankie about the descent.
- b: wait / open / speak 3 / G6: Noor's 'we' question could be a party-planning question for Joy and Femi or a prompt to the game master, and nothing settles which.
- c: ignore / other / speak 1 / G7: Noor turns to the other players to ask about the party's plans rather than addressing the game master.

**o07-00790/2** `people_question_after_agent` (G7): guide **ignore**, majority **none**
> Chris: Remy, can you pull up the latest stats on Duolingo retention rates?
> agent: Sure. About 40% of users drop off after the first month.
> **Chris: Given that, are we still pushing the gamification angle for the episode?**

- a: respond / direct / speak 5 / G6: Chris follows up on Remy’s answer by asking what the statistic means for the episode’s angle.
- b: ignore / other / speak 1 / G7: Chris turns from the agent's answer to ask the people about their own editorial plan for the episode, a decision for the hosts.
- c: wait / other / speak 3 / G6: Chris uses 'we' right after Remy's answer, which could be turning to the human co-host Rémi about their episode plan or including the AI co-host Remy.

**o07-00935/4** `people_question_after_agent` (G7): guide **ignore**, majority **respond**
> Freya: Assistant, which counter-argument is strongest for the intro?
> agent: The 2019 stability study. It contradicts the main thesis directly.
> **Freya: So do we use that one instead of the old one?**

- a: respond / direct / speak 5 / G6: Freya is following up on Dash’s recommendation in her own exchange with it.
- b: respond / direct / speak 5 / G6: Freya continues her own exchange with Dash, following up on the answer it just gave her without turning to anyone else.
- c: wait / direct / speak 3 / G6: Freya was just speaking to the agent, so 'do we use that one' could be asking the AI tutor for advice or turning to the study group to make a joint decision.

**o07-01021/5** `people_question_after_agent` (G7): guide **ignore**, majority **respond**
> Greg: Fine, I'll go in. Maybe I can find another.
> agent: Check the cargo bay. Usually full of spare tools.
> **Greg: So we're skipping the main deck? No way back?**

- a: respond / direct / speak 5 / G6: Greg follows up on Indy's cargo bay suggestion by asking the game master about his options.
- b: respond / direct / speak 5 / G6: The agent runs the game and just answered Greg, who follows up about the game world without addressing anyone else.
- c: respond / direct / speak 5 / G6: Greg continues his exchange with the game master agent by asking a clarifying question about the adventure environment.

**o07-01352/2** `people_question_after_agent` (G7): guide **ignore**, majority **respond**
> Alice: Atlas, is the next one addition?
> agent: No. It's subtraction. Forty-two minus seventeen.
> **Wei: So are we still doing the hard ones?**

- a: respond / direct / speak 5 / G6: Wei asks about the difficulty of the quiz Atlas is running.
- b: respond / direct / speak 5 / G6: The agent runs the quiz and Wei's question about the difficulty of the questions carries on that quiz business without calling anyone else.
- c: wait / direct / speak 3 / G6: Someone other than the agent's last partner questions the quiz difficulty, which could be directed at either the quiz-running agent or Alice.

**o07-01368/4** `people_question_after_agent` (G7): guide **ignore**, majority **respond**
> Petra: Yeah, mostly, but she missed Tuesday morning's dose, I think.
> agent: Noted. That usually isn't a big deal if she caught up later. How is her BP at home?
> **Petra: So are we still on track for the regular slot, or should we push it back?**

- a: respond / direct / speak 5 / G6: Petra continues her intake exchange with Tess by asking whether to keep or delay the appointment.
- b: respond / direct / speak 5 / G6: Petra is mid-exchange with Tess, which runs the clinic intake, and her scheduling question carries on that business without turning to anyone else.
- c: respond / direct / speak 5 / G6: Petra continues her ongoing intake exchange with the agent, which leads the session.

**o07-01568/16** `people_question_after_agent` (G7): guide **ignore**, majority **none**
> Hana: Is there anything else I should prepare before they arrive?
> agent: Just have your current pill bottles handy in case they ask for visual confirmation.
> **Hana: So are we still going with the morning schedule change?**

- a: respond / direct / speak 5 / G6: Hana continues her own intake exchange with Ember without turning to anyone else.
- b: wait / open / speak 3 / G6: Hana has been talking with the intake agent, which leads the session, but a question about whether 'we' are still going with a schedule change could equally be for Leo, so nothing settles it.
- c: ignore / other / speak 1 / G6: Hana turns from the intake assistant to ask Leo about their own shared schedule plans ('are we still going with...').

**o07-02244/8** `people_question_after_agent` (G7): guide **ignore**, majority **none**
> Lars: Does anyone know the current headcount for the ops team?
> agent: It's currently forty-two full-time employees.
> **Lars: So are we still hiring for those open spots?**

- a: respond / direct / speak 5 / G6: Lars follows up on Iris's answer to his headcount question without turning to anyone else.
- b: wait / open / speak 3 / G6: Lars follows up his exchange with Iris, but whether the team is still hiring is the people's own decision, so it could be for the agent or the room.
- c: ignore / other / speak 1 / G7: Lars uses 'we' to ask the group about their own hiring plans and decisions, which is a question for the people rather than the agent.

**a07-00168/3** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Ivan: The airlock door.
> agent: Its control panel is blinking red. The display says the outer hatch is open.
> **Ivan: Okay, let's seal the outer hatch before we go any farther.**

- a: respond / direct / speak 5 / G6: Ivan declares his next in-game action in the ongoing exchange with Echo, the game master.
- b: respond / direct / speak 5 / G6: The agent runs the game and Ivan continues his exchange with it by declaring an in-game action.
- c: respond / direct / speak 5 / G6: Ivan continues his exchange with the game master by stating the next in-game action.

**a07-01378/2** `partner_to_people_after_agent` (G6): guide **ignore**, majority **none**
> Leo: Can Clover check the best airport for the wedding in Siena?
> agent: Florence Airport is about 90 minutes from Siena by car.
> **Leo: Let's use Florence and arrange a shared transfer.**

- a: respond / direct / speak 5 / G6: Leo continues his exchange with Clover by accepting its airport recommendation and asking to arrange a shared transfer.
- b: wait / indirect / speak 3 / G6: Leo follows up on the agent's answer, but 'let's' reads as a proposal to the group, while arranging a transfer is a task the travel agent could do, so the addressee is unsettled.
- c: ignore / other / speak 1 / G6: Leo turns to the group to propose a plan based on the agent's answer rather than continuing the exchange with Clover.

**a07-01407/14** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Femi: The dial reads 0.4 bar. What should I do?
> agent: The system needs topping up. I can arrange an engineer if you're not comfortable using the filling loop.
> **Femi: Let's get an engineer rather than risk doing it ourselves.**

- a: respond / direct / speak 5 / G6: Femi accepts Dash’s offer to arrange an engineer, continuing their support exchange.
- b: respond / direct / speak 5 / G6: Femi answers the agent's offer to arrange an engineer, continuing his exchange with the support agent who leads the call.
- c: wait / direct / speak 3 / G6: Femi say 'let's' which could be proposing the choice to Olga before telling the agent, or directly accepting the support agent's offer to arrange an engineer.

**a07-01668/17** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Anna: Will the technician bring a replacement pump?
> agent: Yes, the technician will bring a compatible pump.
> **Anna: Let's take the Tuesday slot, then.**

- a: respond / direct / speak 5 / G6: Anna continues her exchange with Otto by accepting the appointment slot it offered.
- b: respond / direct / speak 5 / G6: Anna continues her own exchange with the support agent, accepting the appointment it offered, which only the agent can book.
- c: respond / direct / speak 5 / G6: Anna continues her exchange with the support agent to book the appointment slot it offered.

**a07-01745/9** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Dana: Listening.
> agent: You hear slow footsteps and a chain dragging across stone.
> **Dana: Let's hold here and prepare for something to come through.**

- a: respond / direct / speak 5 / G6: Dana follows up on the game master's narration by declaring the party's next action.
- b: respond / direct / speak 5 / G6: The agent is the game master and Dana's line declares the party's action in the ongoing scene, carrying on the session business.
- c: ignore / other / speak 1 / G7: Dana is proposing a plan to the other players rather than stating an action to the game master.

**b07-00036/20** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Raf: Okay, and can you email us something confirming the credit?
> agent: Done. A confirmation just went to the account email with reference CR-20417.
> **Raf: Alright, so we just pay the eighty-nine fifty and ignore the rest.**

- a: respond / direct / speak 5 / G6: Raf continues his exchange with Juno by stating what he thinks he still owes, implicitly asking her to confirm.
- b: respond / direct / speak 4 / G6: Raf is continuing his own exchange with the agent, seeking confirmation of what to do next without turning to Kate, and the agent can usefully clarify since the $89.50 already posted.
- c: respond / direct / speak 5 / G6: Raf continues his support exchange with Juno to confirm what they need to pay.

**c07-00059/19** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Hiro: Let's clear it today—Bea, what's the exact total after the late fee waiver?
> agent: With the forty-five dollar fee waived, your current balance is one hundred twenty-eight dollars and fifty cents.
> **Hiro: One twenty-eight fifty is much better, let's pay that now.**

- a: respond / direct / speak 5 / G6: Hiro follows up on Bea’s balance quote by asking to pay that amount now.
- b: respond / direct / speak 4 / G6: Hiro is continuing his own exchange with Bea, who runs the support call, and is asking to pay the balance she just quoted, which she can process.
- c: respond / direct / speak 5 / G6: Hiro continues his exchange with the support agent by instructing it to process the payment for the balance it just quoted.

**c07-00401/16** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Anna: Can we tell if the staircase is dry and clear of traps?
> agent: The stone steps are dry, though covered in thick vines. You don't spot any obvious tripwires from here.
> **Anna: Let's take the stairs instead of wading through unknown water.**

- a: respond / direct / speak 5 / G6: Anna follows up on Penny’s description by choosing the party’s next move for the game master to resolve.
- b: respond / direct / speak 5 / G6: The agent leads the game and Anna's line declares the party's action in the adventure, carrying on that business.
- c: ignore / other / speak 1 / G7: Anna is proposing a course of action to the other players in the party rather than stating a final action to the game master.

**c07-00427/12** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Lucia: Um, can we also add that he's been taking ibuprofen since Tuesday?
> agent: Yes, I've noted that he's been taking ibuprofen since Tuesday.
> **Lucia: Okay, cool, so we should probably, like, write down the exact dosage before she gets on.**

- a: respond / direct / speak 5 / G6: Lucia continues her intake exchange with the assistant by asking to record the exact dosage.
- b: respond / direct / speak 4 / G6: Lucia continues her exchange with the intake assistant about the notes, so the agent, which leads the intake, should follow up and ask for the dosage.
- c: ignore / other / speak 1 / G6: Lucia turns to Pablo to suggest what the two of them should prepare before the doctor joins.

**o07-00434/7** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Chris: It's eleven. Can you give me a hint if I'm wrong?
> agent: You are correct. It is number eleven.
> **Chris: Alright, let's move on to the next one then.**

- a: respond / direct / speak 5 / G6: Chris is continuing the exchange with Juno and asking it to advance the quiz it runs.
- b: respond / direct / speak 5 / G6: Chris continues his quiz exchange with Juno, which runs the quiz, asking it to move to the next question.
- c: respond / direct / speak 5 / G6: Chris continues his quiz exchange with Juno, who runs the quiz and just confirmed his answer, asking to proceed to the next question.

**o07-00850/15** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Dev: Frankie, skip to Europe now.
> agent: Understood. Capital of Germany?
> **Dev: Berlin. We'll finish this set soon.**

- a: respond / direct / speak 5 / G6: Dev answers the quiz question Frankie just asked.
- b: respond / direct / speak 5 / G6: Dev answers the quiz question the agent just asked, and the agent leads the session.
- c: respond / direct / speak 5 / G6: Dev answers the quiz question just asked by Frankie, who is leading the quiz.

**o07-01195/5** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Anna: Group one, I think? Like, the alkali metals. Can you give me another one?
> agent: Yes, Group one. Another example is sodium, which is also in Group one.
> **Anna: Wait, so they’re both super reactive? We should double-check that later.**

- a: respond / direct / speak 5 / G6: Anna follows up on the tutor’s answer by asking whether both elements are highly reactive.
- b: respond / direct / speak 4 / G6: Anna continues her own exchange with the tutor running the quiz by asking a follow-up about its answer, though her remark about checking later softens it slightly.
- c: ignore / other / speak 1 / G6: Anna shifts from her exchange with the agent to address the group ('We should double-check that later'), rather than asking the agent to answer.

**o07-01545/10** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Omar: Dim and dusty.
> agent: A single chandelier hangs. You see a trapdoor.
> **Omar: Let's open it together.**

- a: respond / direct / speak 5 / G6: Omar declares an in-game action in response to the game master's description of the trapdoor.
- b: respond / direct / speak 5 / G6: The agent leads the game and Omar's line carries on the adventure as an action responding to the agent's description of the trapdoor.
- c: ignore / other / speak 1 / G7: Omar is making a proposal to the other players to coordinate opening the trapdoor together, rather than declaring an action to the game master.

**o07-02618/3** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Fatima: Cracked. Sealing it now.
> agent: The seal holds. Pressure stabilizes in ten seconds.
> **Fatima: Good. We move to the bridge.**

- a: respond / direct / speak 5 / G6: Fatima declares the party’s next action to Max, the game master.
- b: respond / direct / speak 5 / G6: The agent leads the game and Fatima continues the adventure with a player action, calling no one else.
- c: respond / direct / speak 5 / G6: Max is the game master leading the adventure, and Fatima is continuing her exchange with the agent by declaring the party's next in-game action.

**o07-02774/6** `partner_to_people_after_agent` (G6): guide **ignore**, majority **respond**
> Chris: Is that why it's in group one even though it's a gas?
> agent: Yes, because of its single valence electron.
> **Chris: We should focus on the alkali metals next then.**

- a: respond / direct / speak 5 / G6: Chris follows up on Kai’s answer by suggesting the next topic for the quiz Kai is leading.
- b: ignore / other / speak 2 / G6: Chris proposes a study focus to the group without asking the quiz-leading agent anything, though it touches the session's direction.
- c: respond / direct / speak 5 / G6: Chris continues his own exchange with the agent and directs the quiz session that the agent leads.

**a07-00026/11** `follow_up_later` (G6): guide **wait**, majority **respond**
> Chloe: I don't think so, but we can keep track ourselves.
> Mira: Do you usually write down tricky words to remember them?
> **Chloe: Is there a good way to remember which letter comes first?**

- a: respond / direct / speak 5 / G6: Chloe is asking for a spelling tip during the quiz Rook is running.
- b: respond / direct / speak 5 / G6: The agent leads the quiz as its tutor, and this question carries on the spelling business without calling anyone else.
- c: wait / open / speak 3 / G7: Chloe asks an open question about a spelling mnemonic that either Mira or the AI tutor could answer.

**a07-00092/10** `follow_up_later` (G6): guide **wait**, majority **respond**
> Rosa: Agreed, I'll stay on the incident through the handover.
> Rosa: You can take over once I've walked everyone through the timeline.
> **Theo: How long have errors been dropping since the rollback?**

- a: respond / direct / speak 5 / G6: Theo follows up on Frankie's update about the rollback and the drop in checkout errors.
- b: respond / direct / speak 5 / G6: Theo is the agent's recent exchange partner and follows up on the agent's rollback update without turning to anyone else.
- c: wait / open / speak 3 / G6: After turning to the group and hearing from Rosa, the incident lead, Theo's unaddressed question about the rollback could be meant for either Rosa or Frankie.

**a07-00210/13** `follow_up_later` (G6): guide **wait**, majority **respond**
> Tariq: The actual alkali metals get more reactive as you go down the group.
> Freya: Yeah, potassium's more reactive than sodium, if I remember right.
> **Freya: Why does hydrogen get put above the alkali metals anyway?**

- a: respond / direct / speak 5 / G6: Freya asks a follow-up about hydrogen that continues the quiz led by the Assistant.
- b: respond / direct / speak 5 / G6: The agent runs the quiz and Freya, its recent partner on hydrogen, asks a subject question that carries on that tutoring business without calling anyone else.
- c: wait / open / speak 3 / G7: After several turns between the people, Freya asks an open question to the room that the tutor agent could answer if nobody else takes it.

**a07-00220/7** `follow_up_later` (G6): guide **wait**, majority **respond**
> Olu: Should we ask Quinn later for some invoice-chasing tips?
> Rhys: First, let's hear about your most spectacular late payment.
> **Rhys: Actually, how long have we been recording?**

- a: respond / direct / speak 5 / G6: Rhys follows up on Quinn’s confirmation that the podcast is recording.
- b: respond / direct / speak 5 / G6: Rhys follows up his own earlier exchange with Quinn about the recording, which only the agent controls and can answer.
- c: wait / open / speak 3 / G7: The agent is no longer in play after the conversation moved on, and this is an open question to the room that Quinn could answer.

**a07-00283/9** `follow_up_later` (G6): guide **wait**, majority **respond**
> Divya: Sage showed us that diagram earlier.
> Elif: OK car, turn on the cabin lights.
> **Elif: Does the Calvin cycle need light directly?**

- a: respond / direct / speak 5 / G6: Elif resumes her exchange with Sage about the Calvin cycle after a brief aside to the car.
- b: respond / direct / speak 5 / G6: Elif continues her own exchange with Sage, following up on its answer about the Calvin cycle after a brief device command.
- c: wait / open / speak 3 / G7: Elif asks an open biology question to the study group after turning to another device, which the AI tutor could answer if nobody else does.

**a07-00307/18** `follow_up_later` (G6): guide **wait**, majority **respond**
> Rhys: Can you get Dash to find out how many strawberries we'll need?
> Anna: Should we ask Dash after we finish the batter?
> **Rhys: Would a few wet crumbs be okay on the toothpick?**

- a: respond / direct / speak 5 / G6: Rhys follows up on Dash’s earlier advice to him about checking the cake with a toothpick.
- b: respond / direct / speak 5 / G6: Rhys follows up on the agent's own toothpick answer to him, continuing his exchange with Dash without turning to anyone else.
- c: wait / open / speak 3 / G7: After talking with Anna for a few turns, Rhys asks an open baking question without calling anyone, which either the people present or the agent could answer.

**a07-00617/14** `follow_up_later` (G6): guide **wait**, majority **respond**
> Wes: They’re in the hall cupboard, plotting their escape.
> Ottie: Are either of you home tomorrow afternoon?
> **Wes: Will we get a call before the delivery?**

- a: respond / direct / speak 5 / G6: Wes returns to his delivery inquiry with a follow-up about the provider’s notification process.
- b: wait / open / speak 3 / G6: Wes asks about the delivery the agent has been handling, but the talk has moved to the people's own plans, so it could be for the agent or for the room and nothing settles it.
- c: respond / direct / speak 5 / G6: Otto is the AI support agent running the call, and Wes asks a question about the provider's delivery process that carries on the support business and that only the agent can answer.

**a07-00617/19** `follow_up_later` (G6): guide **wait**, majority **respond**
> Joy: And could you clear those shoes out of the hallway?
> Joy: Unless you want the sofa to trip over them.
> **Wes: Can we change that delivery window if we need to?**

- a: respond / direct / speak 5 / G6: Wes is following up on Otto’s answer to his delivery question, and the intervening aside was directed at Ottie.
- b: respond / direct / speak 5 / G6: Wes continues his own exchange with the support agent about the delivery, which the agent as provider support can handle.
- c: respond / direct / speak 5 / G6: Otto is the support agent for the provider, and Wes is asking a support question about the delivery following up on Otto's previous answer.

**a07-00649/16** `follow_up_later` (G6): guide **wait**, majority **respond**
> Marta: Can we add seats midyear?
> Jill: We'd probably need two more by October.
> **Jill: Is the annual price locked in at renewal?**

- a: respond / direct / speak 5 / G6: Jill is following up on her pricing exchange with Hugo by asking about the vendor’s renewal terms.
- b: respond / direct / speak 5 / G6: Jill has been in an exchange with Hugo about pricing, and this follow-up asks a pricing question only the vendor's assistant holds the information for, without turning to anyone else.
- c: respond / direct / speak 5 / G6: Jill continues her pricing exchange with Hugo, asking another question that only the vendor's assistant can answer.

**a07-00779/16** `follow_up_later` (G6): guide **wait**, majority **respond**
> Malik: Okay, let's write down five and move on to the next question.
> Wei: Yeah, I've got the next one open.
> **Malik: Wait, if we added ten, would the median change?**

- a: respond / direct / speak 5 / G6: Malik follows up on Max’s median calculation by asking how adding ten would affect it.
- b: respond / direct / speak 5 / G6: Malik, the agent's last partner, follows up on its median answer without turning to anyone else, and the agent is the group's tutor.
- c: wait / open / speak 3 / G7: After turning back to the group to move on, Malik asks an open math question to the room that the AI tutor could answer if nobody else does.

**a07-00784/14** `follow_up_later` (G6): guide **wait**, majority **respond**
> Can: I like that it suggested spinach too, you know, not just lettuce.
> Femi: Should we ask Pip later about herbs for the windowsill?
> **Femi: Um, would mulch help keep those pots from drying out so fast?**

- a: respond / direct / speak 5 / G6: Femi follows up on Pip’s watering advice for the same pots.
- b: respond / direct / speak 5 / G6: Femi continues her own watering exchange with Pip with a follow-up question, turning to no one else.
- c: wait / open / speak 3 / G7: After talking with Can about Pip in the third person, Femi asks an open factual question to the room that the agent could answer.

**a07-00940/14** `follow_up_later` (G6): guide **wait**, majority **respond**
> Dev: Wait, isn't there a higher rate for seats added midyear?
> Paul: I thought so too, but maybe that was the old pricing.
> **Paul: Are those added seats billed immediately or at renewal?**

- a: respond / direct / speak 5 / G6: Paul follows up on Penny’s answer to his own question about adding seats midyear.
- b: respond / direct / speak 5 / G6: Paul asked the seat question the agent answered, and this is his follow-up on that answer, which only the vendor's assistant can settle.
- c: wait / open / speak 3 / G7: Paul asks an open question to the room about billing after a brief exchange with Dev, which the vendor's assistant could answer.

**a07-00948/22** `follow_up_later` (G6): guide **wait**, majority **respond**
> Kate: Is it recording everything we're saying?
> Mac: I'm not sure, actually.
> **Kate: Does the swelling note say which knee it is?**

- a: respond / direct / speak 5 / G6: Kate is following up on the intake note Max added for her.
- b: respond / direct / speak 5 / G6: Kate is asking about the intake note the agent just made, which only the agent holds and which belongs to the intake session it leads.
- c: respond / direct / speak 5 / G6: Only the intake assistant holds and controls the intake notes it just created, and the agent leads the intake session.

**a07-01070/16** `follow_up_later` (G6): guide **wait**, majority **respond**
> Imran: We'll need an aider on our side to test the retry logic.
> Divya: Ada, can you pull up the integration guide? Actually, never mind.
> **Mei: Does the Retry-After value come back in seconds?**

- a: respond / direct / speak 5 / G6: Mei follows up on Ada’s answer to her own question about rate-limit errors.
- b: respond / direct / speak 5 / G6: Mei follows up on her own exchange with Ada about the Retry-After header without turning to anyone else.
- c: wait / open / speak 3 / G7: Mei already turned back to the group after Ada's earlier answer, so this unaddressed technical question is open to the room and Ada should wait in case someone else answers.

**a07-01133/8** `follow_up_later` (G6): guide **wait**, majority **respond**
> Jess: I'll bring marmalade sandwiches and my finest hard stare.
> Marta: I think tess's pick might actually make me cry
> **Siobhan: Where can we stream it?**

- a: respond / direct / speak 5 / G6: Siobhan follows up on her own exchange with Tess by asking where to stream the film Tess recommended.
- b: respond / direct / speak 5 / G6: Siobhan, who asked Tess for the film, follows up on its answer with a lookup only the agent is positioned to answer, without turning to anyone else.
- c: wait / open / speak 3 / G7: After Siobhan turned back to the group for several lines, her unaddressed question is an open lookup for the room rather than a direct continuation with Tess.

**a07-01217/12** `follow_up_later` (G6): guide **wait**, majority **respond**
> Eko: Yeah, we could address that in the third body paragraph.
> Mei: Mira, did Echo suggest any sources for the cost argument?
> **Eko: For those five paragraphs, roughly how many words should the introduction get?**

- a: respond / direct / speak 5 / G6: Eko follows up on Echo’s five-paragraph recommendation from their earlier exchange.
- b: respond / direct / speak 5 / G6: Eko continues their own exchange with Echo, following up on its five-paragraph answer with a question the tutor can answer.
- c: wait / open / speak 3 / G7: After the people returned to talking among themselves, Eko asks an open question to no one in particular that the AI tutor could answer.

**a07-01547/11** `follow_up_later` (G6): guide **wait**, majority **respond**
> Paul: The garden shop on Cedar has a pretty good selection.
> Mira: Maybe I could squeeze one in by the door, although...
> **Mira: Would that 12-inch pot be deep enough for mint roots?**

- a: respond / direct / speak 5 / G6: Mira returns to her own exchange with Remy by asking about the 12-inch pot it recommended.
- b: respond / direct / speak 5 / G6: Mira follows up on the 12-inch pot answer Remy gave her, continuing her own exchange with the agent.
- c: wait / open / speak 3 / G7: After talking with Paul, Mira poses an unaddressed factual question about the 12-inch pot that either Remy or Paul could answer.

**a07-01770/13** `follow_up_later` (G6): guide **wait**, majority **respond**
> Lucia: Let's check the filesystem with df first, then narrow it down from the mount point.
> Jill: Yeah, that sounds safer. I'll run df now.
> **Lucia: Um, does that du command count deleted files that are still open?**

- a: respond / direct / speak 5 / G6: Lucia follows up on her own exchange with Wren about the du command.
- b: respond / direct / speak 5 / G6: Lucia is continuing her own exchange with Wren, which just answered her question about the du command, and this follow-up turns to no one else.
- c: wait / open / speak 3 / G6: Lucia asks a follow-up question about the du command suggested by Wren, after turning to Jill in the last two turns, making it unclear whether she is asking the agent or the room.

**a07-01887/17** `follow_up_later` (G6): guide **wait**, majority **none**
> Anna: Good, let's stick with that timeline.
> Petra: It also recorded penicillin as a medication allergy.
> **Anna: Should I mention that I stopped taking it?**

- a: respond / direct / speak 5 / G6: Anna is asking what to report as part of the clinic intake Sage is leading.
- b: wait / open / speak 3 / G6: Anna has been talking with Petra about what the agent recorded, so 'should I mention it' may be asking Petra's advice, but the intake agent could also answer it; nothing settles which.
- c: ignore / other / speak 1 / G7: Anna is continuing her side conversation with Petra to ask whether she should tell the intake assistant (or doctor) another detail.

**b07-00026/14** `follow_up_later` (G6): guide **wait**, majority **respond**
> Jamal: Agreed. We'll flag it before she joins.
> Jess: Jamal, can Tess actually pull results from the outside lab, or just the clinic's?
> **Jamal: Does the A1C show whether it went down since December?**

- a: respond / direct / speak 5 / G6: Jamal follows up on his own exchange with Tess by asking what the A1C results in his chart show.
- b: respond / direct / speak 4 / G6: Jamal follows up on his own exchange with Tess about the chart results, and only the agent holds the A1C history, though the intervening talk with Jess leaves slight doubt.
- c: respond / direct / speak 5 / G6: Only the intake assistant has access to the patient's chart to check the A1C results it mentioned earlier.

**b07-00057/12** `follow_up_later` (G6): guide **wait**, majority **respond**
> Ottie: Jill, are you writing these down or just spelling out loud?
> Jill: Writing. I'll check them against the list after.
> **Ottie: So is "accommodation" spelled the same way, double c, double m?**

- a: respond / direct / speak 5 / G6: Ottie returns to the quiz with a spelling question for Otto, the tutor running it.
- b: respond / direct / speak 5 / G6: The agent runs the spelling quiz and this spelling question carries on that business without calling anyone else, much like Ottie's earlier spelling question that the agent answered.
- c: wait / open / speak 3 / G7: Ottie asks an open spelling question to the room without addressing anyone after talking with the other participants.

**b07-00060/9** `follow_up_later` (G6): guide **wait**, majority **respond**
> Can: Twenty minutes is generous, I watched you, it was more like eight.
> Ren: Honestly, our co-host knows more grades than my entire gym combined. Slightly threatening.
> **Can: So is Silence harder than Burden of Dreams, or can you even compare them?**

- a: respond / direct / speak 5 / G6: Can returns to his exchange with Wren by asking it to compare the two climbs it described.
- b: respond / direct / speak 5 / G6: Can has been the agent's exchange partner, and this follows up on the agent's own answers about Silence and Burden of Dreams without turning to anyone else, despite the brief banter in between.
- c: wait / open / speak 3 / G7: After a few turns of banter among the human hosts, Can asks an open question about climbing grades that nobody is specifically called to answer, though the AI co-host could take it.

**b07-00082/11** `follow_up_later` (G6): guide **wait**, majority **respond**
> Abena: Omar, check with him today and get it confirmed in writing.
> Omar: Will do, I'll catch him at lunch.
> **Abena: How many of those powered spots are actually spoken for already?**

- a: respond / direct / speak 5 / G6: Abena returns to her exchange with Quinn about the floor map by asking about the powered spots Quinn just mapped.
- b: respond / direct / speak 4 / G6: Abena returns to the floor map Quinn drafted for her; the agent holds the assignment of powered spots, so it is the likely one to answer.
- c: wait / open / speak 3 / G7: After an exchange with Omar, Abena asks an open question to the room about the powered spots that either Quinn or another teacher might know.

**b07-00085/9** `follow_up_later` (G6): guide **wait**, majority **respond**
> Ravi: Hana, are you okay being on call for the first half?
> Hana: Yeah, I can take eight to midnight, then hand off.
> **Ben: Was that two hours for orders with the indexes already built, or before?**

- a: respond / direct / speak 5 / G6: Ben follows up on the two-hour estimate Rook gave in response to his earlier question.
- b: respond / direct / speak 5 / G6: Ben follows up on the agent's answer to his own earlier question about the dry run, and only the agent holds that detail.
- c: wait / open / speak 3 / G6: Ben follows up on Rook's earlier statement about the two-hour orders copy, but after several human turns it could be aimed at Rook or the rest of the team.

**b07-00102/13** `follow_up_later` (G6): guide **wait**, majority **respond**
> Sam: Do you need to tell the council you've moved for council tax?
> Ines: Yeah, I think you have to, otherwise they bill you for both places.
> **Sam: Does that four hours include the time they spend stuck in traffic though?**

- a: respond / direct / speak 5 / G6: Sam’s reference to ‘that four hours’ resumes his own exchange with Echo about van hire.
- b: respond / direct / speak 5 / G6: Sam follows up on the agent's own answer to Sam about the four-hour van hire, continuing his exchange with Echo.
- c: wait / open / speak 3 / G6: Sam follows up on the four hours from Echo's earlier answer, but since Sam just had an exchange with Ines in between, it could be directed at Echo or the group.

**b07-00117/16** `follow_up_later` (G6): guide **wait**, majority **ignore**
> Ruth: Yeah, I mean, someone should, the old one still says Wednesday.
> Rémi: Remy, could you pull up last quarter's... actually, never mind, I've got it here.
> **Ruth: Wait, with questions at the end, like, does that push us past half an hour or are we still okay?**

- a: wait / open / speak 3 / G7: Ruth asks the room for a timing estimate without directing the question to Remy or anyone else.
- b: ignore / other / speak 1 / G7: Ruth is asking the people about their own meeting timing plan, which only they can judge; nobody called the agent and it is not in the exchange.
- c: ignore / other / speak 1 / G7: Ruth is asking the group about their own meeting timing and agenda plans without addressing the agent.

**b07-00135/8** `follow_up_later` (G6): guide **wait**, majority **respond**
> Aoife: Are the three blockers all on the payments side, or is any of that frontend?
> Wes: Two are payments, one's the checkout banner. That one's small.
> **Wes: So of those seven, how many actually have someone assigned?**

- a: respond / direct / speak 5 / G6: Wes returns to his exchange with Ada by asking about the seven tickets she counted.
- b: respond / direct / speak 5 / G6: Wes continues his own exchange with Ada about the seven open tickets she reported, asking for board information only the agent holds.
- c: wait / open / speak 3 / G6: Wes asks a follow-up question about the seven tickets Ada mentioned earlier after briefly talking with Aoife, leaving it open whether Ada or another team member should answer.

**b07-00172/14** `follow_up_later` (G6): guide **wait**, majority **respond**
> Dana: So do we risk it or back out?
> Finn: Risk it. Gold floor, come on.
> **Femi: Darts poisoned, though?**

- a: respond / direct / speak 5 / G6: Femi follows up with the game master about the darts it just described.
- b: respond / direct / speak 5 / G6: The agent leads the game and the question about the darts carries on game business only the game master can answer.
- c: respond / direct / speak 5 / G6: The agent leads the game session as game master, and Femi is asking a question about the trap it just described.

**b07-00195/10** `follow_up_later` (G6): guide **wait**, majority **respond**
> Tariq: Okay. Big van, early start. I'll come at eight.
> Leo: Aisha, get it to make a packing checklist for me?
> **Tariq: Does that van need a special licence though?**

- a: respond / direct / speak 5 / G6: Tariq follows up on Nova’s van recommendation in his own exchange with it.
- b: respond / direct / speak 5 / G6: Tariq made the van request and Nova answered him, so his question about the van's licence is a follow-up to his own exchange with the agent.
- c: wait / open / speak 3 / G7: Tariq asks an open factual question to the room about the 7.5-tonne van after the conversation had moved back to the people, which the agent could answer if nobody else does.

**b07-00233/17** `follow_up_later` (G6): guide **wait**, majority **respond**
> Jess: So short one this month, big one in summer?
> Fatima: Works for me. Summer's slower anyway.
> **Fatima: Four copies... any ebook holds on it?**

- a: respond / direct / speak 5 / G6: Fatima picks up her earlier exchange with Tess by asking a follow-up about the book’s library availability.
- b: respond / direct / speak 5 / G6: Fatima follows up on the agent's answer to her own request about library availability, asking about ebook holds that the agent holds the information on.
- c: respond / direct / speak 5 / G6: Fatima follows up on her earlier exchange with Tess about library availability, which only the agent has been looking up.

**b07-00237/15** `follow_up_later` (G6): guide **wait**, majority **respond**
> Aisha: Wait, is that really true? That percent swap thing works every time?
> Zoe: I think so, yeah, I mean, it's just multiplying the same two numbers, right?
> **Zoe: So then the subtract-from-thousand thing, does that work with, like, 10,000 too?**

- a: respond / direct / speak 5 / G6: Zoe asks a follow-up about a subtraction technique Ace explained during the quiz it leads.
- b: respond / direct / speak 5 / G6: Ace runs the quiz and Zoe continues her own exchange with it, following up on the subtraction trick it explained to her.
- c: respond / direct / speak 5 / G6: The agent leads the tutoring session and Zoe is asking a follow-up math question about the earlier trick without addressing anyone else.

**b07-00259/11** `follow_up_later` (G6): guide **wait**, majority **respond**
> Tom: Femi, did you already tell Sarah's sister, or is that still on us?
> Femi: No, I— I messaged her but she hasn't, like, she hasn't seen it yet.
> **Tom: Do they, um, do they need a deposit for that back room, or is it just free if we drink?**

- a: respond / direct / speak 5 / G6: Tom returns to his exchange with Nova by asking about the back room it recommended.
- b: respond / direct / speak 5 / G6: Tom made the venue request the agent answered, and this follow-up about the back room it suggested continues his exchange with Nova.
- c: wait / open / speak 3 / G7: After turning away to talk to Femi, Tom asks an open question about the venue Nova suggested without calling anyone, which either Nova or a person could answer.

**b07-00267/6** `follow_up_later` (G6): guide **wait**, majority **respond**
> Tess: Honestly, we're at, like, three right now. Flour prices this year have just been brutal for us.
> Ella: It's the thing nobody tells you starting out — revenue looks great and then, I mean, the margin's just gone.
> **Ella: So what does a wholesale account actually do for margin, like, how much does it move it?**

- a: respond / direct / speak 5 / G6: Ella follows up on Cleo’s answer to her own question by asking how much wholesale accounts improve margins.
- b: respond / direct / speak 5 / G6: Ella called Cleo and got the answer mentioning wholesale accounts; this follows up on her own exchange with the agent without turning to anyone else.
- c: wait / open / speak 3 / G6: Ella follows up on Cleo's earlier point about wholesale accounts after talking with Tess, so the question could be for Cleo or for the group.

**b07-00267/16** `follow_up_later` (G6): guide **wait**, majority **respond**
> Victor: Let's take, like, a five-minute break after this segment, I need water.
> Ella: Yeah, fine by me, my voice is going anyway.
> **Ella: Wait, the county thing — is that, is that usually a fee, or just paperwork?**

- a: respond / direct / speak 5 / G6: Ella resumes her exchange with Cleo by asking about the county permit Cleo just mentioned.
- b: respond / direct / speak 5 / G6: Ella follows up on the agent's answer to her own licensing question, continuing her exchange with Cleo despite the brief break chatter.
- c: respond / direct / speak 5 / G6: Ella follows up directly on the county health department detail from Cleo's answer to her earlier question.

**b07-00321/7** `follow_up_later` (G6): guide **wait**, majority **respond**
> Tess: Now the frosting, do we even have enough butter for... hmm, maybe if I...
> Paul: Should we just ask the assistant about the frosting later, once these are in?
> **Paul: Wait, so the toothpick thing, does it have to come out totally clean, or like a few crumbs?**

- a: respond / direct / speak 5 / G6: Paul is following up on the toothpick advice the assistant gave him.
- b: respond / direct / speak 5 / G6: Paul is following up on the agent's own toothpick advice from his exchange with it, without turning to anyone else.
- c: wait / open / speak 3 / G6: Paul asks a follow-up question about the agent's earlier toothpick tip after turning to talk with Tess, making it unsettled whether he is asking Tess or the agent.

**b07-00335/11** `follow_up_later` (G6): guide **wait**, majority **respond**
> Theo: Fifty connections under peak load, that would explain the timeouts, unless something else is also...
> Petra: It caught that diff faster than any of us did, honestly.
> **Theo: Was the pool change the only thing in that push, or were there other settings?**

- a: respond / direct / speak 5 / G6: Theo follows up on Hugo's answer to his earlier question about the same config push.
- b: respond / direct / speak 5 / G6: Theo asked the earlier question the agent answered about the push, and this follows up on that answer, which only the agent has looked up.
- c: wait / open / speak 3 / G7: After the people talked among themselves, Theo asks an open question to the room about the config push that either a colleague or the agent could answer.

**b07-00348/10** `follow_up_later` (G6): guide **wait**, majority **respond**
> Lena: Locker it is. Whoever's free grabs it after work.
> Kwame: Fine. I pass Fenwick anyway.
> **Lena: How long does it sit there before going back?**

- a: respond / direct / speak 5 / G6: Lena follows up on Tess’s locker answer by asking how long the provider holds the parcel there.
- b: respond / direct / speak 5 / G6: Lena continues her own exchange with the agent about the locker, a question only the support agent holds the information for.
- c: respond / direct / speak 5 / G6: Tess is leading the support call and holds the delivery policy information that Lena is asking about.

**b07-00381/6** `follow_up_later` (G6): guide **wait**, majority **respond**
> Fatima: About that. Short thesis, done.
> Victor: Can someone send me your outlines tonight? Need to compare.
> **Fatima: Wait, does the counterargument count as one of the three?**

- a: respond / direct / speak 5 / G6: Fatima follows up on Cleo’s answer to her own question about the three body paragraphs.
- b: respond / direct / speak 5 / G6: Fatima is following up on Cleo's answer to her own question about body paragraphs, continuing her exchange with the agent.
- c: wait / open / speak 3 / G6: Fatima follows up on Cleo's earlier answer about three paragraphs after talking with the group, so it could be directed at Cleo or the study group.

**b07-00383/14** `follow_up_later` (G6): guide **wait**, majority **respond**
> Dev: Alexa, set a timer for fifteen minutes.
> Can: Mm-hm.
> **Ingrid: Does that Tuesday estimate assume the SSO bug gets fixed this week?**

- a: respond / direct / speak 5 / G6: Ingrid follows up on her exchange with Juno by asking about an assumption behind Juno’s release estimate.
- b: respond / direct / speak 5 / G6: Ingrid was the agent's last exchange partner and this follows up on the agent's own Tuesday estimate, which only the agent can explain.
- c: respond / direct / speak 5 / G6: Ingrid asks about the assumptions behind the Tuesday estimate that Juno provided earlier, which only Juno holds.

**b07-00385/20** `follow_up_later` (G6): guide **wait**, majority **respond**
> Zoe: Honestly, coins shifting means it's asleep on its hoard. That's our window.
> Tariq: Or it's awake and just fidgety. Dragons have anxiety too.
> **Tariq: So were those knights killed here, or just their stuff dumped?**

- a: respond / direct / speak 5 / G6: Tariq asks about the scene in the adventure Hugo is running without addressing another player.
- b: respond / direct / speak 5 / G6: The agent leads the game, and this question about the game world, put to nobody else, is its business to answer.
- c: respond / direct / speak 5 / G6: The agent leads the game session as game master, and Tariq asks an in-game question about the scene without calling anyone else.

**b07-00390/8** `follow_up_later` (G6): guide **wait**, majority **respond**
> Chen: Lucy, I think your coding round just went really differently from mine.
> Lucy: Yeah, she was, she was way more relaxed by the afternoon, honestly.
> **Finn: So what's the average across all four rounds then?**

- a: respond / direct / speak 5 / G6: Finn follows up on his scorecard exchange with Otto by asking for another calculation from the same data.
- b: respond / direct / speak 5 / G6: Finn is the agent's last partner and is asking a follow-up about the scorecard the agent put up and sorted, which the agent holds.
- c: wait / open / speak 3 / G7: After the people turned to talking among themselves, Finn asks an open factual question to the room that either a person or the agent could answer.

**b07-00395/14** `follow_up_later` (G6): guide **wait**, majority **respond**
> Olga: Wait, are you guys, like, actually studying for the exam this weekend?
> Jamal: Have either of you used it for, like, essay outlines yet?
> **Jamal: So, um, who took over after Augustus died in 14?**

- a: respond / direct / speak 5 / G6: Jamal returns to the Rome quiz Kai is running with a follow-up to Kai’s answer about Augustus.
- b: respond / direct / speak 5 / G6: Kai is running the Rome quiz and Jamal, its recent partner, follows up on its Augustus answer with a history question without calling anyone else.
- c: respond / direct / speak 5 / G6: The agent runs the quiz session and Jamal is asking a direct follow-up question to the agent's earlier answer about Augustus.

**c07-00264/4** `follow_up_later` (G6): guide **wait**, majority **respond**
> Kit: How long's the delay?
> Hugo: Looks like twenty minutes, maybe more.
> **Hugo: Is there a faster way around Route 9?**

- a: respond / direct / speak 5 / G6: Hugo follows up on Penny’s traffic report by asking for an alternate route.
- b: respond / direct / speak 5 / G6: Hugo continues his own exchange with Penny about the Route 9 accident, asking for a reroute that the in-car assistant handles.
- c: respond / direct / speak 5 / G6: Hugo continues his exchange with the in-car assistant to ask for an alternative route around the accident it just reported.

**c07-00350/11** `follow_up_later` (G6): guide **wait**, majority **respond**
> Sam: Does that fifteen percent apply to the, uh, the onboarding fee as well?
> Ravi: No, onboarding is a flat one-time charge, though we can sometimes waive half of it.
> **Ravi: Wait, if we go with the two-year plan, what's the policy if they drop below fifty seats?**

- a: respond / direct / speak 5 / G6: Ravi follows up on Bolt’s two-year pricing answer by asking what happens if the seat count drops below fifty.
- b: respond / direct / speak 5 / G6: Ravi, the agent's last partner, follows up his own two-year pricing question with a policy question that only the vendor's assistant would answer, since Ravi himself is the one asking.
- c: respond / direct / speak 5 / G6: Ravi refers to the customers on the call as 'they' and asks about the vendor policy on the two-year fifty-seat plan Bolt just quoted him, continuing his exchange with the agent.

**c07-00495/13** `follow_up_later` (G6): guide **wait**, majority **respond**
> Raf: Ninety days is tight for a full rollout.
> Dana: We only need the core module first.
> **Hugo: Does that four-day setup include data migration?**

- a: respond / direct / speak 5 / G6: Hugo follows up on the four-day setup estimate Kai gave in response to his question.
- b: respond / direct / speak 5 / G6: Hugo follows up on the agent's own answer to his question about the four-day setup, which only the vendor's assistant can clarify.
- c: respond / direct / speak 5 / G6: Hugo asks about the four-day setup mentioned by the vendor's AI assistant, which only the vendor's assistant can answer.

**c07-00509/9** `follow_up_later` (G6): guide **wait**, majority **respond**
> Kwame: Yeah, cutting it now.
> Kwame: Just watch the hallway.
> **Kwame: How many guards on this floor?**

- a: respond / direct / speak 5 / G6: Kwame asks the game master for an in-game detail, following up on the patrol timing.
- b: respond / direct / speak 5 / G6: The agent runs the game, and this is a game question only the GM can answer; Kwame doesn't call anyone else by name.
- c: respond / direct / speak 5 / G6: The agent leads the game session as game master, and Kwame asks a question about the game world that only the game master can answer.

**o07-00112/7** `follow_up_later` (G6): guide **wait**, majority **respond**
> Rosa: The customer seems pretty angry about the missing credit note.
> Connor: Yeah, he mentioned it in the last call too.
> **Chloe: Was that the thread with the attached PDF or just text?**

- a: respond / direct / speak 5 / G6: Chloe is following up with Ada about the email thread Ada shared in response to her request.
- b: wait / direct / speak 3 / G6: Chloe asks about the thread the agent pulled up for her, but two intervening lines between Rosa and Connor make it unclear whether she's continuing with the agent or asking the people.
- c: respond / direct / speak 5 / G6: Chloe follows up on her own exchange with Ada about the email thread.

**o07-00230/14** `follow_up_later` (G6): guide **wait**, majority **ignore**
> Eli: Open the dashboard, then click the migration icon.
> Eli: Raf, please make sure you have admin access.
> **Eli: Can we run a test migration before the real one?**

- a: ignore / other / speak 1 / G7: Eli is proposing a trial run to the team after discussing migration steps and access.
- b: ignore / other / speak 1 / G7: A proposal to the group about the people's own plans, with no question the agent is being asked to answer.
- c: wait / open / speak 3 / G7: Eli asks an open question about how the product's migration works to nobody in particular, which the vendor's AI assistant can answer if no one else does.

**o07-00238/8** `follow_up_later` (G6): guide **wait**, majority **ignore**
> Ivan: Has anyone here ever pulled logs from this system?
> Abena: I used it last month for the API failures.
> **Ivan: What is the maximum file size limit?**

- a: ignore / other / speak 1 / G7: Ivan follows up on Abena’s experience pulling logs from the system.
- b: wait / open / speak 3 / G6: A factual question about the logging system that could be for the agent (which answered earlier) or for Abena, who just said she used it, and nothing settles which.
- c: ignore / other / speak 1 / G7: Ivan is asking a follow-up question to Abena, who just answered his previous question about using the logging system.

**o07-00340/18** `follow_up_later` (G6): guide **wait**, majority **respond**
> Noah: I think we should stick to the plan.
> Chris: Okay, does anyone else have questions before we wait?
> **Noah: Does the doctor take insurance from Blue Cross?**

- a: respond / direct / speak 5 / G6: The insurance question continues the clinic intake that Nova is handling.
- b: wait / open / speak 3 / G7: Nobody is called; Chris asked for questions and Noah poses a factual clinic question the intake assistant could answer, but it is open to the room.
- c: respond / direct / speak 5 / G6: Nova is the clinic intake assistant leading the session, and Noah asks an intake-related question without addressing anyone else.

**o07-00362/13** `follow_up_later` (G6): guide **wait**, majority **respond**
> Hiro: Quinn, wait, sorry, Malik, did you send the contract over yet?
> Hiro: Quinn, can you actually, never mind, let's figure that out later.
> **Abena: Wait, how long does it take to provision the new API keys?**

- a: respond / direct / speak 5 / G6: Abena resumes her exchange with Quinn about the vendor’s API by asking a related follow-up.
- b: respond / direct / speak 5 / G6: Abena was the agent's last exchange partner on API limits and fees, and this follow-up about provisioning API keys carries on that exchange without turning to anyone else.
- c: wait / open / speak 3 / G7: After the conversation moved away from the agent, Abena asks an unaddressed question about the product that the vendor's assistant could answer if nobody else takes it.

**o07-00441/20** `follow_up_later` (G6): guide **wait**, majority **respond**
> Greg: I don't care about the poem right now.
> Imran: Indy is too literal.
> **Divya: What does resignation mean here?**

- a: respond / direct / speak 5 / G6: Divya is asking Indy to clarify a word it used in its answer to her.
- b: respond / direct / speak 5 / G6: Divya continues her own exchange with Indy, following up on the word 'resignation' from its answer to her.
- c: respond / direct / speak 5 / G6: Divya asks a direct follow-up question about a word the agent used in its previous answer to her.

**o07-00841/12** `follow_up_later` (G6): guide **wait**, majority **respond**
> Lucy: Wait, is it below sodium then?
> Pedro: Yeah, it's directly under it in the same group.
> **Pedro: Does it have a higher atomic mass than sodium?**

- a: respond / direct / speak 5 / G6: Pedro asks a follow-up about potassium in the quiz Iris is running.
- b: respond / direct / speak 5 / G6: Iris runs the quiz and just answered Pedro's chemistry question; this is Pedro's follow-up on the same topic, carrying on his exchange with the agent.
- c: respond / direct / speak 5 / G6: The agent leads the quiz session and Pedro asks a chemistry question carrying on the session's business without addressing anyone else.

**o07-00961/13** `follow_up_later` (G6): guide **wait**, majority **respond**
> Leila: Great, I'll write that down before we move on to the next set of questions.
> Jill: You should probably double-check the superscripts, I always mess those up.
> **Leila: Wait, does that mean it has a full outer shell?**

- a: respond / direct / speak 5 / G6: Leila is asking Bolt a follow-up about the electron configuration it just gave her.
- b: respond / direct / speak 5 / G6: Leila follows up on the agent's answer to her own question about argon, and the agent runs the quiz, so the question carries on her exchange with it.
- c: respond / direct / speak 5 / G6: The agent leads the quiz session and Leila asks a follow-up question to the agent's earlier answer about argon.

**o07-00999/11** `follow_up_later` (G6): guide **wait**, majority **respond**
> Greg: But the DNS propagation takes ten minutes, right? So we can't just flip it.
> Bea: Correct. We'd need to lower the TTL manually or use a local resolver trick.
> **Bea: Wait, does the backup cluster have the latest schema version deployed?**

- a: respond / direct / speak 5 / G6: Bea returns to her exchange with Sage about the backup cluster and asks a follow-up about its deployed schema.
- b: respond / direct / speak 5 / G6: Bea is continuing her own exchange with Sage about the backup cluster status, which Sage holds the information on, without turning to anyone else.
- c: wait / open / speak 3 / G7: After turning to discuss DNS with Greg, Bea asks an open question to the room about the backup cluster that either a teammate or Sage could answer.

**o07-01000/13** `follow_up_later` (G6): guide **wait**, majority **respond**
> Jon: I'll put a reminder in the diary right now.
> Ella: I honestly don't know which valve needs closing off.
> **Ella: So, do I need to isolate the gas before he arrives?**

- a: respond / direct / speak 5 / G6: Ella follows up on her booking exchange with Nova by asking what she needs to do before the engineer arrives.
- b: respond / direct / speak 5 / G6: Nova is the provider's support agent leading this support call, and Ella has been dealing with it about the booking, so her question about preparing for the engineer's visit carries on that business.
- c: respond / direct / speak 5 / G6: Nova is leading a support call, and Ella asks a direct support question about preparing for the engineer's visit without addressing anyone else.

**o07-01070/12** `follow_up_later` (G6): guide **wait**, majority **ignore**
> Hana: you should have told us that sooner.
> Sam: Hana, did Clover mention the dosage?
> **Sam: is this ibuprofen or naproxen?**

- a: respond / direct / speak 5 / G6: Sam asks a medication question that continues the clinic intake without calling anyone else.
- b: ignore / other / speak 2 / G7: Sam is continuing his exchange with Hana about the medication, and 'this' points to a physical item only the people can see.
- c: ignore / other / speak 1 / G7: Sam is continuing his exchange with Hana and asking about a physical pill in the room, which only Hana can identify.

**o07-01161/7** `follow_up_later` (G6): guide **wait**, majority **respond**
> Cal: Has anyone used this feature before?
> Cal: I did last month for the dryer.
> **Cal: How long does that usually take to fix?**

- a: respond / direct / speak 5 / G6: Cal follows up on Indy's diagnosis by asking how long the fix usually takes.
- b: wait / open / speak 3 / G7: An unaddressed question after a person-to-person exchange; the support agent could answer how long a fix takes, but a person might too.
- c: respond / direct / speak 5 / G6: The agent is the support agent leading the troubleshooting session, and Cal asks a direct support question without calling anyone else.

**o07-01272/8** `follow_up_later` (G6): guide **wait**, majority **respond**
> Amy: Okay, let's split up. Two per airlock.
> Amy: I'll take the port side.
> **Amy: Do those airlocks have electronic locks?**

- a: respond / direct / speak 5 / G6: Amy is asking the game master for another detail about the airlocks Frankie just described.
- b: respond / direct / speak 5 / G6: Amy follows up her own exchange with the game master about the airlocks, and the agent leads the session.
- c: respond / direct / speak 5 / G6: The agent leads the game session as game master, and Amy is asking a game-world question that only the agent can answer.

**o07-01299/7** `follow_up_later` (G6): guide **wait**, majority **respond**
> Can: I guess we'd better bring the heavy-duty tent.
> Tariq: It's definitely overthinking the precipitation levels.
> **Can: How long does the rain last?**

- a: respond / direct / speak 5 / G6: Can is following up on the forecast Pip gave him.
- b: respond / direct / speak 5 / G6: Can was the agent's last partner on the weather question, and this follow-up asks for forecast detail that only the agent supplied.
- c: wait / open / speak 3 / G7: After turning to talk with Tariq, Can asks an unaddressed question about the weather that the agent could answer.

**o07-01360/20** `follow_up_later` (G6): guide **wait**, majority **respond**
> Finn: Oskar, is that enough time for all our stuff?
> Oskar: Probably not. We have like ten big boxes already.
> **Oskar: What is that weekend surcharge actually, though?**

- a: respond / direct / speak 5 / G6: Oskar returns to his exchange with the assistant by asking it to quantify the weekend surcharge it just mentioned.
- b: respond / direct / speak 5 / G6: Oskar follows up on the agent's answer to his own request about weekend moves; only the agent holds that surcharge information.
- c: respond / direct / speak 5 / G6: Oskar asks a follow-up question about the weekend surcharge that the agent just looked up for him, holding information only the agent has.

**o07-01373/16** `follow_up_later` (G6): guide **wait**, majority **respond**
> Ingrid: Can you save that total for us?
> Ivan: Yeah, let's do that.
> **Ivan: Is there a cheaper option nearby?**

- a: respond / direct / speak 5 / G6: Ivan follows up on the hotel price Rook just gave him by asking about cheaper options nearby.
- b: respond / direct / speak 5 / G6: Ivan continues his own exchange with the agent about the hotel cost, asking a travel lookup only the agent is handling.
- c: respond / direct / speak 5 / G6: Ivan follows up on Rook's answer to his hotel price question with a lookup only the travel assistant would know.

**o07-01569/7** `follow_up_later` (G6): guide **wait**, majority **respond**
> Fatima: Probably, but I'm keeping my gun ready.
> Oskar: You guys remember it said the station was abandoned?
> **Oskar: How long has it been empty anyway?**

- a: respond / direct / speak 5 / G6: Oskar asks an in-world question about the station's history that Indy can answer as game master.
- b: respond / direct / speak 5 / G6: The agent leads the game and this question about the station's lore carries on that business without calling anyone else.
- c: wait / open / speak 3 / G7: Oskar is addressing the group ('You guys' in his previous turn) with an open lore question that either the other players or the game master could answer.

**o07-01740/13** `follow_up_later` (G6): guide **wait**, majority **respond**
> Pablo: This spelling test is getting way harder than I expected.
> Kate: Yeah, I'm just guessing on the last three.
> **Pablo: So does that mean I lose points for guessing wrong?**

- a: respond / direct / speak 5 / G6: Pablo asks about scoring in the quiz Frankie is running.
- b: respond / direct / speak 5 / G6: The agent runs the quiz, and this question about its scoring carries on that business without calling anyone else.
- c: respond / direct / speak 5 / G6: The agent leads the quiz session, and the speaker asks a question directly about the quiz's scoring rules without calling anyone else.

**o07-01897/4** `follow_up_later` (G6): guide **wait**, majority **respond**
> Tariq: Is that enough to cover the backend roles specifically?
> Rhys: Probably, but we might be short on the frontend side.
> **Rhys: How many of those fourteen actually passed the technical screen?**

- a: respond / direct / speak 5 / G6: Rhys follows up on Quinn’s pipeline answer by asking about the fourteen candidates it reported.
- b: respond / direct / speak 5 / G6: Rhys called Quinn earlier and now follows up on the agent's pipeline answer with a question only its data can answer.
- c: wait / open / speak 3 / G6: After briefly replying to Tariq, Rhys asks a follow-up question about Quinn's figure without calling anyone, leaving it open whether he is asking Quinn or the team.

**o07-01982/18** `follow_up_later` (G6): guide **wait**, majority **respond**
> Ada: But won't that break all our other settings?
> Dana: I guess we can just re-pair the phones quickly.
> **Dana: Wait, does the new router support mesh nodes?**

- a: respond / direct / speak 5 / G6: Dana continues the support session with a question about the new router’s capabilities.
- b: respond / direct / speak 5 / G6: Gus is leading this support session and Dana, its exchange partner, asks a support question that Gus could answer, without calling anyone else.
- c: respond / direct / speak 5 / G6: Gus is leading the support call and Dana asks a technical question about the provider's router without addressing anyone else.

**o07-02014/10** `follow_up_later` (G6): guide **wait**, majority **respond**
> Tess: Five. Psy-cho-lo-gy.
> Tess: That one trips everyone up.
> **Victor: Is the 'c' silent?**

- a: respond / direct / speak 5 / G6: Victor asks about the current quiz word, and Frankie is running the quiz.
- b: respond / direct / speak 5 / G6: The agent runs the quiz and Victor's question about the quiz word carries on that business without calling anyone else.
- c: wait / open / speak 3 / G6: Victor has been asking Tess about the spelling word, so this follow-up question could be directed at Tess, the group, or the AI tutor running the quiz.

**o07-02136/14** `follow_up_later` (G6): guide **wait**, majority **respond**
> Priya: I'm tired, so let's not go down another rabbit hole.
> Oskar: It's amazing how much work Otto takes off our plates.
> **Arjun: Wait, can you actually send those logs to the dev team directly?**

- a: respond / direct / speak 5 / G6: Arjun resumes his exchange with Otto by asking whether it can send the logs it offered to pull.
- b: respond / direct / speak 5 / G6: Arjun continues his own exchange with Otto, following up on its offer to pull the logs, which only the agent could do.
- c: respond / direct / speak 5 / G6: Arjun continues his earlier exchange with Otto about pulling the error logs, asking for an action that Otto just offered to perform.

**o07-02156/17** `follow_up_later` (G6): guide **wait**, majority **ignore**
> Ingrid: Let us just get this done quickly then.
> Jamal: Yeah, I am hungry too.
> **Ingrid: How much melatonin are we talking about?**

- a: ignore / other / speak 1 / G6: Ingrid is asking Jamal to clarify what he meant by a low dose.
- b: ignore / other / speak 1 / G6: Ingrid is asking Jamal about his own melatonin dose, which only he can answer, so the question is for him rather than the agent.
- c: ignore / other / speak 1 / G6: Ingrid is asking Jamal about the specific dosage of melatonin that Jamal mentioned taking.

**o07-02191/9** `follow_up_later` (G6): guide **wait**, majority **respond**
> Tess: So are we rushing to the airlock, or do we take the long way?
> Anna: I vote long way. That corridor is way too sketchy.
> **Tess: Wait, does the reserve recharge if we stay in the central hub?**

- a: respond / direct / speak 5 / G6: Tess asks the game master a follow-up about how the oxygen reserve works.
- b: respond / direct / speak 5 / G6: Tess follows up on the agent's own reserve answer to her, and the agent as game master holds the game-world information.
- c: respond / direct / speak 5 / G6: The agent leads the game session as game master, and Tess asks a game mechanics question without calling anyone else.

**o07-02268/22** `follow_up_later` (G6): guide **wait**, majority **respond**
> Harold: Could you reroll that last check?
> Pablo: I think that was against the rules.
> **Anna: Is there a way to bypass the trap?**

- a: respond / direct / speak 5 / G6: Anna asks an in-game question without addressing another player, so it is for Indy as game master.
- b: respond / direct / speak 5 / G6: The agent runs the game, and asking about bypassing a trap carries on that business without calling anyone else.
- c: respond / direct / speak 5 / G6: The agent leads the game session as game master, and Anna asks a question about the adventure environment without calling anyone else.

**o07-02434/13** `follow_up_later` (G6): guide **wait**, majority **respond**
> Olu: Kit, are you sure the gym floor is clean enough?
> Kit: Yeah, the janitors scrubbed it last night.
> **Kit: Wait, does the seven-thirty start include the electrical setup?**

- a: respond / direct / speak 5 / G6: Kit follows up on the seven-thirty time Bea gave in response to Kit's own question.
- b: respond / direct / speak 5 / G6: Kit, the agent's last partner, follows up on the agent's own seven-thirty answer without turning to anyone else, and the agent holds that information.
- c: wait / open / speak 3 / G6: Kit already turned away to speak with Olu for several turns, so this question about Bea's earlier answer could be addressed to either Bea or the room.

**o07-02697/14** `follow_up_later` (G6): guide **wait**, majority **ignore**
> Abena: So are we still sticking with the chicken, or are you too tired to cook?
> Cal: I'm too tired to cook, but I can handle the mixing part.
> **Abena: Wait, does the recipe specify which cut of chicken to use?**

- a: ignore / other / speak 1 / G7: Abena has turned back to Cal, and the question continues their discussion about cooking the chicken.
- b: wait / open / speak 3 / G7: Abena asks an unaddressed question about the recipe after the talk has moved on to people, so it could be for Cal or for the agent and nothing settles it.
- c: ignore / other / speak 1 / G7: Abena has turned to talking with Cal about cooking the chicken, and asks about the recipe they are using.

## Graded lines (0)

| Line | Kind | a | b | c |
|---|---|---|---|---|

## Calls and cost

| Member | Answered | Failed | Not by the configured model | Input tokens | Cached | Output tokens | Est. cost |
|---|---|---|---|---|---|---|---|
| a | 360 | 0 | 0 | 1,754,016 | 1,662,876 | 23,690 | $1.25 |
| b | 360 | 0 | 0 | 2,627,619 | 2,460,128 | 34,974 | $2.41 |
| c | 360 | 0 | 0 | 1,928,711 | 248,307 | 34,065 | $7.65 |
