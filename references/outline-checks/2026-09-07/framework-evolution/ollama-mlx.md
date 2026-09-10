<!-- 从 ollama-mlx.html 迁移的资料快照；原始 HTML SHA-256: 2590f4068f2280522bfd9f24b334a87f47638a382e717155f34828119a0be2d1。 -->

[![Ollama](/public/ollama.png)](/)

[Models](/search) [Docs](/docs) [Pricing](/pricing)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibXQtMC4yNSBtbC0xLjUgaC01IHctNSBmaWxsLWN1cnJlbnQiIHZpZXdib3g9IjAgMCAyMCAyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgPHBhdGggZD0ibTguNSAzYzMuMDM3NTY2MSAwIDUuNSAyLjQ2MjQzMzg4IDUuNSA1LjUgMCAxLjI0ODMyMDk2LS40MTU4Nzc3IDIuMzk5NTA4NS0xLjExNjY0MTYgMy4zMjI1NzExbDQuMTQ2OTcxNyA0LjE0NzA5ODhjLjI5Mjg5MzIuMjkyODkzMi4yOTI4OTMyLjc2Nzc2NyAwIDEuMDYwNjYwMi0uMjY2MjY2Ni4yNjYyNjY1LS42ODI5MzAzLjI5MDQ3MjYtLjk3NjU0MTguMDcyNjE4MWwtLjA4NDExODQtLjA3MjYxODEtNC4xNDcwOTg4LTQuMTQ2OTcxN2MtLjkyMzA2MjYuNzAwNzYzOS0yLjA3NDI1MDE0IDEuMTE2NjQxNi0zLjMyMjU3MTEgMS4xMTY2NDE2LTMuMDM3NTY2MTIgMC01LjUtMi40NjI0MzM5LTUuNS01LjUgMC0zLjAzNzU2NjEyIDIuNDYyNDMzODgtNS41IDUuNS01LjV6bTAgMS41Yy0yLjIwOTEzOSAwLTQgMS43OTA4NjEtNCA0czEuNzkwODYxIDQgNCA0IDQtMS43OTA4NjEgNC00LTEuNzkwODYxLTQtNC00eiIgLz4KICAgIDwvc3ZnPg==)

[Sign in](/signin) [Download](/download)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTMuNzUgNi43NWgxNi41TTMuNzUgMTJoMTYuNW0tMTYuNSA1LjI1aDE2LjUiIC8+CiAgICAgICAgPC9zdmc+) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTYgMThMMTggNk02IDZsMTIgMTIiIC8+CiAgICAgICAgPC9zdmc+)

[Models](/search) [Download](/download) [Docs](/docs) [Pricing](/pricing) [Sign in](/signin)

# Ollama is now powered by MLX on Apple Silicon in preview

## March 30, 2026

