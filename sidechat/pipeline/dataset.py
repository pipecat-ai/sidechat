"""Our own generated conversations as a Hugging Face dataset in Parquet, detached on Modal.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.dataset::run --exp exp-040-side-dataset

Only corpora this project wrote (`corpus`, by default every finished one): no AMI, no benchmark.
Rows are built by the training job's own code (`train._corpus_rows`), so they pass the same filter
and carry the labels of the current guide. One row per line, flattened so the Hub's viewer can show
it; the history stays a list of turns. Writes, under runs/side/datasets/<dataset_id>/:

    data/train-00000-of-00001.parquet, data/validation-..., data/test-...
    README.md (the dataset card, counts filled in), MANIFEST.json (counts, sha256 of each file)

and runs/side/results/<exp>/: status.json, scorecard.json, report.md. Nothing goes to the Hub.

`upload` sends a built folder from R2 to a Hub dataset repo, private unless the repo already exists
as private (it refuses a public one), after checking every file against MANIFEST.json:

    uv run modal run --detach -m sidechat.pipeline.dataset::upload --exp exp-051-side-dataset-upload
"""

from __future__ import annotations

import json
import os
import pathlib

import modal

from sidechat.lib.hf_dataset import SPLITS, arrow_schema, card, flat
from sidechat.lib.r2 import R2_KEYS

APP_NAME = "waystone-side-dataset"
ROOT = pathlib.Path(__file__).resolve().parents[2]  # the repo here; /root inside the container
ROW_GROUP = 10_000


def _secrets(keys: tuple[str, ...] = R2_KEYS) -> list:
    if not modal.is_local():
        return [modal.Secret.from_dict({})]
    if os.environ.get("MODAL_ENVIRONMENT") != "waystone":
        raise SystemExit("refusing: MODAL_ENVIRONMENT must be 'waystone'. Load .env first: set -a; . ./.env; set +a")
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"refusing: {', '.join(missing)} not set. Load .env first: set -a; . ./.env; set +a")
    return [modal.Secret.from_dict({k: os.environ[k] for k in keys})]


def build(s3, corpus: str, folder: pathlib.Path, on_stage=lambda stage: None) -> dict:
    """Write data/<split>-00000-of-00001.parquet for each split into `folder`. Returns the counts."""
    import collections

    import pyarrow as pa
    import pyarrow.parquet as pq

    from sidechat.lib import r2
    from sidechat.pipeline.train import _corpus_rows

    schema = arrow_schema()
    (folder / "data").mkdir(parents=True, exist_ok=True)
    paths = {hub: folder / "data" / f"{hub}-00000-of-00001.parquet" for hub in SPLITS.values()}
    writers = {hub: pq.ParquetWriter(p, schema, compression="zstd", write_page_index=True) for hub, p in paths.items()}
    counts: dict = {
        "by_corpus": {},
        "by_split": collections.Counter(),
        "expect": collections.Counter(),
        "kind": collections.Counter(),
    }
    try:
        for gen_id in [g for g in corpus.split(",") if g]:
            if not gen_id.startswith("gen-"):
                raise ValueError(f"{gen_id}: only corpora this project generated go in this dataset")
            on_stage(f"reading {gen_id}")
            manifest = r2.get_json(s3, f"{r2.PREFIX}/corpus/{gen_id}/manifest.json")
            if manifest is None:
                raise RuntimeError(f"{gen_id}: no manifest.json in R2, so the corpus is not finished")
            rows = _corpus_rows(s3, gen_id, set(SPLITS), safe_only=True)
            on_stage(f"writing {gen_id}")
            kept: dict[str, int] = {}
            for ours, hub in SPLITS.items():
                part = [flat(r) for r in rows if r["tags"]["split"] == ours]
                for i in range(0, len(part), ROW_GROUP):
                    writers[hub].write_table(pa.Table.from_pylist(part[i : i + ROW_GROUP], schema=schema))
                kept[hub] = len(part)
                counts["by_split"][hub] += len(part)
                counts["expect"].update(str(x["expect"]) for x in part)
                counts["kind"].update(x["kind"] for x in part)
            counts["by_corpus"][gen_id] = {
                "written": manifest["rows"],
                "kept": kept,
                "dropped": manifest["rows"] - sum(kept.values()),
                "conversations": manifest.get("conversations"),
                "writers": sorted(manifest.get("by_writer", {})),
            }
            del rows
    finally:
        for w in writers.values():
            w.close()
    counts["rows"] = sum(counts["by_split"].values())
    counts["by_split"], counts["expect"] = dict(counts["by_split"]), dict(counts["expect"])
    counts["kind"] = dict(counts["kind"].most_common())
    return counts


image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install("pyarrow==21.0.0", "boto3>=1.40", "pydantic>=2.9", "pyyaml>=6.0", "huggingface-hub==1.33.0")
    .add_local_python_source("sidechat")
    # train.py, whose row builder this job reuses, declares these two folders in its own image
    .add_local_dir(str(ROOT / "data" / "suites"), remote_path="/root/data/suites")
    .add_local_dir(str(ROOT / "contracts"), remote_path="/root/contracts")
)
app = modal.App(APP_NAME)


