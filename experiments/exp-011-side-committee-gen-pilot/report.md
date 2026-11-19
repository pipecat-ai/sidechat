# Committee pilot: exp-011-side-committee-gen-pilot

Generated 2026-11-18T23:53:31+00:00 by `sidechat/pipeline/label.py`. Every number below is measured in this run.

## What was run

- **Lines:** 450 from `corpus:gen-pilot:dev+test:450`, 430 with a definite decision in the guide and 20 graded.
- **Guide:** `sidechat-guide-0.3`, prompt hash `cd131e750b0b`.
- **Members:** a, b, c, one model family each, at low reasoning effort. Model ids are configuration, not named here (SD-09).
- **Label set:** `corpus:gen-pilot:dev+test:450-committee-0.3` in R2.

## Agreement with the guide

**Majority decision: 95.3% (410/430; 92.9 to 97.0).** Target 90%: met. No majority on the decision for 1 lines.

| | Decision | Intent | For the agent or not | Rule | Mean distance on `speak` |
|---|---|---|---|---|---|
| Majority | 95.3% (410/430; 92.9 to 97.0) | 94.7% (409/432; 92.1 to 96.4) | | | |
| Member a | 93.0% (400/430; 90.2 to 95.1) | 92.1% (398/432; 89.2 to 94.3) | 96.5% (410/425; 94.3 to 97.9) | 81.3% (366/450; 77.5 to 84.7) | 0.2 |
| Member b | 94.9% (408/430; 92.4 to 96.6) | 93.8% (405/432; 91.1 to 95.7) | 97.9% (416/425; 96.0 to 98.9) | 83.6% (376/450; 79.8 to 86.7) | 0.129 |
| Member c | 96.0% (413/430; 93.8 to 97.5) | 95.4% (412/432; 93.0 to 97.0) | 98.6% (419/425; 97.0 to 99.4) | 84.7% (381/450; 81.0 to 87.7) | 0.1 |

Members agreeing with each other on the decision: a-b 96.0% (432/450), a-c 94.9% (427/450), b-c 96.9% (436/450). All three give the same decision and intent on 90.9% (409/450) of lines.

**By the guide's decision**

| Guide says | Majority agrees |
|---|---|
| ignore | 97.9% (228/233; 95.1 to 99.1) |
| respond | 99.3% (142/143; 96.2 to 99.9) |
| wait | 74.1% (40/54; 61.1 to 83.9) |

**By rule**

| Rule | Majority agrees |
|---|---|
| G7 | 93.5% (172/184; 88.9 to 96.2) |
| G6 | 91.8% (89/97; 84.6 to 95.8) |
| G2 | 100.0% (71/71; 94.9 to 100.0) |
| G3 | 100.0% (32/32; 89.3 to 100.0) |
| G4 | 100.0% (31/31; 89.0 to 100.0) |
| G1 | 100.0% (9/9; 70.1 to 100.0) |
| G5 | 100.0% (4/4; 51.0 to 100.0) |
| G8 | 100.0% (2/2; 34.2 to 100.0) |

**Kinds under 100%**

| Kind | Majority agrees |
|---|---|
| `follow_up` | 94.7% (18/19) |
| `statement` | 93.3% (14/15) |
| `open_factual` | 83.3% (10/12) |
| `open_question` | 83.3% (10/12) |
| `unclear_after_agent` | 60.0% (6/10) |
| `continuing_with_person` | 88.9% (8/9) |
| `follow_up_by_other` | 75.0% (6/8) |
| `unclear_you` | 71.4% (5/7) |
| `you_to_person_after_agent` | 85.7% (6/7) |
| `open_request` | 33.3% (1/3) |
| `statement_of_need` | 50.0% (1/2) |
| `table_talk` | 0.0% (0/1) |

## Lines where the majority differs from the guide (20)

**a01-00039/18** `statement` (G7): guide **ignore**, majority **respond**
> Joy: Can you add that to the list?
> Ivan: Sure, I'll put it on the paper list too.
> **Joy: I usually take two tablets, maybe once or twice a month.**

