#!/usr/bin/env python3
"""Build reproducible chapter-eight figures and an offline reading edition."""
from pathlib import Path
import argparse,base64,hashlib,html,json,re,subprocess
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle,FancyBboxPatch,FancyArrowPatch
import numpy as np
import markdown
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
parser=argparse.ArgumentParser();parser.add_argument('--font');args=parser.parse_args()
import sys
sys.path.insert(0,str(HERE.parent))
from preview_output import preview_path
from figure_style.typography import configure_font
font,family=configure_font(args.font)
plt.rcParams.update({'font.family':[family,'DejaVu Sans'],'font.size':11,'axes.unicode_minus':False,'svg.fonttype':'path','svg.hashsalt':'ch08-v1','pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':'white','savefig.facecolor':'white'})
C={'ink':'#203c48','blue':'#286b98','teal':'#16857b','orange':'#bc722b','red':'#a94c52','pale':'#edf3f6','gray':'#e2e7ea','line':'#b7c8ce'}
for row in json.loads((HERE/'sources.json').read_text())['sources']:
 if hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()!=row['sha256']:raise SystemExit('Source changed; review before rebuilding: '+row['path'])
def read(p):return json.loads((ROOT/p).read_text())
def calc(n):return read('calculations/results/'+n+'.json')
outputs=[];data={};warnings=[]
def save(f,name):
 f.canvas.draw();renderer=f.canvas.get_renderer()
 for t in f.findobj(matplotlib.text.Text):
  if t.get_visible() and t.get_text():
   b=t.get_window_extent(renderer)
   if b.x0<0 or b.y0<0 or b.x1>f.bbox.width or b.y1>f.bbox.height:warnings.append({'figure':name,'text':t.get_text()})
 for ext in ['svg','png','pdf']:
  p=HERE/(name+'.'+ext);f.savefig(p,dpi=180,bbox_inches='tight',pad_inches=.15);outputs.append(p)
 plt.close(f)
def canvas(h=7):
 f,a=plt.subplots(figsize=(12,h));f.subplots_adjust(left=.025,right=.975,bottom=.03,top=.97);a.set(xlim=(0,1),ylim=(0,1));a.axis('off');return f,a
def box(a,x,y,w,h,title,body='',col='pale',size=12):
 a.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.003,rounding_size=0.008',fc=C[col],ec=C['line']))
 a.text(x+w/2,y+h*(.66 if body else .5),title,ha='center',va='center',fontsize=size,weight='bold',color=('white' if col in ['teal','blue','orange','red'] else C['ink']))
 if body:a.text(x+w/2,y+h*.27,body,ha='center',va='center',fontsize=10,color=C['ink'])
def arrow(a,p,q,col='teal',rad=0):a.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=14,color=C[col],lw=1.5,connectionstyle=f'arc3,rad={rad}'))
# Batch model: compare the same weight term with two history lengths.
f,a=plt.subplots(figsize=(11,6.8));f.subplots_adjust(left=.10,right=.96,bottom=.14,top=.93)
bs=np.arange(1,129);weight=15136811008/2**30/bs
for L,col in [(2048,'blue'),(8192,'teal')]:
 kv=L*147456/2**30;a.plot(bs,weight+kv,color=C[col],lw=2.5,label=f'{L//1024}K context: total read');a.axhline(kv,color=C[col],ls='--',lw=1.2,label=f'{L//1024}K context: KV')
 cross=(15136811008+L*147456-1)//(L*147456);yy=15136811008/2**30/cross+kv;a.scatter([cross],[yy],color=C[col],s=45);a.annotate(f'b = {cross}',xy=(cross,yy),xytext=(cross*.65,yy*1.6),arrowprops={'arrowstyle':'->','color':C[col]},color=C[col])
