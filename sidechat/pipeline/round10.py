"""Round 10: the line after the agent answers, for both builds, in one detached Modal job.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.round10::run --exp exp-066-side-round10

    uv run python -m sidechat.pipeline.results exp-066-side-round10

On TCL's independent test (exp-063) rc0.3 answers people's lines outright three times as often as on
our own tests, half of it right after the agent answers: in our corpora every question there is for
the agent. Round 10 is round 9 (realreq-0.2, the hold bar on AMI's real dev lines) plus gen-0.5
(exp-064), whose new kinds put people's own questions and comments right after the agent's answer,
and the agent's partner coming back to it later without its name. Steps, each its own experiment
named after this one:

    baselines rc0.3's builds scored on gen-0.5's test split (`train.score_sets`)
    teacher   Ettin-150M, 2 epochs, round 9's teacher corpus plus gen-0.5, seeds 0 and 1
    pick      the seed with more dev decisions right (real dev lines left alone counted)
    students  two-tower Ettin-32M distilled from it, round 9's student corpus plus gen-0.5, seeds 0, 1
    export    the teacher and the students
    latency   the students and rc0.3's agent-1x build on agent-1x and agent-2x beside Jev
    summary   runs/side/results/<exp>/report.md and the gates (`student_gate.gate_r10`, fixed in
              exp-066's record before training): each build against rc0.3's

TCL's test is scored for every model and read for the report and the gate, never for a pick
(SD-27). Picks use dev only.
"""

from __future__ import annotations

import modal

from sidechat.pipeline import export as X
from sidechat.pipeline import latency as LT
from sidechat.pipeline import train as T
from sidechat.pipeline.student_gate import TCL_SET, gate_r10, metrics_r10, pct, tcl_paired

APP_NAME = "waystone-side-round10"
app = modal.App(APP_NAME)
for other in (T.app, X.app, LT.app):
    app.include(other)

R9 = "side-r9-ettin-150m-s1"  # rc0.3's default build
R9TT = "side-r9tt-ettin-32m-s1"  # rc0.3's agent-1x build
TEACHER_CORPUS = "gen-0.1,gen-pilot,gen-0.2,ami-silent,realreq,gen-0.5"  # round 9's, plus gen-0.5
STUDENT_CORPUS = "gen-0.1,gen-pilot,gen-0.2,gen-0.3,gen-0.4,ami-silent,realreq,gen-0.5"  # round 9's, plus gen-0.5
NEW_SETS = "corpus:gen-0.5:test@anonymous,tcl@anonymous"
TEST = {
    "test_corpus": "gen-0.1,gen-pilot",
    "extra_sets": (
        "corpus:gen-0.2:test@anonymous,corpus:gen-0.4:test@anonymous,"
        "slurp,slurp-stt,slurp-stt-keyterm,ami-stt,ami-silent-stt:test,"
        f"{NEW_SETS}"
    ),
}
ROWS = [
    ("Generated test, anonymous", "generated", 1),
    ("Duplex-MPE, right", "duplex", 1),
    ("… for others, answered outright", "duplex_outright", 2),
    ("… for others, held", "duplex_held", 1),
    ("… named request answered", "explicit_t", 1),
    ("… unnamed request answered", "implicit_t", 1),
    ("… unnamed request held", "implicit_held", 1),
    ("Ambient Bench, right", "ambient", 1),
    ("AMI labelled, right", "ami", 1),
    ("AMI as heard, held", "ami_heard_held", 2),
    ("AMI silence test, answered outright", "ami_silent_outright", 2),
    ("Pilot, right", "pilot", 1),
    ("Demo lines, right", "demo", 1),
    ("SLURP named, answered now: written", "slurp_named_written", 1),
    ("SLURP named, answered now: heard", "slurp_named_heard", 1),
    ("SLURP named, answered now: heard with keyterm", "slurp_named_keyterm", 1),
    ("SLURP unnamed, held: written", "slurp_unnamed_held_written", 1),
    ("SLURP unnamed, held: heard", "slurp_unnamed_held_heard", 1),
    ("SLURP unnamed, held: heard with keyterm", "slurp_unnamed_held_keyterm", 1),
    ("SLURP unnamed, answered now: heard", "slurp_unnamed_answered_heard", 1),
    ("TCL, people's lines answered outright", "tcl_outright", 2),
    ("TCL, people's lines held", "tcl_held", 1),
    ("TCL, named requests answered now", "tcl_direct", 1),
    ("TCL, unnamed follow-ups answered now", "tcl_ctx_now", 1),
    ("TCL, unnamed follow-ups held", "tcl_ctx_held", 1),
    ("gen-0.5 test: question to the others after the agent, left alone", "g5_pq", 1),
    ("gen-0.5 test: the partner turning to the others, left alone", "g5_pp", 1),
    ("gen-0.5 test: the partner coming back later, held", "g5_later", 1),
    ("gen-0.5 test: follow-up, answered now", "g5_follow_up", 1),
]


