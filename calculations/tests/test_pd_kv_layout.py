from fractions import Fraction as F
import unittest
from _gap_common import BOOK
from infra_calc.topics import pd_pool, pd_af_handoff, kv_comparison


class KVLayoutTests(unittest.TestCase):
    def test_per_token_units(self):
        self.assertEqual(kv_comparison.per_token_bytes('qwen3-8b', 'gqa'), 144 * 1024)
        self.assertEqual(kv_comparison.per_token_bytes('deepseek-v3', 'mla'), 61 * (512 + 64) * 2)
        rows = {(r['model'], r['layout']): r for r in kv_comparison.calculate(8192)['rows']}
        self.assertEqual(F(rows[('deepseek-v3', 'BF16 compact MLA')]['global_growth_bytes_per_token_per_request']), 61 * 576 * 2)
        extra = kv_comparison.mla_compact_extra_flops_per_token()
        self.assertEqual(extra['extra_flops_per_token'], 61 * 128 * 2 * (128 * 512 + 512 * 128))
        with self.assertRaises(ValueError):
            kv_comparison.per_token_bytes('qwen3-8b', 'mla')

    def test_pd_pool_and_handoff_layouts(self):
        gqa, mla = pd_pool.calculate(), pd_pool.calculate(kv_layout='mla')
        self.assertEqual(gqa['summary']['pd_transfer_bytes_per_request'], 8192 * 144 * 1024)
        self.assertEqual(mla['summary']['pd_transfer_bytes_per_request'], 8192 * 70272)
        self.assertEqual(F(mla['summary']['network_capacity_requests_per_second_exact']), F(25 * 10**9, 8192 * 70272))
        for bw in (25 * 10**9, 50 * 10**9):
            g = pd_af_handoff.calculate(model='qwen3-8b', network_bandwidth=bw)['summary']
            x = pd_af_handoff.calculate(model='qwen3-8b', network_bandwidth=bw, kv_layout='mla')
            s = x['summary']
            self.assertEqual(s['af_total_bytes'], g['af_total_bytes'])
            self.assertEqual(F(s['pd_serialized_ns_exact']), F(8192 * 70272 * 10**9, bw) + 5000)
            self.assertEqual(x['mla_compact_path']['extra_flops_per_step'], 2046820352)
            if x['mla_compact_path']['expanded_path_reference']:
                self.assertTrue(x['mla_compact_path']['expanded_path_reference']['equals_compact_extra_per_layer'])
        self.assertEqual(pd_af_handoff.calculate(model='qwen3-8b'), pd_af_handoff.calculate(model='qwen3-8b', kv_layout='gqa'))

    def test_scenario_rows_exist(self):
        self.assertIn('pd-pool-mla', {r['id'] for r in BOOK['pd_pool']})
        self.assertIn('pd-af-handoff-qwen8-mla-50gbps', {r['id'] for r in BOOK['pd_af_handoff']})


if __name__ == '__main__':
    unittest.main()
