# Jev baseline: exp-020-side-jev-ami-silent

Generated 2026-11-19T00:53:46+00:00 by `sidechat/pipeline/baseline.py`. Every number below is measured in this run.

## What was run

- **Model:** `jev-1.13.0`, asked with the daily-audience demo's two questions and state (commit `73171de`, wording hash `476c554866d6`), through Pipecat 1.16.0's `JevClassifier`.
- **Decision rule:** the demo's. Answer now when `addressed ≥ 0.8`, hold for silence when `question ≥ 0.5`, otherwise stay quiet.
- **Requests:** 10,433 distinct (0 reused from earlier runs, 10,433 asked now, 0 failed).
- **Tokens this run:** 8,209,027 in, 386,021 out. About $0.345 at $0.042 per million input tokens, a price recorded in Audience's repo and not confirmed with TypeSafe.
- **Baseline id:** `jev-demo-0.1`. Stored answers are reused, so later runs compare against these numbers.

A share is written `value (k/n; 95% interval)`. "For others" means lines the set marks as not for the agent.

## ami-silent-0.1.test

Source: `ACloudCenter/ami-addressee` at `4bab33cda780`. Use: train, dev and test by meeting series; the 22 labelled meetings are never trained on.

10,434 rows, 10,434 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 90.0% (9395/10434; 89.5 to 90.6) | 90.0% (9395/10434) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |
| Name said → answer | 100.0% (10434/10434; 100.0 to 100.0) | 100.0% (10434/10434) | 0.0% (0/10434) | 0.0% (0/10434) | n/a | n/a |

Jev latency from Modal: 148 ms at the median, 218 ms at the 95th percentile (10,434 answers, 12 requests at a time).

**By code** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `` | 10434 | 90.0% (9395/10434) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |

**By style** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `` | 10434 | 90.0% (9395/10434) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |

**By kind** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `ami_silent` | 10434 | 90.0% (9395/10434) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |

**Lines Jev decides differently from the label** (1039 of 10434)

