"""Build the labelled rows of one set, with a manifest that says where they came from.

External sets are downloaded from Hugging Face at a pinned revision, so a set means the same rows
every time it is built. Hand-written suites are read from `data/suites/`.
"""

from __future__ import annotations

import hashlib
import json
import pathlib
from collections import Counter
from datetime import UTC, datetime

from sidechat.schema import SCHEMA_VERSION
from sidechat.sources import ambient_bench, ami, duplex_mpe, suites

SETS = ("demo", "pilot", "ambient", "duplex", "ami")


def _sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _fetch(repo: str, revision: str, filename: str) -> str:
    from huggingface_hub import hf_hub_download

    return hf_hub_download(repo, filename, repo_type="dataset", revision=revision)


def build_rows(which: str, limit: int = 0) -> tuple[list[dict], dict, dict]:
    """Rows, their manifest, and extras that travel with the set (a benchmark's own leaderboard).

    `limit` keeps only the first conversations, for a quick trial run. A set name may end in a
    speaker-label condition, `@anonymous` or `@none` (`sidechat/conditions.py`); without one the
    set is as written, which is `named` for suites.
    """
    from sidechat import conditions

    which, _, condition = which.partition("@")
    extras: dict = {}
    if which in suites.SUITE_FILES:
        suite = suites.load(which)
        if limit:
            suite["conversations"] = suite["conversations"][:limit]
        rows = suites.convert(suite)
        path = suites.SUITES_DIR / suites.SUITE_FILES[which]
        source = {
            "kind": "hand-written suite",
            "file": f"data/suites/{path.name}",
            "sha256": _sha256(str(path)),
            "about": suite.get("about", ""),
            "label_source": suite.get("label_source", "author"),
            "use": suite.get("use", "test"),
        }
        if suite.get("label_from") == "guide":
            from sidechat.guide import GUIDE_VERSION

            source["guide"] = GUIDE_VERSION
    elif which.startswith("corpus:"):
        # corpus:<gen_id>[:<splits joined by +>[:<sample size>[:<kinds joined by +>]]], read from R2
        import hashlib
        import random

        from sidechat.lib import r2

        _, gen_id, splits, size, kinds = (which.split(":") + ["", "", "", ""])[:5]
        s3 = r2.client()
        rows = r2.get_jsonl(s3, f"{r2.PREFIX}/corpus/{gen_id}/rows.jsonl") or []
        manifest_in = r2.get_json(s3, f"{r2.PREFIX}/corpus/{gen_id}/manifest.json") or {}
        wanted = set(splits.split("+")) if splits and splits != "all" else None
        if wanted:
            rows = [r for r in rows if r["tags"]["split"] in wanted]
        if kinds:
            rows = [r for r in rows if r["tags"].get("kind") in set(kinds.split("+"))]
        if size:
            rows = random.Random(f"{gen_id}:{splits}").sample(rows, min(int(size), len(rows)))
            rows.sort(key=lambda r: (r["conv_id"], r["turn_index"]))
        name = f"{gen_id}.{(splits or 'all').replace('+', '-')}{size}"
        if kinds:
            name += "-k" + hashlib.sha1(kinds.encode()).hexdigest()[:6]
        rows = [{**r, "set": name} for r in rows]
        source = {
            "kind": "generated corpus",
            "gen_id": gen_id,
            "splits": splits or "all",
            "sample": size or None,
            "kinds": kinds.split("+") if kinds else None,
            "corpus_rows_sha256": manifest_in.get("rows_sha256"),
            "guide": manifest_in.get("guide"),
            "use": "per split",
        }
    elif which == "ami":
        local = _fetch(ami.REPO, ami.REVISION, ami.FILES["all"])
        records = [json.loads(x) for x in pathlib.Path(local).read_text().splitlines() if x.strip()]
        rows = ami.convert(records)
        if limit:
            keep = sorted({r["conv_id"] for r in rows})[:limit]
            rows = [r for r in rows if r["conv_id"] in keep]
        source = {
            "kind": "Hugging Face dataset",
            "repo": ami.REPO,
            "revision": ami.REVISION,
            "files": {ami.FILES["all"]: _sha256(local)},
            "licence": ami.LICENCE,
            "use": ami.USE,
        }
    elif which.startswith("ami-silent"):
        from sidechat.gen import world

        _, _, splits = which.partition(":")
        local = _fetch(ami.REPO, ami.REVISION, ami.FILES["all"])
        records = [json.loads(x) for x in pathlib.Path(local).read_text().splitlines() if x.strip()]
        names = sorted(n for n in world.AGENTS if n not in world.HELDOUT_AGENTS)
        rows = ami.convert_silent(records, names)
        if splits:
            rows = [r for r in rows if r["tags"]["split"] in set(splits.split("+"))]
        rows = [{**r, "set": f"{ami.SILENT_SET}.{splits.replace('+', '-')}" if splits else r["set"]} for r in rows]
        source = {
            "kind": "Hugging Face dataset",
            "repo": ami.REPO,
            "revision": ami.REVISION,
            "files": {ami.FILES["all"]: _sha256(local)},
            "licence": ami.LICENCE,
            "use": ami.SILENT_USE,
        }
    elif which == "duplex":
        scenarios, files = [], {}
        for filename in duplex_mpe.FILES.values():
            local = _fetch(duplex_mpe.REPO, duplex_mpe.REVISION, filename)
            files[filename] = _sha256(local)
            loaded = json.loads(pathlib.Path(local).read_text())
            scenarios.extend(loaded[:limit] if limit else loaded)
        rows = duplex_mpe.convert(scenarios)
        source = {
            "kind": "Hugging Face dataset",
            "repo": duplex_mpe.REPO,
            "revision": duplex_mpe.REVISION,
            "files": files,
            "licence": duplex_mpe.LICENCE,
            "use": duplex_mpe.USE,
        }
    elif which == "ambient":
        local = _fetch(ambient_bench.REPO, ambient_bench.REVISION, ambient_bench.FILES["test"])
        files = {ambient_bench.FILES["test"]: _sha256(local)}
        scenarios = [json.loads(x) for x in pathlib.Path(local).read_text().splitlines() if x.strip()]
        rows = ambient_bench.convert(scenarios[:limit] if limit else scenarios)
        board = _fetch(ambient_bench.REPO, ambient_bench.REVISION, ambient_bench.FILES["leaderboard"])
        extras["leaderboard"] = json.loads(pathlib.Path(board).read_text())
        source = {
            "kind": "Hugging Face dataset",
            "repo": ambient_bench.REPO,
            "revision": ambient_bench.REVISION,
            "files": files,
            "licence": ambient_bench.LICENCE,
            "use": ambient_bench.USE,
        }
    else:
        raise ValueError(f"unknown set {which!r}; choose from {SETS}")

    if condition:
        rows = [conditions.apply(r, condition) for r in rows]
    rows_id = rows[0]["set"] if rows else which
    manifest = {
        "rows_id": rows_id,
        "schema_version": SCHEMA_VERSION,
        "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "source": source,
        "limit": limit or None,
        "condition": condition or "as written",
        "rows": len(rows),
        "conversations": len({r["conv_id"] for r in rows}),
        "by_expect": dict(Counter(str(r["label"]["expect"]) for r in rows)),
        "by_to": dict(Counter(r["label"]["to"] for r in rows)),
    }
    return rows, manifest, extras
