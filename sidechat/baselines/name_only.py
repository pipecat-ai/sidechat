"""The simplest baseline: answer whenever the agent's name is said.

This is what the demo falls back to when Jev cannot be reached (`_Gate._decide`, the `error`
branch). It shows how much of each test set a name match alone gets right.
"""

from __future__ import annotations

from sidechat.baselines.jev_demo import name_pattern
from sidechat.schema import SidechatRequest


def decision(req: SidechatRequest) -> str:
    said = name_pattern(req.agent.name, req.agent.aliases).search(req.text)
    return "respond" if said else "ignore"
