# Training run: exp-030-side-train-r5

Every number below is measured in this run. A share is `value (k/n)`; headline shares also give a 95% interval.

## ettin-150m

Run `side-r5-ettin-150m-s0`. Best epoch 2 of 2; history [{'epoch': 1, 'train_loss': 0.4266, 'dev_loss': 0.2656, 'secs': 814}, {'epoch': 2, 'train_loss': 0.2685, 'dev_loss': 0.2553, 'secs': 1567}]. Temperatures {'intent': 1.5, 'respond': 1.45, 'unclear': 1.45}. 322717 training rows, 6000 dev rows, 1598 s.

Thresholds chosen on dev (anonymous): answer now at `respond` ≥ 0.6, hold at `respond` ≥ 0.45 or `intent.open` ≥ 0.5 (29967/30248 dev decisions right).

| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed | Even calls: mean `respond` |
|---|---|---|---|---|---|---|---|
| generated test @anonymous | Sidechat | 99.0% (21030/21233; 98.9 to 99.2) | 0.2% (22/11573) | 0.2% (19/11573) | 99.2% (6958/7012) | 0.5% (32/7012) | 0.50 (n=2648) |
|  | Jev | 80.7% (2327/2882; 79.3 to 82.1) | 1.3% (21/1584) | 18.8% (298/1584) | 77.7% (743/956) | 7.0% (67/956) |  |
| generated test @named | Sidechat | 99.1% (21031/21233; 98.9 to 99.2) | 0.2% (22/11573) | 0.2% (19/11573) | 99.2% (6958/7012) | 0.5% (32/7012) | 0.50 (n=2648) |
|  | Jev | 81.2% (2341/2882; 79.8 to 82.6) | 1.6% (25/1584) | 18.4% (292/1584) | 79.8% (763/956) | 6.6% (63/956) |  |
| generated test @none | Sidechat | 97.6% (20728/21233; 97.4 to 97.8) | 0.2% (29/11573) | 0.2% (27/11573) | 97.8% (6860/7012) | 0.6% (40/7012) | 0.52 (n=2648) |
| pilot-0.4 | Sidechat | 87.4% (236/270; 82.9 to 90.8) | 3.7% (6/163) | 4.9% (8/163) | 86.4% (70/81) | 7.4% (6/81) | 0.48 (n=26) |
|  | Jev | 80.0% (216/270; 74.8 to 84.3) | 1.8% (3/163) | 17.8% (29/163) | 76.5% (62/81) | 12.3% (10/81) |  |
| pilot-0.4@anonymous | Sidechat | 87.4% (236/270; 82.9 to 90.8) | 3.7% (6/163) | 4.9% (8/163) | 86.4% (70/81) | 7.4% (6/81) | 0.48 (n=26) |
|  | Jev | 77.8% (210/270; 72.5 to 82.3) | 1.8% (3/163) | 18.4% (30/163) | 70.4% (57/81) | 12.3% (10/81) |  |
| demo-lines-0.1 | Sidechat | 100.0% (48/48; 92.6 to 100.0) | 0.0% (0/26) | 0.0% (0/26) | 100.0% (19/19) | 0.0% (0/19) | 0.50 (n=3) |
|  | Jev | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |  |
| duplex-mpe-0.1 | Sidechat | 96.8% (50674/52336; 96.7 to 97.0) | 0.4% (161/44528) | 0.9% (413/44528) | 86.1% (6720/7808) | 11.9% (933/7808) |  |
|  | Jev | 83.1% (43495/52336; 82.8 to 83.4) | 0.4% (182/44528) | 16.0% (7131/44528) | 80.4% (6280/7808) | 0.1% (7/7808) |  |
| ambient-bench-0.1 | Sidechat | 96.8% (15294/15793; 96.6 to 97.1) | 1.6% (251/15793) | 1.6% (248/15793) | n/a | n/a |  |
|  | Jev | 85.4% (13479/15793; 84.8 to 85.9) | 0.1% (13/15793) | 14.6% (2301/15793) | n/a | n/a |  |
| ami-addressee-0.1 | Sidechat | 99.0% (8782/8875; 98.7 to 99.1) | 0.3% (25/8875) | 0.8% (68/8875) | n/a | n/a |  |
|  | Jev | 85.2% (7563/8875; 84.5 to 85.9) | 0.0% (1/8875) | 14.8% (1311/8875) | n/a | n/a |  |
| ami-silent-0.1.test | Sidechat | 99.2% (10356/10434; 99.1 to 99.4) | 0.2% (24/10434) | 0.5% (54/10434) | n/a | n/a |  |
|  | Jev | 90.0% (9395/10434; 89.5 to 90.6) | 0.1% (5/10434) | 9.9% (1034/10434) | n/a | n/a |  |
| gen-0.2.test@anonymous | Sidechat | 98.9% (15974/16158; 98.7 to 99.0) | 0.4% (39/10269) | 0.3% (34/10269) | 98.8% (4345/4397) | 0.6% (28/4397) | 0.50 (n=1492) |
| gen-0.3.test@anonymous | Sidechat | 99.0% (12301/12426; 98.8 to 99.2) | 0.4% (28/7881) | 0.1% (11/7881) | 99.0% (3133/3164) | 0.4% (13/3164) | 0.50 (n=1381) |

**Sidechat against Jev, decision right, same lines** (points, 95% interval)

