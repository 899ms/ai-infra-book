<!-- 从 dflash2.html 迁移的资料快照；原始 HTML SHA-256: d6f431e594abd539758cbfdd7a81856b86174a83f42282245ad3213f6bee2768。 -->

# DFlash 2: Keep Drafting Parallel

August 18, 2026

Inference is the bottleneck of the agent era. Agents read, plan, and call tools, often for hours or days. They consume tokens at a rate chat never approached. Every one of those tokens takes a full forward pass over the model. At Inco AI, we are building the inference stack scaled to the token economics of tomorrow. This post is a sneak peek.

Our team released [DFlash](https://arxiv.org/abs/2602.06036) in January; it now runs in SGLang, vLLM, TensorRT-LLM, and llama.cpp. NVIDIA measured [up to 15× throughput](https://developer.nvidia.com/blog/boost-inference-performance-up-to-15x-on-nvidia-blackwell-using-dflash-speculative-decoding/) with it on Blackwell GPUs; Google reported [3× more tokens per second](https://developers.googleblog.com/supercharging-llm-inference-on-google-tpus-achieving-3x-speedups-with-diffusion-style-speculative-decoding/) on TPUs; CoreWeave's production Kimi K2.7 Code endpoint, [the fastest for that model on Artificial Analysis](https://www.coreweave.com/blog/kimi-k2-7-code-now-available-on-serverless-inference-with-leading-benchmark-price-performance), runs DFlash by default. The ecosystem now builds on it: [NVIDIA](https://huggingface.co/nvidia/Kimi-K2.6-DFlash), [Red Hat](https://huggingface.co/RedHatAI/gemma-4-31B-it-speculator.dflash), and [Modal](https://huggingface.co/modal-labs/Kimi-K3-DFlash) have all published DFlash drafters; Meta ([Muse Glimmer](https://huggingface.co/meta-models/Muse-Glimmer-30B-assistant)), Poolside ([Laguna](https://huggingface.co/poolside/Laguna-S-2.1-DFlash)), Xiaomi ([MiMo-V2.5-Pro](https://huggingface.co/XiaomiMiMo/MiMo-V2.5-Pro-FP4-DFlash)), and NVIDIA ([Nemotron 3.5 Lightning](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Lightning-30B-A3B-NVFP4-DFlash)) ship official drafters with their own models. On Hugging Face, DFlash models have been downloaded **more than 3.5 million times** (as of August 2026).

Speculative decoding is a core piece of the modern inference stack.^([1](#user-content-fn-modal)) A small draft model guesses a block of tokens, and the target model verifies the whole block in one forward pass. Good guesses turn one pass into several tokens; bad ones just get thrown away. For years, though, the draft itself stayed ***autoregressive***: one token at a time. DFlash made it one-pass too: the entire block, every position, predicted ***in parallel***.

DFlash 2 drafting for Qwen3.8-27B on an Apple M5 Max with oMLX, side by side with autoregressive decoding.

DFlash 2 pushes parallel drafting one step further: **over 20% more output from every verification pass, for around 1% added cycle latency**, with the output provably unchanged. Across benchmarks the gain runs 16–25%. With the Qwen3.8-27B drafter released today, SGLang serves at **2.7–3.4× the throughput of autoregressive decoding** at batch size 1. Predicting every position independently leaves headroom in two places: choosing the right tokens and holding accuracy to the end of the block. DFlash 2 recovers both without giving up the one-pass design.

## [Run It Now](#run-it-now)

DFlash 2 already runs in the mainstream inference engines:

SGLang

vLLM

llama.cpp

Ollama

oMLX

```
pip install "sglang[all] @ git+https://github.com/sgl-project/sglang.git#subdirectory=python"
 
python -m sglang.launch_server \
  --model-path Qwen/Qwen3.8-27B \
  --speculative-algorithm DFLASH \
  --speculative-draft-model-path incoai/Qwen3.8-27B-DFlash2 \
  --speculative-num-draft-tokens 8
```

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNvcHkgc2l6ZS0zLjUiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cmVjdCB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHg9IjgiIHk9IjgiIHJ4PSIyIiByeT0iMiIgLz48cGF0aCBkPSJNNCAxNmMtMS4xIDAtMi0uOS0yLTJWNGMwLTEuMS45LTIgMi0yaDEwYzEuMSAwIDIgLjkgMiAyIiAvPjwvc3ZnPg==)

```
pip install -U "vllm @ git+https://github.com/vllm-project/vllm.git@refs/pull/52816/head"
 
vllm serve Qwen/Qwen3.8-27B \
  --speculative-config '{
    "method": "dflash",
    "model": "incoai/Qwen3.8-27B-DFlash2",
    "num_speculative_tokens": 7
  }'
```

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNvcHkgc2l6ZS0zLjUiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cmVjdCB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHg9IjgiIHk9IjgiIHJ4PSIyIiByeT0iMiIgLz48cGF0aCBkPSJNNCAxNmMtMS4xIDAtMi0uOS0yLTJWNGMwLTEuMS45LTIgMi0yaDEwYzEuMSAwIDIgLjkgMiAyIiAvPjwvc3ZnPg==)

```
git clone https://github.com/ggml-org/llama.cpp.git
cd llama.cpp
git fetch origin pull/27342/head:pr-27342
git switch pr-27342
 
# NVIDIA CUDA
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_CUDA=ON
cmake --build build -j
 
# Apple Silicon
cmake -B build -DCMAKE_BUILD_TYPE=Release -DGGML_METAL=ON
cmake --build build -j
 
./build/bin/llama-server \
  -hf ggml-org/Qwen3.8-27B-GGUF:Q4_K_M \
  -hfd incoai/Qwen3.8-27B-DFlash2-GGUF:Q4_K_M \
  --spec-type draft-dflash \
  --spec-draft-n-max 7
```

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNvcHkgc2l6ZS0zLjUiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cmVjdCB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHg9IjgiIHk9IjgiIHJ4PSIyIiByeT0iMiIgLz48cGF0aCBkPSJNNCAxNmMtMS4xIDAtMi0uOS0yLTJWNGMwLTEuMS45LTIgMi0yaDEwYzEuMSAwIDIgLjkgMiAyIiAvPjwvc3ZnPg==)

```
git clone https://github.com/ollama/ollama.git
cd ollama
git fetch origin pull/17865/head:dflash2
git switch dflash2
 
cmake -B build .
cmake --build build --parallel 8
 
TARGET="$(hf download mlx-community/Qwen3.8-27B-4bit)"
DRAFT="$(hf download incoai/Qwen3.8-27B-DFlash2)"
printf "FROM %s\nDRAFT %s\n" "$TARGET" "$DRAFT" > Modelfile
 
./ollama create qwen38-dflash2 \
  --experimental \
  --draft-quantize int4
 
./ollama serve
sleep 2
./ollama run qwen38-dflash2 --think high
```

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNvcHkgc2l6ZS0zLjUiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cmVjdCB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHg9IjgiIHk9IjgiIHJ4PSIyIiByeT0iMiIgLz48cGF0aCBkPSJNNCAxNmMtMS4xIDAtMi0uOS0yLTJWNGMwLTEuMS45LTIgMi0yaDEwYzEuMSAwIDIgLjkgMiAyIiAvPjwvc3ZnPg==)

