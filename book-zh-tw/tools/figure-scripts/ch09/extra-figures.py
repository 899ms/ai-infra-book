"""Chapter-nine mechanism diagrams. Executed by build.py with its drawing helpers."""

# Three workloads redistribute the same four A100 and four H20.
alloc=[(calc(n)['summary'],n) for n in ['pd-pool-book','pd-pool-prefix','pd-pool-short-output']]
f,a=canvas(5.8)
for (sm,name),(y,title) in zip(alloc,[(.76,"推理請求：8192 輸入，1025 輸出"),(.47,"命中 6144 個字首位置"),(.18,"輸出減至 129 個 token")]):
 pa=sm['best_prefill_workers']['A100'];ph=sm['best_prefill_workers']['H20'];rate=num(sm['best_pd_bound_requests_per_second_exact'])
 a.text(.025,y+.14,title,fontsize=12,weight='bold')
 for i in range(8):
  isp=i<pa if i<4 else i-4<ph
  x=.05+i*.10
  a.add_patch(Rectangle((x,y),.082,.10,fc=C['blue'] if isp else C['teal'],ec='white'))
  a.text(x+.041,y+.05,('A100' if i<4 else 'H20')+('\nP' if isp else '\nD'),ha='center',va='center',fontsize=9,color='white')
 a.text(.86,y+.05,f'{rate:.2f} 請求/s',va='center',fontsize=11)
a.text(.05,.02,"藍色：prefill     綠色：decode",fontsize=11)
save(f,'figure-9-4-allocation')
data['new-allocation']={'prefill_A100':[sm['best_prefill_workers']['A100'] for sm,_ in alloc],'prefill_H20':[sm['best_prefill_workers']['H20'] for sm,_ in alloc],'rates':[num(sm['best_pd_bound_requests_per_second_exact']) for sm,_ in alloc]}

# Same task count: each rectangle's area equals rows times active experts. Section 9.3.3 now recalls this
# from section 6.3.2 in prose, so the two rectangle figures were dropped; the numbers stay under validation.
data['new-footprint']={'active_experts':[128,8],'rows_per_expert':[4,64],'weight_MiB':[4608,288],'assignments':512}

# Synchronization waits for the busiest card, with identical total work. HGX H100 at 50% of the 989.4 TFLOP/s BF16 dense peak.
H100_EFF=989.4e12/2
f,axes=plt.subplots(2,1,figsize=(11,7),sharex=True);f.subplots_adjust(left=.12,right=.96,bottom=.12,top=.91,hspace=.50)
for ax,counts,title in [(axes[0],[64]*8,"均勻放置：八張卡同時完成"),(axes[1],[512]+[0]*7,"八個熱點專家在同一卡：其餘卡等待")]:
 times=np.array(counts)*2*18874368/H100_EFF*1e6
 ax.barh(range(8),times,color=C['teal'],height=.65);ax.invert_yaxis()
 ax.set(yticks=range(8),yticklabels=[f'卡 {i}' for i in range(8)],xlim=(0,46),xticks=[0,10,20,30,40])
 ax.set_title(title,loc='left',fontsize=13);ax.axvline(max(times),color=C['orange'],ls='--')
 ax.text(max(times)+.6,3,f'{max(times):.1f} μs\n後可合併',fontsize=11)
 ax.grid(axis='x',alpha=.15)
axes[1].set_xlabel("完成本卡專家計算所需時間 / μs")
save(f,'figure-9-9-balance')
data['new-balance']={'assignments_per_card':[[64]*8,[512]+[0]*7],'device':'H100 SXM','effective_TFLOPs':494.7,'busiest_us':[64*2*18874368/H100_EFF*1e6,512*2*18874368/H100_EFF*1e6]}

