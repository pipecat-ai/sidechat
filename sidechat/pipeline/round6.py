"""Round 6 and the agent-1x students, end to end in one detached Modal job.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.round6::run --exp exp-042-side-round6

Check on it, or read the summary once it is done, from any machine with the `.env`:

    uv run python -m sidechat.pipeline.results exp-042-side-round6

It chains the steps that otherwise need someone to start each one, so nothing depends on the
machine that launched it. Each step is its own experiment with its own report in R2 (records in
`experiments/`):

    committee  the committee on gen-0.4's new kinds (exp-037), beside
    r6         round 6: Ettin-150M on round 3's corpus plus gen-0.4, seeds 0 and 1 (exp-038, exp-039)
    teacher    the round 6 seed with more dev decisions right (dev only, never a benchmark)
    students   distilled from the teacher over round 6's corpus plus gen-0.3: two-tower Ettin-32M and
               68M (exp-048), and Ettin-32M on at most 4 earlier lines in 160 tokens (exp-049). A new
               kind the committee agrees with on under 90% is left out of their corpus
    export     the teacher and the students: ONNX, transformer optimizer, int8 gate (exp-043 to 046)
    latency    on agent-1x and agent-2x beside Jev, one thread (exp-047)
    summary    runs/side/results/<exp>/report.md: every model on the benchmarks, and the gate (a
               student ships only if its full-history median on agent-1x beats Jev's there, and it is
               within a point of the teacher on Duplex-MPE, AMI and the pilot)

`steps` runs a subset, in order (e.g. `students,export,latency` with `--teacher side-r3-ettin-150m-s0`).
"""

from __future__ import annotations

import modal

from sidechat.pipeline import export as X
from sidechat.pipeline import label as L
from sidechat.pipeline import latency as LT
from sidechat.pipeline import train as T

APP_NAME = "waystone-side-round6"
app = modal.App(APP_NAME)
for other in (T.app, L.app, X.app, LT.app):
    app.include(other)

CORPUS = "gen-0.1,gen-pilot,gen-0.2,gen-0.4,ami-silent"
STUDENT_CORPUS = "gen-0.1,gen-pilot,gen-0.2,gen-0.3,gen-0.4,ami-silent"
TEST = {"test_corpus": "gen-0.1,gen-pilot", "extra_sets": "corpus:gen-0.2:test@anonymous,corpus:gen-0.4:test@anonymous"}
NEW_KINDS = ("follow_up_after_reaction", "relay_agent_answer")
COMMITTEE_SETS = (
    "corpus:gen-0.4:dev+test:120:follow_up_after_reaction,"
    "corpus:gen-0.4:dev+test:120:relay_agent_answer,"
    "corpus:gen-0.4:dev+test:90:command_no_name+reply_then_request"
)
REFERENCE = "side-r3-ettin-150m-s0"
EXP = {
    "committee": "exp-037-side-committee-gen-0.4",
    "r6": ["exp-038-side-train-r6", "exp-039-side-train-r6-s1"],
    "tt": "exp-048-side-train-r6-tt",
    "short": "exp-049-side-train-r6-short",
    "latency": "exp-047-side-latency-r6",
}
STUDENTS = {
    "side-r6tt-ettin-32m-s0": "two towers, Ettin-32M",
    "side-r6tt-ettin-68m-s0": "two towers, Ettin-68M",
    "side-r6s-ettin-32m-s0": "one tower, Ettin-32M, 4 earlier lines",
}
EXPORTS = {  # run id -> export experiment
    "teacher": "exp-043-side-export-r6",
    "side-r6tt-ettin-32m-s0": "exp-044-side-export-r6tt-32m",
    "side-r6tt-ettin-68m-s0": "exp-045-side-export-r6tt-68m",
    "side-r6s-ettin-32m-s0": "exp-046-side-export-r6s-32m",
}


