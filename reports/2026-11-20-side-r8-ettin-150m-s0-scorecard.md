# Scorecard 0.1: `side-r8-ettin-150m-s0`

Encoder ettin-150m, input sidechat-input-0.2. Thresholds chosen on dev: answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.4. Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. Built by `scripts/scorecard_report.py` from the run's stored scoring.

| # | Item | Sidechat | Target | |
|---|---|---|---|---|
| 1 | Decision right, main test (anonymous) | 99.0% (21,022/21,233; 98.9 to 99.1); on Jev's 2,882 lines +18.2 points (+16.8 to +19.7) | Jev 80.7% (2,327/2,882; 79.3 to 82.1) | met |
| 2 | Answers now a line for someone else | Duplex-MPE 0.4% (177/44,528; 0.3 to 0.5); main test 0.2% (25/11,573; 0.1 to 0.3) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test | met |
| 3 | Holds for a pause on a line for someone else | Duplex-MPE 1.1% (493/44,528; 1.0 to 1.2); Ambient 2.8% (444/15,793; 2.6 to 3.1); pilot 3.7% (6/163; 1.7 to 7.8) | At most half of Jev's (16.0%, 14.6%, 17.8%) | met |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit T 99.7% (1,993/2,000; 99.3 to 99.8) | Not worse than Jev (99.2%) | met |
| 5 | Answers now the same request without the name | Duplex-MPE implicit T 46.5% (929/2,000; 44.3 to 48.6) | Better than Jev (26.6%) beyond noise; aim for 80% | met (aim of 80% not met) |
| 6 | Line for the agent from the rhythm, no name | pilot G6 lines 67.7% (23/34; 50.8 to 80.9); main test G6 98.3% (2,969/3,021; 97.8 to 98.7) | ≥ 90% answered now | **not met** |
| 7 | Name said about the agent, not to it | Duplex-MPE N1: answers now 0.4% (25/6,080; 0.3 to 0.6), holds 4.9% (300/6,080; 4.4 to 5.5) | Answers now ≤ 0.1%; holds ≤ 6.7% | **not met** |
| 8 | Another device addressed | Duplex-MPE device lines: answers now 0.0% (0/5,146; 0.0 to 0.1) | ≤ 0.5% | met |
| 9 | An open question with nothing to settle it | main test: mean `respond` 0.50, 96.8% (2,562/2,648; 96.0 to 97.4) between 0.25 and 0.75; pilot: mean 0.45, 76.9% (20/26; 58.0 to 89.0) | Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75 | **not met** |
| 10 | Calibration of `respond` | main test: calibration error 0.0039, mean distance 0.0119; Duplex-MPE 0.0108; pilot 0.0553 | ≤ 0.05; mean distance ≤ 0.10 | met |
| 11 | Follow-up by the partner against by someone else | main test: partner 99.4% (799/804; 98.6 to 99.7); someone else 96.2% (425/442; 93.9 to 97.6) | ≥ 90% each | met |
| 12 | The demo's own lines | 47/48 | ≥ 46/48 | met |
| 13 | Anonymous against named speakers | main test 99.0% against 99.0%; pilot 87.8% against 87.8% | Gap ≤ 2 points | met |
| 14 | Unseen writer, settings and agent names | weakest held-out slice `setting,agent_name,writer` 98.5% (380/386; 96.7 to 99.3) (Jev 81.7%); nothing held out 99.1% | ≥ Jev on each, gap to main test ≤ 5 points | met |
| 15 | Real speech-to-text against clean text | not built yet | Gap ≤ 3 points, ≥ Jev | n/a |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | 0.0 (0/10,434); holds 0.7% (68/10,434; 0.5 to 0.8) | ≤ Jev (0.5) | met |

12 of 16 items met. Not met: 6, 7, 9. Item 15 is not built.
