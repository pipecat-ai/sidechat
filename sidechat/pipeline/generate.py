"""Generate conversations: plan in code, write with several model families, label from the plan.

Runs detached on Modal:

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.generate::run --exp exp-009-side-gen-trial --gen-id gen-trial --counts o:8,a:8,c:8,b:8

`counts` is conversations per writer: o (open weights, on an H100), a and c (APIs, training and
test), b (API, test only). The driver plans every conversation, starts one function per writer in
parallel, and assembles the rows when they finish. Everything goes to R2:

    runs/side/corpus/<gen_id>/plans.jsonl             every plan, with its cast
    runs/side/corpus/<gen_id>/written/<w>/*.jsonl     each writer's output, as it arrives
    runs/side/corpus/<gen_id>/conversations.jsonl     plan, lines and checks per conversation
    runs/side/corpus/<gen_id>/rows.jsonl              labelled rows, with split tags
    runs/side/corpus/<gen_id>/manifest.json, sample.md
    runs/side/results/<exp>/                          status.json, report.md

A written conversation is never asked for again, so a stopped run resumes.
"""

from __future__ import annotations

import os
import pathlib

import modal

from sidechat.lib.r2 import R2_KEYS

APP_NAME = "waystone-side-generate"
ROOT = pathlib.Path(__file__).resolve().parents[2]
WRITER_KEYS = ("WRITER_A_MODEL", "WRITER_B_MODEL", "WRITER_C_MODEL", "WRITER_O_MODEL", "WRITER_PRICES")
SECRET_KEYS = (*R2_KEYS, "OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GOOGLE_API_KEY", *WRITER_KEYS)
H100_USD_PER_HOUR = 3.95


def _secrets() -> list:
    if not modal.is_local():
        return [modal.Secret.from_dict({})]
    if os.environ.get("MODAL_ENVIRONMENT") != "waystone":
        raise SystemExit("refusing: MODAL_ENVIRONMENT must be 'waystone'. Load .env first: set -a; . ./.env; set +a")
    missing = [k for k in SECRET_KEYS if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"refusing: {', '.join(missing)} not set in .env")
    return [modal.Secret.from_dict({k: os.environ[k] for k in SECRET_KEYS})]


cpu_image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install("anthropic==2.10.0", "httpx==0.28.1", "boto3>=1.40", "pydantic>=2.9", "pyyaml>=6.0")
    .add_local_python_source("sidechat")
    .add_local_dir(str(ROOT / "contracts"), remote_path="/root/contracts")
)
gpu_image = (
    modal.Image.from_registry("nvidia/cuda:13.0.3-devel-ubuntu24.04", add_python="3.12")
    .entrypoint([])
    .uv_pip_install("vllm==0.30.0", "boto3>=1.40", "pyyaml>=6.0", "httpx==0.28.1")
    .env(
        {
            "HF_HUB_DISABLE_TELEMETRY": "1",
            "HF_HOME": "/cache/hf",
            "VLLM_LOGGING_LEVEL": "WARNING",
            "VLLM_USE_DEEP_GEMM": "0",
            "VLLM_USE_FLASHINFER_SAMPLER": "0",
            "CUDA_HOME": "/usr/local/cuda",
        }
    )
    .add_local_python_source("sidechat")
    .add_local_dir(str(ROOT / "contracts"), remote_path="/root/contracts")
)
hf_cache = modal.Volume.from_name("waystone-hf-cache")
app = modal.App(APP_NAME)


def _base(gen_id: str) -> str:
    from sidechat.lib import r2

    return f"{r2.PREFIX}/corpus/{gen_id}"


def _done(s3, gen_id: str, writer: str) -> dict[str, dict]:
    from sidechat.lib import r2

    out = {}
    for obj in r2.list_keys(s3, f"{_base(gen_id)}/written/{writer}/"):
        for rec in r2.get_jsonl(s3, obj["Key"]) or []:
            if rec.get("ok"):
                out[rec["conv_id"]] = rec
    return out


