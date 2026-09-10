import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;s=json.loads((r/'matrix-results/summary.json').read_text())['rows'];a=json.loads((r/'matrix-audit.json').read_text())['rows']
fig,ax=plt.subplots(1,2,figsize=(10,4),layout='constrained')
for key,label in [('int8_direct','INT8 direct'),('int8_dequant_bf16','Dequantize BF16')]:
 ax[0].plot([x['m'] for x in s],[x['stages'][key+'_e2e']['device_ms']['median']*1000 for x in s],'o-',label=label)
 ax[1].plot([x['m'] for x in a],[x['checks'][key]['relative_l2_to_cpu_fp64']*100 for x in a],'o-',label=label)
ax[1].axhline(2,color='black',linestyle='--',label='Fixed 2% threshold')
for p in ax:p.set_xscale('log');p.set_xlabel('M rows from the same actual activation pool');p.legend(fontsize=8);p.grid(alpha=.2)
ax[0].set_ylabel('CUDA event stream span (µs)');ax[1].set_ylabel('Relative L2 to CPU FP64 (%)')
fig.suptitle('Real routed expert inputs: timing does not establish a quality-preserving gain')
for ext in ['png','svg','pdf']:fig.savefig(r/f'routed-activations.{ext}',dpi=160)
