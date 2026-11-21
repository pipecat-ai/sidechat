# Round 10: the line after the agent answers (exp-066-side-round10)

Teacher: `side-r10-ettin-150m-s1`. `side-r9-ettin-150m-s1` is rc0.3's default build, `side-r9tt-ettin-32m-s1` its agent-1x build. Speakers anonymous. Shares are `value (k/n)`.

| | `side-r9-ettin-150m-s1` | `side-r10-ettin-150m-s0` | `side-r10-ettin-150m-s1` | `side-r9tt-ettin-32m-s1` | `side-r10tt-ettin-32m-s0` | `side-r10tt-ettin-32m-s1` | `jev` |
|---|---|---|---|---|---|---|---|
| Generated test, anonymous | 99.0% (21,009/21,233) | 99.0% (21,011/21,233) | 99.0% (21,012/21,233) | 98.5% (20,914/21,233) | 98.4% (20,902/21,233) | 98.6% (20,941/21,233) | n/a |
| Duplex-MPE, right | 96.4% (50,438/52,336) | 96.2% (50,325/52,336) | 95.9% (50,189/52,336) | 95.7% (50,072/52,336) | 95.5% (49,971/52,336) | 95.2% (49,825/52,336) | 83.1% (43,495/52,336) |
| … for others, answered outright | 0.21% (93/44,528) | 0.39% (172/44,528) | 0.12% (53/44,528) | 0.33% (146/44,528) | 0.14% (64/44,528) | 0.23% (104/44,528) | 0.41% (182/44,528) |
| … for others, held | 0.8% (355/44,528) | 1.2% (528/44,528) | 1.1% (470/44,528) | 0.7% (312/44,528) | 0.7% (291/44,528) | 1.2% (522/44,528) | 16.0% (7,131/44,528) |
| … named request answered | 99.6% (1,991/2,000) | 99.6% (1,992/2,000) | 99.5% (1,990/2,000) | 99.7% (1,993/2,000) | 95.3% (1,907/2,000) | 97.6% (1,952/2,000) | 99.2% (1,983/2,000) |
| … unnamed request answered | 29.3% (587/2,000) | 36.4% (728/2,000) | 20.8% (417/2,000) | 10.2% (205/2,000) | 5.0% (99/2,000) | 8.3% (167/2,000) | 26.6% (531/2,000) |
| … unnamed request held | 13.2% (265/2,000) | 12.6% (251/2,000) | 12.6% (252/2,000) | 7.5% (151/2,000) | 7.5% (150/2,000) | 7.8% (157/2,000) | 73.2% (1,464/2,000) |
| Ambient Bench, right | 96.9% (15,302/15,793) | 96.3% (15,215/15,793) | 97.5% (15,395/15,793) | 97.5% (15,396/15,793) | 97.1% (15,335/15,793) | 97.0% (15,314/15,793) | 85.4% (13,479/15,793) |
| AMI labelled, right | 99.0% (8,785/8,875) | 98.6% (8,752/8,875) | 99.1% (8,793/8,875) | 98.7% (8,757/8,875) | 98.6% (8,746/8,875) | 98.7% (8,758/8,875) | 85.2% (7,563/8,875) |
| AMI as heard, held | 1.12% (92/8,202) | 1.69% (139/8,202) | 1.09% (89/8,202) | 1.43% (117/8,202) | 1.37% (112/8,202) | 1.30% (107/8,202) | 13.48% (1,106/8,202) |
| AMI silence test, answered outright | 0.00% (0/10,434) | 0.02% (2/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.01% (1/10,434) | n/a |
| Pilot, right | 87.8% (237/270) | 88.9% (240/270) | 88.9% (240/270) | 86.7% (234/270) | 87.8% (237/270) | 85.9% (232/270) | 77.8% (210/270) |
| Demo lines, right | 100.0% (48/48) | 97.9% (47/48) | 97.9% (47/48) | 100.0% (48/48) | 97.9% (47/48) | 95.8% (46/48) | n/a |
| SLURP named, answered now: written | 100.0% (61/61) | 100.0% (61/61) | 100.0% (61/61) | 100.0% (61/61) | 100.0% (61/61) | 98.4% (60/61) | 100.0% (61/61) |
| SLURP named, answered now: heard | 8.2% (5/61) | 21.3% (13/61) | 21.3% (13/61) | 9.8% (6/61) | 8.2% (5/61) | 8.2% (5/61) | 49.2% (30/61) |
| SLURP named, answered now: heard with keyterm | 78.7% (48/61) | 78.7% (48/61) | 78.7% (48/61) | 78.7% (48/61) | 77.0% (47/61) | 77.0% (47/61) | 73.8% (45/61) |
| SLURP unnamed, held: written | 94.6% (2,558/2,705) | 96.7% (2,617/2,705) | 94.5% (2,555/2,705) | 91.0% (2,462/2,705) | 90.7% (2,453/2,705) | 88.2% (2,387/2,705) | 90.1% (2,438/2,705) |
| SLURP unnamed, held: heard | 90.9% (2,458/2,704) | 93.6% (2,530/2,704) | 91.7% (2,480/2,704) | 86.6% (2,343/2,704) | 86.4% (2,336/2,704) | 85.1% (2,301/2,704) | 82.3% (2,226/2,704) |
| SLURP unnamed, held: heard with keyterm | 90.9% (2,460/2,705) | 93.5% (2,530/2,705) | 91.5% (2,475/2,705) | 86.6% (2,342/2,705) | 86.3% (2,334/2,705) | 84.8% (2,295/2,705) | 82.1% (2,220/2,705) |
| SLURP unnamed, answered now: heard | 0.1% (2/2,704) | 0.1% (3/2,704) | 0.0% (1/2,704) | 0.9% (25/2,704) | 0.0% (0/2,704) | 0.1% (3/2,704) | 0.0% (1/2,704) |
| TCL, people's lines answered outright | 1.94% (65/3,348) | 2.18% (73/3,348) | 1.67% (56/3,348) | 2.24% (75/3,348) | 1.52% (51/3,348) | 1.46% (49/3,348) | 1.55% (52/3,348) |
| TCL, people's lines held | 3.1% (103/3,348) | 3.2% (106/3,348) | 3.5% (118/3,348) | 2.7% (89/3,348) | 2.7% (89/3,348) | 3.4% (112/3,348) | 36.9% (1,235/3,348) |
| TCL, named requests answered now | 98.7% (156/158) | 98.7% (156/158) | 98.1% (155/158) | 98.7% (156/158) | 98.7% (156/158) | 98.1% (155/158) | 98.1% (155/158) |
| TCL, unnamed follow-ups answered now | 36.2% (51/141) | 34.0% (48/141) | 29.1% (41/141) | 35.5% (50/141) | 31.9% (45/141) | 31.2% (44/141) | 29.1% (41/141) |
| TCL, unnamed follow-ups held | 20.6% (29/141) | 21.3% (30/141) | 24.1% (34/141) | 16.3% (23/141) | 19.9% (28/141) | 24.8% (35/141) | 51.8% (73/141) |
| gen-0.5 test: question to the others after the agent, left alone | 66.6% (203/305) | 98.0% (299/305) | 97.0% (296/305) | 73.4% (224/305) | 95.4% (291/305) | 95.7% (292/305) | 0.0% (0/305) |
| gen-0.5 test: the partner turning to the others, left alone | 85.9% (226/263) | 88.6% (233/263) | 89.7% (236/263) | 83.7% (220/263) | 86.7% (228/263) | 84.4% (222/263) | 85.2% (224/263) |
| gen-0.5 test: the partner coming back later, held | 69.3% (219/316) | 69.0% (218/316) | 67.7% (214/316) | 59.2% (187/316) | 61.7% (195/316) | 62.7% (198/316) | 93.0% (294/316) |
| gen-0.5 test: follow-up, answered now | 99.2% (355/358) | 99.2% (355/358) | 99.2% (355/358) | 99.2% (355/358) | 99.2% (355/358) | 98.6% (353/358) | 44.4% (159/358) |

## Speed on agent-1x (0.5 vCPU, 1 GiB), one thread, history encoded ahead

| Model | Build | Memory MB | Full history | Full history, cold |
|---|---|---|---|---|
| `side-r9tt-ettin-32m-s1` | fp32 | 488 | 20 | 173 |
| `side-r10tt-ettin-32m-s0` | fp32 | 488 | 17 | 130 |
| `side-r10tt-ettin-32m-s1` | fp32 | 487 | 25 | 213 |
| `jev` | API |  | 140 |  |

## The gates

- `side-r10-ettin-150m-s0`: **does not ship**. **fails:** TCL people's lines answered outright +0.24 points, paired (-0.09 to +0.57); TCL unnamed follow-ups answered or held -1.42 points; TCL named requests answered +0.00 points; real unnamed requests held as heard +2.66 points; Duplex-MPE right -0.21 points; **fails:** Ambient Bench right -0.55 points; AMI right -0.38 points; generated test right +0.00 points; pilot right +1.11 points; named requests answered +0.05 points; SLURP named answered (keyterm) +0.00 points; **fails:** Duplex-MPE others answered outright +0.18 points; Duplex-MPE others held +0.39 points; AMI as heard, held +0.57 points; TCL people's lines held +0.09 points; Duplex-MPE others answered outright 0.39% (bar 0.4%)
- `side-r10-ettin-150m-s1`: **does not ship**. **fails:** TCL people's lines answered outright -0.27 points, paired (-0.62 to +0.08); TCL unnamed follow-ups answered or held -3.55 points; TCL named requests answered -0.63 points; real unnamed requests held as heard +0.81 points; Duplex-MPE right -0.47 points; Ambient Bench right +0.59 points; AMI right +0.09 points; generated test right +0.01 points; pilot right +1.11 points; named requests answered -0.05 points; SLURP named answered (keyterm) +0.00 points; Duplex-MPE others answered outright -0.09 points; Duplex-MPE others held +0.26 points; AMI as heard, held -0.03 points; TCL people's lines held +0.44 points; Duplex-MPE others answered outright 0.12% (bar 0.4%)
- `side-r10tt-ettin-32m-s0`: **does not ship**. TCL people's lines answered outright -0.72 points, paired (-1.09 to -0.35); TCL unnamed follow-ups answered or held +0.00 points; TCL named requests answered +0.00 points; real unnamed requests held as heard -0.26 points; Duplex-MPE right -0.19 points; Ambient Bench right -0.39 points; AMI right -0.12 points; generated test right -0.06 points; pilot right +1.11 points; **fails:** named requests answered -4.30 points; SLURP named answered (keyterm) -1.64 points; Duplex-MPE others answered outright -0.19 points; Duplex-MPE others held -0.05 points; AMI as heard, held -0.06 points; TCL people's lines held +0.00 points; Duplex-MPE others answered outright 0.14% (bar 0.4%); full history on agent-1x 17 ms (Jev 140)
- `side-r10tt-ettin-32m-s1`: **does not ship**. TCL people's lines answered outright -0.78 points, paired (-1.14 to -0.42); TCL unnamed follow-ups answered or held +4.26 points; TCL named requests answered -0.63 points; real unnamed requests held as heard -1.55 points; Duplex-MPE right -0.47 points; **fails:** Ambient Bench right -0.52 points; AMI right +0.01 points; generated test right +0.12 points; pilot right -0.74 points; **fails:** named requests answered -2.05 points; SLURP named answered (keyterm) -1.64 points; Duplex-MPE others answered outright -0.10 points; Duplex-MPE others held +0.47 points; AMI as heard, held -0.13 points; TCL people's lines held +0.69 points; Duplex-MPE others answered outright 0.23% (bar 0.4%); full history on agent-1x 25 ms (Jev 140)

## Notes

- Dev picks `side-r10-ettin-150m-s1` among the teachers and `side-r10tt-ettin-32m-s1` among the students.
