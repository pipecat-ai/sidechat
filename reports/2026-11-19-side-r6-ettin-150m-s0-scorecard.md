# Scorecard 0.1: `side-r6-ettin-150m-s0`

Encoder ettin-150m, input sidechat-input-0.2. Thresholds chosen on dev: answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.3. Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. Built by `scripts/scorecard_report.py` from the run's stored scoring.

| # | Item | Sidechat | Target | |
|---|---|---|---|---|
| 1 | Decision right, main test (anonymous) | 99.1% (21,034/21,233; 98.9 to 99.2); on Jev's 2,882 lines +18.4 points (+16.9 to +19.8) | Jev 80.7% (2,327/2,882; 79.3 to 82.1) | met |
| 2 | Answers now a line for someone else | Duplex-MPE 0.4% (199/44,528; 0.4 to 0.5); main test 0.2% (23/11,573; 0.1 to 0.3) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test | **not met** |
| 3 | Holds for a pause on a line for someone else | Duplex-MPE 1.1% (501/44,528; 1.0 to 1.2); Ambient 1.4% (215/15,793; 1.2 to 1.6); pilot 3.7% (6/163; 1.7 to 7.8) | At most half of Jev's (16.0%, 14.6%, 17.8%) | met |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit T 99.4% (1,987/2,000; 98.9 to 99.6) | Not worse than Jev (99.2%) | met |
| 5 | Answers now the same request without the name | Duplex-MPE implicit T 37.4% (748/2,000; 35.3 to 39.5) | Better than Jev (26.6%) beyond noise; aim for 80% | met (aim of 80% not met) |
| 6 | Line for the agent from the rhythm, no name | pilot G6 lines 73.5% (25/34; 56.9 to 85.4); main test G6 98.4% (2,972/3,021; 97.9 to 98.8) | ≥ 90% answered now | **not met** |
| 7 | Name said about the agent, not to it | Duplex-MPE N1: answers now 0.5% (33/6,080; 0.4 to 0.8), holds 5.7% (349/6,080; 5.2 to 6.3) | Answers now ≤ 0.1%; holds ≤ 6.7% | **not met** |
| 8 | Another device addressed | Duplex-MPE device lines: answers now 0.0% (2/5,146; 0.0 to 0.1) | ≤ 0.5% | met |
| 9 | An open question with nothing to settle it | main test: mean `respond` 0.50, 97.2% (2,575/2,648; 96.5 to 97.8) between 0.25 and 0.75; pilot: mean 0.41, 65.4% (17/26; 46.2 to 80.6) | Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75 | **not met** |
| 10 | Calibration of `respond` | main test: calibration error 0.0042, mean distance 0.0104; Duplex-MPE 0.0169; pilot 0.0586 | ≤ 0.05; mean distance ≤ 0.10 | met |
| 11 | Follow-up by the partner against by someone else | main test: partner 99.6% (801/804; 98.9 to 99.9); someone else 96.4% (426/442; 94.2 to 97.8) | ≥ 90% each | met |
| 12 | The demo's own lines | 47/48 | ≥ 46/48 | met |
| 13 | Anonymous against named speakers | main test 99.1% against 99.1%; pilot 87.8% against 87.8% | Gap ≤ 2 points | met |
| 14 | Unseen writer, settings and agent names | weakest held-out slice `setting,agent_name,writer` 97.7% (377/386; 95.6 to 98.8) (Jev 81.7%); nothing held out 99.2% | ≥ Jev on each, gap to main test ≤ 5 points | met |
| 15 | Real speech-to-text against clean text | not built yet | Gap ≤ 3 points, ≥ Jev | n/a |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | 0.0 (0/10,434); holds 0.1% (5/10,434; 0.0 to 0.1) | ≤ Jev (0.5) | met |

11 of 16 items met. Not met: 2, 6, 7, 9. Item 15 is not built.
