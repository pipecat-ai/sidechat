"""Export a trained Sidechat model to ONNX, check it against PyTorch, and time it on CPU.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.export::run --exp exp-015-side-export --run-id side-r1-ettin-68m-s0

Writes `models/side/<run_id>/export/`: model.onnx (encoder and heads in one graph, eager attention
so the graph keeps dynamic shapes), tokenizer.json and config.json (temperatures, thresholds from
the run's scoring, input version). Parity is read through `sidechat/runtime.py`, the code that
ships. Fetch it locally with `uv run python -m sidechat.pipeline.fetch <run_id>`.

A two-tower model (config `arch: twotower`) exports `context.onnx` (history to token states) and
`line.onnx` (line plus cached states to the heads) instead of model.onnx. Each graph goes through
ONNX Runtime's transformer optimizer (kept only if parity holds and it is faster on one thread),
then int8 per channel behind the same quality gate.
"""

from __future__ import annotations

import modal

from sidechat.pipeline.train import _load, _model_key, _secrets, hf_cache, image

APP_NAME = "waystone-side-export"
app = modal.App(APP_NAME)


def int8_excluded(path) -> list[str]:
    """The matrix products int8 leaves in fp32: each encoder layer's MLP output (exp-068)."""
    import onnx

    graph = onnx.load(str(path), load_external_data=False).graph
    return [n.name for n in graph.node if n.op_type == "MatMul" and "mlp" in n.name and "Wo" in n.name]


