import argparse,json,time,os,hashlib
from pathlib import Path
import torch
from transformers import AutoTokenizer,AutoModelForCausalLM
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--name',required=True);a=p.parse_args();O=R/a.name;O.mkdir(exist_ok=False)
M='/home/ubuntu/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218';s=json.loads((R/'rtx-input.json').read_text());start=time.monotonic();tokens=[];result=dict(status='running',pid=os.getpid(),model=M,start_s=start,source_sha256={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['rtx_generate.py','rtx-input.json','PROTOCOL.md']})
try:
 tok=AutoTokenizer.from_pretrained(M,local_files_only=True);model=AutoModelForCausalLM.from_pretrained(M,dtype=torch.bfloat16,attn_implementation='sdpa',local_files_only=True).to('cuda');model.eval();model.requires_grad_(False)
 ids=torch.tensor([s['prompt_ids']],device='cuda');cache=None;eos=model.generation_config.eos_token_id;eos=set(eos if isinstance(eos,list) else [eos]);torch.cuda.synchronize();result['ready_s']=time.monotonic()
 with torch.inference_mode():
  for seq in range(768):
   before=time.monotonic();out=model(input_ids=ids,past_key_values=cache,use_cache=True);cache=out.past_key_values;token=int(out.logits[0,-1].argmax());torch.cuda.synchronize();now=time.monotonic();tokens.append(token)
   with (O/'generated.jsonl').open('a') as f:f.write(json.dumps(dict(seq=seq,token=token,eos=token in eos,start_s=before,end_s=now))+'\n')
   if token in eos:break
   ids=torch.tensor([[token]],device='cuda')
 assert tokens[-1] in eos
 result.update(status='complete',token_ids=tokens,text=tok.decode(tokens,skip_special_tokens=True),tokens_equal_reference=tokens==s['output_ids'])
finally:
 result.update(end_s=time.monotonic(),cuda_peak_allocated_bytes=torch.cuda.max_memory_allocated())
 with (O/'raw.json').open('x') as f:json.dump(result,f,indent=2);f.flush();os.fsync(f.fileno())
print(result['status'],len(tokens),result.get('tokens_equal_reference'),flush=True)
