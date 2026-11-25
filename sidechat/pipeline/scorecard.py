"""The baseline scorecard: how a system's decisions compare with each set's labels.

A decision is one of the three outcomes the daily-audience gate has: `respond` (answer now), `wait`
(hold the answer, give it if nobody else speaks) and `ignore` (stay quiet). Every share carries its
count and a 95% Wilson interval. `render` turns a scorecard into the Markdown report.
"""

from __future__ import annotations

from collections import defaultdict

from sidechat.baselines import jev_demo, name_only
from sidechat.lib.score import auroc, average_precision, ece, paired, quantile, share
from sidechat.schema import SidechatRequest

SWEEP = (0.5, 0.6, 0.7, 0.8, 0.9)
SLICE_TAGS = {
    "duplex-mpe-0.1": ("condition", "event", "condition/event", "addressee", "speech_act"),
    "ambient-bench-0.1": ("bench", "category"),
}
SUITE_TAGS = ("code", "style", "kind")


def decision_metrics(pairs: list[tuple[str | None, str]]) -> dict:
    """`pairs` are (expected, decided). Lines with no expectation count only towards `n`."""
    ign = [d for e, d in pairs if e == "ignore"]
    res = [d for e, d in pairs if e == "respond"]
    wai = [d for e, d in pairs if e == "wait"]
    lab = [(e, d) for e, d in pairs if e]
    return {
        "n": len(pairs),
        "decision_right": share(sum(e == d for e, d in lab), len(lab)),
        # lines for someone else
        "quiet_kept": share(sum(d == "ignore" for d in ign), len(ign)),
        "answers_now_wrongly": share(sum(d == "respond" for d in ign), len(ign)),
        "holds_wrongly": share(sum(d == "wait" for d in ign), len(ign)),
        # lines for the agent
        "answered_now": share(sum(d == "respond" for d in res), len(res)),
        "held_instead": share(sum(d == "wait" for d in res), len(res)),
        "missed": share(sum(d == "ignore" for d in res), len(res)),
        # open questions
        "open_held": share(sum(d == "wait" for d in wai), len(wai)),
        "open_answered_now": share(sum(d == "respond" for d in wai), len(wai)),
        "open_ignored": share(sum(d == "ignore" for d in wai), len(wai)),
    }


def bench_metrics(rows: list[dict], predict_speak: dict[str, bool]) -> dict:
    """Social AI Ambient Bench's own metrics, from its card."""
    tp = fp = fn = tn = 0
    by_scenario: dict[str, bool] = {}
    for r in rows:
        expected, got = r["tags"]["bench"] == "RESPOND", predict_speak[r["row_id"]]
        tp += expected and got
        fp += (not expected) and got
        fn += expected and not got
        tn += (not expected) and not got
        by_scenario[r["conv_id"]] = by_scenario.get(r["conv_id"], True) and (expected == got)

    def f1(tp_, fp_, fn_):
        return 2 * tp_ / (2 * tp_ + fp_ + fn_) if (2 * tp_ + fp_ + fn_) else 0.0

    return {
        "scenario_pass_rate": share(sum(by_scenario.values()), len(by_scenario)),
        "macro_f1": round((f1(tp, fp, fn) + f1(tn, fn, fp)) / 2, 4),
        "false_interruption_rate": share(fp, fp + tn),
        "missed_intervention_rate": share(fn, fn + tp),
        "turn_accuracy": share(tp + tn, tp + tn + fp + fn),
        "counts": {"tp": tp, "fp": fp, "fn": fn, "tn": tn},
    }


def _tag(row: dict, name: str) -> str:
    if "/" in name:
        return "/".join(row["tags"].get(part, "") for part in name.split("/"))
    return row["tags"].get(name, "")


