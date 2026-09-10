"""Normalize sealed media DAGs into application inputs; never simulate sending."""

import argparse
from collections import Counter
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def exact(value):
    if isinstance(value, bool):
        raise ValueError("boolean time")
    value = Fraction(str(value))
    if value < 0:
        raise ValueError("negative time")
    return str(value)


def integer(value, minimum=0):
    if type(value) is not int or value < minimum:
        raise ValueError("invalid integer")
    return value


def packet_view(message, packet_payload=1168):
    """Application byte slices only: no PN, send time, ACK or wire overhead."""
    integer(packet_payload, 1)
    size = message["bytes"]
    if message["transport"] == "datagram" and size > packet_payload:
        raise ValueError(
            "DATAGRAM exceeds payload limit; application fragmentation unspecified"
        )
    for start in range(0, size, packet_payload):
        length = min(packet_payload, size - start)
        yield dict(
            message_id=message["id"],
            fragment_index=start // packet_payload,
            message_offset=start,
            bytes=length,
            stream_offset=(
                message["stream_offset"] + start
                if message["transport"] == "stream"
                else None
            ),
            sender=message["sender"],
            receiver=message["receiver"],
            transport=message["transport"],
            flow_id=message["flow_id"],
        )


def normalize(name, source, packet_payload=1168):
    integer(packet_payload, 1)
    p = deepcopy(source)
    packets, raw_tasks = p["packets"], p.get("tasks", [])
    ids = [x["id"] for x in packets + raw_tasks]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate business node")
    endpoints = {"c2s": ("client", "server"), "s2c": ("server", "client")}
    packet_map = {x["id"]: x for x in packets}
    task_map = {x["id"]: x for x in raw_tasks}

    def dependencies(raw, consumer):
        result = []
        for identity in raw:
            if identity in packet_map:
                endpoint = endpoints[packet_map[identity]["direction"]][1]
                kind = "message_delivered"
            elif identity in task_map:
                endpoint = task_map[identity].get("endpoint", "server")
                kind = "task_completed"
            else:
                raise ValueError("unknown dependency " + identity)
            if endpoint != consumer:
                raise ValueError(
                    "cross-end dependency needs an actual notification message"
                )
            result.append(dict(id=identity, event=kind, endpoint=endpoint))
        return result

    tasks = []
    for index, task in enumerate(raw_tasks):
        endpoint = task.get("endpoint", "server")
        tasks.append(
            dict(
                id=task["id"],
                endpoint=endpoint,
                resource=task.get("resource", "server"),
                duration_seconds=exact(task["duration"]),
                ready_seconds=exact(task.get("ready", 0)),
                dependencies=dependencies(task.get("dependencies", []), endpoint),
                priority=task.get("priority", 0),
                source_order=index,
                cancel_tag=task.get("cancel_tag"),
                timing_basis="existing declared service duration; not measured model throughput",
            )
        )
    messages, loss_assumptions = [], []
    ends = {}
    for index, packet in enumerate(packets):
        sender, receiver = endpoints[packet["direction"]]
        reliable = packet.get("reliable", True)
        if type(reliable) is not bool:
            raise ValueError("reliability must be boolean")
        size, offset = integer(packet["payload_bytes"], 1), integer(packet["offset"])
        key = (packet["direction"], packet["stream"])
        if offset != ends.get(key, 0):
            raise ValueError("noncontiguous original flow offset")
        ends[key] = offset + size
        message = dict(
            id=packet["id"],
            sender=sender,
            receiver=receiver,
            flow_id=packet["stream"],
            transport="stream" if reliable else "datagram",
            bytes=size,
            stream_offset=offset if reliable else None,
            application_offset=offset,
            ready_seconds=exact(packet.get("ready", 0)),
            dependencies=dependencies(packet.get("dependencies", []), sender),
            priority=packet.get("priority", 0),
            source_order=index,
            deadline_seconds=(
                None if packet.get("deadline") is None else exact(packet["deadline"])
            ),
            allow_expire=packet.get("allow_expire", False),
            cancel_tag=packet.get("cancel_tag"),
            on_delivery_cancel_tags=deepcopy(packet.get("cancel_targets", [])),
        )
        if reliable and message["allow_expire"]:
            raise ValueError("reliable bytes cannot silently expire")
        if message["allow_expire"] and message["deadline_seconds"] is None:
            raise ValueError("expiry requires deadline")
        count = (size + packet_payload - 1) // packet_payload
        if not reliable and count != 1:
            raise ValueError("oversized atomic datagram")
        message["packetization"] = dict(
            payload_limit_bytes=packet_payload,
            fragment_count=count,
            final_fragment_bytes=size - (count - 1) * packet_payload,
            coalesce_across_messages=False,
        )
        messages.append(message)
        legacy = {k: packet[k] for k in ("drop_first", "recovery_ready") if k in packet}
        if legacy:
            loss_assumptions.append(dict(message_id=packet["id"], original=legacy))
    # Validate DAG without calculating any ready/completion timestamp.
    graph = {x["id"]: [d["id"] for d in x["dependencies"]] for x in tasks + messages}
    visiting, visited = set(), set()

    def visit(identity):
        if identity in visiting:
            raise ValueError("dependency cycle")
        if identity in visited:
            return
        visiting.add(identity)
        for dependency in graph[identity]:
            visit(dependency)
        visiting.remove(identity)
        visited.add(identity)

    for identity in graph:
        visit(identity)
    business = []
    for raw in p.get("businesses", []):
        item = deepcopy(raw)
        required = item.pop("required", [])
        required += [
            identity
            for block in item.get("blocks", [])
            for identity in block["packets"]
        ]
        receivers = {endpoints[packet_map[k]["direction"]][1] for k in required}
        if len(receivers) != 1:
            raise ValueError("business endpoint is ambiguous")
        endpoint = receivers.pop()
        item["endpoint"] = endpoint
        item["completion_dependencies"] = dependencies(required, endpoint)
        if "blocks" in item:
            item["blocks"] = [
                dict(
                    message_ids=b["packets"],
                    duration_seconds=exact(b["duration"]),
                    slot_start_seconds=exact(b["slot_start"]),
                )
                for b in item["blocks"]
            ]
        item["version_changes"] = [
            dict(endpoint=endpoint, at_seconds=exact(v["at"]), version=v["version"])
            for v in item.get("version_changes", [])
        ]
        business.append(item)
    totals = Counter()
    for message in messages:
        totals[message["sender"] + "_to_" + message["receiver"]] += message["bytes"]
    return dict(
        schema_version=1,
        id=name,
        messages=messages,
        compute_tasks=tasks,
        business_observers=business,
        scheduling=dict(
            send=p.get("scheduler", "fifo"),
            compute=p.get("compute_scheduler", "fifo"),
            compute_nonpreemptive=True,
            resource_capacity_tasks=1,
        ),
        links={
            direction: dict(
                rate_bits_per_second=p[direction + "_bits_per_second"],
                propagation_seconds=exact(p[direction + "_propagation_seconds"]),
            )
            for direction in ("c2s", "s2c")
        },
        connection_ready_seconds=exact(p.get("connection_ready", 0)),
        external_legacy_assumptions=dict(
            teaching_network={
                k: v
                for k, v in p.items()
                if k
                not in {
                    "packets",
                    "tasks",
                    "businesses",
                    "scheduler",
                    "compute_scheduler",
                    "connection_ready",
                    "c2s_bits_per_second",
                    "s2c_bits_per_second",
                    "c2s_propagation_seconds",
                    "s2c_propagation_seconds",
                }
            },
            selected_loss_and_recovery=loss_assumptions,
            action="Do not map credit to cwnd, legacy header to MTU, or recovery_ready to PTO. Choose real network inputs explicitly.",
        ),
        accounting=dict(
            application_bytes_by_direction=dict(totals),
            application_bytes=sum(totals.values()),
            message_count=len(messages),
            task_count=len(tasks),
            fragment_count=sum(m["packetization"]["fragment_count"] for m in messages),
        ),
    )


def load_sealed():
    lock = json.loads((ROOT / "inputs.lock.json").read_text())
    for row in lock:
        raw = (ROOT / row["file"]).read_bytes()
        if len(raw) != row["bytes"] or hashlib.sha256(raw).hexdigest() != row["sha256"]:
            raise ValueError("sealed input changed: " + row["file"])
    return json.loads(
        (ROOT.parent / "shared-media-transport/scenarios.json").read_text()
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--scenario", help="Exact sealed scenario; omit for all sixteen"
    )
    parser.add_argument("--packet-payload", type=int, default=1168)
    parser.add_argument(
        "--packets",
        action="store_true",
        help="Expand byte slices, not simulated packets",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    sources = load_sealed()
    if args.scenario:
        sources = {args.scenario: sources[args.scenario]}
    result = {
        name: normalize(name, value, args.packet_payload)
        for name, value in sources.items()
    }
    if args.packets:
        for value in result.values():
            value["packet_view"] = [
                p
                for message in value["messages"]
                for p in packet_view(message, args.packet_payload)
            ]
    text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
