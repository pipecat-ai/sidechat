# Phase 6 notes: real speech, from found data

2026-11-19. Jon cannot record real calls: "we have to work with what we can find". Phase 6 was built
from public recordings of real people instead (SD-23). Read this, then [TODO.md](../TODO.md).

## What was done

- **The search.** No public, permissively licensed recordings of people talking to an agent in a
  group exist. VACC (Alexa) and Vernissage (a robot) are on request, Ego4D's "talking to me" is
  research only, and Duplex-MPE's and TCL's audio is text-to-speech. Real people talking among
  themselves (AMI, with human addressee labels) and real people speaking to an assistant (SLURP)
  exist. SLURP's audio is CC BY-NC 4.0: Jon allows it for testing only (SD-23).
- **exp-056, item 15.** AMI's per-speaker headset audio (`edinburghcstr/ami`, ihm) for the 22
  labelled and 12 silence-test meetings, through Deepgram nova-3. Each word goes to the AMI dialogue
  act of the same speaker that holds its midpoint, so AMI's human labels carry over. Jev and both
  builds on the same lines as written and as heard.
- **exp-057, requests in real speech.** SLURP's 2,766 recorded requests (headset microphone) said
  at seeded points in AMI's silence-test meetings, written and heard. The agent is "Olly", SLURP's
  name, and has not spoken.
- **Code.** `sidechat/pipeline/stt_ami.py`, `stt_slurp.py`, `phase6.py` (one detached job per test;
  `--test slurp`), `sidechat/lib/stt_align.py`, `sidechat/sources/slurp.py`, the sets `ami-stt`,
  `ami-silent-stt:test`, `slurp` and `slurp-stt`, and `train.score_sets` (score a trained model on
  more sets at its own thresholds). The Jev job's function is now named `baseline_run`.

## Results

[reports/2026-11-19-side-phase6-real-speech.md](../reports/2026-11-19-side-phase6-real-speech.md).

- **Item 15 is met by both builds.** On 8,202 AMI lines (word error rate 25.7%), speech-to-text
  changes almost nothing: gap −0.02 points for the default build, 0.00 for `agent-1x`. Jev holds for
  a pause on 13–15% of people's lines either way.
- **Misheard names break named requests.** Heard, the default build answers 13% of requests that
  say "Olly" (85% as written), `agent-1x` 7% (64%), Jev 49% (100%). Deepgram wrote the name as
  "Olly" 5 times in 61. The models match the agent's own name exactly and case-sensitively, so
  lower-case "olly" (SLURP's text) and "Oli" or "Ollie" (Deepgram) do not count.
- **Unnamed real requests are mostly ignored.** Both builds miss 82–97% of them, and Jev holds for
  82–90%. This is item 5 on real speech, and it is larger than on Duplex-MPE.

About $7.30 for both. Total about $317 of $1,000.

## Things learned

- Real speech-to-text noise does not make these models talk over people. The risk on real speech is
  the other way: missing the agent.
- The agent's name as heard is not the name as configured. Speech-to-text spells unusual names many
  ways, so exact name matching is fragile. The plan's "with and without name hints" (Deepgram's
  keyterm prompting) was never measured.
- Item 5 is not a Duplex-MPE quirk: real people's requests, unnamed, go unanswered.

## Loose ends

- Nothing committed. SLURP's transcripts and rows stay in R2 only (SD-23).
- The splices put out-of-place requests in design meetings; the right test is still real calls.

## Part 2: the agent's name as heard (exp-058)

[reports/2026-11-19-side-phase6-names.md](../reports/2026-11-19-side-phase6-names.md), SD-24.

- **Deepgram's keyterm prompting fixes most of it.** With `keyterm=Olly`, Deepgram wrote the name in
  48 of 61 named requests (5 without) and put it into 4 of 2,705 that never said it. Named requests
  answered as heard: default build 13% to 74%, `agent-1x` 7% to 59%, Jev 49% to 74%. The README
  now says to pass the agent's name as a keyterm.
- **Other spellings as aliases (`sidechat/names.py`) are left off.** Only the 32M gained, a little,
  and the extra names on the card cost elsewhere (Duplex-MPE named requests down 1.4 points for
  `agent-1x`). The module and `score_sets(names=...)` stay for measurement.
- About $2.10. Total about $319 of $1,000.

## Where the next phase picks up

1. ~~Names.~~ Done: keyterm on, spellings off (SD-24). The Pipecat module's example and docs should
   pass the agent's name to Deepgram as a keyterm (pipecat branch `jpt/sidechat`, another session's
   work).
2. **Unnamed requests, with real people's wording.** SLURP's text is CC BY 4.0 (only its audio is
   non-commercial), and MASSIVE's is CC BY 4.0. Their training splits, said in AMI's training
   meetings and labelled by the guide (hold for a pause), would teach what real requests sound like.
   Test on SLURP's test split as heard (same source, so a friendly test) and on Duplex-MPE's unnamed
   requests (an unfriendly one).
