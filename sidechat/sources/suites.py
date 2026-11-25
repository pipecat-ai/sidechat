"""Hand-written suites in `data/suites/*.yaml`: short conversations with a label on every line.

A suite file:

    suite: side-pilot-0.1
    about: one line on what this suite is
    label_source: author
    agent: {name: Atlas, role: AI assistant on the call}
    conversations:
      - id: standup-01
        setting: work standup
        people: [Jon, Sam, Priya]
        turns:
          - [Jon, "Sam, where are we on the release?", "P:Sam", question_to_person]
          - [Atlas, "It's Canberra."]            # the agent's own line: history only
          - [Sam, "No idea."]                    # two items: context only, not scored

A turn is `[speaker, text, code, kind]`. `kind` names the slice the line belongs to. A turn with
only `[speaker, text]` is context for the lines after it and is not scored. The codes:

    D    said to the agent                              -> answer now
    D~   said to the agent, a reply is optional         -> graded (thanks, "that's enough")
    I    asks for the agent without speaking to it      -> answer now ("Can the assistant ...?")
    I~   invites the agent without asking               -> graded ("Maybe Atlas knows.")
    O    open to anyone, the agent could take it        -> hold, answer if nobody else does
    A    mentions the agent, wants nothing from it      -> stay quiet
    P    for a person (P:Sam names them)                -> stay quiet
    G    for the people as a group                      -> stay quiet
    N    for nobody: thinking aloud, an acknowledgement -> stay quiet
    X    for another device                             -> stay quiet
    ?    no expectation recorded                        -> graded

Graded lines carry no expected decision and are left out of decision accuracy.
"""

from __future__ import annotations

import pathlib

from sidechat.schema import Agent, SidechatLabel, SidechatRecord, SidechatRequest, Turn, window

SUITES_DIR = pathlib.Path(__file__).resolve().parents[2] / "data" / "suites"
SUITE_FILES = {
    "demo": "demo-lines-0.1.yaml",
    "pilot": "pilot-0.1.yaml",
    "pilot-0.2": "pilot-0.2.yaml",
    "pilot-0.3": "pilot-0.3.yaml",
    "pilot-0.4": "pilot-0.4.yaml",
}

# code -> (to, intent, expect, respond)
CODES: dict[str, tuple[str, str | None, str | None, float | None]] = {
    "D": ("agent", "direct", "respond", 1.0),
    "D~": ("agent", "direct", None, 0.5),
    "I": ("agent", "indirect", "respond", 1.0),
    "I~": ("group", "indirect", None, 0.5),
    "O": ("group", "open", "wait", 0.5),
    "A": ("group", "about", "ignore", 0.0),
    "P": ("person", "other", "ignore", 0.0),
    "G": ("group", "other", "ignore", 0.0),
    "N": ("nobody", "other", "ignore", 0.0),
    "X": ("device", "other", "ignore", 0.0),
    "?": ("unknown", None, None, None),
}


def parse_code(code: str, source: str) -> SidechatLabel:
    base, _, names = code.partition(":")
    if base not in CODES:
        raise ValueError(f"unknown label code {code!r}")
    to, intent, expect, respond = CODES[base]
    people = [n.strip() for n in names.split(",") if n.strip()]
    if base == "A" and people:
        to = "person"  # said about the agent, to a named person
    return SidechatLabel(to=to, to_people=people, intent=intent, expect=expect, respond=respond, source=source)


def code_of(label: SidechatLabel) -> str:
    """The short code a guide-derived label corresponds to, so both kinds of suite slice alike."""
    if label.intent is None:
        return "U"
    if label.intent == "direct":
        return "D" if label.expect else "D~"
    if label.intent == "indirect":
        return "I" if label.expect else "I~"
    if label.intent == "open":
        return "O"
    if label.intent == "about":
        return "A"
    return {"person": "P", "group": "G", "nobody": "N", "device": "X"}.get(label.to, "?")


def _parse_turn(raw: list, conv_id: str, i: int, by_guide: bool) -> tuple[str | None, str | None, list[str]]:
    """(code, kind, people) for a labelled turn, or (None, None, []) for a context-only one."""
    if len(raw) == 2:
        return None, None, []
    if by_guide:
        if len(raw) == 3:
            return None, raw[2], []
        if len(raw) == 4 and isinstance(raw[3], list):
            return None, raw[2], [str(p) for p in raw[3]]
        raise ValueError(
            f"{conv_id} turn {i}: expected [speaker, text], [speaker, text, kind] or [..., kind, [people]]"
        )
    if len(raw) == 4:
        return raw[2], raw[3], []
    raise ValueError(f"{conv_id} turn {i}: expected [speaker, text] or [speaker, text, code, kind]")


def convert(suite: dict) -> list[dict]:
    """One record per labelled line.

    A suite with `label_from: guide` names each line's kind, and its label comes from
    `sidechat/guide.py`. Otherwise each line carries a hand-written code.
    """
    from sidechat import guide

    name = suite["suite"]
    by_guide = suite.get("label_from") == "guide"
    source = "guide" if by_guide else suite.get("label_source", "author")
    default_agent = suite.get("agent", {"name": "Atlas"})
    rows = []
    for conv in suite["conversations"]:
        agent = Agent(**conv.get("agent", default_agent))
        turns, labelled = [], []
        for i, raw in enumerate(conv["turns"]):
            speaker, text = raw[0], raw[1]
            is_agent = speaker == agent.name
            turns.append(Turn(speaker=speaker, text=text, agent=is_agent))
            code, kind, named = _parse_turn(raw, conv["id"], i, by_guide)
            if kind is None:
                continue  # context only
            if is_agent:
                raise ValueError(f"{conv['id']} turn {i}: the agent's own line takes no label")
            labelled.append((i, code, kind, named))
        people = conv.get("people") or list(dict.fromkeys(t.speaker for t in turns if not t.agent))
        for i, code, kind, named in labelled:
            if by_guide:
                label = guide.label_for(kind, named)
                tags = {"kind": kind, "rule": guide.KINDS[kind].rule, "code": code_of(label)}
            else:
                label = parse_code(code, source)
                tags = {"kind": kind, "code": code.partition(":")[0]}
            rec = SidechatRecord(
                row_id=f"{name}/{conv['id']}/{i}",
                set=name,
                conv_id=conv["id"],
                turn_index=i,
                request=SidechatRequest(
                    agent=agent, text=turns[i].text, speaker=turns[i].speaker, history=window(turns, i), people=people
                ),
                label=label,
                tags={**tags, "setting": conv.get("setting", ""), "style": conv.get("style", "clean")},
            )
            rows.append(rec.model_dump(mode="json"))
    return rows


def load(which: str) -> dict:
    import yaml

    path = SUITES_DIR / SUITE_FILES[which]
    return yaml.safe_load(path.read_text())