![Illustration of Ollama standing beside a fast car that can be run both as a daily driver and go on to win races. Ollama is here to demonstrate high performance on Apple silicon](https://files.ollama.com/ollama_mlx.png)

Today, we’re previewing the fastest way to run Ollama on Apple silicon, powered by MLX, Apple’s machine learning framework.

This unlocks new performance to **accelerate your most demanding work on macOS:**

- Personal assistants like OpenClaw

- Coding agents like Claude Code, OpenCode, or Codex  
    

  Accelerate coding agents like Pi or Claude Code

    

  OpenClaw now responds much faster

    

### Fastest performance on Apple silicon, powered by MLX

Ollama on Apple silicon is now built on top of Apple’s machine learning framework, MLX, to take advantage of its unified memory architecture.

This results in a large speedup of Ollama on all Apple Silicon devices. On Apple’s M5, M5 Pro and M5 Max chips, Ollama leverages the new GPU Neural Accelerators to accelerate both time to first token (TTFT) and generation speed (tokens per second).

Prefill performance

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQwIDIxMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBzdHlsZT0id2lkdGg6MTAwJTtmb250LWZhbWlseTpzeXN0ZW0tdWksc2Fucy1zZXJpZjsiPgo8bGluZSB4MT0iNTAiIHkxPSIyMCIgeDI9IjUwIiB5Mj0iMTcwIiBzdHJva2U9IiNlMGUwZTAiIHN0cm9rZS13aWR0aD0iMSI+PC9saW5lPgo8bGluZSB4MT0iNTAiIHkxPSIxNzAiIHgyPSIyMjAiIHkyPSIxNzAiIHN0cm9rZT0iI2UwZTBlMCIgc3Ryb2tlLXdpZHRoPSIxIj48L2xpbmU+CjxsaW5lIHgxPSI1MCIgeTE9IjIwIiB4Mj0iMjIwIiB5Mj0iMjAiIHN0cm9rZT0iI2UwZTBlMCIgc3Ryb2tlLXdpZHRoPSIwLjUiIHN0cm9rZS1kYXNoYXJyYXk9IjQiPjwvbGluZT4KPGxpbmUgeDE9IjUwIiB5MT0iNTcuNSIgeDI9IjIyMCIgeTI9IjU3LjUiIHN0cm9rZT0iI2UwZTBlMCIgc3Ryb2tlLXdpZHRoPSIwLjUiIHN0cm9rZS1kYXNoYXJyYXk9IjQiPjwvbGluZT4KPGxpbmUgeDE9IjUwIiB5MT0iOTUiIHgyPSIyMjAiIHkyPSI5NSIgc3Ryb2tlPSIjZTBlMGUwIiBzdHJva2Utd2lkdGg9IjAuNSIgc3Ryb2tlLWRhc2hhcnJheT0iNCI+PC9saW5lPgo8bGluZSB4MT0iNTAiIHkxPSIxMzIuNSIgeDI9IjIyMCIgeTI9IjEzMi41IiBzdHJva2U9IiNlMGUwZTAiIHN0cm9rZS13aWR0aD0iMC41IiBzdHJva2UtZGFzaGFycmF5PSI0Ij48L2xpbmU+Cjx0ZXh0IHg9IjQ1IiB5PSIxNzQiIHRleHQtYW5jaG9yPSJlbmQiIGZvbnQtc2l6ZT0iOSIgZmlsbD0iIzk5OSI+MDwvdGV4dD4KPHRleHQgeD0iNDUiIHk9IjEzNi41IiB0ZXh0LWFuY2hvcj0iZW5kIiBmb250LXNpemU9IjkiIGZpbGw9IiM5OTkiPjUwMDwvdGV4dD4KPHRleHQgeD0iNDUiIHk9Ijk5IiB0ZXh0LWFuY2hvcj0iZW5kIiBmb250LXNpemU9IjkiIGZpbGw9IiM5OTkiPjEwMDA8L3RleHQ+Cjx0ZXh0IHg9IjQ1IiB5PSI2MS41IiB0ZXh0LWFuY2hvcj0iZW5kIiBmb250LXNpemU9IjkiIGZpbGw9IiM5OTkiPjE1MDA8L3RleHQ+Cjx0ZXh0IHg9IjQ1IiB5PSIyNCIgdGV4dC1hbmNob3I9ImVuZCIgZm9udC1zaXplPSI5IiBmaWxsPSIjOTk5Ij4yMDAwPC90ZXh0Pgo8dGV4dCB4PSIxMCIgeT0iOTkiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iOCIgZmlsbD0iIzk5OSIgdHJhbnNmb3JtPSJyb3RhdGUoLTkwLDEwLDk5KSI+dG9rZW5zL3M8L3RleHQ+CjxwYXRoIGQ9Ik03NSwzMy42NSBRNzUsMjUuNjUgODMsMjUuNjUgTDEyNywyNS42NSBRMTM1LDI1LjY1IDEzNSwzMy42NSBMMTM1LDE3MCBMNzUsMTcwIFoiIGZpbGw9IiMwMDAiIC8+Cjx0ZXh0IHg9IjEwNSIgeT0iMjAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTEiIGZvbnQtd2VpZ2h0PSI2MDAiIGZpbGw9IiMwMDAiPjE4MTA8L3RleHQ+Cjx0ZXh0IHg9IjEwNSIgeT0iMTg4IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXNpemU9IjEwIiBmaWxsPSIjNTU1Ij5PbGxhbWEgMC4xOTwvdGV4dD4KPHBhdGggZD0iTTE1MCw5MS4zNSBRMTUwLDgzLjM1IDE1OCw4My4zNSBMMjAyLDgzLjM1IFEyMTAsODMuMzUgMjEwLDkxLjM1IEwyMTAsMTcwIEwxNTAsMTcwIFoiIGZpbGw9IiNhYWEiIC8+Cjx0ZXh0IHg9IjE4MCIgeT0iNzgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTEiIGZvbnQtd2VpZ2h0PSI2MDAiIGZpbGw9IiM1NTUiPjExNTQ8L3RleHQ+Cjx0ZXh0IHg9IjE4MCIgeT0iMTg4IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXNpemU9IjEwIiBmaWxsPSIjNTU1Ij5PbGxhbWEgMC4xODwvdGV4dD4KPC9zdmc+)

