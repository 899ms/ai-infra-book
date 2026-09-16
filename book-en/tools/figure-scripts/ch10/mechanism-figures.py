"""Mechanism illustrations, executed by build.py with shared plotting helpers."""
from matplotlib.patches import Polygon

# 3: one module's persistent shards become a temporary complete parameter.
f,a=canvas(5.8)
colors=[C[k] for k in ['blue','teal','orange','red']]
a.text(.02,.93,"long-term storage: one shard per card",fontsize=14)
for i in range(4):
 y=.73-i*.15
 a.text(.025,y+.045,f'GPU {i}',fontsize=12,va='center')
 a.add_patch(Rectangle((.14,y),.12,.09,fc=colors[i],ec='white'))
 a.text(.20,y+.045,f'W{i}',color='white',ha='center',va='center',fontsize=12)
 arrow(a,(.27,y+.045),(.50,.54),col=['blue','teal','orange','red'][i],lw=1.2)
a.text(.345,.83,"all-gather",ha='center',fontsize=12)
a.text(.52,.93,"during current module execution: temporarily assemble full weights",fontsize=14)
for i in range(4):
 a.add_patch(Rectangle((.52+i*.105,.48),.105,.12,fc=colors[i],ec='white'))
 a.text(.572+i*.105,.54,f'W{i}',color='white',ha='center',va='center',fontsize=12)
a.text(.73,.68,"using GPU 0 as example",ha='center',fontsize=11,color=C['muted'])
arrow(a,(.73,.46),(.73,.32))
box(a,.57,.15,.32,.16,"compute current module","then release full weight buffer",col='light',size=12)
a.text(.025,.075,"original shard retained; full weights occupy space only when used",fontsize=12,color=C['muted'])
save(f,'figure-10-3-sharding')
data['sharding_lifetime']={'shards':4,'illustrated_rank':0,'gathered_shard_ids':[0,1,2,3],'persistent_shard_remains':True}

# 4: a saved product occupies the long forward/backward gap; recompute occupies a short interval.
f,a=canvas(6.0)
a.text(.04,.92,'h = a ⊙ u',fontsize=16);a.text(.38,.92,"a, u already retained for backward computation",fontsize=12,color=C['muted'])
arrow(a,(.28,.79),(.95,.79));a.text(.30,.83,"forward",fontsize=12);a.text(.85,.83,"backward",fontsize=12)
for yy,label in [(.58,"save h"),(.30,"rebuild h")]:
 a.text(.035,yy+.025,label,fontsize=13,va='center')
 a.add_patch(Rectangle((.30,yy+.075),.56,.045,fc=C['line'],ec='none'))
 a.text(.58,yy+.097,"a, u retained until backward",ha='center',va='center',fontsize=10)
a.add_patch(Rectangle((.30,.56),.56,.07,fc=C['blue']))
a.text(.58,.595,"h occupies 6 MiB continuously",color='white',ha='center',va='center',fontsize=12)
a.add_patch(Rectangle((.79,.28),.07,.07,fc=C['orange']))
a.text(.54,.31,"h not saved during this period",ha='center',va='center',fontsize=12,color=C['teal'])
a.annotate("multiply before use, then release",(.825,.28),xytext=(.63,.17),fontsize=12,arrowprops={'arrowstyle':'->','color':C['orange']})
a.text(.04,.04,"retain one fewer product, trading for one rebuild before backward",fontsize=12)
save(f,'figure-10-4-recompute')
data['recompute_lifetime']={'product_shape':[128,12288],'dtype_bytes':4,'product_bytes':128*12288*4,'axis':'operation order, not measured duration'}

# 5: where conversion occurs determines how many bytes cross the same interface.
f,a=canvas(6.5)
a.add_patch(Rectangle((.045,.10),.33,.78,fc=C['pale'],ec=C['line']))
a.add_patch(Rectangle((.665,.10),.29,.78,fc=C['light'],ec=C['line']))
a.text(.21,.91,"GPU memory",ha='center',fontsize=14);a.text(.81,.91,"CPU memory",ha='center',fontsize=14)
a.text(.50,.91,"host-GPU link",ha='center',fontsize=12)
box(a,.09,.65,.22,.11,'BF16：96 MiB',size=12)
box(a,.70,.65,.21,.11,"convert to FP32",size=12,col='light')
arrow(a,(.32,.705),(.69,.705),lw=2)
a.text(.50,.75,"transfer 96 MiB",ha='center',fontsize=12,color=C['teal'])
a.text(.09,.56,"transfer first, then convert on CPU",fontsize=11)
box(a,.09,.25,.22,.18,"GPU conversion",'96 + 192 = 288 MiB',size=12,col='sand')
box(a,.70,.285,.21,.11,'FP32：192 MiB',size=12,col='light')
arrow(a,(.32,.34),(.69,.34),lw=4)
a.text(.50,.40,"transfer 192 MiB",ha='center',fontsize=12,color=C['orange'])
a.text(.09,.16,"convert first, then transfer",fontsize=11)
a.text(.50,.025,"GPU conversion is faster, but link transfers twice the data",ha='center',fontsize=13)
save(f,'figure-10-5-casting')
data['cast_paths']={'cpu_path_transfer_bytes':96*2**20,'gpu_path_transfer_bytes':192*2**20,'gpu_conversion_peak_bytes':288*2**20}

