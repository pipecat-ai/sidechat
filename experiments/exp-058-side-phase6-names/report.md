# The agent's name as heard (exp-058-side-phase6-names)

Deepgram with the keyterm `Olly`: word error rate 14.1%. `plain` is each build as released; `variants` adds other spellings of the agent's name as aliases (`sidechat/names.py`). Shares are `value (k/n)`.

| | Default build (round 3, 150M), plain | Jev | Default build (round 3, 150M), variants | agent-1x build (32M), plain | agent-1x build (32M), variants |
|---|---|---|---|---|---|
| Duplex-MPE for others, answered outright | 0.2% (97/44,528) | 0.4% (182/44,528) | 0.3% (119/44,528) | 0.3% (115/44,528) | 0.3% (139/44,528) |
| Duplex-MPE name mentioned, answered outright (N1) | 0.3% (17/6,080) | 0.0% (0/6,080) | 0.3% (18/6,080) | 0.7% (42/6,080) | 0.7% (44/6,080) |
| Duplex-MPE named request answered | 99.5% (1,990/2,000) | 99.2% (1,983/2,000) | 99.2% (1,984/2,000) | 98.7% (1,973/2,000) | 97.3% (1,946/2,000) |
| Duplex-MPE right | 96.7% (50,592/52,336) | 83.1% (43,495/52,336) | 96.5% (50,533/52,336) | 95.6% (50,050/52,336) | 95.6% (50,029/52,336) |
| ambient-bench-0.1 for others, answered outright | 0.2% (33/15,793) | 0.1% (13/15,793) | 0.2% (31/15,793) | 0.6% (93/15,793) | 0.7% (113/15,793) |
| ambient-bench-0.1 right | 98.7% (15,591/15,793) | 85.4% (13,479/15,793) | 98.7% (15,585/15,793) | 98.4% (15,546/15,793) | 98.2% (15,510/15,793) |
| demo-lines-0.1 for others, answered outright | 0.0% (0/26) | 0.0% (0/26) | 0.0% (0/26) | 0.0% (0/26) | 0.0% (0/26) |
| demo-lines-0.1 right | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) | 97.9% (47/48) |
| gen-0.2.test@anonymous right | 98.8% (15,959/16,158) | n/a | 98.8% (15,963/16,158) | 98.6% (15,929/16,158) | 98.6% (15,934/16,158) |
| gen-0.2.test@anonymous: misheard name answered | 100.0% (63/63) | n/a | 100.0% (63/63) | 98.4% (62/63) | 98.4% (62/63) |
| gen-0.2.test@anonymous: name as a word / sound-alike left alone | 94.8% (199/210) | n/a | 94.8% (199/210) | 95.7% (201/210) | 95.7% (201/210) |
| gen-0.4.test@anonymous right | 96.7% (10,038/10,385) | n/a | 96.7% (10,041/10,385) | 97.8% (10,151/10,385) | 97.7% (10,149/10,385) |
| gen-0.4.test@anonymous: misheard name answered | 100.0% (37/37) | n/a | 100.0% (37/37) | 100.0% (37/37) | 100.0% (37/37) |
| gen-0.4.test@anonymous: name as a word / sound-alike left alone | 95.8% (91/95) | n/a | 95.8% (91/95) | 95.8% (91/95) | 95.8% (91/95) |
| pilot-0.4@anonymous for others, answered outright | 4.3% (7/163) | 1.8% (3/163) | 4.3% (7/163) | 3.1% (5/163) | 3.7% (6/163) |
| pilot-0.4@anonymous right | 87.4% (236/270) | 77.8% (210/270) | 87.4% (236/270) | 87.4% (236/270) | 87.0% (235/270) |
| slurp-in-ami-0.1: named answered now | 85.2% (52/61) | 100.0% (61/61) | 90.2% (55/61) | 63.9% (39/61) | 65.6% (40/61) |
| slurp-in-ami-0.1: unnamed held | 18.1% (491/2,705) | 90.1% (2,438/2,705) | 19.5% (527/2,705) | 3.0% (82/2,705) | 3.7% (100/2,705) |
| slurp-in-ami-stt-0.1: named answered now | 13.1% (8/61) | 49.2% (30/61) | 11.5% (7/61) | 6.6% (4/61) | 18.0% (11/61) |
| slurp-in-ami-stt-0.1: unnamed held | 16.7% (451/2,704) | 82.3% (2,226/2,704) | 17.9% (485/2,704) | 3.5% (96/2,704) | 4.1% (112/2,704) |
| slurp-in-ami-stt-keyterm-0.1: named answered now | 73.8% (45/61) | 73.8% (45/61) | 73.8% (45/61) | 59.0% (36/61) | 65.6% (40/61) |
| slurp-in-ami-stt-keyterm-0.1: unnamed held | 16.6% (448/2,705) | 82.1% (2,220/2,705) | 17.8% (482/2,705) | 3.7% (99/2,705) | 4.2% (114/2,705) |
