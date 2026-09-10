import argparse,asyncio,hashlib,json,os,random,time
from dataclasses import asdict,is_dataclass
from pathlib import Path

def fixture(tok,rows,seed,index):
    rng=random.Random(seed)
    values=[str(rng.randrange(100000,1000000)) for _ in range(rows)]
    document='\n'.join(f'k{i:04d} = {v}' for i,v in enumerate(values))
    targets=[rows//8,rows//2,rows-rows//8-1]
    expected={f'k{i:04d}':values[i] for i in targets}
    messages=[dict(role='system',content='Read the supplied records. Return only a JSON object mapping each requested key to its exact six-digit value as a string. Do not add explanation.'),
        dict(role='user',content=f'Records:\n{document}\n\nReturn values for these keys: '+', '.join(expected))]
    ids=tok.apply_chat_template(messages,tokenize=True,return_dict=False,add_generation_prompt=True,enable_thinking=False)
    return dict(id=index,rows=rows,seed=seed,messages=messages,prompt_token_ids=ids,expected=expected)

async def main(args):
    os.environ['VLLM_USE_FLASHINFER_SAMPLER']='0'
    os.environ['HF_HUB_OFFLINE']='1'
    os.environ['TRANSFORMERS_OFFLINE']='1'
    if args.output.exists():raise RuntimeError('Use a fresh output directory')
    args.output.mkdir(parents=True)
    import torch,vllm
    from transformers import AutoTokenizer
    from vllm import AsyncEngineArgs,AsyncLLMEngine,SamplingParams
    tok=AutoTokenizer.from_pretrained(args.model,local_files_only=True)
    tasks=[fixture(tok,n,808000+n+i,f'n{n}-r{i}') for n in [128,512] for i in range(4)]
    calibration=fixture(tok,512,999808,'calibration')
    (args.output/'inputs.json').write_text(json.dumps(dict(tasks=tasks,calibration=calibration))+'\n')
    config=dict(model=args.model,dtype='bfloat16',quantization='fp8',kv_cache_dtype=args.kv_dtype,
        calculate_kv_scales=False,max_model_len=16384,max_num_seqs=24,max_num_batched_tokens=16384,
        enable_chunked_prefill=True,enable_prefix_caching=False,enforce_eager=True,async_scheduling=False,
        gpu_memory_utilization=.30,kv_cache_memory_bytes=8*1024**3,seed=808,disable_log_stats=False,
        attention_backend='TRITON_ATTN',worker_extension_cls='probe.KVProbe')
    env=dict(config=config,torch=torch.__version__,vllm=vllm.__version__,
        hashes={n:hashlib.sha256((Path(__file__).parent/n).read_bytes()).hexdigest() for n in ['run.py','probe.py']},
        input_sha256=hashlib.sha256((args.output/'inputs.json').read_bytes()).hexdigest(),
        scope='Online FP8 weights held fixed; same original BF16 checkpoint. Explicit independent calibration before warmups; first attention call computes scales once. Synthetic exact retrieval quality, not general task quality.')
    (args.output/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
    from vllm.v1.metrics.loggers import StatLoggerBase
    stats_file=(args.output/'engine-stats.jsonl').open('w',buffering=1)
    active_batch=None
    def serialize(value):
        if is_dataclass(value):return asdict(value)
        if hasattr(value,'__dict__'):return vars(value)
        return str(value)
    class RawStats(StatLoggerBase):
        def __init__(self,vllm_config,engine_index=0):pass
        def log_engine_initialized(self):pass
        def record(self,scheduler_stats,iteration_stats,mm_cache_stats=None,engine_idx=0):
            stats_file.write(json.dumps(dict(observed_monotonic_s=time.monotonic(),batch=active_batch,
                scheduler=scheduler_stats,iteration=iteration_stats),default=serialize)+'\n')
    engine=AsyncLLMEngine.from_engine_args(AsyncEngineArgs(**config),stat_loggers=[lambda cfg,idx:RawStats(cfg,idx)])
    requests=(args.output/'requests.jsonl').open('w',buffering=1)
    batches=(args.output/'batches.jsonl').open('w',buffering=1)
    snapshots={}
    async def one(task,rid,mode):
        start=time.monotonic();events=[];final=None
        async for out in engine.generate({'prompt_token_ids':task['prompt_token_ids']},
                SamplingParams(temperature=0,max_tokens=64 if mode=='fixed' else 128,ignore_eos=mode=='fixed'),rid):
            events.append([time.monotonic(),len(out.outputs[0].token_ids)]);final=out
        seq=final.outputs[0]
        row=dict(id=rid,task_id=task['id'],mode=mode,start_s=start,end_s=time.monotonic(),events=events,
            output_ids=list(seq.token_ids),text=seq.text,finish_reason=seq.finish_reason,stop_reason=seq.stop_reason,metrics=asdict(final.metrics))
        requests.write(json.dumps(row)+'\n');return row
    async def batch(concurrency,mode,trial):
        nonlocal active_batch
        selected=[t for t in tasks if t['rows']==512]
        rid=f'{trial}-b{concurrency}-{mode}';active_batch=rid;start=time.monotonic()
        await asyncio.gather(*(one(selected[i%4],f'{rid}-r{i}',mode) for i in range(concurrency)))
        batches.write(json.dumps(dict(id=rid,concurrency=concurrency,mode=mode,trial=trial,start_s=start,end_s=time.monotonic()))+'\n')
        active_batch=None
        await asyncio.sleep(.1)
        print(rid,'done',flush=True)
    try:
        snapshots['weights']=await engine.collective_rpc('weight_snapshot')
        snapshots['before']=await engine.collective_rpc('kv_snapshot')
        if args.kv_dtype!='auto':snapshots['armed_layers']=await engine.collective_rpc('arm_kv_calibration')
        await one(calibration,'calibration','natural')
        snapshots['after_calibration']=await engine.collective_rpc('kv_snapshot')
        await batch(4,'natural','warm')
        conditions=[(b,m) for b in [7,8,15,16,20] for m in ['natural','fixed']]
        rng=random.Random(808)
        for trial in range(2):
            order=conditions.copy();rng.shuffle(order)
            for b,m in order:await batch(b,m,trial)
        snapshots['after']=await engine.collective_rpc('kv_snapshot')
    finally:
        (args.output/'kv-snapshots.json').write_text(json.dumps(snapshots,indent=2)+'\n')
        engine.shutdown();requests.close();batches.close();stats_file.close()

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model',required=True);p.add_argument('--output',type=Path,required=True)
    p.add_argument('--kv-dtype',choices=['auto','fp8_e4m3'],default='auto')
    asyncio.run(main(p.parse_args()))
