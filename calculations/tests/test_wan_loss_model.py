from fractions import Fraction as F
from math import comb
import unittest
from _gap_common import scenario_rows
from infra_calc.topics.wan_loss_model import calculate


class WanLossTests(unittest.TestCase):
    def test_mathis_and_budget(self):
        r = calculate()
        self.assertAlmostEqual(r['mathis']['mbit_per_second'], 0.155, places=3)
        self.assertEqual(F(r['bbr_ideal']['goodput_bits_per_second_exact']), F('0.86') * 333 * 10**6)
        self.assertEqual(F(r['path']['bdp_bytes_exact']), F(333 * 10**6) * F(1, 5) / 8)
        s = r['reliable_stream']
        self.assertEqual(s['packets'], 245)
        self.assertEqual(F(s['serial_budget_seconds_exact']), F(1, 5) + F(3, 100) + F(354640 * 8, 333 * 10**6))
        self.assertAlmostEqual(s['serial_budget_seconds'], 0.2385, places=4)
        self.assertEqual(s['p99_rounds'], 6)
        self.assertGreater(s['expected_completion_seconds'], 3 * s['serial_budget_seconds'])

    def test_fec_binomial_tail(self):
        r = calculate()
        row = r['fec']['rows'][0]
        k, rep, p = row['data_symbols'], row['repair_symbols'], F('0.14')
        tail = lambda n, up: sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(up + 1))
        self.assertGreaterEqual(tail(k + rep, rep), F('0.999'))
        self.assertLess(tail(k + rep - 1, rep - 1), F('0.999'))
        self.assertEqual(r['fec']['rows'][1]['repair_symbols'], rep + 1)

    def test_scenarios(self):
        for row in scenario_rows('wan_loss_model'):
            calculate(**row['inputs'], input_sources=row['input_sources'])


if __name__ == '__main__':
    unittest.main()
