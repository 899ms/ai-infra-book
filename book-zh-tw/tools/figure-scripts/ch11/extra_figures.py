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
    f,a=chart();labels=["CPU 核數","併發模型呼叫數","記憶體 / GiB"];mem=384e9/2**30;before=[30/48,270/320,600/mem];after=[30/48,360/320,780/mem]
    y=np.arange(3)
    a.barh(y+.18,np.array(before)*100,.30,color=C['blue'],label="每次模型呼叫 9 s")
    a.barh(y-.18,np.array(after)*100,.30,color=C['orange'],label="每次模型呼叫 12 s")
    for i,(v,w) in enumerate(zip(before,after)):
        a.text(v*100+1,i+.18,['30 / 48','270 / 320','600 / 358'][i],va='center',fontsize=11)
        a.text(w*100+1,i-.18,['30 / 48','360 / 320','780 / 358'][i],va='center',fontsize=11)
    a.axvline(100,color=C['red'],ls='--');a.set(yticks=y,yticklabels=labels,xlim=(0,250),xlabel="需求 / 容量（%）");a.invert_yaxis();a.legend(loc='lower center',bbox_to_anchor=(.5,1.02),ncol=2,frameon=False)
    done(f,'capacity',{'demand_9':[30,270,600],'demand_12':[30,360,780],'capacity':[48,320,mem],'capacity_labels':['48','320','358']})
    # Page footprint: common horizontal scale reveals replicated bytes.
    f,a=chart();parts=[[2048,0,4],[512,0,4],[0,128,4],[256,128,4]];colors=[C['blue'],C['orange'],C['teal']]
    for i,row in enumerate(parts):
        start=0
        for v,c in zip(row,colors):a.barh(i,v,left=start,color=c,height=.52);start+=v
        a.text(start+25,i,f'{sum(row):,} MiB',va='center')
    a.set(yticks=range(4),yticklabels=["完整複製","僅載入存取內容","共享只讀內容","共享＋保留常用頁"],xlim=(0,2440),xlabel="每個環境在本地儲存的資料 / MiB");a.invert_yaxis()
    for c,l in zip(colors,["本地內容","私有修改頁","管理開銷"]):a.plot([],[],color=c,lw=8,label=l)
    a.legend(frameon=False,loc='lower right');done(f,'pages',{'local_mib':[sum(x) for x in parts],'shared_template_mib':2048})
    # Pause one gap; memory area is the central relationship.
    f,a=chart();a.broken_barh([(10,9)],(1.1,.5),facecolors=C['blue']);a.text(14.5,1.35,'2 GiB × 9 s = 18 GiB·s',ha='center',va='center',color='white')
    a.broken_barh([(10,8),(18,1)],(.1,.5),facecolors=C['teal']);a.text(14,.8,"儲存 2 GiB × 4 s/GiB",ha='center');a.text(18.5,.8,"恢復",ha='center');a.text(14,.35,"沒有釋放記憶體的時間",ha='center',color='white')
    a.set(yticks=[1.35,.35],yticklabels=["持續保留","暫停後恢復"],xlim=(10,19),ylim=(-.25,2),xticks=range(10,20),xlabel="任務開始後的時間 / s")
    a.text(14.5,1.8,"第二輪工具在第 19 秒開始，兩種方案相同",ha='center');done(f,'pause',{'gap':[10,19],'resident_gib_seconds':18,'pause_seconds_per_gib':4,'resume_seconds':1,'paused_gib_seconds':2*(2*4+1),'source':'references/outline-checks/2026-09-07/platform-routing/e2b-persistence.md'})
    # Entire task memory occupied only in prep/tool phases.
    f,a=chart();a.broken_barh([(0,30)],(1.25,.5),facecolors=C['blue']);a.text(15,1.5,'60 GiB·s',ha='center',va='center',color='white')
    for start in [7,17,27]:
        a.broken_barh([(start,2)],(.25,.5),facecolors=C['teal']);a.broken_barh([(start+2,1)],(.25,.5),facecolors=C['orange'])
    a.set(yticks=[1.5,.5],yticklabels=["全程保留環境","每輪重建環境"],xlim=(0,30),ylim=(-.2,2.2),xticks=[0,7,9,10,17,19,20,27,29,30],xlabel="任務開始後的時間 / s")
    a.text(15,1,"三段各佔 2 GiB × 3 s，合計 18 GiB·s",ha='center',fontsize=12)
    for c,l in [(C['teal'],"準備環境"),(C['orange'],"執行工具")]:a.plot([],[],color=c,lw=8,label=l)
    a.legend(loc='upper left',bbox_to_anchor=(0,1.15),ncol=2,frameon=False);done(f,'residency',{'preparation_starts':[7,17,27],'gib_seconds':[60,18]})
    # Bursts queue despite identical service work.
    f,axes=plt.subplots(1,2,figsize=(11,5),sharey=True);f.subplots_adjust(left=.09,right=.97,top=.84,bottom=.16,wspace=.15)
    for a,burst in zip(axes,[False,True]):
        for i in range(10):
            if burst and i:a.barh(i,i,left=0,color=C['gray'],height=.65)
            a.barh(i,1,left=i,color=C['blue'],height=.65);a.plot(0 if burst else i,i,'o',color=C['red'],ms=4)
        a.set(xlim=(-.3,10),ylim=(9.7,-.8),yticks=range(10),yticklabels=range(1,11),xlabel="時間 / s");a.grid(axis='x',alpha=.15);a.set_title("同時到達：平均等待 4.5 s" if burst else "每秒到達一項：無需等待")
    axes[0].set_ylabel("任務編號");axes[1].plot([],[],'o',color=C['red'],label="到達");axes[1].plot([],[],color=C['gray'],lw=8,label="排隊");axes[1].plot([],[],color=C['blue'],lw=8,label="執行");axes[1].legend(ncol=3,frameon=False,loc='lower center',bbox_to_anchor=(.5,1.08))
    done(f,'queue',{'service_seconds':[1]*10,'arrival_even':list(range(10)),'arrival_burst':[0]*10,'start':list(range(10))})
    # Amdahl visible as unchanged blocks.
    f,a=chart();rows=[[40,10,30,5],[20,10,30,5]];colors=[C['blue'],C['orange'],C['teal'],C['muted']]
    for i,row in enumerate(rows):
        left=0
        for j,(v,c) in enumerate(zip(row,colors)):
            a.barh(i,v,left=left,color=c,height=.5);a.text(left+v/2,i,str(v),ha='center',va='center',color='white');left+=v
        a.text(left+1,i,f'合計 {left} s',va='center')
    for c,l in zip(colors,["生成","驗證","更新","釋出"]):a.plot([],[],color=c,lw=8,label=l)
    a.set(yticks=[0,1],yticklabels=["原設定","生成速度加倍"],xlim=(0,100),xlabel="每輪時間 / s");a.invert_yaxis();a.legend(ncol=4,frameon=False,loc='lower center',bbox_to_anchor=(.5,1.03))
    done(f,'rl-stages',{'stage_seconds':rows})
    # Shared network link is a physical constriction.
    f,a=canvas(5.7);box(a,.02,.38,.22,.24,"訓練實例",'Qwen3-8B 16.38 GB');box(a,.32,.38,.23,.24,"共享傳送出口",'200 Gbit/s','sand');arrow(a,(.24,.5),(.32,.5))
    for i,y in enumerate([.80,.47,.14]):
        box(a,.74,y-.08,.23,.19,f'接收實例 {i*2+1}、{i*2+2}',"各接收 16.38 GB",size=12);arrow(a,(.55,.5),(.73,y+.015))
    a.text(.62,.93,"6 個實例，各 50 Gbit/s",ha='center',fontsize=13)
    a.text(.40,.22,"出口累計傳送 6 × 16.38 ≈ 98.3 GB",ha='center',fontsize=13)
    a.text(.40,.12,"全部傳完至少 3.93 s",ha='center',fontsize=15,weight='bold')
    done(f,'weights',{'weight_bytes':16381470720,'receivers':6,'sender_gbps':200,'receiver_gbps':50,'lower_seconds':6*16381470720*8/200e9})
    # Cost composition preserves the fixed portion.
    f,a=chart();rows=[[.020,.010,.002],[.020,.001,.002]];colors=[C['blue'],C['orange'],C['teal']]
    for i,row in enumerate(rows):
        left=0
        for v,c in zip(row,colors):a.barh(i,v,left=left,color=c,height=.5);left+=v
        a.text(left+.0005,i,f'{left:.3f}',va='center')
    for c,l in zip(colors,["輸入 0.020","思考 0.010 → 0.001","可見輸出 0.002"]):a.plot([],[],color=c,lw=8,label=l)
    a.set(yticks=[0,1],yticklabels=["思考 1,000 token","思考 100 token"],xlim=(0,.038),xlabel="每次呼叫成本 / 美元");a.invert_yaxis();a.legend(frameon=False,loc='lower center',bbox_to_anchor=(.5,1.02),ncol=3,fontsize=10)
    done(f,'thinking',{'cost_parts':rows})
    # Fixed intercept and marginal slope.
    fixed=4*720*6.79;per=3*1.125*8.64/3600;cap=32*720*3600/27;cross=fixed/per
    f,a=chart(left=.12);n=np.linspace(0,cap,201);a.plot(n/1e4,np.full_like(n,fixed),label="預留 4 張 B200：19,555.2 美元/月",color=C['blue']);m=np.linspace(0,3.2e6,201);a.plot(m/1e4,per*m,label="按量：0.0081N 美元",color=C['orange'])
    a.scatter([cross/1e4],[fixed],color=C['teal']);a.axvline(cross/1e4,color=C['muted'],ls='--',lw=1);a.annotate("約 241 萬項時成本相等",(cross/1e4,fixed),(60,23000),arrowprops={'arrowstyle':'->','color':C['muted']});a.set(xlabel="每月提交任務數 / 萬項",ylabel="每月總成本 / 美元",xlim=(0,320),ylim=(0,27000),xticks=range(0,301,50));a.legend(frameon=False,loc='upper left')
    done(f,'purchase',{'fixed':fixed,'self_per_task':0,'api_per_task':per,'capacity':cap,'crossover':cross,'reserved_usd_per_gpu_hour':6.79,'on_demand_usd_per_gpu_hour':8.64,'source':'experiments/ch13/13-06/single-agent-serving/comparison-sources/gpu-prices.md'})
    # Six terminal paths with time and deadline, linked to probability tree.
    f,a=canvas(7);box(a,.01,.40,.18,.19,"首次嘗試","10 s；成本 0.010",size=12)
    box(a,.33,.64,.20,.17,"區域性修復","再用 4 s；0.006",size=12)
    box(a,.33,.20,.20,.17,"直接升級","再用 8 s；0.030",size=12)
    box(a,.66,.89,.31,.09,"首次成功：80% · 10 s",color='green',size=12)
    box(a,.66,.72,.31,.09,"修復成功：7.2% · 14 s",color='green',size=12)
    box(a,.66,.49,.31,.14,"修復後升級：22 s","成功 4.704%；失敗 0.096%",'sand',12)
    box(a,.66,.17,.31,.14,"直接升級：18 s","成功 7.84%；失敗 0.16%",'green',12)
    for p,q in [((.19,.5),(.33,.72)),((.19,.46),(.33,.28)),((.53,.76),(.66,.76)),((.53,.69),(.66,.56)),((.53,.28),(.66,.24))]:arrow(a,p,q)
    a.plot([.10,.10,.63],[.59,.935,.935],color=C['teal'],lw=1.7);arrow(a,(.63,.935),(.66,.935));a.text(.20,.95,'80%',fontsize=11)
    a.text(.24,.66,'12%',fontsize=11);a.text(.24,.31,'8%',fontsize=11);a.text(.56,.80,'60%',fontsize=11);a.text(.55,.62,'40%',fontsize=11)
    a.text(.81,.42,"超過 20 s 期限",ha='center',color=C['red'],fontsize=12)
    a.text(.5,.055,"先修復再升級多繞一步，成功結果也會遲到",ha='center',fontsize=14)
    done(f,'retry-tree',{'terminal_probabilities':['.8','.072','.04704','.00096','.0784','.0016'],'terminal_seconds':[10,14,22,22,18,18]})
    # Final decision ties back to initial trace.
    f,a=chart();rows=[("普通模型",9),("快速模型",6)]
    for i,(label,m) in enumerate(rows):
        for r in range(3):
            st=r*(m+1);a.barh(i,m,left=st,color=C['blue'],height=.5);a.barh(i,1,left=st+m,color=C['orange'],height=.5)
        a.text(3*(m+1)+.4,i,f'{3*(m+1)} s',va='center')
    a.axvline(24,color=C['red'],ls='--');a.text(24,-.52,"24 s 期限",ha='center',color=C['red']);a.set(yticks=[0,1],yticklabels=[x[0] for x in rows],xlim=(0,33),ylim=(1.6,-.8),xlabel="任務開始後的時間 / s")
    for c,l in [(C['blue'],"模型呼叫"),(C['orange'],"工具執行")]:a.plot([],[],color=c,lw=8,label=l)
    a.legend(frameon=False,loc='lower right');done(f,'decision',{'model_seconds':[9,6],'task_seconds':[30,21],'deadline':24})
