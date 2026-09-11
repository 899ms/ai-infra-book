# 贯穿算例：HGX H100 上的 Qwen3-32B 张量并行与会话完成时间

本页保存第六章正文的模型约定与完整精度入口。正文 6.1 用 Qwen3-235B-A22B 说明为什么一台 HGX H100 要整台服务一个实例；6.2.2 起用稠密的 Qwen3-32B 比较张量并行的卡数，6.4 加入归约，6.5 改变物理路径，6.7 对同一模型排出会话完成顺序、GPU·s 与能耗。

[计算脚本](continuity_model.py) · [完整结果](continuity-model.json) · [正文](../06-超节点.md)

## 硬件与模型输入

硬件为一台 HGX H100：8 张 H100 SXM，每张 80 GB HBM，峰值带宽 3350 GB/s，BF16 稠密矩阵峰值 989.4 TFLOP/s（均取自 `calculations/configs/hardware.json` 的 `h100-sxm`）。NVLink 4 经 NVSwitch 互联，每卡每方向 450 GB/s（H100 架构白皮书：18 条链路，每条每方向 25 GB/s）。每卡一张 ConnectX-7 400 Gb/s 网卡。

集合通信每轮固定开销取 MSCCL++（ASPLOS 2026）表 1 在同一平台（每节点 8 张 H100、NVLink 4、每卡一张 CX-7）上测得的 NVLink 延迟 822 ns；两台 HGX H100 组成的 16 rank AllReduce 直接读取实验 7-3 的 nccl-tests 公开记录（`experiments/ch07/07-03/rows.csv`，`hgx2`，out-of-place，取不小于消息大小的最小一档，10 KiB 对应 16 KiB 的 32.74 μs）。

Qwen3-32B：64 层、隐藏维 5120、FFN 中间维 25600、64 查询头、8 KV 头、头维 128、词表 151936，BF16 权重与 KV（`calculations/configs/models/qwen3-32b/config.json`）。每卡为激活与其余工作区预留 2 GiB。

## 从访问字节得到时间

每层 FFN 三矩阵共 750 MiB，attention Q/K/V/O 投影共 180 MiB，合计 930 MiB。每 token 的 KV 为 256 KiB。

```
V(s) = 64 × 930 MiB + 256 KiB × (s+1) + 151936 × 5120 × 2 bytes
T(p,s) = max(V_card/3350 GB/s, FLOPs_card/989.4 TFLOP/s) + 128 × T_AR(p)
V_card = weights/p + KV/min(p, 8)
T_AR(p) = 2(p−1)·0.822 μs + 2(p−1)/p × 10240 B / 450 GB/s
```

`s=131064` 时 `V=98,324,971,520 bytes`，TP1 读完约 29.35 ms；同一步矩阵运算约 0.34 TFLOPs，约 0.34 ms，所以各阶段都受内存带宽限制。TP 同比例切分权重与 KV，p≤8 时仍受内存带宽限制；TP16 时 KV 头不够分，每卡读取的 KV 与 TP8 相同。归一化、逐元素运算和采样只读写几个隐藏向量，不计入。

## 容量

每卡需求 = (常驻权重 − 归一化参数)/p + 归一化参数 + 实例内全部排队会话的 KV/min(p,8) + 2 GiB。128K（131,072 个位置）会话：TP1 每卡 102.03 GB，超过 80 GB；TP2、TP4、TP8 实例每卡分别能放 2、7、16 个会话。32K 时分别能放 1、10、28、64 个。

## 从一步到八步，从一会话到四会话

四个会话各有 131,064 个历史 token 和一个尚未写入 KV 的 token。八次 decode 的步前历史依次为 131,064—131,071，步末写满 131,072 个位置。每步单独计算 V(s)，求和得到会话服务时间：TP2 119.11 ms、TP4 63.79 ms、TP8 41.18 ms。

四个会话同时到达，实例一次处理一个完整八步续写，按实例编号轮转分配。八卡全部保留并计费到整组结束，成本以 H100 GPU·s 计；能耗按 DGX H100 系统功率上限 10.2 kW 计。期限 130 ms，至少 75% 按时。

故障在 20 ms 发生于卡 0；该卡所属实例停顿 40 ms，在 60 ms 恢复并从当前会话的八步起点重做，之后依次处理排队会话。其他实例独立执行。

## 其他块

- `dense_moe`：Qwen3-32B、Qwen3-30B-A3B、Qwen3.6-35B-A3B 的常驻权重、每请求状态、batch 1／64 的每步读取与运算，以及 1／2 张 H100 能放下的 32K／128K 请求数，读取 `calculations/results/` 中对应的 forward／qwen36 结果。
- `two_servers`：TP16 横跨两台 HGX H100（实测 AllReduce）与假设同一 NVLink 域内（每轮 0.822 μs）的单步时间。
- `rack`：按 DGX H100 10.2 kW 计的服务器台数上限。
- `memory_pool`：四个 80 GB 节点的借用、CX-7 路径 50 GB/s、往返 7.52 μs 时的在途窗口与重复读取比较。

`figure-data.json` 的 `continuous_execution` 与 `deadline_curves` 由本脚本生成。
