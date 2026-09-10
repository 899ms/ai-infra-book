"""A physical path before its budget; an event clock before its recurrence."""
import numpy as np
import matplotlib.pyplot as plt
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-12-'+n)
    with plt.rc_context(STYLE):
        f,a=canvas(4.8);box(a,.04,.67,.32,.20,'终端：30 MB 原图','blue',11);box(a,.64,.67,.32,.20,'服务器：处理 0.3 s','green',11);arrow(a,(.36,.77),(.64,.77));text(a,.5,.95,'上行：20 Mbit/s，发送 12 s',12,ha='center')
        box(a,.64,.22,.32,.20,'生成 5 MB 成片','green',11);box(a,.04,.22,.32,.20,'终端收齐：任务完成','orange',11);arrow(a,(.8,.67),(.8,.42));arrow(a,(.64,.32),(.36,.32));text(a,.5,.09,'下行：100 Mbit/s，发送 0.4 s',12,ha='center');text(a,.27,.52,'双向传播合计 0.1 s',11,ha='center');save(f,'image-path')
        d=data['12-1'];f,a=plot(4.0);b=np.array(d['uplink_Mbps'])
        for y,l,c in [(240/b+.8,'原方案','#267398'),(240/b+.53,'处理快十倍','#388768'),(120/b+.95,'输入减半','#a56c28')]:a.plot(b,y,label=l,color=c)
        a.set(xscale='log',xlabel='上行速率（Mbit/s）',ylabel='完整成片返回时间（s）');a.legend(frameon=False);save(f,'1-raw')
        for chunked,name in [(False,'2-overlap'),(True,'overlap-chunks')]:
            f,a=plot(4.0,left=.20)
            if chunked:
                for i,ret in enumerate([.08,.16,.16]):
                    u=4*(i+1);a.barh(2,4,left=4*i,height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(1,.1,left=u+.05,height=.5,color=COL['green'],edgecolor=COL['line']);a.barh(0,ret,left=u+.15,height=.5,color=COL['orange'],edgecolor=COL['line'])
            else:
                for row,start,dur,c in [(2,0,12,'blue'),(1,12.05,.3,'green'),(0,12.35,.4,'orange')]:a.barh(row,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line'])
            a.set(yticks=[2,1,0],yticklabels=['上传','处理','回传'],xlim=(0,13),xlabel='时间（s）');save(f,name)
        f,a=plot(4.1,left=.23)
        for row,start,dur,c in [(3,0,20,'blue'),(2,20,12,'green'),(1,32,1,'orange'),(0,78,20,'purple')]:a.barh(row,dur,left=start,height=.5,color=COL[c],edgecolor=COL['line'])
        a.plot(38,1,'o',color='#454545');a.annotate('到达 38 ms',(38,1),(45,1.55),fontsize=11,arrowprops={'arrowstyle':'->'});a.set(yticks=[3,2,1,0],yticklabels=['采集','模型处理','发送／到达','播放'],xlim=(0,105),xlabel='时间（ms）');save(f,'audio-clocks')
        f,a=plot(4.3,left=.20);chunks=data['12-3']['audio_chunks'][:5]
        for i,r in enumerate(chunks):
            a.barh(i,20,left=r['deadline_ns']/1e6,height=.6,color='white',edgecolor=COL['line']);a.barh(i,20,left=r['playback_start_ns']/1e6,height=.36,color=COL['blue'],edgecolor=COL['line']);a.plot(r['arrival_ns']/1e6,i,'o',color='#a56c28')
        a.set(yticks=range(5),yticklabels=[f'块 {i+1}' for i in range(5)],xlabel='时间（ms）',xlim=(25,190));a.invert_yaxis();save(f,'3-paths')
        d=data['12-4'];f,a=plot(3.8)
        for bits,c in zip(d['initial_bits'],['#267398','#a56c28']):t=np.linspace(0,bits/(256000-130000),100);a.plot(t*1000,(bits-t*126000)/1000,color=c,label=f'初始 {bits/256000*1000:g} ms 音频')
        a.set(xlabel='播放开始后的时间（ms）',ylabel='尚未播放的数据（kbit）',ylim=(0,34));a.legend(frameon=False);save(f,'4-buffer')
        f,a=canvas(4.1)
        for x,y,l,c in [(.04,.63,'截图 v','blue'),(.62,.63,'上传与模型判断','green'),(.62,.18,'执行操作','orange'),(.04,.18,'更新界面 v+1','blue')]:box(a,x,y,.34,.21,l,c)
        for p,q in [((.38,.735),(.62,.735)),((.79,.63),(.79,.39)),((.62,.285),(.38,.285)),((.21,.39),(.21,.63))]:arrow(a,p,q)
        save(f,'5-agent')
        for local,name in [(False,'encoder-remote'),(True,'encoder-local')]:
            f,a=canvas(4.2);box(a,.04,.60,.34,.24,'端侧\n视觉编码' if local else '端侧\n压缩图片','green' if local else 'blue');box(a,.62,.60,.34,.24,'远端\n语言模型' if local else '远端\n视觉编码','green');arrow(a,(.38,.72),(.62,.72));text(a,.5,.39,'传完整特征：8.192 MB' if local else '传图片：0.8 MB',13,ha='center');text(a,.5,.20,'四组特征分别注入语言模型不同层' if local else '远端先编码，再进入语言模型',11,ha='center');save(f,name)
        f,a=plot(3.3,left=.23);a.barh([1,0],[1,10.24],height=.5,color=[COL['blue'],COL['green']],edgecolor=COL['line']);a.set(yticks=[1,0],yticklabels=['压缩图片','完整特征'],xlabel='6.4 Mbit/s 上行发送时间（s）',xlim=(0,11.5));save(f,'6-placement')
        f,a=canvas(5.4)
        for row,(l,c) in enumerate([('图片：0.8 MB','blue'),('编码缓存 EC：7.8 MiB','green'),('视觉位置 KV：56.3 MiB','purple')]):
            y=.73-row*.28;box(a,.04,y,.49,.17,l,c,11);text(a,.57,y+.085,['重做视觉编码\n再处理语言前缀','从语言前缀处理开始','从匹配前缀之后继续'][row],11)
        save(f,'cache-restart')
        f,a=plot(3.9);n=np.arange(0,41)
        for extra,c in [(0,'#267398'),(1,'#a56c28')]:a.plot(n,n*.4-data['12-7']['preparation_s']-extra,label=f'恢复 {1+extra} s',color=c)
        a.axhline(0,color='#666');a.set(xlabel='迁移后完成轮数',ylabel='累计净节省（s）');a.legend(frameon=False);save(f,'7-migration')
        # A layer's reductions are separate handoffs with two matching participants.
        for ffn,name in [(False,'8-sync'),(True,'sync-ffn')]:
            f,a=canvas(4.1);text(a,.5,.94,'前馈输出汇总后，进入下一层' if ffn else '注意力输出汇总后，进入前馈',13,ha='center')
            for row in range(2):
                y=.62-row*.36;box(a,.04,y,.29,.20,('FFN' if ffn else '注意力')+f'分片 {row}','blue',11);box(a,.68,y,.28,.20,'下一层' if ffn else '前馈计算','green',11);arrow(a,(.33,y+.10),(.68,y+.10))
            arrow(a,(.50,.72),(.50,.36));arrow(a,(.54,.36),(.54,.72));text(a,.54,.11,'两卡归约输出',11,ha='center');save(f,name)
        f,a=plot(3.8,left=.18);cycle=data['12-9']['cycle_s']*1000
        for i in range(3):
            a.barh(0,25.6,left=i*cycle,height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(0,100,left=i*cycle+25.6,height=.5,color=COL['gray'],edgecolor=COL['line'])
        a.set(yticks=[0],yticklabels=['发送端'],xlabel='时间（ms）',xlim=(0,380));text(a,20,.6,'发 25.6 ms',11);text(a,60,-.6,'等整批确认 100 ms',11);a.set_ylim(-1,1);save(f,'9-window')
        for order,name in [(False,'10-transport'),(True,'transport-per-stream')]:
            f,a=plot(3.2,left=.20)
            for row,ready,done,c in [(1,3,3 if order else 7,'blue'),(0,7,7,'green')]:
                a.barh(row,ready,height=.5,color=COL[c],edgecolor=COL['line'])
                if done>ready:a.barh(row,done-ready,left=ready,height=.5,color=COL['gray'],edgecolor=COL['line'])
                a.plot(done,row,'o',color='#454545')
            a.set(yticks=[1,0],yticklabels=['音频','图片'],xlim=(0,8),xlabel='数据交给应用的时刻（s）');save(f,name)
        f,a=plot(4.0,left=.20)
        for row,parts in enumerate(data['12-11']['exchange_components_us']):
            start=0
            for v,c,l in zip(parts,['gray','blue','orange','green'],['接入等待','数据帧','SIFS','MAC ACK']):a.barh(row,v,left=start,height=.5,color=COL[c],edgecolor=COL['line'],label=l if row==0 else None);start+=v
        a.set(yticks=[0,1],yticklabels=['数据交换','反馈交换'],xlabel='空口占用（μs）',ylim=(-.5,2.4));a.legend(ncol=2,frameon=False,loc='upper left');save(f,'11-wireless')
        f,a=canvas(4.4);box(a,.30,.73,.40,.18,'用户发出取消','orange')
        for x,l,c in [(.04,'本地：清空播放缓冲','blue'),(.57,'远端：停止生成与发送','green')]:box(a,x,.30,.39,.23,l,c,11);arrow(a,(.5,.73),(x+.195,.53),'control')
        text(a,.235,.15,'立即停止播放',11,ha='center');text(a,.765,.15,'控制消息到达后执行',11,ha='center');save(f,'cancel-paths')
        for shared,name in [(False,'multipath-independent'),(True,'12-multipath')]:
            f,a=canvas(4.6);box(a,.04,.39,.23,.21,'30 MB 图片','blue',11)
            for y,l in [(.72,'20 MB／20 Mbit/s'),(.15,'10 MB／10 Mbit/s')]:box(a,.38,y,.40,.17,l,'green',11);arrow(a,(.27,.5),(.38,y+.085))
            if shared:box(a,.82,.37,.15,.25,'共同\n出口','orange',11);arrow(a,(.78,.805),(.89,.62));arrow(a,(.78,.235),(.89,.37));text(a,.5,.05,'共同出口 24 Mbit/s → 至少 10 s',11,ha='center')
            else:text(a,.5,.05,'两路独立：均在 8 s 发完自己的部分',11,ha='center')
            save(f,name)
        for i,row in enumerate(data['12-13']['matched_ASR_ms']):
            f,a=plot(3.8);a.bar([0,1],np.array(row)/1000,color=[COL['blue'],COL['green']],edgecolor=COL['line'])
            for j,v in enumerate(row):a.text(j,v/1000+.03,f'{v:.1f} ms',fontsize=12,ha='center')
            a.set(xticks=[0,1],xticklabels=['直接路径','Queqiao'],ylabel='请求中位数（s）',ylim=(0,1.4));save(f,'13-queqiao' if i==0 else 'queqiao-tuned')
        f,a=canvas(4.7);text(a,.04,.94,'单因素实验设计：每步只改变一个设置',13)
        for row,(l,c) in enumerate([('连接复用 → 握手与首字节时刻','blue'),('窗口设置 → 在途量与确认时刻','green'),('发送节奏 → 出口空闲与完成时刻','orange')]):box(a,.04,.68-row*.26,.92,.18,l,c,12)
        save(f,'experiment-design')
        for i,row in enumerate(data['12-14']['seconds']):
            f,a=plot(3.6,left=.18);start=0
            for v,c,l in zip(row,['gray','orange','green','purple','blue'],['准备','终端','模型','传播','上传']):
                if v:a.barh(0,v,left=start,height=.5,color=COL[c],edgecolor=COL['line'],label=l)
                start+=v
            a.axvline(45,ls='--',color='#a56c28');a.set(yticks=[0],yticklabels=[['端侧','附近','云端'][i]],xlabel='剩余二十轮完成时间（s）',xlim=(0,68),ylim=(-.6,1.6));a.legend(ncol=3,frameon=False,loc='upper left');save(f,'14-budgets' if i==0 else 'budgets-'+str(i))
        f,a=plot(4.0);b=np.array(data['12-15']['scan_Mbps']);a.plot(b,27+128/b,color='#267398',label='云端');a.axhline(41,color='#388768',label='附近：41 s');a.axhline(45,ls='--',color='#a56c28',label='期限：45 s');a.set(xlabel='云上行（Mbit/s）',ylabel='二十轮完成时间（s）');a.legend(frameon=False);save(f,'15-deployment')
        for retained,name in [(True,'16-recovery'),(False,'recovery-all')]:
            f,a=canvas(4.2);text(a,.04,.94,'已执行十轮；恢复连接需 1 s',14)
            for i in range(10):box(a,.04+i%5*.187,.66-(i//5)*.22,.17,.15,str(i+1),'green' if retained and i<9 else 'orange',12)
            text(a,.5,.22,'保留前九轮，只重做第十轮' if retained else '进度丢失，重做十轮',12,ha='center');text(a,.5,.08,'额外 1 + 1.9 = 2.9 s' if retained else '额外 1 + 10 × 1.9 = 20 s',12,ha='center');save(f,name)
    out.finish();return out.outputs,out.checks
