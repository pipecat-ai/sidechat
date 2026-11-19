# The bar: Jev as the daily-audience demo uses it

2026-11-18 · experiment `exp-001-side-jev-baseline` · baseline id `jev-demo-0.1`

Every number here is measured in that run. Full tables, every slice and every disagreeing line are
in [experiments/exp-001-side-jev-baseline/report.md](../experiments/exp-001-side-jev-baseline/report.md).
A share is written `value (k/n; 95% interval)`.

## Summary

- **When its name is said, Jev is close to perfect.** It answers 99.2% of named requests at
  once and never answers outright a line that only mentions the agent.
- **Without the name, it mostly waits.** The same requests with the name removed are answered at
  once 26.6% of the time. Nearly all the rest are held, which in the demo means the bot answers
  2.5 seconds later if nobody else speaks.
- **It holds on about one line in six that was meant for someone else.** Its second question,
  "open for anyone to answer?", fires on requests between people and on thinking aloud. Each is a
  chance for the bot to speak into a pause.
- **Answering a person's line outright is rare:** 0.4%, and almost all of those are lines to
  another device ("Hey Google, …").
- **The ranking is good; the fixed thresholds lose the accuracy.** That is the room a purpose-built
  model with one calibrated "should I speak" number has to work in.

## What was run

| | |
|---|---|
| Model | `jev-1.13.0` through Pipecat 1.16.0's `JevClassifier` |
| Wording | The demo's two questions and state, from `daily-audience` at `73171de`. A test checks the copy against the demo's source |
| Decision rule | The demo's: answer now when `addressed ≥ 0.8`, hold for silence when `question ≥ 0.5`, otherwise stay quiet |
| Requests | 57,434 distinct, all answered, none failed |
| Tokens | 48,333,777 in (842 per request), 2,125,058 out |
| Cost | About $2.03 at $0.042 per million input tokens. That price is recorded in Audience's repo and not confirmed with TypeSafe |
| Time | 16 minutes on one Modal CPU container, 12 requests at a time |
| Latency | 150 ms at the median and about 220 ms at the 95th percentile, from Modal at that load |
| Beside it | A rule that answers whenever the agent's name is said, on the same lines |

Answers are stored in R2 and reused, so later runs compare against exactly these numbers.

## The four sets

| Set | Lines | What it is | Labels |
|---|---|---|---|
| `demo-lines-0.1` | 52 | The demo's own sample and eval lines | The outcome the demo's author expects |
| `pilot-0.1` | 283 | 29 hand-written conversations across the plan's settings | One author's draft, before any guide exists |
| `duplex-mpe-0.1` | 52,364 | Duplex-MPE: 3 or 4 people and an assistant, each request written with and without its name | The benchmark's, per turn. 28 rows left out where its own labels disagree |
| `ambient-bench-0.1` | 16,222 | Social AI Ambient Bench: typed group chats | The benchmark's RESPOND or SILENT |

## Headline numbers

"For others" is a line the set marks as not for the agent. "Holds" means the gate would answer
after a silence.

| Set | Decision right | For others: answers now | For others: holds | For the agent: answers now | For the agent: ignored |
|---|---|---|---|---|---|
| Demo lines | 97.9% (47/48; 89.1 to 99.6) | 0.0% (0/26) | 3.9% (1/26) | 100.0% (19/19) | 0.0% (0/19) |
| Pilot | 81.8% (207/253; 76.6 to 86.1) | 0.6% (1/157) | 15.3% (24/157; 10.5 to 21.7) | 73.4% (58/79; 62.8 to 81.9) | 13.9% (11/79; 8.0 to 23.2) |
| Duplex-MPE | 83.1% (43,495/52,336; 82.8 to 83.4) | 0.4% (182/44,528) | 16.0% (7,131/44,528; 15.7 to 16.4) | 80.4% (6,280/7,808; 79.5 to 81.3) | 0.1% (7/7,808) |
| Ambient Bench, SILENT lines | 85.4% (13,479/15,793; 84.8 to 85.9) | 0.1% (13/15,793) | 14.6% (2,301/15,793; 14.0 to 15.1) | n/a | n/a |

