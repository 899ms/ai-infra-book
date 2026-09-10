"""Work arrives, waits, and releases state: book-size diagrams for chapter 3."""
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
        f,a=canvas(4.4);text(a,.04,.94,'恢复 6144 位置，处理 2048 个新输入',14)
        for i,n in enumerate(data['3-1']['slots_after_calls']):
            y=.71-i*.20;box(a,.04,y,.40,.13,'prefill' if i==0 else f'decode {i}','orange' if i==0 else 'blue')
            box(a,.60,y,.36,.13,f'保留 {n} 个位置','green');arrow(a,(.44,y+.065),(.60,y+.065))
            text(a,.04,y-.04,f'产生第 {i+1} 个输出',11)
        save(f,'1-stages')

        f,a=canvas(3.4);text(a,.04,.93,'同一条请求的三个观察时刻',14)
        arrow(a,(.06,.60),(.95,.60))
        for x,label in [(.12,'请求到达'),(.43,'首个输出'),(.87,'最后输出')]:
            a.plot([x,x],[.57,.63],color=COL['line']);text(a,x,.73,label,12,ha='center')
        box(a,.12,.36,.31,.12,'首响应 TTFT','blue',11);box(a,.43,.36,.44,.12,'后续输出间隔','green')
        box(a,.12,.14,.75,.12,'完整请求时间','orange');save(f,'request-clocks')
        f,a=plot(3.1)
        a.fill_between([0,10],[1,1],color=COL['blue'],edgecolor=COL['line']);a.set(xlim=(0,12),ylim=(0,1.5),xlabel='工具等待（s）',ylabel='状态占用（GiB）',yticks=[0,.5,1])
        a.text(5,.5,'1 GiB × 10 s\n= 10 GiB·s',ha='center',va='center',fontsize=14);save(f,'state-time-area')

        d=data['3-2'];f,a=plot(3.5,left=.18)
        A=np.array(d['A_fraction']);a.bar(range(3),A,color=COL['blue'],edgecolor=COL['line'],label='长输入类');a.bar(range(3),1-A,bottom=A,color=COL['orange'],edgecolor=COL['line'],label='长输出类')
        a.set(xticks=range(3),xticklabels=['均匀混合','变化前窗','变化后窗'],ylim=(0,1.3),ylabel='请求比例');a.legend(ncol=2,frameon=False,loc='upper center');save(f,'2-workload-budget')
        f,a=plot(3.5);x=np.arange(3)
        for dx,key,label,col in [(-.18,'prefill_positions_per_second','输入位置','blue'),(.18,'decode_positions_per_second','后续 decode','orange')]:a.bar(x+dx,d[key],width=.34,label=label,color=COL[col],edgecolor=COL['line'])
        a.set(xticks=x,xticklabels=['均匀混合','变化前窗','变化后窗'],ylabel='每秒阶段位置数',ylim=(0,37000));a.legend(frameon=False);save(f,'stage-demand')
        f,a=canvas(2.8);box(a,.03,.46,.24,.22,'新到工作','orange');box(a,.39,.46,.24,.22,'待处理队列','blue');box(a,.75,.46,.22,.22,'完成工作','green');arrow(a,(.27,.57),(.39,.57));arrow(a,(.63,.57),(.75,.57));text(a,.5,.23,'到来速度超过处理速度，队列就增长',12,ha='center');save(f,'queue-mechanism')
        q=d['fluid_queue'];f,a=plot(3.6)
        a.plot(q['seconds'],q['backlog_steps'],'o-',color='#a56c28');a.axvline(120,ls='--',lw=1,color='#555555')
        a.annotate('79,632 步',(120,79632),xytext=(48,88000),arrowprops={'arrowstyle':'->'},fontsize=12)
        a.set(xlim=(0,150),ylim=(0,100000),xlabel='从开始到达计时（s）',ylabel='待处理 decode 步');save(f,'queue-backlog')
        f,a=plot(3.6);rows=d['arrival_reports'];x=np.arange(2)
        for dx,key,label,col in [(-.18,'ttft_p95_s','首响应 p95','blue'),(.18,'latency_p95_s','完整请求 p95','green')]:a.bar(x+dx,[r[key] for r in rows],width=.34,label=label,color=COL[col],edgecolor=COL['line'])
        a.set(xticks=x,xticklabels=['均匀混合','时段变化'],ylabel='客户端时间（s）',ylim=(0,390));a.legend(frameon=False);save(f,'arrival-measured')

        d=data['teaching_diagrams']['success_cost'];f,a=canvas(3.6)
        for y,title,cost,success,c in [(.58,'原策略',100,50,'blue'),(.17,'新策略',200,80,'orange')]:
            box(a,.03,y,.28,.21,title,c);box(a,.41,y,.55,.21,f'{cost} 成本 ÷ {success} 次成功\n= {cost/success:g} 成本／成功',c)
            arrow(a,(.31,y+.105),(.41,y+.105))
        text(a,.5,.93,'两种策略各尝试 100 次',14,ha='center');save(f,'success-cost')
        rounds=data['3-3']['rounds'];bars('3-agent',['第 1 轮：截断','第 2 轮：写文件','第 3 轮：测试','第 4 轮：结束'],[r['measured_model_seconds'] for r in rounds],'每轮模型墙钟时间（s）')
        f,a=canvas(3.4);text(a,.04,.94,'公共前缀保留一份，分支各自追加',14)
        box(a,.06,.39,.35,.21,'公共前缀','blue')
        for y,label in [(.68,'分支 A 尾部'),(.16,'分支 B 尾部')]:box(a,.62,y,.31,.15,label,'orange');arrow(a,(.41,.495),(.62,y+.075))
        save(f,'branch-state')
        for parallel,name in [(False,'tool-dependency'),(True,'tool-parallel')]:
            f,a=plot(3.5,left=.16)
            stages=[(0,2,0,'模型','blue'),(2,6,1,'工具 A','orange'),(2 if parallel else 8,10,2,'工具 B','green'),(12 if parallel else 18,3,0,'模型','blue')]
            for start,dur,y,label,col in stages:
                a.barh(y,dur,left=start,height=.5,color=COL[col],edgecolor=COL['line']);a.text(start+dur/2,y,str(dur)+' s',ha='center',va='center',fontsize=12)
            a.set(yticks=[0,1,2],yticklabels=['模型','工具 A','工具 B'],xlim=(0,22),ylim=(-.6,2.6),xlabel='任务时间（s）');a.invert_yaxis();save(f,name)

        f,a=canvas(4.0);text(a,.04,.94,'图像先成为位置，再成为语言模型输入',14)
        for y,label,c in [(.69,'640 × 640 像素图像','gray'),(.43,'16 × 16 像素一块 → 40 × 40 个块','blue'),(.17,'相邻 2 × 2 块合并 → 20 × 20 个位置','green')]:
            box(a,.07,y,.86,.15,label,c)
            if y>.2:arrow(a,(.5,y),(.5,y-.10))
        save(f,'vision-shapes')
        f,a=canvas(3.9);text(a,.04,.94,'400 个位置，各自携带特征向量',14)
        box(a,.04,.63,.92,.17,'四组视觉特征：每组宽 2560','blue')
        box(a,.04,.37,.92,.17,'编码结果：400 × 4 × 2560 × 2 bytes','green');arrow(a,(.5,.63),(.5,.54))
        box(a,.04,.08,.92,.17,'进入语言主干后，另产生各层 KV','orange');arrow(a,(.5,.37),(.5,.25));save(f,'vision-state')
        f,a=canvas(4.3);text(a,.04,.94,'从输入表示到可听见的声音',14)
        for i,(label,c) in enumerate([('视觉或音频编码：形成模型输入','blue'),('语言模型：理解并生成回复','green'),('声学生成与解码：产生音频采样','orange'),('接收缓冲与播放设备：输出声音','purple')]):
            y=.73-i*.205;box(a,.06,y,.88,.13,label,c)
            if i<3:arrow(a,(.5,y),(.5,y-.075))
        save(f,'4-realtime')
        d=data['3-4'];f,a=plot(4.8,left=.17,bottom=.15)
        for z in d['audio_chunks']:
            i=z['chunk'];a.barh(i,20,left=z['playback_start_ns']/1e6,height=.48,color=COL['green'],edgecolor=COL['line']);a.plot(z['arrival_ns']/1e6,i,'o',color='#267398');a.plot(z['deadline_ns']/1e6,i,'|',markersize=14,color='#a56c28')
        a.plot([],[],'o',color='#267398',label='到达');a.plot([],[],'|',color='#a56c28',label='原定播放');a.barh([],[],color=COL['green'],edgecolor=COL['line'],label='实际播放')
        a.set(yticks=range(8),yticklabels=[f'块 {i+1}' for i in range(8)],xlim=(0,260),ylim=(-1.5,7.6),xlabel='从采集起点计时（ms）');a.invert_yaxis();a.legend(ncol=3,fontsize=11,frameon=False,loc='upper left');save(f,'audio-timing')
        f,a=canvas(2.8);text(a,.04,.92,'发出打断与停止发声是两个事件',14)
        box(a,.04,.40,.36,.24,'123 ms\n发出打断','orange');box(a,.60,.40,.36,.24,'130 ms\n本地设备静音','green');arrow(a,(.40,.52),(.60,.52));text(a,.5,.18,'间隔 7 ms；旧音频在此期间继续播放',12,ha='center');save(f,'audio-interrupt')

        f,a=canvas(4.1);text(a,.04,.94,'先计算输出，再沿依赖反向传梯度',14)
        for x,label,c in [(.04,'前层','blue'),(.38,'当前层','orange'),(.72,'后层','green')]:box(a,x,.64,.24,.16,label,c)
        arrow(a,(.28,.74),(.38,.74));arrow(a,(.62,.74),(.72,.74));text(a,.50,.86,'前向：输入 → 输出',11,ha='center')
        arrow(a,(.72,.48),(.62,.48));arrow(a,(.38,.48),(.28,.48));text(a,.5,.39,'反向：后一层梯度 → 前一层梯度',12,ha='center')
        box(a,.23,.10,.54,.14,'当前层另算权重梯度，用于更新','purple',11);arrow(a,(.5,.45),(.5,.24));save(f,'5-training')
        f,a=plot(3.2,left=.20)
        for y,start,duration,label,c in [(0,0,1,'前向','blue'),(0,3,1,'反向','orange'),(1,1,3,'保存激活','green')]:
            a.barh(y,duration,left=start,height=.5,color=COL[c],edgecolor=COL['line']);a.text(start+duration/2,y,label,fontsize=12,ha='center',va='center')
        a.set(yticks=[0,1],yticklabels=['该层计算','该层激活'],xlim=(-.1,4.3),ylim=(-.7,1.7),xticks=[0,1,3,4],xticklabels=['开始','前向完成','反向开始','反向完成'],xlabel='事件次序（间距仅作示意）');a.invert_yaxis();save(f,'activation-lifetime')
        t=data['3-5'];bars('training-flops',['前向','反向','前向加反向','总参数 6ND'],[t['summary'][k]/1e12 for k in ['forward_matrix_flops','backward_matrix_flops','training_matrix_flops','six_nd_flops']],'矩阵运算量（TFLOPs）')
        bars('training-states',['BF16 权重','FP32 梯度','FP32 主权重','Adam 一阶矩','Adam 二阶矩'],[v/1e9 for v in t['parameter_state_bytes'].values()],'参数相关状态（GB）',4.0)

        f,a=canvas(4.6);text(a,.04,.94,'生成、反馈和学习使用同一批轨迹',14)
        for i,(label,c) in enumerate([('策略生成回答','blue'),('规则、模型或环境给出反馈','orange'),('筛选样本，组织训练输入','green'),('学习器计算梯度，更新策略','purple')]):
            y=.73-i*.20;box(a,.16,y,.79,.13,label,c)
            if i<3:arrow(a,(.55,y),(.55,y-.07))
        a.plot([.16,.04,.04,.16],[.195,.195,.795,.795],color=COL['line'],lw=1);arrow(a,(.04,.795),(.16,.795))
        text(a,.05,.045,'左侧返回路径：新权重交给下一批生成',11);save(f,'6-rl')
        d=data['3-6'];f,a=plot(3.8,left=.21);names=['rollout_prefill','rollout_decode','reference_scoring','policy_update'];labs=['生成输入','后续生成','参考评分','策略更新'];x=np.arange(4)
        for dx,key,col,label in [(-.18,'base_stages','blue','生成 32，保留 16'),(.18,'low_acceptance_stages','orange','生成 64，保留 16')]:
            vals=[next(z['matrix_flops']/1e12 for z in d[key] if z['name']==name) for name in names];a.bar(x+dx,vals,width=.34,color=COL[col],edgecolor=COL['line'],label=label)
        a.set(xticks=x,xticklabels=labs,ylabel='矩阵运算量（TFLOPs）',ylim=(0,1650));a.legend(frameon=False);save(f,'rl-stage-work')

        d=data['3-7'];f,a=plot(3.8);a.plot([2,7.6],[2,7.6],color='#999999',lw=1)
        for split,col,marker,lab in [('fit','#267398','o','拟合六点'),('holdout','#a56c28','^','留出两点')]:
            rows=[z for z in d['records'] if z['split']==split];law=d['law'];pred=[law['E']+law['A']*(z['N']/law['N0'])**(-law['alpha'])+law['B']*(z['D']/law['D0'])**(-law['beta']) for z in rows];a.scatter([z['loss'] for z in rows],pred,color=col,marker=marker,label=lab)
        a.set(xlim=(2,7.6),ylim=(2,7.6),xlabel='观测损失（nats/token）',ylabel='预测损失（nats/token）');a.legend(frameon=False);save(f,'7-scaling')
        f,a=plot(3.1);res=d['residuals'];a.bar(range(8),[z['residual'] for z in res],color=[COL['blue'] if z['split']=='fit' else COL['orange'] for z in res],edgecolor=COL['line']);a.axhline(0,lw=.8,color='#555555');a.set(xticks=range(8),xticklabels=['F1','F2','F3','F4','F5','F6','H1','H2'],xlabel='F：拟合点；H：留出点',ylabel='预测减观测（nats/token）');save(f,'scaling-residual')
        f,a=plot(3.8);calls=np.linspace(0,4e8,200)
        for r,col in zip(d['lifecycle']['rows'],['#a56c28','#388768','#267398','#777777']):a.plot(calls/1e8,r['upfront_cost']+calls*r['cost_per_call'],color=col,ls='--' if r['outside_fit_box'] else '-',label=f"{r['N']/1e9:g}B"+(' 外推' if r['outside_fit_box'] else ''))
        a.axvline(d['crossing_calls']/1e8,color='#777777',lw=.8);a.set(xlim=(0,4),ylim=(0,1650),xlabel='累计调用（亿次）',ylabel='累计成本（题设单位）');a.legend(frameon=False);save(f,'lifecycle-cost')
        d=data['3-8'];bars('8-history',['Llama 1 6.7B','Llama 2 7B','Llama 3.1 8B','Qwen2.5 7B','Qwen3 8B'],d['ratios'],'报告训练 token 数／参数数',4.0)
        f,a=plot(3.7,left=.26);ctx=[r['parameter_context'] for r in d['moe_rows']];y=np.arange(3)
        for dy,key,col,label in [(-.16,'total_reported','blue','总参数'),(.16,'active_reported','orange','激活参数')]:a.barh(y+dy,[r[key]/1e9 for r in ctx],height=.29,color=COL[col],edgecolor=COL['line'],label=label)
        a.set(yticks=y,yticklabels=['DeepSeek-V3','DeepSeek\nV4-Flash','DeepSeek\nV4-Pro'],xlabel='参数数（十亿）',xlim=(0,1900));a.invert_yaxis();a.legend(frameon=False);save(f,'moe-history')
        hist={r['input']['id']:r for r in data['3-9']['history_rows']}
        for ids,name in [(['llama1-7b','llama1-65b','llama2-7b','llama2-70b'],'9-gpu-hours'),(['llama31-8b','llama31-70b','llama31-405b'],'h100-hours')]:
            bars(name,[k.replace('llama31','Llama 3.1').replace('llama1','Llama 1').replace('llama2','Llama 2').replace('-',' ') for k in ids],[hist[k]['input']['gpu_hours']/1e6 for k in ids],'公开训练用量（百万 GPU 小时）')
        parts=data['3-9']['stage_reports'][0]['input']['parts'];bars('v3-stage-hours',['DeepSeek-V3\n预训练','上下文扩展','后训练'],[parts[k]/1e6 for k in ['pretraining','context_extension','posttraining']],'H800 用量（百万 GPU 小时）')
    from v41_case_figures import draw as draw_v41
    draw_v41(3, out)
    return out.finish()
