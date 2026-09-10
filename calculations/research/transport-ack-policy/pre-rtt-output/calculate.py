"""Incremental confirmed-path network candidate, declared immediate ACK policy."""

from fractions import Fraction as F
from collections import deque
import argparse
import copy
import heapq
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for dependency in json.loads((ROOT / "dependencies.lock.json").read_text()):
    payload = (ROOT / dependency["file"]).read_bytes()
    if (
        len(payload) != dependency["bytes"]
        or hashlib.sha256(payload).hexdigest() != dependency["sha256"]
    ):
        raise ValueError("frozen network dependency changed: " + dependency["file"])
spec = importlib.util.spec_from_file_location(
    "closed_sender", ROOT.parent / "transport-controller-loop/sender.py"
)
sender = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sender)
pacer_spec = importlib.util.spec_from_file_location(
    "controller_pacer", ROOT.parent / "transport-controller-loop/pacer.py"
)
pacer_module = importlib.util.module_from_spec(pacer_spec)
pacer_spec.loader.exec_module(pacer_module)


receiver_spec = importlib.util.spec_from_file_location(
    "ack_receiver", ROOT / "receiver.py"
)
receiver_module = importlib.util.module_from_spec(receiver_spec)
receiver_spec.loader.exec_module(receiver_module)


def validate_inputs(p):
    allowed = {
        "upload_bytes",
        "response_bytes",
        "model_seconds",
        "until",
        "links",
        "routers",
        "sender",
        "packet_payload",
        "ack_policy",
        "receive_window",
        "drop_packets",
        "consume_delay",
        "explicit_consumption",
        "ack_bytes",
        "pacer_interval",
        "controller",
        "pad_in_flight",
    }
    if not isinstance(p, dict) or set(p) - allowed:
        raise ValueError("unknown network input")
    controller = p.get("controller")
    if controller is not None:
        allowed_controller = {
            "name",
            "pacing_gain",
            "time_quantum",
            "debt_quantum",
            "controller_quantum",
            "fast_convergence",
            "bbr_random_draws",
        }
        if (
            not isinstance(controller, dict)
            or set(controller) - allowed_controller
            or controller.get("name") not in ("newreno", "cubic_hystart", "bbr")
        ):
            raise ValueError("invalid explicit controller configuration")
        if p.get("pacer_interval", 0):
            raise ValueError("fixed and dynamic pacers cannot be combined")
    if type(p.get("pad_in_flight", False)) is not bool:
        raise ValueError("padding policy must be boolean")
    for key in (
        "upload_bytes",
        "response_bytes",
        "receive_window",
        "packet_payload",
        "ack_bytes",
    ):
        if key in p and (type(p[key]) is not int or p[key] < 0):
            raise ValueError("nonnegative integer required: " + key)
    if p.get("upload_bytes", 0) <= 0:
        raise ValueError("this workload profile requires a nonempty upload")
    for key in ("model_seconds", "until", "consume_delay", "pacer_interval"):
        if key in p and (isinstance(p[key], bool) or F(str(p[key])) < 0):
            raise ValueError("nonnegative time required")
    controller = p.get("sender", {})
    if not isinstance(controller, dict) or set(controller) - {
        "max_datagram_size",
        "initial_cwnd",
        "initial_ssthresh",
        "initial_rtt",
        "rtt_seed",
        "granularity",
        "max_ack_delay",
        "numeric_quantum",
    }:
        raise ValueError("unknown or network-owned sender option")
    mds = controller.get("max_datagram_size", 1200)
    if type(mds) is not int or not 1200 <= mds <= 65507:
        raise ValueError("invalid declared IPv4 UDP payload limit")
    if (
        not 1 <= p.get("packet_payload", 1168) <= mds - 32
        or not 32 <= p.get("ack_bytes", 64) <= mds
    ):
        raise ValueError("packet layout exceeds declared QUIC datagram budget")
    count = sum(
        (p.get(k, 0) + p.get("packet_payload", 1168) - 1)
        // p.get("packet_payload", 1168)
        for k in ("upload_bytes", "response_bytes")
    )
    if count > 100000 or len(p.get("explicit_consumption", [])) > 100000:
        raise ValueError("finite workload event budget exceeded")
    if set(p["links"]) != {"up", "down"} or set(p.get("routers", {})) - {"up", "down"}:
        raise ValueError("unknown or missing direction")
    for d, link in p["links"].items():
        if set(link) != {"rate_bps", "propagation"}:
            raise ValueError("invalid link fields")
        if F(str(link["rate_bps"])) <= 0 or F(str(link["propagation"])) < 0:
            raise ValueError("invalid link rate/delay")
    for router in p.get("routers", {}).values():
        if (
            set(router) - {"rate_bps", "queue_bytes", "propagation"}
            or F(str(router["rate_bps"])) <= 0
            or F(str(router.get("propagation", 0))) < 0
        ):
            raise ValueError("invalid router")
        if type(router["queue_bytes"]) is not int or router["queue_bytes"] < 0:
            raise ValueError("queue_bytes is waiting wire-byte capacity")
    for item in p.get("drop_packets", []):
        if (
            set(item) != {"direction", "pn"}
            or item["direction"] not in ("up", "down")
            or type(item["pn"]) is not int
            or item["pn"] < 0
        ):
            raise ValueError("invalid declared network drop")
    for item in p.get("explicit_consumption", []):
        if (
            set(item) != {"direction", "at", "upto"}
            or item["direction"] not in ("up", "down")
            or type(item["upto"]) is not int
            or item["upto"] < 0
            or F(str(item["at"])) < 0
        ):
            raise ValueError("invalid consumption")


