# Scorecard 0.1: `side-r9tt-ettin-32m-s0`

Encoder ettin-32m, input sidechat-tt-0.1. Thresholds chosen on dev: answer now at `respond` ≥ 0.55, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.7. Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. Built by `scripts/scorecard_report.py` from the run's stored scoring.

| # | Item | Sidechat | Target | |
|---|---|---|---|---|
| 1 | Decision right, main test (anonymous) | 98.6% (20,942/21,233; 98.5 to 98.8); on Jev's 2,882 lines +17.9 points (+16.5 to +19.4) | Jev 80.7% (2,327/2,882; 79.3 to 82.1) | met |
| 2 | Answers now a line for someone else | Duplex-MPE 0.3% (115/44,528; 0.2 to 0.3); main test 0.2% (19/11,573; 0.1 to 0.3) | ≤ 0.4% on Duplex-MPE, ≤ 1% on main test | met |
| 3 | Holds for a pause on a line for someone else | Duplex-MPE 0.7% (288/44,528; 0.6 to 0.7); Ambient 2.2% (342/15,793; 1.9 to 2.4); pilot 4.9% (8/163; 2.5 to 9.4) | At most half of Jev's (16.0%, 14.6%, 17.8%) | met |
| 4 | Answers now a request that names the agent | Duplex-MPE explicit T 96.5% (1,930/2,000; 95.6 to 97.2) | Not worse than Jev (99.2%) | **not met** |
| 5 | Answers now the same request without the name | Duplex-MPE implicit T 6.5% (129/2,000; 5.5 to 7.6) | Better than Jev (26.6%) beyond noise; aim for 80% | **not met** (aim of 80% not met) |
| 6 | Line for the agent from the rhythm, no name | pilot G6 lines 73.5% (25/34; 56.9 to 85.4); main test G6 98.3% (2,970/3,021; 97.8 to 98.7) | ≥ 90% answered now | **not met** |
| 7 | Name said about the agent, not to it | Duplex-MPE N1: answers now 1.2% (71/6,080; 0.9 to 1.5), holds 4.0% (240/6,080; 3.5 to 4.5) | Answers now ≤ 0.1%; holds ≤ 6.7% | **not met** |
| 8 | Another device addressed | Duplex-MPE device lines: answers now 0.1% (4/5,146; 0.0 to 0.2) | ≤ 0.5% | met |
| 9 | An open question with nothing to settle it | main test: mean `respond` 0.50, 96.2% (2,547/2,648; 95.4 to 96.9) between 0.25 and 0.75; pilot: mean 0.44, 76.9% (20/26; 58.0 to 89.0) | Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75 | **not met** |
| 10 | Calibration of `respond` | main test: calibration error 0.0038, mean distance 0.0137; Duplex-MPE 0.0287; pilot 0.0498 | ≤ 0.05; mean distance ≤ 0.10 | met |
| 11 | Follow-up by the partner against by someone else | main test: partner 99.8% (802/804; 99.1 to 99.9); someone else 92.3% (408/442; 89.4 to 94.4) | ≥ 90% each | met |
| 12 | The demo's own lines | 47/48 | ≥ 46/48 | met |
| 13 | Anonymous against named speakers | main test 98.6% against 98.6%; pilot 87.4% against 87.4% | Gap ≤ 2 points | met |
| 14 | Unseen writer, settings and agent names | weakest held-out slice `setting,agent_name,writer` 97.7% (377/386; 95.6 to 98.8) (Jev 81.7%); nothing held out 98.9% | ≥ Jev on each, gap to main test ≤ 5 points | met |
| 15 | Real speech-to-text against clean text | not built yet | Gap ≤ 3 points, ≥ Jev | n/a |
| 16 | AMI meetings with a silent agent: answers per 1,000 lines | 0.0 (0/10,434); holds 0.5% (52/10,434; 0.4 to 0.7) | ≤ Jev (0.5) | met |

10 of 16 items met. Not met: 4, 5, 6, 7, 9. Item 15 is not built.
