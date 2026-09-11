import unittest
from _gap_common import BOOK
from infra_calc.topics import training_pipeline_schedule as m


class ExtendedScheduleTests(unittest.TestCase):
    def invariant(self, r):
        events = {e['id']: e for e in r['events']}
        for event in events.values():
            for dep in event['dependencies']:
                self.assertLessEqual(events[dep]['end'], event['start'] + 1e-12)
        for resource in {e['resource'] for e in events.values()}:
            seq = sorted((e for e in events.values() if e['resource'] == resource and e['duration'] > 0), key=lambda e: e['start'])
            for a, b in zip(seq, seq[1:]):
                self.assertLessEqual(a['end'], b['start'] + 1e-12)
        for timeline in r['activation_timelines']:
            if timeline['events']:
                self.assertEqual(timeline['events'][-1]['live_bytes'], 0)

    def test_work_groups_match_base_partition(self):
        a, _, _ = m._work(1, 4, 'save_nonlinear')
        b, _, _ = m._work_groups(1, 4, 'save_nonlinear', [list(range(9 * s, 9 * s + 9)) for s in range(4)])
        for x, y in zip(a, b):
            for key in ('forward_matrix_flops', 'backward_matrix_flops', 'forward_scalar_flops', 'backward_scalar_flops', 'parameters', 'nonlinear_saved_bytes_per_microbatch'):
                self.assertEqual(x[key], y[key])

    def test_policies_conserve_work_and_beat_or_match_1f1b(self):
        base = m.calculate(policy='1f1b', microbatches=8, tokens=4)
        for policy in ('interleaved_1f1b', 'zero_bubble', 'dualpipe'):
            r = m.calculate(policy=policy, microbatches=8, tokens=4)
            self.invariant(r)
            self.assertEqual(r['work']['all_microbatches_forward_matrix_flops'], base['work']['all_microbatches_forward_matrix_flops'])
            self.assertEqual(r['work']['total_parameters'], base['work']['total_parameters'])
            self.assertAlmostEqual(r['summary']['useful_forward_backward_device_seconds'], base['summary']['useful_forward_backward_device_seconds'])
            self.assertLess(r['summary']['step_makespan_seconds'], base['summary']['step_makespan_seconds'])
            self.assertIn('declared_schedule_rule', r)
            self.assertEqual(r, m.calculate(**r['scenario']))
        inter = m.calculate(policy='interleaved_1f1b', microbatches=8, tokens=4)
        self.assertEqual(inter['transfers']['forward_messages'], 7 * 8)
        self.assertEqual(len(inter['partition']['virtual_stages']), 8)
        self.assertEqual(sum(len(v['layers']) for v in inter['partition']['virtual_stages']), 36)
        dual = m.calculate(policy='dualpipe', microbatches=8, tokens=4)
        self.assertEqual(dual['partition']['parameter_copies_per_gpu'], 2)
        self.assertEqual(dual['transfers']['forward_messages'], 3 * 8)

    def test_zero_bubble_reproduces_zb_h1(self):
        # zero-bubble.txt Figure 3 (top), p=4, m=8: device g places W_i right after B_(i+g).
        paper = [
            'F1 F2 F3 F4 B1 W1 F5 B2 W2 F6 B3 W3 F7 B4 W4 F8 B5 W5 B6 W6 B7 W7 B8 W8',
            'F1 F2 F3 B1 F4 B2 W1 F5 B3 W2 F6 B4 W3 F7 B5 W4 F8 B6 W5 B7 W6 B8 W7 W8',
            'F1 F2 B1 F3 B2 F4 B3 W1 F5 B4 W2 F6 B5 W3 F7 B6 W4 F8 B7 W5 B8 W6 W7 W8',
            'F1 B1 F2 B2 F3 B3 F4 B4 W1 F5 B5 W2 F6 B6 W3 F7 B7 W4 F8 B8 W5 W6 W7 W8',
        ]
        r = m.calculate(policy='zero_bubble', microbatches=8, tokens=4)
        for g in range(4):
            order = ' '.join(f"{'B' if x['kind'] == 'X' else x['kind']}{x['microbatch'] + 1}" for x in r['stage_orders'][f'gpu{g}:direction0'])
            self.assertEqual(order, paper[g])
        base = m.calculate(policy='1f1b', microbatches=8, tokens=4)
        s = r['summary']
        # T_F = 10 ms, T_B (dX) = T_W (dW) = 10 ms: ZB-H1 bound 3 x 10 ms, ZB-H2 bound 0.
        self.assertAlmostEqual(s['bubble_bound_zb_h1_seconds'], 0.03)
        self.assertAlmostEqual(s['bubble_bound_zb_h2_seconds'], 0.0)
        self.assertAlmostEqual(s['bubble_bound_1f1b_seconds'], 0.09)
        self.assertAlmostEqual(s['bubble_bound_policy_seconds'], 0.03)
        for stage in r['stages']:
            self.assertAlmostEqual(stage['idle_zero_transfer_counterfactual_seconds'], 0.03)
            self.assertAlmostEqual(stage['bubble_bound_zb_h1_seconds'], 0.03)
            self.assertLess(stage['idle_during_training_seconds'], 0.045)
            self.assertLess(stage['idle_during_training_seconds'], base['stages'][stage['stage']]['idle_during_training_seconds'])
        self.assertAlmostEqual(s['step_makespan_seconds'], 0.283)
        self.assertLess(s['step_makespan_seconds'], base['summary']['step_makespan_seconds'])
        # ZB-H1 keeps the first stage's peak equal to 1F1B (p microbatches in flight).
        self.assertEqual(s['reserved_activation_scope_peak_bytes'][0], base['summary']['reserved_activation_scope_peak_bytes'][0])
        self.assertIn('Figure 3', r['declared_schedule_rule'])
        r16 = m.calculate(policy='zero_bubble', microbatches=16, tokens=4)
        self.assertAlmostEqual(r16['summary']['step_makespan_seconds'], 0.523)
        self.assertAlmostEqual(r16['stages'][0]['idle_zero_transfer_counterfactual_seconds'], 0.03)

    def test_bubble_bounds_for_other_policies(self):
        inter = m.calculate(policy='interleaved_1f1b', microbatches=8, tokens=4, virtual_stages=2)
        self.assertAlmostEqual(inter['summary']['bubble_bound_interleaved_fraction'], (1 / 2) * 3 / 8)
        self.assertAlmostEqual(inter['summary']['bubble_bound_interleaved_seconds'], 0.045)
        self.assertAlmostEqual(inter['summary']['bubble_bound_policy_seconds'], 0.045)
        self.assertAlmostEqual(inter['summary']['bubble_bound_zb_h1_seconds'], 0.03)
        self.assertIsNone(inter['summary']['bubble_bound_dualpipe_seconds'])
        dual = m.calculate(policy='dualpipe', microbatches=8, tokens=4)
        # DeepSeek-V3 Table 2: (PP/2-1)(F&B + B - 3W) with F&B = F + B, B = 20 ms, W = 10 ms.
        self.assertAlmostEqual(dual['summary']['bubble_bound_dualpipe_seconds'], (4 / 2 - 1) * (0.03 + 0.02 - 0.03))
        self.assertAlmostEqual(dual['summary']['bubble_bound_policy_seconds'], 0.02)
        self.assertIsNone(dual['summary']['bubble_bound_interleaved_seconds'])
        # interleaved and dualpipe schedules are unchanged by the ZB-H1 fix.
        self.assertAlmostEqual(inter['summary']['step_makespan_seconds'], 0.297666667)
        self.assertAlmostEqual(dual['summary']['step_makespan_seconds'], 0.306)

    def test_validation(self):
        with self.assertRaises(ValueError):
            m.calculate(policy='dualpipe', microbatches=7, tokens=4)
        with self.assertRaises(ValueError):
            m.calculate(policy='interleaved_1f1b', microbatches=6, tokens=4)
        with self.assertRaises(ValueError):
            m.calculate(policy='zero_bubble', declared_weight_backward_fraction='1', tokens=4)

    def test_scenario_rows_exist(self):
        ids = {row['id'] for row in BOOK['training_pipeline_schedule']}
        for name in ('training-pipeline-interleaved-m8', 'training-pipeline-zero-bubble-m8', 'training-pipeline-dualpipe-m8'):
            self.assertIn(name, ids)


if __name__ == '__main__':
    unittest.main()
