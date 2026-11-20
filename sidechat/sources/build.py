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
from sidechat.sources import ambient_bench, ami, duplex_mpe, realreq, slurp, suites, tcl_wakeup

SETS = (
    "demo",
    "pilot",
    "ambient",
    "duplex",
    "ami",
    "ami-silent",
    "ami-stt",
    "ami-silent-stt",
    "slurp",
    "slurp-stt",
    "slurp-stt-keyterm",
    "names-dev",
    "names-dev-stt",
    "names-dev-stt-keyterm",
    "realreq",
    "tcl",
)


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
    elif which.startswith("realreq"):
        # Real people's requests (SLURP's and CLINC150's text) said in AMI's unlabelled meetings.
        import urllib.request

        from sidechat.gen import world

        def get(url: str) -> str:
            with urllib.request.urlopen(url, timeout=120) as resp:
                return resp.read().decode()

        version, _, splits = which.partition(":")
        if version not in realreq.VERSIONS:
            raise ValueError(f"unknown realreq version {version!r}; choose from {sorted(realreq.VERSIONS)}")
        sl = {
            name: [
                json.loads(x)
                for x in get(realreq.SLURP_URL.format(commit=realreq.SLURP_COMMIT, split=name)).splitlines()
                if x.strip()
            ]
            for name in ("train", "devel", "test")
        }
        clinc = json.loads(get(realreq.CLINC_URL.format(commit=realreq.CLINC_COMMIT)))
        reqs = realreq.requests({"train": sl["train"], "devel": sl["devel"]}, clinc, sl["test"], version)
        local = _fetch(ami.REPO, ami.REVISION, ami.FILES["all"])
        records = [json.loads(x) for x in pathlib.Path(local).read_text().splitlines() if x.strip()]
        names = sorted(n for n in world.AGENTS if n not in world.HELDOUT_AGENTS)
        rows = realreq.convert(reqs, records, names, list(world.PEOPLE), version)
        if splits:
            rows = [r for r in rows if r["tags"]["split"] in set(splits.split("+"))]
        source = {
            "kind": "splice: real requests in AMI meetings",
            "slurp": {"url": realreq.SLURP_URL, "commit": realreq.SLURP_COMMIT},
            "clinc": {"url": realreq.CLINC_URL, "commit": realreq.CLINC_COMMIT},
            "ami": {"repo": ami.REPO, "revision": ami.REVISION},
            "licence": realreq.LICENCE,
            "use": realreq.USE,
        }
    elif which in ("slurp", "slurp-stt", "slurp-stt-keyterm", "names-dev", "names-dev-stt", "names-dev-stt-keyterm"):
        # SLURP's requests said in AMI's silence-test meetings (`sidechat/sources/slurp.py`). Test only;
        # names-dev* are the train and devel utterances that say the name, a dev set for names as heard.
        from sidechat.lib import r2

        s3 = r2.client()
        dev = which.startswith("names-dev")
        keyterm = which.endswith("-keyterm")
        if dev:
            prefix = slurp.DEV_STT_KEYTERM_PREFIX if keyterm else slurp.DEV_STT_PREFIX
            set_name = {"names-dev": slurp.DEV_SET, "names-dev-stt": slurp.DEV_STT_SET}.get(
                which, slurp.DEV_STT_KEYTERM_SET
            )
        else:
            prefix = slurp.STT_KEYTERM_PREFIX if keyterm else slurp.STT_PREFIX
            set_name = slurp.STT_KEYTERM_SET if keyterm else ""
        smf = r2.get_json(s3, f"{r2.PREFIX}/{prefix}/manifest.json")
        amf = r2.get_json(s3, f"{r2.PREFIX}/{ami.STT_PREFIX}/manifest.json")
        if not smf or not amf:
            raise ValueError("no SLURP or AMI transcripts in R2 yet: run sidechat.pipeline.phase6 first")
        rows = slurp.convert(
            r2.get_jsonl(s3, f"{r2.PREFIX}/{prefix}/transcripts.jsonl") or [],
            r2.get_jsonl(s3, f"{r2.PREFIX}/{ami.STT_PREFIX}/transcripts.jsonl") or [],
            heard=which not in ("slurp", "names-dev"),
            set_name=set_name,
        )
        source = {
            "kind": "splice: SLURP requests in AMI meetings",
            "slurp": {"text": smf.get("text"), "audio": smf.get("audio"), "stt": smf.get("stt")},
            "ami": {"labels": amf.get("labels"), "audio": amf.get("audio")},
            "licence": slurp.LICENCE,
            "use": slurp.USE,
        }
    elif which in ("ami-stt",) or which.startswith("ami-silent-stt"):
        # AMI's lines as a real speech-to-text service heard them (`sidechat/pipeline/stt_ami.py`).
        from sidechat.gen import world
        from sidechat.lib import r2

        s3 = r2.client()
        stt_manifest = r2.get_json(s3, f"{r2.PREFIX}/{ami.STT_PREFIX}/manifest.json")
        if not stt_manifest:
            raise ValueError("no AMI transcripts in R2 yet: run sidechat.pipeline.stt_ami first")
        stt = {x["da_id"]: x["stt"] for x in r2.get_jsonl(s3, f"{r2.PREFIX}/{ami.STT_PREFIX}/transcripts.jsonl") or []}
        local = _fetch(ami.REPO, ami.REVISION, ami.FILES["all"])
        records = ami.with_stt([json.loads(x) for x in pathlib.Path(local).read_text().splitlines() if x.strip()], stt)
        if which == "ami-stt":
            rows = ami.convert(records, ami.STT_SET)
        else:
            _, _, splits = which.partition(":")
            names = sorted(n for n in world.AGENTS if n not in world.HELDOUT_AGENTS)
            rows = ami.convert_silent(records, names, ami.SILENT_STT_SET)
            if splits:
                rows = [r for r in rows if r["tags"]["split"] in set(splits.split("+"))]
            rows = [
                {**r, "set": f"{ami.SILENT_STT_SET}.{splits.replace('+', '-')}" if splits else r["set"]} for r in rows
            ]
        source = {
            "kind": "Hugging Face dataset, transcribed",
            "repo": ami.REPO,
            "revision": ami.REVISION,
            "files": {ami.FILES["all"]: _sha256(local)},
            "transcripts": f"{r2.PREFIX}/{ami.STT_PREFIX}/transcripts.jsonl",
            "stt": stt_manifest.get("stt"),
            "audio": stt_manifest.get("audio"),
            "licence": ami.LICENCE,
            "use": "test only",
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
    elif which == "tcl":
        # TCL's Intelligent Wakeup, test split, text only, kept in R2 by `sidechat.pipeline.tcl`.
        # Test only (SD-27).
        from sidechat.lib import r2

        s3 = r2.client()
        tmf = r2.get_json(s3, f"{r2.PREFIX}/{tcl_wakeup.TEXT_PREFIX}/manifest.json")
        if not tmf:
            raise ValueError("no TCL text in R2 yet: run sidechat.pipeline.tcl with the fetch step first")
        sessions = r2.get_jsonl(s3, f"{r2.PREFIX}/{tcl_wakeup.TEXT_PREFIX}/test.jsonl") or []
        rows = tcl_wakeup.convert(sessions[:limit] if limit else sessions)
        source = {
            "kind": "Hugging Face dataset, text columns",
            "repo": tcl_wakeup.REPO,
            "revision": tcl_wakeup.REVISION,
            "files": tmf.get("files"),
            "text": f"{r2.PREFIX}/{tcl_wakeup.TEXT_PREFIX}/test.jsonl",
            "licence": tcl_wakeup.LICENCE,
            "use": tcl_wakeup.USE,
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
