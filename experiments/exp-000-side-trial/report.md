# Jev baseline: exp-000-side-trial

Generated 2026-11-18T21:36:38+00:00 by `sidechat/pipeline/baseline.py`. Every number below is measured in this run.

## What was run

- **Model:** `jev-1.13.0`, asked with the daily-audience demo's two questions and state (commit `73171de`, wording hash `476c554866d6`), through Pipecat 1.16.0's `JevClassifier`.
- **Decision rule:** the demo's. Answer now when `addressed ≥ 0.8`, hold for silence when `question ≥ 0.5`, otherwise stay quiet.
- **Requests:** 88 distinct (0 reused from earlier runs, 88 asked now, 0 failed).
- **Tokens this run:** 71,879 in, 3,256 out. About $0.003 at $0.042 per million input tokens, a price recorded in Audience's repo and not confirmed with TypeSafe.
- **Baseline id:** `trial-0`. Stored answers are reused, so later runs compare against these numbers.

A share is written `value (k/n; 95% interval)`. "For others" means lines the set marks as not for the agent.

## demo-lines-0.1

Source: `data/suites/demo-lines-0.1.yaml`. Use: test.

4 rows, 4 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 100.0% (4/4; 51.0 to 100.0) | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |
| Name said → answer | 100.0% (4/4; 51.0 to 100.0) | 100.0% (4/4) | 0.0% (0/4) | 0.0% (0/4) | n/a | n/a |

Jev latency from Modal: 79 ms at the median, 80 ms at the 95th percentile (4 answers, 12 requests at a time).

Jev's `addressed` number without a threshold: AUROC None, average precision None, calibration error 0.025 (0 lines for the agent, 4 not).

**By code** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `P` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `G` | 1 | 100.0% (1/1) | 0.0% (0/1) | 0.0% (0/1) | n/a | n/a |

**By kind** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `question_to_named_person` | 2 | 100.0% (2/2) | 0.0% (0/2) | 0.0% (0/2) | n/a | n/a |
| `statement` | 1 | 100.0% (1/1) | 0.0% (0/1) | 0.0% (0/1) | n/a | n/a |
| `reply_to_person` | 1 | 100.0% (1/1) | 0.0% (0/1) | 0.0% (0/1) | n/a | n/a |

**Lines Jev decides differently from the label** (0 of 4)

## ambient-bench-0.1

Source: `text-ai/social-ai-ambient-bench` at `5efda0b267d6`. Use: test only; the dataset forbids training on it.

22 rows, 22 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 57.9% (11/19; 36.3 to 76.9) | 57.9% (11/19) | 0.0% (0/19) | 42.1% (8/19) | n/a | n/a |
| Name said → answer | 100.0% (19/19; 83.2 to 100.0) | 100.0% (19/19) | 0.0% (0/19) | 0.0% (0/19) | n/a | n/a |

Jev latency from Modal: 63 ms at the median, 78 ms at the 95th percentile (22 answers, 12 requests at a time).

**The benchmark's own metrics.** Its policy expects the assistant to offer help nobody asked for, so a model that speaks only when spoken to misses many RESPOND lines by design.

| Reading | Scenario pass rate | Macro F1 | False interruptions | Missed interventions | Turn accuracy |
|---|---|---|---|---|---|
| strict (speaks = answers now) | 0.0% (0/3) | 0.4634 | 0.0% (0/19) | 100.0% (3/3) | 86.4% (19/22) |
| lenient (speaks = answers now or holds) | 0.0% (0/3) | 0.581 | 42.1% (8/19) | 0.0% (0/3) | 63.6% (14/22) |
| name_only | 0.0% (0/3) | 0.4634 | 0.0% (0/19) | 100.0% (3/3) | 86.4% (19/22) |
| *Claude Opus 4.6, from the benchmark's own leaderboard* | 67.4% | | 4.5% | 25.6% | 94.9% |
| *Gemini 3.1 Pro Preview, from the benchmark's own leaderboard* | 63.6% | | 3.3% | 46.7% | 95.5% |
| *GPT-5.5, from the benchmark's own leaderboard* | 63.6% | | 4.1% | 30.8% | 95.2% |

AUROC of `max(addressed, question)` against RESPOND: 0.8509.

**By bench** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `SILENT` | 19 | 57.9% (11/19) | 0.0% (0/19) | 42.1% (8/19) | n/a | n/a |
| `RESPOND` | 3 | n/a | n/a | n/a | n/a | n/a |

**By category** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `capability_request` | 22 | 57.9% (11/19) | 0.0% (0/19) | 42.1% (8/19) | n/a | n/a |

## duplex-mpe-0.1

Source: `ChengqianMa/Duplex-MPE` at `6d5f59fab123`. Use: held-out benchmark; never train on it.

80 rows, 80 scored.

| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |
|---|---|---|---|---|---|---|
| Jev, demo thresholds | 95.0% (76/80; 87.8 to 98.0) | 95.6% (65/68) | 0.0% (0/68) | 4.4% (3/68) | 91.7% (11/12) | 0.0% (0/12) |
| Name said → answer | 83.8% (67/80; 74.2 to 90.2) | 85.3% (58/68) | 14.7% (10/68) | 0.0% (0/68) | 75.0% (9/12) | 25.0% (3/12) |

