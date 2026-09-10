"""Independent checks for the specialisation payback account (C75).

The planned case is the OpenTallas case study's own worked example, so these
tests check the module against the case rather than against itself.
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
from infra_calc.topics import specialization_payback as m


def value(entry):
    return Fraction(**entry)


class WorkedExampleTests(unittest.TestCase):
    def test_payback_volume_matches_the_case_study(self):
        # 20,000,000 / (0.50 / 1e6) = 40 trillion tokens.
        self.assertEqual(m.payback_volume("20000000", "0.50"), Fraction(40) * 10 ** 12)

    def test_annual_effective_output_matches_the_case_study(self):
        # 100 x 10,000 x 0.50 x 31,536,000 = 15.768 trillion tokens.
        got = m.effective_output(100, 10000, "0.5", Fraction(m.SECONDS_PER_YEAR))
        self.assertEqual(got, Fraction(15768) * 10 ** 9)

    def test_machines_required_matches_the_case_study(self):
        planned = m.calculate(include_site=False)["scenarios"][0]
        self.assertEqual(planned["machines_required"], 254)
        self.assertFalse(planned["pays_back"])
        self.assertEqual(planned["machine_shortfall"], 154)

    def test_coverage_is_delivered_over_required(self):
        planned = m.calculate(include_site=False)["scenarios"][0]
        self.assertEqual(value(planned["coverage"]),
                         value(planned["delivered_tokens"]) / value(planned["required_tokens"]))
        self.assertAlmostEqual(float(value(planned["coverage"])), 0.3942, places=4)

    def test_machines_required_is_a_ceiling(self):
        planned = m.calculate(include_site=False)["scenarios"][0]
        per_machine = value(planned["delivered_tokens"]) / planned["machines"]
        needed = value(planned["required_tokens"]) / per_machine
        self.assertEqual(planned["machines_required"], -(-needed.numerator // needed.denominator))


class RiskTests(unittest.TestCase):
    def test_halving_the_life_doubles_the_machines_needed(self):
        rows = {row["scenario"]: row for row in m.calculate(include_site=False)["scenarios"]}
        self.assertEqual(rows["life_halves"]["machines_required"],
                         2 * rows["planned"]["machines_required"])

    def test_delivery_is_taken_out_of_the_life_not_added_to_it(self):
        rows = {row["scenario"]: row for row in m.calculate(include_site=False)["scenarios"]}
        planned, slipped = rows["planned"], rows["delivery_slips"]
        self.assertLess(value(slipped["serving_seconds"]), value(planned["serving_seconds"]))
        self.assertEqual(value(slipped["serving_seconds"]),
                         value(planned["serving_seconds"]) - 26 * m.SECONDS_PER_WEEK)

    def test_a_delivery_that_consumes_the_whole_life_serves_nothing(self):
        result = m.calculate(delayed_delivery_weeks=60)
        slipped = {row["scenario"]: row for row in result["scenarios"]}["delivery_slips"]
        self.assertFalse(slipped["pays_back"])
        self.assertIn("nothing is served", slipped["reason"])
        self.assertNotIn("required_tokens", slipped)

    def test_a_lower_output_rate_scales_the_machines_needed(self):
        rows = {row["scenario"]: row for row in m.calculate(include_site=False)["scenarios"]}
        planned, degraded = rows["planned"], rows["output_rate_falls"]
        self.assertEqual(degraded["tokens_per_second"], 6000)
        # 10000/6000 of the machines, rounded up.
        self.assertEqual(degraded["machines_required"], 423)

    def test_enough_machines_do_pay_it_back(self):
        result = m.calculate(machines=254, include_site=False)
        planned = result["scenarios"][0]
        self.assertTrue(planned["pays_back"])
        self.assertEqual(planned["machine_shortfall"], 0)
        self.assertIn("planned", result["pays_back_anywhere"])


class SiteTests(unittest.TestCase):
    def test_cooling_multiplies_electricity_only(self):
        site = m.site_cost(100, "10", "1.3", "0.08", "250000", "150000",
                           Fraction(m.SECONDS_PER_YEAR))
        self.assertEqual(value(site["facility_power_kw"]), Fraction(100 * 10) * Fraction("1.3"))
        self.assertEqual(value(site["energy_kwh"]),
                         value(site["facility_power_kw"]) * Fraction(m.SECONDS_PER_YEAR, 3600))
        self.assertEqual(value(site["electricity_cost"]),
                         value(site["energy_kwh"]) * Fraction("0.08"))
        # Network and backup are annual lines, untouched by the overhead.
        self.assertEqual(value(site["network_cost"]), Fraction("250000"))
        self.assertEqual(value(site["backup_cost"]), Fraction("150000"))
        self.assertEqual(value(site["total_site_cost"]),
                         value(site["electricity_cost"]) + Fraction("400000"))

    def test_site_cost_eats_part_of_the_claimed_saving(self):
        planned = m.calculate()["scenarios"][0]
        gross = Fraction("0.50")
        self.assertEqual(value(planned["net_saving_per_million_tokens"]),
                         gross - value(planned["site_cost_per_million_tokens"]))
        self.assertLess(value(planned["net_saving_per_million_tokens"]), gross)
        self.assertTrue(planned["saving_survives_site_cost"])

    def test_a_lower_output_rate_raises_the_site_cost_per_token(self):
        rows = {row["scenario"]: row for row in m.calculate()["scenarios"]}
        self.assertGreater(value(rows["output_rate_falls"]["site_cost_per_million_tokens"]),
                           value(rows["planned"]["site_cost_per_million_tokens"]))

    def test_a_site_cost_above_the_saving_removes_the_payback_entirely(self):
        result = m.calculate(electricity_price_per_kwh="10")
        planned = result["scenarios"][0]
        self.assertFalse(planned["saving_survives_site_cost"])
        self.assertIsNone(planned["required_tokens_net_of_site"])
        self.assertFalse(planned["pays_back_net_of_site"])

    def test_rejects_impossible_site_inputs(self):
        for kwargs in ({"cooling_overhead": "0.9"}, {"machine_power_kw": "0"},
                       {"electricity_price_per_kwh": "-1"}):
            with self.assertRaises(ValueError):
                m.calculate(**kwargs)


class InputTests(unittest.TestCase):
    def test_rejects_a_nonpositive_saving_or_negative_fixed_cost(self):
        with self.assertRaises(ValueError):
            m.payback_volume("20000000", "0")
        with self.assertRaises(ValueError):
            m.payback_volume("-1", "0.50")

    def test_rejects_an_impossible_utilisation(self):
        for share in ("0", "1.5", "-0.2"):
            with self.assertRaises(ValueError):
                m.calculate(utilisation=share)

    def test_rejects_a_shortened_life_longer_than_the_planned_one(self):
        with self.assertRaises(ValueError):
            m.calculate(economic_life_months=6, shortened_life_months=12)


class OutputTests(unittest.TestCase):
    def test_result_is_json_serialisable(self):
        text = json.dumps(m.calculate(), ensure_ascii=False, allow_nan=False)
        self.assertIn("specialisation-payback", text)

    def test_markdown_keeps_the_demand_caveat(self):
        text = m.markdown(m.calculate())
        self.assertIn("整站费用与净节省", text)
        self.assertIn("真实需求", text)
        self.assertIn("教学假设", text)


if __name__ == "__main__":
    unittest.main()
