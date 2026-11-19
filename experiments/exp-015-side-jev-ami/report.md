# Jev baseline: exp-015-side-jev-ami

Generated 2026-11-19T00:05:49+00:00 by `sidechat/pipeline/baseline.py`. Every number below is measured in this run.

## What was run

- **Model:** `jev-1.13.0`, asked with the daily-audience demo's two questions and state (commit `73171de`, wording hash `476c554866d6`), through Pipecat 1.16.0's `JevClassifier`.
- **Decision rule:** the demo's. Answer now when `addressed ≥ 0.8`, hold for silence when `question ≥ 0.5`, otherwise stay quiet.
- **Requests:** 8,875 distinct (0 reused from earlier runs, 8,875 asked now, 0 failed).
- **Tokens this run:** 6,971,445 in, 328,375 out. About $0.293 at $0.042 per million input tokens, a price recorded in Audience's repo and not confirmed with TypeSafe.
- **Baseline id:** `jev-demo-0.1`. Stored answers are reused, so later runs compare against these numbers.

A share is written `value (k/n; 95% interval)`. "For others" means lines the set marks as not for the agent.

## ami-addressee-0.1

Source: `ACloudCenter/ami-addressee` at `4bab33cda780`. Use: test only for now.

8,875 rows, 8,875 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 85.2% (7563/8875; 84.5 to 85.9) | 85.2% (7563/8875) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |
| Name said → answer | 100.0% (8875/8875; 100.0 to 100.0) | 100.0% (8875/8875) | 0.0% (0/8875) | 0.0% (0/8875) | n/a | n/a |

Jev latency from Modal: 74 ms at the median, 136 ms at the 95th percentile (8,875 answers, 12 requests at a time).

**By code** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `` | 8875 | 85.2% (7563/8875) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |

**By style** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `` | 8875 | 85.2% (7563/8875) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |

**By kind** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `` | 8875 | 85.2% (7563/8875) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |

**Lines Jev decides differently from the label** (1312 of 8875)

