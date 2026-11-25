# Scorecard 0.1: `side-r8tt-ettin-32m-s1`

Encoder ettin-32m, input sidechat-tt-0.1. Thresholds chosen on dev: answer now at `respond` ≥ 0.55, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.4. Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. Built by `scripts/scorecard_report.py` from the run's stored scoring.

| # | Item | Sidechat | Target | |
|---|---|---|---|---|
| 1 | Decision right, main test (anonymous) | 98.6% (20,938/21,233; 98.4 to 98.8); on Jev's 2,882 lines +17.7 points (+16.2 to +19.2) | Jev 80.7% (2,327/2,882; 79.3 to 82.1) | met |
| 2 | Answers now a line for someone else | Duplex-MPE 0.2% (98/44,528; 0.2 to 0.3); main test 0.3% (31/11,573; 0.2 to 0.4) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test | met |
| 3 | Holds for a pause on a line for someone else | Duplex-MPE 0.5% (231/44,528; 0.5 to 0.6); Ambient 2.8% (443/15,793; 2.6 to 3.1); pilot 4.9% (8/163; 2.5 to 9.4) | At most half of Jev's (16.0%, 14.6%, 17.8%) | met |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit T 96.4% (1,927/2,000; 95.4 to 97.1) | Not worse than Jev (99.2%) | **not met** |
| 5 | Answers now the same request without the name | Duplex-MPE implicit T 9.7% (194/2,000; 8.5 to 11.1) | Better than Jev (26.6%) beyond noise; aim for 80% | **not met** (aim of 80% not met) |
| 6 | Line for the agent from the rhythm, no name | pilot G6 lines 64.7% (22/34; 47.9 to 78.5); main test G6 98.2% (2,965/3,021; 97.6 to 98.6) | ≥ 90% answered now | **not met** |
| 7 | Name said about the agent, not to it | Duplex-MPE N1: answers now 0.4% (22/6,080; 0.2 to 0.5), holds 2.9% (177/6,080; 2.5 to 3.4) | Answers now ≤ 0.1%; holds ≤ 6.7% | **not met** |
| 8 | Another device addressed | Duplex-MPE device lines: answers now 0.1% (4/5,146; 0.0 to 0.2) | ≤ 0.5% | met |
| 9 | An open question with nothing to settle it | main test: mean `respond` 0.50, 96.2% (2,548/2,648; 95.4 to 96.9) between 0.25 and 0.75; pilot: mean 0.44, 61.5% (16/26; 42.5 to 77.6) | Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75 | **not met** |
| 10 | Calibration of `respond` | main test: calibration error 0.0044, mean distance 0.0129; Duplex-MPE 0.028; pilot 0.0469 | ≤ 0.05; mean distance ≤ 0.10 | met |
| 11 | Follow-up by the partner against by someone else | main test: partner 99.8% (802/804; 99.1 to 99.9); someone else 91.2% (403/442; 88.2 to 93.5) | ≥ 90% each | met |
| 12 | The demo's own lines | 47/48 | ≥ 46/48 | met |
| 13 | Anonymous against named speakers | main test 98.6% against 98.6%; pilot 86.3% against 86.3% | Gap ≤ 2 points | met |
| 14 | Unseen writer, settings and agent names | weakest held-out slice `setting,agent_name,writer` 97.7% (377/386; 95.6 to 98.8) (Jev 81.7%); nothing held out 98.9% | ≥ Jev on each, gap to main test ≤ 5 points | met |
| 15 | Real speech-to-text against clean text | not built yet | Gap ≤ 3 points, ≥ Jev | n/a |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | 0.0 (0/10,434); holds 1.4% (143/10,434; 1.2 to 1.6) | ≤ Jev (0.5) | met |

10 of 16 items met. Not met: 4, 5, 6, 7, 9. Item 15 is not built.
