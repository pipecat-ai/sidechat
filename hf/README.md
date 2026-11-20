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

# Pipecat Sidechat (experimental, rc0.3)

> **⚠️ Experimental.** Outputs, names and calibration may change between releases.

A small text classifier for a voice agent in a conversation with several people. For each line it gives the
probability that the agent should speak now, and whether the line was for it, for the room or about it. Speaker
labels can be anonymous ("Speaker 1"); the agent's name and the rhythm of the last turns carry the signal.

Code: [github.com/pipecat-ai/sidechat](https://github.com/pipecat-ai/sidechat)

Two builds:

| Build | Folder | For |
|---|---|---|
| Default, 150M (`side-r9-ettin-150m-s1`) | repo root | 1 vCPU or more; the more accurate one |
| `agent-1x`, 32M two-tower (`side-r9tt-ettin-32m-s1`) | `agent-1x/` | 0.5 vCPU, 1 GiB (Pipecat Cloud `agent-1x`) |

The `agent-1x` build encodes the earlier lines while the person is still talking, then reads only the new line
when they stop. It was distilled from the default build.

**New in rc0.3:** both builds were also trained on real people's requests to assistants, said in real meetings.
A request without the agent's name ("set a timer for ten minutes"), said before the agent has spoken, is now held
for a pause about nine times in ten. In rc0.2 it was mostly ignored. The cost is more holds on people's own talk;
see Limitations. rc0.2 stays at tag `rc0.2`.

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
print(a.respond, model.decide(a))  # 0.97 respond
```

For `agent-1x`, load the folder and call `prepare` with the next line's request (its history is what counts)
as soon as the previous line ends; `answer` then encodes only the new line:

```python
path = snapshot_download("pipecat-ai/sidechat", allow_patterns=["agent-1x/*.json", "agent-1x/*.onnx"])
model = load(f"{path}/agent-1x", threads=1)
model.prepare(request)          # while the person talks
a = model.answer(request)       # when they stop
```

Give your speech-to-text service the agent's name as a keyterm (Deepgram's `keyterm`). An unusual name is often
misheard otherwise ("Olly" as "Oli"), and a request that names the agent is then missed.

| Output | Meaning |
|---|---|
| `respond` | probability the agent should speak now; about 0.5 for a question left open to the room |
| `intent` | for the agent directly or indirectly, open to the room, about the agent, or other |
| `unclear` | the line fits the agent and someone else equally |

`decide` gives `respond`, `wait` (speak only if nobody else does) or `ignore`, at the thresholds in `config.json`.

## Files

| File | |
|---|---|
| `model.onnx` | default build, fp32, 598 MB (rc0.3 has no int8 build: it failed its quality check) |
| `agent-1x/context.onnx`, `agent-1x/line.onnx` | `agent-1x` build, fp32, 128 + 131 MB |
| `tokenizer.json`, `config.json` (each folder) | tokenizer, calibration and thresholds |
| `data/`, `agent-1x/data/` | the rows each build was trained on (train and dev) |
| `MANIFEST.json` (each folder) | sha256 of every file, row counts |

## Results against Jev

Anonymous speakers. Jev is asked as Pipecat's daily-audience demo asks it.

| Set | Default | `agent-1x` | Jev |
|---|---|---|---|
| [Duplex-MPE](https://huggingface.co/datasets/ChengqianMa/Duplex-MPE), 52,336 lines | 96.4% | 95.7% | 83.1% |
| … lines for others, answered outright | 0.21% | 0.33% | 0.41% |
| … lines for others, held for a pause | 0.8% | 0.7% | 16.0% |
| … request naming the agent, answered | 99.6% | 99.7% | 99.2% |
| … same request without the name, answered | 29.3% | 10.2% | 26.6% |
| [Social AI Ambient Bench](https://huggingface.co/datasets/text-ai/social-ai-ambient-bench), 15,793 lines | 96.9% | 97.5% | 85.4% |
| [AMI](https://huggingface.co/datasets/ACloudCenter/ami-addressee) labelled meetings, 8,875 lines | 99.0% | 98.7% | 85.2% |
| 270 hand-written lines | 87.8% | 86.7% | 77.8% |
| **Real recorded requests in real meetings**, as Deepgram heard them with the name as a keyterm: | | | |
| … without the agent's name, held for a pause (2,705) | 90.9% | 86.6% | 82.1% |
| … naming the agent, answered (61) | 78.7% | 78.7% | 73.8% |
| AMI's meetings as Deepgram heard them: people's lines held for a pause (8,202) | 1.1% | 1.4% | 13.5% |

These are baselines, not proper benchmarks: labels follow the project's own guide, and the choice between
training rounds looked at these sets. The recorded requests are
[SLURP](https://github.com/pswietojanski/slurp)'s test recordings spliced into AMI meetings; they were never
trained on.

## Speed

Median ms per line with 8 earlier lines, one thread, on containers capped like Pipecat Cloud's profiles. Jev is
an API call from the same container, so its time is mostly the network.

| | 0.5 vCPU, 1 GiB | 1 vCPU, 2 GiB | Memory |
|---|---|---|---|
| `agent-1x`, earlier lines encoded ahead | 14 | 14 | 487 MB |
| `agent-1x`, earlier lines not ready | 108 | 68 | |
| Default, fp32 | does not fit well (648, tail to 21 s) | 253 | about 0.9 GB |
| Jev | 49 to 163 | 49 to 149 | |

Encoding the earlier lines takes about 97 ms on `agent-1x`, well inside the time anyone takes to say a line. The
default build's times were measured on rc0.2's default build, which has the same size and graph. On an M5 Max it
takes 10 ms with a short history and 52 ms with 8 earlier lines.

## Limitations

- **More holds on people's own talk than rc0.2.**
  - On real meetings, about 1 line in 100 meant for people is held: the agent speaks only if nobody else does.
    rc0.2 held about 1 in 1,000.
  - On the Ambient Bench, 2 to 3 lines in 100 are held; rc0.2 held about 1.
  - Most of these are questions people ask each other without a name, which in text look like a request to an
    assistant.
  - Neither build answers them outright more often than rc0.2, and Jev holds about 14 in 100.
- **Requests that only the context marks as for the agent** (no name, no request an assistant would obviously
  do) are still often missed. Duplex-MPE's are answered 29% of the time by the default build and 10% by
  `agent-1x`.
- **English text only.** Most training lines are generated; AMI is the only real speech in training, and the
  real requests are text.

## Training

Both use [Ettin](https://huggingface.co/jhu-clsp/ettin-encoder-150m) encoders (MIT) with intent, respond and
unclear heads.

- **Default build:** Ettin-150M, 2 epochs on 240,069 lines.
- **`agent-1x`:** Ettin-32M as one shared encoder for the earlier lines and the new line, joined by a
  cross-attention layer. 3 epochs on 425,828 lines, with the default build's probabilities as 80% of each
  target.

The lines come from three sources:

- **Generated multi-party conversations,** labelled by kind under the project's guide.
- **AMI meetings** ([ACloudCenter/ami-addressee](https://huggingface.co/datasets/ACloudCenter/ami-addressee),
  CC BY 4.0) outside every test meeting, all lines for people.
- **5,000 real requests to assistants:**
  - The requests come from [SLURP](https://github.com/pswietojanski/slurp)'s text (train and devel splits, CC
    BY 4.0; requests in its test split left out) and [CLINC150](https://github.com/clinc/oos-eval)'s queries
    (CC BY 3.0).
  - Each is said in one of those AMI meetings.
  - 45% are without a name and held; 25% have the agent's name added and are answered; 30% have a person's
    name added and are left alone.

Speakers were anonymous in about 60% of training lines, named in 25% and unlabelled in 15%. Duplex-MPE, the
Social AI Ambient Bench and SLURP's recordings were used for evaluation only.
