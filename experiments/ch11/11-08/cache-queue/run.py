import asyncio,hashlib,json,os,random,time
from dataclasses import asdict
from pathlib import Path
from fixture import INITIAL,SPEC,CHECKER,execute
R=Path(__file__).resolve().parent;O=R/'results'
M='/home/ubuntu/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218'
async def main():
 O.mkdir(exist_ok=False);os.environ['VLLM_USE_FLASHINFER_SAMPLER']='0'
 import torch,vllm
 from transformers import AutoTokenizer
 from vllm import AsyncEngineArgs,AsyncLLMEngine,SamplingParams
 tok=AutoTokenizer.from_pretrained(M,local_files_only=True);close=tok.convert_tokens_to_ids('</think>')
 config=dict(model=M,dtype='bfloat16',max_model_len=8192,max_num_seqs=1,max_num_batched_tokens=512,enable_chunked_prefill=True,enable_prefix_caching=True,enforce_eager=True,gpu_memory_utilization=.30,kv_cache_memory_bytes=6*1024**3,seed=1108,async_scheduling=False)
 (O/'environment.json').write_text(json.dumps(dict(config=config,torch=torch.__version__,vllm=vllm.__version__,thinking_close_token=close,source_hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['run.py','fixture.py','PROTOCOL.md']}),indent=2)+'\n')
 order=[];rng=random.Random(1107)
 for rep in range(2):
  cases=[dict(rep=rep,thinking=think,budget=cap,warm=warm,busy=busy) for think,cap in [(True,100),(True,1000),(True,4096),(False,1000)] for warm in [False,True] for busy in [False,True]];rng.shuffle(cases);order.extend(cases)
 (O/'order.json').write_text(json.dumps(order,indent=2)+'\n');engine=AsyncLLMEngine.from_engine_args(AsyncEngineArgs(**config))
 async def generate(ids,params,rid,ready=None):
  start=time.monotonic();events=[];last=None
  async for value in engine.generate({'prompt_token_ids':ids},params,rid):
   now=time.monotonic();events.append(dict(time_s=now,token_count=len(value.outputs[0].token_ids)));last=value
   if ready is not None and value.outputs[0].token_ids:ready.set()
  out=last.outputs[0]
  return dict(start_s=start,end_s=time.monotonic(),input_ids=ids,output_ids=list(out.token_ids),text=out.text,finish_reason=out.finish_reason,cached_tokens=last.num_cached_tokens,metrics=asdict(last.metrics) if last.metrics else None,events=events)
 try:
  for i,c in enumerate(order):
   assert await engine.reset_prefix_cache()
   work=O/f'case{i}';work.mkdir()
   for n,t in [('intervals.py',INITIAL),('SPEC.txt',SPEC),('test_intervals.py',CHECKER)]: (work/n).write_text(t)
   messages=[dict(role='system',content='Repair the function. Return exactly one JSON object with a single content field containing the complete Python code. No imports. No markdown.'),dict(role='user',content=SPEC+'\nCurrent implementation:\n'+INITIAL)]
   ids=tok.apply_chat_template(messages,tokenize=True,return_dict=False,add_generation_prompt=True,enable_thinking=c['thinking']);warmup=None;bg=None;bg_task=None
   if c['warm']:warmup=await generate(ids,SamplingParams(temperature=0,max_tokens=1,ignore_eos=True),f'warm-{i}')
   if c['busy']:
    bgids=tok.encode('Write a long list of historical inventions and explanations.');ready=asyncio.Event();bg_task=asyncio.create_task(generate(bgids,SamplingParams(temperature=0,max_tokens=128,ignore_eos=True),f'background-{i}',ready));await asyncio.wait_for(ready.wait(),30);assert not bg_task.done()
   target=await generate(ids,SamplingParams(temperature=0,max_tokens=c['budget']),f'target-{i}')
   if bg_task:bg=await bg_task
   answer=target['text'].split('</think>',1)[1] if c['thinking'] and '</think>' in target['text'] else '' if c['thinking'] else target['text'];validation_start=time.monotonic()
   try:
    proposal=json.loads(answer.strip());assert set(proposal)=={'content'};write=execute(dict(tool='write_file',path='intervals.py',content=proposal['content']),work);check=execute(dict(tool='run_tests'),work);result=dict(write=write,validation=check,passed=check['returncode']==0 and json.loads(check['stdout'])['passed'])
   except Exception as e:result=dict(passed=False,error=repr(e))
   done=time.monotonic();position=target['output_ids'].index(close) if c['thinking'] and close in target['output_ids'] else None
   first_answer=next((e['time_s'] for e in target['events'] if e['token_count']>(position+1 if position is not None else 0)),None) if not c['thinking'] or position is not None else None
   row=dict(index=i,**c,target=target,warmup=warmup,background=bg,reasoning_tokens_before_close=position if position is not None else len(target['output_ids']) if c['thinking'] else 0,thinking_closed=position is not None,first_answer_segment_s=first_answer,validation_start_s=validation_start,done_s=done,verified_usable_s=done-target['start_s'] if result['passed'] else None,result=result)
   (work/'record.json').write_text(json.dumps(row,indent=2)+'\n')
   with (O/'raw.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
   print(i,c,'tokens',len(target['output_ids']),'cached',target['cached_tokens'],'passed',result['passed'],flush=True)
 finally:engine.shutdown()
if __name__=='__main__':asyncio.run(main())
