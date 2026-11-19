# Pipecat Sidechat: training plan

Draft 1 · 2026-11-18 · not started

Sidechat is a small text classifier for a voice agent that shares a conversation with several
people. For each utterance it answers: was that for me, and should I speak? It is the mirror of
Pipecat Audience (one person, several agents) and reuses Audience's model family, training recipe
and export path.

## 1. Summary

- **Bar:** at least as good as Jev in the `daily-audience` demo on every scorecard item, measured
  on the same lines, and better on the headline (section 3).
- **Model:** Ettin-32M with a small head, as Audience. The main change is that the encoder reads
  several earlier turns, because here nobody tells the model who earlier lines were for (section 4).
- **Data:** new. Audience's 125,001 lines are the wrong shape (section 5.1). The plan is scripted
  multi-speaker conversations from several writer models, real meeting speech from open corpora,
  and real speech-to-text on the test set.
- **Open datasets:** a Hugging Face search found one benchmark that is almost exactly this task
  (Duplex-MPE) and human addressee labels on real meetings (AMI). Details in
  [DATASETS.md](DATASETS.md).
- **Training:** detached H100 runs on Modal, about 17 minutes and about $1.25 per seed at
  Audience's measured rate.
- **Cost:** about $350 to $450, estimated. Labels are the largest part. Proposed cap: $600.

## 2. What the model decides

One call per utterance. Everything except the latest text and the agent's name is optional.

**Input**

| Field | Notes |
|---|---|
| `agent` | Name, aliases (including speech-to-text misspellings), a one-line role |
| `text` | The latest utterance |
| `speaker` | Who said it: a name, or more often an anonymous diarization label such as "Speaker 1". Absent when the transcript is not diarized |
| `history` | Up to 8 earlier turns with speakers, the agent's own lines marked. The model reads their rhythm: who spoke, in order, relative to this line's speaker (SD-13) |
| `people` | Names or labels of the people present. Optional, and usually absent |
| `facts` | Optional: nobody else is present, the utterance was spoken over the agent |

**Output**, all probabilities:

| Field | Meaning |
|---|---|
| `intent.direct` | Said to the agent: by name or role, as "you" in an exchange with it, or as an answer or follow-up to it |
| `intent.indirect` | Wants the agent to act without speaking to it: "Can the assistant summarise that?", "Maybe Atlas knows." |
| `intent.open` | A question or request to nobody in particular that the agent could take if no person does |
| `intent.about` | Mentions the agent and wants nothing from it: "I asked Atlas yesterday." |
| `intent.other` | For a particular person, the group of people, another device, the speaker themself, or a bare acknowledgement |
| `respond` | How likely it is that the agent should speak now. Calibrated; the system using the model sets the thresholds (SD-12) |
| `unclear` | The evidence fits the agent and someone else equally |
| `people` | For each person present, how likely the line was for them. A by-product of the architecture |

The five intents sum to 1. The demo's two numbers map onto them: `addressed` is
`direct + indirect`, and `question` is `open`.

**An even call scores 0.5.** A question to the room that nothing earlier settles should get a
`respond` near 0.5, so the harness can choose to take the floor after a pause. Guide 0.2 calls
this `speak` 3.

**People's names are weak evidence** (SD-14). Diarization labels are often anonymous, and people
do not call each other by them. A name in a line that is not the agent's says the line is for
someone else, not who. The agent's own name is the reliable signal.

`respond` is not the same as "addressed". "Thanks, Atlas." is direct but a reply is optional.
"Let's see if Atlas knows." is not said to the agent but invites it. Those are the lines where a
graded probability is worth more than a yes or no.

**Out of scope:** when a turn has ended (the turn model does that), the 2.5 s silence rule for open
questions (the application does that), audio and video cues, and languages other than English in
the first release.

## 3. The bar: Jev in the demo

### 3.1 What Jev does today

From `~/Sites/daily-audience` at commit `73171de`:

