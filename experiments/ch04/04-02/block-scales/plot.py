import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;s=json.loads((r/'results/summary.json').read_text())['conditions'];audit={x['label']:x for x in json.loads((r/'cpu-audit.json').read_text())['rows']}
fig,ax=plt.subplots(1,2,figsize=(12,4),layout='constrained')
for v in ['activation','both']:
 group=[x for x in s if x['variant']==v]
 for mode,style in [('direct','-o'),('dequant','--s')]:
  label=('Activation groups' if v=='activation' else 'Both operands grouped')+' / '+mode
  ax[0].plot(range(6),[x['stages'][mode]['device_ms']['median'] for x in group],style,label=label)
  ax[1].plot(range(6),[audit[x['label']]['checks'][mode]['relative_l2_to_cpu_fp64']*100 for x in group],style,label=label)
for a in ax:a.set_xticks(range(6),['P1','P8','P64','P512','D1','D8']);a.set_xlabel('Input phase and matrix row count');a.grid(alpha=.2)
ax[0].set_ylabel('CUDA event stream span (ms)');ax[0].legend(fontsize=7)
ax[1].set_ylabel('Relative L2 to CPU FP64 (%)');ax[1].axhline(2,color='black',linestyle=':',label='2% threshold');ax[1].legend(fontsize=7)
fig.suptitle('Fixed 128-element groups / real inputs / local numerical quality')
for ext in ['png','svg','pdf']:fig.savefig(r/f'block-scales.{ext}',dpi=160)
