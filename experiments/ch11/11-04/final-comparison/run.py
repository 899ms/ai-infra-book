import hashlib,json,math
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent
paths=['formal/summary.json','training-consumption/summary.json','additional-device/summary.json','canonical-training/summary.json','model-identity.json','cost-replay/results.json']
def read(p):return json.loads(p.read_text())
a,b,c,d,identity,old=[read(P/p) for p in paths];rows=[]
for batch in c['batches']:
 train=[x for x in d['ledger'] if x['rep']==batch['rep'] and x['strategy']==batch['policy']];assert len(train)==2
 t=d['preparation_s']+sum(x['step_and_checkpoint_s'] for x in train)
 rows.append(dict(arrangement=batch['policy'],rep=batch['rep'],cut=None,generation_s=batch['batch_wall_s'],composed_training_s=t,composed_total_s=batch['batch_wall_s']+t,completed_tasks=2,trained_output_positions=sum(x['completed_training_tokens'] for x in train),training_stream='canonical',teaching_total_cost=batch['teaching_cost_mac1_rtx1_per_hour']+t/3600,measurement_scope='Measured new batch plus separately measured cold-consumer stage composition'))
for cut in [32,96]:
 for strategy in ['restart','preserve']:
  gen=[x for x in a['results'] if x['cut']==cut and x['strategy']==strategy];train=[x for x in b['ledger'] if x['cut']==cut and x['strategy']==strategy];assert len(gen)==len(train)==2
  t=b['preparation_s']+sum(x['training_step_and_checkpoint_s'] for x in train);g=sum(x['wall_s'] for x in gen)
  rows.append(dict(arrangement=strategy,rep=None,cut=cut,generation_s=g,composed_training_s=t,composed_total_s=g+t,completed_tasks=2,trained_output_positions=sum(x['completed_training_tokens'] for x in train),sampled_tokens=sum(x['sampled_tokens'] for x in gen),received_positions=sum(x['unique_tokens'] for x in gen),rebuilt_prefix_positions=sum(x['recovered_prefix_tokens'] for x in train),teaching_total_cost=(g+t)/3600,measurement_scope='Sum of original per-task interrupted windows plus separate cold-consumer stage composition'))
life=[];sensitivity=[];source_extra={}
for batch in [x for x in c['batches'] if x['policy']=='additional']:
 rep=batch['rep'];base=P/'additional-device/results'/f'rep{rep}-additional/extract/worker';raw=read(base/'raw.json');events=[json.loads(l) for l in (base/'generated.jsonl').read_text().splitlines()]
 for p in [base/'raw.json',base/'generated.jsonl']:source_extra[str(p.relative_to(P))]=hashlib.sha256(p.read_bytes()).hexdigest()
 D=raw['ready_s']-raw['start_s'];g=raw['end_s']-raw['ready_s'];end=raw['end_s']-raw['start_s']
 for L in [5,20,40,50,60,90,120]:
  generated=sum(x['end_s']-raw['start_s']<=L for x in events)
  life.append(dict(rep=rep,lifetime_s=L,generated_tokens=generated,completed_artifact_before_cutoff=L>=end,receivable_output_positions=len(raw['token_ids']) if L>=end else 0,completed_training_positions=None,scope='Recorded timeline cutoff, not another physical kill; receipt follows final transfer'))
 fixed=next(x for x in c['batches'] if x['rep']==rep and x['policy']=='fixed');m=fixed['worker_intervals']['extract'][1]-fixed['worker_intervals']['extract'][0]
 # Snapshot path is part of the recorded fixed revision, queried on RTX and sealed separately.
 weights=read(R/'rtx-weight-identity.json');W=weights['weight_bytes']
 for transfer in [False,True]:
  prep=D+(W/1e9 if transfer else 0)
  for ratio in [.1,.3,1.]:
   factor=ratio*g/m;boundary=prep/(1-factor) if factor<1 else None;grid=[]
   for L in [20,40,60,90,120,240,600]:
    n=max(0,math.floor((L-prep)/g));cost=ratio*L/3600;fixedcost=n*m/3600
    grid.append(dict(lifetime_s=L,complete_task_budget=n,extra_cost=cost,equivalent_mac_cost=fixedcost,cheaper=n>0 and cost<fixedcost))
   sensitivity.append(dict(rep=rep,cold_weight_transfer=transfer,declared_link_bytes_s=1e9 if transfer else None,weight_bytes=W,preparation_s=prep,rtx_seconds_per_task=g,mac_seconds_per_task=m,extra_to_mac_price_ratio=ratio,fluid_strict_boundary_s=boundary,first_task_ready_s=prep+g,rows=grid))
result=dict(status='integrated_record_comparison_verified',arrangements=rows,lifetime_replay=life,price_lifetime_sensitivity=sensitivity,old_mac_weight_bytes=old['teaching_model']['weight_bytes'],source_sha256={**{p:hashlib.sha256((P/p).read_bytes()).hexdigest() for p in paths},**source_extra,**{'final-comparison/'+n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['rtx-weight-identity.json','run.py','PROTOCOL.md']}},scope='Measured stages and explicit compositional teaching scenarios. Not a single live four-arm end-to-end trial, new cutoff fault injection, or invoice.')
(R/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(rows,indent=2))
