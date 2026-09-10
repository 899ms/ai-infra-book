"""Independent checks for the Queqiao record re-accounting (C70).

Every expected value here is recomputed by hand from the two pinned documents,
not copied from the module's own output.
"""
import copy
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
from infra_calc.topics import queqiao_records as m


def value(entry):
    return Fraction(**entry)


class RecordIntegrityTests(unittest.TestCase):
    def test_every_locked_input_is_verified(self):
        records, locked = m.load()
        self.assertEqual(len(locked), 3)
        self.assertTrue(all(row["sha256"] for row in locked))
        self.assertEqual(records["reported_resolution_ms"], 0.1)

    def test_a_changed_source_is_rejected(self):
        original = (m.PROJECT / "sources/queqiao-records/records.json").read_bytes()
        try:
            (m.PROJECT / "sources/queqiao-records/records.json").write_bytes(original + b" ")
            with self.assertRaises(ValueError):
                m.load()
        finally:
            (m.PROJECT / "sources/queqiao-records/records.json").write_bytes(original)
        m.load()

    def test_frame_runs_conserve_offered_frames(self):
        # 16 sessions x 200 messages = 3200, and delivered + lost must reach it.
        records, _ = m.load()
        for row in records["frame_records"]:
            if row["delivered_recorded"] is None:
                continue
            self.assertEqual(row["delivered_recorded"] + row["lost"], row["offered"], row["id"])


class ArithmeticTests(unittest.TestCase):
    def test_serialization_matches_hand_arithmetic(self):
        # 354640 bytes x 8 bits / 333e6 bit/s = 2837120000/333000000 ms
        got = m.serialization_ms(354640, 333_000_000)
        self.assertEqual(got, Fraction(354640 * 8 * 1000, 333_000_000))
        self.assertAlmostEqual(float(got), 8.51988, places=4)

    def test_slow_start_needs_five_rounds_for_the_fixed_file(self):
        # 354640 / 1448 = 244.9 -> 245 segments; 10*(2^5-1)=310 >= 245 > 10*(2^4-1)=150.
        ramp = m.slow_start_rounds(354640, 1448, 10)
        self.assertEqual(ramp["segments"], 245)
        self.assertEqual(ramp["rounds"], 5)
        self.assertEqual([step["window_segments"] for step in ramp["schedule"]],
                         [10, 20, 40, 80, 160])

    def test_floor_is_an_interval_from_two_recorded_intervals(self):
        floor = m.floor_interval(354640, (197.0, 205.0), (30.0, 38.0), 333_000_000)
        self.assertEqual(value(floor["low_ms"]), Fraction("197") + Fraction(354640 * 8 * 1000, 333_000_000) + Fraction("30"))
        self.assertEqual(value(floor["high_ms"]), Fraction("205") + Fraction(354640 * 8 * 1000, 333_000_000) + Fraction("38"))
        self.assertLess(value(floor["low_ms"]), value(floor["high_ms"]))

    def test_a_median_under_one_round_trip_plus_model_admits_no_payload(self):
        # 225.8 - 199 - 30 is negative, so no size fits under the stated band.
        self.assertIsNone(m.largest_feasible_payload_bytes(225.8, 199.0, 30.0, 333_000_000))
        # At the recorded minimum round trip it becomes feasible again.
        self.assertIsNotNone(m.largest_feasible_payload_bytes(225.8, 185.9, 30.0, 333_000_000))

    def test_quantile_support_counts_order_statistics(self):
        self.assertEqual(m.quantile_support(1200, Fraction(99, 100))["samples_beyond"], 12)
        # p999 over 1200 frames is the second largest sample.
        tail = m.quantile_support(1200, Fraction(999, 1000))
        self.assertEqual(tail["order_statistic_rank"], 1199)
        self.assertEqual(tail["samples_beyond"], 1)
        self.assertFalse(tail["supported"])
        self.assertIsNone(m.quantile_support(None, Fraction(99, 100))["supported"])


