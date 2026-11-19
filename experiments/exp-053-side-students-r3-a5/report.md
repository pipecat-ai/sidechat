# Round 6 and the agent-1x students (exp-053-side-students-r3-a5)

Teacher: `side-r3-ettin-150m-s0`. Speakers anonymous. Shares are `value (k/n)`; each run's own report has 95% intervals.

| | `side-r3-ettin-150m-s0` | `side-r6-ettin-150m-s0` | `side-r6-ettin-150m-s1` | `side-r6ttr3a5-ettin-32m-s0` | `side-r6ttr3a5-ettin-68m-s0` |
|---|---|---|---|---|---|
| Generated test, anonymous | 99.0% (21,009/21,233) | 99.1% (21,034/21,233) | 99.1% (21,033/21,233) | 98.7% (20,952/21,233) | 98.8% (20,975/21,233) |
| gen-0.4 test, anonymous | n/a | 98.8% (10,259/10,385) | 98.9% (10,266/10,385) | 98.2% (10,199/10,385) | 98.3% (10,212/10,385) |
| Duplex-MPE, right | 96.7% (50,592/52,336) | 96.2% (50,341/52,336) | 95.8% (50,135/52,336) | 95.6% (50,019/52,336) | 95.6% (50,050/52,336) |
| … lines for others answered outright | 0.22% (97/44,528) | 0.45% (199/44,528) | 0.20% (91/44,528) | 0.14% (62/44,528) | 0.18% (79/44,528) |
| … unnamed request answered (implicit T) | 38.8% (775/2,000) | 37.4% (748/2,000) | 22.8% (456/2,000) | 7.2% (145/2,000) | 9.0% (181/2,000) |
| … name said about the agent, answered outright (N1) | 0.28% (17/6,080) | 0.54% (33/6,080) | 0.35% (21/6,080) | 0.20% (12/6,080) | 0.16% (10/6,080) |
| Ambient Bench, right | 98.7% (15,591/15,793) | 98.1% (15,491/15,793) | 98.4% (15,538/15,793) | 98.0% (15,478/15,793) | 98.5% (15,557/15,793) |
| AMI labelled, right | 99.9% (8,865/8,875) | 99.9% (8,869/8,875) | 99.9% (8,866/8,875) | 100.0% (8,874/8,875) | 100.0% (8,871/8,875) |
| AMI silent test, answered outright | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) |
| Pilot, anonymous, right | 87.4% (236/270) | 87.8% (237/270) | 89.3% (241/270) | 86.7% (234/270) | 85.9% (232/270) |
| Demo lines, right | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) |

## Speed on agent-1x (0.5 vCPU, 1 GiB), one thread

Median ms per line through the demo's gate: short history / 8 earlier lines. For a two-tower model the history is encoded first, untimed, as while the person talks.

| Model | Build | Memory MB | Short | Full history | Full history, cold | Beats Jev |
|---|---|---|---|---|---|---|
| `side-r6ttr3a5-ettin-32m-s0` | fp32 (r6ttr3a5-32m) | 488 | 13 | 15 | 117 | yes (Jev 65) |
| `side-r6ttr3a5-ettin-68m-s0` | fp32 (r6ttr3a5-68m) | 803 | 84 | 86 | 398 | no (Jev 65) |

## The gate

- `side-r6ttr3a5-ettin-32m-s0`: **does not ship**. Duplex-MPE -1.1 points against the teacher; AMI +0.1 points against the teacher; pilot -0.7 points against the teacher; full history 15 ms on agent-1x against Jev's 65
- `side-r6ttr3a5-ettin-68m-s0`: **does not ship**. Duplex-MPE -1.0 points against the teacher; AMI +0.1 points against the teacher; pilot -1.5 points against the teacher; full history 86 ms on agent-1x against Jev's 65
