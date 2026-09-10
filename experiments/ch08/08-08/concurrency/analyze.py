import hashlib,json,math,statistics,re
from pathlib import Path
r=Path(__file__).absolute().parent
reports=[];reference=None;outputs={}

def unique(pairs):
 d={}
 for k,v in pairs:
  if k in d:raise ValueError('duplicate')
  d[k]=v
 return d

for name in ['bf16','fp8']:
 p=r/'results'/name;env=json.loads((p/'environment.json').read_text())
 for n,h in env['hashes'].items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
 assert hashlib.sha256((p/'inputs.json').read_bytes()).hexdigest()==env['input_sha256']
 inp=json.loads((p/'inputs.json').read_text());tasks={t['id']:t for t in inp['tasks']}
 for t in tasks.values():
  document=dict(re.findall(r'^(k\d{4}) = (\d{6})$',t['messages'][1]['content'],re.M))
  assert len(document)==t['rows'] and all(document[k]==v for k,v in t['expected'].items())
 snap=json.loads((p/'kv-snapshots.json').read_text());weights=snap['weights'][0]
 assert sum(x['dtype']=='torch.float8_e4m3fn' for x in weights['parameters'])==144
 config=dict(env['config']);config.pop('kv_cache_dtype')
 if reference is None:reference=(weights,inp,config)
 else:assert reference==(weights,inp,config)
 assert snap['after_calibration'][0]['scales']==snap['after'][0]['scales']
 scales=snap['after_calibration'][0]['scales'];assert len(scales)==36
 assert all(not s['calculate'] and math.isfinite(s['k']) and math.isfinite(s['v']) and s['k']>0 and s['v']>0 and s['backend']=='TritonAttentionImpl' for s in scales)
 if name=='fp8':assert snap['armed_layers']==[36] and scales!=snap['before'][0]['scales']
 rows=[json.loads(x) for x in (p/'requests.jsonl').read_text().splitlines()]
 batches=[json.loads(x) for x in (p/'batches.jsonl').read_text().splitlines()]
 stats=[json.loads(x) for x in (p/'engine-stats.jsonl').read_text().splitlines()]
 assert len(rows)==269 and len(batches)==21
 assert len({x['id'] for x in rows})==269
 formal=[b for b in batches if b['trial']!='warm']
 assert {(b['trial'],b['concurrency'],b['mode']) for b in formal}=={(i,c,m) for i in [0,1] for c in [7,8,15,16,20] for m in ['natural','fixed']}
 evaluated=[]
 for b in batches:
  group=[x for x in rows if x['id'].startswith(b['id']+'-')];assert len(group)==b['concurrency']
  records=[x for x in stats if x['batch']==b['id']];assert records
  for x in group:
   if x['mode']=='fixed':assert len(x['output_ids'])==64 and x['finish_reason']=='length'
   try:correct=json.loads(x['text'],object_pairs_hook=unique)==tasks[x['task_id']]['expected']
   except (ValueError,TypeError):correct=False
   first=next(t for t,n in x['events'] if n>0)
   x.update(strict_correct=correct if x['mode']=='natural' else None,latency_s=x['end_s']-x['start_s'],ttft_s=first-x['start_s'])
  peak_running=max(x['scheduler']['num_running_reqs'] for x in records)
  peak_waiting=max(x['scheduler']['num_waiting_reqs'] for x in records)
  peak_usage=max(x['scheduler']['kv_cache_usage'] for x in records)
  preempt=sum((x['iteration'] or {}).get('num_preempted_reqs',0) for x in records)
  evaluated.append(dict(**b,requests=len(group),correct=sum(x['strict_correct'] is True for x in group) if b['mode']=='natural' else None,
   finish_reasons={k:sum(x['finish_reason']==k for x in group) for k in set(x['finish_reason'] for x in group)},
   median_latency_s=statistics.median(x['latency_s'] for x in group),median_ttft_s=statistics.median(x['ttft_s'] for x in group),
   median_engine_queue_s=statistics.median(x['metrics']['scheduled_ts']-x['metrics']['queued_ts'] for x in group),
   output_tokens=sum(len(x['output_ids']) for x in group),peak_running=peak_running,peak_waiting=peak_waiting,peak_kv_usage=peak_usage,
   preemptions=preempt,stats_records=len(records),errors=[dict(id=x['id'],task=x['task_id'],text=x['text']) for x in group if x['strict_correct'] is False]))
 outputs[name]={x['id']:x['output_ids'] for x in rows if x['id'][0].isdigit()}
 repeat_differences=[k for k,v in outputs[name].items() if k.startswith('0-') and outputs[name]['1-'+k[2:]]!=v]
 report=dict(name=name,repeat_output_differences=repeat_differences,batches=evaluated,kv_storage=snap['after_calibration'][0]['unique_kv_storage_bytes'],
  kv_tensors=snap['after_calibration'][0]['kv_tensors'],
  formal_requests=sum(b['requests'] for b in evaluated if b['trial']!='warm'),
  formal_correct=sum(b['correct'] or 0 for b in evaluated if b['trial']!='warm'),
  formal_preemptions=sum(b['preemptions'] for b in evaluated if b['trial']!='warm'))
 assert sum((x['iteration'] or {}).get('num_preempted_reqs',0) for x in stats)==sum(b['preemptions'] for b in evaluated)
 reports.append(report)
 print(name,'formal',report['formal_requests'],'correct',report['formal_correct'],'preemptions',report['formal_preemptions'])
 for b in evaluated:
  if b['trial']!='warm':print(b['id'],b['correct'],b['peak_running'],b['peak_waiting'],round(b['peak_kv_usage'],4),b['preemptions'],round(b['median_latency_s'],3))
(r/'results/summary.json').write_text(json.dumps(dict(configurations=reports,between_format_output_differences=[k for k,v in outputs['bf16'].items() if outputs['fp8'][k]!=v],scope='Shared GPU; repeated four long-document tasks; running includes partial prefill; successful queue admission is not simultaneous full-context residency.'),indent=2)+'\n')
