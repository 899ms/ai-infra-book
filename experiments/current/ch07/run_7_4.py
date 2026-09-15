"""In-network reduction with explicitly defined engine throughput units."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('07-*.md'))
a=F(833,10**9);shard=96*2**20//8;bw=50*10**9;rows=[]
for servers in (2,8):
 ring=2*(servers-1)*a+F(2*(servers-1),servers)*shard/bw
 network=F(shard,bw);engine=[]
 for convention,volume in [('reduced_result_bytes',8*shard),('all_input_operand_bytes',8*servers*shard)]:
  duration=F(volume,200*10**9);bound=F(volume)/(ring-a)
  assert a+F(volume)/bound==ring and network<ring-a
  engine.append(dict(convention=convention,engine_bytes=volume,engine_service_ms=float(duration*1000),is_engine_bottleneck=duration>network,in_network_with_200GBps_ms=float((a+max(network,duration))*1000),strict_engine_threshold_GBps=float(bound/10**9),minimum_integer_GBps=bound.numerator//(bound.denominator*10**9)+1))
 rows.append(dict(servers=servers,per_NIC_shard_bytes=shard,ring_rounds=2*(servers-1),ring_send_bytes=float(F(2*(servers-1),servers)*shard),ring_ms=float(ring*1000),in_network_unlimited_engine_ms=float((a+network)*1000),engine=engine))
out=dict(exercise='7-4',BF16=rows,decode_startup=dict(layers=36,reductions=72,alpha_us=5,ring_total_us=72*14*5,in_network_total_us=72*5,saved_us=72*13*5),scope='Cross-server stage only; payload shard 12MiB per rail; engine shared across eight rails; reduced-result and aggregate-input throughput conventions both explicit',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'7-4-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
