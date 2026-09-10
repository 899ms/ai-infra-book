"""Release anchors and cross-adapter invariants for storage versus decode IO."""
import json
import sys
import unittest
from fractions import Fraction
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from infra_calc.topics import kv_comparison, v41_flash, state
from infra_calc.cli import model_list
from infra_calc.sources import model_config


class CacheComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=kv_comparison.calculate()
        cls.rows={(x['model'],x['layout']):x for x in cls.r['rows']}

    def test_release_cache_anchors(self):
        v4=self.rows['deepseek-v4-flash','FP8/BF16 main + MXFP4 index']
        v41=self.rows['deepseek-v4.1-flash','FP4 global + FP8 SWA + MXFP4 index']
        self.assertEqual(Fraction(v4['global_growth_bytes_per_token_per_request']),Fraction(14057,4))
        self.assertEqual(v41['global_history_bytes'],8192*890)
        self.assertEqual(v41['local_window_bytes'],40*128*528)
        self.assertNotEqual(v41['decode_selected_history_read_bytes'],v41['global_history_bytes'])

    def test_gqa_existing_adapter(self):
        for m in ('qwen3-8b','qwen3-32b','qwen3-30b-a3b','qwen3-235b-a22b'):
            old=state.calculate(m,8192)['summary']; r=self.rows[m,'BF16 GQA']
            self.assertEqual(r['global_history_bytes'],old['resident_bytes'])
            self.assertEqual(r['decode_selected_history_read_bytes'],old['selected_history_payload_bytes'])

    def test_v4_reference_adapter(self):
        for m in ('deepseek-v4-flash','deepseek-v4-pro'):
            old=state.calculate(m,8192)['summary']; r=self.rows[m,'BF16 reference']
            self.assertEqual(r['accounted_resident_bytes'],old['history_resident_bytes'])
            self.assertEqual(r['decode_selected_history_read_bytes'],old['selected_history_payload_bytes'])

    def test_compression_boundaries_and_window_overwrite(self):
        for n in (1,127,128,8191,8192):
            a=kv_comparison.calculate(n)['rows']; b=kv_comparison.calculate(n+1)['rows']
            for x,y in zip(a,b):
                self.assertEqual(y['accounted_resident_bytes']-x['accounted_resident_bytes'],x['next_token_resident_growth_bytes'])
                self.assertGreaterEqual(x['next_token_cache_write_bytes'],x['next_token_resident_growth_bytes'])

    def test_kda_fixed_state_not_token_growth(self):
        r=self.rows['kimi-k3','BF16 compact MLA + FP32 KDA']
        self.assertEqual(r['global_history_bytes'],24*(512+64)*2*8192)
        self.assertGreater(r['recurrent_state_bytes'],0)
        self.assertEqual(r['decode_recurrent_read_bytes'],r['decode_recurrent_write_bytes'])
        self.assertEqual(r['next_token_resident_growth_bytes'],27648)

    def test_batch_scaling(self):
        for x,y in zip(self.r['rows'],kv_comparison.calculate(batch=3)['rows']):
            for k in x:
                if k.endswith('_bytes'):self.assertEqual(y[k],3*x[k],k)
            self.assertEqual(x['global_growth_bytes_per_token_per_request'],y['global_growth_bytes_per_token_per_request'])

    def test_hierarchical_index_cap(self):
        n=131072; x=kv_comparison.calculate(n)['rows'][-1]
        self.assertEqual(x['decode_index_history_read_bytes'],(3*(n//2)+n+4*16384)*68)
        self.assertEqual(x['decode_main_history_read_bytes'],40*128*528+38*512*288)

    def test_limits(self):
        for n in (0,-1,True):
            with self.assertRaises(ValueError):kv_comparison.calculate(n)
        skipped=kv_comparison.calculate(1048576)['skipped']
        self.assertIn('qwen3-8b',[x['model'] for x in skipped])
        with self.assertRaises(ValueError):v41_flash.calculate(1048577)

    def test_registry_scope(self):
        r=next(x for x in model_list() if x['model']==v41_flash.MODEL)
        self.assertIn('v41-flash',r['stage_calculations'])
        self.assertEqual(r['forward'],'pending')


class CheckpointTests(unittest.TestCase):
    def test_complete_checkpoint_and_engram(self):
        r=v41_flash.checkpoint()
        self.assertEqual(r['shards'],48)
        self.assertEqual(r['tensors'],96085)
        self.assertEqual(r['tensor_payload_bytes'],510286023000)
        self.assertEqual(r['logical_parameters_by_component']['backbone'],551566180464)
        self.assertEqual(r['logical_parameters_by_component']['engram'],196928504320)

    def test_config_shape_mismatch_rejected(self):
        config=model_config(v41_flash.MODEL)
        config['text_config']['moe_intermediate_size']+=32
        with patch.object(v41_flash,'model_config',return_value=config):
            with self.assertRaisesRegex(ValueError,'Expert shape'):v41_flash.checkpoint()


if __name__=='__main__':unittest.main()
