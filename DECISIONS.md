# Decisions

Newest first. `date · id · who · decision · why · reversible?`. "Agent default" means the agent
chose it and Jon has not yet confirmed. Open questions are at the bottom.

- 2026-11-20 · SD-26 · Jon · Release rc0.3 on `pipecat-ai/sidechat`: round 9's dev picks replace
  both builds, `side-r9-ettin-150m-s1` at the root (fp32 only) and `side-r9tt-ettin-32m-s1` in
  `agent-1x/`. They fail round 8's gate margins only on holds of people's talk (AMI about 1% from
  0.1%, the Ambient Bench 2 to 3% from 1%, never answered outright), in exchange for holding 87 to
  91% of real unnamed requests (rc0.2: 17% and 4%; Jev 82%). The card states the trade. Round 3's
  int8 file leaves the root, since round 9's int8 failed parity. · Jon: "Ship rc0.3", after the
  round 9 report. · Reversible: tag `rc0.2` keeps the old builds.

- 2026-11-20 · SD-25 · Jon ("Yes, fix it") · Jobs that launch other jobs (the round job,
  `train_run`, `latency_run`, the generator's `run`) are `nonpreemptible`, and the round job and
  `train_run` record the calls they spawn so a restart waits on them instead of launching them
  again (`sidechat/lib/resume.py`). · exp-060's logs: Modal preempted the round's job an hour in and
  restarted it on the same input, and it trained both teachers and the students a second time
  (about $17 wasted); round 8's teachers ran twice too. Modal charges 3x for a non-preemptible
  container's CPU and memory, a few cents for these; GPU jobs cannot be non-preemptible and do not
  need to be. Checked on Modal with a throwaway job: a running or finished call is reattached, a
  cancelled one is launched afresh. · Reversible: drop the flag.

- 2026-11-19 · SD-24 · agent default · Pass the agent's name (and any aliases) to the
  speech-to-text service as a keyterm; do not add other spellings of the name as aliases at runtime.
  · exp-058: Deepgram's keyterm took named requests answered as heard from 13% to 74% (default
  build) and 7% to 59% (`agent-1x`), and put the name into 4 of 2,705 requests that never said it.
  Spellings as aliases helped only the 32M, a little, and cost named requests and false answers
  elsewhere. · Reversible: `sidechat/names.py` stays for measurement.

