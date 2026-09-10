import json,hashlib,struct,argparse,math
from pathlib import Path
import torch
def load_file(path):
 raw=Path(path).read_bytes();length=struct.unpack('<Q',raw[:8])[0];header=json.loads(raw[8:8+length]);out={}
 for name,spec in header.items():
  assert spec['dtype']=='BF16';start,end=spec['data_offsets'];out[name]=torch.frombuffer(bytearray(raw[8+length+start:8+length+end]),dtype=torch.bfloat16).reshape(spec['shape']).clone()
 return out
r=Path(__file__).absolute().parent;torch.set_num_threads(4)
p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');args=p.parse_args()
load=lambda p:json.loads(p.read_text())
sup=load(r/'run/supervisor.json');assert sup['exit_code']==0 and not sup['leftovers'] and sup['reason'] is None
base=torch.load(r/'results/base-projection.pt',weights_only=True,map_location='cpu');x=base['input'].double();y0=base['output'].double();assert x.shape==(512,4096) and y0.shape==(512,6144)
checks=[]
for name in ['a','b']:
 t=torch.load(r/'results'/(name+'-projection.pt'),weights_only=True,map_location='cpu');assert torch.equal(t['input'],base['input'])
 file=r/'adapters'/name/'adapter_model.safetensors';assert hashlib.sha256(file.read_bytes()).hexdigest()==load(r/'adapters'/name/'provenance.json')['sha256']
 w=load_file(str(file));prefix='base_model.model.model.layers.0.self_attn.q_proj.';wa=w[prefix+'lora_A.weight'];wb=w[prefix+'lora_B.weight']
 assert len(t['lora_a'])==len(t['lora_b'])==3
 assert torch.equal(t['lora_a'][0][0,0],wa) and torch.equal(t['lora_b'][0][0,0],wb)
 assert all(torch.count_nonzero(v)==0 for v in t['lora_a'][1:]+t['lora_b'][1:])
 kv_exact=torch.equal(t['output'][:,4096:],base['output'][:,4096:]);assert kv_exact
 delta=(x@wa.double().T)@wb.double().T;observed=t['output'][:,:4096].double()-y0[:,:4096]
 changed=int(torch.count_nonzero(observed));assert changed>0
 error=float(torch.linalg.vector_norm(observed-delta)/torch.linalg.vector_norm(delta))
 output_error=float(torch.linalg.vector_norm(t['output'][:,:4096].double()-(y0[:,:4096]+delta))/torch.linalg.vector_norm(y0[:,:4096]+delta))
 checks.append(dict(adapter=name,changed_q_elements=changed,total_q_elements=observed.numel(),kv_exact=kv_exact,runtime_weights_exact=True,delta_relative_l2=error,delta_threshold=.02,delta_passed=error<=.02,output_relative_l2=output_error,observed_delta_l2=float(torch.linalg.vector_norm(observed)),fp64_delta_l2=float(torch.linalg.vector_norm(delta))))
summary=dict(rows=512,input_shape=list(x.shape),output_shape=list(y0.shape),checks=checks,scope='Full first-layer QKV projection for real input; not all-layer numeric validation or task quality')
if args.check:
 saved=load(r/'analysis.json')
 assert saved['rows']==summary['rows'] and saved['input_shape']==summary['input_shape'] and saved['output_shape']==summary['output_shape']
 for old,new in zip(saved['checks'],summary['checks']):
  assert old.keys()==new.keys()
  for k,v in new.items():
   assert math.isclose(old[k],v,rel_tol=1e-10,abs_tol=1e-12) if isinstance(v,float) else old[k]==v,(k,old[k],v)
 print('PASS: CPU reconstruction matches sealed audit within 1e-10 floating relative tolerance')
else:
 (r/'analysis.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
