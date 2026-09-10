"""Finite teaching transport: shared credit, delivery order and business deadlines."""

from fractions import Fraction as F
import heapq
import json
from ..sources import provenance, read_source


def replay_delivery(packets, arrivals, mode):
    """Replay only delivery order over immutable successful network arrivals."""
    if mode not in ("connection", "per_stream"):
        raise ValueError("delivery mode")
    delivered = {}
    for packet in packets:
        arrival = arrivals.get(packet["id"])
        if arrival is None:
            continue
        if packet.get("allow_expire", False) and F(arrival) > F(
            str(packet["deadline"])
        ):
            continue
        predecessors = []
        for previous in packets:
            if previous is packet:
                break
            if (
                packet.get("reliable", True)
                and previous.get("reliable", True)
                and previous["direction"] == packet["direction"]
                and (mode == "connection" or previous["stream"] == packet["stream"])
            ):
                predecessors.append(previous["id"])
        if all(k in delivered for k in predecessors):
            delivered[packet["id"]] = str(
                max([F(arrival)] + [F(delivered[k]) for k in predecessors])
            )
    return delivered


def calculate(inputs=None):
    p = json.loads(json.dumps(example() if inputs is None else inputs))
    p.setdefault("compute_scheduler", "fifo")
    if p["compute_scheduler"] not in ("fifo", "priority"):
        raise ValueError("unknown compute scheduler")
    selected_revisions = {
        "RFC9221",
        "RFC9000",
        "RFC9002",
        "RFC9114",
        "RFC8836",
        "RFC3550",
    }
    available = provenance("shared-media-rfc") + provenance("protocol-rfc")
    sources = [row for row in available if row["revision"] in selected_revisions]
    if len(sources) != 6 or {row["revision"] for row in sources} != selected_revisions:
        raise ValueError("shared media requires six pinned official RFC sources")
    for source in sources:
        read_source(source["file"])
    rates = {d: F(str(p[d + "_bits_per_second"])) for d in ("c2s", "s2c")}
    delays = {d: F(str(p[d + "_propagation_seconds"])) for d in rates}
    ready = F(str(p.get("connection_ready", 0)))
    if min(rates.values()) <= 0 or min(delays.values()) < 0 or ready < 0:
        raise ValueError("invalid timing")
    if p["scheduler"] not in ("fifo", "priority") or p["delivery_mode"] not in (
        "connection",
        "per_stream",
    ):
        raise ValueError("unknown policy")
    for name in (
        "shared_credit_bytes",
        "reliable_receive_credit_bytes",
        "stream_credit_bytes",
        "ack_bytes",
    ):
        if type(p[name]) is not int or p[name] <= 0:
            raise ValueError("positive integer " + name)
    if type(p["header_bytes"]) is not int or p["header_bytes"] < 0:
        raise ValueError("header bytes")
    packets = p["packets"]
    tasks = p.get("tasks", [])
    if len(packets) + len(tasks) > 20000:
        raise ValueError("node limit 20000")
    ids = [n["id"] for n in packets + tasks]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate node id")
    idset = set(ids)
    node = {n["id"]: n for n in packets + tasks}
    previous_end = {}
    for index, x in enumerate(packets):
        x.setdefault("dependencies", [])
        x.setdefault("ready", 0)
        x.setdefault("priority", 0)
        x.setdefault("reliable", True)
        x.setdefault("allow_expire", False)
        x.setdefault("deadline", None)
        x.setdefault("drop_first", False)
        x.setdefault("recovery_ready", None)
        x.setdefault("cancel_targets", [])
        if (
            x["direction"] not in rates
            or type(x["payload_bytes"]) is not int
            or x["payload_bytes"] <= 0
            or type(x["offset"]) is not int
            or x["offset"] < 0
        ):
            raise ValueError("invalid packet interval")
        if any(
            type(x[k]) is not bool for k in ("reliable", "allow_expire", "drop_first")
        ):
            raise ValueError("policy booleans")
        if x["reliable"] and x["allow_expire"]:
            raise ValueError("reliable data cannot expire")
        if x["allow_expire"] and x["deadline"] is None:
            raise ValueError("expiry requires deadline")
        if not x["reliable"] and x["recovery_ready"] is not None:
            raise ValueError("unreliable data cannot recover")
        if not x["drop_first"] and x["recovery_ready"] is not None:
            raise ValueError("recovery without selected loss")
        if F(str(x["ready"])) < 0 or (
            x["deadline"] is not None and F(str(x["deadline"])) < 0
        ):
            raise ValueError("negative time")
        if x["recovery_ready"] is not None and F(str(x["recovery_ready"])) < 0:
            raise ValueError("negative recovery")
        key = (x["direction"], x["stream"])
        if x["offset"] != previous_end.get(key, 0):
            raise ValueError("stream intervals must be contiguous in input order")
        previous_end[key] = x["offset"] + x["payload_bytes"]
    for x in tasks:
        x.setdefault("dependencies", [])
        x.setdefault("ready", 0)
        x.setdefault("priority", 0)
        x.setdefault("resource", "server")
        x.setdefault("endpoint", "server")
        if x["endpoint"] not in ("client", "server"):
            raise ValueError("unknown task endpoint")
        if F(str(x["duration"])) < 0 or F(str(x["ready"])) < 0:
            raise ValueError("negative work")
    visiting = set()
    visited = set()

    def visit(k):
        if k in visiting:
            raise ValueError("cyclic dependency")
        if k in visited:
            return
        visiting.add(k)
        for dep in node[k]["dependencies"]:
            if dep not in idset:
                raise ValueError("unknown dependency")
            visit(dep)
        visiting.remove(k)
        visited.add(k)

    for k in ids:
        visit(k)

    def producer_endpoint(x):
        return (
            ("server" if x["direction"] == "c2s" else "client")
            if "direction" in x
            else x["endpoint"]
        )

    def consumer_endpoint(x):
        return (
            ("client" if x["direction"] == "c2s" else "server")
            if "direction" in x
            else x["endpoint"]
        )

    for x in packets + tasks:
        for dep in x["dependencies"]:
            if producer_endpoint(node[dep]) != consumer_endpoint(x):
                raise ValueError(
                    "cross-endpoint dependency needs an explicit network message"
                )

    packet_ids = {x["id"] for x in packets}
    for b in p.get("businesses", []):
        if b["kind"] not in ("image", "asr", "screenshot", "tts"):
            raise ValueError("unknown business kind")
        if b["kind"] == "tts":
            if b["playback"] not in ("reliable", "slots") or not b["blocks"]:
                raise ValueError("invalid playback policy")
            last_slot_end = None
            for block in b["blocks"]:
                if (
                    not block["packets"]
                    or any(k not in packet_ids for k in block["packets"])
                    or F(str(block["duration"])) <= 0
                ):
                    raise ValueError("invalid playback block")
                if b["playback"] == "slots":
                    start = F(str(block["slot_start"]))
                    if start < 0 or (
                        last_slot_end is not None and start < last_slot_end
                    ):
                        raise ValueError("overlapping or unordered playback slots")
                    last_slot_end = start + F(str(block["duration"]))
        elif not b["required"] or any(k not in packet_ids for k in b["required"]):
            raise ValueError("invalid required business packets")
        if any(k not in packet_ids for k in b.get("preview_required", [])):
            raise ValueError("unknown preview packet")
        references = (
            [k for block in b["blocks"] for k in block["packets"]]
            if b["kind"] == "tts"
            else b["required"]
        )
        receivers = {
            producer_endpoint(node[k])
            for k in references + b.get("preview_required", [])
        }
        if len(receivers) != 1:
            raise ValueError(
                "business completion must be known at a single receiving endpoint"
            )
        if b["kind"] == "image" and any(
            not node[k]["reliable"] or node[k]["allow_expire"] for k in b["required"]
        ):
            raise ValueError("complete image requires reliable non-expiring packets")
        if b["kind"] == "screenshot" and receivers != {"client"}:
            raise ValueError("screenshot version usability is evaluated at the client")
        if b["kind"] == "screenshot":
            if not isinstance(b["version"], str) or not b["version"]:
                raise ValueError("screenshot version must be nonempty string")
            times = [F(str(c["at"])) for c in b.get("version_changes", [])]
            if any(t < 0 for t in times) or any(
                y <= x for x, y in zip(times, times[1:])
            ):
                raise ValueError("version changes must be strictly ordered")
    for x in packets + tasks:
        if type(x["priority"]) is not int:
            raise ValueError("priority must be integer")
    predecessors = {}
    previous = {}
    for x in packets:
        key = (
            x["direction"],
            None if p["delivery_mode"] == "connection" else x["stream"],
        )
        predecessors[x["id"]] = previous.get(key) if x["reliable"] else None
        if x["reliable"]:
            previous[key] = x["id"]
    now = F(0)
    serial = 0
    queue_order = 0
    events = []
    trace = []
    acks = []
    work = []
    cancellations = []
    credit_events = []
    states = {
        x["id"]: {
            "attempts": 0,
            "received": None,
            "delivered": None,
            "expired": False,
            "ready_order": None,
            "acked": False,
            "recovery_due": False,
        }
        for x in packets
    }
    taskstate = {x["id"]: "waiting" for x in tasks}
    task_order = {}
    done = {}
    cancelled_tags = {"client": set(), "server": set()}
    busy = {d: False for d in rates}
    cpu_busy = {}
    credit = {d: 0 for d in rates}
    receive_credit = {d: 0 for d in rates}
    stream_credit = {}
    ack_queue = {d: [] for d in rates}

    def event(t, callback, priority=0):
        nonlocal serial
        serial += 1
        heapq.heappush(events, (t, priority, serial, callback))

    def wake():
        event(now, dispatch, 3)

    def endpoint(x):
        return (
            ("client" if x["direction"] == "c2s" else "server")
            if "direction" in x
            else x.get("endpoint", "server")
        )

    def cancelled(x):
        return x.get("cancel_tag") in cancelled_tags[endpoint(x)]

    def dependencies_ready(x):
        return all(k in done for k in x["dependencies"]) and F(str(x["ready"])) <= now

    def deliver():
        changed = True
        while changed:
            changed = False
            for i, x in enumerate(packets):
                state = states[x["id"]]
                if (
                    state["received"] is None
                    or state["delivered"] is not None
                    or state["expired"]
                ):
                    continue
                predecessor = predecessors[x["id"]]
                if predecessor is not None and states[predecessor]["delivered"] is None:
                    continue
                state["delivered"] = str(now)
                done[x["id"]] = now
                for tag in x["cancel_targets"]:
                    receiver = "server" if x["direction"] == "c2s" else "client"
                    cancelled_tags[receiver].add(tag)
                    cancellations.append(
                        {
                            "at": str(now),
                            "packet": x["id"],
                            "cancel_tag": tag,
                            "receiver": receiver,
                        }
                    )

                changed = True

    def ack_arrival(x):
        state = states[x["id"]]
        d = x["direction"]
        key = (d, x["stream"])
        released = 0
        if not state["acked"]:
            state["acked"] = True
            released = x["payload_bytes"]
            credit[d] -= released
            if x["reliable"]:
                receive_credit[d] -= released
                stream_credit[key] -= released
        credit_events.append(
            {
                "at": str(now),
                "event": "ack_received",
                "packet": x["id"],
                "released_bytes": released,
                "direction": d,
                "shared_outstanding": credit[d],
                "reliable_receive_outstanding": receive_credit[d],
            }
        )
        wake()

    def arrived(x, attempt):
        state = states[x["id"]]
        if attempt == 1 and x["drop_first"]:
            return
        if state["received"] is None:
            state["received"] = str(now)
        reverse = "s2c" if x["direction"] == "c2s" else "c2s"
        nonlocal queue_order
        queue_order += 1
        ack_queue[reverse].append(
            {"packet": x, "ready": str(now), "order": queue_order}
        )
        deliver()
        wake()

    def tx_data(x, recovery=False):
        state = states[x["id"]]
        d = x["direction"]
        key = (d, x["stream"])
        if not recovery:
            credit[d] += x["payload_bytes"]
            if x["reliable"]:
                receive_credit[d] += x["payload_bytes"]
                stream_credit[key] = stream_credit.get(key, 0) + x["payload_bytes"]
        state["attempts"] += 1
        attempt = state["attempts"]
        busy[d] = True
        end = now + F(8 * (x["payload_bytes"] + p["header_bytes"]), 1) / rates[d]
        arrival = end + delays[d]
        trace.append(
            {
                "kind": "data",
                "packet": x["id"],
                "stream": x["stream"],
                "direction": d,
                "offset": x["offset"],
                "end_offset": x["offset"] + x["payload_bytes"],
                "payload_bytes": x["payload_bytes"],
                "wire_bytes": x["payload_bytes"] + p["header_bytes"],
                "attempt": attempt,
                "start": str(now),
                "end": str(end),
                "arrival": str(arrival),
                "lost": attempt == 1 and x["drop_first"],
            }
        )
        credit_events.append(
            {
                "at": str(now),
                "event": "send",
                "packet": x["id"],
                "direction": d,
                "reserved_bytes": 0 if recovery else x["payload_bytes"],
                "shared_outstanding": credit[d],
                "reliable_receive_outstanding": receive_credit[d],
            }
        )

        def finish():
            busy[d] = False
            wake()

        event(end, finish, 1)
        event(arrival, lambda: arrived(x, attempt))
        wake()

    def tx_ack(a, d):
        busy[d] = True
        end = now + F(8 * p["ack_bytes"], 1) / rates[d]
        arrival = end + delays[d]
        record = {
            "kind": "ack",
            "packet": a["packet"]["id"],
            "direction": d,
            "wire_bytes": p["ack_bytes"],
            "start": str(now),
            "end": str(end),
            "arrival": str(arrival),
        }
        trace.append(record)
        acks.append(record)

        def finish():
            busy[d] = False
            wake()

        event(end, finish, 1)
        event(arrival, lambda: ack_arrival(a["packet"]))

    def dispatch():
        nonlocal queue_order
        for x in packets:
            state = states[x["id"]]
            if state["ready_order"] is None and dependencies_ready(x):
                queue_order += 1
                state["ready_order"] = queue_order
        for x in tasks:
            if taskstate[x["id"]] == "waiting" and cancelled(x):
                taskstate[x["id"]] = "cancelled"
            if dependencies_ready(x) and x["id"] not in task_order:
                queue_order += 1
                task_order[x["id"]] = queue_order
        eligible_tasks = [
            x
            for x in tasks
            if taskstate[x["id"]] == "waiting" and dependencies_ready(x)
        ]
        eligible_tasks.sort(
            key=lambda x: (
                (-x["priority"], task_order[x["id"]])
                if p["compute_scheduler"] == "priority"
                else (task_order[x["id"]],)
            )
        )
        for x in eligible_tasks:
            if cancelled(x):
                taskstate[x["id"]] = "cancelled"
                continue
            if cpu_busy.get((x["endpoint"], x["resource"]), False):
                continue
            taskstate[x["id"]] = "running"
            cpu_busy[(x["endpoint"], x["resource"])] = True
            end = now + F(str(x["duration"]))
            record = {
                "id": x["id"],
                "resource": x["resource"],
                "endpoint": x["endpoint"],
                "start": str(now),
                "end": str(end),
            }
            work.append(record)

            def finish_task(x=x, record=record):
                taskstate[x["id"]] = "complete"
                cpu_busy[(x["endpoint"], x["resource"])] = False
                done[x["id"]] = now
                record["cancel_received_while_running"] = cancelled(x)
                wake()

            event(end, finish_task, 1)
        if now < ready:
            return
        for d in rates:
            if busy[d]:
                continue
            choices = []
            for a in ack_queue[d]:
                choices.append((a["order"], 10**9, "ack", a))
            for x in packets:
                state = states[x["id"]]
                if (
                    x["direction"] != d
                    or cancelled(x)
                    or state["expired"]
                    or state["ready_order"] is None
                ):
                    continue
                recovery = (
                    state["attempts"] == 1
                    and x["drop_first"]
                    and state["recovery_due"]
                    and state["received"] is None
                )
                if state["attempts"] and not recovery:
                    continue
                if not recovery and (
                    credit[d] + x["payload_bytes"] > p["shared_credit_bytes"]
                    or (
                        x["reliable"]
                        and (
                            receive_credit[d] + x["payload_bytes"]
                            > p["reliable_receive_credit_bytes"]
                            or stream_credit.get((d, x["stream"]), 0)
                            + x["payload_bytes"]
                            > p["stream_credit_bytes"]
                        )
                    )
                ):
                    continue
                choices.append(
                    (
                        state["ready_order"],
                        x["priority"],
                        "recovery" if recovery else "data",
                        x,
                    )
                )
            if not choices:
                continue
            selected = min(
                choices,
                key=lambda row: (
                    (-row[1], row[0]) if p["scheduler"] == "priority" else (row[0],)
                ),
            )
            if selected[2] == "ack":
                ack_queue[d].remove(selected[3])
                tx_ack(selected[3], d)
            else:
                tx_data(selected[3], selected[2] == "recovery")

    for x in packets:
        event(F(str(x["ready"])), wake)
        if x["allow_expire"]:

            def expire(x=x):
                state = states[x["id"]]
                if state["delivered"] is None:
                    state["expired"] = True
                wake()

            event(F(str(x["deadline"])), expire, 2)
        if x["recovery_ready"] is not None:

            def recovery(x=x):
                states[x["id"]]["recovery_due"] = True
                wake()

            event(F(str(x["recovery_ready"])), recovery)
    for x in tasks:
        event(F(str(x["ready"])), wake)
    event(ready, wake)
    while events:
        now, _, _, callback = heapq.heappop(events)
        callback()
    business = []
    for b in p.get("businesses", []):
        row = {"id": b["id"], "kind": b["kind"]}
        if b["kind"] == "tts":
            previous = None
            first = None
            stall = F(0)
            missing = F(0)
            plays = []
            for block in b["blocks"]:
                values = [states[k]["delivered"] for k in block["packets"]]
                arrival = (
                    max(map(F, values)) if all(v is not None for v in values) else None
                )
                duration = F(str(block["duration"]))
                if b["playback"] == "slots":
                    start = F(str(block["slot_start"]))
                    available = arrival is not None and arrival <= start
                    if not available:
                        missing += duration
                else:
                    if arrival is None:
                        break
                    start = max(arrival, previous) if previous is not None else arrival
                    available = True
                    if previous is not None:
                        stall += start - previous
                end = start + duration
                previous = end
                if available and first is None:
                    first = start
                plays.append(
                    {
                        "arrival": str(arrival) if arrival is not None else None,
                        "start": str(start),
                        "end": str(end),
                        "played": available,
                    }
                )
            played_count = sum(block["played"] for block in plays)
            row.update(
                business_status=(
                    "complete"
                    if played_count == len(b["blocks"])
                    else (
                        "timeline_complete_with_missing"
                        if b["playback"] == "slots"
                        else "partial_waiting_for_block"
                    )
                ),
                played_blocks=played_count,
                missing_blocks=sum(not block["played"] for block in plays),
                unresolved_blocks=len(b["blocks"]) - len(plays),
                all_required_delivered=all(
                    states[k]["delivered"] is not None
                    for block in b["blocks"]
                    for k in block["packets"]
                ),
                complete_playback=played_count == len(b["blocks"]),
                first_play=str(first) if first is not None else None,
                playback_end=str(previous) if previous is not None else None,
                stall_seconds=str(stall),
                missing_seconds=str(missing),
                blocks=plays,
            )
        else:
            values = [states[k]["delivered"] for k in b["required"]]
            completion = (
                max(map(F, values)) if all(v is not None for v in values) else None
            )
            usable = completion is not None
            if b["kind"] == "screenshot" and completion is not None:
                version = b["version"]
                for change in b.get("version_changes", []):
                    if F(str(change["at"])) <= completion:
                        version = change["version"]
                usable = version == b["version"]
            row.update(
                complete=str(completion) if completion is not None else None,
                usable=usable,
                business_status=(
                    "complete"
                    if usable
                    else "stale_version" if completion is not None else "incomplete"
                ),
            )
            if b.get("preview_required"):
                values = [states[k]["delivered"] for k in b["preview_required"]]
                row["preview_complete"] = (
                    str(max(map(F, values)))
                    if all(v is not None for v in values)
                    else None
                )
                row["preview_quality"] = b.get(
                    "preview_quality", "declared preview, not full-quality output"
                )

        business.append(row)
    packet_results = []
    for x in packets:
        state = states[x["id"]]
        row = dict(id=x["id"], **state)
        row["expiry_stage"] = (
            ("unsent" if not state["attempts"] else "sent")
            if state["expired"]
            else None
        )
        row["deadline_met"] = state["delivered"] is not None and (
            x["deadline"] is None or F(state["delivered"]) <= F(str(x["deadline"]))
        )
        row["cancelled_before_send"] = cancelled(x) and not state["attempts"]
        packet_results.append(row)
    unfinished_details = []
    for x in packets:
        state = states[x["id"]]
        if state["delivered"] is not None or state["expired"] or cancelled(x):
            continue
        if state["received"] is not None:
            reason = "delivery_order_predecessor_missing"
        elif state["attempts"] and x["drop_first"]:
            reason = "selected_loss_without_remaining_recovery_or_feedback"
        elif not all(dep in done for dep in x["dependencies"]):
            reason = "business_dependency_not_complete"
        else:
            reason = "sender_visible_shared_or_reliable_credit_insufficient"
        unfinished_details.append({"packet": x["id"], "reason": reason})
    arrivals = {
        k: s["received"] for k, s in states.items() if s["received"] is not None
    }
    return {
        "calculation": "shared-media-finite-teaching-transport",
        "inputs": p,
        "reference_sources": sources,
        "transmissions": trace,
        "packets": packet_results,
        "credit_events": credit_events,
        "work": work,
        "cancellations": cancellations,
        "businesses": business,
        "task_status": taskstate,
        "delivery_only_replay": {
            mode: replay_delivery(packets, arrivals, mode)
            for mode in ("connection", "per_stream")
        },
        "summary": {
            "evaluated_business_count": len(business),
            "all_businesses_usable": (
                all(b["business_status"] == "complete" for b in business)
                if business
                else None
            ),
            "all_reliable_packets_delivered": all(
                states[x["id"]]["delivered"] is not None
                for x in packets
                if x["reliable"]
            ),
            "data_wire_bytes": sum(
                t["wire_bytes"] for t in trace if t["kind"] == "data"
            ),
            "ack_wire_bytes": sum(t["wire_bytes"] for t in trace if t["kind"] == "ack"),
            "unique_received_payload_bytes": sum(
                x["payload_bytes"]
                for x in packets
                if states[x["id"]]["received"] is not None
            ),
            "unique_delivered_payload_bytes": sum(
                x["payload_bytes"]
                for x in packets
                if states[x["id"]]["delivered"] is not None
            ),
            "shared_outstanding_bytes": credit,
            "last_event": str(now),
        },
        "unfinished_details": unfinished_details,
        "unfinished": [
            x["id"]
            for x in packets
            if states[x["id"]]["delivered"] is None
            and not states[x["id"]]["expired"]
            and not cancelled(x)
        ],
        "limitations": [
            "Teaching packet-ID credit and declared one-shot recovery; not TCP/QUIC cwnd/MAX_DATA/PTO.",
            "ACK means transport receipt, not playback; receive staging consumes into a separately unbounded reassembly store.",
            "Unreliable packets share send credit but not reliable receive/stream credit; lost packets without feedback retain send credit.",
            "Running work and in-flight packets cannot be cancelled; cancellation affects only local future starts after signal arrival.",
        ],
    }


