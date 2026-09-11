# iteration-batching — 

输入：`{"chunk_tokens": 2048, "kv_capacity_bytes": null, "max_sequences": 2, "model": "qwen3-8b", "per_causal_pair_ns": 3, "per_new_token_ns": 30400, "policy": "continuous", "requests": [{"arrival_ns": 0, "id": "r0", "output_tokens": 8, "prompt_tokens": 2048}, {"arrival_ns": 0, "id": "r1", "output_tokens": 2, "prompt_tokens": 2048}, {"arrival_ns": 20000000, "id": "r2", "output_tokens": 2, "prompt_tokens": 8192}, {"arrival_ns": 30000000, "id": "r3", "output_tokens": 4, "prompt_tokens": 2048}], "step_base_ns": 26220000, "token_budget": 4096}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| requests | 4 |
| iterations | 8 |
| finish_ns | 765,590,636 |
| total_output_tokens | 16 |
| total_scheduled_tokens | 14,348 |
| total_matrix_flops | 222,860,086,083,584 |
| peak_live_kv_bytes | 1,510,539,264 |
| peak_reserved_kv_bytes | 1,511,129,088 |
| live_kv_byte_ns | 827,138,281,762,455,552 |
| max_waiting_ns | 561,901,016 |
| max_ttft_ns | 656,711,300 |
| max_itl_ns | 375,968,934 |

| 请求 | 准入ns | TTFT ns | 完成ns | 最大ITL ns | 矩阵FLOPs |
| --- | ---: | ---: | ---: | --- | ---: |
| r0 | 0 | 163327456 | 765590636 | 375968934 | 29803088183296 |
| r1 | 0 | 163327456 | 189620550 | 26293094 | 29705007333376 |
| r2 | 189620550 | 545589484 | 591901016 | 26311532 | 133614291976192 |
| r3 | 591901016 | 656711300 | 765590636 | 26293118 | 29737698590720 |

| 步开始ns | 步结束ns | 新token | 有效配对 | 步内KV bytes | 请求／阶段／新token |
| ---: | ---: | ---: | ---: | ---: | --- |
| 0 | 163327456 | 4096 | 4196352 | 603979776 | r0:prefill:2048, r1:prefill:2048 |
| 163327456 | 189620550 | 2 | 4098 | 604274688 | r0:decode:1, r1:decode:1 |
| 189620550 | 565589484 | 8193 | 33560578 | 1510244352 | r0:decode:1, r2:prefill:8192 |
| 565589484 | 591901016 | 2 | 10244 | 1510539264 | r0:decode:1, r2:decode:1 |
| 591901016 | 686711300 | 2049 | 2100228 | 604569600 | r0:decode:1, r3:prefill:2048 |
| 686711300 | 713004406 | 2 | 4102 | 604864512 | r0:decode:1, r3:decode:1 |
| 713004406 | 739297518 | 2 | 4104 | 605159424 | r0:decode:1, r3:decode:1 |
| 739297518 | 765590636 | 2 | 4106 | 605454336 | r0:decode:1, r3:decode:1 |

计量条件：

- 同一教学请求流：固定批次只在整组退出后补位，连续批处理每个迭代边界补位，两者prefill一次处理完整prompt；chunked在相同连续补位上按decode优先、FIFO prefill分配token预算与单请求块上限。
- 只在迭代边界接纳已到达请求；固定批次不额外等待凑满。每个请求先完成prefill产生首输出，后续输出各消耗一个pending token。最新输出尚未写入KV，最终计算长度为prompt+output-1。
- 每步时长为base+new_tokens*per_new_token_ns+有效因果配对*per_causal_pair_ns，全部显式教学成本，跨请求相加后一次base；它不是实测拟合或硬件峰值预测。官方矩阵另计，非末prefill块不做输出头。
- KV准入按声明最大输出长度预留，严格FIFO不绕过队首；逻辑KV按每步开始分配该步全部新增行、步末完成请求释放。只计KV池，不含权重、页碎片或工作区；无抢占、共享前缀或动态EOS。
- 时间戳是调度模型交付时刻，不模拟HTTP或流式聚合；相同输出数量不证明生成内容或质量一致。maxITL仅对至少两输出请求定义。

固定来源：

- [configs/models/qwen3-8b/config.json](https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/config.json)，SHA256 `f7c4eadfbbf522470667b797a3c89be2524832d2d599797248dc304fff447c30`。
- [sources/qwen3-8b/model.safetensors.index.json](https://huggingface.co/Qwen/Qwen3-8B/resolve/b968826d9c46dd6066d109eabc6255188de91218/model.safetensors.index.json)，SHA256 `f9fdbcb91c23971c13ec5d5f2573d2349e8f61f2f049371ec699281748fdb1bc`。
- [sources/qwen3/modeling_qwen3.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py)，SHA256 `704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2`。
- [sources/qwen3/modeling_qwen3_moe.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py)，SHA256 `3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8`。
