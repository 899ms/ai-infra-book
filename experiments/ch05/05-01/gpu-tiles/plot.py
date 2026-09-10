import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;s=json.loads((r/'analysis.json').read_text())
fig,axes=plt.subplots(2,2,figsize=(10,7),layout='constrained')
labels=['32×64 / 4w','64×64 / 4w','128×128 / 8w']
for row,m in enumerate([1,1024]):
 rows=[x for x in s['rows'] if x['m']==m]
 ax=axes[row,0]; med=[x['median_ms']*1000 for x in rows]
 ax.bar(labels,med,color=['C0','C1','C2']);ax.errorbar(range(3),med,yerr=[[x['median_ms']*1000-x['min_ms']*1000 for x in rows],[x['max_ms']*1000-x['median_ms']*1000 for x in rows]],fmt='none',color='black',capsize=3)
 ax.set_ylabel('CUDA event time / call (µs)');ax.set_title(f'M={m}: median, min–max over 9 batches')
 ax=axes[row,1]
 for j,(key,label) in enumerate([('dram__bytes_op_read.sum','DRAM read'),('dram__bytes_op_write.sum','DRAM write'),('lts__t_bytes.sum','L2 traffic')]):
  ax.bar([i+(j-1)*.24 for i in range(3)],[x['metrics'][key]/1024**2 for x in rows],.24,label=label)
 ax.set_xticks(range(3),labels);ax.set_yscale('log');ax.set_ylabel('Actual counter traffic (MiB, log)');ax.set_title(f'M={m}: one warmed kernel, NCU replay');ax.set_ylim(top=max(x['metrics']['lts__t_bytes.sum']/1024**2 for x in rows)*8);ax.legend(fontsize=8,ncol=3)
fig.suptitle('Qwen3 projection shape: K=4096, N=12288, BF16 control inputs\nShared RTX PRO 6000; fixed buffers, unlocked clocks; not end-to-end speedup',fontsize=12)
for ext in ['png','svg','pdf']:fig.savefig(r/f'gpu-tiles.{ext}',dpi=160)
