"""Sender-visible QUIC-PN mapping into fixed Linux BBR state (not Linux TCP)."""

from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import sys
import hashlib
import json

CONTROLLERS = Path(__file__).resolve().parent.parent / "congestion-controllers"
if str(CONTROLLERS) not in sys.path:
    sys.path.insert(0, str(CONTROLLERS))
from bbr_state import BBR, Ack
from bbr_reference import rate_sample, stamp_us_delta, integer, boolean


def seconds(value):
    if type(value) not in (int, str, F):
        raise ValueError("Exact seconds require int, Fraction or string")
    result = F(value)
    if result < 0:
        raise ValueError("Negative time")
    return result


def microseconds(value):
    return 1 + int(seconds(value) * 1000000)


class BbrAdapter:
    """Both per-PN transport delivery and actual UDP-byte ledgers are retained."""

    def __init__(
        self,
        mds=1200,
        initial_cwnd=None,
        initial_rtt="1/10",
        config=None,
        *,
        initial_cwnd_packets=10,
        require_padding=True,
        random_draws=(0,) * 100,
    ):
        root = Path(__file__).resolve().parent
        for row in json.loads((root / "bbr-adapter-lock.json").read_text())["files"]:
            if (
                hashlib.sha256((root / row["file"]).read_bytes()).hexdigest()
                != row["sha256"]
            ):
                raise ValueError("Reviewed BBR module changed: " + row["file"])
        config = {} if config is None else dict(config)
        require_padding = config.get("pad_in_flight", require_padding)
        random_draws = config.get("bbr_random_draws", random_draws)
        integer(mds, "mds", 1200)
        if initial_cwnd is not None:
            if F(initial_cwnd).denominator != 1 or int(initial_cwnd) % mds:
                raise ValueError("BBR initial cwnd must be whole MDS packets")
            initial_cwnd_packets = int(initial_cwnd) // mds
        integer(mds, "mds", 1200)
        boolean(require_padding, "require_padding")
        rtt = max(1, int(seconds(initial_rtt) * 1000000))
        self.external_pacer = config.get("external_pacer", False)
        boolean(self.external_pacer, "external_pacer")
        self.mds = mds
        self.require_padding = require_padding
        seed_known = config.get("bbr_rtt_seed_known", False)
        boolean(seed_known, "bbr_rtt_seed_known")
        self.rtt_seed_known = seed_known
        self.core = BBR(
            cwnd=initial_cwnd_packets,
            min_rtt_us=rtt if seed_known else 0xFFFFFFFF,
            srtt_us_x8=rtt * 8 if seed_known else 0,
            mss_bytes=mds,
            random_draws=random_draws,
            now_us=1,
        )
        self.records = {}
        self.delivered = 0
        self.delivered_udp_bytes = 0
        self.lost = 0
        self.first_tx_us = 1
        self.delivered_mstamp_us = 1
        self.next_send = F(0)
        self.pending_losses = 0
        self.recovery_cutoff = None
        self.events = []
        self.limited_state = {"app_limited": False, "flow_limited": False}
        self.app_limited_marker = 0

    @property
    def cwnd_bytes(self):
        return self.core.cwnd * self.mds

    @property
    def pacing_rate_quic_bytes_per_second(self):
        return self.core.pacing_rate

    def active(self):
        return [
            r
            for r in self.records.values()
            if r["counted"] and not r["acked"] and not r["lost"]
        ]

    def _flight(self, supplied):
        actual = sum(r["sent_bytes"] for r in self.active())
        if supplied is not None and supplied != actual:
            raise ValueError(f"Sender flight mismatch {supplied} != {actual}")
        return len(self.active())

    def _on_sent(self, packet, now, flight_before=None, limited_flags=None):
        at = seconds(now)
        flags = limited_flags or {}
        for key in ("app_limited", "flow_limited"):
            boolean(flags.get(key, False), key)
        pn = packet["pn"]
        integer(pn, "pn")
        if pn in self.records:
            raise ValueError("Duplicate actual transmission PN")
        size = packet["sent_bytes"]
        integer(size, "sent_bytes", 1)
        for key in ("in_flight", "ack_eliciting"):
            boolean(packet[key], key)
        if packet["in_flight"] and not packet["ack_eliciting"]:
            raise ValueError("Padding-only non-eliciting flight outside BBR mapping")
        counted = packet["in_flight"] and packet["ack_eliciting"]
        if counted and self.require_padding and size != self.mds:
            raise ValueError(
                "BBR primary comparison requires every flight PN padded to MDS"
            )
        self._flight(flight_before)
        if counted and not self.external_pacer and at < self.next_send:
            raise ValueError("Actual send precedes pacer eligibility")
        if counted and not self.active():
            self.first_tx_us = self.delivered_mstamp_us = microseconds(at)
        record = dict(
            pn=pn,
            sent_bytes=size,
            at=str(at),
            sent_us=microseconds(at),
            counted=counted,
            acked=False,
            lost=False,
            frames=deepcopy(packet.get("frames", [])),
            prior_delivered=self.delivered,
            prior_delivered_udp_bytes=self.delivered_udp_bytes,
            first_tx_us=self.first_tx_us,
            delivered_mstamp_us=self.delivered_mstamp_us,
            app_limited=flags.get("app_limited", False),
            flow_limited=flags.get("flow_limited", False),
        )
        self.records[pn] = record
        if counted:
            if self.core.pacing_rate <= 0:
                raise ValueError("No positive BBR pacing rate")
            self.next_send = at + F(size, self.core.pacing_rate)
        event = dict(
            event="sent",
            record=deepcopy(record),
            pacing_rate_used=self.core.pacing_rate,
            next_eligible_seconds_exact=(
                None if self.external_pacer else str(self.next_send)
            ),
            internal_deadline_diagnostic_seconds_exact=str(self.next_send),
        )
        self.events.append(event)
        return event

    def _on_loss(self, records, now, flight_after=None):
        seconds(now)
        new = []
        for row in records:
            pn = row if type(row) is int else row["pn"]
            r = self.records[pn]
            if r["counted"] and not r["acked"] and not r["lost"]:
                r["lost"] = True
                new.append(pn)
        if new:
            if self.recovery_cutoff is None:
                self.core.on_ssthresh()
                self.recovery_cutoff = max(self.records)
            self.lost = (self.lost + len(new)) & 0xFFFFFFFF
            self.pending_losses += len(new)
        if flight_after is not None:
            self._flight(flight_after)
        event = dict(
            event="loss",
            at=str(seconds(now)),
            newly_lost=new,
            recovery_cutoff=self.recovery_cutoff,
            pending_losses=self.pending_losses,
            cwnd_bytes=self.cwnd_bytes,
        )
        self.events.append(event)
        return event

    def _on_ack(
        self,
        newly_seen,
        now,
        *,
        newly_lost=(),
        flight_after=None,
        raw_rtt_seconds=None,
        smoothed_rtt_seconds=None,
        prior_inflight_packets=None,
        pacer_next_eligible=None,
    ):
        at = seconds(now)
        seen = []
        # Mark first ACK identities before checking the caller's post-ACK flight.
        for row in newly_seen:
            pn = row if type(row) is int else row["pn"]
            r = self.records[pn]
            if not r["acked"]:
                r["acked"] = True
                if r["counted"]:
                    seen.append(r)
        self._on_loss(newly_lost, at)
        flight = self._flight(flight_after)
        if not seen:
            event = dict(
                event="ack_no_new_counted_pn",
                at=str(at),
                pending_losses=self.pending_losses,
                delivered=self.delivered,
                cwnd_bytes=self.cwnd_bytes,
            )
            self.events.append(event)
            return event
        self.delivered = (self.delivered + len(seen)) & 0xFFFFFFFF
        self.delivered_udp_bytes += sum(r["sent_bytes"] for r in seen)
        selected = max(seen, key=lambda r: (r["sent_us"], r["pn"]))
        send_interval = stamp_us_delta(selected["sent_us"], selected["first_tx_us"])
        sample = rate_sample(
            total_delivered=self.delivered,
            prior_delivered=selected["prior_delivered"],
            prior_mstamp_us=selected["delivered_mstamp_us"],
            now_us=microseconds(at),
            send_interval_us=send_interval,
            min_rtt_us=(
                self.core.min_rtt_us if self.core.min_rtt_us != 0xFFFFFFFF else 0
            ),
            is_app_limited=selected["app_limited"],
        )
        self.first_tx_us = selected["sent_us"]
        self.delivered_mstamp_us = microseconds(at)
        if self.recovery_cutoff is not None and any(
            r["pn"] > self.recovery_cutoff for r in seen
        ):
            self.recovery_cutoff = None
        ca = 3 if self.recovery_cutoff is not None else 0
        raw = -1 if raw_rtt_seconds is None else int(seconds(raw_rtt_seconds) * 1000000)
        srtt = (
            0
            if smoothed_rtt_seconds is None
            else int(seconds(smoothed_rtt_seconds) * 1000000) * 8
        )
        callback = Ack(
            now_us=microseconds(at),
            total_delivered=self.delivered,
            prior_delivered=selected["prior_delivered"],
            delivered=sample["delivered"],
            interval_us=sample["interval_us"],
            acked_sacked=len(seen),
            losses=self.pending_losses,
            rtt_us=raw,
            inflight=flight,
            prior_inflight=(
                (flight + sum(not r["lost"] for r in seen))
                if prior_inflight_packets is None
                else prior_inflight_packets
            ),
            ca_state=ca,
            app_limited=selected["app_limited"],
            srtt_us_x8=srtt,
            edt_ns=microseconds(
                max(
                    at,
                    (
                        self.next_send
                        if pacer_next_eligible is None
                        else seconds(pacer_next_eligible)
                    ),
                )
            )
            * 1000,
            total_lost=self.lost,
        )
        state_event = self.core.on_ack(callback)
        self.pending_losses = 0
        actual_delta = self.delivered_udp_bytes - selected["prior_delivered_udp_bytes"]
        event = dict(
            event="ack",
            at=str(at),
            newly_counted_pns=[r["pn"] for r in seen],
            selected_pn=selected["pn"],
            selected_send_snapshot=deepcopy(selected),
            sample=sample,
            actual_sample_udp_bytes=actual_delta,
            nominal_sample_quic_bytes=sample["delivered"] * self.mds,
            flow_limited_at_selected_send=selected["flow_limited"],
            callback=state_event,
            cwnd_bytes=self.cwnd_bytes,
            pacing_rate_quic_bytes_per_second=self.core.pacing_rate,
            preserved_next_eligible_seconds_exact=(
                None if self.external_pacer else str(self.next_send)
            ),
            internal_deadline_diagnostic_seconds_exact=str(self.next_send),
        )
        self.events.append(event)
        return event

    def _on_pto(self, now):
        event = dict(
            event="pto",
            at=str(seconds(now)),
            cwnd_bytes=self.cwnd_bytes,
            loss_count=self.lost,
            action="probe opportunity only; no synthetic TCP CA_Loss",
        )
        self.events.append(event)
        return event

    def on_sent(self, record, context):
        flags = {
            key: context.get(key, self.limited_state[key])
            for key in ("app_limited", "flow_limited")
        }
        if flags["app_limited"] and not flags["flow_limited"]:
            self.app_limited_marker = (
                self.delivered + len(self.active())
            ) & 0xFFFFFFFF or 1
        flags["app_limited"] = bool(self.app_limited_marker)
        if record["in_flight"] and self.limited_state["app_limited"]:
            self.core.on_tx_start(
                microseconds(context["now"]), True, self.app_limited_marker or 1
            )
        self.limited_state = {
            "app_limited": False,
            "flow_limited": flags["flow_limited"],
        }
        return self._on_sent(
            record, context["now"], context.get("flight_before"), flags
        )

    def on_ack(self, records, context):
        raw = None
        sample = context.get("rtt_sample")
        if sample is not None:
            if type(sample) is dict:
                raw = sample.get(
                    "raw", sample.get("latest_rtt", sample.get("raw_seconds"))
                )
            else:
                raw = sample
        prior = None
        if self.require_padding and context.get("flight_before") is not None:
            value = F(context["flight_before"]) / self.mds
            if value.denominator != 1:
                raise ValueError("Padded flight must contain whole packets")
            prior = int(value)
        if self.external_pacer and "pacer_next_eligible" not in context:
            raise ValueError(
                "External pacer must provide pre-ACK next eligibility for BBR EDT"
            )
        result = self._on_ack(
            records,
            context["now"],
            flight_after=context.get("flight_after"),
            raw_rtt_seconds=raw,
            smoothed_rtt_seconds=context.get("smoothed_rtt"),
            prior_inflight_packets=prior,
            pacer_next_eligible=context.get("pacer_next_eligible"),
        )
        if (
            self.app_limited_marker
            and ((self.delivered - self.app_limited_marker) & 0xFFFFFFFF) < (1 << 31)
            and self.delivered != self.app_limited_marker
        ):
            self.app_limited_marker = 0
        return result

    def on_loss(self, records, context):
        return self._on_loss(records, context["now"], context.get("flight_after"))

    def on_persistent(self, context):
        """QUIC RFC9002 adapter override; never a synthetic TCP CA_Loss."""
        if not context.get("evidence_key"):
            raise ValueError(
                "Persistent congestion override needs sender evidence identity"
            )
        evidence = context["evidence_key"]
        if not hasattr(self, "persistent_seen"):
            self.persistent_seen = set()
        identity = json.dumps(evidence, sort_keys=True)
        fresh = identity not in self.persistent_seen
        if fresh:
            self.persistent_seen.add(identity)
            self.core.cwnd = 2
        event = dict(
            event="quic_persistent_override",
            at=str(seconds(context["now"])),
            evidence_key=evidence,
            new_evidence=fresh,
            cwnd_bytes=self.cwnd_bytes,
            action="QUIC minimum 2*MDS; BBR mode/recovery unchanged",
        )
        self.events.append(event)
        return event

    def on_pto(self, context):
        return self._on_pto(context["now"])

    def on_limited(self, context):
        flags = {
            key: context.get(key, False) for key in ("app_limited", "flow_limited")
        }
        for key, value in flags.items():
            boolean(value, key)
        self.limited_state = flags
        if flags["app_limited"] and not flags["flow_limited"]:
            self.app_limited_marker = (
                self.delivered + len(self.active())
            ) & 0xFFFFFFFF or 1
        return dict(
            event="limited",
            at=str(seconds(context["now"])),
            **flags,
            app_limited_marker=self.app_limited_marker,
        )

    def snapshot(self):
        return self.status()

    def status(self):
        return dict(
            cwnd_bytes=self.cwnd_bytes,
            pacing_rate_quic_bytes_per_second=self.core.pacing_rate,
            next_eligible_seconds_exact=(
                None if self.external_pacer else str(self.next_send)
            ),
            internal_deadline_diagnostic_seconds_exact=str(self.next_send),
            external_pacer=self.external_pacer,
            delivered_packets=self.delivered,
            delivered_udp_bytes=self.delivered_udp_bytes,
            pending_losses=self.pending_losses,
            active_packet_count=len(self.active()),
            port="QUIC padded-PN BBR mapping; not Linux TCP",
        )
