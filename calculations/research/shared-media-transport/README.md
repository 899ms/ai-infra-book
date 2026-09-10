# C68 共享链路、媒体截止与业务交付：有限教学协议

这是研究候选，尚未公共接入或完成图12-4全部要求。代码采用精确Fraction事件时间，不执行真实TCP/QUIC、模型或播放设备；固定恢复时刻、信用和串行块不是CUBIC/BBR/PTO/MAX_DATA实现。六份固定官方RFC每次校验原字节长度和SHA256，具体适用范围见[来源说明](SOURCE-SCOPE.md)。默认业务常数及夹具来源见[业务输入说明](workload-inputs.md)；协议来源不提供默认模型时延。

```bash
python3 calculations/research/shared-media-transport/calculate.py \
  --output calculations/research/shared-media-transport/result.json
# 单个可编辑场景：--inputs path/to/input.json --output path/to/result.json
```

API `calculate(inputs)`、`example()`、`scenarios()`；runner默认返回16个`名称→结果`。`scenarios.json`保存可编辑原始输入。结果区分事件队列结束、网络未完成、业务可用和播放质量；没有未来事件不表示图片或音频已经全部完成。

## 发送、信用和交付

每方向一个非抢占出口。数据、恢复、ACK及取消共用相应链路，发送器在真正空闲时选择下一单元。`scheduler=fifo|priority`只控制网络发送；`compute_scheduler=fifo|priority`独立控制工作资源，默认FIFO，mixed两个调度对照保持同一compute_scheduler。优先级大者先发送；优先级模式下ACK优先级为声明的10^9。已开始的大单元不能被高优先级音频抢占。

所有数据共享有限`shared_credit_bytes`，按有效payload预留，不因新增流增加。可靠数据还需要`reliable_receive_credit_bytes`和`stream_credit_bytes`；不可靠媒体不占后两项。实际收到ACK才释放发送方可见信用，每个逻辑单元只释放一次。接收方把运输单元消费到**另列、未在本模型限制容量的重组存储**，故这里的接收暂存信用不能冒充完整应用内存或真实流控。ACK表示运输收到，不表示应用按序交付、识别完成或设备播放。

恢复输入`recovery_ready`是声明的最早重发就绪时刻。唯一首发损失`drop_first`可在可靠数据上恢复一次，复用逻辑单元身份及已占信用，记录新attempt和重复wire；这明确不同于真实QUIC每次发送的新包号。没有收到的损失数据不能靠未来接收状态释放信用。不可靠损失不重发，若没有反馈就保留共享信用；`unreliable-loss-credit`展示因此无法再发送下一单元的未完成情况。

网络到达与应用交付分开。可靠数据按`delivery_mode=connection|per_stream`等待前驱；不可靠独立媒体不成为可靠顺序前驱。`delivery_only_replay`在同一成功网络到达记录上只重放交付规则及过期准入，**不重新生成任务、ACK或数据**。它用来隔离队首阻塞；重新运行另一调度/交付政策会影响依赖业务生成，不能把这类变化冒充完全相同发送轨迹。

25,000B图像“包”是声明教学串行块，不宣称符合任何默认路径MTU或真实QUIC单数据报布局。默认头40B、ACK40B同样是教学声明。发送后超期不退还链路占用或字节；实际到达后仍可运输ACK。只有`reliable=false,allow_expire=true`且明确deadline的单元可以过期；可靠成片配置过期策略会被拒绝。

同刻先处理到达/状态变化，随后序列化与工作结束，再处理截止到期，最后发送准入。到达恰在deadline时允许交付，不能先按过期丢弃。输出`expiry_stage`区分未发送/已发送后到期，`lost`与attempt标明网络损失和恢复，`deadline_met`与运输接收分开。

## 任务、消息与取消的端点

输入packets包含全局唯一id、stream（不可靠情形是应用flow标签，不冒称QUIC stream ID）、direction、offset/payload、ready、dependencies、priority、可靠/过期政策、deadline及可选恢复/取消。每应用流的输入区间从0连续覆盖，拒绝空洞和重叠。tasks包含id、dependencies、duration、endpoint/client或server、resource、priority与cancel_tag；工作资源按(endpoint,resource)隔离。

