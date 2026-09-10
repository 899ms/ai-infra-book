import argparse,hashlib,json,torch
from pathlib import Path
r=Path(__file__).absolute().parent;p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();out=a.out.absolute();torch.set_num_threads(2)
def load(p):return json.loads(p.read_text())
def lines(p):return list(map(json.loads,p.read_text().splitlines()))
def equal(a,b):
 if isinstance(a,torch.Tensor):return isinstance(b,torch.Tensor) and a.dtype==b.dtype and a.shape==b.shape and torch.equal(a,b)
 if isinstance(a,dict):return isinstance(b,dict) and a.keys()==b.keys() and all(equal(a[k],b[k]) for k in a)
 if isinstance(a,(list,tuple)):return type(a)==type(b) and len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
 return a==b
def count(x):
 if isinstance(x,torch.Tensor):return 1
 if isinstance(x,dict):return sum(count(v) for v in x.values())
 if isinstance(x,(list,tuple)):return sum(count(v) for v in x)
 return 0
for n,h in load(r/'provenance.json').items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
for n,h in load(out/'environment.json')['source_sha256'].items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
source=(r/'data/input.txt').read_bytes();runs=load(out/'execution.json');assert len(runs)==12;rows=[];steps=0
for run in runs:
 d=out/run['name'];seed=run['seed'];cut=run['cut'];base=r/'reference'/f'seed{seed}-baseline';prefix=r/'reference'/f'seed{seed}-cut{cut}-prefix'
 assert run['exit_code']==0 and not run['leftover'];ident=load(d/'identity.json');assert ident['pid']==run['pid'] and ident['workers']==run['workers'] and ident['start_step']==cut
 assert ident['torch']==load(base/'identity.json')['torch']==torch.__version__
 observed=lines(d/'steps.jsonl');expected=lines(base/'steps.jsonl')[cut:];assert len(observed)==len(expected)==64-cut;steps+=len(observed)
 for x,y in zip(observed,expected):
  assert all(x[k]==y[k] for k in ['step','loss','gradient','positions','input_bytes','input_sha256','buffer_bytes','cursor'])
  raw=bytes(source[i] for i in x['positions']);assert raw==bytes(x['input_bytes']) and hashlib.sha256(raw).hexdigest()==x['input_sha256']
 b=torch.load(base/'final.pt',weights_only=True);f=torch.load(d/'final.pt',weights_only=True)
 for key in ['model','optimizer','rng','loader_rng','cursor','buffer','positions','step']:assert equal(b[key],f[key]),(run['name'],key)
 logs=list(d.glob('worker-*.jsonl'));assert len(logs)==run['workers'];reads=[x for p in logs for x in lines(p)];cp=torch.load(prefix/'checkpoint.pt',weights_only=True)
 assert min(x['record'] for x in reads)==cp['cursor']
 pending=load(prefix/'ready.json')['pending'];assert set(pending)<=set(x['record'] for x in reads)
 for x in reads:
  assert x['start']==sum(257+2*(i%7) for i in range(x['record'])) and x['end']-x['start']==x['bytes']
 consume=lines(d/'consume.jsonl');assert [x['record'] for x in consume]==list(range(cp['cursor'],f['cursor']))
 dispatch=[x['record'] for x in lines(d/'dispatch.jsonl')];assert dispatch==list(range(cp['cursor'],f['dispatch_cursor']))
 rows.append(dict(name=run['name'],seed=seed,cut=cut,workers=run['workers'],steps=len(observed),state_tensors=count(b),exact=True,baseline_dispatch_cursor=b['dispatch_cursor'],final_dispatch_cursor=f['dispatch_cursor'],final_consumed_cursor=f['cursor'],worker_read_records=len(reads),worker_pids=sorted(set(x['pid'] for x in reads)),pending_reread=pending))
assert steps==420
summary=dict(runs=12,updates=steps,actual_workers=sum(x['workers'] for x in rows),all_exact=True,rows=rows,scope='Deterministic ordered reads; worker count changes 2 to 1/4; no random augmentation or performance ranking')
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
