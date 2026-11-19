"""Real speech through real speech-to-text: AMI's headset audio, transcribed by Deepgram.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.stt_ami::run --exp exp-056-side-stt-ami

Scorecard item 15 asks how much worse a model does on what a speech-to-text service hears than on
the clean transcript. AMI gives both on the same lines: human transcripts with addressee labels
(ACloudCenter/ami-addressee) and each speaker's own headset audio, cut into utterances
(edinburghcstr/ami, `ihm`; both CC BY 4.0). A call gives one audio track per person, as a
headset does.

For the 22 labelled meetings and the AMI silence test's meetings, every headset utterance goes to
Deepgram once, as it is. Each word it returns is given to the dialogue act of the same speaker whose
time span holds the word's midpoint, so the lines keep AMI's own boundaries and labels. AMI's
speaker letters (A to D) are matched to its participant ids by overlap in time.

Writes to R2, under runs/side/stt/ami-deepgram-nova-3/: segments/<meeting>.jsonl (Deepgram's words,
so a rerun skips meetings already heard), transcripts.jsonl (one row per dialogue act: gold and
STT text) and manifest.json; and runs/side/results/<exp>/: status.json, scorecard.json, report.md.
The sets `ami-stt` and `ami-silent-stt:test` (`sidechat/sources/build.py`) read them.
"""

from __future__ import annotations

import os
import pathlib

import modal

from sidechat.lib.r2 import R2_KEYS
from sidechat.lib.stt_align import assign_words, match_speakers, wer
from sidechat.pipeline.train import hf_cache

APP_NAME = "waystone-side-stt-ami"
ROOT = pathlib.Path(__file__).resolve().parents[2]
SECRET_KEYS = (*R2_KEYS, "DEEPGRAM_API_KEY")
AUDIO_REPO = "edinburghcstr/ami"
AUDIO_REVISION = "46f28f2503e2ec48f8867a84eef356c70476beab"
DEEPGRAM_URL = "https://api.deepgram.com/v1/listen"
# Deepgram's general model with punctuation and formatting, as a voice agent would ask for.
DEEPGRAM_PARAMS = {"model": "nova-3", "language": "en", "punctuate": "true", "smart_format": "true"}
USD_PER_MIN = 0.0043  # pre-recorded nova-3, for the forecast and the spend cap

image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install(
        "huggingface-hub==1.33.0",
        "numpy==2.2.6",
        "boto3>=1.40",
        "pydantic>=2.9",
        "pyyaml>=6.0",
        "pyarrow==21.0.0",
        "httpx==0.28.1",
    )
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "HF_HOME": "/cache/hf"})
    .add_local_python_source("sidechat")
)
app = modal.App(APP_NAME)


def _secrets() -> list:
    if not modal.is_local():
        return [modal.Secret.from_dict({})]
    if os.environ.get("MODAL_ENVIRONMENT") != "waystone":
        raise SystemExit("refusing: MODAL_ENVIRONMENT must be 'waystone'. Load .env first: set -a; . ./.env; set +a")
    missing = [k for k in SECRET_KEYS if not os.environ.get(k)]
    if missing:
        raise SystemExit(f"refusing: {', '.join(missing)} not set. Load .env first: set -a; . ./.env; set +a")
    return [modal.Secret.from_dict({k: os.environ[k] for k in SECRET_KEYS})]


