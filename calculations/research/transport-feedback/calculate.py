"""RFC9002 confirmed-path feedback replay with absolute STREAM limits.

Finite sender-visible event replay; not a network or automatic sending simulator.
"""

from fractions import Fraction as F
import hashlib
import heapq
import json
from pathlib import Path


def union(intervals):
    result = []
    for start, end in sorted(intervals):
        if result and start <= result[-1][1]:
            result[-1][1] = max(result[-1][1], end)
        else:
            result.append([start, end])
    return result


def calculate(inputs):
    p = json.loads(json.dumps(inputs))
    root = Path(__file__).resolve().parent
    sources = json.loads((root / "sources.lock.json").read_text())
    for source in sources:
        raw = (root / source["file"]).read_bytes()
        if (
            len(raw) != source["bytes"]
            or hashlib.sha256(raw).hexdigest() != source["sha256"]
        ):
            raise ValueError("source integrity mismatch")
    mds = p.get("max_datagram_size", 1200)
    if type(mds) is not int or mds < 1200:
        raise ValueError("max_datagram_size >=1200")
    horizon = F(str(p["until"]))
    granularity = F(str(p.get("granularity", "0.001")))
    ack_delay_max = F(str(p.get("max_ack_delay", "0.025")))
    if horizon < 0 or granularity <= 0 or ack_delay_max < 0:
        raise ValueError("invalid time settings")
    cwnd = F(str(p.get("initial_cwnd", min(10 * mds, max(2 * mds, 14720)))))
    if cwnd < 2 * mds:
        raise ValueError("initial cwnd below minimum")
    threshold = (
        F(str(p["initial_ssthresh"])) if p.get("initial_ssthresh") is not None else None
    )
    if threshold is not None and threshold <= 0:
        raise ValueError("invalid slow start threshold")
    max_data = p["initial_max_data"]
    stream_limits = dict(p["initial_max_stream_data"])
    if (
        type(max_data) is not int
        or not 0 <= max_data <= 2**62 - 1
        or any(not isinstance(k, str) or not k for k in stream_limits)
        or any(
            type(v) is not int or not 0 <= v <= 2**62 - 1
            for v in stream_limits.values()
        )
    ):
        raise ValueError("invalid absolute limits")
    initial_rtt = F(str(p.get("initial_rtt", "0.333")))
    if initial_rtt <= 0:
        raise ValueError("initial RTT positive")
    latest = F(0)
    smoothed = initial_rtt
    variance = initial_rtt / 2
    minimum = None
    first_sample = None
    if p.get("rtt_seed"):
        seed = p["rtt_seed"]
        latest = F(str(seed["latest_rtt"]))
        smoothed = F(str(seed["smoothed_rtt"]))
        variance = F(str(seed["rttvar"]))
        minimum = F(str(seed["min_rtt"]))
        first_sample = F(str(seed.get("first_sample_at", -1)))
        if min(latest, smoothed, minimum) <= 0 or variance < 0 or first_sample > 0:
            raise ValueError("invalid prior RTT seed")
    events = p["events"]
    if len(events) > 10000:
        raise ValueError("event limit")
    queue = []
    serial = 0
    generation = 0
    now = F(0)
    timer = None
    history = {}
    largest_sent = None
    largest_acked = None
    last_eliciting = None
    flight = 0
    pto_count = 0
    probe_allowance = 0
    recovery_start = None
    stream_high = {}
    acked_stream = {}
    datagrams = {}
    acked_datagrams = set()
    ledger = []
    timer_events = []
    loss_events = []
    rtt_events = []

    def schedule(at, priority, kind, value):
        nonlocal serial
        serial += 1
        heapq.heappush(queue, (at, priority, serial, kind, value))

    for event in events:
        at = F(str(event["at"]))
        if at < 0 or at > horizon:
            raise ValueError("event outside finite replay horizon")
        if event["type"] not in (
            "sent",
            "ack",
            "max_data",
            "max_stream_data",
            "can_send",
        ):
            raise ValueError("unknown event")
        schedule(
            at,
            (
                0
                if event["type"] in ("ack", "max_data", "max_stream_data")
                else 2 if event["type"] == "sent" else 3
            ),
            "external",
            event,
        )

    def outstanding():
        return [h for h in history.values() if h["status"] == "sent"]

    def pto_period():
        return smoothed + max(4 * variance, granularity) + ack_delay_max

    def arm():
        nonlocal generation, timer
        generation += 1
        timer = None
        delay = max(F(9, 8) * max(latest, smoothed), granularity)
        eligible = [
            h["time"] + delay
            for pn, h in history.items()
            if h["status"] == "sent"
            and largest_acked is not None
            and pn <= largest_acked
        ]
        if eligible:
            timer = {"kind": "loss", "at": str(max(now, min(eligible)))}
        elif any(h["ack_eliciting"] and h["in_flight"] for h in outstanding()):
            timer = {
                "kind": "pto",
                "at": str(max(now, last_eliciting + pto_period() * 2**pto_count)),
            }
        if timer and F(timer["at"]) <= horizon:
            schedule(F(timer["at"]), 1, "timer", {"generation": generation, **timer})

    def state():
        return {
            "bytes_in_flight": flight,
            "cwnd": str(cwnd),
            "ssthresh": str(threshold) if threshold is not None else None,
            "recovery_start": (
                str(recovery_start) if recovery_start is not None else None
            ),
            "latest_rtt": str(latest),
            "smoothed_rtt": str(smoothed),
            "rttvar": str(variance),
            "min_rtt": str(minimum) if minimum is not None else None,
            "pto_count": pto_count,
            "probe_allowance": probe_allowance,
            "largest_acked": largest_acked,
            "next_timer": dict(timer) if timer else None,
            "max_data": max_data,
            "max_stream_data": dict(stream_limits),
            "stream_highest_sent_offsets": dict(stream_high),
            "max_data_consumed": sum(stream_high.values()),
        }

    def validate_packet(e):
        sent = e["sent_bytes"]
        if type(sent) is not int or sent < 1 or sent > mds:
            raise ValueError("sent_bytes outside declared UDP payload limit")
        for name in ("ack_eliciting", "in_flight", "probe"):
            if type(e.get(name, False)) is not bool:
                raise ValueError("packet flags must be booleans")
        if e.get("ack_eliciting", True) and not e.get("in_flight", True):
            raise ValueError("ack eliciting packet must count in flight")
        frames = e.get("frames", [])
        ends = dict(stream_high)
        payload = 0
        packet_intervals = {}
        new_datagrams = []
        for frame in frames:
            length = frame["length"]
            if type(length) is not int or length <= 0:
                raise ValueError("positive frame payload length")
            payload += length
            if frame["type"] == "stream":
                stream = frame["stream"]
                offset = frame["offset"]
                if (
                    stream not in stream_limits
                    or type(offset) is not int
                    or offset < 0
                    or offset + length > 2**62 - 1
                ):
                    raise ValueError("invalid stream offset or unknown stream")
                intervals = packet_intervals.setdefault(stream, [])
                if any(offset < b and offset + length > a for a, b in intervals):
                    raise ValueError("overlapping STREAM frames in one packet")
                intervals.append((offset, offset + length))
                ends[stream] = max(ends.get(stream, 0), offset + length)
            elif frame["type"] == "datagram":
                if not isinstance(frame["id"], str) or not frame["id"]:
                    raise ValueError(
                        "DATAGRAM application identity must be nonempty string"
                    )
                if frame["id"] in datagrams or frame["id"] in new_datagrams:
                    raise ValueError("DATAGRAM retransmission identity is unsupported")
                new_datagrams.append(frame["id"])
            else:
                raise ValueError("unknown payload frame")
        if frames and (
            not e.get("ack_eliciting", True) or not e.get("in_flight", True)
        ):
            raise ValueError("STREAM/DATAGRAM require ack-eliciting in-flight packets")
        if payload + 32 > sent:
            raise ValueError(
                "payload does not fit declared minimum QUIC frame/header/tag budget"
            )
        reasons = []
        if (
            e.get("in_flight", True)
            and flight + sent > cwnd
            and not e.get("probe", False)
        ):
            reasons.append("cwnd")
        if sum(ends.values()) > max_data:
            reasons.append("MAX_DATA")
        reasons.extend(
            "MAX_STREAM_DATA:" + stream
            for stream, end in ends.items()
            if end > stream_limits[stream]
        )
        if e.get("probe", False) and (
            probe_allowance <= 0 or not e.get("ack_eliciting", True)
        ):
            reasons.append("no_ack_eliciting_PTO_probe_opportunity")
        return ends, reasons

    def detect_loss():
        nonlocal flight, cwnd, threshold, recovery_start
        lost = []
        delay = max(F(9, 8) * max(latest, smoothed), granularity)
        if largest_acked is None:
            return lost
        for pn, h in history.items():
            if h["status"] != "sent" or pn > largest_acked:
                continue
            by_packet = largest_acked >= pn + 3
            by_time = h["time"] + delay <= now
            if by_packet or by_time:
                h["status"] = "lost"
                h["lost_at"] = str(now)
                lost.append(pn)
                if h["in_flight"]:
                    flight -= h["sent_bytes"]
                loss_events.append(
                    {
                        "at": str(now),
                        "pn": pn,
                        "packet_threshold": by_packet,
                        "time_threshold": by_time,
                    }
                )
        congestion = [history[pn] for pn in lost if history[pn]["in_flight"]]
        if congestion:
            latest_lost = max(h["time"] for h in congestion)
            if recovery_start is None or latest_lost > recovery_start:
                recovery_start = now
                threshold = cwnd / 2
                cwnd = max(threshold, 2 * mds)
        # A finite stage-one guard prevents claiming complete NewReno when the
        # declared history reaches the separately unimplemented persistent case.
        if first_sample is not None:
            candidates = sorted(
                (
                    h
                    for h in history.values()
                    if h["status"] == "lost"
                    and h["ack_eliciting"]
                    and h["time"] > first_sample
                ),
                key=lambda h: h["time"],
            )
            for first in candidates:
                for last in candidates:
                    if last["time"] - first["time"] > 3 * pto_period() and not any(
                        h["status"] in ("acked", "lost_then_acked")
                        and first["time"] <= h["time"] <= last["time"]
                        for h in history.values()
                    ):
                        raise ValueError(
                            "persistent congestion interval outside this stage-one reference scope"
                        )
        return lost

    def acknowledge(e):
        nonlocal largest_acked, latest, minimum, smoothed, variance, first_sample, flight, cwnd, pto_count, probe_allowance
        ranges = e["ranges"]
        if not isinstance(ranges, list) or not ranges or len(ranges) > 10000:
            raise ValueError("ACK ranges required")
        numbers = set()
        for item in ranges:
            if (
                not isinstance(item, list)
                or len(item) != 2
                or any(type(n) is not int for n in item)
                or item[0] < 0
                or item[1] < item[0]
                or largest_sent is None
                or item[1] > largest_sent
                or item[1] - item[0] > 10000
            ):
                raise ValueError("invalid ACK range")
            interval = set(range(item[0], item[1] + 1))
            if numbers & interval:
                raise ValueError("overlapping ACK ranges")
            numbers |= interval
        if any(pn not in history for pn in numbers):
            raise ValueError("ACK acknowledges unsent packet")
        delay = F(str(e.get("ack_delay", 0)))
        if delay < 0:
            raise ValueError("negative ACK delay")
        for flag in ("app_limited", "flow_limited"):
            if type(e.get(flag, False)) is not bool:
                raise ValueError("limited flags must be boolean")
        newly = [
            history[pn] for pn in sorted(numbers) if history[pn]["status"] == "sent"
        ]
        late = [
            history[pn] for pn in sorted(numbers) if history[pn]["status"] == "lost"
        ]
        largest = max(numbers)
        largest_acked = (
            max(largest_acked, largest) if largest_acked is not None else largest
        )
        for h in newly + late:
            for frame in h["frames"]:
                if frame["type"] == "stream":
                    acked_stream[frame["stream"]] = union(
                        acked_stream.get(frame["stream"], [])
                        + [[frame["offset"], frame["offset"] + frame["length"]]]
                    )
                else:
                    acked_datagrams.add(frame["id"])
        for h in late:
            h["status"] = "lost_then_acked"
            h["acked_at"] = str(now)
        if not newly:
            return {
                "newly_acked": [],
                "late_acked": [h["pn"] for h in late],
                "newly_lost": [],
            }
        if newly[-1]["pn"] == largest and any(h["ack_eliciting"] for h in newly):
            latest = now - newly[-1]["time"]
            if latest <= 0:
                raise ValueError("RTT sample must be positive")
            adjusted = latest
            if first_sample is None:
                minimum = latest
                smoothed = latest
                variance = latest / 2
                first_sample = now
            else:
                minimum = min(minimum, latest)
                bounded = min(delay, ack_delay_max)
                if latest >= minimum + bounded:
                    adjusted = latest - bounded
                # Verified RFC9002 Errata7539 corrects section5.3 to use
                # the previous SRTT for variance, matching Appendix A.7.
                variance = F(3, 4) * variance + F(1, 4) * abs(smoothed - adjusted)
                smoothed = F(7, 8) * smoothed + F(1, 8) * adjusted
            rtt_events.append(
                {
                    "at": str(now),
                    "pn": largest,
                    "raw": str(latest),
                    "adjusted": str(adjusted),
                    "smoothed": str(smoothed),
                    "rttvar": str(variance),
                }
            )
        for h in newly:
            h["status"] = "acked"
            h["acked_at"] = str(now)
        lost = detect_loss()
        for h in newly:
            if not h["in_flight"]:
                continue
            flight -= h["sent_bytes"]
            if (
                e.get("app_limited", False)
                or e.get("flow_limited", False)
                or (recovery_start is not None and h["time"] <= recovery_start)
            ):
                continue
            if threshold is None or cwnd < threshold:
                cwnd += h["sent_bytes"]
            else:
                cwnd += F(mds * h["sent_bytes"], 1) / cwnd
        pto_count = 0
        probe_allowance = 0
        return {
            "newly_acked": [h["pn"] for h in newly],
            "late_acked": [h["pn"] for h in late],
            "newly_lost": lost,
        }

    while queue:
        at, priority, _, kind, event = heapq.heappop(queue)
        if kind == "timer" and event["generation"] != generation:
            continue
        now = at
        details = {}
        if len(ledger) > 100000:
            raise ValueError("processed event budget")
        if kind == "timer":
            if event["kind"] == "loss":
                details["newly_lost"] = detect_loss()
            else:
                if pto_count >= 32:
                    raise ValueError("PTO replay backoff exceeds finite bound")
                pto_count += 1
                probe_allowance = 2
                details["probe_opportunities"] = 2
            timer_events.append({"at": str(now), "kind": event["kind"], **details})
        elif event["type"] in ("sent", "can_send"):
            ends, reasons = validate_packet(event)
            details = {"can_send": not reasons, "blocked_by": reasons}
            if event["type"] == "sent":
                if reasons:
                    raise ValueError(
                        "observed send violates sender-visible gates: "
                        + ",".join(reasons)
                    )
                pn = event["pn"]
                if (
                    type(pn) is not int
                    or pn < 0
                    or (largest_sent is not None and pn != largest_sent + 1)
                ):
                    raise ValueError(
                        "PN must be new and contiguous in this reference trace"
                    )
                if largest_sent is None and pn != 0:
                    raise ValueError("first PN must be zero in this finite trace")
                largest_sent = pn
                h = {
                    "pn": pn,
                    "time": now,
                    "sent_at": str(now),
                    "sent_bytes": event["sent_bytes"],
                    "frames": event.get("frames", []),
                    "ack_eliciting": event.get("ack_eliciting", True),
                    "in_flight": event.get("in_flight", True),
                    "status": "sent",
                    "probe": event.get("probe", False),
                }
                history[pn] = h
                stream_high = ends
                for frame in h["frames"]:
                    if frame["type"] == "datagram":
                        datagrams[frame["id"]] = frame["length"]
                if h["in_flight"]:
                    flight += h["sent_bytes"]
                if h["ack_eliciting"] and h["in_flight"]:
                    last_eliciting = now
                if h["probe"]:
                    probe_allowance -= 1
        elif event["type"] == "ack":
            details = acknowledge(event)
        elif event["type"] == "max_data":
            value = event["value"]
            if type(value) is not int or not 0 <= value <= 2**62 - 1:
                raise ValueError("invalid MAX_DATA")
            max_data = max(max_data, value)
        elif event["type"] == "max_stream_data":
            value = event["value"]
            stream = event["stream"]
            if (
                stream not in stream_limits
                or type(value) is not int
                or not 0 <= value <= 2**62 - 1
            ):
                raise ValueError("invalid MAX_STREAM_DATA")
            stream_limits[stream] = max(stream_limits[stream], value)
        arm()
        ledger.append(
            {
                "at": str(now),
                "event": event["kind"] + "_timer" if kind == "timer" else event["type"],
                "input": event if kind != "timer" else None,
                "details": details,
                "state": state(),
            }
        )
    clean_history = []
    for h in history.values():
        clean_history.append({k: v for k, v in h.items() if k != "time"})
    return {
        "calculation": "rfc9002-confirmed-application-feedback-reference",
        "inputs": p,
        "reference_sources": sources,
        "events": ledger,
        "packets": clean_history,
        "loss_events": loss_events,
        "timer_events": timer_events,
        "rtt_samples": rtt_events,
        "final_state": state(),
        "sender_confirmed_business": {
            "stream_intervals": acked_stream,
            "unique_stream_bytes": sum(
                b - a for intervals in acked_stream.values() for a, b in intervals
            ),
            "acked_datagram_ids": sorted(acked_datagrams),
            "acked_datagram_bytes": sum(datagrams[k] for k in acked_datagrams),
        },
        "summary": {
            "sent_udp_payload_bytes": sum(h["sent_bytes"] for h in history.values()),
            "stream_payload_transmission_bytes": sum(
                f["length"]
                for h in history.values()
                for f in h["frames"]
                if f["type"] == "stream"
            ),
            "datagram_payload_transmission_bytes": sum(
                f["length"]
                for h in history.values()
                for f in h["frames"]
                if f["type"] == "datagram"
            ),
            "declared_quic_overhead_padding_control_bytes": sum(
                h["sent_bytes"] - sum(f["length"] for f in h["frames"])
                for h in history.values()
            ),
            "last_processed_event": str(now),
            "replay_until": str(horizon),
        },
        "limitations": [
            "Single already-confirmed validated path and Application PN space, no ECN/migration/handshake.",
            "RFC9002 section5.3 corrected by Verified Errata7539 RTT ordering and AppendixB rational NewReno ACK/loss reference; persistent congestion explicitly rejected.",
            "Explicit sender-observed input trace, no serialization/network/receiver/pacer or automatic retransmission scheduler.",
            "PTO grants at most two probe opportunities; actual probe sent events must be supplied and still obey absolute flow limits.",
            "ACK-confirmed byte coverage is sender evidence of transport receipt, not receiver application delivery or playback.",
            "Lost records retained for late ACK business coverage; late ACK alone does not resample RTT, regrow cwnd or release flight twice.",
        ],
    }


