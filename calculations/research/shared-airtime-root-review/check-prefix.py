"""Check horizon causality by rerunning the same workload at earlier cutoffs.

This is a metamorphic check, not an independent implementation of the PHY.
It compares actual event prefixes and separately clips resource reservations.
"""
from copy import deepcopy
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
CANDIDATE = HERE.parent / "shared-airtime-loop"
spec = importlib.util.spec_from_file_location("prefix_candidate", CANDIDATE / "calculate.py")
network = importlib.util.module_from_spec(spec)
spec.loader.exec_module(network)


def source_hashes():
    paths = {Path(__file__), CANDIDATE / "calculate.py", CANDIDATE / "airtime.py",
             CANDIDATE / "scenarios.json"}
    paths.update(Path(module.__file__).resolve() for name, module in tuple(sys.modules.items())
                 if name.startswith("infra_calc") and getattr(module, "__file__", "").endswith(".py"))
    return {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(paths)}


def actual_receipts(result, horizon):
    return [(row["direction"], row["pn"], row["received_at"])
            for row in result["transmissions"]
            if row.get("received_at") is not None and Fraction(row["received_at"]) <= horizon]


def main():
    before = source_hashes()
    cases = json.loads((CANDIDATE / "scenarios.json").read_text())
    reports = []
    for name, original in cases.items():
        if not original["network"]["wireless_access"]["enabled"]:
            continue
        full = network.calculate(deepcopy(original))
        end = Fraction(str(original["network"]["until"]))
        boundaries = {Fraction(0), end / 2}
        for attempt in full["wireless_attempts"]:
            for field in ("reservation_start", "data_start", "data_end", "receive_at", "feedback_at"):
                if attempt[field] is not None:
                    boundaries.add(Fraction(attempt[field]))
        ordered = sorted(t for t in boundaries if 0 <= t < end)
        cutoffs = sorted(t for t in set(ordered + [(a + b) / 2 for a, b in zip(ordered, ordered[1:])]) if t > 0)
        for horizon in cutoffs:
            inputs = deepcopy(original)
            inputs["network"]["until"] = str(horizon)
            short = network.calculate(inputs)
            expected_events = [e for e in full["wireless_events"] if Fraction(e["at"]) <= horizon]
            assert short["wireless_events"] == expected_events, (name, str(horizon), "event prefix")
            assert actual_receipts(short, horizon) == actual_receipts(full, horizon), (name, str(horizon), "receipts")
            for direction in ("up", "down"):
                expected = [e for e in full["sender_events"][direction] if Fraction(e["at"]) <= horizon]
                assert short["sender_events"][direction] == expected, (name, str(horizon), direction, "sender prefix")
            reserved = sum((max(Fraction(0), min(horizon, Fraction(r["end"]) if r["end"] is not None else end)
                                - Fraction(r["start"])) for r in full["wireless_reservations"]), Fraction(0))
            assert Fraction(short["wireless_summary"]["observed_reserved_seconds"]) == reserved, (name, str(horizon), "resource clipping")
        reports.append({"case": name, "cutoffs": [str(t) for t in cutoffs], "checks": 5 * len(cutoffs)})
    assert source_hashes() == before, "sources changed while executing"
    report = {"status": "passed_horizon_prefix_scope", "source_hashes": before,
              "checks": sum(row["checks"] for row in reports), "cases": reports,
              "scope": "Actual wireless and sender event prefixes, endpoint receipts, clipped reservations; not independent controller or PHY verification."}
    (HERE / "prefix-result.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "checks": report["checks"], "cases": len(reports)}))


if __name__ == "__main__":
    main()
