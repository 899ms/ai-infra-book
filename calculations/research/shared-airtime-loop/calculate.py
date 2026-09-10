"""Research shared half-duplex access hop over the public media feedback engine."""

from pathlib import Path
from fractions import Fraction as F
from collections import deque
import argparse
import copy
import hashlib
import heapq
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parent
CALCULATIONS = ROOT.parent.parent
sys.path.insert(0, str(CALCULATIONS / "src"))
from infra_calc.transport import media_network as base

spec = importlib.util.spec_from_file_location(
    "shared_airtime_exchange", ROOT / "airtime.py"
)
airtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(airtime)


def json_value(value):
    if isinstance(value, F):
        return str(value)
    if isinstance(value, dict):
        return {k: json_value(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_value(v) for v in value]
    return value


def verify_sources():
    root = ROOT.parent / "shared-airtime-inputs"
    rows = json.loads((root / "sources.lock.json").read_text())
    for row in rows:
        data = (root / row["file"]).read_bytes()
        if (
            len(data) != row["bytes"]
            or hashlib.sha256(data).hexdigest() != row["sha256"]
        ):
            raise ValueError("airtime reference source changed: " + row["file"])
    return rows


class Network(base.Network):
    def __init__(self, inputs):
        clean = copy.deepcopy(inputs)
        self.radio = clean["network"].pop("wireless_access")
        super().__init__(clean)
        self.inputs = copy.deepcopy(inputs)
        if self.radio.get("enabled") is not True:
            raise ValueError("enabled wireless instance required")
        allowed = {
            "enabled",
            "mode",
            "profile",
            "max_attempts",
            "retry_wait",
            "failures",
        }
        if set(self.radio) - allowed:
            raise ValueError("unknown wireless_access keys")
        self.profile = self.radio["profile"]
        if not isinstance(self.profile, dict):
            raise ValueError("wireless profile must be an object")
        if self.radio.get("mode", "ofdm" if "phy" in self.profile else "abstract") != (
            "ofdm" if "phy" in self.profile else "abstract"
        ):
            raise ValueError("profile/mode mismatch")
        self.max_attempts = airtime.integer(
            self.radio.get("max_attempts", 1), "max_attempts", 1
        )
        if self.max_attempts > 16:
            raise ValueError("at most 16 MAC attempts")
        self.retry_wait = airtime.seconds(self.radio.get("retry_wait", 0), "retry wait")
        self.failures = {}
        if not isinstance(self.radio.get("failures", []), list):
            raise ValueError("failures must be a list")
        for item in self.radio.get("failures", []):
            if not isinstance(item, dict) or set(item) != {
                "direction",
                "pn",
                "attempt",
                "outcome",
            }:
                raise ValueError("MAC failure fields")
            key = (item["direction"], item["pn"], item["attempt"])
            if key[0] not in base.DIRECTIONS:
                raise ValueError("failure direction")
            airtime.integer(key[1], "failure PN")
            airtime.integer(key[2], "failure attempt", 1)
            if key in self.failures or key[2] > self.max_attempts:
                raise ValueError("duplicate or out-of-range MAC failure")
            outcome = item["outcome"]
            if outcome not in ("data_lost", "mac_ack_lost"):
                raise ValueError("failure outcome")
            airtime.exchange(self.profile, 1228, outcome)
            self.failures[key] = outcome
        airtime.exchange(self.profile, 1228)
        airtime.exchange(self.profile, 92, transport_ack=True)
        self.source_capture = False
        self.air_busy = False
        self.air_scheduled = set()
        self.air_pending = []
        self.air_serial = 0
        self.last_direction = None
        self.air_attempts = []
        self.air_reservations = []
        self.air_events = []
        self.air_received = set()
        self.wan_up_busy = False
        self.wan_up_queue = deque()
        self.air_sources = verify_sources()

    def schedule(self, at, priority, kind, data):
        if getattr(self, "source_capture", False) and kind in (
            "serial_done",
            "arrival",
            "router_admit",
        ):
            return
        # A server-origin packet reaches the AP only after the full WAN path.
        if kind == "arrival" and data["direction"] == "down":
            data["wan_arrival"] = str(at)
            data["arrival"] = None
            kind = "air_admit"
        super().schedule(at, priority, kind, data)

    def air_at(self, at):
        at = F(str(at))
        if at not in self.air_scheduled:
            self.air_scheduled.add(at)
            self.schedule(at, 3, "air_pump", None)

    def pump(self, direction):
        if direction == "down":
            super().pump(direction)
        else:
            self.update(direction)
            self.air_at(self.now)

    def client_candidate(self):
        self.update("up")
        candidates = sorted(
            self.heads("up"),
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
        for packet in candidates:
            _, reasons = self.states["up"]["validate_packet"](packet)
            if "up" in self.pacers and packet["in_flight"]:
                ready = self.pacers["up"].ready(self.now)
                if ready > self.now:
                    reasons = [*reasons, "pacer"]
                    self.air_at(ready)
            if not reasons:
                return packet
        return None

    def queue_air(self, record, attempt=1):
        self.air_serial += 1
        entry = dict(
            record=record, attempt=attempt, ready=self.now, order=self.air_serial
        )
        side = 0 if record["direction"] == "up" else 1
        heapq.heappush(self.air_pending, (self.now, side, self.air_serial, entry))
        if attempt == 1:
            record["ap_ready_at"] = str(self.now)
            record["arrival"] = None
        self.air_at(self.now)

    def air_pump(self):
        if self.air_busy:
            return
        candidate = self.client_candidate()
        options = []
        if candidate is not None:
            options.append(
                (F(candidate["ready_at"]), 0, candidate["enqueue_index"], None)
            )
        if self.air_pending:
            options.append(self.air_pending[0])
        if not options:
            return
        entry = min(options, key=lambda x: x[:3])[3]
        if entry is not None:
            heapq.heappop(self.air_pending)
        direction = "up" if entry is None else entry["record"]["direction"]
        packet = (
            candidate if entry is None else self.known[direction][entry["record"]["pn"]]
        )
        service = airtime.exchange(
            self.profile,
            packet["sent_bytes"] + 28,
            transport_ack=packet["kind"] == "ack",
            direction_switch=self.last_direction not in (None, direction),
        )
        self.air_busy = True
        reservation = dict(
            entry=entry,
            direction=direction,
            reserved=self.now,
            switch=self.last_direction not in (None, direction),
            access=service["data_start_offset"],
        )
        reservation["index"] = len(self.air_reservations)
        self.air_reservations.append(
            dict(
                start=str(self.now),
                data_start=str(self.now + reservation["access"]),
                end=None,
                direction=direction,
            )
        )
        self.air_events.append(
            dict(
                at=str(self.now),
                kind="air_reserved",
                direction=direction,
                data_start=str(self.now + reservation["access"]),
            )
        )
        self.schedule(
            self.now + reservation["access"], 3, "air_data_start", reservation
        )

    def air_start(self, reservation):
        entry = reservation["entry"]
        direction = reservation["direction"]
        if entry is None:
            before = len(self.traces)
            self.source_capture = True
            try:
                super().pump("up")
            finally:
                self.source_capture = False
            if len(self.traces) == before:
                self.air_busy = False
                self.air_reservations[reservation["index"]]["end"] = str(self.now)
                self.air_events.append(
                    dict(at=str(self.now), kind="reserved_direction_no_eligible_packet")
                )
                self.air_at(self.now)
                return
            record = self.traces[-1]
            record["arrival"] = None
            attempt = 1
        else:
            record, attempt = entry["record"], entry["attempt"]
        packet = self.known[direction][record["pn"]]
        outcome = self.failures.get((direction, record["pn"], attempt), "success")
        service = airtime.exchange(
            self.profile,
            record["wire_bytes"],
            outcome,
            transport_ack=record["kind"] == "ack",
            direction_switch=reservation["switch"],
        )
        if service["data_start_offset"] != reservation["access"]:
            raise ValueError(
                "profile access delay changed with actual packet selection"
            )
        start = reservation["reserved"]
        row = dict(
            index=len(self.air_attempts),
            direction=direction,
            pn=record["pn"],
            attempt=attempt,
            kind=record["kind"],
            reservation_start=str(start),
            data_start=str(self.now),
            data_end=str(start + service["data_end_offset"]),
            receive_at=(
                None
                if service["data_receive_offset"] is None
                else str(start + service["data_receive_offset"])
            ),
            feedback_at=str(start + service["mac_feedback_offset"]),
            end=str(start + service["exchange_end_offset"]),
            outcome=outcome,
            service=json_value(service),
            received=False,
            feedback_known=False,
        )
        if len(self.air_attempts) >= 400000:
            raise ValueError("wireless attempt budget exceeded")
        self.air_attempts.append(row)
        self.air_reservations[reservation["index"]]["end"] = row["end"]
        record.setdefault("wireless_attempt_indices", []).append(row["index"])
        if direction == "up" and attempt == 1:
            record["send_end"] = row["data_end"]
        self.last_direction = direction
        if row["receive_at"] is not None:
            self.schedule(F(row["receive_at"]), 0, "air_receive", (record, row))
        self.schedule(F(row["end"]), -1, "air_done", (record, row))

    def air_receive(self, record, row):
        row["received"] = True
        key = (record["direction"], record["pn"])
        duplicate = key in self.air_received
        self.air_received.add(key)
        row["duplicate_at_hop_receiver"] = duplicate
        if duplicate:
            # The MAC duplicate is filtered below transport in both directions.
            # Its local MAC ACK remains part of this attempt's service.
            return
        record["wireless_received_at"] = str(self.now)
        if record["direction"] == "up":
            self.wan_up_queue.append(record)
            self.wan_up_start()
        else:
            record["arrival"] = str(self.now)
            super().arrival(record)

    def air_done(self, record, row):
        row["feedback_known"] = True
        self.air_busy = False
        if record["direction"] == "up":
            self.busy["up"] = False
        self.air_events.append(
            dict(
                at=str(self.now),
                kind="mac_feedback",
                direction=record["direction"],
                pn=record["pn"],
                attempt=row["attempt"],
                outcome=row["outcome"],
            )
        )
        if row["outcome"] != "success":
            if row["attempt"] < self.max_attempts:
                self.schedule(
                    self.now + self.retry_wait,
                    1,
                    "air_retry",
                    (record, row["attempt"] + 1),
                )
            else:
                record["mac_retry_exhausted_at"] = str(self.now)
        self.air_at(self.now)

    def wan_up_start(self):
        if self.wan_up_busy or not self.wan_up_queue:
            return
        record = self.wan_up_queue.popleft()
        self.wan_up_busy = True
        end = self.now + F(8 * record["wire_bytes"]) / F(
            str(self.cfg["links"]["up"]["rate_bps"])
        )
        arrival = end + F(str(self.cfg["links"]["up"]["propagation"]))
        record.update(wan_start=str(self.now), wan_end=str(end), arrival=str(arrival))
        self.schedule(end, 1, "wan_up_done", None)
        if not record["dropped"]:
            if "up" in self.routers:
                self.schedule(arrival, 0, "router_admit", record)
                record["arrival"] = None
            else:
                self.schedule(arrival, 0, "arrival", record)

    def run(self):
        # Network orchestration only; application/transport/recovery algorithms
        # remain inherited and are never rerun from historical input events.
        while self.heap:
            self.now, _, _, kind, value = heapq.heappop(self.heap)
            if len(self.traces) > 200000:
                raise ValueError("packet budget exceeded")
            if kind == "air_pump":
                self.air_scheduled.discard(self.now)
                self.air_pump()
            elif kind == "air_data_start":
                self.air_start(value)
            elif kind == "air_admit":
                self.queue_air(value)
            elif kind == "air_receive":
                self.air_receive(*value)
            elif kind == "air_done":
                self.air_done(*value)
            elif kind == "air_retry":
                self.queue_air(*value)
            elif kind == "wan_up_done":
                self.wan_up_busy = False
                self.wan_up_start()
            elif kind == "app_ready":
                self.application.ready(value)
            elif kind == "app_dispatch":
                self.application.dispatch(value)
            elif kind == "app_task_done":
                self.application.task_done(*value)
            elif kind == "activate":
                self.activate(self.application.messages[value])
            elif kind == "arrival":
                super().arrival(value)
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
            else:
                raise ValueError("unknown network event: " + kind)
        result = super().run()
        # The old uniform IP-byte/serialization ratio is invalid inside PHY
        # preamble, symbols and padding. Preserve the key as explicitly unknown.
        result["summary"]["serialized_wire_bytes_by_horizon"] = None
        wan_bytes = F(0)
        for record in self.traces:
            if record["direction"] == "down":
                start, end = F(record["send_start"]), F(record["send_end"])
            elif "wan_start" in record:
                start, end = F(record["wan_start"]), F(record["wan_end"])
            else:
                continue
            wan_bytes += record["wire_bytes"] * min(
                F(1), max(F(0), (self.until - start) / (end - start))
            )
        result["summary"]["wan_serialized_ip_bytes_by_horizon"] = str(wan_bytes)
        result["wireless_attempts"] = self.air_attempts
        result["wireless_events"] = self.air_events
        result["wireless_reservations"] = self.air_reservations
        result["wireless_reference_sources"] = self.air_sources
        result["wireless_reference_root"] = str(ROOT.parent / "shared-airtime-inputs")
        result["wireless_summary"] = dict(
            attempts_started=len(self.air_attempts),
            same_pn_retry_attempts=sum(r["attempt"] > 1 for r in self.air_attempts),
            reserved_service_seconds=str(
                sum(F(r["end"]) - F(r["reservation_start"]) for r in self.air_attempts)
            ),
            observed_reserved_seconds=str(
                sum(
                    max(
                        F(0),
                        min(
                            self.until,
                            F(r["end"]) if r["end"] is not None else self.until,
                        )
                        - F(r["start"]),
                    )
                    for r in self.air_reservations
                )
            ),
            pending_ap_or_retry_packets=len(self.air_pending),
            pending_up_wan_packets=len(self.wan_up_queue),
            radio_busy_at_horizon=self.air_busy,
        )
        return result


def calculate(inputs):
    if not isinstance(inputs, dict) or set(inputs) != {"application", "network"}:
        raise ValueError("exact application/network input required")
    if not isinstance(inputs["network"], dict):
        raise ValueError("network must be an object")
    wireless = inputs["network"].get("wireless_access")
    if wireless is None:
        return base.calculate(inputs)
    if not isinstance(wireless, dict):
        raise ValueError("wireless_access must be an object")
    if wireless.get("enabled") is False:
        clean = copy.deepcopy(inputs)
        del clean["network"]["wireless_access"]
        return base.calculate(clean)
    return Network(inputs).run()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = calculate(json.loads(args.inputs.read_text()))
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
