"""Where an export's parity gap comes from: PyTorch in batches, PyTorch one line at a time, and the
ONNX runtime, on the same pilot lines.

    set -a; . ./.env; set +a
    uv run modal run -m sidechat.pipeline.parity_probe::run --run-id side-ttsmoke-ettin-32m-s0

Prints a short JSON summary. No results are written; it is a debugging aid (exp-036).
"""

from __future__ import annotations

import modal

from sidechat.pipeline.train import _load, _model_key, _secrets, hf_cache, image

app = modal.App("waystone-side-parity-probe")


@app.function(image=image, cpu=4.0, memory=16384, timeout=1800, secrets=_secrets(), volumes={"/cache": hf_cache})
def run(run_id: str, rows: int = 120) -> dict:
    import json
    import pathlib
    import random
    import tempfile

    import torch

    from sidechat import conditions
    from sidechat.lib import r2
    from sidechat.runtime import load
    from sidechat.schema import SidechatRequest
    from sidechat.sources import build
    from sidechat.train import features
    from sidechat.train import model as M

    s3 = r2.client()
    net, tok, config = _load(s3, run_id, "cpu", attn="eager")
    net.eval()
    pilot, _, _ = build.build_rows("pilot-0.4")
    rng = random.Random(0)
    sample = [conditions.apply(r, rng.choice(conditions.CONDITIONS)) for r in rng.sample(pilot, rows)]
    temps = config["temperatures"]
    batched = {p["row_id"]: p for p in M.predict(net, tok, sample, config["max_len"], "cpu", temps, batch=32, spec=config)}
    single = {p["row_id"]: p for p in M.predict(net, tok, sample, config["max_len"], "cpu", temps, batch=1, spec=config)}

    d = pathlib.Path(tempfile.mkdtemp())
    for name in ("config.json", "tokenizer.json", "context.onnx", "line.onnx", "model.onnx"):
        data = r2.get_bytes(s3, _model_key(run_id, f"export/{name}"))
        if data is not None:
            (d / name).write_bytes(data)
    rt = load(d, threads=4)

    def diff(a: dict, b: dict) -> float:
        return max(abs(a["respond"] - b["respond"]), *(abs(a["intent"][k] - b["intent"][k]) for k in a["intent"]))

    out = {"batched_vs_single": [], "single_vs_runtime": [], "examples": []}
    for r in sample:
        q = SidechatRequest(**r["request"])
        a = rt.answer(q).model_dump()
        b, s = batched[r["row_id"]], single[r["row_id"]]
        out["batched_vs_single"].append(diff(b, s))
        out["single_vs_runtime"].append(diff(s, a))
        # Inputs as each side builds them, to compare by eye.
        if diff(s, a) > 0.05 and len(out["examples"]) < 4 and config.get("arch") == "twotower":
            n = config["ctx_len"]
            hf_ctx = tok(features.context_fitted(q, n, lambda t: len(tok(t)["input_ids"])))["input_ids"]
            rt_ctx = rt.tokenizer.encode(features.context_fitted(q, n, lambda t: len(rt.tokenizer.encode(t).ids))).ids
            hf_line = tok(features.line_text(q))["input_ids"]
            rt_line = rt.tokenizer.encode(features.line_text(q)).ids
            out["examples"].append(
                {
                    "torch": s["respond"],
                    "runtime": a["respond"],
                    "ctx_same": hf_ctx == rt_ctx,
                    "line_same": hf_line == rt_line,
                    "ctx_len": len(hf_ctx),
                    "line_len": len(hf_line),
                    "turns": len(q.history),
                    "speaker": q.speaker is not None,
                }
            )
    summary = {
        k: {"max": round(max(v), 6), "over_0.05": sum(x > 0.05 for x in v)} for k, v in out.items() if k != "examples"
    }
    summary["examples"] = out["examples"]
    with torch.no_grad():
        summary["note"] = "max abs difference in respond or any intent probability"
    print(json.dumps(summary, indent=1))
    return summary
