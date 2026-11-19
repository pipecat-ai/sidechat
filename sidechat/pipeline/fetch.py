"""Download an exported model from R2 into `models/<run_id>/` (gitignored).

set -a; . ./.env; set +a
uv run python -m sidechat.pipeline.fetch side-r1-ettin-68m-s0
"""

from __future__ import annotations

import pathlib
import sys

from sidechat.lib import r2

ROOT = pathlib.Path(__file__).resolve().parents[2]


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    run_id = sys.argv[1]
    s3 = r2.client()
    folder = ROOT / "models" / run_id
    folder.mkdir(parents=True, exist_ok=True)
    for name in ("model.onnx", "tokenizer.json", "config.json"):
        data = r2.get_bytes(s3, f"models/side/{run_id}/export/{name}")
        if data is None:
            print(f"{run_id}: no export in R2 yet ({name} missing)")
            return 1
        (folder / name).write_bytes(data)
    int8 = r2.get_bytes(s3, f"models/side/{run_id}/export/model-int8.onnx")
    if int8 is not None:
        (folder / "model-int8.onnx").write_bytes(int8)
    print(
        f"saved models/{run_id}/ ({(folder / 'model.onnx').stat().st_size / 1e6:.1f} MB"
        + (f"; int8 build {len(int8) / 1e6:.1f} MB" if int8 is not None else "")
        + ")"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
