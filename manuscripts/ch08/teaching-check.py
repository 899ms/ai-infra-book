#!/usr/bin/env python3
"""Independently recompute the chapter's teaching decisions using exact arithmetic."""
from fractions import Fraction as F
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
KiB=2**10;MiB=2**20;GiB=2**30
k=2*36*8*128*2

def pages(tokens):return ((tokens+15)//16)*16*k
short=pages(2048+255);long=pages(8192+255);prefix=6144*k;private=pages(8192-6144+255)
assert (short//MiB,long//MiB,prefix//MiB,private//MiB)==(324,1188,864,324)
assert (12*GiB//short,12*GiB//long,(12*GiB-prefix)//private)==(37,10,35)
shared=prefix+16*private
assert shared==6048*MiB and 16*long==19008*MiB
compressed=16*long*F(34,64)
assert compressed==10098*MiB
expected=lambda m:sum(F(3,4)**j for j in range(m+1))
rows=[]
for name,memory,pre,steps,step,rate in [
 ('A',16*long,F(6,10),255,F(1,100),1),
 ('B',shared,F(4,10),255,F(1,100),1),
 ('C',compressed,F(6,10),255,F(12,1000),1),
 ('D',shared+2*GiB,F(6,10),85,F(15,1000),F(12,10)),
 ('E',shared+GiB,F(5,10),51,F(25,1000),F(11,10))]:
 t=pre+steps*step;cost=t*rate/16
 rows.append({'name':name,'memory_gib':float(memory/GiB),'time_s':float(t),'cost_per_qualified_result':float(cost) if memory<=12*GiB and t<=3 else None,'fits_12gib':memory<=12*GiB,'within_3s':t<=3})
assert [r['name'] for r in rows[:4] if r['fits_12gib'] and r['within_3s']]==['B','D']
assert F(1875,1000)*F(12,10)/16<F(295,100)/16
assert shared<=6*GiB<shared+2*GiB
assert F(4,10)+15*F(1,100)<F(6,10)+5*F(15,1000)
assert F(5,10)+3*F(25,1000)==F(575,1000)
assert F(4,10)+15*F(1,100)<F(575,1000)
assert 36==F(1,2)*(100-20)-4 and 24==F(1,2)*(80-24)-4
assert (3*24+4)/F(100-20)==F(95,100)
copy_gib=F(9*288,1024)
assert copy_gib/24*255>26 and copy_gib/384*255<2
out={'kind':'explicit teaching assumptions; no hardware measurements','capacity':{'short_mib':short//MiB,'long_mib':long//MiB,'shared_16_mib':shared//MiB,'independent_16_mib':16*long//MiB,'q8_16_mib':float(compressed/MiB)},'design_candidates':rows,'exercise_4_A_probability_tie':.95,'exercise_5_bandwidth_for_1s_gib_s':float(copy_gib*255),'exercise_7':[{'block':m,'expected_output':float(expected(m)),'linear_ms_per_token':float((F(1,2)+F(1,5)*m)/expected(m)),'padded_ms_per_token':float((F(1,2)+F(1,5)*4*((m+3)//4))/expected(m))} for m in [1,2,4,5,8]],'passed':True}
(HERE/'teaching-validation.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
