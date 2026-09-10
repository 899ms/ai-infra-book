"""Independent strict duration, ACK barrier, first-sample and trigger examples."""
from pathlib import Path
from fractions import Fraction as F
import hashlib
import json
from persistent_congestion import evaluate

ROOT = Path(__file__).resolve().parent
passed = []


def packet(pn, at, status="lost", eliciting=True, prior=True):
    return dict(pn=pn, sent_at=str(at), status=status,
                ack_eliciting=eliciting, rtt_known_at_send=prior)


def run(rows, **kwargs):
    # 1 + 4*0.2 + 0.2 = 2 seconds; persistence threshold is six.
    return evaluate(rows, smoothed_rtt=1, rttvar="1/5", max_ack_delay="1/5", granularity="1/1000", **kwargs)


for name, rows, expected in [
    ("strict equality", [packet(0, 1), packet(1, 7)], False),
    ("strictly exceeds", [packet(0, 1), packet(1, "7.001")], True),
    ("ACK splits span", [packet(0, 1), packet(1, 4, "acked"), packet(2, 8)], False),
    ("late ACK also splits", [packet(0, 1), packet(1, 4, "lost_then_acked"), packet(2, 8)], False),
    ("non eliciting ACK splits", [packet(0, 1), packet(1, 4, "acked", False), packet(2, 8)], False),
    ("oldest lacks prior RTT", [packet(0, 1, prior=False), packet(1, 2), packet(2, 8)], False),
    ("endpoints must elicit ACK", [packet(0, 1, eliciting=False), packet(1, 8)], False),
    ("pending middle is not ACK evidence", [packet(0, 1), packet(1, 4, "sent"), packet(2, 8)], True),
    ("time-zero endpoint", [packet(0, 0), packet(1, 7)], True),
]:
    result = run(rows)
    assert result["established"] is expected, name
    assert result["threshold_duration"] == "6"
    if expected:
        assert result["required_cwnd_bytes"] == 2400
    passed.append(name)

# The RFC example presupposes an RTT estimate before packet2 at t=1;
# its ACK of packet1 at1.2 is not treated as the first RTT sample here.
rows = [packet(1, 0, "acked")] + [packet(pn, at) for pn, at in zip(range(2, 9), [1, 2, 3, 4, 5, 6, 8])] + [packet(9, 12, "acked")]
r = run(rows)
assert r["qualifying_spans"] == [dict(first_pn=2, last_pn=8, start="1", end="8", duration="7", evidence_key="2:8")]
passed.append("RFC7.6.3 seven-second loss with prior estimate")
for trigger in ("pto", "loss_timer"):
    r = run(rows, trigger=trigger)
    assert not r["established"] and r["required_cwnd_bytes"] is None
    passed.append("no declaration on " + trigger)
for invalid in ([packet(0, 0), packet(0, 7)], [packet(1, 0), packet(0, 7)], [packet(0, -1)],
                [packet(0, 0), packet(2, 7)], [packet(0, 0), packet(1, 7, prior=False)]):
    try:
        run(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError("Invalid history accepted")
    passed.append("invalid history rejected")
(ROOT / "persistent-check.json").write_text(json.dumps(dict(status="passed", checks=passed,
    candidate_sha256=hashlib.sha256((ROOT / "persistent_congestion.py").read_bytes()).hexdigest(),
    scope="Pure evidence predicate only; controller episode deduplication and minimum-window action not integrated yet."), indent=2) + "\n")
print(f"Passed {len(passed)} persistent-congestion checks")
