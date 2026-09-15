"""Retention, overlap, endurance and retained shared-pool evidence."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,subprocess
P=Path(__file__).resolve().parent;ROOT=P.parents[2];sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics.kv_tiers import calculate
runs={str(n):calculate(suffix_tokens=n,reuse_windows_s=(300,)) for n in [128,512]}
s=runs['128']['summary'];V=s['prefix_bytes'];recompute=F(s['prefill_prefix_s_exact']);rate=F(s['kv_production_bytes_per_second_exact']);need=rate*300
review=ROOT/'experiments/ch09/09-07/shared-kv/review_pair.py';subprocess.run([sys.executable,'-B',str(review)],cwd=ROOT,check=True,capture_output=True)
cp=review.parent/'capacity-comparison.json';cmp=json.loads(cp.read_text())['comparison'];a,b=cmp
assert a['pool_gib']==4 and b['pool_gib']==8
bm={r['case_id']:r for r in b['candidates']};improved=[]
for r in a['candidates']:
 q=bm[r['case_id']];assert q['matched_tokens']==q['aligned_prefix_tokens']
 if r['matched_tokens']<q['matched_tokens']:improved.append(dict(case_id=r['case_id'],before=r['matched_tokens'],after=q['matched_tokens'],additional_tokens=q['matched_tokens']-r['matched_tokens']))
assert len(improved)==7
host=F(256*2**30);hbm=F(s['hbm_kv_bytes']);allow=F(s['ssd_endurance_bytes_per_second_exact']);fraction=allow/rate
for r in runs.values():
 t=next(t for t in r['tiers'] if t['tier']=='host DRAM');k=t['preload_layers_for_full_overlap'];read=F(t['load_per_layer_s_exact']);comp=F(t['compute_per_layer_s_exact'])
 def ok(n):return all((i-n+1)*read<=i*comp for i in range(n,36))
 assert ok(k) and (k==0 or not ok(k-1))
files=[next((ROOT/'manuscripts').glob('09-*.md')),ROOT/'calculations/src/infra_calc/topics/kv_tiers.py',cp,review]
for r in runs.values():
 for src in r['sources']:
  f=ROOT/src['file']
  if f.exists():files.append(f)
out=dict(exercise='9-7',tiers_by_suffix=runs,comparison100=dict(recompute_once_s=float(recompute),network_fetch_once_s=float(F(V,25*10**9)),network_fetch100_s=float(F(100*V,25*10**9)),serial_network_then_host_once_s=float(F(2*V,25*10**9)),serial_network_then_host100_s=float(F(200*V,25*10**9)),network_bytes100=100*V),retention300=dict(required_bytes=float(need),required_GiB=float(need/2**30),host_bytes=int(host),HBM_upper_bytes=int(hbm),shortfall_beyond_exclusive_HBM_and_host_bytes=float(need-host-hbm)),endurance=dict(bytes_per_s=float(allow),new_KV_fraction=float(fraction),half_generation_fraction=float(2*fraction)),shared_pool_improved=improved,scope='Fixed book storage rates and ideal per-layer computation; write amplification/lookup/queue excluded unless separately noted. Shared-pool evidence is same-GPU independent engines, not remote NIC.',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'9-7-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['tiers_by_suffix','source_sha256']},indent=2))
for n,r in runs.items():
 t=next(t for t in r['tiers'] if t['tier']=='host DRAM');print(n,'warm',float(F(r['summary']['warm_suffix_s_exact'])),'pipeline',float(F(t['layer_pipelined_s_exact'])),'preload',t['preload_layers_for_full_overlap'])