Download and install the [prebuilt oMLX with DFlash 2 support](https://github.com/z-lab/omlx-fork/releases/download/0.6.2-dflash2/oMLX-0.6.2-zlab-dflash2-arm64-signed.dmg).

To run Qwen3.8-27B with DFlash 2:

1.  Open the oMLX [Model Downloader](http://127.0.0.1:8891/admin/dashboard?tab=models&modelsTab=downloader) and download:

    - [`mlx-community/Qwen3.8-27B-4bit`](https://huggingface.co/mlx-community/Qwen3.8-27B-4bit)
    - [`incoai/Qwen3.8-27B-DFlash2`](https://huggingface.co/incoai/Qwen3.8-27B-DFlash2)

2.  Open the [Model Manager](http://127.0.0.1:8891/admin/dashboard?tab=models&modelsTab=manager) and edit `mlx-community/Qwen3.8-27B-4bit`. Configure DFlash with the following settings:

    - **DFlash**: enabled
    - **Draft model**: `incoai/Qwen3.8-27B-DFlash2`
    - **Draft quantization**: enabled
    - **Runtime block size**: `5`
    - **Verify mode**: `dflash`

3.  Save the settings and load the target model.

## [The Right Tokens Are Already There](#the-right-tokens-are-already-there)

DFlash predicts every position independently, in parallel. Each pick is plausible on its own. Yet nothing makes them fit together, and an incoherent block is cut short at verification. Recent methods such as [Domino](https://arxiv.org/abs/2605.29707) and [DSpark](https://arxiv.org/abs/2607.05147) buy coherence with sequential heads that rewrite each position's full-vocabulary distribution. But is that costly autoregressive correction really necessary?

No. The evidence is already in DFlash's own candidate lists. Take the first position: DFlash's top pick is right 85.4% of the time, but the right token is in its top 16 candidates 99.5% of the time. Even when the top pick is wrong, the right token is usually on the list.

| Metric    | 0     | 1     | 2     | 3     | 4     | 5     | 6     | Acceptance length |
|-----------|-------|-------|-------|-------|-------|-------|-------|-------------------|
| Recall@1  | 85.4% | 80.3% | 79.4% | 78.3% | 77.5% | 75.9% | 72.9% | 4.27              |
| Recall@16 | 99.5% | 97.3% | 94.8% | 92.6% | 90.8% | 89.4% | 87.8% | 6.79              |

Table 1. Recall@1 (how often the top pick is right) and Recall@16 (how often the right token is in the top 16) at each draft position, conditioned on every earlier position being right. Five-layer Qwen3-4B DFlash on GSM8K. Acceptance length includes the verifier's next token.

An oracle that always picks the right candidate from the top 16 would lift the acceptance length from 4.27 to 6.79. **That gap is pure selection headroom.** We just need to select the right path through the candidates.

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgNzY0IDM0OCIgY2xhc3M9ImJsb2NrIGgtYXV0byB3LWZ1bGwgbWluLXctWzYwMHB4XSIgcm9sZT0iaW1nIiBhcmlhLWxhYmVsPSJBbmltYXRlZCBkaWFncmFtIG9mIHRoZSBjYW5kaWRhdGUgc2VsZWN0b3I6IERGbGFzaCYjMzk7cyBpbmRlcGVuZGVudCB0b3AgcGlja3MgY29sbGlkZSBpbiBhIHN0dXR0ZXIgYW5kIGRpZSBhdCB2ZXJpZmljYXRpb247IERGbGFzaCAyIGtlZXBzIHRoZSB0b3AgY2FuZGlkYXRlcyBwZXIgcG9zaXRpb24gYW5kIGEgc2VsZWN0b3IgdHJhY2VzIG9uZSBwYXRoIHRocm91Z2ggdGhlbSwgc28gdGhlIHZlcmlmaWVyIGFjY2VwdHMgdGhlIHdob2xlIGJsb2NrLiIgc3R5bGU9ImZvbnQtZmFtaWx5OmluaGVyaXQiPjxkZWZzPjxwYXR0ZXJuIGlkPSJzZi1oYXRjaCIgd2lkdGg9IjgiIGhlaWdodD0iOCIgcGF0dGVybnVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgcGF0dGVybnRyYW5zZm9ybT0icm90YXRlKDEzNSkiPjxyZWN0IHdpZHRoPSI4IiBoZWlnaHQ9IjgiIGZpbGw9InRyYW5zcGFyZW50IiAvPjxyZWN0IHdpZHRoPSIzIiBoZWlnaHQ9IjgiIGZpbGw9InZhcigtLWZpZy1tYXNrLXN0cmlwZSkiIC8+PC9wYXR0ZXJuPjwvZGVmcz48Zz48cmVjdCB4PSIyNCIgeT0iNTAiIHdpZHRoPSI5MiIgaGVpZ2h0PSIyNiIgcng9IjciIGZpbGw9Im5vbmUiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZSkiIC8+PHRleHQgeD0iNzAiIHk9IjYzIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxMyIgZmlsbD0idmFyKC0tZmlnLW11dGVkKSI+RGlmZnVzaW9uPC90ZXh0PjwvZz48Zz48cmVjdCB4PSIyNCIgeT0iODAiIHdpZHRoPSI5MiIgaGVpZ2h0PSIyNiIgcng9IjciIGZpbGw9Im5vbmUiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZSkiIC8+PHRleHQgeD0iNzAiIHk9IjkzIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxMyIgZmlsbD0idmFyKC0tZmlnLW11dGVkKSI+aXM8L3RleHQ+PC9nPjxnPjxyZWN0IHg9IjI0IiB5PSIxMTAiIHdpZHRoPSI5MiIgaGVpZ2h0PSIyNiIgcng9IjciIGZpbGw9Im5vbmUiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZSkiIC8+PHRleHQgeD0iNzAiIHk9IjEyMyIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIGZvbnQtc2l6ZT0iMTMiIGZpbGw9InZhcigtLWZpZy1tdXRlZCkiPmdvb2Q8L3RleHQ+PC9nPjxnPjxyZWN0IHg9IjI0IiB5PSIyMDEiIHdpZHRoPSI5MiIgaGVpZ2h0PSIzMCIgcng9IjciIGZpbGw9InVybCgjc2YtaGF0Y2gpIiBzdHJva2U9InZhcigtLWZpZy1tYXNrLXN0cm9rZSkiIC8+PHRleHQgeD0iNzAiIHk9IjIxNiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIGZvbnQtc2l6ZT0iMTMiIGZpbGw9InZhcigtLWZpZy1tYXNrLXRleHQpIj7in6htYXNr4p+pPC90ZXh0PjwvZz48Zz48cmVjdCB4PSIyNCIgeT0iMjM1IiB3aWR0aD0iOTIiIGhlaWdodD0iMzAiIHJ4PSI3IiBmaWxsPSJ1cmwoI3NmLWhhdGNoKSIgc3Ryb2tlPSJ2YXIoLS1maWctbWFzay1zdHJva2UpIiAvPjx0ZXh0IHg9IjcwIiB5PSIyNTAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGRvbWluYW50LWJhc2VsaW5lPSJjZW50cmFsIiBmb250LXNpemU9IjEzIiBmaWxsPSJ2YXIoLS1maWctbWFzay10ZXh0KSI+4p+obWFza+KfqTwvdGV4dD48L2c+PGc+PHJlY3QgeD0iMjQiIHk9IjI2OSIgd2lkdGg9IjkyIiBoZWlnaHQ9IjMwIiByeD0iNyIgZmlsbD0idXJsKCNzZi1oYXRjaCkiIHN0cm9rZT0idmFyKC0tZmlnLW1hc2stc3Ryb2tlKSIgLz48dGV4dCB4PSI3MCIgeT0iMjg0IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxMyIgZmlsbD0idmFyKC0tZmlnLW1hc2stdGV4dCkiPuKfqG1hc2vin6k8L3RleHQ+PC9nPjxyZWN0IHg9IjE3MCIgeT0iMjAiIHdpZHRoPSI0MzAiIGhlaWdodD0iMzIwIiByeD0iMTIiIGZpbGw9InZhcigtLWZpZy1wYW5lbC1maWxsKSIgc3Ryb2tlPSJ2YXIoLS1maWctc3Ryb2tlKSIgLz48dGV4dCB4PSIxODYiIHk9IjQ2IiBmb250LXNpemU9IjE2IiBmaWxsPSJ2YXIoLS1maWctdGV4dCkiIGZvbnQtd2VpZ2h0PSI2MDAiIGxldHRlci1zcGFjaW5nPSIwLjMiPkluZGVwZW5kZW50IFRvcC0xIFBpY2tzPC90ZXh0PjxyZWN0IHg9IjI0IiB5PSIxNjMiIHdpZHRoPSI5MiIgaGVpZ2h0PSIzNCIgcng9IjciIGZpbGw9InZhcigtLWZpZy1hbWJlci1maWxsKSIgc3Ryb2tlPSJ2YXIoLS1maWctYW1iZXItc3Ryb2tlKSIgLz48dGV4dCB4PSI3MCIgeT0iMTgwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0idmFyKC0tZmlnLWFtYmVyLXRleHQpIj5mb3I8L3RleHQ+PGcgc3R5bGU9Im9wYWNpdHk6MDt0cmFuc2l0aW9uOm9wYWNpdHkgNTAwbXMgZWFzZSI+PGxpbmUgeDE9IjExOSIgeTE9IjE4MCIgeDI9IjIwMyIgeTI9IjEwNCIgc3Ryb2tlPSJ2YXIoLS1maWctZmFpbnQpIiBzdHJva2Utd2lkdGg9IjIuNSI+PC9saW5lPjxsaW5lIHgxPSIyOTgiIHkxPSIxMDQiIHgyPSI1MzYiIHkyPSIxMDQiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZS1zb2Z0KSIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtZGFzaGFycmF5PSI0IDUiPjwvbGluZT48dGV4dCB4PSIzMDYiIHk9IjkwIiBmb250LXNpemU9IjE1IiBmb250LXdlaWdodD0iNzAwIiBmaWxsPSJ2YXIoLS1maWctcmVqZWN0KSI+4pyXPC90ZXh0Pjx0ZXh0IHg9IjMyMyIgeT0iMTM4IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXNpemU9IjExLjUiIGZpbGw9InZhcigtLWZpZy1yZWplY3QpIj5zYW1lIHdvcmQsIHR3aWNlPC90ZXh0PjwvZz48ZyBzdHJva2U9InZhcigtLWZpZy1zdHJva2Utc29mdCkiIHN0cm9rZS13aWR0aD0iMSIgc3R5bGU9Im9wYWNpdHk6MDt0cmFuc2l0aW9uOm9wYWNpdHkgNTAwbXMgZWFzZSI+PGxpbmUgeDE9IjExNiIgeTE9IjE4MCIgeDI9IjIwNiIgeTI9IjEwNCI+PC9saW5lPjxsaW5lIHgxPSIxMTYiIHkxPSIxODAiIHgyPSIyMDYiIHkyPSIxODAiPjwvbGluZT48bGluZSB4MT0iMTE2IiB5MT0iMTgwIiB4Mj0iMjA2IiB5Mj0iMjU2Ij48L2xpbmU+PGxpbmUgeDE9IjI5OCIgeTE9IjEwNCIgeDI9IjM0OCIgeTI9IjEwNCI+PC9saW5lPjxsaW5lIHgxPSIyOTgiIHkxPSIxMDQiIHgyPSIzNDgiIHkyPSIxODAiPjwvbGluZT48bGluZSB4MT0iMjk4IiB5MT0iMTA0IiB4Mj0iMzQ4IiB5Mj0iMjU2Ij48L2xpbmU+PGxpbmUgeDE9IjI5OCIgeTE9IjE4MCIgeDI9IjM0OCIgeTI9IjEwNCI+PC9saW5lPjxsaW5lIHgxPSIyOTgiIHkxPSIxODAiIHgyPSIzNDgiIHkyPSIxODAiPjwvbGluZT48bGluZSB4MT0iMjk4IiB5MT0iMTgwIiB4Mj0iMzQ4IiB5Mj0iMjU2Ij48L2xpbmU+PGxpbmUgeDE9IjI5OCIgeTE9IjI1NiIgeDI9IjM0OCIgeTI9IjEwNCI+PC9saW5lPjxsaW5lIHgxPSIyOTgiIHkxPSIyNTYiIHgyPSIzNDgiIHkyPSIxODAiPjwvbGluZT48bGluZSB4MT0iMjk4IiB5MT0iMjU2IiB4Mj0iMzQ4IiB5Mj0iMjU2Ij48L2xpbmU+PGxpbmUgeDE9IjQ0MCIgeTE9IjEwNCIgeDI9IjQ5MCIgeTI9IjEwNCI+PC9saW5lPjxsaW5lIHgxPSI0NDAiIHkxPSIxMDQiIHgyPSI0OTAiIHkyPSIxODAiPjwvbGluZT48bGluZSB4MT0iNDQwIiB5MT0iMTA0IiB4Mj0iNDkwIiB5Mj0iMjU2Ij48L2xpbmU+PGxpbmUgeDE9IjQ0MCIgeTE9IjE4MCIgeDI9IjQ5MCIgeTI9IjEwNCI+PC9saW5lPjxsaW5lIHgxPSI0NDAiIHkxPSIxODAiIHgyPSI0OTAiIHkyPSIxODAiPjwvbGluZT48bGluZSB4MT0iNDQwIiB5MT0iMTgwIiB4Mj0iNDkwIiB5Mj0iMjU2Ij48L2xpbmU+PGxpbmUgeDE9IjQ0MCIgeTE9IjI1NiIgeDI9IjQ5MCIgeTI9IjEwNCI+PC9saW5lPjxsaW5lIHgxPSI0NDAiIHkxPSIyNTYiIHgyPSI0OTAiIHkyPSIxODAiPjwvbGluZT48bGluZSB4MT0iNDQwIiB5MT0iMjU2IiB4Mj0iNDkwIiB5Mj0iMjU2Ij48L2xpbmU+PC9nPjxwYXRoIGQ9Ik0gMTE5IDE4MCBMIDIwMyAxODAgTSAzMDEgMTgwIEwgMzQ1IDEwNCBNIDQ0MyAxMDQgTCA0ODcgMTA0IiBmaWxsPSJub25lIiBzdHJva2U9InZhcigtLWZpZy1ncmVlbi10ZXh0KSIgc3Ryb2tlLXdpZHRoPSIzIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS1kYXNoYXJyYXk9IjkwMCIgc3Ryb2tlLWRhc2hvZmZzZXQ9IjkwMCIgc3R5bGU9InRyYW5zaXRpb246c3Ryb2tlLWRhc2hvZmZzZXQgOTAwbXMgZWFzZSwgb3BhY2l0eSAzMDBtcyBlYXNlIiBvcGFjaXR5PSIwIiAvPjxnPjx0ZXh0IHg9IjI1MiIgeT0iNzIiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTEiIGZpbGw9InZhcigtLWZpZy1tdXRlZCkiPnBvc2l0aW9uIDwhLS0gLS0+MTwvdGV4dD48ZyBzdHlsZT0ib3BhY2l0eToxO3RyYW5zaXRpb246b3BhY2l0eSA1MDBtcyBlYXNlIj48cmVjdCB4PSIyMDYiIHk9Ijg3IiB3aWR0aD0iOTIiIGhlaWdodD0iMzQiIHJ4PSI3IiBmaWxsPSJ2YXIoLS1maWctY2FuZGlkYXRlLWZpbGwpIiBzdHJva2U9InZhcigtLWZpZy1zdHJva2UpIiBzdHlsZT0idHJhbnNpdGlvbjpmaWxsIDMwMG1zIGVhc2UsIHN0cm9rZSAzMDBtcyBlYXNlIiAvPjx0ZXh0IHg9IjI1MiIgeT0iMTA0IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxMyIgZmlsbD0idmFyKC0tZmlnLW11dGVkKSI+ZGVjb2Rpbmc8L3RleHQ+PC9nPjxnIHN0eWxlPSJvcGFjaXR5OjA7dHJhbnNpdGlvbjpvcGFjaXR5IDUwMG1zIGVhc2UiPjxyZWN0IHg9IjIwNiIgeT0iMTYzIiB3aWR0aD0iOTIiIGhlaWdodD0iMzQiIHJ4PSI3IiBmaWxsPSJ2YXIoLS1maWctY2FuZGlkYXRlLWZpbGwpIiBzdHJva2U9InZhcigtLWZpZy1zdHJva2UpIiBzdHlsZT0idHJhbnNpdGlvbjpmaWxsIDMwMG1zIGVhc2UsIHN0cm9rZSAzMDBtcyBlYXNlIiAvPjx0ZXh0IHg9IjI1MiIgeT0iMTgwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxMyIgZmlsbD0idmFyKC0tZmlnLW11dGVkKSI+c3BlY3VsYXRpdmU8L3RleHQ+PC9nPjxnIHN0eWxlPSJvcGFjaXR5OjA7dHJhbnNpdGlvbjpvcGFjaXR5IDUwMG1zIGVhc2UiPjxyZWN0IHg9IjIwNiIgeT0iMjM5IiB3aWR0aD0iOTIiIGhlaWdodD0iMzQiIHJ4PSI3IiBmaWxsPSJ2YXIoLS1maWctY2FuZGlkYXRlLWZpbGwpIiBzdHJva2U9InZhcigtLWZpZy1zdHJva2UpIiBzdHlsZT0idHJhbnNpdGlvbjpmaWxsIDMwMG1zIGVhc2UsIHN0cm9rZSAzMDBtcyBlYXNlIiAvPjx0ZXh0IHg9IjI1MiIgeT0iMjU2IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxMyIgZmlsbD0idmFyKC0tZmlnLW11dGVkKSI+c2xvdzwvdGV4dD48L2c+PHRleHQgeD0iMjUyIiB5PSIyOTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTUiIGZpbGw9InZhcigtLWZpZy1mYWludCkiIHN0eWxlPSJvcGFjaXR5OjA7dHJhbnNpdGlvbjpvcGFjaXR5IDUwMG1zIGVhc2UiPuKLrjwvdGV4dD48L2c+PGc+PHRleHQgeD0iMzk0IiB5PSI3MiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIxMSIgZmlsbD0idmFyKC0tZmlnLW11dGVkKSI+cG9zaXRpb24gPCEtLSAtLT4yPC90ZXh0PjxnIHN0eWxlPSJvcGFjaXR5OjE7dHJhbnNpdGlvbjpvcGFjaXR5IDUwMG1zIGVhc2UiPjxyZWN0IHg9IjM0OCIgeT0iODciIHdpZHRoPSI5MiIgaGVpZ2h0PSIzNCIgcng9IjciIGZpbGw9InZhcigtLWZpZy1jYW5kaWRhdGUtZmlsbCkiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZSkiIHN0eWxlPSJ0cmFuc2l0aW9uOmZpbGwgMzAwbXMgZWFzZSwgc3Ryb2tlIDMwMG1zIGVhc2UiIC8+PHRleHQgeD0iMzk0IiB5PSIxMDQiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGRvbWluYW50LWJhc2VsaW5lPSJjZW50cmFsIiBmb250LXNpemU9IjEzIiBmaWxsPSJ2YXIoLS1maWctbXV0ZWQpIj5kZWNvZGluZzwvdGV4dD48L2c+PGcgc3R5bGU9Im9wYWNpdHk6MDt0cmFuc2l0aW9uOm9wYWNpdHkgNTAwbXMgZWFzZSI+PHJlY3QgeD0iMzQ4IiB5PSIxNjMiIHdpZHRoPSI5MiIgaGVpZ2h0PSIzNCIgcng9IjciIGZpbGw9InZhcigtLWZpZy1jYW5kaWRhdGUtZmlsbCkiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZSkiIHN0eWxlPSJ0cmFuc2l0aW9uOmZpbGwgMzAwbXMgZWFzZSwgc3Ryb2tlIDMwMG1zIGVhc2UiIC8+PHRleHQgeD0iMzk0IiB5PSIxODAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGRvbWluYW50LWJhc2VsaW5lPSJjZW50cmFsIiBmb250LXNpemU9IjEzIiBmaWxsPSJ2YXIoLS1maWctbXV0ZWQpIj50aGlua2luZzwvdGV4dD48L2c+PGcgc3R5bGU9Im9wYWNpdHk6MDt0cmFuc2l0aW9uOm9wYWNpdHkgNTAwbXMgZWFzZSI+PHJlY3QgeD0iMzQ4IiB5PSIyMzkiIHdpZHRoPSI5MiIgaGVpZ2h0PSIzNCIgcng9IjciIGZpbGw9InZhcigtLWZpZy1jYW5kaWRhdGUtZmlsbCkiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZSkiIHN0eWxlPSJ0cmFuc2l0aW9uOmZpbGwgMzAwbXMgZWFzZSwgc3Ryb2tlIDMwMG1zIGVhc2UiIC8+PHRleHQgeD0iMzk0IiB5PSIyNTYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGRvbWluYW50LWJhc2VsaW5lPSJjZW50cmFsIiBmb250LXNpemU9IjEzIiBmaWxsPSJ2YXIoLS1maWctbXV0ZWQpIj5tb2RlbHM8L3RleHQ+PC9nPjx0ZXh0IHg9IjM5NCIgeT0iMjk4IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXNpemU9IjE1IiBmaWxsPSJ2YXIoLS1maWctZmFpbnQpIiBzdHlsZT0ib3BhY2l0eTowO3RyYW5zaXRpb246b3BhY2l0eSA1MDBtcyBlYXNlIj7ii648L3RleHQ+PC9nPjxnPjx0ZXh0IHg9IjUzNiIgeT0iNzIiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTEiIGZpbGw9InZhcigtLWZpZy1tdXRlZCkiPnBvc2l0aW9uIDwhLS0gLS0+MzwvdGV4dD48ZyBzdHlsZT0ib3BhY2l0eToxO3RyYW5zaXRpb246b3BhY2l0eSA1MDBtcyBlYXNlIj48cmVjdCB4PSI0OTAiIHk9Ijg3IiB3aWR0aD0iOTIiIGhlaWdodD0iMzQiIHJ4PSI3IiBmaWxsPSJ2YXIoLS1maWctY2FuZGlkYXRlLWZpbGwpIiBzdHJva2U9InZhcigtLWZpZy1zdHJva2UpIiBzdHlsZT0idHJhbnNpdGlvbjpmaWxsIDMwMG1zIGVhc2UsIHN0cm9rZSAzMDBtcyBlYXNlIiAvPjx0ZXh0IHg9IjUzNiIgeT0iMTA0IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxMyIgZmlsbD0idmFyKC0tZmlnLW11dGVkKSI+4p+oZW9z4p+pPC90ZXh0PjwvZz48ZyBzdHlsZT0ib3BhY2l0eTowO3RyYW5zaXRpb246b3BhY2l0eSA1MDBtcyBlYXNlIj48cmVjdCB4PSI0OTAiIHk9IjE2MyIgd2lkdGg9IjkyIiBoZWlnaHQ9IjM0IiByeD0iNyIgZmlsbD0idmFyKC0tZmlnLWNhbmRpZGF0ZS1maWxsKSIgc3Ryb2tlPSJ2YXIoLS1maWctc3Ryb2tlKSIgc3R5bGU9InRyYW5zaXRpb246ZmlsbCAzMDBtcyBlYXNlLCBzdHJva2UgMzAwbXMgZWFzZSIgLz48dGV4dCB4PSI1MzYiIHk9IjE4MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIGZvbnQtc2l6ZT0iMTMiIGZpbGw9InZhcigtLWZpZy1tdXRlZCkiPmFnYWluPC90ZXh0PjwvZz48ZyBzdHlsZT0ib3BhY2l0eTowO3RyYW5zaXRpb246b3BhY2l0eSA1MDBtcyBlYXNlIj48cmVjdCB4PSI0OTAiIHk9IjIzOSIgd2lkdGg9IjkyIiBoZWlnaHQ9IjM0IiByeD0iNyIgZmlsbD0idmFyKC0tZmlnLWNhbmRpZGF0ZS1maWxsKSIgc3Ryb2tlPSJ2YXIoLS1maWctc3Ryb2tlKSIgc3R5bGU9InRyYW5zaXRpb246ZmlsbCAzMDBtcyBlYXNlLCBzdHJva2UgMzAwbXMgZWFzZSIgLz48dGV4dCB4PSI1MzYiIHk9IjI1NiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIGZvbnQtc2l6ZT0iMTMiIGZpbGw9InZhcigtLWZpZy1tdXRlZCkiPuKApjwvdGV4dD48L2c+PHRleHQgeD0iNTM2IiB5PSIyOTgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTUiIGZpbGw9InZhcigtLWZpZy1mYWludCkiIHN0eWxlPSJvcGFjaXR5OjA7dHJhbnNpdGlvbjpvcGFjaXR5IDUwMG1zIGVhc2UiPuKLrjwvdGV4dD48L2c+PHRleHQgeD0iMzg1IiB5PSIzMjYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTEuNSIgZmlsbD0idmFyKC0tZmlnLW11dGVkKSIgc3R5bGU9Im9wYWNpdHk6MDt0cmFuc2l0aW9uOm9wYWNpdHkgNTAwbXMgZWFzZSI+YWxsIGFkamFjZW50IHBhaXJzIHNjb3JlZCBhdCBvbmNlIOKGkiBvbmUgcGF0aCBrZXB0PC90ZXh0PjxwYXRoIGQ9Ik02MTAgMTgwIGgxOSBtLTUgLTUgbDUgNSAtNSA1IiBzdHJva2U9InZhcigtLWZpZy1mYWludCkiIHN0cm9rZS13aWR0aD0iMS41IiBmaWxsPSJub25lIiAvPjx0ZXh0IHg9IjY5MiIgeT0iNjQiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTEiIGZpbGw9InZhcigtLWZpZy1tdXRlZCkiPmFjY2VwdGVkIG91dHB1dDwvdGV4dD48ZyBzdHlsZT0ib3BhY2l0eToxO3RyYW5zaXRpb246b3BhY2l0eSA1MDBtcyBlYXNlIj48cmVjdCB4PSI2NDYiIHk9Ijg4IiB3aWR0aD0iOTIiIGhlaWdodD0iMzAiIHJ4PSI3IiBmaWxsPSJ2YXIoLS1maWctYW1iZXItZmlsbCkiIHN0cm9rZT0idmFyKC0tZmlnLWFtYmVyLXN0cm9rZSkiIC8+PHRleHQgeD0iNjkyIiB5PSIxMDMiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGRvbWluYW50LWJhc2VsaW5lPSJjZW50cmFsIiBmb250LXNpemU9IjEzIiBmaWxsPSJ2YXIoLS1maWctYW1iZXItdGV4dCkiPmZvcjwvdGV4dD48L2c+PGcgc3R5bGU9Im9wYWNpdHk6MC4zNTt0cmFuc2l0aW9uOm9wYWNpdHkgNTAwbXMgZWFzZSI+PHJlY3QgeD0iNjQ2IiB5PSIxMjQiIHdpZHRoPSI5MiIgaGVpZ2h0PSIzMCIgcng9IjciIGZpbGw9Im5vbmUiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZSkiIHN0cm9rZS1kYXNoYXJyYXk9IjQgNCIgLz48L2c+PGcgc3R5bGU9Im9wYWNpdHk6MC4zNTt0cmFuc2l0aW9uOm9wYWNpdHkgNTAwbXMgZWFzZSI+PHJlY3QgeD0iNjQ2IiB5PSIxNjQiIHdpZHRoPSI5MiIgaGVpZ2h0PSIzMCIgcng9IjciIGZpbGw9Im5vbmUiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZSkiIHN0cm9rZS1kYXNoYXJyYXk9IjQgNCIgLz48L2c+PGcgc3R5bGU9Im9wYWNpdHk6MC4zNTt0cmFuc2l0aW9uOm9wYWNpdHkgNTAwbXMgZWFzZSI+PHJlY3QgeD0iNjQ2IiB5PSIyMDQiIHdpZHRoPSI5MiIgaGVpZ2h0PSIzMCIgcng9IjciIGZpbGw9Im5vbmUiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZSkiIHN0cm9rZS1kYXNoYXJyYXk9IjQgNCIgLz48L2c+PC9zdmc+)

target-decoded tokenmask tokenaccepted draftselected path

Figure 1. The selector in one cycle. With DFlash alone, each position keeps its top pick; here two neighbors both pick the same word, and the stutter dies at verification. DFlash 2 keeps each position's top candidates, and the selector traces one coherent path through them; here, the whole block survives.

### [A Lightweight Path Selector](#a-lightweight-path-selector)

Coherence is mostly local: a candidate's fit depends mainly on the token just before it, so scoring neighboring pairs should be enough. DFlash 2 keeps the top 16 candidates at each position and scores every adjacent pair: for predecessor $`a`$ and current candidate $`b`$,

``` math
S_t(a,b)=U_t(b)+\langle A(a)\odot H(h_t),B(b)\rangle.
```

The score has two parts. The first, $`U_t(b)`$, is DFlash's own logit: how much the drafter already liked $`b`$ on its own. The second asks how well $`b`$ follows $`a`$: $`A`$ and $`B`$ give each token a compact 256-dimensional embedding, and the two embeddings are matched under a context gate $`H(h_t)`$ that decides which parts of the match count. In essence, this is a low-rank bilinear attention over adjacent candidates.

Scoring stays fully parallel. Every adjacent pair at every position is scored in one shot, with no extra backbone or LM-head pass. The only sequential work is the final walk over precomputed scores: starting from the last verified token, greedy follows the best successor at each step, sampling draws from the same scores, and rejection sampling restores the exact target distribution.

| Method                   | Params | Latency | T = 0    | T = 1    |
|--------------------------|--------|---------|----------|----------|
| DFlash                   | —      | —       | 4.27     | 3.78     |
| \+ DSpark correction     | +77.8M | +9.6%   | 4.49     | 4.08     |
| \+ path selection (ours) | +2.0M  | +0.6%   | **4.61** | **4.25** |

Table 2. Acceptance length with path selection alone (no convolution), for five-layer Qwen3-4B on GSM8K. Overheads are relative to plain DFlash: parameters added to the drafter, and added draft–verify cycle latency.

The selector improves DFlash by **0.34** tokens at $`T=0`$ and **0.47** at $`T=1`$. It beats the DSpark correction in both settings with roughly 40× fewer parameters and 16× lower latency overhead. Choosing is cheaper than predicting. And there is still room: the oracle reaches 6.79. Pairwise scoring is the simplest selector we could think of, and we believe there is plenty to explore.

## [Suffix Decay Is a Local Problem](#suffix-decay-is-a-local-problem)

We also noticed [both recall rows above](#table-1) decline toward the end of the block. Even the oracle decays: with perfect selection, accuracy still falls from 99.5% at the first position to 87.8% by the last. No selector can fix that, because the candidates themselves are running out. We call this **suffix decay**, and it is a backbone problem.

One suspect is capacity: a five-layer backbone may be too small to preserve dependencies across the block. If that is right, depth should help most at later positions. And it does! 3-, 5-, and 15-layer DFlash models are almost identical at the first position, and fan apart down the block. But depth is indiscriminate: ten extra attention blocks add capacity everywhere, even at the early positions that had little left to gain, and erase much of the efficiency that makes DFlash attractive.

DFlash 3L

DFlash 5L

DFlash 15L (3× more params)

DFlash 5L + conv (+3% params)

| Draft position                | 0      | 1      | 2      | 3      | 4      | 5      | 6      |
|-------------------------------|--------|--------|--------|--------|--------|--------|--------|
| DFlash 3L                     | 85.21% | 79.26% | 77.18% | 75.75% | 73.96% | 70.4%  | 64.97% |
| DFlash 5L                     | 85.39% | 80.31% | 79.39% | 78.27% | 77.39% | 76.03% | 72.86% |
| DFlash 15L (3× more params)   | 86.42% | 81.61% | 80.68% | 80.34% | 80.59% | 79.66% | 78.73% |
| DFlash 5L + conv (+3% params) | 85.83% | 80.94% | 79.98% | 79.68% | 79.73% | 79.43% | 77.61% |

Figure 2. Qwen3-4B Recall@1 on GSM8K at T=0, conditioned on every earlier position being right. All drafters are trained under the same setup; the convolutional model is evaluated without the selector. Its convolutions add 3% parameters and 0.7% cycle latency; the ten extra layers of 15L add 15.2%.

Figure 2. Qwen3-4B Recall@1 on GSM8K at T=0, conditioned on every earlier position being right. All drafters are trained under the same setup; the convolutional model is evaluated without the selector. Its convolutions add 3% parameters and 0.7% cycle latency; the ten extra layers of 15L add 15.2%.

We want a targeted fix, and DFlash's attention shows where. It has two jobs: read the context before the block, and model the dependencies inside. But it spends less and less on the second: the block's share of attention falls from **30% in Layer 1 to 8% in Layer 5**, and what remains concentrates in [a shrinking handful of heads](#figure-3). So we split the jobs: a dedicated module takes the within-block work, and attention keeps reading the context.

1

4

8

12

16

20

24

28

32

Layer 1

Layer 2

Layer 3

Layer 4

Layer 5

Attention head

0%90% within-block mass

| Attention head | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| Layer 1 | 17.6% | 2.9% | 41.4% | 50.8% | 29.2% | 50.5% | 44.6% | 5.9% | 44.5% | 11.3% | 17.9% | 36.7% | 0.0% | 14.2% | 0.1% | 0.0% | 13.3% | 1.5% | 18.7% | 7.6% | 45.0% | 33.5% | 53.1% | 42.2% | 64.3% | 60.1% | 32.8% | 47.7% | 49.6% | 57.0% | 26.0% | 52.9% |
| Layer 2 | 20.8% | 26.4% | 39.6% | 18.9% | 8.9% | 22.6% | 13.1% | 32.1% | 22.9% | 25.1% | 24.2% | 28.6% | 36.6% | 26.1% | 41.0% | 36.1% | 17.8% | 25.5% | 25.7% | 25.6% | 4.3% | 21.8% | 23.3% | 22.1% | 15.6% | 70.9% | 58.0% | 2.7% | 28.3% | 38.5% | 20.3% | 33.5% |
| Layer 3 | 1.8% | 11.0% | 9.5% | 5.2% | 34.8% | 8.4% | 12.1% | 14.4% | 11.8% | 22.0% | 8.8% | 3.7% | 4.9% | 10.6% | 17.7% | 52.0% | 4.4% | 19.0% | 13.1% | 9.9% | 61.3% | 76.1% | 47.0% | 60.3% | 1.4% | 8.9% | 6.0% | 64.1% | 9.4% | 3.3% | 8.3% | 8.3% |
| Layer 4 | 0.4% | 37.7% | 28.3% | 85.5% | 0.3% | 1.5% | 0.4% | 0.5% | 1.2% | 12.5% | 36.6% | 1.2% | 1.7% | 0.6% | 2.5% | 1.3% | 7.2% | 3.1% | 48.9% | 3.8% | 3.2% | 1.0% | 23.8% | 1.0% | 0.1% | 0.1% | 0.2% | 0.3% | 2.8% | 6.7% | 12.9% | 12.3% |
| Layer 5 | 1.5% | 0.2% | 0.6% | 0.1% | 60.2% | 76.0% | 0.9% | 0.0% | 0.2% | 12.3% | 32.3% | 0.1% | 15.8% | 0.5% | 0.5% | 0.5% | 0.2% | 0.1% | 0.6% | 0.2% | 0.3% | 28.1% | 0.2% | 1.3% | 0.1% | 0.1% | 0.2% | 29.9% | 0.1% | 0.1% | 0.1% | 1.2% |

Heatmap data

Figure 3. Within-block attention by head in five-layer Qwen3-4B DFlash. Brighter cells mark heads that spend more attention on the draft block; in later layers the within-block mass shrinks and concentrates in a few heads.

### [A Lightweight Local Convolution](#a-lightweight-local-convolution)

The within-block work is short-range to begin with: a block spans only 4 to 16 tokens, and the tightest dependencies sit between neighbors. The natural operator is a short convolution: two taps, one on the current position and one reaching one position back, with weights that adapt to the content. Following [Canon Layers](https://arxiv.org/abs/2512.17351), [Dynamic Short Convolutions](https://arxiv.org/abs/2606.03825), and [Convolution for Large Language Models](https://arxiv.org/abs/2607.18413), we insert this two-tap dynamic depthwise convolution before and after each attention and feed-forward sublayer:

``` math
\operatorname{Conv}_{k}(x)_t
=k_{t,0}\odot x_t+k_{t,1}\odot x_{t-1}.
```

Each coefficient combines a learned base kernel with a small correction computed from the current hidden state; every 16 channels share one correction. The first position reads the last verified token's representation, and every later position reads its predecessor's. Information crosses the block while all positions still compute in parallel.

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgNzYwIDM4MCIgY2xhc3M9Im14LWF1dG8gYmxvY2sgaC1hdXRvIHctZnVsbCBtYXgtdy1bNjgwcHhdIG1pbi13LVs1NjBweF0iIHJvbGU9ImltZyIgYXJpYS1sYWJlbD0iRGlhZ3JhbSBvZiB0aGUgdHdvLXRhcCBkeW5hbWljIGNvbnZvbHV0aW9uLiBUb3A6IG9uZSBkcmFmdGVyIGxheWVyIHdpdGggYSBjb252b2x1dGlvbiBiZWZvcmUgYW5kIGFmdGVyIGVhY2ggYXR0ZW50aW9uIGFuZCBNTFAgc3VibGF5ZXIsIHJlcGVhdGVkIGZpdmUgdGltZXMuIEJvdHRvbSwgem9vbWVkIGludG8gb25lIGNvbnZvbHV0aW9uOiBlYWNoIHBvc2l0aW9uIHRha2VzIG9uZSB0YXAgb24gaXRzZWxmIGFuZCBvbmUgb24gaXRzIHByZWRlY2Vzc29yLCBhbmQgdGhlIGZpcnN0IHBvc2l0aW9uIHJlYWRzIHRoZSBsYXN0IHZlcmlmaWVkIHRva2VuLiIgc3R5bGU9ImZvbnQtZmFtaWx5OmluaGVyaXQiPjxkZWZzPjxtYXJrZXIgaWQ9ImNmLWFycm93IiB2aWV3Ym94PSIwIDAgMTAgMTAiIHJlZng9IjgiIHJlZnk9IjUiIG1hcmtlcndpZHRoPSI1LjUiIG1hcmtlcmhlaWdodD0iNS41IiBvcmllbnQ9ImF1dG8tc3RhcnQtcmV2ZXJzZSI+PHBhdGggZD0iTSAwIDAgTCAxMCA1IEwgMCAxMCB6IiBmaWxsPSJ2YXIoLS1maWctY29yYWwpIiAvPjwvbWFya2VyPjxtYXJrZXIgaWQ9ImNmLWFycm93LWZhaW50IiB2aWV3Ym94PSIwIDAgMTAgMTAiIHJlZng9IjgiIHJlZnk9IjUiIG1hcmtlcndpZHRoPSI3IiBtYXJrZXJoZWlnaHQ9IjciIG9yaWVudD0iYXV0by1zdGFydC1yZXZlcnNlIj48cGF0aCBkPSJNIDAgMCBMIDEwIDUgTCAwIDEwIHoiIGZpbGw9InZhcigtLWZpZy1hcnJvdykiIC8+PC9tYXJrZXI+PG1hcmtlciBpZD0iY2YtYXJyb3ctbGFuZSIgdmlld2JveD0iMCAwIDEwIDEwIiByZWZ4PSI4IiByZWZ5PSI1IiBtYXJrZXJ3aWR0aD0iNiIgbWFya2VyaGVpZ2h0PSI2IiBvcmllbnQ9ImF1dG8iPjxwYXRoIGQ9Ik0gMCAwIEwgMTAgNSBMIDAgMTAgeiIgZmlsbD0idmFyKC0tZmlnLWFycm93KSIgLz48L21hcmtlcj48L2RlZnM+PHJlY3QgeD0iODQiIHk9IjIyIiB3aWR0aD0iNTkyIiBoZWlnaHQ9IjExMiIgcng9IjEzIiBmaWxsPSJub25lIiBzdHJva2U9InZhcigtLWZpZy1zdHJva2UpIiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlLWRhc2hhcnJheT0iNiA0IiAvPjxyZWN0IHg9IjMzOCIgeT0iMTUiIHdpZHRoPSI4NCIgaGVpZ2h0PSIxNCIgZmlsbD0idmFyKC0tYmFja2dyb3VuZCkiIC8+PHRleHQgeD0iMzgwIiB5PSIyNiIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZm9udC1zaXplPSIxMS41IiBmaWxsPSJ2YXIoLS1maWctbXV0ZWQpIiBsZXR0ZXItc3BhY2luZz0iMC41Ij7DlzUgbGF5ZXJzPC90ZXh0PjxsaW5lIHgxPSI0NCIgeTE9Ijc4IiB4Mj0iMTEzIiB5Mj0iNzgiIHN0cm9rZT0idmFyKC0tZmlnLWZhaW50KSIgc3Ryb2tlLXdpZHRoPSIxLjUiPjwvbGluZT48bGluZSB4MT0iMTMzIiB5MT0iNzgiIHgyPSIxNjMiIHkyPSI3OCIgc3Ryb2tlPSJ2YXIoLS1maWctZmFpbnQpIiBzdHJva2Utd2lkdGg9IjEuNSI+PC9saW5lPjxsaW5lIHgxPSIzMDMiIHkxPSI3OCIgeDI9IjMzMyIgeTI9Ijc4IiBzdHJva2U9InZhcigtLWZpZy1mYWludCkiIHN0cm9rZS13aWR0aD0iMS41Ij48L2xpbmU+PGxpbmUgeDE9IjM1MyIgeTE9Ijc4IiB4Mj0iMzgzIiB5Mj0iNzgiIHN0cm9rZT0idmFyKC0tZmlnLWZhaW50KSIgc3Ryb2tlLXdpZHRoPSIxLjUiPjwvbGluZT48bGluZSB4MT0iNDkzIiB5MT0iNzgiIHgyPSI1MjMiIHkyPSI3OCIgc3Ryb2tlPSJ2YXIoLS1maWctZmFpbnQpIiBzdHJva2Utd2lkdGg9IjEuNSI+PC9saW5lPjxsaW5lIHgxPSI1NDMiIHkxPSI3OCIgeDI9IjU3MyIgeTI9Ijc4IiBzdHJva2U9InZhcigtLWZpZy1mYWludCkiIHN0cm9rZS13aWR0aD0iMS41Ij48L2xpbmU+PGxpbmUgeDE9IjY0NyIgeTE9Ijc4IiB4Mj0iNzA4IiB5Mj0iNzgiIHN0cm9rZT0idmFyKC0tZmlnLWZhaW50KSIgc3Ryb2tlLXdpZHRoPSIxLjUiIG1hcmtlci1lbmQ9InVybCgjY2YtYXJyb3ctbGFuZSkiPjwvbGluZT48cmVjdCB4PSIxMTgiIHk9IjQ0IiB3aWR0aD0iMTAiIGhlaWdodD0iNjgiIHJ4PSI1IiBmaWxsPSJ2YXIoLS1maWctY29yYWwtZmlsbCkiIHN0cm9rZT0idmFyKC0tZmlnLWNvcmFsKSIgLz48Zz48cmVjdCB4PSIxNjgiIHk9IjUwIiB3aWR0aD0iMTMwIiBoZWlnaHQ9IjU2IiByeD0iMTEiIGZpbGw9InZhcigtLWZpZy1ib3gtZmlsbCkiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZSkiIC8+PHRleHQgeD0iMjMzIiB5PSI3OCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIGZvbnQtc2l6ZT0iMTUiIGZpbGw9InZhcigtLWZpZy10ZXh0KSI+QXR0ZW50aW9uPC90ZXh0PjwvZz48cmVjdCB4PSIzMzgiIHk9IjQ0IiB3aWR0aD0iMTAiIGhlaWdodD0iNjgiIHJ4PSI1IiBmaWxsPSJ2YXIoLS1maWctY29yYWwtc29mdCkiIHN0cm9rZT0idmFyKC0tZmlnLWNvcmFsKSIgLz48Zz48cmVjdCB4PSIzODgiIHk9IjUwIiB3aWR0aD0iMTAwIiBoZWlnaHQ9IjU2IiByeD0iMTEiIGZpbGw9InZhcigtLWZpZy1ib3gtZmlsbCkiIHN0cm9rZT0idmFyKC0tZmlnLXN0cm9rZSkiIC8+PHRleHQgeD0iNDM4IiB5PSI3OCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIGZvbnQtc2l6ZT0iMTUiIGZpbGw9InZhcigtLWZpZy10ZXh0KSI+TUxQPC90ZXh0PjwvZz48cmVjdCB4PSI1MjgiIHk9IjQ0IiB3aWR0aD0iMTAiIGhlaWdodD0iNjgiIHJ4PSI1IiBmaWxsPSJ2YXIoLS1maWctY29yYWwtZmlsbCkiIHN0cm9rZT0idmFyKC0tZmlnLWNvcmFsKSIgLz48Zz48cmVjdCB4PSI1NzgiIHk9IjUwIiB3aWR0aD0iNjQiIGhlaWdodD0iNTYiIHJ4PSIxMSIgZmlsbD0idmFyKC0tZmlnLWJveC1maWxsKSIgc3Ryb2tlPSJ2YXIoLS1maWctc3Ryb2tlKSIgLz48dGV4dCB4PSI2MTAiIHk9Ijc4IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxNSIgZmlsbD0idmFyKC0tZmlnLXRleHQpIj7igKY8L3RleHQ+PC9nPjxsaW5lIHgxPSIzMzgiIHkxPSIxMTQiIHgyPSI5NiIgeTI9IjE5NiIgc3Ryb2tlPSJ2YXIoLS1maWctc3Ryb2tlLXNvZnQpIiBzdHJva2Utd2lkdGg9IjEuMiIgc3Ryb2tlLWRhc2hhcnJheT0iMyA0Ij48L2xpbmU+PGxpbmUgeDE9IjM0OCIgeTE9IjExNCIgeDI9IjY2NCIgeTI9IjE5NiIgc3Ryb2tlPSJ2YXIoLS1maWctc3Ryb2tlLXNvZnQpIiBzdHJva2Utd2lkdGg9IjEuMiIgc3Ryb2tlLWRhc2hhcnJheT0iMyA0Ij48L2xpbmU+PHJlY3QgeD0iOTYiIHk9IjE5NiIgd2lkdGg9IjU2OCIgaGVpZ2h0PSIxNzIiIHJ4PSIxMyIgZmlsbD0idmFyKC0tZmlnLXBhbmVsLWZpbGwpIiBzdHJva2U9InZhcigtLWZpZy1zdHJva2UpIiAvPjx0ZXh0IHg9IjExNiIgeT0iMjI0IiBmb250LXNpemU9IjEzLjUiPjx0c3BhbiBmaWxsPSJ2YXIoLS1maWctdGV4dCkiIGZvbnQtd2VpZ2h0PSI2MDAiPkluc2lkZSBvbmUgY29udjwvdHNwYW4+PHRzcGFuIGZpbGw9InZhcigtLWZpZy1tdXRlZCkiPiDigJQgZXZlcnkgcG9zaXRpb24gdGFrZXMgdHdvIHRhcHM8L3RzcGFuPjwvdGV4dD48dGV4dCB4PSIxMDgiIHk9IjI1NyIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIGZvbnQtc2l6ZT0iMTIiIGZvbnQtc3R5bGU9Iml0YWxpYyIgZmlsbD0idmFyKC0tZmlnLW11dGVkKSI+eDwvdGV4dD48dGV4dCB4PSIxMDgiIHk9IjMyNyIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIGZvbnQtc2l6ZT0iMTIiIGZvbnQtc3R5bGU9Iml0YWxpYyIgZmlsbD0idmFyKC0tZmlnLW11dGVkKSI+Q29udih4KTwvdGV4dD48Zz48cmVjdCB4PSIxNjYiIHk9IjI0MCIgd2lkdGg9Ijk2IiBoZWlnaHQ9IjM0IiByeD0iOCIgZmlsbD0idmFyKC0tZmlnLWFtYmVyLWZpbGwpIiBzdHJva2U9InZhcigtLWZpZy1hbWJlci1zdHJva2UpIiAvPjx0ZXh0IHg9IjIxNCIgeT0iMjU3IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0idmFyKC0tZmlnLWFtYmVyLXRleHQpIj52ZXJpZmllZDwvdGV4dD48Zz48cmVjdCB4PSIyOTAiIHk9IjI0MCIgd2lkdGg9Ijk2IiBoZWlnaHQ9IjM0IiByeD0iOCIgZmlsbD0idmFyKC0tZmlnLWdyZWVuLWZpbGwpIiBzdHJva2U9InZhcigtLWZpZy1ncmVlbi1zdHJva2UpIiAvPjx0ZXh0IHg9IjMzOCIgeT0iMjU3IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0idmFyKC0tZmlnLWdyZWVuLXRleHQpIj5wb3MgPCEtLSAtLT4xPC90ZXh0PjwvZz48Zz48cmVjdCB4PSI0MTQiIHk9IjI0MCIgd2lkdGg9Ijk2IiBoZWlnaHQ9IjM0IiByeD0iOCIgZmlsbD0idmFyKC0tZmlnLWdyZWVuLWZpbGwpIiBzdHJva2U9InZhcigtLWZpZy1ncmVlbi1zdHJva2UpIiAvPjx0ZXh0IHg9IjQ2MiIgeT0iMjU3IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0idmFyKC0tZmlnLWdyZWVuLXRleHQpIj5wb3MgPCEtLSAtLT4yPC90ZXh0PjwvZz48Zz48cmVjdCB4PSI1MzgiIHk9IjI0MCIgd2lkdGg9Ijk2IiBoZWlnaHQ9IjM0IiByeD0iOCIgZmlsbD0idmFyKC0tZmlnLWdyZWVuLWZpbGwpIiBzdHJva2U9InZhcigtLWZpZy1ncmVlbi1zdHJva2UpIiAvPjx0ZXh0IHg9IjU4NiIgeT0iMjU3IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBkb21pbmFudC1iYXNlbGluZT0iY2VudHJhbCIgZm9udC1zaXplPSIxNCIgZmlsbD0idmFyKC0tZmlnLWdyZWVuLXRleHQpIj5wb3MgPCEtLSAtLT4zPC90ZXh0PjwvZz48L2c+PGc+PHJlY3QgeD0iMjkwIiB5PSIzMTAiIHdpZHRoPSI5NiIgaGVpZ2h0PSIzNCIgcng9IjgiIGZpbGw9InZhcigtLWZpZy1ncmVlbi1maWxsKSIgc3Ryb2tlPSJ2YXIoLS1maWctZ3JlZW4tc3Ryb2tlKSIgLz48dGV4dCB4PSIzMzgiIHk9IjMyNyIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9InZhcigtLWZpZy1ncmVlbi10ZXh0KSI+cG9zIDwhLS0gLS0+MTwvdGV4dD48L2c+PGc+PHJlY3QgeD0iNDE0IiB5PSIzMTAiIHdpZHRoPSI5NiIgaGVpZ2h0PSIzNCIgcng9IjgiIGZpbGw9InZhcigtLWZpZy1ncmVlbi1maWxsKSIgc3Ryb2tlPSJ2YXIoLS1maWctZ3JlZW4tc3Ryb2tlKSIgLz48dGV4dCB4PSI0NjIiIHk9IjMyNyIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9InZhcigtLWZpZy1ncmVlbi10ZXh0KSI+cG9zIDwhLS0gLS0+MjwvdGV4dD48L2c+PGc+PHJlY3QgeD0iNTM4IiB5PSIzMTAiIHdpZHRoPSI5NiIgaGVpZ2h0PSIzNCIgcng9IjgiIGZpbGw9InZhcigtLWZpZy1ncmVlbi1maWxsKSIgc3Ryb2tlPSJ2YXIoLS1maWctZ3JlZW4tc3Ryb2tlKSIgLz48dGV4dCB4PSI1ODYiIHk9IjMyNyIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZG9taW5hbnQtYmFzZWxpbmU9ImNlbnRyYWwiIGZvbnQtc2l6ZT0iMTQiIGZpbGw9InZhcigtLWZpZy1ncmVlbi10ZXh0KSI+cG9zIDwhLS0gLS0+MzwvdGV4dD48L2c+PGxpbmUgeDE9IjMzOCIgeTE9IjI3NiIgeDI9IjMzOCIgeTI9IjMwNiIgc3Ryb2tlPSJ2YXIoLS1maWctYXJyb3cpIiBzdHJva2Utd2lkdGg9IjEuNSIgbWFya2VyLWVuZD0idXJsKCNjZi1hcnJvdy1mYWludCkiPjwvbGluZT48bGluZSB4MT0iNDYyIiB5MT0iMjc2IiB4Mj0iNDYyIiB5Mj0iMzA2IiBzdHJva2U9InZhcigtLWZpZy1hcnJvdykiIHN0cm9rZS13aWR0aD0iMS41IiBtYXJrZXItZW5kPSJ1cmwoI2NmLWFycm93LWZhaW50KSI+PC9saW5lPjxsaW5lIHgxPSI1ODYiIHkxPSIyNzYiIHgyPSI1ODYiIHkyPSIzMDYiIHN0cm9rZT0idmFyKC0tZmlnLWFycm93KSIgc3Ryb2tlLXdpZHRoPSIxLjUiIG1hcmtlci1lbmQ9InVybCgjY2YtYXJyb3ctZmFpbnQpIj48L2xpbmU+PGxpbmUgeDE9IjI0MCIgeTE9IjI3NiIgeDI9IjMxMiIgeTI9IjMwNiIgc3Ryb2tlPSJ2YXIoLS1maWctY29yYWwpIiBzdHJva2Utd2lkdGg9IjEuOCIgbWFya2VyLWVuZD0idXJsKCNjZi1hcnJvdykiPjwvbGluZT48bGluZSB4MT0iMzY0IiB5MT0iMjc2IiB4Mj0iNDM2IiB5Mj0iMzA2IiBzdHJva2U9InZhcigtLWZpZy1jb3JhbCkiIHN0cm9rZS13aWR0aD0iMS44IiBtYXJrZXItZW5kPSJ1cmwoI2NmLWFycm93KSI+PC9saW5lPjxsaW5lIHgxPSI0ODgiIHkxPSIyNzYiIHgyPSI1NjAiIHkyPSIzMDYiIHN0cm9rZT0idmFyKC0tZmlnLWNvcmFsKSIgc3Ryb2tlLXdpZHRoPSIxLjgiIG1hcmtlci1lbmQ9InVybCgjY2YtYXJyb3cpIj48L2xpbmU+PHRleHQgeD0iMjAwIiB5PSIyOTYiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9InZhcigtLWZpZy1jb3JhbC10ZXh0KSI+a+KCgSDCtyB0aGUgcHJlZGVjZXNzb3I8L3RleHQ+PHRleHQgeD0iNTk4IiB5PSIyOTYiIGZvbnQtc2l6ZT0iMTIiIGZpbGw9InZhcigtLWZpZy1tdXRlZCkiPmvigoAgwrcgaXRzZWxmPC90ZXh0Pjwvc3ZnPg==)

two-tap convlast verified tokendraft positions

Figure 4. The two-tap dynamic convolution. One sits before and after each attention and MLP sublayer of every drafter layer. Inside it, each position mixes its own representation with its predecessor's, and the first position reads the last verified token.

The convolution is block-local and stateless, so it drops into DFlash without changing attention, the LM head, or verification.

With only **16.5M added parameters (3%)**, five-layer DFlash with convolution [comes close to 15-layer DFlash](#figure-2), substantially reducing suffix decay. The convolutions add **0.7%** to draft–verify cycle latency; ten more Transformer layers add 15.2%. Average within-block attention across Layers 4 and 5 also falls from **9.4% to 0.5%**, consistent with the convolution absorbing the local work while attention goes back to reading the context. A kernel reaching one position back recovers most of what ten extra layers buy: suffix decay is mostly a *local* problem.

## [Putting It Together](#putting-it-together)

So far, the selector and the convolution have been measured separately; [the full comparison below](#table-3) puts them together. We trained the DFlash and DSpark drafters ourselves under matched setups, while MTP ships with the model.

Qwen3.5-4B

| Dataset   | MTP  | DFlash | DSpark | DFlash 2 |
|-----------|------|--------|--------|----------|
| GSM8K     | 4.78 | 4.99   | 5.69   | **6.20** |
| MATH-500  | 5.04 | 5.42   | 6.20   | **6.76** |
| HumanEval | 4.84 | 5.43   | 5.80   | **6.28** |
| MBPP      | 4.16 | 4.49   | 4.96   | **5.41** |
| MT-Bench  | 3.90 | 4.26   | 4.77   | **5.20** |
| Mean      | 4.54 | 4.92   | 5.49   | **5.97** |

Table 3. Qwen3.5-4B per-request mean acceptance length. Sampling: thinking enabled, temperature 1.0, top-p 0.95, top-k 20, presence penalty 1.5, with lossless rejection sampling.

DFlash 2 leads on every benchmark. Averaged across them, it gains **1.05 tokens over DFlash (21%)** and **0.48 over DSpark**. The upgrade stays cheap: the selector and the convolution together add only **1.3%** to the five-layer DFlash draft–verify cycle latency.

On MATH-500, [the gain is visible position by position](#figure-5): DFlash 2 holds steady near 86% to the last position, and every baseline ends the block 6 to 9 points below it.

MTP

DFlash

DSpark

DFlash 2

| Draft position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| MTP | 84.57% | 80.23% | 79% | 78.42% | 78.63% | 78.17% | 77.36% | 77.74% | 77.91% | 76.96% | 78.06% | 77.4% | 77.49% | 77.48% | 77.85% |
| DFlash | 88.35% | 77.7% | 77.8% | 79.45% | 80.3% | 81.12% | 81.22% | 81.07% | 81.29% | 80.28% | 80.64% | 80.29% | 79.56% | 78.77% | 77.48% |
| DSpark | 87.24% | 84.59% | 83.79% | 83.63% | 83.6% | 83.27% | 82.97% | 82.54% | 82.21% | 82.39% | 81.58% | 80.7% | 81.35% | 80.57% | 79.86% |
| DFlash 2 | 88.3% | 85.3% | 84.98% | 84.88% | 85.41% | 85.3% | 85.36% | 85.13% | 85.95% | 85.99% | 86.41% | 86.46% | 86.43% | 86.02% | 86.48% |

Figure 5. Qwen3.5-4B conditional acceptance rate on MATH-500, same sampling as above.

Figure 5. Qwen3.5-4B conditional acceptance rate on MATH-500, same sampling as above.

## [Two Drafters, Out Today](#two-drafters-out-today)

We are releasing two DFlash 2 drafters today: [one for Qwen3.8-27B](https://huggingface.co/incoai/Qwen3.8-27B-DFlash2) and [one for Meta's Muse Glimmer](https://huggingface.co/incoai/Muse-Glimmer-30B-DFlash2). For Qwen3.8-27B, we compare against the model's native MTP path and a [community DSpark drafter](https://huggingface.co/RadixArk/Qwen3.8-27B-DSpark).

Qwen3.8-27B

| Dataset   | MTP  | DSpark | DFlash 2 |
|-----------|------|--------|----------|
| GSM8K     | 5.02 | 4.36   | **5.46** |
| MATH-500  | 4.72 | 3.92   | **5.28** |
| HumanEval | 3.91 | 3.30   | **4.39** |
| MBPP      | 3.99 | 3.51   | **4.79** |
| MT-Bench  | 3.74 | 3.01   | **4.10** |
| Mean      | 4.28 | 3.62   | **4.80** |

Table 4. Qwen3.8-27B per-request mean acceptance length with the model's default sampling and a block size of 8, against its native MTP path and a community DSpark drafter.

For Meta's Muse Glimmer, we compare against the official DFlash drafter shipped with the model and a [community DSpark drafter](https://huggingface.co/DaoCloud/Muse-Glimmer-30B-DSpark).

Muse Glimmer

| Dataset   | DFlash | DSpark | DFlash 2 |
|-----------|--------|--------|----------|
| GSM8K     | 5.43   | 5.45   | **6.57** |
| MATH-500  | 5.39   | 5.01   | **6.56** |
| HumanEval | 4.11   | 4.33   | **5.66** |
| MBPP      | 3.74   | 4.02   | **5.30** |
| MT-Bench  | 3.52   | 3.59   | **4.42** |
| Mean      | 4.44   | 4.48   | **5.70** |

Table 5. Muse Glimmer per-request mean acceptance length with the model's default sampling and a block size of 16. DFlash is the official drafter Meta ships with the model; DSpark is a community drafter.

The margins are wide: on both models, DFlash 2 averages more than **a full token** ahead of DSpark. It also beats each model's official drafter, MTP on Qwen3.8-27B and DFlash on Muse Glimmer. That translates into **2.7–3.4×** the throughput of autoregressive decoding on Qwen3.8-27B, and **3.1–4.6×** on Muse Glimmer. The [model cards](https://huggingface.co/collections/incoai/dflash-2-6a8432273c9998ce1685d4c5) break the speedups down by task and concurrency.

## [The Bottom Line](#the-bottom-line)

An agent writes in an afternoon what a chatbot writes in a month, and decoding sits under every one of those tokens. DFlash 2 decodes at **close to 3× the speed of autoregressive decoding, about a third of the compute per token**, with the same output.

In seven months, DFlash went from our paper to an industry standard, with more than 3.5 million downloads. Inside the same design, DFlash 2 decodes one more full token per pass, for free. That is only one component of the serving stack. Inference is nowhere near its floor.

At Inco AI, we are building an end-to-end serving stack to keep pushing that floor lower. DFlash 2 is the first piece. Two drafters are out today [on Hugging Face](https://huggingface.co/collections/incoai/dflash-2-6a8432273c9998ce1685d4c5).

If you serve agents at scale and want to evaluate DFlash 2 in your stack, or want a drafter for a model you run, including your own fine-tunes, write to us: <contact@inco.ai>.

We are also hiring. If you want to help build this stack, reach out to us.

**Connect the candidates. Keep drafting parallel.**

Get updates

One email when we ship something new.

Subscribe

We will never share your email address.

## [Citation](#citation)

Please cite this post as:

```
@misc{inco2026dflash2,
  title  = {{DFlash 2: Keep Drafting Parallel}},
  author = {{Inco AI}},
  year   = {2026},
  month  = {August},
  url    = {https://inco.ai/blog/dflash2/}
}
```

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNvcHkgc2l6ZS0zLjUiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cmVjdCB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHg9IjgiIHk9IjgiIHJ4PSIyIiByeT0iMiIgLz48cGF0aCBkPSJNNCAxNmMtMS4xIDAtMi0uOS0yLTJWNGMwLTEuMS45LTIgMi0yaDEwYzEuMSAwIDIgLjkgMiAyIiAvPjwvc3ZnPg==)

## [Footnotes](#footnote-label)

1.  Modal's ["Speculation Is All You Need"](https://modal.com/blog/spec-is-all-u-need) points out that speculative decoding is the optimization that matters for low-latency serving. We are huge fans of their work and appreciate their support and discussions since DFlash's release. [↩](#user-content-fnref-modal)
