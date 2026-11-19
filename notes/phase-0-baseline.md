# Phase 0 notes: setup and baseline

Closed 2026-11-18. Next: Phase 1, the labelling guide and the scorecard.

These notes are for whoever picks the project up next, person or model, with no memory of the
session that did the work. Read this, then [TODO.md](../TODO.md) and
[DECISIONS.md](../DECISIONS.md).

## The project in one paragraph

Sidechat is a small text classifier for a voice agent that shares a conversation with several
people. For each utterance it gives probabilities for who the line was for and whether the agent
should speak. It reuses the architecture and recipe of Pipecat Audience, a sibling model for the
reverse case (one person, several agents). The bar is Jev, TypeSafe's hosted classifier, as the
`~/Sites/daily-audience` demo uses it. The full plan is [PLAN.md](../PLAN.md). The survey of open
datasets is [DATASETS.md](../DATASETS.md).

## What Phase 0 did

| Item | Where |
|---|---|
| `uv` project, 11 tests, ruff clean | `pyproject.toml`, `tests/test_phase0.py` |
| Audience's reusable code, copied unmodified | `vendor/audience/`, provenance in its `PROVENANCE.md` |
| Request, answer and labelled-record schema `sidechat-0.1` | `sidechat/schema.py`, `contracts/sidechat-0.1.schema.json` |
| Statistics: Wilson intervals, paired difference, bootstrap, ECE, AUROC | `sidechat/lib/score.py` |
| R2 helper | `sidechat/lib/r2.py` |
| Jev with the demo's exact wording, state and thresholds | `sidechat/baselines/jev_demo.py` |
| A name-only rule (the demo's fallback when Jev is down) | `sidechat/baselines/name_only.py` |
| Converters for Duplex-MPE, Ambient Bench and hand-written suites | `sidechat/sources/` |
| The demo's own 52 lines as a suite | `data/suites/demo-lines-0.1.yaml` |
| A 283-line hand-written pilot, 29 conversations | `data/suites/pilot-0.1.yaml` |
| The baseline job: detached, resumable, writes everything to R2 | `sidechat/pipeline/baseline.py` |
| The step that fetches a job's results from R2 | `sidechat/pipeline/results.py` |
| The baseline, measured | [reports/2026-11-18-side-jev-baseline.md](../reports/2026-11-18-side-jev-baseline.md) |
| Experiment records, decisions, budget, status | `experiments/`, `DECISIONS.md`, `BUDGET.md`, `TODO.md` |

## The result

57,434 distinct requests to `jev-1.13.0`, all answered, none failed, 16 minutes, about $2.08.

- **Named requests:** Jev answers 99.2% at once (1,983 of 2,000 on Duplex-MPE).
- **The same requests without the name:** 26.6% at once, 73.2% held for silence. A drop of 72.6
  points (70.6 to 74.6).
- **Lines meant for someone else:** held on 15 to 16% across three unrelated sets, answered at
  once 0.4% (mostly lines to another device, like "Hey Google, …").
- **Name said about the agent, not to it:** 0 of 6,080 answered at once.
- **Scores:** AUROC 0.988, calibration error 0.073 (the plan asks for 0.05).

The bar is tight wherever the name is said and wide open wherever it is not. Sidechat has to keep
Jev's precision on names and add reading from the conversation who a line was for.

## How things run

Every job runs detached on Modal and writes to R2, so nothing depends on this machine (SD-02, a
standing rule from Jon). Load `.env` first in every shell:

```bash
set -a; . ./.env; set +a
```

Start a job, then fetch its status or results from any machine with the `.env`:

```bash
uv run modal run --detach -m sidechat.pipeline.baseline::run --exp exp-001-side-jev-baseline --sets demo,pilot,ambient,duplex
```

```bash
uv run python -m sidechat.pipeline.results exp-001-side-jev-baseline
```

Infrastructure facts:

- **Modal:** workspace `jptaylor`, environment `waystone`. Apps are named `waystone-side-<stage>`.
  A job refuses to start unless `MODAL_ENVIRONMENT=waystone`. Secrets are built from `.env` at
  launch with `modal.Secret.from_dict`; nothing is stored on Modal. Use the project's own Modal,
  `uv run modal`; there is no global `modal` on this machine.
- **R2:** the bucket Audience uses. Sidechat writes only under `runs/side/` and `models/side/`.

| R2 path | Holds |
|---|---|
| `runs/side/rows/<rows_id>/` | `rows.jsonl` and `manifest.json` for each set |
| `runs/side/baselines/jev-demo-0.1/` | Jev's stored answers (`parts/`), per-set scores, manifest |
| `runs/side/results/<exp>/` | `status.json` (rewritten as the job runs), `scorecard.json`, `report.md` |

- **Pattern for a new job:** a module in `sidechat/pipeline/` with one `@app.function` called
  `run` that does the whole chain remotely and rewrites `runs/side/results/<exp>/status.json` as
  it goes. Stored work is reused, so a stopped or retried job resumes. `baseline.py` is the model
  to copy.
- **Bookkeeping per paid run:** an `experiments/<exp>/record.yaml` with a forecast before launch,
  a ledger line in `BUDGET.md` after, a report in `reports/` for anything measured. Experiments
  are numbered `exp-NNN-side-<slug>`; the next is `exp-002`.
- **Decision ids:** `SD-NN` for decisions, `SQ-NN` for open questions, both in `DECISIONS.md`.

## Things learned the hard way

- **Jev throughput:** 12 requests at a time gave about 58 a second with no 429s. About 842 input
  tokens per request with 8 turns of history.
- **Duplex-MPE has 28 rows whose event type and addressee disagree.** They are left out of scoring
  (`tags.conflict == "1"`), not relabelled.
- **Ambient Bench must never be trained on.** Its card carries a canary notice. Its policy also
  expects the assistant to volunteer help, so its RESPOND lines are not a fair target for a model
  that speaks when spoken to. The useful number from it is how often a model stays quiet.
- **Neither benchmark may be committed to git as converted rows.** They live in R2 with a
  manifest marked test-only (SD-06).
- **The demo rewrites every alias of the bot's name before asking Jev**, so "at last a number
  that makes sense" goes to Jev as "Atlas a number that makes sense" and scores 0.94. A bug in
  `daily-audience`, recorded in TODO.md.
- **Modal prints "Timed out waiting for final app logs"** at the end of a detached run. Harmless:
  check `status.json` instead.
- **Hugging Face's full-text search rate-limits fast** (429 after about 20 queries).
- **The clone of `spellspeak/model-training` used in Phase 0 was in a temporary scratch folder**
  and will disappear. `vendor/audience/` holds everything Sidechat needs from it. For anything
  else, clone it again: `gh repo clone spellspeak/model-training`.

## Loose ends

| Item | State |
|---|---|
| Git | Repo initialised, 86 files staged, **nothing committed yet** |
| Opt-in call log in `daily-audience` | Held for Jon (SD-08, SQ-05) |
| Open questions SQ-01 to SQ-08 | Defaults assumed, none confirmed by Jon. See `DECISIONS.md` |
| Trial run's objects in R2 | `runs/side/results/exp-000-side-trial/`, `runs/side/baselines/trial-0/`. Small, safe to delete |
| Jev's price | $0.042 per million input tokens, from Audience's repo, not confirmed with TypeSafe |
| Dataset licences | Hub tags only. Check each source's own licence before training on it |
| `audience-data/` | Audience's training data copied from R2 (418 MB, gitignored). Reference only |

## Phase 1: where to pick up

Goal: a labelling guide with its rules as code, a committee that agrees with it, and a frozen
scorecard. PLAN.md section 6 and section 9 have the detail.

1. **Write labelling guide 0.1** in `contracts/`, with its rules of evidence as code in
   `sidechat/`. Model it on Audience's guide (`vendor/audience/contracts/taxonomy/addressee-guide-0.3.md`)
   and rules (`vendor/audience/harness/addressee/evidence.py`). The cases it has to settle:
   - the 46 pilot lines where Jev and the draft labels disagree, and the 30 graded lines (both
     listed in `experiments/exp-001-side-jev-baseline/report.md`);
   - indirect requests: Duplex-MPE marks "Get Aria to text Mum" as silence, while the plan's
     `indirect` intent would have the agent consider it;
   - sessions the agent leads (support, tutoring, a game master), where answers to its questions
     carry no name;
   - thanks, "that's enough" and goodbyes said to the agent: whether it should reply.
2. **Choose the committee.** Three large models from three families, majority vote, Jev not on it
   (PLAN.md section 6). Keys in `.env` today: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`,
   `GOOGLE_API_KEY`. No labeller model ids are set yet. Audience's committee code is in
   `vendor/audience/audience/lib/committee.py`, `labellers.py` and `audience/pipeline/label.py`.
3. **Pilot the committee on the 283 pilot lines** as a detached job (`exp-002`). Target: at least
   90% agreement with the guide. Revise the guide where it fails and relabel the pilot.
4. **Freeze the scorecard** in PLAN.md section 3.3 with Jev's numbers filled in from the baseline.
5. **Write `notes/phase-1-guide.md`** when the phase closes.

Questions worth putting to Jon before or during Phase 1: SQ-02 (output shape), SQ-03 (training on
Jev's answers), and the indirect-request policy.
