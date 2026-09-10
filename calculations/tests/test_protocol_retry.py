"""Independent hand times and causal/identity boundaries for QUIC retry graphs."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from infra_calc.topics import protocol_retry as candidate


def hand_inputs(branch="none", early=False, count=1):
    """Each declared datagram costs1s serialization plus1s propagation."""
    p = candidate.example()
    p.update(
        handshake_event=branch, send_early=early,
        request_payload_bytes=1168 * count, response_payload_bytes=100,
        packet_payload_bytes=1168, zero_rtt_overhead_bytes=32,
        one_rtt_overhead_bytes=32, response_overhead_bytes=1100,
        c2s_bits_per_second=9824, s2c_bits_per_second=9824,
        c2s_propagation_seconds=1, s2c_propagation_seconds=1,
        model_seconds=0, server_flight_ack=False,
    )
    p["packets"] = {name: [1200] for name in (
        "client_hello", "client_finished", "handshake_ack", "retry",
        "client_hello_retry", "hrr", "client_hello_hrr", "failure",
    )}
    p["packets"]["server_flight"] = [1200, 1200]
    return p


class ProtocolRetryTests(unittest.TestCase):
    def test_first_normal_request_needs_no_replay_authorization_after_hrr_or_retry(self):
        # No early bytes were sent: this is a first request, not app replay.
        for branch, request_at, response_at in (
            ("none", 8, 10), ("hrr", 12, 14),
            ("retry", 12, 14), ("psk_unknown_fallback", 8, 10),
        ):
            with self.subTest(branch=branch):
                p = hand_inputs(branch)
                p.update(application_retry_authorized=False,
                         application_early_data_authorized=False)
                if branch == "psk_unknown_fallback":
                    p["valid_psk"] = False
                r = candidate.calculate(p)
                self.assertEqual(r["status"], "complete")
                self.assertEqual(r["summary"]["early_payload_sent_bytes"], 0)
                self.assertEqual(F(r["milestones"]["complete_request"]), request_at)
                self.assertEqual(F(r["milestones"]["complete_response"]), response_at)
                self.assertEqual(r["summary"]["application_execution_count"], 1)

    def test_retry_preserves_packet_numbers_and_stream_ranges_with_new_initial_keys(self):
        r = candidate.calculate(hand_inputs("retry", True, 4))
        request = [e for e in r["transmissions"] if e["kind"] == "request"]
        self.assertEqual([e["packet_number"] for e in request], list(range(7)))
        self.assertTrue(all(e["packet_number_space"] == "application" for e in request))
        self.assertEqual([e["offset"] for e in request],
                         [0, 1168, 2336, 0, 1168, 2336, 3504])
        self.assertTrue(all(e["application_key_epoch"] == 0 for e in request))
        self.assertTrue(all(e["encryption_level"] == "0rtt" for e in request))
        self.assertEqual(r["summary"]["early_payload_sent_bytes"], 8176)
        self.assertEqual(r["summary"]["accepted_unique_request_bytes"], 4672)
        self.assertEqual(F(r["milestones"]["complete_response"]), 12)
        old = next(e for e in r["transmissions"] if e["kind"] == "client_hello")
        new = next(e for e in r["transmissions"] if e["kind"] == "client_hello_retry")
        self.assertEqual((old["packet_number"], new["packet_number"]), (0, 1))
        self.assertEqual((old["initial_key_epoch"], new["initial_key_epoch"]), (0, 1))
        self.assertEqual(old["source_connection_id"], new["source_connection_id"])
        self.assertEqual(old["tls_client_hello_identity"], new["tls_client_hello_identity"])
        self.assertEqual(new["destination_connection_id"], r["inputs"]["retry_scid"])
        self.assertNotIn("packet_number", next(e for e in r["transmissions"] if e["kind"] == "retry"))
        self.assertTrue(all(not e["accepted"] for e in request[:3]))

    def test_tls_rejection_after_retry_counts_wire_repeats_but_not_duplicate_execution(self):
        for retry_authorized in (False, True):
            with self.subTest(retry_authorized=retry_authorized):
                p = hand_inputs("retry", True, 4)
                p.update(early_result="reject", application_retry_authorized=retry_authorized)
                r = candidate.calculate(p)
                self.assertEqual(r["summary"]["application_execution_count"], int(retry_authorized))
                accepted = Counter()
                for e in r["transmissions"]:
                    if e["kind"] == "request" and e["accepted"]:
                        self.assertEqual(e["encryption_level"], "1rtt")
                        accepted.update(range(e["offset"], e["end_offset"]))
                self.assertEqual(accepted, Counter({i: 1 for i in range(4672)}) if retry_authorized else Counter())
                self.assertEqual("complete_response" in r["milestones"], retry_authorized)
                self.assertEqual(r["summary"]["one_rtt_payload_sent_bytes"], 4672 if retry_authorized else 0)
        p = hand_inputs("retry", True, 4)
        p["retry_early_replay_authorized"] = False
        with self.assertRaises(ValueError):
            candidate.calculate(p)

    def test_hrr_stops_new_early_packets_but_keeps_the_in_progress_packet(self):
        for reverse_delay in ("1", "1/2"):
            with self.subTest(reverse_delay=reverse_delay):
                p = hand_inputs("hrr", True, 4)
                p["s2c_propagation_seconds"] = reverse_delay
                r = candidate.calculate(p)
                hrr = F(r["milestones"]["hrr_received"])
                early = [e for e in r["transmissions"] if e["kind"] == "request" and e["encryption_level"] == "0rtt"]
                self.assertEqual([(F(e["start"]), F(e["end"])) for e in early], [(1, 2), (2, 3), (3, 4)])
                self.assertTrue(all(F(e["start"]) < hrr and not e["accepted"] for e in early))
                second = next(e for e in r["transmissions"] if e["kind"] == "client_hello_hrr")
                self.assertEqual(second["tls_client_hello_identity"], "CH2-no-early-data")
                self.assertEqual(second["retry_token_bytes"], 0)
                self.assertEqual(F(second["start"]), 4)
                self.assertEqual(r["summary"]["accepted_unique_request_bytes"], 4672)

    def test_failure_notification_propagates_before_sender_stops(self):
        for branch in ("selected_binder_invalid", "psk_unknown_abort"):
            with self.subTest(branch=branch):
                p = hand_inputs(branch, True, 4)
                p.update(valid_psk=False, client_credentials_available=True)
                r = candidate.calculate(p)
                self.assertEqual(r["status"], "handshake_failed")
                failure = next(e for e in r["transmissions"] if e["kind"] == "failure")
                self.assertEqual(failure["packet_number_space"], "initial")
                self.assertEqual((F(failure["start"]), F(failure["arrival"])), (2, 4))
                request = [e for e in r["transmissions"] if e["kind"] == "request"]
                self.assertEqual([(F(e["start"]), F(e["end"])) for e in request], [(1, 2), (2, 3), (3, 4)])
                self.assertTrue(all(not e["accepted"] for e in request))
                self.assertEqual(F(r["summary"]["last_modeled_arrival"]), 5)
                self.assertEqual(r["summary"]["application_execution_count"], 0)
        # Close must also stop queued controls, not just application data.
        p = hand_inputs("retry", True, 20)
        p["retry_token_valid"] = False
        p["packets"]["client_hello_retry"] = [1200] * 10
        r = candidate.calculate(p)
        notified = F(r["milestones"]["failure_received"])
        self.assertTrue(all(F(e["start"]) < notified for e in r["transmissions"] if e["direction"] == "c2s"))
        self.assertNotIn("server_address_validated", r["milestones"])

    def test_first_token_packet_validates_before_complete_clienthello(self):
        p = hand_inputs("retry")
        p.update(retry_token_bytes=400, client_hello_crypto_bytes=900)
        p["packets"]["client_hello_retry"] = [1200, 1200]
        r = candidate.calculate(p)
        self.assertEqual(F(r["milestones"]["retry_received"]), 4)
        self.assertEqual(F(r["milestones"]["server_address_validated"]), 6)
        self.assertEqual(F(r["milestones"]["client_hello_retry_received"]), 7)
        self.assertEqual(F(r["milestones"]["complete_response"]), 15)
        packets = [e for e in r["transmissions"] if e["kind"] == "client_hello_retry"]
        self.assertEqual([e["retry_token_bytes"] for e in packets], [400, 400])
        self.assertEqual([e["packet_number"] for e in packets], [1, 2])

    def test_invalid_retry_is_discarded_and_waits_for_unmodeled_recovery(self):
        p = hand_inputs("retry", True, 4)
        p["retry_integrity_valid"] = False
        r = candidate.calculate(p)
        self.assertEqual(r["status"], "waiting_unmodeled_recovery")
        self.assertFalse(any(e["kind"] == "client_hello_retry" for e in r["transmissions"]))
        self.assertNotIn("server_address_validated", r["milestones"])
        self.assertEqual(r["summary"]["accepted_unique_request_bytes"], 0)
        self.assertEqual(r["summary"]["application_execution_count"], 0)
        self.assertTrue(all(e.get("attempt_epoch", 0) == 0 for e in r["transmissions"]))

    def test_unsupported_message_shapes_and_missing_replay_permission_reject(self):
        cases = []
        for key, value in (("retry_token_bytes", 0), ("retry_token_valid", 1),
                           ("handshake_event", "hrr+retry"), ("client_hello_crypto_bytes", 2000)):
            p = hand_inputs("retry")
            p[key] = value
            cases.append(p)
        p = hand_inputs("retry")
        p["packets"]["retry"] = [1200, 1200]
        cases.append(p)
        p = hand_inputs("selected_binder_invalid")
        p["packets"]["failure"] = [1200, 1200]
        cases.append(p)
        p = hand_inputs("retry")
        p.update(retry_token_bytes=1160, client_hello_crypto_bytes=100)
        cases.append(p)
        for index, p in enumerate(cases):
            with self.subTest(case=index), self.assertRaises(ValueError):
                candidate.calculate(p)


if __name__ == "__main__":
    unittest.main()
