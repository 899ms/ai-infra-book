"""Independent CPU audit of checkpoint blocks, serialized fixtures and outputs."""
import hashlib,json
from pathlib import Path
import torch
r=Path(__file__).absolute().parent;torch.set_num_threads(4)
meta=json.loads((r/'provenance.json').read_text());assert hashlib.sha256((r/'expert.pt').read_bytes()).hexdigest()==meta['artifact_sha256']
p=torch.load(r/'expert.pt',map_location='cpu',weights_only=True)
for k,h in meta['tensor_hashes'].items():assert hashlib.sha256(p[k].contiguous().view(torch.uint8).numpy().tobytes()).hexdigest()==h
q=p['checkpoint_fp8'];scale=p['checkpoint_scale'];reference=p['reference_fp32']
for i in range(16):
 for j in range(12):assert torch.equal(reference[i*128:(i+1)*128,j*128:(j+1)*128],q[i*128:(i+1)*128,j*128:(j+1)*128].float()*scale[i,j])
results=[]
for m in [1,8,64,512]:
 f=torch.load(r/f'results/fixture-m{m}.pt',map_location='cpu',weights_only=True)
 assert torch.equal(f['w'],reference) and torch.equal(f['qw'],p['int8_weight']) and torch.equal(f['sw'],p['int8_scale'])
 x=f['x'];ref64=x.double()@reference.double()
 assert torch.allclose(f['reference'].double(),ref64,atol=2e-5,rtol=2e-5)
 checks={}
 for mode in ['int8_direct','int8_dequant_bf16']:
  y=torch.load(r/f'results/output-m{m}-{mode}.pt',map_location='cpu',weights_only=True)
  error=float(torch.linalg.vector_norm(y.double()-ref64)/torch.linalg.vector_norm(ref64))
  checks[mode]=dict(relative_l2_to_cpu_fp64=error,passed=error<=.02)
 results.append(dict(m=m,checks=checks))
(r/'tensor-audit.json').write_text(json.dumps(dict(blocks_checked=192,source_tensor_hashes=True,all_shapes_same_weights=True,cpu_reference='FP64 matmul of synthetic input and decoded checkpoint matrix',rows=results),indent=2)+'\n');print(json.dumps(results))
