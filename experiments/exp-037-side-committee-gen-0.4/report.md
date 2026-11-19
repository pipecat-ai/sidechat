# Committee pilot: exp-037-side-committee-gen-0.4

Generated 2026-11-19T10:17:20+00:00 by `sidechat/pipeline/label.py`. Every number below is measured in this run.

## What was run

- **Lines:** 330 from `corpus:gen-0.4:dev+test:120:follow_up_after_reaction, corpus:gen-0.4:dev+test:120:relay_agent_answer, corpus:gen-0.4:dev+test:90:command_no_name+reply_then_request`, 330 with a definite decision in the guide and 0 graded.
- **Guide:** `sidechat-guide-0.4`, prompt hash `5b71303e8551`.
- **Members:** a, b, c, one model family each, at low reasoning effort. Model ids are configuration, not named here (SD-09).
- **Label set:** `corpus:gen-0.4:dev+test:120:follow_up_after_reaction-committee-0.4` in R2.

## Agreement with the guide

**Majority decision: 98.8% (326/330; 96.9 to 99.5).** Target 90%: met. No majority on the decision for 1 lines.

| | Decision | Intent | For the agent or not | Rule | Mean distance on `speak` |
|---|---|---|---|---|---|
| Majority | 98.8% (326/330; 96.9 to 99.5) | 99.4% (328/330; 97.8 to 99.8) | | | |
| Member a | 99.4% (328/330; 97.8 to 99.8) | 99.4% (328/330; 97.8 to 99.8) | 99.7% (329/330; 98.3 to 100.0) | 93.0% (307/330; 89.8 to 95.3) | 0.018 |
| Member b | 98.2% (324/330; 96.1 to 99.2) | 99.1% (327/330; 97.4 to 99.7) | 98.5% (325/330; 96.5 to 99.4) | 92.4% (305/330; 89.1 to 94.8) | 0.048 |
| Member c | 98.2% (324/330; 96.1 to 99.2) | 98.8% (326/330; 96.9 to 99.5) | 98.5% (325/330; 96.5 to 99.4) | 93.3% (308/330; 90.1 to 95.6) | 0.048 |

Members agreeing with each other on the decision: a-b 98.2% (324/330), a-c 98.2% (324/330), b-c 98.5% (325/330). All three give the same decision and intent on 97.3% (321/330) of lines.

**By the guide's decision**

| Guide says | Majority agrees |
|---|---|
| respond | 98.6% (207/210; 95.9 to 99.5) |
| ignore | 99.2% (119/120; 95.4 to 99.9) |

**By rule**

| Rule | Majority agrees |
|---|---|
| G6 | 98.6% (207/210; 95.9 to 99.5) |
| G4 | 99.2% (119/120; 95.4 to 99.9) |

**Kinds under 100%**

| Kind | Majority agrees |
|---|---|
| `follow_up_after_reaction` | 98.3% (118/120) |
| `relay_agent_answer` | 99.2% (119/120) |
| `command_no_name` | 97.7% (42/43) |

## Lines where the majority differs from the guide (4)

**a06-01751/14** `follow_up_after_reaction` (G6): guide **respond**, majority **none**
> agent: In-flight requests may fail, but completed payments won't be reversed.
> Mateo: Right.
> **Mira: Check whether the rollback is ready to run.**

- a: respond / direct / speak 5 / G6: Mira continues her rollback exchange with Nova, and Mateo’s brief acknowledgement doesn’t redirect it.
- b: ignore / other / speak 1 / G7: A bare instruction to check rollback readiness is a task for the engineers handling the deploy (likely Noah), not something the agent controls.
- c: wait / direct / speak 3 / G6: Mira has been talking to Nova, so this could continue her exchange with the agent, or it could be an engineering instruction for Noah or Mateo.

**o06-02979/10** `follow_up_after_reaction` (G6): guide **respond**, majority **wait**
> agent: Mint and oregano are hardy. They spread quickly and tolerate neglect.
> Yuki: Mint is definitely aggressive. I learned that the hard way.
> **Theo: Is there a trick to stopping the spread?**

- a: respond / direct / speak 5 / G6: Theo follows up on Dash’s answer to his own question by asking how to stop mint from spreading.
- b: wait / direct / speak 3 / G6: Theo's follow-up on mint could continue his exchange with Dash, but it comes right after Yuki's personal experience with mint, so it could equally be for Yuki.
- c: wait / open / speak 3 / G6: Theo follows up on the topic of mint spreading, which could be directed at Yuki who just shared personal experience with it, or at Dash who introduced it.

**o06-01594/13** `relay_agent_answer` (G4): guide **ignore**, majority **wait**
> Raj: Does that change if I use peat moss in the mix?
> agent: Peat moss is naturally acidic, so it might lower the pH a bit. You might need to add lime to balance it out.
> **Elif: So Otto reckons peat moss makes the soil too acidic?**

- a: wait / open / speak 3 / G4: Elif mentions Otto in the third person and asks the room to clarify what it meant.
- b: wait / about / speak 3 / G6: Elif, not the agent's partner, questions the agent's answer while referring to Otto in the third person; it could be for Raj or invite Otto to clarify, so waiting is safe.
- c: wait / open / speak 3 / G4: Elif mentions Otto in the third person while putting a clarifying question about its answer to the room, which Otto could answer if nobody else does.

**o06-00969/2** `command_no_name` (G6): guide **respond**, majority **ignore**
> Mohammed: Does anyone know where the boiler service date is listed?
> agent: It's in the service folder, page three, usually.
> **Mohammed: Okay, keep scrolling then, I'll find it.**

- a: respond / direct / speak 5 / G6: Mohammed follows up on Ivy’s answer with a command without turning to anyone else.
- b: ignore / other / speak 1 / G7: Mohammed is telling whoever is scrolling the document to carry on, a physical action only a person can do, not a request to the agent.
- c: ignore / other / speak 1 / G6: Mohammed instructs Evie to keep scrolling on her device, an action only the other person present can perform.

## Graded lines (0)

| Line | Kind | a | b | c |
|---|---|---|---|---|

## Calls and cost

| Member | Answered | Failed | Not by the configured model | Input tokens | Cached | Output tokens | Est. cost |
|---|---|---|---|---|---|---|---|
| a | 330 | 0 | 0 | 1,601,227 | 1,532,088 | 21,017 | $1.11 |
| b | 330 | 0 | 0 | 2,398,914 | 2,250,458 | 26,859 | $2.09 |
| c | 330 | 0 | 0 | 1,760,558 | 201,741 | 23,887 | $6.92 |
