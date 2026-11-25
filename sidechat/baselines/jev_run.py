"""Score rows with Jev, resumably.

Every answer is written to R2 in small part files as it arrives, keyed by the exact request it
answers. A run that is stopped, retried or started again reads the parts first and asks Jev only
for what is still missing. A stored answer is never asked for twice, which also freezes the
baseline: later runs compare against the same numbers.

Runs inside the Modal job (`sidechat/pipeline/baseline.py`). Needs `JEV_API_KEY` and
`pipecat-ai[typesafe]`, the client the demo itself uses.
"""

from __future__ import annotations

import asyncio
import os
import time
from datetime import UTC, datetime

from sidechat.baselines import jev_demo
from sidechat.lib import r2
from sidechat.schema import SidechatRequest

CHUNK = 400  # answers per part file
PREFLIGHT = 150  # answers measured before the cost forecast
MAX_FAILED_SHARE = 0.02


class Stopped(Exception):
    """The run stopped on purpose: over the spend cap, refused by Jev, or failing too often."""


def _base(baseline_id: str) -> str:
    return f"{r2.PREFIX}/baselines/{baseline_id}"


def load_parts(s3, baseline_id: str) -> dict[str, dict]:
    done: dict[str, dict] = {}
    for obj in r2.list_keys(s3, f"{_base(baseline_id)}/parts/"):
        for row in r2.get_jsonl(s3, obj["Key"]) or []:
            if row.get("ok"):
                done[row["key"]] = row
    return done


async def _ask(classifier, question_cls, bot: str, state: dict, attempts: int = 5) -> dict:
    from pipecat.classifiers.base_classifier import ClassifierError

    qs = {name: question_cls(**parts) for name, parts in jev_demo.questions(bot).items()}
    last = ""
    for attempt in range(1, attempts + 1):
        started = time.monotonic()
        try:
            out = await classifier.yes_no(state, qs)
            return {
                "ok": True,
                "addressed": round(out["addressed"].probability, 4),
                "question": round(out["question"].probability, 4),
                "ms": round((time.monotonic() - started) * 1000, 1),
                "attempts": attempt,
            }
        except ClassifierError as e:
            last = str(e)
            if any(code in last for code in ("HTTP 401", "HTTP 402", "HTTP 403")):
                raise Stopped(f"Jev refused the key or the account: {last}") from e
            await asyncio.sleep(min(20.0, 1.5 * 2**attempt))
    return {"ok": False, "error": last[:300], "attempts": attempts}


async def score(
    s3,
    baseline_id: str,
    model: str,
    requests: dict[str, SidechatRequest],
    *,
    concurrency: int,
    spend_cap_usd: float,
    usd_per_m_input: float,
    on_progress,
) -> tuple[dict[str, dict], dict]:
    """Answers by request key, and what the run used.

    `requests` maps each key (`jev_demo.key`) to one request that produces it.
    """
    from pipecat.classifiers.base_classifier import YesNoQuestion
    from pipecat.classifiers.typesafe.jev.classifier import JevClassifier
    from pipecat.classifiers.typesafe.jev.client import JevClient

    done = load_parts(s3, baseline_id)
    reused = sum(1 for k in requests if k in done)
    todo = [k for k in requests if k not in done]
    usage = {
        "model": model,
        "requests": len(requests),
        "reused": reused,
        "asked": 0,
        "failed": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "usd_per_m_input": usd_per_m_input,
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    if not todo:
        on_progress(usage, forecast=None)
        return {k: done[k] for k in requests}, usage

    client = JevClient(api_key=os.environ["JEV_API_KEY"], model=model, timeout=20.0, max_retries=6)
    classifier = JevClassifier(client=client)
    await client.connect()
    gate = asyncio.Semaphore(concurrency)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    forecast = None

    async def one(k: str) -> dict:
        req = requests[k]
        async with gate:
            out = await _ask(classifier, YesNoQuestion, req.agent.name, jev_demo.state(req))
        return {"key": k, **out}

    try:
        position, part = 0, 0
        while position < len(todo):
            size = PREFLIGHT if position == 0 else CHUNK
            batch = todo[position : position + size]
            results = await asyncio.gather(*(one(k) for k in batch))
            position += len(batch)
            ok = [x for x in results if x["ok"]]
            for x in ok:
                done[x["key"]] = x
            usage["asked"] += len(batch)
            usage["failed"] += len(batch) - len(ok)
            usage["input_tokens"] = client.usage.input_tokens
            usage["output_tokens"] = client.usage.output_tokens
            r2.put_jsonl(s3, f"{_base(baseline_id)}/parts/{stamp}-{part:05d}.jsonl", results)
            part += 1

            if usage["asked"] and usage["failed"] / usage["asked"] > MAX_FAILED_SHARE and usage["asked"] >= PREFLIGHT:
                raise Stopped(f"{usage['failed']} of {usage['asked']} requests failed; last errors are in the parts")
            if forecast is None and ok:
                per_request = usage["input_tokens"] / max(1, len(ok))
                forecast = {
                    "input_tokens_per_request": round(per_request, 1),
                    "requests_to_ask": len(todo),
                    "input_tokens": round(per_request * len(todo)),
                    "usd": round(per_request * len(todo) * usd_per_m_input / 1e6, 2),
                    "spend_cap_usd": spend_cap_usd,
                }
                if forecast["usd"] > spend_cap_usd:
                    on_progress(usage, forecast=forecast)
                    raise Stopped(f"forecast ${forecast['usd']} is over the cap of ${spend_cap_usd}")
            on_progress(usage, forecast=forecast)
    finally:
        await client.close()

    usage["usd_estimate"] = round(usage["input_tokens"] * usd_per_m_input / 1e6, 3)
    usage["finished_at"] = datetime.now(UTC).isoformat(timespec="seconds")
    return {k: done[k] for k in requests if k in done}, usage