The name-only rule for comparison:

| Set | Decision right | For others: answers now | For the agent: ignored |
|---|---|---|---|
| Demo lines | 60.4% (29/48) | 46.2% (12/26) | 21.1% (4/19) |
| Pilot | 70.4% (178/253) | 12.7% (20/157) | 48.1% (38/79) |
| Duplex-MPE | 84.6% (44,265/52,336) | 13.6% (6,071/44,528) | 25.6% (2,000/7,808) |

On the pilot Jev beats the name rule by 11.5 points (5.1 to 17.8). On Duplex-MPE "decision right"
puts the name rule 1.5 points ahead, because every hold on a line for someone else counts against
Jev. The columns show the real difference: the name rule answers 13.6% of other people's lines
outright and Jev answers 0.4%.

## Findings

### 1. The name does most of the work

Duplex-MPE writes each request twice, once naming the assistant and once not.

| Request to the agent | Answers now | Holds | Ignores |
|---|---|---|---|
| With the name (2,000) | 99.2% (1,983; 98.6 to 99.5) | 0.8% (16) | 0.1% (1) |
| The same request without it (2,000) | 26.6% (531; 24.7 to 28.5) | 73.2% (1,464) | 0.2% (5) |
| Named question, taken back in the next turn (3,808) | 98.9% (3,766) | 1.1% (41) | 0.0% (1) |

Pair by pair the drop is 72.6 points (70.6 to 74.6). Jev does see these as wanting an answer, since
it holds almost all of them, but it does not read them as said to the agent. Their `addressed`
scores sit just under the threshold: "Do me a favour, you've been listening in on all this, so
total the food spend" scores 0.79.

The pilot agrees, on far fewer lines and with draft labels. The kinds it gets wrong most:

| Kind of line | Right | Example Jev does not answer at once |
|---|---|---|
| Answer to the agent's own question | 2 of 8 | "It's blinking orange." after the agent asked about the light |
| Follow-up with no name | 5 of 9 | "And what does that look like monthly instead of annual?" |
| Action declared to a game master | 0 of 2 | "I want to check the door for traps." |
| Command with no name | 1 of 3 | "Okay, stop the timer, I'm draining it now." |

These are settings where the agent leads the session: a support agent, a tutor, a game master, an
intake assistant. The demo's wording describes an assistant that listens to a call, so some of
this is the prompt and not the model (see Limits).

### 2. It holds on one line in six that was for someone else

The share is steady across three unrelated sets: 15.3% on the pilot, 16.0% on Duplex-MPE, 14.6% on
Ambient Bench. On Duplex-MPE by who the line was for:

| Line was for | Holds |
|---|---|
| Another person (32,838) | 15.7% (5,156) |
| Nobody, thinking aloud (6,540) | 16.7% (1,095) |
| Another device (5,146) | 17.1% (880) |
| A person, mentioning the agent (6,080) | 13.3% (809) |

Typical held lines are a worker telling a colleague where to move a vehicle, and someone asking
the room where they left a tool. (Test lines are not quoted here.) Both are requests or questions,
and neither is something an assistant could do or answer.

A hold is not speech. It becomes speech only if nobody talks for 2.5 seconds. In a lively
conversation most are cancelled, and in a pause the bot answers a question nobody asked it.

### 3. Outright wrong answers are rare, and mostly about other devices

Of 44,528 Duplex-MPE lines for others, Jev answers 182 at once (0.4%). 176 of them are lines to
another device, 3.4% of those (3.0 to 4.0): "Hey Google, set a timer for ten minutes" scores 0.82.
Lines between people are answered 6 times in 32,838.

The pilot's one case is caused by the demo, not Jev. The demo replaces every alias of the bot's
name before asking, so with "at last" listed as a mishearing of "Atlas", the line "at last a
number that makes sense" is sent as "Atlas a number that makes sense" and scores 0.94.

