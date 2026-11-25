# The agent's name as heard

2026-11-19. exp-058 (`sidechat/pipeline/phase6.py --test names`). Follows
[the real-speech report](2026-11-19-side-phase6-real-speech.md): speech-to-text rarely writes an
unusual agent name as configured, so named requests were missed. Two fixes that need no
retraining, measured together on SLURP's real requests said in AMI meetings (61 named, 2,705
unnamed) and, for side effects, on every other set.

## Deepgram's keyterm prompting: turn it on

The same recordings, heard again with `keyterm=Olly`. Deepgram wrote "Olly" in 48 of the 61 named
requests (5 without it) and put it into 4 of 2,705 requests that never said it.

| Named requests answered now (61) | Written | Heard | Heard, name as keyterm |
|---|---|---|---|
| Default build (150M) | 85.2% | 13.1% | **73.8%** |
| `agent-1x` build (32M) | 63.9% | 6.6% | **59.0%** |
| Jev | 100% | 49.2% | 73.8% |

Unnamed requests are unchanged by it (held: default 16.6%, `agent-1x` 3.7%, Jev 82.1%).

## Other spellings of the name as aliases: leave off

`sidechat/names.py` adds spellings of the agent's name built from spelling rules ("Olly": Ollie,
Oli, Olli, Oly ...). The model reads them on the agent's card and in its name features.

| | Default, plain | Default, spellings | `agent-1x`, plain | `agent-1x`, spellings |
|---|---|---|---|---|
| SLURP named, heard | 13.1% | 11.5% | 6.6% | 18.0% |
| SLURP named, heard with keyterm | 73.8% | 73.8% | 59.0% | 65.6% |
| Duplex-MPE named request answered | 99.5% | 99.2% | 98.7% | 97.3% |
| Duplex-MPE for others, answered outright | 0.22% | 0.27% | 0.26% | 0.31% |
| Ambient Bench for others, answered outright | 0.21% | 0.20% | 0.59% | 0.72% |
| Generated tests: name as a word or sound-alike, left alone | no change | | no change | |

The spellings help only the 32M, and mostly where the keyterm already fixes things. The extra
names on the card shift the models elsewhere (Duplex-MPE's "Aria" gets "Arria", "Ariah", and named
requests there drop 1.4 points for `agent-1x`). Not worth turning on. The module stays for
measurement.

## What is left

- Even with the keyterm, 13 of 61 names are still misheard; the default build answers 74% of named
  requests as heard against 85% as written.
- As written, SLURP's text is lower case and the agent's own name is matched case-sensitively, so
  "olly" does not count. Real speech-to-text capitalises names, so this matters less in use.
- Unnamed requests are the larger gap and the names do nothing for them.
