import argparse,hashlib,json,os,platform,signal,subprocess,sys,time
from pathlib import Path
B=Path(__file__).absolute().parent
p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);a=p.parse_args();out=a.out.absolute();out.mkdir(exist_ok=False)
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
for n,h in json.loads((B/'provenance.json').read_text()).items():assert hashlib.sha256((B/n).read_bytes()).hexdigest()==h,n
write(out/'environment.json',dict(platform=platform.platform(),python=sys.version,executable=sys.executable,source_sha256={n:hashlib.sha256((B/n).read_bytes()).hexdigest() for n in ['model.py','run_worker.py','launch.py','PROTOCOL.md','provenance.json']},workers=[1,4],seeds=[1061,1062,1063],cuts=[17,41],steps=64))
records=[];resources=[];total=time.monotonic()
for seed in [1061,1062,1063]:
 for cut in [17,41]:
  for workers in [1,4]:
   name=f'seed{seed}-cut{cut}-w{workers}';dest=out/name;cp=B/'reference'/f'seed{seed}-cut{cut}-prefix/checkpoint.pt'
   cmd=[sys.executable,'-B',str(B/'run_worker.py'),'--output',str(dest),'--seed',str(seed),'--workers',str(workers),'--checkpoint',str(cp)]
   env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',VECLIB_MAXIMUM_THREADS='1',MKL_NUM_THREADS='1')
   with (out/(name+'.log')).open('w') as log:
    proc=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT,env=env,start_new_session=True);start=time.monotonic()
    try:
     while proc.poll() is None:
      rows=subprocess.check_output(['ps','-axo','pid=,ppid=,pgid=,rss='],text=True);own=[]
      for line in rows.splitlines():
       pid,ppid,pgid,rss=map(int,line.split())
       if pgid==proc.pid:own.append(dict(pid=pid,ppid=ppid,rss_bytes=rss*1024))
      resources.append(dict(name=name,time=time.monotonic(),rss_bytes=sum(v['rss_bytes'] for v in own),processes=own))
      assert resources[-1]['rss_bytes']<4*1024**3 and time.monotonic()-start<120
      time.sleep(.1)
     code=proc.wait();end=time.monotonic()
    finally:
     if proc.poll() is None:
      assert os.getpgid(proc.pid)==proc.pid;os.killpg(proc.pid,signal.SIGTERM);proc.wait(timeout=15)
    lines=subprocess.check_output(['ps','-axo','pid=,pgid=,stat='],text=True).splitlines();left=[z for z in lines if int(z.split()[1])==proc.pid and not z.split()[2].startswith('Z')]
    row=dict(name=name,seed=seed,cut=cut,workers=workers,pid=proc.pid,start=start,end=end,exit_code=code,leftover=left);records.append(row);write(out/'execution.json',records);write(out/'resources.json',resources)
    assert code==0 and not left,row
    print(name,code,round(end-start,3),flush=True)
write(out/'completion.json',dict(done=True,runs=len(records),wall_s=time.monotonic()-total))
