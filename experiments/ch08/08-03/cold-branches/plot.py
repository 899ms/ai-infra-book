import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;s=json.loads((r/'analysis.json').read_text());fig,axes=plt.subplots(1,2,figsize=(8,4),layout='constrained')
for ax,key,title in [(axes[0],'branch_scheduled_tokens','Scheduled token positions'),(axes[1],'peak_unique_owned','Peak unique request-owned blocks')]:
 b=ax.bar(['Cold engine','Warmed prefix'],[s[m][key] for m in ['cold','warm']],color=['#4e82b4','#d58942']);ax.bar_label(b,padding=3);ax.set_title(title);ax.set_ylim(0,max(s[m][key] for m in ['cold','warm'])*1.2);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
fig.suptitle('Native four branches: identical outputs, different scheduled work')
for ext in ['png','svg','pdf']:fig.savefig(r/('cold-warm.'+ext),dpi=160)
