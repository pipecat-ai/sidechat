"""Phase 6 from found data: real speech through real speech-to-text, in one detached Modal job.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.phase6::run --exp exp-056-side-phase6-stt

    uv run python -m sidechat.pipeline.results exp-056-side-phase6-stt

No real calls can be recorded (SQ-05), so scorecard item 15 is measured on AMI: real meetings with
human transcripts and each speaker's headset audio. Steps, each its own experiment named after this
one:

    stt      AMI's headset audio for the 22 labelled meetings and the silence test's, through
             Deepgram (`sidechat/pipeline/stt_ami.py`)
    jev      Jev on the transcribed lines (`sidechat/pipeline/baseline.py`, stored answers reused)
    score    round 3 (the default build) and rc0.2's agent-1x build on the transcribed lines, at
             their own thresholds (`train.score_sets`)
    summary  runs/side/results/<exp>/report.md: each system on the same lines as written and as
             heard; item 15 (gap at most 3 points, and at least Jev on what was heard)

Every AMI line is for people, so the right decision is always to stay quiet: this measures whether
real transcription errors make a model answer or hold for people's talk. Lines for the agent in real
speech need another source (SLURP's recordings are CC BY-NC, so test only: SD-23).
"""

from __future__ import annotations

import modal

from sidechat.pipeline import baseline as B
from sidechat.pipeline import stt_ami as S
from sidechat.pipeline import stt_slurp as SL
from sidechat.pipeline import train as T

APP_NAME = "waystone-side-phase6"
app = modal.App(APP_NAME)
for other in (S.app, SL.app, B.app, T.app):
    app.include(other)

MODELS = {"side-r3-ettin-150m-s0": "Default build (round 3, 150M)", "side-r6ttr3t-ettin-32m-s0": "agent-1x build (32M)"}
PAIRS = (  # name, as written, as heard
    ("AMI labelled meetings", "ami-addressee-0.1", "ami-addressee-stt-0.1"),
    ("AMI silence test", "ami-silent-0.1.test", "ami-silent-stt-0.1.test"),
)
STT_SETS = "ami-stt,ami-silent-stt:test"
SLURP_SETS = "slurp,slurp-stt"
SLURP_PAIR = ("slurp-in-ami-0.1", "slurp-in-ami-stt-0.1")


def requests_compare(gold: dict[str, str], heard: dict[str, str], named: set[str]) -> dict:
    """SLURP's requests as written and as heard: answered now when named; answered now, held or
    missed when not (the guide's right answer there is to hold)."""
    from sidechat.lib.score import paired, share

    ids = sorted(set(gold) & set(heard))
    nm = [i for i in ids if i in named]
    un = [i for i in ids if i not in named]

    def m(d: dict[str, str]) -> dict:
        return {
            "named_answered": share(sum(d[i] == "respond" for i in nm), len(nm)),
            "unnamed_answered": share(sum(d[i] == "respond" for i in un), len(un)),
            "unnamed_held": share(sum(d[i] == "wait" for i in un), len(un)),
            "unnamed_missed": share(sum(d[i] == "ignore" for i in un), len(un)),
        }

    return {
        "named": len(nm),
        "unnamed": len(un),
        "written": m(gold),
        "heard": m(heard),
        "named_gap": paired([gold[i] == "respond" for i in nm], [heard[i] == "respond" for i in nm]),
        "unnamed_handled_gap": paired([gold[i] != "ignore" for i in un], [heard[i] != "ignore" for i in un]),
    }


def _render_slurp(exp: str, stt: dict, rows: dict) -> str:
    def p(x: dict | None) -> str:
        return _pct(x, 1)

    lines = [
        f"# Requests to the agent in real speech: SLURP in AMI meetings ({exp})",
        "",
        (
            f"SLURP's recorded requests (test split, headset microphone; {stt.get('heard', 0):,} heard, "
            f'{stt.get("named", 0)} saying "Olly"; word error rate {100 * stt.get("word_error_rate", 0):.1f}%), '
            "each said at a seeded point in an AMI silence-test meeting by one of its speakers. The agent, Olly, "
            "has not spoken. Written: SLURP's text and AMI's transcripts. Heard: what Deepgram heard of both."
        ),
        "",
        (
            "The guide's right answer: a named request is answered now; an unnamed one is held for a pause "
            "(Duplex-MPE would count only answering now)."
        ),
        "",
        "| System | Named, answered now: written / heard | Unnamed: answered now | Unnamed: held | Unnamed: missed |",
        "|---|---|---|---|---|",
    ]
    for system, c in rows.items():
        w, h = c["written"], c["heard"]
        lines.append(
            f"| {system} | {p(w['named_answered'])} / {p(h['named_answered'])} | {p(w['unnamed_answered'])} / {p(h['unnamed_answered'])} | "
            f"{p(w['unnamed_held'])} / {p(h['unnamed_held'])} | {p(w['unnamed_missed'])} / {p(h['unnamed_missed'])} |"
        )
    lines += [
        "",
        "Each cell: written / heard. Lines: "
        + ", ".join(f"{s} {c['named']} named and {c['unnamed']} unnamed" for s, c in list(rows.items())[:1])
        + ".",
    ]
    return "\n".join(lines) + "\n"


