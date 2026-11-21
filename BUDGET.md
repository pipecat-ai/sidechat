# Budget

In US dollars. Cap for the whole project: **$1,000**, set by Jon on 2026-11-18 (SD-17). Every paid run gets a forecast in its `record.yaml` before it starts and a line
here after.

Jev's price is taken as $0.042 per million input tokens, the figure recorded in Audience's repo.
It has not been confirmed with TypeSafe, and output tokens are not priced here. Modal lines are
estimates from run time, not read from billing.

## Ledger

`date · experiment · what · forecast · actual`
- 2026-11-18 · exp-000-side-trial · Trial of the baseline job on three conversations per set: 88
  Jev requests, one CPU container for 11 s plus the image build · under $0.05 · about $0.01
  (71,879 input tokens = $0.003; Modal seconds)
- 2026-11-18 · exp-001-side-jev-baseline · Jev baseline on all four Phase 0 sets, about 57,400
  requests · about $2.00 · about $2.08 (48,333,777 input tokens = $2.03; one CPU container for 980 s,
  about $0.05)
- 2026-11-18 · exp-002-side-committee-trial · Committee trial on the first 2 pilot conversations:
  17 lines x 3 members, one CPU container for 24 s · under $1 · about $0.65 ($0.64 committee
  estimate from tokens; Modal seconds)
- 2026-11-18 · exp-002-side-committee-pilot · Committee on all 283 pilot lines, guide 0.1 · about
  $11 · about $6.86 (a $0.77, b $1.32, c $4.75; Modal about $0.02)
- 2026-11-18 · exp-003-side-jev-pilot-0.2 · Jev re-scored on the guide-labelled pilot and the demo
  lines from stored answers; 0 new requests, one CPU container for 50 s · under $0.05 · about
  $0.01
- 2026-11-18 · exp-004-side-committee-guide-0.2 · Committee on pilot-0.3, guide 0.2 · about $7.50 ·
  about $8.04 (a $0.86, b $1.66, c $5.50; Modal about $0.02)
- 2026-11-18 · exp-005-side-committee-pilot-0.4 · Re-score of exp-004's answers on pilot-0.4, all
  reused · about $0.01 · about $0.01
- 2026-11-18 · exp-006-side-jev-pilot-0.4 · Jev re-scored on pilot-0.4 from stored answers · about
  $0.01 · about $0.01
- 2026-11-18 · exp-007-side-committee-anonymous · Committee on pilot-0.4@anonymous, guide 0.3 · about
  $8 · about $8.12
- 2026-11-18 · exp-008-side-jev-anonymous · Jev on pilot-0.4@anonymous, 283 new requests · about
  $0.02 · about $0.02
- 2026-11-18 · exp-009-side-gen-trial · Generator trial, 32 conversations · about $2 · about $0.61
- 2026-11-18 · exp-010-side-gen-pilot · Generator pilot, 599 conversations · about $5 · about $3.49
- 2026-11-18 · exp-011-side-committee-gen-pilot · Committee on 430 generated lines · about $13 · about $12.27
- 2026-11-19 · exp-012-side-gen-0.1 · Full corpus, 8,095 conversations · about $46 · about $43
- 2026-11-19 · exp-013-side-train-smoke · Training smoke test · about $1.50 · about $0.60
- 2026-11-19 · exp-014-side-export-smoke · Export smoke test · about $0.05 · about $0.05
- 2026-11-19 · exp-015-side-jev-ami · Jev on AMI, 8,875 requests · about $0.35 · about $0.30
- 2026-11-19 · exp-016-side-jev-gen-test · Jev on 6,000 generated test requests · about $0.25 · about $0.20
- 2026-11-19 · exp-017-side-train-r1 · Training round 1, three sizes · about $15 · about $3 (H100:
  1,662 s training, about 870 s scoring)