def example():
    return {
        "max_datagram_size": 1200,
        "initial_max_data": 100000,
        "initial_max_stream_data": {"A": 100000},
        "until": "0.32",
        "events": [
            {
                "type": "sent",
                "at": 0,
                "pn": 0,
                "sent_bytes": 1200,
                "frames": [
                    {"type": "stream", "stream": "A", "offset": 0, "length": 100}
                ],
            },
            {"type": "ack", "at": "0.1", "ranges": [[0, 0]], "ack_delay": 0},
            {
                "type": "sent",
                "at": "0.2",
                "pn": 1,
                "sent_bytes": 1200,
                "frames": [
                    {"type": "stream", "stream": "A", "offset": 100, "length": 100}
                ],
            },
            {"type": "ack", "at": "0.32", "ranges": [[1, 1]], "ack_delay": "0.02"},
        ],
    }


def scenarios():
    rows = {}
    p = example()
    p["until"] = "0.4"
    p["events"].append(
        {"type": "ack", "at": "0.35", "ranges": [[0, 1]], "ack_delay": 0}
    )
    rows["rtt-duplicate-ack"] = p
    p = example()
    p["until"] = "0.38"
    p["events"][-1]["at"] = "0.38"
    rows["rtt-verified-errata"] = p
    seed = {
        "latest_rtt": "0.1",
        "smoothed_rtt": "0.1",
        "rttvar": "0.0375",
        "min_rtt": "0.1",
        "first_sample_at": -1,
    }
    p = example()
    p.update(rtt_seed=seed, until="0.115")
    p["events"] = [
        {
            "type": "sent",
            "at": str(F(i, 1000)),
            "pn": i,
            "sent_bytes": 1200,
            "frames": [{"type": "stream", "stream": "A", "offset": i, "length": 1}],
        }
        for i in range(4)
    ] + [{"type": "ack", "at": "0.103", "ranges": [[3, 3]], "ack_delay": 0}]
    rows["packet-and-time-threshold"] = p
    p = json.loads(json.dumps(p))
    p["events"].append(
        {"type": "ack", "at": "0.1135", "ranges": [[1, 1]], "ack_delay": "0.0125"}
    )
    rows["ack-at-loss-deadline"] = p
    p = example()
    p.update(rtt_seed=seed, until="1.9")
    p["events"] = [
        {
            "type": "sent",
            "at": 1,
            "pn": 0,
            "sent_bytes": 1200,
            "frames": [{"type": "stream", "stream": "A", "offset": 0, "length": 10}],
        }
    ]
    rows["tail-no-feedback-pto"] = p
    p = json.loads(json.dumps(p))
    p["events"] += [
        {
            "type": "sent",
            "at": "1.275",
            "pn": 1,
            "sent_bytes": 1200,
            "probe": True,
            "frames": [{"type": "stream", "stream": "A", "offset": 0, "length": 10}],
        },
        {"type": "ack", "at": "1.375", "ranges": [[0, 1]], "ack_delay": 0},
    ]
    rows["probe-then-ack-reset"] = p
    p = example()
    p.update(rtt_seed=seed, until="1.275")
    p["events"] = [
        {"type": "sent", "at": 1, "pn": 0, "sent_bytes": 1200, "frames": []},
        {"type": "ack", "at": "1.275", "ranges": [[0, 0]], "ack_delay": 0},
    ]
    rows["ack-at-pto-deadline"] = p
    p = example()
    p.update(initial_max_data=6, initial_max_stream_data={"A": 4, "B": 2}, until=6)
    p["events"] = [
        {
            "type": "sent",
            "at": 0,
            "pn": 0,
            "sent_bytes": 1200,
            "frames": [{"type": "stream", "stream": "A", "offset": 0, "length": 4}],
        },
        {
            "type": "sent",
            "at": "0.001",
            "pn": 1,
            "sent_bytes": 1200,
            "frames": [{"type": "stream", "stream": "B", "offset": 0, "length": 2}],
        },
        {
            "type": "ack",
            "at": "0.1",
            "ranges": [[0, 1]],
            "ack_delay": 0,
            "flow_limited": True,
        },
    ]
    query = {
        "type": "can_send",
        "sent_bytes": 1200,
        "frames": [{"type": "stream", "stream": "A", "offset": 4, "length": 2}],
    }
    p["events"] += [
        dict(query, at=4),
        {"type": "max_data", "at": 5, "value": 8},
        dict(query, at=5),
        {"type": "max_stream_data", "at": 6, "stream": "A", "value": 6},
        dict(query, at=6),
    ]
    rows["absolute-flow-feedback"] = p
    p = example()
    p.update(initial_max_data=6, initial_max_stream_data={"A": 6}, until="0.3")
    p["events"] = [
        {
            "type": "sent",
            "at": 0,
            "pn": 0,
            "sent_bytes": 1200,
            "frames": [{"type": "stream", "stream": "A", "offset": 5, "length": 1}],
        },
        {"type": "ack", "at": "0.1", "ranges": [[0, 0]], "ack_delay": 0},
        {
            "type": "sent",
            "at": "0.2",
            "pn": 1,
            "sent_bytes": 1200,
            "frames": [{"type": "stream", "stream": "A", "offset": 0, "length": 5}],
        },
        {"type": "ack", "at": "0.3", "ranges": [[1, 1]], "ack_delay": 0},
    ]
    rows["stream-offset-high-water"] = p
    p = example()
    p.update(initial_max_data=0, initial_max_stream_data={"A": 0}, until="0.1")
    p["events"] = [
        {
            "type": "sent",
            "at": 0,
            "pn": 0,
            "sent_bytes": 1200,
            "frames": [{"type": "datagram", "id": "audio0", "length": 100}],
        },
        {"type": "ack", "at": "0.1", "ranges": [[0, 0]], "ack_delay": 0},
    ]
    rows["datagram-without-stream-credit"] = p
    for label, ack_eliciting, in_flight in [
        ("ack-only", False, False),
        ("padding-only", False, True),
    ]:
        p = example()
        p.update(until="0.5")
        p["events"] = [
            {
                "type": "sent",
                "at": 0,
                "pn": 0,
                "sent_bytes": 1200,
                "ack_eliciting": ack_eliciting,
                "in_flight": in_flight,
                "frames": [],
            }
        ]
        rows[label] = p
    p = json.loads(json.dumps(rows["packet-and-time-threshold"]))
    p["until"] = "0.204"
    p["events"] += [
        {
            "type": "sent",
            "at": "0.104",
            "pn": 4,
            "sent_bytes": 1200,
            "frames": [{"type": "stream", "stream": "A", "offset": 0, "length": 1}],
        },
        {"type": "ack", "at": "0.12", "ranges": [[0, 0]], "ack_delay": 0},
        {"type": "ack", "at": "0.204", "ranges": [[4, 4]], "ack_delay": 0},
    ]
    rows["new-pn-old-offset-recovery"] = p
    p = example()
    p.update(rtt_seed=seed, initial_cwnd=2400, until="0.276")
    p["events"] = [
        {
            "type": "sent",
            "at": str(F(i, 1000)),
            "pn": i,
            "sent_bytes": 1200,
            "frames": [],
        }
        for i in range(2)
    ]
    p["events"].append(
        {
            "type": "sent",
            "at": "0.276",
            "pn": 2,
            "sent_bytes": 1200,
            "probe": True,
            "frames": [],
        }
    )
    rows["pto-probe-over-cwnd"] = p
    return rows


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--inputs", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = (
        calculate(json.loads(args.inputs.read_text()))
        if args.inputs
        else {name: calculate(inputs) for name, inputs in scenarios().items()}
    )
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