def _metrics(card: dict) -> dict:
    """The numbers the summary compares, from a run's stored scorecard."""
    sets = card.get("sets") or {}

    def get(name: str, key: str, sub: str | None = None) -> dict | None:
        s = sets.get(name) or {}
        s = ((s.get("by_condition_event") or {}).get(sub) or {}) if sub else s
        return (s.get("sidechat") or {}).get(key)

    def both(name: str, key: str, subs: tuple[str, ...]) -> dict | None:
        parts = [get(name, key, x) for x in subs]
        parts = [p for p in parts if p and p.get("n")]
        if not parts:
            return None
        k, n = sum(p["k"] for p in parts), sum(p["n"] for p in parts)
        return {"value": k / n, "k": k, "n": n}

    return {
        "generated": get("generated test @anonymous", "decision_right"),
        "gen04": get("gen-0.4.test@anonymous", "decision_right"),
        "duplex": get("duplex-mpe-0.1", "decision_right"),
        "duplex_outright": get("duplex-mpe-0.1", "answers_now_wrongly"),
        "implicit_t": get("duplex-mpe-0.1", "answered_now", "implicit/T"),
        "n1_outright": both("duplex-mpe-0.1", "answers_now_wrongly", ("explicit/N1", "implicit/N1")),
        "ambient": get("ambient-bench-0.1", "decision_right"),
        "ami": get("ami-addressee-0.1", "decision_right"),
        "ami_silent_outright": get("ami-silent-0.1.test", "answers_now_wrongly"),
        "pilot": get("pilot-0.4@anonymous", "decision_right"),
        "demo": get("demo-lines-0.1", "decision_right"),
    }


def _pct(x: dict | None, digits: int = 1) -> str:
    if not x or x.get("value") is None:
        return "n/a"
    return f"{100 * x['value']:.{digits}f}% ({x['k']:,}/{x['n']:,})"


def _render(exp: str, teacher: str, models: dict[str, dict], speed: dict, gate: dict, notes: list[str]) -> str:
    rows = [
        ("Generated test, anonymous", "generated", 1),
        ("gen-0.4 test, anonymous", "gen04", 1),
        ("Duplex-MPE, right", "duplex", 1),
        ("… lines for others answered outright", "duplex_outright", 2),
        ("… unnamed request answered (implicit T)", "implicit_t", 1),
        ("… name said about the agent, answered outright (N1)", "n1_outright", 2),
        ("Ambient Bench, right", "ambient", 1),
        ("AMI labelled, right", "ami", 1),
        ("AMI silent test, answered outright", "ami_silent_outright", 2),
        ("Pilot, anonymous, right", "pilot", 1),
        ("Demo lines, right", "demo", 1),
    ]
    names = list(models)
    lines = [
        f"# Round 6 and the agent-1x students ({exp})",
        "",
        f"Teacher: `{teacher}`. Speakers anonymous. Shares are `value (k/n)`; each run's own report has 95% intervals.",
        "",
        "| | " + " | ".join(f"`{n}`" for n in names) + " |",
        "|---|" + "---|" * len(names),
    ]
    for label, key, digits in rows:
        lines.append(f"| {label} | " + " | ".join(_pct(models[n].get(key), digits) for n in names) + " |")
    lines += ["", "## Speed on agent-1x (0.5 vCPU, 1 GiB), one thread", ""]
    if speed:
        lines += [
            (
                "Median ms per line through the demo's gate: short history / 8 earlier lines. For a two-tower "
                "model the history is encoded first, untimed, as while the person talks."
            ),
            "",
            "| Model | Build | Memory MB | Short | Full history | Full history, cold | Beats Jev |",
            "|---|---|---|---|---|---|---|",
        ]
        for name, s in speed.items():
            lines.append(
                f"| `{name}` | {s.get('build', '')} | {s.get('memory', '')} | {s.get('short', '')} | {s.get('full', '')} | "
                f"{s.get('cold', '')} | {s.get('beats', '')} |"
            )
    else:
        lines.append("Not measured.")
    lines += ["", "## The gate", ""]
    for name, g in gate.items():
        lines.append(f"- `{name}`: **{'ships' if g['ships'] else 'does not ship'}**. {g['why']}")
    if not gate:
        lines.append("No student was gated.")
    if notes:
        lines += ["", "## Notes", ""] + [f"- {n}" for n in notes]
    return "\n".join(lines) + "\n"