- a: respond / direct / speak 5 / G6: Joy answers Gus’s outstanding intake question about how often she takes ibuprofen.
- b: respond / direct / speak 5 / G6: Joy is answering the agent's earlier question about how often she takes the pain medicine, in an intake session the agent leads.
- c: respond / direct / speak 5 / G6: The agent leads the intake session and asked how often she takes the pain medicine, which Joy is now answering.

**a01-00042/8** `open_request` (G7): guide **wait**, majority **respond**
> Fatima: Assistant, roughly how much is a lift ticket for a day?
> agent: An adult day ticket can cost around $200, though prices vary by date and when you buy.
> **Fatima: Oof. Can someone check what a two-day ticket might cost?**

- a: respond / direct / speak 5 / G6: Fatima follows up on Cleo’s answer to her own lift-ticket question without turning to anyone else.
- b: respond / direct / speak 5 / G6: Fatima just asked the agent about lift tickets and this follow-up continues her own exchange with it, asking for something squarely in its role.
- c: wait / open / speak 3 / G7: Fatima turns to the room ('someone') rather than continuing directly with the agent, making an open request that the agent could answer if nobody else takes it.

**b01-00000/18** `follow_up_by_other` (G6): guide **wait**, majority **respond**
> Bea: Casting now. How long's it last?
> agent: One hour, or until you attack. Plenty for the hoard.
> **Lena: Does casting make noise? Dragon awake?**

- a: respond / direct / speak 5 / G6: Lena asks the game master to clarify whether casting makes noise and whether the dragon is awake.
- b: respond / direct / speak 5 / G6: The agent leads the game and Lena's question about game state carries on that business without calling anyone else.
- c: respond / direct / speak 5 / G6: The agent leads the game session as game master, and Lena asks about the game state and mechanics without calling anyone else.

**b01-00006/1** `unclear_you` (G7): guide **wait**, majority **respond**
> Sara: Juno's got the judging rubric loaded. Whole thing.
> **Theo: Can you pull up the deadline for project boards?**

- a: respond / direct / speak 5 / G6: Theo’s “you” refers to Juno, whom Sara just identified as having the judging rubric loaded.
- b: respond / direct / speak 5 / G6: Right after Sara noted Juno holds the rubric, Theo's 'can you pull up' asks for information the agent holds and can display.
- c: wait / open / speak 3 / G7: Theo uses 'you' without naming anyone, and while Sara just mentioned Juno, 'you' could address either Juno or Sara.

**b01-00014/8** `open_question` (G7): guide **wait**, majority **ignore**
> agent: First is the CEO's opening remarks, then the Q3 financial review, then the hiring plan update.
> Ella: Earlier it said the financial review only has fifteen minutes, so we'd have to keep it tight.
> **Aisha: Does anyone know if, uh, if finance has signed off on the final numbers yet?**

- a: ignore / other / speak 1 / G7: Aisha asks the room about Finance’s sign-off, which Penny is not established to track.
- b: ignore / other / speak 1 / G7: Asks the room about what people in finance have done, a status only the people would know, not a lookup for the agent.
- c: ignore / other / speak 1 / G7: Aisha asks the room about an internal team approval status, which is a question about what people did or decided rather than something for the meeting room voice assistant.

**b01-00014/15** `unclear_you` (G7): guide **wait**, majority **respond**
> Aisha: No, the other one, the one with the regional breakdown.
> agent: Got it, that's slide sixteen, churn by region. It's on screen now.
> **Aisha: Could you, um, send that to everyone after the call?**

- a: respond / direct / speak 5 / G6: Aisha follows up directly with Penny about the slide Penny just displayed.
- b: respond / direct / speak 5 / G6: Aisha continues her own exchange with Penny, which just put the slide on screen, asking it to send that slide.
- c: respond / direct / speak 5 / G6: Aisha is continuing her ongoing exchange with Penny by making a follow-up request about the slide Penny just pulled up.

**b01-00032/7** `unclear_after_agent` (G6): guide **wait**, majority **respond**
> Priya: I want to, um, check the jaguar carvings. Like, are the eyes inset with anything?
> agent: Two of the six jaguars have green jade eyes. The other four sockets are empty and scratched.
> **Anna: Wait, scratched how? Like pried out, or worn down?**

