<!-- 从 ollama-memory-2025.html 迁移的资料快照；原始 HTML SHA-256: 532413c74d08c4351531e03c63595b57cb7d29dc7886041d81b8d67ab3e36c0f。 -->

[![Ollama](/public/ollama.png)](/)

[Models](/search) [Docs](/docs) [Pricing](/pricing)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibXQtMC4yNSBtbC0xLjUgaC01IHctNSBmaWxsLWN1cnJlbnQiIHZpZXdib3g9IjAgMCAyMCAyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgPHBhdGggZD0ibTguNSAzYzMuMDM3NTY2MSAwIDUuNSAyLjQ2MjQzMzg4IDUuNSA1LjUgMCAxLjI0ODMyMDk2LS40MTU4Nzc3IDIuMzk5NTA4NS0xLjExNjY0MTYgMy4zMjI1NzExbDQuMTQ2OTcxNyA0LjE0NzA5ODhjLjI5Mjg5MzIuMjkyODkzMi4yOTI4OTMyLjc2Nzc2NyAwIDEuMDYwNjYwMi0uMjY2MjY2Ni4yNjYyNjY1LS42ODI5MzAzLjI5MDQ3MjYtLjk3NjU0MTguMDcyNjE4MWwtLjA4NDExODQtLjA3MjYxODEtNC4xNDcwOTg4LTQuMTQ2OTcxN2MtLjkyMzA2MjYuNzAwNzYzOS0yLjA3NDI1MDE0IDEuMTE2NjQxNi0zLjMyMjU3MTEgMS4xMTY2NDE2LTMuMDM3NTY2MTIgMC01LjUtMi40NjI0MzM5LTUuNS01LjUgMC0zLjAzNzU2NjEyIDIuNDYyNDMzODgtNS41IDUuNS01LjV6bTAgMS41Yy0yLjIwOTEzOSAwLTQgMS43OTA4NjEtNCA0czEuNzkwODYxIDQgNCA0IDQtMS43OTA4NjEgNC00LTEuNzkwODYxLTQtNC00eiIgLz4KICAgIDwvc3ZnPg==)

[Sign in](/signin) [Download](/download)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTMuNzUgNi43NWgxNi41TTMuNzUgMTJoMTYuNW0tMTYuNSA1LjI1aDE2LjUiIC8+CiAgICAgICAgPC9zdmc+) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTYgMThMMTggNk02IDZsMTIgMTIiIC8+CiAgICAgICAgPC9zdmc+)

[Models](/search) [Download](/download) [Docs](/docs) [Pricing](/pricing) [Sign in](/signin)

# New model scheduling

## September 23, 2025

[![Ollama waiting in line](/public/blog/waiting.png)](/download)

Ollama now includes a significantly improved model scheduling system. Ahead of running a model, Ollama’s new engine will now measure the *exact* amount of memory required compared to an estimation in previous versions of Ollama. This has several benefits:

- **Significantly reduced crashes due to out of memory issues:** Because memory management is exact, over-allocations no longer occur meaning fewer out of memory issues.
- **Maximizing GPU utilization:** Ollama’s new memory management allocates more memory to the GPU, increasing token generation and processing speeds
- **Multi-GPU performance:** Ollama will now schedule models more efficiently over multiple GPUs, significantly improving multi-GPU and mismatched GPU performance
- **Accurate reporting:** Measurements in tools like `nvidia-smi` will now match `ollama ps` making it easy to track memory utilization on your system

All models implemented in Ollama’s new engine now have this new feature enabled by default, with more models coming soon as they transition to Ollama’s new engine.

## Examples

### Long context

- GPU: 1x NVIDIA GeForce RTX 4090
- Model: `gemma3:12b`
- Context length: 128k

| Old | New |
|----|----|
| 52.02 tokens/s token generation speed | 85.54 tokens/s token generation speed |
| 19.9GiB of VRAM | 21.4GiB of VRAM |
| ⁴⁸⁄₄₉ layers loaded on GPU | ⁴⁹⁄₄₉ layers loaded on GPU |

### Image input

- GPU: 2x NVIDIA GeForce RTX 4090
- Model: `mistral-small3.2`
- Context length: 32k

| Old | New |
|----|----|
| 127.84 tokens/s prompt evaluation speed | 1380.24 tokens/s prompt evaluation speed |
| 43.15 tokens/s token generation speed | 55.61 tokens/s token generation speed |
| 19.9GiB of VRAM | 21.4GiB of VRAM |
| ⁴⁰⁄₄₁ layers loaded on GPU | ⁴¹⁄₄₁ layers loaded on GPU + vision model |

## Supported models

All models implemented in Ollama’s new engine use the new memory management features:

- [`gpt-oss`](https://ollama.com/library/gpt-oss)
- [`llama4`](https://ollama.com/library/llama4), [`llama3.2-vision`](https://ollama.com/library/llama3.2-vision) (soon: [`llama3.2`](https://ollama.com/library/llama3.2-vision), [`llama3.1`](https://ollama.com/library/llama3.1), [`llama3`](https://ollama.com/library/llama3))
- [`gemma3`](https://ollama.com/library/gemma3), [`embeddinggemma`](https://ollama.com/library/embeddinggemma), [`gemma3n`](https://ollama.com/library/gemma3n)
- [`qwen3`](https://ollama.com/library/qwen3), [`qwen2.5vl`](https://ollama.com/library/qwen2.5vl) (soon: [`qwen3-coder`](https://ollama.com/library/qwen3-coder))
- [`mistral-small3.2`](https://ollama.com/library/mistral-small3.2)
- [`all-minilm`](https://ollama.com/library/all-minilm) and other embedding models

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
