"""Incremental flight index versus a historical scan; optional pre-edit replay."""
from pathlib import Path
from fractions import Fraction as F
import argparse
import hashlib
import json
from bbr_adapter import BbrAdapter


def run(baseline_path=None):
    root = Path(__file__).resolve().parent
    adapters = [BbrAdapter(config={"external_pacer": True}, random_draws=(0,) * 1000)]
    baseline_sha = None
    if baseline_path:
        raw = baseline_path.read_bytes()
        baseline_sha = hashlib.sha256(raw).hexdigest()
        namespace = {"__file__": str(root / "bbr_adapter.py"), "__name__": "baseline"}
        exec(compile(raw, str(baseline_path), "exec"), namespace)
        adapters.append(namespace["BbrAdapter"](
            config={"external_pacer": True}, random_draws=(0,) * 1000))
    callbacks = 0
    digest = hashlib.sha256()

    def call(name, *args):
        nonlocal callbacks
        outputs = [getattr(adapter, name)(*args) for adapter in adapters]
        if len(outputs) > 1:
            assert outputs[0] == outputs[1], (callbacks, name)
            assert adapters[0].snapshot() == adapters[1].snapshot()
        current = adapters[0]
        scan = [r for r in current.records.values()
                if r["counted"] and not r["acked"] and not r["lost"]]
        assert current.active() == scan
        assert list(current.active_records) == [r["pn"] for r in scan]
        assert current.active_bytes == sum(r["sent_bytes"] for r in scan)
        assert current._flight(current.active_bytes) == len(scan)
        digest.update(json.dumps(outputs[0], sort_keys=True).encode())
        callbacks += 1

    for cycle in range(200):
        # Nonmonotonic unique PN order also checks maximum-PN recovery cutoff.
        pns = [cycle * 4 + n for n in (2, 0, 3, 1)]
        for index, pn in enumerate(pns):
            flight = index != 3
            call("on_sent", dict(pn=pn, sent_bytes=1200 if flight else 64,
                 in_flight=flight, ack_eliciting=flight, frames=[]),
                 dict(now=F(cycle) + F(index, 1000),
                      flight_before=min(index, 3) * 1200))
        call("on_loss", [pns[0]], dict(now=F(cycle) + F(1, 20), flight_after=2400))
        call("on_loss", [pns[0]], dict(now=F(cycle) + F(3, 50), flight_after=2400))
        for index, (acks, before, after) in enumerate((
            ([pns[1], pns[3]], 2400, 1200), ([pns[2]], 1200, 0),
            ([pns[0]], 0, 0), ([pns[0]], 0, 0))):
            now = F(cycle) + F(10 + index, 100)
            call("on_ack", acks, dict(now=now, flight_before=before,
                 flight_after=after, pacer_next_eligible=now,
                 rtt_sample=None, smoothed_rtt="1/10"))
    return dict(status="passed", callbacks=callbacks, historical_records=800,
                active_scan_checks=callbacks, baseline_sha256=baseline_sha,
                baseline_file=str(baseline_path.resolve().relative_to(root)) if baseline_path and baseline_path.resolve().is_relative_to(root) else str(baseline_path),
                checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                adapter_sha256=hashlib.sha256((root / "bbr_adapter.py").read_bytes()).hexdigest(),
                event_digest_sha256=digest.hexdigest(),
                comparison="Every returned event and snapshot equal" if baseline_path else
                           "Incremental membership/order/bytes versus historical scan")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, default=Path(__file__).with_name("baselines") / "bbr_adapter_c410_before_active_index.py")
    args = parser.parse_args()
    result = run(args.baseline)
    Path(__file__).with_name("bbr-active-index-check.json").write_text(
        json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
