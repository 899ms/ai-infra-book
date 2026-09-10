<!-- 从 lia-google-index.html 迁移的资料快照；原始 HTML SHA-256: 5cb38657d564336d7765e4b537324d674355ec0f6ce32ae98e5a34c677b1a214。 -->

June 23, 2025

# LIA: Cost-efficient LLM Inference Acceleration with Intel Advanced Matrix Extensions and CXL

[](https://dl.acm.org/doi/full/10.1145/3695053.3731092)

View publication

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIC05NjAgOTYwIDk2MCIgYXJpYS1oaWRkZW49InRydWUiIGZpbGw9ImN1cnJlbnRDb2xvciIgaGVpZ2h0PSIyNHB4IiByb2xlPSJwcmVzZW50YXRpb24iIHdpZHRoPSIyNHB4IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0yMzcuNjktMTAwcS0yMy41MyAwLTQwLjYxLTE3LjA4VDE4MC0xNTcuNjl2LTQyNS45MnEwLTIzLjUzIDE3LjA4LTQwLjYxIDE3LjA4LTE3LjA5IDQwLjYxLTE3LjA5aDEzOC4yM3Y0NS4zOUgyMzcuNjlxLTQuNjEgMC04LjQ2IDMuODQtMy44NCAzLjg1LTMuODQgOC40N3Y0MjUuOTJxMCA0LjYxIDMuODQgOC40NiAzLjg1IDMuODQgOC40NiAzLjg0aDQ4NC42MnE0LjYxIDAgOC40Ni0zLjg0IDMuODQtMy44NSAzLjg0LTguNDZ2LTQyNS45MnEwLTQuNjItMy44NC04LjQ3LTMuODUtMy44NC04LjQ2LTMuODRINTgyLjg1di00NS4zOWgxMzkuNDZxMjMuNTMgMCA0MC42MSAxNy4wOVE3ODAtNjA3LjE0IDc4MC01ODMuNjF2NDI1LjkycTAgMjMuNTMtMTcuMDggNDAuNjFUNzIyLjMxLTEwMEgyMzcuNjlabTIxOS0yNDkuNjl2LTQ0OC41NGwtOTEuNDYgOTEuNDYtMzMtMzIuNjEgMTQ3LjE1LTE0Ni43NyAxNDYuNzcgMTQ2Ljc3LTMyLjYxIDMyLjYxLTkxLjQ2LTkxLjQ2djQ0OC41NGgtNDUuMzlaIiAvPjwvc3ZnPg==)

Share

[![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWxhYmVsPSJYIGxvZ28iIGNsYXNzPSJzaGFyZS1saXN0X19pY29uIiBmb2N1c2FibGU9ImZhbHNlIiBoZWlnaHQ9IjI0IiByb2xlPSJpbWciIHdpZHRoPSIyNCI+PHVzZSBocmVmPSIjeCIgLz48L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://deepmind.google/research/publications/81986/&text=LIA%3A%20Cost-efficient%20LLM%20Inference%20Acceleration%20with%20Intel%20Advanced%20Matrix%20Extensions%20and%20CXL) [![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWxhYmVsPSJGYWNlYm9vayBsb2dvIiBjbGFzcz0ic2hhcmUtbGlzdF9faWNvbiIgZm9jdXNhYmxlPSJmYWxzZSIgaGVpZ2h0PSIyNCIgcm9sZT0iaW1nIiB3aWR0aD0iMjQiPjx1c2UgaHJlZj0iI2ZhY2Vib29rIiAvPjwvc3ZnPg==)](https://www.facebook.com/sharer/sharer.php?u=https://deepmind.google/research/publications/81986/) [![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWxhYmVsPSJMaW5rZWRJbiBsb2dvIiBjbGFzcz0ic2hhcmUtbGlzdF9faWNvbiIgZm9jdXNhYmxlPSJmYWxzZSIgaGVpZ2h0PSIyNCIgcm9sZT0iaW1nIiB3aWR0aD0iMjQiPjx1c2UgaHJlZj0iI2xpbmtlZGluIiAvPjwvc3ZnPg==)](https://www.linkedin.com/sharing/share-offsite/?url=https://deepmind.google/research/publications/81986/) [![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWxhYmVsPSJFbWFpbCBpY29uIiBjbGFzcz0ic2hhcmUtbGlzdF9faWNvbiIgZm9jdXNhYmxlPSJmYWxzZSIgaGVpZ2h0PSIyNCIgcm9sZT0iaW1nIiB3aWR0aD0iMjQiPjx1c2UgaHJlZj0iI2VtYWlsIiAvPjwvc3ZnPg==)](mailto:?subject=LIA%3A%20Cost-efficient%20LLM%20Inference%20Acceleration%20with%20Intel%20Advanced%20Matrix%20Extensions%20and%20CXL&body=https://deepmind.google/research/publications/81986/)

![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWxhYmVsPSJMaW5rIGljb24iIGNsYXNzPSJzaGFyZS1saXN0X19pY29uIiBmb2N1c2FibGU9ImZhbHNlIiBoZWlnaHQ9IjI0IiByb2xlPSJpbWciIHdpZHRoPSIyNCI+PHVzZSBocmVmPSIjbGluayIgLz48L3N2Zz4=) Copied

## Abstract

The limited memory capacity of single GPUs constrains large language model (LLM) inference, necessitating cost-prohibitive multiGPU deployments or frequent performance-limiting CPU-GPU transfers over slow PCIe. In this work, we first benchmark recent Intel CPUs with Advanced Matrix Extensions (AMX), including 4th generation (Sapphire Rapids) and 6th generation (Granite Rapids) Xeon Scalable Processors, demonstrating matrix multiplication throughput of 20 TFLOPS and 40 TFLOPS, respectively— comparable to some recent GPUs. These findings unlock more extensive computation offloading to CPUs, reducing CPU-GPU transfers and alleviating throughput bottlenecks compared to prior generation CPUs. Building on these insights, we design LIA, a single-GPU LLM inference acceleration framework leveraging cooperative AMX-enabled CPU-GPU computation and CXL offloading.LIA systematically offloads computation to CPUs, optimizing both latency and throughput. The framework also introduces a memory offloading policy that seamlessly integrates affordable CXL memory with DDR memory to enhance performance in throughput-driven tasks. On Saphhire Rapids (Granite Rapids) systems with a single H100 GPU, LIA achieves up to 5.1× (19×) lower latency and 3.7×(5.1×) higher throughput compared to the latest single-GPU offloading framework. Furthermore, LIA deploying CXL offloading yields an additional 1.5× throughput improvement over LIA using only DDR memory with a 1.8× increase in maximum batch size (900→1.6K).

## Authors

Hyungyo Kim\*, Nachuan Wang\*, Qirong Xia\*, Jinghan Huang\*, Amir Yazdanbakhsh, Nam Sung Kim\*

\* External author

## Venue

ISCA 2025
