# Real people's requests in training (exp-060-side-round9)

Teacher: `side-r9-ettin-150m-s1`. `side-r3-ettin-150m-s0` is the released default build, `side-r6ttr3t-ettin-32m-s0` the released agent-1x build. Speakers anonymous. Shares are `value (k/n)`.

| | `side-r3-ettin-150m-s0` | `side-r9-ettin-150m-s0` | `side-r9-ettin-150m-s1` | `side-r6ttr3t-ettin-32m-s0` | `side-r9tt-ettin-32m-s0` | `side-r9tt-ettin-32m-s1` | `jev` |
|---|---|---|---|---|---|---|---|
| Generated test, anonymous | 99.0% (21,009/21,233) | 99.0% (21,011/21,233) | 99.0% (21,009/21,233) | 98.5% (20,913/21,233) | 98.6% (20,942/21,233) | 98.5% (20,914/21,233) | n/a |
| Duplex-MPE, right | 96.7% (50,592/52,336) | 96.3% (50,417/52,336) | 96.4% (50,438/52,336) | 95.6% (50,050/52,336) | 95.5% (49,977/52,336) | 95.7% (50,072/52,336) | 83.1% (43,495/52,336) |
| … for others, answered outright | 0.22% (97/44,528) | 0.16% (73/44,528) | 0.21% (93/44,528) | 0.26% (115/44,528) | 0.26% (115/44,528) | 0.33% (146/44,528) | 0.41% (182/44,528) |
| … for others, held | 0.9% (382/44,528) | 0.8% (346/44,528) | 0.8% (355/44,528) | 0.8% (352/44,528) | 0.7% (288/44,528) | 0.7% (312/44,528) | 16.0% (7,131/44,528) |
| … named request answered | 99.5% (1,990/2,000) | 99.7% (1,993/2,000) | 99.6% (1,991/2,000) | 98.7% (1,973/2,000) | 96.5% (1,930/2,000) | 99.7% (1,993/2,000) | 99.2% (1,983/2,000) |
| … unnamed request answered | 38.8% (775/2,000) | 26.6% (532/2,000) | 29.3% (587/2,000) | 10.7% (214/2,000) | 6.5% (129/2,000) | 10.2% (205/2,000) | 26.6% (531/2,000) |
| … unnamed request held | 13.2% (265/2,000) | 11.8% (236/2,000) | 13.2% (265/2,000) | 7.4% (149/2,000) | 7.4% (149/2,000) | 7.5% (151/2,000) | 73.2% (1,464/2,000) |
| Ambient Bench, right | 98.7% (15,591/15,793) | 96.9% (15,300/15,793) | 96.9% (15,302/15,793) | 98.4% (15,546/15,793) | 97.2% (15,355/15,793) | 97.5% (15,396/15,793) | 85.4% (13,479/15,793) |
| AMI labelled, right | 99.9% (8,865/8,875) | 98.7% (8,760/8,875) | 99.0% (8,785/8,875) | 100.0% (8,874/8,875) | 99.1% (8,792/8,875) | 98.7% (8,757/8,875) | 85.2% (7,563/8,875) |
| AMI as heard, held | 0.15% (12/8,202) | 1.60% (131/8,202) | 1.12% (92/8,202) | 0.01% (1/8,202) | 0.79% (65/8,202) | 1.43% (117/8,202) | 13.48% (1,106/8,202) |
| AMI silence test, answered outright | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | n/a |
| Pilot, right | 87.4% (236/270) | 86.7% (234/270) | 87.8% (237/270) | 87.4% (236/270) | 87.4% (236/270) | 86.7% (234/270) | 77.8% (210/270) |
| Demo lines, right | 97.9% (47/48) | 97.9% (47/48) | 100.0% (48/48) | 97.9% (47/48) | 97.9% (47/48) | 100.0% (48/48) | n/a |
| SLURP named, answered now: written | 85.2% (52/61) | 100.0% (61/61) | 100.0% (61/61) | 63.9% (39/61) | 88.5% (54/61) | 100.0% (61/61) | 100.0% (61/61) |
| SLURP named, answered now: heard | 13.1% (8/61) | 11.5% (7/61) | 8.2% (5/61) | 6.6% (4/61) | 8.2% (5/61) | 9.8% (6/61) | 49.2% (30/61) |
| SLURP named, answered now: heard with keyterm | 73.8% (45/61) | 78.7% (48/61) | 78.7% (48/61) | 59.0% (36/61) | 70.5% (43/61) | 78.7% (48/61) | 73.8% (45/61) |
| SLURP unnamed, held: written | 18.2% (491/2,705) | 96.9% (2,621/2,705) | 94.6% (2,558/2,705) | 3.0% (82/2,705) | 86.4% (2,336/2,705) | 91.0% (2,462/2,705) | 90.1% (2,438/2,705) |
| SLURP unnamed, held: heard | 16.7% (451/2,704) | 93.5% (2,529/2,704) | 90.9% (2,458/2,704) | 3.6% (96/2,704) | 81.1% (2,193/2,704) | 86.6% (2,343/2,704) | 82.3% (2,226/2,704) |
| SLURP unnamed, held: heard with keyterm | 16.6% (448/2,705) | 93.6% (2,533/2,705) | 90.9% (2,460/2,705) | 3.7% (99/2,705) | 80.9% (2,188/2,705) | 86.6% (2,342/2,705) | 82.1% (2,220/2,705) |
| SLURP unnamed, answered now: heard | 0.3% (8/2,704) | 0.0% (0/2,704) | 0.1% (2/2,704) | 0.0% (1/2,704) | 0.1% (2/2,704) | 0.9% (25/2,704) | 0.0% (1/2,704) |

