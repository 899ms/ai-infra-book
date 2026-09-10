"""Real BF16 GEMM tiles, fixed operands, full FP64 reference and native counters."""
import argparse, hashlib, json, platform, random, subprocess, time
from pathlib import Path
import torch
import triton
import triton.language as tl
ROOT=Path(__file__).absolute().parent
CONFIGS=[(32,64,32,4),(64,64,32,4),(128,128,32,8)]
@triton.jit
def gemm(A,B,C,M:tl.constexpr,N:tl.constexpr,K:tl.constexpr,BM:tl.constexpr,BN:tl.constexpr,BK:tl.constexpr):
    m=tl.program_id(0)*BM+tl.arange(0,BM)
    n=tl.program_id(1)*BN+tl.arange(0,BN)
    k=tl.arange(0,BK)
    acc=tl.full((BM,BN),0,tl.float32)
    for offset in range(tl.cdiv(K,BK)):
        kk=offset*BK+k
        a=tl.load(A+m[:,None]*K+kk[None,:],(m[:,None]<M)&(kk[None,:]<K),other=0)
        b=tl.load(B+kk[:,None]*N+n[None,:],(kk[:,None]<K)&(n[None,:]<N),other=0)
        acc+=tl.dot(a,b)
    tl.store(C+m[:,None]*N+n[None,:],acc,(m[:,None]<M)&(n[None,:]<N))
def operands(m):
    # CPU generator makes saved operands independent of CUDA RNG implementation.
    g=torch.Generator().manual_seed(501)
    a=torch.randn(m,4096,generator=g).to(torch.bfloat16)
    b=torch.randn(4096,12288,generator=g).to(torch.bfloat16)
    return a,b

def launch(a,b,c,config):
    bm,bn,bk,w=config
    return gemm[(triton.cdiv(a.shape[0],bm),triton.cdiv(b.shape[1],bn))](a,b,c,a.shape[0],b.shape[1],a.shape[1],bm,bn,bk,num_warps=w,num_stages=2)
def digest(t):
    return hashlib.sha256(bytes(t.contiguous().view(torch.uint8).flatten().tolist())).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--profile',action='store_true');p.add_argument('--m',type=int,default=1024);p.add_argument('--config',type=int,default=0);a=p.parse_args()
    torch.set_num_threads(4);torch.cuda.set_per_process_memory_fraction(.12)
    torch.backends.cuda.matmul.allow_tf32=False
    if a.profile:
        x,y=operands(a.m);x=x.cuda();y=y.cuda();z=torch.empty((a.m,12288),device='cuda',dtype=torch.bfloat16)
        for _ in range(5):launch(x,y,z,CONFIGS[a.config])
        torch.cuda.synchronize();torch.cuda.cudart().cudaProfilerStart()
        launch(x,y,z,CONFIGS[a.config]);torch.cuda.synchronize();torch.cuda.cudart().cudaProfilerStop();return
    out=ROOT/'results';out.mkdir(exist_ok=False);(out/'code').mkdir()
    report=dict(seed=501,configs=CONFIGS,stages=2,shapes=[],timing=[],torch=torch.__version__,triton=triton.__version__,python=platform.python_version(),host=platform.node(),gpu=subprocess.check_output(['nvidia-smi','--query-gpu=name,driver_version,memory.free,clocks.sm','--format=csv'],text=True),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
    rng=random.Random(501)
    for m in (1,1024):
        x,y=operands(m);torch.save(dict(a=x,b=y),out/f'input-m{m}.pt')
        x=x.cuda();y=y.cuda();z=torch.empty((m,12288),device='cuda',dtype=torch.bfloat16)
        reference=x.double()@y.double(); checks=[]
        for i,cfg in enumerate(CONFIGS):
            t=time.monotonic();compiled=launch(x,y,z,cfg);torch.cuda.synchronize();first=time.monotonic()-t
            err=z.double()-reference
            relative=(err.norm()/reference.norm()).item();scaled=(err.abs()/(.05+.01*reference.abs())).max().item()
            checks.append(dict(config=i,relative_l2=relative,max_abs=err.abs().max().item(),scaled_max=scaled,pass_quality=relative<.005 and scaled<=1,first_call_s=first,registers=compiled.n_regs,spills=compiled.n_spills,shared_bytes=compiled.metadata.shared))
            torch.save(z.cpu(),out/f'output-m{m}-c{i}.pt')
            for name in ('ttir','ttgir','ptx','cubin'):
                content=compiled.asm[name];dest=out/'code'/f'm{m}-c{i}.{name}';dest.write_bytes(content if isinstance(content,bytes) else content.encode())
            for _ in range(5):launch(x,y,z,cfg)
        torch.save(reference.cpu(),out/f'reference-m{m}.pt')
        report['shapes'].append(dict(m=m,n=12288,k=4096,checks=checks))
        assert all(c['pass_quality'] for c in checks),checks
        torch.cuda.synchronize()
        for trial in range(9):
            order=list(range(3));rng.shuffle(order)
            for position,i in enumerate(order):
                start=torch.cuda.Event(enable_timing=True);end=torch.cuda.Event(enable_timing=True)
                start.record()
                for _ in range(20):launch(x,y,z,CONFIGS[i])
                end.record();end.synchronize()
                report['timing'].append(dict(m=m,trial=trial,position=position,config=i,repeats=20,ms_per_call=start.elapsed_time(end)/20))
        print(json.dumps(report['shapes'][-1]),flush=True)
        del x,y,z,reference
    report['finished_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());(out/'raw.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
