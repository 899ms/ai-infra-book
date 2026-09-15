"""Audit raw request, page, publication and lifecycle evidence without cross-host clock subtraction."""
import hashlib,json,math,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results';S=R/'mac-store'
def read(p):return json.loads(p.read_text())
def lines(p):return [json.loads(l) for l in p.read_text().splitlines()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def p95(a):return sorted(a)[math.ceil(.95*len(a))-1] if a else None
execution=read(O/'execution.json');assert len(execution['rows'])==2 and all(r['exit_code']==0 for r in execution['rows']) and not execution['after_gpu'].strip()
transport=read(R/'transport-execution.json');assert transport['ssh_exit']==0 and transport['store_exit']==-15
ledger=lines(S/'ledger.jsonl');writes=[r for r in ledger if r['path']=='/set'];gets=[r for r in ledger if r['path']=='/get']
written={e['key']:e for r in writes for e in r['response']['entries']}
for k,e in written.items():assert (S/(k+'.bin')).stat().st_size==e['bytes'] and sha(S/(k+'.bin'))==e['sha256']
for r in gets:
 for e in r['response']['entries']:
  if e['found']:assert e['sha256']==written[e['key']]['sha256'] and e['bytes']==written[e['key']]['bytes']
collisions=[e for r in writes for e in r['response']['entries'] if e['collision']]
for e in collisions:
 p=S/'collisions'/(e['key']+'-'+e['incoming_sha256'][:12]+'.bin');assert sha(p)==e['incoming_sha256'] and p.stat().st_size==e['bytes']
inputs=read(R/'inputs.json')
for source,h in inputs['source_sha256'].items():assert sha(Path(source))==h
records=[];phases={};paired=[]
for kind,n in [('chat',4)]:
 for phase in ['producer','consumer']:
  name=kind+'-'+phase;p=O/name;raw=read(p/'raw.json');assert raw['status']=='all_requests_returned'
  for key,h in raw['source_hashes'].items():assert sha(R/key)==h
  requests=lines(p/'requests.jsonl');assert requests==raw['requests'] and len(requests)==n
  barriers=lines(p/'barriers.jsonl');assert len(barriers)==n
  trace=lines(p/'remote.jsonl');assert all(t['error'] is None for t in trace)
  for t in trace:assert any(l['path']=='/'+t['op'] and l['request']==t['meta'] and l['request_bytes']==t['request_bytes'] and l['response_bytes']==t['response_bytes'] for l in ledger)
  phase_rows=[];previous_end=None
  for item,row,barrier in zip([x for x in inputs['requests'] if x['kind']==kind],requests,barriers):
   assert item['turn']==row['turn']==barrier['turn'] and len(item['input_ids'])==row['input_tokens']
   ids=item['input_ids'];prev=None;expected=[]
   for offset in range(0,((len(ids)-1)//16)*16,16):
    h=hashlib.sha256()
    if prev:h.update(bytes.fromhex(prev))
    for token in ids[offset:offset+16]:h.update(token.to_bytes(4,'little'))
    prev=h.hexdigest();expected.append(prev+'_'+raw['config']['model_path'].replace('/','-')+'_0_1')
   assert expected==row['expected_reusable_keys'];assert all(k in written for k in expected)
   final=barrier['observations'][-1];assert final['expected']==final['present']==len(expected)
   meta=row['response']['meta_info'];assert meta['prompt_tokens']==len(ids) and meta['completion_tokens']==1 and meta['num_retractions']==0
   details=meta.get('cached_tokens_details') or dict(device=0,host=0,storage=0)
   assert meta['cached_tokens']==sum(details[k] for k in ['device','host','storage'])
   relevant=[t for t in trace if t['op']=='get' and row['start_s']<=t['start_s']<=t['end_s']<=row['end_s']]
   rec=dict(kind=kind,phase=phase,turn=row['turn'],input_tokens=len(ids),cached_tokens=meta['cached_tokens'],details=details,wall_s=row['end_s']-row['start_s'],get_rpc_count=len(relevant),get_rpc_sum_s=sum(t['end_s']-t['start_s'] for t in relevant),get_rpc_p95_s=p95([t['end_s']-t['start_s'] for t in relevant]))
   rec['replay_gap_since_previous_response_s']=row['start_s']-previous_end if previous_end is not None else None
   previous_end=row['end_s']
   records.append(rec);phase_rows.append(rec)
  phases[name]=dict(requests=n,request_hit_fraction=sum(r['cached_tokens']>0 for r in phase_rows)/n,token_hit_fraction=sum(r['cached_tokens'] for r in phase_rows)/sum(r['input_tokens'] for r in phase_rows),wall_s=sum(r['wall_s'] for r in phase_rows),request_p95_s=p95([r['wall_s'] for r in phase_rows]),levels={k:sum(r['details'][k] for r in phase_rows) for k in ['device','host','storage']})
  assert sum(r['get_rpc_count'] for r in phase_rows)==sum(t['op']=='get' for t in trace)
  retrieval=[r['get_rpc_sum_s'] for r in phase_rows if r['get_rpc_count']]
  phases[name]['requests_with_remote_get']=len(retrieval)
  phases[name]['per_request_get_sum_median_s']=statistics.median(retrieval) if retrieval else None
  phases[name]['per_request_get_sum_p95_s']=p95(retrieval)
  phases[name]['retrieval_quantile_scope']='Sum of successful GET RPC times within each request; excludes exists checks, scheduling and model work. Descriptive nearest-rank sample.'
 for a,b in zip(lines(O/(kind+'-producer')/'requests.jsonl'),lines(O/(kind+'-consumer')/'requests.jsonl')):
  paired.append(dict(kind=kind,turn=a['turn'],output_ids_equal=a['response']['output_ids']==b['response']['output_ids'],producer_output_ids=a['response']['output_ids'],consumer_output_ids=b['response']['output_ids']))
 assert phases[kind+'-consumer']['levels']['storage']>0
result=dict(status='multi_turn_remote_replay_verified',phases=phases,requests=records,paired_outputs=paired,all_paired_outputs_equal=all(p['output_ids_equal'] for p in paired),published_pages=len(written),get_operations=len(gets),conflicting_duplicate_writes=len(collisions),conflicting_keys_read=sorted({e['key'] for e in collisions}&{e['key'] for r in gets for e in r['response']['entries'] if e['found']}),scope='One recorded Chat trace at threshold16 with forced one-token responses. Publication barriers instrument replay and are not original think times. Quantiles are nearest-rank descriptive samples; no full task-quality or stable p95 claim. No three-policy remote routing comparison in this run.')
(R/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='requests'},indent=2))
