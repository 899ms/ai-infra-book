import argparse,hashlib,json,random,time
from pathlib import Path
import torch
r=Path(__file__).absolute().parent
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=False)
torch.set_num_threads(4)
source=torch.load(r/'expert.pt',map_location='cpu',weights_only=True);w=source['reference_fp32'].cuda();k,n=w.shape;assert (k,n)==(2048,1536)
prefill=torch.load(r/'prefill-pool.pt',map_location='cpu',weights_only=True)['input_bf16'][:512].float()
index=json.loads((r/'source/index.json').read_text());parts=[]
for row in index:
 file=r/'source'/row['file'];assert hashlib.sha256(file.read_bytes()).hexdigest()==row['source_sha256']
 t=torch.load(file,map_location='cpu',weights_only=True);assert t['topk_ids'].shape[0]==1 and bool((t['topk_ids']==0).any());parts.append(t['input_bf16'])
decode=torch.cat(parts).float();assert decode.shape==(37,2048)
(a.out/'environment.json').write_text(json.dumps(dict(torch=torch.__version__,device=torch.cuda.get_device_name(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),groups=16,block_k=128,threshold=.02,decode_rows=37,expert_sha256=hashlib.sha256((r/'expert.pt').read_bytes()).hexdigest()),indent=2)+'\n')

def quant(x):
 m=x.shape[0];v=x.reshape(m,16,128);sx=v.abs().amax(2,keepdim=True).clamp_min(1e-12)/127;q=(v/sx).round().clamp(-127,127).to(torch.int8)
 blocks=[]
 for g in range(16):
  b=q[:,g,:].contiguous()
  if m<32:b=torch.nn.functional.pad(b,(0,0,0,32-m))
  blocks.append(b)
 return blocks,sx

def timing(fn):
 torch.cuda.synchronize();start=torch.cuda.Event(enable_timing=True);end=torch.cuda.Event(enable_timing=True);wall=time.perf_counter();start.record()
 for _ in range(10):fn()
 end.record();end.synchronize();return dict(device_ms=start.elapsed_time(end)/10,wall_ms=(time.perf_counter()-wall)*100)
rows=[]
for variant in ['activation','both']:
 qws=[];sws=[];shared_column_scale=source['int8_scale'].cuda()
 for g in range(16):
  raw=w[g*128:(g+1)*128]
  if variant=='activation':qw=source['int8_weight'][g*128:(g+1)*128].cuda();sw=shared_column_scale
  else:sw=raw.abs().amax(0).clamp_min(1e-12)/127;qw=(raw/sw).round().clamp(-127,127).to(torch.int8).contiguous()
  qws.append(qw);sws.append(sw)
 def decode_w():return torch.cat([q.float()*s for q,s in zip(qws,sws)],dim=0).to(torch.bfloat16)
 def direct(x):
  qs,sx=quant(x);out=torch.zeros(x.shape[0],n,device='cuda')
  for g in range(16):out.add_(torch._int_mm(qs[g],qws[g])[:x.shape[0]].float()*sx[:,g]*sws[g])
  return out
 def dequant(x):
  qs,sx=quant(x);decoded=torch.cat([qs[g][:x.shape[0]].float()*sx[:,g] for g in range(16)],dim=1).to(torch.bfloat16)
  return (decoded@decode_w()).float()
 torch.save(dict(qw=[x.cpu() for x in qws],sw=[x.cpu() for x in sws]),a.out/f'weights-{variant}.pt')
 for phase,m in [('prefill',1),('prefill',8),('prefill',64),('prefill',512),('decode',1),('decode',8)]:
  x=(prefill if phase=='prefill' else decode)[:m].cuda();ref=x@w;qs,sx=quant(x);integer_exact=True
  for g in range(16):integer_exact &= torch.equal(torch._int_mm(qs[g],qws[g]),(qs[g].double()@qws[g].double()).to(torch.int32))
  assert integer_exact
  yd=direct(x);yq=dequant(x);checks={name:dict(relative_l2=float(torch.linalg.vector_norm(y-ref)/torch.linalg.vector_norm(ref))) for name,y in [('direct',yd),('dequant',yq)]}
  for v in checks.values():v['passed']=v['relative_l2']<=.02
  label=f'{variant}-{phase}-m{m}'
  torch.save(dict(x=x.cpu(),reference=ref.cpu(),direct=yd.cpu(),dequant=yq.cpu(),qx=[z.cpu() for z in qs],sx=sx.cpu()),a.out/(label+'.pt'))
  funcs={'direct':lambda:direct(x),'dequant':lambda:dequant(x),'activation_quant':lambda:quant(x),'weight_dequant':decode_w}
  for fn in funcs.values():
   for _ in range(3):fn()
  order=[(i,key) for i in range(9) for key in funcs];random.Random(402+m).shuffle(order)
  samples=[dict(trial=i,stage=key,**timing(funcs[key])) for i,key in order]
  with torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU,torch.profiler.ProfilerActivity.CUDA]) as prof:
   for name,fn in [('direct',lambda:direct(x)),('dequant',lambda:dequant(x))]:
    with torch.profiler.record_function(name):fn();torch.cuda.synchronize()
  prof.export_chrome_trace(str(a.out/(label+'-trace.json')))
  rows.append(dict(label=label,variant=variant,phase=phase,m=m,checks=checks,integer_exact=integer_exact,weight_scale_logical_bytes=sum(z.numel()*z.element_size() for z in sws),weight_scale_unique_storage_bytes=sum({z.untyped_storage().data_ptr():z.untyped_storage().nbytes() for z in sws}.values()),activation_scale_bytes=sx.numel()*sx.element_size(),samples=samples))
  (a.out/'raw.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,checks,flush=True)
(a.out/'completion.json').write_text(json.dumps(dict(status='completed',conditions=len(rows)))+'\n')
