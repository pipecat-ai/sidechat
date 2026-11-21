"""Train Sidechat models and score them against Jev, detached on Modal.

    set -a; . ./.env; set +a
    uv run modal run --detach -m sidechat.pipeline.train::run --exp exp-013-side-train-r1 --corpus gen-0.1,gen-pilot --encoders ettin-32m,ettin-68m,ettin-150m

One H100 per encoder trains in parallel. Each saves its best epoch (lowest dev loss in the
anonymous condition) with temperatures fitted on dev to R2:

    models/side/<run_id>/model.safetensors, config.json, tokenizer files

Then each is scored on every test set in every speaker condition, beside Jev on the same rows:

    runs/side/predictions/<run_id>/<set>.jsonl
    runs/side/results/<exp>/status.json, scorecard.json, report.md
"""

from __future__ import annotations

import os
import pathlib

import modal

from sidechat.lib.r2 import R2_KEYS

APP_NAME = "waystone-side-train"
ROOT = pathlib.Path(__file__).resolve().parents[2]

image = (
    modal.Image.debian_slim(python_version="3.12")
    .uv_pip_install("torch==2.14.1", index_url="https://download.pytorch.org/whl/cu126")
    .uv_pip_install(
        "transformers==5.18.0",
        "safetensors==0.8.0",
        "tokenizers==0.23.2",
        "huggingface-hub==1.33.0",
        "numpy==2.2.6",
        "boto3>=1.40",
        "pydantic>=2.9",
        "pyyaml>=6.0",
        "onnx==1.23.2",
        "onnxruntime==1.30.0",
    )
    .env({"HF_HUB_DISABLE_TELEMETRY": "1", "TOKENIZERS_PARALLELISM": "false", "HF_HOME": "/cache/hf"})
    .add_local_python_source("sidechat")
    .add_local_dir(str(ROOT / "data" / "suites"), remote_path="/root/data/suites")
    .add_local_dir(str(ROOT / "contracts"), remote_path="/root/contracts")
)
hf_cache = modal.Volume.from_name("waystone-hf-cache")
app = modal.App(APP_NAME)


def _secrets() -> list:
    if not modal.is_local():
        return [modal.Secret.from_dict({})]
    if os.environ.get("MODAL_ENVIRONMENT") != "waystone":
        raise SystemExit("refusing: MODAL_ENVIRONMENT must be 'waystone'. Load .env first: set -a; . ./.env; set +a")
    return [modal.Secret.from_dict({k: os.environ[k] for k in R2_KEYS})]


def _corpus_rows(s3, corpus: str, splits: set[str], safe_only: bool) -> list[dict]:
    """Rows of the named corpora in these splits. `ami-silent` is the AMI meetings without addressee
    labels (`sidechat/sources/ami.py`); `realreq` is real people's requests said in those meetings
    (`sidechat/sources/realreq.py`). Generated rows take their label from their kind under the
    current guide, so a guide change reaches corpora written before it."""
    from sidechat import guide
    from sidechat.lib import r2
    from sidechat.sources import build

    rows = []
    for gen_id in [g for g in corpus.split(",") if g]:
        if gen_id == "ami-silent" or gen_id.startswith("realreq"):
            got, _, _ = build.build_rows(gen_id)
            rows.extend(r for r in got if r["tags"]["split"] in splits)
            continue
        for r in r2.get_jsonl(s3, f"{r2.PREFIX}/corpus/{gen_id}/rows.jsonl") or []:
            if safe_only and _unsettled_instruction(r):
                continue
            if r["tags"]["split"] in splits and (not safe_only or r["tags"].get("label_safe", "1") == "1"):
                kind = r["tags"].get("kind")
                if kind in guide.KINDS:
                    r["label"] = guide.label_for(kind, r["label"].get("to_people") or None).model_dump(mode="json")
                rows.append(r)
    return rows


def _unsettled_instruction(r: dict) -> bool:
    """An instruction between people written in a session the agent runs or where it controls
    things. The committee reads many of those as for the agent or an even call (exp-024), so they
    are left out of training and scoring; gen-0.2's planner made them, later planners do not."""
    from sidechat.gen import world

    if r["tags"].get("kind") not in ("imperative_to_person", "steps_to_people"):
        return False
    setting = next((x for x in world.SETTINGS if x.id == r["tags"].get("setting")), None)
    return setting is None or setting.leads or bool(setting.controls)


