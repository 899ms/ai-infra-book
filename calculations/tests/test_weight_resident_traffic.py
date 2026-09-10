"""Independent checks for the weight-residency traffic account (C73).

The expected figures are the OpenTallas case study's own published numbers, so
these tests check the module against the case rather than against itself.
"""
import json
import math
import unittest
from fractions import Fraction
from pathlib import Path
import sys

for ancestor in Path(__file__).resolve().parents:
    if (ancestor / "src/infra_calc/sources.py").is_file():
        sys.path.insert(0, str(ancestor / "src"))
        break
from infra_calc import topics

topics.__path__.insert(0, str(Path(__file__).resolve().parents[1] / "src/infra_calc/topics"))
from infra_calc.topics import weight_resident_traffic as m
from infra_calc.sources import model_config


def value(entry):
    return Fraction(**entry)


class GeometryTests(unittest.TestCase):
    def test_checkpoint_and_active_read_match_the_case_study(self):
        shape = m.geometry("qwen3-8b")
        self.assertEqual(shape["checkpoint_bytes"], 16_381_470_720)
        self.assertEqual(shape["active_decode_read_bytes"], 15_136_811_008)
        # The gap is exactly the embedding lookup table decode does not stream.
        self.assertEqual(shape["checkpoint_bytes"] - shape["active_decode_read_bytes"],
                         shape["params_embedding"] * 2)

    def test_state_bytes_match_the_case_study(self):
        shape = m.geometry("qwen3-8b")
        config = model_config("qwen3-8b")
        self.assertEqual(shape["kv_bytes_per_token"], 147_456)
        self.assertEqual(shape["kv_bytes_per_token"],
                         2 * 2 * config["num_hidden_layers"] * config["num_key_value_heads"] * config["head_dim"])

    def test_rejects_a_model_this_adapter_does_not_cover(self):
        for name in ("qwen3-235b-a22b", "deepseek-v3"):
            with self.assertRaises(ValueError):
                m.geometry(name)


class ResidencyTests(unittest.TestCase):
    def test_crossover_batch_matches_the_case_study(self):
        split = m.residency_split("qwen3-8b", 8192, 1)
        self.assertEqual(split["kv_read_bytes_per_sequence_step"], 1_207_959_552)
        self.assertAlmostEqual(float(value(split["crossover_batch_exact"])), 12.53, places=2)
        self.assertEqual(split["crossover_batch_first_integer"], 13)

    def test_memory_service_speedup_matches_the_case_study(self):
        for batch, expected in ((1, 13.53), (16, 1.78)):
            split = m.residency_split("qwen3-8b", 8192, batch)
            self.assertAlmostEqual(float(value(split["memory_service_speedup"])), expected, places=2)

    def test_a_longer_context_moves_the_crossover_as_the_case_study_says(self):
        split = m.residency_split("qwen3-8b", 32768, 1)
        self.assertAlmostEqual(float(value(split["crossover_batch_exact"])), 3.13, places=2)

    def test_the_speedup_is_exactly_one_plus_the_weight_to_state_ratio(self):
        split = m.residency_split("qwen3-8b", 8192, 4)
        expected = 1 + Fraction(split["active_weight_read_bytes"],
                                4 * split["kv_read_bytes_per_sequence_step"])
        self.assertEqual(value(split["memory_service_speedup"]), expected)

    def test_rejects_a_nonpositive_context_or_batch(self):
        for args in ((0, 1), (8192, 0), (-1, 1)):
            with self.assertRaises(ValueError):
                m.residency_split("qwen3-8b", *args)


class SupplyTests(unittest.TestCase):
    def test_bandwidth_stacks_and_area_match_the_case_study(self):
        result = m.calculate()
        supply = result["supply_backsolve"]
        self.assertEqual(supply["kv_read_bandwidth_bytes_per_second"], 12_079_595_520_000)
        self.assertEqual(supply["stacks_required"], 11)
        self.assertAlmostEqual(float(value(supply["session_state_area_mm2"])), 401, places=0)

    def test_lane_counts_match_the_case_study(self):
        supply = m.calculate()["supply_backsolve"]
        self.assertEqual(supply["ideal_lanes"], 75_674)
        self.assertEqual(supply["derated_lanes"], 315_306)

    def test_lane_counts_are_ceilings_not_roundings(self):
        supply = m.calculate()["supply_backsolve"]
        operations = supply["tensor_operations"]
        # 2e9 ops/s per lane over 100us is 2e5 operations per lane.
        self.assertEqual(supply["ideal_lanes"], math.ceil(operations / 200_000))

    def test_rejects_impossible_shares(self):
        for kwargs in ({"arithmetic_budget_share": "1.5"}, {"lane_utilisation": "2"},
                       {"token_budget_seconds": "0"}, {"tokens_per_second": 0}):
            with self.assertRaises(ValueError):
                m.calculate(**kwargs)


