"""Why the default build's int8 export fails parity, and which int8 recipe keeps it (exp-067).

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.int8_probe::run --exp exp-067-side-int8-probe

Rounds 8 and 9's 150M int8 builds kept only 178 of 283 pilot decisions (rc0.3 ships fp32 only);
round 3's passed. This takes a run's exported fp32 graph from R2 and builds int8 variants with
`quantize_dynamic`, each leaving different matrix products in fp32, then measures each against the
fp32 graph on the export's own parity lines (decisions at the run's thresholds, largest probability
difference) and its speed on one thread. Nothing is published; a recipe that keeps parity goes into
`export.py` afterwards.

Writes runs/side/results/<exp>/: status.json, scorecard.json, report.md.

`--make` instead makes the int8 file with export.py's recipe (exp-068) and puts it through the
export's own gate: parity on those lines, then dev (anonymous, AMI's real dev lines with the run's
own hold bar) at thresholds of its own, at most 1 point below fp32. It writes model-int8.onnx and a
config.json carrying `thresholds_int8` to models/side/<run_id>/export-int8/, beside the released
export, which it leaves alone. A two-tower model gets context-int8.onnx and line-int8.onnx.

`--check` scores that int8 file, at its own thresholds, on the test sets the gates use and compares
each with fp32's stored card (exp-070).
"""

from __future__ import annotations

import modal

from sidechat.pipeline.train import _secrets, hf_cache, image

APP_NAME = "waystone-side-int8-probe"
app = modal.App(APP_NAME)

# Matrix-product groups in an Ettin (ModernBERT) layer, by node name.
GROUPS = {
    "attn_qkv": ("attn", "Wqkv"),
    "attn_out": ("attn", "Wo"),
    "mlp_in": ("mlp", "Wi"),
    "mlp_out": ("mlp", "Wo"),
}


def graph_names(config: dict) -> list[str]:
    """The exported graphs: `context` and `line` for a two-tower model, `model` otherwise."""
    return ["context", "line"] if config.get("arch") == "twotower" else ["model"]


def group_of(name: str) -> str:
    for g, parts in GROUPS.items():
        if all(p in name for p in parts):
            return g
    return "other"


def layer_of(name: str) -> int | None:
    import re

    m = re.search(r"layers\.(\d+)", name)
    return int(m.group(1)) if m else None


