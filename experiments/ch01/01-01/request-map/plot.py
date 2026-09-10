"""Static worksheet and answer map; educational roles, not a hardware trace."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
r=Path(__file__).absolute().parent
labels=['1  Application / task','2  Model / workload','3  Inference system','4  Operators / runtime','5  Processor / storage','6  Interconnect / data center']
answers=['A, F: define task and validate answer','A, B, F: messages, token IDs, decoded text','B, C: accept and organize execution','D: execute model operations','E: CPU, GPU, device memory, saved records','No cross-host measurement supplied']
for filled,name in [(False,'worksheet'),(True,'answer-map')]:
 fig,ax=plt.subplots(figsize=(11,6.4));ax.set_xlim(0,11);ax.set_ylim(0,7);ax.axis('off')
 ax.text(.2,6.8,'One successful request: input → model execution → output',fontsize=15,weight='bold')
 ax.text(.2,6.35,'A Task   B Tokenize / submit   C Organize   D Operators   E Resources   F Decode / check',fontsize=10)
 for i,(label,answer) in enumerate(zip(labels,answers)):
  y=5.6-i*.85
  ax.add_patch(FancyBboxPatch((.2,y-.32),10.5,.7,boxstyle='round,pad=0.025',facecolor='#edf3f9' if i%2==0 else '#f5f7fa',edgecolor='#acb8c5'))
  ax.text(.4,y,label,fontsize=11,va='center',weight='bold')
  ax.text(4.5,y,answer if filled else 'Labels: __________________________',fontsize=10,va='center')
 ax.text(.2,.3,'Roles can span layers. This diagram does not show per-stage timing or physical traffic.',fontsize=10,color='#49515a')
 fig.tight_layout()
 for ext in ['png','svg','pdf']:fig.savefig(r/(name+'.'+ext),dpi=160)
 plt.close(fig)
