"""Score one trained model against scorecard 0.1, item by item, from what is stored in R2.

    set -a; . ./.env; set +a
    uv run python scripts/scorecard_report.py side-r3-ettin-150m-s0 > docs/reports/<date>-<run_id>-scorecard.md

Reads the run's scoring (`runs/side/predictions/<run_id>/scorecard.json` and the per-set
predictions) and rebuilds the rows it needs locally. Prints Markdown. Every share has its count
and a 95% Wilson interval. No model is run and nothing is paid for.
"""

from __future__ import annotations

import sys
from collections.abc import Callable

from sidechat.guide import KINDS
from sidechat.lib import r2
from sidechat.lib.score import share
from sidechat.sources import build
from sidechat.train.evaluate import decide


def pct(x: dict | None) -> str:
    if not x or x.get("value") is None:
        return "n/a"
    lo, hi = x["ci95"]
    return f"{100 * x['value']:.1f}% ({x['k']:,}/{x['n']:,}; {100 * lo:.1f} to {100 * hi:.1f})"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    run_id = sys.argv[1]
    s3 = r2.client()
    card = r2.get_json(s3, f"runs/side/predictions/{run_id}/scorecard.json")
    if not card:
        print(f"{run_id}: no scoring in R2")
        return 1
    t, sets = card["thresholds"], card["sets"]

    def preds(name: str) -> dict:
        return {p["row_id"]: p for p in r2.get_jsonl(s3, f"runs/side/predictions/{run_id}/{name}.jsonl") or []}

    def rate(rows: list[dict], p: dict, keep: Callable[[dict], bool], outcome: str) -> dict:
        got = [decide(p[r["row_id"]], t) for r in rows if keep(r) and r["row_id"] in p]
        return share(sum(d == outcome for d in got), len(got))

    duplex = [r for r in build.build_rows("duplex")[0] if r["tags"].get("conflict") != "1"]
    dp = preds("duplex-mpe-0.1")
    pilot = build.build_rows("pilot-0.4@anonymous")[0]
    pp = preds("pilot-0.4@anonymous")

    main_a, main_n = sets["generated test @anonymous"], sets["generated test @named"]
    pilot_a, pilot_n = sets["pilot-0.4@anonymous"], sets["pilot-0.4"]
    dx, amb, demo, ami_s = (
        sets["duplex-mpe-0.1"],
        sets["ambient-bench-0.1"],
        sets["demo-lines-0.1"],
        sets["ami-silent-0.1.test"],
    )

    def ev(e: str, c: str | None = None):
        return lambda r: r["tags"]["event"] == e and (c is None or r["tags"]["condition"] == c)

    t_explicit = rate(duplex, dp, ev("T", "explicit"), "respond")
    t_implicit = rate(duplex, dp, ev("T", "implicit"), "respond")
    n1_now, n1_hold = rate(duplex, dp, ev("N1"), "respond"), rate(duplex, dp, ev("N1"), "wait")
    device = rate(duplex, dp, lambda r: r["label"]["to"] == "device", "respond")
    g6 = lambda r: (
        KINDS.get(r["tags"].get("kind", ""))
        and KINDS[r["tags"]["kind"]].rule == "G6"
        and r["label"]["expect"] == "respond"
    )
    pilot_g6 = rate(pilot, pp, g6, "respond")
    main_g6 = main_a["by_rule"].get("G6", {}).get("sidechat", {}).get("answered_now")
    waits = [pp[r["row_id"]]["respond"] for r in pilot if r["label"]["expect"] == "wait" and r["row_id"] in pp]
    pilot_wait_in = share(sum(0.25 <= x <= 0.75 for x in waits), len(waits))
    ec = main_a["even_call"]
    fu = main_a["by_kind"].get("follow_up", {}).get("sidechat", {}).get("decision_right")
    fbo = main_a["by_kind"].get("follow_up_by_other", {}).get("sidechat", {}).get("decision_right")
    held = main_a["by_heldout"]
    none_key = "" if "" in held else "none"  # the slice of lines with nothing held out
    none_right = held[none_key]["sidechat"]["decision_right"]["value"]
    worst = min(
        ((k, v["sidechat"]["decision_right"]) for k, v in held.items() if k != none_key),
        key=lambda kv: kv[1]["value"],
    )
    worst_jev = (held[worst[0]].get("jev") or {}).get("decision_right", {}).get("value")
    ami_per_1000 = 1000 * ami_s["sidechat"]["answers_now_wrongly"]["k"] / ami_s["sidechat"]["answers_now_wrongly"]["n"]
    jev_ami = ami_s.get("jev", {}).get("answers_now_wrongly", {})
    jev_ami_per_1000 = 1000 * jev_ami["k"] / jev_ami["n"] if jev_ami.get("n") else None

    def ok(b: bool | None) -> str:
        return "n/a" if b is None else ("met" if b else "**not met**")

    v = lambda x: (x or {}).get("value")
    rows = [
        (
            1,
            "Decision right, main test (anonymous)",
            f"{pct(main_a['sidechat']['decision_right'])}; on Jev's {main_a['sidechat_vs_jev']['n']:,} lines {100 * main_a['sidechat_vs_jev']['diff']:+.1f} points ({100 * main_a['sidechat_vs_jev']['ci95'][0]:+.1f} to {100 * main_a['sidechat_vs_jev']['ci95'][1]:+.1f})",
            f"Jev {pct(main_a['jev']['decision_right'])}",
            ok(main_a["sidechat_vs_jev"]["better_beyond_noise"]),
        ),
        (
            2,
            "Answers now a line for someone else",
            f"Duplex-MPE {pct(dx['sidechat']['answers_now_wrongly'])}; main test {pct(main_a['sidechat']['answers_now_wrongly'])}",
            "≤ 0.4% on Duplex-MPE, ≤ 1% on main test",
            ok(
                v(dx["sidechat"]["answers_now_wrongly"]) <= 0.004
                and v(main_a["sidechat"]["answers_now_wrongly"]) <= 0.01
            ),
        ),
        (
            3,
            "Holds for a pause on a line for someone else",
            f"Duplex-MPE {pct(dx['sidechat']['holds_wrongly'])}; Ambient {pct(amb['sidechat']['holds_wrongly'])}; pilot {pct(pilot_n['sidechat']['holds_wrongly'])}",
            "At most half of Jev's (16.0%, 14.6%, 17.8%)",
            ok(
                v(dx["sidechat"]["holds_wrongly"]) <= 0.08
                and v(amb["sidechat"]["holds_wrongly"]) <= 0.073
                and v(pilot_n["sidechat"]["holds_wrongly"]) <= 0.089
            ),
        ),
        (
            4,
            "Answers now a request that names the agent",
            f"Duplex-MPE explicit T {pct(t_explicit)}",
            "Not worse than Jev (99.2%)",
            ok(v(t_explicit) >= 0.992 - 0.004),
        ),
        (
            5,
            "Answers now the same request without the name",
            f"Duplex-MPE implicit T {pct(t_implicit)}",
            "Better than Jev (26.6%) beyond noise; aim for 80%",
            ok(t_implicit["ci95"][0] > 0.266) + (" (aim of 80% not met)" if v(t_implicit) < 0.8 else ""),
        ),
        (
            6,
            "Line for the agent from the rhythm, no name",
            f"pilot G6 lines {pct(pilot_g6)}; main test G6 {pct(main_g6)}",
            "≥ 90% answered now",
            ok(v(pilot_g6) >= 0.9 and v(main_g6) >= 0.9),
        ),
        (
            7,
            "Name said about the agent, not to it",
            f"Duplex-MPE N1: answers now {pct(n1_now)}, holds {pct(n1_hold)}",
            "Answers now ≤ 0.1%; holds ≤ 6.7%",
            ok(v(n1_now) <= 0.001 and v(n1_hold) <= 0.067),
        ),
        (
            8,
            "Another device addressed",
            f"Duplex-MPE device lines: answers now {pct(device)}",
            "≤ 0.5%",
            ok(v(device) <= 0.005),
        ),
        (
            9,
            "An open question with nothing to settle it",
            f"main test: mean `respond` {ec['mean_respond']:.2f}, {pct(ec['share_between_0.25_and_0.75'])} between 0.25 and 0.75; pilot: mean {sum(waits) / max(1, len(waits)):.2f}, {pct(pilot_wait_in)}",
            "Mean between 0.35 and 0.65, ≥ 80% between 0.25 and 0.75",
            ok(
                0.35 <= ec["mean_respond"] <= 0.65
                and v(ec["share_between_0.25_and_0.75"]) >= 0.8
                and v(pilot_wait_in) >= 0.8
            ),
        ),
        (
            10,
            "Calibration of `respond`",
            f"main test: calibration error {main_a['respond_calibration_error']['value']}, mean distance {main_a['respond_mean_abs_error']}; Duplex-MPE {dx['respond_calibration_error']['value']}; pilot {pilot_a['respond_calibration_error']['value']}",
            "≤ 0.05; mean distance ≤ 0.10",
            ok(main_a["respond_calibration_error"]["value"] <= 0.05 and main_a["respond_mean_abs_error"] <= 0.10),
        ),
        (
            11,
            "Follow-up by the partner against by someone else",
            f"main test: partner {pct(fu)}; someone else {pct(fbo)}",
            "≥ 90% each",
            ok(v(fu) >= 0.9 and v(fbo) >= 0.9),
        ),
        (
            12,
            "The demo's own lines",
            f"{demo['sidechat']['decision_right']['k']}/{demo['sidechat']['decision_right']['n']}",
            "≥ 46/48",
            ok(demo["sidechat"]["decision_right"]["k"] >= 46),
        ),
        (
            13,
            "Anonymous against named speakers",
            f"main test {100 * v(main_a['sidechat']['decision_right']):.1f}% against {100 * v(main_n['sidechat']['decision_right']):.1f}%; pilot {100 * v(pilot_a['sidechat']['decision_right']):.1f}% against {100 * v(pilot_n['sidechat']['decision_right']):.1f}%",
            "Gap ≤ 2 points",
            ok(
                abs(v(main_a["sidechat"]["decision_right"]) - v(main_n["sidechat"]["decision_right"])) <= 0.02
                and abs(v(pilot_a["sidechat"]["decision_right"]) - v(pilot_n["sidechat"]["decision_right"])) <= 0.02
            ),
        ),
        (
            14,
            "Unseen writer, settings and agent names",
            f"weakest held-out slice `{worst[0]}` {pct(worst[1])} (Jev {100 * (worst_jev or 0):.1f}%); nothing held out {100 * none_right:.1f}%",
            "≥ Jev on each, gap to main test ≤ 5 points",
            ok(
                none_right - worst[1]["value"] <= 0.05
                and all(
                    v["sidechat"]["decision_right"]["value"]
                    >= (v.get("jev") or {}).get("decision_right", {}).get("value", 0)
                    for v in held.values()
                )
            ),
        ),
        (15, "Real speech-to-text against clean text", "not built yet", "Gap ≤ 3 points, ≥ Jev", "n/a"),
        (
            16,
            "AMI meetings with a silent agent: answers per 1,000 lines",
            f"{ami_per_1000:.1f} ({ami_s['sidechat']['answers_now_wrongly']['k']}/{ami_s['sidechat']['answers_now_wrongly']['n']:,}); holds {pct(ami_s['sidechat']['holds_wrongly'])}",
            f"≤ Jev ({jev_ami_per_1000:.1f})" if jev_ami_per_1000 is not None else "≤ Jev",
            ok(jev_ami_per_1000 is not None and ami_per_1000 <= jev_ami_per_1000),
        ),
    ]
    print(f"# Scorecard 0.1: `{run_id}`\n")
    print(
        f"Encoder {card['config']['encoder']}, input {card['config']['input_version']}. Thresholds chosen on dev: "
        f"answer now at `respond` ≥ {t['respond']}, hold at `respond` ≥ {t['wait']} or `intent.open` ≥ {t['open']}. "
        "Speakers anonymous unless the item says otherwise. Shares are `value (k/n; 95% interval)`. "
        "Built by `scripts/scorecard_report.py` from the run's stored scoring.\n"
    )
    print("| # | Item | Sidechat | Target | |")
    print("|---|---|---|---|---|")
    for n, item, got, target, verdict in rows:
        print(f"| {n} | {item} | {got} | {target} | {verdict} |")
    met = [str(r[0]) for r in rows if r[4].startswith("met")]
    missed = [str(r[0]) for r in rows if "not met" in r[4] and not r[4].startswith("met")]
    print(f"\n{len(met)} of {len(rows)} items met. Not met: {', '.join(missed) or 'none'}. Item 15 is not built.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
