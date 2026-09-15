"""Execute block io-ko-jo / ii-ki-ji with tail masks, then audit transpose records."""
from pathlib import Path
import hashlib,json,statistics
R=Path(__file__).resolve().parent;ROOT=R.parents[2];E=ROOT/'experiments/ch05/05-05'
def multiply(A,W,BM=2,BK=3,BN=4):
 M=len(A);K=len(W);N=len(W[0]);Y=[[0]*N for _ in range(M)];events=[]
 for io in range((M+BM-1)//BM):
  height=min(BM,M-io*BM);acc=[[0]*N for _ in range(height)];events.append(['create_acc_panel',io,height*N])
  for ko in range((K+BK-1)//BK):
   depth=min(BK,K-ko*BK);a=[row[ko*BK:ko*BK+depth] for row in A[io*BM:io*BM+height]];events.append(['create_A_cache',io,ko,height*depth])
   for jo in range((N+BN-1)//BN):
    width=min(BN,N-jo*BN);w=[row[jo*BN:jo*BN+width] for row in W[ko*BK:ko*BK+depth]];events.append(['create_W_cache',io,ko,jo,depth*width])
    for ii in range(height):
     for ki in range(depth):
      v=a[ii][ki]
      for ji in range(width):acc[ii][jo*BN+ji]+=v*w[ki][ji]
    events.append(['release_W_cache',io,ko,jo]);del w
   events.append(['release_A_cache',io,ko]);del a
  for ii in range(height):Y[io*BM+ii]=list(acc[ii])
  events.append(['store_then_release_acc_panel',io]);del acc
 return Y,events
A=[[((i*7+k)%9)-4 for k in range(7)] for i in range(5)];W=[[((k*9+j)%11)-5 for j in range(9)] for k in range(7)]
y,events=multiply(A,W);ref=[[sum(A[i][k]*W[k][j] for k in range(7)) for j in range(9)] for i in range(5)];assert y==ref
manifest=json.loads((E/'results/provenance.json').read_text())
for p,h in manifest['sha256'].items():assert hashlib.sha256((E/p).read_bytes()).hexdigest()==h,p
raw=json.loads((E/'results/results.json').read_text());rows=[]
for r in raw['rows']:
 if r['layout']!='contiguous' or r['tile'] not in (16,32):continue
 ptx=(E/'results'/r['code_files']['ptx']).read_text();ir=(E/'results'/r['code_files']['ttgir']).read_text();assert 'ttg.convert_layout' in ir and 'bar.sync' in ptx
 assert r['correctness']=='bitwise_equal_to_torch_transpose' and len(r['samples_us'])==11
 rows.append(dict(shape=[r['m'],r['n']],tile=r['tile'],grid=r['grid'],registers=r['registers'],shared_bytes=r['shared_bytes'],spills=r['spills'],static_ptx_barrier_count=r['ptx_barrier_count'],median_us=statistics.median(r['samples_us']),code_files=r['code_files']))
assert len(rows)==4 and len(raw['edge_checks'])==27 and all(r['passed'] for r in raw['edge_checks'])
files=[E/'results/results.json',E/'results/provenance.json',E/'run.py',ROOT/'manuscripts/05-算子与运行时.md']
out=dict(exercise='5-5',loop_validation=dict(shape=[5,7,9],blocks=[2,3,4],input=A,weight=W,output=y,events=events,reference_equal=True,scope='Integer exact tail-block validation of the displayed loop, not GPU timing'),transpose=rows,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
(R/'5-5-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(rows,indent=2))
