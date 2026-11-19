# Training run: exp-031-side-train-r5-s1

Every number below is measured in this run. A share is `value (k/n)`; headline shares also give a 95% interval.

## ettin-150m

Run `side-r5-ettin-150m-s1`. Best epoch 2 of 2; history [{'epoch': 1, 'train_loss': 0.4272, 'dev_loss': 0.2867, 'secs': 776}, {'epoch': 2, 'train_loss': 0.2666, 'dev_loss': 0.285, 'secs': 1501}]. Temperatures {'intent': 1.55, 'respond': 1.6, 'unclear': 1.6}. 322717 training rows, 6000 dev rows, 1537 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.65, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.4 (29904/30248 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 98.5% (20911/21233; 98.3 to 98.6) | 0.1% (16/11573) | 0.3% (37/11573) | 97.4% (6830/7012) | 0.5% (37/7012) | 0.50 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 98.5% (20910/21233; 98.3 to 98.6) | 0.1% (16/11573) | 0.3% (36/11573) | 97.4% (6828/7012) | 0.5% (37/7012) | 0.50 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 97.1% (20609/21233; 96.8 to 97.3) | 0.2% (28/11573) | 0.4% (44/11573) | 95.8% (6714/7012) | 0.6% (43/7012) | 0.53 (n=2648) |
| pilot-0.4 | Sidechat | 86.7% (234/270; 82.1 to 90.2) | 4.3% (7/163) | 4.3% (7/163) | 84.0% (68/81) | 6.2% (5/81) | 0.47 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 86.7% (234/270; 82.1 to 90.2) | 4.3% (7/163) | 4.3% (7/163) | 84.0% (68/81) | 4.9% (4/81) | 0.48 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) | 0.50 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 95.8% (50148/52336; 95.6 to 96.0) | 0.6% (258/44528) | 1.4% (613/44528) | 83.1% (6491/7808) | 12.1% (946/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 96.0% (15153/15793; 95.6 to 96.2) | 1.6% (248/15793) | 2.5% (392/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 98.9% (8773/8875; 98.6 to 99.1) | 0.3% (30/8875) | 0.8% (72/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 99.1% (10336/10434; 98.9 to 99.2) | 0.3% (29/10434) | 0.7% (69/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |
| gen-0.2.test@anonymous | Sidechat | 98.5% (15921/16158; 98.3 to 98.7) | 0.3% (35/10269) | 0.4% (41/10269) | 97.5% (4289/4397) | 0.7% (31/4397) | 0.50 (n=1492) |
| gen-0.3.test@anonymous | Sidechat | 98.8% (12271/12426; 98.5 to 98.9) | 0.3% (22/7881) | 0.2% (17/7881) | 97.6% (3088/3164) | 0.7% (22/3164) | 0.50 (n=1381) |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +17.7 (+16.2 to +19.2), better on 2882 lines
- generated test @named: +17.2 (+15.7 to +18.7), better on 2882 lines
- pilot-0.4: +6.7 (+1.4 to +11.9), better on 270 lines
- pilot-0.4@anonymous: +8.9 (+3.6 to +14.2), better on 270 lines
- demo-lines-0.1: +0.0 (-5.8 to +5.8), within noise on 48 lines
- duplex-mpe-0.1: +12.7 (+12.4 to +13.0), better on 52336 lines
- ambient-bench-0.1: +10.6 (+10.0 to +11.2), better on 15793 lines
- ami-addressee-0.1: +13.6 (+12.9 to +14.4), better on 8875 lines
- ami-silent-0.1.test: +9.0 (+8.4 to +9.6), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0042, mean distance to target 0.0125, AUROC 0.9809
- generated test @named: calibration error 0.0043, mean distance to target 0.0125, AUROC 0.981
- generated test @none: calibration error 0.0064, mean distance to target 0.0222, AUROC 0.9809
- pilot-0.4: calibration error 0.0521, mean distance to target 0.0928, AUROC 0.9502
- pilot-0.4@anonymous: calibration error 0.0531, mean distance to target 0.0929, AUROC 0.9498
- demo-lines-0.1: calibration error 0.0391, mean distance to target 0.0391, AUROC 1.0
- duplex-mpe-0.1: calibration error 0.0143, mean distance to target 0.0389, AUROC 0.9883
- ambient-bench-0.1: calibration error 0.0294, mean distance to target 0.058
- ami-addressee-0.1: calibration error 0.0147, mean distance to target 0.0147
- ami-silent-0.1.test: calibration error 0.0117, mean distance to target 0.0117
- gen-0.2.test@anonymous: calibration error 0.0051, mean distance to target 0.014, AUROC 0.9772
- gen-0.3.test@anonymous: calibration error 0.0045, mean distance to target 0.0128, AUROC 0.9789

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 98.1% (10068/10264) | 0.1% (5/5635) | 96.3% (3219/3342) |
| `o` | 98.8% (5629/5697) | 0.2% (5/3090) | 98.4% (1855/1886) |
| `c` | 98.5% (2641/2681) | 0.3% (5/1464) | 98.1% (867/884) |
| `a` | 99.3% (2573/2591) | 0.1% (1/1384) | 98.8% (889/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 98.9% (8216/8312) | 0.2% (9/4509) | 98.4% (2722/2766) |
| `writer` | 98.1% (5546/5653) | 0.1% (2/3151) | 96.3% (1730/1797) |
| `agent_name,writer` | 98.0% (3453/3524) | 0.2% (3/1894) | 96.4% (1124/1166) |
| `agent_name` | 98.9% (2164/2188) | 0.2% (2/1186) | 98.5% (727/738) |
| `setting,writer` | 98.3% (689/701) | 0.0% (0/393) | 96.2% (227/236) |
| `setting,agent_name,writer` | 98.5% (380/386) | 0.0% (0/197) | 96.5% (138/143) |
| `setting` | 99.3% (280/282) | 0.0% (0/138) | 98.3% (117/119) |
| `setting,agent_name` | 97.9% (183/187) | 0.0% (0/105) | 95.7% (45/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.7% (8884/8999) | 0.2% (12/7292) | n/a |
| `G6` | 97.9% (4034/4120) | 0.3% (1/318) | 97.8% (2953/3021) |
| `G2` | 99.2% (3717/3747) | 1.1% (2/181) | 99.2% (3538/3566) |
| `G4` | 95.0% (1679/1768) | 0.0% (0/1183) | 79.8% (339/425) |
| `G3` | 100.0% (2114/2114) | 0.0% (0/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.7% (151/153) | 0.7% (1/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 99.4% (13961/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 99.3% (13952/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.9% (3262/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.9% (3262/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 92.8% (2823/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 93.1% (2828/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 99.4% (1988/2000) | 99.2% (1983/2000) | 99.4% (1988/2000) | 99.2% (1983/2000) |
| `implicit/T` | 36.0% (721/2000) | 26.6% (531/2000) | 36.0% (721/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.3% (1891/1904) | 98.8% (1882/1904) | 99.3% (1891/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 93.1% (1779/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.3% (1891/1904) | 99.0% (1884/1904) | 99.3% (1891/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 93.7% (1790/1911) | 99.5% (1902/1911) | n/a | n/a |
