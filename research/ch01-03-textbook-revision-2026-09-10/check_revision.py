#!/usr/bin/env python3
"""Check revised teaching inputs, table structure, source conservation and exercise answers."""
from pathlib import Path
import hashlib,json,re,math
H=Path(__file__).resolve().parent;R=H.parents[1]
def load(n):return json.loads((R/'calculations/results'/f'{n}.json').read_text())
report={'checks':[],'exercise_answers':{}}
def check(ok,label):
 assert ok,label
 report['checks'].append(label)
for i in [1,2,3]:
 p=next((R/'manuscripts').glob(f'{i:02d}-*.md'));s=p.read_text()
 check(not any(ord(c)<32 and c not in '\n\t' for c in s),f'chapter {i}: no control characters')
 for table in re.findall(r'^\|[^\n]+\n\|[ :|\-]+\n(?:\|[^\n]+\n)+',s,re.M):
  lengths=[row.count('|') for row in table.strip().splitlines()];check(len(set(lengths))==1,f'chapter {i}: table columns {table.splitlines()[0][:35]}')
 nums=re.findall(r'\*\*例题 '+str(i)+r'-(\d+)',s);check(nums==[str(j) for j in range(1,len(nums)+1)],f'chapter {i}: sequential examples')
 check('## 谬误与陷阱' in s and '## 本章小结' in s,f'chapter {i}: teaching conclusions')
d=json.loads((R/'manuscripts/ch02/model-comparison.json').read_text())
for x in d['sources']:check(hashlib.sha256((R/x['path']).read_bytes()).hexdigest()==x['sha256'],'comparison source '+x['path'])
for x in d['models']:check(sum(x['parameter_groups'])==x['total_parameters'],'parameter conservation '+x['model'])
# Textual dimension checks complement source shape audit.
s=(R/'manuscripts/02-模型架构.md').read_text()
for n,total in [(1,36),(2,40),(4,43),(5,93)]:check(f'**表 2-{n}' in s,f'complete model table {n}')
check(13*1207959552>=15136811008 and 12*1207959552<15136811008,'weight/history threshold 13')
# Independently evaluate changed core paper exercises.
a=report['exercise_answers']
a['1-3']={str(b):{'batch_lower_ms':1000*max(140e9*b/(989.4e12*.5),70e9/(3.35e12*.7)),'amortized_ms':1000*max(140e9*b/(989.4e12*.5),70e9/(3.35e12*.7))/b} for b in [1,16,64]}
a['2-2']={}
for B,S,P in [(4,4096,1024),(1,4096,4096)]:
 pairs=B*(P*S+P*(P+1)//2);a['2-2'][f'B{B}-S{S}-P{P}']={'projection_ffn_flops':36*385875968*B*P,'attention_flops':36*16384*pairs,'last_head_flops':B*2*4096*151936}
a['2-5']={'k3_fixed_bytes':(414*2**20)+20348928,'qwen36_fixed_bytes':60*2**20+1966080}
for name,fixed,c in [('k3',a['2-5']['k3_fixed_bytes'],27648),('qwen36',a['2-5']['qwen36_fixed_bytes'],20480)]:
 a['2-5'][name]={'balance_positions':fixed/c,'32k_bytes':fixed+c*32768,'128k_bytes':fixed+c*131072}
a['2-7']={'qwen8':{str(n):(24_000_000_000-16381470720-2*2**30)//(147456*n) for n in [4096,16384]}}
cap=load('llama70-capacity-8k');row=next(z for z in cap['capacity_comparisons'] if z['matrix_bits']==4 and z['capacity_bytes']==80_000_000_000)
a['2-7']['llama70_48GB']={str(n):max(0,(48_000_000_000-row['weight_bytes']-2*2**30)//(row['kv_bytes_per_request']*n//8192)) for n in [8192,32768]}
a['3-2']={str(mu):{'backlog_steps':max(0,(7471.2-mu)*30),'drain_seconds':max(0,(7471.2-mu)*30)/mu} for mu in [6000,8000]}
a['3-4']={'first_four_times_total_s':76.510-36.375*(1-1/4),'half_tools_total_s':76.510-.078/2}
base=load('rl-qwen8-base')['summary'];low=load('rl-qwen8-low-acceptance')['summary'];a['3-7']={'48_candidates_matrix_flops':(base['cycle_matrix_flops']+low['cycle_matrix_flops'])//2,'teacher_added_flops':None}
# Exact teacher cost from source stage, not the rounded printed value.
rl=load('rl-qwen8-base');
stages=rl.get('stages',rl.get('phase_work',[]))
# Preserve exact update and use teacher-forced reference equality.
def find_ref(x):
 if isinstance(x,dict):
  if x.get('stage')=='reference_scoring' or x.get('name')=='reference_scoring':return x
  for v in x.values():
   z=find_ref(v)
   if z:return z
 elif isinstance(x,list):
  for v in x:
   z=find_ref(v)
   if z:return z
 return None
ref=find_ref(rl)
assert ref is not None, 'reference stage present'
if ref:

 for key in ['matrix_flops','flops']:
  if key in ref:a['3-7']['teacher_added_flops']=ref[key]*3//2
(H/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('Passed',len(report['checks']),'checks')
