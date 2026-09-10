import argparse,hashlib,json,statistics,torch
from pathlib import Path
r=Path(__file__).absolute().parent;p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();out=a.out.absolute();torch.set_num_threads(2)
def load(p):return json.loads(p.read_text())
def lines(p):return list(map(json.loads,p.read_text().splitlines())) if p.exists() else []
def eq(a,b):
 if isinstance(a,torch.Tensor):return isinstance(b,torch.Tensor) and a.dtype==b.dtype and a.shape==b.shape and torch.equal(a,b)
 if isinstance(a,dict):return a.keys()==b.keys() and all(eq(a[k],b[k]) for k in a)
 if isinstance(a,(list,tuple)):return type(a)==type(b) and len(a)==len(b) and all(eq(x,y) for x,y in zip(a,b))
 return a==b
keys=['model','optimizer','rng','loader_rng','cursor','buffer','positions','step'];source=(r/'data/input.txt').read_bytes();runs=load(out/'execution.json');assert len(runs)==9
for n,h in load(out/'environment.json')['source_sha256'].items():assert hashlib.sha256((r/n).read_bytes()).hexdigest()==h
base=out/'r0-none';bf=torch.load(base/'final.pt',weights_only=True);bs=lines(base/'steps.jsonl');rows=[]
for run in runs:
 d=out/run['name'];assert run['exit_code']==0 and not run['leftover'];steps=lines(d/'steps.jsonl');assert len(steps)==64
 assert load(d/'identity.json')['torch']==torch.__version__
 for x,y in zip(steps,bs):
  assert all(x[k]==y[k] for k in ['step','loss','gradient','positions','input_bytes','input_sha256','cursor','buffer_bytes'])
  assert bytes(x['input_bytes'])==bytes(source[i] for i in x['positions'])
 f=torch.load(d/'final.pt',weights_only=True);assert all(eq(f[k],bf[k]) for k in keys)
 writes=lines(d/'writes.jsonl');assert len(writes)==(0 if run['mode']=='none' else 3)
 for w in writes:
  cp=torch.load(d/w['file'],weights_only=True);ref=torch.load(out/'r0-sync'/w['file'],weights_only=True)
  assert all(eq(cp[k],ref[k]) for k in keys) and cp['step']==w['step']
 reads=[x for p in d.glob('worker-*.jsonl') for x in lines(p)];assert len(list(d.glob('worker-*.jsonl')))==2 and all(x['nocache_applied'] for x in reads)
 overlap=[x for x in reads if any(max(x['read_start'],w['start'])<min(x['read_end'],w['end']) for w in writes)]
 window=load(d/'window.json');stage=lines(d/'staging.jsonl')
 rows.append(dict(name=run['name'],mode=run['mode'],repeat=run['repeat'],window_s=window['end']-window['start'],input_acquisition_s=sum(x['input_end']-x['input_start'] for x in steps),first_input_s=steps[0]['input_end']-steps[0]['input_start'],later_input_s=sum(x['input_end']-x['input_start'] for x in steps[1:]),update_s=sum(x['end']-x['start'] for x in steps),write_s=sum(x['end']-x['start'] for x in writes),checkpoint_bytes=sum(x['bytes'] for x in writes),read_calls=len(reads),read_call_s=sum(x['read_end']-x['read_start'] for x in reads),reads_overlapping_write=len(overlap),staging_s=sum(x['staged']-x['start'] for x in stage),all_training_exact=True))
summary=dict(runs=9,updates=576,saves=18,rows=rows,medians={mode:{k:statistics.median(x[k] for x in rows if x['mode']==mode) for k in ['window_s','input_acquisition_s','first_input_s','later_input_s','read_call_s','update_s','write_s']} for mode in ['none','sync','async']})
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
