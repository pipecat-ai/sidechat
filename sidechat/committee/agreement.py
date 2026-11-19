"""How far the committee agrees with the guide's labels, and with itself.

The target for Phase 1 (PLAN.md section 9): the committee's majority decision agrees with the
guide on at least 90% of the lines that have a definite decision. Lines the guide leaves graded
(either decision reasonable) are reported separately.
"""

from __future__ import annotations

from collections import defaultdict
from itertools import combinations

from sidechat.guide import KINDS
from sidechat.lib.score import share

TARGET = 0.90


def _guide(row: dict) -> dict:
    lab = row["label"]
    kind = row["tags"].get("kind", "")
    return {
        "expect": lab["expect"],
        "intent": lab["intent"],
        "to_agent": lab["to"] == "agent" if lab["to"] != "unknown" else None,
        "rule": row["tags"].get("rule") or (KINDS[kind].rule if kind in KINDS else None),
        "speak": 1 + 4 * lab["respond"] if lab["respond"] is not None else None,
        "kind": kind,
    }


def build(rows: list[dict], answers: dict[str, dict[str, dict | None]], votes: dict[str, dict], meta: dict) -> dict:
    members = sorted(answers)
    guide = {r["row_id"]: _guide(r) for r in rows}
    definite = [r for r in rows if guide[r["row_id"]]["expect"]]
    graded = [r for r in rows if not guide[r["row_id"]]["expect"]]

    def agree_decision(get) -> dict:
        ok = sum(1 for r in definite if get(r["row_id"]) == guide[r["row_id"]]["expect"])
        return share(ok, len(definite))

    card: dict = {"meta": meta, "rows": len(rows), "definite": len(definite), "graded": len(graded), "target": TARGET}

    # The majority.
    maj = {i: v.get("decision") for i, v in votes.items()}
    card["majority"] = {
        "decision": agree_decision(lambda i: maj.get(i)),
        "no_decision_majority": sum(1 for r in rows if votes[r["row_id"]].get("decision") is None),
        "intent": share(
            sum(
                1
                for r in rows
                if guide[r["row_id"]]["intent"] and votes[r["row_id"]].get("intent") == guide[r["row_id"]]["intent"]
            ),
            sum(1 for r in rows if guide[r["row_id"]]["intent"]),
        ),
        "unanimous": share(sum(1 for r in rows if votes[r["row_id"]].get("unanimous")), len(rows)),
    }
    card["meets_target"] = (card["majority"]["decision"]["value"] or 0) >= TARGET

    # Each member.
    card["members"] = {}
    for m in members:
        got = answers[m]
        answered = [r for r in rows if got.get(r["row_id"])]
        speak_diffs = [
            abs(got[r["row_id"]]["speak"] - guide[r["row_id"]]["speak"])
            for r in answered
            if guide[r["row_id"]]["speak"] is not None
        ]
        to_rows = [r for r in answered if guide[r["row_id"]]["to_agent"] is not None]
        card["members"][m] = {
            "answered": share(len(answered), len(rows)),
            "decision": agree_decision(lambda i, g=got: (g.get(i) or {}).get("decision")),
            "intent": share(
                sum(
                    1
                    for r in answered
                    if guide[r["row_id"]]["intent"] and got[r["row_id"]]["intent"] == guide[r["row_id"]]["intent"]
                ),
                sum(1 for r in answered if guide[r["row_id"]]["intent"]),
            ),
            "for_the_agent": share(
                sum(1 for r in to_rows if (got[r["row_id"]]["to"] == "agent") == guide[r["row_id"]]["to_agent"]),
                len(to_rows),
            ),
            "rule": share(
                sum(1 for r in answered if got[r["row_id"]]["rule"] == guide[r["row_id"]]["rule"]), len(answered)
            ),
            "speak_mean_abs_diff": round(sum(speak_diffs) / len(speak_diffs), 3) if speak_diffs else None,
        }
    card["pairs"] = {
        f"{a}-{b}": share(
            sum(
                1
                for r in rows
                if answers[a].get(r["row_id"])
                and answers[b].get(r["row_id"])
                and answers[a][r["row_id"]]["decision"] == answers[b][r["row_id"]]["decision"]
            ),
            sum(1 for r in rows if answers[a].get(r["row_id"]) and answers[b].get(r["row_id"])),
        )
        for a, b in combinations(members, 2)
    }

    # Slices.
    def sliced(key) -> dict:
        groups: dict[str, list[dict]] = defaultdict(list)
        for r in definite:
            groups[key(r)].append(r)
        return {
            k: share(sum(1 for r in g if maj.get(r["row_id"]) == guide[r["row_id"]]["expect"]), len(g))
            for k, g in sorted(groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        }

    card["by_rule"] = sliced(lambda r: guide[r["row_id"]]["rule"] or "?")
    card["by_expect"] = sliced(lambda r: guide[r["row_id"]]["expect"])
    card["by_kind"] = sliced(lambda r: guide[r["row_id"]]["kind"])

    def detail(r: dict) -> dict:
        g = guide[r["row_id"]]
        return {
            "id": r["row_id"].split("/", 1)[1],
            "speaker": r["request"]["speaker"],
            "text": r["request"]["text"],
            "before": [
                ("agent" if t["agent"] else t["speaker"]) + ": " + t["text"] for t in r["request"]["history"][-2:]
            ],
            "kind": g["kind"],
            "rule": g["rule"],
            "guide": g["expect"],
            "majority": maj.get(r["row_id"]),
            "members": {
                m: {
                    k: (answers[m].get(r["row_id"]) or {}).get(k)
                    for k in ("decision", "intent", "speak", "rule", "reason")
                }
                for m in members
            },
        }

    card["disagreements"] = [detail(r) for r in definite if maj.get(r["row_id"]) != guide[r["row_id"]]["expect"]]
    card["graded_lines"] = [detail(r) for r in graded]
    return card


# ---------------------------------------------------------------------------------------------


def _pct(s: dict | None, interval: bool = True) -> str:
    if not s or s.get("value") is None:
        return "n/a"
    base = f"{100 * s['value']:.1f}% ({s['k']}/{s['n']}"
    return base + (f"; {100 * s['ci95'][0]:.1f} to {100 * s['ci95'][1]:.1f})" if interval else ")")


def _cell(text: str, n: int = 110) -> str:
    text = text.replace("|", "/").replace("\n", " ")
    return text if len(text) <= n else text[: n - 1] + "…"


def render(card: dict) -> str:
    meta = card["meta"]
    maj = card["majority"]
    out = [
        f"# Committee pilot: {meta['exp']}",
        "",
        f"Generated {meta['finished_at']} by `sidechat/pipeline/label.py`. Every number below is measured in this run.",
        "",
        "## What was run",
        "",
        f"- **Lines:** {card['rows']} from `{', '.join(meta['sets'])}`, {card['definite']} with a definite decision in the guide and {card['graded']} graded.",
        f"- **Guide:** `{meta['guide']}`, prompt hash `{meta['prompt_sha']}`.",
        f"- **Members:** {', '.join(meta['members'])}, one model family each, at low reasoning effort. Model ids are configuration, not named here (SD-09).",
        f"- **Label set:** `{meta['label_id']}` in R2.",
        "",
        "## Agreement with the guide",
        "",
        f"**Majority decision: {_pct(maj['decision'])}.** Target {100 * card['target']:.0f}%: "
        + ("met." if card["meets_target"] else "**not met**.")
        + f" No majority on the decision for {maj['no_decision_majority']} lines.",
        "",
        "| | Decision | Intent | For the agent or not | Rule | Mean distance on `speak` |",
        "|---|---|---|---|---|---|",
        f"| Majority | {_pct(maj['decision'])} | {_pct(maj['intent'])} | | | |",
    ]
    for m, s in card["members"].items():
        out.append(
            f"| Member {m} | {_pct(s['decision'])} | {_pct(s['intent'])} | {_pct(s['for_the_agent'])} | {_pct(s['rule'])} | {s['speak_mean_abs_diff']} |"
        )
    out += [
        "",
        "Members agreeing with each other on the decision: "
        + ", ".join(f"{k} {_pct(v, False)}" for k, v in card["pairs"].items())
        + f". All three give the same decision and intent on {_pct(maj['unanimous'], False)} of lines.",
        "",
        "**By the guide's decision**",
        "",
        "| Guide says | Majority agrees |",
        "|---|---|",
        *[f"| {k} | {_pct(v)} |" for k, v in card["by_expect"].items()],
        "",
        "**By rule**",
        "",
        "| Rule | Majority agrees |",
        "|---|---|",
        *[f"| {k} | {_pct(v)} |" for k, v in card["by_rule"].items()],
        "",
        "**Kinds under 100%**",
        "",
        "| Kind | Majority agrees |",
        "|---|---|",
        *[
            f"| `{k}` | {_pct(v, False)} |"
            for k, v in card["by_kind"].items()
            if v["value"] is not None and v["value"] < 1
        ],
        "",
        f"## Lines where the majority differs from the guide ({len(card['disagreements'])})",
        "",
    ]
    for d in card["disagreements"]:
        out.append(
            f"**{d['id']}** `{d['kind']}` ({d['rule']}): guide **{d['guide']}**, majority **{d['majority'] or 'none'}**"
        )
        for b in d["before"]:
            out.append(f"> {_cell(b, 160)}")
        out.append(f"> **{d['speaker']}: {_cell(d['text'], 200)}**")
        out.append("")
        for m, a in d["members"].items():
            out.append(
                f"- {m}: {a['decision']} / {a['intent']} / speak {a['speak']} / {a['rule']}: {_cell(a['reason'] or '', 220)}"
            )
        out.append("")
    out += [
        f"## Graded lines ({len(card['graded_lines'])})",
        "",
        "| Line | Kind | a | b | c |",
        "|---|---|---|---|---|",
    ]
    for d in card["graded_lines"]:
        cells = [f"{a['decision']} {a['speak']}" if a["decision"] else "n/a" for a in d["members"].values()]
        out.append(f"| {d['speaker']}: {_cell(d['text'], 90)} | `{d['kind']}` | " + " | ".join(cells) + " |")
    out += [
        "",
        "## Calls and cost",
        "",
        "| Member | Answered | Failed | Not by the configured model | Input tokens | Cached | Output tokens | Est. cost |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for m, u in meta["usage"].items():
        out.append(
            f"| {m} | {u['answered']} | {u['failed']} | {u.get('fallback', 0)} | {u['input']:,} | {u['cached']:,} | {u['output']:,} | ${u['usd']:.2f} |"
        )
    errors = {m: u.get("errors") for m, u in meta["usage"].items() if u.get("errors")}
    if errors:
        out += ["", "Failures, first few per member:", ""]
        out += [f"- {m}: {_cell(e, 240)}" for m, es in errors.items() for e in es[:3]]
    return "\n".join(out).rstrip() + "\n"