Jev latency from Modal: 65 ms at the median, 87 ms at the 95th percentile (80 answers, 12 requests at a time).

Jev's `addressed` number without a threshold: AUROC 0.9951, average precision 0.9792, calibration error 0.0714 (12 lines for the agent, 68 not).

**The same request with and without the agent's name** (3 pairs): answered now 100.0% with the name, 66.7% without. Difference -33.3 points (-86.7 to +20.0).

**By condition** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `explicit` | 40 | 97.5% (39/40) | 0.0% (0/34) | 2.9% (1/34) | 100.0% (6/6) | 0.0% (0/6) |
| `implicit` | 40 | 92.5% (37/40) | 0.0% (0/34) | 5.9% (2/34) | 83.3% (5/6) | 0.0% (0/6) |

**By event** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `N2` | 40 | 97.5% (39/40) | 0.0% (0/40) | 2.5% (1/40) | n/a | n/a |
| `N1` | 12 | 100.0% (12/12) | 0.0% (0/12) | 0.0% (0/12) | n/a | n/a |
| `N3` | 10 | 80.0% (8/10) | 0.0% (0/10) | 20.0% (2/10) | n/a | n/a |
| `T` | 6 | 83.3% (5/6) | n/a | n/a | 83.3% (5/6) | 0.0% (0/6) |
| `N4_Q` | 6 | 100.0% (6/6) | n/a | n/a | 100.0% (6/6) | 0.0% (0/6) |
| `N4_R` | 6 | 100.0% (6/6) | 0.0% (0/6) | 0.0% (0/6) | n/a | n/a |

**By condition/event** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `explicit/N2` | 20 | 100.0% (20/20) | 0.0% (0/20) | 0.0% (0/20) | n/a | n/a |
| `implicit/N2` | 20 | 95.0% (19/20) | 0.0% (0/20) | 5.0% (1/20) | n/a | n/a |
| `explicit/N1` | 6 | 100.0% (6/6) | 0.0% (0/6) | 0.0% (0/6) | n/a | n/a |
| `implicit/N1` | 6 | 100.0% (6/6) | 0.0% (0/6) | 0.0% (0/6) | n/a | n/a |
| `explicit/N3` | 5 | 80.0% (4/5) | 0.0% (0/5) | 20.0% (1/5) | n/a | n/a |
| `implicit/N3` | 5 | 80.0% (4/5) | 0.0% (0/5) | 20.0% (1/5) | n/a | n/a |
| `explicit/T` | 3 | 100.0% (3/3) | n/a | n/a | 100.0% (3/3) | 0.0% (0/3) |
| `explicit/N4_Q` | 3 | 100.0% (3/3) | n/a | n/a | 100.0% (3/3) | 0.0% (0/3) |
| `explicit/N4_R` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |
| `implicit/T` | 3 | 66.7% (2/3) | n/a | n/a | 66.7% (2/3) | 0.0% (0/3) |
| `implicit/N4_Q` | 3 | 100.0% (3/3) | n/a | n/a | 100.0% (3/3) | 0.0% (0/3) |
| `implicit/N4_R` | 3 | 100.0% (3/3) | 0.0% (0/3) | 0.0% (0/3) | n/a | n/a |

**By addressee** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `other_human` | 48 | 100.0% (48/48) | 0.0% (0/48) | 0.0% (0/48) | n/a | n/a |
| `aria` | 12 | 91.7% (11/12) | n/a | n/a | 91.7% (11/12) | 0.0% (0/12) |
| `device` | 10 | 90.0% (9/10) | 0.0% (0/10) | 10.0% (1/10) | n/a | n/a |
| `none` | 10 | 80.0% (8/10) | 0.0% (0/10) | 20.0% (2/10) | n/a | n/a |

**By speech_act** (Jev, demo thresholds)

| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |
|---|---|---|---|---|---|---|
| `statement` | 38 | 100.0% (38/38) | 0.0% (0/38) | 0.0% (0/38) | n/a | n/a |
| `request` | 20 | 90.0% (18/20) | 0.0% (0/12) | 8.3% (1/12) | 87.5% (7/8) | 0.0% (0/8) |
| `question` | 12 | 100.0% (12/12) | 0.0% (0/8) | 0.0% (0/8) | 100.0% (4/4) | 0.0% (0/4) |
| `self_talk` | 10 | 80.0% (8/10) | 0.0% (0/10) | 20.0% (2/10) | n/a | n/a |

**Moving the `addressed` threshold**

| Threshold | For the agent: answers now | For others: answers now |
|---|---|---|
| 0.5 | 91.7% (11/12) | 1.5% (1/68) |
| 0.6 | 91.7% (11/12) | 1.5% (1/68) |
| 0.7 | 91.7% (11/12) | 0.0% (0/68) |
| 0.8 | 91.7% (11/12) | 0.0% (0/68) |
| 0.9 | 83.3% (10/12) | 0.0% (0/68) |
