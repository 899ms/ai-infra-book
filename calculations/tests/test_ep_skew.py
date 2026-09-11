"""Conservation and bottleneck invariants for the chapter-nine EP model."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('ep_skew', ROOT/'calculations/ep_skew.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EPSkewTest(unittest.TestCase):
    def setUp(self):
        self.scenario=json.loads((ROOT/'calculations/scenarios/ep-skew-example.json').read_text())
    def case(self,i):
        return dict(self.scenario['common'],**self.scenario['cases'][i])
    def test_conservation_and_hotspot(self):
        balanced,hot=[module.evaluate(self.case(i)) for i in (0,1)]
        self.assertEqual(sum(hot['expert_assignments']),8192)
        self.assertEqual(hot['dispatch']['total_bytes'],64*2**20)
        self.assertEqual(hot['dispatch']['total_bytes'],balanced['dispatch']['total_bytes'])
        self.assertEqual(hot['combine']['total_bytes'],hot['dispatch']['total_bytes'])
        self.assertAlmostEqual(hot['barrier_lower_s']/balanced['barrier_lower_s'],2.5)
    def test_transpose_reverses_endpoint_bottleneck(self):
        r=module.evaluate(self.case(1))
        self.assertEqual(r['dispatch']['receive_s'],r['combine']['send_s'])
        self.assertEqual(r['dispatch']['send_s'],r['combine']['receive_s'])
        self.assertGreater(r['dispatch']['receive_s'],r['dispatch']['send_s'])
    def test_cut_survives_rebalancing_and_faster_endpoints(self):
        case=self.case(2); original=module.evaluate(case)
        case['endpoint_Bps']*=100
        faster=module.evaluate(case)
        self.assertEqual(original['dispatch']['lower_s'],64*2**20/25e9)
        self.assertEqual(faster['barrier_lower_s'],original['barrier_lower_s'])
    def test_fp8_does_not_speed_up_combine_or_compute(self):
        hot,fp8=[module.evaluate(self.case(i)) for i in (1,3)]
        self.assertEqual(fp8['dispatch']['lower_s']*2,hot['dispatch']['lower_s'])
        self.assertEqual(fp8['compute_s'],hot['compute_s'])
        self.assertEqual(fp8['combine'],hot['combine'])
    def test_rectangular_pool(self):
        case=self.case(0);case['assignments']=[[1024]*4,[1024]*4]
        r=module.evaluate(case)
        self.assertEqual(r['expert_skew'],1)
        self.assertGreater(r['dispatch']['send_s'],r['dispatch']['receive_s'])
    def test_invalid_workloads_rejected(self):
        for matrix in ([],[[1],[]],[[-1]*4]*4,[[0]*4]*4,[[512.0]*4]*4):
            case=self.case(0);case['assignments']=matrix
            with self.assertRaises(ValueError):module.evaluate(case)


if __name__=='__main__':unittest.main()