- Jev (TypeSafe's hosted classifier) gets the names of the people on the call, the last 8
  utterances and the latest one, and answers two yes/no questions: *said to the bot?* and *an
  unanswered question open to anyone?*
- The gate answers at once when `addressed ≥ 0.8`, waits 2.5 s for silence when `question ≥ 0.5`,
  and otherwise stays quiet. With one person on the call it always answers.
- The call site is one function, `AddressingMonitor.classify` in `server/addressing.py`. A local
  model can replace Jev there without touching the gate.

### 3.2 Measured today

I ran the demo's own `scripts/try_addressing.py` (33 lines, two people and "Atlas"):

- **Latency:** 134 to 310 ms per call from this machine, typically about 170 ms. The demo's README
  says about 140 ms.
- **Clear cases:** all right. Names said to the bot score 0.85 to 0.98. Names said about it score
  0.02 to 0.18.
- **Soft spots:**

| Line | Jev | What happens |
|---|---|---|
| "Should we ask Atlas?" | addressed 0.05, question 0.92 | Bot answers after a silence. The demo lists this as a line it should ignore |
| "Could you send me that file after the call?" | addressed 0.09, question 0.73 | Bot answers after a silence |
| "Is it just me or is the audio a bit choppy?" | addressed 0.07, question 0.93 | Bot answers after a silence |
| "Can you look up the weather in Paris for me?" | addressed 0.51 | Waits instead of answering |
| "Thanks!" after the bot's answer | addressed 0.73 | Just under the 0.8 threshold |

33 lines is a smoke test, not a measurement. Phase 0 measures Jev properly.

### 3.3 How "at least as good" is decided

Every item is scored for Sidechat and for Jev on the same lines, and the difference is tested
line by line. The statistical rule is Audience's: a paired bootstrap of 1,000 resamples, a
difference counts when it is 0.1 points or more on a set of at least 30 lines, and "worse" means
the whole interval is below zero.

Jev is scored with the demo's exact questions and state, and its scores are stored with the date
and model version so the baseline cannot drift. It is also scored with thresholds re-tuned on our
dev set, so Sidechat is not only beating the demo's threshold choices.

**The scorecard is frozen as [contracts/scorecard-0.1.md](contracts/scorecard-0.1.md)** (SD-16):
20 items with Jev's measured numbers, anonymous speakers as the headline condition. The draft
below is kept for the record.

**Draft scorecard (superseded by scorecard 0.1):**

| # | Item | Target |
|---|---|---|
| 1 | Decision right (answer now, hold for silence, stay quiet) on the main test | ≥ Jev, and better beyond noise |
| 2 | Answers a line that was for a person | ≤ Jev, and ≤ 1% |
| 3 | Misses a line said directly to it | ≤ Jev, and ≤ 2% |
| 4 | Name said about the agent, not to it | ≥ Jev |
| 5 | Follow-up to the agent with no name | ≥ Jev |
| 6 | "You" said to a person right after the agent spoke | ≥ Jev |
| 7 | Open questions found | ≥ Jev |
| 8 | Calibration error per head | ≤ 0.05 |
| 9 | Real speech-to-text lines against clean text | Gap ≤ 3 points, and ≥ Jev |
| 10 | Unseen writer, unseen settings, unseen agent names | ≥ Jev on each |
| 11 | Real meetings with a silent agent added: false answers per 1,000 utterances | ≤ Jev |
| 12 | Duplex-MPE and Social AI Ambient Bench, never trained on | ≥ Jev |
| 13 | The demo's 17 Pipecat Evals scenarios, 5 runs each, Sidechat in Jev's place | Pass rate ≥ Jev's the same day |
| 14 | Speed on CPU, one utterance | p95 ≤ 30 ms on 4 threads, ≤ 60 ms on 1 |
| 15 | Size and export | ≤ 150 MB full precision; ONNX matches PyTorch on ≥ 99% of lines |

Every item is scored in three conditions: anonymous speaker labels with no list of people (the
headline), real names, and no labels at all.

## 4. Model

### 4.1 What Audience is

Checked in `spellspeak/model-training` (`audience/lib/twotower.py`, `harness/addressee/features.py`):

- One Ettin-32M encoder used twice. A **card tower** encodes each person's card once (96 tokens)
  and caches it. A **line tower** encodes the line (64 tokens).
- A head scores each person from the two encodings, a token-level match between line and card, and
  a 26-number vector per person. Two more heads give `unclear` and `group`.
- The line tower sees the current line and the text of **one** earlier line. Everything else about
  the conversation arrives as numbers, and those numbers rely on the application knowing who each
  earlier line was said to.
- A single-pass version exists (`audience/lib/finetune.py`). It was rejected for speed: 18.7 to
  65.2 ms against a 10 ms bar.

### 4.2 What changes for Sidechat

| Part | Audience | Sidechat |
|---|---|---|
| Cards | People who might be addressed, with what the speaker can see | The agent (name, aliases, role). Person cards only when real names are known; with anonymous labels they carry nothing (SD-14) |
| Line tower | Line plus one earlier line, 64 tokens | Line plus several earlier turns tagged by role: `[agent]`, `[speaker]`, `[other1]`... (`sidechat/context.py` `render`). Length is experiment 1 |
| Per-person numbers | Distance, gaze, group, conversation state, word-match signals | Is the agent, spoke last, turns since they spoke, asked something still open, name called or only mentioned |
| Per-line numbers | People count, group words, room words | The rhythm (`sidechat/context.py` `rhythm`): turns since the agent spoke, whether its last turn asked something, whether this speaker was its last partner, whether the speaker spoke last; plus speaker known, second-person words, question form, group words, spoken over the agent |
| Heads | Person, unclear, group | Person, unclear, plus `intent` (five-way) and `respond` |
| Loss, calibration | Soft targets, one temperature per head | Same |

Why the line tower grows: in a game the application knows who every earlier line was for. In a
call nobody does. "And how many people live there?" is for the agent only because the agent just
answered, and the model has to read that from the earlier turns.

Earlier speakers go in as roles relative to this line's speaker (`agent`, `speaker`, `other1`,
`other2`), not names, so the input is the same whether diarization gives names or "Speaker 1",
and a name in the history is never mistaken for a name being called in the line. Audience left
speaker names out for the same reason. The committee pilot showed why the rhythm matters: most of
its disagreements turned on whether the speaker was the person the agent had just answered.

