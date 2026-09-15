import json,os,random,subprocess,time
from pathlib import Path
R=Path('/results')
order=[]
for trial in range(3):
    modes=['recorded','coalesce64k','whole']
    random.Random(120404+trial).shuffle(modes)
    order.extend(dict(trial=trial,mode=mode) for mode in modes)
(R/'order.json').write_text(json.dumps(order,indent=2)+'\n')
executions=[]
for row in order:
    name=f"trial{row['trial']}-{row['mode']}"
    subprocess.run(['tc','qdisc','replace','dev','lo','root','netem','limit','10000','delay','40ms','loss','0.1%','rate','20mbit'],check=True)
    for phase in ['before','after']:
        if phase=='after':
            env=dict(os.environ,BOOK_CHUNK_MODE=row['mode'],BOOK_TRIAL=str(row['trial']))
            start=time.monotonic_ns()
            with (R/(name+'.log')).open('w') as f:
                process=subprocess.run(['python','/experiment/run_network.py','--output',str(R/name)],env=env,stdout=f,stderr=subprocess.STDOUT)
            executions.append(dict(row,start_ns=start,end_ns=time.monotonic_ns(),exit_code=process.returncode))
            (R/'executions.json').write_text(json.dumps(executions,indent=2)+'\n')
            assert process.returncode==0,name
        (R/(name+'-'+phase+'.json')).write_bytes(subprocess.check_output(['tc','-json','-s','qdisc','show','dev','lo']))
subprocess.run(['tc','qdisc','del','dev','lo','root'],check=True)
(R/'completion.json').write_text(json.dumps(dict(subruns=len(executions),exit_codes=[e['exit_code'] for e in executions]))+'\n')
