"""Mechanism diagrams for chapters 1–3; quantitative inputs are existing chapter examples.

Called by chapter builders so fonts, artifact manifests and offline embedding remain shared.
Existing numbered filenames are stable; manuscript captions determine reading order.
"""
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
BLUE='#246f91';TEAL='#138b83';ORANGE='#c9782b';GRAY='#dce5e9';INK='#193441'
def panel(ax,title):
 ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off');ax.text(.02,.94,title,fontsize=15,weight='bold',va='top')
def box(ax,x,y,w,h,label,color=BLUE,fs=12):
 ax.add_patch(Rectangle((x,y),w,h,facecolor=color,alpha=.13,edgecolor=color,lw=1.5))
 ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=fs,color=INK,linespacing=1.6)
def arrow(ax,p,q):ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=15,color=INK,lw=1.5))
def draw(ch,save,root):
 meta={}
 if ch==1:
  f,axs=plt.subplots(1,2,figsize=(14,7));f.subplots_adjust(left=.05,right=.96,wspace=.18,bottom=.1,top=.9)
  a=axs[0];a.set_title("A  Same total capacity, different placement",loc='left',fontsize=15,pad=24)
  for y,weights in [(3,[140,0]),(0,[70,70])]:
   for j,v in enumerate(weights):
    yy=y+1-j;a.barh(yy,v,height=.6,color=BLUE);a.plot([80,80],[yy-.42,yy+.42],color=ORANGE,lw=2)
    a.text(max(v,80)+3,yy,f'{v} GB',va='center',fontsize=12)
  a.set(yticks=[4,3,1,0],yticklabels=["concentrated: card 1","card 2","even split: card 1","card 2"],xlim=(0,162),xlabel="weights stored per card (GB)");a.text(82,2,"Capacity per card 80 GB",color=ORANGE);a.spines[['top','right']].set_visible(False)
  a=axs[1];panel(a,"B  After fitting, still needs continuous reading")
  box(a,.05,.58,.37,.20,"GPU memory\nweights 70 GB",BLUE);box(a,.65,.58,.30,.20,"Compute unit\nblock-by-block",TEAL)
  arrow(a,(.43,.68),(.64,.68));a.text(.54,.48,"Read once per step",ha='center',fontsize=12)
  box(a,.09,.17,.82,.19,"70 GB ÷ 3350 GB/s ≈ 20.90 ms\nWeights in memory, reading still takes time",ORANGE)
  save(f,'figure-1-capacity-path');meta['capacity_path']={'capacity_GB':80,'weights_GB':140,'read_GB':70,'bandwidth_GBs':3350}
  f,axs=plt.subplots(1,2,figsize=(14,8));f.subplots_adjust(left=.08,right=.96,top=.88,bottom=.18,wspace=.3)
  batches=np.unique(np.r_[np.geomspace(1,512,150),1,8,64,128,256,512]);N=70e9;compute=2*batches*N/989.4e12;read=np.full_like(batches,70e9/3.35e12);lower=np.maximum(compute,read);cross=989.4e12/(2*3.35e12)
  a=axs[0];a.plot(batches,compute*1e3,label=r'$F/\Pi$',color=BLUE,lw=2);a.plot(batches,read*1e3,label=r'$R_W/\beta$',color=ORANGE,lw=2);a.plot(batches,lower*1e3,label=r'$T_{\mathrm{lower}}$',color=INK,lw=2,ls='--')
  a.set(xscale='log',xlabel=r'batch $B$',ylabel="time per batch (ms)",ylim=(0,80));a.set_title("A  Read-compute turning point",loc='left',fontsize=15);a.axvline(cross,color=TEAL,ls=':');a.text(cross*1.07,59,r'$B_*\approx148$',fontsize=13,color=TEAL);a.legend(fontsize=12,loc='upper left')
  a=axs[1];a.plot(batches,batches/lower,color=TEAL,lw=2.5);a.axvline(cross,color=TEAL,ls=':');a.set(xscale='log',xlabel=r'batch $B$',ylabel="ideal throughput (token/s)",ylim=(0,8000));a.set_title("B  Predicted throughput of same model",loc='left',fontsize=15)
  a.text(3,6800,"Compute limit $\\Pi/(2N)$",fontsize=13);a.text(2,3700,"Read-bound: increase reuse\nCompute-bound: throughput plateaus",fontsize=12,linespacing=1.8)
  for a in axs:a.set_xticks([1,8,64,512],['1','8','64','512']);a.grid(alpha=.15)
  save(f,'figure-1-batch-transition');meta['batch_transition']={'parameters':N,'bytes_per_weight':1,'compute_flops_s':989.4e12,'bandwidth_bytes_s':3.35e12,'crossing_batch':cross,'batch':batches.tolist(),'compute_seconds':compute.tolist(),'read_seconds':read.tolist(),'lower_seconds':lower.tolist(),'throughput':(batches/lower).tolist()}
 if ch==2:
  f,axs=plt.subplots(1,3,figsize=(14,8));f.subplots_adjust(left=.10,right=.95,wspace=.60,top=.9,bottom=.15)
  names=['V4.1 Flash','Qwen3-8B','Qwen3.6','V4-Flash','K3']; colors=['#965466',BLUE,TEAL,ORANGE,'#786295']
  for a,vals,title in zip(axs,[[40,36,40,43,93],[5120,4096,2048,4096,7168],[384,0,256,256,896]],["layers","hidden dimension","routed experts per layer"]):
   a.barh(names,vals,color=colors,height=.55);a.invert_yaxis();a.set_title(title,fontsize=15,pad=20);a.set_xlim(0,max(vals)*1.3)
   for i,v in enumerate(vals):a.text(v+max(vals)*.035,i,str(v) if v else "dense FFN",va='center',fontsize=12)
   a.spines[['top','right']].set_visible(False)
  save(f,'figure-2-architecture');meta['architecture']={'layers':[40,36,40,43,93],'hidden':[5120,4096,2048,4096,7168],'experts':[384,0,256,256,896]}
  f,axs=plt.subplots(1,2,figsize=(14,8));f.subplots_adjust(left=.07,right=.96,wspace=.3,top=.88,bottom=.17)
  a=axs[0];a.set_title("A  One row per decode read",loc='left',fontsize=15,pad=18)
  for j in range(4):
   for x in range(4+j):a.add_patch(Rectangle((x,j),.91,.76,color=BLUE if x<4 else TEAL))
   a.add_patch(Rectangle((4+j,j),.91,.76,fill=False,edgecolor=ORANGE,lw=2))
  a.set(xlim=(-.2,8),ylim=(4.9,-.3),xticks=np.arange(8)+.45,xticklabels=range(1,9),yticks=np.arange(4)+.38,yticklabels=["step 1","step 2","step 3","step 4"],xlabel="history positions (example: H = 4)")
  a.text(0,4.25,"Blue: original input   Green: previously generated   Empty: appended this step",fontsize=10)
  a.spines[['top','right']].set_visible(False)
  a=axs[1];a.set_title("B  Weights shared, history stored separately",loc='left',fontsize=15,pad=18)
  batches=np.arange(1,65);weight=15136811008/2**30
  a.axhline(weight,color=ORANGE,lw=2,label="shared weights read once per batch")
  for n,col in [(8192,BLUE),(2048,TEAL)]:a.plot(batches,batches*147456*n/2**30,color=col,lw=2,label=f'per-request history {n//1024}K')
  for b,n in [(13,8192),(51,2048)]:a.scatter(b,b*147456*n/2**30,color=INK);a.annotate(f'B = {b}',(b,b*147456*n/2**30),xytext=(b-4,24),arrowprops={'arrowstyle':'->','color':INK})
  a.set(xlabel="requests per batch",ylabel="read volume per step (GiB)",xlim=(1,64),ylim=(0,74));a.legend(loc='upper left',fontsize=10)
  save(f,'figure-2-history');meta['history']={'schematic_H':4,'schematic_decode_steps':4,'read_counts':[4,5,6,7],'final_positions':8,'kv_bytes_per_position':147456,'shared_weight_bytes':15136811008,'batch_crossings':[13,51]}
  f,axs=plt.subplots(1,2,figsize=(14,8));f.subplots_adjust(left=.05,right=.96,wspace=.16,bottom=.08,top=.92)
  for a,title,count,rows,size in [(axs[0],"A evenly distributed to 256 experts",256,2,'1.5 GiB'),(axs[1],"B concentrated to same 8 experts",8,64,'48 MiB')]:
   panel(a,title);box(a,.12,.73,.76,.10,"64 tokens × 8 experts each",BLUE)
   arrow(a,(.5,.71),(.5,.64))
   if count==256:
    for i in range(16):box(a,.08+(i%8)*.105,.43+(i//8)*.08,.085,.055,'',TEAL)
    a.text(.5,.34,"256 small matrices, each processing 2 rows",ha='center',fontsize=12)
   else:
    for i in range(8):box(a,.08+i*.105,.42,.085,.19,'',TEAL)
    a.text(.5,.34,"8 large matrices, each processing 64 rows",ha='center',fontsize=12)
   box(a,.12,.13,.76,.12,f'512 expert input rows total\ndifferent expert weights total {size}',ORANGE)
  save(f,'figure-2-expert-reuse');meta['expert_reuse']={'batch':64,'top_k':8,'total_assignments':512,'unique_experts':[256,8],'rows_per_expert':[2,64],'expert_weight_MiB':6,'read_MiB':[1536,48]}
  f,axs=plt.subplots(1,2,figsize=(14,8));f.subplots_adjust(left=.05,right=.96,wspace=.18,bottom=.08,top=.92)
  a=axs[0];panel(a,"A  History saved per position")
  for j in range(6):box(a,.06+j*.145,.57,.13,.16,f'position {j+1}',BLUE,11)
  box(a,.25,.19,.50,.13,"current query",ORANGE)
  for j in range(6):arrow(a,(.50,.33),(.125+j*.145,.55))
  a.text(.50,.82,"Query uses K, V of each position",ha='center',fontsize=12)
  a.text(.50,.10,"As positions increase, history list grows",ha='center',fontsize=12)
  a=axs[1];panel(a,"B  Aggregated into fixed-size state matrix")
  box(a,.04,.59,.28,.15,"Old state matrix",BLUE)
  box(a,.40,.59,.24,.15,"update",TEAL)
  box(a,.72,.59,.25,.15,"New state matrix",BLUE)
  arrow(a,(.33,.66),(.39,.66));arrow(a,(.65,.66),(.71,.66))
  box(a,.40,.31,.24,.14,"Current k, v",ORANGE);arrow(a,(.52,.46),(.52,.58))
  a.text(.50,.19,r'$\mathcal{S}_t=\mathcal{S}_{t-1}+k_tv_t^{\mathsf{T}}$',ha='center',fontsize=17)
  a.text(.50,.08,"matrix size fixed; content updated each step",ha='center',fontsize=12)
  save(f,'figure-2-recurrence');meta['recurrence']={'kind':'schematic linear outer-product update','history_list_positions':6,'state_shape':'fixed'}
  d=json.loads((root/'manuscripts/ch02/model-comparison.json').read_text())['models']
  f,axs=plt.subplots(2,2,figsize=(14,9));f.subplots_adjust(left=.14,right=.95,top=.91,bottom=.12,wspace=.45,hspace=.55)
  specs=[('uniform_bf16_bytes',1e9,"Full BF16 weights (GB)"),('decode_matrix_flops',1e9,"8K history single-step decode (GFLOPs)"),('state_8192_bytes',2**20,"8K history state (MiB)"),('selected_routed_expert_bf16_bytes',2**30,"single-token selected routed expert weights (GiB)")]
  for a,(key,unit,title) in zip(axs.flat,specs):
   vals=[z[key]/unit for z in d];a.barh(names,vals,color=colors,height=.55);a.invert_yaxis();a.set_title(title,fontsize=13,pad=16);a.set_xlim(0,max(vals)*1.36)
   for i,v in enumerate(vals):a.text(v+max(vals)*.025,i,f'{v:.2f}' if v else "non-routed expert",va='center',fontsize=11)
  save(f,'figure-2-resources');meta['resource_comparison']={'source':'manuscripts/ch02/model-comparison.json','models':d}
 if ch==3:
  f,axs=plt.subplots(1,2,figsize=(14,8));f.subplots_adjust(left=.06,right=.95,wspace=.25,top=.91,bottom=.13)
  a=axs[0];panel(a,"A same 100 attempts completed")
  for y,title,success,cost in [(.56,"original system",50,100),(.19,"new system",80,200)]:
   a.text(.04,y+.21,title,fontsize=13,weight='bold')
   for j in range(100):a.add_patch(Rectangle((.04+(j%20)*.044,y+(j//20)*.031),.036,.022,color=TEAL if j<success else GRAY))
   a.text(.04,y-.055,f'success {success} times; total model cost {cost} units',fontsize=12)
  a=axs[1];a.set_title("B total cost ÷ successes",loc='left',fontsize=15,pad=18)
  a.bar(["original system","new system"],[2,2.5],color=[BLUE,ORANGE],width=.5);a.set(ylabel="model cost per successful task (relative units)",ylim=(0,3.5))
  for x,t,y in [(0,'100 / 50 = 2',2),(1,'200 / 80 = 2.5',2.5)]:a.text(x,y+.12,t,ha='center',fontsize=13)
  save(f,'figure-3-success-cost');meta['success_cost']={'teaching_assumption':True,'trials':100,'successes':[50,80],'relative_total_cost':[100,200],'cost_per_success':[2,2.5]}
  f,axs=plt.subplots(1,2,figsize=(14,8));f.subplots_adjust(left=.05,right=.96,wspace=.16,bottom=.08,top=.92)
  a=axs[0];panel(a,"A spatial merging reduces position count")
  for i in range(8):
   for j in range(8):a.add_patch(Rectangle((.06+j*.038,.52+i*.033),.034,.029,color=TEAL if (i//2+j//2)%2 else BLUE,alpha=.65))
  a.text(.21,.43,"40 × 40 patches\nlocal 8 × 8 shown",ha='center',fontsize=12)
  arrow(a,(.40,.64),(.60,.64))
  for i in range(4):
   for j in range(4):a.add_patch(Rectangle((.65+j*.062,.52+i*.06),.056,.054,color=TEAL if (i+j)%2 else BLUE,alpha=.65))
  a.text(.77,.43,"20 × 20\n400 positions total",ha='center',fontsize=12)
  box(a,.07,.17,.83,.13,"every 2 × 2 patches merge into one position\n1600 positions → 400 positions",ORANGE)
  a=axs[1];panel(a,"B feature widens, position count unchanged")
  for j in range(4):box(a,.05+j*.225,.62,.21,.14,'400 × 2560',BLUE if j==0 else TEAL,10)
  a.text(.49,.54,"final features + 3 sets of DeepStack features",ha='center',fontsize=12)
  arrow(a,(.49,.49),(.49,.43));box(a,.08,.29,.82,.13,'EC：400 × 10240，BF16\n7.8125 MiB',TEAL)
  arrow(a,(.49,.28),(.49,.22));box(a,.08,.06,.82,.15,"language model stores KV for 400 positions\n400 × 144 KiB = 56.25 MiB",ORANGE)
  save(f,'figure-3-vision-shapes');meta['vision_shapes']={'pixels':[640,640],'patch_pixels':[16,16],'patch_grid':[40,40],'merge':[2,2],'positions':400,'feature_groups':4,'feature_width':2560,'ec_bytes':8192000,'kv_bytes':400*147456}
  f,axs=plt.subplots(1,2,figsize=(14,8));f.subplots_adjust(left=.1,right=.97,top=.85,bottom=.2,wspace=.3)
  variants=[("A tools serial, total time 21s",[(0,2,3,BLUE),(2,6,2,TEAL),(8,10,1,ORANGE),(18,3,3,BLUE)],16),("B tools parallel, total time 15s",[(0,2,3,BLUE),(2,6,2,TEAL),(2,10,1,ORANGE),(12,3,3,BLUE)],10)]
  for a,(title,blocks,wait) in zip(axs,variants):
   for start,duration,y,col in blocks:
    a.broken_barh([(start,duration)],(y-.25,.5),facecolors=col);a.text(start+duration/2,y,str(duration)+' s',ha='center',va='center',color='white',fontsize=12)
   a.broken_barh([(2,wait)],(-.25,.5),facecolors=GRAY);a.text(2+wait/2,0,f'1 GiB × {wait} s',ha='center',va='center',fontsize=12)
   a.set(xlim=(0,22),ylim=(-.7,3.8),yticks=[0,1,2,3],yticklabels=["retained state","tool 2","tool 1","model"],xlabel="time since task start (s)");a.set_title(title,loc='left',fontsize=14);a.grid(axis='x',alpha=.15);a.set_xticks([0,2,8,12,18,21])
  save(f,'figure-3-tool-dependency');meta['tool_dependency']={'model_seconds':[2,3],'tool_seconds':[6,10],'serial_seconds':21,'parallel_seconds':15,'retained_GiB':1,'tool_wait_GiB_s':[16,10]}
 return meta
