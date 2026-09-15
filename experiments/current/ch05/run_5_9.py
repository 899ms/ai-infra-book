"""Recompute the book's paired requests, recorded phase times and DAG threshold."""
from pathlib import Path
import hashlib,json,statistics,sqlite3
R=Path(__file__).resolve().parent;ROOT=R.parents[2];E=ROOT/'experiments/ch05/05-09';rawpath=E/'results/paired-eager-v1/raw.json';raw=json.loads(rawpath.read_text())
for f,h in raw['source_hashes'].items():assert hashlib.sha256((E/f).read_bytes()).hexdigest()==h
req=[r for r in raw['requests'] if r['phase']=='measure'];assert len(req)==22
assert req==[json.loads(s) for s in (rawpath.parent/'requests.jsonl').read_text().splitlines()]
pairs=[]
for i in range(11):
 g={r['mode']:r for r in req if r['trial']==i};assert set(g)=={'native','schedule'};n,s=g['native'],g['schedule']
 assert n['output_ids']==s['output_ids'] and n['prompt_tokens']==s['prompt_tokens']==7239 and n['output_tokens']==s['output_tokens']==32
 pairs.append(dict(trial=i,native_ms=n['latency_s']*1000,schedule_ms=s['latency_s']*1000,saving_ms=(n['latency_s']-s['latency_s'])*1000))
profilepath=E/'profiles/analysis.json';profiles=json.loads(profilepath.read_text());phases={}
for p in profiles['reports']:
 db=E/'profiles'/(p['mode']+'.sqlite');assert hashlib.sha256(db.read_bytes()).hexdigest()==p['sqlite_sha256']
 con=sqlite3.connect(f'file:{db}?mode=ro',uri=True);events=set(con.execute('select start,end from CUPTI_ACTIVITY_KIND_KERNEL'));con.close()
 hot=[k for k in p['kernels'] if k['category']=='swiglu'];assert len(hot)==1152 and all((k['start_ns'],k['end_ns']) in events for k in hot)
 steps=sorted({k['step'] for k in hot});assert len(steps)==32 and all(sum(k['step']==i for k in hot)==36 for i in steps)
 pre=sum(k['end_ns']-k['start_ns'] for k in hot if k['step']==steps[0])/1e6;dec=sum(k['end_ns']-k['start_ns'] for k in hot if k['step']!=steps[0])/1e6
 phases[p['mode']]=dict(prefill_ms=pre,decode31_ms=dec)
a,b=phases['native'],phases['schedule'];decode_saved=a['decode31_ms']-b['decode31_ms'];prefill_saved=a['prefill_ms']-b['prefill_ms'];estimate=prefill_saved+decode_saved*127/31
out=dict(exercise='5-9',pairs=pairs,paired_median_saving_ms=statistics.median(r['saving_ms'] for r in pairs),difference_of_medians_ms=statistics.median(r['native_ms'] for r in pairs)-statistics.median(r['schedule_ms'] for r in pairs),phases=phases,decode_per_step_saving_ms=decode_saved/31,estimated_127_decode_activation_saving_ms=decode_saved*127/31,estimated_total_activation_saving_ms=estimate,critical_path=[dict(a_us=i,request_us=20+max(i,40)) for i in range(61)],critical_path_plateau_a_us=40,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [rawpath,profilepath,ROOT/'manuscripts/05-算子与运行时.md']})
assert out['critical_path'][39]['request_us']==out['critical_path'][40]['request_us']==60 and out['critical_path'][41]['request_us']==61
(R/'5-9-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('critical_path','source_sha256')},indent=2))
