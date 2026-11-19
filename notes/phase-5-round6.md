# Phase 5 notes: round 6, and a model for `agent-1x`

2026-11-19. Jon asked for round 6 (the gaps more data can close) and a plan to fit the model on
Pipecat Cloud's `agent-1x` (0.5 vCPU, 1 GiB), then went out; this ran headless on Modal.

## Where things stand

- **No small model passes every gate yet; round 3 (`side-r3-ettin-150m-s0`) stays the pick.** The
  full write-up, with the table against Jev and the latency summary, is
  [reports/2026-11-19-side-round6-agent1x.md](../reports/2026-11-19-side-round6-agent1x.md).
- **Speed is solved by the two-tower design.** With the history encoded while the person talks, a
  two-tower Ettin-32M takes 10 to 15 ms a line on agent-1x in fp32 (488 MB), against Jev's 56 to
  163 ms; 88 to 117 ms if the history is not ready. The single-tower 150M takes 0.5 s there.
- **Accuracy is not.** The students match round 3 on Duplex-MPE overall (within 1.0 to 1.4
  points), AMI, Ambient and the pilot, but answer only 6% to 20% of unnamed requests (round 3
  38.8%, Jev 26.6%), and named requests swing with the seed (87.8% to 99.5%).
- **Round 6 did not beat round 3** (item 9 met in one seed, item 7 worse in both).
- Nothing is running on Modal. About $291 of the $1,000 spent. Nothing committed.

## The plan

### Round 6: data for items 6, 7 and 9

From the r3 model's misses, read by kind and tag only (no test text):

- **Item 6:** in the pilot, unnamed follow-ups to the agent were missed 6 times in 9, mostly held
  at about 0.5, and unnamed commands and requests inside an exchange with the agent 6 times in 6
  (`command_no_name`, `reply_then_request`, `resume_no_name`). The planner only ever placed a
  follow-up directly after the agent answered that person, and planned commands rarely (weight 1.5
  against 7).
- **Item 7:** 13 of Duplex-MPE N1's 17 outright answers are statements to another person,
  mentioning the agent, right after it spoke. Nothing in the planner made that line.
- **Item 9:** even calls out of the 0.25 to 0.75 band in both directions, a few of each kind.

gen-0.4 (exp-035) adds `follow_up_after_reaction` (G6: the person the agent answered carries on
with it after someone else's brief reaction) and `relay_agent_answer` (G4: a person tells another
what the agent just said, by name), and raises unnamed commands, replies with requests,
corrections, even calls and follow-ups by someone else (the contrast to a delayed follow-up). The
new kinds go to the committee before their numbers are trusted. Round 6 trains Ettin-150M on round
3's corpus plus gen-0.4, two seeds; gen-0.3 stays out (round 4: it raised outright answers).

### `agent-1x`: why quantization alone will not do

exp-033 measured the r3 model on Modal containers capped like the profiles. With 8 earlier lines,
the int8 build took 532 ms a line on 0.5 vCPU, and int8 was barely faster than fp32 on 1 vCPU
(271 against 253 ms): dynamic int8 saves memory more than time on these CPUs. Jev's round trip from
the same data centre was 55 to 150 ms. The time goes on encoding the history, which is 4 to 5 times
a bare line. So the plan, folding in Jon's five steps and his two-tower idea:

1. **Two towers, history cached.** The history and the line are encoded apart by one shared encoder
   (`TwoTowerModel`, input `sidechat-tt-0.1`). The history for line N is known when line N-1 ends,
   so its encoding is made while the person talks; when they stop only the line (about 30 tokens)
   is encoded and read against the cached history through one cross-attention layer. History
   slots are fixed by first appearance ([p1], [p2]) so they do not depend on who speaks next; the
   rhythm numbers, cheap at the end, still read the turns relative to the speaker.
2. **Distil into a small encoder.** Ettin-32M (and 68M) students copy the 150M teacher's
   calibrated probabilities on the same augmented lines (80% teacher, 20% labels), over round 6's
   corpus plus gen-0.3, which the teacher relabels.
3. **A short single-tower fallback.** Ettin-32M on at most 4 earlier lines in 160 tokens, distilled
   the same way, in case the two towers lose accuracy.
4. **Optimize, then int8.** The export runs ONNX Runtime's transformer optimizer on each graph (kept
   only if parity holds and it is faster on one thread), then int8 per channel behind the existing
   quality gate.
5. **One thread.** The Pipecat adapter now defaults to 1 ONNX thread.
6. **The gate.** Ship a student only if, on the `agent-1x` harness, its full-window median beats
   Jev's from the same profile, and it is within about a point of the 150M teacher on Duplex-MPE,
   AMI and the pilot.

## Results so far

- **gen-0.4** (exp-035, about $20): 7,296 conversations, 102,443 labelled lines; 1,970 broke
  their brief and are left out, mostly the old "about the agent" kinds.
