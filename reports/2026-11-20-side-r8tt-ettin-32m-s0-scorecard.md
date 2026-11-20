# Scorecard 0.1: `side-r8tt-ettin-32m-s0`

Encoder ettin-32m, input sidechat-tt-0.1. Thresholds chosen on dev: answer now at `respond` ≥ 0.55, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.4. Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. Built by `scripts/scorecard_report.py` from the run's stored scoring.

| # | Item | Sidechat | Target | |
|---|---|---|---|---|
| 1 | Decision right, main test (anonymous) | 98.6% (20,932/21,233; 98.4 to 98.7); on Jev's 2,882 lines +17.7 points (+16.2 to +19.1) | Jev 80.7% (2,327/2,882; 79.3 to 82.1) | met |
| 2 | Answers now a line for someone else | Duplex-MPE 0.4% (177/44,528; 0.3 to 0.5); main test 0.2% (24/11,573; 0.1 to 0.3) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test | met |
| 3 | Holds for a pause on a line for someone else | Duplex-MPE 0.8% (370/44,528; 0.8 to 0.9); Ambient 2.4% (377/15,793; 2.2 to 2.6); pilot 5.5% (9/163; 2.9 to 10.2) | At most half of Jev's (16.0%, 14.6%, 17.8%) | met |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit T 99.2% (1,984/2,000; 98.7 to 99.5) | Not worse than Jev (99.2%) | met |
| 5 | Answers now the same request without the name | Duplex-MPE implicit T 11.5% (230/2,000; 10.2 to 13.0) | Better than Jev (26.6%) beyond noise; aim for 80% | **not met** (aim of 80% not met) |
| 6 | Line for the agent from the rhythm, no name | pilot G6 lines 61.8% (21/34; 45.0 to 76.1); main test G6 97.8% (2,955/3,021; 97.2 to 98.3) | ≥ 90% answered now | **not met** |
| 7 | Name said about the agent, not to it | Duplex-MPE N1: answers now 0.5% (29/6,080; 0.3 to 0.7), holds 4.7% (285/6,080; 4.2 to 5.2) | Answers now ≤ 0.1%; holds ≤ 6.7% | **not met** |
| 8 | Another device addressed | Duplex-MPE device lines: answers now 0.1% (4/5,146; 0.0 to 0.2) | ≤ 0.5% | met |
| 9 | An open question with nothing to settle it | main test: mean `respond` 0.50, 95.7% (2,533/2,648; 94.8 to 96.4) between 0.25 and 0.75; pilot: mean 0.44, 61.5% (16/26; 42.5 to 77.6) | Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75 | **not met** |
| 10 | Calibration of `respond` | main test: calibration error 0.0052, mean distance 0.0125; Duplex-MPE 0.028; pilot 0.0534 | ≤ 0.05; mean distance ≤ 0.10 | met |
| 11 | Follow-up by the partner against by someone else | main test: partner 99.9% (803/804; 99.3 to 100.0); someone else 92.3% (408/442; 89.4 to 94.4) | ≥ 90% each | met |
| 12 | The demo's own lines | 48/48 | ≥ 46/48 | met |
| 13 | Anonymous against named speakers | main test 98.6% against 98.6%; pilot 85.6% against 85.9% | Gap ≤ 2 points | met |
| 14 | Unseen writer, settings and agent names | weakest held-out slice `setting,agent_name,writer` 97.4% (376/386; 95.3 to 98.6) (Jev 81.7%); nothing held out 98.8% | ≥ Jev on each, gap to main test ≤ 5 points | met |
| 15 | Real speech-to-text against clean text | not built yet | Gap ≤ 3 points, ≥ Jev | n/a |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | 0.0 (0/10,434); holds 1.3% (131/10,434; 1.1 to 1.5) | ≤ Jev (0.5) | met |

11 of 16 items met. Not met: 5, 6, 7, 9. Item 15 is not built.
