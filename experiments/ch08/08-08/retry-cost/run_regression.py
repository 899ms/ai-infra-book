import argparse,asyncio,hashlib,json,os,random,time
from dataclasses import asdict
from pathlib import Path
from fixture import fixture

def exact(text,expected):
 def unique(pairs):
  d={}
  for k,v in pairs:
   if k in d:raise ValueError('Duplicate JSON key')
   d[k]=v
  return d
 try:return json.loads(text,object_pairs_hook=unique)==expected
 except (ValueError,TypeError):return False

async def main(a):
 os.environ['VLLM_USE_FLASHINFER_SAMPLER']='0';os.environ['HF_HUB_OFFLINE']='1';os.environ['TRANSFORMERS_OFFLINE']='1'
 assert not a.output.exists();a.output.mkdir(parents=True)
 import torch,vllm
 from transformers import AutoTokenizer
 from vllm import AsyncEngineArgs,AsyncLLMEngine,SamplingParams
 tok=AutoTokenizer.from_pretrained(a.model,local_files_only=True)
 tasks=[fixture(tok,512,808512+i,f'known-{i:02d}') for i in range(4)]
 calibration=fixture(tok,512,999808,'calibration');warm=fixture(tok,512,8808999,'warm')
 rng=random.Random(808);orders=[]
 for i in range(2):
  order=list(range(4));rng.shuffle(order);orders.append(order)
 inputs=dict(tasks=tasks,calibration=calibration,warm=warm,orders=orders)
 (a.output/'inputs.json').write_text(json.dumps(inputs)+'\n')
 cfg=dict(model=a.model,dtype='bfloat16',quantization='fp8',kv_cache_dtype='fp8_e4m3',calculate_kv_scales=False,
  max_model_len=16384,max_num_seqs=4,max_num_batched_tokens=16384,enable_chunked_prefill=True,
  enable_prefix_caching=False,enforce_eager=True,async_scheduling=False,gpu_memory_utilization=.30,
  kv_cache_memory_bytes=8*1024**3,seed=808,attention_backend='TRITON_ATTN',worker_extension_cls='switch_probe.SwitchProbe')
 root=Path(__file__).absolute().parent
 env=dict(config=cfg,torch=torch.__version__,vllm=vllm.__version__,hashes={n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ['run_regression.py','fixture.py','probe.py','switch_probe.py']},input_sha256=hashlib.sha256((a.output/'inputs.json').read_bytes()).hexdigest(),policy='Previously observed four regression documents, not heldout quality examples. Known-answer synthetic exact checker; one FP8-Q attempt then at most one BF16-Q retry on incorrect answer; no retries after second failure.')
 (a.output/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
 engine=AsyncLLMEngine.from_engine_args(AsyncEngineArgs(**cfg));snap={}
 attempts=(a.output/'attempts.jsonl').open('w',buffering=1);outcomes=(a.output/'tasks.jsonl').open('w',buffering=1)
 async def attempt(task,rid,mode):
  begin=time.monotonic();final=None;events=[]
  async for out in engine.generate({'prompt_token_ids':task['prompt_token_ids']},SamplingParams(temperature=0,max_tokens=128),rid):
   events.append([time.monotonic(),len(out.outputs[0].token_ids)]);final=out
  end=time.monotonic();seq=final.outputs[0]
  check_begin=time.monotonic();correct=exact(seq.text,task['expected']);check_end=time.monotonic()
  observation=await engine.collective_rpc('query_observation') if mode!='calibration' else None
  row=dict(id=rid,task_id=task['id'],mode=mode,start_s=begin,end_s=end,events=events,output_ids=list(seq.token_ids),text=seq.text,
   finish_reason=seq.finish_reason,stop_reason=seq.stop_reason,metrics=asdict(final.metrics),correct=correct,check_begin_s=check_begin,check_end_s=check_end,q_observation=observation)
  attempts.write(json.dumps(row)+'\n');return row
 try:
  snap['weights']=await engine.collective_rpc('weight_snapshot');snap['armed']=await engine.collective_rpc('arm_kv_calibration')
  await attempt(calibration,'calibration','calibration');snap['calibrated']=await engine.collective_rpc('kv_snapshot')
  snap['observed_layers']=await engine.collective_rpc('observe_query')
  for mode,flag in [('fp8',True),('bf16',False)]:
   assert await engine.collective_rpc('set_query_mode',args=(flag,))==[36]
   await attempt(warm,'warm-'+mode,mode)
  for trial,order in enumerate(orders):
   for i in order:
    task=tasks[i];rid=f'{trial}-{task["id"]}';start=time.monotonic()
    assert await engine.collective_rpc('set_query_mode',args=(True,))==[36]
    first=await attempt(task,rid+'-first','fp8');used=[first]
    if not first['correct']:
     assert await engine.collective_rpc('set_query_mode',args=(False,))==[36]
     used.append(await attempt(task,rid+'-retry','bf16'))
    end=time.monotonic()
    outcomes.write(json.dumps(dict(id=rid,task_id=task['id'],trial=trial,start_s=start,end_s=end,attempt_ids=[x['id'] for x in used],first_correct=first['correct'],final_correct=used[-1]['correct']))+'\n')
    print(rid,'attempts',len(used),'final',used[-1]['correct'],flush=True)
  snap['after']=await engine.collective_rpc('kv_snapshot')
 finally:
  (a.output/'snapshots.json').write_text(json.dumps(snap,indent=2)+'\n');engine.shutdown();attempts.close();outcomes.close()

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--output',type=Path,required=True);asyncio.run(main(p.parse_args()))
