"""The labelling committee: three large models from three families label every line, blind.

Runs detached on Modal:

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.label::run --exp exp-002-side-committee-pilot --sets pilot-0.2

Then, from any machine with the `.env`:

    uv run python -m sidechat.pipeline.results exp-002-side-committee-pilot

What it writes, all in R2:

    runs/side/rows/<rows_id>/                      the rows of each set, as the baseline job does
    runs/side/committee/<prompt_sha>/<m>/*.jsonl   each member's answers, as they arrive, shared
                                                   by every label set under the same prompt
    runs/side/labels/<label_id>/labels.jsonl       per line: the guide's label, each answer, the vote
    runs/side/labels/<label_id>/manifest.json
    runs/side/results/<exp>/                       status.json, scorecard.json, report.md

Members see the line and its conversation, never its kind or the guide's label. A stored answer
is never asked for again, so a stopped or retried run resumes. The members' model ids come from
`.env` (LABELLER_A_MODEL, ...) and are not written anywhere: R2 keeps a short hash of each, so a
changed model never mixes with old answers.

Stop it with `uv run modal app stop waystone-side-label`.
"""

from __future__ import annotations

import os
import pathlib

import modal

from sidechat.lib.r2 import R2_KEYS

APP_NAME = "waystone-side-label"
ROOT = pathlib.Path(__file__).resolve().parents[2]
SECRET_KEYS = (
    *R2_KEYS,
    "OPENAI_API_KEY",
    "ANTHROPIC_API_KEY",
    "GOOGLE_API_KEY",
    "LABELLER_A_MODEL",
    "LABELLER_B_MODEL",
    "LABELLER_C_MODEL",
    "LABELLER_PRICES",
)
PREFLIGHT = 12  # lines per member before the spend forecast
CHUNK = 60  # lines per member between saves
MAX_FAILED_SHARE = 0.15


def _secrets() -> list:
    if not modal.is_local():
        return [modal.Secret.from_dict({})]
    if os.environ.get("MODAL_ENVIRONMENT") != "waystone":
        raise SystemExit("refusing: MODAL_ENVIRONMENT must be 'waystone'. Load .env first: set -a; . ./.env; set +a")
    missing = [k for k in SECRET_KEYS if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"refusing: {', '.join(missing)} not set in .env")
    return [modal.Secret.from_dict({k: os.environ[k] for k in SECRET_KEYS})]


image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install(
        "anthropic==2.10.0", "httpx==0.28.1", "boto3>=1.40", "pydantic>=2.9", "pyyaml>=6.0", "huggingface-hub>=0.30"
    )
    .add_local_python_source("sidechat")
    .add_local_dir(str(ROOT / "data" / "suites"), remote_path="/root/data/suites")
    .add_local_dir(str(ROOT / "contracts"), remote_path="/root/contracts")
)

app = modal.App(APP_NAME)


class Stopped(Exception):
    pass


def _sha(text: str, n: int = 16) -> str:
    import hashlib

    return hashlib.sha256(text.encode()).hexdigest()[:n]


