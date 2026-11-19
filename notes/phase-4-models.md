# Phase 4 notes: the first models

Closed 2026-11-19, 03:40 UTC, after five training rounds overnight. Read this, then [TODO.md](../TODO.md) and
[DECISIONS.md](../DECISIONS.md). How to try a model: [TESTING.md](../TESTING.md). Jon authorized
autonomous work within $1,000 (SD-17).

## Where things stand

**The model to try is `side-r3-ettin-150m-s0`** (round 3, Ettin-150M), exported and already in
`models/` on this Mac. [TESTING.md](../TESTING.md) has the commands and the one-line swap into the
daily-audience demo. It runs at 7 to 14 ms a line on this Mac (11 ms through the demo's gate).

Against scorecard 0.1 it meets 12 of 16 items
([reports/2026-11-19-side-r3-ettin-150m-s0-scorecard.md](../reports/2026-11-19-side-r3-ettin-150m-s0-scorecard.md)):
99.0% right on the main test against Jev's 80.7% (+18.0 points, 16.6 to 19.5), answers outright
0.2% of Duplex-MPE's lines meant for others (Jev 0.4%), holds on 0.9% of them (Jev 16.0%), none of
10,434 AMI silence-test lines answered (Jev 5), 47 of the demo's 48. Not met: item 6 (the pilot's
rhythm-only lines, 22/34 answered at once, Jev 16/34), item 7 (Duplex-MPE lines that only mention
the agent, 0.3% answered outright against a 0.1% bar), item 9 (the pilot's open questions, 17/26
between 0.25 and 0.75; on the main test 96.7%). Item 15 (real speech-to-text) is not built.

Its weakest spot: a request to the agent with no name and no sign earlier that the agent is in the
conversation. It answers 38.8% of Duplex-MPE's (Jev 26.6%, round 1 61%). Saying its name always
works (99.5%).

About $187 of the $1,000 spent (BUDGET.md). Nothing committed.


## What exists now

| Item | Where |
|---|---|
| The model: an Ettin encoder, mean-pooled over everything and over the line alone, plus 31 rhythm and wording numbers, with three heads (intent, respond, unclear) | `sidechat/train/model.py`, `sidechat/train/features.py` |
| Training and scoring jobs (one H100 per size, detached; scoring beside Jev on every set) | `sidechat/pipeline/train.py` |
| Thresholds chosen on dev with two bars on answering outright (generated dev 1%, real AMI speech 0.4%) | `sidechat/train/evaluate.py` (SD-20) |
| Export to ONNX, parity through the shipping runtime, CPU latency, an optional int8 build that ships only if it holds up | `sidechat/pipeline/export.py` |
| The runtime (ONNX Runtime and tokenizers, no torch) | `sidechat/runtime.py` |
| The Pipecat classifier, a drop-in for `JevClassifier` in the daily-audience demo | `sidechat/integrations/pipecat_classifier.py` |
| Scripts to try it: on the demo's lines, and through the demo's own gate | `scripts/try_sidechat.py`, `scripts/try_in_demo.py` |
| AMI meetings without addressee labels: real speech for training, dev and a silence test | `sidechat/sources/ami.py` (`ami-silent`, SD-19) |
| Guide 0.4 and gen-0.2's new kinds | `contracts/sidechat-guide-0.4.md`, `sidechat/guide.py`, `sidechat/gen/planner.py` (SD-18) |
| Scorecard report for a trained model, from stored scoring | `scripts/scorecard_report.py` |
| Tests | `tests/test_phase4.py`, `tests/test_round2.py` |

## Round 1 (exp-017): beats Jev everywhere, answers some people's lines

Ettin-32M, 68M and 150M, 3 epochs on gen-0.1 and gen-pilot. Every size was best at epoch 2 and
overconfident (temperatures 1.2 to 1.45). Decision right, anonymous speakers, against Jev on the
same lines:

| Set | 68M | 150M | Jev |
|---|---|---|---|
| Generated test (2,860 paired lines) | 98.5% | 98.5% | 80.7% |
| Duplex-MPE (52,336) | 96.7% | 96.6% | 83.1% |
| Ambient Bench (15,793) | 96.7% | 96.4% | 85.4% |
| AMI, labelled meetings (8,875) | 97.8% | 97.0% | 85.2% |
| Pilot (265) | 83.4% | 85.7% | 77.4% |
| Demo lines (48) | 46/48 | 45/48 | 47/48 |
| Duplex implicit `T` (a request to the agent with no name) | 61.0% | 57.6% | 26.6% |

