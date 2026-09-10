# 12-7：Queqiao 的单因素比较

**总体部分完成。** [固定音频隧道实跑](audio-tunnel/README.md)已完成原生 Queqiao／TUIC 基线的 8 次完整流和 8 次主动取消：音频逐字节一致，三帧预缓冲的软件消费端未空缓冲，origin 观察到关闭。另已补实际静音输出设备回调；另有Mac—RTX两端实跑，但默认经既有TUN；另已补显式en0绑定与RTX来源核验；声学测量与模型取消仍缺。

- [连接池传输对照](transport-pool/README.md)：固定版本四轮 ABBA、16 组对象传输和 8 组 cold/warm 请求。
- [真实 TTS 接收边界](tts-stream/README.md)：四次完整合成与一次客户端取消，分开 WAV 头和 PCM；提供固定音频来源。
- [固定音频隧道](audio-tunnel/README.md)：逐帧接收、在线软件缓冲及取消传播的完整原件和图。

- [真实输出设备回调](audio-device/README.md)：固定PCM经隧道后由PortAudio/CoreAudio回调消费，分开源不足、驱动欠载与设备取消API。

- [两端实际系统路由](audio-wan/README.md)：固定PCM从RTX传至Mac，保留源不足及取消，明确已有utun路由。

- [显式物理接口对照](audio-physical/README.md)：含基线socket绑定补丁、实际来源证据、源不足与零回调提前取消的验收修正。

旧 Queqiao 原始记录统计属于另一个任务的 C70，本目录未重复。