def calculate(inputs):
    p = copy.deepcopy(inputs)
    validate_inputs(p)
    reference_sources = json.loads((ROOT / "sources.lock.json").read_text())
    for source in reference_sources:
        raw = (ROOT / source["file"]).read_bytes()
        if (
            len(raw) != source["bytes"]
            or hashlib.sha256(raw).hexdigest() != source["sha256"]
        ):
            raise ValueError("network source integrity mismatch")
    until = F(str(p.get("until", 60)))
    directions = ("up", "down")
    opposite = {"up": "down", "down": "up"}
    links = p["links"]
    upload, response = p["upload_bytes"], p.get("response_bytes", 0)
    payload_limit = p.get("packet_payload", 1168)
    if (
        any(type(x) is not int or x < 0 for x in (upload, response))
        or payload_limit <= 0
    ):
        raise ValueError("invalid workload bytes")
    ack_policy = p.get("ack_policy", "immediate_each_packet")
    aggregate = isinstance(ack_policy, dict)
    if not aggregate and ack_policy != "immediate_each_packet":
        raise ValueError("unknown ACK policy")
    receivers = (
        {d: receiver_module.Receiver(ack_policy) for d in directions}
        if aggregate
        else {}
    )
    receiver_timers = {d: None for d in directions}
    if (
        aggregate
        and "max_ack_delay" in p.get("sender", {})
        and F(str(p["sender"]["max_ack_delay"])) != receivers["up"].policy["max_delay"]
    ):
        raise ValueError("sender max_ack_delay conflicts with receiver policy")
    states, pending, pn, busy, pace = {}, {}, {}, {}, {}
    loss_cursor, timer_cursor = {}, {}
    pacers = {}
    routers = p.get("routers", {})
    router_wait = {d: deque() for d in directions}
    router_busy = {d: False for d in directions}
    router_bytes = {d: 0 for d in directions}
    feedback_inputs = {d: [] for d in directions}
    received = {d: [] for d in directions}
    consumed = {d: 0 for d in directions}
    known_packets = {d: {} for d in directions}
    initial_credit = p.get("receive_window", max(upload, response, 1))
    config = p.get("sender", {})
    for d in directions:
        q = dict(
            until=str(until),
            initial_max_data=initial_credit,
            initial_max_stream_data={"business": initial_credit},
            events=[],
            max_ack_delay=0,
            retain_ledger=False,
            track_ack_only=False,
        )
        q.update(config)
        if aggregate:
            q["max_ack_delay"] = str(receivers[d].policy["max_delay"])
            q["track_ack_only"] = True
        if p.get("controller"):
            q["controller"] = {
                **p["controller"],
                "pad_in_flight": p.get("pad_in_flight", False),
            }
        states[d] = sender.create_sender(q)
        if p.get("controller"):
            cc = p["controller"]
            pacers[d] = pacer_module.Pacer(
                states[d]["pacing_rate"](),
                time_quantum=cc.get("time_quantum", "0.000000001"),
                debt_quantum=cc.get("debt_quantum", "0.000000000001"),
            )

            def hook(at, rate, direction=d):
                pacers[direction].advance(at, rate)
                return pacers[direction].ready(at)

            states[d]["set_pacer"](hook)
        pending[d] = {i: deque() for i in range(3)}
        pn[d] = 0
        busy[d] = False
        pace[d] = F(0)
        loss_cursor[d] = timer_cursor[d] = 0
        if F(str(links[d]["rate_bps"])) <= 0 or F(str(links[d]["propagation"])) < 0:
            raise ValueError("invalid link")
    heap, serial, now = [], 0, F(0)
    traces, events, waits = [], [], []
    armed = {d: None for d in directions}
    lossset = {(x["direction"], x["pn"]) for x in p.get("drop_packets", [])}
    consumed_scheduled = {d: 0 for d in directions}
    completed = {
        "upload": None,
        "model_start": None,
        "model_end": None,
        "response": None,
    }
    pump_set = set()
    index = 0

    def schedule(at, priority, kind, data):
        nonlocal serial
        if at <= until:
            serial += 1
            heapq.heappush(heap, (at, priority, serial, kind, data))

    def pump_at(d, at):
        key = (d, at)
        if key not in pump_set:
            pump_set.add(key)
            schedule(at, 3, "pump", d)

    def add(d, packet, priority=2):
        nonlocal index
        index += 1
        if p.get("pad_in_flight", False) and packet["in_flight"]:
            packet["sent_bytes"] = config.get("max_datagram_size", 1200)
        pending[d][priority].append((priority, index, packet))
        pump_at(d, now)

    def packetize(d, length):
        for offset in range(0, length, payload_limit):
            length_now = min(payload_limit, length - offset)
            add(
                d,
                dict(
                    kind="data",
                    frames=[
                        dict(
                            type="stream",
                            stream="business",
                            offset=offset,
                            length=length_now,
                        )
                    ],
                    sent_bytes=length_now + 32,
                    ack_eliciting=True,
                    in_flight=True,
                ),
            )

    def emit(d, event):
        feedback_inputs[d].append(copy.deepcopy(event))
        states[d]["enqueue"](event)

    def update(d):
        if d in pacers:
            pacers[d].advance(now)
        states[d]["advance"](now)
        s = states[d]
        for loss in s["losses"][loss_cursor[d] :]:
            old = known_packets[d][loss["pn"]]
            covered = old["frames"] and all(
                any(
                    a <= f["offset"] and b >= f["offset"] + f["length"]
                    for a, b in s["acked_stream"].get(f["stream"], [])
                )
                for f in old["frames"]
            )
            if old["kind"] != "ack" and not covered:
                packet = copy.deepcopy(old)
                packet.pop("probe", None)
                packet["recovery_of"] = loss["pn"]
                add(d, packet, 1)
        loss_cursor[d] = len(s["losses"])
        for timer in s["timers"][timer_cursor[d] :]:
            if timer["kind"] == "pto":
                candidates = [h for h in s["active"].values() if h["ack_eliciting"]]
                if candidates:
                    old = min(candidates, key=lambda h: h["pn"])
                    packet = copy.deepcopy(known_packets[d][old["pn"]])
                    packet.update(probe=True, probe_of=old["pn"])
                    add(d, packet, 1)
        timer_cursor[d] = len(s["timers"])
        timer = s["state"]()["next_timer"]
        key = (timer["kind"], timer["at"]) if timer else None
        refresh_limited(d)
        if key != armed[d]:
            armed[d] = key
            if timer:
                schedule(F(timer["at"]), 2, "sender_timer", (d, key))

    def refresh_limited(d):
        if not p.get("controller"):
            return
        ready = [q[0][2] for q in pending[d].values() if q and q[0][2]["kind"] != "ack"]
        reasons = states[d]["validate_packet"](ready[0])[1] if ready else []
        states[d]["set_limited"](
            now, not ready, any(reason.startswith("MAX_") for reason in reasons)
        )

    def prefix(d):
        return received[d][0][1] if received[d] and received[d][0][0] == 0 else 0

    def consume(d, upto):
        if upto <= consumed[d]:
            return
        consumed[d] = upto
        limit = initial_credit + upto
        add(
            opposite[d],
            dict(
                kind="max",
                frames=[],
                sent_bytes=64,
                ack_eliciting=True,
                in_flight=True,
                limits={"max_data": limit, "max_stream_data": limit},
            ),
            0,
        )
        events.append(
            dict(
                at=str(now),
                type="consume",
                direction=d,
                consumed=upto,
                advertised_limit=limit,
            )
        )

    def router_start(d, record):
        router_busy[d] = True
        settings = routers[d]
        end = now + F(8 * record["wire_bytes"], 1) / F(str(settings["rate_bps"]))
        record["router_start"] = str(now)
        record["router_end"] = str(end)
        record["arrival"] = str(end + F(str(settings.get("propagation", 0))))
        schedule(end, -1, "router_done", d)
        schedule(F(record["arrival"]), 0, "arrival", record)

    def router_admit(record):
        d = record["direction"]
        record["router_admission"] = str(now)
        if not router_busy[d]:
            router_start(d, record)
        elif router_bytes[d] + record["wire_bytes"] <= routers[d]["queue_bytes"]:
            router_wait[d].append(record)
            router_bytes[d] += record["wire_bytes"]
        else:
            record["dropped"] = True
            record["drop_reason"] = "router_waiting_queue_capacity"
            record["arrival"] = None
            events.append(
                dict(
                    at=str(now), type="network_queue_drop", direction=d, pn=record["pn"]
                )
            )

    def queue_ack(received_direction):
        add(
            opposite[received_direction],
            dict(
                kind="ack",
                frames=[],
                sent_bytes=p.get("ack_bytes", 64),
                ack_eliciting=False,
                in_flight=False,
                ack_for=received_direction,
            ),
            0,
        )

    def arrival(record):
        record["received_at"] = str(now)
        d, number = record["direction"], record["pn"]
        packet = known_packets[d][number]
        other = opposite[d]
        if packet["kind"] == "ack":
            blocked = []
            ready_data = [
                q[0][2]
                for q in pending[other].values()
                if q and q[0][2]["kind"] != "ack"
            ]
            if ready_data:
                _, blocked = states[other]["validate_packet"](ready_data[0])
            emit(
                other,
                dict(
                    type="ack",
                    at=str(now),
                    ranges=packet["ranges"],
                    ack_delay=packet.get("ack_snapshot", {}).get("decoded_delay", "0"),
                    app_limited=not ready_data,
                    flow_limited=any(x.startswith("MAX_") for x in blocked),
                ),
            )
            schedule(now, 2, "feedback", other)
        elif packet["kind"] == "max":
            for kind, value in packet["limits"].items():
                e = dict(type=kind, at=str(now), value=value)
                if kind == "max_stream_data":
                    e["stream"] = "business"
                emit(other, e)
            schedule(now, 2, "feedback", other)
        else:
            for frame in packet["frames"]:
                received[d] = sender.union(
                    received[d] + [[frame["offset"], frame["offset"] + frame["length"]]]
                )
            held = sum(b - a for a, b in received[d]) - consumed[d]
            if held > initial_credit:
                raise ValueError(
                    "receiver buffer exceeds advertised consumption window"
                )
            current = prefix(d)
            events.append(
                dict(
                    at=str(now), type="application_prefix", direction=d, prefix=current
                )
            )
            if p.get("consume_delay") is not None and current > consumed_scheduled[d]:
                consumed_scheduled[d] = current
                schedule(now + F(str(p["consume_delay"])), 1, "consume", (d, current))
            if d == "up" and current == upload and completed["upload"] is None:
                completed["upload"] = completed["model_start"] = str(now)
                schedule(now + F(str(p.get("model_seconds", 0))), 1, "model_done", None)
            if d == "down" and current == response and completed["response"] is None:
                completed["response"] = str(now)
        if aggregate:
            receiver = receivers[d]
            newly_queued = receiver.receive(number, now, packet["ack_eliciting"])
            if newly_queued:
                queue_ack(d)
            key = (receiver.generation, receiver.deadline)
            if receiver.deadline is not None and receiver_timers[d] != key:
                receiver_timers[d] = key
                schedule(receiver.deadline, 1, "ack_deadline", (d, receiver.generation))
        elif packet["ack_eliciting"]:
            # One explicit ACK range for the one newly received packet; no cumulative O(N²) history.
            add(
                other,
                dict(
                    kind="ack",
                    frames=[],
                    sent_bytes=p.get("ack_bytes", 64),
                    ack_eliciting=False,
                    in_flight=False,
                    ranges=[[number, number]],
                ),
                0,
            )
        pump_at(other, now)

    def pump(d):
        if busy[d] or not any(pending[d].values()):
            return
        update(d)
        if now < pace[d]:
            pump_at(d, pace[d])
            return
        selected = None
        reasons_all = set()
        for q in pending[d].values():
            if not q:
                continue
            item = q[0]
            _, reasons = states[d]["validate_packet"](item[2])
            if d in pacers and item[2]["in_flight"]:
                ready_at = pacers[d].ready(now)
                if ready_at > now:
                    reasons = [*reasons, "pacer"]
                    pump_at(d, ready_at)
            if not reasons:
                selected = item
                break
            reasons_all.update(reasons)
        if selected is None:
            waits.append(dict(at=str(now), direction=d, reasons=sorted(reasons_all)))
            return
        pending[d][selected[0]].popleft()
        packet = selected[2]
        if aggregate and packet["kind"] == "ack":
            snapshot = receivers[packet["ack_for"]].snapshot(now, packet["sent_bytes"])
            packet["ranges"] = snapshot["ranges"]
            packet["ack_snapshot"] = snapshot
        number = pn[d]
        pn[d] += 1
        known_packets[d][number] = packet
        event = dict(
            type="sent",
            at=str(now),
            pn=number,
            sent_bytes=packet["sent_bytes"],
            frames=packet["frames"],
            ack_eliciting=packet["ack_eliciting"],
            in_flight=packet["in_flight"],
            probe=packet.get("probe", False),
        )
        if d in pacers and packet["in_flight"]:
            pacers[d].sent(now, packet["sent_bytes"])
        emit(d, event)
        update(d)
        duration = F(8 * (packet["sent_bytes"] + 28), 1) / F(str(links[d]["rate_bps"]))
        end = now + duration
        record = dict(
            direction=d,
            pn=number,
            kind=packet["kind"],
            frames=copy.deepcopy(packet["frames"]),
            send_start=str(now),
            send_end=str(end),
            arrival=str(end + F(str(links[d]["propagation"]))),
            quic_bytes=packet["sent_bytes"],
            udp_ip_bytes=28,
            wire_bytes=packet["sent_bytes"] + 28,
            dropped=(d, number) in lossset,
            probe=packet.get("probe", False),
            received_at=None,
            recovery_of=packet.get("recovery_of"),
            probe_of=packet.get("probe_of"),
        )
        if aggregate and packet["kind"] == "ack":
            record["ack_snapshot"] = copy.deepcopy(packet["ack_snapshot"])
        traces.append(record)
        busy[d] = True
        pace[d] = now + F(str(p.get("pacer_interval", 0)))
        schedule(end, 1, "serial_done", d)
        if not record["dropped"]:
            if d in routers:
                at_router = F(record["arrival"])
                record["arrival"] = None
                schedule(at_router, 0, "router_admit", record)
            else:
                schedule(F(record["arrival"]), 0, "arrival", record)

    packetize("up", upload)
    for item in p.get("explicit_consumption", []):
        schedule(F(str(item["at"])), 1, "consume", (item["direction"], item["upto"]))
    while heap:
        now, _, _, kind, value = heapq.heappop(heap)
        if len(traces) > 200000:
            raise ValueError("packet budget exceeded")
        if kind == "router_admit":
            router_admit(value)
        elif kind == "router_done":
            router_busy[value] = False
            if router_wait[value]:
                record = router_wait[value].popleft()
                router_bytes[value] -= record["wire_bytes"]
                router_start(value, record)
        elif kind == "arrival":
            arrival(value)
        elif kind == "ack_deadline":
            d, generation = value
            if receivers[d].expire(now, generation):
                queue_ack(d)
        elif kind == "serial_done":
            busy[value] = False
            pump_at(value, now)
        elif kind == "consume":
            d, upto = value
            if upto > prefix(d):
                raise ValueError("cannot consume not-yet-delivered bytes")
            consume(d, upto)
        elif kind == "model_done":
            completed["model_end"] = str(now)
            packetize("down", response)
            if response == 0:
                completed["response"] = str(now)
        elif kind == "feedback":
            update(value)
            pump_at(value, now)
        elif kind == "sender_timer":
            d, key = value
            if armed[d] == key:
                update(d)
                pump_at(d, now)
        elif kind == "pump":
            pump_set.discard((value, now))
            pump(value)
    final = {d: states[d]["state"]() for d in directions}
    result = dict(
        inputs=p,
        reference_sources=reference_sources,
        reference_source_root=str(ROOT),
        transmissions=traces,
        business=completed,
        application_events=events,
        waits=waits,
        sender_events=feedback_inputs,
        final_states=final,
        losses={d: states[d]["losses"] for d in directions},
        timers={d: states[d]["timers"] for d in directions},
        numeric_errors={d: states[d]["numeric_errors"] for d in directions},
        received_intervals=received,
        consumed=consumed,
        summary=dict(
            wire_bytes=sum(t["wire_bytes"] for t in traces),
            serialized_wire_bytes_by_horizon=str(
                sum(
                    F(t["wire_bytes"])
                    * min(
                        F(1),
                        max(
                            F(0),
                            (until - F(t["send_start"]))
                            / (F(t["send_end"]) - F(t["send_start"])),
                        ),
                    )
                    for t in traces
                )
            ),
            unique_received_bytes=sum(
                b - a for ranges in received.values() for a, b in ranges
            ),
            pending_packets={
                d: sum(len(q) for q in pending[d].values()) for d in directions
            },
            complete=completed["response"] is not None,
        ),
    )

    if p.get("controller"):
        result["controller_events"] = {
            d: states[d]["adapter"].events if states[d]["adapter"] else []
            for d in directions
        }
        result["controller_numeric_errors"] = {
            d: getattr(states[d]["adapter"], "numeric_errors", []) for d in directions
        }
        result["pacer_errors"] = {d: pacers[d].errors for d in directions}
        result["pacer_final"] = {d: pacers[d].snapshot() for d in directions}
        result["persistent_events"] = {
            d: states[d]["persistent_events"] for d in directions
        }
    if aggregate:
        result["ack_events"] = {d: receivers[d].events for d in directions}
        result["ack_state"] = {d: receivers[d].state() for d in directions}
    return result


