"""Our generated corpora as a Hugging Face dataset: one flat row per line, its Arrow schema and the
dataset card. The Modal job that builds it is `sidechat/pipeline/dataset.py`."""

from __future__ import annotations

import json

SPLITS = {"train": "train", "dev": "validation", "test": "test"}  # ours -> the Hub's names
TAG_COLUMNS = ("kind", "rule", "setting", "writer", "register", "heldout")
SKIP_TAGS = ("split", "agent_name", "unnamed_agent", "brief_ok", "brief_problems", "label_safe")


def flat(r: dict) -> dict:
    """One corpus row as one dataset row. The writer's own checks are dropped: they are not data."""
    q, lab, tags = r["request"], r["label"], r["tags"]
    facts = q.get("facts") or {}
    other = {k: v for k, v in tags.items() if k not in TAG_COLUMNS and k not in SKIP_TAGS}
    return {
        "row_id": r["row_id"],
        "corpus": r["set"],
        "conv_id": r["conv_id"],
        "turn_index": r["turn_index"],
        "agent_name": q["agent"]["name"],
        "agent_aliases": list(q["agent"].get("aliases") or []),
        "agent_role": q["agent"].get("role"),
        "speaker": q.get("speaker"),
        "text": q["text"],
        "history": [
            {"speaker": t.get("speaker"), "text": t["text"], "agent": bool(t.get("agent"))} for t in q["history"]
        ],
        "people": q.get("people"),
        "over_agent": facts.get("over_agent"),
        "alone": facts.get("alone"),
        "to": lab["to"],
        "to_people": list(lab.get("to_people") or []),
        "intent": lab.get("intent"),
        "expect": lab.get("expect"),
        "respond": lab.get("respond"),
        "unclear": bool(lab.get("unclear")),
        **{t: tags.get(t) for t in TAG_COLUMNS},
        "unnamed_agent": tags.get("unnamed_agent") == "1",
        "other_tags": json.dumps(other, sort_keys=True, ensure_ascii=False),
    }


def arrow_schema():
    import pyarrow as pa

    s, b = pa.string(), pa.bool_()
    turn = pa.struct([("speaker", s), ("text", s), ("agent", b)])
    return pa.schema(
        [
            ("row_id", s),
            ("corpus", s),
            ("conv_id", s),
            ("turn_index", pa.int32()),
            ("agent_name", s),
            ("agent_aliases", pa.list_(s)),
            ("agent_role", s),
            ("speaker", s),
            ("text", s),
            ("history", pa.list_(turn)),
            ("people", pa.list_(s)),
            ("over_agent", b),
            ("alone", b),
            ("to", s),
            ("to_people", pa.list_(s)),
            ("intent", s),
            ("expect", s),
            ("respond", pa.float32()),
            ("unclear", b),
            *[(t, s) for t in TAG_COLUMNS],
            ("unnamed_agent", b),
            ("other_tags", s),
        ]
    )


def card(dataset_id: str, guide_version: str, counts: dict) -> str:
    """The dataset card, from the counts this build made."""
    n = counts["rows"]
    size = "100K<n<1M" if 100_000 <= n < 1_000_000 else "10K<n<100K" if n >= 10_000 else "1K<n<10K"
    head = f"""---
license: bsd-2-clause
language: en
pretty_name: Sidechat generated conversations
task_categories:
  - text-classification
tags:
  - pipecat
  - addressee-detection
  - multi-party
  - turn-taking
  - synthetic
size_categories:
  - {size}
configs:
  - config_name: default
    data_files:
      - split: train
        path: data/train-*.parquet
      - split: validation
        path: data/validation-*.parquet
      - split: test
        path: data/test-*.parquet
---
"""
    rows = "\n".join(
        f"| {g} | {c['conversations'] or 0:,} | {c['kept']['train']:,} | {c['kept']['validation']:,} | {c['kept']['test']:,} |"
        for g, c in counts["by_corpus"].items()
    )
    s = counts["by_split"]
    body = f"""
# Sidechat generated conversations (`{dataset_id}`)

Written conversations between several people and one voice agent, one row per line. Each line is
labelled with who it was for and whether the agent should speak. These are the conversations this
project wrote to train [Pipecat Sidechat](https://huggingface.co/pipecat-ai/sidechat). Its first
release, `rc1`, trained on the train splits of gen-pilot, gen-0.1 and gen-0.2, and on real meeting
speech (AMI), which is not included here.

Code: [github.com/pipecat-ai/sidechat](https://github.com/pipecat-ai/sidechat)

## How it was made

A planner lays out each conversation: a setting, two to five people, an agent with a name and a role,
and for every line a *kind* (a named request to the agent, an unnamed follow-up, a question to the
room, a remark to another person that mentions the agent, and so on). Language models, called o, a,
c and b here, write the lines to that plan. The label comes from the kind under the labelling guide
(`{guide_version}`), not from the writer. A committee of three other models, reading samples against
the guide, agreed with these labels on 95.3% of gen-pilot's and 95.8% of gen-0.2's checked lines.
Lines flagged as not matching their brief are left out, as are instructions between people in
sessions the agent runs, which the committee could not settle.

Names are invented. Training replaces speaker names with anonymous labels ("Speaker 1", in order of
first appearance) on most lines, since that is what a diarizer gives; the words still use names.

## Splits

Splits never cut a conversation. Conversations written by writer b, or with an agent name or a
setting kept out of training, are only in `test`, so the test split also measures what the model
never saw.

| Corpus | Conversations | Train | Validation | Test |
|---|---|---|---|---|
{rows}
| **All** | | **{s["train"]:,}** | **{s["validation"]:,}** | **{s["test"]:,}** |

## Columns

| Column | |
|---|---|
| `row_id`, `corpus`, `conv_id`, `turn_index` | where the line comes from; rows of one conversation share `conv_id` |
| `agent_name`, `agent_aliases`, `agent_role` | the agent's card |
| `speaker`, `text` | the line to judge |
| `history` | up to 8 earlier turns, oldest first: `speaker`, `text`, `agent` (the agent said it) |
| `people` | the people present |
| `over_agent` | the line was said while the agent was speaking (null: not known) |
| `alone` | one person present (null: not known) |
| `to` | who the line was for: `agent`, `person`, `group`, `device`, `nobody`, `unknown` |
| `to_people` | names, when `to` is `person` |
| `intent` | `direct`, `indirect`, `open` (to the room), `about` (about the agent), `other` |
| `expect` | `respond` (speak now), `wait` (speak only if nobody else does), `ignore`; null when either is fine |
| `respond` | target probability that the agent should speak now. A question left open to the room is about 0.5 |
| `unclear` | the line fits the agent and someone else equally |
| `kind`, `rule` | the planned kind of line and the guide rule that labels it |
| `setting`, `register`, `writer`, `heldout` | the scene, its tone, which writer wrote it, and whether that writer is held out |
| `unnamed_agent` | the agent is never named in this conversation |
| `other_tags` | any other tags, as JSON |
"""
    return head + body
