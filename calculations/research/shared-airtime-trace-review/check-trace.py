"""Independent saved-trace algebra; imports neither network nor airtime engine."""

from pathlib import Path
from fractions import Fraction as F
from collections import Counter, defaultdict
from bisect import bisect_right
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parent
CALC = ROOT.parent.parent
INPUTS = ROOT.parent / "shared-airtime-inputs"


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def identities():
    rows = json.loads((INPUTS / "sources.lock.json").read_text())
    files = [INPUTS / "sources.lock.json", INPUTS / "profiles.json"]
    for row in rows:
        path = INPUTS / row["file"]
        assert path.stat().st_size == row["bytes"] and sha(path) == row["sha256"], path
        files.append(path)
    files += [
        ROOT.parent / "shared-airtime-loop" / name
        for name in ("calculate.py", "airtime.py")
    ]
    files += list((CALC / "src/infra_calc/transport").glob("*.py"))
    files += [CALC / "src/infra_calc/topics/transport_sender.py"]
    return {str(p.relative_to(CALC)): sha(p) for p in sorted(set(files))}


def union_length(intervals):
    total = 0
    end = None
    for left, right in sorted(intervals):
        if end is None or left > end:
            total += right - left
            end = right
        elif right > end:
            total += right - end
            end = right
    return total


def contiguous(intervals):
    end = 0
    for left, right in sorted(intervals):
        if left > end:
            break
        end = max(end, right)
    return end


def expected_exchange(profile, ip_bytes, transport_ack, outcome, switch):
    """Re-derive selected profile algebra without importing the implementation."""
    if "phy" in profile:
        phy, layout, access = profile["phy"], profile["layout"], profile["access"]
        symbol = F(phy["ofdm_symbol_seconds"])

        def duration(size, rate):
            ndbps = F(str(rate)) * symbol
            bits = 16 + size * 8 + 6
            # This checker deliberately covers the sealed SERVICE16/tail6 profile.
            assert phy["service_bits"] == 16 and phy["tail_bits"] == 6
            count = (F(bits) / ndbps).__ceil__()
            return (
                F(phy["preamble_seconds"])
                + F(phy["signal_header_seconds"])
                + count * symbol
                + F(phy["signal_extension_seconds"])
            )

        extra = sum(
            layout[k]
            for k in (
                "llc_snap_bytes",
                "data_mac_header_bytes",
                "mac_fcs_bytes",
                "security_overhead_bytes",
            )
        )
        psdu = ip_bytes + extra
        ack_bytes = (
            layout["normal_mac_ack_header_bytes"] + layout["normal_mac_ack_fcs_bytes"]
        )
        data = duration(psdu, phy["data_rate_bps"])
        ack = duration(ack_bytes, phy["mac_ack_rate_bps"])
        access_time = F(access["pre_exchange_idle_seconds"]) + access[
            "backoff_slots_selected"
        ] * F(access["slot_seconds"])
        if switch:
            access_time += F(access["direction_switch_extra_seconds"])
        propagation = F(access["radio_propagation_selected_seconds"])
        sifs = F(access["sifs_seconds"])
        timeout = access["mac_ack_complete_timeout_seconds"]
        failed = None if timeout is None else data + F(timeout)
        rf = data + (0 if outcome == "data_lost" else ack)
    else:
        access_time = F(profile["contention_seconds"])
        propagation = F(profile["propagation_seconds"])
        sifs = F(0)
        ack = F(profile["post_data_sifs_plus_mac_ack_seconds"])
        data = (
            F(profile["transport_ack_whole_exchange_seconds"]) - ack
            if transport_ack
            else F(profile["data_ppdu_seconds"])
        )
        failed = (
            F(profile["full_ack_failure_known_from_data_txstart_seconds"])
            if profile.get("full_ack_failure_known_from_data_txstart_seconds")
            is not None
            else None
        )
        psdu = ack_bytes = rf = None
    receive = access_time + data + propagation
    ack_start = receive + sifs
    ack_end = ack_start + ack
    success = ack_end + propagation
    if outcome == "success":
        end = success
    else:
        assert failed is not None and access_time + failed >= success
        end = access_time + failed
    return dict(
        data_start_offset=access_time,
        data_end_offset=access_time + data,
        data_receive_offset=None if outcome == "data_lost" else receive,
        mac_ack_start_offset=None if outcome == "data_lost" else ack_start,
        mac_ack_end_offset=None if outcome == "data_lost" else ack_end,
        mac_feedback_offset=end,
        exchange_end_offset=end,
        data_psdu_bytes=psdu,
        mac_ack_psdu_bytes=ack_bytes,
        radio_transmit_seconds=rf,
    )