def _render(exp: str, teacher: str, models: dict, speed: dict, gates: dict, notes: list[str]) -> str:
    names = list(models)
    lines = [
        f"# Round 10: the line after the agent answers ({exp})",
        "",
        (
            f"Teacher: `{teacher}`. `{R9}` is rc0.3's default build, `{R9TT}` its agent-1x build. "
            "Speakers anonymous. Shares are `value (k/n)`."
        ),
        "",
        "| | " + " | ".join(f"`{n}`" for n in names) + " |",
        "|---|" + "---|" * len(names),
    ]
    for label, key, digits in ROWS:
        lines.append(f"| {label} | " + " | ".join(pct(models[n].get(key), digits) for n in names) + " |")
    lines += ["", "## Speed on agent-1x (0.5 vCPU, 1 GiB), one thread, history encoded ahead", ""]
    if speed:
        lines += ["| Model | Build | Memory MB | Full history | Full history, cold |", "|---|---|---|---|---|"]
        for name, s in speed.items():
            lines.append(
                f"| `{name}` | {s.get('build', '')} | {s.get('memory', '')} | {s.get('full', '')} | {s.get('cold', '')} |"
            )
    else:
        lines.append("Not measured.")
    lines += ["", "## The gates", ""]
    for name, g in gates.items():
        lines.append(f"- `{name}`: **{'ships' if g['ships'] else 'does not ship'}**. {g['why']}")
    if notes:
        lines += ["", "## Notes", ""] + [f"- {n}" for n in notes]
    return "\n".join(lines) + "\n"


