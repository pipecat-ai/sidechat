"""Size and per-line latency of Sidechat beside Jev, through the daily-audience demo's own gate.

Each line is classified the way the demo does it (`AddressingMonitor.classify`) and timed by the
demo's own `classifier_ms`, so both classifiers are measured the same way. Two shapes: the demo's
sample lines as written (0 to 2 earlier lines), and the same lines after a full 8-line history,
the demo's window. Run with the demo's Python, so Pipecat is there:

    set -a; . ./.env; set +a
    PYTHONPATH=. ~/Sites/daily-audience/server/.venv/bin/python scripts/bench_latency.py sidechat models/<run_id>
    PYTHONPATH=. ~/Sites/daily-audience/server/.venv/bin/python scripts/bench_latency.py sidechat models/<run_id> --int8 --threads 4
    PYTHONPATH=. ~/Sites/daily-audience/server/.venv/bin/python scripts/bench_latency.py jev

Prints one JSON line. Jev is asked over the network, so its numbers include the trip from this
machine, and each Jev line costs about $0.00003.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import pathlib
import platform
import resource
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEMO = pathlib.Path(os.environ.get("SIDECHAT_DEMO_DIR") or pathlib.Path.home() / "Sites" / "daily-audience" / "server")
sys.path[:0] = [str(ROOT), str(ROOT / "scripts"), str(DEMO)]

from addressing import AddressingConfig, AddressingMonitor, Roster
from pipecat.processors.aggregators.llm_context import LLMContext
from try_in_demo import SAMPLES, B, split

# An ordinary stretch of talk between the two people, to fill the demo's 8-line window.
LONG = [
    "Jon: Okay, so where did we land on the launch plan?",
    "Sam: The deck is mostly done, just the pricing slide left.",
    "Jon: Right, and marketing wanted the copy by Wednesday.",
    "Sam: They did, but I told them Thursday is more realistic.",
    "Jon: Fair. Did legal sign off on the terms page?",
    "Sam: Not yet, I'm chasing them this afternoon.",
    "Jon: Cool. Let's keep the demo short then, ten minutes tops.",
    "Sam: Agreed, nobody wants a forty-minute walkthrough.",
]


def rss_mb() -> float:
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return round(peak / (1024 * 1024 if sys.platform == "darwin" else 1024), 1)


def cpu_name() -> str:
    info = pathlib.Path("/proc/cpuinfo")
    if info.exists():
        for line in info.read_text().splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    try:
        cmd = ["sysctl", "-n", "machdep.cpu.brand_string"]
        return subprocess.run(cmd, capture_output=True, text=True, check=False).stdout.strip() or platform.processor()
    except OSError:
        return platform.processor()


def limits() -> dict:
    """The container's CPU and memory limits, where cgroups show them (Linux only)."""
    out = {}
    for name, path in (("cpu_max", "/sys/fs/cgroup/cpu.max"), ("memory_max", "/sys/fs/cgroup/memory.max")):
        p = pathlib.Path(path)
        if p.exists():
            out[name] = p.read_text().strip()
    return out


def stats(ms: list[float]) -> dict:
    s = sorted(ms)

    def q(p: float) -> float:
        return round(s[min(len(s) - 1, int(p * len(s)))], 1)

    return {"n": len(s), "mean": round(sum(s) / len(s), 1), "p50": q(0.5), "p90": q(0.9), "p99": q(0.99), "max": round(s[-1], 1)}


def cases() -> dict[str, list[tuple[list[str], str]]]:
    return {
        "demo": list(SAMPLES),
        "full_window": [((LONG + earlier)[-8:], latest) for earlier, latest in SAMPLES],
    }


async def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("which", choices=["sidechat", "jev"])
    ap.add_argument("model", nargs="?", default="")
    ap.add_argument("--int8", action="store_true")
    ap.add_argument("--threads", type=int, default=1, help="the adapter's default is 1")
    ap.add_argument("--rounds", type=int, default=0, help="passes over each shape (default: 5 Sidechat, 2 Jev)")
    args = ap.parse_args()
    rounds = args.rounds or (5 if args.which == "sidechat" else 2)

    out: dict = {"which": args.which, "machine": platform.machine(), "rss_mb_before": rss_mb(), "cpu": cpu_name(),
                 "cpu_count": os.cpu_count(), **limits()}

    t0 = time.perf_counter()
    if args.which == "sidechat":
        from sidechat.integrations.pipecat_classifier import SidechatClassifier

        # No background head start here: each line's history is encoded, untimed, just before it.
        classifier = SidechatClassifier(args.model, bot_name=B, threads=args.threads, int8=args.int8, speculate=False)
        folder = pathlib.Path(args.model)
        arch = json.loads((folder / "config.json").read_text()).get("arch", "single")
        graphs = ["context", "line"] if arch == "twotower" else ["model"]
        out |= {
            "model": classifier.model,
            "build": "int8" if args.int8 else "fp32",
            "threads": args.threads,
            "arch": arch,
            "file_mb": round(sum((folder / f"{g}{'-int8' if args.int8 else ''}.onnx").stat().st_size for g in graphs) / 1e6, 1),
            "tokenizer_mb": round((folder / "tokenizer.json").stat().st_size / 1e6, 1),
        }
    else:
        from pipecat.classifiers.typesafe.jev.classifier import JevClassifier

        classifier = JevClassifier(api_key=os.environ["JEV_API_KEY"], timeout=2.0)  # as the demo's bot.py
        await classifier._client.connect()
        out["model"] = classifier._client._model if hasattr(classifier._client, "_model") else "jev (demo default)"
    out["load_s"] = round(time.perf_counter() - t0, 2)
    out["rss_mb_loaded"] = rss_mb()

    config = AddressingConfig(bot_name=B)
    roster = Roster()
    roster.join({"id": "jon", "info": {"userName": "Jon"}})
    roster.join({"id": "sam", "info": {"userName": "Sam"}})
    monitor = AddressingMonitor(classifier=classifier, context=LLMContext(), roster=roster, config=config)

    two = type(getattr(classifier, "_model", None)).__name__ == "TwoTower"
    prepared: list[float] = []

    async def one(earlier: list[str], latest: str, warm: bool = True) -> float:
        """The demo's classifier_ms for one line. A two-tower model's history is first encoded,
        untimed (as while the person talks), unless `warm` is False."""
        m = split(latest)
        history = [split(x) for x in earlier]
        if two:
            classifier._model._cache.clear()
            if warm:
                t = time.perf_counter()
                classifier.prepare_history(history)
                prepared.append((time.perf_counter() - t) * 1000)
        v = await monitor.classify(history, m["speaker"], m["said"])
        return v.classifier_ms

    first = await one([], SAMPLES[0][1])  # the first line after loading or connecting
    for earlier, latest in SAMPLES[1:4]:
        await one(earlier, latest)
    out["first_line_ms"] = round(first, 1)

    shapes = cases()
    for shape, items in shapes.items():
        ms = []
        for _ in range(rounds):
            for earlier, latest in items:
                ms.append(await one(earlier, latest))
        out[shape] = stats(ms)
        if two:
            out[f"{shape}_history_encode"] = stats(prepared[-len(ms) :])
            cold = [await one(earlier, latest, warm=False) for _ in range(rounds) for earlier, latest in items]
            out[f"{shape}_cold"] = stats(cold)
    out["rss_mb_peak"] = rss_mb()
    if args.which == "jev":
        await classifier._client.close()
    print(json.dumps(out))
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
