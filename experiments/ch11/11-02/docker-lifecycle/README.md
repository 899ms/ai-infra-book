> 2026-09-15更新：作者授权的Docker替代完整状态合同已通过，新增12案例及六个独立内存派生见[实测结果](isolated-daemon/full-worker/README.md)。以下保留早期配置与失败，不能将历史失败误作当前总状态。

# Docker 环境创建、暂停和恢复实测

作者明确将原E2B实验替换为 **rtx-pro上的Docker容器**，因此没有请求E2B凭据，也不把这些数据称为E2B或microVM测量。已验证36个正式案例：三轮bridge/custom-dir、三轮bridge/default-dir、三轮host-network/Unix控制，每轮含暂停、检查点派生、干净重建、文件系统恢复；每个案例另测初始创建。三种配置各自保留，不合并成一个性能样本集。

**创建、暂停续接、干净重建、文件系统恢复的状态合同通过；内存检查点能捕获，但派生恢复未成功。** 18次正式派生恢复全部保留失败，另有诊断尝试；恢复成功时间为null。不能将checkpoint create返回成功写成恢复成功。

## 状态结果

|路径|文件marker|内存nonce/计数器|身份与连接|结果|
|---|---|---|---|---|
|固定基础镜像创建|旧marker不存在|新nonce，counter=0|新容器，建立命令流|通过|
|pause/unpause|保持|保持|同容器，原命令流可继续|通过|
|干净重建|旧marker不存在|新nonce，counter=0|新容器，新连接|通过|
|commit文件系统后启动新容器|旧marker保持|新nonce，counter=0|新容器，新连接；原容器继续|通过|
|内存checkpoint派生两个实例|捕获时保存文件与内存状态|没有成功返回的恢复实例，不能断言恢复后的值|每次创建两个独立目标容器，restore被拒|未成功恢复|

随机nonce只在worker内存里生成，文件标记另行写入容器可写层。外部事件账本保存每条实际请求ID和响应，没有放进容器快照；恢复操作不能回滚这些已经发生的外部事件。PID=1相同不证明实例相同，核验使用Docker完整容器ID和单独的内存nonce。

## 计时

以下仅列 **bridge/default-dir** 三次中位数，单位ms；均包括Docker CLI/API、连接和首工具响应，未隔离服务器CPU背景负载。

|路径|操作开始至首工具完成|
|---|---:|
|初始创建（暂停案例的初始创建）|425.08|
|unpause后首工具|33.97|
|干净重建后首工具|435.19|
|文件系统镜像创建新容器后首工具|376.98|
|内存检查点恢复后首工具|无成功测量|

文件系统恢复行不包含此前commit保存耗时，`summary.json`逐例另列save_api_s；干净重建行不包含此前停止旧实例的耗时，原停止区间在cases.jsonl。不能据这个表估算完整保存/恢复周期而省略保存或清理。各配置初始创建、各操作API边界、重连、首工具和清理的完整区间在原始记录。只有三个重复，不作生产p95或云平台容量推论。

## 兼容性和负结果

运行环境为Docker Engine 28.5.2、containerd1.7.29、runc1.3.3、CRIU3.16.1、Linux6.8.0-138。基础python:3.11-slim固定为实际完整image ID；单容器1 CPU/256MiB，无GPU。未下载镜像、修改Docker daemon或停止其他容器。

1. 活动命令连接存在时捕获被拒；关闭该命令流后同案例的leave-running检查点捕获成功。
2. 原始`docker start --checkpoint-dir`被此daemon拒绝：`custom checkpointdir is not supported`。该组原件在results/，没有删除失败来得到更好结果。
3. 使用新容器的默认checkpoint目录后，bridge配置遇到`/proc/0/ns/net`错误。该错误与[Docker 28上游报告](https://github.com/moby/moby/issues/50750)相符；这里只报告匹配的症状，不宣称修复了Docker。
4. 独立host-network控制避免了bridge路径，命令使用容器内私有Unix socket经docker exec传送，没有host监听端口。仍出现`OCI runtime restore failed: criu failed: type RESTORE`，偶尔出现containerd内容摘要already exists。后者有[上游同类报告](https://github.com/moby/moby/issues/42900)。此控制没有证明成功的内存派生，故保留未完成字段。
5. 初次Unix控制程序把一次read当成完整READY行，遇到分段读取而退出；v2改为读到换行，随后12案例完成。旧程序、日志与清理记录保留。两个额外单案例诊断保存命令和日志；没有根据不完整错误信息猜测CRIU根因。

另保留两次同容器恢复诊断：原状态再次捕获遇到内容摘要重复；第二次先将计数器增加7，避免该重复后捕获成功，但恢复仍报CRIU RESTORE错误。随后普通启动产生新内存nonce，属于冷启动，未计为内存恢复成功。详见results-same-container与results-same-mutated。

[Docker官方checkpoint说明](https://docs.docker.com/reference/cli/docker/checkpoint/)将该功能标为experimental。要完成原题的“两个内存状态派生实例同时独立运行”正向验证，还需要能通过本状态探针的Docker/CRIU恢复组合；目前不是缺E2B API key，也不需要额外GPU。

## 原件和复核

运行源代码和协议、完整Docker命令及退出码、独立事件账本、cases.jsonl、镜像/容器身份、CRIU文件清单与SHA、清理记录均已取回Mac。checkpoint的原始内存镜像仍保存在rtx-pro本实验目录；本地省略snap/二进制目录，保留按文件哈希及采样日志。不声称离线哈希能代替restore成功。所有本次创建的容器已清理，临时镜像标签已移除；checkpoint证据保留。

`python3 analyze.py`核验36个正式案例的状态、请求身份、顺序、源SHA和容器清理，并生成summary.json。原程序只接受新的结果目录，复跑必须选择新目录，不能覆盖这些记录。此次不修改原E2B文档核对记录，它们是另一种运行时的历史来源。
