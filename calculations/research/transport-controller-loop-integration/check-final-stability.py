"""Reconcile final artifacts with CLI evidence and the discovered ordering fix."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
sys.path.insert(0, str(PROJECT / "src"))
from infra_calc.reproduce import verify_results

verification = verify_results(include_figures=False)
before = json.loads((ROOT / "manifest-before-editorial-fix.json").read_text())
after = json.loads((PROJECT / "results/manifest.json").read_text())
old = {r["file"]: r["sha256"] for r in before["artifacts"]}
new = {r["file"]: r["sha256"] for r in after["artifacts"]}
assert old.keys() == new.keys()
changed = sorted(p for p in old if old[p] != new[p])
assert all(p.startswith("results/stage-resources-") for p in changed), changed

semantic_checks = []
for backup in sorted((ROOT / "before-determinism-fix").glob("*.json")):
    current = PROJECT / "results" / backup.name
    assert json.loads(backup.read_text()) == json.loads(current.read_text()), backup.name
    semantic_checks.append(backup.name)
assert len(semantic_checks) == 25

cli = json.loads((ROOT / "cli-check.json").read_text())
assert cli["status"] == "passed" and cli["cli_calls"] == 12
for path, expected in cli["source_hashes_after"].items():
    assert hashlib.sha256((PROJECT / path).read_bytes()).hexdigest() == expected, path
for check in cli["checks"]:
    assert check["bytewise_equal"]
    assert new[check["expected_file"]] == check["actual_sha256"]

report = {
    "status": "passed",
    "verification": verification,
    "unchanged_artifacts": len(new) - len(changed),
    "serialization_changed_artifacts": changed,
    "stage_resource_math_equal": semantic_checks,
    "actual_cli_outputs_still_identical": cli["cli_calls"],
    "cli_math_sources_still_identical": len(cli["source_hashes_after"]),
    "scope": "Final artifact reconciliation; stage resource mapping order was stabilized, not a numerical change.",
}
(ROOT / "final-stability-check.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({k: v for k, v in report.items() if not isinstance(v, list)}))
