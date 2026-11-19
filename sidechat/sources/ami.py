"""AMI meetings with a silent agent: human addressee labels on real speech (scorecard item 17).

Source: https://huggingface.co/datasets/ACloudCenter/ami-addressee (CC BY 4.0, from the AMI Meeting
Corpus manual annotations v1.6.2, also CC BY 4.0). Test only for now.

Four people in a design meeting; annotators marked who each labelled dialogue act was addressed to,
one person or the group. We add an agent, "Atlas", that never speaks. Every labelled line is for
people, so the right decision is always to stay quiet: the set measures false answers and false
holds on real, messy speech. Speakers are AMI's letters (A to D), so this is the anonymous
condition. History is the eight dialogue acts before the line, from all four speakers, in time order.
"""

from __future__ import annotations

import re
from collections import defaultdict

from sidechat.schema import Agent, SidechatLabel, SidechatRecord, SidechatRequest, Turn, window

SET = "ami-addressee-0.1"
REPO = "ACloudCenter/ami-addressee"
REVISION = "4bab33cda7800e616f429da1be956f9ff4075511"
FILES = {"all": "data/records_all.jsonl"}
LICENCE = "CC BY 4.0"
USE = "test only for now"
AGENT = Agent(name="Atlas", role="AI assistant in the meeting")
# The same lines as transcribed from AMI's headset audio by a real speech-to-text service
# (`sidechat/pipeline/stt_ami.py`). A line or earlier turn whose transcript came back empty is
# dropped, as a live pipeline would never pass it on.
STT_SET = "ami-addressee-stt-0.1"
STT_PREFIX = "stt/ami-deepgram-nova-3"  # under runs/side in R2: transcripts.jsonl and manifest.json


def _clean(text: str) -> str:
    text = re.sub(r"\s+([,.?!;:])", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def with_stt(records: list[dict], stt: dict[str, str]) -> list[dict]:
    """The records with each dialogue act's text replaced by its transcript (empty if none)."""
    return [{**r, "text": stt.get(r["da_id"], "")} for r in records]


def convert(records: list[dict], set_name: str = SET) -> list[dict]:
    by_meeting: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        if r.get("text") and r["text"].strip():
            by_meeting[r["meeting_id"]].append(r)
    rows = []
    for meeting, recs in sorted(by_meeting.items()):
        if not any(r.get("labeled") for r in recs):
            continue
        recs.sort(key=lambda r: (r["start_time"], r["end_time"]))
        turns = [Turn(speaker=r["speaker"], text=_clean(r["text"])) for r in recs]
        for i, r in enumerate(recs):
            if not r.get("labeled") or not r.get("addressee_raw"):
                continue
            addressees = [x.strip() for x in r["addressee_raw"].split(",") if x.strip()]
            group = len(addressees) > 1
            label = SidechatLabel(
                to="group" if group else "person",
                to_people=[] if group else addressees,
                intent="other",
                expect="ignore",
                respond=0.0,
                source="human",
            )
            rec = SidechatRecord(
                row_id=f"{set_name}/{r['da_id']}",
                set=set_name,
                conv_id=meeting,
                turn_index=i,
                request=SidechatRequest(
                    agent=AGENT, text=turns[i].text, speaker=r["speaker"], history=window(turns, i), people=None
                ),
                label=label,
                tags={
                    "meeting": meeting,
                    "da_type": r.get("da_type") or "",
                    "addressee": "group" if group else "one person",
                    "words": str(min(r.get("n_words") or 0, 99)),
                },
            )
            rows.append(rec.model_dump(mode="json"))
    return rows


# --- AMI meetings with no addressee labels: real speech for training (SD-19) -------------------
#
# 117 of the 139 meetings have no addressee labels. Those in a series (the same four people) that
# shares no one with the 22 labelled meetings are split by series: 20 series train, 2 dev, 4 test.
# The agent sits in and is never called, so every line is for people: G7, ignore. Questions
# (dialogue acts `el.*`) are left out of train and dev, because a question to the room may be an
# even call under the guide; they stay in the history. Train is sampled by dialogue act; dev keeps
# every other line (it sets the thresholds' real-speech bar); test keeps every line, like the
# labelled set.

SILENT_SET = "ami-silent-0.1"
SILENT_STT_SET = "ami-silent-stt-0.1"
SILENT_USE = "train, dev and test by meeting series; the 22 labelled meetings are never trained on"
# Share of each dialogue act kept for train and dev: all suggestions, offers and reactions (where
# bare instructions between people are), fewer statements, very few stalls and fragments.
SILENT_RATES = {
    "sug": 1.0,
    "off": 1.0,
    "be.pos": 1.0,
    "be.neg": 1.0,
    "und": 0.5,
    "inf": 0.2,
    "ass": 0.2,
    "bck": 0.05,
    "stl": 0.03,
    "fra": 0.05,
}
SILENT_ROLES = ("AI assistant in the meeting", "AI note-taker on the call", "AI assistant on the call")


def series(meeting: str) -> str:
    return meeting[:-1] if meeting[-1:].isalpha() else meeting


def silent_split(series_id: str) -> str:
    import hashlib

    h = int(hashlib.sha1(f"ami-silent:{series_id}".encode()).hexdigest(), 16) % 100
    return "train" if h < 70 else "dev" if h < 80 else "test"


def convert_silent(records: list[dict], agent_names: list[str], set_name: str = "") -> list[dict]:
    """Rows from the unlabelled meetings, split by series. Train and dev get a training agent name
    drawn per meeting; test uses this set's usual agent, Atlas."""
    import random

    set_name = set_name or SILENT_SET
    labelled = {series(r["meeting_id"]) for r in records if r.get("labeled")}
    by_meeting: dict[str, list[dict]] = defaultdict(list)
    for r in records:
        if r.get("text") and r["text"].strip() and series(r["meeting_id"]) not in labelled:
            by_meeting[r["meeting_id"]].append(r)
    rows = []
    for meeting, recs in sorted(by_meeting.items()):
        split = silent_split(series(meeting))
        rng = random.Random(f"ami-silent:{meeting}")
        agent = AGENT if split == "test" else Agent(name=rng.choice(agent_names), role=rng.choice(SILENT_ROLES))
        recs.sort(key=lambda r: (r["start_time"], r["end_time"]))
        turns = [Turn(speaker=r["speaker"], text=_clean(r["text"])) for r in recs]
        for i, r in enumerate(recs):
            da = r.get("da_type") or ""
            if split == "train" and rng.random() >= SILENT_RATES.get(da, 0.0):
                continue
            if split == "dev" and (da.startswith("el.") or da in ("", "oth")):
                continue
            label = SidechatLabel(to="group", intent="other", expect="ignore", respond=0.0, source="ami-silent")
            rec = SidechatRecord(
                row_id=f"{set_name}/{r['da_id']}",
                set=set_name,
                conv_id=meeting,
                turn_index=i,
                request=SidechatRequest(
                    agent=agent, text=turns[i].text, speaker=r["speaker"], history=window(turns, i), people=None
                ),
                label=label,
                tags={
                    "meeting": meeting,
                    "series": series(meeting),
                    "split": split,
                    "da_type": da,
                    "kind": "ami_silent",
                    "words": str(min(r.get("n_words") or 0, 99)),
                },
            )
            rows.append(rec.model_dump(mode="json"))
    return rows
