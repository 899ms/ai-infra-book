"""Exact slot/issue-rate limits and fluid-queue feedback boundaries."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('07-*.md'))
ceil=lambda x:(x.numerator+x.denominator-1)//x.denominator
bw=50*10**9;occupancy=F(4,10**6)
slots=[]
for payload in (256,4096):
 n=ceil(bw*occupancy/payload);assert (n-1)*payload/occupancy<bw<=n*payload/occupancy
 slots.append(dict(payload_bytes=payload,minimum_slots=n,rate_with_128_slots_GBps=float(min(F(bw),128*payload/occupancy)/10**9)))
issue=[]
for ns in (F(186,10),F(62,10)):
 interval=ns/10**9;minimum=ceil(bw*interval)
 assert F(minimum-1)/interval<bw<=F(minimum)/interval
 issue.append(dict(interval_ns=float(ns),minimum_integer_payload_bytes=minimum,required_slots_at_that_payload=ceil(bw*occupancy/minimum),max_256B_GBps=float(min(F(bw),256/interval)/10**9)))
queue=[]
for capacity in (512*1024,1024**2):
 q0=256*1024;feedback=F(capacity-q0,50*10**9)
 assert q0+50*10**9*feedback==capacity
 rates=[]
 for arrival in (50,45,40):
  drain=(50-arrival)*10**9;duration=F(capacity,drain) if drain else None
  if duration is not None:assert capacity-drain*duration==0
  rates.append(dict(arrival_GBps=arrival,net_drain_GBps=50-arrival,empty_after_feedback_us=float(duration*10**6) if duration is not None else None,backlog_if_no_drain=capacity if not drain else None))
 queue.append(dict(capacity_bytes=capacity,initial_backlog_bytes=q0,max_feedback_us=float(feedback*10**6),post_feedback=rates))
for exercise,fields in [('7-8',dict(slots=slots,issue=issue,slot_occupancy_us=4)),('7-11',dict(queue=queue))]:
 out=dict(exercise=exercise,**fields,scope='Exact declared payload and fluid queue models; no new device benchmark',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
 (P/(exercise+'-results.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(slots=slots,issue=issue,queue=queue),indent=2))
