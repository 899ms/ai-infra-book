"""Small independent arithmetic plus frozen historical sender replay."""
from pathlib import Path
from fractions import Fraction as F
import copy,hashlib,json
import sender
ROOT=Path(__file__).resolve().parent
checks=[]
def config(**kw):
 p=dict(initial_max_data=10,initial_max_stream_data={'A':100,'B':5},initial_cwnd=2400,max_ack_delay=0,until=1,events=[])
 p.update(kw);return p
def stream(name,offset,length):return dict(type='stream',stream=name,offset=offset,length=length)
def datagram(name,length):return dict(type='datagram',id=name,length=length)
def packet(pn,at,frames,**kw):return dict(type='sent',at=at,pn=pn,sent_bytes=64,ack_eliciting=True,in_flight=True,frames=frames,**kw)
def emit(s,e):s['enqueue'](e);s['advance'](e['at'])
s=sender.create_sender(config());emit(s,packet(0,0,[stream('A',2,3)]));emit(s,packet(1,'.01',[stream('B',0,5)]));assert s['state']()['max_data_consumed']==10
assert s['validate_packet'](packet(2,'.02',[stream('B',5,1)]))[1]==['MAX_DATA','MAX_STREAM_DATA:B']
emit(s,packet(2,'.02',[datagram('voice0',2)]));assert s['state']()['max_data_consumed']==10
emit(s,packet(3,'.03',[stream('A',2,3)]));assert s['state']()['max_data_consumed']==10
emit(s,dict(type='ack',at='.1',ranges=[[0,3]],ack_delay=0));r=s['result']();assert r['sender_confirmed_business']==dict(stream_intervals={'A':[[2,5]],'B':[[0,5]]},unique_stream_bytes=8,acked_datagram_ids=['voice0'],acked_datagram_bytes=2)
assert r['summary']['stream_payload_transmission_bytes']==11 and s['state']()['bytes_in_flight']==0
checks+=['sum-highest-offsets-includes-unsent-gap','per-stream-and-connection-gates','datagram-zero-reliable-credit','new-PN-old-offset-no-new-credit','ACK-business-unique-versus-transmission']
emit(s,dict(type='max_data',at='.11',value=20));assert s['validate_packet'](packet(4,'.12',[stream('B',5,1)]))[1]==['MAX_STREAM_DATA:B']
emit(s,dict(type='max_stream_data',at='.12',stream='B',value=6));assert not s['validate_packet'](packet(4,'.13',[stream('B',5,1)]))[1]
emit(s,dict(type='ack',at='.13',ranges=[[0,3]],ack_delay=0));assert s['result']()['sender_confirmed_business']==r['sender_confirmed_business'];checks+=['absolute-MAX-arrivals-independent','duplicate-ACK-no-double-credit']
for name,frames in [('repeat-datagram',[datagram('voice0',2)]),('unknown-stream',[stream('Z',0,1)]),('boolean-offset',[stream('A',True,1)]),('negative-offset',[stream('A',-1,1)]),('zero-length',[datagram('x',0)]),('same-packet-duplicate-datagram',[datagram('x',1),datagram('x',1)]),('same-packet-overlap',[stream('A',0,3),stream('A',2,2)])]:
 before=s['state']()
 try:s['validate_packet'](packet(4,'.14',frames))
 except ValueError:pass
 else:raise AssertionError(name)
 assert s['state']()==before;checks.append('reject-'+name)
# Datagram-only PTO: one explicit PING probe; no application frame retransmission.
t=sender.create_sender(config(initial_max_data=0,initial_max_stream_data={},initial_rtt='.1'))
emit(t,packet(0,0,[datagram('loss0',10)]));t['advance']('.3');assert t['timers'][-1]['kind']=='pto'
assert sender.retransmittable_frames(t['history'][0])==[]
emit(t,packet(1,'.301',[],probe=True));emit(t,dict(type='ack',at='.4',ranges=[[1,1]],ack_delay=0));assert t['history'][0]['status']=='lost' and t['state']()['bytes_in_flight']==0
assert t['result']()['sender_confirmed_business']['acked_datagram_bytes']==0
emit(t,dict(type='ack',at='.41',ranges=[[0,0]],ack_delay=0));assert t['result']()['sender_confirmed_business']['acked_datagram_bytes']==10 and t['state']()['bytes_in_flight']==0
assert t['result']()['summary']['datagram_payload_transmission_bytes']==10;checks+=['datagram-only-PTO-explicit-PING','datagram-loss-no-reliable-retry','late-datagram-ACK-once']
mixed=dict(frames=[stream('A',0,3),datagram('m',2)]);selected=sender.retransmittable_frames(mixed);assert selected==[stream('A',0,3)];selected[0]['offset']=99;assert mixed['frames'][0]['offset']==0;checks.append('mixed-recovery-selects-only-STREAM-deep-copy')
# Full math comparison against pre-existing frozen 14-scenario reference results.
old=ROOT.parent/'transport-feedback';cases=json.loads((old/'scenarios.json').read_text());saved=json.loads((old/'result.json').read_text());reg=[]
for name,p in cases.items():
 a=sender.create_sender(p)
 for event in p['events']:a['enqueue'](event)
 a['advance'](p['until']);actual=a['result']();expected=saved[name]
 keys=('events','packets','loss_events','timer_events','rtt_samples','final_state','sender_confirmed_business','summary')
 for key in keys:assert actual[key]==expected[key],(name,key)
 reg.append(name)
out=dict(status='PASS',sender_sha256=hashlib.sha256((ROOT/'sender.py').read_bytes()).hexdigest(),dependencies=sender.verify_dependencies(),checks=checks,check_count=len(checks),historical_full_math_cases=reg,scope='Direct pinned public sender reuse; multi-stream/credit/DATAGRAM/PTO helper review. Network engine not covered.')
(ROOT/'sender-check.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(checks),'small checks;',len(reg),'historical full math cases')
