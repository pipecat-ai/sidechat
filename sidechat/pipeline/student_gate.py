"""The numbers a student round compares and the gate a student must pass to ship for agent-1x
(no Modal or torch here, so it is testable anywhere). Used by `sidechat.pipeline.round7`."""

from __future__ import annotations

JEV_IMPLICIT_T = 0.266  # Jev's share of Duplex-MPE's unnamed requests answered, if a card lacks it


def metrics(card: dict) -> dict:
    """The numbers the summary compares, from a run's stored scorecard."""
    sets = card.get("sets") or {}

    def get(name: str, key: str, sub: str | None = None, who: str = "sidechat") -> dict | None:
        s = sets.get(name) or {}
        s = ((s.get("by_condition_event") or {}).get(sub) or {}) if sub else s
        return (s.get(who) or {}).get(key)

    return {
        "generated": get("generated test @anonymous", "decision_right"),
        "duplex": get("duplex-mpe-0.1", "decision_right"),
        "duplex_outright": get("duplex-mpe-0.1", "answers_now_wrongly"),
        "duplex_held": get("duplex-mpe-0.1", "holds_wrongly"),
        "explicit_t": get("duplex-mpe-0.1", "answered_now", "explicit/T"),
        "implicit_t": get("duplex-mpe-0.1", "answered_now", "implicit/T"),
        "implicit_held": get("duplex-mpe-0.1", "held_instead", "implicit/T"),
        "jev_implicit_t": get("duplex-mpe-0.1", "answered_now", "implicit/T", who="jev"),
        "ambient": get("ambient-bench-0.1", "decision_right"),
        "ami": get("ami-addressee-0.1", "decision_right"),
        "ami_silent_outright": get("ami-silent-0.1.test", "answers_now_wrongly"),
        "pilot": get("pilot-0.4@anonymous", "decision_right"),
        "demo": get("demo-lines-0.1", "decision_right"),
    }


def pct(x: dict | None, digits: int = 1) -> str:
    if not x or x.get("value") is None:
        return "n/a"
    return f"{100 * x['value']:.{digits}f}% ({x['k']:,}/{x['n']:,})"


def gate_one(
    m: dict, t: dict, full_ms: float | None, jev_ms: float | None, jev_implicit: float, parity_ok: bool
) -> dict:
    """The gate for one student `m` against the teacher `t`."""
    checks = []
    for key, label in (("duplex", "Duplex-MPE"), ("ami", "AMI"), ("pilot", "pilot"), ("explicit_t", "named requests")):
        if m.get(key) and t.get(key):
            d = 100 * (m[key]["value"] - t[key]["value"])
            checks.append((d >= -1.0, f"{label} {d:+.1f} points against the teacher"))
        else:
            checks.append((False, f"{label} not scored"))
    if m.get("implicit_t"):
        v = m["implicit_t"]["value"]
        checks.append((v > jev_implicit, f"unnamed requests {100 * v:.1f}% answered (Jev {100 * jev_implicit:.1f}%)"))
    else:
        checks.append((False, "unnamed requests not scored"))
    if full_ms is not None and jev_ms is not None:
        checks.append((full_ms < jev_ms, f"full history {full_ms:.0f} ms on agent-1x (Jev {jev_ms:.0f})"))
    else:
        checks.append((False, "not timed"))
    if not parity_ok:
        checks.append((False, "export parity failed"))
    return {
        "ships": all(ok for ok, _ in checks),
        "why": "; ".join(("" if ok else "**fails:** ") + w for ok, w in checks),
    }


SLURP_SETS = {"written": "slurp-in-ami-0.1", "heard": "slurp-in-ami-stt-0.1", "keyterm": "slurp-in-ami-stt-keyterm-0.1"}
NAMED_KINDS = ("name_first", "name_mid", "name_last")


def _sum_kinds(card: dict, kinds: tuple[str, ...], key: str, who: str = "sidechat") -> dict | None:
    parts = [(((card.get("by_kind") or {}).get(k) or {}).get(who) or {}).get(key) for k in kinds]
    parts = [p for p in parts if p and p.get("n")]
    if not parts:
        return None
    k, n = sum(p["k"] for p in parts), sum(p["n"] for p in parts)
    return {"value": k / n, "k": k, "n": n}