def _is_real(r: dict) -> bool:
    return r["tags"].get("kind") == "ami_silent"


def _model_key(run_id: str, name: str) -> str:
    return f"models/side/{run_id}/{name}"


@app.function(
    image=image,
    gpu="H100",
    cpu=8.0,
    memory=65536,
    timeout=5 * 3600,
    secrets=_secrets(),
    volumes={"/cache": hf_cache},
    retries=modal.Retries(max_retries=1, initial_delay=60.0),
)
def train(
    run_id: str,
    corpus: str,
    encoder: str,
    epochs: int = 3,
    lr: float = 5e-5,
    head_lr: float = 1e-3,
    batch: int = 32,
    seed: int = 0,
    max_len: int = 320,
    warmup: float = 0.1,
    dev_cap: int = 6000,
    train_cap: int = 0,
    text_turns: int = 0,
    teacher: str = "",
    alpha: float = 0.8,
    arch: str = "single",
    ctx_len: int = 320,
    line_len: int = 96,
    drop_kinds: str = "",
    people_only: float = 0.0,
) -> dict:
    """`people_only` is the chance that a training line whose history has the agent's turns loses
    them (`conditions.people_only`); those lines take the teacher's probabilities as their whole target.
    `drop_kinds` (comma-separated) leaves those generated kinds out of training and dev.
    `arch` "twotower" trains the two-tower model (history and line encoded apart, `ctx_len` and
    `line_len` tokens). `text_turns` > 0 trains on the short input (at most that many earlier turns, fitted to
    `max_len`). `teacher` names a trained run to distil from: each batch's targets become
    `alpha` x the teacher's calibrated probabilities on the same augmented lines (read with the
    teacher's own input) + (1 - alpha) x the labels."""
    import random
    import tempfile
    import time

    import torch
    from safetensors.torch import save as st_save
    from transformers import AutoTokenizer

    from sidechat import conditions
    from sidechat.lib import r2
    from sidechat.train import features
    from sidechat.train import model as M

    if people_only and not teacher:
        raise ValueError("people_only needs a teacher: those lines have no label of their own")
    t0 = time.time()
    torch.manual_seed(seed)
    rng = random.Random(seed)
    s3 = r2.client()
    drop = {k for k in drop_kinds.split(",") if k}
    train_rows = [r for r in _corpus_rows(s3, corpus, {"train"}, safe_only=True) if r["tags"].get("kind") not in drop]
    if train_cap:
        rng.shuffle(train_rows)
        train_rows = train_rows[:train_cap]
    dev_rows = [r for r in _corpus_rows(s3, corpus, {"dev"}, safe_only=True) if r["tags"].get("kind") not in drop]
    rng.shuffle(dev_rows)
    dev_rows = [conditions.apply(r, "anonymous") for r in dev_rows[:dev_cap]]
    repo, rev = M.ENCODERS[encoder]
    tok = AutoTokenizer.from_pretrained(repo, revision=rev)
    device = "cuda"
    spec = {
        "arch": arch,
        "encoder": encoder,
        "max_len": max_len,
        "text_turns": text_turns,
        "ctx_len": ctx_len,
        "line_len": line_len,
    }
    net = M.build(spec).to(device)
    enc_params = list(net.enc.parameters())
    enc_ids = {id(p) for p in enc_params}
    head_params = [p for p in net.parameters() if id(p) not in enc_ids]
    opt = torch.optim.AdamW(
        [{"params": enc_params, "lr": lr}, {"params": head_params, "lr": head_lr}], weight_decay=0.01
    )
    steps = epochs * ((len(train_rows) + batch - 1) // batch)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt,
        lambda s: (
            min(1.0, s / max(1, int(warmup * steps))) * max(0.0, (steps - s) / max(1, steps - int(warmup * steps)))
        ),
    )

    tnet = tcfg = ttok = None
    if teacher:
        tnet, ttok, tcfg = _load(s3, teacher, device)
        tnet.eval()

    def distil(part: list[dict], b: dict) -> None:
        """Blend the teacher's probabilities on these lines into the batch's targets (all of the
        target for a people-only line)."""
        t = tcfg["temperatures"]
        with torch.no_grad():
            tb = M.make_batch(ttok, part, tcfg, device)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                li, lr_, lu = M.run(tnet, tb)
            pi = torch.softmax(li.float() / t["intent"], -1)
            pr = torch.sigmoid(lr_.float() / t["respond"])
            pu = torch.sigmoid(lu.float() / t["unclear"])
        a = torch.tensor(
            [1.0 if r["tags"].get("people_only") else alpha for r in part], dtype=torch.float32, device=device
        )
        b["t_intent"] = a[:, None] * pi + (1 - a[:, None]) * b["t_intent"]
        b["t_respond"] = a * pr + (1 - a) * b["t_respond"]
        b["t_unclear"] = a * pu + (1 - a) * b["t_unclear"]

    def dev_loss() -> float:
        net.eval()
        total, n = 0.0, 0
        with torch.no_grad():
            for i in range(0, len(dev_rows), 128):
                part = dev_rows[i : i + 128]
                b = M.make_batch(tok, part, spec, device)
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    out = M.run(net, b)
                total += float(M.loss_fn(out, b)) * len(part)
                n += len(part)
        net.train()
        return total / max(1, n)

    history, best, best_state = [], None, None
    step = 0
    for epoch in range(1, epochs + 1):
        order = list(range(len(train_rows)))
        rng.shuffle(order)
        net.train()
        running = 0.0
        for i in range(0, len(order), batch):
            part = [M.augment(train_rows[j], rng) for j in order[i : i + batch]]
            if people_only:  # draws nothing otherwise, so earlier runs replay
                part = [
                    conditions.people_only(r)
                    if rng.random() < people_only and any(t.get("agent") for t in r["request"]["history"])
                    else r
                    for r in part
                ]
            b = M.make_batch(tok, part, spec, device)
            if tnet is not None:
                distil(part, b)
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = M.run(net, b)
            loss = M.loss_fn(out, b)
            opt.zero_grad(set_to_none=True)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), 1.0)
            opt.step()
            sched.step()
            running += float(loss)
            step += 1
        dl = dev_loss()
        history.append(
            {
                "epoch": epoch,
                "train_loss": round(running / max(1, len(order) // batch), 4),
                "dev_loss": round(dl, 4),
                "secs": round(time.time() - t0),
            }
        )
        if best is None or dl < best:
            best = dl
            best_state = {k: v.detach().to("cpu").clone() for k, v in net.state_dict().items()}
    net.load_state_dict(best_state)
    temps = M.fit_temperatures(M.logits(net, tok, dev_rows, max_len, device, spec=spec))
    best_epoch = min(history, key=lambda h: h["dev_loss"])["epoch"]

    # Save weights, config and tokenizer.
    r2.put_bytes(
        s3, _model_key(run_id, "model.safetensors"), st_save({k: v.contiguous() for k, v in best_state.items()})
    )
    config = {
        "run_id": run_id,
        "encoder": encoder,
        "repo": repo,
        "revision": rev,
        "input_version": features.TT_VERSION if arch == "twotower" else features.INPUT_VERSION,
        "arch": arch,
        "ctx_len": ctx_len if arch == "twotower" else None,
        "line_len": line_len if arch == "twotower" else None,
        "num_dim": features.NUM_DIM,
        "max_len": max_len,
        "temperatures": temps,
        "corpus": corpus,
        "epochs": epochs,
        "best_epoch": best_epoch,
        "history": history,
        "train_rows": len(train_rows),
        "dev_rows": len(dev_rows),
        "lr": lr,
        "head_lr": head_lr,
        "batch": batch,
        "seed": seed,
        "text_turns": text_turns,
        "drop_kinds": sorted(drop) or None,
        "people_only": people_only or None,
        "teacher": teacher or None,
        "alpha": alpha if teacher else None,
    }
    r2.put_json(s3, _model_key(run_id, "config.json"), config)
    with tempfile.TemporaryDirectory() as d:
        tok.save_pretrained(d)
        for f in pathlib.Path(d).iterdir():
            r2.put_bytes(s3, _model_key(run_id, f"tokenizer/{f.name}"), f.read_bytes())
    return {**config, "secs": round(time.time() - t0)}


def _load(s3, run_id: str, device: str, attn: str | None = None):
    import tempfile

    from safetensors.torch import load as st_load
    from transformers import AutoTokenizer

    from sidechat.lib import r2
    from sidechat.train import model as M

    config = r2.get_json(s3, _model_key(run_id, "config.json"))
    net = M.build(config, pretrained=False, attn=attn)
    net.load_state_dict(st_load(r2.get_bytes(s3, _model_key(run_id, "model.safetensors"))))
    net.to(device)
    d = tempfile.mkdtemp()
    for obj in r2.list_keys(s3, _model_key(run_id, "tokenizer/")):
        name = obj["Key"].rsplit("/", 1)[-1]
        pathlib.Path(d, name).write_bytes(r2.get_bytes(s3, obj["Key"]))
    tok = AutoTokenizer.from_pretrained(d)
    return net, tok, config


SCORE_SETS = ("pilot-0.4", "pilot-0.4@anonymous", "demo", "duplex", "ambient", "ami", "ami-silent:test")


@app.function(
    image=image, gpu="H100", cpu=8.0, memory=65536, timeout=3 * 3600, secrets=_secrets(), volumes={"/cache": hf_cache}
)
def score(run_id: str, corpus: str, test_corpus: str = "", extra_sets: str = "", max_held_real: float = 0.0) -> dict:
    """Score on every set. `test_corpus` (default: `corpus`) fixes which corpora's test split is
    "generated test", so rounds compare on the same lines; `extra_sets` are more `build_rows` names."""
    from sidechat import conditions
    from sidechat.lib import r2
    from sidechat.sources import build
    from sidechat.train import evaluate as E
    from sidechat.train import model as M

    s3 = r2.client()
    device = "cuda"
    net, tok, config = _load(s3, run_id, device)
    temps, max_len = config["temperatures"], config["max_len"]

    def run_on(rows: list[dict], name: str) -> dict[str, dict]:
        preds = M.predict(net, tok, rows, max_len, device, temps, spec=config)
        r2.put_jsonl(s3, f"{r2.PREFIX}/predictions/{run_id}/{name}.jsonl", preds)
        return {p["row_id"]: p for p in preds}

    # Thresholds on dev, anonymous, fixed before anything else is scored. AMI's dev series (real
    # speech, every line for people) set a second bar on answering outright, trained on or not.
    dev = [
        conditions.apply(r, "anonymous") for r in _corpus_rows(s3, corpus, {"dev"}, safe_only=True) if not _is_real(r)
    ]
    real = [conditions.apply(r, "anonymous") for r in build.build_rows("ami-silent:dev")[0]]
    dev_preds = run_on(dev + real, "dev@anonymous")
    t = E.choose_thresholds(dev_preds, dev, real_rows=real, max_held_real=max_held_real)

    def jev_scores(rows_id: str) -> dict:
        got = r2.get_jsonl(s3, f"{r2.PREFIX}/baselines/jev-demo-0.1/scores/{rows_id}.jsonl") or []
        return {x["row_id"]: x for x in got}

    card: dict = {"run_id": run_id, "config": config, "thresholds": t, "sets": {}}
    # Named as the row builder names a corpus sample, so row ids pair with Jev's stored answers.
    test_corpus = test_corpus or corpus
    test = [
        {**r, "set": f"{r['set']}.test"}
        for r in _corpus_rows(s3, test_corpus, {"test"}, safe_only=True)
        if not _is_real(r)
    ]
    for cond in ("anonymous", "named", "none"):
        rows = [conditions.apply(r, cond) for r in test]
        preds = run_on(rows, f"test@{cond}")
        first = test_corpus.split(",")[0]
        rows_id = f"{first}.test3000@{cond}" if cond != "named" else f"{first}.test3000"
        jev = jev_scores(rows_id)
        entry = E.set_card(rows, preds, t, jev or None)
        if cond == "anonymous":
            entry["by_writer"] = E.sliced(rows, preds, t, "writer", jev or None)
            entry["by_heldout"] = E.sliced(rows, preds, t, "heldout", jev or None)
            entry["by_rule"] = E.sliced(rows, preds, t, "rule", jev or None)
            entry["by_kind"] = E.sliced(rows, preds, t, "kind", jev or None, min_n=15)
        card["sets"][f"generated test @{cond}"] = entry
    for which in SCORE_SETS + tuple(x for x in extra_sets.split(",") if x):
        rows, manifest, _ = build.build_rows(which)
        preds = run_on(rows, manifest["rows_id"])
        entry = E.set_card(rows, preds, t, jev_scores(manifest["rows_id"]) or None)
        if which.startswith("pilot"):
            entry["by_kind"] = E.sliced(rows, preds, t, "kind", jev_scores(manifest["rows_id"]) or None, min_n=4)
        elif which.startswith(("slurp", "corpus:", "tcl")):  # named against unnamed requests; TCL's kinds
            entry["by_kind"] = E.sliced(rows, preds, t, "kind", jev_scores(manifest["rows_id"]) or None, min_n=1)
        if which == "duplex":
            entry["by_condition_event"] = E.sliced(
                [{**r, "tags": {**r["tags"], "ce": r["tags"]["condition"] + "/" + r["tags"]["event"]}} for r in rows],
                preds,
                t,
                "ce",
                jev_scores(manifest["rows_id"]) or None,
            )
        card["sets"][manifest["rows_id"]] = entry
    r2.put_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json", card)
    return card


@app.function(
    image=image, gpu="H100", cpu=8.0, memory=65536, timeout=2 * 3600, secrets=_secrets(), volumes={"/cache": hf_cache}
)
def score_sets(run_id: str, sets: str, names: str = "") -> dict:
    """Score a trained model on more sets (comma-separated `build_rows` names) at the thresholds its
    own scoring chose, without scoring everything again. Predictions go where `score` puts them;
    the cards go to predictions/<run_id>/sets/<rows_id>.json. `names` "variants" first adds other
    spellings of the agent's name as aliases (`sidechat/names.py`) and keeps everything under
    predictions/<run_id>/variants/ instead; "plain" scores without them under .../plain/."""
    from sidechat import names as N
    from sidechat.lib import r2
    from sidechat.sources import build
    from sidechat.train import evaluate as E
    from sidechat.train import model as M

    s3 = r2.client()
    card = r2.get_json(s3, f"{r2.PREFIX}/predictions/{run_id}/scorecard.json") or {}
    t = card.get("thresholds")
    if not t:
        raise ValueError(f"{run_id} has no stored thresholds: score it first")
    net, tok, config = _load(s3, run_id, "cuda")
    out = {}
    for which in [x.strip() for x in sets.split(",") if x.strip()]:
        rows, manifest, _ = build.build_rows(which)
        rows_id = manifest["rows_id"]
        where = f"{r2.PREFIX}/predictions/{run_id}"
        if names == "variants":
            rows = [N.row_with_variants(r) for r in rows]
            where += "/variants"
        elif names == "plain":  # the same, without variants, kept apart from the stored predictions
            where += "/plain"
        elif names:
            raise ValueError(f"unknown names option {names!r}")
        preds = M.predict(net, tok, rows, config["max_len"], "cuda", config["temperatures"], spec=config)
        r2.put_jsonl(s3, f"{where}/{rows_id}.jsonl", preds)
        jev = {
            x["row_id"]: x for x in r2.get_jsonl(s3, f"{r2.PREFIX}/baselines/jev-demo-0.1/scores/{rows_id}.jsonl") or []
        }
        by_id = {p["row_id"]: p for p in preds}
        entry = {"manifest": manifest, **E.set_card(rows, by_id, t, jev or None)}
        if any(r["tags"].get("kind") for r in rows):
            entry["by_kind"] = E.sliced(rows, by_id, t, "kind", jev or None, min_n=1)
        if rows and "event" in rows[0]["tags"]:
            ce = [{**r, "tags": {**r["tags"], "ce": r["tags"]["condition"] + "/" + r["tags"]["event"]}} for r in rows]
            entry["by_condition_event"] = E.sliced(ce, by_id, t, "ce", jev or None)
        r2.put_json(s3, f"{where}/sets/{rows_id}.json", entry)
        out[rows_id] = {"rows": len(rows)}
    return out


@app.function(
    name="train_run",
    image=image,
    cpu=2.0,
    memory=8192,
    timeout=10 * 3600,
    secrets=_secrets(),
    retries=modal.Retries(max_retries=1, initial_delay=60.0),
    nonpreemptible=True,  # it launches the GPU jobs (sidechat/lib/resume.py)
)
def run(
    exp: str,
    corpus: str = "gen-0.1,gen-pilot",
    encoders: str = "ettin-32m,ettin-68m,ettin-150m",
    epochs: int = 3,
    seed: int = 0,
    tag: str = "r1",
    train_cap: int = 0,
    test_corpus: str = "",
    extra_sets: str = "",
    score_only: bool = False,
    text_turns: int = 0,
    max_len: int = 320,
    teacher: str = "",
    alpha: float = 0.8,
    arch: str = "single",
    ctx_len: int = 320,
    line_len: int = 96,
    drop_kinds: str = "",
    people_only: float = 0.0,
    max_held_real: float = 0.0,
) -> dict:
    """Train one model per encoder in parallel, then score each. `score_only` rescores models
    already trained under these run ids (after a change to scoring). `text_turns`, `max_len`,
    `teacher` and `alpha` are the short input and distillation (`train`)."""
    import time
    import traceback
    from datetime import UTC, datetime

    from sidechat.lib import r2, resume
    from sidechat.train import report

    s3 = r2.client()
    out = f"{r2.PREFIX}/results/{exp}"
    started = time.monotonic()
    status = {
        "exp": exp,
        "app": APP_NAME,
        "state": "running",
        "stage": "training",
        "started_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "args": {
            "corpus": corpus,
            "encoders": encoders,
            "epochs": epochs,
            "seed": seed,
            "tag": tag,
            "test_corpus": test_corpus,
            "extra_sets": extra_sets,
            "score_only": score_only,
            "text_turns": text_turns,
            "max_len": max_len,
            "teacher": teacher,
            "alpha": alpha,
            "arch": arch,
            "ctx_len": ctx_len,
            "line_len": line_len,
            "drop_kinds": drop_kinds,
            "people_only": people_only,
            "max_held_real": max_held_real,
        },
    }
    kept = resume.carried(r2.get_json(s3, f"{out}/status.json"), status["args"])
    if kept:
        status.update(started_at=kept["started_at"], restarts=kept["restarts"])
        status["restarted_at"] = datetime.now(UTC).isoformat(timespec="seconds")
    status["calls"] = kept.get("calls", {})

    def save(**changes) -> None:
        status.update(changes)
        status["updated_at"] = datetime.now(UTC).isoformat(timespec="seconds")
        status["elapsed_s"] = round(time.monotonic() - started)
        r2.put_json(s3, f"{out}/status.json", status)

    spawner = resume.Calls(status["calls"], save)
    try:
        save()
        names = [e for e in encoders.split(",") if e]
        runs = {e: f"side-{tag}-{e}-s{seed}" for e in names}
        calls = (
            {}
            if score_only
            else {
                e: spawner.spawn(
                    f"train/{e}",
                    train,
                    runs[e],
                    corpus,
                    e,
                    epochs=epochs,
                    seed=seed,
                    train_cap=train_cap,
                    max_len=max_len,
                    text_turns=text_turns,
                    teacher=teacher,
                    alpha=alpha,
                    arch=arch,
                    ctx_len=ctx_len,
                    line_len=line_len,
                    drop_kinds=drop_kinds,
                    people_only=people_only,
                )
                for e in names
            }
        )
        trained = {}
        if score_only:
            for e in names:
                cfg = r2.get_json(s3, _model_key(runs[e], "config.json"))
                trained[e] = {**cfg, "secs": 0} if cfg else {"error": "no trained model under this run id"}
        for e, c in calls.items():
            try:
                trained[e] = c.get()
            except Exception as ex:  # noqa: BLE001 - one size failing keeps the others
                trained[e] = {"error": f"{type(ex).__name__}: {str(ex)[:300]}"}
            save(
                trained={
                    k: {x: v.get(x) for x in ("best_epoch", "history", "temperatures", "secs", "error")}
                    for k, v in trained.items()
                }
            )
        save(stage="scoring")
        scored = {}
        score_calls = {
            e: spawner.spawn(f"score/{e}", score, runs[e], corpus, test_corpus, extra_sets, max_held_real)
            for e in names
            if "error" not in trained[e]
        }
        for e, c in score_calls.items():
            try:
                scored[e] = c.get()
            except Exception as ex:  # noqa: BLE001
                scored[e] = {"error": f"{type(ex).__name__}: {str(ex)[:300]}"}
        r2.put_json(s3, f"{out}/scorecard.json", {"trained": trained, "scored": scored})
        r2.put_text(s3, f"{out}/report.md", report.render(exp, trained, scored))
        save(state="done", stage="done")
        return {"state": "done"}
    except Exception as e:
        save(state="failed", reason=f"{type(e).__name__}: {e}", traceback=traceback.format_exc()[-3000:])
        raise
