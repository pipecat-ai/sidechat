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
