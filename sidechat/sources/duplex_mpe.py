"""Duplex-MPE: several people and an assistant, "Aria", with a label on every turn.

Source: https://huggingface.co/datasets/ChengqianMa/Duplex-MPE (CC BY 4.0). Only the two text
manifests are used, not the audio. Held out: never trained on.

The benchmark's event types, from its card:

    T     the scenario's one unresolved request to Aria. Named in the explicit scenario,
          identified only by context in the implicit one.
    N4_Q  a question to Aria that the speaker takes back in the next turn.
    N4_R  that next turn ("never mind, I paid by card there Tuesday").
    N1    mentions Aria without asking it anything.
    N2    said to another person or another device ("Hey Siri, ...").
    N3    no designated addressee, mostly thinking aloud.

Read one utterance at a time, T and N4_Q are for the agent and everything else is not. The
manifests hold the people's turns only, so Aria's replies are not in the history.
"""

from __future__ import annotations

from sidechat.schema import Agent, SidechatLabel, SidechatRecord, SidechatRequest, Turn, window

SET = "duplex-mpe-0.1"
REPO = "ChengqianMa/Duplex-MPE"
REVISION = "6d5f59fab1237c14ee8229ea36f111b7423b0fe6"
FILES = {"explicit": "manifests/explicit.json", "implicit": "manifests/implicit.json"}
LICENCE = "CC BY 4.0"
USE = "held-out benchmark; never train on it"

AGENT = Agent(name="Aria", role="voice assistant in the room")
FOR_AGENT = ("T", "N4_Q")
_TO = {"other_human": "person", "device": "device", "none": "nobody", "animal": "nobody", "aria": "agent"}


def label(event: str, addressee: str) -> SidechatLabel:
    if event in FOR_AGENT:
        return SidechatLabel(to="agent", intent="direct", expect="respond", respond=1.0, source="benchmark")
    to = _TO.get(addressee, "unknown")
    if to == "agent":  # a handful of rows are marked for Aria under a silent event; see `conflict`
        to = "unknown"
    intent = "about" if event == "N1" else "other"
    return SidechatLabel(to=to, intent=intent, expect="ignore", respond=0.0, source="benchmark")


def convert(scenarios: list[dict]) -> list[dict]:
    """One record per human turn."""
    rows = []
    for sc in scenarios:
        people = [chr(ord("A") + i) for i in range(int(sc["n_speakers"]))]
        turns = [Turn(speaker=t["speaker"], text=t["text"]) for t in sc["turns"]]
        for i, t in enumerate(sc["turns"]):
            event, addressee = t["event_type"], t["addressee"]
            conflict = (event in FOR_AGENT) != (addressee == "aria")
            rec = SidechatRecord(
                row_id=f"{SET}/{sc['scenario_id']}/{i}",
                set=SET,
                conv_id=sc["pair_id"],  # the two scenarios of a pair stay together in any split
                turn_index=i,
                request=SidechatRequest(
                    agent=AGENT, text=t["text"], speaker=t["speaker"], history=window(turns, i), people=people
                ),
                label=label(event, addressee),
                tags={
                    "condition": sc["addressing"],
                    "event": event,
                    "addressee": addressee,
                    "speech_act": t["speech_act"],
                    "after_trigger": "1" if i > sc["trigger_index"] else "0",
                    "conflict": "1" if conflict else "0",
                },
            )
            rows.append(rec.model_dump(mode="json"))
    return rows
