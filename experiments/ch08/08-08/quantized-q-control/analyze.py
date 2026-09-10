import hashlib,json,statistics
from pathlib import Path
root=Path(__file__).parent;r=root/'reference';p=root/'results'/'fp8_qbf16'
env=json.loads((p/'environment.json').read_text())
for name,digest in env['hashes'].items():assert hashlib.sha256((root/name).read_bytes()).hexdigest()==digest
original=json.loads((r/'fp8/environment.json').read_text());expected=dict(original['config']);expected['worker_extension_cls']='probe_qbf16.KVQBF16Probe'
assert env['config']==expected and env['input_sha256']==original['input_sha256']
assert hashlib.sha256((p/'inputs.json').read_bytes()).hexdigest()==env['input_sha256']
snaps=json.loads((p/'kv-snapshots.json').read_text());base=json.loads((r/'fp8/kv-snapshots.json').read_text())
assert snaps['weights']==base['weights']
assert snaps['q_override_layers']==[36]
assert snaps['after_calibration'][0]['scales']==base['after_calibration'][0]['scales']==snaps['after'][0]['scales']
assert all(not x['enabled'] for x in snaps['after_q_override'][0]['query_quantization'])
dtypes=snaps['after'][0]['observed_query_dtypes'];assert len(dtypes)==36 and set(dtypes.values())=={'torch.bfloat16'}
import re
inputs={x['id']:x for x in json.loads((p/'inputs.json').read_text())['tasks']}
for t in inputs.values():
 doc=dict(re.findall(r'^(k\d{4}) = (\d{6})$',t['messages'][1]['content'],re.M))
 assert len(doc)==t['rows'] and all(doc[k]==v for k,v in t['expected'].items())
for item in json.loads((r/'index.json').read_text()):
 assert hashlib.sha256((root/item['file']).read_bytes()).hexdigest()==item['sha256']
assert len(snaps['after'][0]['query_dtype_counts'])==36
assert all(k.endswith(':torch.bfloat16') and v>0 for k,v in snaps['after'][0]['query_dtype_counts'].items())
rows=[json.loads(x) for x in (p/'requests.jsonl').read_text().splitlines()]
batches=[json.loads(x) for x in (p/'batches.jsonl').read_text().splitlines()]
assert len(rows)==97 and len(batches)==24
records=[]
def unique_object(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('Duplicate key')
  d[k]=v
 return d
for batch in batches:
 group=[x for x in rows if x['id'].startswith(batch['id']+'-')];assert len(group)==4
 for x in group:
  if batch['trial']=='warm':continue
  if x['mode']=='fixed':assert len(x['output_ids'])==64
  try:parsed=json.loads(x['text'],object_pairs_hook=unique_object)
  except (ValueError,TypeError):parsed=None
  records.append(dict(id=x['id'],task_id=x['task_id'],rows=batch['rows'],concurrency=batch['concurrency'],mode=x['mode'],trial=batch['trial'],
    correct=parsed==inputs[x['task_id']]['expected'] if x['mode']=='natural' else None,parsed=parsed,
    output_tokens=len(x['output_ids']),finish_reason=x['finish_reason'],elapsed_s=x['end_s']-x['start_s']))
summary=[]
for n in [128,512]:
 for concurrency in [1,4]:
  group=[x for x in records if x['mode']=='natural' and (x['rows'],x['concurrency'])==(n,concurrency)];assert len(group)==8
  summary.append(dict(rows=n,concurrency=concurrency,correct=sum(x['correct'] for x in group),requests=8,
    output_tokens=sum(x['output_tokens'] for x in group),truncated=sum(x['finish_reason']=='length' for x in group),median_elapsed_s=statistics.median(x['elapsed_s'] for x in group)))
comparisons={}
control={x['id']:x for x in rows if x['id'][0].isdigit()}
for name in ['bf16','fp8']:
 ref={x['id']:x for x in map(json.loads,(r/name/'requests.jsonl').read_text().splitlines()) if x['id'][0].isdigit()}
 assert ref.keys()==control.keys()
 comparisons[name]=[k for k in ref if ref[k]['output_ids']!=control[k]['output_ids']]
repeat_differences=[k for k,x in control.items() if k.startswith('0-') and x['output_ids']!=control['1-'+k[2:]]['output_ids']]
(root/'results'/'q-control-summary.json').write_text(json.dumps(dict(summary=summary,records=records,output_differences_against=comparisons,repeat_output_differences=repeat_differences,query_dtype_counts=snaps['after'][0]['query_dtype_counts'],
    q_dtype_observed=dtypes,calibrated_kv_scales_match=True,scope='Instrumented Q-BF16 control, same FP8 KV calibration. Eight distinct tasks; quality comparison; additional Python dtype-observation overhead included in time.'),indent=2)+'\n')
for x in summary:print(json.dumps(x))
print('Output differences vs BF16 / default FP8', {k:len(v) for k,v in comparisons.items()})