It holds for a pause on about 1% of lines meant for others, where Jev holds on 15 to 18%. But it
answers outright 0.8% of Duplex-MPE's and AMI's lines meant for others (Jev 0.4% and 0.01%):
twice item 2's bar. What it answered: bare instructions between people in real meetings ("go
on", a request for the next slide), a presenter's "any questions?", and opening lines with no
history. It also missed answers to the agent's question given after a quick check with someone
else, and held instead of answering a named "thanks" or "that's enough" (the guide called those
even; the demo expects an answer).

Rescored under round 2's rules (exp-021), thresholds alone do not fix it: for 68M the AMI dev
series do not bind, and for 150M the bar pushes answer-now to 0.85, which meets item 2 on
Duplex-MPE but drops the agent's own lines answered at once from 98.6% to 89.3%.

The round-1 68M is exported (exp-018): 274 MB, the same decisions as PyTorch on 283/283 lines, 4
to 10 ms a line on this Mac. It runs through the demo's own gate (`scripts/try_in_demo.py`).

## Round 2: data aimed at round 1's mistakes

- **gen-0.2 (exp-019):** 11,500 conversations under guide 0.4 with bare instructions between
  people, steps explained to people, the meeting's host, answers to the agent after a quick
  check with a named person, and quiet stretches (8% of conversations never involve the agent;
  25% open with 3 to 8 lines of people among themselves).
- **AMI's unlabelled meetings (SD-19):** 15,276 lines of real meeting speech from 20 series that
  share no speaker with the labelled test meetings; 2 series for dev, 4 held out as the silence
  test (item 16). Disfluency augmentation on generated lines keeps "uh" from being a cue.
- **Guide 0.4 (SD-18):** named thanks, stop and goodbye get a short acknowledgement.
- **Thresholds (SD-20):** a second bar, at most 0.4% of real-speech dev lines answered outright.
- **Training (exp-022):** 68M and 150M, 2 epochs, scored on the same generated test as round 1.

**Result:** outright answers to people's lines fixed (Duplex-MPE 0.4%, AMI none, demo 47/48),
but unnamed requests to the agent collapsed: Duplex-MPE implicit `T` 23.0% for 68M (round 1
61.0%). The median such request scored 0.80 in round 1 and 0.06 in round 2: the stay-quiet data
taught that an unnamed request with no agent in the history is for people.

The committee checked gen-0.2's new kinds (exp-024): 95.8% agreement, but bare instructions
between people only 90.2%, every miss in a session the agent runs or controls, where an
instruction may be for it. 42% of them were written there.

## Round 3 (exp-025): those instructions filtered

Round 2 exactly, minus the 1,693 instructions and steps written where the agent leads or controls
things. 150M recovered part of the way and is the best model so far, **`side-r3-ettin-150m-s0`**
(exported in exp-027, in `models/`, the one TESTING.md points at):

| Set (anonymous) | Round 3 150M | Round 1 68M | Jev |
|---|---|---|---|
| Duplex-MPE | 96.7% | 96.7% | 83.1% |
| … for others answered outright | 0.2% | 0.8% | 0.4% |
| … implicit `T` (unnamed request) | 38.8% | 61.0% | 26.6% |
| Ambient Bench | 98.7% | 96.7% | 85.4% |
| AMI labelled meetings | 99.9% | 97.8% | 85.2% |
| AMI silence test, answers per 1,000 | 0 | 5.5 | 0.5 |
| Pilot | 87.4% | 83.4% | 77.8% |
| Demo lines | 47/48 | 46/48 | 47/48 |

68M did not recover (implicit `T` 20.3%). gen-0.3 (exp-026) adds even-call requests after quiet
openings and plans no instructions where the agent leads or controls; round 4 trains on it.

## Round 4 (exp-028, exp-029): gen-0.3 added, no better

| Run | Duplex | Outright on others | Implicit `T` | Ambient | AMI | Pilot | Demo |
|---|---|---|---|---|---|---|---|
| r4 68M seed 0 | 95.2% | 0.4% | 17.1% | 98.1% | 100.0% | 86.7% | 47/48 |
| r4 150M seed 0 | 95.6% | 1.0% | 34.5% | 98.5% | 99.9% | 87.4% | 47/48 |
| r4 150M seed 1 | 95.2% | 0.8% | 28.1% | 98.9% | 99.9% | 87.8% | 47/48 |
| r3 150M (shipped) | 96.7% | 0.2% | 38.8% | 98.7% | 99.9% | 87.4% | 47/48 |

The even-call requests did not bring back unnamed requests, and two seeds of the same run differ
by 6 points on implicit `T`: one run's number on that slice is noisy. Round 5 (exp-030, exp-031)
drops the AMI rows to see whether real meetings' "can you ..." between people is what suppresses
unnamed requests.

