# Round 8: real people's requests in training (exp-059-side-round8)

Teacher: `side-r8-ettin-150m-s1`. `side-r3-ettin-150m-s0` is the released default build, `side-r6ttr3t-ettin-32m-s0` the released agent-1x build. Speakers anonymous. Shares are `value (k/n)`.

| | `side-r3-ettin-150m-s0` | `side-r8-ettin-150m-s0` | `side-r8-ettin-150m-s1` | `side-r6ttr3t-ettin-32m-s0` | `side-r8tt-ettin-32m-s0` | `side-r8tt-ettin-32m-s1` | `jev` |
|---|---|---|---|---|---|---|---|
| Generated test, anonymous | 99.0% (21,009/21,233) | 99.0% (21,022/21,233) | 99.0% (21,013/21,233) | 98.5% (20,913/21,233) | 98.6% (20,932/21,233) | 98.6% (20,938/21,233) | n/a |
| Duplex-MPE, right | 96.7% (50,592/52,336) | 96.6% (50,559/52,336) | 96.3% (50,382/52,336) | 95.6% (50,050/52,336) | 95.5% (49,996/52,336) | 95.8% (50,120/52,336) | 83.1% (43,495/52,336) |
| … for others, answered outright | 0.22% (97/44,528) | 0.40% (177/44,528) | 0.56% (249/44,528) | 0.26% (115/44,528) | 0.40% (177/44,528) | 0.22% (98/44,528) | 0.41% (182/44,528) |
| … for others, held | 0.9% (382/44,528) | 1.1% (493/44,528) | 1.0% (448/44,528) | 0.8% (352/44,528) | 0.8% (370/44,528) | 0.5% (231/44,528) | 16.0% (7,131/44,528) |
| … named request answered | 99.5% (1,990/2,000) | 99.7% (1,993/2,000) | 99.6% (1,992/2,000) | 98.7% (1,973/2,000) | 99.2% (1,984/2,000) | 96.4% (1,927/2,000) | 99.2% (1,983/2,000) |
| … unnamed request answered | 38.8% (775/2,000) | 46.5% (929/2,000) | 39.1% (781/2,000) | 10.7% (214/2,000) | 11.5% (230/2,000) | 9.7% (194/2,000) | 26.6% (531/2,000) |
| … unnamed request held | 13.2% (265/2,000) | 13.7% (274/2,000) | 12.4% (249/2,000) | 7.4% (149/2,000) | 6.8% (135/2,000) | 6.9% (137/2,000) | 73.2% (1,464/2,000) |
| Ambient Bench, right | 98.7% (15,591/15,793) | 96.8% (15,283/15,793) | 96.9% (15,305/15,793) | 98.4% (15,546/15,793) | 97.1% (15,333/15,793) | 96.6% (15,251/15,793) | 85.4% (13,479/15,793) |
| AMI labelled, right | 99.9% (8,865/8,875) | 98.7% (8,761/8,875) | 98.2% (8,711/8,875) | 100.0% (8,874/8,875) | 98.0% (8,698/8,875) | 97.7% (8,667/8,875) | 85.2% (7,563/8,875) |
| AMI as heard, held | 0.15% (12/8,202) | 1.62% (133/8,202) | 2.37% (194/8,202) | 0.01% (1/8,202) | 2.44% (200/8,202) | 2.48% (203/8,202) | 13.48% (1,106/8,202) |
| AMI silence test, answered outright | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.01% (1/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | n/a |
| Pilot, right | 87.4% (236/270) | 87.8% (237/270) | 87.4% (236/270) | 87.4% (236/270) | 85.6% (231/270) | 86.3% (233/270) | 77.8% (210/270) |
| Demo lines, right | 97.9% (47/48) | 97.9% (47/48) | 95.8% (46/48) | 97.9% (47/48) | 100.0% (48/48) | 97.9% (47/48) | n/a |
| SLURP named, answered now: written | 85.2% (52/61) | 100.0% (61/61) | 100.0% (61/61) | 63.9% (39/61) | 98.4% (60/61) | 100.0% (61/61) | 100.0% (61/61) |
| SLURP named, answered now: heard | 13.1% (8/61) | 9.8% (6/61) | 14.8% (9/61) | 6.6% (4/61) | 8.2% (5/61) | 8.2% (5/61) | 49.2% (30/61) |
| SLURP named, answered now: heard with keyterm | 73.8% (45/61) | 78.7% (48/61) | 78.7% (48/61) | 59.0% (36/61) | 77.0% (47/61) | 78.7% (48/61) | 73.8% (45/61) |
| SLURP unnamed, held: written | 18.2% (491/2,705) | 97.2% (2,629/2,705) | 96.9% (2,620/2,705) | 3.0% (82/2,705) | 94.4% (2,553/2,705) | 93.1% (2,519/2,705) | 90.1% (2,438/2,705) |
| SLURP unnamed, held: heard | 16.7% (451/2,704) | 95.3% (2,576/2,704) | 95.2% (2,573/2,704) | 3.6% (96/2,704) | 90.9% (2,458/2,704) | 91.0% (2,461/2,704) | 82.3% (2,226/2,704) |
| SLURP unnamed, held: heard with keyterm | 16.6% (448/2,705) | 95.3% (2,579/2,705) | 95.2% (2,574/2,705) | 3.7% (99/2,705) | 90.8% (2,457/2,705) | 90.9% (2,458/2,705) | 82.1% (2,220/2,705) |
| SLURP unnamed, answered now: heard | 0.3% (8/2,704) | 0.0% (0/2,704) | 0.0% (0/2,704) | 0.0% (1/2,704) | 0.5% (14/2,704) | 0.1% (4/2,704) | 0.0% (1/2,704) |

## Speed on agent-1x (0.5 vCPU, 1 GiB), one thread, history encoded ahead

| Model | Build | Memory MB | Full history | Full history, cold |
|---|---|---|---|---|
| `side-r6ttr3t-ettin-32m-s0` | fp32 | 489 | 12 | 108 |
| `side-r8tt-ettin-32m-s0` | fp32 | 490 | 15 | 117 |
| `side-r8tt-ettin-32m-s1` | fp32 | 490 | 15 | 116 |
| `jev` | API |  | 133 |  |

## The gates

- `side-r8-ettin-150m-s1`: **does not ship**. unnamed requests held as heard 95.2% (was 16.7%); Duplex-MPE right -0.40 points; **fails:** Ambient Bench right -1.81 points; **fails:** AMI right -1.74 points; generated test right +0.01 points; pilot right +0.00 points; named requests answered +0.10 points; SLURP named answered (keyterm) +4.92 points; **fails:** Duplex-MPE others answered outright +0.34 points; Duplex-MPE others held +0.15 points; **fails:** AMI as heard, held +2.22 points; **fails:** Duplex-MPE others answered outright 0.56% (bar 0.4%)
- `side-r8tt-ettin-32m-s0`: **does not ship**. unnamed requests held as heard 90.9% (was 3.6%); Duplex-MPE right -0.10 points; **fails:** Ambient Bench right -1.35 points; **fails:** AMI right -1.98 points; generated test right +0.09 points; **fails:** pilot right -1.85 points; named requests answered +0.55 points; SLURP named answered (keyterm) +18.03 points; **fails:** Duplex-MPE others answered outright +0.14 points; Duplex-MPE others held +0.04 points; **fails:** AMI as heard, held +2.43 points; Duplex-MPE others answered outright 0.40% (bar 0.4%); full history on agent-1x 15 ms (Jev 133)
- `side-r8tt-ettin-32m-s1`: **does not ship**. unnamed requests held as heard 91.0% (was 3.6%); Duplex-MPE right +0.14 points; **fails:** Ambient Bench right -1.87 points; **fails:** AMI right -2.33 points; generated test right +0.12 points; **fails:** pilot right -1.11 points; **fails:** named requests answered -2.30 points; SLURP named answered (keyterm) +19.67 points; Duplex-MPE others answered outright -0.04 points; Duplex-MPE others held -0.27 points; **fails:** AMI as heard, held +2.47 points; Duplex-MPE others answered outright 0.22% (bar 0.4%); full history on agent-1x 15 ms (Jev 133)
