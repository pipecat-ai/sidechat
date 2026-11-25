# Round 6 and the agent-1x students, against Jev

2026-11-19. Experiments exp-035 to exp-053. Speakers anonymous throughout.

## Verdict

**No small model passes every gate yet.** The two-tower students are fast enough for `agent-1x`
and match round 3 on most sets, but each loses something round 3 keeps. Round 3
(`side-r3-ettin-150m-s0`) stays the pick; it runs well on a laptop-class CPU, not on `agent-1x`.

The gate as set (faster than Jev on `agent-1x` with a full history, within about a point of the
teacher on Duplex-MPE, AMI and the pilot) was passed by one student, the two-tower 68M taught by
round 3 (seed 0). It answers only 87.8% of Duplex-MPE's named requests (round 3 99.5%, Jev
99.2%): named requests are a small share of Duplex-MPE, so it stayed within a point. The gate
should also require items 4 and 5 (named and unnamed requests) to be no worse than the teacher. No
student passes that.

## Accuracy against Jev

| | Round 3, 150M (the pick) | Two-tower 68M, seed 0 | Two-tower 32M, seed 0 | Two-tower 68M, seed 1 | Jev |
|---|---|---|---|---|---|
| Generated test, right | 99.0% | 98.6% | 98.5% | 98.7% | 80.7% (2,882-line sample) |
| Duplex-MPE, 52,336 lines, right | 96.7% | 95.8% | 95.6% | 96.0% | 83.1% |
| … lines for others, answered outright | 0.22% | 0.17% | 0.26% | 0.12% | 0.41% |
| … lines for others, held for a pause | 0.9% | 0.4% | 0.8% | 0.5% | 16.0% |
| … request with the agent's name, answered | 99.5% | **87.8%** | 98.7% | 99.5% | 99.2% |
| … same request without the name, answered | 38.8% | **19.5%** | **10.7%** | **9.0%** | 26.6% |
| Ambient Bench, 15,793 lines | 98.7% | 98.6% | 98.4% | 98.9% | 85.4% |
| AMI real meetings, 8,875 lines | 99.9% | 100.0% | 100.0% | 100.0% | 85.2% |
| AMI silence test, answered outright (of 10,434) | 0 | 0 | 0 | 0 | 5 |
| Pilot, 270 hand-written lines | 87.4% | 87.4% | 87.4% | 85.6% | 77.8% |
| The demo's 48 lines | 47 | 47 | 47 | 47 | 47 |
| Scorecard items met (of 16) | 12 | 10 | 10 | not run | |

The students are distilled from round 3 (80% its probabilities, 20% labels) over round 6's corpus
plus gen-0.3. Two more seeds and a label-heavier mix (exp-052, exp-053) did not do better: named
requests swing with the seed (87.8% to 99.5% for the 68M, 92.1% to 98.7% for the 32M), and every
student answers 6% to 20% of unnamed requests. On those, the students mostly do nothing (73% to
85% missed, 6% to 7% held), where Jev mostly holds (73%) and round 3 misses 48%.

Round 6 itself (150M, two seeds) did not beat round 3: it met item 9 in one seed (open questions
near 50:50 in the pilot, 21/26) but made item 7 worse in both (N1 answered outright 0.35% to 0.54%,
round 3 0.28%), and seed 1 fell below Jev on unnamed requests (22.8%).

## Latency against Jev

Median ms a line through the daily-audience demo's gate, one ONNX thread, on Modal containers
capped like Pipecat Cloud's profiles. "Full history" is 8 earlier lines. Two-tower models encode
the history while the person is still talking (`prepare`); "history not ready" is both towers at
the end of the turn.

| On agent-1x (0.5 vCPU, 1 GiB) | Memory | Short history | Full history | History not ready |
|---|---|---|---|---|
| Two-tower 32M, fp32 | 488 MB | 7 to 13 | **10 to 15** | 88 to 117 |
| Two-tower 68M, int8 (seed 0 only; int8 failed its gate for the others) | 557 MB | 21 | **23** | 211 |
| Two-tower 68M, fp32 | 803 to 818 MB | 83 to 92 | 83 to 96 | 380 to 488 |
| Round 3/6 150M, int8 (today's single-tower design) | 571 MB | 97 to 103 | 508 to 532 | |
| Round 3 150M, fp32 | 910 MB, at the edge of 1 GiB | 507 | 648 (p99 25 s) | |
| **Jev** (an API call from the same container) | 114 MB | 53 to 159 | **56 to 163** | |

| On agent-2x (1 vCPU, 2 GiB) | Full history | History not ready |
|---|---|---|
| Two-tower 32M, fp32 | 9 | 35 |
| Two-tower 68M, int8 | 25 | 121 |
| Round 3 150M, fp32 | 253 | |
| Jev | 58 to 149 | |

- **A two-tower 32M is 4 to 16 times faster than Jev on agent-1x** once the history is ready, and
  about as fast as Jev even when it is not. Encoding the history takes 76 ms on agent-1x, well
  inside the time anyone takes to say a line.
- **The single-tower 150M cannot run on agent-1x**: 0.5 s a line with int8, and fp32 does not
  fit.
- **Jev's time is the network.** Its median moved from 53 to 163 ms between containers; the
  students' moved by a few ms.
- **int8 is unreliable for the students**: it passed its quality gate for 2 of 9 builds. The 32M
  does not need it.
- On agent-1x the two-tower p90 is 60 to 75 ms in the bench, because the history is encoded just
  before the line and uses up the half core's quota; in a call it is encoded seconds earlier.

## What would close the gap

1. **Unnamed requests** (item 5) are the main loss. The guide calls an unnamed request with no
   agent in the history an even call (0.5), so the students learn to sit near the hold threshold
   and fall below it; round 3's 38.8% comes from cues the small students do not pick up. Two
   options: decide in the guide that such a request is held (the harness answers after a pause,
   as Jev does), or give the students lines like these scored by the teacher.
2. **Named requests** (item 4) swing with the seed. Pick the checkpoint on a named-request dev
   slice, or keep labels at full weight on named lines (the guide is certain there).
3. **Keep the 32M in fp32** and drop int8 for students: it is fast enough and avoids the gate.
