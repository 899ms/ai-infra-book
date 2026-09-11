import unittest
from _gap_common import scenario_rows
from infra_calc.topics.straggler_max import calculate, expected_standard_max
from infra_calc.topics import checkpoint_interval


class StragglerTests(unittest.TestCase):
    def test_order_statistics_known_values(self):
        self.assertEqual(expected_standard_max(1), 0.0)
        self.assertAlmostEqual(expected_standard_max(2), 0.5641895835, places=8)  # 1/sqrt(pi)
        self.assertAlmostEqual(expected_standard_max(3), 0.8462843753, places=8)  # 3/(2 sqrt(pi))
        self.assertAlmostEqual(expected_standard_max(8), 1.4236003, places=6)

    def test_step_rows_and_responses(self):
        r = calculate(ranks=[8, 48])
        for row in r['rows']:
            self.assertAlmostEqual(row['expected_max_seconds'], 52.2 + 1.044 * row['expected_standard_max'])
            self.assertAlmostEqual(row['expected_step_seconds'], row['expected_max_seconds'] + 4.5)
            self.assertGreater(row['responses']['wait']['step_seconds'], row['expected_step_seconds'] - 1e-9)
            self.assertGreater(row['responses']['redistribute']['step_seconds'], 56.7)
        base = checkpoint_interval.calculate(model='qwen3-8b', devices=48, intervals_seconds=[300, 600, 900, 1800, 3600])
        self.assertEqual(r['evict_response']['blocking_save_cost_exact_seconds'], base['summary']['blocking_save_cost_exact_seconds'])
        for row in r['checkpoint_loss']['rows']:
            self.assertGreater(row['with_spike_rollback_loss'], row['hardware_only_loss'])

    def test_scenarios(self):
        for row in scenario_rows('straggler_max'):
            calculate(**row['inputs'], input_sources=row['input_sources'])


if __name__ == '__main__':
    unittest.main()
