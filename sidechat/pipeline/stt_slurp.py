"""Real requests to an assistant, through real speech-to-text: SLURP's recordings, heard by Deepgram.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.phase6::run --exp exp-057-side-phase6-slurp --test slurp

SLURP (Bastianelli et al., 2020) is people speaking requests to a home assistant, "Olly", most of
them without its name. Its text is CC BY 4.0 and its audio CC BY-NC 4.0: test only, never trained
on, and nothing from it goes into git or onto the Hub (SD-23). The test split's utterances with a
close-talk headset recording (a call's microphone, not a far-field one) are heard once each, with
the same Deepgram settings as AMI (`sidechat/pipeline/stt_ami.py`).

Writes to R2, under runs/side/stt/slurp-deepgram-nova-3/: transcripts.jsonl (one row per utterance:
its id, recording, text, scenario, intent and what was heard) and manifest.json; and
runs/side/results/<exp>/: status.json, scorecard.json, report.md. The sets `slurp` and `slurp-stt`
(`sidechat/sources/slurp.py`) splice these into AMI's silence-test meetings.
"""

from __future__ import annotations

import modal

from sidechat.pipeline.stt_ami import DEEPGRAM_PARAMS, DEEPGRAM_URL, USD_PER_MIN, _secrets, image

APP_NAME = "waystone-side-stt-slurp"
TEXT_URL = "https://raw.githubusercontent.com/pswietojanski/slurp/{commit}/dataset/slurp/test.jsonl"
TEXT_COMMIT = "8eb16545762be97ace75334109d73824217311f1"
AUDIO_URL = "https://zenodo.org/api/records/4274930/files/slurp_real.tar.gz/content"
app = modal.App(APP_NAME)