- a: respond / direct / speak 5 / G6: Anna asks the game master to clarify a detail in the scene it just described.
- b: respond / direct / speak 5 / G6: The agent leads the game, and Anna's question carries on the scene by asking for details the game master just described.
- c: respond / direct / speak 5 / G6: The agent is the game master leading the adventure, and Anna asks a direct game question that only the agent can answer.

**b01-00049/5** `follow_up_by_other` (G6): guide **wait**, majority **respond**
> Ada: It's flashing E21, does that mean anything to you, Hugo?
> agent: E21 means a drain fault, usually a blocked pump filter. It's behind the small panel bottom-left.
> **Lucy: So do we need to drain the water before opening that panel?**

- a: respond / direct / speak 5 / G6: Lucy is continuing the troubleshooting that Hugo is leading by asking how to safely open the panel he identified.
- b: wait / direct / speak 3 / G6: Lucy, not the agent's last partner Ada, follows up on the agent's answer; it could be for the agent or the group, so waiting is safe.
- c: respond / direct / speak 5 / G6: The agent leads this support call and Lucy's question carries on the troubleshooting business directly after Hugo's instruction.

**b01-00053/6** `open_factual` (G7): guide **wait**, majority **ignore**
> Cal: I know. My change only swapped the stub library, timing shouldn't have moved.
> Chen: Anyone actually tried reproducing it locally, or are we all just hitting retry?
> **Chen: Is the failure always the same timeout, or are there different errors?**

- a: ignore / other / speak 1 / G7: Chen is continuing the team's discussion by asking what errors they observed in the test runs.
- b: ignore / other / speak 1 / G7: A question about the test failures the people have observed; it carries on the discussion between people, and the agent holds no record of it.
- c: ignore / other / speak 1 / G7: Chen is asking the team about their internal build failures, which is an ongoing discussion among the people that the agent has no record of.

**b01-00054/3** `unclear_after_agent` (G6): guide **wait**, majority **respond**
> Eli: Can the assistant tell us what we actually need for the allergy part before the doctor joins?
> agent: I'll need each allergen, the reaction you had, and roughly when it last happened.
> **Ingrid: Wait, every allergen? Even the, like, the seasonal stuff, pollen and all that?**

- a: respond / direct / speak 5 / G6: Ingrid asks Wren to clarify what counts as an allergen for the intake it is leading.
- b: respond / direct / speak 5 / G6: Ingrid is questioning the intake requirement Wren just gave in answer to a request made for her, and Wren leads the intake session, so the follow-up is for Wren.
- c: respond / direct / speak 5 / G6: The agent leads the intake session and only the agent knows what information it requires for the allergy intake.

**c01-00002/9** `unclear_after_agent` (G6): guide **wait**, majority **respond**
> Grace: Iris, can we do a harder one next, maybe in South America?
> agent: Sure, let's try South America. What is the capital of Bolivia?
> **Ngozi: Hold on, doesn't Bolivia have two capitals, or is one just the main one?**

- a: respond / direct / speak 5 / G6: Ngozi is asking Iris to clarify the quiz question Iris just posed to the group.
- b: respond / direct / speak 5 / G6: Iris runs the quiz and just asked about Bolivia's capital; Ngozi's question carries on that quiz business without calling anyone else.
- c: respond / direct / speak 5 / G6: The agent is running the quiz and just asked everyone a question, which Ngozi directly engages with without addressing another person.

**c01-00085/22** `continuing_with_person` (G7): guide **ignore**, majority **wait**
> agent: Sure, we can do percentages! What's twenty percent of eighty?
> Malik: I think, like, the max score we can get today is twenty points.
> **Malik: Do you remember how many we got right so far?**

- a: respond / direct / speak 5 / G6: Malik asks the tutor running the quiz for the tally so far.
- b: wait / open / speak 3 / G6: Max running the quiz could track the score, but Malik's 'you' could equally be for a fellow player, and nothing settles which.
- c: wait / open / speak 3 / G6: Malik asks 'you' about the quiz score without naming an addressee, which could be directed at the agent running the quiz or one of the other participants.

