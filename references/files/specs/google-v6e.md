<!-- 从 google-v6e.html 迁移的资料快照；原始 HTML SHA-256: c073bfdcd8b7874dca697b2b3bfb758c1ad8af0acf1f2b2edd8a090b1a732ad0。 -->

- [Home](https://docs.cloud.google.com/)

- 

  [Documentation](https://docs.cloud.google.com/docs)

- 

  [AI and ML](https://docs.cloud.google.com/docs/ai-ml)

- 

  [Cloud TPU](https://docs.cloud.google.com/tpu/docs)

- 

  [Guides](https://docs.cloud.google.com/tpu/docs/intro-to-tpu)

Send feedback

Stay organized with collections Save and categorize content based on your preferences.

# TPU v6e

This document describes the architecture and supported configurations of Cloud TPU v6e (Trillium). On all technical surfaces, such as the API and logs, and throughout this document, Trillium will be referred to as v6e.

With a 256-chip footprint per Pod, v6e shares many similarities with [v5e](/tpu/docs/v5e). This system is optimized for transformer, text-to-image, and convolutional neural network (CNN) training, fine-tuning, and serving.

## System architecture

Each v6e chip contains one TensorCore. Each TensorCore has 2 matrix-multiply units (MXU), a vector unit, and a scalar unit. The following table shows the key specifications and their values for TPU v6e.

| Specification | Values |
|----|----|
| Performance/total cost of ownership (TCO) (expected) | 1 |
| Peak compute per chip (bf16) | 918 TFLOPs |
| Peak compute per chip (Int8) | 1836 TOPs |
| HBM capacity per chip | 32 GB |
| HBM bandwidth per chip | 1638 GBps |
| Bidirectional inter-chip interconnect (ICI) bandwidth (per chip) | 800 GBps |
| ICI ports per chip | 4 |
| DRAM per host | 1536 GiB |
| Chips per host | 8 |
| TPU Pod size | 256 chips |
| Interconnect topology | 2D torus |
| BF16 peak compute per Pod | 234.9 PFLOPs |
| All-reduce bandwidth per Pod | 102.4 TB/s |
| Bisection bandwidth per Pod | 3.2 TB/s |
| Per-host NIC configuration | 4 x 200 Gbps NIC |
| Data center network bandwidth per Pod | 25.6 Tbps |
| Special features | [SparseCore](/tpu/docs/system-architecture-tpu-vm#sparsecore) |

## Supported configurations

**Note:** Use the [TPU topology visualizer](https://tpu-visualizer.uc.r.appspot.com/) to view 3D renderings of different TPU configurations.

The following table shows the 2D slice shapes that are supported for v6e:

| Topology | TPU chips | Hosts | VMs | Machine type       | Scope       |
|----------|-----------|-------|-----|--------------------|-------------|
| 1x1      | 1         | 1/8   | 1   | `ct6e-standard-1t` | Sub-host    |
| 2x2      | 4         | 1/2   | 1   | `ct6e-standard-4t` | Sub-host    |
| 2x4      | 8         | 1     | 1   | `ct6e-standard-8t` | Single-host |
| 2x4      | 8         | 1     | 2   | `ct6e-standard-4t` | Multi-host  |
| 4x4      | 16        | 2     | 4   | `ct6e-standard-4t` | Multi-host  |
| 4x8      | 32        | 4     | 8   | `ct6e-standard-4t` | Multi-host  |
| 8x8      | 64        | 8     | 16  | `ct6e-standard-4t` | Multi-host  |
| 8x16     | 128       | 16    | 32  | `ct6e-standard-4t` | Multi-host  |
| 16x16    | 256       | 32    | 64  | `ct6e-standard-4t` | Multi-host  |

**Note:** The 8-chip (2x4) configuration attached to 2 VMs is only supported when using the GKE API.

Slices with 8 chips (`v6e-8`) attached to a single VM are optimized for inference, allowing all 8 chips to be used in a single serving workload. You can perform multi-host inference using Pathways on Cloud. For more information, see [Perform multihost inference using Pathways](/ai-hypercomputer/docs/workloads/pathways-on-cloud/multihost-inference).

For information about the number of VMs for each topology, see [VM Types](#vm-types).

### VM types

Each TPU v6e VM can contain 1, 4, or 8 chips. 4-chip and smaller slices have the same non-uniform memory access (NUMA) node. For more information about NUMA nodes, see [Non-uniform memory access](https://en.wikipedia.org/wiki/Non-uniform_memory_access) on Wikipedia.

![Diagram of a v6e host](/static/tpu/docs/images/v6e-tpu-host.png)

v6e slices are created using half-host VMs, each with 4 TPU chips. There are two exceptions to this rule:

- `v6e-1`: A VM with only a single chip, primarily intended for testing
- `v6e-8`: A full-host VM that has been optimized for an inference use case with all 8 chips attached to a single VM.

The following table shows a comparison of TPU v6e VM types:

| VM type | Number of vCPUs per VM | RAM (GB) per VM | Number of NUMA nodes per VM |
|----|----|----|----|
| 1-chip VM | 44 | 176 | 1 |
| 4-chip VM | 180 | 720 | 1 |
| 8-chip VM | 360 | 1440 | 2 |

**Note:** We don't recommend using a full-host VM (`v6e-8` with one VM) for dual networks due to performance impacts.

## What's next

- Run [training and inference using TPU v6e](/tpu/docs/v6e-intro)

Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-08-26 UTC.

Need to tell us more?

\[\[\["Easy to understand","easyToUnderstand","thumb-up"\],\["Solved my problem","solvedMyProblem","thumb-up"\],\["Other","otherUp","thumb-up"\]\],\[\["Hard to understand","hardToUnderstand","thumb-down"\],\["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"\],\["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"\],\["Other","otherDown","thumb-down"\]\],\["Last updated 2026-08-26 UTC."\],\[\],\[\]\]