@app.function(image=image, cpu=8.0, memory=16384, timeout=2 * 3600, secrets=_secrets(), volumes={"/cache": hf_cache})
def run(
    exp: str,
    run_id: str = "side-r9-ettin-150m-s1",
    parity_rows: int = 300,
    combos: bool = False,
    make: bool = False,
    check: bool = False,
    check_sets: str = "",
) -> dict:
    """`combos` runs the second set (exp-068): the fixes the first set found, together. `make` makes
    the shipping int8 file instead (exp-069)."""
    import pathlib
    import random
    import shutil
    import statistics
    import time
    import traceback
    from collections import Counter
    from datetime import UTC, datetime

    import onnx
    from onnxruntime.quantization import QuantType, quantize_dynamic

    from sidechat import conditions
    from sidechat.lib import r2
    from sidechat.runtime import load
    from sidechat.schema import SidechatRequest
    from sidechat.sources import build

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    started = time.monotonic()
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {
            "run_id": run_id,
            "parity_rows": parity_rows,
            "combos": combos,
            "make": make,
            "check": check,
            "check_sets": check_sets,
        },
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    try:
        save(stage="downloading the fp32 export")
        base = pathlib.Path("/tmp/base")
        base.mkdir(parents=True, exist_ok=True)
        (base / "config.json").write_bytes(r2.get_bytes(s3, f"models/side/{run_id}/export/config.json"))
        config = __import__("json").loads((base / "config.json").read_text())
        thresholds = config["thresholds"]
        graphs = graph_names(config)
        for name in ("tokenizer.json", *(f"{g}.onnx" for g in graphs)):
            (base / name).write_bytes(r2.get_bytes(s3, f"models/side/{run_id}/export/{name}"))

        # The export's own parity lines.
        rows, _, _ = build.build_rows("pilot-0.4")
        rng = random.Random(0)
        sample = rng.sample(rows, min(parity_rows, len(rows)))
        sample = [conditions.apply(r, rng.choice(conditions.CONDITIONS)) for r in sample]
        reqs = [SidechatRequest(**r["request"]) for r in sample]

        save(stage="fp32 reference")
        fp32 = load(base, threads=4)
        ref = fp32.answers(reqs)
        ref_dec = [fp32.decide(a, thresholds) for a in ref]

        def timed(model) -> dict:
            ms = []
            for q in reqs[:120]:
                t0 = time.perf_counter()
                model.answer(q)
                ms.append(1000 * (time.perf_counter() - t0))
            return {"p50": round(statistics.median(ms), 1), "mean": round(statistics.fmean(ms), 1)}

        fp32_1 = load(base, threads=1)
        results: dict = {"fp32": {"latency_1_thread": timed(fp32_1)}}
        # int8 kernels differ by instruction set: without VNNI, u8 x s8 products can saturate.
        info = pathlib.Path("/proc/cpuinfo").read_text() if pathlib.Path("/proc/cpuinfo").exists() else ""
        flags = next((ln.split(":", 1)[1].split() for ln in info.splitlines() if ln.startswith("flags")), [])
        model_name = next((ln.split(":", 1)[1].strip() for ln in info.splitlines() if ln.startswith("model name")), "")
        results["cpu"] = {
            "model": model_name,
            "vnni": sorted(f for f in flags if "vnni" in f),
            "avx512": any(f.startswith("avx512") for f in flags),
        }

        graph = onnx.load(str(base / f"{graphs[-1]}.onnx"), load_external_data=False)
        inits = {i.name for i in graph.graph.initializer}
        mm = [n.name for n in graph.graph.node if n.op_type == "MatMul" and any(x in inits for x in n.input)]
        layers = sorted({x for x in (layer_of(n) for n in mm) if x is not None})
        results["graph"] = {
            "matmuls_with_weights": len(mm),
            "by_group": dict(Counter(group_of(n) for n in mm)),
            "layers": len(layers),
            "sample_names": mm[:6],
        }
        del graph

        def variant(name: str, exclude: list[str], **kw) -> None:
            save(stage=f"variant {name}")
            d = pathlib.Path(f"/tmp/v-{name}")
            d.mkdir(parents=True, exist_ok=True)
            for f in ("model.onnx", "tokenizer.json", "config.json"):
                if not (d / f).exists():
                    shutil.copy(base / f, d / f)
            opts = {"MatMulConstBOnly": True, **kw.pop("extra", {})}
            quantize_dynamic(
                str(d / "model.onnx"),
                str(d / "model-int8.onnx"),
                weight_type=kw.pop("weight_type", QuantType.QInt8),
                per_channel=kw.pop("per_channel", True),
                reduce_range=kw.pop("reduce_range", False),
                op_types_to_quantize=["MatMul"],
                nodes_to_exclude=exclude,
                extra_options=opts,
            )
            m = load(d, threads=4, int8=True)
            got = m.answers(reqs)
            same = sum(m.decide(a, thresholds) == r for a, r in zip(got, ref_dec))
            diffs = [abs(a.respond - b.respond) for a, b in zip(got, ref)]
            results[name] = {
                "excluded": len(exclude),
                "decisions_same": same,
                "rows": len(reqs),
                "max_respond_diff": round(max(diffs), 4),
                "mean_respond_diff": round(statistics.fmean(diffs), 4),
                "size_mb": round((d / "model-int8.onnx").stat().st_size / 1e6, 1),
                "latency_1_thread": timed(load(d, threads=1, int8=True)),
            }
            shutil.rmtree(d, ignore_errors=True)
            r2.put_json(s3, f"{out}/scorecard.json", {"exp": exp, "run_id": run_id, "results": results})

        def names(*groups: str, layers_in: set[int] | None = None) -> list[str]:
            return [n for n in mm if group_of(n) in groups and (layers_in is None or layer_of(n) in layers_in)]

        last = max(layers) if layers else 0
        if check:
            return _check(s3, out, run_id, base, save, check_sets)
        if make:
            return _build(s3, out, run_id, base, config, reqs, ref, ref_dec, thresholds, results, timed, save)
        if len(graphs) > 1:
            raise ValueError("the recipe search reads one graph; a two-tower model takes --make or --check only")
        if combos:
            variant("per tensor", [], per_channel=False)
            variant("per tensor, reduce range", [], per_channel=False, reduce_range=True)
            variant("per tensor, no mlp_out", names("mlp_out"), per_channel=False)
            variant("reduce range, no mlp_out", names("mlp_out"), reduce_range=True)
            variant("per tensor, reduce range, no mlp_out", names("mlp_out"), per_channel=False, reduce_range=True)
            variant("reduce range, no mlp", names("mlp_in", "mlp_out"), reduce_range=True)
            variant("uint8 weights, per channel", [], weight_type=QuantType.QUInt8)
            variant("uint8 weights, per tensor", [], weight_type=QuantType.QUInt8, per_channel=False)
            layers = []  # no per-layer scan
        else:
            variant("all (as shipped before)", [])
            variant("all but the heads", names("other"))
            variant("no mlp_out", names("mlp_out"))
            variant("no mlp", names("mlp_in", "mlp_out"))
            variant("no attention", names("attn_qkv", "attn_out"))
            variant("no first and last two layers", [n for n in mm if layer_of(n) in {0, last - 1, last}])
            variant("no mlp_out, no heads", names("mlp_out", "other"))
            variant("per tensor", [], per_channel=False)
            variant("reduce range", [], reduce_range=True)
            variant("uint8 weights, reduce range", [], weight_type=QuantType.QUInt8, reduce_range=True)
        # Each layer's MLP output on its own: which layers carry the error.
        best_single = None
        for i in layers:
            keep = [n for n in names("mlp_out") if layer_of(n) == i]
            if not keep:
                continue
            variant(f"no mlp_out in layer {i}", keep)
            r = results[f"no mlp_out in layer {i}"]
            if best_single is None or r["decisions_same"] > results[best_single]["decisions_same"]:
                best_single = f"no mlp_out in layer {i}"

        lines = [
            f"# Why the default build's int8 fails parity ({exp})",
            "",
            (
                f"`{run_id}`'s fp32 export against int8 variants on the export's {len(reqs)} parity lines "
                f"(pilot-0.4, mixed speaker conditions), decisions at its thresholds "
                f"(respond {thresholds['respond']}, wait {thresholds['wait']}). fp32 on one thread: "
                f"{results['fp32']['latency_1_thread']['p50']} ms a line (p50). Graph: {results['graph']}. "
                f"CPU: {results['cpu']}."
            ),
            "",
            "| Variant | MatMuls in fp32 | Decisions same | Largest respond difference | Mean | MB | ms a line, 1 thread |",
            "|---|---|---|---|---|---|---|",
        ]
        for k, v in results.items():
            if k in ("fp32", "graph", "cpu"):
                continue
            lines.append(
                f"| {k} | {v['excluded']} | {v['decisions_same']}/{v['rows']} | {v['max_respond_diff']} | "
                f"{v['mean_respond_diff']} | {v['size_mb']} | {v['latency_1_thread']['p50']} |"
            )
        r2.put_json(s3, f"{out}/scorecard.json", {"exp": exp, "run_id": run_id, "results": results})
        r2.put_text(s3, f"{out}/report.md", "\n".join(lines) + "\n")
        save(state="done", stage="done")
        return {"state": "done"}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise


