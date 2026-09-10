"""Independent checks for the two-sided iso-resource comparison (C74)."""
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
from infra_calc.topics import iso_resource_comparison as m
from infra_calc import hardware


def value(entry):
    return Fraction(**entry)


class PublishedRateTests(unittest.TestCase):
    def test_a_precision_without_a_published_rate_is_refused(self):
        a100 = hardware.select_device("a100-80gb-sxm")
        self.assertIsNone(m.published_peak(a100, "FP8"))
        self.assertIsNotNone(m.published_peak(a100, "BF16"))
        h100 = hardware.select_device("h100-sxm")
        self.assertIsNotNone(m.published_peak(h100, "FP8"))

    def test_the_refusal_reaches_the_candidate_list_with_its_reason(self):
        result = m.calculate()
        refused = result["right"]["refused"]
        self.assertTrue(refused)
        for row in refused:
            self.assertIn("publishes no dense FP8", row["reason"])
        self.assertEqual(result["right"]["admissible"],
                         ["BF16/tp1", "BF16/tp2", "BF16/tp4", "BF16/tp8"])

    def test_a_published_rate_carries_its_locator(self):
        result = m.calculate()
        row = result["left"]["lowest_latency"]
        self.assertIn("source_id", row["peak"])
        self.assertTrue(row["peak"]["locator"])