# A schedule rather than a summed bar explains what overlap actually hides. Stage times: balanced cross-server row of ep-skew-book.
ep=json.loads((ROOT/'calculations/results/ep-skew-book.json').read_text())['results'][0];assert ep['name']=='均衡'
D,Cc,Rr=ep['dispatch']['lower_s']*1e3,max(ep['compute_s'])*1e3,ep['combine']['lower_s']*1e3
d,c,r=D/2,Cc/2,Rr/2;c2=max(2*d,d+c);r2=max(c2+c,d+c+r)
serial_items=[(0,0,D,"分派"),(1,D,Cc,"計算"),(2,D+Cc,Rr,"合併")]
pipe_items=[(0,0,d,'1'),(0,d,d,'2'),(1,d,c,'1'),(1,c2,c,'2'),(2,d+c,r,'1'),(2,r2,r,'2')]
pipeline=r2+r;assert abs(pipeline-ep['two_microbatch_pipeline_s']*1e3)<1e-9
f,axes=plt.subplots(2,1,figsize=(11,6.6),sharex=True);f.subplots_adjust(left=.15,right=.97,bottom=.12,top=.91,hspace=.65)
for ax,(title,items) in zip(axes,[(f'序列：{D+Cc+Rr:.3f} ms',serial_items),(f'兩個微批流水：{pipeline:.3f} ms',pipe_items)]):
 for row,start,dur,txt in items:
  ax.barh(row,dur,left=start,height=.65,color=C[['blue','teal','orange'][row]],edgecolor='white')
  ax.text(start+dur/2,row,txt,ha='center',va='center',color='white',fontsize=11)
 ax.set(yticks=[0,1,2],yticklabels=["分派","專家計算","結果合併"],xlim=(0,.9),ylim=(2.6,-.6))
 ax.set_title(title,loc='left',fontsize=13);ax.grid(axis='x',alpha=.15)
axes[1].set(xlabel="時間 / ms",xticks=[0,.2,.4,.6,.8])
save(f,'figure-9-11-overlap')
data['new-overlap']={'source':'ep-skew-book','stage_ms':[D,Cc,Rr],'serial_ms':D+Cc+Rr,'pipeline_ms':pipeline,'serial_items':serial_items,'pipeline_items':pipe_items,'comm_stretch':ep['pipeline_break_even_comm_stretch'],'compute_stretch':ep['pipeline_break_even_compute_stretch']}

# Each row is a dependency timeline. Queue and retrieval start together. Compute times follow the A100 at 50% of peak.
cr={k:calc(f'cache-route-a100-{k}')['summary'] for k in ['50gbe','200gbe']}
V=cr['50gbe']['prefix_state_bytes'];host=num(cr['50gbe']['host_gpu_transfer_ns_exact'])/1e6
warm=num(cr['50gbe']['warm_compute_ns_exact'])/1e6;full=num(cr['50gbe']['full_compute_ns_exact'])/1e6
routes=[("A：本地命中",250,None,warm),("B：本地重算",20,None,full),("B：遠端 50 GbE",20,'50gbe',warm),("B：遠端 200 GbE",20,'200gbe',warm)]
f,axes=plt.subplots(4,1,figsize=(11,8.2),sharex=True);f.subplots_adjust(left=.13,right=.97,bottom=.11,top=.94,hspace=.85)
finish=[];segments=[]
for ax,(title,q,key,c) in zip(axes,routes):
 ax.barh(0,q,color=C['line'],height=.6)
 ready=0;segs=[]
 if key:
  for duration,col in [(10,'muted'),(num(cr[key]['remote_transfer_ns_exact'])/1e6,'orange'),(host,'blue')]:
   ax.barh(1,duration,left=ready,color=C[col],height=.6,edgecolor='white');segs.append(duration);ready+=duration
 start=max(q,ready);finish.append(start+c);segments.append(segs)
 ax.barh(0,c,left=start,color=C['teal'],height=.6)
 ax.axvline(start+c,color=C['teal'],ls=':',alpha=.7)
 ax.text(start+c+8,.2,f'{start+c:.0f} ms',fontsize=11)
 ax.set(yticks=[0,1],yticklabels=['GPU',"取回"],ylim=(1.6,-.6),xlim=(0,1000),xticks=[0,200,400,600,800,1000])
 ax.set_title(title,loc='left',fontsize=12);ax.grid(axis='x',alpha=.12)
