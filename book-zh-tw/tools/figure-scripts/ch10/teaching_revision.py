"""Follow state ownership, then execution dependencies, then recoverable progress."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-10-'+n)
    with plt.rc_context(STYLE):
        f,a=canvas(5.0)
        for x,y,w,l,c in [(.04,.70,.25,"輸入樣本",'blue'),(.38,.70,.25,"前向計算",'blue'),(.72,.70,.24,"損失",'orange'),(.38,.39,.25,"反向計算",'green'),(.04,.08,.25,"參數梯度",'green'),(.38,.08,.25,"Adam 更新",'purple'),(.72,.08,.24,"新權重",'blue')]:box(a,x,y,w,.17,l,c)
        for p,q in [((.29,.785),(.38,.785)),((.63,.785),(.72,.785)),((.84,.70),(.63,.475)),((.38,.475),(.165,.25)),((.29,.165),(.38,.165)),((.63,.165),(.72,.165))]:arrow(a,p,q)
        text(a,.04,.95,"一次迭代：由預測誤差得到下一份權重",13);text(a,.50,.63,"保留活化值供反向使用",11,ha='center');text(a,.75,.39,"更新時讀取\n主權重與兩份矩狀態",11);save(f,'update-cycle')
        f,a=plot(4.7,left=.20,bottom=.16);vals=np.array(data['10-1']['allocations_bytes'])/1e9;left=np.zeros(2)
        for j,(l,c) in enumerate([("BF16 權重",'blue'),("BF16 梯度",'green'),("FP32 主權重",'orange'),("一階矩",'purple'),("二階矩",'gray')]):a.barh([1,0],vals[:,j],left=left,height=.45,color=COL[c],edgecolor=COL['line'],label=l);left+=vals[:,j]
        a.set(yticks=[1,0],yticklabels=["推理權重","訓練狀態"],xlabel="容量（GB）",xlim=(0,145),ylim=(-.5,2.8));a.legend(frameon=False,ncol=2,loc='upper left');save(f,'1-state')
        for j,key in enumerate(['3/10','2/5','1/2']):
            f,a=plot(3.7);v=data['10-2']['compute'][key];a.bar(range(4),v,color=COL['blue'],edgecolor=COL['line']);a.scatter(range(4),data['10-2']['capacity'],marker='D',facecolors=COL['orange'],edgecolors=COL['line'],label="視訊記憶體約束卡數下限",zorder=3)
            for x,y in enumerate(v):a.text(x,y+.8,str(y),fontsize=12,ha='center')
            a.set(xticks=range(4),xticklabels=['4090','A100','H100','B200'],ylabel="所需加速器數（張）",ylim=(0,50));a.legend(frameon=False);save(f,'2-budget' if j==0 else f'budget-{j}')
        for stage in range(4):
            f,a=canvas(4.6);text(a,.04,.94,["普通資料並行","ZeRO-1：最佳化器相關狀態分片","ZeRO-2：再將梯度分片","ZeRO-3：再將模型權重分片"][stage],13)
            for row,(l,c,split) in enumerate([("權重",'blue',stage>=3),("梯度",'green',stage>=2),("主權重＋矩",'purple',stage>=1)]):
                y=.64-row*.22;text(a,.02,y+.07,l,11)
                for i in range(4):box(a,.29+i*.17,y,.15,.15,("片 "+str(i)) if split else "完整",c,11)
            for i in range(4):text(a,.365+i*.17,.84,"卡 "+str(i),11,ha='center')
            save(f,f'zero-{stage}')
        f,a=canvas(4.7)
        for i in range(4):
            x=.04+i*.235;box(a,x,.70,.21,.15,f'卡 {i}：片 {i}',['blue','green','orange','purple'][i],11);arrow(a,(x+.105,.70),(x+.105,.45))
        box(a,.04,.18,.92,.27,'','gray');text(a,.5,.12,"GPU 0 的執行緩衝區",12,ha='center')
        for i in range(4):box(a,.06+i*.225,.23,.205,.15,f'片 {i}',['blue','green','orange','purple'][i],11)
        text(a,.5,.03,"用完釋放完整緩衝，原始分片繼續保留",11,ha='center');save(f,'3-sharding')
        f,a=canvas(4.1);box(a,.04,.59,.29,.20,"上游梯度 dY",'green');box(a,.63,.59,.33,.20,"本層：Y = XW",'blue');arrow(a,(.33,.69),(.63,.69))
        box(a,.04,.18,.39,.20,"dX：傳給前一層",'green');box(a,.57,.18,.39,.20,"dW：更新本層參數",'purple')
        arrow(a,(.70,.59),(.235,.38));arrow(a,(.83,.59),(.765,.38));save(f,'gradient-branches')
        for rebuild,name in [(False,'4-recompute'),(True,'recompute-rebuild')]:
            f,a=canvas(3.8);text(a,.04,.92,"反向前重建乘積" if rebuild else "保留前向計算的乘積",14)
            for i,l in enumerate(["前向相乘","等待反向","下投影反向"]):text(a,.17+i*.33,.71,l,11,ha='center')
            box(a,.04,.41,.92,.14,"一直保留 a、u",'blue')
            box(a,.71 if rebuild else .04,.18,.25 if rebuild else .92,.14,'h：6 MiB','orange',11)
            if rebuild:arrow(a,(.83,.41),(.83,.32))
            save(f,name)
        for gpu,name in [(False,'5-casting'),(True,'casting-gpu')]:
            f,a=canvas(4.5);box(a,.04,.65,.35,.20,'GPU：BF16\n96 MiB','blue');box(a,.61,.23,.35,.20,'CPU：FP32\n192 MiB','green')
            if gpu:box(a,.04,.23,.35,.20,'GPU：FP32\n192 MiB','orange');arrow(a,(.215,.65),(.215,.43));arrow(a,(.39,.33),(.61,.33));text(a,.5,.52,"鏈路傳 192 MiB",11,ha='center')
            else:box(a,.61,.65,.35,.20,'CPU：BF16\n96 MiB','blue');arrow(a,(.39,.75),(.61,.75));arrow(a,(.785,.65),(.785,.43));text(a,.5,.52,"鏈路傳 96 MiB",11,ha='center')
            text(a,.5,.08,"GPU 轉換時同時佔用 288 MiB" if gpu else "格式轉換在 CPU 完成",12,ha='center');save(f,name)
        d=data['10-6'];f,a=plot(4.2)
        for k,l,c in [('total_gib',"分片＋10 GiB 臨時緩衝",'#267398'),('persistent_gib',"訓練狀態分片",'#388768')]:a.plot(d['participants'],d[k],label=l,color=c)
        a.axhline(22,ls='--',color='#a56c28',label="RTX 4090 可用 22 GiB");a.set(xlabel="分片參與者數",ylabel="每卡視訊記憶體需求（GiB）",ylim=(0,47));a.legend(frameon=False);save(f,'6-candidates')
        for i,(label,d) in enumerate(data['10-7'].items()):
            f,a=plot(4.1,left=.18)
            for e in d['events']:
                if e['stage'] is None:continue
                a.barh(e['stage'],e['duration']*1000,left=e['start']*1000,height=.58,color=COL[{'F':'blue','B':'orange','update':'green'}[e['kind']]],edgecolor=COL['line'],linewidth=.5)
            a.set(yticks=range(4),yticklabels=[f'階段 {j}' for j in range(4)],xlim=(0,355),xlabel="時間（ms）");a.invert_yaxis();a.set_title(f'{label}：{d["summary"]["step_makespan_seconds"]*1000:.0f} ms',loc='left');save(f,'7-pipeline' if i==0 else 'pipeline-1f1b')
        f,a=plot(3.4,left=.22)
        for e in data['10-7']['1F1B']['events']:
            if e['stage']==3 and e['end']*1000>65 and e['start']*1000<110:a.barh(0,min(e['end']*1000,110)-max(e['start']*1000,65),left=max(e['start']*1000,65),height=.5,color=COL[{'F':'blue','B':'orange','update':'green'}[e['kind']]],edgecolor=COL['line'])
        a.axvspan(93,95,color=COL['gray']);a.annotate("等輸入：2 ms",(94,0),xytext=(82,.7),fontsize=12,arrowprops={'arrowstyle':'->'});a.set(xlim=(65,110),ylim=(-.6,1.2),yticks=[0],yticklabels=["階段 3"],xlabel="時間（ms）",xticks=[65,75,85,95,105]);save(f,'pipeline-gap')
        f,a=plot(3.7)
        for i,(l,d) in enumerate(data['10-7'].items()):a.bar(np.arange(4)+(i-.5)*.34,np.array(d['summary']['reserved_activation_scope_peak_bytes'])/1e9,.32,color=COL[['blue','orange'][i]],edgecolor=COL['line'],label=l)
        a.set(xticks=range(4),xticklabels=[f'階段 {i}' for i in range(4)],ylabel="活化值與收發緩衝峰值（GB）",ylim=(0,3.4));a.legend(frameon=False);save(f,'pipeline-memory')
        for busy,name in [(False,'8-overlap'),(True,'overlap-busy')]:
            f,a=plot(3.2,left=.20);a.barh(1,5,color=COL['blue'],height=.5,edgecolor=COL['line'])
            if busy:a.barh(0,4,color=COL['gray'],height=.5,edgecolor=COL['line'])
            a.barh(0,3,left=4 if busy else 0,color=COL['orange'],height=.5,edgecolor=COL['line']);a.axvline(5,ls='--',color='#666');a.set(xlim=(0,7.5),yticks=[1,0],yticklabels=["獨立計算","鏈路"],xlabel="時間（ms）");save(f,name)
        for i,lengths in enumerate(data['10-9']['lengths']):
            f,a=plot(4.8,left=.20);offset=0
            for n,c in zip(lengths,['blue','green']):a.add_patch(Polygon([(offset,offset),(offset,offset+n),(offset+n,offset+n)],facecolor=COL[c],edgecolor=COL['line']));offset+=n
            a.set(xlim=(0,8192),ylim=(8192,0),xticks=[0,lengths[0],8192],yticks=[0,lengths[0],8192],xlabel="鍵的 token 索引",ylabel="查詢 token 索引");a.set_aspect('equal');save(f,'9-attention-area' if i==0 else 'attention-unequal')
        f,a=canvas(4.1);box(a,.04,.65,.92,.17,"已訓練：到 batch 100",'green')
        for i in range(8):box(a,.04+(i%4)*.235,.37-(i//4)*.20,.21,.14,str(101+i),'blue' if i<4 else 'gray',12)
        text(a,.5,.05,"101—108：已安排準備，仍等待訓練",12,ha='center');save(f,'10-input-queue')
        f,a=canvas(4.0)
        for i in range(4):
            x=.04+i*.235;box(a,x,.66,.215,.18,f'舊 {i}',['blue','green','orange','purple'][i])
            for j in range(2):box(a,x+j*.1175,.22,.10,.18,str(i*2+j),['blue','green','orange','purple'][i]);arrow(a,(x+.1075,.66),(x+j*.1175+.05,.40))
        text(a,.5,.07,"新分片：每片 1536 行；舊分片：3072 行",11,ha='center');save(f,'11-resharding')
        f,a=canvas(4.4)
        for i,(l,c) in enumerate([("捕獲一致狀態",'blue'),("複製到獨立緩衝",'orange'),("後臺寫入資料",'blue'),("提交完整快照",'green')]):
            y=.75-i*.21;box(a,.23,y,.54,.15,l,c)
            if i<3:arrow(a,(.5,y),(.5,y-.06))
        text(a,.80,.60,"訓練\n可繼續",11);save(f,'checkpoint-commit')
        for i,(l,rows) in enumerate(data['10-12']['timelines'].items()):
            f,a=plot(3.9,left=.19)
            for j,r in enumerate(rows):
                t=r['seconds'];a.barh(j,.5,left=t['capture'],color=COL['orange'],height=.5,edgecolor=COL['line']);a.barh(j,min(t['durable'],50)-t['upload_start'],left=t['upload_start'],color=COL['blue'],height=.5,edgecolor=COL['line'])
                if t['durable']>50:a.barh(j,t['durable']-50,left=50,color='white',hatch='///',height=.5,edgecolor=COL['line'])
                a.plot(t['durable'],j,'o',mfc=COL['green'] if t['durable']<=50 else 'white',mec=COL['line']);a.text(t['durable'],j+.4,str(t['durable'])+' s',fontsize=11,ha='center')
            a.axvline(50,ls='--',color='#a56c28');a.set(xlim=(18,59),ylim=(-.5,1.8),yticks=[0,1],yticklabels=["快照 1","快照 2"],xlabel="時間（s）");a.invert_yaxis();a.set_title(l+"：故障發生在 50 s",loc='left');save(f,'12-recovery' if i==0 else 'recovery-fast')
        d=data['10-13'];t=np.array(d['interval_seconds']);c=d['checkpoint_seconds'];lam=d['job_failure_rate_per_second'];r=d['restore_seconds'];f,a=plot(4.1)
        for y,l,color in [(c/t,"儲存",'#267398'),(lam*t/2,"重做",'#a56c28'),(c/t+lam*t/2+lam*r,"總附加時間",'#388768')]:a.plot(t/60,y*100,label=l,color=color)
        a.set(xlabel="儲存間隔（分鐘）",ylabel="每單位有用訓練的附加時間（%）");a.legend(frameon=False);save(f,'13-save-interval')
        f,a=canvas(4.2)
        for i,(l,c) in enumerate([("生成\n12 條/s",'blue'),("驗證\n6 條/s",'orange'),("學習\n8 條/s",'green')]):box(a,.04+i*.34,.48,.24,.24,l,c)
        for x in [.28,.62]:arrow(a,(x,.60),(x+.10,.60))
        text(a,.70,.34,"保留 75% → 4.5 條/s",11,ha='center');arrow(a,(.84,.48),(.84,.16),'control');arrow(a,(.84,.16),(.16,.16),'control');arrow(a,(.16,.16),(.16,.48),'control');text(a,.5,.08,"新權重用於後續生成",12,ha='center');save(f,'14-rl-flow')
        for i,key in enumerate(['restore_bytes','staged_bytes']):
            f,a=plot(4.1,bottom=.26);v=np.array(data['10-15'][key])/2**30;a.step(range(4),v,where='post',color='#267398');a.plot(range(4),v,'o',color='#267398');a.axhline(80e9/2**30,ls='--',color='#a56c28',label='H100 SXM 74.5 GiB');a.legend(frameon=False,loc='upper right');a.set(xticks=range(4),xticklabels=["訓練\n結束","載入權重\n分配 KV" if i==0 else "只載入\n權重","釋放\n訓練狀態","開始\n生成"],ylabel="視訊記憶體佔用（GiB）",ylim=(0,100));a.text(1,v[1]+4,f'峰值 {v[1]:.1f} GiB',fontsize=12,ha='center');save(f,'15-rl' if i==0 else 'rl-staged')
        f,a=canvas(4.5)
        for row,(l,c) in enumerate([("μ：實際生成樣本的策略",'blue'),("πold：本輪最佳化開始時的策略",'orange'),("πθ：本輪更新中的當前策略",'green')]):
            y=.70-row*.28;box(a,.04,y,.92,.18,l,c)
            if row<2:arrow(a,(.5,y),(.5,y-.10),'control')
        text(a,.5,.04,"對同一字首與 token 分別記錄機率",12,ha='center');save(f,'policy-versions')
        for async_,name in [(False,'16-async-cycle'),(True,'async-overlap')]:
            f,a=plot(3.5,left=.20);items=[(2,0,40,'blue'),(1,0 if async_ else 40,16,'green'),(0,40 if async_ else 56,4,'orange')]
            for row,s,d,c in items:a.barh(row,d,left=s,height=.5,color=COL[c],edgecolor=COL['line'])
            a.set(yticks=[2,1,0],yticklabels=["生成","學習","權重同步"],xlim=(0,62),xlabel="穩態週期內時間（s）");save(f,name)
        f,a=canvas(4.9);box(a,.04,.69,.40,.20,"生成時記錄\n樣本 A／token 17／層 3",'blue',11);box(a,.60,.69,.36,.20,"專家 ID：[2, 7]",'orange',11);arrow(a,(.44,.79),(.60,.79))
        box(a,.60,.28,.36,.20,"訓練時仍選 2、7",'orange',11);arrow(a,(.78,.69),(.78,.48),'control');box(a,.04,.28,.40,.20,"用當前權重計算\n分數、輸出與梯度",'green',11);arrow(a,(.60,.38),(.44,.38));text(a,.5,.08,"記錄固定離散選擇；當前權重參與數值計算",11,ha='center');save(f,'17-replay')
        f,a=plot(3.8,left=.18);rows=data['10-18']['rows']
        for i,r in enumerate(rows):
            left=0
            for j,(v,c) in enumerate(zip(r['days'],['blue','orange','gray'])):a.barh(i,v,left=left,height=.45,color=COL[c],edgecolor=COL['line'],label=["基礎訓練","儲存恢復","計劃停頓"][j] if i==0 else None);left+=v
            a.text(left+.4,i,f'{left:.1f}',fontsize=12,va='center')
        a.axvline(30,ls='--',color='#a56c28');a.set(yticks=[0,1],yticklabels=["32 卡","48 卡"],xlabel="完成時間（天）",xlim=(0,41),ylim=(-.5,2.0));a.legend(frameon=False,ncol=2,loc='upper left');save(f,'18-deadline')
        d=data['10-19'];f,a=plot(3.9)
        for k,c in zip(d['curves'],['#388768','#267398','#a56c28']):a.plot(d['relative_bandwidth'],d['curves'][k],color=c,label=f'原通訊佔比 {float(k):.0%}')
        a.set(xlabel="新頻寬／原頻寬",ylabel="新耗時／原耗時");a.legend(frameon=False);save(f,'19-hardware')
        f,a=plot(4.2)
        for (key,d),l,c in zip(data['10-20'].items(),['A100','H100','B200'],['#267398','#388768','#a56c28']):a.plot(np.array(d['parameters'])/1e12,np.array(d['continuous_required_devices'])/1e4,color=c,label=l+'（40%）');a.plot(np.array(d['parameters'])/1e12,np.array(d['continuous_required_devices_mfu50'])/1e4,color=c,ls='--',lw=1)
        a.plot([],[],color='#666',ls='--',lw=1,label="虛線：50%");a.axhline(1.6384,ls='--',color='#666');a.set(yscale='log',xlabel="稠密模型參數量（萬億）",ylabel="90 天所需加速器（萬張）");a.legend(frameon=False);save(f,'20-scale')
        # 21-23: where each bubble-compressing schedule fills the 1F1B gaps; same scale and colours as 17/18.
        fill={'F':'blue','B':'orange','X':'orange','W':'purple','update':'green'}
        for key,name in [('10-21','pipeline-interleaved'),('10-22','pipeline-zero-bubble'),('10-23','pipeline-dualpipe')]:
            d=data[key];f,a=plot(4.1,left=.18)
            for e in d['events']:
                second=e['chunk']==1 or e['direction']==1
                a.barh(e['stage'],e['duration']*1000,left=e['start']*1000,height=.58,color=COL[fill[e['kind']]],edgecolor=COL['line'],linewidth=.5,hatch='////' if second else None)
            a.set(yticks=range(4),yticklabels=[f'階段 {j}' for j in range(4)],xlim=(0,355),xlabel="時間（ms）");a.invert_yaxis();a.set_title(f"{d['label']}：{d['summary']['step_makespan_seconds']*1000:.0f} ms",loc='left');save(f,name)
        # 24: smaller pipeline bubbles trade against transfers, activation peaks and parameters.
        d=data['10-24'];names=list(d);x=np.arange(4)
        f,(a1,a2)=plt.subplots(1,2,figsize=(420/72,3.9));f.subplots_adjust(left=.125,right=.94,bottom=.24,top=.80,wspace=.42)
        a1.bar(x-.17,[d[k]['makespan_m8_ms'] for k in names],.32,color=COL['blue'],edgecolor=COL['line'],label="8 個 micro-batch")
        a1.bar(x+.17,[d[k]['makespan_m16_ms'] for k in names],.32,color=COL['orange'],edgecolor=COL['line'],label="16 個 micro-batch")
        for xx,k in zip(x,names):a1.text(xx-.17,d[k]['makespan_m8_ms']+8,f"{d[k]['makespan_m8_ms']:.0f}",ha='center',fontsize=11);a1.text(xx+.17,d[k]['makespan_m16_ms']+8,f"{d[k]['makespan_m16_ms']:.0f}",ha='center',fontsize=11)
        a1.set(xticks=x,ylabel="完成時間（ms）",ylim=(0,700));a1.set_xticklabels(['1F1B',"交錯 v=2","零氣泡",'DualPipe'],rotation=22,ha='right');a1.legend(frameon=False,ncol=2,loc='lower center',bbox_to_anchor=(.5,1.01),fontsize=11)
        peaks=[max(d[k]['stage_peaks_m8_mib']) for k in names]
        a2.bar(x,peaks,.55,color=COL['green'],edgecolor=COL['line'])
        for xx,p in zip(x,peaks):a2.text(xx,p+30,f'{p:,.0f}',ha='center',fontsize=11)
        a2.set(xticks=x,ylabel="最大單階段峰值（MiB）",ylim=(0,1900));a2.set_xticklabels(['1F1B',"交錯 v=2","零氣泡",'DualPipe'],rotation=22,ha='right')
        out.save(f,'figure-10-pipeline-schedules')
        # 29: capacity factor trades dropped assignments against padded rows.
        d=data['10-29'];f,a=plot(3.9)
        a.bar(x-.17,[v*100 for v in d['model_dropped_fraction']],.32,color=COL['orange'],edgecolor=COL['line'],label="丟棄的 dispatch 佔比")
        a.bar(x+.17,[v*100 for v in d['model_padded_fraction']],.32,color=COL['blue'],edgecolor=COL['line'],label="補零行佔執行量")
        for xx,dr,pa in zip(x,d['model_dropped_fraction'],d['model_padded_fraction']):
            a.text(xx-.17,dr*100+1.2,f'{dr*100:.1f}',ha='center',fontsize=11);a.text(xx+.17,pa*100+1.2,f'{pa*100:.0f}',ha='center',fontsize=11)
        a.set(xticks=x,xticklabels=['1.0','1.25','1.5','2.0'],xlabel="容量因子 c",ylabel="佔比（%）",ylim=(0,58));a.legend(frameon=False,loc='upper left')
        out.save(f,'figure-10-moe-capacity')
    from core_principles_figures import draw as draw_principles
    draw_principles(10, out)
    out.finish();return out.outputs,out.checks
