# Phase 7 notes, part 1: Sidechat in Pipecat

2026-11-19. Phase 7 (ship) is in progress. The model is already public on Hugging Face
(`pipecat-ai/sidechat`, commit `c9b59be`, exp-034, published by another session). This part adds
the Pipecat module that downloads and runs it, and a Labs docs page. Neither is committed. Read
this, then [TODO.md](../TODO.md).

## Where things stand

- **Pipecat core**, branch `jpt/sidechat` in `~/Sites/pipecat` (cloned for this), uncommitted:
  `pipecat.models.labs.side_chat`, ready for a PR once the model is on Hugging Face.
- **The model**: Pipecat downloads `pipecat-ai/sidechat` pinned at commit
  `c9b59bebf7e17993df3f55a9a81813bdccd80c7b`, in the export's own layout (`model.onnx`,
  `model-int8.onnx`, `tokenizer.json`, `config.json` with `thresholds` and `thresholds_int8`). The
  repo has no tags yet.
- **Docs**: a new Labs tab with an overview and a Sidechat page, branch `jpt/labs-sidechat` in a
  worktree at `~/Sites/pipecat-docs-labs`, uncommitted. The main `~/Sites/pipecat-docs` checkout,
  with Jon's uncommitted Voice Reader callout, is untouched.

## What exists now

| Item | Where |
|---|---|
| Inputs, ported exactly: roles, rhythm numbers, encoder text (`sidechat-input-0.2`) | `src/pipecat/models/labs/side_chat/conversation.py` |
| `SideChatModel`: download from `pipecat-ai/sidechat` at a pinned commit, tokenizer and ONNX on the CPU, temperatures, thresholds per precision; refuses a config with `text_turns`, which it doesn't build | `.../side_chat/model.py` |
| `SideChatClassifier`: a `BaseClassifier` that answers its own questions (`respond`, `addressed`, `open`, `intent`, `unclear`) about a dict state | `.../side_chat/classifier.py` |
| `SideChatGate` and `SideChatListener`: the drop-in, see below | `.../side_chat/gate.py` |
| 39 tests | `tests/test_side_chat.py` |
| Example bot | `examples/labs/labs-sidechat-group-conversation.py` |
| `sidechat` extra (`huggingface_hub`, `tokenizers`) and `uv.lock` | `pyproject.toml` |
| Parity check, this repo's runtime against the port | `scripts/check_pipecat_parity.py` (this repo) |

### How the gate works

```
transport.input() -> stt -> gate.listener() -> user_aggregator -> gate -> llm -> tts -> transport.output() -> assistant_aggregator
```

- The **gate** holds each user turn's `LLMContextFrame` and asks the model: `respond` passes it on,
  `hold` waits `hold_secs` (2.5) of nobody speaking and then passes it (dropped if anyone starts
  speaking), `ignore` drops it. The line stays in the context either way, so the bot hears
  everything, as the daily-audience demo does.
- History comes from `LLMContextUserTurnFrame` (people) and `LLMContextAssistantTurnFrame` (the
  bot), up to 8 turns.
- The **listener** sits before the user aggregator, because the aggregator drops speaker
  information. It labels speakers "Speaker 1", "Speaker 2"... from `TranscriptionFrame.speaker`
  (diarization) and `user_id` (transport participants); a turn goes to whoever said most of it.
- `over_agent` is True when speech started while the bot spoke, otherwise None, never False:
  training only ever saw True or nothing.
- If the model fails or takes over `timeout` (2 s), the gate answers only lines that name the bot.
  A model that can't load marks the gate unusable and the same rule applies.
- An eager-end-of-turn speculation that the model would hold is dropped instead.
- `on_verdict` reports each decision with `respond` and `open`.

## Results

**The Hub's files**: `config.json`, `tokenizer.json`, `model.onnx` and `model-int8.onnx` in
`models/side-r3-ettin-150m-s0/` have the sha256s in the Hub's `MANIFEST.json`, so every run below
is the model Pipecat downloads. The download itself stalled from this sandbox: metadata and small
files came from huggingface.co, the large files' storage host made no progress. It is covered by a
unit test with the Hub faked, and needs one real run on a normal network.

**Parity** (`scripts/check_pipecat_parity.py`, 10.5 minutes on this Mac): 6,544 lines, every
suite in all three speaker conditions plus variants with aliases, people, speech over the agent
and histories long enough to be truncated (401 at the 320-token limit). Inputs identical on every
line. Probabilities within 5e-7 (this repo rounds to 6 places) and no decision differs, for fp32
and for int8.

**The real model through the gate**, two diarized speakers and a bot named Atlas:

| Line | Gate |
|---|---|
| Speaker 1: Morning! Did you see the game last night? | ignore, respond 0.00 |
| Speaker 2: I did, what a finish. | ignore, 0.00 |
| Speaker 1: Should we ask Atlas who scored? | ignore, 0.00 |
| Speaker 2: Atlas, who scored the winning goal? | respond, 1.00 |
| (bot answers) Speaker 2: And who assisted? | respond, 1.00 |
| Speaker 1: Does anyone know when the next match is? | hold, 0.50, then respond after the silence |
| Speaker 2: Thanks, Atlas. | respond, 0.68 |

