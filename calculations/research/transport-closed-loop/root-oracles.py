"""Preimplementation physical-event arithmetic, independent of sender/network code.

These expected traces implement the five hand examples in the network contract.
They are not a general simulator and do not prove the future candidate passes.
"""
from fractions import Fraction as F
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
UP = 9824
DOWN = 736
PROPAGATION = F(1)
IP_UDP = 28


def transfer(start, quic_bytes, rate):
    end = F(start) + F(8 * (quic_bytes + IP_UDP), rate)
    return dict(start=str(start), end=str(end), receive=str(end + PROPAGATION),
                quic_bytes=quic_bytes, wire_bytes=quic_bytes + IP_UDP)


def data(start):
    return transfer(F(start), 1200, UP)


def ack(start):
    return transfer(F(start), 64, DOWN)


first_ack = ack(F(data(0)["receive"]))
third_start = F(first_ack["receive"])
response_start = F(data(1)["receive"]) + 1
response = transfer(response_start, 64, DOWN)
response_ack = transfer(F(response["receive"]), 64, UP)
max_update = transfer(F(4), 64, DOWN)
max_ack = transfer(F(max_update["receive"]), 64, UP)
flow_third = F(max_ack["end"])
loss_observed = F(ack(F(data(1)["receive"]))["receive"])
pto = F(4) + 4 * F(2)

cases = {
    "cwnd-three-packets": dict(
        data=[data(0), data(1), data(third_start)],
        acks=[first_ack, ack(3), ack(F(data(third_start)["receive"]))],
        third_send=str(third_start), first_rtt=first_ack["receive"],
        unique_stream_bytes=3504, wire_c2s=3*1228, wire_s2c=3*92),
    "model-response-before-last-upload-ack": dict(
        request=[data(0), data(1)], upload_acks=[ack(2), ack(3)],
        model_start=data(1)["receive"], model_duration="1", model_end=str(response_start),
        response=response, response_ack=response_ack,
        final_business=response["receive"], final_response_ack=response_ack["receive"],
        unique_request_bytes=2336, unique_response_bytes=32,
        wire_c2s=2*1228+92, wire_s2c=3*92),
    "consumed-credit-arrives-later": dict(
        initial_max_data=2336, initial_max_stream_data=2336,
        consume_at="4", consumed_unique_bytes=2336,
        max_update=max_update, max_update_ack=max_ack, flow_eligible_at=max_update["receive"],
        new_max_data=4672, new_max_stream_data=4672,
        data=[data(0), data(1), data(flow_third)],
        third_send=str(flow_third), third_receive=data(flow_third)["receive"],
        ordinary_ack_does_not_open_flow=True, wire_c2s=3*1228+92, wire_s2c=4*92),
    "hole-recovery-from-actual-feedback": dict(
        lost_original=dict(pn=0, **data(0)), later=dict(pn=1, **data(1)),
        later_ack=ack(3), loss_observed=str(loss_observed), threshold_duration="9/2",
        recovery=dict(pn=2, offset=0, **data(loss_observed)),
        recovery_ack=ack(F(data(loss_observed)["receive"])),
        ordered_request_complete=data(loss_observed)["receive"],
        unique_request_bytes=2336, transmitted_stream_bytes=3504,
        wire_c2s=3*1228, wire_s2c=2*92),
    "tail-pto-actual-probe": dict(
        seed_smoothed_rtt="4", seed_rttvar="2", max_ack_delay="0", first_pto=str(pto),
        lost_original=dict(pn=0, **data(0)),
        probe=dict(pn=1, offset=0, **data(pto)),
        probe_ack=ack(F(data(pto)["receive"])),
        first_loss_evidence=ack(F(data(pto)["receive"]))["receive"],
        pto_itself_marks_loss=False, unique_request_bytes=1168,
        transmitted_stream_bytes=2336, wire_c2s=2*1228, wire_s2c=92),
}
assert third_start == 4 and flow_third == F(6) + F(23, 307) and loss_observed == 5 and pto == 12
assert F(response["start"]) < F(ack(3)["receive"])
assert response["receive"] == "6" and response_ack["receive"] == "2172/307"
result = dict(status="preimplementation-arithmetic-only-not-candidate-acceptance",
              units="seconds, bytes; 28-byte declared IPv4/UDP overhead",
              reference_contract="../transport-feedback/NEXT-NETWORK-CONTRACT.md",
              policy="ACK every ack-eliciting packet immediately; ACK-only not acknowledged; explicit consumption only in flow fixture",
              correction="Flow fixture originally conflated eligibility at 6s with actual sending: MAX is ack-eliciting, so its independent reverse ACK occupies the uplink for 23/307s before the next STREAM packet. Corrected after protocol implementation review; no ACK coalescing introduced to preserve the old expectation.",
              cases=cases)
(ROOT / "root-oracles.json").write_text(json.dumps(result, indent=2) + "\n")
print("Wrote five exact physical-event expectations; candidate not executed")
