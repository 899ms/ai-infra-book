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


def create_sender(inputs):
    p = json.loads(json.dumps(inputs))
    root = Path(__file__).resolve().parent.parent / "transport-feedback"
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
    watermark = F(0)
    processed_priority = -1
    processed_count = 0
    timer = None
    history = {}
    active = {}
    numeric_errors = []
    quantum = F(str(p["numeric_quantum"])) if "numeric_quantum" in p else None
    if quantum is not None and (quantum <= 0 or quantum > granularity):
        raise ValueError(
            "numeric quantum must be positive and no coarser than timer granularity"
        )
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

    def outstanding():
        return list(active.values())

    def pto_period():
        return smoothed + max(4 * variance, granularity) + ack_delay_max

    def arm():
        nonlocal generation, timer, latest, smoothed, variance, cwnd, threshold
        if quantum is not None:
            values = {
                "latest": latest,
                "smoothed": smoothed,
                "variance": variance,
                "cwnd": cwnd,
                "threshold": threshold,
            }
            for key, value in values.items():
                if value is None:
                    continue
                rounded = round(value / quantum) * quantum
                if value > 0 and rounded <= 0:
                    rounded = quantum
                if key == "cwnd":
                    rounded = max(rounded, F(2 * mds))
                if rounded != value:
                    numeric_errors.append(
                        {
                            "at": str(now),
                            "field": key,
                            "original": str(value),
                            "rounded": str(rounded),
                            "local_error": str(rounded - value),
                        }
                    )
                values[key] = rounded
            latest, smoothed, variance, cwnd, threshold = (
                values[k]
                for k in ("latest", "smoothed", "variance", "cwnd", "threshold")
            )
        generation += 1
        timer = None
        delay = max(F(9, 8) * max(latest, smoothed), granularity)
        eligible = [
            h["time"] + delay
            for pn, h in active.items()
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
        for pn, h in list(active.items()):
            if h["status"] != "sent" or pn > largest_acked:
                continue
            by_packet = largest_acked >= pn + 3
            by_time = h["time"] + delay <= now
            if by_packet or by_time:
                h["status"] = "lost"
                active.pop(pn)
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
            if quantum is None and any(
                max(v.numerator.bit_length(), v.denominator.bit_length()) > 12000
                for v in (latest, smoothed, variance, cwnd)
            ):
                raise ValueError(
                    "exact rational state exceeds budget; declare numeric_quantum for long traces"
                )
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
            active.pop(h["pn"], None)
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

    def process_next():
        nonlocal processed_priority, processed_count
        nonlocal now, largest_sent, stream_high, flight, last_eliciting, probe_allowance, pto_count, max_data
        at, priority, _, kind, event = heapq.heappop(queue)
        if kind == "timer" and event["generation"] != generation:
            return False
        processed_priority = priority if at == now else priority
        now = at
        details = {}
        processed_count += 1
        if processed_count > 200000:
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
                if h["in_flight"] or p.get("track_ack_only", True):
                    active[pn] = h
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
        if not p.get("retain_ledger", True) and len(ledger) > 1:
            del ledger[:-1]
        return True

    def result():
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
                "sent_udp_payload_bytes": sum(
                    h["sent_bytes"] for h in history.values()
                ),
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

    def enqueue(event):
        at = F(str(event["at"]))
        if at < watermark or at > horizon:
            raise ValueError("event outside advancing sender horizon")
        if event["type"] not in (
            "sent",
            "ack",
            "max_data",
            "max_stream_data",
            "can_send",
        ):
            raise ValueError("unknown sender event")
        priority = (
            0
            if event["type"] in ("ack", "max_data", "max_stream_data")
            else 2 if event["type"] == "sent" else 3
        )
        if at == now and priority < processed_priority:
            raise ValueError("same-time event arrives after higher-priority processing")
        schedule(at, priority, "external", event)

    def advance(until, inclusive=True):
        nonlocal watermark
        boundary = F(str(until))
        if type(inclusive) is not bool or boundary < watermark or boundary > horizon:
            raise ValueError("invalid advancing boundary")
        watermark = boundary
        while queue and (
            queue[0][0] < boundary or (inclusive and queue[0][0] == boundary)
        ):
            process_next()
        return state()

    return dict(
        enqueue=enqueue,
        advance=advance,
        state=state,
        result=result,
        validate_packet=validate_packet,
        history=history,
        ledger=ledger,
        losses=loss_events,
        timers=timer_events,
        numeric_errors=numeric_errors,
        active=active,
        acked_stream=acked_stream,
    )
