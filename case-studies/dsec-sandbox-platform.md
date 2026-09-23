# DSec：Agent RL 沙箱平台的资源与状态

DeepSeek 的 DSec（DeepSeek Elastic Compute）为 RL rollout、评测和环境构建提供沙箱，是第 11 章贯穿设计题在生产规模上的对应物。第 11 章正文只保留推理链上必需的几个数；本文记录全部引用数字、出处小节和本书所做的换算。[^src]

## 平台规模与负载特征

| 项目 | 数值 | 出处 |
|---|---|---|
| 一个集群单元 | 约 160 个 CPU 节点、30K 核、约 250 TB DRAM | §2.4 |
| 每日沙箱数 | 约 300 万 | §2.4 |
| 峰值并发 | 约 38 万 | §2.4 |
| 峰值创建速率 | 超过 5,000 个/s | §2.4 |
| 单个作业的沙箱数 | 最多 32K；容器任务 p50 352、p99 4,044；microVM 任务 p50 2,528、p99 16,388 | §4.1、图 2 |
| CPU 使用率 | 约 90% 的容器与 microVM 平均用量 ≤ 申请量的 5% | §4.3、图 5 |
| 单节点密度 | 稳定运行过 ≥3,200 个容器或 ≥800 个 microVM；某日观测峰值 1,048 个容器、524 个 microVM | §4.3、图 6 |
| 存活时间 | 中位数：容器 17.4 min、microVM 15.5 min；p99 均超过 3 h | §4.3、图 7 |
| 一周内活跃的环境制品 | 容器：11,266 个基础镜像、102,171 个 workspace，82.8 TB；microVM：2 个基础镜像、53,590 个 workspace、4,889 个快照，50.9 TB | §4.2、表 2 |
| 镜像 fanout | 容器 p50 3、p90 28；microVM p50 1、p90 3 | §4.4、图 8 |
| 运行时访问比例 | C++ 8.7%（4.9 GB）、Go 13.3%（4.1 GB）、Java 9.2%（12.1 GB）、JavaScript 4.2%（9.6 GB）、Python 6.0%（6.0 GB） | §4.4、表 3 |

正文第 11.1.2 节引用 90%／5%、存活时间与单节点密度；第 11.2.2 节引用表 3 的 4%–13% 与 4–12 GB。

## 本书换算

**每节点创建速率（第 11.3.2 节）。** $5000/160\approx31.3$ 个/(节点·s)。这是整个单元峰值按节点的平均值，与第 11.2.4 节单台主机每秒创建 30 个环境的题设相当。

**一个作业的沙箱内存（第 11.2.3 节）。** 按章首 1 vCPU、2 GiB 的沙箱规格，$32768\times2\ \mathrm{GiB}=65536\ \mathrm{GiB}\approx70.4\ \mathrm{TB}$，占一个单元约 250 TB DRAM 的约 28%。2 GiB 是本书题设，不是 DSec 公布的沙箱内存。

**暂停的收益（第 11.2.3 节）。** 沿用 E2B 文档的每 GiB 保存 4 s、恢复 1 s，2 GiB 沙箱的保存与恢复共 9 s，期间仍占内存。若 GPU 作业中断 2 h（第 10.4.4 节 MiMo Pro 的 14 次中断区间在 0.96–2.95 h 之间），释放时间为 $7200-9=7191$ s，与继续占用的 9 s 之比约为 799。

## 机制与测量

**按需加载（§5.3、§8.2）。** 10 节点测试集群上一次启动 8,192 个容器：按需加载 EROFS 约 35 min 完成，与镜像全部预先缓存相当；完整拉取镜像超过 60 min，慢 1.71 倍。每节点累计写盘：完整拉取超过 1,600 GB，按需加载约 700 GB（减少约 57%），全部缓存约 600 GB。设计原则来自 3FS 的读写不对称：写入留在本地；读取按需并合并成大块；元数据尽量放在本地。

**可组合层（§4.2、§5.1、§8.3）。** 基础镜像、workspace 与 toolkit 分别维护为只读层，由 overlayfs 在创建时叠加；升级 $m$ 个基础镜像或 $k$ 个 toolkit 的重建代价从 $O(m\cdot N)$、$O(k\cdot N)$ 降为 $O(m)$、$O(k)$。同一评测中，tar 逐个解压需 79 min，直接挂载 EROFS 层 45 min（1.76 倍），tar 方案写盘总量为 5.5 倍。正文未展开这一项。

