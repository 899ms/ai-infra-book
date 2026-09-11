from fractions import Fraction as F
import unittest
from _gap_common import scenario_rows
from infra_calc.topics.moe_capacity import calculate


class MoECapacityTests(unittest.TestCase):
    def test_chapter_example(self):
        r = calculate()
        rows = {row['capacity_factor_exact']: row for row in r['chapter_example']['rows']}
        self.assertEqual((rows['1']['capacity_per_expert'], rows['1']['dropped_total'], rows['1']['padded_total']), (64, 32, 32))
        self.assertEqual((rows['5/4']['dropped_total'], rows['5/4']['padded_total']), (16, 48))
        self.assertEqual((rows['3/2']['dropped_total'], rows['3/2']['padded_total']), (0, 64))
        self.assertEqual(rows['2']['padded_total'], 128)

    def test_locked_config_example(self):
        r = calculate()
        m = r['model_example']
        self.assertEqual((m['experts'], m['top_k'], m['assignments']), (128, 8, 65536))
        for row in m['rows']:
            executed = row['executed_rows_total']
            self.assertEqual(executed, 128 * row['capacity_per_expert'])
            self.assertEqual(executed + row['dropped_total'], 65536 + row['padded_total'])
        with self.assertRaises(ValueError):
            calculate(declared_hot_multiplier='3')

    def test_scenarios(self):
        for row in scenario_rows('moe_capacity'):
            calculate(**row['inputs'], input_sources=row['input_sources'])


if __name__ == '__main__':
    unittest.main()
