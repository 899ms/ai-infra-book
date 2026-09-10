"""Independent checks for the uncertainty and design-record pass (C76).

The payback decision is used throughout because it evaluates instantly; the
graph decision is exercised once, in its own slower test.
"""
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
from infra_calc.topics import design_record as m
from infra_calc.topics import specialization_payback


def value(entry):
    return Fraction(**entry)


PAYBACK = ("specialisation_payback",)


class OutcomeTests(unittest.TestCase):
    def test_the_outcome_reads_the_named_scenario(self):
        planned = m.payback_outcome()
        halved = m.payback_outcome(scenario="life_halves")
        self.assertEqual(planned["label"], "does_not_pay_back")
        self.assertLess(halved["margin"], planned["margin"])

    def test_an_unknown_scenario_is_refused(self):
        with self.assertRaises(ValueError):
            m.payback_outcome(scenario="wishful_thinking")

    def test_the_margin_is_the_coverage_the_other_topic_reports(self):
        expected = specialization_payback.calculate()["scenarios"][0]["coverage"]
        self.assertEqual(m.payback_outcome()["margin"], value(expected))


class ScanTests(unittest.TestCase):
    def test_each_input_is_moved_alone(self):
        result = m.calculate(decisions=PAYBACK)
        scan = result["decisions"][0]["scan"]
        self.assertEqual(scan["baseline"]["label"], "does_not_pay_back")
        names = [row["input"] for row in scan["inputs"]]
        self.assertEqual(sorted(names), sorted(m.DECISIONS["specialisation_payback"]["uncertain_inputs"]))
        for row in scan["inputs"]:
            self.assertEqual(row["points"]["nominal"]["label"], scan["baseline"]["label"])

    def test_no_declared_interval_reverses_this_decision(self):
        scan = m.calculate(decisions=PAYBACK)["decisions"][0]["scan"]
        for row in scan["inputs"]:
            self.assertFalse(row["changes_the_decision_within_its_interval"], row["input"])

    def test_margin_swing_is_the_spread_over_the_three_points(self):
        scan = m.calculate(decisions=PAYBACK)["decisions"][0]["scan"]
        for row in scan["inputs"]:
            margins = [value(row["points"][end]["margin"]) for end in ("low", "nominal", "high")]
            self.assertEqual(value(row["margin_swing"]), max(margins) - min(margins))

    def test_an_input_with_no_effect_has_no_swing(self):
        scan = m.calculate(decisions=PAYBACK)["decisions"][0]["scan"]
        rows = {row["input"]: row for row in scan["inputs"]}
        # Electricity price does not enter the gross coverage at all.
        self.assertEqual(value(rows["electricity_price_per_kwh"]["margin_swing"]), 0)
        self.assertGreater(value(rows["saving_per_million_tokens"]["margin_swing"]), 0)


class FlipTests(unittest.TestCase):
    def test_the_machine_bracket_rediscovers_the_case_study_answer(self):
        ranked = m.calculate(decisions=PAYBACK)["decisions"][0]["value_of_information"]
        rows = {row["input"]: row for row in ranked}
        bracket = rows["machines"]["flip"]["bracket"]
        low, high = value(bracket[0]), value(bracket[1])
        # The case study needs 254 machines; the search must bracket that.
        self.assertLessEqual(low, 254)
        self.assertGreaterEqual(high, 253)
        self.assertEqual(rows["machines"]["flip"]["direction"], "above")

    def test_a_flip_bracket_really_straddles_the_change(self):
        ranked = m.calculate(decisions=PAYBACK)["decisions"][0]["value_of_information"]
        decision = m.DECISIONS["specialisation_payback"]
        baseline = m.evaluate(decision, {})["label"]
        for row in ranked:
            flip = row["flip"]
            if flip["bracket"] is None:
                continue
            spec = decision["uncertain_inputs"][row["input"]]
            cast = int if spec.get("integer") else str
            inside = m.evaluate(decision, {row["input"]: cast(value(flip["bracket"][0]))})["label"]
            outside = m.evaluate(decision, {row["input"]: cast(value(flip["bracket"][1]))})["label"]
            if flip["direction"] == "above":
                self.assertEqual(inside, baseline, row["input"])
                self.assertEqual(outside, flip["outside_label"], row["input"])

    def test_an_input_that_cannot_flip_it_says_so(self):
        ranked = m.calculate(decisions=PAYBACK)["decisions"][0]["value_of_information"]
        rows = {row["input"]: row for row in ranked}
        # Utilisation is capped at one, so it cannot be raised into a payback.
        self.assertIsNone(rows["utilisation"]["flip"]["direction"])
        self.assertIn("never changes the decision", rows["utilisation"]["flip"]["reason"])

    def test_ranking_puts_decisive_inputs_first(self):
        ranked = m.calculate(decisions=PAYBACK)["decisions"][0]["value_of_information"]
        self.assertEqual([row["rank"] for row in ranked], sorted(row["rank"] for row in ranked))
        for row in ranked:
            self.assertIn(row["rank"], (0, 1, 2, 3))


