# Training run: exp-022-side-train-r2

Every number below is measured in this run. A share is `value (k/n)`; headline shares also give a 95% interval.

## ettin-68m

Run `side-r2-ettin-68m-s0`. Best epoch 2 of 2; history [{'epoch': 1, 'train_loss': 0.4454, 'dev_loss': 0.2276, 'secs': 618}, {'epoch': 2, 'train_loss': 0.2632, 'dev_loss': 0.2078, 'secs': 1188}]. Temperatures {'intent': 1.45, 'respond': 1.4, 'unclear': 1.35}. 236439 training rows, 6000 dev rows, 1206 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.4 (20790/20988 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 98.8% (20985/21233; 98.7 to 99.0) | 0.2% (25/11573) | 0.3% (39/11573) | 99.0% (6942/7012) | 0.6% (43/7012) | 0.50 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 98.9% (20988/21233; 98.7 to 99.0) | 0.2% (25/11573) | 0.4% (40/11573) | 99.0% (6943/7012) | 0.6% (43/7012) | 0.50 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 97.2% (20637/21233; 97.0 to 97.4) | 0.2% (27/11573) | 0.4% (43/11573) | 97.9% (6867/7012) | 0.7% (49/7012) | 0.53 (n=2648) |
| pilot-0.4 | Sidechat | 85.2% (230/270; 80.5 to 88.9) | 3.1% (5/163) | 6.1% (10/163) | 82.7% (67/81) | 8.6% (7/81) | 0.42 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 85.2% (230/270; 80.5 to 88.9) | 3.1% (5/163) | 6.1% (10/163) | 82.7% (67/81) | 8.6% (7/81) | 0.42 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) | 0.50 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 95.3% (49894/52336; 95.2 to 95.5) | 0.4% (161/44528) | 1.6% (707/44528) | 79.8% (6234/7808) | 17.9% (1396/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 98.6% (15574/15793; 98.4 to 98.8) | 0.4% (61/15793) | 1.0% (158/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 100.0% (8874/8875; 99.9 to 100.0) | 0.0% (0/8875) | 0.0% (1/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 100.0% (10432/10434; 99.9 to 100.0) | 0.0% (0/10434) | 0.0% (2/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |
| gen-0.2.test@anonymous | Sidechat | 98.7% (15947/16158; 98.5 to 98.9) | 0.4% (45/10269) | 0.4% (40/10269) | 98.5% (4332/4397) | 0.7% (31/4397) | 0.50 (n=1492) |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +18.1 (+16.6 to +19.5), better on 2882 lines
- generated test @named: +17.6 (+16.2 to +19.0), better on 2882 lines
- pilot-0.4: +5.2 (-0.3 to +10.7), within noise on 270 lines
- pilot-0.4@anonymous: +7.4 (+1.8 to +13.0), better on 270 lines
- demo-lines-0.1: +0.0 (-5.8 to +5.8), within noise on 48 lines
- duplex-mpe-0.1: +12.2 (+11.9 to +12.6), better on 52336 lines
- ambient-bench-0.1: +13.3 (+12.7 to +13.8), better on 15793 lines
- ami-addressee-0.1: +14.8 (+14.0 to +15.5), better on 8875 lines
- ami-silent-0.1.test: +9.9 (+9.4 to +10.5), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.005, mean distance to target 0.0117, AUROC 0.9872
- generated test @named: calibration error 0.0051, mean distance to target 0.0116, AUROC 0.9873
- generated test @none: calibration error 0.0065, mean distance to target 0.0207, AUROC 0.987
- pilot-0.4: calibration error 0.0563, mean distance to target 0.0955, AUROC 0.9505
- pilot-0.4@anonymous: calibration error 0.0569, mean distance to target 0.0957, AUROC 0.9501
- demo-lines-0.1: calibration error 0.0393, mean distance to target 0.0394, AUROC 1.0
- duplex-mpe-0.1: calibration error 0.0281, mean distance to target 0.0416, AUROC 0.9754
- ambient-bench-0.1: calibration error 0.0178, mean distance to target 0.0325
- ami-addressee-0.1: calibration error 0.0002, mean distance to target 0.0002
- ami-silent-0.1.test: calibration error 0.0002, mean distance to target 0.0002
- gen-0.2.test@anonymous: calibration error 0.0058, mean distance to target 0.013, AUROC 0.9859

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 98.7% (10131/10264) | 0.2% (14/5635) | 98.9% (3306/3342) |
| `o` | 98.9% (5636/5697) | 0.2% (5/3090) | 99.1% (1869/1886) |
| `c` | 98.6% (2644/2681) | 0.3% (4/1464) | 98.5% (871/884) |
| `a` | 99.3% (2574/2591) | 0.1% (2/1384) | 99.6% (896/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 99.0% (8232/8312) | 0.2% (9/4509) | 99.2% (2745/2766) |
| `writer` | 98.7% (5581/5653) | 0.2% (7/3151) | 98.9% (1777/1797) |
| `agent_name,writer` | 98.6% (3476/3524) | 0.3% (5/1894) | 98.9% (1153/1166) |
| `agent_name` | 98.6% (2158/2188) | 0.2% (2/1186) | 98.8% (729/738) |
| `setting,writer` | 99.3% (696/701) | 0.0% (0/393) | 99.6% (235/236) |
| `setting,agent_name,writer` | 97.9% (378/386) | 1.0% (2/197) | 98.6% (141/143) |
| `setting` | 98.9% (279/282) | 0.0% (0/138) | 97.5% (116/119) |
| `setting,agent_name` | 98.9% (185/187) | 0.0% (0/105) | 97.9% (46/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.4% (8854/8999) | 0.3% (21/7292) | n/a |
| `G6` | 97.7% (4027/4120) | 0.0% (0/318) | 97.8% (2953/3021) |
| `G2` | 100.0% (3745/3747) | 0.5% (1/181) | 100.0% (3565/3566) |
| `G4` | 99.7% (1763/1768) | 0.0% (0/1183) | 99.8% (424/425) |
| `G3` | 100.0% (2113/2114) | 0.1% (1/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.7% (151/153) | 1.3% (2/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 99.4% (13959/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 99.3% (13952/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.7% (3258/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.8% (3261/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 89.3% (2717/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 89.3% (2714/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 99.7% (1993/2000) | 99.2% (1983/2000) | 99.7% (1993/2000) | 99.2% (1983/2000) |
| `implicit/T` | 23.0% (460/2000) | 26.6% (531/2000) | 23.0% (460/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.3% (1891/1904) | 98.8% (1882/1904) | 99.3% (1891/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 99.4% (1899/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.3% (1890/1904) | 99.0% (1884/1904) | 99.3% (1890/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 99.4% (1900/1911) | 99.5% (1902/1911) | n/a | n/a |

## ettin-150m

Run `side-r2-ettin-150m-s0`. Best epoch 2 of 2; history [{'epoch': 1, 'train_loss': 0.4285, 'dev_loss': 0.2139, 'secs': 716}, {'epoch': 2, 'train_loss': 0.255, 'dev_loss': 0.2038, 'secs': 1366}]. Temperatures {'intent': 1.35, 'respond': 1.35, 'unclear': 1.25}. 236439 training rows, 6000 dev rows, 1417 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.4 (20788/20988 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 98.9% (20989/21233; 98.7 to 99.0) | 0.2% (23/11573) | 0.2% (27/11573) | 98.9% (6932/7012) | 0.6% (41/7012) | 0.50 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 98.9% (20989/21233; 98.7 to 99.0) | 0.2% (24/11573) | 0.2% (27/11573) | 98.9% (6935/7012) | 0.6% (40/7012) | 0.50 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 97.2% (20634/21233; 97.0 to 97.4) | 0.2% (24/11573) | 0.3% (30/11573) | 98.0% (6868/7012) | 0.7% (48/7012) | 0.53 (n=2648) |
| pilot-0.4 | Sidechat | 86.3% (233/270; 81.7 to 89.9) | 3.7% (6/163) | 4.9% (8/163) | 84.0% (68/81) | 6.2% (5/81) | 0.42 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 86.3% (233/270; 81.7 to 89.9) | 3.7% (6/163) | 4.9% (8/163) | 84.0% (68/81) | 7.4% (6/81) | 0.42 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) | 0.50 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 95.5% (49963/52336; 95.3 to 95.6) | 0.6% (279/44528) | 1.5% (675/44528) | 81.8% (6389/7808) | 14.8% (1157/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 98.8% (15597/15793; 98.6 to 98.9) | 0.3% (46/15793) | 0.9% (150/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 99.9% (8865/8875; 99.8 to 99.9) | 0.0% (0/8875) | 0.1% (10/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 100.0% (10430/10434; 99.9 to 100.0) | 0.0% (0/10434) | 0.0% (4/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |
| gen-0.2.test@anonymous | Sidechat | 98.8% (15970/16158; 98.7 to 99.0) | 0.3% (31/10269) | 0.3% (31/10269) | 98.5% (4333/4397) | 0.8% (33/4397) | 0.50 (n=1492) |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +18.1 (+16.7 to +19.6), better on 2882 lines
- generated test @named: +17.6 (+16.2 to +19.1), better on 2882 lines
- pilot-0.4: +6.3 (+1.0 to +11.6), better on 270 lines
- pilot-0.4@anonymous: +8.5 (+3.0 to +14.0), better on 270 lines
- demo-lines-0.1: +0.0 (-5.8 to +5.8), within noise on 48 lines
- duplex-mpe-0.1: +12.4 (+12.0 to +12.7), better on 52336 lines
- ambient-bench-0.1: +13.4 (+12.9 to +14.0), better on 15793 lines
- ami-addressee-0.1: +14.7 (+13.9 to +15.4), better on 8875 lines
- ami-silent-0.1.test: +9.9 (+9.3 to +10.5), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0043, mean distance to target 0.0119, AUROC 0.979
- generated test @named: calibration error 0.0042, mean distance to target 0.0118, AUROC 0.9791
- generated test @none: calibration error 0.0055, mean distance to target 0.0207, AUROC 0.979
- pilot-0.4: calibration error 0.0645, mean distance to target 0.0962, AUROC 0.9495
- pilot-0.4@anonymous: calibration error 0.065, mean distance to target 0.0966, AUROC 0.9488
- demo-lines-0.1: calibration error 0.0431, mean distance to target 0.0431, AUROC 1.0
- duplex-mpe-0.1: calibration error 0.02, mean distance to target 0.0422, AUROC 0.9838
- ambient-bench-0.1: calibration error 0.0149, mean distance to target 0.03
- ami-addressee-0.1: calibration error 0.0009, mean distance to target 0.0009
- ami-silent-0.1.test: calibration error 0.0006, mean distance to target 0.0006
- gen-0.2.test@anonymous: calibration error 0.0049, mean distance to target 0.0124, AUROC 0.9759

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 98.7% (10127/10264) | 0.2% (10/5635) | 98.7% (3297/3342) |
| `o` | 98.9% (5633/5697) | 0.2% (7/3090) | 98.9% (1865/1886) |
| `c` | 98.9% (2651/2681) | 0.3% (5/1464) | 99.0% (875/884) |
| `a` | 99.5% (2578/2591) | 0.1% (1/1384) | 99.4% (895/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 99.0% (8231/8312) | 0.3% (12/4509) | 99.1% (2741/2766) |
| `writer` | 98.8% (5587/5653) | 0.1% (3/3151) | 98.9% (1778/1797) |
| `agent_name,writer` | 98.4% (3468/3524) | 0.4% (7/1894) | 98.5% (1149/1166) |
| `agent_name` | 99.0% (2167/2188) | 0.1% (1/1186) | 99.2% (732/738) |
| `setting,writer` | 99.0% (694/701) | 0.0% (0/393) | 97.9% (231/236) |
| `setting,agent_name,writer` | 97.9% (378/386) | 0.0% (0/197) | 97.2% (139/143) |
| `setting` | 99.3% (280/282) | 0.0% (0/138) | 98.3% (117/119) |
| `setting,agent_name` | 98.4% (184/187) | 0.0% (0/105) | 95.7% (45/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.6% (8873/8999) | 0.2% (18/7292) | n/a |
| `G6` | 97.4% (4014/4120) | 0.0% (0/318) | 97.4% (2942/3021) |
| `G2` | 100.0% (3746/3747) | 0.0% (0/181) | 100.0% (3565/3566) |
| `G4` | 99.6% (1761/1768) | 0.2% (3/1183) | 100.0% (425/425) |
| `G3` | 99.9% (2112/2114) | 0.1% (1/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.7% (151/153) | 0.7% (1/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 99.6% (13984/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 99.6% (13983/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.9% (3262/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.9% (3263/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 91.0% (2768/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 91.0% (2764/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 99.7% (1993/2000) | 99.2% (1983/2000) | 99.7% (1993/2000) | 99.2% (1983/2000) |
| `implicit/T` | 30.9% (618/2000) | 26.6% (531/2000) | 30.9% (618/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.2% (1889/1904) | 98.8% (1882/1904) | 99.2% (1889/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 92.9% (1776/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.2% (1889/1904) | 99.0% (1884/1904) | 99.2% (1889/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 92.8% (1774/1911) | 99.5% (1902/1911) | n/a | n/a |
