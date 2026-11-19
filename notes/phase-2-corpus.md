# Phase 2 notes: the generated corpus

Closed 2026-11-19. Phases 3 and 4 (committee check of generated labels, first models) were started
in the same overnight session; see `notes/phase-4-models.md` when it exists.

Written for whoever picks this up next. Read this, then [TODO.md](../TODO.md) and
[DECISIONS.md](../DECISIONS.md). Jon authorized autonomous overnight work within $1,000 (SD-17).

## What exists now

| Item | Where |
|---|---|
| Guide 0.3: how to read anonymous speaker labels | `contracts/sidechat-guide-0.3.md`, `sidechat/guide.py` |
| Speaker-label conditions (named, anonymous, none); a set name can carry one, e.g. `pilot-0.4@anonymous` | `sidechat/conditions.py`, `sidechat/sources/build.py` |
| The world: 18 settings (2 held out), 28 agent names (4 held out, word-like ones for G5), sound-alike people, devices, registers | `sidechat/gen/world.py` |
| The planner: conversations as beats, each kind with preconditions on the conversation's rhythm | `sidechat/gen/planner.py` |
| The writer prompt, per-kind briefs, and the checks that flag a line breaking its brief | `sidechat/gen/writer.py` |
| The four writers (model ids in `.env` only: `WRITER_A/B/C/O_MODEL`, `WRITER_PRICES`) | `sidechat/gen/writers.py` |
| Rows, splits and `label_safe` | `sidechat/gen/rows.py` |
| The generation job (detached; one function per writer in parallel; resumable) | `sidechat/pipeline/generate.py` |
| A generated corpus as a scoring set: `corpus:<gen_id>[:<splits>[:<n>]]` | `sidechat/sources/build.py` |
| AMI meetings with a silent agent (human addressee labels, real speech, test only) | `sidechat/sources/ami.py`, set `ami` |
| Tests | `tests/test_phase2.py` |

## Writers

| Writer | Family | Use |
|---|---|---|
| o | Open weights, the teacher Audience used, served with vLLM on an H100 from the cached `waystone-hf-cache` volume | Training, dev and test |
| a | OpenAI-style API, an efficient tier | Training, dev and test |
| c | Google-style API, an efficient tier | Training, dev and test |
| b | Anthropic API | **Test only**: wording no training writer produced |

## Results so far

| Experiment | What | Result |
|---|---|---|
| exp-007 | Committee on pilot-0.4 with anonymous speakers, guide 0.3 | 98.9% agree (named, guide 0.2: 99.2%) |
| exp-008 | Jev on pilot-0.4 with anonymous speakers | 77.4% right, against 79.6% named |
| exp-009 | Generator trial, 8 conversations per writer | Worked; found the planner putting person-to-person lines right after the agent asked something (fixed) |
| exp-010 | Generator pilot `gen-pilot`: 599 conversations, 8,426 lines, $3.49 | 97.7% of lines keep to their brief |
| exp-011 | **Committee on 430 gen-pilot dev and test lines, blind** | **Agrees with the generated labels on 95.3% (410/430)**: ignore 97.9%, respond 99.3%, wait 74.1% |
| exp-012 | **Full corpus `gen-0.1`**: o 4,000, a 1,700, c 1,700, b 700 conversations, about $43 | 8,095 conversations, 113,262 lines (train 84,304, dev 8,398, test 20,560); ignore 60,270, respond 34,631, wait 13,254, even call 5,107; 110,631 keep to their brief |
| exp-016 | Jev on 3,000 generated test lines, each in the named and anonymous condition | 81.2% right named, 80.7% anonymous; answers 1.4 to 1.7% of lines for others at once and holds 18 to 19% of them |

The `wait` disagreements are follow-ups and challenges to the agent's answer from someone other
than its partner, which the committee often calls `respond`. They stay `wait` (a 0.5 target), the
even call Jon asked for (SD-12).

## Things learned

- **The planner must not put a person-to-person line right after the agent asks or answers.** The
  writer turns it into an answer to the agent, and the label is then wrong. `_allowed` forbids it.
- **Writers often refer to the agent as "it" in remarks about it.** The check flags those lines,
  but their label (stay quiet) is still right, so `label_safe` keeps them. A line whose problem
  could change the label (the agent called when it should not be, or not called when it should)
  is left out of training.
- **The open-weights writer is the cheapest by far** (about $0.001 a conversation on an H100) and
  writes well. API writers cost a quarter of a cent (a) to two cents (b, c) a conversation.
- **Member c of the committee is still the expensive one** (about 70% of committee cost).