## Speed on agent-1x (0.5 vCPU, 1 GiB), one thread, history encoded ahead

| Model | Build | Memory MB | Full history | Full history, cold |
|---|---|---|---|---|
| `side-r6ttr3t-ettin-32m-s0` | fp32 | 490 | 15 | 117 |
| `side-r9tt-ettin-32m-s0` | fp32 | 490 | 10 | 90 |
| `side-r9tt-ettin-32m-s1` | fp32 | 487 | 14 | 108 |
| `jev` | API |  | 49 |  |

## The gates

- `side-r9-ettin-150m-s1`: **does not ship**. unnamed requests held as heard 90.9% (was 16.7%); Duplex-MPE right -0.30 points; **fails:** Ambient Bench right -1.83 points; **fails:** AMI right -0.90 points; generated test right +0.00 points; pilot right +0.37 points; named requests answered +0.05 points; SLURP named answered (keyterm) +4.92 points; Duplex-MPE others answered outright -0.01 points; Duplex-MPE others held -0.06 points; AMI as heard, held +0.97 points; Duplex-MPE others answered outright 0.21% (bar 0.4%)
- `side-r9tt-ettin-32m-s0`: **does not ship**. unnamed requests held as heard 81.1% (was 3.6%); Duplex-MPE right -0.14 points; **fails:** Ambient Bench right -1.21 points; **fails:** AMI right -0.93 points; generated test right +0.14 points; pilot right +0.00 points; **fails:** named requests answered -2.15 points; SLURP named answered (keyterm) +11.48 points; Duplex-MPE others answered outright +0.00 points; Duplex-MPE others held -0.14 points; AMI as heard, held +0.78 points; Duplex-MPE others answered outright 0.26% (bar 0.4%); full history on agent-1x 10 ms (Jev 49)
- `side-r9tt-ettin-32m-s1`: **does not ship**. unnamed requests held as heard 86.6% (was 3.6%); Duplex-MPE right +0.04 points; **fails:** Ambient Bench right -0.95 points; **fails:** AMI right -1.32 points; generated test right +0.01 points; pilot right -0.74 points; named requests answered +1.00 points; SLURP named answered (keyterm) +19.67 points; Duplex-MPE others answered outright +0.07 points; Duplex-MPE others held -0.09 points; **fails:** AMI as heard, held +1.42 points; Duplex-MPE others answered outright 0.33% (bar 0.4%); full history on agent-1x 14 ms (Jev 49)

## Notes

- Dev picks `side-r9-ettin-150m-s1` among the teachers and `side-r9tt-ettin-32m-s1` among the students.
