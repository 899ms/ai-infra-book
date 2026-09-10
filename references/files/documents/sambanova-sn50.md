<!-- 从 sambanova-sn50.html 迁移的资料快照；原始 HTML SHA-256: 2c40f22553a419309f5e9a6df1ebfdac34546c4fd95905331c9d66d4c40cd50b。 -->

[![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzNyIgaGVpZ2h0PSI2NyIgdmlld2JveD0iMCAwIDM3IDY3Ij4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBkPSJNMzMuMzIgMyAzIDMzLjMybDMwLjMyIDMwLjMyNiIgc3Ryb2tlPSIjZmZmZmZmIiBzdHJva2Utd2lkdGg9IjUuNzQ1IiBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgLz4KICAgICAgICAgICAgICAgICAgPC9zdmc+)BACK TO RESOURCES](/resources)

[Blog](/resources/tag/blog)

# Hot Chips 2026: Dataflow at Scale

By **Raghu Prabhakar, Chief Architect, SambaNova**

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTMiIGhlaWdodD0iMTUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDQ0OCA1MTIiPjxwYXRoIGZpbGw9ImN1cnJlbnRDb2xvciIgZD0iTTQwMCA2NGgtNDhWMTJjMC02LjYyNy01LjM3My0xMi0xMi0xMmgtNDBjLTYuNjI3IDAtMTIgNS4zNzMtMTIgMTJ2NTJIMTYwVjEyYzAtNi42MjctNS4zNzMtMTItMTItMTJoLTQwYy02LjYyNyAwLTEyIDUuMzczLTEyIDEydjUySDQ4QzIxLjQ5IDY0IDAgODUuNDkgMCAxMTJ2MzUyYzAgMjYuNTEgMjEuNDkgNDggNDggNDhoMzUyYzI2LjUxIDAgNDgtMjEuNDkgNDgtNDhWMTEyYzAtMjYuNTEtMjEuNDktNDgtNDgtNDh6bS02IDQwMEg1NGE2IDYgMCAwIDEtNi02VjE2MGgzNTJ2Mjk4YTYgNiAwIDAgMS02IDZ6bS01Mi44NDktMjAwLjY1TDE5OC44NDIgNDA0LjUxOWMtNC43MDUgNC42NjctMTIuMzAzIDQuNjM3LTE2Ljk3MS0uMDY4bC03NS4wOTEtNzUuNjk5Yy00LjY2Ny00LjcwNS00LjYzNy0xMi4zMDMuMDY4LTE2Ljk3MWwyMi43MTktMjIuNTM2YzQuNzA1LTQuNjY3IDEyLjMwMy00LjYzNyAxNi45Ny4wNjlsNDQuMTA0IDQ0LjQ2MSAxMTEuMDcyLTExMC4xODFjNC43MDUtNC42NjcgMTIuMzAzLTQuNjM3IDE2Ljk3MS4wNjhsMjIuNTM2IDIyLjcxOGM0LjY2NyA0LjcwNSA0LjYzNiAxMi4zMDMtLjA2OSAxNi45N3oiIC8+PC9zdmc+) September 2, 2026

At Hot Chips 2026, the industry converged on a new bottleneck: AI is moving from one-shot answers to agents that reason, call tools, and keep working. That means far more generated tokens, and far more time spent in decode.

## **TL;DR**

- Agentic AI generates more tokens and spends most of inference in memory-bound decode, so system bandwidth matters more than peak compute.
- Across six frontier-model configs SambaNova analyzed, decode was 75% to 97% of model-inference time.
- Model Bandwidth Utilization (MBU) measures how much installed bandwidth actually moves weights and KV-cache: installed bandwidth times MBU equals tokens per second.
- The SN50 RDU pairs a dataflow execution model and 432 MB on-chip SRAM with scale-up and scale-out Ethernet to keep bandwidth productive across chips.
- Scaling modeled DeepSeek-R1 from 64 to 256 RDUs lifts per-user speed from 200 to 500 tokens per second (TPS) while MBU holds between 44% and 51%.

