"""Public transport endpoints against independently fixed hand expectations."""
import copy
from fractions import Fraction as F
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from infra_calc.topics import transport_closed_loop as network
from infra_calc.topics.transport_sender import create_sender
from infra_calc.report import markdown


class ClosedLoopTests(unittest.TestCase):
    def test_response_starts_before_last_upload_ack(self):
        result = network.calculate()
        self.assertEqual(result['business'],dict(upload='3',model_start='3',model_end='4',response='6'))
        upload_acks = [e for e in result['sender_events']['up'] if e['type']=='ack']
        self.assertEqual([F(e['at']) for e in upload_acks], [F(4), F(5)])
        self.assertIn('完整线上包时间轴', markdown(result))

    def test_cwnd_and_absolute_flow_are_separate(self):
        result = network.calculate(network.scenarios()['absolute-flow-arrival'])
        data = [t for t in result['transmissions'] if t['direction']=='up' and t['kind']=='data']
        self.assertEqual(F(data[-1]['send_start']), F(6)+F(23,307))
        self.assertEqual(F(result['business']['upload']), F(8)+F(23,307))

    def test_loss_waits_for_sender_feedback(self):
        result = network.calculate(network.scenarios()['loss-feedback-recovery'])
        self.assertEqual(result['losses']['up'][0]['at'],'5')
        self.assertEqual(result['business']['upload'],'7')
        retry = [t for t in result['transmissions'] if t['recovery_of'] is not None]
        self.assertEqual((retry[0]['pn'],retry[0]['frames'][0]['offset']),(2,0))

    def test_pto_does_not_immediately_mark_loss(self):
        result = network.calculate(network.scenarios()['tail-pto-probe'])
        self.assertEqual(result['timers']['up'][0]['at'],'12')
        self.assertEqual(result['losses']['up'][0]['at'],'16')
        self.assertEqual(result['business']['upload'],'14')
        data = [t for t in result['transmissions'] if t['kind']=='data']
        self.assertEqual(len(data),2)
        self.assertEqual(result['summary']['unique_received_bytes'],1168)

    def test_router_drop_preserves_flight_before_feedback(self):
        p = network.example()
        p.update(upload_bytes=3504,response_bytes=0,until=6)
        p['sender']['initial_cwnd']=3600
        p['links']['down']['propagation']=100
        p['routers']={'up':dict(rate_bps=4912,queue_bytes=0,propagation=100)}
        result = network.calculate(p)
        self.assertEqual(result['losses']['up'],[])
        self.assertEqual(result['final_states']['up']['bytes_in_flight'],3600)
        dropped = [t for t in result['transmissions'] if t['dropped']]
        self.assertEqual([t['pn'] for t in dropped],[1])

    def test_zero_credit_is_explicitly_incomplete(self):
        r=network.calculate(network.scenarios()['no-credit-incomplete'])
        self.assertFalse(r['summary']['complete'])
        self.assertIsNone(r['business']['response'])
        self.assertIn('MAX_DATA',r['waits'][0]['reasons'])

    def test_incremental_watermark_and_numeric_contract(self):
        p=dict(until=20,initial_max_data=1000,initial_max_stream_data={'s':1000},events=[])
        s=create_sender(p);s['advance'](10)
        with self.assertRaises(ValueError):s['enqueue'](dict(type='max_data',at=5,value=2000))
        with self.assertRaises(ValueError):s['advance'](9)
        with self.assertRaises(ValueError):create_sender(dict(p,numeric_quantum=0))
        with self.assertRaises(ValueError):create_sender(dict(p,numeric_quantum=1000))

    def test_strict_network_inputs_and_source_set(self):
        p=network.example();p['packet_payload']=0
        with self.assertRaises(ValueError):network.calculate(p)
        p=network.example();p['sender']['events']=[]
        with self.assertRaises(ValueError):network.calculate(p)
        r=network.calculate()
        self.assertEqual({s['revision'] for s in r['reference_sources']},{'RFC9000','RFC9002','RFC9002 Verified Errata7539'})


if __name__=='__main__':unittest.main()
