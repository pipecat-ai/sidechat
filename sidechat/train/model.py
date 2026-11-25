"""The Sidechat model: an Ettin encoder over the text, plus the numbers, into three heads.

    intent   five-way softmax: direct, indirect, open, about, other
    respond  sigmoid: how likely the agent should speak now (soft targets: an even call is 0.5)
    unclear  sigmoid: the line fits the agent and someone else equally

The encoder is pooled twice: over the whole input (the conversation) and over the line's own
tokens, so the heads see both what came before and the line itself. Needs torch and transformers;
imported only inside the training and scoring jobs.
"""

from __future__ import annotations

import random
import re

import torch
from torch import nn

from sidechat.schema import INTENTS, SidechatRequest
from sidechat.train import features

ENCODERS = {
    "ettin-32m": ("jhu-clsp/ettin-encoder-32m", "1b8ba06455dd44f80fc9c1ca9e22806157a57379"),
    "ettin-68m": ("jhu-clsp/ettin-encoder-68m", "ac19ae4bc51093b31c475665ac872a936d056cc2"),
    "ettin-150m": ("jhu-clsp/ettin-encoder-150m", "45d08642849e5c5701b162671ac811b7654bfd9f"),
}


class SidechatModel(nn.Module):
    def __init__(
        self,
        encoder: str,
        num_dim: int = features.NUM_DIM,
        dropout: float = 0.1,
        pretrained: bool = True,
        attn: str | None = None,
    ):
        from transformers import AutoConfig, AutoModel

        super().__init__()
        repo, rev = ENCODERS[encoder]
        kw = {"attn_implementation": attn} if attn else {}
        if pretrained:
            self.enc = AutoModel.from_pretrained(repo, revision=rev, **kw)
        else:
            self.enc = AutoModel.from_config(AutoConfig.from_pretrained(repo, revision=rev), **kw)
        h = self.enc.config.hidden_size
        self.num = nn.Sequential(nn.Linear(num_dim, 64), nn.GELU())
        self.mix = nn.Sequential(nn.Dropout(dropout), nn.Linear(2 * h + 64, 256), nn.GELU(), nn.Dropout(dropout))
        self.intent = nn.Linear(256, len(INTENTS))
        self.respond = nn.Linear(256, 1)
        self.unclear = nn.Linear(256, 1)

    def forward(self, ids, mask, line_mask, num):
        h = self.enc(input_ids=ids, attention_mask=mask).last_hidden_state
        m = mask.unsqueeze(-1).to(h.dtype)
        lm = line_mask.unsqueeze(-1).to(h.dtype)
        pooled = (h * m).sum(1) / m.sum(1).clamp(min=1.0)
        line = (h * lm).sum(1) / lm.sum(1).clamp(min=1.0)
        x = self.mix(torch.cat([pooled, line, self.num(num)], dim=-1))
        return self.intent(x), self.respond(x).squeeze(-1), self.unclear(x).squeeze(-1)


def _mean(h, mask):
    m = mask.unsqueeze(-1).to(h.dtype)
    return (h * m).sum(1) / m.sum(1).clamp(min=1.0)


