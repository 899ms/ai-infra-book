"""Chapter 2 drawings follow the objects from one position to a whole request."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,name):out.save(f,'figure-2-'+name)
    def cells(a,x,y,count,w=.65,h=.10,colors=None,labels=None):
        for j in range(count):
            box(a,x+j*w/count,y,w/count-.006,h,labels[j] if labels else str(j+1),colors[j] if colors else 'blue',11)
    def bars(name,labels,values,xlabel,colors=None):
        f,a=plot(4.1 if len(values)>4 else 3.4,left=.31)
        a.barh(range(len(values)),values,color=colors or COL['blue'],edgecolor=COL['line'],height=.55)
        a.set(yticks=range(len(values)),yticklabels=labels,xlim=(0,max(values)*1.28),xlabel=xlabel);a.invert_yaxis()
        for i,v in enumerate(values):a.text(v+max(values)*.025,i,f'{v:,.2f}',va='center',fontsize=11)
        save(f,name)
    with plt.rc_context(STYLE):
        for mode,name,title in [('rnn','1-dependencies',"同層先完成前一 token"),('causal','causal-dependencies',"本層各 token 讀取上一層的因果字首")]:
            f,a=canvas(3.7);text(a,.04,.94,title,14)
            xs=[.23,.44,.65,.86];ys=[.18,.46,.74]
            for l,y in enumerate(ys):
                text(a,.04,y,["輸入","第 1 層","第 2 層"][l],11)
                for j,x in enumerate(xs):
                    if l:
                        for k in ([j] if mode=='rnn' else range(j+1)):
                            arrow(a,(xs[k],ys[l-1]+.04),(x,y-.04))
                        if mode=='rnn' and j:arrow(a,(xs[j-1]+.035,y),(x-.035,y))
                    a.scatter(x,y,s=450,facecolor=COL['blue'],edgecolor=COL['line'],zorder=5)
            for j,x in enumerate(xs):text(a,x,.055,f'token {j+1}',11,ha='center')
            save(f,name)

        f,a=canvas(4.3);text(a,.04,.94,"從同一輸入產生三種表示",14)
        box(a,.30,.74,.40,.12,"當前 token 的隱藏向量",'gray')
        for x,label,c in [(.04,"查詢 Q",'orange'),(.36,"鍵 K",'blue'),(.68,"值 V",'green')]:
            arrow(a,(.5,.74),(x+.14,.62));box(a,x,.46,.28,.16,label,c)
        text(a,.50,.34,"查詢與鍵匹配，得到各 token 的係數",12,ha='center')
        box(a,.09,.10,.82,.14,"按係數彙總各 token 的值，形成輸出",'purple')
        arrow(a,(.5,.29),(.5,.25));save(f,'qkv-objects')

        f,a=canvas(3.7);text(a,.04,.94,"已有 2 個 token，再輸入 3 個 token",14)
        for i in range(3):
            y=.66-i*.19;text(a,.04,y+.065,f'新 token {i+1}',11)
            for j in range(5):
                a.add_patch(Rectangle((.29+j*.125,y),.12,.13,facecolor=COL['blue'] if j<2 else COL['green'] if j<3+i else COL['white'],edgecolor=COL['line'],lw=.8))
                if j<3+i:text(a,.35+j*.125,y+.065,'✓',12,ha='center')
        text(a,.415,.84,"已有上下文",11,ha='center');text(a,.73,.84,"本次輸入",11,ha='center')
        text(a,.5,.065,"舊上下文配對 6 ＋ 塊內因果配對 6",12,ha='center');save(f,'causal-pairs')

        f,a=canvas(4.8);text(a,.04,.95,"一層先交換資訊，再變換特徵",14)
        stages=[("輸入：每 token 4096 個數",'gray'),("歸一化 → 注意力 → 輸出投影",'blue'),("與子層輸入逐元素相加",'green'),("歸一化 → 前饋網路",'orange'),("與子層輸入逐元素相加",'green')]
        for i,(s,c) in enumerate(stages):
            y=.77-i*.16;box(a,.19,y,.76,.115,s,c)
            if i<4:arrow(a,(.57,y),(.57,y-.045))
        for y1,y2 in [(.77,.507),(.45,.187)]:
            a.plot([.19,.065,.065,.19],[y1+.035,y1+.035,y2,y2],color=COL['line'],lw=1)
            arrow(a,(.065,y2),(.19,y2))
        text(a,.05,.055,"左側旁路保留子層輸入，供殘差相加",11);save(f,'2-layer')

        f,a=canvas(3.9);box(a,.30,.80,.40,.12,"輸入 X：4096 維",'gray')
        box(a,.04,.55,.40,.14,"gate 投影 → SiLU",'orange');box(a,.56,.55,.40,.14,"up 投影",'blue')
        arrow(a,(.5,.80),(.24,.69));arrow(a,(.5,.80),(.76,.69))
        text(a,.24,.46,"12288 維",11,ha='center');text(a,.76,.46,"12288 維",11,ha='center')
        box(a,.30,.26,.40,.13,"對應元素相乘",'green');arrow(a,(.24,.43),(.4,.40));arrow(a,(.76,.43),(.6,.40))
        box(a,.20,.04,.60,.13,"down 投影：回傳 4096 維",'purple');arrow(a,(.5,.26),(.5,.17));save(f,'ffn-gates')

        f,a=canvas(4.2);text(a,.04,.94,"每一步追加一 個 token，重讀已有上下文",14)
        for i,n in enumerate([4,5,6,7]):
            y=.71-i*.18;text(a,.03,y+.05,f'第 {i+1} 步',11)
            cells(a,.22,y,n+1,w=.70,h=.12,colors=['blue']*n+['orange'])
        text(a,.5,.07,"藍：本步讀取的上下文；橙：本步追加",11,ha='center');save(f,'history')
        f,a=plot(3.4)
        B=np.arange(1,65);W=data['teaching_diagrams']['history']['shared_weight_bytes']/2**30
        a.axhline(W,color='#267398',label="每批讀取的權重");a.plot(B,B*8192*147456/2**30,color='#a56c28',label="8K token KV × 請求數")
        a.set(xlim=(0,64),ylim=(0,75),xlabel="批內請求數",ylabel="邏輯讀取量（GiB）");a.legend(frameon=False)
        save(f,'history-batch')

        f,a=canvas(5.6)
        for row,(title,groups) in enumerate([("MHA：每個查詢各有一組 KV",4),("GQA：每兩個查詢共用一組 KV",2),("MQA：四個查詢共用一組 KV",1)]):
            top=.95-row*.32;text(a,.04,top,title,14)
            for j in range(4):
                x=.10+j*.225;box(a,x,top-.13,.15,.07,f'Q{j+1}','orange',11)
                g=j if groups==4 else j//2 if groups==2 else 0;dest=.10+(g+.5)*.825/groups
                arrow(a,(x+.075,top-.13),(dest,top-.20))
            for g in range(groups):
                x=.10+g*.825/groups;box(a,x,top-.28,.825/groups-.02,.08,f'KV {g+1}','blue',11)
        save(f,'3-sharing')
        bars('4-cache',["MHA：32 組","GQA：8 組","MQA：1 組"],data['figure_2_4']['qwen_variants_mib'],"8K 上下文狀態容量（MiB）")

        f,a=canvas(4.8)
        text(a,.04,.94,"路徑一：先展開每個上下文 token",14)
        box(a,.04,.69,.25,.13,"潛變數 c",'blue');box(a,.38,.69,.25,.13,"展開鍵 K",'green');box(a,.72,.69,.24,.13,"點積分數",'purple')
        arrow(a,(.29,.755),(.38,.755));arrow(a,(.63,.755),(.72,.755))
        text(a,.32,.60,"上下文先計算 K = c Uₖ",12)
        text(a,.04,.46,"路徑二：先變換當前查詢",14)
        box(a,.04,.22,.25,.13,"當前查詢 q",'orange');box(a,.38,.22,.25,.13,"變換後查詢",'orange');box(a,.72,.22,.24,.13,"點積分數",'purple')
        arrow(a,(.29,.285),(.38,.285));arrow(a,(.63,.285),(.72,.285))
        box(a,.71,.035,.25,.10,"潛變數 c",'blue');arrow(a,(.835,.135),(.835,.22))
        text(a,.04,.09,"查詢先計算 q Uₖᵀ",12)
        save(f,'mla-paths')
        bars('mla-capacity',["緊湊潛變數","展開各頭 KV"],data['figure_2_4']['k3_mla_paths_mib'],"Kimi K3 的 24 層 MLA 狀態（MiB）")

        f,a=canvas(4.3);text(a,.04,.94,"先形成壓縮條目，再由查詢選擇",14)
        cells(a,.05,.72,8,w=.90,h=.11)
        for i in range(2):
            arrow(a,(.27+i*.45,.71),(.27+i*.45,.59));box(a,.10+i*.45,.45,.34,.13,f'壓縮條目 {i+1}','green')
        text(a,.5,.35,"範例：每 4 個 token 合成 1 條",11,ha='center')
        box(a,.04,.08,.25,.13,"當前查詢",'orange');box(a,.38,.08,.25,.13,"掃描索引",'purple');box(a,.72,.08,.24,.13,"讀取選中條目",'green',11)
        arrow(a,(.29,.145),(.38,.145));arrow(a,(.63,.145),(.72,.145));save(f,'5-sparse')
        c=data['figure_2_5']['components'];bars('sparse-capacity',["視窗狀態","壓縮表示","索引條目","壓縮緩衝"],[c['window_history_bytes']/2**20,c['compressed_history_bytes']/2**20,c['index_history_bytes']/2**20,data['figure_2_5']['compressor_buffer_bytes']/2**20],"DeepSeek V4-Flash 的 8K 上下文狀態（MiB）")
        f,a=canvas(3.4)
        for i in range(4):
            x=.04+i*.24;box(a,x,.56,.20,.17,f'到達 {i+1}\n塊內 {i+1}/4','orange' if i==3 else 'blue',11)
            if i<3:arrow(a,(x+.20,.64),(x+.24,.64))
        box(a,.62,.12,.33,.17,"釋出壓縮條目",'green');arrow(a,(.86,.56),(.79,.29))
        text(a,.05,.28,"前三步更新同一緩衝\n第四步完成一塊",12);save(f,'compression-steps')

        f,a=canvas(3.9);text(a,.04,.94,"上下文增加，狀態矩陣保持同樣大小",14)
        for x,title,c in [(.04,"舊狀態",'blue'),(.37,"新鍵值外積",'orange'),(.70,"新狀態",'green')]:
            for i in range(3):
                for j in range(3):a.add_patch(Rectangle((x+j*.08,.46+i*.08),.08,.08,facecolor=COL[c],edgecolor=COL['line'],lw=.7))
            text(a,x+.12,.36,title,12,ha='center')
        text(a,.32,.58,'+',16,ha='center');text(a,.655,.58,'=',16,ha='center')
        box(a,.22,.09,.56,.13,"當前查詢 × 新狀態 → 輸出",'purple');save(f,'recurrence')

        f,a=canvas(4.1);text(a,.04,.94,"模型設定決定採用哪種注意力",14)
        box(a,.05,.62,.40,.18,"30 層線性注意力\n固定遞推狀態",'blue');box(a,.55,.62,.40,.18,"10 層完整注意力\n逐 token 上下文",'green')
        box(a,.20,.34,.60,.13,"層內歸一化與殘差連線",'gray')
        arrow(a,(.25,.62),(.4,.47));arrow(a,(.75,.62),(.6,.47))
        box(a,.06,.07,.41,.16,"路由專家：256 選 8",'orange',11);box(a,.57,.07,.37,.16,"共享專家",'purple')
        arrow(a,(.4,.34),(.27,.23));arrow(a,(.6,.34),(.76,.23));save(f,'6-hybrid')
        import json
        comparison=json.loads((here/'model-comparison.json').read_text())
        d=comparison['state_curves']
        names=dict(zip([x['model_id'] for x in comparison['models']],['V4.1 Flash','Qwen3-8B','Qwen3.6','V4-Flash','Kimi K3']))
        for field,name,ylabel in [('resident_bytes','7-state-growth',"單請求狀態容量（GiB）"),('accounted_access_bytes','state-access',"每步狀態存取量（GiB）")]:
            f,a=plot(4.4,left=.19,bottom=.18)
            for key,col in zip(names,['#965466','#267398','#72558c','#388768','#a56c28']):
                a.plot(np.array(d['lengths'])/1024,np.array(d[field][key])/2**30,'o-',label=names[key],color=col)
            a.set(xscale='log',yscale='log',xlabel="上下文長度（千 token，對數軸）",ylabel=ylabel+"，對數軸")
            a.legend(frameon=False,fontsize=11,loc='upper left');save(f,name)

        f,a=canvas(4.0);text(a,.04,.94,"分派次數相同，存取到的專家可以不同",14)
        for y,title,n,c in [(.58,"分散：覆蓋 256 個專家",256,'blue'),(.17,"集中：覆蓋 8 個專家",8,'orange')]:
            box(a,.04,y,.34,.19,"64 個 token\n每個選擇 8 個",'gray');arrow(a,(.38,y+.095),(.54,y+.095))
            box(a,.54,y,.42,.19,f'{n} 個專家\n每專家平均 {512/n:.0f} 行',c)
            text(a,.04,y-.07,title,12)
        save(f,'expert-reuse')

        f,a=canvas(4.3)
        for i,(title,streams) in enumerate([("普通殘差：保留一條旁路",1),("mHC：保留四路，再混合回傳",4)]):
            y=.56-i*.43;text(a,.04,y+.32,title,14)
            for j in range(streams):box(a,.04+j*.10,y+.11,.075,.09,str(j+1),'blue',11)
            box(a,.55,y+.09,.39,.14,"子層輸入 4096 維",'orange',11)
            arrow(a,(.44 if streams==4 else .13,y+.155),(.55,y+.155))
            text(a,.05,y-.04,"一條原輸入與子層輸出相加" if streams==1 else "四路先匯合供子層使用，隨後混合子層輸出",11)
        save(f,'8-residual')

        arch=data['teaching_diagrams']['architecture']
        for key,label,name in [('layers',"主幹層數",'architecture'),('hidden',"主幹隱藏維度",'architecture-width'),('experts',"每個 MoE 層的路由專家數",'architecture-experts')]:bars(name,['DeepSeek\nV4.1 Flash','Qwen3-8B','Qwen3.6','DeepSeek\nV4-Flash','Kimi K3'],arch[key],label)
        models=data['teaching_diagrams']['resource_comparison']['models']
        for key,div,label,name in [('uniform_bf16_bytes',1e9,"完整 BF16 權重（GB）",'resources'),('decode_matrix_flops',1e9,"8K 上下文單步矩陣運算（GFLOPs）",'resources-compute'),('state_8192_bytes',2**20,"8K 上下文狀態（MiB）",'resources-state')]:bars(name,['DeepSeek\nV4.1 Flash','Qwen3-8B','Qwen3.6','DeepSeek\nV4-Flash',"Kimi K3\n緊湊"],[m[key]/div for m in models],label)

        # Compare 8K with exactly 1M visible positions; retain 200K in JSON.
        long_data=json.loads((here/'long-context-comparison.json').read_text())
        f,a=plot(6.0,left=.32,bottom=.17)
        f.subplots_adjust(top=.84)
        labels=['DeepSeek\nV4.1 Flash','Qwen3-8B','Qwen3.6','DeepSeek\nV4-Flash',"Kimi K3\n緊湊"]
        for start,offset,color,label in [(0,-.18,COL['blue'],"8K 上下文"),(10,.18,COL['orange'],"1M 可見 token")]:
            vals=[r['matrix_flops']/1e9 for r in long_data['models'][start:start+5]]
            yy=np.arange(5)+offset
            a.barh(yy,np.array(vals)-1,left=1,height=.30,color=color,edgecolor=COL['line'],label=label)
            for y,value in zip(yy,vals):a.text(value*1.08,y,f'{value:,.2f}',va='center',fontsize=11)
        a.set(yticks=range(5),yticklabels=labels,xscale='log',xlim=(1,19000),
              xlabel="單步矩陣運算（GFLOPs，對數軸）",ylim=(4.65,-.65))
        a.set_xticks([1,10,100,1000,10000],['1','10','100','1000','10000'])
        a.minorticks_off()
        a.legend(loc='upper left',bbox_to_anchor=(0,1.16),ncol=1,frameon=False)
        a.grid(axis='x',alpha=.15)
        save(f,'long-context-compute')

        rows=data['figure_2_9']['capacity_rows'];f,a=plot(3.8,left=.26,bottom=.25);left=np.zeros(3)
        for key,label,col in [('weight_bytes',"權重",'blue'),('workspace_bytes',"工作區預留",'orange'),('kv_bytes_per_request',"單請求 KV",'green')]:
            vals=np.array([r[key]/1e9 for r in rows]);a.barh(range(3),vals,left=left,height=.5,label=label,color=COL[col],edgecolor=COL['line']);left+=vals
        for i,r in enumerate(rows):a.plot([r['capacity_bytes']/1e9]*2,[i-.35,i+.35],color=COL['ink'],lw=1.2)
        a.set(yticks=range(3),yticklabels=['Qwen BF16\nRTX 4090','70B 8-bit\nH100 SXM','70B 4-bit\nH100 SXM'],xlim=(0,85),xlabel="容量（GB）");a.invert_yaxis();a.legend(loc='upper center',bbox_to_anchor=(.5,-.22),ncol=3,frameon=False);save(f,'9-capacity')
        d=data['figure_2_9']['history_capacity'];bars('history-capacity',["8K 上下文","32K 上下文"],d['maximum_requests'],"容量允許的獨立請求數")

        f,a=canvas(4.8);text(a,.04,.94,"輸入 128 個 token，回傳 4 個 token",14)
        for i in range(4):
            y=.72-i*.21
            box(a,.03,y,.24,.14,"輸入 128 個" if i==0 else f'輸入 y{i}','blue',11)
            box(a,.36,y,.27,.14,'prefill' if i==0 else f'decode {i}','orange')
            box(a,.72,y,.25,.14,f'輸出 y{i+1}','green')
            arrow(a,(.27,y+.07),(.36,y+.07));arrow(a,(.63,y+.07),(.72,y+.07))
            text(a,.49,y-.045,f'已保留 {128+i} 個 token',11,ha='center')
        save(f,'10-request')
        bars('request-compute',['DeepSeek\nV4.1 Flash','Qwen3-8B','Qwen3.6','DeepSeek\nV4-Flash',"Kimi K3\n緊湊"],[r['matrix_flops']/1e12 for r in comparison['requests']],"完整請求矩陣運算（TFLOPs）")
    from core_principles_figures import draw as draw_principles
    draw_principles(2, out)
    from v41_case_figures import draw as draw_v41
    draw_v41(2, out)
    return out.finish()
