# kv-tiers — 

输入：`{"compute_efficiency": "1/2", "device": "a100-80gb-sxm", "gpus_per_server": 8, "hbm_bytes": 80000000000, "host_dram_bytes": 2199023255552, "model": "qwen3-8b", "mooncake_block_tokens": 512, "mooncake_lru": [[1000, "0.30"], [10000, "0.40"], [30000, "0.48"], [50000, "0.50"], [100000, "0.51"]], "nic_bytes_per_second": 25000000000, "pcie_bytes_per_second": 25000000000, "prefix_tokens": 8192, "reuse_windows_s": [10, 600], "ssd_bytes": 3840000000000, "ssd_dwpd": 1, "ssd_read_bytes_per_second": 7100000000, "ssd_write_bytes_per_second": 4200000000, "suffix_tokens": 256}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| kv_bytes_per_token | 147,456 |
| prefix_bytes | 1,207,959,552 |
| layers | 36 |
| per_layer_bytes_exact | `"33554432"` |
| weight_bytes | 16,381,470,720 |
| prefill_prefix_s_exact | `"326158016/380859375"` |
| warm_suffix_s_exact | `"293812928/9521484375"` |
| kv_production_bytes_per_second_exact | `"7188480000000000/5096219"` |
| hbm_kv_bytes | 63,618,529,280 |
| dram_per_gpu_bytes | `"274877906944"` |
| prefetch_window_prefixes | 227 |
| ssd_endurance_bytes_per_second_exact | `"400000000/9"` |
| ssd_write_over_endurance_exact | `"161740800/5096219"` |
| ssd_admissible_fraction_exact | `"5096219/161740800"` |
| ssd_write_bandwidth_fraction_exact | `"11980800/35673533"` |
| dram_write_bandwidth_fraction_exact | `"1437696/25481095"` |

| 层 | 容量 bytes | 保留 s | 读 8K 前缀 ms | 写 ms | 串行 ms | 逐层流水 ms | 全部重叠需预载层数 | 盖住读取的最少新 token |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| HBM | 63618529280 | 45.1 | 0.0 | 0.0 | — | — | — | — |
| host DRAM | 274877906944 | 194.9 | 48.3 | 48.3 | 79.2 | 49.2 | 14 | 400 |
| local NVMe | 3840000000000 | 2722.3 | 170.1 | 287.6 | 201.0 | 171.0 | 30 | 1388 |
| remote pool | — | — | 96.6 | 96.6 | 127.5 | 97.5 | 25 | 796 |

| 复用窗口 s | 所需容量 bytes |
| ---: | ---: |
| 10 | 1.411e+10 |
| 600 | 8.463e+11 |

| Mooncake 块数 | token | Qwen3-8B KV bytes | LRU 命中率 |
| ---: | ---: | ---: | ---: |
| 1000 | 512000 | 75497472000 | 0.30 |
| 10000 | 5120000 | 754974720000 | 0.40 |
| 30000 | 15360000 | 2264924160000 | 0.48 |
| 50000 | 25600000 | 3774873600000 | 0.50 |
| 100000 | 51200000 | 7549747200000 | 0.51 |

计量条件：

- 每卡一份：DGX A100 的 2 TB DIMM 按 8 张 GPU 均分（按二进制 TiB 计），每卡一块 3.84 TB U.2 NVMe 与一张 200 Gb/s 网卡。HBM 容量按厂商 80 GB 十进制计并扣除 BF16 权重，未扣激活与工作区，是 KV 可用空间的上限。
- NVMe 读写带宽与耐久度取 Solidigm D7-P5520 3.84 TB 产品简介的最大值；路径时间只受盘本身限制，不计文件系统与 PCIe 争用。
- KV 产生率 = 一张 GPU 连续执行无命中 8192-token prefill 时每秒产生的 KV 字节；保留时间 = 容量 / 产生率，对应只按时间先后淘汰、全部写入该层的情形。
- 远端池整份先经网卡到主机再经 PCIe 到 GPU，两段串行；逐层预加载按总读取时间均分到各层。
- 逐层计算时间按命中后 suffix 的矩阵 FLOPs 均分到各层；预加载层数 k 指计算开始前已在 HBM 的层数。
- Mooncake 表 1 的块数按每块 512 token 换算为 Qwen3-8B 的 KV 字节；命中率属于该一小时采样 trace，容量随真实流量同比例放大。

固定来源：

- [references/files/specs/nvidia-dgx-a100-datasheet.pdf](https://images.nvidia.com/aem-dam/Solutions/Data-Center/nvidia-dgx-a100-datasheet.pdf)，SHA256 `183a3a104c36807f6bc9b1a6c705fcaa5825a25c3978043e89eeb22149edbdfd`。
- [references/files/specs/solidigm-d7-p5520-brief.pdf](https://www.solidigm.com/content/dam/solidigm/en/site/products/data-center/product-briefs/d7-p5520-p5620-product-brief/documents/d7-p5520-p5620-product-brief.pdf)，SHA256 `71e7b908c4a7d2bee23fd5abc6afbc4ccfb8f258823aa530343e04f7539b0b85`。
- [references/files/papers/cachedattention.pdf](https://www.usenix.org/system/files/atc24-gao-bin-cost.pdf)，SHA256 `5c5bd05811c38652883a3483e4d5a0bd936bc190571621830648acea90755d1a`。
- [references/files/papers/kvcache-in-the-wild.pdf](https://arxiv.org/pdf/2506.02634)，SHA256 `f54f033a1f62293ac662b44e2e51c68306157756cf20a2f951342d6cdeccee54`。
- [references/files/papers/mooncake.pdf](https://arxiv.org/pdf/2407.00079)，SHA256 `af8db47ba2ccbbd7ca3f46de6176292010192afb0ffe5c51da2db56e1006f27a`。
