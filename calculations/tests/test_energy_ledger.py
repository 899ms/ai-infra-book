from fractions import Fraction as F
import json
import unittest
from _gap_common import ROOT, scenario_rows
from infra_calc.topics.energy_ledger import calculate


class EnergyLedgerTests(unittest.TestCase):
    def test_bytes_come_from_results_and_physics_rows(self):
        r = calculate()
        decode = json.loads((ROOT / 'results/qwen3-8b-decode-b1-s8192.json').read_text())['summary']
        self.assertEqual(r['decode_step']['weight_read_bytes'], decode['weight_read_once_per_operator_bytes'])
        self.assertEqual(r['decode_step']['kv_read_bytes_at_chapter1_context'], decode['kv_bytes_per_token_per_request'] * 2048)
        self.assertEqual(F(r['voltage_scaling']['dynamic_power_ratio_exact']), F(121, 289))
        self.assertEqual(F(r['power_density']['density_ratio_exact']), F(5, 4))
        self.assertEqual(r['rack']['max_cards'], 90)
        self.assertEqual([row['power_kw'] for row in r['rack']['rows']], [88.8, 98.4, 127.2])

    def test_extract_rows_when_present(self):
        r = calculate()
        if not r['sources_extract']['present']:
            self.assertIsNone(r['joules_per_token'])
            return
        levels = r['energy_per_byte']
        self.assertEqual(F(levels['hbm']['pj_per_byte_exact']), F('3.97') * 8)
        self.assertEqual(F(levels['shared_l1']['pj_per_byte_exact']), F(5, 4))
        split = r['joules_per_token']['per_token_split_weights_kv_compute']
        self.assertAlmostEqual(split['weight_joules'], 3.97 * 8 * r['decode_step']['weight_read_bytes'] / 1e12)
        self.assertNotIn('register', levels)
        self.assertNotIn('nic', levels)
        self.assertEqual(r['phone']['x16_channel_gb_per_second'], 21.4)

    def test_missing_extract_leaves_rows_absent(self):
        r = calculate(sources_extract='research/does-not-exist.json')
        self.assertFalse(r['sources_extract']['present'])
        self.assertEqual(r['energy_per_byte'], {})
        self.assertIsNone(r['joules_per_token'])
        self.assertIsNone(r['phone'])

    def test_scenarios(self):
        for row in scenario_rows('energy_ledger'):
            calculate(**row['inputs'], input_sources=row['input_sources'])


if __name__ == '__main__':
    unittest.main()
