from fractions import Fraction as F
import unittest
from _gap_common import scenario_rows
from infra_calc.topics.critical_batch import calculate


class CriticalBatchTests(unittest.TestCase):
    def test_relation_and_ceiling(self):
        r = calculate()
        ref = r['reference']
        self.assertEqual(ref['steps'], 31790)
        s_min, e_min, noise = F(ref['s_min_exact']), F(ref['e_min_exact']), F(ref['noise_scale_tokens'])
        self.assertEqual(e_min / s_min, noise)
        for row in r['rows']:
            b = F(row['weak_batch_tokens'])
            s = s_min * (1 + noise / b)
            self.assertEqual(F(row['weak_steps_exact']), s)
            self.assertAlmostEqual(row['weak_examples_tokens'], float(b * s))
            self.assertEqual(row['strong_steps'], 31790)
        ref_row = next(row for row in r['rows'] if row['cards'] == 48)
        self.assertEqual(ref_row['weak_speedup_over_reference'], 1.0)
        self.assertEqual(F(r['summary']['weak_scaling_speedup_ceiling_exact']), 1 + noise / F(384 * 8192))
        with self.assertRaises(ValueError):
            calculate(overhead_seconds_per_step='1')

    def test_scenarios(self):
        for row in scenario_rows('critical_batch'):
            calculate(**row['inputs'], input_sources=row['input_sources'])


if __name__ == '__main__':
    unittest.main()