def check(result):
    p = result["inputs"]
    until = F(str(p["network"]["until"]))
    tx = result["transmissions"]
    packets = {(r["direction"], r["pn"]): r for r in tx}
    assert len(packets) == len(tx)
    sent = {}
    for direction, events in result["sender_events"].items():
        records = [e for e in events if e["type"] == "sent"]
        assert [e["pn"] for e in records] == list(range(len(records)))
        for e in records:
            key = direction, e["pn"]
            assert key not in sent
            sent[key] = e
            r = packets[key]
            assert F(e["at"]) == F(r["send_start"]) and e["frames"] == r["frames"]
            assert (
                e["sent_bytes"] == r["quic_bytes"]
                and r["wire_bytes"] == e["sent_bytes"] + 28
            )
    assert (
        sent.keys() == packets.keys()
    ), "MAC retry created or omitted transport sent identity"
    # Every real transport ACK arrival induces one feedback event; local MAC ACK
    # confirmations and filtered MAC duplicates cannot invent transport ACKs.
    expected_feedback = Counter(
        (("down" if r["direction"] == "up" else "up"), F(r["received_at"]))
        for r in tx
        if r["kind"] == "ack" and r["received_at"] is not None
    )
    feedback = Counter(
        (d, F(e["at"]))
        for d, events in result["sender_events"].items()
        for e in events
        if e["type"] == "ack"
    )
    assert expected_feedback == feedback
    per_message = defaultdict(list)
    by_flow = defaultdict(list)
    message_records = defaultdict(list)
    flow_events = defaultdict(list)
    messages = {m["id"]: m for m in p["application"]["messages"]}
    for r in tx:
        if r["received_at"] is None:
            continue
        assert F(r["received_at"]) <= until
        if r["kind"] != "data":
            continue
        message_records[r["message_id"]].append(r)
        length = sum(f["length"] for f in r["frames"])
        message = messages[r["message_id"]]
        assert (
            0 <= r["message_offset"] < message["bytes"]
            and r["message_offset"] + length <= message["bytes"]
        )
        interval = (r["message_offset"], r["message_offset"] + length)
        per_message[r["message_id"]].append(interval)
        for f in r["frames"]:
            if f["type"] == "stream":
                assert (
                    f["stream"] == message["flow_id"]
                    and f["offset"] == message["stream_offset"] + r["message_offset"]
                )
                by_flow[r["direction"], f["stream"]].append(
                    (f["offset"], f["offset"] + f["length"])
                )
                flow_events[r["direction"], f["stream"]].append(
                    (F(r["received_at"]), f["offset"], f["offset"] + f["length"])
                )
    unique = sum(union_length(v) for v in per_message.values())
    assert unique == result["summary"]["unique_received_application_bytes"]
    delivered = sum(
        m["bytes"] for key, m in messages.items() if key in result["delivered"]
    )
    assert delivered == result["summary"]["delivered_application_bytes"]
    prefix_histories = {}
    for flow, events in flow_events.items():
        intervals = []
        times = []
        prefixes = []
        for at, left, right in sorted(events):
            merged = []
            for a, b in sorted([*intervals, (left, right)]):
                if merged and a <= merged[-1][1]:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], b))
                else:
                    merged.append((a, b))
            intervals = merged
            times.append(at)
            prefixes.append(
                intervals[0][1] if intervals and intervals[0][0] == 0 else 0
            )
        prefix_histories[flow] = (times, prefixes)
    for key, m in messages.items():
        if key not in result["delivered"]:
            continue
        delivered_at = F(result["delivered"][key])
        assert delivered_at <= until
        arrivals = [
            r for r in message_records[key] if F(r["received_at"]) <= delivered_at
        ]
        covered = [
            (
                r["message_offset"],
                r["message_offset"] + sum(f["length"] for f in r["frames"]),
            )
            for r in arrivals
        ]
        assert contiguous(covered) >= m["bytes"], ("incomplete delivered message", key)
        if m["transport"] == "stream":
            direction = "up" if m["sender"] == "client" else "down"
            times, prefixes = prefix_histories[direction, m["flow_id"]]
            index = bisect_right(times, delivered_at) - 1
            assert index >= 0 and prefixes[index] >= m["stream_offset"] + m["bytes"]
    if "wireless_attempts" not in result:
        return dict(
            mode="disabled",
            packets=len(tx),
            unique_received_bytes=unique,
            source_sent_events=len(sent),
        )
    wireless = p["network"]["wireless_access"]
    profile = wireless["profile"]
    attempts = result["wireless_attempts"]
    failures = {
        (f["direction"], f["pn"], f["attempt"]): f["outcome"]
        for f in wireless.get("failures", [])
    }
    groups = defaultdict(list)
    last_direction = None
    seen = set()
    observed = F(0)
    reservations = result["wireless_reservations"]
    reservation_index = {(F(v["start"]), v["direction"]): v for v in reservations}
    assert len(reservation_index) == len(reservations)
    previous_end = F(0)
    for reservation in reservations:
        start = F(reservation["start"])
        data_start = F(reservation["data_start"])
        end = F(reservation["end"]) if reservation["end"] is not None else until
        assert start >= previous_end and data_start >= start and end >= start
        assert start <= until
        observed += max(F(0), min(until, end) - start)
        previous_end = end
    for index, a in enumerate(attempts):
        assert a["index"] == index
        key = a["direction"], a["pn"]
        r = packets[key]
        groups[key].append(a)
        assert a["attempt"] == len(groups[key]) and a["attempt"] <= wireless.get(
            "max_attempts", 1
        )
        outcome = failures.get((*key, a["attempt"]), "success")
        assert a["outcome"] == outcome
        fields = expected_exchange(
            profile,
            r["wire_bytes"],
            r["kind"] == "ack",
            outcome,
            last_direction not in (None, a["direction"]),
        )
        last_direction = a["direction"]
        start = F(a["reservation_start"])
        for field, value in fields.items():
            actual = a["service"][field]
            assert actual is None if value is None else F(str(actual)) == value, (
                key,
                field,
                actual,
                value,
            )
        for name, offset in (
            ("data_start", "data_start_offset"),
            ("data_end", "data_end_offset"),
            ("receive_at", "data_receive_offset"),
            ("feedback_at", "mac_feedback_offset"),
            ("end", "exchange_end_offset"),
        ):
            value = fields[offset]
            assert a[name] is None if value is None else F(a[name]) == start + value, (
                key,
                name,
            )
        assert a["received"] == (
            a["receive_at"] is not None and F(a["receive_at"]) <= until
        )
        assert a["feedback_known"] == (F(a["feedback_at"]) <= until)
        if a["received"]:
            assert a["duplicate_at_hop_receiver"] == (key in seen)
            seen.add(key)
        assert reservation_index[start, a["direction"]]["end"] == a["end"]
        if a["attempt"] > 1:
            previous = groups[key][-2]
            assert previous["outcome"] != "success" and previous["feedback_known"]
            assert F(a["data_start"]) >= F(previous["feedback_at"]) + F(
                str(wireless.get("retry_wait", 0))
            )
    for key, group in groups.items():
        r = packets[key]
        assert r["wireless_attempt_indices"] == [a["index"] for a in group]
        first_received = next((a for a in group if a["received"]), None)
        assert r.get("wireless_received_at") == (
            first_received["receive_at"] if first_received else None
        )
        if key[0] == "up":
            assert (
                r["send_start"] == group[0]["data_start"]
                and r["send_end"] == group[0]["data_end"]
            )
        if first_received and key[0] == "down":
            assert r["received_at"] == first_received["receive_at"]
    wan = defaultdict(list)
    wan_prefix = F(0)
    for r in tx:
        d = r["direction"]
        settings = p["network"]["links"][d]
        if d == "down":
            start, end = F(r["send_start"]), F(r["send_end"])
        elif "wan_start" in r:
            start, end = F(r["wan_start"]), F(r["wan_end"])
            assert start >= F(r["wireless_received_at"])
        else:
            continue
        assert end - start == F(r["wire_bytes"] * 8) / F(str(settings["rate_bps"]))
        wan[d].append((start, end))
        wan_prefix += r["wire_bytes"] * min(
            F(1), max(F(0), (until - start) / (end - start))
        )
        hop = end + F(str(settings["propagation"]))
        if "router_start" in r:
            router = p["network"]["routers"][d]
            assert F(r["router_start"]) >= hop
            assert F(r["router_end"]) - F(r["router_start"]) == F(
                r["wire_bytes"] * 8
            ) / F(str(router["rate_bps"]))
            hop = F(r["router_end"]) + F(str(router.get("propagation", 0)))
        if d == "down" and "ap_ready_at" in r:
            assert F(r["ap_ready_at"]) == hop and F(r["wan_arrival"]) == hop
            for attempt in groups[d, r["pn"]]:
                assert F(attempt["data_start"]) >= hop
        if d == "up" and r["received_at"] is not None:
            assert F(r["received_at"]) == hop
    for d, intervals in wan.items():
        ordered = sorted(intervals)
        assert all(a[1] <= b[0] for a, b in zip(ordered, ordered[1:])), d
    summary = result["wireless_summary"]
    assert F(summary["observed_reserved_seconds"]) == observed
    assert F(summary["reserved_service_seconds"]) == sum(
        F(a["end"]) - F(a["reservation_start"]) for a in attempts
    )
    assert summary["attempts_started"] == len(attempts)
    assert summary["same_pn_retry_attempts"] == sum(len(g) - 1 for g in groups.values())
    assert result["summary"]["serialized_wire_bytes_by_horizon"] is None
    assert F(result["summary"]["wan_serialized_ip_bytes_by_horizon"]) == wan_prefix
    return dict(
        mode="enabled",
        packets=len(tx),
        attempts=len(attempts),
        reservations=len(reservations),
        observed_air_seconds=str(observed),
        unique_received_bytes=unique,
        source_sent_events=len(sent),
        transport_feedback_events=sum(feedback.values()),
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--result", type=Path, default=ROOT.parent / "shared-airtime-loop/result.json"
    )
    parser.add_argument("--output", type=Path, default=ROOT / "small-check.json")
    args = parser.parse_args()
    before = identities()
    result_hash = sha(args.result)
    data = json.loads(args.result.read_text())
    rows = {"single": data} if "transmissions" in data else data
    checks = {name: check(result) for name, result in rows.items()}
    assert before == identities() and result_hash == sha(
        args.result
    ), "identity changed during review"
    args.output.write_text(
        json.dumps(
            dict(
                status="passed",
                scope="independent saved-trace airtime/WAN/PN/unique-byte algebra; not full application scheduler or standards certification",
                checks=checks,
                result_file=str(args.result.resolve()),
                result_sha256=result_hash,
                source_and_runtime_hashes=before,
                checker_sha256=sha(Path(__file__)),
            ),
            indent=2,
        )
        + "\n"
    )
    print("passed", len(checks), "saved results")


if __name__ == "__main__":
    main()