@app.function(
    name="label_run",
    image=image,
    cpu=2.0,
    memory=4096,
    timeout=6 * 3600,
    secrets=_secrets(),
    retries=modal.Retries(max_retries=2, backoff_coefficient=1.0, initial_delay=30.0),
)
def run(
    exp: str,
    sets: str = "pilot-0.2",
    label_id: str = "",
    members: str = "a,b,c",
    concurrency: int = 8,
    spend_cap_usd: float = 25.0,
    limit: int = 0,
) -> dict:
    """Label every line of `sets` with the committee and score agreement with the guide.

    `label_id` defaults to `<first set>-committee-<guide version>`. `limit` keeps the first
    conversations of each set; give a trial run its own `exp` and `label_id`.
    """
    import asyncio
    import time
    import traceback
    from datetime import UTC, datetime

    from sidechat.committee import agreement, prompt
    from sidechat.committee import members as mem
    from sidechat.committee.vote import committee_label, vote
    from sidechat.guide import GUIDE_VERSION
    from sidechat.lib import r2
    from sidechat.schema import SidechatRequest
    from sidechat.sources import build

    s3 = r2.client()
    chosen = [m.strip() for m in members.split(",") if m.strip()]
    set_names = [x.strip() for x in sets.split(",") if x.strip()]
    label_id = label_id or f"{set_names[0]}-committee-{GUIDE_VERSION.rsplit('-', 1)[-1]}"
    out = f"{r2.PREFIX}/results/{exp}"
    base = f"{r2.PREFIX}/labels/{label_id}"
    started = time.monotonic()
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {
            "sets": sets,
            "label_id": label_id,
            "members": members,
            "concurrency": concurrency,
            "spend_cap_usd": spend_cap_usd,
            "limit": limit,
        },
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    try:
        prices = mem.prices()
        if any(m not in prices for m in chosen):
            raise Stopped("LABELLER_PRICES must give a price for every member, e.g. a:2/10,b:4/20,c:2/10")
        model_sha = {m: _sha(mem.model(m), 10) for m in chosen}

        # 1. Rows.
        rows: list[dict] = []
        for which in set_names:
            save(stage=f"building rows: {which}")
            set_rows, manifest, _ = build.build_rows(which, limit)
            rows_id = manifest["rows_id"]
            manifest["sha256"] = r2.put_jsonl(s3, f"{r2.PREFIX}/rows/{rows_id}/rows.jsonl", set_rows)
            manifest["r2_key"] = f"{r2.PREFIX}/rows/{rows_id}/rows.jsonl"
            r2.put_json(s3, f"{r2.PREFIX}/rows/{rows_id}/manifest.json", manifest)
            rows.extend(set_rows)
        by_id = {r["row_id"]: r for r in rows}
        save(sets={rows_id: n for rows_id, n in __import__("collections").Counter(r["set"] for r in rows).items()})

        # 2. Answers.
        system = prompt.system_prompt()
        psha = prompt.prompt_sha()
        users = {r["row_id"]: prompt.user_message(SidechatRequest(**r["request"])) for r in rows}
        key = {(m, i): _sha(f"{m}|{model_sha[m]}|{psha}|{users[i]}", 24) for m in chosen for i in by_id}
        # Answers depend on the member, its model, the prompt and the line, never on the label set,
        # so they are stored once per prompt and shared by every label set that asks the same thing.
        answers_base = f"{r2.PREFIX}/committee/{psha}"
        wanted = {m: {key[(m, i)] for i in by_id} for m in chosen}
        done: dict[str, dict[str, dict]] = {m: {} for m in chosen}
        sources = [f"{answers_base}/{{m}}/"] + [  # older runs kept them under their label set
            f"{r2.PREFIX}/labels/{d}/parts/{{m}}/"
            for d in sorted({o["Key"].split("/")[3] for o in r2.list_keys(s3, f"{r2.PREFIX}/labels/")})
        ]
        for m in chosen:
            for pattern in sources:
                for obj in r2.list_keys(s3, pattern.format(m=m)):
                    for rec in r2.get_jsonl(s3, obj["Key"]) or []:
                        if rec.get("ok") and rec["key"] in wanted[m]:
                            done[m][rec["key"]] = rec
        reused = {m: sum(1 for i in by_id if key[(m, i)] in done[m]) for m in chosen}
        todo = {m: [i for i in by_id if key[(m, i)] not in done[m]] for m in chosen}
        tally = {
            m: {
                "answered": reused[m],
                "reused": reused[m],
                "failed": 0,
                "fallback": 0,
                "input": 0,
                "cached": 0,
                "cache_write": 0,
                "output": 0,
                "usd": 0.0,
                "errors": [],
            }
            for m in chosen
        }

        def progress(forecast=None) -> None:
            save(
                stage="labelling",
                progress={
                    m: {k: t[k] for k in ("answered", "reused", "failed", "usd")} | {"of": len(rows)}
                    for m, t in tally.items()
                },
                usd=round(sum(t["usd"] for t in tally.values()), 3),
                forecast=forecast,
            )

        async def label_all() -> None:
            import anthropic
            import httpx

            asks = {"a": mem.ask_a, "b": mem.ask_b, "c": mem.ask_c}
            async with httpx.AsyncClient(limits=httpx.Limits(max_connections=64)) as http:
                claude = anthropic.AsyncAnthropic(max_retries=4, timeout=180.0)
                clients = {"a": http, "b": claude, "c": http}
                gates = {m: asyncio.Semaphore(concurrency) for m in chosen}
                stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
                part_no = {m: 0 for m in chosen}

                async def one(m: str, i: str) -> dict:
                    async with gates[m]:
                        reply = await asks[m](clients[m], system, users[i])
                    return {
                        "key": key[(m, i)],
                        "row_id": i,
                        "member": m,
                        "model_sha": model_sha[m],
                        "prompt_sha": psha,
                        "ok": reply.ok,
                        "answer": reply.answer,
                        "error": reply.error,
                        "usage": reply.usage,
                        "served_by_configured_model": reply.served_by_configured_model,
                        "ms": reply.ms,
                        "attempts": reply.attempts,
                    }

                async def batch(per_member: dict[str, list[str]]) -> None:
                    jobs = [(m, i) for m, ids in per_member.items() for i in ids]
                    results = await asyncio.gather(*(one(m, i) for m, i in jobs))
                    for m in chosen:
                        mine = [x for x in results if x["member"] == m]
                        if not mine:
                            continue
                        r2.put_jsonl(s3, f"{answers_base}/{m}/{stamp}-{part_no[m]:04d}.jsonl", mine)
                        part_no[m] += 1
                        t = tally[m]
                        for x in mine:
                            for k in ("input", "cached", "cache_write", "output"):
                                t[k] += x["usage"].get(k, 0)
                            t["usd"] += mem.cost_usd(m, x["usage"], prices[m])
                            t["fallback"] += 0 if x["served_by_configured_model"] else 1
                            if x["ok"]:
                                done[m][x["key"]] = x
                                t["answered"] += 1
                            else:
                                t["failed"] += 1
                                if len(t["errors"]) < 5:
                                    t["errors"].append(f"{x['row_id']}: {x['error']}")

                try:
                    first = {m: todo[m][:PREFLIGHT] for m in chosen}
                    await batch(first)
                    asked = {m: len(first[m]) for m in chosen}
                    forecast = {}
                    for m in chosen:
                        if asked[m]:
                            per_line = tally[m]["usd"] / asked[m]
                            forecast[m] = round(per_line * len(todo[m]), 2)
                    forecast_total = round(sum(forecast.values()), 2)
                    progress({"usd": forecast_total, "by_member": forecast, "spend_cap_usd": spend_cap_usd})
                    if forecast_total > spend_cap_usd:
                        raise Stopped(f"forecast ${forecast_total} is over the cap of ${spend_cap_usd}")
                    for m in chosen:
                        if asked[m] and tally[m]["failed"] / asked[m] > MAX_FAILED_SHARE:
                            raise Stopped(
                                f"member {m}: {tally[m]['failed']} of {asked[m]} failed: {tally[m]['errors'][:2]}"
                            )
                    position = PREFLIGHT
                    while any(position < len(todo[m]) for m in chosen):
                        await batch({m: todo[m][position : position + CHUNK] for m in chosen})
                        position += CHUNK
                        progress({"usd": forecast_total, "by_member": forecast, "spend_cap_usd": spend_cap_usd})
                        spent = sum(t["usd"] for t in tally.values())
                        if spent > spend_cap_usd:
                            raise Stopped(f"spent about ${spent:.2f}, over the cap of ${spend_cap_usd}")
                        for m in chosen:
                            n = tally[m]["answered"] + tally[m]["failed"] - reused[m]
                            if n and tally[m]["failed"] / n > MAX_FAILED_SHARE:
                                raise Stopped(
                                    f"member {m}: {tally[m]['failed']} of {n} failed: {tally[m]['errors'][:2]}"
                                )
                finally:
                    await claude.close()

        save(stage="labelling", progress={m: {"answered": reused[m], "of": len(rows)} for m in chosen})
        try:
            asyncio.run(label_all())
        except mem.MemberRefused as e:
            raise Stopped(f"a member was refused: {e}") from e

        # 3. Vote, store, score.
        save(stage="voting and scoring")
        answers = {m: {i: (done[m].get(key[(m, i)]) or {}).get("answer") for i in by_id} for m in chosen}
        votes = {i: vote({m: answers[m][i] for m in chosen}) for i in by_id}
        labels = []
        for i, r in by_id.items():
            c = committee_label(votes[i])
            labels.append(
                {
                    "row_id": i,
                    "set": r["set"],
                    "conv_id": r["conv_id"],
                    "tags": r["tags"],
                    "guide": r["label"],
                    "members": {m: answers[m][i] for m in chosen},
                    "vote": votes[i],
                    "committee": c.model_dump(mode="json") if c else None,
                }
            )
        sha = r2.put_jsonl(s3, f"{base}/labels.jsonl", labels)
        usage = {m: {**{k: v for k, v in t.items() if k != "usd"}, "usd": round(t["usd"], 3)} for m, t in tally.items()}
        r2.put_json(
            s3,
            f"{base}/manifest.json",
            {
                "label_id": label_id,
                "guide": GUIDE_VERSION,
                "prompt_sha": psha,
                "members": chosen,
                "member_model_env": {m: mem.MODEL_ENV[m] for m in chosen},
                "member_model_sha": model_sha,
                "effort": mem.EFFORT,
                "sets": set_names,
                "rows": len(rows),
                "labels_sha256": sha,
                "exp": exp,
                "usage": usage,
                "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
            },
        )
        meta = {
            "exp": exp,
            "label_id": label_id,
            "sets": set_names,
            "guide": GUIDE_VERSION,
            "prompt_sha": psha,
            "members": chosen,
            "usage": usage,
            "limit": limit or None,
            "finished_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        card = agreement.build(rows, answers, votes, meta)
        r2.put_json(s3, f"{out}/scorecard.json", card)
        r2.put_text(s3, f"{out}/report.md", agreement.render(card))
        save(
            state="done",
            stage="done",
            usd=round(sum(t["usd"] for t in tally.values()), 3),
            headline={"majority_decision": card["majority"]["decision"], "meets_target": card["meets_target"]},
        )
        return {"state": "done", "results": out}
    except Stopped as e:
        save(state="stopped", reason=str(e))
        return {"state": "stopped", "reason": str(e)}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
