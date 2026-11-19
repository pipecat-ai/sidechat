"""Student round 2 for agent-1x, aimed at unnamed requests (item 5), in one detached Modal job.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.round7::run --exp exp-055-side-round7

    uv run python -m sidechat.pipeline.results exp-055-side-round7

Every model reads Duplex-MPE's unnamed requests as said to a person or to the agent, and round 3
answers 38.8% of them where the rc0.2 student answers 10.7% (SD-21). The students copy round 3 on
full transcripts but have never seen a transcript of the people's side only, which is how an
integration that logs only the people's speech, and Duplex-MPE, give the history. So some training
lines lose the agent's turns and take round 3's probabilities as their whole target
(`train(people_only=...)`). Steps, each its own experiment named after this one:

    students   two-tower Ettin-32M taught by round 3, people-only share 0.25 and 0.5, seeds 0 and 1
    export     ONNX, transformer optimizer, int8 gate
    latency    on agent-1x and agent-2x beside Jev and the rc0.2 student, one thread
    summary    runs/side/results/<exp>/report.md and the gate: faster than Jev on agent-1x with a full
               history; within a point of the teacher on Duplex-MPE, AMI and the pilot; named
               requests within a point of the teacher (item 4); unnamed requests answered more
               often than Jev (item 5); export parity

`steps` runs a subset, in order.
"""

from __future__ import annotations

import modal

from sidechat.pipeline import export as X
from sidechat.pipeline import latency as LT
from sidechat.pipeline import train as T
from sidechat.pipeline.student_gate import JEV_IMPLICIT_T, gate_one
from sidechat.pipeline.student_gate import metrics as _metrics
from sidechat.pipeline.student_gate import pct as _pct

APP_NAME = "waystone-side-round7"
app = modal.App(APP_NAME)
for other in (T.app, X.app, LT.app):
    app.include(other)

CORPUS = "gen-0.1,gen-pilot,gen-0.2,gen-0.3,gen-0.4,ami-silent"  # the rc0.2 student's
TEST = {"test_corpus": "gen-0.1,gen-pilot", "extra_sets": "corpus:gen-0.2:test@anonymous,corpus:gen-0.4:test@anonymous"}
TEACHER = "side-r3-ettin-150m-s0"
RC02 = "side-r6ttr3t-ettin-32m-s0"  # rc0.2's agent-1x build


def _render(exp: str, models: dict[str, dict], speed: dict, gate: dict, notes: list[str]) -> str:
    rows = [
        ("Generated test, anonymous", "generated", 1),
        ("Duplex-MPE, right", "duplex", 1),
        ("… lines for others answered outright", "duplex_outright", 2),
        ("… lines for others held", "duplex_held", 1),
        ("… named request answered (item 4)", "explicit_t", 1),
        ("… unnamed request answered (item 5)", "implicit_t", 1),
        ("… unnamed request held", "implicit_held", 1),
        ("Ambient Bench, right", "ambient", 1),
        ("AMI labelled, right", "ami", 1),
        ("AMI silent test, answered outright", "ami_silent_outright", 2),
        ("Pilot, anonymous, right", "pilot", 1),
        ("Demo lines, right", "demo", 1),
    ]
    names = list(models)
    lines = [
        f"# Student round 2 for agent-1x ({exp})",
        "",
        f"Teacher: `{TEACHER}`. `{RC02}` is rc0.2's agent-1x build. Speakers anonymous. Shares are `value (k/n)`.",
        "",
        "| | " + " | ".join(f"`{n}`" for n in names) + " |",
        "|---|" + "---|" * len(names),
    ]
    for label, key, digits in rows:
        lines.append(f"| {label} | " + " | ".join(_pct(models[n].get(key), digits) for n in names) + " |")
    lines += ["", "## Speed on agent-1x (0.5 vCPU, 1 GiB), one thread", ""]
    if speed:
        lines += [
            "Median ms per line through the demo's gate; the history is encoded first, untimed, as while the person talks.",
            "",
            "| Model | Build | Memory MB | Short | Full history | Full history, cold |",
            "|---|---|---|---|---|---|",
        ]
        for name, s in speed.items():
            lines.append(
                f"| `{name}` | {s.get('build', '')} | {s.get('memory', '')} | {s.get('short', '')} | {s.get('full', '')} | {s.get('cold', '')} |"
            )
    else:
        lines.append("Not measured.")
    lines += ["", "## The gate", ""]
    for name, g in gate.items():
        lines.append(f"- `{name}`: **{'ships' if g['ships'] else 'does not ship'}**. {g['why']}")
    if notes:
        lines += ["", "## Notes", ""] + [f"- {n}" for n in notes]
    return "\n".join(lines) + "\n"


