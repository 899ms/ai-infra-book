import json
from pathlib import Path
import torch
r=Path(__file__).absolute().parent;torch.set_num_threads(4)
w=torch.load(r/'expert.pt',map_location='cpu',weights_only=True)['reference_fp32'];prefill=torch.load(r/'prefill-pool.pt',map_location='cpu',weights_only=True)['input_bf16'].float()
index=json.loads((r/'source/index.json').read_text());decode=torch.cat([torch.load(r/'source'/x['file'],map_location='cpu',weights_only=True)['input_bf16'] for x in index]).float();rows=[]
for meta in json.loads((r/'results/raw.json').read_text()):
 d=torch.load(r/'results'/(meta['label']+'.pt'),map_location='cpu',weights_only=True);m=meta['m'];expected=(prefill if meta['phase']=='prefill' else decode)[:m];assert torch.equal(d['x'],expected)
 ref=expected.double()@w.double();assert torch.allclose(d['reference'].double(),ref,atol=2e-5,rtol=2e-5)
 weights=torch.load(r/'results'/('weights-'+meta['variant']+'.pt'),map_location='cpu',weights_only=True)
 dx=torch.cat([d['qx'][g][:m].double()*d['sx'][:,g].double() for g in range(16)],dim=1)
 dw=torch.cat([weights['qw'][g].double()*weights['sw'][g].double() for g in range(16)],dim=0)
 assert torch.allclose(d['direct'].double(),dx@dw,atol=2e-5,rtol=2e-5)
 checks={}
 for key in ['direct','dequant']:
  error=float(torch.linalg.vector_norm(d[key].double()-ref)/torch.linalg.vector_norm(ref));checks[key]=dict(relative_l2_to_cpu_fp64=error,passed=error<=.02)
 rows.append(dict(label=meta['label'],input_source_exact=True,checks=checks))
(r/'cpu-audit.json').write_text(json.dumps(dict(rows=rows,reference='CPU FP64 on original real input and decoded checkpoint weights; INT8 direct also checked against dequantized operand product'),indent=2)+'\n');print(json.dumps(rows))
