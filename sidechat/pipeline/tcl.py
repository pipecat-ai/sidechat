"""An independent test: TCL's Intelligent Wakeup (test split, text only), in one detached Modal job.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.tcl::run --exp exp-063-side-tcl-wakeup

    uv run python -m sidechat.pipeline.results exp-063-side-tcl-wakeup

Steps:

    fetch    the test split's five Parquet files at v1.0.1, keeping only the text columns, into R2
             (runs/side/sources/tcl-wakeup-v1.0.1/: private, never git or the Hub, SD-27)
    jev      Jev on every person's turn, speakers named and anonymous (`sidechat/pipeline/baseline.py`)
    score    rc0.3's and rc0.2's builds on the same rows, at their own thresholds (`train.score_sets`)
    summary  runs/side/results/<exp>/scorecard.json and report.md

The summary gives TCL's own measures, with an answer now as the accept (precision, recall, F1, false
accepts per hour of recording), the same with a hold counted as an accept, and each kind of line
(`sidechat/sources/tcl_wakeup.py`): answered now, held, or left alone. Nothing is tuned on this set.
"""

from __future__ import annotations

import os

import modal

from sidechat.lib.r2 import R2_KEYS
from sidechat.pipeline import baseline as B
from sidechat.pipeline import stt_ami as S
from sidechat.pipeline import train as T
from sidechat.sources import tcl_wakeup as TW

APP_NAME = "waystone-side-tcl"
app = modal.App(APP_NAME)
for other in (B.app, T.app):
    app.include(other)

MODELS = {
    "side-r9-ettin-150m-s1": "rc0.3 default (150M)",
    "side-r9tt-ettin-32m-s1": "rc0.3 agent-1x (32M)",
    "side-r3-ettin-150m-s0": "rc0.2 default (150M)",
    "side-r6ttr3t-ettin-32m-s0": "rc0.2 agent-1x (32M)",
}
CONDITIONS = ("named", "anonymous")
SETS = "tcl,tcl@anonymous"
KINDS = TW.KINDS

# TCL's own audio model on the same 3,647 turns, trained on TCL's train split: its repo's
# experiments/audio_experiments/int_wakeup-whisper_base-ctx20-ft4-results.md, ensemble at 0.90.
TCL_AUDIO = {
    "precision": 0.931,
    "recall": 0.853,
    "f1": 0.890,
    "fa_per_hour": 2.83,
    "direct": {"k": 148, "n": 158},
    "contextual": {"k": 107, "n": 141},
    "false_accepts": {"k": 19, "n": 3348},
}


def _secrets() -> list:
    if not modal.is_local():
        return [modal.Secret.from_dict({})]
    if os.environ.get("MODAL_ENVIRONMENT") != "waystone":
        raise SystemExit("refusing: MODAL_ENVIRONMENT must be 'waystone'. Load .env first: set -a; . ./.env; set +a")
    missing = [k for k in R2_KEYS if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"refusing: {', '.join(missing)} not set. Load .env first: set -a; . ./.env; set +a")
    return [modal.Secret.from_dict({k: os.environ[k] for k in R2_KEYS})]