**Tests**: 39 pass, stable over repeated parallel runs. Ruff clean. The three failures in
`tests/test_adapters_llm_shims.py` locally are missing extras and fail the same on `main`.
`scripts/check_licenses.py` passes. CI gets `tokenizers` and `huggingface_hub` through the `cli`
extra, as it does for the Voice Reader tests. Docs: `docs-meta-lint` clean for the new pages,
`mint broken-links --check-anchors --check-redirects` clean, `llms.txt` regenerated.

## How things run

```bash
~/Sites/pipecat/.venv/bin/python scripts/check_pipecat_parity.py models/side-r3-ettin-150m-s0
```

```bash
cd ~/Sites/pipecat && uv run pytest tests/test_side_chat.py -q
```


## Things learned

- **The user aggregator drops who spoke.** `TranscriptionFrame` carries `speaker` and `user_id`,
  but the turn it writes doesn't, so the gate needs a listener before the aggregator.
- **An STT service's `speaker_format` writes labels into the text**, where the model would read
  them as words. The docs and example leave it unset.
- **Train-time conventions leak into the runtime contract**: `over_agent` must be None, not False,
  and the role defaults to "AI assistant on the call", one of the training roles.
- **Release evals can't assert silence** (no scripted expectation for "the bot says nothing"), so
  the example has no eval entry yet.
- **Interruptions are separate.** The gate decides whether the bot answers, not whether it can be
  cut off: with the default turn start strategies, people talking to each other interrupt the bot.

## Loose ends, held for Jon

1. **Open the PR** on pipecat, then add the changelog fragment under its number (text below).
2. **Optionally tag the Hub commit** (`rc1`) and pin the tag instead of the sha.
3. **A model with `text_turns`** (the short-input models exp-036 is trying) needs `fitted()` ported
   to `conversation.py`; until then `SideChatModel` refuses its config. Run the parity check again
   on any new export before Pipecat pins it.
4. **The docs page names no Pipecat version.** Add "needs Pipecat X or later" once the release that
   carries the PR is known. It names Jev as the baseline, as the public card does.
5. Not tested here: the real download from the Hub, and the gate with live speech recognition on a
   real call (SQ-05). The card's timings put 0.5 vCPU at 507 to 648 ms a line; the docs say to give
   the bot at least one vCPU.
6. Possible next pieces: an interruption strategy that lets only lines for the bot cut it off; a
   release eval once scripted scenarios can expect silence; always answering when one person is
   present (needs the transport's participant count).

## Where the next phase picks up

1. Jon reviews; commit and open the pipecat PR and the docs PR (docs after the Pipecat release).
2. Try `examples/labs/labs-sidechat-group-conversation.py` on a real Daily call with two or three
   people.
3. Then PLAN.md phase 6 (real speech) and the open items in
   [phase-4-models.md](phase-4-models.md).

## PR draft for pipecat

**Title:** Add Sidechat, a Pipecat Labs model for bots in group conversations

A bot that shares a call with several people answers every line it hears. Sidechat
(https://huggingface.co/pipecat-ai/sidechat) is a small text model that reads each line with the
turns before it and says whether it was for the bot and whether the bot should speak now, after
a pause, or not at all. It runs on the CPU in about 10 to 50 ms a line. This adds it under a new
`pipecat.models.labs` package for experiments, which can change or be removed in any release.

- **`SideChatGate`.** Goes between the user aggregator and the LLM and holds each user turn's
  context frame. A line for the bot runs the LLM; a question to the room runs it after
  `hold_secs` of nobody speaking; anything else is dropped, and the line stays in the context.
  `on_verdict` reports each decision. If the model can't answer, only lines that name the bot are
  answered.
- **`SideChatListener`.** From `gate.listener()`, goes between the STT service and the user
  aggregator and labels each line's speaker from diarization or the transport's participants, since
  the aggregator's turn doesn't say who spoke.
- **`SideChatClassifier`.** The model behind the classifier interface. It answers its own
  questions, `respond`, `addressed`, `open`, `intent` and `unclear`, about a state with the line,
  its speaker and up to 8 earlier turns.
- **Model.** `SideChatModel` downloads from Hugging Face at a pinned commit on first use, and a
  process loads it once. `fp32` by default, `int8` at about 0.7 GB instead of 1 GB, each with the
  thresholds its release chose. The `sidechat` extra adds `huggingface_hub` and `tokenizers`.
- **Example.** `examples/labs/labs-sidechat-group-conversation.py`, a Daily bot with Deepgram
  diarization.

**Changelog fragment** (`changelog/<PR>.added.md`):

- Added Sidechat, a Pipecat Labs model in `pipecat.models.labs.side_chat` that tells a bot in a
  group conversation which lines are for it. `SideChatGate` goes between the user aggregator and
  the LLM and lets the LLM answer only those lines: it answers a line for the bot, answers a
  question to the room if nobody else speaks for `hold_secs`, and stays quiet otherwise.
  `gate.listener()` goes before the user aggregator and tells it who said each line.
  `SideChatClassifier` answers the model's own questions (`respond`, `addressed`, `open`, `intent`
  and `unclear`) about a line and the turns before it. The model runs on the CPU and downloads from
  Hugging Face on first use. Labs models are experimental and can change or be removed in any
  release. Install with `pipecat-ai[sidechat]`; see
  `examples/labs/labs-sidechat-group-conversation.py`.
