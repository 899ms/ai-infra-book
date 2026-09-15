"""Independent triplet request coverage, replacement, token and exclusivity checks."""
import hashlib,json,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
completion=read(O/'completion.json')
for f,h in completion['source_hashes'].items():assert sha(R/f)==h,f
assert not read(O/'before.json')['apps'].strip() and not read(O/'after.json')['pids']
assert len(read(O/'execution.json'))==3 and all(r['exit_code']==0 for r in read(O/'execution.json'))
for p in O.glob('*-gpu.jsonl'):
 rows=[json.loads(l) for l in p.read_text().splitlines()];assert rows and all(not r['foreign_pids'] for r in rows)
allpairs=[];engines=[];modes=['native','schedule','agent']
for engine in range(3):
 p=O/f'requests-{engine}';raw=read(p/'raw.json');assert raw['status']=='passed'
 for f,h in raw['source_hashes'].items():assert sha(R/f)==h
 assert raw['config']['enforce_eager'] and not raw['config']['enable_prefix_caching']
 assert len(raw['installed'][0]['layer_names'])==36
 assert {r['mode'] for r in raw['audits']}==set(modes)
 for audit in raw['audits']:
  records=audit['records'][0];assert len(records)==72
  assert len({r['layer'] for r in records})==36
  assert sum(r['shape']==[7239,24576] for r in records)==36
  assert sum(r['shape']==[1,24576] for r in records)==36
  assert all(r['mode']==audit['mode'] and r['dtype']=='torch.bfloat16' for r in records)
 for switch in raw['switches']:
  s=switch[0];assert not s['audit'] and s['layers']==36
  expected={'native':'vllm.model_executor.layers.activation','schedule':'candidate','agent':'agent_candidate'}[s['mode']]
  assert all(m['module']==expected for m in s['methods'])
 req=[r for r in raw['requests'] if r['phase']=='measure'];assert len(req)==33
 assert [json.loads(l) for l in (p/'requests.jsonl').read_text().splitlines()]==req
 for r in req:
  assert r['prompt_tokens']==7239 and r['output_tokens']==32
  assert [e['token_count'] for e in r['events']]==list(range(1,33))
 pairs=[]
 for trial in range(11):
  group={r['mode']:r for r in req if r['trial']==trial};assert set(group)==set(modes)
  assert {r['order'] for r in group.values()}=={0,1,2}
  for name in ['schedule','agent']:
   n,c=group['native'],group[name]
   pairs.append(dict(engine=engine,trial=trial,candidate=name,output_equal=n['output_ids']==c['output_ids'],
      latency_saving_ms=(n['latency_s']-c['latency_s'])*1000,ttft_saving_ms=(n['ttft_s']-c['ttft_s'])*1000))
 allpairs+=pairs
 engines.append(dict(engine=engine,raw_sha256=sha(p/'raw.json'),comparisons=[dict(candidate=name,
    exact_output_pairs=sum(x['output_equal'] for x in pairs if x['candidate']==name),
    median_saving_ms=statistics.median(x['latency_saving_ms'] for x in pairs if x['candidate']==name),
    positive_pairs=sum(x['latency_saving_ms']>0 for x in pairs if x['candidate']==name)) for name in ['schedule','agent']]))
report=dict(status='three_engines_verified',requests=99,engines=engines,pairs=allpairs,
 scope='Three engine initializations, randomized triplets within engine, one known prompt, 32 forced outputs. GPU process samples exclusive, CPU background uncontrolled. No general quality, saturation throughput, or performance extrapolation.')
(O/'summary.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='pairs'},indent=2))