class ConditionTests(unittest.TestCase):
    def test_rows_from_different_conditions_cannot_be_compared(self):
        records, _ = m.load()
        rows = {row["id"]: row for row in records["request_records"]}
        with self.assertRaises(ValueError):
            m.compare(rows["asr-rot-new-direct"], rows["asr-fixed-new-queqiao"])
        with self.assertRaises(ValueError):
            m.compare(rows["asr-rot-held-stock-direct"], rows["asr-rot-held-tuned-queqiao"])
        with self.assertRaises(ValueError):
            m.compare(rows["asr-rot-new-direct"], rows["asr-rot-new-direct"])

    def test_same_condition_ratios_reproduce_the_documents_headlines(self):
        result = m.calculate()
        ratios = {(row["numerator_id"], row["denominator_id"]): value(row["ratio"])
                  for row in result["same_condition_comparisons"]}
        # PATH states 15.5x for the fixed-file synthesis download.
        self.assertEqual(ratios[("tts-fixed-new-direct", "tts-fixed-new-queqiao")], Fraction("827.7") / Fraction("53.4"))
        self.assertAlmostEqual(float(ratios[("tts-fixed-new-direct", "tts-fixed-new-queqiao")]), 15.5, places=1)
        # PATH states 8.8x once the client is tuned on the erasing direction.
        self.assertAlmostEqual(float(ratios[("tts-rot-held-tuned-direct", "tts-rot-held-tuned-queqiao")]), 8.8, places=1)
        # PATH states the tuned direct client beats the transport by 1.3x.
        self.assertAlmostEqual(1 / float(ratios[("asr-rot-held-tuned-direct", "asr-rot-held-tuned-queqiao")]), 1.3, places=1)
        # PATH states 1.03x warm on the fixed file, but that is a median of
        # per-round ratios; the ratio of the two medians is 240.9/236.5.
        self.assertEqual(ratios[("asr-fixed-held-tuned-direct", "asr-fixed-held-tuned-queqiao")],
                         Fraction("240.9") / Fraction("236.5"))

    def test_paired_ratio_is_carried_and_never_recomputed(self):
        result = m.calculate()
        rows = {(row["numerator_id"], row["denominator_id"]): row
                for row in result["same_condition_comparisons"]}
        warm = rows[("asr-fixed-held-tuned-direct", "asr-fixed-held-tuned-queqiao")]
        self.assertEqual(value(warm["documented_paired_ratio"]), Fraction("1.03"))
        # The two statistics differ, and the difference is stated rather than hidden.
        self.assertNotEqual(value(warm["documented_paired_ratio"]), value(warm["ratio"]))
        self.assertEqual(value(warm["paired_vs_ratio_of_medians"]),
                         Fraction("1.03") - Fraction("240.9") / Fraction("236.5"))
        # A condition the documents give no paired median for stays empty.
        stock = rows[("asr-rot-held-stock-direct", "asr-rot-held-stock-queqiao")]
        self.assertIsNone(stock["documented_paired_ratio"])
        self.assertIsNone(stock["paired_vs_ratio_of_medians"])

    def test_retracted_row_is_flagged_below_the_floor(self):
        result = m.calculate()
        rows = {row["id"]: row for row in result["floor_feasibility"]}
        retracted = rows["asr-rot-held-tuned-direct"]
        self.assertIsNone(retracted["largest_feasible_payload_bytes"])
        self.assertTrue(retracted["below_floor_at_smallest_payload"])
        self.assertFalse(retracted["label_supported"])
        # The surviving fixed-file rows sit just above the same floor.
        for name in ("asr-fixed-held-tuned-direct", "asr-fixed-held-tuned-queqiao"):
            self.assertFalse(rows[name]["below_floor_at_smallest_payload"], name)
            self.assertTrue(rows[name]["label_supported"])


