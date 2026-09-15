"""Scaling curves and continuous/discrete optima with exact model coefficients."""
from pathlib import Path
from fractions import Fraction as F
import math,json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('07-*.md'))
compute=F(20);base=F(360*2**20*1000,50*10**9);rows=[]
for label,traffic,bw in [('baseline',1,1),('half_traffic',F(1,2),1),('two_NICs',1,2)]:
 comm=base*traffic/bw;cross=compute/comm;opt=math.sqrt(float(cross));lo=math.floor(opt);hi=math.ceil(opt)
 value=lambda x:max(float(compute)/x,float(comm)*x)
 integer=min(range(1,65),key=value);assert integer in (lo,hi)
 powers=min([1,2,4,8,16,32,64],key=value)
 grid=[F(i,100) for i in range(100,1601)]
 curves=[dict(multiplier=float(x),compute_ms=float(compute/x),constant_comm_ms=float(comm),serial_ms=float(compute/x+comm),overlap_ms=float(max(compute/x,comm)),growing_comm_ms=float(comm*x),growing_overlap_ms=float(max(compute/x,comm*x))) for x in grid]
 assert compute/cross==comm
 rows.append(dict(case=label,comm_at_x1_ms=float(comm),cross_constant_exact=str(cross),cross_constant=float(cross),growing_optimal_continuous_x=opt,growing_min_ms=value(opt),growing_optimal_integer_x=integer,growing_integer_ms=value(integer),growing_optimal_power2_x=powers,growing_power2_ms=value(powers),curves=curves))
fig,axes=plt.subplots(1,2,figsize=(11,4.3),layout='constrained')
for row,color in zip(rows,['#333333','#2675bd','#dc7627']):
 x=[a['multiplier'] for a in row['curves']]
 for ax,key,style in [(axes[0],'serial_ms','--'),(axes[0],'overlap_ms','-'),(axes[1],'growing_overlap_ms','-')]:
  ax.plot(x,[a[key] for a in row['curves']],color=color,linestyle=style,label=row['case']+' '+key,alpha=.8)
axes[0].set(title='Constant traffic: serial and ideal overlap',ylim=(0,30))
axes[1].set(title='Traffic proportional to card multiplier',ylim=(0,65))
for ax in axes:ax.set(xlabel='Card multiplier x',ylabel='Completion time (ms)',xlim=(1,8));ax.grid(alpha=.2);ax.legend(fontsize=7)
fig.savefig(P/'7-2-curves.png',dpi=150);fig.savefig(P/'7-2-curves.svg');plt.close(fig)
out=dict(exercise='7-2',rows=rows,scope='Ideal uniform compute scaling, independent bidirectional traffic, full utilization of both NICs; continuous optimum and deployment-granularity alternatives distinguished',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'7-2-results.json').write_text(json.dumps(out,indent=2)+'\n');print([{k:v for k,v in r.items() if k!='curves'} for r in rows])
