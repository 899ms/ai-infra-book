import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
r=Path(__file__).absolute().parent;s=json.loads((r/'summary.json').read_text())
fig,ax=plt.subplots(1,2,figsize=(8,3.8),layout='constrained')
for i,c in enumerate(s['reports']):
 m=c['metrics'];ax[0].bar([j+(i-.5)*.32 for j in range(3)],[m[k]/1e6 for k in ['dram__bytes_op_read.sum','dram__bytes_op_write.sum','lts__t_bytes.sum']],.32,label=c['format'].upper()+' KV')
ax[0].set_xticks(range(3),['DRAM read','DRAM write','L2 requests']);ax[0].set_ylabel('Measured MB (decimal)');ax[0].legend()
ax[1].bar(['BF16 KV','FP8 KV'],[c['metrics']['gpu__time_duration.sum']/1000 for c in s['reports']],color=['C0','C1']);ax[1].set_ylabel('Profiled kernel duration (µs)')
fig.suptitle('First decode attention body only / shared GPU / one sample each')
for ext in ['png','svg','pdf']:fig.savefig(r/f'memory-counters.{ext}',dpi=160)
