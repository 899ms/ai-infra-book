"""Check complete public payloads and actual CLI output against frozen research."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CALC = ROOT / "calculations"
sys.path.insert(0, str(CALC / "src"))
from infra_calc.topics import shared_media_transport
from infra_calc import report


def normalized(result):
    # Only source registration differs between the frozen research and package.
    return {k: v for k, v in result.items() if k not in ("reference_sources", "reference_source_root")}


def main():
    folder = Path(__file__).resolve().parent
    candidate = CALC / "research/shared-media-transport"
    frozen = json.loads((candidate / "result.json").read_text())
    scenarios = json.loads((CALC / "scenarios/book.json").read_text())["shared_media_transport"]
    checked = []
    with tempfile.TemporaryDirectory() as directory:
        inputs = Path(directory) / "inputs.json"
        output = Path(directory) / "output"
        for row in scenarios:
            name = row["id"].removeprefix("shared-media-")
            actual = shared_media_transport.calculate(row["inputs"])
            assert normalized(actual) == normalized(frozen[name]), name
            inputs.write_text(json.dumps(row["inputs"]))
            for fmt in ("json", "md"):
                subprocess.run([sys.executable, str(CALC / "calc.py"), "shared-media-transport",
                                "--inputs", str(inputs), "--format", fmt,
                                "--output", str(output)], check=True, capture_output=True)
                artifact = CALC / "results" / (row["id"] + "." + fmt)
                if fmt == "json":
                    assert json.loads(output.read_text()) == actual
                    assert json.loads(artifact.read_text()) == actual
                else:
                    assert output.read_text() == report.markdown(actual)
                    assert artifact.read_text() == output.read_text()
            checked.append(row["id"])
            print("checked " + row["id"], flush=True)
    result = {"status": "passed", "full_candidate_payload_matches": len(checked),
              "actual_cli_invocations": 2*len(checked), "frozen_artifacts_checked": 2*len(checked),
              "scenarios": checked}
    (folder / "public-check.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
