# Student round 2 for agent-1x, against round 3 and Jev

2026-11-19. exp-055 (`sidechat/pipeline/round7.py`). Notes:
[phase-5-students-round2.md](../notes/phase-5-students-round2.md). Speakers anonymous throughout.

## Verdict

**No student passes, and the change did not work.** Training the two-tower 32M on people-only
histories (the agent's turns taken out, round 3's probabilities as the whole target) moved unnamed
requests answered from 10.7% to 11.2–13.4%, about seed noise, and cost 1.5–2.6 points on the pilot.
rc0.2's `agent-1x` build stays as it is.

| Arm (two-tower Ettin-32M, taught by round 3) | Unnamed answered | Unnamed held | Named answered | Pilot | Duplex-MPE | For others, answered outright |
|---|---|---|---|---|---|---|
| Round 3, 150M (the teacher) | 38.8% | 13.2% | 99.5% | 87.4% | 96.7% | 0.22% |
| rc0.2 `agent-1x` (no people-only lines) | 10.7% | 7.4% | 98.7% | 87.4% | 95.6% | 0.26% |
| People-only 25%, seed 0 | 13.4% | 7.8% | 99.0% | 85.6% | 95.5% | 0.44% |
| People-only 25%, seed 1 | 11.2% | 5.9% | 95.2% | 84.8% | 95.5% | 0.20% |
| People-only 50%, seed 0 | 11.7% | 9.0% | 99.1% | 85.9% | 95.5% | 0.43% |
| People-only 50%, seed 1 | 13.2% | 9.6% | 99.2% | 85.9% | 95.7% | 0.24% |
| Jev | 26.6% | 73% | 99.2% | 77.8% | 83.1% | 0.41% |

All six models answer none of AMI's 10,434 silence-test lines outright, get 47 of the demo's 48
lines, and score 99.9–100% on AMI's labelled meetings. Speed on agent-1x, full history encoded
ahead, one thread: 13–17 ms for every student, Jev 152 ms in the same container.

## The gate

Faster than Jev on agent-1x; within a point of round 3 on Duplex-MPE, AMI, the pilot and named
requests; unnamed requests answered more often than Jev; export parity.

| Model | Fails on |
|---|---|
| rc0.2 `agent-1x` | Duplex-MPE (−1.04 points), unnamed requests |
| People-only 25%, seed 0 | Duplex-MPE, pilot, unnamed requests |
| People-only 25%, seed 1 | Duplex-MPE, pilot, named requests (−4.3 points), unnamed requests |
| People-only 50%, seed 0 | Duplex-MPE, pilot, unnamed requests |
| People-only 50%, seed 1 | pilot, unnamed requests |

The two seed-0 arms also answer 0.43–0.44% of Duplex-MPE's lines for others outright, above item
2's bar of 0.4%.

## What this says

- **The missing agent turns are not why the small students miss unnamed requests.** With round
  3's answers on exactly such histories as targets, the 32M still answers about one in eight. Round
  3 reads something in those lines that a 32M does not pick up from our generated conversations.
- **The augmentation costs elsewhere**: the pilot drops 1.5–2.6 points, and named requests still
  swing with the seed (95.2% to 99.2%).
- The full per-run reports are in R2 under `runs/side/results/exp-055-side-round7*/`; the summary
  is `experiments/exp-055-side-round7/report.md`.
