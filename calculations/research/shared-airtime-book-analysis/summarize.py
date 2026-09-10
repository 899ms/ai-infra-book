"""Produce a layered airtime ledger from one actually generated full trace.

This report aggregates observations. It does not replace the independent trace
checker and does not infer application success from an empty packet queue.
"""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    manifest_hash = sha(args.manifest)
    manifest = json.loads(args.manifest.read_text())
    if manifest["status"] != "COMPLETE_STABLE_IDENTITY_NOT_INDEPENDENT_ACCEPTANCE":
        raise ValueError("a successfully completed generation manifest is required")
    result_path = args.manifest.parent / manifest["result_file"]
    if sha(result_path) != manifest["result_sha256"]:
        raise ValueError("result does not match generation manifest")
    result = json.loads(result_path.read_text())
    counts = Counter()
    seconds = defaultdict(F)
    octets = Counter()
    for row in result["wireless_attempts"]:
        service = row["service"]
        if service["data_ppdu"] is None or service["mac_ack_ppdu"] is None:
            raise ValueError("this physical ledger requires a fully specified successful OFDM exchange")
        if not row["received"] or not row["feedback_known"] or row["outcome"] != "success":
            raise ValueError("partial or failed exchanges require a separate observed-phase ledger")
        group = row["direction"] + "." + row["kind"]
        counts[group] += 1
        counts["same_pn_retries"] += row["attempt"] > 1
        octets["ip_bytes_in_radio_attempts"] += service["ip_bytes"]
        octets["data_psdu_bytes"] += service["data_psdu_bytes"]
        octets["mac_ack_psdu_bytes"] += service["mac_ack_psdu_bytes"]
        seconds["reserved"] += F(service["reserved_service_seconds"])
        seconds["radio_transmit"] += F(service["radio_transmit_seconds"])
        seconds["access_idle"] += F(service["access_idle_seconds"])
        seconds["group_reserved." + group] += F(service["reserved_service_seconds"])
    seconds["non_transmit_reserved"] = seconds["reserved"] - seconds["radio_transmit"]
    seconds["remaining_non_transmit_after_access"] = seconds["non_transmit_reserved"] - seconds["access_idle"]
    assert seconds["reserved"] == F(result["wireless_summary"]["observed_reserved_seconds"])
    octets["all_psdu_bytes"] = octets["data_psdu_bytes"] + octets["mac_ack_psdu_bytes"]
    octets["mac_llc_fcs_over_ip"] = octets["data_psdu_bytes"] - octets["ip_bytes_in_radio_attempts"]
    report = {
        "case": manifest["case"],
        "scope": "Aggregated complete successful OFDM exchanges; requires separate independent trace acceptance.",
        "manifest_sha256": manifest_hash,
        "result_sha256": manifest["result_sha256"],
        "script_sha256": sha(Path(__file__)),
        "packet_counts": dict(counts),
        "radio_octets": dict(octets),
        "air_seconds_exact": {key: str(value) for key, value in seconds.items()},
        "air_seconds_decimal": {key: float(value) for key, value in seconds.items()},
        "end_to_end_summary": result["summary"],
        "businesses": result["businesses"],
        "notes": [
            "PSDU bytes exclude PHY preamble and symbol timing; time intervals are never converted into fabricated bytes.",
            "IP bytes repeated in radio attempts are not unique application bytes.",
            "Radio transmit time excludes access idle, SIFS and propagation; reserved time includes the declared service phases.",
            "WAN and radio can overlap. Their service sums are not an end-to-end completion-time prediction.",
            "This reference uses declared global FIFO with no random contention, aggregation, encryption or measured device behavior.",
        ],
    }
    assert sha(args.manifest) == manifest_hash and sha(result_path) == manifest["result_sha256"]
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"case": report["case"], "reserved_seconds": str(seconds["reserved"]), "all_psdu_bytes": octets["all_psdu_bytes"]}))


if __name__ == "__main__":
    main()
