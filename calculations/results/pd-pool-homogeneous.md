# pd-pool — 

输入：`{"arrival_requests_per_second": "4", "cached_prefix_tokens": 0, "kv_layout": "gqa", "kv_model": "deepseek-v3", "model": "qwen3-8b", "network_bytes_per_second": 25000000000, "output_tokens": 1025, "prompt_tokens": 8192, "workers": [{"bandwidth_efficiency": 0.5, "compute_efficiency": 0.5, "count": 8, "decode_batch": 32, "device": "a100-80gb-sxm", "name": "A100"}]}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| new_prefill_tokens_per_request | 8,192 |
| decode_calls_per_request | 1,024 |
| kv_layout | `"gqa"` |
| kv_bytes_per_token | 147,456 |
| full_prompt_state_bytes | 1,207,959,552 |
| pd_transfer_bytes_per_request | 1,207,959,552 |
| network_capacity_requests_per_second_exact | `"48828125/2359296"` |
| assignments | 9 |
| best_prefill_workers | `{"A100": 3}` |
| best_decode_workers | `{"A100": 5}` |
| best_pd_bound_requests_per_second_exact | `"19912109375/7026552064"` |
| colocated_bound_requests_per_second_exact | `"776572265625/254401730888"` |
| pd_to_colocated_bound_ratio_exact | `"31800216361/34254441312"` |
| best_bottlenecks | `["decode"]` |
| arrival_strictly_below_best_pd_bound | `false` |
| arrival_strictly_below_colocated_bound | `false` |

| worker类型 | 副本数 | 每请求P资源秒 | 每请求D资源秒 | 单副本共置请求/s |
| --- | ---: | --- | --- | --- |
| A100 | 8 | 326158016/380859375 | 7026552064/3982421875 | 776572265625/2035213847104 |

| P分配 | D分配 | P请求/s | D请求/s | 联合上界请求/s | 限制资源 | 到达率严格低于上界 |
| --- | --- | --- | --- | --- | --- | --- |
| {'A100': 0} | {'A100': 8} | 0 | 3982421875/878319008 | 0 | ['prefill'] | False |
| {'A100': 1} | {'A100': 7} | 380859375/326158016 | 3982421875/1003793152 | 380859375/326158016 | ['prefill'] | False |
| {'A100': 2} | {'A100': 6} | 380859375/163079008 | 11947265625/3513276032 | 380859375/163079008 | ['prefill'] | False |
| {'A100': 3} | {'A100': 5} | 1142578125/326158016 | 19912109375/7026552064 | 19912109375/7026552064 | ['decode'] | False |
| {'A100': 4} | {'A100': 4} | 380859375/81539504 | 3982421875/1756638016 | 3982421875/1756638016 | ['decode'] | False |
| {'A100': 5} | {'A100': 3} | 1904296875/326158016 | 11947265625/7026552064 | 11947265625/7026552064 | ['decode'] | False |
| {'A100': 6} | {'A100': 2} | 1142578125/163079008 | 3982421875/3513276032 | 3982421875/3513276032 | ['decode'] | False |
| {'A100': 7} | {'A100': 1} | 2666015625/326158016 | 3982421875/7026552064 | 3982421875/7026552064 | ['decode'] | False |
| {'A100': 8} | {'A100': 0} | 380859375/40769752 | 0 | 0 | ['decode'] | False |

计量条件：

- 每个worker代表已能容纳该完整模型与所需KV的独立服务副本。device形式的worker按hardware.json锁定的官方峰值乘以声明效率，用模型forward账推出两阶段服务时间；显式token/s形式则直接采用给定的有效能力。
- 输入阶段token/s必须对应相同模型、精度、上下文、batch和质量条件下的有效服务能力。prefill按新处理token数，decode按调用次数；prefill最后logits产生首输出，所以G输出需要G-1次decode。
- 每个worker固定分配P或D，池内允许理想流量分配；独立资源容量取min，异构副本的请求/s先相加。共置每副本先加两个阶段的资源秒再取倒数，假定阶段共享资源且无额外混跑惩罚。
- 这是给定服务能力的稳态上界。没有请求排队、时变负载、启动同步、流水填充、transfer窗口限制、SLO、能耗或费用，不能把低于上界视为稳定性或尾延迟保证。
- P已命中前缀仅减少其新token工作；假设D冷缓存，仍交接完整prompt状态。跨长度复用相同token/s只是一项教学敏感性假设，实际需重新校准。
- KV使用state模块的默认BF16与模型状态约定，不含格式转换、分片复制、路由元数据或双端temporary。网络给共享有效单向payload带宽上界，收发不重复相加。
- 仅一个输出时不需要D调用或KV交接，最优把全部worker给P；多输出时要求两个池都有正能力。到达率恰等容量不标为严格低于，余量也不代替SLO证据。
- 枚举内最大值只对当前整数候选与假设成立；同值选输入顺序中的首项，不是唯一配比或真实系统最优。
- kv_layout=mla 时，交接状态按锁定 DeepSeek-V3 config 的紧凑 MLA 每 token 字节（层数×(d_c+d_r)×2 B）乘相同 prompt 长度；其余阶段速率与模型不变，只比较交接字节的影响。

固定来源：

- [configs/models/qwen3-8b/config.json](https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/config.json)，SHA256 `f7c4eadfbbf522470667b797a3c89be2524832d2d599797248dc304fff447c30`。
- [sources/qwen3-8b/model.safetensors.index.json](https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/model.safetensors.index.json)，SHA256 `f9fdbcb91c23971c13ec5d5f2573d2349e8f61f2f049371ec699281748fdb1bc`。
- [sources/qwen3/modeling_qwen3.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py)，SHA256 `704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2`。
- [sources/qwen3/modeling_qwen3_moe.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py)，SHA256 `3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8`。
- [sources/hardware/nvidia-a100-page.md](https://www.nvidia.com/en-us/data-center/a100/)，SHA256 `826e119ab5590b37d6a031e9212684c9d3090a813433a248ea4ca96aa14430ed`。
- [../references/files/specs/nvidia-a100.pdf](https://images.nvidia.com/aem-dam/en-zz/Solutions/data-center/nvidia-ampere-architecture-whitepaper.pdf)，SHA256 `3a800ad7668ec37037fa5870a8e3bb681b75f19668b3d11492ab9b0da0d58815`。
- [sources/hardware/nvidia-ptx-isa-9-3.md](https://docs.nvidia.com/cuda/parallel-thread-execution/index.html)，SHA256 `0d921e5e90e12dcd5af70a68404ced5c47beeed5aaf54c8ec0caeddcfefff6a7`。