| Line | Kind | Expected | Jev | addressed | question |
|---|---|---|---|---|---|
| B: Do you want to introduce yourself again? | `` | ignore | wait | 0.06 | 0.82 |
| A: Um introduce yourself, | `` | ignore | wait | 0.05 | 0.59 |
| A: um say one thing about yourself | `` | ignore | wait | 0.04 | 0.54 |
| A: and then draw your favourite animal | `` | ignore | wait | 0.05 | 0.52 |
| A: and tell us about it. | `` | ignore | wait | 0.04 | 0.60 |
| B: Um I don't know which one of these I have to bring with me. | `` | ignore | wait | 0.28 | 0.84 |
| A: How do you spell your name? | `` | ignore | wait | 0.08 | 0.65 |
| A: So what are your favourite characteristics? | `` | ignore | wait | 0.09 | 0.87 |
| A: Shall we just go around the table? | `` | ignore | wait | 0.07 | 0.90 |
| C: shouldn't I | `` | ignore | wait | 0.13 | 0.76 |
| B: you can erase the turtle, | `` | ignore | wait | 0.07 | 0.53 |
| C: Is that at least identifiable? | `` | ignore | wait | 0.14 | 0.85 |
| B: snake? | `` | ignore | wait | 0.05 | 0.76 |
| D: but how? | `` | ignore | wait | 0.17 | 0.90 |
| D: Sort of give an idea. | `` | ignore | wait | 0.21 | 0.79 |
| A: just to generate a little bit of discussion about the project um, I could I'd like to hear about your experien | `` | ignore | wait | 0.07 | 0.89 |
| A: um your first ideas about um creating a new r remote control, | `` | ignore | wait | 0.08 | 0.85 |
| A: what would be the best um like you what are the features that you really like | `` | ignore | wait | 0.07 | 0.91 |
| A: what are the features that you don't like, etcetera, | `` | ignore | wait | 0.06 | 0.90 |
| D: What about like batteries and things like that, | `` | ignore | wait | 0.09 | 0.89 |
| D: like are there some remotes that don don't require like batteries | `` | ignore | wait | 0.10 | 0.93 |
| D: or do all remotes require batteries? | `` | ignore | wait | 0.15 | 0.94 |
| A: So how do we work with that? | `` | ignore | wait | 0.06 | 0.92 |
| B: Could we get something that | `` | ignore | wait | 0.13 | 0.84 |
| B: but that just has your major buttons for that work for everything, you know volume control, on, off, | `` | ignore | wait | 0.09 | 0.57 |
| B: and if um if you'd save the more complicated functions maybe for separate remotes that you wouldn't need to us | `` | ignore | wait | 0.08 | 0.66 |
| C: Can I ask, | `` | ignore | wait | 0.07 | 0.81 |
| C: are we designing a remote control for a television only | `` | ignore | wait | 0.09 | 0.91 |
| C: um, and if if this device is just to be used for the television | `` | ignore | wait | 0.06 | 0.81 |
| C: would we even technically be possible to include video recorder functions on it? | `` | ignore | wait | 0.20 | 0.89 |
| C: Um or should we just stick to just stick to having television television related buttons on it? | `` | ignore | wait | 0.22 | 0.90 |
| A: Mind if we move on? | `` | ignore | wait | 0.04 | 0.91 |
| A: so we can continue discussing more new ideas if you'd like um, | `` | ignore | wait | 0.05 | 0.85 |
| A: Any questions? | `` | ignore | wait | 0.05 | 0.92 |
| C: What we're gonna be discussing at the next meeting? | `` | ignore | wait | 0.48 | 0.90 |
| C: Do we know that? | `` | ignore | wait | 0.29 | 0.86 |
| C: Can you e-mail your slides as well? | `` | ignore | wait | 0.05 | 0.67 |
| C: Is that possible? | `` | ignore | wait | 0.31 | 0.71 |
| A: four? | `` | ignore | wait | 0.10 | 0.80 |
| A: Is that correct? | `` | ignore | wait | 0.06 | 0.86 |
| A: Just make sure you keep checking the company web site and the emails. | `` | ignore | wait | 0.06 | 0.72 |
| A: just check the time, | `` | ignore | wait | 0.13 | 0.81 |
| A: did you all get the minutes? | `` | ignore | wait | 0.06 | 0.91 |
| A: um you can go in any order you choose um. | `` | ignore | wait | 0.04 | 0.64 |
| D: Mm shall we go in the order that you just did it? | `` | ignore | wait | 0.09 | 0.87 |
| D: How do I hook my screen up? | `` | ignore | wait | 0.18 | 0.92 |
| D: Where does it go? | `` | ignore | wait | 0.09 | 0.90 |
| D: Where's function? | `` | ignore | wait | 0.12 | 0.89 |
| A: Is it plugged in all the way | `` | ignore | wait | 0.07 | 0.84 |
| D: Push the screw. | `` | ignore | wait | 0.10 | 0.56 |
| D: I don't know if you guys are able to get access to um the report that was online | `` | ignore | wait | 0.10 | 0.86 |
| D: or if I'm the only one who is. | `` | ignore | wait | 0.05 | 0.89 |
| D: and I was hoping someone might be able to inform me as to what R_S_I_ is, | `` | ignore | wait | 0.10 | 0.94 |
| A: Was that you? | `` | ignore | wait | 0.08 | 0.80 |
| D: have I unscrewed it? | `` | ignore | wait | 0.09 | 0.79 |
| A: Push. | `` | ignore | wait | 0.06 | 0.59 |
| C: Um how do we actually go about designing a new television remote control? | `` | ignore | wait | 0.19 | 0.94 |
| C: uh what can we do with the current state of technology as it is. | `` | ignore | wait | 0.08 | 0.89 |
| C: uh what things do they get right, | `` | ignore | wait | 0.12 | 0.89 |
| C: what's wrong with 'em, | `` | ignore | wait | 0.12 | 0.53 |
| C: um how we can improve on the designs that that that I found | `` | ignore | wait | 0.12 | 0.68 |
| C: and what can we do to make our product stand out from from the large majority of remote controls. | `` | ignore | wait | 0.08 | 0.90 |
| D: did it let you go on the Internet | `` | ignore | wait | 0.27 | 0.82 |
| D: or was that just what it let you see? | `` | ignore | wait | 0.18 | 0.80 |
| B: how do I play again? | `` | ignore | wait | 0.14 | 0.91 |
| B: but how do I get to the next s | `` | ignore | wait | 0.19 | 0.87 |
| B: what what needs to be done | `` | ignore | wait | 0.12 | 0.77 |
| B: and how do we convert all the elements to make that done. | `` | ignore | wait | 0.11 | 0.86 |
| A: use that thing you can go back, previous. | `` | ignore | wait | 0.30 | 0.76 |
| A: right? | `` | ignore | wait | 0.10 | 0.77 |
| C: What's up? | `` | ignore | wait | 0.12 | 0.87 |
| D: What's teletext? | `` | ignore | wait | 0.06 | 0.93 |
| C: You don't have it in the States? | `` | ignore | wait | 0.05 | 0.85 |
| A: would you care to explain it? | `` | ignore | wait | 0.12 | 0.80 |
| A: How? | `` | ignore | wait | 0.11 | 0.88 |
| C: So what's our corporate image like? | `` | ignore | wait | 0.05 | 0.89 |
| A: we need to talk about our functions and our target group. | `` | ignore | wait | 0.07 | 0.50 |
| A: We need to decide who our target group is. | `` | ignore | wait | 0.07 | 0.75 |
| A: who are we aiming this at? | `` | ignore | wait | 0.06 | 0.91 |
| D: I do think, who's gonna have the money to buy that also, that one? | `` | ignore | wait | 0.04 | 0.88 |
| C: Is it is it something that's gonna be sold separately from the television | `` | ignore | wait | 0.05 | 0.89 |
| C: or is it something that comes w with a television? | `` | ignore | wait | 0.04 | 0.90 |
| A: Are we gonna use that as one of our functions? | `` | ignore | wait | 0.06 | 0.91 |
| C: we've got a price limit of was it twelve twelve and a half Euros for to produce it? | `` | ignore | wait | 0.05 | 0.85 |
| C: And I wonder if we can get voice recognition into that twelve and a half Euros without having to make too many | `` | ignore | wait | 0.13 | 0.84 |
| D: But what else are we gonna put, | `` | ignore | wait | 0.07 | 0.82 |
| D: I don't know what else you can put in a remote to make it technologically advanced though. | `` | ignore | wait | 0.05 | 0.67 |
| D: and why's anyone gonna buy a new remote? | `` | ignore | wait | 0.05 | 0.88 |
| B: but why are we why are we aiming for a technological advancement? | `` | ignore | wait | 0.06 | 0.90 |
| D: If someone's looking to buy a new remote, don't they want like an upgrade? | `` | ignore | wait | 0.06 | 0.90 |
| A: Upgrade? | `` | ignore | wait | 0.06 | 0.78 |
| A: And we also need to talk about if we're only gonna have the very simple ones | `` | ignore | wait | 0.07 | 0.66 |
| A: or also have the other ones just separate somehow | `` | ignore | wait | 0.05 | 0.70 |
| D: that had like the main buttons | `` | ignore | wait | 0.09 | 0.60 |
| D: Do you know what I'm saying? | `` | ignore | wait | 0.12 | 0.88 |
| A: what are we emphasising? I what in this project? | `` | ignore | wait | 0.05 | 0.93 |
| D: What can you do to like make the infra-red more functional, | `` | ignore | wait | 0.11 | 0.86 |
| D: like why would it not be? | `` | ignore | wait | 0.28 | 0.79 |
| A: So our target group, we're saying, fifteen to thirty five? | `` | ignore | wait | 0.06 | 0.90 |
| D: And if the whole idea is you're using a remote then why would you have voice, | `` | ignore | wait | 0.12 | 0.86 |
| D: like you know what I mean and then it's like you wouldn't need a remote | `` | ignore | wait | 0.05 | 0.53 |
| A: can we narrow it down to maybe um teenagers and families? | `` | ignore | wait | 0.05 | 0.92 |
| A: 'Cause that would go up to like fifty? | `` | ignore | wait | 0.05 | 0.85 |
| D: and like how recently have they bought their television like that sort of thing. | `` | ignore | wait | 0.05 | 0.69 |
| A: do we want some kind of thing to find it if it's lost? | `` | ignore | wait | 0.07 | 0.92 |
| A: or beep? | `` | ignore | wait | 0.06 | 0.88 |
| A: We want a possibility to um to get um a possibility to get the extra functions. | `` | ignore | wait | 0.08 | 0.70 |
| A: And we also want it to be fashionable, | `` | ignore | wait | 0.12 | 0.70 |
| A: do it. | `` | ignore | wait | 0.14 | 0.60 |
| A: Any other essential functions that we need? | `` | ignore | wait | 0.12 | 0.92 |
| A: Battery? Do we need a long-life battery? | `` | ignore | wait | 0.09 | 0.93 |
| C: We should maybe investigate whether it needs a battery at all. | `` | ignore | wait | 0.05 | 0.80 |
| B: So you don't ha you got like a rechargeable battery. | `` | ignore | wait | 0.09 | 0.75 |
| A: I mean, would you put it on top of the T_V_? | `` | ignore | wait | 0.07 | 0.86 |
| A: just think | `` | ignore | wait | 0.06 | 0.62 |
| A: has everyone said their functions | `` | ignore | wait | 0.07 | 0.90 |
| A: I don't know what summarisation. | `` | ignore | wait | 0.11 | 0.61 |
| A: If everyone could do that as well, that'd be great. | `` | ignore | wait | 0.04 | 0.84 |
| A: Be sure to note any frustrations or any um issues that come up in your um in your um summary. | `` | ignore | wait | 0.06 | 0.59 |
| A: Mm 'kay? | `` | ignore | wait | 0.07 | 0.57 |
| D: were you able to like put yours in the group folder? | `` | ignore | wait | 0.06 | 0.78 |
| B: Yeah? | `` | ignore | wait | 0.04 | 0.59 |
| D: Where is that? | `` | ignore | wait | 0.08 | 0.80 |
| A: You don't have mine? | `` | ignore | wait | 0.04 | 0.77 |
| A: uh whoever wants to go first is f fine by me | `` | ignore | wait | 0.04 | 0.73 |
| A: without th further ado, whoever wants to go first is free to. | `` | ignore | wait | 0.04 | 0.86 |
| A: I'm not calling you the wrong name over and over again? | `` | ignore | wait | 0.06 | 0.62 |
| A: What kind of th thickness are we looking at? | `` | ignore | wait | 0.06 | 0.90 |
| A: is there an option that we can have that off or on | `` | ignore | wait | 0.17 | 0.89 |
| B: um and my question to all of you is, should we look to other manufacturies | `` | ignore | wait | 0.09 | 0.95 |
| B: or should we just make do with what we have available? | `` | ignore | wait | 0.07 | 0.94 |
| D: but with our time constraints, is that really a feasible option? | `` | ignore | wait | 0.04 | 0.89 |
| A: Can we do marketing piloting too? | `` | ignore | wait | 0.07 | 0.92 |
| A: Try to see what kind before we launch can we see how they're received? | `` | ignore | wait | 0.05 | 0.90 |
| D: You waiting for me? | `` | ignore | wait | 0.09 | 0.80 |
| C: Did you? | `` | ignore | wait | 0.08 | 0.64 |
| D: what a teaser ain't it. | `` | ignore | wait | 0.08 | 0.60 |
| A: isn't it? | `` | ignore | wait | 0.07 | 0.82 |
| C: One moment please. | `` | ignore | wait | 0.10 | 0.50 |
| A: Based on what Nathan presented as far as the um various costs and benefits um I think, I dunno, what do you gu | `` | ignore | wait | 0.04 | 0.92 |
| D: But can we really afford it | `` | ignore | wait | 0.04 | 0.91 |
| D: right? | `` | ignore | wait | 0.16 | 0.83 |
| D: Per? | `` | ignore | wait | 0.07 | 0.79 |
| D: or we have to be under twelve fifty? | `` | ignore | wait | 0.04 | 0.85 |
| D: Do we remember? | `` | ignore | wait | 0.06 | 0.91 |
| D: Can we justify it? | `` | ignore | wait | 0.12 | 0.90 |
| C: Where do you guys come up with these numbers? | `` | ignore | wait | 0.17 | 0.87 |
| D: See if we can cut some corners. | `` | ignore | wait | 0.05 | 0.62 |
| C: Does having both really up our costs? | `` | ignore | wait | 0.07 | 0.91 |
| A: which, which do we suspect we should hold o we should hold on to? | `` | ignore | wait | 0.07 | 0.89 |
| A: Is it cheaper to do the V_R_ or to do the uh touch screen? | `` | ignore | wait | 0.05 | 0.77 |
| A: more or less you guys think that o o of the two of 'em, the voice recognition will be better. | `` | ignore | wait | 0.10 | 0.84 |
| D: and when are we gonna have basic prototypes coming up next | `` | ignore | wait | 0.12 | 0.84 |
| D: that's you guys's next step right? | `` | ignore | wait | 0.06 | 0.81 |
| B: Are we going to talk now about um the materials that we're gonna use for the case and all those things? | `` | ignore | wait | 0.04 | 0.92 |
| A: Would the solar power be enough to fuel a voice recognition? | `` | ignore | wait | 0.08 | 0.91 |
| A: Or this kinesthetic one, would that be enough to fuel a voice recognition remote control? | `` | ignore | wait | 0.16 | 0.90 |
| D: what of people with like the T_V_ in their basement, | `` | ignore | wait | 0.05 | 0.80 |
| B: Why, why moving away from hand-held, why? | `` | ignore | wait | 0.05 | 0.82 |
| B: What's the uh idea? | `` | ignore | wait | 0.09 | 0.85 |
| B: Do you think people that are people that buy a remote, are they always gonna wanna use the voice recognition | `` | ignore | wait | 0.08 | 0.88 |
| B: or is it just something that they do sometimes. | `` | ignore | wait | 0.06 | 0.87 |
| A: or like um who is it, | `` | ignore | wait | 0.08 | 0.75 |
| A: I mean, why not have a little rounded kind of thing, | `` | ignore | wait | 0.05 | 0.82 |
| D: you know like that little pod looking thing? | `` | ignore | wait | 0.05 | 0.61 |
| D: which is the next big thing, | `` | ignore | wait | 0.14 | 0.78 |
| A: let's see if we can do a squishy non-remote control-looking remote control. | `` | ignore | wait | 0.07 | 0.63 |
| D: and do we wanna consider like an iPod screen | `` | ignore | wait | 0.08 | 0.88 |
| A: if we're gonna have a non-remote-looking remote, how do we yeah. | `` | ignore | wait | 0.06 | 0.84 |
| B: we need to figure out what kind of buttons we're going to use, | `` | ignore | wait | 0.06 | 0.80 |
| B: are we going to use scroll buttons? Rubber buttons? Um | `` | ignore | wait | 0.07 | 0.90 |
| A: any final thoughts before we think about doing the protot moving on to the prototype. | `` | ignore | wait | 0.06 | 0.90 |
| C: Well what are we actually doing? | `` | ignore | wait | 0.15 | 0.90 |
| A: I wasn't? | `` | ignore | wait | 0.04 | 0.70 |
| A: any other final thoughts before we go ahead and | `` | ignore | wait | 0.05 | 0.89 |
| A: cool? | `` | ignore | wait | 0.07 | 0.86 |
| B: have we decided that we are gonna go with different style cases for different people? | `` | ignore | wait | 0.04 | 0.92 |
| B: Or are we just going to go with one? | `` | ignore | wait | 0.05 | 0.93 |
| A: let's work on uh multiple case colours. | `` | ignore | wait | 0.05 | 0.58 |
| A: what can we accomplish, um, given these parameters that we're just gonna sort of have this kind of uh non-remo | `` | ignore | wait | 0.07 | 0.83 |
| A: Um, what are our broad constraints before we deve design a prototype. | `` | ignore | wait | 0.08 | 0.90 |
| A: figure out how probably best to lay out this idea of this simple design with the voice recognition built in an | `` | ignore | wait | 0.06 | 0.64 |
| A: Somehow work out how we can get this all s in the same place. | `` | ignore | wait | 0.06 | 0.80 |
| A: Um, and if you can check product evaluation with m some pilots and stuff. | `` | ignore | wait | 0.06 | 0.80 |
| A: Um I need you guys to work together on making a prototype, um using um prototype building materials um. | `` | ignore | wait | 0.05 | 0.85 |
| A: is that alright, | `` | ignore | wait | 0.07 | 0.83 |
| A: you guys feel clear about this? | `` | ignore | wait | 0.04 | 0.93 |
| C: Ready for this? | `` | ignore | wait | 0.08 | 0.85 |
| A: All set? | `` | ignore | wait | 0.07 | 0.86 |
| B: really? | `` | ignore | wait | 0.04 | 0.57 |
| A: uh, I will open them slowly, no? | `` | ignore | wait | 0.06 | 0.79 |
| A: what kind of risk we'd be looking at with some of the various approaches we were discussing | `` | ignore | wait | 0.05 | 0.51 |
| A: um, go ahead and take it away guys. | `` | ignore | wait | 0.05 | 0.65 |
| B: What's to be said about it? | `` | ignore | wait | 0.06 | 0.86 |
| B: why not? | `` | ignore | wait | 0.08 | 0.82 |
| C: if you will. | `` | ignore | wait | 0.06 | 0.55 |
| C: Um, what other things do we see here, well, um | `` | ignore | wait | 0.07 | 0.86 |
| C: do you have anything else to add to that? | `` | ignore | wait | 0.15 | 0.87 |
| D: Do we need to worry about um rot factors? | `` | ignore | wait | 0.09 | 0.90 |
| C: um I dunno if you guys have any questions | `` | ignore | wait | 0.06 | 0.89 |
| C: or f whether that uh whether we need to worry about any uh other marketing areas or anything of that nature. | `` | ignore | wait | 0.04 | 0.87 |
| C: Um, did we come in under budget? | `` | ignore | wait | 0.06 | 0.89 |
| B: what was our goal? | `` | ignore | wait | 0.06 | 0.87 |
| C: Did we talk about the voice recognition uh option? | `` | ignore | wait | 0.06 | 0.92 |
| B: Oh no, we haven't talked about that yet have we? | `` | ignore | wait | 0.03 | 0.83 |
| B: Any questions? | `` | ignore | wait | 0.06 | 0.92 |
| D: Do we have um other, for lack of a better word, skins? Covers? | `` | ignore | wait | 0.07 | 0.90 |
| D: or are those ones gonna be developed later once we see how the couple we have g go or? | `` | ignore | wait | 0.06 | 0.87 |
| B: Um, do you wanna answer this one | `` | ignore | wait | 0.10 | 0.72 |
| D: Do we know where we stand on that yet? | `` | ignore | wait | 0.05 | 0.86 |
| B: or do you want me to answer it? | `` | ignore | wait | 0.04 | 0.65 |
| A: if we can just itemize what's in here, | `` | ignore | wait | 0.05 | 0.65 |
| A: right? | `` | ignore | wait | 0.09 | 0.85 |
| A: With a back-up battery? | `` | ignore | wait | 0.07 | 0.88 |
| A: isn't it? | `` | ignore | wait | 0.07 | 0.83 |
| A: don't we? | `` | ignore | wait | 0.05 | 0.84 |
| B: don't you? | `` | ignore | wait | 0.16 | 0.75 |
| D: M come in at sixteen? | `` | ignore | wait | 0.10 | 0.56 |
| B: does it? | `` | ignore | wait | 0.10 | 0.80 |
| B: How do you feel about that? | `` | ignore | wait | 0.18 | 0.78 |
| B: what am I gonna do? | `` | ignore | wait | 0.09 | 0.83 |
| C: right? | `` | ignore | wait | 0.04 | 0.68 |
| B: isn't it? | `` | ignore | wait | 0.04 | 0.79 |
| D: Um cord? | `` | ignore | wait | 0.16 | 0.80 |
| D: Can you reach, | `` | ignore | wait | 0.21 | 0.82 |
| D: does it fulfil its functions as a remote? | `` | ignore | wait | 0.10 | 0.84 |
| D: Is the design what we wanted it to do? | `` | ignore | wait | 0.09 | 0.88 |
| D: are technologies up to where we hoped they would be | `` | ignore | wait | 0.06 | 0.88 |
| D: and does it fulfil the aesthetic qualities that our original market research was looking for? Um. | `` | ignore | wait | 0.06 | 0.88 |
| D: Basic questions like, you know, does it turn on? | `` | ignore | wait | 0.05 | 0.80 |
| D: Does it respond to voice recognition? | `` | ignore | wait | 0.09 | 0.91 |
| D: Um, the only thing is with with the pull-out panel, that is, can it take some adjusting | `` | ignore | wait | 0.06 | 0.85 |
| D: do you need the cord back? | `` | ignore | wait | 0.08 | 0.82 |
| A: go on. | `` | ignore | wait | 0.08 | 0.51 |
| A: do they? | `` | ignore | wait | 0.09 | 0.84 |
| D: As in within the team or? | `` | ignore | wait | 0.07 | 0.83 |
| B: it's just kind of a open mic kind of thing or | `` | ignore | wait | 0.07 | 0.75 |
| A: any thoughts? | `` | ignore | wait | 0.10 | 0.92 |
| B: Are we considering these points here? | `` | ignore | wait | 0.08 | 0.89 |
| A: What do you guys feel about the process? | `` | ignore | wait | 0.04 | 0.94 |
| D: We could now if that'd make up for it | `` | ignore | wait | 0.09 | 0.73 |
| B: What if you get a response two or three months from now? | `` | ignore | wait | 0.04 | 0.66 |
| D: what kind of coaching is that really? | `` | ignore | wait | 0.24 | 0.84 |
| D: What if I really needed something. | `` | ignore | wait | 0.17 | 0.89 |
| A: What did you guys think about the the the roles? | `` | ignore | wait | 0.05 | 0.94 |
| D: Do your own. | `` | ignore | wait | 0.09 | 0.69 |
| D: give the rest of us some structure to work with so hey. | `` | ignore | wait | 0.08 | 0.71 |
| C: is that the first time you've taken on that kind of role? | `` | ignore | wait | 0.11 | 0.73 |
| A: But you guys felt that you could keep the, yeah, suspension of disbelief kind of like like the role and the ok | `` | ignore | wait | 0.05 | 0.88 |
| A: did you guys ever used to build spaceships with Legos | `` | ignore | wait | 0.07 | 0.92 |
| A: Um you guys felt like there was enough teamwork in all? | `` | ignore | wait | 0.05 | 0.93 |
| B: Yeah? | `` | ignore | wait | 0.14 | 0.59 |
| A: It's true huh? | `` | ignore | wait | 0.06 | 0.81 |
| A: wasn't it? | `` | ignore | wait | 0.06 | 0.79 |
| B: is there anything about the way that we got so much inform what was it that kept us from going to the the boar | `` | ignore | wait | 0.07 | 0.89 |
| A: I wanna see the output files from these um, from the digital paper. | `` | ignore | wait | 0.14 | 0.85 |
| A: I wanna see wh wh what my my handwriting looks like digitized | `` | ignore | wait | 0.19 | 0.84 |
| A: just to see what it looks like in P_D_F_ format or something. | `` | ignore | wait | 0.11 | 0.52 |
| A: I I'm curious about what the de-briefing is gonna be like. | `` | ignore | wait | 0.12 | 0.72 |
| A: what exactly we're looking for here. | `` | ignore | wait | 0.10 | 0.84 |
| C: is this all we need to get through? | `` | ignore | wait | 0.16 | 0.86 |
| D: It did it just say in an email that we need to discuss that? | `` | ignore | wait | 0.08 | 0.85 |
| D: That slide was like that? | `` | ignore | wait | 0.04 | 0.74 |
| C: Any new ideas with regard to remote control concepts? | `` | ignore | wait | 0.08 | 0.94 |
| A: Does kinda make you wonder, | `` | ignore | wait | 0.07 | 0.76 |
| A: how much can you do with a remote control? | `` | ignore | wait | 0.14 | 0.89 |
| C: What is that? Our limited ability to think outside the box? | `` | ignore | wait | 0.17 | 0.86 |
| B: Are we back into project mood? | `` | ignore | wait | 0.09 | 0.92 |
| D: how long was our meeting supposed to be? | `` | ignore | wait | 0.06 | 0.91 |
| D: How much time do we have left? | `` | ignore | wait | 0.09 | 0.92 |
| A: I I I mm we should go on a bit yeah about the project eval, um. | `` | ignore | wait | 0.04 | 0.50 |
| A: what like you know what am I really doing, | `` | ignore | wait | 0.10 | 0.75 |
| C: Why? | `` | ignore | wait | 0.05 | 0.77 |
| D: so type away. | `` | ignore | wait | 0.11 | 0.65 |
| B: Did you really? | `` | ignore | wait | 0.04 | 0.72 |
| A: Really? | `` | ignore | wait | 0.05 | 0.70 |
| A: they didn't come like this? | `` | ignore | wait | 0.05 | 0.85 |
| D: Like with those words already on it? | `` | ignore | wait | 0.05 | 0.75 |
| A: Any other thoughts come to mind? | `` | ignore | wait | 0.09 | 0.93 |
| D: I wanna know how our product would fare. | `` | ignore | wait | 0.33 | 0.83 |
| C: again I reiterate my question | `` | ignore | wait | 0.12 | 0.61 |
| C: of how different we are comp compared to the other groups, especially between culture groups and what not. | `` | ignore | wait | 0.06 | 0.73 |
| B: we have more slides or? | `` | ignore | wait | 0.05 | 0.87 |
| B: It'd be so cool if we get a copy of the recording. | `` | ignore | wait | 0.07 | 0.84 |
| D: Make it sound eloquent. | `` | ignore | wait | 0.12 | 0.76 |
| C: What the uhs and the | `` | ignore | wait | 0.21 | 0.60 |
| B: Filler words or? | `` | ignore | wait | 0.12 | 0.86 |
| C: yeah? | `` | ignore | wait | 0.25 | 0.72 |
| C: In the eighties? | `` | ignore | wait | 0.04 | 0.67 |
| C: You guys ready to celebrate? | `` | ignore | wait | 0.05 | 0.90 |
| D: Apparently, does that include like champagne or something exciting? | `` | ignore | wait | 0.08 | 0.90 |
| B: Has it been forty minutes or whatever? | `` | ignore | wait | 0.06 | 0.90 |
| C: Celebrate. | `` | ignore | wait | 0.04 | 0.61 |
| A: Where do you find that? | `` | ignore | wait | 0.11 | 0.83 |
| B: Is that the only song you have? | `` | ignore | wait | 0.22 | 0.81 |
| A: Is this one of those media player? | `` | ignore | wait | 0.10 | 0.87 |
| C: Huh? | `` | ignore | wait | 0.25 | 0.65 |
| D: is that a close? | `` | ignore | wait | 0.22 | 0.83 |
| C: and you have to adjust the length. | `` | ignore | wait | 0.08 | 0.52 |
| D: You know? | `` | ignore | wait | 0.07 | 0.75 |
| B: Just try. | `` | ignore | wait | 0.09 | 0.60 |
| B: and you can put can clip it uh on your | `` | ignore | wait | 0.16 | 0.57 |
| B: I don't know whether you worked with them before. | `` | ignore | wait | 0.09 | 0.76 |
| B: uh, well, how it should be | `` | ignore | wait | 0.05 | 0.64 |
| B: and uh wh what uh what our new product should look lite like. | `` | ignore | wait | 0.05 | 0.65 |
| B: mm? | `` | ignore | wait | 0.12 | 0.60 |
| B: but maybe one of you did, so Um | `` | ignore | wait | 0.10 | 0.84 |
| B: Do Do we have to say something about that? | `` | ignore | wait | 0.07 | 0.90 |
| B: um we uh we should try to t to draw on it | `` | ignore | wait | 0.04 | 0.59 |
| D: shall I start? | `` | ignore | wait | 0.09 | 0.87 |
| B: D doesn't it work? | `` | ignore | wait | 0.04 | 0.61 |
| B: Why don't you draw uh your favourite animal on on th on the white-board. | `` | ignore | wait | 0.09 | 0.68 |
| C: eh? | `` | ignore | wait | 0.08 | 0.63 |
| C: We need a wireless microphone. | `` | ignore | wait | 0.07 | 0.74 |
| C: You know? | `` | ignore | wait | 0.09 | 0.69 |
| C: the dog doesn't have a tail? | `` | ignore | wait | 0.06 | 0.89 |
| B: isn't it? | `` | ignore | wait | 0.06 | 0.78 |
| B: Uh d did you uh work out cord? | `` | ignore | wait | 0.09 | 0.76 |
| D: right? | `` | ignore | wait | 0.20 | 0.80 |
| C: right? | `` | ignore | wait | 0.07 | 0.78 |
| A: A horse? | `` | ignore | wait | 0.08 | 0.85 |
| C: I think you can put that. | `` | ignore | wait | 0.08 | 0.61 |
| B: Can you can meet them in Africa, I think. | `` | ignore | wait | 0.21 | 0.80 |
| A: No? | `` | ignore | wait | 0.08 | 0.74 |
| B: I hope you have some space in your uh the horse of uh Mael. | `` | ignore | wait | 0.06 | 0.58 |
| C: So what should I draw? | `` | ignore | wait | 0.16 | 0.91 |
| A: Um. A mouse? | `` | ignore | wait | 0.08 | 0.79 |
| A: Your turn. | `` | ignore | wait | 0.12 | 0.64 |
| B: Which animal has not been drawn yet. | `` | ignore | wait | 0.08 | 0.85 |
| B: so why not draw an animal from the water. | `` | ignore | wait | 0.05 | 0.83 |
| D: Put it colours. | `` | ignore | wait | 0.11 | 0.71 |
| B: yes, why not? | `` | ignore | wait | 0.08 | 0.64 |
| C: you know it's going to eat the cat rather than the cat eating the fish, no? | `` | ignore | wait | 0.06 | 0.86 |
| D: right? | `` | ignore | wait | 0.12 | 0.77 |
| D: yeah? | `` | ignore | wait | 0.06 | 0.68 |
| B: Excuse me? | `` | ignore | wait | 0.06 | 0.74 |
| B: And uh now just let have some discussion about what is a good remote control | `` | ignore | wait | 0.05 | 0.79 |
| B: and uh well keep in mind this this first point, it has to be original, | `` | ignore | wait | 0.04 | 0.50 |
| B: Um, maybe someone can mention some additional uh prerequisites for a good remote control. | `` | ignore | wait | 0.08 | 0.95 |
| C: You need to browse the browse the channels in upward downward way, | `` | ignore | wait | 0.22 | 0.69 |
| D: are the marketing guy? Or | `` | ignore | wait | 0.05 | 0.80 |
| D: And you are in the u use user interface uh design. | `` | ignore | wait | 0.04 | 0.57 |
| C: yeah? | `` | ignore | wait | 0.06 | 0.68 |
| B: Are there some other very important things to to do well, | `` | ignore | wait | 0.09 | 0.89 |
| D: Like what? | `` | ignore | wait | 0.07 | 0.83 |
| D: Like internet on the on T_V_? | `` | ignore | wait | 0.07 | 0.85 |
| B: Uh w y you two should should, I think, think this over uh w espec what, what functionality. | `` | ignore | wait | 0.06 | 0.60 |
| A: So try and get T_V_ manufacturers to | `` | ignore | wait | 0.06 | 0.64 |
| B: Uh I would like to get this wrapped up | `` | ignore | wait | 0.04 | 0.55 |
| B: well, uh, you wor yes, work on a design, | `` | ignore | wait | 0.04 | 0.59 |
| B: keep it general, | `` | ignore | wait | 0.05 | 0.64 |
| B: And uh you and you and uh uh uh well, think about requirements, | `` | ignore | wait | 0.06 | 0.62 |
| B: Does it need internet, | `` | ignore | wait | 0.10 | 0.87 |
| B: or or do do we stay at | `` | ignore | wait | 0.06 | 0.82 |
| B: K keep it in mind. | `` | ignore | wait | 0.05 | 0.65 |
| B: Uh, you said twenty-five minutes, | `` | ignore | wait | 0.19 | 0.54 |
| B: so maybe you could hurry up a bit | `` | ignore | wait | 0.10 | 0.69 |
| A: sorry? | `` | ignore | wait | 0.05 | 0.61 |
| B: so if you could uh | `` | ignore | wait | 0.08 | 0.66 |
| A: You have another meeting soon? | `` | ignore | wait | 0.07 | 0.57 |
| A: So I will now ask you which is very important for the design of a new remote control for to uh each of us to t | `` | ignore | wait | 0.07 | 0.87 |
| A: Do you have any idea of which animal you want to show us? | `` | ignore | wait | 0.06 | 0.82 |
| A: If you want to react uh about this wonderful drawing uh I'll let you uh comment. | `` | ignore | wait | 0.07 | 0.54 |
| C: You should write y the name I think. | `` | ignore | wait | 0.14 | 0.75 |
| B: Wha what is this strange beast? | `` | ignore | wait | 0.16 | 0.85 |
| D: Is it beautiful? | `` | ignore | wait | 0.14 | 0.87 |
| B: Is it a monster? | `` | ignore | wait | 0.13 | 0.87 |
| D: Do you know? | `` | ignore | wait | 0.13 | 0.82 |
| D: Isn't it? | `` | ignore | wait | 0.08 | 0.71 |
| D: Is it better? | `` | ignore | wait | 0.10 | 0.85 |
| B: Does have a name? | `` | ignore | wait | 0.06 | 0.83 |
| A: Like a what? | `` | ignore | wait | 0.06 | 0.74 |
| B: Scary? | `` | ignore | wait | 0.07 | 0.82 |
| B: Is it for uh for putting a for logos, no. | `` | ignore | wait | 0.19 | 0.79 |
| B: I is there a matter for a new remote control? | `` | ignore | wait | 0.07 | 0.87 |
| B: Is it uh a single device remote control or is it a multi-device remote control? | `` | ignore | wait | 0.37 | 0.85 |
| B: this is not defined at all? | `` | ignore | wait | 0.09 | 0.82 |
| A: yeah you you can suggest points like this. | `` | ignore | wait | 0.07 | 0.54 |
| A: so we have to decide for example if it can control one device or multiple. | `` | ignore | wait | 0.07 | 0.60 |
| A: So what's what are your ideas about that? | `` | ignore | wait | 0.07 | 0.79 |
| A: Maybe I can have the your opinion from the marketing side? | `` | ignore | wait | 0.07 | 0.76 |
| B: Well uh do we sell other stuff? | `` | ignore | wait | 0.28 | 0.86 |
| B: otherwise who would buy a remote control from us. | `` | ignore | wait | 0.04 | 0.74 |
| A: Do you agree? | `` | ignore | wait | 0.04 | 0.63 |
| A: And uh do you have any ideas um of uh design ideas or any uh uh technical requirement we we should uh fulfil? | `` | ignore | wait | 0.07 | 0.90 |
| A: And do you have it also to be to be lighted in order to be used in the dark? | `` | ignore | wait | 0.05 | 0.91 |
| A: And do you have any um any uh idea of the trend the trend in domain, what it shouldn't it should look like, or | `` | ignore | wait | 0.06 | 0.89 |
| A: Optional or selled with it? | `` | ignore | wait | 0.05 | 0.85 |
| C: We should have s uh special bu button on the T_V_ to make the remote control beeping. | `` | ignore | wait | 0.06 | 0.58 |
| A: So we can uh have a whistle uh remote control? | `` | ignore | wait | 0.07 | 0.86 |
| A: I don't know, whistle-able? | `` | ignore | wait | 0.08 | 0.85 |
| B: but uh of course we you don't normally need uh any audio uh recording stuff on your remote control right? | `` | ignore | wait | 0.35 | 0.83 |
| B: but I'm not sure about the what you, | `` | ignore | wait | 0.22 | 0.54 |
| B: who is giving who's giving who's giving our budget. Who's | `` | ignore | wait | 0.10 | 0.85 |
| A: Okay so try to find that for next meeting. | `` | ignore | wait | 0.05 | 0.53 |
| A: next meeting is in thirty minutes or | `` | ignore | wait | 0.04 | 0.76 |
| B: Uh, so we come back in five minutes? | `` | ignore | wait | 0.09 | 0.85 |
| A: You eat it? | `` | ignore | wait | 0.05 | 0.83 |
| A: Does it move uh? | `` | ignore | wait | 0.11 | 0.88 |
| A: Okay? | `` | ignore | wait | 0.06 | 0.78 |
| A: I will try to summarise it and put that summary in the shared folder if you want to look at it afterwards | `` | ignore | wait | 0.03 | 0.54 |
| A: So uh who want to start the the presentation of what they did? | `` | ignore | wait | 0.04 | 0.94 |
| A: You can start. | `` | ignore | wait | 0.04 | 0.51 |
| A: You have uh PowerPoint? | `` | ignore | wait | 0.07 | 0.82 |
| B: no? | `` | ignore | wait | 0.04 | 0.76 |
| A: Who are you? | `` | ignore | wait | 0.09 | 0.82 |
| B: No? | `` | ignore | wait | 0.07 | 0.60 |
| C: What do you have in short cut? | `` | ignore | wait | 0.05 | 0.81 |
| B: Go up. | `` | ignore | wait | 0.08 | 0.71 |
| B: Again. | `` | ignore | wait | 0.10 | 0.63 |
| B: Go back. | `` | ignore | wait | 0.09 | 0.64 |
| B: Let's go and check. | `` | ignore | wait | 0.08 | 0.51 |
| C: Otherwise, could you just describe | `` | ignore | wait | 0.12 | 0.82 |
| C: by hand? | `` | ignore | wait | 0.08 | 0.79 |
| C: With the the whiteboard? | `` | ignore | wait | 0.06 | 0.75 |
| B: So um the question well first of all what to control. | `` | ignore | wait | 0.18 | 0.80 |
| C: What do you mean by linear access then? | `` | ignore | wait | 0.05 | 0.82 |
| A: and there's a fourth one no? | `` | ignore | wait | 0.11 | 0.87 |
| A: So the better now for special navigation? | `` | ignore | wait | 0.17 | 0.85 |
| B: So if there are common parameters maybe we should put special buttons for that um | `` | ignore | wait | 0.14 | 0.67 |
| A: and and voice command did you uh | `` | ignore | wait | 0.09 | 0.79 |
| A: So that's uh that close your investigations? | `` | ignore | wait | 0.11 | 0.84 |
| A: Maybe we can have a look at the user requirements with | `` | ignore | wait | 0.08 | 0.65 |
| D: Um I dunno if you can open the | `` | ignore | wait | 0.10 | 0.73 |
| A: Messenger no? | `` | ignore | wait | 0.12 | 0.83 |
| A: In which folder? | `` | ignore | wait | 0.10 | 0.78 |
| B: Where did you put it? | `` | ignore | wait | 0.11 | 0.74 |
| A: Short-cut to AMI shared folder? | `` | ignore | wait | 0.09 | 0.81 |
| A: Maybe you can send it to me by email. | `` | ignore | wait | 0.04 | 0.75 |
| A: You send it? | `` | ignore | wait | 0.09 | 0.69 |
| D: It's participant one? | `` | ignore | wait | 0.15 | 0.76 |
| A: So maybe I can switch slides when you whenever you ask, | `` | ignore | wait | 0.07 | 0.65 |
| D: okay? | `` | ignore | wait | 0.11 | 0.71 |
| A: We can just keep doing that? | `` | ignore | wait | 0.13 | 0.87 |
| A: so fewer buttons maybe would be good? | `` | ignore | wait | 0.10 | 0.77 |
| B: But what kind of remote controls did you look at? | `` | ignore | wait | 0.14 | 0.79 |
| D: Sorry? | `` | ignore | wait | 0.16 | 0.62 |
| B: What kind of task was it? | `` | ignore | wait | 0.07 | 0.76 |
| B: It was a T_V_? | `` | ignore | wait | 0.05 | 0.71 |
| A: What is her other side? | `` | ignore | wait | 0.08 | 0.78 |
| A: Oh yeah? | `` | ignore | wait | 0.07 | 0.73 |
| D: and if they mm pay more for speech recognition in remote control | `` | ignore | wait | 0.10 | 0.79 |
| D: So maybe we we can have a speech recognition in. | `` | ignore | wait | 0.15 | 0.68 |
| D: Okay and if there is th the conclusion now. | `` | ignore | wait | 0.10 | 0.72 |
| D: I dunno if you see something else important or | `` | ignore | wait | 0.24 | 0.83 |
| A: What's your opinion? | `` | ignore | wait | 0.10 | 0.81 |
| C: Finish tonight. | `` | ignore | wait | 0.06 | 0.66 |
| A: Maybe you can go to the whiteboard if you have some drawings to do | `` | ignore | wait | 0.04 | 0.68 |
| A: Are you okay? | `` | ignore | wait | 0.06 | 0.81 |
| A: U_C_ is the central unit? | `` | ignore | wait | 0.12 | 0.85 |
| A: you s you speak about with voi voice control? | `` | ignore | wait | 0.13 | 0.85 |
| A: So do you have any idea of how long it would take to have voice recognition now? | `` | ignore | wait | 0.10 | 0.89 |
| A: Even if we have a L_C_D_ display? | `` | ignore | wait | 0.08 | 0.83 |
| A: So who think it would be good to go for uh like speech recognition? | `` | ignore | wait | 0.07 | 0.93 |
| C: so how many units should we sell to have a | `` | ignore | wait | 0.13 | 0.90 |
| B: How muc how much do you get how much do you if you buy one million units | `` | ignore | wait | 0.23 | 0.88 |
| B: We're gonna need chips right. | `` | ignore | wait | 0.07 | 0.86 |
| B: How much will it cost for one hundred thousand? | `` | ignore | wait | 0.09 | 0.87 |
| B: So you have any idea for a powerful one that has uh good enough for do speech recognition. | `` | ignore | wait | 0.26 | 0.90 |
| B: Yeah? | `` | ignore | wait | 0.08 | 0.61 |
| A: Maybe we can uh we can look at the new requirement I receive from the management board and discus discuss all  | `` | ignore | wait | 0.05 | 0.66 |
| C: I just had a question uh | `` | ignore | wait | 0.06 | 0.65 |
| C: do you want to continue with your presenta? | `` | ignore | wait | 0.07 | 0.82 |
| C: Do they say that this is difficult but for the same reason or do they have other reason? | `` | ignore | wait | 0.10 | 0.81 |
| C: and what about if we design a remote control which can be configure as you want? | `` | ignore | wait | 0.12 | 0.91 |
| B: All right? | `` | ignore | wait | 0.06 | 0.81 |
| B: So will you add with the channel keys, right? | `` | ignore | wait | 0.16 | 0.75 |
| A: and which button do we need which function do we want etcetera. | `` | ignore | wait | 0.08 | 0.84 |
| A: no? | `` | ignore | wait | 0.07 | 0.85 |
| A: and what el what function do you see | `` | ignore | wait | 0.09 | 0.88 |
| A: in addition to that? | `` | ignore | wait | 0.07 | 0.85 |
| A: And that's all? | `` | ignore | wait | 0.10 | 0.85 |
| A: Maybe we can include that also. Previous previous channel button. | `` | ignore | wait | 0.09 | 0.66 |
| A: I I talk about that, yeah? | `` | ignore | wait | 0.09 | 0.79 |
| B: How should they how should we implement that? | `` | ignore | wait | 0.09 | 0.90 |
| B: Because uh could be numerical only or could be also incremental. | `` | ignore | wait | 0.06 | 0.58 |
| A: We go faster? | `` | ignore | wait | 0.06 | 0.86 |
| A: Maybe we should have also a digit button | `` | ignore | wait | 0.07 | 0.57 |
| B: Maybe we should have a complete keyboard and just type console commands. | `` | ignore | wait | 0.10 | 0.51 |
| A: Maybe we have also to have digits or only incremental. | `` | ignore | wait | 0.15 | 0.77 |
| B: No? | `` | ignore | wait | 0.21 | 0.74 |
| A: and do we put an L_C_D_ display? | `` | ignore | wait | 0.07 | 0.89 |
| A: So no L_C_D_? | `` | ignore | wait | 0.07 | 0.80 |
| A: Uh maybe for next meeting uh send me your presentation before by email so that we can see them uh altogether. | `` | ignore | wait | 0.07 | 0.78 |
| B: What is the folder that you put yours in? | `` | ignore | wait | 0.11 | 0.74 |
| B: And did it it did work? | `` | ignore | wait | 0.27 | 0.79 |
| B: what is your email? | `` | ignore | wait | 0.06 | 0.72 |
| A: Okay? | `` | ignore | wait | 0.06 | 0.66 |
| B: How about uh management or something. | `` | ignore | wait | 0.06 | 0.85 |
| A: So each of you will uh show us the various investigation they've done during uh previous uh hours. | `` | ignore | wait | 0.03 | 0.74 |
| A: So maybe we can start with uh industrial design. | `` | ignore | wait | 0.04 | 0.56 |
| B: Uh, I_D_ you want? | `` | ignore | wait | 0.09 | 0.72 |
| B: And I think we if we could just talk about that if we really need a wheel sensor or if we can not if if we cou | `` | ignore | wait | 0.09 | 0.87 |
| A: But is it a significant price on the whole remote control? | `` | ignore | wait | 0.08 | 0.87 |
| A: So will will will this with uh including all possible things, so buttons, wheel and the chip, be uh lower than | `` | ignore | wait | 0.08 | 0.88 |
| C: Did you receive the email about the voice recognition? | `` | ignore | wait | 0.09 | 0.81 |
| C: No? | `` | ignore | wait | 0.05 | 0.70 |
| A: And could it be adapted? | `` | ignore | wait | 0.09 | 0.86 |
| A: Okay and there can uh recognize some commands and stuff? | `` | ignore | wait | 0.13 | 0.82 |
| B: and if we could reduce that. | `` | ignore | wait | 0.14 | 0.69 |
| C: I have a question about that actually. | `` | ignore | wait | 0.08 | 0.62 |
| C: Um, what is the purpose of the light? | `` | ignore | wait | 0.07 | 0.84 |
| A: You can easily find the button in the dark or so? | `` | ignore | wait | 0.05 | 0.81 |
| C: Yeah but is going to be always turned on, the light? | `` | ignore | wait | 0.11 | 0.84 |
| A: no? | `` | ignore | wait | 0.11 | 0.70 |
| C: but you need another sensor for that, right? | `` | ignore | wait | 0.12 | 0.85 |
| A: But it can be uh battery consuming, no? | `` | ignore | wait | 0.09 | 0.86 |
| A: To have the light always on? | `` | ignore | wait | 0.09 | 0.82 |
| C: just move to the next slide. | `` | ignore | wait | 0.23 | 0.80 |
| C: So basically want very simple, right? | `` | ignore | wait | 0.08 | 0.81 |
| A: And also does it uh fit well in hand? | `` | ignore | wait | 0.11 | 0.86 |
| C: so go to the next page, | `` | ignore | wait | 0.15 | 0.69 |
| C: Uh you just need to put the channel numbers somewhere a bit out of the way. | `` | ignore | wait | 0.13 | 0.67 |
| A: For designer of user interface? | `` | ignore | wait | 0.06 | 0.84 |
| A: or we can move to the next part, maybe, and discuss afterwards? | `` | ignore | wait | 0.05 | 0.85 |
| D: Okay, I can go? | `` | ignore | wait | 0.43 | 0.82 |
| D: Can I? | `` | ignore | wait | 0.43 | 0.83 |
| D: So, are things we are we have uh speak about before. | `` | ignore | wait | 0.16 | 0.81 |
| D: And um so you you can go | `` | ignore | wait | 0.14 | 0.55 |
| D: So, maybe if our remote control have to be a fruit form or vegetable form | `` | ignore | wait | 0.08 | 0.51 |
| D: Uh I don't know which material can be spongy, | `` | ignore | wait | 0.12 | 0.66 |
| C: it it would work, right? | `` | ignore | wait | 0.08 | 0.89 |
| A: uh sorry? | `` | ignore | wait | 0.09 | 0.75 |
| A: Before? | `` | ignore | wait | 0.09 | 0.76 |
| A: Has it? | `` | ignore | wait | 0.14 | 0.80 |
| C: How do we make it look cool is the question. | `` | ignore | wait | 0.12 | 0.91 |
| A: Cool, fancy? | `` | ignore | wait | 0.05 | 0.86 |
| C: Is there any fruit that is spongy? | `` | ignore | wait | 0.12 | 0.94 |
| B: And for maybe look and feel, what about a a piece of ice, | `` | ignore | wait | 0.16 | 0.89 |
| B: with blue L_E_D_ inside? | `` | ignore | wait | 0.12 | 0.80 |
| A: wit uh any others idea you have. | `` | ignore | wait | 0.06 | 0.88 |
| A: What kind of fr fruit would you like to to control your T_V_ with? | `` | ignore | wait | 0.07 | 0.90 |
| C: no? | `` | ignore | wait | 0.09 | 0.79 |
| A: Maybe we can keep the banana. | `` | ignore | wait | 0.09 | 0.56 |
| C: Now who are recording this meeting? | `` | ignore | wait | 0.18 | 0.94 |
| B: So we will just use a a standard battery? | `` | ignore | wait | 0.06 | 0.87 |
| B: Uh what do you mean by case? | `` | ignore | wait | 0.09 | 0.78 |
| C: right? | `` | ignore | wait | 0.06 | 0.78 |
| C: You think it's possible? | `` | ignore | wait | 0.07 | 0.60 |
| B: Button, where do we want some buttons? | `` | ignore | wait | 0.22 | 0.89 |
| C: right? | `` | ignore | wait | 0.06 | 0.84 |
| C: This for the wheel and then this for the buttons? | `` | ignore | wait | 0.19 | 0.85 |
| C: Should have the two sides. | `` | ignore | wait | 0.10 | 0.51 |
| A: Yeah? | `` | ignore | wait | 0.15 | 0.74 |
| A: So have the final uh look and feel design according to the decision. | `` | ignore | wait | 0.05 | 0.71 |
| A: And have the the user interface design and uh then evaluate the prodyuc the product. | `` | ignore | wait | 0.04 | 0.52 |
| A: do you need to add anything? | `` | ignore | wait | 0.09 | 0.85 |
| A: You feel okay? | `` | ignore | wait | 0.08 | 0.73 |
| A: You feel uh free to express what you want to say? | `` | ignore | wait | 0.07 | 0.67 |
| A: You don't feel too constrained? | `` | ignore | wait | 0.07 | 0.55 |
| A: You don't feel free to answer this? | `` | ignore | wait | 0.06 | 0.50 |
| C: What's your talk? | `` | ignore | wait | 0.23 | 0.77 |
| C: Um, so you're participant two? | `` | ignore | wait | 0.08 | 0.72 |
| C: did you save your presentation? | `` | ignore | wait | 0.09 | 0.83 |
| C: Isn't that technical functions? | `` | ignore | wait | 0.11 | 0.85 |
| D: Um so move to the next slide. | `` | ignore | wait | 0.08 | 0.75 |
| D: So how can we um design a user interface with so sa with so many sophisticated functions? | `` | ignore | wait | 0.07 | 0.92 |
| D: Um, let's move to next slide. | `` | ignore | wait | 0.07 | 0.72 |
| D: move to next s slide. | `` | ignore | wait | 0.24 | 0.81 |
| C: So you propose to to have the | `` | ignore | wait | 0.05 | 0.52 |
| B: To merge the two system huh. | `` | ignore | wait | 0.11 | 0.79 |
| C: You mean this one? | `` | ignore | wait | 0.16 | 0.75 |
| C: you have to learn the manual before using this remote control, I suppose. | `` | ignore | wait | 0.07 | 0.78 |
| B: you maybe you have some international standards, | `` | ignore | wait | 0.08 | 0.78 |
| C: you mean for the yeah pic pictograms or things like that? | `` | ignore | wait | 0.08 | 0.75 |
| C: Go on, go back | `` | ignore | wait | 0.09 | 0.64 |
| B: but the question is how to merge you know the Google system to the system, alright. | `` | ignore | wait | 0.09 | 0.79 |
| C: you will propose us something which is yeah so powerful and easy to use. | `` | ignore | wait | 0.22 | 0.65 |
| C: So you mean that infrared control is a cheap technology? | `` | ignore | wait | 0.08 | 0.77 |
| C: Do y you know the requirements for the remote control? | `` | ignore | wait | 0.11 | 0.89 |
| A: What the cost is? | `` | ignore | wait | 0.10 | 0.85 |
| B: You can move to the next slide, so. | `` | ignore | wait | 0.11 | 0.73 |
| B: You can go to the next slide. | `` | ignore | wait | 0.07 | 0.75 |
| C: What is this? | `` | ignore | wait | 0.10 | 0.89 |
| B: and you know because you f the b the the battery problem can hold you know will you use a battery or the a wir | `` | ignore | wait | 0.07 | 0.81 |
| B: if you have some question I didn't answer? | `` | ignore | wait | 0.12 | 0.88 |
| A: What's the average price of this technology then? | `` | ignore | wait | 0.12 | 0.89 |
| D: So what, the wireless remote control? | `` | ignore | wait | 0.10 | 0.79 |
| D: There's a wire with remote control? | `` | ignore | wait | 0.06 | 0.84 |
| B: you have to decide how how you will you know, put some energy inside, | `` | ignore | wait | 0.07 | 0.52 |
| C: So you think that uh a cable between the remote control and the T_V_ won't be a good idea. | `` | ignore | wait | 0.07 | 0.74 |
| C: but as Industrial Designer, do you think that it will be feasible to have uh linked or to have link between th | `` | ignore | wait | 0.12 | 0.80 |
| C: Do you think it will be cheaper? | `` | ignore | wait | 0.10 | 0.85 |
| C: Could you answer please? | `` | ignore | wait | 0.09 | 0.80 |
| A: The wire? | `` | ignore | wait | 0.06 | 0.78 |
| C: Mayb maybe you have just to to kind of research | `` | ignore | wait | 0.06 | 0.55 |
| C: just think of um the usability. | `` | ignore | wait | 0.05 | 0.68 |
| D: Design a wireless remote control. | `` | ignore | wait | 0.12 | 0.83 |
| C: Just think of the problem. | `` | ignore | wait | 0.06 | 0.78 |
| C: If when you have wireless remote control and if you lose it? | `` | ignore | wait | 0.07 | 0.91 |
| A: yeah? | `` | ignore | wait | 0.17 | 0.65 |
| A: if the user would be happy to have something or something else uh. | `` | ignore | wait | 0.07 | 0.63 |
| A: so could you go to next slide. | `` | ignore | wait | 0.12 | 0.75 |
| C: You mean the loo the look, the outside? | `` | ignore | wait | 0.05 | 0.69 |
| A: Could you go next slide? | `` | ignore | wait | 0.17 | 0.83 |
| C: What is R_S_I_? | `` | ignore | wait | 0.20 | 0.88 |
| A: Okay? | `` | ignore | wait | 0.07 | 0.75 |
| C: And just to have uh an idea, do you think you as the User Interface Designer to would it be possible to have l | `` | ignore | wait | 0.10 | 0.53 |
| C: but do you think it will be easy to use? | `` | ignore | wait | 0.06 | 0.64 |
| D: But what I'm not so sure is about how to make the remote control look funny look fancy, not funny. | `` | ignore | wait | 0.13 | 0.81 |
| D: Maybe we can have di di we can have uh several options, | `` | ignore | wait | 0.04 | 0.50 |
| C: is it okay for your presentation? | `` | ignore | wait | 0.06 | 0.78 |
| C: Nothing else to to add? | `` | ignore | wait | 0.05 | 0.85 |
| A: just yeah. If we would if we could remember like, not too many buttons and make it look fancy, I think it woul | `` | ignore | wait | 0.07 | 0.60 |
| C: so you will have to take care of it of it in your thinking, in your designing of the remote control. | `` | ignore | wait | 0.17 | 0.60 |
| C: you will have to think about it in your in in the design of your remote control, | `` | ignore | wait | 0.10 | 0.52 |
| C: Is it okay? | `` | ignore | wait | 0.13 | 0.86 |
| C: But uh that's your your job to find something mm matches. | `` | ignore | wait | 0.14 | 0.66 |
| B: 'cause what I'm thinking is how will you will connect the T_V_ to internet, so. | `` | ignore | wait | 0.09 | 0.82 |
| B: but this this mean that your T_V_ would be able to, you know, connect to internet, you know, surf the web. | `` | ignore | wait | 0.18 | 0.53 |
| C: So everybody is okay with the new requirements? | `` | ignore | wait | 0.04 | 0.93 |
| D: As as for the colour, what what do you think? | `` | ignore | wait | 0.07 | 0.86 |
| B: Yellow? | `` | ignore | wait | 0.04 | 0.77 |
| B: Do you think that people like the colour yellow? | `` | ignore | wait | 0.07 | 0.85 |
| D: Yellow? T_V_ remote control? | `` | ignore | wait | 0.05 | 0.76 |
| C: Maybe you can change the colour, | `` | ignore | wait | 0.08 | 0.77 |
| B: I think if you have you know th like a yellow ribbon here is the double R_. Or should be. | `` | ignore | wait | 0.11 | 0.61 |
| C: It's okay? | `` | ignore | wait | 0.11 | 0.84 |
| A: Regarding the first line, what So we're just expecting no more use of the teletext. | `` | ignore | wait | 0.09 | 0.76 |
| B: But I dunno, but why, | `` | ignore | wait | 0.13 | 0.83 |
| C: It's okay? | `` | ignore | wait | 0.08 | 0.84 |
| B: So, ready? | `` | ignore | wait | 0.12 | 0.82 |
| D: so whe where is the remote control? | `` | ignore | wait | 0.07 | 0.85 |
| C: Where? | `` | ignore | wait | 0.12 | 0.85 |
| B: and maybe we can discuss everything. | `` | ignore | wait | 0.04 | 0.51 |
| D: What slides? | `` | ignore | wait | 0.06 | 0.88 |
| A: keep on speaking. | `` | ignore | wait | 0.09 | 0.69 |
| A: but don't touch don't destroy your prototype. | `` | ignore | wait | 0.04 | 0.55 |
| C: You c can can you can see the the shape of the buttons n is a mushroom, so | `` | ignore | wait | 0.09 | 0.61 |
| B: Really? | `` | ignore | wait | 0.07 | 0.82 |
| A: Next slide. | `` | ignore | wait | 0.17 | 0.63 |
| C: So where's the battery battery? | `` | ignore | wait | 0.07 | 0.89 |
| C: Here? | `` | ignore | wait | 0.24 | 0.83 |
| A: And where is the solar solar cell? | `` | ignore | wait | 0.09 | 0.91 |
| A: Where is the solar cell? | `` | ignore | wait | 0.09 | 0.92 |
| A: Do you think it won't be It won't cris increase the price? | `` | ignore | wait | 0.14 | 0.87 |
| A: so, mister money, what's your opinion according to this remote control? | `` | ignore | wait | 0.14 | 0.52 |
| D: Do we have a fancy look and feel, according to you? | `` | ignore | wait | 0.14 | 0.87 |
| D: but is it really | `` | ignore | wait | 0.06 | 0.79 |
| C: So it depend on how d do you define fancy. | `` | ignore | wait | 0.05 | 0.55 |
| B: Is it really fancy? | `` | ignore | wait | 0.06 | 0.88 |
| B: Do Don't do that, please. | `` | ignore | wait | 0.08 | 0.67 |
| A: It would be bet more like a lemon? | `` | ignore | wait | 0.09 | 0.84 |
| A: And you know, you have the finger here, with the buttons? | `` | ignore | wait | 0.09 | 0.78 |
| A: What's the use for that? | `` | ignore | wait | 0.11 | 0.88 |
| A: And where is the voice recognition? | `` | ignore | wait | 0.20 | 0.90 |
| A: Is it better like that? | `` | ignore | wait | 0.12 | 0.84 |
| B: The colour, is the colour acceptable? | `` | ignore | wait | 0.20 | 0.88 |
| B: So the shape now. | `` | ignore | wait | 0.11 | 0.61 |
| B: It's too much red? | `` | ignore | wait | 0.05 | 0.73 |
| B: In the basement? | `` | ignore | wait | 0.06 | 0.83 |
| D: Right. So, from one to seven? | `` | ignore | wait | 0.08 | 0.81 |
| A: Seven is the ma the maximum? | `` | ignore | wait | 0.07 | 0.83 |
| D: Three? | `` | ignore | wait | 0.09 | 0.71 |
| A: Isn't it bitter like that? | `` | ignore | wait | 0.06 | 0.84 |
| B: Is it easy to use? | `` | ignore | wait | 0.09 | 0.87 |
| A: Feasible? | `` | ignore | wait | 0.08 | 0.82 |
| A: You said previously that you there's um microphone inside an | `` | ignore | wait | 0.11 | 0.57 |
| A: there's the technology inside that recognise simple vocal comments? | `` | ignore | wait | 0.12 | 0.86 |
| A: And you can turn it so maybe it's techno technologically innov innovative? | `` | ignore | wait | 0.18 | 0.59 |
| A: Maybe two? | `` | ignore | wait | 0.12 | 0.76 |
| D: So using the same scale, two? | `` | ignore | wait | 0.08 | 0.78 |
| A: Two? | `` | ignore | wait | 0.08 | 0.78 |
| A: . You agree? | `` | ignore | wait | 0.09 | 0.82 |
| A: isn't it? | `` | ignore | wait | 0.06 | 0.79 |
| D: is it easy to use? | `` | ignore | wait | 0.14 | 0.89 |
| D: can you can you just re explain me the | `` | ignore | wait | 0.18 | 0.87 |
| D: Please. | `` | ignore | wait | 0.12 | 0.79 |
| D: Yeah but how how intuitive is it to turn things to change channels? | `` | ignore | wait | 0.11 | 0.84 |
| A: and you can turn like that to change the channel? | `` | ignore | wait | 0.11 | 0.83 |
| D: How can you go directly to twenty, for example? | `` | ignore | wait | 0.14 | 0.89 |
| D: But I mean if you're fro from two? | `` | ignore | wait | 0.05 | 0.69 |
| C: So change. | `` | ignore | wait | 0.07 | 0.55 |
| C: So you got how many degree you you it | `` | ignore | wait | 0.08 | 0.81 |
| D: How d how do you know this angle is th is the correct one? | `` | ignore | wait | 0.06 | 0.87 |
| A: Just go through all the channels and maybe stop if there is something interesting? | `` | ignore | wait | 0.11 | 0.85 |
| A: yeah, what's what's this cherry? | `` | ignore | wait | 0.10 | 0.81 |
| C: You ca you can turn this. | `` | ignore | wait | 0.14 | 0.63 |
| B: S But I di I didn't see where the t f the turn off t turn on turn off button so much activates | `` | ignore | wait | 0.09 | 0.77 |
| A: W that why we have the solar ti yeah. | `` | ignore | wait | 0.08 | 0.67 |
| D: So, which number? | `` | ignore | wait | 0.12 | 0.85 |
| A: Do you agree? | `` | ignore | wait | 0.09 | 0.85 |
| A: Three? | `` | ignore | wait | 0.06 | 0.75 |
| D: So reasonably, is four, is one? | `` | ignore | wait | 0.07 | 0.81 |
| B: Maybe you can vote to see how many everybody gives | `` | ignore | wait | 0.08 | 0.85 |
| B: and no and just take the mean. | `` | ignore | wait | 0.10 | 0.70 |
| A: And what's your opinion? | `` | ignore | wait | 0.19 | 0.79 |
| B: Will you give four? | `` | ignore | wait | 0.19 | 0.72 |
| B: Five? | `` | ignore | wait | 0.05 | 0.61 |
| C: you compare with traditional uh um tr traditional controller? | `` | ignore | wait | 0.07 | 0.86 |
| C: But in the traditional controller, how do how can you control the scale? | `` | ignore | wait | 0.07 | 0.90 |
| B: Are there some buttons? Okay. | `` | ignore | wait | 0.07 | 0.80 |
| D: But this this has to stay on the table, right? | `` | ignore | wait | 0.13 | 0.83 |
| D: So, average? | `` | ignore | wait | 0.07 | 0.84 |
| A: So, th the project is accepted? | `` | ignore | wait | 0.07 | 0.89 |
| A: If you re we really want to have a fruitful remote control. | `` | ignore | wait | 0.05 | 0.57 |
| A: we need to calculate the production cost. | `` | ignore | wait | 0.06 | 0.52 |
| A: We have battery, right? | `` | ignore | wait | 0.08 | 0.89 |
| A: Um, how many do y do you need, solar cells? | `` | ignore | wait | 0.06 | 0.87 |
| A: Do you think one would be enough, or such as | `` | ignore | wait | 0.07 | 0.85 |
| A: as number of branches? | `` | ignore | wait | 0.08 | 0.73 |
| A: Single simple chip on print? | `` | ignore | wait | 0.09 | 0.79 |
| A: Just one would be necessary? | `` | ignore | wait | 0.08 | 0.83 |
| A: One? | `` | ignore | wait | 0.08 | 0.73 |
| A: One? | `` | ignore | wait | 0.08 | 0.64 |
| A: just keep on going, just to have an idea. | `` | ignore | wait | 0.08 | 0.68 |
| B: Is Yes a wooden pl I and that's | `` | ignore | wait | 0.08 | 0.65 |
| A: yeah, but what what about case? | `` | ignore | wait | 0.06 | 0.88 |
| A: One? | `` | ignore | wait | 0.08 | 0.83 |
| A: Uh do we need special colour? | `` | ignore | wait | 0.09 | 0.90 |
| A: Y maybe, two? | `` | ignore | wait | 0.07 | 0.80 |
| A: Push button. | `` | ignore | wait | 0.08 | 0.53 |
| B: Five? | `` | ignore | wait | 0.13 | 0.86 |
| A: Scroll wheel. | `` | ignore | wait | 0.08 | 0.50 |
| A: So, no button supplements? | `` | ignore | wait | 0.08 | 0.88 |
| A: Maybe if w t if suppose if we change and we g put just one? | `` | ignore | wait | 0.06 | 0.78 |
| A: Has it changed. | `` | ignore | wait | 0.07 | 0.84 |
| A: no? | `` | ignore | wait | 0.08 | 0.78 |
| A: . So we'll we have only one? | `` | ignore | wait | 0.09 | 0.83 |
| D: Okay, so what's the bottleneck? | `` | ignore | wait | 0.07 | 0.90 |
| C: How about we change the sale? | `` | ignore | wait | 0.04 | 0.88 |
| A: Maybe don't bat no battery, only solar cells. | `` | ignore | wait | 0.08 | 0.65 |
| B: Two? | `` | ignore | wait | 0.07 | 0.82 |
| C: Could we have look at the p the the prod the p the cost? | `` | ignore | wait | 0.07 | 0.89 |
| C: Which part is the most expensive part? | `` | ignore | wait | 0.07 | 0.90 |
| B: The solar cells, r is i is it? | `` | ignore | wait | 0.08 | 0.78 |
| B: So what are we going to do with this project evaluation? | `` | ignore | wait | 0.09 | 0.92 |
| A: So did you enjoy your clay modelling? | `` | ignore | wait | 0.07 | 0.83 |
| A: Yeah? Was it a nice way to create your remote control? | `` | ignore | wait | 0.05 | 0.69 |
| C: Yeah, | `` | ignore | respond | 0.81 | 0.07 |
| A: And for the marketing guy? | `` | ignore | wait | 0.05 | 0.76 |
| D: Uh tha that was good but we should have more brainstorming like meetings, maybe. | `` | ignore | wait | 0.05 | 0.64 |
| A: And new ideas about new products, | `` | ignore | wait | 0.06 | 0.64 |
| A: Squared? | `` | ignore | wait | 0.07 | 0.83 |
| A: do you think you can celebrate your creation? | `` | ignore | wait | 0.07 | 0.84 |
| A: Maybe what you can do a test. Put it outside, and if bees come, it's really fruit. | `` | ignore | wait | 0.06 | 0.74 |
| A: But don't put sugar in it, it's not working. | `` | ignore | wait | 0.06 | 0.60 |
| C: So we have give him give it a cute name. | `` | ignore | wait | 0.05 | 0.76 |
| D: Yeah, but just flying saucer, or | `` | ignore | wait | 0.07 | 0.58 |
| A: Will you buy one? | `` | ignore | wait | 0.09 | 0.88 |
| C: Traditional one? | `` | ignore | wait | 0.12 | 0.77 |
| C: So this one and this one. What do you choose? | `` | ignore | wait | 0.08 | 0.80 |
| C: What do you choose? | `` | ignore | wait | 0.09 | 0.83 |
| C: So buy one. | `` | ignore | wait | 0.06 | 0.69 |
| B: S so who is going to take the remote control? | `` | ignore | wait | 0.04 | 0.93 |
| A: Um uh we want to know to at the end to know the new project's requirement | `` | ignore | wait | 0.05 | 0.78 |
| A: we need uh to know the the user uh needs | `` | ignore | wait | 0.05 | 0.57 |
| A: we want to know how it going to work | `` | ignore | wait | 0.08 | 0.83 |
| A: how to to design this uh this | `` | ignore | wait | 0.12 | 0.82 |
| D: Who starts? | `` | ignore | wait | 0.09 | 0.90 |
| D: next please. | `` | ignore | wait | 0.10 | 0.67 |
| D: what I suggest is that uh instead of deciding ourself what what could be and what should be a good uh remote c | `` | ignore | wait | 0.07 | 0.50 |
| D: how they feel about w the current remote controls, | `` | ignore | wait | 0.05 | 0.50 |
| D: Don't forget about that. | `` | ignore | wait | 0.10 | 0.53 |
| D: And next please. | `` | ignore | wait | 0.09 | 0.61 |
| D: Um next please. | `` | ignore | wait | 0.09 | 0.66 |
| D: Maybe if we have something where we could ask the remote control please, where are you? | `` | ignore | wait | 0.07 | 0.80 |
| A: Why not? | `` | ignore | wait | 0.09 | 0.85 |
| D: But why not? Yeah. | `` | ignore | wait | 0.07 | 0.72 |
| D: but uh I don't remember what is R_S_I_. | `` | ignore | wait | 0.11 | 0.76 |
| D: nobody has any idea about that? | `` | ignore | wait | 0.10 | 0.94 |
| B: But twenty six percent, do you know | `` | ignore | wait | 0.07 | 0.74 |
| D: what else do I have? | `` | ignore | wait | 0.09 | 0.85 |
| D: Next slide? | `` | ignore | wait | 0.08 | 0.84 |
| D: but what is important | `` | ignore | wait | 0.08 | 0.59 |
| D: if if there are good reason not to put teletext it's okay | `` | ignore | wait | 0.10 | 0.50 |
| D: and uh then we can ask uh ourself uh what people don't have that may be useful. | `` | ignore | wait | 0.06 | 0.57 |
| D: next slide. | `` | ignore | wait | 0.09 | 0.69 |
| D: So now it really depends on the kind of uh targeting uh wha who are we targeting with this remote control? | `` | ignore | wait | 0.07 | 0.88 |
| D: if you have any question? | `` | ignore | wait | 0.07 | 0.87 |
| D: yeah? | `` | ignore | wait | 0.05 | 0.50 |
| B: should we aim at the young people or not? | `` | ignore | wait | 0.06 | 0.71 |
| D: 'Kay? | `` | ignore | wait | 0.09 | 0.61 |
| D: So I think it's you, huh? | `` | ignore | wait | 0.27 | 0.65 |
| B: So next slide please. | `` | ignore | wait | 0.16 | 0.78 |
| B: So, make a click, please. | `` | ignore | wait | 0.15 | 0.79 |
| B: and please make a click, | `` | ignore | wait | 0.14 | 0.80 |
| B: which one would you prefer? | `` | ignore | wait | 0.19 | 0.90 |
| B: Be simple. Be simple | `` | ignore | wait | 0.07 | 0.70 |
| B: So be simple. | `` | ignore | wait | 0.08 | 0.57 |
| B: When you go to the sofa, take your control | `` | ignore | wait | 0.07 | 0.64 |
| D: And when does it turn off? | `` | ignore | wait | 0.17 | 0.90 |
| B: Suppose you set u you set up some volume | `` | ignore | wait | 0.08 | 0.51 |
| D: wha what is the use usefulness of the screen? | `` | ignore | wait | 0.08 | 0.90 |
| D: Uh is it a touch screen by the way? | `` | ignore | wait | 0.08 | 0.88 |
| B: yeah? | `` | ignore | wait | 0.13 | 0.74 |
| B: so you want to use it for your hi-fi system. | `` | ignore | wait | 0.13 | 0.62 |
| B: You want to change tracks | `` | ignore | wait | 0.11 | 0.71 |
| A: and then maybe m make it more generalised yeah. | `` | ignore | wait | 0.06 | 0.52 |
| D: for instance if I want to go to directly to channel twenty five, how would I do can I do that with this? | `` | ignore | wait | 0.17 | 0.91 |
| D: Or is it? | `` | ignore | wait | 0.10 | 0.74 |
| B: right? | `` | ignore | wait | 0.05 | 0.69 |
| D: Go to channel twenty five. | `` | ignore | wait | 0.11 | 0.76 |
| B: Or say this can be back. | `` | ignore | wait | 0.09 | 0.63 |
| C: uh if you want to go for a universal then we ought to limit for functions for each of our devices. | `` | ignore | wait | 0.08 | 0.59 |
| B: Could we carry out some research if we w really need this, | `` | ignore | wait | 0.07 | 0.89 |
| B: like how many people really need to go to channel number twenty five and then to sixty four? | `` | ignore | wait | 0.06 | 0.88 |
| B: Alright? | `` | ignore | wait | 0.06 | 0.68 |
| A: Uh you're finish? | `` | ignore | wait | 0.06 | 0.79 |
| C: And since I also want to know feedback from our Marketing Expert and User Interface, | `` | ignore | wait | 0.05 | 0.51 |
| C: so if you want to add some more components we can incorporate them. | `` | ignore | wait | 0.10 | 0.78 |
| A: Mm-hmm. And from from the discussion we had do you can you make it on the whiteboard, or mm. | `` | ignore | wait | 0.08 | 0.79 |
| A: And what about the price of this component? | `` | ignore | wait | 0.11 | 0.89 |
| B: Did you consider the r gest uh gesture recognition? | `` | ignore | wait | 0.10 | 0.85 |
| D: no? | `` | ignore | wait | 0.09 | 0.72 |
| A: what about the idea of automatic on off on the button, yeah. | `` | ignore | wait | 0.08 | 0.87 |
| B: Mm why? | `` | ignore | wait | 0.41 | 0.78 |
| D: Sh should we target a a user personalised uh uh remote control? | `` | ignore | wait | 0.08 | 0.90 |
| A: Wouldn't that make uh arguments? | `` | ignore | wait | 0.07 | 0.86 |
| A: I want uh | `` | ignore | wait | 0.18 | 0.60 |
| A: You have mm something else to say? Uh. | `` | ignore | wait | 0.07 | 0.80 |
| C: Can you just | `` | ignore | wait | 0.21 | 0.81 |
| A: you will focus on the component concept um | `` | ignore | wait | 0.04 | 0.51 |
| A: And we have um maybe we have to we say, only for T_V_, not teletext? | `` | ignore | wait | 0.11 | 0.85 |
| A: do you see something else? | `` | ignore | wait | 0.08 | 0.85 |
| B: Uh, should it be equipped with the uh, with uh speakers? | `` | ignore | wait | 0.16 | 0.90 |
| B: and it answers is I'm here? Or | `` | ignore | wait | 0.13 | 0.82 |
| B: Just beeps? | `` | ignore | wait | 0.11 | 0.73 |
| A: Or maybe you want to phone him. | `` | ignore | wait | 0.08 | 0.64 |
| A: yeah? | `` | ignore | wait | 0.21 | 0.74 |
| D: You can clap. Can you? | `` | ignore | wait | 0.07 | 0.61 |
| A: What about people without hand? | `` | ignore | wait | 0.09 | 0.93 |
| D: With only one hand? | `` | ignore | wait | 0.11 | 0.84 |
| C: we need to think about more how to incorporate it. | `` | ignore | wait | 0.05 | 0.57 |
| B: Just don't interfere with other devices like | `` | ignore | wait | 0.07 | 0.53 |
| D: Think about it. | `` | ignore | wait | 0.08 | 0.73 |
| D: we're done? | `` | ignore | wait | 0.13 | 0.89 |
| A: let's go to lunch. | `` | ignore | wait | 0.09 | 0.68 |
| B: And chocolate? | `` | ignore | wait | 0.06 | 0.85 |
| A: Okay. And you have some slides then? | `` | ignore | wait | 0.03 | 0.81 |
| A: Uh so in which uh | `` | ignore | wait | 0.05 | 0.74 |
| B: Please, next slide. | `` | ignore | wait | 0.14 | 0.79 |
| A: MASA? | `` | ignore | wait | 0.12 | 0.72 |
| B: S please, next slide. | `` | ignore | wait | 0.20 | 0.59 |
| B: so please press something. | `` | ignore | wait | 0.11 | 0.81 |
| B: Please press it. | `` | ignore | wait | 0.11 | 0.79 |
| D: Can I? | `` | ignore | wait | 0.10 | 0.83 |
| A: What do you say? | `` | ignore | wait | 0.12 | 0.85 |
| B: You must say it. | `` | ignore | wait | 0.09 | 0.63 |
| B: , please next slide. | `` | ignore | wait | 0.17 | 0.75 |
| B: You can have a look at it, | `` | ignore | wait | 0.07 | 0.50 |
| C: You can just say, where is my remote control. | `` | ignore | wait | 0.16 | 0.54 |
| D: You mean we can change the colour uh of th | `` | ignore | wait | 0.08 | 0.77 |
| A: That's for the L_C_D_ or for the titanium? | `` | ignore | wait | 0.09 | 0.80 |
| A: wh what are the strawberries for? | `` | ignore | wait | 0.12 | 0.87 |
| D: What do you think? | `` | ignore | wait | 0.13 | 0.85 |
| C: So, if you are vegetarian or you have any options, please let us know. | `` | ignore | wait | 0.06 | 0.91 |
| B: Let's make a party first maybe. | `` | ignore | wait | 0.06 | 0.69 |
| A: W Who is the five uh fifty millions we first make a party in? | `` | ignore | wait | 0.05 | 0.85 |
| C: Yeah, then we can have how much for how money is left. | `` | ignore | wait | 0.06 | 0.72 |
| D: Yeah. So, evaluation please. | `` | ignore | wait | 0.23 | 0.81 |
| D: and um, I think, we now need altogether to try to evaluate it to see if it makes sense to do it, if it fulfils | `` | ignore | wait | 0.07 | 0.53 |
| D: next slide, please. | `` | ignore | wait | 0.25 | 0.80 |
| D: and together try to evaluate this according to this criterion and from one to seven. | `` | ignore | wait | 0.05 | 0.68 |
| D: So, maybe we can have a look at the criteria? | `` | ignore | wait | 0.07 | 0.90 |
| D: so let's vote. | `` | ignore | wait | 0.07 | 0.80 |
| D: what do you think, is it fancy? | `` | ignore | wait | 0.12 | 0.88 |
| D: Or have you ever seen something like that? | `` | ignore | wait | 0.12 | 0.84 |
| D: What do you think? | `` | ignore | wait | 0.22 | 0.84 |
| A: Uh what do you think? | `` | ignore | wait | 0.12 | 0.83 |
| B: Feel the weight. | `` | ignore | wait | 0.10 | 0.64 |
| D: What do you think? | `` | ignore | wait | 0.12 | 0.86 |
| D: Two? | `` | ignore | wait | 0.28 | 0.73 |
| D: So, what about technology? | `` | ignore | wait | 0.07 | 0.88 |
| D: Do you think it makes sense that it's going to live again? | `` | ignore | wait | 0.17 | 0.88 |
| D: Not at all? | `` | ignore | wait | 0.07 | 0.77 |
| D: Yeah, that does make sense, yeah? | `` | ignore | wait | 0.08 | 0.77 |
| C: Useful? | `` | ignore | wait | 0.13 | 0.84 |
| D: Well, so the question is does it have uh the minimum requirement of re remote control? | `` | ignore | wait | 0.15 | 0.88 |
| A: What is uh next, please? | `` | ignore | wait | 0.10 | 0.84 |
| A: And you can uh do di two sites? | `` | ignore | wait | 0.11 | 0.85 |
| D: It's much longer than that that being two two five, no? | `` | ignore | wait | 0.07 | 0.80 |
| D: Don't you think so? | `` | ignore | wait | 0.06 | 0.76 |
| D: So what do you think for it, usefulness? | `` | ignore | wait | 0.17 | 0.87 |
| A: Yeah. And which what is that? | `` | ignore | wait | 0.08 | 0.83 |
| D: Two or three? | `` | ignore | wait | 0.08 | 0.84 |
| D: Two or three? | `` | ignore | wait | 0.12 | 0.76 |
| D: Is it the the the effective size and weight that the | `` | ignore | wait | 0.07 | 0.79 |
| D: Is it uh real size, real weight? | `` | ignore | wait | 0.09 | 0.81 |
| D: Size is going to be that, yeah? | `` | ignore | wait | 0.09 | 0.77 |
| C: The case is silver titanium, no? | `` | ignore | wait | 0.09 | 0.80 |
| A: And what about the strawberries on the top? | `` | ignore | wait | 0.07 | 0.88 |
| C: So, maybe think we can have rubber or some sponges, stuff for strawberries and different colours. | `` | ignore | wait | 0.10 | 0.72 |
| A: Okay, so you you you feel like it's something uh a protection for the remote control. | `` | ignore | wait | 0.06 | 0.67 |
| D: but uh can we adapt it to each each personal use? | `` | ignore | wait | 0.12 | 0.89 |
| D: You Do you think you are gonna be able to do that with ti titanium as well? | `` | ignore | wait | 0.14 | 0.80 |
| D: Who is good in math? | `` | ignore | wait | 0.10 | 0.94 |
| A: So now, it has to fulfil the financial criterium? | `` | ignore | wait | 0.11 | 0.85 |
| D: So so how many batteries do we need? | `` | ignore | wait | 0.15 | 0.89 |
| D: One battery? | `` | ignore | wait | 0.06 | 0.74 |
| D: Why two? | `` | ignore | wait | 0.11 | 0.84 |
| D: Say no. | `` | ignore | wait | 0.10 | 0.74 |
| D: Two batteries or one? | `` | ignore | wait | 0.08 | 0.84 |
| D: You never use uh Excel? | `` | ignore | wait | 0.07 | 0.82 |
| B: What what's the limit? | `` | ignore | wait | 0.11 | 0.84 |
| B: Check that number also. | `` | ignore | wait | 0.07 | 0.82 |
| D: It's a simple chip? | `` | ignore | wait | 0.04 | 0.73 |
| D: One or two? | `` | ignore | wait | 0.16 | 0.83 |
| D: One? | `` | ignore | wait | 0.09 | 0.64 |
| D: So the case, which one uh is it in the end? | `` | ignore | wait | 0.06 | 0.77 |
| C: no? | `` | ignore | wait | 0.06 | 0.68 |
| D: no? | `` | ignore | wait | 0.07 | 0.81 |
| D: It's only curve? | `` | ignore | wait | 0.10 | 0.82 |
| D: So, what is it? | `` | ignore | wait | 0.11 | 0.84 |
| D: T titanium? | `` | ignore | wait | 0.07 | 0.73 |
| D: Let's stick to s titan. | `` | ignore | wait | 0.05 | 0.63 |
| D: Special colour? | `` | ignore | wait | 0.07 | 0.84 |
| B: Well, n Why three? | `` | ignore | wait | 0.05 | 0.81 |
| C: No, only one, no? | `` | ignore | wait | 0.07 | 0.79 |
| B: Why three? | `` | ignore | wait | 0.06 | 0.81 |
| A: How many push-button? | `` | ignore | wait | 0.07 | 0.85 |
| A: Three or two? | `` | ignore | wait | 0.11 | 0.83 |
| D: That's all? | `` | ignore | wait | 0.15 | 0.77 |
| D: Uh, is it a scroll wheel and pe push button, th this centre one? | `` | ignore | wait | 0.11 | 0.84 |
| A: Because how do you do to y select? | `` | ignore | wait | 0.14 | 0.81 |
| D: no? | `` | ignore | wait | 0.20 | 0.73 |
| A: Stay longer. Okay. | `` | ignore | wait | 0.07 | 0.74 |
| A: You you have all of these, no? | `` | ignore | wait | 0.08 | 0.83 |
| D: Special colour? | `` | ignore | wait | 0.08 | 0.82 |
| D: Special material? | `` | ignore | wait | 0.12 | 0.82 |
| A: Not special colours an interest in? | `` | ignore | wait | 0.08 | 0.84 |
| A: And buttons are not colourised? | `` | ignore | wait | 0.07 | 0.79 |
| D: Are we supposed to cut things out now? | `` | ignore | wait | 0.07 | 0.89 |
| A: So think of what we can cut uh here. | `` | ignore | wait | 0.09 | 0.85 |
| A: But you don't need a battery? | `` | ignore | wait | 0.06 | 0.86 |
| A: it's like the hand dynamo, no? | `` | ignore | wait | 0.07 | 0.81 |
| B: Why not. | `` | ignore | wait | 0.06 | 0.60 |
| B: Advanced chip on print, right? | `` | ignore | wait | 0.09 | 0.82 |
| B: So, put minus one there, please. | `` | ignore | wait | 0.17 | 0.76 |
| B: Why not? | `` | ignore | wait | 0.10 | 0.85 |
| B: And? | `` | ignore | wait | 0.10 | 0.73 |
| D: And? | `` | ignore | wait | 0.09 | 0.60 |
| A: M maybe minus uh three, no? | `` | ignore | wait | 0.09 | 0.74 |
| B: So, was there result? | `` | ignore | wait | 0.07 | 0.86 |
| C: It's not changing, no? | `` | ignore | wait | 0.07 | 0.81 |
| B: Why? | `` | ignore | wait | 0.07 | 0.83 |
| D: Click somewhere, | `` | ignore | wait | 0.08 | 0.75 |
| D: Maybe put minus two, so it looks uh more reasonable. | `` | ignore | wait | 0.09 | 0.58 |
| B: Why not. | `` | ignore | wait | 0.11 | 0.55 |
| D: It's not recorded, is it? | `` | ignore | wait | 0.31 | 0.90 |
| A: Oh, we can put uh a hand dynamo and a battery if you want. | `` | ignore | wait | 0.06 | 0.72 |
| B: let's add one instead of two. | `` | ignore | wait | 0.07 | 0.69 |
| D: Is it? | `` | ignore | wait | 0.09 | 0.81 |
| C: Is really strict? | `` | ignore | wait | 0.09 | 0.86 |
| D: So, remove one of them. Yeah. | `` | ignore | wait | 0.25 | 0.75 |
| B: 'Cause uh I wonder if we put A_ or B_ somewhere instead of a number. | `` | ignore | wait | 0.07 | 0.61 |
| D: Let's finish this meeting instead. | `` | ignore | wait | 0.05 | 0.73 |
| D: What else? | `` | ignore | wait | 0.06 | 0.86 |
| D: Are the cost under twelve? | `` | ignore | wait | 0.10 | 0.84 |
| B: Next slide. | `` | ignore | wait | 0.11 | 0.65 |
| A: Mm. See mm how Are we a good team? Mm. | `` | ignore | wait | 0.07 | 0.82 |
| A: Is there enough room for creativity? | `` | ignore | wait | 0.08 | 0.93 |
| A: And you. | `` | ignore | wait | 0.11 | 0.56 |
| D: Maybe a lack of leadership? | `` | ignore | wait | 0.05 | 0.83 |
| B: M maybe not, huh? | `` | ignore | wait | 0.05 | 0.74 |
| B: What was the | `` | ignore | wait | 0.07 | 0.82 |
| B: what was good? | `` | ignore | wait | 0.05 | 0.81 |
| B: What was bad? | `` | ignore | wait | 0.05 | 0.88 |
| D: New ideas found? | `` | ignore | wait | 0.06 | 0.90 |
| D: what about the the pink the pinkness of that uh | `` | ignore | wait | 0.07 | 0.81 |
| D: Finished? | `` | ignore | wait | 0.11 | 0.84 |
| D: Are the costs within the budget? | `` | ignore | wait | 0.19 | 0.86 |
| D: Is the project evaluated? | `` | ignore | wait | 0.07 | 0.89 |
| B: we could forecast it, right? | `` | ignore | wait | 0.09 | 0.88 |
| D: To whom? | `` | ignore | wait | 0.07 | 0.83 |
| D: To the whole our company? | `` | ignore | wait | 0.05 | 0.81 |
| B: You? | `` | ignore | wait | 0.03 | 0.52 |
| C: So where we will go now? | `` | ignore | wait | 0.06 | 0.91 |
| C: Will go to Italian restaurant, or | `` | ignore | wait | 0.13 | 0.86 |
| A: And what you're uh drawing? | `` | ignore | wait | 0.06 | 0.80 |
| A: Uh how you spell your name uh? | `` | ignore | wait | 0.04 | 0.74 |
| A: And? | `` | ignore | wait | 0.07 | 0.72 |
| C: Do you also do marketing? | `` | ignore | wait | 0.07 | 0.78 |
| A: And? | `` | ignore | wait | 0.05 | 0.64 |
| A: So who is uh marketing, nobody in the market | `` | ignore | wait | 0.08 | 0.88 |
| A: but uh do you already have like a functional design or a technical design or | `` | ignore | wait | 0.04 | 0.57 |
| A: do you have some project plan, something with you or | `` | ignore | wait | 0.03 | 0.72 |
| A: so uh by when you think you can uh give me some kind of uh project plan, okay, | `` | ignore | wait | 0.04 | 0.76 |
| A: so there's any questions or uh first of all about uh this project? | `` | ignore | wait | 0.06 | 0.86 |
| C: What is the goal of the project? | `` | ignore | wait | 0.09 | 0.90 |
| A: so can you explain uh what exactly the product is? | `` | ignore | wait | 0.04 | 0.76 |
| D: is that right? | `` | ignore | wait | 0.12 | 0.81 |
| A: So uh you'll be leading the team for your design team or how many members is working in the team, for the desi | `` | ignore | wait | 0.07 | 0.61 |
| C: Uh for the industrial design? | `` | ignore | wait | 0.73 | 0.57 |
| A: Yeah, but uh before we talk about uh the finance, okay, uh do you have some idea how we can uh sell this produ | `` | ignore | wait | 0.06 | 0.63 |
| A: and how much is going to benefit to the company and uh of course it's to the individual also. | `` | ignore | wait | 0.04 | 0.56 |
| A: but uh uh when you think you can give me like a kind of design on the functional design or the technical desig | `` | ignore | wait | 0.11 | 0.76 |
| A: Yeah, but uh I need something in the writing, | `` | ignore | wait | 0.08 | 0.57 |
| A: so like uh what's your functional design, what's your technical design, and uh how many people you need for th | `` | ignore | wait | 0.07 | 0.71 |
| A: so you've you've had to meet with the marketing team and how they're going to market and what are the marketin | `` | ignore | wait | 0.07 | 0.71 |
| A: when are you going to introduce, okay, and by the time you introduce the product and uh you know there there w | `` | ignore | wait | 0.06 | 0.73 |
| A: okay, so I need some kind of uh uh the plan in the writing from you. | `` | ignore | wait | 0.06 | 0.63 |
| C: And when would you like that? | `` | ignore | wait | 0.15 | 0.73 |
| C: Uh well if uh if we have enough time uh then d do you think um two weeks is a is close enough? | `` | ignore | wait | 0.36 | 0.70 |
| C: Uh are there other people who will be contributing to the plan? | `` | ignore | wait | 0.27 | 0.83 |
| A: So, who are the people you need uh from the marketing or uh the technical side or uh the administration point  | `` | ignore | wait | 0.05 | 0.76 |
| A: so just let me know so I can uh coordinate all the teams. | `` | ignore | wait | 0.04 | 0.74 |
| A: and d do you have some already planned something for your marketing strategy or uh the sales strategy? | `` | ignore | wait | 0.06 | 0.71 |
| D: Do we already have a cost limit on this, th an idea of how much uh we want to market this for, how much it's g | `` | ignore | wait | 0.13 | 0.80 |
| D: that's up that's up to us to decide, eh? | `` | ignore | wait | 0.09 | 0.65 |
| A: and how we are going to compete in the market, okay, in the the technically, or in the sales wise, okay, the c | `` | ignore | wait | 0.06 | 0.82 |
| A: Then uh we have to design, okay, how long it will take the whole project, okay, how much is going to cost us,  | `` | ignore | wait | 0.05 | 0.67 |
| A: Okay, so I think it's uh maybe if we can uh give me some kind of your uh the sales plan, okay, including the t | `` | ignore | wait | 0.09 | 0.77 |
| A: Okay, and if you need uh any coordination in between uh compared to the maybe the some technical vendors or co | `` | ignore | wait | 0.06 | 0.78 |
| A: or maybe uh, you are my coordinator, am I right? | `` | ignore | wait | 0.05 | 0.72 |
| B: I guess build the plan based on all of that, | `` | ignore | wait | 0.06 | 0.51 |
| A: But what I request, okay, keep Ed in the loop, okay, in between your uh meeting and Christine meeting, because | `` | ignore | wait | 0.06 | 0.74 |
| A: Okay and please please copy all the mails, okay, all the discussions to me, okay, | `` | ignore | wait | 0.12 | 0.71 |
| A: So any questions for uh time being? | `` | ignore | wait | 0.06 | 0.88 |
| A: and uh first of all with your user acceptance, okay, how it looks like and how it's going to be work in the ma | `` | ignore | wait | 0.04 | 0.53 |
| A: It's okay? | `` | ignore | wait | 0.05 | 0.79 |
| C: Would you mind um at the conclusion of our meeting could could you send us a copy of your slides? | `` | ignore | wait | 0.06 | 0.80 |
| A: le let us keep all the emails and all the copies, okay, share each other, okay, so you know everybody what's h | `` | ignore | wait | 0.04 | 0.61 |
| A: It's good? | `` | ignore | wait | 0.05 | 0.78 |
| A: can you go to the next slide? | `` | ignore | wait | 0.22 | 0.84 |
| B: do you wanna open the | `` | ignore | wait | 0.08 | 0.80 |
| C: Two? | `` | ignore | wait | 0.05 | 0.63 |
| C: Do you want the mouse, | `` | ignore | wait | 0.07 | 0.77 |
| C: or do you want me to | `` | ignore | wait | 0.05 | 0.61 |
| B: I don't know why um we were asked to do this. | `` | ignore | wait | 0.07 | 0.58 |
| B: so I think it should give you some sort of an oral cue. | `` | ignore | wait | 0.28 | 0.59 |
| A: if you can add other facility, other feature, like uh unbreakable. | `` | ignore | wait | 0.10 | 0.71 |
| A: if you can add the feature, okay, for your uh fabric whatever in your outline design okay, with unbreakable, | `` | ignore | wait | 0.12 | 0.68 |
| A: if I'm not wrong. Maybe you can uh add it in that. | `` | ignore | wait | 0.08 | 0.60 |
| A: and uh uh any questions or uh clarifications, or any discussion on the functional design? | `` | ignore | wait | 0.05 | 0.92 |
| C: Do you have any preconceived ideas in terms of materials? | `` | ignore | wait | 0.15 | 0.85 |
| B: wouldn't it? | `` | ignore | wait | 0.04 | 0.79 |
| B: um I wanted feedback, | `` | ignore | wait | 0.10 | 0.84 |
| B: I think we need to rate rank these, | `` | ignore | wait | 0.07 | 0.68 |
| B: but we'll see what your uh personal preferences are and your thoughts. | `` | ignore | wait | 0.09 | 0.78 |
| C: I just wondering whether that you had any sort of | `` | ignore | wait | 0.07 | 0.73 |
| B: nobody told me how mu what our financial objective is, so um | `` | ignore | wait | 0.07 | 0.68 |
| A: okay? | `` | ignore | wait | 0.11 | 0.72 |
| A: how much its cost for the manufacturing | `` | ignore | wait | 0.06 | 0.80 |
| A: Then uh you can come back with your feedback. | `` | ignore | wait | 0.06 | 0.63 |
| A: But let's try it, okay, with the different uh the designs, okay, the functional designs. | `` | ignore | wait | 0.06 | 0.74 |
| A: Okay? | `` | ignore | wait | 0.06 | 0.76 |
| A: any other questions? | `` | ignore | wait | 0.06 | 0.92 |
| D: Okay? | `` | ignore | wait | 0.05 | 0.72 |
| B: Speech recognition?. | `` | ignore | wait | 0.07 | 0.79 |
| A: So what do you think about uh the design? | `` | ignore | wait | 0.07 | 0.81 |
| A: Do you think you can make it or uh | `` | ignore | wait | 0.08 | 0.74 |
| B: uh I'm sorry? | `` | ignore | wait | 0.16 | 0.59 |
| A: What do you think about uh the design, uh what he was talking about of the speech recognition? | `` | ignore | wait | 0.09 | 0.75 |
| A: and uh you can uh let me know, okay, so what kind of uh the details you require okay, to add this feature in t | `` | ignore | wait | 0.07 | 0.84 |
| A: we need to know how much is the timeframe you need to develop, apart from uh what today. | `` | ignore | wait | 0.08 | 0.84 |
| D: What do they want? | `` | ignore | wait | 0.05 | 0.72 |
| D: Uh, a risk, take a risk on the market? | `` | ignore | wait | 0.12 | 0.80 |
| D: Something that's gonna cost more, but could very easily s make a boom in the market? | `` | ignore | wait | 0.11 | 0.67 |
| A: I don't mind to convince, okay, the management to spend some more money on the project, okay, if you can make  | `` | ignore | wait | 0.04 | 0.54 |
| A: if you have any uh new ideas, okay, for uh your you can always come up | `` | ignore | wait | 0.09 | 0.76 |
| A: and uh you can tell me if you need any uh s special, okay, coordination, okay, between any uh technical compan | `` | ignore | wait | 0.08 | 0.71 |
| A: And uh what's your comments about uh | `` | ignore | wait | 0.10 | 0.84 |
| C: maybe if I go through my presentation, you can sort of see what the user perspective is, and how it ties into  | `` | ignore | wait | 0.23 | 0.66 |
| A: Uh where are you, here? | `` | ignore | wait | 0.10 | 0.81 |
| A: Is it okay? | `` | ignore | wait | 0.08 | 0.82 |
| C: Um and then what the remote control should look like, | `` | ignore | wait | 0.06 | 0.73 |
| C: I don't know if you guys have any questions or | `` | ignore | wait | 0.08 | 0.86 |
| A: for anybody need uh any help, for time being, on this uh subjects, okay, so please come back to me, | `` | ignore | wait | 0.05 | 0.65 |
| C: Should we maybe make a decision about what features we actually want to include, | `` | ignore | wait | 0.17 | 0.91 |
| C: do we actually want to incorporate all of them, | `` | ignore | wait | 0.11 | 0.90 |
| C: or have we missed anything? | `` | ignore | wait | 0.08 | 0.93 |
| B: Do you wanna go back and look at the closing slide, | `` | ignore | wait | 0.05 | 0.86 |
| B: maybe that would provide some guidance? | `` | ignore | wait | 0.04 | 0.84 |
| B: I think we should do as many features as uh start with all of them right now | `` | ignore | wait | 0.05 | 0.56 |
| B: You can object if you want to | `` | ignore | wait | 0.07 | 0.76 |
| C: I was just thinking is it really practical to start designing something with features that we're just gonna en | `` | ignore | wait | 0.07 | 0.84 |
| A: and uh please put your all information in the sharing folder | `` | ignore | wait | 0.05 | 0.86 |
| A: Okay? | `` | ignore | wait | 0.05 | 0.79 |
| C: So uh, if you could open the PowerPoint presentation. | `` | ignore | wait | 0.07 | 0.80 |
| C: So uh can we put it in slide show mode? | `` | ignore | wait | 0.12 | 0.89 |
| C: you know uh, well you guys come from tropical countries so you can kinda think of some trees and some nice woo | `` | ignore | wait | 0.06 | 0.81 |
| C: Do you have any problems with that? | `` | ignore | wait | 0.12 | 0.92 |
| A: Can you go back uh one slide? | `` | ignore | wait | 0.09 | 0.77 |
| C: I'm not sure, how do I | `` | ignore | wait | 0.32 | 0.86 |
| A: question, uh, what's mean exactly, advanced chip on print? | `` | ignore | wait | 0.14 | 0.87 |
| A: What's the meaning of that? | `` | ignore | wait | 0.14 | 0.88 |
| A: is it on a micro-proc micro-processor based or uh | `` | ignore | wait | 0.08 | 0.85 |
| B: Why was the plastic eliminated as a possible material? | `` | ignore | wait | 0.07 | 0.90 |
| B: wouldn't you, | `` | ignore | wait | 0.05 | 0.77 |
| A: So so you're not convinced about the the wood, yes. | `` | ignore | wait | 0.07 | 0.56 |
| C: you're what? | `` | ignore | wait | 0.04 | 0.58 |
| A: what about yo you? | `` | ignore | wait | 0.08 | 0.77 |
| B: in terms of comments on this or in terms of my own | `` | ignore | wait | 0.07 | 0.61 |
| D: Wood? | `` | ignore | wait | 0.12 | 0.72 |
| A: This one? | `` | ignore | wait | 0.07 | 0.78 |
| B: so if you want to just go straight to the second slide, | `` | ignore | wait | 0.05 | 0.72 |
| A: So what's your, uh, the comments or uh s | `` | ignore | wait | 0.08 | 0.82 |
| D: If you can find me, where I'm at. | `` | ignore | wait | 0.13 | 0.84 |
| C: f go to findings. | `` | ignore | wait | 0.11 | 0.61 |
| D: How hard they squeeze? | `` | ignore | wait | 0.05 | 0.82 |
| D: We have to come up with something totally new that is not on the market. | `` | ignore | wait | 0.06 | 0.59 |
| A: but uh le let's decide first about the components concept and uh interface concept, okay, | `` | ignore | wait | 0.04 | 0.71 |
| A: if is acceptable for both of you, what uh Ed was talking. | `` | ignore | wait | 0.04 | 0.81 |
| A: And your design whether you want with the display or without display or just a simple, so | `` | ignore | wait | 0.04 | 0.82 |
| C: do you know how much it costs, um, to to add a little display like this uh? | `` | ignore | wait | 0.07 | 0.77 |
| C: Do you wanna take an action item to go find out? | `` | ignore | wait | 0.05 | 0.78 |
| B: What about the buttons, would Would the buttons be wood too, or | `` | ignore | wait | 0.04 | 0.88 |
| A: maybe what you can do is uh, both of you, you can come up with the the prototype, okay, the model. | `` | ignore | wait | 0.04 | 0.77 |
| A: Okay? | `` | ignore | wait | 0.04 | 0.78 |
| C: are we done with this meeting? | `` | ignore | wait | 0.05 | 0.92 |
| A: is it okay if uh they will come up with the prototype design, okay. | `` | ignore | wait | 0.05 | 0.84 |
| A: Then meantime you can come up with the price, how much it's cost as extra for uh the display. | `` | ignore | wait | 0.09 | 0.76 |
| C: And a marketing strategy. | `` | ignore | wait | 0.12 | 0.50 |
| A: how mu how much how much you can sell extra. | `` | ignore | wait | 0.06 | 0.83 |
| A: Okay, so, any questions? | `` | ignore | wait | 0.06 | 0.92 |
| A: So, by next meeting, so, please come up with the the prototype, okay, | `` | ignore | wait | 0.05 | 0.81 |
| A: It's okay? | `` | ignore | wait | 0.06 | 0.83 |
| A: Okay? | `` | ignore | wait | 0.04 | 0.56 |
| A: So shall I go to | `` | ignore | wait | 0.05 | 0.83 |
| C: But if you've already got the remote control in your hand you need to open the flip to use the voice, why use  | `` | ignore | wait | 0.72 | 0.83 |
| D: I don't wanna say. Louder. Yeah. | `` | ignore | wait | 0.28 | 0.65 |
| C: So, I mean I can pass this around if anyone wants to | `` | ignore | wait | 0.05 | 0.70 |
| B: You need to work on the weight a little bit. | `` | ignore | wait | 0.07 | 0.61 |
| A: That's your uh prototype model? | `` | ignore | wait | 0.06 | 0.72 |
| A: So any comments or uh | `` | ignore | wait | 0.07 | 0.90 |
| B: . It's gonna cost a long way to c you know, cost a lot of money to market it, is it? | `` | ignore | wait | 0.05 | 0.81 |
| B: So that means we can put the uh the L_C_D_ in, yeah. | `` | ignore | wait | 0.05 | 0.50 |
| D: But as far as production um I'm putting up a question | `` | ignore | wait | 0.05 | 0.66 |
| D: If we can go to to my display. | `` | ignore | wait | 0.09 | 0.76 |
| A: You're in four? | `` | ignore | wait | 0.07 | 0.71 |
| B: Is this the same one you did before? | `` | ignore | wait | 0.08 | 0.71 |
| D: You have to go back and find another one. | `` | ignore | wait | 0.06 | 0.65 |
| D: Uh functional, try functional, | `` | ignore | wait | 0.10 | 0.53 |
| D: Okay? | `` | ignore | wait | 0.05 | 0.77 |
| D: Next screen. | `` | ignore | wait | 0.09 | 0.54 |
| D: Which means that uh if we have a target of two million would the company has to take twenty five percent of th | `` | ignore | wait | 0.06 | 0.89 |
| D: Okay? | `` | ignore | wait | 0.10 | 0.81 |
| D: Can the company sell two million units? | `` | ignore | wait | 0.10 | 0.91 |
| D: Can it sell it for fifty Euros? | `` | ignore | wait | 0.27 | 0.90 |
| B: Could could I go to findings? | `` | ignore | wait | 0.09 | 0.85 |
| B: Uh uh um I would uh like to explore the possibility of using um alternative um delivery and sales channel | `` | ignore | wait | 0.08 | 0.72 |
| B: don't you think? | `` | ignore | wait | 0.11 | 0.86 |
| A: okay then, l uh let's wait for the production, okay, then uh you can evaluate the product, | `` | ignore | wait | 0.06 | 0.52 |
| A: so how it looks like technically and uh how it look like uh the real. | `` | ignore | wait | 0.07 | 0.85 |
| C: What turnaround time do we have? | `` | ignore | wait | 0.08 | 0.89 |
| B: Prototypes, you mean. | `` | ignore | wait | 0.17 | 0.61 |
| A: S Any any other uh questions or uh comments to be discuss? | `` | ignore | wait | 0.04 | 0.91 |
| B: Did you have something? | `` | ignore | wait | 0.09 | 0.76 |
| C: Well I was just wondering about if we're gonna do a product evaluation then what about time for redesign if th | `` | ignore | wait | 0.06 | 0.90 |
| A: Okay? | `` | ignore | wait | 0.07 | 0.78 |
| B: Would it be the Christmas season by any chance? | `` | ignore | wait | 0.06 | 0.75 |
| B: Which sport season? | `` | ignore | wait | 0.32 | 0.89 |
| C: Really? | `` | ignore | wait | 0.03 | 0.75 |
| A: and uh are the costs within the budget | `` | ignore | wait | 0.05 | 0.83 |
| A: and uh is the product evaluated, okay, so that will uh come soon. | `` | ignore | wait | 0.04 | 0.68 |
| A: So let's meet up uh this evening to hang up for some party. | `` | ignore | wait | 0.05 | 0.72 |
| A: and uh I hope you will introduce yourself uh in a few minutes, | `` | ignore | wait | 0.04 | 0.81 |
| A: Um you have to put your laptop exactly in that field | `` | ignore | wait | 0.05 | 0.78 |
| A: and uh I'd like to hear uh who you are and what your functions are uh on this project. | `` | ignore | wait | 0.08 | 0.88 |
| A: Let's start with the ladies. | `` | ignore | wait | 0.04 | 0.58 |
| A: but we ask you not to do that. | `` | ignore | wait | 0.05 | 0.62 |
| A: Just simply create a new one | `` | ignore | wait | 0.07 | 0.51 |
| A: Um does everyone understand this | `` | ignore | wait | 0.06 | 0.93 |
| A: nice application? | `` | ignore | wait | 0.11 | 0.85 |
| A: but don't uh delete entire pages. | `` | ignore | wait | 0.06 | 0.50 |
| A: because I'm uh going to ask you to draw your favourite animal. | `` | ignore | wait | 0.05 | 0.51 |
| A: to do it on a blank sheet, | `` | ignore | wait | 0.04 | 0.53 |
| A: and um try to draw | `` | ignore | wait | 0.08 | 0.63 |
| A: Or maybe you should guess what I'm drawing, eh. | `` | ignore | wait | 0.10 | 0.84 |
| B: It has wings? | `` | ignore | wait | 0.10 | 0.89 |
| A: Would you like to go next? | `` | ignore | wait | 0.08 | 0.89 |
| D: Anything else you need to know? | `` | ignore | wait | 0.18 | 0.86 |
| A: Could you write the words, uh underneath it? | `` | ignore | wait | 0.10 | 0.78 |
| A: Or more words. | `` | ignore | wait | 0.08 | 0.63 |
| B: Should I uh | `` | ignore | wait | 0.10 | 0.85 |
| B: you can guess what it is, I hope. | `` | ignore | wait | 0.11 | 0.83 |
| B: You can try out the eraser now. | `` | ignore | wait | 0.09 | 0.60 |
| A: huh? | `` | ignore | wait | 0.08 | 0.50 |
| A: Uh what's your experience with remote controls, | `` | ignore | wait | 0.11 | 0.88 |
| A: um what kind of ideas do you have to design a new remote control, | `` | ignore | wait | 0.11 | 0.90 |
| A: maybe for which market segments should we aim, | `` | ignore | wait | 0.08 | 0.91 |
| A: or should we aim for all segments. | `` | ignore | wait | 0.09 | 0.92 |
| A: actually I'd like to hand the word uh back to you. | `` | ignore | wait | 0.11 | 0.71 |
| A: What's your experience with remote control? | `` | ignore | wait | 0.12 | 0.86 |
| B: search for the buttons, which one is which | `` | ignore | wait | 0.11 | 0.82 |
| A: maybe we should try to make it fun. | `` | ignore | wait | 0.07 | 0.62 |
| B: perhaps you can integrate them or something. | `` | ignore | wait | 0.08 | 0.57 |
| B: But you should make sure that you have every button they need on it. | `` | ignore | wait | 0.11 | 0.54 |
| B: what's the name? | `` | ignore | wait | 0.07 | 0.83 |
| B: I dunno if you should uh take that in consideration, | `` | ignore | wait | 0.07 | 0.54 |
| D: You can use which which type of television you have. | `` | ignore | wait | 0.06 | 0.64 |
| A: any more ideas? | `` | ignore | wait | 0.08 | 0.93 |
| A: No? | `` | ignore | wait | 0.06 | 0.83 |
| A: Is it my laptop? | `` | ignore | wait | 0.15 | 0.84 |
| C: Stop the meeting now. | `` | ignore | wait | 0.14 | 0.87 |
| A: And this was the Interface Designer? | `` | ignore | wait | 0.06 | 0.80 |
| A: Or what was it, I_D_? | `` | ignore | wait | 0.06 | 0.83 |
| A: Let's just use the acronyms. | `` | ignore | wait | 0.06 | 0.61 |
| A: Uh are there any more questions? | `` | ignore | wait | 0.05 | 0.93 |
| A: No? | `` | ignore | wait | 0.05 | 0.81 |
| D: I have one question. | `` | ignore | wait | 0.11 | 0.56 |
| A: one question? | `` | ignore | wait | 0.04 | 0.54 |
| D: Where does it says we have to make a remote, | `` | ignore | wait | 0.08 | 0.89 |
| A: All set? | `` | ignore | wait | 0.07 | 0.87 |
| A: I guess each one of you has prepared one? | `` | ignore | wait | 0.04 | 0.92 |
| A: Um well I don't know who wants to go first with his presentation. | `` | ignore | wait | 0.03 | 0.92 |
| D: shall I go first with the users? | `` | ignore | wait | 0.04 | 0.86 |
| A: Is there an order? | `` | ignore | wait | 0.07 | 0.91 |
| C: Huh? | `` | ignore | wait | 0.09 | 0.73 |
| A: And one question, | `` | ignore | wait | 0.06 | 0.58 |
| A: uh your name Denni, is it with a | `` | ignore | wait | 0.04 | 0.54 |
| C: You know what a let is? | `` | ignore | wait | 0.15 | 0.92 |
| C: or just is it's it's very light to uh to make uh to use it. | `` | ignore | wait | 0.10 | 0.51 |
| B: Shall I go uh next? | `` | ignore | wait | 0.08 | 0.87 |
| B: turn it on, | `` | ignore | wait | 0.11 | 0.59 |
| B: if you use it your C_D_ player the remote control will that one. | `` | ignore | wait | 0.19 | 0.66 |
| B: split screen and uh is that a function that you should have? | `` | ignore | wait | 0.16 | 0.87 |
| B: You must still have it open. | `` | ignore | wait | 0.09 | 0.56 |
| D: Are the younger people going to buy the remote control or the elderly people? | `` | ignore | wait | 0.07 | 0.93 |
| D: or shouldn't be that complex | `` | ignore | wait | 0.06 | 0.75 |
| D: because we have to search for the buttons, which one are you going to use. | `` | ignore | wait | 0.06 | 0.70 |
| D: Put one option | `` | ignore | wait | 0.07 | 0.54 |
| C: Uh L_C_D_ screen as in uh touch screen? | `` | ignore | wait | 0.07 | 0.86 |
| A: I dunno uh did everyone receive an email with uh the new project requirements? | `` | ignore | wait | 0.05 | 0.93 |
| A: No? | `` | ignore | wait | 0.04 | 0.63 |
| B: Perhaps the rest? | `` | ignore | wait | 0.06 | 0.83 |
| A: who has any idea about what should be on it, and what shouldn't? | `` | ignore | wait | 0.06 | 0.94 |
| B: you said it should only uh work with one appliance? | `` | ignore | wait | 0.04 | 0.60 |
| B: Or with one uh d che only the T_V_? | `` | ignore | wait | 0.14 | 0.80 |
| B: And the video also, or not uh? | `` | ignore | wait | 0.08 | 0.88 |
| A: it says only for television here, huh. | `` | ignore | wait | 0.08 | 0.63 |
| A: huh? | `` | ignore | wait | 0.08 | 0.71 |
| D: no? | `` | ignore | wait | 0.10 | 0.73 |
| C: yeah? | `` | ignore | wait | 0.09 | 0.66 |
| D: oh teletext doesn't have to be? | `` | ignore | wait | 0.07 | 0.84 |
| D: Our main targets' age are? were? Forty five plus, or? | `` | ignore | wait | 0.06 | 0.89 |
| C: is it possible to make an L_C_D_ screen uh, | `` | ignore | wait | 0.10 | 0.89 |
| C: how was the information? | `` | ignore | wait | 0.12 | 0.84 |
| C: perhaps we should we should focus on that L_C_D_ screen. | `` | ignore | wait | 0.07 | 0.54 |
| C: but uh will we not uh exceed our uh our uh production uh | `` | ignore | wait | 0.04 | 0.84 |
| C: Is it possible to find out, anyway? | `` | ignore | wait | 0.08 | 0.89 |
| C: You know? | `` | ignore | wait | 0.09 | 0.65 |
| B: But if you would do an L_C_D_ screen do we have don don't you have any buttons? | `` | ignore | wait | 0.07 | 0.78 |
| B: Or because if it only directs at the T_V_, then you only have uh I don't know what you want to do with the L_C | `` | ignore | wait | 0.05 | 0.61 |
| A: we're going for an L_C_D_ screen? | `` | ignore | wait | 0.08 | 0.85 |
| B: we had twelve fifty, I guess, for uh production? | `` | ignore | wait | 0.05 | 0.61 |
| B: Any guesses? | `` | ignore | wait | 0.05 | 0.92 |
| B: and will they use it if it only has an L_C_D_ screen? | `` | ignore | wait | 0.05 | 0.86 |
| A: L_C_D_ it is? | `` | ignore | wait | 0.08 | 0.74 |
| A: And what else? | `` | ignore | wait | 0.09 | 0.87 |
| C: if you uh you receive an email about that, uh can you post it in the | `` | ignore | wait | 0.07 | 0.82 |
| C: or shouldn't we post that in uh our projects mail uh folder. | `` | ignore | wait | 0.05 | 0.87 |
| B: perhaps we should have a backup plan | `` | ignore | wait | 0.04 | 0.71 |
| B: The L_C_D_? | `` | ignore | wait | 0.07 | 0.82 |
| A: and maybe you can make something fancy out of an L_C_D_ remote, | `` | ignore | wait | 0.07 | 0.63 |
| C: Okay? | `` | ignore | wait | 0.07 | 0.64 |
| A: what else does our remote need? | `` | ignore | wait | 0.12 | 0.91 |
| B: But shouldn't you put a button of for teletext on the for the people who want to use it? | `` | ignore | wait | 0.06 | 0.83 |
| D: Sorry? | `` | ignore | wait | 0.07 | 0.53 |
| B: or not? | `` | ignore | wait | 0.07 | 0.85 |
| C: Uh I think it's also important to uh make it possible to um how do you call it in English, uh, to not use batt | `` | ignore | wait | 0.07 | 0.65 |
| B: We should think of the twelve fifty we have | `` | ignore | wait | 0.07 | 0.57 |
| B: Perhaps you should be able to to switch the control off. | `` | ignore | wait | 0.06 | 0.60 |
| B: If you have an L_C_D_ screen that's burns all the time I dunno. | `` | ignore | wait | 0.07 | 0.50 |
| A: And maybe a low battery indicator? On the screen. | `` | ignore | wait | 0.12 | 0.72 |
| B: or not? | `` | ignore | wait | 0.06 | 0.80 |
| A: you have some more | `` | ignore | wait | 0.07 | 0.54 |
| C: so make it possible to not uh display uh a button at ten points | `` | ignore | wait | 0.06 | 0.53 |
| D: Yeah? | `` | ignore | wait | 0.06 | 0.56 |
| A: And you said something about speech recognition? | `` | ignore | wait | 0.14 | 0.83 |
| C: Speech recognition? | `` | ignore | wait | 0.11 | 0.69 |
| C: let's leave out all the remote controls | `` | ignore | wait | 0.05 | 0.80 |
| B: You can clap or something. | `` | ignore | wait | 0.06 | 0.66 |
| D: would you pay more for speech recognition in a remote control. It's the only thing it says. | `` | ignore | wait | 0.12 | 0.85 |
| B: but do we want to implement that, | `` | ignore | wait | 0.09 | 0.89 |
| A: Speech recognition scores even higher, huh? | `` | ignore | wait | 0.08 | 0.79 |
| C: Why not? | `` | ignore | wait | 0.15 | 0.81 |
| C: Why not? | `` | ignore | wait | 0.08 | 0.80 |
| A: But would it be useful to imple implement both? | `` | ignore | wait | 0.07 | 0.91 |
| A: On one remote? | `` | ignore | wait | 0.07 | 0.84 |
| B: but how would you like to implement that, | `` | ignore | wait | 0.07 | 0.84 |
| B: that you say volume up, and then it goes up, | `` | ignore | wait | 0.18 | 0.65 |
| B: Then uh it's y it's yours to do a French and Dutch and English | `` | ignore | wait | 0.12 | 0.71 |
| D: what else? | `` | ignore | wait | 0.09 | 0.87 |
| A: no speech recognition? | `` | ignore | wait | 0.22 | 0.87 |
| B: you sh you should to adjust the thing. | `` | ignore | wait | 0.14 | 0.62 |
| D: Curved? | `` | ignore | wait | 0.07 | 0.83 |
| C: So does it confuse uh the user? | `` | ignore | wait | 0.10 | 0.89 |
| D: What else can you do with a television? | `` | ignore | wait | 0.34 | 0.89 |
| A: Aren't we forgetting something very important? | `` | ignore | wait | 0.11 | 0.91 |
| B: you could look here | `` | ignore | wait | 0.07 | 0.52 |
| D: Which ones were yours? | `` | ignore | wait | 0.05 | 0.75 |
| B: They're a bit small, you can we should stretch them, | `` | ignore | wait | 0.07 | 0.51 |
| B: And for a T_V_? Can you zoom in a T_V_? | `` | ignore | wait | 0.20 | 0.89 |
| B: And do we want them in different colours, | `` | ignore | wait | 0.05 | 0.91 |
| B: and the buttons, should they have colours? | `` | ignore | wait | 0.05 | 0.90 |
| D: Because uh how many percent? | `` | ignore | wait | 0.09 | 0.86 |
| D: Eighty percent? | `` | ignore | wait | 0.10 | 0.84 |
| B: right? | `` | ignore | wait | 0.07 | 0.78 |
| B: Perhaps you can uh make adjustable fronts, like with the telephones. | `` | ignore | wait | 0.10 | 0.77 |
| C: make it available in different colours, you mean? | `` | ignore | wait | 0.08 | 0.80 |
| C: Leave. | `` | ignore | wait | 0.11 | 0.71 |
| B: Five minutes? | `` | ignore | wait | 0.11 | 0.83 |
| A: and what else? | `` | ignore | wait | 0.13 | 0.87 |
| D: Channel settings? | `` | ignore | wait | 0.07 | 0.85 |
| B: Perhaps you should you'd throw them on on in one pile. | `` | ignore | wait | 0.06 | 0.60 |
| A: and maybe there are options for the remote itself? Like uh large icons or small icons | `` | ignore | wait | 0.08 | 0.57 |
| B: Or do we have any buttons? On the remote. | `` | ignore | wait | 0.08 | 0.90 |
| B: Which one? | `` | ignore | wait | 0.07 | 0.79 |
| A: huh? | `` | ignore | wait | 0.07 | 0.63 |
| B: right? | `` | ignore | wait | 0.09 | 0.73 |
| B: you should be able to set which T_V_ you have. | `` | ignore | wait | 0.08 | 0.60 |
| B: But isn't idea to use uh uh what you said, uh normal on and off button for the T_V_, | `` | ignore | wait | 0.12 | 0.84 |
| D: otherwise is it it jumps to stand-by mode automatically. | `` | ignore | wait | 0.06 | 0.70 |
| A: So how do you turn the thing on? | `` | ignore | wait | 0.09 | 0.87 |
| A: huh? | `` | ignore | wait | 0.06 | 0.63 |
| A: or just the remote? | `` | ignore | wait | 0.14 | 0.88 |
| B: I don't know whether it's handy to have a n a normal on button, a r just uh rubber uh for for T_V_, | `` | ignore | wait | 0.06 | 0.68 |
| C: why would it be a a need to have a normal button? | `` | ignore | wait | 0.06 | 0.88 |
| A: that's might be a unique selling point, huh for a remote. | `` | ignore | wait | 0.06 | 0.82 |
| B: Should we put this back in our rooms, | `` | ignore | wait | 0.09 | 0.90 |
