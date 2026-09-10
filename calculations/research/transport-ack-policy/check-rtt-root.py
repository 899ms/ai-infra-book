"""Hand arithmetic for actual network ACK delay and sender RTT updates."""
import copy
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import calculate

ROOT = Path(__file__).resolve().parent


def hashes():
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for name in ("calculate.py", "receiver.py", "dependencies.lock.json", "sources.lock.json")}


initial = hashes()
base = json.loads((ROOT / "scenarios.json").read_text())["tail-deadline"]
checks, cases = [], {}


def equal(label, actual, expected):
    assert actual == expected, (label, actual, expected)
    checks.append({"case": label, "actual": str(actual), "expected": str(expected)})


for label in ("prior_sample", "first_sample", "reverse_busy"):
    inputs = copy.deepcopy(base)
    if label == "first_sample":
        inputs["sender"].pop("rtt_seed")
        inputs["sender"]["initial_rtt"] = 10  # Estimate keeps PTO after the ACK.
    if label == "reverse_busy":
        inputs.update(response_bytes=1168, until=100)
        inputs["sender"]["rtt_seed"] = dict(latest_rtt=4, smoothed_rtt=4, rttvar=20, min_rtt=1)
    result = calculate.calculate(inputs)
    cases[label] = result
    state = result["final_states"]["up"]
    acks = [t for t in result["transmissions"] if t["direction"] == "down" and t["kind"] == "ack"]
    equal(label + " one actual ACK", len(acks), 1)
    equal(label + " no phantom loss", len(result["losses"]["up"]), 0)
    equal(label + " no remaining flight", state["bytes_in_flight"], 0)
    snapshot = acks[0]["ack_snapshot"]
    expected_sample = {
        "prior_sample": dict(at="9/2", pn=0, raw="9/2", adjusted="4", smoothed="4", rttvar="3/2"),
        "first_sample": dict(at="9/2", pn=0, raw="9/2", adjusted="9/2", smoothed="9/2", rttvar="9/4"),
        "reverse_busy": dict(at="399/23", pn=0, raw="399/23", adjusted="775/46", smoothed="2063/368", rttvar="3351/184"),
    }[label]
    equal(label + " exported actual RTT record", result["rtt_samples"]["up"], [expected_sample])
    if label != "reverse_busy":
        equal(label + " ACK arrives", F(acks[0]["arrival"]), F(9, 2))
        equal(label + " wire ACK delay", F(snapshot["decoded_delay"]), F(1, 2))
        equal(label + " raw latest RTT", F(state["latest_rtt"]), F(9, 2))
    if label == "prior_sample":
        # Adjusted RTT = 4.5-.5 =4; SRTT remains4; variance=.75*2=1.5.
        equal("valid prior sample allows delay deduction", F(state["smoothed_rtt"]), F(4))
        equal("variance uses previous SRTT", F(state["rttvar"]), F(3, 2))
    if label == "first_sample":
        equal("first RTT does not deduct receiver delay", F(state["smoothed_rtt"]), F(9, 2))
        equal("first variance is half raw RTT", F(state["rttvar"]), F(9, 4))
        equal("first minRTT is observed raw RTT", F(state["min_rtt"]), F(9, 2))
    if label == "reverse_busy":
        # Response starts at2, occupies307/23 seconds. ACK then occupies1
        # second and propagates1: sender's raw RTT is399/23 seconds.
        equal("busy ACK starts after response serialization", F(acks[0]["send_start"]), F(353, 23))
        equal("busy raw receiver delay", F(snapshot["raw_delay"]), F(307, 23))
        equal("busy decoded delay at eight microsecond tick", F(snapshot["decoded_delay"]), F(834239, 62500))
        equal("busy deadline violation is visible", snapshot["exceeds_max_delay"], True)
        equal("busy raw RTT includes true queue wait", F(state["latest_rtt"]), F(399, 23))
        # Only max_ack_delay=.5 can be subtracted, not all 13.347824s.
        # Adjusted=775/46; SRTT=7/8*4+1/8*775/46=2063/368.
        equal("sender bounds delay subtraction", F(state["smoothed_rtt"]), F(2063, 368))
        equal("bounded sample variance", F(state["rttvar"]), F(3351, 184))

assert hashes() == initial
report = {"status": "passed", "checks": checks, "cases": cases,
          "source_hashes": initial, "passed": len(checks),
          "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
          "scope": "Three actual network cases, first/prior sample and queued ACK deadline violation; not large-workload acceptance"}
(ROOT / "rtt-root-check.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"passed": len(checks), "source_hashes": initial}))