Decode performance

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIDAgMjQwIDIxMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBzdHlsZT0id2lkdGg6MTAwJTtmb250LWZhbWlseTpzeXN0ZW0tdWksc2Fucy1zZXJpZjsiPgo8bGluZSB4MT0iNTAiIHkxPSIyMCIgeDI9IjUwIiB5Mj0iMTcwIiBzdHJva2U9IiNlMGUwZTAiIHN0cm9rZS13aWR0aD0iMSI+PC9saW5lPgo8bGluZSB4MT0iNTAiIHkxPSIxNzAiIHgyPSIyMjAiIHkyPSIxNzAiIHN0cm9rZT0iI2UwZTBlMCIgc3Ryb2tlLXdpZHRoPSIxIj48L2xpbmU+CjxsaW5lIHgxPSI1MCIgeTE9IjIwIiB4Mj0iMjIwIiB5Mj0iMjAiIHN0cm9rZT0iI2UwZTBlMCIgc3Ryb2tlLXdpZHRoPSIwLjUiIHN0cm9rZS1kYXNoYXJyYXk9IjQiPjwvbGluZT4KPGxpbmUgeDE9IjUwIiB5MT0iNTcuNSIgeDI9IjIyMCIgeTI9IjU3LjUiIHN0cm9rZT0iI2UwZTBlMCIgc3Ryb2tlLXdpZHRoPSIwLjUiIHN0cm9rZS1kYXNoYXJyYXk9IjQiPjwvbGluZT4KPGxpbmUgeDE9IjUwIiB5MT0iOTUiIHgyPSIyMjAiIHkyPSI5NSIgc3Ryb2tlPSIjZTBlMGUwIiBzdHJva2Utd2lkdGg9IjAuNSIgc3Ryb2tlLWRhc2hhcnJheT0iNCI+PC9saW5lPgo8bGluZSB4MT0iNTAiIHkxPSIxMzIuNSIgeDI9IjIyMCIgeTI9IjEzMi41IiBzdHJva2U9IiNlMGUwZTAiIHN0cm9rZS13aWR0aD0iMC41IiBzdHJva2UtZGFzaGFycmF5PSI0Ij48L2xpbmU+Cjx0ZXh0IHg9IjQ1IiB5PSIxNzQiIHRleHQtYW5jaG9yPSJlbmQiIGZvbnQtc2l6ZT0iOSIgZmlsbD0iIzk5OSI+MDwvdGV4dD4KPHRleHQgeD0iNDUiIHk9IjEzNi41IiB0ZXh0LWFuY2hvcj0iZW5kIiBmb250LXNpemU9IjkiIGZpbGw9IiM5OTkiPjQwPC90ZXh0Pgo8dGV4dCB4PSI0NSIgeT0iOTkiIHRleHQtYW5jaG9yPSJlbmQiIGZvbnQtc2l6ZT0iOSIgZmlsbD0iIzk5OSI+ODA8L3RleHQ+Cjx0ZXh0IHg9IjQ1IiB5PSI2MS41IiB0ZXh0LWFuY2hvcj0iZW5kIiBmb250LXNpemU9IjkiIGZpbGw9IiM5OTkiPjEyMDwvdGV4dD4KPHRleHQgeD0iNDUiIHk9IjI0IiB0ZXh0LWFuY2hvcj0iZW5kIiBmb250LXNpemU9IjkiIGZpbGw9IiM5OTkiPjE2MDwvdGV4dD4KPHRleHQgeD0iMTAiIHk9Ijk5IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXNpemU9IjgiIGZpbGw9IiM5OTkiIHRyYW5zZm9ybT0icm90YXRlKC05MCwxMCw5OSkiPnRva2Vucy9zPC90ZXh0Pgo8cGF0aCBkPSJNNzUsNzMgUTc1LDY1IDgzLDY1IEwxMjcsNjUgUTEzNSw2NSAxMzUsNzMgTDEzNSwxNzAgTDc1LDE3MCBaIiBmaWxsPSIjMDAwIiAvPgo8dGV4dCB4PSIxMDUiIHk9IjU5IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXNpemU9IjExIiBmb250LXdlaWdodD0iNjAwIiBmaWxsPSIjMDAwIj4xMTI8L3RleHQ+Cjx0ZXh0IHg9IjEwNSIgeT0iMTg4IiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXNpemU9IjEwIiBmaWxsPSIjNTU1Ij5PbGxhbWEgMC4xOTwvdGV4dD4KPHBhdGggZD0iTTE1MCwxMjMuNjMgUTE1MCwxMTUuNjMgMTU4LDExNS42MyBMMjAyLDExNS42MyBRMjEwLDExNS42MyAyMTAsMTIzLjYzIEwyMTAsMTcwIEwxNTAsMTcwIFoiIGZpbGw9IiNhYWEiIC8+Cjx0ZXh0IHg9IjE4MCIgeT0iMTEwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmb250LXNpemU9IjExIiBmb250LXdlaWdodD0iNjAwIiBmaWxsPSIjNTU1Ij41ODwvdGV4dD4KPHRleHQgeD0iMTgwIiB5PSIxODgiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtc2l6ZT0iMTAiIGZpbGw9IiM1NTUiPk9sbGFtYSAwLjE4PC90ZXh0Pgo8L3N2Zz4=)

