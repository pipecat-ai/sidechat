# Phase 7 notes, part 3: release rc0.3

2026-11-20. After round 9's report, Jon said "Ship rc0.3". Read this, then [TODO.md](../TODO.md).

## What was done

- **rc0.3 on `pipecat-ai/sidechat`** (SD-26, exp-061):
  - **Repo root:** round 9's 150M, `side-r9-ettin-150m-s1`. fp32 only: its int8 build failed parity
    (178/283 decisions the same), so round 3's `model-int8.onnx` was removed in the same commit.
  - **`agent-1x/`:** round 9's two-tower 32M, `side-r9tt-ettin-32m-s1`, fp32.
  - **Rows:** each folder carries the rows its build was trained on, now including `realreq-0.2`
    (SLURP's text CC BY 4.0 and CLINC150's CC BY 3.0, attributed on the card).
  - **Commits:** root `05704f4` (with `model-int8.onnx` removed), `agent-1x/` `f585138`, then
    `dafacac` to correct the card's example output (0.97, not rc0.2's 0.99). Tag `rc0.3` points
    to `dafacac`; it was moved there from `f585138` minutes after it was made.
  - **Tags:** rc0.2 still points to `08c9b8c`. Pipecat's download pinned at `c9b59be` is
    unaffected.
  - **Checked from the Hub at `rc0.3`:** every graph, tokenizer and config matches its MANIFEST
    sha256. The root loads as the single-tower model and answers the card's example 0.97 respond;
    `agent-1x` loads as `TwoTower` and answers 0.98. There is no int8 file.
  - **Rows:** 240,069 train and 26,631 dev at the root; 425,828 and 44,624 in `agent-1x/`. The
    train counts match the runs' own.
- **Checks before publishing:**
  - The 150M's export: the same decision as PyTorch on 283/283 parity lines.
  - The 32M's export: its export report had been overwritten by seed 0's (both used one name), so it
    was checked locally against the stored PyTorch predictions. The same decision on 1,500/1,500
    sampled AMI lines; the largest `respond` difference was 0.006 (GPU against CPU).
- **The card (`hf/README.md`) and README:**
  - rc0.3's results against Jev, including real recorded requests and AMI as heard.
  - The keyterm advice.
  - Speed: round 9's latency run for `agent-1x`; rc0.2's times for the default build, which has the
    same size and graph.
  - A plain limitation on holds of people's talk.
- **Fixes along the way:**
  - `publish.py` removes graphs an earlier build left in the folder (exact names only, never another
    folder's).
  - Round jobs name exports and latency variants with the seed, so two students' reports no longer
    overwrite each other.
- The repo is committed and pushed with tag `rc0.3`.

## Loose ends

- Pipecat's port runs single-tower models only, and pins rc0.2's predecessor `c9b59be`. Moving it to
  rc0.3's default build is a one-line revision change there. `agent-1x/` still needs the two-tower
  port.
- No int8 for the default build: round 9's failed parity badly (178/283), and round 8's did too.
  The int8 path may need another look before it is offered again.
