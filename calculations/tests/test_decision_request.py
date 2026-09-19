"""Decision-request identities: derived demo tokens, roofline bounds and price ratios."""
from fractions import Fraction as F
from pathlib import Path
import json
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from infra_calc.topics.decision_request import calculate, evidence, LOCK
from infra_calc.models import forward
from infra_calc.schema import Scenario


class DecisionRequestTests(unittest.TestCase):
    def test_demo_tokens_and_published_price(self):
        r = calculate()
        self.assertEqual(r['scenario']['input_tokens'], 1929)
        self.assertEqual(F(r['scenario']['derived_input_tokens_exact']), F('0.000081') / F('0.042') * 10**6)
        self.assertAlmostEqual(r['prices']['jev_usd_per_request'], 1929 * 0.042e-6, places=9)
        self.assertEqual(r['prices']['demo']['cost_ratio'], round(0.013880 / 0.000081, 1))

    def test_decision_path_is_one_compute_bound_forward(self):
        r = calculate()
        d = r['decision_path_dense']
        pre = forward('qwen3-8b', Scenario(tokens=1929, output_head='last'))['summary']
        self.assertEqual(d['matrix_flops'], pre['matrix_flops'] + 7 * d['head_flops_per_position'])
        self.assertEqual(d['bound'], 'compute')
        self.assertEqual(F(d['compute_seconds_exact']), F(d['matrix_flops']) / (F('989.4') * 10**12 * F('0.4')))
        self.assertEqual(d['kv_retained_bytes'], 0)
        self.assertGreater(F(d['compute_seconds_exact']), F(d['memory_seconds_exact']))

    def test_llm_path_adds_serial_decode(self):
        r = calculate(output_tokens=(64,))
        row = r['llm_path_dense'][0]
        d = r['decision_path_dense']
        self.assertEqual(row['decode_steps'], 63)
        self.assertEqual(row['step_bound_batch_1'], 'memory')
        self.assertGreater(row['latency_seconds'], 9 * d['latency_seconds'])
        self.assertLess(row['gpu_seconds_per_request'], 1.5 * d['gpu_seconds_per_request'])
        self.assertGreater(row['gpu_seconds_per_request'], d['gpu_seconds_per_request'])

    def test_v41_ced_path_and_ratios(self):
        r = calculate()
        v = r['decision_path_v41_flash']
        self.assertLess(v['ced']['matrix_flops'], v['reference']['matrix_flops'])
        self.assertGreater(r['prices']['jev_price_over_dense_floor'], 1)
        self.assertGreater(r['prices']['jev_price_over_v41_ced_floor'], 1)
        self.assertLess(r['prices']['jev_price_over_v41_ced_floor'], r['prices']['jev_price_over_dense_floor'])
        share = r['prices']['escalation_share_doubling_cost']['to_demo_llm']
        self.assertAlmostEqual(share, round(r['prices']['jev_usd_per_request'] / 0.013880, 5), places=5)

    def test_lock_and_inputs(self):
        lock = evidence()
        self.assertEqual(json.loads(LOCK.read_text())['declared']['jev']['usd_per_million_input_tokens'], '0.042')
        self.assertEqual(len(lock['files']), 6)
        self.assertTrue(all(not r['file'].endswith('.html') for r in lock['files']))
        with self.assertRaises(ValueError):
            calculate(output_tokens=(1,))
        with self.assertRaises(ValueError):
            calculate(compute_efficiency='1.5')
        self.assertEqual(calculate(input_tokens=8192)['scenario']['input_tokens'], 8192)


if __name__ == '__main__':
    unittest.main()
