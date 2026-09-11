from fractions import Fraction as F
import unittest
from _gap_common import scenario_rows
from infra_calc.topics.feedback_queue import incast


class IncastTests(unittest.TestCase):
    def test_allowed_delay_and_required_buffer(self):
        r = incast(senders=[8, 16, 64], sender_bytes_per_second=50 * 10**9, egress_bytes_per_second=50 * 10**9, free_buffer_bytes=2**20)
        for row in r['rows']:
            excess = (row['N'] - 2) * 50 * 10**9
            self.assertEqual(F(row['excess_bytes_per_second_exact']), excess)
            self.assertEqual(F(row['allowed_feedback_ns_exact']), F(2**20 * 10**9, excess))
            self.assertEqual(F(row['required_buffer_bytes']['end_to_end']['exact']), F(20000 * excess, 10**9))
            self.assertEqual(row['fluid_check']['dropped_exact_bytes'], '0')
        self.assertEqual(F(r['feedback_distances'][0]['feedback_ns_exact']), 300 + F(1500 * 10**9, 50 * 10**9))
        self.assertFalse(r['summary']['end_to_end_fits']['8'])
        self.assertTrue(r['summary']['one_hop_fits']['64'])

    def test_no_excess_and_validation(self):
        r = incast(senders=[2], sender_bytes_per_second=10, egress_bytes_per_second=10)
        self.assertIn('note', r['rows'][0])
        with self.assertRaises(ValueError):
            incast(senders=[1])

    def test_scenarios(self):
        for row in scenario_rows('incast_feedback'):
            incast(**row['inputs'], input_sources=row['input_sources'])


if __name__ == '__main__':
    unittest.main()
