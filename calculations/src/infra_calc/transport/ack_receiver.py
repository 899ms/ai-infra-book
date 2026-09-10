"""Bounded ACK range retention with actual-send snapshots; single Application space."""

from fractions import Fraction as F
import heapq


def varint_bytes(value):
    if type(value) is not int or not 0 <= value < 2**62:
        raise ValueError("QUIC varint outside range")
    for width, bound in ((1, 2**6), (2, 2**14), (4, 2**30), (8, 2**62)):
        if value < bound:
            return width


def validate(policy):
    allowed = {
        "mode",
        "every",
        "max_delay",
        "delay_exponent",
        "retain_packets",
        "reorder_immediate",
        "header_tag_bytes",
    }
    if (
        not isinstance(policy, dict)
        or set(policy) - allowed
        or policy.get("mode") != "count_or_timer"
    ):
        raise ValueError("invalid ACK policy")
    result = dict(
        every=2,
        max_delay="0.01",
        delay_exponent=3,
        retain_packets=256,
        reorder_immediate=True,
        header_tag_bytes=24,
    )
    result.update(policy)
    for key, low, high in (
        ("every", 1, 10000),
        ("delay_exponent", 0, 20),
        ("retain_packets", 1, 10000),
        ("header_tag_bytes", 17, 1200),
    ):
        if type(result[key]) is not int or not low <= result[key] <= high:
            raise ValueError("invalid " + key)
    if type(result["reorder_immediate"]) is not bool:
        raise ValueError("reorder policy must be bool")
    delay = F(str(result["max_delay"]))
    ms = delay * 1000
    if ms.denominator != 1 or not 0 <= ms < 2**14:
        raise ValueError("max_delay must be integer milliseconds below 2**14")
    if delay and delay < F(2 ** result["delay_exponent"], 1000000):
        raise ValueError("nonzero max_delay smaller than ACK encoding tick")
    result["max_delay"] = delay
    return result


class Receiver:
    def __init__(self, policy):
        self.policy = validate(policy)
        self.history = {}
        self.retained = set()
        self.retained_heap = []
        self.pending = set()
        self.largest = None
        self.largest_eliciting = None
        self.deadline = None
        self.generation = 0
        self.queued = False
        self.events = []
        self.now = F(0)

    def _time(self, now):
        now = F(str(now))
        if now < self.now:
            raise ValueError("receiver time reversal")
        return now

    def trigger(self, now, reason):
        if self.queued:
            return False
        self.queued = True
        self.events.append(
            dict(
                at=str(now), event="trigger", reason=reason, generation=self.generation
            )
        )
        return True

    def receive(self, pn, now, ack_eliciting):
        now = self._time(now)
        if (
            type(pn) is not int
            or not 0 <= pn < 2**62
            or type(ack_eliciting) is not bool
        ):
            raise ValueError("invalid received packet identity")
        if ack_eliciting and len(self.pending) >= 10000 and pn not in self.pending:
            raise ValueError("unreported ACK packet budget exceeded")
        duplicate = pn in self.history
        out_of_order = self.largest_eliciting is not None and (
            pn < self.largest_eliciting
            or (
                pn > self.largest_eliciting
                and not all(
                    n in self.history for n in range(self.largest_eliciting + 1, pn)
                )
            )
        )
        self.now = now
        if not duplicate:
            self.history[pn] = now
            self.retained.add(pn)
            heapq.heappush(self.retained_heap, pn)
            while len(self.retained) > self.policy["retain_packets"]:
                self.retained.remove(heapq.heappop(self.retained_heap))
        self.largest = pn if self.largest is None else max(self.largest, pn)
        self.events.append(
            dict(
                at=str(now),
                event="receive",
                pn=pn,
                ack_eliciting=ack_eliciting,
                duplicate=duplicate,
            )
        )
        if not ack_eliciting:
            return False
        self.largest_eliciting = (
            pn if self.largest_eliciting is None else max(self.largest_eliciting, pn)
        )
        self.pending.add(pn)
        if self.deadline is None:
            self.generation += 1
            self.deadline = now + self.policy["max_delay"]
        reason = (
            "duplicate"
            if duplicate
            else (
                "reorder"
                if out_of_order and self.policy["reorder_immediate"]
                else (
                    "count"
                    if len(self.pending) >= self.policy["every"]
                    else "zero_delay" if self.policy["max_delay"] == 0 else None
                )
            )
        )
        return self.trigger(now, reason) if reason else False

    def expire(self, now, generation):
        now = self._time(now)
        self.now = now
        if (
            generation != self.generation
            or self.deadline is None
            or now < self.deadline
            or not self.pending
        ):
            return False
        return self.trigger(now, "deadline")

    def snapshot(self, now, packet_bytes):
        now = self._time(now)
        if not self.queued or not self.pending:
            raise ValueError("no pending ACK snapshot")
        numbers = sorted(self.retained | self.pending)
        ranges = []
        for pn in numbers:
            if ranges and ranges[-1][1] + 1 == pn:
                ranges[-1][1] = pn
            else:
                ranges.append([pn, pn])
        largest = numbers[-1]
        raw_delay = now - self.history[largest]
        tick = F(2 ** self.policy["delay_exponent"], 1000000)
        encoded = int(raw_delay // tick)
        decoded = encoded * tick
        descending = list(reversed(ranges))
        values = [
            2,
            largest,
            encoded,
            len(ranges) - 1,
            descending[0][1] - descending[0][0],
        ]
        for previous, current in zip(descending, descending[1:]):
            values += [previous[0] - current[1] - 2, current[1] - current[0]]
        minimum = self.policy["header_tag_bytes"] + sum(varint_bytes(x) for x in values)
        if type(packet_bytes) is not int or packet_bytes < minimum:
            raise ValueError(
                "ACK snapshot exceeds declared packet capacity: " + str(minimum)
            )
        result = dict(
            ranges=ranges,
            largest=largest,
            largest_received_at=str(self.history[largest]),
            raw_delay=str(raw_delay),
            encoded_delay=encoded,
            delay_exponent=self.policy["delay_exponent"],
            decoded_delay=str(decoded),
            encoding_error=str(decoded - raw_delay),
            frame_bytes=minimum - self.policy["header_tag_bytes"],
            header_tag_bytes=self.policy["header_tag_bytes"],
            exceeds_max_delay=raw_delay > self.policy["max_delay"],
            covered_pending=len(self.pending),
            retention_packets=self.policy["retain_packets"],
        )
        self.events.append(dict(at=str(now), event="start", **result))
        self.now = now
        self.pending.clear()
        self.deadline = None
        self.queued = False
        self.generation += 1
        return result

    def state(self):
        return dict(
            pending=sorted(self.pending),
            deadline=None if self.deadline is None else str(self.deadline),
            queued=self.queued,
            generation=self.generation,
            retained=sorted(self.retained),
            received_count=len(self.history),
        )
