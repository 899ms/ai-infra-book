# 跨模型 KV 存储与单次 decode 读取

B=1，可见长度 N=1048576；所有数值为 bytes，单 token 增长列为每请求。

| 模型 / 缓存格式 | 全局增长 B/token | 全局历史 | 固定/窗口状态 | decode 主历史读 | decode index 读 | 下个 token 容量增长 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| kimi-k3 / BF16 compact MLA + FP32 KDA | 27,648 | 28,991,029,248 | 454,459,392 | 28,991,029,248 | 0 | 27,648 |
| kimi-k3 / BF16 expanded MLA + FP32 KDA | 1,474,560 | 1,546,188,226,560 | 454,459,392 | 1,546,188,226,560 | 0 | 1,474,560 |
| deepseek-v4-flash / BF16 reference | 6,880 | 7,214,202,880 | 5,636,096 | 184,418,304 | 1,409,286,144 | 0 |
| deepseek-v4-flash / FP8/BF16 main + MXFP4 index | 3,514.25 | 3,684,958,208 | 3,214,336 | 105,176,064 | 374,341,632 | 0 |
| deepseek-v4-pro / BF16 reference | 9,848 | 10,326,376,448 | 7,995,392 | 299,499,520 | 2,013,265,920 | 0 |
| deepseek-v4-pro / FP8/BF16 main + MXFP4 index | 5,031.4375 | 5,275,844,608 | 4,559,872 | 170,808,320 | 534,773,760 | 0 |
| deepseek-v4.1-flash / FP4 global + FP8 SWA + MXFP4 index | 890 | 933,232,640 | 2,703,360 | 8,306,688 | 182,714,368 | 356 |

## 固定状态与写入（均为单次 decode、全 batch）

| 模型 / 格式 | recurrent 读 | recurrent 写 | conv read-once | 新 KV / SWA 写 |
| --- | ---: | ---: | ---: | ---: |
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

- kimi-k3 / BF16 compact MLA + FP32 KDA: 24 MLA + 69 KDA; compact is declared absorbed execution, expanded matches pinned HF cache. KDA fixed state and short convolution must not be described as per-token-growing KV.
- kimi-k3 / BF16 expanded MLA + FP32 KDA: 24 MLA + 69 KDA; compact is declared absorbed execution, expanded matches pinned HF cache. KDA fixed state and short convolution must not be described as per-token-growing KV.
- deepseek-v4-flash / BF16 reference: CSA top-k main read plus full index scan; HCA reads all compressed entries. Shared latent counted once per attention layer for QK/PV. Compressor buffers/updates excluded. Production main 584B includes scale padding; reference is BF16.
- deepseek-v4-flash / FP8/BF16 main + MXFP4 index: CSA top-k main read plus full index scan; HCA reads all compressed entries. Shared latent counted once per attention layer for QK/PV. Compressor buffers/updates excluded. Production main 584B includes scale padding; reference is BF16.
- deepseek-v4-pro / BF16 reference: CSA top-k main read plus full index scan; HCA reads all compressed entries. Shared latent counted once per attention layer for QK/PV. Compressor buffers/updates excluded. Production main 584B includes scale padding; reference is BF16.
- deepseek-v4-pro / FP8/BF16 main + MXFP4 index: CSA top-k main read plus full index scan; HCA reads all compressed entries. Shared latent counted once per attention layer for QK/PV. Compressor buffers/updates excluded. Production main 584B includes scale padding; reference is BF16.
- deepseek-v4.1-flash / FP4 global + FP8 SWA + MXFP4 index: 4 KV owners, 8 indexing layers, 30 reuse layers; production candidate-limited index read (<= 16384 entries for later indexers). Per-layer logical reads count shared cache repeatedly; unique union/actual HBM unknown. Released reference scans full BF16 index before masking (1744830464 B), unlike production selective read. Compressor/candidate/top-k metadata excluded.

跳过超出配置上下文上限的模型：qwen3-8b, qwen3-32b, qwen3-30b-a3b, qwen3-235b-a22b, deepseek-r1-distill-llama-70b, qwen3.5-397b-a17b, qwen3.6-35b-a3b, deepseek-v3
