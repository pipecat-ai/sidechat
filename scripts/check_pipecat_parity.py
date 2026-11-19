"""Check that Pipecat's port of Sidechat builds the same inputs and reads the same answers as this repo.

Run with the Python of a Pipecat checkout that has `pipecat.models.labs.side_chat`:

    ~/Sites/pipecat/.venv/bin/python scripts/check_pipecat_parity.py models/side-r3-ettin-150m-s0

The folder is the export, laid out as `pipecat-ai/sidechat` on Hugging Face is, so both runtimes
load the same files.

The lines are every hand-written suite in all three speaker conditions, plus variants of each that
exercise aliases, people's names, speech over the agent and a history long enough to be truncated.
For each line it compares the encoder text, the line's offset and the numbers exactly, then the
model's probabilities and decisions for fp32 and int8. Exits non-zero on any difference.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from pipecat.models.labs.side_chat.conversation import (
    SideChatAgent,
    SideChatLine,
    SideChatTurn,
    encoder_text,
    numbers,
)
from pipecat.models.labs.side_chat.model import SideChatModel

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


def port(req: SidechatRequest) -> tuple[SideChatAgent, SideChatLine]:
    agent = SideChatAgent(name=req.agent.name, aliases=tuple(req.agent.aliases), role=req.agent.role)
    line = SideChatLine(
        text=req.text,
        speaker=req.speaker,
        history=[SideChatTurn(text=t.text, speaker=t.speaker, agent=t.agent) for t in req.history],
        people=req.people,
        over_agent=req.facts.over_agent if req.facts else None,
    )
    return agent, line


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("model_dir", type=pathlib.Path, help="the export, as sidechat.pipeline.fetch saves it")
    args = ap.parse_args()

    reqs = requests()
    failures = 0
    truncated = 0
    for req in reqs:
        agent, line = port(req)
        if encoder_text(agent, line) != features.text(req):
            failures += 1
            print(f"text differs: {req.text!r}")
        if numbers(agent, line) != features.numbers(req):
            failures += 1
            print(f"numbers differ: {req.text!r}")
    print(f"inputs: {len(reqs)} lines, {failures} differ")

    for precision in ("fp32", "int8"):
        ours = load(args.model_dir, threads=4, int8=precision == "int8")
        theirs = SideChatModel(args.model_dir, precision=precision, threads=4)
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
            if precision == "fp32" and len(theirs._tokenizer.encode(features.text(req)[0]).ids) >= 320:
                truncated += 1
        # This repo rounds to 6 places; the port doesn't.
        ok = worst <= 1e-5 and not disagree
        failures += not ok
        print(f"{precision}: {len(reqs)} lines, largest difference {worst:.2e}, {disagree} decisions differ")
    print(f"lines at the token limit: {truncated}")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
