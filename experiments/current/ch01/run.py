"""Current chapter-one exercises: exact arithmetic and archived measurements."""
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

R=Path(__file__).resolve().parent
ROOT=R.parents[2]
source=ROOT/'manuscripts/01-初识 AI Infra.md'
measurement=ROOT/'experiments/ch01/01-04/results/analysis.json'
raw=json.loads(measurement.read_text())
measured=sorted((r for r in raw['groups'] if r['kind']=='short'),key=lambda r:r['batch'])
assert [r['batch'] for r in measured]==[1,4,16,64]
# The exercise explicitly asks for the values annotated on the plots (two decimals).
figure=[dict(batch=r['batch'],throughput=F(f"{r['throughput']:.2f}"),tpot_ms=F(f"{r['tpot_ms']:.2f}")) for r in measured]
ratios=[dict(batch=r['batch'],throughput_ratio=r['throughput']/figure[0]['throughput'],
    tpot_ratio=r['tpot_ms']/figure[0]['tpot_ms'],tpot_increase_percent=(r['tpot_ms']/figure[0]['tpot_ms']-1)*100,
    throughput=r['throughput'],tpot_ms=r['tpot_ms']) for r in figure]
capacity=[]
for precision,weight in [('BF16',F('141.11')),('int8',F('73.73'))]:
    for name,caps in [('one_H100',[F(80)]),('two_H100',[F(80),F(80)]),('A6000_H100',[F(48),F(80)])]:
        budgets=[c-5 for c in caps]
        if name=='two_H100':allocation=[weight/2]*2
        elif name=='A6000_H100':allocation=[min(weight,budgets[0]),max(F(0),weight-budgets[0])]
        else:allocation=[weight]
        capacity.append(dict(precision=precision,layout=name,weight_gb=weight,budgets_gb=budgets,
            allocation_gb=allocation,capacity_feasible=all(w<=b for w,b in zip(allocation,budgets))))
rows=[]
for weight_gb in [70,35]:
    memory=F(weight_gb)/F(3350)*F(10,7)
    unit_compute=F(140)/F(989400)*2
    for batch in [1,16,64]:
        lower=max(memory,unit_compute*batch)
        rows.append(dict(weight_gb=weight_gb,batch=batch,read_ms=memory*1000,compute_ms=unit_compute*batch*1000,
            batch_lower_ms=lower*1000,amortized_ms=lower*1000/batch,ideal_tokens_s=batch/lower,
            ruled_out_10ms=lower>F(1,100),crossing_batch=memory/unit_compute))
assert all(r['ruled_out_10ms'] for r in rows)
assert rows[0]['crossing_batch']==F(494700,4690)
def encode(x):
    if isinstance(x,F):return dict(exact=str(x),value=float(x))
    raise TypeError(type(x).__name__)
result=dict(scope='Current chapter 1; capacity/theory calculations and ratios of existing plot annotations, no new GPU benchmark.',
    capacity=capacity,transfer=dict(gigabytes_per_second=F(400,8),one_gb_seconds=F(1,50)),
    decode=rows,measured_ratios=ratios,
    sources={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [source,measurement,Path(__file__)]})
(R/'results.json').write_text(json.dumps(result,default=encode,indent=2)+'\n')
lines=['# 当前第1章计算表','', '输入采用正文给定的十进制 GB；图1-13/1-14采用标注的两位小数。','',
    '|权重GB|B|整批下界ms|每输出分摊ms|理想token/s|10ms目标被下界排除|','|---|---|---|---|---|---|']
for r in rows:lines.append(f"|{r['weight_gb']}|{r['batch']}|{float(r['batch_lower_ms']):.6f}|{float(r['amortized_ms']):.6f}|{float(r['ideal_tokens_s']):.3f}|是|")
lines+=['','|并发|吞吐token/s|TPOT ms|吞吐/单请求|TPOT增长%|','|---|---|---|---|---|']
for r in ratios:lines.append(f"|{r['batch']}|{float(r['throughput']):.2f}|{float(r['tpot_ms']):.2f}|{float(r['throughput_ratio']):.6f}|{float(r['tpot_increase_percent']):.6f}|")
(R/'tables.md').write_text('\n'.join(lines)+'\n')
print('4 current exercises: numerical portions verified; interpretation and protocol in README.md')
