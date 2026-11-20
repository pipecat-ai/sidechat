# Phase 5 notes, part 3: round 8, real people's requests in training

2026-11-20. Jon said "do it" to teaching unnamed requests with real people's wording. Round 8 ran
(exp-059). Read this, then [TODO.md](../TODO.md).

## What was done

- **`realreq`** (`sidechat/sources/realreq.py`, a corpus name `_corpus_rows` builds on the fly):
  12,000 train and 2,000 dev requests from SLURP's text (train and devel splits, CC BY 4.0; any
  request also in its test split is left out) and CLINC150's in-scope queries (CC BY 3.0). Each is
  said at a seeded point in one of AMI's unlabelled training or dev meetings, never the labelled
  meetings or the silence test. Formatted as speech-to-text with formatting writes. Labels by guide
  0.4: 60% unnamed and held, 25% with the agent's name added and answered, 15% with a person's name
  added and left alone.
- **Round 8** (`sidechat/pipeline/round8.py`): Ettin-150M on round 3's corpus plus `realreq` (two
  seeds); two-tower Ettin-32M students distilled from the dev-picked seed with `realreq` added (two
  seeds); exports; agent-1x timing; gates against the released builds
  (`student_gate.gate_default`, `metrics_r8`). Scoring now slices SLURP and generated sets by kind.
- Scorecards for all four: `reports/2026-11-20-side-r8*-scorecard.md`.

## Results

[reports/2026-11-20-side-round8.md](../reports/2026-11-20-side-round8.md).

- Real unnamed requests in meetings, as heard, are held 91–95% (released builds 4–17%, Jev 82%).
  Named requests improve too.
- Duplex-MPE's unnamed requests move less: 38.8% to 46.5% for one 150M seed, unchanged otherwise.
- Costs: about 1.5 points more holds on people's talk (AMI, Ambient Bench; still far under Jev), and
  answers outright on Duplex-MPE's lines for others up from 0.22% to 0.40% or 0.56%.
- Dev cannot separate the 150M seeds and picks the one over item 2's bar, so the default build is
  not ready. The 32M seed 0 (dev's pick) meets 11 scorecard items to rc0.2's 10.
- About $30; each teacher's job ran twice. Round 9's logs show the likely cause: Modal preempts the
  CPU container of a job that launches others and restarts it on the same input, and the restarted
  job launches its jobs again. Fixed after round 9 started (`sidechat/lib/resume.py`, SD-25).

## Things learned

- Real wording transfers: a model taught people's own requests holds people's own requests. Context
  alone (Duplex-MPE) is a different skill, and this data barely teaches it.
- Teaching "hold for this kind of request" spreads to people's request-like talk. The fix is
  balance: fewer such lines, or more requests between people in the same meetings.
- Seed variance on outright answers (0.40% against 0.56%) is as large as the effect being gated.
  Dev decides seeds and it cannot see this; a dev bar on answers outright for real people's lines
  (as SD-20 has for AMI's dev series) would.

## Loose ends

- Nothing committed or published. Round 8's models stay in R2.

## Where the next phase picks up

1. **Decide rc0.3's `agent-1x` build**: round 8's 32M seed 0 (more scorecard items and real requests
   held) or rc0.2's (fewer holds on people's talk).
2. **Round 9 for the default build**: `realreq` at a lower share or with requests between people in
   the same meetings, and a dev bar on answering people's lines outright, so the seed pick can see
   item 2.
