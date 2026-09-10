# C68 混合图片、音频与截图：输入依据与边界

2026-09-09。只读当前公共计算、固定官方元数据和实验文件；本文件不注册来源、不实现调度、不声称真实协议性能。路径均相对仓库根目录。以下字节是十进制 B，链路速率为 bit/s，时间为秒；用 rational string 保持精确。

## 建议冻结的有限主场景

共享 `c2s=20,000,000 bit/s`、`s2c=100,000,000 bit/s`，每向传播 `1/20 s`，段上限25,000B、数据头40B、ACK40B、IW50,000B、cap/rwnd1,000,000B，固定RTO1s。它们全部沿用 `calculations/results/window-reused.json` 的教学参数，不是硬件/网络实测。音频/截图/图片共享同一方向序列化资源与连接窗口，不能各自拿一份完整带宽。

| 流 | 有效载荷 | 就绪/依赖 | 业务边界与声明截止 |
| --- | ---: | --- | --- |
| image-input | 30,000,000B c2s | t=0 | 必须完整接收；不因媒体过期丢弃 |
| image-output | 5,000,000B s2c | image-input 完整收到 + `3/10 s` | 必须完整交付；这0.3s是声明服务时间 |
| asr-input-0…7 | 每块640B c2s | `(i+1)/50 s` | 16kHz mono PCM16，8×20ms=160ms；全部收到后才允许本例完整识别 |
| asr-text | 64B s2c | 全8块完整收到 + `1/20 s` | UTF-8文本载荷固定64B是新声明，0.05s识别也是声明；不能由32token推出64B |
| tts-output-0…7 | 每块960B s2c | 服务端 ASR task 完成后，依次再加 `(i+1)*3/250 s` | 24kHz mono PCM16，8×20ms=160ms。12ms/块是已有audio_timing教学生产间隔，不是Fish测速 |
| screenshot-a-v1 | 3,443B c2s | t=`1/25 s` | 本地固定PNG原样bytes；版本v1 |
| screenshot-a-v2 | 3,545B c2s | t=`2/25 s` | 同尺寸不同内容；版本v2到来使未开始v1工作过时，若采用该政策需显式标注 |
| screenshot-b-v1 | 3,708B c2s | t=`3/25 s` | 不同画面/版本域b，不应自动使a失效 |

截图就绪40/80/120ms、每帧100ms容许延迟，以及截图理解/动作服务50ms（若需要动作结果，可声明64B）都是**新教学假设**，不是下面CPU encoder记录。可先只统计完整截图交付/过期接收，暂不虚构VL动作生成。

音频截止应独立给明示播放锚点与20ms周期。建议两种对照：可靠有序播放，以首块到达+40ms为启动锚、缺块停顿；固定期限媒体，以源生产计划首块时刻+150ms为首块deadline，之后每20ms递增，迟到块标为不可播放或丢弃。150ms为新假设，40ms来自旧教学情景；不要用“首块实际到达+缓冲”偷偷让整条deadline随拥塞平移而报告零超期。ASR全句输入默认可靠，不能套TTS过期丢帧后仍宣称识别语义相同。

冻结三种负载子集便于归因：①图片独占；②ASR→TTS与截图共存；③图片+ASR→TTS+截图全混合。保持有效字节/到达计划/策略一致再比较FIFO与明确调度策略。应用依赖延迟、媒体生产频率、ACK传播分别记账。

## 图片依据

`calculations/results/window-reused.json` 声明 input30,000,000B、output5,000,000B、model3/10s，完整接收结果 `4206639/312500 s`。该结果是事件计算，不是实际图像生成器测速。30MB不是由像素尺寸、patch数或视觉embedding反推得到；本场景已声明一个文件体积。混合后必须重跑共同引擎，不能拿这个独占结果直接叠加其它流。

## 音频依据：波形、code、embedding分开

