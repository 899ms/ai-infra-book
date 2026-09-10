"""Recompute all ten unmodified inputs against the frozen network payload."""

import hashlib
import importlib.util
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent
BASELINE = ROOT.parent / "transport-closed-loop" / "result.json"


def hashes():
    return {n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest()
            for n in ("calculate.py", "sender.py", "pacer.py")}


def math_payload(result):
    return {k: v for k, v in result.items()
            if k not in ("reference_sources", "reference_source_root")}


initial = hashes()
spec = importlib.util.spec_from_file_location("baseline_review_network", ROOT / "calculate.py")
network = importlib.util.module_from_spec(spec)
spec.loader.exec_module(network)
baseline_bytes = BASELINE.read_bytes()
frozen = json.loads(baseline_bytes)
expected_hash = hashlib.sha256(baseline_bytes).hexdigest()
del baseline_bytes
inputs = network.scenarios()
assert set(inputs) == set(frozen), "baseline scenario set changed"
checks = []
for name, case in inputs.items():
    start = time.monotonic()
    assert case == frozen[name]["inputs"], (name, "inputs changed")
    actual = network.calculate(case)
    assert math_payload(actual) == math_payload(frozen[name]), (name, "full mathematical payload changed")
    checks.append({"case": name, "status": "passed", "elapsed_seconds": time.monotonic() - start})
    print(name + ": complete payload equal", flush=True)
assert hashes() == initial, "candidate changed during verification; rerun at final freeze"
assert hashlib.sha256(BASELINE.read_bytes()).hexdigest() == expected_hash, "baseline changed"
report = {
    "status": "passed", "scope": "all ten original inputs, complete recursive payload equality excluding source metadata only",
    "source_hashes": initial, "baseline_sha256": expected_hash,
    "checker_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "checks": checks,
}
(ROOT / "baseline-root-check.json").write_text(json.dumps(report, indent=2) + "\n")
