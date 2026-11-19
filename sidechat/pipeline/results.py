"""See how a job is doing, and fetch its results once it is done. Reads R2 only.

    set -a; . ./.env; set +a
    uv run python -m sidechat.pipeline.results exp-001-side-jev-baseline
    uv run python -m sidechat.pipeline.results exp-001-side-jev-baseline --report reports/2026-11-18-side-jev-baseline.md

While the job runs this prints its status. When it is done it also saves `scorecard.json`,
`report.md` and `status.json` into `experiments/<exp>/`, and the report to `--report` if given.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys

from sidechat.lib import r2

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("exp")
    ap.add_argument("--report", help="also save the report here, e.g. reports/2026-11-18-side-jev-baseline.md")
    args = ap.parse_args()

    s3 = r2.client()
    base = f"{r2.PREFIX}/results/{args.exp}"
    status = r2.get_json(s3, f"{base}/status.json")
    if status is None:
        print(f"{args.exp}: nothing in R2 yet. The job has not written its first status.")
        return 1

    jev = status.get("jev") or {}
    print(
        f"{args.exp}: {status['state']}, stage: {status.get('stage')}, {status.get('elapsed_s', 0)} s elapsed, updated {status.get('updated_at')}"
    )
    if status.get("sets"):
        print("  rows:", ", ".join(f"{k} {v:,}" for k, v in status["sets"].items()))
    if jev.get("requests"):
        print(
            f"  Jev: {jev.get('answered', 0):,} of {jev['requests']:,} answered ({jev.get('reused', 0):,} reused, {jev.get('failed', 0):,} failed), "
            f"{jev.get('input_tokens', 0):,} input tokens"
        )
    for member, p in (status.get("progress") or {}).items():
        print(
            f"  member {member}: {p.get('answered', 0):,} of {p.get('of', 0):,} answered ({p.get('reused', 0):,} reused, "
            f"{p.get('failed', 0):,} failed), about ${p.get('usd', 0):.2f}"
        )
    if status.get("forecast"):
        f = status["forecast"]
        what = f"{f['requests_to_ask']:,} requests" if "requests_to_ask" in f else "the remaining lines"
        print(f"  forecast: about ${f['usd']} for {what} (cap ${f['spend_cap_usd']})")
    if status.get("headline"):
        h = status["headline"]["majority_decision"]
        print(
            f"  majority agrees with the guide on {100 * h['value']:.1f}% ({h['k']}/{h['n']}); target met: {status['headline']['meets_target']}"
        )
    if status.get("reason"):
        print("  reason:", status["reason"])

    folder = ROOT / "experiments" / args.exp
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "status.json").write_text(json.dumps(status, indent=1) + "\n")
    if status["state"] != "done":
        return 0 if status["state"] == "running" else 2

    card = r2.get_bytes(s3, f"{base}/scorecard.json")
    report = r2.get_bytes(s3, f"{base}/report.md")
    (folder / "scorecard.json").write_bytes(card)
    (folder / "report.md").write_bytes(report)
    print(f"  saved experiments/{args.exp}/scorecard.json and report.md")
    run_args = status.get("args") or {}
    if not run_args.get("limit"):  # a trial run's manifests describe cut-down sets
        manifests = ROOT / "data" / "manifests"
        manifests.mkdir(parents=True, exist_ok=True)
        keys = {rows_id: f"{r2.PREFIX}/rows/{rows_id}/manifest.json" for rows_id in status.get("sets") or {}}
        if run_args.get("baseline_id"):
            keys[run_args["baseline_id"]] = f"{r2.PREFIX}/baselines/{run_args['baseline_id']}/manifest.json"
        if run_args.get("label_id"):
            keys[run_args["label_id"]] = f"{r2.PREFIX}/labels/{run_args['label_id']}/manifest.json"
        for name, key in keys.items():
            data = r2.get_bytes(s3, key)
            if data:
                (manifests / f"{name}.json").write_bytes(data)
        print(f"  saved {len(keys)} manifests to data/manifests/")
    if args.report:
        target = ROOT / args.report
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(report)
        print(f"  saved {args.report}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
