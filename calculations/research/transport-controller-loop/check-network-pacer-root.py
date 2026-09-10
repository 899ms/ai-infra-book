"""Hand-derived padded NewReno pacing and physical serializer examples."""

from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("network_pacing_review", ROOT / "calculate.py")
network = importlib.util.module_from_spec(spec)
spec.loader.exec_module(network)


def inputs():
    return {
        "upload_bytes": 3504,
        "response_bytes": 32,
        "model_seconds": 0,
        "until": 8,
        "links": {
            d: {"rate_bps": 1000000000, "propagation": 1}
            for d in ("up", "down")
        },
        "sender": {
            "initial_cwnd": 12000,
            "rtt_seed": {"latest_rtt": 4, "smoothed_rtt": 4, "rttvar": 2, "min_rtt": 4},
        },
        "controller": {"name": "newreno"},
        "pad_in_flight": True,
    }


checks = []


def equal(name, actual, expected):
    assert actual == expected, (name, actual, expected)
    checks.append({"case": name, "actual": str(actual), "expected": str(expected)})


p = inputs()
r = network.calculate(p)
up = [t for t in r["transmissions"] if t["direction"] == "up" and t["kind"] == "data"]
down_acks = [t for t in r["transmissions"] if t["direction"] == "down" and t["kind"] == "ack"]
response = [t for t in r["transmissions"] if t["direction"] == "down" and t["kind"] == "data"]

# The first ACK cannot return before 2 seconds. Initial rate is
# (5/4)*12000/4 = 3750 QUIC B/s, so the gap is 1200/3750 = 8/25 s.
equal("three pre-feedback paced starts", [F(t["send_start"]) for t in up], [F(0), F(8, 25), F(16, 25)])
data_wire_time = F(1228 * 8, 1000000000)
ack_wire_time = F(92 * 8, 1000000000)
arrivals = [s + data_wire_time + 1 for s in (F(0), F(8, 25), F(16, 25))]
equal("physical data serialization and propagation", [F(t["received_at"]) for t in up], arrivals)
equal("ACKs start at receiver arrival", [F(t["send_start"]) for t in down_acks], arrivals)
# The final upload ACK gets the serializer first. ACKs do not leave paced
# debt, so the response starts immediately after that 92-byte wire packet.
equal("ACK serializer precedes response without pacing debt", F(response[0]["send_start"]), arrivals[-1] + ack_wire_time)
equal("short response is padded", response[0]["quic_bytes"], 1200)
equal("response still carries only 32 business bytes", response[0]["frames"][0]["length"], 32)
equal("response completion includes full padded packet", F(response[0]["received_at"]), arrivals[-1] + ack_wire_time + data_wire_time + 1)
equal("four padded packets and four ACKs wire bytes", r["summary"]["wire_bytes"], 4 * 1228 + 4 * 92)
equal("effective bytes exclude padding and transport", r["summary"]["unique_received_bytes"], 3504 + 32)

# Physical bottleneck: each full packet occupies this source for one
# second, longer than its initial 0.32-second pacing gap. Propagation of
# 10 seconds guarantees no feedback can affect these three starts.
slow = inputs()
slow["until"] = 40
slow["links"]["up"] = {"rate_bps": 9824, "propagation": 10}
slow["links"]["down"]["propagation"] = 10
slow["sender"]["rtt_seed"] = {"latest_rtt": 4, "smoothed_rtt": 4, "rttvar": 20, "min_rtt": 4}
s = network.calculate(slow)
slow_up = [t for t in s["transmissions"] if t["direction"] == "up" and t["kind"] == "data"]
equal("physical serializer dominates pacer", [F(t["send_start"]) for t in slow_up], [F(0), F(1), F(2)])
equal("physical serialization is nonpreemptive", [F(t["send_end"]) for t in slow_up], [F(1), F(2), F(3)])

# A millisecond path returns the response while the original upload's
# pacing debt remains outstanding. Its pure ACK must bypass that debt.
bypass = inputs()
bypass.update(upload_bytes=1168, until="0.003")
for link in bypass["links"].values():
    link["propagation"] = "0.001"
b = network.calculate(bypass)
return_ack = [t for t in b["transmissions"] if t["direction"] == "up" and t["kind"] == "ack"]
equal("ACK bypass starts on response arrival", F(return_ack[0]["send_start"]), 2 * F(1, 1000) + 2 * data_wire_time + ack_wire_time)
equal("upload pacing debt still positive after ACK bypass", F(b["pacer_final"]["up"]["debt_quic_bytes"]) > 0, True)
equal("bypass pure ACK remains unpadded", return_ack[0]["quic_bytes"], 64)

for name, result in (("paced", r), ("source_limited", s), ("ack_bypass", b)):
    for direction in ("up", "down"):
        packets = [t for t in result["transmissions"] if t["direction"] == direction]
        assert all(F(a["send_end"]) <= F(b["send_start"]) for a, b in zip(packets, packets[1:]))
    equal(name + " complete", result["summary"]["complete"], True)

report = {
    "scope": "Three independently calculated padded NewReno cases including ACK bypass with outstanding debt; not three-controller acceptance",
    "passed": len(checks),
    "source_hashes": {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in ("calculate.py", "sender.py", "pacer.py", Path(__file__).name)},
    "checks": checks,
    "cases": {"paced": r, "source_limited": s, "ack_bypass": b},
}
(ROOT / "network-pacer-root-check.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"passed": len(checks), "source_hashes": report["source_hashes"]}))
