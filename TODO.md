# Where things stand

Updated 2026-11-19, 03:40 UTC, at the end of the overnight run. Jon asked for autonomous work through the phases within $1,000
(SD-17), to have a model to test in the morning. Read the latest note in [notes/](notes/) first,
then this, then [DECISIONS.md](DECISIONS.md). How to try a model: [TESTING.md](TESTING.md).

## Done

| Phase | What | Note |
|---|---|---|
| 0 | Repo, schema, converters, the Jev baseline on 4 sets (exp-001) | [phase-0-baseline.md](notes/phase-0-baseline.md) |
| 1 | Labelling guide 0.2 with rules as code, the committee (99.2% on pilot-0.4), turn-rhythm context, scorecard 0.1 | [phase-1-guide.md](notes/phase-1-guide.md) |
| 2 | Guide 0.3 (anonymous speakers), the conversation generator, gen-pilot (8,426 lines), committee check of generated labels (95.3%), AMI test set, gen-0.1 | [phase-2-corpus.md](notes/phase-2-corpus.md) |
| 4 | Five training rounds. The pick, `side-r3-ettin-150m-s0`, meets 12 of 16 scorecard items: 99.0% right on the main test (Jev 80.7%), answers 0.2% of Duplex-MPE's lines for others outright (Jev 0.4%), none on the AMI silence test (Jev 5 of 10,434), 47/48 demo lines. Exported, in `models/`, runs in the demo's gate at 11 ms a line | [phase-4-models.md](notes/phase-4-models.md) |

## Next

- **Try it:** [TESTING.md](TESTING.md). The model is `side-r3-ettin-150m-s0`, already in `models/`.
  Its scorecard: [reports/2026-11-19-side-r3-ettin-150m-s0-scorecard.md](reports/2026-11-19-side-r3-ettin-150m-s0-scorecard.md).
- Nothing is running on Modal.
- Then: the steps in [phase-4-models.md](notes/phase-4-models.md), "Where the next phase picks
  up": real calls (SQ-05), unnamed requests to an agent with no turns in the history, items 6, 7
  and 9.

## The bar

Jev answers 99.2% of named requests at once but only 26.6% of the same requests unnamed; on the
pilot it answers at once 47.1% of lines for the agent that carry no name. It holds for a pause on
15 to 18% of lines meant for someone else (14.8% on real AMI meetings). Full detail:
[contracts/scorecard-0.1.md](contracts/scorecard-0.1.md).

## Held for Jon

- Commit: "we'll commit later". Everything is staged, nothing committed.
- The opt-in call log in `daily-audience` (SD-08, SQ-05). Nothing in `daily-audience` has been
  edited; TESTING.md shows the one-line swap to try Sidechat there.
- Open questions SQ-01 and SQ-03 to SQ-07 in DECISIONS.md, each with a default assumed.
- SD-18 (guide 0.4: a named thanks, stop or goodbye is answered briefly), SD-19 (AMI's unlabelled
  meetings in training) and SD-20 (a real-speech bar on thresholds) are agent defaults to confirm.

## Open debts

- The demo rewrites every alias of the bot's name before asking Jev, so "at last a number that
  makes sense" is sent as "Atlas a number that makes sense". A bug in `daily-audience`.
- Jev's price per token is from Audience's repo, not confirmed.
- Dataset licences in DATASETS.md are Hub tags; check each source's own licence before training.
- Eight turns of history can miss state the agent holds (exp-004's timer line).
- int8 holds up for 150M only (exp-027), not 68M (exp-023). Latency on this Mac is 7 to 52 ms a
  line depending on history and threads, against Jev's 165 ms (exp-032). On cloud CPUs it is
  slower than Jev: about 250 ms with a full window on 1 vCPU and 530 ms (int8) on `agent-1x`, where
  fp32 does not fit (exp-033). Next for speed: a smaller encoder, fewer context tokens, and a
  default of 1 thread in the Pipecat adapter.
- Trial objects in R2 are safe to delete: `runs/side/results/exp-000-side-trial/`,
  `exp-002-side-committee-trial/`, `exp-009-side-gen-trial/`, `exp-013-side-train-smoke/`,
  `exp-014-side-export-smoke/`, `runs/side/baselines/trial-0/`, `runs/side/labels/trial-committee-0/`,
  `runs/side/corpus/gen-trial/`, `models/side/side-smoke-ettin-32m-s0/`.