# 8: the same communication shifts beyond computation when a link is occupied.
f,ax=plt.subplots(figsize=(11.5,5.3));f.subplots_adjust(left=.18,right=.96,bottom=.18,top=.88)
for y in [3,1]:
 ax.broken_barh([(0,5)],(y-.23,.46),facecolors=C['blue']);ax.text(2.5,y,"independent compute 5 ms",color='white',ha='center',va='center',fontsize=12)
ax.broken_barh([(0,3)],(2-.23,.46),facecolors=C['teal']);ax.text(1.5,2,"reduction 3 ms",color='white',ha='center',va='center')
ax.broken_barh([(0,4)],(-.23,.46),facecolors=C['orange']);ax.text(2,0,"link occupied by other communication first",color='white',ha='center',va='center',fontsize=11)
ax.broken_barh([(4,3)],(-.23,.46),facecolors=C['teal']);ax.text(5.5,0,"reduction 3 ms",color='white',ha='center',va='center')
ax.axvline(5,ls='--',color=C['muted']);ax.axvspan(5,7,color=C['red'],alpha=.08)
ax.annotate('',xy=(5,.55),xytext=(7,.55),arrowprops={'arrowstyle':'<->','color':C['red']});ax.text(6,.70,"wait 2 ms",ha='center',color=C['red'],fontsize=12)
ax.set(yticks=[3,2,1,0],yticklabels=["link idle · compute","link idle · communication","link busy · compute","link busy · communication"],xticks=range(8),xlim=(0,7.4),ylim=(-.6,3.6),xlabel="time since gradient ready / ms");ax.spines['left'].set_visible(False)
save(f,'figure-10-8-overlap')
data['communication_window']={'compute_ms':[0,5],'free_link_reduce_ms':[0,3],'occupied_link_ms':[0,4],'queued_reduce_ms':[4,7],'wait_ms':2}

