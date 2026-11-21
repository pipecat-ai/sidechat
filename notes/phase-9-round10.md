# Phase 9 notes: round 10, int8 again, and rc0.3.1

2026-11-20, overnight. After TCL's test, Jon asked to "run all we can so things can run
overnight and we arrive at the best possible model". This phase aimed generated data at rc0.3's
weak spot on TCL and fixed the int8 build. Read this, then [TODO.md](../TODO.md). Full results:
[reports/2026-11-20-side-round10.md](../reports/2026-11-20-side-round10.md).

## What was done

- **gen-0.5** (exp-064, about $23): 5,997 conversations and 83,933 lines.
  - Three new kinds for the line after the agent answers (SD-28):
    - `people_question_after_agent`: someone asks the others about their own plans;
    - `partner_to_people_after_agent`: the person the agent answered turns to the others;
    - `follow_up_later`: that person comes back to the agent's answer later, without its name.
  - They sit outside the default mix (`planner.ADDED`), so earlier plans replay unchanged.
  - The test split is written by writer b, held out of training.
- **The committee check** (exp-065, $11.35). Agreement with the labels, by kind:
  - `people_question_after_agent`: 93.3% (112/120). Kept.
  - `partner_to_people_after_agent`: 87.5%. Left out: the differences come where the agent leads
    or has just offered something.
  - `follow_up_later`: 39.2%. Left out: the majority answers these where our label holds them.
    This is open question SQ-09 for Jon.
- **Round 10** (exp-066, about $23):
  - Round 9's recipe plus gen-0.5 without the two failed kinds.
  - Two 150M teachers and two 32M two-tower students, judged against rc0.3 by a gate fixed
    beforehand (`student_gate.gate_r10`). TCL is read only for the gate and the report, never for
    picks.
- **Two more students** (exp-071, about $16) under a rule fixed beforehand: the dev pick across all
  four seeds must pass the same gate.
- **int8 for both of rc0.3's builds** (exp-067 to exp-070, exp-072, exp-073, about $2.65):
  - found the cause and fixed the recipe in `export.py`;
  - built int8 files for the default build and the two-tower agent-1x build;
  - checked both on every test set.

## Results

- **The teacher learned the new kind but not TCL's distinction.**
  - Questions to the others right after the agent are left alone 97.0%, against rc0.3's 66.6%.
  - TCL's outright answers on people's lines: 1.67% against 1.94%, paired -0.27 points (-0.62 to
    +0.08), not beyond noise.
  - TCL's ranking right after Sigma, when the other person speaks, is unchanged (AUROC 0.66
    against 0.67).
  - It answers fewer unnamed requests: Duplex-MPE 20.8% against 29.3% (below Jev's 26.6%, so
    scorecard item 5 would be lost), and TCL's follow-ups 29.1% against 36.2%.
  - No ship.
- **The students cut TCL's outright answers beyond noise but lose named requests.**
  - Seeds 0 and 1: 51 and 49 of 3,348, against rc0.3 agent-1x's 75.
  - Duplex-MPE's named requests answered: 95.3% and 97.6%, against 99.7% (margin 1 point).
  - Seeds 2 and 3 (exp-071): every seed cuts TCL's outright answers beyond noise (-0.72 to -0.84
    points). Dev picks s2, which fails one margin by one line: Ambient Bench, 79 lines fewer right
    where 78.97 are allowed. By the rule, nothing ships.
  - s2's trade, if Jon wants to weigh it:
    - Gains: TCL's outright answers fall by a third, and Duplex-MPE's from 0.33% to 0.18%.
    - Costs: half Duplex-MPE's unnamed requests answered (4.9% against 10.2%), 57 of 61 written
      SLURP named requests, 47 of 48 demo lines.
- **int8 works again.**
  - The cause: int8 products overflowing on CPUs without VNNI. The fix: reduced range, with each
    layer's MLP output kept in fp32.
  - rc0.3's 150M in int8: 281/283 parity decisions, 1.6× faster on one thread (191 ms against
    298), 325 MB against 598.
  - On every test set it is within a point of fp32, with 98.5% to 99.9% of decisions the same.
    It holds slightly less on both sides: its hold threshold is 0.45 against 0.4.
  - Files: `models/side/side-r9-ettin-150m-s1/export-int8/` (`model-int8.onnx`, and `config.json`
    with `thresholds_int8`). R2 only.
  - The recipe passes on all five builds it was tried on. Besides rc0.3's 150M, these are round
    10's teacher (280/283) and students s2 and s3 (282 and 277 of 283), and rc0.3's agent-1x build
    (exp-072).
  - rc0.3's agent-1x in int8: 279/283 parity, dev 98.55% against 98.55%. Both towers cold on one
    thread take 14.2 ms against 25.1; 195 MB.
  - Files: `models/side/side-r9tt-ettin-32m-s1/export-int8/` (`context-int8.onnx`, `line-int8.onnx`,
    `config.json`). R2 only.
  - On the test sets (exp-073), it is closer still to fp32. Decisions are 98.6% to 99.9% the same.
    No set answers people outright more beyond noise. Named requests are unchanged, and there are
    slightly fewer holds.

## Release rc0.3.1 (SD-29, exp-074, exp-075)

Jon: "Yes, publish rc0.3.1".

- **What changed on `pipecat-ai/sidechat`:**
  - The root gains `model-int8.onnx` (commit `0a0cbce`).
  - `agent-1x/` gains `context-int8.onnx` and `line-int8.onnx` (commit `dfa2379`, tagged
    `rc0.3.1`).
  - Each `config.json` gains `thresholds_int8` and `int8_recipe`; everything else is rc0.3's. The
    fp32 graphs and tokenizer have rc0.3's sha256.
  - `rc0.3` (`dafacac`) and `rc0.2` (`08c9b8c`) are untouched. Pipecat's pin `c9b59be` is unaffected.
