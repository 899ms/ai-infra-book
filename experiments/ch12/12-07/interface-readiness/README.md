# 12-7 物理接口与默认路径探测

Darwin IPv4 socket设置IP_BOUND_IF=25，绑定en0并getsockopt读回索引14；默认socket读回0。bound/default/default/bound四轮，每轮64/1200byte，8/8收到一致echo。绑定RTT196.267–235.537ms，默认290.528–741.603ms；两组RTX观察到的来源IP哈希不同。仅描述此8包，不推断总体性能。

`python3 run.py`独立执行，需ssh rtx-pro与本地runs不存在。限时nonce peer自动退出；SSH只控制启动，probe数据走应用UDP。没有改系统路由或防火墙，没有启动GPU任务。源代码、回包校验和两种路由原件在本目录。进一步[音频接口绑定实跑](../audio-physical/README.md)用RTX来源观测核对实际应用路径。