def set_card(rows_id: str, rows: list[dict], scores: dict[str, dict], extras: dict) -> dict:
    scored = [r for r in rows if r["row_id"] in scores and r["tags"].get("conflict") != "1"]
    card: dict = {
        "rows": len(rows),
        "scored": len(scored),
        "unscored": sum(1 for r in rows if r["row_id"] not in scores),
        "label_conflicts_left_out": sum(1 for r in rows if r["tags"].get("conflict") == "1"),
    }
    if not scored:
        return card
    jev = {
        r["row_id"]: jev_demo.decision(scores[r["row_id"]]["addressed"], scores[r["row_id"]]["question"])
        for r in scored
    }
    name = {r["row_id"]: name_only.decision(SidechatRequest(**r["request"])) for r in scored}
    expect = {r["row_id"]: r["label"]["expect"] for r in scored}
    systems = {"jev_demo": jev, "name_only": name}

    card["systems"] = {s: decision_metrics([(expect[i], d[i]) for i in d]) for s, d in systems.items()}
    card["jev_vs_name_only"] = paired(
        [name[i] == expect[i] for i in name if expect[i]], [jev[i] == expect[i] for i in jev if expect[i]]
    )

    # Jev's probabilities, read without a threshold.
    known = [r for r in scored if r["label"]["to"] != "unknown"]
    if known:
        pairs = [(scores[r["row_id"]]["addressed"], r["label"]["to"] == "agent") for r in known]
        card["addressed_probability"] = {
            "positive": "the line was for the agent",
            "auroc": auroc(pairs),
            "average_precision": average_precision(pairs),
            "calibration_error": ece([(p, float(y)) for p, y in pairs]),
        }
    card["threshold_sweep"] = {
        str(t): {
            "answered_now": share(
                sum(scores[i]["addressed"] >= t for i in expect if expect[i] == "respond"),
                sum(1 for i in expect if expect[i] == "respond"),
            ),
            "answers_now_wrongly": share(
                sum(scores[i]["addressed"] >= t for i in expect if expect[i] == "ignore"),
                sum(1 for i in expect if expect[i] == "ignore"),
            ),
        }
        for t in SWEEP
    }

    # Slices.
    tags = SLICE_TAGS.get(rows_id, SUITE_TAGS)
    card["slices"] = {}
    for tag in tags:
        groups: dict[str, list[dict]] = defaultdict(list)
        for r in scored:
            groups[_tag(r, tag)].append(r)
        card["slices"][tag] = {
            value: {
                s: decision_metrics([(expect[r["row_id"]], d[r["row_id"]]) for r in group]) for s, d in systems.items()
            }
            for value, group in sorted(groups.items(), key=lambda kv: -len(kv[1]))
        }

    if rows_id == "duplex-mpe-0.1":
        # The same request with and without the agent's name, pair by pair.
        by_pair: dict[str, dict[str, bool]] = defaultdict(dict)
        for r in scored:
            if r["tags"]["event"] == "T":
                by_pair[r["conv_id"]][r["tags"]["condition"]] = jev[r["row_id"]] == "respond"
        both = [v for v in by_pair.values() if len(v) == 2]
        card["named_vs_unnamed_request"] = {
            "note": "b is the request without the agent's name, a is the same request with it",
            **paired([v["explicit"] for v in both], [v["implicit"] for v in both]),
        }
    if rows_id == "ambient-bench-0.1":
        card["bench"] = {
            "strict (speaks = answers now)": bench_metrics(scored, {i: jev[i] == "respond" for i in jev}),
            "lenient (speaks = answers now or holds)": bench_metrics(scored, {i: jev[i] != "ignore" for i in jev}),
            "name_only": bench_metrics(scored, {i: name[i] == "respond" for i in name}),
        }
        speak = [
            (max(scores[r["row_id"]]["addressed"], scores[r["row_id"]]["question"]), r["tags"]["bench"] == "RESPOND")
            for r in scored
        ]
        card["bench"]["auroc of max(addressed, question)"] = auroc(speak)
        board = (extras.get("leaderboard") or {}).get("leaderboard") or []
        card["bench"]["their_leaderboard_top"] = board[:3]
        card["bench"]["their_prompt"] = (extras.get("leaderboard") or {}).get("prompt")
    if rows_id not in SLICE_TAGS:
        # Suites are small enough to list line by line.
        card["lines"] = [
            {
                "id": r["row_id"].split("/", 1)[1],
                "kind": r["tags"].get("kind", ""),
                "speaker": r["request"]["speaker"],
                "text": r["request"]["text"],
                "expect": expect[r["row_id"]],
                "addressed": scores[r["row_id"]]["addressed"],
                "question": scores[r["row_id"]]["question"],
                "jev": jev[r["row_id"]],
            }
            for r in scored
        ]
    ms = [scores[r["row_id"]]["ms"] for r in scored if scores[r["row_id"]].get("ms") is not None]
    card["latency_ms"] = {"p50": quantile(ms, 0.5), "p95": quantile(ms, 0.95), "n": len(ms)}
    return card


def build(sets: dict[str, dict], meta: dict) -> dict:
    """`sets` maps rows_id to {"rows", "scores", "manifest", "extras"}."""
    return {
        "meta": meta,
        "sets": {
            rows_id: {"manifest": s["manifest"], **set_card(rows_id, s["rows"], s["scores"], s.get("extras", {}))}
            for rows_id, s in sets.items()
        },
    }