def example():
    return dict(
        upload_bytes=2336,
        response_bytes=32,
        model_seconds="1",
        until="20",
        links=dict(
            up=dict(rate_bps=9824, propagation=1),
            down=dict(rate_bps=736, propagation=1),
        ),
        sender=dict(
            initial_cwnd=2400,
            rtt_seed=dict(latest_rtt=4, smoothed_rtt=4, rttvar=2, min_rtt=4),
        ),
    )


def legacy_scenarios():
    out = {"response-dependency": example()}
    one = example()
    one.update(upload_bytes=3504, response_bytes=0, model_seconds=0)
    out["cwnd-third-packet"] = one
    flow = copy.deepcopy(one)
    flow.update(
        receive_window=2336,
        explicit_consumption=[dict(at=4, direction="up", upto=2336)],
    )
    out["absolute-flow-arrival"] = flow
    loss = example()
    loss.update(
        response_bytes=0, model_seconds=0, drop_packets=[dict(direction="up", pn=0)]
    )
    out["loss-feedback-recovery"] = loss
    tail = copy.deepcopy(loss)
    tail["upload_bytes"] = 1168
    out["tail-pto-probe"] = tail
    ack_loss = example()
    ack_loss.update(drop_packets=[dict(direction="down", pn=0)], until=30)
    out["ack-loss"] = ack_loss
    router = copy.deepcopy(one)
    router["until"] = 60
    router["sender"]["initial_cwnd"] = 12000
    router["links"]["up"]["rate_bps"] = 98240
    router["routers"] = {"up": dict(rate_bps=9824, queue_bytes=0, propagation=0)}
    out["finite-router-drop"] = router
    consumption = copy.deepcopy(one)
    consumption.update(receive_window=2336, consume_delay=1)
    out["automatic-consumption"] = consumption
    blocked = copy.deepcopy(one)
    blocked.update(receive_window=0, until=10)
    out["no-credit-incomplete"] = blocked
    book = example()
    book.update(
        upload_bytes=30000000, response_bytes=5000000, model_seconds="0.3", until=60
    )
    book["links"] = {
        "up": dict(rate_bps=20000000, propagation="0.05"),
        "down": dict(rate_bps=100000000, propagation="0.05"),
    }
    book["sender"] = dict(initial_cwnd=12000, numeric_quantum="0.000000000001")
    out["book-30mb-5mb"] = book
    return out


def scenarios():
    return json.loads((ROOT / "scenarios.json").read_text())


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inputs", type=Path)
    ap.add_argument("--output", type=Path)
    a = ap.parse_args()
    r = (
        calculate(json.loads(a.inputs.read_text()))
        if a.inputs
        else {k: calculate(v) for k, v in scenarios().items()}
    )
    output = json.dumps(r, indent=2) + "\n"
    if a.output:
        a.output.write_text(output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
