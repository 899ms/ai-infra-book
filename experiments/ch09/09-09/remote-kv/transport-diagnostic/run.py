"""Bounded SSH byte-transfer probes, independent of KV/model execution."""
import subprocess,time,json,hashlib,os
from pathlib import Path
P=Path(__file__).resolve().parent;assert not (P/'results.json').exists();rows=[]
for n in [65536,1048576]:
 payload=os.urandom(n);digest=hashlib.sha256(payload).hexdigest()
 for mode in ['default','throughput']:
  args=['ssh','-o','BatchMode=yes','-o','Compression=no','-o','ConnectTimeout=10']
  if mode=='throughput':args+=['-o','IPQoS=throughput','-o','ControlMaster=no','-o','ControlPath=none']
  args+=['rtx-pro',"python3 -c 'import sys,hashlib; b=sys.stdin.buffer.read(); print(len(b),hashlib.sha256(b).hexdigest()); sys.stdout.flush(); sys.stdout.buffer.write(b)' "]
  start=time.monotonic()
  try:
   r=subprocess.run(args,input=payload,capture_output=True,timeout=25);end=time.monotonic();header,_,body=r.stdout.partition(b'\n')
   valid=r.returncode==0 and header.decode().split()==[str(n),digest] and body==payload
   row=dict(bytes_each_direction=n,mode=mode,duration_s=end-start,rc=r.returncode,valid=valid,stderr=r.stderr.decode(),payload_sha256=digest)
  except subprocess.TimeoutExpired as e:row=dict(bytes_each_direction=n,mode=mode,duration_s=time.monotonic()-start,timeout_s=25,valid=False,received_bytes=len(e.stdout or b''),stderr=(e.stderr or b'').decode(),payload_sha256=digest)
  rows.append(row);(P/'results.json').write_text(json.dumps(dict(rows=rows,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()),indent=2)+'\n');print(json.dumps(row),flush=True)