1. `calculations/sources/qwen3-omni-30b-a3b-instruct/preprocessor_config.json` 为固定官方来源，revision `26291f793822fb6be9555850f06dfe95f2d7e695`。`calculations/results/omni-audio-encoder-short.json` 的 input_time_axis 明示 sample_rate16,000、hop160。20ms采集块是新声明，因此320 samples；再声明mono PCM signed16，即320×1×2=640B。**不是从mel帧数倒推原始waveform长度**；STFT边界/padding另有口径。
2. 同一短音频encoder算例的mel_lengths=[1,9]产生3个有效编码位置、6,144个embedding元素、12,288B输出特征、4,947,107,840矩阵FLOPs。这些是模型接口/算子量；不能把12,288B作为640B采集块的wire大小，也不能将它除硬件峰值当50ms识别时间。它不是完整ASR输出文字或本混合场景的推理记录。
3. `calculations/results/audio-timing-base.json` 明示24,000Hz、mono、2B/sample、20,000,000ns/块，所以960B/块。8块共7,680B与160ms。12,000,000ns模型、40,000,000ns jitter buffer均是教学输入，sources=[]。其send_ns=1ms和逐块网络延迟不应迁移到本引擎作为另收费时间：本引擎已经按960B与共享链路计算序列化/传播。
4. `calculations/configs/models/fish-audio-s2-pro/config.json` 固定HF revision `1de9996b6be38b745688de084d87a5633f714e4e`；num_codebooks10、vocab_size4096描述生成码，不给出PCM网络bitrate。Fish官方 `fish_speech/configs/modded_dac_vq.yaml` 固定源码 revision `befe4001745417f8c42131739d862b8a6fdbd15a`、SHA256 `73321408579c372149620d877f0dfb841cf70465758a535f7243e1cb6553d56a` 声明44,100Hz，与24kHz教学音频不是同一采样率。
5. `calculations/results/fish-wave-two-chunks.json` 的43 acoustic frames经现有算子计算得到88,064输出samples、时长22016/11025秒；6,880B是code D2H，176,128B是声明BF16 waveform D2H，352,256B是standalone DAC CLI waveform D2H。结果明确output_file_bytes=null、first_audio_latency_seconds=null、full_request_latency_seconds=null。不能直接把任一D2H数称为WAV文件或传输编码字节。

可另加**Fish波形派生对照**：由88,064 samples声明mono PCM16，裸payload176,128B，时长22016/11025秒；若拆43个2048-sample块，每块4096B与2048/44100秒。PCM16导出选择、43块独立可播放与每块生产时间均是额外教学假设，不能从现有“一次codec decode、随后两次样本切片”结果冒充流式Fish执行。主场景推荐先使用已有24kHz教学TTS，标题明确“PCM业务模型”，不要冠名Fish实测。

## 截图依据与可重复字节

`experiments/ch12/12-03/fixtures/` 是程序生成、已视觉QA的确定性测试图片，不是实拍Computer Use任务。manifest中：

| 文件 | 尺寸 | bytes | SHA256 |
| --- | --- | ---: | --- |
| a-v1.png | 256×256 | 3443 | fa24b682e13e4c899e27876385c23c59d4d86605ebde81f32094d5bb60d8329d |
| a-v2.png | 256×256 | 3545 | f970d25f43eca62a0d4a1ca150a3cd2f4278993de37ce0b9be0d33f75e19fa86 |
| b-v1.png | 320×256 | 3708 | 676b006fc62b5098155a190bcc74d3cbee8a5b5828778a3b743950f6b686a215 |

本次直接重读文件大小与SHA核验。实验README还记录四组BF16特征（最终+3 DeepStack），a的EC safetensors文件2,097,584B，b为2,621,872B；这些是另一种传输对象，不是PNG或语言KV。CPU视觉encoder基准6.0426/5.7660/7.9719s是固定机器单次记录，不能作为WAN模型服务通用耗时。真正实验wire还含12B framing与UTF-8 JSON；此建议只把PNG计为应用payload，额外声明的40B教学段头不表示复现其TCP应用framing。

同内容不同问题仍需语言计算；同尺寸新内容不能复用旧特征。若新模型要模拟stale版本，定义版本域、替代触发时刻与已预约wire是否不可撤销；不因a-v2生产就把已发送a-v1物理字节从总量删除。

## 建议接口与验收字段

每个业务对象至少有 `id, stream_id, direction, payload_bytes, ready_seconds_exact, dependencies, service_seconds_exact, media_duration_seconds_exact, deadline_seconds_exact, policy, version_domain, version`。依赖语义区分“完整接收”“服务结束”“首块播放”，并注明事件所在端；wire packet identity仍以对象/流/序号区分。业务metadata不必全进入内核，不能阻塞先完成小整数共同窗口手算。

输出至少分列唯一生产bytes、实际发送/重传/ACK bytes、已交付bytes、过期/替代但仍付wire的bytes、完整图片时刻、ASR最终文本时刻、TTS首播与缺块/迟到、每截图接收时刻及版本有效性。正式支持丢弃/替代前不要只按deadline标志声称已取消生产、GPU工作或网络预约。

同服务端因果例：`max(asr-input-0…7.server_complete_received) → ASR server task(+1/20 s) → {asr-text ready-to-send, TTS server production}`。两个输出分支均由服务端 ASR 完成触发；TTS 第 i 块就绪为该服务端结束时刻加 `(i+1)*3/250 s`，不等待 asr-text 在客户端完整收到。若另设“客户端收到识别文本后才请求TTS”的交互策略，必须加入显式 client→server 通知/请求的有效bytes、共享wire占用和到达事件；不能让服务端免费获知远端完成。
