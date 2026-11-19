# Training run: exp-028-side-train-r4

Every number below is measured in this run. A share is `value (k/n)`; headline shares also give a 95% interval.

## ettin-68m

Run `side-r4-ettin-68m-s0`. Best epoch 2 of 2; history [{'epoch': 1, 'train_loss': 0.4251, 'dev_loss': 0.2456, 'secs': 637}, {'epoch': 2, 'train_loss': 0.2651, 'dev_loss': 0.231, 'secs': 1213}]. Temperatures {'intent': 1.5, 'respond': 1.45, 'unclear': 1.55}. 337993 training rows, 6000 dev rows, 1237 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.4 (29958/30248 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 99.0% (21015/21233; 98.8 to 99.1) | 0.2% (22/11573) | 0.3% (32/11573) | 99.0% (6945/7012) | 0.5% (37/7012) | 0.50 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 99.0% (21015/21233; 98.8 to 99.1) | 0.2% (21/11573) | 0.3% (34/11573) | 99.1% (6946/7012) | 0.5% (37/7012) | 0.50 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 97.5% (20695/21233; 97.2 to 97.7) | 0.3% (31/11573) | 0.2% (28/11573) | 97.8% (6857/7012) | 0.8% (54/7012) | 0.53 (n=2648) |
| pilot-0.4 | Sidechat | 86.7% (234/270; 82.1 to 90.2) | 3.1% (5/163) | 4.9% (8/163) | 84.0% (68/81) | 8.6% (7/81) | 0.44 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 86.7% (234/270; 82.1 to 90.2) | 3.1% (5/163) | 4.9% (8/163) | 84.0% (68/81) | 8.6% (7/81) | 0.44 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) | 0.52 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 95.2% (49802/52336; 95.0 to 95.3) | 0.4% (194/44528) | 1.4% (642/44528) | 78.2% (6110/7808) | 18.0% (1403/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 98.1% (15493/15793; 97.9 to 98.3) | 0.7% (117/15793) | 1.2% (183/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 100.0% (8872/8875; 99.9 to 100.0) | 0.0% (0/8875) | 0.0% (3/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 100.0% (10433/10434; 100.0 to 100.0) | 0.0% (0/10434) | 0.0% (1/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |
| gen-0.2.test@anonymous | Sidechat | 98.8% (15970/16158; 98.7 to 99.0) | 0.4% (45/10269) | 0.3% (33/10269) | 98.7% (4340/4397) | 0.7% (31/4397) | 0.50 (n=1492) |
| gen-0.3.test@anonymous | Sidechat | 98.9% (12288/12426; 98.7 to 99.1) | 0.3% (24/7881) | 0.2% (15/7881) | 98.6% (3120/3164) | 0.7% (22/3164) | 0.50 (n=1381) |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +18.4 (+17.0 to +19.9), better on 2882 lines
- generated test @named: +17.9 (+16.5 to +19.4), better on 2882 lines
- pilot-0.4: +6.7 (+1.5 to +11.8), better on 270 lines
- pilot-0.4@anonymous: +8.9 (+3.5 to +14.3), better on 270 lines
- demo-lines-0.1: +0.0 (-5.8 to +5.8), within noise on 48 lines
- duplex-mpe-0.1: +12.0 (+11.7 to +12.4), better on 52336 lines
- ambient-bench-0.1: +12.8 (+12.2 to +13.3), better on 15793 lines
- ami-addressee-0.1: +14.8 (+14.0 to +15.5), better on 8875 lines
- ami-silent-0.1.test: +10.0 (+9.4 to +10.5), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0047, mean distance to target 0.0113, AUROC 0.9809
- generated test @named: calibration error 0.0048, mean distance to target 0.0112, AUROC 0.981
- generated test @none: calibration error 0.006, mean distance to target 0.0207, AUROC 0.9799
- pilot-0.4: calibration error 0.0541, mean distance to target 0.0981, AUROC 0.9474
- pilot-0.4@anonymous: calibration error 0.0539, mean distance to target 0.0983, AUROC 0.9472
- demo-lines-0.1: calibration error 0.0371, mean distance to target 0.0372, AUROC 1.0
- duplex-mpe-0.1: calibration error 0.025, mean distance to target 0.043, AUROC 0.9762
- ambient-bench-0.1: calibration error 0.0218, mean distance to target 0.038
- ami-addressee-0.1: calibration error 0.0003, mean distance to target 0.0003
- ami-silent-0.1.test: calibration error 0.0002, mean distance to target 0.0002
- gen-0.2.test@anonymous: calibration error 0.0056, mean distance to target 0.0124, AUROC 0.9775
- gen-0.3.test@anonymous: calibration error 0.0054, mean distance to target 0.0116, AUROC 0.9789

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 98.8% (10144/10264) | 0.2% (12/5635) | 98.9% (3306/3342) |
| `o` | 99.1% (5643/5697) | 0.1% (3/3090) | 99.2% (1870/1886) |
| `c` | 98.8% (2648/2681) | 0.4% (6/1464) | 98.9% (874/884) |
| `a` | 99.6% (2580/2591) | 0.1% (1/1384) | 99.4% (895/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 99.2% (8242/8312) | 0.2% (8/4509) | 99.3% (2746/2766) |
| `writer` | 98.9% (5592/5653) | 0.2% (6/3151) | 99.1% (1780/1797) |
| `agent_name,writer` | 98.7% (3479/3524) | 0.3% (6/1894) | 98.8% (1152/1166) |
| `agent_name` | 99.0% (2165/2188) | 0.2% (2/1186) | 99.1% (731/738) |
| `setting,writer` | 99.1% (695/701) | 0.0% (0/393) | 99.2% (234/236) |
| `setting,agent_name,writer` | 97.9% (378/386) | 0.0% (0/197) | 97.9% (140/143) |
| `setting` | 98.6% (278/282) | 0.0% (0/138) | 97.5% (116/119) |
| `setting,agent_name` | 99.5% (186/187) | 0.0% (0/105) | 97.9% (46/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.6% (8876/8999) | 0.2% (18/7292) | n/a |
| `G6` | 98.0% (4037/4120) | 0.0% (0/318) | 97.9% (2957/3021) |
| `G2` | 99.9% (3744/3747) | 1.1% (2/181) | 100.0% (3565/3566) |
| `G4` | 99.7% (1762/1768) | 0.1% (1/1183) | 99.5% (423/425) |
| `G3` | 100.0% (2113/2114) | 0.0% (0/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.7% (151/153) | 0.7% (1/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 99.2% (13939/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 99.2% (13930/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.8% (3260/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.8% (3261/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 90.1% (2740/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 90.6% (2752/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 99.6% (1992/2000) | 99.2% (1983/2000) | 99.6% (1992/2000) | 99.2% (1983/2000) |
| `implicit/T` | 17.1% (341/2000) | 26.6% (531/2000) | 17.1% (341/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.3% (1890/1904) | 98.8% (1882/1904) | 99.3% (1890/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 99.6% (1904/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.1% (1887/1904) | 99.0% (1884/1904) | 99.1% (1887/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 99.7% (1906/1911) | 99.5% (1902/1911) | n/a | n/a |

## ettin-150m

Run `side-r4-ettin-150m-s0`. Best epoch 2 of 2; history [{'epoch': 1, 'train_loss': 0.4082, 'dev_loss': 0.2422, 'secs': 977}, {'epoch': 2, 'train_loss': 0.256, 'dev_loss': 0.2243, 'secs': 1879}]. Temperatures {'intent': 1.4, 'respond': 1.4, 'unclear': 1.3}. 337993 training rows, 6000 dev rows, 1911 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.65, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.6 (29963/30248 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 99.0% (21029/21233; 98.9 to 99.2) | 0.1% (13/11573) | 0.2% (20/11573) | 99.2% (6954/7012) | 0.5% (33/7012) | 0.50 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 99.0% (21029/21233; 98.9 to 99.2) | 0.1% (13/11573) | 0.2% (21/11573) | 99.2% (6954/7012) | 0.5% (32/7012) | 0.50 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 97.5% (20708/21233; 97.3 to 97.7) | 0.2% (20/11573) | 0.2% (21/11573) | 97.5% (6840/7012) | 0.7% (46/7012) | 0.53 (n=2648) |
| pilot-0.4 | Sidechat | 87.4% (236/270; 82.9 to 90.8) | 3.1% (5/163) | 4.3% (7/163) | 85.2% (69/81) | 7.4% (6/81) | 0.39 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 87.4% (236/270; 82.9 to 90.8) | 3.1% (5/163) | 4.3% (7/163) | 85.2% (69/81) | 7.4% (6/81) | 0.39 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) | 0.50 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 95.6% (50034/52336; 95.4 to 95.8) | 1.0% (430/44528) | 1.2% (530/44528) | 82.8% (6466/7808) | 14.7% (1150/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 98.5% (15551/15793; 98.3 to 98.7) | 0.5% (87/15793) | 1.0% (155/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 99.9% (8867/8875; 99.8 to 100.0) | 0.0% (1/8875) | 0.1% (7/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 99.9% (10427/10434; 99.9 to 100.0) | 0.0% (1/10434) | 0.1% (6/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |
| gen-0.2.test@anonymous | Sidechat | 98.9% (15976/16158; 98.7 to 99.0) | 0.4% (38/10269) | 0.2% (24/10269) | 98.7% (4340/4397) | 0.6% (28/4397) | 0.50 (n=1492) |
| gen-0.3.test@anonymous | Sidechat | 98.9% (12286/12426; 98.7 to 99.0) | 0.3% (24/7881) | 0.1% (11/7881) | 98.4% (3113/3164) | 0.8% (24/3164) | 0.50 (n=1381) |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +18.4 (+16.9 to +19.8), better on 2882 lines
- generated test @named: +17.9 (+16.4 to +19.3), better on 2882 lines
- pilot-0.4: +7.4 (+2.2 to +12.6), better on 270 lines
- pilot-0.4@anonymous: +9.6 (+4.2 to +15.0), better on 270 lines
- demo-lines-0.1: +0.0 (-5.8 to +5.8), within noise on 48 lines
- duplex-mpe-0.1: +12.5 (+12.2 to +12.8), better on 52336 lines
- ambient-bench-0.1: +13.1 (+12.6 to +13.7), better on 15793 lines
- ami-addressee-0.1: +14.7 (+14.0 to +15.4), better on 8875 lines
- ami-silent-0.1.test: +9.9 (+9.3 to +10.5), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.004, mean distance to target 0.0105, AUROC 0.9803
- generated test @named: calibration error 0.004, mean distance to target 0.0104, AUROC 0.9803
- generated test @none: calibration error 0.0051, mean distance to target 0.0203, AUROC 0.9788
- pilot-0.4: calibration error 0.0598, mean distance to target 0.0932, AUROC 0.9517
- pilot-0.4@anonymous: calibration error 0.0596, mean distance to target 0.0934, AUROC 0.9515
- demo-lines-0.1: calibration error 0.0381, mean distance to target 0.0381, AUROC 1.0
- duplex-mpe-0.1: calibration error 0.0233, mean distance to target 0.0451, AUROC 0.9799
- ambient-bench-0.1: calibration error 0.0171, mean distance to target 0.0335
- ami-addressee-0.1: calibration error 0.0015, mean distance to target 0.0015
- ami-silent-0.1.test: calibration error 0.0012, mean distance to target 0.0012
- gen-0.2.test@anonymous: calibration error 0.0053, mean distance to target 0.0122, AUROC 0.9771
- gen-0.3.test@anonymous: calibration error 0.0053, mean distance to target 0.0115, AUROC 0.9791

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 98.9% (10147/10264) | 0.1% (8/5635) | 99.0% (3308/3342) |
| `o` | 99.1% (5648/5697) | 0.1% (3/3090) | 99.3% (1873/1886) |
| `c` | 99.0% (2654/2681) | 0.1% (2/1464) | 99.1% (876/884) |
| `a` | 99.6% (2580/2591) | 0.0% (0/1384) | 99.7% (897/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 99.2% (8250/8312) | 0.1% (5/4509) | 99.5% (2752/2766) |
| `writer` | 99.0% (5596/5653) | 0.2% (5/3151) | 99.1% (1781/1797) |
| `agent_name,writer` | 98.8% (3483/3524) | 0.2% (3/1894) | 99.2% (1157/1166) |
| `agent_name` | 99.1% (2169/2188) | 0.0% (0/1186) | 99.3% (733/738) |
| `setting,writer` | 98.4% (690/701) | 0.0% (0/393) | 97.5% (230/236) |
| `setting,agent_name,writer` | 97.9% (378/386) | 0.0% (0/197) | 97.9% (140/143) |
| `setting` | 98.6% (278/282) | 0.0% (0/138) | 96.6% (115/119) |
| `setting,agent_name` | 98.9% (185/187) | 0.0% (0/105) | 97.9% (46/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.7% (8886/8999) | 0.1% (10/7292) | n/a |
| `G6` | 98.1% (4041/4120) | 0.0% (0/318) | 98.2% (2968/3021) |
| `G2` | 99.9% (3744/3747) | 0.5% (1/181) | 99.9% (3564/3566) |
| `G4` | 99.6% (1760/1768) | 0.2% (2/1183) | 99.3% (422/425) |
| `G3` | 100.0% (2114/2114) | 0.0% (0/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 99.4% (152/153) | 0.0% (0/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 99.1% (13913/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 99.0% (13910/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.9% (3264/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.9% (3265/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 94.1% (2861/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 94.2% (2862/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 99.7% (1993/2000) | 99.2% (1983/2000) | 99.7% (1993/2000) | 99.2% (1983/2000) |
| `implicit/T` | 34.5% (691/2000) | 26.6% (531/2000) | 34.5% (691/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.4% (1892/1904) | 98.8% (1882/1904) | 99.4% (1892/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 91.3% (1744/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.3% (1890/1904) | 99.0% (1884/1904) | 99.3% (1890/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 91.5% (1749/1911) | 99.5% (1902/1911) | n/a | n/a |