**内存（§5.2、§8.4）。** virtio-pmem＋DAX 让各 microVM 共享宿主机的一份 page cache，峰值内存降低 40.2%；代价是 guest 为 pmem 地址范围分配 struct page（4 KiB 页、64 B 描述符，即设备容量的 1/64，128 GB 设备需 2 GB），瞬时 CPU 峰值由 26.5% 升到 41.4%。DAMON 回收冷文件页，配合 virtio-balloon 空闲页报告（默认 order-9，即 2 MiB 块），峰值基本不变，时间积分内存降低 21.2%。生产中只读的 EROFS 基础镜像与 toolkit 层用 pmem，较大的可写磁盘用 DAMON＋空闲页报告。

**CPU QoS（§5.2、§8.5）。** BE 任务放入 `SCHED_IDLE`，LS 任务开启 core scheduling（`prctl(PR_SCHED_CORE)`）。下棋 agent 在 50% BE 负载下每步耗时增加 45.2%；只用 `SCHED_IDLE` 最多改善 3.4%；两者结合后增幅为 17.3%。剩余干扰来自多核高负载时的降频、内存带宽与 LLC 争用，DSec 未另做内存带宽隔离。

**放置（§3.2、§7）。** 过滤出健康、具备所需后端与硬件的节点，随机抽取 $k$ 个选负载最低者；每个调度实例把尚未反映在 watcher 快照中的近期放置叠加到本地视图；节点 edge 保留最终准入权。调度器与 watcher 均无持久状态。本地利用率超过 80% 时，部分请求分流到云上 VM：30 TB 去重后的 EROFS 镜像集覆盖 70% 的容器任务，依赖全在其中的任务才可分流；200 台云 VM 吸收约 30% 的峰值溢出（§3.4，正文未展开）。

**暂停（§6.3）。** 容器：`docker pause` 冻结进程树，开启 `memory.swap.max` 并写 `memory.reclaim` 主动回收；恢复时对内存映射执行 `MADV_WILLNEED` 异步预取，再 `docker unpause`。microVM：保存内存与执行状态快照后结束 Firecracker 进程，恢复时由新进程载入快照。发往已暂停沙箱的请求会先透明地恢复它。

**agent 循环的归属（§6.2）。** 早期 agent 循环与模型服务、RL 框架同在可抢占的 GPU pod 中，抢占后依靠命令日志重放，已完成的操作复用记录结果。从 DeepSeek V4.1 起，rollout 执行拆为运行 scaffold 与工具的 agent 沙箱和管理沙箱的 worker 容器，二者都在可抢占 GPU 池之外，共同作为 rollout 状态的唯一来源。

**隔离与越界行为（§2.2、§3.3、§6.4–6.5）。** 四类后端：FnCall（预建、可复用，面向无状态任务，含 GPU 版）、容器（运行在 QEMU／libvirt 虚拟机内）、Firecracker microVM、完整 VM（QEMU，含 Android 与 GPU 半虚拟化图形）。记录到的 agent 行为包括伪造发往 chronus socket 的 RPC、读取 chronus 日志、覆盖 `/bin/bash`、用 `XFS_IOC_SWAPEXT` 绕过访问控制而损坏 XFS 元数据，以及扫描端口、借助 Go module proxy 获取参考实现。无意破坏包括递归 `grep` 读取 `/proc/kpagecgroup` 触发内核缺陷，以及 `yes` 的输出被记录到数十 GB。缓解措施是 AppArmor（文件与 socket）和按任务动态更新的 eBPF 网络白名单。

**GPU 验证后端（§7）。** MIG 切分、CPU FnCall 负责编译、预热的 Python 进程池；非性能敏感任务另有共享 GPU 模式。

[^src]: DeepSeek-AI 与清华大学，DeepSeek Elastic Compute (DSec): A Sandbox Infrastructure for Effective Agentic Training at Scale，arXiv 2609.22978v1，2026-09-19。[PDF](../references/files/papers/dsec-sandbox.pdf)、[文本](../references/text/dsec-sandbox.txt)。评测环境为 10 节点测试集群（AMD EPYC 9655，宿主 Linux 7.0），与生产部署分开（§8.1）。
