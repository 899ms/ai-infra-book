"""Exact weight/KV read budgets and physical paged-KV capacity."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[2];source=next((ROOT/'manuscripts').glob('08-*.md'))
Dw=15136811008;k=144*1024;pool=12*2**30;rows=[]
for length in (2048,8192):
 kv=length*k;threshold=(Dw+kv-1)//kv
 assert (threshold-1)*kv<Dw<=threshold*kv
 stored=length+255;blocks=(stored+15)//16;capacity=blocks*16*k;limit=pool//capacity
 assert limit*capacity<=pool<(limit+1)*capacity
 rows.append(dict(context_tokens=length,read_per_output=[dict(batch=b,weight_bytes=Dw//b,kv_bytes=kv,total_bytes=Dw//b+kv,total_GiB=float(F(Dw//b+kv,2**30))) for b in (1,4,16,64)],KV_dominance_minimum_batch=threshold,stored_tokens=stored,allocated_tokens=blocks*16,blocks_per_request=blocks,request_KV_bytes=capacity,maximum_independent_requests=limit,used_bytes_at_limit=limit*capacity,remaining_bytes=pool-limit*capacity,capacity_precedes_read_crossover=limit<threshold))
pages=[]
for size in (2,4,8):
 counts=[(n+size-1)//size for n in (9,13,5,15)];waste=[c*size-n for c,n in zip(counts,(9,13,5,15))]
 assert sum(counts)*size==42+sum(waste)
 pages.append(dict(block_tokens=size,blocks_per_sequence=counts,unused_slots_per_sequence=waste,total_unused_slots=sum(waste),block_table_entries=sum(counts)))
shared=[]
for b in (8,16,32):
 independent=b*528;physical=384+b*144;assert independent-physical==(b-1)*384
 shared.append(dict(requests=b,independent_blocks=independent,shared_physical_blocks=physical,shared_block_table_entries=b*(384+144),independent_KV_MiB=independent*16*k/2**20,shared_KV_MiB=physical*16*k/2**20,independent_fits_12GiB=independent*16*k<=pool,shared_fits_12GiB=physical*16*k<=pool))
provenance={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()}
for name,data in [('8-1',dict(contexts=rows)),('8-3',dict(paging=pages,long_request_capacity=shared,one_private_block_becomes_shared=dict(before_physical_blocks='P+bQ',after_physical_blocks='P+1+b(Q-1)',saved_physical_blocks='b-1',block_table_entries_change=0)))]:
 out=dict(exercise=name,**data,scope='Analytical BF16 KV model, 256 outputs include first prefill output, final emitted token has no KV; no extra allocator metadata in given KV pool',source_sha256=provenance)
 (P/(name+'-results.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
