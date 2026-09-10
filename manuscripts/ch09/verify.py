#!/usr/bin/env python3
"""Verify chapter coverage, source locks, math and figure data without GPU work."""
from pathlib import Path
from fractions import Fraction
from urllib.parse import unquote,urlsplit
import hashlib,json,re,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
checks=[]
def check(condition,name):checks.append({'name':name,'passed':bool(condition)})
def read(n):return json.loads((ROOT/'calculations/results'/f'{n}.json').read_text())
def val(x):return float(Fraction(str(x)))
md=HERE.parent/'09-分布式推理.md';s=md.read_text();html=md.with_suffix('.html').read_text();outline=(ROOT/'outlines/09-分布式推理.md').read_text()
check(re.findall(r'^#{2,3} (9\.\d+(?:\.\d+)?) ',s,re.M)==re.findall(r'^#{2,3} (9\.\d+(?:\.\d+)?) ',outline,re.M),'All seven sections and 24 subsection numbers match outline')
check(re.findall(r'^\*\*9-(\d+)\s',s,re.M)==[str(i) for i in range(1,11)],'Ten chapter exercises retained')
index=json.loads((HERE/'figure-index.json').read_text());count=len(index)
check(re.findall(r'^\*图 (9-\d+)：',s,re.M)==[f'9-{i}' for i in range(1,count+1)],'Sequential external captions')
check(len(re.findall(r'!\[.*?\]\(ch09/figure-',s))==count,'Active figures included')
ids=set(re.findall(r'\[\^([^\]]+)\]:',s));uses=set(re.findall(r'\[\^([^\]]+)\](?!:)',s));check(ids==uses,'All citations defined and used')
for match in re.findall(r'\]\(([^)]+)\)',s):
 parts=urlsplit(match)
 if parts.scheme:continue
 path=(md.parent/unquote(parts.path)).resolve();check(path.exists(),'Local reference '+match)
for source in json.loads((HERE/'sources.json').read_text())['sources']:
 path=ROOT/source['path'];check(path.exists() and hashlib.sha256(path.read_bytes()).hexdigest()==source['sha256'],'Source lock '+source['path'])
for entry in index:
 p=HERE/(entry['name']+'.svg')
 root=ET.parse(p).getroot();text=' '.join(root.itertext());check(not re.search(r'图\s*\d+\s*[-–]\s*\d+',text),'No caption number inside '+p.name)
 for ext in ['png','pdf']:check(p.with_suffix('.'+ext).stat().st_size>1000,'Export '+p.with_suffix('.'+ext).name)
check(len(index)==count,'Active vector figure index')
check(html.count('src="data:image/png;base64,')==count,'Reading HTML embeds all active figures')
math=json.loads((HERE/'math-validation.json').read_text());check(math['expressions']>=80 and not math['errors'],'KaTeX parsed all inline and display formulas')
check('MATHPLACEHOLDER' not in html and 'katex-error' not in html,'No unrendered math')
layout=json.loads((HERE/'teaching-layout-validation.json').read_text())
check(len(layout)==count and all(x['width_pt']==420 and x['min_label_pt']>=11 and not x['text_extent_warnings'] for x in layout),'Book-size readable labels')
# Independently check the chapter's key arithmetic against frozen results.
V=2*36*8192*8*128*2;check(V==1207959552,'GQA KV bytes');check(V/2**30==1.125,'Binary capacity conversion')
handoff=read('pd-af-handoff-qwen8')['summary'];check(handoff['pd_snapshot_bytes']==V,'PD frozen payload');A=2*36*4096*2;check(A==589824==handoff['af_total_bytes'],'AF directional payload sum');check(36*2==handoff['af_directional_messages'],'AF message count')
af_ns=72*5000+Fraction(A*10**9,25*10**9);check(af_ns==Fraction(handoff['af_serialized_ns_exact']),'AF serialized time');check(abs(float(af_ns)*128/1e6-49.09989888)<1e-8,'Full decode handoff accumulation')
check(A*8192/2**30==4.5,'Full prefill AF payload in teaching placement')
z=read('pd-pool-book');grid=[]
for row in z['pool_assignments']:
 pa=row['prefill_workers']['prefill-oriented'];pb=row['prefill_workers']['decode-oriented'];rate=min(2*pa+Fraction(pb,2),Fraction(4-pa,2)+2*(4-pb),Fraction(25*10**9,V));check(rate==Fraction(row['bound_requests_per_second_exact']),f'Integer allocation A={pa},B={pb}');grid.append(rate)
