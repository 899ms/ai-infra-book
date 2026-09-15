"""Rational packet events: unequal delays and selective first-packet recovery."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('07-*.md'))
tau=F(4096,50_000) # microseconds at 50 GB/s
single=1+8*tau;cross=single-4*tau
assert max(1+4*tau,cross+4*tau)==single

def events(assign,delay,lost=False):
 clocks=[F(0),F(0)];out=[]
 for seq,path in enumerate(assign):
  start=clocks[path];clocks[path]+=tau
  arrival=clocks[path]+delay[path]
  if seq==0 and lost:arrival=tau+40+tau+delay[0]
  out.append(dict(seq=seq,path=path,send_start_us=float(start),original_send_end_us=float(clocks[path]),arrival_us=float(arrival),arrival_exact=arrival))
 pending=set();expected=0;peak=0;first=None;delivered={}
 for time in sorted({x['arrival_exact'] for x in out}):
  pending.update(x['seq'] for x in out if x['arrival_exact']==time)
  while expected in pending:
   pending.remove(expected);delivered[expected]=float(time);expected+=1
   if first is None:first=float(time)
  peak=max(peak,len(pending))
 assert expected==8 and not pending
 for x in out:x.pop('arrival_exact');x['in_order_delivery_us']=delivered[x['seq']]
 return dict(events=out,first_delivery_us=first,complete_us=max(delivered.values()),peak_reorder_packets=peak,peak_reorder_bytes=peak*4096)
sweep=[dict(second_delay_us=float(F(1)+F(i,10)),dual_complete_us=float(max(1+4*tau,F(1)+F(i,10)+4*tau)),single_complete_us=float(single)) for i in range(81)]
equal=events([0,1]*4,[F(1),F(9)]);unequal=events([0,1,0,1,0,1,0,0],[F(1),F(9)]);loss=events([0,1]*4,[F(1),F(9)],True)
assert equal['peak_reorder_bytes']==12288 and loss['peak_reorder_bytes']==28672
assert loss['first_delivery_us']==float(tau+40+tau+1)
out=dict(exercise='7-13',packet_serialization_us=float(tau),single_complete_us=float(single),crossover_second_delay_us=float(cross),sweep=sweep,equal_4_4=equal,unequal_5_3=unequal,first_packet_loss_40us=loss,scope='Independent serializers, full-packet arrival and instantaneous in-order delivery; recovery wait counted from original packet-0 send end; no congestion or feedback detection model',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'7-13-results.json').write_text(json.dumps(out,indent=2)+'\n');print('tau',float(tau),'crossover',float(cross),'single',float(single),'5/3',unequal['complete_us'],'loss',loss['complete_us'],'buffer',loss['peak_reorder_bytes'])
