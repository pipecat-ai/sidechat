# An independent test: TCL's Intelligent Wakeup

2026-11-20. exp-063. Counts with 95% intervals. No line of the set is quoted: it is CC BY-NC and
test only (SD-27).

## The question

Our tests are mostly our own: generated conversations, our guide's labels, and found data we
converted. Where does rc0.3 stand on an on-task set someone else made and labelled?

## The set

[TCLResearchEurope/intelligent_wakeup](https://huggingface.co/datasets/TCLResearchEurope/intelligent_wakeup)
v1.0.1, test split.

- **What it is:** 243 sessions of people at home or work with a voice assistant, Sigma, in the room.
  Written by a language model, spoken by text-to-speech. Only the text is used here, as written (no
  speech-to-text), with the directions for the voice removed.
- **Sessions:** 212 with two people and 31 with one. 89 sessions never address Sigma; each is the
  twin of one that does.
- **Lines:** 3,647 people's turns. Sigma's 321 turns stay in the history as the agent's.
- **Its label:** a person's turn is for Sigma when Sigma speaks next.
  - **Direct** (158) has Sigma's name.
  - **Contextual** (141) has no name, usually a follow-up in an exchange with Sigma.
  - The other 3,348 lines are not for Sigma.
- **Converter:** `sidechat/sources/tcl_wakeup.py`. Its counts match TCL's own.

**The reference** is TCL's own audio model, on the same 3,647 turns, from its repo. It was trained
on TCL's train split (the same generator, voices and scenario list) and hears the audio. Ours have
never seen this set's style and read only the text. Nothing was tuned on this set: every build runs
at its own thresholds, and Jev runs as the demo asks it.

## Results

Speakers anonymous (SD-14's headline). With speakers named, every figure is within two points. The
paired comparisons below are with speakers named.

An accept is an answer now. Holds are counted apart, because a hold is not an answer.

| | Precision | Recall | F1 | False accepts an hour | Named requests answered now | Follow-ups answered now | Follow-ups held | People's lines answered | People's lines held |
|---|---|---|---|---|---|---|---|---|---|
| TCL's audio model (trained on TCL) | 0.931 | 0.853 | **0.890** | 2.8 | 93.7% (148/158) | **75.9%** (107/141; 68.2 to 82.2) | | **0.57%** (19/3,348; 0.36 to 0.88) | |
| Jev | 0.790 | 0.656 | 0.717 | 7.7 | 98.1% (155/158) | 29.1% (41/141; 22.2 to 37.1) | 51.8% | 1.55% (52; 1.19 to 2.03) | 36.9% |
| **rc0.3 default (150M)** | 0.761 | 0.692 | 0.725 | 9.7 | 98.7% (156/158) | 36.2% (51/141; 28.7 to 44.4) | 20.6% | 1.94% (65; 1.53 to 2.47) | 3.1% |
| rc0.3 agent-1x (32M) | 0.733 | 0.689 | 0.710 | 11.2 | 98.7% | 35.5% (50) | 16.3% | 2.24% (75) | 2.7% |
| rc0.2 default (150M) | 0.793 | 0.679 | 0.732 | 7.9 | 98.7% | 33.3% (47) | 19.9% | 1.58% (53) | 2.6% |
| rc0.2 agent-1x (32M) | 0.779 | 0.672 | 0.722 | 8.5 | 98.7% | 31.9% (45) | 18.4% | 1.70% (57) | 2.1% |

False accepts an hour are per hour of recording (6.7 hours), TCL's own denominator.

- **Named requests: as good as it gets from text.** Every build answers 98.7% at once, the same as
  Jev. TCL's audio model gets 93.7%; it hears the name, where we read it.
- **On answering now, rc0.3 ties Jev.** Lines decided right, paired: +0.05 points (-0.47 to +0.58).
  But Jev also holds 37% of people's lines; rc0.3 holds 3%.
- **rc0.3 against rc0.2: the same here,** except the known trade.
  - Unnamed follow-ups answered now: +1.4 points (-4.5 to +7.3).
  - People's lines answered outright: no worse beyond noise (0.2 points more, -0.1 to +0.5).
  - People's lines left alone: 0.7 points fewer (0.3 to 1.1), mostly holds, as on AMI and the
    Ambient Bench.
- **Against a model trained on this set's own distribution, we are well behind.** Part of the gap
  in false accepts is the label (below).
  - TCL's model answers twice as many unnamed follow-ups: 76% against 36%.
  - It answers a third as many people's lines outright: 0.57% against 1.94%.
  - This is the first test where rc0.3 answers people outright more than about 0.5% of the time
    (Duplex-MPE 0.2%, AMI none).

With a hold counted as an accept, rc0.3 reaches recall 0.79 at precision 0.58; Jev reaches 0.90 at
0.17.

## Where the errors are

These figures are with speakers named. "After Sigma" counts turns since Sigma last spoke.

| Where the line is | Lines | For Sigma | rc0.3 ranks them (AUROC) | Answered now, for Sigma | Answered now, not for Sigma |
|---|---|---|---|---|---|
| Before Sigma has spoken | 2,473 | 154 | **0.995** | 151 of 154 | 14 of 2,319 |
| Right after Sigma, the one who asked | 59 | 29 | 0.86 | 23 of 29 | 7 of 30 |
| Right after Sigma, the other person | 217 | 51 | **0.67** | 19 of 51 | 26 of 166 |
| 4+ turns after Sigma, the one who asked | 286 | 25 | 0.77 | 2 of 25 | 1 of 261 |

The 19 lines that name Sigma without a reply are left out of this table and covered below.

- **The weak spot is the line right after the agent answers.** There, whether a question is a
  follow-up to the agent or talk to the other person is barely in the text.
  - 33 of rc0.3's 64 false accepts are people's lines right after Sigma: 21 questions and 12
    instructions or statements.
  - Thanks and acknowledgements are not the cause (1 of 64).
  - Jev has the same pattern: 46 of its 57.
- **Returning to Sigma after a gap, without the name, is mostly missed.** rc0.3 answers 2 of 25 and
  holds none; Jev holds 56%.
- **The thresholds are not the cause.** A threshold chosen on this test itself would give F1 0.725,
  the same as rc0.3's own (0.724). Only the ranking can gain, and only at the positions above.
- **The label is strict, and that inflates false accepts.**
  - **Sigma answers a turn late.** A line counts for Sigma only if Sigma's turn comes next. In 15
    of rc0.3's 64 false accepts, Sigma speaks two turns later, after another person's turn; across
    all people's lines that happens 6% of the time. Jev: 19 of 57.
  - **Lines that name Sigma without a reply** (19). rc0.3 answers 10 of them outright:
    - 4 are questions put to Sigma by name, counted as not for it because a person speaks next;
    - 4 are a named thanks, which our guide answers briefly (SD-18).

    So by our guide, most of these 10 are right.
  - **Both sides are scored on the same label.** The comparison with TCL's model stands, but part of
    the false-accept gap is the label, not the model.
- **A person alone with Sigma is easier.** rc0.3 answers 70% of those follow-ups (19/27), against
  27% when two people talk (31/114).

## What it means

- **On an independent on-task set, rc0.3 answers now about as well as Jev, and holds a tenth as
  often.** It is not as good as a model trained on that set's own data. The gap is in one place:
  who the line right after the agent's answer is for.
- **It is not a threshold or calibration problem.** It is information, so the fixes are inputs or
  training:
  - **Timing input** (option 2 in the phase 8 note) fits this exactly. A follow-up to the agent
    comes right after the agent stops; a reply to the partner often overlaps or answers what the
    agent said. TCL gives onsets only, so this set cannot test it.
  - **Our own generated follow-ups** (option 3) can now be specific:
    - the other person following up to the agent without its name;
    - people reacting among themselves to the agent's answer;
    - a person returning to the agent several turns later.
    
    TCL's own data cannot be trained on (CC BY-NC, SD-27).
- **The headline numbers stay as published.** This set's text is scripted by a language model and
  spoken by synthetic voices, so it is one more view, not the measure of real calls.
