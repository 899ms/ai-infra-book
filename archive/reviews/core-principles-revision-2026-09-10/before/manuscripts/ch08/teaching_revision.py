"""Request iterations, physical KV blocks and service outcomes."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-8-'+n)
    with plt.rc_context(STYLE):
        f,a=canvas(4.7);text(a,.04,.94,'请求保持身份，批次每轮重新组成',14)
        for row,labels in enumerate([['请求 A','请求 B'],['请求 A','请求 C']]):
            y=.60-row*.36;text(a,.04,y+.17,f'迭代 {row}',12)
            for i,label in enumerate(labels):box(a,.25+i*.37,y,.30,.20,label,'blue' if label=='请求 A' else 'green',12)
        text(a,.5,.08,'B 已结束 → 空出的执行位置交给 C',12,ha='center');save(f,'request-iterations')
        f,a=plot(3.0,left=.12);start=0
        for dur,l,c in [(.1,'排队','gray'),(.3,'prefill','blue'),(2.55,'decode','green')]:a.barh(0,dur,left=start,height=.35,color=COL[c],edgecolor=COL['line'],label=l);start+=dur
        a.scatter([.4,2.95],[0,0],color='#252525',zorder=5);a.axvline(3,ls='--',color='#a56c28');a.set(yticks=[],xlim=(0,3.15),xlabel='从到达起计时（s）');a.legend(ncol=3,frameon=False,loc='upper center');save(f,'1-lifecycle')
        f,a=plot(3.7);b=np.array(data['batch']['batch']);w=data['batch']['shared_weight_bytes']/2**30/b
        for L,c in [(2048,'#267398'),(8192,'#388768')]:a.plot(b,w+L*144/2**20,color=c,label=f'{L} 位置上下文');a.axhline(L*144/2**20,color=c,ls=':')
        a.plot(b,w,ls='--',color='#777777',label='共享权重项');a.set(xscale='log',yscale='log',xlabel='批内请求数',ylabel='每输出读取量（GiB）');a.legend(frameon=False);save(f,'2-batch')
        for i,key in enumerate(['fixed','continuous','chunked']):
            f,a=plot(3.8,left=.16)
            for step in data[key]:
                for plan in step['plans']:
                    lane=int(plan['request'][1:]);a.barh(lane,step['duration_ns']/1000,left=step['start_ns']/1000,height=.55,color=COL['blue' if plan['phase']=='prefill' else 'green'],edgecolor=COL['line'],linewidth=.45)
            a.scatter([0,0,20,30],range(4),marker='^',color='#252525',s=18,zorder=5);a.set(yticks=range(4),yticklabels=[f'r{j}' for j in range(4)],xlim=(0,330),xlabel='教学时间（μs）');a.invert_yaxis();save(f,'3-scheduling' if i==0 else f'scheduling-{key}')
        for i,d in enumerate(data['attention_geometry']):
            f,a=canvas(3.5);h=d['history'];step=.065;start=.15
            for row in range(4):
                for col in range(h+4):box(a,start+col*step,.65-row*.13,step-.008,.105,'','blue' if col<h else ('green' if col-h<=row else 'white'))
            text(a,.04,.91,f'旧上下文 {h} + 新位置 4',14);text(a,.5,.12,f'旧上下文配对 {4*h} + 块内配对 10 = {4*h+10}',12,ha='center');save(f,'4-attention' if i==0 else 'attention-history')
        f,a=canvas(4.5);text(a,.04,.94,'逻辑块按序排列，物理块分散存放',14)
        for i,target in enumerate([2,0,3]):
            x=.06+i*.31;box(a,x,.68,.24,.13,f'逻辑块 {i}','blue',11);text(a,x+.12,.54,f'块表：{i} → {target}',11,ha='center');arrow(a,(x+.12,.46),(.14+target*.235,.31))
        for i in range(4):box(a,.04+i*.235,.12,.20,.18,f'物理块 {i}','green' if i in [0,2,3] else 'gray',11)
        save(f,'page-map')
        for mode,name in [('reserved','5-pages'),('paged','pages-paged')]:
            f,a=canvas(4.6)
            for row,L in enumerate(data['pages']['lengths']):
                y=.70-row*.18;text(a,.03,y+.04,f'{"ABCD"[row]}：{L}',11)
                slots=16 if mode=='reserved' else (L+3)//4*4
                for j in range(slots):box(a,.19+j*.047,y,.039,.10,'','blue' if j<L else 'gray')
            text(a,.5,.05,f'共分配 {64 if mode=="reserved" else 52} 个位置',13,ha='center');save(f,name)
        f,a=canvas(4.4);box(a,.04,.67,.27,.15,'A 的块表','blue');box(a,.69,.67,.27,.15,'B 的块表','green');box(a,.31,.34,.38,.16,'两个共同前缀块\n各有两个引用','purple',11)
        arrow(a,(.175,.67),(.40,.50));arrow(a,(.825,.67),(.60,.50));box(a,.03,.07,.28,.13,'A 私有后缀','blue',11);box(a,.69,.07,.28,.13,'B 私有后缀','green',11);arrow(a,(.175,.67),(.175,.20));arrow(a,(.825,.67),(.825,.20));save(f,'pages-shared')
        f,a=canvas(4.3);box(a,.25,.70,.50,.16,'共享尾块：[a, b, c, 空]','purple',12)
        for x,label,c in [(.03,'分支 A：[a, b, c, x]','blue'),(.54,'分支 B：[a, b, c, y]','green')]:box(a,x,.20,.43,.19,label,c,11);arrow(a,(.5,.70),(x+.215,.39))
        text(a,.5,.52,'写入分歧前，取得各自的尾块副本',12,ha='center');save(f,'copy-on-write')
        f,a=canvas(4.3)
        for row,(label,count,col) in enumerate([('A、B 使用共同块',2,'purple'),('A 结束，B 继续使用',1,'green'),('B 结束，设备已用完',0,'gray')]):
            y=.69-row*.27;box(a,.04,y,.61,.17,label,col,11);box(a,.75,y,.21,.17,f'引用 {count}',col,11)
            if row<2:arrow(a,(.86,y),(.86,y-.10))
        save(f,'reference-release')
        f,a=canvas(4.2)
        for x,l,c in [(.03,'收到取消\n停止后续迭代','orange'),(.37,'等待已提交\n设备操作完成','blue'),(.71,'释放私有块\n更新共享引用','green')]:box(a,x,.41,.26,.27,l,c,11)
        arrow(a,(.29,.54),(.37,.54));arrow(a,(.63,.54),(.71,.54));text(a,.5,.18,'取消调用返回 1.6 ms；块释放约 31 ms',11,ha='center');save(f,'cancel-lifetime')
        # Exact common-prefix lengths; tree topology is drawn by logical depth.
        d=data['prefix'];f,a=canvas(4.5);positions={0:(.12,.50),1:(.38,.83),2:(.38,.40),3:(.63,.63),4:(.63,.24),5:(.86,.39),6:(.86,.10)}
        for u,v,n in d['edges']:
            arrow(a,positions[u],positions[v]);x=(positions[u][0]+positions[v][0])/2;y=(positions[u][1]+positions[v][1])/2;text(a,x,y+.065,f'+{n}',11,ha='center')
        for i,node in enumerate(d['tree']):
            x,y=positions[i];a.plot(x,y,'o',color='#267398',ms=5)
            if len(node['ids'])==1:text(a,x,y+.09,f'轮 {node["ids"][0]+1}',11,ha='center')
        text(a,.04,.95,'前四轮：从共同 206 个 token 开始',14);text(a,.5,.03,'边上数字：新增 token 数',11,ha='center');save(f,'6-prefix')
        f,a=plot(3.8);v=np.array(d['adjacent_lcp']);a.bar(range(1,13),v,color=COL['blue'],label='与上一轮共同前缀');a.bar(range(1,13),np.array(d['input_lengths'])-v,bottom=v,color=COL['orange'],label='其余输入');a.set(xlabel='输入轮次',ylabel='token 数',xticks=[1,3,6,9,12]);a.legend(frameon=False);save(f,'prefix-lengths')
        f,a=canvas(3.8);text(a,.04,.94,'文本匹配到 10752，状态从 8192 恢复',13);a.plot([.05,.95],[.48,.48],color='#777777')
        for x,label,c in [(.10,'4096\n快照','blue'),(.48,'8192\n最近快照','green'),(.85,'10752\n匹配末端','orange')]:box(a,x-.07,.39,.17,.22,label,c,11)
        arrow(a,(.57,.49),(.77,.49));text(a,.68,.22,'重算 2560 个位置',12,ha='center');save(f,'prefix-restore')
        f,a=canvas(4.1)
        for row in range(2):
            y=.63-row*.40
            if row==0:box(a,.04,y,.92,.19,'A：864 MiB，净节省 36 ms','blue')
            else:
                for i in range(3):box(a,.04+i*.31,y,.30,.19,'B：288 MiB\n24 ms','green',11)
            text(a,.5,y-.09,f'合计节省 {36 if row==0 else 72} ms',12,ha='center')
        save(f,'7-cache-choice')
        f,a=plot(3.5,left=.20)
        for i,(payload,scale) in enumerate(zip(data['kv_layout']['payload_bytes'],data['kv_layout']['scale_bytes'])):a.barh(i,payload,height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(i,scale,left=payload,height=.5,color=COL['orange'],edgecolor=COL['line'])
        a.set(yticks=range(3),yticklabels=['BF16','q8_0','q4_0'],xlim=(0,68),xlabel='保存同一组 32 个值（bytes）');a.invert_yaxis();save(f,'8-kv-format')
        f,a=plot(3.6,left=.23)
        for i,buff in enumerate([288,576]):a.barh(i,buff,height=.48,color=COL['orange'],edgecolor=COL['line']);a.barh(i,2592-buff,left=buff,height=.48,color=COL['green'],edgecolor=COL['line'])
        a.set(yticks=[0,1],yticklabels=['一组预取缓冲','两组预取缓冲'],xlim=(0,2800),xlabel='卸载腾出的空间（MiB）');a.invert_yaxis();save(f,'9-offload')
        f,a=plot(3.5);v=data['offload']['copy_ms'];a.bar([0,1],v,color=[COL['blue'],COL['green']],edgecolor=COL['line']);a.set(xticks=[0,1],xticklabels=['24 GiB/s','384 GiB/s'],ylabel='每轮复制下界（ms）',ylim=(0,120));save(f,'offload-copy')
        for i,m in enumerate(data['kv']['correct_by_task']):
            f,a=plot(4.7,left=.25);a.imshow(m,cmap=ListedColormap([COL['orange'],COL['green']]),vmin=0,vmax=1,aspect='auto')
            for y,row in enumerate(m):
                for x,val in enumerate(row):a.text(x,y,'○' if val else '×',ha='center',va='center',fontsize=14)
            a.set(yticks=range(8),yticklabels=[f'任务 {j+1}' for j in range(len(data['kv']['task_ids']))],xticks=range(4),xticklabels=['1 / 1','1 / 2','4 / 1','4 / 2'],xlabel='并发数 / 重复序号');save(f,'10-kv-quality' if i==0 else f'kv-quality-{i}')
        f,a=canvas(4.6)
        for row,(title,tokens) in enumerate([('草稿',['a','b','c','d']),('验证',['a','b','x','丢弃']),('保留',['a','b','x'])]):
            y=.71-row*.28;text(a,.03,y+.065,title,12)
            for j,t in enumerate(tokens):box(a,.21+j*.19,y,.16,.14,t,'green' if j<2 else ('orange' if row==0 or t=='丢弃' else 'blue'),12)
        save(f,'11-verification')
        for draft,n in [('A','sample-A'),('B','sample-B')]:
            p=.25 if draft=='A' else .75;f,a=canvas(4.0);box(a,.32,.71,.36,.17,f'草稿恒为 {draft}','gray')
            for x,label,prob,c in [(.03,'接受 '+draft,p,'green'),(.54,'拒绝，输出 '+('B' if draft=='A' else 'A'),1-p,'orange')]:box(a,x,.18,.43,.19,label,c,12);arrow(a,(.5,.71),(x+.215,.37));text(a,x+.215,.48,f'概率 {prob:g}',12,ha='center')
            text(a,.5,.06,'最终：P(A) = 1/4，P(B) = 3/4',12,ha='center');save(f,n)
        f,a=plot(3.6);q=np.linspace(0,2,100)
        for d,c in zip(data['speculation']['drafts'],['#267398','#388768']):a.plot(q,(1.4+q)/d['expected_output'],color=c,label=d['draft'])
        a.axhline(1,color='#777777',ls='--',label='普通 decode');a.set(xlabel='每轮草稿查询（ms）',ylabel='每输出 token 耗时（ms）');a.legend(frameon=False);save(f,'12-speculation')
        for field,name in [('completed_per_s','13-service'),('slo_goodput_per_s','service-goodput')]:
            f,a=plot(4.0,bottom=.28);groups=data['service']['groups'];labels=[]
            for i,g in enumerate(groups):
                vals=[x[field] for x in g];a.bar(i,np.median(vals),color=COL['blue' if field=='completed_per_s' else 'green'],edgecolor=COL['line']);a.scatter([i]*len(vals),vals,color='#252525',s=16);labels.append(('逐个' if g[0]['service']=='serial' else '连续' if g[0]['service']=='continuous' else '突发')+('\n'+str(g[0]['rate']) if g[0]['rate'] is not None else '\n一次到达'))
            a.set(xticks=range(len(groups)),xticklabels=labels,ylim=(0,3.1),ylabel='完成吞吐（req/s）' if field=='completed_per_s' else '正确且按期完成（req/s）',xlabel='接纳策略；下行为到达率（req/s）');save(f,name)
        f,a=plot(3.8);a.fill_between([0,12],0,3,color=COL['green'],alpha=.65)
        for c in data['design_plane']['configurations']:a.scatter(c['memory_gib'],c['time_s'],color='#267398');a.annotate(c['name'],(c['memory_gib'],c['time_s']),xytext=(5,5),textcoords='offset points',fontsize=12)
        a.axvline(12,ls='--',color='#777777');a.axhline(3,ls='--',color='#777777');a.set(xlim=(0,21),ylim=(0,4.1),xlabel='KV 与辅助缓冲（GiB）',ylabel='整组完成时间（s）');save(f,'14-design')
        f,a=plot(3.6);s=np.array(data['task']['local_speedups'])
        for frac,col in zip(data['task']['decode_fractions'],['#267398','#388768','#a56c28']):a.plot(s,1/(1-frac+frac/s),label=f'decode 占 {frac:.0%}',color=col)
        a.set(xlabel='decode 加速比',ylabel='完整任务加速比',xlim=(1,8));a.legend(frameon=False);save(f,'15-task')
    out.finish();return out.outputs,out.checks
