# Sidechat

> **Experimental (rc0.3).** Outputs, names and calibration may change between releases.

A small text classifier for a voice agent in a conversation with several people. For each line it
gives the probability that the agent should speak now, and whether the line was for it, for the
room, or about it. Speaker labels can be anonymous ("Speaker 1"); the agent's own name and the
rhythm of the last turns carry the signal.

Model and training data: [pipecat-ai/sidechat](https://huggingface.co/pipecat-ai/sidechat), ONNX, two builds:

| Build | Where on the Hub | For |
|---|---|---|
| Default: Ettin-150M (`side-r9-ettin-150m-s1`) | repo root | 1 vCPU or more; the more accurate one |
| `agent-1x`: Ettin-32M, two-tower (`side-r9tt-ettin-32m-s1`) | `agent-1x/` | 0.5 vCPU, 1 GiB; encodes the history while the person talks |

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
print(a.respond, model.decide(a))  # 0.97 respond
```

For `agent-1x`, `load(f"{path}/agent-1x", threads=1)`, call `model.prepare(request)` as soon as
the previous line ends, and `model.answer(request)` when the person stops.

Give your speech-to-text service the agent's name as a keyterm (Deepgram's `keyterm`): an unusual
name is otherwise often misheard ("Olly" as "Oli"), and a request that names the agent is then
missed. On real recorded requests this took named requests answered from 13% to 74%.

`decide` turns the probabilities into `respond`, `wait` (speak only if nobody else does) or `ignore`, at
thresholds chosen on dev data. In Pipecat, `sidechat.integrations.pipecat_classifier.SidechatClassifier`
answers the same `yes_no` questions as `JevClassifier`, and encodes the next history in the
background for a two-tower build.

## Results against Jev

Anonymous speakers. Jev is asked exactly as the daily-audience demo asks it.

| Set | Default | `agent-1x` | Jev |
|---|---|---|---|
| Generated test (ours), 21,233 lines; Jev on a 2,882-line sample | 99.0% right | 98.5% | 80.7% |
| [Duplex-MPE](https://huggingface.co/datasets/ChengqianMa/Duplex-MPE), 52,336 lines | 96.4% | 95.7% | 83.1% |
| … lines for others, answered outright | 0.21% | 0.33% | 0.41% |
| … lines for others, held for a pause | 0.8% | 0.7% | 16.0% |
| … request to the agent by name, answered | 99.6% | 99.7% | 99.2% |
| … the same request without the name, answered | 29.3% | 10.2% | 26.6% |
| [Social AI Ambient Bench](https://huggingface.co/datasets/text-ai/social-ai-ambient-bench), 15,793 lines | 96.9% | 97.5% | 85.4% |
| [AMI](https://huggingface.co/datasets/ACloudCenter/ami-addressee) labelled meetings, 8,875 lines | 99.0% | 98.7% | 85.2% |
| AMI held-out meetings, 10,434 lines for people: answered outright | 0 | 0 | 5 |
| AMI through Deepgram, 8,202 lines for people: held for a pause | 1.1% | 1.4% | 13.5% |
| Real recorded requests in AMI meetings, through Deepgram with the name as keyterm: unnamed, held (2,705) | 90.9% | 86.6% | 82.1% |
| … naming the agent, answered (61) | 78.7% | 78.7% | 73.8% |
| Pilot, 270 hand-written lines | 87.8% | 86.7% | 77.8% |
| The demo's 48 lines | 48 | 48 | 47 |

**These are baselines, not proper benchmarks.** Some sets are small or written by us, labels follow
our own guide (`contracts/`), and the choice between training rounds looked at these sets.

rc0.3 adds real people's requests to assistants (SLURP's and CLINC150's text, said in AMI meetings)
to training. Both builds now hold most unnamed requests said before the agent has spoken, which rc0.2
mostly ignored (17% and 4% held). The cost is more holds on people's own talk: about 1 in 100 of
AMI's lines (rc0.2: about 1 in 1,000), mostly questions people ask each other without a name.
Details: [reports/2026-11-20-side-round9.md](reports/2026-11-20-side-round9.md).

## Size and speed

Per line, median ms with 8 earlier lines, through the demo's gate, 1 thread. The cloud columns are
Modal containers capped like Pipecat Cloud's `agent-1x` and `agent-2x`.

| | 0.5 vCPU, 1 GB | 1 vCPU, 2 GB | Mac (M5 Max) | Memory |
|---|---|---|---|---|
| `agent-1x` fp32, history encoded ahead | 14 | 14 | | 487 MB |
| `agent-1x` fp32, history not ready | 108 | 68 | | |
| Default fp32 (598 MB file) | 648, tail to 21 s | 253 | 52 | about 0.9 GB |
| Jev (an API call) | 49 to 163 | 49 to 149 | 172 | |

Encoding the history takes about 97 ms on `agent-1x`, well inside the time anyone takes to say a
line. The default build's times are rc0.2's (same size and graph); rc0.3 ships no int8 build, which
failed its quality check. Jev's time is the network, so it varies between containers. Details:
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
