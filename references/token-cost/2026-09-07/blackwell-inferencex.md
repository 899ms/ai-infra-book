<!-- 从 blackwell-inferencex.html 迁移的资料快照；原始 HTML SHA-256: 2b3f9379dd047ad563e52d511339634789bb2c8e139abe2bd5f167aa404ab527。 -->

# New SemiAnalysis InferenceX Data Shows NVIDIA Blackwell Ultra Delivers up to 50x Better Performance and 35x Lower Costs for Agentic AI

Cloud providers including Microsoft, CoreWeave and Oracle Cloud Infrastructure are deploying NVIDIA GB300 NVL72 systems at scale for low-latency and long-context use cases such as agentic coding and coding assistants.

February 16, 2026 by [Ashraf Eassa](https://blogs.nvidia.com/blog/author/ashrafeassa/ "Posts by Ashraf Eassa")

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTExIDEuNUM2LjAyOTQ0IDEuNSAyIDUuNTI5NDQgMiAxMC41QzIgMTUuNDcwNiA2LjAyOTQ0IDE5LjUgMTEgMTkuNUMxNS45NzA2IDE5LjUgMjAgMTUuNDcwNiAyMCAxMC41QzIwIDUuNTI5NDQgMTUuOTcwNiAxLjUgMTEgMS41Wk0wLjUgMTAuNUMwLjUgNC43MDEwMSA1LjIwMTAxIDAgMTEgMEMxNi43OTkgMCAyMS41IDQuNzAxMDEgMjEuNSAxMC41QzIxLjUgMTYuMjk5IDE2Ljc5OSAyMSAxMSAyMUM1LjIwMTAxIDIxIDAuNSAxNi4yOTkgMC41IDEwLjVaTTEwLjI1IDQuNUgxMS43NVY5LjkyNDVMMTYuOTkxMSAxMS4zMjg5TDE2LjYwMjkgMTIuNzc3N0wxMC4yNSAxMS4wNzU1VjQuNVoiIGZpbGw9IiM2NjY2NjYiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTguNyIgdmlld2JveD0iMCAwIDE4IDE4LjciIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CiAgICAgICAgICAgICAgICAgICAgPHBhdGggZmlsbC1ydWxlPSJldmVub2RkIiBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0wIDAuNUgxOFYxNS41SDguNTY1NTNMNC44NjQ0MiAxOS4yMDExTDMuODcyNzEgMTUuNUgwVjAuNVpNMS41IDJWMTRINS4wMjM3MUw1LjY0MDg4IDE2LjMwMzNMNy45NDQyMSAxNEgxNi41VjJIMS41WiIgZmlsbD0iIzY2NjY2NiIgLz4KICAgICAgICAgICAgICAgIDwvc3ZnPg==)

[0 Comments](https://blogs.nvidia.com/blog/data-blackwell-ultra-performance-lower-cost-agentic-ai/#disqus_thread)

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTkiIHZpZXdib3g9IjAgMCAxOCAxOSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMTggMC41SDEwLjVWMkgxNS40MzkzTDYuOTY5NjcgMTAuNDY5Nkw4LjAzMDMzIDExLjUzMDNMMTYuNSAzLjA2MDYzVjhIMThWMC41WiIgZmlsbD0iIzY2NjY2NiIgLz4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBkPSJNNy41IDEuOTk5OTdIMFYxOC41SDE2LjVWMTFIMTVWMTdIMS41VjMuNDk5OTdINy41VjEuOTk5OTdaIiBmaWxsPSIjNjY2NjY2IiAvPgogICAgICAgICAgICAgICAgPC9zdmc+)

Share

Share This Article