- 2026-11-19 · exp-018-side-export-r1 · Export of side-r1-ettin-68m-s0, fp32 and int8 · about $0.30 · about $0.30
- 2026-11-19 · exp-023-side-export-r1b · Re-export with the fixed int8 path · about $0.30 · about $0.10
- 2026-11-19 · exp-022-side-train-r2 · Training round 2, 68M and 150M · about $6 · about $5 (H100 about 2,550 s training, 900 s scoring)
- 2026-11-19 · exp-024-side-committee-gen-0.2 · Committee on 360 lines of gen-0.2's new kinds · about $10 · about $11
- 2026-11-19 · exp-025-side-train-r3 · Training round 3 (round 2 with unsettled instructions filtered) · about $6 · about $5
- 2026-11-19 · exp-027-side-export-r3 · Export of side-r3-ettin-150m-s0 · about $0.30 · about $0.40
- 2026-11-19 · exp-026-side-gen-0.3 · Corpus gen-0.3, 9,000 conversations · about $23 · about $23
- 2026-11-19 · exp-028-side-train-r4 · Training round 4, 68M and 150M, seed 0 · about $7 · about $7
- 2026-11-19 · exp-029-side-train-r4-s1 · Training round 4, 150M, seed 1 · about $4 · about $4
- 2026-11-19 · exp-030-side-train-r5 · Round 5 ablation without AMI rows, 150M seed 0 · about $4 · about $4
- 2026-11-19 · exp-031-side-train-r5-s1 · Round 5 ablation without AMI rows, 150M seed 1 · about $4 · about $4
- 2026-11-19 · exp-019-side-gen-0.2 · Corpus gen-0.2, 11,500 conversations · about $34 · about $32
- 2026-11-19 · exp-020-side-jev-ami-silent · Jev on the AMI silent test, 10,434 requests · about $0.35 · about $0.35
- 2026-11-19 · exp-021-side-rescore-r1 · Round 1 rescored under round 2's scoring · about $1.50 · about $0.60
- 2026-11-19 · exp-032-side-latency · Latency beside Jev on this Mac, about 140 Jev requests · under $0.01 · under $0.01
- 2026-11-19 · exp-033-side-latency-cloud · Latency on Pipecat Cloud-shaped CPU containers, two runs · under $0.50 · about $0.20
- 2026-11-19 · exp-034-side-publish · Model, card and training rows to the Hub · under $0.50 · under $0.10
- 2026-11-19 · exp-040-side-dataset · Generated corpora as a Parquet dataset for the Hub, in R2 · under $0.25 · about $0.01
- 2026-11-19 · exp-051-side-dataset-upload · That dataset to the Hub, private · under $0.05 · under $0.01
- 2026-11-19 · exp-035-side-gen-0.4 · Corpus gen-0.4, 7,296 conversations (round 6 data) · about $19 · about $20
- 2026-11-19 · exp-036-side-tt-smoke · Two-tower and distillation smoke test, two exports · about $2 · about $1.50
- 2026-11-19 · exp-042-side-round6 · Round 6 and the agent-1x students, chained (exp-037 to exp-049) · about $36 · about $38
- 2026-11-19 · exp-050-side-round6-reexport · Exports and agent-1x timing again after the tokenizer fix, plus three parity probes · about $3.50 · about $3
- 2026-11-19 · exp-051-side-students-r3 · Two-tower students taught by round 3, exports, timing · about $9 · about $13.50
- 2026-11-19 · exp-052, exp-053 · The round 3 students again: seed 1, and teacher share 0.5 · about $18 · about $26
- 2026-11-19 · exp-054-side-publish-rc0.2 · rc0.2 to the Hub: the agent-1x build and its rows · under $0.50 · under $0.05
- 2026-11-19 · exp-055-side-round7 · Student round 2 for agent-1x: people-only histories, 4 students, exports, timing · about $25 · about $19
- 2026-11-19 · exp-056-side-phase6-stt · AMI's headset audio through Deepgram; Jev and two models on what was heard · about $9 · about $5.50
- 2026-11-19 · exp-057-side-phase6-slurp · SLURP's recorded requests in AMI meetings, written and heard; Jev and two models · about $3 · about $1.80
- 2026-11-19 · exp-058-side-phase6-names · The agent's name as heard: Deepgram keyterm, name spellings as aliases, both builds on every set · about $3.50 · about $2.10
- 2026-11-19 · exp-059-side-round8 · Round 8: real people's requests in training; two 150M teachers, two 32M students, exports, timing · about $32 · about $30
- 2026-11-20 · exp-060-side-round9 · Round 9: round 8 rebalanced (realreq-0.2, a hold bar on real dev lines); two 150M teachers, two 32M students, exports, timing · about $28 · about $35 (about $17 of it duplicate runs after a Modal preemption, SD-25)
- 2026-11-20 · exp-061-side-publish-rc0.3 · rc0.3 to the Hub: round 9's two builds and their rows · under $0.50 · under $0.05
- 2026-11-20 · exp-062-side-names-dev · SLURP's train and devel recordings that say the name, through Deepgram, plain and with keyterm · about $1.50 · about $0.90
- 2026-11-20 · exp-063-side-tcl-wakeup · An independent test: TCL's Intelligent Wakeup, test split,
  text only; Jev and rc0.3's and rc0.2's builds, speakers named and anonymous · about $1 · about
  $0.40 (Jev $0.25 for 7,293 requests, 5,921,211 input tokens; Modal about $0.15)
