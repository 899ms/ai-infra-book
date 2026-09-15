"""First-order checkpoint cost; physical commit-boundary tests tracked separately."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib,math
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
c=F(14*8190735360,7*10**9);recovery=120
# Keep the chapter's 7.9h job and rounded 337d/device conventions explicit.
base=F(1,28440);small=F(48,337*86400)
cases=[]
for name,rate in [('1024_independent',base),('1024_plus_daily_common',base+F(1,86400)),('48_independent',small),('48_plus_weekly_rollback',small+F(1,7*86400))]:
 opt=math.sqrt(float(2*c/rate));rows=[]
 for tau in ([300,900,1800] if name.startswith('1024') else [600]):
  save=c/tau;redo=rate*tau/2;restart=rate*recovery
  rows.append(dict(interval_s=tau,save_fraction=float(save),redo_fraction=float(redo),restart_fraction=float(restart),total_fraction=float(save+redo+restart)))
 assert abs(-float(c)/opt**2+float(rate)/2)<1e-15
 cases.append(dict(name=name,rate_per_s=float(rate),job_MTBF_s=float(1/rate),optimal_interval_s=opt,rows=rows))
source=next((ROOT/'manuscripts').glob('10-*.md'))
out=dict(exercise='10-6',status='calculation_complete_physical_evidence_in_commit_after',save_s=float(c),recovery_s=recovery,cases=cases,scope='First-order extra time per useful time. Daily/weekly common shock adds once per job, not once per GPU. Weekly rollback treated as loss since latest usable checkpoint with same 120s recovery; deeper loss requires a different model.',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'10-6-calculation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
