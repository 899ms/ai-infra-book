# 跨模型 KV 存储与单次 decode 读取

B=1，可见长度 N=131072；所有数值为 bytes，单 token 增长列为每请求。

| 模型 / 缓存格式 | 全局增长 B/token | 全局历史 | 固定/窗口状态 | decode 主历史读 | decode index 读 | 下个 token 容量增长 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| deepseek-r1-distill-llama-70b / BF16 GQA | 327,680 | 42,949,672,960 | 0 | 42,949,672,960 | 0 | 327,680 |
| qwen3.5-397b-a17b / BF16 full KV + FP32 recurrent | 30,720 | 4,026,531,840 | 193,167,360 | 4,026,531,840 | 0 | 30,720 |
| qwen3.6-35b-a3b / BF16 full KV + FP32 recurrent | 20,480 | 2,684,354,560 | 64,880,640 | 2,684,354,560 | 0 | 20,480 |
| deepseek-v3 / BF16 compact MLA | 70,272 | 9,210,691,584 | 0 | 9,210,691,584 | 0 | 70,272 |
| kimi-k3 / BF16 compact MLA + FP32 KDA | 27,648 | 3,623,878,656 | 454,459,392 | 3,623,878,656 | 0 | 27,648 |
| kimi-k3 / BF16 expanded MLA + FP32 KDA | 1,474,560 | 193,273,528,320 | 454,459,392 | 193,273,528,320 | 0 | 1,474,560 |
| deepseek-v4-flash / BF16 reference | 6,880 | 901,775,360 | 5,636,096 | 37,617,664 | 176,160,768 | 0 |
| deepseek-v4-flash / FP8/BF16 main + MXFP4 index | 3,514.25 | 460,619,776 | 3,214,336 | 21,453,824 | 46,792,704 | 0 |
| deepseek-v4-pro / BF16 reference | 9,848 | 1,290,797,056 | 7,995,392 | 71,958,528 | 251,658,240 | 0 |
| deepseek-v4-pro / FP8/BF16 main + MXFP4 index | 5,031.4375 | 659,480,576 | 4,559,872 | 41,038,848 | 66,846,720 | 0 |
| deepseek-v4.1-flash / FP4 global + FP8 SWA + MXFP4 index | 890 | 116,654,080 | 2,703,360 | 8,306,688 | 26,738,688 | 356 |

## 固定状态与写入（均为单次 decode、全 batch）

| 模型 / 格式 | recurrent 读 | recurrent 写 | conv read-once | 新 KV / SWA 写 |
| --- | ---: | ---: | ---: | ---: |
| deepseek-r1-distill-llama-70b / BF16 GQA | 0 | 0 | 0 | 327,680 |
| qwen3.5-397b-a17b / BF16 full KV + FP32 recurrent | 188,743,680 | 188,743,680 | 4,423,680 | 30,720 |
| qwen3.6-35b-a3b / BF16 full KV + FP32 recurrent | 62,914,560 | 62,914,560 | 1,966,080 | 20,480 |
| deepseek-v3 / BF16 compact MLA | 0 | 0 | 0 | 70,272 |
| kimi-k3 / BF16 compact MLA + FP32 KDA | 434,110,464 | 434,110,464 | 20,348,928 | 27,648 |
| kimi-k3 / BF16 expanded MLA + FP32 KDA | 434,110,464 | 434,110,464 | 20,348,928 | 1,474,560 |
| deepseek-v4-flash / BF16 reference | 0 | 0 | 0 | 44,032 |
| deepseek-v4-flash / FP8/BF16 main + MXFP4 index | 0 | 0 | 0 | 25,112 |
| deepseek-v4-pro / BF16 reference | 0 | 0 | 0 | 62,464 |
| deepseek-v4-pro / FP8/BF16 main + MXFP4 index | 0 | 0 | 0 | 35,624 |
| deepseek-v4.1-flash / FP4 global + FP8 SWA + MXFP4 index | 0 | 0 | 0 | 21,476 |

## 定义与限制

