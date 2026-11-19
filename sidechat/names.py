"""Other spellings of the agent's name, for what a speech-to-text service may write.

Speech-to-text spells an unusual name many ways: SLURP's "Olly" came back from Deepgram as "Oli" and
"Ollie" far more often than as "Olly" (exp-057). The model already reads aliases: they go on the
agent's card and are matched case-insensitively (`sidechat/train/features.py`), and training gave
many agents misheard aliases. So other spellings can be added as aliases at runtime, with no
retraining.

The spellings come from spelling rules alone, never from a test set:

- the same final vowel sound spelled another way: -y, -ie, -i, -ee, -ey (Olly, Ollie, Oli);
- a doubled consonant single, or a single one between vowels doubled (Olly, Oly; Remy, Remmy);
- a final -a as -ah (Nova, Novah); ph as f and f as ph; ck as k.

The name in lower case is not added: a name that is also a word ("Max", "Echo") would then match
the word. Aliases the caller already gave are kept first.
"""

from __future__ import annotations

import re

from sidechat.schema import SidechatRequest

VOWELS = "aeiou"
EE_ENDINGS = ("ie", "ee", "ey", "y", "i")
MAX_VARIANTS = 8


def _consonant_swaps(w: str) -> list[str]:
    out = []
    for i in range(1, len(w) - 1):
        c = w[i]
        if c in VOWELS or not c.isalpha():
            continue
        if w[i + 1] == c:
            out.append(w[:i] + w[i + 1 :])  # doubled -> single
        elif w[i - 1] in VOWELS and w[i + 1] in VOWELS + "y" and c not in "hwxy":
            out.append(w[: i + 1] + c + w[i + 1 :])  # single between vowels -> doubled
    return out


def _letter_swaps(w: str) -> list[str]:
    out = []
    if w.endswith("a"):
        out.append(w + "h")
    if "ph" in w:
        out.append(w.replace("ph", "f"))
    elif "f" in w:
        out.append(w.replace("f", "ph", 1))
    if "ck" in w:
        out.append(w.replace("ck", "k"))
    return out


def _ending(w: str) -> tuple[str, str] | None:
    for end in EE_ENDINGS:
        if w.endswith(end) and len(w) > len(end) + 1 and w[-len(end) - 1] not in VOWELS:
            return w[: -len(end)], end
    return None


def variants(name: str) -> list[str]:
    """Other spellings of a one-word name (capitalised), most likely first; [] for anything else."""
    if not re.fullmatch(r"[A-Za-z]{3,}", name or ""):
        return []
    w = name.lower()
    bases = [w, *_consonant_swaps(w)]
    ordered: list[str] = []
    if _ending(w):
        # The common spellings of the final sound over every base first, the rare ones last.
        for end in ("ie", "i", "y", "", "ee", "ey"):
            for b in bases:
                got = _ending(b)
                if got is None:
                    continue
                ordered.append(b if end == "" else got[0] + end)
    else:
        ordered += bases[1:]
    ordered += _letter_swaps(w) + [v for b in bases[1:] for v in _letter_swaps(b)]
    seen, out = {w}, []
    for v in ordered:
        if v not in seen and len(v) >= 3:
            seen.add(v)
            out.append(v.capitalize())
    return out[:MAX_VARIANTS]


def with_variants(req: SidechatRequest) -> SidechatRequest:
    """The request with the agent's name spellings added to its aliases."""
    a = req.agent
    have = {x.lower() for x in a.aliases} | {a.name.lower()}
    extra = [v for v in variants(a.name) if v.lower() not in have]
    if not extra:
        return req
    return req.model_copy(update={"agent": a.model_copy(update={"aliases": [*a.aliases, *extra]})})


def row_with_variants(row: dict) -> dict:
    """A scoring row with `with_variants` applied to its request."""
    req = with_variants(SidechatRequest(**row["request"]))
    return {**row, "request": req.model_dump(mode="json")}