# 9: attention is area, not merely the total length along one axis.
f,axes=plt.subplots(1,2,figsize=(11,5.9));f.subplots_adjust(left=.08,right=.97,bottom=.22,top=.86,wspace=.24)
for ax,lengths,title in zip(axes,[(4096,4096),(7168,1024)],["two equal-length sequences","one long, one short"]):
 offset=0
 for n,col in zip(lengths,['blue','teal']):
  end=offset+n
  ax.add_patch(Rectangle((offset,offset),n,n,fc=C['pale'],ec=C['line'],lw=.8))
  ax.add_patch(Polygon([(offset,offset),(offset,end),(end,end)],fc=C[col],alpha=.80))
  ax.text(offset+n*.32,offset+n*.69,str(n),ha='center',va='center',fontsize=12,color='white' if n>2000 else C['ink'])
  offset=end
 pairs=sum(n*(n+1)//2 for n in lengths)
 ax.set(xlim=(0,8192),ylim=(8192,0),aspect='equal',xticks=[0,8192],yticks=[0,8192],xlabel="token position read");ax.set_title(title,fontsize=13)
 ax.text(.5,-.24,f'~ {round(pairs/1e4,-1):.0f} 10k attention pairs',transform=ax.transAxes,ha='center',fontsize=12)
axes[0].set_ylabel("token position initiating attention computation")
save(f,'figure-10-9-attention-area')
data['attention_area']={'lengths':[[4096,4096],[7168,1024]],'pairs':[16781312,26218496],'total_tokens':8192}

# 10: data is prepared at the right, then consumed from the left in batch order.
f,a=canvas(5.5)
box(a,.03,.67,.25,.18,"GPU training","just completed batch 100",col='light',size=12)
box(a,.71,.67,.25,.18,"read and preprocess","prepare upcoming training data",size=12)
for i in range(8):
 x=.12+i*.103
 a.add_patch(Rectangle((x,.34),.086,.12,fc=C['sand'],ec=C['orange'],lw=1,linestyle='--' if i>=5 else '-'))
 a.text(x+.043,.40,str(101+i),ha='center',va='center',fontsize=12)
arrow(a,(.163,.47),(.163,.66));arrow(a,(.884,.66),(.884,.47),col='orange')
a.text(.50,.56,"batch not yet used for training",ha='center',fontsize=13)
arrow(a,(.82,.23),(.22,.23));a.text(.50,.15,"fetch by batch order: 101 first, then 102...",ha='center',fontsize=12)
a.text(.14,.93,"training position: 100",ha='center',fontsize=12,color=C['teal'])
a.text(.84,.93,"prefetch position: 108",ha='center',fontsize=12,color=C['orange'])
a.text(.50,.015,"resumes from 101 after recovery; prep task ahead does not mean training is done",ha='center',fontsize=12,color=C['muted'])
save(f,'figure-10-10-input-queue')
data['input_queue']={'last_trained_batch':100,'last_dispatched_batch':108,'pending_batches':list(range(101,109)),'ready_status':'illustrative'}

# 11: identical row ranges, different partition boundaries.
f,a=canvas(5.7)
x0=.10;width=.84
for i in range(4):
 x=x0+i*width/4
 a.add_patch(Rectangle((x,.66),width/4,.15,fc=colors[i],ec='white',lw=2))
 a.text(x+width/8,.735,f'old shard {i}\n24 MiB',ha='center',va='center',color='white',fontsize=12)
 for j in [0,1]:
  xx=x+(j+.5)*width/8
  arrow(a,(xx,.65),(xx,.43),col=['blue','teal','orange','red'][i],lw=1.3)
for i in range(8):
 x=x0+i*width/8
 a.add_patch(Rectangle((x,.25),width/8,.17,fc=colors[i//2],ec='white',lw=2))
 a.text(x+width/16,.335,f'new shard {i}\n12 MiB',ha='center',va='center',color='white',fontsize=10)
a.text(.02,.92,"same 12,288-row weights",fontsize=14)
a.text(.015,.73,'TP=4',fontsize=11);a.text(.015,.33,'TP=8',fontsize=11)
for i in range(5):a.text(x0+i*width/4,.87,f'{i*3072:,}',ha='center',fontsize=10,color=C['muted'])
a.text(.52,.095,"each old shard's first and second halves go to two new shards respectively",ha='center',fontsize=12)
save(f,'figure-10-11-resharding')
data['checkpoint_resharding']={'shape':[12288,4096],'old_parts':4,'new_parts':8,'old_rows':3072,'new_rows':1536,'new_to_old':[i//2 for i in range(8)]}

# 13: checkpoint overhead is a descending and an ascending cost.
f,ax=plt.subplots(figsize=(11.2,5.9));f.subplots_adjust(left=.10,right=.96,bottom=.17,top=.90)
c=14*N/7e9;lam=1/(7.9*3600);tau=np.linspace(180,2400,350)
sv=c/tau*100;redo=lam*tau/2*100;recovery=lam*120*100;total=sv+redo+recovery
ax.plot(tau/60,sv,label="save: longer interval, less amortization",color=C['blue'],lw=2)
ax.plot(tau/60,redo,label="redo: longer interval, more loss",color=C['orange'],lw=2)
ax.plot(tau/60,total,label="total (incl. recovery)",color=C['teal'],lw=2.5)
opt=(2*c/lam)**.5;val=(c/opt+lam*opt/2+lam*120)*100
ax.plot(opt/60,val,'o',color=C['teal']);ax.annotate("lowest point about 16 min",(opt/60,val),xytext=(20,5.4),fontsize=12,arrowprops={'arrowstyle':'->','color':C['teal']})
ax.set(xlim=(3,40),ylim=(0,9),xticks=[5,15,30,40],xlabel="effective training time between saves / min",ylabel="extra time per unit effective training time / %");ax.legend(frameon=False,fontsize=10);ax.grid(alpha=.15)
save(f,'figure-10-13-save-interval')
data['checkpoint_tradeoff']={'checkpoint_seconds':c,'job_failure_rate_per_second':lam,'restore_seconds':120,'interval_seconds':tau.tolist(),'save_percent':sv.tolist(),'redo_percent':redo.tolist(),'total_percent':total.tolist(),'optimal_seconds':opt}

# 14: one feedback loop, with a visibly narrower verification stage.
f,a=canvas(5.9)
box(a,.025,.52,.23,.22,"generation","throughput: 12 items/s",col='pale',size=14)
box(a,.38,.52,.23,.22,"Verification","throughput: 6 items/s",col='sand',size=14)
box(a,.745,.52,.23,.22,"learning","throughput: 8 items/s",col='light',size=14)
arrow(a,(.26,.63),(.375,.63),lw=3);arrow(a,(.615,.63),(.74,.63),lw=1.5)
a.text(.32,.80,"awaiting verification",ha='center',fontsize=11,color=C['orange'])
a.text(.68,.80,"4.5 items/s",ha='center',fontsize=12,color=C['teal'])
a.annotate('',xy=(.67,.28),xytext=(.67,.59),arrowprops={'arrowstyle':'->','color':C['red']})
a.text(.67,.20,"version too old: discard 25%",ha='center',fontsize=11,color=C['red'])
a.plot([.86,.86,.14,.14],[.50,.08,.08,.50],color=C['blue'],lw=1.3)
a.annotate('',xy=(.14,.51),xytext=(.14,.36),arrowprops={'arrowstyle':'-|>','color':C['blue']})
a.text(.35,.105,"new weights sent back to generator",ha='center',fontsize=12,color=C['blue'])
a.text(.03,.93,"verification passes 6/s; after filtering only 4.5/s enter learning",fontsize=13)
save(f,'figure-10-14-rl-flow')
data['rl_supply_flow']={'generate_capacity':12,'verify_capacity':6,'learn_capacity':8,'retained_fraction':.75,'effective_rate':4.5}

# 16: overlapping independent stages changes the interval between weight synchronizations.
f,ax=plt.subplots(figsize=(11.5,5.8));f.subplots_adjust(left=.18,right=.96,bottom=.17,top=.88)
for y,items in [(3,[(0,40,"generate current batch",'blue'),(56,4,'','orange')]),(2,[(40,16,"learn current batch",'teal'),(56,4,'','orange')]),(1,[(0,40,"generate next batch",'blue'),(40,4,'','orange')]),(0,[(0,16,"learn previous batch",'teal'),(40,4,'','orange')])]:
 for start,duration,label,col in items:
  ax.broken_barh([(start,duration)],(y-.24,.48),facecolors=C[col]);ax.text(start+duration/2,y,label,ha='center',va='center',color='white',fontsize=11)
ax.axvline(44,color=C['muted'],ls='--');ax.axvline(60,color=C['muted'],ls='--')
ax.text(60,3.48,'60 s',ha='center',fontsize=12);ax.text(44,1.48,'44 s',ha='center',fontsize=12)
ax.text(20,-.55,"orange: syncing new weights, both ends paused",fontsize=11,color=C['orange'])
ax.set(xlim=(0,63),ylim=(-.8,3.8),yticks=[3,2,1,0],yticklabels=["sync · generator","sync · learner","async · generator","async · learner"],xlabel="time / s",xticks=[0,16,40,44,56,60]);ax.spines['left'].set_visible(False)
save(f,'figure-10-16-async-cycle')
data['rl_async_cycle']={'generate_seconds':40,'learn_seconds':16,'sync_seconds':4,'sequential_period_seconds':60,'overlapped_period_seconds':44,'minimum_retained_fraction':44/60}

# 18: chronological budget, with the same 30-day limit across designs.
case=read('manuscripts/ch10/design-case.json')
f,ax=plt.subplots(figsize=(11.5,5.1));f.subplots_adjust(left=.12,right=.94,bottom=.20,top=.84)
for y,row in zip([1,0],case['candidates']):
 parts=[row['base_training_days'],row['base_training_days']*row['total_loss'],5];left=0
 for j,(val,col) in enumerate(zip(parts,['blue','orange','muted'])):
  ax.barh(y,val,left=left,height=.38,color=C[col],label=["training (incl. communication & input wait)","save & recovery","planned stall"][j] if y==1 else None)
  if j!=1:ax.text(left+val/2,y,f'{val:.1f} days',ha='center',va='center',color='white',fontsize=12)
  left+=val
 ax.text(left+.4,y,f'{left:.1f} days',va='center',fontsize=13)
ax.axvline(30,color=C['red'],ls='--',lw=1.4);ax.text(30,1.53,"30-day deadline",ha='center',fontsize=12,color=C['red'])
ax.annotate('',xy=(26.0695,-.34),xytext=(30,-.34),arrowprops={'arrowstyle':'<->','color':C['teal']});ax.text(28,-.55,"margin about 3.9 days",ha='center',fontsize=11,color=C['teal'])
ax.set(xlim=(0,39),ylim=(-.75,1.75),yticks=[1,0],yticklabels=["32 cards","48 cards"],xlabel="time to complete entire task / days");ax.legend(loc='upper left',bbox_to_anchor=(0,1.22),ncol=3,frameon=False,fontsize=10)
save(f,'figure-10-18-deadline')
data['task_deadline_breakdown']={'parts':['base_training_days','checkpoint_and_recovery_days','planned_days'],'rows':[{'devices':r['devices'],'days':[r['base_training_days'],r['base_training_days']*r['total_loss'],5],'finish_days':r['finish_days']} for r in case['candidates']],'deadline_days':30}
