"""CUBIC + initial HyStart++ under explicit QUIC transmission-frontier mapping."""

import copy
from fractions import Fraction as F

from . import cubic as CUBIC
from . import hystart as HYSTART


class CubicAdapter:
    def __init__(self, mds, initial_cwnd, initial_rtt, config=None):
        self.mds = mds
        self.config = config or {}
        CUBIC.sources()
        HYSTART.verify_sources()
        self.core = CUBIC.Controller(
            dict(
                initial=dict(cwnd=str(F(initial_cwnd) / mds), ssthresh=str(2**62)),
                fast_convergence=self.config.get("fast_convergence", False),
            )
        )
        self.initial_cwnd = F(initial_cwnd)
        self.initial_active = True
        self.hy = None
        self.frontier = 0
        self.confirmed = set()
        self.prefix_index = 0
        self.prefix = 0
        self.transmissions = []
        self.by_pn = {}
        self.rtt = F(initial_rtt)
        self.limited = False
        self.gain = F(str(self.config.get("pacing_gain", "5/4")))
        self.quantum = F(str(self.config.get("controller_quantum", "0.000000000001")))
        if self.quantum <= 0 or self.gain < 1:
            raise ValueError("invalid CUBIC numeric/pacing profile")
        self.events = []
        self.numeric_errors = []

    @property
    def cwnd_bytes(self):
        return self.core.cwnd * self.mds

    @property
    def pacing_rate_quic_bytes_per_second(self):
        return self.gain * self.cwnd_bytes / self.rtt

    def snapshot(self):
        return dict(
            controller="cubic_hystart",
            cwnd_bytes=str(self.cwnd_bytes),
            phase=(
                self.hy.phase
                if self.initial_active and self.hy
                else (
                    "initial_waiting_for_ack"
                    if self.initial_active
                    else self.core.phase
                )
            ),
            effective_epoch=str(self.core.elapsed),
            w_est_segments=str(self.core.estimate),
            w_max_segments=str(self.core.maximum),
            k_bounds=[str(k) for k in self.core.k],
            hystart_round=self.hy.round if self.hy else None,
            hystart_css_rounds=self.hy.css_completed if self.hy else 0,
            pacing_rate_quic_bytes_per_second=str(
                self.pacing_rate_quic_bytes_per_second
            ),
            limited=self.limited,
        )

    def finish_event(self, kind, context, detail=None):
        for field in ("cwnd", "estimate"):
            old = getattr(self.core, field)
            q = self.quantum / self.mds
            value = round(old / q) * q
            if field == "cwnd":
                value = max(value, F(2))
            if old != value:
                self.numeric_errors.append(
                    dict(
                        at=str(context["now"]),
                        field=field,
                        original=str(old),
                        rounded=str(value),
                        local_error=str(value - old),
                    )
                )
            setattr(self.core, field, value)
        self.events.append(
            dict(
                at=str(context["now"]),
                kind=kind,
                detail=CUBIC.serialize(detail or {}),
                state=self.snapshot(),
            )
        )

    def on_sent(self, record, context):
        if record["in_flight"]:
            start = self.frontier
            self.frontier += record["sent_bytes"]
            row = dict(
                pn=record["pn"],
                start=start,
                end=self.frontier,
                bytes=record["sent_bytes"],
            )
            self.by_pn[record["pn"]] = row
            self.transmissions.append(row)
            if self.hy and self.initial_active:
                self.hy.step(
                    dict(type="sent", at=str(context["now"]), snd_nxt=self.frontier)
                )

    def on_limited(self, context):
        limited = context.get("app_limited", False) or context.get(
            "flow_limited", False
        )
        if limited == self.limited:
            return
        self.limited = limited
        if limited:
            self.core.step(
                dict(
                    type="limited_start",
                    at=str(context["now"]),
                    reason=(
                        "application"
                        if context.get("app_limited")
                        else "receiver_window"
                    ),
                )
            )
        else:
            self.core.step(dict(type="limited_end", at=str(context["now"])))
        self.finish_event("limited", context)

    def on_loss(self, records, context):
        if not records:
            return
        now = context["now"]
        if context.get("new_recovery_epoch") is False:
            self.finish_event(
                "loss-within-recovery", context, dict(pns=[r["pn"] for r in records])
            )
            return
        if self.initial_active:
            if self.hy:
                self.hy.step(dict(type="congestion", at=str(now), signal="loss"))
            self.initial_active = False
        if self.core.phase == "recovery":
            self.core.step(dict(type="recovery_exit", at=str(now)))
        self.core.step(
            dict(
                type="congestion",
                at=str(now),
                event_id="loss-" + str(now),
                flight_size=str(F(context["flight_before"]) / self.mds),
            )
        )
        self.finish_event(
            "loss",
            context,
            dict(
                pns=[r["pn"] for r in records], flight_before=context["flight_before"]
            ),
        )

    def on_ack(self, records, context):
        now = context["now"]
        self.rtt = F(context["smoothed_rtt"])
        active = [r for r in records if r["in_flight"] and not r["was_lost"]]
        for r in records:
            if r["pn"] in self.by_pn:
                self.confirmed.add(r["pn"])
        while (
            self.prefix_index < len(self.transmissions)
            and self.transmissions[self.prefix_index]["pn"] in self.confirmed
        ):
            self.prefix = self.transmissions[self.prefix_index]["end"]
            self.prefix_index += 1
        if self.initial_active:
            if not active:
                return
            if self.hy is None:
                self.hy = HYSTART.Startup(
                    dict(
                        smss=self.mds,
                        initial_cwnd=str(self.cwnd_bytes),
                        initial_snd_nxt=self.frontier,
                        paced=True,
                    )
                )
            sample = context.get("rtt_sample")
            event = dict(
                type="ack",
                at=str(now),
                ack_seq=self.prefix,
                newly_acked_bytes=sum(r["sent_bytes"] for r in active),
            )
            if sample:
                event.update(
                    rtt=sample["adjusted"],
                    rtt_sample_id=str(sample["pn"]) + "@" + str(now),
                )
            before = self.hy.cwnd
            detail = self.hy.step(event)
            if self.limited:
                self.hy.cwnd = before
                if (
                    self.hy.handoff
                    and self.hy.handoff.get("policy") == "congestion_avoidance"
                ):
                    self.hy.ssthresh = before
                    self.hy.handoff.update(cwnd=before, ssthresh=before)
            self.core.cwnd = self.hy.cwnd / self.mds
            if self.hy.phase == "congestion_avoidance_handoff":
                self.initial_active = False
                self.core.prior = self.core.cwnd
                self.core.threshold = self.core.cwnd
                self.core.phase = "avoidance"
                self.core.force_zero = True
                self.core.now = now
                self.core.new_epoch()
            self.finish_event(
                "hystart_ack",
                context,
                dict(
                    growth_suppressed=self.limited,
                    transition=detail["details"].get("transition"),
                ),
            )
            return
        eligible = [
            r
            for r in active
            if context.get("recovery_start") is None
            or r["time"] > context["recovery_start"]
        ]
        if not eligible:
            return
        if self.core.phase == "recovery":
            self.core.step(dict(type="recovery_exit", at=str(now)))
        detail = self.core.step(
            dict(
                type="ack",
                at=str(now),
                segments_acked=str(F(sum(r["sent_bytes"] for r in eligible), self.mds)),
                smoothed_rtt=str(self.rtt),
            )
        )
        self.finish_event(
            "cubic_ack", context, detail["detail"] if "detail" in detail else detail
        )

    def on_pto(self, context):
        self.events.append(
            dict(
                at=str(context["now"]),
                kind="pto-no-window-reduction",
                state=self.snapshot(),
            )
        )

    def on_persistent(self, context):
        self.initial_active = False
        self.core.cwnd = F(2)
        self.core.force_zero = True
        self.core.phase = "slow_start"
        self.core.elapsed = F(0)
        self.core.now = context["now"]
        self.finish_event("persistent-congestion-minimum", context)
