<!-- 从 trtllm-overview.html 迁移的资料快照；原始 HTML SHA-256: f2bb1e51a8908df0605df9c29c7238a6f36849667f9834a989e69bf58ab324da。 -->

- [](index.html)
- Overview

<a id="overview"></a>

# Overview
<a id="about-tensorrt-llm"></a>

## About TensorRT LLM
[TensorRT LLM](https://developer.nvidia.com/tensorrt) is NVIDIA’s comprehensive open-source library for accelerating and optimizing inference performance of the latest large language models (LLMs) on NVIDIA GPUs.

<a id="key-capabilities"></a>

## Key Capabilities
<a id="architected-on-pytorch"></a>

### 🔥 **Architected on Pytorch**
TensorRT LLM provides a high-level Python [LLM API](quick-start-guide.html#run-offline-inference-with-llm-api) that supports a wide range of inference setups - from single-GPU to multi-GPU or multi-node deployments. It includes built-in support for various parallelism strategies and advanced features. The LLM API integrates seamlessly with the broader inference ecosystem, including NVIDIA [Dynamo](https://github.com/ai-dynamo/dynamo) and the [Triton Inference Server](https://github.com/triton-inference-server/server).

TensorRT LLM is designed to be modular and easy to modify. Its PyTorch-native architecture allows developers to experiment with the runtime or extend functionality. Several popular models are also pre-defined and can be customized using [native PyTorch code](#source:tensorrt_llm/_torch/models/modeling_deepseekv3.py), making it easy to adapt the system to specific needs.

<a id="state-of-the-art-performance"></a>

### ⚡ **State-of-the-Art Performance**
TensorRT LLM delivers breakthrough performance on the latest NVIDIA GPUs:

- **DeepSeek R1**: [World-record inference performance on Blackwell GPUs](https://developer.nvidia.com/blog/nvidia-blackwell-delivers-world-record-deepseek-r1-inference-performance/)

- **Llama 4 Maverick**: [Breaks the 1,000 TPS/User Barrier on B200 GPUs](https://developer.nvidia.com/blog/blackwell-breaks-the-1000-tps-user-barrier-with-metas-llama-4-maverick/)

<a id="comprehensive-model-support"></a>

### 🎯 **Comprehensive Model Support**
TensorRT LLM supports the latest and most popular LLM and DiT architectures. See [complete list](models/supported-models.html).

- **Language Models**: GPT-OSS, Deepseek-R1/V3, Llama 3/4, Qwen2/3, Gemma 3, Phi 4…

- **Multi-modal Models**: LLaVA-NeXT, Qwen2-VL, VILA, Llama 3.2 Vision…

- **[Visual Generation](models/visual-generation.html) Models**: FLUX, Wan2.1/2.2 for image and video generation.

TensorRT LLM strives to support the most popular models on **Day 0**.

<a id="fp4-support"></a>

### FP4 Support
[NVIDIA B200 GPUs](https://www.nvidia.com/en-us/data-center/dgx-b200/), when used with TensorRT LLM, enable seamless loading of model weights in the new [FP4 format](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/#what_is_nvfp4), allowing you to automatically leverage optimized FP4 kernels for efficient and accurate low-precision inference.

<a id="fp8-support"></a>

### FP8 Support
On NVIDIA H100 and later GPUs, TensorRT LLM supports [FP8 quantization](features/quantization.html), which can double performance and halve memory consumption compared to 16-bit floating point, with minimal impact on model accuracy.

<a id="advanced-optimization-production-features"></a>

### 🚀 **Advanced Optimization & Production Features**
- **[In-Flight Batching & Paged Attention](features/paged-attention-ifb-scheduler.html)**: In-flight batching eliminates wait times by dynamically managing request execution, processing context and generation phases together for maximum GPU utilization and reduced latency.

- **[Multi-GPU Multi-Node Inference](features/parallel-strategy.html)**: Seamless distributed inference with tensor, pipeline, and expert parallelism across multiple GPUs and nodes through the Model Definition API.

- **[Advanced Quantization](features/quantization.html)**:

  - **FP4 Quantization**: Native support on NVIDIA B200 GPUs with optimized FP4 kernels

  - **FP8 Quantization**: Automatic conversion on NVIDIA H100 GPUs leveraging Hopper architecture

- **[Speculative Decoding](features/speculative-decoding.html)**: Multiple algorithms including EAGLE, MTP and NGram

- **[KV Cache Management](features/kvcache.html)**: Paged KV cache with intelligent block reuse and memory optimization

- **[Chunked Prefill](features/paged-attention-ifb-scheduler.html)**: Efficient handling of long sequences by splitting context into manageable chunks

- **[LoRA Support](features/lora.html)**: Multi-adapter support with HuggingFace and NeMo formats, efficient fine-tuning and adaptation

- **[Checkpoint Loading](features/checkpoint-loading.html)**: Flexible model loading from various formats (HuggingFace, NeMo, custom)

- **[Guided Decoding](features/guided-decoding.html)**: Advanced sampling with stop words, bad words, and custom constraints

- **[Disaggregated Serving (Beta)](features/disagg-serving.html)**: Separate context and generation phases across different GPUs for optimal resource utilization

<a id="what-can-you-do-with-tensorrt-llm"></a>

## What Can You Do With TensorRT LLM?
Whether you’re building the next generation of AI applications, optimizing existing LLM deployments, or exploring the frontiers of large language model technology, TensorRT LLM provides the tools, performance, and flexibility you need to succeed in the era of generative AI. To get started, refer to the [Quick Start Guide](quick-start-guide.html#quick-start-guide).

[](index.html "previous page")

previous

Welcome to TensorRT LLM’s Documentation!

[](quick-start-guide.html "next page")

next

Quick Start Guide

On this page

- [About TensorRT LLM](#about-tensorrt-llm)
- [Key Capabilities](#key-capabilities)
  - [🔥 **Architected on Pytorch**](#architected-on-pytorch)
  - [⚡ **State-of-the-Art Performance**](#state-of-the-art-performance)
  - [🎯 **Comprehensive Model Support**](#comprehensive-model-support)
  - [FP4 Support](#fp4-support)
  - [FP8 Support](#fp8-support)
  - [🚀 **Advanced Optimization & Production Features**](#advanced-optimization-production-features)
- [What Can You Do With TensorRT LLM?](#what-can-you-do-with-tensorrt-llm)
