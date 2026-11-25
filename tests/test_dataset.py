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
    assert "not here" not in text.split("## Splits")[1]


def test_card_says_what_a_left_out_setting_holds_without_naming_it():
    counts = {
        "rows": 3,
        "by_split": {"train": 1, "validation": 1, "test": 1},
        "by_corpus": {"gen-x": {"conversations": 2, "kept": {"train": 1, "validation": 1, "test": 1}}},
        "left_out_settings": {"some_setting": 1036},
    }
    text = dataset.card("t", "sidechat-guide-0.5", counts)
    assert "is not here (1,036 lines)" in text and "some_setting" not in text
    assert "| **All** | **2** | **1** | **1** | **1** |" in text


def test_settings_this_repository_does_not_define_are_not_published():
    from sidechat.gen import world
    from sidechat.lib.hf_dataset import not_published

    own = min(world.OWN_IDS)
    assert not not_published(own, set(), True) and not not_published(None, set(), True)
    assert not_published("a_setting_defined_elsewhere", set(), True)
    assert not not_published("a_setting_defined_elsewhere", set(), False)  # `--drop-settings ""` publishes all
    assert not_published(own, {own}, False)
    for s in world.ALL_SETTINGS:  # whatever else this machine defines stays out by default
        assert not_published(s.id, set(), True) == (s.id not in world.OWN_IDS)
