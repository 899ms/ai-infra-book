"""Verify measured profiler feedback, Agent edits, charged budget, and held-out gate."""
import ast,hashlib,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results/exclusive-followups-001';A=O/'agent'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
env=read(A/'environment.json');s=read(A/'summary.json')
for f,h in env['source_hashes'].items():assert sha(R/f)==h
baseline=R/'results/exclusive-profile-001/schedule/3-schedule.json';assert sha(baseline)==env['baseline_profile_sha256']
base=read(baseline);assert base['status']=='passed'
rounds=[read(p) for p in sorted(A.glob('round-*.json'))];assert len(rounds)==s['round_count']<=6
charged=0.;seen={ast.dump(ast.parse((R/'schedule.py').read_text()))};prior=None;results=[]
profile=[dict(t=r['t'],profiler_feedback=r['profiler_feedback'],median_graph_us=statistics.median(r['samples_us'])) for r in base['rows']]
for i,row in enumerate(rounds):
 assert row['turn']==i and len(row['messages'])==2+2*i
 assert json.dumps(profile) in row['messages'][0]['content']
 if prior:
  assert row['messages'][:-2]==prior['messages'] and row['messages'][-2]['content']==prior['output_text']
 action=json.loads(row['output_text']);assert action==row['action']
 code=(A/f'candidate-{i}.py').read_text();assert code==action['code']
 fingerprint=ast.dump(ast.parse(code));reply=row['tool_result'];new=fingerprint not in seen
 if reply['status']=='passed':
  assert new and sha(A/f'candidate-{i}.py')==row['candidate_sha256']
  for shape in reply['rows']:
   trace=read(A/shape['profiler_feedback']['trace'])
   kernels=[e for e in trace['traceEvents'] if e.get('cat')=='kernel']
   assert kernels and [e['name'] for e in kernels]==[e['name'] for e in shape['profiler_feedback']['kernels']]
  assert abs(reply['score_us']-sum(statistics.median(r['samples_us']) for r in reply['rows']))<1e-8
  seen.add(fingerprint)
 charged+=row['generation_s']+reply.get('gpu_event_window_s',0)
 assert abs(charged-row['charged_s'])<1e-8
 results.append(dict(turn=i,status=reply['status'],new_AST=new,error=reply.get('error'),score_us=reply.get('score_us'),charged_s=charged,
  shape_medians_us=[statistics.median(r['samples_us']) for r in reply.get('rows',[])]))
 prior=row
assert abs(charged-s['charged_s'])<1e-8 and charged<=s['budget_s']==60
passing=[r for r in results if r['status']=='passed'];winner=min(passing,key=lambda r:(r['score_us'],r['turn']))
assert s['status']=='selected' and winner['turn']==s['selected_turn']
heldout=read(O/'agent-heldout.json');assert heldout['selection']==s and heldout['selection_sha256']==sha(A/'summary.json')
assert heldout['source_sha256']==sha(R/'heldout_agent.py')
assert len(heldout['rows'])==5 and all(r['status']=='passed' for r in heldout['rows'])
assert [r['shape'][0] for r in heldout['rows']]==[17,257,4096,7,1]
report=dict(status='feedback_and_heldout_independently_verified',rounds=results,selected=s,heldout=heldout['rows'],
 profile_baseline_sha256=sha(baseline),scope='Fourth independent attempt retained alongside three previous negative attempts. Six-candidate/60s ceiling, not equal actual spend. Profile durations are instrumented, score is separate graph replay. Request deployment measured separately.')
(O/'agent-verified.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
