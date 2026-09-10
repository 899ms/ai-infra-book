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
        f,a=plot(3.4,left=.28)
        a.barh(range(len(values)),values,color=colors or COL['blue'],edgecolor=COL['line'],height=.55)
        a.set(yticks=range(len(values)),yticklabels=labels,xlim=(0,max(values)*1.28),xlabel=xlabel);a.invert_yaxis()
        for i,v in enumerate(values):a.text(v+max(values)*.025,i,f'{v:,.2f}',va='center',fontsize=11)
        save(f,name)
    with plt.rc_context(STYLE):
        for mode,name,title in [('rnn','1-dependencies','同层先完成前一位置'),('causal','causal-dependencies','本层各位置读取上一层的因果前缀')]:
            f,a=canvas(3.7);text(a,.04,.94,title,14)
            xs=[.23,.44,.65,.86];ys=[.18,.46,.74]
            for l,y in enumerate(ys):
                text(a,.04,y,['输入','第 1 层','第 2 层'][l],11)
                for j,x in enumerate(xs):
                    if l:
                        for k in ([j] if mode=='rnn' else range(j+1)):
                            arrow(a,(xs[k],ys[l-1]+.04),(x,y-.04))
                        if mode=='rnn' and j:arrow(a,(xs[j-1]+.035,y),(x-.035,y))
                    a.scatter(x,y,s=450,facecolor=COL['blue'],edgecolor=COL['line'],zorder=5)
            for j,x in enumerate(xs):text(a,x,.055,f'位置 {j+1}',11,ha='center')
            save(f,name)

        f,a=canvas(4.3);text(a,.04,.94,'从同一输入产生三种表示',14)
        box(a,.30,.74,.40,.12,'当前位置的隐藏向量','gray')
        for x,label,c in [(.04,'查询 Q','orange'),(.36,'键 K','blue'),(.68,'值 V','green')]:
            arrow(a,(.5,.74),(x+.14,.62));box(a,x,.46,.28,.16,label,c)
        text(a,.50,.34,'查询与键匹配，得到各位置的系数',12,ha='center')
        box(a,.09,.10,.82,.14,'按系数汇总各位置的值，形成输出','purple')
        arrow(a,(.5,.29),(.5,.25));save(f,'qkv-objects')

        f,a=canvas(3.7);text(a,.04,.94,'已有 2 个位置，再输入 3 个位置',14)
        for i in range(3):
            y=.66-i*.19;text(a,.04,y+.065,f'新位置 {i+1}',11)
            for j in range(5):
                a.add_patch(Rectangle((.29+j*.125,y),.12,.13,facecolor=COL['blue'] if j<2 else COL['green'] if j<3+i else COL['white'],edgecolor=COL['line'],lw=.8))
                if j<3+i:text(a,.35+j*.125,y+.065,'✓',12,ha='center')
        text(a,.415,.84,'已有上下文',11,ha='center');text(a,.73,.84,'本次输入',11,ha='center')
        text(a,.5,.065,'6 个旧上下文位置对 ＋ 6 个新位置对',12,ha='center');save(f,'causal-pairs')

        f,a=canvas(4.8);text(a,.04,.95,'一层先交换信息，再变换特征',14)
        stages=[('输入：每位置 4096 个数','gray'),('归一化 → 注意力 → 输出投影','blue'),('与子层输入逐元素相加','green'),('归一化 → 前馈网络','orange'),('与子层输入逐元素相加','green')]
        for i,(s,c) in enumerate(stages):
            y=.77-i*.16;box(a,.19,y,.76,.115,s,c)
            if i<4:arrow(a,(.57,y),(.57,y-.045))
        for y1,y2 in [(.77,.507),(.45,.187)]:
            a.plot([.19,.065,.065,.19],[y1+.035,y1+.035,y2,y2],color=COL['line'],lw=1)
            arrow(a,(.065,y2),(.19,y2))
        text(a,.05,.055,'左侧旁路保留子层输入，供残差相加',11);save(f,'2-layer')

        f,a=canvas(3.9);box(a,.30,.80,.40,.12,'输入 X：4096 维','gray')
        box(a,.04,.55,.40,.14,'gate 投影 → SiLU','orange');box(a,.56,.55,.40,.14,'up 投影','blue')
        arrow(a,(.5,.80),(.24,.69));arrow(a,(.5,.80),(.76,.69))
        text(a,.24,.46,'12288 维',11,ha='center');text(a,.76,.46,'12288 维',11,ha='center')
        box(a,.30,.26,.40,.13,'对应元素相乘','green');arrow(a,(.24,.43),(.4,.40));arrow(a,(.76,.43),(.6,.40))
        box(a,.20,.04,.60,.13,'down 投影：返回 4096 维','purple');arrow(a,(.5,.26),(.5,.17));save(f,'ffn-gates')

        f,a=canvas(4.2);text(a,.04,.94,'每一步追加一个位置，重读已有上下文',14)
        for i,n in enumerate([4,5,6,7]):
            y=.71-i*.18;text(a,.03,y+.05,f'第 {i+1} 步',11)
            cells(a,.22,y,n+1,w=.70,h=.12,colors=['blue']*n+['orange'])
        text(a,.5,.07,'蓝：本步读取的上下文；橙：本步追加',11,ha='center');save(f,'history')
        f,a=plot(3.4)
        B=np.arange(1,65);W=data['teaching_diagrams']['history']['shared_weight_bytes']/2**30
        a.axhline(W,color='#267398',label='共享权重');a.plot(B,B*8192*147456/2**30,color='#a56c28',label='8K 上下文 × 请求数')
        a.set(xlim=(0,64),ylim=(0,75),xlabel='批内请求数',ylabel='逻辑读取量（GiB）');a.legend(frameon=False)
        save(f,'history-batch')

        f,a=canvas(5.6)
        for row,(title,groups) in enumerate([('MHA：每个查询各有一组 KV',4),('GQA：每两个查询共用一组 KV',2),('MQA：四个查询共用一组 KV',1)]):
            top=.95-row*.32;text(a,.04,top,title,14)
            for j in range(4):
                x=.10+j*.225;box(a,x,top-.13,.15,.07,f'Q{j+1}','orange',11)
                g=j if groups==4 else j//2 if groups==2 else 0;dest=.10+(g+.5)*.825/groups
                arrow(a,(x+.075,top-.13),(dest,top-.20))
            for g in range(groups):
                x=.10+g*.825/groups;box(a,x,top-.28,.825/groups-.02,.08,f'KV {g+1}','blue',11)
        save(f,'3-sharing')
        bars('4-cache',['MHA：32 组','GQA：8 组','MQA：1 组'],data['figure_2_4']['qwen_variants_mib'],'8K 上下文状态容量（MiB）')

        f,a=canvas(4.8)
        text(a,.04,.94,'路径一：先展开每个上下文位置',14)
        box(a,.04,.69,.25,.13,'潜变量 c','blue');box(a,.38,.69,.25,.13,'展开键 K','green');box(a,.72,.69,.24,.13,'点积分数','purple')
        arrow(a,(.29,.755),(.38,.755));arrow(a,(.63,.755),(.72,.755))
        text(a,.32,.60,'上下文先计算 K = c Uₖ',12)
        text(a,.04,.46,'路径二：先变换当前查询',14)
        box(a,.04,.22,.25,.13,'当前查询 q','orange');box(a,.38,.22,.25,.13,'变换后查询','orange');box(a,.72,.22,.24,.13,'点积分数','purple')
        arrow(a,(.29,.285),(.38,.285));arrow(a,(.63,.285),(.72,.285))
        box(a,.71,.035,.25,.10,'潜变量 c','blue');arrow(a,(.835,.135),(.835,.22))
        text(a,.04,.09,'查询先计算 q Uₖᵀ',12)
        save(f,'mla-paths')
        bars('mla-capacity',['紧凑潜变量','展开各头 KV'],data['figure_2_4']['k3_mla_paths_mib'],'Kimi K3 的 24 层 MLA 状态（MiB）')

        f,a=canvas(4.3);text(a,.04,.94,'先形成压缩条目，再由查询选择',14)
        cells(a,.05,.72,8,w=.90,h=.11)
        for i in range(2):
            arrow(a,(.27+i*.45,.71),(.27+i*.45,.59));box(a,.10+i*.45,.45,.34,.13,f'压缩条目 {i+1}','green')
        text(a,.5,.35,'示例：每 4 个位置合成 1 条',11,ha='center')
        box(a,.04,.08,.25,.13,'当前查询','orange');box(a,.38,.08,.25,.13,'扫描索引','purple');box(a,.72,.08,.24,.13,'读取选中条目','green',11)
        arrow(a,(.29,.145),(.38,.145));arrow(a,(.63,.145),(.72,.145));save(f,'5-sparse')
        c=data['figure_2_5']['components'];bars('sparse-capacity',['窗口状态','压缩表示','索引条目','压缩缓冲'],[c['window_history_bytes']/2**20,c['compressed_history_bytes']/2**20,c['index_history_bytes']/2**20,data['figure_2_5']['compressor_buffer_bytes']/2**20],'DeepSeek V4-Flash 的 8K 上下文状态（MiB）')
        f,a=canvas(3.4)
        for i in range(4):
            x=.04+i*.24;box(a,x,.56,.20,.17,f'到达 {i+1}\n块内 {i+1}/4','orange' if i==3 else 'blue',11)
            if i<3:arrow(a,(x+.20,.64),(x+.24,.64))
        box(a,.62,.12,.33,.17,'发布压缩条目','green');arrow(a,(.86,.56),(.79,.29))
        text(a,.05,.28,'前三步更新同一缓冲\n第四步完成一块',12);save(f,'compression-steps')

        f,a=canvas(3.9);text(a,.04,.94,'上下文增加，状态矩阵保持同样大小',14)
        for x,title,c in [(.04,'旧状态','blue'),(.37,'新键值外积','orange'),(.70,'新状态','green')]:
            for i in range(3):
                for j in range(3):a.add_patch(Rectangle((x+j*.08,.46+i*.08),.08,.08,facecolor=COL[c],edgecolor=COL['line'],lw=.7))
            text(a,x+.12,.36,title,12,ha='center')
        text(a,.32,.58,'+',16,ha='center');text(a,.655,.58,'=',16,ha='center')
        box(a,.22,.09,.56,.13,'当前查询 × 新状态 → 输出','purple');save(f,'recurrence')

        f,a=canvas(4.1);text(a,.04,.94,'模型配置决定采用哪种注意力',14)
        box(a,.05,.62,.40,.18,'30 层线性注意力\n固定递推状态','blue');box(a,.55,.62,.40,.18,'10 层完整注意力\n逐位置上下文','green')
        box(a,.20,.34,.60,.13,'层内归一化与残差连接','gray')
        arrow(a,(.25,.62),(.4,.47));arrow(a,(.75,.62),(.6,.47))
        box(a,.06,.07,.41,.16,'路由专家：256 选 8','orange',11);box(a,.57,.07,.37,.16,'共享专家','purple')
        arrow(a,(.4,.34),(.27,.23));arrow(a,(.6,.34),(.76,.23));save(f,'6-hybrid')
        d=data['figure_2_7'];names={'qwen':'Qwen3-8B','v4':'DeepSeek\nV4-Flash','k3':'Kimi K3\n紧凑'}
        for field,name,ylabel in [('resident_bytes','7-state-growth','状态容量（GiB）'),('accounted_access_bytes','state-access','每步计入的访问量（GiB）')]:
            f,a=plot(3.8)
            for key,col in zip(names,['#267398','#388768','#a56c28']):a.plot(np.array(d['lengths'])/1024,np.array(d[field][key])/2**30,'o-',label=names[key],color=col)
            a.set(xscale='log',yscale='log',xlabel='上下文长度（千个位置，对数轴）',ylabel=ylabel+'，对数轴');a.legend(frameon=False);save(f,name)

        f,a=canvas(4.0);text(a,.04,.94,'分派次数相同，访问到的专家可以不同',14)
        for y,title,n,c in [(.58,'分散：覆盖 256 个专家',256,'blue'),(.17,'集中：覆盖 8 个专家',8,'orange')]:
            box(a,.04,y,.34,.19,'64 个 token\n每个选择 8 个','gray');arrow(a,(.38,y+.095),(.54,y+.095))
            box(a,.54,y,.42,.19,f'{n} 个专家\n每专家平均 {512/n:.0f} 行',c)
            text(a,.04,y-.07,title,12)
        save(f,'expert-reuse')

        f,a=canvas(4.3)
        for i,(title,streams) in enumerate([('普通残差：保留一条旁路',1),('mHC：保留四路，再混合返回',4)]):
            y=.56-i*.43;text(a,.04,y+.32,title,14)
            for j in range(streams):box(a,.04+j*.10,y+.11,.075,.09,str(j+1),'blue',11)
            box(a,.55,y+.09,.39,.14,'子层输入 4096 维','orange',11)
            arrow(a,(.44 if streams==4 else .13,y+.155),(.55,y+.155))
            text(a,.05,y-.04,'一条原输入与子层输出相加' if streams==1 else '四路先汇合供子层使用，随后混合子层输出',11)
        save(f,'8-residual')

        arch=data['teaching_diagrams']['architecture']
        for key,label,name in [('layers','主干层数','architecture'),('hidden','主干隐藏维度','architecture-width'),('experts','每个 MoE 层的路由专家数','architecture-experts')]:bars(name,['Qwen3-8B','Qwen3.6','DeepSeek\nV4-Flash','Kimi K3'],arch[key],label)
        models=data['teaching_diagrams']['resource_comparison']['models']
        for key,div,label,name in [('uniform_bf16_bytes',1e9,'完整 BF16 权重（GB）','resources'),('decode_matrix_flops',1e9,'8K 上下文单步矩阵运算（GFLOPs）','resources-compute'),('state_8192_bytes',2**20,'8K 上下文状态（MiB）','resources-state')]:bars(name,['Qwen3-8B','Qwen3.6','DeepSeek\nV4-Flash','Kimi K3\n紧凑'],[m[key]/div for m in models],label)

        # Pair lengths within each model; logarithmic axis keeps all four readable.
        import json
        long_data=json.loads((here/'long-context-comparison.json').read_text())
        f,a=plot(5.3,left=.30,bottom=.17)
        f.subplots_adjust(top=.84)
        labels=['Qwen3-8B*','Qwen3.6','DeepSeek\nV4-Flash','Kimi K3\n紧凑']
        for j,(offset,color,label) in enumerate([(-.18,COL['blue'],'8K 上下文'),(.18,COL['orange'],'200K 上下文')]):
            vals=[r['matrix_flops']/1e9 for r in long_data['models'][j*4:(j+1)*4]]
            yy=np.arange(4)+offset
            a.barh(yy,np.array(vals)-1,left=1,height=.30,color=color,edgecolor=COL['line'],label=label)
            for y,value in zip(yy,vals):a.text(value*1.08,y,f'{value:,.2f}',va='center',fontsize=11)
        a.set(yticks=range(4),yticklabels=labels,xscale='log',xlim=(1,4000),
              xlabel='单步矩阵运算（GFLOPs，对数轴）',ylim=(3.65,-.65))
        a.set_xticks([1,10,100,1000],['1','10','100','1000'])
        a.minorticks_off()
        a.legend(loc='upper left',bbox_to_anchor=(0,1.16),ncol=2,frameon=False)
        a.grid(axis='x',alpha=.15)
        save(f,'long-context-compute')

        rows=data['figure_2_9']['capacity_rows'];f,a=plot(3.8,left=.26,bottom=.25);left=np.zeros(3)
        for key,label,col in [('weight_bytes','权重','blue'),('workspace_bytes','预留','orange'),('kv_bytes_per_request','一条 KV','green')]:
            vals=np.array([r[key]/1e9 for r in rows]);a.barh(range(3),vals,left=left,height=.5,label=label,color=COL[col],edgecolor=COL['line']);left+=vals
        for i,r in enumerate(rows):a.plot([r['capacity_bytes']/1e9]*2,[i-.35,i+.35],color=COL['ink'],lw=1.2)
        a.set(yticks=range(3),yticklabels=['Qwen BF16','70B 8-bit','70B 4-bit'],xlim=(0,85),xlabel='容量（GB）');a.invert_yaxis();a.legend(loc='upper center',bbox_to_anchor=(.5,-.22),ncol=3,frameon=False);save(f,'9-capacity')
        d=data['figure_2_9']['history_capacity'];bars('history-capacity',['8K 上下文','32K 上下文'],d['maximum_requests'],'容量允许的独立请求数')

        f,a=canvas(4.8);text(a,.04,.94,'输入 128 个位置，返回 4 个 token',14)
        for i in range(4):
            y=.72-i*.21
            box(a,.03,y,.24,.14,'输入 128 个' if i==0 else f'输入 y{i}','blue',11)
            box(a,.36,y,.27,.14,'prefill' if i==0 else f'decode {i}','orange')
            box(a,.72,y,.25,.14,f'输出 y{i+1}','green')
            arrow(a,(.27,y+.07),(.36,y+.07));arrow(a,(.63,y+.07),(.72,y+.07))
            text(a,.49,y-.045,f'已保留 {128+i} 个位置',11,ha='center')
        save(f,'10-request')
        bars('request-compute',['Qwen3-8B','DeepSeek\nV4-Flash','DeepSeek\nV4-Pro','Kimi K3\n展开'],data['figure_2_10']['matrix_tflops'],'完整请求矩阵运算（TFLOPs）')
    from core_principles_figures import draw as draw_principles
    draw_principles(2, out)
    from v41_case_figures import draw as draw_v41
    draw_v41(2, out)
    return out.finish()
