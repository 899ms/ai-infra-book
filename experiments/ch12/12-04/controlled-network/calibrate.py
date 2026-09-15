"""Probe shaping inside an isolated Docker network namespace, not the host."""
import json
import subprocess
from pathlib import Path
import time

R=Path('/results')
R.mkdir(exist_ok=True)
def call(args, name, check=True):
    start=time.monotonic_ns()
    process=subprocess.run(args,capture_output=True,text=True)
    row=dict(command=args,start_ns=start,end_ns=time.monotonic_ns(),exit_code=process.returncode,
             stdout=process.stdout,stderr=process.stderr)
    (R/name).write_text(json.dumps(row,indent=2)+'\n')
    if check:assert process.returncode==0,row
    return row
call(['python','-m','pip','freeze'],'python-packages.json')
call(['dpkg-query','-W','iproute2','iputils-ping','iperf3'],'network-packages.json')
call(['uname','-a'],'kernel.json')
call(['ip','-json','address'],'interfaces.json')
for label,delay,loss in [('unshaped',None,None),('rtt80-rate20-loss0','40ms','0%'),('rtt80-rate20-loss01','40ms','0.1%')]:
    if delay:
        call(['tc','qdisc','replace','dev','lo','root','netem','limit','10000','delay',delay,'loss',loss,'rate','20mbit'],label+'-set.json')
    call(['tc','-json','-s','qdisc','show','dev','lo'],label+'-before.json')
    call(['ping','-n','-c','10','-i','0.2','127.0.0.1'],label+'-ping.json',check=False)
    server=subprocess.Popen(['iperf3','-s','-1','-B','127.0.0.1','-p','19304','--json'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    time.sleep(.3)
    try:
        call(['iperf3','-c','127.0.0.1','-p','19304','-t','3','--json'],label+'-tcp.json')
        out,err=server.communicate(timeout=15)
        (R/(label+'-server.json')).write_text(json.dumps(dict(exit_code=server.returncode,stdout=out,stderr=err),indent=2)+'\n')
        assert server.returncode==0
    finally:
        if server.poll() is None:
            server.terminate();server.wait(timeout=5)
    call(['tc','-json','-s','qdisc','show','dev','lo'],label+'-after.json')
call(['tc','qdisc','del','dev','lo','root'],'qdisc-cleanup.json')
(R/'completion.json').write_text(json.dumps(dict(completed_profiles=3))+'\n')
