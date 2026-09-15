"""CPU expert compute/read crossovers, with communication separately counted."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('09-*.md'));params=18874368;rows=[]
for width in (2,1):
 for bw in (220,125):
  for name,compute in [('AVX-512',1800*10**9),('AMX',21300*10**9)]:
   cross=F(width*compute,2*bw*10**9);first=(cross.numerator+cross.denominator-1)//cross.denominator
   assert F(2*(first-1)*params,compute)<F(width*params,bw*10**9)<=F(2*first*params,compute)
   for m in (1,128):
    read=F(width*params,bw*10**9);calc=F(2*m*params,compute);comm=F(10,10**6)+F(2*m*4096*2,25*10**9);t=max(read,calc)
    rows.append(dict(weight_bytes_per_parameter=width,DRAM_GBps=bw,kernel=name,equality_rows_exact=str(cross),equality_rows=float(cross),first_integer_compute_ge_read=first,rows_per_expert=m,read_ms=float(read*1000),compute_ms=float(calc*1000),CPU_operator_ms=float(t*1000),activation_roundtrip_ms=float(comm*1000),one_expert_CPU_path_ms=float((t+comm)*1000),eight_serial_experts_path_ms=float(8*(t+comm)*1000),bottleneck='compute' if calc>read else 'read' if read>calc else 'tie'))
out=dict(exercise='9-3',expert_parameters=params,results=rows,scope='Constant effective CPU FLOP/s; one-byte weights are hypothetical with no conversion cost; BF16 activations retained; expert weights read once per batch',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'9-3-results.json').write_text(json.dumps(out,indent=2)+'\n')
for r in rows:print(r['weight_bytes_per_parameter'],r['DRAM_GBps'],r['kernel'],r['equality_rows'],r['first_integer_compute_ge_read'],r['rows_per_expert'],r['CPU_operator_ms'],r['eight_serial_experts_path_ms'],r['bottleneck'])
