"""Measure Docker lifecycle semantics without touching unrelated containers."""
import hashlib
import json
from pathlib import Path
import random
import os
import select
import shutil
import socket
import subprocess
import time
import uuid

R = Path(__file__).resolve().parent
O = R/'results-restore-diagnostic'


def save(p, x):
    p.write_text(json.dumps(x, indent=2)+'\n')


def main():
    O.mkdir(exist_ok=False)
    runid = 'book1102-'+uuid.uuid4().hex[:10]
    containers, images, connections, commands, rows = [], [], [], [], []
    def append(name, row):
        with (O/name).open('a') as f:
            f.write(json.dumps(row)+'\n')
    def cmd(args, check=True, timeout=60):
        start = time.monotonic()
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        row = dict(command=args,start=start,end=time.monotonic(),exit_code=p.returncode,stdout=p.stdout,stderr=p.stderr)
        commands.append(row)
        append('commands.jsonl',row)
        if check and p.returncode:
            raise RuntimeError(row)
        return row
    def docker(*args, **kw):
        return cmd(['docker', *map(str,args)], **kw)
    base = docker('image','inspect','python:3.11-slim','--format','{{.Id}}')['stdout'].strip()
    save(O/'environment.json',dict(runid=runid,base_image_id=base,
        docker=json.loads(docker('version','--format','{{json .}}')['stdout']),
        criu=cmd(['criu','--version'])['stdout'],kernel=cmd(['uname','-a'])['stdout'],
        source_hashes={n:hashlib.sha256((R/n).read_bytes()).hexdigest() for n in ['run_restore_diagnostic.py','worker_unix.py','PROTOCOL.md']}))
    docker_root = Path(docker('info','--format','{{.DockerRootDir}}')['stdout'].strip())
    assert docker_root.is_absolute()
    def inspect(cid):
        row=json.loads(docker('inspect',cid)['stdout'])[0]
        return dict(id=row['Id'],state=row['State'],ip=row['NetworkSettings']['IPAddress'],image=row['Image'])
    def create(label,image=base):
        start=time.monotonic()
        name=runid+'-'+label
        row=docker('create','--name',name,'--label','book.experiment='+runid,'--cpus','1','--memory','256m',
            '--memory-swap','256m','--network','host',image,'python','-u','/tmp/book-worker.py')
        cid=row['stdout'].strip();containers.append(cid)
        docker('cp',str(R/'worker_unix.py'),cid+':/tmp/book-worker.py')
        return cid,dict(start=start,created=time.monotonic())
    class CommandStream:
        def __init__(self,p): self.p=p
        def sendall(self,data): self.p.stdin.write(data);self.p.stdin.flush()
        def recv(self,n):
            if not select.select([self.p.stdout],[],[],10)[0]:raise TimeoutError('command stream')
            return os.read(self.p.stdout.fileno(),n)
        def close(self):
            if self.p.poll() is None:
                self.p.stdin.close()
                try:self.p.wait(timeout=5)
                except subprocess.TimeoutExpired:self.p.terminate();self.p.wait(timeout=5)
    def connect(cid):
        start=time.monotonic();info=inspect(cid)
        bridge="""import socket,sys,time
s=socket.socket(socket.AF_UNIX)
for i in range(100):
 try:s.connect('/tmp/book-control.sock');break
 except (FileNotFoundError,ConnectionRefusedError):time.sleep(.02)
print('READY',flush=True)
for line in sys.stdin.buffer:
 s.sendall(line);data=b''
 while not data.endswith(b'\\n'):
  chunk=s.recv(65536)
  if not chunk:raise RuntimeError('EOF')
  data+=chunk
 sys.stdout.buffer.write(data);sys.stdout.buffer.flush()
s.close()
"""
        p=subprocess.Popen(['docker','exec','-i',cid,'python','-u','-c',bridge],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stream=CommandStream(p);connections.append(stream)
        ready=b''
        while not ready.endswith(b'\n'):
            chunk=stream.recv(6)
            if not chunk:
                raise RuntimeError('bridge EOF: '+p.stderr.read().decode())
            ready+=chunk
        assert ready==b'READY\n',ready
        return stream,dict(start=start,ready=time.monotonic(),container=info,transport='docker exec stdio to private container UNIX socket',host_network=True)
    def call(s,op='get',**kw):
        req=dict(op=op,request_id=uuid.uuid4().hex,**kw);start=time.monotonic()
        s.sendall(json.dumps(req).encode()+b'\n');data=b''
        while not data.endswith(b'\n'):
            chunk=s.recv(65536)
            if not chunk:raise ConnectionError('EOF')
            data+=chunk
        value=json.loads(data);assert value['request_id']==req['request_id']
        row=dict(start=start,end=time.monotonic(),request=req,response=value)
        append('external-ledger.jsonl',row)
        return row
    def launch(label,image=base):
        cid,timing=create(label,image)
        timing['start_api']=docker('start',cid)
        s,conn=connect(cid);first=call(s)
        timing.update(connection=conn,first_tool=first,end=first['end'])
        return cid,s,timing
    def committed(cid,label):
        name=runid+':'+label
        row=docker('commit','--pause=true',cid,name)
        images.append(name)
        return name,row
    def collect_checkpoint(path):
        if not path.exists():return
        listing=cmd(['sudo','-n','python3','-c',
            'import pathlib,json,hashlib,sys; p=pathlib.Path(sys.argv[1]); print(json.dumps([dict(path=str(f.relative_to(p)),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sorted(p.rglob("*")) if f.is_file()]))',str(path)])
        save(path.parent/(path.name+'-files.json'),json.loads(listing['stdout']))
        for name in ['dump.log','restore.log']:
            result=cmd(['sudo','-n','find',str(path),'-name',name],check=False)
            for index,file in enumerate(result['stdout'].splitlines()):
                data=cmd(['sudo','-n','cat',file],check=False)
                (path.parent/(path.name+f'-{index}-'+name)).write_text(data['stdout'])
    order=[]
    for trial in range(3):
        paths=['pause','checkpoint','clean_rebuild','filesystem']
        random.Random(1102+trial).shuffle(paths)
        order.extend((trial,p) for p in paths)
    order=[(0,'checkpoint')]
    save(O/'order.json',order)
    try:
        for trial,path in order:
            label=f't{trial}-{path}'
            cid,s,creation=launch(label)
            marker={'trial':trial,'path':path,'nonce':uuid.uuid4().hex}
            before=call(s,'set',marker=marker)
            row=dict(trial=trial,path=path,container=cid,creation=creation,before=before)
            if path=='pause':
                row['pause']=docker('pause',cid)
                row['paused_inspect']=inspect(cid)
                time.sleep(.2)
                row['unpause']=docker('unpause',cid)
                row['after']=call(s)
                row['same_connection']=True
            elif path=='clean_rebuild':
                s.close();row['old_stop']=docker('stop','-t','1',cid)
                new,ns,timing=launch(label+'-new')
                row.update(new_container=new,recovery=timing,after=timing['first_tool'])
                ns.close()
            elif path=='filesystem':
                image,commit=committed(cid,label)
                row['commit']=commit
                row['original_after_commit']=call(s)
                new,ns,timing=launch(label+'-new',image)
                row.update(new_container=new,recovery=timing,after=timing['first_tool'])
                ns.close()
            else:
                folder=O/label;folder.mkdir()
                # Native established-connection behavior is measured before reconnection control.
                live=folder/'live';live.mkdir()
                row['live_checkpoint']=docker('checkpoint','create','--leave-running','--checkpoint-dir',live,cid,'snap',check=False)
                try:row['live_connection_after']=call(s)
                except Exception as exc:row['live_connection_error']=repr(exc)
                s.close()
                time.sleep(.2)
                disconnected=folder/'disconnected';disconnected.mkdir()
                image,commit=committed(cid,label)
                row['commit']=commit
                cp=docker('checkpoint','create','--leave-running','--checkpoint-dir',disconnected,cid,'snap',check=False)
                row['checkpoint']=cp
                row['derivatives']=[]
                if cp['exit_code']==0:
                    for number in range(2):
                        new,timing=create(label+f'-clone{number}',image)
                        copy=folder/f'clone{number}';copy.mkdir()
                        cmd(['sudo','-n','cp','-a',str(disconnected/'snap'),str(copy/'snap')])
                        native_dir=docker_root/'containers'/new/'checkpoints'
                        cmd(['sudo','-n','mkdir','-p',str(native_dir)])
                        cmd(['sudo','-n','cp','-a',str(copy/'snap'),str(native_dir/'snap')])
                        restored=docker('start','--checkpoint','snap',new,check=False)
                        found=cmd(['sudo','-n','find',str(docker_root/'containers'/new),'-type','f','-name','*.log'],check=False)
                        diagnostics=[]
                        for logpath in found['stdout'].splitlines():
                            log=cmd(['sudo','-n','cat',logpath],check=False)
                            diagnostics.append(dict(path=logpath,content=log['stdout']))
                        derivative=dict(container=new,creation=timing,restore=restored,diagnostics=diagnostics)
                        if restored['exit_code']==0:
                            ns,conn=connect(new)
                            derivative.update(connection=conn,first_tool=call(ns),mutated=call(ns,'add',value=number+10))
                            ns.close()
                        row['derivatives'].append(derivative)
                        collect_checkpoint(copy)
                rs,reconnect=connect(cid)
                row['original_after']=call(rs);row['original_reconnect']=reconnect;rs.close()
                collect_checkpoint(live);collect_checkpoint(disconnected)
            rows.append(row);append('cases.jsonl',row)
            print(trial,path,'recorded',flush=True)
            s.close()
            # Reclaim each case promptly; global cleanup also handles partial failures.
            for own in list(containers):
                docker('rm','-f',own,check=False)
                containers.remove(own)
        save(O/'completion.json',dict(status='diagnostic_case_recorded',count=len(rows),runid=runid))
    finally:
        for s in connections:
            s.close()
        for cid in containers:
            docker('logs',cid,check=False)
            docker('rm','-f',cid,check=False)
        for image in images:
            docker('image','rm',image,check=False)
        remaining=docker('ps','-aq','--filter','label=book.experiment='+runid)['stdout'].split()
        save(O/'cleanup.json',dict(runid=runid,remaining_containers=remaining,images=images))
        assert not remaining


if __name__=='__main__':
    main()
