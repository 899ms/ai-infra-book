# qwen3-dense-forward — qwen3-32b

输入：`{"activation_bytes": 2, "batch": 64, "history": 32768, "kv_bytes": 2, "output_head": "last", "score_bytes": 4, "tokens": 1, "weight_bytes": 2}`

数值是分析计算；字节以 bytes 保存，FMA=2，不是硬件测量。

| 结果 | 值 |
| --- | ---: |
| parameters | 32,762,123,264 |
| weight_resident_bytes | 65,524,246,528 |
| backbone_projection_ffn_flops | 3,994,319,585,280 |
| causal_attention_matrix_flops | 4,398,180,728,832 |
| rectangular_attention_matrix_flops | 4,398,180,728,832 |
| matrix_flops | 8,492,073,091,072 |
| scalar_flops | 35,255,525,504 |
| special_ops | `{"sin": 128, "cos": 128, "rsqrt": 303168, "negate": 123731968, "exp": 8695054336, "compare_max": 8589934592, "mask_decisions": 8590196736}` |
| weight_read_once_per_operator_bytes | 63,969,077,248 |
| activation_operand_read_bytes | 619,888,018,184 |
| activation_operand_write_bytes | 69,941,903,872 |
| kv_bytes_per_token_per_request | 262,144 |
| kv_resident_before_bytes | 549,755,813,888 |
| kv_resident_after_bytes | 549,772,591,104 |
| kv_new_write_bytes | 16,777,216 |
| kv_existing_history_unique_payload_bytes | 549,755,813,888 |
| kv_attention_unique_payload_bytes | 549,772,591,104 |
| kv_logical_query_head_operand_bytes | 4,398,180,728,832 |
| attention_score_tensor_per_layer_bytes | 536,887,296 |
| materialized_scores_probabilities_io_all_layers_bytes | 137,443,147,776 |
| minimum_required_weight_and_kv_bytes | 615,296,837,632 |

每行是一次出现的成本，整模型需乘 repeats；层编号为 0 起。

| 算子 | 重复 | 输入／矩阵／输出 | 矩阵 FLOPs | 普通算术 | 权重读 bytes | 激活读 bytes | 激活写 bytes |
| --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| embedding | 1 | indices=[64, 1]；table=[151936, 5120]；output=[64, 5120] | 0 | 0 | 655,360 | 512 | 655,360 |
| rope_table | 1 | frequencies=[1, 64]；cos_sin_each=[1, 128] | 0 | 64 | 0 | 264 | 512 |
| input_layernorm | 64 | input=[64, 5120]；weight=[5120]；output=[64, 5120] | 0 | 1,310,784 | 10,240 | 655,360 | 655,360 |
| q_proj | 64 | input=[64, 5120]；weight_math=[5120, 8192]；weight_storage=[8192, 5120]；output=[64, 8192] | 5,368,709,120 | 0 | 83,886,080 | 655,360 | 1,048,576 |
| k_proj | 64 | input=[64, 5120]；weight_math=[5120, 1024]；weight_storage=[1024, 5120]；output=[64, 1024] | 671,088,640 | 0 | 10,485,760 | 655,360 | 131,072 |
| v_proj | 64 | input=[64, 5120]；weight_math=[5120, 1024]；weight_storage=[1024, 5120]；output=[64, 1024] | 671,088,640 | 0 | 10,485,760 | 655,360 | 131,072 |
| q_norm | 64 | input=[4096, 128]；weight=[128]；output=[4096, 128] | 0 | 2,101,248 | 256 | 1,048,576 | 1,048,576 |
| k_norm | 64 | input=[512, 128]；weight=[128]；output=[512, 128] | 0 | 262,656 | 256 | 131,072 | 131,072 |
| apply_rope | 64 | Q=[64, 64, 1, 128]；K=[64, 8, 1, 128] | 0 | 1,769,472 | 0 | 1,180,160 | 1,179,648 |
| kv_append | 64 | new_K_and_V_each=[64, 8, 1, 128] | 0 | 0 | 0 | 262,144 | 262,144 |
| qk | 64 | Q=[64, 64, 1, 128]；K_shared=[64, 8, 32769, 128]；scores_rectangular=[64, 64, 1, 32769] | 34,360,786,944 | 0 | 0 | 4,296,146,944 | 536,887,296 |
| score_scale_mask_softmax | 64 | scores=[64, 64, 1, 32769] | 0 | 536,883,200 | 0 | 536,887,296 | 536,887,296 |
| pv | 64 | P=[64, 64, 1, 32769]；V_shared=[64, 8, 32769, 128]；output=[64, 64, 1, 128] | 34,360,786,944 | 0 | 0 | 4,831,985,664 | 1,048,576 |
| o_proj | 64 | input=[64, 8192]；weight_math=[8192, 5120]；weight_storage=[5120, 8192]；output=[64, 5120] | 5,368,709,120 | 0 | 83,886,080 | 1,048,576 | 655,360 |
| attention_residual | 64 | inputs_each=[64, 5120]；output=[64, 5120] | 0 | 327,680 | 0 | 1,310,720 | 655,360 |
| post_attention_layernorm | 64 | input=[64, 5120]；weight=[5120]；output=[64, 5120] | 0 | 1,310,784 | 10,240 | 655,360 | 655,360 |
| gate_proj | 64 | input=[64, 5120]；weight_math=[5120, 25600]；weight_storage=[25600, 5120]；output=[64, 25600] | 16,777,216,000 | 0 | 262,144,000 | 655,360 | 3,276,800 |
| up_proj | 64 | input=[64, 5120]；weight_math=[5120, 25600]；weight_storage=[25600, 5120]；output=[64, 25600] | 16,777,216,000 | 0 | 262,144,000 | 655,360 | 3,276,800 |
| silu_mul | 64 | gate=[64, 25600]；up=[64, 25600]；output=[64, 25600] | 0 | 6,553,600 | 0 | 6,553,600 | 3,276,800 |
| down_proj | 64 | input=[64, 25600]；weight_math=[25600, 5120]；weight_storage=[5120, 25600]；output=[64, 5120] | 16,777,216,000 | 0 | 262,144,000 | 3,276,800 | 655,360 |
| ffn_residual | 64 | inputs_each=[64, 5120]；output=[64, 5120] | 0 | 327,680 | 0 | 1,310,720 | 655,360 |
| final_norm | 1 | input=[64, 5120]；weight=[5120]；output=[64, 5120] | 0 | 1,310,784 | 10,240 | 655,360 | 655,360 |
| lm_head | 1 | input=[64, 5120]；weight_math=[5120, 151936]；weight_storage=[151936, 5120]；output=[64, 151936] | 99,572,776,960 | 0 | 1,555,824,640 | 655,360 | 19,447,808 |

