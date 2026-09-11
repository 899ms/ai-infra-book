from fractions import Fraction as F
import unittest
from _gap_common import scenario_rows
from infra_calc.topics.clos_cut import calculate


class ClosCutTests(unittest.TestCase):
    def test_fat_tree_reach_and_bisection(self):
        r = calculate(radix=64, oversubscription='1', supernode_scenario=None)
        two, three = r['tiers']
        self.assertEqual((two['endpoints'], three['endpoints']), (64 * 64 // 2, 64 ** 3 // 4))
        self.assertEqual(three['switches'], dict(edge=2048, aggregation=2048, core=1024))
        self.assertEqual(F(two['bisection_fraction_of_nonblocking_exact']), 1)
        self.assertEqual(F(two['bisection_bytes_per_second_exact']), F(2048, 2) * 50 * 10**9)
        cut = r['partition_cuts'][0]
        self.assertEqual((cut['leaves_used'], cut['cut_links']), (32, 1024))
        self.assertEqual(F(cut['cut_bytes_per_second_per_endpoint_exact']), 50 * 10**9)

    def test_oversubscription_scales_reach_and_cut(self):
        r = calculate(radix=64, oversubscription='3', supernode_scenario=None)
        self.assertEqual((r['leaf']['downlinks'], r['leaf']['uplinks']), (48, 16))
        self.assertEqual(r['tiers'][1]['endpoints'], 64 ** 3 // 4 * 48 // 32)
        self.assertEqual(F(r['tiers'][0]['bisection_fraction_of_nonblocking_exact']), F(1, 3))
        self.assertEqual(F(r['partition_cuts'][0]['cut_bytes_per_second_per_endpoint_exact']), F(22 * 16 * 50 * 10**9, 1024))
        with self.assertRaises(ValueError):
            calculate(radix=64, oversubscription='2', supernode_scenario=None)

    def test_supernode_egress_reads_scenario(self):
        r = calculate(oversubscription='3')['supernode_egress']
        self.assertEqual(r['gpus'], 1024)
        for row in r['rows']:
            self.assertEqual(F(row['oversubscribed_egress_bytes_per_second_exact']) * 3, F(row['nominal_nic_egress_bytes_per_second_exact']))

    def test_rail_pairs_and_bytes(self):
        r = calculate(mode='rail')
        g = r['gradient']
        self.assertEqual(g['bytes'], 12288 * 4096 * 4)
        self.assertEqual(r['summary']['bytes_per_rail_each_direction'], g['bytes'] // 8)
        self.assertEqual([p['nic_rail_server1'] for p in r['pairs']], list(range(8)))
        self.assertEqual(r['summary']['spine_crossing_bytes'], 0)
        self.assertEqual(F(r['summary']['per_rail_seconds_exact']), F(g['bytes'] // 8, 50 * 10**9) + F(4000, 10**9))
        self.assertEqual(F(r['summary']['rail_parallel_speedup_exact']) < 8, True)
        shifted = calculate(mode='rail', pairing='shifted')
        self.assertEqual(shifted['summary']['spine_crossing_bytes'], g['bytes'])

    def test_in_network_rows_are_consistent_with_results(self):
        r = calculate(mode='in_network')
        for row in r['rows']:
            self.assertEqual(row['switch_reduce']['rounds'], 1)
            self.assertEqual(row['switch_reduce']['cross_server_bytes'], row['shard_bytes'] * row['ranks'])
            self.assertEqual(row['shard_bytes'] * row['local_ranks'], row['gradient_bytes_per_rank'])

    def test_scenarios(self):
        for row in scenario_rows('clos_cut'):
            calculate(**row['inputs'], input_sources=row['input_sources'])


if __name__ == '__main__':
    unittest.main()