@app.function(
    image=cpu_image,
    cpu=2.0,
    memory=4096,
    timeout=4 * 3600,
    secrets=_secrets(),
    retries=modal.Retries(max_retries=2, initial_delay=30.0),
)
def write_api(gen_id: str, writer: str, items: list[dict], concurrency: int, spend_cap_usd: float) -> dict:
    """Write `items` with an API writer, saving every 25 conversations."""
    import asyncio
    from datetime import UTC, datetime

    from sidechat.gen import writers
    from sidechat.lib import r2

    s3 = r2.client()
    done = _done(s3, gen_id, writer)
    todo = [i for i in items if i["conv_id"] not in done]
    buffer: list[dict] = []
    tally = {"written": len(done), "failed": 0, "usd": 0.0}
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    part = [0]
    lock = asyncio.Lock()

    async def on_done(rec: dict) -> None:
        async with lock:
            buffer.append(rec)
            tally["usd"] += writers.cost(writer, rec["usage"])
            tally["written" if rec["ok"] else "failed"] += 1
            if len(buffer) >= 25:
                r2.put_jsonl(s3, f"{_base(gen_id)}/written/{writer}/{stamp}-{part[0]:04d}.jsonl", list(buffer))
                part[0] += 1
                buffer.clear()
            if tally["usd"] > spend_cap_usd:
                raise RuntimeError(f"writer {writer} passed its cap of ${spend_cap_usd}")

    concurrency = {"a": concurrency, "b": max(4, concurrency // 2), "c": concurrency}[writer]
    try:
        asyncio.run(writers.write_api(writer, todo, concurrency, on_done))
    finally:
        if buffer:
            r2.put_jsonl(s3, f"{_base(gen_id)}/written/{writer}/{stamp}-{part[0]:04d}.jsonl", list(buffer))
    return {"writer": writer, **tally}


@app.function(
    image=gpu_image,
    gpu="H100",
    cpu=8.0,
    memory=65536,
    timeout=4 * 3600,
    secrets=_secrets(),
    volumes={"/cache": hf_cache},
)
def write_open(gen_id: str, items: list[dict], seed: int, shard: int = 0) -> dict:
    """Write `items` with the open-weights writer on vLLM, in batches of 400. Shards run on
    separate GPUs in parallel, each with its own part files."""
    import time
    from datetime import UTC, datetime

    from vllm import LLM, SamplingParams

    from sidechat.gen.writer import SYSTEM, parse_lines
    from sidechat.lib import r2

    s3 = r2.client()
    done = _done(s3, gen_id, "o")
    todo = [i for i in items if i["conv_id"] not in done]
    if not todo:
        return {"writer": "o", "written": len(done), "failed": 0, "gpu_s": 0}
    repo, _, revision = os.environ["WRITER_O_MODEL"].partition("@")
    t0 = time.time()
    llm = LLM(
        model=repo,
        revision=revision or None,
        max_model_len=8192,
        gpu_memory_utilization=0.9,
        kv_cache_dtype="fp8",
        enable_prefix_caching=True,
        seed=seed,
        max_num_seqs=256,
    )
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    written = failed = 0
    for n, start in enumerate(range(0, len(todo), 400)):
        batch = todo[start : start + 400]
        pending = list(batch)
        results: dict[str, dict] = {}
        for attempt in range(3):
            if not pending:
                break
            params = SamplingParams(n=1, temperature=0.9, top_p=0.95, max_tokens=3500, seed=seed + 1000 * attempt + n)
            outs = llm.chat(
                [[{"role": "system", "content": SYSTEM}, {"role": "user", "content": i["prompt"]}] for i in pending],
                params,
                chat_template_kwargs={"enable_thinking": False},
                use_tqdm=False,
            )
            retry = []
            for item, out in zip(pending, outs):
                usage = {"input": len(out.prompt_token_ids), "output": len(out.outputs[0].token_ids)}
                try:
                    results[item["conv_id"]] = {
                        "conv_id": item["conv_id"],
                        "writer": "o",
                        "ok": True,
                        "lines": parse_lines(out.outputs[0].text, item["n"]),
                        "usage": usage,
                        "attempts": attempt + 1,
                    }
                except Exception as e:  # noqa: BLE001
                    results[item["conv_id"]] = {
                        "conv_id": item["conv_id"],
                        "writer": "o",
                        "ok": False,
                        "error": f"{type(e).__name__}: {str(e)[:200]}",
                        "usage": usage,
                    }
                    retry.append(item)
            pending = retry
        recs = list(results.values())
        written += sum(r["ok"] for r in recs)
        failed += sum(not r["ok"] for r in recs)
        r2.put_jsonl(s3, f"{_base(gen_id)}/written/o/{stamp}-s{shard}-{n:04d}.jsonl", recs)
    return {"writer": "o", "written": written + len(done), "failed": failed, "gpu_s": round(time.time() - t0)}


def _cast_to_dict(cast) -> dict:
    return {
        "setting": cast.setting.id,
        "agent": cast.agent,
        "aliases": list(cast.aliases),
        "unnamed": cast.unnamed,
        "people": cast.people,
        "topic": cast.topic,
        "register": cast.register,
        "soundalike": cast.soundalike,
        "heldout": cast.heldout,
    }


def _cast_from_dict(d: dict):
    from sidechat.gen.world import SETTINGS, Cast

    setting = next(s for s in SETTINGS if s.id == d["setting"])
    return Cast(
        setting,
        d["agent"],
        tuple(d["aliases"]),
        d["unnamed"],
        d["people"],
        d["topic"],
        d["register"],
        d.get("soundalike"),
        d.get("heldout", []),
    )


def _beats_from(dicts: list[dict]):
    from sidechat.gen.planner import Beat

    return [Beat(**b) for b in dicts]


@app.function(
    image=cpu_image,
    cpu=2.0,
    memory=8192,
    timeout=8 * 3600,
    secrets=_secrets(),
    retries=modal.Retries(max_retries=1, initial_delay=60.0),
)
def run(
    exp: str,
    gen_id: str,
    counts: str = "o:8,a:8,c:8,b:8",
    seed: int = 1,
    concurrency: int = 24,
    spend_cap_usd: float = 150.0,
    boost: str = "",
    quiet: str = "",
    o_shards: int = 1,
    after_quiet: float = 0.0,
    add: str = "",
    delayed: float = 0.0,
) -> dict:
    """Plan, write and label `counts` conversations per writer. `boost` raises kinds' weights, e.g.
    `follow_up_by_other:3,unclear_after_agent:3`, for a top-up corpus aimed at weak kinds. `quiet`
    is `<share never involving the agent>,<share opening with people only>` (gen-0.2: 0.08,0.25).
    `o_shards` splits the open-weights writer over that many GPUs. `after_quiet` is the chance a
    quiet opening ends with a request the agent could do, put to nobody (gen-0.3: 0.6). `add` gives
    weights to kinds outside the default mix (`relay_agent_answer:2`), and `delayed` is the chance of
    a follow-up to the agent after someone else's brief reaction (gen-0.4)."""
    import random
    import time
    import traceback
    from collections import Counter
    from datetime import UTC, datetime

    from sidechat.gen import planner, world, writers
    from sidechat.gen.rows import conversation_rows
    from sidechat.gen.writer import check, user_prompt
    from sidechat.lib import r2

    s3 = r2.client()
    base, out = _base(gen_id), f"{r2.PREFIX}/results/{exp}"
    started = time.monotonic()
    status = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "planning",
        "gen_id": gen_id,
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {
            "gen_id": gen_id,
            "counts": counts,
            "seed": seed,
            "spend_cap_usd": spend_cap_usd,
            "boost": boost,
            "quiet": quiet,
            "o_shards": o_shards,
            "after_quiet": after_quiet,
            "add": add,
            "delayed": delayed,
        },
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    try:
        want = {w: int(n) for w, n in (x.split(":") for x in counts.split(",") if x)}
        boosts = {k: float(v) for k, v in (x.split(":") for x in boost.split(",") if x)}
        quiet_shares = tuple(float(x) for x in quiet.split(",")) if quiet else (0.0, 0.0)
        added = {k: float(v) for k, v in (x.split(":") for x in add.split(",") if x)}
        plans = r2.get_jsonl(s3, f"{base}/plans.jsonl") or []
        have = Counter(p["writer"] for p in plans)
        for w, n in want.items():
            rng = random.Random(f"{seed}-{w}-{have[w]}")
            for k in range(have[w], n):
                cast = world.make_cast(rng, test_only=(w == writers.HELDOUT_WRITER) or rng.random() < 0.06)
                beats = planner.plan(
                    rng, cast, boost=boosts, quiet=quiet_shares, after_quiet=after_quiet, add=added, delayed=delayed
                )
                plans.append(
                    {
                        "conv_id": f"{w}{seed:02d}-{k:05d}",
                        "writer": w,
                        "cast": _cast_to_dict(cast),
                        "beats": planner.describe(beats),
                        "prompt": user_prompt(cast, beats),
                        "n": len(beats),
                    }
                )
        r2.put_jsonl(s3, f"{base}/plans.jsonl", plans)
        save(stage="writing", planned=dict(Counter(p["writer"] for p in plans)))

        # Every writer in parallel. API writers get a share of the cap each.
        calls = []
        api = [w for w in want if w in writers.API_WRITERS]
        for w in want:
            items = [{"conv_id": p["conv_id"], "prompt": p["prompt"], "n": p["n"]} for p in plans if p["writer"] == w]
            if w == "o":
                shards = max(1, o_shards)
                calls.extend(write_open.spawn(gen_id, items[i::shards], seed + i, i) for i in range(shards))
            else:
                calls.append(write_api.spawn(gen_id, w, items, concurrency, spend_cap_usd / max(1, len(api))))
        results = []
        for c in calls:
            try:
                results.append(c.get())
            except Exception as e:  # noqa: BLE001 - one writer failing does not lose the others
                results.append({"error": f"{type(e).__name__}: {str(e)[:300]}"})
        save(stage="assembling", writers=results)

        # Assemble rows from whatever is written.
        written = {}
        for w in want:
            written.update(_done(s3, gen_id, w))
        convs, rows = [], []
        for p in plans:
            rec = written.get(p["conv_id"])
            if not rec:
                continue
            cast, beats = _cast_from_dict(p["cast"]), _beats_from(p["beats"])
            problems = [[] if b.who == planner.AGENT else check(b, t, cast) for b, t in zip(beats, rec["lines"])]
            rows.extend(
                conversation_rows(
                    gen_id,
                    p["conv_id"],
                    cast,
                    beats,
                    rec["lines"],
                    problems,
                    p["writer"],
                    heldout_writer=p["writer"] == writers.HELDOUT_WRITER,
                )
            )
            convs.append(
                {
                    "conv_id": p["conv_id"],
                    "writer": p["writer"],
                    "cast": p["cast"],
                    "beats": p["beats"],
                    "lines": rec["lines"],
                    "problems": problems,
                    "usage": rec.get("usage", {}),
                }
            )
        sha = r2.put_jsonl(s3, f"{base}/rows.jsonl", rows)
        r2.put_jsonl(s3, f"{base}/conversations.jsonl", convs)

        usage = {}
        for w in want:  # noqa: PLC0206
            recs = [written[p["conv_id"]] for p in plans if p["writer"] == w and p["conv_id"] in written]
            inp = sum(r.get("usage", {}).get("input", 0) for r in recs)
            outp = sum(r.get("usage", {}).get("output", 0) for r in recs)
            usd = (
                writers.cost(w, {"input": inp, "output": outp})
                if w != "o"
                else sum(r.get("gpu_s", 0) for r in results if r.get("writer") == "o") / 3600 * H100_USD_PER_HOUR
            )
            usage[w] = {
                "conversations": len(recs),
                "planned": want[w],
                "input": inp,
                "output": outp,
                "usd": round(usd, 2),
            }
        by = lambda key: dict(Counter(r["tags"][key] if key in r["tags"] else str(r["label"][key]) for r in rows))
        manifest = {
            "gen_id": gen_id,
            "rows": len(rows),
            "conversations": len(convs),
            "rows_sha256": sha,
            "seed": seed,
            "counts": want,
            "writers_env": {w: f"WRITER_{w.upper()}_MODEL" for w in want},
            "heldout_writer": writers.HELDOUT_WRITER,
            "guide": __import__("sidechat.guide", fromlist=["x"]).GUIDE_VERSION,
            "by_split": by("split"),
            "by_writer": by("writer"),
            "by_expect": by("expect"),
            "brief_ok": by("brief_ok"),
            "usage": usage,
            "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        r2.put_json(s3, f"{base}/manifest.json", manifest)
        r2.put_text(s3, f"{base}/sample.md", _sample(convs[:40]))
        r2.put_text(s3, f"{out}/report.md", _report(exp, manifest, rows))
        r2.put_json(s3, f"{out}/scorecard.json", manifest)
        save(
            state="done",
            stage="done",
            rows=len(rows),
            conversations=len(convs),
            usd=round(sum(u["usd"] for u in usage.values()), 2),
        )
        return {"state": "done", "rows": len(rows)}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise


def _sample(convs: list[dict]) -> str:
    from sidechat import guide

    out = ["# Sample conversations", ""]
    for c in convs:
        cast = c["cast"]
        out += [
            f"## {c['conv_id']} (writer {c['writer']}): {cast['setting']}, {cast['topic']}",
            f"Agent {cast['agent']}; people {', '.join(cast['people'])}; {cast['register']}",
            "",
        ]
        for b, line, prob in zip(c["beats"], c["lines"], c["problems"]):
            if b["who"] == "@agent":
                out.append(f"- **{cast['agent']}**: {line}")
            else:
                k = guide.KINDS[b["kind"]]
                flag = f" ⚠ {'; '.join(prob)}" if prob else ""
                out.append(f"- {b['who']}: {line}  `{b['kind']} → {k.expect or 'either'}`{flag}")
        out.append("")
    return "\n".join(out)


def _report(exp: str, m: dict, rows: list[dict]) -> str:
    from collections import Counter

    bad = Counter(r["tags"]["kind"] for r in rows if r["tags"]["brief_ok"] == "0")
    tot = Counter(r["tags"]["kind"] for r in rows)
    lines = [
        f"# Generation: {exp}",
        "",
        f"Corpus `{m['gen_id']}`: {m['conversations']} conversations, {m['rows']} labelled lines.",
        "",
        "| Writer | Planned | Written | Input tokens | Output tokens | Est. cost |",
        "|---|---|---|---|---|---|",
    ]
    for w, u in m["usage"].items():
        lines.append(
            f"| {w} | {u['planned']} | {u['conversations']} | {u['input']:,} | {u['output']:,} | ${u['usd']} |"
        )
    lines += [
        "",
        f"Splits: {m['by_split']}. Labels: {m['by_expect']}. Lines that keep to their brief: {m['brief_ok']}.",
        "",
        "**Kinds whose lines most often break their brief**",
        "",
        "| Kind | Broken | Of |",
        "|---|---|---|",
    ]
    for k, n in bad.most_common(15):
        lines.append(f"| `{k}` | {n} | {tot[k]} |")
    problems = Counter(p for r in rows for p in r["tags"]["brief_problems"].split("; ") if p)
    lines += ["", "**Problems**", ""] + [f"- {p}: {n}" for p, n in problems.most_common(10)]
    return "\n".join(lines) + "\n"
