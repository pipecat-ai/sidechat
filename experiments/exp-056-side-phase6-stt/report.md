# Real speech through speech-to-text (exp-056-side-phase6-stt)

AMI's headset audio through Deepgram (`{'model': 'nova-3', 'language': 'en', 'punctuate': 'true', 'smart_format': 'true'}`): 26,622 dialogue acts, 4,869 heard as nothing (left out), word error rate 25.7% against AMI's transcripts.

Every line is for people. Shares of the same lines, as written and as heard; `(k)` is the count.

## AMI labelled meetings

| System | Lines | Left alone, written | Left alone, heard | Gap (points) | Answered, written | Answered, heard | Held, written | Held, heard |
|---|---|---|---|---|---|---|---|---|
| Default build (round 3, 150M) | 8,202 | 99.88% (8,192) | 99.85% (8,190) | -0.02 (-0.08 to +0.03) | 0.00% (0) | 0.00% (0) | 0.1% (10) | 0.1% (12) |
| agent-1x build (32M) | 8,202 | 99.99% (8,201) | 99.99% (8,201) | +0.00 (+0.00 to +0.00) | 0.00% (0) | 0.00% (0) | 0.0% (1) | 0.0% (1) |
| Jev | 8,202 | 84.86% (6,960) | 86.52% (7,096) | +1.66 (+1.07 to +2.25) | 0.01% (1) | 0.00% (0) | 15.1% (1,241) | 13.5% (1,106) |

## AMI silence test

| System | Lines | Left alone, written | Left alone, heard | Gap (points) | Answered, written | Answered, heard | Held, written | Held, heard |
|---|---|---|---|---|---|---|---|---|
| Default build (round 3, 150M) | 8,577 | 99.87% (8,566) | 99.92% (8,570) | +0.05 (-0.02 to +0.11) | 0.00% (0) | 0.00% (0) | 0.1% (11) | 0.1% (7) |
| agent-1x build (32M) | 8,577 | 100.00% (8,577) | 99.99% (8,576) | -0.01 (-0.03 to +0.01) | 0.00% (0) | 0.01% (1) | 0.0% (0) | 0.0% (0) |
| Jev | 8,577 | 88.52% (7,592) | 89.02% (7,635) | +0.50 (+0.02 to +0.99) | 0.01% (1) | 0.02% (2) | 11.5% (984) | 11.0% (940) |

## Item 15

- Default build (round 3, 150M): **met**. gap -0.02 points (bar: no worse than -3); left alone as heard 99.85%, Jev 86.52%
- agent-1x build (32M): **met**. gap +0.00 points (bar: no worse than -3); left alone as heard 99.99%, Jev 86.52%
