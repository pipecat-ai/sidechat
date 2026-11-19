---
license: bsd-2-clause
language: en
library_name: onnx
pipeline_tag: text-classification
base_model:
  - jhu-clsp/ettin-encoder-150m
  - jhu-clsp/ettin-encoder-32m
datasets:
  - ACloudCenter/ami-addressee
tags:
  - pipecat
  - onnx
  - addressee-detection
  - multi-party
  - turn-taking
---

# Pipecat Sidechat (experimental, rc0.2)

> **⚠️ Experimental.** Outputs, names and calibration may change between releases.

A small text classifier for a voice agent in a conversation with several people. For each line it gives the
probability that the agent should speak now, and whether the line was for it, for the room or about it. Speaker
labels can be anonymous ("Speaker 1"); the agent's name and the rhythm of the last turns carry the signal.

Code: [github.com/pipecat-ai/sidechat](https://github.com/pipecat-ai/sidechat)

Two builds:

| Build | Folder | For |
|---|---|---|
| Default, 150M (`side-r3-ettin-150m-s0`) | repo root | 1 vCPU or more; the more accurate one |
| `agent-1x`, 32M two-tower (`side-r6ttr3t-ettin-32m-s0`) | `agent-1x/` | 0.5 vCPU, 1 GiB (Pipecat Cloud `agent-1x`) |

The `agent-1x` build encodes the earlier lines while the person is still talking, then reads only the new line
when they stop. It was distilled from the default build.

## Use

```bash
pip install git+https://github.com/pipecat-ai/sidechat
```

```python
from huggingface_hub import snapshot_download
from sidechat.runtime import load
from sidechat.schema import Agent, SidechatRequest, Turn

model = load(snapshot_download("pipecat-ai/sidechat", allow_patterns=["*.json", "model.onnx"]))
a = model.answer(SidechatRequest(
    agent=Agent(name="Atlas"),
    speaker="Speaker 1",
    text="Can you check that for us?",
    history=[Turn(speaker="Atlas", text="Want me to look up flights?", agent=True)],
))
print(a.respond, model.decide(a))  # 0.99 respond
```

For `agent-1x`, load the folder and call `prepare` with the next line's request (its history is what counts)
as soon as the previous line ends; `answer` then encodes only the new line:

```python
path = snapshot_download("pipecat-ai/sidechat", allow_patterns=["agent-1x/*.json", "agent-1x/*.onnx"])
model = load(f"{path}/agent-1x", threads=1)
model.prepare(request)          # while the person talks
a = model.answer(request)       # when they stop
```

| Output | Meaning |
|---|---|
| `respond` | probability the agent should speak now; about 0.5 for a question left open to the room |
| `intent` | for the agent directly or indirectly, open to the room, about the agent, or other |
| `unclear` | the line fits the agent and someone else equally |

`decide` gives `respond`, `wait` (speak only if nobody else does) or `ignore`, at the thresholds in `config.json`.
Pass `int8=True` to `load` for the default build's `model-int8.onnx`, which has thresholds of its own.

## Files

| File | |
|---|---|
| `model.onnx`, `model-int8.onnx` | default build, fp32 598 MB, int8 267 MB |
| `agent-1x/context.onnx`, `agent-1x/line.onnx` | `agent-1x` build, fp32, 128 + 131 MB |
| `tokenizer.json`, `config.json` (each folder) | tokenizer, calibration and thresholds |
| `data/`, `agent-1x/data/` | the rows each build was trained on (train and dev) |
| `MANIFEST.json` (each folder) | sha256 of every file, row counts |

## Results against Jev

Anonymous speakers. Jev is asked as Pipecat's daily-audience demo asks it.

| Set | Default | `agent-1x` | Jev |
|---|---|---|---|
| [Duplex-MPE](https://huggingface.co/datasets/ChengqianMa/Duplex-MPE), 52,336 lines | 96.7% | 95.6% | 83.1% |
| … lines for others, answered outright | 0.22% | 0.26% | 0.41% |
| … lines for others, held for a pause | 0.9% | 0.8% | 16.0% |
| … request naming the agent, answered | 99.5% | 98.7% | 99.2% |
| … same request without the name, answered | 38.8% | 10.7% | 26.6% |
| [Social AI Ambient Bench](https://huggingface.co/datasets/text-ai/social-ai-ambient-bench), 15,793 lines | 98.7% | 98.4% | 85.4% |
| [AMI](https://huggingface.co/datasets/ACloudCenter/ami-addressee) labelled meetings, 8,875 lines | 99.9% | 100.0% | 85.2% |
| 270 hand-written lines | 87.4% | 87.4% | 77.8% |

These are baselines, not proper benchmarks: labels follow the project's own guide, and the choice between
training rounds looked at these sets.

## Speed

Median ms per line with 8 earlier lines, one thread, on containers capped like Pipecat Cloud's profiles. Jev is
an API call from the same container, so its time is mostly the network.

| | 0.5 vCPU, 1 GiB | 1 vCPU, 2 GiB | Memory |
|---|---|---|---|
| `agent-1x`, earlier lines encoded ahead | 10 to 15 | 9 | 488 MB |
| `agent-1x`, earlier lines not ready | 88 to 117 | 35 | |
| Default, int8 / fp32 | 532 / does not fit | 253 (fp32) | 571 MB (int8) |
| Jev | 56 to 163 | 58 to 149 | |

On an M5 Max the default build takes 10 ms with a short history and 52 ms with 8 earlier lines.

## Limitations

- A request without the agent's name, before the agent has spoken, is answered less than half the time by the
  default build and about one time in ten by `agent-1x`, which mostly ignores it (Jev mostly holds for a pause).
- English text only. Most training lines are generated; only AMI is real speech.

## Training

Both use [Ettin](https://huggingface.co/jhu-clsp/ettin-encoder-150m) encoders (MIT) with intent, respond and
unclear heads. The default build: Ettin-150M, 2 epochs on 235,069 lines. `agent-1x`: Ettin-32M as one shared
encoder for the earlier lines and the new line, joined by a cross-attention layer, 3 epochs on 420,828 lines,
with the default build's probabilities as 80% of each target. The lines come from generated multi-party
conversations, labelled by kind under the project's guide, and from AMI meetings
([ACloudCenter/ami-addressee](https://huggingface.co/datasets/ACloudCenter/ami-addressee), CC BY 4.0) outside
every test meeting, all lines for people. Speakers were anonymous in 60% of training lines, named in 25% and
unlabelled in 15%. Duplex-MPE and the Social AI Ambient Bench were used for evaluation only.
