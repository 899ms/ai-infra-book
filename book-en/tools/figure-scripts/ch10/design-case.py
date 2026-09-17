#!/usr/bin/env python3
"""Reproduce the chapter-ten running design exercise on RTX 4090 hosts.

Inputs with a source: RTX 4090 BF16 dense peak and memory from calculations/configs/hardware.json;
PCIe 4.0 x16 (32 GB/s per direction), no NVLink and no GPU peer-to-peer from the archived RTX 4090
spec page and references/text/h100-vs-4090.txt (lines 119, 147, 183); eight 200 Gb/s NICs per 8-GPU
host from references/text/h100-vs-4090.txt line 119; 40% efficiency from the Llama 3 BF16 MFU range
(references/text/llama3.txt lines 544-547, 580); the unhidden first all-gather and last reduce-scatter
from references/text/megascale.txt lines 238-247; storage write 7 GB/s from the DGX SuperPOD reference
architecture Table 6 ("Good", single SU aggregate write); job interruption rate from the Meta cluster
paper (1024-GPU jobs: MTTF 7.9 h, MTTF proportional to 1/N_gpus).
"""
from pathlib import Path
from fractions import Fraction
import json, math
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
source=json.loads((ROOT/'calculations/results/training-deadline-book.json').read_text())
state=json.loads((ROOT/'calculations/results/training-state-book.json').read_text())
F=source['summary']['task_training_matrix_flops']
N=8190735360
assert state['summary']['parameters']==N
EMBED=next(t['parameters'] for t in state['training_state_tensors'] if t['name']=='model.embed_tokens.weight')
PEAK=165200000000000;EFF=Fraction(2,5)
PCIE=32*10**9;NIC=25*10**9;NICS_PER_HOST=8
CKPT_BW=7*10**9
JOB_MTTF_1024=Fraction(79,10)*3600
DEVICE_MTBF=1024*JOB_MTTF_1024
INPUT_WAIT=Fraction(1,2)
assumptions=dict(kind='design_from_cited_device_inputs',parameters=N,embedding_parameters=EMBED,effective_tokens=10**11,sequence_tokens=8192,sequences_per_update=384,deadline_days=30,planned_nontraining_days=5,
 device='rtx4090',device_peak_flops=PEAK,local_efficiency=float(EFF),local_efficiency_source='references/text/llama3.txt lines 544-547, 580 (38-43% BF16 MFU)',
 net_device_gib=22,additional_live_gib=10,
 pcie_bytes_per_second_per_direction=PCIE,nic_bytes_per_second=NIC,nics_per_host=NICS_PER_HOST,
 link_source='RTX 4090 spec (PCIe Gen 4, NVLink: No); references/text/h100-vs-4090.txt lines 119, 147, 183',
 collectives_per_microbatch=3,collective_payload='BF16 weights all-gather (forward, backward) and BF16 gradient reduce-scatter',
 exposed_rule='first all-gather and last reduce-scatter of the step (embedding unit); references/text/megascale.txt lines 238-247',
 input_wait_seconds=float(INPUT_WAIT),checkpoint_bytes=14*N,checkpoint_bandwidth_bytes_per_second=CKPT_BW,
 checkpoint_bandwidth_source='references/text/dgx-superpod-h100-ra.txt Table 6, Good, single SU aggregate write',
 checkpoint_useful_interval_seconds=1800,device_mtbf_seconds=int(DEVICE_MTBF),device_mtbf_source='references/text/meta-cluster-reliability.txt lines 736-747 (1024-GPU MTTF 7.9 h, MTTF ~ 1/N)',
 recovery_seconds=120,input_workers=4,sequences_per_worker_second=2)
