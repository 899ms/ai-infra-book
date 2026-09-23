"""Keep the task, its environment and its resource occupancy visually distinct."""
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-11-'+n)
    def timeline(name,model=9,env=False,rebuild=False):
        f,a=plot(3.7,left=.21);period=model+1
        for k in range(3):
            if env:a.barh(0,3 if rebuild else period,left=k*period+model-2 if rebuild else k*period,height=.55,color=COL['green'],edgecolor=COL['line'])
            else:
                a.barh(1,model,left=k*period,height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(0,1,left=k*period+model,height=.5,color=COL['orange'],edgecolor=COL['line'])
        a.set(yticks=[0] if env else [1,0],yticklabels=["2 GiB 記憶體"] if env else ["模型呼叫","工具 CPU"],xlabel="從任務到達計時（s）",xlim=(0,31),ylim=(-.7,1.6 if not env else .7));save(f,name)
    with plt.rc_context(STYLE):
        timeline('1-timeline');timeline('memory-area',env=True)
        for i,key in enumerate(['demand_9','demand_12']):
            f,a=plot(3.6,left=.24);v=data['capacity'][key];cap=data['capacity']['capacity'];a.barh(range(3),np.array(v)/cap*100,color=[COL[c] for c in ['orange','blue','green']],edgecolor=COL['line']);a.axvline(100,ls='--',color='#666')
            for j,(x,c,l) in enumerate(zip(v,cap,data['capacity']['capacity_labels'])):a.text(x/c*100+2,j,f'{x}/{l}',fontsize=11,va='center')
            a.set(yticks=range(3),yticklabels=["CPU 核","模型併發","記憶體 GiB"],xlim=(0,250),xlabel="需求／容量（%）");a.invert_yaxis();save(f,'capacity' if i==0 else 'capacity-slow')
        f,a=canvas(4.5)
        for x,y,w,l,c in [(.04,.66,.32,"任務控制器",'orange'),(.64,.66,.32,"模型服務",'blue'),(.04,.19,.32,"環境平台",'gray'),(.64,.19,.32,"工具環境",'green')]:box(a,x,y,w,.22,l,c)
        for p,q in [((.36,.82),(.64,.82)),((.64,.71),(.36,.71)),((.2,.66),(.2,.41)),((.36,.35),(.64,.35)),((.64,.24),(.36,.24))]:arrow(a,p,q)
        text(a,.5,.94,"模型請求／完整工具參數",11,ha='center');text(a,.5,.09,"工具執行／儲存結果／交回控制器",11,ha='center');save(f,'2-boundary')
        for i,l in enumerate(["行程","容器",'microVM']):
            f,a=canvas(4.0);text(a,.04,.94,l+"的隔離邊界",14);box(a,.04,.11,.92,.17,"宿主作業系統核心",'gray')
            for j in range(2):
                x=.04+j*.48;box(a,x,.39,.44,.40,'','blue' if i<2 else 'green');text(a,x+.22,.67,"任務 "+str(j),12,ha='center');text(a,x+.22,.50,["私有地址空間","私有檢視與配額","獨立虛擬機器核心"][i],11,ha='center');arrow(a,(x+.22,.39),(x+.22,.28))
            save(f,'isolation-'+str(i))
        f,a=canvas(4.2);box(a,.04,.62,.35,.24,"共享模板\n檔案與依賴",'blue');box(a,.61,.62,.35,.24,"環境私有內容\n修改頁與管理資料",'orange');box(a,.24,.13,.52,.24,"活躍環境記憶體\n行程、工作頁與緩衝區",'green')
        arrow(a,(.215,.62),(.40,.37));arrow(a,(.785,.62),(.60,.37));text(a,.5,.48,"載入執行所需內容",11,ha='center');save(f,'template-runtime')
        f,a=plot(4.0,left=.25);v=data['pages']['local_mib'];a.barh(range(4),v,color=COL['blue'],edgecolor=COL['line'])
        for i,x in enumerate(v):a.text(x+30,i,str(x),fontsize=11,va='center')
        a.set(yticks=range(4),yticklabels=["完整複製","按需載入","僅私有頁","保留熱點頁"],xlim=(0,2500),xlabel="每環境本地內容（MiB）");a.invert_yaxis();save(f,'pages')
        for pause,name in [(False,'pause'),(True,'pause-release')]:
            f,a=plot(3.0,left=.21)
            for start,dur,c in ([(10,8,'orange'),(18,1,'blue')] if pause else [(10,9,'green')]):a.barh(0,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line'])
            if pause:text(a,14,0,"儲存 8 s",11,ha='center');text(a,18.5,0,"恢復",11,ha='center')
            a.set(yticks=[0],yticklabels=["2 GiB 記憶體"],xlim=(10,19),xticks=[10,14,18,19],xlabel="時間（s）");save(f,name)
        timeline('residency',env=True);timeline('residency-rebuild',env=True,rebuild=True)
        for lead,name in [(0,'3-lifecycle'),(1,'prewarm-1'),(2,'prewarm-2'),(3,'prewarm-3')]:
            f,a=plot(2.8,left=.22);start=4-lead;a.barh(0,2,left=start,height=.5,color=COL['blue'],edgecolor=COL['line'])
            if lead>2:a.barh(0,lead-2,left=start+2,height=.5,color=COL['orange'],edgecolor=COL['line'])
            a.axvline(4,ls='--',color='#666');a.set(yticks=[0],yticklabels=["準備環境"],xlim=(0,6.2),xlabel="時間（s）");save(f,name)
        f,a=plot(3.6,left=.25);a.barh(1,2,left=2,height=.5,color=COL['gray'],edgecolor=COL['line']);a.barh(0,2,left=4,height=.5,color=COL['blue'],edgecolor=COL['line']);a.axvline(4,ls='--',color='#666');a.set(yticks=[1,0],yticklabels=["誤選環境","實際所需環境"],xlim=(0,6.2),xlabel="時間（s）");save(f,'prewarm-wrong')
        for after,name in [(False,'4-placement'),(True,'placement-after')]:
            f,a=canvas(4.1);text(a,.5,.93,"新作業需要：同節點四張 H100＋16 核",13,ha='center')
            for i,(node,gpu,cpu) in enumerate([('DGX H100','H100',16 if after else 8),('DGX A100','A100',24 if after else 32)]):
                x=.04+i*.49;box(a,x,.23,.43,.48,'','gray');text(a,x+.215,.62,f'節點 {i+1}：{node}',13,ha='center');text(a,x+.215,.47,f'4 張空閒 {gpu}',12,ha='center');text(a,x+.215,.33,f'{cpu} 個空閒 CPU 核',11,ha='center')
            save(f,name)
        for burst,name in [(False,'queue'),(True,'queue-burst')]:
            f,a=plot(5.0,left=.16)
            for i in range(10):
                arrive=0 if burst else i
                if burst:a.barh(i,i,left=0,height=.52,color=COL['gray'])
                a.barh(i,1,left=i,height=.52,color=COL['blue'],edgecolor=COL['line']);a.plot(arrive,i,'o',ms=4,color='#454545')
            a.set(yticks=range(10),yticklabels=[str(i+1) for i in range(10)],ylabel="工具呼叫",xlabel="時間（s）",xlim=(-.3,10.3));a.invert_yaxis();save(f,name)
        f,a=plot(3.8,left=.18)
        for i,row in enumerate(data['rl-stages']['stage_seconds']):
            start=0
            for j,(v,c,l) in enumerate(zip(row,['blue','orange','green','purple'],["生成","驗證","更新","釋出"])):a.barh(i,v,left=start,height=.5,color=COL[c],edgecolor=COL['line'],label=l if i==0 else None);start+=v
        a.set(yticks=[0,1],yticklabels=["原設定","生成加速"],xlim=(0,90),ylim=(-.5,2.1),xlabel="迭代時間（s）");a.legend(ncol=4,frameon=False,loc='upper left');save(f,'rl-stages')
        f,a=canvas(5.0);box(a,.27,.74,.46,.16,"傳送端：200 Gbit/s",'orange',12)
        for i in range(6):
            x=.04+(i%3)*.32;y=.43-(i//3)*.26;box(a,x,y,.28,.18,f'實例 {i+1}\n16.38 GB／50 Gbit/s','blue',11)
        arrow(a,(.5,.74),(.5,.66));text(a,.5,.64,"同一出口共傳 98.3 GB",11,ha='center')
        for i in range(3):
            x=.18+i*.32;arrow(a,(x,.59),(x,.61));arrow(a,(x,.43),(x,.35))
        a.plot([.18,.82],[.59,.59],color=COL['line'],lw=1);text(a,.5,.05,"單份至少 2.62 s；全部至少 3.93 s",12,ha='center');save(f,'weights')
        for batch,name in [(False,'5-stages'),(True,'stages-batch')]:
            f,a=plot(3.1,left=.20)
            for i in range(3):a.barh(0,10,left=i*10+(20 if batch else 0),height=.5,color=COL[['blue','green','orange'][i]],edgecolor=COL['line']);a.plot(i*10,1,'o',color='#454545')
            a.set(yticks=[1,0],yticklabels=["樣本到達","驗證行程"],xlim=(-1,51),xlabel="時間（s）");save(f,name)
        f,a=plot(4.0,left=.20);a.barh(range(10),[1]*9+[100],height=.6,color=[COL['blue']]*9+[COL['orange']],edgecolor=COL['line']);a.axvline(10,ls='--',color='#666');a.set(yticks=[0,8,9],yticklabels=["樣本 1","樣本 9","樣本 10"],xlim=(0,105),xlabel="驗證時間（s）");a.invert_yaxis();save(f,'remaining-time')
        f,a=plot(3.9,left=.18)
        for i,row in enumerate(data['thinking']['cost_parts']):
            start=0
            for v,c,l in zip(row,['blue','orange','green'],["輸入","思考","可見輸出"]):a.barh(i,v,left=start,height=.5,color=COL[c],edgecolor=COL['line'],label=l if i==0 else None);start+=v
        a.set(yticks=[0,1],yticklabels=["1000 思考","100 思考"],xlabel="單次呼叫成本（美元）",ylim=(-.5,2.0));a.legend(ncol=3,frameon=False,loc='upper left');save(f,'thinking')
        f,a=canvas(4.1);box(a,.04,.40,.23,.23,"任務控制器",'orange',11);box(a,.38,.40,.23,.23,"服務入口",'gray');box(a,.74,.68,.22,.19,"外部 API",'blue',11);box(a,.74,.15,.22,.19,"自建副本",'green',11);arrow(a,(.27,.515),(.38,.515));arrow(a,(.61,.56),(.74,.775));arrow(a,(.61,.46),(.74,.245));text(a,.50,.86,"按呼叫用量計費",11,ha='center');text(a,.5,.13,"按加速器與執行支出計費",11,ha='center');save(f,'6-service')
        for quality,name in [(False,'7-routing'),(True,'routing-deadline')]:
            d=data['11-7'];h=np.array(d['h']);f,a=plot(4.0)
            if quality:a.plot(h*100,.98*h*100,color='#267398');a.axhline(90,ls='--',color='#a56c28');a.axvline(d['joint_target_hit']*100,ls='--',color='#666');a.set(ylabel="按時成功的提交比例（%）",ylim=(0,105))
            else:a.plot(h*100,d['cost_B'],label='B：Sonnet 5',color='#267398');a.axhline(d['cost_A'],label='A：Haiku 4.5',color='#a56c28');a.axvline(d['cost_crossover']*100,ls='--',color='#666');a.set(ylabel="每個成功任務的成本（美元）");a.legend(frameon=False)
            a.set(xlabel="B 請求命中率（%）",xlim=(0,100));save(f,name)
        f,a=plot(3.8);d=data['purchase'];n=np.linspace(0,d['capacity'],100);m=np.linspace(0,3.2e6,100);a.plot(n/1e4,d['fixed']+n*d['self_per_task'],label="預留 4 張 B200",color='#267398');a.plot(m/1e4,m*d['api_per_task'],label="按量計費",color='#388768');a.axvline(d['crossover']/1e4,ls='--',color='#666');a.set(xlabel="每月提交任務數（萬項）",ylabel="每月總成本（美元）",xlim=(0,320));a.legend(frameon=False);save(f,'purchase')
        f,a=canvas(4.6)
        for x,l,c in [(.04,"控制器",'orange'),(.64,"外部系統",'blue')]:box(a,x,.69,.32,.17,l,c)
        arrow(a,(.36,.77),(.64,.77));text(a,.5,.95,"操作 ID：K",12,ha='center');box(a,.64,.39,.32,.17,"操作已提交",'green',11);arrow(a,(.80,.69),(.80,.56));arrow(a,(.64,.46),(.36,.46),'control');text(a,.17,.46,"確認丟失",12,ha='center');arrow(a,(.36,.18),(.64,.18),'control');text(a,.5,.08,"恢復後先按 K 查詢結果",12,ha='center');save(f,'commit-ack')
        # Split the probability tree at the local-repair node to keep edge labels readable.
        f,a=canvas(5.3);box(a,.30,.75,.40,.17,"首次嘗試：10 s",'blue')
        for x,l,c in [(.02,"首次成功\n80%",'green'),(.355,"區域性修復\n12%",'orange'),(.69,"直接升級\n8%",'purple')]:box(a,x,.37,.29,.22,l,c);arrow(a,(.5,.75),(x+.145,.59))
        text(a,.5,.18,"下方比例均以全部提交為分母",11,ha='center');save(f,'retry-tree')
        f,a=canvas(5.4);box(a,.29,.74,.42,.18,"進入修復：全部的 12%",'orange',11)
        box(a,.04,.37,.37,.22,"修復成功：7.2%\n累計 14 s",'green',11);box(a,.59,.37,.37,.22,"修復後升級：4.8%\n累計 22 s",'purple',11)
        arrow(a,(.40,.74),(.225,.59));arrow(a,(.60,.74),(.775,.59));text(a,.18,.68,"條件 60%",11,ha='center');text(a,.82,.68,"條件 40%",11,ha='center');text(a,.5,.19,'12% × 60% = 7.2%\n12% × 40% = 4.8%',12,ha='center');save(f,'retry-conditional')
        f,a=plot(4.0,bottom=.28);v=data['11-8']['policy_costs'];a.bar(range(3),v,color=[COL[c] for c in ['blue','green','orange']],edgecolor=COL['line'])
        for i,y in enumerate(v):a.text(i,y+.00035,f'{y:.4f}',ha='center',fontsize=12)
        a.set(xticks=range(3),xticklabels=["僅首次\n成功任務","有限恢復\n成功任務","有限恢復\n按時成功"],ylabel="全部支出（美元）／符合條件的任務數",ylim=(0,.018));save(f,'8-retry')
        f,a=plot(3.6,left=.20)
        for i,model in enumerate([9,6]):
            for k in range(3):a.barh(i,model,left=k*(model+1),height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(i,1,left=k*(model+1)+model,height=.5,color=COL['orange'],edgecolor=COL['line'])
        a.axvline(24,ls='--',color='#a56c28');a.set(yticks=[0,1],yticklabels=["普通模型","快速模型"],xlim=(0,31),xlabel="完成時間（s）");save(f,'decision')
        # Per-round cloud uploads may fail independently of local persistence.
        f,a=canvas(3.6)
        for x,label in [(.36,"執行測試\n第 1 輪"),(.59,"修改程式碼\n第 2 輪"),(.82,"再次測試\n第 3 輪")]:
            text(a,x,.89,label,11,ha='center')
        for y,label in [(.69,"本地記錄"),(.43,"雲端記錄"),(.17,"雲端進度")]:
            text(a,.02,y,label,12)
        for x in [.26,.49,.72]:box(a,x,.61,.20,.16,"已儲存",'blue',11)
        box(a,.26,.35,.20,.16,"已儲存",'green',11)
        gap=box(a,.49,.35,.20,.16,"上傳失敗",'orange',11)
        gap.set_linestyle('--')
        box(a,.72,.35,.20,.16,"已儲存",'green',11)
        box(a,.26,.09,.20,.16,"到第 1 輪",'green',11)
        a.plot([.475,.475],[.06,.56],color=COL['line'],ls='--',lw=1)
        text(a,.71,.17,"第 2 輪缺失，不能跳到第 3 輪",11,ha='center')
        save(f,'recovery-coverage')
        data['recovery-coverage']={'kind':'teaching','unit':'react_round','trusted_base':0,'local_saved':[1,2,3],'cloud_saved':[1,3],'cloud_gap':[2],'cloud_covered_through':1,'upload_policy':'per-round incremental async; failed upload does not block later uploads'}
    from dsec_figures import draw as draw_dsec
    draw_dsec(out)
    from core_principles_figures import draw as draw_principles
    draw_principles(11, out)
    out.finish();return out.outputs,out.checks
