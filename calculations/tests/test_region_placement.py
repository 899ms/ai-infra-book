"""Independent checks for cross-region placement (C71).

Byte counts and geometry are recomputed here from the raw trace and the official
config, not read back from the module's own result.
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
from infra_calc.topics import region_placement as m
from infra_calc.topics import agent_trace
from infra_calc.sources import model_config


def value(entry):
    return Fraction(**entry)


class GeometryTests(unittest.TestCase):
    def test_state_bytes_match_the_official_attention_geometry(self):
        config = model_config("qwen3-8b")
        expected = 2 * 2 * config["num_hidden_layers"] * config["num_key_value_heads"] * config["head_dim"]
        self.assertEqual(m.kv_bytes_per_token("qwen3-8b", 16), expected)
        self.assertEqual(m.kv_bytes_per_token("qwen3-8b", 8), expected // 2)

    def test_rejects_an_unsupported_state_width(self):
        for bits in (4, 32, 0):
            with self.assertRaises(ValueError):
                m.kv_bytes_per_token("qwen3-8b", bits)


class LedgerTests(unittest.TestCase):
    def test_payloads_are_the_traces_own_bytes(self):
        files, _ = agent_trace.read_trace("thinking-off")
        raw = files["rounds.jsonl"]
        result = m.calculate()
        previous = 0
        for record, entry in zip(raw, result["round_ledger"]):
            prefix = len(json.dumps(record["messages"], ensure_ascii=False).encode())
            self.assertEqual(entry["prefix_bytes"], prefix)
            self.assertEqual(entry["delta_bytes"], prefix - previous)
            self.assertEqual(entry["reply_bytes"], len(record["output_text"].encode()))
            previous = prefix

    def test_warm_carries_the_growth_and_stateless_carries_the_whole_prefix(self):
        result = m.calculate()
        ledger = result["round_ledger"]
        # The deltas must telescope to the final prefix.
        self.assertEqual(sum(entry["delta_bytes"] for entry in ledger), ledger[-1]["prefix_bytes"])
        stateless = next(row for row in result["session_costs"] if row["placement"] == "remote_stateless")
        warm = next(row for row in result["session_costs"] if row["placement"] == "remote_warm")
        local = next(row for row in result["session_costs"] if row["placement"] == "local")
        self.assertEqual(stateless["inbound_bytes"], sum(entry["prefix_bytes"] for entry in ledger))
        self.assertEqual(warm["inbound_bytes"], ledger[-1]["prefix_bytes"])
        self.assertLess(warm["inbound_bytes"], stateless["inbound_bytes"])
        self.assertEqual(local["inbound_bytes"], 0)
        self.assertEqual(local["outbound_bytes"], 0)

    def test_a_shrinking_prefix_is_rejected(self):
        files, _ = agent_trace.read_trace("thinking-off")
        rounds = m.calculate()["round_ledger"]
        broken = {"rounds.jsonl": [dict(row) for row in files["rounds.jsonl"]]}
        broken["rounds.jsonl"][3]["messages"] = broken["rounds.jsonl"][0]["messages"]
        accounted = agent_trace.calculate()["agent_rounds"]
        with self.assertRaises(ValueError):
            m.round_bytes(broken, accounted, 147456)
        self.assertEqual(len(rounds), len(accounted))


class FeasibilityTests(unittest.TestCase):
    def test_power_and_lead_time_gate_before_price(self):
        regions = m.region_inputs(None)
        gate = {row["region"]: row for row in m.feasibility(regions, 250, 12)}
        self.assertFalse(gate["far"]["feasible"])
        self.assertTrue(gate["near"]["feasible"])
        self.assertIn("30 weeks", " ".join(gate["far"]["reasons"]))
        capped = m.feasibility(regions, 500, 52)
        self.assertFalse(any(row["feasible"] for row in capped))

    def test_a_cheap_but_infeasible_site_never_ranks(self):
        result = m.calculate(deadline_weeks=12)
        self.assertNotIn("far/remote_warm", result["ranked_feasible"])
        self.assertIn("far/remote_warm", result["excluded_by_hard_constraints"])
        self.assertEqual(result["ranked_feasible"], ["near/local"])

    def test_deadline_scan_brackets_the_lead_time(self):
        result = m.calculate()
        rows = {row["deadline_weeks"]: row["feasible_regions"] for row in result["deadline_scan"]}
        self.assertEqual(rows[26], ["near"])
        self.assertEqual(sorted(rows[30]), ["far", "near"])

    def test_rejects_malformed_regions(self):
        with self.assertRaises(ValueError):
            m.region_inputs({})
        with self.assertRaises(ValueError):
            m.region_inputs({"near": dict(m.DEFAULT_REGIONS["near"])})
        broken = {name: dict(row) for name, row in m.DEFAULT_REGIONS.items()}
        broken["far"]["cooling_overhead"] = "0.8"
        with self.assertRaises(ValueError):
            m.region_inputs(broken)
        negative = {name: dict(row) for name, row in m.DEFAULT_REGIONS.items()}
        negative["far"]["egress_price_per_gb"] = "-0.01"
        with self.assertRaises(ValueError):
            m.region_inputs(negative)


class BreakEvenTests(unittest.TestCase):
    def test_hold_boundary_is_the_saving_divided_by_the_residency_rate(self):
        result = m.calculate()
        boundary = result["hold_boundary"]
        saving = value(boundary["saving_at_zero_hold"])
        rate = value(boundary["residency_cost_per_hour"])
        self.assertEqual(value(boundary["hold_hours"]), saving / rate)
        self.assertEqual(value(boundary["hold_seconds"]), saving / rate * 3600)
        # Independent recomputation of the residency rate from the peak state.
        peak = boundary["resident_state_bytes"]
        self.assertEqual(rate, Fraction(peak, 10 ** 9) * Fraction("0.05"))

    def test_holding_past_the_boundary_flips_the_ordering(self):
        boundary = m.calculate()["hold_boundary"]
        hours = float(value(boundary["hold_hours"]))
        below = m.calculate(state_hold_hours=hours * 0.5)
        above = m.calculate(state_hold_hours=hours * 2)
        pick = lambda result, name: value(next(row["total_cost"] for row in result["session_costs"]
                                               if row["placement"] == name))
        self.assertLess(pick(below, "remote_warm"), pick(below, "remote_stateless"))
        self.assertGreater(pick(above, "remote_warm"), pick(above, "remote_stateless"))

    def test_egress_boundary_flips_the_local_comparison(self):
        result = m.calculate()
        boundary = float(value(result["egress_price_boundary"]["price_per_gb"]))
        pick = lambda result, name: value(next(row["total_cost"] for row in result["session_costs"]
                                               if row["placement"] == name))
        for factor, warm_should_win in ((0.5, True), (2.0, False)):
            regions = {name: dict(row) for name, row in m.DEFAULT_REGIONS.items()}
            regions["far"]["egress_price_per_gb"] = str(boundary * factor)
            scenario = m.calculate(regions=regions)
            self.assertEqual(pick(scenario, "remote_warm") < pick(scenario, "local"), warm_should_win)

    def test_reuse_scan_crosses_and_the_measured_trace_sits_on_the_warm_side(self):
        result = m.calculate()
        scan = result["reuse_scan"]
        self.assertIsNotNone(scan["ordering_changes_between"])
        first, last = scan["scan"][0], scan["scan"][-1]
        self.assertFalse(first["warm_is_cheaper"])
        self.assertTrue(last["warm_is_cheaper"])
        # The measured hit fraction is far above the crossing.
        crossing = max(float(value(row["cache_hit_fraction"]))
                       for row in scan["scan"] if not row["warm_is_cheaper"])
        self.assertGreater(float(value(scan["measured_cache_hit_fraction"])), crossing)

    def test_warm_prefill_work_falls_as_reuse_rises(self):
        result = m.calculate()
        totals = [value(row["warm_total_cost"]) for row in result["reuse_scan"]["scan"]]
        self.assertEqual(totals, sorted(totals, reverse=True))


class WaitTests(unittest.TestCase):
    def test_local_pays_no_round_trip_and_remote_pays_one_per_round(self):
        result = m.calculate()
        rounds = len(result["round_ledger"])
        waits = {(row["placement"], row["round_trip_bound"]): value(row["session_wait_seconds"])
                 for row in result["session_waits"]}
        self.assertEqual(waits[("local", "low")], waits[("local", "high")])
        # Widening the round trip by 8ms costs one trip per round on the remote arms.
        for placement in ("remote_stateless", "remote_warm"):
            gap = waits[(placement, "high")] - waits[(placement, "low")]
            self.assertEqual(gap, Fraction(rounds) * Fraction(8, 1000))

    def test_stateless_waits_longer_than_warm(self):
        result = m.calculate()
        waits = {(row["placement"], row["round_trip_bound"]): value(row["session_wait_seconds"])
                 for row in result["session_waits"]}
        self.assertGreater(waits[("remote_stateless", "low")], waits[("remote_warm", "low")])
        self.assertGreater(waits[("remote_warm", "low")], waits[("local", "low")])


class OutputTests(unittest.TestCase):
    def test_result_is_json_serialisable_and_finite(self):
        result = m.calculate()
        text = json.dumps(result, ensure_ascii=False, allow_nan=False)
        self.assertIn("cross-region-placement", text)

    def test_markdown_keeps_the_lower_bound_distinct_from_the_measurement(self):
        text = m.markdown(m.calculate())
        self.assertIn("下界", text)
        self.assertIn("实测", text)
        self.assertIn("硬约束先于价格", text)

    def test_rejects_bad_inputs(self):
        for kwargs in ({"ingress_price_per_gb": -1}, {"state_hold_hours": 0},
                       {"device_flops_per_second": 0}, {"required_kw": 0}):
            with self.assertRaises(ValueError):
                m.calculate(**kwargs)


if __name__ == "__main__":
    unittest.main()