- N is visible cached length for the last-position query (includes its current token); reads are a single decode query over that snapshot. Next-token growth/write refer to N→N+1. B independent equal-length requests, no prefix sharing.
- Global growth is asymptotic amortized bytes/token/request. Compression completion makes instantaneous growth discontinuous. Local windows overwrite slots after saturation, so writes are not resident growth.
- Decode main reads assume one logical fetch of each selected latent or K/V per attention layer, reused across heads and QK/PV. Index scans are additional. These are operand payloads, not measured HBM bytes: fusion, L2, tiling and cross-layer retention change physical traffic.
- Resident total here includes global history, effective SWA and declared recurrent/conv state only; not a complete runtime capacity budget. Compressor and allocator buffers, page metadata, candidate/top-k arrays, weights, workspaces and parallel copies are excluded.
- Recurrent read/write and convolution read-once payload are separate from growing history. Convolution update implementation traffic is not claimed.
- Precision/layout is part of each row. BF16 baselines and production compressed layouts are not equal-quality or equal-speed benchmark results. Models beyond their pinned context limit are explicitly skipped.
- Official V4 chart 3514 is rounded from 3514.25 B/token; V4.1 gives exactly 890 at even lengths. Their ratio is 3.9485955, not a whole-model memory or decode-speed ratio.

## 各路径说明

- deepseek-r1-distill-llama-70b / BF16 GQA: 2 × layers × KV heads × head_dim × 2B; one logical K/V read per layer, no multiplier by query heads.
- qwen3.5-397b-a17b / BF16 full KV + FP32 recurrent: 15 full-attention / 45 linear layers. Linear recurrence is fixed state, read and written each step; BF16 convolution slots counted separately, implementation movement not inferred.
- qwen3.6-35b-a3b / BF16 full KV + FP32 recurrent: 10 full-attention / 30 linear layers. Linear recurrence is fixed state, read and written each step; BF16 convolution slots counted separately, implementation movement not inferred.
- deepseek-v3 / BF16 compact MLA: Declared absorbed MLA layout; latent and RoPE stored once, not expanded K/V. No DSA indexer in V3.
- kimi-k3 / BF16 compact MLA + FP32 KDA: 24 MLA + 69 KDA; compact is declared absorbed execution, expanded matches pinned HF cache. KDA fixed state and short convolution must not be described as per-token-growing KV.
- kimi-k3 / BF16 expanded MLA + FP32 KDA: 24 MLA + 69 KDA; compact is declared absorbed execution, expanded matches pinned HF cache. KDA fixed state and short convolution must not be described as per-token-growing KV.
- deepseek-v4-flash / BF16 reference: CSA top-k main read plus full index scan; HCA reads all compressed entries. Shared latent counted once per attention layer for QK/PV. Compressor buffers/updates excluded. Production main 584B includes scale padding; reference is BF16.
- deepseek-v4-flash / FP8/BF16 main + MXFP4 index: CSA top-k main read plus full index scan; HCA reads all compressed entries. Shared latent counted once per attention layer for QK/PV. Compressor buffers/updates excluded. Production main 584B includes scale padding; reference is BF16.
- deepseek-v4-pro / BF16 reference: CSA top-k main read plus full index scan; HCA reads all compressed entries. Shared latent counted once per attention layer for QK/PV. Compressor buffers/updates excluded. Production main 584B includes scale padding; reference is BF16.
- deepseek-v4-pro / FP8/BF16 main + MXFP4 index: CSA top-k main read plus full index scan; HCA reads all compressed entries. Shared latent counted once per attention layer for QK/PV. Compressor buffers/updates excluded. Production main 584B includes scale padding; reference is BF16.
- deepseek-v4.1-flash / FP4 global + FP8 SWA + MXFP4 index: 4 KV owners, 8 indexing layers, 30 reuse layers; production candidate-limited index read (<= 16384 entries for later indexers). Per-layer logical reads count shared cache repeatedly; unique union/actual HBM unknown. Released reference scans full BF16 index before masking (218103808 B), unlike production selective read. Compressor/candidate/top-k metadata excluded.

跳过超出配置上下文上限的模型：qwen3-8b, qwen3-32b, qwen3-30b-a3b, qwen3-235b-a22b
