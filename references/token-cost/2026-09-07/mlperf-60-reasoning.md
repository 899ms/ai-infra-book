<!-- 从 mlperf-60-reasoning.html 迁移的资料快照；原始 HTML SHA-256: 2fcfcc0ccd2a22c8adeadd73529c7f380208043ee0d0dfcf850c11936800ab85。 -->

Insights

# A new GPT-OSS benchmark and DeepSeek R1 updates for latency-optimized reasoning

MLPerf Inference v6.0 expands open-weight LLM coverage with a new GPT-OSS 120B benchmark and a latency-constrained interactive scenario for DeepSeek-R1 — the first MLPerf standard for speculative decoding.

March 24, 2026

![](https://mlcommons.org/wp-content/uploads/2026/03/sazzzz.svg)

## Introduction

The MLPerf® Inference v6.0 release marks a significant expansion in our coverage of the open-weight large language model (LLM) landscape. As the industry moves toward more specialized and capable open models, the benchmarks must evolve to reflect these shifts in deployment strategies and model architectures.

In this round, the Reasoning LLM task force introduces two major additions to the suite:

- **GPT-OSS 120B:** a new benchmark based on a popular open-source, high-capability model which excels at mathematics, scientific reasoning, and coding. It features a large-scale mixture-of-experts (MOE) architecture of 117B total parameters. 
- **DeepSeek-R1 interactive scenario:** Building upon the existing DeepSeek-R1 benchmark, we add a low-latency-constrained interactive workload targeting real-time reasoning applications. This workload also features the first standard for speculative decoding in MLPerf.

## A new benchmark with GPT-OSS 120B

GPT-OSS 120B is a popular new open-source, high-capability model, featuring a mixture-of-experts (MoE) architecture with 117B total parameters (5.1B active per token). This model natively supports configurable reasoning effort levels and is deployed across a diverse range of complex, knowledge-intensive workflows including advanced coding, competition mathematics, and graduate-level scientific logic. 

Frontier models are often deployed across a wide spectrum of production workloads—from fast, routine requests to complex, multi-step problem solving. To accurately reflect this duality, we introduced a split-dataset strategy: 

- Performance dataset of routine, low-effort usage tasks (e.g., summarization)
- Accuracy dataset of difficult reasoning problems across coding, scientific knowledge and math.

Across both modes, all inputs utilize the OpenAI [Harmony chat format](https://developers.openai.com/cookbook/articles/openai-harmony/), allowing us to natively control the model’s reasoning effort (low, medium, or high) directly through system prompts.

### Dataset selection for GPT-OSS

For the first time in MLPerf inference benchmark we have decided to separate performance and accuracy datasets. In all existing MLPerf Inference benchmarks, a single dataset is used for both. However, separating the two brings flexibility that allows agility in benchmark definition for this workload and also in the future. Additionally, the two tasks are different, and the separation allows the use of an optimal dataset for each task. 

A key consideration in the task force deliberation has been to ensure consistency between performance and accuracy runs. This issue was resolved by adding a new compliance test that verifies accuracy while running in the performance mode. 

**Accuracy mode (high reasoning effort)**

To ensure the benchmark sticks to a fair accuracy baseline, we curated a composite dataset requiring high reasoning effort.

- **Max output length:** **32,768 tokens**.
- **Evaluation strategy:** Pass @ 1 with k repeats.
- **Datasets:**

&nbsp;

- **AIME 2024:** Advanced mathematics problems. *Metric: Exact Match.*
- **LiveCodeBench v6:** Real-time coding tasks. *Metric: Pass/Fail.*
- **GPQA-Diamond:** Graduate-level science QA. *Metric: Correct/Not Correct.*

The evaluation and dataset curation was based on [OpenAI’s official evaluation scripts](https://github.com/openai/gpt-oss/tree/main/gpt_oss/evals). We created a feature branch ([feat/mlperf_integration](https://github.com/v-shobhit/gpt-oss/tree/feat/mlperf_integration)) that:

1.  Enabled inference on tokenized inputs (HarmonySampler), and
2.  Added evaluation for LiveCodeBench v6

To curate the accuracy dataset, we then collected input traces from running \`gpt_oss.evals\` and ran multiple times to get a reliable accuracy threshold on AIME25, LCB_V6 and GPQA_Diamond.

### Accuracy targets for GPT-OSS

To qualify for submission, implementations must meet or exceed the following accuracy targets on the curated accuracy dataset:

|  |  |  |  |
|----|----|----|----|
| **Dataset** | **Repeats per Sample** | **Accuracy Target** | **Evaluation Metric** |
| AIME 2024 | 8 | 82.92% | Exact Match (MCQ) |
| GPQA-Diamond | 5 | 74.95% | Correct/Not Correct |
| LiveCodeBench v6 | 3 | 84.68% | Pass/Fail (Code Execution) |

**Performance mode (low reasoning effort)**

For measuring pure inference speed (tokens/second), we utilize a dataset sampled from ccdv/pubmed-summarization.

- **Task:** PubMed health article summarization.
- **Configuration:** “Low reasoning effort” via Harmony format.
- **Sequence lengths:** Max output length is set to **10,240 tokens**.
- **Metrics:** Throughput and Latency.
- *Mean input sequence length:* 5,000 tokens
- *Mean output sequence length:* 1,250 tokens

![](https://mlcommons.org/wp-content/uploads/2026/03/image-6.png)

![](https://mlcommons.org/wp-content/uploads/2026/03/image-7.png)

### Performance metrics

The performance metrics evaluate the systems under strict latency constraints depending on the deployment scenario.

GPT-OSS constraints:

- **Interactive Scenario:** 99th percentile TTFT \<= 2.0s; TPOT \<= 15ms.
- **Server Scenario:** 99th percentile TTFT \<= 3.0s; TPOT \<= 80ms.

### Accuracy metrics

For **GPT-OSS**, accuracy is evaluated strictly on the accuracy mode dataset. AIME 2024 is evaluated via Exact Match, LiveCodeBench v6 via Code Execution (Pass/Fail), and GPQA-Diamond via Correct/Not Correct mapping.

### Compliance checks

Because this benchmark uses separate datasets for accuracy and performance evaluations, new compliance checks were introduced to ensure accuracy when running in performance modes. The tests are as follows:

1.  [TEST07](https://github.com/mlcommons/inference/tree/master/compliance/TEST07): This test verifies the accuracy of a performance run by using the GPQA dataset, one of the three accuracy datasets. Using all three datasets would be too computationally expensive, and the task force decided to use a subset for enforcing the accuracy verification.
2.  [TEST09](https://github.com/mlcommons/inference/tree/master/compliance/TEST09): This test verifies that the mean output length generated from the performance dataset is within 10% of the output length from reference implementation.  

### Reference implementation

The official reference implementations for the MLPerf Inference v6.0 benchmarks provide the necessary code and instructions to run the end-to-end evaluations.

- **GPT-OSS 120B:** [GitHub link](https://github.com/mlcommons/inference/tree/master/language/gpt-oss-120b)

## A new workload: the DeepSeek-R1 interactive scenario

Building on the DeepSeek-R1 benchmark introduced in v5.1, we added an interactive scenario designed to represent the growing demand for low-latency responses in advanced reasoning uses cases like math, knowledge and reasoning, and complex coding tasks. The dataset (LiveCodeBench, MATH500, AIME, GPQA-Diamond, and MMLU-Pro) remains identical to the server scenario, with a minimum query count of 4,388, but the workload shifts to tighter bounded response times than server scenario.

### Performance metrics

The performance metrics evaluate the systems under strict latency constraints depending on the deployment scenario.

DeepSeek-R1 Interactive Constraints & Speculative Decoding:

- **New interactive scenario (Poisson arrival):** 99th percentile TTFT \<= 1.5s; TPOT \<= 15ms.
- (Existing) server scenario (Poisson arrival): 99th percentile TTFT \<= 2s, TPOT \<= 80ms.

To meet the demanding latency requirements of the DeepSeek-R1 Interactive scenario, we are enabling **speculative decoding** for this specific workload. Implementations must use the official DeepSeek-R1 MTP (Multi-Token Prediction) Head with EAGLE-style decoding:

- **Algorithm:** EAGLE-style decoding with deepseek-ai/deepseek-r1 MTP head.
- **Configuration:** speculative-num-steps=3, speculative-eagle-topk=1.0.
- **Prohibitions:** Implementations cannot artificially manipulate acceptance rates. Techniques such as continued pre-training of the MTP head, quantization of the MTP head weights, or post-training adjustments (fine-tuning, RLHF) are strictly disallowed.
- See official rules here: [mlperf-inference/policies](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc#appendix-c-speculative-decoding)

### Accuracy metrics

For **DeepSeek-R1 interactive**, the accuracy metrics remain identical to the v5.1 server submission (exact match for math/QA and code execution for LiveCodeBench), ensuring the speculative decoding implementation does not degrade the model’s reasoning capabilities.

### Reference implementation

The official reference implementations for the MLPerf Inference v6.0 benchmarks provide the necessary code and instructions to run the end-to-end evaluations.

- **DeepSeek-R1:** [GitHub link](https://github.com/mlcommons/inference/tree/master/language/deepseek-r1)

## Conclusion

With MLPerf Inference v6.0, we continue to push the boundaries of what a standardized benchmark suite can measure. By introducing a split-dataset approach for GPT-OSS and a rigorous, latency-constrained Interactive scenario for DeepSeek-R1, we are providing the industry with the tools needed to evaluate the next generation of AI applications—from high-throughput summarization to real-time agentic reasoning.

We invite the community to explore the reference implementations and to participate in future rounds as we continue to track the rapid evolution of large language models.

For additional information on MLCommons and details on becoming a member, please visit [MLCommons.org](https://mlcommons.org/) or email [\[email protected\]](/cdn-cgi/l/email-protection#74041506001d171d0415001d1b1a341918171b19191b1a075a1b0613).

Category

[MLPerf Inference](https://mlcommons.org/category/mlperf-inference/) [News](https://mlcommons.org/category/news/)

------------------------------------------------------------------------

Authors

Viraat Chandra (Taskforce Chair, NVIDIA) Shobhit Verma (GPT-OSS Lead, NVIDIA) Zhihan Jiang, (NVIDIA) Miro Hodak (AMD) Uma Kannikati (AMD) Rebecca Lee (AMD) Yamini Kamisetty (AMD) Tom St. John (Gimlet Labs)

------------------------------------------------------------------------

Share

- [Share via email ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIj4KICAgICAgICAgICAgICA8cGF0aCBkPSJNMyAzSDIxQzIxLjU1MjMgMyAyMiAzLjQ0NzcyIDIyIDRWMjBDMjIgMjAuNTUyMyAyMS41NTIzIDIxIDIxIDIxSDNDMi40NDc3MiAyMSAyIDIwLjU1MjMgMiAyMFY0QzIgMy40NDc3MiAyLjQ0NzcyIDMgMyAzWk0yMCA3LjIzNzkyTDEyLjA3MTggMTQuMzM4TDQgNy4yMTU5NFYxOUgyMFY3LjIzNzkyWk00LjUxMTQ2IDVMMTIuMDYxOSAxMS42NjJMMTkuNTAxIDVINC41MTE0NloiIGZpbGw9IiMxMTE0MUYiIC8+CiAgICAgICAgICAgIDwvc3ZnPg==)](/cdn-cgi/l/email-protection#90afe3e5f2faf5f3e4add3f8f5f3fbbbffe5e4bbe4f8f9e3bbe0ffe3e4bbf6e2fffdbbdddcd3fffdfdfffee3b5a3d1bbd1bbfef5e7bbd7c0c4bddfc3c3bbf2f5fef3f8fdf1e2fbbbf1fef4bbd4f5f5e0c3f5f5fbbbc2a1bbe5e0f4f1e4f5e3bbf6ffe2bbfcf1e4f5fef3e9bdffe0e4f9fdf9eaf5f4bbe2f5f1e3fffef9fef7b6f2fff4e9adc2f5f1f4bbe4f8f5bbf1e2e4f9f3fcf5bbfffebbfdfcf3fffdfdfffee3beffe2f7bbf8f5e2f5b5a3d1bbf8e4e4e0e3b5a3d1b5a2d6b5a2d6fdfcf3fffdfdfffee3beffe2f7b5a2d6a2a0a2a6b5a2d6a0a3b5a2d6fdfce0f5e2f6bdf9fef6f5e2f5fef3f5bdf7e0e4bdffe3e3b5a2d6)
- [Share on facebook ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIj4KICAgICAgICAgICAgICA8cGF0aCBkPSJNMTQgMTMuNUgxNi41TDE3LjUgOS41SDE0VjcuNUMxNCA2LjQ3MDYyIDE0IDUuNSAxNiA1LjVIMTcuNVYyLjE0MDFDMTcuMTc0MyAyLjA5Njg1IDE1Ljk0MyAyIDE0LjY0MjkgMkMxMS45Mjg0IDIgMTAgMy42NTY4NiAxMCA2LjY5OTcxVjkuNUg3VjEzLjVIMTBWMjJIMTRWMTMuNVoiIGZpbGw9IiMxMTE0MUYiIC8+CiAgICAgICAgICAgIDwvc3ZnPg==)](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fmlcommons.org%2F2026%2F03%2Fmlperf-inference-gpt-oss%2F)
- [Share LinkedIn ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIj4KICAgICAgICAgICAgICA8cGF0aCBkPSJNNi45NDE0NiA0Ljk5OTkzQzYuOTQxMDkgNS44MTQyNCA2LjQ0NzA2IDYuNTQ3MDIgNS42OTIzMiA2Ljg1MjczQzQuOTM3NTggNy4xNTg0NSA0LjA3Mjg1IDYuOTc2MDUgMy41MDU4OCA2LjM5MTU1QzIuOTM4OTEgNS44MDcwNCAyLjc4MjkzIDQuOTM3MTUgMy4xMTE0OCA0LjE5MjA3QzMuNDQwMDQgMy40NDY5OSA0LjE4NzUyIDIuOTc1NSA1LjAwMTQ2IDIuOTk5OTNDNi4wODI1MyAzLjAzMjM4IDYuOTQxOTUgMy45MTgzNyA2Ljk0MTQ2IDQuOTk5OTNaTTcuMDAxNDYgOC40Nzk5M0gzLjAwMTQ2VjIwLjk5OTlINy4wMDE0NlY4LjQ3OTkzWk0xMy4zMjE1IDguNDc5OTNIOS4zNDE0NlYyMC45OTk5SDEzLjI4MTVWMTQuNDI5OUMxMy4yODE1IDEwLjc2OTkgMTguMDUxNSAxMC40Mjk5IDE4LjA1MTUgMTQuNDI5OVYyMC45OTk5SDIyLjAwMTVWMTMuMDY5OUMyMi4wMDE1IDYuODk5OTMgMTQuOTQxNSA3LjEyOTkzIDEzLjI4MTUgMTAuMTU5OUwxMy4zMjE1IDguNDc5OTNaIiBmaWxsPSIjMTExNDFGIiAvPgogICAgICAgICAgICA8L3N2Zz4=)](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fmlcommons.org%2F2026%2F03%2Fmlperf-inference-gpt-oss%2F&title=A+new+GPT-OSS+benchmark+and+DeepSeek+R1+updates+for+latency-optimized+reasoning)
- [Share on X ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIj4KICAgICAgICAgICAgICA8cGF0aCBkPSJNMTguMjA0OCAyLjI1SDIxLjUxMjhMMTQuMjg1OCAxMC41MUwyMi43ODc4IDIxLjc1SDE2LjEzMDhMMTAuOTE2OCAxNC45MzNMNC45NTA4NCAyMS43NUgxLjY0MDg0TDkuMzcwODQgMTIuOTE1TDEuMjE0ODQgMi4yNUg4LjA0MDg0TDEyLjc1MzggOC40ODFMMTguMjA0OCAyLjI1Wk0xNy4wNDM4IDE5Ljc3SDE4Ljg3NjhMNy4wNDQ4NCA0LjEyNkg1LjA3Nzg0TDE3LjA0MzggMTkuNzdaIiBmaWxsPSIjMTExNDFGIiAvPgogICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?text=A+new+GPT-OSS+benchmark+and+DeepSeek+R1+updates+for+latency-optimized+reasoning&url=https%3A%2F%2Fmlcommons.org%2F2026%2F03%2Fmlperf-inference-gpt-oss%2F)
- [Copy link ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iY29weS10ZXh0X19jb3B5IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIj4KICAgICAgICAgICAgICA8cGF0aCBkPSJNMTguMzY0MyAxNS41MzU2TDE2Ljk1MDEgMTQuMTIxNEwxOC4zNjQzIDEyLjcwNzJDMjAuMzE2OSAxMC43NTQ2IDIwLjMxNjkgNy41ODg3MiAxOC4zNjQzIDUuNjM2MUMxNi40MTE3IDMuNjgzNDcgMTMuMjQ1OCAzLjY4MzQ3IDExLjI5MzIgNS42MzYxTDkuODc4OTggNy4wNTAzMUw4LjQ2NDc3IDUuNjM2MUw5Ljg3ODk4IDQuMjIxODhDMTIuNjEyNyAxLjQ4ODIxIDE3LjA0NDggMS40ODgyMSAxOS43Nzg1IDQuMjIxODhDMjIuNTEyMiA2Ljk1NTU1IDIyLjUxMjIgMTEuMzg3NyAxOS43Nzg1IDE0LjEyMTRMMTguMzY0MyAxNS41MzU2Wk0xNS41MzU4IDE4LjM2NDFMMTQuMTIxNiAxOS43NzgzQzExLjM4OCAyMi41MTE5IDYuOTU1OCAyMi41MTE5IDQuMjIyMTMgMTkuNzc4M0MxLjQ4ODQ2IDE3LjA0NDYgMS40ODg0NiAxMi42MTI0IDQuMjIyMTMgOS44Nzg3NEw1LjYzNjM0IDguNDY0NTJMNy4wNTA1NiA5Ljg3ODc0TDUuNjM2MzQgMTEuMjkzQzMuNjgzNzIgMTMuMjQ1NiAzLjY4MzcyIDE2LjQxMTQgNS42MzYzNCAxOC4zNjQxQzcuNTg4OTYgMjAuMzE2NyAxMC43NTQ4IDIwLjMxNjcgMTIuNzA3NCAxOC4zNjQxTDE0LjEyMTYgMTYuOTQ5OEwxNS41MzU4IDE4LjM2NDFaTTE0LjgyODcgNy43NTc0MkwxNi4yNDMgOS4xNzE2M0w5LjE3MTg4IDE2LjI0MjdMNy43NTc2NiAxNC44Mjg1TDE0LjgyODcgNy43NTc0MloiIGZpbGw9IiMxMTE0MUYiIC8+CiAgICAgICAgICAgIDwvc3ZnPg==) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iY29weS10ZXh0X19jaGVjayIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiPjxwYXRoIGQ9Ik05Ljk5OTcgMTUuMTcwOUwxOS4xOTIxIDUuOTc4NTJMMjAuNjA2MyA3LjM5MjczTDkuOTk5NyAxNy45OTkzTDMuNjM1NzQgMTEuNjM1NEw1LjA0OTk2IDEwLjIyMTJMOS45OTk3IDE1LjE3MDlaIiAvPjwvc3ZnPg==)]()

------------------------------------------------------------------------

#### Related Insights

[![](https://mlcommons.org/wp-content/uploads/2026/09/stoarge3blog.svg)](https://mlcommons.org/2026/09/mlperf-storage-v3-0-results/)

### [MLCommons Releases New MLPerf Storage v3.0 Benchmark Results](https://mlcommons.org/2026/09/mlperf-storage-v3-0-results/)

News September 1, 2026

[![](https://mlcommons.org/wp-content/uploads/2026/08/6.png)](https://mlcommons.org/2026/08/double-blind-reliability-evaluation/)

### [The key to trustworthy AI evaluation is secrecy by design](https://mlcommons.org/2026/08/double-blind-reliability-evaluation/)

News August 27, 2026

[![](https://mlcommons.org/wp-content/uploads/2026/08/end2end2.svg)](https://mlcommons.org/2026/08/endtoend-inference/)

### [Introducing the MLPerf End-to-End RAG Inference Benchmark](https://mlcommons.org/2026/08/endtoend-inference/)

News August 26, 2026

[![](https://mlcommons.org/wp-content/uploads/2026/08/client2blog.svg)](https://mlcommons.org/2026/08/mlperf-client-v2-0/)

### [MLPerf Client v2.0 Expands AI PC Benchmarking with Image Generation and Agentic AI](https://mlcommons.org/2026/08/mlperf-client-v2-0/)

News August 18, 2026

[View All](https://mlcommons.org/category/mlperf-inference/)
