from fractions import Fraction
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from infra_calc.topics import edge_tiers


class EdgeTiersTests(unittest.TestCase):
    @staticmethod
    def _read(path):
        rows = {
            "results/qwen3-8b-decode-b1-s8192.json": {
                "summary": {
                    "weight_read_once_per_operator_bytes": 640,
                    "kv_existing_history_unique_payload_bytes": 20,
                }
            },
            "results/energy-ledger-book.json": {"summary": {"phone_bus_gb_per_second": 1}},
            "experiments/ch08/08-01/efficiency.json": {
                "rows": [{"context": 8192, "batch": 1, "decode_round_ms": 2, "peak_read_ms": 1}]
            },
            "results/vision-encoding-single.json": {
                "summary": {"matrix_flops_per_image": 1000, "complete_encoder_bytes_per_image": 100}
            },
        }
        return rows[path]

    @staticmethod
    def _device(identifier):
        return {
            "name": identifier,
            "memory": {"bandwidth_bytes_per_second": 1000},
            "power_watts": 1,
        }

    def _calculate(self, deadline_seconds):
        with (
            patch.object(edge_tiers, "_read", side_effect=self._read),
            patch.object(edge_tiers, "_peak", return_value=Fraction(1000)),
            patch.object(edge_tiers, "prefill_flops", return_value=0),
            patch.object(edge_tiers.hardware, "select_device", side_effect=self._device),
        ):
            return edge_tiers.calculate(
                cases=({"id": "deadline", "rounds": 20, "deadline_seconds": deadline_seconds},)
            )

    def test_impossible_deadline_has_no_uplink_threshold(self):
        for deadline_seconds in (1, 190):
            with self.subTest(deadline_seconds=deadline_seconds):
                result = self._calculate(deadline_seconds=deadline_seconds)

                self.assertIsNone(result["uplink"]["cloud_deadline_uplink_bits_per_second"])
                self.assertIsNone(result["summary"]["cloud_deadline_uplink_mbit_per_second"])
                self.assertEqual(
                    result["uplink"]["cloud_never_meets_deadline_reason"],
                    "cloud time without upload already meets or exceeds the deadline",
                )

    def test_feasible_deadline_keeps_positive_uplink_threshold(self):
        result = self._calculate(deadline_seconds=1000)

        self.assertGreater(result["uplink"]["cloud_deadline_uplink_bits_per_second"], 0)
        self.assertIsNone(result["uplink"]["cloud_never_meets_deadline_reason"])


if __name__ == "__main__":
    unittest.main()
