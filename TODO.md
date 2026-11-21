# Where things stand

Updated 2026-11-21, after phase 9 (round 10 and int8). Before that: 2026-11-20, after the phase 8 checks (names as heard, an independent test). Earlier: 03:40 UTC, the end of the overnight run. Jon asked for autonomous work through the phases within $1,000
(SD-17), to have a model to test in the morning. Read the latest note in [notes/](notes/) first,
then this, then [DECISIONS.md](DECISIONS.md). How to try a model: [TESTING.md](TESTING.md).

## Done

| Phase | What | Note |
|---|---|---|
| 0 | Repo, schema, converters, the Jev baseline on 4 sets (exp-001) | [phase-0-baseline.md](notes/phase-0-baseline.md) |
| 1 | Labelling guide 0.2 with rules as code, the committee (99.2% on pilot-0.4), turn-rhythm context, scorecard 0.1 | [phase-1-guide.md](notes/phase-1-guide.md) |
| 2 | Guide 0.3 (anonymous speakers), the conversation generator, gen-pilot (8,426 lines), committee check of generated labels (95.3%), AMI test set, gen-0.1 | [phase-2-corpus.md](notes/phase-2-corpus.md) |
| 4 | Five training rounds. The pick, `side-r3-ettin-150m-s0`, meets 12 of 16 scorecard items: 99.0% right on the main test (Jev 80.7%), answers 0.2% of Duplex-MPE's lines for others outright (Jev 0.4%), none on the AMI silence test (Jev 5 of 10,434), 47/48 demo lines. Exported, in `models/`, runs in the demo's gate at 11 ms a line | [phase-4-models.md](notes/phase-4-models.md) |
| 5 | Round 6 (gen-0.4, committee 98.8%) did not beat round 3. Two-tower distilled students fit agent-1x (10 to 15 ms a line, Jev 56 to 163 ms) but lose unnamed requests; none passes every gate | [phase-5-round6.md](notes/phase-5-round6.md) |
| 5, part 2 | Student round 2 (exp-055): people-only histories taught by round 3; unnamed requests 11.2–13.4% (rc0.2 student 10.7%), pilot down 1.5–2.6 points. No student passes | [phase-5-students-round2.md](notes/phase-5-students-round2.md) |
| 5, part 3 | Round 8 (exp-059): real people's requests (SLURP's and CLINC150's text) in AMI meetings. Real unnamed requests held 91–95% as heard (was 4–17%, Jev 82%); costs about 1.5 points more holds on people's talk and more outright answers on Duplex-MPE. Default build not ready; the 32M seed 0 is a candidate for rc0.3's agent-1x | [phase-5-round8.md](notes/phase-5-round8.md) |
| 5, part 4 | Round 9 (exp-060): round 8 rebalanced (realreq-0.2, a hold bar on real dev lines, seed picks counting real lines). Dev's 150M pick meets round 3's 12 items with outright answers at round 3's level and real unnamed requests held 91% (Jev 82%); the 32M pick meets 11 (rc0.2 10), holds 87%, 14 ms on agent-1x. Cost: about 1 to 1.7 points more holds on people's talk (AMI, Ambient Bench), which fails the round's gate | [phase-5-round9.md](notes/phase-5-round9.md) |
| 6 | Real speech from found data (no calls can be recorded, SD-23): item 15 met by both builds on AMI's audio through Deepgram (gap 0.0 points; Jev holds 13–15% of people's lines). SLURP's real requests in AMI meetings: misheard names drop named requests answered from 85% to 13% (Jev 49%), and both builds ignore 82–97% of unnamed ones (Jev holds 82–90%) | [phase-6-real-speech.md](notes/phase-6-real-speech.md) |
| 7, part 2 | Release rc0.2 on `pipecat-ai/sidechat` (tag `rc0.2`, commit `08c9b8c`): round 3's 150M at the root, unchanged, and the two-tower 32M as `agent-1x/` (10 to 15 ms a line on agent-1x; answers 10.7% of unnamed requests, Jev 26.6%). The label for unnamed requests stays (SD-21) | [phase-7-release-rc0.2.md](notes/phase-7-release-rc0.2.md) |
| 7, part 3 | Release rc0.3 on `pipecat-ai/sidechat` (tag `rc0.3`): round 9's 150M at the root (fp32; int8 failed parity and round 3's was removed) and round 9's two-tower 32M as `agent-1x/`. Both hold most real unnamed requests (91% and 87%, Jev 82%) and hold about 1% of people's real meeting lines (rc0.2 about 0.1%) | [phase-7-release-rc0.3.md](notes/phase-7-release-rc0.3.md) |
| 7, part 1 | Pipecat module `pipecat.models.labs.side_chat` (gate, listener, classifier, model), downloading `pipecat-ai/sidechat` at commit `c9b59be`, on pipecat branch `jpt/sidechat`; parity with this repo's runtime on 6,544 lines; a Labs docs page on pipecat-docs branch `jpt/labs-sidechat`. Neither committed | [phase-7-pipecat.md](notes/phase-7-pipecat.md) |
| 8 | Ceiling checks (exp-062, exp-063): Duplex-MPE's unnamed requests are mostly the benchmark's style; the name as heard is at the text ceiling with the keyterm; on TCL's independent test rc0.3 ties Jev on answering now (F1 0.725 against 0.717) and holds a tenth as often, and its weak spot is the line right after the agent answers (AUROC 0.67) | [phase-8-ceiling-checks.md](notes/phase-8-ceiling-checks.md) |
| 9 | Round 10 and rc0.3.1 (exp-064 to exp-075): gen-0.5's kinds for the line after the agent answers. The teacher learned the new kind (97% left alone, rc0.3 67%) but not TCL's distinction (AUROC 0.66, outright answers not down beyond noise); students cut TCL's outright answers but lose named requests. Nothing ships: the dev pick of four students misses one margin by one line (Ambient Bench). int8 fixed for both of rc0.3's builds and released as rc0.3.1 (opt-in): within a point of fp32 on every test set | [phase-9-round10.md](notes/phase-9-round10.md) |

