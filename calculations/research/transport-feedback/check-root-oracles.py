"""Execute root's prewritten arithmetic and actual CLI reproducibility checks."""
from fractions import Fraction as F
from pathlib import Path
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("candidate", ROOT / "calculate.py")
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)
frozen = "1f3890671c60d9841d3dd89e289483940872c2823d7ba767b3a6b845dcbea567"
assert hashlib.sha256((ROOT / "calculate.py").read_bytes()).hexdigest() == frozen
checks = []


def check(name, actual, expected):
    assert actual == expected, (name, actual, expected)
    checks.append(name)


def sent(pn, at, offset=0, length=100):
    return dict(type="sent", pn=pn, at=at, sent_bytes=1200,
                frames=[dict(type="stream", stream="A", offset=offset, length=length)])


def ack(at, pn):
    return dict(type="ack", at=at, ranges=[[pn, pn]])


p = candidate.example()
p["until"] = "1.3"
p["events"].append(sent(2, "1", 200))
r = candidate.calculate(p)
check("rtt samples", [(F(x["smoothed"]), F(x["rttvar"])) for x in r["rtt_samples"]],
      [(F(1, 10), F(1, 20)), (F(1, 10), F(3, 80))])
check("PTO deadline", [(x["kind"], F(x["at"])) for x in r["timer_events"]], [("pto", F(51, 40))])
check("PTO no loss", r["loss_events"], [])
check("no synthetic probe bytes", r["summary"]["sent_udp_payload_bytes"], 3600)
check("PTO unchanged window", F(r["final_state"]["cwnd"]), F(14400))
check("pending timer vs observation horizon", F(r["final_state"]["next_timer"]["at"]), F(31, 20))
check("last actual event", F(r["summary"]["last_processed_event"]), F(51, 40))
p["events"].append(ack("1.275", 2))
r = candidate.calculate(p)
check("ACK wins PTO tie", r["timer_events"], [])

p = candidate.example()
p["until"] = "0.38"
p["events"][-1]["at"] = "0.38"
r = candidate.calculate(p)
check("verified erratum variance", F(r["rtt_samples"][-1]["rttvar"]), F(21, 400))
check("verified erratum smoothed", F(r["rtt_samples"][-1]["smoothed"]), F(43, 400))

p = dict(initial_max_data=10000, initial_max_stream_data={"A": 10000}, until="0.1145",
         rtt_seed=dict(latest_rtt="0.1", smoothed_rtt="0.1", min_rtt="0.1", rttvar="0.05"),
         events=[sent(i, str(F(i, 1000)), i * 100) for i in range(4)] + [ack("0.103", 3)])
r = candidate.calculate(p)
check("packet and independent time thresholds", [(x["pn"], F(x["at"])) for x in r["loss_events"]],
      [(0, F(103, 1000)), (1, F(227, 2000)), (2, F(229, 2000))])
check("time zero loss enters recovery only once", F(r["final_state"]["cwnd"]), F(6000))
p["events"].append(ack("0.1135", 1))
r = candidate.calculate(p)
check("ACK wins loss tie", [x["pn"] for x in r["loss_events"]], [0])
# ACK1 gives a new RTT sample: 113.5-1=112.5 ms. That moves PN2's
# deadline to 2 + 9/8*112.5 = 128.5625 ms, beyond this replay horizon.
check("new ACK recomputes remaining deadline", F(r["final_state"]["next_timer"]["at"]), F(2057, 16000))

p = dict(initial_max_data=6, initial_max_stream_data={"A": 6}, until="0.1",
         events=[sent(0, 0, 5, 1), sent(1, "0.001", 0, 5),
                 dict(type="ack", at="0.1", ranges=[[0, 1]])])
r = candidate.calculate(p)
check("offset hole counts as flow", r["events"][0]["state"]["max_data_consumed"], 6)
check("hole filling does not consume more flow", r["final_state"]["max_data_consumed"], 6)
check("unique confirmed hole-filled bytes", r["sender_confirmed_business"]["unique_stream_bytes"], 6)

p = dict(initial_max_data=6, initial_max_stream_data={"A": 4, "B": 2}, until=6,
         events=[sent(0, 0, 0, 4), sent(1, "0.001", 0, 2),
                 dict(type="ack", at="0.1", ranges=[[0, 1]])])
p["events"][1]["frames"][0]["stream"] = "B"
for t in ("0.2", "5", "6"):
    e = sent(2, t, 4, 2)
    e["type"] = "can_send"
    p["events"].append(e)
p["events"] += [dict(type="max_data", at=5, value=8),
                 dict(type="max_stream_data", at=6, stream="A", value=6)]
r = candidate.calculate(p)
check("absolute limits must both arrive", [x["details"]["can_send"] for x in r["events"] if x["event"] == "can_send"], [False, False, True])

with tempfile.TemporaryDirectory() as directory:
    path = Path(directory)
    subprocess.run([sys.executable, str(ROOT / "calculate.py"), "--output", str(path / "all.json")], check=True)
    check("actual default CLI all 14 payloads", json.loads((path / "all.json").read_text()), json.loads((ROOT / "result.json").read_text()))
    for name, inputs in candidate.scenarios().items():
        (path / "input.json").write_text(json.dumps(inputs))
        subprocess.run([sys.executable, str(ROOT / "calculate.py"), "--inputs", str(path / "input.json"), "--output", str(path / "one.json")], check=True)
        check("actual editable CLI " + name, json.loads((path / "one.json").read_text()), candidate.calculate(inputs))

assert hashlib.sha256((ROOT / "calculate.py").read_bytes()).hexdigest() == frozen
(ROOT / "root-check.json").write_text(json.dumps(dict(status="passed", candidate_sha256=frozen,
    checks=checks, actual_cli_invocations=15,
    scope="Prewritten root arithmetic plus complete CLI payload equality; no network/receiver/controller closed loop claimed."), indent=2) + "\n")
print(f"Passed {len(checks)} root checks and 15 actual CLI invocations")