依赖只可在同一知情端消费：上行包交付可启动服务器工作；服务器工作可生成下行包。客户端收到ASR文本不能瞬时让服务器开始TTS，若要这种交互必须添加实际回传消息。依赖环、未知节点和跨端瞬时依赖直接拒绝。

取消是应用控制消息：经过可靠顺序交付后，接收应用的一端才更新该端cancel_tag；仅transport到达或ACK不能绕过连接/流队首阻塞。c2s取消到服务器不能同时让客户端未发送上行消失。尚未开始的匹配工作/发送被抑制；已开始计算和数据不可抢占，计算仍完成并记账，但未发送输出可以被抑制。`cancel-running-work`保留2–5秒计算，取消2–3秒发送/4秒到达，5秒后结果被抑制。

## 业务指标及固定场景

- `hol-connection`、`hol-per_stream`：同一A–E合同的B0丢失/5秒恢复记录，音频交付7秒与3秒，图像均7秒，data wire均4B。
- `schedule-fifo`、`schedule-priority`：同分包，音频6秒与3秒；图像5秒与6秒，不能宣称优先级使全部业务都快。
- `credit-1-streams`、`credit-3-streams`：两份共享信用，第三包最早4秒发送。
- `playback-reliable`、`playback-slots`：到达3/6/7，可靠播放3–5/6–8/8–10，停顿1秒；槽3–5/5–7/7–9缺第二块，缺音2秒。播放指标分`business_status`、已播/缺失/未解决块和完整播放标志，部分前缀终点不是完整播放完成。
- `image-30mb-5mb`：30,000,000B全量图像收到后才能启动0.3秒整图任务，任务完成再生成5,000,000B成片。没有把早到音频或首响应字节当整图结果。
- `mixed-fifo`、`mixed-priority`：同一图像、8块ASR输入（声明16kHz mono PCM16/20ms=640B）、声明0.05秒ASR任务/64B结果、8块TTS（声明24kHz mono PCM16/20ms=960B，每块生产0.012秒）、一张3443B截图、64B动作结果和32B取消信号共享资源。TTS任务从**服务器ASR任务完成**派生。其生成速度不是Fish Speech实测。
- `mixed-preview-priority`：在混合输入上增加显式0.05秒预览工作和500000B预览。`preview_complete`单列，声明预览不等于成片质量；不是把真实RAW模型假定为天然可独立分块。此消融的额外工作/字节不能藏进基线。
- `screenshot-complete`、`screenshot-stale`：同一上传—推理—动作结果完整轮次，分别无版本变更／客户端0.08秒已知v2；旧v1结果到客户端即使传输完整也不能用于当前操作。版本判断域明确为客户端。
- `cancel-running-work`与`unreliable-loss-credit`保留取消及无反馈信用停滞边界。

混合输入只使用一张截图，不是业务输入建议中三张截图的全集；按实际输入总量复算。业务required与所有播放块必须在同一接收端可知，可靠成片不得用可丢弃单元。无结果/旧版本/播放缺块均不能靠`unfinished=[]`变成业务完成。

## 可复核输出与限制

`transmissions`逐单元给方向、offset/end、attempt、payload/wire、start/end/arrival及loss；`credit_events`记录预留/实际ACK释放；`packets`记录收到、交付、过期、取消；`work`记录端点/资源/非抢占时间；`cancellations`记录真实接收端与时刻；`businesses`连接完整图像、识别文本、播放和截图可用结果。`unfinished_details`给依赖未完成、丢失无剩余恢复或反馈、共享信用不足、交付前驱缺失等明确原因。

最多20000个数据/工作节点。未实现完整网络栈、一般损失探测、ACK压缩/延迟ACK、真实拥塞/流控、物理无线竞争、实际模型推理与设备音频处理；六份规范用于划清语义，不给这些教学参数背书。业务quality与网络完成分账，C68和相邻C69原缺口继续保留。

## 研究时间轴

[小整数丢失与逐流交付图](figure-hol/timeline.png)和[混合业务首秒图](figure-mixed-start/timeline.png)由plot.py直接读取事件结果生成；SVG、精确事件data.json和来源manifest同目录。首秒图为明确窗口裁剪，不表示图片在1秒内完成；红色业务点是已到达但版本不可用的结果。当前只是图12-4的研究面板，公共图表注册与完整组合图仍待。
