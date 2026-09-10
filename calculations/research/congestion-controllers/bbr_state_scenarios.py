"""Deterministic callback scenarios for the evolving Linux BBR state port."""

from pathlib import Path
from dataclasses import replace
import json
import hashlib
from bbr_reference import sources
from bbr_state import BBR, Ack


def callback(i, **changes):
    base = dict(
        now_us=i * 100000,
        total_delivered=i * 10,
        prior_delivered=(i - 1) * 10,
        delivered=10,
        interval_us=100000,
        acked_sacked=10,
        losses=0,
        rtt_us=100000,
        inflight=100,
        prior_inflight=100,
        srtt_us_x8=800000,
    )
    base.update(changes)
    return Ack(**base)


def run():
    sources()
    root = Path(__file__).resolve().parent
    for row in json.loads((root / "bbr-sources.lock.json").read_text())["sources"]:
        payload = (root / row["file"]).read_bytes()
        assert (
            len(payload) == row["bytes"]
            and hashlib.sha256(payload).hexdigest() == row["sha256"]
        )
    rows = {}
    b = BBR(random_draws=[0] * 20)
    for i in range(1, 5):
        b.on_ack(callback(i))
    assert b.mode == "DRAIN" and b.full_bw_reached
    b.on_ack(callback(5, inflight=0, prior_inflight=0))
    assert b.mode == "PROBE_BW" and b.cycle_idx == 0
    # Strict time gate: equality at minRTT keeps high-gain phase.
    b.on_ack(callback(6))
    assert b.cycle_idx == 0
    b.on_ack(callback(7))
    assert b.cycle_idx == 1
    b.on_ack(callback(8, inflight=0, prior_inflight=0))
    assert b.cycle_idx == 2
    for i in range(9, 21):
        b.on_ack(callback(i))
    assert {
        r["state"]["cycle_idx"] for r in b.events if r["state"]["mode"] == "PROBE_BW"
    } == set(range(8))
    rows["startup-drain-eight-phases"] = b.events.copy()
    # Expired minRTT enters probe; threshold equality alone does not exit.
    b.on_ack(callback(21, now_us=11000000, inflight=4, prior_inflight=4))
    assert b.mode == "PROBE_RTT" and b.cwnd <= 4
    b.on_ack(callback(22, now_us=11200000, inflight=4, prior_inflight=4))
    assert b.mode == "PROBE_RTT" and b.probe_rtt_round_done
    b.on_ack(callback(23, now_us=11201000, inflight=4, prior_inflight=4))
    assert b.mode == "PROBE_BW"
    rows["probe-rtt"] = b.events[-3:]
    recovered = BBR(cwnd=100, random_draws=[0] * 10)
    recovered.on_ssthresh()
    recovered.on_ack(
        callback(1, ca_state=3, losses=2, total_lost=2, inflight=70, acked_sacked=3)
    )
    assert recovered.packet_conservation and recovered.cwnd == 73
    recovered.on_ack(callback(2, ca_state=0, total_lost=2, inflight=60, acked_sacked=2))
    assert not recovered.packet_conservation and recovered.cwnd >= 100
    rows["recovery"] = recovered.events
    # Lower app-limited sample does not age/filter out a previously high max.
    app = BBR(random_draws=[0] * 10)
    app.on_ack(callback(1, delivered=100, total_delivered=100, acked_sacked=100))
    peak = app.bw.value
    for i in range(2, 15):
        app.on_ack(
            callback(
                i,
                app_limited=True,
                total_delivered=100 + (i - 1) * 10,
                prior_delivered=100 + (i - 2) * 10,
            )
        )
    assert app.bw.value == peak and app.full_bw_cnt == 0
    rows["app-limited-filter"] = app.events
    idle = BBR(random_draws=[0] * 10)
    idle.on_tx_start(11000000, True)
    idle.on_ack(callback(1, now_us=11100000))
    assert idle.mode == "STARTUP" and not idle.idle_restart
    rows["idle-probe-suppression"] = idle.events
    # Additional callback increases same-epoch excess ACK history.
    aggr = BBR(cwnd=100, random_draws=[0] * 10)
    aggr.on_ack(callback(1))
    aggr.on_ack(callback(2, now_us=100001, prior_delivered=0, delivered=20))
    assert max(aggr.extra_acked) == 20
    rows["ack-aggregation"] = aggr.events
    # HZ250 gives exactly50 ticks for200ms; strict > deadline still applies.
    hz = BBR(hz=250, random_draws=[1] * 10)
    hz.on_ack(callback(1, now_us=11000000, inflight=4, prior_inflight=4))
    assert hz.probe_rtt_done_stamp == 2800
    hz.on_ack(callback(2, now_us=11200000, inflight=4, prior_inflight=4))
    assert hz.mode == "PROBE_RTT"
    hz.on_ack(callback(3, now_us=11204000, inflight=4, prior_inflight=4))
    assert hz.mode == "STARTUP"
    rows["hz250-probe-rtt"] = hz.events
    policer = BBR(random_draws=[0] * 20)
    for i in range(1, 9):
        lost = 1 if i < 4 else 10 if i < 8 else 20
        losses = {1: 1, 4: 9, 8: 10}.get(i, 0)
        policer.on_ack(
            callback(i, losses=losses, total_lost=lost, inflight=0, prior_inflight=0)
        )
    assert policer.lt_use_bw and policer.lt_bw == 1677
    assert policer.pacing_gain == 256
    for i in range(9, 57):
        policer.on_ack(callback(i, total_lost=20, inflight=0, prior_inflight=0))
    assert not policer.lt_use_bw
    rows["policer-two-intervals-and48-round-expiry"] = policer.events
    reset = BBR(random_draws=[0] * 10)
    reset.on_ack(callback(1, losses=1, total_lost=1))
    assert reset.lt_is_sampling
    reset.on_ack(callback(2, total_lost=1, app_limited=True))
    assert not reset.lt_is_sampling and reset.lt_bw == 0
    rows["policer-app-limited-reset"] = reset.events
    return dict(
        status="passed",
        scenario_count=len(rows),
        scenarios=rows,
        scope="TCP callback port scenarios; not network execution or full independent acceptance",
    )


if __name__ == "__main__":
    r = run()
    Path(__file__).with_name("bbr-state-results.json").write_text(
        json.dumps(r, indent=2) + "\n"
    )
    print(json.dumps({"status": r["status"], "scenario_count": r["scenario_count"]}))
