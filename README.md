# Sidechat

> **Experimental (rc0.2).** Outputs, names and calibration may change between releases.

A small text classifier for a voice agent in a conversation with several people. For each line it
gives the probability that the agent should speak now, and whether the line was for it, for the
room, or about it. Speaker labels can be anonymous ("Speaker 1"); the agent's own name and the
rhythm of the last turns carry the signal.

Model and training data: [pipecat-ai/sidechat](https://huggingface.co/pipecat-ai/sidechat), ONNX, two builds:

| Build | Where on the Hub | For |
|---|---|---|
| Default: Ettin-150M | repo root | 1 vCPU or more; the more accurate one |
| `agent-1x`: Ettin-32M, two-tower | `agent-1x/` | 0.5 vCPU, 1 GiB; encodes the history while the person talks |

## Use

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

For `agent-1x`, `load(f"{path}/agent-1x", threads=1)`, call `model.prepare(request)` as soon as
the previous line ends, and `model.answer(request)` when the person stops.

`decide` turns the probabilities into `respond`, `wait` (speak only if nobody else does) or `ignore`, at
thresholds chosen on dev data. In Pipecat, `sidechat.integrations.pipecat_classifier.SidechatClassifier`
answers the same `yes_no` questions as `JevClassifier`, and encodes the next history in the
background for a two-tower build.

## Results against Jev

Anonymous speakers. Jev is asked exactly as the daily-audience demo asks it.

| Set | Default | `agent-1x` | Jev |
|---|---|---|---|
| Generated test (ours), 21,233 lines; Jev on a 2,882-line sample | 99.0% right | 98.5% | 80.7% |
| [Duplex-MPE](https://huggingface.co/datasets/ChengqianMa/Duplex-MPE), 52,336 lines | 96.7% | 95.6% | 83.1% |
| … lines for others, answered outright | 0.22% | 0.26% | 0.41% |
| … lines for others, held for a pause | 0.9% | 0.8% | 16.0% |
| … request to the agent by name, answered | 99.5% | 98.7% | 99.2% |
| … the same request without the name, answered | 38.8% | 10.7% | 26.6% |
| [Social AI Ambient Bench](https://huggingface.co/datasets/text-ai/social-ai-ambient-bench), 15,793 lines | 98.7% | 98.4% | 85.4% |
| [AMI](https://huggingface.co/datasets/ACloudCenter/ami-addressee) labelled meetings, 8,875 lines | 99.9% | 100.0% | 85.2% |
| AMI held-out meetings, 10,434 lines for people: answered outright | 0 | 0 | 5 |
| Pilot, 270 hand-written lines | 87.4% | 87.4% | 77.8% |
| The demo's 48 lines | 47 | 47 | 47 |

**These are baselines, not proper benchmarks.** Some sets are small or written by us, labels follow
our own guide (`contracts/`), and the choice between training rounds looked at these sets.

`agent-1x` mostly ignores a request without the agent's name before the agent has spoken; Jev
mostly holds for a pause on those.

## Size and speed

Per line, median ms with 8 earlier lines, through the demo's gate, 1 thread. The cloud columns are
Modal containers capped like Pipecat Cloud's `agent-1x` and `agent-2x`.

| | 0.5 vCPU, 1 GB | 1 vCPU, 2 GB | Mac (M5 Max) | Memory |
|---|---|---|---|---|
| `agent-1x` fp32, history encoded ahead | 10 to 15 | 9 | | 488 MB |
| `agent-1x` fp32, history not ready | 88 to 117 | 35 | | |
| Default int8 (267 MB file) | 532 | 271 | 49 | about 0.6 GB |
| Default fp32 (598 MB file) | 648, tail to 21 s | 253 | 52 | about 0.9 GB |
| Jev (an API call) | 56 to 163 | 58 to 149 | 172 | |

Encoding the history takes about 76 ms on `agent-1x`, well inside the time anyone takes to say a
line. Jev's time is the network, so it varies between containers. Details: [reports/](reports/).

## Repo

| Path | What |
|---|---|
| `sidechat/` | Schema, runtime, Pipecat adapter, data generation, training and Modal jobs |
| `contracts/` | The labelling guide and scorecard |
| `notes/`, `experiments/`, `reports/` | One note per phase, one record per run, write-ups |
| `PLAN.md`, `DECISIONS.md`, `DATASETS.md`, `BUDGET.md`, `TODO.md` | Plan, decisions, data survey, spend, status |

Jobs run detached on Modal and write to R2 (credentials in `.env`):

```bash
set -a; . ./.env; set +a
uv run modal run --detach -m sidechat.pipeline.train::run --exp <exp> ...
uv run python -m sidechat.pipeline.results <exp>
```

```bash
uv run pytest -q
```
