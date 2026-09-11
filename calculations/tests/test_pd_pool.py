"""Independent worker assignment enumeration and demand-unit boundaries."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from infra_calc.topics.pd_pool import calculate


# The explicit-rate form is still supported; these tests pin the enumeration with fixed teaching rates.
TEACH=[dict(name='prefill-oriented',count=4,prefill_tokens_per_second=16384,decode_tokens_per_second=64),
       dict(name='decode-oriented',count=4,prefill_tokens_per_second=4096,decode_tokens_per_second=256)]


class PDPoolTests(unittest.TestCase):
    def test_heterogeneous_assignment_against_individual_workers(self):
        r=calculate(workers=TEACH,output_tokens=129);s=r['summary']
        # Enumerate 256 assignments of individual workers, not grouped counts.
        candidates=[]
        for roles in product((0,1),repeat=8):
            p=sum(F(2 if i<4 else 1,1 if i<4 else 2) for i,role in enumerate(roles) if role)
            d=sum(F(1 if i<4 else 2,2 if i<4 else 1) for i,role in enumerate(roles) if not role)
            candidates.append(min(p,d,F(25*10**9,1207959552)))
        self.assertEqual(F(s['best_pd_bound_requests_per_second_exact']),max(candidates))
        self.assertEqual(max(candidates),8)
        self.assertEqual(F(s['colocated_bound_requests_per_second_exact']),F(16,5))
        self.assertEqual(s['best_prefill_workers'],{'prefill-oriented':4,'decode-oriented':0})

    def test_homogeneous_and_network_limited(self):
        workers=[dict(name='same',count=8,prefill_tokens_per_second=8192,decode_tokens_per_second=128)]
        r=calculate(workers=workers,output_tokens=129)['summary']
        self.assertEqual(F(r['best_pd_bound_requests_per_second_exact']),4)
        self.assertEqual(F(r['pd_to_colocated_bound_ratio_exact']),1)
        r=calculate(workers=TEACH,output_tokens=129,network_bytes_per_second=1207959552,arrival_requests_per_second=1)['summary']
        self.assertEqual(F(r['best_pd_bound_requests_per_second_exact']),1)
        self.assertFalse(r['arrival_strictly_below_best_pd_bound'])
        self.assertIn('network',r['best_bottlenecks'])

    def test_first_output_and_cold_destination_prefix(self):
        r=calculate(workers=TEACH,output_tokens=1)['summary']
        self.assertEqual(r['decode_calls_per_request'],0)
        self.assertEqual(r['pd_transfer_bytes_per_request'],0)
        self.assertEqual(F(r['best_pd_bound_requests_per_second_exact']),10)
        self.assertEqual(r['best_decode_workers'],{'prefill-oriented':0,'decode-oriented':0})
        prefix=calculate(workers=TEACH,output_tokens=129,cached_prefix_tokens=6144)
        self.assertEqual(prefix['summary']['new_prefill_tokens_per_request'],2048)
        self.assertEqual(prefix['summary']['pd_transfer_bytes_per_request'],1207959552)
        self.assertEqual(F(prefix['pool_worker_rates'][0]['prefill_service_seconds_exact']),F(1,8))
        for args in ({'output_tokens':0},{'cached_prefix_tokens':8192},{'network_bytes_per_second':0},
                     {'arrival_requests_per_second':float('nan')}):
            with self.assertRaises(ValueError):calculate(**args)

    def test_device_workers_follow_roofline_of_forward_accounting(self):
        # Four A100 80GB SXM and four H20 96GB at 50% of peak; 8192 prompt tokens, 1024 decode calls at batch 32.
        r=calculate();s=r['summary']
        prefill_flops,step_bytes=133594323353600,15137073152+41075343360
        tA=F(prefill_flops)/F(156*10**12);tH=F(prefill_flops)/F(74*10**12)
        dA=1024*F(step_bytes)/F(10195*10**8)/32;dH=1024*F(step_bytes)/F(2048*10**9)/32
        best=max(min(a/tA+h/tH,(4-a)/dA+(4-h)/dH,F(25*10**9,1207959552)) for a in range(5) for h in range(5))
        self.assertEqual(F(s['best_pd_bound_requests_per_second_exact']),best)
        self.assertEqual(s['best_prefill_workers'],{'A100':4,'H20':0})
        self.assertEqual(F(s['colocated_bound_requests_per_second_exact']),4/(tA+dA)+4/(tH+dH))
        rates={d['device']:d for d in r['derived_stage_rates']}
        self.assertEqual((rates['a100-80gb-sxm']['prefill']['bound'],rates['h20-sxm5-96gb']['decode']['bound']),('compute','memory'))
        self.assertTrue(all(d['fits_nominal_capacity'] for d in r['derived_stage_rates']))