def decisions(kind: str, scored: list[dict], t: dict | None = None) -> dict[str, str]:
    """da_id -> respond / wait / ignore, for a model's predictions (`t` its thresholds) or Jev's scores."""
    from sidechat.baselines import jev_demo
    from sidechat.train import evaluate as E

    out = {}
    for x in scored:
        da = x["row_id"].split("/", 1)[1]
        out[da] = E.decide(x, t) if kind == "model" else jev_demo.decision(x["addressed"], x["question"])
    return out


def compare(gold: dict[str, str], heard: dict[str, str]) -> dict:
    """The same lines as written and as heard; every line should be left alone."""
    from sidechat.lib.score import paired, share

    ids = sorted(set(gold) & set(heard))
    n = len(ids)

    def m(d: dict[str, str]) -> dict:
        return {
            "quiet": share(sum(d[i] == "ignore" for i in ids), n),
            "answered": share(sum(d[i] == "respond" for i in ids), n),
            "held": share(sum(d[i] == "wait" for i in ids), n),
        }

    return {
        "n": n,
        "written": m(gold),
        "heard": m(heard),
        "gap": paired([gold[i] == "ignore" for i in ids], [heard[i] == "ignore" for i in ids]),
    }


def _pct(x: dict | None, digits: int = 2) -> str:
    if not x or x.get("value") is None:
        return "n/a"
    return f"{100 * x['value']:.{digits}f}% ({x['k']:,})"


def _render(exp: str, stt: dict, table: dict, verdict: dict) -> str:
    lines = [
        f"# Real speech through speech-to-text ({exp})",
        "",
        (
            f"AMI's headset audio through {stt.get('stt', {}).get('service', 'STT')} "
            f"(`{stt.get('stt', {}).get('params', {})}`): {stt.get('dialogue_acts', 0):,} dialogue acts, "
            f"{stt.get('empty_transcripts', 0):,} heard as nothing (left out), word error rate "
            f"{100 * stt.get('word_error_rate', 0):.1f}% against AMI's transcripts."
        ),
        "",
        "Every line is for people. Shares of the same lines, as written and as heard; `(k)` is the count.",
        "",
    ]
    for name, rows in table.items():
        lines += [
            f"## {name}",
            "",
            "| System | Lines | Left alone, written | Left alone, heard | Gap (points) | Answered, written | Answered, heard | Held, written | Held, heard |",
            "|---|---|---|---|---|---|---|---|---|",
        ]
        for system, c in rows.items():
            g = c["gap"]
            gap = (
                f"{100 * g['diff']:+.2f} ({100 * g['ci95'][0]:+.2f} to {100 * g['ci95'][1]:+.2f})"
                if g.get("diff") is not None
                else "n/a"
            )
            lines.append(
                f"| {system} | {c['n']:,} | {_pct(c['written']['quiet'])} | {_pct(c['heard']['quiet'])} | {gap} | "
                f"{_pct(c['written']['answered'])} | {_pct(c['heard']['answered'])} | {_pct(c['written']['held'], 1)} | {_pct(c['heard']['held'], 1)} |"
            )
        lines.append("")
    lines += ["## Item 15", ""]
    for system, v in verdict.items():
        lines.append(f"- {system}: **{'met' if v['met'] else 'not met'}**. {v['why']}")
    return "\n".join(lines) + "\n"


NAME_SETS = (
    "slurp,slurp-stt,slurp-stt-keyterm,duplex,ambient,pilot-0.4@anonymous,demo,"
    "corpus:gen-0.2:test@anonymous,corpus:gen-0.4:test@anonymous"
)
NAME_KINDS = ("name_misheard", "name_word_sense", "alias_false_match", "similar_name_person")
SLURP_NAMED = ("name_first", "name_mid", "name_last")


