# The agent's name as heard: what is left to recover

2026-11-20. exp-062. Follows [the phase 6 names report](2026-11-19-side-phase6-names.md). Counts
with 95% intervals. No line is quoted; the only words shown are what speech-to-text wrote in place
of the name.

## The question

With Deepgram's keyterm, rc0.3 answers 48 of SLURP's 61 named test requests as heard. It answers
every one whose transcript has "Olly" (48 of 48) and none of the 13 whose transcript lost it. So the
loss is in speech-to-text. Can a fix in text (the runtime, or training) recover the name from what
the service wrote, without answering people's own lines?

## A dev set, so the test stays the test

SLURP's train and devel utterances that say "Olly", every recording of each, were heard by Deepgram
nova-3 twice, plain and with `keyterm=Olly`. That is 449 utterances: 507 close-talk headset
recordings and 727 far-field ones. SLURP's audio is CC BY-NC: these are for measuring only, never
training (SD-23). Sets `names-dev`, `names-dev-stt` and `names-dev-stt-keyterm`
(`sidechat/sources/slurp.py`, `stt_slurp.run --split dev`).

## What speech-to-text writes for the name

| | Headset | Far-field |
|---|---|---|
| Name written, plain | 3.0% (15/507; 1.8 to 4.8) | 0.1% (1/727; 0.0 to 0.8) |
| Name written, with the keyterm | **81.5%** (413/507; 77.8 to 84.6) | **68.8%** (500/727; 65.3 to 72.0) |

The headset figure matches the test split (48/61, 78.7%).

**Plain:** the name comes back as another spelling. On headset recordings, "oli" 166 times, "ollie"
100, "ali" 12, "holly" 10. Next most common are "only" (34) and dropped entirely (78).

**With the keyterm:** the spellings are gone. What is left of the 94 headset misses:

- **Dropped entirely:** 49, 52.1% (42.1 to 61.9).
- **Common words:** "only" 12, "you" 5.
- **Another assistant's name:** a few speakers said "Siri", "Alexa" or "Cortana" where SLURP's text
  says "Olly".

Far-field misses look the same: dropped 57, "only" 37, "you" 24.

## Can text bring it back?

The candidate fix restores the agent's name when a word one letter from it (or the same by a simple
sound key) stands where people call someone: the first word, after an optional "hey" or "okay", or
the last word. It comes in two strengths:

| | Recovered, headset, keyterm | Recovered, far-field, keyterm | Recovered, headset, plain | Fires wrongly on people's lines if the agent is "Olly" |
|---|---|---|---|---|
| Comma required ("Oli, …") | +0.2 points (1/507) | +0.1 (1/727) | +41.8 (212/507) | AMI heard 0/8,202, Ambient 0/16,222. But 32 of 98 generated lines that call a person whose name is close to the agent's |
| No comma needed | +2.6 (13/507) | +5.5 (40/727) | +63.9 (324/507) | AMI heard 0.2% (14/8,202), Ambient 0.2% (25/16,222); for "Sam", up to 0.65% |

Each wrong fire puts the agent's name into a person's line, which the model then answers outright.

- **With the keyterm, the comma rule recovers almost nothing.** The keyterm already fixes the
  spellings the rule would catch.
- **The no-comma rule recovers 3 to 5 points but answers people.** For an agent called Olly, it
  would answer about 1 in 600 of people's own lines outright, half of item 2's whole allowance
  (0.4%). Every line starting with "Only…" counts, and short names (Sam, Max) are worse.
- **Without a keyterm, the comma rule does help** (3% to 45% on headsets). But the keyterm alone
  reaches 81.5%, so the advice stays: use the keyterm.

## What it means

- **With the keyterm, names as heard are at the ceiling of what text can do.** Half the remaining
  misses have no trace of the name in the transcript. Most of the rest are ordinary words that
  people also say to each other.
- **Ship no rule.** The model and runtime stay as they are, and the card's advice (pass the name as
  a keyterm) is the fix.
- **Further gains have to come before the text:**
  - a speech-to-text service or setting that keeps the name more often (measurable on this dev set
    for about $0.30 a configuration);
  - wake-word spotting on the audio.
- **Far-field audio (a room device) loses the name more often than headsets** (69% against 82%
  kept). Pipecat's usual case, each person on their own microphone, is the headset row.

## Cost

About $0.90: Deepgram about $0.58 (two passes of 68 minutes), plus Modal. That includes two
downloads Zenodo cut part way. The job now resumes a cut download and keeps the chosen recordings
in R2, so a second pass reads them from there.
