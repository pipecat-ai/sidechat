"""R2 storage for every job's inputs and outputs.

Layout, all under `runs/side/` and `models/side/` in the bucket Audience uses:

    runs/side/rows/<rows_id>/rows.jsonl, manifest.json
    runs/side/baselines/<baseline_id>/parts/<n>.jsonl, scores/<rows_id>.jsonl, manifest.json
    runs/side/results/<exp>/status.json, scorecard.json, report.md

The settings come from the environment: `R2_ENDPOINT`, `R2_REGION`, `R2_ACCESS_KEY_ID`,
`R2_SECRET_ACCESS_KEY`, `R2_BUCKET`. Locally, load `.env` first: `set -a; . ./.env; set +a`.
"""

from __future__ import annotations

import hashlib
import json
import os

R2_KEYS = ("R2_ENDPOINT", "R2_REGION", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET")
PREFIX = "runs/side"


def client():
    import boto3
    from botocore.config import Config

    missing = [k for k in R2_KEYS if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"missing {', '.join(missing)}. Load .env first: set -a; . ./.env; set +a")
    return boto3.client(
        "s3",
        endpoint_url=os.environ["R2_ENDPOINT"],
        region_name=os.environ["R2_REGION"] or "auto",
        aws_access_key_id=os.environ["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4", retries={"max_attempts": 8, "mode": "adaptive"}),
    )


def _bucket() -> str:
    return os.environ["R2_BUCKET"]


def put_bytes(s3, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
    s3.put_object(Bucket=_bucket(), Key=key, Body=data, ContentType=content_type)
    return hashlib.sha256(data).hexdigest()


def put_json(s3, key: str, value) -> str:
    return put_bytes(s3, key, json.dumps(value, indent=1, ensure_ascii=False).encode(), "application/json")


def put_jsonl(s3, key: str, rows: list[dict]) -> str:
    body = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows).encode()
    return put_bytes(s3, key, body, "application/x-ndjson")


def put_text(s3, key: str, text: str) -> str:
    return put_bytes(s3, key, text.encode(), "text/markdown; charset=utf-8")


def get_bytes(s3, key: str) -> bytes | None:
    try:
        return s3.get_object(Bucket=_bucket(), Key=key)["Body"].read()
    except s3.exceptions.NoSuchKey:
        return None


def get_json(s3, key: str):
    data = get_bytes(s3, key)
    return None if data is None else json.loads(data)


def get_jsonl(s3, key: str) -> list[dict] | None:
    data = get_bytes(s3, key)
    return None if data is None else [json.loads(x) for x in data.decode().splitlines() if x.strip()]


def list_keys(s3, prefix: str) -> list[dict]:
    """Every object under a prefix: [{"Key", "Size", "LastModified"}]."""
    out = []
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=_bucket(), Prefix=prefix):
        out.extend(page.get("Contents", []))
    return out


def delete(s3, key: str) -> None:
    """Remove one object (a stale build this project wrote)."""
    s3.delete_object(Bucket=_bucket(), Key=key)