check(max(grid)==8 and 8/Fraction(5,2)==Fraction(z['summary']['colocated_bound_requests_per_second_exact']),'PD and colocated upper bounds')
P=3*4096*1536;W=2*P
check(W==36*2**20 and 32*W*94/2**30==105.75,'Expert and all-layer resident capacity')
for m in [78,79]:
 tasks=8*m
 cpu=Fraction(16*5000)+Fraction(tasks*16384,25)+max(Fraction(2*P*tasks,2000),Fraction(W*8,200))
 gpu=Fraction(8*5000)+Fraction(W*8,25)+max(Fraction(2*P*tasks,100000),Fraction(W*8,1000))
 z=read('expert-locality-boundary'+str(m))['summary'];check(cpu==Fraction(z['cpu_service_ns_exact']) and gpu==Fraction(z['weight_copy_service_ns_exact']),f'Independent expert boundary {m}')
check(7*32==224 and 8*32==256,'Padding controls')
z=read('replica-payback-book')['summary'];n=Fraction(z['serialized_copy_setup_ns_exact'])//Fraction(z['per_batch_saving_ns_exact'])+1;check(n==27==z['algebraic_strict_payback_batches'],'Strict replica payback');check(94*W/2**30==3.3046875,'Per-layer replica capacity')
route=read('cache-route-stale')['summary'];check(Fraction(9,10)*90+Fraction(1,10)*260==107 and Fraction(route['a_expected_ns_exact'])==107000000,'Stale cache expected time');check(Fraction(route['a_p99_ns_exact'])==260000000,'Stale cache p99');check(Fraction(route['strict_mean_hit_probability_threshold_exact'])==Fraction(6,17),'Mean hit threshold')
z=read('cache-restart-book')['summary'];check(z['consumer_read_file_bytes']==144*2**20 and z['consumer_reusable_bytes']==Fraction(567,4)*2**20,'Read versus reusable bytes')
check(Fraction(10,1)/Fraction(2,10000)==50000,'Startup break-even execution steps')
check(40/(8-4)==10 and 40/(5-4)==40,'Queue drain after readiness')
# Added numerical arguments: use identical dimensions, explicit resource assumptions.
E,K,M=128,8,64;Pe=3*4096*1536;We=2*Pe
check(M*K==512 and M*K/E==4 and M==64,'Same 512 dispatches, four versus 64 rows per expert')
check(M*K*2*Pe==19327352832,'Expert work remains 19.3 GFLOPs')
check(E*We==int(4.5*2**30) and K*We==288*2**20 and E/K==16,'Distinct weight traffic differs by sixteen')
check(round(E*(1-(1-K/E)**M))==126,'Independent-routing expectation near 126 experts')
check(round(E*(1-(1-K/E)**M)*We/2**30,2)==4.43,'Expected distinct weight volume')
check((M*K*2*Pe)/(M*K*2*Pe/8)==8,'Most-loaded rank work differs eightfold')
check(min(2*8,2*.5+4*2)==9 and min(8,3*.5+4*2)==8,'Prefix hit reallocates two A workers to decode')
check(Fraction(3,16)+4*Fraction(1,4)==Fraction(19,16),'Long output allocation')
fig=json.loads((HERE/'figure-data.json').read_text())
check(round(fig['9-6']['cpu_ms'][127],1)==20.1 and round(fig['9-6']['weight_copy_gpu_ms'][127],1)==12.5,'High reuse reverses CPU/GPU choice')
check(Fraction(1,10)+Fraction(3,10)+Fraction(1,10)+Fraction(3,10)==Fraction(8,10),'Two-microbatch overlap example')
check(Fraction(1,10)+Fraction(4,10)+Fraction(1,10)+Fraction(4,10)==1,'Shared-resource slowdown consumes overlap saving')
check(50+60>100 and 50+2*60<2*100,'Save-and-retrieve needs reuse')
network=read('reconfiguration-declared-serial')['summary']['network_bytes'];slow=network/5e9+9;fast=network/25e9+9
check(round(slow,1)==12.3 and round(fast,1)==9.7 and round((slow-fast)/slow*100)==21,'Migration bandwidth yields 21 percent total improvement')
check([round(8/(3600*r)*1000,2) for r in [3.2,8,2]]==[.69,.28,1.11],'Effective output changes cost ordering')
check(fig['9-12']['pages_read']==64 and fig['9-12']['pages_reused']==63,'Single relationship in page reuse figure')
check(fig['9-16']['pool_initial_payload_GiB']==2*fig['9-16']['direct_payload_GiB'],'Direct versus pool initial traffic')
check(set(fig['9-17'])=={'type','startup_s','arrival_rps','time_s','queues','drain_time_from_start_s'},'Startup figure contains only backlog argument')

