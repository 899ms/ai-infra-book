"""One condition per fresh CUDA process; allocator peaks, not total board memory."""
import argparse,json,gc,pickle,hashlib
from pathlib import Path
import torch
p=argparse.ArgumentParser();p.add_argument('--mode',choices=['direct','dequant'],required=True);p.add_argument('--phase',choices=['decode','prefill'],required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
r=Path(__file__).absolute().parent;a.out.mkdir(parents=True,exist_ok=False);torch.set_num_threads(4)
source=torch.load(r/'expert.pt',weights_only=True,map_location='cpu');data=torch.load(r/(a.phase+'.pt'),weights_only=True,map_location='cpu')
m=1 if a.phase=='decode' else 512;cpu_x=data['input_bf16'][:m].float();assert cpu_x.shape==(m,2048)
torch.cuda.init();torch.cuda.synchronize();torch.cuda.empty_cache()
def stats():
 return dict(allocated=torch.cuda.memory_allocated(),reserved=torch.cuda.memory_reserved(),peak_allocated=torch.cuda.max_memory_allocated(),peak_reserved=torch.cuda.max_memory_reserved())
baseline=stats()
# Both deployable paths start with just FP32 input, INT8 weights and column scales.
x=cpu_x.cuda();qw=source['int8_weight'].cuda();sw=source['int8_scale'].cuda()
blocks=[qw[g*128:(g+1)*128] for g in range(16)]
assert all(q.is_contiguous() for q in blocks)
torch.cuda.synchronize();resident=stats()

def quant():
 v=x.reshape(m,16,128);sx=v.abs().amax(2,keepdim=True).clamp_min(1e-12)/127;q=(v/sx).round().clamp(-127,127).to(torch.int8)
 parts=[]
 for g in range(16):
  b=q[:,g,:].contiguous()
  if m<32:b=torch.nn.functional.pad(b,(0,0,0,32-m))
  parts.append(b)
 return parts,sx

def operation():
 parts,sx=quant()
 if a.mode=='direct':
  y=torch.zeros((m,1536),device='cuda')
  for g in range(16):y.add_(torch._int_mm(parts[g],blocks[g])[:m].float()*sx[:,g]*sw)
  return y
 dx=torch.cat([parts[g][:m].float()*sx[:,g] for g in range(16)],dim=1).to(torch.bfloat16)
 # Match block-scales: expand each group, concatenate, then BF16 conversion.
 dw=torch.cat([b.float()*sw for b in blocks],dim=0).to(torch.bfloat16)
 return (dx@dw).float()

records=[];reference=None
for stage in ['cold','warm-0','warm-1','warm-2']:
 gc.collect();torch.cuda.synchronize()
 if stage=='cold':torch.cuda.empty_cache()
 torch.cuda.reset_peak_memory_stats();start=stats()
 torch.cuda.memory._record_memory_history(enabled='all',context='all',stacks='python',max_entries=100000)
 y=operation();torch.cuda.synchronize();end=stats()
 torch.cuda.memory._dump_snapshot(str(a.out/(stage+'-snapshot.pickle')))
 torch.cuda.memory._record_memory_history(enabled=None)
 value=y.cpu().clone()
 if reference is None:reference=value
 else:assert torch.equal(value,reference)
 records.append(dict(stage=stage,start=start,end=end,peak_increment_bytes=end['peak_allocated']-start['allocated'],output_bytes=y.numel()*y.element_size()))
 del y;torch.cuda.synchronize();records[-1]['after_output_release']=stats()
torch.save(dict(x=cpu_x,output=reference),a.out/'output.pt')
row=dict(mode=a.mode,phase=a.phase,m=m,baseline=baseline,resident=resident,resident_increment_bytes=resident['allocated']-baseline['allocated'],logical=dict(input=x.numel()*x.element_size(),int8_weight=qw.numel()*qw.element_size(),scale=sw.numel()*sw.element_size()),records=records,torch=torch.__version__,device=torch.cuda.get_device_name(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='PyTorch CUDA allocator; excludes driver/context and non-allocator library memory. No latency claim.')
(a.out/'measurement.json').write_text(json.dumps(row,indent=2)+'\n');print(a.mode,a.phase,row['resident_increment_bytes'],[v['peak_increment_bytes'] for v in records],flush=True)
