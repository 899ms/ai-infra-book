"""Image, screenshot and phone budgets under the manuscript's assumptions."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,math
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
images=[]
for uplink in [10,20,100]:
 images.append(dict(uplink_Mbps=uplink,original_s=float(F(240,uplink)+F('.8')),accelerated_s=float(F(240,uplink)+F('.53')),compressed_s=float(F(120,uplink)+F('.95'))))
# Three independent chunks; full duplex, single compute and download resources.
chunks=[];compute_free=download_free=F(0)
for i,down in enumerate([F('.08'),F('.16'),F('.16')]):
 upload_start=F(4*i);upload_end=upload_start+4;arrive=upload_end+F('.05')
 cs=max(arrive,compute_free);ce=cs+F('.1');ds=max(ce,download_free);de=ds+down
 chunks.append(dict(chunk=i+1,upload_start_s=float(upload_start),upload_end_s=float(upload_end),server_arrive_s=float(arrive),compute_start_s=float(cs),compute_end_s=float(ce),download_start_s=float(ds),download_end_s=float(de),client_arrive_s=float(de+F('.05'))))
 assert cs>=arrive and cs>=compute_free and ds>=ce and ds>=download_free
 compute_free=ce;download_free=de
assert chunks[-1]['client_arrive_s']==12.36
original=F('3.5');compressed=F('2.78');maxround=math.ceil(30*original/compressed)-1
assert maxround*compressed<30*original<=(maxround+1)*compressed
src=ROOT/'calculations/results/qwen3-8b-decode-b1-s8192.json';s=json.loads(src.read_text())['summary']
bandwidth=4*16*F('10.6')*10**9/8
read=s['weight_read_once_per_operator_bytes'];resident=s['weight_resident_bytes'];kv=s['kv_existing_history_unique_payload_bytes'];per=s['kv_bytes_per_token_per_request']
assert kv==8192*per and resident==s['parameters']*2
ratio=F(18,64);remaining=8*10**9-resident*ratio;requests=remaining//kv;context=remaining//per
assert requests*kv<=remaining<(requests+1)*kv
assert context*per<=remaining<(context+1)*per
phone=[]
for name,w in [('BF16',F(read)),('q4_0',read*ratio)]:
 step=(w+kv)/bandwidth
 phone.append(dict(format=name,weight_read_bytes=float(w),step_s=float(step),token_s=float(1/step)))
sources=[ROOT/'manuscripts/12-端边云协同.md',src]
out=dict(exercises=['12-1','12-2','12-9'],kind='analytical_stated_conditions',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sources},image=dict(cases=images,compression_break_even_Mbps=800,partial_acceleration_20Mbps_s=float(12+F('.1')+F('.12')+F('.4')),chunks=chunks),screenshot=dict(original30_s=float(30*original),compressed30_s=float(30*compressed),saved30_s=float(30*(original-compressed)),compressed38_s=float(38*compressed),maximum_strictly_faster_rounds=maxround,added_RTT_original30_s=float(30*(original+F('.1'))),added_RTT_compressed38_s=float(38*(compressed+F('.1')))),phone=dict(bandwidth_bytes_s=int(bandwidth),kv_bytes=kv,kv_bytes_per_token=per,cases=phone,resident_BF16_bytes=resident,resident_q4_bytes=float(resident*ratio),remaining_after_reserve_weight_bytes=float(remaining),max_8K_requests=int(requests),single_context_max_tokens=int(context),power_only_token_s=[float(F('13.8')/F('.756')),float(F('13.8')/F('.576'))]))
(P/'12-1-2-9-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