- 2026-11-19 · SD-23 · Jon · No real calls can be recorded ("we have to work with what we can
  find"). Phase 6 uses found real speech instead: AMI's headset audio through Deepgram for item 15,
  and SLURP's recordings of people speaking to an assistant, spliced into AMI meetings, for
  requests to the agent in real speech. SLURP's audio is CC BY-NC 4.0 (its text is CC BY 4.0): Jon
  allows it for testing only, never training, and its audio and converted rows stay out of git and
  off the Hub. · Jon: "Yes, test only". · Reversible: drop the SLURP sets.

- 2026-11-19 · SD-22 · Jon (delegated) · Release rc0.2 on `pipecat-ai/sidechat`: round 3's 150M
  stays the default at the repo root, unchanged, so Pipecat's pinned download is unaffected, and
  the two-tower 32M student (`side-r6ttr3t-ettin-32m-s0`, fp32) ships as an opt-in `agent-1x/`
  build. It passes the gate as Jon set it (faster than Jev on agent-1x with a full history; within
  about a point of round 3 on Duplex-MPE, AMI and the pilot) but answers fewer unnamed requests
  than Jev (item 5), which the card says plainly. · Jon: "push and ship this on hugging face, we
  can call this RC0.2". · Reversible: delete `agent-1x/` on the Hub; the tag stays.

- 2026-11-19 · SD-21 · Jon (delegated) · Unnamed requests to an agent that has not spoken keep
  guide 0.4's label: a request open to the room is `wait` with `respond` 0.5 (SD-11, SD-12). No
  relabel. · Measured on stored predictions (tags only): every model reads Duplex-MPE's implicit
  requests as said to a person or to the agent, almost never as open (median open intent 0.01;
  intent `other` for 52% to 84% of them), so neither "held" nor "even call" changes what any model
  does there. Item 5 also swings with the seed and round (150M: 22.8% to 47.2% answered now;
  round 1's labels-only 68M: 61%), so it is a reading-the-context problem, not a label problem. ·
  Reversible: a guide revision.

- 2026-11-19 · SD-20 · agent default · Thresholds get a second bar on dev: answer at most 0.4% of
  real-speech lines meant for people outright, measured on AMI's two dev series (4,186 lines). The
  generated dev alone allowed thresholds that answered 0.8% of Duplex-MPE's and AMI's lines for
  others outright, twice item 2's bar. · Round 1 (exp-017): about 0.3% on generated dev, 0.8 to
  1.9% on real and benchmark speech. · Reversible: one argument in `choose_thresholds`.

- 2026-11-19 · SD-19 · agent default · AMI meetings without addressee labels are used for
  training. Of the 117, those in series that share no speaker with the 22 labelled meetings are
  split by series: 20 series train (15,276 sampled lines), 2 dev, 4 test (10,434 lines, the item 16
  silence test). Every line is for people (G7, ignore); questions (`el.*`) are left out of train
  and dev as possible even calls. Disfluency augmentation is added to generated lines at the same
  time, so "uh" and repeats are not themselves a sign of a line for people. · Round 1 answered
  bare instructions between people in real meetings ("go on", a request for the next slide), and
  the generated corpus has the agent in nearly every conversation. CC BY 4.0. · Reversible:
  drop `ami-silent` from the training corpus list. The 22 labelled meetings stay test only.

- 2026-11-19 · SD-18 · agent default · Guide 0.4: calling the agent by name to thank it, stop it
  or say goodbye gets a short acknowledgement: `respond`, speak 4 (was an even call, speak 3).
  New kinds for the generator: bare instructions between people, steps explained to people, the
  meeting's host, and an answer to the agent after a quick check with a named person (G6,
  respond). Labels of earlier corpora follow from their kinds, so they move with the guide. · The
  daily-audience author expects "Thanks, Atlas." and "Okay Atlas, that's enough." to be answered
  (demo lines); the agent's own name is the reliable signal (SD-14). The committee was not rerun
  on 0.4. · Reversible: one line per kind in `sidechat/guide.py`. **Jon to confirm.**

- 2026-11-18 · SD-17 · Jon · Work through the phases autonomously overnight and make the model
  as accurate as possible for Jon to test in the morning. Spend up to $1,000 in all. · Jon:
  "You have my permission to spend up to $1000." · Supersedes the proposed $600 cap (SQ-08).

- 2026-11-18 · SD-16 · agent default · Scorecard 0.1 is frozen (`contracts/scorecard-0.1.md`):
  20 items, Jev's measured numbers where they exist, anonymous speakers as the headline condition.
  · PLAN.md section 9 Phase 1. · Changes only by a logged revision.
- 2026-11-18 · SD-15 · agent default · Guide 0.2 and the committee (members a, b and c at low
  effort) are accepted for Phase 3. On pilot-0.4 the majority agrees with the guide on 99.2%
  (263/265; exp-005); member a is the weakest (95.5%). Committee answers are stored once per
  prompt hash (`runs/side/committee/<prompt_sha>/`) and shared by every label set. · Re-scoring a
  relabelled set costs nothing. · Reversible.
- 2026-11-18 · SD-14 · Jon · Speaker labels may be anonymous ("Speaker 1"), and people do not call
  each other by them. People's names are a weak signal; the agent's name is the reliable one.
  Anonymous labels with no list of people are the default condition for training and the headline
  for scoring; real names are a variant. · Jon: "Names are a weak signal outside of [the bot's
  name]." · Standing.
- 2026-11-18 · SD-13 · Jon · The model reads the rhythm of the last turns explicitly: who spoke,
  in order, relative to the line's speaker (agent, speaker, other1, ...), plus a few numbers
  (`sidechat/context.py`). · Jon: it must know whether it was speaking before, "you spoke, they
  spoke, you spoke". Most committee disagreements in exp-002 turned on exactly this. · Standing.
  Finding from exp-004: an 8-turn window can miss state the agent holds (a timer it set 11 turns
  earlier). Facts about what the agent controls may be worth adding as input later.
- 2026-11-18 · SD-12 · Jon · `respond` is a calibrated probability, and the system using the model
  sets the thresholds. A line that leaves it open, such as a question to the room that nothing
  earlier settles, should score about 0.5, so the harness can choose to take the floor. Guide 0.2
  calls this `speak` 3, an even call. · Jon's instruction. · Standing.

