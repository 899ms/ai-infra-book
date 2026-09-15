import json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parent;ROOT=R/'results';ROOT.mkdir(exist_ok=False)
def run(*args,output=None):
 p=subprocess.run(args,check=True,text=True,capture_output=output is not None)
 if output:output.write_text(p.stdout)
for workload in ['asr','tts','computer','image']:
 O=ROOT/workload;O.mkdir();run('docker','image','inspect','ai-infra-book-net1204:local',output=O/'image-inspect.json')
 order=[dict(trial=t,mode=m) for t in range(3) for m in (['default','64k','4m'][t:]+['default','64k','4m'][:t])];(O/'order.json').write_text(json.dumps(order,indent=2)+'\n')
 for c in order:
  name=f"trial{c['trial']}-{c['mode']}";print('START',workload,name,flush=True)
  run('docker','run','-d','--name','book-matchedwin1204','--network','none','--cap-add','NET_ADMIN','--cpus','2','--memory','2g','-v',f'{R.parent}:/work','-w','/work/receive-windows','ai-infra-book-net1204:local','sleep','infinity',output=O/(name+'-id.txt'))
  try:
   run('docker','inspect','book-matchedwin1204',output=O/(name+'-container.json'))
   run('docker','exec','book-matchedwin1204','tc','qdisc','add','dev','lo','root','netem','delay','40ms','rate','20mbit','loss','0.1%')
   run('docker','exec','book-matchedwin1204','tc','-s','-j','qdisc','show','dev','lo',output=O/(name+'-before.json'))
   run('docker','exec','-e','BOOK_WINDOW_MODE='+c['mode'],'-e','BOOK_WINDOW_TRIAL='+str(c['trial']),'book-matchedwin1204','python',workload+'.py','--output',f'results/{workload}/{name}')
   run('docker','exec','book-matchedwin1204','sleep','1')
   run('docker','exec','book-matchedwin1204','tc','-s','-j','qdisc','show','dev','lo',output=O/(name+'-after.json'))
  finally:run('docker','rm','-f','book-matchedwin1204',output=O/(name+'-removed.txt'))
  print('DONE',workload,name,flush=True)
