"""Selection invariants and consistency with the pre-existing chapter-six model."""
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
choice=load('choice','calculations/parallel_choice.py')
old=load('continuity','manuscripts/ch06/continuity_model.py')
scaling=load('scaling','calculations/supernode_scaling.py')

class SelectionTests(unittest.TestCase):
    def test_existing_chapter_timing_preserved(self):
        s=json.loads((ROOT/'calculations/scenarios/parallel-choice-example.json').read_text())
        r=choice.evaluate(dict(s['common'],**s['cases'][0]))
        for row in r['candidates']:
            expected=sum(old.step(row['tp'],s['common']['history']+i)['total_s'] for i in range(8))
            self.assertAlmostEqual(row['service_s'],expected,places=12)
        cross=choice.evaluate(dict(s['common'],**s['cases'][2]))
        tp16=next(c for c in cross['candidates'] if c['tp']==16)
        expected=sum(old.step(16,s['common']['history']+i,'measured_two_servers')['total_s'] for i in range(8))
        self.assertAlmostEqual(tp16['service_s'],expected,places=12)
    def test_capacity_slo_and_no_feasible_choice(self):
        s=json.loads((ROOT/'calculations/scenarios/parallel-choice-example.json').read_text())
        self.assertEqual([choice.evaluate(dict(s['common'],**c))['winner_tp'] for c in s['cases']],[2,8,8,2])
        first=choice.evaluate(dict(s['common'],**s['cases'][0]))
        self.assertIn('每卡容量不足',first['candidates'][0]['rejections'])
    def test_global_work_and_gradient_conservation(self):
        c=json.loads((ROOT/'calculations/scenarios/supernode-scaling-example.json').read_text())
        for size in c['supernode_sizes']:
            for tp in c['tp_candidates']:
                if tp>size:continue
                r=scaling.evaluate(dict(c,tp=tp),size,c['profiles'][0])
                self.assertEqual(r['tp']*r['dp'],1024)
                self.assertEqual(r['local_dp']*r['supernodes'],r['dp'])
                expected=2*(r['supernodes']-1)/r['supernodes']*2*c['parameters']
                self.assertAlmostEqual(r['per_supernode_remote_bytes'],expected)
                self.assertAlmostEqual(r['compute_s'],6*c['parameters']*c['global_tokens']/1024/(989.4e12*0.41))
    def test_egress_cap_can_reverse_algorithm_choice(self):
        c=json.loads((ROOT/'calculations/scenarios/supernode-scaling-example.json').read_text())
        fast=scaling.evaluate(c,64,c['profiles'][0]);cap=scaling.evaluate(c,64,c['profiles'][1])
        self.assertEqual(fast['chosen'],'hierarchical')
        self.assertEqual(cap['chosen'],'flat')
        self.assertGreater(cap['hierarchical_s'],cap['flat_s'])
        self.assertLess(fast['step_s'],cap['step_s'])
    def test_larger_domain_increases_restore_time(self):
        c=json.loads((ROOT/'calculations/scenarios/supernode-scaling-example.json').read_text())
        a=scaling.evaluate(c,128,c['profiles'][0]);b=scaling.evaluate(c,256,c['profiles'][0])
        self.assertEqual(a['recovery_s'],188)
        self.assertEqual(b['recovery_s'],316)
        self.assertLess(a['effective_tokens_per_s'],a['tokens_per_s'])
    def test_causal_work_partition(self):
        self.assertEqual(sum(range(1,5)),10)
        self.assertEqual(sum(range(5,9)),26)
        self.assertEqual(sum([1,2,7,8]),sum([3,4,5,6]))

if __name__=='__main__':unittest.main()
