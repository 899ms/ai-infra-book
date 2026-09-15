"""Single GPU H2D/GEMM overlap control for current exercise 6-5(d)."""
import torch, json, random, hashlib, subprocess, platform
from pathlib import Path
P=Path(__file__).resolve().parent
assert not (P/'results.json').exists(), 'Preserve completed run'
torch.set_num_threads(4)
torch.backends.cuda.matmul.allow_tf32=False
rng=torch.Generator().manual_seed(605)
a_cpu=torch.randint(-2,3,(16,4096),generator=rng).float()
b_cpu=torch.randint(-2,3,(4096,4096),generator=rng).float()
ref=(a_cpu.double()@b_cpu.double()).float()
a=a_cpu.cuda(); b=b_cpu.cuda(); c=torch.empty((16,4096),device='cuda')
streams=[torch.cuda.Stream(),torch.cuda.Stream()]
rows=[]; randomizer=random.Random(605)
for size in (4*2**20,64*2**20):
 host=torch.arange(size//4,dtype=torch.float32).pin_memory()
 target=torch.empty_like(host,device='cuda')
 for trial in range(-3,11):
  modes=['transfer','compute','shared'];randomizer.shuffle(modes)
  for mode in modes:
   target.zero_();c.zero_();torch.cuda.synchronize()
   origin=torch.cuda.Event(enable_timing=True)
   events={key:(torch.cuda.Event(enable_timing=True),torch.cuda.Event(enable_timing=True)) for key in ('transfer','compute')}
   # Delay release so the CPU can queue both branches before they become ready.
   torch.cuda._sleep(20_000_000)
   origin.record()
   for key,stream in zip(('transfer','compute'),streams):
    if mode not in (key,'shared'):continue
    with torch.cuda.stream(stream):
     stream.wait_event(origin)
     events[key][0].record()
     if key=='transfer':target.copy_(host,non_blocking=True)
     else:torch.mm(a,b,out=c)
     events[key][1].record()
   torch.cuda.synchronize()
   marks={key:dict(ready_ms=0.,start_ms=origin.elapsed_time(e[0]),end_ms=origin.elapsed_time(e[1]),duration_ms=e[0].elapsed_time(e[1])) for key,e in events.items() if mode in (key,'shared')}
   for q in marks.values():assert 0<=q['start_ms']<=q['end_ms']
   transfer_ok=bool(torch.equal(target.cpu(),host)) if mode!='compute' else None
   compute_ok=bool(torch.equal(c.cpu(),ref)) if mode!='transfer' else None
   assert transfer_ok is not False and compute_ok is not False
   rows.append(dict(bytes=size,trial=trial,warmup=trial<0,mode=mode,events=marks,transfer_exact=transfer_ok,compute_exact=compute_ok,makespan_ms=max(q['end_ms'] for q in marks.values())))
out=dict(scope='One RTX GPU, pinned H2D copy plus FP32 GEMM [16,4096]@[4096,4096]; not AllReduce or multi-GPU communication',shape=[16,4096,4096],dtype='float32',tf32=False,seed=605,torch=torch.__version__,python=platform.python_version(),device=torch.cuda.get_device_name(),gpu_before=subprocess.check_output(['nvidia-smi','--query-gpu=name,driver_version','--format=csv,noheader'],text=True).strip(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),input_sha256={k:hashlib.sha256(v.numpy().tobytes()).hexdigest() for k,v in [('a',a_cpu),('b',b_cpu),('reference',ref)]},rows=rows,limitations=['CUDA events bracket operation stream intervals, not instruction-level kernel start','Readiness is common artificial release event after delay; stream start can include scheduling delay','H2D uses copy engine and PCIe; cannot substitute for NCCL SM/network contention'])
(P/'results.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS: 84 cases including 18 warmups; every executed transfer and GEMM exact')
