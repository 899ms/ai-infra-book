import hashlib,json,math
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
s=read(R/'samples.json');raw=read(R/'results/raw.json');ex=read(R/'execution.json');v=read(R/'checkpoint-verification.json')
assert ex['exit_code']==0 and not ex['after_gpu'].strip() and raw['status']=='all_samples_checkpointed'
for p,h in s['source_sha256'].items():assert sha(P/p)==h
for p,h in raw['source_sha256'].items():assert sha(R/p)==h
assert sha(R/'verify_checkpoints.py')==v['source_sha256']
rows=[json.loads(l) for l in (R/'results/events.jsonl').read_text().splitlines()];assert rows==raw['rows'] and len(rows)==12
ledger=[]
for a,b in zip(s['samples'],rows):
 assert a['request_id']==b['request_id'] and a['sample_sha256']==b['sample_sha256'] and b['completed_training_tokens']==len(a['output_ids']) and math.isfinite(b['loss']) and b['gradient_norms']['B']>0
 assert b['adapter_sha256']['B']!=raw['initial_tensor_sha256']['B']
 check=next(x for x in v['checks'] if x['request_id']==a['request_id']);assert check['adam_update_verified'] and check['moments_verified']
 assert sha(R/'results'/(a['request_id']+'.pt'))==check['checkpoint_sha256']==b['checkpoint_sha256']
 ledger.append(dict(request_id=a['request_id'],task=a['task'],strategy=a['strategy'],rep=a['rep'],completed_training_tokens=b['completed_training_tokens'],sample_sha256=a['sample_sha256'],step_and_checkpoint_s=b['end_s']-b['start_s'],loss=b['loss']))
unique={x['sample_sha256']:len(x['output_ids']) for x in s['samples']}
result=dict(status='canonical_batch_training_verified',logical_samples=12,completed_training_tokens=sum(x['completed_training_tokens'] for x in ledger),distinct_content_streams=len(unique),distinct_content_output_tokens=sum(unique.values()),preparation_s=raw['preparation_s'],process_wall_s=raw['end_s']-raw['start_s'],ledger=ledger,scope='Independent supervised adapter checkpoints for explicitly normalized new samples; raw received positions are a different ledger. No live generation-to-training clock or RL improvement.')
assert {x['sample_sha256'] for x in s['samples']}=={x['sample_sha256'] for x in read(P/'training-consumption/samples.json')['samples']}
assert result['completed_training_tokens']==3000 and result['distinct_content_streams']==2
for row in read(R/'normalization.json'):assert row['semantic_content_equal']
(R/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
