import hashlib,json,math,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
samples=read(R/'samples.json');raw=read(R/'results/raw.json');execution=read(R/'execution.json')
assert execution['exit_code']==0 and not execution['after_gpu'].strip() and raw['status']=='all_samples_checkpointed'
for n,h in samples['source_sha256'].items():assert sha(P/n)==h
for n,h in raw['source_sha256'].items():assert sha(R/n)==h
rows=[json.loads(l) for l in (R/'results/events.jsonl').read_text().splitlines()];assert rows==raw['rows'] and len(rows)==len(samples['samples'])==12
formal=read(P/'formal/summary.json');ledger=[]
for s,r in zip(samples['samples'],rows):
 assert s['request_id']==r['request_id'] and s['sample_sha256']==r['sample_sha256']
 assert r['completed_training_tokens']==len(s['output_ids'])==s['manager_unique_tokens'] and r['optimizer_step']==1
 assert math.isfinite(r['loss']) and r['gradient_norms']['B']>0 and all(math.isfinite(x) for x in r['gradient_norms'].values())
 assert r['adapter_sha256']['B']!=raw['initial_tensor_sha256']['B']
 assert sha(R/'results'/(s['request_id']+'.pt'))==r['checkpoint_sha256']
 f=next(x for x in formal['results'] if x['request_id']==s['request_id'])
 ledger.append(dict(request_id=s['request_id'],task=s['task'],strategy=s['strategy'],cut=s['cut'],sampled_tokens=s['sampled_tokens'],manager_unique_tokens=s['manager_unique_tokens'],duplicate_deliveries=s['duplicate_deliveries'],recovered_prefix_tokens=sum(w['prefix_rebuild_tokens'] for w in f['workers']),completed_training_tokens=r['completed_training_tokens'],training_step_and_checkpoint_s=r['end_s']-r['start_s'],checkpoint_sha256=r['checkpoint_sha256']))
paired=[]
for task in ['extract','sequence']:
 a=[r for r in rows if r['request_id'].startswith(task+'-')]
 paired.append(dict(task=task,logical_samples=len(a),adapter_tensors_identical=len({json.dumps(r['adapter_sha256'],sort_keys=True) for r in a})==1,losses=[r['loss'] for r in a]))
result=dict(status='durable_adapter_training_consumption_verified',logical_samples=12,distinct_prompt_output_contents=len({s['sample_sha256'] for s in samples['samples']}),sampled_tokens=sum(x['sampled_tokens'] for x in ledger),manager_unique_tokens=sum(x['manager_unique_tokens'] for x in ledger),completed_training_tokens=sum(x['completed_training_tokens'] for x in ledger),unique_content_output_tokens=sum(len(next(s for s in samples['samples'] if s['sample_sha256']==h)['output_ids']) for h in {s['sample_sha256'] for s in samples['samples']}),preparation_s=raw['preparation_s'],trainable_parameters=raw['trainable_parameters'],cuda_peak_allocated_bytes=raw['cuda_peak_allocated_bytes'],training_process_wall_s=raw['end_s']-raw['start_s'],ledger=ledger,paired=paired,scope='12 independent one-step adapter optimizer checkpoints, not sequential12-step or RL training. Generation MLX4bit and consumer BF16 artifacts differ. Counts denote logical request positions; content duplicated across trials is separately counted.')
(R/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
