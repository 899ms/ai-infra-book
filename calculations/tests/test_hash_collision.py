from fractions import Fraction as F
from itertools import product
import unittest
from _gap_common import scenario_rows
from infra_calc.topics.hash_collision import calculate, max_load_distribution


class HashCollisionTests(unittest.TestCase):
    def test_exact_distribution_against_enumeration(self):
        for n, m in ((3, 2), (4, 3), (5, 4)):
            cdf = max_load_distribution(n, m)
            counts = [0] * (n + 1)
            for assignment in product(range(m), repeat=n):
                counts[max(assignment.count(b) for b in range(m))] += 1
            for bound in range(n + 1):
                self.assertEqual(cdf[bound], F(sum(counts[:bound + 1]), m ** n))

    def test_summary_identities(self):
        r = calculate(flows=8, uplinks=8, spray_paths=0)['summary']
        self.assertEqual(F(r['probability_no_collision_exact']), F(40320, 8 ** 8))
        self.assertEqual(F(r['expected_empty_uplinks_exact']), 8 * F(7, 8) ** 8)
        self.assertEqual(F(r['effective_fraction_of_nominal_cut_exact']) * F(r['expected_max_load_exact']), 1)
        self.assertGreater(F(r['expected_max_load_exact']), 2)

    def test_spray_reuses_packet_reorder(self):
        s = calculate(flows=8, uplinks=8, spray_paths=2, spray_tokens=1, spray_packet_bytes=4096, spray_path_delays_ns=[0, 0])['per_packet_spray']
        self.assertEqual(s['packet_count'], 2)
        self.assertEqual(F(s['completion_exact_ns']), F(4096 * 10**9, 50 * 10**9))
        self.assertEqual(F(s['reorder_wait_exact_ns']), 0)
        with self.assertRaises(ValueError):
            calculate(spray_paths=3, spray_path_delays_ns=[1, 2])

    def test_scenarios(self):
        rows = scenario_rows('hash_collision')
        ids = [row['id'] for row in rows]
        self.assertEqual(ids, ['hash-collision-8-on-32', 'hash-collision-8-on-16', 'hash-collision-32-on-32',
                               'hash-collision-32-on-16', 'hash-collision-128-on-16'])
        for row in rows:
            n, m = row['inputs']['flows'], row['inputs']['uplinks']
            # Flows sharing one leaf switch are hashed onto that leaf's uplinks: 32 for the k=64
            # nonblocking leaf, 16 for the 3:1 oversubscribed leaf (clos-cut results).
            self.assertIn(m, (16, 32))
            self.assertEqual(row['id'], f'hash-collision-{n}-on-{m}')
            clos = 'results/clos-cut-k64-nonblocking.md' if m == 32 else 'results/clos-cut-k64-oversub3.md'
            self.assertTrue(row['input_sources']['uplinks'].startswith(clos), row['id'])
            r = calculate(**row['inputs'], input_sources=row['input_sources'])
            self.assertEqual(r['summary']['p99_max_load'] >= 1, True)
            self.assertLess(F(r['summary']['effective_fraction_of_nominal_cut_exact']), 1)
            self.assertEqual(r['per_packet_spray'] is not None, row['inputs']['spray_paths'] > 0)
        spray = calculate(**rows[0]['inputs'])['per_packet_spray']
        self.assertEqual((spray['paths'], spray['payload_bytes']), (8, 8 * 2**20))


if __name__ == '__main__':
    unittest.main()
