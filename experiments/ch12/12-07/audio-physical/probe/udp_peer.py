"""Bounded nonce echo probe; no proxy or persistent listener."""
import argparse,json,socket,time,hashlib
p=argparse.ArgumentParser();p.add_argument('--nonce',required=True);p.add_argument('--port',type=int,default=19277);a=p.parse_args()
s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);s.bind(('0.0.0.0',a.port));s.settimeout(.5)
start=time.monotonic();seen=[];prefix=a.nonce.encode()+b':'
print(json.dumps(dict(event='ready',port=a.port)),flush=True)
while time.monotonic()-start<30:
 try:data,addr=s.recvfrom(2048)
 except socket.timeout:continue
 if not data.startswith(prefix):continue
 s.sendto(data,addr);seen.append(dict(bytes=len(data),elapsed_s=time.monotonic()-start,source_ip_sha256=hashlib.sha256(addr[0].encode()).hexdigest(),source_port=addr[1]))
 if len(seen)>=8:break
s.close();print(json.dumps(dict(event='complete',received=seen,elapsed_s=time.monotonic()-start)),flush=True)
