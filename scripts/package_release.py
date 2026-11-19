"""Lay out an exported model as a Hugging Face release that Pipecat's `SideChatModel` loads.

    uv run python scripts/package_release.py models/side-r3-ettin-150m-s0 models/sidechat-rc1 --release rc1

The release folder holds:

    config.json        input version, intents, temperatures, and thresholds per precision
    model.onnx         full precision
    model.int8.onnx    int8 weights, when the export made them
    tokenizer.json

The ONNX files and tokenizer are hard links to the export's (copies across filesystems), so
packaging costs no disk. The model card (README.md) is written separately.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sidechat.schema import INTENTS  # noqa: E402
from sidechat.train.features import INPUT_VERSION  # noqa: E402


def thresholds(raw: dict) -> dict:
    return {"respond": raw["respond"], "hold": raw["wait"], "open": raw["open"]}


def link(src: pathlib.Path, dst: pathlib.Path) -> None:
    if dst.exists():
        dst.unlink()
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model_dir", type=pathlib.Path)
    ap.add_argument("out_dir", type=pathlib.Path)
    ap.add_argument("--release", required=True, help="the release tag, e.g. rc1")
    args = ap.parse_args()

    src = json.loads((args.model_dir / "config.json").read_text())
    if src.get("input_version") != INPUT_VERSION:
        sys.exit(f"{args.model_dir} reads {src.get('input_version')}, this code builds {INPUT_VERSION}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    precisions = {"fp32": thresholds(src["thresholds"])}
    link(args.model_dir / "model.onnx", args.out_dir / "model.onnx")
    if (args.model_dir / "model-int8.onnx").exists():
        if not src.get("thresholds_int8"):
            sys.exit(f"{args.model_dir} has int8 weights without thresholds of their own")
        precisions["int8"] = thresholds(src["thresholds_int8"])
        link(args.model_dir / "model-int8.onnx", args.out_dir / "model.int8.onnx")
    link(args.model_dir / "tokenizer.json", args.out_dir / "tokenizer.json")

    config = {
        "name": "sidechat",
        "release": args.release,
        "run_id": src["run_id"],
        "encoder": src["encoder"],
        "input_version": src["input_version"],
        "max_len": src["max_len"],
        "intents": list(INTENTS),
        "temperatures": src["temperatures"],
        "thresholds": precisions,
    }
    (args.out_dir / "config.json").write_text(json.dumps(config, indent=1) + "\n")
    print(f"{args.out_dir}: {', '.join(sorted(p.name for p in args.out_dir.iterdir()))}")


if __name__ == "__main__":
    main()
