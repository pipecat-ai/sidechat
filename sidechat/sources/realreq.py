"""Real people's requests to an assistant, said in real meetings: training lines for item 5.

Every model ignores most unnamed requests an assistant could do when they are said in a meeting
where it has not spoken (exp-057: both builds miss 82% to 97% of SLURP's recorded requests; Jev
holds for 82%). The generator's requests are written by language models; these are people's own.

Requests:

- SLURP's text, train and devel splits (https://github.com/pswietojanski/slurp, CC BY 4.0; only its
  audio is non-commercial, and none is used here). Requests that also appear in its test split are
  left out, since that split is a test set (exp-057).
- CLINC150's in-scope queries, train and val splits (https://github.com/clinc/oos-eval, CC BY 3.0).

Each request is said at a seeded point in one of AMI's unlabelled meetings (the `ami-silent` series
split: train meetings for train, dev for dev; never the 22 labelled meetings or the silence test),
by one of its speakers, with the eight dialogue acts before it as history. The agent has a training
name and an AI role and has not spoken. Labels follow guide 0.4:

    60%  as said, no name           open_request: hold for a pause (respond 0.5)
    25%  the agent's name added      name_first or name_last: respond
    15%  a person's name added       question_to_named_person: ignore (the name settles it)

SLURP's "olly" becomes the agent's name. Text is given a capital and an end mark, as a
speech-to-text service with formatting writes it, so case and punctuation do not give it away.
"""

from __future__ import annotations

import random
import re
from collections import defaultdict

from sidechat import guide
from sidechat.schema import Agent, SidechatRecord, SidechatRequest, Turn, window
from sidechat.sources import ami

SET = "realreq-0.1"
# Versions by corpus name: how many requests from each source, and the shares said unnamed (held)
# and with the agent's name (answered); the rest name a person (left alone). 0.2 (round 9) has fewer
# requests and more said to a person, after round 8's model held more of people's own talk.
VERSIONS = {
    "realreq": {
        "set": "realreq-0.1",
        "sizes": {"train": {"slurp": 7000, "clinc": 5000}, "dev": {"slurp": 1200, "clinc": 800}},
        "unnamed": 0.60,
        "agent_named": 0.25,
    },
    "realreq-0.2": {
        "set": "realreq-0.2",
        "sizes": {"train": {"slurp": 3000, "clinc": 2000}, "dev": {"slurp": 600, "clinc": 400}},
        "unnamed": 0.45,
        "agent_named": 0.25,
    },
}
SLURP_URL = "https://raw.githubusercontent.com/pswietojanski/slurp/{commit}/dataset/slurp/{split}.jsonl"
SLURP_COMMIT = "8eb16545762be97ace75334109d73824217311f1"
CLINC_URL = "https://raw.githubusercontent.com/clinc/oos-eval/{commit}/data/data_full.json"
CLINC_COMMIT = "828f8093932c8fe6ca7936c3d2e52903b1c523de"
LICENCE = "SLURP text CC BY 4.0; CLINC150 CC BY 3.0; AMI CC BY 4.0"
USE = "training (train and dev splits only)"
SIZES = VERSIONS["realreq"]["sizes"]
QUESTION_START = re.compile(
    r"^(what|who|whom|whose|where|when|why|how|which|is|are|am|was|were|can|could|would|will|do|does|did|"
    r"should|shall|may|might|have|has|had|any|anything)\b"
)


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9' ]", " ", text.lower())).strip()


def formatted(text: str) -> str:
    """Lower-case corpus text as a formatting speech-to-text service would write it."""
    t = re.sub(r"\s+", " ", text).strip()
    t = re.sub(r"\bi\b", "I", t)
    t = re.sub(r"\bi'(m|ll|ve|d)\b", lambda m: "I'" + m.group(1), t)
    end = "?" if QUESTION_START.match(t.lower()) else "."
    t = t.rstrip(" .?!")
    return (t[:1].upper() + t[1:] + end) if t else t


def after_name(body: str) -> str:
    """A formatted request as it reads after a name and a comma: no capital, except "I"."""
    return body if body[:2] in ("I ", "I'") else body[:1].lower() + body[1:]


