"""Statistics for scorecards. Every share comes with its count and a 95% interval.

`wilson`, `share`, `paired` and `ece` are lifted from Audience
(`vendor/audience/audience/lib/score.py`). `bootstrap_diff`, `auroc` and `average_precision` are
new here. Pure Python, so the same code runs in a Modal container and locally.
"""

from __future__ import annotations

import math
import random
from collections import defaultdict


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    """95% Wilson interval for k successes in n."""
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return round(max(0.0, c - h), 4), round(min(1.0, c + h), 4)


def share(k: int, n: int) -> dict:
    return {"value": round(k / n, 4) if n else None, "k": k, "n": n, "ci95": wilson(k, n)}


def paired(a: list[bool], b: list[bool]) -> dict:
    """b against a on the same lines: the difference in share right (b minus a), a 95% interval
    for it (Wald, paired), and whether b is worse beyond noise (the whole interval below zero)."""
    n = len(a)
    if n == 0 or n != len(b):
        return {"n": n, "diff": None}
    only_a = sum(x and not y for x, y in zip(a, b))
    only_b = sum(y and not x for x, y in zip(a, b))
    d = (only_b - only_a) / n
    se = math.sqrt(max(0.0, (only_a + only_b) - (only_b - only_a) ** 2 / n)) / n
    lo, hi = d - 1.96 * se, d + 1.96 * se
    return {
        "n": n,
        "a_right": sum(a),
        "b_right": sum(b),
        "only_a": only_a,
        "only_b": only_b,
        "diff": round(d, 4),
        "ci95": [round(lo, 4), round(hi, 4)],
        "worse_beyond_noise": hi < 0,
        "better_beyond_noise": lo > 0,
    }


def bootstrap_diff(a: list[bool], b: list[bool], resamples: int = 1000, seed: int = 0) -> dict:
    """b minus a on the same lines, with a percentile interval from paired resampling.

    The plan's rule (PLAN.md 3.3): a difference counts when it is 0.1 points or more on a set of at
    least 30 lines, and "worse" means the whole interval is below zero.
    """
    n = len(a)
    if n == 0 or n != len(b):
        return {"n": n, "diff": None}
    rng = random.Random(seed)
    deltas = [int(y) - int(x) for x, y in zip(a, b)]
    d = sum(deltas) / n
    draws = sorted(sum(deltas[rng.randrange(n)] for _ in range(n)) / n for _ in range(resamples))
    lo, hi = draws[int(0.025 * resamples)], draws[min(resamples - 1, int(0.975 * resamples))]
    counts = n >= 30 and abs(d) >= 0.001
    return {
        "n": n,
        "diff": round(d, 4),
        "ci95": [round(lo, 4), round(hi, 4)],
        "counts": counts,
        "worse_beyond_noise": counts and hi < 0,
        "better_beyond_noise": counts and lo > 0,
    }


def ece(pairs: list[tuple[float, float]], bins: int = 10) -> dict:
    """Expected calibration error over equal-width bins. `pairs` are (probability, outcome)."""
    if not pairs:
        return {"value": None, "n": 0}
    groups = defaultdict(list)
    for p, y in pairs:
        groups[min(bins - 1, int(p * bins))].append((p, y))
    total = len(pairs)
    e = sum(
        len(g) / total * abs(sum(p for p, _ in g) / len(g) - sum(y for _, y in g) / len(g)) for g in groups.values()
    )
    return {"value": round(e, 4), "n": total}


def auroc(pairs: list[tuple[float, bool]]) -> dict:
    """Area under the ROC curve: how often a positive line scores above a negative one."""
    pos = sum(1 for _, y in pairs if y)
    neg = len(pairs) - pos
    if pos == 0 or neg == 0:
        return {"value": None, "pos": pos, "neg": neg}
    ranked = sorted(pairs, key=lambda py: py[0])
    rank_sum, i = 0.0, 0
    while i < len(ranked):  # average ranks over ties
        j = i
        while j < len(ranked) and ranked[j][0] == ranked[i][0]:
            j += 1
        mean_rank = (i + 1 + j) / 2
        rank_sum += mean_rank * sum(1 for k in range(i, j) if ranked[k][1])
        i = j
    return {"value": round((rank_sum - pos * (pos + 1) / 2) / (pos * neg), 4), "pos": pos, "neg": neg}


def average_precision(pairs: list[tuple[float, bool]]) -> dict:
    """Area under the precision-recall curve. Reads well when positives are rare."""
    pos = sum(1 for _, y in pairs if y)
    if pos == 0:
        return {"value": None, "pos": 0, "neg": len(pairs)}
    hits, total = 0, 0.0
    for rank, (_, y) in enumerate(sorted(pairs, key=lambda py: -py[0]), start=1):
        if y:
            hits += 1
            total += hits / rank
    return {"value": round(total / pos, 4), "pos": pos, "neg": len(pairs) - pos}


def quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    s = sorted(values)
    return s[min(len(s) - 1, int(q * len(s)))]