def _build(s3, out, run_id, base, config, reqs, ref, ref_dec, thresholds, results, timed, save) -> dict:
    import json
    import statistics

    from onnxruntime.quantization import QuantType, quantize_dynamic

    from sidechat import conditions
    from sidechat.lib import r2
    from sidechat.pipeline.export import int8_excluded
    from sidechat.pipeline.train import _corpus_rows, _is_real
    from sidechat.runtime import load
    from sidechat.schema import SidechatRequest
    from sidechat.sources import build
    from sidechat.train import evaluate as E

    save(stage="building int8")
    graphs = graph_names(config)
    excluded = []
    for g in graphs:
        skip = int8_excluded(base / f"{g}.onnx")
        excluded += skip
        quantize_dynamic(
            str(base / f"{g}.onnx"),
            str(base / f"{g}-int8.onnx"),
            weight_type=QuantType.QInt8,
            per_channel=True,
            reduce_range=True,
            op_types_to_quantize=["MatMul"],
            nodes_to_exclude=skip,
            extra_options={"MatMulConstBOnly": True},
        )
    q4 = load(base, threads=4, int8=True)
    got = q4.answers(reqs)
    same = sum(q4.decide(a, thresholds) == r for a, r in zip(got, ref_dec))
    diffs = [abs(a.respond - b.respond) for a, b in zip(got, ref)]
    parity = {
        "rows": len(reqs),
        "decisions_same": same,
        "max_respond_diff": round(max(diffs), 4),
        "mean_respond_diff": round(statistics.fmean(diffs), 4),
    }
    ok = same >= 0.95 * len(reqs)
    card = r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json") or {}
    train_config = card.get("config") or {}
    dev_card = None
    t8 = None
    if ok:
        save(stage="dev at thresholds of its own")
        dev = [
            conditions.apply(r, "anonymous")
            for r in _corpus_rows(s3, train_config["corpus"], {"dev"}, safe_only=True)
            if not _is_real(r)
        ]
        real = [conditions.apply(r, "anonymous") for r in build.build_rows("ami-silent:dev")[0]]
        q8 = load(base, threads=8, int8=True)
        preds8 = {}
        both = dev + real
        for i in range(0, len(both), 64):
            part = both[i : i + 64]
            for r, a in zip(part, q8.answers([SidechatRequest(**r["request"]) for r in part])):
                preds8[r["row_id"]] = {"row_id": r["row_id"], **a.model_dump(include={"intent", "respond", "unclear"})}
        t8 = E.choose_thresholds(
            preds8, dev, real_rows=real, max_held_real=float((card.get("thresholds") or {}).get("max_held_real") or 0.0)
        )
        preds32 = {
            p["row_id"]: p for p in r2.get_jsonl(s3, f"{r2.PREFIX}/predictions/{run_id}/dev@anonymous.jsonl") or []
        }
        dev32 = E.set_card(dev, preds32, thresholds)["sidechat"]
        dev8 = E.set_card(dev, preds8, t8)["sidechat"]
        gap = dev32["decision_right"]["value"] - dev8["decision_right"]["value"]
        dev_card = {"int8": dev8, "fp32": dev32, "gap_points": round(100 * gap, 2), "thresholds_int8": t8}
        ok = gap <= 0.01
    q1 = timed(load(base, threads=1, int8=True))
    results["int8"] = {
        "recipe": "per channel, reduce_range, MatMul with constant B only, each layer's mlp.Wo left in fp32",
        "excluded": len(excluded),
        "parity_vs_fp32_onnx": parity,
        "dev": dev_card,
        "size_mb": round(sum((base / f"{g}-int8.onnx").stat().st_size for g in graphs) / 1e6, 1),
        "latency_1_thread": q1,
        "passes": ok,
    }
    if ok:
        save(stage="uploading")
        folder = f"models/side/{run_id}/export-int8"
        for g in graphs:
            r2.put_bytes(s3, f"{folder}/{g}-int8.onnx", (base / f"{g}-int8.onnx").read_bytes())
        cfg = {**config, "thresholds_int8": t8, "int8_recipe": results["int8"]["recipe"]}
        r2.put_bytes(s3, f"{folder}/config.json", json.dumps(cfg, indent=1).encode())
        results["int8"]["uploaded_to"] = folder
    r2.put_json(s3, f"{out}/scorecard.json", {"exp": out.rsplit("/", 1)[-1], "run_id": run_id, "results": results})
    lines = [
        f"# int8 for `{run_id}` ({out.rsplit('/', 1)[-1]})",
        "",
        (
            f"Recipe: {results['int8']['recipe']}. Parity against fp32 on {parity['rows']} pilot lines: "
            f"{parity['decisions_same']} decisions the same, largest respond difference {parity['max_respond_diff']}, "
            f"mean {parity['mean_respond_diff']}."
        ),
        "",
    ]
    if dev_card:
        lines.append(
            f"Dev (anonymous): fp32 {100 * dev_card['fp32']['decision_right']['value']:.2f}% right at its "
            f"thresholds, int8 {100 * dev_card['int8']['decision_right']['value']:.2f}% at its own "
            f"({dev_card['thresholds_int8']}); gap {dev_card['gap_points']} points (bar 1)."
        )
    lines += [
        "",
        (
            f"One thread: fp32 {results['fp32']['latency_1_thread']['p50']} ms a line, int8 {q1['p50']} ms "
            f"(p50). {results['int8']['size_mb']} MB."
        ),
        "",
        f"**{'Passes' if ok else 'Fails'}** the export's gate."
        + (f" Written to `{results['int8'].get('uploaded_to')}`." if ok else ""),
    ]
    r2.put_text(s3, f"{out}/report.md", "\n".join(lines) + "\n")
    save(state="done", stage="done")
    return {"state": "done", "passes": ok}


