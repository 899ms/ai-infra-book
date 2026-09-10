"""Public ACK policy regression from wire-time and varint hand arithmetic."""

import copy
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from infra_calc.topics import transport_closed_loop as network
from infra_calc.transport.ack_receiver import Receiver, varint_bytes


def inputs(upload=1168, delay="1/2"):
    # STREAM: (1168 + 32 + 28)*8 / 9824 = 1 second on wire.
    # ACK: (64 + 28)*8 / 736 = 1 second on wire. Each propagates 1s.
    return dict(
        upload_bytes=upload,
        response_bytes=0,
        model_seconds=0,
        until=20,
        links=dict(
            up=dict(rate_bps=9824, propagation=1),
            down=dict(rate_bps=736, propagation=1),
        ),
        sender=dict(
            initial_cwnd=2400,
            rtt_seed=dict(latest_rtt=4, smoothed_rtt=4, rttvar=2, min_rtt=4),
        ),
        ack_policy=dict(mode="count_or_timer", every=2, max_delay=delay),
    )


def down_acks(result):
    return [
        row
        for row in result["transmissions"]
        if row["direction"] == "down" and row["kind"] == "ack"
    ]


class AckPolicyTests(unittest.TestCase):
    def test_two_packets_trigger_one_ack(self):
        result = network.calculate(inputs(upload=2336, delay=10))
        # Packet arrivals at 2 and 3: count triggers at 3, ACK arrives at 5.
        acks = down_acks(result)
        self.assertEqual(len(acks), 1)
        self.assertEqual(F(acks[0]["send_start"]), 3)
        self.assertEqual(F(acks[0]["arrival"]), 5)
        self.assertEqual(acks[0]["ack_snapshot"]["ranges"], [[0, 1]])
        self.assertEqual(acks[0]["ack_snapshot"]["encoded_delay"], 0)
        self.assertEqual(result["final_states"]["up"]["bytes_in_flight"], 0)
        self.assertEqual(result["losses"]["up"], [])

    def test_tail_deadline_and_prior_rtt(self):
        result = network.calculate(inputs())
        ack = down_acks(result)[0]
        # Tail arrives 2, deadline 2.5, reverse serialization+propagation 2.
        self.assertEqual(F(ack["send_start"]), F(5, 2))
        self.assertEqual(F(ack["arrival"]), F(9, 2))
        self.assertEqual(ack["ack_snapshot"]["encoded_delay"], 62500)
        self.assertEqual(
            result["rtt_samples"]["up"],
            [dict(at="9/2", pn=0, raw="9/2", adjusted="4", smoothed="4", rttvar="3/2")],
        )
        state = result["final_states"]["up"]
        self.assertEqual(F(state["smoothed_rtt"]), 4)
        self.assertEqual(F(state["rttvar"]), F(3, 2))

    def test_first_rtt_does_not_subtract_ack_delay(self):
        scenario = inputs()
        scenario["sender"].pop("rtt_seed")
        scenario["sender"]["initial_rtt"] = 10  # An estimate, not a prior sample.
        result = network.calculate(scenario)
        self.assertEqual(
            result["rtt_samples"]["up"],
            [
                dict(
                    at="9/2",
                    pn=0,
                    raw="9/2",
                    adjusted="9/2",
                    smoothed="9/2",
                    rttvar="9/4",
                )
            ],
        )
        self.assertEqual(F(result["final_states"]["up"]["min_rtt"]), F(9, 2))
        self.assertEqual(result["losses"]["up"], [])

    def test_same_time_arrival_and_deadline_send_once(self):
        result = network.calculate(inputs(upload=2336, delay=1))
        # The second arrival and first tail deadline are both t=3.
        acks = down_acks(result)
        self.assertEqual(len(acks), 1)
        self.assertEqual(F(acks[0]["send_start"]), 3)
        self.assertEqual(acks[0]["ack_snapshot"]["ranges"], [[0, 1]])
        self.assertEqual(acks[0]["ack_snapshot"]["encoded_delay"], 0)

    def test_busy_reverse_serializer_exposes_real_delay_and_caps_rtt_deduction(self):
        scenario = inputs()
        scenario.update(response_bytes=1168, until=100)
        scenario["sender"]["rtt_seed"] = dict(
            latest_rtt=4, smoothed_rtt=4, rttvar=20, min_rtt=1
        )
        result = network.calculate(scenario)
        acks = down_acks(result)
        self.assertEqual(len(acks), 1)
        ack = acks[0]
        # Response starts at 2; its 1228 wire bytes take 307/23 seconds.
        # Queued ACK starts 353/23 and arrives another two seconds later.
        self.assertEqual(F(ack["send_start"]), F(353, 23))
        self.assertEqual(F(ack["arrival"]), F(399, 23))
        snapshot = ack["ack_snapshot"]
        self.assertEqual(F(snapshot["raw_delay"]), F(307, 23))
        self.assertEqual(snapshot["encoded_delay"], 1668478)
        self.assertEqual(F(snapshot["decoded_delay"]), F(834239, 62500))
        self.assertTrue(snapshot["exceeds_max_delay"])
        # Subtract only negotiated .5s, then use old SRTT=4 for variance.
        self.assertEqual(
            result["rtt_samples"]["up"],
            [
                dict(
                    at="399/23",
                    pn=0,
                    raw="399/23",
                    adjusted="775/46",
                    smoothed="2063/368",
                    rttvar="3351/184",
                )
            ],
        )
        self.assertEqual(result["losses"]["up"], [])

    def test_varint_width_boundaries_and_capacity_rejection_are_atomic(self):
        for number, width in (
            (0, 1),
            (63, 1),
            (64, 2),
            (16383, 2),
            (16384, 4),
            (2**30 - 1, 4),
            (2**30, 8),
            (2**62 - 1, 8),
        ):
            self.assertEqual(varint_bytes(number), width)
        for number in (-1, 2**62, True):
            with self.assertRaises(ValueError):
                varint_bytes(number)
        receiver = Receiver(dict(mode="count_or_timer", every=1))
        for pn in range(0, 512, 2):
            receiver.receive(pn, 0, True)
        state = copy.deepcopy(receiver.__dict__)
        # Header 24 + frame [type1,largest2,delay1,count2,first1,
        # 255*(gap1,length1)] = 24+517 = 541 bytes exactly.
        for capacity in (64, 540):
            with self.assertRaises(ValueError):
                receiver.snapshot(F(0), capacity)
            self.assertEqual(receiver.__dict__, state)
        snapshot = receiver.snapshot(F(0), 541)
        self.assertEqual(snapshot["frame_bytes"], 517)
        self.assertEqual(snapshot["ranges"], [[pn, pn] for pn in range(0, 512, 2)])

    def test_queued_snapshot_uses_largest_pn_and_floors_ticks(self):
        receiver = Receiver(dict(mode="count_or_timer", every=1))
        receiver.receive(2, "0.020", True)
        receiver.receive(0, "0.029", True)
        snapshot = receiver.snapshot(F(30003, 1000000), 64)
        # Largest PN arrived at .020, not the last-arriving lower PN.
        self.assertEqual(F(snapshot["raw_delay"]), F(10003, 1000000))
        self.assertEqual(snapshot["encoded_delay"], 1250)
        self.assertEqual(F(snapshot["encoding_error"]), F(-3, 1000000))
        self.assertEqual(snapshot["ranges"], [[0, 0], [2, 2]])

    def test_legacy_default_remains_immediate_and_example_entrypoint_works(self):
        scenario = inputs(upload=2336)
        scenario.pop("ack_policy")
        implicit = network.calculate(scenario)
        explicit = network.calculate(dict(scenario, ack_policy="immediate_each_packet"))
        # The caller-supplied inputs are echoed; only that echo differs.
        self.assertEqual(implicit["inputs"], scenario)
        self.assertEqual(explicit["inputs"]["ack_policy"], "immediate_each_packet")
        self.assertEqual(
            {k: v for k, v in implicit.items() if k != "inputs"},
            {k: v for k, v in explicit.items() if k != "inputs"},
        )
        # Legacy emits an ACK for each arrival, without a count/timer wait.
        self.assertEqual(
            [F(row["send_start"]) for row in down_acks(implicit)], [F(2), F(3)]
        )
        self.assertEqual(
            [F(row["arrival"]) for row in down_acks(implicit)], [F(4), F(5)]
        )
        self.assertEqual(network.calculate(), network.calculate(network.example()))


if __name__ == "__main__":
    unittest.main()
