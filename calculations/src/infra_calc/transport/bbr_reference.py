"""Selected Linux v6.6 TCP BBR/rate functions; not a transport or complete BBR.

Upstream skb selection, max filter, EDT accounting and TCP recovery decisions are
explicit inputs. No QUIC feedback is interpreted as a Linux TCP callback.
"""

from .reference_sources import reference_sources

from dataclasses import dataclass, asdict
import json

BW_UNIT = 1 << 24
GAIN_UNIT = 256
HIGH_GAIN = 739
DRAIN_GAIN = 88
PROBE_GAINS = (320, 192, 256, 256, 256, 256, 256, 256)


def integer(value, name, minimum=0, maximum=None):
    if (
        type(value) is not int
        or value < minimum
        or (maximum is not None and value > maximum)
    ):
        raise ValueError(name)
    return value


def boolean(value, name):
    if type(value) is not bool:
        raise ValueError(name)
    return value


def u32(value, name):
    return integer(value, name, maximum=(1 << 32) - 1)


def before(left, right):
    """Linux serial arithmetic; callers must keep distances below 2^31."""
    u32(left, "left")
    u32(right, "right")
    return bool(((left - right) & 0xFFFFFFFF) & 0x80000000)


def stamp_us_delta(t1, t0):
    """tcp.h: max_t(s64, unsigned-u64 subtraction, 0), returned as u32."""
    integer(t1, "t1", maximum=(1 << 64) - 1)
    integer(t0, "t0", maximum=(1 << 64) - 1)
    difference = (t1 - t0) & ((1 << 64) - 1)
    if difference & (1 << 63):
        difference -= 1 << 64
    return max(difference, 0) & 0xFFFFFFFF


def sources():
    return reference_sources("bbr")


def rate_sample(
    *,
    total_delivered,
    prior_delivered,
    prior_mstamp_us,
    now_us,
    send_interval_us,
    min_rtt_us,
    is_app_limited=False,
    sack_reneging=False
):
    """tcp_rate_gen arithmetic after tcp_rate_skb_delivered selected an skb.

    prior_delivered and timestamps are saved at transmission; total_delivered
    is the TCP post-ACK/SACK counter. Not current ACK size / inter-ACK gap.
    """
    u32(total_delivered, "total_delivered")
    u32(prior_delivered, "prior_delivered")
    for name, value in [
        ("prior_mstamp_us", prior_mstamp_us),
        ("now_us", now_us),
        ("send_interval_us", send_interval_us),
        ("min_rtt_us", min_rtt_us),
    ]:
        integer(value, name)
    boolean(is_app_limited, "is_app_limited")
    boolean(sack_reneging, "sack_reneging")
    if now_us < prior_mstamp_us:
        raise ValueError("Nonmonotonic microsecond timestamps")
    if not prior_mstamp_us or sack_reneging:
        return dict(
            valid=False,
            reason="missing_prior_timestamp_or_sack_reneging",
            delivered=-1,
            interval_us=-1,
        )
    delivered = (total_delivered - prior_delivered) & 0xFFFFFFFF
    if delivered >= 1 << 31:
        raise ValueError("Sample spans ambiguous/signed delivered counter range")
    ack_interval = stamp_us_delta(now_us, prior_mstamp_us)
    interval = max(send_interval_us, ack_interval)
    valid = interval > 0 and interval >= min_rtt_us
    return dict(
        valid=valid,
        reason=None if valid else "nonpositive_or_below_min_rtt",
        delivered=delivered,
        interval_us=interval if valid else -1,
        snd_interval_us=send_interval_us,
        rcv_interval_us=ack_interval,
        prior_delivered=prior_delivered,
        is_app_limited=is_app_limited,
        bw_scaled=delivered * BW_UNIT // interval if valid else None,
    )


def pacing_bytes_per_second(bw_scaled, mss_bytes, gain):
    u32(bw_scaled, "bw_scaled")
    integer(mss_bytes, "mss_bytes", 1)
    integer(gain, "gain", 1)
    product = bw_scaled * mss_bytes * gain
    if product >= 1 << 64 or (product >> 8) * 990000 >= 1 << 64:
        raise ValueError("Outside u64 arithmetic domain")
    return ((product >> 8) * 990000) >> 24


def bdp_packets(bw_scaled, min_rtt_us, gain):
    u32(bw_scaled, "bw_scaled")
    u32(min_rtt_us, "min_rtt_us")
    integer(gain, "gain", 1)
    if min_rtt_us == 0xFFFFFFFF:
        return 10  # TCP_INIT_CWND safe default, not a new RTT estimate.
    product = bw_scaled * min_rtt_us * gain
    if product >= 1 << 64:
        raise ValueError("Outside u64 arithmetic domain")
    return ((product >> 8) + BW_UNIT - 1) // BW_UNIT


def quantization_budget(cwnd, tso_segs_goal, mode, cycle_idx=0):
    integer(cwnd, "cwnd")
    integer(tso_segs_goal, "tso_segs_goal", 1)
    if mode not in ("STARTUP", "DRAIN", "PROBE_BW", "PROBE_RTT"):
        raise ValueError("mode")
    integer(cycle_idx, "cycle_idx", maximum=7)
    result = (cwnd + 3 * tso_segs_goal + 1) & ~1
    return result + 2 if mode == "PROBE_BW" and cycle_idx == 0 else result


