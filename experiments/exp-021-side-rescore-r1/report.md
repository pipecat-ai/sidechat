# Training run: exp-021-side-rescore-r1

Every number below is measured in this run. A share is `value (k/n)`; headline shares also give a 95% interval.

## ettin-32m

Run `side-r1-ettin-32m-s0`. Best epoch 2 of 3; history [{'epoch': 1, 'train_loss': 0.6555, 'dev_loss': 0.3331, 'secs': 142}, {'epoch': 2, 'train_loss': 0.3576, 'dev_loss': 0.3207, 'secs': 267}, {'epoch': 3, 'train_loss': 0.2897, 'dev_loss': 0.3393, 'secs': 391}]. Temperatures {'intent': 1.3, 'respond': 1.45, 'unclear': 1.4}. 89995 training rows, 6000 dev rows, 0 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.8, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.8 (8354/8733 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 95.0% (20179/21233; 94.7 to 95.3) | 0.1% (14/11573) | 0.5% (53/11573) | 88.8% (6224/7012) | 1.1% (77/7012) | 0.50 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 95.0% (20180/21233; 94.7 to 95.3) | 0.1% (15/11573) | 0.5% (53/11573) | 88.8% (6225/7012) | 1.1% (76/7012) | 0.50 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 93.2% (19794/21233; 92.9 to 93.5) | 0.2% (21/11573) | 0.4% (49/11573) | 84.5% (5924/7012) | 1.7% (117/7012) | 0.53 (n=2648) |
| pilot-0.4 | Sidechat | 81.1% (219/270; 76.0 to 85.3) | 2.5% (4/163) | 6.8% (11/163) | 66.7% (54/81) | 14.8% (12/81) | 0.49 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 81.1% (219/270; 76.0 to 85.3) | 2.5% (4/163) | 6.8% (11/163) | 66.7% (54/81) | 14.8% (12/81) | 0.49 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 91.7% (44/48; 80.5 to 96.7) | 0.0% (0/26) | 0.0% (0/26) | 79.0% (15/19) | 0.0% (0/19) | 0.51 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 94.6% (49512/52336; 94.4 to 94.8) | 0.5% (209/44528) | 1.9% (859/44528) | 77.5% (6052/7808) | 16.4% (1279/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 95.6% (15093/15793; 95.2 to 95.9) | 1.0% (159/15793) | 3.4% (541/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 96.0% (8519/8875; 95.6 to 96.4) | 1.0% (85/8875) | 3.0% (271/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 97.2% (10140/10434; 96.9 to 97.5) | 0.6% (60/10434) | 2.2% (234/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +14.1 (+12.6 to +15.7), better on 2882 lines
- generated test @named: +13.7 (+12.2 to +15.3), better on 2882 lines
- pilot-0.4: +1.1 (-4.7 to +7.0), within noise on 270 lines
- pilot-0.4@anonymous: +3.3 (-2.5 to +9.2), within noise on 270 lines
- demo-lines-0.1: -6.2 (-15.2 to +2.7), within noise on 48 lines
- duplex-mpe-0.1: +11.5 (+11.2 to +11.8), better on 52336 lines
- ambient-bench-0.1: +10.2 (+9.7 to +10.8), better on 15793 lines
- ami-addressee-0.1: +10.8 (+10.0 to +11.5), better on 8875 lines
- ami-silent-0.1.test: +7.1 (+6.6 to +7.7), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0056, mean distance to target 0.0197, AUROC 0.9838
- generated test @named: calibration error 0.0055, mean distance to target 0.0197, AUROC 0.9839
- generated test @none: calibration error 0.0103, mean distance to target 0.0304, AUROC 0.9821
- pilot-0.4: calibration error 0.059, mean distance to target 0.1179, AUROC 0.9435
- pilot-0.4@anonymous: calibration error 0.0589, mean distance to target 0.1181, AUROC 0.9433
- demo-lines-0.1: calibration error 0.0528, mean distance to target 0.0539, AUROC 0.9927
- duplex-mpe-0.1: calibration error 0.0205, mean distance to target 0.0525, AUROC 0.9703
- ambient-bench-0.1: calibration error 0.0376, mean distance to target 0.0691
- ami-addressee-0.1: calibration error 0.0459, mean distance to target 0.0459
- ami-silent-0.1.test: calibration error 0.0327, mean distance to target 0.0327

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 94.6% (9710/10264) | 0.1% (5/5635) | 88.1% (2945/3342) |
| `o` | 95.4% (5434/5697) | 0.1% (2/3090) | 89.7% (1691/1886) |
| `c` | 95.2% (2551/2681) | 0.3% (4/1464) | 88.3% (781/884) |
| `a` | 95.9% (2484/2591) | 0.2% (3/1384) | 89.7% (807/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 95.5% (7937/8312) | 0.2% (7/4509) | 89.4% (2472/2766) |
| `writer` | 94.8% (5359/5653) | 0.1% (4/3151) | 88.1% (1583/1797) |
| `agent_name,writer` | 94.3% (3324/3524) | 0.1% (1/1894) | 88.3% (1030/1166) |
| `agent_name` | 95.4% (2087/2188) | 0.2% (2/1186) | 89.8% (663/738) |
| `setting,writer` | 94.6% (663/701) | 0.0% (0/393) | 86.9% (205/236) |
| `setting,agent_name,writer` | 94.3% (364/386) | 0.0% (0/197) | 88.8% (127/143) |
| `setting` | 94.0% (265/282) | 0.0% (0/138) | 86.6% (103/119) |
| `setting,agent_name` | 96.3% (180/187) | 0.0% (0/105) | 87.2% (41/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.2% (8841/8999) | 0.2% (12/7292) | n/a |
| `G6` | 93.9% (3870/4120) | 0.0% (0/318) | 94.8% (2864/3021) |
| `G2` | 94.5% (3540/3747) | 0.0% (0/181) | 94.2% (3360/3566) |
| `G4` | 75.4% (1333/1768) | 0.1% (1/1183) | 0.0% (0/425) |
| `G3` | 100.0% (2113/2114) | 0.0% (0/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.0% (150/153) | 0.7% (1/153) | n/a |
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
| `explicit/T` | 96.2% (1925/2000) | 99.2% (1983/2000) | 96.2% (1925/2000) | 99.2% (1983/2000) |
| `implicit/T` | 17.8% (356/2000) | 26.6% (531/2000) | 17.8% (356/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.2% (1888/1904) | 98.8% (1882/1904) | 99.2% (1888/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 95.2% (1819/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 98.9% (1883/1904) | 99.0% (1884/1904) | 98.9% (1883/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 94.7% (1809/1911) | 99.5% (1902/1911) | n/a | n/a |

## ettin-68m

Run `side-r1-ettin-68m-s0`. Best epoch 2 of 3; history [{'epoch': 1, 'train_loss': 0.6158, 'dev_loss': 0.3204, 'secs': 184}, {'epoch': 2, 'train_loss': 0.3375, 'dev_loss': 0.3098, 'secs': 349}, {'epoch': 3, 'train_loss': 0.2747, 'dev_loss': 0.3302, 'secs': 512}]. Temperatures {'intent': 1.4, 'respond': 1.45, 'unclear': 1.35}. 89995 training rows, 6000 dev rows, 0 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.8 (8551/8733 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 97.6% (20728/21233; 97.4 to 97.8) | 0.3% (33/11573) | 0.2% (29/11573) | 95.8% (6715/7012) | 1.0% (69/7012) | 0.50 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 97.6% (20726/21233; 97.4 to 97.8) | 0.3% (33/11573) | 0.3% (30/11573) | 95.8% (6714/7012) | 1.0% (68/7012) | 0.50 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 96.0% (20389/21233; 95.8 to 96.3) | 0.4% (46/11573) | 0.4% (42/11573) | 94.0% (6593/7012) | 1.1% (74/7012) | 0.52 (n=2648) |
| pilot-0.4 | Sidechat | 81.8% (221/270; 76.8 to 86.0) | 4.9% (8/163) | 6.1% (10/163) | 72.8% (59/81) | 8.6% (7/81) | 0.48 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 81.8% (221/270; 76.8 to 86.0) | 4.9% (8/163) | 6.1% (10/163) | 72.8% (59/81) | 8.6% (7/81) | 0.48 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 95.8% (46/48; 86.0 to 98.9) | 0.0% (0/26) | 0.0% (0/26) | 89.5% (17/19) | 0.0% (0/19) | 0.51 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 96.7% (50581/52336; 96.5 to 96.8) | 0.8% (374/44528) | 1.2% (552/44528) | 89.4% (6979/7808) | 8.9% (694/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 96.7% (15267/15793; 96.4 to 96.9) | 1.1% (169/15793) | 2.3% (357/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 97.8% (8681/8875; 97.5 to 98.1) | 0.8% (68/8875) | 1.4% (126/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 98.5% (10273/10434; 98.2 to 98.7) | 0.5% (57/10434) | 1.0% (104/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +16.8 (+15.3 to +18.3), better on 2882 lines
- generated test @named: +16.3 (+14.8 to +17.8), better on 2882 lines
- pilot-0.4: +1.8 (-3.6 to +7.3), within noise on 270 lines
- pilot-0.4@anonymous: +4.1 (-1.4 to +9.5), within noise on 270 lines
- demo-lines-0.1: -2.1 (-9.1 to +5.0), within noise on 48 lines
- duplex-mpe-0.1: +13.5 (+13.2 to +13.9), better on 52336 lines
- ambient-bench-0.1: +11.3 (+10.8 to +11.8), better on 15793 lines
- ami-addressee-0.1: +12.6 (+11.9 to +13.3), better on 8875 lines
- ami-silent-0.1.test: +8.4 (+7.9 to +9.0), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0069, mean distance to target 0.0168, AUROC 0.9792
- generated test @named: calibration error 0.0068, mean distance to target 0.0168, AUROC 0.9793
- generated test @none: calibration error 0.0101, mean distance to target 0.0274, AUROC 0.9788
- pilot-0.4: calibration error 0.0747, mean distance to target 0.1134, AUROC 0.9261
- pilot-0.4@anonymous: calibration error 0.0761, mean distance to target 0.1134, AUROC 0.9259
- demo-lines-0.1: calibration error 0.0443, mean distance to target 0.0443, AUROC 0.9891
- duplex-mpe-0.1: calibration error 0.0139, mean distance to target 0.0355, AUROC 0.986
- ambient-bench-0.1: calibration error 0.0239, mean distance to target 0.0459
- ami-addressee-0.1: calibration error 0.0222, mean distance to target 0.0222
- ami-silent-0.1.test: calibration error 0.0152, mean distance to target 0.0152

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 97.4% (9993/10264) | 0.3% (17/5635) | 95.4% (3187/3342) |
| `o` | 97.7% (5565/5697) | 0.3% (9/3090) | 96.0% (1810/1886) |
| `c` | 97.7% (2618/2681) | 0.4% (6/1464) | 95.7% (846/884) |
| `a` | 98.5% (2552/2591) | 0.1% (1/1384) | 96.9% (872/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 98.0% (8147/8312) | 0.2% (10/4509) | 96.4% (2667/2766) |
| `writer` | 97.5% (5510/5653) | 0.3% (9/3151) | 95.4% (1715/1797) |
| `agent_name,writer` | 97.2% (3425/3524) | 0.3% (5/1894) | 95.4% (1112/1166) |
| `agent_name` | 97.4% (2131/2188) | 0.5% (6/1186) | 95.5% (705/738) |
| `setting,writer` | 97.7% (685/701) | 0.2% (1/393) | 95.3% (225/236) |
| `setting,agent_name,writer` | 96.6% (373/386) | 1.0% (2/197) | 94.4% (135/143) |
| `setting` | 97.2% (274/282) | 0.0% (0/138) | 94.1% (112/119) |
| `setting,agent_name` | 97.9% (183/187) | 0.0% (0/105) | 93.6% (44/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.3% (8844/8999) | 0.4% (31/7292) | n/a |
| `G6` | 96.3% (3968/4120) | 0.0% (0/318) | 96.5% (2915/3021) |
| `G2` | 94.9% (3557/3747) | 0.0% (0/181) | 94.7% (3376/3566) |
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

Run `side-r1-ettin-150m-s0`. Best epoch 2 of 3; history [{'epoch': 1, 'train_loss': 0.5978, 'dev_loss': 0.3279, 'secs': 255}, {'epoch': 2, 'train_loss': 0.3325, 'dev_loss': 0.2988, 'secs': 465}, {'epoch': 3, 'train_loss': 0.2679, 'dev_loss': 0.3134, 'secs': 678}]. Temperatures {'intent': 1.25, 'respond': 1.45, 'unclear': 1.2}. 89995 training rows, 6000 dev rows, 0 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.85, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.6 (8380/8733 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 95.6% (20304/21233; 95.3 to 95.9) | 0.2% (22/11573) | 0.3% (32/11573) | 89.3% (6264/7012) | 1.0% (71/7012) | 0.49 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 95.6% (20307/21233; 95.4 to 95.9) | 0.2% (22/11573) | 0.3% (32/11573) | 89.3% (6265/7012) | 1.0% (70/7012) | 0.49 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 93.8% (19919/21233; 93.5 to 94.1) | 0.2% (22/11573) | 0.4% (45/11573) | 84.3% (5912/7012) | 1.0% (69/7012) | 0.52 (n=2648) |
| pilot-0.4 | Sidechat | 82.2% (222/270; 77.2 to 86.3) | 1.8% (3/163) | 8.0% (13/163) | 70.4% (57/81) | 6.2% (5/81) | 0.48 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 81.8% (221/270; 76.8 to 86.0) | 1.8% (3/163) | 8.0% (13/163) | 69.1% (56/81) | 6.2% (5/81) | 0.48 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 89.6% (43/48; 77.8 to 95.5) | 0.0% (0/26) | 3.9% (1/26) | 79.0% (15/19) | 0.0% (0/19) | 0.49 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 95.8% (50153/52336; 95.7 to 96.0) | 0.4% (172/44528) | 1.6% (705/44528) | 83.3% (6502/7808) | 9.3% (726/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 96.4% (15228/15793; 96.1 to 96.7) | 0.6% (89/15793) | 3.0% (476/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 97.0% (8612/8875; 96.7 to 97.4) | 0.5% (46/8875) | 2.5% (217/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 97.9% (10214/10434; 97.6 to 98.2) | 0.4% (40/10434) | 1.7% (180/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +15.0 (+13.5 to +16.6), better on 2882 lines
- generated test @named: +14.5 (+13.0 to +16.1), better on 2882 lines
- pilot-0.4: +2.2 (-3.2 to +7.6), within noise on 270 lines
- pilot-0.4@anonymous: +4.1 (-1.5 to +9.6), within noise on 270 lines
- demo-lines-0.1: -8.3 (-18.1 to +1.4), within noise on 48 lines
- duplex-mpe-0.1: +12.7 (+12.4 to +13.1), better on 52336 lines
- ambient-bench-0.1: +11.1 (+10.5 to +11.6), better on 15793 lines
- ami-addressee-0.1: +11.8 (+11.1 to +12.5), better on 8875 lines
- ami-silent-0.1.test: +7.8 (+7.3 to +8.4), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0084, mean distance to target 0.0174, AUROC 0.9854
- generated test @named: calibration error 0.0084, mean distance to target 0.0174, AUROC 0.9854
- generated test @none: calibration error 0.0099, mean distance to target 0.0269, AUROC 0.9851
- pilot-0.4: calibration error 0.0488, mean distance to target 0.1055, AUROC 0.9424
- pilot-0.4@anonymous: calibration error 0.0488, mean distance to target 0.1054, AUROC 0.9423
- demo-lines-0.1: calibration error 0.0293, mean distance to target 0.0495, AUROC 0.9855
- duplex-mpe-0.1: calibration error 0.0111, mean distance to target 0.036, AUROC 0.9896
- ambient-bench-0.1: calibration error 0.0223, mean distance to target 0.0482
- ami-addressee-0.1: calibration error 0.0304, mean distance to target 0.0304
- ami-silent-0.1.test: calibration error 0.0209, mean distance to target 0.0209

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 95.5% (9804/10264) | 0.2% (10/5635) | 89.2% (2981/3342) |
| `o` | 95.9% (5462/5697) | 0.2% (5/3090) | 89.7% (1691/1886) |
| `c` | 95.2% (2553/2681) | 0.3% (5/1464) | 88.9% (786/884) |
| `a` | 95.9% (2485/2591) | 0.1% (2/1384) | 89.6% (806/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 95.7% (7956/8312) | 0.2% (9/4509) | 89.4% (2472/2766) |
| `writer` | 95.8% (5414/5653) | 0.1% (3/3151) | 89.4% (1606/1797) |
| `agent_name,writer` | 95.2% (3355/3524) | 0.3% (6/1894) | 89.3% (1041/1166) |
| `agent_name` | 96.0% (2100/2188) | 0.2% (2/1186) | 90.2% (666/738) |
| `setting,writer` | 95.2% (667/701) | 0.0% (0/393) | 87.7% (207/236) |
| `setting,agent_name,writer` | 95.3% (368/386) | 0.5% (1/197) | 88.8% (127/143) |
| `setting` | 93.6% (264/282) | 0.7% (1/138) | 86.6% (103/119) |
| `setting,agent_name` | 96.3% (180/187) | 0.0% (0/105) | 89.4% (42/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.6% (8877/8999) | 0.2% (16/7292) | n/a |
| `G6` | 95.9% (3952/4120) | 0.0% (0/318) | 96.0% (2900/3021) |
| `G2` | 94.6% (3545/3747) | 0.0% (0/181) | 94.3% (3364/3566) |
| `G4` | 75.6% (1336/1768) | 0.2% (3/1183) | 0.0% (0/425) |
| `G3` | 99.9% (2112/2114) | 0.1% (1/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.0% (150/153) | 1.3% (2/153) | n/a |
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
| `explicit/T` | 98.5% (1969/2000) | 99.2% (1983/2000) | 98.5% (1969/2000) | 99.2% (1983/2000) |
| `implicit/T` | 37.7% (754/2000) | 26.6% (531/2000) | 37.7% (754/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.3% (1891/1904) | 98.8% (1882/1904) | 99.3% (1891/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 91.3% (1744/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.2% (1888/1904) | 99.0% (1884/1904) | 99.2% (1888/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 91.1% (1741/1911) | 99.5% (1902/1911) | n/a | n/a |
