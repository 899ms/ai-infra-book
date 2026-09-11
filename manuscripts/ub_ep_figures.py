"""UB layer separation and EP skew, using the book's common figure style."""
from pathlib import Path
import json
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from figure_style import COL, STYLE, Exporter, canvas, plot, box, text, arrow
from figure_style.typography import configure_font

ROOT=Path(__file__).resolve().parents[1]


def draw(ch, here):
    out=Exporter(here)
    with plt.rc_context(STYLE):
        if ch == 6:
            f,a=canvas(4.3)
            text(a,.04,.95,'应用端点分别保留，可靠传输按需共享',13)
            for x,label in ((.06,'应用 A\nJetty A'),(.59,'应用 B\nJetty B')):
                box(a,x,.69,.35,.18,label,'blue')
                arrow(a,(x+.175,.69),(.5,.56))
            box(a,.17,.37,.66,.19,'共享 TP 通道\n序号、确认、重传、拥塞控制','orange')
            arrow(a,(.5,.37),(.5,.24))
            box(a,.17,.06,.66,.18,'远端事务层\n按目标端点分派与检查权限','green')
            text(a,.50,.63,'事务 → 报文',11,ha='center')
            text(a,.73,.30,'网络交付',11,ha='center')
            out.save(f,'figure-6-ub-layers')
            fab=json.loads((ROOT/'calculations/results/ub-fabric-book.json').read_text())
            LINE={'blue':'#267398','orange':'#a56c28','green':'#28856a','purple':'#7a5c99'}
            # Controller placement: behind PCIe versus on the on-chip bus.
            f,a=canvas(4.0)
            text(a,.04,.95,'一次远程读取的发起路径',13)
            for x0,title,chain in ((.02,'PCIe 外设网卡',[('处理器','blue'),('片上\n总线','green'),('PCIe','gray'),('网卡','orange')]),
                                   (.52,'片上总线上的控制器',[('处理器','blue'),('片上\n总线','green'),('UB\n控制器','orange')])):
                text(a,x0+.23,.84,title,12,ha='center')
                n=len(chain);gap=.025;w=(.46-(n-1)*gap)/n
                for i,(label,c) in enumerate(chain):
                    x=x0+i*(w+gap)
                    box(a,x,.47,w,.26,label,c,11)
                    if i<n-1:arrow(a,(x+w,.60),(x+w+gap,.60))
                arrow(a,(x0+.23,.47),(x0+.23,.33))
                text(a,x0+.23,.27,'网络',11,ha='center')
            text(a,.25,.11,'门铃与 DMA 各穿越 PCIe 一次',11,ha='center')
            text(a,.75,.11,'指令经片上总线直达控制器',11,ha='center')
            out.save(f,'figure-6-ub-controller')
            # Per-NIC state against hosts in one fabric, three organisations.
            hosts=[r['hosts'] for r in fab['hosts']]
            f,a=plot(3.8,left=.19)
            f.subplots_adjust(top=.80)
            for key,label,c in (('roce_bytes','逐对连接（RoCE）','orange'),('directory_bytes','目录式一致互联','purple'),('ub_bytes','端点加通道（UB）','green')):
                a.plot(hosts,[r[key]/1024 for r in fab['hosts']],marker='o',color=LINE[c],label=label)
            a.axhline(fab['cache']['context_cache_bytes']/1024,color=COL['line'],ls='--')
            a.text(hosts[0],fab['cache']['context_cache_bytes']/1024*1.4,'片上上下文缓存 256 KiB',fontsize=11)
            a.set(xscale='log',yscale='log',xlabel='互联内的主机数（每台 8 个端点）',ylabel='每个 NIC 的状态（KiB）')
            a.set_xticks(hosts);a.set_xticklabels([str(h) for h in hosts])
            a.legend(frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.45,1.27),columnspacing=.8,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-6-ub-hosts')
            # Connection setup time, N local × N remote endpoints, 32 cores in parallel.
            f,a=plot(3.7,left=.19)
            f.subplots_adjust(top=.82)
            ns=[r['endpoints'] for r in fab['setup']]
            for key,label,c in (('roce_parallel_s','每对关系一条连接（RoCE）','orange'),('ub_parallel_s','每端点一个 Jetty、每远端一条通道（UB）','green')):
                a.plot(ns,[max(r[key],1e-9) for r in fab['setup']],marker='o',color=LINE[c],label=label)
            top=fab['setup'][-1]
            a.annotate(f"{top['roce_parallel_s']:.1f} s",(ns[-1],top['roce_parallel_s']),xytext=(-52,-4),textcoords='offset points',fontsize=11)
            a.annotate(f"{top['ub_parallel_s']*1000:.0f} ms",(ns[-1],top['ub_parallel_s']),xytext=(-46,-14),textcoords='offset points',fontsize=11)
            a.set(xscale='log',yscale='log',xlabel='本地端点数 N（远端端点数 M = N）',ylabel='建立全部关系的时间（s）')
            a.set_xticks(ns);a.set_xticklabels([str(n) for n in ns])
            a.legend(frameon=False,ncol=1,loc='upper center',bbox_to_anchor=(.45,1.3),handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-6-ub-setup')
        if ch == 6:
            # Who issues a network request: CPU proxy, GPU SMs, or the NIC's own processor.
            f, a = canvas(4.0)
            for i, (title, ctrl, note) in enumerate([('CPU 代理线程', 0, '穿越 PCIe：3 次'), ('GPU 的 SM', 1, '穿越 PCIe：2 次'), ('网卡上的处理器', 2, '穿越 PCIe：0 次')]):
                x0 = .02 + .33 * i
                text(a, x0 + .15, .95, title, 12, ha='center')
                box(a, x0 + .01, .70, .12, .12, 'CPU', 'orange' if ctrl == 0 else 'gray', 11)
                box(a, x0 + .17, .70, .12, .12, 'GPU', 'orange' if ctrl == 1 else 'blue', 11)
                a.plot([x0, x0 + .30], [.52, .52], color=COL['line'], lw=.9, ls=(0, (3, 3)))
                text(a, x0 + .30, .56, 'PCIe', 11, ha='right')
                box(a, x0 + .09, .20, .12, .12, '网卡', 'orange' if ctrl == 2 else 'green', 11)
                if ctrl == 0:
                    arrow(a, (x0 + .17, .76), (x0 + .13, .76)); text(a, x0 + .15, .86, '就绪', 11, ha='center')
                    arrow(a, (x0 + .06, .70), (x0 + .12, .32)); text(a, x0 + .01, .45, '门铃、请求项', 11)
                elif ctrl == 1:
                    arrow(a, (x0 + .19, .70), (x0 + .13, .32)); text(a, x0 + .01, .45, '门铃、请求项', 11)
                else:
                    arrow(a, (x0 + .06, .70), (x0 + .12, .32)); text(a, x0 + .01, .45, '每批一次触发', 11)
                arrow(a, (x0 + .18, .32), (x0 + .24, .70)); text(a, x0 + .21, .40, '载荷、完成', 11)
                text(a, x0 + .15, .08, note, 11, ha='center')
            out.save(f, 'figure-6-initiator')
        if ch == 7:
            # PCIe transaction types: posted writes finish on send; reads wait for tagged completions.
            f, a = canvas(3.2)
            text(a, .02, .90, '写（posted）：发出即完成', 12)
            box(a, .10, .58, .16, .16, '发起方', 'blue', 11); box(a, .74, .58, .16, .16, '接收方', 'green', 11)
            arrow(a, (.26, .66), (.74, .66)); text(a, .50, .74, '写事务报文：地址＋数据', 11, ha='center')
            text(a, .02, .44, '读（non-posted）：在途数受标签与信用限制', 12)
            box(a, .10, .10, .16, .16, '发起方', 'blue', 11); box(a, .74, .10, .16, .16, '接收方', 'green', 11)
            arrow(a, (.26, .22), (.74, .22)); text(a, .50, .31, '读请求报文：地址＋标签', 11, ha='center')
            arrow(a, (.74, .14), (.26, .14)); text(a, .50, .04, '完成报文：数据＋同一标签', 11, ha='center')
            out.save(f, 'figure-7-pcie-transactions')
            # Which ceiling binds a 64 B random DMA read on the KV-Direct platform.
            f, a = plot(2.8, left=.34, bottom=.26)
            labels = ['链路带宽换算', '报文头开销上限', '在途标签上限', '实测']
            vals = [123, 87, 61, 60]; cols = [COL['blue'], COL['blue'], COL['orange'], COL['green']]
            a.barh(range(4), vals, color=cols, edgecolor=COL['line'], height=.55)
            for i, v in enumerate(vals): a.text(v + 2, i, f'{v}', va='center', fontsize=11)
            a.set(yticks=range(4), yticklabels=labels, xlim=(0, 140), xlabel='64 B 随机 DMA 读，每秒百万次操作'); a.invert_yaxis()
            out.save(f, 'figure-7-pcie-limits')
            # Two traffic classes sharing a GPU's PCIe link, per direction.
            f, a = canvas(3.8)
            box(a, .03, .62, .18, .14, '主机内存', 'gray', 11); box(a, .03, .24, .18, .14, '网卡', 'gray', 11)
            a.plot([.56, .56], [.10, .92], color=COL['line'], lw=.9, ls=(0, (3, 3))); text(a, .56, .96, 'PCIe 链路', 11, ha='center')
            box(a, .62, .14, .34, .70, '', 'blue'); text(a, .79, .78, 'GPU', 12, ha='center')
            box(a, .68, .40, .22, .14, 'HBM', 'white', 11)
            arrow(a, (.21, .72), (.62, .72)); text(a, .41, .79, '完成报文（H2D 复制）', 11, ha='center')
            arrow(a, (.62, .62), (.21, .62)); text(a, .41, .55, 'posted 写（D2H 复制）', 11, ha='center')
            arrow(a, (.21, .34), (.62, .34)); text(a, .41, .41, 'posted 写（远端写入）', 11, ha='center')
            arrow(a, (.62, .24), (.21, .24)); text(a, .41, .17, '完成报文（远端读取）', 11, ha='center')
            text(a, .79, .30, '离开 GPU 的两路\n都先从 HBM 取数', 11, ha='center')
            text(a, .79, .64, '进入 GPU 的两路\n在链路上争用', 11, ha='center')
            out.save(f, 'figure-7-pcie-asymmetry')
            f,a=canvas(4.6)
            text(a,.04,.96,'64 卡超节点：8 个 TP8 组',13)
            for row in range(8):
                y=.79-row*.075
                text(a,.02,y+.023,str(row),11)
                for col in range(8):box(a,.10+col*.103,y,.079,.047,'','orange' if col==0 else 'blue')
            text(a,.51,.88,'同一行：TP 分片，共同计算一份输入',11,ha='center')
            text(a,.5,.12,'同一列：对应梯度先在本地归约',12,ha='center')
            arrow(a,(.5,.09),(.5,.02))
            text(a,.73,.04,'再跨节点交换',11,ha='center')
            out.save(f,'figure-7-supernode-groups')
            records=json.loads((ROOT/'calculations/results/supernode-scaling-book.json').read_text())['results']
            f,a=plot(3.7,left=.19)
            labels=['出口扩展','出口封顶','出口扩展＋本地加倍']
            colors=['#267398','#a56c28','#28856a']
            for i in range(3):
                rs=records[i*4:(i+1)*4]
                a.plot(range(4),[r['tokens_per_s']/1e4 for r in rs],marker='o',color=colors[i],label=labels[i])
            a.set(xticks=range(4),xticklabels=['8','64','128','256'],xlabel='每超节点卡数',ylabel='吞吐（万 token/s）',ylim=(32,57))
            a.legend(frameon=False,fontsize=11,loc='upper left')
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-supernode-scaling')
            fab=json.loads((ROOT/'calculations/results/ub-fabric-book.json').read_text())
            LINE={'blue':'#267398','orange':'#a56c28','green':'#28856a','purple':'#7a5c99'}
            # Endpoint state, N = M sweep.
            f,a=plot(3.7,left=.19)
            f.subplots_adjust(top=.82)
            ns=[r['endpoints'] for r in fab['state']]
            a.plot(ns,[r['roce_bytes']/1024 for r in fab['state']],marker='o',color=LINE['orange'],label='N×M 份连接状态（RoCE）')
            a.plot(ns,[r['ub_bytes']/1024 for r in fab['state']],marker='o',color=LINE['green'],label='N 个 Jetty 加 M 条通道（UB）')
            a.axhline(fab['cache']['context_cache_bytes']/1024,color=COL['line'],ls='--')
            a.text(ns[0],fab['cache']['context_cache_bytes']/1024*1.5,'片上缓存 256 KiB',fontsize=11)
            top=fab['state'][-1]
            a.annotate(f"{top['ratio']:,.0f} 倍",(ns[-1],top['ub_bytes']/1024),xytext=(-40,12),textcoords='offset points',fontsize=11)
            a.set(xscale='log',yscale='log',xlabel='本地端点数 N（远端端点数 M = N）',ylabel='每个 NIC 的状态（KiB）')
            a.set_xticks(ns);a.set_xticklabels([str(n) for n in ns])
            a.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.45,1.25),columnspacing=1,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-ub-state-growth')
            # Latency against active endpoints: the cache cliff.
            f,a=plot(3.6,left=.17)
            f.subplots_adjust(top=.82)
            sw=fab['cache']['sweep'];xs=[r['endpoints'] for r in sw]
            a.step(xs,[r['roce_dma_ns']/1000 for r in sw],where='post',color=LINE['orange'],label='RoCE 读取')
            a.step(xs,[r['ub_loadstore_ns']/1000 for r in sw],where='post',color=LINE['green'],label='UB Load')
            a.annotate(f"N = {fab['cache']['roce_spill_endpoints']} 溢出，每次多 {fab['cache']['roce_refetch_ns']} ns",(fab['cache']['roce_spill_endpoints'],sw[-1]['roce_dma_ns']/1000),xytext=(6,6),textcoords='offset points',fontsize=11)
            a.annotate(f"N = {fab['cache']['ub_spill_endpoints']} 溢出，多 {fab['cache']['ub_refetch_ns']} ns",(fab['cache']['ub_spill_endpoints'],sw[-1]['ub_loadstore_ns']/1000),xytext=(-4,8),textcoords='offset points',fontsize=11,ha='right')
            a.set(xscale='log',xlabel='活跃端点数 N（M = N）',ylabel='一次 64 B 读取（μs）',ylim=(0,3.9))
            a.set_xticks([1,8,64,512,4096]);a.set_xticklabels(['1','8','64','512','4096'])
            a.legend(frameon=False,ncol=2,loc='upper center',bbox_to_anchor=(.45,1.22),columnspacing=1.5,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-ub-cache-cliff')
            # Round trip budget by phase group, three stacks.
            f,a=plot(3.9,left=.24,bottom=.18)
            f.subplots_adjust(top=.80)
            stacks=[('roce_dma','外设式 RoCE 读取'),('ub_urma','UB 异步读取'),('ub_loadstore','UB Load')]
            groups=fab['groups'];fills=['blue','gray','green','orange','purple','white']
            from matplotlib.patches import Patch
            for row,(key,label) in enumerate(stacks):
                start=0
                for g,c in zip(groups,fills):
                    v=fab['round_trip'][key]['group_ns'][g]
                    if v:a.barh(row,v,left=start,height=.55,color=COL[c],edgecolor=COL['line']);start+=v
                a.text(start+40,row,f"推导 {fab['round_trip'][key]['total_ns']:.0f}，仿真 {fab['round_trip'][key]['paper_measured_ns']}",va='center',fontsize=11)
            a.set(yticks=range(3),yticklabels=[l for _,l in stacks],xlabel='一次 64 B 远程读取的关键路径（ns）',xlim=(0,3300))
            a.invert_yaxis()
            a.legend(handles=[Patch(facecolor=COL[c],edgecolor=COL['line'],label=g) for g,c in zip(groups,fills)],frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.4,1.3),columnspacing=.8,handlelength=1.2)
            out.save(f,'figure-7-ub-round-trip')
            # Total against one-way link delay: same slope, different intercepts.
            f,a=plot(3.6,left=.17)
            f.subplots_adjust(top=.82)
            for key,label,c in (('roce_dma','外设式 RoCE 读取','orange'),('ub_urma','UB 异步读取','blue'),('ub_loadstore','UB Load','green')):
                pts=fab['round_trip'][key]['link_sweep']
                a.plot([p['link_ns'] for p in pts],[p['total_ns']/1000 for p in pts],marker='o',color=LINE[c],label=label)
            a.set(xlabel='线路单程时延（ns）',ylabel='一次 64 B 读取（μs）',xlim=(0,540),ylim=(0,3.4))
            a.legend(frameon=False,ncol=3,loc='upper center',bbox_to_anchor=(.45,1.22),columnspacing=1.2,handlelength=1.4)
            a.grid(axis='y',alpha=.15)
            out.save(f,'figure-7-ub-link-delay')
        if ch == 9:
            data=json.loads((ROOT/'calculations/results/ep-skew-book.json').read_text())['results']
            f,a=plot(3.7,left=.16)
            for i,(r,label,col) in enumerate(zip(data[:2],['均衡','热点'],['blue','orange'])):
                v=np.array(r['expert_assignments'])*8192/2**20
                a.bar(np.arange(4)+(i-.5)*.32,v,width=.30,label=label,color=COL[col],edgecolor=COL['line'])
                for j,y in enumerate(v):a.text(j+(i-.5)*.32,y+.8,f'{y:g}',ha='center',fontsize=11)
            a.set(xticks=range(4),xticklabels=['组 0','组 1','组 2','组 3'],ylim=(0,49),ylabel='每组每方向载荷（MiB）')
            a.legend(frameon=False,ncol=2,loc='upper right')
            out.save(f,'figure-9-ep-skew')
            f,a=plot(3.3,left=.21,bottom=.23)
            f.subplots_adjust(top=.81)
            for row,times in enumerate(((.1,.3,.1),(.2,.8,.4))):
                start=0
                for duration,c in zip(times,('blue','green','orange')):
                    a.barh(row,duration,left=start,height=.42,color=COL[c],edgecolor=COL['line']);start+=duration
                if start<1.4:a.barh(row,1.4-start,left=start,height=.42,color=COL['gray'],edgecolor=COL['line'])
                a.text(start,row-.34,f'{start:.1f} ms',ha='center',fontsize=11)
            from matplotlib.patches import Patch
            handles=[Patch(facecolor=COL[c],edgecolor=COL['line'],label=label) for c,label in [('blue','分派'),('green','计算'),('orange','返回'),('gray','等待')]]
            a.axvline(1.4,color=COL['line'],ls='--');a.set(yticks=[0,1],yticklabels=['快专家','慢专家'],xlabel='从该层分派开始计时（ms）',xlim=(0,1.52),ylim=(1.6,-.65))
            a.legend(handles=handles,frameon=False,ncol=4,loc='upper center',bbox_to_anchor=(.48,1.28),columnspacing=.65,handlelength=1)
            out.save(f,'figure-9-ep-tail')
    (Path(here)/'ub-ep-layout-validation.json').write_text(json.dumps(out.checks,ensure_ascii=False,indent=2)+'\n')
    return out.outputs


if __name__=='__main__':
    _,family=configure_font()
    plt.rcParams.update({'font.family':[family,'DejaVu Sans'],'axes.unicode_minus':False,'svg.hashsalt':'ub-ep-book'})
    for ch in (6,7,9):draw(ch,ROOT/f'manuscripts/ch{ch:02}')