class RecordTests(unittest.TestCase):
    def test_every_required_field_is_filled(self):
        record = m.calculate(decisions=PAYBACK)["decisions"][0]["record"]
        for field in ("candidates", "first_prediction", "evidence_kinds", "observation",
                      "revised_decision", "next_limit", "flip_condition",
                      "minimum_measurement", "held_out_predictions"):
            self.assertIn(field, record)
            self.assertIsNotNone(record[field], field)

    def test_no_recomputation_is_counted_as_a_measurement(self):
        record = m.calculate(decisions=PAYBACK)["decisions"][0]["record"]
        self.assertNotIn("measured", record["evidence_kinds"])
        self.assertIn("not an independent measurement", record["observation"])
        self.assertEqual(record["first_prediction"], record["revised_decision"])

    def test_the_minimum_measurement_admits_when_nothing_decides_it(self):
        record = m.calculate(decisions=PAYBACK)["decisions"][0]["record"]
        self.assertIn("No declared interval changes this decision", record["minimum_measurement"])

    def test_held_out_predictions_differ_by_configuration(self):
        record = m.calculate(decisions=PAYBACK)["decisions"][0]["record"]
        rows = {row["configuration"]: row for row in record["held_out_predictions"]}
        self.assertEqual(sorted(rows), ["life_halves", "output_rate_falls"])
        first = [value(x) for x in rows["life_halves"]["predicted_margin_interval"]]
        second = [value(x) for x in rows["output_rate_falls"]["predicted_margin_interval"]]
        self.assertNotEqual(first, second)
        for row in rows.values():
            low, high = (value(x) for x in row["predicted_margin_interval"])
            self.assertLessEqual(low, high)
            self.assertIn("falsified_if", row)

    def test_a_held_out_prediction_covers_its_own_nominal_case(self):
        decision = m.DECISIONS["specialisation_payback"]
        record = m.calculate(decisions=PAYBACK)["decisions"][0]["record"]
        for row in record["held_out_predictions"]:
            selector = next(entry["selector"] for entry in decision["held_out"]
                            if entry["name"] == row["configuration"])
            observed = m.evaluate(decision, dict(selector))
            low, high = (value(x) for x in row["predicted_margin_interval"])
            self.assertLessEqual(low, observed["margin"])
            self.assertLessEqual(observed["margin"], high)
            self.assertIn(observed["label"], row["predicted_labels"])


class GraphDecisionTests(unittest.TestCase):
    def test_the_graph_decision_reports_a_held_out_prediction(self):
        result = m.calculate(decisions=("execution_dag_screening",))
        entry = result["decisions"][0]
        self.assertEqual(entry["scan"]["baseline"]["label"], "batch")
        record = entry["record"]
        held = record["held_out_predictions"][0]
        self.assertEqual(held["configuration"], "disaggregate")
        # It is never predicted to win.
        self.assertNotIn("on_the_front", held["predicted_labels"])

    def test_an_expensive_input_is_scanned_but_not_searched(self):
        entry = m.calculate(decisions=("execution_dag_screening",))["decisions"][0]
        rows = {row["input"]: row for row in entry["value_of_information"]}
        self.assertFalse(rows["history"]["flip"]["searched"])
        self.assertIsNone(rows["history"]["flip"]["bracket"])
        self.assertIn("not searched", rows["history"]["verdict"])
        # It still appears in the endpoint scan with three evaluated points.
        scan = {row["input"]: row for row in entry["scan"]["inputs"]}
        self.assertEqual(sorted(scan["history"]["points"]), ["high", "low", "nominal"])


class InputTests(unittest.TestCase):
    def test_rejects_an_unknown_decision(self):
        for bad in ((), ("nonexistent",), ("specialisation_payback", "nonexistent")):
            with self.assertRaises(ValueError):
                m.calculate(decisions=bad)


class OutputTests(unittest.TestCase):
    def test_result_is_json_serialisable(self):
        text = json.dumps(m.calculate(decisions=PAYBACK), ensure_ascii=False, allow_nan=False)
        self.assertIn("design-record-uncertainty", text)

    def test_markdown_carries_the_record_fields(self):
        text = m.markdown(m.calculate(decisions=PAYBACK))
        for heading in ("最小补测", "翻转条件", "留出配置的可证伪预测", "证据类型"):
            self.assertIn(heading, text)


if __name__ == "__main__":
    unittest.main()