def metrics_r8(card: dict, who: str = "sidechat") -> dict:
    """`metrics` plus real speech: AMI as heard, and SLURP's requests in AMI meetings (named answered
    now, unnamed held) as written, heard, and heard with the name as a keyterm. `who` "jev" reads
    Jev's numbers from the same cards."""
    sets = card.get("sets") or {}

    def get(name: str, key: str, sub: str | None = None) -> dict | None:
        s = sets.get(name) or {}
        s = ((s.get("by_condition_event") or {}).get(sub) or {}) if sub else s
        return (s.get(who) or {}).get(key)

    out = metrics(card) if who == "sidechat" else {}
    if who != "sidechat":
        for key, name, k in (
            ("duplex", "duplex-mpe-0.1", "decision_right"),
            ("duplex_outright", "duplex-mpe-0.1", "answers_now_wrongly"),
            ("duplex_held", "duplex-mpe-0.1", "holds_wrongly"),
            ("ambient", "ambient-bench-0.1", "decision_right"),
            ("ami", "ami-addressee-0.1", "decision_right"),
            ("pilot", "pilot-0.4@anonymous", "decision_right"),
        ):
            out[key] = get(name, k)
        out["explicit_t"] = get("duplex-mpe-0.1", "answered_now", "explicit/T")
        out["implicit_t"] = get("duplex-mpe-0.1", "answered_now", "implicit/T")
        out["implicit_held"] = get("duplex-mpe-0.1", "held_instead", "implicit/T")
    out["ami_heard_held"] = get("ami-addressee-stt-0.1", "holds_wrongly")
    out["ami_heard_outright"] = get("ami-addressee-stt-0.1", "answers_now_wrongly")
    for label, rows_id in SLURP_SETS.items():
        c = sets.get(rows_id) or {}
        out[f"slurp_named_{label}"] = _sum_kinds(c, NAMED_KINDS, "answered_now", who)
        out[f"slurp_unnamed_held_{label}"] = _sum_kinds(c, ("open_request",), "open_held", who)
        out[f"slurp_unnamed_answered_{label}"] = _sum_kinds(c, ("open_request",), "open_answered_now", who)
    return out


def gate_default(m: dict, base: dict) -> dict:
    """A new default build against the released one (`base`): unnamed requests held more often as
    heard, beyond noise, and nothing else worse beyond a small margin."""
    checks = []

    def cmp(key: str, label: str, margin: float, higher_is_better: bool = True) -> None:
        a, b = m.get(key), base.get(key)
        if not a or not b or a.get("value") is None or b.get("value") is None:
            checks.append((False, f"{label} not scored"))
            return
        d = 100 * (a["value"] - b["value"])
        ok = d >= -margin if higher_is_better else d <= margin
        checks.append((ok, f"{label} {d:+.2f} points"))

    u, ub = m.get("slurp_unnamed_held_heard"), base.get("slurp_unnamed_held_heard")
    if u and ub and u.get("n") and ub.get("n"):
        from sidechat.lib.score import wilson

        lo = wilson(u["k"], u["n"])[0]
        hi = wilson(ub["k"], ub["n"])[1]
        checks.append(
            (lo > hi, f"unnamed requests held as heard {100 * u['value']:.1f}% (was {100 * ub['value']:.1f}%)")
        )
    else:
        checks.append((False, "unnamed requests as heard not scored"))
    for key, label, margin in (
        ("duplex", "Duplex-MPE right", 0.5),
        ("ambient", "Ambient Bench right", 0.5),
        ("ami", "AMI right", 0.5),
        ("generated", "generated test right", 0.5),
        ("pilot", "pilot right", 1.0),
        ("explicit_t", "named requests answered", 1.0),
        ("slurp_named_keyterm", "SLURP named answered (keyterm)", 5.0),
    ):
        cmp(key, label, margin)
    for key, label, margin in (
        ("duplex_outright", "Duplex-MPE others answered outright", 0.1),
        ("duplex_held", "Duplex-MPE others held", 1.0),
        ("ami_heard_held", "AMI as heard, held", 1.0),
    ):
        cmp(key, label, margin, higher_is_better=False)
    o = m.get("duplex_outright")
    if o and o.get("value") is not None:
        checks.append((o["value"] <= 0.004, f"Duplex-MPE others answered outright {100 * o['value']:.2f}% (bar 0.4%)"))
    return {
        "ships": all(ok for ok, _ in checks),
        "why": "; ".join(("" if ok else "**fails:** ") + w for ok, w in checks),
    }


TCL_SET = "tcl-wakeup-0.1@anonymous"
GEN05_SET = "gen-0.5.test@anonymous"