def _sum(slices: dict, kinds: tuple[str, ...], key: str) -> dict | None:
    from sidechat.lib.score import share

    parts = [((slices.get(k) or {}).get("sidechat") or {}).get(key) for k in kinds]
    parts = [x for x in parts if x and x.get("n")]
    if not parts:
        return None
    return share(sum(x["k"] for x in parts), sum(x["n"] for x in parts))


def name_metrics(cards: dict[str, dict]) -> dict:
    """The numbers the names summary compares, from score_sets' cards (rows_id -> card)."""
    out: dict = {}

    def side(card: dict, key: str) -> dict | None:
        return (card.get("sidechat") or {}).get(key)

    for rows_id, c in cards.items():
        if rows_id.startswith("slurp-in-ami"):
            k = c.get("by_kind") or {}
            out[f"{rows_id}: named answered now"] = _sum(k, SLURP_NAMED, "answered_now")
            out[f"{rows_id}: unnamed held"] = _sum(k, ("open_request",), "open_held")
        elif rows_id == "duplex-mpe-0.1":
            ce = c.get("by_condition_event") or {}
            out["Duplex-MPE right"] = side(c, "decision_right")
            out["Duplex-MPE for others, answered outright"] = side(c, "answers_now_wrongly")
            out["Duplex-MPE named request answered"] = _sum(ce, ("explicit/T",), "answered_now")
            out["Duplex-MPE name mentioned, answered outright (N1)"] = _sum(
                ce, ("explicit/N1", "implicit/N1"), "answers_now_wrongly"
            )
        elif rows_id.startswith("gen-"):
            k = c.get("by_kind") or {}
            out[f"{rows_id} right"] = side(c, "decision_right")
            out[f"{rows_id}: misheard name answered"] = _sum(k, ("name_misheard",), "answered_now")
            out[f"{rows_id}: name as a word / sound-alike left alone"] = _sum(
                k, ("name_word_sense", "alias_false_match", "similar_name_person"), "quiet_kept"
            )
        else:
            out[f"{rows_id} right"] = side(c, "decision_right")
            out[f"{rows_id} for others, answered outright"] = side(c, "answers_now_wrongly")
    return out


def _names(exp: str, want: list[str], jev_cap_usd: float, save, wait, status: dict) -> dict:
    from datetime import UTC, datetime

    from sidechat.lib import r2

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    if "stt" in want:
        save(stage="stt with the name as a keyterm")
        status["steps"]["stt"] = wait({"stt": SL.run.spawn(f"{exp}-stt", keyterm="Olly")})["stt"]
        if (status["steps"]["stt"] or {}).get("state") != "done":
            save(state="failed", reason=f"speech-to-text did not finish: {status['steps']['stt']}")
            return {"state": "failed"}
    if "jev" in want:  # before scoring, so the cards carry Jev
        save(stage="jev")
        status["steps"]["jev"] = wait(
            {"jev": B.run.spawn(f"{exp}-jev", sets="slurp-stt-keyterm", spend_cap_usd=jev_cap_usd)}
        )["jev"]
    if "score" in want:
        save(stage="scoring, plain and with name spellings")
        calls = {f"{r} {n}": T.score_sets.spawn(r, NAME_SETS, names=n) for r in MODELS for n in ("plain", "variants")}
        got = wait(calls)
        status["steps"].update(
            {k: (v.get("state") or "done") if isinstance(v, dict) and "state" in v else "done" for k, v in got.items()}
        )
    save(stage="summary")
    table: dict = {}
    for run_id, label in MODELS.items():
        for n in ("plain", "variants"):
            cards = {}
            for k in r2.list_keys(s3, f"{r2.PREFIX}/predictions/{run_id}/{n}/sets/"):
                rows_id = k["Key"].rsplit("/", 1)[-1][: -len(".json")]
                cards[rows_id] = r2.get_json(s3, k["Key"]) or {}
            table[f"{label}, {n}"] = name_metrics(cards)
            if n == "plain":
                jev = {
                    rid: {
                        "sidechat": c.get("jev") or {},
                        "by_kind": {k: {"sidechat": v.get("jev") or {}} for k, v in (c.get("by_kind") or {}).items()},
                        "by_condition_event": {
                            k: {"sidechat": v.get("jev") or {}} for k, v in (c.get("by_condition_event") or {}).items()
                        },
                    }
                    for rid, c in cards.items()
                }
                table.setdefault("Jev", name_metrics(jev))
    kt = r2.get_json(s3, f"{r2.PREFIX}/stt/slurp-deepgram-nova-3-keyterm/manifest.json") or {}
    card = {
        "exp": exp,
        "test": "names",
        "keyterm_stt": kt,
        "table": table,
        "finished_at": datetime.now(UTC).isoformat(timespec="seconds"),
    }
    r2.put_json(s3, f"{out}/scorecard.json", card)
    keys = sorted({k for v in table.values() for k in v})
    systems = list(table)
    lines = [
        f"# The agent's name as heard ({exp})",
        "",
        (
            f"Deepgram with the keyterm `Olly`: word error rate {100 * kt.get('word_error_rate', 0):.1f}%. "
            "`plain` is each build as released; `variants` adds other spellings of the agent's name as aliases "
            "(`sidechat/names.py`). Shares are `value (k/n)`."
        ),
        "",
        "| | " + " | ".join(systems) + " |",
        "|---|" + "---|" * len(systems),
    ]
    for k in keys:
        cells = []
        for s_ in systems:
            x = table[s_].get(k)
            cells.append(
                "n/a" if not x or x.get("value") is None else f"{100 * x['value']:.1f}% ({x['k']:,}/{x['n']:,})"
            )
        lines.append(f"| {k} | " + " | ".join(cells) + " |")
    r2.put_text(s3, f"{out}/report.md", "\n".join(lines) + "\n")
    save(state="done", stage="done")
    return {"state": "done"}


