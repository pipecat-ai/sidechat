"""The three speaker-label conditions every set is scored in (scorecard 0.1, DECISIONS.md SD-14).

    named      speakers by name, with the list of people present: what the daily-audience demo gives
    anonymous  speakers as "Speaker 1", "Speaker 2", ... in order of first appearance, and no list of
               people: what a diarized transcript usually gives. The headline condition
    none       no speaker labels and no list of people: an undiarized transcript

Only the labels change. The words do not: people still call each other by name in what they say,
and nobody says "Speaker 2" aloud. The agent's own turns stay marked as the agent's, because the
system always knows what it said itself.
"""

from __future__ import annotations

CONDITIONS = ("named", "anonymous", "none")


def _anonymise(request: dict) -> dict:
    order: dict[str, str] = {}

    def label(name: str | None) -> str | None:
        if name is None:
            return None
        if name not in order:
            order[name] = f"Speaker {len(order) + 1}"
        return order[name]

    history = []
    for t in request["history"]:
        history.append(t if t.get("agent") else {**t, "speaker": label(t.get("speaker"))})
    return {**request, "history": history, "speaker": label(request.get("speaker")), "people": None}


def _strip(request: dict) -> dict:
    history = [t if t.get("agent") else {**t, "speaker": None} for t in request["history"]]
    return {**request, "history": history, "speaker": None, "people": None}


def apply(row: dict, condition: str) -> dict:
    """A copy of a record (as a dict) in the given condition.

    Its `set` gets the condition as a suffix (`pilot-0.4@anonymous`), so answers and scores for
    different conditions never mix. Names in `label.to_people` are dropped outside `named`: with
    anonymous labels the model cannot know which speaker a called name belongs to.
    """
    if condition not in CONDITIONS:
        raise ValueError(f"unknown condition {condition!r}; choose from {CONDITIONS}")
    if condition == "named":
        return row
    request = _anonymise(row["request"]) if condition == "anonymous" else _strip(row["request"])
    label = {**row["label"], "to_people": []}
    suffix = f"@{condition}"
    row_id = row["row_id"]
    row_id = (
        row_id.replace(row["set"], row["set"] + suffix, 1) if row_id.startswith(row["set"] + "/") else row_id + suffix
    )
    return {
        **row,
        "row_id": row_id,
        "set": row["set"] + suffix,
        "request": request,
        "label": label,
        "tags": {**row["tags"], "condition": condition},
    }


def people_only(row: dict) -> dict:
    """A training view, not a scoring condition: the row as a transcript of the people's side only.
    The agent's turns leave the history, and whether the line was said over the agent is no longer
    known. The kind's label assumes the agent's turns are visible, so such a row is trained on the
    teacher's probabilities alone (`train(people_only=...)`)."""
    req = dict(row["request"])
    req["history"] = [t for t in req["history"] if not t.get("agent")]
    if req.get("facts"):
        req["facts"] = {**req["facts"], "over_agent": None}
    return {**row, "request": req, "tags": {**row["tags"], "people_only": "1"}}
