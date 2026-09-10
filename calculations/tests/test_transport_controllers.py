"""Independent arithmetic and protocol boundaries for public controller inputs."""
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from infra_calc.topics import transport_closed_loop as network
from infra_calc.topics.transport_sender import create_sender
from infra_calc.transport.pacer import Pacer


class ControllerTests(unittest.TestCase):
    def test_rate_changes_settle_only_elapsed_old_rate(self):
        p = Pacer(1200)
        p.sent(0, 1200)
        p.advance(F(1, 4), 2400)
        self.assertEqual(p.debt, 900)
        self.assertEqual(p.ready(F(1, 4)), F(5, 8))
        p.advance(F(3, 8), 600)
        self.assertEqual(p.ready(F(3, 8)), F(11, 8))

    def test_padding_and_ack_physical_serialization(self):
        p = network.example()
        p.update(upload_bytes=3504, response_bytes=32, model_seconds=0,
                 controller={"name": "newreno"}, pad_in_flight=True, until=8)
        p["sender"]["initial_cwnd"] = 12000
        p["links"] = {d: dict(rate_bps=1000000000, propagation=1) for d in ("up", "down")}
        r = network.calculate(p)
        data = [t for t in r["transmissions"] if t["kind"] == "data"]
        self.assertEqual([F(t["send_start"]) for t in data[:3]], [0, F(8, 25), F(16, 25)])
        self.assertEqual(F(data[3]["send_start"]), F(16, 25) + 1 + F(8 * (1228 + 92), 1000000000))
        self.assertEqual(data[3]["quic_bytes"], 1200)
        self.assertEqual(r["summary"]["wire_bytes"], 4 * (1228 + 92))
        self.assertEqual(r["summary"]["unique_received_bytes"], 3536)
        self.assertIn("控制器与发送节奏", network.markdown(r))

    def test_three_controller_sources_and_business_accounting(self):
        for name in ("newreno", "cubic_hystart", "bbr"):
            with self.subTest(controller=name):
                p = network.example()
                p.update(controller={"name": name}, pad_in_flight=True, until=60)
                r = network.calculate(p)
                self.assertTrue(r["summary"]["complete"])
                self.assertEqual(r["summary"]["unique_received_bytes"], 2368)
                files = {row["file"] for row in r["reference_sources"]}
                self.assertTrue(all(not path.startswith("research/") for path in files))
                if name == "bbr":
                    self.assertIn("sources/congestion-controllers/tcp_bbr.c", files)
                    self.assertIn("sources/congestion-controllers/win_minmax.c", files)
                if name == "cubic_hystart":
                    self.assertIn("sources/congestion-controllers/rfc9406.txt", files)

    def test_persistent_action_deduplicates_late_ack(self):
        for controller in ("newreno", "cubic_hystart"):
            with self.subTest(controller=controller):
                state = create_sender(dict(
                    until=9, initial_cwnd=120000, initial_max_data=100000,
                    initial_max_stream_data={"b": 100000}, events=[], max_ack_delay=0,
                    rtt_seed=dict(latest_rtt=".1", smoothed_rtt=".1", rttvar=".025", min_rtt=".1"),
                    controller={"name": controller, "pad_in_flight": True},
                ))
                for pn in range(9):
                    state["enqueue"](dict(type="sent", at=str(pn), pn=pn, sent_bytes=1200,
                        ack_eliciting=True, in_flight=True,
                        frames=[dict(type="stream", stream="b", offset=1168 * pn, length=1168)]))
                state["enqueue"](dict(type="ack", at="8.1", ranges=[[8, 8]]))
                state["advance"]("8.1")
                self.assertEqual(F(state["state"]()["cwnd"]), 2400)
                self.assertEqual(F(state["persistent_events"][0]["evidence"]["threshold_duration"]), F(21, 40))
                state["enqueue"](dict(type="ack", at="8.2", ranges=[[0, 0]]))
                state["advance"]("8.2")
                self.assertEqual(len(state["persistent_events"]), 1)
                self.assertEqual(F(state["state"]()["cwnd"]), 2400)


if __name__ == "__main__":
    unittest.main()
