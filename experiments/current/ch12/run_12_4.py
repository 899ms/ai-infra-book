"""Recount archived matched ACK traces, with separate packet-count approximation."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,math
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
sources=[ROOT/'manuscripts/12-端边云协同.md'];rows=[];inputs=[]
for name in ['controller-loop-book-newreno','ack-policy-book-newreno']:
 src=ROOT/'calculations/results'/f'{name}.json';x=json.loads(src.read_text());sources.append(src);inputs.append(x['inputs'].copy())
 groups={k:[t for t in x['transmissions'] if t['kind']==k] for k in ['data','ack']}
 assert sum(map(len,groups.values()))==len(x['transmissions'])
 data=groups['data'];ack=groups['ack'];payload=sum(f.get('length',0) for t in data for f in t['frames'] if f['type']=='stream')
 assert payload==35000000 and all(not t['dropped'] and t['recovery_of'] is None for t in x['transmissions'])
 data_wire=sum(t['wire_bytes'] for t in data);ack_wire=sum(t['wire_bytes'] for t in ack);total=data_wire+ack_wire
 assert total==x['summary']['wire_bytes'] and x['summary']['complete']
 for direction in ['up','down']:
  tx=sorted((t for t in x['transmissions'] if t['direction']==direction),key=lambda t:F(t['send_start']))
  assert all(F(a['send_end'])<=F(b['send_start']) for a,b in zip(tx,tx[1:]))
 rows.append(dict(name=name,data_packets=len(data),ack_packets=len(ack),image_bytes=payload,data_headers_padding_bytes=data_wire-payload,ack_bytes=ack_wire,total_bytes=total,response_s=float(F(x['business']['response']))))
inputs[1].pop('ack_policy');assert inputs[0]==inputs[1]
counts=[math.ceil(30000000/1168),math.ceil(5000000/1168)]
base=sum(counts);simple=[]
for kind,ackn in [('immediate',base),('every_two_ideal',sum(math.ceil(n/2) for n in counts))]:
 simple.append(dict(kind=kind,data_packets=base,headers_bytes=base*60,ack_packets=ackn,ack_bytes=ackn*92,total_bytes=35000000+base*60+ackn*92))
out=dict(exercise='12-4',new_connection_extra_s=12,reused_connection_extra_s=.4,saved_s=11.6,simple_packet_model=simple,matched_archived_simulation=rows,matched_saved_bytes=rows[0]['total_bytes']-rows[1]['total_bytes'],matched_extra_completion_s=rows[1]['response_s']-rows[0]['response_s'],source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sources})
(P/'12-4-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
