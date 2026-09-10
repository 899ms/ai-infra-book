"""Independent sender-snapshot, transport identity and frontier checks."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
from bbr_adapter import BbrAdapter
from cubic_adapter import CubicAdapter
from sender import create_sender
ROOT=Path(__file__).resolve().parent

def packet(pn,t=0,flight=True):
 return dict(pn=pn,time=F(str(t)),sent_bytes=1200 if flight else 64,in_flight=flight,ack_eliciting=flight,frames=[],was_lost=False)

def bc(now,before,after=None,raw=None):
 return dict(now=F(str(now)),flight_before=before,flight_after=before if after is None else after,smoothed_rtt=F('0.05'),rtt_sample=None if raw is None else {'raw':str(raw)},pacer_next_eligible=F(str(now)))

def run():
 tests=[]
 b=BbrAdapter(config={'external_pacer':True})
 b.on_sent(packet(0),bc(0,0));b.on_sent(packet(1,'.01'),bc('.01',1200))
 b.on_ack([0],bc('.05',2400,1200,'.05'))
 b.on_sent(packet(2,'.08'),bc('.08',1200))
 e=b.on_ack([1,2],bc('.1',2400,0,'.02'))
 assert e['selected_pn']==2 and e['sample']['delivered']==2
 assert e['sample']['snd_interval_us']==80000 and e['sample']['rcv_interval_us']==50000
 assert e['sample']['interval_us']==80000 and e['sample']['bw_scaled']==419
 assert e['actual_sample_udp_bytes']==e['nominal_sample_quic_bytes']==2400
 tests.append('selected-send-snapshot-and-dominant-send-interval')
 b=BbrAdapter(config={'external_pacer':True});b.on_sent(packet(0),bc(0,0))
 b.on_loss([0],bc('.1',1200,0));b.on_sent(packet(1,'.2'),bc('.2',0))
 e=b.on_ack([1],bc('.3',1200,0,'.1'));assert b.delivered==1
 e=b.on_ack([0],bc('.4',0,0));assert b.delivered==2 and b.delivered_udp_bytes==2400
 assert e['callback']['input']['rtt_us']==-1
 b.on_ack([0],bc('.5',0,0));assert b.delivered==2 and len(b.active())==0
 tests.append('late-ack-once-no-duplicate-flight-or-rtt')
 b=BbrAdapter(config={'external_pacer':True});b.on_sent(packet(0,flight=False),bc(0,0));b.on_ack([0],bc('.1',0,0));assert b.delivered==0
 tests.append('pure-ack-not-bbr-delivery')
 b=BbrAdapter(config={'external_pacer':True});b.on_limited(dict(now=0,app_limited=False,flow_limited=True))
 e=b.on_sent(packet(0),bc(0,0));assert e['record']['flow_limited'] and not e['record']['app_limited']
 tests.append('flow-limited-not-application-limited')
 b=BbrAdapter(config={'external_pacer':True});b.on_limited(dict(now=0,app_limited=True,flow_limited=False))
 b.on_sent(packet(0),bc(0,0));b.on_limited(dict(now='.01',app_limited=False,flow_limited=False))
 e=b.on_ack([0],bc('.1',1200,0,'.1'));assert e['sample']['is_app_limited']
 tests.append('application-flag-from-sent-snapshot')
 old=(b.cwnd_bytes,b.delivered,b.lost);b.on_pto(dict(now='.2'));assert old==(b.cwnd_bytes,b.delivered,b.lost)
 tests.append('pto-not-loss-or-delivery')
 b=BbrAdapter(config={'external_pacer':True});b.on_sent(packet(0),bc(0,0));b.on_loss([0],bc('.1',1200,0))
 b.on_sent(packet(1,'.2'),bc('.2',0));b.on_ack([1],bc('.3',1200,0,'.1'))
 e=b.on_sent(packet(2,1),bc(1,0));assert e['record']['first_tx_us']==e['record']['delivered_mstamp_us']==1000001
 e=b.on_ack([2],bc('1.1',1200,0,'.1'));assert e['sample']['interval_us']==100000 and e['sample']['bw_scaled']==167
 tests.append('new-empty-flight-epoch-after-retransmission-ack')
 c=CubicAdapter(1200,12000,F('.1'))
 c.on_sent(packet(0),dict(now=F(0)));c.on_sent(packet(1,'.01'),dict(now=F('.01')))
 c.on_sent(packet(2,'.02',False),dict(now=F('.02')))
 assert c.frontier==2400
 ctx=dict(now=F('.1'),smoothed_rtt=F('.1'),rtt_sample=None,recovery_start=None)
 c.on_ack([packet(1,'.01')],ctx);assert c.hy.acked_seq==0 and c.hy.round==1 and c.cwnd_bytes==13200
 c.on_ack([packet(0)],dict(ctx,now=F('.2')));assert c.hy.acked_seq==2400 and c.hy.round==2 and c.cwnd_bytes==14400
 tests.append('hystart-frontier-does-not-skip-ack-hole')
 assert c.hy.samples==0
 tests.append('hystart-does-not-sample-smoothed-rtt')
 c=CubicAdapter(1200,12000,F('.1'))
 for pn in range(8):c.on_sent(packet(pn),dict(now=F(0)))
 for n in range(1,49):
  if n%8==0 and n<48:
   for pn in range(n,n+8):c.on_sent(packet(pn,F(n)-F('0.5')),dict(now=F(n)-F('0.5')))
  c.on_ack([packet(n-1)],dict(now=F(n),smoothed_rtt=F('.01'),rtt_sample=dict(pn=n-1,adjusted='.01' if n<=8 else '.014'),recovery_start=None))
 assert not c.initial_active and c.hy.css_completed==5 and c.cwnd_bytes==40800
 assert c.core.phase=='avoidance'
 tests.append('hystart-css-to-cubic-byte-unit-handoff-once')
 c=CubicAdapter(1200,12000,F('.1'))
 c.on_loss([packet(0)],dict(now=F(1),flight_before=12000,new_recovery_epoch=True))
 assert c.cwnd_bytes==8400
 c.on_loss([packet(1)],dict(now=F(2),flight_before=10800,new_recovery_epoch=False))
 assert c.cwnd_bytes==8400
 c.on_ack([dict(packet(0),was_lost=True)],dict(now=F(3),smoothed_rtt=F('.1'),rtt_sample=None,recovery_start=F(1)))
 assert c.cwnd_bytes==8400
 tests.append('cubic-one-loss-reduction-per-epoch-and-no-late-growth')
 for name in ('bbr','cubic_hystart'):
  st=create_sender(dict(until=1,initial_max_data=1168,initial_max_stream_data={'business':1168},initial_cwnd=12000,max_ack_delay=0,rtt_seed=dict(latest_rtt='.1',smoothed_rtt='.1',rttvar='.05',min_rtt='.1'),controller=dict(name=name,pad_in_flight=True),events=[]))
  # Supplied-time sender replay: this neutral hook deliberately does not audit pacing.
  st['set_pacer'](lambda at,rate:at)
  ev=[]
  for pn,t in [(0,'0'),(1,'0.3')]:
   ev.append(dict(type='sent',at=t,pn=pn,sent_bytes=1200,ack_eliciting=True,in_flight=True,probe=pn==1,frames=[dict(type='stream',stream='business',offset=0,length=1168)]))
  ev += [dict(type='ack',at='.4',ranges=[[1,1]],ack_delay=0),dict(type='ack',at='.5',ranges=[[0,0]],ack_delay=0),dict(type='ack',at='.6',ranges=[[0,0]],ack_delay=0)]
  for e in ev:st['enqueue'](e)
  st['advance'](1)
  assert st['timers'][0]['at']=='3/10' and st['losses'][0]['at']=='2/5'
  assert st['state']()['bytes_in_flight']==0 and st['state']()['max_data_consumed']==1168
  assert st['acked_stream']['business']==[[0,1168]]
  if name=='bbr':
   a=st['adapter'];assert a.delivered==2
   acks=[e for e in a.events if e['event']=='ack'];assert len(acks)==2 and acks[-1]['callback']['input']['rtt_us']==-1
  else:assert st['adapter'].cwnd_bytes==2400
  tests.append('sender-pto-probe-late-duplicate-'+name)
 return dict(status='passed',checks=tests,hashes={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in ('bbr_adapter.py','cubic_adapter.py','sender.py')},scope='direct independent adapter callbacks, excludes pacer and full network')
if __name__=='__main__':
 r=run();(ROOT/'adapters-independent.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
