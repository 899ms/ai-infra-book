import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;s=json.loads((r/'analysis.json').read_text())
fig,axes=plt.subplots(2,2,figsize=(10,7),layout='constrained')
for i,n in enumerate([4096,65536]):
 for j,mode in enumerate(['eager','graph']):
  ax=axes[i,j]
  for k,method in enumerate(['row','split'] if n==4096 else ['row','split','streamed']):
   rows=[next(x for x in s['rows'] if x['n']==n and x['m']==m and x['method']==method and x['mode']==mode) for m in [1,32,1024]]
   ax.errorbar([0,1,2],[x['median_us'] for x in rows],yerr=[[x['median_us']-x['min_us'] for x in rows],[x['max_us']-x['median_us'] for x in rows]],marker='o',capsize=3,label={'row':'Full-vector row','split':'Split: three kernels','streamed':'Streamed row (later batch)'}[method])
  ax.set_xticks([0,1,2],['1','32','1024']);ax.set_xlabel('Rows M (categorical)');ax.set_ylabel('Complete RMSNorm (µs, log)');ax.set_yscale('log');ax.set_title(f'N={n}, {mode}');ax.legend(fontsize=8);ax.grid(axis='y',alpha=.2)
fig.suptitle('RMSNorm: row vs split reduction, same BF16 inputs\n9 batches × 20 calls; median and min–max; shared RTX, warm buffers',fontsize=12)
for ext in ['png','svg','pdf']:fig.savefig(r/f'rmsnorm-split.{ext}',dpi=160)
