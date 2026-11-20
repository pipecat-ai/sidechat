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
