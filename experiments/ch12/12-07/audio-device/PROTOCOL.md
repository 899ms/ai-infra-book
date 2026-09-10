# 真实输出设备回调协议

固定 audio-tunnel 的 Queqiao 源码、Fish PCM、40ms/100Mbit/s 模拟链路、四轮 pool ABBA 与完整/取消条件。原生网络与origin保持相同，接收者把逐帧 PCM 写入独立 Python sink 的 stdin，不用相对timer代替音频消费。新增 pipe/helper 开销明确属于本实现，不能把不同批次与旧sink做纯性能差值。

使用实际默认 MacBook Pro Speakers，经现有 PortAudio/CoreAudio，requested 44100Hz mono PCM16、882frames/callback、至少5292byte预缓冲；只将本stream输出buffer清零静音，不改系统音量。回调按设备请求消费队列并记录帧数、缓冲、source starvation、PortAudio output-underflow flag与API DAC时间。回调是Python/ctypes并有日志开销，不满足硬实时编程规则；欠载若出现须保留，不归咎网络或协议。

PCM消费内容逐字校验；静音意味着没有声学播放质量/实际出声测量。API outputBufferDacTime 是驱动提供的时间，不是麦克风采样。源不足、驱动欠载、EOF尾部补零分开。取消的pipe EOF短于预定音频长度，主线程调用Pa_AbortStream并记录调用返回；不等于远端模型取消。全量8完整+8取消正式条件保留。