### 4. The scores rank well; the thresholds cost accuracy

| Set | AUROC of `addressed` | Calibration error |
|---|---|---|
| Duplex-MPE (7,808 for the agent, 44,528 not) | 0.988 | 0.073 |
| Pilot (88 for the agent, 185 not) | 0.965 | 0.066 |

Moving the threshold on Duplex-MPE trades one error for the other:

| `addressed` threshold | For the agent: answers now | For others: answers now |
|---|---|---|
| 0.5 | 92.0% | 4.0% |
| 0.7 | 85.8% | 1.3% |
| 0.8 (the demo's) | 80.4% | 0.4% |
| 0.9 | 70.1% | 0.04% |

No threshold gets both. A calibration error of about 0.07 is above the plan's 0.05 bar.

### 5. Ambient Bench measures a different policy

Its assistant is expected to volunteer help nobody asked for. Read strictly (speaking means
answering now) Jev passes 72.8% of scenarios (882/1,212), above the benchmark's own leaderboard top
of 67.4%, but only by staying quiet: it misses 92.8% of the RESPOND lines. Read leniently (a hold
counts as speaking) it misses 7.5% and passes 20.1%. Neither reading is the product Sidechat is
for. The figure to keep is the silence one: on 15,793 chat messages for other people it answers
0.1% outright and holds on 14.6%.

## What this sets as the bar

Against the plan's scorecard (PLAN.md 3.3):

| Item | Jev today | For Sidechat |
|---|---|---|
| Answers a line that was for a person | 0.4% on Duplex-MPE | Tight. The plan's 1% ceiling is looser than Jev, so the bar is 0.4% |
| Misses a line said directly to it, by name | About 1% not answered at once | Tight |
| Name said about the agent, not to it | 0 of 6,080 answered | Tight. Match it |
| Request or follow-up with no name | 26.6% answered at once | Wide open. The largest gain available |
| Holds on a line for someone else | 15 to 16% | Wide open |
| Calibration error | 0.07 | Open: the plan asks for 0.05 |
| Speed | 150 ms median over the network | A local model has two orders of magnitude to spare |

The shape of the job: keep Jev's precision on names, and add what the name hides, which is reading
from the conversation who a line was for.

## Limits

- **The pilot's labels are one author's.** They were written before any guide. 46 of 253 decisions
  differ from Jev's, and some of those are arguable: "Is the doctor running late?" with no name is
  labelled as for the agent because only the agent could know. Phase 1's guide and committee decide.
- **Duplex-MPE is written, not recorded.** Its card says the scripts were generated by one model
  and validated by people. It shows what Jev does with wording, not with real speech.
- **The assistant's replies are missing from Duplex-MPE's history.** The manifests hold the people's
  turns only. Jev would have more to go on with its own answer in view.
- **The demo's wording says "a live video call".** Duplex-MPE's scenes are rooms and Ambient Bench
  is typed chat. A reworded prompt may do better on unnamed requests. This run measures the demo
  as built, which is the stated bar.
- **Policies differ on indirect requests.** Duplex-MPE marks "Get Aria to text Mum that we'll be at
  hers closer to nine, would you?" as silence. The plan's `indirect` intent would have the agent
  consider it. The guide has to choose.
- **Timing is not modelled.** Whether a hold becomes speech depends on the pause that follows.
- **Latency is from Modal at 12 requests at a time.** A three-conversation trial at low load gave
  63 to 80 ms; the demo's README reports about 140 ms.

## Reproduce

```bash
set -a; . ./.env; set +a
```

```bash
uv run modal run --detach -m sidechat.pipeline.baseline::run --exp exp-001-side-jev-baseline --sets demo,pilot,ambient,duplex
```

```bash
uv run python -m sidechat.pipeline.results exp-001-side-jev-baseline
```

A re-run asks Jev nothing: all 57,434 answers are stored under `runs/side/baselines/jev-demo-0.1/`.
