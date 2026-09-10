"""Read-only capture of real layer-0 expert-0 inputs and native top-k decisions."""
import hashlib,inspect,json
from pathlib import Path
class CaptureProbe:
 def arm_capture(self,out):
  import torch
  from vllm.model_executor.layers.fused_moe.experts.triton_moe import TritonExperts
  self.capture_root=Path(out);self.capture_case=None;self.capture_step=0;self.current_input=None;self.saved_weight=False
  matches=[(n,m) for n,m in self.model_runner.model.named_modules() if n.endswith('layers.0.mlp')]
  assert len(matches)==1,[n for n,m in matches]
  name,module=matches[0];orig_forward=module.forward
  def forward(hidden_states,*args,**kwargs):
   self.current_input=hidden_states
   try:return orig_forward(hidden_states,*args,**kwargs)
   finally:self.current_input=None
  module.forward=forward
  original=TritonExperts.apply;signature=inspect.signature(original)
  def apply(expert,output,hidden_states,w1,w2,topk_weights,topk_ids,*args,**kwargs):
   if self.current_input is not None and self.capture_case is not None:
    data=signature.bind(expert,output,hidden_states,w1,w2,topk_weights,topk_ids,*args,**kwargs).arguments
    assert self.current_input.shape[0]==topk_ids.shape[0]
    ids=topk_ids.detach().cpu().clone();positions=(ids==0).any(dim=1).nonzero().flatten()
    x=self.current_input.detach().index_select(0,positions.to(self.current_input.device)).cpu().clone()
    assert not data['apply_router_weight_on_input']
    tag=f'{self.capture_case}-{self.capture_step:03d}';self.capture_step+=1
    payload=dict(input_bf16=x,token_positions=positions,topk_ids=ids)
    torch.save(payload,self.capture_root/(tag+'.pt'))
    row=dict(case=self.capture_case,step=self.capture_step-1,file=tag+'.pt',input_rows=self.current_input.shape[0],selected_rows=x.shape[0],input_dtype=str(x.dtype),prepared_dtype=str(hidden_states.dtype),layer=name,expert_index=0,top_k=ids.shape[1],apply_router_weight_on_input=False)
    with (self.capture_root/'activations.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    if not self.saved_weight:
     torch.save(dict(weight=w1[0].detach().cpu().clone(),scale=expert.w1_scale[0].detach().cpu().clone()),self.capture_root/'runtime-expert.pt');self.saved_weight=True
   return original(expert,output,hidden_states,w1,w2,topk_weights,topk_ids,*args,**kwargs)
  TritonExperts.apply=apply
  return dict(layer=name,expert_index=0,observer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),kernel_source_sha256=hashlib.sha256(Path(inspect.getfile(TritonExperts)).read_bytes()).hexdigest(),scope='Pre-quantization BF16 rows whose actual top-k includes expert 0; no route or return mutation')
 def set_capture_case(self,case):
  self.capture_case=case;self.capture_step=0
