"""Explicit original-book ACK aggregation comparison; complete traces retained."""

from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import time
import calculate

ROOT = Path(__file__).resolve().parent
BASE = ROOT.parent / "transport-controller-loop"


def filehash(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1048576):
            h.update(block)
    return h.hexdigest()


def sources():
    roots = [
        ROOT,
        ROOT.parent / "congestion-controllers",
        ROOT.parent / "hystart-plus-plus",
        ROOT.parent / "congestion-controller-inputs",
    ]
    result = []
    for root in roots:
        lock = json.loads((root / "sources.lock.json").read_text())
        rows = lock["sources"] if isinstance(lock, dict) else lock
        for row in rows:
            path = root / row["file"]
            assert (
                path.stat().st_size == row["bytes"] and filehash(path) == row["sha256"]
            )
            result.append(dict(source_root=str(root), **row))
    return result


def code_hashes():
    paths = [ROOT / "calculate.py", ROOT / "receiver.py", Path(__file__)]
    paths += [
        ROOT / row["file"]
        for row in json.loads((ROOT / "dependencies.lock.json").read_text())
    ]
    paths += [
        ROOT.parent / "congestion-controllers" / name
        for name in ("cubic.py", "bbr_state.py", "bbr_reference.py", "bbr_minmax.py")
    ]
    paths += [ROOT.parent / "hystart-plus-plus/calculate.py"]
    return {str(path): filehash(path) for path in paths}


def inputs():
    originals = json.loads((BASE / "controller-scenarios.json").read_text())
    out = {}
    for name in ("newreno", "cubic_hystart", "bbr"):
        p = copy.deepcopy(originals["book-" + name])
        p["ack_policy"] = dict(
            mode="count_or_timer",
            every=2,
            max_delay="0.01",
            delay_exponent=3,
            retain_packets=256,
            reorder_immediate=True,
            header_tag_bytes=24,
        )
        assert {k: v for k, v in p.items() if k != "ack_policy"} == originals[
            "book-" + name
        ]
        out[name] = p
    return out


def run(name, p, pilot):
    before = code_hashes()
    refs = sources()
    started = time.monotonic()
    result = calculate.calculate(p)
    assert (
        before == code_hashes() and refs == sources()
    ), "code/source changed during generation"
    stem = ("pilot-" if pilot else "book-aggregate-") + name
    path = ROOT / (stem + "-result.json")
    with path.open("w") as stream:
        json.dump(result, stream, indent=2)
        stream.write("\n")
    ack = [t for t in result["transmissions"] if t["kind"] == "ack"]
    baseline = json.loads((BASE / ("book-" + name + "-manifest.json")).read_text())
    manifest = dict(
        scenario=stem,
        code_hashes=before,
        reference_sources=refs,
        elapsed_seconds=time.monotonic() - started,
        result_file=path.name,
        result_sha256=filehash(path),
        inputs=p,
        comparison_baseline_manifest="../transport-controller-loop/book-"
        + name
        + "-manifest.json",
        baseline_result_sha256=baseline["result_sha256"],
        only_original_book_input_change=None if pilot else "ack_policy",
        sender_policy_effect=dict(
            max_ack_delay_seconds="0.01",
            track_ack_only=True,
            reason="peer receive policy feeds PTO/RTT rules; ACK ranges may acknowledge pure ACK PN",
        ),
        business=result["business"],
        summary=result["summary"],
        transmission_count=len(result["transmissions"]),
        ack_count=len(ack),
        ack_quic_bytes=sum(t["quic_bytes"] for t in ack),
        max_ack_frame_bytes=max(
            (t["ack_snapshot"]["frame_bytes"] for t in ack), default=0
        ),
        max_ack_ranges=max((len(t["ack_snapshot"]["ranges"]) for t in ack), default=0),
        ack_delay_overruns=sum(t["ack_snapshot"]["exceeds_max_delay"] for t in ack),
        loss_counts={d: len(v) for d, v in result["losses"].items()},
    )
    (ROOT / (stem + "-manifest.json")).write_text(json.dumps(manifest, indent=2) + "\n")
    print(
        json.dumps(
            {
                k: manifest[k]
                for k in (
                    "scenario",
                    "elapsed_seconds",
                    "business",
                    "summary",
                    "transmission_count",
                    "ack_count",
                    "max_ack_frame_bytes",
                    "max_ack_ranges",
                    "ack_delay_overruns",
                    "loss_counts",
                )
            }
        ),
        flush=True,
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--controller", choices=list(inputs()))
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--write-inputs", action="store_true")
    args = ap.parse_args()
    all_inputs = inputs()
    if args.write_inputs:
        (ROOT / "book-comparison-inputs.json").write_text(
            json.dumps(all_inputs, indent=2) + "\n"
        )
        return
    for name in [args.controller] if args.controller else all_inputs:
        p = all_inputs[name]
        if args.pilot:
            p.update(upload_bytes=300000, response_bytes=50000)
        run(name, p, args.pilot)


if __name__ == "__main__":
    main()
