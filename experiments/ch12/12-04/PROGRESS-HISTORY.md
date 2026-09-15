# Historical progress notes

These notes describe intermediate checkpoints. Current status is in README.md and COVERAGE-REVIEW.md. Later evidence supersedes pending-status statements below; old experiment data is preserved.

> 2026-09-15 四负载窗口匹配重跑已完成：[324/324独立验证与图](receive-windows/README.md)，显式NODELAY1/proto6、全字节/时序/参数与36容器清理通过。旧手工socket批次保留但不混合。transfer-chunks270交换已开始，恢复工作负载代码已准备未运行。

> 2026-09-15 socket默认值复核：[探针](socket-defaults/README.md)确认implicit与manual proto0的NODELAY默认不同。TTS54与Computer162窗口记录已验证但需保留此条件；[四负载完整匹配重跑](receive-windows/README.md)显式NODELAY1并逐socket读取，正在执行。

> 2026-09-15 ASR窗口：[54/54真实传输与参数核验](asr-windows/README.md)。三种接收配置按位置平衡次序运行，WAV/完整UTF8与实际TCP/QUIC配置全部验证，九容器清理。其余负载/因素缺口以COVERAGE-REVIEW为准。

> 2026-09-15 图像恢复：[20任务/32交换独立验证](interrupted-recovery/README.md)，12次断连后全量重传或保留输出续传均恢复精确成片。参见[完整负载覆盖表](COVERAGE-REVIEW.md)：图像结果不替代ASR/TTS/Computer Use未测单元，ASR窗口补测进行中。

> 2026-09-15 图像窗口配置：[54/54真实传输与TCP/QUIC参数核验](window-sizing/README.md)。默认/64KiB/4MiB均保留全样本；TCP小buffer明显受接收窗口限制，QUIC初始额度会增长。故障恢复运行中，跨负载最终整合仍待。

> 2026-09-15 Computer Use补测：[真实截图模型与网络记录](computer-use/README.md)。原始无约束0/3，结构化解码独立3/3成功（各8动作）；固定首trial的98网络交换全验证。窗口、恢复及最终整合仍待，不将记录等待当新GPU推理。

## Full-resolution image workload update

[Eight actual RAW developments and final-image transfer records](image-records/README.md) completed. Full4284×2844 JPEGs were verified and visually inspected; Mac/RTX CPU output differences are retained. The initial asymmetric-deadline network batch had9 HTTP3 timeouts; a full rerun with a common120s deadline passed26/26 image decodes and pixel checks. Processing time is explicitly replayed in the network stage. Computer Use, window sizing, interrupted recovery and final integration remain pending.

## TTS chunking comparison update

[90 transfers across three chunk policies](tts-chunking/README.md) completed and verified: recorded segments,64KiB PCM coalescing and whole-response buffering. All modes were rerun in shuffled order across three trials under the same configured network profile. Source bytes and availability are fixed; actual acoustic playback is not measured. Image/Computer Use, window sizing and interrupted recovery remain pending.

## TTS first-playable delivery update

[52 TTS availability-trace transfers](tts-network/README.md) completed under both fixed netem profiles. All WAV/PCM bytes and294 release segments per response verified; header arrival, complete20ms PCM frame and three-frame readiness are separate. This uses recorded synthesis availability and actual HTTP transport, not new synthesis or acoustic playback. Image/Computer Use and window/chunk/recovery comparisons remain pending.

## Actual ASR and speech-network records

[Four GPU recognition runs and52 network-record requests](speech-records/README.md) completed. Actual fixed WAV and recognition-result bytes are transferred under both netem profiles; the measured0.623s median model service is an explicit replay wait. Recognition contains two extra tokens relative to the intended synthesis text; no human acoustic ground truth is claimed. TTS/image/Computer Use and window/chunk/recovery comparisons remain pending.

## Controlled-network transport update

[Docker netem calibration and two full protocol profiles](controlled-network/README.md) completed388 byte-exact HTTP1.1/HTTP3 responses under measured80.12ms RTT and configured20Mbit/s,loss0/0.1%. Application-level image/speech/Computer Use, window/chunk tuning and recovery comparisons remain pending. Earlier loopback records below remain separate.

# 实验 12-4：连接复用与多流传输

对应正文 12.2。本目录交付两组真实传输实测，均走本地真实 socket，**不是用计时模拟协议**。

## 两组记录

- [loopback/](loopback/README.md)：HTTP/1.1 over TCP+TLS1.3 与 HTTP/3 over QUIC 的对照。**192 个正式请求 ＋ 2 个预热，194/194 上传与回传字节校验通过**；HTTP/1.1 实际协商 TLSv1.3／ALPN `http/1.1`，HTTP/3 实际握手 ALPN `h3`，97 个成功响应头与 DATA 帧由原始 qlog 复核。两路径共享 64 KiB 固定载荷与同一现场生成的自签证书。没有 HTTP/2，也没有 0-RTT／会话恢复。
- [h3-multistream/](h3-multistream/README.md)：HTTP/3 单连接多流真实 PNG 传输。正式批次 144 次请求 ＋ 18 次连接预热共 **162 次响应全部通过 PNG 字节与 RGBA 像素校验**；此前独立 smoke 的 48 次请求与 6 次预热也全部通过。并发条件下客户端在途与服务端接收的重叠峰值**实际达到 8**，串行条件均为 1。

## 结论

连接复用与多流是两件不同的事，两组记录分别给出证据：

1. **协议本身的差别在本地 loopback 上很小**，因为没有丢包、没有排队，QUIC 的主要优势（连接迁移、无队头阻塞）用不上。194/194 字节校验说明两条路径功能等价——**要比较协议，必须在有损网络上比**。
2. **单连接多流真正做到了并发**：在途峰值 8 对串行的 1，证明多流不是"轮流用一条连接"。这是连接复用能兑现的部分。

## 独立运行

各子目录自带运行入口与依赖锁文件（`requirements-lock.txt`）。本地 Mac arm64、Python 3.14.7、h11 0.16.0、aioquic 1.3.0。

## 限制

- 本地 loopback，无丢包、无排队、无跨主机路径；不能据此排名两种协议在广域网上的表现。
- 原需求中的图片成片、ASR/TTS、Computer Use 结果及固定广域网络条件仍未完成——这几项的时间预算由实验 12-2 的计算给出。
- 证书为现场生成的自签测试证书，客户端将其作为可信 CA 验证 localhost SAN；不代表生产 PKI 路径的开销。
