import argparse,hashlib,json,time,random
from pathlib import Path
R=Path(__file__).resolve().parent

def main(a):
 a.output.mkdir(parents=True,exist_ok=False)
 import sglang as sgl
 config=json.loads((R/'config.json').read_text());inputs=json.loads((R/'inputs.json').read_text())['requests'];engine=None;records=[]
 result=dict(status='running',config=config,source_hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['run.py','config.json','inputs.json','PROTOCOL.md']})
 try:
  start=time.monotonic();engine=sgl.Engine(**config);result['startup_s']=time.monotonic()-start
  rng=random.Random(909)
  for rep in range(3):
   order=inputs.copy();rng.shuffle(order)
   for item in order:
    start=time.monotonic();response=engine.generate(input_ids=item['input_ids'],sampling_params=dict(temperature=0,max_new_tokens=1,ignore_eos=True))
    row=dict(rep=rep,kind=item['kind'],turn=item['turn'],input_tokens=len(item['input_ids']),start_s=start,end_s=time.monotonic(),response=response);records.append(row)
    with (a.output/'requests.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    print(rep,item['kind'],item['turn'],'returned',flush=True)
  result['server_info']=engine.get_server_info();result['status']='all_requests_returned'
 finally:
  if engine is not None:engine.shutdown()
  result['requests']=records;(a.output/'raw.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--phase',required=True);main(p.parse_args())