@app.function(image=LT.image, cpu=0.25, memory=1024, timeout=14 * 3600, secrets=T._secrets())
def run(
    exp: str = "exp-042-side-round6",
    steps: str = "committee,r6,students,export,latency",
    teacher: str = "",
    min_agreement: float = 0.9,
    wait_for: str = "",
    suffix: str = "",
    student_tag: str = "",
    tt_encoders: str = "ettin-32m,ettin-68m",
    short: bool = True,
    export_teacher: bool = True,
    student_seed: int = 0,
    student_alpha: float = 0.8,
) -> dict:
    """`wait_for` names experiments to wait for first (until R2 says they are done, failed or stopped);
    `suffix` is added to the step experiments' names, so a second pass keeps the first's.
    `student_tag` names a second set of students (e.g. `r3t`, taught by round 3) so they do not
    overwrite the first; `tt_encoders` and `short` choose which students; `export_teacher` False
    leaves the teacher's export as it is. `student_seed` and `student_alpha` (the teacher's share of
    the targets) vary the students' training."""
    import time
    import traceback
    from datetime import UTC, datetime

    from sidechat.lib import r2

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    started = time.monotonic()
    want = [x.strip() for x in steps.split(",") if x.strip()]
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {"steps": steps, "teacher": teacher, "min_agreement": min_agreement},
        "steps": {},
    }
    notes: list[str] = []

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    def step(name: str, value) -> None:
        status["steps"][name] = value
        save(stage=name)

    def wait(calls: dict) -> dict:
        got = {}
        for k, c in calls.items():
            try:
                got[k] = c.get()
            except Exception as e:  # noqa: BLE001 - a failed branch is reported, the others go on
                got[k] = {"state": "failed", "error": f"{type(e).__name__}: {str(e)[:300]}"}
        return got

    try:
        save()
        for e in [x.strip() for x in wait_for.split(",") if x.strip()]:
            save(stage=f"waiting for {e}")
            while ((r2.get_json(s3, f"{r2.PREFIX}/results/{e}/status.json") or {}).get("state")) not in ("done", "failed", "stopped"):
                time.sleep(60)
        # 1. The committee and round 6, side by side.
        calls = {}
        if "committee" in want:
            calls["committee"] = L.run.spawn(EXP["committee"], sets=COMMITTEE_SETS, spend_cap_usd=20.0)
        if "r6" in want:
            for seed, e in enumerate(EXP["r6"]):
                calls[f"r6-s{seed}"] = T.run.spawn(
                    e, corpus=CORPUS, encoders="ettin-150m", epochs=2, seed=seed, tag="r6", **TEST
                )
        if calls:
            step("committee and round 6", {k: "running" for k in calls})
            step("committee and round 6", wait(calls))

        # 2. Kinds to leave out of the students' corpus.
        drop = []
        committee = r2.get_json(s3, f"{r2.PREFIX}/results/{EXP['committee']}/scorecard.json") or {}
        by_kind = committee.get("by_kind") or {}
        for k in NEW_KINDS:
            v = (by_kind.get(k) or {}).get("value")
            if v is not None and v < min_agreement:
                drop.append(k)
                notes.append(f"The committee agrees with `{k}` on {100 * v:.1f}%, under {100 * min_agreement:.0f}%: left out of the students' corpus.")
            elif v is None:
                notes.append(f"No committee result for `{k}`; kept.")
        status["committee_by_kind"] = {k: by_kind.get(k) for k in (*NEW_KINDS, "command_no_name", "reply_then_request")}

        # 3. The teacher: the round 6 seed with more dev decisions right.
        if not teacher:
            best = None
            for seed in (0, 1):
                card = r2.get_json(s3, f"{r2.PREFIX}/predictions/side-r6-ettin-150m-s{seed}/scorecard.json") or {}
                t = card.get("thresholds") or {}
                if t.get("dev_n"):
                    share = t["dev_right"] / t["dev_n"]
                    if best is None or share > best[1]:
                        best = (f"side-r6-ettin-150m-s{seed}", share)
            teacher = best[0] if best else REFERENCE
            if not best:
                notes.append(f"No round 6 model scored; the students learn from `{REFERENCE}`.")
        step("teacher", teacher)

        # 4. The students.
        tt_tag, s_tag = f"r6tt{student_tag}", f"r6s{student_tag}"
        tt_encs = [e for e in tt_encoders.split(",") if e]
        sd = student_seed
        students = {f"side-{tt_tag}-{e}-s{sd}": f"two towers, {e}" for e in tt_encs}
        if short:
            students[f"side-{s_tag}-ettin-32m-s{sd}"] = "one tower, ettin-32m, 4 earlier lines"
        if "students" in want:
            common = dict(
                corpus=STUDENT_CORPUS,
                epochs=3,
                seed=student_seed,
                teacher=teacher,
                alpha=student_alpha,
                drop_kinds=",".join(drop),
                **TEST,
            )
            calls = {}
            if tt_encs:
                calls["two towers"] = T.run.spawn(
                    EXP["tt"] + suffix, encoders=",".join(tt_encs), tag=tt_tag, arch="twotower", **common
                )
            if short:
                calls["short"] = T.run.spawn(
                    EXP["short"] + suffix, encoders="ettin-32m", tag=s_tag, text_turns=4, max_len=160, **common
                )
            step("students", {k: "running" for k in calls})
            step("students", wait(calls))

        # 5. Exports.
        exports = {k: EXPORTS.get(k, f"{exp}-export-{LT._short(k)}") + suffix for k in students}
        if export_teacher:
            exports = {teacher: EXPORTS["teacher"] + suffix, **exports}
        latency_exp = EXP["latency"] + suffix
        if "export" in want:
            calls = {}
            for run_id, e in exports.items():
                if r2.get_json(s3, T._model_key(run_id, "config.json")) is not None:
                    calls[run_id] = X.run.spawn(e, run_id)
            step("export", {k: "running" for k in calls})
            step("export", {k: {x: v.get(x) for x in ("size_mb", "optimized", "error")} if isinstance(v, dict) else v
                            for k, v in wait(calls).items()})

        # 6. Latency beside Jev.
        if "latency" in want:
            ids = [i for i in exports if r2.get_json(s3, T._model_key(i, "export/config.json")) is not None]
            step("latency", "running")
            got = wait({"latency": LT.run.spawn(latency_exp, run_ids=",".join(ids), profiles="agent-1x,agent-2x",
                                                threads="1", rounds=3, jev=True)})
            step("latency", got["latency"])

        # 7. Summary and the gate.
        save(stage="summary")
        models = {}
        for run_id in [REFERENCE, *(f"side-r6-ettin-150m-s{s}" for s in (0, 1)), *students]:
            card = r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json")
            if card:
                models[run_id] = _metrics(card)
        lat = r2.get_json(s3, f"{r2.PREFIX}/results/{latency_exp}/scorecard.json") or {}
        variants = [v for v in lat.get("variants") or [] if v.get("profile") == "agent-1x"]
        jev = next((v for v in variants if v.get("name") == "jev" and v.get("ok")), None)
        jev_full = (jev or {}).get("full_window", {}).get("p50")
        speed = {}
        for run_id in exports:
            short = LT._short(run_id)
            mine = [v for v in variants if v.get("run_id") == run_id and v.get("ok")]
            pick = next((v for v in mine if v.get("int8")), None) or next(iter(mine), None)
            if not pick:
                continue
            full = pick["full_window"]["p50"]
            speed[run_id] = {
                "build": f"{'int8' if pick.get('int8') else 'fp32'} ({short})",
                "memory": f"{pick.get('rss_mb_peak', 0):.0f}",
                "short": f"{pick['demo']['p50']:.0f}",
                "full": f"{full:.0f}",
                "cold": f"{pick['full_window_cold']['p50']:.0f}" if pick.get("full_window_cold") else "",
                "beats": "" if jev_full is None else ("yes" if full < jev_full else "no") + f" (Jev {jev_full:.0f})",
                "full_ms": full,
            }
        bad_parity = set()
        for run_id, e in exports.items():
            p = (r2.get_json(s3, f"{r2.PREFIX}/results/{e}/scorecard.json") or {}).get("parity") or {}
            if p.get("rows") and p["decisions_same"] < 0.98 * p["rows"]:
                bad_parity.add(run_id)
                notes.append(
                    f"`{run_id}`'s export disagrees with PyTorch on {p['rows'] - p['decisions_same']} of {p['rows']} "
                    f"parity lines (largest probability difference {p['max_prob_diff']}): its timing is not trusted."
                )
        gate = {}
        t = models.get(teacher)
        for run_id in students:
            m = models.get(run_id)
            if not m or not t:
                continue
            gaps = []
            for key, label in (("duplex", "Duplex-MPE"), ("ami", "AMI"), ("pilot", "pilot")):
                if m.get(key) and t.get(key):
                    d = 100 * (m[key]["value"] - t[key]["value"])
                    gaps.append((label, d))
            close = all(d >= -1.0 for _, d in gaps)
            s = speed.get(run_id) or {}
            fast = jev_full is not None and s.get("full_ms") is not None and s["full_ms"] < jev_full
            gate[run_id] = {
                "ships": bool(close and fast and run_id not in bad_parity),
                "why": "; ".join(f"{label} {d:+.1f} points against the teacher" for label, d in gaps)
                + (f"; full history {s['full']} ms on agent-1x against Jev's {jev_full:.0f}" if s and jev_full else "; not timed"),
            }
        card = {"exp": exp, "teacher": teacher, "dropped_kinds": drop, "models": models, "speed": speed, "gate": gate,
                "notes": notes, "finished_at": datetime.now(UTC).isoformat(timespec="seconds")}
        r2.put_json(s3, f"{out}/scorecard.json", card)
        r2.put_text(s3, f"{out}/report.md", _render(exp, teacher, models, speed, gate, notes))
        save(state="done", stage="done")
        return {"state": "done", "teacher": teacher, "gate": gate}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