## Next

- **Review** (held for Jon): commit and open the pipecat PR (draft text and changelog in
  [phase-7-pipecat.md](notes/phase-7-pipecat.md)) and the docs PR.
- **Dataset** (held for Jon): `sidechat-gen-0.1`, our generated corpora gen-pilot to gen-0.3 as
  Parquet with a card, 404,715 lines (exp-040, `sidechat/pipeline/dataset.py`), is on the Hub as
  the private dataset `pipecat-ai/sidechat-gen` (exp-051). Confirm the card's licence
  (bsd-2-clause, as the model) before making it public. gen-0.4 can join once its committee check
  is in.
- **Try it on a real call**: `examples/labs/labs-sidechat-group-conversation.py` in the pipecat
  checkout, with two or three people.
- **rc0.2 is out** with an opt-in `agent-1x/` build. Its gap is unnamed requests (item 5). The
  label is not the cause (SD-21): the small models read those lines as said to a person.
- **Student round 2 did not help** (exp-055, [phase-5-students-round2.md](notes/phase-5-students-round2.md)):
  people-only histories moved unnamed requests from 10.7% to 11.2–13.4% and cost the pilot 1.5–2.6
  points. No student passes; rc0.2 stays as released. Stop student rounds on item 5 for now.
- **Pipecat** downloads the root build pinned at `c9b59be`; rc0.2's root files are identical, so
  nothing changes there. Running `agent-1x/` in Pipecat needs a two-tower port and the tokenizer
  truncation fix (exp-036).
- **Phase 6 is done from found data** ([phase-6-real-speech.md](notes/phase-6-real-speech.md)). Names: pass the
  agent's name to the speech-to-text service as a keyterm (named requests heard 13% to 74%); name
  spellings as aliases are left off (SD-24). Unnamed requests with real people's wording:
  rounds 8 and 9 ([phase-5-round9.md](notes/phase-5-round9.md)). Shipped as rc0.3
  (SD-26, [phase-7-release-rc0.3.md](notes/phase-7-release-rc0.3.md)). Jobs that launch others no
  longer run twice when Modal preempts them (SD-25).
- **Duplex-MPE's unnamed requests are mostly a style gap, not a model gap**
  ([2026-11-20-side-duplex-implicit.md](reports/2026-11-20-side-duplex-implicit.md)). Its requests
  to the assistant say "you" 74% of the time, which is how real people ask each other (AMI 37%),
  not how they ask assistants (SLURP 7%). Don't train on it.
- **Names as heard are at the text ceiling with the keyterm**
  ([2026-11-20-side-names-as-heard.md](reports/2026-11-20-side-names-as-heard.md), exp-062): of the
  named requests the keyterm still loses, half have no trace of the name and most of the rest are
  ordinary words ("only", "you"). No rule recovers them without answering people. Remaining options:
  an independent test (TCL `intelligent_wakeup`, test only); context-only requests from the
  generator (modest gain); timing input (a model change); a speech-to-text setting that keeps the
  name more often (about $0.30 a configuration on the names dev set).