- 2026-11-20 · exp-064-side-gen-0.5 · Corpus gen-0.5, 5,997 conversations aimed at the line after the agent
  answers (round 10 data) · about $21 · about $23 (o $1.75, a $5.23, c $7.93, b $7.82, CPU about $0.40)
- 2026-11-20 · exp-065-side-committee-gen-0.5 · Committee on 360 lines of gen-0.5's three new kinds · about
  $11 · about $11.35 (a $1.25, b $2.41, c $7.65)
- 2026-11-20 · exp-066-side-round10 · Round 10: two teachers and two students with gen-0.5, exports, timing;
  Jev on gen-0.5's test · about $35 · about $23 (H100 about $20, CPU about $1.50, Jev $0.48)
- 2026-11-20 · exp-067, exp-068 · Why the default build's int8 fails parity, two probe sets · about $0.55 ·
  about $0.50
- 2026-11-20 · exp-069-side-int8-rc0.3 · rc0.3's default build in int8 with the new recipe, through the
  export's gate · about $0.40 · about $0.40
- 2026-11-20 · exp-070-side-int8-rc0.3-check, -b · That int8 file on the test sets against fp32's stored
  predictions, in two 8-CPU containers (Duplex-MPE took the first one's two hours) · about $0.50, then
  $0.50 more · about $1.30
- 2026-11-21 · exp-071-side-round10-students · Two more round 10 students (seeds 2 and 3), three
  exports, agent-1x timing · about $15 · about $16 (two H100s about 1.75 hours, about $14; CPU about $2)
- 2026-11-21 · exp-072-side-int8-rc0.3-agent1x · rc0.3's agent-1x build (two towers) in int8 with the
  new recipe, through the export's gate · about $0.30 · about $0.10
- 2026-11-21 · exp-073-side-int8-rc0.3-agent1x-check, -b · That int8 build on the test sets against fp32's
  stored predictions, in two 8-CPU containers · about $0.70 · about $0.35
- 2026-11-21 · exp-074-side-latency-int8 · rc0.3's two builds in fp32 and int8 on containers capped like
  agent-1x and agent-2x, for rc0.3.1's card · about $0.20 · under $0.10
- 2026-11-21 · exp-075-side-publish-rc0.3.1 · Release rc0.3.1 (int8 files for both builds), two publish
  jobs · under $0.50 · under $0.05

Note for Phase 3: member c costs 6 to 7 times member a, because its provider cached almost none of
the shared prompt (about 7% of input tokens against 95% for a and b). At the plan's ~5,500
committee lines that is about $100 for c alone. Its batch API is half price.

## Total

About $462 spent of the $1,000 cap. Nothing in flight.
