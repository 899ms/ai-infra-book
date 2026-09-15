"""Capacity/cost design; measured parameter replacement still tracked separately."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,math
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=ROOT/'manuscripts/ch10/design-case.json';d=json.loads(source.read_text());N=d['assumptions']['parameters'];rows=[]
for r in d['candidates']:
 n=r['devices'];bf=F(16*N,n);fp=F(N,n)*(15+F(1,4096))
 rows.append(dict(cards=n,finish_days=r['finish_days'],GPU_hours_including5planned_days=n*r['finish_days']*24,GPU_hours_training_and_recovery=n*(r['finish_days']-5)*24,BF16_state_GiB=float(bf/2**30),FP8_operand_state_GiB=float(fp/2**30),cases=[dict(extra_GiB=extra,BF16_peak_GiB=float(bf/2**30+extra),BF16_headroom_GiB=float(22-extra-bf/2**30),FP8_peak_GiB=float(fp/2**30+extra),FP8_headroom_GiB=float(22-extra-fp/2**30)) for extra in [10,20]]))
r=d['candidates'][0];step=F(r['base_step_exact']);a=d['assumptions'];loss=F(14*N,7*10**9*1800)+F(32,a['device_mtbf_seconds'])*(900+120)
maxsteps=int(F(25*86400)/(step*(1+loss)));max_tokens=maxsteps*d['tokens_per_update']
assert maxsteps*step*(1+loss)<=25*86400<(maxsteps+1)*step*(1+loss)
out=dict(exercise='10-3',status='calculation_complete_measured_replacement_in_checkpoint_write',rows=rows,four_hosts=dict(max_full_updates=maxsteps,max_tokens_at_same_step_cost=max_tokens,fraction_original_tokens=max_tokens/10**11,required_calendar_days=r['finish_days'],minimum_compute_efficiency=r['minimum_local_efficiency']),FP8_scope='Book average full-block format 1+4/16384 bytes for operand copy, other14bytes unchanged; ideal uniform state partition. Actual nonmatrix tensors and block padding require implementation-specific accounting.',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [source,next((ROOT/'manuscripts').glob('10-*.md'))]})
(P/'10-3-calculation.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
