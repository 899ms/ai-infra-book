<!-- 从 nvidia-h20-vgpu-release7.html 迁移的资料快照；原始 HTML SHA-256: 7dcb1f989bc74d7c6a3d94f52b18233308684c03009d6027910e344c2660e830。 -->

- [](../../../index.html)
- [NVIDIA AI Enterprise and NVIDIA vGPU for Compute](../../vgpu.html)
- [NVIDIA vGPU Types Reference](index.html)
- Hopper Architecture vGPU Types

[Is this page helpful?](https://surveys.hotjar.com/4904bf71-6484-47a7-83ff-4715cceabdb5)

<a id="hopper-architecture-vgpu-types"></a>

# Hopper Architecture vGPU Types
The NVIDIA Hopper architecture delivers exceptional performance for large-scale AI, high-performance computing (HPC), and data analytics workloads. Hopper GPUs feature a revolutionary Transformer Engine, fourth-generation Tensor Cores, and enhanced Multi-Instance GPU (MIG) capabilities that enable secure partitioning and optimal resource utilization in enterprise environments.

Designed for the most demanding AI workloads including large language models, recommendation systems, and scientific computing, Hopper provides breakthrough performance with support for FP8 precision, NVLink 4.0, and advanced memory technologies. Both MIG-backed and time-sliced vGPU configurations ensure deployment options for virtualized infrastructure.

<a id="mig-backed-and-time-sliced-nvidia-vgpu-for-compute"></a>

## MIG-Backed and Time-Sliced NVIDIA vGPU for Compute
Physical GPUs per board: 1

The maximum number of vGPUs per board is the product of the maximum number of vGPUs per GPU and the number of physical GPUs per board.

Required license edition: NVIDIA AI Enterprise

**MIG-Backed NVIDIA vGPU for Compute**

For details on GPU instance profiles, refer to the [NVIDIA Multi-Instance GPU User Guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/). For mode selection and isolation trade-offs, see [Supported vGPU Modes](../overview.html#vgpu-modes) and [MIG-Backed vGPU](../features/mig-backed-vgpu.html#feature-mig-backed-vgpu).

**Time-Sliced NVIDIA vGPU for Compute**

Intended use cases:

- vGPUs with more than 40 GB of framebuffer: Training Workloads

- vGPUs with 40 GB of framebuffer: Inference Workloads

These vGPU types support a single display with a fixed maximum resolution.

For scheduler choices that affect time-sliced density and latency, see [Scheduling Policies](../features/scheduling.html#feature-scheduling-policies).

NVIDIA H800 PCIe 94GB (H800 NVL)

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H800L-7-94C | 96 | 1 | 7 | 7 | MIG 7g.94gb |
| H800L-4-47C | 48 | 1 | 4 | 4 | MIG 4g.47gb |
| H800L-3-47C | 48 | 2 | 3 | 3 | MIG 3g.47gb |
| H800L-2-24C | 24 | 3 | 2 | 2 | MIG 2g.24gb |
| H800L-1-24C | 24 | 4 | 1 | 1 | MIG 1g.24gb |
| H800L-1-12C | 12 | 7 | 1 | 1 | MIG 1g.12gb |
| H800L-1-12CME [^1] | 12 | 1 | 1 | 1 | MIG 1g.12gb+me |

Table 164 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H800 PCIe 94GB (H800 NVL)[\#](#id36 "Link to this table") {#id36}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^2] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H800L-94C | 96 | 1 | 1 | 3840x2400 | 1 |
| H800L-47C | 48 | 2 | 2 | 3840x2400 | 1 |
| H800L-23C | 23 | 4 | 4 | 3840x2400 | 1 |
| H800L-15C | 15 | 6 | 4 | 3840x2400 | 1 |
| H800L-11C | 11 | 8 | 8 | 3840x2400 | 1 |
| H800L-6C | 6 | 15 | 8 | 3840x2400 | 1 |
| H800L-4C | 4 | 23 | 16 | 3840x2400 | 1 |

Table 165 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H800 PCIe 94GB (H800 NVL)[\#](#id37 "Link to this table") {#id37}

NVIDIA H800 PCIe 80GB

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H800-7-80C | 81 | 1 | 7 | 7 | MIG 7g.80gb |
| H800-4-40C | 40 | 1 | 4 | 4 | MIG 4g.40gb |
| H800-3-40C | 40 | 2 | 3 | 3 | MIG 3g.40gb |
| H800-2-20C | 20 | 3 | 2 | 2 | MIG 2g.20gb |
| H800-1-20C [^3] | 20 | 4 | 1 | 1 | MIG 1g.20gb |
| H800-1-10C | 10 | 7 | 1 | 1 | MIG 1g.10gb |
| H800-1-10CME [^4] | 10 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 166 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H800 PCIe 80GB[\#](#id38 "Link to this table") {#id38}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^5] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H800-80C | 81 | 1 | 1 | 3840x2400 | 1 |
| H800-40C | 40 | 2 | 2 | 3840x2400 | 1 |
| H800-20C | 20 | 4 | 4 | 3840x2400 | 1 |
| H800-16C | 16 | 5 | 4 | 3840x2400 | 1 |
| H800-10C | 10 | 8 | 8 | 3840x2400 | 1 |
| H800-8C | 8 | 10 | 8 | 3840x2400 | 1 |
| H800-5C | 5 | 16 | 16 | 3840x2400 | 1 |
| H800-4C | 4 | 20 | 16 | 3840x2400 | 1 |

Table 167 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H800 PCIe 80GB[\#](#id39 "Link to this table") {#id39}

NVIDIA H800 SXM5 80GB

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H800XM-7-80C | 81 | 1 | 7 | 7 | MIG 7g.80gb |
| H800XM-4-40C | 40 | 1 | 4 | 4 | MIG 4g.40gb |
| H800XM-3-40C | 40 | 2 | 3 | 3 | MIG 3g.40gb |
| H800XM-2-20C | 20 | 3 | 2 | 2 | MIG 2g.20gb |
| H800XM-1-20C [^6] | 20 | 4 | 1 | 1 | MIG 1g.20gb |
| H800XM-1-10C | 10 | 7 | 1 | 1 | MIG 1g.10gb |
| H800XM-1-10CME [^7] | 10 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 168 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H800 SXM5 80GB[\#](#id40 "Link to this table") {#id40}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^8] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H800XM-80C | 81 | 1 | 1 | 3840x2400 | 1 |
| H800XM-40C | 40 | 2 | 2 | 3840x2400 | 1 |
| H800XM-20C | 20 | 4 | 4 | 3840x2400 | 1 |
| H800XM-16C | 16 | 5 | 4 | 3840x2400 | 1 |
| H800XM-10C | 10 | 8 | 8 | 3840x2400 | 1 |
| H800XM-8C | 8 | 10 | 8 | 3840x2400 | 1 |
| H800XM-5C | 5 | 16 | 16 | 3840x2400 | 1 |
| H800XM-4C | 4 | 20 | 16 | 3840x2400 | 1 |

Table 169 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H800 SXM5 80GB[\#](#id41 "Link to this table") {#id41}

NVIDIA H200 PCIe 141GB (H200 NVL)

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H200-7-141C | 144 | 1 | 7 | 7 | MIG 7g.141gb |
| H200-4-71C | 72 | 1 | 4 | 4 | MIG 4g.71gb |
| H200-3-71C | 72 | 2 | 3 | 3 | MIG 3g.71gb |
| H200-2-35C | 35 | 3 | 2 | 2 | MIG 2g.35gb |
| H200-1-35C [^9] | 35 | 4 | 1 | 1 | MIG 1g.35gb |
| H200-1-18C | 18 | 7 | 1 | 1 | MIG 1g.18gb |
| H200-1-18CME [^10] | 18 | 1 | 1 | 1 | MIG 1g.18gb+me |

Table 170 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H200 PCIe 141GB (H200 NVL)[\#](#id42 "Link to this table") {#id42}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^11] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H200-141C | 144 | 1 | 1 | 3840x2400 | 1 |
| H200-70C | 71 | 2 | 2 | 3840x2400 | 1 |
| H200-35C | 35 | 4 | 4 | 3840x2400 | 1 |
| H200-28C | 28 | 5 | 5 | 3840x2400 | 1 |
| H200-17C | 17 | 8 | 8 | 3840x2400 | 1 |
| H200-14C | 14 | 10 | 10 | 3840x2400 | 1 |
| H200-8C | 8 | 16 | 16 | 3840x2400 | 1 |
| H200-7C | 7 | 20 | 20 | 3840x2400 | 1 |
| H200-4C | 4 | 32 | 32 | 3840x2400 | 1 |

Table 171 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H200 PCIe 141GB (H200 NVL)[\#](#id43 "Link to this table") {#id43}

NVIDIA H200 SXM5 141GB

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H200X-7-141C | 144 | 1 | 7 | 7 | MIG 7g.141gb |
| H200X-4-71C | 72 | 1 | 4 | 4 | MIG 4g.71gb |
| H200X-3-71C | 72 | 2 | 3 | 3 | MIG 3g.71gb |
| H200X-2-35C | 35 | 3 | 2 | 2 | MIG 2g.35gb |
| H200X-1-35C [^12] | 35 | 4 | 1 | 1 | MIG 1g.35gb |
| H200X-1-18C | 18 | 7 | 1 | 1 | MIG 1g.18gb |
| H200X-1-18CME [^13] | 18 | 1 | 1 | 1 | MIG 1g.18gb+me |

Table 172 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H200 SXM5 141GB[\#](#id44 "Link to this table") {#id44}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^14] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H200X-141C | 144 | 1 | 1 | 3840x2400 | 1 |
| H200X-70C | 71 | 2 | 2 | 3840x2400 | 1 |
| H200X-35C | 35 | 4 | 4 | 3840x2400 | 1 |
| H200X-28C | 28 | 5 | 5 | 3840x2400 | 1 |
| H200X-17C | 17 | 8 | 8 | 3840x2400 | 1 |
| H200X-14C | 14 | 10 | 10 | 3840x2400 | 1 |
| H200X-8C | 8 | 16 | 16 | 3840x2400 | 1 |
| H200X-7C | 7 | 20 | 20 | 3840x2400 | 1 |
| H200X-4C | 4 | 32 | 32 | 3840x2400 | 1 |

Table 173 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H200 SXM5 141GB[\#](#id45 "Link to this table") {#id45}

NVIDIA H100 PCIe 94GB (H100 NVL)

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H100L-7-94C | 96 | 1 | 7 | 7 | MIG 7g.94gb |
| H100L-4-47C | 48 | 1 | 4 | 4 | MIG 4g.47gb |
| H100L-3-47C | 48 | 2 | 3 | 3 | MIG 3g.47gb |
| H100L-2-24C | 24 | 3 | 2 | 2 | MIG 2g.24gb |
| H100L-1-24C [^15] | 24 | 4 | 1 | 1 | MIG 1g.24gb |
| H100L-1-12C | 12 | 7 | 1 | 1 | MIG 1g.12gb |
| H100L-1-12CME [^16] | 12 | 1 | 1 | 1 | MIG 1g.12gb+me |

Table 174 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H100 PCIe 94GB (H100 NVL)[\#](#id46 "Link to this table") {#id46}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^17] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H100L-94C | 96 | 1 | 1 | 3840x2400 | 1 |
| H100L-47C | 48 | 2 | 2 | 3840x2400 | 1 |
| H100L-23C | 23 | 4 | 4 | 3840x2400 | 1 |
| H100L-15C | 15 | 6 | 4 | 3840x2400 | 1 |
| H100L-11C | 11 | 8 | 8 | 3840x2400 | 1 |
| H100L-6C | 6 | 15 | 8 | 3840x2400 | 1 |
| H100L-4C | 4 | 23 | 16 | 3840x2400 | 1 |

Table 175 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H100 PCIe 94GB (H100 NVL)[\#](#id47 "Link to this table") {#id47}

NVIDIA H100 SXM5 94GB

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H100XL-7-94C | 96 | 1 | 7 | 7 | MIG 7g.94gb |
| H100XL-4-47C | 48 | 1 | 4 | 4 | MIG 4g.47gb |
| H100XL-3-47C | 48 | 2 | 3 | 3 | MIG 3g.47gb |
| H100XL-2-24C | 24 | 3 | 2 | 2 | MIG 2g.24gb |
| H100XL-1-24C [^18] | 24 | 4 | 1 | 1 | MIG 1g.24gb |
| H100XL-1-12C | 12 | 7 | 1 | 1 | MIG 1g.12gb |
| H100XL-1-12CME [^19] | 12 | 1 | 1 | 1 | MIG 1g.12gb+me |

Table 176 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H100 SXM5 94GB[\#](#id48 "Link to this table") {#id48}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^20] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H100XL-94C | 96 | 1 | 1 | 3840x2400 | 1 |
| H100XL-47C | 48 | 2 | 2 | 3840x2400 | 1 |
| H100XL-23C | 23 | 4 | 4 | 3840x2400 | 1 |
| H100XL-15C | 15 | 6 | 4 | 3840x2400 | 1 |
| H100XL-11C | 11 | 8 | 8 | 3840x2400 | 1 |
| H100XL-6C | 6 | 15 | 8 | 3840x2400 | 1 |
| H100XL-4C | 4 | 23 | 16 | 3840x2400 | 1 |

Table 177 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H100 SXM5 94GB[\#](#id49 "Link to this table") {#id49}

NVIDIA H100 PCIe 80GB

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H100-7-80C | 81 | 1 | 7 | 7 | MIG 7g.80gb |
| H100-4-40C | 40 | 1 | 4 | 4 | MIG 4g.40gb |
| H100-3-40C | 40 | 2 | 3 | 3 | MIG 3g.40gb |
| H100-2-20C | 20 | 3 | 2 | 2 | MIG 2g.20gb |
| H100-1-20C [^21] | 20 | 4 | 1 | 1 | MIG 1g.20gb |
| H100-1-10C | 10 | 7 | 1 | 1 | MIG 1g.10gb |
| H100-1-10CME [^22] | 10 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 178 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H100 PCIe 80GB[\#](#id50 "Link to this table") {#id50}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^23] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H100-80 | 81 | 1 | 1 | 3840x2400 | 1 |
| H100-40C | 40 | 2 | 2 | 3840x2400 | 1 |
| H100-20C | 20 | 4 | 4 | 3840x2400 | 1 |
| H100-16C | 16 | 6 | 4 | 3840x2400 | 1 |
| H100-10C | 10 | 8 | 8 | 3840x2400 | 1 |
| H100-8C | 8 | 10 | 8 | 3840x2400 | 1 |
| H100-5C | 5 | 16 | 16 | 3840x2400 | 1 |
| H100-4C | 4 | 20 | 16 | 3840x2400 | 1 |

Table 179 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H100 PCIe 80GB[\#](#id51 "Link to this table") {#id51}

NVIDIA H100 SXM5 80GB

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H100XM-7-80C | 81 | 1 | 7 | 7 | MIG 7g.80gb |
| H100XM-4-40C | 40 | 1 | 4 | 4 | MIG 4g.40gb |
| H100XM-3-40C | 40 | 2 | 3 | 3 | MIG 3g.40gb |
| H100XM-2-20C | 20 | 3 | 2 | 2 | MIG 2g.20gb |
| H100XM-1-20C [^24] | 20 | 4 | 1 | 1 | MIG 1g.20gb |
| H100XM-1-10C | 10 | 7 | 1 | 1 | MIG 1g.10gb |
| H100XM-1-10CME [^25] | 10 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 180 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H100 SXM5 80GB[\#](#id52 "Link to this table") {#id52}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^26] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H100XM-80C | 81 | 1 | 1 | 3840x2400 | 1 |
| H100XM-40C | 40 | 2 | 2 | 3840x2400 | 1 |
| H100XM-20C | 20 | 4 | 4 | 3840x2400 | 1 |
| H100XM-16C | 16 | 6 | 4 | 3840x2400 | 1 |
| H100XM-10C | 10 | 8 | 8 | 3840x2400 | 1 |
| H100XM-8C | 8 | 10 | 8 | 3840x2400 | 1 |
| H100XM-5C | 5 | 16 | 16 | 3840x2400 | 1 |
| H100XM-4C | 4 | 20 | 16 | 3840x2400 | 1 |

Table 181 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H100 SXM5 80GB[\#](#id53 "Link to this table") {#id53}

NVIDIA H100 SXM5 64GB

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H100XS-7-64C | 65 | 1 | 7 | 7 | MIG 7g.64gb |
| H100XS-4-32C | 32 | 1 | 4 | 4 | MIG 4g.32gb |
| H100XS-3-32C | 32 | 2 | 3 | 3 | MIG 3g.32gb |
| H100XS-2-16C | 16 | 3 | 2 | 2 | MIG 2g.16gb |
| H100XS-1-16C [^27] | 16 | 4 | 1 | 1 | MIG 1g.16gb |
| H100XS-1-8C | 8 | 7 | 1 | 1 | MIG 1g.8gb |
| H100XS-1-8CME [^28] | 8 | 1 | 1 | 1 | MIG 1g.8gb+me |

Table 182 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H100 SXM5 64GB[\#](#id54 "Link to this table") {#id54}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^29] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H100XS-64C | 65 | 1 | 1 | 3840x2400 | 1 |
| H100XS-32C | 32 | 2 | 2 | 3840x2400 | 1 |
| H100XS-16C | 16 | 4 | 4 | 3840x2400 | 1 |
| H100XS-8C | 8 | 8 | 8 | 3840x2400 | 1 |
| H100XS-4C | 4 | 16 | 16 | 3840x2400 | 1 |

Table 183 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H100 SXM5 64GB[\#](#id55 "Link to this table") {#id55}

NVIDIA H20 SXM5 141GB

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H20X-7-141C | 144 | 1 | 7 | 7 | MIG 7g.141gb |
| H20X-4-71C | 72 | 1 | 4 | 4 | MIG 4g.71gb |
| H20X-3-71C | 72 | 2 | 3 | 3 | MIG 3g.71gb |
| H20X-2-35C | 35 | 3 | 2 | 2 | MIG 2g.35gb |
| H20X-1-35C [^30] | 35 | 4 | 1 | 1 | MIG 1g.35gb |
| H20X-1-18C | 18 | 7 | 1 | 1 | MIG 1g.18gb |
| H20X-1-18CME [^31] | 18 | 1 | 1 | 1 | MIG 1g.18gb+me |

Table 184 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H20 SXM5 141GB[\#](#id56 "Link to this table") {#id56}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^32] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H20X-141C | 144 | 1 | 1 | 3840x2400 | 1 |
| H20X-70C | 71 | 2 | 2 | 3840x2400 | 1 |
| H20X-35C | 35 | 4 | 4 | 3840x2400 | 1 |
| H20X-28C | 28 | 5 | 5 | 3840x2400 | 1 |
| H20X-17C | 17 | 8 | 8 | 3840x2400 | 1 |
| H20X-14C | 14 | 10 | 10 | 3840x2400 | 1 |
| H20X-8C | 8 | 16 | 16 | 3840x2400 | 1 |
| H20X-7C | 7 | 20 | 20 | 3840x2400 | 1 |
| H20X-4C | 4 | 32 | 32 | 3840x2400 | 1 |

Table 185 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H20 SXM5 141GB[\#](#id57 "Link to this table") {#id57}

NVIDIA H20 SXM5 96GB

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H20-7-96C | 98 | 1 | 7 | 7 | MIG 7g.96gb |
| H20-4-48C | 49 | 1 | 4 | 4 | MIG 4g.48gb |
| H20-3-48C | 49 | 2 | 3 | 3 | MIG 3g.48gb |
| H20-2-24C | 24 | 3 | 2 | 2 | MIG 2g.24gb |
| H20-1-24C [^33] | 24 | 4 | 1 | 1 | MIG 1g.24gb |
| H20-1-12C | 12 | 7 | 1 | 1 | MIG 1g.12gb |
| H20-1-12CME [^34] | 12 | 1 | 1 | 1 | MIG 1g.12gb+me |

Table 186 MIG-Backed NVIDIA vGPU for Compute for NVIDIA H20 SXM5 96GB[\#](#id58 "Link to this table") {#id58}

| Virtual GPU Type | Framebuffer (GB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^35] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H20-96C | 98 | 1 | 1 | 3840x2400 | 1 |
| H20-48C | 49 | 2 | 2 | 3840x2400 | 1 |
| H20-24C | 24 | 4 | 2 | 3840x2400 | 1 |
| H20-16C | 16 | 6 | 4 | 3840x2400 | 1 |
| H20-12C | 12 | 8 | 4 | 3840x2400 | 1 |
| H20-6C | 6 | 16 | 8 | 3840x2400 | 1 |
| H20-4C | 4 | 24 | 8 | 3840x2400 | 1 |

Table 187 Time-Sliced NVIDIA vGPU for Compute for NVIDIA H20 SXM5 96GB[\#](#id59 "Link to this table") {#id59}

------------------------------------------------------------------------

Footnotes

\[1\] ([1](#id1),[2](#id3),[3](#id4),[4](#id6),[5](#id7),[6](#id9),[7](#id10),[8](#id12),[9](#id13),[10](#id15),[11](#id16),[12](#id18),[13](#id19),[14](#id21),[15](#id22),[16](#id24),[17](#id25),[18](#id27),[19](#id28),[20](#id30),[21](#id31),[22](#id33),[23](#id34))

These vGPU types are supported on ESXi, starting with vSphere 8.0 update 3.

\[2\] ([1](#id2),[2](#id5),[3](#id8),[4](#id11),[5](#id14),[6](#id17),[7](#id20),[8](#id23),[9](#id26),[10](#id29),[11](#id32),[12](#id35))

NVIDIA vGPU for Compute is optimized for compute-intensive workloads. As a result, they support only a single display head and do not provide Quadro graphics acceleration.

[](blackwell.html "previous page")

previous

Blackwell Architecture vGPU Types

[](ada-lovelace.html "next page")

next

Ada Lovelace Architecture vGPU Types

On this page

- [MIG-Backed and Time-Sliced NVIDIA vGPU for Compute](#mig-backed-and-time-sliced-nvidia-vgpu-for-compute)

[^1]:

[^2]:

[^3]:

[^4]:

[^5]:

[^6]:

[^7]:

[^8]:

[^9]:

[^10]:

[^11]:

[^12]:

[^13]:

[^14]:

[^15]:

[^16]:

[^17]:

[^18]:

[^19]:

[^20]:

[^21]:

[^22]:

[^23]:

[^24]:

[^25]:

[^26]:

[^27]:

[^28]:

[^29]:

[^30]:

[^31]:

[^32]:

[^33]:

[^34]:

[^35]:
