"""The three committee members and how each is asked.

Which model fills each role is configuration, not code: `LABELLER_A_MODEL`, `LABELLER_B_MODEL` and
`LABELLER_C_MODEL` in `.env`. No labeller model is named in this repository (SD-09). Each member is a different model family, reached through its provider's own API:

    a  a Responses-style API      OPENAI_API_KEY      raw HTTP
    b  a Messages-style API       ANTHROPIC_API_KEY   the provider's Python SDK
    c  a generateContent API      GOOGLE_API_KEY      raw HTTP

All three run at low reasoning effort and answer in the JSON schema in `prompt.py`. Prices for the
spend cap come from `LABELLER_PRICES`, e.g. `a:2/10,b:4/20,c:2/10` (dollars per million input and
output tokens).
"""

from __future__ import annotations

import asyncio
import os
import random
import time
from dataclasses import dataclass, field

from sidechat.committee.prompt import SCHEMA, parse_answer

MEMBERS = ("a", "b", "c")
KEY_ENV = {"a": "OPENAI_API_KEY", "b": "ANTHROPIC_API_KEY", "c": "GOOGLE_API_KEY"}
MODEL_ENV = {m: f"LABELLER_{m.upper()}_MODEL" for m in MEMBERS}
EFFORT = "low"
MAX_OUTPUT_TOKENS = 8000
ATTEMPTS = 6
# Share of the input price a cached input token costs, for the spend estimate only.
CACHED_FACTOR = {"a": 0.25, "b": 0.1, "c": 0.25}
CACHE_WRITE_FACTOR = {"a": 1.0, "b": 1.25, "c": 1.0}


class MemberRefused(Exception):
    """A permanent error: wrong key, unknown model, a request the API will never accept."""


@dataclass
class Reply:
    ok: bool
    answer: dict | None = None
    error: str | None = None
    usage: dict = field(default_factory=dict)  # input, cached, cache_write, output
    served_by_configured_model: bool = True
    ms: float = 0.0
    attempts: int = 1


def model(member: str) -> str:
    value = os.environ.get(MODEL_ENV[member], "").strip()
    if not value:
        raise MemberRefused(f"{MODEL_ENV[member]} is not set")
    return value


def prices() -> dict[str, tuple[float, float]]:
    out = {}
    for part in os.environ.get("LABELLER_PRICES", "").split(","):
        if ":" in part:
            m, _, pair = part.partition(":")
            i, _, o = pair.partition("/")
            out[m.strip()] = (float(i), float(o))
    return out


def cost_usd(member: str, usage: dict, price: tuple[float, float] | None) -> float:
    if not price:
        return 0.0
    pin, pout = price
    plain = max(0, usage.get("input", 0) - usage.get("cached", 0) - usage.get("cache_write", 0))
    total = (
        plain * pin
        + usage.get("cached", 0) * pin * CACHED_FACTOR[member]
        + usage.get("cache_write", 0) * pin * CACHE_WRITE_FACTOR[member]
        + usage.get("output", 0) * pout
    )
    return total / 1e6


def _gemini_schema(schema: dict) -> dict:
    """The same schema without `additionalProperties`, which the generateContent API may refuse."""
    return {k: v for k, v in schema.items() if k != "additionalProperties"}


async def _post_json(http, url: str, headers: dict, body: dict) -> tuple[int, dict | str]:
    r = await http.post(url, headers=headers, json=body, timeout=180.0)
    try:
        return r.status_code, r.json()
    except ValueError:
        return r.status_code, r.text[:500]


async def _with_retries(call) -> Reply:
    """Retry rate limits, overloads, timeouts and server errors. Anything else is final."""
    last = "no attempt"
    for attempt in range(1, ATTEMPTS + 1):
        started = time.monotonic()
        try:
            reply = await call()
            reply.ms, reply.attempts = round((time.monotonic() - started) * 1000, 1), attempt
            return reply
        except MemberRefused:
            raise
        except Exception as e:  # noqa: BLE001 - transient by elimination; retried, then recorded
            last = f"{type(e).__name__}: {str(e)[:300]}"
        await asyncio.sleep(min(60.0, 2.0 * 2 ** (attempt - 1)) + random.uniform(0, 1.5))
    return Reply(ok=False, error=f"gave up after {ATTEMPTS} attempts: {last}", attempts=ATTEMPTS)


class _Transient(Exception):
    """Retried by `_with_retries`."""


class _BadRequest(Exception):
    """Recorded as a failed answer for this line; not retried."""


def _check_status(status: int, data) -> None:
    if status == 200:
        return
    text = str(data)[:400]
    if status in (408, 409, 429, 500, 502, 503, 504, 529):
        raise _Transient(f"HTTP {status}: {text}")
    if status in (401, 403, 404):
        raise MemberRefused(f"HTTP {status}: {text}")
    raise _BadRequest(f"HTTP {status}: {text}")


# --- member a: a Responses-style API -------------------------------------------------------


