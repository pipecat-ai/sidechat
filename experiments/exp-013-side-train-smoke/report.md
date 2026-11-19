# Training run: exp-013-side-train-smoke

Every number below is measured in this run. A share is `value (k/n)`; headline shares also give a 95% interval.

## ettin-32m

Run `side-smoke-ettin-32m-s0`. Best epoch 1 of 1; history [{'epoch': 1, 'train_loss': 1.8176, 'dev_loss': 1.2168, 'secs': 14}]. Temperatures {'intent': 0.85, 'respond': 0.95, 'unclear': 1.2}. 3000 training rows, 656 dev rows, 22 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.55 or `intent.open` ≥ 0.5 (519/633 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 78.0% (1086/1392; 75.8 to 80.1) | 3.8% (29/766) | 1.0% (8/766) | 68.4% (321/469) | 26.4% (124/469) | 0.53 (n=157) |
| generated test @named | Sidechat | 78.4% (1091/1392; 76.1 to 80.5) | 3.8% (29/766) | 1.2% (9/766) | 69.5% (326/469) | 25.6% (120/469) | 0.53 (n=157) |
| generated test @none | Sidechat | 76.4% (1063/1392; 74.1 to 78.5) | 4.8% (37/766) | 1.7% (13/766) | 67.0% (314/469) | 27.1% (127/469) | 0.55 (n=157) |
| pilot-0.4 | Sidechat | 74.0% (196/265; 68.4 to 78.9) | 15.3% (25/163) | 3.7% (6/163) | 77.6% (59/76) | 19.7% (15/76) | 0.50 (n=26) |
|  | Jev | 79.6% (211/265; 74.4 to 84.0) | 1.8% (3/163) | 17.8% (29/163) | 75.0% (57/76) | 13.2% (10/76) |  |
| pilot-0.4@anonymous | Sidechat | 73.6% (195/265; 68.0 to 78.5) | 15.3% (25/163) | 3.7% (6/163) | 76.3% (58/76) | 21.1% (16/76) | 0.49 (n=26) |
|  | Jev | 77.4% (205/265; 72.0 to 82.0) | 1.8% (3/163) | 18.4% (30/163) | 68.4% (52/76) | 13.2% (10/76) |  |
| demo-lines-0.1 | Sidechat | 89.6% (43/48; 77.8 to 95.5) | 3.9% (1/26) | 3.9% (1/26) | 89.5% (17/19) | 10.5% (2/19) | 0.66 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 93.3% (48837/52336; 93.1 to 93.5) | 2.5% (1095/44528) | 0.9% (403/44528) | 74.4% (5807/7808) | 22.0% (1720/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 94.7% (14963/15793; 94.4 to 95.1) | 3.2% (512/15793) | 2.0% (318/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- pilot-0.4: -5.7 (-11.7 to +0.4), within noise on 265 lines
- pilot-0.4@anonymous: -3.8 (-10.0 to +2.4), within noise on 265 lines
- demo-lines-0.1: -8.3 (-18.1 to +1.4), within noise on 48 lines
- duplex-mpe-0.1: +10.2 (+9.8 to +10.6), better on 52336 lines
- ambient-bench-0.1: +9.4 (+8.8 to +10.0), better on 15793 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0321, mean distance to target 0.2068, AUROC 0.9202
- generated test @named: calibration error 0.0292, mean distance to target 0.2064, AUROC 0.9207
- generated test @none: calibration error 0.0264, mean distance to target 0.2168, AUROC 0.9057
- pilot-0.4: calibration error 0.0716, mean distance to target 0.2524, AUROC 0.8772
- pilot-0.4@anonymous: calibration error 0.0679, mean distance to target 0.252, AUROC 0.8766
- demo-lines-0.1: calibration error 0.0842, mean distance to target 0.1443, AUROC 0.9673
- duplex-mpe-0.1: calibration error 0.0975, mean distance to target 0.17, AUROC 0.9536
- ambient-bench-0.1: calibration error 0.14, mean distance to target 0.1726

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 76.3% (609/798) | 4.1% (18/439) | 66.0% (171/259) |
| `o` | 79.4% (250/315) | 3.2% (6/185) | 67.7% (63/93) |
| `a` | 85.3% (128/150) | 3.6% (3/84) | 82.1% (46/56) |
| `c` | 76.7% (99/129) | 3.5% (2/58) | 67.2% (41/61) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `writer` | 77.1% (354/459) | 3.9% (10/254) | 71.0% (103/145) |
| `none` | 81.1% (296/365) | 3.6% (7/195) | 73.2% (101/138) |
| `agent_name,writer` | 75.2% (203/270) | 4.7% (7/150) | 58.2% (53/91) |
| `agent_name` | 81.5% (154/189) | 2.7% (3/111) | 75.4% (43/57) |
| `setting,writer` | 73.7% (42/57) | 3.2% (1/31) | 58.8% (10/17) |
| `setting` | 67.5% (27/40) | 4.8% (1/21) | 40.0% (6/15) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 88.0% (493/560) | 1.9% (9/472) | n/a |
| `G6` | 48.6% (143/294) | 0.0% (0/21) | 56.6% (120/212) |
| `G2` | 82.6% (200/242) | 21.4% (3/14) | 82.9% (189/228) |
| `G4` | 76.3% (87/114) | 2.6% (2/77) | 41.4% (12/29) |
| `G3` | 91.3% (126/138) | 6.5% (9/138) | n/a |
| `G1` | 72.7% (16/22) | 22.7% (5/22) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 96.0% (13491/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 95.8% (13450/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 96.3% (3146/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 96.5% (3151/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 99.7% (3032/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 99.6% (3028/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 78.8% (1575/2000) | 99.2% (1983/2000) | 78.8% (1575/2000) | 99.2% (1983/2000) |
| `implicit/T` | 34.2% (684/2000) | 26.6% (531/2000) | 34.2% (684/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 93.4% (1779/1904) | 98.8% (1882/1904) | 93.4% (1779/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 97.6% (1865/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 92.9% (1769/1904) | 99.0% (1884/1904) | 92.9% (1769/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 97.7% (1867/1911) | 99.5% (1902/1911) | n/a | n/a |
