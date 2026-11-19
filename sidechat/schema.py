"""Sidechat request, answer and labelled record: schema `sidechat-0.1`.

One request is one utterance in a conversation between several people and one agent. The answer
says who the utterance was for and whether the agent should speak. See PLAN.md section 2.

A record is a request with its label and where it came from. Every data source is converted to
records (`sidechat/sources/`), so scoring and training read one format.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

SCHEMA_VERSION = "sidechat-0.1"
MAX_HISTORY = 8

Intent = Literal["direct", "indirect", "open", "about", "other"]
INTENTS: tuple[Intent, ...] = ("direct", "indirect", "open", "about", "other")

# Who the utterance was for.
To = Literal["agent", "person", "group", "device", "nobody", "unknown"]

# What the agent should do, in the three outcomes the daily-audience gate has:
# answer now, hold the answer and give it if nobody else speaks, or stay quiet.
Expect = Literal["respond", "wait", "ignore"]


class Agent(BaseModel):
    """The agent's card: what people call it."""

    name: str
    aliases: list[str] = Field(default_factory=list)  # other spellings, including speech-to-text ones
    role: str | None = None  # one line, e.g. "AI assistant on the call"


class Turn(BaseModel):
    """One earlier utterance."""

    speaker: str | None = None  # None when the transcript is not diarized
    text: str
    agent: bool = False  # the agent said this


class Facts(BaseModel):
    """Optional facts the application may know. Unknown is None."""

    alone: bool | None = None  # one person present, so there is nobody else to mean
    over_agent: bool | None = None  # the utterance was spoken while the agent was speaking


class SidechatRequest(BaseModel):
    """One line to judge, with what came before it.

    `speaker` and each turn's speaker are whatever the diarizer gives: a name, or more often an
    anonymous label such as "Speaker 1" that nobody says aloud. People's names are weak evidence;
    the agent's own name is the reliable one (DECISIONS.md SD-14). The model reads the history as
    roles relative to `speaker` (`sidechat/context.py`), so names and labels work the same.
    """

    agent: Agent
    text: str
    speaker: str | None = None  # a name or a diarization label; None when not diarized
    history: list[Turn] = Field(default_factory=list)  # oldest first, at most MAX_HISTORY
    people: list[str] | None = None  # names or labels of the people present; usually absent
    facts: Facts | None = None

    @field_validator("history")
    @classmethod
    def _history_fits(cls, v: list[Turn]) -> list[Turn]:
        if len(v) > MAX_HISTORY:
            raise ValueError(f"history holds {len(v)} turns, the limit is {MAX_HISTORY}")
        return v


class SidechatAnswer(BaseModel):
    """The model's answer. Every number is a probability."""

    intent: dict[Intent, float]  # sums to 1
    respond: float  # the agent should speak now
    unclear: float = 0.0  # the evidence fits the agent and someone else equally
    people: dict[str, float] = Field(default_factory=dict)  # per person present: the line was for them

    @model_validator(mode="after")
    def _probabilities(self) -> SidechatAnswer:
        if set(self.intent) != set(INTENTS):
            raise ValueError(f"intent needs exactly {INTENTS}")
        numbers = [*self.intent.values(), self.respond, self.unclear, *self.people.values()]
        if any(not 0.0 <= p <= 1.0 for p in numbers):
            raise ValueError("probabilities must be between 0 and 1")
        if abs(sum(self.intent.values()) - 1.0) > 1e-3:
            raise ValueError("intent probabilities must sum to 1")
        return self

    @property
    def addressed(self) -> float:
        """The demo's "said to the bot?" number."""
        return self.intent["direct"] + self.intent["indirect"]

    @property
    def open_question(self) -> float:
        """The demo's "open question for anyone?" number."""
        return self.intent["open"]


class SidechatLabel(BaseModel):
    """What is known about one utterance. Fields a source cannot supply stay None."""

    to: To
    to_people: list[str] = Field(default_factory=list)  # names, when `to` is "person"
    intent: Intent | None = None
    expect: Expect | None = None  # None: graded, either behaviour is acceptable
    respond: float | None = None  # target for the `respond` head, 0 to 1
    unclear: bool = False
    source: str  # "construction", "benchmark", "author", "committee", "human"


class SidechatRecord(BaseModel):
    schema_version: Literal["sidechat-0.1"] = SCHEMA_VERSION
    row_id: str
    set: str  # the dataset this row belongs to, e.g. "duplex-mpe-0.1"
    conv_id: str  # rows of one conversation share this; splits never cut a conversation
    turn_index: int
    request: SidechatRequest
    label: SidechatLabel
    tags: dict[str, str] = Field(default_factory=dict)  # slices: kind, condition, category, ...


def window(turns: list[Turn], index: int, limit: int = MAX_HISTORY) -> list[Turn]:
    """The history for the utterance at `index`: up to `limit` turns before it."""
    return turns[max(0, index - limit) : index]
