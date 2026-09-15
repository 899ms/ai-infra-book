import hashlib,json,sqlite3
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent;A=P/'additional-device';summary=json.loads((A/'summary.json').read_text());formal=json.loads((P/'formal/summary.json').read_text());sources={};samples=[]
def read(p):
 sources[str(p.relative_to(P))]=hashlib.sha256(p.read_bytes()).hexdigest();return json.loads(p.read_text())
read(A/'summary.json');read(P/'formal/summary.json')
for row in summary['samples']:
 d=A/'results'/f'rep{row["rep"]}-{row["policy"]}'/row['task'];rid=f'rep{row["rep"]}-{row["policy"]}-{row["task"]}'
 if row['task']=='extract' and row['policy']=='additional':
  raw=read(d/'worker/raw.json');prompt=read(A/'rtx-input.json')['prompt_ids'];text=raw['text'];revision=raw['model'];db=d/'manager-receipt.sqlite'
 else:
  env=read(d/'attempt-0/environment.json');prompt=env['prompt_ids'];revision=env['model'];text=next(x['text'] for x in formal['results'] if x['task']==row['task'] and x['strategy']=='baseline');db=d/'manager-snapshot.sqlite'
 sources[str(db.relative_to(P))]=hashlib.sha256(db.read_bytes()).hexdigest();c=sqlite3.connect('file:'+str(db)+'?mode=ro&immutable=1',uri=True);tokens=c.execute('select seq,token from tokens order by seq').fetchall();c.close();assert [x[0] for x in tokens]==list(range(len(tokens)));ids=[x[1] for x in tokens];assert len(ids)==row['manager_received_tokens'] and row['quality_passed']
 samples.append(dict(request_id=rid,task=row['task'],strategy=row['policy'],rep=row['rep'],prompt_ids=prompt,output_ids=ids,expected_text=text,generation_model_revision=revision,sample_sha256=hashlib.sha256(json.dumps([prompt,ids],separators=(',',':')).encode()).hexdigest()))
(R/'samples.json').write_text(json.dumps(dict(samples=samples,source_sha256=sources),indent=2)+'\n');print(len(samples),sum(len(x['output_ids']) for x in samples))
