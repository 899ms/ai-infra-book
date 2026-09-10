"""Independent formula checks against config, source layout and existing adapters."""
from pathlib import Path
from collections import Counter
from fractions import Fraction
import json,sys,hashlib
R=Path(__file__).resolve().parent;ROOT=R.parents[1]
sys.path.insert(0,str(ROOT/'calculations/src'))
from infra_calc.topics import kv_comparison
v4=json.loads((ROOT/'calculations/configs/models/deepseek-v4-flash/config.json').read_text())
v41=json.loads((ROOT/'calculations/configs/models/deepseek-v4.1-flash/config.json').read_text())['text_config']
assert Counter(v4['compress_ratios'][:43])=={0:2,4:21,128:20}
assert v41['num_hidden_layers']==40 and v41['kv_source_layer_ids']==[2,8,14,20]
assert v41['index_source_layer_ids']==[2,8,14,20,24,28,32,36]
assert [v41['compress_ratios'][i] for i in v41['kv_source_layer_ids']]==[2,2,2,1]
assert v41['candidate_topk_blocks']*v41['candidate_block_size']==16384
# Derive bytes, rather than reading the adapter's constants.
a=448+64*2+8;b=512//2+512//16;ix=128//2+128//32;local=512+512//32
assert (a,b,ix,local)==(584,288,68,528)
assert 21*Fraction(a+ix,4)+20*Fraction(a,128)==Fraction(14057,4)
assert Fraction(5,2)*(b+ix)==890
rows=[]
for N in [8192,8193,8194,131072,1048576]:
 result=kv_comparison.calculate(N)['rows']
 x=next(r for r in result if r['model']=='deepseek-v4-flash' and r['layout']!='BF16 reference')
 y=next(r for r in result if r['model']=='deepseek-v4.1-flash')
 v4g=21*(N//4)*(a+ix)+20*(N//128)*a
 v41g=(3*(N//2)+N)*(b+ix)
 v4read=43*128*a+21*min(N//4,512)*a+20*(N//128)*a+21*(N//4)*ix
 v41read=40*128*local+38*512*b+(3*(N//2)+N+4*min(N,16384))*ix
 assert x['global_history_bytes']==v4g and y['global_history_bytes']==v41g
 assert x['decode_selected_history_read_bytes']==v4read and y['decode_selected_history_read_bytes']==v41read
 rows.append(dict(length=N,v4_global=v4g,v41_global=v41g,v4_read=v4read,v41_read=v41read))
report=dict(passed=True,checks=['Layer counts from config','Source layers and index modes','Cache formats including scales and padding','Global growth and odd/even boundaries','Logical main plus index reads at five lengths'],rows=rows,
limitations=['Logical reads, not measured HBM','No quality experiment','Encoder/decoder replay verified from report section 3.2.2, not inferred from these numbers'])
(R/'number-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
