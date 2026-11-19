# Training run: exp-017-side-train-r1

Every number below is measured in this run. A share is `value (k/n)`; headline shares also give a 95% interval.

## ettin-32m

Run `side-r1-ettin-32m-s0`. Best epoch 2 of 3; history [{'epoch': 1, 'train_loss': 0.6555, 'dev_loss': 0.3331, 'secs': 142}, {'epoch': 2, 'train_loss': 0.3576, 'dev_loss': 0.3207, 'secs': 267}, {'epoch': 3, 'train_loss': 0.2897, 'dev_loss': 0.3393, 'secs': 391}]. Temperatures {'intent': 1.3, 'respond': 1.45, 'unclear': 1.4}. 89995 training rows, 6000 dev rows, 405 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.8 (8516/8654 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 98.0% (20625/21044; 97.8 to 98.2) | 0.3% (37/11573) | 0.3% (30/11573) | 98.3% (6710/6823) | 1.1% (73/6823) | 0.50 (n=2648) |
|  | Jev | 80.7% (2308/2860; 79.2 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.5% (724/934) | 6.9% (64/934) |  |
| generated test @named | Sidechat | 98.0% (20625/21044; 97.8 to 98.2) | 0.3% (36/11573) | 0.3% (32/11573) | 98.3% (6710/6823) | 1.1% (73/6823) | 0.50 (n=2648) |
|  | Jev | 81.2% (2323/2860; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (745/934) | 6.3% (59/934) |  |
| generated test @none | Sidechat | 96.2% (20239/21044; 95.9 to 96.4) | 0.4% (42/11573) | 0.2% (28/11573) | 95.7% (6528/6823) | 1.6% (112/6823) | 0.53 (n=2648) |
| pilot-0.4 | Sidechat | 83.4% (221/265; 78.5 to 87.4) | 3.7% (6/163) | 5.5% (9/163) | 77.6% (59/76) | 15.8% (12/76) | 0.49 (n=26) |
|  | Jev | 79.6% (211/265; 74.4 to 84.0) | 1.8% (3/163) | 17.8% (29/163) | 75.0% (57/76) | 13.2% (10/76) |  |
| pilot-0.4@anonymous | Sidechat | 83.4% (221/265; 78.5 to 87.4) | 3.7% (6/163) | 5.5% (9/163) | 77.6% (59/76) | 15.8% (12/76) | 0.49 (n=26) |
|  | Jev | 77.4% (205/265; 72.0 to 82.0) | 1.8% (3/163) | 18.4% (30/163) | 68.4% (52/76) | 13.2% (10/76) |  |
| demo-lines-0.1 | Sidechat | 95.8% (46/48; 86.0 to 98.9) | 0.0% (0/26) | 0.0% (0/26) | 89.5% (17/19) | 0.0% (0/19) | 0.51 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 95.1% (49779/52336; 94.9 to 95.3) | 1.0% (434/44528) | 1.4% (634/44528) | 80.9% (6319/7808) | 16.4% (1279/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 95.6% (15093/15793; 95.2 to 95.9) | 1.9% (308/15793) | 2.5% (392/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 96.0% (8519/8875; 95.6 to 96.4) | 1.8% (162/8875) | 2.2% (194/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +17.1 (+15.6 to +18.6), better on 2860 lines
- generated test @named: +16.6 (+15.1 to +18.1), better on 2860 lines
- pilot-0.4: +3.8 (-1.8 to +9.4), within noise on 265 lines
- pilot-0.4@anonymous: +6.0 (+0.4 to +11.7), better on 265 lines
- demo-lines-0.1: -2.1 (-9.1 to +5.0), within noise on 48 lines
- duplex-mpe-0.1: +12.0 (+11.7 to +12.3), better on 52336 lines
- ambient-bench-0.1: +10.2 (+9.7 to +10.8), better on 15793 lines
- ami-addressee-0.1: +10.8 (+10.0 to +11.5), better on 8875 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0052, mean distance to target 0.0178, AUROC 0.9838
- generated test @named: calibration error 0.0053, mean distance to target 0.0177, AUROC 0.9839
- generated test @none: calibration error 0.0082, mean distance to target 0.0285, AUROC 0.9821
- pilot-0.4: calibration error 0.0617, mean distance to target 0.1137, AUROC 0.9435
- pilot-0.4@anonymous: calibration error 0.0616, mean distance to target 0.1139, AUROC 0.9433
- demo-lines-0.1: calibration error 0.0528, mean distance to target 0.0539, AUROC 0.9927
- duplex-mpe-0.1: calibration error 0.0205, mean distance to target 0.0525, AUROC 0.9703
- ambient-bench-0.1: calibration error 0.0376, mean distance to target 0.0691
- ami-addressee-0.1: calibration error 0.0459, mean distance to target 0.0459

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 97.5% (9913/10168) | 0.3% (18/5635) | 97.7% (3171/3246) |
| `o` | 98.2% (5544/5644) | 0.3% (8/3090) | 98.9% (1812/1833) |
| `c` | 98.4% (2617/2661) | 0.5% (7/1464) | 98.6% (852/864) |
| `a` | 99.2% (2551/2571) | 0.3% (4/1384) | 99.4% (875/880) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 98.6% (8126/8244) | 0.2% (11/4509) | 99.1% (2674/2698) |
| `writer` | 97.5% (5463/5603) | 0.4% (11/3151) | 97.5% (1704/1747) |
| `agent_name,writer` | 97.4% (3397/3488) | 0.3% (6/1894) | 98.0% (1108/1130) |
| `agent_name` | 98.2% (2128/2168) | 0.7% (8/1186) | 98.5% (707/718) |
| `setting,writer` | 98.1% (682/695) | 0.0% (0/393) | 97.4% (224/230) |
| `setting,agent_name,writer` | 97.1% (371/382) | 0.5% (1/197) | 97.1% (135/139) |
| `setting` | 98.9% (274/277) | 0.0% (0/138) | 98.2% (112/114) |
| `setting,agent_name` | 98.4% (184/187) | 0.0% (0/105) | 97.9% (46/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 97.9% (8810/8999) | 0.4% (30/7292) | n/a |
| `G6` | 95.2% (3923/4120) | 0.0% (0/318) | 96.8% (2923/3021) |
| `G2` | 99.6% (3544/3558) | 0.0% (0/181) | 99.6% (3364/3377) |
| `G4` | 99.2% (1753/1768) | 0.3% (4/1183) | 99.5% (423/425) |
| `G3` | 100.0% (2113/2114) | 0.1% (1/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.0% (150/153) | 1.3% (2/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 98.6% (13846/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 98.5% (13840/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.1% (3239/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.3% (3244/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 93.2% (2834/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 93.1% (2829/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 98.2% (1963/2000) | 99.2% (1983/2000) | 98.2% (1963/2000) | 99.2% (1983/2000) |
| `implicit/T` | 29.1% (582/2000) | 26.6% (531/2000) | 29.1% (582/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.2% (1889/1904) | 98.8% (1882/1904) | 99.2% (1889/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 95.2% (1819/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.0% (1885/1904) | 99.0% (1884/1904) | 99.0% (1885/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 94.7% (1809/1911) | 99.5% (1902/1911) | n/a | n/a |

## ettin-68m

Run `side-r1-ettin-68m-s0`. Best epoch 2 of 3; history [{'epoch': 1, 'train_loss': 0.6158, 'dev_loss': 0.3204, 'secs': 184}, {'epoch': 2, 'train_loss': 0.3375, 'dev_loss': 0.3098, 'secs': 349}, {'epoch': 3, 'train_loss': 0.2747, 'dev_loss': 0.3302, 'secs': 512}]. Temperatures {'intent': 1.4, 'respond': 1.45, 'unclear': 1.35}. 89995 training rows, 6000 dev rows, 533 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.8 (8549/8654 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 98.5% (20726/21044; 98.3 to 98.7) | 0.3% (33/11573) | 0.2% (29/11573) | 98.4% (6713/6823) | 1.0% (69/6823) | 0.50 (n=2648) |
|  | Jev | 80.7% (2308/2860; 79.2 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.5% (724/934) | 6.9% (64/934) |  |
| generated test @named | Sidechat | 98.5% (20724/21044; 98.3 to 98.6) | 0.3% (33/11573) | 0.3% (30/11573) | 98.4% (6712/6823) | 1.0% (68/6823) | 0.50 (n=2648) |
|  | Jev | 81.2% (2323/2860; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (745/934) | 6.3% (59/934) |  |
| generated test @none | Sidechat | 96.9% (20387/21044; 96.6 to 97.1) | 0.4% (46/11573) | 0.4% (42/11573) | 96.6% (6591/6823) | 1.1% (74/6823) | 0.52 (n=2648) |
| pilot-0.4 | Sidechat | 83.4% (221/265; 78.5 to 87.4) | 4.9% (8/163) | 6.1% (10/163) | 77.6% (59/76) | 9.2% (7/76) | 0.48 (n=26) |
|  | Jev | 79.6% (211/265; 74.4 to 84.0) | 1.8% (3/163) | 17.8% (29/163) | 75.0% (57/76) | 13.2% (10/76) |  |
| pilot-0.4@anonymous | Sidechat | 83.4% (221/265; 78.5 to 87.4) | 4.9% (8/163) | 6.1% (10/163) | 77.6% (59/76) | 9.2% (7/76) | 0.48 (n=26) |
|  | Jev | 77.4% (205/265; 72.0 to 82.0) | 1.8% (3/163) | 18.4% (30/163) | 68.4% (52/76) | 13.2% (10/76) |  |
| demo-lines-0.1 | Sidechat | 95.8% (46/48; 86.0 to 98.9) | 0.0% (0/26) | 0.0% (0/26) | 89.5% (17/19) | 0.0% (0/19) | 0.51 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 96.7% (50581/52336; 96.5 to 96.8) | 0.8% (374/44528) | 1.2% (552/44528) | 89.4% (6979/7808) | 8.9% (694/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 96.7% (15267/15793; 96.4 to 96.9) | 1.1% (169/15793) | 2.3% (357/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 97.8% (8681/8875; 97.5 to 98.1) | 0.8% (68/8875) | 1.4% (126/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +17.6 (+16.1 to +19.1), better on 2860 lines
- generated test @named: +17.1 (+15.6 to +18.6), better on 2860 lines
- pilot-0.4: +3.8 (-1.5 to +9.1), within noise on 265 lines
- pilot-0.4@anonymous: +6.0 (+0.8 to +11.3), better on 265 lines
- demo-lines-0.1: -2.1 (-9.1 to +5.0), within noise on 48 lines
- duplex-mpe-0.1: +13.5 (+13.2 to +13.9), better on 52336 lines
- ambient-bench-0.1: +11.3 (+10.8 to +11.8), better on 15793 lines
- ami-addressee-0.1: +12.6 (+11.9 to +13.3), better on 8875 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0048, mean distance to target 0.0147, AUROC 0.9792
- generated test @named: calibration error 0.0047, mean distance to target 0.0147, AUROC 0.9793
- generated test @none: calibration error 0.008, mean distance to target 0.0253, AUROC 0.9788
- pilot-0.4: calibration error 0.0756, mean distance to target 0.109, AUROC 0.9261
- pilot-0.4@anonymous: calibration error 0.077, mean distance to target 0.109, AUROC 0.9259
- demo-lines-0.1: calibration error 0.0443, mean distance to target 0.0443, AUROC 0.9891
- duplex-mpe-0.1: calibration error 0.0139, mean distance to target 0.0355, AUROC 0.986
- ambient-bench-0.1: calibration error 0.0239, mean distance to target 0.0459
- ami-addressee-0.1: calibration error 0.0222, mean distance to target 0.0222

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 98.3% (9992/10168) | 0.3% (17/5635) | 98.2% (3186/3246) |
| `o` | 98.6% (5564/5644) | 0.3% (9/3090) | 98.7% (1809/1833) |
| `c` | 98.4% (2618/2661) | 0.4% (6/1464) | 97.9% (846/864) |
| `a` | 99.3% (2552/2571) | 0.1% (1/1384) | 99.1% (872/880) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 98.8% (8146/8244) | 0.2% (10/4509) | 98.8% (2666/2698) |
| `writer` | 98.3% (5509/5603) | 0.3% (9/3151) | 98.1% (1714/1747) |
| `agent_name,writer` | 98.2% (3425/3488) | 0.3% (5/1894) | 98.4% (1112/1130) |
| `agent_name` | 98.3% (2131/2168) | 0.5% (6/1186) | 98.2% (705/718) |
| `setting,writer` | 98.6% (685/695) | 0.2% (1/393) | 97.8% (225/230) |
| `setting,agent_name,writer` | 97.6% (373/382) | 1.0% (2/197) | 97.1% (135/139) |
| `setting` | 98.9% (274/277) | 0.0% (0/138) | 98.2% (112/114) |
| `setting,agent_name` | 97.9% (183/187) | 0.0% (0/105) | 93.6% (44/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.3% (8844/8999) | 0.4% (31/7292) | n/a |
| `G6` | 96.3% (3968/4120) | 0.0% (0/318) | 96.5% (2915/3021) |
| `G2` | 99.9% (3555/3558) | 0.0% (0/181) | 99.9% (3374/3377) |
| `G4` | 99.7% (1763/1768) | 0.0% (0/1183) | 99.8% (424/425) |
| `G3` | 100.0% (2114/2114) | 0.0% (0/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.0% (150/153) | 1.3% (2/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 98.5% (13830/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 98.5% (13831/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 98.9% (3231/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 98.9% (3231/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 93.8% (2853/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 93.8% (2851/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 99.2% (1983/2000) | 99.2% (1983/2000) | 99.2% (1983/2000) | 99.2% (1983/2000) |
| `implicit/T` | 61.0% (1220/2000) | 26.6% (531/2000) | 61.0% (1220/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.2% (1889/1904) | 98.8% (1882/1904) | 99.2% (1889/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 98.9% (1889/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.1% (1887/1904) | 99.0% (1884/1904) | 99.1% (1887/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 98.7% (1886/1911) | 99.5% (1902/1911) | n/a | n/a |

## ettin-150m

Run `side-r1-ettin-150m-s0`. Best epoch 2 of 3; history [{'epoch': 1, 'train_loss': 0.5978, 'dev_loss': 0.3279, 'secs': 255}, {'epoch': 2, 'train_loss': 0.3325, 'dev_loss': 0.2988, 'secs': 465}, {'epoch': 3, 'train_loss': 0.2679, 'dev_loss': 0.3134, 'secs': 678}]. Temperatures {'intent': 1.25, 'respond': 1.45, 'unclear': 1.2}. 89995 training rows, 6000 dev rows, 724 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.6 (8538/8654 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 98.5% (20718/21044; 98.3 to 98.6) | 0.3% (33/11573) | 0.2% (21/11573) | 98.6% (6729/6823) | 0.9% (62/6823) | 0.49 (n=2648) |
|  | Jev | 80.7% (2308/2860; 79.2 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.5% (724/934) | 6.9% (64/934) |  |
| generated test @named | Sidechat | 98.5% (20721/21044; 98.3 to 98.6) | 0.3% (33/11573) | 0.2% (21/11573) | 98.6% (6730/6823) | 0.9% (61/6823) | 0.49 (n=2648) |
|  | Jev | 81.2% (2323/2860; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (745/934) | 6.3% (59/934) |  |
| generated test @none | Sidechat | 97.0% (20415/21044; 96.8 to 97.2) | 0.3% (39/11573) | 0.2% (28/11573) | 97.1% (6623/6823) | 0.9% (64/6823) | 0.52 (n=2648) |
| pilot-0.4 | Sidechat | 85.7% (227/265; 80.9 to 89.4) | 3.7% (6/163) | 6.1% (10/163) | 85.5% (65/76) | 6.6% (5/76) | 0.48 (n=26) |
|  | Jev | 79.6% (211/265; 74.4 to 84.0) | 1.8% (3/163) | 17.8% (29/163) | 75.0% (57/76) | 13.2% (10/76) |  |
| pilot-0.4@anonymous | Sidechat | 85.7% (227/265; 80.9 to 89.4) | 3.7% (6/163) | 6.1% (10/163) | 85.5% (65/76) | 6.6% (5/76) | 0.48 (n=26) |
|  | Jev | 77.4% (205/265; 72.0 to 82.0) | 1.8% (3/163) | 18.4% (30/163) | 68.4% (52/76) | 13.2% (10/76) |  |
| demo-lines-0.1 | Sidechat | 93.8% (45/48; 83.2 to 97.9) | 0.0% (0/26) | 3.9% (1/26) | 89.5% (17/19) | 0.0% (0/19) | 0.49 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 96.6% (50571/52336; 96.5 to 96.8) | 0.8% (343/44528) | 1.2% (534/44528) | 88.6% (6920/7808) | 9.3% (726/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 96.4% (15228/15793; 96.1 to 96.7) | 1.2% (188/15793) | 2.4% (377/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 97.0% (8612/8875; 96.7 to 97.4) | 1.2% (108/8875) | 1.8% (155/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +17.7 (+16.2 to +19.2), better on 2860 lines
- generated test @named: +17.2 (+15.7 to +18.6), better on 2860 lines
- pilot-0.4: +6.0 (+0.8 to +11.3), better on 265 lines
- pilot-0.4@anonymous: +8.3 (+2.8 to +13.9), better on 265 lines
- demo-lines-0.1: -4.2 (-12.2 to +3.9), within noise on 48 lines
- duplex-mpe-0.1: +13.5 (+13.2 to +13.9), better on 52336 lines
- ambient-bench-0.1: +11.1 (+10.5 to +11.6), better on 15793 lines
- ami-addressee-0.1: +11.8 (+11.1 to +12.5), better on 8875 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0063, mean distance to target 0.0152, AUROC 0.9854
- generated test @named: calibration error 0.0063, mean distance to target 0.0152, AUROC 0.9854
- generated test @none: calibration error 0.0078, mean distance to target 0.0248, AUROC 0.9851
- pilot-0.4: calibration error 0.0532, mean distance to target 0.1011, AUROC 0.9424
- pilot-0.4@anonymous: calibration error 0.0532, mean distance to target 0.1009, AUROC 0.9423
- demo-lines-0.1: calibration error 0.0293, mean distance to target 0.0495, AUROC 0.9855
- duplex-mpe-0.1: calibration error 0.0111, mean distance to target 0.036, AUROC 0.9896
- ambient-bench-0.1: calibration error 0.0223, mean distance to target 0.0482
- ami-addressee-0.1: calibration error 0.0304, mean distance to target 0.0304

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 98.2% (9987/10168) | 0.2% (13/5635) | 98.4% (3194/3246) |
| `o` | 98.6% (5566/5644) | 0.3% (8/3090) | 98.8% (1810/1833) |
| `c` | 98.3% (2615/2661) | 0.6% (9/1464) | 98.5% (851/864) |
| `a` | 99.2% (2550/2571) | 0.2% (3/1384) | 99.3% (874/880) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 98.6% (8131/8244) | 0.3% (14/4509) | 98.8% (2666/2698) |
| `writer` | 98.3% (5507/5603) | 0.2% (5/3151) | 98.3% (1718/1747) |
| `agent_name,writer` | 98.0% (3417/3488) | 0.4% (7/1894) | 98.5% (1113/1130) |
| `agent_name` | 98.9% (2143/2168) | 0.4% (5/1186) | 99.0% (711/718) |
| `setting,writer` | 98.9% (687/695) | 0.0% (0/393) | 98.7% (227/230) |
| `setting,agent_name,writer` | 98.4% (376/382) | 0.5% (1/197) | 97.8% (136/139) |
| `setting` | 98.6% (273/277) | 0.7% (1/138) | 98.2% (112/114) |
| `setting,agent_name` | 98.4% (184/187) | 0.0% (0/105) | 97.9% (46/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.1% (8829/8999) | 0.4% (26/7292) | n/a |
| `G6` | 96.8% (3988/4120) | 0.0% (0/318) | 97.2% (2938/3021) |
| `G2` | 99.8% (3552/3558) | 0.0% (0/181) | 99.8% (3371/3377) |
| `G4` | 99.3% (1755/1768) | 0.2% (3/1183) | 98.8% (420/425) |
| `G3` | 99.9% (2112/2114) | 0.1% (1/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.0% (150/153) | 2.0% (3/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 99.4% (13965/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 99.4% (13961/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.7% (3256/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.7% (3257/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 94.2% (2865/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 94.2% (2862/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 99.3% (1986/2000) | 99.2% (1983/2000) | 99.3% (1986/2000) | 99.2% (1983/2000) |
| `implicit/T` | 57.6% (1152/2000) | 26.6% (531/2000) | 57.6% (1152/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.3% (1891/1904) | 98.8% (1882/1904) | 99.3% (1891/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 91.3% (1744/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.3% (1891/1904) | 99.0% (1884/1904) | 99.3% (1891/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 91.1% (1741/1911) | 99.5% (1902/1911) | n/a | n/a |
