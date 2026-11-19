"""List or download objects from the training R2 bucket.

usage:
  r2.py ENV_FILE list PREFIX
  r2.py ENV_FILE get PREFIX DEST_DIR
"""
import hashlib
import os
import sys

import boto3
from botocore.config import Config


def load_r2(env_path):
    vals = {}
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("R2_") and "=" in line:
                k, v = line.split("=", 1)
                vals[k] = v.strip().strip('"').strip("'")
    return vals


def client(cfg):
    return boto3.client(
        "s3",
        endpoint_url=cfg["R2_ENDPOINT"],
        region_name=cfg.get("R2_REGION") or "auto",
        aws_access_key_id=cfg["R2_ACCESS_KEY_ID"],
        aws_secret_access_key=cfg["R2_SECRET_ACCESS_KEY"],
        config=Config(signature_version="s3v4", retries={"max_attempts": 5}),
    )


def objects(s3, bucket, prefix):
    for page in s3.get_paginator("list_objects_v2").paginate(Bucket=bucket, Prefix=prefix):
        yield from page.get("Contents", [])


def main():
    env_path, cmd, prefix = sys.argv[1:4]
    cfg = load_r2(env_path)
    s3, bucket = client(cfg), cfg["R2_BUCKET"]
    if cmd == "list":
        total = n = 0
        for o in objects(s3, bucket, prefix):
            print(f"{o['Size']:>12}  {o['LastModified']:%Y-%m-%d}  {o['Key']}")
            total += o["Size"]
            n += 1
        print(f"{n} objects, {total / 1e6:.1f} MB")
    elif cmd == "get":
        dest = sys.argv[4]
        for o in objects(s3, bucket, prefix):
            key = o["Key"]
            out = os.path.join(dest, key)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            s3.download_file(bucket, key, out)
            h = hashlib.sha256()
            with open(out, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            print(f"{h.hexdigest()}  {o['Size']:>12}  {key}")


if __name__ == "__main__":
    main()
