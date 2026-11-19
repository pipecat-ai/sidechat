"""Latency and memory of Sidechat beside Jev, on containers shaped like Pipecat Cloud's agent profiles.

The daily-audience bot deploys on `agent-1x` (0.5 vCPU, 1 GB). Each variant here runs in its own
Modal container with that CPU and memory as hard limits (and again for `agent-2x` and `agent-3x`),
so a build that does not fit is killed as it would be in the bot. Inside, `scripts/bench_latency.py`
asks each line through the demo's own gate (`AddressingMonitor.classify`, copied into the image
from ~/Sites/daily-audience, unedited) and times it by its `classifier_ms`, exactly as on the Mac.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.latency::run --exp exp-033-side-latency-cloud

Then:

    uv run python -m sidechat.pipeline.results exp-033-side-latency-cloud

Writes runs/side/results/<exp>/: variants/<profile>/<variant>.json as each finishes, then
scorecard.json and report.md. status.json is rewritten as the job goes. The bench process holds
only the classifier and Pipecat; the real bot also holds the transport, VAD, smart-turn and its
service clients in the same memory and on the same CPU.
"""

from __future__ import annotations

import pathlib

import modal

from sidechat.pipeline.baseline import _secrets

APP_NAME = "waystone-side-latency"
ROOT = pathlib.Path(__file__).resolve().parents[2]
DEMO = pathlib.Path.home() / "Sites" / "daily-audience" / "server"

# Pipecat Cloud's agent profiles (docs: pipecat-cloud/fundamentals/deploy, "Agent Profiles").
PROFILES = {"agent-1x": (0.5, 1024), "agent-2x": (1.0, 2048), "agent-3x": (1.5, 3072)}

image = (
    modal.Image.debian_slim(python_version="3.12")  # the workspace's builder stops at 3.12; the demo runs 3.13
    .uv_pip_install(
        "pipecat-ai[typesafe]==1.16.0",  # the demo's version
        "onnxruntime==1.32.0",  # as in the demo's environment
        "tokenizers==0.23.3",
        "boto3>=1.40",
        "pydantic>=2.9",
    )
    .add_local_python_source("sidechat")
    .add_local_file(str(DEMO / "addressing.py"), remote_path="/root/demo/addressing.py")
    .add_local_file(str(ROOT / "scripts" / "try_in_demo.py"), remote_path="/root/scripts/try_in_demo.py")
    .add_local_file(str(ROOT / "scripts" / "bench_latency.py"), remote_path="/root/scripts/bench_latency.py")
)

app = modal.App(APP_NAME)


def _bench(spec: dict) -> dict:
    """Run one variant in a child process, so its memory is measured alone and a kill is caught."""
    import json
    import os
    import subprocess
    import sys
    import time

    from sidechat.lib import r2

    s3 = r2.client()
    started = time.monotonic()
    out = {**spec, "region": os.environ.get("MODAL_REGION"), "cloud": os.environ.get("MODAL_CLOUD_PROVIDER")}
    cmd = [sys.executable, "/root/scripts/bench_latency.py", spec["which"]]
    if spec["which"] == "sidechat":
        folder = pathlib.Path("/tmp/models") / spec["run_id"]
        folder.mkdir(parents=True, exist_ok=True)
        graphs = [f"{g}-int8.onnx" if spec["int8"] else f"{g}.onnx" for g in spec.get("graphs", ["model"])]
        for name in ("config.json", "tokenizer.json", *graphs):  # streamed to disk, never held in memory
            s3.download_file(r2._bucket(), f"models/side/{spec['run_id']}/export/{name}", str(folder / name))
        cmd += [str(folder), "--threads", str(spec["threads"])] + (["--int8"] if spec["int8"] else [])
    cmd += ["--rounds", str(spec["rounds"])]  # options after the model path: argparse takes positionals first
    env = {**os.environ, "SIDECHAT_DEMO_DIR": "/root/demo", "PYTHONPATH": "/root"}
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd="/root", timeout=1500, check=False)
    lines = [x for x in proc.stdout.splitlines() if x.startswith("{")]
    if proc.returncode == 0 and lines:
        out |= {"ok": True, **json.loads(lines[-1])}
    else:
        out |= {
            "ok": False,
            "returncode": proc.returncode,
            "killed": proc.returncode in (-9, 137),
            "stderr_tail": proc.stderr[-1500:],
        }
    out["elapsed_s"] = round(time.monotonic() - started, 1)
    r2.put_json(s3, f"{r2.PREFIX}/results/{spec['exp']}/variants/{spec['profile']}/{spec['name']}.json", out)
    return out


