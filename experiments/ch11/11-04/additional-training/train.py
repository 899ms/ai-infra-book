import hashlib,json,os,time,platform,importlib.metadata
from pathlib import Path
import torch
from transformers import AutoModelForCausalLM,AutoTokenizer
R=Path(__file__).resolve().parent;O=R/'results';O.mkdir(exist_ok=False)
M='/home/ubuntu/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def th(t):return hashlib.sha256(t.detach().cpu().contiguous().view(torch.uint8).numpy().tobytes()).hexdigest()
def sync():torch.cuda.synchronize()
class LoRA(torch.nn.Module):
 def __init__(self,base):
  super().__init__();self.base=base
  self.A=torch.nn.Parameter(torch.randn(4,base.in_features,device='cuda',dtype=torch.float32)*.01)
  self.B=torch.nn.Parameter(torch.zeros(base.out_features,4,device='cuda',dtype=torch.float32))
 def forward(self,x):return self.base(x)+(x.float()@self.A.T@self.B.T).to(x.dtype)
start=time.monotonic();rows=[]
meta=dict(status='running',pid=os.getpid(),start_s=start,model=M,versions={n:importlib.metadata.version(n) for n in ['torch','transformers']},host=platform.node(),source_sha256={n:sha(R/n) for n in ['train.py','samples.json','PROTOCOL.md','export.py']})
try:
 torch.manual_seed(1105);torch.cuda.manual_seed_all(1105)
 tok=AutoTokenizer.from_pretrained(M,local_files_only=True)
 samples=json.loads((R/'samples.json').read_text())['samples']
 for s in samples:assert tok.decode(s['output_ids'],skip_special_tokens=True)==s['expected_text']
 model=AutoModelForCausalLM.from_pretrained(M,dtype=torch.bfloat16,attn_implementation='sdpa',local_files_only=True).to('cuda');model.eval();model.requires_grad_(False)
 layer=model.model.layers[-1].self_attn;adapter=LoRA(layer.q_proj);layer.q_proj=adapter
 initial={n:p.detach().clone() for n,p in adapter.named_parameters() if p.requires_grad};assert set(initial)=={'A','B'}
 sync();meta.update(preparation_s=time.monotonic()-start,trainable_parameters=sum(p.numel() for p in [adapter.A,adapter.B]),initial_tensor_sha256={n:th(t) for n,t in initial.items()})
 for s in samples:
  t=time.monotonic()
  with torch.no_grad():
   for n,p in [('A',adapter.A),('B',adapter.B)]:p.copy_(initial[n])
  optimizer=torch.optim.AdamW([adapter.A,adapter.B],lr=.001,weight_decay=0)
  optimizer.zero_grad(set_to_none=True)
  ids=torch.tensor([s['prompt_ids']+s['output_ids']],device='cuda');labels=ids.clone();labels[:,:len(s['prompt_ids'])]=-100
  assert int((labels[:,1:]!=-100).sum())==len(s['output_ids'])
  sync();forward=time.monotonic();loss=model(input_ids=ids,labels=labels,use_cache=False).loss;sync();forward_end=time.monotonic();assert torch.isfinite(loss)
  loss.backward();sync();backward_end=time.monotonic();grad={n:float(p.grad.norm()) for n,p in [('A',adapter.A),('B',adapter.B)]};assert all(torch.isfinite(p.grad).all() for p in [adapter.A,adapter.B]) and grad['B']>0
  optimizer.step();sync();step_end=time.monotonic();weights={n:p.detach().cpu().clone() for n,p in [('A',adapter.A),('B',adapter.B)]};assert th(weights['B'])!=th(initial['B'])
  state=dict(adapter=weights,optimizer=optimizer.state_dict(),request_id=s['request_id'],sample_sha256=s['sample_sha256'],trained_output_tokens=len(s['output_ids']),model=M)
  dst=O/(s['request_id']+'.pt');tmp=dst.with_suffix('.tmp')
  with tmp.open('xb') as f:torch.save(state,f);f.flush();os.fsync(f.fileno())
  tmp.replace(dst);fd=os.open(O,os.O_RDONLY);os.fsync(fd);os.close(fd)
  restored=torch.load(dst,map_location='cpu',weights_only=True)
  for n in weights:assert torch.equal(restored['adapter'][n],weights[n])
  for v in restored['optimizer']['state'].values():assert int(v['step'])==1
  assert restored['sample_sha256']==s['sample_sha256'] and restored['trained_output_tokens']==len(s['output_ids'])
  row=dict(request_id=s['request_id'],sample_sha256=s['sample_sha256'],loss=float(loss),gradient_norms=grad,completed_training_tokens=len(s['output_ids']),start_s=t,end_s=time.monotonic(),forward_s=forward_end-forward,backward_s=backward_end-forward_end,optimizer_s=step_end-backward_end,checkpoint_and_verify_s=time.monotonic()-step_end,adapter_sha256={n:th(v) for n,v in weights.items()},checkpoint_sha256=sha(dst),optimizer_step=1)
  rows.append(row)
  with (O/'events.jsonl').open('a') as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())
  print(s['request_id'],row['completed_training_tokens'],row['loss'],'checkpoint verified',flush=True)
 meta['status']='all_samples_checkpointed'
finally:
 meta.update(rows=rows,end_s=time.monotonic(),cuda_peak_allocated_bytes=torch.cuda.max_memory_allocated());(O/'raw.json').write_text(json.dumps(meta,indent=2)+'\n')
