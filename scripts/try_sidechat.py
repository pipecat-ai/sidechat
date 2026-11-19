"""Try a Sidechat model on the daily-audience demo's own sample lines, beside Jev, or on your own.

    set -a; . ./.env; set +a
    uv run python -m sidechat.pipeline.fetch <run_id>          # once: downloads models/<run_id>/
    uv run python scripts/try_sidechat.py models/<run_id>
    uv run python scripts/try_sidechat.py models/<run_id> --anonymous      # speakers as "Speaker 1", no names
    uv run python scripts/try_sidechat.py models/<run_id> --int8           # the int8 build, if exported
    uv run python scripts/try_sidechat.py models/<run_id> --line "Sam: Atlas, what time is it?" --before "Jon: Hi."

The sample lines are the demo's `scripts/try_addressing.py` list. Jev's numbers come from the stored
baseline (exp-001, the demo's exact wording), so no Jev call is made.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from sidechat import conditions  # noqa: E402
from sidechat.runtime import load  # noqa: E402
from sidechat.schema import Agent, SidechatRequest, Turn  # noqa: E402
from sidechat.sources import suites  # noqa: E402

AGENT = Agent(name="Atlas", role="AI assistant on the call")
PEOPLE = ["Jon", "Sam"]


def split(line: str) -> tuple[str, str]:
    speaker, _, said = line.partition(": ")
    return speaker.strip(), said.strip()


def request(latest: str, earlier: list[str], anonymous: bool) -> SidechatRequest:
    speaker, text = split(latest)
    history = []
    for e in earlier:
        s, t = split(e)
        history.append(Turn(speaker=s, text=t, agent=s == AGENT.name))
    req = SidechatRequest(agent=AGENT, text=text, speaker=speaker, history=history, people=PEOPLE)
    if anonymous:
        req = SidechatRequest(**conditions.apply({"row_id": "x/y", "set": "x", "request": req.model_dump(mode="json"),
                                                  "label": {"to_people": []}, "tags": {}}, "anonymous")["request"])
    return req


def jev_for_demo() -> dict[str, tuple[float, float]]:
    """Jev's stored scores for the demo lines, by text, when this machine has them."""
    path = ROOT / "experiments" / "exp-003-side-jev-pilot-0.2" / "scorecard.json"
    if not path.exists():
        return {}
    card = json.loads(path.read_text())
    lines = card["sets"].get("demo-lines-0.1", {}).get("lines", [])
    return {x["text"]: (x["addressed"], x["question"]) for x in lines}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("--anonymous", action="store_true", help="give speakers as 'Speaker 1', with no names")
    ap.add_argument("--line", help="your own line, as 'Speaker: text'")
    ap.add_argument("--before", action="append", default=[], help="an earlier line, as 'Speaker: text' (repeatable)")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--int8", action="store_true", help="use the int8 build (model-int8.onnx), if exported")
    args = ap.parse_args()

    model = load(args.model, threads=args.threads, int8=args.int8)
    t = model.thresholds
    print(f"model {model.config['run_id']} ({model.config['encoder']}); answers at respond >= {t['respond']}, "
          f"holds at respond >= {t['wait']} or open >= {t['open']}\n")

    if args.line:
        cases = [(args.before, args.line)]
    else:
        suite = suites.load("demo")
        cases = []
        for conv in suite["conversations"]:
            turns = [f"{x[0]}: {x[1]}" for x in conv["turns"]]
            for i, x in enumerate(conv["turns"]):
                if len(x) == 4:
                    cases.append((turns[max(0, i - 8) : i], turns[i]))
    jev = jev_for_demo()
    print(f"{'respond':>7} {'direct':>6} {'open':>5} {'about':>5} {'ms':>5}  {'Sidechat':<8} {'Jev':<8}  line")
    for earlier, latest in cases:
        req = request(latest, earlier, args.anonymous)
        t0 = time.perf_counter()
        a = model.answer(req)
        ms = (time.perf_counter() - t0) * 1000
        decision = model.decide(a)
        j = jev.get(split(latest)[1])
        jd = "" if not j else ("respond" if j[0] >= 0.8 else "wait" if j[1] >= 0.5 else "ignore")
        print(f"{a.respond:7.2f} {a.intent['direct']:6.2f} {a.intent['open']:5.2f} {a.intent['about']:5.2f} {ms:5.0f}  "
              f"{decision:<8} {jd:<8}  {latest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
