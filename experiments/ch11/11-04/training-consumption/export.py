import hashlib,json,sqlite3
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent
s=json.loads((P/'formal/summary.json').read_text());samples=[];sources={}
for row in sorted(s['results'],key=lambda x:x['request_id']):
 d=P/'formal'/row['request_id'];db=d/'manager-snapshot.sqlite';env=d/'attempt-0/environment.json'
 conn=sqlite3.connect('file:'+str(db)+'?mode=ro&immutable=1',uri=True);tokens=conn.execute('select seq,token,eos from tokens order by seq').fetchall();conn.close()
 assert [x[0] for x in tokens]==list(range(len(tokens))) and [x[1] for x in tokens]==row['token_ids'] and tokens[-1][2]==1
 e=json.loads(env.read_text());prompt=e['prompt_ids'];assert hashlib.sha256(json.dumps(prompt,separators=(',',':')).encode()).hexdigest()==e['prompt_sha']
 assert row['quality_passed'] and row['tokens_equal_baseline'] and not row['conflicts']
 samples.append(dict(request_id=row['request_id'],task=row['task'],strategy=row['strategy'],cut=row['cut'],prompt_ids=prompt,output_ids=row['token_ids'],expected_text=row['text'],sampled_tokens=row['sampled_tokens'],manager_unique_tokens=row['unique_tokens'],duplicate_deliveries=row['duplicate_deliveries'],generation_model_revision=e['model'],sample_sha256=hashlib.sha256(json.dumps([prompt,row['token_ids']],separators=(',',':')).encode()).hexdigest()))
 for p in [db,env,P/'formal/summary.json']:sources[str(p.relative_to(P))]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'samples.json').write_text(json.dumps(dict(samples=samples,source_sha256=sources),indent=2)+'\n')
print(len(samples),sum(len(x['output_ids']) for x in samples),'logical output positions')
