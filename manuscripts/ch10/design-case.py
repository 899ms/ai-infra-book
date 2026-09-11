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
lines=['# 贯穿设计题：32 卡与 48 卡 RTX 4090\n','此题以既有 Qwen3-8B 矩阵工作为来源，硬件与效率输入都来自归档资料；它给出条件式系统设计结果，不是新执行的 GPU 基准。\n','## 条件\n',
 '- 100B 有效 token；384 条 8192-token 序列组成一次训练迭代；最后不足满批时保守地仍按完整步时安排。',
 '- RTX 4090 dense BF16 峰值 165.2 TFLOP/s（hardware.json）；单卡计算效率 40%，取 Llama 3 报告的 38%—43% BF16 MFU（references/text/llama3.txt 第 544—547、580 行）。',
 '- 四台或六台八卡主机；全组 ZeRO-3；TP=PP=1；每卡单序列微批，分别累积 12／8 次。',
 '- 每卡可用显存 22 GiB，全部激活、完整模块参数、工作区的同时存活附加量上限 10 GiB。',
 '- RTX 4090 无 NVLink、不支持卡间 P2P，每卡收发都经自己的 PCIe 4.0 x16（每方向 32 GB/s）；每台主机八张 200 Gb/s 网卡（references/text/h100-vs-4090.txt 第 119 行）。',
 '- 每个微批次三次集合通信（前向、反向各一次 BF16 权重全收集，一次 BF16 梯度归约后分散），每次每卡 (d−1)/d×2N bytes；暴露的通信只计一步中第一次全收集与最后一次归约后分散（MegaScale，references/text/megascale.txt 第 238—247 行），二者作用于词嵌入。',
 '- 平均输入等待 0.5 s；四个数据准备进程各准备两条序列/s。',
 '- 每 1800 s 有用训练同步保存一次；检查点 14N bytes，写入 7 GB/s（DGX SuperPOD 参考架构表 6 的 Good 档单 SU 合计写入）；每卡 MTBF 取 Meta 1024 卡作业 7.9 小时的 1024 倍，任一卡故障中断作业，恢复 120 s。',
 '- 保存及恢复使用正文一阶模型；5 天预留用于启动、评估与计划性停顿。\n','## 复算\n',
 '单卡计算时间 = 每卡计算量 /（峰值 × 效率）；每步训练时间 = 单卡计算 + 暴露通信 + 输入等待。保存恢复附加比例为 c/1800 + λ×900 + λ×120。总天数为 5 + 训练迭代次数×每步训练时间×(1+附加比例)/86400。\n',
 '| 卡数 | 峰值预算/GiB | 单卡计算/s | 每步链路/s | 暴露通信/s | 每步训练时间/s | 附加比例 | 完成/天 | 每步上限/s | 最低单卡计算效率 |','|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in rows:lines.append(f"| {r['devices']} | {r['peak_budget_gib']:.3f} | {r['local_seconds']:.3f} | {r['link_seconds_pcie']:.3f} | {r['exposed_communication_seconds']:.4f} | {r['base_step_seconds']:.3f} | {r['total_loss']:.5%} | {r['finish_days']:.3f} | {r['max_base_step_seconds']:.3f} | {r['minimum_local_efficiency']:.3%} |")
lines+=['\n数值源和完整输入见 [design-case.json](design-case.json)，执行 `python3 manuscripts/ch10/design-case.py` 可复算。正文保留足以判断 30 天期限的精度。']
(HERE/'design-case.md').write_text('\n'.join(lines)+'\n')
