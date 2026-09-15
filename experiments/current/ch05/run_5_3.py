"""Exact online-softmax example and fixed-capacity extra-slot accounting."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json,math,sys
R=Path(__file__).resolve().parent;ROOT=R.parents[2];sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics.attention_tiles import calculate
# Scores are logs of exact weights1,2,4; use rational rescaling rather than rounded logs.
ell=F(3,2);u=F(7,2);r=F(1,2);newell=r*ell+1;newu=r*u+5;out=newu/newell
assert (newell,newu,out)==(F(7,4),F(27,4),F(27,7))
assert out==F(1+2*3+4*5,1+2+4)
weights=[math.exp(x-math.log(4)) for x in (0,math.log(2),math.log(4))];assert abs(sum(p*v for p,v in zip(weights,(1,3,5)))/sum(weights)-float(out))<1e-14
rows=[]
for slots in (1,2):
 d=calculate(capacity_bytes=101376,kv_blocks=[64],kv_slots=slots,causal=False);x=d['attention_tile_rows'][0]
 a=(101376-2*64*128*slots)//(6*128+4*64+12)
 assert x['query_block']==a and x['query_blocks']==math.ceil(8192/a)
 assert x['reserved_working_bytes']<=101376<x['reserved_working_bytes']+1036
 assert x['interface_bytes']==(math.ceil(8192/a)*4+4)*2**20
 rows.append(dict(slots=slots,**x))
files=['manuscripts/05-算子与运行时.md','calculations/src/infra_calc/topics/attention_tiles.py']
d=dict(exercise='5-3',new_state=dict(m='ln4',ell=str(newell),u=str(newu),output=str(out),float_output=float(out)),capacity_rows=rows,source_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files})
(R/'5-3-results.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d,indent=2))
