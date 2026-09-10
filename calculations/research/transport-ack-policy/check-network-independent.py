"""Actual candidate execution; independently reconstruct wire ACK claims and service."""
import copy
import hashlib
import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ack_network_review',ROOT/'calculate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def hashes():return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'calculate.py',ROOT/'receiver.py',ROOT/'sources.lock.json',ROOT/'dependencies.lock.json']}
before=hashes(); inputs=json.loads((ROOT/'scenarios.json').read_text()); saved=json.loads((ROOT/'result.json').read_text()); results=[]
for name,p in inputs.items():
 r=m.calculate(copy.deepcopy(p)); assert r==saved[name],name
 ts=r['transmissions']; count=0
 for d in ['up','down']:
  ps=[x for x in ts if x['direction']==d]; last=F(0)
  for x in ps:
   start,end=F(x['send_start']),F(x['send_end']);assert start>=last;last=end
   assert end-start==F(x['wire_bytes']*8)/F(str(p['links'][d]['rate_bps']))
   if not x['dropped']: assert F(x['arrival'])==end+F(str(p['links'][d]['propagation']))
 for x in ts:
  if x['kind']!='ack':continue
  d='up' if x['direction']=='down' else 'down';at=F(x['send_start']);s=x['ack_snapshot']
  arrived={a['pn']:F(a['arrival']) for a in ts if a['direction']==d and not a['dropped'] and a['arrival'] is not None and F(a['arrival'])<=at}
  claimed=[n for lo,hi in s['ranges'] for n in range(lo,hi+1)]
  assert claimed==sorted(arrived), (name,claimed,arrived) # Small fixtures fit retention; full history expected.
  highest=max(arrived);assert highest==s['largest'];raw=at-arrived[highest];assert raw==F(s['raw_delay'])
  tick=F(2**s['delay_exponent'],1000000);assert s['encoded_delay']==raw//tick;assert F(s['decoded_delay'])==s['encoded_delay']*tick
  matching=[e for e in r['sender_events'][d] if e['type']=='ack' and e['at']==x['arrival'] and e['ranges']==s['ranges']]
  assert len(matching)==(0 if x['dropped'] else 1),(name,x,matching)
  if matching:assert F(matching[0]['ack_delay'])==F(s['decoded_delay'])
  count+=1
 acks=[x for x in ts if x['kind']=='ack']
 if name in ('count-two','same-time-arrival-deadline'):
  assert len(acks)==1 and F(acks[0]['send_start'])==3 and F(acks[0]['arrival'])==5
  assert sum(x['wire_bytes'] for x in ts)==2548
 if name=='tail-deadline':assert len(acks)==1 and F(acks[0]['send_start'])==F(5,2) and F(acks[0]['arrival'])==F(9,2)
 if name=='lost-first-ack':
  assert len(acks)==2 and acks[0]['dropped'] and acks[1]['ack_snapshot']['ranges']==[[0,1]]
  assert [e['at'] for e in r['sender_events']['up'] if e['type']=='ack']==['5']
 if name in ('queued-snapshot-refresh','queued-deadline-overrun'):
  assert [(F(a['send_start']),F(a['send_end'])) for a in acks]==[(F(2),F(4)),(F(4),F(6))]
  assert acks[0]['ack_snapshot']['ranges']==[[0,0]]
  expected_high=2 if name=='queued-snapshot-refresh' else 1
  assert acks[1]['ack_snapshot']['ranges']==[[0,expected_high]]
  assert F(acks[1]['ack_snapshot']['raw_delay'])==(0 if expected_high==2 else 1)
  if expected_high==1:assert acks[1]['ack_snapshot']['exceeds_max_delay'] is True
 results.append(dict(name=name,transmissions=len(ts),acks_independently_checked=count,actual_matches_saved=True))
# Precomputed busy reverse serializer: 1228*8/736 = 307/23 seconds.
busy=copy.deepcopy(inputs['tail-deadline']);busy['response_bytes']=1168;busy['until']=100
busy['sender']['rtt_seed']={k:100 for k in ('latest_rtt','smoothed_rtt','rttvar','min_rtt')}
b=m.calculate(busy);ba=[x for x in b['transmissions'] if x['direction']=='down' and x['kind']=='ack'];assert len(ba)==1
assert F(ba[0]['send_start'])==F(353,23) and F(ba[0]['ack_snapshot']['raw_delay'])==F(307,23)
assert ba[0]['ack_snapshot']['exceeds_max_delay'] is True
assert F(ba[0]['send_end'])==F(376,23)
results.append(dict(name='busy-reverse-serializer-independent',inputs=busy,ack_start='353/23',raw_delay='307/23',exceeds_max_delay=True))
after=hashes();assert before==after
out=dict(status='PASS',scope='Eight actual small network scenarios; independently reconstructed serialization/ACK ranges/delay/arrival feedback plus four prespecified timing oracles. No large workload claim.',sources_before=before,sources_after=after,scenarios=results)
(ROOT/'network-independent.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
