import hashlib,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
for folder in ['receive-windows','transfer-chunks']:
 V=json.loads((R.parent/folder/'verification.json').read_text());assert V['verified']
 for name,digest in V['source_sha256'].items():assert hashlib.sha256((R.parent/folder/name).read_bytes()).hexdigest()==digest
ROOT=R/'results';ROOT.mkdir(exist_ok=False)
def run(*args,output=None):
 p=subprocess.run(args,check=True,text=True,capture_output=output is not None)
 if output:output.write_text(p.stdout)
for workload in ['asr','tts','computer']:
 O=ROOT/workload;O.mkdir();run('docker','image','inspect','ai-infra-book-net1204:local',output=O/'image-inspect.json')
 run('docker','run','-d','--name','book-workload-recovery1204','--network','none','--cap-add','NET_ADMIN','--cpus','2','--memory','2g','-v',f'{R.parent}:/work','-w','/work/workload-recovery','ai-infra-book-net1204:local','sleep','infinity',output=O/'container-id.txt')
 try:
  run('docker','inspect','book-workload-recovery1204',output=O/'container-inspect.json')
  run('docker','exec','book-workload-recovery1204','tc','qdisc','add','dev','lo','root','netem','delay','40ms','rate','20mbit','loss','0.1%')
  run('docker','exec','book-workload-recovery1204','tc','-s','-j','qdisc','show','dev','lo',output=O/'before.json')
  run('docker','exec','book-workload-recovery1204','python','run.py','--workload',workload,'--output',f'results/{workload}/run')
  run('docker','exec','book-workload-recovery1204','sleep','1')
  run('docker','exec','book-workload-recovery1204','tc','-s','-j','qdisc','show','dev','lo',output=O/'after.json')
 finally:run('docker','rm','-f','book-workload-recovery1204',output=O/'container-removed.txt')
