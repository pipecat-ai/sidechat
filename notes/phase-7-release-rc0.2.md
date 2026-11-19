# Phase 7 notes, part 2: release rc0.2

2026-11-19. Jon left the label for unnamed requests to the agent's recommendation, then asked to
"push and ship this on hugging face, we can call this RC0.2". Both are done. Read this, then
[TODO.md](../TODO.md).

## What was done

- **The label for unnamed requests stays as guide 0.4 has it** (SD-21). Before relabelling, the
  stored predictions on Duplex-MPE's implicit requests were read by tag (no text). Every model
  reads those lines as said to a person (`other`) or to the agent (`direct`), almost never as open:

  | Model | Answered now | Held | Missed | Median open intent | Intent `other` |
  |---|---|---|---|---|---|
  | Round 3, 150M | 38.8% | 13.2% | 48.0% | 0.01 | 52% |
  | Two-tower 68M, seed 0 | 19.5% | 7.2% | 73.3% | 0.01 | 76% |
  | Two-tower 32M, seed 0 | 10.7% | 7.5% | 81.8% | 0.01 | 84% |

  Lowering the open-intent threshold from 0.7 to 0.3 adds under 2 points of holds for the 32M. So
  neither "held" nor "even call" changes what a model does on these lines. Item 5 also swings with
  the seed and round: 150M models from 22.8% to 47.2%, and round 1's labels-only 68M at 61%.
- **rc0.2 on `pipecat-ai/sidechat`** (SD-22, exp-054): commit `08c9b8c`, tag `rc0.2`.
  - The root files (round 3's 150M) are byte-identical to `c9b59be`, which Pipecat pins.
  - `agent-1x/` holds the two-tower 32M student (`side-r6ttr3t-ettin-32m-s0`, fp32): context.onnx,
    line.onnx, tokenizer (no truncation), config, MANIFEST.json, and its 420,828 training rows.
  - The card describes both builds, with results and speed against Jev.
  - Checked: the folder downloaded at `rc0.2` loads as `TwoTower` and gives the card's example
    0.99 respond.
- `sidechat/pipeline/publish.py` takes `--subdir` and `--tag`, copies the graphs the export's arch
  names, and refuses a two-tower tokenizer that carries truncation.
- README: both builds, results against Jev, speed on agent-1x and agent-2x.
- The repo is committed and pushed with tag `rc0.2`. The same commit carries other sessions'
  finished work: the dataset job (exp-040), the phase 7 part 1 note, and the parity script.

## Why ship the 32M now

It passes the gate as Jon set it: faster than Jev on agent-1x with a full history (10 to 15 ms,
Jev 56 to 163), and within about a point of round 3 on Duplex-MPE (95.6% against 96.7%), AMI (100%
against 99.9%) and the pilot (87.4% both). It misses the stricter rule added after round 6: unnamed
requests at 10.7%, against Jev's 26.6% and round 3's 38.8%. So it is opt-in, in its own folder,
with the gap stated on the card, and round 3 stays the default.

## Loose ends

- Pipecat's port (`pipecat.models.labs.side_chat`) runs single-tower models only. `agent-1x/` there
  needs a two-tower port, the `prepare` hook, and the tokenizer fix.
- The HF dataset `pipecat-ai/sidechat-gen` stays private (licence to confirm).

## Where the next phase picks up

1. **Student round 2, aimed at item 5.**
   - Generate lines whose addressee only the context settles (`only_agent_can_do`,
     `addressed_by_exclusion`, `question_only_agent_can_answer`, `unclear_you`) in conversations
     where the agent has not spoken.
   - Score them with the teacher.
   - Pick the checkpoint on a named-request dev slice, and run two seeds.
   - Gate on items 4 and 5 as well as speed.
2. A two-tower port in Pipecat if `agent-1x` is to run there.
3. Real calls (SQ-05).