@dataclass
class StartupDrain:
    """bbr_update_bw round marker + full_bw/drain only.

    filtered_max_bw is the upstream Linux minmax result, not this sample.
    packets_in_net_at_edt and drain_target are upstream integer outputs.
    """

    next_rtt_delivered: int = 0
    rtt_cnt: int = 0
    full_bw: int = 0
    full_bw_cnt: int = 0
    full_bw_reached: bool = False
    mode: str = "STARTUP"

    def __post_init__(self):
        u32(self.next_rtt_delivered, "next_rtt_delivered")
        u32(self.rtt_cnt, "rtt_cnt")
        u32(self.full_bw, "full_bw")
        integer(self.full_bw_cnt, "full_bw_cnt", maximum=3)
        boolean(self.full_bw_reached, "full_bw_reached")
        if self.mode not in ("STARTUP", "DRAIN"):
            raise ValueError("Initial mode must be STARTUP or DRAIN")

    def update(
        self,
        *,
        sample,
        total_delivered,
        filtered_max_bw,
        packets_in_net_at_edt,
        drain_target
    ):
        u32(total_delivered, "total_delivered")
        u32(filtered_max_bw, "filtered_max_bw")
        integer(packets_in_net_at_edt, "packets_in_net_at_edt")
        integer(drain_target, "drain_target")
        if self.mode not in ("STARTUP", "DRAIN"):
            raise ValueError(
                "StartupDrain stops at PROBE_BW boundary; use full mode implementation afterward"
            )
        if not isinstance(sample, dict) or "valid" not in sample:
            raise ValueError("sample requires explicit validity")
        boolean(sample["valid"], "sample.valid")
        if sample["valid"]:
            if "is_app_limited" not in sample or "prior_delivered" not in sample:
                raise ValueError("valid sample requires app-limited and prior counter")
            boolean(sample["is_app_limited"], "sample.is_app_limited")
            u32(sample["prior_delivered"], "sample.prior_delivered")
        round_start = False
        if sample["valid"]:
            if not before(sample["prior_delivered"], self.next_rtt_delivered):
                self.next_rtt_delivered = total_delivered
                self.rtt_cnt = (self.rtt_cnt + 1) & 0xFFFFFFFF
                round_start = True
        threshold = ((self.full_bw * 320) >> 8) & 0xFFFFFFFF
        if (
            not self.full_bw_reached
            and round_start
            and not sample.get("is_app_limited", False)
        ):
            if filtered_max_bw >= threshold:
                self.full_bw = filtered_max_bw
                self.full_bw_cnt = 0
            else:
                self.full_bw_cnt += 1
                self.full_bw_reached = self.full_bw_cnt >= 3
        if self.mode == "STARTUP" and self.full_bw_reached:
            self.mode = "DRAIN"
        if self.mode == "DRAIN" and packets_in_net_at_edt <= drain_target:
            self.mode = "PROBE_BW"
        return dict(
            state=asdict(self),
            round_start=round_start,
            bw_threshold=threshold,
            pacing_gain=(
                HIGH_GAIN
                if self.mode == "STARTUP"
                else DRAIN_GAIN if self.mode == "DRAIN" else None
            ),
            needs_probe_bw_phase_initialization=self.mode == "PROBE_BW",
        )


def recovery_cwnd(
    *,
    cwnd,
    losses,
    acked,
    inflight,
    previous_ca,
    current_ca,
    prior_cwnd,
    packet_conservation=False
):
    """bbr_set_cwnd_to_recover_or_restore only, before cwnd target/cap logic.

    TCP core selects CA state. This function does not detect loss or mark PN.
    Linux CA_Open=0, Disorder=1, CWR=2, Recovery=3, Loss=4.
    """
    for key, value in locals().copy().items():
        if key == "packet_conservation":
            boolean(value, key)
        else:
            integer(value, key)
    if max(previous_ca, current_ca) > 4:
        raise ValueError("TCP CA enum")
    adjusted = max(cwnd - losses, 1) if losses else cwnd
    reset_round = False
    if current_ca == 3 and previous_ca != 3:
        packet_conservation = True
        reset_round = True
        adjusted = inflight + acked
    elif previous_ca >= 3 and current_ca < 3:
        adjusted = max(adjusted, prior_cwnd)
        packet_conservation = False
    if packet_conservation:
        adjusted = max(adjusted, inflight + acked)
    return dict(
        cwnd_before_target_and_caps=adjusted,
        packet_conservation=packet_conservation,
        reset_next_rtt_delivered_to_current_total=reset_round,
        previous_ca_after=current_ca,
    )


def probe_rtt_exit_ready(*, now_jiffies, done_stamp, round_done):
    """Exit gate only: Linux uses strictly after(), not >= deadline."""
    u32(now_jiffies, "now_jiffies")
    u32(done_stamp, "done_stamp")
    boolean(round_done, "round_done")
    return bool(done_stamp and round_done and before(done_stamp, now_jiffies))
