# Phase 6: real speech, from found data

2026-11-19. exp-056 (AMI through speech-to-text) and exp-057 (SLURP's requests in AMI meetings).
Notes: [phase-6-real-speech.md](../notes/phase-6-real-speech.md). No real calls could be recorded
(SD-23), so both tests use public recordings of real people. Speakers are anonymous letters
throughout. Deepgram nova-3 with punctuation and formatting heard everything.

## 1. People's talk through speech-to-text (item 15): met by both builds

AMI's per-speaker headset audio for the 22 labelled meetings and the 12 silence-test meetings
(26,622 dialogue acts, 941 minutes). Word error rate against AMI's own transcripts: 25.7%. 4,869
acts were heard as nothing, mostly "yeah" and "mm-hmm", and are left out, as a live pipeline would
never pass them on. Every line is for people, so the right decision is always to stay quiet. The
same lines are compared as written and as heard.

| AMI labelled meetings, 8,202 lines | Left alone, written | Left alone, heard | Gap | Held, written / heard |
|---|---|---|---|---|
| Default build (round 3, 150M) | 99.88% | 99.85% | −0.02 points (−0.08 to +0.03) | 10 / 12 lines |
| `agent-1x` build (32M) | 99.99% | 99.99% | 0.00 | 1 / 1 |
| Jev | 84.86% | 86.52% | +1.66 | 15.1% / 13.5% |

| AMI silence test, 8,577 lines | Left alone, written | Left alone, heard | Answered outright, heard |
|---|---|---|---|
| Default build | 99.87% | 99.92% | 0 |
| `agent-1x` build | 100.00% | 99.99% | 1 |
| Jev | 88.52% | 89.02% | 2 |

**Item 15 is met by both builds**: real transcription errors cost nothing measurable on people's
talk (bar: within 3 points, and at least Jev). Jev holds for a pause on 11–15% of these lines either
way.

## 2. Requests to the agent in real speech: two real gaps

SLURP's recordings of people speaking requests to a home assistant, "Olly" (test split, close-talk
headset; 2,766 requests, 61 of them saying the name; word error rate 14.1%), each put at a seeded
point in an AMI silence-test meeting, as said by one of its speakers. The agent, Olly, has not
spoken. SLURP's audio is CC BY-NC: test only (SD-23).

| | Named, answered now: written / heard | Unnamed, answered now | Unnamed, held | Unnamed, missed |
|---|---|---|---|---|
| Default build | 85.2% / **13.1%** | 0.2% / 0.3% | 18.2% / 16.7% | 81.7% / 83.0% |
| `agent-1x` build | 63.9% / **6.6%** | 0.0% / 0.0% | 3.0% / 3.5% | 97.0% / 96.4% |
| Jev | 100% / 49.2% | 0.1% / 0.0% | **90.2% / 82.3%** | 9.7% / 17.6% |

Each cell is written / heard. Under guide 0.4 a named request is answered now and an unnamed one is
held for a pause.

- **Misheard names.** Deepgram wrote the name as "Olly" in 5 of the 61 named requests: "Oli" 21,
  "Ollie" 6, "Ali" 3, and 26 lost or spelled otherwise. Our models match the agent's own name
  exactly and case-sensitively (`sidechat/train/features.py`, the name features; aliases are matched
  case-insensitively), so heard named requests fall from 85% to 13% (default) and 64% to 7%
  (`agent-1x`). Jev, an LLM, still answers about half. Case also matters as written: SLURP's text is
  lower case, and "olly" does not match "Olly", which is why the default build misses 15% of named
  requests even as written.
- **Unnamed requests.** Real requests an assistant could do, said without the name in a meeting
  where the agent has not spoken, are mostly ignored by both builds (82–97%). Jev holds for a pause
  on 82–90%. This is item 5's gap on real speech, and larger: it says the gap would matter in use.

## Caveats

- The SLURP lines are spliced: a request to play music or set an alarm said in the middle of a
  design meeting. That makes them stand out from the talk around them, which should make them easier
  to spot, not harder.
- 61 named lines is a small sample (95% intervals about ±9 points).
- The labels for unnamed lines are the guide's (hold); Duplex-MPE would call them for the agent.
  Either way both builds mostly do neither.
