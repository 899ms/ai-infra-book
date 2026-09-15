import json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent
import hashlib
V=json.loads((R.parent/'receive-windows/verification.json').read_text());assert V['verified'], 'Receive-window verification required before this benchmark'
for name,digest in V['source_sha256'].items():assert hashlib.sha256((R.parent/'receive-windows'/name).read_bytes()).hexdigest()==digest, 'Receive-window verification is stale'
ROOT=R/'results';ROOT.mkdir(exist_ok=False)
def run(*args,output=None):
 p=subprocess.run(args,check=True,text=True,capture_output=output is not None)
 if output:output.write_text(p.stdout)
for workload in ['asr','computer','image']:
 O=ROOT/workload;O.mkdir();run('docker','image','inspect','ai-infra-book-net1204:local',output=O/'image-inspect.json')
 order=[dict(trial=t,mode=m) for t in range(3) for m in (['whole','16k','64k'][t:]+['whole','16k','64k'][:t])];(O/'order.json').write_text(json.dumps(order,indent=2)+'\n')
 for c in order:
  name=f"trial{c['trial']}-{c['mode']}";print('START',workload,name,flush=True)
  run('docker','run','-d','--name','book-chunks1204','--network','none','--cap-add','NET_ADMIN','--cpus','2','--memory','2g','-v',f'{R.parent}:/work','-w','/work/transfer-chunks','ai-infra-book-net1204:local','sleep','infinity',output=O/(name+'-id.txt'))
  try:
   run('docker','inspect','book-chunks1204',output=O/(name+'-container.json'))
   run('docker','exec','book-chunks1204','tc','qdisc','add','dev','lo','root','netem','delay','40ms','rate','20mbit','loss','0.1%')
   run('docker','exec','book-chunks1204','tc','-s','-j','qdisc','show','dev','lo',output=O/(name+'-before.json'))
   run('docker','exec','-e','BOOK_CHUNK_MODE='+c['mode'],'-e','BOOK_WINDOW_TRIAL='+str(c['trial']),'book-chunks1204','python',workload+'.py','--output',f'results/{workload}/{name}')
   run('docker','exec','book-chunks1204','sleep','1')
   run('docker','exec','book-chunks1204','tc','-s','-j','qdisc','show','dev','lo',output=O/(name+'-after.json'))
  finally:run('docker','rm','-f','book-chunks1204',output=O/(name+'-removed.txt'))
  print('DONE',workload,name,flush=True)
