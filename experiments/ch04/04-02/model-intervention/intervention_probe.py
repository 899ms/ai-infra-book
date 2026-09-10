"""Overwrite only layer-0 expert-0 first GEMM assignment rows; quality experiment."""
import hashlib, inspect, json
from pathlib import Path
class InterventionProbe:
 def arm_intervention(self,out,weights):
  import torch
  import vllm.model_executor.layers.fused_moe.experts.triton_moe as tm
  self.root=Path(out);self.case=None;self.current=None;self.context=None;self.step=0
  source=torch.load(weights,map_location='cpu',weights_only=True)
  qw=source['int8_weight'].cuda();sw=source['int8_scale'].cuda()
  blocks=[qw[g*128:(g+1)*128].contiguous() for g in range(16)]
  dw=(qw.float()*sw).to(torch.bfloat16)
  matches=[(n,m) for n,m in self.model_runner.model.named_modules() if n.endswith('layers.0.mlp')]
  assert len(matches)==1
  name,module=matches[0];forward=module.forward
  def wrapped_forward(hidden_states,*args,**kwargs):
   self.current=hidden_states
   try:return forward(hidden_states,*args,**kwargs)
   finally:self.current=None
  module.forward=wrapped_forward
  apply=tm.TritonExperts.apply;sig=inspect.signature(apply);kernel=tm.invoke_fused_moe_triton_kernel
  checked=False
  def wrapped_apply(expert,output,hidden_states,w1,w2,topk_weights,topk_ids,*args,**kwargs):
   nonlocal checked
   active=self.current is not None and self.case is not None
   if active:
    data=sig.bind(expert,output,hidden_states,w1,w2,topk_weights,topk_ids,*args,**kwargs).arguments
    assert not data['apply_router_weight_on_input']
    assert self.current.shape[0]==topk_ids.shape[0]
    if not checked:
     assert torch.equal(w1[0].cpu().view(torch.uint8),source['checkpoint_fp8'].T.contiguous().view(torch.uint8))
     assert torch.equal(expert.w1_scale[0].cpu(),source['checkpoint_scale'].T.contiguous())
     checked=True
    self.context=(w1.data_ptr(),topk_ids)
   try:return apply(expert,output,hidden_states,w1,w2,topk_weights,topk_ids,*args,**kwargs)
   finally:
    if active:self.context=None
  def wrapped_kernel(A,B,C,*args,**kwargs):
   result=kernel(A,B,C,*args,**kwargs)
   if self.context is None or B.data_ptr()!=self.context[0]:return result
   ids=self.context[1];flat=C.view(-1,C.shape[-1]);assert flat.shape==(ids.numel(),1536)
   positions=(ids==0).nonzero();rows=positions[:,0]*ids.shape[1]+positions[:,1]
   x=self.current.index_select(0,positions[:,0]).float();m=x.shape[0]
   before=flat.clone()
   if m:
    v=x.reshape(m,16,128);sx=v.abs().amax(2,keepdim=True).clamp_min(1e-12)/127
    q=(v/sx).round().clamp(-127,127).to(torch.int8)
    if self.mode=='direct':
     y=torch.zeros((m,1536),device=x.device)
     for g in range(16):
      part=q[:,g].contiguous()
      if m<32:part=torch.nn.functional.pad(part,(0,0,0,32-m))
      y.add_(torch._int_mm(part,blocks[g])[:m].float()*sx[:,g]*sw)
    else:
     dx=(q.float()*sx).reshape(m,2048).to(torch.bfloat16);y=dx@dw
    flat.index_copy_(0,rows,y.to(flat.dtype))
   mask=torch.ones(flat.shape[0],dtype=torch.bool,device=flat.device);mask[rows]=False
   assert torch.equal(flat[mask],before[mask]),'unselected outputs changed'
   tag=f'{self.case}-{self.step:03d}';self.step+=1
   torch.save(dict(input_bf16=x.to(torch.bfloat16).cpu().clone(),positions=positions.cpu().clone(),topk_ids=ids.cpu().clone(),native=before.index_select(0,rows).cpu().clone(),replacement=flat.index_select(0,rows).cpu().clone()),self.root/(tag+'.pt'))
   with (self.root/'interventions.jsonl').open('a') as f:f.write(json.dumps(dict(case=self.case,mode=self.mode,step=self.step-1,file=tag+'.pt',input_rows=ids.shape[0],selected_rows=m,unselected_exact=True,weight_verified=checked))+'\n')
   return result
  tm.TritonExperts.apply=wrapped_apply;tm.invoke_fused_moe_triton_kernel=wrapped_kernel
  return dict(layer=name,expert=0,block_k=128,weights_sha256=hashlib.sha256(Path(weights).read_bytes()).hexdigest(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='Native GEMM followed by selected output overwrite; timing is not a speed benchmark')
 def set_intervention_case(self,case,mode):
  assert mode in ('direct','dequant');self.case=case;self.mode=mode;self.step=0
