"""Run explicit controller comparison inputs and preserve full packet evidence."""

import argparse
import copy
import hashlib
import json
from pathlib import Path
import time
import calculate

ROOT = Path(__file__).resolve().parent
CODE_FILES = [
    "calculate.py",
    "sender.py",
    "cubic_adapter.py",
    "bbr_adapter.py",
    "pacer.py",
    "persistent_congestion.py",
]


def hashes():
    return {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in CODE_FILES}


def verify_sources():
    roots = [
        ROOT,
        ROOT.parent / "congestion-controllers",
        ROOT.parent / "hystart-plus-plus",
        ROOT.parent / "congestion-controller-inputs",
    ]
    checked = []
    for source_root in roots:
        lock = json.loads((source_root / "sources.lock.json").read_text())
        rows = lock["sources"] if isinstance(lock, dict) else lock
        for row in rows:
            raw = (source_root / row["file"]).read_bytes()
            if (
                len(raw) != row["bytes"]
                or hashlib.sha256(raw).hexdigest() != row["sha256"]
            ):
                raise ValueError("Source mismatch: " + str(source_root / row["file"]))
            checked.append(dict(source_root=str(source_root), **row))
    return checked


def scenarios():
    result = {}
    for name in ("newreno", "cubic_hystart", "bbr"):
        book = copy.deepcopy(calculate.scenarios()["book-30mb-5mb"])
        book.update(controller={"name": name}, pad_in_flight=True)
        result["book-" + name] = book
        router = copy.deepcopy(book)
        router.update(upload_bytes=3000000, response_bytes=500000, until=60)
        router["links"]["up"] = dict(rate_bps=1000000000, propagation=0)
        router["routers"] = {
            "up": dict(rate_bps=20000000, queue_bytes=10000000, propagation="0.05")
        }
        result["router-" + name] = router
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--scenario", choices=list(scenarios()))
    ap.add_argument("--write-inputs", action="store_true")
    args = ap.parse_args()
    inputs = scenarios()
    if args.write_inputs:
        (ROOT / "controller-scenarios.json").write_text(
            json.dumps(inputs, indent=2) + "\n"
        )
        return
    selected = [args.scenario] if args.scenario else list(inputs)
    for name in selected:
        sources_before = verify_sources()
        before = hashes()
        started = time.monotonic()
        value = calculate.calculate(inputs[name])
        if before != hashes() or sources_before != verify_sources():
            raise RuntimeError("source changed during scenario; result not frozen")
        path = ROOT / (name + "-result.json")
        path.write_text(json.dumps(value, indent=2) + "\n")
        manifest = dict(
            reference_sources=sources_before,
            scenario=name,
            code_hashes=before,
            elapsed_seconds=time.monotonic() - started,
            result_file=path.name,
            result_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            business=value["business"],
            summary=value["summary"],
        )
        (ROOT / (name + "-manifest.json")).write_text(
            json.dumps(manifest, indent=2) + "\n"
        )
        print(json.dumps(manifest), flush=True)


if __name__ == "__main__":
    main()
