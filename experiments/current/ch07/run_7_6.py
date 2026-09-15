"""Rail permutation, failed-NIC redistribution, and TP16 coordinate mapping."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('07-*.md'))
payload=24*2**20;routes=[];A=[0]*8;B=[0]*8
for i in range(8):
 j=(i+4)%8;dest=[(2,F(1,2)),(4,F(1,2))] if j==3 else [(j,F(1))]
 for nic,fraction in dest:
  amount=int(payload*fraction);A[i]+=amount;B[nic]+=amount
  routes.append(dict(rank_A=i,rank_B=j+8,A_rail=i,B_rail=nic,bytes_each_direction=amount,via_spine=i!=nic,borrowed_NIC=j==3))
assert sum(A)==sum(B)==8*payload and B==[payload,payload,payload*3//2,0,payload*3//2,payload,payload,payload]
alpha=F(833,10**9);time=2*alpha+F(max(A+B),50*10**9)
local=F(payload,450*10**9)
coords=[]
for rail in range(8):
 coords.append(dict(rail=rail,TP_coordinates=[rail,rail+8],DP_members_per_coordinate_inside_supernode=8,gradient_GB_per_coordinate=4,cross_domain_GB_per_coordinate=7,total_cross_domain_GB=14))
assert sum(x['total_cross_domain_GB'] for x in coords)==112
out=dict(exercise='7-6',shift4_healthy=dict(pairs=[[i,(i+4)%8+8] for i in range(8)],spine_bytes_each_direction=8*payload,spine_both_directions_bytes=16*payload,stage_ms=float((2*alpha+F(payload,50*10**9))*1000)),failed_B_NIC3=dict(routes=routes,A_NIC_send_bytes=A,B_NIC_send_bytes=B,spine_bytes_each_direction=sum(r['bytes_each_direction'] for r in routes if r['via_spine']),NIC_stage_lower_ms=float(time*1000),local_detour_serial_payload_ms=float(local*1000),no_overlap_added_detour_stage_ms=float((time+local)*1000)),TP16=coords,scope='Payload per NIC per direction across both rounds; independent full-duplex links, sufficient spine capacity. Added NVLink detour is either pipelined or charged separately; no measured failure recovery time.',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'7-6-results.json').write_text(json.dumps(out,indent=2)+'\n');print(out['shift4_healthy']);print({k:v for k,v in out['failed_B_NIC3'].items() if k!='routes'})
