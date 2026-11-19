# Sidechat example

A Pipecat voice bot for a room of people. It hears everything but answers only when Sidechat says
a line was for it. All of it is in [bot.py](bot.py).

```
Deepgram Flux (STT) -> context -> Sidechat gate -> OpenAI -> Deepgram Flux (TTS)
```

## Run

You need the exported model in `../models/side-r3-ettin-150m-s0`, or set `SIDECHAT_MODEL` to its folder.

```bash
cp env.example .env   # add your Deepgram and OpenAI keys
uv sync
uv run bot.py
```

Open http://localhost:7860/client and talk to each other around one microphone. Say "Atlas" to bring the
bot in. Each decision is logged:

```
Sidechat: ignore (respond 0.00) for 'Sam, did you send the deck to the client?'
Sidechat: respond (respond 0.86) for 'And how many people live there?'
Sidechat: wait (respond 0.51) for 'Okay. Does anyone know when the next release is?'
```

`wait` is a question left open to the room: the bot answers it after two quiet seconds, and drops it
if someone else speaks first.

For people on their own devices, run `uv run bot.py -t daily` and share the room URL. That needs
`DAILY_API_KEY`.