**A caveat on these numbers.** The pick between rounds and sizes was made partly on Duplex-MPE,
Ambient Bench and AMI, so the shipped model's numbers on them are a little optimistic. The
thresholds were always chosen on dev. A fresh test (real calls from the demo, SQ-05) would settle
it.

## Round 5 (exp-030, exp-031): without the AMI rows

Round 4's corpus without AMI, 150M, seeds 0 and 1. Unnamed requests partly come back (implicit `T`
47.2% and 36.0%), but outright answers on other speech rise: Ambient 1.6% (round 3 0.2%), the AMI
silence test 2 to 3 per 1,000 (round 3 none, Jev 0.5). AMI is what keeps the model quiet on real
speech. An offline average of round 3 and round 5 seed 0 (from stored predictions, no cost) lands
near round 3 (Duplex 0.1% outright, implicit `T` 39.2%) and is not worth two models a line.

So round 3's 150M stays the pick. If Jon would rather the agent answer more unnamed requests at the
price of more barging in on real speech, `side-r5-ettin-150m-s0` is that trade (export it with
`sidechat.pipeline.export`, about $0.40).

## How things run

```bash
set -a; . ./.env; set +a
uv run modal run --detach -m sidechat.pipeline.train::run --exp <exp> --corpus gen-0.1,gen-pilot,gen-0.2,ami-silent --encoders ettin-68m,ettin-150m --epochs 2 --tag r2 --test-corpus gen-0.1,gen-pilot --extra-sets corpus:gen-0.2:test@anonymous
uv run modal run --detach -m sidechat.pipeline.export::run --exp <exp> --run-id <run_id>
uv run python -m sidechat.pipeline.fetch <run_id>
uv run python -m sidechat.pipeline.results <exp>
```

`--score-only` rescores models already trained under a tag (exp-021).

## Things learned

- **The generated test is too easy to choose between models.** Every size scores about 98.5% on
  it; the differences show on the benchmarks and real speech. Choose on Duplex-MPE, AMI and the
  pilot, not the generated test.
- **The costly mistake hides on real speech.** On generated dev the model answered 0.2% of
  people's lines outright; on real meetings, four times that. The AMI dev series now guard it.
- **Plain dynamic int8 quantization breaks this encoder** (exp-018: probabilities off by up to
  0.995). The export now quantizes weights per channel and only products with a constant side,
  and ships int8 only if it stays within a point of fp32 on dev.
- **The demo's Pipecat (1.16) calls `_ask(state, questions, inputs=...)` and reads `model` as a
  property.** The adapter now matches; `scripts/try_in_demo.py` is the check.
- **Modal CPUs are slow:** 52 ms a line there for 68M, 4 to 10 ms on this Mac.
- **Stay-quiet data has a price.** Every batch of "this is for people" data (AMI, quiet stretches,
  bare instructions) made the agent more reluctant to take an unnamed request when it had not
  spoken yet. Check Duplex-MPE implicit `T` whenever such data is added.
- **Check a new kind with the committee before training on it.** exp-024 caught that 42% of the
  bare instructions were written where the agent could carry them out (about $11).
- **Single runs are noisy on the small slices.** Two seeds of the same run differ by 6 to 11 points
  on implicit `T` and by up to 0.6 points on outright answers. Compare rounds on more than one
  seed before reading much into those slices.
- **The bigger encoder generalises better here.** 150M recovered from noisy data where 68M did
  not, at about twice the cost a line (still about 11 ms on this Mac).

## Loose ends

- The committee was not rerun on guide 0.4 (SD-18 is an agent default for Jon to confirm).
- Duplex-MPE implicit `T` (unnamed requests to the agent) is the weakest benchmark slice: 61%.
- Real speech-to-text twins (item 15) and real calls from the demo (SQ-05) are not built.

## Where the next phase picks up

1. **Jon's morning test** (TESTING.md), then decisions SD-18 to SD-20 and the commit.
2. **Real calls** (SQ-05, item 15's speech-to-text twins): the one test that is fresh for every
   model here, since the pick between rounds used the benchmarks.
3. **Unnamed requests with no agent in the history.** Ideas not yet tried: AMI rows at a lower
   share instead of all or none; generated conversations where the agent's own turns are dropped
   from the history, as Duplex-MPE's manifests do; a guide decision on whether such a request is an
   even call (now) or the agent's (Duplex-MPE's view).
4. **int8:** passes the gate for 150M (98.6% on dev against 99.0%) but not 68M; static quantization
   with calibration might do better.
5. Items 6, 7 and 9 on the pilot and Duplex-MPE `N1` (see the scorecard report).