**o01-00043/18** `open_question` (G7): guide **wait**, majority **ignore**
> Malik: Can you remind me to bring the wrench?
> agent: Reminder set for tomorrow at 9 AM.
> **Diego: Does anyone know if the hallway light is on?**

- a: ignore / other / speak 1 / G7: Diego asks the room about a physical condition that Juno has no established way to check.
- b: ignore / other / speak 1 / G7: A question to the room about the physical state of the house that only a person present can check, not something the support agent can know.
- c: ignore / other / speak 1 / G7: Diego asks about the physical state of the hallway light, which only Malik in the house can know or check, not a support agent on a call.

**o01-00072/7** `open_request` (G7): guide **wait**, majority **ignore**
> Kofi: I'm grabbing pizza with my cousins. It's supposed to be a disaster.
> Zoe: Haha, sounds intense. Do you trust their cooking?
> **Zoe: Can someone check the current temperature of the water bath?**

- a: ignore / other / speak 1 / G7: Zoe is asking someone in the room to check the water bath, a physical task the assistant cannot perform.
- b: ignore / other / speak 1 / G7: A request to the room for a physical check of the water bath, which only a person present can carry out.
- c: ignore / other / speak 1 / G7: Zoe is asking someone in the room to physically check the water bath, which only a person present can do.

**o01-00106/6** `open_factual` (G7): guide **wait**, majority **respond**
> Kate: Thanks, that saves me a lot of guessing.
> agent: You're welcome.
> **Kate: When is the final draft actually due?**

- a: respond / direct / speak 5 / G6: Kate follows up on her exchange with Dash by asking another question about the same assignment.
- b: respond / direct / speak 5 / G6: Kate continues her own exchange with Dash, who just answered her and holds the rubric information, with a follow-up question.
- c: respond / direct / speak 5 / G6: Kate continues her exchange with the agent by asking a follow-up question right after the agent spoke to her.

**o01-00154/14** `you_to_person_after_agent` (G6): guide **ignore**, majority **wait**
> Tess: Can you throttle the incoming traffic to reduce the load?
> agent: I have reduced the inbound rate limit by 50 percent. Watch for stability.
> **Marta: You might want to verify that change, it seems aggressive.**

- a: wait / direct / speak 3 / G6: Marta follows up on Dash’s change but could be asking either Dash or Tess to verify it.
- b: wait / direct / speak 3 / G6: Marta, not the agent's last partner, challenges the agent's action with a 'you' that could be for Dash or for Tess, and nothing settles which.
- c: ignore / other / speak 1 / G6: Marta is advising Tess to manually verify the aggressive rate-limit change that Tess just asked the agent to make.

**o01-00194/13** `unclear_after_agent` (G6): guide **wait**, majority **ignore**
> Jill: Wait, is that a major issue or just noise?
> agent: It's likely just noise, but I'm monitoring it closely.
> **Omar: I'm not convinced that's just noise, it feels risky.**

- a: ignore / other / speak 1 / G6: Omar expresses doubt about Nova’s assessment without asking for a response.
- b: ignore / other / speak 1 / G6: Omar is remarking on the agent's answer without asking anything, which makes it a comment to the room.
- c: wait / direct / speak 3 / G6: Omar, who was not the agent's last partner, challenges the agent's answer, so it is unclear whether he is addressing Nova or the group.

**o01-00198/6** `follow_up` (G6): guide **respond**, majority **none**
> Malik: So we're basically baking in there all day, huh?
> agent: It'll be about seventy-eight degrees inside, so bring water.
> **Malik: Do we have enough fans to keep the judges comfortable?**

- a: respond / direct / speak 5 / G6: Malik follows up on Hugo’s answer about the gym temperature by asking whether there are enough fans.
- b: wait / open / speak 3 / G6: Malik continues his exchange with Hugo, but asking whether they have enough fans is about the group's own supplies, so it could be for Hugo or for the people and nothing settles it.
- c: ignore / other / speak 1 / G7: Malik asks the group a logistics question ('Do we have...') about their own physical supplies rather than continuing a factual lookup with the agent.