# ---------------------------------------------------------------------------------------------
# Markdown


def _pct(s: dict | None) -> str:
    if not s or s.get("value") is None:
        return "n/a"
    lo, hi = s["ci95"]
    return f"{100 * s['value']:.1f}% ({s['k']}/{s['n']}; {100 * lo:.1f} to {100 * hi:.1f})"


def _short(s: dict | None) -> str:
    if not s or s.get("value") is None:
        return "n/a"
    return f"{100 * s['value']:.1f}% ({s['k']}/{s['n']})"


SYSTEM_NAMES = {"jev_demo": "Jev, demo thresholds", "name_only": "Name said → answer"}


def _systems_table(systems: dict) -> list[str]:
    out = [
        "| System | Decision right | For others: stays quiet | For others: answers now | For others: holds | For the agent: answers now | For the agent: missed |",
        "|---|---|---|---|---|---|---|",
    ]
    for key, m in systems.items():
        out.append(
            f"| {SYSTEM_NAMES.get(key, key)} | {_pct(m['decision_right'])} | {_short(m['quiet_kept'])} | "
            f"{_short(m['answers_now_wrongly'])} | {_short(m['holds_wrongly'])} | {_short(m['answered_now'])} | {_short(m['missed'])} |"
        )
    return out


def _slice_table(title: str, slices: dict, system: str = "jev_demo", limit: int = 40) -> list[str]:
    out = [
        f"**By {title}** (Jev, demo thresholds)",
        "",
        "| Slice | Lines | Decision right | For others: answers now | For others: holds | For the agent: answers now | Missed |",
        "|---|---|---|---|---|---|---|",
    ]
    for value, by_system in list(slices.items())[:limit]:
        m = by_system[system]
        out.append(
            f"| `{value}` | {m['n']} | {_short(m['decision_right'])} | {_short(m['answers_now_wrongly'])} | "
            f"{_short(m['holds_wrongly'])} | {_short(m['answered_now'])} | {_short(m['missed'])} |"
        )
    return out + [""]