@app.function(name="slurp_run", image=image, cpu=4.0, memory=8192, timeout=4 * 3600, secrets=_secrets())
def run(exp: str, concurrency: int = 16, spend_cap_usd: float = 5.0, keyterm: str = "") -> dict:
    """`keyterm` names a word for Deepgram to listen for (its keyterm prompting, e.g. the agent's
    name); the transcripts then go under the `-keyterm` prefix and leave the plain ones as they are."""
    import json
    import os
    import pathlib
    import tarfile
    import time
    import traceback
    from concurrent.futures import ThreadPoolExecutor
    from datetime import UTC, datetime

    import httpx

    from sidechat.lib import r2
    from sidechat.lib.stt_align import wer
    from sidechat.sources import slurp

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    base = f"{r2.PREFIX}/{slurp.STT_KEYTERM_PREFIX if keyterm else slurp.STT_PREFIX}"
    params = {**DEEPGRAM_PARAMS, **({"keyterm": keyterm} if keyterm else {})}
    started = time.monotonic()
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {"concurrency": concurrency, "spend_cap_usd": spend_cap_usd, "keyterm": keyterm},
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    try:
        save(stage="reading SLURP's test text")
        text = httpx.get(TEXT_URL.format(commit=TEXT_COMMIT), timeout=60, follow_redirects=True).text
        utts = [json.loads(x) for x in text.splitlines() if x.strip()]
        chosen = {}
        for u in utts:
            rec = next((r["file"] for r in u["recordings"] if "headset" in r["file"]), None)
            if rec:
                chosen[rec] = u
        save(stage="downloading the audio", utterances=len(utts), with_headset=len(chosen))

        # The archive once, keeping only the chosen recordings.
        path = pathlib.Path("/tmp/slurp_real.tar.gz")
        with httpx.stream("GET", AUDIO_URL, timeout=600, follow_redirects=True) as resp:
            resp.raise_for_status()
            with path.open("wb") as f:
                for chunk in resp.iter_bytes(1 << 20):
                    f.write(chunk)
        audio: dict[str, bytes] = {}
        with tarfile.open(path, "r:gz") as tar:
            for m in tar:
                name = m.name.rsplit("/", 1)[-1]
                if m.isfile() and name in chosen:
                    audio[name] = tar.extractfile(m).read()
        path.unlink(missing_ok=True)
        save(stage="hearing", found=len(audio))

        key = os.environ["DEEPGRAM_API_KEY"]
        client = httpx.Client(timeout=60.0, headers={"Authorization": f"Token {key}"})

        # A flac's length, for the spend cap: total samples over the sample rate in its STREAMINFO.
        def seconds(b: bytes) -> float:
            if b[:4] != b"fLaC":
                return 3.0
            info = b[8:26]
            rate = (info[10] << 12) | (info[11] << 4) | (info[12] >> 4)
            total = ((info[13] & 0x0F) << 32) | (info[14] << 24) | (info[15] << 16) | (info[16] << 8) | info[17]
            return total / rate if rate else 3.0

        minutes = sum(seconds(b) for b in audio.values()) / 60
        if minutes * USD_PER_MIN > spend_cap_usd:
            save(state="stopped", reason=f"{minutes:.0f} minutes would pass ${spend_cap_usd}")
            return {"state": "stopped"}

        def hear(name: str) -> tuple[str, str, bool]:
            last = ""
            for attempt in range(5):
                try:
                    resp = client.post(
                        DEEPGRAM_URL,
                        params=params,
                        content=audio[name],
                        headers={"Content-Type": "audio/flac"},
                    )
                except httpx.HTTPError as e:
                    last = f"{type(e).__name__}: {e}"
                    time.sleep(2**attempt)
                    continue
                if resp.status_code == 429 or resp.status_code >= 500:
                    last = f"HTTP {resp.status_code}"
                    time.sleep(2**attempt)
                    continue
                if resp.status_code != 200:
                    return name, f"HTTP {resp.status_code}", False
                return name, resp.json()["results"]["channels"][0]["alternatives"][0]["transcript"], True
            return name, last, False

        with ThreadPoolExecutor(concurrency) as pool:
            heard = {n: (t, ok) for n, t, ok in pool.map(hear, sorted(audio))}
        rows, edits, ref_words, failed = [], 0, 0, 0
        for name, u in sorted(chosen.items(), key=lambda kv: kv[1]["slurp_id"]):
            if name not in heard:
                continue
            t, ok = heard[name]
            failed += not ok
            stt = t if ok else ""
            e, n = wer(u["sentence"], stt)
            edits, ref_words = edits + e, ref_words + n
            rows.append(
                {
                    "slurp_id": str(u["slurp_id"]),
                    "file": name,
                    "sentence": u["sentence"],
                    "scenario": u["scenario"],
                    "intent": u["intent"],
                    "stt": stt,
                }
            )
        r2.put_jsonl(s3, f"{base}/transcripts.jsonl", rows)
        manifest = {
            "stt": {"service": "Deepgram", "url": DEEPGRAM_URL, "params": params},
            "text": {"url": TEXT_URL.format(commit=TEXT_COMMIT), "licence": "CC BY 4.0"},
            "audio": {"url": AUDIO_URL, "licence": "CC BY-NC 4.0", "use": "test only (SD-23)"},
            "utterances": len(utts),
            "with_headset": len(chosen),
            "heard": len(rows),
            "failed": failed,
            "empty": sum(not r["stt"] for r in rows),
            "named": sum("olly" in r["sentence"].split() for r in rows),
            "word_error_rate": round(edits / max(1, ref_words), 4),
            "minutes": round(minutes, 1),
            "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        r2.put_json(s3, f"{base}/manifest.json", manifest)
        r2.put_json(
            s3, f"{out}/scorecard.json", {"exp": exp, **manifest, "cost_usd_estimate": round(minutes * USD_PER_MIN, 2)}
        )
        r2.put_text(
            s3,
            f"{out}/report.md",
            f"# {exp}: SLURP through Deepgram\n\n{len(rows):,} requests heard ({manifest['named']} with the name), "
            f"{manifest['empty']} empty, {failed} failed. Word error rate against SLURP's text: "
            f"{100 * manifest['word_error_rate']:.1f}%. {minutes:.0f} minutes (about ${minutes * USD_PER_MIN:.2f}).\n",
        )
        save(state="done", stage="done", heard=len(rows), wer=manifest["word_error_rate"])
        return {"state": "done", "heard": len(rows)}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
