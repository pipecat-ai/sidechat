# Testing Sidechat

Everything below runs on this Mac. The model runs on CPU with ONNX Runtime; no GPU and no API key
are needed to try it.

**The model to try: `side-r3-ettin-150m-s0`** (round 3, Ettin-150M). It is already fetched to
`models/side-r3-ettin-150m-s0/` on this Mac, so you can skip step 1. If a later round beats it, the
latest note in [notes/](notes/) and [TODO.md](TODO.md) say so. In the commands below, `<run_id>`
is that name. The round-1 model, `side-r1-ettin-68m-s0`, is also in `models/` for comparison.

## 1. Fetch the model

```bash
set -a; . ./.env; set +a
```

```bash
uv run python -m sidechat.pipeline.fetch <run_id>
```

That saves `models/<run_id>/` (the ONNX graph, its tokenizer and its config with the decision
thresholds). `models/` is gitignored.

## 2. Try it on the demo's own lines

```bash
uv run python scripts/try_sidechat.py models/<run_id>
```

It prints Sidechat's `respond` probability, its intents and its decision for each of the
daily-audience demo's sample lines, beside Jev's decision from the stored baseline. Add
`--anonymous` to give speakers as "Speaker 1" with no names, as a diarizer would. Add `--int8` to
use the int8 build, if the export has one. rc0.3.1's are about half the size and 1.6 to 1.8 times
faster on one thread, and at their own thresholds make the same decision as fp32 on 98.5% to 99.9%
of test lines; fp32 is the default.

Try your own line, with the turns before it:

```bash
uv run python scripts/try_sidechat.py models/<run_id> --before "Jon: Atlas, how far is Leeds?" --before "Atlas: About forty miles." --line "Sam: And by train?"
```

## 3. Run the demo's own decision code with Sidechat in Jev's place

```bash
PYTHONPATH=. ~/Sites/daily-audience/server/.venv/bin/python scripts/try_in_demo.py models/<run_id>
```

This uses the demo's `AddressingMonitor` and thresholds unchanged and prints what the gate would
do. Nothing in the demo is edited.

## 4. Try it live in the demo

Install this project into the demo's server environment:

```bash
cd ~/Sites/daily-audience/server && uv pip install -e ~/Sites/pipecat-sidechat
```

Then in `server/bot.py`, replace the classifier:

```python
# classifier=JevClassifier(api_key=jev_api_key(), timeout=2.0),
from sidechat.integrations.pipecat_classifier import SidechatClassifier
classifier=SidechatClassifier("/Users/jpt/Sites/pipecat-sidechat/models/side-r3-ettin-150m-s0", bot_name=BOT_NAME),
```

`SidechatClassifier` answers the demo's `addressed` and `question` questions, rescaled so the
demo's thresholds (0.8 and 0.5) fall on the model's own, so nothing else needs to change. The
transcript panel shows its probabilities as it showed Jev's.

## What to expect

On this Mac it takes about 10 ms on a line with little history and 30 to 50 ms with the demo's full
8-line window, against about 165 ms for Jev's round trip. It needs about 1 GB of memory (0.7 GB
for int8), which is more than the deployed bot's `agent-1x` profile leaves. On cloud CPUs it is
slower than Jev: about 250 ms a line with a full history on 1 vCPU, so test it locally first. Details are in
[reports/2026-11-19-side-latency.md](reports/2026-11-19-side-latency.md). Measured against Jev on the same
lines (`experiments/exp-025-side-train-r3/report.md`, anonymous speakers; every scorecard item is in
[reports/2026-11-19-side-r3-ettin-150m-s0-scorecard.md](reports/2026-11-19-side-r3-ettin-150m-s0-scorecard.md)):

| Set | Sidechat | Jev |
|---|---|---|
| Duplex-MPE, 52,336 lines | 96.7% right | 83.1% |
| … lines for others answered outright | 0.2% | 0.4% |
| … lines for others held for a pause | 0.9% | 16.0% |
| … a named request to the agent, answered | 99.5% | 99.2% |
| … the same request with no name, answered | 38.8% | 26.6% |
| Ambient Bench, 15,793 lines | 98.7% | 85.4% |
| AMI meetings, real speech, 8,875 lines | 99.9% | 85.2% |
| Pilot, 270 hand-written lines | 87.4% | 77.8% |
| The demo's 48 lines | 47 | 47 |

What it does: answers when called by name (including thanks and "that's enough"), follows the
rhythm (a follow-up or an answer to its own question with no name is for it), holds about 50:50
on a question left open to the room so the harness can take the floor after a pause, and stays
quiet through talk between people, including talk *about* it.

Where it is weakest: a request to the agent with no name and no sign in the earlier turns that
the agent is in the conversation ("Can you look up the weather?" as the first line). It holds or
lets those go more often than it answers them. Saying its name always works.
