"""Teaching execution model joining Qwen3 shapes to deployment decisions."""
from pathlib import Path
import json
HERE=Path(__file__).resolve().parent
PARAMS=dict(layers=36,hidden=4096,intermediate=12288,query_heads=32,kv_heads=8,head_dim=128,vocab=151936,element_bytes=2,history=8192,steps=8,hbm_Bps=1e12,matrix_flops_per_s=100e12,serial_s=.0002,local_alpha_s=2e-6,local_link_Bps=50e9,cross_alpha_s=4e-6,cross_link_Bps=25e9)
def ring(p,m,alpha,bw):return 2*(p-1)*alpha+2*(p-1)/p*m/bw
def step(p,history=8192,cross=False):
    h=4096; q=32*128;kv=8*128
    ffn=3*h*12288*2
    attn=(2*h*q+2*h*kv)*2
    kv_position=2*36*kv*2
    head=151936*h*2
    payload=36*(ffn+attn)+kv_position*(history+1)+head
    local=payload/1e12/p
    alpha,bw=(4e-6,25e9) if cross else (2e-6,50e9)
    comm=72*ring(p,8192,alpha,bw)
    return dict(tp=p,history=history,read_write_bytes=payload,local_s=local,communication_s=comm,serial_s=.0002,total_s=local+comm+.0002)
def generate():
    base=[step(p) for p in [1,2,4,8]]
    candidates=[]
    for p in [1,2,4,8]:
        stages=[step(p,8192+j)['total_s'] for j in range(8)]
        service=sum(stages)*1000
        instances=8//p
        ends=[(r//instances+1)*service for r in range(4)]
        # At 20ms the first instance fails; after 40ms it restarts its current request.
        clocks=[0.]*instances;fault_ends=[]
        for r in range(4):
            inst=r%instances
            if inst==0 and clocks[inst]==0:clocks[inst]=60.
            clocks[inst]+=service;fault_ends.append(clocks[inst])
        healthy_cost=8*max(ends)*.001
        fault_cost=8*max(fault_ends)*.001+1
        candidates.append(dict(tp=p,instances=instances,step_times_s=stages,service_ms=service,healthy_completion_ms=ends,fault_completion_ms=fault_ends,healthy_cost=healthy_cost,fault_cost=fault_cost))
    out=dict(kind='teaching_model_not_measurement',parameters=PARAMS,first_steps=base,cross_tp8=step(8,cross=True),candidates=candidates)
    (HERE/'continuity-model.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    return out
if __name__=='__main__':
    d=generate()
    for x in d['first_steps']:print(x['tp'],round(x['total_s']*1e3,4))
    for x in d['candidates']:print(x['tp'],round(x['service_ms'],4),x['healthy_completion_ms'],x['fault_completion_ms'],x['healthy_cost'],x['fault_cost'])
    print('cross8',d['cross_tp8']['total_s']*1e3)
