# Committee pilot: exp-002-side-committee-trial

Generated 2026-11-18T22:29:39+00:00 by `sidechat/pipeline/label.py`. Every number below is measured in this run.

## What was run

- **Lines:** 17 from `pilot-0.2`, 16 with a definite decision in the guide and 1 graded.
- **Guide:** `sidechat-guide-0.1`, prompt hash `0fa7e0d30b2b`.
- **Members:** a, b, c, one model family each, at low reasoning effort. Model ids are configuration, not named here (SD-09).
- **Label set:** `trial-committee-0` in R2.

## Agreement with the guide

**Majority decision: 87.5% (14/16; 64.0 to 96.5).** Target 90%: **not met**. No majority on the decision for 0 lines.

| | Decision | Intent | For the agent or not | Rule | Mean distance on `speak` |
|---|---|---|---|---|---|
| Majority | 87.5% (14/16; 64.0 to 96.5) | 93.8% (15/16; 71.7 to 98.9) | | | |
| Member a | 87.5% (14/16; 64.0 to 96.5) | 93.8% (15/16; 71.7 to 98.9) | 100.0% (16/16; 80.6 to 100.0) | 88.2% (15/17; 65.7 to 96.7) | 0.235 |
| Member b | 87.5% (14/16; 64.0 to 96.5) | 93.8% (15/16; 71.7 to 98.9) | 100.0% (16/16; 80.6 to 100.0) | 76.5% (13/17; 52.7 to 90.5) | 0.235 |
| Member c | 87.5% (14/16; 64.0 to 96.5) | 87.5% (14/16; 64.0 to 96.5) | 100.0% (16/16; 80.6 to 100.0) | 88.2% (15/17; 65.7 to 96.7) | 0.235 |

Members agreeing with each other on the decision: a-b 100.0% (17/17), a-c 94.1% (16/17), b-c 94.1% (16/17). All three give the same decision and intent on 82.3% (14/17) of lines.

**By the guide's decision**

| Guide says | Majority agrees |
|---|---|
| ignore | 90.9% (10/11; 62.3 to 98.4) |
| respond | 100.0% (3/3; 43.9 to 100.0) |
| wait | 50.0% (1/2; 9.4 to 90.5) |

**By rule**

| Rule | Majority agrees |
|---|---|
| G7 | 80.0% (8/10; 49.0 to 94.3) |
| G2 | 100.0% (2/2; 34.2 to 100.0) |
| G3 | 100.0% (2/2; 34.2 to 100.0) |
| G6 | 100.0% (2/2; 34.2 to 100.0) |

**Kinds under 100%**

| Kind | Majority agrees |
|---|---|
| `people_after_agent` | 50.0% (1/2) |
| `open_question` | 0.0% (0/1) |

## Lines where the majority differs from the guide (2)

**standup-01/7** `people_after_agent` (G7): guide **ignore**, majority **wait**
> Jon: And put a reminder on it for tomorrow morning.
> agent: Done. Reminder set for nine tomorrow.
> **Sam: Nine's a bit early for Priya.**

- a: wait / other / speak 3 / G6: Sam is reacting to Atlas’s reminder time, but the comment could be for Atlas or the other people on the call.
- b: wait / other / speak 3 / G6: Sam, not the agent's last partner, reacts to the agent's answer; it could be a remark to Jon or a nudge to the agent to change the time, and nothing settles which.
- c: wait / direct / speak 3 / G6: Someone other than the agent's last partner reacts to the time the agent set, which could be directed at the agent to change the reminder or at Jon and Priya.

**planning-02/2** `open_question` (G7): guide **wait**, majority **ignore**
> Maya: So the big one is the billing migration. Tom, how many points did we say?
> Tom: Thirteen, I think. Might be more.
> **Lena: Does anyone remember what we shipped last sprint?**

- a: ignore / other / speak 1 / G7: Lena is asking the team to recall what they shipped, not asking Atlas to look it up.
- b: ignore / other / speak 1 / G7: Lena is asking the team to recall their own past work, which is a question about the people themselves rather than a lookup for the agent.
- c: ignore / other / speak 1 / G7: Lena asks the group a question about what they did last sprint, which is about the people's own work rather than something a general AI assistant on the call would answer.

## Graded lines (1)

| Line | Kind | a | b | c |
|---|---|---|---|---|
| Lena: Atlas would know, it's got the board. | `invite` | respond 3 | respond 3 | wait 3 |

## Calls and cost

| Member | Answered | Failed | Not by the configured model | Input tokens | Cached | Output tokens | Est. cost |
|---|---|---|---|---|---|---|---|
| a | 17 | 0 | 0 | 62,327 | 53,070 | 1,083 | $0.06 |
| b | 17 | 0 | 0 | 94,543 | 48,267 | 1,612 | $0.28 |
| c | 17 | 0 | 0 | 69,781 | 0 | 1,227 | $0.30 |