CHECK_SETS = (
    "duplex",
    "ambient",
    "ami",
    "ami-silent:test",
    "ami-stt",
    "pilot-0.4@anonymous",
    "slurp-stt-keyterm",
    "tcl@anonymous",
)


def _check(s3, out, run_id, base, save, check_sets: str = "") -> dict:
    import json

    from sidechat.lib import r2
    from sidechat.lib.score import paired
    from sidechat.runtime import load
    from sidechat.schema import SidechatRequest
    from sidechat.sources import build
    from sidechat.train import evaluate as E

    folder = f"models/side/{run_id}/export-int8"
    cfg = json.loads(r2.get_bytes(s3, f"{folder}/config.json"))
    for g in graph_names(cfg):
        (base / f"{g}-int8.onnx").write_bytes(r2.get_bytes(s3, f"{folder}/{g}-int8.onnx"))
    t8 = cfg["thresholds_int8"]
    card = r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json") or {}
    t32 = card["thresholds"]
    q = load(base, threads=8, int8=True)
    table = {}
    for which in [x for x in check_sets.split(",") if x] or CHECK_SETS:
        save(stage=f"checking {which}")
        rows, manifest, _ = build.build_rows(which)
        rows_id = manifest["rows_id"]
        preds8 = {}
        for i in range(0, len(rows), 64):
            part = rows[i : i + 64]
            for r, a in zip(part, q.answers([SidechatRequest(**r["request"]) for r in part])):
                preds8[r["row_id"]] = {"row_id": r["row_id"], **a.model_dump(include={"intent", "respond", "unclear"})}
        preds32 = {p["row_id"]: p for p in r2.get_jsonl(s3, f"{r2.PREFIX}/predictions/{run_id}/{rows_id}.jsonl") or []}
        c8 = E.set_card(rows, preds8, t8)["sidechat"]
        entry = {"rows": len(rows), "int8": c8}
        if preds32:
            c32 = E.set_card(rows, preds32, t32)["sidechat"]
            d8 = {i: E.decide(preds8[i], t8) for i in preds8}
            d32 = {i: E.decide(preds32[i], t32) for i in preds32 if i in d8}
            ids = sorted(d32)
            expect = {r["row_id"]: r["label"]["expect"] for r in rows}
            quiet = [i for i in ids if expect.get(i) == "ignore"]
            entry |= {
                "fp32": c32,
                "same_decision": sum(d8[i] == d32[i] for i in ids) / max(1, len(ids)),
                "quiet_kept_paired": paired([d32[i] != "respond" for i in quiet], [d8[i] != "respond" for i in quiet]),
            }
        table[rows_id] = entry
        r2.put_json(s3, f"{out}/scorecard.json", {"exp": out.rsplit("/", 1)[-1], "run_id": run_id, "table": table})

    def f(x: dict | None, key: str) -> str:
        v = ((x or {}).get(key) or {}).get("value")
        return "n/a" if v is None else f"{100 * v:.2f}%"

    lines = [
        f"# int8 against fp32 on the test sets (`{run_id}`, {out.rsplit('/', 1)[-1]})",
        "",
        f"int8 at its own thresholds {t8.get('respond')}/{t8.get('wait')}, fp32 at {t32.get('respond')}/{t32.get('wait')}.",
        "",
        "| Set | Rows | Same decision | Right, fp32 | Right, int8 | Others answered, fp32 | int8 | Others held, fp32 | int8 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for rid, e in table.items():
        lines.append(
            f"| {rid} | {e['rows']:,} | {100 * e.get('same_decision', 0):.2f}% | {f(e.get('fp32'), 'decision_right')} | "
            f"{f(e['int8'], 'decision_right')} | {f(e.get('fp32'), 'answers_now_wrongly')} | "
            f"{f(e['int8'], 'answers_now_wrongly')} | {f(e.get('fp32'), 'holds_wrongly')} | {f(e['int8'], 'holds_wrongly')} |"
        )
    r2.put_text(s3, f"{out}/report.md", "\n".join(lines) + "\n")
    save(state="done", stage="done")
    return {"state": "done"}
