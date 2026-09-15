import hashlib,json,math,random,sqlite3,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results';P=R.parent
def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(l) for l in p.read_text().splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def unique(pairs):
 d={}
 for k,v in pairs:assert k not in d;d[k]=v
 return d
execution=read(O/'execution.json');rows=lines(O/'batches.jsonl');assert rows==execution['rows'] and len(rows)==6
for n,h in execution['source_sha256'].items():assert sha(R/n)==h
rng=random.Random(1105);expected=[]
for rep in range(3):
 order=['fixed','additional'];rng.shuffle(order);expected.extend((rep,p) for p in order)
assert [(r['rep'],r['policy']) for r in rows]==expected
baseline=read(P/'formal/summary.json');tasks=read(R/'tasks.json')['formal'];summary=[];samples=[]
for row in rows:
 root=O/f'rep{row["rep"]}-{row["policy"]}';intervals={};gpu_window=0;rtx_phases=None
 for task in tasks:
  d=root/task['id'];reference=next(x for x in baseline['results'] if x['task']==task['id'] and x['strategy']=='baseline')
  if task['id']=='extract' and row['policy']=='additional':
   raw=read(d/'worker/raw.json');receipt=read(d/'receipt.json');ex=read(d/'execution.json');assert ex['exit_code']==0 and not ex['after_gpu'].strip() and receipt['ssh_exit']==0 and raw['status']=='complete'
   for n,h in raw['source_sha256'].items():assert sha(R/n)==h
   conn=sqlite3.connect('file:'+str(d/'manager-receipt.sqlite')+'?mode=ro&immutable=1',uri=True);tokens=conn.execute('select seq,token from tokens order by seq').fetchall();conn.close();ids=[x[1] for x in tokens];assert ids==raw['token_ids'] and [x[0] for x in tokens]==list(range(len(ids)))
   generated=lines(d/'worker/generated.jsonl');assert [g['token'] for g in generated]==ids and generated[-1]['eos'] and not any(g['eos'] for g in generated[:-1])
   text=raw['text'];intervals['extract']=[receipt['start_s'],receipt['manager_committed_s']];gpu_window=receipt['remote_command_returned_s']-receipt['start_s']
   assert receipt['received_tokens']==len(ids);allocated=ex['end_unix']-ex['start_unix'];assert allocated>0
   rtx_phases=dict(model_preparation_s=raw['ready_s']-raw['start_s'],generation_s=raw['end_s']-raw['ready_s'],after_ssh_return_to_manager_commit_s=receipt['manager_committed_s']-receipt['remote_command_returned_s'])
  else:
   ex=read(d/'execution.json');assert len(ex)==1 and ex[0]['returncode']==0 and not ex[0]['leftover'] and ex[0]['killed'] is None
   conn=sqlite3.connect('file:'+str(d/'manager-snapshot.sqlite')+'?mode=ro&immutable=1',uri=True);tokens=conn.execute('select seq,token from tokens order by seq').fetchall();conn.close();ids=[x[1] for x in tokens];assert [x[0] for x in tokens]==list(range(len(ids)))
   generated=lines(d/'attempt-0/generated.jsonl');assert [x['token'] for x in generated]==ids and generated[-1]['eos'];assert ids==reference['token_ids'];text=reference['text'];intervals[task['id']]=[ex[0]['start'],ex[0]['end']]
   events=lines(d/'manager-events.jsonl');commits=[x for x in events if x['kind']=='committed'];assert len(commits)==len(ids) and not any(x['duplicate'] for x in commits)
  parsed=json.loads(text,object_pairs_hook=unique);assert parsed==task['expected']
  if task['id']=='sequence':assert all(type(x)==int for x in parsed)
  else:assert list(parsed)==list(task['expected'])
  assert row['start_s']<=intervals[task['id']][0]<=intervals[task['id']][1]<=row['end_s']
  samples.append(dict(rep=row['rep'],policy=row['policy'],task=task['id'],generated_tokens=len(ids),manager_received_tokens=len(ids),tokens_equal_original=ids==reference['token_ids'],quality_passed=True,completed_training_tokens=None))
 overlap=max(0,min(x[1] for x in intervals.values())-max(x[0] for x in intervals.values()))
 if row['policy']=='additional':assert overlap>0
 else:assert overlap==0
 wall=row['end_s']-row['start_s'];summary.append(dict(rep=row['rep'],policy=row['policy'],batch_wall_s=wall,worker_intervals=intervals,rtx_phases=rtx_phases,interval_overlap_s=overlap,rtx_requested_window_s=gpu_window,teaching_cost_mac1_rtx1_per_hour=(wall+gpu_window)/3600))
paired=[]
for rep in range(3):
 f=next(x for x in summary if x['rep']==rep and x['policy']=='fixed');a=next(x for x in summary if x['rep']==rep and x['policy']=='additional')
 paired.append(dict(rep=rep,fixed_s=f['batch_wall_s'],additional_s=a['batch_wall_s'],time_saved_s=f['batch_wall_s']-a['batch_wall_s'],extra_teaching_cost=a['teaching_cost_mac1_rtx1_per_hour']-f['teaching_cost_mac1_rtx1_per_hour']))
result=dict(status='additional_physical_device_batches_verified',batches=summary,samples=samples,paired=paired,scope='Heterogeneous MacMLX4bit+RTXBF16 versus Mac alone; existing disk weights, fresh engines. Fixed Mac reserved whole batch; RTX teaching allocation uses SSH command window, not measured GPU busy time or invoice. Completed-training tokens for these new samples remain unknown. Earlier preserved-prefix measurements remain separate.')
(R/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(paired,indent=2))
