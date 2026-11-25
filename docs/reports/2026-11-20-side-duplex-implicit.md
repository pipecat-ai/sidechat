# Why rc0.3 misses Duplex-MPE's unnamed requests

2026-11-20. A free check on stored predictions (no training, no API calls). Duplex-MPE is test
only: this reads its tags and counts simple features of its lines by code, and quotes no line.
Model: rc0.3's default build, `side-r9-ettin-150m-s1`, unless named.

## The question

Most of rc0.3's errors on Duplex-MPE are one kind of line: 1,413 of 1,898 errors are the
scenario's request to the assistant ("Aria") said without its name (scorecard item 5). Before
spending on it, can these be fixed from text at all, and would training on part of Duplex-MPE be
worth it?

## Findings

**1. The model is confident these lines are said to a person.**
- It ignores 57.4% (1,148/2,000; 55.2 to 59.6). For 1,144 of those 1,148, the intent it gives
  most weight is "other", with median probability 0.95.
- Every one of these lines has a named twin in the paired scenario (same context, the name added).
  The model answers 99.6% of the twins.

**2. A threshold can't buy them back cheaply.**
- The model does rank them above lines for people: `respond` separates them from Duplex-MPE's
  other lines with AUROC 0.965, and from its requests between people with 0.985.
- But the tail overlaps. Lowering the hold threshold from 0.4 to 0.05 engages 69.5% of the
  unnamed requests instead of 42.6% (answered or held). It also roughly doubles or triples holds on
  people's lines everywhere:

  | Hold if `respond` ≥ | Duplex unnamed requests engaged | Duplex lines for others | AMI | AMI heard | Ambient (all lines) |
  |---|---|---|---|---|---|
  | 0.4 (rc0.3) | 42.6% | 1.0% | 1.0% | 1.1% | 4.4% |
  | 0.1 | 62.1% | 2.4% | 1.4% | 1.7% | 7.1% |
  | 0.05 | 69.5% | 3.3% | 1.8% | 2.4% | 9.0% |
  | 0.02 | 79.3% | 5.4% | 2.7% | 3.5% | 12.7% |

  Round 3 and the `agent-1x` build show the same shape.

**3. Duplex-MPE phrases its requests to Aria the way real people ask each other.**
- In Duplex-MPE, a request to Aria has "you" or "your" in it 73.9% of the time (1,478/2,000; 71.9
  to 75.8). Requests between people there have it 22.1% of the time (845/3,821; 20.8 to 23.5).
- Real speech runs the other way:
  - Requests people said to an assistant in SLURP: 7.2% (196/2,705; 6.3 to 8.3).
  - AMI's requests and questions from one person to another: 36.5% (303/830; 33.3 to 39.8).
- The model follows real speech. It ignores 62.5% of Duplex-MPE's requests to Aria that contain
  "you" (924/1,478; 60.0 to 64.9), against 42.9% of those that don't (224/522; 38.7 to 47.2).

**4. Context moves it only a little.**
- When Aria was named in the line just before, the model answers 38.4% (157/409; 33.8 to 43.2).
- When Aria was never named earlier, it answers 25.4% (161/635; 22.1 to 28.9).
- Duplex-MPE's history also leaves out Aria's own replies. Those replies are the strongest cue the
  model reads (SD-13), and in real use they would be there.

**5. Real requests to an assistant are already caught.** rc0.3 holds 91% of SLURP's recorded
requests said in AMI meetings without a name (Jev: 82%).

## What it means

- **Training on half of Duplex-MPE is not worth it.** Most of what it would teach is its own style,
  "can you…" means the assistant, which is backwards in real speech. Gains on the other half would
  measure that style, and the model would likely hold more of people's real requests to each other.
  It would also spend half of the main independent benchmark.
- **Item 5's aim of 80% is not a fair target on Duplex-MPE as written.** Jev engages 99.8% of
  these lines, but only by holding nearly everything, including 16% of lines meant for people.
- **One real weakness remains: context.** The model barely uses "the assistant was just mentioned"
  or "a request only the assistant could do" when no name is said. That could be taught with
  generated lines of those kinds and measured on this set's 409 lines that follow a mention, but
  the room for gain is modest.
