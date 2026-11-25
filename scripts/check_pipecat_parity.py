"""Check that Pipecat's port of Sidechat builds the same inputs and reads the same answers as this repo.

Run with the Python of a Pipecat checkout that has `pipecat.classifiers.sidechat`:

    <pipecat checkout>/.venv/bin/python scripts/check_pipecat_parity.py --variant small

It downloads the release from Hugging Face the way Pipecat does (`--revision`, by default the one
Pipecat pins; `--variant base` is the default build at the repo's root, `small` the two-tower build
in `agent-1x/`), and both runtimes load those files. `--model-dir` checks a local export instead.

The lines are every hand-written suite in all three speaker conditions, plus variants of each that
exercise aliases, people's names, speech over the agent and a history long enough to be truncated.
For each line it compares the model's texts and the numbers exactly, then the model's
probabilities and decisions for fp32 and int8. Exits non-zero on any difference.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipecat.classifiers.sidechat.conversation import (
    SidechatAgent,
    SidechatLine,
    SidechatTurn,
    encoder_text,
    line_text,
    numbers,
    turns_text,
)
from pipecat.classifiers.sidechat.model import SIDECHAT_REVISION, PipecatSidechatModel

from sidechat import conditions
from sidechat.runtime import load
from sidechat.schema import SidechatRequest
from sidechat.sources import suites
from sidechat.train import features

SUITES = tuple(suites.SUITE_FILES)
FILLER = " and then we went over the numbers for the third quarter again, line by line"


def requests() -> list[SidechatRequest]:
    out = []
    for name in SUITES:
        for row in suites.convert(suites.load(name)):
            for condition in conditions.CONDITIONS:
                out.append(SidechatRequest.model_validate(conditions.apply(row, condition)["request"]))
    variants = []
    for i, req in enumerate(out):
        if i % 3 == 0:
            agent = req.agent.model_copy(update={"aliases": ["at last", "the bot"]})
            variants.append(req.model_copy(update={"agent": agent}))
        if i % 3 == 1:
            variants.append(req.model_copy(update={"facts": {"over_agent": True}, "people": ["Sam", "Priya"]}))
        if i % 5 == 0 and req.history:
            long = [t.model_copy(update={"text": t.text + FILLER * 3}) for t in req.history]
            variants.append(req.model_copy(update={"history": long}))
    return [SidechatRequest.model_validate(r.model_dump()) for r in out + variants]


def port(req: SidechatRequest) -> tuple[SidechatAgent, SidechatLine]:
    agent = SidechatAgent(name=req.agent.name, aliases=tuple(req.agent.aliases), role=req.agent.role)
    line = SidechatLine(
        text=req.text,
        speaker=req.speaker,
        history=[SidechatTurn(text=t.text, speaker=t.speaker, agent=t.agent) for t in req.history],
        people=req.people,
        over_agent=req.facts.over_agent if req.facts else None,
    )
    return agent, line


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--variant", choices=("base", "small"), default="small")
    ap.add_argument("--revision", default=SIDECHAT_REVISION, help="the release on Hugging Face")
    ap.add_argument("--model-dir", type=pathlib.Path, help="a local export, instead of downloading one")
    args = ap.parse_args()

    reqs = requests()
    failures = 0
    truncated = 0
    for precision in ("fp32", "int8"):
        if args.model_dir:
            theirs = PipecatSidechatModel(args.model_dir, precision=precision, threads=4)
            folder = args.model_dir
        else:
            theirs = PipecatSidechatModel.download(
                revision=args.revision, variant=args.variant, precision=precision, threads=4
            )
            folder = pathlib.Path(theirs._session._model_path).parent
        ours = load(folder, threads=4, int8=precision == "int8")
        two_tower = theirs.prepares
        tokenizer = theirs._tokenizer

        def count(text: str, tokenizer=tokenizer) -> int:
            return len(tokenizer.encode(text).ids)

        if precision == "fp32":
            differ = 0
            for req in reqs:
                agent, line = port(req)
                if two_tower:
                    limit = theirs.config["ctx_len"]
                    same = turns_text(agent, line, limit, count) == features.context_fitted(req, limit, count)
                    same = same and line_text(agent, line) == features.line_text(req)
                    truncated += count(features.context_text(req)) > limit
                else:
                    same = encoder_text(agent, line) == features.text(req)
                    truncated += count(features.text(req)[0]) >= theirs.config["max_len"]
                if not same:
                    differ += 1
                    print(f"text differs: {req.text!r}")
                if numbers(agent, line) != features.numbers(req):
                    differ += 1
                    print(f"numbers differ: {req.text!r}")
            failures += differ
            print(f"{folder}")
            print(f"inputs: {len(reqs)} lines, {differ} differ")

        worst = 0.0
        disagree = 0
        for req in reqs:
            agent, line = port(req)
            a = ours.answer(req)
            b = theirs.answer(agent, line)
            diffs = [abs(a.respond - b.respond), abs(a.unclear - b.unclear)]
            diffs += [abs(a.intent[k] - b.intent[k]) for k in a.intent]
            worst = max(worst, *diffs)
            mine = ours.decide(a).replace("wait", "hold")
            if mine != theirs.decide(b):
                disagree += 1
                print(f"{precision} decision differs: {req.text!r} {mine} {theirs.decide(b)}")
        # This repo rounds to 6 places; the port doesn't.
        ok = worst <= 1e-5 and not disagree
        failures += not ok
        print(f"{precision}: {len(reqs)} lines, largest difference {worst:.2e}, {disagree} decisions differ")
    print(f"lines at the token limit: {truncated}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
