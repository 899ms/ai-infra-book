"""Deadline sensitivity, normal stragglers and a sourced peak-compute substitution."""
from pathlib import Path
from fractions import Fraction as F
import sys,json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics.straggler_max import expected_standard_max
from infra_calc import hardware
p=ROOT/'manuscripts/ch10/design-case.json';design=json.loads(p.read_text());a=design['assumptions'];r=next(x for x in design['candidates'] if x['devices']==48)
c=float(F(r['local_seconds_exact']));e=float(F(r['exposed_communication_exact']));link=r['link_seconds_pcie'];loss=r['total_loss'];steps=design['updates'];z=expected_standard_max(48);zfine=expected_standard_max(48,48000);assert abs(z-zfine)<1e-10
rows=[]
def row(name,compute,comm,wait):
 step=compute+comm+wait;days=5+steps*step*(1+loss)/86400
 out=dict(case=name,compute_s=compute,communication_wait_s=comm,input_wait_s=wait,step_s=step,finish_days=days,meets30days=days<=30);rows.append(out);return out
row('base',c,e,.5);row('half_PCIe_prefetch',c,2*e,.5);row('half_PCIe_no_prefetch',c,2*link,.5);row('efficiency30',c*4/3,e,.5);row('input5',c,e,5);row('independent_normal_5pct',c*(1+.05*z),e,.5)
restores=[]
for prefetch in [True,False]:
 for fluctuates in [False,True]:
  factor=1+.05*z if fluctuates else 1
  comp=c*4/3*factor;comm=2*(e if prefetch else link);base_step=comp+comm+5
  options={'restore_PCIe':comp+comm/2+5,'restore_efficiency40':c*factor+comm+5,'restore_input0_5':comp+comm+.5}
  if not prefetch:options['restore_prefetch_only']=comp+2*e+5
  if fluctuates:options['remove_compute_variability']=c*4/3+comm+5
  restores.append(dict(prefetch=prefetch,include_5pct_normal=fluctuates,degraded_step_s=base_step,alternatives=[dict(option=k,step_s=v,saved_s=base_step-v,finish_days=5+steps*v*(1+loss)/86400) for k,v in options.items()]))
dev=hardware.select_device('a100-80gb-sxm');peak=hardware.select_peak(dev,'BF16','FP32','tensor','dense');assert peak['tera_ops_per_second']==312
sub=row('A100_peak_only_counterfactual',c*165.2/312,e,.5)
files=[p,ROOT/'calculations/src/infra_calc/topics/straggler_max.py',next((ROOT/'manuscripts').glob('10-*.md'))]
source_records=[x for x in hardware.records() if x.get('id') in dev['source_ids']]
for src in source_records:
 f=ROOT/'calculations'/src['file']
 if f.exists():files.append(f)
out=dict(exercise='10-9',cases=rows,standard_normal_max48=z,quadrature_change=abs(z-zfine),combined_degradation=restores,substitution=dict(source_device=dev['name'],peak_TFLOPs=peak['tera_ops_per_second'],sources=source_records,scope='Only peak compute changed from165.2 to312, eta40% and all other inputs held fixed. Hybrid sensitivity, not an actual A100 deployment performance prediction.'),scope='Normal independent rank variability is explicit; standard deviation alone does not specify expected maximum. Recovery fraction and five planned days unchanged.',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'10-9-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(rows,indent=2));print('z',z);print('restores',[(r['prefetch'],r['include_5pct_normal'],[(v['option'],v['saved_s']) for v in r['alternatives']]) for r in restores])
