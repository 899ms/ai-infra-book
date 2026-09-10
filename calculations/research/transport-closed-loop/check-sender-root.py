"""Incremental sender versus frozen replay, including advancement boundaries."""
from fractions import Fraction as F
from pathlib import Path
import copy
import hashlib
import importlib.util
import json

ROOT = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


old = load("frozen_feedback", ROOT.parent / "transport-feedback/calculate.py")
new = load("advancing_sender", ROOT / "sender.py")
start_hash = hashlib.sha256((ROOT / "sender.py").read_bytes()).hexdigest()
passed, failures = [], []


def check(name, action):
    try:
        action()
        passed.append(name)
    except Exception as exc:
        failures.append(dict(name=name, error=repr(exc)))


def compare(inputs, mode):
    expected = old.calculate(inputs)
    p = copy.deepcopy(inputs)
    if mode == "dynamic":
        p["events"] = []
    sender = new.create_sender(p)
    if mode != "dynamic":
        for event in inputs["events"]:
            sender["enqueue"](event)
    if mode == "one":
        sender["advance"](inputs["until"])
    elif mode == "chunks":
        horizon = F(str(inputs["until"]))
        for i in range(21):
            sender["advance"](horizon * i / 20)
    else:
        timestamps = sorted({F(str(e["at"])) for e in inputs["events"]})
        for at in timestamps:
            sender["advance"](at, inclusive=False)
            for event in inputs["events"]:
                if F(str(event["at"])) == at:
                    sender["enqueue"](event)
            sender["advance"](at)
        sender["advance"](inputs["until"])
    actual = sender["result"]()
    # Dynamically submitted events are external history, not constructor inputs.
    if mode == "dynamic":
        actual = {k: v for k, v in actual.items() if k != "inputs"}
        expected = {k: v for k, v in expected.items() if k != "inputs"}
    assert actual == expected, "Complete replay payload mismatch"


for name, inputs in old.scenarios().items():
    for mode in ("one", "chunks", "dynamic"):
        check(name + ":" + mode, lambda p=inputs, m=mode: compare(p, m))


def empty():
    return new.create_sender(dict(initial_max_data=1000, initial_max_stream_data={"A": 1000},
                                  until=10, events=[]))


def reject(action):
    try:
        action()
    except ValueError:
        return
    raise AssertionError("Invalid advancing-time operation accepted")


check("negative advance", lambda: reject(lambda: empty()["advance"](-1)))
check("beyond declared horizon", lambda: reject(lambda: empty()["advance"](11)))


def no_rewind():
    sender = empty()
    sender["advance"](5)
    reject(lambda: sender["advance"](4))


def no_past_enqueue():
    sender = empty()
    sender["advance"](5)
    reject(lambda: sender["enqueue"](dict(type="max_data", at=4, value=2000)))
    assert sender["result"]()["summary"]["last_processed_event"] == "0"


check("advance cannot rewind empty interval", no_rewind)
check("enqueue cannot rewind empty interval; observation is not event", no_past_enqueue)


def late_priority():
    sender = empty()
    sender["enqueue"](dict(type="sent", pn=0, at=0, sent_bytes=1200, frames=[]))
    sender["advance"](0)
    deadline = F(sender["state"]()["next_timer"]["at"])
    sender["advance"](deadline)
    reject(lambda: sender["enqueue"](dict(type="ack", at=str(deadline), ranges=[[0, 0]])))
    # The authorized probe follows the timer at the same timestamp.
    sender["enqueue"](dict(type="sent", pn=1, at=str(deadline), sent_bytes=1200, frames=[], probe=True))
    sender["advance"](deadline)
    assert sender["state"]()["bytes_in_flight"] == 2400


check("already-fired timer cannot gain retrospective ACK; probe is legal", late_priority)


def quantized_arithmetic():
    inputs = old.example()
    inputs["numeric_quantum"] = "1/1000000000"
    state = new.create_sender(inputs)
    for event in inputs["events"]:
        state["enqueue"](event)
    state["advance"](inputs["until"])
    for row in state["numeric_errors"]:
        original, rounded = F(row["original"]), F(row["rounded"])
        assert F(row["local_error"]) == rounded - original
        assert abs(rounded - original) <= F(1, 1000000000)
    assert F(state["state"]()["cwnd"]) >= 2400
    # A minimum window on a grid that does not divide it must remain legal.
    p = dict(initial_max_data=1000, initial_max_stream_data={"A": 1000}, until=1,
             initial_cwnd=2400, numeric_quantum="9/1000000", events=[])
    state = new.create_sender(p)
    state["enqueue"](dict(type="max_data", at=0, value=2000))
    state["advance"](0)
    assert F(state["state"]()["cwnd"]) >= 2400
    for value in (0, -1, 1000):
        p["numeric_quantum"] = value
        reject(lambda: new.create_sender(p))


check("quantized local errors, minimum window and invalid precision", quantized_arithmetic)
assert hashlib.sha256((ROOT / "sender.py").read_bytes()).hexdigest() == start_hash
report = dict(status="passed" if not failures else "failed", candidate_sha256=start_hash,
              passed=passed, failures=failures,
              scope="14 frozen complete payloads under whole/chunked/dynamic advancement; monotone time and same-time priority boundaries. Also checks local quantization arithmetic and minimum-window preservation; no network closure or accumulated numerical-error bound.")
(ROOT / "sender-root-check.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(dict(status=report["status"], passed=len(passed), failures=failures), indent=2))
raise SystemExit(bool(failures))
