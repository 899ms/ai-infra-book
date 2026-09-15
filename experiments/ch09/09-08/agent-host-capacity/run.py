import argparse,hashlib,json,random,time
from pathlib import Path
R=Path(__file__).resolve().parent

def main(a):
 a.output.mkdir(parents=True,exist_ok=False)
 import sglang as sgl
 c=json.loads((R/'config.json').read_text());c['max_total_tokens']=int(a.phase)
 inputs=[x for x in json.loads((R/'inputs.json').read_text())['requests'] if x['kind']=='agent'];rng=random.Random(908);pressure=[[rng.randrange(1000,10000) for _ in range(3584)] for _ in inputs];records=[];engine=None
 result=dict(status='running',config=c,source_hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['run.py','config.json','inputs.json','PROTOCOL.md']})
 try:
  start=time.monotonic();engine=sgl.Engine(**c);result['startup_s']=time.monotonic()-start
  for item,other in zip(inputs,pressure):
   for phase,ids in [('target_before',item['input_ids']),('pressure',other),('target_after',item['input_ids'])]:
    start=time.monotonic();response=engine.generate(input_ids=ids,sampling_params=dict(temperature=0,max_new_tokens=1,ignore_eos=True));row=dict(turn=item['turn'],phase=phase,input_ids=ids,start_s=start,end_s=time.monotonic(),response=response);records.append(row)
    with (a.output/'requests.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
    print(a.phase,item['turn'],phase,response['meta_info'].get('cached_tokens_details'),flush=True)
  result['server_info']=engine.get_server_info();result['status']='all_requests_returned'
 finally:
  if engine is not None:engine.shutdown()
  result['requests']=records;(a.output/'raw.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--phase',required=True);main(p.parse_args())