### 4.3 Experiment 1: how much history, and which layout

Each is two seeds. All four cost about $10 together.

| Run | Layout | History | Line tokens |
|---|---|---|---|
| E1 | Two-tower, as Audience | 1 turn | 64 |
| E2 | Two-tower | 4 turns | 160 |
| E3 | Two-tower | 8 turns | 256 |
| E4 | Single pass, cards and turns together | 8 turns | 384 |

The best scorecard wins, and speed breaks ties. Single-pass is back in the running for two
reasons. In Audience's first comparison it scored higher than the two-tower layout (81.1% against
71.9% of answers wholly right) and was dropped only for speed. And here there are far fewer cards
and the speed bar is 30 ms, not 10. Ettin-68M is a fallback only: Audience's report says it "was
no better at any data size".

## 5. Data

### 5.1 Why Audience's data is not enough

I summarised all nine corpora downloaded from R2 (`audience-data/`):

- 125,001 lines in 18 settings, all game worlds.
- 94% are one player speaking to characters. Sidechat's commonest case, people talking to each
  other with an agent listening, is absent.
- Median line is 8 words. No line has more than 2 earlier lines.
- The labels answer "which character?", not "should I speak?".

It stays useful as a side experiment: pick one character as "me" and re-read each label as for me
or not. That costs nothing to try and is not on the main path.

### 5.2 Three sources

**A. Scripted conversations (the bulk).** Code writes a plan for a whole conversation, a writer
model writes the lines, and the label comes from the plan. This is Audience's method applied to
whole conversations instead of single lines.

- A plan has a setting, 2 to 6 people, an agent, and 12 to 30 beats. Each beat fixes the speaker,
  who it is for, and the kind of line.
- Every human beat becomes one row: up to 8 earlier turns, the line, the label. About 12,000
  conversations give about 170,000 rows before twins.
- **Settings:** work meetings, sales and support calls with two customers, classrooms and study
  groups, family kitchen or car with an assistant, podcasts with an AI co-host, tabletop games with
  an AI game master, telehealth with a relative present. Two settings are held out for test.
- **Agents:** many names, including ones that are common words or sound like other words, and
  unnamed agents ("the assistant"). A share of names is held out for test.
- **Writers:** at least three model families: the open-weights teacher Audience used, on Modal, plus two API
  models. One family writes test conversations only. Audience's weakest slice was lines worded
  unlike its training data (59% to 65% right), and it had one writer.

Kinds of line the plans cover:

