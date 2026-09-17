"""Figures for the book's three principles; use the existing book-size exporter."""
import matplotlib.pyplot as plt
import numpy as np
from figure_style import COL, STYLE, canvas, plot, text, box, arrow

W = 15136811008
WEIGHTS = 16381470720
K = 2 * 36 * 8 * 128 * 2 * 8192
WORKSPACE = 2 * 2**30
CAPACITY = 24 * 10**9

def draw(chapter, out):
    with plt.rc_context(STYLE):
        if chapter == 1:
            f,a=canvas(5.2)
            text(a,.25,.94,"traditional application",14,ha='center');text(a,.75,.94,"model-driven application",14,ha='center')
            for x,labels in [(.03,[("code and data",'orange'),("compiler and OS",'purple'),("execution of program instructions",'green'),("processor, memory, and interconnect",'blue')]),(.54,[('Agent','orange'),("model interface",'purple'),("compute output, save context state",'green'),("Accelerator, Memory, and Interconnect",'blue')])]:
                for i,(label,c) in enumerate(labels):
                    y=.73-i*.18;box(a,x,y,.43,.12,label,c)
                    if i<3:arrow(a,(x+.215,y),(x+.215,y-.06))
            arrow(a,(.54,.79),(.46,.61),kind='control')
            text(a,.5,.065,"tool programs still executed by OS",12,ha='center')
            out.save(f,'figure-1-programmability')
        if chapter == 2:
            f,a=plot(3.8,left=.08,bottom=.22)
            vals=[4*K/1e9,WORKSPACE/1e9,(CAPACITY-4*K-WORKSPACE)/1e9]
            left=0
            for v,c in zip(vals,['green','gray','blue']):
                a.barh(.5,v,left=left,height=.24,color=COL[c],edgecolor=COL['line']);left+=v
            a.set(xlim=(0,24),ylim=(0,1.45),yticks=[],xticks=[0,4,8,12,16,20,24],xlabel="RTX 4090 24 GB capacity allocation (GB)")
            for x,y,label,target in [(2.4,1.20,"4 request KV\n4.83 GB",2.4),(7,.95,"workspace\n2.15 GB",5.9),(16,1.20,"weight remainder\n17.02 GB",15.5)]:
                a.annotate(label,xy=(target,.64),xytext=(x,y),ha='center',va='center',fontsize=12,arrowprops=dict(arrowstyle='-',color=COL['line']))
            a.text(12,.14,"BF16 parameter upper bound ≈ 8.51B",ha='center',fontsize=13)
            out.save(f,'figure-2-reverse-budget')
        if chapter == 4:
            f,a=canvas(4.8)
            rows=[("existing accelerator","capacity, bandwidth, interconnect",'blue'),("model and software choices","compression, tiling, parallelism",'green'),("persistent execution bottleneck","shapes next-gen hardware requirements",'orange'),("new accelerators and candidates","re-compare model architectures",'purple')]
            for i,(title,desc,c) in enumerate(rows):
                y=.76-i*.22
                box(a,.06,y,.88,.16,title+'\n'+desc,c)
                if i<3:arrow(a,(.50,y),(.50,y-.06))
            out.save(f,'figure-4-codesign-loop')
            f,a=canvas(4.5)
            text(a,.04,.94,"shared interface for weights and state",14)
            box(a,.04,.66,.39,.18,"HBM\nweights + KV",'blue');box(a,.66,.66,.30,.18,"compute",'orange')
            arrow(a,(.43,.75),(.66,.75));text(a,.54,.59,'W + BK',12,ha='center')
            text(a,.04,.46,"dedicated read-only weight path",14)
            box(a,.04,.25,.39,.13,"ROM: weights W",'blue');box(a,.04,.04,.39,.13,"HBM: KV state BK",'green')
            box(a,.66,.13,.30,.20,"compute",'orange')
            arrow(a,(.43,.315),(.66,.27));arrow(a,(.43,.105),(.66,.19))
            out.save(f,'figure-4-rom-paths')
        if chapter == 8:
            f,a=plot(3.8,left=.16,bottom=.19)
            b=np.arange(1,33)
            a.plot(b,(W/b+K)/1e9,color='#527fa0',lw=2,label="traditional HBM: W/B + K")
            a.plot(b,np.full_like(b,K,dtype=float)/1e9,color='#48826b',lw=2,label="dedicated ROM: K")
            for batch in [1,16]:
                v=(W/batch+K)/1e9;a.scatter([batch],[v],color='#527fa0',s=22)
                a.annotate(f'{v:.2f} GB',(batch,v),xytext=(8,2),textcoords='offset points',fontsize=11)
            a.set(xlim=(0,33),ylim=(0,20),xticks=[1,8,16,24,32],xlabel='batch size B',ylabel="HBM reads per output token (GB)")
            a.legend(frameon=False,loc='upper right');out.save(f,'figure-8-batch-counterfactual')
            f,a=canvas(4.2)
            rows=[(.72,"append",[(8,"8K reuse",'blue'),(1,'','orange')]),(.43,"rewrite beginning",[(9,"9K reprocessing",'orange')]),(.14,"summarize history",[(2,'2K','orange'),(1,'1K','orange')])]
            for y,label,segments in rows:
                text(a,.03,y+.06,label,12)
                x=.26
                for length,lab,col in segments:
                    width=length*.073
                    box(a,x,y,width,.13,lab,col);x+=width
                if label=='追加':text(a,x-.0365,y-.065,"1K new",11,ha='center')
                if label=='总结历史':text(a,.61,y+.065,"summary work counted separately",11)
            text(a,.5,.96,"same history, three update methods",14,ha='center')
            out.save(f,'figure-8-context-edits')
        if chapter == 10:
            f,a=canvas(4.2)
            text(a,.04,.94,"fixed-version serving",14)
            box(a,.04,.67,.38,.17,"ROM\nweights v0",'blue');box(a,.64,.67,.32,.17,"generation\nwritable KV",'green');arrow(a,(.42,.755),(.64,.755))
            text(a,.04,.48,"continuously updated policy",14)
            box(a,.04,.19,.25,.18,"training\nupdate parameters",'orange');box(a,.39,.19,.25,.18,"writable weights\nv0 → v1",'blue');box(a,.74,.19,.23,.18,"generation\nusing v1",'green')
            arrow(a,(.29,.28),(.39,.28));arrow(a,(.64,.28),(.74,.28))
            text(a,.5,.065,"publish weights after update, keep version consistent",12,ha='center');out.save(f,'figure-10-weight-update')
        if chapter == 11:
            f,a=plot(4.4,left=.24,bottom=.17)
            cold=2+2**31/(25e9/8)
            for y,v,c in [(4,6,'blue'),(3,cold,'green'),(1,1,'blue'),(0,cold,'green')]:a.barh(y,v,height=.55,color=COL[c],edgecolor=COL['line']);a.text(v+.13,y,f'{v:.1f} s' if v!=int(v) else f'{int(v)} s',va='center',fontsize=11)
            a.axhline(2.2,color=COL['line'],lw=.7)
            a.annotate('',xy=(cold,1.5),xytext=(1,1.5),arrowprops=dict(arrowstyle='<->',color=COL['line']));a.text(3.6,1.62,f'extra wait ~ {cold-1:.1f} s',ha='left',fontsize=11)
            a.set(yticks=[4,3,1,0],yticklabels=["fast serving","cold-path creation","accelerated model","cold-path creation"],xlim=(0,8),ylim=(-.65,4.7),xlabel="timer starts at model (s)")
            out.save(f,'figure-11-environment-overlap')
        if chapter == 12:
            f,a=plot(3.5,left=.24,bottom=.21)
            for y,v in [(2,8),(1,.8),(0,0)]:
                a.barh(y,v,height=.55,color=COL['blue'],edgecolor=COL['line'],label="model" if y==2 else None)
                a.barh(y,2,left=v,height=.55,color=COL['orange'],edgecolor=COL['line'],label="other serial stages" if y==2 else None)
                a.text(v+2+.12,y,f'{v+2:g} s',va='center',fontsize=12)
            a.set(yticks=[2,1,0],yticklabels=["original task","model 10x faster","ideal lower bound"],xlim=(0,12),ylim=(-.7,3),xlabel="complete task time (s)");f.subplots_adjust(top=.84);a.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.45,1.17),columnspacing=1.5,handlelength=1.4)
            out.save(f,'figure-12-task-counterfactual')