- 2026-11-18 · SD-11 · agent default · Guide 0.1's policy on the grey zone: the agent speaks when
  spoken to (by name, by role, in an exchange with it, or in a session it leads) and holds for a
  pause on a question left open to the room. A proposal to ask it later ("Shall we check with
  Nova?") is `about`, stay quiet. An invitation ("Rook will know the rules") or a request to relay
  ("Get Atlas to order milk") is graded: either decision is fine. A line that could be for the
  agent or a person is `wait`. Volunteering help on a statement of need is out of scope. ·
  PLAN.md section 2; matches the demo's expectations for its own lines and Duplex-MPE's for
  mentions. · Reversible: a guide revision and a relabel; the committee pilot measures it.
- 2026-11-18 · SD-10 · agent default · The pilot is relabelled from the guide, not by hand:
  `pilot-0.2` names each line's kind and takes its label from `sidechat/guide.py`. Two lines whose
  kind mixed two labels were reclassified. `pilot-0.1` is kept unchanged because the Jev baseline
  (exp-001) was scored against it. · One source of truth for labels, which the generator will
  also use. · Reversible.
- 2026-11-18 · SD-09 · agent default, following Jon's AD-38 in Audience · No teacher or labeller
  model is named in this repository. The committee's members are a, b and c, one model family
  each; their model ids and prices live in `.env` (`LABELLER_A_MODEL`, `LABELLER_B_MODEL`,
  `LABELLER_C_MODEL`, `LABELLER_PRICES`). R2 keeps only a short hash of each id. Jev, the
  baseline Jon named, is not covered. · Jon set this rule for Audience; nothing suggests he wants
  otherwise here. · Reversible.

- 2026-11-18 · SD-08 · agent default · The opt-in call log for `daily-audience` (PLAN.md Phase 0)
  is held until Jon says go. · It edits a separate deployed project and records real people, which
  is Jon's call (SQ-05). · Reversible: nothing has been changed there.
- 2026-11-18 · SD-07 · agent default · Duplex-MPE is read one utterance at a time: `T` and `N4_Q`
  are for the agent, every other event is not. The 28 rows whose event type and addressee disagree
  are left out of scoring. · The benchmark scores a speech model over time; a text classifier sees
  each turn alone. `N4_Q` is a named question to the agent at the moment it is said, and the
  "never mind" comes in the next turn. · Reversible: a relabel, no new answers needed.
- 2026-11-18 · SD-06 · agent default · Duplex-MPE and Social AI Ambient Bench are test sets only.
  Ambient Bench carries a notice forbidding training on it. Converted rows of either are never
  committed to git; they live in R2 with a manifest that says "test only". · Keeps two test sets
  we did not write independent of our training data. · Not reversible for Ambient Bench.
- 2026-11-18 · SD-05 · agent default · The baseline is `jev-demo-0.1`: `jev-1.13.0`, the demo's
  wording at commit `73171de`, its thresholds 0.8 and 0.5, its 8 earlier messages. Stored answers
  are reused and a stored answer is never asked for again. · A hosted model can change; the bar
  must not move. · Reversible: a new wording or model gets a new baseline id.
- 2026-11-18 · SD-04 · agent default · Schema `sidechat-0.1`: five intents (direct, indirect,
  open, about, other) summing to 1, plus `respond`, `unclear` and per-person scores. · PLAN.md
  section 2; maps onto the demo's two numbers. · Reversible until a model ships (SQ-02).
- 2026-11-18 · SD-03 · agent default · Modal workspace `jptaylor`, environment `waystone`, the R2
  bucket Audience uses. Sidechat's own names: apps `waystone-side-<stage>`, R2 prefixes
  `runs/side/` and `models/side/`. Secrets are built from `.env` at launch, none stored on Modal.
  · This project's `.env` already points there and Audience's jobs follow the same rule.
  · Reversible.
- 2026-11-18 · SD-02 · Jon decided · Every pipeline job runs detached on Modal and writes its
  results to R2. · "So I can go offline at any point and come back to results." · Standing rule.
- 2026-11-18 · SD-01 · agent default · The project lives in this folder as its own repo. Audience's
  reusable code is copied unmodified into `vendor/audience/` from `spellspeak/model-training` at
  `c1f4d99`; adapted files are rewritten under `sidechat/`. · Sidechat is a Pipecat model, and the
  folder and keys were set up here. · Reversible: it could move into that repo as a track (SQ-01).

## Open questions

Each has the default the work assumes. From PLAN.md section 12.

| Id | Question | Default |
|---|---|---|
| SQ-01 | Own repo here, or a track inside `spellspeak/model-training`? | Own repo here |
| SQ-02 | Is the output shape right (five intents, `respond`, `unclear`, per-person)? | Yes. Jon confirmed `respond` as a calibrated probability (SD-12); per-person scores matter little with anonymous labels (SD-14) |
| SQ-03 | May Jev's answers be used as training targets? | No, pending TypeSafe's terms |
| SQ-04 | Speed bar | p95 ≤ 30 ms on 4 CPU threads |
| SQ-05 | Record internal team calls from the demo for a real-calls test slice? | Yes, opt-in, internal only. Not started (SD-08) |
| SQ-06 | Share-alike and non-commercial datasets in training? | No |
| SQ-07 | Release name and licence | `pipecat-ai/sidechat`, Apache-2.0, English only for rc1 |
| SQ-08 | Spend cap | Settled: $1,000 (SD-17) |
