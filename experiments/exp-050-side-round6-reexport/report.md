# Round 6 and the agent-1x students (exp-050-side-round6-reexport)

Teacher: `side-r6-ettin-150m-s1`. Speakers anonymous. Shares are `value (k/n)`; each run's own report has 95% intervals.

| | `side-r3-ettin-150m-s0` | `side-r6-ettin-150m-s0` | `side-r6-ettin-150m-s1` | `side-r6tt-ettin-32m-s0` | `side-r6tt-ettin-68m-s0` | `side-r6s-ettin-32m-s0` |
|---|---|---|---|---|---|---|
| Generated test, anonymous | 99.0% (21,009/21,233) | 99.1% (21,034/21,233) | 99.1% (21,033/21,233) | 98.7% (20,955/21,233) | 98.7% (20,961/21,233) | 98.8% (20,978/21,233) |
| gen-0.4 test, anonymous | n/a | 98.8% (10,259/10,385) | 98.9% (10,266/10,385) | 98.5% (10,232/10,385) | 98.5% (10,232/10,385) | 98.7% (10,250/10,385) |
| Duplex-MPE, right | 96.7% (50,592/52,336) | 96.2% (50,341/52,336) | 95.8% (50,135/52,336) | 95.2% (49,812/52,336) | 95.5% (49,992/52,336) | 95.3% (49,879/52,336) |
| … lines for others answered outright | 0.22% (97/44,528) | 0.45% (199/44,528) | 0.20% (91/44,528) | 0.25% (111/44,528) | 0.23% (103/44,528) | 0.49% (219/44,528) |
| … unnamed request answered (implicit T) | 38.8% (775/2,000) | 37.4% (748/2,000) | 22.8% (456/2,000) | 6.1% (122/2,000) | 9.6% (191/2,000) | 13.8% (275/2,000) |
| … name said about the agent, answered outright (N1) | 0.28% (17/6,080) | 0.54% (33/6,080) | 0.35% (21/6,080) | 0.94% (57/6,080) | 0.36% (22/6,080) | 1.35% (82/6,080) |
| Ambient Bench, right | 98.7% (15,591/15,793) | 98.1% (15,491/15,793) | 98.4% (15,538/15,793) | 97.7% (15,433/15,793) | 98.1% (15,488/15,793) | 98.5% (15,556/15,793) |
| AMI labelled, right | 99.9% (8,865/8,875) | 99.9% (8,869/8,875) | 99.9% (8,866/8,875) | 100.0% (8,872/8,875) | 100.0% (8,874/8,875) | 99.9% (8,869/8,875) |
| AMI silent test, answered outright | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) | 0.00% (0/10,434) |
| Pilot, anonymous, right | 87.4% (236/270) | 87.8% (237/270) | 89.3% (241/270) | 86.7% (234/270) | 86.3% (233/270) | 86.3% (233/270) |
| Demo lines, right | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) |

## Speed on agent-1x (0.5 vCPU, 1 GiB), one thread

Median ms per line through the demo's gate: short history / 8 earlier lines. For a two-tower model the history is encoded first, untimed, as while the person talks.

| Model | Build | Memory MB | Short | Full history | Full history, cold | Beats Jev |
|---|---|---|---|---|---|---|
| `side-r6-ettin-150m-s1` | int8 (r6-150m) | 573 | 97 | 508 |  | no (Jev 66) |
| `side-r6tt-ettin-32m-s0` | int8 (r6tt-32m) | 416 | 8 | 11 | 97 | yes (Jev 66) |
| `side-r6tt-ettin-68m-s0` | fp32 (r6tt-68m) | 802 | 92 | 96 | 488 | no (Jev 66) |
| `side-r6s-ettin-32m-s0` | fp32 (r6s-32m) | 357 | 23 | 100 |  | no (Jev 66) |

## The gate

- `side-r6tt-ettin-32m-s0`: **does not ship**. Duplex-MPE -0.6 points against the teacher; AMI +0.1 points against the teacher; pilot -2.6 points against the teacher; full history 11 ms on agent-1x against Jev's 66
- `side-r6tt-ettin-68m-s0`: **does not ship**. Duplex-MPE -0.3 points against the teacher; AMI +0.1 points against the teacher; pilot -3.0 points against the teacher; full history 96 ms on agent-1x against Jev's 66
- `side-r6s-ettin-32m-s0`: **does not ship**. Duplex-MPE -0.5 points against the teacher; AMI +0.0 points against the teacher; pilot -3.0 points against the teacher; full history 100 ms on agent-1x against Jev's 66
