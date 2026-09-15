"""Shape mixture arithmetic, original six-candidate search, and actual Agent costs."""
from fractions import Fraction as F
from pathlib import Path
import ast,hashlib,json,statistics,math
R=Path(__file__).resolve().parent;ROOT=R.parents[2];E=ROOT/'experiments/ch05/05-06';S=E/'results/schedule-search-v2'
mixture=[dict(p=str(p),original_us=10,new_us=float(20-15*p),dispatch_us=float(11-5*p),dispatch_saving_us=float(5*p-1)) for p in (F(1,2),F(2,3),F(9,10))]
search=json.loads((S/'search.json').read_text());rows=[];files=[S/'search.json']
for record in search['records']:
 p=S/record['file'];d=json.loads(p.read_text());files.append(p);assert d['status']=='passed'
 for f,h in d['source_hashes'].items():assert hashlib.sha256((E/f).read_bytes()).hexdigest()==h
 med={r['t']:statistics.median(r['samples_us']) for r in d['rows']};assert all(len(r['samples_us'])==11 for r in d['rows'])
 rows.append(dict(index=record['index'],kind=d['kind'],median_us=med,score_us=sum(med.values()),wall_s=d['wall_s'],event_window_s=d['gpu_event_window_s']))
candidates=[r for r in rows if r['kind']=='schedule'];assert len(candidates)==6
budget=sum(r['event_window_s'] for r in candidates);assert abs(budget-search['schedule_event_window_s'])<1e-9
best=min(candidates,key=lambda r:r['score_us']);native=next(r for r in rows if r['kind']=='native');savings={t:native['median_us'][t]-best['median_us'][t] for t in (1,7239)}
agent=[];initial=ast.dump(ast.parse((E/'schedule.py').read_text()))
for v in (1,2):
 p=E/f'results/agent-search-v{v}';summary=json.loads((p/'summary.json').read_text());files.append(p/'summary.json')
 rounds=[json.loads(f.read_text()) for f in sorted(p.glob('round-*.json'))];assert len(rounds)==6
 for i,r in enumerate(rounds):assert ast.dump(ast.parse((p/f'candidate-{i}.py').read_text()))==initial
 generation=sum(r['generation_s'] for r in rounds)
 events=sum(json.loads(f.read_text())['gpu_event_window_s'] for f in p.glob('evaluation-*.json'))
 assert abs(generation+events-summary['charged_s'])<1e-6
 agent.append(dict(version=v,rounds=6,new_asts=0,charged_s=summary['charged_s'],elapsed_s=summary['elapsed_s']))
wall=sum(r['wall_s'] for r in candidates);pair_saving=sum(savings.values())
out=dict(exercise='5-6',mixture=mixture,dispatch_strictly_better_p='p > 1/5',all_new_strictly_better_p='p > 2/3',search_rows=rows,selected_index=best['index'],six_candidate_event_window_s=budget,six_candidate_evaluation_wall_s=wall,all_eight_evaluation_wall_s=sum(r['wall_s'] for r in rows),selection_sample_saving_us=savings,conditional_equal_shape_pair_saving_us=pair_saving,conditional_wall_amortization_pairs=math.ceil(wall/(pair_saving/1e6)),original_agent_runs=agent,original_agent_total_charged_s=sum(r['charged_s'] for r in agent),original_agent_total_loop_s=sum(r['elapsed_s'] for r in agent),source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
(R/'5-6-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('search_rows','source_sha256')},indent=2))
