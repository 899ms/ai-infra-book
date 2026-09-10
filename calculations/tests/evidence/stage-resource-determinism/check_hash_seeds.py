import subprocess,sys,os,json,hashlib
from pathlib import Path
root=Path.cwd()/'calculations'
code='''import json
from infra_calc.paths import PROJECT
from infra_calc.topics import stage_resource_bounds as m
rows=json.loads((PROJECT/'scenarios/book.json').read_text())['stage_resource_bounds']
output={}
for row in rows:
 result=m.calculate(**{k:v for k,v in row.items() if k!='id'})
 output[row['id']]={'result':result,'markdown':m.markdown(result)}
print(json.dumps(output,ensure_ascii=False))
'''
outputs=[]
for seed in ('1','2'):
 env=dict(os.environ,PYTHONHASHSEED=seed,PYTHONPATH=str(root/'src'))
 outputs.append(subprocess.check_output([sys.executable,'-c',code],env=env))
a,b=map(json.loads,outputs)
changed=[k for k in a if a[k]!=b[k]]
raw_changed=[k for k in a if json.dumps(a[k])!=json.dumps(b[k])]
math_equal=all(a[k]['result']==b[k]['result'] for k in a)
paths=[]
def orderdiff(x,y,path=''):
 if isinstance(x,dict):
  if list(x)!=list(y): paths.append(path)
  for k in x: orderdiff(x[k],y[k],path+'.'+k)
 elif isinstance(x,list):
  for i,(u,v) in enumerate(zip(x,y)):orderdiff(u,v,path+f'[{i}]')
for k in a:orderdiff(a[k]['result'],b[k]['result'],k)
result={'topic_sha256':hashlib.sha256((root/'src/infra_calc/topics/stage_resource_bounds.py').read_bytes()).hexdigest(),'seeds':[1,2],'scenarios':len(a),'whole_outputs_equal':outputs[0]==outputs[1],'result_values_equal':math_equal,'changed_json_serializations':raw_changed,'changed_parsed_records_including_markdown':changed,'different_mapping_order_paths':paths,'output_sha256':[hashlib.sha256(x).hexdigest() for x in outputs]}
Path('/tmp/stage-seed-'+sys.argv[1]+'.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
