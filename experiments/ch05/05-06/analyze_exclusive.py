"""Verify exclusive run records, profiler traces, search budget and Agent failures."""
import ast
import hashlib
import json
from pathlib import Path
import statistics

R=Path(__file__).resolve().parent
O=R/'results/exclusive-profile-001'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
completion=read(O/'completion.json')
for f,h in completion['source_hashes'].items():assert sha(R/f)==h,f
assert not read(O/'before.json')['apps'].strip() and not read(O/'after.json')['pids']
for p in O.glob('*-gpu.jsonl'):
    samples=[json.loads(l) for l in p.read_text().splitlines()]
    assert samples and all(not s['foreign_pids'] for s in samples)
execution=read(O/'execution.json');assert all(r['exit_code']==0 for r in execution)
search=read(O/'schedule/search.json');assert len(search['records'])==8
schedules=[]
for r in search['records']:
    data=read(O/'schedule'/r['file']);assert data['status']=='passed'
    assert [row['t'] for row in data['rows']]==[1,7239]
    for row in data['rows']:
        assert len(row['samples_us'])==11
        trace=read(O/'schedule'/row['profiler_feedback']['trace'])
        kernels=[e for e in trace['traceEvents'] if e.get('cat')=='kernel']
        assert kernels and len(kernels)==len(row['profiler_feedback']['kernels'])
        assert [e['name'] for e in kernels]==[e['name'] for e in row['profiler_feedback']['kernels']]
    medians=[statistics.median(row['samples_us']) for row in data['rows']]
    schedules.append(dict(kind=data['kind'],block=data['block'],warps=data['warps'],shape_medians_us=medians,
        mean_shape_us=statistics.mean(medians),actual_36_calls_each_us=36*sum(medians),
        score_us=sum(medians),event_window_s=data['gpu_event_window_s']))
spent=sum(s['event_window_s'] for s in schedules if s['kind']=='schedule')
assert abs(spent-search['event_window_s'])<1e-8 and spent<=60
selected=min((r for r in schedules if r['kind']=='schedule'),key=lambda r:r['score_us'])
agent=O/'agent';env=read(agent/'environment.json');summary=read(agent/'summary.json')
for f,h in env['source_hashes'].items():assert sha(R/f)==h,f
rounds=[read(p) for p in sorted(agent.glob('round-*.json'))]
assert len(rounds)==summary['round_count']==6 and summary['status']=='no_valid_candidate'
initial=ast.dump(ast.parse((R/'schedule.py').read_text()));charged=0.;previous=None
for i,row in enumerate(rounds):
    assert row['turn']==i and len(row['messages'])==2+2*i
    if previous:
        assert row['messages'][:-2]==previous['messages']
        assert row['messages'][-2]['content']==previous['output_text']
    action=json.loads(row['output_text']);assert action==row['action']
    assert action['code']==(agent/f'candidate-{i}.py').read_text()
    assert ast.dump(ast.parse(action['code']))==initial
    assert row['tool_result']['status']=='failed' and 'Repeated unchanged kernel' in row['tool_result']['error']
    charged+=row['generation_s'];assert abs(charged-row['charged_s'])<1e-8
    previous=row
assert abs(charged-summary['charged_s'])<1e-8 and charged<=60
paired=read(O/'interleaved/raw.json')
assert paired['status']=='passed' and len(paired['samples'])==132
for f,h in paired['source_hashes'].items():assert sha(R/f)==h
comparison=[]
for t in [1,7239]:
    for mode in ['eager','graph']:
        values={name:{r['trial']:r['event_us'] for r in paired['samples'] if (r['t'],r['mode'],r['name'])==(t,mode,name)} for name in ['native','compiled','schedule']}
        assert all(set(v)==set(range(11)) for v in values.values())
        for baseline in ['native','compiled']:
            deltas=[values[baseline][i]-values['schedule'][i] for i in range(11)]
            comparison.append(dict(t=t,mode=mode,baseline=baseline,paired_saving_us=statistics.median(deltas),positive_trials=sum(x>0 for x in deltas)))
report=dict(status='exclusive_run_verified',schedules=schedules,selected_schedule_this_run=selected,
    schedule_candidate_event_s=spent,agent=summary,agent_new_kernels=0,
    paired_existing_schedule_comparison=comparison,
    profiler_feedback_limit='Every baseline/schedule candidate produced CUDA profiler traces. All Agent submissions were rejected before evaluation, so no new Agent-candidate profiler feedback occurred; prepared follow-up supplies the measured starting-kernel profile explicitly.',
    contention_source='results/original-hotspot-concurrency.json: 72 original hotspot calls, compared against all981 kernels and12 copies, zero observed overlap.',
    scope='Exclusive GPU by author allocation and sampled foreign-process checks; CPU background load remains. Same six-candidate and60s ceilings, not equal actual spend. No Agent winner or Agent deployment benefit claimed.')
(O/'summary.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
