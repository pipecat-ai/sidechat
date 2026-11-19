# Phase 5 notes, part 2: student round 2 for agent-1x

2026-11-19. Jon said "Yes, start it" to a second student round aimed at unnamed requests (item 5).
It ran (exp-055) and did not help. rc0.2 stays as released. Read this, then [TODO.md](../TODO.md).

## What was done

- **The idea.** Every model reads Duplex-MPE's unnamed requests as said to a person or to the agent
  (SD-21). Round 3 answers 38.8% of them, the rc0.2 student 10.7%. The students had only ever seen
  full transcripts, with the agent's turns in the history. So a share of training lines lost the
  agent's turns and took round 3's probabilities as their whole target, as a transcript of only the
  people's speech looks (`conditions.people_only`, `train(people_only=...)`).
- **The round.** Four two-tower Ettin-32M students, otherwise exactly the rc0.2 student's training:
  people-only share 0.25 and 0.5, seeds 0 and 1. Exports, timing on agent-1x and agent-2x beside
  Jev and the rc0.2 build, and a summary with the gate, all chained in one detached job
  (`sidechat/pipeline/round7.py`; the gate is in `sidechat/pipeline/student_gate.py`).
- **Dropped from the plan, with reasons.** Picking a checkpoint on named requests: every past
  student's best epoch was its last. New generated lines: the generator already makes these kinds,
  and the students get them right on our own test.
- **Disclosed in the record.** The augmentation copies a property of Duplex-MPE's format (its card
  says the assistant's replies are not in the manifests), so any Duplex-MPE gain would partly be
  that match.

## Results

[reports/2026-11-19-side-round7-students.md](../reports/2026-11-19-side-round7-students.md).

| | Unnamed answered | Pilot | Named answered |
|---|---|---|---|
| Round 3 (teacher) | 38.8% | 87.4% | 99.5% |
| rc0.2 `agent-1x` | 10.7% | 87.4% | 98.7% |
| Round 7 students (4) | 11.2% to 13.4% | 84.8% to 85.9% | 95.2% to 99.2% |
| Jev | 26.6% | 77.8% | 99.2% |

No student passes the gate. All are 13 to 17 ms a line on agent-1x (Jev 152 ms in the same
container). About $19.

## Things learned

- **The missing agent turns are not why a 32M misses unnamed requests.** Trained on round 3's
  answers for exactly such histories, it still answers about one in eight. Round 3 reads something
  in those lines that a 32M does not learn from our generated conversations.
- **People-only lines cost the pilot 1.5 to 2.6 points**, and two arms answer 0.43–0.44% of
  Duplex-MPE's lines for others outright, above item 2's bar.
- The gate now runs in code for every student, including the released one: rc0.2's build fails it
  on Duplex-MPE by 0.04 points beyond the one-point margin, and on unnamed requests.

## Loose ends

- Not committed: `round7.py`, `student_gate.py`, `conditions.people_only` and the `people_only`
  option in `train.py` (off by default; earlier runs replay unchanged), tests, this note, the report.
- Round 7's student models stay in R2 (`models/side/side-r7po*-ettin-32m-s*`), unpublished.

## Where the next phase picks up

1. **Stop student rounds on item 5 for now.** Two rounds and eight 32M students are all between 6%
   and 20%. More training tricks on generated data are unlikely to reach Jev's 26.6%.
2. **Real calls (phase 6, SQ-05)** decide whether unnamed requests to a quiet agent matter in use.
   If they do, the options are a bigger student that still fits agent-1x, or the harness holding
   such lines for a pause on its own (Jev's behaviour) rather than the model.
