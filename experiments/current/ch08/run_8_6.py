"""KV layout arithmetic, paired correctness, and complete successful attempt costs."""
from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('08-*.md'));raw=ROOT/'experiments/ch08/08-08'
cap=[]
for label,tokens in [('input',8192),('complete_paged',8448)]:
 bf=tokens*147456;assert bf%64==0
 cap.append(dict(state=label,allocated_tokens=tokens,BF16_MiB=bf/2**20,q8_0_bytes=bf//64*34,q8_0_MiB=bf//64*34/2**20,q4_0_bytes=bf//64*18,q4_0_MiB=bf//64*18/2**20))
s=json.loads((raw/'results/summary.json').read_text());q=json.loads((raw/'results/q-control-summary.json').read_text());quality={}
for c in s['configurations']:
 quality[c['name']]={r['id']:dict(task=r['task_id'],correct=r['strict_correct']) for r in c['requests'] if r['mode']=='natural' and r['trial'] in (0,1)}
quality['fp8_bf16_q']={r['id']:dict(task=r['task_id'],correct=r['correct']) for r in q['records'] if r['mode']=='natural' and r['trial'] in (0,1)}
assert all(len(v)==32 for v in quality.values())
changes=[]
for id,a in quality['bf16'].items():
 b=quality['fp8_bf16_q'][id]
 if a['correct']!=b['correct']:changes.append(dict(id=id,task=a['task'],BF16=a['correct'],FP8_KV_BF16_Q=b['correct']))
costs=[];files=[source,raw/'results/summary.json',raw/'results/q-control-summary.json',raw/'results/raw-manifest.json',raw/'analyze.py',raw/'analyze_q_control.py']
for group in ('results','results-regression'):
 d=raw/'retry-cost'/group;attempts={r['id']:r for r in map(json.loads,(d/'attempts.jsonl').read_text().splitlines())}
 for t in map(json.loads,(d/'tasks.jsonl').read_text().splitlines()):
  chain=[attempts[a] for a in t['attempt_ids']];assert t['final_correct'] and chain[-1]['correct']
  gen=sum(r['end_s']-r['start_s'] for r in chain);last=chain[-1]['end_s']-chain[-1]['start_s'];whole=t['end_s']-t['start_s'];assert whole>=gen>=last
  costs.append(dict(group=group,task_execution=t['id'],attempts=len(chain),all_generation_s=gen,last_success_generation_s=last,omitted_failed_generation_s=gen-last,observed_task_s=whole,checks_and_other_overhead_s=whole-gen))
 files.extend(d/f for f in ('attempts.jsonl','tasks.jsonl','environment.json'))
out=dict(exercise='8-6',capacity=cap,quality_correct_counts={k:sum(r['correct'] for r in v.values()) for k,v in quality.items()},changed_correctness=changes,successful_task_costs=costs,scope='q8_0/q4_0 grouped layouts are distinct from measured FP8 E4M3 KV; quality comparison BF16 weights, retry experiment online FP8 weights; all formal successful tasks retained',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'8-6-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(capacity=cap,counts=out['quality_correct_counts'],changes=changes,retried=[r for r in costs if r['attempts']>1]),indent=2))