def example():
    return {
        "scheduler": "fifo",
        "delivery_mode": "per_stream",
        "c2s_bits_per_second": 8,
        "s2c_bits_per_second": 8,
        "c2s_propagation_seconds": 1,
        "s2c_propagation_seconds": 1,
        "header_bytes": 0,
        "ack_bytes": 1,
        "shared_credit_bytes": 100,
        "reliable_receive_credit_bytes": 100,
        "stream_credit_bytes": 100,
        "packets": [
            {
                "id": "B0",
                "stream": "B",
                "direction": "c2s",
                "offset": 0,
                "payload_bytes": 1,
                "drop_first": True,
                "recovery_ready": 5,
            },
            {
                "id": "A0",
                "stream": "A",
                "direction": "c2s",
                "offset": 0,
                "payload_bytes": 1,
                "deadline": 4,
            },
            {
                "id": "B1",
                "stream": "B",
                "direction": "c2s",
                "offset": 1,
                "payload_bytes": 1,
            },
        ],
        "businesses": [
            {"id": "image", "kind": "image", "required": ["B0", "B1"]},
            {"id": "audio", "kind": "asr", "required": ["A0"]},
        ],
    }


def markdown(result):
    """Present business quality, credit and event accounting before the full trace."""
    p = result["inputs"]
    lines = [
        "# 共享媒体有限教学传输",
        "",
        "声明的串行块、信用与单次恢复模型，不是 TCP／QUIC 协议栈或实测推理／播放性能。",
        "",
        "## 独立调度与信用输入",
        "",
        "| 参数 | 声明值 |",
        "| --- | --- |",
    ]
    fields = (
        "scheduler",
        "compute_scheduler",
        "delivery_mode",
        "shared_credit_bytes",
        "reliable_receive_credit_bytes",
        "stream_credit_bytes",
        "header_bytes",
        "ack_bytes",
    )
    lines.extend("| " + key + " | `" + str(p[key]) + "` |" for key in fields)
    lines.extend(
        [
            "",
            "网络调度与计算调度分开。所有数据共享发送信用；不可靠媒体不占可靠接收／流信用。实际 ACK 只说明运输收到，不代表应用播放。",
            "",
            "## 业务可用性与播放质量",
            "",
        ]
    )
    for business in result["businesses"]:
        lines.extend(
            [
                "### " + business["id"] + "（" + business["kind"] + "）",
                "",
                "| 指标 | 值 |",
                "| --- | --- |",
            ]
        )
        for key, value in business.items():
            if key in ("id", "kind", "blocks"):
                continue
            lines.append(
                "| " + key + " | `" + json.dumps(value, ensure_ascii=False) + "` |"
            )
        if "blocks" in business:
            lines.extend(
                [
                    "",
                    "| 块 | 到达（s） | 播放开始（s） | 播放结束（s） | 实际播放 |",
                    "| ---: | ---: | ---: | ---: | --- |",
                ]
            )
            for index, block in enumerate(business["blocks"]):
                lines.append(
                    "| "
                    + str(index)
                    + " | "
                    + str(block["arrival"])
                    + " | "
                    + block["start"]
                    + " | "
                    + block["end"]
                    + " | "
                    + str(block["played"])
                    + " |"
                )
        lines.append("")
    if not result["businesses"]:
        lines.extend(["本场景只检查运输条件，没有声明完整业务。", ""])
    lines.extend(["## 字节与未完成原因", "", "| 数量 | 值 |", "| --- | --- |"])
    lines.extend(
        "| " + key + " | `" + json.dumps(value, ensure_ascii=False) + "` |"
        for key, value in result["summary"].items()
    )
    lines.extend(
        [
            "",
            "事件队列结束或 unfinished 为空不能代替业务完成；旧截图、缺音、取消输出分别保留状态。",
            "",
        ]
    )
    lines.extend(
        "- `" + row["packet"] + "`：" + row["reason"]
        for row in result["unfinished_details"]
    )
    lines.extend(
        [
            "",
            "## 非抢占工作与应用取消",
            "",
            "| 工作 | 执行端／资源 | 开始（s） | 结束（s） | 运行中获知取消 |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    lines.extend(
        "| "
        + row["id"]
        + " | "
        + row["endpoint"]
        + "/"
        + row["resource"]
        + " | "
        + row["start"]
        + " | "
        + row["end"]
        + " | "
        + str(row["cancel_received_while_running"])
        + " |"
        for row in result["work"]
    )
    lines.extend(
        [
            "",
            "取消信号经过实际网络与可靠顺序交付后只影响接收端。已开始计算和发送保留。",
            "",
        ]
    )
    lines.extend(
        "- "
        + row["at"]
        + " s：`"
        + row["receiver"]
        + "` 收到应用控制 `"
        + row["packet"]
        + "`，取消 `"
        + row["cancel_tag"]
        + "`。"
        for row in result["cancellations"]
    )
    lines.extend(["", "## 适用范围与固定来源", ""])
    lines.extend("- " + text for text in result["limitations"])
    lines.extend(
        "- [" + row["revision"] + "](" + row["url"] + ")：`" + row["sha256"] + "`。"
        for row in result["reference_sources"]
    )
    lines.extend(
        [
            "",
            "## 完整输入、逐包轨迹与固定轨迹交付重放",
            "",
            "```json",
            json.dumps(result, ensure_ascii=False, indent=2),
            "```",
            "",
        ]
    )
    return "\n".join(lines)
