# Student round 2 for agent-1x (exp-055-side-round7)

Teacher: `side-r3-ettin-150m-s0`. `side-r6ttr3t-ettin-32m-s0` is rc0.2's agent-1x build. Speakers anonymous. Shares are `value (k/n)`.

| | `side-r3-ettin-150m-s0` | `side-r6ttr3t-ettin-32m-s0` | `side-r7po25-ettin-32m-s0` | `side-r7po25-ettin-32m-s1` | `side-r7po50-ettin-32m-s0` | `side-r7po50-ettin-32m-s1` |
|---|---|---|---|---|---|---|
| Generated test, anonymous | 99.0% (21,009/21,233) | 98.5% (20,913/21,233) | 98.6% (20,938/21,233) | 98.5% (20,912/21,233) | 98.6% (20,945/21,233) | 98.6% (20,926/21,233) |
| Duplex-MPE, right | 96.7% (50,592/52,336) | 95.6% (50,050/52,336) | 95.5% (49,967/52,336) | 95.5% (49,981/52,336) | 95.5% (49,980/52,336) | 95.7% (50,080/52,336) |
| … lines for others answered outright | 0.22% (97/44,528) | 0.26% (115/44,528) | 0.44% (195/44,528) | 0.20% (91/44,528) | 0.43% (192/44,528) | 0.24% (109/44,528) |
| … lines for others held | 0.9% (382/44,528) | 0.8% (352/44,528) | 0.9% (422/44,528) | 0.8% (362/44,528) | 0.9% (377/44,528) | 0.8% (376/44,528) |
| … named request answered (item 4) | 99.5% (1,990/2,000) | 98.7% (1,973/2,000) | 99.0% (1,980/2,000) | 95.2% (1,903/2,000) | 99.1% (1,982/2,000) | 99.2% (1,983/2,000) |
| … unnamed request answered (item 5) | 38.8% (775/2,000) | 10.7% (214/2,000) | 13.4% (268/2,000) | 11.2% (223/2,000) | 11.7% (233/2,000) | 13.2% (265/2,000) |
| … unnamed request held | 13.2% (265/2,000) | 7.4% (149/2,000) | 7.8% (156/2,000) | 5.9% (117/2,000) | 9.0% (181/2,000) | 9.6% (191/2,000) |
| Ambient Bench, right | 98.7% (15,591/15,793) | 98.4% (15,546/15,793) | 98.0% (15,484/15,793) | 98.5% (15,558/15,793) | 98.5% (15,557/15,793) | 98.2% (15,510/15,793) |
| AMI labelled, right | 99.9% (8,865/8,875) | 100.0% (8,874/8,875) | 100.0% (8,875/8,875) | 100.0% (8,875/8,875) | 100.0% (8,873/8,875) | 100.0% (8,875/8,875) |
| AMI silent test, answered outright | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) |
| Pilot, anonymous, right | 87.4% (236/270) | 87.4% (236/270) | 85.6% (231/270) | 84.8% (229/270) | 85.9% (232/270) | 85.9% (232/270) |
| Demo lines, right | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) |

## Speed on agent-1x (0.5 vCPU, 1 GiB), one thread

Median ms per line through the demo's gate; the history is encoded first, untimed, as while the person talks.

| Model | Build | Memory MB | Short | Full history | Full history, cold |
|---|---|---|---|---|---|
| `side-r6ttr3t-ettin-32m-s0` | fp32 | 488 | 14 | 16 | 112 |
| `side-r7po25-ettin-32m-s0` | fp32 | 489 | 14 | 17 | 118 |
| `side-r7po25-ettin-32m-s1` | fp32 | 488 | 12 | 13 | 110 |
| `side-r7po50-ettin-32m-s0` | fp32 | 490 | 14 | 15 | 111 |
| `side-r7po50-ettin-32m-s1` | fp32 | 489 | 15 | 17 | 120 |
| `jev` | API |  | 144 | 152 |  |

## The gate

- `side-r6ttr3t-ettin-32m-s0`: **does not ship**. **fails:** Duplex-MPE -1.0 points against the teacher; AMI +0.1 points against the teacher; pilot +0.0 points against the teacher; named requests -0.8 points against the teacher; **fails:** unnamed requests 10.7% answered (Jev 26.6%); full history 16 ms on agent-1x (Jev 152)
- `side-r7po25-ettin-32m-s0`: **does not ship**. **fails:** Duplex-MPE -1.2 points against the teacher; AMI +0.1 points against the teacher; **fails:** pilot -1.8 points against the teacher; named requests -0.5 points against the teacher; **fails:** unnamed requests 13.4% answered (Jev 26.6%); full history 17 ms on agent-1x (Jev 152)
- `side-r7po25-ettin-32m-s1`: **does not ship**. **fails:** Duplex-MPE -1.2 points against the teacher; AMI +0.1 points against the teacher; **fails:** pilot -2.6 points against the teacher; **fails:** named requests -4.3 points against the teacher; **fails:** unnamed requests 11.2% answered (Jev 26.6%); full history 13 ms on agent-1x (Jev 152)
- `side-r7po50-ettin-32m-s0`: **does not ship**. **fails:** Duplex-MPE -1.2 points against the teacher; AMI +0.1 points against the teacher; **fails:** pilot -1.5 points against the teacher; named requests -0.4 points against the teacher; **fails:** unnamed requests 11.7% answered (Jev 26.6%); full history 15 ms on agent-1x (Jev 152)
- `side-r7po50-ettin-32m-s1`: **does not ship**. Duplex-MPE -1.0 points against the teacher; AMI +0.1 points against the teacher; **fails:** pilot -1.5 points against the teacher; named requests -0.3 points against the teacher; **fails:** unnamed requests 13.2% answered (Jev 26.6%); full history 17 ms on agent-1x (Jev 152)
