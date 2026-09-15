"""Executable counterexamples for nonlinear placement and BF16 boundary removal."""
from pathlib import Path
import hashlib,json,math,struct
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def silu(x):return x/(1+math.exp(-x))
def bf16(x):
 # Finite positive examples, IEEE round-to-nearest ties-to-even from FP32.
 bits=struct.unpack('<I',struct.pack('<f',x))[0];rounded=(bits+0x7fff+((bits>>16)&1))&0xffff0000
 return struct.unpack('<f',struct.pack('<I',rounded))[0]
partial=[1.,-1.];running=0;premature_outputs=[]
for x in partial:
 running+=x;premature_outputs.append(silu(running))
assert premature_outputs[-1]==0
correct=silu(sum(partial));per_partial=sum(silu(x) for x in partial);overwrite=0
for x in partial:overwrite=silu(overwrite+x)
assert correct==0 and abs(per_partial-correct)>.4 and abs(overwrite-correct)>.1
# Both operands and the FP32 sum are exact dyadic values.
a=[1.,1/256];w=[1.,1.];acc=sum(x*y for x,y in zip(a,w));assert acc==1+1/256 and bf16(acc)==1
with_round=silu(bf16(acc));without=silu(acc);assert with_round!=without and bf16(with_round)!=bf16(without)
M=K=4096;N=1536;BN=128;columns=N//BN;input_bytes=2*M*K;fp8_bytes=M*K
separate=input_bytes+fp8_bytes+columns*fp8_bytes;fused=input_bytes+columns*input_bytes
common=(M//128)*K*N+2*M*N
assert (separate+common)//2**20==444 and (fused+common)//2**20==620
# Ones and zeros map exactly at scale1/448, for both materialized and repeated quantization.
row=[1.,0.]*128;scale=max(abs(v) for v in row)/448
quantized=[v/scale for v in row];assert set(quantized)=={0.,448.}
assert all([v/scale for v in row]==quantized for _ in range(columns))
out=dict(exercise='5-4',nonlinear=dict(partial_sums=partial,correct=correct,premature_stores_without_acc_mutation=premature_outputs,silu_each_partial_then_sum=per_partial,overwrite_acc_inside_loop=overwrite),rounding=dict(A=a,W=w,fp32_sum=acc,bf16_sum=bf16(acc),silu_after_bf16=with_round,silu_without_bf16=without,final_bf16_with=bf16(with_round),final_bf16_without=bf16(without)),quantization=dict(shape=[M,K,N],output_column_blocks=columns,quantized_elements_materialized=M*K,quantized_elements_repeated=columns*M*K,materialized_input_path_bytes=separate,repeated_input_path_bytes=fused,common_weight_output_bytes=common,materialized_total_bytes=separate+common,repeated_total_bytes=fused+common,example_scale=scale,example_quantized_values=sorted(set(quantized)),scope='Same precomputed full-row scale and exact representable0/448 values; no implementation of general FP8 conversion or proof for every input'),source_sha256={'manuscripts/05-算子与运行时.md':hashlib.sha256((ROOT/'manuscripts/05-算子与运行时.md').read_bytes()).hexdigest()})
(R/'5-4-results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
