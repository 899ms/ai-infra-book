"""Verify actual cross-machine write/read and separate native cache hit levels."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results-smoke-004';S=R/'mac-store-smoke-004'
def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(l) for l in p.read_text().splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
execution=read(O/'execution.json');assert len(execution['rows'])==2 and all(r['exit_code']==0 for r in execution['rows']) and not execution['after_gpu'].strip()
ledger=lines(S/'ledger.jsonl');writes=[r for r in ledger if r['path']=='/set'];gets=[r for r in ledger if r['path']=='/get'];assert writes and gets
written={e['key']:e for r in writes for e in r['response']['entries']}
for k,e in written.items():assert (S/(k+'.bin')).stat().st_size==e['bytes'] and sha(S/(k+'.bin'))==e['sha256']
for r in gets:
 for e in r['response']['entries']:
  if e['found']:assert e['sha256']==written[e['key']]['sha256'] and e['bytes']==written[e['key']]['bytes']
records=[];texts=[];tokens=[]
for phase in ['producer','consumer']:
 p=O/phase;raw=read(p/'raw.json');assert raw['status']=='all_requests_returned'
 for n,h in raw['source_hashes'].items():assert sha(R/n)==h,n
 req=lines(p/'requests.jsonl');assert req==raw['requests'] and len(req)==3
 trace=lines(p/'remote.jsonl');assert all(t['error'] is None for t in trace)
 for t in trace:
  assert any(l['path']=='/'+t['op'] and l['request']==t['meta'] and l['request_bytes']==t['request_bytes'] and l['response_bytes']==t['response_bytes'] for l in ledger)
 for i,row in enumerate(req):
  response=row['response'];meta=response['meta_info'];assert meta['prompt_tokens']==1024 and meta['completion_tokens']==16 and meta['num_retractions']==0
  details=meta.get('cached_tokens_details') or dict(device=0,host=0,storage=0)
  assert meta['cached_tokens']==sum(details[k] for k in ['device','host','storage'])
  if phase=='producer' and i==0:assert meta['cached_tokens']==0
  elif phase=='consumer' and i==0:assert details['storage']==1008 and details['device']==details['host']==0
  else:assert details['device']==1008 and details['host']==details['storage']==0
  records.append(dict(phase=phase,index=i,wall_s=row['end_s']-row['start_s'],cached_tokens=meta['cached_tokens'],details=details));texts.append(response['text']);tokens.append(tuple(response['output_ids']))
assert len(set(texts))==len(set(tokens))==1
get_calls=[t for t in lines(O/'consumer/remote.jsonl') if t['op']=='get']
result=dict(status='cross_machine_kv_recovery_verified',requests=records,outputs_identical=True,
    remote_pages=len(written),page_bytes=sorted({e['bytes'] for e in written.values()}),
    consumer_get_operations=len(get_calls),consumer_get_wall_s=sum(t['end_s']-t['start_s'] for t in get_calls),
    consumer_get_HTTP_payload_bytes=sum(t['response_bytes'] for t in get_calls),
    scope='One producer and one fresh consumer, six model requests. Native SGLang dynamic backend over HTTP through SSH, RTX-to-Mac storage. Not a production remote-cache benchmark, physical SSD I/O, representative p95, complete Agent quality, or complete9-9 matrix.',
    artifact_sha256={str(p.relative_to(R)):sha(p) for p in [O/'producer/raw.json',O/'consumer/raw.json',O/'execution.json',S/'ledger.jsonl']})
(R/'smoke-summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
