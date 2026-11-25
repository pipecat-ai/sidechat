"""The training run's report: each model against Jev on every set, in plain tables."""

from __future__ import annotations


def _pct(s: dict | None, ci: bool = False) -> str:
    if not s or s.get("value") is None:
        return "n/a"
    base = f"{100 * s['value']:.1f}% ({s['k']}/{s['n']}"
    return base + (f"; {100 * s['ci95'][0]:.1f} to {100 * s['ci95'][1]:.1f})" if ci else ")")


def _diff(p: dict | None) -> str:
    if not p or p.get("diff") is None:
        return "n/a"
    lo, hi = p["ci95"]
    verdict = "better" if p.get("better_beyond_noise") else "worse" if p.get("worse_beyond_noise") else "within noise"
    return f"{100 * p['diff']:+.1f} ({100 * lo:+.1f} to {100 * hi:+.1f}), {verdict}"


HEAD = (
    "| Set | System | Decision right | For others: answers now | For others: holds | For the agent: answers now | "
    "For the agent: missed | Even calls: mean `respond` |"
)
SEP = "|---|---|---|---|---|---|---|---|"


def _row(name: str, who: str, m: dict, even: dict | None = None) -> str:
    e = f"{even['mean_respond']:.2f} (n={even['n']})" if even else ""
    return (
        f"| {name} | {who} | {_pct(m['decision_right'], True)} | {_pct(m['answers_now_wrongly'])} | {_pct(m['holds_wrongly'])} | "
        f"{_pct(m['answered_now'])} | {_pct(m['missed'])} | {e} |"
    )


def model_section(name: str, trained: dict, card: dict) -> list[str]:
    t = card["thresholds"]
    out = [
        f"## {name}",
        "",
        (
            f"Run `{card['run_id']}`. Best epoch {trained.get('best_epoch')} of {len(trained.get('history', []))}; "
            f"history {trained.get('history')}. Temperatures {trained.get('temperatures')}. "
            f"{trained.get('train_rows')} training rows, {trained.get('dev_rows')} dev rows, {trained.get('secs')} s."
        ),
        "",
        (
            f"Thresholds chosen on dev (anonymous): answer now at `respond` ≥ {t['respond']}, hold at `respond` ≥ {t['wait']} "
            f"or `intent.open` ≥ {t['open']} ({t['dev_right']}/{t['dev_n']} dev decisions right)."
        ),
        "",
        HEAD,
        SEP,
    ]
    for set_name, s in card["sets"].items():
        out.append(_row(set_name, "Sidechat", s["sidechat"], s.get("even_call")))
        if "jev" in s:
            out.append(_row("", "Jev", s["jev"]))
    out += ["", "**Sidechat against Jev, decision right, same lines** (points, 95% interval)", ""]
    for set_name, s in card["sets"].items():
        if "sidechat_vs_jev" in s:
            out.append(f"- {set_name}: {_diff(s['sidechat_vs_jev'])} on {s['sidechat_vs_jev']['n']} lines")
    out += ["", "**Calibration and ranking**", ""]
    for set_name, s in card["sets"].items():
        bits = []
        if "respond_calibration_error" in s:
            bits.append(f"calibration error {s['respond_calibration_error']['value']}")
        if "respond_mean_abs_error" in s:
            bits.append(f"mean distance to target {s['respond_mean_abs_error']}")
        if "respond_auroc_for_agent" in s and s["respond_auroc_for_agent"].get("value") is not None:
            bits.append(f"AUROC {s['respond_auroc_for_agent']['value']}")
        if bits:
            out.append(f"- {set_name}: " + ", ".join(bits))
    anon = card["sets"].get("generated test @anonymous", {})
    for key, title in (
        ("by_writer", "writer (b is held out)"),
        ("by_heldout", "held-out reason"),
        ("by_rule", "guide rule"),
    ):
        if anon.get(key):
            out += [
                "",
                f"**Generated test, anonymous, by {title}**",
                "",
                "| Slice | Decision right | For others: answers now | For the agent: answers now |",
                "|---|---|---|---|",
            ]
            for k, s in anon[key].items():
                m = s["sidechat"]
                out.append(
                    f"| `{k or 'none'}` | {_pct(m['decision_right'])} | {_pct(m['answers_now_wrongly'])} | {_pct(m['answered_now'])} |"
                )
    dup = next((s for k, s in card["sets"].items() if k.startswith("duplex")), None)
    if dup and dup.get("by_condition_event"):
        out += [
            "",
            "**Duplex-MPE by condition and event**",
            "",
            "| Slice | Sidechat right | Jev right | Sidechat answers now | Jev answers now |",
            "|---|---|---|---|---|",
        ]
        for k, s in dup["by_condition_event"].items():
            j = s.get("jev", {})
            out.append(
                f"| `{k}` | {_pct(s['sidechat']['decision_right'])} | {_pct(j.get('decision_right'))} | "
                f"{_pct(s['sidechat']['answered_now'])} | {_pct(j.get('answered_now'))} |"
            )
    return out + [""]


def render(exp: str, trained: dict, scored: dict) -> str:
    out = [
        f"# Training run: {exp}",
        "",
        (
            "Every number below is measured in this run. A share is `value (k/n)`; "
            "headline shares also give a 95% interval."
        ),
        "",
    ]
    for name, card in scored.items():
        if "error" in card:
            out += [f"## {name}", "", f"Scoring failed: {card['error']}", ""]
            continue
        out += model_section(name, trained.get(name, {}), card)
    for name, t in trained.items():
        if "error" in t:
            out += [f"## {name}", "", f"Training failed: {t['error']}", ""]
    return "\n".join(out).rstrip() + "\n"