def metrics_r10(card: dict, who: str = "sidechat") -> dict:
    """`metrics_r8` plus round 10's targets: TCL's independent test (SD-27; read for the report and
    the gate, never for picks) and gen-0.5's new kinds on its test split."""
    out = metrics_r8(card, who)
    sets = card.get("sets") or {}
    tcl = sets.get(TCL_SET) or {}
    by = tcl.get("by_kind") or {}

    def k(kind: str, key: str) -> dict | None:
        return ((by.get(kind) or {}).get(who) or {}).get(key)

    out["tcl_outright"] = (tcl.get(who) or {}).get("answers_now_wrongly")
    out["tcl_held"] = (tcl.get(who) or {}).get("holds_wrongly")
    out["tcl_direct"] = k("direct", "answered_now")
    out["tcl_ctx_now"] = k("contextual", "answered_now")
    out["tcl_ctx_held"] = k("contextual", "held_instead")
    g5 = sets.get(GEN05_SET) or {}
    out["g5_pq"] = _sum_kinds(g5, ("people_question_after_agent",), "quiet_kept", who)
    out["g5_pp"] = _sum_kinds(g5, ("partner_to_people_after_agent",), "quiet_kept", who)
    out["g5_later"] = _sum_kinds(g5, ("follow_up_later",), "open_held", who)
    out["g5_follow_up"] = _sum_kinds(g5, ("follow_up",), "answered_now", who)
    return out


def tcl_paired(new: dict[str, str], base: dict[str, str], rows: list[dict]) -> dict:
    """Paired comparisons on TCL's test, from each model's decisions (row_id -> respond, wait or
    ignore): people's lines answered outright, and unnamed follow-ups answered or held."""
    from sidechat.lib.score import paired

    others = [r["row_id"] for r in rows if r["tags"]["kind"] not in ("direct", "contextual")]
    ctx = [r["row_id"] for r in rows if r["tags"]["kind"] == "contextual"]
    both = [i for i in others if i in new and i in base]
    cb = [i for i in ctx if i in new and i in base]
    return {
        # "right" is not answering outright, so a positive difference is fewer outright answers
        "others_not_outright": paired([base[i] != "respond" for i in both], [new[i] != "respond" for i in both]),
        "ctx_now_or_held": paired([base[i] != "ignore" for i in cb], [new[i] != "ignore" for i in cb]),
    }


def gate_r10(m: dict, base: dict, tcl: dict | None) -> dict:
    """Round 10's gate, fixed before training (exp-066): a new build against rc0.3's (`base`).
    It must answer fewer of TCL's people's lines outright, beyond noise (paired), hold on to unnamed
    follow-ups there and to round 9's real unnamed requests, and keep everything else within a
    small margin."""
    checks = []

    def cmp(key: str, label: str, margin: float, higher_is_better: bool = True) -> None:
        a, b = m.get(key), base.get(key)
        if not a or not b or a.get("value") is None or b.get("value") is None:
            checks.append((False, f"{label} not scored"))
            return
        d = 100 * (a["value"] - b["value"])
        ok = d >= -margin if higher_is_better else d <= margin
        checks.append((ok, f"{label} {d:+.2f} points"))

    o = (tcl or {}).get("others_not_outright") or {}
    if o.get("diff") is not None:
        lo, hi = o["ci95"]
        why = f"TCL people's lines answered outright {-100 * o['diff']:+.2f} points, paired"
        checks.append((lo > 0, f"{why} ({-100 * hi:+.2f} to {-100 * lo:+.2f})"))
    else:
        checks.append((False, "TCL not scored"))
    c = (tcl or {}).get("ctx_now_or_held") or {}
    if c.get("diff") is not None:
        checks.append(
            (100 * c["diff"] >= -5.0, f"TCL unnamed follow-ups answered or held {100 * c['diff']:+.2f} points")
        )
    for key, label, margin in (
        ("tcl_direct", "TCL named requests answered", 1.0),
        ("slurp_unnamed_held_heard", "real unnamed requests held as heard", 3.0),
        ("duplex", "Duplex-MPE right", 0.5),
        ("ambient", "Ambient Bench right", 0.5),
        ("ami", "AMI right", 0.5),
        ("generated", "generated test right", 0.5),
        ("pilot", "pilot right", 1.0),
        ("explicit_t", "named requests answered", 1.0),
        ("slurp_named_keyterm", "SLURP named answered (keyterm)", 5.0),
    ):
        cmp(key, label, margin)
    for key, label, margin in (
        ("duplex_outright", "Duplex-MPE others answered outright", 0.1),
        ("duplex_held", "Duplex-MPE others held", 1.0),
        ("ami_heard_held", "AMI as heard, held", 1.0),
        ("tcl_held", "TCL people's lines held", 1.0),
    ):
        cmp(key, label, margin, higher_is_better=False)
    d = m.get("duplex_outright")
    if d and d.get("value") is not None:
        checks.append((d["value"] <= 0.004, f"Duplex-MPE others answered outright {100 * d['value']:.2f}% (bar 0.4%)"))
    return {
        "ships": all(ok for ok, _ in checks),
        "why": "; ".join(("" if ok else "**fails:** ") + w for ok, w in checks),
    }