def fetch(s3) -> dict:
    """The test split's text columns at the pinned revision, into R2. The audio column is not read."""
    import hashlib
    from datetime import UTC, datetime

    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download

    from sidechat.lib import r2

    sessions, files = [], {}
    for f in TW.FILES:
        local = hf_hub_download(TW.REPO, f, repo_type="dataset", revision=TW.REVISION)
        h = hashlib.sha256()
        with open(local, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        files[f] = h.hexdigest()
        sessions += pq.read_table(local, columns=list(TW.COLUMNS)).to_pylist()
        os.remove(local)
    if {s["split"] for s in sessions} != {TW.SPLIT}:
        raise ValueError(f"expected only the test split, got {sorted({s['split'] for s in sessions})}")
    base = f"{r2.PREFIX}/{TW.TEXT_PREFIX}"
    manifest = {
        "repo": TW.REPO,
        "revision": TW.REVISION,
        "split": TW.SPLIT,
        "files": files,
        "columns": list(TW.COLUMNS),
        "sessions": len(sessions),
        "turns": sum(len(s["turns"]) for s in sessions),
        "hours": round(sum(s["duration_seconds"] for s in sessions) / 3600, 3),
        "licence": TW.LICENCE,
        "use": TW.USE,
        "sha256": r2.put_jsonl(s3, f"{base}/test.jsonl", sessions),
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    r2.put_json(s3, f"{base}/manifest.json", manifest)
    return manifest


def _pct(x: dict | None, digits: int = 1) -> str:
    if not x or x.get("value") is None:
        return "n/a"
    lo, hi = x["ci95"]
    return f"{100 * x['value']:.{digits}f}% ({x['k']:,}/{x['n']:,}; {100 * lo:.{digits}f} to {100 * hi:.{digits}f})"


def _render(exp: str, card: dict) -> str:
    t = card["text"]
    lines = [
        f"# TCL Intelligent Wakeup, test split, text only ({exp})",
        "",
        (
            f"{t['sessions']} sessions, {card['rows']['named']:,} people's turns, {t['hours']} hours of recording. "
            "Sidechat's builds at their own thresholds, Jev as the demo asks it. An accept is an answer now; "
            "a hold is counted apart. Nothing was tuned on this set. Shares are `value (k/n; 95% interval)`."
        ),
        "",
        (
            "TCL's own audio model, trained on TCL's train split, from its repo: precision 0.931, recall 0.853, "
            "F1 0.890, 2.83 false accepts an hour of recording; direct 148/158, contextual 107/141, "
            "false accepts 19/3,348."
        ),
    ]
    for cond in CONDITIONS:
        table = card["table"][cond]
        lines += [
            "",
            f"## Speakers {cond}",
            "",
            (
                "| | precision | recall | F1 | FA/hour | direct, now | contextual, now | contextual, held | "
                "others, answered | others, held |"
            ),
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        for name, m in table.items():
            now = m["now"]
            others_held = sum(m[k]["wait"]["k"] for k in KINDS[2:])
            others_n = sum(m[k]["wait"]["n"] for k in KINDS[2:])
            lines.append(
                f"| {name} | {now['precision']} | {now['recall']['value']} | {now['f1']} | {now['fa_per_hour']} | "
                f"{_pct(m['direct']['respond'])} | {_pct(m['contextual']['respond'])} | "
                f"{_pct(m['contextual']['wait'])} | {_pct(now['false_accepts'], 2)} | "
                f"{100 * others_held / max(1, others_n):.2f}% ({others_held:,}) |"
            )
        lines += ["", "By kind, answered now / held / left alone:", ""]
        lines += ["| | " + " | ".join(KINDS) + " |", "|---|" + "---|" * len(KINDS)]
        for name, m in table.items():
            cells = [
                " / ".join(
                    f"{100 * m[k][x]['value']:.1f}" if m[k][x]["value"] is not None else "n/a"
                    for x in ("respond", "wait", "ignore")
                )
                + f" (n {m[k]['respond']['n']})"
                for k in KINDS
            ]
            lines.append(f"| {name} | " + " | ".join(cells) + " |")
        lines += ["", "With a hold counted as an accept:", ""]
        lines += ["| | precision | recall | F1 | FA/hour |", "|---|---|---|---|---|"]
        for name, m in table.items():
            x = m["now_or_held"]
            lines.append(f"| {name} | {x['precision']} | {x['recall']['value']} | {x['f1']} | {x['fa_per_hour']} |")
    return "\n".join(lines) + "\n"


def summary(s3, exp: str) -> dict:
    from datetime import UTC, datetime

    from sidechat import conditions
    from sidechat.baselines import jev_demo
    from sidechat.lib import r2
    from sidechat.train import evaluate as E

    text = r2.get_json(s3, f"{r2.PREFIX}/{TW.TEXT_PREFIX}/manifest.json") or {}
    base = TW.convert(r2.get_jsonl(s3, f"{r2.PREFIX}/{TW.TEXT_PREFIX}/test.jsonl") or [])
    table: dict = {}
    counts: dict = {}
    for cond in CONDITIONS:
        rows = [conditions.apply(r, cond) for r in base]
        rows_id = rows[0]["set"]
        counts[cond] = len(rows)
        systems: dict = {}
        jev = r2.get_jsonl(s3, f"{r2.PREFIX}/baselines/jev-demo-0.1/scores/{rows_id}.jsonl") or []
        if jev:
            dec = {x["row_id"]: jev_demo.decision(x["addressed"], x["question"]) for x in jev}
            systems["Jev"] = TW.measures(rows, dec, text.get("hours", 0))
        for run_id, label in MODELS.items():
            t = (r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json") or {}).get("thresholds")
            preds = r2.get_jsonl(s3, f"{r2.PREFIX}/predictions/{run_id}/{rows_id}.jsonl") or []
            if t and preds:
                systems[label] = TW.measures(rows, {p["row_id"]: E.decide(p, t) for p in preds}, text.get("hours", 0))
        table[cond] = systems
    card = {
        "exp": exp,
        "text": text,
        "rows": counts,
        "models": MODELS,
        "tcl_audio_model": TCL_AUDIO,
        "table": table,
        "finished_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    out = f"{r2.PREFIX}/results/{exp}"
    r2.put_json(s3, f"{out}/scorecard.json", card)
    r2.put_text(s3, f"{out}/report.md", _render(exp, card))
    return card


@app.function(  # it launches Jev and the scoring, so it is not preempted (sidechat/lib/resume.py)
    image=S.image, cpu=1.0, memory=4096, timeout=6 * 3600, secrets=_secrets(), nonpreemptible=True
)
def run(exp: str = "exp-063-side-tcl-wakeup", steps: str = "fetch,jev,score,summary", jev_cap_usd: float = 3.0) -> dict:
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
        "args": {"steps": steps, "jev_cap_usd": jev_cap_usd},
        "steps": {},
    }
    kept = resume.carried(r2.get_json(s3, f"{out}/status.json"), status["args"])
    if kept:
        status.update(started_at=kept["started_at"], steps=kept["steps"], restarts=kept["restarts"])
        status["restarted_at"] = datetime.now(UTC).isoformat(timespec="seconds")
    status["calls"] = kept.get("calls", {})

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

    try:
        save()
        if "fetch" in want and "fetch" not in status["steps"]:
            save(stage="fetching the test split's text")
            m = fetch(s3)
            status["steps"]["fetch"] = {"sessions": m["sessions"], "turns": m["turns"], "hours": m["hours"]}
            save()
        calls = {}
        if "jev" in want and "jev" not in status["steps"]:
            calls["jev"] = spawner.spawn("jev", B.run, f"{exp}-jev", sets=SETS, spend_cap_usd=jev_cap_usd)
        if "score" in want and "score" not in status["steps"]:
            for run_id in MODELS:
                calls[run_id] = spawner.spawn(f"score/{run_id}", T.score_sets, run_id, SETS)
        if calls:
            save(stage="jev and scoring")
            got = wait(calls)
            done = {k: (v.get("state") or "done") if isinstance(v, dict) else "done" for k, v in got.items()}
            if "jev" in got:
                status["steps"]["jev"] = done.pop("jev")
            if done:
                status["steps"]["score"] = done
            save()
        if "summary" in want:
            save(stage="summary")
            summary(s3, exp)
        save(state="done", stage="done")
        return {"state": "done"}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
