"""Finite sender snapshot and late-ACK checks, without a network engine."""

from pathlib import Path
import json
from bbr_adapter import BbrAdapter


def packet(pn, flight=True, frames=None):
    return dict(
        pn=pn,
        sent_bytes=1200 if flight else 64,
        in_flight=flight,
        ack_eliciting=flight,
        frames=frames or [],
    )


def run():
    b = BbrAdapter()
    frame = [dict(stream="A", offset=0, length=1168)]
    b.on_sent(packet(0, frames=frame), dict(now="0", flight_before=0))
    b.on_loss([0], dict(now="1/20", flight_after=0))
    b.on_sent(packet(1, frames=frame), dict(now="2/25", flight_before=0))
    first = b.on_ack(
        [1],
        dict(
            now="1/10",
            flight_before=1200,
            flight_after=0,
            rtt_sample={"raw": "1/50"},
            smoothed_rtt="1/10",
        ),
    )
    assert first["sample"]["bw_scaled"] == 838 and b.delivered == 1
    late = b.on_ack(
        [0],
        dict(
            now="3/25",
            flight_before=0,
            flight_after=0,
            rtt_sample=None,
            smoothed_rtt="1/10",
        ),
    )
    assert late["sample"]["bw_scaled"] == 279 and b.delivered == 2
    assert late["callback"]["input"]["rtt_us"] == -1
    duplicate = b.on_ack([0], dict(now="13/100", flight_after=0))
    assert b.delivered == 2 and duplicate["event"] == "ack_no_new_counted_pn"
    b.on_sent(packet(2), dict(now="3/20", flight_before=0))
    b.on_sent(packet(3, False), dict(now="4/25", flight_before=1200))
    mixed = b.on_ack(
        [2, 3],
        dict(
            now="1/4",
            flight_before=1200,
            flight_after=0,
            rtt_sample={"raw": "1/10"},
            smoothed_rtt="1/10",
        ),
    )
    assert mixed["newly_counted_pns"] == [2] and b.delivered == 3
    before = b.cwnd_bytes
    b.on_pto(dict(now="3/10"))
    assert b.cwnd_bytes == before
    # ACK-time application queue state never overwrites the selected send flag.
    flags = BbrAdapter()
    flags.on_sent(
        packet(0), dict(now=0, flight_before=0, flow_limited=True, app_limited=False)
    )
    result = flags.on_ack([0], dict(now="1/10", flight_after=0, app_limited=True))
    assert (
        not result["sample"]["is_app_limited"]
        and result["flow_limited_at_selected_send"]
    )
    external = BbrAdapter(config={"external_pacer": True})
    external.on_sent(packet(0), dict(now=0, flight_before=0))
    mapped = external.on_ack(
        [0],
        dict(
            now="1/10",
            flight_before=1200,
            flight_after=0,
            pacer_next_eligible="1/2",
            rtt_sample={"raw": "1/10"},
            smoothed_rtt="1/10",
        ),
    )
    assert mapped["callback"]["input"]["edt_ns"] == 500001000
    assert external.snapshot()["next_eligible_seconds_exact"] is None
    idle = BbrAdapter()
    idle.on_sent(packet(0, frames=frame), dict(now=0, flight_before=0))
    idle.on_loss([0], dict(now="1/20", flight_after=0))
    idle.on_sent(packet(1, frames=frame), dict(now="2/25", flight_before=0))
    idle.on_ack(
        [1],
        dict(
            now="1/10", flight_before=1200, flight_after=0, rtt_sample={"raw": "1/50"}
        ),
    )
    assert not idle.records[0]["acked"] and not idle.active()
    idle.on_sent(packet(2), dict(now=10, flight_before=0))
    assert idle.records[2]["first_tx_us"] == 10000001
    assert idle.records[2]["delivered_mstamp_us"] == 10000001
    resumed = idle.on_ack(
        [2],
        dict(
            now="101/10", flight_before=1200, flight_after=0, rtt_sample={"raw": "1/10"}
        ),
    )
    assert (
        resumed["sample"]["interval_us"] == 100000
        and resumed["sample"]["bw_scaled"] == 167
    )
    evidence = {"first_pn": 0, "last_pn": 2, "loss_epoch": "example"}
    before_mode = idle.core.mode
    override = idle.on_persistent(dict(now=11, evidence_key=evidence))
    assert (
        override["new_evidence"]
        and idle.cwnd_bytes == 2400
        and idle.core.mode == before_mode
    )
    idle.core.cwnd = 5
    duplicate_override = idle.on_persistent(dict(now=12, evidence_key=evidence))
    assert not duplicate_override["new_evidence"] and idle.cwnd_bytes == 6000
    rejected = 0
    for call in [
        lambda: BbrAdapter().on_sent(
            dict(packet(0), sent_bytes=64), dict(now=0, flight_before=0)
        ),
        lambda: BbrAdapter().on_sent(packet(0), dict(now=0, flight_before=1200)),
    ]:
        try:
            call()
        except ValueError:
            rejected += 1
    assert rejected == 2
    return dict(
        status="passed",
        scope="Local sender hooks only; closed-loop integration pending",
        late_ack_and_control_trace=b.events,
        limited_trace=flags.events,
        external_pacer_trace=external.events,
        idle_after_recovery_trace=idle.events,
        rejected_cases=rejected,
    )


if __name__ == "__main__":
    result = run()
    Path(__file__).with_name("bbr-adapter-check.json").write_text(
        json.dumps(result, indent=2) + "\n"
    )
    print(
        json.dumps(
            {"status": result["status"], "rejected_cases": result["rejected_cases"]}
        )
    )
