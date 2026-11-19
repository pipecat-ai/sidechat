# Training run: exp-025-side-train-r3

Every number below is measured in this run. A share is `value (k/n)`; headline shares also give a 95% interval.

## ettin-68m

Run `side-r3-ettin-68m-s0`. Best epoch 2 of 2; history [{'epoch': 1, 'train_loss': 0.444, 'dev_loss': 0.2448, 'secs': 510}, {'epoch': 2, 'train_loss': 0.2661, 'dev_loss': 0.2327, 'secs': 968}]. Temperatures {'intent': 1.6, 'respond': 1.7, 'unclear': 1.45}. 235069 training rows, 6000 dev rows, 995 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.4 (20628/20841 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 98.9% (21007/21233; 98.8 to 99.1) | 0.2% (25/11573) | 0.3% (33/11573) | 99.1% (6947/7012) | 0.5% (37/7012) | 0.50 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 98.9% (21003/21233; 98.8 to 99.1) | 0.2% (26/11573) | 0.3% (33/11573) | 99.1% (6947/7012) | 0.5% (37/7012) | 0.50 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 97.3% (20658/21233; 97.1 to 97.5) | 0.3% (33/11573) | 0.4% (44/11573) | 97.5% (6834/7012) | 0.7% (47/7012) | 0.52 (n=2648) |
| pilot-0.4 | Sidechat | 85.2% (230/270; 80.5 to 88.9) | 3.7% (6/163) | 6.1% (10/163) | 82.7% (67/81) | 7.4% (6/81) | 0.42 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 85.2% (230/270; 80.5 to 88.9) | 3.7% (6/163) | 6.1% (10/163) | 82.7% (67/81) | 7.4% (6/81) | 0.42 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 100.0% (48/48; 92.6 to 100.0) | 0.0% (0/26) | 0.0% (0/26) | 100.0% (19/19) | 0.0% (0/19) | 0.50 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 95.5% (49968/52336; 95.3 to 95.7) | 0.3% (144/44528) | 1.3% (598/44528) | 79.2% (6182/7808) | 16.7% (1300/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 98.6% (15579/15793; 98.5 to 98.8) | 0.3% (44/15793) | 1.1% (170/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 100.0% (8874/8875; 99.9 to 100.0) | 0.0% (0/8875) | 0.0% (1/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 100.0% (10434/10434; 100.0 to 100.0) | 0.0% (0/10434) | 0.0% (0/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |
| gen-0.2.test@anonymous | Sidechat | 98.7% (15952/16158; 98.5 to 98.9) | 0.5% (52/10269) | 0.4% (40/10269) | 98.7% (4339/4397) | 0.6% (25/4397) | 0.50 (n=1492) |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +18.4 (+17.0 to +19.9), better on 2882 lines
- generated test @named: +17.9 (+16.5 to +19.4), better on 2882 lines
- pilot-0.4: +5.2 (-0.0 to +10.4), within noise on 270 lines
- pilot-0.4@anonymous: +7.4 (+2.1 to +12.8), better on 270 lines
- demo-lines-0.1: +2.1 (-2.0 to +6.1), within noise on 48 lines
- duplex-mpe-0.1: +12.4 (+12.0 to +12.7), better on 52336 lines
- ambient-bench-0.1: +13.3 (+12.8 to +13.8), better on 15793 lines
- ami-addressee-0.1: +14.8 (+14.0 to +15.5), better on 8875 lines
- ami-silent-0.1.test: +10.0 (+9.4 to +10.5), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0045, mean distance to target 0.0138, AUROC 0.9804
- generated test @named: calibration error 0.0041, mean distance to target 0.0138, AUROC 0.9805
- generated test @none: calibration error 0.0058, mean distance to target 0.0234, AUROC 0.9793
- pilot-0.4: calibration error 0.0737, mean distance to target 0.1011, AUROC 0.9448
- pilot-0.4@anonymous: calibration error 0.0741, mean distance to target 0.1012, AUROC 0.9448
- demo-lines-0.1: calibration error 0.0339, mean distance to target 0.0339, AUROC 1.0
- duplex-mpe-0.1: calibration error 0.0141, mean distance to target 0.0472, AUROC 0.9769
- ambient-bench-0.1: calibration error 0.0144, mean distance to target 0.0336
- ami-addressee-0.1: calibration error 0.0002, mean distance to target 0.0002
- ami-silent-0.1.test: calibration error 0.0001, mean distance to target 0.0001
- gen-0.2.test@anonymous: calibration error 0.0057, mean distance to target 0.0154, AUROC 0.9772

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 98.8% (10142/10264) | 0.3% (15/5635) | 99.0% (3309/3342) |
| `o` | 99.0% (5640/5697) | 0.2% (5/3090) | 99.2% (1870/1886) |
| `c` | 98.7% (2647/2681) | 0.2% (3/1464) | 98.8% (873/884) |
| `a` | 99.5% (2578/2591) | 0.1% (2/1384) | 99.4% (895/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 99.1% (8236/8312) | 0.2% (7/4509) | 99.2% (2744/2766) |
| `writer` | 98.8% (5587/5653) | 0.2% (6/3151) | 99.0% (1779/1797) |
| `agent_name,writer` | 98.8% (3481/3524) | 0.4% (7/1894) | 99.1% (1155/1166) |
| `agent_name` | 99.0% (2166/2188) | 0.2% (2/1186) | 99.1% (731/738) |
| `setting,writer` | 99.3% (696/701) | 0.0% (0/393) | 99.6% (235/236) |
| `setting,agent_name,writer` | 97.9% (378/386) | 1.0% (2/197) | 97.9% (140/143) |
| `setting` | 98.9% (279/282) | 0.7% (1/138) | 98.3% (117/119) |
| `setting,agent_name` | 98.4% (184/187) | 0.0% (0/105) | 97.9% (46/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.6% (8874/8999) | 0.3% (19/7292) | n/a |
| `G6` | 97.9% (4033/4120) | 0.0% (0/318) | 98.0% (2960/3021) |
| `G2` | 100.0% (3746/3747) | 0.5% (1/181) | 100.0% (3566/3566) |
| `G4` | 99.4% (1758/1768) | 0.2% (3/1183) | 99.1% (421/425) |
| `G3` | 100.0% (2113/2114) | 0.1% (1/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.7% (151/153) | 0.7% (1/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 99.3% (13943/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 99.2% (13936/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.8% (3261/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.9% (3264/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 92.4% (2811/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 92.4% (2809/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 99.8% (1995/2000) | 99.2% (1983/2000) | 99.8% (1995/2000) | 99.2% (1983/2000) |
| `implicit/T` | 20.3% (407/2000) | 26.6% (531/2000) | 20.3% (407/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.3% (1891/1904) | 98.8% (1882/1904) | 99.3% (1891/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 98.4% (1880/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.2% (1889/1904) | 99.0% (1884/1904) | 99.2% (1889/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 98.5% (1882/1911) | 99.5% (1902/1911) | n/a | n/a |

## ettin-150m

Run `side-r3-ettin-150m-s0`. Best epoch 2 of 2; history [{'epoch': 1, 'train_loss': 0.4283, 'dev_loss': 0.2437, 'secs': 645}, {'epoch': 2, 'train_loss': 0.2567, 'dev_loss': 0.2211, 'secs': 1215}]. Temperatures {'intent': 1.55, 'respond': 1.55, 'unclear': 1.35}. 235069 training rows, 6000 dev rows, 1264 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.3 (20625/20841 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 99.0% (21009/21233; 98.8 to 99.1) | 0.2% (25/11573) | 0.3% (31/11573) | 99.2% (6956/7012) | 0.5% (34/7012) | 0.50 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 98.9% (21008/21233; 98.8 to 99.1) | 0.2% (26/11573) | 0.3% (31/11573) | 99.2% (6958/7012) | 0.5% (33/7012) | 0.50 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 97.4% (20689/21233; 97.2 to 97.6) | 0.3% (33/11573) | 0.3% (35/11573) | 98.1% (6876/7012) | 0.6% (40/7012) | 0.53 (n=2648) |
| pilot-0.4 | Sidechat | 87.4% (236/270; 82.9 to 90.8) | 4.3% (7/163) | 3.7% (6/163) | 85.2% (69/81) | 6.2% (5/81) | 0.41 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 87.4% (236/270; 82.9 to 90.8) | 4.3% (7/163) | 3.7% (6/163) | 85.2% (69/81) | 7.4% (6/81) | 0.41 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) | 0.50 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 96.7% (50592/52336; 96.5 to 96.8) | 0.2% (97/44528) | 0.9% (382/44528) | 83.8% (6543/7808) | 12.7% (995/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 98.7% (15591/15793; 98.5 to 98.9) | 0.2% (33/15793) | 1.1% (169/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 99.9% (8865/8875; 99.8 to 99.9) | 0.0% (0/8875) | 0.1% (10/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 99.9% (10423/10434; 99.8 to 99.9) | 0.0% (0/10434) | 0.1% (11/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |
| gen-0.2.test@anonymous | Sidechat | 98.8% (15959/16158; 98.6 to 98.9) | 0.4% (44/10269) | 0.4% (43/10269) | 98.7% (4341/4397) | 0.7% (29/4397) | 0.50 (n=1492) |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +18.0 (+16.6 to +19.5), better on 2882 lines
- generated test @named: +17.7 (+16.2 to +19.1), better on 2882 lines
- pilot-0.4: +7.4 (+2.2 to +12.6), better on 270 lines
- pilot-0.4@anonymous: +9.6 (+4.2 to +15.0), better on 270 lines
- demo-lines-0.1: +0.0 (-5.8 to +5.8), within noise on 48 lines
- duplex-mpe-0.1: +13.6 (+13.2 to +13.9), better on 52336 lines
- ambient-bench-0.1: +13.4 (+12.8 to +13.9), better on 15793 lines
- ami-addressee-0.1: +14.7 (+13.9 to +15.4), better on 8875 lines
- ami-silent-0.1.test: +9.8 (+9.3 to +10.4), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0046, mean distance to target 0.0126, AUROC 0.9808
- generated test @named: calibration error 0.0046, mean distance to target 0.0126, AUROC 0.9809
- generated test @none: calibration error 0.0057, mean distance to target 0.022, AUROC 0.9803
- pilot-0.4: calibration error 0.0576, mean distance to target 0.0941, AUROC 0.9533
- pilot-0.4@anonymous: calibration error 0.0562, mean distance to target 0.0945, AUROC 0.9528
- demo-lines-0.1: calibration error 0.0421, mean distance to target 0.0421, AUROC 1.0
- duplex-mpe-0.1: calibration error 0.0128, mean distance to target 0.0335, AUROC 0.9856
- ambient-bench-0.1: calibration error 0.015, mean distance to target 0.0307
- ami-addressee-0.1: calibration error 0.0013, mean distance to target 0.0013
- ami-silent-0.1.test: calibration error 0.0011, mean distance to target 0.0011
- gen-0.2.test@anonymous: calibration error 0.0054, mean distance to target 0.0138, AUROC 0.978

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 98.8% (10139/10264) | 0.3% (15/5635) | 99.1% (3311/3342) |
| `o` | 99.0% (5639/5697) | 0.2% (6/3090) | 99.3% (1872/1886) |
| `c` | 99.0% (2654/2681) | 0.2% (3/1464) | 99.3% (878/884) |
| `a` | 99.5% (2577/2591) | 0.1% (1/1384) | 99.4% (895/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 99.1% (8238/8312) | 0.2% (9/4509) | 99.4% (2748/2766) |
| `writer` | 98.8% (5587/5653) | 0.2% (6/3151) | 99.2% (1782/1797) |
| `agent_name,writer` | 98.8% (3481/3524) | 0.4% (8/1894) | 99.1% (1156/1166) |
| `agent_name` | 99.1% (2169/2188) | 0.1% (1/1186) | 99.6% (735/738) |
| `setting,writer` | 99.1% (695/701) | 0.0% (0/393) | 98.7% (233/236) |
| `setting,agent_name,writer` | 97.4% (376/386) | 0.5% (1/197) | 97.9% (140/143) |
| `setting` | 98.9% (279/282) | 0.0% (0/138) | 98.3% (117/119) |
| `setting,agent_name` | 98.4% (184/187) | 0.0% (0/105) | 95.7% (45/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.6% (8870/8999) | 0.3% (19/7292) | n/a |
| `G6` | 98.0% (4038/4120) | 0.0% (0/318) | 98.2% (2968/3021) |
| `G2` | 99.9% (3744/3747) | 0.0% (0/181) | 99.9% (3563/3566) |
| `G4` | 99.7% (1762/1768) | 0.2% (3/1183) | 100.0% (425/425) |
| `G3` | 99.9% (2112/2114) | 0.1% (2/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.7% (151/153) | 0.7% (1/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 99.7% (14010/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 99.7% (14006/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.9% (3265/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.9% (3265/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 95.3% (2898/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 95.5% (2901/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 99.5% (1990/2000) | 99.2% (1983/2000) | 99.5% (1990/2000) | 99.2% (1983/2000) |
| `implicit/T` | 38.8% (775/2000) | 26.6% (531/2000) | 38.8% (775/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.3% (1890/1904) | 98.8% (1882/1904) | 99.3% (1890/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 96.7% (1847/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.2% (1888/1904) | 99.0% (1884/1904) | 99.2% (1888/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 97.2% (1857/1911) | 99.5% (1902/1911) | n/a | n/a |
