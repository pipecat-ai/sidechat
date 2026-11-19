"""Run an exported Sidechat model on CPU: ONNX Runtime and tokenizers, no torch.

    from sidechat.runtime import load
    model = load("models/side-r1-ettin-68m-s0")      # the folder `sidechat.pipeline.fetch` saves
                                                       # (int8=True for the int8 build, if exported)
    answer = model.answer(request)                     # a SidechatAnswer
    model.decide(answer)                               # "respond", "wait" or "ignore", with the dev thresholds

The folder holds `model.onnx`, `tokenizer.json` and `config.json` (temperatures, thresholds,
input version). Inputs are built exactly as in training (`sidechat/train/features.py`).
"""

from __future__ import annotations

import json
import math
import pathlib
import threading
from collections import OrderedDict
from dataclasses import dataclass

from sidechat.schema import INTENTS, SidechatAnswer, SidechatRequest
from sidechat.train import features


def _softmax(xs: list[float], t: float) -> list[float]:
    m = max(x / t for x in xs)
    e = [math.exp(x / t - m) for x in xs]
    s = sum(e)
    return [x / s for x in e]


def _sigmoid(x: float, t: float) -> float:
    return 1 / (1 + math.exp(-x / t))


@dataclass
class Sidechat:
    session: object
    tokenizer: object
    config: dict

    @property
    def thresholds(self) -> dict:
        return self.config.get("thresholds") or {"respond": 0.7, "wait": 0.4, "open": 0.5}

    def _inputs(self, reqs: list[SidechatRequest]) -> dict:
        import numpy as np

        max_len = self.config["max_len"]
        turns = self.config.get("text_turns", 0)
        encs, starts = [], []
        for q in reqs:
            if turns:
                text, start = features.fitted(q, turns, max_len, lambda t: len(self.tokenizer.encode(t).ids))
            else:
                text, start = features.text(q)
            enc = self.tokenizer.encode(text)
            encs.append(enc)
            starts.append(start)
        n = min(max_len, max(len(e.ids) for e in encs))
        ids = np.zeros((len(encs), n), dtype=np.int64)
        mask = np.zeros((len(encs), n), dtype=np.int64)
        line = np.zeros((len(encs), n), dtype=np.int64)
        for i, (e, start) in enumerate(zip(encs, starts)):
            k = min(n, len(e.ids))
            ids[i, :k] = e.ids[:k]
            mask[i, :k] = 1
            for j in range(k):
                if e.offsets[j][0] >= start:
                    line[i, j] = 1
            if line[i].sum() == 0:
                line[i, max(0, k - 16) : k] = 1
        num = np.array([features.numbers(q) for q in reqs], dtype=np.float32)
        return {"ids": ids, "mask": mask, "line_mask": line, "num": num}

    def answers(self, reqs: list[SidechatRequest]) -> list[SidechatAnswer]:
        t = self.config["temperatures"]
        li, lr, lu = self.session.run(None, self._inputs(reqs))
        out = []
        for a, b, c in zip(li, lr, lu):
            probs = _softmax([float(x) for x in a], t["intent"])
            out.append(
                SidechatAnswer(
                    intent={k: round(p, 6) for k, p in zip(INTENTS, probs)},
                    respond=round(_sigmoid(float(b), t["respond"]), 6),
                    unclear=round(_sigmoid(float(c), t["unclear"]), 6),
                )
            )
        return out

    def answer(self, req: SidechatRequest) -> SidechatAnswer:
        return self.answers([req])[0]

    def prepare(self, req: SidechatRequest) -> None:
        """Nothing to do ahead of time for a single-tower model (see `TwoTower.prepare`)."""

    def decide(self, answer: SidechatAnswer, thresholds: dict | None = None) -> str:
        t = thresholds or self.thresholds
        if answer.respond >= t["respond"]:
            return "respond"
        if answer.respond >= t["wait"] or answer.intent["open"] >= t["open"]:
            return "wait"
        return "ignore"


