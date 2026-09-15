"""Generate two actual candidate batches; execution occurs separately in Docker."""
import asyncio,hashlib,json,os,time
from pathlib import Path
P=Path(__file__).resolve().parent
MODEL='/home/ubuntu/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218'
async def main():
 os.environ['VLLM_USE_FLASHINFER_SAMPLER']='0'
 import torch,vllm
 from transformers import AutoTokenizer
 from vllm import AsyncEngineArgs,AsyncLLMEngine,SamplingParams
 out=P/'generation';out.mkdir(exist_ok=False)
 config=dict(model=MODEL,dtype='bfloat16',max_model_len=4096,max_num_seqs=6,max_num_batched_tokens=1024,enable_chunked_prefill=True,enable_prefix_caching=False,enforce_eager=True,gpu_memory_utilization=.5,kv_cache_memory_bytes=4*1024**3,seed=1106,async_scheduling=False)
 (out/'environment.json').write_text(json.dumps(dict(config=config,torch=torch.__version__,vllm=vllm.__version__,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
 tokenizer=AutoTokenizer.from_pretrained(MODEL,local_files_only=True);engine=AsyncLLMEngine.from_engine_args(AsyncEngineArgs(**config))
 specs={'B':'Write solve(n) returning Fibonacci F(n), F(0)=0,F(1)=1, for nonnegative integer n. Use direct recursion solve(n-1)+solve(n-2), no memoization, no imports.','A':'Write solve(n) returning the sum of i*i for integers 0 <= i < n. Use a Python for loop, no closed-form formula, no imports.'}
 origin=time.monotonic();(out/'origin.json').write_text(json.dumps(dict(start_s=origin))+'\n')
 async def one(batch,i):
  messages=[dict(role='system',content='Return exactly one JSON object with key content whose value is the complete Python source defining solve. No markdown.'),dict(role='user',content=specs[batch])]
  ids=tokenizer.apply_chat_template(messages,tokenize=True,return_dict=False,add_generation_prompt=True,enable_thinking=False)
  start=time.monotonic();events=[]
  async for r in engine.generate({'prompt_token_ids':ids},SamplingParams(temperature=.6,seed=11060+i+(0 if batch=='B' else 3),max_tokens=512),f'{batch}{i}'):
   events.append(dict(at_s=time.monotonic(),tokens=len(r.outputs[0].token_ids)))
  end=time.monotonic();o=r.outputs[0]
  row=dict(id=f'{batch}{i}',batch=batch,index=i,messages=messages,input_ids=ids,output_ids=list(o.token_ids),text=o.text,finish_reason=o.finish_reason,start_s=start,ready_s=end,arrival_s=end-origin,events=events)
  try:row['code']=json.loads(o.text)['content'];row['parse_error']=None
  except Exception as e:row['code']=None;row['parse_error']=repr(e)
  (out/f'{batch}{i}.json').write_text(json.dumps(row,indent=2)+'\n');print(row['id'],len(o.token_ids),row['arrival_s'],row['parse_error'],flush=True)
 try:
  await asyncio.gather(*(one('B',i) for i in range(3)))
  await asyncio.gather(*(one('A',i) for i in range(3)))
 finally:engine.shutdown()
if __name__=='__main__':asyncio.run(main())
