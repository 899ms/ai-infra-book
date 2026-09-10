<!-- 从 eagle31.html 迁移的资料快照；原始 HTML SHA-256: 20e006a4db7d2eaa340f8ae22ed7427f654da28ff149d3b3c7a0eaeedae7538a。 -->

[Blog](/blog)

# EAGLE 3.1: Advancing Speculative Decoding Through Collaboration Between the EAGLE Team, vLLM, and TorchSpec

May 26, 20264 min read

EAGLE Team, vLLM Team, and TorchSpec Team

[\#speculative-decoding](/blog/tags/speculative-decoding)[\#performance](/blog/tags/performance)

- [EAGLE 3.1 Innovations](#eagle-31-innovations)
- [EAGLE 3.1 Training with TorchSpec](#eagle-31-training-with-torchspec)
- [EAGLE 3.1 Integration with vLLM](#eagle-31-integration-with-vllm)
- [Open-Source Collaboration Across the Ecosystem](#open-source-collaboration-across-the-ecosystem)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWxpc3QgaC00IHctNCI+PHBhdGggZD0iTTMgMTJoLjAxIiAvPjxwYXRoIGQ9Ik0zIDE4aC4wMSIgLz48cGF0aCBkPSJNMyA2aC4wMSIgLz48cGF0aCBkPSJNOCAxMmgxMyIgLz48cGF0aCBkPSJNOCAxOGgxMyIgLz48cGF0aCBkPSJNOCA2aDEzIiAvPjwvc3ZnPg==)Table of Contents![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNoZXZyb24tZG93biBoLTQgdy00Ij48cGF0aCBkPSJtNiA5IDYgNiA2LTYiIC8+PC9zdmc+)

The EAGLE series — including EAGLE 1, EAGLE 2, and EAGLE 3 — has become one of the most widely adopted and practically deployed families of speculative decoding algorithms across both research and production systems.

Today, the [EAGLE team](https://github.com/SafeAILab/EAGLE), [vLLM team](https://github.com/vllm-project/vllm), and [TorchSpec team](https://github.com/lightseekorg/TorchSpec) are excited to jointly introduce **EAGLE 3.1** — a major step forward in speculative decoding robustness, efficiency, and deployability.

## EAGLE 3.1 Innovations

While speculative decoding performs well in controlled settings, performance often degrades under different chat templates, long-context inputs, or out-of-distribution system prompts.

The EAGLE team traced this fragility to a phenomenon we call [attention drift](https://arxiv.org/pdf/2605.09992) — as speculation depth increases, the drafter gradually shifts attention away from sink tokens and toward its own generated tokens.

We identified two underlying issues. First, the fused input representation becomes increasingly imbalanced as higher-layer hidden states dominate the drafter input. Second, hidden-state magnitude grows across speculation steps due to the unnormalized residual path. Together, these effects make the drafter progressively less stable at deeper speculation depths.

![Figure 1: EAGLE 3 vs. EAGLE 3.1 architecture comparison. EAGLE 3.1 adds FC normalization after each target hidden state and feeds post-norm hidden states into the next decoding step.](/blog-assets/figures/2026-05-26-eagle-3-1/pre-norm-vs-post-norm.png)

Figure 1: EAGLE 3 vs. EAGLE 3.1 architecture comparison. EAGLE 3.1 adds FC normalization after each target hidden state and feeds post-norm hidden states into the next decoding step.

To address this issue, EAGLE 3.1 introduces two key architectural improvements:

- FC normalization after each target hidden state and before the FC layer
- Feeding post-norm hidden states into the next decoding step

Intuitively, the post-norm design makes the method behave more like recursively invoking the drafter across decoding steps, rather than simply appending additional layers to the target model.

These changes significantly improve robustness across deployment scenarios. Compared with EAGLE 3, EAGLE 3.1 demonstrates:

- Better training-time to inference-time extrapolation
- Stronger long-context robustness
- Higher resilience to chat template and system prompt variation
- More stable acceptance length across diverse serving environments

In long-context workloads, **EAGLE 3.1 achieves up to 2× longer acceptance length compared with EAGLE 3**.

## EAGLE 3.1 Training with TorchSpec

[TorchSpec](https://github.com/lightseekorg/torchspec) now provides efficient training [support for EAGLE 3.1](https://github.com/lightseekorg/TorchSpec/pull/97) and future speculative decoding algorithms.

By lowering training overhead and simplifying experimentation workflows, TorchSpec helps accelerate iteration and exploration for next-generation speculative decoding research and deployment.

Based on TorchSpec and vLLM, we also trained and open-sourced an EAGLE 3.1 draft model for Kimi K2.6:

[https://huggingface.co/lightseekorg/kimi-k2.6-eagle3.1-mla](https://huggingface.co/lightseekorg/kimi-k2.6-eagle3.1-mla)

The model serves as an example of deploying EAGLE 3.1 with TorchSpec training and vLLM serving support on a real-world serving model.

## EAGLE 3.1 Integration with vLLM

EAGLE 3.1 lands in [vLLM](https://github.com/vllm-project/vllm) as a [config-driven extension](https://github.com/vllm-project/vllm/pull/42764) of the existing EAGLE 3 implementation.

The integration includes:

- FC normalization support
- Post-norm hidden-state feedback
- Removal of hardcoded assumptions around target hidden states

At the same time, backward compatibility with existing EAGLE 3 checkpoints is fully preserved. As a result, EAGLE 3.1 draft models can be plugged directly through the same speculative-decoding code path, for example:

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNvcHkgaC0zLjUgdy0zLjUgdGV4dC1tdXRlZC1mb3JlZ3JvdW5kIj48cmVjdCB3aWR0aD0iMTQiIGhlaWdodD0iMTQiIHg9IjgiIHk9IjgiIHJ4PSIyIiByeT0iMiIgLz48cGF0aCBkPSJNNCAxNmMtMS4xIDAtMi0uOS0yLTJWNGMwLTEuMS45LTIgMi0yaDEwYzEuMSAwIDIgLjkgMiAyIiAvPjwvc3ZnPg==)

``` overflow-x-auto
vllm serve nvidia/Kimi-K2.6-NVFP4 \
  --trust-remote-code \
  --tensor-parallel-size 4 \
  --tool-call-parser kimi_k2 \
  --enable-auto-tool-choice \
  --reasoning-parser kimi_k2 \
  --attention-backend tokenspeed_mla \
  --speculative-config '{"model":"lightseekorg/kimi-k2.6-eagle3.1-mla","method":"eagle3","num_speculative_tokens":3}' \
  --language-model-only
```

This makes draft-model upgrades in production vLLM serving smooth and easy.

The support has already been merged into the current main branch of vLLM and will be available via vLLM's nightly release as well as the upcoming **v0.22.0** release.

As an early data point, we benchmarked the Kimi K2.6 EAGLE 3.1 draft model on Kimi-K2.6-NVFP4 with vLLM (TP=4, GB200, non-disagg) on the SPEED-Bench coding dataset. EAGLE 3.1 delivers **2.03× higher per-user output throughput at concurrency 1**, and the speedup stays meaningful as concurrency scales (1.71× at C=4, 1.66× at C=16).

![Figure 2: Per-user output throughput (TPS) on Kimi-K2.6-NVFP4 with vLLM, TP=4, GB200 on SPEED-Bench coding. EAGLE 3.1-MLA vs. no-spec baseline.](/blog-assets/figures/2026-05-26-eagle-3-1/tpot_baseline_vs_eagle31.png)

Figure 2: Per-user output throughput (TPS) on Kimi-K2.6-NVFP4 with vLLM, TP=4, GB200 on SPEED-Bench coding. EAGLE 3.1-MLA vs. no-spec baseline.

## Open-Source Collaboration Across the Ecosystem

This collaboration between the EAGLE team, vLLM team, TorchSpec team represents a strong example of open-source collaboration across algorithm research, system optimization, and training infrastructure.

The EAGLE team continues advancing speculative decoding algorithms, vLLM helps bring these innovations into production inference systems at scale, and TorchSpec enables efficient training and rapid experimentation for future speculative decoding algorithms.

We are also grateful to NVIDIA for their GPU support and continued partnership. This support has played an important role in enabling the development, validation, and benchmarking efforts required to bring EAGLE 3.1 from algorithmic innovation to practical deployment.

Together, we hope to continue raising the overall baseline for speculative decoding and driving further improvements in token efficiency across the broader LLM ecosystem.

Share:

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWxpbmsyIGgtNCB3LTQiPjxwYXRoIGQ9Ik05IDE3SDdBNSA1IDAgMCAxIDcgN2gyIiAvPjxwYXRoIGQ9Ik0xNSA3aDJhNSA1IDAgMSAxIDAgMTBoLTIiIC8+PGxpbmUgeDE9IjgiIHgyPSIxNiIgeTE9IjEyIiB5Mj0iMTIiPjwvbGluZT48L3N2Zz4=)

[![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC00IHctNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiPjxwYXRoIGQ9Ik0xOC4yNDQgMi4yNWgzLjMwOGwtNy4yMjcgOC4yNiA4LjUwMiAxMS4yNEgxNi4xN2wtNS4yMTQtNi44MTdMNC45OSAyMS43NUgxLjY4bDcuNzMtOC44MzVMMS4yNTQgMi4yNUg4LjA4bDQuNzEzIDYuMjMxem0tMS4xNjEgMTcuNTJoMS44MzNMNy4wODQgNC4xMjZINS4xMTd6IiAvPjwvc3ZnPg==)](https://x.com/intent/tweet?url=https%3A%2F%2Fvllm.ai%2Fblog%2F2026-05-26-eagle-3-1&text=EAGLE%203.1%3A%20Advancing%20Speculative%20Decoding%20Through%20Collaboration%20Between%20the%20EAGLE%20Team%2C%20vLLM%2C%20and%20TorchSpec "Share on X")[![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC00IHctNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiPjxwYXRoIGQ9Ik0yMC40NDcgMjAuNDUyaC0zLjU1NHYtNS41NjljMC0xLjMyOC0uMDI3LTMuMDM3LTEuODUyLTMuMDM3LTEuODUzIDAtMi4xMzYgMS40NDUtMi4xMzYgMi45Mzl2NS42NjdIOS4zNTFWOWgzLjQxNHYxLjU2MWguMDQ2Yy40NzctLjkgMS42MzctMS44NSAzLjM3LTEuODUgMy42MDEgMCA0LjI2NyAyLjM3IDQuMjY3IDUuNDU1djYuMjg2ek01LjMzNyA3LjQzM2EyLjA2MiAyLjA2MiAwIDAxLTIuMDYzLTIuMDY1IDIuMDY0IDIuMDY0IDAgMTEyLjA2MyAyLjA2NXptMS43ODIgMTMuMDE5SDMuNTU1VjloMy41NjR2MTEuNDUyek0yMi4yMjUgMEgxLjc3MUMuNzkyIDAgMCAuNzc0IDAgMS43Mjl2MjAuNTQyQzAgMjMuMjI3Ljc5MiAyNCAxLjc3MSAyNGgyMC40NTFDMjMuMiAyNCAyNCAyMy4yMjcgMjQgMjIuMjcxVjEuNzI5QzI0IC43NzQgMjMuMiAwIDIyLjIyMiAwaC4wMDN6IiAvPjwvc3ZnPg==)](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fvllm.ai%2Fblog%2F2026-05-26-eagle-3-1 "Share on LinkedIn")

[![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWZpbGUtdGV4dCBoLTMuNSB3LTMuNSI+PHBhdGggZD0iTTE1IDJINmEyIDIgMCAwIDAtMiAydjE2YTIgMiAwIDAgMCAyIDJoMTJhMiAyIDAgMCAwIDItMlY3WiIgLz48cGF0aCBkPSJNMTQgMnY0YTIgMiAwIDAgMCAyIDJoNCIgLz48cGF0aCBkPSJNMTAgOUg4IiAvPjxwYXRoIGQ9Ik0xNiAxM0g4IiAvPjxwYXRoIGQ9Ik0xNiAxN0g4IiAvPjwvc3ZnPg==)View Markdown Source](https://github.com/vllm-project/vllm-project.github.io/blob/main/_posts/2026-05-26-eagle-3-1.md)

[OldervLLM x Novita AI: PegaFlow for Production-Grade External KV Cache](/blog/2026-05-18-pegaflow)[NewerFrom Text to Multimodal Routing: Hardening Vision Signals in vLLM Semantic Router](/blog/2026-05-28-vllm-sr-vision-encoder-hardening)

## Related Posts

[](/blog/2026-08-14-dspark-adaptive-verification)

### Adaptive Verification in vLLM: DSpark confidence-scheduled verification

Aug 14, 2026·8 min read

Sizing the DSpark draft-verification budget from per-request confidence instead of verifying every drafted token, so one configuration holds the throughput/latency frontier from batch size 1 to 256.

[](/blog/2026-07-23-glm-5.2-nvfp4-b300-pd)

### From Day 0 to Production SLAs: Serving GLM-5.2 on 24 NVIDIA B300 GPUs with vLLM

Jul 23, 2026·18 min read

How we took GLM-5.2-NVFP4 from 40 ms to 17 ms mean TPOT on 24 B300 GPUs with vLLM: P/D disaggregation, MTP speculative decoding, Model Runner V2, and the SLA-first trade-offs behind the final configuration.

[](/blog/2026-07-15-inkling)

### TML Inkling on vLLM: Day-0 Support with Optimized Performance

Jul 15, 2026·8 min read

vLLM brings day-0 support to TML Inkling, a 1T-parameter multimodal model, with MTP, long-context serving, parallelism, and up to 380 tokens per second per user on NVIDIA GB200 GPUs.

- [EAGLE 3.1 Innovations](#eagle-31-innovations)
- [EAGLE 3.1 Training with TorchSpec](#eagle-31-training-with-torchspec)
- [EAGLE 3.1 Integration with vLLM](#eagle-31-integration-with-vllm)
- [Open-Source Collaboration Across the Ecosystem](#open-source-collaboration-across-the-ecosystem)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWxpc3QgaC00IHctNCI+PHBhdGggZD0iTTMgMTJoLjAxIiAvPjxwYXRoIGQ9Ik0zIDE4aC4wMSIgLz48cGF0aCBkPSJNMyA2aC4wMSIgLz48cGF0aCBkPSJNOCAxMmgxMyIgLz48cGF0aCBkPSJNOCAxOGgxMyIgLz48cGF0aCBkPSJNOCA2aDEzIiAvPjwvc3ZnPg==)Table of Contents![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGNsYXNzPSJsdWNpZGUgbHVjaWRlLWNoZXZyb24tZG93biBoLTQgdy00Ij48cGF0aCBkPSJtNiA5IDYgNiA2LTYiIC8+PC9zdmc+)
