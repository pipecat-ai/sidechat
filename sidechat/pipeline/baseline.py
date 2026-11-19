"""Phase 0 baseline job: Jev, asked exactly as the daily-audience demo asks it, on every Phase 0 set.

Runs detached on Modal, so nothing depends on the machine that started it:

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.baseline::run --exp exp-001-side-jev-baseline

Then, from any machine with the `.env`:

    uv run python -m sidechat.pipeline.results exp-001-side-jev-baseline

One remote function does the whole chain and writes each step to R2:

    1. build the rows of each set (Hugging Face at pinned revisions, and data/suites/)
         -> runs/side/rows/<rows_id>/rows.jsonl, manifest.json
    2. ask Jev, resumably
         -> runs/side/baselines/<baseline_id>/parts/*.jsonl, scores/<rows_id>.jsonl
    3. score
         -> runs/side/results/<exp>/scorecard.json, report.md
    status.json in that folder is rewritten as the job goes.

Stop it with `uv run modal app stop waystone-side-baseline`. Starting it again picks up where it
stopped: answers already stored are not asked for again.
"""

from __future__ import annotations

import os
import pathlib

import modal

from sidechat.lib.r2 import R2_KEYS

APP_NAME = "waystone-side-baseline"
ROOT = pathlib.Path(__file__).resolve().parents[2]  # the repo here; /root inside the container
SECRET_KEYS = (*R2_KEYS, "JEV_API_KEY")


def _secrets() -> list:
    """Built from the environment at launch, as Audience's jobs do. Nothing is stored on Modal."""
    if not modal.is_local():
        return [modal.Secret.from_dict({})]
    if os.environ.get("MODAL_ENVIRONMENT") != "waystone":
        raise SystemExit("refusing: MODAL_ENVIRONMENT must be 'waystone'. Load .env first: set -a; . ./.env; set +a")
    missing = [k for k in SECRET_KEYS if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"refusing: {', '.join(missing)} not set. Load .env first: set -a; . ./.env; set +a")
    return [modal.Secret.from_dict({k: os.environ[k] for k in SECRET_KEYS})]


image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install(
        "pipecat-ai[typesafe]==1.16.0",  # the demo's version: the same Jev client and default model
        "boto3>=1.40",
        "pydantic>=2.9",
        "pyyaml>=6.0",
        "huggingface-hub>=0.30",
    )
    .add_local_python_source("sidechat")
    .add_local_dir(str(ROOT / "data" / "suites"), remote_path="/root/data/suites")
)

app = modal.App(APP_NAME)


@app.function(
    image=image,
    cpu=2.0,
    memory=4096,
    timeout=4 * 3600,
    secrets=_secrets(),
    retries=modal.Retries(max_retries=2, backoff_coefficient=1.0, initial_delay=30.0),
)
def run(
    exp: str,
    sets: str = "demo,ambient,duplex",
    baseline_id: str = "jev-demo-0.1",
    jev_model: str = "jev-1.13.0",
    concurrency: int = 12,
    spend_cap_usd: float = 5.0,
    usd_per_m_input: float = 0.042,
    limit: int = 0,
) -> dict:
    """Score Jev on `sets` (comma-separated: demo, pilot, ambient, duplex).

    `limit` keeps the first conversations of each set, for a trial run. Use a separate `exp` and
    `baseline_id` for trials so they never mix with the real baseline.
    """
    import asyncio
    import time
    import traceback
    from datetime import UTC, datetime

    from sidechat.baselines import jev_demo, jev_run
    from sidechat.lib import r2
    from sidechat.pipeline import scorecard
    from sidechat.schema import SidechatRequest
    from sidechat.sources import build

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    started = time.monotonic()
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {
            "sets": sets,
            "baseline_id": baseline_id,
            "jev_model": jev_model,
            "concurrency": concurrency,
            "spend_cap_usd": spend_cap_usd,
            "limit": limit,
        },
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    try:
        # 1. Rows.
        built: dict[str, dict] = {}
        for which in [x.strip() for x in sets.split(",") if x.strip()]:
            save(stage=f"building rows: {which}")
            rows, manifest, extras = build.build_rows(which, limit)
            rows_id = manifest["rows_id"]
            manifest["sha256"] = r2.put_jsonl(s3, f"{r2.PREFIX}/rows/{rows_id}/rows.jsonl", rows)
            manifest["r2_key"] = f"{r2.PREFIX}/rows/{rows_id}/rows.jsonl"
            r2.put_json(s3, f"{r2.PREFIX}/rows/{rows_id}/manifest.json", manifest)
            built[rows_id] = {"rows": rows, "manifest": manifest, "extras": extras}
        save(sets={k: v["manifest"]["rows"] for k, v in built.items()})

        # 2. Jev. Rows that would send the same request share one answer.
        key_of: dict[str, str] = {}
        requests: dict[str, SidechatRequest] = {}
        for s in built.values():
            for r in s["rows"]:
                req = SidechatRequest(**r["request"])
                k = jev_demo.key(jev_model, req)
                key_of[r["row_id"]] = k
                requests.setdefault(k, req)

        def progress(usage: dict, forecast: dict | None) -> None:
            done = usage["reused"] + usage["asked"] - usage["failed"]
            save(stage="asking Jev", jev={**usage, "answered": done}, forecast=forecast)

        save(stage="asking Jev", jev={"requests": len(requests)})
        answers, usage = asyncio.run(
            jev_run.score(
                s3,
                baseline_id,
                jev_model,
                requests,
                concurrency=concurrency,
                spend_cap_usd=spend_cap_usd,
                usd_per_m_input=usd_per_m_input,
                on_progress=progress,
            )
        )
        base = f"{r2.PREFIX}/baselines/{baseline_id}"
        for rows_id, s in built.items():
            s["scores"] = {
                r["row_id"]: {x: answers[key_of[r["row_id"]]][x] for x in ("addressed", "question", "ms")}
                for r in s["rows"]
                if key_of[r["row_id"]] in answers
            }
            r2.put_jsonl(s3, f"{base}/scores/{rows_id}.jsonl", [{"row_id": i, **v} for i, v in s["scores"].items()])
        r2.put_json(
            s3,
            f"{base}/manifest.json",
            {
                "baseline_id": baseline_id,
                "model": jev_model,
                "prompt_sha": jev_demo.prompt_sha(),
                "demo": {"repo": jev_demo.DEMO_REPO, "commit": jev_demo.DEMO_COMMIT, "pipecat": jev_demo.DEMO_PIPECAT},
                "thresholds": {"respond": jev_demo.RESPOND_THRESHOLD, "question": jev_demo.QUESTION_THRESHOLD},
                "last_run": {"exp": exp, **usage},
                "sets": sorted(built),
            },
        )

        # 3. Scorecard and report.
        save(stage="scoring")
        meta = {
            "exp": exp,
            "baseline_id": baseline_id,
            "jev_model": jev_model,
            "prompt_sha": jev_demo.prompt_sha(),
            "concurrency": concurrency,
            "limit": limit or None,
            "usage": usage,
            "finished_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        card = scorecard.build(built, meta)
        r2.put_json(s3, f"{out}/scorecard.json", card)
        r2.put_text(s3, f"{out}/report.md", scorecard.render(card))
        save(state="done", stage="done", jev={**usage, "answered": len(answers)})
        return {"state": "done", "results": out, "usage": usage}
    except jev_run.Stopped as e:
        save(state="stopped", reason=str(e))
        return {"state": "stopped", "reason": str(e)}
    except Exception as e:  # recorded where the results would be, then raised so Modal retries
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
