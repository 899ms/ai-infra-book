"""Teaching figures: stage order, resource occupancy, and cost composition."""
import numpy as np
import matplotlib.pyplot as plt
from fractions import Fraction

def draw(save, C, data, canvas, box, arrow, design, lifecycle):
    def chart(height=4.8,left=.19):
        f,a=plt.subplots(figsize=(11,height));f.subplots_adjust(left=left,right=.93,bottom=.19,top=.87)
        a.grid(axis='x',alpha=.15);a.set_axisbelow(True)
        return f,a
    def done(f,key,values):
        save(f,'figure-11-'+key);data[key]=values
    # Same workload, different limiting resource.
    f,a=chart();labels=["CPU core count","concurrent model calls","memory / GiB"];mem=384e9/2**30;before=[30/48,270/320,600/mem];after=[30/48,360/320,780/mem]
    y=np.arange(3)
    a.barh(y+.18,np.array(before)*100,.30,color=C['blue'],label="each model call 9 s")
    a.barh(y-.18,np.array(after)*100,.30,color=C['orange'],label="each model call 12 s")
    for i,(v,w) in enumerate(zip(before,after)):
        a.text(v*100+1,i+.18,['30 / 48','270 / 320','600 / 358'][i],va='center',fontsize=11)
        a.text(w*100+1,i-.18,['30 / 48','360 / 320','780 / 358'][i],va='center',fontsize=11)
    a.axvline(100,color=C['red'],ls='--');a.set(yticks=y,yticklabels=labels,xlim=(0,250),xlabel="demand / capacity (%)");a.invert_yaxis();a.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2,frameon=False)
    done(f,'capacity',{'demand_9':[30,270,600],'demand_12':[30,360,780],'capacity':[48,320,mem],'capacity_labels':['48','320','358']})
    # Page footprint: common horizontal scale reveals replicated bytes.
    f,a=chart();parts=[[2048,0,4],[512,0,4],[0,128,4],[256,128,4]];colors=[C['blue'],C['orange'],C['teal']]
    for i,row in enumerate(parts):
        start=0
        for v,c in zip(row,colors):a.barh(i,v,left=start,color=c,height=.52);start+=v
        a.text(start+25,i,f'{sum(row):,} MiB',va='center')
    a.set(yticks=range(4),yticklabels=["full replication","load accessed content only","shared read-only content","shared + retained common pages"],xlim=(0,2440),xlabel="data saved locally per environment / MiB");a.invert_yaxis()
    for c,l in zip(colors,["local content","private modified pages","management overhead"]):a.plot([],[],color=c,lw=8,label=l)
    a.legend(frameon=False,loc='lower right');done(f,'pages',{'local_mib':[sum(x) for x in parts],'shared_template_mib':2048})
    # Pause one gap; memory area is the central relationship.
    f,a=chart();a.broken_barh([(10,9)],(1.1,.5),facecolors=C['blue']);a.text(14.5,1.35,'2 GiB × 9 s = 18 GiB·s',ha='center',va='center',color='white')
    a.broken_barh([(10,8),(18,1)],(.1,.5),facecolors=C['teal']);a.text(14,.8,"save 2 GiB × 4 s/GiB",ha='center');a.text(18.5,.8,"recovery",ha='center');a.text(14,.35,"time without memory release",ha='center',color='white')
    a.set(yticks=[1.35,.35],yticklabels=["continuous retention","resume after pause"],xlim=(10,19),ylim=(-.25,2),xticks=range(10,20),xlabel="time since task start / s")
    a.text(14.5,1.8,"second tool round starts at 19 s, same for both schemes",ha='center');done(f,'pause',{'gap':[10,19],'resident_gib_seconds':18,'pause_seconds_per_gib':4,'resume_seconds':1,'paused_gib_seconds':2*(2*4+1),'source':'references/outline-checks/2026-09-07/platform-routing/e2b-persistence.md'})
    # Entire task memory occupied only in prep/tool phases.
    f,a=chart();a.broken_barh([(0,30)],(1.25,.5),facecolors=C['blue']);a.text(15,1.5,'60 GiB·s',ha='center',va='center',color='white')
    for start in [7,17,27]:
        a.broken_barh([(start,2)],(.25,.5),facecolors=C['teal']);a.broken_barh([(start+2,1)],(.25,.5),facecolors=C['orange'])
    a.set(yticks=[1.5,.5],yticklabels=["environment retained throughout","rebuild environment each round"],xlim=(0,30),ylim=(-.2,2.2),xticks=[0,7,9,10,17,19,20,27,29,30],xlabel="time since task start / s")
    a.text(15,1,"three segments each 2 GiB × 3 s, total 18 GiB·s",ha='center',fontsize=12)
    for c,l in [(C['teal'],"prepare environment"),(C['orange'],"run tool")]:a.plot([],[],color=c,lw=8,label=l)
    a.legend(loc='upper left',bbox_to_anchor=(0,1.15),ncol=2,frameon=False);done(f,'residency',{'preparation_starts':[7,17,27],'gib_seconds':[60,18]})
    # Bursts queue despite identical service work.
    f,axes=plt.subplots(1,2,figsize=(11,5),sharey=True);f.subplots_adjust(left=.09,right=.97,top=.84,bottom=.16,wspace=.15)
    for a,burst in zip(axes,[False,True]):
        for i in range(10):
            if burst and i:a.barh(i,i,left=0,color=C['gray'],height=.65)
            a.barh(i,1,left=i,color=C['blue'],height=.65);a.plot(0 if burst else i,i,'o',color=C['red'],ms=4)
        a.set(xlim=(-.3,10),ylim=(9.7,-.8),yticks=range(10),yticklabels=range(1,11),xlabel="time / s");a.grid(axis='x',alpha=.15);a.set_title("simultaneous arrival: avg wait 4.5 s" if burst else "one arrival per second: no wait")
    axes[0].set_ylabel("task ID");axes[1].plot([],[],'o',color=C['red'],label="arrival");axes[1].plot([],[],color=C['gray'],lw=8,label="Queueing");axes[1].plot([],[],color=C['blue'],lw=8,label="execution");axes[1].legend(ncol=3,frameon=False,loc='lower center',bbox_to_anchor=(.5,1.08))
    done(f,'queue',{'service_seconds':[1]*10,'arrival_even':list(range(10)),'arrival_burst':[0]*10,'start':list(range(10))})
    # Amdahl visible as unchanged blocks.
    f,a=chart();rows=[[40,10,30,5],[20,10,30,5]];colors=[C['blue'],C['orange'],C['teal'],C['muted']]
    for i,row in enumerate(rows):
        left=0
        for j,(v,c) in enumerate(zip(row,colors)):
            a.barh(i,v,left=left,color=c,height=.5);a.text(left+v/2,i,str(v),ha='center',va='center',color='white');left+=v
        a.text(left+1,i,f'total {left} s',va='center')
    for c,l in zip(colors,["generation","Verification","update","release"]):a.plot([],[],color=c,lw=8,label=l)
    a.set(yticks=[0,1],yticklabels=["original config","generation speed doubled"],xlim=(0,100),xlabel="time per round / s");a.invert_yaxis();a.legend(ncol=4,frameon=False,loc='lower center',bbox_to_anchor=(.5,1.03))
    done(f,'rl-stages',{'stage_seconds':rows})
    # Shared network link is a physical constriction.
    f,a=canvas(5.7);box(a,.02,.38,.22,.24,"training instance",'Qwen3-8B 16.38 GB');box(a,.32,.38,.23,.24,"shared egress",'200 Gbit/s','sand');arrow(a,(.24,.5),(.32,.5))
    for i,y in enumerate([.80,.47,.14]):
        box(a,.74,y-.08,.23,.19,f'receiving instance {i*2+1}、{i*2+2}',"each receives 16.38 GB",size=12);arrow(a,(.55,.5),(.73,y+.015))
    a.text(.62,.93,"6 instances, 50 Gbit/s each",ha='center',fontsize=13)
    a.text(.40,.22,"egress total 6 × 16.38 ≈ 98.3 GB",ha='center',fontsize=13)
    a.text(.40,.12,"at least 3.93 s to finish transfer",ha='center',fontsize=15,weight='bold')
    done(f,'weights',{'weight_bytes':16381470720,'receivers':6,'sender_gbps':200,'receiver_gbps':50,'lower_seconds':6*16381470720*8/200e9})
    # Cost composition preserves the fixed portion.
    f,a=chart();rows=[[.020,.010,.002],[.020,.001,.002]];colors=[C['blue'],C['orange'],C['teal']]
    for i,row in enumerate(rows):
        left=0
        for v,c in zip(row,colors):a.barh(i,v,left=left,color=c,height=.5);left+=v
        a.text(left+.0005,i,f'{left:.3f}',va='center')
    for c,l in zip(colors,["input 0.020","thinking 0.010 → 0.001","visible output 0.002"]):a.plot([],[],color=c,lw=8,label=l)
    a.set(yticks=[0,1],yticklabels=["thinking 1,000 tokens","thinking 100 tokens"],xlim=(0,.038),xlabel="cost per call / USD");a.invert_yaxis();a.legend(frameon=False,loc='lower center',bbox_to_anchor=(.5,1.02),ncol=3,fontsize=10)
    done(f,'thinking',{'cost_parts':rows})
    # Fixed intercept and marginal slope.
    fixed=4*720*6.79;per=3*1.125*8.64/3600;cap=32*720*3600/27;cross=fixed/per
    f,a=chart(left=.12);n=np.linspace(0,cap,201);a.plot(n/1e4,np.full_like(n,fixed),label="reserved 4x B200: $19,555.2/month",color=C['blue']);m=np.linspace(0,3.2e6,201);a.plot(m/1e4,per*m,label="pay-as-you-go: $0.0081N",color=C['orange'])
    a.scatter([cross/1e4],[fixed],color=C['teal']);a.axvline(cross/1e4,color=C['muted'],ls='--',lw=1);a.annotate("cost equal at ≈2.41M items",(cross/1e4,fixed),(60,23000),arrowprops={'arrowstyle':'->','color':C['muted']});a.set(xlabel="Monthly submitted tasks / 10k",ylabel="Monthly total cost / USD",xlim=(0,320),ylim=(0,27000),xticks=range(0,301,50));a.legend(frameon=False,loc='upper left')
    done(f,'purchase',{'fixed':fixed,'self_per_task':0,'api_per_task':per,'capacity':cap,'crossover':cross,'reserved_usd_per_gpu_hour':6.79,'on_demand_usd_per_gpu_hour':8.64,'source':'experiments/ch13/13-06/single-agent-serving/comparison-sources/gpu-prices.md'})
    # Six terminal paths with time and deadline, linked to probability tree.
    f,a=canvas(7);box(a,.01,.40,.18,.19,"first attempt","10 s; cost 0.010",size=12)
    box(a,.33,.64,.20,.17,"local repair","plus 4 s; 0.006",size=12)
    box(a,.33,.20,.20,.17,"direct upgrade","plus 8 s; 0.030",size=12)
    box(a,.66,.89,.31,.09,"first success: 80% · 10 s",color='green',size=12)
    box(a,.66,.72,.31,.09,"repair success: 7.2% · 14 s",color='green',size=12)
    box(a,.66,.49,.31,.14,"upgrade after repair: 22 s","success 4.704%; failure 0.096%",'sand',12)
    box(a,.66,.17,.31,.14,"direct upgrade: 18 s","success 7.84%; failure 0.16%",'green',12)
    for p,q in [((.19,.5),(.33,.72)),((.19,.46),(.33,.28)),((.53,.76),(.66,.76)),((.53,.69),(.66,.56)),((.53,.28),(.66,.24))]:arrow(a,p,q)
    a.plot([.10,.10,.63],[.59,.935,.935],color=C['teal'],lw=1.7);arrow(a,(.63,.935),(.66,.935));a.text(.20,.95,'80%',fontsize=11)
    a.text(.24,.66,'12%',fontsize=11);a.text(.24,.31,'8%',fontsize=11);a.text(.56,.80,'60%',fontsize=11);a.text(.55,.62,'40%',fontsize=11)
    a.text(.81,.42,"exceeds 20 s deadline",ha='center',color=C['red'],fontsize=12)
    a.text(.5,.055,"repair-then-upgrade adds a step; even success arrives late",ha='center',fontsize=14)
    done(f,'retry-tree',{'terminal_probabilities':['.8','.072','.04704','.00096','.0784','.0016'],'terminal_seconds':[10,14,22,22,18,18]})
    # Final decision ties back to initial trace.
    f,a=chart();rows=[("standard model",9),("fast model",6)]
    for i,(label,m) in enumerate(rows):
        for r in range(3):
            st=r*(m+1);a.barh(i,m,left=st,color=C['blue'],height=.5);a.barh(i,1,left=st+m,color=C['orange'],height=.5)
        a.text(3*(m+1)+.4,i,f'{3*(m+1)} s',va='center')
    a.axvline(24,color=C['red'],ls='--');a.text(24,-.52,"24 s deadline",ha='center',color=C['red']);a.set(yticks=[0,1],yticklabels=[x[0] for x in rows],xlim=(0,33),ylim=(1.6,-.8),xlabel="time since task start / s")
    for c,l in [(C['blue'],"model call"),(C['orange'],"tool execution")]:a.plot([],[],color=c,lw=8,label=l)
    a.legend(frameon=False,loc='lower right');done(f,'decision',{'model_seconds':[9,6],'task_seconds':[30,21],'deadline':24})
