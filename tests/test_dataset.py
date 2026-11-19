"""The Hugging Face dataset job's row flattening and card (sidechat/lib/hf_dataset.py)."""

from __future__ import annotations

import json

import pytest

from sidechat.lib import hf_dataset as dataset

ROW = {
    "schema_version": "sidechat-0.1",
    "row_id": "gen-x/o01-00000/2",
    "set": "gen-x",
    "conv_id": "o01-00000",
    "turn_index": 2,
    "request": {
        "agent": {"name": "Gus", "aliases": [], "role": "AI assistant on the call"},
        "text": "Gus, what time is it there?",
        "speaker": "Ana",
        "history": [{"speaker": "Ana", "text": "Morning.", "agent": False}],
        "people": ["Ana", "Ben"],
        "facts": {"alone": None, "over_agent": True},
    },
    "label": {
        "to": "agent",
        "to_people": [],
        "intent": "direct",
        "expect": "respond",
        "respond": 0.97,
        "unclear": False,
        "source": "guide",
    },
    "tags": {
        "kind": "named_question",
        "rule": "G1",
        "setting": "s",
        "writer": "o",
        "register": "r",
        "split": "train",
        "heldout": "",
        "brief_ok": "1",
        "label_safe": "1",
        "brief_problems": "",
        "agent_name": "Gus",
        "unnamed_agent": "0",
        "delayed": "1",
    },
}


def test_flat_keeps_the_data_and_drops_the_writers_checks():
    f = dataset.flat(ROW)
    assert f["corpus"] == "gen-x" and f["text"] == ROW["request"]["text"]
    assert f["over_agent"] is True and f["alone"] is None
    assert f["unnamed_agent"] is False and f["respond"] == 0.97
    assert json.loads(f["other_tags"]) == {"delayed": "1"}
    assert not {"brief_ok", "label_safe", "brief_problems", "split"} & set(f)


def test_the_schema_matches_the_rows():
    pytest.importorskip("pyarrow")  # only in the Modal image
    assert dataset.arrow_schema().names == list(dataset.flat(ROW))


def test_card_names_the_hub_splits():
    counts = {
        "rows": 3,
        "by_split": {"train": 1, "validation": 1, "test": 1},
        "by_corpus": {"gen-x": {"conversations": 1, "kept": {"train": 1, "validation": 1, "test": 1}}},
    }
    text = dataset.card("t", "sidechat-guide-0.4", counts)
    assert set(dataset.SPLITS.values()) == {"train", "validation", "test"}
    assert all(f"path: data/{s}-*.parquet" in text for s in dataset.SPLITS.values())
    assert "| gen-x | 1 | 1 | 1 | 1 |" in text
