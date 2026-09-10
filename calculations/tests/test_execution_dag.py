"""Independent checks for the execution DAG and candidate screening (C72)."""
import json
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
from infra_calc.topics import execution_dag as m
from infra_calc.topics import stage_resource_bounds
from infra_calc.sources import model_config


def value(entry):
    return Fraction(**entry)


class GraphTests(unittest.TestCase):
    def test_the_chain_visits_every_stage_once(self):
        result = m.calculate()
        path = result["baseline_graph"]["critical_path"]
        self.assertEqual(len(path), result["baseline_graph"]["node_count"])
        self.assertEqual(len(set(path)), len(path))
        config = model_config("qwen3-8b")
        # input, every layer, and the output head.
        self.assertEqual(len(path), config["num_hidden_layers"] + 2)

    def test_the_bound_is_the_sum_of_the_serial_node_bounds(self):
        result = m.calculate()
        total = sum(max(1, round(node["bound_seconds"] * 10 ** 9)) for node in result["nodes"])
        self.assertEqual(value(result["baseline_graph"]["bound_seconds"]),
                         Fraction(total, 10 ** 9))

    def test_unpublished_rates_stay_listed_and_are_never_filled_in(self):
        result = m.calculate()
        self.assertTrue(result["coverage_gaps"])
        for name in result["coverage_gaps"]:
            self.assertTrue(name.startswith("special:"), name)
        # No node claims a special resource contributed to its bound.
        for node in result["nodes"]:
            for name in node["resources_without_a_published_rate"]:
                self.assertNotIn(name, node["resource_seconds"])

    def test_a_cycle_is_rejected(self):
        with self.assertRaises(ValueError):
            m.request_dag.schedule([{"id": "a", "deps": ["b"], "duration_ns": 1, "resource": None},
                                    {"id": "b", "deps": ["a"], "duration_ns": 1, "resource": None}])


