# 两端真实UDP音频协议

固定Queqiao/TUIC版本及同一Fish PCM。Mac原生client→实际网络UDP→RTX原生server→RTX loopback音频origin；Mac接收端继续用真实静音CoreAudio回调。没有pathsim、SSH数据转发或模型再生成。SSH只部署源码、临时认证材料和读取结果。操作系统路由原件另存，不假设路径无其他中间设备。

保持pool on/off/off/on，8完整+8取消，预热后请求音频；origin每20ms发送一帧。两种协议分别绑定RTX UDP19280/19281，loopback音频19282/预热19283。独立临时证书和授权设备，不关闭校验；实验结束删除密钥、退出自身server，不修改防火墙/已有服务。固定大小128byte条件标签代替原g字节，供两端原件对齐。

客户端和发送端各自记录单调时钟，没有校时，不相减推算单向延迟。取消时可分别确认client close、origin EOF与设备abort，但跨主机传播时长保留未知。当前路径自然抖动/负载不受控，保留欠载和慢样本，不以失败重跑抹掉网络不利结果。静音设备回调不是声学输出证据，重放没有模型取消。
