"""Deadline efficiency and weak/strong scaling at fixed declared noise scale."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics.critical_batch import calculate
base=ROOT/'manuscripts/ch10';design=json.loads((base/'design-case.json').read_text());a=design['assumptions'];d=next(x for x in design['candidates'] if x['devices']==32)
updates=(10**11+384*8192-1)//(384*8192);assert updates==31790
budget25=F(25*86400,updates);budget30=F(30*86400,updates)
V=3*12*F(31,32)*2*a['parameters'];link=V/(32*10**9)
exposed=2*F(31,32)*2*a['embedding_parameters']/(32*10**9)
assert float(link)==d['link_seconds_pcie'] and exposed==F(d['exposed_communication_exact'])
unit=F(d['local_seconds_exact'])*F(2,5);overhead=exposed+F(1,2)
loss=F(14*a['parameters'],7*10**9*1800)+F(32,a['device_mtbf_seconds'])*(900+120)
eta0=unit/(budget25-overhead);eta1=unit/(budget25/(1+loss)-overhead)
assert unit/eta0+overhead==budget25 and (unit/eta1+overhead)*(1+loss)==budget25
scaling={}
files=[next((ROOT/'manuscripts').glob('10-*.md')),base/'design-case.json',base/'design-case.py',ROOT/'calculations/src/infra_calc/topics/critical_batch.py']
for name in ['critical-batch-book','critical-batch-noise-20m']:
 p=ROOT/f'calculations/results/{name}.json';old=json.loads(p.read_text());r=calculate(**old['scenario']);assert r['rows']==old['rows'] and r['summary']==old['summary'];files.append(p)
 scaling[name]=dict(reference=r['reference'],summary=r['summary'],rows=[x for x in r['rows'] if x['cards'] in [96,1536]])
out=dict(exercise='10-2',updates=updates,batch_tokens=384*8192,step_budget30_s=float(budget30),step_budget25_s=float(budget25),link_bytes_per_step=float(V),link_time_s=float(link),exposed_communication_s=float(exposed),input_wait_s=.5,minimum_efficiency_without_recovery=float(eta0),recovery_fraction=float(loss),base_step_budget_with_recovery_s=float(budget25/(1+loss)),minimum_efficiency_with_recovery=float(eta1),scaling=scaling,scope='Fixed batch deadline uses book design compute, not 6ND shortcut. Scaling uses archived 48-card reference and excludes recovery/nontraining days; noise values are assumptions.',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'10-2-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k not in ['scaling','source_sha256']},indent=2))
for name,r in scaling.items():print(name,r['summary']['weak_scaling_speedup_ceiling'],[(x['cards'],x['weak_wall_days'],x['strong_wall_days']) for x in r['rows']])
