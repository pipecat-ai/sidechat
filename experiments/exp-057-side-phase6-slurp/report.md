# Requests to the agent in real speech: SLURP in AMI meetings (exp-057-side-phase6-slurp)

SLURP's recorded requests (test split, headset microphone; 2,766 heard, 61 saying "Olly"; word error rate 14.1%), each said at a seeded point in an AMI silence-test meeting by one of its speakers. The agent, Olly, has not spoken. Written: SLURP's text and AMI's transcripts. Heard: what Deepgram heard of both.

The guide's right answer: a named request is answered now; an unnamed one is held for a pause (Duplex-MPE would count only answering now).

| System | Named, answered now: written / heard | Unnamed: answered now | Unnamed: held | Unnamed: missed |
|---|---|---|---|---|
| Default build (round 3, 150M) | 85.2% (52) / 13.1% (8) | 0.2% (5) / 0.3% (8) | 18.2% (491) / 16.7% (451) | 81.7% (2,208) / 83.0% (2,245) |
| agent-1x build (32M) | 63.9% (39) / 6.6% (4) | 0.0% (0) / 0.0% (1) | 3.0% (82) / 3.5% (96) | 97.0% (2,622) / 96.4% (2,607) |
| Jev | 100.0% (61) / 49.2% (30) | 0.1% (3) / 0.0% (1) | 90.2% (2,438) / 82.3% (2,226) | 9.7% (263) / 17.6% (477) |

Each cell: written / heard. Lines: Default build (round 3, 150M) 61 named and 2704 unnamed.