def render(card: dict) -> str:
    meta = card["meta"]
    use = meta.get("usage", {})
    out = [
        f"# Jev baseline: {meta['exp']}",
        "",
        f"Generated {meta['finished_at']} by `sidechat/pipeline/baseline.py`. Every number below is measured in this run.",
        "",
        "## What was run",
        "",
        (
            f"- **Model:** `{meta['jev_model']}`, asked with the daily-audience demo's two questions and state "
            f"(commit `{jev_demo.DEMO_COMMIT}`, wording hash `{meta['prompt_sha']}`), through Pipecat {jev_demo.DEMO_PIPECAT}'s `JevClassifier`."
        ),
        (
            f"- **Decision rule:** the demo's. Answer now when `addressed ≥ {jev_demo.RESPOND_THRESHOLD}`, hold for silence when "
            f"`question ≥ {jev_demo.QUESTION_THRESHOLD}`, otherwise stay quiet."
        ),
        (
            f"- **Requests:** {use.get('requests', 0):,} distinct ({use.get('reused', 0):,} reused from earlier runs, "
            f"{use.get('asked', 0):,} asked now, {use.get('failed', 0):,} failed)."
        ),
        (
            f"- **Tokens this run:** {use.get('input_tokens', 0):,} in, {use.get('output_tokens', 0):,} out. "
            f"About ${use.get('usd_estimate', 0)} at ${use.get('usd_per_m_input')} per million input tokens, an assumed price."
        ),
        f"- **Baseline id:** `{meta['baseline_id']}`. Stored answers are reused, so later runs compare against these numbers.",
        "",
        'A share is written `value (k/n; 95% interval)`. "For others" means lines the set marks as not for the agent.',
        "",
    ]
    for rows_id, s in card["sets"].items():
        src = s["manifest"]["source"]
        where = src.get("repo") or src.get("file")
        out += [
            f"## {rows_id}",
            "",
            f"Source: `{where}`"
            + (f" at `{src['revision'][:12]}`" if src.get("revision") else "")
            + f". Use: {src.get('use', '')}.",
            "",
        ]
        out.append(
            f"{s['rows']:,} rows, {s['scored']:,} scored"
            + (
                f", {s['label_conflicts_left_out']} left out because the set's own labels disagree"
                if s.get("label_conflicts_left_out")
                else ""
            )
            + (f", {s['unscored']} without an answer from Jev" if s.get("unscored") else "")
            + "."
        )
        out.append("")
        if "systems" not in s:
            continue
        out += _systems_table(s["systems"]) + [""]
        lat = s.get("latency_ms", {})
        if lat.get("p50") is not None:
            out += [
                (
                    f"Jev latency from Modal: {lat['p50']:.0f} ms at the median, {lat['p95']:.0f} ms at the 95th percentile "
                    f"({lat['n']:,} answers, {meta.get('concurrency')} requests at a time)."
                ),
                "",
            ]
        if s.get("addressed_probability", {}).get("auroc", {}).get("value") is not None:
            a = s["addressed_probability"]
            out += [
                (
                    f"Jev's `addressed` number without a threshold: AUROC {a['auroc']['value']}, average precision {a['average_precision']['value']}, "
                    f"calibration error {a['calibration_error']['value']} ({a['auroc']['pos']:,} lines for the agent, {a['auroc']['neg']:,} not)."
                ),
                "",
            ]
        if "named_vs_unnamed_request" in s:
            p = s["named_vs_unnamed_request"]
            if p.get("diff") is not None:
                out += [
                    (
                        f"**The same request with and without the agent's name** ({p['n']:,} pairs): answered now {100 * p['a_right'] / p['n']:.1f}% with the name, "
                        f"{100 * p['b_right'] / p['n']:.1f}% without. Difference {100 * p['diff']:+.1f} points ({100 * p['ci95'][0]:+.1f} to {100 * p['ci95'][1]:+.1f})."
                    ),
                    "",
                ]
        if "bench" in s:
            b = s["bench"]
            out += [
                "**The benchmark's own metrics.** Its policy expects the assistant to offer help nobody asked for, so a model that speaks only when spoken to misses many RESPOND lines by design.",
                "",
                "| Reading | Scenario pass rate | Macro F1 | False interruptions | Missed interventions | Turn accuracy |",
                "|---|---|---|---|---|---|",
            ]
            for name_, m in b.items():
                if isinstance(m, dict) and "scenario_pass_rate" in m:
                    out.append(
                        f"| {name_} | {_short(m['scenario_pass_rate'])} | {m['macro_f1']} | {_short(m['false_interruption_rate'])} | "
                        f"{_short(m['missed_intervention_rate'])} | {_short(m['turn_accuracy'])} |"
                    )
            for row in b.get("their_leaderboard_top") or []:
                out.append(
                    f"| *{row.get('model')}, from the benchmark's own leaderboard* | {100 * row.get('scenario_pass_rate', 0):.1f}% | | "
                    f"{100 * row.get('fir', 0):.1f}% | {100 * row.get('mir', 0):.1f}% | {100 * row.get('turn_accuracy', 0):.1f}% |"
                )
            out += [
                "",
                f"AUROC of `max(addressed, question)` against RESPOND: {b['auroc of max(addressed, question)']['value']}.",
                "",
            ]
        for tag, slices in (s.get("slices") or {}).items():
            out += _slice_table(tag, slices)
        sweep = s.get("threshold_sweep") or {}
        if any(v["answered_now"]["n"] for v in sweep.values()):
            out += [
                "**Moving the `addressed` threshold**",
                "",
                "| Threshold | For the agent: answers now | For others: answers now |",
                "|---|---|---|",
            ]
            out += [
                f"| {t} | {_short(v['answered_now'])} | {_short(v['answers_now_wrongly'])} |" for t, v in sweep.items()
            ]
            out.append("")
        if "lines" in s:
            wrong = [x for x in s["lines"] if x["expect"] and x["expect"] != x["jev"]]
            graded = [x for x in s["lines"] if not x["expect"]]
            out += [
                f"**Lines Jev decides differently from the label** ({len(wrong)} of {sum(1 for x in s['lines'] if x['expect'])})",
                "",
            ]
            if wrong:
                out += ["| Line | Kind | Expected | Jev | addressed | question |", "|---|---|---|---|---|---|"]
                out += [
                    f"| {x['speaker']}: {x['text'][:110].replace('|', '/')} | `{x['kind']}` | {x['expect']} | {x['jev']} | {x['addressed']:.2f} | {x['question']:.2f} |"
                    for x in wrong
                ]
                out.append("")
            if graded:
                out += [
                    f"**Graded lines, no single right decision** ({len(graded)})",
                    "",
                    "| Line | Kind | Jev | addressed | question |",
                    "|---|---|---|---|---|",
                ]
                out += [
                    f"| {x['speaker']}: {x['text'][:110].replace('|', '/')} | `{x['kind']}` | {x['jev']} | {x['addressed']:.2f} | {x['question']:.2f} |"
                    for x in graded
                ]
                out.append("")
    return "\n".join(out).rstrip() + "\n"
