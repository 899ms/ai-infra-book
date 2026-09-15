"""Incast with two receiving NICs and unchanged 50 GB/s sender links."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('07-*.md'))
refpath=ROOT/'calculations/results/incast-feedback-book.json';ref=json.loads(refpath.read_text());c=ref['scenario'];buffer=c['free_buffer_bytes'];sender=c['sender_bytes_per_second'];egress=2*c['egress_bytes_per_second'];mtu=c['mtu_bytes']
rows=[]
for cable in (30,100):
 # Per-link serializer remains 50GB/s; receiver aggregate becomes 100GB/s.
 feedback=F(2*cable*c['declared_propagation_ns_per_m'],10**9)+F(mtu,sender)
 if cable==30:assert feedback*10**9==F(ref['feedback_distances'][0]['feedback_ns_exact'])
 for n in (8,16,64):
  arrival=(n-1)*sender;excess=arrival-egress;allowed=F(buffer,excess);headroom=excess*feedback
  assert excess*allowed==buffer
  rows.append(dict(N=n,senders=n-1,cable_m=cable,arrival_GBps=arrival/1e9,excess_GBps=excess/1e9,allowed_feedback_us=float(allowed*10**6),one_hop_feedback_us=float(feedback*10**6),headroom_bytes=int(headroom),headroom_MiB=float(headroom/2**20),fits_1MiB=headroom<=buffer))
rtt=F(5,10**6);valid=[n for n in range(2,100) if max(0,(n-1)*sender-egress)*rtt<=buffer];limit=max(valid)
assert max(0,limit*sender-egress)*rtt>buffer
out=dict(exercise='7-12',rows=rows,max_N_5us=limit,sender_count_at_max=limit-1,headroom_at_max_bytes=int(((limit-1)*sender-egress)*rtt),headroom_next_N_bytes=int((limit*sender-egress)*rtt),scope='Fluid aggregate receive model; two independent 50GB/s receiving links assumed balanced, individual feedback serializer remains 50GB/s',source_sha256={str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in (source,refpath)})
(P/'7-12-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