b=384*8192;steps=math.ceil(Fraction(10**11,b));c=Fraction(14*N,CKPT_BW)
rows=[]
for p in (32,48):
 m=384//p;share=Fraction(p-1,p)
 local=Fraction(F,10**11)*b/(p*PEAK*EFF)
 per_collective=share*2*N
 link_bytes=m*3*per_collective
 link=link_bytes/PCIE
 single_nic=link_bytes/NIC
 exposed=2*share*2*EMBED/PCIE
 base=local+exposed+INPUT_WAIT;lam=Fraction(p)/DEVICE_MTBF
 loss=c/1800+lam*(900+120)
 budget=Fraction(25*86400,steps)/(1+loss)
 rows.append(dict(devices=p,hosts=p//8,microbatches_per_device=m,persistent_gib=16*N/p/2**30,peak_budget_gib=16*N/p/2**30+10,local_seconds=float(local),
  local_seconds_exact=str(local),collective_bytes_per_device=float(per_collective),link_bytes_per_step_per_device=float(link_bytes),
  link_seconds_pcie=float(link),link_seconds_single_nic_per_host=float(single_nic),link_seconds_per_microbatch=float(link/m),local_seconds_per_microbatch=float(local/m),
  exposed_communication_seconds=float(exposed),exposed_communication_exact=str(exposed),overhead_seconds_exact=str(exposed+INPUT_WAIT),
  base_step_seconds=float(base),base_step_exact=str(base),no_overlap_step_seconds=float(local+link+INPUT_WAIT),single_nic_no_overlap_step_seconds=float(local+single_nic+INPUT_WAIT),
  save_loss=float(c/1800),redo_loss=float(lam*900),recovery_loss=float(lam*120),total_loss=float(loss),
  base_training_days=float(steps*base/86400),finish_days=float(5+steps*base*(1+loss)/86400),
  max_base_step_seconds=float(budget),max_communication_seconds=float(budget-local-INPUT_WAIT),
  minimum_local_efficiency=float(local*EFF/(budget-exposed-INPUT_WAIT)),
  efficiency_30_step_seconds=float(local*Fraction(4,3)+exposed+INPUT_WAIT),half_pcie_step_seconds=float(local+2*exposed+INPUT_WAIT),half_pcie_link_per_microbatch=float(2*link/m)))
out=dict(assumptions=assumptions,source='calculations/results/training-deadline-book.json',task_matrix_flops=F,tokens_per_update=b,updates=steps,raw_step_budget_seconds=25*86400/steps,checkpoint_seconds=float(c),candidates=rows)
(HERE/'design-case.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
lines=["# Running Design Problem: 32-Card and 48-Card RTX 4090\n","This problem draws on existing Qwen3-8B matrix work; hardware and efficiency inputs come from archived materials. It gives conditional system design results, not newly run GPU benchmarks.\n","## Conditions\n",
 "- 100B effective tokens; 384 sequences of 8192 tokens form one training iteration; the final under-full batch is conservatively still scheduled at full step time.",
 "- RTX 4090 dense BF16 peak 165.2 TFLOP/s (hardware.json); per-card compute efficiency 40%, taking the 38%-43% BF16 MFU reported by Llama 3 (references/text/llama3.txt lines 544-547, 580).",
 "- Four or six eight-card hosts; full-group ZeRO-3; TP=PP=1; single-sequence micro-batch per card, accumulated 12/8 times respectively.",
 "- 22 GiB usable memory per card; concurrent overhead cap of 10 GiB for all activations, full module parameters, and workspace.",
 "- RTX 4090 has no NVLink and no inter-card P2P support; each card's send/receive goes through its own PCIe 4.0 x16 (32 GB/s per direction); each host has eight 200 Gb/s NICs (references/text/h100-vs-4090.txt line 119).",
 "- Each micro-batch has three collective communications (one BF16 weight all-gather each for forward and backward, one BF16 gradient reduce-scatter), each per card (d−1)/d×2N bytes; exposed communication only counts the first all-gather and last reduce-scatter in a step (MegaScale, references/text/megascale.txt lines 238-247), both applied to the word embedding.",
 "- Average input wait 0.5 s; four data preparation processes each prepare two sequences/s.",
 "- Every 1800 s of useful training, a synchronous save occurs; checkpoint 14N bytes, written at 7 GB/s (Good tier single-SU aggregate write from DGX SuperPOD reference architecture Table 6); per-card MTBF taken as 1024x the 7.9 hours of Meta's 1024-card job, any card failure interrupts the job, recovery 120 s.",
 "- Save and recovery use the first-order model from the main text; 5 days reserved for startup, evaluation, and planned pauses.\n","## Recalculation\n",
 "Per-card compute time = per-card FLOPs / (peak × efficiency); per-step training time = per-card compute + exposed communication + input wait. Save/recovery overhead ratio = c/1800 + λ×900 + λ×120. Total days = 5 + training iterations × per-step training time × (1+overhead ratio)/86400.\n",
 "| Card count | Peak budget/GiB | Per-card compute/s | Per-step link/s | Exposed comm/s | Per-step training time/s | Overhead ratio | Completion/days | Per-step ceiling/s | Min per-card compute efficiency |",'|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in rows:lines.append(f"| {r['devices']} | {r['peak_budget_gib']:.3f} | {r['local_seconds']:.3f} | {r['link_seconds_pcie']:.3f} | {r['exposed_communication_seconds']:.4f} | {r['base_step_seconds']:.3f} | {r['total_loss']:.5%} | {r['finish_days']:.3f} | {r['max_base_step_seconds']:.3f} | {r['minimum_local_efficiency']:.3%} |")
lines+=["\nSee [design-case.json](design-case.json) for value sources and full inputs; run `python3 manuscripts/ch10/design-case.py` to recompute. Main text retains precision sufficient to judge the 30-day deadline."]
(HERE/'design-case.md').write_text('\n'.join(lines)+'\n')
