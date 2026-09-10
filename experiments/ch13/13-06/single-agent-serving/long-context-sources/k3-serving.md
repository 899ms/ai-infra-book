<!-- 从 k3-serving.html 迁移的资料快照；原始 HTML SHA-256: a0951b361f6d7bbabee225a9276c89a0fe676818c555874052c0184d6fb1f364。 -->

## ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNMi43NSAxNC4yNUgxNS4yNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuNzUgMy43NUgxNS4yNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuNzUgOUg4LjI1IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)On this page

- [Deployment](#deployment)
  - [Mamba ratio calculator](#mamba-ratio-calculator)
- [Advanced Features Playground](#advanced-features-playground)
- [1. Model Introduction](#1-model-introduction)
- [2. Configuration Tips](#2-configuration-tips)
- [3. Advanced Usage](#3-advanced-usage)
  - [3.1 Reasoning](#3-1-reasoning)
  - [3.2 Tool Calling](#3-2-tool-calling)
  - [3.3 HiCache (Hierarchical KV Caching)](#3-3-hicache-hierarchical-kv-caching)
  - [3.4 PD Disaggregation](#3-4-pd-disaggregation)
  - [Deep PP for prefill](#deep-pp-for-prefill)
  - [3.5 VLM Serving Profiles](#3-5-vlm-serving-profiles)
  - [VLM feature transport](#vlm-feature-transport)
  - [VLM compatibility](#vlm-compatibility)
  - [Should ViT BCG be enabled?](#should-vit-bcg-be-enabled)
  - [Low-HBM VLM](#low-hbm-vlm)
  - [3.6 Large-Scale Serving Presets (16–64 GPUs, Blackwell)](#3-6-large-scale-serving-presets-16%E2%80%9364-gpus-blackwell)

Kimi (Moonshot AI)

# Kimi-K3

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)Copy pageCopy page

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBmb2N1c2FibGU9ImZhbHNlIiBjbGFzcz0ic2l6ZS0zIHRyYW5zaXRpb24tdHJhbnNmb3JtIHRleHQtZ3JheS00MDAgZ3JvdXAtaG92ZXI6dGV4dC1ncmF5LTYwMCBkYXJrOnRleHQtZ3JheS02MDAgZGFyazpncm91cC1ob3Zlcjp0ZXh0LWdyYXktNDAwIHNocmluay0wIHJvdGF0ZS05MCI+PHBhdGggZD0iTTYuNSAyLjc1TDEyLjc1IDlMNi41IDE1LjI1IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Deploy Moonshot AI’s Kimi-K3 with SGLang — a 2.8T-parameter hybrid Mixture-of-Experts vision-language model (Kimi Delta Attention + MLA, 16/896 active experts) with NVIDIA, AMD, and NPU recipes.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)Copy pageCopy page

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBmb2N1c2FibGU9ImZhbHNlIiBjbGFzcz0ic2l6ZS0zIHRyYW5zaXRpb24tdHJhbnNmb3JtIHRleHQtZ3JheS00MDAgZ3JvdXAtaG92ZXI6dGV4dC1ncmF5LTYwMCBkYXJrOnRleHQtZ3JheS02MDAgZGFyazpncm91cC1ob3Zlcjp0ZXh0LWdyYXktNDAwIHNocmluay0wIHJvdGF0ZS05MCI+PHBhdGggZD0iTTYuNSAyLjc1TDEyLjc1IDlMNi41IDE1LjI1IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

## 

[​](#deployment)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Deployment

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTMgc2hyaW5rLTAgdGV4dC1ncmF5LTYwMCB0cmFuc2l0aW9uLXRyYW5zZm9ybSBkdXJhdGlvbi0yMDAgZGFyazp0ZXh0LWdyYXktNDAwIC1yb3RhdGUtOTAiPjxwYXRoIGQ9Ik0xNC4wMjM4IDQuMDAwMDJIMy45NzU3NkMzLjMzNzc2IDQuMDAwMDIgMi43NDk3NiA0LjM0NzAyIDIuNDQyNzYgNC45MDYwMkMyLjEzNTc2IDUuNDY1MDIgMi4xNTU3NiA2LjE0ODAyIDIuNDk3NzYgNi42ODcwMkw3LjUyMTc2IDE0LjYxQzcuODQ0NzYgMTUuMTE5IDguMzk2NzYgMTUuNDIyIDguOTk5NzYgMTUuNDIyQzkuNjAyNzYgMTUuNDIyIDEwLjE1NDggMTUuMTE4IDEwLjQ3NzggMTQuNjFMMTUuNTAyOCA2LjY4NjAyQzE1Ljg0MzggNi4xNDcwMiAxNS44NjQ4IDUuNDY0MDIgMTUuNTU3OCA0LjkwNTAyQzE1LjI1MDggNC4zNDYwMiAxNC42NjI4IDMuOTk5MDIgMTQuMDI0OCAzLjk5OTAyTDE0LjAyMzggNC4wMDAwMloiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48L3N2Zz4=)

Install SGLang

For all methods and hardware platforms, see the [official SGLang installation guide](/docs/get-started/install). The two paths below match the **Python / Docker** toggle in the command panel.

- Python (pip / uv)

- Docker

- NPU

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
pip install --upgrade pip
pip install uv
uv pip install --prerelease=allow sglang
```

Then run the **Python** output of the command panel below in that environment.

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
docker pull lmsysorg/sglang:latest                                  # NVIDIA (CUDA)
docker pull lmsysorg/sglang-rocm:v0.5.18-rocm720-mi35x-20260903     # AMD MI350X / MI355X (ROCm)
```

For how to launch the image, see [Install → Method 3: Using Docker](/docs/get-started/install#method-3-using-docker). Substitute the inner `sglang serve ...` with what the command generator below produces.

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
docker pull quay.io/ascend/sglang:main-cann9.0.0-a3
```

For host and platform setup, see the [NPU installation guide](/docs/hardware-platforms/ascend-npus/getting-started/installation) and the [quick start guide](/docs/hardware-platforms/ascend-npus/getting-started/quick_start).**Weights (NPU):** [Kimi-K3-W4A8](https://www.modelscope.cn/models/sgl-npu/Kimi-K3-W4A8) (W4A8, 1.49 TB) · [Kimi-K3-DSpark](https://www.modelscope.cn/models/RadixArk/Kimi-K3-DSpark) (DSPARK draft, 4.5 GB)

Pick your hardware, then the deployment shape and operating point. Node count follows the hardware recipe (B200 2×8, GB200 4×4, H100 4×8, B300 1×8, H200 2×8 — 4×8 on Unified High-Throughput, GB300 2×4, MI350X/MI355X 1×8, Atlas 800I A3 4×8 — 32 cards / 64 dies), so it is not a separate choice. If you serve the NVFP4 checkpoint (`nvidia/Kimi-K3-NVFP4`, the **Quantization** row in the panel below), use the `lmsysorg/sglang:dev-dev-kimi-k3-nvfp4` image. **PD Mode** — `Unified` serves prefill and decode together. `Prefill` / `Decode` split them into dedicated pools (see [PD disaggregation](#3-4-pd-disaggregation)); `Prefill` ships two strategies, both chunked at 16k. On the 8-GPU platforms (B300 1×8, GB300 2×4), `Default` is TP8 and `Long-Context` is `--pp-size 8 --tp-size 1`. On the 16-GPU platforms (B200 2×8, GB200 4×4), both are `--pp-size 16 --tp-size 1` and differ only in `--mem-fraction-static` (0.85 vs 0.90) — deep PP is the throughput shape there, not just the long-context one (see [Deep PP](#deep-pp-for-prefill)). **Strategy** — the operating point within that shape:

- **Low-Latency** — no DCP, so the MLA KV stays TP-replicated. For chat. B200 splits its two nodes into PP2 × TP8; every other platform is flat TP.
- **Balanced** — the accuracy-preserving default: PP2 × DCPEP8 on B200 (the two pipeline stages and DCP8 split KV and KDA state), TP16/DCP16 on GB200, TP8/DCP8 on B300/GB300, TP8 ROCm/AITER on MI35x.
- **High-Throughput** — the large-scale lane: pick a **Cluster Size** and **Large-Scale Preset** in the Playground ([details](#large-scale-presets)). The cell itself is Balanced, except on H100 (plus `extra_buffer_lazy`) and H200 (widens to 4×8 TP32/EP32 at `--mem-fraction-static 0.90`).

`Long-Context` appears only under the `Prefill` PD mode; for long-context unified serving on B200, start from High-Throughput and raise `--context-length`. **Spec Decode** — layers onto the strategy without changing it, on every platform except B200. DSPARK proposes 7 draft tokens per step (tune in the Playground) and requires `pp_size == 1`, so on B200 it also drops the pipeline and re-lays the same 16 GPUs flat: PP2 × TP8 → TP16, PP2 × DCPEP8 → DCPEP16. DFLASH has no published draft checkpoint. The win is largest on short interactive traffic and fades as the prompt grows.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgdGV4dC1ibHVlLTgwMCBkYXJrOnRleHQtYmx1ZS0zMDAiPjxwYXRoIGQ9Ik0gOSAxLjY3MTQgQyAxMy4wMzcxIDEuNjcxNCAxNi4zMjg2IDQuOTYyOSAxNi4zMjg2IDkgQyAxNi4zMjg2IDEzLjAzNzEgMTMuMDM3MSAxNi4zMjg2IDkgMTYuMzI4NiBDIDcuMDU3NCAxNi4zMjUyIDUuMTk1MyAxNS41NTIgMy44MjE3IDE0LjE3ODMgQyAyLjQ0OCAxMi44MDQ3IDEuNjc0OCAxMC45NDI2IDEuNjcxNCA5IEMgMS42NzE0IDQuOTYyOSA0Ljk2MjkgMS42NzE0IDkgMS42NzE0IFogTSA5IDAgQyA0LjAzNzEgMCAwIDQuMDM3MSAwIDkgQyAwIDEzLjk2MjkgNC4wMzcxIDE4IDkgMTggQyAxMy45NjI5IDE4IDE4IDEzLjk2MjkgMTggOSBDIDE4IDQuMDM3MSAxMy45NjI5IDAgOSAwIFogTSAxMC4yODU3IDMuODU3MSBIIDcuNzE0MyBWIDEwLjI4NTcgSCAxMC4yODU3IFYgMy44NTcxIFogTSAxMC4yODU3IDExLjU3MTQgSCA3LjcxNDMgViAxNC4xNDI5IEggMTAuMjg1NyBWIDExLjU3MTQgWiIgZmlsbD0iY3VycmVudENvbG9yIiBzdHJva2U9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiAvPjwvc3ZnPg==)

`--mamba-full-memory-ratio` is the one sizing flag, computed live: set your average request length in the [Mamba ratio calculator](#mamba-ratio-calculator); everything else follows the panels, and the result is pinned into the command. (The Atlas 800I A3 uses `--max-mamba-cache-size` instead.)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgdGV4dC1ibHVlLTgwMCBkYXJrOnRleHQtYmx1ZS0zMDAiPjxwYXRoIGQ9Ik0gOSAxLjY3MTQgQyAxMy4wMzcxIDEuNjcxNCAxNi4zMjg2IDQuOTYyOSAxNi4zMjg2IDkgQyAxNi4zMjg2IDEzLjAzNzEgMTMuMDM3MSAxNi4zMjg2IDkgMTYuMzI4NiBDIDcuMDU3NCAxNi4zMjUyIDUuMTk1MyAxNS41NTIgMy44MjE3IDE0LjE3ODMgQyAyLjQ0OCAxMi44MDQ3IDEuNjc0OCAxMC45NDI2IDEuNjcxNCA5IEMgMS42NzE0IDQuOTYyOSA0Ljk2MjkgMS42NzE0IDkgMS42NzE0IFogTSA5IDAgQyA0LjAzNzEgMCAwIDQuMDM3MSAwIDkgQyAwIDEzLjk2MjkgNC4wMzcxIDE4IDkgMTggQyAxMy45NjI5IDE4IDE4IDEzLjk2MjkgMTggOSBDIDE4IDQuMDM3MSAxMy45NjI5IDAgOSAwIFogTSAxMC4yODU3IDMuODU3MSBIIDcuNzE0MyBWIDEwLjI4NTcgSCAxMC4yODU3IFYgMy44NTcxIFogTSAxMC4yODU3IDExLjU3MTQgSCA3LjcxNDMgViAxNC4xNDI5IEggMTAuMjg1NyBWIDExLjU3MTQgWiIgZmlsbD0iY3VycmVudENvbG9yIiBzdHJva2U9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiAvPjwvc3ZnPg==)

B300 1×8 Unified speed numbers are measured on `v0.5.18 @ 71de97b2` with `--random-range-ratio 1.0`, `--warmup-requests 64`, `--flush-cache`, at ISL 8192 / OSL 1024. DSPARK cells pin the acceptance length via the serve env `SGLANG_SIMULATE_ACC_LEN=4.5` — they report what block size 7 delivers at that acceptance, not a measured acceptance rate for this workload. Balanced DSPARK adds `--max-running-requests 256`; without it speculation resets the cap to 48. The KDA state pool still clamps admission below that (101 / 68 / 91 / 60 concurrent requests for MXFP4 NOSPEC / MXFP4 DSPARK / NVFP4 NOSPEC / NVFP4 DSPARK), which is why no point past concurrency 64 is published for Balanced.

### 

[​](#mamba-ratio-calculator)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Mamba ratio calculator

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTMgc2hyaW5rLTAgdGV4dC1ncmF5LTYwMCB0cmFuc2l0aW9uLXRyYW5zZm9ybSBkdXJhdGlvbi0yMDAgZGFyazp0ZXh0LWdyYXktNDAwIC1yb3RhdGUtOTAiPjxwYXRoIGQ9Ik0xNC4wMjM4IDQuMDAwMDJIMy45NzU3NkMzLjMzNzc2IDQuMDAwMDIgMi43NDk3NiA0LjM0NzAyIDIuNDQyNzYgNC45MDYwMkMyLjEzNTc2IDUuNDY1MDIgMi4xNTU3NiA2LjE0ODAyIDIuNDk3NzYgNi42ODcwMkw3LjUyMTc2IDE0LjYxQzcuODQ0NzYgMTUuMTE5IDguMzk2NzYgMTUuNDIyIDguOTk5NzYgMTUuNDIyQzkuNjAyNzYgMTUuNDIyIDEwLjE1NDggMTUuMTE4IDEwLjQ3NzggMTQuNjFMMTUuNTAyOCA2LjY4NjAyQzE1Ljg0MzggNi4xNDcwMiAxNS44NjQ4IDUuNDY0MDIgMTUuNTU3OCA0LjkwNTAyQzE1LjI1MDggNC4zNDYwMiAxNC42NjI4IDMuOTk5MDIgMTQuMDI0OCAzLjk5OTAyTDE0LjAyMzggNC4wMDAwMloiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48L3N2Zz4=)

How --mamba-full-memory-ratio is calculated

`--mamba-full-memory-ratio` is the ratio between the KDA state pool and the MLA KV pool. Every parameter below except `L` is read live from the Deploy panel and Playground selection; the balanced value is the per-request cost ratio:

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
ratio = (S + D) x state_bytes / (L x (mla_kv_bytes / DCP + draft_kv_bytes))
```

- `S` — KDA state slots per request: `extra_buffer=5`, `extra_buffer_lazy=4`, `no_buffer=3`, disabled radix cache `=1`. `SGLANG_OPT_MAMBA_SKIP_DECODE_LOCK` frees one slot on the extra-buffer strategies; with the overlap scheduler off (or `pp > 1`, which disables it) the track buffer costs one slot instead of two.
- `D` — verify intermediate states under speculative decoding: `0` when disabled, otherwise DSPARK block size + 1 (`8` at the default 7). ReplaySSM (`--enable-linear-replayssm-spec`) folds them into a per-slot ring, returning `D` to `0`.
- `state_bytes` — one state slot’s bytes, from K3’s fixed geometry, the attention-TP width, and the SSM dtype.
- `mla_kv_bytes` — one token’s MLA latent KV bytes (KV-dtype dependent); DCP shards it across its ranks. The DSPARK draft model’s KV (~1.4 KB per token) is replicated on every rank, so it enters flat — negligible without DCP, the same order as the sharded MLA share under DCP8.
- `L` — average total request length in tokens: input + output.

## 

[​](#advanced-features-playground)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Advanced Features Playground

The Playground is where you experiment with **SGLang features beyond the deployment matrix**. The Deploy panel above emits the recipes the SGLang team is converging on; the Playground lets you turn on additional knobs on top of whichever cell the Deploy panel is currently showing.

## 

[​](#1-model-introduction)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

1. Model Introduction

**Kimi-K3** is Moonshot AI’s flagship hybrid MoE vision-language model: **2.8 trillion parameters**, **16 of 896 experts** active per token, roughly **2.5× the scaling efficiency of Kimi-K2**. The backbone interleaves **Kimi Delta Attention (KDA)** with MLA across 93 layers (plus Attention Residuals and Stable LatentMoE); serving supports image input and a **1M-token** window with prefix caching. Weights ship in **MXFP4**: the FlashInfer MXFP4 (trtllm-gen SiTU) runner serves them on Blackwell, Marlin (W4A16) elsewhere, MegaMoE for short-context batch throughput. K3 **always runs with thinking enabled**, with reasoning depth controlled by `reasoning_effort` (`low` / `high` / `max`; default `max`).

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgdGV4dC1ibHVlLTgwMCBkYXJrOnRleHQtYmx1ZS0zMDAiPjxwYXRoIGQ9Ik0gOSAxLjY3MTQgQyAxMy4wMzcxIDEuNjcxNCAxNi4zMjg2IDQuOTYyOSAxNi4zMjg2IDkgQyAxNi4zMjg2IDEzLjAzNzEgMTMuMDM3MSAxNi4zMjg2IDkgMTYuMzI4NiBDIDcuMDU3NCAxNi4zMjUyIDUuMTk1MyAxNS41NTIgMy44MjE3IDE0LjE3ODMgQyAyLjQ0OCAxMi44MDQ3IDEuNjc0OCAxMC45NDI2IDEuNjcxNCA5IEMgMS42NzE0IDQuOTYyOSA0Ljk2MjkgMS42NzE0IDkgMS42NzE0IFogTSA5IDAgQyA0LjAzNzEgMCAwIDQuMDM3MSAwIDkgQyAwIDEzLjk2MjkgNC4wMzcxIDE4IDkgMTggQyAxMy45NjI5IDE4IDE4IDEzLjk2MjkgMTggOSBDIDE4IDQuMDM3MSAxMy45NjI5IDAgOSAwIFogTSAxMC4yODU3IDMuODU3MSBIIDcuNzE0MyBWIDEwLjI4NTcgSCAxMC4yODU3IFYgMy44NTcxIFogTSAxMC4yODU3IDExLjU3MTQgSCA3LjcxNDMgViAxNC4xNDI5IEggMTAuMjg1NyBWIDExLjU3MTQgWiIgZmlsbD0iY3VycmVudENvbG9yIiBzdHJva2U9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiAvPjwvc3ZnPg==)

Kimi-K3 is Moonshot AI’s first open-source model in the trillion-plus class; **full model weights are scheduled to release by July 27, 2026**. The recipes on this page were validated on the public [`sgl-project/sglang` `kimi-k3` branch](https://github.com/sgl-project/sglang/tree/kimi-k3) — the HuggingFace repository (`moonshotai/Kimi-K3`) and a public `lmsysorg/sglang` image with K3 support will be available at launch.The B300 1×8 `Unified` Low-Latency and Balanced cells are **Verified** — a speed round on the final weights is published below. Every other cell is still marked **Final Verification In Progress**: the recipe runs, but its serving round on the final weights and current code is still open. Accuracy has not been re-measured on any cell — re-measure before you rely on one.

**Recommended generation:** `temperature=1.0`, `top_p=0.95`, `presence_penalty=0`, `frequency_penalty=0` (fixed by the model; informational — do not hardcode in sample code). **Resources:** [HuggingFace](https://huggingface.co/moonshotai/Kimi-K3) · [Kimi-K3 Quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart).

## 

[​](#2-configuration-tips)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

2. Configuration Tips

**Memory: two pools, one flag.** K3 splits static memory into a worst-case-reserved **KDA state pool** (it sets the concurrency ceiling) and a paged **MLA KV pool**, divided by `--mamba-full-memory-ratio`. The command panel pins that flag to the [calculator](#mamba-ratio-calculator)’s output — set your average request length there; every other calculator input follows the panels. (On the Atlas 800I A3: `--max-mamba-cache-size`, no calculator.) After boot, read back `max_total_num_tokens` (the KV side) and the admitted-request cap (the state side). Capacity levers, all in the Playground. Each trades precision or cache behavior for capacity — re-verify accuracy on your workload:

| Lever | Effect |
|----|----|
| `--mamba-radix-cache-strategy extra_buffer_lazy` | 4 state slots per request instead of 5 |
| `--mamba-ssm-dtype bfloat16` | ~halves state bytes; with spec on, KDA verification falls back from the fused kernel to Triton |
| `--kv-cache-dtype fp8_e4m3` | halves KV bytes per token; under PD both roles must match at connect |
| `--mem-fraction-static` 0.90–0.92 | cheapest first win when the boot log shows a large idle `avail mem` |
| `SGLANG_OPT_MAMBA_SKIP_DECODE_LOCK=1` | frees one more slot per request (experimental, under validation) |

Speculation: DSPARK holds block size + 1 (= 8) intermediate states per request — the calculator folds this in — and an unset `--max-running-requests` resets to 48 under spec (the command panel reminds you; set it explicitly to raise). **MoE runner.** Leave `--moe-runner-backend` unset on Blackwell: FlashInfer MXFP4 (W4A8, official trtllm-gen SiTU kernels) is selected; H100/H200 pin Marlin. The B200 Balanced and High-Throughput cells pin `flashinfer_mxfp4` explicitly because that is the shape they were brought up on. **Attention backend.** Leave all three attention knobs unset on Blackwell: K3 resolves prefill, decode, and — under DSPARK — verification as a set (`trtllm_mla` across the board; `cutedsl_mla` takes decode and verification under DCP). On the non-DCP recipes, setting any one of the three cancels the auto-resolution for the others. The B200 Balanced and High-Throughput cells pin `--decode-attention-backend cutedsl_mla`, which is what auto-resolution picks for those DCP recipes anyway — it is written out because it is the shape they were brought up on, not because it changes the resolution. H100/H200 pin `flashmla` for decode. **Context length.** `--context-length` bounds the longest accepted request plus some context-scaled buffers; it does not size the KV pool. For long context the lever that adds capacity is `fp8_e4m3` KV. **DSPARK.** Adds `--speculative-algorithm DSPARK` plus the draft checkpoint on top of the showing strategy. Leave `--speculative-draft-attention-backend` unset. The published B300 DSPARK numbers pin the acceptance length with `SGLANG_SIMULATE_ACC_LEN`, so no measured acceptance rate exists for a real workload yet — measure against the same recipe running NOSPEC before adopting. **Per-platform notes:**

| Platform | Topology | Notes |
|----|----|----|
| B300 1×8 | TP8 (+DCP8) | accuracy-first defaults on Low-Latency and Balanced |
| GB300 2×4 | TP8/DCP8 | MNNVL transport and cuMem auto-detected |
| B200 2×8 | PP2 × TP8 on Low-Latency, PP2 × DCPEP8 on Balanced and High-Throughput. DSPARK re-lays the same 16 GPUs as TP16 / TP16+DCP16+EP16. PD prefill is TP1 × PP16 | Unified serves all three operating points; `Long-Context` is a `Prefill`-only strategy |
| GB200 4×4 | TP16/DCP16 | MNNVL auto-detected |
| H200 2×8 (4×8 on Unified High-Throughput) | TP16/EP16 + symm-mem, Marlin + FlashMLA; High-Throughput widens to TP32/EP32 over 4 nodes at mem-frac 0.90 with `extra_buffer_lazy` | same block on every node; export the cross-node NIC (`GLOO_SOCKET_IFNAME` / `NCCL_SOCKET_IFNAME`, `SGLANG_HOST_IP`); keep `NCCL_MNNVL_ENABLE=1 NCCL_CUMEM_ENABLE=1` |
| H100 4×8 | TP32/EP32, Marlin + FlashMLA | SM90a build of the K3 image; pin NCCL/Gloo to the same NIC on all nodes; least post-weight headroom (80 GB) |
| MI350X/MI355X 1×8 | TP8 ROCm/AITER | AITER A8W4 FlyDSL MoE, Triton attention (`SGLANG_MLA_DECODE_TUNE=1` for gfx950 MLA decode geometry), graph bs up to 256, fp8 kvcache; DSPARK supported. Activation-quant and fused-KDA-decode knobs: [AMD ROCm/AITER environment](#amd-env) |
| Atlas 800I A3 4×8 (32 cards / 64 dies) | TP64/DP4 + DeepEP | PD-mixed `Unified` only; DSPARK baked in; pin `GLOO`/`HCCL_SOCKET_IFNAME` on every node |

**DCP notes** — the DCP cells are Balanced and High-Throughput on every Blackwell platform, in both the `Unified` and `Decode` roles:

- DCP is the only axis that shards the TP-replicated MLA KV; Low-Latency skips it.
- Leave `--dcp-comm-backend` unset (fabric-resolved: `fi_a2a` on GB200/GB300, `a2a` on B200/B300).
- No `--enable-symm-mem` under DCP (force-disabled for decode-graph correctness).
- Explicit `tokenspeed_mla` force-rewrites `--kv-cache-dtype` to fp8; the default `cutedsl_mla` serves either dtype.
- Calculator ratios run well above 1 here (`r > 1` is legal): `bfloat16` state buys admission, `fp8` KV buys context.
- Don’t use EP with an a2a backend: a2a buffers reclaim the KV that DCP buys. Compose only to measure. a2a backend is set when `--moe-a2a-backend` is set.

Outside the two verified B300 1×8 `Unified` cells, no cell has a serving round in this exact shape — treat those as starting points to verify. **AMD ROCm/AITER environment (MI350X / MI355X).** The MI35x cell emits `SGLANG_USE_AITER=1 SGLANG_AITER_K3_OPT=1 AITER_FLYDSL_FORCE=1 AITER_SITUV2_A8W4=1` — the first three turn on the AITER ROCm path, its K3-specific fused kernels, and the FlyDSL MoE kernels; the rest of this table is what you can change on top. Everything here is gfx950/ROCm-only and inert elsewhere. These knobs first ship in the `20260903` daily ROCm image pinned above — on an older image they are simply unread — and the two SiTU rows also need an AITER revision at or past [ROCm/aiter#4534](https://github.com/ROCm/aiter/pull/4534) (FlyDSL 0.3.0).

| Env var | Default | Effect |
|----|----|----|
| `AITER_SITUV2_A8W4=1` | unset | SiTU v2 MoE with A8W4 activation quantization, on AITER’s GU-interleaved preshuffled weight layout. The performance default the cell ships. |
| `AITER_SITUV2_A4W4=1` | unset | A4W4 instead, on the generic separated shuffle layout. Numerically correct but slower than A8W4 (530.8 vs 537.3 tok/s median output on 8×MI35x). Setting **both** gives A8W4 precedence — SGLang follows AITER and keeps the GU-interleaved layout. |
| `SGLANG_K3_KDA_FUSED_BACKEND=aiter` | unset | Opt in to the fused ROCm KDA decode boundary: the `f_b` projection is deferred into the gfx950 FlyDSL kernel so decode fuses `f_b` + convolution + recurrent state update + gated RMSNorm. Any other value (or unset) keeps the unfused KDA path. |
| `SGLANG_K3_FLYDSL_SOURCE` | `auto` | Which FlyDSL implementation backs the fused decode: `auto` prefers SGLang’s vendored kernels and falls back to the AITER module, `sglang` / `aiter` pin one. Leave it alone unless you are bisecting the two. |

The fused KDA backend is fail-closed at two levels: it arms during model init only when the flag is exactly `aiter` **and** the gfx950 FlyDSL kernels are importable, and each decode step re-validates shapes, dtypes, strides, state indices, and output buffers before dispatch — anything unexpected falls back to the stock KDA implementation rather than erroring. Batch size 2 automatically picks a separately validated kernel schedule; every other batch keeps the original build options. Measured on a 69-layer graph the fused boundary is 9.20 → 8.38 µs/layer (−8.9%), with GSM8K 1319 at 0.950.

## 

[​](#3-advanced-usage)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

3. Advanced Usage

### 

[​](#3-1-reasoning)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

3.1 Reasoning

K3 always thinks; the `kimi_k3` reasoning parser (toggle **Reasoning Parser** in the **Parsers** card of the [Playground above](#playground)) separates that thinking from the final answer — thinking lands in `message.reasoning_content`, the answer in `message.content`. Control the reasoning depth with `reasoning_effort` (`low` / `high` / `max`; default `max`).

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTMgc2hyaW5rLTAgdGV4dC1ncmF5LTYwMCB0cmFuc2l0aW9uLXRyYW5zZm9ybSBkdXJhdGlvbi0yMDAgZGFyazp0ZXh0LWdyYXktNDAwIC1yb3RhdGUtOTAiPjxwYXRoIGQ9Ik0xNC4wMjM4IDQuMDAwMDJIMy45NzU3NkMzLjMzNzc2IDQuMDAwMDIgMi43NDk3NiA0LjM0NzAyIDIuNDQyNzYgNC45MDYwMkMyLjEzNTc2IDUuNDY1MDIgMi4xNTU3NiA2LjE0ODAyIDIuNDk3NzYgNi42ODcwMkw3LjUyMTc2IDE0LjYxQzcuODQ0NzYgMTUuMTE5IDguMzk2NzYgMTUuNDIyIDguOTk5NzYgMTUuNDIyQzkuNjAyNzYgMTUuNDIyIDEwLjE1NDggMTUuMTE4IDEwLjQ3NzggMTQuNjFMMTUuNTAyOCA2LjY4NjAyQzE1Ljg0MzggNi4xNDcwMiAxNS44NjQ4IDUuNDY0MDIgMTUuNTU3OCA0LjkwNTAyQzE1LjI1MDggNC4zNDYwMiAxNC42NjI4IDMuOTk5MDIgMTQuMDI0OCAzLjk5OTAyTDE0LjAyMzggNC4wMDAwMloiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48L3N2Zz4=)

Reasoning Example (Python)

Example

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
from openai import OpenAI

client = OpenAI(base_url="http://localhost:30000/v1", api_key="EMPTY")
resp = client.chat.completions.create(
    model="moonshotai/Kimi-K3",
    messages=[{"role": "user", "content": "What is 15% of 240?"}],
    reasoning_effort="high",  # "low" | "high" | "max" (default max)
)
msg = resp.choices[0].message
print("Reasoning:", getattr(msg, "reasoning_content", None))
print("Answer:", msg.content)
```

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTMgc2hyaW5rLTAgdGV4dC1ncmF5LTYwMCB0cmFuc2l0aW9uLXRyYW5zZm9ybSBkdXJhdGlvbi0yMDAgZGFyazp0ZXh0LWdyYXktNDAwIC1yb3RhdGUtOTAiPjxwYXRoIGQ9Ik0xNC4wMjM4IDQuMDAwMDJIMy45NzU3NkMzLjMzNzc2IDQuMDAwMDIgMi43NDk3NiA0LjM0NzAyIDIuNDQyNzYgNC45MDYwMkMyLjEzNTc2IDUuNDY1MDIgMi4xNTU3NiA2LjE0ODAyIDIuNDk3NzYgNi42ODcwMkw3LjUyMTc2IDE0LjYxQzcuODQ0NzYgMTUuMTE5IDguMzk2NzYgMTUuNDIyIDguOTk5NzYgMTUuNDIyQzkuNjAyNzYgMTUuNDIyIDEwLjE1NDggMTUuMTE4IDEwLjQ3NzggMTQuNjFMMTUuNTAyOCA2LjY4NjAyQzE1Ljg0MzggNi4xNDcwMiAxNS44NjQ4IDUuNDY0MDIgMTUuNTU3OCA0LjkwNTAyQzE1LjI1MDggNC4zNDYwMiAxNC42NjI4IDMuOTk5MDIgMTQuMDI0OCAzLjk5OTAyTDE0LjAyMzggNC4wMDAwMloiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48L3N2Zz4=)

Example Output

Output

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
Pending update...
```

### 

[​](#3-2-tool-calling)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

3.2 Tool Calling

Enable the `kimi_k3` tool-call parser (toggle **Tool Call Parser** in the **Parsers** card of the [Playground above](#playground)) to surface structured tool calls via `message.tool_calls`. Because K3 is a thinking model, the follow-up turn may put text in `reasoning_content` as well as `content` — print both. (Not yet supported on the Atlas 800I A3.)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTMgc2hyaW5rLTAgdGV4dC1ncmF5LTYwMCB0cmFuc2l0aW9uLXRyYW5zZm9ybSBkdXJhdGlvbi0yMDAgZGFyazp0ZXh0LWdyYXktNDAwIC1yb3RhdGUtOTAiPjxwYXRoIGQ9Ik0xNC4wMjM4IDQuMDAwMDJIMy45NzU3NkMzLjMzNzc2IDQuMDAwMDIgMi43NDk3NiA0LjM0NzAyIDIuNDQyNzYgNC45MDYwMkMyLjEzNTc2IDUuNDY1MDIgMi4xNTU3NiA2LjE0ODAyIDIuNDk3NzYgNi42ODcwMkw3LjUyMTc2IDE0LjYxQzcuODQ0NzYgMTUuMTE5IDguMzk2NzYgMTUuNDIyIDguOTk5NzYgMTUuNDIyQzkuNjAyNzYgMTUuNDIyIDEwLjE1NDggMTUuMTE4IDEwLjQ3NzggMTQuNjFMMTUuNTAyOCA2LjY4NjAyQzE1Ljg0MzggNi4xNDcwMiAxNS44NjQ4IDUuNDY0MDIgMTUuNTU3OCA0LjkwNTAyQzE1LjI1MDggNC4zNDYwMiAxNC42NjI4IDMuOTk5MDIgMTQuMDI0OCAzLjk5OTAyTDE0LjAyMzggNC4wMDAwMloiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48L3N2Zz4=)

Tool Calling Example (Python)

Example

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
from openai import OpenAI

client = OpenAI(base_url="http://localhost:30000/v1", api_key="EMPTY")
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
}]
resp = client.chat.completions.create(
    model="moonshotai/Kimi-K3",
    messages=[{"role": "user", "content": "What's the weather in Beijing?"}],
    tools=tools,
)
msg = resp.choices[0].message
print("Reasoning:", getattr(msg, "reasoning_content", None))
print("Tool calls:", msg.tool_calls)
```

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTMgc2hyaW5rLTAgdGV4dC1ncmF5LTYwMCB0cmFuc2l0aW9uLXRyYW5zZm9ybSBkdXJhdGlvbi0yMDAgZGFyazp0ZXh0LWdyYXktNDAwIC1yb3RhdGUtOTAiPjxwYXRoIGQ9Ik0xNC4wMjM4IDQuMDAwMDJIMy45NzU3NkMzLjMzNzc2IDQuMDAwMDIgMi43NDk3NiA0LjM0NzAyIDIuNDQyNzYgNC45MDYwMkMyLjEzNTc2IDUuNDY1MDIgMi4xNTU3NiA2LjE0ODAyIDIuNDk3NzYgNi42ODcwMkw3LjUyMTc2IDE0LjYxQzcuODQ0NzYgMTUuMTE5IDguMzk2NzYgMTUuNDIyIDguOTk5NzYgMTUuNDIyQzkuNjAyNzYgMTUuNDIyIDEwLjE1NDggMTUuMTE4IDEwLjQ3NzggMTQuNjFMMTUuNTAyOCA2LjY4NjAyQzE1Ljg0MzggNi4xNDcwMiAxNS44NjQ4IDUuNDY0MDIgMTUuNTU3OCA0LjkwNTAyQzE1LjI1MDggNC4zNDYwMiAxNC42NjI4IDMuOTk5MDIgMTQuMDI0OCAzLjk5OTAyTDE0LjAyMzggNC4wMDAwMloiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48L3N2Zz4=)

Example Output

Output

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
Pending update...
```

### 

[​](#3-3-hicache-hierarchical-kv-caching)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

3.3 HiCache (Hierarchical KV Caching)

K3’s hybrid HiCache tiers the paged MLA KV **and** the KDA/mamba state across L1 (GPU) / L2 (host) / L3 (Mooncake) — enable it from the **HiCache** card in the [Playground above](#playground) for long multi-turn workloads.

- On the DCP recipes (Blackwell Balanced / High-Throughput, in both the `Unified` and `Decode` roles), the host tiers are not fully DCP-aware yet: **L3 always, and L1+L2 with Spec Decode on, drop the DCP flags** (the command hints call it out — per-request KV capacity shrinks accordingly). L1+L2 with Spec Decode off keeps DCP. Only DCP goes: the MLA KV reverts to TP-replicated, but the cell’s other parallelism stays, so B300/GB300/GB200 land on plain TP while B200 Unified keeps its `--pp-size 2` / `--ep-size`.
- Low-Latency and the Hopper recipes take all tiers unchanged.

### 

[​](#3-4-pd-disaggregation)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

3.4 PD Disaggregation

PD splits prefill and decode into separate server groups; because K3 is hybrid, the transfer moves **both** the paged MLA KV and the KDA recurrent state.

- **Transfer**: the cells emit **NiXL** (RDMA); Mooncake stays selectable in the Playground.
- **Ports**: prefill `30000`, decode `30100` (derived ZMQ/dist ranges must not collide on a shared host). The positional `8998` after `--prefill` must match `--disaggregation-bootstrap-port`, or only the decode worker registers.
- **Decode state pool**: chunk cache — one slot per request; `--mamba-radix-cache-strategy` is inert. Keep `--disaggregation-decode-extra-slots` pinned: unpinned it defaults to twice the batch below 32 requests and **zero** above.

#### 

[​](#deep-pp-for-prefill)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Deep PP for prefill

Deep PP is `--tp-size 1` with one pipeline stage per GPU — `--pp-size 8` on B300/GB300, `--pp-size 16` on B200/GB200. Pipeline P2P overlaps the next microbatch’s compute, unlike TP/EP collectives, and each stage owns whole layers (a clean slice of KV and state). `--tp-size 1` is also what buys context: above TP1 the MLA KV is replicated across the TP ranks, so TP2 × PP8 holds roughly half the tokens of TP1 × PP16 for the same memory.

- Use one stage per GPU; a shallow split still pays the in-stage all-reduce and can lose to flat TP.
- Pays only with several requests in flight. On the 8-GPU platforms that is why `Default` stays TP8; on the 16-GPU platforms deep PP wins at the Default operating point too, so both strategies use it — measured on GB200 at ISL 8192 / concurrency 32, PP16 × TP1 reached 4550 prefill tok/s/GPU vs 3596 (PP8 × TP2), 2407 (TEP16), and 1652 (TP16). Below concurrency ~8 the pipeline cannot fill and TEP16 leads instead (1947 vs 1227) — use `--tp-size 16 --ep-size 16` there.
- DSPARK off (`pp_size == 1` required) — on B200/GB200 that applies to `Default` as well.
- Fan one prefill role out to several decode roles; budget for in-transfer KV on the decode side.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTMgc2hyaW5rLTAgdGV4dC1ncmF5LTYwMCB0cmFuc2l0aW9uLXRyYW5zZm9ybSBkdXJhdGlvbi0yMDAgZGFyazp0ZXh0LWdyYXktNDAwIC1yb3RhdGUtOTAiPjxwYXRoIGQ9Ik0xNC4wMjM4IDQuMDAwMDJIMy45NzU3NkMzLjMzNzc2IDQuMDAwMDIgMi43NDk3NiA0LjM0NzAyIDIuNDQyNzYgNC45MDYwMkMyLjEzNTc2IDUuNDY1MDIgMi4xNTU3NiA2LjE0ODAyIDIuNDk3NzYgNi42ODcwMkw3LjUyMTc2IDE0LjYxQzcuODQ0NzYgMTUuMTE5IDguMzk2NzYgMTUuNDIyIDguOTk5NzYgMTUuNDIyQzkuNjAyNzYgMTUuNDIyIDEwLjE1NDggMTUuMTE4IDEwLjQ3NzggMTQuNjFMMTUuNTAyOCA2LjY4NjAyQzE1Ljg0MzggNi4xNDcwMiAxNS44NjQ4IDUuNDY0MDIgMTUuNTU3OCA0LjkwNTAyQzE1LjI1MDggNC4zNDYwMiAxNC42NjI4IDMuOTk5MDIgMTQuMDI0OCAzLjk5OTAyTDE0LjAyMzggNC4wMDAwMloiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48L3N2Zz4=)

Router

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
python3 -m sglang_router.launch_router \
  --pd-disaggregation \
  --prefill http://<prefill-host>:30000 8998 \
  --decode http://<decode-host>:30100 \
  --host 0.0.0.0 --port 8000 \
  --disable-circuit-breaker \
  --health-check-interval-secs 999999
```

Clients then send requests to the router (`:8000`) instead of an individual role server.

### 

[​](#3-5-vlm-serving-profiles)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

3.5 VLM Serving Profiles

The open-source K3 serving contract currently supports **image input only** — its processor rejects video and audio input.

#### 

[​](#vlm-feature-transport)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

VLM feature transport

Use **VLM Transport** in the command picker. `Auto` is a topology-aware starting point, not a claim that one configuration is fastest for every workload.

| Picker selection | Processor-to-scheduler feature path |
|----|----|
| Auto · single-node Unified CUDA | CUDA IPC |
| Auto · Unified GB200/GB300 | CUDA VMM when IMEX is available; CPU otherwise |
| Auto · PD or other topologies | CPU |
| CPU | CPU, with no GPU feature pool |

CUDA IPC and CUDA VMM reserve up to `SGLANG_MM_FEATURE_CACHE_MB` (1 GiB by default) on the base GPU and fall back to CPU per tensor when full. This setting does not control EPD encoder output or PD KV/KDA transfer. K3 already defaults to 2 processor workers and 16 I/O workers; leave those flags unset unless tuning.

#### 

[​](#vlm-compatibility)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

VLM compatibility

| Feature | K3 behavior |
|----|----|
| PD | Supported. Image processing and ViT run on prefill; the PD transfer then moves both paged MLA KV and KDA recurrent state as described in [PD disaggregation](#pd-disaggregation). |
| EPD | Supported on the public `kimi-k3` branch. Use an `--encoder-only` vision role and a `--language-only` prefill role; add the normal decode role for full EPD. See the [EPD guide](/docs/advanced_features/epd_disaggregation). |
| MM encoder DP | Built in. K3 shards complete images across TP ranks, so leave `--mm-enable-dp-encoder` unset in unified, PD-prefill, and encoder-only roles. |
| MM feature transport | Processor-to-scheduler features only. EPD encoder output and PD KV/KDA transfer use their own backends. |
| ViT BCG | Compatible with unified and encoder-only roles, but recommended only for repeated encoder shapes after measuring the HBM trade-off below. |

#### 

[​](#should-vit-bcg-be-enabled)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Should ViT BCG be enabled?

Keep ViT BCG **off** for general serving; enable `SGLANG_VIT_ENABLE_CUDA_GRAPH=1` only for ViT-only / EPD encoder workloads with recurring image shapes and spare HBM.

- The win is confined to the encoder — no reliable end-to-end TTFT/TPOT gain in full-model serving.
- Each captured graph retains HBM (graph + per-entry metadata); measure on your own shapes.
- The default cache captures after two hits and falls back to eager above 6,144 tokens; do not enlarge it without measuring.

#### 

[​](#low-hbm-vlm)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

Low-HBM VLM

Use this profile when keeping HBM headroom matters more than peak concurrency. It removes the GPU feature pool, keeps ViT BCG disabled, halves the context window, caps concurrency, and lowers the static-memory target:

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
sglang serve \
  --trust-remote-code \
  --model-path moonshotai/Kimi-K3 \
  --tp-size 8 \
  --context-length 65536 \
  --enable-symm-mem \
  --mem-fraction-static 0.82 \
  --mm-feature-transport cpu \
  --reasoning-parser kimi_k3 \
  --tool-call-parser kimi_k3 \
  --host 0.0.0.0 \
  --port 30000
```

`--mem-fraction-static 0.82` is a conservative B300 starting point, not a portable minimum: raise it toward `0.85` if startup reports insufficient memory; if HBM must go back to other workloads, reduce context/concurrency first. The precision levers (`fp8_e4m3` KV, `bfloat16` SSM state) save far more but stay accuracy-gated.

### 

[​](#3-6-large-scale-serving-presets-16–64-gpus-blackwell)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0zIHNocmluay0wIj48cGF0aCBkPSJNOC41MDAwMSA2LjgyN0M4LjE0ODAxIDYuOTk1IDcuODE4MDEgNy4yMjUgNy41MjcwMSA3LjUxN0w3LjUxNzAxIDcuNTI3QzYuMTM2MDEgOC45MDggNi4xMzYwMSAxMS4xNDYgNy41MTcwMSAxMi41MjdMOS42OTIwMSAxNC43MDJDMTEuMDczIDE2LjA4MyAxMy4zMTEgMTYuMDgzIDE0LjY5MiAxNC43MDJMMTQuNzAyIDE0LjY5MkMxNi4wODMgMTMuMzExIDE2LjA4MyAxMS4wNzMgMTQuNzAyIDkuNjkyTDEzLjc3MSA4Ljc2MSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTkuNTAwMDIgMTEuMTczQzkuODUyMDIgMTEuMDA1IDEwLjE4MiAxMC43NzUgMTAuNDczIDEwLjQ4M0wxMC40ODMgMTAuNDczQzExLjg2NCA5LjA5MiAxMS44NjQgNi44NTQgMTAuNDgzIDUuNDczTDguMzA4MDIgMy4yOThDNi45MjcwMiAxLjkxNyA0LjY4OTAyIDEuOTE3IDMuMzA4MDIgMy4yOThMMy4yOTgwMiAzLjMwOEMxLjkxNzAyIDQuNjg5IDEuOTE3MDIgNi45MjcgMy4yOTgwMiA4LjMwOEw0LjIyOTAyIDkuMjM5IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

3.6 Large-Scale Serving Presets (16–64 GPUs, Blackwell)

**The KDA state pool is the concurrency ceiling** — DP, EP, and DCP do not shard it; only attention-TP width, SSM dtype, and cache strategy change the per-GPU bill. The MLA KV is cheap to shrink (fp8) or deduplicate (DCP). Two presets come out of this, at `N = 8k` GPUs:

| Preset | What it trades | Pick it for |
|----|----|----|
| **Peak Throughput** — `dp = k`, attention-TP 8 | State shards 8-way. The per-step KDA all-reduce stays within one 8-GPU B200/B300 node, or spans two 4-GPU GB200/GB300 nodes over MNNVL. `--kv-cache-dtype fp8_e4m3` is load-bearing — bf16 KV does not fit 128 requests per replica. | Maximum sustained TPS — the default large-scale shape. |
| **Peak Capacity (+DCP8)** — `dp = k` + `--dcp-size 8` | Deduplicates the attention-TP group’s MLA KV: concurrency ceiling +72% at the same engine throughput, ~1.8× ITL. | Context ≥ ~16K, or per-replica concurrency past 128. |

- **Radix cache** is independent of the preset: for prefix-free traffic (offline batch, evals) switch it off (Playground’s **Prefix Cache** card) — one state slot per request instead of 4–5.
- The fully data-parallel extreme (`--dp-size` = GPU count, attention-TP 1) — the shape behind the 64-GPU sweep’s ~3K tok/s per GPU — is not a preset: 288 GB GPUs only, radix forced off, no head-to-head against the preset shape.

The Peak Throughput preset at 32 GPUs on B200/B300 (4 nodes × 8; every node runs the same command with its own `--node-rank`). On GB200/GB300 the same 32-GPU shape uses 8 nodes × 4, and the Playground emits `--nnodes 8`:

Command

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9jb3B5LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2NvcHktYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik0xNC4yNSA1LjI1SDcuMjVDNi4xNDU0MyA1LjI1IDUuMjUgNi4xNDU0MyA1LjI1IDcuMjVWMTQuMjVDNS4yNSAxNS4zNTQ2IDYuMTQ1NDMgMTYuMjUgNy4yNSAxNi4yNUgxNC4yNUMxNS4zNTQ2IDE2LjI1IDE2LjI1IDE1LjM1NDYgMTYuMjUgMTQuMjVWNy4yNUMxNi4yNSA2LjE0NTQzIDE1LjM1NDYgNS4yNSAxNC4yNSA1LjI1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTIuODAxMDMgMTEuOTk4TDEuNzcyMDMgNS4wNzM5N0MxLjYxMDAzIDMuOTgwOTcgMi4zNjQwMyAyLjk2Mzk3IDMuNDU2MDMgMi44MDE5N0wxMC4zOCAxLjc3Mjk3QzExLjMxMyAxLjYzMzk3IDEyLjE5IDIuMTYyOTcgMTIuNTI4IDMuMDAwOTciIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBncm91cC1ob3Zlci9hc2stYXNzaXN0YW50LWJ1dHRvbjp0ZXh0LWdyYXktNTAwIGRhcms6dGV4dC13aGl0ZS80MCBkYXJrOmdyb3VwLWhvdmVyL2Fzay1hc3Npc3RhbnQtYnV0dG9uOnRleHQtd2hpdGUvNjAiPjxwYXRoIGQ9Ik01LjY1Nzk5IDIuOTlMNC4zOTQ5OSAyLjU2OUwzLjk3Mzk5IDEuMzA2QzMuODM2OTkgMC44OTggMy4xNjE5OSAwLjg5OCAzLjAyNDk5IDEuMzA2TDIuNjAzOTkgMi41NjlMMS4zNDA5OSAyLjk5QzEuMTM2OTkgMy4wNTggMC45OTg5OTMgMy4yNDkgMC45OTg5OTMgMy40NjRDMC45OTg5OTMgMy42NzkgMS4xMzY5OSAzLjg3IDEuMzQwOTkgMy45MzhMMi42MDM5OSA0LjM1OUwzLjAyNDk5IDUuNjIyQzMuMDkyOTkgNS44MjYgMy4yODQ5OSA1Ljk2NCAzLjQ5OTk5IDUuOTY0QzMuNzE0OTkgNS45NjQgMy45MDU5OSA1LjgyNiAzLjk3NDk5IDUuNjIyTDQuMzk1OTkgNC4zNTlMNS42NTg5OSAzLjkzOEM1Ljg2Mjk5IDMuODcgNi4wMDA5OSAzLjY3OSA2LjAwMDk5IDMuNDY0QzYuMDAwOTkgMy4yNDkgNS44NjE5OSAzLjA1OCA1LjY1Nzk5IDIuOTlaIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZT0ibm9uZSIgLz48cGF0aCBkPSJNOS41IDIuNzVMMTEuNDEyIDcuNTg3TDE2LjI1IDkuNUwxMS40MTIgMTEuNDEzTDkuNSAxNi4yNUw3LjU4NyAxMS40MTNMMi43NSA5LjVMNy41ODcgNy41ODdMOS41IDIuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)

``` shiki
SGLANG_OPT_DEEPGEMM_MEGA_MOE_NUM_MAX_TOKENS_PER_RANK=20480 \
sglang serve \
  --trust-remote-code \
  --model-path moonshotai/Kimi-K3 \
  --tp-size 32 --ep-size 32 \
  --enable-dp-attention --dp-size 4 --enable-dp-lm-head \
  --nnodes 4 --node-rank <rank> --dist-init-addr <node0-ip>:20000 \
  --moe-a2a-backend megamoe --moe-runner-backend deep_gemm \
  --kv-cache-dtype fp8_e4m3 \
  --mamba-ssm-dtype bfloat16 \
  --mamba-radix-cache-strategy extra_buffer_lazy \
  --mem-fraction-static 0.92 \
  --reasoning-parser kimi_k3 --tool-call-parser kimi_k3 \
  --host 0.0.0.0 --port 30000
```

Scale by holding the per-replica shape fixed and moving only the replica count; pool sizing rides the calculator-driven `--mamba-full-memory-ratio`, which folds in DP, DCP, precision, and speculation:

| GPUs | B200/B300 nodes | GB200/GB300 nodes | `--tp-size` / `--ep-size` | `--dp-size` |
|------|-----------------|-------------------|---------------------------|-------------|
| 16   | 2×8             | 4×4               | 16                        | 2           |
| 32   | 4×8             | 8×4               | 32                        | 4           |
| 64   | 8×8             | 16×4              | 64                        | 8           |

For Peak Capacity, add `--dcp-size 8` and re-derive the pool split with the [Mamba ratio calculator](#mamba-ratio-calculator). Both presets are one click away in the [Playground above](#playground): pick a **Cluster Size** and a **Large-Scale Preset** and the full command composes onto whichever cell is showing. Decisions the preset already makes:

- **MegaMoE + `deep_gemm`** — the fused DeepGEMM all-to-all/MoE path used by these large-scale DP/EP throughput presets, with K3’s SiTU activation.
- **SP-MoE and shared-expert overlap** engage automatically under EP a2a; the K3 all-reduce fusion does not.
- **Spec Decode follows the Deploy knob.** Acceptance thins at large batch; spec × EP × DP-attention is validated only at 8-GPU EP8 × DP2 (full GSM8K) — experimental at these scales.

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgdGV4dC1ibHVlLTgwMCBkYXJrOnRleHQtYmx1ZS0zMDAiPjxwYXRoIGQ9Ik0gOSAxLjY3MTQgQyAxMy4wMzcxIDEuNjcxNCAxNi4zMjg2IDQuOTYyOSAxNi4zMjg2IDkgQyAxNi4zMjg2IDEzLjAzNzEgMTMuMDM3MSAxNi4zMjg2IDkgMTYuMzI4NiBDIDcuMDU3NCAxNi4zMjUyIDUuMTk1MyAxNS41NTIgMy44MjE3IDE0LjE3ODMgQyAyLjQ0OCAxMi44MDQ3IDEuNjc0OCAxMC45NDI2IDEuNjcxNCA5IEMgMS42NzE0IDQuOTYyOSA0Ljk2MjkgMS42NzE0IDkgMS42NzE0IFogTSA5IDAgQyA0LjAzNzEgMCAwIDQuMDM3MSAwIDkgQyAwIDEzLjk2MjkgNC4wMzcxIDE4IDkgMTggQyAxMy45NjI5IDE4IDE4IDEzLjk2MjkgMTggOSBDIDE4IDQuMDM3MSAxMy45NjI5IDAgOSAwIFogTSAxMC4yODU3IDMuODU3MSBIIDcuNzE0MyBWIDEwLjI4NTcgSCAxMC4yODU3IFYgMy44NTcxIFogTSAxMC4yODU3IDExLjU3MTQgSCA3LjcxNDMgViAxNC4xNDI5IEggMTAuMjg1NyBWIDExLjU3MTQgWiIgZmlsbD0iY3VycmVudENvbG9yIiBzdHJva2U9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiAvPjwvc3ZnPg==)

No preset has a full serving round on final weights; the constants derive from measured single- and dual-node rounds plus a 64-GPU sweep. Validate throughput and accuracy on your workload before committing a fleet.

Was this page helpful?

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1jdXJyZW50Ij48cGF0aCBkPSJNNS4yNSA3LjQ5NEM1LjI1IDcuMDE0IDUuNDIzIDYuNTUgNS43MzYgNi4xODdMMTAgMS4yNUMxMC44NTQgMS42NzcgMTEuMjUgMi42NzggMTAuOTIgMy41NzRMOS43NSA2Ljc1SDE0LjE1MkMxNS40NjUgNi43NSAxNi40MjEgNy45OTMgMTYuMDg1IDkuMjYyTDE0Ljg5NCAxMy43NjJDMTQuNjYyIDE0LjYzOSAxMy44NjggMTUuMjUgMTIuOTYxIDE1LjI1SDcuMjVDNi4xNDUgMTUuMjUgNS4yNSAxNC4zNTUgNS4yNSAxMy4yNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PHBhdGggZD0iTTQuMjUgNi43NUgyLjc1QzIuMTk3NzIgNi43NSAxLjc1IDcuMTk3NzIgMS43NSA3Ljc1VjE0LjI1QzEuNzUgMTQuODAyMyAyLjE5NzcyIDE1LjI1IDIuNzUgMTUuMjVINC4yNUM0LjgwMjI4IDE1LjI1IDUuMjUgMTQuODAyMyA1LjI1IDE0LjI1VjcuNzVDNS4yNSA3LjE5NzcyIDQuODAyMjggNi43NSA0LjI1IDYuNzVaIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)Yes

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIxLjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgYXJpYS1oaWRkZW49InRydWUiIGNsYXNzPSJzaXplLTQgc2hyaW5rLTAgdGV4dC1jdXJyZW50Ij48cGF0aCBkPSJNNS4yNSAxMC41MDZDNS4yNSAxMC45ODYgNS40MjMgMTEuNDUgNS43MzYgMTEuODEzTDEwIDE2Ljc1QzEwLjg1NCAxNi4zMjMgMTEuMjUgMTUuMzIyIDEwLjkyIDE0LjQyNkw5Ljc1IDExLjI1SDE0LjE1MkMxNS40NjUgMTEuMjUgMTYuNDIxIDEwLjAwNyAxNi4wODUgOC43MzhMMTQuODk0IDQuMjM4QzE0LjY2MiAzLjM2MSAxMy44NjggMi43NSAxMi45NjEgMi43NUg3LjI1QzYuMTQ1IDIuNzUgNS4yNSAzLjY0NSA1LjI1IDQuNzUiIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjxwYXRoIGQ9Ik00LjI1IDIuNzVIMi43NUMyLjE5NzcyIDIuNzUgMS43NSAzLjE5NzcyIDEuNzUgMy43NVYxMC4yNUMxLjc1IDEwLjgwMjMgMi4xOTc3MiAxMS4yNSAyLjc1IDExLjI1SDQuMjVDNC44MDIyOCAxMS4yNSA1LjI1IDEwLjgwMjMgNS4yNSAxMC4yNVYzLjc1QzUuMjUgMy4xOTc3MiA0LjgwMjI4IDIuNzUgNC4yNSAyLjc1WiIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PC9zdmc+)No

[](/cookbook/autoregressive/IFM/K2-Horizon)

K2 Horizon

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0yLjUgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBkYXJrOnRleHQtZ3JheS02MDAgZ3JvdXAtaG92ZXI6dGV4dC1ncmF5LTUwMCBkYXJrOmdyb3VwLWhvdmVyOnRleHQtZ3JheS01MDAiIGRhdGEtY29tcG9uZW50LXBhcnQ9InBhZ2luYXRpb24tY2hldnJvbiI+PHBhdGggZD0iTTExLjUgMTUuMjVMNS4yNSA5TDExLjUgMi43NSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHdpZHRoPSIxLjUiIGxpbmVjYXA9InJvdW5kIiBsaW5lam9pbj0icm91bmQiIC8+PC9zdmc+)Previous

[](/cookbook/autoregressive/Moonshotai/Kimi-K2.7-Code)

Kimi-K2.7-Code

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0yLjUgc2hyaW5rLTAgdGV4dC1ncmF5LTQwMCBkYXJrOnRleHQtZ3JheS02MDAgZ3JvdXAtaG92ZXI6dGV4dC1ncmF5LTUwMCBkYXJrOmdyb3VwLWhvdmVyOnRleHQtZ3JheS01MDAiIGRhdGEtY29tcG9uZW50LXBhcnQ9InBhZ2luYXRpb24tY2hldnJvbiI+PHBhdGggZD0iTTYuNSAyLjc1TDEyLjc1IDlMNi41IDE1LjI1IiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48L3N2Zz4=)Next

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxOCIgaGVpZ2h0PSIxOCIgdmlld2JveD0iMCAwIDE4IDE4IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0ic2l6ZS0yLjUgc2hyaW5rLTAgdGV4dC13aGl0ZSBkYXJrOnRleHQtd2hpdGUiPjxwYXRoIGQ9Ik05LjAgMS41NzU0TDguOTk5OSAxNi40MTcxIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgd2lkdGg9IjEuNSIgbGluZWNhcD0icm91bmQiIGxpbmVqb2luPSJyb3VuZCIgLz48cGF0aCBkPSJNMi4yNTYzIDguMzE5TDguOTk5OSAxLjU3NTRMMTUuNzQzNSA4LjMxOTEiIHN0cm9rZT0iY3VycmVudENvbG9yIiB3aWR0aD0iMS41IiBsaW5lY2FwPSJyb3VuZCIgbGluZWpvaW49InJvdW5kIiAvPjwvc3ZnPg==)

[github![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZm9yY2VkLWNvbG9yczpmb3JjZWQtY29sb3ItYWRqdXN0LW5vbmUgZm9yY2VkLWNvbG9yczpiZy1bY29sb3I6Q2FudmFzVGV4dF0hIHctNSBoLTUgYmctZ3JheS00MDAgZGFyazpiZy1ncmF5LTUwMCBob3ZlcjpiZy1ncmF5LTUwMCBkYXJrOmhvdmVyOmJnLWdyYXktNDAwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgc3R5bGU9Ii13ZWJraXQtbWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL2dpdGh1Yi5zdmcmcXVvdDspOy13ZWJraXQtbWFzay1yZXBlYXQ6bm8tcmVwZWF0Oy13ZWJraXQtbWFzay1wb3NpdGlvbjpjZW50ZXI7bWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL2dpdGh1Yi5zdmcmcXVvdDspO21hc2stcmVwZWF0Om5vLXJlcGVhdDttYXNrLXBvc2l0aW9uOmNlbnRlciI+PC9zdmc+)](https://github.com/sgl-project/sglang)[x![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZm9yY2VkLWNvbG9yczpmb3JjZWQtY29sb3ItYWRqdXN0LW5vbmUgZm9yY2VkLWNvbG9yczpiZy1bY29sb3I6Q2FudmFzVGV4dF0hIHctNSBoLTUgYmctZ3JheS00MDAgZGFyazpiZy1ncmF5LTUwMCBob3ZlcjpiZy1ncmF5LTUwMCBkYXJrOmhvdmVyOmJnLWdyYXktNDAwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgc3R5bGU9Ii13ZWJraXQtbWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL3gtdHdpdHRlci5zdmcmcXVvdDspOy13ZWJraXQtbWFzay1yZXBlYXQ6bm8tcmVwZWF0Oy13ZWJraXQtbWFzay1wb3NpdGlvbjpjZW50ZXI7bWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL3gtdHdpdHRlci5zdmcmcXVvdDspO21hc2stcmVwZWF0Om5vLXJlcGVhdDttYXNrLXBvc2l0aW9uOmNlbnRlciI+PC9zdmc+)](https://x.com/lmsysorg)[linkedin![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZm9yY2VkLWNvbG9yczpmb3JjZWQtY29sb3ItYWRqdXN0LW5vbmUgZm9yY2VkLWNvbG9yczpiZy1bY29sb3I6Q2FudmFzVGV4dF0hIHctNSBoLTUgYmctZ3JheS00MDAgZGFyazpiZy1ncmF5LTUwMCBob3ZlcjpiZy1ncmF5LTUwMCBkYXJrOmhvdmVyOmJnLWdyYXktNDAwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgc3R5bGU9Ii13ZWJraXQtbWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL2xpbmtlZGluLnN2ZyZxdW90Oyk7LXdlYmtpdC1tYXNrLXJlcGVhdDpuby1yZXBlYXQ7LXdlYmtpdC1tYXNrLXBvc2l0aW9uOmNlbnRlcjttYXNrLWltYWdlOnVybCgmcXVvdDtodHRwczovL2QzZ2syYzV4aW0xamUyLmNsb3VkZnJvbnQubmV0L2ZvbnRhd2Vzb21lL3Y3LjIuMC9icmFuZHMvbGlua2VkaW4uc3ZnJnF1b3Q7KTttYXNrLXJlcGVhdDpuby1yZXBlYXQ7bWFzay1wb3NpdGlvbjpjZW50ZXIiPjwvc3ZnPg==)](https://www.linkedin.com/company/sgl-project/posts?feedView=all)[slack![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZm9yY2VkLWNvbG9yczpmb3JjZWQtY29sb3ItYWRqdXN0LW5vbmUgZm9yY2VkLWNvbG9yczpiZy1bY29sb3I6Q2FudmFzVGV4dF0hIHctNSBoLTUgYmctZ3JheS00MDAgZGFyazpiZy1ncmF5LTUwMCBob3ZlcjpiZy1ncmF5LTUwMCBkYXJrOmhvdmVyOmJnLWdyYXktNDAwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgc3R5bGU9Ii13ZWJraXQtbWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL3NsYWNrLnN2ZyZxdW90Oyk7LXdlYmtpdC1tYXNrLXJlcGVhdDpuby1yZXBlYXQ7LXdlYmtpdC1tYXNrLXBvc2l0aW9uOmNlbnRlcjttYXNrLWltYWdlOnVybCgmcXVvdDtodHRwczovL2QzZ2syYzV4aW0xamUyLmNsb3VkZnJvbnQubmV0L2ZvbnRhd2Vzb21lL3Y3LjIuMC9icmFuZHMvc2xhY2suc3ZnJnF1b3Q7KTttYXNrLXJlcGVhdDpuby1yZXBlYXQ7bWFzay1wb3NpdGlvbjpjZW50ZXIiPjwvc3ZnPg==)](https://slack.sglang.io/)[discord![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZm9yY2VkLWNvbG9yczpmb3JjZWQtY29sb3ItYWRqdXN0LW5vbmUgZm9yY2VkLWNvbG9yczpiZy1bY29sb3I6Q2FudmFzVGV4dF0hIHctNSBoLTUgYmctZ3JheS00MDAgZGFyazpiZy1ncmF5LTUwMCBob3ZlcjpiZy1ncmF5LTUwMCBkYXJrOmhvdmVyOmJnLWdyYXktNDAwIiBhcmlhLWhpZGRlbj0idHJ1ZSIgZm9jdXNhYmxlPSJmYWxzZSIgc3R5bGU9Ii13ZWJraXQtbWFzay1pbWFnZTp1cmwoJnF1b3Q7aHR0cHM6Ly9kM2drMmM1eGltMWplMi5jbG91ZGZyb250Lm5ldC9mb250YXdlc29tZS92Ny4yLjAvYnJhbmRzL2Rpc2NvcmQuc3ZnJnF1b3Q7KTstd2Via2l0LW1hc2stcmVwZWF0Om5vLXJlcGVhdDstd2Via2l0LW1hc2stcG9zaXRpb246Y2VudGVyO21hc2staW1hZ2U6dXJsKCZxdW90O2h0dHBzOi8vZDNnazJjNXhpbTFqZTIuY2xvdWRmcm9udC5uZXQvZm9udGF3ZXNvbWUvdjcuMi4wL2JyYW5kcy9kaXNjb3JkLnN2ZyZxdW90Oyk7bWFzay1yZXBlYXQ6bm8tcmVwZWF0O21hc2stcG9zaXRpb246Y2VudGVyIj48L3N2Zz4=)](https://discord.gg/4ugb2t6YY2)

[Powered by![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTI3NCIgaGVpZ2h0PSIzNjciIHZpZXdib3g9IjAgMCAxMjc0IDM2NyIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiBjbGFzcz0iaC0zLjUgdy1hdXRvIHRyYW5zbGF0ZS15LTAuNzUiPjxwYXRoIGQ9Ik0xMTU0LjM4IDM2Ni4wMzhIMTA5Ny44NkwxMTM3LjY5IDI3Ni4xNEwxMDU4LjA0IDk3LjEwNDZIMTExNC45M0wxMTYxLjM1IDIwOS4zMzdDMTE2Mi45NyAyMTMuMjYgMTE2OC41MyAyMTMuMjUzIDExNzAuMTQgMjA5LjMyNUwxMjE2LjIxIDk3LjEwNDZIMTI3My40OUwxMTU0LjM4IDM2Ni4wMzhaIiBmaWxsPSJjdXJyZW50Q29sb3IiIC8+PHBhdGggZD0iTTk4Mi43MTQgMjg2Ljc2MVYxNDIuNjIySDk0NC40MDNWOTcuMTA0MUg5ODIuNzE0VjcyLjQ0ODhDOTgyLjcxNCA0OS45NDI5IDk4OS41NDIgMzIuMjQxNiAxMDAzLjIgMTkuMzQ1QzEwMTYuODUgNi40NDgzMiAxMDM0LjE3IDAgMTA1NS4xNiAwQzEwNjguMDYgMCAxMDc5LjA2IDEuMzkwODEgMTA4OC4xNiA0LjE3MjQ0VjUwLjA2OTNDMTA4Mi4wOSA0Ny43OTM0IDEwNzUuMDEgNDYuNjU1NSAxMDY2LjkyIDQ2LjY1NTVDMTA1NS41NCA0Ni42NTU1IDEwNDcuMzIgNDkuMTg0MyAxMDQyLjI3IDU0LjI0MThDMTAzNy4yMSA1OS4wNDY0IDEwMzQuNjggNjcuMjY0OCAxMDM0LjY4IDc4Ljg5NzFWOTcuMTA0MUgxMDg4LjE2VjE0Mi42MjJIMTAzNC42OFYyODYuNzYxSDk4Mi43MTRaIiBmaWxsPSJjdXJyZW50Q29sb3IiIC8+PHBhdGggZD0iTTg5Ny45MTYgNjYuMDAwNUM4ODkuMDY2IDY2LjAwMDUgODgxLjM1MyA2Mi44Mzk1IDg3NC43NzggNTYuNTE3NkM4NjguMjAzIDQ5Ljk0MjkgODY0LjkxNiA0Mi4xMDM3IDg2NC45MTYgMzMuMDAwMkM4NjQuOTE2IDIzLjg5NjcgODY4LjIwMyAxNi4xODQgODc0Ljc3OCA5Ljg2MjE1Qzg4MS4zNTMgMy4yODczOCA4ODkuMDY2IDAgODk3LjkxNiAwQzkwNy4yNzMgMCA5MTUuMTEyIDMuMjg3MzggOTIxLjQzNCA5Ljg2MjE1QzkyOC4wMDggMTYuMTg0IDkzMS4yOTYgMjMuODk2NyA5MzEuMjk2IDMzLjAwMDJDOTMxLjI5NiA0Mi4xMDM3IDkyOC4wMDggNDkuOTQyOSA5MjEuNDM0IDU2LjUxNzZDOTE1LjExMiA2Mi44Mzk1IDkwNy4yNzMgNjYuMDAwNSA4OTcuOTE2IDY2LjAwMDVaTTg3Mi4xMjMgMjg2Ljc2MVY5Ny4xMDQxSDkyNC4wODlWMjg2Ljc2MUg4NzIuMTIzWiIgZmlsbD0iY3VycmVudENvbG9yIiAvPjxwYXRoIGQ9Ik03ODEuNjM4IDI4Ni43NjFWMi4yNzYwOUg4MzMuNjA0VjI4Ni43NjFINzgxLjYzOFoiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48cGF0aCBkPSJNNzIyLjkzNCAyODkuMDM3QzcwMS42OTMgMjg5LjAzNyA2ODQuMjQ0IDI4My4yMjEgNjcwLjU4OSAyNzEuNTg4QzY1Ny4xODcgMjU5LjcwMyA2NTAuNDg1IDI0Mi42MzQgNjUwLjQ4NSAyMjAuMzgxVjE0Mi42MjJINjEyLjE3NVY5Ny4xMDQ0SDY1MC40ODVWNDQuMzc5OUg3MDIuNDUxVjk3LjEwNDRINzU1LjkzNFYxNDIuNjIySDcwMi40NTFWMjEwLjE0QzcwMi40NTEgMjIxLjc3MiA3MDQuOTggMjMwLjExNyA3MTAuMDM4IDIzNS4xNzRDNzE1LjA5NSAyMzkuOTc5IDcyMy4zMTMgMjQyLjM4MSA3MzQuNjkzIDI0Mi4zODFDNzQyLjc4NSAyNDIuMzgxIDc0OS44NjUgMjQxLjI0MyA3NTUuOTM0IDIzOC45NjdWMjg0Ljg2NEM3NDYuODMxIDI4Ny42NDYgNzM1LjgzMSAyODkuMDM3IDcyMi45MzQgMjg5LjAzN1oiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48cGF0aCBkPSJNNDE3LjY3NCAyODYuNzYxVjk3LjEwNDFINDY5LjY0VjExMC45NjdDNDY5LjY0IDExMy4zMTEgNDcyLjgzIDExNC4zNDcgNDc0LjM4MiAxMTIuNTkxQzQ4NS45NjcgOTkuNDg0OCA1MDIuNDY3IDkyLjkzMTcgNTIzLjg4MSA5Mi45MzE3QzU0Ni42NCA5Mi45MzE3IDU2NC40NjggMTAwLjUxOCA1NzcuMzY1IDExNS42OUM1OTAuNTE0IDEzMC42MSA1OTcuMDg5IDE1MC41ODcgNTk3LjA4OSAxNzUuNjIyVjI4Ni43NjFINTQ1LjEyM1YxODQuMzQ2QzU0NS4xMjMgMTcwLjQzOCA1NDIuMjE1IDE1OS42OTEgNTM2LjM5OSAxNTIuMTA1QzUzMC41ODMgMTQ0LjI2NSA1MjIuMzY0IDE0MC4zNDYgNTExLjc0MyAxNDAuMzQ2QzQ5OS4xIDE0MC4zNDYgNDg4Ljg1OCAxNDQuODk4IDQ4MS4wMTkgMTU0LjAwMUM0NzMuNDMzIDE2My4xMDUgNDY5LjY0IDE3Ni41MDcgNDY5LjY0IDE5NC4yMDhWMjg2Ljc2MUg0MTcuNjc0WiIgZmlsbD0iY3VycmVudENvbG9yIiAvPjxwYXRoIGQ9Ik0zNTIuOTgxIDY2LjAwMDVDMzQ0LjEzIDY2LjAwMDUgMzM2LjQxNyA2Mi44Mzk1IDMyOS44NDMgNTYuNTE3NkMzMjMuMjY4IDQ5Ljk0MjkgMzE5Ljk4IDQyLjEwMzcgMzE5Ljk4IDMzLjAwMDJDMzE5Ljk4IDIzLjg5NjcgMzIzLjI2OCAxNi4xODQgMzI5Ljg0MyA5Ljg2MjE1QzMzNi40MTcgMy4yODczOCAzNDQuMTMgMCAzNTIuOTgxIDBDMzYyLjMzNyAwIDM3MC4xNzYgMy4yODczOCAzNzYuNDk4IDkuODYyMTVDMzgzLjA3MyAxNi4xODQgMzg2LjM2IDIzLjg5NjcgMzg2LjM2IDMzLjAwMDJDMzg2LjM2IDQyLjEwMzcgMzgzLjA3MyA0OS45NDI5IDM3Ni40OTggNTYuNTE3NkMzNzAuMTc2IDYyLjgzOTUgMzYyLjMzNyA2Ni4wMDA1IDM1Mi45ODEgNjYuMDAwNVpNMzI3LjE4NyAyODYuNzYxVjk3LjEwNDFIMzc5LjE1M1YyODYuNzYxSDMyNy4xODdaIiBmaWxsPSJjdXJyZW50Q29sb3IiIC8+PHBhdGggZD0iTTIzOC45NjcgMjg2Ljc2MVYxODUuNDg0QzIzOC45NjcgMTU1LjM5MiAyMjkuMTA1IDE0MC4zNDYgMjA5LjM4MSAxNDAuMzQ2QzE5OC4wMDEgMTQwLjM0NiAxODguODk4IDE0NC42NDUgMTgyLjA3IDE1My4yNDJDMTc1LjQ5NSAxNjEuODQgMTcxLjk1NSAxNzQuNjEgMTcxLjQ0OSAxOTEuNTUzVjI4Ni43NjFIMTE5LjQ4NFYxODUuNDg0QzExOS40ODQgMTU1LjM5MiAxMDkuNjIxIDE0MC4zNDYgODkuODk3MiAxNDAuMzQ2Qzc4LjI2NDkgMTQwLjM0NiA2OS4wMzUgMTQ0Ljg5OCA2Mi4yMDczIDE1NC4wMDFDNTUuMzc5NyAxNjMuMTA1IDUxLjk2NTkgMTc2LjUwNyA1MS45NjU5IDE5NC4yMDhWMjg2Ljc2MUgwVjk3LjEwNDFINTEuOTY1OVYxMTEuMTAzQzUxLjk2NTkgMTEzLjQzNSA1NS4xMDE0IDExNC40NjIgNTYuNjMzIDExMi43MDRDNjguMTEzNiA5OS41MjIzIDgzLjM3NDEgOTIuOTMxNyAxMDIuNDE1IDkyLjkzMTdDMTI3LjQzNiA5Mi45MzE3IDE0Ni4yODMgMTAzLjI2MiAxNTguOTUzIDEyMy45MjNDMTU5Ljk1MyAxMjUuNTUzIDE2Mi40MTIgMTI1LjUyNyAxNjMuNDA2IDEyMy44OTRDMTY4Ljg4NCAxMTQuODkxIDE3Ni40OTYgMTA3LjczMSAxODYuMjQzIDEwMi40MTVDMTk3LjM2OSA5Ni4wOTI2IDIwOC42MjIgOTIuOTMxNyAyMjAuMDAyIDkyLjkzMTdDMjQyLjUwNyA5Mi45MzE3IDI1OS45NTYgMTAwLjM5MiAyNzIuMzQ3IDExNS4zMTFDMjg0LjczOCAxMzAuMjMxIDI5MC45MzMgMTUwLjcxNCAyOTAuOTMzIDE3Ni43NlYyODYuNzYxSDIzOC45NjdaIiBmaWxsPSJjdXJyZW50Q29sb3IiIC8+PC9zdmc+)This documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com?utm_campaign=poweredBy&utm_medium=referral&utm_source=lmsysorg)