计量条件：

- 所有请求等长、相同位置 ID、无跨请求前缀共享，无 TP/PP；dropout=0 推理。
- 全模型权重统一 weight_bytes 的教学格式；不由 torch_dtype 推断实际量化格式。
- 每行 operator 成本为一次出现，repeats 是层数；布局视图与 GQA repeat 不额外物化。
- FMA=2；matrix_flops 是有效因果矩阵工作，scalar_flops 是声明算法的普通算术；特殊函数另列。
- operator 读写是独立算子操作数载荷，分数／概率矩形物化；不是实测 HBM、不是全图流量下界。
- 标量行内中间量视为片上；矩形注意力同时报告，FlashAttention/tile/缓存流量由执行专题另算。
- 不计采样、tokenizer、kernel launch、分配器、KV 管理索引及后端工作区；不据此声称完整 token 时间。

固定来源：

- [configs/models/qwen3-32b/config.json](https://huggingface.co/Qwen/Qwen3-32B/resolve/9216db5781bf21249d130ec9da846c4624c16137/config.json)，SHA256 `97e295b63283935788fac5e4f8860862a56d4089538cafc93f0431f2ebe483bb`。
- [sources/qwen3-32b/model.safetensors.index.json](https://huggingface.co/Qwen/Qwen3-32B/resolve/9216db5781bf21249d130ec9da846c4624c16137/model.safetensors.index.json)，SHA256 `bed42c6c55274bc08a1f616bceb3bcb84b3f02cb6584c573bd18c6519291ecd0`。
- [sources/qwen3/modeling_qwen3.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3/modeling_qwen3.py)，SHA256 `704c914530530a1acb0b443add1f520404e3ac2c28c0ab7e16f80f86cfe8ccb2`。
- [sources/qwen3/modeling_qwen3_moe.py](https://raw.githubusercontent.com/huggingface/transformers/0720e206c6ba28887e4d60ef60a6a089f6c1cc76/src/transformers/models/qwen3_moe/modeling_qwen3_moe.py)，SHA256 `3af43d01f9f902c8009b6dd7d7b8b563561b53dd0aa54175f585ae90d049fdb8`。
