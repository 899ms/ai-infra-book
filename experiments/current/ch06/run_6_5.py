"""Reconcile original four-rank observations and compute strict amortization."""
from pathlib import Path
from fractions import Fraction as F
from statistics import median
import json,hashlib,math
P=Path(__file__).resolve().parent;ROOT=P.parents[2];OLD=ROOT/'experiments/ch06/06-05'
manifest=json.loads((OLD/'manifest.json').read_text())
for entry in manifest['files']:
 f=OLD/entry['path'];assert len(f.read_bytes())==entry['bytes'];assert hashlib.sha256(f.read_bytes()).hexdigest()==entry['sha256'],f
raw=[[json.loads(x) for x in (OLD/f'formal/rank{rank}.jsonl').read_text().splitlines()] for rank in range(4)]
summary=json.loads((OLD/'analysis.json').read_text())['summary'];groups=[]
for i,cfg in enumerate(json.loads((OLD/'formal/environment.json').read_text())['plan']):
 if cfg['warmup']:continue
 ranks=[raw[r][i] for r in range(4)]
 for r,row in enumerate(ranks):
  assert row['rank']==r and all(row[k]==v for k,v in cfg.items())
  assert row['comm_correct'] is not False and row['compute_correct'] is not False
 groups.append(dict(**cfg,wall_ns=max(x['end_ns'] for x in ranks)-min(x['start_ns'] for x in ranks),comm_ns=max(x['marks']['comm_callback_ns']-x['marks']['comm_submit_ns'] for x in ranks) if cfg['mode']!='compute' else None,compute_ns=max(x['marks']['compute_end_ns']-x['marks']['compute_start_ns'] for x in ranks) if cfg['mode']!='comm' else None))
assert len(groups)==45
outrows=[]
for size in (4*2**20,64*2**20):
 med={}
 for mode in ('comm','compute','shared'):
  g=[x for x in groups if x['bytes']==size and x['mode']==mode];assert len(g)==5
  med[mode]={k:median(x[k] for x in g) if g[0][k] is not None else None for k in ('wall_ns','comm_ns','compute_ns')}
  ref=next(x for x in summary if x['bytes']==size and x['mode']==mode)
  for k,rk in [('wall_ns','wall_median_ms'),('comm_ns','comm_visible_median_ms'),('compute_ns','compute_median_ms')]:
   if med[mode][k] is not None:assert med[mode][k]/1e6==ref[rk]
 separate=med['comm']['comm_ns']+med['compute']['compute_ns']; shared=max(med['shared']['comm_ns'],med['shared']['compute_ns']);delta=separate-shared
 wall_delta=med['comm']['wall_ns']+med['compute']['wall_ns']-med['shared']['wall_ns']
 n=10**9//delta+1;assert (n-1)*delta<=10**9<n*delta
 pairs=[]
 for trial in range(5):
  g={x['mode']:x for x in groups if x['bytes']==size and x['trial']==trial}
  pairs.append(g['comm']['wall_ns']+g['compute']['wall_ns']-g['shared']['wall_ns'])
 outrows.append(dict(bytes=size,median_intervals_ns=med,figure_separate_sum_ns=separate,figure_shared_max_ns=shared,figure_saving_ns=delta,shared_dominant='compute' if med['shared']['compute_ns']>med['shared']['comm_ns'] else 'comm',strict_calls_for_1s=n,wall_medians_saving_ns=wall_delta,wall_strict_calls_for_1s=10**9//wall_delta+1,paired_wall_saving_ns=pairs))
def norm(x):
 rms=math.sqrt(sum(v*v for v in x)/len(x));return [v/rms for v in x]
a=[1.,0.];b=[0.,1.];after=norm([x+y for x,y in zip(a,b)]);before=[x+y for x,y in zip(norm(a),norm(b))];assert after!=before
sources=['experiments/current/ch06/gpu-overlap/analysis.json','experiments/current/ch06/gpu-overlap/results.json','experiments/current/ch06/gpu-overlap/run.py','manuscripts/06-超节点.md','experiments/ch06/06-05/manifest.json','experiments/ch06/06-05/analysis.json']+[f'experiments/ch06/06-05/formal/rank{i}.jsonl' for i in range(4)]
out=dict(exercise='6-5',cpu_original_manifest_files_verified=len(manifest['files']),cpu_rows=outrows,rmsnorm=dict(a=a,b=b,normalize_sum=after,sum_normalized=before,epsilon=0,scale=1),scope='Figure operation-interval arithmetic and separate whole-group estimates; no directly measured combined sequential CPU baseline',source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in sources})
(P/'6-5-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(outrows,indent=2))
