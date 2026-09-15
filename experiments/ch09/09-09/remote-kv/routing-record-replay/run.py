import hashlib,json,math,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;K=R.parent;B=K.parent
paths=[K/'cross-mac-traces-001/summary.json',K/'cross-mac-chat-threshold16-001/summary.json',K/'trace-cold-control-001/summary.json',K/'cross-mac-005/summary.json',B/'queue-pressure/summary.json',B/'completion-prediction/model.json',R/'PROTOCOL.md',R/'run.py']
def read(p):return json.loads(p.read_text())
def p95(a):return sorted(a)[math.ceil(.95*len(a))-1] if a else None
normal=read(paths[0]);chat=read(paths[1]);cold=read(paths[2]);cal=read(paths[3]);queues=read(paths[4]);warm=read(paths[5])
assert normal['all_paired_outputs_equal'] and chat['all_paired_outputs_equal'] and cold['all_repeated_outputs_equal']
page_s=cal['consumer_get_wall_s']/cal['consumer_get_operations'];records=[];states=[]
for source,kind,threshold in [(chat,'chat',16),(normal,'agent',256)]:
 for r in [x for x in source['requests'] if x['phase']=='consumer' and x['kind']==kind]:
  c=next(x for x in cold['per_input'] if (x['kind'],x['turn'])==(kind,r['turn']))
  out=next(x for x in source['paired_outputs'] if (x['kind'],x['turn'])==(kind,r['turn']))
  assert all(x==out['consumer_output_ids'] for x in c['output_ids'])
  reusable=(r['input_tokens']-1)//16*16;device=r['details']['device'];missing=reusable-device
  remote=missing if missing>=threshold else 0
  assert remote==r['details']['storage']
  estimate_cache=c['wall_s'][0]+remote/16*page_s if remote else (warm['warm_after_busy_s'] if device else c['wall_s'][0])
  states.append(dict(kind=kind,turn=r['turn'],input_tokens=r['input_tokens'],device_tokens=device,eligible_remote_tokens=remote,threshold=threshold,calibrated_cache_s=estimate_cache,calibrated_cold_s=c['wall_s'][0],observed_cache_s=r['wall_s'],heldout_cold_s=c['wall_s'][1:],replay_gap_s=r['replay_gap_since_previous_response_s']))
  for qi,q in enumerate(queues['rows']):
   for busy in ['cache','cold']:
    queue={k:q['busy_remaining_at_dispatch_s'] if k==busy else 0. for k in ['cache','cold']}
    hits={'cache':device+remote,'cold':0};estimate={'cache':estimate_cache,'cold':c['wall_s'][0]}
    for rep in [1,2]:
     for policy in ['queue_first','cache_first','predicted_completion']:
      order=['cold','cache']
      if policy=='queue_first':selected=min(order,key=lambda k:queue[k])
      elif policy=='cache_first':selected=min(order,key=lambda k:(-hits[k],queue[k]))
      else:selected=min(order,key=lambda k:queue[k]+estimate[k])
      decision=dict(kind=kind,turn=r['turn'],queue_source_row=qi,busy=busy,cold_pass=rep,policy=policy,queue_s=queue,estimated_service_s=estimate,available_cache_tokens=hits,selected=selected)
      service={'cache':r['wall_s'],'cold':c['wall_s'][rep]};realized={k:queue[k]+service[k] for k in order}
      decision.update(input_tokens=r['input_tokens'],completion_s=realized[selected],alternative_completion_s=realized,regret_s=realized[selected]-min(realized.values()),prediction_error_s=estimate[selected]-service[selected],cached_tokens=hits[selected],levels=r['details'] if selected=='cache' else dict(device=0,host=0,storage=0),get_rpc_sum_s=r['get_rpc_sum_s'] if selected=='cache' else 0.)
      assert decision['regret_s']>=0 and decision['cached_tokens']==sum(decision['levels'][k] for k in ['device','host','storage'])
      records.append(decision)
assert len(records)==1152
summary=[]
for kind in ['chat','agent']:
 for busy in ['cache','cold']:
  for policy in ['queue_first','cache_first','predicted_completion']:
   a=[r for r in records if (r['kind'],r['busy'],r['policy'])==(kind,busy,policy)];get=[r['get_rpc_sum_s'] for r in a if r['get_rpc_sum_s']]
   summary.append(dict(kind=kind,busy=busy,policy=policy,decisions=len(a),cache_selections=sum(r['selected']=='cache' for r in a),mean_completion_s=statistics.mean(r['completion_s'] for r in a),mean_regret_s=statistics.mean(r['regret_s'] for r in a),max_regret_s=max(r['regret_s'] for r in a),mean_absolute_prediction_error_s=statistics.mean(abs(r['prediction_error_s']) for r in a),request_hit_rate=sum(r['cached_tokens']>0 for r in a)/len(a),token_hit_rate=sum(r['cached_tokens'] for r in a)/sum(r['input_tokens'] for r in a),levels={k:sum(r['levels'][k] for r in a) for k in ['device','host','storage']},selected_get_sum_sample_p95_s=p95(get)))
result=dict(status='record_replay_completed',source_sha256={str(p.relative_to(B)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},page_calibration_s=page_s,states=states,summary=summary,decisions=records,scope='Independent additive queue scenarios composed from real records. Not newly measured concurrent or state-evolving routing. Repeated source values do not create independent p95 samples.')
(R/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary,indent=2))
