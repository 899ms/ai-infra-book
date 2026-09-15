"""Equal-byte split versus actual AF traffic and two-stage pipeline DAG."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('09-*.md'))
B=25*10**9;kv=9*2**27;decode=72*8192;prefill=8192*decode;rows=[]
for us in (1,5,20):
 a=F(us,10**6);one=a+F(kv,B);split=72*a+F(kv,B);pre=72*a+F(prefill,B);step=72*a+F(decode,B)
 assert split-one==71*a
 rows.append(dict(alpha_us=us,one_PD_ms=float(one*1000),same_bytes_72_transfers_ms=float(split*1000),extra_split_ms=float(71*a*1000),actual_AF_prefill_ms=float(pre*1000),actual_AF_decode_step_ms=float(step*1000),actual_AF_1024_decode_ms=float(1024*step*1000),actual_AF_full_request_ms=float((pre+1024*step)*1000)))
endA=endF=0;events=[]
for i in range(4):
 a0=endA;endA=a0+2;f0=max(endA,endF);endF=f0+3;events.append(dict(microbatch=i,attention_ms=[a0,endA],FFN_ms=[f0,endF]))
assert endF==14 and 4*(2+3)-endF==6
out=dict(exercise='9-4',PD_bytes=kv,same_bytes_split_per_transfer=kv//72,AF_decode_step_bytes=decode,AF_prefill_bytes=prefill,AF_full_request_bytes=prefill+1024*decode,AF_full_request_transfers=72*(1+1024),communication=rows,pipeline=events,serial_ms=20,pipeline_ms=endF,strict_added_critical_path_bound_ms=6,scope='Serial AF transfers, unchunked prefill, 1025 outputs require 1024 subsequent decode steps; four independent microbatches with separate compute resources',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'9-4-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
