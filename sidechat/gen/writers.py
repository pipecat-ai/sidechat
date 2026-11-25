"""The writer models: each turns a prompt into a conversation's lines.

Which model each writer is lives in `.env` only (SD-09): `WRITER_A_MODEL` (a Responses-style API),
`WRITER_B_MODEL` (a Messages-style API, through the provider's SDK), `WRITER_C_MODEL` (a
generateContent API) and `WRITER_O_MODEL` (open weights, `repo@revision`, served with vLLM on
Modal). Writer b writes test conversations only, so the test set has wording no training writer
produced. Prices for the spend cap: `WRITER_PRICES`, e.g. `a:1/5,b:4/20,c:1.5/7.5`.
"""

from __future__ import annotations

import asyncio
import os
import random

from sidechat.gen.writer import OUTPUT_SCHEMA, SYSTEM, parse_lines

API_WRITERS = ("a", "b", "c")
HELDOUT_WRITER = "b"
KEY_ENV = {"a": "OPENAI_API_KEY", "b": "ANTHROPIC_API_KEY", "c": "GOOGLE_API_KEY"}
MAX_OUTPUT = 8000


def model(writer: str) -> str:
    value = os.environ.get(f"WRITER_{writer.upper()}_MODEL", "").strip()
    if not value:
        raise RuntimeError(f"WRITER_{writer.upper()}_MODEL is not set")
    return value


def prices() -> dict[str, tuple[float, float]]:
    out = {}
    for part in os.environ.get("WRITER_PRICES", "").split(","):
        if ":" in part:
            w, _, pair = part.partition(":")
            i, _, o = pair.partition("/")
            out[w.strip()] = (float(i), float(o))
    return out


def cost(writer: str, usage: dict) -> float:
    pin, pout = prices().get(writer, (0.0, 0.0))
    return (usage.get("input", 0) * pin + usage.get("output", 0) * pout) / 1e6


async def _a(http, prompt: str) -> tuple[str, dict]:
    body = {
        "model": model("a"),
        "input": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
        "text": {"format": {"type": "json_schema", "name": "conversation", "schema": OUTPUT_SCHEMA, "strict": True}},
        "reasoning": {"effort": "low"},
        "max_output_tokens": MAX_OUTPUT,
        "store": False,
    }
    r = await http.post(
        "https://api.openai.com/v1/responses",
        json=body,
        timeout=240.0,
        headers={"Authorization": f"Bearer {os.environ[KEY_ENV['a']]}"},
    )
    data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {str(data or r.text)[:300]}")
    u = data.get("usage") or {}
    text = "".join(
        c.get("text", "")
        for item in data.get("output", [])
        if item.get("type") == "message"
        for c in item.get("content", [])
        if c.get("type") == "output_text"
    )
    return text, {"input": u.get("input_tokens", 0), "output": u.get("output_tokens", 0)}


async def _b(client, prompt: str) -> tuple[str, dict]:
    resp = await client.beta.messages.create(
        model=model("b"),
        max_tokens=MAX_OUTPUT,
        system=[{"type": "text", "text": SYSTEM, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": prompt}],
        output_config={"effort": "low", "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
    )
    if resp.stop_reason in ("refusal", "max_tokens"):
        raise RuntimeError(f"stop reason {resp.stop_reason}")
    u = resp.usage
    text = next((b.text for b in resp.content if b.type == "text"), "")
    inp = (u.input_tokens or 0) + (u.cache_read_input_tokens or 0) + (u.cache_creation_input_tokens or 0)
    return text, {"input": inp, "output": u.output_tokens or 0}


async def _c(http, prompt: str) -> tuple[str, dict]:
    import copy

    schema = copy.deepcopy(OUTPUT_SCHEMA)  # a copy: the strict schema writer a sends must keep its fields
    schema.pop("additionalProperties", None)
    schema["properties"]["lines"]["items"].pop("additionalProperties", None)
    body = {
        "systemInstruction": {"parts": [{"text": SYSTEM}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseJsonSchema": schema,
            "thinkingConfig": {"thinkingLevel": "low"},
            "maxOutputTokens": MAX_OUTPUT,
        },
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model('c')}:generateContent"
    r = await http.post(url, json=body, timeout=240.0, headers={"x-goog-api-key": os.environ[KEY_ENV["c"]]})
    data = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code}: {str(data or r.text)[:300]}")
    u = data.get("usageMetadata") or {}
    cand = (data.get("candidates") or [{}])[0]
    text = "".join(p.get("text", "") for p in (cand.get("content") or {}).get("parts", []) if not p.get("thought"))
    return text, {
        "input": u.get("promptTokenCount", 0),
        "output": u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0),
    }


async def write_api(writer: str, items: list[dict], concurrency: int, on_done) -> None:
    """Write each item ({conv_id, prompt, n}) and call `on_done(record)` as each finishes."""
    import anthropic
    import httpx

    gate = asyncio.Semaphore(concurrency)
    async with httpx.AsyncClient(limits=httpx.Limits(max_connections=concurrency * 2)) as http:
        claude = anthropic.AsyncAnthropic(max_retries=4, timeout=240.0) if writer == "b" else None
        call = {"a": lambda p: _a(http, p), "b": lambda p: _b(claude, p), "c": lambda p: _c(http, p)}[writer]

        async def one(item: dict) -> None:
            usage_total = {"input": 0, "output": 0}
            last = ""
            async with gate:
                for attempt in range(1, 6):
                    try:
                        text, usage = await call(item["prompt"])
                        for k in usage_total:
                            usage_total[k] += usage.get(k, 0)
                        lines = parse_lines(text, item["n"])
                        await on_done(
                            {
                                "conv_id": item["conv_id"],
                                "writer": writer,
                                "ok": True,
                                "lines": lines,
                                "usage": usage_total,
                                "attempts": attempt,
                            }
                        )
                        return
                    except Exception as e:  # noqa: BLE001 - retried, then recorded
                        last = f"{type(e).__name__}: {str(e)[:300]}"
                        transient = any(
                            c in last
                            for c in ("429", "500", "502", "503", "504", "529", "Timeout", "timeout", "Connect")
                        )
                        await asyncio.sleep((2.0 * 2**attempt if transient else 1.0) + random.uniform(0, 1))
            await on_done(
                {"conv_id": item["conv_id"], "writer": writer, "ok": False, "error": last, "usage": usage_total}
            )

        try:
            await asyncio.gather(*(one(i) for i in items))
        finally:
            if claude is not None:
                await claude.close()
