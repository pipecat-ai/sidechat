"""Social AI Ambient Bench: typed group chats where each message is RESPOND or SILENT.

Source: https://huggingface.co/datasets/text-ai/social-ai-ambient-bench (Apache-2.0).

TEST ONLY. The dataset carries a notice that it must never appear in a training corpus. Nothing
converted here may be used for training, and the converted rows are never committed to git.

Its policy is wider than Sidechat's: the assistant, "alfi", is expected to offer help that nobody
asked for (a fact correction, a suggestion). So RESPOND here means "should contribute", which a
model that speaks only when spoken to will miss by design. The useful numbers for Sidechat are how
often it stays quiet on SILENT messages, and the categories where alfi is actually asked.
"""

from __future__ import annotations

from sidechat.schema import Agent, SidechatLabel, SidechatRecord, SidechatRequest, Turn, window

SET = "ambient-bench-0.1"
REPO = "text-ai/social-ai-ambient-bench"
REVISION = "5efda0b267d6bd5ecae74cbe1141a66f64495661"
FILES = {"test": "data/test.jsonl", "leaderboard": "results/baseline_results.json"}
LICENCE = "Apache-2.0"
USE = "test only; the dataset forbids training on it"

AGENT = Agent(name="alfi", role="AI assistant in the group chat")


def convert(scenarios: list[dict]) -> list[dict]:
    """One record per message. The benchmark's label is kept in `tags["bench"]`."""
    rows = []
    for sc in scenarios:
        people = list(dict.fromkeys(t["speaker"] for t in sc["turns"]))
        turns = [Turn(speaker=t["speaker"], text=t["message"]) for t in sc["turns"]]
        for i, t in enumerate(sc["turns"]):
            speak = t["expected_output"] == "RESPOND"
            rec = SidechatRecord(
                row_id=f"{SET}/{sc['id']}/{i}",
                set=SET,
                conv_id=sc["id"],
                turn_index=i,
                request=SidechatRequest(
                    agent=AGENT, text=t["message"], speaker=t["speaker"], history=window(turns, i), people=people
                ),
                # RESPOND does not say whether the message was for alfi, so `to` and `intent` stay open,
                # and answering now or after a silence both count as speaking.
                label=SidechatLabel(
                    to="unknown",
                    expect=None if speak else "ignore",
                    respond=1.0 if speak else 0.0,
                    source="benchmark",
                ),
                tags={"bench": t["expected_output"], "category": sc["category"]},
            )
            rows.append(rec.model_dump(mode="json"))
    return rows