- generated test @anonymous: +18.3 (+16.9 to +19.8), better on 2882 lines
- generated test @named: +17.8 (+16.4 to +19.3), better on 2882 lines
- pilot-0.4: +7.4 (+2.2 to +12.6), better on 270 lines
- pilot-0.4@anonymous: +9.6 (+4.2 to +15.0), better on 270 lines
- demo-lines-0.1: +2.1 (-2.0 to +6.1), within noise on 48 lines
- duplex-mpe-0.1: +13.7 (+13.4 to +14.0), better on 52336 lines
- ambient-bench-0.1: +11.5 (+10.9 to +12.0), better on 15793 lines
- ami-addressee-0.1: +13.7 (+13.0 to +14.5), better on 8875 lines
- ami-silent-0.1.test: +9.2 (+8.6 to +9.8), better on 10434 lines

**Calibration and ranking**

- generated test @anonymous: calibration error 0.0039, mean distance to target 0.0111, AUROC 0.9794
- generated test @named: calibration error 0.0039, mean distance to target 0.0111, AUROC 0.9794
- generated test @none: calibration error 0.0056, mean distance to target 0.0202, AUROC 0.9786
- pilot-0.4: calibration error 0.0591, mean distance to target 0.0941, AUROC 0.951
- pilot-0.4@anonymous: calibration error 0.059, mean distance to target 0.0939, AUROC 0.9509
- demo-lines-0.1: calibration error 0.0381, mean distance to target 0.0381, AUROC 1.0
- duplex-mpe-0.1: calibration error 0.0143, mean distance to target 0.0328, AUROC 0.9819
- ambient-bench-0.1: calibration error 0.0246, mean distance to target 0.048
- ami-addressee-0.1: calibration error 0.0124, mean distance to target 0.0124
- ami-silent-0.1.test: calibration error 0.0096, mean distance to target 0.0096
- gen-0.2.test@anonymous: calibration error 0.0052, mean distance to target 0.0128, AUROC 0.9757
- gen-0.3.test@anonymous: calibration error 0.0055, mean distance to target 0.0117, AUROC 0.9775

**Generated test, anonymous, by writer (b is held out)**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `b` | 99.0% (10159/10264) | 0.2% (10/5635) | 99.1% (3312/3342) |
| `o` | 99.0% (5641/5697) | 0.2% (6/3090) | 99.4% (1874/1886) |
| `c` | 99.0% (2653/2681) | 0.3% (4/1464) | 99.2% (877/884) |
| `a` | 99.5% (2577/2591) | 0.1% (2/1384) | 99.4% (895/900) |

**Generated test, anonymous, by held-out reason**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `none` | 99.2% (8242/8312) | 0.2% (8/4509) | 99.5% (2751/2766) |
| `writer` | 99.1% (5604/5653) | 0.1% (3/3151) | 99.2% (1783/1797) |
| `agent_name,writer` | 98.8% (3483/3524) | 0.3% (5/1894) | 99.3% (1158/1166) |
| `agent_name` | 99.0% (2166/2188) | 0.2% (3/1186) | 99.3% (733/738) |
| `setting,writer` | 98.9% (693/701) | 0.0% (0/393) | 98.3% (232/236) |
| `setting,agent_name,writer` | 98.2% (379/386) | 1.0% (2/197) | 97.2% (139/143) |
| `setting` | 98.6% (278/282) | 0.7% (1/138) | 97.5% (116/119) |
| `setting,agent_name` | 98.9% (185/187) | 0.0% (0/105) | 97.9% (46/47) |

**Generated test, anonymous, by guide rule**

| Slice | Decision right | For others: answers now | For the agent: answers now |
|---|---|---|---|
| `G7` | 98.8% (8887/8999) | 0.2% (15/7292) | n/a |
| `G6` | 98.1% (4041/4120) | 0.0% (0/318) | 98.2% (2968/3021) |
| `G2` | 100.0% (3745/3747) | 1.1% (2/181) | 100.0% (3566/3566) |
| `G4` | 99.7% (1762/1768) | 0.2% (2/1183) | 99.8% (424/425) |
| `G3` | 99.9% (2112/2114) | 0.1% (2/2114) | n/a |
| `G1` | 100.0% (243/243) | 0.0% (0/243) | n/a |
| `G5` | 98.7% (151/153) | 0.7% (1/153) | n/a |
| `G8` | 100.0% (89/89) | 0.0% (0/89) | n/a |

**Duplex-MPE by condition and event**

| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |
|---|---|---|---|---|
| `implicit/N2` | 99.4% (13967/14047) | 80.5% (11311/14047) | n/a | n/a |
| `explicit/N2` | 99.4% (13962/14045) | 81.1% (11390/14045) | n/a | n/a |
| `explicit/N3` | 99.9% (3263/3267) | 83.2% (2717/3267) | n/a | n/a |
| `implicit/N3` | 99.9% (3262/3267) | 83.3% (2722/3267) | n/a | n/a |
| `explicit/N1` | 93.7% (2848/3041) | 87.0% (2644/3041) | n/a | n/a |
| `implicit/N1` | 94.1% (2861/3039) | 86.4% (2627/3039) | n/a | n/a |
| `explicit/T` | 99.8% (1996/2000) | 99.2% (1983/2000) | 99.8% (1996/2000) | 99.2% (1983/2000) |
| `implicit/T` | 47.2% (944/2000) | 26.6% (531/2000) | 47.2% (944/2000) | 26.6% (531/2000) |
| `explicit/N4_Q` | 99.3% (1891/1904) | 98.8% (1882/1904) | 99.3% (1891/1904) | 98.8% (1882/1904) |
| `explicit/N4_R` | 99.1% (1894/1911) | 99.5% (1902/1911) | n/a | n/a |
| `implicit/N4_Q` | 99.2% (1889/1904) | 99.0% (1884/1904) | 99.2% (1889/1904) | 99.0% (1884/1904) |
| `implicit/N4_R` | 99.3% (1897/1911) | 99.5% (1902/1911) | n/a | n/a |
