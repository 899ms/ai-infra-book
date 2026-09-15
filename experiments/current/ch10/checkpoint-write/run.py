"""Full-size synthetic checkpoint payload write on local filesystem; not model serialization."""
from pathlib import Path
import os,time,json,hashlib,shutil,platform
P=Path(__file__).resolve().parent;out=P/'formal-001';out.mkdir(exist_ok=False)
N=14*8190735360;chunk=os.urandom(64*2**20);target=out/'payload.bin'
assert shutil.disk_usage(P).free>N+20*2**30
start=time.monotonic();fd=os.open(target,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);written=0
try:
 while written<N:
  data=memoryview(chunk)[:min(len(chunk),N-written)]
  while data:
   n=os.write(fd,data);written+=n;data=data[n:]
  if written%(8*2**30)<len(chunk):(out/'progress.json').write_text(json.dumps(dict(bytes=written,total=N,elapsed_s=time.monotonic()-start)))
 write_end=time.monotonic();os.fsync(fd);sync_end=time.monotonic()
finally:os.close(fd)
assert target.stat().st_size==N
samples=[]
with target.open('rb',buffering=0) as f:
 for pos in [0,12345,N//7,N//3,N//2,N-65536]:
  f.seek(pos);b=f.read(65536);offset=pos%len(chunk);expected=(chunk+chunk)[offset:offset+len(b)]
  assert b==expected;samples.append(dict(offset=pos,bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
r=dict(status='completed',bytes=N,write_s=write_end-start,fsync_s=sync_end-write_end,total_write_fsync_s=sync_end-start,effective_GBps=N/(sync_end-start)/1e9,sample_checks=samples,hostname=platform.node(),python=platform.python_version(),source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='One synthetic payload matching14N checkpoint bytes; pre-generated random64MiB chunk repeated, no sparse allocation requested. Local filesystem write+fsync includes writes/loop/open, excludes data generation, model staging, metadata commit and distributed coordination. Six sampled regions verified, not full payload hash.')
(out/'result.json').write_text(json.dumps(r,indent=2)+'\n');target.unlink();(out/'cleanup.json').write_text(json.dumps(dict(generated_payload_removed=not target.exists()))+'\n');print(json.dumps(r))
