"""Both current5-1 blocks: occupancy and tile traffic plus archived CPU timing."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,statistics
R=Path(__file__).resolve().parent;ROOT=R.parents[2];E=ROOT/'experiments/ch05/05-01'
need=F(3350*10**9*600,10**9*132);occ=[]
for regs in (128,64):
 smem=2*64*64+2*64*64+4*64*64;reserved=smem+1024
 limits=dict(threads=2048//256,registers=65536//(256*regs),shared_memory=233472//reserved,block_limit=32);blocks=min(limits.values());warps=blocks*8;inflight=warps*4*32*16
 assert smem==32768 and limits['shared_memory']==6
 assert blocks==(2 if regs==128 else 4) and inflight>need
 occ.append(dict(registers_per_thread=regs,working_smem_bytes=smem,reserved_smem_bytes=reserved,limits=limits,resident_blocks=blocks,warps=warps,occupancy=warps/64,limiter=[k for k,v in limits.items() if v==blocks],inflight_bytes=inflight,required_bytes_exact=str(need),required_bytes=float(need)))
traffic=[]
for n in (64,128):
 m=64;k=32;M=1024;K=4096;N=12288
 a=2*M*K*(N//n);w=2*K*N*(M//m);o=2*M*N
 traffic.append(dict(tile=[m,k,n],local_a_bytes=2*m*k,local_w_bytes=2*k*n,accumulator_bytes=4*m*n,local_total_bytes=2*m*k+2*k*n+4*m*n,A_full_reads=N//n,W_full_reads=M//m,A_read_bytes=a,W_read_bytes=w,O_write_bytes=o,total_bytes=a+w+o))
ratio=F(traffic[1]['total_bytes'],traffic[0]['total_bytes']);assert ratio==F(97,129)
manifest=json.loads((E/'results/provenance.json').read_text())
for p,h in manifest['sha256'].items():assert hashlib.sha256((E/p).read_bytes()).hexdigest()==h,p
raw=json.loads((E/'results/results.json').read_text());cpu=[]
for shape in ((64,64,64),(128,512,64),(256,128,256),(127,257,65)):
 rows=[r for r in raw['rows'] if (r['m'],r['k'],r['n'])==shape and r['method'] in ('ijk','ikj')];assert len(rows)==2
 med={r['method']:statistics.median(r['samples_us']) for r in rows};assert all(len(r['samples_us'])==9 for r in rows)
 cpu.append(dict(shape=shape,median_us=med,ikj_speedup=med['ijk']/med['ikj'],GFLOPs_s={s:2*shape[0]*shape[1]*shape[2]/(t*1000) for s,t in med.items()}))
files=[ROOT/'manuscripts/05-算子与运行时.md',E/'results/results.json',E/'results/provenance.json',E/'results/compiler.log',E/'matmul.c']
out=dict(exercise_blocks=['5-1 occupancy','5-1 matrix tile'],occupancy=occ,traffic=traffic,strictly_faster_bandwidth_ratio_exact=str(ratio),strictly_faster_bandwidth_ratio=float(ratio),cpu=cpu,source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
(R/'5-1-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'},indent=2))
