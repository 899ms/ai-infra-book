"""Profile one warmed real GEMM per fixed shape and tile."""
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--ncu',required=True);p.add_argument('--sudo',action='store_true');a=p.parse_args();r=Path(__file__).absolute().parent
out=r/'counters';out.mkdir(exist_ok=False)
metrics=['dram__bytes_op_read.sum','dram__bytes_op_write.sum','lts__t_bytes.sum','gpu__time_duration.sum','sm__warps_active.avg.pct_of_peak_sustained_active']
records=[]
for m in [1,1024]:
 for c in range(3):
  name=f'm{m}-c{c}'
  prefix=['sudo','-n'] if a.sudo else []
  command=prefix+[a.ncu,'--target-processes','application-only','--profile-from-start','off','--replay-mode','kernel','--cache-control','none','--clock-control','none','--kernel-name','regex:gemm','--launch-count','1','--metrics',','.join(metrics),'--export',str(out/name),sys.executable,str(r/'run.py'),'--profile','--m',str(m),'--config',str(c)]
  subprocess.run([sys.executable,str(r/'resource_guard.py'),'--out',str(r/'runs'/name),'--',*command],cwd=r,check=True)
  with (out/f'{name}.csv').open('w') as f:subprocess.run([a.ncu,'--import',str(out/f'{name}.ncu-rep'),'--page','raw','--csv','--print-units','base'],stdout=f,check=True)
  records.append(dict(m=m,config=c,command=command));print(name,flush=True)
(out/'collection.json').write_text(json.dumps(dict(metrics=metrics,records=records,version=subprocess.check_output([a.ncu,'--version'],text=True)),indent=2)+'\n')
