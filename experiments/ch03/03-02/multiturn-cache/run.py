import argparse,asyncio,hashlib,json,os,random,time
from pathlib import Path
from dataclasses import asdict
r=Path(__file__).absolute().parent
async def main(a):
 os.environ.update(VLLM_USE_FLASHINFER_SAMPLER='0',HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1')
 import torch,vllm
 from transformers import AutoTokenizer
 from vllm import AsyncEngineArgs,AsyncLLMEngine,SamplingParams
 from vllm.v1.metrics.loggers import StatLoggerBase
 a.out.mkdir(parents=True,exist_ok=False)
 tok=AutoTokenizer.from_pretrained(a.model,local_files_only=True)
 tasks=[]
 for client in range(4):
  rng=random.Random(302900+client);values={f'k{i:04d}':str(rng.randrange(100000,1000000)) for i in range(512)}
  doc='\n'.join(k+' = '+v for k,v in values.items())
  groups=[['k0064','k0256','k0447'],['k0007','k0100','k0500'],['k0031','k0300','k0480']]
  tasks.append(dict(client=client,values=values,document=doc,groups=groups))
 (a.out/'tasks.json').write_text(json.dumps(tasks)+'\n')
 cfg=dict(model=a.model,dtype='bfloat16',kv_cache_dtype='auto',max_model_len=8192,max_num_seqs=1,max_num_batched_tokens=2048,enable_chunked_prefill=True,enable_prefix_caching=a.apc,enforce_eager=True,async_scheduling=False,gpu_memory_utilization=.30,kv_cache_memory_bytes=2*1024**3,seed=302,attention_backend='TRITON_ATTN')
 (a.out/'environment.json').write_text(json.dumps(dict(config=cfg,torch=torch.__version__,vllm=vllm.__version__,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
 state={'request':None};stats=(a.out/'scheduler.jsonl').open('w',buffering=1)
 class Logger(StatLoggerBase):
  def __init__(self,*args,**kwargs):pass
  def log_engine_initialized(self):pass
  def record(self,scheduler_stats,iteration_stats,mm_cache_stats=None,engine_idx=0):
   stats.write(json.dumps(dict(time=time.monotonic(),request=state['request'],running=scheduler_stats.num_running_reqs,waiting=scheduler_stats.num_waiting_reqs,kv_usage=scheduler_stats.kv_cache_usage,preemptions=getattr(iteration_stats,'num_preempted_reqs',0) if iteration_stats else 0))+'\n')
 engine=None
 try:
  engine=AsyncLLMEngine.from_engine_args(AsyncEngineArgs(**cfg),stat_loggers=[lambda *args:Logger()])
  histories={c:[dict(role='system',content='Read the supplied records. Return only a JSON object mapping each requested key to its exact six-digit value as a string. Do not add explanation.')] for c in range(4)}
  with (a.out/'requests.jsonl').open('w',buffering=1) as log:
   for turn in range(3):
    for task in tasks:
     client=task['client'];keys=task['groups'][turn];query=('Records:\n'+task['document']+'\n\n' if turn==0 else 'Using the original records, ')+ 'Return values for these keys: '+', '.join(keys)
     history=histories[client];history.append(dict(role='user',content=query));ids=tok.apply_chat_template(history,tokenize=True,return_dict=False,add_generation_prompt=True,enable_thinking=False)
     assert len(ids)+128<=8192
     rid=f'c{client}-t{turn}';state['request']=rid;start=time.monotonic();events=[];final=None
     async for item in engine.generate({'prompt_token_ids':ids},SamplingParams(temperature=0,max_tokens=128),rid):final=item;events.append([time.monotonic(),len(item.outputs[0].token_ids)])
     seq=final.outputs[0];assert final.prompt_token_ids==ids and tok.decode(seq.token_ids,skip_special_tokens=True)==seq.text
     row=dict(id=rid,client=client,turn=turn,messages=list(history),prompt_ids=ids,output_ids=list(seq.token_ids),text=seq.text,expected={k:task['values'][k] for k in keys},finish_reason=seq.finish_reason,cached_tokens=final.num_cached_tokens,metrics=asdict(final.metrics),start=start,end=time.monotonic(),events=events)
     log.write(json.dumps(row)+'\n');history.append(dict(role='assistant',content=seq.text));print(rid,row['cached_tokens'],len(seq.token_ids),flush=True)
  (a.out/'completion.json').write_text(json.dumps(dict(requests=12,done=True))+'\n')
 finally:
  if engine is not None:engine.shutdown()
  stats.close()
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--model',required=True);p.add_argument('--apc',action='store_true');asyncio.run(main(p.parse_args()))
