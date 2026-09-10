"""Probe direct native UDP path; SSH is used only to launch the peer."""
import json,secrets,socket,subprocess,time
from pathlib import Path
B=Path(__file__).absolute().parent
out=B/'runs';out.mkdir(exist_ok=False);nonce=secrets.token_hex(16)
code=(B/'udp_peer.py').read_bytes()
cmd=['ssh','rtx-pro','python3','-u','-','--nonce',nonce,'--port','19277']
p=subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p.stdin.write(code);p.stdin.close()
ready=p.stdout.readline();assert json.loads(ready)['event']=='ready'
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.settimeout(2)
rows=[]
for i,n in enumerate([64,512,1200,1400,1400,1200,512,64]):
 payload=(nonce+':'+str(i)+':').encode();payload+=bytes([i])*(n-len(payload))
 start=time.perf_counter_ns();s.sendto(payload,('155.103.252.95',19277))
 try:
  data,addr=s.recvfrom(2048);end=time.perf_counter_ns();equal=data==payload and addr==('155.103.252.95',19277)
  row=dict(index=i,bytes=n,echo_equal=equal,rtt_ms=(end-start)/1e6,timeout=False)
 except socket.timeout:row=dict(index=i,bytes=n,echo_equal=False,rtt_ms=None,timeout=True)
 rows.append(row)
s.close();remaining=p.stdout.read();stderr=p.stderr.read();exitcode=p.wait(timeout=10)
(out/'peer.jsonl').write_bytes(ready+remaining);(out/'peer.stderr').write_bytes(stderr)
(out/'result.json').write_text(json.dumps(dict(transport='direct IPv4 UDP, not SSH tunnel',destination='rtx-pro',port=19277,probes=rows,peer_exit_code=exitcode),indent=2)+'\n')
assert exitcode==0
print(json.dumps(rows))
