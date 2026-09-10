import argparse,asyncio,hashlib,json,os,time
from pathlib import Path
async def main(a):
 os.environ.update(VLLM_USE_FLASHINFER_SAMPLER='0',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
 a.out.mkdir(parents=True,exist_ok=False);os.environ['KV_OBSERVER_LOG']=str((a.out/'blocks.jsonl').absolute())
 import torch,vllm
 from transformers import AutoTokenizer
 from vllm import AsyncEngineArgs,AsyncLLMEngine,SamplingParams
 from vllm.lora.request import LoRARequest
 r=Path(__file__).absolute().parent;tok=AutoTokenizer.from_pretrained(a.model,local_files_only=True)
 text='Explain bounded worker queues and completion ordering. '*500;ids=tok.encode(text,add_special_tokens=False)[:1536]
 cfg=dict(model=a.model,dtype='bfloat16',max_model_len=2048,max_num_seqs=4,max_num_batched_tokens=512,enable_chunked_prefill=True,enable_prefix_caching=True,enforce_eager=True,async_scheduling=False,gpu_memory_utilization=.30,kv_cache_memory_bytes=1024**3,seed=803,scheduler_cls='observer.ObservedScheduler',enable_lora=True,max_loras=a.slots,max_cpu_loras=2,max_lora_rank=8,worker_extension_cls='probe.AdapterProbe')
 (a.out/'environment.json').write_text(json.dumps(dict(config=cfg,torch=torch.__version__,vllm=vllm.__version__,hashes={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in ['run.py','observer.py','probe.py']}),indent=2)+'\n');(a.out/'input.json').write_text(json.dumps(ids)+'\n')
 adapters={name:LoRARequest('book-control-'+name+'-v1',80301+i,str(r/'adapters'/name)) for i,name in enumerate(['a','b'])}
 engine=AsyncLLMEngine.from_engine_args(AsyncEngineArgs(**cfg))
 try:
  with (a.out/'requests.jsonl').open('w',buffering=1) as log:
   async def one(rid,name,limit,wave):
    events=[];start=time.monotonic();final=None
    async for result in engine.generate({'prompt_token_ids':ids},SamplingParams(temperature=0,max_tokens=limit,ignore_eos=True),rid,lora_request=adapters[name]):
     final=result;events.append([time.monotonic(),len(result.outputs[0].token_ids)])
    seq=final.outputs[0];assert final.prompt_token_ids==ids and len(seq.token_ids)==limit
    row=dict(id=rid,adapter=name,wave=wave,start=start,end=time.monotonic(),events=events,cached_tokens=final.num_cached_tokens,output_ids=list(seq.token_ids),text=seq.text,finish_reason=seq.finish_reason)
    log.write(json.dumps(row)+'\n');print(rid,final.num_cached_tokens,flush=True)
   for name in ['a','b']:await one('warm-'+name,name,1,-1)
   for wave in range(3):
    await asyncio.gather(*(one(f'w{wave}-r{i}-{name}',name,64,wave) for i,name in enumerate(['a','b','a','b'])))
    state=await engine.collective_rpc('adapter_state')
    with (a.out/'slots.jsonl').open('a') as f:f.write(json.dumps(dict(wave=wave,state=state))+'\n')
  (a.out/'completion.json').write_text(json.dumps(dict(done=True,requests=14))+'\n')
 finally:engine.shutdown()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--slots',type=int,choices=[1,2],required=True);p.add_argument('--model',required=True);p.add_argument('--out',type=Path,required=True);asyncio.run(main(p.parse_args()))
