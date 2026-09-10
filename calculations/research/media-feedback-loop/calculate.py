"""Research media DAG with real single-path feedback; declared QUIC packet layout."""

from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict, deque
import heapq
import copy
import json
import argparse
import sys
import importlib.util

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parents[2] / "calculations/src"))
from infra_calc.transport.ack_receiver import Receiver
from infra_calc.transport.pacer import Pacer
from infra_calc.transport.reference_sources import reference_sources


def local_module(filename):
    spec = importlib.util.spec_from_file_location(
        "media_feedback_" + filename[:-3], ROOT / filename
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


Application = local_module("application.py").Application
validate_application = local_module("application_validation.py").validate_application
sender = local_module("sender.py")
validate_network = local_module("network_validation.py").validate_network

DIRECTIONS = ("up", "down")
OTHER = {"up": "down", "down": "up"}
ENDPOINT = {"up": "client", "down": "server"}


def merge(ranges, start, end):
    if start == end:
        return
    result = []
    for a, b in ranges:
        if b < start:
            result.append([a, b])
        elif end < a:
            result.append([start, end])
            start, end = a, b
        else:
            start, end = min(start, a), max(end, b)
    result.append([start, end])
    ranges[:] = result


def prefix(ranges):
    return ranges[0][1] if ranges and ranges[0][0] == 0 else 0


class Network:
    def __init__(self, inputs):
        self.inputs = copy.deepcopy(inputs)
        self.app_input = inputs["application"]
        self.cfg = inputs["network"]
        validate_application(self.app_input)
        validate_network(self.cfg, self.app_input)
        self.reference_sources = sender.reference_sources(
            include_datagram=any(
                m["transport"] == "datagram" for m in self.app_input["messages"]
            )
        )
        if self.cfg.get("controller", {}).get("name") == "cubic_hystart":
            self.reference_sources += reference_sources("cubic") + reference_sources(
                "hystart"
            )
        elif self.cfg.get("controller", {}).get("name") == "bbr":
            self.reference_sources += reference_sources("bbr")
        if self.app_input["scheduling"]["compute"] != "fifo":
            raise ValueError("only declared FIFO compute supported")
        self.now = F(0)
        self.until = F(str(self.cfg["until"]))
        self.heap = []
        self.serial = 0
        self.packet_index = 0
        self.states = {}
        self.queues = {d: defaultdict(deque) for d in DIRECTIONS}
        self.known = {d: {} for d in DIRECTIONS}
        self.pn = {d: 0 for d in DIRECTIONS}
        self.busy = {d: False for d in DIRECTIONS}
        self.pacers = {}
        self.receivers = {}
        self.ack_timer = {d: None for d in DIRECTIONS}
        self.armed = {d: None for d in DIRECTIONS}
        self.loss_cursor = {d: 0 for d in DIRECTIONS}
        self.timer_cursor = {d: 0 for d in DIRECTIONS}
        self.received = {d: defaultdict(list) for d in DIRECTIONS}
        self.consumed = {d: defaultdict(int) for d in DIRECTIONS}
        self.consume_scheduled = {d: defaultdict(int) for d in DIRECTIONS}
        self.received_message = defaultdict(list)
        self.flow_messages = defaultdict(list)
        self.flow_cursor = defaultdict(int)
        self.traces = []
        self.events = []
        self.waits = []
        self.feedback = {d: [] for d in DIRECTIONS}
        self.peak_memory = {d: 0 for d in DIRECTIONS}
        self.drop = {
            (x["direction"], x["pn"]) for x in self.cfg.get("drop_packets", [])
        }
        self.routers = self.cfg.get("routers", {})
        self.router_busy = {d: False for d in DIRECTIONS}
        self.router_queues = {d: deque() for d in DIRECTIONS}
        self.router_bytes = {d: 0 for d in DIRECTIONS}
        self.pump_set = set()
        self.policy = self.cfg.get("ack_policy", "immediate_each_packet")
        self.aggregate = isinstance(self.policy, dict)
        if not self.aggregate and self.policy != "immediate_each_packet":
            raise ValueError("unknown ACK policy")
        for d in DIRECTIONS:
            options = copy.deepcopy(self.cfg.get("sender", {}))
            options.update(
                until=str(self.until),
                initial_cwnd=self.cfg["initial_cwnd"],
                initial_max_data=self.cfg["initial_max_data"][d],
                initial_max_stream_data=self.cfg["initial_max_stream_data"][d],
                events=[],
                retain_ledger=False,
                track_ack_only=self.aggregate,
                max_ack_delay=0,
            )
            if self.aggregate:
                self.receivers[d] = Receiver(self.policy)
                options["max_ack_delay"] = str(self.receivers[d].policy["max_delay"])
            if self.cfg.get("controller"):
                options["controller"] = {
                    **self.cfg["controller"],
                    "pad_in_flight": self.cfg.get("pad_in_flight", True),
                }
            self.states[d] = sender.create_sender(options)
            if self.cfg.get("controller"):
                cc = self.cfg["controller"]
                self.pacers[d] = Pacer(
                    self.states[d]["pacing_rate"](),
                    time_quantum=cc.get("time_quantum", "0.000000001"),
                    debt_quantum=cc.get("debt_quantum", "0.000000000001"),
                )

                def hook(at, rate, direction=d):
                    self.pacers[direction].advance(at, rate)
                    return self.pacers[direction].ready(at)

                self.states[d]["set_pacer"](hook)
            if self.cfg["initial_max_data"][d] > self.cfg["receive_memory_bytes"][d]:
                raise ValueError("advertised data credit exceeds receiver memory")
        self.application = Application(
            self.app_input, self.schedule, self.activate, lambda: self.now
        )
        for m in self.app_input["messages"]:
            if m["transport"] == "stream":
                self.flow_messages[self.direction(m), m["flow_id"]].append(m)
        for values in self.flow_messages.values():
            values.sort(key=lambda m: m["stream_offset"])

    def direction(self, message):
        return "up" if message["sender"] == "client" else "down"

    def schedule(self, at, priority, kind, data):
        at = F(str(at))
        if at < self.now:
            raise ValueError("event scheduled into past")
        if at <= self.until:
            self.serial += 1
            heapq.heappush(self.heap, (at, priority, self.serial, kind, data))

    def pump_at(self, d, at):
        key = (d, at)
        if key not in self.pump_set:
            self.pump_set.add(key)
            self.schedule(at, 3, "pump", d)

    def add(self, d, packet, level=2):
        self.packet_index += 1
        packet["enqueue_index"] = self.packet_index
        packet["level"] = level
        packet["ready_at"] = str(self.now)
        if self.cfg.get("pad_in_flight", True) and packet["in_flight"]:
            packet["sent_bytes"] = 1200
        key = (
            ("control", level)
            if level < 2
            else ("flow", packet["frames"][0]["type"], packet["flow_id"])
        )
        self.queues[d][key].append(packet)
        self.pump_at(d, self.now)

    def activate(self, message):
        d = self.direction(message)
        if self.now < F(self.app_input["connection_ready_seconds"]):
            self.schedule(
                F(self.app_input["connection_ready_seconds"]),
                1,
                "activate",
                message["id"],
            )
            return
        limit = message["packetization"]["payload_limit_bytes"]
        for offset in range(0, message["bytes"], limit):
            length = min(limit, message["bytes"] - offset)
            frame = (
                dict(
                    type="stream",
                    stream=message["flow_id"],
                    offset=message["stream_offset"] + offset,
                    length=length,
                )
                if message["transport"] == "stream"
                else dict(type="datagram", id=message["id"], length=length)
            )
            self.add(
                d,
                dict(
                    kind="data",
                    frames=[frame],
                    sent_bytes=length + 32,
                    ack_eliciting=True,
                    in_flight=True,
                    message_id=message["id"],
                    flow_id=message["flow_id"],
                    message_offset=offset,
                    length=length,
                    priority=message["priority"],
                ),
            )
        if message["bytes"] == 0:
            self.application.delivered(message["id"])

    def emit(self, d, event):
        self.feedback[d].append(copy.deepcopy(event))
        self.states[d]["enqueue"](event)

    def covered(self, d, packet):
        if not packet["frames"]:
            return False
        if any(f["type"] != "stream" for f in packet["frames"]):
            return False
        return all(
            any(
                a <= f["offset"] and b >= f["offset"] + f["length"]
                for a, b in self.states[d]["acked_stream"].get(f["stream"], [])
            )
            for f in packet["frames"]
        )

    def update(self, d):
        if d in self.pacers:
            self.pacers[d].advance(self.now)
        state = self.states[d]
        state["advance"](self.now)
        for loss in state["losses"][self.loss_cursor[d] :]:
            old = self.known[d][loss["pn"]]
            if old["kind"] in ("max", "ping") or (
                sender.retransmittable_frames(old) and not self.covered(d, old)
            ):
                packet = copy.deepcopy(old)
                packet.pop("probe", None)
                packet["recovery_of"] = loss["pn"]
                self.add(d, packet, 1)
        self.loss_cursor[d] = len(state["losses"])
        for timer in state["timers"][self.timer_cursor[d] :]:
            if timer["kind"] == "pto":
                candidates = [h for h in state["active"].values() if h["ack_eliciting"]]
                reliable = [
                    h
                    for h in candidates
                    if self.known[d][h["pn"]]["kind"] in ("max", "ping")
                    or sender.retransmittable_frames(h)
                ]
                if reliable:
                    old = min(reliable, key=lambda h: h["pn"])
                    packet = copy.deepcopy(self.known[d][old["pn"]])
                    packet.update(probe=True, probe_of=old["pn"])
                elif candidates:
                    packet = dict(
                        kind="ping",
                        frames=[],
                        sent_bytes=64,
                        ack_eliciting=True,
                        in_flight=True,
                        probe=True,
                        probe_of=min(h["pn"] for h in candidates),
                    )
                else:
                    continue
                self.add(d, packet, 1)
        self.timer_cursor[d] = len(state["timers"])
        self.refresh_limited(d)
        timer = state["state"]()["next_timer"]
        key = (timer["kind"], timer["at"]) if timer else None
        if key != self.armed[d]:
            self.armed[d] = key
            if timer:
                self.schedule(F(timer["at"]), 2, "sender_timer", (d, key))

    def heads(self, d):
        for queue in self.queues[d].values():
            while queue:
                p = queue[0]
                if p["kind"] != "data" or p["level"] < 2:
                    break
                message = self.application.messages[p["message_id"]]
                expired = (
                    message["allow_expire"]
                    and message["deadline_seconds"] is not None
                    and self.now > F(message["deadline_seconds"])
                )
                if not self.application.suppressed(message) and not expired:
                    break
                queue.popleft()
                self.events.append(
                    dict(
                        at=str(self.now),
                        kind="suppress_unsent_slice",
                        message=message["id"],
                        offset=p["message_offset"],
                        reason="expired" if expired else "cancelled",
                    )
                )
                self.application.status[message["id"]] = (
                    "expired" if expired else "cancelled"
                )
            if queue:
                yield queue[0]

    def refresh_limited(self, d):
        if not self.cfg.get("controller"):
            return
        ready = [p for p in self.heads(d) if p["kind"] != "ack"]
        reasons = [self.states[d]["validate_packet"](p)[1] for p in ready]
        flow = bool(ready) and all(
            any(r.startswith("MAX_") for r in rs) for rs in reasons
        )
        self.states[d]["set_limited"](self.now, not ready, flow)

    def queue_ack(self, d):
        self.add(
            OTHER[d],
            dict(
                kind="ack",
                frames=[],
                sent_bytes=self.cfg.get("ack_bytes", 64),
                ack_eliciting=False,
                in_flight=False,
                ack_for=d,
            ),
            0,
        )

    def acknowledge_received(self, d, number, packet):
        if self.aggregate:
            receiver = self.receivers[d]
            if receiver.receive(number, self.now, packet["ack_eliciting"]):
                self.queue_ack(d)
            key = (receiver.generation, receiver.deadline)
            if receiver.deadline is not None and key != self.ack_timer[d]:
                self.ack_timer[d] = key
                self.schedule(
                    receiver.deadline, 1, "ack_deadline", (d, receiver.generation)
                )
        elif packet["ack_eliciting"]:
            self.add(
                OTHER[d],
                dict(
                    kind="ack",
                    frames=[],
                    sent_bytes=self.cfg.get("ack_bytes", 64),
                    ack_eliciting=False,
                    in_flight=False,
                    ranges=[[number, number]],
                ),
                0,
            )

    def ordered(self, d, flow):
        current = prefix(self.received[d][flow])
        key = (d, flow)
        messages = self.flow_messages[key]
        while self.flow_cursor[key] < len(messages):
            m = messages[self.flow_cursor[key]]
            if m["stream_offset"] + m["bytes"] > current:
                break
            self.application.delivered(m["id"])
            self.flow_cursor[key] += 1
        delay = self.cfg.get("consume_delay")
        if delay is not None and current > self.consume_scheduled[d][flow]:
            self.consume_scheduled[d][flow] = current
            self.schedule(self.now + F(str(delay)), 1, "consume", (d, flow, current))

    def consume(self, d, flow, upto):
        if upto <= self.consumed[d][flow]:
            return
        if upto > prefix(self.received[d][flow]):
            raise ValueError("future consumption")
        self.consumed[d][flow] = upto
        limits = [
            dict(
                type="max_data",
                value=self.cfg["initial_max_data"][d] + sum(self.consumed[d].values()),
            ),
            dict(
                type="max_stream_data",
                stream=flow,
                value=self.cfg["initial_max_stream_data"][d][flow] + upto,
            ),
        ]
        self.add(
            OTHER[d],
            dict(
                kind="max",
                frames=[],
                sent_bytes=64,
                ack_eliciting=True,
                in_flight=True,
                limits=limits,
            ),
            0,
        )
        self.events.append(
            dict(
                at=str(self.now),
                kind="consume",
                direction=d,
                flow=flow,
                upto=upto,
                limits=limits,
            )
        )

    def arrival(self, record):
        record["received_at"] = str(self.now)
        d = record["direction"]
        packet = self.known[d][record["pn"]]
        other = OTHER[d]
        if packet["kind"] == "ack":
            ready = [p for p in self.heads(other) if p["kind"] != "ack"]
            reasons = [self.states[other]["validate_packet"](p)[1] for p in ready]
            self.emit(
                other,
                dict(
                    type="ack",
                    at=str(self.now),
                    ranges=packet["ranges"],
                    ack_delay=packet.get("ack_snapshot", {}).get("decoded_delay", "0"),
                    app_limited=not ready,
                    flow_limited=bool(ready)
                    and all(any(r.startswith("MAX_") for r in rs) for rs in reasons),
                ),
            )
            self.schedule(self.now, 2, "feedback", other)
        elif packet["kind"] == "max":
            for limit in packet["limits"]:
                self.emit(other, dict(at=str(self.now), **limit))
            self.schedule(self.now, 2, "feedback", other)
        elif packet["kind"] == "data":
            m = self.application.messages[packet["message_id"]]
            f = packet["frames"][0]
            merge(
                self.received_message[m["id"]],
                packet["message_offset"],
                packet["message_offset"] + packet["length"],
            )
            if f["type"] == "stream":
                merge(
                    self.received[d][f["stream"]],
                    f["offset"],
                    f["offset"] + f["length"],
                )
                held = sum(
                    b - a for ranges in self.received[d].values() for a, b in ranges
                ) - sum(self.consumed[d].values())
                self.peak_memory[d] = max(self.peak_memory[d], held)
                if held > self.cfg["receive_memory_bytes"][d]:
                    raise ValueError(
                        "receiver memory exhausted under advertised credit"
                    )
                self.ordered(d, f["stream"])
            else:
                held = sum(
                    b - a for ranges in self.received[d].values() for a, b in ranges
                ) - sum(self.consumed[d].values())
                expired = (
                    m["allow_expire"]
                    and m["deadline_seconds"] is not None
                    and self.now > F(m["deadline_seconds"])
                )
                if (
                    expired
                    or held + packet["length"] > self.cfg["receive_memory_bytes"][d]
                ):
                    reason = "expired" if expired else "receiver_memory_drop"
                    self.application.status[m["id"]] = reason
                    self.events.append(
                        dict(at=str(self.now), kind=reason, message=m["id"])
                    )
                else:
                    self.peak_memory[d] = max(
                        self.peak_memory[d], held + packet["length"]
                    )
                    self.application.delivered(m["id"])
        self.acknowledge_received(d, record["pn"], packet)
        self.pump_at(other, self.now)

    def pump(self, d):
        if self.busy[d]:
            return
        self.update(d)
        candidates = sorted(
            self.heads(d),
            key=lambda p: (
                p["level"],
                (
                    -p.get("priority", 0)
                    if self.app_input["scheduling"]["send"] == "priority"
                    else 0
                ),
                p["enqueue_index"],
            ),
        )
        chosen = None
        blocked = set()
        for p in candidates:
            _, reasons = self.states[d]["validate_packet"](p)
            if d in self.pacers and p["in_flight"]:
                ready = self.pacers[d].ready(self.now)
                if ready > self.now:
                    reasons = [*reasons, "pacer"]
                    self.pump_at(d, ready)
            if not reasons:
                chosen = p
                break
            blocked.update(reasons)
        if chosen is None:
            if blocked:
                self.waits.append(
                    dict(at=str(self.now), direction=d, reasons=sorted(blocked))
                )
            return
        key = (
            ("control", chosen["level"])
            if chosen["level"] < 2
            else ("flow", chosen["frames"][0]["type"], chosen["flow_id"])
        )
        self.queues[d][key].popleft()
        packet = chosen
        if self.aggregate and packet["kind"] == "ack":
            snap = self.receivers[packet["ack_for"]].snapshot(
                self.now, packet["sent_bytes"]
            )
            packet["ranges"] = snap["ranges"]
            packet["ack_snapshot"] = snap
        number = self.pn[d]
        self.pn[d] += 1
        self.known[d][number] = packet
        event = dict(
            type="sent",
            at=str(self.now),
            pn=number,
            sent_bytes=packet["sent_bytes"],
            frames=packet["frames"],
            ack_eliciting=packet["ack_eliciting"],
            in_flight=packet["in_flight"],
            probe=packet.get("probe", False),
        )
        if d in self.pacers and packet["in_flight"]:
            self.pacers[d].sent(self.now, packet["sent_bytes"])
        self.emit(d, event)
        self.update(d)
        end = self.now + F(8 * (packet["sent_bytes"] + 28), 1) / F(
            str(self.cfg["links"][d]["rate_bps"])
        )
        record = dict(
            direction=d,
            pn=number,
            kind=packet["kind"],
            message_id=packet.get("message_id"),
            message_offset=packet.get("message_offset"),
            frames=copy.deepcopy(packet["frames"]),
            send_start=str(self.now),
            send_end=str(end),
            arrival=str(end + F(str(self.cfg["links"][d]["propagation"]))),
            received_at=None,
            quic_bytes=packet["sent_bytes"],
            wire_bytes=packet["sent_bytes"] + 28,
            dropped=(d, number) in self.drop,
            probe=packet.get("probe", False),
            probe_of=packet.get("probe_of"),
            recovery_of=packet.get("recovery_of"),
        )
        if "ack_snapshot" in packet:
            record["ack_snapshot"] = copy.deepcopy(packet["ack_snapshot"])
        self.traces.append(record)
        self.busy[d] = True
        self.schedule(end, 1, "serial_done", d)
        if not record["dropped"]:
            if d in self.routers:
                self.schedule(F(record["arrival"]), 0, "router_admit", record)
                record["arrival"] = None
            else:
                self.schedule(F(record["arrival"]), 0, "arrival", record)

    def router_start(self, d, record):
        self.router_busy[d] = True
        settings = self.routers[d]
        end = self.now + F(8 * record["wire_bytes"], 1) / F(str(settings["rate_bps"]))
        record.update(
            router_start=str(self.now),
            router_end=str(end),
            arrival=str(end + F(str(settings.get("propagation", 0)))),
        )
        self.schedule(end, -1, "router_done", d)
        self.schedule(F(record["arrival"]), 0, "arrival", record)

    def run(self):
        while self.heap:
            self.now, _, _, kind, value = heapq.heappop(self.heap)
            if len(self.traces) > 200000:
                raise ValueError("packet budget exceeded")
            if kind == "app_ready":
                self.application.ready(value)
            elif kind == "app_dispatch":
                self.application.dispatch(value)
            elif kind == "app_task_done":
                self.application.task_done(*value)
            elif kind == "activate":
                self.activate(self.application.messages[value])
            elif kind == "arrival":
                self.arrival(value)
            elif kind == "consume":
                self.consume(*value)
            elif kind == "serial_done":
                self.busy[value] = False
                self.pump_at(value, self.now)
            elif kind == "pump":
                self.pump_set.discard((value, self.now))
                self.pump(value)
            elif kind == "feedback":
                self.update(value)
                self.pump_at(value, self.now)
            elif kind == "sender_timer":
                d, key = value
                if self.armed[d] == key:
                    self.update(d)
                    self.pump_at(d, self.now)
            elif kind == "ack_deadline":
                d, generation = value
                if self.receivers[d].expire(self.now, generation):
                    self.queue_ack(d)
            elif kind == "router_admit":
                d = value["direction"]
                value["router_admission"] = str(self.now)
                if not self.router_busy[d]:
                    self.router_start(d, value)
                elif (
                    self.router_bytes[d] + value["wire_bytes"]
                    <= self.routers[d]["queue_bytes"]
                ):
                    self.router_queues[d].append(value)
                    self.router_bytes[d] += value["wire_bytes"]
                else:
                    value.update(
                        dropped=True, drop_reason="router_waiting_queue_capacity"
                    )
            elif kind == "router_done":
                self.router_busy[value] = False
                if self.router_queues[value]:
                    record = self.router_queues[value].popleft()
                    self.router_bytes[value] -= record["wire_bytes"]
                    self.router_start(value, record)
        snapshots = {d: self.states[d]["result"]() for d in DIRECTIONS}
        businesses = self.application.observers(self.until)
        return dict(
            inputs=self.inputs,
            reference_sources=self.reference_sources,
            transmissions=self.traces,
            sender_events=self.feedback,
            application_events=self.application.events,
            network_events=self.events,
            work=self.application.work,
            businesses=businesses,
            message_status=self.application.status,
            delivered={k: str(v) for k, v in self.application.completed.items()},
            waits=self.waits,
            received_intervals={d: dict(v) for d, v in self.received.items()},
            consumed={d: dict(v) for d, v in self.consumed.items()},
            peak_receive_memory=self.peak_memory,
            final_states={d: self.states[d]["state"]() for d in DIRECTIONS},
            losses={d: self.states[d]["losses"] for d in DIRECTIONS},
            timers={d: self.states[d]["timers"] for d in DIRECTIONS},
            rtt_samples={d: snapshots[d]["rtt_samples"] for d in DIRECTIONS},
            numeric_errors={d: self.states[d]["numeric_errors"] for d in DIRECTIONS},
            controller_events={
                d: self.states[d]["adapter"].events if self.states[d]["adapter"] else []
                for d in DIRECTIONS
            },
            controller_numeric_errors={
                d: (
                    getattr(self.states[d]["adapter"], "numeric_errors", [])
                    if self.states[d]["adapter"]
                    else []
                )
                for d in DIRECTIONS
            },
            persistent_events={
                d: self.states[d]["persistent_events"] for d in DIRECTIONS
            },
            pacer_final={d: self.pacers[d].snapshot() for d in self.pacers},
            pacer_errors={d: self.pacers[d].errors for d in self.pacers},
            ack_events={d: self.receivers[d].events for d in self.receivers},
            summary=dict(
                wire_bytes=sum(t["wire_bytes"] for t in self.traces),
                serialized_wire_bytes_by_horizon=str(
                    sum(
                        F(t["wire_bytes"])
                        * min(
                            F(1),
                            max(
                                F(0),
                                (self.until - F(t["send_start"]))
                                / (F(t["send_end"]) - F(t["send_start"])),
                            ),
                        )
                        for t in self.traces
                    )
                ),
                delivered_application_bytes=sum(
                    m["bytes"]
                    for key, m in self.application.messages.items()
                    if key in self.application.completed
                ),
                unique_received_application_bytes=sum(
                    b - a
                    for ranges in self.received_message.values()
                    for a, b in ranges
                ),
                complete=(
                    all(b["complete"] for b in businesses)
                    if businesses
                    else all(
                        k in self.application.completed
                        for k in self.application.messages
                    )
                ),
                all_messages_delivered=all(
                    k in self.application.completed for k in self.application.messages
                ),
                pending_packets={
                    d: sum(len(q) for q in self.queues[d].values()) for d in DIRECTIONS
                },
            ),
        )


def calculate(inputs):
    return Network(inputs).run()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--inputs", type=Path, required=True)
    ap.add_argument("--output", type=Path)
    a = ap.parse_args()
    result = calculate(json.loads(a.inputs.read_text()))
    text = json.dumps(result, indent=2) + "\n"
    if a.output:
        a.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
