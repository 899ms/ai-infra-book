import inspect,hashlib
from pathlib import Path
class AdapterProbe:
 def adapter_state(self):
  manager=self.model_runner.lora_manager
  return dict(registered=sorted(manager.list_adapters()),gpu_slot_ids=list(manager._adapter_manager.lora_index_to_id))
 def arm_projection(self,out):
  import torch
  self.capture_root=Path(out);self.capture_case=None;self.captured=False
  matches=[(n,m) for n,m in self.model_runner.model.named_modules() if n.endswith('layers.0.self_attn.qkv_proj')];assert len(matches)==1,[n for n,m in matches]
  name,module=matches[0]
  def hook(m,args,result):
   if self.capture_case is None or self.captured:return
   x=args[0];y=result[0] if isinstance(result,tuple) else result
   assert x.shape==(512,4096) and y.shape==(512,6144)
   payload=dict(input=x.detach().cpu().clone(),output=y.detach().cpu().clone(),lora_a=[z.detach().cpu().clone() for z in m.lora_a_stacked],lora_b=[z.detach().cpu().clone() for z in m.lora_b_stacked],slot_ids=self.adapter_state()['gpu_slot_ids'])
   torch.save(payload,self.capture_root/(self.capture_case+'-projection.pt'));self.captured=True
  self.projection_hook=module.register_forward_hook(hook)
  source=Path(inspect.getfile(type(module)));(self.capture_root/'native_projection.py').write_bytes(source.read_bytes())
  return dict(module=name,type=type(module).__name__,source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
 def set_projection_case(self,name):self.capture_case=name;self.captured=False
