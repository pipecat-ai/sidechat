# Scorecard 0.1: `side-r9-ettin-150m-s1`

Encoder ettin-150m, input sidechat-input-0.2. Thresholds chosen on dev: answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.4. Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. Built by `scripts/scorecard_report.py` from the run's stored scoring.

| # | Item | Sidechat | Target | |
|---|---|---|---|---|
| 1 | Decision right, main test (anonymous) | 99.0% (21,009/21,233; 98.8 to 99.1); on Jev's 2,882 lines +18.2 points (+16.8 to +19.7) | Jev 80.7% (2,327/2,882; 79.3 to 82.1) | met |
| 2 | Answers now a line for someone else | Duplex-MPE 0.2% (93/44,528; 0.2 to 0.3); main test 0.2% (24/11,573; 0.1 to 0.3) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test | met |
| 3 | Holds for a pause on a line for someone else | Duplex-MPE 0.8% (355/44,528; 0.7 to 0.9); Ambient 2.8% (447/15,793; 2.6 to 3.1); pilot 4.9% (8/163; 2.5 to 9.4) | At most half of Jev's (16.0%, 14.6%, 17.8%) | met |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit T 99.6% (1,991/2,000; 99.2 to 99.8) | Not worse than Jev (99.2%) | met |
| 5 | Answers now the same request without the name | Duplex-MPE implicit T 29.3% (587/2,000; 27.4 to 31.4) | Better than Jev (26.6%) beyond noise; aim for 80% | met (aim of 80% not met) |
| 6 | Line for the agent from the rhythm, no name | pilot G6 lines 67.7% (23/34; 50.8 to 80.9); main test G6 97.9% (2,957/3,021; 97.3 to 98.3) | ≥ 90% answered now | **not met** |
| 7 | Name said about the agent, not to it | Duplex-MPE N1: answers now 0.6% (38/6,080; 0.5 to 0.9), holds 4.2% (256/6,080; 3.7 to 4.7) | Answers now ≤ 0.1%; holds ≤ 6.7% | **not met** |
| 8 | Another device addressed | Duplex-MPE device lines: answers now 0.1% (4/5,146; 0.0 to 0.2) | ≤ 0.5% | met |
| 9 | An open question with nothing to settle it | main test: mean `respond` 0.50, 96.9% (2,565/2,648; 96.1 to 97.5) between 0.25 and 0.75; pilot: mean 0.44, 69.2% (18/26; 50.0 to 83.5) | Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75 | **not met** |
| 10 | Calibration of `respond` | main test: calibration error 0.0045, mean distance 0.0118; Duplex-MPE 0.0174; pilot 0.0646 | ≤ 0.05; mean distance ≤ 0.10 | met |
| 11 | Follow-up by the partner against by someone else | main test: partner 99.4% (799/804; 98.6 to 99.7); someone else 97.3% (430/442; 95.3 to 98.4) | ≥ 90% each | met |
| 12 | The demo's own lines | 48/48 | ≥ 46/48 | met |
| 13 | Anonymous against named speakers | main test 99.0% against 98.9%; pilot 87.8% against 87.8% | Gap ≤ 2 points | met |
| 14 | Unseen writer, settings and agent names | weakest held-out slice `setting,agent_name,writer` 97.9% (378/386; 96.0 to 99.0) (Jev 81.7%); nothing held out 99.1% | ≥ Jev on each, gap to main test ≤ 5 points | met |
| 15 | Real speech-to-text against clean text | not built yet | Gap ≤ 3 points, ≥ Jev | n/a |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | 0.0 (0/10,434); holds 0.5% (57/10,434; 0.4 to 0.7) | ≤ Jev (0.5) | met |

12 of 16 items met. Not met: 6, 7, 9. Item 15 is not built.