@app.function(image=S.image, cpu=0.25, memory=1024, timeout=10 * 3600, secrets=S._secrets())
def run(
    exp: str = "exp-056-side-phase6-stt",
    steps: str = "stt,jev,score",
    jev_cap_usd: float = 3.0,
    test: str = "ami",
    wait_for: str = "",
) -> dict:
    """`test` "ami" is item 15 on AMI's own lines; "slurp" is SLURP's requests said in AMI's
    meetings (it needs the AMI transcripts, so `wait_for` can name that run's speech-to-text step);
    "names" measures the agent's name as heard: Deepgram's keyterm prompting and other spellings of
    the name as aliases (`sidechat/names.py`), on every set, plain against with spellings."""
    import time
    import traceback
    from datetime import UTC, datetime

    from sidechat.lib import r2
    from sidechat.sources import ami

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    started = time.monotonic()
    want = [x.strip() for x in steps.split(",") if x.strip()]
    status: dict = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "starting",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {"steps": steps, "jev_cap_usd": jev_cap_usd, "test": test, "wait_for": wait_for},
        "steps": {},
    }

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    def wait(calls: dict) -> dict:
        got = {}
        for k, c in calls.items():
            try:
                got[k] = c.get()
            except Exception as e:  # noqa: BLE001 - a failed branch is reported, the others go on
                got[k] = {"state": "failed", "error": f"{type(e).__name__}: {str(e)[:300]}"}
        return got

    try:
        save()
        for e in [x.strip() for x in wait_for.split(",") if x.strip()]:
            save(stage=f"waiting for {e}")
            while ((r2.get_json(s3, f"{r2.PREFIX}/results/{e}/status.json") or {}).get("state")) not in (
                "done",
                "failed",
                "stopped",
            ):
                time.sleep(60)
        if test == "names":
            return _names(exp, want, jev_cap_usd, save, wait, status)
        sets = SLURP_SETS if test == "slurp" else STT_SETS
        job = SL.run if test == "slurp" else S.run
        if "stt" in want:
            save(stage="stt")
            status["steps"]["stt"] = wait({"stt": job.spawn(f"{exp}-stt")})["stt"]
            if (status["steps"]["stt"] or {}).get("state") != "done":
                save(state="failed", reason=f"speech-to-text did not finish: {status['steps']['stt']}")
                return {"state": "failed"}
        calls = {}
        if "jev" in want:
            calls["jev"] = B.run.spawn(f"{exp}-jev", sets=sets, spend_cap_usd=jev_cap_usd)
        if "score" in want:
            for run_id in MODELS:
                calls[run_id] = T.score_sets.spawn(run_id, sets)
        if calls:
            save(stage="jev and scoring")
            got = wait(calls)
            status["steps"].update(
                {k: (v.get("state") or "done") if isinstance(v, dict) else "done" for k, v in got.items()}
            )

        # Summary.
        save(stage="summary")
        if test == "slurp":
            from sidechat.sources import slurp as SR

            stt = r2.get_json(s3, f"{r2.PREFIX}/{SR.STT_PREFIX}/manifest.json") or {}
            named = {
                r["slurp_id"]
                for r in r2.get_jsonl(s3, f"{r2.PREFIX}/{SR.STT_PREFIX}/transcripts.jsonl") or []
                if SR.named(r["sentence"])
            }
            gold_id, stt_id = SLURP_PAIR
            rows: dict = {}
            for run_id, label in MODELS.items():
                t = (r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json") or {}).get("thresholds")
                g = r2.get_jsonl(s3, f"{r2.PREFIX}/predictions/{run_id}/{gold_id}.jsonl") or []
                h = r2.get_jsonl(s3, f"{r2.PREFIX}/predictions/{run_id}/{stt_id}.jsonl") or []
                if t and g and h:
                    rows[label] = requests_compare(decisions("model", g, t), decisions("model", h, t), named)
            jg = r2.get_jsonl(s3, f"{r2.PREFIX}/baselines/jev-demo-0.1/scores/{gold_id}.jsonl") or []
            jh = r2.get_jsonl(s3, f"{r2.PREFIX}/baselines/jev-demo-0.1/scores/{stt_id}.jsonl") or []
            if jg and jh:
                rows["Jev"] = requests_compare(decisions("jev", jg), decisions("jev", jh), named)
            card = {
                "exp": exp,
                "test": test,
                "stt": stt,
                "table": rows,
                "finished_at": datetime.now(UTC).isoformat(timespec="seconds"),
            }
            r2.put_json(s3, f"{out}/scorecard.json", card)
            r2.put_text(s3, f"{out}/report.md", _render_slurp(exp, stt, rows))
            save(state="done", stage="done")
            return {"state": "done"}
        stt = r2.get_json(s3, f"{r2.PREFIX}/{ami.STT_PREFIX}/manifest.json") or {}
        table: dict = {}
        for name, gold_id, stt_id in PAIRS:
            rows: dict = {}
            for run_id, label in MODELS.items():
                t = (r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json") or {}).get("thresholds")
                g = r2.get_jsonl(s3, f"{r2.PREFIX}/predictions/{run_id}/{gold_id}.jsonl") or []
                h = r2.get_jsonl(s3, f"{r2.PREFIX}/predictions/{run_id}/{stt_id}.jsonl") or []
                if t and g and h:
                    rows[label] = compare(decisions("model", g, t), decisions("model", h, t))
            jg = r2.get_jsonl(s3, f"{r2.PREFIX}/baselines/jev-demo-0.1/scores/{gold_id}.jsonl") or []
            jh = r2.get_jsonl(s3, f"{r2.PREFIX}/baselines/jev-demo-0.1/scores/{stt_id}.jsonl") or []
            if jg and jh:
                rows["Jev"] = compare(decisions("jev", jg), decisions("jev", jh))
            table[name] = rows
        verdict = {}
        main = table.get(PAIRS[0][0]) or {}
        jev_heard = ((main.get("Jev") or {}).get("heard") or {}).get("quiet", {}).get("value")
        for label in MODELS.values():
            c = main.get(label)
            if not c or c["gap"].get("diff") is None:
                continue
            gap = 100 * c["gap"]["diff"]
            heard = c["heard"]["quiet"]["value"]
            ok_gap = gap >= -3.0
            ok_jev = jev_heard is None or heard >= jev_heard
            verdict[label] = {
                "met": ok_gap and ok_jev and jev_heard is not None,
                "why": f"gap {gap:+.2f} points (bar: no worse than -3); left alone as heard {100 * heard:.2f}%"
                + (f", Jev {100 * jev_heard:.2f}%" if jev_heard is not None else ", Jev not scored"),
            }
        card = {
            "exp": exp,
            "stt": stt,
            "table": table,
            "verdict": verdict,
            "finished_at": datetime.now(UTC).isoformat(timespec="seconds"),
        }
        r2.put_json(s3, f"{out}/scorecard.json", card)
        r2.put_text(s3, f"{out}/report.md", _render(exp, stt, table, verdict))
        save(state="done", stage="done")
        return {"state": "done", "verdict": verdict}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
