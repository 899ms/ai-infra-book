import concurrent.futures,hashlib,json,random,sqlite3,subprocess,time
from pathlib import Path
from mac_runner import run_case
R=Path(__file__).resolve().parent;O=R/'results';O.mkdir(exist_ok=False)
remote='/home/ubuntu/ai-infra-book-experiments/ch11/11-04/additional-device';meta=json.loads((R/'model-identity.json').read_text());tasks=json.loads((R/'tasks.json').read_text())['formal'];start=time.monotonic();rows=[]
def mac(root,task):
 job=dict(request_id=root.name,task=task,cut=32,strategy='baseline',max_tokens=768,model_revision=meta['revision'])
 run_case(root,job,start)
def rtx(root,name):
 root.mkdir();begin=time.monotonic()
 with (root/'ssh.log').open('x') as log:rc=subprocess.run(['ssh','-o','BatchMode=yes','rtx-pro',f'cd {remote} && python3 -u rtx_launch.py --name {name}'],stdout=log,stderr=subprocess.STDOUT).returncode
 ended=time.monotonic();assert rc==0
 for source,dest in [(name+'/',str(root/'worker')+'/'),(name+'-execution.json',str(root/'execution.json')),(name+'-worker.log',str(root/'worker.log')),(name+'-gpu.jsonl',str(root/'gpu.jsonl'))]:subprocess.run(['rsync','-a',f'rtx-pro:{remote}/{source}',dest],check=True)
 value=json.loads((root/'worker/raw.json').read_text());assert value['status']=='complete'
 conn=sqlite3.connect(root/'manager-receipt.sqlite');conn.execute('PRAGMA synchronous=FULL');conn.execute('create table tokens(seq integer primary key,token integer not null)');conn.executemany('insert into tokens values (?,?)',enumerate(value['token_ids']));conn.commit();committed=time.monotonic();conn.close()
 row=dict(start_s=begin,remote_command_returned_s=ended,manager_committed_s=committed,received_tokens=len(value['token_ids']),ssh_exit=rc);(root/'receipt.json').write_text(json.dumps(row,indent=2)+'\n');return row
rng=random.Random(1105)
try:
 for rep in range(3):
  order=['fixed','additional'];rng.shuffle(order)
  for policy in order:
   root=O/f'rep{rep}-{policy}';root.mkdir();begin=time.monotonic()
   if policy=='fixed':
    for task in tasks:mac(root/task['id'],task)
   else:
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
     f=pool.submit(mac,root/'sequence',next(t for t in tasks if t['id']=='sequence'));g=pool.submit(rtx,root/'extract',f'rep{rep}-additional');f.result();g.result()
   row=dict(rep=rep,policy=policy,start_s=begin,end_s=time.monotonic());rows.append(row)
   with (O/'batches.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
   print(row,flush=True)
finally:
 (O/'execution.json').write_text(json.dumps(dict(rows=rows,start_s=start,end_s=time.monotonic(),source_sha256={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['run.py','mac_runner.py','worker.py','rtx_generate.py','rtx_launch.py','rtx-input.json','tasks.json','model-identity.json','PROTOCOL.md']}),indent=2)+'\n')