- [ ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaWNvbi1zb2NpYWwtdHdpdHRlciIgd2lkdGg9IjI1cHgiIGhlaWdodD0iMjVweCIgdmlld2JveD0iMCAwIDI0IDI0IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPgogICAgICAgICAgICA8cGF0aCBmaWxsPSIjZmZmIiBkPSJNMTMuOTAzIDEwLjQ2OSAyMS4zNDggMmgtMS43NjRsLTYuNDY1IDcuMzUzTDcuOTU1IDJIMmw3LjgwOCAxMS4xMkwyIDIyaDEuNzY0CiAgICAgICAgICAgICAgICBsNi44MjgtNy43NjVMMTYuMDQ0IDIySDIybC04LjA5Ny0xMS41MzFabS0yLjQxNyAyLjc0OC0uNzkxLTEuMTA3CiAgICAgICAgICAgICAgICBMNC40IDMuM2gyLjcxbDUuMDggNy4xMS43OTEgMS4xMDcgNi42MDQgOS4yNDJoLTIuNzFsLTUuMzg5LTcuNTQyWiI+CiAgICAgICAgICAgIDwvcGF0aD4KICAgICAgICA8L3N2Zz4=) ](https://twitter.com/intent/tweet?text=New%20SemiAnalysis%20InferenceX%20Data%20Shows%20NVIDIA%20Blackwell%20Ultra%20Delivers%20up%20to%2050x%20Better%20Performance%20and%2035x%20Lower%20Costs%20for%20Agentic%20AI%20https%3A%2F%2Fblogs.nvidia.com%2Fblog%2Fdata-blackwell-ultra-performance-lower-cost-agentic-ai%2F)

  X

- [ ![](data:image/svg+xml;base64,PHN2ZyB2ZXJzaW9uPSIxLjEiIGlkPSJMYXllcl8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCIgdmlld2JveD0iMCAwIDUxMiA1MTIiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpuZXcgMCAwIDUxMiA1MTI7IiB4bWw6c3BhY2U9InByZXNlcnZlIiB3aWR0aD0iMjVweCIgaGVpZ2h0PSIyNXB4IiBmaWxsPSIjZmZmIj4KICAgICAgICAgICAgICAgICAgICA8Zz4KICAgICAgICAgICAgICAgICAgICAgICAgPHBhdGggZD0iTTMwNCwxOTJoOTZ2OTZoLTk2djIyNGgtOTZWMjg4aC05NnYtOTZoOTZ2LTQwLjJjMC0zOCwxMi04Ni4xLDM1LjgtMTEyLjQKICAgICAgICAgICAgICAgICAgICAgICAgICAgIEMyNjcuNiwxMy4xLDI5Ny4zLDAsMzMyLjksMEg0MDB2OTZoLTY3LjIKICAgICAgICAgICAgICAgICAgICAgICAgICAgIGMtMTUuOSwwLTI4LjgsMTIuOS0yOC44LDI4LjhWMTkyeiIgLz4KICAgICAgICAgICAgICAgICAgICA8L2c+CiAgICAgICAgICAgICAgICA8L3N2Zz4=) ](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fblogs.nvidia.com%2Fblog%2Fdata-blackwell-ultra-performance-lower-cost-agentic-ai%2F)

  Facebook

- [ ![](data:image/svg+xml;base64,PHN2ZyB2ZXJzaW9uPSIxLjEiIGlkPSJMYXllcl8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCIgdmlld2JveD0iMCAwIDUxMiA1MTIiIHdpZHRoPSIyNXB4IiBoZWlnaHQ9IjI1cHgiIHN0eWxlPSJlbmFibGUtYmFja2dyb3VuZDpuZXcgMCAwIDUxMiA1MTI7IiB4bWw6c3BhY2U9InByZXNlcnZlIiBmaWxsPSIjZmZmIj4KICAgICAgICAgICAgICAgIDxnPgogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik01MTIsMzExLjM0djE4OS4yOUg0MDIuMjdWMzI0LjAxCiAgICAgICAgICAgICAgICAgICAgICAgIGMwLTQ0LjM5LTE1Ljg4LTc0LjY1LTU1LjU5LTc0LjY1CiAgICAgICAgICAgICAgICAgICAgICAgIGMtMzAuMzQsMC00OC4zNywyMC40Mi01Ni4zMiw0MC4xMwogICAgICAgICAgICAgICAgICAgICAgICBjLTIuOTEsNy4wNi0zLjYzLDE2Ljg4LTMuNjMsMjYuNzV2MTg0LjM4aC0xMDkuOAogICAgICAgICAgICAgICAgICAgICAgICBjMCwwLDEuNDgtMjk5LjExLDAtMzMwLjEzaDEwOS44djQ2LjhsLTAuNzMsMS4wOGgwLjczdi0xLjA4CiAgICAgICAgICAgICAgICAgICAgICAgIGMxNC41NS0yMi40NSw0MC42MS01NC41NCw5OC45LTU0LjU0QzQ1Ny44NiwxNjIuNzYsNTEyLDIwOS45Niw1MTIsMzExLjM0egogICAgICAgICAgICAgICAgICAgICAgICBNNjIuMTMsMTEuMzdDMjQuNTgsMTEuMzcsMCwzNiwwLDY4LjM5CiAgICAgICAgICAgICAgICAgICAgICAgIGMwLDMxLjY5LDIzLjg3LDU3LjA3LDYwLjY3LDU3LjA3aDAuNzNjMzguMywwLDYyLjA4LTI1LjM4LDYyLjA4LTU3LjA3CiAgICAgICAgICAgICAgICAgICAgICAgIEMxMjIuOCwzNiw5OS43MywxMS4zNyw2Mi4xNSwxMS4zN0g2Mi4xM3ogTTYuNTQsNTAwLjYzCiAgICAgICAgICAgICAgICAgICAgICAgIGgxMDkuNzNWMTcwLjVINi41NFY1MDAuNjN6IiAvPgogICAgICAgICAgICAgICAgPC9nPgogICAgICAgICAgICAgICAgPC9zdmc+) ](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fblogs.nvidia.com%2Fblog%2Fdata-blackwell-ultra-performance-lower-cost-agentic-ai%2F&title=New+SemiAnalysis+InferenceX+Data+Shows+NVIDIA+Blackwell+Ultra+Delivers+up+to+50x+Better+Performance+and+35x+Lower+Costs+for+Agentic+AI)

  LinkedIn

- [ ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjVweCIgaGVpZ2h0PSIyNXB4IiB2aWV3Ym94PSIwIDAgMjQgMjQiIGZpbGw9Im5vbmUiPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8cmVjdCB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIGZpbGw9IiMwMDAwMDAiIC8+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Ik04IDlWN2EyIDIgMCAwIDEgMi0yaDZhMiAyIDAgMCAxIDIgMnY4YTIgMiAwIDAgMS0yIDJoLTIiIHN0cm9rZT0iI0ZGRiIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIC8+CiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDxyZWN0IHg9IjQiIHk9IjEzIiB3aWR0aD0iOCIgaGVpZ2h0PSI4IiByeD0iMiIgc3Ryb2tlPSIjRkZGIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgLz4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICA8L3N2Zz4=) ](# "Copy link to clipboard")

  Copy link

  Link copied!

![](https://blogs.nvidia.com/wp-content/uploads/2026/02/inference-charts-inferencemax-v1.5-perf-charts-4753570-r12_1-alt-scaled-1280x720.png)

The NVIDIA Blackwell platform has been widely adopted by leading inference providers such as [Baseten, DeepInfra, Fireworks AI and Together AI](https://blogs.nvidia.com/blog/inference-open-source-models-blackwell-reduce-cost-per-token) to reduce cost per token by up to 10x. Now, the NVIDIA Blackwell Ultra platform is taking this momentum further for agentic AI.

AI agents and coding assistants are driving explosive growth in software-programming-related AI queries: from 11% to about 50% last year, according to [OpenRouter’s State of Inference report](https://openrouter.ai/state-of-ai). These applications require low latency to maintain real-time responsiveness across multistep workflows and long context when reasoning across entire codebases.

[New SemiAnalysis InferenceX performance data](https://inferencex.semianalysis.com/) shows that the combination of NVIDIA’s software optimizations and the next-generation NVIDIA Blackwell Ultra platform has delivered breakthrough advances on both fronts. NVIDIA GB300 NVL72 systems now deliver up to 50x higher throughput per megawatt, resulting in 35x lower cost per token compared with the NVIDIA Hopper platform.

By innovating across chips, system architecture and software, NVIDIA’s extreme codesign accelerates performance across AI workloads — from agentic coding to interactive coding assistants — while driving down costs at scale.

![](https://blogs.nvidia.com/wp-content/uploads/2026/02/semianalysisv5-1680x945.jpg)

## **GB300 NVL72 Delivers up to 50x Better Performance for Low-Latency Workloads**

Recent analysis from [Signal65](https://signal65.com/research/ai/from-dense-to-mixture-of-experts-the-new-economics-of-ai-inference/) shows that NVIDIA GB200 NVL72 with extreme hardware and software codesign delivers more than 10x more tokens per watt, resulting in one-tenth the cost per token compared with the NVIDIA Hopper platform. These massive performance gains continue to expand as the underlying stack improves.

Continuous optimizations from the NVIDIA TensorRT-LLM, NVIDIA Dynamo, Mooncake and SGLang teams continue to significantly boost Blackwell NVL72 throughput for [mixture-of-experts (MoE) inference](https://blogs.nvidia.com/blog/mixture-of-experts-frontier-models/) across all latency targets. For instance, NVIDIA TensorRT-LLM library improvements have delivered up to 5x better performance on GB200 for low-latency workloads compared with just four months ago.

- **Higher-performance GPU kernels** optimized for efficiency and low latency help make the most of Blackwell’s immense compute capabilities and boost throughput.
- **NVIDIA NVLink Symmetric Memory** enables direct GPU-to-GPU memory access for more efficient communication.
- **Programmatic dependent launch** minimizes idle time by launching the next kernel’s setup phase before the previous one completes.

Building on these software advances, GB300 NVL72 — which features the Blackwell Ultra GPU — pushes the throughput-per-megawatt frontier to 50x compared with the Hopper platform.

This performance gain translates into superior economics, with NVIDIA GB300 lowering costs compared with the Hopper platform across the entire latency spectrum. The most dramatic reduction occurs at low latency, where agentic applications operate: up to 35x lower cost per million tokens compared with the Hopper platform.

![](https://blogs.nvidia.com/wp-content/uploads/2026/02/gb300-nvl72-delivers-35x-reduction-in-token-cost-1680x945.png)

NVIDIA GB300 NVL72 and the codesigned software stack including NVIDIA Dynamo and TensorRT-LLM deliver 35x lower cost per token compared with NVIDIA Hopper platform.

For agentic coding and interactive assistants workloads where every millisecond compounds across multistep workflows, this combination of relentless software optimization and next-generation hardware enables AI platforms to scale real-time interactive experiences to significantly more users.

## **GB300 NVL72 Delivers Superior Economics for Long-Context Workloads**

While both GB200 NVL72 and GB300 NVL72 efficiently deliver ultralow latency, the distinct advantages of GB300 NVL72 become most apparent in long-context scenarios. [For workloads with 128,000-token inputs and 8,000-token outputs](https://developer.nvidia.com/deep-learning-performance-training-inference/ai-inference) — such as AI coding assistants reasoning across codebases — GB300 NVL72 delivers up to 1.5x lower cost per token compared with GB200 NVL72.

![](https://blogs.nvidia.com/wp-content/uploads/2026/02/gb300-nvl72-delivers-large-leap-for-long-context-ai-1680x945.png)

NVIDIA GB300 NVL72 is ideal for low-latency, long-context workloads.

Context grows as the agent reads in more of the code. This allows it to better understand the code base but also requires much more compute. Blackwell Ultra has 1.5x higher NVFP4 compute performance and 2x faster attention processing, enabling the agent to efficiently understand entire code bases.

## **Infrastructure for Agentic AI**

Leading cloud providers and AI innovators have already deployed NVIDIA GB200 NVL72 at scale, and are also deploying GB300 NVL72 in production. [Microsoft](https://azure.microsoft.com/en-us/blog/microsoft-azure-delivers-the-first-large-scale-cluster-with-nvidia-gb300-nvl72-for-openai-workloads/), [CoreWeave](https://www.coreweave.com/blog/coreweaves-nvidia-gb300-nvl72-production-ready-instances-for-enterprise-ai-featuring-nvidia-blackwell-ultra-gpus-deliver-more-than-6x-performance-gain-on-deepseek-r1) and [OCI](https://blogs.oracle.com/cloud-infrastructure/supercluster-nvidia-blackwell-dedicated-alloy) are deploying GB300 NVL72 for low-latency and long-context use cases such as agentic coding and coding assistants. By reducing token costs, GB300 NVL72 enables a new class of applications that can reason across massive codebases in real time.

“As inference moves to the center of AI production, long-context performance and token efficiency become critical,” said Chen Goldberg, senior vice president of engineering at CoreWeave. “Grace Blackwell NVL72 addresses that challenge directly, and CoreWeave’s AI cloud, including CKS and SUNK, is designed to translate GB300 systems’ gains, building on the success of GB200, into predictable performance and cost efficiency. The result is better token economics and more usable inference for customers running workloads at scale.”

## **NVIDIA Vera Rubin NVL72 to Bring Next-Generation Performance**

With NVIDIA Blackwell systems deployed at scale, continuous software optimizations will keep unlocking additional performance and cost improvements across the installed base.

Looking ahead, the [NVIDIA Rubin platform](https://www.nvidia.com/en-us/data-center/technologies/rubin/) — which combines six new chips to create one AI supercomputer — is set to deliver another round of massive performance leaps. For MoE inference, it delivers up to 10x higher throughput per megawatt compared with Blackwell, translating into one-tenth the cost per million tokens. And for the next wave of frontier AI models, Rubin can train large MoE models using just one-fourth the number of GPUs compared with Blackwell.

*Learn more about the NVIDIA Rubin platform and the* [*Vera Rubin NVL72 system*](https://www.nvidia.com/en-us/data-center/vera-rubin-nvl72/)*. *

![NVIDIA GTC Berlin Registration Is Now Open](https://blogs.nvidia.com/wp-content/uploads/2026/06/gtc26-berlin-open-reg-mktg-kit-corp-blog-1920x1080-1-1-960x540.jpg)

### [NVIDIA GTC Berlin Registration Is Now Open](https://www.nvidia.com/en-eu/gtc/?nvid=nv-int-tblg-568814)

October 20-22

[Register Now ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdib3g9IjAgMCAyMiAyMiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMS4yNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgPHBhdGggZD0iTTkgNmw2IDYtNiA2IiAvPgogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIDwvc3ZnPg==) ](https://www.nvidia.com/en-eu/gtc/?nvid=nv-int-tblg-568814)

### Recent News

[AI](https://blogs.nvidia.com/blog/category/generative-ai/)

### [Sparks Fly: NVIDIA Accelerates Local AI at IFA 2026](https://blogs.nvidia.com/blog/local-ai-ifa-next-gen-agents-nv-pair-rtx-spark/)

September 3, 2026

[Gaming](https://blogs.nvidia.com/blog/category/gaming/)

### [‘NBA 2K27’ With NVIDIA DLSS 5 Leads 28 New Games Coming to GeForce NOW](https://blogs.nvidia.com/blog/geforce-now-thursday-september-2026-games-list/)

September 3, 2026

[Corporate](https://blogs.nvidia.com/blog/category/corporate/)

### [NVIDIA to Acquire Hugging Face](https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/)

September 3, 2026

[AI](https://blogs.nvidia.com/blog/category/generative-ai/)

### [NVIDIA and CrowdStrike Strengthen Agentic Cybersecurity Frontier](https://blogs.nvidia.com/blog/nvidia-crowdstrike-fal-con-2026/)

September 1, 2026

[View All Recent News ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAiIGhlaWdodD0iMjAiIHZpZXdib3g9IjAgMCAyMiAyMiIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMS4yNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj4KICAgICAgICAgICAgICAgICAgICAgICAgPHBhdGggZD0iTTkgNmw2IDYtNiA2IiAvPgogICAgICAgICAgICAgICAgICAgIDwvc3ZnPg==) ](https://blogs.nvidia.com/recent-news/)

- Categories:
- [AI Infrastructure](https://blogs.nvidia.com/blog/category/enterprise/)
- [Cloud](https://blogs.nvidia.com/blog/category/enterprise/cloud-2/)
- [Hardware](https://blogs.nvidia.com/blog/category/enterprise/hardware/)
- [Networking](https://blogs.nvidia.com/blog/category/enterprise/intelligent-networking/)
- [Software](https://blogs.nvidia.com/blog/category/enterprise/software/)

- Tags:
- [Agentic AI](https://blogs.nvidia.com/blog/tag/agentic-ai/)
- [Dynamo](https://blogs.nvidia.com/blog/tag/dynamo/)
- [Inference](https://blogs.nvidia.com/blog/tag/inference/)
- [NVIDIA Blackwell](https://blogs.nvidia.com/blog/tag/nvidia-blackwell/)
- [NVIDIA Rubin](https://blogs.nvidia.com/blog/tag/nvidia-rubin/)
- [NVLink](https://blogs.nvidia.com/blog/tag/nvlink/)
- [TensorRT](https://blogs.nvidia.com/blog/tag/tensorrt/)
- [Think SMART](https://blogs.nvidia.com/blog/tag/think-smart/)

### Related News

[](https://blogs.nvidia.com/blog/local-ai-ifa-next-gen-agents-nv-pair-rtx-spark/)

![Sparks Fly: NVIDIA Accelerates Local AI at IFA 2026](https://blogs.nvidia.com/wp-content/uploads/2026/09/nv-blog-1280x680-1-300x169.jpg)

[AI](https://blogs.nvidia.com/blog/category/generative-ai/)

### [Sparks Fly: NVIDIA Accelerates Local AI at IFA 2026](https://blogs.nvidia.com/blog/local-ai-ifa-next-gen-agents-nv-pair-rtx-spark/)

Sep 3, 2026

[](https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/)

![NVIDIA to Acquire Hugging Face](https://blogs.nvidia.com/wp-content/uploads/2026/09/hf-nvidia-partner_hf-nvidia-partner-press-1920x1080-2-300x169.png)

[Corporate](https://blogs.nvidia.com/blog/category/corporate/)

### [NVIDIA to Acquire Hugging Face](https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/)

Sep 3, 2026

[](https://blogs.nvidia.com/blog/ugm-indosat-nvidia-ai-technology-center/)

![Universitas Gadjah Mada, Indosat and NVIDIA Open Indonesia’s First University AI Center to Develop Local AI Talent](https://blogs.nvidia.com/wp-content/uploads/2026/08/telco-tech-blog-header-indosat-ai-technology-center-1920x1080-1-300x169.png)

[AI](https://blogs.nvidia.com/blog/category/generative-ai/)

### [Universitas Gadjah Mada, Indosat and NVIDIA Open Indonesia’s First University AI Center to Develop Local AI Talent](https://blogs.nvidia.com/blog/ugm-indosat-nvidia-ai-technology-center/)

Aug 14, 2026

[](https://blogs.nvidia.com/blog/local-ai-open-source-models-agents-nemotron/)

![NVIDIA and Local AI Community Fuel Open Source Models and Intelligent Agents](https://blogs.nvidia.com/wp-content/uploads/2026/08/raig-rolling-blog-local-ai-community-open-source-300x169.jpg)

[AI](https://blogs.nvidia.com/blog/category/generative-ai/)

### [NVIDIA and Local AI Community Fuel Open Source Models and Intelligent Agents](https://blogs.nvidia.com/blog/local-ai-open-source-models-agents-nemotron/)

Aug 11, 2026
