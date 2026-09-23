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
            text(a,.25,.94,"傳統應用",14,ha='center');text(a,.75,.94,"模型驅動的應用",14,ha='center')
            for x,labels in [(.03,[("程式碼與資料",'orange'),("編譯器與作業系統",'purple'),("程式指令的執行",'green'),("處理器、記憶體與互聯",'blue')]),(.54,[('Agent','orange'),("模型介面",'purple'),("計算輸出、儲存上下文狀態",'green'),("加速器、記憶體與互聯",'blue')])]:
                for i,(label,c) in enumerate(labels):
                    y=.73-i*.18;box(a,x,y,.43,.12,label,c)
                    if i<3:arrow(a,(x+.215,y),(x+.215,y-.06))
            arrow(a,(.54,.79),(.46,.61),kind='control')
            text(a,.5,.065,"工具行程仍由作業系統執行",12,ha='center')
            out.save(f,'figure-1-programmability')
        if chapter == 2:
            f,a=plot(3.8,left=.08,bottom=.22)
            vals=[4*K/1e9,WORKSPACE/1e9,(CAPACITY-4*K-WORKSPACE)/1e9]
            left=0
            for v,c in zip(vals,['green','gray','blue']):
                a.barh(.5,v,left=left,height=.24,color=COL[c],edgecolor=COL['line']);left+=v
            a.set(xlim=(0,24),ylim=(0,1.45),yticks=[],xticks=[0,4,8,12,16,20,24],xlabel="RTX 4090 的 24 GB 容量分配（GB）")
            for x,y,label,target in [(2.4,1.20,"4 條請求 KV\n4.83 GB",2.4),(7,.95,"工作區\n2.15 GB",5.9),(16,1.20,"權重餘量\n17.02 GB",15.5)]:
                a.annotate(label,xy=(target,.64),xytext=(x,y),ha='center',va='center',fontsize=12,arrowprops=dict(arrowstyle='-',color=COL['line']))
            a.text(12,.14,"BF16 參數上界 ≈ 85.1 億",ha='center',fontsize=13)
            out.save(f,'figure-2-reverse-budget')
        if chapter == 4:
            f,a=canvas(4.8)
            rows=[("已有加速器","容量、頻寬、互聯",'blue'),("模型與軟體選擇","壓縮、分塊、並行",'green'),("持續的執行瓶頸","形成下一代硬體需求",'orange'),("新加速器與新候選","重新比較模型結構",'purple')]
            for i,(title,desc,c) in enumerate(rows):
                y=.76-i*.22
                box(a,.06,y,.88,.16,title+'\n'+desc,c)
                if i<3:arrow(a,(.50,y),(.50,y-.06))
            out.save(f,'figure-4-codesign-loop')
            f,a=canvas(4.5)
            text(a,.04,.94,"權重與狀態共用介面",14)
            box(a,.04,.66,.39,.18,"HBM\n權重 + KV",'blue');box(a,.66,.66,.30,.18,"計算",'orange')
            arrow(a,(.43,.75),(.66,.75));text(a,.54,.59,'W + BK',12,ha='center')
            text(a,.04,.46,"獨立的只讀權重通路",14)
            box(a,.04,.25,.39,.13,"ROM：權重 W",'blue');box(a,.04,.04,.39,.13,"HBM：KV 狀態 BK",'green')
            box(a,.66,.13,.30,.20,"計算",'orange')
            arrow(a,(.43,.315),(.66,.27));arrow(a,(.43,.105),(.66,.19))
            out.save(f,'figure-4-rom-paths')
        if chapter == 8:
            f,a=plot(3.8,left=.16,bottom=.19)
            b=np.arange(1,33)
            a.plot(b,(W/b+K)/1e9,color='#527fa0',lw=2,label="傳統 HBM：W/B + K")
            a.plot(b,np.full_like(b,K,dtype=float)/1e9,color='#48826b',lw=2,label="獨立 ROM：K")
            for batch in [1,16]:
                v=(W/batch+K)/1e9;a.scatter([batch],[v],color='#527fa0',s=22)
                a.annotate(f'{v:.2f} GB',(batch,v),xytext=(8,2),textcoords='offset points',fontsize=11)
            a.set(xlim=(0,33),ylim=(0,20),xticks=[1,8,16,24,32],xlabel='batch size B',ylabel="每輸出 token 的 HBM 讀取（GB）")
            a.legend(frameon=False,loc='upper right');out.save(f,'figure-8-batch-counterfactual')
            f,a=canvas(4.2)
            rows=[(.72,"追加",[(8,"8K 複用",'blue'),(1,'','orange')]),(.43,"改寫開頭",[(9,"9K 重新處理",'orange')]),(.14,"總結歷史",[(2,'2K','orange'),(1,'1K','orange')])]
            for y,label,segments in rows:
                text(a,.03,y+.06,label,12)
                x=.26
                for length,lab,col in segments:
                    width=length*.073
                    box(a,x,y,width,.13,lab,col);x+=width
                if label=='追加':text(a,x-.0365,y-.065,"1K 新增",11,ha='center')
                if label=='總結歷史':text(a,.61,y+.065,"另計總結工作",11)
            text(a,.5,.96,"相同歷史，三種更新方式",14,ha='center')
            out.save(f,'figure-8-context-edits')
        if chapter == 10:
            f,a=canvas(4.2)
            text(a,.04,.94,"固定版本服務",14)
            box(a,.04,.67,.38,.17,"ROM\n權重 v0",'blue');box(a,.64,.67,.32,.17,"生成\n可寫 KV",'green');arrow(a,(.42,.755),(.64,.755))
            text(a,.04,.48,"持續更新的策略",14)
            box(a,.04,.19,.25,.18,"訓練\n更新參數",'orange');box(a,.39,.19,.25,.18,"可寫權重\nv0 → v1",'blue');box(a,.74,.19,.23,.18,"生成\n使用 v1",'green')
            arrow(a,(.29,.28),(.39,.28));arrow(a,(.64,.28),(.74,.28))
            text(a,.5,.065,"更新後釋出權重，保持版本一致",12,ha='center');out.save(f,'figure-10-weight-update')
        if chapter == 11:
            f,a=plot(4.4,left=.24,bottom=.17)
            cold=2+2**31/(25e9/8)
            for y,v,c in [(4,6,'blue'),(3,cold,'green'),(1,1,'blue'),(0,cold,'green')]:a.barh(y,v,height=.55,color=COL[c],edgecolor=COL['line']);a.text(v+.13,y,f'{v:.1f} 秒' if v!=int(v) else f'{int(v)} 秒',va='center',fontsize=11)
            a.axhline(2.2,color=COL['line'],lw=.7)
            a.annotate('',xy=(cold,1.5),xytext=(1,1.5),arrowprops=dict(arrowstyle='<->',color=COL['line']));a.text(3.6,1.62,f'額外等待約 {cold-1:.1f} 秒',ha='left',fontsize=11)
            a.set(yticks=[4,3,1,0],yticklabels=["快速服務","冷路徑建立","加速模型","冷路徑建立"],xlim=(0,8),ylim=(-.65,4.7),xlabel="從模型開始計時（秒）")
            out.save(f,'figure-11-environment-overlap')
        if chapter == 12:
            f,a=plot(3.5,left=.24,bottom=.21)
            for y,v in [(2,8),(1,.8),(0,0)]:
                a.barh(y,v,height=.55,color=COL['blue'],edgecolor=COL['line'],label="模型" if y==2 else None)
                a.barh(y,2,left=v,height=.55,color=COL['orange'],edgecolor=COL['line'],label="其他依序執行階段" if y==2 else None)
                a.text(v+2+.12,y,f'{v+2:g} 秒',va='center',fontsize=12)
            a.set(yticks=[2,1,0],yticklabels=["原任務","模型快 10 倍","理想下界"],xlim=(0,12),ylim=(-.7,3),xlabel="完整任務時間（秒）");f.subplots_adjust(top=.84);a.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.45,1.17),columnspacing=1.5,handlelength=1.4)
            out.save(f,'figure-12-task-counterfactual')
