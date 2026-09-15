import hashlib,json,random,statistics
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
x=read(O/'execution.json');assert len(x['rows'])==1 and x['rows'][0]['exit_code']==0 and not x['after_gpu'].strip()
raw=read(O/'cold/raw.json');assert raw['status']=='all_requests_returned'
for n,h in raw['source_hashes'].items():assert sha(R/n)==h
rows=[json.loads(l) for l in (O/'cold/requests.jsonl').read_text().splitlines()];assert rows==raw['requests'] and len(rows)==48
inputs=read(R/'inputs.json');rng=random.Random(909);expected=[]
for source,h in inputs['source_sha256'].items():assert sha(Path(source))==h
for rep in range(3):
 order=inputs['requests'].copy();rng.shuffle(order);expected.extend((rep,i) for i in order)
for row,(rep,item) in zip(rows,expected):
 assert (row['rep'],row['kind'],row['turn'])==(rep,item['kind'],item['turn'])
 m=row['response']['meta_info'];assert m['prompt_tokens']==len(item['input_ids']) and m['completion_tokens']==1 and m['num_retractions']==0 and m['cached_tokens']==0
summary=[]
for item in inputs['requests']:
 selected=[r for r in rows if (r['kind'],r['turn'])==(item['kind'],item['turn'])];tokens=[r['response']['output_ids'] for r in selected];times=[r['end_s']-r['start_s'] for r in selected]
 summary.append(dict(kind=item['kind'],turn=item['turn'],input_tokens=len(item['input_ids']),wall_s=times,median_s=statistics.median(times),output_ids=tokens,outputs_equal=all(t==tokens[0] for t in tokens)))
result=dict(status='cold_recomputation_verified',requests=48,all_cache_hits_zero=True,all_repeated_outputs_equal=all(r['outputs_equal'] for r in summary),per_input=summary,scope='Three shuffled passes in one engine. No queueing and no GPU-kernel-only timing. First pass is retained, including warmup.')
(R/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