async def ask_a(http, system: str, user: str) -> Reply:
    body = {
        "model": model("a"),
        "input": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "text": {"format": {"type": "json_schema", "name": "sidechat_label", "schema": SCHEMA, "strict": True}},
        "reasoning": {"effort": EFFORT},
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "store": False,
    }
    headers = {"Authorization": f"Bearer {os.environ[KEY_ENV['a']]}"}

    async def call() -> Reply:
        status, data = await _post_json(http, "https://api.openai.com/v1/responses", headers, body)
        try:
            _check_status(status, data)
        except _BadRequest as e:
            return Reply(ok=False, error=str(e))
        u = data.get("usage") or {}
        usage = {
            "input": u.get("input_tokens", 0),
            "cached": (u.get("input_tokens_details") or {}).get("cached_tokens", 0),
            "output": u.get("output_tokens", 0),
        }
        if data.get("status") == "incomplete":
            return Reply(ok=False, error=f"incomplete: {data.get('incomplete_details')}", usage=usage)
        text = "".join(
            c.get("text", "")
            for item in data.get("output", [])
            if item.get("type") == "message"
            for c in item.get("content", [])
            if c.get("type") == "output_text"
        )
        refusal = next(
            (
                c.get("refusal")
                for item in data.get("output", [])
                for c in item.get("content", []) or []
                if c.get("type") == "refusal"
            ),
            None,
        )
        if refusal:
            return Reply(ok=False, error=f"refusal: {str(refusal)[:200]}", usage=usage)
        try:
            return Reply(ok=True, answer=parse_answer(text), usage=usage)
        except ValueError as e:
            return Reply(ok=False, error=f"invalid answer: {e}", usage=usage)

    return await _with_retries(call)


# --- member b: a Messages-style API, through the provider's SDK ----------------------------


async def ask_b(client, system: str, user: str) -> Reply:
    configured = model("b")

    async def call() -> Reply:
        import anthropic

        try:
            resp = await client.beta.messages.create(
                model=configured,
                max_tokens=MAX_OUTPUT_TOKENS,
                system=[{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": user}],
                output_config={"effort": EFFORT, "format": {"type": "json_schema", "schema": SCHEMA}},
                betas=["server-side-fallback-2026-07-01"],
                fallbacks="default",
            )
        except (anthropic.AuthenticationError, anthropic.PermissionDeniedError, anthropic.NotFoundError) as e:
            raise MemberRefused(f"{type(e).__name__}: {str(e)[:300]}") from e
        except anthropic.BadRequestError as e:
            return Reply(ok=False, error=f"HTTP 400: {str(e)[:300]}")
        except (anthropic.RateLimitError, anthropic.InternalServerError, anthropic.APIConnectionError) as e:
            raise _Transient(str(e)[:300]) from e
        u = resp.usage
        usage = {
            "input": (u.input_tokens or 0) + (u.cache_read_input_tokens or 0) + (u.cache_creation_input_tokens or 0),
            "cached": u.cache_read_input_tokens or 0,
            "cache_write": u.cache_creation_input_tokens or 0,
            "output": u.output_tokens or 0,
        }
        same_model = resp.model == configured
        if resp.stop_reason == "refusal":
            return Reply(ok=False, error="refusal", usage=usage, served_by_configured_model=same_model)
        if resp.stop_reason == "max_tokens":
            return Reply(ok=False, error="max_tokens", usage=usage, served_by_configured_model=same_model)
        text = next((b.text for b in resp.content if b.type == "text"), "")
        try:
            return Reply(ok=True, answer=parse_answer(text), usage=usage, served_by_configured_model=same_model)
        except ValueError as e:
            return Reply(ok=False, error=f"invalid answer: {e}", usage=usage, served_by_configured_model=same_model)

    return await _with_retries(call)


# --- member c: a generateContent API -------------------------------------------------------


async def ask_c(http, system: str, user: str) -> Reply:
    name = model("c")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{name}:generateContent"
    body = {
        "systemInstruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseJsonSchema": _gemini_schema(SCHEMA),
            "thinkingConfig": {"thinkingLevel": EFFORT},
            "maxOutputTokens": MAX_OUTPUT_TOKENS,
        },
    }
    headers = {"x-goog-api-key": os.environ[KEY_ENV["c"]]}

    async def call() -> Reply:
        status, data = await _post_json(http, url, headers, body)
        try:
            _check_status(status, data)
        except _BadRequest as e:
            return Reply(ok=False, error=str(e))
        u = data.get("usageMetadata") or {}
        usage = {
            "input": u.get("promptTokenCount", 0),
            "cached": u.get("cachedContentTokenCount", 0),
            "output": u.get("candidatesTokenCount", 0) + u.get("thoughtsTokenCount", 0),
        }
        candidates = data.get("candidates") or []
        if not candidates:
            return Reply(ok=False, error=f"no candidates: {str(data.get('promptFeedback'))[:200]}", usage=usage)
        cand = candidates[0]
        text = "".join(p.get("text", "") for p in (cand.get("content") or {}).get("parts", []) if not p.get("thought"))
        if cand.get("finishReason") not in (None, "STOP"):
            return Reply(ok=False, error=f"finish reason {cand.get('finishReason')}", usage=usage)
        try:
            return Reply(ok=True, answer=parse_answer(text), usage=usage)
        except ValueError as e:
            return Reply(ok=False, error=f"invalid answer: {e}", usage=usage)

    return await _with_retries(call)
