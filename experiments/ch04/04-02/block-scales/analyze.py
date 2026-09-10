import hashlib,json,statistics
from pathlib import Path
r=Path(__file__).absolute().parent;p=r/'results';env=json.loads((p/'environment.json').read_text());assert env['source_sha256']==hashlib.sha256((r/'run.py').read_bytes()).hexdigest();assert env['expert_sha256']==hashlib.sha256((r/'expert.pt').read_bytes()).hexdigest()
rows=json.loads((p/'raw.json').read_text());assert len(rows)==12
assert {(x['variant'],x['phase'],x['m']) for x in rows}=={(v,phase,m) for v in ['activation','both'] for phase,m in [('prefill',1),('prefill',8),('prefill',64),('prefill',512),('decode',1),('decode',8)]}
result=[]
for x in rows:
 assert x['integer_exact'];assert len(x['samples'])==36
 for q in x['checks'].values():assert q['passed']==(q['relative_l2']<=.02)
 stages={}
 for stage in ['direct','dequant','activation_quant','weight_dequant']:
  a=[s for s in x['samples'] if s['stage']==stage];assert sorted(y['trial'] for y in a)==list(range(9))
  assert all(y['device_ms']>0 and y['wall_ms']>0 for y in a)
  stages[stage]={k:dict(median=statistics.median(y[k] for y in a),min=min(y[k] for y in a),max=max(y[k] for y in a)) for k in ['device_ms','wall_ms']}
 trace=json.loads((p/(x['label']+'-trace.json')).read_text())['traceEvents'];names={z.get('name') for z in trace};assert 'direct' in names and 'dequant' in names;kernels=[z for z in trace if z.get('cat')=='kernel'];assert kernels
 result.append(dict(label=x['label'],variant=x['variant'],phase=x['phase'],m=x['m'],checks=x['checks'],stages=stages,kernel_events=len(kernels),weight_scale_unique_storage_bytes=x['weight_scale_unique_storage_bytes'],activation_scale_bytes=x['activation_scale_bytes']))
(p/'summary.json').write_text(json.dumps(dict(conditions=result,scope='Actual observed inputs; group size fixed at128; 16 INT8 partial products versus one BF16 product after reconstruction; no model-level quality or optimal kernel claim.'),indent=2)+'\n')
for x in result:print(x['label'],{k:round(v['relative_l2']*100,4) for k,v in x['checks'].items()},[round(x['stages'][k]['device_ms']['median']*1000,2) for k in ['direct','dequant']])