_kw = {"image": image, "timeout": 1800, "secrets": _secrets()}


@app.function(cpu=(0.5, 0.5), memory=(1024, 1024), **_kw)
def bench_1x(spec: dict) -> dict:
    return _bench(spec)


@app.function(cpu=(1.0, 1.0), memory=(2048, 2048), **_kw)
def bench_2x(spec: dict) -> dict:
    return _bench(spec)


@app.function(cpu=(1.5, 1.5), memory=(3072, 3072), **_kw)
def bench_3x(spec: dict) -> dict:
    return _bench(spec)


BENCH = {"agent-1x": bench_1x, "agent-2x": bench_2x, "agent-3x": bench_3x}


def _short(run_id: str) -> str:
    """side-r3-ettin-150m-s0 -> r3-150m."""
    parts = run_id.split("-")
    return f"{parts[1]}-{parts[3]}" if len(parts) >= 4 else run_id


def _render(exp: str, results: list[dict], run_ids: list[str]) -> str:
    def cell(r: dict, shape: str) -> str:
        s = r.get(shape) or {}
        return f"{s['p50']:.0f} / {s['p90']:.0f} / {s['p99']:.0f}" if s else ""

    any_ok = next((r for r in results if r.get("ok")), {})
    lines = [
        f"# Latency on Pipecat Cloud-shaped containers ({exp})",
        "",
        (
            f"CPU: {any_ok.get('cpu', '?')}; Modal region {any_ok.get('region') or '?'} ({any_ok.get('cloud') or '?'}). "
            "Each variant ran alone in a container with the profile's CPU and memory as hard limits. Times are "
            "the demo's `classifier_ms` (p50 / p90 / p99, ms) over its 33 sample lines: \"demo\" as written "
            "(0 to 2 earlier lines), \"full window\" after 8 earlier lines. Memory is the bench process's peak "
            "resident size (Python, Pipecat and the classifier, nothing else of the bot). A two-tower "
            "model's history is encoded first, untimed, as it would be while the person talks; its cold time "
            "(both towers) and the history encoding are shown apart. \"Beats Jev\" compares the full-window "
            "median with Jev's in the same profile."
        ),
        "",
        f"Models: {', '.join(run_ids)}.",
        "",
    ]
    for profile, (cpu, mem) in PROFILES.items():
        rows = [r for r in results if r["profile"] == profile]
        if not rows:
            continue
        jev = next((r for r in rows if r["name"] == "jev" and r.get("ok")), None)
        jev_full = (jev or {}).get("full_window", {}).get("p50")
        lines += [
            f"## {profile}: {cpu} vCPU, {mem} MiB",
            "",
            (
                "| Variant | Threads | Memory MB | Load s | First line ms | demo p50 / p90 / p99 | full window p50 / p90 / p99 "
                "| full window cold p50 | history encode p50 | Beats Jev | Lines |"
            ),
            "|---|---|---|---|---|---|---|---|---|---|---|",
        ]
        for r in rows:
            if not r.get("ok"):
                why = "killed (out of memory)" if r.get("killed") else f"failed (exit {r.get('returncode', r.get('error', '?'))})"
                lines.append(f"| {r['name']} | {r.get('threads', '')} | {why} | | | | | | | | |")
                continue
            n = (r.get("demo") or {}).get("n", 0) + (r.get("full_window") or {}).get("n", 0)
            cold = (r.get("full_window_cold") or {}).get("p50")
            enc = (r.get("full_window_history_encode") or {}).get("p50")
            full = (r.get("full_window") or {}).get("p50")
            beats = "" if r["name"] == "jev" or jev_full is None or full is None else ("yes" if full < jev_full else "no")
            lines.append(
                f"| {r['name']} | {r.get('threads', '')} | {r.get('rss_mb_peak', 0):.0f} | {r.get('load_s', 0):.2f} | "
                f"{r.get('first_line_ms', 0):.0f} | {cell(r, 'demo')} | {cell(r, 'full_window')} | "
                f"{'' if cold is None else f'{cold:.0f}'} | {'' if enc is None else f'{enc:.0f}'} | {beats} | {n} |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


@app.function(name="latency_run", image=image, cpu=0.25, memory=512, timeout=3600, secrets=_secrets())
def run(
    exp: str,
    run_ids: str = "side-r3-ettin-150m-s0,side-r1-ettin-68m-s0",
    profiles: str = "agent-1x,agent-2x,agent-3x",
    threads: str = "1,2",
    rounds: int = 3,
    jev: bool = True,
) -> dict:
    """Bench every model build at each thread count on each profile, plus Jev once per profile."""
    import time
    import traceback
    from datetime import UTC, datetime

    from sidechat.lib import r2

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    started = time.monotonic()
    ids = [x.strip() for x in run_ids.split(",") if x.strip()]
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {"run_ids": run_ids, "profiles": profiles, "threads": threads, "rounds": rounds, "jev": jev},
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    try:
        builds = []
        for run_id in ids:
            keys = {o["Key"].rsplit("/", 1)[-1] for o in r2.list_keys(s3, f"models/side/{run_id}/export/")}
            cfg = r2.get_json(s3, f"models/side/{run_id}/export/config.json") or {}
            graphs = ["context", "line"] if cfg.get("arch") == "twotower" else ["model"]
            for int8 in (False, True):
                if all((f"{g}-int8.onnx" if int8 else f"{g}.onnx") in keys for g in graphs):
                    builds.append((run_id, int8, graphs))
        specs = []
        for profile in [p.strip() for p in profiles.split(",") if p.strip()]:
            for run_id, int8, graphs in builds:
                for t in [int(x) for x in threads.split(",") if x.strip()]:
                    name = f"{_short(run_id)}-{'int8' if int8 else 'fp32'}-t{t}"
                    specs.append({"exp": exp, "profile": profile, "name": name, "which": "sidechat", "run_id": run_id,
                                  "int8": int8, "threads": t, "rounds": rounds, "graphs": graphs})
            if jev:
                specs.append({"exp": exp, "profile": profile, "name": "jev", "which": "jev", "rounds": 2})
        save(stage=f"benching {len(specs)} variants", variants=len(specs))

        calls = [(s, BENCH[s["profile"]].spawn(s)) for s in specs]
        results = []
        for s, call in calls:
            try:
                results.append(call.get())
            except Exception as e:  # noqa: BLE001 - the container itself died (most likely out of memory); record it and go on
                results.append({**s, "ok": False, "killed": "memory" in str(e).lower(), "error": f"{type(e).__name__}: {e}"[:500]})
            save(stage=f"benching {len(specs)} variants", done=len(results))

        card = {"exp": exp, "profiles": PROFILES, "run_ids": ids, "variants": results,
                "finished_at": datetime.now(UTC).isoformat(timespec="seconds")}
        r2.put_json(s3, f"{out}/scorecard.json", card)
        r2.put_text(s3, f"{out}/report.md", _render(exp, results, ids))
        failed = sum(1 for r in results if not r.get("ok"))
        save(state="done", stage="done", done=len(results), failed=failed)
        return {"state": "done", "results": out, "failed": failed}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
