---
license: bsd-2-clause
language: en
library_name: onnx
pipeline_tag: text-classification
base_model:
  - jhu-clsp/ettin-encoder-150m
  - jhu-clsp/ettin-encoder-32m
datasets:
  - pipecat-ai/sidechat-gen
  - ACloudCenter/ami-addressee
tags:
  - pipecat
  - onnx
  - addressee-detection
  - multi-party
  - turn-taking
---

# Pipecat Sidechat (experimental, rc0.3.1)

> **⚠️ Experimental.** Outputs, names and calibration may change between releases.

A small text classifier for a voice agent in a conversation with several people. For each line it says whether
the agent should speak now, wait to see if anyone else does, or stay quiet. It runs on the CPU, and speakers can
be anonymous ("Speaker 1").

| | Default | `agent-1x` |
|---|---|---|
| Requests that name the agent, answered | 99.6% | 99.7% |
| People's lines answered by mistake | 0.2% | 0.3% |
| People's lines held for a pause | 0.8% | 0.7% |
| Real spoken requests without the name, held for a pause | 91% | 87% |
| Time per line, int8, on 1 vCPU | 303 ms | 7 ms |
| Download, int8 | 325 MB | 195 MB |

The first three rows are on [Duplex-MPE](https://huggingface.co/datasets/ChengqianMa/Duplex-MPE), 52,336 lines.
The fourth is on recorded requests placed in real meetings, as Deepgram heard them.

Code: [github.com/pipecat-ai/sidechat](https://github.com/pipecat-ai/sidechat).
Training data: [pipecat-ai/sidechat-gen](https://huggingface.co/datasets/pipecat-ai/sidechat-gen).

## Builds

| Build | Folder | For |
|---|---|---|
| Default, 150M | repo root | 1 vCPU or more; the more accurate one |
| `agent-1x`, 32M two-tower | `agent-1x/` | 0.5 vCPU, 1 GiB; encodes the earlier lines while the person talks |

Each has fp32 and int8 files. int8 decides the same as fp32 on 98.5% to 99.9% of test lines.

## Use

### In Pipecat

`PipecatSidechat` goes between the user aggregator and the LLM, and lets the LLM answer only the turns meant
for the bot:

```python
from pipecat.turns.sidechat import PipecatSidechat

sidechat = PipecatSidechat(agent_name="Atlas")

pipeline = Pipeline([
    transport.input(), stt, user_aggregator,
    sidechat,
    llm, tts, transport.output(), assistant_aggregator,
])
```

It loads `agent-1x` in int8 unless told otherwise (`variant="small"`); `variant="base"` loads the default
build. It is in [pipecat-ai/pipecat#6934](https://github.com/pipecat-ai/pipecat/pull/6934) until that is
released, with a full bot in `examples/turn-management/turn-management-sidechat.py`.

### An agent that responds to commands

The model learned from meetings, where a request that doesn't name the agent is most often for a person. An
agent that people ask for the same few things without its name, such as one that runs the screen in a room, can
list them in `commands`. A turn that contains one is answered whatever the model reads:

```python
sidechat = PipecatSidechat(
    agent_name="Atlas",
    role="voice assistant in the meeting room's screen; it shows the agenda and keeps time",
    commands=["show the agenda", "next item", "start the timer", "stop the timer"],
)

@sidechat.event_handler("on_sidechat_decision")
async def on_sidechat_decision(sidechat, verdict):
    logger.info(f"{verdict.decision} ({verdict.reason}): {verdict.line.text}")
```

| Someone says | The model alone | With `commands` |
|---|---|---|
| "Atlas, show the agenda." | respond | respond |
| "Okay. Next item." | ignore | respond |
| "Show the agenda again." | ignore | respond |
| "Did you get the numbers from Priya?" | ignore | ignore |
| "I can take the next item if you like." | ignore | respond |

These are `agent-1x`'s decisions on one scripted meeting. The last row is the cost: a command matches by its
words, whole and in any case, so the same words said to a person are answered too. List what people ask the
agent for ("show the agenda"), not words they also use with each other ("the agenda"). A turn answered this way
reports the reason `command`.

`role` is one line on what the agent is and does. The model reads it with every turn.

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

| Output | Meaning |
|---|---|
| `respond` | probability the agent should speak now; about 0.5 for a question left open to the room |
| `intent` | for the agent directly or indirectly, open to the room, about the agent, or other |
| `unclear` | the line fits the agent and someone else equally |

`decide` gives `respond`, `wait` (speak only if nobody else does) or `ignore`, at the thresholds in
`config.json`. For the default build, load the repo root with `model.onnx` or `model-int8.onnx`.

Give your speech-to-text service the agent's name as a keyterm (Deepgram's `keyterm`). An unusual name is often
misheard otherwise, and a request that names the agent is then missed.

## Strengths and weaknesses

**Strengths**

- **It stays quiet through people's talk.** It answers 0.2% of lines meant for others and holds under 1%.
- **It answers when called.** Requests that name the agent are answered 99.6% of the time.
- **It holds real requests that don't name it** (91%), and answers if nobody else does.
- **It is fast and local.** `agent-1x` takes about 10 ms a line on half a CPU, with no API call.

**Weaknesses**

- **Requests that only the context marks as for the agent** are often missed: 29% answered by the default
  build and 10% by `agent-1x`.
- **A follow-up without the name, right after the agent answers,** is hard to tell from talk to another
  person.
- **An agent that people ask for things without its name** misses many of them. In a test with a device in a
  room, the default build ignored 22% of the lines said to it (32 of 148) and `agent-1x` 29%. A list of 10
  `commands` brought that to 14% and 17%, and matched none of 3,329 lines of people's household talk. The list
  was written by someone who had read the test's lines, so take that as a best case.
- **About 1 in 100 of people's lines in real meetings is held for a pause,** mostly questions people ask each
  other without a name.
- **English text only.**

## Compared with Jev

Jev is a hosted classifier, asked as Pipecat's daily-audience demo asks it. Speakers are anonymous.

| | Default | `agent-1x` | Jev |
|---|---|---|---|
| Duplex-MPE, decisions right (52,336 lines) | 96.4% | 95.7% | 83.1% |
| [Social AI Ambient Bench](https://huggingface.co/datasets/text-ai/social-ai-ambient-bench), right (15,793) | 96.9% | 97.5% | 85.4% |
| [AMI](https://huggingface.co/datasets/ACloudCenter/ami-addressee) meetings, right (8,875) | 99.0% | 98.7% | 85.2% |
| Duplex-MPE, people's lines held for a pause | 0.8% | 0.7% | 16.0% |
| Duplex-MPE, requests only the context marks, answered | 29.3% | 10.2% | 26.6% |
| Real spoken requests without the name, held (2,705) | 90.9% | 86.6% | 82.1% |
| Time per line on 1 vCPU | 303 ms | 7 ms | 49 to 149 ms |

Labels follow the project's own guide, so read these as comparisons, not benchmarks.

## Training

Both builds use [Ettin](https://huggingface.co/jhu-clsp/ettin-encoder-150m) encoders (MIT) with intent, respond
and unclear heads. `agent-1x` is distilled from the default build.

- **Our data:** generated multi-party conversations, labelled by kind under the project's guide. All of it is
  in [pipecat-ai/sidechat-gen](https://huggingface.co/datasets/pipecat-ai/sidechat-gen).
- **Public data:** [AMI](https://huggingface.co/datasets/ACloudCenter/ami-addressee) meetings (CC BY 4.0), and
  5,000 requests to assistants from [SLURP](https://github.com/pswietojanski/slurp)'s text (CC BY 4.0) and
  [CLINC150](https://github.com/clinc/oos-eval) (CC BY 3.0), each placed in an AMI meeting.

Duplex-MPE, the Social AI Ambient Bench and SLURP's recordings were used for evaluation only.
