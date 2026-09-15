import json,random,subprocess,os
from pathlib import Path
R=Path(__file__).resolve().parent;O=R/'results';O.mkdir(exist_ok=False)
def run(*args,output=None):
 p=subprocess.run(args,check=True,text=True,capture_output=output is not None)
 if output:(O/output).write_text(p.stdout)
run('docker','image','inspect','ai-infra-book-net1204:local',output='image-inspect.json')
order=[]
for trial in range(3):
 base=['default','64k','4m'];modes=base[trial:]+base[:trial]
 for mode in modes:order.append(dict(trial=trial,mode=mode))
(O/'order.json').write_text(json.dumps(order,indent=2)+'\n')
for c in order:
 name=f"trial{c['trial']}-{c['mode']}";print('START',name,flush=True)
 run('docker','run','-d','--name','book-ttswindow1204','--network','none','--cap-add','NET_ADMIN','--cpus','2','--memory','2g','-v',f'{R.parent}:/work','-w','/work/tts-windows','ai-infra-book-net1204:local','sleep','infinity',output=name+'-id.txt')
 try:
  run('docker','inspect','book-ttswindow1204',output=name+'-container.json')
  run('docker','exec','book-ttswindow1204','tc','qdisc','add','dev','lo','root','netem','delay','40ms','rate','20mbit','loss','0.1%')
  run('docker','exec','book-ttswindow1204','tc','-s','-j','qdisc','show','dev','lo',output=name+'-before.json')
  run('docker','exec','-e','BOOK_WINDOW_MODE='+c['mode'],'-e','BOOK_WINDOW_TRIAL='+str(c['trial']),'book-ttswindow1204','python','run_network.py','--output','results/'+name)
  run('docker','exec','book-ttswindow1204','sleep','1')
  run('docker','exec','book-ttswindow1204','tc','-s','-j','qdisc','show','dev','lo',output=name+'-after.json')
 finally:run('docker','rm','-f','book-ttswindow1204',output=name+'-removed.txt')
 print('DONE',name,flush=True)