@app.function(name="export_run", image=image, cpu=8.0, memory=16384, timeout=2 * 3600, secrets=_secrets(), volumes={"/cache": hf_cache})
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

    class Context(torch.nn.Module):
        def __init__(self, m):
            super().__init__()
            self.m = m

        def forward(self, ids, mask):
            return self.m.encode_context(ids, mask)

    class Line(torch.nn.Module):
        def __init__(self, m):
            super().__init__()
            self.m = m

        def forward(self, ids, mask, ctx, ctx_mask, num):
            return self.m.forward_line(ids, mask, ctx, ctx_mask, num)

    d = pathlib.Path(tempfile.mkdtemp())
    turns = config.get("text_turns", 0)
    tt = config.get("arch") == "twotower"
    graphs = ["context", "line"] if tt else ["model"]
    outs = {"intent": {0: "rows"}, "respond": {0: "rows"}, "unclear": {0: "rows"}}
    # Trace on one long input and one shorter one. The encoder builds its sliding-window mask (128
    # tokens) and its padding mask only when the input needs them, and tracing keeps whichever
    # branch the example took: short examples drop the window from the graph, and longer inputs are
    # then read wrongly (the first two-tower export, exp-036).
    long_turns = [{"speaker": f"P{i % 3}", "text": " ".join(["word"] * 45), "agent": False} for i in range(8)]
    example = [{**sample[0], "request": {**sample[0]["request"], "history": long_turns}}, sample[1]]
    b = M.make_batch(tok, example, config, "cpu")
    if tt:
        with torch.no_grad():
            ctx = net.encode_context(b["ctx_ids"], b["ctx_mask"])
        torch.onnx.export(
            Context(net),
            (b["ctx_ids"], b["ctx_mask"]),
            str(d / "context.onnx"),
            input_names=["ids", "mask"],
            output_names=["ctx"],
            dynamic_axes={"ids": {0: "rows", 1: "len"}, "mask": {0: "rows", 1: "len"}, "ctx": {0: "rows", 1: "len"}},
            opset_version=17,
            dynamo=False,
        )
        torch.onnx.export(
            Line(net),
            (b["line_ids"], b["line_mask"], ctx, b["ctx_mask"], b["num"]),
            str(d / "line.onnx"),
            input_names=["ids", "mask", "ctx", "ctx_mask", "num"],
            output_names=["intent", "respond", "unclear"],
            dynamic_axes={
                "ids": {0: "rows", 1: "len"},
                "mask": {0: "rows", 1: "len"},
                "ctx": {0: "rows", 1: "ctx_len"},
                "ctx_mask": {0: "rows", 1: "ctx_len"},
                "num": {0: "rows"},
                **outs,
            },
            opset_version=17,
            dynamo=False,
        )
    else:
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
                **outs,
            },
            opset_version=17,
            dynamo=False,
        )
    tok.save_pretrained(str(d / "tok"))
    # Saved with truncation and padding off: a fast tokenizer keeps the settings of its last call,
    # and the two-tower line's 96 tokens would otherwise cut every history (exp-036).
    from tokenizers import Tokenizer

    shipped = Tokenizer.from_file(str(d / "tok" / "tokenizer.json"))
    shipped.no_truncation()
    shipped.no_padding()
    shipped.save(str(d / "tokenizer.json"))
    runtime_config = {
        "run_id": run_id,
        "encoder": config["encoder"],
        "input_version": config["input_version"],
        "arch": config.get("arch", "single"),
        "max_len": config["max_len"],
        "ctx_len": config.get("ctx_len"),
        "line_len": config.get("line_len"),
        "text_turns": turns,
        "temperatures": config["temperatures"],
        "thresholds": thresholds,
        "exported_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    (d / "config.json").write_text(__import__("json").dumps(runtime_config, indent=1))

    # Parity: the shipping runtime against PyTorch on the same lines.
    ref = {
        p["row_id"]: p
        for p in M.predict(net, tok, sample, config["max_len"], "cpu", config["temperatures"], batch=32, spec=config)
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

    def latency(int8: bool, folder: pathlib.Path | None = None) -> dict:
        """Per line, one at a time. A two-tower model's history is encoded first, untimed, as it
        would be while the person talks (`prepare`); `cold_1_threads` times both towers."""
        reqs = [SidechatRequest(**r["request"]) for r in sample[:200]]
        timing = {}
        runs = [(4, True), (1, True)] + ([(1, False)] if tt else [])
        for threads, warm in runs:
            m = load(folder or d, threads=threads, int8=int8)
            for q in reqs[:10]:
                m.answer(q)
            ms = []
            for q in reqs:
                if warm:
                    m.prepare(q)
                else:
                    getattr(m, "_cache", {}).clear()
                t0 = time.perf_counter()
                m.answer(q)
                ms.append((time.perf_counter() - t0) * 1000)
            ms.sort()
            timing[f"{threads}_threads" if warm else f"cold_{threads}_threads"] = {
                "p50_ms": round(statistics.median(ms), 2),
                "p95_ms": round(ms[int(0.95 * len(ms))], 2),
            }
        return timing

    fp32 = {"parity": parity(load(d, threads=4)), "latency_modal_cpu": latency(False)}

    # ONNX Runtime's transformer optimizer fuses layer norms, GELU and, where its patterns match,
    # attention. The fused graph replaces model.onnx only if it keeps parity and is faster on one
    # thread; int8 is then built from whichever graph ships.
    optimized: dict = {}
    try:
        import shutil

        from onnxruntime.transformers.optimizer import optimize_model

        e_cfg = net.enc.config
        o = d / "opt"
        o.mkdir()
        fused: dict = {}
        for g in graphs:
            om = optimize_model(
                str(d / f"{g}.onnx"),
                model_type="bert",
                num_heads=e_cfg.num_attention_heads,
                hidden_size=e_cfg.hidden_size,
                use_gpu=False,
            )
            om.save_model_to_file(str(o / f"{g}.onnx"))
            fused[g] = {k: v for k, v in (om.get_fused_operator_statistics() or {}).items() if v}
        for name in ("tokenizer.json", "config.json"):
            shutil.copy(d / name, o / name)
        po, lo = parity(load(o, threads=4)), latency(False, o)
        base_ms, opt_ms = fp32["latency_modal_cpu"]["1_threads"]["p50_ms"], lo["1_threads"]["p50_ms"]
        keeps = po["decisions_same"] >= fp32["parity"]["decisions_same"] - 1 and po["max_prob_diff"] <= max(
            0.01, 2 * fp32["parity"]["max_prob_diff"]
        )
        optimized = {
            "fused": fused,
            "parity": po,
            "latency_modal_cpu": lo,
            "shipped": bool(keeps and opt_ms < 0.95 * base_ms),
        }
        if optimized["shipped"]:
            for g in graphs:
                shutil.copy(o / f"{g}.onnx", d / f"{g}.onnx")
            fp32 = {"parity": po, "latency_modal_cpu": lo}
    except Exception as e:  # noqa: BLE001 - the plain export stands on its own
        optimized = {"error": f"{type(e).__name__}: {e}"[:500], "shipped": False}

    # int8: weights only, per channel, and only matrix products with a constant side. Quantizing
    # every MatMul (attention scores included) wrecked round 1's model (exp-018). Weights in 7 bits
    # (`reduce_range`), so u8 x s8 products cannot saturate on CPUs without VNNI, and each layer's
    # MLP output product left in fp32: together they keep 281 of 283 parity decisions where the
    # earlier recipe kept 176 (exp-067, exp-068).
    int8_error = None
    try:
        from onnxruntime.quantization import QuantType, quantize_dynamic

        for g in graphs:
            quantize_dynamic(
                str(d / f"{g}.onnx"),
                str(d / f"{g}-int8.onnx"),
                weight_type=QuantType.QInt8,
                per_channel=True,
                reduce_range=True,
                op_types_to_quantize=["MatMul"],
                nodes_to_exclude=int8_excluded(d / f"{g}.onnx"),
                extra_options={"MatMulConstBOnly": True},
            )
    except Exception as e:  # noqa: BLE001 - the fp32 export stands on its own
        int8_error = f"{type(e).__name__}: {e}"[:500]
    size_mb = round(sum((d / f"{g}.onnx").stat().st_size for g in graphs) / 1e6, 1)
    names = [f"{g}.onnx" for g in graphs] + ["tokenizer.json", "config.json"]

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
                "size_mb": round(sum((d / f"{g}-int8.onnx").stat().st_size for g in graphs) / 1e6, 1),
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
                names[len(graphs) : len(graphs)] = [f"{g}-int8.onnx" for g in graphs]
    for g in graphs:  # a stale int8 build from an earlier export
        stale = _model_key(run_id, f"export/{g}-int8.onnx")
        if f"{g}-int8.onnx" not in names and r2.get_bytes(s3, stale) is not None:
            r2.delete(s3, stale)
    for name in names:
        r2.put_bytes(s3, _model_key(run_id, f"export/{name}"), (d / name).read_bytes())
    timing = fp32["latency_modal_cpu"]
    result = {
        "run_id": run_id,
        "size_mb": size_mb,
        "parity": fp32["parity"],
        "latency_modal_cpu": timing,
        "thresholds": thresholds,
        "optimized": optimized,
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
        f"- Transformer optimizer: {'shipped' if optimized.get('shipped') else 'not shipped'}; "
        f"{optimized.get('fused') or optimized.get('error')}"
        + (
            f"; the fused graph took {optimized['latency_modal_cpu']['1_threads']['p50_ms']} ms on 1 thread"
            if optimized.get("latency_modal_cpu")
            else ""
        )
        + ".\n"
    )
    if tt:
        report += (
            f"- Two towers: the line alone (history cached) as above; both towers cold on 1 thread "
            f"{timing['cold_1_threads']['p50_ms']} ms median.\n"
        )
    if int8 and int8.get("shipped"):
        p8, t8l, dv = int8["parity_vs_fp32_torch"], int8["latency_modal_cpu"], int8["dev_anonymous"]
        report += (
            f"\n## int8 build (`{'`, `'.join(g + '-int8.onnx' for g in graphs)}`, load with `int8=True`)\n\n"
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
