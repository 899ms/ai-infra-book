# sm-occupancy — 

输入：`{"accumulator_in_shared": true, "declared_latency_ns": 1000, "declared_load_bytes_per_thread": 16, "declared_mma_shape": [16, 8, 16], "declared_outstanding_loads_per_warp": 2, "declared_registers_per_thread": 128, "declared_warp_size": 32, "extra_shared_bytes": 0, "hbm_bytes_per_second": 3350000000000, "sms": 132, "threads_per_block": 256, "tile_k": 64, "tile_m": 128, "tile_n": 128}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| resident_blocks | 2 |
| resident_warps | 16 |
| occupancy | 0.25 |
| binding_limits | `["registers", "shared_memory"]` |
| shared_bytes_per_block | 98,304 |
| registers_per_thread | 128 |
| needed_bytes_in_flight_per_sm | 25,378.78787878788 |
| available_bytes_in_flight_per_sm | 16,384 |
| covers_latency | `false` |
| mma_instructions_per_tile | 512 |
| tile_flops | 2,097,152 |

计量条件：

- SM 限制取自归档的 Hopper 调优指南（每 SM 64 warp、64K 寄存器、32 个线程块、228 KB 共享内存，每块 227 KB 上限并预留 1 KB）；warp 宽度 32 为声明常量。寄存器按线程数×每线程寄存器直接相乘，不模拟分配粒度。
- 内核参数（每块线程数、每线程寄存器数、tile 形状）是声明的教学输入；96 KiB 工作集与第 4.3.2 节相同，由 gemm_tiles.account 复算。累加器放共享内存与放寄存器两种口径分别给出。
- 延迟隐藏用 Little 定律：需要在途字节 = HBM 带宽 × 声明延迟；可用在途字节 = 常驻 warp × 每 warp 未完成加载数 × 每次加载字节。延迟、未完成数与加载宽度均为声明值，未归档实测；TMA 批量拷贝不按此计。
- MMA 指令数 = tile 各维除以声明指令形状之积，与 tile FLOPs 自洽；指令形状未在归档文本中出现，为声明输入，不代表 wgmma 的实际发射方式或吞吐。

固定来源：