# Complete deployment worked example and explanatory crossover.
check(8*8320*144/1024**2+1.125 < 12,'Eight final KV states and one receive buffer fit 12 GiB')
check(64//1.125==56,'Shared pool holds 56 complete prefixes')
check(round(25e9/(2*V),1)==10.3,'Shared-channel two-hop capacity')
check(40+(4-3.2)*15==52,'Colocated backlog at 25 seconds')
check(Fraction(4)+Fraction(40,15)==Fraction(20,3),'Recovery deadline requires 20/3 requests per second')
check(round(8/(3600*4)*1000,2)==.56,'Provisioned cost at actual arrival rate')
check(10+40/(Fraction(100,17)-4)==Fraction(125,4),'Cached colocated backlog drains at 31.25 seconds (31.3 rounded half up)')
check(3*Fraction(19,16)<4<4*Fraction(19,16),'Long-output steady arrival needs four fixed groups')
check(5*Fraction(19,16)<Fraction(20,3)<6*Fraction(19,16),'Long-output recovery deadline needs six fixed groups')
check(2e12/200e9==10 and 2e12/100e9==20,'Worked solution CPU resource crossover')

# Verify that each new mechanism diagram agrees with its teaching example.
check(fig['new-footprint']['active_experts'][0]*fig['new-footprint']['rows_per_expert'][0]==512 and fig['new-footprint']['active_experts'][1]*fig['new-footprint']['rows_per_expert'][1]==512,'Equal rectangle areas represent identical dispatch counts')
check(fig['new-footprint']['weight_MiB']==[128*36,8*36],'Expert footprint bytes')
check(all(sum(v)==512 for v in fig['new-balance']['assignments_per_card']),'Balanced and concentrated devices perform equal total work')
check(fig['new-allocation']['rates']==[8,9,19/16],'Allocation diagram uses three solved pool rates')
check([round(x) for x in fig['new-route']['first_token_ms']]==[260,200,310,129],'Route timelines reproduce four completion times')
check(abs(fig['new-migration']['catchup_s']-1/(2-.5))<1e-12,'Copy catches growing state at two thirds of a second')
check(fig['new-recovery']['input_positions']+fig['new-recovery']['replayed_outputs']==fig['new-recovery']['restored_KV_positions']==8320,'Recovery diagram preserves KV position boundary')
check(fig['new-overlap']['pipeline_ms']==.8 and fig['new-overlap']['serial_ms']==1,'Overlap schedule completion times')

for record in json.loads((HERE/'manifest.json').read_text())['outputs']:
 p=ROOT/record['path'];check(hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'],'Artifact hash '+p.name)
report={'status':'passed' if all(c['passed'] for c in checks) else 'failed','checks':len(checks),'errors':[c['name'] for c in checks if not c['passed']],'sections':7,'subsections':24,'figures':count,'exercises':10,'cjk_characters':sum('\u4e00'<=x<='\u9fff' for x in s),'new_gpu_measurements':False}
(HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(report['errors']))
