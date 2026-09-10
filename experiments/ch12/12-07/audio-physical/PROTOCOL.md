# 12-7 显式物理接口两端协议

沿用固定Queqiao/TUIC版本、Fish PCM、Mac静音真实音频回调、RTX实际原生UDP server、四轮pool ABBA以及8完整/8取消。两个client均设置原生LocalAddress="if:en0"，由固定源码netbind.InterfaceControl在Darwin设置IP_BOUND_IF；不改系统路由、不关闭TUN。先行独立probe实际getsockopt读回en0索引14。

RTX包装PacketConn.ReadFrom仅记录每个新来源socket的IP哈希/端口/栈，不改报文；对照先行probe的来源哈希，核验实际到达RTX的路径身份。不能由一个来源地址推出全路径没有任何中间设备。client—origin的时钟未同步，不相减推算单向取消传播。

除了共同的接口绑定和来源观测外，固定音频、发送节拍、设备helper和条件顺序同前一批；前批不是同一时段，所以不把两批差值直接当作TUN开销。源不足/驱动欠载分别报告，慢样本、正式重复、主动取消保留。固定音频重放没有模型取消；静音不是声学测量。

执行前修正：此版本baseline原只解析本地IP，不支持if:en0。实验副本仅将baseline的UDP socket解析/创建改为同一个netbind.ResolveWithInterface与InterfaceControl；原始文件保存在sources/baseline-original.go，before/after SHA见baseline-binding-patch.json。QUIC/TUIC认证、拥塞与数据流逻辑未改，其余265源文件保持原SHA。比较时明确这是socket绑定适配版基线。