| Group | Kinds |
|---|---|
| For the agent | Name first, in the middle or last; role ("assistant, …"); wake phrase; follow-up with no name; answer to the agent's question; correction ("no, I meant…"); stop or dismiss; thanks |
| Indirect | "Can the assistant…?", "Maybe Atlas knows", "Let's see what the AI says", a relayed request |
| Open | "Does anyone know…?", a plain factual question to no one, a request with an unclear "you" |
| About the agent | Reported ("I asked Atlas yesterday"), judged ("Atlas got that wrong"), quoted, hypothetical ("should we ask Atlas?") |
| For people | Statement, question to a named person, reply, "you" to a person right after the agent spoke, people discussing the agent's answer |
| Nobody | Thinking aloud, bare acknowledgement, talking to someone off the call, another device ("Hey Siri…") |
| Mixed | Aside then request ("Not sure. Atlas, what is…?"), thanks then a turn to a person |
| Fragments | Name then a pause, interim transcripts cut mid-sentence |

Three constructions built in from the start:

- **Minimal pairs.** The same line under two histories: after the agent's answer it is for the
  agent, after Sam's answer it is for Sam. These teach context instead of keywords.
- **Explicit and implicit pairs.** Each request to the agent with and without its name. Duplex-MPE
  is built this way, which makes the two comparable.
- **Lines that break their plan are kept**, marked for the committee, never dropped. Audience
  learned that filtering with the rules' own matcher makes the rules look perfect.

**B. Real speech from open corpora.** Details and licences in [DATASETS.md](DATASETS.md).

- **AMI with addressee labels** (CC BY 4.0): 8,876 utterances from 22 meetings where a human
  annotator marked who each was for. Each of the other three participants in turn plays "me",
  which gives real-speech rows labelled for me, for someone else, or for everyone. Some meetings
  are held out as a real-speech test.
- **All of AMI as a silence test:** add a silent agent to 139 real meetings. Every line is for
  someone else, so any answer is a false one. This is scorecard item 11.
- **Splices:** real excerpts from AMI and the Dinner Party Corpus with one written line to the
  agent inserted. Labels checked by the committee.
- **Request wording:** MASSIVE, SLURP and CLINC150 hold tens of thousands of things people say to
  assistants. They seed what the requests in source A are about, and the same request said to a
  person makes a hard negative.

**C. Real calls from the demo.** The gate already reports every utterance with speaker, text and
Jev's scores. Add an opt-in log, record a few internal calls with everyone's consent, and label
them. Target: 300 to 1,000 utterances as a test slice. Audience's card lists "has not met real
users yet" as a limit, and this is the direct fix.

### 5.3 Twins and noise

- **Speaker labels:** most training lines use anonymous labels ("Speaker 1") and no list of
  people, as diarized transcripts do (SD-14). Some keep real names and some have no labels. Every
  test line is scored in all three conditions.
- **Real speech-to-text:** test lines and a sample of training lines are spoken by a TTS voice and
  transcribed by Deepgram, with and without name hints. Audience used synthetic noise only; its
  plan names real STT as the fix if generated lines prove too clean. Names misheard as words
  ("at last") come out of this for free.
- **Wrong speaker:** on a few percent of training lines the speaker tag is swapped. The demo
  credits the wrong person when people overlap.

### 5.4 Held out, never trained on

| Set | Size | Why |
|---|---|---|
| Duplex-MPE | 4,000 scenarios, about 26,000 human turns per condition | Independent, same task, per-turn labels |
| Social AI Ambient Bench | 16,222 turns | Chat-style banter: tests staying quiet |
| MeetingToM, "you" task | 300 records | Who "you" refers to in real meetings |
| Held-out AMI meetings | To be set | Human labels on real speech |
| Real demo calls | 300 to 1,000 utterances | Real use |
| One writer family, two settings, a share of agent names | From source A | Wording and settings never seen |

Splits are by conversation, never by line.

## 6. Labels

- **Guide first.** A written guide whose rules are also code, as Audience's are. Phase 1 pilots it
  on 300 lines and revises it before any corpus is built. Audience changed one rule twice after
  pilots.
- **Training labels** come from the plan. Lines that broke their plan get one labeller.
- **Dev and test labels** are the majority of a committee of three large models, on about 5,500
  lines. A line trains or tests under its plan label only where the committee agrees with it.
