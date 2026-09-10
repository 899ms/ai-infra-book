# 预登记：输入读取与检查点写入共存

M2 Max本机CPU/同一文件系统；原byte模型和文本，确定性64步训练、2个spawn DataLoader worker、prefetch2。记录读取fd调用Darwin F_NOCACHE=48，来源本机SDK sys/fcntl.h。该设置不等于测得物理设备字节，也不绕过设备自身缓存。

3轮固定seed1061，各运行none/sync/async一次，轮次顺序循环轮换；sync/async在16/32/48步相同深拷贝snapshot并使用torch.save、文件fsync、rename、目录fsync。async为同进程单后台线程，仅允许一个待完成任务，新保存前等待上一任务。训练窗口从iterator创建后至64步及保存任务全部完成；最终审计final.pt另存，不计该窗口。

记录原始worker read、父进程输入等待、更新、staging、写入完成事件和全部状态。比较实际读取与写入的重叠及窗口时间，不将重叠视作必然争用，不从小模型低强度负载推断大模型带宽。每步训练结果及最终模型/Adam/RNG/packing必须精确匹配。CPU/存储共享、单机9运行不是设备独占性能排名。
