"""Lining up a speech-to-text service's words with a corpus's own utterances (no Modal, no audio).

Used by `sidechat/pipeline/stt_ami.py`: AMI's dialogue acts keep their boundaries and labels, and
each word Deepgram heard on a speaker's headset goes to the act of that speaker that holds its
midpoint.
"""

from __future__ import annotations


def match_speakers(das: list[dict], segments: list[dict]) -> dict[str, str]:
    """AMI letter -> participant id, by the seconds each letter's acts overlap each id's segments."""
    from collections import defaultdict

    overlap: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    by_id: dict[str, list[tuple[float, float]]] = defaultdict(list)
    for s in segments:
        by_id[s["speaker_id"]].append((s["begin"], s["end"]))
    for d in das:
        for sid, spans in by_id.items():
            for b, e in spans:
                o = min(d["end_time"], e) - max(d["start_time"], b)
                if o > 0:
                    overlap[d["speaker"]][sid] += o
    out: dict[str, str] = {}
    for letter, scores in overlap.items():
        out[letter] = max(scores, key=scores.get)
    return out


def assign_words(
    das: list[dict], words_by_id: dict[str, list[tuple[float, float, str]]], letters: dict[str, str]
) -> dict:
    """da_id -> the words (absolute times) of its speaker whose midpoint falls in its span."""
    import bisect

    out: dict[str, str] = {}
    index = {sid: (sorted(ws), [(a + b) / 2 for a, b, _ in sorted(ws)]) for sid, ws in words_by_id.items()}
    for d in das:
        sid = letters.get(d["speaker"])
        if sid is None or sid not in index:
            out[d["da_id"]] = ""
            continue
        ws, mids = index[sid]
        lo = bisect.bisect_left(mids, d["start_time"])
        hi = bisect.bisect_right(mids, d["end_time"])
        out[d["da_id"]] = " ".join(w for _, _, w in ws[lo:hi]).strip()
    return out


def wer(ref: str, hyp: str) -> tuple[int, int]:
    """Word edits and reference words, after lower-casing and dropping punctuation."""
    import re

    r = re.findall(r"[a-z0-9']+", ref.lower())
    h = re.findall(r"[a-z0-9']+", hyp.lower())
    prev = list(range(len(h) + 1))
    for i, rw in enumerate(r, 1):
        cur = [i] + [0] * len(h)
        for j, hw in enumerate(h, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (rw != hw))
        prev = cur
    return prev[-1], len(r)