- **`respond` is graded.** Each member rates it on five steps. The target is the mean, so a score
  of 0.7 means about 70% of careful readers would have the agent speak.
- **Jev is not on the committee.** It is the baseline, and a baseline that votes on the test
  labels is scored against itself. Audience's committee already dropped its TypeSafe member.
- **Third member from a third family.** Audience's replacement member agreed with the other two on
  only 63% of lines, so its labels were in practice two models'. Use a third model family here.
- **Human check.** Jon labels about 300 to 500 lines: a sample of every slice and every line where
  the committee split. Where it matters, this set decides the Jev comparison.
- **Batch APIs with a sync fallback and a prompt hash check**, lifted from Audience. Its batches
  stalled twice and a cache was written instead of read, which is why labels cost 2 to 3 times the
  forecast.

## 7. Training on Modal

**Recipe:** Audience's r3 recipe unchanged to start: 3 epochs, encoder lr 5e-5, head lr 1e-3, batch
32, two seeds, lowest dev loss kept, one temperature per head fitted on dev, people shuffled into
a new order every batch.

**Detached runs.** Audience's `train.py` is not safe to detach: the laptop starts each run, waits
for it and writes the results file locally. Two changes:

1. Each training function writes its own scorecard and checkpoint to R2
   (`runs/side/results/<exp>/`, `models/side/<run_id>/`).
2. The driver that starts the seeds and gathers them is itself a Modal function.

Then:

```bash
set -a; . ./.env; set +a
```

```bash
uv run modal run --detach sidechat/pipeline/train.py --corpus-id side-corpus-0.1 --label-id side-corpus-0.1-committee --layout tt --history 4 --seeds 0,1 --epochs 3 --h100 --exp exp-004-side-train-r1
```

```bash
uv run python sidechat/pipeline/results.py --fetch exp-004-side-train-r1
```

**Where it runs:** this project's `.env` already points at Modal workspace `jptaylor`, environment
`waystone`, and the R2 bucket Audience used. Audience's jobs refuse to start in any other
environment and build their secrets from `.env` at launch. Sidechat keeps that and uses its own
names: apps `waystone-side-<stage>`, R2 prefixes `runs/side/` and `models/side/`.

**Rounds:** r1 is experiment 1. After that each round adds data for the weakest slices and
retrains, as Audience did (r2 added simple lines, r3 added questions to the room).

## 8. Export, runtime and the demo

- **Export:** ONNX in full precision plus the 16-bit copy, checked against PyTorch on 600 test
  lines, timed on this Mac and on a Modal CPU. Core ML later with the script in
  `spellspeak/models`.
- **Runtime:** a small Python package that ships with the model (rendering, the numbers, the rules
  baseline, the ONNX runner) and has no torch dependency.
- **In the demo:** `ADDRESSING_BACKEND=jev|sidechat` in `daily-audience`, switching what
  `AddressingMonitor.classify` calls. Then the 17 Pipecat Evals scenarios run both ways.
- **Release:** `pipecat-ai/sidechat` on Hugging Face, Apache-2.0, a card with measured numbers only.

## 9. Phases

| Phase | Work | Done when |
|---|---|---|
| 0. Setup and baseline | Scaffold the repo, lift the reusable code, write the request and answer schema, score Jev on Duplex-MPE, the Ambient Bench and a 300-line pilot, add the opt-in log to the demo | Jev's numbers are in a report and the size of the gap is known |
| 1. Guide and scorecard | Labelling guide 0.1 with rules as code, committee pilot on 300 lines, freeze the scorecard | Committee agrees with the guide on ≥ 90% of pilot lines |
| 2. Corpus 0.1 | Generator, a 500-conversation pilot read by hand, then the full run, twins, AMI rows, splices | Manifests in the repo, data in R2, a sample page reviewed |
| 3. Labels | Committee on dev and test, one labeller on flagged training lines, Jon's check set | Label sets in R2, agreement reported per kind |
| 4. First models | Experiment 1, detached, two seeds each, scored against Jev and the rules baseline | A layout is chosen and the first paired scorecard exists |
| 5. Rounds | Top up the weakest slices and retrain, up to three tries per item | Every scorecard item met, or a note explaining what is not |
| 6. Real speech | STT round trip, real calls, the AMI silence test | Items 9 and 11 measured |
| 7. Ship | Export, speed, runtime, demo A/B, card, release candidate | Item 13 measured and `rc1` tagged |

