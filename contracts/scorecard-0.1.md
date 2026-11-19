# Sidechat scorecard 0.1

Frozen 2026-11-18 (DECISIONS.md SD-16). Changes only by a logged revision. Every item says which
set it is scored on, Jev's measured number where one exists, and the target.

## How Sidechat is scored

**Its output is probabilities, not a decision** (SD-12). `respond` is how likely it is that the
agent should speak now. A line that leaves it open, such as a question to the room that nothing
earlier settles, should score about 0.5, and the system using the model decides what to do with
that, such as taking the floor after a pause.

To compare with Jev's decisions, Sidechat's outputs become the same three outcomes the
daily-audience gate has:

- **answer now** when `respond` ≥ *t*<sub>r</sub>;
- **hold for a pause** when `respond` ≥ *t*<sub>w</sub>, or `intent.open` ≥ *t*<sub>o</sub>;
- otherwise **stay quiet**.

The three thresholds are chosen on the dev split and fixed before the test split is opened. Jev
is scored twice: with the demo's thresholds (`addressed` 0.8, `question` 0.5) and with thresholds
tuned on the same dev split. Comparisons use whichever Jev is better on that item.

**Statistics.** Every share has its count and a 95% Wilson interval. A difference is a paired
bootstrap of 1,000 resamples on the same lines. It counts when it is at least 0.1 points on a set
of at least 30 lines. "Worse" means the whole interval is below zero. Code:
`sidechat/lib/score.py`.

## Conditions

Diarization labels are often anonymous ("Speaker 1"), and people do not call each other by them.
The agent's name is the one name that is reliable (SD-14). So every item is scored in three
conditions, and **anonymous is the headline**:

| Condition | Speaker labels | List of people | Notes |
|---|---|---|---|
| **Anonymous** (headline) | "Speaker 1", "Speaker 2", ... | Not given | What a diarized transcript usually gives |
| Named | Real names | Given | What the daily-audience demo gives |
| No labels | None | Not given | An undiarized transcript |

Duplex-MPE's speakers are the letters A to D, so its numbers below are effectively anonymous.

## Sets

| Set | Lines | Labels | Status |
|---|---|---|---|
| `pilot-0.4` | 283 (265 with a definite decision) | Guide 0.2. Committee majority agrees on 99.2% (exp-005), but 13 kinds were corrected after seeing committee answers | Built |
| `demo-lines-0.1` | 52 | The daily-audience author's expectations | Built |
| Duplex-MPE | 52,364 turns | The benchmark's, read per utterance (SD-07). Never trained on | Built |
| Social AI Ambient Bench | 16,222 messages | The benchmark's. Never trained on (SD-06) | Built |
| Main test | To be set | Generated, committee-checked | Phase 2 and 3 |
| Held-out writer, settings and agent names | To be set | As main test | Phase 2 and 3 |
| Real speech-to-text twins | To be set | As main test | Phase 6 |
| AMI silence test | 139 meetings | Every line is for someone else | Phase 6 |
| AMI human addressee labels | 8,876 utterances | Human annotators | Phase 2 |
| Real calls from the demo | 300 to 1,000 | Committee plus Jon | Held (SQ-05) |

## Items

Jev's numbers come from exp-001 (Duplex-MPE, Ambient Bench, demo lines) and exp-006
(pilot-0.4), all with the demo's thresholds.

| # | Item | Set | Jev today | Target |
|---|---|---|---|---|
| 1 | Decision right | Main test (gen-0.1 test) | 80.7% anonymous, 81.2% named, on 3,000 lines (exp-016) | ≥ Jev, and better beyond noise |
| 2 | Answers now a line meant for someone else | Duplex-MPE / main test | 0.4% (182/44,528) / 1.4% anonymous (exp-016) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test |
| 3 | Holds for a pause on a line meant for someone else | Duplex-MPE / Ambient Bench SILENT / pilot | 16.0% (7,131/44,528) / 14.6% (2,301/15,793) / 17.8% (29/163) | At most half of Jev's on each |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit `T` | 99.2% (1,983/2,000) | Not worse than Jev beyond noise |
| 5 | Answers now the same request without the name | Duplex-MPE implicit `T` | 26.6% (531/2,000) | Better beyond noise; aim for 80% |
| 6 | Line for the agent from the conversation's rhythm, no name (answers, follow-ups, sessions it leads) | pilot G6 lines / main test | 47.1% (16/34) / Phase 3 | ≥ 90% answered now |
| 7 | Name said about the agent, not to it | Duplex-MPE `N1` | Answers now 0 of 6,080, holds 13.3% (809/6,080) | Answers now ≤ 0.1%, holds ≤ half of Jev's |
| 8 | Another device addressed ("Hey Google, ...") | Duplex-MPE device lines | Answers now 3.4% (176/5,146) | ≤ 0.5% |
| 9 | An open question with nothing to settle it | `wait` lines in pilot and main test | Holds 88.5% (23/26) on pilot | Mean `respond` between 0.35 and 0.65, and ≥ 80% of these lines between 0.25 and 0.75 |
| 10 | Calibration of `respond` | Main test | `addressed` calibration error 0.073 on Duplex-MPE, 0.063 on pilot | ≤ 0.05; mean distance to graded targets ≤ 0.10 |
| 11 | Follow-up by the agent's partner against follow-up by someone else | Main test slices | Phase 3 | Decision right ≥ 90% on each |
| 12 | The daily-audience demo's own lines | `demo-lines-0.1` | 97.9% (47/48) | ≥ 46/48 |
| 13 | Anonymous against named speakers | Main test, pilot | Pilot: 77.4% anonymous against 79.6% named (exp-008, exp-006) | Gap ≤ 2 points |
| 14 | Unseen writer, settings and agent names | Held-out splits | Phase 3 | ≥ Jev on each, gap to main test ≤ 5 points |
| 15 | Real speech-to-text against clean text | STT twins | Phase 6 | Gap ≤ 3 points, and ≥ Jev |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | AMI silence test (`ami-silent-0.1.test`, 4 held-out series, 10,434 lines, SD-19) | 0.5 (5/10,434), holds 9.9% (exp-020) | ≤ Jev |
| 17 | AMI human addressee labels: lines for people kept quiet | AMI addressee test (8,875 lines) | 85.2% kept quiet: answers now 0.01%, holds 14.8% (exp-015) | ≥ Jev |
| 18 | The demo's 17 Pipecat Evals scenarios, 5 runs each, Sidechat in Jev's place | daily-audience evals | Phase 7 | Pass rate ≥ Jev's the same day |
| 19 | Speed, one line on CPU | 4 threads / 1 thread | Jev: 150 ms median over the network | p95 ≤ 30 ms / ≤ 60 ms (SQ-04) |
| 20 | Size and export | ONNX | n/a | ≤ 150 MB full precision; matches PyTorch on ≥ 99% of lines |

## What Jev tells us about the bar

Tight where the agent is named (items 4, 7) and on staying quiet outright (item 2). Wide open
where the name is missing and the rhythm of the turns decides (items 5, 6), and on holding for a
pause when the line was for someone else (item 3).