class TwoTowerModel(nn.Module):
    """One encoder used twice (`sidechat-tt-0.1`): over the history, whose token states are cached
    while the next person talks, and over the line when they stop. The line's tokens read the
    cached history through one cross-attention layer; the heads see the line, the history, what the
    line drew from it, and the rhythm numbers. Attention is written out, so it exports to ONNX."""

    def __init__(
        self,
        encoder: str,
        num_dim: int = features.NUM_DIM,
        dropout: float = 0.1,
        pretrained: bool = True,
        attn: str | None = None,
        heads: int = 4,
    ):
        from transformers import AutoConfig, AutoModel

        super().__init__()
        repo, rev = ENCODERS[encoder]
        kw = {"attn_implementation": attn} if attn else {}
        if pretrained:
            self.enc = AutoModel.from_pretrained(repo, revision=rev, **kw)
        else:
            self.enc = AutoModel.from_config(AutoConfig.from_pretrained(repo, revision=rev), **kw)
        h = self.enc.config.hidden_size
        self.heads, self.dh = heads, h // heads
        self.q, self.k, self.v, self.o = (nn.Linear(h, h) for _ in range(4))
        self.num = nn.Sequential(nn.Linear(num_dim, 64), nn.GELU())
        self.mix = nn.Sequential(nn.Dropout(dropout), nn.Linear(3 * h + 64, 256), nn.GELU(), nn.Dropout(dropout))
        self.intent = nn.Linear(256, len(INTENTS))
        self.respond = nn.Linear(256, 1)
        self.unclear = nn.Linear(256, 1)

    def encode_context(self, ids, mask):
        return self.enc(input_ids=ids, attention_mask=mask).last_hidden_state

    def forward_line(self, ids, mask, ctx, ctx_mask, num):
        line = self.enc(input_ids=ids, attention_mask=mask).last_hidden_state
        ctx = ctx.to(line.dtype)
        b, n, _ = line.shape
        t = ctx.shape[1]
        q = self.q(line).view(b, n, self.heads, self.dh).transpose(1, 2)
        k = self.k(ctx).view(b, t, self.heads, self.dh).transpose(1, 2)
        v = self.v(ctx).view(b, t, self.heads, self.dh).transpose(1, 2)
        scores = (q @ k.transpose(-1, -2)) / (self.dh**0.5)
        scores = scores.masked_fill(ctx_mask[:, None, None, :] == 0, -1e4)
        drawn = (torch.softmax(scores.float(), -1).to(v.dtype) @ v).transpose(1, 2).reshape(b, n, -1)
        drawn = self.o(drawn)
        x = self.mix(torch.cat([_mean(line, mask), _mean(ctx, ctx_mask), _mean(drawn, mask), self.num(num)], dim=-1))
        return self.intent(x), self.respond(x).squeeze(-1), self.unclear(x).squeeze(-1)

    def forward(self, ctx_ids, ctx_mask, line_ids, line_mask, num):
        return self.forward_line(line_ids, line_mask, self.encode_context(ctx_ids, ctx_mask), ctx_mask, num)


def build(spec: dict, pretrained: bool = True, attn: str | None = None) -> nn.Module:
    """The model a run's config describes: `arch` "twotower" or the original single tower."""
    cls = TwoTowerModel if spec.get("arch") == "twotower" else SidechatModel
    return cls(spec["encoder"], pretrained=pretrained, attn=attn)


# --- batches ----------------------------------------------------------------------------------

_PUNCT = re.compile(r"[^\w\s']")


def _stt(text: str) -> str:
    """Text as plain speech-to-text writes it: lower case, no punctuation."""
    return " ".join(_PUNCT.sub(" ", text.lower()).split())


_FILLERS = ("uh", "um", "er", "uh", "um", "you know", "I mean", "like")
# Kinds whose label hangs on an exact phrase (a misheard name, a phrase that sounds like it).
_EXACT_KINDS = {"name_misheard", "alias_false_match", "name_word_sense"}


def _disfluent(text: str, rng: random.Random) -> str:
    """Text as people say it: a filler or two, a repeated word, sometimes a filler first. Real
    meeting speech (AMI) is full of these, and every AMI line is for people, so generated lines
    for the agent need them too or disfluency itself would read as "not for the agent"."""
    words = text.split()
    if not words:
        return text
    out = []
    for w in words:
        if rng.random() < 0.1:
            out.append(rng.choice(_FILLERS))
        out.append(w)
        if rng.random() < 0.04 and len(w) <= 5:
            out.append(w)
    if rng.random() < 0.3:
        out.insert(0, rng.choice(("uh", "um", "so", "er")))
    return " ".join(out)


