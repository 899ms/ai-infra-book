import unittest
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from infra_calc import hardware
from infra_calc.sources import read_source
from infra_calc.topics.training_deadline import calculate


class H20EvidenceTests(unittest.TestCase):
    def test_named_capacity_not_vgpu_framebuffer(self):
        raw=read_source('sources/hardware/nvidia-h20-vgpu-release7.md')
        text=raw.decode() if isinstance(raw,bytes) else raw
        for size in (96,141):
            self.assertIn(f'NVIDIA H20 SXM5 {size}GB',text)
            device=hardware.select_device(f'h20-sxm5-{size}gb')
            self.assertEqual(device['memory']['nominal_capacity'],size)
        # 96 GB peaks come from the MegaScale-Infer paper table, not from another H20 capacity or generation.
        small=hardware.select_device('h20-sxm5-96gb')
        self.assertEqual(small['memory']['bandwidth_bytes_per_second'],4096e9)
        self.assertEqual(small['memory']['bandwidth_evidence']['source_id'],'megascale-infer')
        peak=hardware.select_peak(small,'BF16','FP32','tensor','dense')
        self.assertEqual((peak['tera_ops_per_second'],peak['source_id']),(148,'megascale-infer'))
        self.assertEqual(len(small['peak_rates']),1)
        large=hardware.select_device('h20-sxm5-141gb')
        self.assertIsNone(large['memory']['bandwidth_bytes_per_second'])
        self.assertEqual(large['peak_rates'],[])
        with self.assertRaises(ValueError):hardware.select_peak(large,'BF16','FP32','tensor','dense')

    def test_capacity_available_without_compute_substitution(self):
        r=calculate(devices=['h20-sxm5-96gb','h20-sxm5-141gb'])
        self.assertEqual([x['device'] for x in r['training_deadline_rows']],['h20-sxm5-96gb']*len(r['training_deadline_rows']))
        self.assertEqual([x['capacity_bound_devices'] for x in r['training_deadline_devices']],[2,1])
