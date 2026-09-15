"""Fixed-work training, recovery sensitivity and full-step communication timelines."""
from pathlib import Path
import importlib.util,json,hashlib,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('07-*.md'))
code=ROOT/'calculations/supernode_scaling.py';scenario=ROOT/'calculations/scenarios/supernode-scaling-example.json';archive=ROOT/'calculations/results/supernode-scaling-book.json'
spec=importlib.util.spec_from_file_location('scaling',code);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
c=json.loads(scenario.read_text());old=json.loads(archive.read_text())
base=[mod.evaluate(c,s,p) for p in c['profiles'] for s in c['supernode_sizes']]
assert base==old['results']
sweeps=[]
for p in c['profiles']:
 for s in c['supernode_sizes']:
  options=[mod.evaluate(dict(c,tp=tp),s,p) for tp in c['tp_candidates'] if s%tp==0 and tp<=s]
  for r in options:
   tp=r['tp'];dp=r['dp'];q=r['local_dp'];h=r['supernodes'];g=64e9/tp;bl=c['local_Bps']*p.get('local_multiplier',1);bo=r['egress_Bps']
   assert dp*c['global_tokens']/dp==2**20 and (c['global_tokens']/dp)/8192==tp/8
   oracle=2*(q-1)*c['local_alpha_s']+2*(q-1)*g/(q*bl)+2*(h-1)*c['remote_alpha_s']+max(2*(h-1)*g/(h*q*c['nic_Bps']),2*(h-1)*tp*g/(h*bo))
   assert math.isclose(oracle,r['hierarchical_s'],rel_tol=1e-13)
  best=min(options,key=lambda r:r['step_s']);sweeps.append(dict(profile=p['name'],supernode_gpus=s,best_tp=best['tp'],candidates=options))
assert sweeps==old['tp_sweep']
recovery=[]
for p in c['profiles']:
 for s in c['supernode_sizes']:
  a=mod.evaluate(c,s,p);b=mod.evaluate(dict(c,restore_Bps=c['restore_Bps']/2),s,p)
  assert a['step_s']==b['step_s'] and b['recovery_s']==60+2*s and b['effective_tokens_per_s']<a['effective_tokens_per_s']
  recovery.append(dict(profile=p['name'],supernode_gpus=s,normal=a,half_restore_bandwidth=b,effective_loss_percent=100*(1-b['effective_tokens_per_s']/a['effective_tokens_per_s'])))
M=192*2**20;alpha=.833e-6;local=14*(M/8)/450e9
flat=30*alpha+360*2**20/50e9
hier=16*alpha+local+24*2**20/50e9
slots_bw=128*256/(2e-6);required_slots=math.ceil(50e9*2e-6/256)
assert required_slots==391 and (required_slots-1)*256/(2e-6)<50e9<=required_slots*256/(2e-6)
limited=16*alpha+local+24*2**20/slots_bw
one=16*alpha+local+192*2**20/50e9
steps=[]
for name,comm,ready in [('Continuous serial',flat,20),('Hierarchical serial',hier,20),('128 slots serial',limited,20),('Continuous ready at 17',flat,17),('Hierarchical ready at 17',hier,17),('One NIC ready at 17',one,17)]:
 end=ready+comm*1000;update=max(20,end)
 steps.append(dict(name=name,compute_ms=[0,20],ready_ms=ready,communication_ms=[ready,end],update_ms=[update,update+2],step_ms=update+2))
latest=20-hier*1000;assert math.isclose(latest+hier*1000,20)
decode=[]
for name,bw,a in [('baseline',50e9,5e-6),('bandwidth_3x',150e9,5e-6),('startup_2us',50e9,2e-6)]:
 for payload in (8192,8*2**20):
  startup=14*a;transfer=1.75*payload/bw
  decode.append(dict(profile=name,payload_bytes=payload,one_allreduce_us=(startup+transfer)*1e6,total_72_ms=72*(startup+transfer)*1000,startup_72_ms=72*startup*1000,payload_72_ms=72*transfer*1000))
files=[source,code,scenario,archive]
out=dict(exercise='7-15',baseline_archive_exact_match=True,training_baseline=base,tp_sweep=sweeps,recovery=recovery,step_timelines=steps,latest_hierarchical_ready_ms=latest,slot_Bps=slots_bw,minimum_slots_for_50GBps=required_slots,decode_and_large_message=decode,scope='Book analytical models; fixed 1048576 training tokens/update; no new 1024-GPU run; restore bytes held at book 64GB/GPU; startup_2us means each ring round',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files})
(P/'7-15-results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
fig,ax=plt.subplots(figsize=(11,6))
for i,r in enumerate(steps):
 for j,(k,color) in enumerate([('compute_ms','#888888'),('communication_ms','#2878b5'),('update_ms','#39985a')]):
  a,b=r[k];ax.barh(i+j*.2,b-a,left=a,height=.17,color=color,label=k.removesuffix('_ms') if i==0 else None)
 ax.plot(r['ready_ms'],i+.2,'ko',ms=4);ax.text(r['step_ms']+.15,i+.3,f"{r['step_ms']:.3f} ms",fontsize=9)
ax.set_yticks([i+.2 for i in range(len(steps))],[r['name'] for r in steps]);ax.invert_yaxis();ax.set(xlim=(0,33),xlabel='Time from compute start (ms)',title='Training-step timelines: dots mark data readiness');ax.legend(loc='lower right');ax.grid(axis='x',alpha=.2);fig.tight_layout();fig.savefig(P/'7-15-step-timelines.png',dpi=160);fig.savefig(P/'7-15-step-timelines.svg');plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(11,4))
labels=['Scaling egress, local 450','Egress cap 400, local 450','Scaling egress, local 900']
for p,label in zip(c['profiles'],labels):
 rs=[r for r in base if r['profile']==p['name']];rr=[r for r in recovery if r['profile']==p['name']]
 axes[0].plot([r['supernode_gpus'] for r in rs],[r['tokens_per_s']/1e6 for r in rs],'o-',label=label)
 axes[1].plot([r['supernode_gpus'] for r in rr],[r['normal']['effective_tokens_per_s']/1e6 for r in rr],'o-',label=label+'; restore 64')
 axes[1].plot([r['supernode_gpus'] for r in rr],[r['half_restore_bandwidth']['effective_tokens_per_s']/1e6 for r in rr],'x--',label=label+'; restore 32')
for ax,title in zip(axes,['Normal progress (TP8)','Effective progress (TP8)']):ax.set(title=title,xlabel='GPUs per supernode',ylabel='Million tokens/s',xticks=c['supernode_sizes']);ax.grid(alpha=.2);ax.legend(fontsize=6)
fig.tight_layout();fig.savefig(P/'7-15-scaling.png',dpi=160);fig.savefig(P/'7-15-scaling.svg');plt.close(fig)
print('Baseline and TP sweep exactly match archive; all invariants passed.')
for r in base: print(r['profile'],r['supernode_gpus'],r['chosen'],round(r['step_s'],9),round(r['tokens_per_s']))
print('TP best:',[(r['profile'],r['supernode_gpus'],r['best_tp']) for r in sweeps])
print('Latest ready',latest,'steps',[(r['name'],r['step_ms']) for r in steps])
print('Decode',decode)
for r in recovery[:4]:print('recovery',r['supernode_gpus'],r['normal']['recovery_s'],r['half_restore_bandwidth']['recovery_s'],r['normal']['effective_tokens_per_s'],r['half_restore_bandwidth']['effective_tokens_per_s'])
