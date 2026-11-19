---
license: bsd-2-clause
language: en
library_name: onnx
pipeline_tag: text-classification
base_model: jhu-clsp/ettin-encoder-150m
datasets:
  - ACloudCenter/ami-addressee
tags:
  - pipecat
  - onnx
  - addressee-detection
  - multi-party
  - turn-taking
---

# Pipecat Sidechat (experimental)

> **⚠️ Experimental.** The first trained release, `side-r3-ettin-150m-s0`. Outputs, names and calibration may
> change between releases.

A small text classifier for a voice agent in a conversation with several people. For each line it gives the
probability that the agent should speak now, and whether the line was for it, for the room or about it. Speaker
labels can be anonymous ("Speaker 1"); the agent's name and the rhythm of the last turns carry the signal.

Code: [github.com/pipecat-ai/sidechat](https://github.com/pipecat-ai/sidechat)

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

| Output | Meaning |
|---|---|
| `respond` | probability the agent should speak now; about 0.5 for a question left open to the room |
| `intent` | for the agent directly or indirectly, open to the room, about the agent, or other |
| `unclear` | the line fits the agent and someone else equally |

`decide` gives `respond`, `wait` (speak only if nobody else does) or `ignore`, at the thresholds in `config.json`.
Pass `int8=True` to `load` for `model-int8.onnx`, which has thresholds of its own.

## Files

| File | |
|---|---|
| `model.onnx` | fp32, 598 MB |
| `model-int8.onnx` | int8, 267 MB |
| `tokenizer.json`, `config.json` | tokenizer, calibration and thresholds |
| `data/train.jsonl.gz`, `data/dev.jsonl.gz` | the rows it was trained on |
| `MANIFEST.json` | sha256 of every file, row counts |

## Results against Jev

Anonymous speakers. Jev is asked as Pipecat's daily-audience demo asks it.

| Set | Sidechat | Jev |
|---|---|---|
| [Duplex-MPE](https://huggingface.co/datasets/ChengqianMa/Duplex-MPE), 52,336 lines | 96.7% | 83.1% |
| … lines for others, answered outright | 0.2% | 0.4% |
| … request to the agent without its name, answered | 38.8% | 26.6% |
| [Social AI Ambient Bench](https://huggingface.co/datasets/text-ai/social-ai-ambient-bench), 15,793 lines | 98.7% | 85.4% |
| [AMI](https://huggingface.co/datasets/ACloudCenter/ami-addressee) labelled meetings, 8,875 lines | 99.9% | 85.2% |
| 270 hand-written lines | 87.4% | 77.8% |

These are baselines, not proper benchmarks: labels follow the project's own guide, and the choice between
training rounds looked at these sets.

## Speed

Median per line, short history / 8 earlier lines, one thread: 10 / 52 ms on an M5 Max, 66 / 253 ms on 1 vCPU,
507 / 648 ms on 0.5 vCPU (int8: 103 / 532 ms). On a small cloud CPU it is slower than an API call to Jev.

## Limitations

- A request without the agent's name, before the agent has spoken, is answered less than half the time.
- English text only. Most training lines are generated; only AMI is real speech.

## Training

The [Ettin-150M encoder](https://huggingface.co/jhu-clsp/ettin-encoder-150m) (MIT) with intent, respond and
unclear heads, 2 epochs. 235,069 training lines: 219,793 from generated multi-party conversations, labelled by
kind under the project's guide, and 15,276 lines for people from AMI meetings
([ACloudCenter/ami-addressee](https://huggingface.co/datasets/ACloudCenter/ami-addressee), CC BY 4.0) outside
every test meeting. Speakers were anonymous in 60% of training lines, named in 25% and unlabelled in 15%.
Duplex-MPE and the Social AI Ambient Bench were used for evaluation only.
