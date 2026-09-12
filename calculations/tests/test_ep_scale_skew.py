"""Hand-checkable invariants for the chapter-nine EP-size skew sweep."""
import importlib.util
import json
import random
from fractions import Fraction
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('ep_scale_skew', ROOT/'calculations/ep_scale_skew.py')
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class EPScaleSkewTest(unittest.TestCase):
    def setUp(self):
        self.scenario=json.loads((ROOT/'calculations/scenarios/ep-scale-skew-example.json').read_text())
    def test_hot_expert_exact(self):
        # One expert per card: the busiest card is the hot expert alone, 128 rows against a mean of 32.
        self.assertEqual(module.hot_case(self.scenario,256)['ratio'],4)
        # EP8: 128 + 31 * 8064/255 rows against a mean of 1024.
        self.assertEqual(module.hot_case(self.scenario,8)['busiest_rows'],128+31*Fraction(8064,255))
    def test_hot_ratio_grows_with_ep(self):
        ratios=[module.hot_case(self.scenario,ep)['ratio'] for ep in self.scenario['ep_sizes']]
        self.assertEqual(ratios,sorted(ratios))
    def test_random_ratio_grows_with_ep(self):
        small=dict(self.scenario,trials=40)
        r=module.random_ratios(small,random.Random(small['seed']))
        means=[r[ep]['mean_ratio'] for ep in small['ep_sizes']]
        self.assertTrue(all(m>1 for m in means))
        self.assertLess(means[0],means[-1])


if __name__=='__main__':
    unittest.main()
