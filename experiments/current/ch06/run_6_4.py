"""Exercise 6-4: synchronous ring simulation and exact collective cost model."""
from fractions import Fraction as F
from pathlib import Path
import hashlib, importlib.util, json, math
R=Path(__file__).resolve().parent; ROOT=R.parents[2]
a=F(822,10**9); bw=450*10**9; message=10240

def ring(n,m,alpha=a,bandwidth=bw):
    return 2*(n-1)*alpha+F(2*(n-1),n)*m/bandwidth

def tree(n,m,alpha=a,bandwidth=bw):
    return 2*int(math.log2(n))*(alpha+F(m,bandwidth))

# Simultaneous sends: round r sends block (rank-r) mod n clockwise.
# Every receiver adds its own contribution to the received partial.
state={(rank,block):frozenset([rank]) for rank in range(4) for block in range(4)}
trace=[dict(round=0,holder=1,contributors=[1])]
for r in range(3):
    sends=[]
    for rank in range(4):
        block=(rank-r)%4; receiver=(rank+1)%4
        partial=state[rank,block]
        assert receiver not in partial
        sends.append((receiver,block,partial|{receiver}))
    for receiver,block,partial in sends:
        state[receiver,block]=partial
        if block==1:trace.append(dict(round=r+1,holder=receiver,contributors=sorted(partial)))
for rank in range(4): assert state[rank,(rank+1)%4]==frozenset(range(4))
assert [x['holder'] for x in trace]==[1,2,3,0]
rows=[dict(cards=n,ring_send_M_coefficient=str(F(2*(n-1),n)),ring_send_bytes_10KiB=int(F(2*(n-1),n)*message),ring_s=float(ring(n,message)),tree_s=float(tree(n,message))) for n in (4,8)]
cross=[]
for alpha in (a,a/2):
    x=8*alpha*bw/F(17,4)
    assert ring(8,x,alpha)==tree(8,x,alpha)
    floor=x.numerator//x.denominator
    assert tree(8,floor,alpha)<ring(8,floor,alpha)
    assert ring(8,floor+1,alpha)<tree(8,floor+1,alpha)
    cross.append(dict(alpha_s=float(alpha),exact_bytes=str(x),bytes=float(x),KiB=float(x/1024),first_integer_bytes_ring_faster=floor+1))
spec=importlib.util.spec_from_file_location('continuity',ROOT/'manuscripts/ch06/continuity_model.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
baseline=m.step(8,m.PARAMS['history']); local=max(baseline['local_s'],baseline['compute_s'])
arch=json.loads((ROOT/'manuscripts/ch06/continuity-model.json').read_text())
assert math.isclose(baseline['total_s'],next(x for x in arch['first_steps'] if x['tp']==8)['total_s'],abs_tol=1e-14)
assert m.MESSAGE==message and m.ALLREDUCES==128
variants=[]
for label,t in [('ring',ring(8,message)),('tree',tree(8,message)),('ring_double_link_bandwidth',ring(8,message,bandwidth=2*bw)),('tree_double_link_bandwidth',tree(8,message,bandwidth=2*bw))]:
    total=local+128*float(t)
    variants.append(dict(variant=label,collective_s=float(t),communication_s=128*float(t),local_s=local,total_s=total,saving_vs_ring_s=baseline['total_s']-total,speedup_vs_ring=baseline['total_s']/total))
assert math.isclose(variants[0]['total_s'],baseline['total_s'],abs_tol=1e-14)
assert math.isclose(float(128*(ring(8,message)-ring(8,message,bandwidth=2*bw))),arch['collectives']['bandwidth_doubled_saving_s'],abs_tol=1e-14)
files=['manuscripts/06-超节点.md','manuscripts/ch06/continuity_model.py','manuscripts/ch06/continuity-model.json','calculations/configs/hardware.json','calculations/configs/models/qwen3-32b/config.json']
out=dict(exercise='6-4',block1_trace=trace,collectives=rows,crossovers=cross,TP8_first_step=variants,scope='Exact declared synchronous ring/unsegmented binomial-tree model; no new multi-GPU measurement; bandwidth doubling applies to NVLink, not HBM',source_sha256={f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in files})
(R/'6-4-results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