def augment(row: dict, rng: random.Random) -> dict:
    """A training view of a row: a speaker-label condition, sometimes speech-to-text text, sometimes
    a shorter history, sometimes no role for the agent."""
    from sidechat import conditions

    roll = rng.random()
    cond = "anonymous" if roll < 0.6 else "named" if roll < 0.85 else "none"
    row = conditions.apply(row, cond)
    req = dict(row["request"])
    if rng.random() < 0.2:
        req["text"] = _stt(req["text"]) or req["text"]
        req["history"] = [
            {**t, "text": _stt(t["text"]) or t["text"]} if not t.get("agent") else t for t in req["history"]
        ]
    if rng.random() < 0.2 and row["tags"].get("kind") not in _EXACT_KINDS:
        req["text"] = _disfluent(req["text"], rng)
        req["history"] = [
            {**t, "text": _disfluent(t["text"], rng)} if not t.get("agent") and rng.random() < 0.5 else t
            for t in req["history"]
        ]
    if req["history"] and rng.random() < 0.2:
        req["history"] = req["history"][-rng.randint(0, len(req["history"])) :] if rng.random() < 0.8 else []
    if rng.random() < 0.15:
        req["agent"] = {**req["agent"], "role": None}
    return {**row, "request": req}


def targets(label: dict) -> tuple[list[float], float, float]:
    intent = [0.0] * len(INTENTS)
    if label.get("intent"):
        intent[INTENTS.index(label["intent"])] = 1.0
    else:  # unclear lines: could be for the agent or for a person
        intent[INTENTS.index("direct")] = 0.5
        intent[INTENTS.index("other")] = 0.5
    respond = label["respond"] if label.get("respond") is not None else 0.5
    return intent, float(respond), float(bool(label.get("unclear")))


def encode(tok, rows: list[dict], max_len: int, device: str, turns: int = 0) -> dict:
    """`turns` > 0 is the short input: at most that many earlier turns, the oldest dropped until the
    text fits `max_len` (`features.fitted`). 0 keeps the original input, cut at `max_len`."""
    reqs = [SidechatRequest(**r["request"]) for r in rows]
    if turns:
        count = lambda t: len(tok(t)["input_ids"])
        texts, starts = zip(*(features.fitted(q, turns, max_len, count) for q in reqs))
    else:
        texts, starts = zip(*(features.text(q) for q in reqs))
    enc = tok(
        list(texts), truncation=True, max_length=max_len, padding=True, return_offsets_mapping=True, return_tensors="pt"
    )
    offsets = enc.pop("offset_mapping")
    line_mask = torch.zeros_like(enc["attention_mask"])
    for i, start in enumerate(starts):
        line_mask[i] = (offsets[i, :, 0] >= start) & (enc["attention_mask"][i] > 0)
        if line_mask[i].sum() == 0:  # the line was cut off: use the last tokens
            n = int(enc["attention_mask"][i].sum())
            line_mask[i, max(0, n - 16) : n] = 1
    num = torch.tensor([features.numbers(q) for q in reqs], dtype=torch.float32)
    out = {"ids": enc["input_ids"], "mask": enc["attention_mask"], "line_mask": line_mask, "num": num}
    return _with_targets(out, rows, device)


def _with_targets(out: dict, rows: list[dict], device: str) -> dict:
    if "label" in rows[0]:
        t = [targets(r["label"]) for r in rows]
        out["t_intent"] = torch.tensor([x[0] for x in t])
        out["t_respond"] = torch.tensor([x[1] for x in t])
        out["t_unclear"] = torch.tensor([x[2] for x in t])
    return {k: v.to(device) for k, v in out.items()}


def encode_tt(tok, rows: list[dict], ctx_len: int, line_len: int, device: str) -> dict:
    """A two-tower batch: the history (oldest turns dropped to fit `ctx_len`) and the line."""
    reqs = [SidechatRequest(**r["request"]) for r in rows]
    count = lambda t: len(tok(t)["input_ids"])
    c = tok(
        [features.context_fitted(q, ctx_len, count) for q in reqs],
        truncation=True,
        max_length=ctx_len,
        padding=True,
        return_tensors="pt",
    )
    li = tok([features.line_text(q) for q in reqs], truncation=True, max_length=line_len, padding=True, return_tensors="pt")
    num = torch.tensor([features.numbers(q) for q in reqs], dtype=torch.float32)
    out = {
        "ctx_ids": c["input_ids"],
        "ctx_mask": c["attention_mask"],
        "line_ids": li["input_ids"],
        "line_mask": li["attention_mask"],
        "num": num,
    }
    return _with_targets(out, rows, device)


