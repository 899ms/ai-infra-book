"""Public shared-radio mechanisms with precomputed causal boundaries."""

import copy
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from infra_calc.topics.transport_closed_loop import calculate
from infra_calc.transport.airtime import exchange
from infra_calc.transport.reference_sources import reference_sources
from test_media_feedback import inputs, message

TEACHING = dict(
    contention_seconds="0",
    propagation_seconds="0",
    data_ppdu_seconds="1",
    post_data_sifs_plus_mac_ack_seconds="1/4",
    transport_ack_whole_exchange_seconds="1/2",
    transport_ack_ppdu_seconds="1/4",
    transport_ack_post_data_sifs_plus_mac_ack_seconds="1/4",
    whole_exchange_includes_own_mac_ack=True,
    full_ack_failure_known_from_data_txstart_seconds="3/2",
)
REFERENCE = dict(
    phy=dict(
        data_rate_bps=54000000,
        mac_ack_rate_bps=6000000,
        ofdm_symbol_seconds="0.000004",
        service_bits=16,
        tail_bits=6,
        preamble_seconds="0.000016",
        signal_header_seconds="0.000004",
        signal_extension_seconds="0",
    ),
    layout=dict(
        llc_snap_bytes=8,
        data_mac_header_bytes=24,
        mac_fcs_bytes=4,
        security_overhead_bytes=0,
        normal_mac_ack_header_bytes=10,
        normal_mac_ack_fcs_bytes=4,
    ),
    access=dict(
        pre_exchange_idle_seconds="0.000034",
        backoff_slots_selected=0,
        slot_seconds="0.000009",
        direction_switch_extra_seconds="0",
        radio_propagation_selected_seconds="0",
        sifs_seconds="0.000016",
        mac_ack_complete_timeout_seconds=None,
    ),
)


def case(messages, **overrides):
    p = inputs(
        messages,
        links={d: dict(rate_bps=9824, propagation=0) for d in ("up", "down")},
        until=12,
        sender=dict(
            rtt_seed=dict(latest_rtt=100, smoothed_rtt=100, rttvar=50, min_rtt=100)
        ),
    )
    p["network"]["wireless_access"] = dict(
        enabled=True,
        profile=copy.deepcopy(TEACHING),
        max_attempts=2,
        retry_wait="1/2",
        failures=[],
    )
    p["network"].update(overrides)
    return p