class CapacityTests(unittest.TestCase):
    def test_the_split_matches_the_official_geometry_and_parameter_count(self):
        bounds = stage_resource_bounds.calculate(model="qwen3-8b", tokens=128, history=4096)
        split = m.split_capacity(bounds, "qwen3-8b")
        config = model_config("qwen3-8b")
        unit = 2 * 2 * config["num_hidden_layers"] * config["num_key_value_heads"] * config["head_dim"]
        self.assertEqual(split["positions"], 4224)
        self.assertEqual(split["kv_bytes"], unit * 4224)
        self.assertEqual(split["weight_bytes"] + split["kv_bytes"],
                         bounds["capacity"]["comparison_bytes"])
        # Weights at BF16 are two bytes per parameter, so this must be an even count.
        self.assertEqual(split["weight_bytes"] % 2, 0)

    def test_narrowing_the_state_only_moves_the_state_term(self):
        result = m.calculate(state_bits=8)
        rows = {row["action"]: row for row in result["candidates"]}
        split = rows["baseline"]["capacity_split"]
        self.assertEqual(rows["compress_state"]["capacity_bytes"],
                         split["weight_bytes"] + split["kv_bytes"] // 2)
        self.assertEqual(rows["baseline"]["capacity_bytes"],
                         split["weight_bytes"] + split["kv_bytes"])

    def test_batching_scales_only_the_state(self):
        result = m.calculate(batch=1)
        rows = {row["action"]: row for row in result["candidates"]}
        base, batched = rows["baseline"], rows["batch"]
        self.assertEqual(batched["call"]["batch"], 8)
        self.assertEqual(batched["capacity_bytes"] - base["capacity_bytes"],
                         7 * base["capacity_split"]["kv_bytes_per_request"])


class CandidateTests(unittest.TestCase):
    def test_every_rewrite_states_what_it_adds(self):
        result = m.calculate()
        for row in result["candidates"]:
            if row["action"] == "baseline":
                continue
            self.assertTrue(row["added_cost"], row["action"])
            self.assertTrue(row["note"], row["action"])

    def test_caching_a_prefix_needs_a_prefix(self):
        with self.assertRaises(ValueError):
            m.calculate(history=0)

    def test_disaggregation_moves_the_whole_session_state(self):
        result = m.calculate()
        rows = {row["action"]: row for row in result["candidates"]}
        transfer = rows["disaggregate"]["state_transfer"]
        self.assertEqual(transfer["bytes"], rows["baseline"]["capacity_split"]["kv_bytes"])
        self.assertEqual(rows["disaggregate"]["devices"], 2)
        # It can only be slower than the same work without the transfer.
        self.assertGreater(value(rows["disaggregate"]["graph"]["bound_seconds"]),
                           value(rows["baseline"]["graph"]["bound_seconds"]))

    def test_caching_a_prefix_lowers_the_bound(self):
        result = m.calculate()
        rows = {row["action"]: row for row in result["candidates"]}
        self.assertLess(value(rows["cache_prefix"]["graph"]["bound_seconds"]),
                        value(rows["baseline"]["graph"]["bound_seconds"]))
        self.assertEqual(rows["cache_prefix"]["call"]["tokens"], 1)


class ScreeningTests(unittest.TestCase):
    def test_caps_exclude_before_objectives_are_compared(self):
        result = m.calculate(power_cap_watts=700)
        excluded = [row["action"] for row in result["screening"]["excluded_by_caps"]]
        self.assertIn("disaggregate", excluded)
        self.assertNotIn("disaggregate", result["screening"]["pareto_front"])
        self.assertNotIn("disaggregate", [row["action"] for row in result["screening"]["dominated"]])

    def test_an_area_cap_only_applies_when_a_footprint_is_declared(self):
        without = m.calculate(area_cap_mm2=100)
        self.assertIn("not screened", without["area_status"])
        self.assertEqual(without["screening"]["excluded_by_caps"], [])
        with_area = m.calculate(area_cap_mm2=1000, area_mm2_per_device=814)
        excluded = [row["action"] for row in with_area["screening"]["excluded_by_caps"]]
        self.assertIn("disaggregate", excluded)

    def test_a_dominated_candidate_names_what_beats_it(self):
        result = m.calculate()
        dominated = {row["action"]: row["dominated_by"] for row in result["screening"]["dominated"]}
        self.assertIn("disaggregate", dominated)
        self.assertTrue(dominated["disaggregate"])
        for name in dominated["disaggregate"]:
            self.assertIn(name, result["screening"]["pareto_front"])

    def test_domination_is_never_claimed_between_front_members(self):
        result = m.calculate()
        scored = {row["action"]: row for row in result["screening"]["scored"]}
        front = result["screening"]["pareto_front"]
        for left in front:
            for right in front:
                if left == right:
                    continue
                a, b = scored[left], scored[right]
                strictly_better_everywhere = (
                    value(b["latency_bound_seconds"]) <= value(a["latency_bound_seconds"])
                    and value(b["throughput_tokens_per_second"]) >= value(a["throughput_tokens_per_second"])
                    and value(b["cost_per_token"]) <= value(a["cost_per_token"]))
                self.assertFalse(strictly_better_everywhere and (
                    value(b["latency_bound_seconds"]) < value(a["latency_bound_seconds"])
                    or value(b["throughput_tokens_per_second"]) > value(a["throughput_tokens_per_second"])
                    or value(b["cost_per_token"]) < value(a["cost_per_token"])),
                    f"{right} dominates {left} but both are on the front")

    def test_single_objective_winners_agree_with_the_scored_rows(self):
        result = m.calculate()
        screening = result["screening"]
        rows = [row for row in screening["scored"] if row["admissible"]]
        self.assertEqual(screening["lowest_latency"],
                         min(rows, key=lambda row: value(row["latency_bound_seconds"]))["action"])
        self.assertEqual(screening["highest_throughput"],
                         max(rows, key=lambda row: value(row["throughput_tokens_per_second"]))["action"])
        self.assertEqual(screening["lowest_cost_per_token"],
                         min(rows, key=lambda row: value(row["cost_per_token"]))["action"])

    def test_cost_is_device_time_at_the_declared_price(self):
        result = m.calculate(price_per_device_hour="3.0")
        rows = {row["action"]: row for row in result["screening"]["scored"]}
        for row in rows.values():
            expected = value(row["latency_bound_seconds"]) * row["devices"] * Fraction("3.0") / 3600
            self.assertEqual(value(row["cost_per_call"]), expected)

    def test_rejects_bad_inputs(self):
        for kwargs in ({"tokens": 0}, {"batch": 0}, {"power_cap_watts": 0},
                       {"price_per_device_hour": "-1"}, {"actions": ("cache_prefix",)},
                       {"actions": ("baseline", "teleport")}, {"state_bits": 4}):
            with self.assertRaises(ValueError):
                m.calculate(**kwargs)


class OutputTests(unittest.TestCase):
    def test_result_is_json_serialisable(self):
        text = json.dumps(m.calculate(), ensure_ascii=False, allow_nan=False)
        self.assertIn("execution-dag-screening", text)

    def test_markdown_reports_the_gaps_and_the_front(self):
        text = m.markdown(m.calculate())
        self.assertIn("帕累托前沿", text)
        self.assertIn("未公布速率", text)
        self.assertIn("上限先于目标", text)


if __name__ == "__main__":
    unittest.main()
