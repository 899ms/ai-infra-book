# pd-pool — 

输入：`{"arrival_requests_per_second": "4", "cached_prefix_tokens": 0, "kv_layout": "gqa", "kv_model": "deepseek-v3", "model": "qwen3-8b", "network_bytes_per_second": 25000000000, "output_tokens": 1025, "prompt_tokens": 8192, "workers": [{"bandwidth_efficiency": 0.5, "compute_efficiency": 0.5, "count": 4, "decode_batch": 32, "device": "a100-80gb-sxm", "name": "A100"}, {"bandwidth_efficiency": 0.5, "compute_efficiency": 0.5, "count": 4, "decode_batch": 32, "device": "h20-sxm5-96gb", "name": "H20"}]}`

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
| assignments | 25 |
| best_prefill_workers | `{"A100": 4, "H20": 0}` |
| best_decode_workers | `{"A100": 0, "H20": 4}` |
| best_pd_bound_requests_per_second_exact | `"125000000/27447469"` |
| colocated_bound_requests_per_second_exact | `"23814473165145361328125/7894003424232391199952"` |
| pd_to_colocated_bound_ratio_exact | `"505216219150873036796928/334667271143249503000325"` |
| best_bottlenecks | `["decode"]` |
| arrival_strictly_below_best_pd_bound | `true` |
| arrival_strictly_below_colocated_bound | `false` |

| worker类型 | 副本数 | 每请求P资源秒 | 每请求D资源秒 | 单副本共置请求/s |
| --- | ---: | --- | --- | --- |
| A100 | 4 | 326158016/380859375 | 7026552064/3982421875 | 776572265625/2035213847104 |
| H20 | 4 | 652316032/361328125 | 27447469/31250000 | 5781250000/15514838277 |

| P分配 | D分配 | P请求/s | D请求/s | 联合上界请求/s | 限制资源 | 到达率严格低于上界 |
| --- | --- | --- | --- | --- | --- | --- |
| {'A100': 0, 'H20': 0} | {'A100': 4, 'H20': 4} | 0 | 11982421875/1756638016 | 0 | ['prefill'] | False |
| {'A100': 0, 'H20': 1} | {'A100': 4, 'H20': 3} | 361328125/652316032 | 9982421875/1756638016 | 361328125/652316032 | ['prefill'] | False |
| {'A100': 0, 'H20': 2} | {'A100': 4, 'H20': 2} | 361328125/326158016 | 7982421875/1756638016 | 361328125/326158016 | ['prefill'] | False |
| {'A100': 0, 'H20': 3} | {'A100': 4, 'H20': 1} | 1083984375/652316032 | 5982421875/1756638016 | 1083984375/652316032 | ['prefill'] | False |
| {'A100': 0, 'H20': 4} | {'A100': 4, 'H20': 0} | 361328125/163079008 | 3982421875/1756638016 | 361328125/163079008 | ['prefill'] | False |
| {'A100': 1, 'H20': 0} | {'A100': 3, 'H20': 4} | 380859375/326158016 | 43947265625/7026552064 | 380859375/326158016 | ['prefill'] | False |
| {'A100': 1, 'H20': 1} | {'A100': 3, 'H20': 3} | 1123046875/652316032 | 35947265625/7026552064 | 1123046875/652316032 | ['prefill'] | False |
| {'A100': 1, 'H20': 2} | {'A100': 3, 'H20': 2} | 185546875/81539504 | 27947265625/7026552064 | 185546875/81539504 | ['prefill'] | False |
| {'A100': 1, 'H20': 3} | {'A100': 3, 'H20': 1} | 1845703125/652316032 | 2849609375/1003793152 | 1845703125/652316032 | ['prefill'] | False |
| {'A100': 1, 'H20': 4} | {'A100': 3, 'H20': 0} | 1103515625/326158016 | 11947265625/7026552064 | 11947265625/7026552064 | ['decode'] | False |
| {'A100': 2, 'H20': 0} | {'A100': 2, 'H20': 4} | 380859375/163079008 | 19982421875/3513276032 | 380859375/163079008 | ['prefill'] | False |
| {'A100': 2, 'H20': 1} | {'A100': 2, 'H20': 3} | 1884765625/652316032 | 2283203125/501896576 | 1884765625/652316032 | ['prefill'] | False |
| {'A100': 2, 'H20': 2} | {'A100': 2, 'H20': 2} | 1123046875/326158016 | 11982421875/3513276032 | 11982421875/3513276032 | ['decode'] | False |
| {'A100': 2, 'H20': 3} | {'A100': 2, 'H20': 1} | 2607421875/652316032 | 7982421875/3513276032 | 7982421875/3513276032 | ['decode'] | False |
| {'A100': 2, 'H20': 4} | {'A100': 2, 'H20': 0} | 185546875/40769752 | 3982421875/3513276032 | 3982421875/3513276032 | ['decode'] | False |
| {'A100': 3, 'H20': 0} | {'A100': 1, 'H20': 4} | 1142578125/326158016 | 35982421875/7026552064 | 1142578125/326158016 | ['prefill'] | False |
| {'A100': 3, 'H20': 1} | {'A100': 1, 'H20': 3} | 2646484375/652316032 | 27982421875/7026552064 | 27982421875/7026552064 | ['decode'] | False |
| {'A100': 3, 'H20': 2} | {'A100': 1, 'H20': 2} | 751953125/163079008 | 19982421875/7026552064 | 19982421875/7026552064 | ['decode'] | False |
| {'A100': 3, 'H20': 3} | {'A100': 1, 'H20': 1} | 3369140625/652316032 | 11982421875/7026552064 | 11982421875/7026552064 | ['decode'] | False |
| {'A100': 3, 'H20': 4} | {'A100': 1, 'H20': 0} | 1865234375/326158016 | 3982421875/7026552064 | 3982421875/7026552064 | ['decode'] | False |
| {'A100': 4, 'H20': 0} | {'A100': 0, 'H20': 4} | 380859375/81539504 | 125000000/27447469 | 125000000/27447469 | ['decode'] | True |
| {'A100': 4, 'H20': 1} | {'A100': 0, 'H20': 3} | 3408203125/652316032 | 93750000/27447469 | 93750000/27447469 | ['decode'] | False |
| {'A100': 4, 'H20': 2} | {'A100': 0, 'H20': 2} | 1884765625/326158016 | 62500000/27447469 | 62500000/27447469 | ['decode'] | False |
| {'A100': 4, 'H20': 3} | {'A100': 0, 'H20': 1} | 4130859375/652316032 | 31250000/27447469 | 31250000/27447469 | ['decode'] | False |
| {'A100': 4, 'H20': 4} | {'A100': 0, 'H20': 0} | 1123046875/163079008 | 0 | 0 | ['decode'] | False |

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
- [sources/hardware/nvidia-h20-vgpu-release7.md](https://docs.nvidia.com/ai-enterprise/release-7/latest/infra-software/vgpu/reference/hopper.html)，SHA256 `c1bc1f43b221a4e7c3d2fb7fd3e1998bc3a74412ad634f7be40e3461fe9f5d86`。
- [../references/files/specs/nvidia-h20-spec-sheet.pdf](https://flopper.io/gpu/nvidia-h20-96gb/spec-sheet.pdf)，SHA256 `10066ce28de21151385fc05110af461ccce6a2ea73a0b3322efe5a47e67ce1e5`。
- [../references/outline-checks/2026-09-07/execution-feedback/megascale-infer.pdf](https://arxiv.org/pdf/2504.02263v1)，SHA256 `3596ecc1eda339b0e33e3f3de5d4910b42f1aeb2e880c68b405a59678a66f403`。