@app.function(
    name="stt_run",
    image=image,
    cpu=4.0,
    memory=16384,
    timeout=6 * 3600,
    secrets=_secrets(),
    volumes={"/cache": hf_cache},
)
def run(exp: str, concurrency: int = 16, spend_cap_usd: float = 15.0, limit_meetings: int = 0) -> dict:
    import json
    import time
    import traceback
    from collections import defaultdict
    from concurrent.futures import ThreadPoolExecutor
    from datetime import UTC, datetime

    import httpx
    import pyarrow.parquet as pq
    from huggingface_hub import HfApi, hf_hub_download

    from sidechat.lib import r2
    from sidechat.sources import ami
    from sidechat.sources.build import _fetch

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    base = f"{r2.PREFIX}/{ami.STT_PREFIX}"
    started = time.monotonic()
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {"concurrency": concurrency, "spend_cap_usd": spend_cap_usd, "limit_meetings": limit_meetings},
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    try:
        save()
        # 1. Which meetings: the 22 labelled, and the silence test's.
        local = _fetch(ami.REPO, ami.REVISION, ami.FILES["all"])
        records = [json.loads(x) for x in pathlib.Path(local).read_text().splitlines() if x.strip()]
        records = [r for r in records if r.get("text") and r["text"].strip()]
        labelled_series = {ami.series(r["meeting_id"]) for r in records if r.get("labeled")}
        labelled = sorted({r["meeting_id"] for r in records if r.get("labeled")})
        silent = sorted(
            {
                r["meeting_id"]
                for r in records
                if ami.series(r["meeting_id"]) not in labelled_series
                and ami.silent_split(ami.series(r["meeting_id"])) == "test"
            }
        )
        meetings = labelled + silent
        if limit_meetings:
            meetings = meetings[:limit_meetings]
        wanted = set(meetings)
        das_by_meeting: dict[str, list[dict]] = defaultdict(list)
        for r in records:
            if r["meeting_id"] in wanted:
                das_by_meeting[r["meeting_id"]].append(r)
        save(
            stage="reading audio",
            meetings={"labelled": len(labelled), "silence test": len(silent), "used": len(meetings)},
        )

        # 2. Their headset utterances, shard by shard (only these meetings are kept).
        done = {k["Key"].rsplit("/", 1)[-1][: -len(".jsonl")] for k in r2.list_keys(s3, f"{base}/segments/")}
        todo = wanted - done
        segments: dict[str, list[dict]] = defaultdict(list)
        if todo:
            files = sorted(
                f
                for f in HfApi().list_repo_files(AUDIO_REPO, repo_type="dataset", revision=AUDIO_REVISION)
                if f.startswith("ihm/") and f.endswith(".parquet")
            )
            for n, f in enumerate(files, 1):
                path = hf_hub_download(
                    AUDIO_REPO, f, repo_type="dataset", revision=AUDIO_REVISION, local_dir="/tmp/ami"
                )
                table = pq.read_table(
                    path,
                    columns=["meeting_id", "speaker_id", "begin_time", "end_time", "audio"],
                    filters=[("meeting_id", "in", sorted(todo))],
                )
                for row in table.to_pylist():
                    segments[row["meeting_id"]].append(
                        {
                            "speaker_id": row["speaker_id"],
                            "begin": float(row["begin_time"]),
                            "end": float(row["end_time"]),
                            "audio": row["audio"]["bytes"],
                        }
                    )
                pathlib.Path(path).unlink(missing_ok=True)
                save(stage=f"reading audio: shard {n} of {len(files)}", segments=sum(len(v) for v in segments.values()))
        missing = sorted(m for m in todo if not segments.get(m))

        # 3. Deepgram, once per utterance, meeting by meeting (each meeting saved as it finishes).
        key = os.environ["DEEPGRAM_API_KEY"]
        client = httpx.Client(timeout=60.0, headers={"Authorization": f"Token {key}"})
        spent_min = 0.0

        def kind(audio: bytes) -> str:
            return "audio/wav" if audio[:4] == b"RIFF" else "audio/flac" if audio[:4] == b"fLaC" else "audio/*"

        def hear(seg: dict) -> dict:
            out = {"speaker_id": seg["speaker_id"], "begin": seg["begin"], "end": seg["end"], "words": [], "ok": False}
            last = ""
            for attempt in range(5):
                try:
                    resp = client.post(
                        DEEPGRAM_URL,
                        params=DEEPGRAM_PARAMS,
                        content=seg["audio"],
                        headers={"Content-Type": kind(seg["audio"])},
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
                    return {**out, "error": f"HTTP {resp.status_code}: {resp.text[:200]}"}
                alt = resp.json()["results"]["channels"][0]["alternatives"][0]
                out["words"] = [
                    [
                        round(seg["begin"] + w["start"], 3),
                        round(seg["begin"] + w["end"], 3),
                        w.get("punctuated_word") or w["word"],
                    ]
                    for w in alt.get("words", [])
                ]
                out["ok"] = True
                return out
            return {**out, "error": last}

        failed = 0
        with ThreadPoolExecutor(concurrency) as pool:
            for n, m in enumerate(sorted(segments), 1):
                minutes = sum(s["end"] - s["begin"] for s in segments[m]) / 60
                if (spent_min + minutes) * USD_PER_MIN > spend_cap_usd:
                    save(
                        state="stopped",
                        reason=f"spend cap: {spent_min:.0f} min heard, the next meeting would pass ${spend_cap_usd}",
                    )
                    return {"state": "stopped"}
                heard = list(pool.map(hear, segments[m]))
                failed += sum(not h["ok"] for h in heard)
                spent_min += minutes
                r2.put_jsonl(s3, f"{base}/segments/{m}.jsonl", heard)
                save(stage=f"transcribing: meeting {n} of {len(segments)}", minutes=round(spent_min, 1), failed=failed)
                segments[m] = []  # free the audio

        # 4. Words to dialogue acts, for every meeting heard (this run or an earlier one).
        save(stage="assigning words")
        rows, letters_all, edits, ref_words, empty = [], {}, 0, 0, 0
        for m in meetings:
            heard = r2.get_jsonl(s3, f"{base}/segments/{m}.jsonl") or []
            if not heard:
                continue
            das = sorted(das_by_meeting[m], key=lambda r: (r["start_time"], r["end_time"]))
            letters = match_speakers(das, heard)
            letters_all[m] = letters
            words_by_id: dict[str, list] = defaultdict(list)
            for h in heard:
                words_by_id[h["speaker_id"]].extend(tuple(w) for w in h["words"])
            stt = assign_words(das, words_by_id, letters)
            for d in das:
                e, n_ref = wer(d["text"], stt[d["da_id"]])
                edits, ref_words = edits + e, ref_words + n_ref
                empty += not stt[d["da_id"]]
                rows.append(
                    {
                        "da_id": d["da_id"],
                        "meeting": m,
                        "speaker": d["speaker"],
                        "start": d["start_time"],
                        "end": d["end_time"],
                        "labelled_meeting": m in labelled,
                        "gold": d["text"],
                        "stt": stt[d["da_id"]],
                    }
                )
        r2.put_jsonl(s3, f"{base}/transcripts.jsonl", rows)
        manifest = {
            "stt": {"service": "Deepgram", "url": DEEPGRAM_URL, "params": DEEPGRAM_PARAMS},
            "audio": {"repo": AUDIO_REPO, "revision": AUDIO_REVISION, "config": "ihm", "licence": "CC BY 4.0"},
            "labels": {"repo": ami.REPO, "revision": ami.REVISION},
            "meetings": {
                "labelled": [m for m in labelled if m in letters_all],
                "silence_test": [m for m in silent if m in letters_all],
            },
            "no_audio": missing,
            "speaker_match": letters_all,
            "dialogue_acts": len(rows),
            "empty_transcripts": empty,
            "word_error_rate": round(edits / max(1, ref_words), 4),
            "minutes_heard_this_run": round(spent_min, 1),
            "failed_requests_this_run": failed,
            "built_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        r2.put_json(s3, f"{base}/manifest.json", manifest)
        card = {"exp": exp, **manifest, "cost_usd_estimate": round(spent_min * USD_PER_MIN, 2)}
        r2.put_json(s3, f"{out}/scorecard.json", card)
        r2.put_text(
            s3,
            f"{out}/report.md",
            "\n".join(
                [
                    f"# {exp}: AMI through Deepgram",
                    "",
                    f"{len(rows):,} dialogue acts in {len(letters_all)} meetings; {empty:,} came back empty.",
                    f"Word error rate against AMI's transcripts: {100 * manifest['word_error_rate']:.1f}%.",
                    f"{spent_min:.0f} minutes of audio heard this run (about ${spent_min * USD_PER_MIN:.2f}); {failed} requests failed.",
                    f"Meetings with no audio in `{AUDIO_REPO}`: {', '.join(missing) or 'none'}.",
                    "",
                ]
            ),
        )
        save(state="done", stage="done", dialogue_acts=len(rows), empty=empty, wer=manifest["word_error_rate"])
        return {"state": "done", **{k: manifest[k] for k in ("dialogue_acts", "empty_transcripts", "word_error_rate")}}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
