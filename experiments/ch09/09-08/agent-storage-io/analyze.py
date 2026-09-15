import hashlib,json,math,random,statistics
from pathlib import Path
R=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
spec=read(R/'input-manifest.json');ex=read(R/'results/execution.json');rows=[json.loads(l) for l in (R/'results/operations.jsonl').read_text().splitlines()];assert ex['status']=='all_pages_verified' and ex['operations']==len(rows)==788
for n,h in ex['source_sha256'].items():assert sha(R/n)==h
source=Path(spec['source']);assert sha(source/'results/agent-producer/requests.jsonl')==spec['request_source_sha256']
for n,e in spec['files'].items():assert sha(source/'mac-store'/n)==e['sha256'] and (source/'mac-store'/n).stat().st_size==e['bytes']
for r in rows:assert r['sha256']==spec['files'][r['name']]['sha256'] and r['bytes']==2359296 and r['end_s']>r['start_s']
names=list(spec['files']);assert [x['name'] for x in rows if x['op']=='direct_write_fsync']==names
rng=random.Random(908)
for rep in range(3):
 order=names.copy();rng.shuffle(order);assert [x['name'] for x in rows if x['op']=='direct_read' and x['rep']==rep]==order
summary={}
for op in ['direct_write_fsync','direct_read']:
 a=[x for x in rows if x['op']==op];times=sorted(x['end_s']-x['start_s'] for x in a);summary[op]=dict(operations=len(a),bytes=sum(x['bytes'] for x in a),sum_s=sum(times),median_s=statistics.median(times),sample_p95_s=times[math.ceil(.95*len(times))-1])
perpage={n:dict(write_s=next(r['end_s']-r['start_s'] for r in rows if r['op']=='direct_write_fsync' and r['name']==n),read_samples_s=[r['end_s']-r['start_s'] for r in rows if r['op']=='direct_read' and r['name']==n]) for n in names}
result=dict(status='agent_page_direct_io_verified',page_bytes=2359296,pages=197,filesystem=ex['filesystem'],summary=summary,per_page=perpage,remote_written_files='/home/ubuntu/ai-infra-book-experiments/ch09/09-08/agent-storage-io/results/written',scope='O_DIRECT kernel-page-cache bypass, not hardware-cache bypass. Write includes file+directory fsync; read hash verification outside timing. Storage primitives, not model recovery or representative request p95.')
(R/'summary.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(summary,indent=2))
