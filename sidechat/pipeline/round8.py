"""Round 8: real people's requests in training, for both builds, in one detached Modal job.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.round8::run --exp exp-059-side-round8

    uv run python -m sidechat.pipeline.results exp-059-side-round8

On real speech both builds ignore most unnamed requests an assistant could do (exp-057: 82% to 97%
missed; Jev holds 82%). This round adds `realreq` (`sidechat/sources/realreq.py`): 12,000 requests
people wrote or said to assistants (SLURP's and CLINC150's text), said in AMI's unlabelled training
meetings, held for a pause when unnamed, answered when they name the agent, left alone when they
name a person. Steps, each its own experiment named after this one:

    teacher   round 3's recipe (Ettin-150M, 2 epochs) on round 3's corpus plus realreq, seeds 0 and 1
    pick      the seed with more dev decisions right
    students  two-tower Ettin-32M distilled from it on the rc0.2 student's corpus plus realreq,
              seeds 0 and 1
    export    the teacher and the students
    latency   the students and the rc0.2 student on agent-1x and agent-2x beside Jev
    summary   runs/side/results/<exp>/report.md and the gates: the teacher against round 3, each
              student against the rc0.2 student (`student_gate.gate_default`), and students must
              beat Jev's speed on agent-1x

Every model is scored on real speech too: AMI as heard and SLURP's requests in AMI meetings,
written, heard, and heard with the name as a keyterm. SLURP's test split is never trained on; its
requests are left out of `realreq`.
"""

from __future__ import annotations

import modal

from sidechat.pipeline import export as X
from sidechat.pipeline import latency as LT
from sidechat.pipeline import train as T
from sidechat.pipeline.student_gate import gate_default, metrics_r8, pct

APP_NAME = "waystone-side-round8"
app = modal.App(APP_NAME)
for other in (T.app, X.app, LT.app):
    app.include(other)

R3 = "side-r3-ettin-150m-s0"
RC02 = "side-r6ttr3t-ettin-32m-s0"
TEACHER_CORPUS = "gen-0.1,gen-pilot,gen-0.2,ami-silent,realreq"  # round 3's, plus realreq
STUDENT_CORPUS = "gen-0.1,gen-pilot,gen-0.2,gen-0.3,gen-0.4,ami-silent,realreq"  # rc0.2 student's, plus realreq
TEST = {
    "test_corpus": "gen-0.1,gen-pilot",
    "extra_sets": (
        "corpus:gen-0.2:test@anonymous,corpus:gen-0.4:test@anonymous,"
        "slurp,slurp-stt,slurp-stt-keyterm,ami-stt,ami-silent-stt:test"
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
]


def _render(exp: str, teacher: str, models: dict, speed: dict, gates: dict, notes: list[str]) -> str:
    names = list(models)
    lines = [
        f"# Real people's requests in training ({exp})",
        "",
        (
            f"Teacher: `{teacher}`. `{R3}` is the released default build, `{RC02}` the released agent-1x build. "
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
    exp: str = "exp-059-side-round8",
    steps: str = "teacher,students,export,latency",
    teacher: str = "",
    tag: str = "r8",
    realreq: str = "realreq",
    max_held_real: float = 0.0,
) -> dict:
    """`teacher` skips the pick (and is required if `teacher` is not in `steps`). Round 9 is the same
    job with `tag` r9, `realreq` realreq-0.2 (fewer requests, more said to a person) and
    `max_held_real` 0.002 (thresholds hold at most 0.2% of AMI's real dev lines)."""
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
        "args": {"steps": steps, "teacher": teacher, "tag": tag, "realreq": realreq, "max_held_real": max_held_real},
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

        students = [f"side-{tag}tt-ettin-32m-s{s}" for s in (0, 1)]
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
                    **TEST,
                )
                for s in (0, 1)
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
            ids = [RC02] + [i for i in students if r2.get_json(s3, T._model_key(i, "export/config.json")) is not None]
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

        # Summary and gates.
        save(stage="summary")
        models, cards = {}, {}
        for run_id in [R3, *teachers, RC02, *students]:
            card = r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json")
            if not card:
                continue
            if run_id in (R3, RC02):
                # Scored before the real-speech sets: their cards for those come from exp-056 to exp-058
                # (`score_sets`, at the same stored thresholds).
                extra = {
                    "ami-addressee-stt-0.1": f"{run_id}/sets/ami-addressee-stt-0.1.json",
                    "ami-silent-stt-0.1.test": f"{run_id}/sets/ami-silent-stt-0.1.test.json",
                    "slurp-in-ami-0.1": f"{run_id}/plain/sets/slurp-in-ami-0.1.json",
                    "slurp-in-ami-stt-0.1": f"{run_id}/plain/sets/slurp-in-ami-stt-0.1.json",
                    "slurp-in-ami-stt-keyterm-0.1": f"{run_id}/plain/sets/slurp-in-ami-stt-keyterm-0.1.json",
                }
                for rows_id, key in extra.items():
                    c = r2.get_json(s3, f"{r2.PREFIX}/predictions/{key}")
                    if c and rows_id not in card.get("sets", {}):
                        card.setdefault("sets", {})[rows_id] = c
            cards[run_id] = card
            models[run_id] = metrics_r8(card)
        if teacher in cards:
            models["jev"] = metrics_r8(cards[teacher], who="jev")
        lat = r2.get_json(s3, f"{r2.PREFIX}/results/{latency_exp}/scorecard.json") or {}
        variants = [v for v in lat.get("variants") or [] if v.get("profile") == "agent-1x"]
        jev = next((v for v in variants if v.get("name") == "jev" and v.get("ok")), None)
        jev_ms = (jev or {}).get("full_window", {}).get("p50")
        speed = {}
        for run_id in [RC02, *students]:
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
        gates = {}
        if teacher in models and R3 in models:
            gates[teacher] = gate_default(models[teacher], models[R3])
        for run_id in students:
            if run_id in models and RC02 in models:
                g = gate_default(models[run_id], models[RC02])
                s = (speed.get(run_id) or {}).get("full_ms")
                fast = s is not None and jev_ms is not None and s < jev_ms
                g["why"] += (
                    f"; {'' if fast else '**fails:** '}full history on agent-1x {s if s is None else round(s)} ms (Jev {jev_ms if jev_ms is None else round(jev_ms)})"
                )
                g["ships"] = g["ships"] and fast
                gates[run_id] = g
        notes.append(f"Dev picks `{teacher}` among the teachers and `{dev_pick(students)}` among the students.")
        card = {
            "exp": exp,
            "teacher": teacher,
            "student_pick": dev_pick(students),
            "models": models,
            "speed": speed,
            "gates": gates,
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
