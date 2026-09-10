"""RFC9002 section 7.6 evidence for a confirmed single Application PN space.

This is a pure predicate over sender history, not a loss detector. The caller
supplies complete packet history and separately tracks loss reports/episodes.
"""

from fractions import Fraction

from .reference_sources import reference_sources


def rational(value):
    if isinstance(value, bool):
        raise ValueError("Boolean is not a time value")
    return Fraction(str(value))


def evaluate(
    packets,
    *,
    smoothed_rtt,
    rttvar,
    max_ack_delay,
    granularity,
    max_datagram_size=1200,
    trigger="ack",
):
    """Return loss-span evidence; only ACK receipt may establish congestion.

    Each record contains pn, sent_at, status, ack_eliciting and the explicit
    rtt_known_at_send flag. The flag avoids guessing ordering when a first RTT
    sample and a packet send share a timestamp. All ACKed packets split a span,
    including retained late ACKs and non-ack-eliciting packets.
    """
    reference_sources("quic")
    smoothed, variance, delay, tick = map(
        rational, (smoothed_rtt, rttvar, max_ack_delay, granularity)
    )
    if smoothed <= 0 or variance < 0 or delay < 0 or tick <= 0:
        raise ValueError("Invalid RTT parameters")
    if type(max_datagram_size) is not int or max_datagram_size < 1200:
        raise ValueError("max_datagram_size must be an integer >=1200")
    if trigger not in ("ack", "loss_timer", "pto"):
        raise ValueError("Unsupported observation trigger")
    duration = 3 * (smoothed + max(4 * variance, tick) + delay)
    records = []
    seen = set()
    for packet in packets:
        if set(packet) != {
            "pn",
            "sent_at",
            "status",
            "ack_eliciting",
            "rtt_known_at_send",
        }:
            raise ValueError("Packet evidence must use the declared fields")
        pn = packet["pn"]
        if type(pn) is not int or pn < 0 or pn in seen:
            raise ValueError("Packet identity must be unique")
        seen.add(pn)
        at = rational(packet["sent_at"])
        if at < 0 or packet["status"] not in (
            "sent",
            "lost",
            "acked",
            "lost_then_acked",
        ):
            raise ValueError("Invalid packet time/status")
        if any(
            type(packet[k]) is not bool for k in ("ack_eliciting", "rtt_known_at_send")
        ):
            raise ValueError("Packet flags must be booleans")
        records.append((at, pn, packet))
    records.sort()
    if any(left[1] + 1 != right[1] for left, right in zip(records, records[1:])):
        raise ValueError("Complete contiguous PN history is required in this reference")
    prior_seen = False
    for _, _, packet in records:
        if prior_seen and not packet["rtt_known_at_send"]:
            raise ValueError(
                "Prior RTT knowledge cannot disappear on the confirmed path"
            )
        prior_seen |= packet["rtt_known_at_send"]

    evidence = []
    first = last = None

    def finish_span():
        if first is not None and last is not None and last[0] - first[0] > duration:
            evidence.append(
                dict(
                    first_pn=first[1],
                    last_pn=last[1],
                    start=str(first[0]),
                    end=str(last[0]),
                    duration=str(last[0] - first[0]),
                    evidence_key=f"{first[1]}:{last[1]}",
                )
            )

    for at, pn, packet in records:
        if packet["status"] in ("acked", "lost_then_acked"):
            finish_span()
            first = last = None
        elif (
            packet["status"] == "lost"
            and packet["ack_eliciting"]
            and packet["rtt_known_at_send"]
        ):
            first = first or (at, pn)
            last = (at, pn)
    finish_span()
    return dict(
        established=bool(evidence) and trigger == "ack",
        trigger=trigger,
        threshold_duration=str(duration),
        qualifying_spans=evidence,
        required_cwnd_bytes=(
            2 * max_datagram_size if evidence and trigger == "ack" else None
        ),
        scope="Confirmed single Application PN space; RTT state supplied at this observation; no PTO exponential factor.",
        integration="Caller must track unconsumed loss declarations and persistent episodes before applying minimum cwnd. evidence_key describes a span but is not sufficient for deduplication: late ACK can split old spans without new loss. Late ACKs do not automatically undo a prior action.",
    )