- **The committee agrees with gen-0.4's labels on 98.8%** (exp-037, 326/330; 96.9 to 99.5):
  `follow_up_after_reaction` 98.3% (118/120), `relay_agent_answer` 99.2% (119/120),
  `reply_then_request` 100% (47/47), `command_no_name` 97.7% (42/43). Nothing is left out of the
  students' corpus. About $10.
- **The two-tower code runs end to end** (exp-036 smoke: 32M, 4,000 lines, one epoch). On an
  unthrottled Modal core, the line alone with the history cached takes 15 to 17 ms, both towers
  cold 55 to 61 ms (fp32, one thread).
- **A runtime bug, found and fixed.** The first two-tower exports disagreed with PyTorch (largest
  difference 0.53). Not the graph: a fast tokenizer keeps the truncation of its last call, and the
  exported tokenizer.json had kept the line's 96 tokens, so the runtime cut every history to 96.
  Single-tower exports were spared only because their last call used their own `max_len`. The
  runtime now turns truncation and padding off, and the export saves the tokenizer with both off.
  `sidechat/pipeline/parity_probe.py` (PyTorch batched, PyTorch line by line, runtime) went from
  0.40 to 6e-6. Two things follow:
  - exp-042 was already running with the old code, so its exports and timing of the two-tower
    students are not trusted. exp-050 waits for it, re-exports and re-times them, and writes the
    summary to read.
  - Anyone porting a two-tower model (the Pipecat module) must load the tokenizer with
    truncation off too.
- **Round 6 does not beat round 3** (exp-038, exp-039; scorecards in `reports/`). Seed 1: 12 of 16
  (meets item 9, 21/26 even calls in range; misses item 5, unnamed requests 22.8% against Jev's
  26.6%). Seed 0: 11 of 16 (misses item 2, 0.45% outright). Both: item 6 nudged (pilot G6 22 to
  24-25 of 34, inside the noise) and item 7 worse (N1 outright 0.28% to 0.35-0.54%). The seeds tie
  on dev to one line; the rule took seed 1 as teacher.
- **Students of round 6's seed 1 fail the gate** (exp-048, exp-049): all within a point on
  Duplex-MPE and AMI, all 2.6 to 3.0 points below it on the pilot.
- **Students of round 3** (exp-051): the two-tower 68M passes the stated gate (Duplex-MPE -0.9,
  AMI +0.1, pilot +0.0 points; 23 ms a line on agent-1x with the history encoded beforehand, Jev
  163 ms in that run). But its full scorecard is 10 of 16: it answers only 87.8% of Duplex-MPE's
  named requests (171 of 2,000 scored below 0.1; round 3 99.5%, Jev 99.2%) and 19.5% of unnamed
  ones. The 32M answers 98.7% of named requests but 10.7% of unnamed ones, and is 1.04 points below
  round 3 on Duplex-MPE. **The stated gate is too loose:** named requests are a small share of
  Duplex-MPE's lines, so a model can lose a tenth of them and stay within a point. The gate to use
  is the stated one plus items 4 and 5 not worse than the teacher.
- **exp-052 and exp-053 are running**: the round 3 students again with seed 1, and with the labels
  weighted more (teacher share 0.5). They say whether the 68M's named-request misses are the seed,
  and whether the labels keep items 4 and 5.

### Speed against Jev on agent-1x (0.5 vCPU, 1 GiB)

Median ms a line through the demo's gate, one thread; the history (8 earlier lines) encoded
beforehand for the two-tower models, as while the person talks.