a.plot(bs,weight,color='#7b858a',lw=1.7,label="weight amortized per token");a.set(xscale='log',yscale='log',xlim=(1,128),ylim=(.09,20),xlabel='batch size b',ylabel="read volume per output token / GiB",xticks=[1,2,4,8,16,32,64,128],xticklabels=[1,2,4,8,16,32,64,128],yticks=[.125,.25,.5,1,2,4,8,16],yticklabels=['0.125','0.25','0.5','1','2','4','8','16']);a.minorticks_off();a.grid(alpha=.16);a.legend(frameon=False,loc='upper right')
data['batch']={'shared_weight_bytes':15136811008,'kv_bytes_per_position':147456,'batch':bs.tolist(),'history_lengths':[2048,8192]};save(f,'figure-8-2-batch')
# 1. Time bars are read from saved events, never hand-estimated GPU times.
f=plt.figure(figsize=(13,10));gs=f.add_gridspec(3,1,height_ratios=[1,1,1],hspace=.65,left=.08,right=.96,top=.95,bottom=.06)
for j,(policy,label) in enumerate([('fixed',"fixed batch"),('continuous',"continuous batching"),('chunked',"decode-priority chunking")]):
 d=calc('iteration-batching-pro6000-'+policy);a=f.add_subplot(gs[j]);data[policy]=d['batching_steps']
 for step in d['batching_steps']:
  for plan in step['plans']:
   y=3-int(plan['request'][1:]);start=step['start_ns']/1e6;dur=step['duration_ns']/1e6
   a.broken_barh([(start,dur)],(y-.34,.68),facecolors=C['blue' if plan['phase']=='prefill' else 'teal'],edgecolors='white',lw=.8)
   # The time bars carry the scheduling argument; detailed step counts stay in figure-data.json.
 s=d['summary'];a.set(yticks=range(4),yticklabels=['r3','r2','r1','r0'],xlim=(0,900),xticks=[0,150,300,450,600,750,900],ylim=(-.85,3.85),xlabel="Time / ms");a.set_title(label+f"  ·  total time {s['finish_ns']/1e6:.0f} ms, max interval {s['max_itl_ns']/1e6:.0f} ms",loc='left',fontsize=12,pad=9)
 # Arrival markers and maximum output gap are derived from the saved request events.
 for reqrow in d['batching_requests']:
  y=3-int(reqrow['id'][1:]);a.scatter([reqrow['arrival_ns']/1e6],[y],marker='>',s=45,color=C['ink'],zorder=6,clip_on=False)
 gaps=[(v-u,r['id'],u/1000,v/1000) for r in d['batching_requests'] for u,v in zip(r['delivery_ns'],r['delivery_ns'][1:])]
 gap,rid,x0,x1=max(gaps);y=3-int(rid[1:])+.48;x0/=1000;x1/=1000
 a.annotate('',xy=(x1,y),xytext=(x0,y),arrowprops={'arrowstyle':'|-|','color':C['orange'],'lw':1.6});a.text((x0+x1)/2,y+.13,f'{gap/1e6:.1f} ms',ha='center',va='bottom',fontsize=9,color=C['orange'])
