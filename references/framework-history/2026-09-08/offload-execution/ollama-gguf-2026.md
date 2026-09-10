<!-- 从 ollama-gguf-2026.html 迁移的资料快照；原始 HTML SHA-256: 7db1ea4375143816216e0474425d68a58818b9fad8b6cb1a82c47d609aaa553d。 -->

[![Ollama](/public/ollama.png)](/)

[Models](/search) [Docs](/docs) [Pricing](/pricing)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibXQtMC4yNSBtbC0xLjUgaC01IHctNSBmaWxsLWN1cnJlbnQiIHZpZXdib3g9IjAgMCAyMCAyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgPHBhdGggZD0ibTguNSAzYzMuMDM3NTY2MSAwIDUuNSAyLjQ2MjQzMzg4IDUuNSA1LjUgMCAxLjI0ODMyMDk2LS40MTU4Nzc3IDIuMzk5NTA4NS0xLjExNjY0MTYgMy4zMjI1NzExbDQuMTQ2OTcxNyA0LjE0NzA5ODhjLjI5Mjg5MzIuMjkyODkzMi4yOTI4OTMyLjc2Nzc2NyAwIDEuMDYwNjYwMi0uMjY2MjY2Ni4yNjYyNjY1LS42ODI5MzAzLjI5MDQ3MjYtLjk3NjU0MTguMDcyNjE4MWwtLjA4NDExODQtLjA3MjYxODEtNC4xNDcwOTg4LTQuMTQ2OTcxN2MtLjkyMzA2MjYuNzAwNzYzOS0yLjA3NDI1MDE0IDEuMTE2NjQxNi0zLjMyMjU3MTEgMS4xMTY2NDE2LTMuMDM3NTY2MTIgMC01LjUtMi40NjI0MzM5LTUuNS01LjUgMC0zLjAzNzU2NjEyIDIuNDYyNDMzODgtNS41IDUuNS01LjV6bTAgMS41Yy0yLjIwOTEzOSAwLTQgMS43OTA4NjEtNCA0czEuNzkwODYxIDQgNCA0IDQtMS43OTA4NjEgNC00LTEuNzkwODYxLTQtNC00eiIgLz4KICAgIDwvc3ZnPg==)

[Sign in](/signin) [Download](/download)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTMuNzUgNi43NWgxNi41TTMuNzUgMTJoMTYuNW0tMTYuNSA1LjI1aDE2LjUiIC8+CiAgICAgICAgPC9zdmc+) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTYgMThMMTggNk02IDZsMTIgMTIiIC8+CiAgICAgICAgPC9zdmc+)

[Models](/search) [Download](/download) [Docs](/docs) [Pricing](/pricing) [Sign in](/signin)

# Improved performance and model support with GGUF

## June 5, 2026

[Ollama 0.30](https://ollama.com/download) is now available with improved performance and GGUF model compatibility through [llama.cpp](https://github.com/ggml-org/llama.cpp). This augments Ollama’s [MLX engine](/blog/mlx) on Apple silicon, bringing support to more models on a wider range of hardware.

## Performance across more GPUs

### Faster throughput on NVIDIA hardware

With [Ollama 0.30](https://ollama.com/download), performance on NVIDIA hardware is now up to 20% faster, leveraging optimizations contributed by the NVIDIA and llama.cpp teams.

![Tested with the Gemma 4 26B model running on an NVIDIA RTX 5090 using the Q4_K_M quantization.](https://files.ollama.com/030nvidia_throughput.png)

*Tested with the Gemma 4 26B model running on an NVIDIA RTX 5090 using the Q4_K_M quantization.*

### Wider hardware support with Vulkan

Vulkan is now enabled by default, extending Ollama’s GPU acceleration to a wider range of hardware, including AMD and Intel devices. More users can now run models on the GPU out of the box, without installing vendor-specific libraries.

## Support for more models

[Ollama 0.30](https://ollama.com/download) expands compatibility with the GGUF ecosystem, so more models run out of the box—including model families such as [LFM](https://huggingface.co/LiquidAI/LFM2-8B-A1B-GGUF) and [Prism](https://huggingface.co/prism-ml/Bonsai-8B-gguf), as well as fine-tuned models published by [Unsloth](https://unsloth.ai/docs/get-started/unsloth-model-catalog).

### Run GGUF models from Hugging Face

To use a model, first download the GGUF file or a directory containing GGUF files. Next, create a `Modelfile` with the `FROM` command pointing to the path of the GGUF file (or directory):

    FROM ./my-model.Q4_K_M.gguf

Then create and run the model:

``` bash
ollama create -f Modelfile my-model
ollama run my-model
```

### Coding agents and assistants

If a model supports tool calling, that capability carries over to Ollama. You can use these models with your favorite coding agents and personal assistants in a single command.

**Claude Code**

``` bash
ollama launch claude --model my-model
```

**Hermes Agent**

``` bash
ollama launch hermes --model my-model
```

**OpenClaw**

``` bash
ollama launch openclaw --model my-model
```

To verify that a GGUF file supports tool calling, look for the `tools` capability with `ollama show`:

``` bash
ollama show my-model
```

## Acknowledgements

We’d like to acknowledge the work done by Georgi Gerganov and the llama.cpp maintainer teams, as well as hardware partners including NVIDIA, AMD, Qualcomm, and Intel, who have worked hard to optimize performance with the GGML ecosystem on their respective platforms.

If you have any feedback, join [Ollama’s Discord](https://discord.gg/ollama) or reach out at hello@ollama.com.

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
