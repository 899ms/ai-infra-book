import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).absolute().parent;m=json.loads((r/'manifest.json').read_text())
for name,digest in m.items():assert hashlib.sha256((r/name).read_bytes()).hexdigest()==digest,name
for name in ['bf16','fp8']:
 s=json.loads((r/'runs'/name/'supervisor.json').read_text());assert s['exit_code']==0 and s['reason'] is None and s['leftovers']=={}
 command=json.loads((r/'runs'/name/'launch.json').read_text())['command']
 for flag,value in [('--launch-skip','36'),('--launch-count','1'),('--cache-control','none'),('--clock-control','none'),('--profile-from-start','off'),('--kernel-name','regex:kernel_unified_attention')]:assert command[command.index(flag)+1]==value
subprocess.run([sys.executable,str(r/'analyze.py')],check=True)
print('PASS:',len(m),'files; actual counters, matched scope, weights, calibration, completed runs')
