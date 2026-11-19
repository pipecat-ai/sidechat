"""Export a trained Sidechat model to ONNX, check it against PyTorch, and time it on CPU.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.export::run --exp exp-015-side-export --run-id side-r1-ettin-68m-s0

Writes `models/side/<run_id>/export/`: model.onnx (encoder and heads in one graph, eager attention
so the graph keeps dynamic shapes), tokenizer.json and config.json (temperatures, thresholds from
the run's scoring, input version). Parity is read through `sidechat/runtime.py`, the code that
ships. Fetch it locally with `uv run python -m sidechat.pipeline.fetch <run_id>`.
"""

from __future__ import annotations

import modal

from sidechat.pipeline.train import _load, _model_key, _secrets, hf_cache, image

APP_NAME = "waystone-side-export"
app = modal.App(APP_NAME)


@app.function(image=image, cpu=8.0, memory=16384, timeout=2 * 3600, secrets=_secrets(), volumes={"/cache": hf_cache})
def run(exp: str, run_id: str, parity_rows: int = 300) -> dict:
    import pathlib
    import random
    import statistics
    import tempfile
    import time
    from datetime import UTC, datetime

    import torch

    from sidechat import conditions
    from sidechat.lib import r2
    from sidechat.runtime import load
    from sidechat.schema import SidechatRequest
    from sidechat.sources import build
    from sidechat.train import model as M

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    r2.put_json(
        s3,
        f"{out}/status.json",
        {
            "exp": exp,
            "state": "running",
            "stage": "exporting",
            "updated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        },
    )
    net, tok, config = _load(s3, run_id, "cpu", attn="eager")
    net.eval()
    card = r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json") or {}
    thresholds = card.get("thresholds") or {"respond": 0.7, "wait": 0.4, "open": 0.5}

    rows, _, _ = build.build_rows("pilot-0.4")
    rng = random.Random(0)
    sample = rng.sample(rows, min(parity_rows, len(rows)))
    sample = [conditions.apply(r, rng.choice(conditions.CONDITIONS)) for r in sample]

    class Wrap(torch.nn.Module):
        def __init__(self, m):
            super().__init__()
            self.m = m

        def forward(self, ids, mask, line_mask, num):
            return self.m(ids, mask, line_mask, num)

    d = pathlib.Path(tempfile.mkdtemp())
    b = M.encode(tok, sample[:2], config["max_len"], "cpu")
    torch.onnx.export(
        Wrap(net),
        (b["ids"], b["mask"], b["line_mask"], b["num"]),
        str(d / "model.onnx"),
        input_names=["ids", "mask", "line_mask", "num"],
        output_names=["intent", "respond", "unclear"],
        dynamic_axes={
            "ids": {0: "rows", 1: "len"},
            "mask": {0: "rows", 1: "len"},
            "line_mask": {0: "rows", 1: "len"},
            "num": {0: "rows"},
            "intent": {0: "rows"},
            "respond": {0: "rows"},
            "unclear": {0: "rows"},
        },
        opset_version=17,
        dynamo=False,
    )
    tok.save_pretrained(str(d / "tok"))
    (d / "tokenizer.json").write_bytes((d / "tok" / "tokenizer.json").read_bytes())
    # int8: weights only, per channel, and only matrix products with a constant side. Quantizing
    # every MatMul (attention scores included) wrecked round 1's model (exp-018).
    int8_error = None
    try:
        from onnxruntime.quantization import QuantType, quantize_dynamic

        quantize_dynamic(
            str(d / "model.onnx"),
            str(d / "model-int8.onnx"),
            weight_type=QuantType.QInt8,
            per_channel=True,
            op_types_to_quantize=["MatMul"],
            extra_options={"MatMulConstBOnly": True},
        )
    except Exception as e:  # noqa: BLE001 - the fp32 export stands on its own
        int8_error = f"{type(e).__name__}: {e}"[:500]
    runtime_config = {
        "run_id": run_id,
        "encoder": config["encoder"],
        "input_version": config["input_version"],
        "max_len": config["max_len"],
        "temperatures": config["temperatures"],
        "thresholds": thresholds,
        "exported_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    (d / "config.json").write_text(__import__("json").dumps(runtime_config, indent=1))

    # Parity: the shipping runtime against PyTorch on the same lines.
    ref = {
        p["row_id"]: p for p in M.predict(net, tok, sample, config["max_len"], "cpu", config["temperatures"], batch=32)
    }

    def parity(model) -> dict:
        diffs, same = [], 0
        for r in sample:
            a = model.answer(SidechatRequest(**r["request"]))
            p = ref[r["row_id"]]
            diffs.append(
                max(
                    abs(a.respond - p["respond"]),
                    abs(a.unclear - p["unclear"]),
                    max(abs(a.intent[k] - p["intent"][k]) for k in p["intent"]),
                )
            )
            same += model.decide(a, thresholds) == model.decide(
                a.model_copy(update={"respond": p["respond"], "intent": p["intent"]}), thresholds
            )
        return {"rows": len(sample), "max_prob_diff": round(max(diffs), 6), "decisions_same": same}

    def latency(int8: bool) -> dict:
        reqs = [SidechatRequest(**r["request"]) for r in sample[:200]]
        timing = {}
        for threads in (4, 1):
            m = load(d, threads=threads, int8=int8)
            for q in reqs[:10]:
                m.answer(q)
            ms = []
            for q in reqs:
                t0 = time.perf_counter()
                m.answer(q)
                ms.append((time.perf_counter() - t0) * 1000)
            ms.sort()
            timing[f"{threads}_threads"] = {
                "p50_ms": round(statistics.median(ms), 2),
                "p95_ms": round(ms[int(0.95 * len(ms))], 2),
            }
        return timing

    fp32 = {"parity": parity(load(d, threads=4)), "latency_modal_cpu": latency(False)}
    size_mb = round((d / "model.onnx").stat().st_size / 1e6, 1)
    names = ["model.onnx", "tokenizer.json", "config.json"]

    # The int8 build ships only if it stays close to fp32: first on the parity lines, then on dev
    # (anonymous, with the same real-speech bar), where it gets its own thresholds.
    int8 = None
    if int8_error is None:
        from sidechat.pipeline.train import _corpus_rows, _is_real
        from sidechat.train import evaluate as E

        p8 = parity(load(d, threads=4, int8=True))
        if p8["decisions_same"] < 0.95 * p8["rows"]:
            int8_error = f"parity too far from PyTorch: same decision on {p8['decisions_same']}/{p8['rows']}, largest probability difference {p8['max_prob_diff']}"
        else:
            q = load(d, threads=8, int8=True)
            dev = [
                conditions.apply(r, "anonymous")
                for r in _corpus_rows(s3, config["corpus"], {"dev"}, safe_only=True)
                if not _is_real(r)
            ]
            real = [conditions.apply(r, "anonymous") for r in build.build_rows("ami-silent:dev")[0]]
            preds8 = {}
            for i in range(0, len(dev + real), 64):
                part = (dev + real)[i : i + 64]
                for r, a in zip(part, q.answers([SidechatRequest(**r["request"]) for r in part])):
                    preds8[r["row_id"]] = {
                        "row_id": r["row_id"],
                        **a.model_dump(include={"intent", "respond", "unclear"}),
                    }
            t8 = E.choose_thresholds(preds8, dev, real_rows=real)
            preds32 = {
                p["row_id"]: p for p in r2.get_jsonl(s3, f"{r2.PREFIX}/predictions/{run_id}/dev@anonymous.jsonl") or []
            }
            dev32 = E.set_card(dev, preds32, thresholds)["sidechat"] if preds32 else None
            dev8 = E.set_card(dev, preds8, t8)["sidechat"]
            int8 = {
                "size_mb": round((d / "model-int8.onnx").stat().st_size / 1e6, 1),
                "thresholds": t8,
                "parity_vs_fp32_torch": p8,
                "latency_modal_cpu": latency(True),
                "dev_anonymous": {"int8": dev8, "fp32": dev32},
            }
            gap = (dev32["decision_right"]["value"] - dev8["decision_right"]["value"]) if dev32 else 0.0
            if gap > 0.01:
                int8_error = f"dev decision right {100 * gap:.1f} points below fp32"
                int8["shipped"] = False
            else:
                int8["shipped"] = True
                runtime_config["thresholds_int8"] = t8
                (d / "config.json").write_text(__import__("json").dumps(runtime_config, indent=1))
                names.insert(1, "model-int8.onnx")
    if "model-int8.onnx" not in names and r2.get_bytes(s3, _model_key(run_id, "export/model-int8.onnx")) is not None:
        r2.delete(s3, _model_key(run_id, "export/model-int8.onnx"))  # a stale build from an earlier export
    for name in names:
        r2.put_bytes(s3, _model_key(run_id, f"export/{name}"), (d / name).read_bytes())
    timing = fp32["latency_modal_cpu"]
    result = {
        "run_id": run_id,
        "size_mb": size_mb,
        "parity": fp32["parity"],
        "latency_modal_cpu": timing,
        "thresholds": thresholds,
        "int8": {**(int8 or {}), "error": int8_error},
    }

    def pct(x: dict | None, key: str) -> str:
        v = ((x or {}).get(key) or {}).get("value")
        return "n/a" if v is None else f"{100 * v:.1f}%"

    p = fp32["parity"]
    report = (
        f"# Export: {exp}\n\nModel `{run_id}` ({config['encoder']}), {size_mb} MB.\n\n"
        f"- Parity with PyTorch on {p['rows']} pilot lines in mixed speaker conditions: largest probability difference "
        f"{p['max_prob_diff']}, same decision on {p['decisions_same']}/{p['rows']}.\n"
        f"- Latency on a Modal CPU, one line at a time: {timing['4_threads']['p50_ms']} ms median and "
        f"{timing['4_threads']['p95_ms']} ms p95 on 4 threads; {timing['1_threads']['p50_ms']} / {timing['1_threads']['p95_ms']} ms on 1.\n"
        f"- Thresholds carried in config.json: {thresholds}.\n"
    )
    if int8 and int8.get("shipped"):
        p8, t8l, dv = int8["parity_vs_fp32_torch"], int8["latency_modal_cpu"], int8["dev_anonymous"]
        report += (
            f"\n## int8 build (`model-int8.onnx`, load with `int8=True`)\n\n"
            f"- {int8['size_mb']} MB. Largest probability difference from PyTorch {p8['max_prob_diff']}; same decision "
            f"(fp32 thresholds) on {p8['decisions_same']}/{p8['rows']}.\n"
            f"- Latency: {t8l['4_threads']['p50_ms']} ms median, {t8l['4_threads']['p95_ms']} ms p95 on 4 threads; "
            f"{t8l['1_threads']['p50_ms']} / {t8l['1_threads']['p95_ms']} ms on 1.\n"
            f"- Its own thresholds on dev (anonymous): {int8['thresholds']}. Dev decision right: int8 "
            f"{pct(dv['int8'], 'decision_right')}, fp32 {pct(dv['fp32'], 'decision_right')}; answers now on lines for "
            f"others: int8 {pct(dv['int8'], 'answers_now_wrongly')}, fp32 {pct(dv['fp32'], 'answers_now_wrongly')}.\n"
        )
    else:
        report += f"\nNo int8 build shipped: {int8_error}\n"
    r2.put_json(s3, f"{out}/scorecard.json", result)
    r2.put_text(s3, f"{out}/report.md", report)
    r2.put_json(
        s3,
        f"{out}/status.json",
        {
            "exp": exp,
            "state": "done",
            "stage": "done",
            "args": {"run_id": run_id},
            "updated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        },
    )
    return result
