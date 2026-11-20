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

`--split dev` hears instead the train and devel utterances that say the agent's name, every
recording of each (close-talk and far-field): a dev set for the name as heard, so that work on it
never looks at the test split. Its transcripts go under the `slurp-names-dev` prefixes.
"""

from __future__ import annotations

import modal

from sidechat.pipeline.stt_ami import DEEPGRAM_PARAMS, DEEPGRAM_URL, USD_PER_MIN, _secrets, image

APP_NAME = "waystone-side-stt-slurp"
TEXT_URL = "https://raw.githubusercontent.com/pswietojanski/slurp/{commit}/dataset/slurp/{split}.jsonl"
TEXT_COMMIT = "8eb16545762be97ace75334109d73824217311f1"
AUDIO_URL = "https://zenodo.org/api/records/4274930/files/slurp_real.tar.gz/content"
app = modal.App(APP_NAME)


@app.function(name="slurp_run", image=image, cpu=4.0, memory=8192, timeout=4 * 3600, secrets=_secrets())
def run(exp: str, concurrency: int = 16, spend_cap_usd: float = 5.0, keyterm: str = "", split: str = "test") -> dict:
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
    if split not in ("test", "dev"):
        raise ValueError(f"split must be test or dev, not {split!r}")
    if split == "dev":
        base = f"{r2.PREFIX}/{slurp.DEV_STT_KEYTERM_PREFIX if keyterm else slurp.DEV_STT_PREFIX}"
    else:
        base = f"{r2.PREFIX}/{slurp.STT_KEYTERM_PREFIX if keyterm else slurp.STT_PREFIX}"
    params = {**DEEPGRAM_PARAMS, **({"keyterm": keyterm} if keyterm else {})}
    started = time.monotonic()
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {"concurrency": concurrency, "spend_cap_usd": spend_cap_usd, "keyterm": keyterm, "split": split},
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    try:
        save(stage=f"reading SLURP's {split} text")
        files = ("test",) if split == "test" else ("train", "devel")
        utts = []
        for f in files:
            text = httpx.get(TEXT_URL.format(commit=TEXT_COMMIT, split=f), timeout=60, follow_redirects=True).text
            utts += [json.loads(x) for x in text.splitlines() if x.strip()]
        chosen = {}
        for u in utts:
            if split == "test":
                rec = next((r["file"] for r in u["recordings"] if "headset" in r["file"]), None)
                if rec:
                    chosen[rec] = u
            elif slurp.named(u["sentence"]):
                for r in u["recordings"]:
                    chosen[r["file"]] = u
        save(stage="downloading the audio", utterances=len(utts), with_headset=len(chosen))

        # The archive once, keeping only the chosen recordings. Zenodo can close a long download
        # part way (exp-062), so it resumes from where it stopped.
        # The chosen recordings are kept in R2 (private, never git or the Hub, SD-23) after the
        # first download, so another pass over the same split does not download the archive again.
        cache = f"{r2.PREFIX}/stt/slurp-audio-cache/{split}"
        cached = {o["Key"].rsplit("/", 1)[-1] for o in r2.list_keys(s3, f"{cache}/")}
        path = pathlib.Path("/tmp/slurp_real.tar.gz")
        path.unlink(missing_ok=True)
        total = None
        for attempt in range(10 if not set(chosen) <= cached else 0):
            have = path.stat().st_size if path.exists() else 0
            if total is not None and have >= total:
                break
            try:
                headers = {"Range": f"bytes={have}-"} if have else {}
                with httpx.stream("GET", AUDIO_URL, timeout=600, follow_redirects=True, headers=headers) as resp:
                    resp.raise_for_status()
                    if have and resp.status_code != 206:  # the range was ignored: start again
                        have = 0
                    if resp.status_code == 206:
                        total = int(resp.headers["content-range"].rsplit("/", 1)[-1])
                    elif "content-length" in resp.headers:
                        total = int(resp.headers["content-length"])
                    with path.open("ab" if have else "wb") as f:
                        for chunk in resp.iter_bytes(1 << 20):
                            f.write(chunk)
                if total is None or path.stat().st_size >= total:
                    break
            except httpx.HTTPError as e:
                save(stage=f"downloading the audio (retry {attempt + 1}: {type(e).__name__})")
                time.sleep(min(60, 5 * 2**attempt))
        if total is not None and path.stat().st_size < total:
            raise RuntimeError(f"downloaded {path.stat().st_size:,} of {total:,} bytes")
        audio: dict[str, bytes] = {}
        if set(chosen) <= cached:
            save(stage="reading the cached audio")
            with ThreadPoolExecutor(concurrency) as pool:
                got = pool.map(lambda n: (n, r2.get_bytes(s3, f"{cache}/{n}")), sorted(chosen))
                audio = dict(got)
        else:
            with tarfile.open(path, "r:gz") as tar:
                for m in tar:
                    name = m.name.rsplit("/", 1)[-1]
                    if m.isfile() and name in chosen:
                        audio[name] = tar.extractfile(m).read()
            path.unlink(missing_ok=True)
            save(stage="caching the chosen audio")
            with ThreadPoolExecutor(concurrency) as pool:
                list(pool.map(lambda kv: r2.put_bytes(s3, f"{cache}/{kv[0]}", kv[1]), audio.items()))
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
                    # dev hears every recording of an utterance, so its rows carry the recording too
                    "slurp_id": str(u["slurp_id"]) if split == "test" else f"{u['slurp_id']}.{name.rsplit('.', 1)[0]}",
                    "device": "headset" if "headset" in name else "far-field",
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
            "text": {"urls": [TEXT_URL.format(commit=TEXT_COMMIT, split=f) for f in files], "licence": "CC BY 4.0"},
            "split": split,
            "audio": {
                "url": AUDIO_URL,
                "licence": "CC BY-NC 4.0",
                "use": "test only (SD-23)" if split == "test" else "dev and test only, never training (SD-23)",
            },
            "utterances": len(utts),
            "recordings": len(chosen),
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
