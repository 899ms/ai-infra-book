# Docker完整生命周期状态合同：12案例通过

rtx-pro独立Docker24.0.9/containerd、CRIU4.2.1（commit9539417f3e3cfa4eb84c319cd71f4d52f1f08645），同一固定python:3.11-slim image ID、worker源码、1CPU/256MiB，无GPU。三轮确定性打乱四路径；每案例均记录初始创建、容器身份、文件marker、仅在内存中的nonce/counter、命令ID及外部事件账本。运行代码和environment.json绑定源码与实际版本。

**12案例状态核验通过，三次检查点各派生两个实例，共六个成功恢复。**

| 路径 | 三次结果 |
|---|---|
| pause/unpause | 同容器ID，文件、nonce及counter保持；原命令流继续 |
| clean rebuild | 新容器ID、新nonce、counter=0，旧marker不存在 |
| filesystem commit | 新容器ID、新nonce、counter=0，marker保留；原实例保持 |
| checkpoint派生 | 捕获后原实例保持；两个新容器恢复相同nonce、counter=1和marker；分别加10／11后为11／12；两者都改完再分别重连读取，仍为11／12，原实例仍1 |

全部状态探针request_id与外部账本一一对应，账本位于容器外，恢复没有回滚此前请求记录。容器内PID=1、恢复后的hostname等不作为独立身份依据，身份用完整Docker container ID。六个派生实例真实同时存在并分别修改，不是先销毁再启动同一实例。

活动控制连接下三次捕获均拒绝，负结果完整保留；关闭连接后leave-running捕获均成功，恢复后重新建立控制连接并测首工具。这区分进程内存恢复与活动连接保持：快照路径不能声称恢复原活动连接。

## 时间和代价

以下是本机三次中位数，含CLI/API和主机背景负载；不是生产p95。初始创建以pause案例为同一基准。

| 计时区间 | 中位数 |
|---|---:|
| 初始创建开始→首工具 | 269.226ms |
| unpause开始→首工具 | 28.000ms |
| 干净新容器创建开始→首工具 | 286.022ms |
| 已commit镜像的新容器创建开始→首工具 | 272.975ms |
| clone首次restore尝试→首工具（六个clone，含本次重试） | 299.007ms |

clone六次区间为500.438／291.843／284.612／306.171／280.589／307.755ms。这里从commands.jsonl的首次start --checkpoint取起点，不能只用最终成功重试的起点而漏掉失败开销。镜像commit、checkpoint保存、创建clone及拷贝checkpoint另在命令事件中记录，未包含在299ms恢复区间；文件系统行不包含commit保存；干净重建行不包含旧实例停止。不能把这些恢复段数字当完整保存／派生成本。

Agent有待续接进程状态时可用通过本探针的内存恢复，并重新连接；需要跨实例复用时须保留提交记录，避免重放外部副作用。RL验证需要干净基线时应使用干净重建；filesystem恢复会带回文件，内存恢复还带回计数器及进程状态，不能视为无污染重置。容量／启动预算另见当前第11章答案，按恢复状态与并发资源分别计入，不用此小worker的256MiB外推真实Agent容量。

## 明确的运行变更及限制

PROTOCOL.md是原Docker协议的封存副本；本次实际变更由probe.py/run.py给出：系统安装保持不变，使用隔离daemon及构建的CRIU；host网络下通过docker exec桥接容器私有Unix socket（不是原协议所述TCP监听），不绑定用户目录。初始image由本机已有镜像导出／导入隔离store；没有收费资源。

Docker有时在content提交遇到already exists，本实验仅针对当前失败digest查询私有store、若仍存在则删除，再重试本地checkpoint，所有尝试保留。成功结论因此是**带明确诊断重试的Docker24/CRIU4.2.1组合**，不声称系统Docker28原生无干预通过。该组合和原来的失败组合不合并成一个成功率／性能样本。

两个daemon正常退出0，runner记录本实验容器全部删除。旧runtime有三次删除等待并遗留无工作子进程的shim，后续按私有socket与进程类型检查并终止；最终shim-cleanup.json复查为空。初次清理遍历匹配过宽，误匹配到执行检查的shell并由“存在子进程”断言停止，未杀该shell；复查改为同时要求comm=containerd-shim。远端私有镜像／checkpoint存储保留，未改其他daemon。

全部cases、ledger、命令、源及checkpoint原件已取回Mac。首次普通rsync无法读取root权限snap目录，返回23；随后以远端sudo rsync仅读取本实验路径完成传输，退出0。analyze.py离线验证12案例、源哈希、唯一请求ID、状态合同、六次派生修改及交叉读取；summary.json记录通过。此为作者授权的Docker替代实验，不是E2B测量；不承诺断电持久性、跨机器迁移或任意生产工作负载可恢复。
