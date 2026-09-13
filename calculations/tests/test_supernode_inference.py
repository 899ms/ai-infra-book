"""Invariants of the section 6.7.4 decode model and its OpenTallas composition rule."""
import importlib.util
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
inf=load('inference','calculations/supernode_inference.py')
SCENARIO=json.loads((ROOT/'calculations/scenarios/supernode-inference-example.json').read_text())

class InferenceModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=SCENARIO;cls.m=inf.load_model(cls.c)
    def test_checkpoint_groups_cover_pinned_payload(self):
        m=self.m
        index=json.loads((ROOT/'calculations/sources/deepseek-v4.1-flash/model.safetensors.index.json').read_text())
        self.assertEqual(sum(m['groups'].values()),index['metadata']['total_size'])
        self.assertEqual(m['replicated_bytes']+m['routed_bytes']+m['engram_bytes']+m['groups']['dspark']+m['groups']['vision'],m['checkpoint_bytes'])
        self.assertAlmostEqual(m['kv_resident_bytes'],890*self.c['context_tokens']+m['kv_resident_bytes']-890*self.c['context_tokens'])
    def test_batch_one_reads_one_expert_per_layer_on_the_critical_path(self):
        c,m=self.c,self.m
        for S in c['supernode_sizes']:
            t=inf.step_time(c,m,S,1)
            self.assertAlmostEqual(t['weight_bytes'],m['replicated_read_bytes']+m['layers']*m['expert_bytes'])
            self.assertEqual(t['sessions_per_card'],1)
        self.assertAlmostEqual(inf.step_time(c,m,256,1)['step_s'],inf.step_time(c,m,8,1)['step_s'],places=4)
    def test_capacity_and_weights_shrink_with_supernode(self):
        c,m=self.c,self.m
        caps=[inf.capacity_sessions(c,m,S) for S in c['supernode_sizes']]
        self.assertEqual([x['weights_per_card_bytes']>y['weights_per_card_bytes'] for x,y in zip(caps,caps[1:])],[True]*3)
        self.assertEqual([x['sessions']<y['sessions'] for x,y in zip(caps,caps[1:])],[True]*3)
        self.assertEqual(caps[0]['weights_per_card_bytes'],m['replicated_bytes']+(m['routed_bytes']+m['engram_bytes'])/8)
    def test_served_rows_respect_capacity_and_tpot(self):
        c,m=self.c,self.m
        for S in c['supernode_sizes']:
            r=inf.evaluate(c,m,S)
            self.assertLessEqual(r['served']['sessions_per_card'],r['sessions'])
            self.assertLessEqual(r['served']['step_s'],c['tpot_s'])
            self.assertAlmostEqual(r['tokens_per_s_per_gpu'],r['served']['sessions_per_card']/r['served']['step_s'])
        rdma=inf.evaluate(c,m,64,remote=c['server_gpus'])
        local=inf.evaluate(c,m,64)
        self.assertGreater(rdma['served']['comm_s'],local['served']['comm_s'])
        self.assertLess(rdma['tokens_per_s_per_gpu'],local['tokens_per_s_per_gpu'])
    def test_opentallas_rule_reproduces_reported_rates(self):
        rom=inf.rom_rows(self.c,self.m)
        for r in rom['rows']:
            self.assertAlmostEqual(1/r['token_s'],r['per_user_tokens_s'],delta=1e-6*r['per_user_tokens_s'])
        hbm,sram=rom['rows'][0],rom['rows'][1]
        self.assertEqual(sram['resident_sessions'],1)
        self.assertGreater(hbm['resident_sessions'],1000)
        self.assertEqual(rom['sram_only_wafers'],12)

if __name__=='__main__':unittest.main()
