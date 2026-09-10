#!/usr/bin/env python3
"""Verify chapter text, source-driven figures, formula rendering and local links."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from svg_labels import svg_labels
from fractions import Fraction
from urllib.parse import unquote,urlsplit
import hashlib,json,re,math,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
s=(HERE.parent/'10-训练系统.md').read_text();page=(HERE.parent/'10-训练系统.html').read_text();errors=[]
def check(ok,msg):
 if not ok:errors.append(msg)
def calc(n):return json.loads((ROOT/'calculations/results'/f'{n}.json').read_text())
figure_count=len(json.loads((HERE/'figure-index.json').read_text()))
heads=re.findall(r'^### (10\.\d+\.\d+)',s,re.M);expected=re.findall(r'^### (10\.\d+\.\d+)',(ROOT/'outlines/10-训练系统.md').read_text(),re.M)
check(heads==expected,'outline subsection alignment')
check('训练一致性' not in s and '训练一致性' not in page, 'obsolete RL consistency terminology')
for marker in ['专家路由重放与训推一致性', '前缀分布偏移', 'on-policy distillation', '温度缩放', '冻结同一份权重']:
 check(marker in s and marker in page, 'RL consistency coverage: '+marker)
check(re.findall(r'^> \*\*习题 (10-\d+)',s,re.M)==[f'10-{i}' for i in range(1,11)],'exercise sequence')
check(re.findall(r'^> \*\*习题 (10-\d+) · 综合设计',s,re.M)==['10-3','10-7','10-10'],'integrative design exercises')
check(re.findall(r'^\*图 (10-\d+)(?:：|　)',s,re.M)==[f'10-{i}' for i in range(1,figure_count+1)],'external caption sequence')
check(len(re.findall(r'!\[',s))==figure_count,'active figures')
for rec in json.loads((HERE/'sources.json').read_text())['sources']:
 check(hashlib.sha256((ROOT/rec['path']).read_bytes()).hexdigest()==rec['sha256'],'source hash: '+rec['path'])
manifest=json.loads((HERE/'manifest.json').read_text())
for rec in manifest['outputs']:
 check(hashlib.sha256((ROOT/rec['path']).read_bytes()).hexdigest()==rec['sha256'],'output hash: '+rec['path'])
for rec in manifest['outputs']:
 p=ROOT/rec['path']
 if p.suffix!='.svg':continue
 texts=svg_labels(p)
 check(not any(re.search(r'图\s*\d+[-—]\d+',t) for t in texts),'figure number inside '+p.name)
 check(bool(texts),'SVG has text or outlined glyph labels: '+p.name)
for u in re.findall(r'\]\(([^)]+)\)',s):
 parts=urlsplit(u)
 if parts.scheme:continue
 target=(HERE.parent/unquote(parts.path)).resolve()
 check(target.exists(),'missing link '+u)
for marker in re.findall(r'\[\^([^\]]+)\]',s):check(f'[^{marker}]:' in s,'undefined footnote '+marker)
check('MATHPLACEHOLDER' not in page,'unrendered math')
check(page.count('src="data:image/png;base64,')==figure_count,'embedded image count')
check(len(re.findall(r'<nav[^>]*>.*?</nav>',page,re.S))==1,'navigation')
mathreport=json.loads((HERE/'math-validation.json').read_text());check(not mathreport['errors'],'math errors')
layout=json.loads((HERE/'teaching-layout-validation.json').read_text());check(len(layout)==figure_count and all(not r['text_extent_warnings'] and r['width_pt']==420 and r['min_label_pt']>=11 for r in layout),'book-size figure layout')
# Recompute the key decision examples independently of drawing code.
N=8190735360;check(16*N==calc('training-state-book')['summary']['unsharded_persistent_bytes'],'Adam total')
F=calc('training-deadline-book')['summary']['task_training_matrix_flops'];check(math.ceil(F/(165.2e12*30*86400))==13,'4090 peak count')
check(math.ceil(F/(165.2e12*.4*30*86400))==31,'4090 40 percent count')
G=96*2**20;cross=1/(3*(1/100e9-1/1500e9));check(abs(cross/1e9-35.714285714)<1e-8,'cast crossover')
check(8192*48*8*2==6*2**20,'routing bytes')
check(Fraction(8,5)/20+Fraction(24,5)/20==Fraction(8,25),'global token normalization')
check(2*4096*4097//2==16781312,'balanced pairs');check(7168*7169//2+1024*1025//2==26218496,'skew pairs')
check(Fraction(44,60)==Fraction(11,15),'async effective threshold')
c=14*N/8e9;lam=1024/(365*86400);check(abs(math.sqrt(2*c/lam)-939.6125188821188)<1e-8,'checkpoint interval')
d=json.loads((HERE/'figure-data.json').read_text());check(d['10-7']['填满排空']['summary']['step_makespan_seconds']<d['10-7']['1F1B']['summary']['step_makespan_seconds'],'pipeline counterexample')
# Check revised figure conclusions against source quantities and displayed precision.
for n,shown in [(8,25.3),(16,17.6)]:
 i=d['10-6']['participants'].index(n)
 check(math.isclose(d['10-6']['total_gib'][i],16*N/n/2**30+10),'sharded capacity source')
 check(round(d['10-6']['total_gib'][i],1)==shown,'sharded capacity displayed value')
for interval,expected in [(300,[4.8,.5,.4,5.7]),(900,[1.6,1.5,.4,3.4]),(1800,[.8,2.9,.4,4.1])]:
 losses=[100*c/interval,100*lam*interval/2,100*lam*120]
 check([round(x,1) for x in losses+[sum(losses)]]==expected,'checkpoint period comparison')
for label,rows in d['10-12']['timelines'].items():
 latest=max(row['seconds']['capture'] for row in rows if row['seconds']['durable']<=d['10-12']['failure_seconds'])
 check(latest==d['10-12']['recoverable_capture_seconds'][label],'recoverable checkpoint at failure')
v=calc('weight-handoff-qwen8')['summary']['phase_live_bytes']
check(max(d['10-15']['restore_bytes'])==v['restore_all_before_release'],'restore peak')
check(max(d['10-15']['staged_bytes'])==v['sync_weights_before_release'],'staged peak')
check(max(d['10-15']['restore_bytes'])-max(d['10-15']['staged_bytes'])==24*2**30,'handoff peak reduction')
check(round((72*2**20/(16*2**30)+.0001)*1000,1)==4.5,'whole bucket time')
check(round((24*2**20/(16*2**30)+.0001)*1000,1)==1.6,'split bucket window')
check([min(8,.75*min(g,v)) for g,v in [(12,6),(24,6),(12,12)]]==[4.5,4.5,8],'RL supply bottleneck')
for name in ['填满排空','1F1B']:
 ev=d['10-7'][name]['events'];check(sum(x['kind']=='update' for x in ev)==4,'all optimizer events drawn');check(sum(x['kind']=='F' for x in ev)==32 and sum(x['kind']=='B' for x in ev)==32,'pipeline full event count')
# Independently evaluate the running design, using source FLOPs and declared inputs.
case=json.loads((HERE/'design-case.json').read_text())
check(case['tokens_per_update']==384*8192 and case['updates']==math.ceil(10**11/(384*8192)),'running task work')
for row in case['candidates']:
 p=row['devices'];local=F/10**11*(384*8192)/(p*165.2e12*.4)
 loss=c/1800+p/(365*86400)*(900+120)
 finish=5+math.ceil(10**11/(384*8192))*(local+4.5)*(1+loss)/86400
 check(math.isclose(row['finish_days'],finish,rel_tol=1e-12),'running deadline recompute')
 check(384%p==0 and row['microbatches_per_device']==384//p,'unchanged global batch')
 check(row['peak_budget_gib']<22,'running capacity feasibility')
 check((finish<30)==(p==48),'running design selection')
 check(round(finish,1)==(35.8 if p==32 else 26.1),'running displayed days')
check(round(case['candidates'][1]['max_base_step_seconds'],1)==67.3,'running acceptance step time')
for dev,curve in d['10-20'].items():
 source_row=curve['source_rows'][0]
 expected=source_row['training_days']*16384/90
 check(math.isclose(curve['continuous_required_devices'][-1],expected*10),'scale boundary')
 check(math.isclose(curve['parameters_at_16384_devices'],16384/expected*1e12),'scale intersection')
recompute=calc('pipeline-gemm-recompute-products')['reservation']
check(recompute['added_persistent_bytes_per_microbatch_stage'][0]==45*2**20,'recompute retained operands')
check(calc('pipeline-gemm-save-1f1b')['reservation']['added_persistent_bytes_per_microbatch_stage'][0]==135*2**20,'saved operands derivation')
check(recompute['additional_product_workspace_bytes_per_stage'][0]==6*2**20,'recompute workspace derivation')
ev=calc('training-pipeline-1f1b-m8')['events'];lookup={e['id']:e for e in ev}
check(math.isclose(lookup['F:3:2']['start']-lookup['B:3:1']['end'],.002),'annotated pipeline dependency gap')
main=s.split('## 参考资料与进一步阅读')[0]
check(not re.search(r'不代表|不能只|尚需核验|不用于.*外推|上式只描述',main),'no defensive prose endings')
check(main.index('> **习题')>main.index('## 习题与实验'),'exercises collected after main exposition')
# New mechanism figures must depict the same conditions used in the derivations.
check(d['recompute_lifetime']['product_bytes']==6*2**20,'lifetime product shape')
check(d['cast_paths']['gpu_path_transfer_bytes']==2*d['cast_paths']['cpu_path_transfer_bytes'],'conversion path bytes')
w=d['communication_window'];check(w['queued_reduce_ms'][1]-w['compute_ms'][1]==w['wait_ms']==2,'communication waiting interval')
a=d['attention_area'];check([sum(n*(n+1)//2 for n in lens) for lens in a['lengths']]==a['pairs'],'attention triangles are true pairs')
q=d['input_queue'];check(q['pending_batches']==list(range(q['last_trained_batch']+1,q['last_dispatched_batch']+1)),'queue resumes at first untrained batch')
r=d['checkpoint_resharding'];check(r['old_rows']*r['old_parts']==r['new_rows']*r['new_parts']==r['shape'][0],'resharding preserves row coverage')
t=d['checkpoint_tradeoff'];check(math.isclose(t['optimal_seconds'],math.sqrt(2*t['checkpoint_seconds']/t['job_failure_rate_per_second'])),'checkpoint curve minimum')
rl=d['rl_supply_flow'];check(min(rl['learn_capacity'],rl['retained_fraction']*min(rl['generate_capacity'],rl['verify_capacity']))==rl['effective_rate'],'RL flow bottleneck')
cycle=d['rl_async_cycle'];check(cycle['overlapped_period_seconds']==max(cycle['generate_seconds'],cycle['learn_seconds'])+cycle['sync_seconds'],'async timeline')
for row in d['task_deadline_breakdown']['rows']:check(math.isclose(sum(row['days']),row['finish_days']),'deadline bars add to finish time')
figrefs=[int(n) for n in re.findall(r'图 10-(\d+)',s)]
check(all(1<=n<=figure_count for n in figrefs),'figure references within chapter sequence')
report={'status':'passed' if not errors else 'failed','sections':6,'subsections':len(heads),'exercises':10,'figures':figure_count,'image_files':sum(Path(r['path']).suffix in ['.svg','.png','.pdf'] for r in manifest['outputs']),'formulas':mathreport['expressions'],'source_files':len(json.loads((HERE/'sources.json').read_text())['sources']),'chinese_characters':len(re.findall(r'[\u4e00-\u9fff]',s)),'errors':errors}
(HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2));raise SystemExit(bool(errors))