@app.function(image=LT.image, cpu=0.25, memory=1024, timeout=14 * 3600, secrets=T._secrets())
def run(
    exp: str = "exp-055-side-round7",
    steps: str = "students,export,latency",
    shares: str = "0.25,0.5",
    seeds: str = "0,1",
    encoder: str = "ettin-32m",
) -> dict:
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
        "args": {"steps": steps, "shares": shares, "seeds": seeds, "encoder": encoder},
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
        arms = []  # (tag, share, seed)
        for share in [float(x) for x in shares.split(",") if x]:
            for seed in [int(x) for x in seeds.split(",") if x]:
                arms.append((f"r7po{round(100 * share):02d}", share, seed))
        students = {f"side-{tag}-{encoder}-s{seed}": (tag, share, seed) for tag, share, seed in arms}

        # 1. The students.
        if "students" in want:
            calls = {
                run_id: T.run.spawn(
                    f"{exp}-train-{tag}-s{seed}",
                    corpus=CORPUS,
                    encoders=encoder,
                    epochs=3,
                    seed=seed,
                    tag=tag,
                    teacher=TEACHER,
                    alpha=0.8,
                    arch="twotower",
                    people_only=share,
                    **TEST,
                )
                for run_id, (tag, share, seed) in students.items()
            }
            step("students", {k: "running" for k in calls})
            step(
                "students",
                {k: v.get("state", "done") if isinstance(v, dict) else "done" for k, v in wait(calls).items()},
            )

        # 2. Exports.
        exports = {run_id: f"{exp}-export-{LT._short(run_id)}" for run_id in students}
        if "export" in want:
            calls = {
                run_id: X.run.spawn(e, run_id)
                for run_id, e in exports.items()
                if r2.get_json(s3, T._model_key(run_id, "config.json")) is not None
            }
            step("export", {k: "running" for k in calls})
            step(
                "export",
                {
                    k: {x: v.get(x) for x in ("size_mb", "optimized", "error")} if isinstance(v, dict) else v
                    for k, v in wait(calls).items()
                },
            )

        # 3. Latency beside Jev and the rc0.2 student, in the same containers.
        latency_exp = f"{exp}-latency"
        if "latency" in want:
            ids = [RC02] + [i for i in exports if r2.get_json(s3, T._model_key(i, "export/config.json")) is not None]
            step("latency", "running")
            got = wait(
                {
                    "latency": LT.run.spawn(
                        latency_exp,
                        run_ids=",".join(ids),
                        profiles="agent-1x,agent-2x",
                        threads="1",
                        rounds=3,
                        jev=True,
                    )
                }
            )
            step("latency", got["latency"].get("state", "done") if isinstance(got["latency"], dict) else "done")

        # 4. Summary and the gate.
        save(stage="summary")
        models = {}
        for run_id in [TEACHER, RC02, *students]:
            card = r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json")
            if card:
                models[run_id] = _metrics(card)
        t = models.get(TEACHER) or {}
        jev_implicit = (t.get("jev_implicit_t") or {}).get("value") or JEV_IMPLICIT_T
        lat = r2.get_json(s3, f"{r2.PREFIX}/results/{latency_exp}/scorecard.json") or {}
        variants = [v for v in lat.get("variants") or [] if v.get("profile") == "agent-1x"]
        jev = next((v for v in variants if v.get("name") == "jev" and v.get("ok")), None)
        jev_ms = (jev or {}).get("full_window", {}).get("p50")
        speed = {}
        for run_id in [RC02, *students]:
            mine = [v for v in variants if v.get("run_id") == run_id and v.get("ok")]
            pick = next((v for v in mine if not v.get("int8")), None) or next(iter(mine), None)
            if not pick:
                continue
            speed[run_id] = {
                "build": "int8" if pick.get("int8") else "fp32",
                "memory": f"{pick.get('rss_mb_peak', 0):.0f}",
                "short": f"{pick['demo']['p50']:.0f}",
                "full": f"{pick['full_window']['p50']:.0f}",
                "cold": f"{pick['full_window_cold']['p50']:.0f}" if pick.get("full_window_cold") else "",
                "full_ms": pick["full_window"]["p50"],
            }
        if jev_ms is not None:
            speed["jev"] = {
                "build": "API",
                "full": f"{jev_ms:.0f}",
                "short": f"{jev['demo']['p50']:.0f}" if jev.get("demo") else "",
            }
        gate = {}
        for run_id in [RC02, *students]:  # rc0.2's build is gated too, for comparison
            m = models.get(run_id)
            if not m or not t:
                gate[run_id] = {"ships": False, "why": "not trained or not scored"}
                continue
            e = exports.get(run_id)
            p = ((r2.get_json(s3, f"{r2.PREFIX}/results/{e}/scorecard.json") or {}).get("parity") or {}) if e else {}
            parity_ok = not (p.get("rows") and p["decisions_same"] < 0.98 * p["rows"])
            gate[run_id] = gate_one(m, t, (speed.get(run_id) or {}).get("full_ms"), jev_ms, jev_implicit, parity_ok)
        card = {
            "exp": exp,
            "teacher": TEACHER,
            "models": models,
            "speed": speed,
            "gate": gate,
            "notes": notes,
            "finished_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        r2.put_json(s3, f"{out}/scorecard.json", card)
        r2.put_text(s3, f"{out}/report.md", _render(exp, models, speed, gate, notes))
        save(state="done", stage="done")
        return {"state": "done", "gate": gate}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
