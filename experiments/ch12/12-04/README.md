# 实验 12-4：连接复用与多流传输

**已按原题允许的计算／网络记录范围完成。** 四类实际源计算、连接复用、匹配窗口、分块/释放、恢复与贡献分析均已核验。[播放记录计算](playback-records/README.md)将196条实测TTS到达轨迹转换成明确三帧缓冲策略下的首次播放、逐帧消费与停顿。实际声学起播未测，不冒充人耳或麦克风测量；原题没有额外声学必需条件。逐项证据与此范围判定见[覆盖审查](COVERAGE-REVIEW.md)。

本实验使用本地Mac与RTX服务器，以及隔离Docker中的真实TCP/TLS和QUIC传输，无E2B依赖。源模型/CPU计算实际执行过；网络矩阵使用固定真实输入输出及已测服务时间/可用时间记录重放，不把每次传输算作新推理或新浏览器任务。固定网络为容器loopback netem配置80ms RTT、20Mbit/s、0.1%损失；部分复用实验另有零损失对照。早期短校准RTT约80.12ms、TCP有效吞吐17.4–17.7Mbit/s，配置带宽与应用goodput不等同。

| 子项 | 当前证据 |
|---|---|
| 图片源与复用 | [Mac/RTX RAW处理与成片](image-records/README.md)：各1预热3正式；最终26/26传输经完整JPEG/RGB核验。初始超时批次保留。 |
| ASR源与复用 | [Whisper实际识别与52网络交换](speech-records/README.md)：固定Fish音频、完整UTF8结果；对合成意图文本的编辑距不当作人工声学真值。 |
| TTS源与复用 | [52次完整音频传输](tts-network/README.md)：294段源接收可用时序重放，完整WAV/PCM、首20ms及三帧阈值核验。 |
| Computer Use源与复用 | [真实截图模型任务与98交换](computer-use/README.md)：无约束3次均JSON失败；独立结构化解码3次均完成8动作，失败记录保留。网络阶段为固定八轮动作记录。 |
| 接收窗口 | [匹配设置324交换](receive-windows/README.md)：四负载、三配置、三位置平衡轮次，显式TCP_NODELAY=1/proto6与实际readback，全部通过。 |
| TTS释放/分块 | [90交换](tts-chunking/README.md)：原294段、64KiB合并、整段等待；全字节与释放时间核验。 |
| 应用写入分块 | [transfer-chunks](transfer-chunks/README.md)：whole/16KiB/64KiB，三负载270交换全部验证，27容器已清理。 |
| 图片恢复 | [20任务/32交换](interrupted-recovery/README.md)：12次断连，完整重传与保留不可变输出续传，完整成片身份核验。 |
| 其余负载恢复 | [workload-recovery](workload-recovery/PROTOCOL.md)：合同、运行器、独立分析器已准备，60任务/222交换/36断连全部独立验收，三容器已清理。 |

匹配窗口前发现手工socket的proto元数据影响asyncio默认NODELAY行为，[同镜像探针](socket-defaults/README.md)对此做了复核。旧窗口批次保留并注明条件，不与新的NODELAY1矩阵混合。随机损失、共享事件循环、qlog及测量开销都可能影响结果；小样本中位数不支持一般协议排名。

附加协议证据包括[固定网络校准与388交换](controlled-network/README.md)、[HTTP3实际多流并发](h3-multistream/README.md)及[早期loopback记录与勘误](loopback/README.md)。这些记录不替代四类业务结果。客户端是归档h11/aioquic实现，default表示这些实现的默认设置，不声称代表所有浏览器或网络库。

[跨负载贡献分析](CONTRIBUTIONS.md)汇总同批次对照与限制。

[历史进展记录](PROGRESS-HISTORY.md)保留各中间检查点。复跑入口、原始结果、分析器及适用限制见各子目录。不同实验的服务/连接清理/结果验证边界须分别读取，不混合绝对延迟。
