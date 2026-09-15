"""Fresh engine remote KV producer/consumer; retains actual outputs before analysis."""
import argparse,hashlib,json,os,time
from pathlib import Path
from store import pack,unpack
import urllib.request
R=Path(__file__).resolve().parent

def main(a):
 a.output.mkdir(parents=True,exist_ok=False)
 os.environ['BOOK_REMOTE_KV_TRACE']=str((a.output/'remote.jsonl').resolve())
 os.environ['BOOK_UNUSED_LOCAL_CACHE']=str((a.output/'unused-local').resolve())
 os.environ['BOOK_REMOTE_KV_URL']='http://127.0.0.1:18799'
 import sglang as sgl
 config=json.loads((R/'config.json').read_text());ids=json.loads((R/'inputs.json').read_text());records=[];engine=None
 result=dict(phase=a.phase,status='running',config=config,source_hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['run.py','store.py','remote_backend.py','inputs.json','config.json','PROTOCOL.md']})
 try:
  start=time.monotonic();engine=sgl.Engine(**config);result['startup_s']=time.monotonic()-start
  for i in range(3):
   start=time.monotonic();response=engine.generate(input_ids=ids,sampling_params=dict(temperature=0,max_new_tokens=16,ignore_eos=True));row=dict(index=i,start_s=start,end_s=time.monotonic(),response=response);records.append(row)
   with (a.output/'requests.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
   print('request',i,'returned',flush=True)
  # Allow write-through worker to finish; record inventory separately.
  time.sleep(5)
  req=urllib.request.Request(os.environ['BOOK_REMOTE_KV_URL']+'/inventory',data=pack({}))
  with urllib.request.urlopen(req,timeout=120) as f:result['remote_inventory']=unpack(f.read())[0]
  result['server_info']=engine.get_server_info();result['status']='all_requests_returned'
 finally:
  if engine is not None:engine.shutdown()
  result['requests']=records;(a.output/'raw.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--phase',required=True);main(p.parse_args())
