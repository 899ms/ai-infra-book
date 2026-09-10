import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;rows=json.loads((r/'analysis.json').read_text())['branch_observations'];fig,ax=plt.subplots(figsize=(8,4),layout='constrained')
for key,label in [('summed_block_references','Sum of per-branch block references'),('request_owned_blocks','Unique request-owned blocks'),('shared_by_four','Blocks shared by all four')]:ax.plot([x['snapshot'] for x in rows],[x[key] for x in rows],label=label)
ax.set_xlabel('Scheduler observation index (not elapsed GPU time)');ax.set_ylabel('Blocks / references');ax.set_title('Native n=4 sampling with a warmed prefix');ax.legend(fontsize=9);ax.grid(alpha=.2)
for ext in ['png','svg','pdf']:fig.savefig(r/('sharing.'+ext),dpi=160)
