# Training run: exp-036-side-tt-smoke

Every number below is measured in this run. A share is `value (k/n)`; headline shares also give a 95% interval.

## ettin-32m

Run `side-ttsmoke-ettin-32m-s0`. Best epoch 1 of 1; history [{'epoch': 1, 'train_loss': 1.7475, 'dev_loss': 1.0644, 'secs': 63}]. Temperatures {'intent': 0.85, 'respond': 0.95, 'unclear': 0.9}. 4000 training rows, 6000 dev rows, 89 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.85, hold at `respond` ≥ 0.6 or `intent.open` ≥ 0.3 (6216/8093 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 75.9% (15054/19824; 75.3 to 76.5) | 0.8% (90/10807) | 3.9% (418/10807) | 49.2% (3211/6526) | 21.8% (1425/6526) | 0.50 (n=2491) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 76.1% (15082/19824; 75.5 to 76.7) | 0.8% (89/10807) | 3.9% (426/10807) | 49.8% (3247/6526) | 21.3% (1393/6526) | 0.51 (n=2491) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 74.1% (14693/19824; 73.5 to 74.7) | 0.8% (82/10807) | 3.5% (379/10807) | 43.2% (2817/6526) | 26.3% (1714/6526) | 0.52 (n=2491) |
| pilot-0.4 | Sidechat | 70.4% (190/270; 64.7 to 75.5) | 3.7% (6/163) | 10.4% (17/163) | 45.7% (37/81) | 25.9% (21/81) | 0.41 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 69.6% (188/270; 63.9 to 74.8) | 3.7% (6/163) | 10.4% (17/163) | 44.4% (36/81) | 25.9% (21/81) | 0.40 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 83.3% (40/48; 70.4 to 91.3) | 0.0% (0/26) | 7.7% (2/26) | 68.4% (13/19) | 0.0% (0/19) | 0.60 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 92.7% (48530/52336; 92.5 to 93.0) | 0.1% (29/44528) | 0.5% (244/44528) | 54.8% (4275/7808) | 28.3% (2207/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 96.9% (15301/15793; 96.6 to 97.1) | 0.1% (19/15793) | 3.0% (473/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 98.0% (8696/8875; 97.7 to 98.3) | 0.1% (10/8875) | 1.9% (169/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 98.8% (10305/10434; 98.5 to 99.0) | 0.0% (4/10434) | 1.2% (125/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: -4.8 (-6.7 to -2.9), worse on 2882 lines
- generated test @named: -5.0 (-6.9 to -3.1), worse on 2882 lines
- pilot-0.4: -9.6 (-15.5 to -3.8), worse on 270 lines
- pilot-0.4@anonymous: -8.2 (-14.1 to -2.2), worse on 270 lines
- demo-lines-0.1: -14.6 (-26.1 to -3.0), worse on 48 lines
- duplex-mpe-0.1: +9.6 (+9.3 to +10.0), better on 52336 lines
- ambient-bench-0.1: +11.5 (+11.0 to +12.1), better on 15793 lines
- ami-addressee-0.1: +12.8 (+12.1 to +13.5), better on 8875 lines
- ami-silent-0.1.test: +8.7 (+8.2 to +9.3), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0178, mean distance to target 0.175, AUROC 0.9362
- generated test @named: calibration error 0.0169, mean distance to target 0.1746, AUROC 0.9366
- generated test @none: calibration error 0.021, mean distance to target 0.1892, AUROC 0.9234
- pilot-0.4: calibration error 0.0712, mean distance to target 0.2355, AUROC 0.8993
- pilot-0.4@anonymous: calibration error 0.0685, mean distance to target 0.2353, AUROC 0.899
- demo-lines-0.1: calibration error 0.0978, mean distance to target 0.1305, AUROC 0.98
- duplex-mpe-0.1: calibration error 0.0279, mean distance to target 0.0996, AUROC 0.9393
- ambient-bench-0.1: calibration error 0.0803, mean distance to target 0.1181
- ami-addressee-0.1: calibration error 0.0827, mean distance to target 0.0827
- ami-silent-0.1.test: calibration error 0.0751, mean distance to target 0.0751

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 74.9% (7087/9458) | 0.6% (33/5196) | 45.4% (1397/3075) |
| `o` | 77.7% (4176/5377) | 1.1% (33/2905) | 54.9% (981/1788) |
| `c` | 74.8% (1908/2550) | 0.8% (11/1406) | 45.2% (371/821) |
| `a` | 77.2% (1883/2439) | 1.0% (13/1300) | 54.9% (462/842) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 77.2% (6128/7941) | 1.0% (43/4314) | 52.4% (1373/2622) |
| `writer` | 75.7% (3929/5190) | 0.5% (16/2897) | 44.4% (731/1648) |
| `agent_name,writer` | 74.7% (2427/3250) | 0.6% (11/1744) | 48.9% (524/1071) |
| `agent_name` | 76.6% (1529/1996) | 1.2% (13/1075) | 55.6% (377/678) |
| `setting,writer` | 73.3% (472/644) | 0.3% (1/362) | 37.9% (83/219) |
| `setting,agent_name,writer` | 69.2% (259/374) | 2.6% (5/193) | 43.1% (59/137) |
| `setting` | 66.9% (162/242) | 0.0% (0/117) | 38.5% (40/104) |
| `setting,agent_name` | 79.1% (148/187) | 0.9% (1/105) | 51.1% (24/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 93.2% (7868/8439) | 0.2% (11/6820) | n/a |
| `G6` | 31.9% (1221/3826) | 0.0% (0/297) | 25.2% (709/2809) |
| `G2` | 72.9% (2543/3488) | 25.1% (42/167) | 74.5% (2475/3321) |
| `G4` | 71.0% (1175/1654) | 0.1% (1/1106) | 6.8% (27/396) |
| `G3` | 95.0% (1877/1976) | 0.6% (12/1976) | n/a |
| `G1` | 74.2% (164/221) | 9.0% (20/221) | n/a |
| `G5` | 90.6% (126/139) | 2.9% (4/139) | n/a |
| `G8` | 98.8% (80/81) | 0.0% (0/81) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 99.2% (13940/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 99.2% (13938/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.6% (3255/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.6% (3255/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 99.4% (3022/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 99.5% (3024/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 54.4% (1089/2000) | 99.2% (1983/2000) | 54.4% (1089/2000) | 99.2% (1983/2000) |
| `implicit/T` | 4.1% (82/2000) | 26.6% (531/2000) | 4.1% (82/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 82.1% (1564/1904) | 98.8% (1882/1904) | 82.1% (1564/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 100.0% (1911/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 80.9% (1540/1904) | 99.0% (1884/1904) | 80.9% (1540/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 100.0% (1910/1911) | 99.5% (1902/1911) | n/a | n/a |
