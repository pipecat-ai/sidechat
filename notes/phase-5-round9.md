# Phase 5 notes, part 4: round 9, round 8 rebalanced

2026-11-20. Jon said "Rebalance first" before any rc0.3 decision. Round 9 ran (exp-060). Read this,
then [TODO.md](../TODO.md).

## What was done

- **`realreq-0.2`** (`sidechat/sources/realreq.py`, `VERSIONS`):
  - 5,000 training requests and 1,000 dev requests (round 8: 12,000 and 2,000).
  - 45% unnamed and held, 25% naming the agent, 30% naming a person (round 8: 15% naming a person).
- **A hold bar on real dev lines:** `choose_thresholds(max_held_real=...)` in
  `sidechat/train/evaluate.py`. Round 9 used 0.2% of AMI's 4,186 real dev lines.
- **Seed picks count real lines:** `dev_pick` in `round8.py` counts AMI's real dev lines left alone
  as well as generated dev decisions.
- **Same recipe otherwise:** `round8.py` with `--tag r9 --realreq realreq-0.2 --max-held-real 0.002`.
- **Scorecards for all four models:** `reports/2026-11-20-side-r9*-scorecard.md`.
- **No more duplicate jobs after a preemption:** Modal preempted the round's job, which launched its
  jobs a second time (as in round 8). Jobs that launch others are now non-preemptible and reattach
  to the calls they already made after a restart (`sidechat/lib/resume.py`, SD-25). This was
  checked on Modal with a throwaway job of well under a cent. Round 9 itself ran the old code.

## Results

[reports/2026-11-20-side-round9.md](../reports/2026-11-20-side-round9.md).

- **Dev's picks:** `side-r9-ettin-150m-s1` and `side-r9tt-ettin-32m-s1`.
- **The 150M pick:**
  - Meets the same 12 scorecard items as round 3.
  - Answers Duplex-MPE's lines for others outright as rarely as round 3 does (0.21% against 0.22%).
  - Holds 90.9% of real unnamed requests as heard (round 3: 16.7%; Jev: 82.3%).
- **The 32M pick:**
  - Meets 11 items to rc0.2's 10.
  - Holds 86.6% of real unnamed requests (rc0.2: 3.6%).
  - Takes 14 ms on agent-1x (Jev: 49 ms).
- **The remaining cost is holds on people's own talk, about 1 to 1.7 points more:**
  - AMI: 0.1% to 1.0–1.3%.
  - Ambient Bench: 1.1% to 2.1–2.8%.
  - Jev holds about 14.6–14.8% on these sets.

  Most of the held AMI lines are nameless questions between people. Thresholds don't move them.
- **The gate:** by its round 8 margins (0.5 points on AMI and the Ambient Bench), neither pick
  ships.
- **Cost:** about $35, of which about $17 was the duplicate runs.

## Things learned

- **Balance worked.** Fewer real requests and more said to a person halved round 8's holds on
  people's talk and brought outright answers back to round 3's level, for a few points of real
  requests held.
- **The remaining trade is in the text, not the threshold.** Without a name, "what's the price of
  that?" said to the room and a request to an assistant look alike. The model holds about one in
  ten of AMI's nameless questions for information. A threshold change from 0.40 to 0.55 moves
  holds by 0.1 point.
- **The dev hold bar can't see this.** AMI's dev series leave questions out (SD-19), so the bar held
  every model to 6 to 8 lines while the test sets, which include questions, show about 1%.
- **Counting real lines in the seed pick helped.** This time dev picked the seed that meets item 2
  and item 5.
- **Item 5 on Duplex-MPE dropped for the 150M** (38.8% to 29.3%, still above Jev) while real
  requests rose. These are two skills (round 8). Round 9's data helps the real one.
- **Modal preempts CPU containers too.** A job that launches others must not launch them twice
  (SD-25).

## Loose ends

- Nothing committed or published. Round 9's models stay in R2.

## Where the next phase picks up

1. **Decide rc0.3** (Jon): ship `side-r9-ettin-150m-s1` as the default and `side-r9tt-ettin-32m-s1`
   as `agent-1x`, with the holds stated plainly, or keep rc0.2. The gate's margins were mine; the
   trade they block is a product call.
2. If rc0.3 ships: publish with `sidechat/pipeline/publish.py` (root and `agent-1x/`), update the
   card and README tables from the report, and tag `rc0.3`.
3. If not: a round 10 that adds AMI's own questions between people to training as left alone, to
   cut holds further. This conflicts with SD-19's reading of them as possible even calls, so it
   needs a guide decision first.
