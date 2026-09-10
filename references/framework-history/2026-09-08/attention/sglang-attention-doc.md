<!-- 从 sglang-attention-doc.html 迁移的资料快照；原始 HTML SHA-256: 20dac50d647c9b2f8bf34d9d8475d89aa3a221dab83fbfecbd6300b7013424fb。 -->

## ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNMi43NSAxNC4yNUgxNS4yNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuNzUgMy43NUgxNS4yNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuNzUgOUg4LjI1IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)On this page

- [Support Matrix](#support-matrix)
  - [MHA Backends](#mha-backends)
  - [MLA Backends](#mla-backends)
  - [GDN Attention Backends](#gdn-attention-backends)
  - [DSA Attention Backend](#dsa-attention-backend)
  - [Hybrid attention (different backends for prefill vs decode) (Experimental)](#hybrid-attention-different-backends-for-prefill-vs-decode-experimental)
  - [Speculative decoding with hybrid attention](#speculative-decoding-with-hybrid-attention)
- [Attention Backend Selection Guide (CUDA)](#attention-backend-selection-guide-cuda)
  - [Automatic Selection Logic](#automatic-selection-logic)
- [User Guide](#user-guide)
  - [Launch Command for Different Attention Backends](#launch-command-for-different-attention-backends)
- [Steps to add a new attention backend](#steps-to-add-a-new-attention-backend)

Advanced Features

# Attention Backend

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)Copy pageCopy page

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBmb2N1c2FibGU9ImZhbHNlIiBjbGFzcz0ic2l6ZS0zIHRyYW5zaXRpb24tdHJhbnNmb3JtIHRleHQtZ3JheS00MDAgZ3JvdXAtaG92ZXI6dGV4dC1ncmF5LTYwMCBkYXJrOnRleHQtZ3JheS02MDAgZGFyazpncm91cC1ob3Zlcjp0ZXh0LWdyYXktNDAwIHNocmluay0wIHJvdGF0ZS05MCI+PHBhdGggZD0iTTYuNSAyLjc1TDEyLjc1IDlMNi41IDE1LjI1IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)Copy pageCopy page

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBmb2N1c2FibGU9ImZhbHNlIiBjbGFzcz0ic2l6ZS0zIHRyYW5zaXRpb24tdHJhbnNmb3JtIHRleHQtZ3JheS00MDAgZ3JvdXAtaG92ZXI6dGV4dC1ncmF5LTYwMCBkYXJrOnRleHQtZ3JheS02MDAgZGFyazpncm91cC1ob3Zlcjp0ZXh0LWdyYXktNDAwIHNocmluay0wIHJvdGF0ZS05MCI+PHBhdGggZD0iTTYuNSAyLjc1TDEyLjc1IDlMNi41IDE1LjI1IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

SGLang supports a large variety of attention backends. Each of them has different pros and cons. You can test them according to your needs.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJmbGV4LW5vbmUgc2l6ZS01IHRleHQteWVsbG93LTgwMCBkYXJrOnRleHQteWVsbG93LTMwMCI+PHBhdGggZD0iTSA5IDYuNzUgdiAxLjUgbSAwIDMgaCAwLjAwNzUgbSAtNS4yMDM1IDMgaCAxMC4zOTIgYyAxLjE1NSAwIDEuODc2NSAtMS4yNTAzIDEuMjk5IC0yLjI1IEwgMTAuMjk5IDMgYyAtMC41Nzc1IC0wLjk5OTcgLTIuMDIwNSAtMC45OTk3IC0yLjU5OCAwIEwgMi41MDUgMTIgYyAtMC41Nzc1IDAuOTk5NyAwLjE0NCAyLjI1IDEuMjk5IDIuMjUgeiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIC8+PC9zdmc+)

Selecting an optimal attention backend is crucial for maximizing your performance. Different backends excel in various scenarios, so choose based on your model, hardware, and use case. Not all backends are supported on all platforms and model architectures.If you don’t specify `--attention-backend`, SGLang makes a best effort to automatically select the most performant backend based on your hardware and model architecture.

## 

[​](#support-matrix)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Support Matrix

The support matrix is split into two parts: MHA (standard attention) and MLA (multi-head latent attention). For an explanation of the key differences between MHA and MLA, please see the [SGLang documentation on DeepSeek MLA](/cookbook/autoregressive/DeepSeek/DeepSeek-V3#4-2-4-mla-optimizations) and the original [DeepSeek MLA paper](https://arxiv.org/pdf/2405.04434).

### 

[​](#mha-backends)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

MHA Backends

| **Backend** | **Page Size \> 1 (native)** | **FP8 KV Cache** | **FP4 KV Cache** | **Spec topk=1** | **Spec topk\>1** | **Sliding Window** | **MultiModal** |
|----|----|----|----|----|----|----|----|
| **FlashInfer** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **FA3 (FlashAttention 3)** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **FA4 (FlashAttention 4)** | 128 | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Triton** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Torch Native (SDPA)** | ❌ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| **FlexAttention (PyTorch)** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **TRTLLM MHA** | 16, 32 or 64 | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| **Dual Chunk FlashAttention** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **HPC-Ops** | 64 | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **AITER (ROCm)** | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Wave (ROCm)** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Ascend (NPU)** | ✅ | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ |
| **Intel XPU** | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Intel AMX (CPU)** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

### 

[​](#mla-backends)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

MLA Backends

| **Backend** | **Native Page Sizes** | **FP8 KV Cache** | **FP4 KV Cache** | **Chunked Prefix Cache** | **Spec topk=1** | **Spec topk\>1** |
|----|----|----|----|----|----|----|
| **FlashInfer MLA** | 1 | ❌ | ✅ | ✅ | ✅ | ❌ |
| **FlashMLA** | 64 | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Cutlass MLA** | 128 | ✅ | ✅ | ✅ | ✅ | ❌ |
| **TRTLLM MLA (Blackwell)** | 32 or 64 | ✅ | ✅ | ✅ | ✅ | ❌ |
| **CuteDSL MLA (Blackwell)** | 32 or 64 | ✅ | ❌ | ✅ | ✅ | ❌ |
| **TokenSpeed MLA (Blackwell)** | 32 or 64 | ✅ (required) | ❌ | ✅ | ✅ | ❌ |
| **FA3 (FlashAttention 3)** | n/a | ❌ | ❌ | ✅ | ✅ | ⚠️ (page_size=1 only) |
| **Triton** | n/a | ❌ | ❌ | ❌ | ✅ | ⚠️ (page_size=1 only) |
| **FA4** | 1 | ❌ | ✅ | ✅ | ❌ | ❌ |
| **Ascend MLA (NPU)** | 128 | ❌ | ❌ | ❌ | ❌ | ❌ |

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgdGV4dC1ibHVlLTgwMCBkYXJrOnRleHQtYmx1ZS0zMDAiPjxwYXRoIGQ9Ik0gOSAxLjY3MTQgQyAxMy4wMzcxIDEuNjcxNCAxNi4zMjg2IDQuOTYyOSAxNi4zMjg2IDkgQyAxNi4zMjg2IDEzLjAzNzEgMTMuMDM3MSAxNi4zMjg2IDkgMTYuMzI4NiBDIDcuMDU3NCAxNi4zMjUyIDUuMTk1MyAxNS41NTIgMy44MjE3IDE0LjE3ODMgQyAyLjQ0OCAxMi44MDQ3IDEuNjc0OCAxMC45NDI2IDEuNjcxNCA5IEMgMS42NzE0IDQuOTYyOSA0Ljk2MjkgMS42NzE0IDkgMS42NzE0IFogTSA5IDAgQyA0LjAzNzEgMCAwIDQuMDM3MSAwIDkgQyAwIDEzLjk2MjkgNC4wMzcxIDE4IDkgMTggQyAxMy45NjI5IDE4IDE4IDEzLjk2MjkgMTggOSBDIDE4IDQuMDM3MSAxMy45NjI5IDAgOSAwIFogTSAxMC4yODU3IDMuODU3MSBIIDcuNzE0MyBWIDEwLjI4NTcgSCAxMC4yODU3IFYgMy44NTcxIFogTSAxMC4yODU3IDExLjU3MTQgSCA3LjcxNDMgViAxNC4xNDI5IEggMTAuMjg1NyBWIDExLjU3MTQgWiIgZmlsbD0iY3VycmVudENvbG9yIiBzdHJva2U9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiAvPjwvc3ZnPg==)

Multimodal attention is selected by `--mm-attention-backend`. The “MultiModal” column indicates whether a corresponding multimodal implementation exists for that backend family.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgdGV4dC1ibHVlLTgwMCBkYXJrOnRleHQtYmx1ZS0zMDAiPjxwYXRoIGQ9Ik0gOSAxLjY3MTQgQyAxMy4wMzcxIDEuNjcxNCAxNi4zMjg2IDQuOTYyOSAxNi4zMjg2IDkgQyAxNi4zMjg2IDEzLjAzNzEgMTMuMDM3MSAxNi4zMjg2IDkgMTYuMzI4NiBDIDcuMDU3NCAxNi4zMjUyIDUuMTk1MyAxNS41NTIgMy44MjE3IDE0LjE3ODMgQyAyLjQ0OCAxMi44MDQ3IDEuNjc0OCAxMC45NDI2IDEuNjcxNCA5IEMgMS42NzE0IDQuOTYyOSA0Ljk2MjkgMS42NzE0IDkgMS42NzE0IFogTSA5IDAgQyA0LjAzNzEgMCAwIDQuMDM3MSAwIDkgQyAwIDEzLjk2MjkgNC4wMzcxIDE4IDkgMTggQyAxMy45NjI5IDE4IDE4IDEzLjk2MjkgMTggOSBDIDE4IDQuMDM3MSAxMy45NjI5IDAgOSAwIFogTSAxMC4yODU3IDMuODU3MSBIIDcuNzE0MyBWIDEwLjI4NTcgSCAxMC4yODU3IFYgMy44NTcxIFogTSAxMC4yODU3IDExLjU3MTQgSCA3LjcxNDMgViAxNC4xNDI5IEggMTAuMjg1NyBWIDExLjU3MTQgWiIgZmlsbD0iY3VycmVudENvbG9yIiBzdHJva2U9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiAvPjwvc3ZnPg==)

- DSA is specifically designed for [DeepSeek V3.2](https://lmsys.org/blog/2025-09-29-deepseek-V32/). See the [DSA Attention Backend](#dsa-attention-backend) section and [DeepSeek V3.2 deployment guide](/cookbook/autoregressive/DeepSeek/DeepSeek-V3_2) for details.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgdGV4dC1ibHVlLTgwMCBkYXJrOnRleHQtYmx1ZS0zMDAiPjxwYXRoIGQ9Ik0gOSAxLjY3MTQgQyAxMy4wMzcxIDEuNjcxNCAxNi4zMjg2IDQuOTYyOSAxNi4zMjg2IDkgQyAxNi4zMjg2IDEzLjAzNzEgMTMuMDM3MSAxNi4zMjg2IDkgMTYuMzI4NiBDIDcuMDU3NCAxNi4zMjUyIDUuMTk1MyAxNS41NTIgMy44MjE3IDE0LjE3ODMgQyAyLjQ0OCAxMi44MDQ3IDEuNjc0OCAxMC45NDI2IDEuNjcxNCA5IEMgMS42NzE0IDQuOTYyOSA0Ljk2MjkgMS42NzE0IDkgMS42NzE0IFogTSA5IDAgQyA0LjAzNzEgMCAwIDQuMDM3MSAwIDkgQyAwIDEzLjk2MjkgNC4wMzcxIDE4IDkgMTggQyAxMy45NjI5IDE4IDE4IDEzLjk2MjkgMTggOSBDIDE4IDQuMDM3MSAxMy45NjI5IDAgOSAwIFogTSAxMC4yODU3IDMuODU3MSBIIDcuNzE0MyBWIDEwLjI4NTcgSCAxMC4yODU3IFYgMy44NTcxIFogTSAxMC4yODU3IDExLjU3MTQgSCA3LjcxNDMgViAxNC4xNDI5IEggMTAuMjg1NyBWIDExLjU3MTQgWiIgZmlsbD0iY3VycmVudENvbG9yIiBzdHJva2U9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiAvPjwvc3ZnPg==)

For the KV4 FA4 scenario, FA4 requires using a different —decode-attention-backend to run. Except for trtllm_mha being incompatible with FA4, all other decode backends behave as shown in the table.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQuNSB0ZXh0LWdyZWVuLTgwMCBkYXJrOnRleHQtZ3JlZW4tMzAwIj48cGF0aCBkPSJNIDQuMDIxNiAxNS45NzI3IEMgNC4wMjE2IDE2LjE5NDEgNC4wODU1IDE2LjQxMDEgNC4yMDc0IDE2LjU5NDcgTCA0LjgxIDE3LjQ5NzkgQyA0Ljk5NDYgMTcuNzc0NyA1LjQxMzcgMTggNS43NDY3IDE4IEggNy45MTQ5IEMgOC4yNDY4IDE4IDguNjY1OSAxNy43NzUgOC44NTA1IDE3LjQ5NzkgTCA5LjQ1MSAxNi41OTUxIEMgOS41NTQzIDE2LjQzOSA5LjYzOTEgMTYuMTYwMSA5LjYzOTEgMTUuOTcyNyBMIDkuNjQzNiAxNC41OTQ1IEggNC4wMTgxIEwgNC4wMjE2IDE1Ljk3MjcgWiBNIDYuODMwOCAwIEMgMy4yNDUzIDAuMDExMyAwLjY0MjkgMi45MTcxIDAuNjQyOSA2LjE1NjMgQyAwLjY0MjkgNy43MTY3IDEuMjIwOSA5LjEzOTIgMi4xNzQ0IDEwLjIyNzggQyAyLjc1NTYgMTAuODkwMSAzLjY2MyAxMi4yNzUxIDQuMDEwNCAxMy40NDMgQyA0LjAxMTUgMTMuNDUxOCA0LjAxMzcgMTMuNDYxMiA0LjAxNDggMTMuNDcwNiBIIDkuNjQ3MyBDIDkuNjQ4MyAxMy40NjEyIDkuNjUwNSAxMy40NTI0IDkuNjUxNyAxMy40NDMgQyA5Ljk5ODggMTIuMjc1MSAxMC45MDY1IDEwLjg5MDEgMTEuNDg3NyAxMC4yMjc4IEMgMTIuNDQyMiA5LjE2OTUgMTMuMDE4OSA3Ljc0OSAxMy4wMTg5IDYuMTU2MyBDIDEzLjAxODkgMi43NzA1IDEwLjI0ODMgMC4wMDAxIDYuODMwOCAwIFogTSAxMC4yMjAyIDkuMTQ0OSBDIDkuNjY5NiA5Ljc3MjQgOC45ODgyIDEwLjc3MjcgOC40OTU2IDExLjgxMzEgSCA1LjE2OTIgQyA0LjY3NjYgMTAuNzcyNyAzLjk5NTMgOS43NzI0IDMuNDQ1IDkuMTQ1MiBDIDIuNzI1NyA4LjMyNTcgMi4zMzA1IDcuMjQ2MyAyLjMzMDUgNi4xNTYzIEMgMi4zMzA1IDMuOTgzNSA0LjAyMTYgMS42OTY0IDYuNzk5MiAxLjY4NzYgQyA5LjMxMzEgMS42ODc2IDExLjMzMTIgMy43MDU4IDExLjMzMTIgNi4xNTYzIEMgMTEuMzMxMiA3LjI0NjMgMTAuOTM3NCA4LjMyNTcgMTAuMjIwMiA5LjE0NDkgWiBNIDYuMjY4MyAyLjgxMjcgQyA0LjcxNzggMi44MTI3IDMuNDU1NiA0LjA3NDkgMy40NTU2IDUuNjI1NCBDIDMuNDU1NiA1LjkzNjQgMy43MDcyIDYuMTg4IDQuMDE4MSA2LjE4OCBDIDQuMzI5MSA2LjE4OCA0LjU4MDcgNS45MzQ4IDQuNTgwNyA1LjYyNTQgQyA0LjU4MDcgNC42OTQ4IDUuMzM3NiAzLjkzNzggNi4yNjgzIDMuOTM3OCBDIDYuNTc5MiAzLjkzNzggNi44MzA4IDMuNjg2NSA2LjgzMDggMy4zNzU2IEMgNi44MzA4IDMuMDY0NyA2LjU3NzcgMi44MTI3IDYuMjY4MyAyLjgxMjcgWiIgZmlsbD0iY3VycmVudENvbG9yIiBzdHJva2U9Im5vbmUiIC8+PC9zdmc+)

Speculative decoding topk: `topk` is the number of draft tokens sampled per step from the draft model. `topk = 1` follows classic EAGLE; `topk > 1` explores multiple branches and requires backend support in both draft and verification paths.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQuNSB0ZXh0LWdyZWVuLTgwMCBkYXJrOnRleHQtZ3JlZW4tMzAwIj48cGF0aCBkPSJNIDQuMDIxNiAxNS45NzI3IEMgNC4wMjE2IDE2LjE5NDEgNC4wODU1IDE2LjQxMDEgNC4yMDc0IDE2LjU5NDcgTCA0LjgxIDE3LjQ5NzkgQyA0Ljk5NDYgMTcuNzc0NyA1LjQxMzcgMTggNS43NDY3IDE4IEggNy45MTQ5IEMgOC4yNDY4IDE4IDguNjY1OSAxNy43NzUgOC44NTA1IDE3LjQ5NzkgTCA5LjQ1MSAxNi41OTUxIEMgOS41NTQzIDE2LjQzOSA5LjYzOTEgMTYuMTYwMSA5LjYzOTEgMTUuOTcyNyBMIDkuNjQzNiAxNC41OTQ1IEggNC4wMTgxIEwgNC4wMjE2IDE1Ljk3MjcgWiBNIDYuODMwOCAwIEMgMy4yNDUzIDAuMDExMyAwLjY0MjkgMi45MTcxIDAuNjQyOSA2LjE1NjMgQyAwLjY0MjkgNy43MTY3IDEuMjIwOSA5LjEzOTIgMi4xNzQ0IDEwLjIyNzggQyAyLjc1NTYgMTAuODkwMSAzLjY2MyAxMi4yNzUxIDQuMDEwNCAxMy40NDMgQyA0LjAxMTUgMTMuNDUxOCA0LjAxMzcgMTMuNDYxMiA0LjAxNDggMTMuNDcwNiBIIDkuNjQ3MyBDIDkuNjQ4MyAxMy40NjEyIDkuNjUwNSAxMy40NTI0IDkuNjUxNyAxMy40NDMgQyA5Ljk5ODggMTIuMjc1MSAxMC45MDY1IDEwLjg5MDEgMTEuNDg3NyAxMC4yMjc4IEMgMTIuNDQyMiA5LjE2OTUgMTMuMDE4OSA3Ljc0OSAxMy4wMTg5IDYuMTU2MyBDIDEzLjAxODkgMi43NzA1IDEwLjI0ODMgMC4wMDAxIDYuODMwOCAwIFogTSAxMC4yMjAyIDkuMTQ0OSBDIDkuNjY5NiA5Ljc3MjQgOC45ODgyIDEwLjc3MjcgOC40OTU2IDExLjgxMzEgSCA1LjE2OTIgQyA0LjY3NjYgMTAuNzcyNyAzLjk5NTMgOS43NzI0IDMuNDQ1IDkuMTQ1MiBDIDIuNzI1NyA4LjMyNTcgMi4zMzA1IDcuMjQ2MyAyLjMzMDUgNi4xNTYzIEMgMi4zMzA1IDMuOTgzNSA0LjAyMTYgMS42OTY0IDYuNzk5MiAxLjY4NzYgQyA5LjMxMzEgMS42ODc2IDExLjMzMTIgMy43MDU4IDExLjMzMTIgNi4xNTYzIEMgMTEuMzMxMiA3LjI0NjMgMTAuOTM3NCA4LjMyNTcgMTAuMjIwMiA5LjE0NDkgWiBNIDYuMjY4MyAyLjgxMjcgQyA0LjcxNzggMi44MTI3IDMuNDU1NiA0LjA3NDkgMy40NTU2IDUuNjI1NCBDIDMuNDU1NiA1LjkzNjQgMy43MDcyIDYuMTg4IDQuMDE4MSA2LjE4OCBDIDQuMzI5MSA2LjE4OCA0LjU4MDcgNS45MzQ4IDQuNTgwNyA1LjYyNTQgQyA0LjU4MDcgNC42OTQ4IDUuMzM3NiAzLjkzNzggNi4yNjgzIDMuOTM3OCBDIDYuNTc5MiAzLjkzNzggNi44MzA4IDMuNjg2NSA2LjgzMDggMy4zNzU2IEMgNi44MzA4IDMuMDY0NyA2LjU3NzcgMi44MTI3IDYuMjY4MyAyLjgxMjcgWiIgZmlsbD0iY3VycmVudENvbG9yIiBzdHJva2U9Im5vbmUiIC8+PC9zdmc+)

Page size controls how many tokens are grouped into a KV cache block. For the prefix cache to take effect, the number of tokens must fill at least one complete page. For example, if your prompt is only 32 tokens and `page_size = 64`, it won’t fill a complete page and cannot be matched in the prefix cache (pages cannot be padded). With 65 tokens and `page_size = 64`, only the first page of 64 tokens will be cached and matched; the remaining 1 token is discarded. Use `page_size = 1` for maximum prefix reuse (token-level matching). Note that higher page sizes generally improve attention kernel performance, so prefer `page_size > 1` when prefix cache reuse is not critical.

Many backends that do not natively operate on pages can emulate `page_size > 1` at the wrapper layer by expanding page tables to per-token indices. The “Page Size \> 1 (native)” column indicates true in-kernel paging. Some backends require fixed native page sizes and cannot be reduced/emulated differently: TRTLLM MHA (16/32/64), TRTLLM MLA (32/64), CuteDSL MLA (32/64), FlashMLA (64), Cutlass MLA (128), Ascend (128), HPC-Ops (64). MLA page-size constraints:

- FlashInfer MLA: page_size = 1.
- FlashMLA: page_size = 64.
- Cutlass MLA: page_size = 128.
- TRTLLM MLA: page_size ∈ {32, 64}.
- CuteDSL MLA: page_size ∈ {32, 64} (decode-only; prefill falls back to `trtllm_mla` when unset).
- TokenSpeed MLA: page_size ∈ {32, 64} (Blackwell SM100/SM12x only; requires `--kv-cache-dtype fp8_e4m3`).

### 

[​](#gdn-attention-backends)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

GDN Attention Backends

GDN (Gated Delta Network) is a linear attention mechanism with O(n) complexity, used in hybrid models that alternate GDN linear attention layers with standard full attention layers. GDN is **not** selected via `--attention-backend`; it is automatically activated when the model architecture requires it (e.g., Qwen 3.5, Qwen 3 Next, Jet Nemotron, Jet VLM). The GDN linear attention layers have their own kernel backends, selected via `--linear-attn-backend` (default: `triton`). You can override the kernel per phase with `--linear-attn-decode-backend` and `--linear-attn-prefill-backend`. On SM100/SM103 with CUDA 13+, SGLang automatically selects FlashInfer for GDN prefill when the per-phase override is unset, the base linear-attention backend is Triton, recurrent state is BF16, key/value head dimensions are 128, dynamic chunking and page-major KV layout are disabled, and `--chunked-prefill-size` is between 1 and 8192. Radix caching may be disabled or use `no_buffer`, `extra_buffer`, or `extra_buffer_lazy`; the extra-buffer paths use state checkpoints.

| Backend | Decode | Prefill / Extend | Spec Decoding (Target Verify) |
|----|----|----|----|
| **Triton (CUDA)** | ✅ | ✅ | ✅ |
| **Triton (AMD/ROCm)** | ✅ | ✅ | ✅ |
| **Triton (NPU)** | ✅ | ✅ | ❌ |
| **Triton (CPU)** | ✅ | ✅ | ❌ |
| **CuTe DSL (CUDA only)** | ✅ | ❌ | ❌ |
| **FlashInfer (CUDA, SM90/SM100/SM103)** | ✅ | ✅ | ✅ linear chain; tree falls back to Triton |

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJmbGV4LW5vbmUgc2l6ZS01IHRleHQteWVsbG93LTgwMCBkYXJrOnRleHQteWVsbG93LTMwMCI+PHBhdGggZD0iTSA5IDYuNzUgdiAxLjUgbSAwIDMgaCAwLjAwNzUgbSAtNS4yMDM1IDMgaCAxMC4zOTIgYyAxLjE1NSAwIDEuODc2NSAtMS4yNTAzIDEuMjk5IC0yLjI1IEwgMTAuMjk5IDMgYyAtMC41Nzc1IC0wLjk5OTcgLTIuMDIwNSAtMC45OTk3IC0yLjU5OCAwIEwgMi41MDUgMTIgYyAtMC41Nzc1IDAuOTk5NyAwLjE0NCAyLjI1IDEuMjk5IDIuMjUgeiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIC8+PC9zdmc+)

GDN models are hybrid: the full-attention layers still require a standard `--attention-backend`. Platform constraints for the full-attention backend on hybrid GDN models:

- **Blackwell SM120 (e.g., RTX PRO 6000 Blackwell)**: `triton` or `flashinfer` for prefill/full attention; `trtllm_mha` is supported for `--decode-attention-backend` only.
- **Other Blackwell variants (including SM100 B200/GB200)**: `triton`, `trtllm_mha`, or `fa4` only.
- **NPU (Ascend)**: `ascend` only.
- **AMD (ROCm)**: `triton` recommended.
- **Other CUDA (Hopper, Ampere, etc.)**: auto-selection works; no special constraints.

### 

[​](#dsa-attention-backend)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

DSA Attention Backend

DSA (DeepSeek Sparse Attention) is a native sparse attention mechanism used by [DeepSeek V3.2](https://lmsys.org/blog/2025-09-29-deepseek-V32/). It is activated automatically when the model architecture requires it and is selected via `--attention-backend dsa` (deprecated alias: `nsa`). Internally, the DSA backend dispatches to different sub-backends for prefill and decode phases. You can override these with `--dsa-prefill-backend` and `--dsa-decode-backend`:

| Sub-backend | Prefill | Decode | Notes |
|----|----|----|----|
| **flashmla_sparse** | ✅ | ✅ | Default prefill on Hopper and Blackwell (BF16) |
| **flashmla_sparse_q8** | ✅ | ❌ | Native FP8 (q8×kv8) sparse prefill on Hopper (SM90); requires `—kv-cache-dtype fp8_e4m3` |
| **flashmla_kv** | ✅ | ✅ | Default for FP8 on Hopper (prefill + decode) |
| **flashmla_auto** | ✅ | ❌ | Picks flashmla_sparse or flashmla_kv by KV cache dtype |
| **fa3** | ✅ | ✅ | Default decode on Hopper (BF16) |
| **trtllm** | ✅ | ✅ | Default decode on Blackwell (BF16); default for FP8 on Blackwell (prefill + decode) |
| **tilelang** | ✅ | ✅ | Default on AMD (ROCm) |
| **aiter** | ✅ | ✅ | AMD-specific kernel library (requires aiter package) |

For deployment examples, see the [DeepSeek V3.2 deployment guide](/cookbook/autoregressive/DeepSeek/DeepSeek-V3_2).

### 

[​](#hybrid-attention-different-backends-for-prefill-vs-decode-experimental)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Hybrid attention (different backends for prefill vs decode) (Experimental)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJmbGV4LW5vbmUgc2l6ZS01IHRleHQteWVsbG93LTgwMCBkYXJrOnRleHQteWVsbG93LTMwMCI+PHBhdGggZD0iTSA5IDYuNzUgdiAxLjUgbSAwIDMgaCAwLjAwNzUgbSAtNS4yMDM1IDMgaCAxMC4zOTIgYyAxLjE1NSAwIDEuODc2NSAtMS4yNTAzIDEuMjk5IC0yLjI1IEwgMTAuMjk5IDMgYyAtMC41Nzc1IC0wLjk5OTcgLTIuMDIwNSAtMC45OTk3IC0yLjU5OCAwIEwgMi41MDUgMTIgYyAtMC41Nzc1IDAuOTk5NyAwLjE0NCAyLjI1IDEuMjk5IDIuMjUgeiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMS41IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIC8+PC9zdmc+)

Hybrid attention is an experimental feature.

You can mix-and-match attention backends for prefill and decode. This is useful when one backend excels at prefill and another excels at decode. For the implementation details, please see `python/sglang/srt/layers/attention/hybrid_attn_backend.py`.

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
# Example: Prefill with FA4, Decode with TRTLLM MLA (Blackwell)
python3 -m sglang.launch_server \
  --model-path nvidia/DeepSeek-R1-FP4 \
  --tp 8 \
  --attention-backend trtllm_mla \
  --moe-runner-backend flashinfer_trtllm \
  --quantization modelopt_fp4 \
  --prefill-attention-backend fa4
```

#### 

[​](#speculative-decoding-with-hybrid-attention)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Speculative decoding with hybrid attention

Hybrid attention also works with speculative decoding. The backend used for draft decoding and target verification depends on `--speculative-attention-mode`:

- `--speculative-attention-mode decode` (recommended): draft/verify use the decode backend.
- `--speculative-attention-mode prefill` (default): draft/verify use the prefill backend.

Constraints when combining hybrid attention with speculative decoding:

- If any attention backend is `trtllm_mha`, speculative decoding supports only `--speculative-eagle-topk 1`.
- For paged MHA backends with `--page-size > 1` and `--speculative-eagle-topk > 1`, only `flashinfer` is supported.
- CUDA Graph: the decode backend is always captured; the prefill backend is captured only when `--speculative-attention-mode prefill`.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQuNSB0ZXh0LWdyZWVuLTgwMCBkYXJrOnRleHQtZ3JlZW4tMzAwIj48cGF0aCBkPSJNIDQuMDIxNiAxNS45NzI3IEMgNC4wMjE2IDE2LjE5NDEgNC4wODU1IDE2LjQxMDEgNC4yMDc0IDE2LjU5NDcgTCA0LjgxIDE3LjQ5NzkgQyA0Ljk5NDYgMTcuNzc0NyA1LjQxMzcgMTggNS43NDY3IDE4IEggNy45MTQ5IEMgOC4yNDY4IDE4IDguNjY1OSAxNy43NzUgOC44NTA1IDE3LjQ5NzkgTCA5LjQ1MSAxNi41OTUxIEMgOS41NTQzIDE2LjQzOSA5LjYzOTEgMTYuMTYwMSA5LjYzOTEgMTUuOTcyNyBMIDkuNjQzNiAxNC41OTQ1IEggNC4wMTgxIEwgNC4wMjE2IDE1Ljk3MjcgWiBNIDYuODMwOCAwIEMgMy4yNDUzIDAuMDExMyAwLjY0MjkgMi45MTcxIDAuNjQyOSA2LjE1NjMgQyAwLjY0MjkgNy43MTY3IDEuMjIwOSA5LjEzOTIgMi4xNzQ0IDEwLjIyNzggQyAyLjc1NTYgMTAuODkwMSAzLjY2MyAxMi4yNzUxIDQuMDEwNCAxMy40NDMgQyA0LjAxMTUgMTMuNDUxOCA0LjAxMzcgMTMuNDYxMiA0LjAxNDggMTMuNDcwNiBIIDkuNjQ3MyBDIDkuNjQ4MyAxMy40NjEyIDkuNjUwNSAxMy40NTI0IDkuNjUxNyAxMy40NDMgQyA5Ljk5ODggMTIuMjc1MSAxMC45MDY1IDEwLjg5MDEgMTEuNDg3NyAxMC4yMjc4IEMgMTIuNDQyMiA5LjE2OTUgMTMuMDE4OSA3Ljc0OSAxMy4wMTg5IDYuMTU2MyBDIDEzLjAxODkgMi43NzA1IDEwLjI0ODMgMC4wMDAxIDYuODMwOCAwIFogTSAxMC4yMjAyIDkuMTQ0OSBDIDkuNjY5NiA5Ljc3MjQgOC45ODgyIDEwLjc3MjcgOC40OTU2IDExLjgxMzEgSCA1LjE2OTIgQyA0LjY3NjYgMTAuNzcyNyAzLjk5NTMgOS43NzI0IDMuNDQ1IDkuMTQ1MiBDIDIuNzI1NyA4LjMyNTcgMi4zMzA1IDcuMjQ2MyAyLjMzMDUgNi4xNTYzIEMgMi4zMzA1IDMuOTgzNSA0LjAyMTYgMS42OTY0IDYuNzk5MiAxLjY4NzYgQyA5LjMxMzEgMS42ODc2IDExLjMzMTIgMy43MDU4IDExLjMzMTIgNi4xNTYzIEMgMTEuMzMxMiA3LjI0NjMgMTAuOTM3NCA4LjMyNTcgMTAuMjIwMiA5LjE0NDkgWiBNIDYuMjY4MyAyLjgxMjcgQyA0LjcxNzggMi44MTI3IDMuNDU1NiA0LjA3NDkgMy40NTU2IDUuNjI1NCBDIDMuNDU1NiA1LjkzNjQgMy43MDcyIDYuMTg4IDQuMDE4MSA2LjE4OCBDIDQuMzI5MSA2LjE4OCA0LjU4MDcgNS45MzQ4IDQuNTgwNyA1LjYyNTQgQyA0LjU4MDcgNC42OTQ4IDUuMzM3NiAzLjkzNzggNi4yNjgzIDMuOTM3OCBDIDYuNTc5MiAzLjkzNzggNi44MzA4IDMuNjg2NSA2LjgzMDggMy4zNzU2IEMgNi44MzA4IDMuMDY0NyA2LjU3NzcgMi44MTI3IDYuMjY4MyAyLjgxMjcgWiIgZmlsbD0iY3VycmVudENvbG9yIiBzdHJva2U9Im5vbmUiIC8+PC9zdmc+)

If you set only one of `--prefill-attention-backend` or `--decode-attention-backend`, the unspecified phase inherits `--attention-backend`. If both are specified and differ, SGLang automatically enables a hybrid wrapper to dispatch to the chosen backend per phase.

## 

[​](#attention-backend-selection-guide-cuda)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Attention Backend Selection Guide (CUDA)

If the `--attention-backend` argument is not specified, SGLang automatically selects the best backend based on the hardware (CUDA) and model architecture.

### 

[​](#automatic-selection-logic)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Automatic Selection Logic

**1. MHA Models (e.g., Llama, Qwen)**

- **Hopper (e.g., H100, H200)**: Defaults to `fa3` if using CUDA 12.3+ and the model configuration is supported.
- **Blackwell (e.g., B200)**: Defaults to `trtllm_mha`, unless using speculative decoding with `topk > 1`.
- **Other Architectures (Ampere, Ada, etc.)**: Defaults to `flashinfer` if available; otherwise falls back to `triton`.

**2. MLA Models (e.g., DeepSeek V3)**

- **Hopper**: Defaults to `fa3` (requires CUDA 12.3+).
- **Blackwell**: Defaults to `flashinfer`; `trtllm_mla` is auto-selected for DeepSeek V3 models specifically.
- **Other Architectures**: Defaults to `triton`.

## 

[​](#user-guide)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

User Guide

### 

[​](#launch-command-for-different-attention-backends)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Launch Command for Different Attention Backends

- FlashInfer (Default for Non-Hopper Machines, e.g., A100, A40)

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --attention-backend flashinfer
python3 -m sglang.launch_server \
  --tp 8 \
  --model deepseek-ai/DeepSeek-V3 \
  --attention-backend flashinfer \
  --trust-remote-code
```

- FlashAttention 3 (Default for Hopper Machines, e.g., H100, H200, H20)

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --attention-backend fa3
python3 -m sglang.launch_server \
  --tp 8 \
  --model deepseek-ai/DeepSeek-V3 \
  --trust-remote-code \
  --attention-backend fa3
```

- Triton

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --attention-backend triton
python3 -m sglang.launch_server \
  --tp 8 \
  --model deepseek-ai/DeepSeek-V3 \
  --attention-backend triton \
  --trust-remote-code
```

- FlashMLA

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --tp 8 \
  --model deepseek-ai/DeepSeek-R1 \
  --attention-backend flashmla \
  --trust-remote-code
python3 -m sglang.launch_server \
  --tp 8 \
  --model deepseek-ai/DeepSeek-R1 \
  --attention-backend flashmla \
  --kv-cache-dtype fp8_e4m3 \
  --trust-remote-code
```

- TRTLLM MLA (Optimized for Blackwell Architecture, e.g., B200)

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --tp 8 \
  --model deepseek-ai/DeepSeek-R1 \
  --attention-backend trtllm_mla \
  --trust-remote-code
```

- TRTLLM MLA with FP8 KV Cache (Higher concurrency, lower memory footprint)

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --tp 8 \
  --model deepseek-ai/DeepSeek-R1 \
  --attention-backend trtllm_mla \
  --kv-cache-dtype fp8_e4m3 \
  --trust-remote-code
```

- TRTLLM MHA (Optimized for Blackwell Architecture, e.g., B200)

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --tp 4 \
  --model Qwen/Qwen3.5-35B-A3B-FP8 \
  --attention-backend trtllm_mha \
  --trust-remote-code
```

- TRTLLM MHA (XQA backend) (Optimized for SM90 and SM120, e.g., H20, H200, 5090) Note that TRTLLM XQA backend only works well for pagesize 64.

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --tp 4 \
  --model Qwen/Qwen3.5-35B-A3B-FP8 \
  --decode-attention-backend trtllm_mha \
  --trust-remote-code
```

- HPC-Ops (MHA kernels from [HPC-Ops](https://github.com/Tencent/hpc-ops) by the Tencent Hunyuan AI Infra team; Hopper (SM90) only, requires installing the `hpc` package from source, page size 64, bf16 or fp8_e4m3 KV cache, head_dim 128, q/kv head group 4 or 8)

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --model Qwen/Qwen3-30B-A3B-Instruct-2507-FP8 \
  --attention-backend hpc_ops \
  --page-size 64 \
  --trust-remote-code

# FP8 models should also set --kv-cache-dtype fp8_e4m3 to run the FP8 attention
# kernels. This enables the fused QKNorm+RoPE+FP8-quant+StoreKV op, which is
# currently wired for Hunyuan V3 and requires per-rank (q_heads, kv_heads) of
# (64, 8) or (8, 1), e.g. --tp 1 or --tp 8 for Hy3.
python3 -m sglang.launch_server \
  --tp 8 \
  --model tencent/Hy3-FP8 \
  --attention-backend hpc_ops \
  --kv-cache-dtype fp8_e4m3 \
  --page-size 64 \
  --trust-remote-code
```

- FlashAttention 4 (MHA & MLA)

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
# FA4 for both prefill and decode on SM90/SM100
python3 -m sglang.launch_server \
  --model-path Qwen/Qwen3-30B-A3B-Instruct-2507-FP8 \
  --attention-backend fa4 \
  --page-size 128 \
  --trust-remote-code

python3 -m sglang.launch_server \
  --tp 8 \
  --model deepseek-ai/DeepSeek-R1 \
  --prefill-attention-backend fa4 \
  --trust-remote-code
```

- Cutlass MLA

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --tp 8 \
  --model deepseek-ai/DeepSeek-R1 \
  --attention-backend cutlass_mla \
  --trust-remote-code
```

- Ascend

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --attention-backend ascend
```

- Intel XPU

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --attention-backend intel_xpu
```

- Wave

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --attention-backend wave
```

- FlexAttention

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --attention-backend flex_attention
```

- Dual Chunk FlashAttention

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --model Qwen/Qwen2.5-14B-Instruct-1M \
  --attention-backend dual_chunk_flash_attn
```

- Torch Native

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang.launch_server \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --attention-backend torch_native
```

## 

[​](#steps-to-add-a-new-attention-backend)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Steps to add a new attention backend

To add a new attention backend, you can learn from the existing backends (`python/sglang/srt/layers/attention/triton_backend.py`, `python/sglang/srt/layers/attention/flashattention_backend.py`) and follow the steps below.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgdGV4dC1ibHVlLTgwMCBkYXJrOnRleHQtYmx1ZS0zMDAiPjxwYXRoIGQ9Ik0gOSAxLjY3MTQgQyAxMy4wMzcxIDEuNjcxNCAxNi4zMjg2IDQuOTYyOSAxNi4zMjg2IDkgQyAxNi4zMjg2IDEzLjAzNzEgMTMuMDM3MSAxNi4zMjg2IDkgMTYuMzI4NiBDIDcuMDU3NCAxNi4zMjUyIDUuMTk1MyAxNS41NTIgMy44MjE3IDE0LjE3ODMgQyAyLjQ0OCAxMi44MDQ3IDEuNjc0OCAxMC45NDI2IDEuNjcxNCA5IEMgMS42NzE0IDQuOTYyOSA0Ljk2MjkgMS42NzE0IDkgMS42NzE0IFogTSA5IDAgQyA0LjAzNzEgMCAwIDQuMDM3MSAwIDkgQyAwIDEzLjk2MjkgNC4wMzcxIDE4IDkgMTggQyAxMy45NjI5IDE4IDE4IDEzLjk2MjkgMTggOSBDIDE4IDQuMDM3MSAxMy45NjI5IDAgOSAwIFogTSAxMC4yODU3IDMuODU3MSBIIDcuNzE0MyBWIDEwLjI4NTcgSCAxMC4yODU3IFYgMy44NTcxIFogTSAxMC4yODU3IDExLjU3MTQgSCA3LjcxNDMgViAxNC4xNDI5IEggMTAuMjg1NyBWIDExLjU3MTQgWiIgZmlsbD0iY3VycmVudENvbG9yIiBzdHJva2U9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiAvPjwvc3ZnPg==)

Linear attention kernel backends (GDN, KDA) follow a different pattern. They implement `LinearAttnKernelBase` in `python/sglang/srt/layers/attention/linear/kernels/` and are dispatched by `GDNKernelDispatcher` / `KDAKernelDispatcher` rather than registered via `@register_attention_backend`.

1.  Run without cuda graph. Support the two forward functions
    - forward_extend
      - Will be used for prefill, prefill with KV cache, and target verification
      - It will be called once per layer
    - forward_decode
      - Will be used for normal decode, and draft decode
      - It will be called once per layer
    - init_forward_metadata
      - Initialize the class and common metadata shared by all layers
      - Call the plan function for optimizations like split_kv
      - It will be called once per forward
2.  Run with cuda graph. It has two phases (capture and replay) and you need to implement three functions
    - init_cuda_graph_state
      - It will be called once during life time
      - Create all common shared buffers
    - init_forward_metadata_capture_cuda_graph
      - It will be called before capturing a cuda graph
      - It is similar to init_forward_metadata but write the medatada to some pre-defined buffers
    - init_forward_metadata_replay_cuda_graph
      - It will be called before replaying a cuda graph
      - This function is in the critical path and needs to be fast

Was this page helpful?

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1jdXJyZW50Ij48cGF0aCBkPSJNNS4yNSA3LjQ5NEM1LjI1IDcuMDE0IDUuNDIzIDYuNTUgNS43MzYgNi4xODdMMTAgMS4yNUMxMC44NTQgMS42NzcgMTEuMjUgMi42NzggMTAuOTIgMy41NzRMOS43NSA2Ljc1SDE0LjE1MkMxNS40NjUgNi43NSAxNi40MjEgNy45OTMgMTYuMDg1IDkuMjYyTDE0Ljg5NCAxMy43NjJDMTQuNjYyIDE0LjYzOSAxMy44NjggMTUuMjUgMTIuOTYxIDE1LjI1SDcuMjVDNi4xNDUgMTUuMjUgNS4yNSAxNC4zNTUgNS4yNSAxMy4yNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTQuMjUgNi43NUgyLjc1QzIuMTk3NzIgNi43NSAxLjc1IDcuMTk3NzIgMS43NSA3Ljc1VjE0LjI1QzEuNzUgMTQuODAyMyAyLjE5NzcyIDE1LjI1IDIuNzUgMTUuMjVINC4yNUM0LjgwMjI4IDE1LjI1IDUuMjUgMTQuODAyMyA1LjI1IDE0LjI1VjcuNzVDNS4yNSA3LjE5NzcyIDQuODAyMjggNi43NSA0LjI1IDYuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)Yes

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1jdXJyZW50Ij48cGF0aCBkPSJNNS4yNSAxMC41MDZDNS4yNSAxMC45ODYgNS40MjMgMTEuNDUgNS43MzYgMTEuODEzTDEwIDE2Ljc1QzEwLjg1NCAxNi4zMjMgMTEuMjUgMTUuMzIyIDEwLjkyIDE0LjQyNkw5Ljc1IDExLjI1SDE0LjE1MkMxNS40NjUgMTEuMjUgMTYuNDIxIDEwLjAwNyAxNi4wODUgOC43MzhMMTQuODk0IDQuMjM4QzE0LjY2MiAzLjM2MSAxMy44NjggMi43NSAxMi45NjEgMi43NUg3LjI1QzYuMTQ1IDIuNzUgNS4yNSAzLjY0NSA1LjI1IDQuNzUiIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjxwYXRoIGQ9Ik00LjI1IDIuNzVIMi43NUMyLjE5NzcyIDIuNzUgMS43NSAzLjE5NzcyIDEuNzUgMy43NVYxMC4yNUMxLjc1IDEwLjgwMjMgMi4xOTc3MiAxMS4yNSAyLjc1IDExLjI1SDQuMjVDNC44MDIyOCAxMS4yNSA1LjI1IDEwLjgwMjMgNS4yNSAxMC4yNVYzLjc1QzUuMjUgMy4xOTc3MiA0LjgwMjI4IDIuNzUgNC4yNSAyLjc1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PC9zdmc+)No

[](/docs/advanced_features/hyperparameter_tuning)

Hyperparameter Tuning

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0yLjUgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBkYXJrOnRleHQtZ3JheS02MDAgZ3JvdXAtaG92ZXI6dGV4dC1ncmF5LTUwMCBkYXJrOmdyb3VwLWhvdmVyOnRleHQtZ3JheS01MDAiIGRhdGEtY29tcG9uZW50LXBhcnQ9InBhZ2luYXRpb24tY2hldnJvbiI+PHBhdGggZD0iTTExLjUgMTUuMjVMNS4yNSA5TDExLjUgMi43NSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PC9zdmc+)Previous

[](/docs/advanced_features/hisparse_guide)

HiSparse: Hierarchical Sparse Attention

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0yLjUgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBkYXJrOnRleHQtZ3JheS02MDAgZ3JvdXAtaG92ZXI6dGV4dC1ncmF5LTUwMCBkYXJrOmdyb3VwLWhvdmVyOnRleHQtZ3JheS01MDAiIGRhdGEtY29tcG9uZW50LXBhcnQ9InBhZ2luYXRpb24tY2hldnJvbiI+PHBhdGggZD0iTTYuNSAyLjc1TDEyLjc1IDlMNi41IDE1LjI1IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)Next

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0yLjUgc2hyaW5rLTAgdGV4dC13aGl0ZSBkYXJrOnRleHQtd2hpdGUiPjxwYXRoIGQ9Ik05LjAgMS41NzU0TDguOTk5OSAxNi40MTcxIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48cGF0aCBkPSJNMi4yNTYzIDguMzE5TDguOTk5OSAxLjU3NTRMMTUuNzQzNSA4LjMxOTEiIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

[github![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZm9yY2VkLWNvbG9yczpmb3JjZWQtY29sb3ItYWRqdXN0LW5vbmUgZm9yY2VkLWNvbG9yczpiZy1bY29sb3I6Q2FudmFzVGV4dF0hIHctNSBoLTUgYmctZ3JheS00MDAgZGFyazpiZy1ncmF5LTUwMCBob3ZlcjpiZy1ncmF5LTUwMCBkYXJrOmhvdmVyOmJnLWdyYXktNDAwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgc3R5bGU9Ii13ZWJraXQtbWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL2dpdGh1Yi5zdmcmcXVvdDspOy13ZWJraXQtbWFzay1yZXBlYXQ6bm8tcmVwZWF0Oy13ZWJraXQtbWFzay1wb3NpdGlvbjpjZW50ZXI7bWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL2dpdGh1Yi5zdmcmcXVvdDspO21hc2stcmVwZWF0Om5vLXJlcGVhdDttYXNrLXBvc2l0aW9uOmNlbnRlciI+PC9zdmc+)](https://github.com/sgl-project/sglang)[x![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZm9yY2VkLWNvbG9yczpmb3JjZWQtY29sb3ItYWRqdXN0LW5vbmUgZm9yY2VkLWNvbG9yczpiZy1bY29sb3I6Q2FudmFzVGV4dF0hIHctNSBoLTUgYmctZ3JheS00MDAgZGFyazpiZy1ncmF5LTUwMCBob3ZlcjpiZy1ncmF5LTUwMCBkYXJrOmhvdmVyOmJnLWdyYXktNDAwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgc3R5bGU9Ii13ZWJraXQtbWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL3gtdHdpdHRlci5zdmcmcXVvdDspOy13ZWJraXQtbWFzay1yZXBlYXQ6bm8tcmVwZWF0Oy13ZWJraXQtbWFzay1wb3NpdGlvbjpjZW50ZXI7bWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL3gtdHdpdHRlci5zdmcmcXVvdDspO21hc2stcmVwZWF0Om5vLXJlcGVhdDttYXNrLXBvc2l0aW9uOmNlbnRlciI+PC9zdmc+)](https://x.com/lmsysorg)[linkedin![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZm9yY2VkLWNvbG9yczpmb3JjZWQtY29sb3ItYWRqdXN0LW5vbmUgZm9yY2VkLWNvbG9yczpiZy1bY29sb3I6Q2FudmFzVGV4dF0hIHctNSBoLTUgYmctZ3JheS00MDAgZGFyazpiZy1ncmF5LTUwMCBob3ZlcjpiZy1ncmF5LTUwMCBkYXJrOmhvdmVyOmJnLWdyYXktNDAwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgc3R5bGU9Ii13ZWJraXQtbWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL2xpbmtlZGluLnN2ZyZxdW90Oyk7LXdlYmtpdC1tYXNrLXJlcGVhdDpuby1yZXBlYXQ7LXdlYmtpdC1tYXNrLXBvc2l0aW9uOmNlbnRlcjttYXNrLWltYWdlOnVybCgmcXVvdDtodHRwczovL2QzZ2syYzV4aW0xamUyLmNsb3VkZnJvbnQubmV0L2ZvbnRhd2Vzb21lL3Y3LjIuMC9icmFuZHMvbGlua2VkaW4uc3ZnJnF1b3Q7KTttYXNrLXJlcGVhdDpuby1yZXBlYXQ7bWFzay1wb3NpdGlvbjpjZW50ZXIiPjwvc3ZnPg==)](https://www.linkedin.com/company/sgl-project/posts?feedView=all)[slack![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZm9yY2VkLWNvbG9yczpmb3JjZWQtY29sb3ItYWRqdXN0LW5vbmUgZm9yY2VkLWNvbG9yczpiZy1bY29sb3I6Q2FudmFzVGV4dF0hIHctNSBoLTUgYmctZ3JheS00MDAgZGFyazpiZy1ncmF5LTUwMCBob3ZlcjpiZy1ncmF5LTUwMCBkYXJrOmhvdmVyOmJnLWdyYXktNDAwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgc3R5bGU9Ii13ZWJraXQtbWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL3NsYWNrLnN2ZyZxdW90Oyk7LXdlYmtpdC1tYXNrLXJlcGVhdDpuby1yZXBlYXQ7LXdlYmtpdC1tYXNrLXBvc2l0aW9uOmNlbnRlcjttYXNrLWltYWdlOnVybCgmcXVvdDtodHRwczovL2QzZ2syYzV4aW0xamUyLmNsb3VkZnJvbnQubmV0L2ZvbnRhd2Vzb21lL3Y3LjIuMC9icmFuZHMvc2xhY2suc3ZnJnF1b3Q7KTttYXNrLXJlcGVhdDpuby1yZXBlYXQ7bWFzay1wb3NpdGlvbjpjZW50ZXIiPjwvc3ZnPg==)](https://slack.sglang.io/)[discord![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZm9yY2VkLWNvbG9yczpmb3JjZWQtY29sb3ItYWRqdXN0LW5vbmUgZm9yY2VkLWNvbG9yczpiZy1bY29sb3I6Q2FudmFzVGV4dF0hIHctNSBoLTUgYmctZ3JheS00MDAgZGFyazpiZy1ncmF5LTUwMCBob3ZlcjpiZy1ncmF5LTUwMCBkYXJrOmhvdmVyOmJnLWdyYXktNDAwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgc3R5bGU9Ii13ZWJraXQtbWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL2Rpc2NvcmQuc3ZnJnF1b3Q7KTstd2Via2l0LW1hc2stcmVwZWF0Om5vLXJlcGVhdDstd2Via2l0LW1hc2stcG9zaXRpb246Y2VudGVyO21hc2staW1hZ2U6dXJsKCZxdW90O2h0dHBzOi8vZDNnazJjNXhpbTFqZTIuY2xvdWRmcm9udC5uZXQvZm9udGF3ZXNvbWUvdjcuMi4wL2JyYW5kcy9kaXNjb3JkLnN2ZyZxdW90Oyk7bWFzay1yZXBlYXQ6bm8tcmVwZWF0O21hc2stcG9zaXRpb246Y2VudGVyIj48L3N2Zz4=)](https://discord.gg/4ugb2t6YY2)

[Powered by![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI3NCIgaGVpZ2h0PSIzNjciIHZpZXdib3g9IjAgMCAxMjc0IDM2NyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBjbGFzcz0iaC0zLjUgdy1hdXRvIHRyYW5zbGF0ZS15LTAuNzUiPjxwYXRoIGQ9Ik0xMTU0LjM4IDM2Ni4wMzhIMTA5Ny44NkwxMTM3LjY5IDI3Ni4xNEwxMDU4LjA0IDk3LjEwNDZIMTExNC45M0wxMTYxLjM1IDIwOS4zMzdDMTE2Mi45NyAyMTMuMjYgMTE2OC41MyAyMTMuMjUzIDExNzAuMTQgMjA5LjMyNUwxMjE2LjIxIDk3LjEwNDZIMTI3My40OUwxMTU0LjM4IDM2Ni4wMzhaIiBmaWxsPSJjdXJyZW50Q29sb3IiIC8+PHBhdGggZD0iTTk4Mi43MTQgMjg2Ljc2MVYxNDIuNjIySDk0NC40MDNWOTcuMTA0MUg5ODIuNzE0VjcyLjQ0ODhDOTgyLjcxNCA0OS45NDI5IDk4OS41NDIgMzIuMjQxNiAxMDAzLjIgMTkuMzQ1QzEwMTYuODUgNi40NDgzMiAxMDM0LjE3IDAgMTA1NS4xNiAwQzEwNjguMDYgMCAxMDc5LjA2IDEuMzkwODEgMTA4OC4xNiA0LjE3MjQ0VjUwLjA2OTNDMTA4Mi4wOSA0Ny43OTM0IDEwNzUuMDEgNDYuNjU1NSAxMDY2LjkyIDQ2LjY1NTVDMTA1NS41NCA0Ni42NTU1IDEwNDcuMzIgNDkuMTg0MyAxMDQyLjI3IDU0LjI0MThDMTAzNy4yMSA1OS4wNDY0IDEwMzQuNjggNjcuMjY0OCAxMDM0LjY4IDc4Ljg5NzFWOTcuMTA0MUgxMDg4LjE2VjE0Mi42MjJIMTAzNC42OFYyODYuNzYxSDk4Mi43MTRaIiBmaWxsPSJjdXJyZW50Q29sb3IiIC8+PHBhdGggZD0iTTg5Ny45MTYgNjYuMDAwNUM4ODkuMDY2IDY2LjAwMDUgODgxLjM1MyA2Mi44Mzk1IDg3NC43NzggNTYuNTE3NkM4NjguMjAzIDQ5Ljk0MjkgODY0LjkxNiA0Mi4xMDM3IDg2NC45MTYgMzMuMDAwMkM4NjQuOTE2IDIzLjg5NjcgODY4LjIwMyAxNi4xODQgODc0Ljc3OCA5Ljg2MjE1Qzg4MS4zNTMgMy4yODczOCA4ODkuMDY2IDAgODk3LjkxNiAwQzkwNy4yNzMgMCA5MTUuMTEyIDMuMjg3MzggOTIxLjQzNCA5Ljg2MjE1QzkyOC4wMDggMTYuMTg0IDkzMS4yOTYgMjMuODk2NyA5MzEuMjk2IDMzLjAwMDJDOTMxLjI5NiA0Mi4xMDM3IDkyOC4wMDggNDkuOTQyOSA5MjEuNDM0IDU2LjUxNzZDOTE1LjExMiA2Mi44Mzk1IDkwNy4yNzMgNjYuMDAwNSA4OTcuOTE2IDY2LjAwMDVaTTg3Mi4xMjMgMjg2Ljc2MVY5Ny4xMDQxSDkyNC4wODlWMjg2Ljc2MUg4NzIuMTIzWiIgZmlsbD0iY3VycmVudENvbG9yIiAvPjxwYXRoIGQ9Ik03ODEuNjM4IDI4Ni43NjFWMi4yNzYwOUg4MzMuNjA0VjI4Ni43NjFINzgxLjYzOFoiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48cGF0aCBkPSJNNzIyLjkzNCAyODkuMDM3QzcwMS42OTMgMjg5LjAzNyA2ODQuMjQ0IDI4My4yMjEgNjcwLjU4OSAyNzEuNTg4QzY1Ny4xODcgMjU5LjcwMyA2NTAuNDg1IDI0Mi42MzQgNjUwLjQ4NSAyMjAuMzgxVjE0Mi42MjJINjEyLjE3NVY5Ny4xMDQ0SDY1MC40ODVWNDQuMzc5OUg3MDIuNDUxVjk3LjEwNDRINzU1LjkzNFYxNDIuNjIySDcwMi40NTFWMjEwLjE0QzcwMi40NTEgMjIxLjc3MiA3MDQuOTggMjMwLjExNyA3MTAuMDM4IDIzNS4xNzRDNzE1LjA5NSAyMzkuOTc5IDcyMy4zMTMgMjQyLjM4MSA3MzQuNjkzIDI0Mi4zODFDNzQyLjc4NSAyNDIuMzgxIDc0OS44NjUgMjQxLjI0MyA3NTUuOTM0IDIzOC45NjdWMjg0Ljg2NEM3NDYuODMxIDI4Ny42NDYgNzM1LjgzMSAyODkuMDM3IDcyMi45MzQgMjg5LjAzN1oiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48cGF0aCBkPSJNNDE3LjY3NCAyODYuNzYxVjk3LjEwNDFINDY5LjY0VjExMC45NjdDNDY5LjY0IDExMy4zMTEgNDcyLjgzIDExNC4zNDcgNDc0LjM4MiAxMTIuNTkxQzQ4NS45NjcgOTkuNDg0OCA1MDIuNDY3IDkyLjkzMTcgNTIzLjg4MSA5Mi45MzE3QzU0Ni42NCA5Mi45MzE3IDU2NC40NjggMTAwLjUxOCA1NzcuMzY1IDExNS42OUM1OTAuNTE0IDEzMC42MSA1OTcuMDg5IDE1MC41ODcgNTk3LjA4OSAxNzUuNjIyVjI4Ni43NjFINTQ1LjEyM1YxODQuMzQ2QzU0NS4xMjMgMTcwLjQzOCA1NDIuMjE1IDE1OS42OTEgNTM2LjM5OSAxNTIuMTA1QzUzMC41ODMgMTQ0LjI2NSA1MjIuMzY0IDE0MC4zNDYgNTExLjc0MyAxNDAuMzQ2QzQ5OS4xIDE0MC4zNDYgNDg4Ljg1OCAxNDQuODk4IDQ4MS4wMTkgMTU0LjAwMUM0NzMuNDMzIDE2My4xMDUgNDY5LjY0IDE3Ni41MDcgNDY5LjY0IDE5NC4yMDhWMjg2Ljc2MUg0MTcuNjc0WiIgZmlsbD0iY3VycmVudENvbG9yIiAvPjxwYXRoIGQ9Ik0zNTIuOTgxIDY2LjAwMDVDMzQ0LjEzIDY2LjAwMDUgMzM2LjQxNyA2Mi44Mzk1IDMyOS44NDMgNTYuNTE3NkMzMjMuMjY4IDQ5Ljk0MjkgMzE5Ljk4IDQyLjEwMzcgMzE5Ljk4IDMzLjAwMDJDMzE5Ljk4IDIzLjg5NjcgMzIzLjI2OCAxNi4xODQgMzI5Ljg0MyA5Ljg2MjE1QzMzNi40MTcgMy4yODczOCAzNDQuMTMgMCAzNTIuOTgxIDBDMzYyLjMzNyAwIDM3MC4xNzYgMy4yODczOCAzNzYuNDk4IDkuODYyMTVDMzgzLjA3MyAxNi4xODQgMzg2LjM2IDIzLjg5NjcgMzg2LjM2IDMzLjAwMDJDMzg2LjM2IDQyLjEwMzcgMzgzLjA3MyA0OS45NDI5IDM3Ni40OTggNTYuNTE3NkMzNzAuMTc2IDYyLjgzOTUgMzYyLjMzNyA2Ni4wMDA1IDM1Mi45ODEgNjYuMDAwNVpNMzI3LjE4NyAyODYuNzYxVjk3LjEwNDFIMzc5LjE1M1YyODYuNzYxSDMyNy4xODdaIiBmaWxsPSJjdXJyZW50Q29sb3IiIC8+PHBhdGggZD0iTTIzOC45NjcgMjg2Ljc2MVYxODUuNDg0QzIzOC45NjcgMTU1LjM5MiAyMjkuMTA1IDE0MC4zNDYgMjA5LjM4MSAxNDAuMzQ2QzE5OC4wMDEgMTQwLjM0NiAxODguODk4IDE0NC42NDUgMTgyLjA3IDE1My4yNDJDMTc1LjQ5NSAxNjEuODQgMTcxLjk1NSAxNzQuNjEgMTcxLjQ0OSAxOTEuNTUzVjI4Ni43NjFIMTE5LjQ4NFYxODUuNDg0QzExOS40ODQgMTU1LjM5MiAxMDkuNjIxIDE0MC4zNDYgODkuODk3MiAxNDAuMzQ2Qzc4LjI2NDkgMTQwLjM0NiA2OS4wMzUgMTQ0Ljg5OCA2Mi4yMDczIDE1NC4wMDFDNTUuMzc5NyAxNjMuMTA1IDUxLjk2NTkgMTc2LjUwNyA1MS45NjU5IDE5NC4yMDhWMjg2Ljc2MUgwVjk3LjEwNDFINTEuOTY1OVYxMTEuMTAzQzUxLjk2NTkgMTEzLjQzNSA1NS4xMDE0IDExNC40NjIgNTYuNjMzIDExMi43MDRDNjguMTEzNiA5OS41MjIzIDgzLjM3NDEgOTIuOTMxNyAxMDIuNDE1IDkyLjkzMTdDMTI3LjQzNiA5Mi45MzE3IDE0Ni4yODMgMTAzLjI2MiAxNTguOTUzIDEyMy45MjNDMTU5Ljk1MyAxMjUuNTUzIDE2Mi40MTIgMTI1LjUyNyAxNjMuNDA2IDEyMy44OTRDMTY4Ljg4NCAxMTQuODkxIDE3Ni40OTYgMTA3LjczMSAxODYuMjQzIDEwMi40MTVDMTk3LjM2OSA5Ni4wOTI2IDIwOC42MjIgOTIuOTMxNyAyMjAuMDAyIDkyLjkzMTdDMjQyLjUwNyA5Mi45MzE3IDI1OS45NTYgMTAwLjM5MiAyNzIuMzQ3IDExNS4zMTFDMjg0LjczOCAxMzAuMjMxIDI5MC45MzMgMTUwLjcxNCAyOTAuOTMzIDE3Ni43NlYyODYuNzYxSDIzOC45NjdaIiBmaWxsPSJjdXJyZW50Q29sb3IiIC8+PC9zdmc+)This documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=lmsysorg)
