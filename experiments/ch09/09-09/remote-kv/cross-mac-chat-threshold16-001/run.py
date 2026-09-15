import argparse,hashlib,json,os,time,urllib.request
from pathlib import Path
from store import pack,unpack
R=Path(__file__).resolve().parent
URL='http://127.0.0.1:18797'
def rpc(op,meta):
 with urllib.request.urlopen(urllib.request.Request(URL+'/'+op,data=pack(meta)),timeout=120) as f:return unpack(f.read())[0]
def main(a):
 a.output.mkdir(parents=True,exist_ok=False)
 os.environ.update(BOOK_REMOTE_KV_TRACE=str(a.output/'remote.jsonl'),BOOK_UNUSED_LOCAL_CACHE=str(a.output/'unused-local'),BOOK_REMOTE_KV_URL=URL)
 import sglang as sgl
 from sglang.srt.mem_cache.radix_cache import RadixKey
 kind,phase=a.phase.split('-');config=json.loads((R/'config.json').read_text())
 inputs=[x for x in json.loads((R/'inputs.json').read_text())['requests'] if x['kind']==kind]
 suffix='_'+config['model_path'].replace('/','-')+'_0_1'
 result=dict(phase=a.phase,status='running',config=config,source_hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['run.py','store.py','remote_backend.py','inputs.json','config.json','PROTOCOL.md']});records=[];engine=None
 try:
  start=time.monotonic();engine=sgl.Engine(**config);result['startup_s']=time.monotonic()-start
  for item in inputs:
   ids=item['input_ids'];keys=[];prev=None;native=RadixKey(ids)
   for offset in range(0,((len(ids)-1)//16)*16,16):
    prev=native.hash_page(offset,offset+16,prev);keys.append(prev+suffix)
   before=rpc('exists',dict(keys=keys));start=time.monotonic()
   response=engine.generate(input_ids=ids,sampling_params=dict(temperature=0,max_new_tokens=1,ignore_eos=True))
   row=dict(kind=kind,turn=item['turn'],input_tokens=len(ids),start_s=start,end_s=time.monotonic(),response=response,expected_reusable_keys=keys,store_exists_before=before)
   records.append(row)
   with (a.output/'requests.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
   deadline=time.monotonic()+1800;observations=[]
   while True:
    present=rpc('exists',dict(keys=keys));observations.append(dict(time_s=time.monotonic(),present=sum(present['exists']),expected=len(keys)))
    t=a.output/'remote.jsonl';trace=[json.loads(l) for l in t.read_text().splitlines()] if t.exists() else []
    if any(x['error'] is not None for x in trace):raise RuntimeError('remote transport error')
    if all(present['exists']):break
    if time.monotonic()>deadline:raise TimeoutError('native prefix publication')
    time.sleep(2)
   with (a.output/'barriers.jsonl').open('a') as f:f.write(json.dumps(dict(turn=item['turn'],observations=observations))+'\n')
   print(kind,phase,item['turn'],'returned and published',flush=True)
  result['server_info']=engine.get_server_info();result['status']='all_requests_returned'
 finally:
  if engine is not None:engine.shutdown()
  result['requests']=records;(a.output/'raw.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--phase',required=True);main(p.parse_args())