| Model | Build | Memory | Short history | Full history | Full history, history not ready | Encoding the history |
|---|---|---|---|---|---|---|
| Two-tower 32M (r3 teacher) | fp32 | 488 MB | 7 | 10 | 88 | 76 |
| Two-tower 68M (r3 teacher) | int8 | 557 MB | 21 | 23 | 211 | 190 |
| Two-tower 32M (r6 teacher) | int8 | 416 MB | 8 | 11 | 97 | |
| One-tower 32M, 4 earlier lines | fp32 | 357 MB | 23 | 100 | | |
| Round 6 150M (today's design) | int8 | 573 MB | 97 | 508 | | |
| Jev (an API call) | | 114 MB | 53 to 159 | 56 to 163 | | |

Jev's median moved between 53 and 163 ms from one container to the next (network); the student
numbers held within a few ms across runs. The two-tower p90 on agent-1x is about 60 to 75 ms,
because in the bench the history is encoded just before the line and uses up the half-core's
quota; in a call it is encoded seconds earlier. On agent-2x the 68M int8 takes 25 ms and its
history 101 ms.

## How things run

```bash
set -a; . ./.env; set +a
uv run python -m sidechat.pipeline.results exp-042-side-round6        # the chain
uv run python -m sidechat.pipeline.results exp-050-side-round6-reexport  # the export and gate to trust
```

`sidechat/pipeline/round6.py` chains every step (`--steps`, `--teacher`, `--wait-for`,
`--suffix` to rerun part of it). Each step's own report is in R2 under its experiment.

## Final results

| Run | What | Outcome |
|---|---|---|
| exp-035 | gen-0.4, 102,443 lines | done, $20 |
| exp-037 | committee on gen-0.4's new kinds | 98.8% agreement |
| exp-038, exp-039 | round 6, 150M, two seeds | 11 and 12 of 16 items; does not beat round 3 |
| exp-048, exp-049 | students of round 6 seed 1 (two-tower 32M/68M, short 32M) | fail the pilot by 2.6 to 3.0 points |
| exp-051 | two-tower students of round 3, seed 0 | 68M passes the stated gate, misses 12% of named requests; 32M 1.04 points short on Duplex-MPE |
| exp-052 | the same, seed 1 | named requests fixed for 68M, broken for 32M; 68M int8 failed, fp32 too slow |
| exp-053 | the same, labels weighted more | no better on unnamed requests |
| exp-042, exp-050 | the chain, and its exports again after the tokenizer fix | |

## What exists now

| Thing | Where |
|---|---|
| gen-0.4's kinds and planner options (`add`, `delayed`) | `sidechat/guide.py`, `sidechat/gen/planner.py`, `sidechat/gen/writer.py`, `sidechat/pipeline/generate.py` |
| Short input (`text_turns`, oldest turns dropped to fit) | `sidechat/train/features.py` (`fitted`) |
| Two-tower input and model (`sidechat-tt-0.1`) | `features.context_text`, `line_text`; `sidechat/train/model.py` (`TwoTowerModel`) |
| Distillation, `drop_kinds`, `arch` in training | `sidechat/pipeline/train.py` |
| Two-graph export, transformer optimizer, tokenizer saved without truncation | `sidechat/pipeline/export.py` |
| Runtime: `TwoTower` with a history cache and `prepare()`; tokenizer truncation off | `sidechat/runtime.py` |
| Adapter: 1 thread by default, `prepare_history()`, background head start | `sidechat/integrations/pipecat_classifier.py` |
| The chained job, re-runnable by step | `sidechat/pipeline/round6.py` |
| Parity probe (PyTorch batched, line by line, runtime) | `sidechat/pipeline/parity_probe.py` |
| Bench and cloud harness for two-tower models | `scripts/bench_latency.py`, `sidechat/pipeline/latency.py` |
| Tests | `tests/test_round6.py` |

## Things learned

- **A fast tokenizer keeps the truncation of its last call, and `save_pretrained` writes it into
  tokenizer.json.** The runtime cut every two-tower history to the line's 96 tokens until the
  runtime and the export turned truncation off. Anything else that loads an exported
  tokenizer.json (the Pipecat module) should do the same.
- **A gate on overall Duplex-MPE accuracy hides named requests.** They are 2,000 of 52,336 lines.
  Gate on items 4 and 5 as well.
- **Distilled students keep the teacher's quiet and lose its reach.** They match round 3 on lines
  for others and on real meetings, but drop most unnamed requests, where the guide says "even call"
  and round 3 relies on cues the small models do not learn.
- **Named-request handling in the students is seed-dependent**, so one run of a student says little.
- **int8 for the small students is fragile** (2 of 9 builds passed its gate, one hit a quantizer
  error). A 32M in fp32 is fast enough.
- **The transformer optimizer fuses GELU and the skip layer norms in Ettin, not its attention**,
  and was never 5% faster, so it never shipped.
- **Jev's latency is network-bound** and varies threefold between containers.

## Loose ends

- The Pipecat module (phase 7) ports the single-tower runtime only; a two-tower model needs its
  history cache, `prepare` hook and the tokenizer fix there too.
- The demo's gate does not call `prepare_history`; the adapter's background head start covers lines
  that follow each other with no agent turn between them.
- `side-r6ttr3t-ettin-68m-s1` is the most accurate student on named requests and lines that only
  mention the agent (N1 0.07%, item 7 met) but has no int8 build; fp32 is 91 ms on agent-1x.

## Where the next phase picks up

1. ~~Decide how unnamed requests to an agent that has not spoken should be labelled.~~ Decided
   (SD-21): the label stays. The models read those lines as said to a person, not as open, so the
   label does not move item 5. rc0.2 shipped the 32M as `agent-1x/` (SD-22,
   [phase-7-release-rc0.2.md](phase-7-release-rc0.2.md)).
2. **Student round 2**: two-tower 32M in fp32, checkpoint picked on a named-request dev slice,
   labels at full weight on named lines, plus teacher-scored lines like unnamed requests; two
   seeds. Gate on items 4 and 5 as well as Jev's speed on agent-1x.
3. Real calls (SQ-05) remain the fresh test for every model here.
