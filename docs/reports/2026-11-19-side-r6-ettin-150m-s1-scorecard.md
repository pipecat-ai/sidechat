# Scorecard 0.1: `side-r6-ettin-150m-s1`

Encoder ettin-150m, input sidechat-input-0.2. Thresholds chosen on dev: answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.4. Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. Built by `scripts/scorecard_report.py` from the run's stored scoring.

| # | Item | Sidechat | Target | |
|---|---|---|---|---|
| 1 | Decision right, main test (anonymous) | 99.1% (21,033/21,233; 98.9 to 99.2); on Jev's 2,882 lines +18.1 points (+16.7 to +19.6) | Jev 80.7% (2,327/2,882; 79.3 to 82.1) | met |
| 2 | Answers now a line for someone else | Duplex-MPE 0.2% (91/44,528; 0.2 to 0.2); main test 0.1% (14/11,573; 0.1 to 0.2) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test | met |
| 3 | Holds for a pause on a line for someone else | Duplex-MPE 1.2% (521/44,528; 1.1 to 1.3); Ambient 1.3% (207/15,793; 1.1 to 1.5); pilot 4.9% (8/163; 2.5 to 9.4) | At most half of Jev's (16.0%, 14.6%, 17.8%) | met |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit T 99.4% (1,987/2,000; 98.9 to 99.6) | Not worse than Jev (99.2%) | met |
| 5 | Answers now the same request without the name | Duplex-MPE implicit T 22.8% (456/2,000; 21.0 to 24.7) | Better than Jev (26.6%) beyond noise; aim for 80% | **not met** (aim of 80% not met) |
| 6 | Line for the agent from the rhythm, no name | pilot G6 lines 70.6% (24/34; 53.8 to 83.2); main test G6 98.1% (2,963/3,021; 97.5 to 98.5) | ≥ 90% answered now | **not met** |
| 7 | Name said about the agent, not to it | Duplex-MPE N1: answers now 0.4% (21/6,080; 0.2 to 0.5), holds 6.5% (392/6,080; 5.9 to 7.1) | Answers now ≤ 0.1%; holds ≤ 6.7% | **not met** |
| 8 | Another device addressed | Duplex-MPE device lines: answers now 0.0% (0/5,146; 0.0 to 0.1) | ≤ 0.5% | met |
| 9 | An open question with nothing to settle it | main test: mean `respond` 0.50, 97.3% (2,577/2,648; 96.6 to 97.9) between 0.25 and 0.75; pilot: mean 0.44, 80.8% (21/26; 62.1 to 91.5) | Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75 | met |
| 10 | Calibration of `respond` | main test: calibration error 0.0036, mean distance 0.011; Duplex-MPE 0.0211; pilot 0.0428 | ≤ 0.05; mean distance ≤ 0.10 | met |
| 11 | Follow-up by the partner against by someone else | main test: partner 99.6% (801/804; 98.9 to 99.9); someone else 97.5% (431/442; 95.6 to 98.6) | ≥ 90% each | met |
| 12 | The demo's own lines | 47/48 | ≥ 46/48 | met |
| 13 | Anonymous against named speakers | main test 99.1% against 99.1%; pilot 89.3% against 89.3% | Gap ≤ 2 points | met |
| 14 | Unseen writer, settings and agent names | weakest held-out slice `setting` 98.6% (278/282; 96.4 to 99.5) (Jev 78.8%); nothing held out 99.2% | ≥ Jev on each, gap to main test ≤ 5 points | met |
| 15 | Real speech-to-text against clean text | not built yet | Gap ≤ 3 points, ≥ Jev | n/a |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | 0.0 (0/10,434); holds 0.1% (8/10,434; 0.0 to 0.1) | ≤ Jev (0.5) | met |

12 of 16 items met. Not met: 5, 6, 7. Item 15 is not built.