Phases 0 and 1 are about a day. Audience went from first model to its second release candidate in
two days of sessions, so a week is a fair estimate for the rest. The real-calls slice depends on
people being free for calls.

## 10. Budget (estimates)

| Item | Estimate | Basis |
|---|---|---|
| Jev baseline scoring | < $5 | Audience's repo records $0.042 per million input tokens; check the current price |
| Generation on Modal (open-weights teacher) | $8 | Audience: about $1.60 per 7,700 scenes; whole conversations are longer |
| Generation by API writers | $80 | About 6,000 conversations; depends on the models chosen |
| TTS and STT round trip | $40 | About 6,000 lines |
| Labels | $200, range $120 to $350 | Audience paid about $11 per 1,000 committee lines when the batch APIs worked and about $52 when a batch stalled and ran live |
| Training and scoring | $40 | Audience: about $2.50 for two H100 seeds plus CPU jobs |
| **Total** | **about $370** | Proposed cap $600 |

Audience's track cost about $218. Its first round came to about $105 against a $65 forecast, and
labels were most of every overrun. This budget prices labels at what they actually cost.

## 11. Risks

| Risk | What to do |
|---|---|
| The grey zone has no single right answer | Graded `respond`, committee vote shares, Jon's check set, and a guide piloted before the corpus |
| Written conversations do not sound like real ones | Three writer families with one held out, real AMI speech in training, real calls and Duplex-MPE in test |
| Our test favours our own generator | Three test sets we did not write (section 5.4), each also scored for Jev |
| Jev changes under us | Store its scores with date and version, re-run only on purpose |
| Speaker tags are wrong in real calls | Swapped-tag training noise and a no-tags test column |
| Longer input is too slow | Experiment 1 measures it; the two-tower layout with 4 turns is the fallback |
| Labels overrun again | Priced at observed rates, sync fallback ready, pilot before the full set |
| A Hub licence tag is wrong | Check each source's own licence before use; training takes permissive licences only |

## 12. Decisions for Jon

Each has a default the plan assumes.

1. **Where this lives.** Default: this folder as its own repo, lifting the reusable code from
   `spellspeak/model-training` at a pinned commit. Alternative: a new track inside that repo.
2. **The output.** Default: five intents, `respond`, `unclear`, and per-person scores (section 2).
3. **Training on Jev's answers.** Default: no. Jev is only the baseline, pending a read of
   TypeSafe's terms.
4. **Speed bar.** Default: p95 ≤ 30 ms on 4 threads. Audience's was 10 ms, which rules out reading
   8 turns.
5. **Recording team calls** for the real-calls test slice. Default: yes, opt-in, internal only.
6. **Share-alike and non-commercial datasets.** Default: kept out of training (Critical Role,
   MultiTalkBench, Intelligent Wakeup, MeetingBank).
7. **Release.** Default: `pipecat-ai/sidechat`, Apache-2.0, English only for `rc1`.
8. **Spend cap.** Default: $600.

## Appendix: what to lift from Audience

From `spellspeak/model-training`, `main` at `c1f4d99` (rc2's code is at tag
`spellspeak-audience-rc2.2`):

| Use | Files |
|---|---|
| Model and training loop | `audience/lib/twotower.py`, `finetune.py`, `models.py` |
| Scoring | `audience/lib/score.py` (intervals, paired differences, calibration error) |
| Committee | `audience/lib/labellers.py`, `committee.py`, `sets.py`, `audience/pipeline/label.py` |
| Generation job | `audience/pipeline/generate.py`, `audience/lib/corpus.py` (noisy twins) |
| Modal jobs | `audience/pipeline/train.py`, `export.py`, `latency.py`, `package.py`, `publish.py`, `infra/images.py`, `infra/teardown.py` |
| Runtime pattern | `harness/addressee/` (`render.py`, `features.py`, `rules.py`, `classifier.py`) |

Tied to the game setting and rewritten here: person cards with visible features, spatial facts
and `bands.py`, the 18 settings, the kinds and rules in guide 0.3, and the rules baseline's word
lists.
