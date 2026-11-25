# Scorecard 0.1: `side-r9tt-ettin-32m-s1`

Encoder ettin-32m, input sidechat-tt-0.1. Thresholds chosen on dev: answer now at `respond` ≥ 0.55, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.5. Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. Built by `scripts/scorecard_report.py` from the run's stored scoring.

| # | Item | Sidechat | Target | |
|---|---|---|---|---|
| 1 | Decision right, main test (anonymous) | 98.5% (20,914/21,233; 98.3 to 98.7); on Jev's 2,882 lines +17.7 points (+16.2 to +19.2) | Jev 80.7% (2,327/2,882; 79.3 to 82.1) | met |
| 2 | Answers now a line for someone else | Duplex-MPE 0.3% (146/44,528; 0.3 to 0.4); main test 0.3% (32/11,573; 0.2 to 0.4) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test | met |
| 3 | Holds for a pause on a line for someone else | Duplex-MPE 0.7% (312/44,528; 0.6 to 0.8); Ambient 2.1% (331/15,793; 1.9 to 2.3); pilot 5.5% (9/163; 2.9 to 10.2) | At most half of Jev's (16.0%, 14.6%, 17.8%) | met |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit T 99.7% (1,993/2,000; 99.3 to 99.8) | Not worse than Jev (99.2%) | met |
| 5 | Answers now the same request without the name | Duplex-MPE implicit T 10.2% (205/2,000; 9.0 to 11.7) | Better than Jev (26.6%) beyond noise; aim for 80% | **not met** (aim of 80% not met) |
| 6 | Line for the agent from the rhythm, no name | pilot G6 lines 73.5% (25/34; 56.9 to 85.4); main test G6 98.1% (2,963/3,021; 97.5 to 98.5) | ≥ 90% answered now | **not met** |
| 7 | Name said about the agent, not to it | Duplex-MPE N1: answers now 1.2% (75/6,080; 1.0 to 1.5), holds 4.1% (252/6,080; 3.7 to 4.7) | Answers now ≤ 0.1%; holds ≤ 6.7% | **not met** |
| 8 | Another device addressed | Duplex-MPE device lines: answers now 0.0% (2/5,146; 0.0 to 0.1) | ≤ 0.5% | met |
| 9 | An open question with nothing to settle it | main test: mean `respond` 0.50, 96.6% (2,559/2,648; 95.9 to 97.3) between 0.25 and 0.75; pilot: mean 0.44, 73.1% (19/26; 53.9 to 86.3) | Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75 | **not met** |
| 10 | Calibration of `respond` | main test: calibration error 0.0035, mean distance 0.014; Duplex-MPE 0.0255; pilot 0.0502 | ≤ 0.05; mean distance ≤ 0.10 | met |
| 11 | Follow-up by the partner against by someone else | main test: partner 99.4% (799/804; 98.6 to 99.7); someone else 90.5% (400/442; 87.4 to 92.9) | ≥ 90% each | met |
| 12 | The demo's own lines | 48/48 | ≥ 46/48 | met |
| 13 | Anonymous against named speakers | main test 98.5% against 98.5%; pilot 86.7% against 87.0% | Gap ≤ 2 points | met |
| 14 | Unseen writer, settings and agent names | weakest held-out slice `setting,agent_name,writer` 97.7% (377/386; 95.6 to 98.8) (Jev 81.7%); nothing held out 98.7% | ≥ Jev on each, gap to main test ≤ 5 points | met |
| 15 | Real speech-to-text against clean text | not built yet | Gap ≤ 3 points, ≥ Jev | n/a |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | 0.0 (0/10,434); holds 0.8% (82/10,434; 0.6 to 1.0) | ≤ Jev (0.5) | met |

11 of 16 items met. Not met: 5, 6, 7, 9. Item 15 is not built.
