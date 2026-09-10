import argparse,asyncio,hashlib,json,os,time
from pathlib import Path
async def main(a):
 os.environ.update(VLLM_USE_FLASHINFER_SAMPLER='0',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
 a.out.mkdir(parents=True,exist_ok=False);os.environ['KV_OBSERVER_LOG']=str((a.out/'blocks.jsonl').absolute())
 import torch,vllm
 from transformers import AutoTokenizer
 from vllm import AsyncEngineArgs,AsyncLLMEngine,SamplingParams
 tok=AutoTokenizer.from_pretrained(a.model,local_files_only=True);ids=tok.encode('Explain bounded worker queues and completion ordering. '*500,add_special_tokens=False)[:1536];assert len(ids)==1536
 cfg=dict(model=a.model,dtype='bfloat16',max_model_len=2048,max_num_seqs=4,max_num_batched_tokens=512,enable_chunked_prefill=True,enable_prefix_caching=True,enforce_eager=True,async_scheduling=False,gpu_memory_utilization=.30,kv_cache_memory_bytes=1024**3,seed=803,scheduler_cls='observer.ObservedScheduler')
 r=Path(__file__).absolute().parent;(a.out/'environment.json').write_text(json.dumps(dict(config=cfg,torch=torch.__version__,vllm=vllm.__version__,hashes={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in ['run.py','observer.py']}),indent=2)+'\n');(a.out/'input.json').write_text(json.dumps(ids)+'\n')
 engine=AsyncLLMEngine.from_engine_args(AsyncEngineArgs(**cfg))
 try:
  with (a.out/'requests.jsonl').open('w',buffering=1) as log:
   for name,n in [('branches',4),('after',1)]:
    start=time.monotonic();events=[];final=None;completed={}
    async for result in engine.generate({'prompt_token_ids':ids},SamplingParams(n=n,temperature=.8,seed=803,max_tokens=128,ignore_eos=True),name):
     final=result;completed.update({x.index:x for x in result.outputs});events.append(dict(time=time.monotonic(),outputs=[dict(index=x.index,tokens=len(x.token_ids)) for x in result.outputs]))
    assert final.prompt_token_ids==ids and len(completed)==n
    log.write(json.dumps(dict(id=name,n=n,start=start,end=time.monotonic(),cached_tokens=final.num_cached_tokens,events=events,outputs=[dict(index=x.index,ids=list(x.token_ids),text=x.text,finish_reason=x.finish_reason) for x in sorted(completed.values(),key=lambda x:x.index)]))+'\n');print(name,n,flush=True)
  (a.out/'completion.json').write_text(json.dumps(dict(done=True,requests=2,sequences=5))+'\n')
 finally:engine.shutdown()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--out',type=Path,required=True);asyncio.run(main(p.parse_args()))
