# Phase 1 notes: the labelling guide, the committee and the scorecard

Closed 2026-11-18. Next: Phase 2, the generated corpus.

Written for whoever picks this up next, with no memory of the session. Read this, then
[TODO.md](../TODO.md) and [DECISIONS.md](../DECISIONS.md). Phase 0's note is
[phase-0-baseline.md](phase-0-baseline.md) and still holds for how jobs run.

## What Phase 1 set out to do

From PLAN.md section 9: a labelling guide with its rules as code, a committee of three large
models that agrees with the guide on at least 90% of a pilot, and a frozen scorecard. All three
are done.

## What exists now

| Item | Where |
|---|---|
| Labelling guide 0.2, the prose the committee reads | [contracts/sidechat-guide-0.2.md](../contracts/sidechat-guide-0.2.md). 0.1 is kept beside it as the record of exp-002 |
| The same guide as code: one label per kind of line, 72 kinds, each citing its rule (G1 to G8) | `sidechat/guide.py` |
| The pilot, labelled from kinds by the guide | `data/suites/pilot-0.4.yaml` (283 lines). 0.1 to 0.3 are kept: each is what some experiment was scored against |
| The committee: prompt, three members, vote, agreement scorecard | `sidechat/committee/` |
| The committee job, detached and resumable | `sidechat/pipeline/label.py` |
| The rhythm of the last turns as roles and numbers (Jon's point) | `sidechat/context.py` |
| The frozen scorecard | [contracts/scorecard-0.1.md](../contracts/scorecard-0.1.md) |
| Tests | `tests/test_phase1.py` (28 tests in all, ruff clean) |

## Results

| Experiment | What | Result |
|---|---|---|
| exp-002 | Committee on pilot-0.2 under guide 0.1 | Majority agrees with the guide on 95.9% (254/265). Target 90% met |
| exp-004 | Committee on pilot-0.3 under guide 0.2 | 98.1% (260/265) |
| exp-005 | exp-004's answers re-scored on pilot-0.4 | **99.2% (263/265)**: respond 76/76, wait 26/26, ignore 161/163 |
| exp-003, exp-006 | Jev re-scored on the relabelled pilot | pilot-0.4: 79.6% of decisions right (211/265) |

Members on pilot-0.4: a 95.5%, b 99.2%, c 98.9%. All three give the same decision and intent on
90.5% of lines. No answer failed and none came from a fallback model in about 1,750 calls.

**Read 99.2% with care.** 13 of the pilot's 283 kinds were corrected after seeing what the committee
said (each correction is listed in `pilot-0.3.yaml` and `pilot-0.4.yaml`, and each follows the
guide's own text). So the pilot now partly fits the committee. The independent test of committee
against guide is the first generated dev set in Phase 3.

Jev on the frozen scorecard's pilot items: lines for the agent that carry no name and depend on
the rhythm of the turns (answers to its question, follow-ups, sessions it leads) are answered at
once only 47.1% of the time (16/34). That is the gap Sidechat exists to close.

Phase 1 spent about $15.60; the project about $17.70 of the proposed $600.

## What the committee taught us

- **Most disagreements were labelling mistakes, not guide gaps.** Of exp-002's 11, nine were kinds
  assigned against the guide's own text. The commonest: a "follow-up" asked by someone other than
  the person the agent had just answered. Kinds must encode such conditions. Phase 2's generator
  knows by construction who the agent answered, so it can choose the kind correctly; a person
  labelling by hand gets it wrong.
- **The rhythm of the turns decides most hard lines.** Who spoke last, whose question the agent
  answered, whether the speaker is that person. This is why Jon's request for an explicit
  "you spoke, they spoke" input matters (SD-13). `sidechat/context.py` gives the roles and numbers.
- **Eight turns can be too few.** "Okay, stop the timer" is for the agent only if you can see it set
  the timer, 11 turns back. The label follows what is visible (`wait`). Facts about what the agent
  controls (timers, music, calls) may be worth adding as input later.
- **Two lines stay split**, and that is fine: "Who's the smallest?" said to a game master's answer
  got respond, wait and ignore from the three members, and a half-asked "what was the name of that
  other place..." got wait against the guide's ignore.
- **Member c is expensive.** Its provider cached about 7% of the shared prompt against 95% for a
  and b, so it costs 6 to 7 times member a. At the plan's ~5,500 committee lines that is ~$100 for
  c alone. Its batch API is half price.

## Jon's three instructions this phase

| Instruction | Where it is now |
|---|---|
| `respond` is a probability; an open question nothing settles should be about 50:50, and the harness decides | SD-12, PLAN.md section 2, guide 0.2 (`speak` 3 is "an even call"), scorecard item 9 |
| The model must read the rhythm of the last few turns, "you spoke, they spoke" | SD-13, `sidechat/context.py`, PLAN.md section 4.2 |
| Diarization labels are often anonymous; people's names are a weak signal, the agent's name the strong one | SD-14, `sidechat/schema.py` docstring, PLAN.md sections 2, 4.2 and 5.3, scorecard conditions (anonymous is the headline) |

## How things run (new since Phase 0)

The committee job, detached:

```bash
set -a; . ./.env; set +a
```

```bash
uv run modal run --detach -m sidechat.pipeline.label::run --exp <exp> --sets <suite or set>
```

```bash
uv run python -m sidechat.pipeline.results <exp>
```

- **Members:** a, b and c, one model family each, at low reasoning effort. Model ids and prices are
  in `.env` only (`LABELLER_A_MODEL`, `LABELLER_B_MODEL`, `LABELLER_C_MODEL`, `LABELLER_PRICES`),
  following Jon's rule from Audience that no labeller or teacher model is named in the repo (SD-09).
  Do not write them into any tracked file, report or R2 object.
- **Answers are stored once per prompt hash** at `runs/side/committee/<prompt_sha>/<member>/` and
  shared by every label set (SD-15). Re-scoring a relabelled set costs nothing. Changing the guide
  changes the hash, so every line is asked again.
- **Labels and reports:** `runs/side/labels/<label_id>/` (labels.jsonl, manifest.json) and
  `runs/side/results/<exp>/`.
- **Guide-labelled suites:** a suite with `label_from: guide` lists each line as
  `[speaker, text, kind]` or `[speaker, text, kind, [people]]`; context-only lines are
  `[speaker, text]`. Labels come from `sidechat/guide.py`.
- **A guard test** (`test_guide_quotes_no_test_line`) fails if the guide quotes any pilot or demo
  line, word for word or nearly. It caught 14 leaks in the first draft.

## Loose ends

| Item | State |
|---|---|
| Git | Nothing committed yet; Jon said "we'll commit later" |
| Call log in `daily-audience` | Still held for Jon (SD-08, SQ-05) |
| Open questions SQ-01, SQ-03 to SQ-08 | Defaults assumed. SQ-02 partly confirmed by SD-12 |
| Guide sentence for anonymous labels | Not yet in the guide (would change the prompt hash). Planned for guide 0.3 in Phase 2 |
| Jev with anonymous speaker labels | Not measured. Duplex-MPE's letters A to D already behave that way |
| Trial objects in R2 | `results/exp-000-side-trial`, `results/exp-002-side-committee-trial`, `baselines/trial-0`, `labels/trial-committee-0`. Small, safe to delete |
| Dataset licences | Still Hub tags only; check before training on anything |

## Phase 2: where to pick up

Goal (PLAN.md sections 5 and 9): the generated corpus, built to guide 0.2's kinds, with anonymous
speaker labels as the default.

1. **Guide 0.3, small:** add that speaker labels may be anonymous ("Speaker 1"), that nobody is
   called by them, and that any name that is not the agent's, used to call someone, means a person.
   Run the committee on an anonymous-label copy of pilot-0.4 (a transform of the suite, not new
   lines) to check agreement holds, and re-ask Jev on the same copy for scorecard item 13.
2. **The conversation generator:** code plans each conversation as beats with a kind, a speaker and
   who it is for, and the writer models write the lines. The kind comes from the plan, so the label
   comes from `sidechat/guide.py` with the rhythm conditions right by construction. Use several
   writer families with one held out for test (PLAN.md 5.2). Teacher and writer model ids go in
   `.env`, like the labellers.
3. **Speaker labels:** most generated lines get anonymous labels and no list of people; some keep
   names; some have no labels (SD-14). Include lines that call people by name, so the model learns
   that a non-agent name means "someone else".
4. **AMI human addressee labels** (`ACloudCenter/ami-addressee`, CC BY 4.0; check the original
   licence): convert to rows for scorecard item 17.
5. **A 500-conversation pilot read by hand** before the full run, then the full run and its twins.
6. **Decide member c's cost** before Phase 3 labels ~5,500 lines: its batch API, or accept ~$100.
7. **Close with `notes/phase-2-corpus.md`.**
