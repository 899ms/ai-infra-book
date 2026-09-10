import hashlib,json,time
from pathlib import Path
import torch,triton
import triton.language as tl
R=Path(__file__).absolute().parent
@triton.jit
def streamed_row(X,W,Y,N:tl.constexpr,B:tl.constexpr):
 row=tl.program_id(0);j=tl.arange(0,B);total=tl.full((),0,tl.float32)
 for offset in range(N//B):
  x=tl.load(X+row*N+offset*B+j).to(tl.float32)
  total+=tl.sum(x*x,0)
 inv=tl.rsqrt(total/N+1e-6)
 for offset in range(N//B):
  jj=offset*B+j;x=tl.load(X+row*N+jj).to(tl.float32);w=tl.load(W+jj).to(tl.float32)
  tl.store(Y+row*N+jj,x*inv*w)
def main():
 torch.set_num_threads(4);torch.cuda.set_per_process_memory_fraction(.12)
 out=R/'streamed';out.mkdir(exist_ok=False);report=dict(cases=[],timing=[],source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),input_sha256=hashlib.sha256((R/'results/input-n65536.pt').read_bytes()).hexdigest())
 inp=torch.load(R/'results/input-n65536.pt',weights_only=True,map_location='cpu');base=inp['x'].cuda();w=inp['w'].cuda();n=65536
 for m in [1,32,1024]:
  x=base[:m];y=torch.empty_like(x)
  def call():return streamed_row[(m,)](x,w,y,n,1024,num_warps=4)
  t=time.monotonic();k=call();torch.cuda.synchronize();first=time.monotonic()-t
  saved=y.clone();xd=x.double();ref=xd*torch.rsqrt(xd.square().mean(1,keepdim=True)+1e-6)*w.double();err=y.double()-ref;rel=(err.norm()/ref.norm()).item();scaled=(err.abs()/(.01+.01*ref.abs())).max().item()
  repeated=[]
  for _ in range(5):call();repeated.append(torch.equal(saved,y))
  torch.save(saved.cpu(),out/f'output-m{m}.pt')
  for ext in ['ttir','ttgir','ptx','cubin']:
   v=k.asm[ext];(out/f'm{m}.{ext}').write_bytes(v if isinstance(v,bytes) else v.encode())
  g=torch.cuda.CUDAGraph()
  with torch.cuda.graph(g):
   for _ in range(20):call()
  for trial in range(9):
   for mode in (['eager','graph'] if trial%2==0 else ['graph','eager']):
    st=torch.cuda.Event(enable_timing=True);en=torch.cuda.Event(enable_timing=True);st.record()
    if mode=='graph':g.replay()
    else:
     for _ in range(20):call()
    en.record();en.synchronize();report['timing'].append(dict(m=m,mode=mode,trial=trial,repeats=20,us_per_call=st.elapsed_time(en)*1000/20))
  with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU,torch.profiler.ProfilerActivity.CUDA]) as prof:call();torch.cuda.synchronize()
  prof.export_chrome_trace(str(out/f'trace-m{m}.json'))
  case=dict(m=m,n=n,relative_l2=rel,scaled_max=scaled,pass_quality=rel<.005 and scaled<=1,repeats_bitwise_equal=repeated,first_call_s=first,registers=k.n_regs,spills=k.n_spills,shared_bytes=k.metadata.shared,scratch_bytes=0)
  report['cases'].append(case);print(json.dumps(case),flush=True);del g,xd,ref,err,saved,y
 (out/'raw.json').write_text(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