class TwoTower(Sidechat):
    """A two-tower model (`sidechat-tt-0.1`): `context.onnx` encodes the history, `line.onnx` the
    line with the cached history. Call `prepare` with the next line's history as soon as it is known
    (when the previous line ends) and `answer` then only encodes the new line. A history seen before
    is never encoded twice; the cache keeps the last few."""

    def __init__(self, context_session, line_session, tokenizer, config: dict, keep: int = 16):
        super().__init__(line_session, tokenizer, config)
        self.context_session = context_session
        self._cache: OrderedDict[str, tuple] = OrderedDict()
        self._keep = keep
        self._lock = threading.Lock()  # `prepare` may run in another thread than `answer`

    def _ids(self, text: str, limit: int):
        import numpy as np

        ids = self.tokenizer.encode(text).ids[:limit]
        return np.array([ids], dtype=np.int64), np.ones((1, len(ids)), dtype=np.int64)

    def _context(self, req: SidechatRequest) -> tuple:
        n = self.config["ctx_len"]
        text = features.context_fitted(req, n, lambda t: len(self.tokenizer.encode(t).ids))
        with self._lock:
            hit = self._cache.get(text)
            if hit is not None:
                self._cache.move_to_end(text)
                return hit
        ids, mask = self._ids(text, n)
        states = self.context_session.run(None, {"ids": ids, "mask": mask})[0]
        with self._lock:
            self._cache[text] = (states, mask)
            while len(self._cache) > self._keep:
                self._cache.popitem(last=False)
        return states, mask

    def prepare(self, req: SidechatRequest) -> None:
        """Encode and cache this request's history now; its line is not read."""
        self._context(req)

    def answers(self, reqs: list[SidechatRequest]) -> list[SidechatAnswer]:
        import numpy as np

        t = self.config["temperatures"]
        out = []
        for q in reqs:
            states, cmask = self._context(q)
            ids, mask = self._ids(features.line_text(q), self.config["line_len"])
            num = np.array([features.numbers(q)], dtype=np.float32)
            li, lr, lu = self.session.run(
                None, {"ids": ids, "mask": mask, "ctx": states, "ctx_mask": cmask, "num": num}
            )
            probs = _softmax([float(x) for x in li[0]], t["intent"])
            out.append(
                SidechatAnswer(
                    intent={k: round(p, 6) for k, p in zip(INTENTS, probs)},
                    respond=round(_sigmoid(float(lr[0]), t["respond"]), 6),
                    unclear=round(_sigmoid(float(lu[0]), t["unclear"]), 6),
                )
            )
        return out


def load(folder: str | pathlib.Path, threads: int = 4, int8: bool = False) -> Sidechat:
    """`int8=True` loads the int8 build (`model-int8.onnx`, or `context-int8.onnx` and
    `line-int8.onnx` for a two-tower model) when the export made one; its own thresholds, if the
    export chose them, replace the fp32 ones."""
    import onnxruntime as ort
    from tokenizers import Tokenizer

    folder = pathlib.Path(folder)
    opts = ort.SessionOptions()
    opts.intra_op_num_threads = threads
    opts.inter_op_num_threads = 1
    config = json.loads((folder / "config.json").read_text())
    tt = config.get("arch") == "twotower"
    graphs = ["context", "line"] if tt else ["model"]
    sessions = []
    for g in graphs:
        name = f"{g}-int8.onnx" if int8 else f"{g}.onnx"
        if not (folder / name).exists():
            raise FileNotFoundError(f"{folder / name} not found")
        sessions.append(ort.InferenceSession(str(folder / name), opts, providers=["CPUExecutionProvider"]))
    tokenizer = Tokenizer.from_file(str(folder / "tokenizer.json"))
    # The inputs are cut here, by length, never by the tokenizer: a tokenizer.json saved after a
    # call with `max_length` keeps that truncation (a two-tower export kept the line's 96 tokens and
    # cut every history to 96, exp-036).
    tokenizer.no_truncation()
    tokenizer.no_padding()
    if int8 and config.get("thresholds_int8"):
        config = {**config, "thresholds": config["thresholds_int8"]}
    want = features.TT_VERSION if tt else features.INPUT_VERSION
    if config.get("input_version") != want:
        raise ValueError(f"model expects {config.get('input_version')}, this code builds {want}")
    if tt:
        return TwoTower(sessions[0], sessions[1], tokenizer, config)
    return Sidechat(sessions[0], tokenizer, config)
