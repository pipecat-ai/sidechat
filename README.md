# Sidechat

> **Experimental.** Outputs, names and calibration may change between releases.

A small text classifier for a voice agent in a conversation with several people. For each line it
gives the probability that the agent should speak now, and whether the line was for it, for the
room, or about it. Speaker labels can be anonymous ("Speaker 1"); the agent's own name and the
rhythm of the last turns carry the signal.

Model and training data: [pipecat-ai/sidechat](https://huggingface.co/pipecat-ai/sidechat) (Ettin-150M encoder, ONNX).

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

`decide` turns the probabilities into `respond`, `wait` (speak only if nobody else does) or `ignore`, at
thresholds chosen on dev data. In Pipecat, `sidechat.integrations.pipecat_classifier.SidechatClassifier`
answers the same `yes_no` questions as `JevClassifier`.

## Results against Jev

Anonymous speakers. Jev is asked exactly as the daily-audience demo asks it.

| Set | Sidechat | Jev |
|---|---|---|
| Generated test (ours), 2,882 lines | 99.1% right | 80.7% |
| [Duplex-MPE](https://huggingface.co/datasets/ChengqianMa/Duplex-MPE), 52,336 lines | 96.7% | 83.1% |
| … lines for others, answered outright | 0.2% | 0.4% |
| … lines for others, held for a pause | 0.9% | 16.0% |
| … request to the agent by name, answered | 99.5% | 99.2% |
| … the same request without the name, answered | 38.8% | 26.6% |
| [Social AI Ambient Bench](https://huggingface.co/datasets/text-ai/social-ai-ambient-bench), 15,793 lines | 98.7% | 85.4% |
| [AMI](https://huggingface.co/datasets/ACloudCenter/ami-addressee) labelled meetings, 8,875 lines | 99.9% | 85.2% |
| AMI held-out meetings, 10,434 lines for people: answered outright | 0 | 5 |
| Pilot, 270 hand-written lines | 87.4% | 77.8% |
| The demo's 48 lines | 47 | 47 |

**These are baselines, not proper benchmarks.** Some sets are small or written by us, labels follow
our own guide (`contracts/`), and the choice between training rounds looked at these sets.

## Size and speed

About 150M parameters: `model.onnx` 598 MB (fp32), `model-int8.onnx` 267 MB. Per line, median ms
with a short history / with 8 earlier lines, through the demo's gate, 1 thread:

| | Mac (M5 Max) | 1 vCPU, 2 GB | 0.5 vCPU, 1 GB |
|---|---|---|---|
| Sidechat fp32 (about 0.9 GB resident) | 10 / 52 | 66 / 253 | 507 / 648, tail to 21 s |
| Sidechat int8 (about 0.6 GB) | 9 / 49 | 51 / 271 | 103 / 532 |
| Jev (an API call) | 165 / 172 | 53 to 149 | |

The cloud rows are Modal containers capped like Pipecat Cloud's `agent-2x` and `agent-1x`; Jev's
range there is from three containers. Time grows with the history, so on a small cloud CPU this
model is slower than Jev's round trip. More threads only help on more cores. Details:
[reports/](reports/).

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
