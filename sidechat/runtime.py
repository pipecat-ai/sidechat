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
        encs, starts = [], []
        for q in reqs:
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

    def decide(self, answer: SidechatAnswer, thresholds: dict | None = None) -> str:
        t = thresholds or self.thresholds
        if answer.respond >= t["respond"]:
            return "respond"
        if answer.respond >= t["wait"] or answer.intent["open"] >= t["open"]:
            return "wait"
        return "ignore"


def load(folder: str | pathlib.Path, threads: int = 4, int8: bool = False) -> Sidechat:
    """`int8=True` loads `model-int8.onnx` (dynamic int8 weights, smaller and faster on CPU) when
    the export made one; its own thresholds, if the export chose them, replace the fp32 ones."""
    import onnxruntime as ort
    from tokenizers import Tokenizer

    folder = pathlib.Path(folder)
    opts = ort.SessionOptions()
    opts.intra_op_num_threads = threads
    opts.inter_op_num_threads = 1
    name = "model-int8.onnx" if int8 else "model.onnx"
    if not (folder / name).exists():
        raise FileNotFoundError(f"{folder / name} not found")
    session = ort.InferenceSession(str(folder / name), opts, providers=["CPUExecutionProvider"])
    tokenizer = Tokenizer.from_file(str(folder / "tokenizer.json"))
    config = json.loads((folder / "config.json").read_text())
    if int8 and config.get("thresholds_int8"):
        config = {**config, "thresholds": config["thresholds_int8"]}
    if config.get("input_version") != features.INPUT_VERSION:
        raise ValueError(f"model expects {config.get('input_version')}, this code builds {features.INPUT_VERSION}")
    return Sidechat(session, tokenizer, config)
