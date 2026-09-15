# 同机Docker网络存储控制

本控制使用相同1024输入、16输出与单页HTTP后端，GPU引擎与独立Docker存储进程均在rtx-pro。通过127.0.0.1 TCP实际传输，容器1CPU/512MiB，无GPU、非privileged，使用已缓存python3.11-slim固定image ID。不把此结果称为跨机器或WAN测试；Mac链路上001至004失败记录独立保留。生产者正常退出、新引擎从独立容器页文件读取后，才核验storage命中、完整输出及逐页SHA。运行期容器文件证据保存在rtx-pro，Mac仅取回日志和元数据，非原始全部页镜像。
