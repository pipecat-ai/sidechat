# Training run: exp-029-side-train-r4-s1

Every number below is measured in this run. A share is `value (k/n)`; headline shares also give a 95% interval.

## ettin-150m

Run `side-r4-ettin-150m-s1`. Best epoch 2 of 2; history [{'epoch': 1, 'train_loss': 0.4177, 'dev_loss': 0.2583, 'secs': 993}, {'epoch': 2, 'train_loss': 0.2585, 'dev_loss': 0.2321, 'secs': 1927}]. Temperatures {'intent': 1.5, 'respond': 1.45, 'unclear': 1.45}. 337993 training rows, 6000 dev rows, 1964 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.4 or `intent.open` ≥ 0.7 (29971/30248 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 99.1% (21031/21233; 98.9 to 99.2) | 0.2% (21/11573) | 0.2% (25/11573) | 99.2% (6958/7012) | 0.5% (36/7012) | 0.50 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 99.1% (21033/21233; 98.9 to 99.2) | 0.2% (21/11573) | 0.2% (25/11573) | 99.2% (6957/7012) | 0.5% (36/7012) | 0.50 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 97.5% (20701/21233; 97.3 to 97.7) | 0.2% (28/11573) | 0.2% (29/11573) | 98.3% (6893/7012) | 0.6% (40/7012) | 0.53 (n=2648) |
| pilot-0.4 | Sidechat | 87.8% (237/270; 83.3 to 91.2) | 3.1% (5/163) | 3.7% (6/163) | 86.4% (70/81) | 6.2% (5/81) | 0.40 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 87.8% (237/270; 83.3 to 91.2) | 3.1% (5/163) | 3.7% (6/163) | 86.4% (70/81) | 6.2% (5/81) | 0.40 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) | 0.50 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 95.2% (49823/52336; 95.0 to 95.4) | 0.8% (341/44528) | 1.6% (698/44528) | 81.1% (6334/7808) | 15.6% (1220/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 98.9% (15619/15793; 98.7 to 99.1) | 0.2% (30/15793) | 0.9% (144/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 99.9% (8870/8875; 99.9 to 100.0) | 0.0% (0/8875) | 0.1% (5/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 99.9% (10428/10434; 99.9 to 100.0) | 0.0% (0/10434) | 0.1% (6/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |
| gen-0.2.test@anonymous | Sidechat | 98.8% (15964/16158; 98.6 to 99.0) | 0.4% (37/10269) | 0.4% (44/10269) | 98.6% (4337/4397) | 0.7% (32/4397) | 0.50 (n=1492) |
| gen-0.3.test@anonymous | Sidechat | 99.0% (12300/12426; 98.8 to 99.2) | 0.3% (25/7881) | 0.1% (12/7881) | 98.5% (3117/3164) | 0.6% (20/3164) | 0.50 (n=1381) |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +18.4 (+16.9 to +19.9), better on 2882 lines
- generated test @named: +17.9 (+16.5 to +19.4), better on 2882 lines
- pilot-0.4: +7.8 (+2.5 to +13.1), better on 270 lines
- pilot-0.4@anonymous: +10.0 (+4.5 to +15.4), better on 270 lines
- demo-lines-0.1: +0.0 (-5.8 to +5.8), within noise on 48 lines
- duplex-mpe-0.1: +12.1 (+11.8 to +12.4), better on 52336 lines
- ambient-bench-0.1: +13.6 (+13.0 to +14.1), better on 15793 lines
- ami-addressee-0.1: +14.7 (+14.0 to +15.5), better on 8875 lines
- ami-silent-0.1.test: +9.9 (+9.3 to +10.5), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0041, mean distance to target 0.011, AUROC 0.9814
- generated test @named: calibration error 0.0041, mean distance to target 0.011, AUROC 0.9815
- generated test @none: calibration error 0.0047, mean distance to target 0.0208, AUROC 0.98
- pilot-0.4: calibration error 0.0539, mean distance to target 0.0913, AUROC 0.9526
- pilot-0.4@anonymous: calibration error 0.0545, mean distance to target 0.0917, AUROC 0.9517
- demo-lines-0.1: calibration error 0.0417, mean distance to target 0.0417, AUROC 1.0
- duplex-mpe-0.1: calibration error 0.0223, mean distance to target 0.0453, AUROC 0.9757
- ambient-bench-0.1: calibration error 0.0129, mean distance to target 0.032
- ami-addressee-0.1: calibration error 0.0012, mean distance to target 0.0012
- ami-silent-0.1.test: calibration error 0.0009, mean distance to target 0.0009
- gen-0.2.test@anonymous: calibration error 0.0055, mean distance to target 0.0129, AUROC 0.978
- gen-0.3.test@anonymous: calibration error 0.0051, mean distance to target 0.0117, AUROC 0.9803

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 98.9% (10155/10264) | 0.2% (10/5635) | 99.1% (3313/3342) |
| `o` | 99.1% (5646/5697) | 0.1% (4/3090) | 99.3% (1873/1886) |
| `c` | 98.9% (2651/2681) | 0.3% (5/1464) | 99.2% (877/884) |
| `a` | 99.5% (2579/2591) | 0.1% (2/1384) | 99.4% (895/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 99.2% (8243/8312) | 0.2% (10/4509) | 99.4% (2750/2766) |
| `writer` | 99.0% (5596/5653) | 0.2% (5/3151) | 99.2% (1783/1797) |
| `agent_name,writer` | 99.0% (3487/3524) | 0.3% (5/1894) | 99.5% (1160/1166) |
| `agent_name` | 99.1% (2169/2188) | 0.1% (1/1186) | 99.3% (733/738) |
| `setting,writer` | 98.6% (691/701) | 0.0% (0/393) | 97.9% (231/236) |
| `setting,agent_name,writer` | 98.7% (381/386) | 0.0% (0/197) | 97.2% (139/143) |
| `setting` | 98.9% (279/282) | 0.0% (0/138) | 97.5% (116/119) |
| `setting,agent_name` | 98.9% (185/187) | 0.0% (0/105) | 97.9% (46/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.7% (8879/8999) | 0.3% (19/7292) | n/a |
| `G6` | 98.2% (4045/4120) | 0.0% (0/318) | 98.3% (2969/3021) |
| `G2` | 100.0% (3745/3747) | 0.5% (1/181) | 100.0% (3565/3566) |
| `G4` | 99.7% (1763/1768) | 0.1% (1/1183) | 99.8% (424/425) |
| `G3` | 100.0% (2114/2114) | 0.0% (0/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 100.0% (153/153) | 0.0% (0/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 99.4% (13962/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 99.3% (13952/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.8% (3261/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.9% (3263/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 90.1% (2741/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 90.6% (2753/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 99.6% (1991/2000) | 99.2% (1983/2000) | 99.6% (1991/2000) | 99.2% (1983/2000) |
| `implicit/T` | 28.1% (561/2000) | 26.6% (531/2000) | 28.1% (561/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.4% (1892/1904) | 98.8% (1882/1904) | 99.4% (1892/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 92.6% (1769/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.3% (1890/1904) | 99.0% (1884/1904) | 99.3% (1890/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 93.6% (1788/1911) | 99.5% (1902/1911) | n/a | n/a |
