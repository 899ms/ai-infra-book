"""Exact chapter energy ledger and conditional H100 power-cap calculation."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,sys
R=Path(__file__).resolve().parent;ROOT=R.parents[2];sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc import hardware
p=ROOT/'calculations/results/energy-ledger-book.json';d=json.loads(p.read_text());s=d['summary']
h=hardware.select_device('h100-sxm');peak=hardware.select_peak(h,'BF16','FP32','tensor','dense')
W=s['weight_read_bytes'];K=s['kv_read_bytes'];flops=s['matrix_flops'];epb=F(d['energy_per_byte']['hbm']['pj_per_byte_exact'])/10**12;epf=F(d['joules_per_token']['compute']['pj_per_flop_exact'])/10**12
EW=W*epb;EK=K*epb;EC=flops*epf
assert abs(float(EW+EK+EC)-s['joules_per_token_total'])<1e-15
rows=[dict(batch=b,weight_j=float(EW/b),kv_j=float(EK),compute_j=float(EC),total_j=float(EW/b+EK+EC)) for b in (1,8,32,128)]
threshold=EW//EC+1;assert EW/threshold<EC<=EW/(threshold-1)
cross=F(W,4*K);assert EW/cross==4*EK
bw=F(str(h['memory']['bandwidth_bytes_per_second']));rate=F(str(peak['tera_ops_per_second']))*10**12;tdp=F(h['power_watts']);mem=epb*bw;budget=(tdp-mem)/rate
energy32=EW+32*(EK+EC);traffic=W+32*K;fp=32*flops;power=[]
for mode,r in [('constant_voltage',2/3),('voltage_proportional_to_frequency',(2/3)**(1/3))]:
 ct=float(fp/rate)/r;mt=float(traffic/bw);t=max(ct,mt)
 power.append(dict(mode=mode,frequency_ratio=r,compute_seconds=ct,memory_seconds=mt,step_seconds=t,step_energy_j=float(energy32),ledger_average_watts=float(energy32)/t,tdp_minus_ledger_average_watts=float(tdp)-float(energy32)/t,limiter='memory' if mt>ct else 'compute'))
files=[p,ROOT/'calculations/configs/hardware.json',ROOT/'manuscripts/04-加速器架构.md']
out=dict(exercise='4-8',rows=rows,minimum_batch_weight_below_compute=int(threshold),continuous_crossover_32k_batch_exact=str(cross),continuous_crossover_32k_batch=float(cross),first_integer_batch_kv_ge_weight=(cross.numerator+cross.denominator-1)//cross.denominator,h100=dict(power_watts=int(tdp),bandwidth_bytes_s=float(bw),bf16_dense_flops_s=float(rate),memory_power_watts=float(mem),compute_power_budget_watts=float(tdp-mem),budget_pj_per_flop=float(budget*10**12),assumed_actual_pj_per_flop=float(F(3,2)*budget*10**12)),power=power,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
(R/'4-8-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
