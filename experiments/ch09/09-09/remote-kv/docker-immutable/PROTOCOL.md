# 同机Docker网络存储控制

本控制使用相同1024输入、16输出与单页HTTP后端，GPU引擎与独立Docker存储进程均在rtx-pro。通过127.0.0.1 TCP实际传输，容器1CPU/512MiB，无GPU、非privileged，使用已缓存python3.11-slim固定image ID。不把此结果称为跨机器或WAN测试；Mac链路上001至004失败记录独立保留。生产者正常退出、新引擎从独立容器页文件读取后，才核验storage命中、完整输出及逐页SHA。运行期容器文件证据保存在rtx-pro，Mac仅取回日志和元数据，非原始全部页镜像。

独立immutable控制：先前严格重复键字节相等策略在消费者成功取回后拒绝一次重写。此控制沿用原生HiCacheFile的已存在键保留首值语义，记录incoming/stored SHA，并将不同内容保存在collisions子目录，既不覆写首值，也不隐去差异。模型、输入、输出一致性和传输SHA门槛保持；不能将输出一致写成KV逐位一致。与严格策略是独立对照，不覆盖其失败。
