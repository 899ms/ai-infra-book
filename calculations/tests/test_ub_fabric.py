"""Additive state, cache-spill boundaries, phase sums and setup counts for the UB fabric topic."""
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from infra_calc.topics.ub_fabric import calculate, PAPER_MEASURED_NS


class UBFabricTests(unittest.TestCase):
    def test_state_is_additive_versus_multiplicative(self):
        r = calculate()
        top = r['state'][-1]
        self.assertEqual(top['endpoints'], 1024)
        self.assertEqual(top['ub_bytes'], 1024 * 52 + 1024 * 56)
        self.assertEqual(top['roce_bytes'], 1024 * 1024 * 512 + 1024 * 32)
        self.assertEqual(top['ratio'], 4854.8)
        self.assertEqual(r['state'][0]['roce_bytes'], 544)
        self.assertEqual(r['state'][0]['ub_bytes'], 108)

    def test_cache_spill_boundaries(self):
        r = calculate()
        self.assertEqual(r['cache']['roce_spill_endpoints'], 23)
        self.assertEqual(22 * 22 * 512 + 22 * 32 <= 262144, True)
        self.assertEqual(r['cache']['ub_spill_endpoints'], 2428)
        self.assertEqual(r['cache']['roce_refetch_ns'], 1000)
        self.assertEqual(r['cache']['ub_refetch_ns'], 200)
        sweep = {row['endpoints']: row for row in r['cache']['sweep']}
        self.assertAlmostEqual(sweep[22]['roce_dma_ns'], sweep[1]['roce_dma_ns'])
        self.assertAlmostEqual(sweep[23]['roce_dma_ns'], sweep[1]['roce_dma_ns'] + 1000)
        self.assertAlmostEqual(sweep[2427]['ub_loadstore_ns'], sweep[1]['ub_loadstore_ns'])
        self.assertAlmostEqual(sweep[2428]['ub_loadstore_ns'], sweep[1]['ub_loadstore_ns'] + 200)
        large = calculate(context_cache_bytes=1048576)
        self.assertEqual(large['cache']['roce_spill_endpoints'], 46)

    def test_round_trip_phase_sums_match_paper_within_handoff_overhead(self):
        r = calculate()
        rt = r['round_trip']
        self.assertAlmostEqual(rt['ub_loadstore']['total_ns'], 420, delta=1)
        self.assertAlmostEqual(rt['ub_urma']['total_ns'], 746, delta=1)
        self.assertAlmostEqual(rt['roce_dma']['total_ns'], 2222, delta=1)
        self.assertEqual(rt['roce_dma']['group_ns']['PCIe 穿越'], 1650)
        self.assertEqual(rt['ub_loadstore']['group_ns']['PCIe 穿越'], 0)
        self.assertEqual(rt['ub_loadstore']['group_ns']['软件提交'], 0)
        for stack, measured in PAPER_MEASURED_NS.items():
            self.assertLess(abs(rt[stack]['total_ns'] - measured), 81)
        for stack in rt:
            for point in rt[stack]['link_sweep']:
                self.assertAlmostEqual(point['total_ns'], rt[stack]['fixed_ns'] + 2 * point['link_ns'])
        self.assertEqual(r['summary']['round_trip_ratio'], 5.3)

    def test_hosts_in_cache_and_setup_counts(self):
        r = calculate()
        self.assertEqual(r['summary']['roce_max_hosts_in_cache'], 8)
        self.assertEqual(r['summary']['ub_max_hosts_in_cache'], 4674)
        rows = {row['hosts']: row for row in r['hosts']}
        self.assertEqual(rows[192]['roce_bytes'], 64 * 191 * 512 + 8 * 32)
        self.assertEqual(rows[192]['ub_bytes'], 8 * 52 + 191 * 56)
        self.assertEqual(rows[1024]['directory_bytes'], 1048576 * (1023 / 8 + 8))
        many = calculate(apps_per_host=64)
        self.assertEqual(many['summary']['roce_max_hosts_in_cache'], 1)
        setup = {row['endpoints']: row for row in r['setup']}
        self.assertEqual(setup[1024]['roce_objects'], 1048576)
        self.assertAlmostEqual(setup[1024]['roce_serial_s'], 545.25952)
        self.assertAlmostEqual(setup[1024]['roce_parallel_s'], 17.03936)
        self.assertAlmostEqual(setup[1024]['ub_parallel_s'], 0.016320)
        self.assertEqual(setup[1024]['ratio'], 1044.1)

    def test_throughput_cost_and_invalid_inputs(self):
        r = calculate()
        self.assertAlmostEqual(r['throughput']['ub_requests_per_us'], 161.0, places=1)
        self.assertAlmostEqual(r['throughput']['roce_requests_per_us'], 53.67, places=2)
        self.assertAlmostEqual(r['throughput']['ub_GBps_4KiB'], 659.46, places=2)
        self.assertEqual(r['cost']['extra_cold_cycles'], 15)
        self.assertAlmostEqual(r['cost']['extra_cold_ns'], 46.6, places=1)
        self.assertEqual(r['cost']['ub_lut_share'], 0.1408)
        self.assertAlmostEqual(r['ordering']['gating_max_ns'], 155.3, places=1)
        with self.assertRaises(ValueError):
            calculate(qp_bytes=0)
        with self.assertRaises(ValueError):
            calculate(host_counts=[1, 8])
        with self.assertRaises(ValueError):
            calculate(endpoint_counts=[])


if __name__ == '__main__':
    unittest.main()