That shift makes the hardware challenge much more interesting. The next generation of inference will not be won with one big chip. Frontier models already span multiple chips, and their speed depends on how efficiently processors, memory, and networks operate as one system. A fast chip matters. A fast system matters more.

Our Hot Chips talk, “Dataflow at Scale: the SN50 RDU,” focused on that full-system problem: How much installed bandwidth reaches the model; how dataflow keeps work moving inside the [RDU](/products/rdu-ai-chips); and how the network preserves that efficiency as models scale across chips, nodes, and racks.

![Raghu at Hot Chips 2026](https://sambanova.ai/hs-fs/hubfs/Raghu%20at%20Hot%20Chips%202026.jpg?width=1620&height=1080&name=Raghu%20at%20Hot%20Chips%202026.jpg)

Raghu Prabhakar, Chief Architect at SambaNova, presents the SN50 RDU at Hot Chips 2026.

## From Peak Bandwidth to Useful Model Bandwidth

Previous SambaNova blogs explain [the decode bottleneck](/blog/agentic-inference-needs-hybrid-hardware) and why [disaggregated inference](/blog/understanding-disaggregated-inference) maps compute-heavy prefill to GPUs and memory-bound decode to RDUs. Our talk started with the metric that connects that architecture to delivered token speed: Model Bandwidth Utilization (MBU).

This idea is well-established, not new. The [MosaicML engineering team at Databricks](https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices) introduced MBU as achieved model-data bandwidth divided by a system’s peak memory bandwidth. Peak high bandwidth memory (HBM) tells you what the hardware could move. MBU tells you how much of that bandwidth is actually moving model weights and key-value (KV) cache data during token generation. For bandwidth-bound decode, installed bandwidth multiplied by MBU gives effective model bandwidth, which is the part that translates into tokens per second.

In the six frontier-model configurations SambaNova analyzed, decode represented 75% to 97% of model-inference time. At the high end, the DeepSeek-V3 case (8K input, 1K output, B300 FP4, and one active request) spent 97% of model-inference time in decode. The exact split varies by model, context, precision, and concurrency, but the system lesson is consistent: Peak compute alone does not predict the speed users will feel from an agent.

![Image 9-2-26 at 12.02 PM](https://sambanova.ai/hs-fs/hubfs/Image%209-2-26%20at%2012.02%20PM.png?width=1533&height=799&name=Image%209-2-26%20at%2012.02%20PM.png)

MBU connects peak HBM bandwidth to the model-data movement that drives token generation.  
Source: Raghu Prabhakar, Hot Chips 2026. Concept reference: MosaicML/Databricks.

This distinction gets more important as systems grow. Adding accelerators increases theoretical bandwidth, but per-user token speed will not rise with it if synchronization, memory traffic, or communication overhead drives utilization down. The goal is not simply more bandwidth. The goal is more bandwidth that the model can use.

## How Dataflow Turns Bandwidth into Tokens

The SN50 RDU starts with a dataflow execution model rather than a sequence of separately launched kernels. The compiler maps the model across a tiled mesh of compute and memory units. SN50’s 432 MB of distributed on-chip SRAM keeps frequently used data close to compute and allows intermediate values to flow between operations without repeated trips to HBM.

Persistent decoder execution and operator fusion keep the model moving across token steps instead of repeatedly stopping and resuming work at kernel boundaries. Double-buffered memory units begin moving the next model tile while the current computation runs. Collective communication can terminate in SRAM, avoiding unnecessary HBM traffic and allowing compute, memory access, and communication to overlap.

That overlap is the link between MBU and scale. Useful bandwidth is not a property of memory alone; it is the result of keeping the entire execution pipeline productive. Once a model spans multiple RDUs, the network becomes part of that pipeline.

## Inference at Scale Needs Scale-Up and Scale-Out

Dense frontier models and mixture-of-experts models span many accelerators. Their fabrics must carry frequent collectives and dynamic token movement without turning communication into the next bottleneck.

The SambaNova SN50 uses three connected network domains. Inside an eight-socket node, seven integrated 800G Ethernet links form a fully connected topology, which gives each RDU a direct path to other RDUs in the node. Beyond the node, two additional 800G ports per RDU connect to the inter-node scale-up fabric. Across those domains, the SN50 integrates ten 800G Ethernet ports with an aggregate 2 TB/s per RDU. In the 64-socket example, two 64-port 800G switches connect every node to both switches, with one link from every RDU going to each switch.

Scale-out has a different job. Each SN50 RDU uses a 400G RoCEv2 NIC to connect scale-up domains across a rail-optimized Ethernet network. This layer supports disaggregated inference and KV-cache transfer between scale-up domains. A separate front-end data center network remains available for hosts, storage, and management.

![Image 9-2-26 at 12.04 PM-1](https://sambanova.ai/hs-fs/hubfs/Image%209-2-26%20at%2012.04%20PM-1.png?width=1530&height=807&name=Image%209-2-26%20at%2012.04%20PM-1.png)

SN50 combines a fully connected eight-socket node, 800G inter-node scale-up, and a 400G RoCEv2 scale-out path between scale-up domains. Source: Raghu Prabhakar, Hot Chips 2026.

The separation matters because the traffic is different. Scale-up carries the tightly coupled communication required to split one model across RDUs. Scale-out connects larger domains and heterogeneous inference stages. Each tier is built around the communication pattern it has to sustain.

## Why Tensor and Expert Parallelism Need Different Network Behavior

Tensor parallelism splits large tensor operations across RDUs. Every step depends on collectives, such as reduce-scatter, all-gather, and all-reduce, so communication has to keep pace with matrix computation. The on-silicon tensor-parallel general matrix multiplication (GEMM) benchmark presented at Hot Chips achieved at least 70% TFLOPs utilization, the share of available floating-point compute kept productive, across 8, 16, and 32 SN50 sockets. At 32 sockets, the benchmark achieved full overlap of compute and communication. This is a scoped kernel result, not end-to-end model performance, but it shows the behavior the scale-up fabric is designed to preserve.

![Image 9-2-26 at 12.04 PM](https://sambanova.ai/hs-fs/hubfs/Image%209-2-26%20at%2012.04%20PM.png?width=1531&height=805&name=Image%209-2-26%20at%2012.04%20PM.png)

SN50’s on-silicon tensor-parallel GEMM benchmark achieved at least 70% TFLOPs utilization across 8, 16, and 32 sockets, with full compute-communication overlap at 32 sockets. Source: SambaNova on-silicon measurement presented by Raghu Prabhakar, Hot Chips 2026, slide 28.

Expert parallelism creates a different challenge. In a mixture-of-experts model, the router selects different experts for different tokens. Dispatch and combine therefore generate dynamic traffic whose destinations change with every batch. SN50 supports both all-to-all and broadcast-and-filter approaches. All-to-all filters at the source and avoids extra traffic, but produces non-uniform flows. Broadcast-and-filter creates more uniform traffic and can begin alongside router computation, at the cost of sending additional data.

![Image 9-2-26 at 12.06 PM](https://sambanova.ai/hs-fs/hubfs/Image%209-2-26%20at%2012.06%20PM.png?width=1412&height=794&name=Image%209-2-26%20at%2012.06%20PM.png)

 

In SambaNova’s 64-socket expert-parallel configuration, more than 70% of the bandwidth was used to load experts. Across both tensor and expert parallelism, bandwidth becomes performance when the execution model can overlap communication and match the network behavior to the traffic the model actually generates.

## Keeping MBU High as the System Grows

The scaling question is simple: Can more chips deliver more speed without giving back the useful bandwidth that made each chip fast?

Across SambaNova’s modeled DeepSeek-R1 8K-input/1K-output operating points, projected per-user speed rises from 200 to 300 to 500 tokens per second as the configuration scales from 64 to 128 to 256 SN50 RDUs. MBU remains at 51%, 44%, and 45%, respectively. These are modeled operating points, not measured production results, and outcomes will vary by workload. They illustrate the design target: Increase decode capacity while preserving a substantial share of useful model bandwidth.

![Image 9-2-26 at 12.07 PM](https://sambanova.ai/hs-fs/hubfs/Image%209-2-26%20at%2012.07%20PM.png?width=1506&height=782&name=Image%209-2-26%20at%2012.07%20PM.png)

  
  
More RDUs increase aggregate bandwidth, while dataflow with the scale-up fabric are designed to keep enough of that bandwidth productive for token speed to climb. Scaling is not only about fitting a larger model, it is about keeping the model moving.

## The Hot Chips Takeaway

The takeaway from Hot Chips 2026 is straightforward: Agentic inference is a systems problem. GPUs remain a strong fit for training and compute-bound prefill. RDUs are purpose-built for memory-bound decode. CPUs coordinate tools, APIs, vector databases, and actions around the model. The network lets many processors operate as one inference platform.

SambaNova has already shown what that hybrid architecture can deliver. At RAISE Summit 2026, a preview system using four NVIDIA H200 GPUs for prefill and 16 SN50 RDUs for decode reached 763 output tokens per second on MiniMax M2.7 with 10,000 input tokens in benchmarking by Artificial Analysis. SemiAnalysis later benchmarked [SambaRack](/products/sambarack) SN50 on the same model in two tensor-parallel configurations. Those results are covered in the [RAISE MiniMax blog post](/blog/sn50-runs-fastest-minimax-speeds-in-the-world) and [SemiAnalysis benchmark recap](/blog/semianalysis-benchmarks-sambarack-sn50-with-fast-inference-on-minimax-m2.7).

![Image 9-2-26 at 12.08 PM](https://sambanova.ai/hs-fs/hubfs/Image%209-2-26%20at%2012.08%20PM.png?width=1521&height=746&name=Image%209-2-26%20at%2012.08%20PM.png)

  
  
Peak bandwidth describes possibility. MBU shows how much of that possibility reaches the model. Our [Dataflow Architecture](/products/dataflow-architecture) keeps model data moving inside the RDU. Scale-up Ethernet carries tensor- and expert-parallel traffic; scale-out Ethernet carries KV-cache transfers and disaggregated inference traffic across domains. Put those pieces together, and the architecture is designed to give agentic AI fast tokens, while preserving useful bandwidth as models scale.

## FAQs

What is Model Bandwidth Utilization (MBU)?

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTUuMjkyODkgOC4yOTI4OUM0LjkwMjM3IDguNjgzNDIgNC45MDIzNyA5LjMxNjU4IDUuMjkyODkgOS43MDcxMUwxMS4yOTI5IDE1LjcwNzFDMTEuNjgzNCAxNi4wOTc2IDEyLjMxNjYgMTYuMDk3NiAxMi43MDcxIDE1LjcwNzFMMTguNzA3MSA5LjcwNzExQzE5LjA5NzYgOS4zMTY1OCAxOS4wOTc2IDguNjgzNDIgMTguNzA3MSA4LjI5Mjg5QzE4LjMxNjYgNy45MDIzNyAxNy42ODM0IDcuOTAyMzcgMTcuMjkyOSA4LjI5Mjg5TDEyIDEzLjU4NThMNi43MDcxMSA4LjI5Mjg5QzYuMzE2NTggNy45MDIzNyA1LjY4MzQyIDcuOTAyMzcgNS4yOTI4OSA4LjI5Mjg5WiIgZmlsbD0iY3VycmVudENvbG9yIiAvPgogICAgICAgICAgICAgICAgICA8L3N2Zz4=) ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTUuMjkyODkgMTUuNzA3MUM0LjkwMjM3IDE1LjMxNjYgNC45MDIzNyAxNC42ODM0IDUuMjkyODkgMTQuMjkyOUwxMS4yOTI5IDguMjkyODlDMTEuNjgzNCA3LjkwMjM3IDEyLjMxNjYgNy45MDIzNyAxMi43MDcxIDguMjkyODlMMTguNzA3MSAxNC4yOTI5QzE5LjA5NzYgMTQuNjgzNCAxOS4wOTc2IDE1LjMxNjYgMTguNzA3MSAxNS43MDcxQzE4LjMxNjYgMTYuMDk3NiAxNy42ODM0IDE2LjA5NzYgMTcuMjkyOSAxNS43MDcxTDEyIDEwLjQxNDJMNi43MDcxMSAxNS43MDcxQzYuMzE2NTggMTYuMDk3NiA1LjY4MzQyIDE2LjA5NzYgNS4yOTI4OSAxNS43MDcxWiIgZmlsbD0iY3VycmVudENvbG9yIiAvPgogICAgICAgICAgICAgICAgICA8L3N2Zz4=)

MBU is achieved model-data bandwidth divided by a system's peak memory bandwidth. It shows how much of a system's installed bandwidth is actually moving model weights and KV-cache data during token generation. For bandwidth-bound decode, installed bandwidth multiplied by MBU gives the effective bandwidth that translates into tokens per second.

Why does decode matter more than prefill for agentic inference?

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTUuMjkyODkgOC4yOTI4OUM0LjkwMjM3IDguNjgzNDIgNC45MDIzNyA5LjMxNjU4IDUuMjkyODkgOS43MDcxMUwxMS4yOTI5IDE1LjcwNzFDMTEuNjgzNCAxNi4wOTc2IDEyLjMxNjYgMTYuMDk3NiAxMi43MDcxIDE1LjcwNzFMMTguNzA3MSA5LjcwNzExQzE5LjA5NzYgOS4zMTY1OCAxOS4wOTc2IDguNjgzNDIgMTguNzA3MSA4LjI5Mjg5QzE4LjMxNjYgNy45MDIzNyAxNy42ODM0IDcuOTAyMzcgMTcuMjkyOSA4LjI5Mjg5TDEyIDEzLjU4NThMNi43MDcxMSA4LjI5Mjg5QzYuMzE2NTggNy45MDIzNyA1LjY4MzQyIDcuOTAyMzcgNS4yOTI4OSA4LjI5Mjg5WiIgZmlsbD0iY3VycmVudENvbG9yIiAvPgogICAgICAgICAgICAgICAgICA8L3N2Zz4=) ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTUuMjkyODkgMTUuNzA3MUM0LjkwMjM3IDE1LjMxNjYgNC45MDIzNyAxNC42ODM0IDUuMjkyODkgMTQuMjkyOUwxMS4yOTI5IDguMjkyODlDMTEuNjgzNCA3LjkwMjM3IDEyLjMxNjYgNy45MDIzNyAxMi43MDcxIDguMjkyODlMMTguNzA3MSAxNC4yOTI5QzE5LjA5NzYgMTQuNjgzNCAxOS4wOTc2IDE1LjMxNjYgMTguNzA3MSAxNS43MDcxQzE4LjMxNjYgMTYuMDk3NiAxNy42ODM0IDE2LjA5NzYgMTcuMjkyOSAxNS43MDcxTDEyIDEwLjQxNDJMNi43MDcxMSAxNS43MDcxQzYuMzE2NTggMTYuMDk3NiA1LjY4MzQyIDE2LjA5NzYgNS4yOTI4OSAxNS43MDcxWiIgZmlsbD0iY3VycmVudENvbG9yIiAvPgogICAgICAgICAgICAgICAgICA8L3N2Zz4=)

Agents reason, call tools, and keep working, which generates far more tokens. Decode is memory-bound, and in the six configurations SambaNova analyzed it accounted for 75% to 97% of model-inference time. Peak compute alone does not predict the token speed users feel.

How does the SN50 RDU scale across multiple chips?

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTUuMjkyODkgOC4yOTI4OUM0LjkwMjM3IDguNjgzNDIgNC45MDIzNyA5LjMxNjU4IDUuMjkyODkgOS43MDcxMUwxMS4yOTI5IDE1LjcwNzFDMTEuNjgzNCAxNi4wOTc2IDEyLjMxNjYgMTYuMDk3NiAxMi43MDcxIDE1LjcwNzFMMTguNzA3MSA5LjcwNzExQzE5LjA5NzYgOS4zMTY1OCAxOS4wOTc2IDguNjgzNDIgMTguNzA3MSA4LjI5Mjg5QzE4LjMxNjYgNy45MDIzNyAxNy42ODM0IDcuOTAyMzcgMTcuMjkyOSA4LjI5Mjg5TDEyIDEzLjU4NThMNi43MDcxMSA4LjI5Mjg5QzYuMzE2NTggNy45MDIzNyA1LjY4MzQyIDcuOTAyMzcgNS4yOTI4OSA4LjI5Mjg5WiIgZmlsbD0iY3VycmVudENvbG9yIiAvPgogICAgICAgICAgICAgICAgICA8L3N2Zz4=) ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTUuMjkyODkgMTUuNzA3MUM0LjkwMjM3IDE1LjMxNjYgNC45MDIzNyAxNC42ODM0IDUuMjkyODkgMTQuMjkyOUwxMS4yOTI5IDguMjkyODlDMTEuNjgzNCA3LjkwMjM3IDEyLjMxNjYgNy45MDIzNyAxMi43MDcxIDguMjkyODlMMTguNzA3MSAxNC4yOTI5QzE5LjA5NzYgMTQuNjgzNCAxOS4wOTc2IDE1LjMxNjYgMTguNzA3MSAxNS43MDcxQzE4LjMxNjYgMTYuMDk3NiAxNy42ODM0IDE2LjA5NzYgMTcuMjkyOSAxNS43MDcxTDEyIDEwLjQxNDJMNi43MDcxMSAxNS43MDcxQzYuMzE2NTggMTYuMDk3NiA1LjY4MzQyIDE2LjA5NzYgNS4yOTI4OSAxNS43MDcxWiIgZmlsbD0iY3VycmVudENvbG9yIiAvPgogICAgICAgICAgICAgICAgICA8L3N2Zz4=)

The SN50 uses three connected network domains. Inside an eight-socket node, seven integrated 800G Ethernet links form a fully connected topology. Two more 800G ports per RDU connect the inter-node scale-up fabric, and a 400G RoCEv2 NIC handles scale-out between scale-up domains, including KV-cache transfer for disaggregated inference.

Why do tensor and expert parallelism need different network behavior?

![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTUuMjkyODkgOC4yOTI4OUM0LjkwMjM3IDguNjgzNDIgNC45MDIzNyA5LjMxNjU4IDUuMjkyODkgOS43MDcxMUwxMS4yOTI5IDE1LjcwNzFDMTEuNjgzNCAxNi4wOTc2IDEyLjMxNjYgMTYuMDk3NiAxMi43MDcxIDE1LjcwNzFMMTguNzA3MSA5LjcwNzExQzE5LjA5NzYgOS4zMTY1OCAxOS4wOTc2IDguNjgzNDIgMTguNzA3MSA4LjI5Mjg5QzE4LjMxNjYgNy45MDIzNyAxNy42ODM0IDcuOTAyMzcgMTcuMjkyOSA4LjI5Mjg5TDEyIDEzLjU4NThMNi43MDcxMSA4LjI5Mjg5QzYuMzE2NTggNy45MDIzNyA1LjY4MzQyIDcuOTAyMzcgNS4yOTI4OSA4LjI5Mjg5WiIgZmlsbD0iY3VycmVudENvbG9yIiAvPgogICAgICAgICAgICAgICAgICA8L3N2Zz4=) ![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgICAgICA8cGF0aCBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGNsaXAtcnVsZT0iZXZlbm9kZCIgZD0iTTUuMjkyODkgMTUuNzA3MUM0LjkwMjM3IDE1LjMxNjYgNC45MDIzNyAxNC42ODM0IDUuMjkyODkgMTQuMjkyOUwxMS4yOTI5IDguMjkyODlDMTEuNjgzNCA3LjkwMjM3IDEyLjMxNjYgNy45MDIzNyAxMi43MDcxIDguMjkyODlMMTguNzA3MSAxNC4yOTI5QzE5LjA5NzYgMTQuNjgzNCAxOS4wOTc2IDE1LjMxNjYgMTguNzA3MSAxNS43MDcxQzE4LjMxNjYgMTYuMDk3NiAxNy42ODM0IDE2LjA5NzYgMTcuMjkyOSAxNS43MDcxTDEyIDEwLjQxNDJMNi43MDcxMSAxNS43MDcxQzYuMzE2NTggMTYuMDk3NiA1LjY4MzQyIDE2LjA5NzYgNS4yOTI4OSAxNS43MDcxWiIgZmlsbD0iY3VycmVudENvbG9yIiAvPgogICAgICAgICAgICAgICAgICA8L3N2Zz4=)

Tensor parallelism depends on collectives like reduce-scatter, all-gather, and all-reduce, so communication must keep pace with matrix computation. Expert parallelism routes different tokens to different experts, creating dynamic dispatch-and-combine traffic that changes every batch. SN50 supports both all-to-all and broadcast-and-filter approaches for that expert traffic.

[Back to top](#top)

Share this

[Share on X ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1MTIiIGhlaWdodD0iNTEyIiB2aWV3Ym94PSIwIDAgNTEyIDUxMiI+PHBhdGggZmlsbD0iY3VycmVudENvbG9yIiBkPSJNMzg5LjIgNDhoNzAuNkwzMDUuNiAyMjQuMiA0ODcgNDY0SDM0NUwyMzMuNyAzMTguNiAxMDYuNSA0NjRIMzUuOGwxNjQuOS0xODguNUwyNi44IDQ4aDE0NS42bDEwMC41IDEzMi45TDM4OS4yIDQ4em0tMjQuOCAzNzMuOGgzOS4xTDE1MS4xIDg4aC00MmwyNTUuMyAzMzMuOHoiIC8+PC9zdmc+) ](https://x.com/intent/post?url=https://sambanova.ai/blog/hot-chips-2026-dataflow-at-scale&text=Hot+Chips+2026%3A+SN50+RDU+Dataflow+at+Scale) [Share on Facebook ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMjAiIGhlaWdodD0iNTEyIiB2aWV3Ym94PSIwIDAgMzIwIDUxMiI+PHBhdGggZmlsbD0iY3VycmVudENvbG9yIiBkPSJNMjc5LjE0IDI4OGwxNC4yMi05Mi42NmgtODguOTF2LTYwLjEzYzAtMjUuMzUgMTIuNDItNTAuMDYgNTIuMjQtNTAuMDZoNDAuNDJWNi4yNlMyNjAuNDMgMCAyMjUuMzYgMGMtNzMuMjIgMC0xMjEuMDggNDQuMzgtMTIxLjA4IDEyNC43MnY3MC42MkgyMi44OVYyODhoODEuMzl2MjI0aDEwMC4xN1YyODh6IiAvPjwvc3ZnPg==) ](https://www.facebook.com/sharer/sharer.php?u=https://sambanova.ai/blog/hot-chips-2026-dataflow-at-scale&t=Hot+Chips+2026%3A+SN50+RDU+Dataflow+at+Scale) [Share on LinkedIn ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI0NDgiIGhlaWdodD0iNTEyIiB2aWV3Ym94PSIwIDAgNDQ4IDUxMiI+PHBhdGggZmlsbD0iY3VycmVudENvbG9yIiBkPSJNMTAwLjI4IDQ0OEg3LjRWMTQ4LjloOTIuODh6TTUzLjc5IDEwOC4xQzI0LjA5IDEwOC4xIDAgODMuNSAwIDUzLjhhNTMuNzkgNTMuNzkgMCAwIDEgMTA3LjU4IDBjMCAyOS43LTI0LjEgNTQuMy01My43OSA1NC4zek00NDcuOSA0NDhoLTkyLjY4VjMwMi40YzAtMzQuNy0uNy03OS4yLTQ4LjI5LTc5LjItNDguMjkgMC01NS42OSAzNy43LTU1LjY5IDc2LjdWNDQ4aC05Mi43OFYxNDguOWg4OS4wOHY0MC44aDEuM2MxMi40LTIzLjUgNDIuNjktNDguMyA4Ny44OC00OC4zIDk0IDAgMTExLjI4IDYxLjkgMTExLjI4IDE0Mi4zVjQ0OHoiIC8+PC9zdmc+) ](https://www.linkedin.com/shareArticle?mini=true&url=https://sambanova.ai/blog/hot-chips-2026-dataflow-at-scale&t=Hot+Chips+2026%3A+SN50+RDU+Dataflow+at+Scale)

Previous story

[← MiniMax M3 Running Fastest on SambaCloud](/blog/minimax-m3-running-fastest-on-sambacloud)

[![](data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjQiIGhlaWdodD0iMjQiIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgICAgICAgICAgIDxwYXRoIGZpbGwtcnVsZT0iZXZlbm9kZCIgY2xpcC1ydWxlPSJldmVub2RkIiBkPSJNMTkuNzg1OCA3LjA4MzAxTDEzLjgxMDIgMi41OTcyN0MxMi43MTQ4IDEuNzc0OTUgMTEuMjA5OSAxLjgwNDQ1IDEwLjE0NjcgMi42NjkxTDQuMTIyMjcgNy41Njg0QzMuNDEyNzkgOC4xNDUzNyAzIDkuMDE3MzkgMyA5LjkzOTIxVjE4Ljk2MDFDMyAyMC42MzkgNC4zNDMxNSAyMiA2IDIyTDggMjJIMTBIMTRIMTZMMTggMjJDMTkuNjU2OSAyMiAyMSAyMC42MzkgMjEgMTguOTYwMVY5LjUyNTY2QzIxIDguNTYyNTEgMjAuNTQ5NiA3LjY1NjM0IDE5Ljc4NTggNy4wODMwMVpNMTYgMTkuOTczNEgxOEMxOC41NTIzIDE5Ljk3MzQgMTkgMTkuNTE5NyAxOSAxOC45NjAxVjkuNTI1NjZDMTkgOS4yMDQ2MSAxOC44NDk5IDguOTAyNTUgMTguNTk1MyA4LjcxMTQ0TDEyLjYxOTcgNC4yMjU3QzEyLjI1NDYgMy45NTE1OSAxMS43NTI5IDMuOTYxNDMgMTEuMzk4NSA0LjI0OTY1TDUuMzc0MDkgOS4xNDg5NEM1LjEzNzYgOS4zNDEyNiA1IDkuNjMxOTQgNSA5LjkzOTIxVjE4Ljk2MDFDNSAxOS41MTk3IDUuNDQ3NzIgMTkuOTczNCA2IDE5Ljk3MzRIOFYxNi45MzM1QzggMTQuNjk0OSA5Ljc5MDg2IDEyLjg4MDMgMTIgMTIuODgwM0MxNC4yMDkxIDEyLjg4MDMgMTYgMTQuNjk0OSAxNiAxNi45MzM1VjE5Ljk3MzRaTTEwIDE5Ljk3MzRIMTRWMTYuOTMzNUMxNCAxNS44MTQyIDEzLjEwNDYgMTQuOTA2OSAxMiAxNC45MDY5QzEwLjg5NTQgMTQuOTA2OSAxMCAxNS44MTQyIDEwIDE2LjkzMzVWMTkuOTczNFoiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz4KICAgICAgICAgICAgICA8L3N2Zz4=)](/blog)
