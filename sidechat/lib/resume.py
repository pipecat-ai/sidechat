"""Picking up a job that Modal restarted on the same input, without launching its jobs twice.

Modal preempts containers and restarts the function on the same input. A job that launches others
then launched them again: round 8's and round 9's runs each trained their teachers twice, and a
restarted `train_run` trained its model twice (exp-060, logs at 10:35 and 10:44). Two guards:

- The jobs that launch others are `nonpreemptible` (CPU only; Modal charges 3x for their CPU and
  memory, a few cents for these small containers). GPU jobs cannot be, and need not be: a
  restarted GPU job is the same call, which its launcher is still waiting on.
- A launcher records each call it spawns in its status. Restarted with the same arguments while
  that status still says running, it waits on those calls that are still running or finished
  instead of spawning new ones, and skips the steps it had finished. A job that ended (done or
  failed, including a retry after an error) starts afresh, and so does any call that failed or
  was cancelled.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any


def carried(prev: dict | None, args: dict) -> dict:
    """What a restarted job keeps from its own earlier status: its start, the calls it spawned and
    the steps it finished. Nothing unless that status is a run of the same job, with the same
    arguments, that never ended."""
    if not prev or prev.get("state") != "running" or prev.get("args") != args:
        return {}
    return {
        "started_at": prev.get("started_at"),
        "calls": dict(prev.get("calls") or {}),
        "steps": dict(prev.get("steps") or {}),
        "restarts": int(prev.get("restarts") or 0) + 1,
    }


def usable(call: Any) -> bool:
    """A call worth waiting on again: still running, or finished with its result still there. One
    that failed, was cancelled (the app stopped) or whose result expired is spawned afresh."""
    try:
        call.get(timeout=0)
    except TimeoutError:  # Python's own, raised by Modal when no output is ready yet: still running
        return True
    except Exception:  # noqa: BLE001 - failed, cancelled or expired (Modal's own TimeoutError subclasses included)
        return False
    return True


class Calls:
    """Spawns Modal calls under stable keys, recording each call's id in `ids` (the status's
    "calls", saved by `save`). A key spawned before is reattached instead, if `usable`."""

    def __init__(self, ids: dict[str, str], save: Callable[[], None], find: Callable[[str], Any] | None = None) -> None:
        self.ids = ids
        self.save = save
        self.find = find

    def _known(self, key: str) -> Any:
        if key not in self.ids:
            return None
        if self.find is None:
            import modal

            self.find = modal.FunctionCall.from_id
        try:
            call = self.find(self.ids[key])
        except Exception:  # noqa: BLE001 - unknown id: spawn afresh
            return None
        return call if usable(call) else None

    def spawn(self, key: str, fn: Any, *args: Any, **kwargs: Any) -> Any:
        known = self._known(key)
        if known is not None:
            return known
        call = fn.spawn(*args, **kwargs)
        self.ids[key] = call.object_id
        self.save()
        return call
