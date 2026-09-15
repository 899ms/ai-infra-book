"""Recount actual SQLite launches/kernels; derive the RTX4090 copy crossover."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sqlite3
R=Path(__file__).resolve().parent;ROOT=R.parents[2];E=ROOT/'experiments/ch05/05-08/results';db=E/'timeline.sqlite';c=sqlite3.connect(f'file:{db}?mode=ro',uri=True);strings=dict(c.execute('select id,value from StringIds'));expected={'eager':(18,18),'fused':(15,15),'graph':(3,18),'fused_graph':(3,15)}
rows=[]
for start,end,text in c.execute("select start,end,text from NVTX_EVENTS where text like 'exp5_8:%' order by start"):
 label=text.split(':',1)[1]
 if label not in expected:continue
 names=[strings[n] for n, in c.execute('select nameId from CUPTI_ACTIVITY_KIND_RUNTIME where start>=? and end<=?',(start,end))]
 launches=[n for n in names if 'Launch' in n];kernels=c.execute('select count(*) from CUPTI_ACTIVITY_KIND_KERNEL where start>=? and end<=?',(start,end)).fetchone()[0]
 assert (len(launches),kernels)==expected[label],(label,launches,kernels)
 rows.append(dict(mode=label,host_launches=len(launches),graph_launches=sum('GraphLaunch' in n for n in launches),kernels=kernels))
c.close();assert len(rows)==4,rows
bw=1008*10**9;threshold=F(15,10**6)*bw/2;examples=[]
for mib in (2,16):
 size=mib*2**20;copy=F(2*size,bw)*10**6;examples.append(dict(input_mib=mib,copy_us=float(copy),eager_us=40,graph_with_copy_us=float(25+copy),graph_direct_write_us=25,direct_saving_us=15))
assert 2*threshold/bw==F(15,10**6)
files=[db,E/'trace-analysis.json',ROOT/'manuscripts/05-算子与运行时.md',ROOT/'calculations/configs/hardware.json']
out=dict(exercise='5-8',actual_three_FFN_counts=rows,bandwidth_bytes_s=bw,input_break_even_bytes=int(threshold),input_break_even_mib=float(threshold/2**20),examples=examples,scope='Trace counts are measurements; copy time and fixed compute/submission are teaching estimates, not new RTX4090 timing',source_sha256={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
(R/'5-8-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
