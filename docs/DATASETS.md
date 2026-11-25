# Open datasets for Sidechat: Hugging Face survey

2026-11-18

## What was searched

- About 200 keyword searches of the Hub's dataset index (121 in the first pass returned 1,773
  distinct repos, then about 80 more targeted ones).
- About 60 full-text searches of dataset cards. A third of the second batch was rate-limited, so
  full-text coverage is good but not complete.
- 46 datasets vetted by reading the card and one sample row through the Hub's API.

**Read the licence column with care.** It is the tag the uploader set on the Hub. Several repos
repackage older corpora, and the original licence is what binds. Phase 0 checks each source's own
licence before anything is used.

## 1. Same task, or close to it

| Dataset | Licence (Hub tag) | Size | What it is | Use |
|---|---|---|---|---|
| [ChengqianMa/Duplex-MPE](https://huggingface.co/datasets/ChengqianMa/Duplex-MPE) | CC BY 4.0 | 4,000 scenarios in 2,000 pairs; 26,182 human turns per condition | 3 or 4 people and an assistant, "Aria". Every turn is labelled with its addressee (`aria`, `other_human`, `device`, `none`), a speech act and an event type. Each pair has the request to Aria with its name and without. Written text with synthetic audio | **Held-out benchmark.** The closest match found |
| [text-ai/social-ai-ambient-bench](https://huggingface.co/datasets/text-ai/social-ai-ambient-bench) | Apache-2.0 | 1,212 group chats, 16,222 turns, 429 marked RESPOND | Typed group chat with an assistant, "alfi". Each turn is RESPOND or SILENT. Its policy answers open requests for help, so RESPOND maps to our `open` and `direct` together | **Held-out benchmark**, mainly for staying quiet during banter |
| [ACloudCenter/ami-addressee](https://huggingface.co/datasets/ACloudCenter/ami-addressee) | CC BY 4.0 | 8,876 labelled utterances from 22 meetings; all 110,795 utterances for context | Human addressee annotations from the AMI Meeting Corpus. About 3,600 are for one person and most of the rest for everyone | **Training and test.** The only human-labelled addressee data on real speech |
| [ishiki-labs/multi-party-dialogue](https://huggingface.co/datasets/ishiki-labs/multi-party-dialogue) | Apache-2.0 | AMI 14,088; Friends 12,862; SPGI 99,290 decision points | Will this participant speak next? Includes who the current turn addresses and whether that is explicit | **AMI part only**, as extra real-speech rows. The Friends and SPGI parts repackage material under other terms |
| [OliviaWang1101/MeetingToM](https://huggingface.co/datasets/OliviaWang1101/MeetingToM) | CC BY 4.0 | 1,200 records, 300 on who "you" refers to | Questions about AMI meetings. Media is not included | **Small test** of "you" |
| [duke-trust-lab/When2Speak](https://huggingface.co/datasets/duke-trust-lab/When2Speak) | CC BY 4.0 | 216,800 context and decision pairs from 16,000 conversations | Should an agent speak or stay silent? Written conversations, the agent shown as `[AGENT]` | **Not for labels.** Its agent joins in unprompted when it has something useful, which is a different policy. Possibly a source of conversations to relabel |
| [BiggestWave/Chorus-Duplex](https://huggingface.co/datasets/BiggestWave/Chorus-Duplex) | CC BY 4.0 | 100 dialogues, 1,667 turns per its stats file | Mandarin and English, 2 or 3 people and an assistant, per-turn addressee, side talk, acknowledgements, interruptions | **Watch.** Small today and the rows I read were Mandarin |
| [HashNuke/barge-in-detector-data](https://huggingface.co/datasets/HashNuke/barge-in-detector-data) | MIT | 13,580 utterances | Text said over a speaking agent, labelled as an acknowledgement or a real interruption. English, several Indian languages, Chinese | **Extra rows** for the "spoken over the agent" case |
| [puneetUMD/MultiPartyTurnBench](https://huggingface.co/datasets/puneetUMD/MultiPartyTurnBench) | CC BY 4.0, gated | Under 1,000 rows | Multi-party turn-taking benchmark. The card needs an access request, so I have not read it | **Request access** and look |
| [phelipescript/ddsd-ptbr-corpus](https://huggingface.co/datasets/phelipescript/ddsd-ptbr-corpus) | CC BY 4.0 | 232,876 sentences | Brazilian Portuguese sentences labelled as said to the computer or not | **Later**, if Portuguese is wanted |

## 2. Real multi-speaker talk

For authentic lines between people, which written conversations imitate badly.

| Dataset | Licence (Hub tag) | Size | What it is | Use |
|---|---|---|---|---|
| [edinburghcstr/ami](https://huggingface.co/datasets/edinburghcstr/ami) | CC BY 4.0 | 267,303 utterance rows | The AMI meetings with speaker and timing per utterance. Text is upper case | The silence test (plan item 11) and the base for splices |
| [benjamin-paine/dinner-party-corpus](https://huggingface.co/datasets/benjamin-paine/dinner-party-corpus) | CDLA-Permissive-1.0 | 297,276 rows, one per utterance and recording device | Amazon's Dinner Party Corpus: people talking over dinner at home, recorded by several devices | Casual real speech for splices |
| [bolinlai/Werewolf-Among-Us](https://huggingface.co/datasets/bolinlai/Werewolf-Among-Us) | Apache-2.0 | About 199 recorded games, per its card | Video, audio and transcripts of social deduction games, where people question and accuse each other directly | Real direct address between people |
| [pszemraj/qmsum-cleaned](https://huggingface.co/datasets/pszemraj/qmsum-cleaned) | Apache-2.0 | 3,620 rows | AMI, ICSI and committee meeting transcripts with role names | Extra meeting text |
| [wylupek/mrda-corpus](https://huggingface.co/datasets/wylupek/mrda-corpus) | "other" | 108,202 utterances | ICSI meetings with dialogue-act labels | Check the licence first |
| [tasksource/molweni](https://huggingface.co/datasets/tasksource/molweni) | Apache-2.0 | 30,066 questions over chats | Ubuntu IRC group chats. Typed, with speaker names | Low priority: typed chat, not speech |
| [docketx/oral-arguments-us](https://huggingface.co/datasets/docketx/oral-arguments-us) | CC0 | 102,649 rows | Court oral arguments with machine transcripts | Low priority: formal, and speakers may not be marked |

## 3. Things people say to assistants

One person, one assistant. Used to make requests in written scenes sound real, and to build hard
negatives by having the same request said to a person.

| Dataset | Licence (Hub tag) | Size | Notes |
|---|---|---|---|
| [AmazonScience/massive](https://huggingface.co/datasets/AmazonScience/massive) | CC BY 4.0 | About 1M utterances in 52 languages | Assistant commands. Also the route to other languages later |
| [tasksource/slurp](https://huggingface.co/datasets/tasksource/slurp) | CC BY 4.0 | 15,656 transcripts | Home-assistant commands as people typed and said them |
| [clinc/clinc_oos](https://huggingface.co/datasets/clinc/clinc_oos) | CC BY 3.0 | 59,275 rows across configurations | 150 intents plus out-of-scope queries |
| [google-research-datasets/taskmaster1](https://huggingface.co/datasets/google-research-datasets/taskmaster1) | CC BY 4.0 | Not reported by the Hub viewer | Task dialogues between a person and an assistant |
| [danielrosehill/Voice-Command-Sentences](https://huggingface.co/datasets/danielrosehill/Voice-Command-Sentences) | CC BY 4.0 | 34,276 rows | Recorded voice commands with text |
| [gpt-omni/VoiceAssistant-400K](https://huggingface.co/datasets/gpt-omni/VoiceAssistant-400K) | Apache-2.0 | 470,054 rows | Written questions to a voice assistant with synthetic audio |

## 4. Looked at and left out

| Dataset | Why |
|---|---|
| [TCLResearchEurope/intelligent_wakeup](https://huggingface.co/datasets/TCLResearchEurope/intelligent_wakeup) | On task (multi-speaker conversations with the assistant-directed moments marked, 2,297 rows) but CC BY-NC 4.0. Not for training. Could be a test set if a non-commercial licence is acceptable for evaluation |
| [microsoft/crd3](https://huggingface.co/datasets/microsoft/crd3) | Critical Role: several players and a game master, the closest real analogue of people plus one "host". CC BY-SA 4.0, so kept out of training by default |
| [MultiTalk/MultiTalkBench](https://huggingface.co/datasets/MultiTalk/MultiTalkBench) | 104 long audio samples for speech-to-speech models. CC BY-SA 4.0, and not text data |
| [M2cha4l1124/MSI-Bench](https://huggingface.co/datasets/M2cha4l1124/MSI-Bench) | Multi-speaker voice-agent scenes, but about memory and authority, not addressee. Its v2 is CC BY-NC 4.0 |
| [huuuyeah/meetingbank](https://huggingface.co/datasets/huuuyeah/meetingbank), MediaSum, CallHome, SAMSum, Seamless Interaction | Non-commercial or no-derivatives licences |
| [declare-lab/MELD](https://huggingface.co/datasets/declare-lab/MELD), [wangyueqian/friends_mmc](https://huggingface.co/datasets/wangyueqian/friends_mmc), [neoluigi/MELD-MPCA](https://huggingface.co/datasets/neoluigi/MELD-MPCA), bazinga | Built on TV scripts. The repo's licence tag does not cover the underlying show |
| [woodygan/CATS-ami-next-speaker-audio](https://huggingface.co/datasets/woodygan/CATS-ami-next-speaker-audio), [Orange/ecml_arena_dataset](https://huggingface.co/datasets/Orange/ecml_arena_dataset) | No licence stated |
| [dklement/SBCSAE](https://huggingface.co/datasets/dklement/SBCSAE) | Tagged MIT, but the Santa Barbara Corpus has its own terms. Check before use |
| [microsoft/NOTSOFAR](https://huggingface.co/datasets/microsoft/NOTSOFAR), [argmaxinc/icsi-meetings](https://huggingface.co/datasets/argmaxinc/icsi-meetings) | Meeting audio. Useful only with transcripts, and NOTSOFAR has no licence tag |
| [anyreach-ai/semantic-turn-taking-benchmark](https://huggingface.co/datasets/anyreach-ai/semantic-turn-taking-benchmark), [cekura/turn-taking-bench](https://huggingface.co/datasets/cekura/turn-taking-bench) | Two-party end-of-turn detection: when to speak, not whether a line was for you |
| [abolhasani/PSR_ACL](https://huggingface.co/datasets/abolhasani/PSR_ACL) | 2,520 Twitch chat messages with a direct-address flag. Small, typed, vague licence |
| DISLab/SoCRATES, OfficerChul/DICE-BENCH, kimperyang/GroupMemBench | Multi-party, but about mediation, tool use and memory |

## 5. What this changes in the plan

1. **Three test sets we did not write.** Duplex-MPE, the Ambient Bench and MeetingToM's "you"
   questions. Jev is scored on them too, which makes the comparison independent of our generator.
2. **Human labels on real speech.** AMI's addressee annotations give training rows and a test
   slice that no model labelled.
3. **A design to copy.** Duplex-MPE pairs every request with and without the assistant's name and
   includes lines to another device ("Hey Siri…"). The generator does both.
4. **No ready-made training set.** Nothing found is large, permissively licensed, on this task and
   in speech register at once. Scripted conversations remain the bulk of the training data.

## 6. Gaps in the search

- Corpora that are not on the Hub were not searched: Ego4D's "talking to me" task, the Vernissage
  and MuMMER human-robot corpora, and ConvoKit's collections.
- The gated repos (MultiPartyTurnBench, SPoRC, DialogStudio, bazinga) were not read.
- Sizes come from the Hub's viewer where it reported them and from the card otherwise.

## 7. Added since the survey

| Set | From | Size | What it is | Use |
|---|---|---|---|---|
| `gen-0.6` | Our generator (exp-080) | About 5,000 conversations | A device in a room whose role says what it does: five settings for training, and one more written only for the test split, which is not published | **Training**, and its test split. `sidechat/gen/world.py` (`ROOM_DEVICES`) |