class LegAndQuantileTests(unittest.TestCase):
    def test_legs_do_not_add_and_the_residual_beats_rounding(self):
        result = m.calculate()
        rows = {row["id"]: row for row in result["leg_accounts"]}
        direct = rows["asr-rot-new-direct"]
        # 187.1 + 948.2 = 1135.3 against a recorded total of 1133.5.
        self.assertEqual(value(direct["summed_legs_ms"]), Fraction("1135.3"))
        self.assertEqual(value(direct["residual_ms"]), Fraction("-1.8"))
        self.assertEqual(value(direct["resolution_bound_ms"]), Fraction("0.15"))
        self.assertFalse(direct["within_resolution"])
        # The tunnel arm's residual is inside the reported resolution.
        self.assertTrue(rows["asr-rot-new-queqiao"]["within_resolution"])

    def test_capture_and_playback_are_outside_every_recorded_leg(self):
        result = m.calculate()
        for row in result["leg_accounts"]:
            if not row["decomposable"]:
                continue
            for stage in ("capture", "encode", "playback_buffer", "playback"):
                self.assertIn(stage, row["stages_uncovered"], row["id"])

    def test_missing_quantiles_stay_missing(self):
        result = m.calculate()
        rows = {row["id"]: row for row in result["frame_runs"]}
        endtoend = rows["frames-dc-udp-direct"]
        self.assertFalse(endtoend["quantiles"]["p50"]["available"])
        self.assertIsNone(endtoend["quantiles"]["p50"]["value_ms"])
        self.assertIsNone(endtoend["tail_over_median"])
        self.assertIsNotNone(endtoend["tail_over_median_reason"])
        # A run that prints both keeps its ratio.
        live = rows["frames-live-tcp-queqiao"]
        self.assertEqual(value(live["tail_over_median"]), Fraction("728.4") / Fraction("208.4"))

    def test_p999_from_1200_frames_is_marked_unsupported(self):
        result = m.calculate()
        row = {item["id"]: item for item in result["frame_runs"]}["frames-dc-tcp-queqiao"]
        support = row["quantiles"]["p999"]["support"]
        self.assertEqual(support["samples_beyond"], 1)
        self.assertFalse(support["supported"])

    def test_loss_fractions_are_exact(self):
        result = m.calculate()
        rows = {row["id"]: row for row in result["frame_runs"]}
        self.assertEqual(value(rows["frames-live-udp-direct"]["loss_fraction"]), Fraction(163, 3200))
        self.assertEqual(value(rows["frames-live-udp-queqiao"]["loss_fraction"]), Fraction(34, 3200))
        self.assertEqual(rows["frames-dc-udp-direct"]["delivered_derived"], 1160)
        self.assertIsNone(rows["frames-emulated-24-session"]["loss_fraction"])


class SupplyTests(unittest.TestCase):
    def test_only_the_eroded_download_falls_under_playback_consumption(self):
        result = m.calculate()
        supply = result["playback_supply"]
        self.assertEqual(supply["consumption_bits_per_s"], 16000 * 1 * 2 * 8)
        short = [row for row in supply["rows"] if not row["sufficient_for_playback"]]
        self.assertEqual([row["measurement"] for row in short], ["download_direct_cubic_low"])
        # 60ms of buffer at 0.13 Mbit/s supply against 0.256 Mbit/s consumption:
        # 60 * 256000 / (256000 - 130000) ms.
        self.assertEqual(value(short[0]["stall_onset_ms"]),
                         Fraction(60) * Fraction(256000) / Fraction(256000 - 130000))

    def test_a_larger_prebuffer_only_moves_the_stall_later(self):
        small = m.calculate(prebuffer_ms=60.0)["playback_supply"]["rows"]
        large = m.calculate(prebuffer_ms=600.0)["playback_supply"]["rows"]
        pick = lambda rows: next(row for row in rows if row["measurement"] == "download_direct_cubic_low")
        self.assertEqual(value(pick(large)["stall_onset_ms"]), 10 * value(pick(small)["stall_onset_ms"]))
        self.assertFalse(pick(large)["sufficient_for_playback"])

    def test_rejects_a_nonpositive_prebuffer(self):
        for bad in (0, -1, float("nan")):
            with self.assertRaises(ValueError):
                m.calculate(prebuffer_ms=bad)


class OutputTests(unittest.TestCase):
    def test_result_is_json_serialisable_and_finite(self):
        result = m.calculate()
        text = json.dumps(result, ensure_ascii=False, allow_nan=False)
        self.assertIn("queqiao-recorded-conditions", text)
        self.assertNotIn("NaN", text)

    def test_markdown_states_the_retraction_and_the_unsupported_quantile(self):
        result = m.calculate()
        text = m.markdown(result)
        self.assertIn("不可行", text)
        self.assertIn("Below the floor", text)
        self.assertIn("分位数", text)

    def test_calculate_does_not_mutate_the_loaded_records(self):
        before = copy.deepcopy(m.load()[0])
        m.calculate()
        self.assertEqual(before, m.load()[0])


if __name__ == "__main__":
    unittest.main()
