# 跨模型 KV 存储与单次 decode 读取

B=1，可见长度 N=8191；所有数值为 bytes，单 token 增长列为每请求。

| 模型 / 缓存格式 | 全局增长 B/token | 全局历史 | 固定/窗口状态 | decode 主历史读 | decode index 读 | 下个 token 容量增长 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| qwen3-8b / BF16 GQA | 147,456 | 1,207,812,096 | 0 | 1,207,812,096 | 0 | 147,456 |
| qwen3-32b / BF16 GQA | 262,144 | 2,147,221,504 | 0 | 2,147,221,504 | 0 | 262,144 |
| qwen3-30b-a3b / BF16 GQA | 98,304 | 805,208,064 | 0 | 805,208,064 | 0 | 98,304 |
| qwen3-235b-a22b / BF16 GQA | 192,512 | 1,576,865,792 | 0 | 1,576,865,792 | 0 | 192,512 |
| deepseek-r1-distill-llama-70b / BF16 GQA | 327,680 | 2,684,026,880 | 0 | 2,684,026,880 | 0 | 327,680 |
| qwen3.5-397b-a17b / BF16 full KV + FP32 recurrent | 30,720 | 251,627,520 | 193,167,360 | 251,627,520 | 0 | 30,720 |
| qwen3.6-35b-a3b / BF16 full KV + FP32 recurrent | 20,480 | 167,751,680 | 64,880,640 | 167,751,680 | 0 | 20,480 |
| deepseek-v3 / BF16 compact MLA | 70,272 | 575,597,952 | 0 | 575,597,952 | 0 | 70,272 |
| kimi-k3 / BF16 compact MLA + FP32 KDA | 27,648 | 226,464,768 | 454,459,392 | 226,464,768 | 0 | 27,648 |
| kimi-k3 / BF16 expanded MLA + FP32 KDA | 1,474,560 | 12,078,120,960 | 454,459,392 | 12,078,120,960 | 0 | 1,474,560 |
| deepseek-v4-flash / BF16 reference | 6,880 | 56,313,600 | 5,636,096 | 17,936,384 | 11,004,672 | 47,360 |
| deepseek-v4-flash / FP8/BF16 main + MXFP4 index | 3,514.25 | 28,763,364 | 3,214,336 | 10,229,344 | 2,923,116 | 25,372 |
| deepseek-v4-pro / BF16 reference | 9,848 | 80,604,672 | 7,995,392 | 41,452,544 | 15,720,960 | 70,144 |
| deepseek-v4-pro / FP8/BF16 main + MXFP4 index | 5,031.4375 | 41,179,872 | 4,559,872 | 23,640,904 | 4,175,880 | 37,664 |
| deepseek-v4.1-flash / FP4 global + FP8 SWA + MXFP4 index | 890 | 7,289,456 | 2,703,360 | 8,306,688 | 3,620,320 | 1,424 |

## 固定状态与写入（均为单次 decode、全 batch）

| 模型 / 格式 | recurrent 读 | recurrent 写 | conv read-once | 新 KV / SWA 写 |
| --- | ---: | ---: | ---: | ---: |
| qwen3-8b / BF16 GQA | 0 | 0 | 0 | 147,456 |
| qwen3-32b / BF16 GQA | 0 | 0 | 0 | 262,144 |
| qwen3-30b-a3b / BF16 GQA | 0 | 0 | 0 | 98,304 |
| qwen3-235b-a22b / BF16 GQA | 0 | 0 | 0 | 192,512 |
| deepseek-r1-distill-llama-70b / BF16 GQA | 0 | 0 | 0 | 327,680 |
| qwen3.5-397b-a17b / BF16 full KV + FP32 recurrent | 188,743,680 | 188,743,680 | 4,423,680 | 30,720 |
| qwen3.6-35b-a3b / BF16 full KV + FP32 recurrent | 62,914,560 | 62,914,560 | 1,966,080 | 20,480 |
| deepseek-v3 / BF16 compact MLA | 0 | 0 | 0 | 70,272 |
| kimi-k3 / BF16 compact MLA + FP32 KDA | 434,110,464 | 434,110,464 | 20,348,928 | 27,648 |
| kimi-k3 / BF16 expanded MLA + FP32 KDA | 434,110,464 | 434,110,464 | 20,348,928 | 1,474,560 |
| deepseek-v4-flash / BF16 reference | 0 | 0 | 0 | 91,392 |
| deepseek-v4-flash / FP8/BF16 main + MXFP4 index | 0 | 0 | 0 | 50,484 |
| deepseek-v4-pro / BF16 reference | 0 | 0 | 0 | 132,608 |
| deepseek-v4-pro / FP8/BF16 main + MXFP4 index | 0 | 0 | 0 | 73,288 |
| deepseek-v4.1-flash / FP4 global + FP8 SWA + MXFP4 index | 0 | 0 | 0 | 22,544 |

## 定义与限制

- N is visible cached length for the last-position query (includes its current token); reads are a single decode query over that snapshot. Next-token growth/write refer to N→N+1. B independent equal-length requests, no prefix sharing.
- Global growth is asymptotic amortized bytes/token/request. Compression completion makes instantaneous growth discontinuous. Local windows overwrite slots after saturation, so writes are not resident growth.
- Decode main reads assume one logical fetch of each selected latent or K/V per attention layer, reused across heads and QK/PV. Index scans are additional. These are operand payloads, not measured HBM bytes: fusion, L2, tiling and cross-layer retention change physical traffic.
- Resident total here includes global history, effective SWA and declared recurrent/conv state only; not a complete runtime capacity budget. Compressor and allocator buffers, page metadata, candidate/top-k arrays, weights, workspaces and parallel copies are excluded.
- Recurrent read/write and convolution read-once payload are separate from growing history. Convolution update implementation traffic is not claimed.
- Precision/layout is part of each row. BF16 baselines and production compressed layouts are not equal-quality or equal-speed benchmark results. Models beyond their pinned context limit are explicitly skipped.
- Official V4 chart 3514 is rounded from 3514.25 B/token; V4.1 gives exactly 890 at even lengths. Their ratio is 3.9485955, not a whole-model memory or decode-speed ratio.

## 各路径说明

- qwen3-8b / BF16 GQA: 2 × layers × KV heads × head_dim × 2B; one logical K/V read per layer, no multiplier by query heads.
- qwen3-32b / BF16 GQA: 2 × layers × KV heads × head_dim × 2B; one logical K/V read per layer, no multiplier by query heads.
- qwen3-30b-a3b / BF16 GQA: 2 × layers × KV heads × head_dim × 2B; one logical K/V read per layer, no multiplier by query heads.
- qwen3-235b-a22b / BF16 GQA: 2 × layers × KV heads × head_dim × 2B; one logical K/V read per layer, no multiplier by query heads.
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
- deepseek-v4.1-flash / FP4 global + FP8 SWA + MXFP4 index: 4 KV owners, 8 indexing layers, 30 reuse layers; production candidate-limited index read (<= 16384 entries for later indexers). Per-layer logical reads count shared cache repeatedly; unique union/actual HBM unknown. Released reference scans full BF16 index before masking (13629440 B), unlike production selective read. Compressor/candidate/top-k metadata excluded.
