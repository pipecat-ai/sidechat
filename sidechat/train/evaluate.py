"""Turn Sidechat's probabilities into decisions and score them like Jev (scorecard 0.1).

A decision is the gate's three outcomes. With thresholds chosen on dev and fixed before test:

    respond  when respond >= t_respond
    wait     when respond >= t_wait or intent.open >= t_open
    ignore   otherwise

No torch here.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import product

from sidechat.lib.score import auroc, ece, paired, share
from sidechat.pipeline.scorecard import decision_metrics

T_RESPOND = [x / 100 for x in range(40, 91, 5)]
T_WAIT = [x / 100 for x in range(20, 61, 5)]
T_OPEN = [x / 100 for x in range(20, 81, 10)] + [1.01]


def decide(p: dict, t: dict) -> str:
    if p["respond"] >= t["respond"]:
        return "respond"
    if p["respond"] >= t["wait"] or p["intent"]["open"] >= t["open"]:
        return "wait"
    return "ignore"


def choose_thresholds(
    preds: dict[str, dict],
    rows: list[dict],
    max_wrong_now: float = 0.01,
    real_rows: list[dict] | None = None,
    max_wrong_now_real: float = 0.004,
) -> dict:
    """The thresholds with the most decisions right on rows with a definite decision, among those that
    answer at most `max_wrong_now` of the stay-quiet lines outright (scorecard item 2: answering a
    line meant for someone else is the costly error). Ties go to the higher answer-now threshold.

    `real_rows` (stay-quiet lines of real speech, their predictions in `preds`) add a second bar:
    answer at most `max_wrong_now_real` of them outright. Item 2's bar on Duplex-MPE is 0.4%; real
    speech is where the generated dev is too easy. They do not count towards decisions right.
    """
    lab = [(preds[r["row_id"]], r["label"]["expect"]) for r in rows if r["label"]["expect"] and r["row_id"] in preds]
    quiet = max(1, sum(e == "ignore" for _, e in lab))
    real = [
        preds[r["row_id"]]["respond"]
        for r in real_rows or []
        if r["label"]["expect"] == "ignore" and r["row_id"] in preds
    ]
    best, best_key, fallback, fallback_key = None, None, None, None
    for tr, tw, to in product(T_RESPOND + [0.92, 0.94, 0.96, 0.98], T_WAIT, T_OPEN):
        if tw >= tr:
            continue
        t = {"respond": tr, "wait": tw, "open": to}
        right = sum(decide(p, t) == e for p, e in lab)
        wrong_now = sum(decide(p, t) == "respond" and e == "ignore" for p, e in lab)
        wrong_real = sum(x >= tr for x in real)
        key = (right, -wrong_now, tr)
        ok = wrong_now / quiet <= max_wrong_now and (not real or wrong_real / len(real) <= max_wrong_now_real)
        if ok and (best_key is None or key > best_key):
            best, best_key = t, key
        fkey = (-wrong_real, -wrong_now, right)
        if fallback_key is None or fkey > fallback_key:
            fallback, fallback_key = t, fkey
    if best is None:
        best, best_key = fallback, (fallback_key[2], fallback_key[1], fallback["respond"])
    wrong = sum(decide(p, best) == "respond" and e == "ignore" for p, e in lab)
    out = {
        **best,
        "dev_right": best_key[0],
        "dev_n": len(lab),
        "dev_wrong_now": wrong,
        "dev_quiet": quiet,
        "max_wrong_now": max_wrong_now,
    }
    if real:
        out.update(
            real_wrong_now=sum(x >= best["respond"] for x in real),
            real_quiet=len(real),
            max_wrong_now_real=max_wrong_now_real,
        )
    return out


def set_card(rows: list[dict], preds: dict[str, dict], t: dict, jev: dict[str, dict] | None = None) -> dict:
    """Decision metrics for Sidechat (and Jev on the same rows, when its scores are given)."""
    from sidechat.baselines import jev_demo

    rows = [r for r in rows if r["row_id"] in preds and r["tags"].get("conflict") != "1"]
    side = {r["row_id"]: decide(preds[r["row_id"]], t) for r in rows}
    expect = {r["row_id"]: r["label"]["expect"] for r in rows}
    card: dict = {"rows": len(rows), "sidechat": decision_metrics([(expect[i], side[i]) for i in side])}
    if jev:
        both = [r for r in rows if r["row_id"] in jev]
        jd = {r["row_id"]: jev_demo.decision(jev[r["row_id"]]["addressed"], jev[r["row_id"]]["question"]) for r in both}
        card["jev"] = decision_metrics([(expect[i], jd[i]) for i in jd])
        lab = [r["row_id"] for r in both if expect[r["row_id"]]]
        card["sidechat_vs_jev"] = paired([jd[i] == expect[i] for i in lab], [side[i] == expect[i] for i in lab])
    known = [r for r in rows if r["label"]["to"] != "unknown"]
    if known:
        pairs = [(preds[r["row_id"]]["respond"], r["label"]["to"] == "agent") for r in known]
        card["respond_auroc_for_agent"] = auroc(pairs)
    graded = [
        (preds[r["row_id"]]["respond"], r["label"]["respond"]) for r in rows if r["label"].get("respond") is not None
    ]
    if graded:
        card["respond_calibration_error"] = ece(graded)
        card["respond_mean_abs_error"] = round(sum(abs(p - y) for p, y in graded) / len(graded), 4)
    waits = [preds[r["row_id"]]["respond"] for r in rows if r["label"]["expect"] == "wait"]
    if waits:
        card["even_call"] = {
            "n": len(waits),
            "mean_respond": round(sum(waits) / len(waits), 4),
            "share_between_0.25_and_0.75": share(sum(0.25 <= w <= 0.75 for w in waits), len(waits)),
        }
    return card


def sliced(
    rows: list[dict], preds: dict[str, dict], t: dict, tag: str, jev: dict | None = None, min_n: int = 20
) -> dict:
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        groups[r["tags"].get(tag, "")].append(r)
    return {
        k: set_card(g, preds, t, jev) for k, g in sorted(groups.items(), key=lambda kv: -len(kv[1])) if len(g) >= min_n
    }
