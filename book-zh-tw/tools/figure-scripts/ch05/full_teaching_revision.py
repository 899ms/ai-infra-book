"""Extend the approved 5.2–5.3 style to execution, compilation and runtime."""
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,name):out.save(f,'figure-5-'+name)
    with plt.rc_context(STYLE):
        d=data['5-1'];f,a=plot(3.6,left=.20)
        cells=[]
        for y,kernel in enumerate(d['kernel_us']):
            start=0
            for dur,label,c in [(3,"提\n交",'orange'),(8,'H2D','blue'),(kernel,'kernel','green'),(4,'D2H','purple')]:
                cell=a.barh(y,dur,left=start,height=.64,color=COL[c],edgecolor=COL['line'])[0]
                label_artist=a.text(start+dur/2,y,label,fontsize=12,ha='center',va='center',linespacing=1.15)
                cells.append((cell,label_artist))
                start+=dur
        a.set(yticks=[0,1],yticklabels=["原 kernel","kernel 加快"],xlim=(0,37),ylim=(-.6,1.6),xlabel="從 CPU 提交起計時（μs）")
        a.invert_yaxis()
        # Preserve proportional durations and require padding inside every cell.
        f.canvas.draw();renderer=f.canvas.get_renderer();padding=2*f.dpi/72
        for cell,label_artist in cells:
            outer=cell.get_window_extent(renderer);inner=label_artist.get_window_extent(renderer)
            if not (outer.x0+padding <= inner.x0 and inner.x1 <= outer.x1-padding
                    and outer.y0+padding <= inner.y0 and inner.y1 <= outer.y1-padding):
                raise ValueError(f'figure-5-1: label must fit inside its cell: {label_artist.get_text()}')
        save(f,'1-execution')
        f,a=canvas(4.6);text(a,.04,.94,"縮排層級決定儲存到何時",14)
        box(a,.04,.08,.92,.76,'','gray');text(a,.07,.79,"遍歷輸出塊 io、jo",14)
        box(a,.12,.62,.76,.10,"建立 FP32 累加器：16 KiB",'green')
        box(a,.15,.29,.70,.26,'','blue');text(a,.18,.49,"迴圈 ko：共 128 次",12)
        text(a,.20,.38,"讀取 A、W 塊 → 更新累加器",11)
        box(a,.12,.12,.76,.10,"歸約結束 → BF16 舍入 → SiLU",'orange',11)
        arrow(a,(.5,.62),(.5,.55));arrow(a,(.5,.29),(.5,.22));save(f,'9-polyhedral')
        f,a=canvas(3.8)
        for y,title,expr,c in [(.57,"先相加，再啟用",'1 + (−1) = 0 → SiLU(0) = 0','green'),(.12,"先分別啟用，再相加",'SiLU(1) + SiLU(−1) ≈ 0.4621','orange')]:
            text(a,.04,y+.25,title,14);box(a,.04,y,.92,.17,expr,c)
        save(f,'activation-order')
        f,a=canvas(3.8);text(a,.04,.94,"先讀完整行，才能確定整行量化 scale",14)
        box(a,.04,.60,.40,.18,"塊 0：最大值 1",'blue');box(a,.56,.60,.40,.18,"塊 1：最大值 10",'orange')
        arrow(a,(.24,.60),(.42,.43));arrow(a,(.76,.60),(.58,.43));box(a,.20,.28,.60,.14,"整行最大值為 10",'green')
        text(a,.5,.11,"第一項：1 → 44.8 → 舍入 44 → 55/56",12,ha='center');save(f,'quantization-scale')
        f,a=canvas(4.3)
        for y,title,label,c in [(.59,"儲存低位寬中間結果","讀原輸入 32 + 寫量化 16 + 重讀 192",'green'),(.13,"每個列塊重新量化","讀原輸入求 scale 32 + 重讀原輸入 384",'orange')]:
            text(a,.04,y+.26,title,14);box(a,.04,y,.92,.17,label,c,11)
            text(a,.50,y-.065,"輸入相關：240 MiB" if c=='green' else "輸入相關：416 MiB",12,ha='center')
        save(f,'10-quantization')
        d=data['5-11'];f,a=plot(3.4);p=np.linspace(0,1,101);a.axhline(10,color='#267398',label="原實作");a.plot(p,20-15*p,color='#a56c28',label="新實作");a.axvline(2/3,ls=':',color='#777777');a.set(xlim=(0,1),ylim=(0,23),xlabel="形狀 A 的呼叫比例",ylabel="平均執行時間（μs）");a.legend(frameon=False);save(f,'11-feedback')
        # One trace panel per capture; exact event times remain tied to source records.
        ranges=data['5-12']['ranges']
        for i,r in enumerate(ranges):
            f,a=plot(2.9,left=.20)
            for event in r['kernels']:a.barh(1,(event['end_ns']-event['start_ns'])/1000,left=(event['start_ns']-r['start_ns'])/1000,height=.38,color=COL['green'],edgecolor=COL['line'],lw=.5)
            # Host API collection is emitted by the fixed trace-analysis source.
            events=r.get('launches',r.get('apis',[]))
            for event in [e for e in events if 'Launch' in e['name']]:a.barh(0,(event['end_ns']-event['start_ns'])/1000,left=(event['start_ns']-r['start_ns'])/1000,height=.38,color=COL['blue'],edgecolor=COL['line'],lw=.5)
            a.set(yticks=[0,1],yticklabels=["主機 launch","加速器 kernel"],xlim=(0,(r['end_ns']-r['start_ns'])/1000),ylim=(-.6,1.6),xlabel="從本段採集起點計時（μs）");a.invert_yaxis();save(f,'12-runtime' if i==0 else f'runtime-{i}')
        f,a=canvas(3.7);text(a,.04,.94,"圖重放按已記錄的地址讀取輸入",14)
        box(a,.04,.62,.34,.18,"本次新輸入\n地址 X",'blue');box(a,.62,.62,.34,.18,"固定圖緩衝\n地址 G",'orange');arrow(a,(.38,.71),(.62,.71))
        text(a,.5,.51,"X 與 G 不同時，複製到 G",11,ha='center')
        box(a,.24,.13,.52,.16,"重放 CUDA Graph，讀取 G",'green');arrow(a,(.79,.62),(.5,.29));save(f,'graph-address')
        d=data['5-13'];f,a=plot(3.5,left=.25)
        for y,(prep,copy) in enumerate(zip(d['prepare_us'],d['copy_us'])):
            for start,dur,c in [(0,prep,'orange'),(prep,copy,'blue'),(prep+copy,20,'green')]:a.barh(y,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line'])
        a.set(yticks=range(3),yticklabels=["普通提交","圖：2 MiB 輸入","圖：16 MiB 輸入"],xlim=(0,46),xlabel="準備、複製與計算總時間（μs）");a.invert_yaxis()
        from matplotlib.patches import Patch
        f.subplots_adjust(top=.85);a.legend(handles=[Patch(facecolor=COL[c],edgecolor=COL['line'],label=label) for c,label in [('orange',"準備"),('blue',"複製"),('green',"計算")]],ncol=3,loc='lower center',bbox_to_anchor=(.5,1.0),frameon=False,columnspacing=1.5,handlelength=1.4);save(f,'13-graph-copy')
        d=data['5-14'];f,a=plot(3.5);r=np.arange(1,141)
        for row,col,label in zip(d['policies'],['#267398','#388768','#a56c28'],["通用","分桶","特化"]):a.plot(r,(row['prepare_ns']+r*row['cohort_execution_ns'])/1e6,color=col,label=label)
        a.set(xlabel="重複執行的組數",ylabel="準備加執行（ms）",xlim=(0,140));a.legend(frameon=False);save(f,'14-specialization')
        d=data['5-15']
        for fine,name in [(False,'15-persistent'),(True,'persistent-blocks')]:
            f,a=plot(3.5,left=.19)
            bars=d['timelines']['fine' if fine else 'coarse']
            for b in bars:
                a.barh(0,b['projection_end']-b['projection_start'],left=b['projection_start'],height=.45,color=COL['blue'],edgecolor=COL['line'])
                a.barh(1,b['activation_end']-b['activation_start'],left=b['activation_start'],height=.45,color=COL['green'],edgecolor=COL['line'])
            a.set(yticks=[0,1],yticklabels=["投影","啟用"],xlim=(0,135),xticks=range(0,131,20),ylim=(-.6,1.6),xlabel="時間（μs）");a.invert_yaxis();a.axvline(bars[0]['activation_start'],ls='--',color='#a56c28');save(f,name)
        f,a=canvas(4.9)
        for i,A in enumerate([60,15]):
            y=.58-i*.45;text(a,.04,y+.32,f'A 為 {A} μs：請求 {10+max(A,40)+10} μs',14)
            box(a,.04,y+.06,.20,.15,"準備 10",'gray',11);box(a,.38,y+.16,.24,.13,f'A：{A}','orange');box(a,.38,y-.03,.24,.13,'B：40','blue');box(a,.76,y+.06,.20,.15,"收尾 10",'green',11)
            for yy in [y+.225,y+.035]:arrow(a,(.24,y+.135),(.38,yy));arrow(a,(.62,yy),(.76,y+.135))
        save(f,'16-critical-path')
        d=data['5-17'];v=[r['latency_saving_ms'] for r in d['pairs']];f,a=plot(3.8)
        a.axhline(0,color='#555555',lw=.8);a.vlines(range(1,12),0,v,color='#267398');a.scatter(range(1,12),v,color='#267398');a.axhline(np.median(v),color='#a56c28',ls='--',label=f'中位數 {np.median(v):.1f} ms')
        a.set(xlim=(.5,11.5),ylim=(-3.2,5.4),xticks=range(1,12),xlabel="配對輪次",ylabel="原請求減新請求耗時（ms）");a.legend(frameon=False);save(f,'17-request')
    from v41_case_figures import draw as draw_v41
    draw_v41(5, out)
    out.finish();return out.outputs,out.checks
