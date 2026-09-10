import json,hashlib
from pathlib import Path
import torch
from safetensors.torch import save_file
r=Path(__file__).absolute().parent
for name,seed in [('a',80301),('b',80302)]:
 d=r/'adapters'/name;d.mkdir(parents=True,exist_ok=False);g=torch.Generator().manual_seed(seed);weights={}
 for layer in range(36):
  for part,shape in [('A',(8,4096)),('B',(4096,8))]:weights[f'base_model.model.model.layers.{layer}.self_attn.q_proj.lora_{part}.weight']=(torch.randn(shape,generator=g)*.05).to(torch.bfloat16)
 save_file(weights,str(d/'adapter_model.safetensors'))
 (d/'adapter_config.json').write_text(json.dumps(dict(peft_type='LORA',task_type='CAUSAL_LM',r=8,lora_alpha=8,target_modules=['q_proj'],bias='none'),indent=2)+'\n')
 (d/'provenance.json').write_text(json.dumps(dict(seed=seed,trained=False,scope='Nonzero random control adapter, not a task-trained model',tensor_count=len(weights),nonzero=sum(int(torch.count_nonzero(x)) for x in weights.values()),sha256=hashlib.sha256((d/'adapter_model.safetensors').read_bytes()).hexdigest()),indent=2)+'\n')