@app.function(
    image=image,
    cpu=4.0,
    memory=32768,
    timeout=3600,
    secrets=_secrets(),
    retries=modal.Retries(max_retries=1, initial_delay=30.0),
)
def run(exp: str, corpus: str = "gen-pilot,gen-0.1,gen-0.2,gen-0.3", dataset_id: str = "sidechat-gen-0.1") -> dict:
    import hashlib
    import shutil
    import time
    import traceback
    from datetime import UTC, datetime

    from sidechat import guide
    from sidechat.lib import r2

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    dest = f"{r2.PREFIX}/datasets/{dataset_id}"
    started = time.monotonic()
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {"corpus": corpus, "dataset_id": dataset_id},
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    try:
        folder = pathlib.Path("/tmp/dataset")
        shutil.rmtree(folder, ignore_errors=True)
        counts = build(s3, corpus, folder, on_stage=lambda stage: save(stage=stage))
        (folder / "README.md").write_text(card(dataset_id, guide.GUIDE_VERSION, counts))
        files = {}
        for p in sorted(folder.rglob("*")):
            if p.is_file():
                files[p.relative_to(folder).as_posix()] = {
                    "bytes": p.stat().st_size,
                    "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
                }
        manifest = {
            "dataset_id": dataset_id,
            "corpus": corpus,
            "guide": guide.GUIDE_VERSION,
            "rows": counts,
            "files": files,
            "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        (folder / "MANIFEST.json").write_text(json.dumps(manifest, indent=1) + "\n")

        save(stage=f"uploading to {dest}", rows=counts["by_split"])
        for p in sorted(folder.rglob("*")):
            if p.is_file():
                s3.upload_file(str(p), r2._bucket(), f"{dest}/{p.relative_to(folder).as_posix()}")
        r2.put_json(s3, f"{out}/scorecard.json", {"exp": exp, "dest": dest, **manifest})
        lines = [
            f"# {exp}: {dataset_id}",
            "",
            f"In R2 at `{dest}/`, labels under {guide.GUIDE_VERSION}.",
            "",
            "| Corpus | Lines written | Kept | Train | Validation | Test |",
            "|---|---|---|---|---|---|",
        ]
        for g, c in counts["by_corpus"].items():
            k = c["kept"]
            lines.append(
                f"| {g} | {c['written']:,} | {sum(k.values()):,} | {k['train']:,} | {k['validation']:,} | {k['test']:,} |"
            )
        s = counts["by_split"]
        lines += [
            f"| **All** | | **{counts['rows']:,}** | {s['train']:,} | {s['validation']:,} | {s['test']:,} |",
            "",
            "| File | Bytes | sha256 |",
            "|---|---|---|",
        ]
        lines += [f"| {k} | {v['bytes']:,} | `{v['sha256'][:16]}` |" for k, v in files.items()]
        lines += ["", "Expect: " + ", ".join(f"{k} {v:,}" for k, v in sorted(counts["expect"].items())), ""]
        r2.put_text(s3, f"{out}/report.md", "\n".join(lines))
        save(state="done", stage="done")
        return {"state": "done", "dest": dest, "rows": counts["by_split"]}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise


@app.function(image=image, cpu=2.0, memory=4096, timeout=3600, secrets=_secrets((*R2_KEYS, "HF_TOKEN")))
def upload(exp: str, dataset_id: str = "sidechat-gen-0.1", repo: str = "pipecat-ai/sidechat-gen") -> dict:
    import hashlib
    import shutil
    import time
    import traceback
    from datetime import UTC, datetime

    from huggingface_hub import HfApi
    from huggingface_hub.errors import RepositoryNotFoundError

    from sidechat.lib import r2

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    src = f"{r2.PREFIX}/datasets/{dataset_id}"
    started = time.monotonic()
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {"dataset_id": dataset_id, "repo": repo},
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    try:
        save(stage=f"reading {src}")
        folder = pathlib.Path("/tmp/upload")
        shutil.rmtree(folder, ignore_errors=True)
        for k in r2.list_keys(s3, src + "/"):
            p = folder / k["Key"][len(src) + 1 :]
            p.parent.mkdir(parents=True, exist_ok=True)
            s3.download_file(r2._bucket(), k["Key"], str(p))
        manifest = json.loads((folder / "MANIFEST.json").read_text())
        for name, f in manifest["files"].items():
            if hashlib.sha256((folder / name).read_bytes()).hexdigest() != f["sha256"]:
                raise RuntimeError(f"{name}: sha256 does not match MANIFEST.json")

        api = HfApi(token=os.environ["HF_TOKEN"])
        try:
            if not api.repo_info(repo, repo_type="dataset").private:
                raise RuntimeError(f"{repo} exists and is public; refusing to upload to it")
        except RepositoryNotFoundError:
            api.create_repo(repo, repo_type="dataset", private=True)
        save(stage=f"uploading to {repo}")
        commit = api.upload_folder(
            folder_path=str(folder),
            repo_id=repo,
            repo_type="dataset",
            commit_message=f"{dataset_id}: generated conversations as Parquet, with the card",
        )
        private = api.repo_info(repo, repo_type="dataset").private
        card = {
            "exp": exp,
            "dataset_id": dataset_id,
            "repo": repo,
            "private": private,
            "commit": commit.oid,
            "files": manifest["files"],
            "rows": manifest["rows"]["by_split"],
            "finished_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        r2.put_json(s3, f"{out}/scorecard.json", card)
        lines = [
            f"# {exp}: {dataset_id} to {repo}",
            "",
            f"Commit `{commit.oid}`, private: {private}.",
            "",
            "| File | Bytes | sha256 |",
            "|---|---|---|",
        ]
        lines += [f"| {k} | {v['bytes']:,} | `{v['sha256'][:16]}` |" for k, v in manifest["files"].items()]
        lines += ["", "Rows: " + ", ".join(f"{k} {v:,}" for k, v in manifest["rows"]["by_split"].items()), ""]
        r2.put_text(s3, f"{out}/report.md", "\n".join(lines))
        save(state="done", stage="done", commit=commit.oid, private=private)
        return {"state": "done", "repo": repo, "commit": commit.oid, "private": private}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
