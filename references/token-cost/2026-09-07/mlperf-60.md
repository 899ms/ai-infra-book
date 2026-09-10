<!-- 从 mlperf-60.html 迁移的资料快照；原始 HTML SHA-256: d3c96e77d8a27054a137f3f427af17991d0dc7a2e66911fd95bae022c513c8c7。 -->

Insights

# MLCommons Releases New MLPerf Inference v6.0 Benchmark Results

The most significant update to the benchmark suite to date, with new tests ensuring that it remains the most comprehensive measure of AI system performance

April 1, 2026

![](https://mlcommons.org/wp-content/uploads/2026/04/INF6BLOGHERO.svg)

Today, MLCommons^(®) announced new results for its industry-standard MLPerf^(®) Inference v6.0 benchmark suite. This release includes several important advances that ensure the benchmark suite tests current, real-world scenarios for AI deployments and delivers a comprehensive picture of AI system performance.

Five of the eleven datacenter tests in MLPerf Inference v6.0 are new or updated, and the release also includes a new object-detection test for edge systems. The major changes include:

●      A new, open-weight large-language model [benchmark](https://mlcommons.org/2026/03/mlperf-inference-gpt-oss/) based on GPT-OSS 120B that can be used for mathematics, scientific reasoning, and coding;

●      An expanded DeepSeek-R1 advanced-reasoning [benchmark](https://mlcommons.org/2026/03/mlperf-inference-gpt-oss/), including an interactive scenario that permits speculative decoding;

●      DLRMv3, the third generation of our recommender [benchmark](https://mlcommons.org/2026/02/dlrmv3-inference-meta/) and now the first sequential recommendation benchmark test in the suite, which is thoroughly modernized based on generous engineering contributions from Meta, a world leader in recommender systems;

●      The suite’s first text-to-video generation [benchmark](https://mlcommons.org/2026/03/texttovideo-inference/);

●      A new vision-language model (VLM) [benchmark](https://mlcommons.org/2026/02/vlm-inference-shopify/) that transforms unstructured multimodal data from Shopify’s extensive product Catalog into structured metadata;

●      An upgraded single-shot object detection [benchmark](https://mlcommons.org/2026/03/yolo-inference/) for edge scenarios based on Ultralytics’ YOLOv11 Large model.

“This is the most significant revision of the Inference benchmark suite that we’ve ever done,” said Frank Han, Technical Staff, Systems Development Engineering at Dell Technologies and MLPerf Inference Working Group Co-chair. “The decision to update so many benchmarks in this round was prompted by the extraordinary enthusiasm and collaboration from our members, who contributed an unprecedented amount of engineering effort and IP toward building new inference benchmarks. Adding these new tests allows MLPerf Inference to better keep pace with the breakneck pace of evolution in AI models and techniques so that our benchmarks are relevant and representative of real-world deployments.”

The open-source MLPerf Inference benchmark suite measures system performance in an architecture-neutral, representative, and reproducible manner. The goal is to create a level playing field for competition that drives innovation, performance, and energy efficiency for the entire industry. The published results provide critical technical information for customers who are procuring and tuning AI systems. 

“We thank Meta, Shopify and Ultralytics for their substantial collaboration with us in making these changes to the MLPerf Inference benchmark suite and for contributing their datasets, task definitions and expertise,” said Miro Hodak, Senior Member of Technical Staff at AMD and MLPerf Inference Working Group Co-chair. “These partnerships were essential in ensuring that the tests include scenarios and workloads that represent the current state of the industry.”

“MLPerf Inference benchmarks play a vital role in driving transparency and accountability across the AI industry,” said Glenn Jocher, CEO & Founder of Ultralytics. “At Ultralytics, rigorous, reproducible benchmarking is central to how we develop and validate our Ultralytics YOLO models — ensuring developers and organizations can make informed decisions about real-world performance. We’re proud to be part of an ecosystem that holds the entire field to a higher standard.”  
  
“Commerce is one of the most complex domains in AI, yet researchers rarely have data that reflects that complexity,” said Kshetrajna Raghavan, Principal Engineer, Applied ML at Shopify. “Shopify is uniquely positioned to address this, sitting at the intersection of millions of merchants and billions of products. Sharing this taxonomy allows the whole field to evolve.”

**New tools for submitters and consumers**

With Inference 6.0, submitters have the option to use a newly available harness to complete benchmark tests. The new system, LoadGen++, allows LLMs to run with a serving-style software stack, which is familiar from typical deployments today. “LoadGen++ is a significant upgrade from its predecessor, and represents an important investment by MLCommons that will allow us to stay nimble as we continue to produce benchmark tests that track the state of the art,” said Han.

In addition, the Inference 6.0 results can be viewed in a [new online dashboard](https://mlcommons.org/visualizer) on the MLCommons site. The dashboard brings new levels of interactivity to viewing results, including advanced filtering and customized performance graphs.

**Large-scale, multi-node systems gaining attention **

The submissions to Inference 6.0 demonstrate that technology providers want to showcase the performance of scaled-up, multi-node systems running real-world inference workloads. This round recorded a new high for multi-node system submissions, a 30% increase over the Inference 5.1 benchmark six months ago. Moreover, 10% of all of the submitted systems in Inference 6.0 had more than ten nodes, compared to only 2% in the previous round. The largest system submitted in Inference 6.0 featured 72 nodes and 288 accelerators, quadrupling the number of nodes in the largest system in the previous round. 

“As more AI applications have moved into production and wide availability, the demand for large-scale, high-performance systems to run them has grown,” says Hodak. “At the same time, multi-node systems bring a unique set of technical challenges beyond those of single-node systems, requiring configuration and optimization of system architectures, network interconnects, data storage, and software layers. Stakeholders are eagerly stepping up to meet these challenges and run inference workloads at scale.”

**The AI community continues to embrace and invest in MLPerf Inference**

The MLPerf Inference 6.0 benchmark received submissions from a total of 24 participating organizations: AMD, ASUSTeK, Cisco, CoreWeave, Dell, GATEOverflow, GigaComputing, Google, Hewlett Packard Enterprise, Intel, Inventec Corporation, KRAI, Lambda, Lenovo, MangoBoost, MiTAC, Nebius, Netweb Technologies India Limited, NVIDIA, Oracle, Quanta Cloud Technology, Red Hat, Stevens Institute of Technology, and Supermicro. 

“I would like to welcome our first-time submitters, Inventec Corporation, Netweb Technologies India Limited, and Stevens Institute of Technology,” said Han. “The AI ecosystem is large and diverse, and it continues to grow and evolve rapidly. On behalf of MLCommons, I want to also thank our members, our contributors, and our partners including Meta, Shopify, and Ultralytics, for collaborating with us to build and shepherding forward the most comprehensive and relevant performance benchmark suite for AI inference. Together, we are ensuring that stakeholders in our community have valuable, real-world information that helps them to make better decisions.”

**View the results**

To view the results for MLPerf Inference v6.0, please visit the [Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) and [Edge](https://mlcommons.org/benchmarks/inference-edge/) benchmark results pages. For an interactive view of datacenter results, access the new benchmark results dashboard: <https://mlcommons.org/visualizer>. 

**About MLCommons**

MLCommons is the world’s leader in AI benchmarking. An open engineering consortium supported by over 130 members and affiliates, MLCommons has a proven record of bringing together academia, industry, and civil society to measure and improve AI. The foundation for MLCommons began with the MLPerf benchmarks in 2018, which rapidly grew into a set of industry metrics for measuring machine learning performance and promoting transparency in machine learning techniques. Since then, MLCommons has continued to use collective engineering to build the benchmarks and metrics required for better AI – ultimately helping to evaluate and improve the accuracy, safety, speed, and efficiency of AI technologies.

For additional information on MLCommons and details on becoming a member, please visit [MLCommons.org](https://mlcommons.org/) or email [\[email protected\]](/cdn-cgi/l/email-protection#cebeafbcbaa7ada7beafbaa7a1a08ea3a2ada1a3a3a1a0bde0a1bca9).

Press Inquiries: contact [\[email protected\]](/cdn-cgi/l/email-protection)

Category

[MLPerf Inference](https://mlcommons.org/category/mlperf-inference/)

------------------------------------------------------------------------

Authors

ML Commons

------------------------------------------------------------------------

Share

- [Share via email ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIj4KICAgICAgICAgICAgICA8cGF0aCBkPSJNMyAzSDIxQzIxLjU1MjMgMyAyMiAzLjQ0NzcyIDIyIDRWMjBDMjIgMjAuNTUyMyAyMS41NTIzIDIxIDIxIDIxSDNDMi40NDc3MiAyMSAyIDIwLjU1MjMgMiAyMFY0QzIgMy40NDc3MiAyLjQ0NzcyIDMgMyAzWk0yMCA3LjIzNzkyTDEyLjA3MTggMTQuMzM4TDQgNy4yMTU5NFYxOUgyMFY3LjIzNzkyWk00LjUxMTQ2IDVMMTIuMDYxOSAxMS42NjJMMTkuNTAxIDVINC41MTE0NloiIGZpbGw9IiMxMTE0MUYiIC8+CiAgICAgICAgICAgIDwvc3ZnPg==)](/cdn-cgi/l/email-protection#5e612d2b3c343b3d2a631d363b3d3575312b2a752a36372d752e312d2a75382c31337513121d31333331302d7b6d1f7513121d31333331302d750c3b323b3f2d3b2d75103b297513120e3b2c38751730383b2c3b303d3b752868706e751c3b303d36333f2c35750c3b2d2b322a2d783c313a27630c3b3f3a752a363b753f2c2a373d323b7531307533323d31333331302d70312c3975363b2c3b7b6d1f75362a2a2e2d7b6d1f7b6c187b6c1833323d31333331302d70312c397b6c186c6e6c687b6c186e6a7b6c1833322e3b2c38733730383b2c3b303d3b732868736e732c3b2d2b322a2d7b6c18)
- [Share on facebook ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIj4KICAgICAgICAgICAgICA8cGF0aCBkPSJNMTQgMTMuNUgxNi41TDE3LjUgOS41SDE0VjcuNUMxNCA2LjQ3MDYyIDE0IDUuNSAxNiA1LjVIMTcuNVYyLjE0MDFDMTcuMTc0MyAyLjA5Njg1IDE1Ljk0MyAyIDE0LjY0MjkgMkMxMS45Mjg0IDIgMTAgMy42NTY4NiAxMCA2LjY5OTcxVjkuNUg3VjEzLjVIMTBWMjJIMTRWMTMuNVoiIGZpbGw9IiMxMTE0MUYiIC8+CiAgICAgICAgICAgIDwvc3ZnPg==)](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fmlcommons.org%2F2026%2F04%2Fmlperf-inference-v6-0-results%2F)
- [Share LinkedIn ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIj4KICAgICAgICAgICAgICA8cGF0aCBkPSJNNi45NDE0NiA0Ljk5OTkzQzYuOTQxMDkgNS44MTQyNCA2LjQ0NzA2IDYuNTQ3MDIgNS42OTIzMiA2Ljg1MjczQzQuOTM3NTggNy4xNTg0NSA0LjA3Mjg1IDYuOTc2MDUgMy41MDU4OCA2LjM5MTU1QzIuOTM4OTEgNS44MDcwNCAyLjc4MjkzIDQuOTM3MTUgMy4xMTE0OCA0LjE5MjA3QzMuNDQwMDQgMy40NDY5OSA0LjE4NzUyIDIuOTc1NSA1LjAwMTQ2IDIuOTk5OTNDNi4wODI1MyAzLjAzMjM4IDYuOTQxOTUgMy45MTgzNyA2Ljk0MTQ2IDQuOTk5OTNaTTcuMDAxNDYgOC40Nzk5M0gzLjAwMTQ2VjIwLjk5OTlINy4wMDE0NlY4LjQ3OTkzWk0xMy4zMjE1IDguNDc5OTNIOS4zNDE0NlYyMC45OTk5SDEzLjI4MTVWMTQuNDI5OUMxMy4yODE1IDEwLjc2OTkgMTguMDUxNSAxMC40Mjk5IDE4LjA1MTUgMTQuNDI5OVYyMC45OTk5SDIyLjAwMTVWMTMuMDY5OUMyMi4wMDE1IDYuODk5OTMgMTQuOTQxNSA3LjEyOTkzIDEzLjI4MTUgMTAuMTU5OUwxMy4zMjE1IDguNDc5OTNaIiBmaWxsPSIjMTExNDFGIiAvPgogICAgICAgICAgICA8L3N2Zz4=)](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fmlcommons.org%2F2026%2F04%2Fmlperf-inference-v6-0-results%2F&title=MLCommons+Releases+New+MLPerf+Inference+v6.0+Benchmark+Results)
- [Share on X ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIj4KICAgICAgICAgICAgICA8cGF0aCBkPSJNMTguMjA0OCAyLjI1SDIxLjUxMjhMMTQuMjg1OCAxMC41MUwyMi43ODc4IDIxLjc1SDE2LjEzMDhMMTAuOTE2OCAxNC45MzNMNC45NTA4NCAyMS43NUgxLjY0MDg0TDkuMzcwODQgMTIuOTE1TDEuMjE0ODQgMi4yNUg4LjA0MDg0TDEyLjc1MzggOC40ODFMMTguMjA0OCAyLjI1Wk0xNy4wNDM4IDE5Ljc3SDE4Ljg3NjhMNy4wNDQ4NCA0LjEyNkg1LjA3Nzg0TDE3LjA0MzggMTkuNzdaIiBmaWxsPSIjMTExNDFGIiAvPgogICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?text=MLCommons+Releases+New+MLPerf+Inference+v6.0+Benchmark+Results&url=https%3A%2F%2Fmlcommons.org%2F2026%2F04%2Fmlperf-inference-v6-0-results%2F)
- [Copy link ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iY29weS10ZXh0X19jb3B5IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIj4KICAgICAgICAgICAgICA8cGF0aCBkPSJNMTguMzY0MyAxNS41MzU2TDE2Ljk1MDEgMTQuMTIxNEwxOC4zNjQzIDEyLjcwNzJDMjAuMzE2OSAxMC43NTQ2IDIwLjMxNjkgNy41ODg3MiAxOC4zNjQzIDUuNjM2MUMxNi40MTE3IDMuNjgzNDcgMTMuMjQ1OCAzLjY4MzQ3IDExLjI5MzIgNS42MzYxTDkuODc4OTggNy4wNTAzMUw4LjQ2NDc3IDUuNjM2MUw5Ljg3ODk4IDQuMjIxODhDMTIuNjEyNyAxLjQ4ODIxIDE3LjA0NDggMS40ODgyMSAxOS43Nzg1IDQuMjIxODhDMjIuNTEyMiA2Ljk1NTU1IDIyLjUxMjIgMTEuMzg3NyAxOS43Nzg1IDE0LjEyMTRMMTguMzY0MyAxNS41MzU2Wk0xNS41MzU4IDE4LjM2NDFMMTQuMTIxNiAxOS43NzgzQzExLjM4OCAyMi41MTE5IDYuOTU1OCAyMi41MTE5IDQuMjIyMTMgMTkuNzc4M0MxLjQ4ODQ2IDE3LjA0NDYgMS40ODg0NiAxMi42MTI0IDQuMjIyMTMgOS44Nzg3NEw1LjYzNjM0IDguNDY0NTJMNy4wNTA1NiA5Ljg3ODc0TDUuNjM2MzQgMTEuMjkzQzMuNjgzNzIgMTMuMjQ1NiAzLjY4MzcyIDE2LjQxMTQgNS42MzYzNCAxOC4zNjQxQzcuNTg4OTYgMjAuMzE2NyAxMC43NTQ4IDIwLjMxNjcgMTIuNzA3NCAxOC4zNjQxTDE0LjEyMTYgMTYuOTQ5OEwxNS41MzU4IDE4LjM2NDFaTTE0LjgyODcgNy43NTc0MkwxNi4yNDMgOS4xNzE2M0w5LjE3MTg4IDE2LjI0MjdMNy43NTc2NiAxNC44Mjg1TDE0LjgyODcgNy43NTc0MloiIGZpbGw9IiMxMTE0MUYiIC8+CiAgICAgICAgICAgIDwvc3ZnPg==) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iY29weS10ZXh0X19jaGVjayIgdmlld2JveD0iMCAwIDI0IDI0IiBmaWxsPSJjdXJyZW50Q29sb3IiPjxwYXRoIGQ9Ik05Ljk5OTcgMTUuMTcwOUwxOS4xOTIxIDUuOTc4NTJMMjAuNjA2MyA3LjM5MjczTDkuOTk5NyAxNy45OTkzTDMuNjM1NzQgMTEuNjM1NEw1LjA0OTk2IDEwLjIyMTJMOS45OTk3IDE1LjE3MDlaIiAvPjwvc3ZnPg==)]()

------------------------------------------------------------------------

#### Related Insights

[![](https://mlcommons.org/wp-content/uploads/2026/08/end2end2.svg)](https://mlcommons.org/2026/08/endtoend-inference/)

### [Introducing the MLPerf End-to-End RAG Inference Benchmark](https://mlcommons.org/2026/08/endtoend-inference/)

News August 26, 2026

[![](https://mlcommons.org/wp-content/uploads/2026/07/Edge-Agentic-Inference-Blog-Hero-400-x-300-px.svg)](https://mlcommons.org/2026/07/mlperf-inference-v61-edge-agentic/)

### [Call for Submission: Edge Agentic Inference Benchmark for MLPerf Inference v6.1](https://mlcommons.org/2026/07/mlperf-inference-v61-edge-agentic/)

Blog July 9, 2026

[![](https://mlcommons.org/wp-content/uploads/2026/07/Agentic-Inference-Blog-Image-Option-B.svg)](https://mlcommons.org/2026/07/agentic-inference-for-mlperf-inference/)

### [Agentic Inference for MLPerf Inference](https://mlcommons.org/2026/07/agentic-inference-for-mlperf-inference/)

News July 8, 2026

[![](https://mlcommons.org/wp-content/uploads/2026/03/sazzzz.svg)](https://mlcommons.org/2026/03/mlperf-inference-gpt-oss/)

### [A new GPT-OSS benchmark and DeepSeek R1 updates for latency-optimized reasoning](https://mlcommons.org/2026/03/mlperf-inference-gpt-oss/)

News March 24, 2026

[View All](https://mlcommons.org/category/mlperf-inference/)
