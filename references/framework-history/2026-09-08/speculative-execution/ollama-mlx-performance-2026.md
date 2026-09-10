<!-- 从 ollama-mlx-performance-2026.html 迁移的资料快照；原始 HTML SHA-256: 1141d64e388394c3f9d038241e9a2613683a530a1b7c928c989e6af5e561fb0d。 -->

[![Ollama](/public/ollama.png)](/)

[Models](/search) [Docs](/docs) [Pricing](/pricing)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibXQtMC4yNSBtbC0xLjUgaC01IHctNSBmaWxsLWN1cnJlbnQiIHZpZXdib3g9IjAgMCAyMCAyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgPHBhdGggZD0ibTguNSAzYzMuMDM3NTY2MSAwIDUuNSAyLjQ2MjQzMzg4IDUuNSA1LjUgMCAxLjI0ODMyMDk2LS40MTU4Nzc3IDIuMzk5NTA4NS0xLjExNjY0MTYgMy4zMjI1NzExbDQuMTQ2OTcxNyA0LjE0NzA5ODhjLjI5Mjg5MzIuMjkyODkzMi4yOTI4OTMyLjc2Nzc2NyAwIDEuMDYwNjYwMi0uMjY2MjY2Ni4yNjYyNjY1LS42ODI5MzAzLjI5MDQ3MjYtLjk3NjU0MTguMDcyNjE4MWwtLjA4NDExODQtLjA3MjYxODEtNC4xNDcwOTg4LTQuMTQ2OTcxN2MtLjkyMzA2MjYuNzAwNzYzOS0yLjA3NDI1MDE0IDEuMTE2NjQxNi0zLjMyMjU3MTEgMS4xMTY2NDE2LTMuMDM3NTY2MTIgMC01LjUtMi40NjI0MzM5LTUuNS01LjUgMC0zLjAzNzU2NjEyIDIuNDYyNDMzODgtNS41IDUuNS01LjV6bTAgMS41Yy0yLjIwOTEzOSAwLTQgMS43OTA4NjEtNCA0czEuNzkwODYxIDQgNCA0IDQtMS43OTA4NjEgNC00LTEuNzkwODYxLTQtNC00eiIgLz4KICAgIDwvc3ZnPg==)

[Sign in](/signin) [Download](/download)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTMuNzUgNi43NWgxNi41TTMuNzUgMTJoMTYuNW0tMTYuNSA1LjI1aDE2LjUiIC8+CiAgICAgICAgPC9zdmc+) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTYgMThMMTggNk02IDZsMTIgMTIiIC8+CiAgICAgICAgPC9zdmc+)

[Models](/search) [Download](/download) [Docs](/docs) [Pricing](/pricing) [Sign in](/signin)

# Ollama's highest performance on Apple Silicon yet with MLX

## June 11, 2026

Ollama’s MLX engine has been updated to deliver its highest performance on Apple Silicon yet. By leaning more heavily on Apple’s unified memory and the Metal-backed [MLX](https://github.com/ml-explore/mlx) framework, models output higher quality responses, respond faster, and use less memory.

Your browser does not support the video tag.

A coding agent with Gemma 4 12B on a MacBook Pro M5 Max. Ollama's improved MLX engine provides higher-quality results, higher output speeds and faster time to first token with thinking and multiple sub-agents.

## Higher quality responses with NVFP4

Ollama’s MLX engine has been updated to support NVIDIA’s model-optimized [NVFP4](https://developer.nvidia.com/blog/introducing-nvfp4-for-efficient-and-accurate-low-precision-inference/) format, allowing for higher quality outputs than other 4-bit quantization formats while maintaining state-of-the-art performance. As an added benefit, models that are optimized for datacenter deployment can now be imported and run on with Ollama’s MLX engine allowing for portability between the datacenter and the desktop.

NVFP4 tracks the local dynamic range of model weights more closely, reducing loss from quantization. When measuring the perplexity difference between `q4_K_M`, a common 4-bit quantization format available with Ollama, NVFP4, and unquantized bf16 weights for the Gemma 4 12B model, model-optimized NVFP4 roughly halves the quality loss while maintaining performance:

Perplexity

Gemma 4 12B – lower is better

NVFP4 roughly halves the quality loss of 4-bit quantization, relative to unquantized BF16.

## Faster output performance

Ollama’s MLX engine is now up to 20% faster from new optimizations: several operations are now fused into single Metal kernels via MLX’s just-in-time compiler features, and we’ve reworked Ollama’s GPU-backed sampling to run more efficiently.

Output speed

tokens/s · higher is better

NVFP4 generates about 20% faster than q4_K_M on the updated engine.  
Average output speed over 10 runs when provided an 8,300-token input prompt.

## More responsive with agent workflows

Agent workloads are dominated by prompt processing. Every tool call is a new request, and every request resends the whole transcript: system prompt, tool definitions, and every file read so far. Over a single task the model ends up processing the same context dozens of times. Prefix caching avoids the repeated work, as long as each request picks up where the last one left off.

Real agent sessions don’t work that way for long. Ollama’s new snapshot system saves model state at key points across conversations, using the same approach that serves agent workloads in Ollama’s cloud:

- **Multiple agents:** An agent hands off to a subagent and picks back up later, or two sessions run at the same time. Each one resumes from its own saved state, and anything they have in common — often tens of thousands of tokens of system prompt, tool definitions, and ingested files — is only processed once.

- **Thinking models:** Reasoning tokens are generated, then dropped from the conversation history, so the next request never matches the state the engine just built. Each turn would normally reprocess the whole conversation. A snapshot taken right before the response starts gives the next turn somewhere to resume from.

- **Branching and retries:** A different follow-up or a regenerated response diverges from the cached conversation instead of extending it. Because snapshots exist where conversations split, only the new direction needs to be processed.

Most new models make this harder than it sounds. Sliding-window attention and recurrent layers carry state that can’t be rewound. Once the model moves past a point in the conversation, that point can’t be recovered unless state was saved at the time. Ollama saves state at the points conversations are likely to return to: where they branch, at intervals through long prompts, and just before each response. Keeping snapshots selective and incremental leaves more memory for the model.

## Get started

To run models with Ollama’s MLX engine, [download](https://ollama.com/download) the latest version of Ollama, then run a model:

    ollama run gemma4:12b-mlx

For use in a coding agent, use `ollama launch`:

    ollama launch pi --model gemma4:12b-mlx

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