data['chunk_history']=calc('chunk-history-book')['chunk_history_rows'];save(f,'figure-8-3-scheduling')
# 2. Physical pages, with explicit shared block references.
f,a=canvas(8.5);lengths=[9,13,5,15];styles=[("reserved as whole",64),("4 positions per block",52),("A, B share first 8 positions",44)]
# A and B both have at least eight valid positions; two complete blocks can be shared.
for j,(lab,total) in enumerate(styles):
 top=.93-j*.29;a.text(.025,top,lab,fontsize=14,weight='bold');a.text(.975,top,f'{total} physical positions',ha='right',fontsize=13,color=C['teal'])
 for r,L in enumerate(lengths):
  y=top-.052-r*.044;a.text(.03,y+.012,f'{chr(65+r)}  L={L}',va='center',fontsize=10)
  alloc=16 if j==0 else ((L+3)//4)*4
  for k in range(alloc):
   x=.20+k*.043
   shared=(j==2 and r==1 and k<8)
   col='white' if shared else (C['blue'] if k<L else C['gray'])
   a.add_patch(Rectangle((x,y),.038,.026,fc=col,ec=C['teal'] if shared else 'white',lw=1,hatch='//' if shared else None))
  if j>0:
   for boundary in range(0,alloc+1,4):
    bx=.198+boundary*.043;a.plot([bx,bx],[y-.003,y+.03],color=C['line'],lw=.8)
  if j==2 and r==1:
   arrow(a,(.20+.16,y+.028),(.20+.16,y+.044),'teal');a.text(.92,y+.012,"reference A",va='center',color=C['teal'],fontsize=10)
 a.text(.20,top-.24,"blue: valid position    gray: allocated unused    hatch: reuse existing block (no new alloc)",fontsize=10,color=C['ink'])
data['pages']={'lengths':lengths,'page_size':4,'reserved':64,'paged':52,'shared':44,'shared_prefix':8};save(f,'figure-8-5-pages')
# 3. Radix tree from first four actual token streams; all-round prefix lengths.
req=read('experiments/ch08/08-04/inputs/agent-prompts.json')['requests'];seq=[r['prompt_token_ids'] for r in req]
def lcp(items):
 n=0
 for vals in zip(*items):
  if len(set(vals))!=1:break
  n+=1
 return n
nodes=[];edges=[]
def tree(ids,depth,parent=None):
 end=depth+lcp([seq[i][depth:] for i in ids]);idx=len(nodes);nodes.append({'ids':ids,'depth':end,'y':sum(ids)/len(ids),'parent':parent})
 if parent is not None:edges.append((parent,idx,end-depth))
 groups={}
 for i in ids:
  if len(seq[i])==end:continue
  groups.setdefault(seq[i][end],[]).append(i)
 for group in groups.values():tree(group,end,idx)
 return idx
# append endpoints if identical prefixes would otherwise obscure a terminal leaf.
tree(list(range(4)),0)
f=plt.figure(figsize=(13,6.5));a=f.add_axes([.05,.14,.39,.73]);a.set(xlim=(-.3,4.7),ylim=(-.5,3.6));a.axis('off');a.set_title("compressed prefix tree, first 4 rounds",loc='left',fontsize=14)
levels={}
for i,n in enumerate(nodes):levels[i]=0 if n['parent'] is None else levels[n['parent']]+1
for parent,child,count in edges:
 x1=levels[parent];x2=levels[child];y1=3-nodes[parent]['y'];y2=3-nodes[child]['y'];a.plot([x1,x2],[y1,y2],color=C['line']);a.text((x1+x2)/2,(y1+y2)/2+.12,f'+{count}',fontsize=9,ha='center',bbox={'fc':'white','ec':'none','pad':1})
for i,n in enumerate(nodes):
 x=levels[i];y=3-n['y'];a.plot(x,y,'o',color=C['teal'],ms=8)
 if len(n['ids'])==1:a.text(x+.12,y,f"round {n['ids'][0]+1}：{n['depth']}",va='center',fontsize=10)
 elif n['parent'] is None:a.text(x-.08,y-.32,f"shared {n['depth']}",fontsize=10)
a.text(0,-.43,"edge: new tokens; leaf: total input tokens",fontsize=10)
a=f.add_axes([.56,.18,.40,.69]);common=[0]+[lcp([seq[i-1],seq[i]]) for i in range(1,len(seq))];lens=[len(s) for s in seq];a.bar(range(1,13),common,color=C['teal'],label="shared prefix with previous round");a.bar(range(1,13),np.array(lens)-common,bottom=common,color=C['orange'],label="remaining input");a.set(xticks=[1,3,6,9,12],xlabel="round",ylabel="input token count");a.set_title("12-round token matching [input analysis]",fontsize=12,loc='left');a.legend(fontsize=9,frameon=False)
data['prefix']={'tree':nodes,'edges':edges,'input_lengths':lens,'adjacent_lcp':common,'kind':'derived_token_identity_not_measured_hits'};save(f,'figure-8-6-prefix')
# 4. One relation: buffering changes the number of complete histories that fit.
f,a=canvas(6.5);a.text(.02,.94,"same 2592 MiB offloaded; buffer usage changes acceptable context count",fontsize=15,weight='bold')
scale=.74/2592
for y,buff,count in [(.66,288,2),(.29,576,1)]:
 x=.20;a.text(.02,y+.065,f'{buff//288} buffer groups',va='center',fontsize=12)
 a.add_patch(Rectangle((x,y),buff*scale,.13,fc=C['orange']));a.text(x+buff*scale/2,y+.065,str(buff),ha='center',va='center',color='white',fontsize=11)
 pos=x+buff*scale
 for i in range(count):
  a.add_patch(Rectangle((pos,y),1152*scale,.13,fc=C['teal'],ec='white',lw=2));a.text(pos+576*scale,y+.065,'8K KV：1152',ha='center',va='center',color='white',fontsize=12);pos+=1152*scale
 remaining=2592-buff-count*1152
 if remaining:
  a.add_patch(Rectangle((pos,y),remaining*scale,.13,fc=C['gray']));a.text(pos+remaining*scale/2,y+.065,f'remaining {remaining}',ha='center',va='center',fontsize=12)
 a.text(.20,y-.085,f'net space {2592-buff} MiB → {count} full contexts',fontsize=13,color=C['ink'])
a.text(.5,.04,"orange: prefetch buffer    green: full KV context    gray: remainder <1 (unit: MiB)",ha='center',fontsize=11)
data['offload']={'offload_gib':2.53125,'offload_bytes':2717908992,'buffer_gib':[.28125,.5625],'net_gib':[2.25,1.96875],'links':['PCIe Gen5 x16','GH200 NVLink-C2C'],'bandwidth_gb_s':[64,450],'copy_ms':[2717908992/64e9*1000,2717908992/450e9*1000],'results':['calculations/results/weight-offload-pcie5.json','calculations/results/weight-offload-gh200-c2c.json']}
from fractions import Fraction
for path,ms in zip(data['offload']['results'],data['offload']['copy_ms']):assert abs(float(Fraction(read(path)['summary']['per_forward_copy_service_ns_exact']))/1e6-ms)<1e-9
save(f,'figure-8-9-offload')
# Task-aligned quality comparison, with all four natural runs per task visible.
quality=read('experiments/ch08/08-08/results/summary.json');qcontrol=read('experiments/ch08/08-08/results/q-control-summary.json')
record_sets=[[r for r in c['requests'] if r['mode']=='natural' and r['trial']!='warm'] for c in quality['configurations']]+[[r for r in qcontrol['records'] if r['mode']=='natural']]
task_ids=sorted({r['task_id'] for r in record_sets[0]});cols=[(1,0),(1,1),(4,0),(4,1)];quality_matrices=[]
for records in record_sets:
 lookup={(r['task_id'],r['concurrency'],r['trial']):bool(r.get('strict_correct',r.get('correct'))) for r in records};assert len(lookup)==32
 quality_matrices.append([[int(lookup[(task,conc,trial)]) for conc,trial in cols] for task in task_ids])
correct=[int(np.array(m).sum()) for m in quality_matrices];assert correct==[28,26,28]
f,axs=plt.subplots(1,3,figsize=(12,6.8),sharey=True);f.subplots_adjust(left=.13,right=.97,bottom=.18,top=.88,wspace=.12)
from matplotlib.colors import ListedColormap
for a,m,title,total in zip(axs,quality_matrices,['BF16 KV',"original FP8 implementation",'FP8 KV ＋ BF16 Q'],correct):
 a.imshow(m,cmap=ListedColormap([C['red'],C['teal']]),vmin=0,vmax=1,aspect='auto');a.set(xticks=range(4),xticklabels=['1 / 1','1 / 2','4 / 1','4 / 2'],yticks=range(8),yticklabels=task_ids,xlabel="concurrency / repeat index");a.set_title(f'{title}\ncorrect {total}/32',fontsize=12)
 for yy,row in enumerate(m):
  for xx,val in enumerate(row):a.text(xx,yy,'○' if val else '×',ha='center',va='center',color='white',fontsize=16)
 a.set_xticks(np.arange(-.5,4,1),minor=True);a.set_yticks(np.arange(-.5,8,1),minor=True);a.grid(which='minor',color='white',lw=2);a.tick_params(which='minor',bottom=False,left=False)
axs[0].set_ylabel("task ID");f.text(.55,.035,"each cell: one natural generation; green ○ correct, red × wrong",ha='center',fontsize=11)
data['kv']={'format_mib':[1152,612,324],'quality_bf16_weights':correct,'total_executions_each':32,'unique_tasks':8,'task_ids':task_ids,'columns':cols,'correct_by_task':quality_matrices};save(f,'figure-8-10-kv-quality')
# 6. One relation: lookup cost can erase the benefit of additional outputs.
f,a=plt.subplots(figsize=(10,6));f.subplots_adjust(left=.11,right=.96,bottom=.14,top=.90)
T0=read('experiments/ch08/08-01/efficiency.json');T0=next(r['decode_round_ms'] for r in T0['rows'] if r['kind']=='short' and r['batch']==1);Q=.1
queries=np.linspace(0,60,121);vals=[];crosses=[]
for name,prob,col in [('AAAA',.25,'red'),('BBBB',.75,'teal')]:
 out=sum(prob**i for i in range(5));cost=(T0+Q)/out;vals.append({'draft':name,'acceptance':prob,'expected_output':out,'ms_per_output':cost});crosses.append(out*T0-T0)
 a.plot(queries,(queries+T0)/out,color=C[col],lw=2.5,label=f'{name}: avg output count {out:.2f} token/round')
 a.scatter([Q],[cost],color=C[col],s=40);a.annotate(f'{cost:.1f} ms/token',xy=(Q,cost),xytext=(3,cost-5),fontsize=11,color=C[col])
a.axhline(T0,color=C['ink'],ls='--',lw=1.4,label=f'normal decode:{T0:.1f} ms/token')
for x,col in zip(crosses,['red','teal']):
 a.scatter([x],[T0],color=C[col],s=45);a.annotate(f'query approx {x:.1f} ms',xy=(x,T0),xytext=(x+1.5,T0+6),arrowprops={'arrowstyle':'->','color':C[col]},fontsize=11)
a.set(xlabel="time per query round / ms",ylabel="avg time per output token / ms",xlim=(0,60),ylim=(0,70),xticks=[0,10,20,30,40,50,60]);a.grid(alpha=.2);a.legend(frameon=False,loc='upper left')
data['speculation']={'target_p_A':.25,'query_ms':Q,'verification_ms':T0,'ordinary_ms':T0,'device':'rtx-pro6000-blackwell-ws','source':'experiments/ch08/08-01/efficiency.json','drafts':vals,'query_break_even_ms':crosses};save(f,'figure-8-12-speculation')
# 7. Amdahl bound only; never filled with missing MiMo stage data.
f,a=plt.subplots(figsize=(10,5.8));f.subplots_adjust(left=.10,right=.95,bottom=.14,top=.89);ss=np.linspace(1,8,100)
for frac,col in [(.2,'blue'),(.5,'teal'),(.8,'orange')]:
 yy=1/(1-frac+frac/ss);a.plot(ss,yy,lw=2.4,color=C[col],label=f'decode share of baseline {int(frac*100)}%')
a.scatter([4],[1.6],color=C['teal']);a.annotate("local 4x → task 1.6x",xy=(4,1.6),xytext=(4.4,2.25),arrowprops={'arrowstyle':'->','color':C['teal']},fontsize=11);a.set(xlabel="decode local speedup",ylabel="full task speedup",xlim=(1,8),ylim=(1,3.8));a.grid(alpha=.2);a.legend(frameon=False,loc='upper left');a.set_title("other stages unchanged, no added cost [teaching upper bound]",loc='left',fontsize=13)
data['task']={'decode_fractions':[.2,.5,.8],'local_speedups':ss.tolist(),'speedups':[[float(1/(1-f+f/s)) for s in ss] for f in [.2,.5,.8]]};save(f,'figure-8-15-task')
# 8. All repetitions preserved; rates plotted categorically.
d=read('experiments/ch08/08-09/analysis.json');groups=d['groups'];order=[('serial',1),('serial',4),('serial',16),('continuous',1),('continuous',4),('continuous',16),('offline',None)]
print('Service groups:',sorted({(r['service'],str(r['rate'])) for r in groups}))
# Native labels are read, with aliases resolved explicitly below.
services=sorted(set(r['service'] for r in groups));print(services)
ordered=[]
for kind,rate in order:
 matches=[r for r in groups if r['service']==kind and (rate is None or r['rate']==rate)]
 if not matches:
  aliases={'continuous':['continuous','concurrent'],'offline':['offline','burst']}.get(kind,[kind]);matches=[r for r in groups if r['service'] in aliases and (rate is None or r['rate']==rate)]
 assert len(matches)==3,(kind,rate,[(r['service'],r['rate']) for r in groups]);ordered.append(matches)
f,a=plt.subplots(figsize=(12,6.5));f.subplots_adjust(left=.09,right=.97,bottom=.20,top=.91);labels=["one-by-one\n1/s","one-by-one\n4/s","one-by-one\n16/s","continuous\n1/s","continuous\n4/s","continuous\n16/s","offline\nburst"];xs=np.arange(7)
for key,offset,col,lab in [('completed_per_s',-.17,'blue',"completed throughput"),('slo_goodput_per_s',.17,'teal',"qualified throughput")]:
 vals=[[r[key] for r in g] for g in ordered];med=[np.median(v) for v in vals];a.bar(xs+offset,med,width=.30,color=C[col],alpha=.75,label=lab)
 for i,v in enumerate(vals):
  a.scatter(i+offset+np.array([-.05,0,.05]),v,s=20,color=C[col],edgecolors='white',linewidth=.4,zorder=4)
  a.text(i+offset,max(v)+.08,f'{med[i]:.2f}',ha='center',fontsize=10,color=C[col])
a.set(ylabel="window throughput / req/s",ylim=(0,3.1),yticks=[0,.5,1,1.5,2,2.5,3],xticks=xs,xticklabels=labels);a.legend(frameon=False,fontsize=11,loc='upper left');a.grid(axis='y',alpha=.15)
data['service']={'source':'experiments/ch08/08-09/analysis.json','groups':ordered,'correct':d['correct'],'qualified':d['qualified'],'requests':d['formal_requests']};save(f,'figure-8-13-service')
# Worked examples are recomputed first; the mechanism diagrams read their results.
subprocess.run([sys.executable,str(HERE/'teaching-check.py')],check=True,capture_output=True,text=True)
from illustrations import draw
draw(save, canvas, box, arrow, C, data)
(HERE/'figure-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n');(HERE/'figure-layout-check.json').write_text(json.dumps({'text_extent_warnings':warnings},ensure_ascii=False,indent=2)+'\n')
import sys
sys.path.insert(0,str(HERE.parent))
from teaching_revision import draw as draw_teaching
teaching_outputs,teaching_checks=draw_teaching(HERE,data)
outputs=list(dict.fromkeys(outputs+teaching_outputs))
# Offline HTML: render KaTeX locally and embed all image/font bytes.
md=HERE.parent/'08-推理优化.md';raw=md.read_text();maths=[]
def protect(m):
 t=m[0];display=t.startswith('$$');token=f'MATHPLACEHOLDER{len(maths)}END';maths.append({'latex':(t[2:-2] if display else t[1:-1]).strip(),'display':display,'token':token});return '\n\n'+token+'\n\n' if display else token
body=markdown.markdown(re.sub(r'\$\$[\s\S]*?\$\$|\$[^$\n]+\$',protect,raw),extensions=['tables','footnotes','fenced_code','toc'])
node="const fs=require('fs'),k=require(process.argv[1]);process.stdout.write(JSON.stringify(JSON.parse(fs.readFileSync(0,'utf8')).map(x=>k.renderToString(x.latex,{displayMode:x.display,throwOnError:true,output:'htmlAndMathml'}))))"
res=subprocess.run(['node','-e',node,str(HERE/'vendor/katex/katex.js')],input=json.dumps(maths),capture_output=True,text=True,check=True)
for entry,rendered in zip(maths,json.loads(res.stdout)):body=body.replace('<p>'+entry['token']+'</p>',rendered) if entry['display'] else body.replace(entry['token'],rendered)
mathcss=(HERE/'vendor/katex/katex.min.css').read_text()
def fonturl(m):
 p=HERE/'vendor/katex'/m[1];return 'url(data:font/'+p.suffix[1:]+';base64,'+base64.b64encode(p.read_bytes()).decode()+')'
mathcss=re.sub(r'url\((fonts/[^)]+)\)',fonturl,mathcss)
body=re.sub(r'<table>(.*?)</table>',r'<div class="table-scroll"><table>\1</table></div>',body,flags=re.S)
for p in outputs:
 if p.suffix=='.svg':body=body.replace('src="ch08/'+p.name+'"','src="data:image/png;base64,'+base64.b64encode(p.with_suffix('.png').read_bytes()).decode()+'"')
css=(HERE/'reading.css').read_text();nav=''.join('<a href="#'+i+'">'+t+'</a>' for i,t in re.findall(r'<h2 id="([^"]+)">(8\.\d+ [^<]+)</h2>',body))
page="<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Chapter 8 Inference Optimization</title><style>"+css+mathcss+"</style></head><body><main><nav aria-label=\"Chapter contents\">"+nav+'</nav>'+body+'</main></body></html>';hp=preview_path(md)
zoom="<dialog id=\"figure-view\" aria-label=\"enlarge figure\"><button id=\"close-figure\" type=\"button\">close</button><div id=\"figure-content\"></div></dialog><script>\nconst view=document.getElementById('figure-view'),content=document.getElementById('figure-content');\nfor(const img of document.querySelectorAll('main img')){img.tabIndex=0;img.setAttribute('role','button');img.setAttribute('aria-label',img.alt+', click to enlarge');const show=()=>{content.replaceChildren(img.cloneNode());content.firstChild.removeAttribute('role');content.firstChild.removeAttribute('tabindex');view.showModal();};img.addEventListener('click',show);img.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();show();}});}\ndocument.getElementById('close-figure').onclick=()=>view.close();view.addEventListener('close',()=>content.replaceChildren());\n</script>"
page=page.replace('</body>',zoom+'</body>')
import sys
sys.path.insert(0,str(HERE.parent))
from teaching_reading import readable_diagrams
page=readable_diagrams(page)
hp.write_text(page)
(HERE/'math-validation.json').write_text(json.dumps({'renderer':'KaTeX 0.16.11','expressions':len(maths),'display_expressions':sum(x['display'] for x in maths),'errors':[]},indent=2)+'\n')
from book_assets import sync_figure_index
active_assets=sync_figure_index(HERE)
artifacts=outputs+[HERE/'teaching_revision.py',HERE/'figure-index.json',HERE/'teaching-layout-validation.json',HERE/'figure-data.json',md,hp]+active_assets
(HERE/'manifest.json').write_text(json.dumps({'chapter':8,'generator':'manuscripts/ch08/build.py','figures':len(outputs)//3,'font_family':family,'outputs':[{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in artifacts if not (p.parent==ROOT/'manuscripts' and re.match(r'^[01][0-9]-',p.name))]},ensure_ascii=False,indent=2)+'\n')
print(f'Built {len(outputs)} images; {len(maths)} formulas; {len(warnings)} extent warnings.')
