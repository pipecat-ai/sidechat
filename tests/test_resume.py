"""A job Modal restarts on the same input waits on the calls it spawned instead of spawning again."""

from __future__ import annotations

from sidechat.lib.resume import Calls, carried, usable

ARGS = {"tag": "r9", "max_held_real": 0.002}


def test_only_a_running_job_with_the_same_args_carries_over():
    prev = {
        "state": "running",
        "args": dict(ARGS),
        "started_at": "t0",
        "calls": {"teacher/s0": "fc-1"},
        "steps": {"teacher": {"s0": "done"}},
    }
    kept = carried(prev, ARGS)
    assert kept == {
        "started_at": "t0",
        "calls": {"teacher/s0": "fc-1"},
        "steps": {"teacher": {"s0": "done"}},
        "restarts": 1,
    }
    assert carried({**prev, "restarts": 1}, ARGS)["restarts"] == 2
    assert carried(None, ARGS) == {}
    assert carried({**prev, "state": "done"}, ARGS) == {}  # a rerun after it ended starts afresh
    assert carried({**prev, "state": "failed"}, ARGS) == {}  # so does a retry after an error
    assert carried({**prev, "args": {**ARGS, "tag": "r10"}}, ARGS) == {}


class _Call:
    def __init__(self, object_id: str, outcome: object = None) -> None:
        self.object_id, self.outcome = object_id, outcome

    def get(self, timeout: float | None = None) -> object:
        if isinstance(self.outcome, BaseException):
            raise self.outcome
        return self.outcome


class _Fn:
    def __init__(self) -> None:
        self.spawned: list[tuple] = []

    def spawn(self, *args: object, **kwargs: object) -> _Call:
        self.spawned.append((args, kwargs))
        return _Call(f"fc-new-{len(self.spawned)}")


def test_usable_calls():
    assert usable(_Call("a", TimeoutError()))  # still running
    assert usable(_Call("a", {"state": "done"}))  # finished, result kept
    assert not usable(_Call("a", RuntimeError("cancelled")))


def test_a_restart_reattaches_and_spawns_only_what_is_missing():
    known = {"fc-run": _Call("fc-run", TimeoutError()), "fc-dead": _Call("fc-dead", RuntimeError("stopped"))}
    saves = []
    ids = {"teacher/s0": "fc-run", "teacher/s1": "fc-dead"}
    calls = Calls(ids, lambda: saves.append(dict(ids)), find=known.__getitem__)
    fn = _Fn()
    assert calls.spawn("teacher/s0", fn, "exp-train-s0", seed=0) is known["fc-run"]
    again = calls.spawn("teacher/s1", fn, "exp-train-s1", seed=1)  # its call was cancelled: spawn afresh
    fresh = calls.spawn("students/s0", fn, "exp-train-tt-s0", seed=0)
    assert fn.spawned == [(("exp-train-s1",), {"seed": 1}), (("exp-train-tt-s0",), {"seed": 0})]
    assert ids == {"teacher/s0": "fc-run", "teacher/s1": again.object_id, "students/s0": fresh.object_id}
    assert saves[-1] == ids  # each spawn is saved before the job waits on it