def requests(slurp: dict[str, list[dict]], clinc: dict, slurp_test: list[dict], version: str = "realreq") -> list[dict]:
    """The requests used, each with a stable id, its source and its split. `slurp` maps "train" and
    "devel" to SLURP's rows; `clinc` is CLINC's data_full.json."""
    held_out = {norm(r["sentence"]) for r in slurp_test}
    out, seen = [], set()

    def add(text: str, source: str, split: str, ident: str) -> None:
        n = norm(text)
        if not n or n in held_out or n in seen:
            return
        seen.add(n)
        out.append({"id": ident, "text": text, "source": source, "split": split})

    for split, name in (("train", "train"), ("dev", "devel")):
        for r in slurp.get(name, []):
            add(r["sentence"], "slurp", split, f"slurp-{r['slurp_id']}")
    for split, name in (("train", "train"), ("dev", "val")):
        for i, (text, _intent) in enumerate(clinc.get(name, [])):
            add(text, "clinc", split, f"clinc-{name}-{i}")
    rng = random.Random("realreq-sample")
    picked = []
    for split, want in VERSIONS[version]["sizes"].items():
        for source, n in want.items():
            pool = [r for r in out if r["split"] == split and r["source"] == source]
            rng.shuffle(pool)
            picked.extend(sorted(pool[:n], key=lambda r: r["id"]))
    return picked


def convert(
    reqs: list[dict], records: list[dict], agent_names: list[str], people: list[str], version: str = "realreq"
) -> list[dict]:
    """Rows: each request said in an AMI meeting of its split. `records` are ACloudCenter's AMI
    records (all of them; the labelled series and the silence test are never used)."""
    labelled = {ami.series(r["meeting_id"]) for r in records if r.get("labeled")}
    meetings: dict[str, dict[str, list[dict]]] = {"train": defaultdict(list), "dev": defaultdict(list)}
    for r in records:
        s = ami.series(r["meeting_id"])
        split = ami.silent_split(s)
        if r.get("text") and r["text"].strip() and s not in labelled and split in meetings:
            meetings[split][r["meeting_id"]].append(r)
    for by_meeting in meetings.values():
        for recs in by_meeting.values():
            recs.sort(key=lambda r: (r["start_time"], r["end_time"]))
    v = VERSIONS[version]
    set_name, unnamed, named_to = v["set"], v["unnamed"], v["unnamed"] + v["agent_named"]
    rows = []
    for q in reqs:
        pool = meetings[q["split"]]
        rng = random.Random(f"realreq:{q['id']}")
        meeting = rng.choice(sorted(pool))
        acts = pool[meeting]
        i = rng.randint(8, len(acts) - 1)
        speaker = rng.choice(sorted({a["speaker"] for a in acts}))
        agent = Agent(name=rng.choice(agent_names), role=rng.choice(ami.SILENT_ROLES))
        words = q["text"].split()
        named_in_text = "olly" in [w.lower() for w in words]
        text = " ".join(agent.name if w.lower() == "olly" else w for w in words)
        roll = rng.random()
        if named_in_text:
            kind = (
                "name_first"
                if words[0].lower() == "olly"
                else "name_last"
                if words[-1].lower() == "olly"
                else "name_mid"
            )
            line, to_people = formatted(text), None
        elif roll < unnamed:
            kind, line, to_people = "open_request", formatted(text), None
        elif roll < named_to:
            if rng.random() < 0.6:
                kind, line = "name_first", f"{agent.name}, {after_name(formatted(text))}"
            else:
                body = formatted(text)
                kind, line = "name_last", f"{body[:-1]}, {agent.name}{body[-1]}"
            to_people = None
        else:
            person = rng.choice([p for p in people if p != agent.name])
            kind, line, to_people = "question_to_named_person", f"{person}, {after_name(formatted(text))}", [person]
        line = line[:1].upper() + line[1:]
        turns = [Turn(speaker=a["speaker"], text=ami._clean(a["text"])) for a in acts[:i]]
        rec = SidechatRecord(
            row_id=f"{set_name}/{q['id']}",
            set=set_name,
            conv_id=f"{meeting}+{q['id']}",
            turn_index=len(turns),
            request=SidechatRequest(
                agent=agent,
                text=line,
                speaker=speaker,
                history=window(turns + [Turn(speaker=speaker, text=line)], len(turns)),
            ),
            label=guide.label_for(kind, to_people),
            tags={"kind": kind, "split": q["split"], "source": q["source"], "meeting": meeting, "realreq": "1"},
        )
        rows.append(rec.model_dump(mode="json"))
    return rows
