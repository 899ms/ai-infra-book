"""Placement first, state handoff second, resource rates last."""
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-9-'+n)
    with plt.rc_context(STYLE):
        for i,title in enumerate(["多卡共同執行一個完整模型","完整副本分別接收請求","PD：按輸入處理與生成階段分工","AF：按每層的運算元分工"]):
            f,a=canvas(3.7);text(a,.04,.94,title,14)
            if i==0:
                box(a,.04,.22,.92,.48,'','gray');text(a,.5,.61,"一個排程器，一組模型權重與狀態",12,ha='center')
                for j in range(8):box(a,.06+j*.112,.32,.09,.12,str(j),'blue',11)
            elif i==1:
                for x in [.04,.56]:box(a,x,.25,.40,.26,"完整模型副本",'blue');text(a,x+.2,.72,"獨立請求",12,ha='center');arrow(a,(x+.2,.65),(x+.2,.51))
            else:
                for x,label,c in [(.04,"P：處理輸入" if i==2 else "注意力",'blue'),(.61,"D：逐步生成" if i==2 else "FFN／專家",'green')]:box(a,x,.28,.35,.27,label,c)
                arrow(a,(.39,.46),(.61,.46));text(a,.5,.68,"傳輸上下文 KV" if i==2 else "逐層傳遞啟用",12,ha='center')
                if i==3:arrow(a,(.61,.35),(.39,.35))
            save(f,'1-organization' if i==0 else f'organization-{i}')
        f,a=canvas(4.3)
        for j,l in enumerate(['P','D',"工具等待","下一輪 P"]):box(a,.20+j*.19,.73,.18,.15,l,'gray',11)
        for row,(l,start,c) in enumerate([("權重",.20,'blue'),('KV',.20,'green'),("可複用 EC",.20,'purple')]):
            y=.48-row*.17;text(a,.02,y+.05,l,11);box(a,start,y,.75,.10,'',c)
        text(a,.5,.04,"階段寬度示意順序；等待期間狀態仍保留",11,ha='center');save(f,'2-state')
        for stage,name in [(0,'kv-residency'),(1,'kv-publish'),(2,'kv-release')]:
            if stage==0:
                # Two states of the same 8K context; box widths follow the byte counts (1.125 GiB versus 549 MiB).
                f,a=canvas(4.6);text(a,.04,.95,"傳輸開始：兩端都佔用完整空間",13)
                for row,(model,size,w) in enumerate([('Qwen3-8B，GQA','1.125 GiB',.35),("DeepSeek-V3，緊湊 MLA",'549 MiB',.17)]):
                    y=.52-row*.38;text(a,.04,y+.30,model,12)
                    box(a,.04,y,w,.22,"源 P\n"+size,'blue');box(a,.96-w,y,w,.22,"目的 D\n"+size,'orange');arrow(a,(.04+w,y+.11),(.96-w,y+.11),'data')
                text(a,.5,.05,"資料複製中；方框寬度按位元組數比例",12,ha='center');save(f,name);continue
            f,a=canvas(3.9);text(a,.04,.94,["傳輸開始：兩端都佔用完整空間","傳輸完成：通知目的端可以使用 KV","源端釋放緩衝區，D 繼續生成"][stage],13)
            box(a,.04,.35,.35,.29,"源 P\n1.125 GiB" if stage<2 else "源 P\n已釋放",'blue' if stage<2 else 'gray');box(a,.61,.35,.35,.29,"目的 D\n1.125 GiB",'orange' if stage==0 else 'green');arrow(a,(.39,.5),(.61,.5),'data' if stage==0 else 'control');text(a,.5,.15,"資料複製中" if stage==0 else "完成標記建立使用順序" if stage==1 else "下一請求可使用源端空間",12,ha='center');save(f,name)
        f,a=canvas(4.4)
        r=data['9-3']['per_card_rates']
        for row,(title,per,c) in enumerate([("P 池：四張 A100",r['A100']['prefill'],'blue'),("D 池：四張 H20",r['H20']['decode'],'green')]):
            y=.61-row*.40;text(a,.04,y+.23,title,14)
            for i in range(4):box(a,.04+i*.235,y,.21,.16,f'{per:.2f} 請求/s',c,11)
            text(a,.5,y-.09,f'池能力：{4*per:.2f} 請求/s',12,ha='center')
        save(f,'pd-layout')
        f,a=plot(4.5,left=.17);matrix=np.zeros((5,5))
        for row in data['9-3']['assignments']:
            x=row['prefill_workers']['A100'];y=row['prefill_workers']['H20'];matrix[y,x]=float(Fraction(row['bound_requests_per_second_exact']))
        a.imshow(matrix,origin='lower',cmap='Blues',vmin=0,vmax=10,aspect='equal')
        for y in range(5):
            for x in range(5):a.text(x,y,f'{matrix[y,x]:.2f}',fontsize=11,ha='center',va='center')
        a.add_patch(plt.Rectangle((3.5,-.5),1,1,fill=False,edgecolor='#a56c28',lw=2.2))
        a.set(xticks=range(5),yticks=range(5),xlabel="分給 P 的 A100 數量",ylabel="分給 P 的 H20 數量");save(f,'3-pd')
        f,a=canvas(4.9)
        for row,(na,nh) in enumerate(zip(data['new-allocation']['prefill_A100'],data['new-allocation']['prefill_H20'])):
            y=.70-row*.31;text(a,.04,y+.18,["推理請求：1025 個輸出","字首命中 6144 個 token","輸出減至 129 個 token"][row],13)
            for i in range(8):
                isp=i<na if i<4 else i-4<nh
                box(a,.035+i*.117,y,.10,.12,('A100' if i<4 else 'H20')+'\n'+('P' if isp else 'D'),'blue' if isp else 'green',11)
            text(a,.5,y-.045,f'請求率上限 {data["new-allocation"]["rates"][row]:.2f}/s',11,ha='center')
        save(f,'4-allocation')
        for local,name in [(False,'5-local'),(True,'local-cpu')]:
            f,a=canvas(4.4);box(a,.04,.67,.35,.18,"CPU 主存：專家權重",'blue',11);box(a,.61,.67,.35,.18,"GPU：輸入啟用",'green',11)
            if local:
                arrow(a,(.61,.76),(.39,.76));box(a,.04,.31,.35,.18,"CPU 專家計算",'blue');arrow(a,(.215,.67),(.215,.49));arrow(a,(.39,.40),(.61,.40));box(a,.61,.31,.35,.18,"GPU 匯合結果",'orange',11)
            else:
                arrow(a,(.39,.76),(.61,.76));box(a,.61,.31,.35,.18,"GPU 專家計算",'green');arrow(a,(.785,.67),(.785,.49))
            text(a,.5,.13,"啟用往返：每行共 16 KiB" if local else "搬移一份專家權重：36 MiB",12,ha='center');save(f,name)
        d=data['9-6'];f,a=plot(3.9)
        for key,label,c,ls in [('cpu_avx512_ms','CPU，AVX-512','#267398','-'),('cpu_amx_ms','CPU，AMX','#267398','--'),('weight_copy_gpu_ms',"搬權重到 GPU",'#a56c28','-')]:a.plot(d['tokens_per_expert'],d[key],label=label,color=c,ls=ls)
        a.set_xscale('log',base=2);a.set(xlabel="每個專家收到的 token 數（對數刻度）",ylabel="八個專家的路徑時間（ms）",xlim=(1,1024),ylim=(0,30),xticks=[1,4,16,64,256,1024],xticklabels=['1','4','16','64','256','1024']);a.minorticks_off();a.legend(frameon=False);save(f,'6-reuse')
        # The two expert-footprint rectangles repeated figure 6-19, so section 9.3.3 keeps only the prose recall.
        d=data['9-mla-handoff'];f,a=plot(3.8)
        for k,l,c in [('pd_gqa_ms',"PD 一次交接：GQA 1.125 GiB",'#267398'),('pd_mla_ms',"PD 一次交接：緊湊 MLA 549 MiB",'#388768'),('af_step_ms',"AF 一步交接：72 次",'#a56c28')]:a.plot(d['startup_us'],d[k],label=l,color=c)
        for key,c in [('gqa25','#267398'),('mla25','#388768')]:
            x=d['equal_time_startup_us'][key];y=589824/25e9*1e3+72*x/1e3
            a.scatter([x],[y],color=c,zorder=3);a.annotate(f'{x:.0f} μs',(x,y),xytext=(x+25,y-9),fontsize=11)
        a.set(xlabel="每次啟動開銷（μs）",ylabel="序列交接時間（ms）",xlim=(0,800),ylim=(0,80),yticks=[0,20,40,60,80]);a.legend(frameon=False,loc='upper left');save(f,'mla-handoff')
        for i,tasks in enumerate(data['new-balance']['assignments_per_card']):
            f,a=plot(4,left=.17);times=np.array(tasks)*2*18874368/(data['new-balance']['effective_TFLOPs']*1e12)*1e6;a.barh(range(8),times,color=COL['blue'],edgecolor=COL['line']);a.axvline(max(times),ls='--',color='#a56c28');a.set(yticks=range(8),yticklabels=[f'卡 {j}' for j in range(8)],xlim=(0,42),xlabel="H100 上的專家矩陣計算（μs）");a.invert_yaxis();save(f,'9-balance' if i==0 else 'balance-hotspot')
        d=data['9-10'];f,a=plot(3.6)
        for key,label,c in [('nvlink',"同一臺 HGX 內經 NVLink",'#388768'),('cx7',"跨伺服器經 ConnectX-7",'#a56c28')]:a.plot(d['batches'],d['net_saving_ms'][key],color=c,label=label)
        a.axhline(0,color='#777777');a.set(xlabel="熱點持續的批數",ylabel="累計淨節省（ms）");a.legend(frameon=False);save(f,'10-experts')
        for i,items in enumerate([data['new-overlap']['serial_items'],data['new-overlap']['pipeline_items']]):
            f,a=plot(3.5,left=.23)
            for row,start,dur,_ in items:a.barh(row,dur,left=start,height=.5,color=COL[['blue','green','orange'][row]],edgecolor=COL['line'])
            a.set(yticks=[0,1,2],yticklabels=["分派","專家計算","結果合併"],xlim=(0,.88),xlabel="時間（ms）");a.invert_yaxis();save(f,'11-overlap' if i==0 else 'overlap-pipeline')
        f,a=canvas(3.8);box(a,.04,.50,.34,.24,"目錄記錄\n標識 → 儲存位置",'orange',11);box(a,.62,.50,.34,.24,"KV 資料物件\n實際上下文狀態",'blue',11);arrow(a,(.38,.62),(.62,.62),'control');text(a,.5,.22,"先按目錄定位，再確認物件可用並取回",12,ha='center');save(f,'cache-directory')
        f,a=canvas(4.5)
        for i in range(64):
            x=.04+i%16*.059;y=.72-i//16*.14;box(a,x,y,.05,.10,str(i+1),'orange' if i==63 else 'green',11)
        text(a,.5,.94,"讀入 64 頁，前 63 頁可連續複用",14,ha='center');text(a,.5,.10,"綠色：1008 token；橙色：16 token 仍需處理",11,ha='center');save(f,'12-cache')
        d=data['new-route']
        for i,(queue,segs,compute) in enumerate(zip(d['queues_ms'],d['retrieval_segments_ms'],d['compute_ms'])):
            f,a=plot(3.0,left=.17);a.barh(0,queue,height=.45,color=COL['gray']);ready=0
            for dur,c in zip(segs,['gray','orange','blue']):a.barh(1,dur,left=ready,height=.45,color=COL[c],edgecolor=COL['line']);ready+=dur
            a.barh(0,compute,left=max(queue,ready),height=.45,color=COL['green']);a.set(yticks=[0,1],yticklabels=['GPU',"取回"],xlim=(0,950),xlabel="從請求到達起計時（ms）");a.invert_yaxis();save(f,'13-route' if i==0 else f'route-{i}')
        d=data['new-migration'];f,a=plot(3.7);t=np.linspace(0,8,321);src=d['initial_GB']+d['growth_GBs']*t;a.plot(t,src,color='#a56c28',label="源端狀態")
        for B,c,label in zip(d['copy_GBs'],['#388768','#267398'],["已複製：25 GB/s 網路卡","已複製：50 GbE"]):a.plot(t,np.minimum(B*t,src),color=c,label=label)
        a.set(xlabel="後臺複製時間（s）",ylabel="累計狀態（GB）",xlim=(0,8),ylim=(0,48));a.legend(frameon=False,loc='lower right');save(f,'14-migration')
        f,a=canvas(4.8)
        for row,title in enumerate(["已可靠記錄的序列","故障前儲存的 KV","恢復後繼續生成"]):
            y=.68-row*.27;text(a,.04,y+.20,title,13);box(a,.04,y,.36,.13,"輸入 8192 token",'blue',11)
            if row!=1:box(a,.43,y,.32,.13,"輸出 1—1024",'green',11);box(a,.78,y,.19,.13,"輸出 1025",'orange',11)
            else:text(a,.68,y+.065,"生成部分尚未儲存",11,ha='center')
        text(a,.5,.03,"補算 1024 token → KV 到 9216 → 處理輸出 1025",11,ha='center');save(f,'15-recovery')
        for pooled,name in [(False,'16-composition'),(True,'composition-pool')]:
            f,a=canvas(3.6);nodes=['P',"共享池",'D'] if pooled else ['P','D'];xs=[.04,.40,.76] if pooled else [.04,.76]
            for x,n in zip(xs,nodes):box(a,x,.39,.20,.22,n,'orange' if n=='共享池' else 'blue')
            for x1,x2 in zip(xs,xs[1:]):arrow(a,(x1+.20,.5),(x2,.5));text(a,(x1+.20+x2)/2,.71,'1.125 GiB',11,ha='center')
            text(a,.5,.18,"完整寫入並通知 D 後，D 再讀取" if pooled else "P 直接將完整狀態交給 D",12,ha='center');save(f,name)
        d=data['9-17'];f,a=plot(4.8,bottom=.36)
        for (key,q),c,label in zip(d['queues'].items(),['#388768','#267398','#a56c28'],["直接 PD","理想分塊共置","不分塊共置"]):a.plot(d['time_s'],q,color=c,label=f'{label} {key} 請求/s')
        a.axvline(10,ls='--',color='#777777');a.axvline(60,ls=':',color='#a95159');a.set(xlabel="從啟動開始計時（s）",ylabel="積壓請求數",xlim=(0,80),ylim=(0,70));a.legend(frameon=False,loc='upper center',bbox_to_anchor=(.42,-.2));save(f,'17-service')
    from v41_case_figures import draw as draw_v41
    draw_v41(9, out)
    out.finish();return out.outputs,out.checks
