"""Activation-chain traffic and explicit last-use allocator ledgers."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,statistics
R=Path(__file__).resolve().parent;ROOT=R.parents[2];E=ROOT/'experiments/ch05/05-02'
def ledger(fused,retain):
 live={};rows=[]
 def event(action,name,size=0):
  if action=='allocate':assert name not in live;live[name]=size
  elif action=='release':assert name in live;del live[name]
  rows.append(dict(action=action,tensor=name,live=dict(live),bytes=sum(live.values())))
 event('allocate','G',24*2**20);event('allocate','U',24*2**20)
 if fused:
  event('allocate','Q',12*2**20);event('read G,U / write Q','fused')
  if not retain:event('release','G');event('release','U')
 else:
  event('allocate','T',24*2**20);event('read G / write T','silu')
  if not retain:event('release','G')
  event('allocate','Z',24*2**20);event('read T,U / write Z','multiply');event('release','T')
  if not retain:event('release','U')
  event('allocate','Q',12*2**20);event('read Z / write Q','quantize');event('release','Z')
 return dict(fused=fused,retain_caller_inputs=retain,peak_bytes=max(x['bytes'] for x in rows),events=rows)
ledgers=[ledger(f,r) for f in (False,True) for r in (False,True)]
assert [x['peak_bytes']//2**20 for x in ledgers]==[72,96,60,60]
per_row=96*2**20//1024;threshold=F(1792*10**9*5,10**6*per_row);first=threshold.numerator//threshold.denominator+1
assert F(per_row*(first-1),1792*10**9)<=F(5,10**6)<F(per_row*first,1792*10**9)
manifest=json.loads((E/'results/provenance.json').read_text())
for p,h in manifest['sha256'].items():assert hashlib.sha256((E/p).read_bytes()).hexdigest()==h
raw=json.loads((E/'results/results.json').read_text());measured=[]
for n in (1,32,1024):
 g=[r for r in raw['rows'] if r['tokens']==n and r['block']==1024];assert len(g)==2
 measured.append(dict(tokens=n,graph_median_us={r['mode']:statistics.median(r['graph_samples_us']) for r in g},scope='Measured2-op SiLU/multiply chain, not3-op quantization extension'))
files=[ROOT/'manuscripts/05-算子与运行时.md',E/'results/results.json',E/'results/provenance.json']
out=dict(exercise='5-2',separate_traffic_mib=[48,72,36],separate_total_mib=156,fused_total_mib=60,saved_bytes_per_row=per_row,continuous_threshold_rows=str(threshold),first_strictly_beneficial_rows=first,ledgers=ledgers,measured=measured,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
(R/'5-2-results.json').write_text(json.dumps(out,indent=2)+'\n');print('peaksMiB',[x['peak_bytes']//2**20 for x in ledgers],'threshold',float(threshold),'first',first,'measured',measured)