class SharedAirtimeTests(unittest.TestCase):
    def test_selected_ofdm_and_unknown_failure_wait(self):
        row = exchange(REFERENCE, 1228)
        self.assertEqual(row["data_psdu_bytes"], 1264)
        self.assertEqual(row["mac_ack_psdu_bytes"], 14)
        self.assertEqual(row["data_ppdu"]["duration"], F(208, 1000000))
        self.assertEqual(row["exchange_end_offset"], F(302, 1000000))
        with self.assertRaises(ValueError):
            exchange(REFERENCE, 1228, "mac_ack_lost")
        invalid = copy.deepcopy(REFERENCE)
        invalid["access"]["mac_ack_complete_timeout_seconds"] = "0.000045"
        with self.assertRaises(ValueError):
            exchange(invalid, 1228, "mac_ack_lost")

    def test_shared_direction_and_appended_wan(self):
        r = calculate(
            case([message("up", size=1), message("down", sender="server", size=1)])
        )
        data = [a for a in r["wireless_attempts"] if a["kind"] == "data"]
        self.assertEqual(
            [(a["direction"], F(a["reservation_start"])) for a in data],
            [("up", F(0)), ("down", F(5, 4))],
        )
        self.assertEqual(F(r["delivered"]["up"]), 2)
        self.assertEqual(F(r["delivered"]["down"]), F(9, 4))
        for a, b in zip(r["wireless_reservations"], r["wireless_reservations"][1:]):
            self.assertLessEqual(F(a["end"]), F(b["start"]))

    def test_disabled_has_identical_original_payload(self):
        p = case([message("x", size=1)])
        del p["network"]["wireless_access"]
        expected = calculate(p)
        p["network"]["wireless_access"] = {"enabled": False}
        self.assertEqual(calculate(p), expected)

    def test_down_mac_duplicate_stays_below_transport(self):
        p = case([message("x", sender="server", size=1)])
        p["network"]["wireless_access"]["failures"] = [
            dict(direction="down", pn=0, attempt=1, outcome="mac_ack_lost")
        ]
        r = calculate(p)
        self.assertEqual(len([t for t in r["transmissions"] if t["kind"] == "ack"]), 1)
        self.assertEqual(
            [a["pn"] for a in r["wireless_attempts"] if a["direction"] == "down"],
            [0, 0],
        )
        self.assertEqual(
            len([e for e in r["sender_events"]["down"] if e["type"] == "sent"]), 1
        )
        self.assertEqual(r["summary"]["unique_received_application_bytes"], 1)

    def test_mac_exhaustion_waits_for_real_pto(self):
        p = case([message("x", size=1)], sender={"initial_rtt": "4/3"})
        p["network"]["wireless_access"]["failures"] = [
            dict(direction="up", pn=0, attempt=n, outcome="data_lost") for n in (1, 2)
        ]
        r = calculate(p)
        data = [t for t in r["transmissions"] if t["kind"] == "data"]
        self.assertEqual(
            [(t["pn"], F(t["send_start"])) for t in data], [(0, F(0)), (1, F(4))]
        )
        self.assertTrue(data[1]["probe"])
        self.assertEqual(F(r["delivered"]["x"]), 6)

    def test_source_ack_refresh_waits_for_radio(self):
        policy = dict(
            mode="count_or_timer",
            every=2,
            max_delay="1/4",
            delay_exponent=3,
            retain_packets=256,
            reorder_immediate=True,
            header_tag_bytes=24,
        )
        p = case(
            [message(str(i), sender="server", size=1) for i in range(3)],
            initial_cwnd=4800,
            ack_policy=policy,
        )
        r = calculate(p)
        ack = next(t for t in r["transmissions"] if t["kind"] == "ack")
        self.assertEqual(F(ack["send_start"]), F(7, 2))
        self.assertEqual(ack["ack_snapshot"]["ranges"], [[0, 1]])
        self.assertEqual(F(ack["ack_snapshot"]["raw_delay"]), F(1, 4))

    def test_preamble_horizon_does_not_invent_ip_bytes(self):
        p = case([message("x", size=1)], until="0.000044")
        p["network"]["wireless_access"]["profile"] = copy.deepcopy(REFERENCE)
        r = calculate(p)
        self.assertIsNone(r["summary"]["serialized_wire_bytes_by_horizon"])
        self.assertEqual(r["summary"]["wan_serialized_ip_bytes_by_horizon"], "0")
        self.assertFalse(r["wireless_attempts"][0]["received"])
        self.assertEqual(
            F(r["wireless_summary"]["observed_reserved_seconds"]), F(44, 1000000)
        )

    def test_wan_arrival_is_not_final_client_arrival(self):
        r = calculate(case([message("x", sender="server", size=1)], until="1/2"))
        packet = r["transmissions"][0]
        self.assertIsNone(packet["arrival"])
        self.assertEqual(F(packet["wan_arrival"]), 1)
        self.assertEqual(r["wireless_attempts"], [])
        self.assertEqual(F(r["summary"]["wan_serialized_ip_bytes_by_horizon"]), 614)

    def test_official_group_and_strict_outer_dispatch(self):
        rows = reference_sources("shared_airtime")
        self.assertEqual(len(rows), 14)
        self.assertTrue(
            all(r["file"].startswith("sources/shared-airtime/") for r in rows)
        )
        p = case([message("x", size=1)])
        p["upload_bytes"] = 1
        with self.assertRaises(ValueError):
            calculate(p)


if __name__ == "__main__":
    unittest.main()
