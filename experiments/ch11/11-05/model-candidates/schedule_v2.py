import asyncio,json,hashlib,random,time,uuid,platform
from pathlib import Path
P=Path(__file__).resolve().parent;O=P/'validation-v2'
async def main():
 O.mkdir(exist_ok=False);runid='book1106-'+uuid.uuid4().hex[:10];owned=set();commands=[]
 async def command(*args):
  t=time.monotonic();p=await asyncio.create_subprocess_exec(*args,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
  stdout,stderr=await asyncio.wait_for(p.communicate(),30)
  row=dict(args=args,start_s=t,end_s=time.monotonic(),rc=p.returncode,stdout=stdout.decode(),stderr=stderr.decode());commands.append(row)
  with (O/'commands.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  if p.returncode:raise RuntimeError(row)
  return row
 base=(await command('docker','image','inspect','python:3.11-slim','--format','{{.Id}}'))['stdout'].strip()
 tasks=[]
 for f in sorted((P/'generation').glob('[AB]*.json')):
  r=json.loads(f.read_text());assert r['code'] and not r['parse_error'];n=(40 if r['index']==2 else 35) if r['batch']=='B' else 2000000
  tasks.append(dict(id=r['id'],batch=r['batch'],arrival_s=r['arrival_s'],code=r['code'],test_n=n,source_sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 rng=random.Random(1106);order=[]
 for trial in range(3):
  policies=['fixed_quota','fifo','batch_A_first'];rng.shuffle(policies);order.extend(dict(trial=trial,policy=p) for p in policies)
 (O/'protocol.json').write_text(json.dumps(dict(runid=runid,base_image=base,tasks=tasks,order=order,execution_deadline_s=2,slots=2,platform=platform.platform(),source_sha256={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in ['schedule_v2.py','validate_worker.py']}),indent=2)+'\n')
 try:
  for case in order:
   folder=O/f"{case['trial']}-{case['policy']}";folder.mkdir();start=time.monotonic();pending=list(tasks);running={};rows=[];decisions=[]
   async def launch(job):
    dispatch=time.monotonic();work=folder/job['id'];work.mkdir();(work/'job.json').write_text(json.dumps(job)+'\n')
    cid=(await command('docker','create','--label','book.experiment='+runid,'--network','none','--cpus','1','--memory','128m','--memory-swap','128m','--pids-limit','32','--cap-drop','ALL','--security-opt','no-new-privileges','--user','65534:65534',base,'python','-u','/tmp/worker.py'))['stdout'].strip();owned.add(cid)
    await command('docker','cp',str(work/'job.json'),cid+':/tmp/job.json');await command('docker','cp',str(P/'validate_worker.py'),cid+':/tmp/worker.py')
    ready=time.monotonic();proc=await asyncio.create_subprocess_exec('docker','start','-a',cid,stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE);events=[];feedback=None
    while True:
     line=await asyncio.wait_for(proc.stdout.readline(),15)
     if not line:break
     event=json.loads(line);event['host_received_s']=time.monotonic();events.append(event)
     if event['event']=='feedback':feedback=event['host_received_s']
    await asyncio.wait_for(proc.wait(),15);stderr=(await proc.stderr.read()).decode();exit_observed=time.monotonic();assert proc.returncode==0 and feedback is not None,(stderr,events)
    state=json.loads((await command('docker','inspect','--format','{{json .State}}',cid))['stdout']);assert not state['Running'] and state['ExitCode']==0
    await command('docker','rm',cid);owned.remove(cid);release=time.monotonic()
    row=dict(id=job['id'],batch=job['batch'],arrival_s=job['arrival_s'],test_n=job['test_n'],cid=cid,dispatch_s=dispatch,container_ready_s=ready,feedback_s=feedback,exit_observed_s=exit_observed,release_s=release,events=events,stderr=stderr,state=state)
    (work/'result.json').write_text(json.dumps(row,indent=2)+'\n');return row
   while pending or running:
    now=time.monotonic();eligible=[j for j in pending if start+j['arrival_s']<=now]
    if case['policy']=='fixed_quota':eligible=[j for j in eligible if j['batch'] not in {v['batch'] for v in running.values()}]
    if eligible and len(running)<2:
     key=(lambda j:(j['batch']!='A',j['arrival_s'],j['id'])) if case['policy']=='batch_A_first' else (lambda j:(j['arrival_s'],j['id']))
     job=min(eligible,key=key);decisions.append(dict(at_s=now,eligible=[j['id'] for j in eligible],running=[j['id'] for j in running.values()],chosen=job['id']));pending.remove(job);running[asyncio.create_task(launch(job))]=job;continue
    if running:
     future=[start+j['arrival_s']-time.monotonic() for j in pending if start+j['arrival_s']>time.monotonic()]
     done,_=await asyncio.wait(running,timeout=min(future) if future else None,return_when=asyncio.FIRST_COMPLETED)
     for t in done:rows.append(await t);del running[t]
    elif pending:await asyncio.sleep(max(0,min(start+j['arrival_s'] for j in pending)-time.monotonic()))
   record=dict(**case,start_s=start,end_s=time.monotonic(),tasks=rows,decisions=decisions)
   with (O/'raw.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
   print(case,[(r['id'],r['events'][-1]['status']) for r in rows],flush=True)
 finally:
  for cid in list(owned):await command('docker','rm','-f',cid);owned.remove(cid)
  remaining=(await command('docker','ps','-aq','--filter','label=book.experiment='+runid))['stdout'].split();assert not remaining
  (O/'cleanup.json').write_text(json.dumps(dict(runid=runid,remaining=remaining))+'\n')
if __name__=='__main__':asyncio.run(main())
