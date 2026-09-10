"""Bounded reference-function cases; no network/controller closed loop."""

from pathlib import Path
import json
from bbr_reference import (
    sources,
    rate_sample,
    StartupDrain,
    before,
    pacing_bytes_per_second,
    bdp_packets,
    quantization_budget,
    recovery_cwnd,
    probe_rtt_exit_ready,
)


def run():
    sample = rate_sample(
        total_delivered=110,
        prior_delivered=100,
        prior_mstamp_us=1000,
        now_us=21000,
        send_interval_us=100000,
        min_rtt_us=100000,
    )
    assert sample["bw_scaled"] == 1677 and sample["interval_us"] == 100000
    assert pacing_bytes_per_second(1677, 1500, 739) == 428493
    assert bdp_packets(1677, 100000, 256) == 10
    assert quantization_budget(10, 1, "DRAIN") == 14
    state = StartupDrain(full_bw=1000, next_rtt_delivered=100)
    rounds = []
    for n in range(3):
        event = dict(sample, prior_delivered=100 + 10 * n)
        row = state.update(
            sample=event,
            total_delivered=110 + 10 * n,
            filtered_max_bw=1200,
            packets_in_net_at_edt=20,
            drain_target=14,
        )
        assert row["state"]["full_bw_cnt"] == n + 1
        rounds.append(row)
    assert state.mode == "DRAIN"
    drain = state.update(
        sample=dict(sample, prior_delivered=130),
        total_delivered=140,
        filtered_max_bw=1200,
        packets_in_net_at_edt=14,
        drain_target=14,
    )
    assert state.mode == "PROBE_BW"
    raw = StartupDrain(full_bw=10, next_rtt_delivered=100).update(
        sample=sample,
        total_delivered=110,
        filtered_max_bw=12,
        packets_in_net_at_edt=20,
        drain_target=14,
    )
    assert raw["state"]["full_bw_cnt"] == 0 and raw["state"]["full_bw"] == 12
    app = StartupDrain(full_bw=1000, next_rtt_delivered=100).update(
        sample=dict(sample, is_app_limited=True),
        total_delivered=110,
        filtered_max_bw=1200,
        packets_in_net_at_edt=20,
        drain_target=14,
    )
    assert app["round_start"] and app["state"]["full_bw_cnt"] == 0
    nonround = StartupDrain(full_bw=1000, next_rtt_delivered=101).update(
        sample=sample,
        total_delivered=110,
        filtered_max_bw=1200,
        packets_in_net_at_edt=20,
        drain_target=14,
    )
    assert not nonround["round_start"]
    invalid = rate_sample(
        total_delivered=110,
        prior_delivered=100,
        prior_mstamp_us=1000,
        now_us=21000,
        send_interval_us=100000,
        min_rtt_us=100001,
    )
    assert not invalid["valid"]
    missing = rate_sample(
        total_delivered=110,
        prior_delivered=100,
        prior_mstamp_us=0,
        now_us=21000,
        send_interval_us=100000,
        min_rtt_us=100000,
    )
    assert not missing["valid"]
    assert not before(1, 4294967294) and before(99, 100) and not before(100, 100)
    recover = recovery_cwnd(
        cwnd=100,
        losses=2,
        acked=3,
        inflight=70,
        previous_ca=0,
        current_ca=3,
        prior_cwnd=100,
    )
    assert (
        recover["cwnd_before_target_and_caps"] == 73 and recover["packet_conservation"]
    )
    restored = recovery_cwnd(
        cwnd=73,
        losses=0,
        acked=2,
        inflight=60,
        previous_ca=3,
        current_ca=0,
        prior_cwnd=100,
        packet_conservation=True,
    )
    assert (
        restored["cwnd_before_target_and_caps"] == 100
        and not restored["packet_conservation"]
    )
    assert not probe_rtt_exit_ready(now_jiffies=100, done_stamp=100, round_done=True)
    assert probe_rtt_exit_ready(now_jiffies=101, done_stamp=100, round_done=True)
    assert not probe_rtt_exit_ready(now_jiffies=101, done_stamp=100, round_done=False)
    return dict(
        status="passed",
        scope="Selected source functions; full BBR and transport not implemented",
        sources=sources(),
        sample=sample,
        pacing_bytes_per_second=428493,
        bdp_packets=10,
        quantized_drain_target_packets=14,
        rounds=rounds,
        drain=drain,
        integer_threshold_correction=raw,
        app_limited=app,
        not_new_round=nonround,
        invalid_interval=invalid,
        missing_timestamp=missing,
        recovery=recover,
        restored=restored,
    )


if __name__ == "__main__":
    result = run()
    Path(__file__).with_name("bbr-results.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(json.dumps({"status": result["status"], "scope": result["scope"]}))
