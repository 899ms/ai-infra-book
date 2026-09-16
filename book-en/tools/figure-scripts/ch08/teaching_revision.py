"""Request iterations, physical KV blocks and service outcomes."""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from figure_style import COL,STYLE,canvas,plot,text,box,arrow,Exporter

def draw(here,data):
    out=Exporter(here)
    def save(f,n):out.save(f,'figure-8-'+n)
    with plt.rc_context(STYLE):
        f,a=canvas(4.7);text(a,.04,.94,"request keeps identity, batch reformed each round",14)
        for row,labels in enumerate([["Request A","Request B"],["Request A","Request C"]]):
            y=.60-row*.36;text(a,.04,y+.17,f'Iteration {row}',12)
            for i,label in enumerate(labels):box(a,.25+i*.37,y,.30,.20,label,'blue' if label=='请求 A' else 'green',12)
        text(a,.5,.08,"B finished → freed slot given to C",12,ha='center');save(f,'request-iterations')
        f,a=plot(3.0,left=.12);start=0;life=data['lifecycle']
        for dur,l,c in [(life['queue_s'],"Queueing",'gray'),(life['prefill_s'],'prefill','blue'),(life['output_intervals']*life['interval_s'],'decode','green')]:a.barh(0,dur,left=start,height=.35,color=COL[c],edgecolor=COL['line'],label=l);start+=dur
        a.scatter([life['queue_s']+life['prefill_s'],life['completion_s']],[0,0],color='#252525',zorder=5);a.axvline(life['deadline_s'],ls='--',color='#a56c28');a.set(yticks=[],xlim=(0,7.4),xlabel="Time since arrival (s)");f.subplots_adjust(top=.78);a.legend(ncol=3,frameon=False,loc='upper center',bbox_to_anchor=(.5,1.28),columnspacing=1.5,handlelength=1.4);save(f,'1-lifecycle')
        f,a=plot(3.7);b=np.array(data['batch']['batch']);w=data['batch']['shared_weight_bytes']/2**30/b
        for L,c in [(2048,'#267398'),(8192,'#388768')]:a.plot(b,w+L*144/2**20,color=c,label=f'Context {L} tokens: total read volume');a.axhline(L*144/2**20,color=c,ls=':')
        a.plot(b,w,ls='--',color='#777777',label="Weight reads per output token");a.set(xscale='log',yscale='log',xlabel="Requests per batch",ylabel="Read volume per generated token (GiB)");a.legend(frameon=False,fontsize=11);save(f,'2-batch')
        for i,key in enumerate(['fixed','continuous','chunked']):
            f,a=plot(3.8,left=.16)
            for step in data[key]:
                for plan in step['plans']:
                    lane=int(plan['request'][1:]);a.barh(lane,step['duration_ns']/1e6,left=step['start_ns']/1e6,height=.55,color=COL['blue' if plan['phase']=='prefill' else 'green'],edgecolor=COL['line'],linewidth=.45)
            a.scatter([0,0,20,30],range(4),marker='^',color='#252525',s=18,zorder=5);a.set(yticks=range(4),yticklabels=[f'request r{j}' for j in range(4)],xlim=(0,900),xlabel="time (ms)");a.invert_yaxis();save(f,'3-scheduling' if i==0 else f'scheduling-{key}')
        for i,d in enumerate(data['attention_geometry']):
            f,a=canvas(3.5);h=d['history'];step=.065;start=.15
            for row in range(4):
                for col in range(h+4):box(a,start+col*step,.65-row*.13,step-.008,.105,'','blue' if col<h else ('green' if col-h<=row else 'white'))
            text(a,.04,.91,f'Old context {h} token + 4 new input tokens',14);text(a,.5,.12,f'Old context pairing {4*h} + intra-block pairing 10 = {4*h+10}',12,ha='center');save(f,'4-attention' if i==0 else 'attention-history')
        f,a=canvas(4.5);text(a,.04,.94,"logical blocks in order, physical blocks scattered",14)
        for i,target in enumerate([2,0,3]):
            x=.06+i*.31;box(a,x,.68,.24,.13,f'Logical block {i}','blue',11);text(a,x+.12,.54,f'Block table: {i} → {target}',11,ha='center');arrow(a,(x+.12,.46),(.14+target*.235,.31))
        for i in range(4):box(a,.04+i*.235,.12,.20,.18,f'Physical block {i}','green' if i in [0,2,3] else 'gray',11)
        save(f,'page-map')
        for mode,name in [('reserved','5-pages'),('paged','pages-paged')]:
            f,a=canvas(4.6)
            for row,L in enumerate(data['pages']['lengths']):
                y=.70-row*.18;text(a,.03,y+.04,f'{"ABCD"[row]}：{L}',11)
                slots=16 if mode=='reserved' else (L+3)//4*4
                for j in range(slots):box(a,.19+j*.047,y,.039,.10,'','blue' if j<L else 'gray')
            text(a,.5,.05,f'KV allocation capacity: {64 if mode=="reserved" else 52} token',13,ha='center');save(f,name)
        f,a=canvas(4.4);box(a,.04,.67,.27,.15,"A's block table",'blue');box(a,.69,.67,.27,.15,"B's block table",'green');box(a,.31,.34,.38,.16,"two shared prefix blocks\neach with two references",'purple',11)
        arrow(a,(.175,.67),(.40,.50));arrow(a,(.825,.67),(.60,.50));box(a,.03,.07,.28,.13,"A private suffix",'blue',11);box(a,.69,.07,.28,.13,"B private suffix",'green',11);arrow(a,(.175,.67),(.175,.20));arrow(a,(.825,.67),(.825,.20));save(f,'pages-shared')
        f,a=canvas(4.3);box(a,.25,.70,.50,.16,"shared tail block: [a, b, c, empty]",'purple',12)
        for x,label,c in [(.03,"Branch A: [a, b, c, x]",'blue'),(.54,"Branch B: [a, b, c, y]",'green')]:box(a,x,.20,.43,.19,label,c,11);arrow(a,(.5,.70),(x+.215,.39))
        text(a,.5,.52,"before write divergence, obtain own tail block copy",12,ha='center');save(f,'copy-on-write')
        f,a=canvas(4.3)
        for row,(label,count,col) in enumerate([("A, B share common blocks",2,'purple'),("A ends, B continues using",1,'green'),("B ends, accelerator no longer accesses",0,'gray')]):
            y=.69-row*.27;box(a,.04,y,.61,.17,label,col,11);box(a,.75,y,.21,.17,f'Reference {count}',col,11)
            if row<2:arrow(a,(.86,y),(.86,y-.10))
        save(f,'reference-release')
        f,a=canvas(4.2)
        for x,l,c in [(.03,"Receive cancel\nStop subsequent iterations",'orange'),(.37,"Wait for submitted\naccelerator ops to complete",'blue'),(.71,"Release private blocks\nUpdate shared references",'green')]:box(a,x,.41,.26,.27,l,c,11)
        arrow(a,(.29,.54),(.37,.54));arrow(a,(.63,.54),(.71,.54));text(a,.5,.18,"Cancel call returns in 1.6 ms; block release ~31 ms",11,ha='center');save(f,'cancel-lifetime')
        # Exact common-prefix lengths; tree topology is drawn by logical depth.
        d=data['prefix'];f,a=canvas(4.5);positions={0:(.12,.50),1:(.38,.83),2:(.38,.40),3:(.63,.63),4:(.63,.24),5:(.86,.39),6:(.86,.10)}
        for u,v,n in d['edges']:
            arrow(a,positions[u],positions[v]);x=(positions[u][0]+positions[v][0])/2;y=(positions[u][1]+positions[v][1])/2;text(a,x,y+.065,f'+{n}',11,ha='center')
        for i,node in enumerate(d['tree']):
            x,y=positions[i];a.plot(x,y,'o',color='#267398',ms=5)
            if len(node['ids'])==1:text(a,x,y+.09,f'round {node["ids"][0]+1}',11,ha='center')
        text(a,.04,.95,"First four rounds: start from 206 shared tokens",14);text(a,.5,.03,"Edge labels: new token count",11,ha='center');save(f,'6-prefix')
        f,a=plot(3.8);v=np.array(d['adjacent_lcp']);a.bar(range(1,13),v,color=COL['blue'],label="shared prefix with previous round");a.bar(range(1,13),np.array(d['input_lengths'])-v,bottom=v,color=COL['orange'],label="remaining input");a.set(xlabel="Input round",ylabel="token count",xticks=[1,3,6,9,12]);a.legend(frameon=False);save(f,'prefix-lengths')
        f,a=canvas(3.8);text(a,.04,.94,"Text matches to 10752, state restored from 8192",13);a.plot([.05,.95],[.48,.48],color='#777777')
        for x,label,c in [(.10,"4096\nsnapshot",'blue'),(.48,"8192\nlatest snapshot",'green'),(.85,"10752\nmatch end",'orange')]:box(a,x-.07,.39,.17,.22,label,c,11)
        arrow(a,(.57,.49),(.77,.49));text(a,.68,.22,"Recompute 2560 tokens",12,ha='center');save(f,'prefix-restore')
        f,a=canvas(4.1)
        for row in range(2):
            y=.63-row*.40
            cc=data['cache_choice'];va=round(cc['A']['net_ms'],1);vb=round(cc['B']['each_net_ms'],1)
            if row==0:box(a,.04,y,.92,.19,f'A: 864 MiB, net savings {va} ms','blue')
            else:
                for i in range(3):box(a,.04+i*.31,y,.30,.19,f'B：288 MiB\n{vb} ms','green',11)
            text(a,.5,y-.09,f'Total savings {va if row==0 else round(3*vb,1)} ms',12,ha='center')
        save(f,'7-cache-choice')
        f,a=plot(3.5,left=.20)
        for i,(payload,scale) in enumerate(zip(data['kv_layout']['payload_bytes'],data['kv_layout']['scale_bytes'])):a.barh(i,payload,height=.5,color=COL['blue'],edgecolor=COL['line']);a.barh(i,scale,left=payload,height=.5,color=COL['orange'],edgecolor=COL['line'])
        a.set(yticks=range(3),yticklabels=['BF16','q8_0','q4_0'],xlim=(0,68),xlabel="Storage for same 32 values (bytes)");a.invert_yaxis();save(f,'8-kv-format')
        f,a=plot(3.6,left=.23)
        for i,buff in enumerate([288,576]):a.barh(i,buff,height=.48,color=COL['orange'],edgecolor=COL['line']);a.barh(i,2592-buff,left=buff,height=.48,color=COL['green'],edgecolor=COL['line'])
        a.set(yticks=[0,1],yticklabels=["One prefetch buffer set","Two prefetch buffer sets"],xlim=(0,2800),xlabel="Space freed by offload (MiB)");a.invert_yaxis();save(f,'9-offload')
        f,a=plot(3.5);v=data['offload']['copy_ms'];a.bar([0,1],v,color=[COL['blue'],COL['green']],edgecolor=COL['line']);a.set(xticks=[0,1],xticklabels=['PCIe Gen5 x16\n64 GB/s','NVLink-C2C\n450 GB/s'],ylabel="Per-round copy lower bound (ms)",ylim=(0,50));save(f,'offload-copy')
        for i,m in enumerate(data['kv']['correct_by_task']):
            f,a=plot(4.7,left=.25);a.imshow(m,cmap=ListedColormap([COL['orange'],COL['green']]),vmin=0,vmax=1,aspect='auto')
            for y,row in enumerate(m):
                for x,val in enumerate(row):a.text(x,y,'○' if val else '×',ha='center',va='center',fontsize=14)
            a.set(yticks=range(8),yticklabels=[f'task {j+1}' for j in range(len(data['kv']['task_ids']))],xticks=range(4),xticklabels=['1 / 1','1 / 2','4 / 1','4 / 2'],xlabel="concurrency / repeat index");save(f,'10-kv-quality' if i==0 else f'kv-quality-{i}')
        f,a=canvas(4.6)
        for row,(title,tokens) in enumerate([("draft",['a','b','c','d']),("Verification",['a','b','x',"discard"]),("Retention",['a','b','x'])]):
            y=.71-row*.28;text(a,.03,y+.065,title,12)
            for j,t in enumerate(tokens):box(a,.21+j*.19,y,.16,.14,t,'green' if j<2 else ('orange' if row==0 or t=='丢弃' else 'blue'),12)
        save(f,'11-verification')
        for draft,n in [('A','sample-A'),('B','sample-B')]:
            p=.25 if draft=='A' else .75;f,a=canvas(4.0);box(a,.32,.71,.36,.17,f'Draft always {draft}','gray')
            for x,label,prob,c in [(.03,"Accept "+draft,p,'green'),(.54,"Reject, output "+('B' if draft=='A' else 'A'),1-p,'orange')]:box(a,x,.18,.43,.19,label,c,12);arrow(a,(.5,.71),(x+.215,.37));text(a,x+.215,.48,f'Probability {prob:g}',12,ha='center')
            text(a,.5,.06,"final: P(A) = 1/4, P(B) = 3/4",12,ha='center');save(f,n)
        f,a=plot(3.6);q=np.linspace(0,60,121);sp=data['speculation']
        for d,c,x in zip(sp['drafts'],['#267398','#388768'],sp['query_break_even_ms']):a.plot(q,(sp['verification_ms']+q)/d['expected_output'],color=c,label=d['draft']);a.scatter([x],[sp['ordinary_ms']],color=c,zorder=5)
        a.axhline(sp['ordinary_ms'],color='#777777',ls='--',label="Normal decode");a.set(xlabel="Draft query per round (ms)",ylabel="Time per output token (ms)",xlim=(0,60),ylim=(0,70));a.legend(frameon=False);save(f,'12-speculation')
        for field,name in [('completed_per_s','13-service'),('slo_goodput_per_s','service-goodput')]:
            f,a=plot(4.0,bottom=.28);groups=data['service']['groups'];labels=[]
            for i,g in enumerate(groups):
                vals=[x[field] for x in g];a.bar(i,np.median(vals),color=COL['blue' if field=='completed_per_s' else 'green'],edgecolor=COL['line']);a.scatter([i]*len(vals),vals,color='#252525',s=16);labels.append(("one by one" if g[0]['service']=='serial' else "continuous" if g[0]['service']=='continuous' else "burst")+('\n'+str(g[0]['rate']) if g[0]['rate'] is not None else "\nsingle arrival"))
            a.set(xticks=range(len(groups)),xticklabels=labels,ylim=(0,3.1),ylabel="completion throughput (req/s)" if field=='completed_per_s' else "correct and on-time (req/s)",xlabel="admission policy; x-axis arrival rate (req/s)");save(f,name)
        f,a=plot(3.8);dp=data['design_plane'];a.fill_between([0,dp['capacity_gib']],0,dp['deadline_s'],color=COL['green'],alpha=.65)
        for c in data['design_plane']['configurations']:a.scatter(c['memory_gib'],c['time_s'],color='#267398');a.annotate(c['name'],(c['memory_gib'],c['time_s']),xytext=(5,5),textcoords='offset points',fontsize=12)
        a.axvline(dp['capacity_gib'],ls='--',color='#777777');a.axhline(dp['deadline_s'],ls='--',color='#777777');a.set(xlim=(0,21),ylim=(0,16.5),xlabel="KV and auxiliary buffers (GiB)",ylabel="Whole-group completion time (s)");save(f,'14-design')
        f,a=plot(3.6);s=np.array(data['task']['local_speedups'])
        for frac,col in zip(data['task']['decode_fractions'],['#267398','#388768','#a56c28']):a.plot(s,1/(1-frac+frac/s),label=f'decode share {frac:.0%}',color=col)
        a.set(xlabel="decode speedup",ylabel="full task speedup",xlim=(1,8));a.legend(frameon=False);save(f,'15-task')
    from core_principles_figures import draw as draw_principles
    draw_principles(8, out)
    from v41_case_figures import draw as draw_v41
    draw_v41(8, out)
    out.finish();return out.outputs,out.checks
