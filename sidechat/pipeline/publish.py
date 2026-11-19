"""Publish a Sidechat model to the Hugging Face Hub: the ONNX export, the model card (hf/README.md)
and the rows it was trained on (train and dev, rebuilt exactly as the training job built them).

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.publish::run --exp exp-034-side-publish --run-id side-r3-ettin-150m-s0

`--subdir agent-1x` puts a second build in that folder (graphs, tokenizer, config, its own rows and
MANIFEST.json) and leaves the root files as they are; the card is always the root README.md.
`--tag rc0.2` tags the commit. The Hub repo is created private; make it public on the Hub when ready. Test-only sets (Duplex-MPE,
the Ambient Bench, AMI's labelled and held-out meetings) are never part of training, so never
uploaded. Writes runs/side/results/<exp>/: status.json, then scorecard.json (every file uploaded,
with its sha256) and report.md.
"""

from __future__ import annotations

import os
import pathlib

import modal

from sidechat.lib.r2 import R2_KEYS
from sidechat.pipeline.train import hf_cache
from sidechat.pipeline.train import image as train_image

APP_NAME = "waystone-side-publish"
ROOT = pathlib.Path(__file__).resolve().parents[2]
SECRET_KEYS = (*R2_KEYS, "HF_TOKEN")
DROP_TAGS = ("brief_ok", "brief_problems", "label_safe")  # the writer's own checks, not data


def _secrets() -> list:
    if not modal.is_local():
        return [modal.Secret.from_dict({})]
    if os.environ.get("MODAL_ENVIRONMENT") != "waystone":
        raise SystemExit("refusing: MODAL_ENVIRONMENT must be 'waystone'. Load .env first: set -a; . ./.env; set +a")
    missing = [k for k in SECRET_KEYS if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"refusing: {', '.join(missing)} not set. Load .env first: set -a; . ./.env; set +a")
    return [modal.Secret.from_dict({k: os.environ[k] for k in SECRET_KEYS})]


image = train_image.add_local_file(str(ROOT / "hf" / "README.md"), remote_path="/root/hf/README.md")
app = modal.App(APP_NAME)


@app.function(image=image, cpu=4.0, memory=16384, timeout=2 * 3600, secrets=_secrets(), volumes={"/cache": hf_cache})
def run(
    exp: str,
    run_id: str = "side-r3-ettin-150m-s0",
    repo: str = "pipecat-ai/sidechat",
    private: bool = True,
    subdir: str = "",
    tag: str = "",
) -> dict:
    import collections
    import gzip
    import hashlib
    import json
    import shutil
    import time
    import traceback
    from datetime import UTC, datetime

    from huggingface_hub import HfApi

    from sidechat.lib import r2
    from sidechat.pipeline.train import _corpus_rows

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    started = time.monotonic()
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {"run_id": run_id, "repo": repo, "private": private, "subdir": subdir, "tag": tag},
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    def sha(path: pathlib.Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for block in iter(lambda: f.read(1 << 20), b""):
                h.update(block)
        return h.hexdigest()

    try:
        cfg = r2.get_json(s3, f"models/side/{run_id}/config.json")
        top = pathlib.Path("/tmp/publish")
        shutil.rmtree(top, ignore_errors=True)
        folder = top / subdir if subdir else top
        (folder / "data").mkdir(parents=True)

        # 1. The training rows, built by the training job's own code.
        counts: dict = {}
        for split in ("train", "dev"):
            save(stage=f"building {split} rows from {cfg['corpus']}")
            rows = _corpus_rows(s3, cfg["corpus"], {split}, safe_only=True)
            with gzip.open(folder / "data" / f"{split}.jsonl.gz", "wt", encoding="utf-8") as f:
                for r in rows:
                    r["tags"] = {k: v for k, v in r["tags"].items() if k not in DROP_TAGS}
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
            counts[split] = {
                "rows": len(rows),
                "by_set": dict(collections.Counter(r["set"] for r in rows)),
                "by_respond": dict(collections.Counter(str(r["label"]["respond"]) for r in rows)),
            }
        if counts["train"]["rows"] != cfg.get("train_rows"):
            raise RuntimeError(
                f"rebuilt {counts['train']['rows']} train rows, the run trained on {cfg.get('train_rows')}"
            )

        # 2. The export and the card.
        save(stage="copying the export", rows=counts)
        export = r2.get_json(s3, f"models/side/{run_id}/export/config.json")
        graphs = ["context", "line"] if export.get("arch") == "twotower" else ["model"]
        names = [f"{g}{p}.onnx" for g in graphs for p in ("", "-int8")] + ["tokenizer.json", "config.json"]
        for name in names:
            try:
                s3.download_file(r2._bucket(), f"models/side/{run_id}/export/{name}", str(folder / name))
            except Exception:
                if name.endswith("-int8.onnx"):  # the int8 build is made only when it passes its gate
                    continue
                raise
        if export.get("arch") == "twotower":
            tok = json.loads((folder / "tokenizer.json").read_text())
            if tok.get("truncation") or tok.get("padding"):
                raise RuntimeError("a two-tower tokenizer.json must not carry truncation or padding (exp-036)")
        shutil.copy("/root/hf/README.md", top / "README.md")
        files = {
            p.relative_to(folder).as_posix(): {"bytes": p.stat().st_size, "sha256": sha(p)}
            for p in sorted(folder.rglob("*"))
            if p.is_file()
        }
        (folder / "MANIFEST.json").write_text(
            json.dumps({"run_id": run_id, "files": files, "rows": counts}, indent=1) + "\n"
        )

        # 3. The Hub.
        save(stage=f"uploading to {repo}")
        api = HfApi(token=os.environ["HF_TOKEN"])
        api.create_repo(repo, repo_type="model", private=private, exist_ok=True)
        where = f"{subdir}/: " if subdir else ""
        commit = api.upload_folder(
            folder_path=str(top),
            repo_id=repo,
            repo_type="model",
            commit_message=f"{where}{run_id}: ONNX export, model card and training rows",
        )
        if tag:
            save(stage=f"tagging {tag}")
            api.create_tag(repo, tag=tag, revision=commit.oid, tag_message=f"{tag}: {where}{run_id}")
        card = {
            "exp": exp,
            "run_id": run_id,
            "repo": repo,
            "private": private,
            "subdir": subdir,
            "tag": tag,
            "commit": commit.oid,
            "files": files,
            "rows": counts,
            "finished_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        r2.put_json(s3, f"{out}/scorecard.json", card)
        lines = [
            f"# {exp}: {run_id} to {repo}" + (f"/{subdir}" if subdir else ""),
            "",
            f"Commit `{commit.oid}`" + (f", tagged `{tag}`" if tag else "") + f", private: {private}.",
            "",
            "| File | Bytes | sha256 |",
            "|---|---|---|",
        ]
        lines += [f"| {k} | {v['bytes']:,} | `{v['sha256'][:16]}` |" for k, v in files.items()]
        lines += ["", f"Rows: train {counts['train']['rows']:,}, dev {counts['dev']['rows']:,}.", ""]
        r2.put_text(s3, f"{out}/report.md", "\n".join(lines))
        save(state="done", stage="done", commit=commit.oid)
        return {"state": "done", "commit": commit.oid}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