Testing was conducted on March 29, 2026, using Alibaba’s Qwen3.5-35B-A3B model quantized to NVFP4 and Ollama’s previous implementation quantized to Q4_K_M using Ollama 0.18. Ollama 0.19 will see even higher performance (1851 token/s prefill and 134 token/s decode when running with int4 quantization).

### NVFP4 support: higher quality responses and production parity

Ollama now leverages NVIDIA’s [NVFP4](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/) format to maintain model accuracy while reducing memory bandwidth and storage requirements for inference workloads.

As more inference providers scale inference using NVFP4 format, this allows Ollama users to share the same results as they would in a production environment.

It further opens up Ollama to have the ability to run models optimized by NVIDIA’s [model optimizer](https://github.com/NVIDIA/Model-Optimizer). Other precisions will be made available based on the design and usage intent from Ollama’s research and hardware partners.

### Improved caching for more responsiveness

Ollama’s cache has been upgraded to make coding and agentic tasks more efficient.

- **Lower memory utilization:** Ollama will now reuse its cache across conversations, meaning less memory utilization and more cache hits when branching when using a shared system prompt with tools like Claude Code.

- **Intelligent checkpoints:** Ollama will now store snapshots of its cache at intelligent locations in the prompt, resulting in less prompt processing and faster responses.

- **Smarter eviction:** shared prefixes survive longer even when older branches are dropped.

### Get started

[Download Ollama 0.19](https://ollama.com/download)

This preview release of Ollama accelerates the new [Qwen3.5-35B-A3B](https://ollama.com/library/qwen3.5) model, with sampling parameters tuned for coding tasks.

Please make sure you have a Mac with more than 32GB of unified memory.

**Claude Code:**

    ollama launch claude --model qwen3.5:35b-a3b-coding-nvfp4

**OpenClaw:**

    ollama launch openclaw --model qwen3.5:35b-a3b-coding-nvfp4

**Chat with the model:**

    ollama run qwen3.5:35b-a3b-coding-nvfp4

### Future models

We are actively working to support future models. For users with custom models fine-tuned on supported architectures, we will introduce an easier way to import models into Ollama. In the meantime, we will expand the list of supported architectures.

### Acknowledgments

Thank you to:

- The MLX contributor team who built an incredible acceleration framework
- NVIDIA contributors to NVFP4 quantization, NVFP4 model optimizer, MLX CUDA support, Ollama optimizations and testing
- The GGML & llama.cpp team who built a thriving local framework and community
- The Alibaba Qwen team for open-sourcing excellent models and their collaboration

© 2026 Ollama

[Download](/download) [Blog](/blog) [Docs](https://docs.ollama.com) [GitHub](https://github.com/ollama/ollama) [Discord](https://discord.com/invite/ollama) [X (Twitter)](https://twitter.com/ollama) [Support](mailto:support@ollama.com) [Careers](https://jobs.ashbyhq.com/ollama) [Privacy](/privacy) [Terms](/terms)

- [Blog](/blog)
- [Download](/download)
- [Docs](https://docs.ollama.com)

&nbsp;

- [GitHub](https://github.com/ollama/ollama)
- [Discord](https://discord.com/invite/ollama)
- [X (Twitter)](https://twitter.com/ollama)
- [Meetups](https://lu.ma/ollama)
- [Careers](https://jobs.ashbyhq.com/ollama)
- [Privacy](/privacy)
- [Terms](/terms)

© 2026 Ollama Inc.
