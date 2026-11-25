"""Phase 4 helpers that need no torch: input features, decisions and thresholds."""

from __future__ import annotations

from sidechat.schema import INTENTS, SidechatRequest
from sidechat.sources import suites
from sidechat.train import evaluate, features


def _p(respond, open_=0.0):
    intent = dict.fromkeys(INTENTS, 0.0)
    intent["open"] = open_
    return {"respond": respond, "intent": intent, "unclear": 0.0}


def test_decide():
    t = {"respond": 0.7, "wait": 0.4, "open": 0.5}
    assert evaluate.decide(_p(0.9), t) == "respond"
    assert evaluate.decide(_p(0.5), t) == "wait"
    assert evaluate.decide(_p(0.1, 0.6), t) == "wait"
    assert evaluate.decide(_p(0.1, 0.1), t) == "ignore"


def test_choose_thresholds_finds_separation():
    rows, preds = [], {}
    for i, (exp, p) in enumerate([("respond", 0.95)] * 20 + [("wait", 0.5)] * 10 + [("ignore", 0.05)] * 30):
        rid = f"r{i}"
        rows.append({"row_id": rid, "label": {"expect": exp}, "tags": {}})
        preds[rid] = _p(p)
    t = evaluate.choose_thresholds(preds, rows)
    assert t["dev_right"] == 60 and t["respond"] > 0.5 > t["wait"]


def test_set_card_on_pilot():
    rows = suites.convert(suites.load("pilot-0.4"))
    preds = {r["row_id"]: _p(r["label"]["respond"] if r["label"]["respond"] is not None else 0.5) for r in rows}
    t = {"respond": 0.7, "wait": 0.4, "open": 1.01}
    card = evaluate.set_card(rows, preds, t)
    assert card["sidechat"]["decision_right"]["value"] == 1.0  # the labels' own targets decide perfectly
    assert card["even_call"]["mean_respond"] == 0.5


def test_features_shape():
    r = suites.convert(suites.load("pilot-0.4"))[10]
    req = SidechatRequest(**r["request"])
    text, start = features.text(req)
    assert text.startswith("agent: ") and text[start:].startswith(">> [")
    assert len(features.numbers(req)) == features.NUM_DIM