class FanTests(unittest.TestCase):
    def test_column_and_row_shards_move_the_same_total_but_in_opposite_directions(self):
        result = m.calculate()
        column, row = result["fan_traffic"]["column"], result["fan_traffic"]["row"]
        self.assertEqual(column["fan_out_bytes_per_layer"], row["fan_in_bytes_per_layer"])
        self.assertEqual(column["fan_in_bytes_per_layer"], row["fan_out_bytes_per_layer"])
        self.assertEqual(column["reduction_rounds_per_layer"], 0)
        self.assertGreater(row["reduction_rounds_per_layer"], 0)

    def test_tiles_and_mesh_follow_from_the_layer_bytes(self):
        shape = m.geometry("qwen3-8b")
        for tile in (16 * 1024 ** 2, 64 * 1024 ** 2, 256 * 1024 ** 2):
            row = m.fanout_fanin("qwen3-8b", tile, "column", "1e-7")
            self.assertEqual(row["tiles_per_layer"], math.ceil(shape["layer_bytes"] / tile))
            self.assertEqual(row["mesh_side"], math.ceil(math.sqrt(row["tiles_per_layer"])))
            self.assertEqual(row["mesh_diameter_hops"], 2 * (row["mesh_side"] - 1))
            self.assertEqual(row["spanning_tree_hops_per_collective"], row["tiles_per_layer"] - 1)

    def test_smaller_tiles_cost_more_hops(self):
        big = m.fanout_fanin("qwen3-8b", 256 * 1024 ** 2, "column", "1e-7")
        small = m.fanout_fanin("qwen3-8b", 4 * 1024 ** 2, "column", "1e-7")
        self.assertGreater(small["tiles_per_layer"], big["tiles_per_layer"])
        self.assertGreater(small["total_hops_per_token"], big["total_hops_per_token"])
        self.assertGreaterEqual(small["critical_path_hops_per_token"], big["critical_path_hops_per_token"])

    def test_rejects_an_unknown_sharding(self):
        with self.assertRaises(ValueError):
            m.fanout_fanin("qwen3-8b", 1024, "diagonal", "1e-7")


class SpanTests(unittest.TestCase):
    def test_budget_per_collective_follows_from_the_real_layer_count(self):
        span = m.calculate()["synchronisation_span"]
        config = model_config("qwen3-8b")
        self.assertEqual(span["collective_events_per_token"], config["num_hidden_layers"] * 2)
        # 100us x 30% over 72 events.
        self.assertEqual(value(span["budget_per_collective_seconds"]),
                         Fraction("0.0001") * Fraction("0.3") / span["collective_events_per_token"])

    def test_the_diameter_thresholds_are_exact(self):
        span = m.calculate()["synchronisation_span"]
        events = span["collective_events_per_token"]
        hop = Fraction("1e-7")
        self.assertEqual(span["largest_diameter_within_token_budget"],
                         int(Fraction("0.0001") / (events * hop)))
        self.assertEqual(span["largest_diameter_within_per_collective_budget"],
                         int(value(span["budget_per_collective_seconds"]) / hop))

    def test_the_scan_brackets_where_propagation_alone_fails(self):
        scan = {row["diameter_hops"]: row for row in m.calculate()["diameter_scan"]}
        largest = m.calculate()["synchronisation_span"]["largest_diameter_within_token_budget"]
        self.assertTrue(scan[largest]["fits_token_budget"])
        self.assertFalse(scan[largest + 1]["fits_token_budget"])
        # The case study's 15-hop mesh is on the failing side.
        self.assertFalse(scan[15]["fits_token_budget"])
        self.assertGreater(float(value(scan[15]["overrun_factor_against_token_budget"])), 1)

    def test_an_explicit_diameter_overrides_the_derived_mesh(self):
        result = m.calculate(diameter_hops=15)
        self.assertEqual(result["diameter_hops_used"], 15)
        self.assertNotEqual(result["diameter_hops_derived_from_mesh"], 15)
        self.assertFalse(result["synchronisation_span"]["fits_token_budget"])


class OutputTests(unittest.TestCase):
    def test_omitted_constraints_are_stated(self):
        result = m.calculate()
        self.assertGreaterEqual(len(result["omitted_constraints"]), 5)
        joined = " ".join(result["omitted_constraints"])
        for topic in ("KV writes", "contention", "silicon"):
            self.assertIn(topic, joined)

    def test_result_is_json_serialisable(self):
        text = json.dumps(m.calculate(), ensure_ascii=False, allow_nan=False)
        self.assertIn("weight-resident-remaining-traffic", text)

    def test_markdown_reports_the_thresholds_and_the_omissions(self):
        text = m.markdown(m.calculate())
        self.assertIn("供给倒推", text)
        self.assertIn("明确未计入的约束", text)
        self.assertIn("预算允许的最大直径", text)


if __name__ == "__main__":
    unittest.main()
