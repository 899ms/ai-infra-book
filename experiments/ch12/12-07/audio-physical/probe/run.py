"""Paired native IP_BOUND_IF / default-route UDP probes, no system route changes."""
import json,secrets,socket,subprocess,time
from pathlib import Path
B=Path(__file__).absolute().parent;out=B/'runs';out.mkdir(exist_ok=False)
index=socket.if_nametoindex('en0');nonce=secrets.token_hex(16)
for name,cmd in [('default-route',['route','-n','get','155.103.252.95']),('scoped-route',['route','-n','get','-ifscope','en0','155.103.252.95'])]:
 r=subprocess.run(cmd,capture_output=True,check=True);(out/(name+'.txt')).write_bytes(r.stdout)
p=subprocess.Popen(['ssh','rtx-pro','python3','-u','-','--nonce',nonce,'--port','19277'],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p.stdin.write((B/'udp_peer.py').read_bytes());p.stdin.close();ready=p.stdout.readline();assert json.loads(ready)['event']=='ready'
rows=[]
for round,bound in enumerate([True,False,False,True]):
 s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.settimeout(2)
 if bound:s.setsockopt(socket.IPPROTO_IP,25,index)
 actual=s.getsockopt(socket.IPPROTO_IP,25);assert actual==(index if bound else 0)
 for n in [64,1200]:
  i=len(rows);payload=(nonce+':'+str(i)+':').encode();payload+=bytes([i])*(n-len(payload))
  start=time.perf_counter_ns();s.sendto(payload,('155.103.252.95',19277))
  try:
   data,addr=s.recvfrom(2048);elapsed=(time.perf_counter_ns()-start)/1e6
   row=dict(index=i,round=round,bound=bound,interface='en0' if bound else None,kernel_bound_if=actual,bytes=n,echo_equal=data==payload and addr==('155.103.252.95',19277),rtt_ms=elapsed,timeout=False)
  except socket.timeout:row=dict(index=i,round=round,bound=bound,interface='en0' if bound else None,kernel_bound_if=actual,bytes=n,echo_equal=False,rtt_ms=None,timeout=True)
  rows.append(row)
 s.close()
rest=p.stdout.read();err=p.stderr.read();code=p.wait(timeout=10)
(out/'peer.jsonl').write_bytes(ready+rest);(out/'peer.stderr').write_bytes(err)
(out/'result.json').write_text(json.dumps(dict(probes=rows,peer_exit_code=code,interface_index=index,ip_bound_if_option=25,system_routes_modified=False),indent=2)+'\n')
assert code==0;print(json.dumps(rows))
