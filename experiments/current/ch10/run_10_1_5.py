"""FP32-gradient state budgets and data/checkpoint supply arithmetic."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib,math
P=Path(__file__).resolve().parent;ROOT=P.parents[2];sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics.training_state import calculate
r=calculate(gradient_bytes=4,participants=8)
N=r['summary']['parameters'];assert N==8190735360 and N%8==0
rows=[]
for z in r['training_state_stages']:
 stage=z['stage'];expected=[18*N,F(15,2)*N,4*N,F(9,4)*N][stage]
 assert z['persistent_bytes_per_rank']==expected
 v=z['persistent_bytes_per_rank'];rows.append(dict(stage=stage,persistent_bytes=v,persistent_GiB=v/2**30,simultaneous_peak_bytes=v+12*2**30,sequential_peak_bytes=v+9*2**30,simultaneous_peak_GiB=v/2**30+12,sequential_peak_GiB=v/2**30+9))
cons=F(384)/F('52.8');deficit=cons-6;loss=deficit*60;recover=8-cons
assert deficit>0 and recover>0
minimum=math.ceil(loss);assert minimum>=loss>minimum-1
actual_ckpt=14*N
files=[next((ROOT/'manuscripts').glob('10-*.md')),ROOT/'calculations/src/infra_calc/topics/training_state.py']
for src in r['sources']:
 f=ROOT/'calculations'/src['file']
 if f.exists():files.append(f)
out=dict(exercises=['10-1','10-5'],training_state=r,peak_cases=rows,input_supply=dict(consumption_sequences_s=float(cons),paused_supply_sequences_s=6,deficit_sequences_s=float(deficit),pause_s=60,depleted_sequences_exact=str(loss),minimum_integer_prebuffer=minimum,replenishment_surplus_sequences_s=float(recover),time_to_restore_actual_depletion_s=float(loss/recover),time_to_fill77_from_empty_s=float(F(77)/recover)),checkpoint=dict(rounded_115GB_min_interval_s=float(F(115*10**9,7*10**9)),exact_14N_bytes=actual_ckpt,exact_min_interval_s=float(F(actual_ckpt,7*10**9))),source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'10-1-5-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['training_state','source_sha256']},indent=2))
