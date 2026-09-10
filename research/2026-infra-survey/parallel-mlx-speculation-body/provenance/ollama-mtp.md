<!-- 从 ollama-mtp.html 迁移的资料快照；原始 HTML SHA-256: b63b0c4e4c20ee6b884e40f98cf9c71ed8336d145c0c13fb2acf143a7ceecc29。 -->

[![Ollama](/public/ollama.png)](/)

[Models](/search) [Docs](/docs) [Pricing](/pricing)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibXQtMC4yNSBtbC0xLjUgaC01IHctNSBmaWxsLWN1cnJlbnQiIHZpZXdib3g9IjAgMCAyMCAyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgPHBhdGggZD0ibTguNSAzYzMuMDM3NTY2MSAwIDUuNSAyLjQ2MjQzMzg4IDUuNSA1LjUgMCAxLjI0ODMyMDk2LS40MTU4Nzc3IDIuMzk5NTA4NS0xLjExNjY0MTYgMy4zMjI1NzExbDQuMTQ2OTcxNyA0LjE0NzA5ODhjLjI5Mjg5MzIuMjkyODkzMi4yOTI4OTMyLjc2Nzc2NyAwIDEuMDYwNjYwMi0uMjY2MjY2Ni4yNjYyNjY1LS42ODI5MzAzLjI5MDQ3MjYtLjk3NjU0MTguMDcyNjE4MWwtLjA4NDExODQtLjA3MjYxODEtNC4xNDcwOTg4LTQuMTQ2OTcxN2MtLjkyMzA2MjYuNzAwNzYzOS0yLjA3NDI1MDE0IDEuMTE2NjQxNi0zLjMyMjU3MTEgMS4xMTY2NDE2LTMuMDM3NTY2MTIgMC01LjUtMi40NjI0MzM5LTUuNS01LjUgMC0zLjAzNzU2NjEyIDIuNDYyNDMzODgtNS41IDUuNS01LjV6bTAgMS41Yy0yLjIwOTEzOSAwLTQgMS43OTA4NjEtNCA0czEuNzkwODYxIDQgNCA0IDQtMS43OTA4NjEgNC00LTEuNzkwODYxLTQtNC00eiIgLz4KICAgIDwvc3ZnPg==)

[Sign in](/signin) [Download](/download)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTMuNzUgNi43NWgxNi41TTMuNzUgMTJoMTYuNW0tMTYuNSA1LjI1aDE2LjUiIC8+CiAgICAgICAgPC9zdmc+) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTYgMThMMTggNk02IDZsMTIgMTIiIC8+CiAgICAgICAgPC9zdmc+)

[Models](/search) [Download](/download) [Docs](/docs) [Pricing](/pricing) [Sign in](/signin)

# Faster Gemma 4 on MLX with multi-token prediction

## June 29, 2026

Gemma 4 is now significantly faster in Ollama 0.31. On Apple Silicon, it generates tokens **nearly 90% faster** on average across a coding-agent benchmark. The speedup is on by default, and it does not change the model’s output:

The speedup comes from multi-token prediction (MTP). Gemma 4 ships with a small, fast draft model that runs alongside the main model and proposes the next several tokens. The main model then verifies that proposal in a single pass and keeps the tokens it agrees with. Because the draft model is a small fraction of the main model’s size, its proposals are inexpensive, and when they are correct the model commits several tokens for the cost of one.

Code is especially predictable. It is full of closing brackets, repeated identifiers, and boilerplate, so the draft model’s proposals are accepted often. This matters most for coding agents, which call the model continuously as they read files, run tools, and work through a task. Faster generation makes those agents noticeably more responsive.

Achieving this reliably is the difficult part. The ideal number of tokens to draft changes from one moment to the next, and drafting too many can make MTP slower than not speculating at all. Ollama tunes this automatically as the model runs, so the speedup requires no configuration.

We measured this on the Aider polyglot benchmark, which runs a real coding agent through real programming tasks. The benefit from MTP depends heavily on the workload, and a synthetic benchmark can be made to show almost any result. These numbers reflect what to expect in practice.

Generation speed

tokens/s · higher is better

With MTP, Gemma 4 generates tokens nearly 90% faster on the Aider polyglot benchmark.  
Gemma 4 12B (nvfp4) on an M5 Max.

## How it works

Three changes work together: how the draft length is chosen, how the engine runs each round, and how the GPU handles the work.

### Auto-tuning the draft length

There is no single best number of tokens to draft before verifying. It depends on the model, how it is quantized, the hardware, and how predictable the text is at any given moment. A value that works well on one setup can be wrong on another. Drafting too few leaves performance on the table. Drafting too many spends more time checking rejected proposals than it saves, and MTP ends up slower than plain decoding.

Ollama determines the draft length at runtime. As it generates, it tracks how often proposals are accepted and how long each verification pass takes, then selects the length that produces the most tokens per second. It continues adjusting as the text changes, and when proposals stop being accepted it returns to plain one-at-a-time decoding. Speculation therefore does not slow generation down when it stops helping.

### Speculative decoding in the engine

Each round begins with the draft model. It predicts a token, feeds that token back in to predict the next, and repeats until it has a short run of proposals. The main model then verifies the entire run at once, sampling at each position to determine which proposals are accepted. All of this runs on the GPU as a single pass: drafting, sampling, verification, and the sampling that follows, with no return to the CPU in between.

Accepted tokens are kept. The rejected ones are more involved, because by the time they are rejected they have already written into the cache, the running state the model reuses to avoid recomputing earlier tokens. Undoing them is inexpensive. The engine records a rollback point before each proposal, and a rejection rewinds to the last accepted token. Nothing earlier is touched or recomputed.

### A faster way to verify a batch

Most of the cost is in verification, not drafting. The draft model is small, so proposing tokens is inexpensive. Verification runs the full model over the entire batch of proposals at once, and that batch is an awkward size, usually 2 to 8 tokens. Matrix multiplication kernels are typically built for either a single token (decode) or a large batch (prefill), and a handful of draft tokens falls between the two.

We contributed a kernel for this case to MLX, where other models can use it as well, not only Gemma 4 in Ollama. It reads and unpacks each block of weights once and reuses it across the entire batch, rather than re-reading the weights for every token. On an M5 Max with nvfp4, this makes Gemma 4’s largest matrix multiplications **2× to 2.5× faster**. The computation is identical; the speedup comes from removing redundant work.

## Get started

Download Ollama 0.31 or later for macOS:

[Download Ollama](https://ollama.com/download)

Then use `ollama launch` to launch a [coding agent](https://docs.ollama.com/integrations#code-in-the-terminal) powered by Gemma 4:

``` bash
ollama launch claude --model gemma4:12b-mlx
```

> Note: If you downloaded Gemma 4 earlier, re-pull it to get the version with MTP using `ollama pull gemma4:12b-mlx`.

`ollama launch` also works with Codex, Droid, OpenCode, Copilot, and others.

Gemma 4 is the first model to receive this performance improvement, with more to follow.

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
