"""Prewritten hand oracles for shared transport and useful business delivery.

Small declared wire units isolate mechanisms; these are not QUIC packet layouts.
"""
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from infra_calc.topics import shared_media_transport as candidate


def packet(pid, stream=None, size=1, offset=0, direction='c2s', **kwargs):
    return dict(id=pid, stream=stream or pid, payload_bytes=size, offset=offset,
                direction=direction, **kwargs)


def inputs(packets):
    return dict(
        scheduler='fifo', delivery_mode='per_stream',
        c2s_bits_per_second=8, s2c_bits_per_second=8,
        c2s_propagation_seconds=1, s2c_propagation_seconds=1,
        header_bytes=0, ack_bytes=1, shared_credit_bytes=100,
        reliable_receive_credit_bytes=100, stream_credit_bytes=100,
        packets=packets, tasks=[], businesses=[],
    )


def hol_inputs():
    return inputs([
        packet('B0', 'image', drop_first=True, recovery_ready=5),
        packet('A0', 'audio', deadline=4),
        packet('B1', 'image', offset=1),
    ])


def state(result, pid):
    return next(p for p in result['packets'] if p['id'] == pid)


def at(result, pid):
    value = state(result, pid)['delivered']
    return F(value) if value is not None else None


class SharedMediaTransportTests(unittest.TestCase):
    def test_same_wire_hol_changes_audio_delivery_but_not_full_image(self):
        p = hol_inputs()
        independent = candidate.calculate(p)
        p['delivery_mode'] = 'connection'
        ordered = candidate.calculate(p)
        self.assertEqual(independent['transmissions'], ordered['transmissions'])
        self.assertEqual((at(independent, 'A0'), at(ordered, 'A0')), (3, 7))
        self.assertEqual((at(independent, 'B1'), at(ordered, 'B1')), (7, 7))
        self.assertTrue(state(independent, 'A0')['deadline_met'])
        self.assertFalse(state(ordered, 'A0')['deadline_met'])
        self.assertEqual(independent['summary']['data_wire_bytes'], 4)
        self.assertEqual(independent['summary']['unique_received_payload_bytes'], 3)
        retries = [t for t in independent['transmissions']
                   if t['kind'] == 'data' and t['packet'] == 'B0']
        self.assertEqual([t['attempt'] for t in retries], [1, 2])
        self.assertEqual([(t['offset'], t['end_offset']) for t in retries], [(0, 1)] * 2)

    def test_priority_uses_same_packets_and_cannot_preempt_started_work(self):
        p = inputs([packet(f'B{i}', 'image', offset=i) for i in range(4)]
                   + [packet('A', ready=1, priority=10)])
        fifo = candidate.calculate(p)
        p['scheduler'] = 'priority'
        priority = candidate.calculate(p)
        self.assertEqual((at(fifo, 'B3'), at(fifo, 'A')), (5, 6))
        self.assertEqual((at(priority, 'B3'), at(priority, 'A')), (6, 3))
        self.assertEqual(fifo['summary']['data_wire_bytes'], 5)
        self.assertEqual(priority['summary']['data_wire_bytes'], 5)
        p = inputs([packet('bulk', size=4), packet('A', ready=1, priority=10)])
        p['scheduler'] = 'priority'
        self.assertEqual(at(candidate.calculate(p), 'A'), 6)

    def test_shared_credit_waits_for_reverse_ack_across_one_or_three_streams(self):
        for split in (False, True):
            with self.subTest(split=split):
                p = inputs([packet(str(i), str(i) if split else 'one',
                                   offset=0 if split else i) for i in range(3)])
                p['shared_credit_bytes'] = 2
                r = candidate.calculate(p)
                data = [t for t in r['transmissions'] if t['kind'] == 'data']
                ack = [t for t in r['transmissions'] if t['kind'] == 'ack']
                self.assertEqual([F(t['start']) for t in data], [0, 1, 4])
                self.assertEqual([F(t['arrival']) for t in data], [2, 3, 6])
                self.assertEqual([F(t['arrival']) for t in ack][:2], [4, 5])
                self.assertEqual(r['summary']['shared_outstanding_bytes'], {'c2s': 0, 's2c': 0})

    def test_unreliable_data_bypasses_receive_credit_but_not_shared_credit(self):
        p = inputs([packet('media', size=2, reliable=False), packet('image')])
        p.update(shared_credit_bytes=2, reliable_receive_credit_bytes=1, stream_credit_bytes=1)
        r = candidate.calculate(p)
        self.assertEqual(at(r, 'media'), 3)
        image = next(t for t in r['transmissions'] if t['kind'] == 'data' and t['packet'] == 'image')
        self.assertEqual(F(image['start']), 5)
        p['packets'][0]['drop_first'] = True
        r = candidate.calculate(p)
        self.assertEqual(state(r, 'image')['attempts'], 0)
        self.assertEqual(r['summary']['shared_outstanding_bytes']['c2s'], 2)
        self.assertIn('image', r['unfinished'])
        # With enough shared credit, a lost datagram cannot block a reliable
        # stream through a fictitious connection-wide receive prefix.
        p['shared_credit_bytes'] = 100
        p['delivery_mode'] = 'connection'
        self.assertEqual(at(candidate.calculate(p), 'image'), 4)

    def test_playback_stall_is_distinct_from_fixed_slot_missing_audio(self):
        p = inputs([packet(str(i), 'voice', offset=i, ready=t)
                    for i, t in enumerate((1, 4, 5))])
        p['businesses'] = [dict(id='voice', kind='tts', playback='reliable', blocks=[
            dict(packets=[str(i)], duration=2, slot_start=3 + 2*i) for i in range(3)
        ])]
        voice = candidate.calculate(p)['businesses'][0]
        self.assertEqual([(F(b['start']), F(b['end'])) for b in voice['blocks']],
                         [(3, 5), (6, 8), (8, 10)])
        self.assertEqual(F(voice['stall_seconds']), 1)
        self.assertTrue(voice['complete_playback'])
        p['businesses'][0]['playback'] = 'slots'
        voice = candidate.calculate(p)['businesses'][0]
        self.assertEqual([b['played'] for b in voice['blocks']], [True, False, True])
        self.assertEqual((F(voice['missing_seconds']), F(voice['playback_end'])), (2, 9))
        self.assertFalse(voice['complete_playback'])
        for deadline, expected in ((2, 2), ('199/100', None)):
            q = inputs([packet('a', reliable=False, allow_expire=True, deadline=deadline)])
            r = candidate.calculate(q)
            self.assertEqual(at(r, 'a'), expected)
            self.assertEqual(r['summary']['data_wire_bytes'], 1)

    def test_full_image_requires_all_input_then_model_then_shared_response_link(self):
        p = hol_inputs()
        p['tasks'] = [dict(id='model', dependencies=['B0', 'B1'], duration=2)]
        p['packets'].append(packet('final', size=2, direction='s2c', dependencies=['model']))
        p['businesses'] = [dict(id='image', kind='image', required=['final'])]
        r = candidate.calculate(p)
        self.assertEqual([(F(w['start']), F(w['end'])) for w in r['work']], [(7, 9)])
        self.assertEqual(F(r['businesses'][0]['complete']), 12)
        reverse = sorted((F(t['start']), F(t['end']))
                         for t in r['transmissions'] if t['direction'] == 's2c')
        self.assertTrue(all(a[1] <= b[0] for a, b in zip(reverse, reverse[1:])))

    def test_cancel_requires_ordered_delivery_and_only_informs_receiver(self):
        for mode, cancel_at, jobs in (('connection', 7, 1), ('per_stream', 3, 0)):
            with self.subTest(mode=mode):
                p = hol_inputs()
                p['delivery_mode'] = mode
                p['packets'][1]['cancel_targets'] = ['job']
                p['tasks'] = [dict(id='job', duration=2, ready=4, cancel_tag='job')]
                r = candidate.calculate(p)
                self.assertEqual(F(r['cancellations'][0]['at']), cancel_at)
                self.assertEqual(len(r['work']), jobs)
        p = inputs([packet('cancel', cancel_targets=['job']),
                    packet('client-future', ready=2, cancel_tag='job'),
                    packet('server-future', direction='s2c', ready=2, cancel_tag='job')])
        r = candidate.calculate(p)
        self.assertEqual(state(r, 'client-future')['attempts'], 1)
        self.assertEqual(state(r, 'server-future')['attempts'], 0)
        p = inputs([packet('up'), packet('cancel', ready=2, cancel_targets=['job']),
                    packet('response', direction='s2c', dependencies=['model'], cancel_tag='job')])
        p['tasks'] = [dict(id='model', dependencies=['up'], duration=3, cancel_tag='job')]
        r = candidate.calculate(p)
        self.assertEqual(F(r['cancellations'][0]['at']), 4)
        self.assertEqual([(F(w['start']), F(w['end'])) for w in r['work']], [(2, 5)])
        self.assertEqual(state(r, 'response')['attempts'], 0)

    def test_network_priority_does_not_silently_change_compute_policy(self):
        p = inputs([packet('a')])
        p['scheduler'] = 'priority'
        p['tasks'] = [dict(id='first', duration=1, priority=0),
                      dict(id='second', duration=1, priority=10)]
        self.assertEqual([w['id'] for w in candidate.calculate(p)['work']], ['first', 'second'])
        p['compute_scheduler'] = 'priority'
        self.assertEqual([w['id'] for w in candidate.calculate(p)['work']], ['second', 'first'])

    def test_quiescent_or_stale_or_partial_is_not_useful_completion(self):
        p = inputs([packet('a', ready=1, reliable=False, allow_expire=True, deadline=0)])
        p['businesses'] = [dict(id='voice', kind='tts', playback='slots',
                               blocks=[dict(packets=['a'], duration=1, slot_start=0)])]
        r = candidate.calculate(p)
        self.assertEqual(r['unfinished'], [])
        self.assertFalse(r['summary']['all_businesses_usable'])
        p = inputs([packet('a'), packet('b', 'a', offset=1, drop_first=True)])
        p['businesses'] = [dict(id='voice', kind='tts', playback='reliable',
                               blocks=[dict(packets=[k], duration=1) for k in ('a', 'b')])]
        voice = candidate.calculate(p)['businesses'][0]
        self.assertEqual(voice['unresolved_blocks'], 1)
        self.assertFalse(voice['complete_playback'])
        for changed_at, usable in ((2, False), ('201/100', True)):
            p = inputs([packet('result', direction='s2c')])
            p['businesses'] = [dict(id='screen', kind='screenshot', required=['result'],
                                   version='v1', version_changes=[dict(at=changed_at, version='v2')])]
            self.assertEqual(candidate.calculate(p)['businesses'][0]['usable'], usable)

    def test_invalid_cross_endpoint_dependencies_and_business_contracts_are_rejected(self):
        cases = []
        p = inputs([packet('upload'), packet('client-send', dependencies=['upload'])])
        cases.append(p)  # Client cannot observe server receipt without a message.
        p = inputs([packet('up'), packet('down', direction='s2c')])
        p['businesses'] = [dict(id='asr', kind='asr', required=['up', 'down'])]
        cases.append(p)
        p = inputs([packet('unreliable', reliable=False, allow_expire=True, deadline=3)])
        p['businesses'] = [dict(id='image', kind='image', required=['unreliable'])]
        cases.append(p)
        p = inputs([packet('a', dependencies=['a'])])
        cases.append(p)
        for index, p in enumerate(cases):
            with self.subTest(index=index), self.assertRaises(ValueError):
                candidate.calculate(p)


if __name__ == '__main__':
    unittest.main()
