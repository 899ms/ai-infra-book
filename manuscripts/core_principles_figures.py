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
            text(a,.25,.94,'传统应用',14,ha='center');text(a,.75,.94,'模型驱动的应用',14,ha='center')
            for x,labels in [(.03,[('代码与数据','orange'),('编译器与操作系统','purple'),('程序指令的执行','green'),('处理器、内存与互联','blue')]),(.54,[('Agent','orange'),('模型接口','purple'),('计算输出、保存上下文状态','green'),('加速器、内存与互联','blue')])]:
                for i,(label,c) in enumerate(labels):
                    y=.73-i*.18;box(a,x,y,.43,.12,label,c)
                    if i<3:arrow(a,(x+.215,y),(x+.215,y-.06))
            arrow(a,(.54,.79),(.46,.61),kind='control')
            text(a,.5,.065,'工具程序仍由操作系统执行',12,ha='center')
            out.save(f,'figure-1-programmability')
        if chapter == 2:
            f,a=plot(3.8,left=.08,bottom=.22)
            vals=[4*K/1e9,WORKSPACE/1e9,(CAPACITY-4*K-WORKSPACE)/1e9]
            left=0
            for v,c in zip(vals,['green','gray','blue']):
                a.barh(.5,v,left=left,height=.24,color=COL[c],edgecolor=COL['line']);left+=v
            a.set(xlim=(0,24),ylim=(0,1.45),yticks=[],xticks=[0,4,8,12,16,20,24],xlabel='24 GB 可用容量的分配（GB）')
            for x,y,label,target in [(2.4,1.20,'4 条请求 KV\n4.83 GB',2.4),(7,.95,'工作区\n2.15 GB',5.9),(16,1.20,'权重余量\n17.02 GB',15.5)]:
                a.annotate(label,xy=(target,.64),xytext=(x,y),ha='center',va='center',fontsize=12,arrowprops=dict(arrowstyle='-',color=COL['line']))
            a.text(12,.14,'BF16 参数上界 ≈ 85.1 亿',ha='center',fontsize=13)
            out.save(f,'figure-2-reverse-budget')
        if chapter == 4:
            f,a=canvas(4.8)
            rows=[('已有设备','容量、带宽、互联','blue'),('模型与软件选择','压缩、分块、并行','green'),('持续的执行瓶颈','形成下一代硬件需求','orange'),('新设备与新候选','重新比较模型结构','purple')]
            for i,(title,desc,c) in enumerate(rows):
                y=.76-i*.22
                box(a,.06,y,.88,.16,title+'\n'+desc,c)
                if i<3:arrow(a,(.50,y),(.50,y-.06))
            out.save(f,'figure-4-codesign-loop')
            f,a=canvas(4.5)
            text(a,.04,.94,'权重与状态共用接口',14)
            box(a,.04,.66,.39,.18,'HBM\n权重 + KV','blue');box(a,.66,.66,.30,.18,'计算','orange')
            arrow(a,(.43,.75),(.66,.75));text(a,.54,.59,'W + BK',12,ha='center')
            text(a,.04,.46,'独立的只读权重通路',14)
            box(a,.04,.25,.39,.13,'ROM：权重 W','blue');box(a,.04,.04,.39,.13,'HBM：KV 状态 BK','green')
            box(a,.66,.13,.30,.20,'计算','orange')
            arrow(a,(.43,.315),(.66,.27));arrow(a,(.43,.105),(.66,.19))
            out.save(f,'figure-4-rom-paths')
        if chapter == 8:
            f,a=plot(3.8,left=.16,bottom=.19)
            b=np.arange(1,33)
            a.plot(b,(W/b+K)/1e9,color='#527fa0',lw=2,label='传统 HBM：W/B + K')
            a.plot(b,np.full_like(b,K,dtype=float)/1e9,color='#48826b',lw=2,label='独立 ROM：K')
            for batch in [1,16]:
                v=(W/batch+K)/1e9;a.scatter([batch],[v],color='#527fa0',s=22)
                a.annotate(f'{v:.2f} GB',(batch,v),xytext=(8,2),textcoords='offset points',fontsize=11)
            a.set(xlim=(0,33),ylim=(0,20),xticks=[1,8,16,24,32],xlabel='批次大小 B',ylabel='每输出 token 的 HBM 读取（GB）')
            a.legend(frameon=False,loc='upper right');out.save(f,'figure-8-batch-counterfactual')
            f,a=canvas(4.2)
            rows=[(.72,'追加',[(8,'8K 复用','blue'),(1,'','orange')]),(.43,'改写开头',[(9,'9K 重新处理','orange')]),(.14,'总结历史',[(2,'2K','orange'),(1,'1K','orange')])]
            for y,label,segments in rows:
                text(a,.03,y+.06,label,12)
                x=.26
                for length,lab,col in segments:
                    width=length*.073
                    box(a,x,y,width,.13,lab,col);x+=width
                if label=='追加':text(a,x-.0365,y-.065,'1K 新增',11,ha='center')
                if label=='总结历史':text(a,.61,y+.065,'另计总结工作',11)
            text(a,.5,.96,'相同历史，三种更新方式',14,ha='center')
            out.save(f,'figure-8-context-edits')
        if chapter == 10:
            f,a=canvas(4.2)
            text(a,.04,.94,'固定版本服务',14)
            box(a,.04,.67,.38,.17,'ROM\n权重 v0','blue');box(a,.64,.67,.32,.17,'生成\n可写 KV','green');arrow(a,(.42,.755),(.64,.755))
            text(a,.04,.48,'持续更新的策略',14)
            box(a,.04,.19,.25,.18,'训练\n更新参数','orange');box(a,.39,.19,.25,.18,'可写权重\nv0 → v1','blue');box(a,.74,.19,.23,.18,'生成\n使用 v1','green')
            arrow(a,(.29,.28),(.39,.28));arrow(a,(.64,.28),(.74,.28))
            text(a,.5,.065,'更新后发布权重，保持版本一致',12,ha='center');out.save(f,'figure-10-weight-update')
        if chapter == 11:
            f,a=plot(4.4,left=.24,bottom=.17)
            for y,v,c in [(4,10,'blue'),(3,6,'green'),(1,1,'blue'),(0,6,'green')]:a.barh(y,v,height=.55,color=COL[c],edgecolor=COL['line']);a.text(v+.13,y,f'{v} 秒',va='center',fontsize=11)
            a.axhline(2.2,color=COL['line'],lw=.7)
            a.annotate('',xy=(6,1.5),xytext=(1,1.5),arrowprops=dict(arrowstyle='<->',color=COL['line']));a.text(3.5,1.77,'额外等待 5 秒',ha='center',fontsize=11)
            a.set(yticks=[4,3,1,0],yticklabels=['原模型','环境创建','加速模型','环境创建'],xlim=(0,12),ylim=(-.65,4.7),xlabel='从模型开始计时（秒）')
            out.save(f,'figure-11-environment-overlap')
        if chapter == 12:
            f,a=plot(3.5,left=.24,bottom=.21)
            for y,v in [(2,8),(1,.8),(0,0)]:
                a.barh(y,v,height=.55,color=COL['blue'],edgecolor=COL['line'],label='模型' if y==2 else None)
                a.barh(y,2,left=v,height=.55,color=COL['orange'],edgecolor=COL['line'],label='其他串行阶段' if y==2 else None)
                a.text(v+2+.12,y,f'{v+2:g} 秒',va='center',fontsize=12)
            a.set(yticks=[2,1,0],yticklabels=['原任务','模型快 10 倍','理想下界'],xlim=(0,12),ylim=(-.7,3),xlabel='完整任务时间（秒）');a.legend(frameon=False,loc='upper right')
            out.save(f,'figure-12-task-counterfactual')
