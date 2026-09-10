# 8-3：两个adapter竞争一个或两个GPU槽位

相同A/B控制adapter、相同输入和KV容量下，一个GPU adapter槽时，原生调度器最多同时运行一种adapter及两条请求；两个槽时，两种adapter及四条请求可同时运行。24条正式请求全部完成，两种配置按ID对应的12对输出逐token相同。

| 原生调度观察 | 1个GPU槽 | 2个GPU槽 |
|---|---:|---:|
| 正式请求 | 12 | 12 |
| 同时RUNNING的adapter身份峰值 | 1 | 2 |
| RUNNING请求峰值 | 2 | 4 |
| WAITING请求峰值 | 2 | 0 |
| 观察到PREEMPTED状态的请求 | 0 | 0 |
| 请求拥有唯一KV块峰值 | 105 | 210 |
| 最终空闲块／池总块 | 454/455 | 454/455 |

一个槽时，两个同身份请求可以共用已缓存前缀并同时运行，另一个身份等待；两个槽允许两种身份同时进入运行状态。跨全部1214个快照，任何被多个请求同时拥有的块都只对应同一个adapter身份；块引用计数和空闲／唯一拥有／保留守恒全部通过。RUNNING状态可能包含prefill，不应直接当成同时decode数。无PREEMPTED状态观察也不冒称逐内核故障跟踪。

## 逐身份完成记录

每配置、每身份六条正式请求，下面是原始样本中位／最大值，单位秒，计时从应用提交到完整64token返回：

| 身份 | 1槽中位／最大 | 2槽中位／最大 |
|---|---:|---:|
| A | 1.797／4.582 | 1.788／1.824 |
| B | 3.637／6.386 | 1.790／1.824 |

固定先1槽再2槽，模型与Triton形状有首次运行开销，观察器同步写日志；三轮不是三个独立引擎重复，不把六条请求当成生产p95/p99分布。A/B到达顺序固定，也不将本组身份时间差归因于adapter优劣。全部逐请求start/events/end和首次RUNNING观察等待都保留，后者包含提交、IPC及观察边界，不冒充纯调度队列耗时。

## 固定条件与范围

复用 [非零未训练LoRA控制](../adapter-isolation/README.md) 的两份rank8、36层q_proj adapter，名称/ID固定互异。1536token同一合成输入，每引擎先A/B各1token加载预热，再进行三轮A/B/A/B四请求并发，每条强制64输出；轮次之间等待全部完成。总28模型请求，24正式加4预热；没有重跑此前串行实验。

Qwen3-8B BF16固定快照、RTX PRO6000Blackwell、vLLM0.23/Torch2.11cu130；KV1GiB、maxseq4、maxlen2048、chunk512、APC开启、eager、max_cpu_loras2，只有max_loras从1改2。输入及其余引擎配置精确一致。观察原Scheduler状态，不模拟队列或人为添加等待。实际四条请求在每轮都同时在途，按原始起止区间交叉验证。

每轮结束通过原worker LoRA manager记录GPU槽数组及CPU注册ID；results中的slots.jsonl保留实际槽位。数据文件在slots1/slots2及对应*-run中。两个guard均exit0（25.065/15.808s）、无残留或资源终止，未停止其他服务。无失败批次需清理。

## 独立复现

```sh
python reproduce.py --model /path/to/frozen/Qwen3-8B/snapshot
python analyze.py
python verify.py
```

使用同一vLLM环境的独立副本，先移走封存slots1/slots2及对应*-run和analysis.json；输出已存在则拒绝覆盖。全部adapter文件随包保存，不依赖相邻实验、PEFT或calculations。verify.py针对既有封存，重现实验的新时间戳不应要求匹配旧manifest。

本轮验证固定两个控制身份的槽位竞争与实际等待，未验证trained adapter质量、生产租户分布、抢占/取消公平性或稳定延迟收益；全书最终跨session审计仍待。
