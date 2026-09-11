"""Independent size, directional traffic and necessary-budget checks."""
from fractions import Fraction
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from infra_calc.topics import hierarchical_gradient as gradient

ELEMENTS = 12288 * 4096
MiB = 2**20
# Contrast configuration: four ranks per server, two 25 GB/s NICs behind a 40 GB/s shared exit.
TWO_NIC = dict(ranks_per_server=4, nics_per_server=2, nic_bytes_per_second=25_000_000_000,
               local_bytes_per_second=200_000_000_000, shared_egress_bytes_per_second=40_000_000_000)


class HierarchicalGradientTests(unittest.TestCase):
    def test_book_configuration_conservation(self):
        """Two HGX-class servers: 16 ranks, one 50 GB/s NIC per rank, 450 GB/s local."""
        for dtype, width in [('FP32', 4), ('BF16', 2)]:
            payload = ELEMENTS * width
            for algorithm, remote_factor, rounds, nics, edges in [
                ('flat_contiguous', Fraction(15, 4), 30, 1, 2),
                ('flat_interleaved', 30, 30, 8, 16), ('hierarchical', 2, 16, 8, 0)
            ]:
                result = gradient.calculate(gradient_dtype=dtype, algorithm=algorithm)
                self.assertEqual(result['gradient']['bytes_per_rank'], payload)
                self.assertEqual(result['gradient']['participants'], 16)
                summary = result['summary']
                self.assertEqual(summary['network_send_bytes'], 30 * payload)
                self.assertEqual(summary['remote_send_bytes'], remote_factor * payload)
                self.assertEqual(summary['reduction_scalar_adds'], 15 * ELEMENTS)
                self.assertEqual(summary['rounds'], rounds)
                self.assertEqual(summary['remote_nics_used_per_server'], nics)
                self.assertEqual(summary['first_round_remote_edges'], edges)
                self.assertIsNone(summary['actual_training_deadline_feasible'])

    def test_contiguous_ring_uses_one_nic_and_hierarchy_uses_all_eight(self):
        payload = ELEMENTS * 4
        chunk = payload // 16
        flat = gradient.calculate(algorithm='flat_contiguous')
        # Thirty rounds, each waiting on one 12 MiB message through a single 50 GB/s NIC.
        expected = 30 * (Fraction(chunk, 50_000_000_000) + Fraction(2000, 10**9))
        self.assertEqual(Fraction(flat['summary']['serial_barrier_lower_seconds_exact']), expected)
        resources = {r['resource']: r for r in flat['resources']}
        self.assertEqual(resources['server0.nic7.tx']['bytes'], 30 * chunk)
        self.assertEqual(resources['server1.nic0.rx']['bytes'], 30 * chunk)
        self.assertNotIn('server0.nic0.tx', resources)
        self.assertNotIn('server0.egress', resources)
        hier = gradient.calculate(algorithm='hierarchical')
        # Fourteen local rounds of 24 MiB over NVLink plus two cross-server rounds of 12 MiB per NIC.
        expected = 14 * (Fraction(2 * chunk, 450_000_000_000) + Fraction(2000, 10**9))
        expected += 2 * (Fraction(chunk, 50_000_000_000) + Fraction(2000, 10**9))
        self.assertEqual(Fraction(hier['summary']['serial_barrier_lower_seconds_exact']), expected)
        resources = {r['resource']: r for r in hier['resources']}
        for nic in range(8):
            self.assertEqual(resources[f'server0.nic{nic}.tx']['bytes'], 2 * chunk)
            self.assertEqual(resources[f'server1.nic{nic}.rx']['bytes'], 2 * chunk)
        self.assertEqual(hier['summary']['remote_send_bytes_per_direction'], 16 * 2 * chunk // 2)
        self.assertTrue(hier['summary']['necessary_budget_not_excluded'])
        self.assertFalse(flat['summary']['necessary_budget_not_excluded'])
        # The interleaved ring moves eight times the cross-server bytes for the same round time.
        inter = gradient.calculate(algorithm='flat_interleaved')
        self.assertEqual(inter['summary']['serial_barrier_lower_seconds_exact'], flat['summary']['serial_barrier_lower_seconds_exact'])
        self.assertEqual(inter['summary']['remote_send_bytes'], 8 * flat['summary']['remote_send_bytes'])

    def test_single_nic_striping_serialises_the_cross_server_stage(self):
        payload = ELEMENTS * 4
        chunk = payload // 16
        result = gradient.calculate(algorithm='hierarchical', nics_per_server=1)
        expected = 14 * (Fraction(2 * chunk, 450_000_000_000) + Fraction(2000, 10**9))
        expected += 2 * (Fraction(8 * chunk, 50_000_000_000) + Fraction(2000, 10**9))
        self.assertEqual(Fraction(result['summary']['serial_barrier_lower_seconds_exact']), expected)
        self.assertEqual(result['summary']['remote_nics_used_per_server'], 1)

    def test_contrast_configuration_two_nics_cannot_exceed_shared_egress(self):
        payload = ELEMENTS * 4
        for algorithm, remote_factor, rounds in [('flat_contiguous', Fraction(7, 2), 14),
                                                 ('flat_interleaved', 14, 14), ('hierarchical', 2, 8)]:
            summary = gradient.calculate(algorithm=algorithm, **TWO_NIC)['summary']
            self.assertEqual(summary['network_send_bytes'], 14 * payload)
            self.assertEqual(summary['remote_send_bytes'], remote_factor * payload)
            self.assertEqual(summary['rounds'], rounds)
        result = gradient.calculate(**TWO_NIC)
        # Six local rounds M/4 on 200 GB/s, two remote rounds M/2 on a fixed 40 GB/s exit.
        expected = 6 * Fraction(payload, 4 * 200_000_000_000)
        expected += 2 * Fraction(payload, 2 * 40_000_000_000)
        expected += Fraction(8 * 2000, 10**9)
        self.assertEqual(Fraction(result['summary']['serial_barrier_lower_seconds_exact']), expected)
        resources = {r['resource']: r for r in result['resources']}
        self.assertEqual(resources['server0.egress']['bytes'], payload)
        for nic in (0, 1):
            self.assertEqual(resources[f'server0.nic{nic}.tx']['bytes'], payload // 2)
            self.assertEqual(resources[f'server1.nic{nic}.rx']['bytes'], payload // 2)
        times = {n: Fraction(gradient.calculate(algorithm='flat_contiguous', **dict(TWO_NIC, nics_per_server=n))['summary']['serial_barrier_lower_seconds_exact']) for n in (1, 2, 3)}
        self.assertEqual(times[1], 14 * (Fraction(24 * MiB, 25_000_000_000) + Fraction(2000, 10**9)))
        self.assertEqual(times[2], times[3])
        self.assertEqual(times[2], 14 * (Fraction(24 * MiB, 40_000_000_000) + Fraction(2000, 10**9)))

    def test_receiver_can_determine_bound_and_budget_is_only_necessary(self):
        payload = ELEMENTS * 4
        arguments = {'bandwidth_overrides': {'server1.nic0.rx': 1_000_000_000}, **TWO_NIC, 'nics_per_server': 1}
        result = gradient.calculate(**arguments)
        expected = Fraction(6 * payload, 4 * 200_000_000_000)
        expected += Fraction(payload, 1_000_000_000) + Fraction(16000, 10**9)
        self.assertEqual(Fraction(result['summary']['serial_barrier_lower_seconds_exact']), expected)
        ns = expected * 10**9
        floor = ns.numerator // ns.denominator
        for budget, allowed in [(floor, ns.denominator == 1), (floor + 1, True)]:
            summary = gradient.calculate(**arguments, budget_ns=budget)['summary']
            self.assertEqual(summary['necessary_budget_not_excluded'], allowed)
            self.assertIsNone(summary['actual_training_deadline_feasible'])

    def test_invalid_inputs_do_not_get_unlimited_resources(self):
        cases = [dict(nics_per_server=True), dict(nics_per_server=9), dict(nics_per_server=0),
                 dict(ranks_per_server=6), dict(ranks_per_server=4, nics_per_server=8),
                 dict(nic_bytes_per_second=0), dict(local_bytes_per_second=None),
                 dict(shared_egress_bytes_per_second=0),
                 dict(gradient_dtype='FP8'), dict(startup_ns=-1), dict(budget_ns=True),
                 dict(bandwidth_overrides={'unknown': 10}),
                 dict(bandwidth_overrides={'server0.nic0.tx': 0}),
                 dict(bandwidth_overrides={'server0.egress': 10}),
                 dict(bandwidth_overrides={'server0.nic0.tx': None})]
        for arguments in cases:
            with self.subTest(arguments=arguments), self.assertRaises(ValueError):
                gradient.calculate(**arguments)


if __name__ == '__main__':
    unittest.main()
