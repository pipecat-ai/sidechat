"""SLURP's requests to an assistant, said in the middle of real AMI meetings.

SLURP's text is CC BY 4.0 and its audio CC BY-NC 4.0: test only, never trained on; its rows stay out
of git and off the Hub (DECISIONS.md SD-23).

Each request from SLURP's test split (with a close-talk recording, `sidechat/pipeline/stt_slurp.py`)
is put at a point in one of AMI's silence-test meetings, chosen by its id, as said by one of that
meeting's speakers. The history is the eight AMI dialogue acts before that point. The agent is
"Olly", the name SLURP's speakers used, and it has not spoken. Two sets share the same splices:

    slurp-in-ami-0.1      SLURP's text, and AMI's transcripts
    slurp-in-ami-stt-0.1  what Deepgram heard of both (lines or turns heard as nothing are left out)

Labels follow the guide (0.4): a request that says "Olly" is for the agent (respond); one that does
not, with nobody else settled as its addressee, is a request open to the room the agent could do
(`open_request`: hold for a pause, `respond` 0.5). Duplex-MPE would call the second kind for the
agent, so the summary reports answered now and held apart.
"""

from __future__ import annotations

import random
from collections import defaultdict

from sidechat import guide
from sidechat.schema import Agent, SidechatRecord, SidechatRequest, Turn, window

SET = "slurp-in-ami-0.1"
STT_SET = "slurp-in-ami-stt-0.1"
STT_PREFIX = "stt/slurp-deepgram-nova-3"  # under runs/side in R2: transcripts.jsonl and manifest.json
STT_KEYTERM_PREFIX = "stt/slurp-deepgram-nova-3-keyterm"  # heard with the agent's name as a keyterm
STT_KEYTERM_SET = "slurp-in-ami-stt-keyterm-0.1"
# A dev set for the name as heard: SLURP's train and devel utterances that say "Olly", every
# recording of each (`stt_slurp.run --split dev`). Never the test split; never training (SD-23).
DEV_STT_PREFIX = "stt/slurp-names-dev-deepgram-nova-3"
DEV_STT_KEYTERM_PREFIX = "stt/slurp-names-dev-deepgram-nova-3-keyterm"
DEV_SET = "slurp-names-dev-0.1"
DEV_STT_SET = "slurp-names-dev-stt-0.1"
DEV_STT_KEYTERM_SET = "slurp-names-dev-stt-keyterm-0.1"
AGENT = Agent(name="Olly", role="AI assistant in the meeting")
LICENCE = "text CC BY 4.0, audio CC BY-NC 4.0"
USE = "test only (SD-23)"


def named(sentence: str) -> bool:
    return "olly" in sentence.lower().split()


def kind(sentence: str) -> str:
    words = sentence.lower().split()
    if "olly" not in words:
        return "open_request"
    return "name_first" if words[0] == "olly" else "name_last" if words[-1] == "olly" else "name_mid"


def convert(slurp_rows: list[dict], ami_rows: list[dict], heard: bool, set_name: str = "") -> list[dict]:
    """`slurp_rows`: SLURP transcripts (sentence, stt, ...). `ami_rows`: AMI transcripts of the
    silence-test meetings (meeting, speaker, start, gold, stt). `heard` picks the STT text."""
    meetings: dict[str, list[dict]] = defaultdict(list)
    for r in ami_rows:
        if not r.get("labelled_meeting"):
            meetings[r["meeting"]].append(r)
    names = sorted(meetings)
    for m in names:
        meetings[m].sort(key=lambda r: (r["start"], r["end"]))
    set_name = set_name or (STT_SET if heard else SET)
    rows = []
    for s in slurp_rows:
        text = (s["stt"] if heard else s["sentence"]).strip()
        rng = random.Random(f"slurp-in-ami:{s['slurp_id']}")
        meeting = rng.choice(names)
        acts = meetings[meeting]
        i = rng.randint(8, len(acts) - 1)
        speaker = rng.choice(sorted({a["speaker"] for a in acts}))
        if not text:
            continue
        before = [Turn(speaker=a["speaker"], text=(a["stt"] if heard else a["gold"]).strip()) for a in acts[:i]]
        before = [t for t in before if t.text]
        k = kind(s["sentence"])
        rec = SidechatRecord(
            row_id=f"{set_name}/{s['slurp_id']}",
            set=set_name,
            conv_id=f"{meeting}+{s['slurp_id']}",
            turn_index=len(before),
            request=SidechatRequest(
                agent=AGENT,
                text=text,
                speaker=speaker,
                history=window(before + [Turn(speaker=speaker, text=text)], len(before)),
            ),
            label=guide.label_for(k),
            tags={
                "kind": k,
                "named": "1" if named(s["sentence"]) else "0",
                "scenario": s["scenario"],
                "intent": s["intent"],
                "meeting": meeting,
                "device": s.get("device", "headset"),
            },
        )
        rows.append(rec.model_dump(mode="json"))
    return rows
