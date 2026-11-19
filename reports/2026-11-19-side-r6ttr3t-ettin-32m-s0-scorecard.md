# Scorecard 0.1: `side-r6ttr3t-ettin-32m-s0`

Encoder ettin-32m, input sidechat-tt-0.1. Thresholds chosen on dev: answer now at `respond` ≥ 0.55, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.7. Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. Built by `scripts/scorecard_report.py` from the run's stored scoring.

| # | Item | Sidechat | Target | |
|---|---|---|---|---|
| 1 | Decision right, main test (anonymous) | 98.5% (20,913/21,233; 98.3 to 98.7); on Jev's 2,882 lines +17.7 points (+16.2 to +19.2) | Jev 80.7% (2,327/2,882; 79.3 to 82.1) | met |
| 2 | Answers now a line for someone else | Duplex-MPE 0.3% (115/44,528; 0.2 to 0.3); main test 0.3% (30/11,573; 0.2 to 0.4) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test | met |
| 3 | Holds for a pause on a line for someone else | Duplex-MPE 0.8% (352/44,528; 0.7 to 0.9); Ambient 1.0% (154/15,793; 0.8 to 1.1); pilot 5.5% (9/163; 2.9 to 10.2) | At most half of Jev's (16.0%, 14.6%, 17.8%) | met |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit T 98.7% (1,973/2,000; 98.0 to 99.1) | Not worse than Jev (99.2%) | **not met** |
| 5 | Answers now the same request without the name | Duplex-MPE implicit T 10.7% (214/2,000; 9.4 to 12.1) | Better than Jev (26.6%) beyond noise; aim for 80% | **not met** (aim of 80% not met) |
| 6 | Line for the agent from the rhythm, no name | pilot G6 lines 67.7% (23/34; 50.8 to 80.9); main test G6 98.0% (2,961/3,021; 97.5 to 98.5) | ≥ 90% answered now | **not met** |
| 7 | Name said about the agent, not to it | Duplex-MPE N1: answers now 0.7% (42/6,080; 0.5 to 0.9), holds 4.9% (296/6,080; 4.4 to 5.4) | Answers now ≤ 0.1%; holds ≤ 6.7% | **not met** |
| 8 | Another device addressed | Duplex-MPE device lines: answers now 0.0% (0/5,146; 0.0 to 0.1) | ≤ 0.5% | met |
| 9 | An open question with nothing to settle it | main test: mean `respond` 0.50, 96.1% (2,544/2,648; 95.3 to 96.8) between 0.25 and 0.75; pilot: mean 0.42, 69.2% (18/26; 50.0 to 83.5) | Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75 | **not met** |
| 10 | Calibration of `respond` | main test: calibration error 0.0041, mean distance 0.013; Duplex-MPE 0.0273; pilot 0.055 | ≤ 0.05; mean distance ≤ 0.10 | met |
| 11 | Follow-up by the partner against by someone else | main test: partner 99.8% (802/804; 99.1 to 99.9); someone else 91.2% (403/442; 88.2 to 93.5) | ≥ 90% each | met |
| 12 | The demo's own lines | 47/48 | ≥ 46/48 | met |
| 13 | Anonymous against named speakers | main test 98.5% against 98.5%; pilot 87.4% against 87.0% | Gap ≤ 2 points | met |
| 14 | Unseen writer, settings and agent names | weakest held-out slice `setting,agent_name,writer` 97.4% (376/386; 95.3 to 98.6) (Jev 81.7%); nothing held out 98.8% | ≥ Jev on each, gap to main test ≤ 5 points | met |
| 15 | Real speech-to-text against clean text | not built yet | Gap ≤ 3 points, ≥ Jev | n/a |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | 0.0 (0/10,434); holds 0.0% (0/10,434; 0.0 to 0.0) | ≤ Jev (0.5) | met |

10 of 16 items met. Not met: 4, 5, 6, 7, 9. Item 15 is not built.
