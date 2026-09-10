"""Independent checkpoint sums, explicit pair masks and schedule boundaries."""
import json
from math import prod
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from infra_calc.topics import v41_forward as v, v41_flash
from infra_calc.sources import model_config


class ForwardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=model_config(v.MODEL)['text_config']

    def test_all_parameter_components_conserve_checkpoint(self):
        tensors,parts,checkpoint=v.parameter_inventory()
        self.assertEqual(sum(parts.values()),748494684784)
        self.assertEqual(parts['engram'],196928504320)
        self.assertEqual(parts['routed_experts'],40*384*3*5120*2304)
        self.assertEqual(sum(prod(s) for s in tensors.values()),sum(parts.values()))

    def test_dense_projection_work_from_checkpoint_not_adapter_rows(self):
        # At N=2 every indexer is active. Weight sums independently recover
        # every executed linear/einsum projection, including grouped wo_a.
        r=v.calculate(tokens=2,execution='reference');tensors,_,_=v.parameter_inventory()
        expected=0
        for name,shape in tensors.items():
            if len(shape)!=2 or name=='embed.weight' or ('.engram.' in name and not name.endswith('wkv.weight')):
                continue
            rows=1 if name=='head.weight' else 2
            if '.ffn.experts.' in name:rows=2*6/384
            if '.indexer.wk.' in name:
                layer=int(name.split('.')[1]);rows=2//self.c['compress_ratios'][layer]
            expected += prod(shape)*rows*2
        interactions=r['summary']['context_interaction_flops']
        self.assertEqual(r['summary']['matrix_flops']-interactions,int(expected))

    def test_explicit_causal_mask_and_rectangle(self):
        for n in (1,2,3,7,129):
            r=v.calculate(tokens=n,execution='reference')
            main=0;index=0
            for layer in range(40):
                ratio=self.c['compress_ratios'][layer]
                for query in range(n):
                    window=[k for k in range(n) if 0<=query-k<128]
                    keys=[k for k in range(n//ratio) if (k+1)*ratio<=query+1] if ratio else []
                    main += 4*64*512*(len(window)+min(len(keys),512))
                if layer in self.c['index_source_layer_ids']:
                    index += 2*32*128*n*(n//ratio)
            self.assertEqual(r['summary']['context_interaction_flops'],main+index)

    def test_ced_replay_and_global_projection(self):
        for n in (1,127,128,129,8192):
            r=v.calculate(tokens=n);rows=r['layer_schedule']
            self.assertEqual([x['query_tokens'] for x in rows[:20]],[n]*20)
            self.assertEqual([x['query_tokens'] for x in rows[20:]],[min(n,128)]*20)
            self.assertEqual(rows[20]['global_projection_tokens'],n)
            self.assertEqual(rows[20]['new_global_entries'],n)
            prior=v41_flash.calculate(length=n)['expert_work']
            s=r['summary']['matrix_components']
            self.assertEqual(s['shared_expert']+s['routed_expert'],prior['ced_bounded_replay_prefill_expert_matrix_flops'])
            window=next(o for o in r['operations'] if o['name']=='layers.20.attn.qk_pv')['window_pairs_per_request']
            tail=min(n,128);self.assertEqual(window,tail*(tail+1)//2)

    def test_short_ced_equal_reference_when_index_algorithm_equal(self):
        for n in (1,2,128):
            a=v.calculate(tokens=n,execution='reference',index_algorithm='candidate')
            b=v.calculate(tokens=n,execution='ced',index_algorithm='candidate')
            self.assertEqual(a['summary']['matrix_flops'],b['summary']['matrix_flops'])
        a=v.calculate(tokens=129,execution='reference',index_algorithm='candidate')
        b=v.calculate(tokens=129,execution='ced',index_algorithm='candidate')
        self.assertLess(b['summary']['matrix_flops'],a['summary']['matrix_flops'])

    def test_decode_compressor_boundaries_and_index_cap(self):
        for history in (1,2,127,128,8191,8192,204800):
            r=v.calculate(tokens=1,history=history)
            layer=r['layer_schedule'][2]
            self.assertEqual(layer['new_global_entries'],(history+1)//2-history//2)
            scan=next(o for o in r['operations'] if o['name']=='layers.24.attn.index_dot')
            self.assertEqual(scan['index_pairs_per_request'],min(history+1,16384))
            self.assertEqual(r['summary']['matrix_components']['shared_expert']+r['summary']['matrix_components']['routed_expert'],v41_flash.calculate(length=history)['expert_work']['decode_expert_matrix_flops'])

    def test_cache_shared_owners_and_fixed_buffers(self):
        for n in (0,1,2,127,128,8192):
            r=v.state(n);s=r['components']
            self.assertEqual(s['global_main_bytes']+s['global_index_bytes'],(3*(n//2)+n)*(512+128)*2)
            self.assertEqual(s['compressor_fp32_bytes'],3*2*2*512*4)
            self.assertEqual(s['window_bytes'],40*min(n,128)*512*2)
            self.assertEqual(s['engram_token_ids_bytes'],n*8)
            p=v.state(n,layout='production')['components']
            self.assertEqual(p['global_main_bytes']+p['global_index_bytes'],(3*(n//2)+n)*356)
            if n:self.assertEqual(p['global_main_bytes']+p['global_index_bytes'],v41_flash.calculate(length=n)['global_cache']['bytes'])

    def test_batch_scaling_and_sums(self):
        a=v.calculate(tokens=129);b=v.calculate(tokens=129,batch=3)
        self.assertEqual(b['summary']['matrix_flops'],3*a['summary']['matrix_flops'])
        self.assertEqual(b['state_after']['resident_bytes'],3*a['state_after']['resident_bytes'])
        self.assertEqual(sum(o['matrix_flops'] for o in a['operations']),a['summary']['matrix_flops'])

    def test_one_million_exact_endpoint(self):
        r=v.calculate(tokens=1,history=1048575)
        self.assertEqual(r['state_after']['length'],1048576)
        self.assertEqual(r['layer_schedule'][2]['new_global_entries'],1)
        self.assertEqual(r['layer_schedule'][20]['new_global_entries'],1)
        with self.assertRaises(ValueError):v.calculate(tokens=1,history=1048576)

    def test_input_validation(self):
        for kwargs in ({'tokens':True},{'batch':0},{'history':-1},{'tokens':2,'history':1},{'execution':'v4'},{'tokens':1048577},{'index_algorithm':'dense'}):
            with self.assertRaises(ValueError):v.calculate(**kwargs)


if __name__=='__main__':unittest.main()