class CapacityAndPowerTests(unittest.TestCase):
    def test_replicas_come_from_the_shared_power_cap(self):
        result = m.calculate(power_cap_watts=5600)
        rows = {(row["precision"], row["tensor_parallel"]): row
                for row in result["left"]["candidates"] if row["admissible"]}
        for (_, tp), row in rows.items():
            self.assertEqual(row["replicas"], 5600 // (tp * 700))
            self.assertEqual(row["devices"], tp * row["replicas"])

    def test_a_cap_too_small_for_one_replica_refuses_the_candidate(self):
        result = m.calculate(power_cap_watts=700)
        refused = {row["candidate"]: row["reason"] for row in result["left"]["refused"]}
        self.assertIn("BF16/tp2", refused)
        self.assertIn("1400 W", refused["BF16/tp2"])
        self.assertIn("BF16/tp1", result["left"]["admissible"])

    def test_state_shards_by_key_value_head_not_by_rank(self):
        result = m.calculate()
        rows = {row["tensor_parallel"]: row for row in result["left"]["candidates"]
                if row["admissible"] and row["precision"] == "BF16"}
        for tp in (1, 2, 4, 8):
            self.assertEqual(rows[tp]["state_shards"], min(tp, 8))

    def test_capacity_refusal_states_the_shortfall(self):
        result = m.calculate(batch=512, context=32768)
        reasons = [row["reason"] for row in result["right"]["refused"]]
        self.assertTrue(any("per device against" in reason for reason in reasons))


class QualityTests(unittest.TestCase):
    def test_a_narrower_width_is_set_aside_without_evidence(self):
        result = m.calculate()
        self.assertEqual(sorted(result["left"]["excluded_for_quality"]),
                         ["FP8/tp1", "FP8/tp2", "FP8/tp4", "FP8/tp8"])
        for name in ("lowest_latency", "lowest_cost_per_token"):
            self.assertEqual(result["left"][name]["precision"], "BF16")

    def test_declaring_evidence_lets_the_narrower_width_be_ranked(self):
        result = m.calculate(quality_evidence={"BF16": True, "FP8": True})
        self.assertEqual(result["left"]["excluded_for_quality"], [])
        self.assertEqual(result["left"]["lowest_latency"]["precision"], "FP8")

    def test_the_baseline_width_must_have_evidence(self):
        with self.assertRaises(ValueError):
            m.calculate(quality_evidence={"BF16": False})

    def test_only_the_evidence_moves_when_an_objective_flips(self):
        result = m.calculate()
        flips = result["objectives_that_flip_on_quality_evidence"]
        self.assertTrue(flips)
        for row in flips:
            self.assertEqual(row["precision_granted_evidence"], "FP8")
            self.assertNotEqual(row["winner_without_evidence"], row["winner_with_evidence"])
        # The hardware inputs are untouched between the two runs.
        granted = m.calculate(quality_evidence={"BF16": True, "FP8": True})
        self.assertEqual(result["inputs"]["power_cap_watts"], granted["inputs"]["power_cap_watts"])
        self.assertEqual(result["fixed_configuration_comparison"]["cheaper_side"],
                         granted["fixed_configuration_comparison"]["cheaper_side"])


class ComparisonTests(unittest.TestCase):
    def test_the_fixed_pair_uses_one_configuration_on_both_sides(self):
        result = m.calculate(fixed_precision="BF16", fixed_tensor_parallel=1)
        rows = result["fixed_configuration_comparison"]["rows"]
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertEqual(row["precision"], "BF16")
            self.assertEqual(row["tensor_parallel"], 1)

    def test_each_objective_names_a_winner_and_a_ratio(self):
        result = m.calculate()
        objectives = {row["objective"] for row in result["head_to_head"]}
        self.assertEqual(objectives, {"lowest_latency", "highest_throughput_within_slo",
                                      "lowest_cost_per_token"})
        for row in result["head_to_head"]:
            self.assertIsNotNone(row["winner"])
            self.assertGreaterEqual(float(value(row["ratio"])), 1)

    def test_the_winner_really_is_the_better_value(self):
        result = m.calculate()
        sides = {result["left"]["device"]: result["left"], result["right"]["device"]: result["right"]}
        for row in result["head_to_head"]:
            key = {"lowest_latency": "latency_seconds",
                   "highest_throughput_within_slo": "throughput_tokens_per_second",
                   "lowest_cost_per_token": "cost_per_token"}[row["objective"]]
            winner = value(sides[row["winner"]][row["objective"]][key])
            loser = value(sides[row["loser"]][row["objective"]][key])
            if row["objective"] == "highest_throughput_within_slo":
                self.assertGreaterEqual(winner, loser)
            else:
                self.assertLessEqual(winner, loser)

    def test_price_flip_is_the_ratio_of_the_two_best_costs(self):
        result = m.calculate()
        flip = result["price_flip"]
        left = value(result["left"]["lowest_cost_per_token"]["cost_per_token"])
        right = value(result["right"]["lowest_cost_per_token"]["cost_per_token"])
        self.assertEqual(value(flip["ratio"]), max(left, right) / min(left, right))
        self.assertEqual(flip["cheaper_side"],
                         result["left"]["device"] if left < right else result["right"]["device"])

    def test_raising_the_cheaper_price_past_the_flip_changes_the_winner(self):
        result = m.calculate()
        flip = result["price_flip"]
        ratio = float(value(flip["ratio"]))
        base = {"h100-sxm": "3.0", "a100-80gb-sxm": "1.5"}
        raised = dict(base)
        raised[flip["cheaper_side"]] = str(float(base[flip["cheaper_side"]]) * ratio * 1.01)
        after = m.calculate(left_price_per_device_hour=raised["h100-sxm"],
                            right_price_per_device_hour=raised["a100-80gb-sxm"])
        self.assertEqual(after["price_flip"]["cheaper_side"], flip["dearer_side"])

    def test_an_slo_nobody_meets_leaves_the_throughput_objective_open(self):
        result = m.calculate(slo_seconds="0.000001")
        self.assertFalse(result["left"]["meets_slo"])
        self.assertFalse(result["right"]["meets_slo"])
        row = next(entry for entry in result["head_to_head"]
                   if entry["objective"] == "highest_throughput_within_slo")
        self.assertIsNone(row["winner"])


class InputTests(unittest.TestCase):
    def test_rejects_bad_inputs(self):
        for kwargs in ({"batch": 0}, {"context": 0}, {"power_cap_watts": 0},
                       {"slo_seconds": "0"}, {"fixed_precision": "INT4"},
                       {"fixed_tensor_parallel": 3},
                       {"left_price_per_device_hour": "-1"}):
            with self.assertRaises(ValueError):
                m.calculate(**kwargs)


class OutputTests(unittest.TestCase):
    def test_result_is_json_serialisable(self):
        text = json.dumps(m.calculate(), ensure_ascii=False, allow_nan=False)
        self.assertIn("iso-resource-two-sided-comparison", text)

    def test_markdown_separates_the_fixed_pair_from_the_tuned_sides(self):
        text = m.markdown(m.calculate())
        self.assertIn("先比较两套固定配置", text)
        self.assertIn("再让两侧各自调优", text)
        self.assertIn("仅因质量证据而翻转的目标", text)
        self.assertIn("翻转条件", text)


if __name__ == "__main__":
    unittest.main()
