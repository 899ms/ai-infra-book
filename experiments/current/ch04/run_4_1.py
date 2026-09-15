"""Current4-1 exact B200 single-SM resource accounting and independent changes."""
import hashlib,json,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics.fa4_resource_balance import tile
out=[]
for m,n in [(128,256),(256,128)]:
 for name,mults in [('baseline',(1,1,1)),('matrix_only_x2',(2,1,1)),('exp_only_x2',(1,2,1)),('smem_only_x2',(1,1,2)),('matrix_exp_x2',(2,2,1)),('all_x2',(2,2,2))]:
  row=tile(m,n,128,*mults)
  # Independent scalar reductions of the pinned paper equations for128 multiples.
  assert row['work']['matrix_flops']==4*m*n*128
  assert row['work']['smem_read_bytes']==3*m*n*128//64
  assert row['work']['exp_results']==m*n
  out.append(dict(scenario=name,**row))
files=['manuscripts/04-加速器架构.md','calculations/configs/fa4-resource-inputs.json','calculations/src/infra_calc/topics/fa4_resource_balance.py','calculations/sources/fa4-resource-balance/paper.txt']
x=dict(exercise='4-1',scope='Exact paper resource bound, not new B200 measurement',rows=out,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files})
(R/'4-1-results.json').write_text(json.dumps(x,indent=2)+'\n')
print('verified',len(out),'resource configurations')
