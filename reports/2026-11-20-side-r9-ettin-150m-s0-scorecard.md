# Scorecard 0.1: `side-r9-ettin-150m-s0`

Encoder ettin-150m, input sidechat-input-0.2. Thresholds chosen on dev: answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.3. Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. Built by `scripts/scorecard_report.py` from the run's stored scoring.

| # | Item | Sidechat | Target | |
|---|---|---|---|---|
| 1 | Decision right, main test (anonymous) | 99.0% (21,011/21,233; 98.8 to 99.1); on Jev's 2,882 lines +18.2 points (+16.7 to +19.7) | Jev 80.7% (2,327/2,882; 79.3 to 82.1) | met |
| 2 | Answers now a line for someone else | Duplex-MPE 0.2% (73/44,528; 0.1 to 0.2); main test 0.2% (29/11,573; 0.2 to 0.4) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test | met |
| 3 | Holds for a pause on a line for someone else | Duplex-MPE 0.8% (346/44,528; 0.7 to 0.9); Ambient 2.8% (434/15,793; 2.5 to 3.0); pilot 4.9% (8/163; 2.5 to 9.4) | At most half of Jev's (16.0%, 14.6%, 17.8%) | met |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit T 99.7% (1,993/2,000; 99.3 to 99.8) | Not worse than Jev (99.2%) | met |
| 5 | Answers now the same request without the name | Duplex-MPE implicit T 26.6% (532/2,000; 24.7 to 28.6) | Better than Jev (26.6%) beyond noise; aim for 80% | **not met** (aim of 80% not met) |
| 6 | Line for the agent from the rhythm, no name | pilot G6 lines 61.8% (21/34; 45.0 to 76.1); main test G6 98.1% (2,963/3,021; 97.5 to 98.5) | ≥ 90% answered now | **not met** |
| 7 | Name said about the agent, not to it | Duplex-MPE N1: answers now 0.3% (20/6,080; 0.2 to 0.5), holds 4.5% (273/6,080; 4.0 to 5.0) | Answers now ≤ 0.1%; holds ≤ 6.7% | **not met** |
| 8 | Another device addressed | Duplex-MPE device lines: answers now 0.0% (2/5,146; 0.0 to 0.1) | ≤ 0.5% | met |
| 9 | An open question with nothing to settle it | main test: mean `respond` 0.50, 96.9% (2,566/2,648; 96.2 to 97.5) between 0.25 and 0.75; pilot: mean 0.42, 69.2% (18/26; 50.0 to 83.5) | Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75 | **not met** |
| 10 | Calibration of `respond` | main test: calibration error 0.0048, mean distance 0.0123; Duplex-MPE 0.018; pilot 0.0574 | ≤ 0.05; mean distance ≤ 0.10 | met |
| 11 | Follow-up by the partner against by someone else | main test: partner 99.9% (803/804; 99.3 to 100.0); someone else 96.8% (428/442; 94.8 to 98.1) | ≥ 90% each | met |
| 12 | The demo's own lines | 47/48 | ≥ 46/48 | met |
| 13 | Anonymous against named speakers | main test 99.0% against 99.0%; pilot 86.7% against 86.7% | Gap ≤ 2 points | met |
| 14 | Unseen writer, settings and agent names | weakest held-out slice `setting,agent_name,writer` 97.9% (378/386; 96.0 to 99.0) (Jev 81.7%); nothing held out 99.1% | ≥ Jev on each, gap to main test ≤ 5 points | met |
| 15 | Real speech-to-text against clean text | not built yet | Gap ≤ 3 points, ≥ Jev | n/a |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | 0.0 (0/10,434); holds 0.9% (89/10,434; 0.7 to 1.1) | ≤ Jev (0.5) | met |

11 of 16 items met. Not met: 5, 6, 7, 9. Item 15 is not built.
