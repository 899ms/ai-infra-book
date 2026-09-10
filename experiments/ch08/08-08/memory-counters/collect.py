"""Use the installed Nsight Compute CLI; run with existing counter privileges."""
import argparse,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--ncu',required=True);a=p.parse_args();r=Path(__file__).absolute().parent
metrics='dram__bytes_op_read.sum,dram__bytes_op_write.sum,lts__t_bytes.sum,gpu__time_duration.sum'
for name in ['bf16','fp8']:
 assert not (r/f'{name}.ncu-rep').exists()
 command=[a.ncu,'--target-processes','all','--profile-from-start','off','--replay-mode','kernel','--cache-control','none','--clock-control','none','--kernel-name','regex:kernel_unified_attention','--launch-skip','36','--launch-count','1','--metrics',metrics,'--export',str(r/name),sys.executable,str(r/'run.py'),'--format',name,'--output',str(r/'results'/name)]
 subprocess.run([sys.executable,str(r/'resource_guard.py'),'--out',str(r/'runs'/name),'--',*command],cwd=r,check=True)
 with (r/f'{name}.csv').open('w') as f:subprocess.run([a.ncu,'--import',str(r/f'{name}.ncu-rep'),'--page','raw','--csv','--print-units','base'],stdout=f,check=True)
(r/'tool-version.txt').write_text(subprocess.check_output([a.ncu,'--version'],text=True))
