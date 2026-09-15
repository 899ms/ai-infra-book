import asyncio,base64,hashlib,io,json,os,time
from dataclasses import asdict
from pathlib import Path
R=Path(__file__).resolve().parent; O=R/'server-results'
M='/home/ubuntu/.cache/huggingface/hub/models--Qwen--Qwen3-VL-8B-Instruct/snapshots/0c351dd01ed87e9c1b53cbc748cba10e6187ff3b'
async def main():
 O.mkdir(exist_ok=False); os.environ['VLLM_USE_FLASHINFER_SAMPLER']='0'
 import torch,vllm
 from PIL import Image
 from transformers import AutoProcessor
 from vllm import AsyncEngineArgs,AsyncLLMEngine,SamplingParams
 config=dict(model=M,dtype='bfloat16',max_model_len=8192,max_num_seqs=1,max_num_batched_tokens=8192,enable_prefix_caching=False,enforce_eager=True,gpu_memory_utilization=.65,kv_cache_memory_bytes=4*1024**3,seed=1204,async_scheduling=False)
 processor=AutoProcessor.from_pretrained(M,local_files_only=True)
 (O/'environment.json').write_text(json.dumps(dict(config=config,torch=torch.__version__,vllm=vllm.__version__,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n')
 engine=AsyncLLMEngine.from_engine_args(AsyncEngineArgs(**config)); stop=asyncio.Event();lock=asyncio.Lock()
 async def handle(reader,writer):
  try:
   head=await reader.readuntil(b'\r\n\r\n'); lines=head.decode().split('\r\n');path=lines[0].split()[1]
   if path=='/stop': response={'stopping':True};stop.set()
   elif path=='/health':response={'ready':True}
   else:
    length=int(next(x.split(':',1)[1] for x in lines if x.lower().startswith('content-length:')));assert 0<length<10_000_000
    request=json.loads(await reader.readexactly(length)); png=base64.b64decode(request['image']); picture=Image.open(io.BytesIO(png)).convert('RGB')
    messages=[{'role':'user','content':[{'type':'image'},{'type':'text','text':request['instruction']}]}]
    prompt=processor.apply_chat_template(messages,tokenize=False,add_generation_prompt=True)
    async with lock:
     start=time.monotonic();events=[];last=None
     async for value in engine.generate({'prompt':prompt,'multi_modal_data':{'image':picture}},SamplingParams(temperature=0,max_tokens=request.get('max_tokens',160)),request['id']):
      last=value;events.append({'time_s':time.monotonic(),'token_count':len(value.outputs[0].token_ids)})
     out=last.outputs[0]
     response=dict(id=request['id'],start_s=start,end_s=time.monotonic(),image_sha256=hashlib.sha256(png).hexdigest(),image_size=picture.size,prompt=prompt,prompt_token_ids=last.prompt_token_ids,output_ids=list(out.token_ids),text=out.text,finish_reason=out.finish_reason,metrics=asdict(last.metrics) if last.metrics else None,events=events)
     with (O/'raw.jsonl').open('a') as f:f.write(json.dumps(response)+'\n')
     print(request['id'],out.text,flush=True)
   body=json.dumps(response).encode();writer.write(b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nConnection: close\r\nContent-Length: '+str(len(body)).encode()+b'\r\n\r\n'+body);await writer.drain()
  except Exception as e:
   import traceback;traceback.print_exc();body=json.dumps({'error':repr(e)}).encode();writer.write(b'HTTP/1.1 500 Error\r\nConnection: close\r\nContent-Length: '+str(len(body)).encode()+b'\r\n\r\n'+body);await writer.drain()
  finally:writer.close();await writer.wait_closed()
 server=await asyncio.start_server(handle,'127.0.0.1',19308);(O/'ready.json').write_text(json.dumps({'pid':os.getpid()}));print('READY',flush=True)
 try:
  async with server:await stop.wait()
 finally:engine.shutdown()
if __name__=='__main__':asyncio.run(main())