- **On an independent test, rc0.3 answers as well as Jev and holds a tenth as often**
  ([2026-11-20-side-tcl-wakeup.md](reports/2026-11-20-side-tcl-wakeup.md), exp-063, SD-27). On TCL's
  Intelligent Wakeup (text only, test only): F1 0.725 against Jev's 0.717, and 3% of people's
  lines held against 37%. Named requests are answered 98.7%. TCL's audio model, trained on its own
  data, reaches 0.890. The gap is the line right after the agent answers (AUROC 0.67), so timing
  input is the next real step. Generated follow-ups are the text-side option.

- **Round 10 did not move TCL's weak spot** ([2026-11-20-side-round10.md](reports/2026-11-20-side-round10.md)).
  Generated questions and comments to the others right after the agent were learned in
  distribution, but TCL's lines there stayed as hard (AUROC 0.66). Stop generated kinds aimed at
  TCL's errors: more would be tuning on a test set. Timing input is the next real step (Jon's design
  call).
- **rc0.3.1 is out** (SD-29, exp-075): rc0.3's builds unchanged, plus int8 files for both, opt in
  with `int8=True`. Tag `rc0.3.1`; `rc0.3` and `rc0.2` stay. Within a point of fp32 on every test set;
  on capped containers the default build is 1.5 times faster in int8 (303 ms against 465 at 1 vCPU)
  with 0.3 GB less memory. The recipe is now in `export.py` for every later export. Pipecat's
  download is still pinned at `c9b59be`.
- **Round 10's student s2 missed by one line** (held for Jon): it fails only Ambient Bench's margin
  (79 lines fewer right where 78.97 are allowed). It answers a third fewer of TCL's people's lines
  outright, but half as many of Duplex-MPE's unnamed requests. Nothing ships unless Jon waives the
  margin.

## The bar

Jev answers 99.2% of named requests at once but only 26.6% of the same requests unnamed; on the
pilot it answers at once 47.1% of lines for the agent that carry no name. It holds for a pause on
15 to 18% of lines meant for someone else (14.8% on real AMI meetings). Full detail:
[contracts/scorecard-0.1.md](contracts/scorecard-0.1.md).

## Held for Jon

- Commit: phase 8 is committed and pushed (`1c0f862`). Phase 9's work (gen-0.5, round 10, int8)
  is in the working tree, not committed.
- The opt-in call log in `daily-audience` (SD-08, SQ-05). Nothing in `daily-audience` has been
  edited; TESTING.md shows the one-line swap to try Sidechat there.
- Open questions SQ-01 and SQ-03 to SQ-07 in DECISIONS.md, each with a default assumed.
- SQ-09: does a person coming back to the agent's answer later, without its name, get an answer
  (the committee's majority, TCL's label) or a hold (our label)? `follow_up_later` stays out of
  training until settled. SD-28 (gen-0.5's kinds) is an agent default to confirm.
- SD-18 (guide 0.4: a named thanks, stop or goodbye is answered briefly), SD-19 (AMI's unlabelled
  meetings in training) and SD-20 (a real-speech bar on thresholds) are agent defaults to confirm.

## Open debts

- The demo rewrites every alias of the bot's name before asking Jev, so "at last a number that
  makes sense" is sent as "Atlas a number that makes sense". A bug in `daily-audience`.
- Jev's price per token is from Audience's repo, not confirmed.
- Dataset licences in DATASETS.md are Hub tags; check each source's own licence before training.
- Eight turns of history can miss state the agent holds (exp-004's timer line).
- int8 holds up for 150M only (exp-027), not 68M (exp-023). Latency on this Mac is 7 to 52 ms a
  line depending on history and threads, against Jev's 165 ms (exp-032). On cloud CPUs it is
  slower than Jev: about 250 ms with a full window on 1 vCPU and 530 ms (int8) on `agent-1x`, where
  fp32 does not fit (exp-033). Next for speed: a smaller encoder, fewer context tokens, and a
  default of 1 thread in the Pipecat adapter.
- Trial objects in R2 are safe to delete: `runs/side/results/exp-000-side-trial/`,
  `exp-002-side-committee-trial/`, `exp-009-side-gen-trial/`, `exp-013-side-train-smoke/`,
  `exp-014-side-export-smoke/`, `runs/side/baselines/trial-0/`, `runs/side/labels/trial-committee-0/`,
  `runs/side/corpus/gen-trial/`, `models/side/side-smoke-ettin-32m-s0/`.
