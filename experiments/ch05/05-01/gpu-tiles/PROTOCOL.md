# 5-1 GPU分块：执行前固定协议

固定Qwen3 FFN单支投影维度K4096/N12288，M1与1024，BF16随机控制操作数、FP32累加/BF16输出。不是训练权重或模型质量。三个(BM,BN,BK,warps)=(32,64,32,4)/(64,64,32,4)/(128,128,32,8)，均num_stages2；第三组同时改变warps，不单独归因于块边长。

所有候选与同一完整FP64 GEMM参考比较：相对L2<0.5%，每元素abs误差≤0.05+0.01*abs(reference)。失败的数值结果是科学负结果，保留；不调阈值求通过。输入、输出、参考张量保存，可独立复核。

首次调用含编译/缓存/模块载入，不当纯编译时间。五次预热，九轮随机顺序，每候选20次连续launch，CUDA事件时间除20；包含提交不及时的设备空闲，不是纯内核时间。共享GPU、未锁频、固定重复缓冲，不作稳定性能排行。

六种形状/配置分别NCU采集一次预热后真实GEMM：DRAM读/写、L2字节、执行时间与实际活跃warp比例。kernel replay、cache-control none、clock-control none，不当冷缓存、隔离计时或单独算术下界。RTX为GDDR显存，DRAM指标不能叫实测HBM。

保留真实编译TTIR/TTGIR/PTX/cubin、寄存器、shared memory及spills；不把源码中块容量代替编译分配，不把单kernel活跃warp当多租户并发。访问计数/容量枚举仍由calculations负责，独立目录不读写该任务。