| Line | Kind | Expected | Jev | addressed | question |
|---|---|---|---|---|---|
| A: Uh and to that end we need all to work together uh to do that. | `ami_silent` | ignore | wait | 0.04 | 0.50 |
| A: if if an anybody feels that they need to say more about themselves please do, | `ami_silent` | ignore | wait | 0.03 | 0.89 |
| A: if if if anybody wants to b briefly give their their background | `ami_silent` | ignore | wait | 0.03 | 0.91 |
| A: so that everybody's quite clear what everybody uh uh everybody's experience is | `ami_silent` | ignore | wait | 0.03 | 0.59 |
| A: please do so. Uh | `ami_silent` | ignore | wait | 0.03 | 0.84 |
| A: in fact I'd I'd I'd welcome anybody to uh say something briefly about themselves, | `ami_silent` | ignore | wait | 0.04 | 0.93 |
| A: and and saying what what contribution you you're looking to make. | `ami_silent` | ignore | wait | 0.04 | 0.84 |
| A: so we'll um uh we'll do a virtual drawing on the on on the whiteboard of of your your own uh uh favourite anim | `ami_silent` | ignore | wait | 0.05 | 0.76 |
| A: but le let's go round the table, | `ami_silent` | ignore | wait | 0.04 | 0.65 |
| A: your favourite animal. | `ami_silent` | ignore | wait | 0.04 | 0.66 |
| A: Mm and why? | `ami_silent` | ignore | wait | 0.06 | 0.63 |
| A: Sorry? | `ami_silent` | ignore | wait | 0.09 | 0.65 |
| A: would anybody like t like to to start by giving their o um sort of quick views of of current remote controls. | `ami_silent` | ignore | wait | 0.05 | 0.94 |
| A: Any any thoughts about buttons or any oth other way of approaching the p the uh the problem? | `ami_silent` | ignore | wait | 0.11 | 0.90 |
| A: Or anybody else, strong feelings about remote controls? | `ami_silent` | ignore | wait | 0.10 | 0.95 |
| A: Are there you know, bad ones they've used | `ami_silent` | ignore | wait | 0.09 | 0.93 |
| A: or good ones they've used | `ami_silent` | ignore | wait | 0.07 | 0.91 |
| A: or ones that they've lost and never found again? | `ami_silent` | ignore | wait | 0.12 | 0.92 |
| A: Um what so wh what's in in what particular style features are you thinking about? | `ami_silent` | ignore | wait | 0.09 | 0.82 |
| A: I mean do you think there's a risk if it doesn't look like remote control, | `ami_silent` | ignore | wait | 0.11 | 0.80 |
| A: Any other thoughts about um th the physical appearance of a of remote controls? | `ami_silent` | ignore | wait | 0.10 | 0.90 |
| A: Um any thoughts about buttons or flat screens or uh uh | `ami_silent` | ignore | wait | 0.06 | 0.90 |
| A: Um do we need it to uh | `ami_silent` | ignore | wait | 0.07 | 0.83 |
| A: Do we do we want uh | `ami_silent` | ignore | wait | 0.07 | 0.85 |
| C: Like a like a mobile phone? | `ami_silent` | ignore | wait | 0.12 | 0.84 |
| A: and that we want to uh uh uh t take over the entire um the planet with? | `ami_silent` | ignore | wait | 0.03 | 0.58 |
| A: first thoughts on um | `ami_silent` | ignore | wait | 0.06 | 0.53 |
| A: and um colours, materials? Kendra, anyone? | `ami_silent` | ignore | wait | 0.05 | 0.84 |
| C: how you can get the different um what are they called? Like the face-plates | `ami_silent` | ignore | wait | 0.08 | 0.81 |
| A: Um should have interchangeable fascias | `ami_silent` | ignore | wait | 0.09 | 0.53 |
| A: whether they mean th they don't want it to cover teletext | `ami_silent` | ignore | wait | 0.06 | 0.61 |
| A: or whether they don't want it to cover, you know, videos, D_V_D_s, um satellite boxes, | `ami_silent` | ignore | wait | 0.06 | 0.50 |
| A: But uh do do introduce some some constraints as to how we might do that. | `ami_silent` | ignore | wait | 0.07 | 0.80 |
| A: but uh um we we need to talk that through. | `ami_silent` | ignore | wait | 0.06 | 0.52 |
| A: um so I I I'll leave it up to you to who who who thinks they would like to go go first? | `ami_silent` | ignore | wait | 0.04 | 0.92 |
| D: Uh can I steal the cable? | `ami_silent` | ignore | wait | 0.11 | 0.86 |
| D: how do I start there? | `ami_silent` | ignore | wait | 0.35 | 0.88 |
| D: It also asked um if we would if people would pay more for speech recognition | `ami_silent` | ignore | wait | 0.19 | 0.72 |
| D: Um. You see this okay? | `ami_silent` | ignore | wait | 0.11 | 0.83 |
| D: no? | `ami_silent` | ignore | wait | 0.08 | 0.79 |
| D: You see what I mean? | `ami_silent` | ignore | wait | 0.16 | 0.81 |
| C: Have you seen the new mo mobile phones | `ami_silent` | ignore | wait | 0.08 | 0.88 |
| A: Uh. Should we actually bite the bullet here? | `ami_silent` | ignore | wait | 0.08 | 0.89 |
| A: If people really don't use those buttons to any extent at all um remove them altogether. | `ami_silent` | ignore | wait | 0.06 | 0.64 |
| D: Just remove them completely? | `ami_silent` | ignore | wait | 0.07 | 0.84 |
| A: I wonder whether we could get the remote control with no buttons at all if we went for voice recognition, | `ami_silent` | ignore | wait | 0.06 | 0.84 |
| A: do we know whether they | `ami_silent` | ignore | wait | 0.09 | 0.85 |
| A: would people miss them? | `ami_silent` | ignore | wait | 0.10 | 0.89 |
| A: carry on. | `ami_silent` | ignore | wait | 0.09 | 0.57 |
| A: Do you want to just carry on with | `ami_silent` | ignore | wait | 0.08 | 0.82 |
| D: if we could uh power on and channel selection and and volume selection, wouldn't have to really | `ami_silent` | ignore | wait | 0.14 | 0.70 |
| A: who | `ami_silent` | ignore | wait | 0.09 | 0.81 |
| D: Do you want the cable? | `ami_silent` | ignore | wait | 0.05 | 0.83 |
| C: Is it doing | `ami_silent` | ignore | wait | 0.08 | 0.85 |
| C: Um we want something that sends messages easily to the television | `ami_silent` | ignore | wait | 0.12 | 0.62 |
| C: and I was kind of wondering about this example that they have. | `ami_silent` | ignore | wait | 0.14 | 0.64 |
| B: Which one does this plug into? | `ami_silent` | ignore | wait | 0.11 | 0.83 |
| B: I can't did you | `ami_silent` | ignore | wait | 0.07 | 0.69 |
| B: could you see it on you screen | `ami_silent` | ignore | wait | 0.11 | 0.80 |
| B: which will be the part that actually what? Sends signals to the the television. | `ami_silent` | ignore | wait | 0.05 | 0.82 |
| A: Um I don't suppose we've got any statistics on the the life expectancy of uh remote controls, particularly sor | `ami_silent` | ignore | wait | 0.09 | 0.87 |
| A: uh uh p perhaps we should, know, reduce the uh, you know, the sort of moving parts even more by not even havin | `ami_silent` | ignore | wait | 0.07 | 0.62 |
| B: Just having one that's guaranteed to last five to ten years? | `ami_silent` | ignore | wait | 0.10 | 0.72 |
| A: Are are people really gonna use it though? Um. | `ami_silent` | ignore | wait | 0.06 | 0.92 |
| A: what so wh what what do we think about the um the the permanent mm battery? | `ami_silent` | ignore | wait | 0.10 | 0.90 |
| A: Is the | `ami_silent` | ignore | wait | 0.09 | 0.74 |
| C: Do they make batteries that last that long? | `ami_silent` | ignore | wait | 0.07 | 0.86 |
| B: Most of them, don't they have sort of a combination of the two, | `ami_silent` | ignore | wait | 0.13 | 0.83 |
| A: th th this needs going t into the technology a bit. | `ami_silent` | ignore | wait | 0.08 | 0.52 |
| C: Per hour? | `ami_silent` | ignore | wait | 0.07 | 0.83 |
| A: but if you can incorporate um channel change and volume buttons um in into the design, then then that's fine. | `ami_silent` | ignore | wait | 0.09 | 0.69 |
| A: Um uh d so does that accurately summarise what we've discussed? | `ami_silent` | ignore | wait | 0.16 | 0.89 |
| C: I just have one question. | `ami_silent` | ignore | wait | 0.07 | 0.62 |
| C: are we doing just the television | `ami_silent` | ignore | wait | 0.16 | 0.81 |
| C: or are we doing | `ami_silent` | ignore | wait | 0.23 | 0.84 |
| C: so not D_V_D_ players, | `ami_silent` | ignore | wait | 0.25 | 0.67 |
| A: no? | `ami_silent` | ignore | wait | 0.10 | 0.75 |
| D: Didn't you mention the teletext, just television only? | `ami_silent` | ignore | wait | 0.14 | 0.73 |
| A: we can all give some thought to that uh for for the next meeting, | `ami_silent` | ignore | wait | 0.03 | 0.56 |
| A: Alright? | `ami_silent` | ignore | wait | 0.16 | 0.85 |
| A: um and come up with some interesting uh uh w suggestions for our our new remote control. | `ami_silent` | ignore | wait | 0.05 | 0.51 |
| A: Um and the the decisions that we need to to make today, finally, are um what energy source we want to use, | `ami_silent` | ignore | wait | 0.05 | 0.52 |
| A: whether i it is practical to use uh um a a a long lasting one. | `ami_silent` | ignore | wait | 0.05 | 0.69 |
| A: um d d do we go for a custom designed chip? | `ami_silent` | ignore | wait | 0.07 | 0.78 |
| A: Or or do we buy one off the shelf and and programme it ourselves? | `ami_silent` | ignore | wait | 0.06 | 0.87 |
| A: if if we can have the the three presentations again please, | `ami_silent` | ignore | wait | 0.05 | 0.83 |
| B: as for how we should end up uh using this in our remote uh t couple of main questions are the buttons. | `ami_silent` | ignore | wait | 0.10 | 0.53 |
| A: so how um | `ami_silent` | ignore | wait | 0.08 | 0.72 |
| A: can you uh just put that one back up again, please? Um. | `ami_silent` | ignore | wait | 0.11 | 0.75 |
| A: Do we do we know uh by how much? | `ami_silent` | ignore | wait | 0.08 | 0.86 |
| A: And and do we know how long it'll take to uh develop a a custom chip. | `ami_silent` | ignore | wait | 0.06 | 0.89 |
| A: I think we need to make a a decision here. | `ami_silent` | ignore | wait | 0.07 | 0.52 |
| A: Um uh now before we go round everybody else, does anybody um | `ami_silent` | ignore | wait | 0.05 | 0.86 |
| A: h have any have anyti ha anything to say about that? | `ami_silent` | ignore | wait | 0.05 | 0.90 |
| C: I just have a question about that. | `ami_silent` | ignore | wait | 0.04 | 0.53 |
| C: Um does it make a difference if there are just a few commands, | `ami_silent` | ignore | wait | 0.05 | 0.86 |
| C: for example if you um can pre-programme in like numbers one through ten | `ami_silent` | ignore | wait | 0.06 | 0.87 |
| C: and pre-programme say, you know, nine channels | `ami_silent` | ignore | wait | 0.16 | 0.73 |
| C: and then just use the voice recognition to say channel one | `ami_silent` | ignore | wait | 0.13 | 0.66 |
| C: it's like to have a certain number of favourites um | `ami_silent` | ignore | wait | 0.40 | 0.65 |
| A: this is the internal company information, is it? | `ami_silent` | ignore | wait | 0.21 | 0.86 |
| A: uh perhaps we ought to uh stick to uh to buttons, | `ami_silent` | ignore | wait | 0.10 | 0.57 |
| A: Thoughts? | `ami_silent` | ignore | wait | 0.11 | 0.94 |
| D: Would | `ami_silent` | ignore | wait | 0.06 | 0.70 |
| A: I mean do w do we think that the voice technology is fundamental to the project? | `ami_silent` | ignore | wait | 0.09 | 0.92 |
| A: do we need the five buttons for channel change, up down, volume up down and on off, just as a a backup or just | `ami_silent` | ignore | wait | 0.07 | 0.92 |
| A: d did you want to say anything? | `ami_silent` | ignore | wait | 0.07 | 0.84 |
| A: No? | `ami_silent` | ignore | wait | 0.09 | 0.61 |
| A: Shall we move rapidly on to uh Kendra? | `ami_silent` | ignore | wait | 0.05 | 0.80 |
| A: Uh um ra rapidly move the cable over. | `ami_silent` | ignore | wait | 0.06 | 0.75 |
| C: Is it gonna work? | `ami_silent` | ignore | wait | 0.09 | 0.85 |
| C: what | `ami_silent` | ignore | wait | 0.10 | 0.74 |
| C: Bring a little picture of what I thought ours could look like. | `ami_silent` | ignore | wait | 0.11 | 0.62 |
| A: if I can interrupt you. | `ami_silent` | ignore | wait | 0.08 | 0.52 |
| A: do you wanna say anything about um slide controls? | `ami_silent` | ignore | wait | 0.10 | 0.83 |
| D: if you g if you if you got a channel up down, we can have a slider in that as well. | `ami_silent` | ignore | wait | 0.27 | 0.55 |
| C: but what what do you guys think? | `ami_silent` | ignore | wait | 0.10 | 0.92 |
| A: is that that all you want to say at the mo | `ami_silent` | ignore | wait | 0.09 | 0.74 |
| D: I s that out of sequence? | `ami_silent` | ignore | wait | 0.13 | 0.86 |
| A: What? | `ami_silent` | ignore | wait | 0.08 | 0.78 |
| D: Um you have we could if we could save | `ami_silent` | ignore | wait | 0.09 | 0.63 |
| D: depending on the cost of the product itself, you know, could we have uh a cheaper b cheaper power source and t | `ami_silent` | ignore | wait | 0.08 | 0.87 |
| C: What if we included the batteries in the cover? | `ami_silent` | ignore | wait | 0.06 | 0.93 |
| C: can I see that thing? | `ami_silent` | ignore | wait | 0.09 | 0.81 |
| D: are we gonna make this as part of like like uh a part of the f like it it | `ami_silent` | ignore | wait | 0.10 | 0.83 |
| D: so are we gonna make this part of the furniture? | `ami_silent` | ignore | wait | 0.08 | 0.89 |
| A: um w we need to decide on the just the basic shape of the thing. | `ami_silent` | ignore | wait | 0.06 | 0.69 |
| A: And, know whether we go down the fruit and veg route, | `ami_silent` | ignore | wait | 0.06 | 0.55 |
| A: and, you know, whether whether the you know, the the fixed part of it is the corporate yellow. Um | `ami_silent` | ignore | wait | 0.04 | 0.65 |
| C: um maybe we could make it a slightly different shape | `ami_silent` | ignore | wait | 0.06 | 0.60 |
| C: What do you guys think about that? | `ami_silent` | ignore | wait | 0.09 | 0.94 |
| D: I mean are we are we starting to get away from the the voice functionality of it? | `ami_silent` | ignore | wait | 0.13 | 0.90 |
| B: But do you know, this shape also kind of les lend itself to to voice | `ami_silent` | ignore | wait | 0.05 | 0.75 |
| C: So I guess we could have a menu button as well. | `ami_silent` | ignore | wait | 0.09 | 0.52 |
| A: Do we need some sort of display? | `ami_silent` | ignore | wait | 0.09 | 0.92 |
| B: I never understood how that worked though, | `ami_silent` | ignore | wait | 0.07 | 0.54 |
| C: You know what I mean? | `ami_silent` | ignore | wait | 0.06 | 0.78 |
| A: and uh pa play play with a bit of Plasticine or play-dough, | `ami_silent` | ignore | wait | 0.07 | 0.54 |
| D: Uh can I just get some things clear just for my sake. | `ami_silent` | ignore | wait | 0.06 | 0.83 |
| D: And we're having a custom chip? | `ami_silent` | ignore | wait | 0.08 | 0.86 |
| D: And interchangeable case? | `ami_silent` | ignore | wait | 0.06 | 0.83 |
| D: And uh are we gonna have it il being illuminated from inside onto the buttons or | `ami_silent` | ignore | wait | 0.10 | 0.86 |
| D: Are we having it that it's any angle, or is it just | `ami_silent` | ignore | wait | 0.06 | 0.86 |
| C: Like this or like this. | `ami_silent` | ignore | wait | 0.08 | 0.74 |
| A: So f if if you'd like to uh present your your proposals. | `ami_silent` | ignore | wait | 0.06 | 0.83 |
| A: I just wondered I mean h how will people put these down I wonder? | `ami_silent` | ignore | wait | 0.08 | 0.88 |
| A: What's on the next one? | `ami_silent` | ignore | wait | 0.09 | 0.86 |
| A: Does anybody want to uh | `ami_silent` | ignore | wait | 0.05 | 0.90 |
| A: where where you know well where where we're where where we're at? | `ami_silent` | ignore | wait | 0.04 | 0.77 |
| D: The the product or the project? | `ami_silent` | ignore | wait | 0.05 | 0.64 |
| D: my presentation just now? | `ami_silent` | ignore | wait | 0.06 | 0.73 |
| D: uh can I get the | `ami_silent` | ignore | wait | 0.41 | 0.83 |
| D: um gauge our team response to these questions. | `ami_silent` | ignore | wait | 0.05 | 0.63 |
| D: on a scale of one to seven, one being true and seven being being false. | `ami_silent` | ignore | wait | 0.06 | 0.62 |
| D: Is the device f flashy and fashionable? | `ami_silent` | ignore | wait | 0.22 | 0.89 |
| D: and also uh technologically innovative? | `ami_silent` | ignore | wait | 0.17 | 0.92 |
| D: Easy to use? | `ami_silent` | ignore | wait | 0.11 | 0.92 |
| D: Uh suitable for the consumer? | `ami_silent` | ignore | wait | 0.10 | 0.89 |
| D: Uh is it complicated? | `ami_silent` | ignore | wait | 0.10 | 0.90 |
| D: aren't we? | `ami_silent` | ignore | wait | 0.09 | 0.81 |
| D: Uh functional? | `ami_silent` | ignore | wait | 0.15 | 0.84 |
| D: Um. Where are we? | `ami_silent` | ignore | wait | 0.09 | 0.93 |
| D: We've b built in the the speech, where are you, function. | `ami_silent` | ignore | wait | 0.32 | 0.83 |
| A: Does it take long to learn to use? | `ami_silent` | ignore | wait | 0.23 | 0.91 |
| D: what else? | `ami_silent` | ignore | wait | 0.18 | 0.85 |
| D: Um will device appeal to all age groups? | `ami_silent` | ignore | wait | 0.08 | 0.90 |
| A: why not? | `ami_silent` | ignore | wait | 0.09 | 0.85 |
| D: Uh can you just click the my mouse to move onto next page? | `ami_silent` | ignore | wait | 0.26 | 0.87 |
| D: and what h did we make the management's | `ami_silent` | ignore | wait | 0.06 | 0.84 |
| A: is t it's television only, | `ami_silent` | ignore | wait | 0.09 | 0.82 |
| A: coming up with what | `ami_silent` | ignore | wait | 0.06 | 0.81 |
| A: Need a need a calculator for that. | `ami_silent` | ignore | wait | 0.10 | 0.81 |
| A: either of you want to uh say anything? | `ami_silent` | ignore | wait | 0.05 | 0.92 |
| A: Um are the costs within budget? | `ami_silent` | ignore | wait | 0.05 | 0.90 |
| A: Is the project evaluated? | `ami_silent` | ignore | wait | 0.07 | 0.90 |
| A: So um if you want, I'll just give a brief overview of what's happening | `ami_silent` | ignore | wait | 0.03 | 0.62 |
| A: Well you know how many of us are are present | `ami_silent` | ignore | wait | 0.06 | 0.81 |
| D: are they number of people per room indicated strict, or can we play around with? | `ami_silent` | ignore | wait | 0.09 | 0.82 |
| D: I mean if there are two people, is it really that you can't put three or uh two and a half or uh | `ami_silent` | ignore | wait | 0.07 | 0.79 |
| D: how how was it calculated? | `ami_silent` | ignore | wait | 0.08 | 0.82 |
| A: What's What should be said here, | `ami_silent` | ignore | wait | 0.12 | 0.86 |
| A: I don't know if, well, you | `ami_silent` | ignore | wait | 0.09 | 0.53 |
| A: I I will maybe distribute now documents if you don't have them. | `ami_silent` | ignore | wait | 0.07 | 0.52 |
| D: Are you sure of that? | `ami_silent` | ignore | wait | 0.16 | 0.77 |
| C: Do we really need that? | `ami_silent` | ignore | wait | 0.08 | 0.89 |
| D: so you should be able to valorize this if possible. | `ami_silent` | ignore | wait | 0.12 | 0.68 |
| A: Maybe we can think of, yeah, some two or three, yeah, for visiting people. | `ami_silent` | ignore | wait | 0.06 | 0.53 |
| A: So we also need to to find the a spot for the photocopier, the fax machine, and the printer. | `ami_silent` | ignore | wait | 0.04 | 0.51 |
| A: ask the people you know, your assistants, for instance, | `ami_silent` | ignore | wait | 0.20 | 0.75 |
| C: And if we don't get this space then what happens? | `ami_silent` | ignore | wait | 0.09 | 0.91 |
| A: Uh if i if we don't get these? | `ami_silent` | ignore | wait | 0.06 | 0.80 |
| A: Do do you think there are chances that they take from us one of the rooms or uh | `ami_silent` | ignore | wait | 0.04 | 0.87 |
| A: Um okay, so maybe we could try to to see now what would be the main options. | `ami_silent` | ignore | wait | 0.06 | 0.65 |
| A: Say the general uh, well, arrangement options. | `ami_silent` | ignore | wait | 0.09 | 0.88 |
| A: Do you think that we should put people, say, according to projects for instance? | `ami_silent` | ignore | wait | 0.10 | 0.90 |
| A: So how | `ami_silent` | ignore | wait | 0.08 | 0.77 |
| D: but uh one again clarification question, | `ami_silent` | ignore | wait | 0.08 | 0.67 |
| D: what is the real margin of manoeuvre that we have for these discussions, | `ami_silent` | ignore | wait | 0.06 | 0.84 |
| D: because uh at least we are half per cent uh fifty per cent of from E_P_F_L_ | `ami_silent` | ignore | wait | 0.05 | 0.52 |
| D: so what what will be the impact of what we will come out come up with? | `ami_silent` | ignore | wait | 0.06 | 0.84 |
| D: Another way of asking the question, is there any other group already working on uh on the how this should be u | `ami_silent` | ignore | wait | 0.29 | 0.90 |
| D: Or are we the the one that is supposed to do the p the the p position for it? | `ami_silent` | ignore | wait | 0.18 | 0.86 |
| D: But wha why why don't they have any representative here. | `ami_silent` | ignore | wait | 0.44 | 0.89 |
| C: why didn't we have a meeting together? | `ami_silent` | ignore | wait | 0.06 | 0.88 |
| D: why do we do it separately? | `ami_silent` | ignore | wait | 0.04 | 0.89 |
| A: So that would have been maybe, yeah, another solution is to ask everyone to provide uh an arrangement, | `ami_silent` | ignore | wait | 0.05 | 0.50 |
| A: Um so since all of you have a copy of the uh, well, of the drawing, I think for the next time, m maybe you cou | `ami_silent` | ignore | wait | 0.04 | 0.85 |
| A: But let us try to see today whether we prefer to organise people, say, by projects or just professor and assis | `ami_silent` | ignore | wait | 0.04 | 0.87 |
| A: So what would be f, say, first your preferences, | `ami_silent` | ignore | wait | 0.06 | 0.89 |
| A: Let's let's start with us, maybe today. | `ami_silent` | ignore | wait | 0.08 | 0.71 |
| A: Um what do you think about it? | `ami_silent` | ignore | wait | 0.09 | 0.91 |
| A: Would you prefer to be alone, | `ami_silent` | ignore | wait | 0.07 | 0.82 |
| A: would you prefer to be with your assistant. | `ami_silent` | ignore | wait | 0.09 | 0.82 |
| A: You who are part-time, do you think you can come here on a very w well regular schedule or is it part-time, bu | `ami_silent` | ignore | wait | 0.04 | 0.78 |
| B: Uh I still would like to have my drawers and these things. | `ami_silent` | ignore | wait | 0.34 | 0.63 |
| A: Are you disturbed by the phone calls of other people? | `ami_silent` | ignore | wait | 0.06 | 0.64 |
| C: Ye mm before um talking more about individual preferences, is there any possibility, what they have done in th | `ami_silent` | ignore | wait | 0.06 | 0.83 |
| C: So one option and that but that we would need to ask about if we could uh split one of the rooms uh | `ami_silent` | ignore | wait | 0.05 | 0.59 |
| D: Do you go for boxes for instance? | `ami_silent` | ignore | wait | 0.06 | 0.81 |
| C: So I mean I think that we should still check with them | `ami_silent` | ignore | wait | 0.05 | 0.59 |
| A: Um, maybe we could s look a bit at the projects. | `ami_silent` | ignore | wait | 0.08 | 0.61 |
| A: Do you think it's a good idea to put together in the same room as much as possible people from the same projec | `ami_silent` | ignore | wait | 0.06 | 0.88 |
| A: since they talk quite a lot of to each other? | `ami_silent` | ignore | wait | 0.11 | 0.79 |
| D: But uh I would p probably formulate it in the way that uh, do we want to have only a lounge or s something tha | `ami_silent` | ignore | wait | 0.04 | 0.86 |
| A: And the other question is, can we squeeze maybe four people in the uh or at least four places in the three thr | `ami_silent` | ignore | wait | 0.08 | 0.88 |
| A: so you don't really feel um very strongly attached to this uh grouping by projects idea? | `ami_silent` | ignore | wait | 0.06 | 0.78 |
| D: you f more need about th to discuss about where is the printer, how do I get furniture, I'm I don't have a a p | `ami_silent` | ignore | wait | 0.10 | 0.78 |
| A: Um, are you aware f of any strong constraints right now? | `ami_silent` | ignore | wait | 0.04 | 0.85 |
| B: Is it allowed to smoke inside an office, if it's a one person | `ami_silent` | ignore | wait | 0.17 | 0.92 |
| D: Not even in the cafeteria? | `ami_silent` | ignore | wait | 0.08 | 0.86 |
| D: Downstairs? | `ami_silent` | ignore | wait | 0.06 | 0.80 |
| D: On the roof maybe. | `ami_silent` | ignore | wait | 0.06 | 0.68 |
| B: there there's no place in inside the building? | `ami_silent` | ignore | wait | 0.05 | 0.85 |
| A: O on the toilets or | `ami_silent` | ignore | wait | 0.12 | 0.69 |
| D: And uh if you put two person persons or three persons for the admin space, who who who else would you put in t | `ami_silent` | ignore | wait | 0.09 | 0.84 |
| D: Maybe you could put some visitors, but um I know. It's not very uh realistic in a in a in an admin room, but u | `ami_silent` | ignore | wait | 0.19 | 0.56 |
| C: Why don't we ask about that? | `ami_silent` | ignore | wait | 0.10 | 0.86 |
| A: Uh, the the middle one here? | `ami_silent` | ignore | wait | 0.07 | 0.72 |
| D: But then uh that the the question of what do we do with the second position there remains fully open. | `ami_silent` | ignore | wait | 0.26 | 0.62 |
| D: So I would be I would be more of the opinion to to see whether it's it's so evident that, let's say the at lea | `ami_silent` | ignore | wait | 0.07 | 0.56 |
| D: I mean, you have you have a fore foreign researcher coming visiting you and you will put put him in the admin  | `ami_silent` | ignore | wait | 0.47 | 0.75 |
| D: Yeah? | `ami_silent` | ignore | wait | 0.06 | 0.67 |
| D: Is that so? | `ami_silent` | ignore | wait | 0.05 | 0.76 |
| A: Uh could we try So could you try please to uh | `ami_silent` | ignore | wait | 0.08 | 0.75 |
| A: Do you want an extra uh piece of paper? | `ami_silent` | ignore | wait | 0.07 | 0.77 |
| A: Maybe try to, well, think on your own and then talk a little bit just to the people around you. | `ami_silent` | ignore | wait | 0.05 | 0.72 |
| D: Yeah, b why why couldn't we do like couldn't we do it like for for the the set-up of meetings. | `ami_silent` | ignore | wait | 0.11 | 0.89 |
| A: So w w w will you ask people just for their place or also for the other people's place? | `ami_silent` | ignore | wait | 0.10 | 0.84 |
| B: W what abou what about the the the cafeteria? | `ami_silent` | ignore | wait | 0.09 | 0.87 |
| B: I mean, we are going to purchase a cafeteria with a projector and all this altogether or | `ami_silent` | ignore | wait | 0.06 | 0.86 |
| A: Okay then for the next time, um try to come up either with your own preferences, | `ami_silent` | ignore | wait | 0.05 | 0.78 |
| A: or if you can poll a little bit the people around you, | `ami_silent` | ignore | wait | 0.05 | 0.57 |
| D: The one that I don't want to have in the next room? | `ami_silent` | ignore | wait | 0.44 | 0.76 |
| A: I was thinking just ask people around you what they think about this. | `ami_silent` | ignore | wait | 0.07 | 0.62 |
| A: If you can do slides, it's even better, | `ami_silent` | ignore | wait | 0.06 | 0.51 |
| B: Bu I ju just before finishing uh, I mean, we have a cafeteria or we don't eat at all? | `ami_silent` | ignore | wait | 0.06 | 0.87 |
| A: What do you mean by cafeteria exactly? | `ami_silent` | ignore | wait | 0.06 | 0.88 |
| B: A place n what mm uh we can take a coffee also. | `ami_silent` | ignore | wait | 0.12 | 0.64 |
| A: What | `ami_silent` | ignore | wait | 0.06 | 0.73 |
| B: No? | `ami_silent` | ignore | wait | 0.12 | 0.75 |
| B: But they close at five or? | `ami_silent` | ignore | wait | 0.36 | 0.83 |
| A: Could we try to meet uh next Tuesday? | `ami_silent` | ignore | wait | 0.07 | 0.91 |
| D: T to try the coffee? | `ami_silent` | ignore | wait | 0.05 | 0.80 |
| A: Um, next Tuesday maybe at t maybe a bit later? | `ami_silent` | ignore | wait | 0.04 | 0.78 |
| A: Maybe at eleven o'clock? | `ami_silent` | ignore | wait | 0.04 | 0.87 |
| A: Come on, try try to be nice. | `ami_silent` | ignore | wait | 0.07 | 0.66 |
| A: Gi give me a reasonable date. | `ami_silent` | ignore | wait | 0.04 | 0.73 |
| D: Where is the meeting? | `ami_silent` | ignore | wait | 0.07 | 0.89 |
| D: It's Unimail? | `ami_silent` | ignore | wait | 0.05 | 0.85 |
| C: Nah? | `ami_silent` | ignore | wait | 0.07 | 0.72 |
| A: So about two o'clock? | `ami_silent` | ignore | wait | 0.07 | 0.86 |
| A: Would that be okay? | `ami_silent` | ignore | wait | 0.07 | 0.87 |
| A: Um now you can all give your presentations. | `ami_silent` | ignore | wait | 0.03 | 0.79 |
| A: I just wanted to put those in there to see if you guys had any comments on them. | `ami_silent` | ignore | wait | 0.04 | 0.82 |
| A: Uh did you all receive that email? | `ami_silent` | ignore | wait | 0.04 | 0.91 |
| A: So does anyone have any overall | `ami_silent` | ignore | wait | 0.04 | 0.91 |
| D: What are we gonna have that makes this thing better than | `ami_silent` | ignore | wait | 0.05 | 0.92 |
| D: which is, what are we gonna be targeting our market uh that identifies our product as better than because it d | `ami_silent` | ignore | wait | 0.06 | 0.86 |
| D: It's just when we eliminate that then what do we bring? | `ami_silent` | ignore | wait | 0.10 | 0.90 |
| D: What are we bringing in to take the place of this, | `ami_silent` | ignore | wait | 0.15 | 0.92 |
| A: Can you handle that black and yellow? | `ami_silent` | ignore | wait | 0.09 | 0.81 |
| D: So you have this? | `ami_silent` | ignore | wait | 0.06 | 0.79 |
| A: Mm it's enough. But uh click it on off? | `ami_silent` | ignore | wait | 0.10 | 0.80 |
| D: Now is would this be considered just a standard uh um | `ami_silent` | ignore | wait | 0.09 | 0.86 |
| A: Do we have an idea of costs of different components? | `ami_silent` | ignore | wait | 0.09 | 0.94 |
| A: Do we have any ballpark figures for that yet? No. | `ami_silent` | ignore | wait | 0.08 | 0.77 |
| D: Mm the shell? | `ami_silent` | ignore | wait | 0.04 | 0.63 |
| C: Open. | `ami_silent` | ignore | wait | 0.21 | 0.62 |
| A: View a slide show, that's what you wanna do, yeah? | `ami_silent` | ignore | wait | 0.11 | 0.65 |
| A: Just go up to view. | `ami_silent` | ignore | wait | 0.09 | 0.54 |
| A: if it i if it isn't more expensive for us to k make because as far as I understand it, it can be operated with | `ami_silent` | ignore | wait | 0.06 | 0.70 |
| A: Okay. Isn't | `ami_silent` | ignore | wait | 0.06 | 0.74 |
| D: I have maybe a silly question. | `ami_silent` | ignore | wait | 0.10 | 0.58 |
| D: I I don't understand how those two things are connected. | `ami_silent` | ignore | wait | 0.09 | 0.82 |
| D: How does how does computers and teletext h how why is one eliminating the need of the other? | `ami_silent` | ignore | wait | 0.11 | 0.94 |
| D: I don't understand that. | `ami_silent` | ignore | wait | 0.11 | 0.73 |
| B: I think if it's possible you should try to you know have a talk with management about that. | `ami_silent` | ignore | wait | 0.08 | 0.53 |
| D: So if we drop if we are gonna choose to drop teletext, again what are we adding to the product that makes it m | `ami_silent` | ignore | wait | 0.06 | 0.90 |
| A: 'Cause we really don't have anything else there, do we? | `ami_silent` | ignore | wait | 0.10 | 0.82 |
| A: Does that make sense, huh? | `ami_silent` | ignore | wait | 0.06 | 0.84 |
| D: and if I'm coming in with a with with twenty-five Euros, which is mid-market price, um then what am I going to | `ami_silent` | ignore | wait | 0.13 | 0.89 |
| D: So that's just my question, | `ami_silent` | ignore | wait | 0.12 | 0.61 |
| B: I'm just thinking you know with all these universal remotes that are out there, how many people how many peopl | `ami_silent` | ignore | wait | 0.06 | 0.86 |
| A: Is that | `ami_silent` | ignore | wait | 0.13 | 0.71 |
| B: Because I think as we as we add costs for things like uh for like if we add the voice recognition and things l | `ami_silent` | ignore | wait | 0.10 | 0.82 |
| B: and how much | `ami_silent` | ignore | wait | 0.03 | 0.55 |
| D: You know sell uh things come to my mind is uh uh something that's uh um voice-activated. | `ami_silent` | ignore | wait | 0.10 | 0.50 |
| D: Is that for over here? | `ami_silent` | ignore | wait | 0.19 | 0.77 |
| A: Is it? | `ami_silent` | ignore | wait | 0.11 | 0.76 |
| D: So some way that I can I can find my remote by clapping my hands or something | `ami_silent` | ignore | wait | 0.22 | 0.81 |
| D: 'cause when they talk about tel taking out teletext, it's like, what are we gonna put in? | `ami_silent` | ignore | wait | 0.10 | 0.80 |
| D: What makes this thing attractive? | `ami_silent` | ignore | wait | 0.13 | 0.89 |
| D: Have to do you have to do it in the box? | `ami_silent` | ignore | wait | 0.05 | 0.81 |
| A: I have a question uh for you. | `ami_silent` | ignore | wait | 0.09 | 0.71 |
| A: Does any of the um the features that Pedro's spoken about here have any implications we might not have thought | `ami_silent` | ignore | wait | 0.10 | 0.82 |
| A: In terms of making it work or the cost of that or | `ami_silent` | ignore | wait | 0.12 | 0.67 |
| D: and uh how do I go here? | `ami_silent` | ignore | wait | 0.12 | 0.86 |
| D: Is that right? | `ami_silent` | ignore | wait | 0.12 | 0.80 |
| D: Yeah, what for me is it um | `ami_silent` | ignore | wait | 0.12 | 0.81 |
| D: Um so I would like to have a product that that we can sell easily. | `ami_silent` | ignore | wait | 0.06 | 0.54 |
| B: but instead what about if we had like a power cradle? | `ami_silent` | ignore | wait | 0.06 | 0.87 |
| A: Now the the question is can we make this for less than twelve-fifty per? | `ami_silent` | ignore | wait | 0.09 | 0.89 |
| A: We we well do we necessarily have to change the end cost because uh Can we dl can we do that without uh changi | `ami_silent` | ignore | wait | 0.06 | 0.86 |
| B: and you can look into what kind of effect an increased cost is gonna have on our on our final numbers. | `ami_silent` | ignore | wait | 0.05 | 0.64 |
| D: You know, let's let's sell this wholesale for for fifty Euros, sixty Euros. | `ami_silent` | ignore | wait | 0.05 | 0.53 |
| D: Let's make this thing really exclusive, environmentally sensitive, uh high-tech design, uh ergonomics, all of  | `ami_silent` | ignore | wait | 0.05 | 0.58 |
| D: Just make this thing uh, yeah, the the the Rolls Royce of of remote controls. | `ami_silent` | ignore | wait | 0.06 | 0.71 |
| D: hey what kind of remote do you have? | `ami_silent` | ignore | wait | 0.08 | 0.85 |
| D: one one thing I don't understand is h they've they've given us this package, okay. | `ami_silent` | ignore | wait | 0.04 | 0.56 |
| D: I don't know what kind of role we have in this in the corporate ladder uh, | `ami_silent` | ignore | wait | 0.05 | 0.67 |
| D: do we follow their directives or do we make uh presentations back and and then and then discuss? | `ami_silent` | ignore | wait | 0.08 | 0.91 |
| D: because who wants just a television remote? | `ami_silent` | ignore | wait | 0.07 | 0.73 |
| A: Is twenty-five Euros a mid-market price for a remote? | `ami_silent` | ignore | wait | 0.06 | 0.89 |
| B: What about um the idea that I had with the cradle? | `ami_silent` | ignore | wait | 0.04 | 0.87 |
| B: How do you feel about that? | `ami_silent` | ignore | wait | 0.10 | 0.79 |
| B: Or how does everybody feel? | `ami_silent` | ignore | wait | 0.04 | 0.91 |
| A: Well how does everybody feel? | `ami_silent` | ignore | wait | 0.04 | 0.92 |
| A: the problem with that in my mind I just think off-hand as a as a consumer, would I wanna buy that? | `ami_silent` | ignore | wait | 0.06 | 0.79 |
| D: Are we gonna make this selling selling the cost as a high high-tech uh um environmentally sensitive whatever,  | `ami_silent` | ignore | wait | 0.04 | 0.88 |
| A: So what do we think maybe we should | `ami_silent` | ignore | wait | 0.05 | 0.89 |
| D: W a question I have in in a | `ami_silent` | ignore | wait | 0.09 | 0.60 |
| D: Can can can we have multiple designs? | `ami_silent` | ignore | wait | 0.05 | 0.91 |
| D: and so so instead of them all looking the same, people can have maybe four or five different designs they can  | `ami_silent` | ignore | wait | 0.08 | 0.68 |
| D: I don't know what that creates cost, or | `ami_silent` | ignore | wait | 0.09 | 0.64 |
| D: What ab what ab | `ami_silent` | ignore | wait | 0.05 | 0.64 |
| D: what about a a remote that's that doesn't maybe look like a remote? | `ami_silent` | ignore | wait | 0.05 | 0.90 |
| B: Or what if it looks like a pen? | `ami_silent` | ignore | wait | 0.04 | 0.77 |
| B: A pointer? | `ami_silent` | ignore | wait | 0.03 | 0.79 |
| B: un unless you guys are die-hard against the fact that um it's possible like it reduces the usability of the re | `ami_silent` | ignore | wait | 0.04 | 0.74 |
| B: As a watch? | `ami_silent` | ignore | wait | 0.28 | 0.77 |
| D: We gotta stop? | `ami_silent` | ignore | wait | 0.07 | 0.86 |
| D: Who's lost or broken their their remote. | `ami_silent` | ignore | wait | 0.03 | 0.50 |
| D: So how many remotes do they wanna buy? | `ami_silent` | ignore | wait | 0.04 | 0.88 |
| D: Can we p can we sell them a remote that can maybe guarantee they will not need to buy another one? | `ami_silent` | ignore | wait | 0.05 | 0.91 |
| D: And so with with with this kind of system or locator or something, to to think about, how have people been bee | `ami_silent` | ignore | wait | 0.08 | 0.90 |
| D: How does this happen? | `ami_silent` | ignore | wait | 0.08 | 0.93 |
| D: And and then and then design the product, maybe some component of the product that can identify this as the la | `ami_silent` | ignore | wait | 0.06 | 0.77 |
| D: So do we need to re-train Mike on how to put his mic on? | `ami_silent` | ignore | wait | 0.05 | 0.89 |
| D: Okay, can he get it all by himself this time? | `ami_silent` | ignore | wait | 0.06 | 0.82 |
| A: 'Kay, ready to go? | `ami_silent` | ignore | wait | 0.08 | 0.89 |
| D: Thirty's really young, eh? | `ami_silent` | ignore | wait | 0.08 | 0.83 |
| A: And does anyone really want to go first? | `ami_silent` | ignore | wait | 0.04 | 0.94 |
| A: You p two? | `ami_silent` | ignore | wait | 0.09 | 0.70 |
| A: What's | `ami_silent` | ignore | wait | 0.07 | 0.68 |
| C: Presented by name. | `ami_silent` | ignore | wait | 0.06 | 0.68 |
| A: Your name is name? | `ami_silent` | ignore | wait | 0.08 | 0.62 |
| D: I just love you tech guys, huh. | `ami_silent` | ignore | wait | 0.08 | 0.55 |
| C: I wanna change that. | `ami_silent` | ignore | wait | 0.08 | 0.59 |
| A: Okay so we basically have battery versus cradle here? | `ami_silent` | ignore | wait | 0.08 | 0.87 |
| A: Wood wood would ge would give us a little bit of a marketing niche, wouldn't it. | `ami_silent` | ignore | wait | 0.06 | 0.87 |
| A: 'Kay. Do you get a good grip on the rubber? | `ami_silent` | ignore | wait | 0.05 | 0.78 |
| B: where it's curved on m m multiple axes, right? | `ami_silent` | ignore | wait | 0.11 | 0.84 |
| B: oh why doesn't this scroll up? | `ami_silent` | ignore | wait | 0.09 | 0.83 |
| A: So presentation from I guess design would go best. Next. | `ami_silent` | ignore | wait | 0.06 | 0.55 |
| A: Technical functions or interface concept? | `ami_silent` | ignore | wait | 0.07 | 0.84 |
| A: But what if you actually had to press a button to make it recognize? | `ami_silent` | ignore | wait | 0.12 | 0.89 |
| A: So if you pressed it and went, up? | `ami_silent` | ignore | wait | 0.10 | 0.81 |
| B: Well then why don't you just press the up button? | `ami_silent` | ignore | wait | 0.21 | 0.70 |
| A: So we're suggesting doing a sorta scroll wheel thing for the volume? | `ami_silent` | ignore | wait | 0.06 | 0.80 |
| A: So on to Y functional requirements or trend watching? | `ami_silent` | ignore | wait | 0.10 | 0.89 |
| B: Are you talking about the picture? | `ami_silent` | ignore | wait | 0.04 | 0.72 |
| D: I'm a I'm a little bit stuck right now in that what uh w what is it that I'm gonna market? | `ami_silent` | ignore | wait | 0.13 | 0.87 |
| D: What are we gonna do to make this one special and unique? | `ami_silent` | ignore | wait | 0.19 | 0.93 |
| B: What's special and unique about a scroll? | `ami_silent` | ignore | wait | 0.06 | 0.87 |
| D: what I'm looking for as marketing is m give me something different. | `ami_silent` | ignore | wait | 0.12 | 0.83 |
| D: I give me a lower price, | `ami_silent` | ignore | wait | 0.10 | 0.80 |
| D: give me a higher price, | `ami_silent` | ignore | wait | 0.15 | 0.75 |
| D: give me some new technology, | `ami_silent` | ignore | wait | 0.11 | 0.81 |
| D: don't give me the same thing that everybody else is putting out there on the shelf it's f at the same price. | `ami_silent` | ignore | wait | 0.14 | 0.77 |
| D: I need something to market about this thing. | `ami_silent` | ignore | wait | 0.16 | 0.75 |
| D: What i if when when we have | `ami_silent` | ignore | wait | 0.12 | 0.76 |
| D: when we when we have something like the cradle or or something give that's | `ami_silent` | ignore | wait | 0.37 | 0.64 |
| D: as as a marketing standard I need something to market, to make this product unique. | `ami_silent` | ignore | wait | 0.16 | 0.79 |
| D: Um uh my personal preference is that we make some adjustment in the cost, either lower | `ami_silent` | ignore | wait | 0.06 | 0.61 |
| B: Well let's get a product then. | `ami_silent` | ignore | wait | 0.05 | 0.50 |
| D: If you if you give me if you give me a cut-out of what everybody else has then I need to I need to find a lowe | `ami_silent` | ignore | wait | 0.08 | 0.67 |
| A: So our big questions here really are cradle or not cradle? | `ami_silent` | ignore | wait | 0.07 | 0.86 |
| A: Do we go basic or do we go for features? | `ami_silent` | ignore | wait | 0.06 | 0.93 |
| A: Uh d does anyone really wanna do anything with the scroll wheel or should we ditch that off-hand first? | `ami_silent` | ignore | wait | 0.05 | 0.88 |
| B: Well my question is what would the scroll wheel do? | `ami_silent` | ignore | wait | 0.46 | 0.89 |
| B: Function-wise, what does that do that | `ami_silent` | ignore | wait | 0.26 | 0.87 |
| A: so wh what would you imagine it doing? | `ami_silent` | ignore | wait | 0.06 | 0.65 |
| D: Yeah wh wh what's the wh | `ami_silent` | ignore | wait | 0.31 | 0.66 |
| C: But would we | `ami_silent` | ignore | wait | 0.08 | 0.80 |
| B: or do you think volume would be | `ami_silent` | ignore | wait | 0.07 | 0.74 |
| A: So our big decision then is like how do we do um like | `ami_silent` | ignore | wait | 0.04 | 0.79 |
| A: What type of casing? | `ami_silent` | ignore | wait | 0.05 | 0.89 |
| A: d d do we want to do anything more basic with the uh more advanced with the user interface in terms of do we w | `ami_silent` | ignore | wait | 0.08 | 0.87 |
| A: or do we want if we're ditching the scroll wheels do we want to go L_C_D_? | `ami_silent` | ignore | wait | 0.06 | 0.89 |
| A: Do we want to give do we want to have anything else on it? | `ami_silent` | ignore | wait | 0.07 | 0.92 |
| B: Unless you can think of something interesting to do with it. | `ami_silent` | ignore | wait | 0.15 | 0.86 |
| A: the question is now I guess we need t to decide on | `ami_silent` | ignore | wait | 0.06 | 0.66 |
| A: well y you guys basically have to now go and figure out the details of this thing. | `ami_silent` | ignore | wait | 0.04 | 0.58 |
| A: So, what we need to know in terms of marketing and uh project management are are there any other questions tha | `ami_silent` | ignore | wait | 0.05 | 0.90 |
| A: What what overall things have we not decided on? | `ami_silent` | ignore | wait | 0.05 | 0.93 |
| B: There's the scroll wheel, in or out? | `ami_silent` | ignore | wait | 0.18 | 0.85 |
| B: What do you guys like in the user interface? | `ami_silent` | ignore | wait | 0.12 | 0.95 |
| A: I think maybe in terms of marketing, is that gonna make enough of a difference to justify the cost? | `ami_silent` | ignore | wait | 0.07 | 0.90 |
| D: You know the other thing I thought about was you know, do we go to something like this? | `ami_silent` | ignore | wait | 0.04 | 0.80 |
| D: Make a remote that doesn't look like a remote. | `ami_silent` | ignore | wait | 0.05 | 0.73 |
| A: and I guess th th the question th th that you're being asked right now is whether is the dock enough of a uniq | `ami_silent` | ignore | wait | 0.04 | 0.69 |
| A: or do we really need the scroll wheel as well? | `ami_silent` | ignore | wait | 0.04 | 0.88 |
| A: That's gonna n is that gonna need a better chip as well? | `ami_silent` | ignore | wait | 0.09 | 0.84 |
| A: it's not gonna need q quality, is it? It's | `ami_silent` | ignore | wait | 0.08 | 0.81 |
| B: So the scroll wheel, in or out? | `ami_silent` | ignore | wait | 0.13 | 0.86 |
| A: Or do you have to go through and you wait for it? | `ami_silent` | ignore | wait | 0.11 | 0.84 |
| A: And if we're marketing it as a high niche product, then we're gonna be selling it to people who are buying goo | `ami_silent` | ignore | wait | 0.06 | 0.50 |
| D: So ca can we can we create that kind of interface within a scroll system? | `ami_silent` | ignore | wait | 0.43 | 0.89 |
| D: You understand what I'm saying? | `ami_silent` | ignore | wait | 0.28 | 0.86 |
| B: Well, what about this what about if you can programme in your favourite channels into this scroll wheel and yo | `ami_silent` | ignore | wait | 0.09 | 0.75 |
| B: Why? | `ami_silent` | ignore | wait | 0.38 | 0.80 |
| A: How would you program it though? | `ami_silent` | ignore | wait | 0.10 | 0.91 |
| B: Oh well we also have to determine in some manner how to switch between modes, between going through your favou | `ami_silent` | ignore | wait | 0.05 | 0.56 |
| A: Would that work? | `ami_silent` | ignore | wait | 0.09 | 0.79 |
| A: Is that | `ami_silent` | ignore | wait | 0.07 | 0.74 |
| A: And if we're making back-lit buttons period, do we want that just for the mode indicator or maybe to indicate  | `ami_silent` | ignore | wait | 0.07 | 0.90 |
| B: I wanna make sure everybody's okay with that. | `ami_silent` | ignore | wait | 0.03 | 0.85 |
| B: I just wanna make sure everybody's on board with it. So | `ami_silent` | ignore | wait | 0.03 | 0.74 |
| A: So we really need to be sure as to what we can push the cost up to, | `ami_silent` | ignore | wait | 0.05 | 0.65 |
| A: But I'd say what sorta price are we looking to be able to sell something like that, | `ami_silent` | ignore | wait | 0.05 | 0.91 |
| A: and what sorta price can we make it for? | `ami_silent` | ignore | wait | 0.05 | 0.91 |
| D: I guess what I just want to me the next step is for these guys to come come in with the design proposal w with | `ami_silent` | ignore | wait | 0.04 | 0.66 |
| A: But th what's our ballpark as to what we'd be able to sell something like this for? | `ami_silent` | ignore | wait | 0.05 | 0.91 |
| B: Let's let's try and think now, how much would you pay for | `ami_silent` | ignore | wait | 0.04 | 0.85 |
| D: We have to find cost. | `ami_silent` | ignore | wait | 0.04 | 0.50 |
| B: with all these features how much would you pay | `ami_silent` | ignore | wait | 0.05 | 0.87 |
| B: if you went to the store, and you were in the market f to replace your T_V_ remote, how much would you pay for | `ami_silent` | ignore | wait | 0.07 | 0.89 |
| A: But you've gotta think who our target market is | `ami_silent` | ignore | wait | 0.07 | 0.64 |
| A: uh would I buy it? | `ami_silent` | ignore | wait | 0.09 | 0.80 |
| A: So the question is what we ca we make it for. | `ami_silent` | ignore | wait | 0.05 | 0.91 |
| C: Okay so you can market pe depending on that? | `ami_silent` | ignore | wait | 0.08 | 0.84 |
| A: although does it? | `ami_silent` | ignore | wait | 0.12 | 0.82 |
| D: Is my | `ami_silent` | ignore | wait | 0.36 | 0.70 |
| D: three twenty one is the next meeting? | `ami_silent` | ignore | wait | 0.55 | 0.87 |
| A: Okay are there any other questions with regards to what this thing's gonna do, look like, how it's gonna work  | `ami_silent` | ignore | wait | 0.04 | 0.92 |
| B: Put on your mic. | `ami_silent` | ignore | wait | 0.09 | 0.72 |
| C: So you forgot how this works again? | `ami_silent` | ignore | wait | 0.09 | 0.69 |
| A: 'kay? | `ami_silent` | ignore | wait | 0.05 | 0.61 |
| A: You guys are gonna give us a presentation of our wonder product | `ami_silent` | ignore | wait | 0.03 | 0.50 |
| C: Hmm you knocked it up? | `ami_silent` | ignore | wait | 0.09 | 0.61 |
| A: Let's try and keep this one on schedule. | `ami_silent` | ignore | wait | 0.04 | 0.74 |
| A: Your thing is in where is it? | `ami_silent` | ignore | wait | 0.08 | 0.75 |
| A: Is it in | `ami_silent` | ignore | wait | 0.04 | 0.72 |
| A: Who wants it? | `ami_silent` | ignore | wait | 0.05 | 0.92 |
| A: Zapping your favourite channels, eh? | `ami_silent` | ignore | wait | 0.09 | 0.60 |
| B: and uh what was the other button here? | `ami_silent` | ignore | wait | 0.13 | 0.87 |
| A: Is that | `ami_silent` | ignore | wait | 0.09 | 0.72 |
| A: could that be easy to for the scroll wheel to be rotated if it lands on it? | `ami_silent` | ignore | wait | 0.08 | 0.84 |
| A: I take it that this is gonna be slightly lighter in the final design as well. | `ami_silent` | ignore | wait | 0.06 | 0.53 |
| A: You have to reach a little bit don't you. | `ami_silent` | ignore | wait | 0.05 | 0.71 |
| A: And hold it so | `ami_silent` | ignore | wait | 0.08 | 0.56 |
| A: wh what's the marketing perspective? | `ami_silent` | ignore | wait | 0.12 | 0.87 |
| C: Wicked isn't it? | `ami_silent` | ignore | wait | 0.09 | 0.78 |
| A: So the the two blue are are those for the the it to charge off of in? | `ami_silent` | ignore | wait | 0.11 | 0.86 |
| A: Yeah it's the right shape isn't it? | `ami_silent` | ignore | wait | 0.09 | 0.75 |
| A: hasn't it? | `ami_silent` | ignore | wait | 0.05 | 0.76 |
| A: So is that the the final colour scheme as well or? | `ami_silent` | ignore | wait | 0.09 | 0.84 |
| A: 'Kay so are we done with the this presentation? | `ami_silent` | ignore | wait | 0.07 | 0.90 |
| D: So you're not gonna find my uh my folder up there | `ami_silent` | ignore | wait | 0.12 | 0.57 |
| A: Have you? Okay. | `ami_silent` | ignore | wait | 0.06 | 0.64 |
| A: Can I not get your get at stuff from your shared folder now? | `ami_silent` | ignore | wait | 0.19 | 0.76 |
| D: Is this one of the tests is to see how we can adapt to s changing situations in the in the meeting room? | `ami_silent` | ignore | wait | 0.21 | 0.90 |
| D: That's not how you spell method, is it? | `ami_silent` | ignore | wait | 0.08 | 0.85 |
| D: And when I speak about method I speak about the marketing of the product huh. | `ami_silent` | ignore | wait | 0.05 | 0.55 |
| D: Help me. | `ami_silent` | ignore | wait | 0.28 | 0.89 |
| D: One thing I would want to to see is uh is can we can we get a lifetime uh guarantee on this product, a normal  | `ami_silent` | ignore | wait | 0.07 | 0.87 |
| D: which means that this product, for the for the life of of the life use, if it should have a technical problem, | `ami_silent` | ignore | wait | 0.08 | 0.88 |
| A: Do you | `ami_silent` | ignore | wait | 0.09 | 0.77 |
| A: would you a argue that that we're better going for the higher cost than bringing it down into twenty f five as | `ami_silent` | ignore | wait | 0.07 | 0.77 |
| A: And we're actually quite open to be able to expand the product for a later version with those features quite s | `ami_silent` | ignore | wait | 0.06 | 0.81 |
| D: Well one of one of the thoughts that I had is can can this unit be be produced in a way that makes it upgradab | `ami_silent` | ignore | wait | 0.15 | 0.88 |
| D: You know is there a card in th can we make a card and so after | `ami_silent` | ignore | wait | 0.22 | 0.86 |
| A: where | `ami_silent` | ignore | wait | 0.07 | 0.64 |
| A: I I was wondering, you | `ami_silent` | ignore | wait | 0.08 | 0.63 |
| A: when you talked about the fifteen point eight Euros, I was wondering how you came up with that figure? | `ami_silent` | ignore | wait | 0.09 | 0.76 |
| A: Uh do you think that's fair coming from a m the manufacturing? | `ami_silent` | ignore | wait | 0.08 | 0.86 |
| A: Is that a single-curved rather than a double-curved? | `ami_silent` | ignore | wait | 0.10 | 0.77 |
| A: You think? | `ami_silent` | ignore | wait | 0.04 | 0.69 |
| A: But we save one Euro that way, yeah? | `ami_silent` | ignore | wait | 0.07 | 0.83 |
| A: Do don't speak so | `ami_silent` | ignore | wait | 0.07 | 0.59 |
| A: w do we have any | `ami_silent` | ignore | wait | 0.07 | 0.82 |
| A: we have special form don't we? | `ami_silent` | ignore | wait | 0.09 | 0.88 |
| B: Ah. What do you know. | `ami_silent` | ignore | wait | 0.08 | 0.75 |
| A: is this intended to be a button as well or just a scroll? | `ami_silent` | ignore | wait | 0.07 | 0.86 |
| A: Just a scroll? | `ami_silent` | ignore | wait | 0.05 | 0.74 |
| A: It's not one of the scrolls where, for example, with this one you could push it down to be a button? | `ami_silent` | ignore | wait | 0.05 | 0.82 |
| A: where we have a look at the criterias th that Paul the criterion criteria that Paul has has given us, and we c | `ami_silent` | ignore | wait | 0.06 | 0.80 |
| A: Anyone got any thoughts? | `ami_silent` | ignore | wait | 0.06 | 0.95 |
| B: What? | `ami_silent` | ignore | wait | 0.07 | 0.60 |
| A: How how have we done today? | `ami_silent` | ignore | wait | 0.06 | 0.92 |
| A: Any other chang uh thoughts? | `ami_silent` | ignore | wait | 0.04 | 0.94 |
| A: Okay so th th what about um room for creativity? | `ami_silent` | ignore | wait | 0.09 | 0.92 |
| A: Is it the. | `ami_silent` | ignore | wait | 0.07 | 0.75 |
| D: because we d we still have the the teletext capability in this thing right, | `ami_silent` | ignore | wait | 0.07 | 0.87 |
| A: 'Kay leadership, what do we report back to the bosses? | `ami_silent` | ignore | wait | 0.05 | 0.78 |
| A: What did we think of the meeting room, | `ami_silent` | ignore | wait | 0.06 | 0.92 |
| A: Keep it, keep it calm. | `ami_silent` | ignore | wait | 0.07 | 0.64 |
| A: What new ideas have we found? | `ami_silent` | ignore | wait | 0.08 | 0.92 |
| D: New ideas f uh for the product or for the the the the environment or | `ami_silent` | ignore | wait | 0.13 | 0.81 |
| D: what are we ta | `ami_silent` | ignore | wait | 0.11 | 0.79 |
| A: Uh for the product? | `ami_silent` | ignore | wait | 0.09 | 0.87 |
| A: And for the meeting room, Has anyone got any more | `ami_silent` | ignore | wait | 0.06 | 0.94 |
| A: Are the costs within the budget? | `ami_silent` | ignore | wait | 0.08 | 0.87 |
| A: And the costs within the budget? | `ami_silent` | ignore | wait | 0.08 | 0.82 |
| A: Is the project evaluated? | `ami_silent` | ignore | wait | 0.14 | 0.88 |
| C: Who wrote that one? | `ami_silent` | ignore | wait | 0.07 | 0.90 |
| D: So we need to close this meeting, | `ami_silent` | ignore | wait | 0.05 | 0.51 |
| D: so let's close this and come back and 'kay. | `ami_silent` | ignore | wait | 0.04 | 0.50 |
| A: Let's start with you, | `ami_silent` | ignore | wait | 0.08 | 0.72 |
| A: can you introduce yourself? | `ami_silent` | ignore | wait | 0.10 | 0.85 |
| C: First one is uh what happens inside the apparatus, | `ami_silent` | ignore | wait | 0.05 | 0.78 |
| C: second is what is uh the apparatus made of, | `ami_silent` | ignore | wait | 0.05 | 0.86 |
| C: and the third is what should it look like. | `ami_silent` | ignore | wait | 0.05 | 0.77 |
| A: What should it look like? Okay. | `ami_silent` | ignore | wait | 0.08 | 0.63 |
| A: So that's what you need to do to bring us the latest info and what people want. | `ami_silent` | ignore | wait | 0.14 | 0.71 |
| A: just take a new slide | `ami_silent` | ignore | wait | 0.08 | 0.54 |
| A: just stuff that you wanna share, just put it in the in the project folder, | `ami_silent` | ignore | wait | 0.05 | 0.68 |
| A: Just try whatever you want, | `ami_silent` | ignore | wait | 0.08 | 0.73 |
| A: and like it says, draw your favourite animal. | `ami_silent` | ignore | wait | 0.05 | 0.85 |
| A: I think the creative genius should go first. | `ami_silent` | ignore | wait | 0.08 | 0.65 |
| B: The creative genius? | `ami_silent` | ignore | wait | 0.26 | 0.73 |
| A: So, draw us your favourite animal. | `ami_silent` | ignore | wait | 0.05 | 0.53 |
| A: Draw us a technical animal. | `ami_silent` | ignore | wait | 0.04 | 0.60 |
| A: Let's go easy on it. | `ami_silent` | ignore | wait | 0.08 | 0.61 |
| A: What do you like? | `ami_silent` | ignore | wait | 0.09 | 0.84 |
| A: Pick a pick a | `ami_silent` | ignore | wait | 0.07 | 0.71 |
| A: pick a clean sheet. | `ami_silent` | ignore | wait | 0.07 | 0.77 |
| A: Oh. Take a clean sheet first. | `ami_silent` | ignore | wait | 0.07 | 0.71 |
| D: What? | `ami_silent` | ignore | wait | 0.09 | 0.77 |
| A: Just press next. | `ami_silent` | ignore | wait | 0.08 | 0.60 |
| D: You have to hold it, | `ami_silent` | ignore | wait | 0.11 | 0.54 |
| D: right? | `ami_silent` | ignore | wait | 0.13 | 0.75 |
| A: I suggest you make us the elephant in the market. The big and strong player in the market. | `ami_silent` | ignore | wait | 0.06 | 0.57 |
| C: you should press next. | `ami_silent` | ignore | wait | 0.12 | 0.66 |
| A: Press next. Yeah, | `ami_silent` | ignore | wait | 0.05 | 0.52 |
| B: You picked a hard one, didn't you? | `ami_silent` | ignore | wait | 0.08 | 0.52 |
| D: Experience with the tiger. | `ami_silent` | ignore | wait | 0.10 | 0.51 |
| D: What? They are | `ami_silent` | ignore | wait | 0.06 | 0.59 |
| C: I'm not sure how the legs should go, | `ami_silent` | ignore | wait | 0.09 | 0.65 |
| A: What does it want? | `ami_silent` | ignore | wait | 0.09 | 0.84 |
| A: Just put 'em here. Whatever. | `ami_silent` | ignore | wait | 0.13 | 0.52 |
| B: You've done this before, haven't you? | `ami_silent` | ignore | wait | 0.06 | 0.69 |
| A: Like you take just take your freedom and use a a trendy interface that you design for us. | `ami_silent` | ignore | wait | 0.12 | 0.62 |
| A: You're supposed to make i make it different from uh from what other people have, and just make it a little dis | `ami_silent` | ignore | wait | 0.09 | 0.59 |
| A: Warning. Finish meeting now. | `ami_silent` | ignore | wait | 0.11 | 0.58 |
| A: Uh put this down. | `ami_silent` | ignore | wait | 0.12 | 0.74 |
| A: Examples. | `ami_silent` | ignore | wait | 0.18 | 0.58 |
| A: So what do you guys think about | `ami_silent` | ignore | wait | 0.08 | 0.91 |
| A: I'll start with you. | `ami_silent` | ignore | wait | 0.09 | 0.54 |
| A: What are y What are your first ideas for the new product? | `ami_silent` | ignore | wait | 0.06 | 0.87 |
| B: I basically had a question. | `ami_silent` | ignore | wait | 0.14 | 0.56 |
| A: What | `ami_silent` | ignore | wait | 0.06 | 0.59 |
| B: Do uh | `ami_silent` | ignore | wait | 0.11 | 0.64 |
| B: Are we going to introduce a multi remote control? | `ami_silent` | ignore | wait | 0.09 | 0.90 |
| B: Is it just the T_V_ | `ami_silent` | ignore | wait | 0.14 | 0.85 |
| B: or do we want to in | `ami_silent` | ignore | wait | 0.11 | 0.81 |
| B: Do we want people who are disabled in any way to uh, yeah, to be able to use it as well? | `ami_silent` | ignore | wait | 0.08 | 0.93 |
| A: You have anything you wanna share quickly? | `ami_silent` | ignore | wait | 0.06 | 0.87 |
| A: where did I | `ami_silent` | ignore | wait | 0.07 | 0.61 |
| A: What do we This Quick What we're going to | `ami_silent` | ignore | wait | 0.07 | 0.65 |
| A: Just go go for that. | `ami_silent` | ignore | wait | 0.07 | 0.52 |
| A: Do you have anything you you came up with yet? About uh marketing transfer, whatever? | `ami_silent` | ignore | wait | 0.08 | 0.85 |
| D: Um about what? Marketing? | `ami_silent` | ignore | wait | 0.06 | 0.66 |
| A: I'm not sure what you what you came up with yet. You have anything to share? | `ami_silent` | ignore | wait | 0.05 | 0.76 |
| A: shall we wait? | `ami_silent` | ignore | wait | 0.11 | 0.90 |
| A: so have a seat. | `ami_silent` | ignore | wait | 0.04 | 0.68 |
| A: have a little thoughts on what your vision is and on this project, | `ami_silent` | ignore | wait | 0.05 | 0.73 |
| A: and share some thoughts, | `ami_silent` | ignore | wait | 0.04 | 0.54 |
| A: Who would like wanna go first? | `ami_silent` | ignore | wait | 0.04 | 0.95 |
| A: Yeah. So there? | `ami_silent` | ignore | wait | 0.09 | 0.73 |
| A: If I can cut in, | `ami_silent` | ignore | wait | 0.07 | 0.65 |
| A: is it people or men? | `ami_silent` | ignore | wait | 0.07 | 0.81 |
| A: just talk ahead. | `ami_silent` | ignore | wait | 0.12 | 0.55 |
| D: hmm? | `ami_silent` | ignore | wait | 0.18 | 0.60 |
| B: Which channel selection? | `ami_silent` | ignore | wait | 0.06 | 0.81 |
| A: That's like a button on your T_V_? | `ami_silent` | ignore | wait | 0.07 | 0.84 |
| D: um to to look it um wh what's on every channel uh and uh what do I want with it? | `ami_silent` | ignore | wait | 0.13 | 0.84 |
| B: Is that manageable? | `ami_silent` | ignore | wait | 0.30 | 0.87 |
| D: What? | `ami_silent` | ignore | respond | 0.80 | 0.77 |
| A: You want the you want it to be programmed, for example | `ami_silent` | ignore | wait | 0.14 | 0.52 |
| D: Yeah. | `ami_silent` | ignore | respond | 0.84 | 0.07 |
| A: or you want it to recognise your favourite channel? | `ami_silent` | ignore | wait | 0.10 | 0.72 |
| D: Yeah. | `ami_silent` | ignore | respond | 0.83 | 0.10 |
| D: Recognise | `ami_silent` | ignore | respond | 0.90 | 0.31 |
| D: Yeah, that's uh what my personal preference like. | `ami_silent` | ignore | respond | 0.84 | 0.04 |
| B: Shall I go? | `ami_silent` | ignore | wait | 0.15 | 0.85 |
| B: what does the user do, what does the th remote control do, | `ami_silent` | ignore | wait | 0.13 | 0.83 |
| B: What goes wrong at the user. | `ami_silent` | ignore | wait | 0.07 | 0.85 |
| B: Where is the remote control? | `ami_silent` | ignore | wait | 0.12 | 0.89 |
| B: where's the remote control? | `ami_silent` | ignore | wait | 0.08 | 0.91 |
| B: but maybe we could do a little uh investigation to see whether some symbols are uh need to be replaced by othe | `ami_silent` | ignore | wait | 0.09 | 0.56 |
| A: and what's possible for that budget. | `ami_silent` | ignore | wait | 0.06 | 0.50 |
| C: work a little with me. | `ami_silent` | ignore | wait | 0.09 | 0.75 |
| C: Which buttons are wanted, | `ami_silent` | ignore | wait | 0.16 | 0.86 |
| C: uh is our remote control universal | `ami_silent` | ignore | wait | 0.17 | 0.89 |
| C: or should it be programmable. | `ami_silent` | ignore | wait | 0.11 | 0.88 |
| C: Uh if it should be programmeab grammeale then we need um something like a mode that you can switch it. | `ami_silent` | ignore | wait | 0.11 | 0.61 |
| C: And uh how big is the remote control uh going to be? | `ami_silent` | ignore | wait | 0.18 | 0.91 |
| C: so uh uh that's why I also would like to say uh go a little bit easy on the designs, | `ami_silent` | ignore | wait | 0.15 | 0.77 |
| C: So keep in mind that everything that you keep uh think of, it has to b to be built. | `ami_silent` | ignore | wait | 0.11 | 0.71 |
| A: You mean integrate them all into the circuit board. | `ami_silent` | ignore | wait | 0.09 | 0.59 |
| C: um uh how to say it? | `ami_silent` | ignore | wait | 0.09 | 0.58 |
| C: so we really need to have a look, do we want that or not. | `ami_silent` | ignore | wait | 0.16 | 0.79 |
| A: That was it? | `ami_silent` | ignore | wait | 0.08 | 0.79 |
| A: back this up to the screen. | `ami_silent` | ignore | wait | 0.20 | 0.77 |
| A: Just put it somewhere or under second option or whatever. | `ami_silent` | ignore | wait | 0.07 | 0.59 |
| D: With more Where | `ami_silent` | ignore | wait | 0.07 | 0.51 |
| A: With that concept I started thinking, so why not just steal Nokia's idea | `ami_silent` | ignore | wait | 0.06 | 0.60 |
| A: I'm not sure if you came up with anything in the meantime, after making a presentation. | `ami_silent` | ignore | wait | 0.05 | 0.77 |
| A: Would you like to share? | `ami_silent` | ignore | wait | 0.03 | 0.73 |
| B: Is it manageable? Is it easy? | `ami_silent` | ignore | wait | 0.06 | 0.83 |
| D: Why? | `ami_silent` | ignore | wait | 0.06 | 0.83 |
| A: What we could do, what could be possible, is maybe not an L_C_D_ screen but with a preview, | `ami_silent` | ignore | wait | 0.06 | 0.66 |
| A: find a little compromise in that, | `ami_silent` | ignore | wait | 0.11 | 0.58 |
| A: What did I write down? | `ami_silent` | ignore | wait | 0.19 | 0.86 |
| A: just make a button on your T_V_ | `ami_silent` | ignore | wait | 0.07 | 0.71 |
| C: whe where do you wanna hit the T_ you wanna | `ami_silent` | ignore | wait | 0.30 | 0.78 |
| A: I mean where else should you put it? | `ami_silent` | ignore | wait | 0.07 | 0.83 |
| A: but how are you gonna use that if your | `ami_silent` | ignore | wait | 0.07 | 0.78 |
| A: I mean if your remote control is lost, how are you gonna press where are you gonna press the button? | `ami_silent` | ignore | wait | 0.06 | 0.82 |
| A: you mean as like a separate thing you can attach to your T_V_. | `ami_silent` | ignore | wait | 0.06 | 0.68 |
| C: then uh I'd I'd like to know now if we want the uh universal remote control or not, | `ami_silent` | ignore | wait | 0.13 | 0.89 |
| C: because that's uh determines everything I'm gonna do. | `ami_silent` | ignore | wait | 0.08 | 0.59 |
| D: right? | `ami_silent` | ignore | wait | 0.06 | 0.73 |
| A: What else do we have? | `ami_silent` | ignore | wait | 0.07 | 0.92 |
| A: you should you should look into the in into the materials that are real durable. | `ami_silent` | ignore | wait | 0.05 | 0.70 |
| A: For example? | `ami_silent` | ignore | wait | 0.06 | 0.80 |
| B: But should the exchangeable covers include the buttons themselves | `ami_silent` | ignore | wait | 0.10 | 0.88 |
| B: or just the | `ami_silent` | ignore | wait | 0.07 | 0.73 |
| C: Know what I mean? | `ami_silent` | ignore | wait | 0.29 | 0.76 |
| A: you have to come up with a components concept, | `ami_silent` | ignore | wait | 0.06 | 0.79 |
| A: you should do some trend-watching, | `ami_silent` | ignore | wait | 0.06 | 0.73 |
| B: Is it techni technically possible to uh send a signal to a television and then pops up a menu, | `ami_silent` | ignore | wait | 0.12 | 0.90 |
| B: so we're going to work with that? | `ami_silent` | ignore | wait | 0.12 | 0.80 |
| B: isn't it? | `ami_silent` | ignore | wait | 0.09 | 0.81 |
| A: A double-sided remote control? | `ami_silent` | ignore | wait | 0.08 | 0.76 |
| A: if you can put some research into that, if it's possible. | `ami_silent` | ignore | wait | 0.14 | 0.82 |
| A: I mean what do you want, | `ami_silent` | ignore | wait | 0.07 | 0.85 |
| A: do you want, but | `ami_silent` | ignore | wait | 0.05 | 0.76 |
| A: Let's see that you what would be handy. | `ami_silent` | ignore | wait | 0.07 | 0.75 |
| A: just take it. | `ami_silent` | ignore | wait | 0.07 | 0.61 |
| B: the volume, do we want that horizontal or vertical? | `ami_silent` | ignore | wait | 0.07 | 0.88 |
| A: Do you take triangles | `ami_silent` | ignore | wait | 0.07 | 0.83 |
| C: Perhaps we should also make uh something like a flash on it, if you if it's lost, for people that are deaf. | `ami_silent` | ignore | wait | 0.08 | 0.77 |
| C: deaf people? | `ami_silent` | ignore | wait | 0.07 | 0.83 |
| B: uh the power button somewhere over here? | `ami_silent` | ignore | wait | 0.11 | 0.90 |
| B: What would you like to? | `ami_silent` | ignore | wait | 0.11 | 0.82 |
| A: I thought maybe we should move the buttons down | `ami_silent` | ignore | wait | 0.07 | 0.63 |
| B: mute button. Is that somewhere here? | `ami_silent` | ignore | wait | 0.18 | 0.90 |
| A: Do we hardly | `ami_silent` | ignore | wait | 0.09 | 0.77 |
| B: Is that used often? | `ami_silent` | ignore | wait | 0.30 | 0.87 |
| D: sorry? | `ami_silent` | ignore | wait | 0.06 | 0.80 |
| B: The mute button? Do people use that often? | `ami_silent` | ignore | wait | 0.31 | 0.91 |
| A: you could put it somewhere here. | `ami_silent` | ignore | wait | 0.07 | 0.63 |
| A: Can I have that? | `ami_silent` | ignore | wait | 0.14 | 0.81 |
| A: Take this out and here see | `ami_silent` | ignore | wait | 0.10 | 0.53 |
| A: Uh are we gonna take triangles anyway? | `ami_silent` | ignore | wait | 0.11 | 0.88 |
| B: aren't they? | `ami_silent` | ignore | wait | 0.14 | 0.78 |
| D: Wha | `ami_silent` | ignore | wait | 0.07 | 0.56 |
| A: should we chan | `ami_silent` | ignore | wait | 0.09 | 0.84 |
| C: Shall we uh also look if it's possible to make a rechargeable remote? | `ami_silent` | ignore | wait | 0.13 | 0.92 |
| C: That you don't have to buy new batteries if every | `ami_silent` | ignore | wait | 0.08 | 0.57 |
| A: Maybe we should what | `ami_silent` | ignore | wait | 0.07 | 0.66 |
| B: But isn't that expensive in the entire package? | `ami_silent` | ignore | wait | 0.41 | 0.85 |
| A: but just take a look at it, | `ami_silent` | ignore | wait | 0.07 | 0.76 |
| C: but I'm not sure how that uh is possible with the costs, that you can put in normal batteries, rechargeable, | `ami_silent` | ignore | wait | 0.13 | 0.61 |
| C: Know what I mean? | `ami_silent` | ignore | wait | 0.22 | 0.83 |
| A: A what? | `ami_silent` | ignore | wait | 0.08 | 0.77 |
| D: But Which | `ami_silent` | ignore | wait | 0.17 | 0.79 |
| B: But again, isn't that too expensive? | `ami_silent` | ignore | wait | 0.14 | 0.85 |
| B: And do people actually want that? To pay extra they want to pay for rechargeable? | `ami_silent` | ignore | wait | 0.07 | 0.89 |
| A: Do they want | `ami_silent` | ignore | wait | 0.07 | 0.82 |
| A: but they want a rechargeable one? | `ami_silent` | ignore | wait | 0.08 | 0.86 |
| A: you should find out if it's if rechargeable is important. | `ami_silent` | ignore | wait | 0.06 | 0.79 |
| B: Can can we save this or | `ami_silent` | ignore | wait | 0.14 | 0.90 |
| A: or maybe you can find out i what people are willing to pay. | `ami_silent` | ignore | wait | 0.08 | 0.73 |
| A: but just try to find out what they're willing to pay for it, | `ami_silent` | ignore | wait | 0.04 | 0.79 |
| C: I would like to make a decision. What it costs and what kind of materials that we can uh choose what we want i | `ami_silent` | ignore | wait | 0.05 | 0.80 |
| A: if you have some financial information that that'd be nice, | `ami_silent` | ignore | wait | 0.05 | 0.84 |
| B: Could you post some other essentials of what people want, | `ami_silent` | ignore | wait | 0.21 | 0.87 |
| B: so that I can work with some buttons, where to put it | `ami_silent` | ignore | wait | 0.14 | 0.79 |
| B: You seem to have information on that, | `ami_silent` | ignore | wait | 0.19 | 0.72 |
| B: I'd like to uh see some of it. | `ami_silent` | ignore | wait | 0.12 | 0.79 |
| C: Was it not possible to uh send emails around the office? | `ami_silent` | ignore | wait | 0.11 | 0.87 |
| A: they include the new one. Or just for you. | `ami_silent` | ignore | wait | 0.09 | 0.68 |
| B: where would we | `ami_silent` | ignore | wait | 0.13 | 0.83 |
| D: maybe you ca you can look at uh that | `ami_silent` | ignore | wait | 0.13 | 0.76 |
| B: Where would we want the uh teletext button? | `ami_silent` | ignore | wait | 0.10 | 0.89 |
| B: Do we put it somewhere over here? | `ami_silent` | ignore | wait | 0.06 | 0.90 |
| A: tick the new one. | `ami_silent` | ignore | wait | 0.07 | 0.70 |
| A: let's increase it a little | `ami_silent` | ignore | wait | 0.08 | 0.66 |
| B: Or maybe this is something for the next meeting, | `ami_silent` | ignore | wait | 0.05 | 0.51 |
| A: draw us up some some designs of of possible | `ami_silent` | ignore | wait | 0.08 | 0.58 |
| A: Just play a little with this, | `ami_silent` | ignore | wait | 0.05 | 0.68 |
| A: shift a little up or down | `ami_silent` | ignore | wait | 0.08 | 0.65 |
| C: What uh what did you wanna say? | `ami_silent` | ignore | wait | 0.11 | 0.78 |
| A: Or just po post your designs from time to time on the product share. | `ami_silent` | ignore | wait | 0.04 | 0.68 |
| A: what | `ami_silent` | ignore | wait | 0.08 | 0.74 |
| A: I'm not sure who present that again, | `ami_silent` | ignore | wait | 0.09 | 0.80 |
| C: is it? | `ami_silent` | ignore | wait | 0.06 | 0.79 |
| C: Uh isn't there a possibility to do research on that, so we know that for sure? | `ami_silent` | ignore | wait | 0.16 | 0.92 |
| A: Under forty. Yeah? | `ami_silent` | ignore | wait | 0.04 | 0.76 |
| C: Did they really said it like that? Those two things. | `ami_silent` | ignore | wait | 0.10 | 0.72 |
| C: Do they realise how much that costs? | `ami_silent` | ignore | wait | 0.07 | 0.80 |
| A: Uh shall we? | `ami_silent` | ignore | wait | 0.09 | 0.84 |
| A: Would you pay for uh speech recognition in a remote control. | `ami_silent` | ignore | wait | 0.14 | 0.89 |
| A: Yeah, just look at the possibilities then, | `ami_silent` | ignore | wait | 0.08 | 0.66 |
| D: How much it will cost | `ami_silent` | ignore | wait | 0.12 | 0.89 |
| A: We should see if what it costs, if it's possible. | `ami_silent` | ignore | wait | 0.06 | 0.63 |
| C: huh? | `ami_silent` | ignore | wait | 0.06 | 0.58 |
| A: Sorry? | `ami_silent` | ignore | wait | 0.08 | 0.72 |
| A: Yeah? | `ami_silent` | ignore | wait | 0.13 | 0.54 |
| B: what kind of | `ami_silent` | ignore | wait | 0.11 | 0.81 |
| A: Could you give me the pen back? | `ami_silent` | ignore | wait | 0.06 | 0.80 |
| A: No? | `ami_silent` | ignore | wait | 0.08 | 0.81 |
| A: How can you use an L_C_D_ screen? | `ami_silent` | ignore | wait | 0.08 | 0.86 |
| A: but why | `ami_silent` | ignore | wait | 0.10 | 0.82 |
| D: you must use the maximum of it. | `ami_silent` | ignore | wait | 0.12 | 0.51 |
| A: if it's possible wi if it's not too expensive, we should include it, | `ami_silent` | ignore | wait | 0.06 | 0.55 |
| B: can I | `ami_silent` | ignore | wait | 0.07 | 0.77 |
| B: Do we put the volume control and the channel control here, | `ami_silent` | ignore | wait | 0.06 | 0.92 |
| B: or do we put it on he | `ami_silent` | ignore | wait | 0.05 | 0.87 |
| B: Would we like to press it in the middle? | `ami_silent` | ignore | wait | 0.06 | 0.91 |
| A: Or maybe we should m we could uh draw draw something a bit that has it on on on the bottom. | `ami_silent` | ignore | wait | 0.06 | 0.59 |
| D: Finish meeting now. | `ami_silent` | ignore | wait | 0.11 | 0.75 |
| A: Finish meeting now. | `ami_silent` | ignore | wait | 0.12 | 0.53 |
| B: would we like this | `ami_silent` | ignore | wait | 0.14 | 0.88 |
| B: or would we like the | `ami_silent` | ignore | wait | 0.09 | 0.82 |
| A: We either we have to decide what what people want. | `ami_silent` | ignore | wait | 0.07 | 0.50 |
| D: And uh what about speech recognition uh | `ami_silent` | ignore | wait | 0.10 | 0.90 |
| A: Just to do research into both, w what it costs and what it takes for space. | `ami_silent` | ignore | wait | 0.09 | 0.53 |
| A: But let's cut the meeting for now yes. | `ami_silent` | ignore | wait | 0.05 | 0.84 |
| C: uh let's give this uh a name, and not like some vague serial number that no one understands, like with cars. | `ami_silent` | ignore | wait | 0.05 | 0.79 |
| C: Shall we all try uh to think about a name? | `ami_silent` | ignore | wait | 0.04 | 0.94 |
| A: Yeah, let's think of a name, okay. | `ami_silent` | ignore | wait | 0.07 | 0.61 |
| B: go and finish up | `ami_silent` | ignore | wait | 0.05 | 0.55 |
| C: Do we uh save the? | `ami_silent` | ignore | wait | 0.06 | 0.85 |
| C: Did you manage? | `ami_silent` | ignore | wait | 0.12 | 0.80 |
| A: are you d | `ami_silent` | ignore | wait | 0.10 | 0.75 |
| A: what were j you guys discussing? | `ami_silent` | ignore | wait | 0.13 | 0.87 |
| C: just uh ask if if he could manage. | `ami_silent` | ignore | wait | 0.17 | 0.57 |
| A: Did you find anything new? | `ami_silent` | ignore | wait | 0.10 | 0.82 |
| A: Come on.. | `ami_silent` | ignore | wait | 0.09 | 0.56 |
| C: everything alright. | `ami_silent` | ignore | wait | 0.14 | 0.74 |
| C: Did you manage? | `ami_silent` | ignore | wait | 0.06 | 0.72 |
| A: What's uh here. | `ami_silent` | ignore | wait | 0.09 | 0.81 |
| C: Do you have a lot of new information? | `ami_silent` | ignore | wait | 0.13 | 0.85 |
| B: Hmm? | `ami_silent` | ignore | wait | 0.09 | 0.61 |
| C: Do you have a lot of new information? | `ami_silent` | ignore | wait | 0.14 | 0.85 |
| B: You need to start it up first? | `ami_silent` | ignore | wait | 0.20 | 0.84 |
| A: go again. | `ami_silent` | ignore | wait | 0.10 | 0.67 |
| A: Again you get your three presentate to see what you came up with. | `ami_silent` | ignore | wait | 0.04 | 0.71 |
| B: what t | `ami_silent` | ignore | wait | 0.07 | 0.60 |
| A: how about you go first. | `ami_silent` | ignore | wait | 0.06 | 0.76 |
| C: I suggest that we uh decide on that one uh immediately. | `ami_silent` | ignore | wait | 0.06 | 0.69 |
| A: Does it provide enough energy? | `ami_silent` | ignore | wait | 0.12 | 0.86 |
| A: Also if if we were choose the the L_C_D_ option, would it give enough energy | `ami_silent` | ignore | wait | 0.13 | 0.87 |
| B: Is that enough? | `ami_silent` | ignore | wait | 0.11 | 0.85 |
| B: And what does the hand dynamo | `ami_silent` | ignore | wait | 0.23 | 0.85 |
| A: why shouldn't we take a basic battery? | `ami_silent` | ignore | wait | 0.08 | 0.90 |
| C: Only basic battery? | `ami_silent` | ignore | wait | 0.06 | 0.84 |
| A: Why not? | `ami_silent` | ignore | wait | 0.06 | 0.87 |
| A: So why sh mm I think better. | `ami_silent` | ignore | wait | 0.09 | 0.62 |
| C: Huh? | `ami_silent` | ignore | wait | 0.09 | 0.59 |
| C: Okay? | `ami_silent` | ignore | wait | 0.07 | 0.65 |
| B: Curves being? | `ami_silent` | ignore | wait | 0.05 | 0.85 |
| A: But what were the implications if you if put more curves it it's gets more expensive. | `ami_silent` | ignore | wait | 0.06 | 0.84 |
| A: Continue. | `ami_silent` | ignore | wait | 0.10 | 0.72 |
| B: will rubber actually protect the remote control itself? | `ami_silent` | ignore | wait | 0.05 | 0.90 |
| D: Are are we focussi focussing on on the | `ami_silent` | ignore | wait | 0.08 | 0.87 |
| A: let's just rule out wood for now | `ami_silent` | ignore | wait | 0.05 | 0.57 |
| D: but are we focussing on the uh younger people or the elder people? | `ami_silent` | ignore | wait | 0.12 | 0.90 |
| C: but I need to know after this meeting. | `ami_silent` | ignore | wait | 0.09 | 0.54 |
| C: What is this? | `ami_silent` | ignore | wait | 0.19 | 0.86 |
| C: Which one of those are we gonna use? | `ami_silent` | ignore | wait | 0.16 | 0.90 |
| A: I'm still deciding on what what what could you use it for. | `ami_silent` | ignore | wait | 0.09 | 0.81 |
| C: Huh? | `ami_silent` | ignore | wait | 0.19 | 0.53 |
| B: is it really necessary | `ami_silent` | ignore | wait | 0.14 | 0.84 |
| C: We can do that. Think. | `ami_silent` | ignore | wait | 0.09 | 0.51 |
| A: But why do we need it? | `ami_silent` | ignore | wait | 0.10 | 0.90 |
| B: but why would we use it? | `ami_silent` | ignore | wait | 0.26 | 0.89 |
| A: If we don't need it, why put it in your why put it in your in your if it's if it's not something people are lo | `ami_silent` | ignore | wait | 0.11 | 0.81 |
| A: Are they? | `ami_silent` | ignore | wait | 0.05 | 0.80 |
| C: Uh L_C_D_ screen? | `ami_silent` | ignore | wait | 0.11 | 0.86 |
| C: Is that s | `ami_silent` | ignore | wait | 0.06 | 0.76 |
| A: What you what | `ami_silent` | ignore | wait | 0.08 | 0.73 |
| A: what'd you get on the L_C_D_ screen? | `ami_silent` | ignore | wait | 0.06 | 0.77 |
| A: Is it expensive? | `ami_silent` | ignore | wait | 0.06 | 0.84 |
| A: Does it | `ami_silent` | ignore | wait | 0.06 | 0.80 |
| A: And how much more expensive is that? | `ami_silent` | ignore | wait | 0.13 | 0.80 |
| C: Are we gonna do that or not? | `ami_silent` | ignore | wait | 0.09 | 0.89 |
| A: Once again I was would ask you if it's expensive, | `ami_silent` | ignore | wait | 0.07 | 0.81 |
| A: what d what was exact what you got on the on the new component? | `ami_silent` | ignore | wait | 0.08 | 0.75 |
| A: So why why | `ami_silent` | ignore | wait | 0.05 | 0.68 |
| A: if it's small and we can imp why shouldn't we? | `ami_silent` | ignore | wait | 0.05 | 0.78 |
| C: how did you | `ami_silent` | ignore | wait | 0.32 | 0.81 |
| A: And there's um get your mar marketing report? | `ami_silent` | ignore | wait | 0.11 | 0.79 |
| A: What was uh the last number | `ami_silent` | ignore | wait | 0.13 | 0.85 |
| A: of how many people were interested in voice recognition? | `ami_silent` | ignore | wait | 0.12 | 0.84 |
| A: If it's small, if it's fits, if if people like it, why not? | `ami_silent` | ignore | wait | 0.07 | 0.52 |
| C: But don't we have any w uh information about scroll-wheel? Scroll-wheel. If people would like that. | `ami_silent` | ignore | wait | 0.11 | 0.89 |
| A: Were were you | `ami_silent` | ignore | wait | 0.07 | 0.72 |
| A: we're finished? | `ami_silent` | ignore | wait | 0.08 | 0.80 |
| B: right? | `ami_silent` | ignore | wait | 0.07 | 0.69 |
| A: did you have all the materials? | `ami_silent` | ignore | wait | 0.09 | 0.79 |
| A: Or everything that you desc | `ami_silent` | ignore | wait | 0.06 | 0.53 |
| A: just just go for design for now. | `ami_silent` | ignore | wait | 0.05 | 0.63 |
| A: Just m have a seat for a second. Uh | `ami_silent` | ignore | wait | 0.05 | 0.63 |
| A: Why is it s why is it squared? | `ami_silent` | ignore | wait | 0.08 | 0.85 |
| B: Why is it square? | `ami_silent` | ignore | wait | 0.18 | 0.80 |
| A: Why did you pick square? | `ami_silent` | ignore | wait | 0.04 | 0.67 |
| A: Or uh not square, but why is it yeah, sharp corners. | `ami_silent` | ignore | wait | 0.05 | 0.76 |
| D: Where? | `ami_silent` | ignore | wait | 0.06 | 0.85 |
| D: Wher | `ami_silent` | ignore | wait | 0.07 | 0.80 |
| A: So which actually making a whole different product instead of two different models. | `ami_silent` | ignore | wait | 0.05 | 0.50 |
| A: or for example, why did you pick the mm the numbers uh all the way below, and the and the channels and volume  | `ami_silent` | ignore | wait | 0.05 | 0.74 |
| D: Um where is that? Where is th | `ami_silent` | ignore | wait | 0.10 | 0.88 |
| A: you should send it to the f to the folder first. | `ami_silent` | ignore | wait | 0.07 | 0.61 |
| D: where is your | `ami_silent` | ignore | wait | 0.14 | 0.75 |
| A: But maybe just th make uh the top a little round it off on the sides. | `ami_silent` | ignore | wait | 0.06 | 0.67 |
| D: Two? | `ami_silent` | ignore | wait | 0.06 | 0.75 |
| C: and that disables what was it again? | `ami_silent` | ignore | wait | 0.08 | 0.87 |
| D: Yeah? | `ami_silent` | ignore | wait | 0.05 | 0.56 |
| B: right? | `ami_silent` | ignore | wait | 0.07 | 0.83 |
| A: Just doodle something on the board on the left. | `ami_silent` | ignore | wait | 0.07 | 0.81 |
| A: let's see what you're doing. | `ami_silent` | ignore | wait | 0.06 | 0.71 |
| B: But isn't the f the fruit like a cover thing, | `ami_silent` | ignore | wait | 0.07 | 0.81 |
| A: we decided on what | `ami_silent` | ignore | wait | 0.06 | 0.74 |
| A: what did you guys wanna know again | `ami_silent` | ignore | wait | 0.06 | 0.90 |
| B: Did you present e everything you wanted to? | `ami_silent` | ignore | wait | 0.33 | 0.79 |
| A: Wouldn't the b the design we talked about. | `ami_silent` | ignore | wait | 0.09 | 0.81 |
| A: Uh user interface, type. | `ami_silent` | ignore | wait | 0.08 | 0.54 |
| A: apparently you guys, you should work together on the final design, both on internal and external design. | `ami_silent` | ignore | wait | 0.07 | 0.64 |
| A: you should you should probably find out how the product will fall into the market, how uh what's gonna happen  | `ami_silent` | ignore | wait | 0.06 | 0.80 |
| A: Wanna spend some more | `ami_silent` | ignore | wait | 0.07 | 0.81 |
| B: Are we all in agreement about the, well, the primary structure of the of my design? Except for the edges. Like | `ami_silent` | ignore | wait | 0.08 | 0.89 |
| A: where the pen go? | `ami_silent` | ignore | wait | 0.07 | 0.86 |
| A: open your thing again. | `ami_silent` | ignore | wait | 0.11 | 0.74 |
| A: Let's see what if you can come up with anything new. | `ami_silent` | ignore | wait | 0.10 | 0.76 |
| A: So what would give us your ne your design would be | `ami_silent` | ignore | wait | 0.13 | 0.81 |
| A: right? | `ami_silent` | ignore | wait | 0.12 | 0.78 |
| A: Is it is it the lights for for finding the finding remote | `ami_silent` | ignore | wait | 0.09 | 0.84 |
| A: or lights that it that | `ami_silent` | ignore | wait | 0.07 | 0.63 |
| D: And speech w recognition. Are we | `ami_silent` | ignore | wait | 0.09 | 0.80 |
| B: where did I imagine. | `ami_silent` | ignore | wait | 0.08 | 0.67 |
| A: And just make it red now. | `ami_silent` | ignore | wait | 0.10 | 0.71 |
| A: What do we have here? | `ami_silent` | ignore | wait | 0.10 | 0.88 |
| A: um are we gonna use square buttons or round ones actually? | `ami_silent` | ignore | wait | 0.10 | 0.91 |
| A: Are these for any extra controls? | `ami_silent` | ignore | wait | 0.12 | 0.88 |
| B: And these two buttons are or not necessary | `ami_silent` | ignore | wait | 0.13 | 0.76 |
| A: If we go for for round buttons in general, do we want to the menu key in the middle to be round? For example, | `ami_silent` | ignore | wait | 0.06 | 0.87 |
| A: do you want for example a round button in the middle or square one? | `ami_silent` | ignore | wait | 0.09 | 0.87 |
| B: Does everybody agree on that? | `ami_silent` | ignore | wait | 0.08 | 0.93 |
| B: You prefer a round? | `ami_silent` | ignore | wait | 0.04 | 0.56 |
| A: And you could include a button here for the mute, I suppose. For something else, | `ami_silent` | ignore | wait | 0.11 | 0.53 |
| A: I think it it would be nice to put the logo here, for example, if you have some buttons here. | `ami_silent` | ignore | wait | 0.07 | 0.60 |
| D: And what about | `ami_silent` | ignore | wait | 0.09 | 0.78 |
| D: What about a button for your uh favourite channel? | `ami_silent` | ignore | wait | 0.06 | 0.86 |
| A: But you think here or here? | `ami_silent` | ignore | wait | 0.06 | 0.77 |
| B: So Is your | `ami_silent` | ignore | wait | 0.11 | 0.71 |
| A: What are these for? | `ami_silent` | ignore | wait | 0.09 | 0.88 |
| A: What? | `ami_silent` | ignore | wait | 0.08 | 0.83 |
| D: What? | `ami_silent` | ignore | wait | 0.06 | 0.69 |
| A: You're accustomed to eleven? | `ami_silent` | ignore | wait | 0.06 | 0.66 |
| B: we still need an okay button. | `ami_silent` | ignore | wait | 0.09 | 0.68 |
| A: I mean why wouldn't you include a | `ami_silent` | ignore | wait | 0.07 | 0.82 |
| A: So why not give it a function. | `ami_silent` | ignore | wait | 0.08 | 0.85 |
| A: Let's say I mean could be anything. | `ami_silent` | ignore | wait | 0.06 | 0.59 |
| B: you could also shift the two buttons to be nicely aligned. | `ami_silent` | ignore | wait | 0.08 | 0.76 |
| A: But you want zero to be mis-aligned with the rest. | `ami_silent` | ignore | wait | 0.05 | 0.55 |
| A: what are we missing? | `ami_silent` | ignore | wait | 0.10 | 0.91 |
| A: Want this straight or what? | `ami_silent` | ignore | wait | 0.06 | 0.80 |
| A: Do we want something interesting with it | `ami_silent` | ignore | wait | 0.07 | 0.91 |
| A: Would give us a light here. | `ami_silent` | ignore | wait | 0.11 | 0.70 |
| A: You want it curved or what? | `ami_silent` | ignore | wait | 0.10 | 0.85 |
| A: Maybe you want | `ami_silent` | ignore | wait | 0.10 | 0.77 |
| A: Should like this? | `ami_silent` | ignore | wait | 0.10 | 0.82 |
| D: Why? | `ami_silent` | ignore | wait | 0.08 | 0.86 |
| B: Hmm? | `ami_silent` | ignore | wait | 0.12 | 0.64 |
| A: you want to a little more like this? | `ami_silent` | ignore | wait | 0.07 | 0.81 |
| A: Stop the curve here | `ami_silent` | ignore | wait | 0.11 | 0.77 |
| A: or continue it | `ami_silent` | ignore | wait | 0.06 | 0.68 |
| B: Won't that be a problem with the L_C_D_ screen? | `ami_silent` | ignore | wait | 0.07 | 0.88 |
| A: Um, any other com what | `ami_silent` | ignore | wait | 0.07 | 0.82 |
| A: what are we missing here? | `ami_silent` | ignore | wait | 0.08 | 0.92 |
| A: where do we want the microphone, for example, to be? On the side or on the or, for example, on top? Like here. | `ami_silent` | ignore | wait | 0.09 | 0.91 |
| D: Top? | `ami_silent` | ignore | wait | 0.25 | 0.72 |
| A: Why uh | `ami_silent` | ignore | wait | 0.10 | 0.73 |
| C: but s I don't know what they exactly mean by a sample sensor. | `ami_silent` | ignore | wait | 0.10 | 0.62 |
| C: Could it talk back? Like uh g uh give confirmation or something. | `ami_silent` | ignore | wait | 0.25 | 0.90 |
| B: but do you actually need the remote talking back? | `ami_silent` | ignore | wait | 0.11 | 0.82 |
| B: Which is. | `ami_silent` | ignore | wait | 0.10 | 0.63 |
| A: how do you draw that again? | `ami_silent` | ignore | wait | 0.10 | 0.85 |
| B: So what's basically edi the editi idea, sorry, now? | `ami_silent` | ignore | wait | 0.07 | 0.75 |
| A: everybody satisfied with the with the current design we have? | `ami_silent` | ignore | wait | 0.04 | 0.94 |
| D: Why? | `ami_silent` | ignore | wait | 0.06 | 0.82 |
| A: So are we gonna | `ami_silent` | ignore | wait | 0.06 | 0.79 |
| A: base colour is black? | `ami_silent` | ignore | wait | 0.07 | 0.91 |
| A: don't don't stick yourself on the covers right now. | `ami_silent` | ignore | wait | 0.05 | 0.60 |
| A: But don't stick yourself on the cover | `ami_silent` | ignore | wait | 0.04 | 0.66 |
| A: let's see if if we can do the LED onto it. | `ami_silent` | ignore | wait | 0.07 | 0.54 |
| A: You doodle a doodle us a nice nice design for for the next meeting, | `ami_silent` | ignore | wait | 0.08 | 0.81 |
| B: where would you like to put it? | `ami_silent` | ignore | wait | 0.07 | 0.77 |
| A: if it if it has no function, why even put it there? | `ami_silent` | ignore | wait | 0.05 | 0.86 |
| C: Let's vote on it. | `ami_silent` | ignore | wait | 0.05 | 0.74 |
| C: What do you want? | `ami_silent` | ignore | wait | 0.08 | 0.79 |
| C: or out? | `ami_silent` | ignore | wait | 0.08 | 0.77 |
| B: Do you have all your answers? | `ami_silent` | ignore | wait | 0.19 | 0.78 |
| C: I have one question. | `ami_silent` | ignore | wait | 0.06 | 0.56 |
| C: I only have one question with the material, | `ami_silent` | ignore | wait | 0.32 | 0.67 |
| C: but can we make yellow rubber? | `ami_silent` | ignore | wait | 0.11 | 0.89 |
| D: we don't uh use our reco uh we uh removable cover? | `ami_silent` | ignore | wait | 0.11 | 0.83 |
| D: huh? | `ami_silent` | ignore | wait | 0.11 | 0.59 |
| A: Can I close this? | `ami_silent` | ignore | wait | 0.21 | 0.89 |
| B: do we? | `ami_silent` | ignore | wait | 0.07 | 0.85 |
| A: Could open that anyway, think. | `ami_silent` | ignore | wait | 0.10 | 0.65 |
| A: you could could present that. | `ami_silent` | ignore | wait | 0.06 | 0.67 |
| A: you just go ahead and present | `ami_silent` | ignore | wait | 0.06 | 0.60 |
| A: What? | `ami_silent` | ignore | wait | 0.13 | 0.76 |
| D: Hmm? | `ami_silent` | ignore | wait | 0.06 | 0.71 |
| A: hasn't changed that much, huh? | `ami_silent` | ignore | wait | 0.05 | 0.81 |
| B: If you have anything to add, please interrupt me. | `ami_silent` | ignore | wait | 0.15 | 0.89 |
| A: So which you see the | `ami_silent` | ignore | wait | 0.08 | 0.72 |
| A: What do we scrap. | `ami_silent` | ignore | wait | 0.11 | 0.91 |
| A: You make it d orange or whatever you want. | `ami_silent` | ignore | wait | 0.06 | 0.50 |
| B: So can't we just basically extend it to thirteen? | `ami_silent` | ignore | wait | 0.15 | 0.77 |
| D: What | `ami_silent` | ignore | wait | 0.07 | 0.81 |
| A: Just keep you just make new covers for the for it, | `ami_silent` | ignore | wait | 0.06 | 0.60 |
| A: Could | `ami_silent` | ignore | wait | 0.06 | 0.58 |
| A: Is that an option? | `ami_silent` | ignore | wait | 0.08 | 0.88 |
| A: For you? | `ami_silent` | ignore | wait | 0.07 | 0.76 |
| C: Can we then not also uh change the material? | `ami_silent` | ignore | wait | 0.55 | 0.88 |
| C: But what do you then suggest we'd lose? | `ami_silent` | ignore | wait | 0.67 | 0.78 |
| C: and that's enough? | `ami_silent` | ignore | wait | 0.67 | 0.79 |
| D: so why why uh do we have to keep us uh uh um on the twelve and a half? | `ami_silent` | ignore | wait | 0.07 | 0.86 |
| C: Perhaps we should make clear to our customer that we had to do this to stay under the cost. | `ami_silent` | ignore | wait | 0.04 | 0.62 |
| A: Is it worth is it is it | `ami_silent` | ignore | wait | 0.08 | 0.81 |
| A: does it mean anything to the customer? | `ami_silent` | ignore | wait | 0.09 | 0.89 |
| B: So which curve is that | `ami_silent` | ignore | wait | 0.07 | 0.81 |
| C: Hmm? | `ami_silent` | ignore | wait | 0.06 | 0.65 |
| A: we could just discuss how the project went. | `ami_silent` | ignore | wait | 0.06 | 0.63 |
| D: let's eval evaluate uh the product of us, our design. | `ami_silent` | ignore | wait | 0.07 | 0.76 |
| A: Just create our own option. | `ami_silent` | ignore | wait | 0.08 | 0.66 |
| D: Anyone? | `ami_silent` | ignore | wait | 0.10 | 0.93 |
| A: Maybe you can hear it. | `ami_silent` | ignore | wait | 0.08 | 0.53 |
| D: How is that? Uh w we had we don't have an uh manual, | `ami_silent` | ignore | wait | 0.09 | 0.77 |
| A: So just make that a two. | `ami_silent` | ignore | wait | 0.07 | 0.55 |
| D: But it tells you or not? | `ami_silent` | ignore | wait | 0.16 | 0.82 |
| D: But wha w | `ami_silent` | ignore | wait | 0.31 | 0.75 |
| D: What are we uh displaying on the L_C_D_ screen? | `ami_silent` | ignore | wait | 0.23 | 0.91 |
| D: What uh? | `ami_silent` | ignore | wait | 0.08 | 0.76 |
| A: I mean in the L_C_D_ screen, the small screen. What does it display? | `ami_silent` | ignore | wait | 0.08 | 0.87 |
| D: And for a channel selection, uh or that's not | `ami_silent` | ignore | wait | 0.11 | 0.69 |
| D: it must be clear then what what what for we use it. | `ami_silent` | ignore | wait | 0.06 | 0.57 |
| A: But also things like like like menus or p how about preferences of your | `ami_silent` | ignore | wait | 0.06 | 0.83 |
| A: uh with configuring your remote control for favourite your favourite channel for example, how do you configure | `ami_silent` | ignore | wait | 0.12 | 0.90 |
| A: I think we d should just lower this. | `ami_silent` | ignore | wait | 0.06 | 0.54 |
| C: Think about | `ami_silent` | ignore | wait | 0.08 | 0.60 |
| A: Can you talk to remote control? | `ami_silent` | ignore | wait | 0.19 | 0.87 |
| B: Maybe we should go with a two then, | `ami_silent` | ignore | wait | 0.06 | 0.55 |
| D: right? | `ami_silent` | ignore | wait | 0.10 | 0.77 |
| B: Overall score. | `ami_silent` | ignore | wait | 0.09 | 0.61 |
| B: Is two two third. | `ami_silent` | ignore | wait | 0.06 | 0.71 |
| D: Y not | `ami_silent` | ignore | wait | 0.10 | 0.77 |
| A: It just looking for improvements what what you could have improved. | `ami_silent` | ignore | wait | 0.08 | 0.76 |
| A: Or your sh you should lose the L_C_D_ screen probably, | `ami_silent` | ignore | wait | 0.05 | 0.50 |
| B: So did you | `ami_silent` | ignore | wait | 0.07 | 0.76 |
| A: what was left in the the Another one. | `ami_silent` | ignore | wait | 0.09 | 0.78 |
| A: General project, what's i in | `ami_silent` | ignore | wait | 0.08 | 0.79 |
| D: Favourite channel. | `ami_silent` | ignore | wait | 0.09 | 0.65 |
| C: You have to finish it completely, | `ami_silent` | ignore | wait | 0.05 | 0.52 |
| B: Oh can you? Okay. | `ami_silent` | ignore | wait | 0.12 | 0.62 |
| C: then download it, | `ami_silent` | ignore | wait | 0.05 | 0.54 |
| A: Any new ideas? | `ami_silent` | ignore | wait | 0.15 | 0.90 |
| B: it could also possibly be well, is it a more real-time information base, | `ami_silent` | ignore | wait | 0.10 | 0.80 |
| B: Is that we finished up the design | `ami_silent` | ignore | wait | 0.07 | 0.86 |
| A: Any new ideas found? | `ami_silent` | ignore | wait | 0.08 | 0.89 |
| A: Or is that a 'cause | `ami_silent` | ignore | wait | 0.07 | 0.80 |
| B: How much time do we have for this anyway? | `ami_silent` | ignore | wait | 0.08 | 0.92 |
| A: Should i | `ami_silent` | ignore | wait | 0.11 | 0.85 |
| C: bring out the beer. | `ami_silent` | ignore | wait | 0.13 | 0.78 |
| D: I want one for my own. | `ami_silent` | ignore | wait | 0.07 | 0.61 |
| A: I'm not sure what we should still do though | `ami_silent` | ignore | wait | 0.08 | 0.87 |
| A: what | `ami_silent` | ignore | wait | 0.15 | 0.81 |
| A: right? | `ami_silent` | ignore | wait | 0.09 | 0.83 |
| A: What you ha from your assistant. So let's | `ami_silent` | ignore | wait | 0.18 | 0.55 |
| D: What | `ami_silent` | ignore | wait | 0.11 | 0.76 |
| A: How about you cook a how about you cook up a product name? | `ami_silent` | ignore | wait | 0.09 | 0.86 |
| D: Or fruit name. | `ami_silent` | ignore | wait | 0.08 | 0.51 |
| A: oh, think of a catchy name. | `ami_silent` | ignore | wait | 0.07 | 0.92 |
| A: What? Fruit? | `ami_silent` | ignore | wait | 0.11 | 0.82 |
| B: can we do anything with that? | `ami_silent` | ignore | wait | 0.10 | 0.90 |
| B: Is that a name or a c campaign? | `ami_silent` | ignore | wait | 0.38 | 0.88 |
| A: Real reactor? | `ami_silent` | ignore | wait | 0.06 | 0.83 |
| B: You should write it down as a an option. | `ami_silent` | ignore | wait | 0.08 | 0.69 |
| B: Should I write the banana down or | `ami_silent` | ignore | wait | 0.09 | 0.89 |
| B: Sure? | `ami_silent` | ignore | wait | 0.11 | 0.71 |
| B: Uh do you mean it like | `ami_silent` | ignore | wait | 0.10 | 0.78 |
| C: ? | `ami_silent` | ignore | wait | 0.06 | 0.57 |
| B: You mean it like this? | `ami_silent` | ignore | wait | 0.07 | 0.71 |
| C: Doesn't sound? | `ami_silent` | ignore | wait | 0.10 | 0.79 |
| A: Just write out triple, like a word triple R_C_, triple stripe Oh. Triple dash R_ dash s s C_. | `ami_silent` | ignore | wait | 0.06 | 0.50 |
| B: Dash C_? | `ami_silent` | ignore | wait | 0.20 | 0.79 |
| A: Triple R_ or triple R_C_? | `ami_silent` | ignore | wait | 0.07 | 0.84 |
| B: Like a C_ right now or a dash in a C_? | `ami_silent` | ignore | wait | 0.31 | 0.86 |
| A: How about do both? | `ami_silent` | ignore | wait | 0.09 | 0.85 |
| B: Is it triple R_C_s? No. | `ami_silent` | ignore | wait | 0.11 | 0.77 |
| B: which ones are we going to scratch definitely? | `ami_silent` | ignore | wait | 0.05 | 0.90 |
| B: Triple R_? | `ami_silent` | ignore | wait | 0.07 | 0.86 |
| C: did you do now? | `ami_silent` | ignore | wait | 0.11 | 0.83 |
| A: Could you guys draw me a picture of the final design to put on the cover of the report? | `ami_silent` | ignore | wait | 0.07 | 0.90 |
| C: Can't we take this one? | `ami_silent` | ignore | wait | 0.14 | 0.83 |
| C: Is it okay if I try? Is that okay with you? | `ami_silent` | ignore | wait | 0.08 | 0.84 |
| C: but where to I don't know. | `ami_silent` | ignore | wait | 0.10 | 0.80 |
| C: Oh, can I say exp | `ami_silent` | ignore | wait | 0.11 | 0.82 |
| C: can I not put this wherever I wants. | `ami_silent` | ignore | wait | 0.16 | 0.85 |
| C: My document is the wrong one, huh. | `ami_silent` | ignore | wait | 0.11 | 0.77 |
| C: Are you gonna do that? | `ami_silent` | ignore | wait | 0.10 | 0.77 |
| D: Can I see scores? | `ami_silent` | ignore | wait | 0.13 | 0.87 |