def make_batch(tok, rows: list[dict], spec: dict, device: str) -> dict:
    """A batch for the model `spec` (a run's config) describes."""
    if spec.get("arch") == "twotower":
        return encode_tt(tok, rows, spec["ctx_len"], spec["line_len"], device)
    return encode(tok, rows, spec["max_len"], device, turns=spec.get("text_turns", 0))


def run(net, b: dict):
    if "ctx_ids" in b:
        return net(b["ctx_ids"], b["ctx_mask"], b["line_ids"], b["line_mask"], b["num"])
    return net(b["ids"], b["mask"], b["line_mask"], b["num"])


def loss_fn(out, b) -> torch.Tensor:
    li, lr_, lu = (x.float() for x in out)
    intent = -(b["t_intent"] * torch.log_softmax(li, -1)).sum(-1).mean()
    respond = nn.functional.binary_cross_entropy_with_logits(lr_, b["t_respond"])
    unclear = nn.functional.binary_cross_entropy_with_logits(lu, b["t_unclear"])
    return 1.5 * respond + intent + 0.5 * unclear


@torch.no_grad()
def predict(
    model,
    tok,
    rows: list[dict],
    max_len: int,
    device: str,
    temps: dict | None = None,
    batch: int = 128,
    turns: int = 0,
    spec: dict | None = None,
) -> list[dict]:
    temps = temps or {"intent": 1.0, "respond": 1.0, "unclear": 1.0}
    spec = spec or {"max_len": max_len, "text_turns": turns}
    model.eval()
    out = []
    for i in range(0, len(rows), batch):
        part = rows[i : i + batch]
        b = make_batch(tok, [{"request": r["request"]} for r in part], spec, device)
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device == "cuda"):
            li, lr_, lu = run(model, b)
        pi = torch.softmax(li.float() / temps["intent"], -1).cpu().tolist()
        pr = torch.sigmoid(lr_.float() / temps["respond"]).cpu().tolist()
        pu = torch.sigmoid(lu.float() / temps["unclear"]).cpu().tolist()
        for r, a, b_, c in zip(part, pi, pr, pu):
            out.append(
                {
                    "row_id": r["row_id"],
                    "intent": dict(zip(INTENTS, (round(x, 5) for x in a))),
                    "respond": round(b_, 5),
                    "unclear": round(c, 5),
                }
            )
    return out


@torch.no_grad()
def logits(
    model, tok, rows: list[dict], max_len: int, device: str, batch: int = 128, turns: int = 0, spec: dict | None = None
):
    """Raw logits on rows with labels, for fitting temperatures."""
    spec = spec or {"max_len": max_len, "text_turns": turns}
    model.eval()
    acc = {"li": [], "lr": [], "lu": [], "ti": [], "tr": [], "tu": []}
    for i in range(0, len(rows), batch):
        b = make_batch(tok, rows[i : i + batch], spec, device)
        with torch.autocast("cuda", dtype=torch.bfloat16, enabled=device == "cuda"):
            li, lr_, lu = run(model, b)
        for k, v in (
            ("li", li),
            ("lr", lr_),
            ("lu", lu),
            ("ti", b["t_intent"]),
            ("tr", b["t_respond"]),
            ("tu", b["t_unclear"]),
        ):
            acc[k].append(v.float().cpu())
    return {k: torch.cat(v) for k, v in acc.items()}


def fit_temperatures(lg: dict) -> dict:
    """One temperature per head, by grid search on dev loss."""
    grid = [0.5 + 0.05 * i for i in range(91)]

    def best(fn):
        return min(grid, key=fn)

    bce = nn.functional.binary_cross_entropy_with_logits
    return {
        "intent": round(best(lambda t: float(-(lg["ti"] * torch.log_softmax(lg["li"] / t, -1)).sum(-1).mean())), 3),
        "respond": round(best(lambda t: float(bce(lg["lr"] / t, lg["tr"]))), 3),
        "unclear": round(best(lambda t: float(bce(lg["lu"] / t, lg["tu"]))), 3),
    }
