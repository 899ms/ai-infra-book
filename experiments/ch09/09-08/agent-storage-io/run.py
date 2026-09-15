import hashlib,json,mmap,os,platform,random,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results';O.mkdir(exist_ok=False);D=O/'written';D.mkdir();spec=json.loads((R/'input-manifest.json').read_text());rows=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
state=dict(status='running',platform=platform.platform(),filesystem=subprocess.check_output(['df','-T',str(R)],text=True),source_sha256={n:sha(R/n) for n in ['run.py','PROTOCOL.md','input-manifest.json','files.txt']},start_unix=time.time())
try:
 assert hasattr(os,'O_DIRECT');names=list(spec['files']);assert len(names)==197
 for name in names:
  e=spec['files'][name];data=(R/'pages'/name).read_bytes();assert len(data)==e['bytes']==2359296 and hashlib.sha256(data).hexdigest()==e['sha256'] and len(data)%4096==0
  with mmap.mmap(-1,len(data)) as buf:
   buf[:]=data;start=time.monotonic();fd=os.open(D/name,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_DIRECT,0o600)
   try:assert os.write(fd,buf)==len(data);os.fsync(fd)
   finally:os.close(fd)
   parent=os.open(D,os.O_RDONLY)
   try:os.fsync(parent)
   finally:os.close(parent)
   end=time.monotonic()
  row=dict(op='direct_write_fsync',name=name,bytes=len(data),start_s=start,end_s=end,sha256=e['sha256']);rows.append(row)
  with (O/'operations.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
 rng=random.Random(908)
 for rep in range(3):
  order=names.copy();rng.shuffle(order)
  for name in order:
   e=spec['files'][name]
   with mmap.mmap(-1,e['bytes']) as buf:
    start=time.monotonic();fd=os.open(D/name,os.O_RDONLY|os.O_DIRECT)
    try:n=os.readv(fd,[buf])
    finally:os.close(fd)
    end=time.monotonic();assert n==e['bytes'];digest=hashlib.sha256(buf).hexdigest();assert digest==e['sha256']
   row=dict(op='direct_read',rep=rep,name=name,bytes=n,start_s=start,end_s=end,sha256=digest);rows.append(row)
   with (O/'operations.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  print('read pass',rep,'verified',flush=True)
 state['status']='all_pages_verified'
finally:
 state.update(end_unix=time.time(),operations=len(rows));(O/'execution.json').write_text(json.dumps(state,indent=2)+'\n')
