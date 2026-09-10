"""Sender-event integration checks; no simulated receiver or pacer claim."""

from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("persistent_sender_review", ROOT / "sender.py")
sender = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sender)
checks = []


def equal(name, actual, expected):
    assert actual == expected, (name, actual, expected)
    checks.append({"case": name, "actual": str(actual), "expected": str(expected)})


def create(controller="newreno"):
    return sender.create_sender(dict(
        until=12, initial_cwnd=120000, initial_max_data=1000000,
        initial_max_stream_data={"b": 1000000}, events=[], max_ack_delay=0,
        rtt_seed=dict(latest_rtt=".1", smoothed_rtt=".1", rttvar=".025", min_rtt=".1"),
        controller={"name": controller, "pad_in_flight": True},
    ))


def sent(pn, at):
    return dict(type="sent", at=str(at), pn=pn, sent_bytes=1200,
                ack_eliciting=True, in_flight=True,
                frames=[dict(type="stream", stream="b", offset=1168 * pn, length=1168)])


def ack(pn, at):
    return dict(type="ack", at=str(at), ranges=[[pn, pn]])


x = create()
for pn in range(9):
    x["enqueue"](sent(pn, pn))
x["advance"](8)
equal("PTOs without ACK do not establish persistence", len(x["persistent_events"]), 0)
equal("PTOs do not declare packets lost", len(x["losses"]), 0)
x["enqueue"](ack(8, "8.1"))
x["advance"]("8.1")
equal("ACK establishes one episode", len(x["persistent_events"]), 1)
event = x["persistent_events"][0]
# RTT stays .1; variance becomes (3/4)*.025 = .01875.
# Threshold = 3*(.1+4*.01875) = .525 = 21/40 seconds.
equal("post ACK threshold", F(event["evidence"]["threshold_duration"]), F(21, 40))
equal("all loss declarations consumed", event["consumed_loss_declarations"], list(range(8)))
equal("actual minimum window action", F(x["state"]()["cwnd"]), F(2400))
x["enqueue"](ack(0, "8.2"))
x["advance"]("8.2")
equal("late ACK changes history without a second action", len(x["persistent_events"]), 1)
equal("late ACK does not release flight twice", x["state"]()["bytes_in_flight"], 0)
for e in (sent(9, "8.3"), ack(9, "8.4"), sent(10, "8.5"), sent(11, "8.6"), ack(11, "8.75")):
    x["enqueue"](e)
x["advance"]("8.75")
equal("new separate short loss cannot reuse old long span", len(x["persistent_events"]), 1)
equal("separate loss remains unconsumed", sorted(x["unconsumed_losses"]), [10])

# ACK PN2 leaves PN1 not yet past the 9/8 RTT loss threshold. The loss
# timer then discovers PN1, but the minimum-window action waits for ACK.
y = create()
for e in (sent(0, 0), sent(1, 1), sent(2, "1.001"), ack(2, "1.101")):
    y["enqueue"](e)
y["advance"]("1.101")
equal("first ACK only loses older endpoint", [e["pn"] for e in y["losses"]], [0])
equal("one lost endpoint is insufficient", len(y["persistent_events"]), 0)
y["advance"]("1.15")
equal("loss timer discovers second endpoint", [e["pn"] for e in y["losses"]], [0, 1])
equal("loss timer alone does not perform action", len(y["persistent_events"]), 0)
y["enqueue"](ack(2, "1.2"))
y["advance"]("1.2")
equal("next actual ACK consumes deferred evidence", len(y["persistent_events"]), 1)
equal("deferred action sets minimum window", F(y["state"]()["cwnd"]), F(2400))
equal("deferred loss declarations consumed once", sorted(y["unconsumed_losses"]), [])

z = create("cubic_hystart")
for pn in range(9):
    z["enqueue"](sent(pn, pn))
z["enqueue"](ack(8, "8.1"))
z["advance"]("8.1")
equal("CUBIC persistent action occurs once", len(z["persistent_events"]), 1)
equal("CUBIC persistent overrides ordinary loss window", F(z["state"]()["cwnd"]), F(2400))
z["enqueue"](ack(0, "8.2"))
z["advance"]("8.2")
equal("CUBIC late ACK does not repeat persistent action", len(z["persistent_events"]), 1)
equal("CUBIC late ACK does not grow minimum window", F(z["state"]()["cwnd"]), F(2400))

result = {
    "scope": "NewReno sender replay: persistent action, late ACK deduplication, separate short loss and deferred loss-timer evidence; CUBIC minimum action and late ACK; not full network or BBR acceptance",
    "passed": len(checks),
    "source_hashes": {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in ("sender.py", "persistent_congestion.py", "cubic_adapter.py", Path(__file__).name)},
    "checks": checks,
    "immediate_events": x["persistent_events"],
    "deferred_events": y["persistent_events"],
    "cubic_events": z["persistent_events"],
}
(ROOT / "persistent-sender-root-check.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({"passed": len(checks), "source_hashes": result["source_hashes"]}))
