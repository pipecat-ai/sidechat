# Sidechat

> **Experimental (rc0.3.1).** Outputs, names and calibration may change between releases.

A small text classifier for a voice agent in a conversation with several people. For each line it
says whether the agent should speak now, wait to see if anyone else does, or stay quiet. It runs on
the CPU, and speakers can be anonymous ("Speaker 1").

| | Default | `agent-1x` |
|---|---|---|
| Requests that name the agent, answered | 99.6% | 99.7% |
| People's lines answered by mistake | 0.2% | 0.3% |
| People's lines held for a pause | 0.8% | 0.7% |
| Real spoken requests without the name, held for a pause | 91% | 87% |
| Time per line, int8, on 1 vCPU | 303 ms | 7 ms |
| Download, int8 | 325 MB | 195 MB |

- **Model:** [pipecat-ai/sidechat](https://huggingface.co/pipecat-ai/sidechat) on Hugging Face, ONNX.
  The default build is Ettin-150M; `agent-1x` is a two-tower Ettin-32M for 0.5 vCPU.
- **Training data:** [pipecat-ai/sidechat-gen](https://huggingface.co/datasets/pipecat-ai/sidechat-gen),
  655,339 generated lines.
- **In Pipecat:** [pipecat-ai/pipecat#6934](https://github.com/pipecat-ai/pipecat/pull/6934).

## Use

### In Pipecat

`PipecatSidechat` goes between the user aggregator and the LLM, and lets the LLM answer only the
turns meant for the bot. It is in the pull request above until that is released, with a full bot in
`examples/turn-management/turn-management-sidechat.py`.

```python
from pipecat.turns.sidechat import PipecatSidechat

sidechat = PipecatSidechat(agent_name="Atlas")

pipeline = Pipeline([
    transport.input(), stt, user_aggregator,
    sidechat,
    llm, tts, transport.output(), assistant_aggregator,
])
```

It loads `agent-1x` in int8 unless told otherwise (`variant="small"`); `variant="base"` loads the
default build.

An agent that people ask for the same few things without its name can list them in `commands`. A
turn that contains one is answered whatever the model reads, so list what people ask the agent
for, not words they also use with each other:

```python
sidechat = PipecatSidechat(
    agent_name="Atlas",
    role="voice assistant in the meeting room's screen; it shows the agenda and keeps time",
    commands=["show the agenda", "next item", "start the timer", "stop the timer"],
)
```

### On its own

```bash
pip install git+https://github.com/pipecat-ai/sidechat
```

```python
from huggingface_hub import snapshot_download
from sidechat.runtime import load
from sidechat.schema import Agent, SidechatRequest, Turn

path = snapshot_download("pipecat-ai/sidechat", allow_patterns=["agent-1x/*.json", "agent-1x/*-int8.onnx"])
model = load(f"{path}/agent-1x", threads=1, int8=True)

request = SidechatRequest(
    agent=Agent(name="Atlas"),
    speaker="Speaker 1",
    text="Can you check that for us?",
    history=[Turn(speaker="Atlas", text="Want me to look up flights?", agent=True)],
)
model.prepare(request)  # agent-1x only: encode the earlier lines while the person talks
answer = model.answer(request)
print(answer.respond, model.decide(answer))  # 0.97 respond
```

`decide` gives `respond`, `wait` (speak only if nobody else does) or `ignore`. Give your
speech-to-text service the agent's name as a keyterm, or a misheard name loses the request.

## Strengths and weaknesses

- **It stays quiet through people's talk,** answers when called by name, and holds real requests
  that don't name it until nobody else answers.
- **It is fast and local:** `agent-1x` takes about 10 ms a line on half a CPU.
- **It often misses requests that only the context marks as for the agent,** and a follow-up
  without the name right after the agent answers.
- **An agent that people ask for things without its name misses many of them:** 22% of the lines
  said to a device in a room in one test (32 of 148), and 14% with a list of 10 `commands`, a best
  case.
- **It holds about 1 in 100 of people's lines in real meetings.** English text only.

## Compared with Jev

Jev is a hosted classifier, asked as Pipecat's daily-audience demo asks it. Speakers are anonymous.

| | Default | `agent-1x` | Jev |
|---|---|---|---|
| [Duplex-MPE](https://huggingface.co/datasets/ChengqianMa/Duplex-MPE), decisions right (52,336 lines) | 96.4% | 95.7% | 83.1% |
| [Social AI Ambient Bench](https://huggingface.co/datasets/text-ai/social-ai-ambient-bench), right (15,793) | 96.9% | 97.5% | 85.4% |
| [AMI](https://huggingface.co/datasets/ACloudCenter/ami-addressee) meetings, right (8,875) | 99.0% | 98.7% | 85.2% |
| Duplex-MPE, people's lines held for a pause | 0.8% | 0.7% | 16.0% |
| Duplex-MPE, requests only the context marks, answered | 29.3% | 10.2% | 26.6% |
| Real spoken requests without the name, held (2,705) | 90.9% | 86.6% | 82.1% |
| Time per line on 1 vCPU | 303 ms | 7 ms | 49 to 149 ms |

Labels follow the project's own guide, so read these as comparisons, not benchmarks. Full results
are in [docs/reports/](docs/reports/).

## Repo

| Path | What |
|---|---|
| `sidechat/` | Schema, runtime, data generation, training and the Modal jobs |
| `contracts/` | The labelling guide and the scorecard |
| `data/` | Hand-written test suites and set manifests |
| `hf/` | The model card |
| `docs/` | Reports of measured results, and notes on the datasets considered |

Code and reports cite decisions (`SD-nn`), open questions (`SQ-nn`) and experiments (`exp-nnn`) by
id. Those ids belong to the project's working record, which is not part of this repository.

```bash
uv run pytest -q
```

```bash
uv run ruff check sidechat tests
```

Jobs run detached on Modal and write to R2, with credentials in `.env`:

```bash
set -a; . ./.env; set +a
uv run modal run --detach -m sidechat.pipeline.train::run --exp <exp>
uv run python -m sidechat.pipeline.results <exp>
```
