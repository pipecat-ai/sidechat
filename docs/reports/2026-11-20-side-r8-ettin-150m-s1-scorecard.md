# Scorecard 0.1: `side-r8-ettin-150m-s1`

Encoder ettin-150m, input sidechat-input-0.2. Thresholds chosen on dev: answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.3. Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. Built by `scripts/scorecard_report.py` from the run's stored scoring.

| # | Item | Sidechat | Target | |
|---|---|---|---|---|
| 1 | Decision right, main test (anonymous) | 99.0% (21,013/21,233; 98.8 to 99.1); on Jev's 2,882 lines +18.1 points (+16.6 to +19.6) | Jev 80.7% (2,327/2,882; 79.3 to 82.1) | met |
| 2 | Answers now a line for someone else | Duplex-MPE 0.6% (249/44,528; 0.5 to 0.6); main test 0.3% (30/11,573; 0.2 to 0.4) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test | **not met** |
| 3 | Holds for a pause on a line for someone else | Duplex-MPE 1.0% (448/44,528; 0.9 to 1.1); Ambient 2.6% (414/15,793; 2.4 to 2.9); pilot 4.3% (7/163; 2.1 to 8.6) | At most half of Jev's (16.0%, 14.6%, 17.8%) | met |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit T 99.6% (1,992/2,000; 99.2 to 99.8) | Not worse than Jev (99.2%) | met |
| 5 | Answers now the same request without the name | Duplex-MPE implicit T 39.1% (781/2,000; 36.9 to 41.2) | Better than Jev (26.6%) beyond noise; aim for 80% | met (aim of 80% not met) |
| 6 | Line for the agent from the rhythm, no name | pilot G6 lines 67.7% (23/34; 50.8 to 80.9); main test G6 98.2% (2,968/3,021; 97.7 to 98.7) | ≥ 90% answered now | **not met** |
| 7 | Name said about the agent, not to it | Duplex-MPE N1: answers now 0.4% (25/6,080; 0.3 to 0.6), holds 5.3% (320/6,080; 4.7 to 5.9) | Answers now ≤ 0.1%; holds ≤ 6.7% | **not met** |
| 8 | Another device addressed | Duplex-MPE device lines: answers now 0.1% (7/5,146; 0.1 to 0.3) | ≤ 0.5% | met |
| 9 | An open question with nothing to settle it | main test: mean `respond` 0.50, 96.9% (2,567/2,648; 96.2 to 97.5) between 0.25 and 0.75; pilot: mean 0.42, 73.1% (19/26; 53.9 to 86.3) | Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75 | **not met** |
| 10 | Calibration of `respond` | main test: calibration error 0.0041, mean distance 0.0108; Duplex-MPE 0.0138; pilot 0.0503 | ≤ 0.05; mean distance ≤ 0.10 | met |
| 11 | Follow-up by the partner against by someone else | main test: partner 99.6% (801/804; 98.9 to 99.9); someone else 96.6% (427/442; 94.5 to 97.9) | ≥ 90% each | met |
| 12 | The demo's own lines | 46/48 | ≥ 46/48 | met |
| 13 | Anonymous against named speakers | main test 99.0% against 99.0%; pilot 87.4% against 87.4% | Gap ≤ 2 points | met |
| 14 | Unseen writer, settings and agent names | weakest held-out slice `setting,agent_name` 98.4% (184/187; 95.4 to 99.5) (Jev 89.3%); nothing held out 99.2% | ≥ Jev on each, gap to main test ≤ 5 points | met |
| 15 | Real speech-to-text against clean text | not built yet | Gap ≤ 3 points, ≥ Jev | n/a |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | 0.1 (1/10,434); holds 1.2% (125/10,434; 1.0 to 1.4) | ≤ Jev (0.5) | met |

11 of 16 items met. Not met: 2, 6, 7, 9. Item 15 is not built.
