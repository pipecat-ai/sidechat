"""Publish a Sidechat model to the Hugging Face Hub: the ONNX export and the model card (hf/README.md).

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.publish::run --exp <exp> --run-id side-r9-ettin-150m-s1

`--subdir agent-1x` puts a second build in that folder (graphs, tokenizer, config and
MANIFEST.json) and leaves the root files as they are; the card is always the root README.md.
`--tag rc0.3.1` tags the commit. The Hub repo is created private; make it public on the Hub when
ready. Training data is not uploaded here: our own is the dataset `pipecat-ai/sidechat-gen`
(`sidechat/pipeline/dataset.py`). Writes runs/side/results/<exp>/: status.json, then
scorecard.json (every file uploaded, with its sha256) and report.md.

`card` publishes the card alone, and takes training rows an earlier release left in the repo out.
`--message` is the commit's message on the Hub:

    uv run modal run --detach -m sidechat.pipeline.publish::card --exp <exp> --message "Model card: <what changed>"
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
    import hashlib
    import json
    import shutil
    import time
    import traceback
    from datetime import UTC, datetime

    from huggingface_hub import HfApi

    from sidechat.lib import r2

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
        top = pathlib.Path("/tmp/publish")
        shutil.rmtree(top, ignore_errors=True)
        folder = top / subdir if subdir else top
        folder.mkdir(parents=True)

        # 1. The export and the card.
        save(stage="copying the export")
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
        (folder / "MANIFEST.json").write_text(json.dumps({"run_id": run_id, "files": files}, indent=1) + "\n")

        # 2. The Hub.
        save(stage=f"uploading to {repo}")
        api = HfApi(token=os.environ["HF_TOKEN"])
        api.create_repo(repo, repo_type="model", private=private, exist_ok=True)
        where = f"{subdir}/: " if subdir else ""
        # Graphs an earlier build left in this folder that this one does not ship (an int8 build
        # that failed its check this time) go in the same commit, so no folder mixes two builds.
        prefix = f"{subdir}/" if subdir else ""
        stale = [
            f
            for f in api.list_repo_files(repo)
            if f.startswith(prefix)
            and "/" not in f[len(prefix) :]
            and f.endswith(".onnx")
            and f[len(prefix) :] not in files
        ]
        commit = api.upload_folder(
            folder_path=str(top),
            repo_id=repo,
            repo_type="model",
            commit_message=f"{where}{run_id}: ONNX export and model card",
            delete_patterns=stale or None,
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
            "removed": stale,
            "files": files,
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
        if stale:
            lines += ["", "Removed (an earlier build's graphs this one does not ship): " + ", ".join(stale)]
        lines += [""]
        r2.put_text(s3, f"{out}/report.md", "\n".join(lines))
        save(state="done", stage="done", commit=commit.oid)
        return {"state": "done", "commit": commit.oid}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise


@app.function(image=image, cpu=1.0, memory=2048, timeout=1800, secrets=_secrets())
def card(exp: str, repo: str = "pipecat-ai/sidechat", folders: str = ",agent-1x", message: str = "Model card") -> dict:
    """Publish the model card alone, in one commit that also takes the training rows out of each
    build's folder (`data/`) and its MANIFEST.json. The models' files are not touched."""
    import hashlib
    import json
    import time
    import traceback
    from datetime import UTC, datetime

    from huggingface_hub import CommitOperationAdd, CommitOperationDelete, HfApi, hf_hub_download

    from sidechat.lib import r2

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    started = time.monotonic()
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {"repo": repo, "folders": folders, "message": message},
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    try:
        api = HfApi(token=os.environ["HF_TOKEN"])
        before = api.repo_info(repo).sha
        present = set(api.list_repo_files(repo))
        readme = pathlib.Path("/root/hf/README.md").read_bytes()
        ops: list = [CommitOperationAdd(path_in_repo="README.md", path_or_fileobj=readme)]
        removed = []
        for sub in folders.split(","):
            prefix = f"{sub}/" if sub else ""
            data = sorted(f for f in present if f.startswith(f"{prefix}data/"))
            removed += data
            ops += [CommitOperationDelete(path_in_repo=f) for f in data]
            name = f"{prefix}MANIFEST.json"
            manifest = json.loads(pathlib.Path(hf_hub_download(repo, name, revision=before)).read_text())
            manifest["files"] = {k: v for k, v in manifest["files"].items() if not k.startswith("data/")}
            manifest.pop("rows", None)
            if "README.md" in manifest["files"]:
                manifest["files"]["README.md"] = {"bytes": len(readme), "sha256": hashlib.sha256(readme).hexdigest()}
            ops.append(
                CommitOperationAdd(path_in_repo=name, path_or_fileobj=(json.dumps(manifest, indent=1) + "\n").encode())
            )
        save(stage=f"committing to {repo}")
        commit = api.create_commit(repo, operations=ops, commit_message=message)
        result = {
            "exp": exp,
            "repo": repo,
            "before": before,
            "commit": commit.oid,
            "removed": removed,
            "files": sorted(api.list_repo_files(repo)),
            "finished_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        r2.put_json(s3, f"{out}/scorecard.json", result)
        lines = [
            f"# {exp}: the model card to {repo}",
            "",
            f"Commit `{commit.oid}`, on `{before}`.",
            "",
            "Removed: " + (", ".join(removed) or "nothing") + ".",
            "",
            "Files now: " + ", ".join(result["files"]) + ".",
            "",
        ]
        r2.put_text(s3, f"{out}/report.md", "\n".join(lines))
        save(state="done", stage="done", commit=commit.oid)
        return {"state": "done", "commit": commit.oid}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
