import hashlib,json,random,subprocess,time
from pathlib import Path
import torch,triton
import triton.language as tl
R=Path(__file__).absolute().parent
@triton.jit
def row_norm(X,W,Y,N:tl.constexpr,B:tl.constexpr):
 row=tl.program_id(0);j=tl.arange(0,B)
 x=tl.load(X+row*N+j,j<N,0).to(tl.float32);w=tl.load(W+j,j<N,0).to(tl.float32)
 inv=tl.rsqrt(tl.sum(x*x,0)/N+1e-6)
 tl.store(Y+row*N+j,x*inv*w,j<N)
@triton.jit
def partial(X,P,N:tl.constexpr,S:tl.constexpr,B:tl.constexpr):
 row=tl.program_id(0);part=tl.program_id(1);j=part*B+tl.arange(0,B)
 x=tl.load(X+row*N+j,j<N,0).to(tl.float32)
 tl.store(P+row*S+part,tl.sum(x*x,0))
@triton.jit
def final_reduce(P,I,N:tl.constexpr,S:tl.constexpr,B:tl.constexpr):
 row=tl.program_id(0);j=tl.arange(0,B)
 v=tl.load(P+row*S+j,j<S,0)
 tl.store(I+row,tl.rsqrt(tl.sum(v,0)/N+1e-6))
@triton.jit
def apply_norm(X,W,I,Y,N:tl.constexpr,B:tl.constexpr):
 row=tl.program_id(0);j=tl.program_id(1)*B+tl.arange(0,B)
 x=tl.load(X+row*N+j,j<N,0).to(tl.float32);w=tl.load(W+j,j<N,0).to(tl.float32)
 inv=tl.load(I+row);tl.store(Y+row*N+j,x*inv*w,j<N)
def main():
 torch.set_num_threads(4);torch.cuda.set_per_process_memory_fraction(.12)
 out=R/'results';out.mkdir(exist_ok=False);(out/'code').mkdir()
 rng=random.Random(50151);report=dict(torch=torch.__version__,triton=triton.__version__,gpu=subprocess.check_output(['nvidia-smi','--query-gpu=name,driver_version,memory.free','--format=csv'],text=True),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),cases=[],timing=[])
 for n in [4096,65536]:
  gen=torch.Generator().manual_seed(50151);x_cpu=torch.randn(1024,n,generator=gen).to(torch.bfloat16);w_cpu=(torch.randn(n,generator=gen)*.1+1).to(torch.bfloat16)
  torch.save(dict(x=x_cpu,w=w_cpu),out/f'input-n{n}.pt');base=x_cpu.cuda();w=w_cpu.cuda()
  for m in [1,32,1024]:
   x=base[:m];y=torch.empty_like(x);s=triton.cdiv(n,1024);p=torch.empty((m,s),device='cuda',dtype=torch.float32);inv=torch.empty(m,device='cuda',dtype=torch.float32)
   def row():return [row_norm[(m,)](x,w,y,n,triton.next_power_of_2(n),num_warps=8)]
   def split():return [partial[(m,s)](x,p,n,s,1024,num_warps=4),final_reduce[(m,)](p,inv,n,s,triton.next_power_of_2(s),num_warps=4),apply_norm[(m,s)](x,w,inv,y,n,1024,num_warps=4)]
   funcs={'row':row,'split':split};checks={};graphs={}
   xd=x.double();reference=xd*torch.rsqrt((xd*xd).mean(1,keepdim=True)+1e-6)*w.double();del xd
   for name,fn in funcs.items():
    t=time.monotonic();kernels=fn();torch.cuda.synchronize();first=time.monotonic()-t
    saved=y.clone();err=y.double()-reference;rel=(err.norm()/reference.norm()).item();scaled=(err.abs()/(.01+.01*reference.abs())).max().item()
    metadata=[]
    for i,k in enumerate(kernels):
     metadata.append(dict(registers=k.n_regs,spills=k.n_spills,shared_bytes=k.metadata.shared))
     for ext in ['ttir','ttgir','ptx','cubin']:
      v=k.asm[ext];(out/'code'/f'n{n}-m{m}-{name}-{i}.{ext}').write_bytes(v if isinstance(v,bytes) else v.encode())
    repeated=[]
    for _ in range(5):fn();repeated.append(torch.equal(y,saved))
    torch.save(saved.cpu(),out/f'output-n{n}-m{m}-{name}.pt')
    checks[name]=dict(relative_l2=rel,scaled_max=scaled,max_abs=err.abs().max().item(),pass_quality=rel<.005 and scaled<=1,repeats_bitwise_equal=repeated,first_call_s=first,kernels=metadata)
    g=torch.cuda.CUDAGraph()
    with torch.cuda.graph(g):
     for _ in range(20):fn()
    graphs[name]=g
   torch.cuda.synchronize()
   for trial in range(9):
    order=[('row','eager'),('row','graph'),('split','eager'),('split','graph')];rng.shuffle(order)
    for pos,(name,mode) in enumerate(order):
     st=torch.cuda.Event(enable_timing=True);en=torch.cuda.Event(enable_timing=True);st.record()
     if mode=='graph':graphs[name].replay()
     else:
      for _ in range(20):funcs[name]()
     en.record();en.synchronize();report['timing'].append(dict(m=m,n=n,method=name,mode=mode,trial=trial,position=pos,repeats=20,us_per_call=st.elapsed_time(en)*1000/20))
   with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU,torch.profiler.ProfilerActivity.CUDA]) as prof:
    with torch.profiler.record_function('book_row'):row()
    with torch.profiler.record_function('book_split'):split()
    torch.cuda.synchronize()
   prof.export_chrome_trace(str(out/f'trace-n{n}-m{m}.json'))
   case=dict(m=m,n=n,parts=s,scratch_bytes=p.numel()*p.element_size()+inv.numel()*inv.element_size(),checks=checks)
   report['cases'].append(case);print(json.dumps(case),flush=True)
   del graphs,reference,p,inv,y
  del base,w,x_cpu,w_cpu
 (out/'raw.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