@app.function(  # it launches every step, so it is not preempted (sidechat/lib/resume.py)
    image=LT.image, cpu=0.25, memory=1024, timeout=16 * 3600, secrets=T._secrets(), nonpreemptible=True
)
def run(
    exp: str = "exp-066-side-round10",
    steps: str = "baselines,teacher,students,export,latency",
    teacher: str = "",
    tag: str = "r10",
    realreq: str = "realreq-0.2",
    max_held_real: float = 0.002,
    drop_kinds: str = "",
    student_seeds: str = "0,1",
    pick_among: str = "",
) -> dict:
    """`teacher` skips the pick (and is required if `teacher` is not in `steps`). `drop_kinds` leaves
    kinds out of training (`train.run(drop_kinds=...)`), for a kind the committee reads otherwise.
    `student_seeds` trains other student seeds against a fixed `teacher`; `pick_among` adds earlier
    students (run ids) to the dev pick, so the pick is made across every seed (exp-071)."""
    import time
    import traceback
    from datetime import UTC, datetime

    from sidechat.lib import r2, resume

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
        "args": {
            "steps": steps,
            "teacher": teacher,
            "tag": tag,
            "realreq": realreq,
            "max_held_real": max_held_real,
            "drop_kinds": drop_kinds,
            "student_seeds": student_seeds,
            "pick_among": pick_among,
        },
        "steps": {},
    }
    # Restarted by Modal on the same input: wait on the calls already spawned, skip finished steps.
    kept = resume.carried(r2.get_json(s3, f"{out}/status.json"), status["args"])
    if kept:
        status.update(started_at=kept["started_at"], steps=kept["steps"], restarts=kept["restarts"])
        status["restarted_at"] = datetime.now(UTC).isoformat(timespec="seconds")
    status["calls"] = kept.get("calls", {})
    notes: list[str] = []

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    spawner = resume.Calls(status["calls"], save)

    def wait(calls: dict) -> dict:
        got = {}
        for k, c in calls.items():
            try:
                got[k] = c.get()
            except Exception as e:  # noqa: BLE001 - a failed branch is reported, the others go on
                got[k] = {"state": "failed", "error": f"{type(e).__name__}: {str(e)[:300]}"}
        return got

    def brief(got: dict) -> dict:
        return {k: (v.get("state") or "done") if isinstance(v, dict) else "done" for k, v in got.items()}

    try:
        save()
        teacher_corpus = TEACHER_CORPUS.replace("realreq", realreq)
        student_corpus = STUDENT_CORPUS.replace("realreq", realreq)
        teachers = [f"side-{tag}-ettin-150m-s{s}" for s in (0, 1)]
        base_calls = {}
        if "baselines" in want and "baselines" not in status["steps"]:
            # rc0.3 on gen-0.5's test split; its TCL cards are exp-063's, at the same thresholds.
            base_calls = {
                run_id: spawner.spawn(f"baselines/{run_id}", T.score_sets, run_id, "corpus:gen-0.5:test@anonymous")
                for run_id in (R9, R9TT)
            }
        if "teacher" in want and "teacher" not in status["steps"]:
            calls = {
                f"s{s}": spawner.spawn(
                    f"teacher/s{s}",
                    T.run,
                    f"{exp}-train-{tag}-s{s}",
                    corpus=teacher_corpus,
                    encoders="ettin-150m",
                    epochs=2,
                    seed=s,
                    tag=tag,
                    max_held_real=max_held_real,
                    drop_kinds=drop_kinds,
                    **TEST,
                )
                for s in (0, 1)
            }
            save(stage="teacher")
            status["steps"]["teacher"] = brief(wait(calls))

        def dev_pick(run_ids: list[str]) -> str | None:
            """The run with the most dev decisions right, real people's dev lines left alone counted."""
            best = None
            for run_id in run_ids:
                t = (r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json") or {}).get("thresholds") or {}
                if t.get("dev_n"):
                    q = t.get("real_quiet", 0)
                    left = q - t.get("real_wrong_now", 0) - t.get("real_held", 0)
                    share = (t["dev_right"] + left) / (t["dev_n"] + q)
                    if best is None or share > best[1]:
                        best = (run_id, share)
            return best[0] if best else None

        if not teacher:
            teacher = status["steps"].get("pick") or dev_pick(teachers)
            if not teacher:
                save(state="failed", reason="no teacher scored")
                return {"state": "failed"}
        status["steps"]["pick"] = teacher
        save(stage="students")

        seeds = [int(x) for x in student_seeds.split(",") if x.strip()]
        students = [f"side-{tag}tt-ettin-32m-s{s}" for s in seeds]
        earlier = [x for x in pick_among.split(",") if x.strip()]
        if "students" in want and "students" not in status["steps"]:
            calls = {
                f"s{s}": spawner.spawn(
                    f"students/s{s}",
                    T.run,
                    f"{exp}-train-{tag}tt-s{s}",
                    corpus=student_corpus,
                    encoders="ettin-32m",
                    epochs=3,
                    seed=s,
                    tag=f"{tag}tt",
                    teacher=teacher,
                    alpha=0.8,
                    arch="twotower",
                    max_held_real=max_held_real,
                    drop_kinds=drop_kinds,
                    **TEST,
                )
                for s in seeds
            }
            status["steps"]["students"] = brief(wait(calls))

        # The seed is in the name: without it both students' exports wrote one report (exp-060).
        exports = {
            run_id: f"{exp}-export-{LT._short(run_id)}-{run_id.rsplit('-', 1)[-1]}" for run_id in [teacher, *students]
        }
        if "export" in want and "export" not in status["steps"]:
            calls = {
                run_id: spawner.spawn(f"export/{run_id}", X.run, e, run_id)
                for run_id, e in exports.items()
                if r2.get_json(s3, T._model_key(run_id, "config.json")) is not None
            }
            save(stage="export")
            status["steps"]["export"] = brief(wait(calls))

        latency_exp = f"{exp}-latency"
        if "latency" in want and "latency" not in status["steps"]:
            ids = [R9TT] + [
                i for i in [*earlier, *students] if r2.get_json(s3, T._model_key(i, "export/config.json")) is not None
            ]
            save(stage="latency")
            got = wait(
                {
                    "latency": spawner.spawn(
                        "latency",
                        LT.run,
                        latency_exp,
                        run_ids=",".join(ids),
                        profiles="agent-1x,agent-2x",
                        threads="1",
                        rounds=3,
                        jev=True,
                    )
                }
            )
            status["steps"]["latency"] = brief(got)

        if base_calls:
            save(stage="baselines")
            status["steps"]["baselines"] = brief(wait(base_calls))

        # Summary and gates.
        save(stage="summary")
        models, cards = {}, {}
        for run_id in [R9, *teachers, R9TT, *earlier, *students]:
            card = r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json")
            if not card:
                continue
            if run_id in (R9, R9TT):
                # Scored before gen-0.5 and TCL: those cards come from `score_sets` at the same thresholds.
                for rows_id in ("gen-0.5.test@anonymous", TCL_SET):
                    c = r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/sets/{rows_id}.json")
                    if c and rows_id not in card.get("sets", {}):
                        card.setdefault("sets", {})[rows_id] = c
            cards[run_id] = card
            models[run_id] = metrics_r10(card)
        if teacher in cards:
            models["jev"] = metrics_r10(cards[teacher], who="jev")
        lat = r2.get_json(s3, f"{r2.PREFIX}/results/{latency_exp}/scorecard.json") or {}
        variants = [v for v in lat.get("variants") or [] if v.get("profile") == "agent-1x"]
        jev = next((v for v in variants if v.get("name") == "jev" and v.get("ok")), None)
        jev_ms = (jev or {}).get("full_window", {}).get("p50")
        speed = {}
        for run_id in [R9TT, *earlier, *students]:
            mine = [v for v in variants if v.get("run_id") == run_id and v.get("ok")]
            pick = next((v for v in mine if not v.get("int8")), None) or next(iter(mine), None)
            if pick:
                speed[run_id] = {
                    "build": "int8" if pick.get("int8") else "fp32",
                    "memory": f"{pick.get('rss_mb_peak', 0):.0f}",
                    "full": f"{pick['full_window']['p50']:.0f}",
                    "cold": f"{pick['full_window_cold']['p50']:.0f}" if pick.get("full_window_cold") else "",
                    "full_ms": pick["full_window"]["p50"],
                }
        if jev_ms is not None:
            speed["jev"] = {"build": "API", "full": f"{jev_ms:.0f}"}
        # TCL, paired against rc0.3's builds on the same lines (SD-27: for the gate, not the picks).
        from sidechat.sources import build
        from sidechat.train import evaluate as E

        tcl_rows = build.build_rows("tcl@anonymous")[0]

        def decided(run_id: str) -> dict[str, str]:
            t = (r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json") or {}).get("thresholds")
            preds = r2.get_jsonl(s3, f"{r2.PREFIX}/predictions/{run_id}/{TCL_SET}.jsonl") or []
            return {p["row_id"]: E.decide(p, t) for p in preds} if t else {}

        paired_tcl = {}
        for run_id, base_id in [(x, R9) for x in teachers] + [(x, R9TT) for x in [*earlier, *students]]:
            if run_id in models:
                paired_tcl[run_id] = tcl_paired(decided(run_id), decided(base_id), tcl_rows)
        gates = {}
        for run_id in teachers:
            if run_id in models and R9 in models:
                gates[run_id] = gate_r10(models[run_id], models[R9], paired_tcl.get(run_id))
        for run_id in [*earlier, *students]:
            if run_id in models and R9TT in models:
                g = gate_r10(models[run_id], models[R9TT], paired_tcl.get(run_id))
                s = (speed.get(run_id) or {}).get("full_ms")
                fast = s is not None and jev_ms is not None and s < jev_ms
                g["why"] += (
                    f"; {'' if fast else '**fails:** '}full history on agent-1x {s if s is None else round(s)} ms (Jev {jev_ms if jev_ms is None else round(jev_ms)})"
                )
                g["ships"] = g["ships"] and fast
                gates[run_id] = g
        notes.append(
            f"Dev picks `{teacher}` among the teachers and `{dev_pick([*earlier, *students])}` among the students."
        )
        card = {
            "exp": exp,
            "teacher": teacher,
            "student_pick": dev_pick([*earlier, *students]),
            "models": models,
            "speed": speed,
            "gates": gates,
            "tcl_paired": paired_tcl,
            "notes": notes,
            "finished_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        r2.put_json(s3, f"{out}/scorecard.json", card)
        r2.put_text(s3, f"{out}/report.md", _render(exp, teacher, models, speed, gates, notes))
        save(state="done", stage="done")
        return {"state": "done", "teacher": teacher, "gates": {k: v["ships"] for k, v in gates.items()}}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
