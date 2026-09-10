"""Read a completed result and audit physical, ACK, byte and DAG invariants.

Never imports or executes the candidate. No-router traces only, explicitly.
"""

import argparse
from bisect import bisect_right
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path


def add_interval(ranges, start, end):
    values = sorted([*ranges, (start, end)])
    merged = []
    for a, b in values:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    ranges[:] = merged


def length(ranges):
    return sum(b - a for a, b in ranges)


def audit(path, image_baseline=False):
    # Caller supplies an already completed file; syntax failure is a hard error.
    raw = path.read_bytes()
    source_hash = hashlib.sha256(raw).hexdigest()
    result = json.loads(raw)
    app, network = result["inputs"]["application"], result["inputs"]["network"]
    assert not network.get(
        "routers"
    ), "router service requires a separate explicit trace auditor"
    until = F(str(network["until"]))
    messages = {m["id"]: m for m in app["messages"]}
    tasks = {t["id"]: t for t in app["compute_tasks"]}
    delivered = {k: F(v) for k, v in result["delivered"].items()}
    rows = result["transmissions"]
    by_pn = {}
    last_end = defaultdict(F)
    sent_by_message = defaultdict(list)
    received_by_message = defaultdict(list)
    arrivals_by_message = defaultdict(list)
    physical_events = []
    wire = 0
    serialized = F(0)
    data_packets = 0
    datagram_transmissions = defaultdict(int)
    ack_by_arrival = {}
    for row in rows:
        d, pn = row["direction"], row["pn"]
        identity = (d, pn)
        assert identity not in by_pn, ("duplicate PN", identity)
        by_pn[identity] = row
        start, end = F(row["send_start"]), F(row["send_end"])
        assert start >= last_end[d] and 0 <= start <= until
        assert row["wire_bytes"] == row["quic_bytes"] + 28
        assert end - start == F(8 * row["wire_bytes"]) / F(
            str(network["links"][d]["rate_bps"])
        )
        assert F(row["arrival"]) == end + F(str(network["links"][d]["propagation"]))
        last_end[d] = end
        wire += row["wire_bytes"]
        serialized += row["wire_bytes"] * min(
            F(1), max(F(0), (until - start) / (end - start))
        )
        arrived = row["received_at"] is not None
        if row["dropped"]:
            assert not arrived
        elif F(row["arrival"]) <= until:
            assert arrived
        if arrived:
            assert F(row["received_at"]) == F(row["arrival"]) <= until
            if row["kind"] == "ack":
                key = (d, F(row["received_at"]))
                assert key not in ack_by_arrival
                ack_by_arrival[key] = row
        if row["message_id"] is None:
            assert not row["frames"]
            continue
        data_packets += 1
        message = messages[row["message_id"]]
        assert d == ("up" if message["sender"] == "client" else "down")
        assert start >= F(message["ready_seconds"])
        assert len(row["frames"]) == 1
        frame = row["frames"][0]
        size, offset = frame["length"], row["message_offset"]
        assert (
            0 <= offset < message["bytes"]
            and 0 < size <= 1168
            and offset + size <= message["bytes"]
        )
        assert size + 32 <= row["quic_bytes"] <= 1200
        if network.get("pad_in_flight", True):
            assert row["quic_bytes"] == 1200
        if message["transport"] == "stream":
            assert frame == dict(
                type="stream",
                stream=message["flow_id"],
                offset=message["stream_offset"] + offset,
                length=size,
            )
        else:
            assert offset == 0 and size == message["bytes"]
            assert frame == dict(type="datagram", id=message["id"], length=size)
            datagram_transmissions[message["id"]] += 1
            assert datagram_transmissions[message["id"]] == 1
        add_interval(sent_by_message[message["id"]], offset, offset + size)
        if arrived:
            add_interval(received_by_message[message["id"]], offset, offset + size)
            arrivals_by_message[message["id"]].append(
                (F(row["received_at"]), offset, size)
            )
            physical_events.append(
                (F(row["received_at"]), 0, len(physical_events), "data", row)
            )
        for dep in message["dependencies"]:
            assert dep["id"] in delivered and delivered[dep["id"]] <= start
    # Every sent event must correspond to exactly one actual transmission.
    ack_checks = 0
    for d, events in result["sender_events"].items():
        seen_sent = set()
        for event in events:
            if event["type"] == "sent":
                row = by_pn[(d, event["pn"])]
                assert F(event["at"]) == F(row["send_start"])
                assert (
                    event["sent_bytes"] == row["quic_bytes"]
                    and event["frames"] == row["frames"]
                )
                assert event["pn"] not in seen_sent
                seen_sent.add(event["pn"])
            if event["type"] != "ack":
                continue
            reverse = "down" if d == "up" else "up"
            ack = ack_by_arrival[(reverse, F(event["at"]))]
            if "ack_snapshot" in ack:
                assert event["ranges"] == ack["ack_snapshot"]["ranges"]
            for first, last in event["ranges"]:
                assert 0 <= first <= last
                for pn in range(first, last + 1):
                    target = by_pn[(d, pn)]
                    assert target["received_at"] is not None
                    assert F(target["received_at"]) <= F(ack["send_start"])
                    ack_checks += 1
        assert seen_sent == {pn for direction, pn in by_pn if direction == d}
    # Reconstruct reliable receive buffer and instantaneous DATAGRAM occupancy.
    for index, event in enumerate(result["network_events"]):
        if event["kind"] == "consume":
            physical_events.append((F(event["at"]), 1, index, "consume", event))
    intervals = defaultdict(list)
    consumed = defaultdict(int)
    peaks = {"up": 0, "down": 0}
    prefix_history = defaultdict(list)
    for at, _, _, kind, event in sorted(physical_events, key=lambda v: v[:3]):
        d = event["direction"]
        if kind == "consume":
            key = (d, event["flow"])
            prefix = (
                intervals[key][0][1]
                if intervals[key] and intervals[key][0][0] == 0
                else 0
            )
            assert consumed[key] <= event["upto"] <= prefix
            consumed[key] = event["upto"]
            continue
        message = messages[event["message_id"]]
        frame = event["frames"][0]
        if message["transport"] == "stream":
            key = (d, message["flow_id"])
            add_interval(
                intervals[key], frame["offset"], frame["offset"] + frame["length"]
            )
            prefix = intervals[key][0][1] if intervals[key][0][0] == 0 else 0
            prefix_history[key].append((at, prefix))
        held = sum(length(v) - consumed[k] for k, v in intervals.items() if k[0] == d)
        if message["transport"] == "datagram":
            expired = message["allow_expire"] and at > F(message["deadline_seconds"])
            if expired or held + frame["length"] > network["receive_memory_bytes"][d]:
                continue
            held += frame["length"]
        assert held <= network["receive_memory_bytes"][d]
        peaks[d] = max(peaks[d], held)
    assert peaks == result["peak_receive_memory"]
    for key, message in messages.items():
        if key not in delivered:
            continue
        at = delivered[key]
        assert at <= until and length(received_by_message[key]) == message["bytes"]
        available = []
        for time, offset, size in arrivals_by_message[key]:
            if time <= at:
                add_interval(available, offset, offset + size)
        assert length(available) == message["bytes"]
        if message["transport"] == "stream":
            d = "up" if message["sender"] == "client" else "down"
            history = prefix_history[(d, message["flow_id"])]
            i = bisect_right(history, (at, 2**63)) - 1
            assert (
                i >= 0 and history[i][1] >= message["stream_offset"] + message["bytes"]
            )
    busy = defaultdict(list)
    for work in result["work"]:
        task = tasks[work["id"]]
        start, end = F(work["start"]), F(work["end"])
        assert end - start == F(task["duration_seconds"]) and start >= F(
            task["ready_seconds"]
        )
        assert (work["endpoint"], work["resource"]) == (
            task["endpoint"],
            task["resource"],
        )
        for dep in task["dependencies"]:
            assert (
                dep["endpoint"] == task["endpoint"]
                and dep["id"] in delivered
                and delivered[dep["id"]] <= start
            )
        if work["finished"]:
            assert delivered[work["id"]] == end <= until
        busy[(work["endpoint"], work["resource"])].append((start, end))
    for periods in busy.values():
        periods.sort()
        assert all(a[1] <= b[0] for a, b in zip(periods, periods[1:]))
    offered = sum(m["bytes"] for m in messages.values())
    sent_unique = sum(length(v) for v in sent_by_message.values())
    received_unique = sum(length(v) for v in received_by_message.values())
    delivered_bytes = sum(m["bytes"] for k, m in messages.items() if k in delivered)
    assert wire == result["summary"]["wire_bytes"]
    assert serialized == F(
        result["summary"].get("serialized_wire_bytes_by_horizon", serialized)
    )
    assert received_unique == result["summary"]["unique_received_application_bytes"]
    assert delivered_bytes == result["summary"].get(
        "delivered_application_bytes", delivered_bytes
    )
    assert delivered_bytes <= received_unique <= sent_unique <= offered
    highest = {"up": {}, "down": {}}
    for row in rows:
        for frame in row["frames"]:
            if frame["type"] == "stream":
                flow = frame["stream"]
                highest[row["direction"]][flow] = max(
                    highest[row["direction"]].get(flow, 0),
                    frame["offset"] + frame["length"],
                )
    for direction, flows in highest.items():
        assert result["final_states"][direction]["max_data_consumed"] == sum(
            flows.values()
        )
        for flow, end in flows.items():
            assert (
                result["final_states"][direction]["stream_highest_sent_offsets"][flow]
                == end
            )
    for observer in app["business_observers"]:
        actual = next(b for b in result["businesses"] if b["id"] == observer["id"])
        needed = [dep["id"] for dep in observer["completion_dependencies"]]
        complete = all(identity in delivered for identity in needed)
        assert actual["all_required_delivered"] == complete
        if complete:
            assert F(actual["complete_at"]) == max(
                (delivered[identity] for identity in needed), default=F(0)
            )
        else:
            assert actual["complete_at"] is None
        if observer["kind"] in ("image", "asr"):
            assert actual["complete"] == complete
    screenshot_quality = []
    for observer in app["business_observers"]:
        if observer["kind"] != "screenshot":
            continue
        report = next(b for b in result["businesses"] if b["id"] == observer["id"])
        required = [d["id"] for d in observer["completion_dependencies"]]
        complete = all(k in delivered for k in required)
        at = max((delivered[k] for k in required), default=F(0)) if complete else None
        version = observer["version"]
        for change in observer["version_changes"]:
            assert change["endpoint"] == observer["endpoint"]
            if at is not None and F(change["at_seconds"]) <= at:
                version = change["version"]
        assert report["usable"] == (complete and version == observer["version"])
        screenshot_quality.append(
            dict(
                id=observer["id"], transport_complete=complete, usable=report["usable"]
            )
        )
    audio_quality = []
    for observer in app["business_observers"]:
        if observer["kind"] != "tts":
            continue
        actual = next(b for b in result["businesses"] if b["id"] == observer["id"])
        assert len(actual["blocks"]) == len(observer["blocks"])
        played_seconds = F(0)
        missing_slots = F(0)
        for block, play in zip(observer["blocks"], actual["blocks"]):
            ids = block["message_ids"]
            duration = F(block["duration_seconds"])
            slot = F(block["slot_start_seconds"])
            if play["play_start"] is not None:
                start = F(play["play_start"])
                assert start <= until and all(
                    k in delivered and delivered[k] <= start for k in ids
                )
                assert F(play["scheduled_play_end"]) == start + duration
                assert play["play_end"] == (
                    str(start + duration) if start + duration <= until else None
                )
                played_seconds += min(duration, until - start)
            if observer["playback"] == "slots":
                usable = slot <= until and all(
                    k in delivered and delivered[k] <= slot for k in ids
                )
                assert (play["play_start"] is not None) == usable
                if usable:
                    assert F(play["play_start"]) == slot
                elif slot <= until:
                    missing_slots += min(duration, until - slot)
        if observer["playback"] == "slots":
            assert F(actual["missing_audio_seconds"]) == missing_slots
        audio_quality.append(
            dict(
                id=observer["id"],
                offered_duration_seconds=str(
                    sum(F(b["duration_seconds"]) for b in observer["blocks"])
                ),
                played_seconds_by_horizon=str(played_seconds),
                missing_slot_seconds=(
                    str(missing_slots) if observer["playback"] == "slots" else None
                ),
            )
        )
    if image_baseline:
        assert data_packets == 30800 and offered == 35000000
        assert sent_unique == received_unique == delivered_bytes == 35000000
        assert result["summary"]["all_messages_delivered"]
        assert len(result["work"]) == 1 and F(result["work"][0]["end"]) - F(
            result["work"][0]["start"]
        ) == F(3, 10)
    assert (
        hashlib.sha256(path.read_bytes()).hexdigest() == source_hash
    ), "result changed during audit"
    return dict(
        status="PASS",
        result_file=str(path),
        result_sha256=source_hash,
        transmissions=len(rows),
        data_packets=data_packets,
        ack_covered_PN_checks=ack_checks,
        wire_bytes=wire,
        serialized_wire_bytes_by_horizon=str(serialized),
        offered_application_bytes=offered,
        sent_unique_application_bytes=sent_unique,
        physically_received_unique_application_bytes=received_unique,
        delivered_application_bytes=delivered_bytes,
        screenshot_quality=screenshot_quality,
        audio_quality=audio_quality,
        independently_reconstructed_peak_memory=peaks,
        compute_tasks_checked=len(result["work"]),
        scope="No-router full trace physical/ACK/byte/memory/DAG checks. Does not replay controller math or require all mixed messages usable.",
        checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    parser.add_argument("--image-baseline", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = audit(args.result, args.image_baseline)
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))
