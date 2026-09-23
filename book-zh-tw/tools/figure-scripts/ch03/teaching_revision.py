"""Work arrives, waits, and releases state: book-size diagrams for chapter 3."""
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,name):out.save(f,'figure-3-'+name)
    def bars(name,labels,values,xlabel,height=3.5):
        f,a=plot(height,left=.29);a.barh(range(len(values)),values,color=COL['blue'],edgecolor=COL['line'],height=.52)
        a.set(yticks=range(len(values)),yticklabels=labels,xlim=(0,max(values)*1.30),xlabel=xlabel);a.invert_yaxis()
        for i,v in enumerate(values):a.text(v+max(values)*.02,i,f'{v:,.3f}',fontsize=11,va='center')
        save(f,name)
    with plt.rc_context(STYLE):
        f,a=canvas(4.4);text(a,.04,.94,"複用 6144 token，處理 2048 新 token",14)
        for i,n in enumerate(data['3-1']['slots_after_calls']):
            y=.71-i*.20;box(a,.04,y,.40,.13,'prefill' if i==0 else f'decode {i}','orange' if i==0 else 'blue')
            box(a,.60,y,.36,.13,f'KV 覆蓋 {n} token','green');arrow(a,(.44,y+.065),(.60,y+.065))
            text(a,.04,y-.04,f'產生第 {i+1} 個輸出',11)
        save(f,'1-stages')

        f,a=canvas(3.4);text(a,.04,.93,"同一條請求的三個觀察時刻",14)
        arrow(a,(.06,.60),(.95,.60))
        for x,label in [(.12,"請求到達"),(.43,"首個輸出"),(.87,"最後輸出")]:
            a.plot([x,x],[.57,.63],color=COL['line']);text(a,x,.73,label,12,ha='center')
        box(a,.12,.36,.31,.12,"首回應 TTFT",'blue',11);box(a,.43,.36,.44,.12,"後續輸出間隔",'green')
        box(a,.12,.14,.75,.12,"完整請求時間",'orange');save(f,'request-clocks')
        f,a=plot(3.1)
        a.fill_between([0,10],[1,1],color=COL['blue'],edgecolor=COL['line']);a.set(xlim=(0,12),ylim=(0,1.5),xlabel="工具等待（s）",ylabel="狀態佔用（GiB）",yticks=[0,.5,1])
        a.text(5,.5,'1 GiB × 10 s\n= 10 GiB·s',ha='center',va='center',fontsize=14);save(f,'state-time-area')

        d=data['3-2'];f,a=plot(3.5,left=.18)
        A=np.array(d['A_fraction']);a.bar(range(3),A,color=COL['blue'],edgecolor=COL['line'],label="長輸入類");a.bar(range(3),1-A,bottom=A,color=COL['orange'],edgecolor=COL['line'],label="長輸出類")
        a.set(xticks=range(3),xticklabels=["均勻混合","變化前窗","變化後窗"],ylim=(0,1.3),ylabel="請求比例");a.legend(ncol=2,frameon=False,loc='upper center');save(f,'2-workload-budget')
        f,a=plot(3.5);x=np.arange(3)
        for dx,key,label,col in [(-.18,'prefill_positions_per_second',"輸入 token",'blue'),(.18,'decode_positions_per_second',"後續 decode",'orange')]:a.bar(x+dx,d[key],width=.34,label=label,color=COL[col],edgecolor=COL['line'])
        a.set(xticks=x,xticklabels=["均勻混合","變化前窗","變化後窗"],ylabel="階段工作量（token/s）",ylim=(0,37000));a.legend(frameon=False);save(f,'stage-demand')
        f,a=canvas(2.8);box(a,.03,.46,.24,.22,"新到工作",'orange');box(a,.39,.46,.24,.22,"待處理佇列",'blue');box(a,.75,.46,.22,.22,"完成工作",'green');arrow(a,(.27,.57),(.39,.57));arrow(a,(.63,.57),(.75,.57));text(a,.5,.23,"到來速度超過處理速度，佇列就增長",12,ha='center');save(f,'queue-mechanism')
        q=d['fluid_queue'];f,a=plot(3.6)
        a.plot(q['seconds'],q['backlog_steps'],'o-',color='#a56c28');a.axvline(120,ls='--',lw=1,color='#555555')
        a.annotate(f"{q['backlog_steps'][2]:,.0f} 步",(120,q['backlog_steps'][2]),xytext=(40,125000),arrowprops={'arrowstyle':'->'},fontsize=12)
        a.set(xlim=(0,150),ylim=(0,140000),xlabel="從開始到達計時（s）",ylabel="待處理 decode 步");save(f,'queue-backlog')
        f,a=plot(3.6);rows=d['arrival_reports'];x=np.arange(2)
        for dx,key,label,col in [(-.18,'ttft_p95_s',"首回應 p95",'blue'),(.18,'latency_p95_s',"完整請求 p95",'green')]:a.bar(x+dx,[r[key] for r in rows],width=.34,label=label,color=COL[col],edgecolor=COL['line'])
        a.set(xticks=x,xticklabels=["均勻混合","時段變化"],ylabel="客戶端時間（s）",ylim=(0,390));a.legend(frameon=False);save(f,'arrival-measured')

        d=data['teaching_diagrams']['success_cost'];f,a=canvas(3.6)
        for y,title,cost,success,c in [(.58,"原策略",100,50,'blue'),(.17,"新策略",200,80,'orange')]:
            box(a,.03,y,.28,.21,title,c);box(a,.41,y,.55,.21,f'{cost} 成本 ÷ {success} 次成功\n= {cost/success:g} 成本／成功',c)
            arrow(a,(.31,y+.105),(.41,y+.105))
        text(a,.5,.93,"兩種策略各嘗試 100 次",14,ha='center');save(f,'success-cost')
        rounds=data['3-3']['rounds'];bars('3-agent',["第 1 輪：截斷","第 2 輪：寫檔案","第 3 輪：測試","第 4 輪：結束"],[r['measured_model_seconds'] for r in rounds],"每輪模型牆鐘時間（s）")
        f,a=canvas(3.4);text(a,.04,.94,"公共字首保留一份，分支各自追加",14)
        box(a,.06,.39,.35,.21,"公共字首",'blue')
        for y,label in [(.68,"分支 A 尾部"),(.16,"分支 B 尾部")]:box(a,.62,y,.31,.15,label,'orange');arrow(a,(.41,.495),(.62,y+.075))
        save(f,'branch-state')
        for parallel,name in [(False,'tool-dependency'),(True,'tool-parallel')]:
            f,a=plot(3.5,left=.16)
            stages=[(0,2,0,"模型",'blue'),(2,6,1,"工具 A",'orange'),(2 if parallel else 8,10,2,"工具 B",'green'),(12 if parallel else 18,3,0,"模型",'blue')]
            for start,dur,y,label,col in stages:
                a.barh(y,dur,left=start,height=.5,color=COL[col],edgecolor=COL['line']);a.text(start+dur/2,y,str(dur)+' s',ha='center',va='center',fontsize=12)
            a.set(yticks=[0,1,2],yticklabels=["模型","工具 A","工具 B"],xlim=(0,22),ylim=(-.6,2.6),xlabel="任務時間（s）");a.invert_yaxis();save(f,name)

        dr=json.loads((Path(here).parents[1]/'calculations/results/decision-request-book.json').read_text())
        dd=dr['decision_path_dense'];dl=dr['llm_path_dense'][0];q=dr['scenario']['questions']
        pre=dd['latency_seconds']*1000;step=dl['step_seconds_batch_1']*1000;steps=dl['decode_steps'];total=dl['latency_seconds']*1000
        f,axs=plt.subplots(2,1,figsize=(420/72,4.2),sharex=True);f.subplots_adjust(left=.20,right=.96,bottom=.13,top=.92,hspace=.55)
        for a in axs:a.spines[['top','right']].set_visible(False)
        a=axs[0];a.set_title(f'決策路徑：一次前向，{pre:.1f} ms 後同時得到 {q} 個答案',loc='left',fontsize=12)
        a.barh(0,pre,height=.5,color=COL['blue'],edgecolor=COL['line']);a.text(pre+14,0,f'prefill {dr["scenario"]["input_tokens"]} 個 token，受算力限制',va='center',fontsize=11)
        a.scatter([pre+4]*q,np.linspace(.78,1.22,q),s=14,color=COL['green'],edgecolor=COL['line'],linewidth=.6,zorder=3)
        a.text(pre+14,1,f'{q} 個位置的輸出分佈一次讀出',va='center',fontsize=11)
        a.set(yticks=[0,1],yticklabels=['prefill',"讀取分佈"],ylim=(-.6,1.6));a.invert_yaxis()
        a=axs[1];a.set_title(f'LLM 路徑：同樣的 prefill 之後逐 token 生成 {dl["output_tokens"]} 個 token',loc='left',fontsize=12)
        a.barh(0,pre,height=.5,color=COL['blue'],edgecolor=COL['line'])
        a.barh([1]*steps,[step*.72]*steps,left=[pre+i*step for i in range(steps)],height=.5,color=COL['orange'],edgecolor=COL['line'],linewidth=.4)
        a.text(pre+steps*step/2,.42,f'{steps} 步 decode，每步 {step:.1f} ms，受頻寬限制，依次執行',ha='center',va='center',fontsize=11)
        a.set(yticks=[0,1],yticklabels=['prefill',"逐 token 生成"],ylim=(-.6,1.6),xlim=(0,total*1.04),xlabel="請求開始後的時間（ms）");a.invert_yaxis()
        a.set_xticks([0,round(pre),200,400,round(total)])
        save(f,'decision-request')

        f,a=canvas(4.0);text(a,.04,.94,"影像編碼為視覺 token，再輸入語言模型",14)
        for y,label,c in [(.69,"640 × 640 畫素影像",'gray'),(.43,"16 × 16 畫素一塊 → 40 × 40 個塊",'blue'),(.17,"相鄰 2 × 2 塊合併 → 20 × 20 個 token",'green')]:
            box(a,.07,y,.86,.15,label,c)
            if y>.2:arrow(a,(.5,y),(.5,y-.10))
        save(f,'vision-shapes')
        f,a=canvas(3.9);text(a,.04,.94,"400 個視覺 token，各對應一個特徵向量",14)
        box(a,.04,.63,.92,.17,"四組視覺特徵：每組寬 2560",'blue')
        box(a,.04,.37,.92,.17,"編碼結果：400 × 4 × 2560 × 2 bytes",'green');arrow(a,(.5,.63),(.5,.54))
        box(a,.04,.08,.92,.17,"進入語言主幹後，另產生各層 KV",'orange');arrow(a,(.5,.37),(.5,.25));save(f,'vision-state')
        f,a=canvas(4.3);text(a,.04,.94,"從輸入表示到可聽見的聲音",14)
        for i,(label,c) in enumerate([("視覺或音訊編碼：形成模型輸入",'blue'),("語言模型：理解並生成回覆",'green'),("聲學生成與解碼：產生音訊取樣",'orange'),("接收緩衝與播放裝置：輸出聲音",'purple')]):
            y=.73-i*.205;box(a,.06,y,.88,.13,label,c)
            if i<3:arrow(a,(.5,y),(.5,y-.075))
        save(f,'4-realtime')
        d=data['3-4'];f,a=plot(4.8,left=.17,bottom=.15)
        for z in d['audio_chunks']:
            i=z['chunk'];a.barh(i,20,left=z['playback_start_ns']/1e6,height=.48,color=COL['green'],edgecolor=COL['line']);a.plot(z['arrival_ns']/1e6,i,'o',color='#267398');a.plot(z['deadline_ns']/1e6,i,'|',markersize=14,color='#a56c28')
        a.plot([],[],'o',color='#267398',label="到達");a.plot([],[],'|',color='#a56c28',label="原定播放");a.barh([],[],color=COL['green'],edgecolor=COL['line'],label="實際播放")
        a.set(yticks=range(8),yticklabels=[f'塊 {i+1}' for i in range(8)],xlim=(0,260),ylim=(-1.5,7.6),xlabel="從採集起點計時（ms）");a.invert_yaxis();a.legend(ncol=3,fontsize=11,frameon=False,loc='upper left');save(f,'audio-timing')
        f,a=canvas(2.8);text(a,.04,.92,"發出打斷與停止發聲是兩個事件",14)
        box(a,.04,.40,.36,.24,"123 ms\n發出打斷",'orange');box(a,.60,.40,.36,.24,"130 ms\n本地裝置靜音",'green');arrow(a,(.40,.52),(.60,.52));text(a,.5,.18,"間隔 7 ms；舊音訊在此期間繼續播放",12,ha='center');save(f,'audio-interrupt')

        f,a=canvas(4.1);text(a,.04,.94,"先計算輸出，再沿依賴反向傳梯度",14)
        for x,label,c in [(.04,"前層",'blue'),(.38,"當前層",'orange'),(.72,"後層",'green')]:box(a,x,.64,.24,.16,label,c)
        arrow(a,(.28,.74),(.38,.74));arrow(a,(.62,.74),(.72,.74));text(a,.50,.86,"前向：輸入 → 輸出",11,ha='center')
        arrow(a,(.72,.48),(.62,.48));arrow(a,(.38,.48),(.28,.48));text(a,.5,.39,"反向：後一層梯度 → 前一層梯度",12,ha='center')
        box(a,.23,.10,.54,.14,"當前層另算權重梯度，用於更新",'purple',11);arrow(a,(.5,.45),(.5,.24));save(f,'5-training')
        f,a=plot(3.2,left=.20)
        for y,start,duration,label,c in [(0,0,1,"前向",'blue'),(0,3,1,"反向",'orange'),(1,1,3,"活化值的生命週期",'green')]:
            a.barh(y,duration,left=start,height=.5,color=COL[c],edgecolor=COL['line']);a.text(start+duration/2,y,label,fontsize=12,ha='center',va='center')
        a.set(yticks=[0,1],yticklabels=["該層計算","該層活化值"],xlim=(-.1,4.3),ylim=(-.7,1.7),xticks=[0,1,3,4],xticklabels=["開始","前向完成","反向開始","反向完成"],xlabel="事件次序（間距僅作示意）");a.invert_yaxis();save(f,'activation-lifetime')
        t=data['3-5'];bars('training-flops',["前向","反向","前向加反向","按總參數估算：6ND"],[t['summary'][k]/1e12 for k in ['forward_matrix_flops','backward_matrix_flops','training_matrix_flops','six_nd_flops']],"矩陣運算量（TFLOPs）")
        bars('training-states',["BF16 權重","FP32 梯度","FP32 主權重","Adam 一階矩","Adam 二階矩"],[v/1e9 for v in t['parameter_state_bytes'].values()],"參數相關狀態（GB）",4.0)

        f,a=canvas(4.6);text(a,.04,.94,"生成、回饋和學習使用同一批軌跡",14)
        for i,(label,c) in enumerate([("策略生成回答",'blue'),("規則、模型或環境給出回饋",'orange'),("篩選樣本，組織訓練輸入",'green'),("學習器計算梯度，更新策略",'purple')]):
            y=.73-i*.20;box(a,.16,y,.79,.13,label,c)
            if i<3:arrow(a,(.55,y),(.55,y-.07))
        a.plot([.16,.04,.04,.16],[.195,.195,.795,.795],color=COL['line'],lw=1);arrow(a,(.04,.795),(.16,.795))
        text(a,.05,.045,"左側回傳路徑：新權重交給下一批生成",11);save(f,'6-rl')
        d=data['3-6'];f,a=plot(3.8,left=.21);names=['rollout_prefill','rollout_decode','reference_scoring','policy_update'];labs=["生成輸入","後續生成","參考評分","策略更新"];x=np.arange(4)
        for dx,key,col,label in [(-.18,'base_stages','blue',"生成 32，保留 16"),(.18,'low_acceptance_stages','orange',"生成 64，保留 16")]:
            vals=[next(z['matrix_flops']/1e12 for z in d[key] if z['name']==name) for name in names];a.bar(x+dx,vals,width=.34,color=COL[col],edgecolor=COL['line'],label=label)
        a.set(xticks=x,xticklabels=labs,ylabel="矩陣運算量（TFLOPs）",ylim=(0,1650));a.legend(frameon=False);save(f,'rl-stage-work')

        d=data['3-7'];f,a=plot(3.8);a.plot([2,7.6],[2,7.6],color='#999999',lw=1)
        for split,col,marker,lab in [('fit','#267398','o',"擬合六點"),('holdout','#a56c28','^',"留出兩點")]:
            rows=[z for z in d['records'] if z['split']==split];law=d['law'];pred=[law['E']+law['A']*(z['N']/law['N0'])**(-law['alpha'])+law['B']*(z['D']/law['D0'])**(-law['beta']) for z in rows];a.scatter([z['loss'] for z in rows],pred,color=col,marker=marker,label=lab)
        a.set(xlim=(2,7.6),ylim=(2,7.6),xlabel="觀測損失（nats/token）",ylabel="預測損失（nats/token）");a.legend(frameon=False);save(f,'7-scaling')
        f,a=plot(3.1);res=d['residuals'];a.bar(range(8),[z['residual'] for z in res],color=[COL['blue'] if z['split']=='fit' else COL['orange'] for z in res],edgecolor=COL['line']);a.axhline(0,lw=.8,color='#555555');a.set(xticks=range(8),xticklabels=['F1','F2','F3','F4','F5','F6','H1','H2'],xlabel="F：擬合點；H：留出點",ylabel="預測減觀測（nats/token）");save(f,'scaling-residual')
        f,a=plot(3.8);calls=np.linspace(0,4e8,200)
        for r,col in zip(d['lifecycle']['rows'],['#a56c28','#388768','#267398','#777777']):a.plot(calls/1e8,(r['upfront_cost']+calls*r['cost_per_call'])/3600,color=col,ls='--' if r['outside_fit_box'] else '-',label=f"{r['N']/1e9:g}B"+(" 外推" if r['outside_fit_box'] else ''))
        a.axvline(d['crossing_calls']/1e8,color='#777777',lw=.8);a.set(xlim=(0,4),ylim=(0,1200),xlabel="累計呼叫（億次）",ylabel="累計成本（H100 SXM GPU 小時）");a.legend(frameon=False);save(f,'lifecycle-cost')
        d=data['3-8'];bars('8-history',['Llama 1 6.7B','Llama 2 7B','Llama 3.1 8B','Qwen2.5 7B','Qwen3 8B'],d['ratios'],"報告訓練 token 數／參數數",4.0)
        hist={r['input']['id']:r for r in data['3-9']['history_rows']}
        hopper=989.4/312  # BF16 dense peak ratio vs A100 80GB; H800 matches H100 compute.
        rows=[('llama1-7b','Llama 1 6.7B（A100）',1),('llama1-65b','Llama 1 65B（A100）',1),
              ('llama2-7b','Llama 2 7B（A100）',1),('llama2-70b','Llama 2 70B（A100）',1),
              ('llama31-8b','Llama 3.1 8B（H100）',hopper),('llama31-70b','Llama 3.1 70B（H100）',hopper),
              ('llama31-405b','Llama 3.1 405B（H100）',hopper),
              ('deepseek-v3-pretraining',"DeepSeek-V3 預訓練（H800）",hopper)]
        vals=[hist[k]['input']['gpu_hours']*ratio/1e6 for k,_,ratio in rows]
        cols=[COL['blue']]*4+[COL['green']]*3+[COL['orange']]
        f,a=plot(5.0,left=.40,bottom=.26)
        a.barh(range(len(vals)),vals,color=cols,edgecolor=COL['line'],height=.55)
        a.set(yticks=range(len(vals)),yticklabels=[label for _,label,_ in rows],xscale='log',xlim=(.05,300),
              xticks=[.1,1,10,100],xlabel="A100 等效訓練用量（百萬 GPU 小時）\n橫軸為對數尺度")
        a.xaxis.set_minor_formatter(plt.NullFormatter())
        a.xaxis.set_major_formatter(plt.FuncFormatter(lambda v,_:f'{v:g}'));a.invert_yaxis();a.set_ylim(11,-.6)
        for i,v in enumerate(vals):a.text(v*1.10,i,f'{v:,.2f}',fontsize=11,va='center')
        handles=[plt.Rectangle((0,0),1,1,facecolor=COL[c],edgecolor=COL['line']) for c in ['blue','green','orange']]
        a.legend(handles,["原裝置 A100（實測）","原裝置 H100（×3.17）","原裝置 H800（×3.17）"],frameon=False,loc='lower right')
        save(f,'9-gpu-hours')
    from v41_case_figures import draw as draw_v41
    draw_v41(3, out)
    return out.finish()