- **The card and README** gain int8: how to load it, the files, and the training recipe. The speed
  table is now one run (exp-074) with fp32 and int8 side by side.
- **Speed** (one thread, 8 earlier lines, capped containers; this host is slower than rc0.2's run):

| | 0.5 vCPU, 1 GiB | 1 vCPU, 2 GiB | Memory |
|---|---|---|---|
| `agent-1x`, history encoded ahead: fp32 → int8 | 11 → 10 ms | 16 → 7 ms | 487 → 428 MB |
| `agent-1x`, history not ready: fp32 → int8 | 104 → 95 ms | 77 → 32 ms | |
| Default: fp32 → int8 | 991 → 672 ms | 465 → 303 ms | about 0.9 GB → 628 MB |

  At 0.5 vCPU, `agent-1x`'s int8 gains little time but uses 60 MB less memory. The default fp32 build
  took 3 minutes to load at 0.5 vCPU, near the memory limit; int8 loads in 3 seconds.
- **Checked from the Hub at `rc0.3.1`:**
  - Every graph, tokenizer and config matches its MANIFEST.
  - The card's example gives 0.968 respond (fp32) and 0.967 (int8) at the root, and 0.976 and
    0.973 in `agent-1x`.
- **In R2:** each run's `export/` now holds the int8 files. rc0.3's `config.json` is kept at
  `models/side/<run>/export-rc0.3/config.json`.

## How things run

```bash
set -a; . ./.env; set +a
```

```bash
uv run modal run --detach -m sidechat.pipeline.round10::run --exp <exp> --drop-kinds follow_up_later,partner_to_people_after_agent
```

```bash
uv run modal run --detach -m sidechat.pipeline.round10::run --exp <exp> --steps students,export,latency --teacher side-r10-ettin-150m-s1 --student-seeds 2,3 --pick-among side-r10tt-ettin-32m-s0,side-r10tt-ettin-32m-s1
```

```bash
uv run modal run --detach -m sidechat.pipeline.int8_probe::run --exp <exp> --run-id side-r9tt-ettin-32m-s1 --make
```

```bash
uv run modal run --detach -m sidechat.pipeline.int8_probe::run --exp <exp> --run-id side-r9tt-ettin-32m-s1 --check --check-sets duplex
```

- **`round10.py`** is round 8's job with gen-0.5, TCL scored on every model, and `gate_r10`.
  `--steps` picks parts, `--student-seeds` and `--pick-among` add seeds to an earlier round, and
  `--drop-kinds` leaves kinds out of training.
- **`int8_probe.py`** has three modes, each a detached 8-CPU job:
  - `--make` builds and gates an int8 file into `export-int8/`, beside a released export. A
    two-tower model gets `context-int8.onnx` and `line-int8.onnx`. `--run-id` defaults to rc0.3's
    150M.
  - `--check` scores it on the test sets against fp32's stored predictions. Duplex-MPE alone takes
    about 90 minutes for the 150M and 30 for the 32M, so give it a container of its own with
    `--check-sets`.
  - `--combos` reruns the recipe search (one-graph models only).
- **`build.build_rows("tcl@anonymous")`** reads TCL's text from R2. It never enters git.

## Things learned

- **Generated kinds teach what they show, not more.** The new kind's lines were learned in
  distribution (97%). TCL's lines right after the agent stayed as hard as before. What separates a
  nameless follow-up to the agent from a reply to the partner is barely in the text.
- **Students moved TCL where the teacher did not,** partly by being stricter. All four answer
  fewer of Duplex-MPE's unnamed requests (4.9% to 8.8%, against 10.2%), and two lose named ones.
  Their dev thresholds are stricter too (respond 0.65 against 0.55).
- **The int8 failure was a CPU feature, not the model.** Full-range per-channel int8 overflows
  without VNNI. Round 3's int8 passed under the old recipe and rounds 8 and 9 did not, so a pass
  depended on the weights. The recipe now in `export.py` is the default for every later export.
- **Picks and gates were fixed before results** (exp-066's gate, exp-071's rule), so nothing was
  chosen on TCL. The rule held even when the dev pick missed by one line.

## Loose ends

- **SQ-09** (Jon): does a person coming back to the agent's answer later, without its name, get an
  answer or a hold? Until settled, `follow_up_later` stays out of training.
- **`partner_to_people_after_agent`** needs the planner to exclude sessions where the agent leads
  or has just offered something, then a committee check, before use.
- **Pipecat** still downloads the pinned `c9b59be`. Moving it to rc0.3.1 and offering int8 there is
  a change in the pipecat branch. `agent-1x/` still needs the two-tower port there.
- **A later int8 build** goes the way rc0.3.1's did. `int8_probe --make` writes it beside the
  export. Copy its files and `config.json` into `export/`, then publish.
- **TCL's AUROC after the agent** is the measure to watch for timing input.
- **Nothing is committed** since `1c0f862`.

## Where the next phase picks up

- **rc0.3.1 is the release:** rc0.3's models, with int8 as an opt-in for both builds.
- **Timing input** is the next real step for the line after the agent answers:
  - when the line starts relative to the agent's end;
  - overlap with the agent.

  It needs a source with timings (AMI has word times; our generated corpora have none) and a
  change to the request schema and the Pipecat adapter. It is Jon's design call.
- **Stop generated kinds aimed at TCL's errors.** More would be tuning on a test set.