**o01-00228/0** `statement_of_need` (G7): guide **ignore**, majority **respond**
> **Petra: I have no idea which direction that corridor is facing.**

- a: respond / direct / speak 5 / G6: Petra is raising an in-game uncertainty that Ace can clarify as the game master.
- b: respond / direct / speak 4 / G6: Ace runs the adventure, and Petra's confusion about the corridor's direction is game business the game master should clarify, though she voices it as a remark rather than a direct question.
- c: ignore / other / speak 2 / G7: Petra makes a statement of uncertainty to the group with no direct question or action in the game yet, so the agent should not volunteer unasked help.

**o01-00268/0** `table_talk` (G7): guide **ignore**, majority **respond**
> **Chloe: I’m taking the long way through the sewers to avoid the guards.**

- a: respond / direct / speak 5 / G6: Chloe declares an in-game action for Wren, the game master, to resolve.
- b: respond / direct / speak 5 / G6: The agent is the game master leading the session, and the line is a player action carrying on the game without calling anyone else.
- c: respond / direct / speak 5 / G6: The agent leads the game session as game master, and Chloe declares an in-game action without calling anyone else.

## Graded lines (20)

| Line | Kind | a | b | c |
|---|---|---|---|---|
| Noor: Nova would know how long to wait. | `invite` | wait 3 | wait 3 | wait 3 |
| Zara: Ask Tess how big a van we need. | `invite` | wait 3 | wait 3 | wait 3 |
| Jack: I'd kind of like to know what Wren thinks about baking time for two eight-inch pans. | `indirect_wish` | respond 4 | respond 4 | respond 4 |
| Anna: Great, thanks, that's helpful. | `thanks` | ignore 1 | ignore 1 | respond 3 |
| Sam: Oh, awesome, thank you so much. | `thanks` | respond 5 | respond 3 | respond 3 |
| Ben: Okay, Remy would know. Ask Remy. | `invite` | wait 3 | wait 3 | wait 3 |
| Jack: Tess would know. | `invite` | wait 3 | wait 3 | wait 3 |
| Ingrid: Thanks, Wren, that was really quick. | `thanks_named` | respond 3 | respond 3 | respond 3 |
| Greg: If anyone needs the ticket numbers, just ask Penny. | `invite` | wait 3 | wait 3 | ignore 1 |
| Jamal: Okay, Remy, that's enough for now, you can close the spreadsheet. | `stop_named` | respond 5 | respond 5 | respond 5 |
| Ngozi: Um, Max would probably know the last deploy time. | `invite` | wait 3 | wait 3 | wait 3 |
| Diego: Okay, that helps. Thanks. | `thanks` | ignore 1 | respond 3 | respond 3 |
| Tess: Orion would know how far the walk actually is. | `invite` | wait 3 | wait 3 | wait 3 |
| Isis: Noa, ask Iris to list the missing names. | `relayed_invite` | wait 3 | wait 3 | wait 3 |
| Anna: Ask Iris about that. | `invite` | wait 3 | wait 3 | wait 3 |
| Noa: Wren, stop. | `stop_named` | ignore 3 | ignore 3 | ignore 3 |
| Imran: Wren, that's enough. | `stop_named` | ignore 3 | ignore 3 | ignore 3 |
| Noor: Goodnight, Kai. | `farewell_named` | respond 3 | respond 3 | respond 3 |
| Divya: Kai would know the current exchange rate. | `invite` | wait 3 | wait 3 | wait 3 |
| Lucia: Ember would know the pricing details for the upgrade. | `invite` | wait 3 | wait 3 | wait 3 |

## Calls and cost

| Member | Answered | Failed | Not by the configured model | Input tokens | Cached | Output tokens | Est. cost |
|---|---|---|---|---|---|---|---|
| a | 450 | 0 | 0 | 2,050,769 | 1,945,540 | 27,691 | $1.46 |
| b | 450 | 0 | 0 | 3,089,718 | 2,907,918 | 37,534 | $2.69 |
| c | 450 | 0 | 0 | 2,264,210 | 533,308 | 31,666 | $8.09 |
