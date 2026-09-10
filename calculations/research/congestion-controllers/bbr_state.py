"""Linux v6.6 BBR callback state port under an explicit TCP-core input contract.

No wire simulation, ACK/SACK selection, loss detector, or QUIC adaptation lives
here. Upstream TCP counters and skb rate samples are required, never inferred
from receiver knowledge. The upstream callbacks remain explicit rather than synthesized.
"""

from dataclasses import dataclass, asdict
from copy import deepcopy
from bbr_minmax import RunningMax
from bbr_reference import (
    BW_UNIT,
    HIGH_GAIN,
    DRAIN_GAIN,
    PROBE_GAINS,
    before,
    integer,
    u32,
    boolean,
    bdp_packets,
    pacing_bytes_per_second,
    quantization_budget,
    recovery_cwnd,
    stamp_us_delta,
)


@dataclass
class Ack:
    now_us: int
    total_delivered: int
    prior_delivered: int
    delivered: int
    interval_us: int
    acked_sacked: int
    losses: int
    rtt_us: int
    inflight: int
    prior_inflight: int
    ca_state: int = 0
    app_limited: bool = False
    ack_delayed: bool = False
    srtt_us_x8: int = 0
    edt_ns: int = 0
    total_lost: int = 0

    def validate(self):
        for key in (
            "now_us",
            "total_delivered",
            "prior_delivered",
            "acked_sacked",
            "losses",
            "inflight",
            "prior_inflight",
            "srtt_us_x8",
            "edt_ns",
            "total_lost",
        ):
            integer(getattr(self, key), key)
        for key in ("total_delivered", "prior_delivered", "total_lost"):
            u32(getattr(self, key), key)
        integer(self.delivered, "delivered", -1, (1 << 31) - 1)
        integer(self.interval_us, "interval_us", -1, (1 << 63) - 1)
        integer(self.rtt_us, "rtt_us", -1, (1 << 63) - 1)
        u32(self.srtt_us_x8, "srtt_us_x8")
        integer(self.edt_ns, "edt_ns", maximum=(1 << 64) - 1)
        integer(self.now_us, "now_us", maximum=((1 << 64) - 1) // 1000)
        if self.delivered >= 0 and self.interval_us > 0:
            if self.delivered != (
                (self.total_delivered - self.prior_delivered) & 0xFFFFFFFF
            ):
                raise ValueError(
                    "Valid sample delivered must match total minus saved prior counter"
                )
        integer(self.ca_state, "ca_state", maximum=4)
        boolean(self.app_limited, "app_limited")
        boolean(self.ack_delayed, "ack_delayed")
        if (
            max(self.inflight, self.prior_inflight, self.acked_sacked, self.losses)
            > 1000000
        ):
            raise ValueError("Reference packet-budget domain exceeds 1 million")


class BBR:
    def __init__(
        self,
        *,
        cwnd=10,
        min_rtt_us=100000,
        srtt_us_x8=800000,
        hz=1000,
        mss_bytes=1500,
        pacing_shift=10,
        max_pacing_rate=10**12,
        cwnd_clamp=1000000,
        random_draws=(0,),
        initial_delivered=0,
        now_us=0,
        max_tcp_header_bytes=256,
        gso_legacy_max_size=65536,
    ):
        for name, value in locals().copy().items():
            if name in ("self", "random_draws"):
                continue
            integer(value, name)
        if hz not in (100, 250, 300, 1000):
            raise ValueError("Supported explicit Linux HZ: 100/250/300/1000")
        if not mss_bytes or not cwnd or cwnd > cwnd_clamp or cwnd_clamp > 1000000:
            raise ValueError("Initial cwnd/MSS domain")
        if not isinstance(random_draws, (list, tuple)) or not random_draws:
            raise ValueError("Provide explicit get_random_u32_below(7) draw sequence")
        for draw in random_draws:
            integer(draw, "random_draw", maximum=6)
        u32(srtt_us_x8, "srtt_us_x8")
        u32(mss_bytes, "mss_bytes")
        integer(now_us, "now_us", maximum=((1 << 64) - 1) // 1000)
        integer(max_pacing_rate, "max_pacing_rate", maximum=(1 << 64) - 1)
        integer(pacing_shift, "pacing_shift", maximum=63)
        u32(min_rtt_us, "min_rtt_us")
        u32(initial_delivered, "initial_delivered")
        self.max_tcp_header_bytes = max_tcp_header_bytes
        self.gso_legacy_max_size = gso_legacy_max_size
        if max_tcp_header_bytes + 1 >= gso_legacy_max_size:
            raise ValueError("Invalid declared ABI header/GSO budget")
        self.hz = hz
        self.mss = mss_bytes
        self.pacing_shift = pacing_shift
        self.max_pacing_rate = max_pacing_rate
        self.cwnd_clamp = cwnd_clamp
        self.draws = list(random_draws)
        self.draw_index = 0
        self.now_us = now_us
        self.delivered_mstamp = now_us
        self.cwnd = cwnd
        self.bw = RunningMax(0, 0)
        self.rtt_cnt = 0
        self.next_rtt_delivered = initial_delivered
        self.min_rtt_us = min_rtt_us
        self.min_rtt_stamp = self.jiffies(now_us)
        self.mode = "STARTUP"
        self.pacing_gain = 0
        self.cwnd_gain = 0
        self.full_bw = 0
        self.full_bw_cnt = 0
        self.full_bw_reached = False
        self.round_start = False
        self.packet_conservation = False
        self.prev_ca = 0
        self.prior_cwnd = 0
        self.cycle_idx = 0
        self.cycle_mstamp = 0
        self.probe_rtt_done_stamp = 0
        self.probe_rtt_round_done = False
        self.idle_restart = False
        self.ack_epoch_mstamp = now_us
        self.ack_epoch_acked = 0
        self.extra_acked = [0, 0]
        self.extra_acked_win_rtts = 0
        self.extra_acked_win_idx = 0
        self.has_seen_rtt = bool(srtt_us_x8)
        initial_rtt = max(srtt_us_x8 >> 3, 1) if srtt_us_x8 else 1000
        initial_bw = cwnd * BW_UNIT // initial_rtt
        u32(initial_bw, "initial bandwidth")
        self.pacing_rate = min(
            max_pacing_rate, pacing_bytes_per_second(initial_bw, self.mss, HIGH_GAIN)
        )
        self.lt_bw = 0
        self.lt_use_bw = False
        self.lt_is_sampling = False
        self.lt_last_stamp = now_us // 1000
        self.lt_last_delivered = initial_delivered
        self.lt_last_lost = 0
        self.lt_rtt_cnt = 0
        self.last_total_delivered = initial_delivered
        self.last_total_lost = 0
        self.snd_ssthresh = 0x7FFFFFFF
        self.app_limited_until = 0
        self.events = []

    def effective_bw(self):
        return self.lt_bw if self.lt_use_bw else self.bw.value

    def reset_lt_interval(self):
        self.lt_last_stamp = (self.delivered_mstamp // 1000) & 0xFFFFFFFF
        self.lt_last_delivered = self.last_total_delivered
        self.lt_last_lost = self.last_total_lost
        self.lt_rtt_cnt = 0

    def reset_lt(self):
        self.lt_bw = 0
        self.lt_use_bw = False
        self.lt_is_sampling = False
        self.reset_lt_interval()

    def update_lt(self, ack):
        if self.lt_use_bw:
            if self.mode == "PROBE_BW" and self.round_start:
                self.lt_rtt_cnt += 1
                if self.lt_rtt_cnt >= 48:
                    self.reset_lt()
                    self.reset_probe_bw()
            return
        if not self.lt_is_sampling:
            if not ack.losses:
                return
            self.reset_lt_interval()
            self.lt_is_sampling = True
        if ack.app_limited:
            self.reset_lt()
            return
        if self.round_start:
            self.lt_rtt_cnt += 1
        if self.lt_rtt_cnt < 4:
            return
        if self.lt_rtt_cnt > 16:
            self.reset_lt()
            return
        if not ack.losses:
            return
        lost = (ack.total_lost - self.lt_last_lost) & 0xFFFFFFFF
        delivered = (ack.total_delivered - self.lt_last_delivered) & 0xFFFFFFFF
        if not delivered or ((lost << 8) & 0xFFFFFFFF) < (
            (50 * delivered) & 0xFFFFFFFF
        ):
            return
        elapsed = ((self.delivered_mstamp // 1000) - self.lt_last_stamp) & 0xFFFFFFFF
        if elapsed == 0 or elapsed >= 1 << 31:
            return
        if elapsed >= 0xFFFFFFFF // 1000:
            self.reset_lt()
            return
        bw = (delivered * BW_UNIT // (elapsed * 1000)) & 0xFFFFFFFF
        if self.lt_bw:
            # Restrict signed-difference ambiguity rather than inventing abs semantics.
            diff = abs(bw - self.lt_bw)
            if diff >= 1 << 31:
                raise ValueError("Policer bandwidth difference outside signed domain")
            if ((diff * 256) & 0xFFFFFFFF) <= (
                (32 * self.lt_bw) & 0xFFFFFFFF
            ) or pacing_bytes_per_second(diff, self.mss, 256) <= 500:
                self.lt_bw = ((bw + self.lt_bw) & 0xFFFFFFFF) >> 1
                self.lt_use_bw = True
                self.pacing_gain = 256
                self.lt_rtt_cnt = 0
                return
        self.lt_bw = bw
        self.reset_lt_interval()

    def on_undo_cwnd(self):
        self.full_bw = 0
        self.full_bw_cnt = 0
        self.reset_lt()
        return self.cwnd

    def on_ca_loss(self):
        self.prev_ca = 4
        self.full_bw = 0
        self.round_start = True
        synthetic = Ack(
            self.now_us,
            self.last_total_delivered,
            0,
            0,
            0,
            0,
            1,
            -1,
            0,
            0,
            total_lost=self.last_total_lost,
        )
        self.update_lt(synthetic)

    def jiffies(self, now_us):
        return (now_us * self.hz // 1000000) & 0xFFFFFFFF

    def tso_goal(self):
        # ABI-dependent macros are explicit constructor inputs, not portable constants.
        byte_budget = min(
            self.pacing_rate >> self.pacing_shift,
            self.gso_legacy_max_size - 1 - self.max_tcp_header_bytes,
        )
        minimum = 1 if self.pacing_rate < 150000 else 2
        return min(max(byte_budget // self.mss, minimum), 127)

    def inflight_target(self, gain):
        return quantization_budget(
            bdp_packets(self.bw.value, self.min_rtt_us, gain),
            self.tso_goal(),
            self.mode,
            self.cycle_idx,
        )

    def net_at_edt(self, inflight, ack):
        duration = max(ack.edt_ns - ack.now_us * 1000, 0) // 1000
        interval_delivered = (self.effective_bw() * duration >> 24) & 0xFFFFFFFF
        projected = inflight + (self.tso_goal() if self.pacing_gain > 256 else 0)
        return max(projected - interval_delivered, 0)

    def save_cwnd(self):
        if self.prev_ca < 3 and self.mode != "PROBE_RTT":
            self.prior_cwnd = self.cwnd
        else:
            self.prior_cwnd = max(self.prior_cwnd, self.cwnd)

    def reset_probe_bw(self):
        if self.draw_index >= len(self.draws):
            raise ValueError("Explicit random draw sequence exhausted")
        draw = self.draws[self.draw_index]
        self.draw_index += 1
        self.mode = "PROBE_BW"
        self.cycle_idx = (8 - draw) & 7
        self.cycle_mstamp = self.delivered_mstamp

    def reset_mode(self):
        if self.full_bw_reached:
            self.reset_probe_bw()
        else:
            self.mode = "STARTUP"

    def update_bandwidth(self, ack):
        self.round_start = False
        if ack.delivered < 0 or ack.interval_us <= 0:
            return
        if not before(ack.prior_delivered, self.next_rtt_delivered):
            self.next_rtt_delivered = ack.total_delivered
            self.rtt_cnt = (self.rtt_cnt + 1) & 0xFFFFFFFF
            self.round_start = True
            self.packet_conservation = False
        self.update_lt(ack)
        sample = ack.delivered * BW_UNIT // ack.interval_us
        u32(sample, "sample BW")
        if not ack.app_limited or sample >= self.bw.value:
            self.bw.update(10, self.rtt_cnt, sample)

    def update_ack_aggregation(self, ack):
        if ack.acked_sacked <= 0 or ack.delivered < 0 or ack.interval_us <= 0:
            return
        if self.round_start:
            self.extra_acked_win_rtts = min(31, self.extra_acked_win_rtts + 1)
            if self.extra_acked_win_rtts >= 5:
                self.extra_acked_win_rtts = 0
                self.extra_acked_win_idx = 1 - self.extra_acked_win_idx
                self.extra_acked[self.extra_acked_win_idx] = 0
        epoch_us = stamp_us_delta(self.delivered_mstamp, self.ack_epoch_mstamp)
        expected = (self.effective_bw() * epoch_us // BW_UNIT) & 0xFFFFFFFF
        if (
            self.ack_epoch_acked <= expected
            or self.ack_epoch_acked + ack.acked_sacked >= 1 << 20
        ):
            self.ack_epoch_acked = 0
            self.ack_epoch_mstamp = self.delivered_mstamp
            expected = 0
        self.ack_epoch_acked = min(0xFFFFF, self.ack_epoch_acked + ack.acked_sacked)
        extra = min(self.ack_epoch_acked - expected, self.cwnd)
        if extra > self.extra_acked[self.extra_acked_win_idx]:
            self.extra_acked[self.extra_acked_win_idx] = extra & 0xFFFF

    def update_cycle(self, ack):
        if self.mode != "PROBE_BW":
            return
        full = (
            stamp_us_delta(self.delivered_mstamp, self.cycle_mstamp) > self.min_rtt_us
        )
        if self.pacing_gain == 256:
            advance = full
        elif self.pacing_gain > 256:
            advance = full and (
                ack.losses > 0
                or self.net_at_edt(ack.prior_inflight, ack)
                >= self.inflight_target(self.pacing_gain)
            )
        else:
            advance = full or self.net_at_edt(
                ack.prior_inflight, ack
            ) <= self.inflight_target(256)
        if advance:
            self.cycle_idx = (self.cycle_idx + 1) & 7
            self.cycle_mstamp = self.delivered_mstamp

    def update_full_bw(self, ack):
        if self.full_bw_reached or not self.round_start or ack.app_limited:
            return
        threshold = ((self.full_bw * 320) >> 8) & 0xFFFFFFFF
        if self.bw.value >= threshold:
            self.full_bw = self.bw.value
            self.full_bw_cnt = 0
        else:
            self.full_bw_cnt += 1
            self.full_bw_reached = self.full_bw_cnt >= 3

    def update_drain(self, ack):
        if self.mode == "STARTUP" and self.full_bw_reached:
            self.mode = "DRAIN"
            self.snd_ssthresh = self.inflight_target(256)
        if self.mode == "DRAIN" and self.net_at_edt(
            ack.inflight, ack
        ) <= self.inflight_target(256):
            self.reset_probe_bw()

    def check_probe_done(self):
        if self.probe_rtt_done_stamp and before(
            self.probe_rtt_done_stamp, self.jiffies(self.now_us)
        ):
            self.min_rtt_stamp = self.jiffies(self.now_us)
            self.cwnd = max(self.cwnd, self.prior_cwnd)
            self.reset_mode()

    def update_min_rtt(self, ack):
        tick = self.jiffies(ack.now_us)
        expired = before((self.min_rtt_stamp + 10 * self.hz) & 0xFFFFFFFF, tick)
        if ack.rtt_us >= 0 and (
            ack.rtt_us < self.min_rtt_us or (expired and not ack.ack_delayed)
        ):
            self.min_rtt_us = ack.rtt_us & 0xFFFFFFFF
            self.min_rtt_stamp = tick
        if expired and not self.idle_restart and self.mode != "PROBE_RTT":
            self.mode = "PROBE_RTT"
            self.save_cwnd()
            self.probe_rtt_done_stamp = 0
        if self.mode == "PROBE_RTT":
            self.app_limited_until = (
                (ack.total_delivered + ack.inflight) & 0xFFFFFFFF
            ) or 1
            if not self.probe_rtt_done_stamp and ack.inflight <= 4:
                # msecs_to_jiffies(200), with supported HZ values and rounding up.
                self.probe_rtt_done_stamp = (
                    tick + (200 * self.hz + 999) // 1000
                ) & 0xFFFFFFFF
                self.probe_rtt_round_done = False
                self.next_rtt_delivered = ack.total_delivered
            elif self.probe_rtt_done_stamp:
                if self.round_start:
                    self.probe_rtt_round_done = True
                if self.probe_rtt_round_done:
                    self.check_probe_done()
        if ack.delivered > 0:
            self.idle_restart = False

    def update_gains(self):
        if self.mode == "STARTUP":
            self.pacing_gain = self.cwnd_gain = HIGH_GAIN
        elif self.mode == "DRAIN":
            self.pacing_gain = DRAIN_GAIN
            self.cwnd_gain = HIGH_GAIN
        elif self.mode == "PROBE_BW":
            self.pacing_gain = 256 if self.lt_use_bw else PROBE_GAINS[self.cycle_idx]
            self.cwnd_gain = 512
        else:
            self.pacing_gain = self.cwnd_gain = 256

    def set_pacing(self, ack):
        rate = min(
            self.max_pacing_rate,
            pacing_bytes_per_second(self.effective_bw(), self.mss, self.pacing_gain),
        )
        if not self.has_seen_rtt and ack.srtt_us_x8:
            initial_bw = self.cwnd * BW_UNIT // max(ack.srtt_us_x8 >> 3, 1)
            self.pacing_rate = min(
                self.max_pacing_rate,
                pacing_bytes_per_second(initial_bw, self.mss, HIGH_GAIN),
            )
            self.has_seen_rtt = True
        if self.full_bw_reached or rate > self.pacing_rate:
            self.pacing_rate = rate

    def set_cwnd(self, ack):
        if ack.acked_sacked:
            recovered = recovery_cwnd(
                cwnd=self.cwnd,
                losses=ack.losses,
                acked=ack.acked_sacked,
                inflight=ack.inflight,
                previous_ca=self.prev_ca,
                current_ca=ack.ca_state,
                prior_cwnd=self.prior_cwnd,
                packet_conservation=self.packet_conservation,
            )
            self.cwnd = recovered["cwnd_before_target_and_caps"]
            self.packet_conservation = recovered["packet_conservation"]
            self.prev_ca = ack.ca_state
            if recovered["reset_next_rtt_delivered_to_current_total"]:
                self.next_rtt_delivered = ack.total_delivered
            if not self.packet_conservation:
                extra = (
                    min(max(self.extra_acked), self.effective_bw() * 100000 // BW_UNIT)
                    if self.full_bw_reached
                    else 0
                )
                target = quantization_budget(
                    bdp_packets(self.effective_bw(), self.min_rtt_us, self.cwnd_gain)
                    + extra,
                    self.tso_goal(),
                    self.mode,
                    self.cycle_idx,
                )
                if self.full_bw_reached:
                    self.cwnd = min(self.cwnd + ack.acked_sacked, target)
                elif self.cwnd < target or ack.total_delivered < 10:
                    self.cwnd += ack.acked_sacked
                self.cwnd = max(self.cwnd, 4)
        self.cwnd = min(self.cwnd, self.cwnd_clamp)
        if self.mode == "PROBE_RTT":
            self.cwnd = min(self.cwnd, 4)

    def on_ack(self, ack):
        ack.validate()
        if ack.now_us < self.now_us:
            raise ValueError("Nonmonotonic callback time")
        self.now_us = ack.now_us
        self.last_total_delivered = ack.total_delivered
        self.last_total_lost = ack.total_lost
        if self.app_limited_until and before(
            self.app_limited_until, ack.total_delivered
        ):
            self.app_limited_until = 0
        if ack.acked_sacked:
            self.delivered_mstamp = ack.now_us
        self.update_bandwidth(ack)
        self.update_ack_aggregation(ack)
        self.update_cycle(ack)
        self.update_full_bw(ack)
        self.update_drain(ack)
        self.update_min_rtt(ack)
        self.update_gains()
        self.set_pacing(ack)
        self.set_cwnd(ack)
        row = dict(input=asdict(ack), state=self.snapshot())
        self.events.append(row)
        return row

    def on_ssthresh(self):
        self.save_cwnd()
        return self.snd_ssthresh

    def on_tx_start(self, now_us, app_limited, app_limited_until=None):
        integer(now_us, "now_us")
        boolean(app_limited, "app_limited")
        marker = (
            (1 if app_limited else 0)
            if app_limited_until is None
            else app_limited_until
        )
        u32(marker, "app_limited_until")
        if bool(marker) != app_limited:
            raise ValueError("TX_START marker and app-limited flag disagree")
        self.app_limited_until = marker
        if now_us < self.now_us:
            raise ValueError("Nonmonotonic callback time")
        self.now_us = now_us
        if app_limited:
            self.idle_restart = True
            self.ack_epoch_mstamp = now_us
            self.ack_epoch_acked = 0
            if self.mode == "PROBE_BW":
                self.pacing_rate = min(
                    self.max_pacing_rate,
                    pacing_bytes_per_second(self.effective_bw(), self.mss, 256),
                )
            elif self.mode == "PROBE_RTT":
                self.check_probe_done()

    def snapshot(self):
        return {
            key: deepcopy(value)
            for key, value in vars(self).items()
            if key not in ("bw", "events")
        } | {
            "max_bw_scaled": self.bw.value,
            "bw_filter": [asdict(s) for s in self.bw.samples],
        }