axes[-1].set_xlabel("從請求到達開始的時間 / ms")
f.text(.14,.025,"灰：排隊／查詢    橙：遠端讀取    藍：主存 → GPU    綠：計算",fontsize=11)
save(f,'figure-9-13-route')
rows={k:{row['path']:num(row['finish_ns_exact'])/1e6 for row in calc(f'cache-route-a100-{k}')['cache_route_paths']} for k in cr}
assert all(abs(x-y)<1e-9 for x,y in zip(finish,[rows['50gbe']['A valid HBM'],rows['50gbe']['B recompute'],rows['50gbe']['B remote through host'],rows['200gbe']['B remote through host']]))
data['new-route']={'sources':['cache-route-a100-50gbe','cache-route-a100-200gbe'],'queues_ms':[q for _,q,_,_ in routes],'compute_ms':[c for *_,c in routes],'retrieval_segments_ms':segments,'first_token_ms':finish,'host_ms':host}

# Background copying catches a moving frontier: one H20 D worker (batch 32, average context 8704) keeps decoding while its KV is copied.
h20=next(x for x in calc('pd-pool-book')['derived_stage_rates'] if x['device']=='h20-sxm5-96gb')
kv_token=147456;V0=32*8704*kv_token/1e9;g=num(h20['decode']['calls_per_second_exact'])*kv_token/1e9
links=[(25,'teal',"目標經 200 Gb/s 網路卡：25 GB/s"),(6.25,'blue',"目標經 50 GbE：6.25 GB/s")]
catch=[V0/(B-g) for B,_,_ in links]
f,ax=plt.subplots(figsize=(10,5.5));f.subplots_adjust(left=.12,right=.96,bottom=.17,top=.91)
t=np.linspace(0,8,321);ax.plot(t,V0+g*t,label=f'源端：{V0:.1f} GB，每秒增長 {g:.3f} GB',color=C['orange'],lw=2.5)
for (B,col,label),tc in zip(links,catch):
 ax.plot(t,np.minimum(B*t,V0+g*t),label=label,color=C[col],lw=2.5)
 ax.scatter([tc],[V0+g*tc],color=C['ink'],zorder=3);ax.annotate(f'約 {tc:.2f} s 趕上',xy=(tc,V0+g*tc),xytext=(tc+.35,V0-14),fontsize=12,arrowprops={'arrowstyle':'->'})
ax.set(xlabel="後臺複製開始後的時間 / s",ylabel="累計狀態大小 / GB",xlim=(0,8),ylim=(0,50));ax.legend(frameon=False,loc='lower right',fontsize=10);ax.grid(alpha=.15)
save(f,'figure-9-14-migration')
data['new-migration']={'source':'pd-pool-book','initial_GB':V0,'growth_GBs':g,'copy_GBs':[B for B,_,_ in links],'catchup_s':catch}

# Token log and KV checkpoint have different ends.
f,a=canvas(6)
for y,title in [(.72,"已返回並記錄的序列"),(.43,"故障前儲存的 KV"),(.14,"重建後繼續生成")]:
 a.text(.025,y+.15,title,fontsize=12,weight='bold')
 box(a,.04,y,.39,.10,"輸入：8192 個 token",col='pale',fs=11)
 if y!=.43:
  box(a,.45,y,.32,.10,"已返回輸出 1—1024",col='green',fs=11)
  box(a,.80,y,.16,.10,"輸出 1025",col='sand',fs=11)
 else:
  a.text(.47,y+.05,"缺少生成部分的 KV",va='center',fontsize=12,color=C['orange'])
a.text(.46,.32,"將已記錄的輸出 1—1024 重新送入模型",fontsize=11,color=C['teal'])
a.text(.05,.015,"KV 先恢復到 9216 個 token，再處理輸出 1025，生成下一個 token。",fontsize=12)
save(f,'figure-9-15-recovery')
data['new-recovery']={'input_positions':8192,'delivered_outputs':1025,'replayed_outputs':1024,'restored_KV_positions':9216}
