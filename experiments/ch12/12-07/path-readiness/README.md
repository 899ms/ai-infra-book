# 12-7 两端UDP可达性

以有时限的nonce echo进程验证Mac到RTX的应用层UDP往返；SSH只负责启动peer，没有数据转发。64/512/1200/1400byte各两次，8/8回包逐字一致，RTT217.748–529.344ms，首次慢样本保留。peer在8包后主动退出，最多运行30秒。

后续路由核对发现Mac默认经过utun1024，因此这是当前系统路由下的UDP可达性，不能证明绕过TUN、裸公网RTT、UDP全部报文尺寸可用或可推广的MTU。

`python3 run.py`独立执行，需ssh rtx-pro且本地runs不存在；原始peer事件和各probe保存在runs。没有模型、GPU或C70统计。进一步实际音频见[两端变体](../audio-wan/README.md)。
