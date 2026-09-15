"""Executable synthetic route packing, CP4 slicing and corruption detection."""
from pathlib import Path
import hashlib,json
import numpy as np
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
L=8192;layers=48;k=8;experts=256
# Logical route identity is sample, original position, layer, ordered top-k slot.
s=np.arange(2,dtype=np.int32)[:,None,None,None]
t=np.arange(L,dtype=np.int32)[None,:,None,None]
l=np.arange(layers,dtype=np.int32)[None,None,:,None]
j=np.arange(k,dtype=np.int32)[None,None,None,:]
routes=(s*101+t*7+l*13+j*17)%experts
assert routes.shape==(2,L,layers,k)
assert np.all(np.diff(np.sort(routes,axis=-1),axis=-1)>0)
# Pack B before A to ensure identity isn't silently inferred from pack order.
order=[1,0];packed=np.concatenate([routes[i] for i in order],axis=0)
keys=np.array([(sample,pos) for sample in order for pos in range(L)],dtype=np.int32)
shards=[packed[i*4096:(i+1)*4096].copy() for i in range(4)]
keyshards=[keys[i*4096:(i+1)*4096].copy() for i in range(4)]
restored=np.empty_like(routes)
for chunk,kk in zip(shards,keyshards):restored[kk[:,0],kk[:,1]]=chunk
assert np.array_equal(routes,restored)
# Corruption preserves shape, ID range and top-k uniqueness; route for p+1 attaches to p.
bad=shards[0].copy();bad[17]=shards[0][18]
assert bad.shape==shards[0].shape and bad.min()>=0 and bad.max()<experts
assert np.all(np.diff(np.sort(bad,axis=-1),axis=-1)>0)
expected=routes[keyshards[0][:,0],keyshards[0][:,1]]
where=np.argwhere(np.any(bad!=expected,axis=-1))
assert len(where)==48 and set(where[:,0])=={17}
correct=expected[17,3];wrong=bad[17,3]
assert not np.array_equal(correct,wrong)
# Toy expert f_e(x)=(e+1)*x, x=1, equal weights: exposes dispatch effect only.
y_correct=float(np.mean(correct+1));y_wrong=float(np.mean(wrong+1));assert y_correct!=y_wrong
source=next((ROOT/'manuscripts').glob('10-*.md'))
out=dict(exercise='10-8',single_sequence_entries=L*layers*k,uint16_single_bytes=L*layers*k*2,int32_single_bytes=L*layers*k*4,two_sequence_bytes_uint16=2*L*layers*k*2,two_sequence_bytes_int32=2*L*layers*k*4,pack_order=['B','A'],shards=[dict(rank=i,packed_start=i*4096,packed_stop=(i+1)*4096,sample='B' if i<2 else 'A',original_start=(i%2)*4096,original_stop=(i%2+1)*4096,uint16_bytes=chunk.size*2,int32_bytes=chunk.nbytes,route_sha256=hashlib.sha256(chunk.astype('<i4').tobytes()).hexdigest(),identity_and_route_sha256=hashlib.sha256(keyshards[i].astype('<i4').tobytes()+chunk.astype('<i4').tobytes()).hexdigest()) for i,chunk in enumerate(shards)],roundtrip_equal=True,misalignment=dict(rank=0,sample='B',expected_original_position=17,used_original_position=18,affected_layers=len(where),example_layer=3,correct_experts=correct.tolist(),wrong_experts=wrong.tolist(),toy_correct_output=y_correct,toy_wrong_output=y_wrong,shape_range_uniqueness_checks_pass=True,identity_route_check_rejected=True),scope='Synthetic routes and toy expert output. No NeMo/R3 training replay, learned scores, logprob equivalence or multi-GPU execution claim.',source_sha256={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest()})
(P/'10-8-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
