<!-- 从 nvidia-h20-vgpu.html 迁移的资料快照；原始 HTML SHA-256: 5b489a127b67ce3ac34da9a243c360919c32f5e463b89e4e6dc210c24091405f。 -->

- [](../index.html)
- NVIDIA AI Enterprise and NVIDIA vGPU (C-Series)

[Is this page helpful?](https://surveys.hotjar.com/4904bf71-6484-47a7-83ff-4715cceabdb5)

<a id="nvidia-ai-enterprise-and-nvidia-vgpu-c-series"></a>

# NVIDIA AI Enterprise and NVIDIA vGPU (C-Series)
NVIDIA AI Enterprise offers a flexible licensing mechanism delivered through a comprehensive software suite designed for enterprise-grade AI. This suite combines infrastructure tools, application frameworks, libraries, and NVIDIA Inference Microservice (NIM), streamlining the deployment of AI workloads across various environments. This approach helps organizations tailor AI solutions to specific requirements, maximizing performance and scalability without the need for multiple dedicated GPU resources.

NVIDIA vGPU (C-Series) drivers are one of the deployment approaches supported by NVIDIA AI Enterprise in virtualized environments. NVIDIA vGPU (C-Series) extends the capabilities of NVIDIA AI Enterprise by enabling AI and machine learning tasks to run in virtual machines that share GPU resources. This allows AI tasks to maximize GPU utilization while supporting multiple users, making it easier to handle dynamic workloads on local servers or in the cloud. By leveraging vGPU (C-Series) within NVIDIA AI Enterprise, organizations can confidently scale their AI infrastructure and integrate advanced computing power into existing virtualization strategies.

<a id="key-concepts"></a>

## Key Concepts
<a id="vgpu-c-series"></a>

### vGPU (C-Series)
NVIDIA Virtual GPU (C-Series) accelerates AI and ML workloads by enabling multiple virtual machines to have simultaneous, direct access to a single physical GPU while maintaining the high-performance compute capabilities required for complex model training, inference, and data processing. By distributing GPU resources dynamically and efficiently across multiple VMs, vGPU (C-Series) optimizes utilization and lowers overall hardware costs, making it especially beneficial for large-scale and rapidly evolving AI environments.

<a id="nvidia-vgpu-c-series-virtual-gpu-manager"></a>

### NVIDIA vGPU (C-Series) Virtual GPU Manager
The NVIDIA vGPU (C-Series) Virtual GPU Manager enables GPU virtualization by allowing multiple virtual machines (VMs) to share a physical GPU, optimizing GPU allocation for different workloads. The NVIDIA AI Enterprise host driver, also known as the NVIDIA vGPU (C-Series) Virtual GPU Manager, is installed on the hypervisor, is hypervisor specific,and is best suited for running AI and machine learning workloads in virtualized environments by optimizing GPU performance for tasks like deep learning, model training, and inference. It’s part of the NVIDIA AI Enterprise software, which is designed for deep learning, data science, and other high-performance computing in virtual environments.

The NVIDIA vGPU (C-Series) Virtual GPU Manager packages can be downloaded from the NGC Catalog.

<a id="nvidia-vgpu-c-series-driver"></a>

### NVIDIA vGPU (C-Series) Driver
The NVIDIA vGPU (C-Series) Driver is installed on each VM’s operating system, allowing the VM to fully leverage the virtualized GPU resources. It works with the NVIDIA vGPU (C-Series) Virtual GPU Manager to ensure resource sharing and isolation. The NVIDIA vGPU (C-Series) Driver maintains a consistent, high-performance computing experience for AI and ML workloads, streamlining the deployment and management of GPU-accelerated applications within virtualized environments run AI workloads on vGPU powered VMs in virtualized environments. It’s part of the NVIDIA AI Enterprise software, which is designed for deep learning, data science, and other high-performance computing in virtual environments.

The NVIDIA vGPU (C-Series) Driver packages can be downloaded from the NGC Catalog.

<a id="features"></a>

## Features
Below are the key features that highlight the capabilities and benefits of NVIDIA vGPU (C-Series), designed to work alongside NVIDIA AI Enterprise, and optimize performance and efficiency across various use cases.

**GPU Virtualization for Multiple VMs and Containers**  
NVIDIA vGPU (C-Series) lets multiple virtual machines (VMs) or containers share one physical GPU. This means you can distribute GPU power to different tasks (like AI, machine learning, or data processing) without needing a separate GPU for each task, making better use of the available hardware.

vGPU (C-Series) also supports a multi-GPU scenario by enabling multiple GPUs to be assigned to a single VM for larger models and increasingly demanding workflows.

**Scalability and High User Density**  
NVIDIA vGPU (C-Series) allows many users or tasks to use GPU resources at the same time, which is perfect for cloud setups, virtual desktops, and shared AI environments. This makes it easier for AI businesses to support lots of users or applications without needing extra hardware.

**High-Performance GPU Acceleration**  
With NVIDIA vGPU (C-Series), you can use GPU power for demanding tasks like deep learning, training models, and data analysis. This helps AI and machine learning tasks run much faster compared to using just the CPU.

**Flexible Resource Allocation**  
NVIDIA vGPU (C-Series) lets businesses control how GPU resources are distributed. Admins can assign specific amounts of GPU memory and processing power to different VMs or containers, making sure each task gets the right amount of resources. This flexibility helps improve efficiency and reduce costs.

**Multi-Workload Support**  
NVIDIA vGPU (C-Series) can handle many types of tasks, from graphics rendering for remote workstations to AI/ML and high-performance computing. This flexibility is important for NVIDIA AI Enterprise customers who need to run different demanding applications on the same system.

**Support for AI Frameworks and Libraries**  
NVIDIA vGPU (C-Series) works smoothly with popular AI tools like TensorFlow, PyTorch, and MXNet, boosting performance for deep learning tasks. This helps NVIDIA AI Enterprise customers fully use GPU power for AI and ML, making their work faster and more efficient.

**Cloud and Data Center Optimization**  
NVIDIA vGPU (C-Series) lets both on-premises data centers and cloud environments make full use of GPU resources. Customers can set up AI systems in hybrid or multi-cloud setups, ensuring GPU resources are well-distributed, which helps manage and scale AI workloads more easily in the cloud.

**MIG-Backed NVIDIA vGPUs**  
With MIG-backed NVIDIA vGPU (C-Series), a physical GPU can be split into smaller, separate parts. This lets businesses assign different amounts of GPU power to various tasks, so less demanding AI tasks can run smoothly while still giving more power to bigger tasks. This feature is especially useful in shared, cloud, or mixed environments.

<a id="faqs"></a>

## FAQs
**Q: What is the difference between time-sliced vGPUs and MIG-backed vGPUs?**

A: Time-sliced vGPUs and MIG-backed vGPUs are two different approaches to sharing GPU resources in virtualized environments. Here are the key differences:

| Time-sliced vGPUs | MIG-backed vGPUs |
|----|----|
| Share the entire GPU among multiple virtual machines (VMs). | Partition the GPU into smaller, dedicated instances. |
| Each vGPU gets full access to all streaming multiprocessors (SMs) and engines, but only for a specific time slice. | Each vGPU gets exclusive access to a portion of the GPU’s memory and compute resources. |
| Processes run in series, with each vGPU waiting while others use the GPU. | Processes run in parallel on dedicated hardware slices. |
| The number of VMs per GPU is limited only by framebuffer size. | Depending on the number of MIG instances supported on a GPU, this can range from 4 to 7 VMs per GPU. |
| Better for workloads that require occasional bursts of full GPU power. | Provides better performance isolation and more consistent latency. |

Table 17 Differences Between Time-Sliced and MIG-Backed vGPUs[\#](#id152 "Link to this table") {#id152}

<a id="release-notes"></a>

## Release Notes
<a id="prerequisites"></a>

### Prerequisites
<a id="using-nvidia-vgpu-c-series"></a>

#### Using NVIDIA vGPU (C-Series)
Because the NVIDIA vGPU (C-Series) has large BAR memory settings, using these vGPUs has some restrictions on VMware ESXi.

- The guest OS must be a 64-bit OS.

- 64-bit MMIO and EFI boot must be enabled for the VM.

- The guest OS must be able to be installed in EFI boot mode.

- The VM’s MMIO space must be increased 64GB or more, depending on the GPU’s MMIO requirements, as explained in [VMware Knowledge Base Article: VMware vSphere VMDirectPath I/O: Requirements for Platforms and Devices (2142307)](https://knowledge.broadcom.com/external/article?legacyId=2142307).

<a id="using-nvidia-vgpu-c-series-on-gpus-requiring-64gb-or-more-of-mmio-space-with-large-memory-vms"></a>

#### Using NVIDIA vGPU (C-Series) on GPUs Requiring 64GB or More of MMIO Space with Large-Memory VMs
Some GPUs require 64GB or more of MMIO (Memory-Mapped I/O) space. When a vGPU on a GPU that requires 64GB or more of MMIO space is assigned to a VM with 32GB or more of memory on ESXi, the VM’s MMIO space must be increased to the amount that the GPU requires.

For more information, refer to the [VMware Knowledge Base Article: VMware vSphere VMDirectPath I/O: Requirements for Platforms and Devices (2142307)](https://knowledge.broadcom.com/external/article?legacyId=2142307).

No extra configuration is needed.

The following table lists the GPUs that require 64GB or more of MMIO space and the amount of MMIO space that each GPU requires.

| GPU                             | MMIO Space Required |
|---------------------------------|---------------------|
| NVIDIA H200 (all variants)      | 512GB               |
| NVIDIA H100 (all variants)      | 256GB               |
| NVIDIA H800 (all variants)      | 256GB               |
| NVIDIA H20 141GB                | 512GB               |
| NVIDIA H20 96GB                 | 256GB               |
| NVIDIA L40                      | 128GB               |
| NVIDIA L20                      | 128GB               |
| NVIDIA L4                       | 64GB                |
| NVIDIA L2                       | 64GB                |
| NVIDIA RTX 6000 Ada             | 128GB               |
| NVIDIA RTX 5000 Ada             | 64GB                |
| NVIDIA A40                      | 128GB               |
| NVIDIA A30                      | 64GB                |
| NVIDIA A10                      | 64GB                |
| NVIDIA A100 80GB (all variants) | 256GB               |
| NVIDIA A100 40GB (all variants) | 128GB               |
| NVIDIA RTX A6000                | 128GB               |
| NVIDIA RTX A5500                | 64GB                |
| NVIDIA RTX A5000                | 64GB                |
| Quadro RTX 8000 Passive         | 64GB                |
| Quadro RTX 6000 Passive         | 64GB                |
| Tesla V100 (all variants)       | 64GB                |

Table 18 Requirements for Using NVIDIA vGPU (C-Series) on GPUs Requiring 64GB or More of MMIO Space with Large-Memory VMs[\#](#id153 "Link to this table") {#id153}

<a id="platform-support"></a>

### Platform Support
<a id="microsoft-windows-guest-operating-systems"></a>

#### Microsoft Windows Guest Operating Systems
NVIDIA AI Enterprise supports only the Tesla Compute Cluster (TCC) driver model for Windows guest drivers.

Windows guest OS support is limited to running applications natively in Windows VMs without containers. NVIDIA AI Enterprise features that depend on the containerization of applications are not supported on Windows guest operating systems.

If you are using a generic Linux supported by the KVM hypervisor, consult the documentation from your hypervisor vendor for information about Windows releases supported as a guest OS.

For more information, refer to the [Non-containerized Applications on Hypervisors and Guest Operating Systems Supported with vGPU](../support/support-matrix.html#table-guest-os-systems-6-2) table.

<a id="nvidia-vgpu-c-series-migration"></a>

#### NVIDIA vGPU (C-Series) Migration
NVIDIA vGPU (C-Series) Migration, which includes vMotion and suspend-resume, is supported for both time-sliced and MIG-backed vGPUs on all supported GPUs and guest operating systems but only on a subset of supported hypervisor software releases.

**Limitations with NVIDIA vGPU (C-Series) Migration Support**

**Red Hat Enterprise Linux with KVM**: Migration between hosts running different versions of the NVIDIA Virtual GPU Manager driver is not supported, even within the same NVIDIA Virtual GPU Manager driver branch.

NVIDIA vGPU (C-Series) migration is disabled for a VM for which any of the following NVIDIA CUDA Toolkit features is enabled:

- Unified memory

- Debuggers

- Profilers

**Supported Hypervisor Software Releases**

Since Red Hat Enterprise Linux with KVM 9.4

Not supported on Ubuntu

All supported releases of VMware vSphere

**Known Issues with NVIDIA vGPU (C-Series) Migration Support**

| Use Case | Affected GPUs | Issue |
|----|----|----|
| Migration between hosts with different ECC memory configuration | All GPUs that support vGPU migration | Migration of VMs configured with vGPU stops before the migration is complete |

Table 19 Requirements for Using NVIDIA vGPU (C-Series) on GPUs Requiring 64 GB or More of MMIO Space with Large-Memory VMs[\#](#id154 "Link to this table") {#id154}

<a id="vgpus-that-support-multiple-vgpus-assigned-to-a-vm"></a>

##### vGPUs that Support Multiple vGPUs Assigned to a VM
The supported vGPUs depend on the hypervisor:

- For Linux with KVM hypervisors listed in [NVIDIA AI Enterprise Infrastructure Support Matrix](../support/support-matrix.html#support-matrix), Red Hat Enterprise Linux KVM, and Ubuntu, **all** NVIDIA vGPU (C-Series) are supported with PCIe GPUs. On GPUs that support the Multi-Instance GPU (MIG) feature, both time-sliced and MIG-backed vGPUs are supported.

- For VMware vSphere, the supported vGPUs depend on the hypervisor release:

  - **Since VMware vSphere 8.0**: All NVIDIA vGPU (C-Series) are supported. On GPUs that support the Multi-Instance GPU (MIG) feature, both time-sliced and MIG-backed vGPUs are supported.

  - **VMware vSphere 7.x releases**: Only NVIDIA vGPU (C-Series) allocated all of the physical GPU’s framebuffer are supported.

You can assign multiple vGPUs with differing amounts of frame buffer to a single VM, provided the board type and the series of all the vGPUs are the same. For example, you can assign an A40-48C vGPU and an A40-16C vGPU to the same VM. However, you cannot assign an A30-8C vGPU and an A16-8C vGPU to the same VM.

[TABLE]

Table 20 Multiple vGPU Support on the NVIDIA Ada Lovelace Architecture[\#](#id155 "Link to this table") {#id155}

[TABLE]

Table 21 Multiple vGPU Support on the NVIDIA Ampere GPU Architecture[\#](#id156 "Link to this table") {#id156}

| Board                             | vGPU [^1]                   |
|-----------------------------------|-----------------------------|
| NVIDIA H800 PCIe 94GB (H800 NVL)  | All NVIDIA vGPU (C-Series)  |
| NVIDIA H800 PCIe 80GB             | All NVIDIA vGPU (C-Series)  |
| NVIDIA H800 SXM5 80GB             | NVIDIA vGPU (C-Series) [^2] |
| NVIDIA H200 PCIe 141GB (H200 NVL) | All NVIDIA vGPU (C-Series)  |
| NVIDIA H200 SXM5 141GB            | NVIDIA vGPU (C-Series) [^3] |
| NVIDIA H100 PCIe 94GB (H100 NVL)  | All NVIDIA vGPU (C-Series)  |
| NVIDIA H100 SXM5 94GB             | NVIDIA vGPU (C-Series) [^4] |
| NVIDIA H100 PCIe 80GB             | All NVIDIA vGPU (C-Series)  |
| NVIDIA H100 SXM5 80GB             | NVIDIA vGPU (C-Series) [^5] |
| NVIDIA H100 SXM5 64GB             | NVIDIA vGPU (C-Series) [^6] |
| NVIDIA H20 SXM5 141GB             | NVIDIA vGPU (C-Series) [^7] |
| NVIDIA H20 SXM5 96GB              | NVIDIA vGPU (C-Series) [^8] |

Table 22 Multiple vGPU Support on the NVIDIA Hopper GPU Architecture[\#](#id157 "Link to this table") {#id157}

[TABLE]

Table 23 Multiple vGPU Support on the NVIDIA Turing GPU Architecture[\#](#id158 "Link to this table") {#id158}

[TABLE]

Table 24 Multiple vGPU Support on the NVIDIA Volta GPU Architecture[\#](#id159 "Link to this table") {#id159}

<a id="vgpus-that-support-peer-to-peer-cuda-transfers"></a>

##### vGPUs that Support Peer-to-Peer CUDA Transfers
Only C-series time-sliced vGPUs allocated all of the physical GPU framebuffer on physical GPUs that support NVLink are supported.

[TABLE]

Table 25 Peer-to-Peer CUDA Transfer Support on the NVIDIA Ampere GPU Architecture[\#](#id160 "Link to this table") {#id160}

| Board                             | vGPU       |
|-----------------------------------|------------|
| NVIDIA H800 PCIe 94GB (H800 NVL)  | H800L-94C  |
| NVIDIA H800 PCIe 80GB             | H800-80C   |
| NVIDIA H200 PCIe 141GB (H200 NVL) | H200-141C  |
| NVIDIA H200 SXM5 141GB            | H200X-141C |
| NVIDIA H100 PCIe 94GB (H100 NVL)  | H100L-94C  |
| NVIDIA H100 SXM5 94GB             | H100XL-94C |
| NVIDIA H100 PCIe 80GB             | H100-80C   |
| NVIDIA H100 SXM5 80GB             | H100XM-80C |
| NVIDIA H100 SXM5 64GB             | H100XS-64C |
| NVIDIA H20 SXM5 141GB             | H20X-141C  |
| NVIDIA H20 SXM5 96GB              | H20-96C    |

Table 26 Peer-to-Peer CUDA Transfer Support on the NVIDIA Hopper GPU Architecture[\#](#id161 "Link to this table") {#id161}

| Board                   | vGPU         |
|-------------------------|--------------|
| Quadro RTX 8000 passive | RTX8000P-48C |
| Quadro RTX 6000 passive | RTX6000P-24C |

Table 27 Peer-to-Peer CUDA Transfer Support on the NVIDIA Turing GPU Architecture[\#](#id162 "Link to this table") {#id162}

| Board                | vGPU       |
|----------------------|------------|
| Tesla V100 SXM2      | V100X-16C  |
| Tesla V100 SXM2 32GB | V100DX-32C |

Table 28 Peer-to-Peer CUDA Transfer Support on the NVIDIA Volta GPU Architecture[\#](#id163 "Link to this table") {#id163}

<a id="gpudirect-technology"></a>

#### GPUDirect Technology
NVIDIA GPUDirect Remote Direct Memory Access (RDMA) technology enables network devices to access the vGPU frame buffer directly, bypassing CPU host memory altogether. GPUDirect Storage technology enables a direct data path for direct memory access (DMA) transfers between GPU and storage. GPUDirect technology is supported only on a subset of vGPUs and guest OS releases.

**Supported vGPUs**

GPUDirect RDMA and GPUDirect Storage technology are supported on all time-sliced and MIG-backed NVIDIA vGPU (C-Series) on physical GPUs that support single root I/O virtualization (SR-IOV).

GPUs are based on the following GPU architectures:

NVIDIA Ada Lovelace

- NVIDIA L40

- NVIDIA L40S

- NVIDIA L20

- NVIDIA L20 liquid-cooled

- NVIDIA L4

- NVIDIA L2

- NVIDIA RTX 6000 Ada

- NVIDIA RTX 5880 Ada

- NVIDIA RTX 5000 Ada

NVIDIA Ampere

- NVIDIA A800 PCIe 80GB

- NVIDIA A800 PCIe 80GB liquid-cooled

- NVIDIA A800 HGX 80GB

- NVIDIA AX800

- NVIDIA A800 PCIe 40GB active-cooled

- NVIDIA A100 PCIe 80GB

- NVIDIA A100 PCIe 80GB liquid-cooled

- NVIDIA A100 HGX 80GB

- NVIDIA A100 PCIe 40GB

- NVIDIA A100 HGX 40GB

- NVIDIA A100X

- NVIDIA A40

- NVIDIA A30

- NVIDIA A30 liquid-cooled

- NVIDIA A30X

- NVIDIA A16

- NVIDIA A10

- NVIDIA A2

- NVIDIA RTX A6000

- NVIDIA RTX A5500

- NVIDIA RTX A5000

NVIDIA Hopper

- NVIDIA H800 PCIe 94GB (H800 NVL)

- NVIDIA H800 PCIe 80GB

- NVIDIA H800 SXM5 80GB

- NVIDIA H200 PCIe 141GB (H200 NVL)

- NVIDIA H200 SXM5 141GB

- NVIDIA H100 PCIe 94GB (H100 NVL)

- NVIDIA H100 SXM5 94GB

- NVIDIA H100 PCIe 80GB

- NVIDIA H100 SXM5 80GB

- NVIDIA H100 SXM5 64GB

- NVIDIA H20 SXM5 141GB

- NVIDIA H20 SXM5 96G

**Supported Guest OS Releases**

Linux only. GPUDirect technology is **not** supported on Windows.

**Supported Network Interface Cards**

GPUDirect technology is supported on the following network interface cards:

- NVIDIA ConnectX- 7 SmartNIC

- Mellanox Connect-X 6 SmartNIC

- Mellanox Connect-X 5 Ethernet adapter card

**Limitations**

Starting with GPUDirect Storage technology release 1.7.2, the following limitations apply:

- GPUDirect Storage technology is not supported on GPUs based on the NVIDIA Ampere GPU architecture.

- On GPUs based on the NVIDIA Hopper GPU architecture and the NVIDIA Ada Lovelace GPU architecture, GPUDirect Storage technology is supported only with the guest driver for Linux based on NVIDIA Linux open GPU kernel modules.

GPUDirect Storage technology releases before 1.7.2 are supported only with guest drivers with Linux kernel versions earlier than 6.6.

GPUDirect Storage technology is supported only on the following guest OS releases:

- Ubuntu 22.04 LTS

- Ubuntu 20.04 LTS

<a id="nvidia-nvswitch-on-chip-memory-fabric"></a>

#### NVIDIA NVSwitch On-Chip Memory Fabric
NVIDIA NVSwitch on-chip memory fabric enables peer-to-peer vGPU communication within a single node over the NVLink fabric. It is supported only on a subset of hardware platforms, vGPUs, hypervisor software releases, and guest OS releases.

For information about using the NVSwitch on-chip memory fabric, refer to the [Fabric Manager for NVIDIA NVSwitch Systems User Guide](https://docs.nvidia.com/datacenter/tesla/pdf/fabric-manager-user-guide.pdf).

**Hardware Platforms**

- NVIDIA HGX H800 8-GPU baseboard

- NVIDIA HGX H100 8-GPU baseboard

- NVIDIA HGX A100 8-GPU baseboard

**Supported vGPUs**

Only the following C-series time-sliced vGPUs that are allocated all of the physical GPU’s framebuffer are supported:

- NVIDIA H800

- NVIDIA H200 HGX

- NVIDIA H100 SXM5

- NVIDIA H20

- NVIDIA A800

- NVIDIA A100 HGX

| Board                  | vGPU       |
|------------------------|------------|
| NVIDIA H800 SXM5 80GB  | H800XM-80C |
| NVIDIA H200 SXM5 141GB | H200X-141C |
| NVIDIA H100 SXM5 80GB  | H100XM-80C |
| NVIDIA H20 SXM5 141GB  | H20X-141C  |
| NVIDIA H20 SXM5 96GB   | H20-96C    |

Table 29 NVIDIA NVSwitch On-Chip Memory Fabric Support on the NVIDIA Hopper GPU Architecture[\#](#id164 "Link to this table") {#id164}

| Board                | vGPU       |
|----------------------|------------|
| NVIDIA A800 HGX 80GB | A800DX-80C |
| NVIDIA A100 HGX 80GB | A100DX-80C |
| NVIDIA A100 HGX 40GB | A100X-40C  |

Table 30 NVIDIA NVSwitch On-Chip Memory Fabric Support on the NVIDIA Ampere GPU Architecture[\#](#id165 "Link to this table") {#id165}

**Hypervisor Releases**

Consult the documentation from your hypervisor vendor for information about which generic Linux with KVM hypervisor software releases supports NVIDIA NVSwitch on-chip memory fabric.

All supported Red Hat Enterprise Linux KVM releases support NVIDIA NVSwitch on-chip memory fabric.

On the Ubuntu hypervisor, NVSwitch is not supported.

The earliest VMware vSphere Hypervisor (ESXi) release that supports NVIDIA NVSwitch on-chip memory fabric depends on the GPU architecture.

| GPU Architecture | Earliest Supported VMware vSphere Hypervisor (ESXi) Release |
|----|----|
| NVIDIA Hopper | VMware vSphere Hypervisor (ESXi) 8 update 2 |
| NVIDIA Ampere | VMware vSphere Hypervisor (ESXi) 8 update 1 |

Table 31 Hypervisor Releases that Support NVIDIA NVSwitch On-Chip Memory Fabric[\#](#id166 "Link to this table") {#id166}

**Guest OS Releases**

Linux only. NVIDIA NVSwitch on-chip memory fabric is **not** supported on Windows.

**Limitations**

- Only time-sliced vGPUs are supported. MIG-backed vGPUs are **not** supported.

- On the Ubuntu hypervisor, NVSwitch is **not** supported.

- GPU passthrough is **not** supported.

- SLI is not supported.

- All vGPUs communicating peer-to-peer must be assigned to the same VM.

- On GPUs based on the NVIDIA Hopper GPU architecture, multicast is **not** supported.

<a id="nvlink-multicast"></a>

#### NVLink Multicast
NVLink multicast support requires that unified memory is enabled. For more information about enabling unified memory, refer to the [Enabling Unified Memory for a vGPU](https://docs.nvidia.com/vgpu/17.0/grid-vgpu-user-guide/index.html#enabling-unified-memory-vgpu) section.

Only full-sized, time-sliced NVIDIA vGPUs (C-Series) support NVLink multicast.

| Board                | vGPU              |
|----------------------|-------------------|
| NVIDIA HGX H800      | NVIDIA H800XM-80C |
| NVIDIA HGX H200      | NVIDIA H200X-141C |
| NVIDIA HGX H100      | NVIDIA H100XM-80C |
| NVIDIA H20 HGX 141GB | H20X-141C         |
| HGX H20 96GB         | NVIDIA H20-96C    |

Table 32 NVIDIA NVLink Multicast Support on the NVIDIA Hopper GPU Architecture[\#](#id167 "Link to this table") {#id167}

<a id="vgpus-that-support-unified-memory"></a>

#### vGPUs that Support Unified Memory
All MIG-backed vGPUs are supported on GPUs that support the Multi-Instance GPU (MIG) feature. Only time-sliced NVIDIA vGPUs (C-Series) that allocate all of the physical GPU’s frame buffer on physical GPUs that support unified memory are supported.

[TABLE]

Table 33 Unified Memory Support on the NVIDIA Ada Lovelace GPU Architecture[\#](#id168 "Link to this table") {#id168}

[TABLE]

Table 34 Unified Memory Support on the NVIDIA Ampere GPU Architecture[\#](#id169 "Link to this table") {#id169}

[TABLE]

Table 35 Unified Memory Support on the NVIDIA Hopper GPU Architecture[\#](#id170 "Link to this table") {#id170}

<a id="limitations"></a>

### Limitations
<a id="total-frame-buffer-for-vgpus-is-less-than-the-total-frame-buffer-on-the-physical-gpu"></a>

#### Total Frame Buffer for vGPUs is Less Than the Total Frame Buffer on the Physical GPU
The hypervisor uses some of the physical GPU’s frame buffer on behalf of the VM for allocations that the guest OS would otherwise have made in its frame buffer. The frame buffer used by the hypervisor is not available for vGPUs on the physical GPU. In NVIDIA vGPU deployments, the frame buffer for the guest OS is reserved in advance, whereas in bare-metal deployments, the frame buffer for the guest OS is reserved based on the runtime needs of applications.

If error-correcting code (ECC) memory is enabled on a physical GPU that does not have HBM2 memory, the amount of frame buffer usable by vGPUs is further reduced. All types of vGPUs are affected, not just those that support ECC memory.

An additional frame buffer is allocated for dynamic page retirement on all GPUs that support ECC memory and, therefore, dynamic page retirement. The allocated amount is inversely proportional to the maximum number of vGPUs per physical GPU. All GPUs that support ECC memory are affected, even those with HBM2 memory or for which ECC memory is disabled.

The approximate amount of frame buffer that NVIDIA AI Enterprise reserves can be calculated from the following formula:

    max-reserved-fb = vgpu-profile-size-in-mb÷16 + 16 + ecc-adjustments + page-retirement-allocation + compression-adjustment

`max-reserved-fb` - The total amount of reserved frame buffer in Mbytes that is unavailable for vGPUs.

`vgpu-profile-size-in-mb` - The amount of frame buffer allocated to a single vGPU in Mbytes. This amount depends on the vGPU type. For example, for the T4-16Q vGPU type, `vgpu-profile-size-in-mb` is 16384.

`ecc-adjustments` - The amount of frame buffer in Mbytes that is not usable by vGPUs when ECC is enabled on a physical GPU that does not have HBM2 memory.

- If ECC is enabled on a physical GPU that does not have HBM2 memory, `ecc-adjustments` is `fb-without-ecc/16`, equivalent to 64 Mbytes for every Gbyte of frame buffer assigned to the vGPU. `fb-without-ecc` is the total amount of frame buffer with ECC disabled.

- If ECC is disabled or the GPU has HBM2 memory, `ecc-adjustments` is 0.

`page-retirement-allocation` - The amount of frame buffer in Mbytes reserved for dynamic page retirement.

- On GPUs based on the NVIDIA Maxwell GPU architecture, `page-retirement-allocation`` ``=`` ``4÷max-vgpus-per-gpu`.

- On GPUs based on NVIDIA GPU architectures after the Maxwell architecture, `page-retirement-allocation`` ``=`` ``128÷max-vgpus-per-gpu`.

`max-vgpus-per-gpu` - The maximum number of vGPUs that can be created simultaneously on a physical GPU. This number varies according to the vGPU type. For example, for the T4-16Q vGPU type, `max-vgpus-per-gpu` is 1.

`compression-adjustment` - The amount of frame buffer in Mbytes that is reserved for the higher compression overhead in vGPU types with 12 Gbytes or more of frame buffer on GPUs based on the Turing architecture. `compression-adjustment` depends on the vGPU type, as shown in the following table.

| vGPU Type    | Compression Adjustment (MB) |
|--------------|-----------------------------|
| T4-16C       | 28                          |
| RTX6000-12C  | 32                          |
| RTX6000-24C  | 104                         |
| RTX6000P-12C | 32                          |
| RTX6000P-24C | 104                         |
| RTX8000-12C  | 32                          |
| RTX8000-16C  | 64                          |
| RTX8000-24C  | 96                          |
| RTX8000-48C  | 238                         |
| RTX8000P-12C | 32                          |
| RTX8000P-16C | 64                          |
| RTX8000P-24C | 96                          |
| RTX8000P-48C | 238                         |

Table 36 Total frame buffer for vGPUs is less than the total frame buffer on the physical GPU[\#](#id171 "Link to this table") {#id171}

For all other vGPU types, `compression-adjustment` is 0.

<a id="single-vgpu-benchmark-scores-are-lower-than-passthrough-gpu"></a>

#### Single vGPU Benchmark Scores are Lower Than Passthrough GPU
**Description**

A single vGPU configured on a physical GPU produces lower benchmark scores than the physical GPU run in passthrough mode.

Aside from performance differences that may be attributed to a vGPU’s smaller frame buffer size, vGPU incorporates a performance balancing feature known as a Frame Rate Limiter (FRL). On vGPUs that use the best-effort scheduler, FRL is enabled. On vGPUs that use the fixed share or equal share scheduler, FRL is disabled.

FRL ensures balanced performance across multiple vGPUs resident on the same physical GPU. The FRL setting is designed to give a good interactive remote graphics experience. Still, it may reduce scores in benchmarks that depend on measuring frame rendering rates compared to the same benchmarks running on a passthrough GPU.

**Resolution**

An internal vGPU setting controls FRL. On vGPUs that use the best-effort scheduler, NVIDIA does not validate a vGPU with FRL disabled. Still, for benchmark performance validation, FRL can be temporarily disabled by adding the configuration parameter `pciPassthru0.cfg.frame_rate_limiter` in the VM’s advanced configuration options.

Note

This setting can only be changed when the VM is powered off.

1.  Select **Edit Settings**.

2.  In the Edit Settings window, select the **VM Options** tab.

3.  From the **Advanced** drop-down list, select **Edit Configuration**.

4.  In the Configuration Parameters dialog box, click **Add Row**.

5.  In the **Name** field, type the parameter `pciPassthru0.cfg.frame_rate_limiter`.

6.  In the **Value** field, type `0` and click **OK**.

[![Single vGPU benchmark scores are lower than passthrough GPU](../_images/vm-config-param-advanced.png)](../_images/vm-config-param-advanced.png)

With this setting, the VM’s vGPU will run without any frame rate limit. The FRL can be reverted to its default setting by setting `pciPassthru0.cfg.frame_rate_limiter` to `1` or removing the parameter from the advanced settings.

**Resolution**

An internal vGPU setting controls FRL. On vGPUs that use the best-effort scheduler, NVIDIA does not validate a vGPU with FRL disabled, but for benchmark performance validation, FRL can be temporarily disabled by setting `frame_rate_limiter=0` in the vGPU configuration file.

    # echo "frame_rate_limiter=0" > /sys/bus/mdev/devices/vgpu-id/nvidia/vgpu_params

For example:

    # echo "frame_rate_limiter=0" > /sys/bus/mdev/devices/aa618089-8b16-4d01-a136-25a0f3c73123/nvidia/vgpu_params

The setting takes effect the next time any VM using the given vGPU type is started.

With this setting, the VM’s vGPU will run without any frame rate limit.

The FRL can be reverted to its default setting as follows:

1.  Clear all parameter settings in the vGPU configuration file.

        # echo " " > /sys/bus/mdev/devices/vgpu-id/nvidia/vgpu_params

    Note

    You cannot clear specific parameter settings. If your vGPU configuration file contains other parameter settings that you want to keep, you must reinstate them in the next step.

2.  Set `frame_rate_limiter=1` in the vGPU configuration file.

        # echo "frame_rate_limiter=1" > /sys/bus/mdev/devices/vgpu-id/nvidia/vgpu_params

    If you need to reinstate other parameter settings, include them in the command to set `frame_rate_limiter=1`. For example:

        # echo "frame_rate_limiter=1 disable_vnc=1" > /sys/bus/mdev/devices/aa618089-8b16-4d01-a136-25a0f3c73123/nvidia/vgpu_params

<a id="user-guide"></a>

## User Guide
<a id="installing-the-nvidia-virtual-gpu-manager"></a>

### Installing the NVIDIA Virtual GPU Manager
<a id="nvidia-virtual-gpu-manager-for-red-hat-enterprise-linux-kvm"></a>

#### NVIDIA Virtual GPU Manager for Red Hat Enterprise Linux KVM
This topic assumes you want to set up a single Red Hat Enterprise Linux Kernel-based Virtual Machine (KVM) VM to use NVIDIA vGPU.

Caution

Output from the VM console is unavailable for VMs running vGPU. Before configuring vGPU, ensure you have installed an alternate means of accessing the VM (such as a VNC server).

Follow this sequence of instructions:

1.  Install the Virtual GPU Manager Package for Red Hat Enterprise Linux KVM

2.  Verify the Installation of the NVIDIA AI Enterprise for Red Hat Enterprise Linux KVM

3.  **MIG-backed vGPUs only**: Configure a GPU for MIG-Backed vGPUs

4.  **vGPUs that support SR-IOV only**: Prepare the Virtual Function for an NVIDIA vGPU that Supports SR-IOV on a Linux with KVM Hypervisor

5.  **Optional**: Put a GPU into Mixed-Size Mode

6.  Get the BDF and Domain of a GPU on a Linux with KVM Hypervisor

7.  Create an NVIDIA vGPU on a Linux with KVM Hypervisor

8.  Add one or more vGPUs to a Linux with KVM Hypervisor VM

9.  **Optional**: Place a vGPU on a Physical GPU in Mixed-Size Mode

10. Set the vGPU Plugin Parameters on a Linux with KVM Hypervisor

After the process, you can install the NVIDIA vGPU (C-Series) Driver for your guest OS and license any NVIDIA AI Enterprise-licensed products you use.

<a id="nvidia-virtual-gpu-manager-for-ubuntu"></a>

#### NVIDIA Virtual GPU Manager for Ubuntu
Caution

Output from the VM console is unavailable for VMs running vGPU. Before configuring vGPU, ensure you have installed an alternate means of accessing the VM (such as a VNC server).

Follow this sequence of instructions to set up a single Ubuntu VM to use NVIDIA vGPU.

1.  Install the NVIDIA Virtual GPU Manager for Ubuntu

2.  **MIG-backed vGPUs only**: Configure a GPU for MIG-Backed vGPUs

3.  Get the BDF and Domain of a GPU on a Linux with KVM Hypervisor

4.  **vGPUs that support SR-IOV only**: Prepare the Virtual Function for an NVIDIA vGPU that Supports SR-IOV on a Linux with KVM Hypervisor

5.  **Optional**: Put a GPU Into Mixed-Size Mode

6.  Create an NVIDIA vGPU on a Linux with KVM Hypervisor

7.  Add one or more vGPUs to a Linux with KVM Hypervisor VM

8.  **Optional**: Place a vGPU on a Physical GPU in Mixed-Size Mode

9.  Set the vGPU Plugin Parameters on a Linux with KVM Hypervisor

After the process, you can install the NVIDIA vGPU (C-Series) Driver for your guest OS and license any NVIDIA AI Enterprise-licensed products you use.

<a id="nvidia-virtual-gpu-manager-for-vmware-vsphere"></a>

#### NVIDIA Virtual GPU Manager for VMware vSphere
You can use the NVIDIA Virtual GPU Manager for VMware vSphere to set up a VMware vSphere VM to use NVIDIA vGPU.

Note

Some servers, for example, the Dell R740, do not configure SR-IOV capability if the SR-IOV SBIOS setting is disabled on the server. If you are using the Tesla T4 GPU with VMware vSphere on such a server, you must ensure that the SR-IOV SBIOS setting is enabled on the server.

However, with any server hardware, SR-IOV is not enabled in the VMware vCenter Server for the Tesla T4 GPU. If SR-IOV is enabled in the VMware vCenter Server for T4, the GPU’s status is listed as needing a reboot. You can ignore this status message.

**Requirements for Configuring NVIDIA vGPU in a DRS Cluster**

You can configure a VM with NVIDIA vGPU on an ESXi host in a VMware Distributed Resource Scheduler (DRS) cluster. However, to ensure that the cluster’s automation level supports VMs configured with NVIDIA vGPU, you must set the automation level to **Partially Automated** or **Manual**.

For more information about these settings, refer to [Edit Cluster Settings](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.resmgmt.doc/GUID-755AB944-F3D0-43DD-82CD-8CDDDF8674E8.html) in the VMware documentation.

<a id="administering-mig-backed-nvidia-vgpus"></a>

### Administering MIG-Backed NVIDIA vGPUs
<a id="architecture"></a>

#### Architecture
A MIG-backed vGPU is a vGPU that resides on a GPU instance in a MIG-capable physical GPU. Each MIG-backed vGPU resident on a GPU has exclusive access to the GPU instance’s engines, including the compute and video decode engines.

In a MIG-backed vGPU, processes that run on the vGPU run in parallel with processes running on other vGPUs on the GPU. The process runs on all vGPUs resident on a physical GPU simultaneously.

[![MIG-Backed NVIDIA vGPU Internal Architecture](../_images/architecture-grid-vgpu-mig-backed-internal.png)](../_images/architecture-grid-vgpu-mig-backed-internal.png)

<a id="configurations-on-a-single-gpu"></a>

#### Configurations on a Single GPU
NVIDIA vGPU supports homogeneous and mixed MIG-backed virtual GPUs based on the underlying GPU instance configuration.

For example, an NVIDIA A100 PCIe 40GB card has one physical GPU and can support several types of virtual GPU. The figure shows examples of valid homogeneous and mixed MIG-backed virtual GPU configurations on NVIDIA A100 PCIe 40GB.

- A valid homogeneous configuration with 3 A100-2-10C vGPUs on 3 MIG.2g.10b GPU instances

- A valid homogeneous configuration with 2 A100-3-20C vGPUs on 3 MIG.3g.20b GPU instances

- A valid mixed configuration with 1 A100-4-20C vGPU on a MIG.4g.20b GPU instance, 1 A100-2-10C vGPU on a MIG.2.10b GPU instance, and 1 A100-1-5C vGPU on a MIG.1g.5b instance

[![Valid MIG-Backed Virtual GPU Configurations on a Single GPU](../_images/mixed-vgpu-configurations.png)](../_images/mixed-vgpu-configurations.png)

<a id="configuring-the-nvidia-virtual-gpu-manager"></a>

#### Configuring the NVIDIA Virtual GPU Manager
<a id="modifying-a-mig-backed-vgpu-s-configuration"></a>

##### Modifying a MIG-Backed vGPU’s Configuration
If compute instances weren’t created within the GPU instances when the GPU was configured for MIG-backed vGPUs, you can add the compute instances for an individual vGPU from within the guest VM. If you want to replace the compute instances created when the GPU was configured for MIG-backed vGPUs, you can delete them before adding the compute instances from within the guest VM.

Ensure that the following prerequisites are met:

- You have root user privileges in the guest VM.

- Other processes, such as CUDA applications, monitoring applications, or the `nvidia-smi` command, do not use the GPU instance.

Perform this task in a guest VM command shell.

1.  Open a command shell as the root user in the guest VM. You can use a secure shell (SSH) on all supported hypervisors. Individual hypervisors may provide additional means for logging in. For details, refer to the documentation for your hypervisor.

2.  List the available GPU instances.

        $ nvidia-smi mig -lgi
          +----------------------------------------------------+
          | GPU instances:                                     |
          | GPU   Name          Profile  Instance   Placement  |
          |                       ID       ID       Start:Size |
          |====================================================|
          |   0  MIG 2g.10gb       0        0          0:8     |
          +----------------------------------------------------+

3.  **Optional**: If compute instances were created when the GPU was configured for MIG-backed vGPUs that you no longer require, delete them.

        $ nvidia-smi mig -dci -ci compute-instance-id -gi gpu-instance-id

    `compute-instance-id` - The ID of the compute instance that you want to delete.

    `gpu-instance-id` - The ID of the GPU instance from which you want to delete the compute instance.

    Note

    This command fails if another process is using the GPU instance. In this situation, stop all processes using the GPU instance and retry the command.

    This example deletes `compute`` ``instance`` ``0` from GPU instance `0` on `GPU`` ``0`.

        $ nvidia-smi mig -dci -ci 0 -gi 0
        Successfully destroyed compute instance ID  0 from GPU  0 GPU instance ID  0

4.  List the compute instance profiles that are available for your GPU instance.

        $ nvidia-smi mig -lcip

    This example shows that one `MIG`` ``2g.10gb` compute instance or two `MIG`` ``1c.2g.10gb` compute instances can be created within the GPU instance.

        $ nvidia-smi mig -lcip
          +-------------------------------------------------------------------------------+
          | Compute instance profiles:                                                    |
          | GPU    GPU      Name          Profile  Instances   Exclusive      Shared      |
          |      Instance                   ID     Free/Total     SM      DEC   ENC   OFA |
          |        ID                                                     CE    JPEG      |
          |===============================================================================|
          |   0     0       MIG 1c.2g.10gb   0      2/2           14       1     0     0  |
          |                                                                2     0        |
          +-------------------------------------------------------------------------------+
          |   0     0       MIG 2g.10gb      1*     1/1           28       1     0     0  |
          |                                                                2     0        |
          +-------------------------------------------------------------------------------+

5.  Create the compute instances that you need within the available GPU instance. Run the following command to create each compute instance individually.

        $ nvidia-smi mig -cci compute-instance-profile-id -gi gpu-instance-id

    `compute-instance-profile-id` - The compute instance profile ID that specifies the compute instance.

    `gpu-instance-id` - The GPU instance ID specifies the GPU instance within which you want to create the compute instance.

    Note

    This command fails if another process is using the GPU instance. In this situation, stop all GPU processes and retry the command.

    This example creates a `MIG`` ``2g.10gb` compute instance on GPU instance 0.

        $ nvidia-smi mig -cci 1 -gi 0
        Successfully created compute instance ID  0 on GPU  0 GPU instance ID  0 using profile MIG 2g.10gb (ID  1)

    This example creates two `MIG`` ``1c.2g.10gb` compute instances on GPU instance 0 by running the same command twice.

        $ nvidia-smi mig -cci 0 -gi 0
        Successfully created compute instance ID  0 on GPU  0 GPU instance ID  0 using profile MIG 1c.2g.10gb (ID  0)
        $ nvidia-smi mig -cci 0 -gi 0
        Successfully created compute instance ID  1 on GPU  0 GPU instance ID  0 using profile MIG 1c.2g.10gb (ID  0)

6.  Verify that the compute instances were created within the GPU instance. Use the nvidia-smi command for this purpose. This example confirms that a `MIG`` ``2g.10gb` compute instance was created on GPU instance 0.

        nvidia-smi
          Mon Mar 25 19:01:24 2024
          +-----------------------------------------------------------------------------+
          | NVIDIA-SMI 550.54.16    Driver Version: 550.54.16   CUDA Version:  12.3     |
          |-------------------------------+----------------------+----------------------+
          | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
          | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
          |                               |                      |               MIG M. |
          |===============================+======================+======================|
          |   0  GRID A100X-2-10C     On  | 00000000:00:08.0 Off |                   On |
          | N/A   N/A    P0    N/A /  N/A |   1058MiB / 10235MiB |     N/A      Default |
          |                               |                      |              Enabled |
          +-------------------------------+----------------------+----------------------+

          +-----------------------------------------------------------------------------+
          | MIG devices:                                                                |
          +------------------+----------------------+-----------+-----------------------+
          | GPU  GI  CI  MIG |         Memory-Usage |        Vol|         Shared        |
          |      ID  ID  Dev |           BAR1-Usage | SM     Unc| CE  ENC  DEC  OFA  JPG|
          |                  |                      |        ECC|                       |
          |==================+======================+===========+=======================|
          |  0    0   0   0  |   1058MiB / 10235MiB | 28      0 |  2   0    1    0    0 |
          |                  |      0MiB /  4096MiB |           |                       |
          +------------------+----------------------+-----------+-----------------------+

          +-----------------------------------------------------------------------------+
          | Processes:                                                                  |
          |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
          |        ID   ID                                                   Usage      |
          |=============================================================================|
          |  No running processes found                                                 |
          +-----------------------------------------------------------------------------+

    This example confirms that two `MIG`` ``1c.2g.10gb` compute instances were created on GPU instance 0.

        $ nvidia-smi
          Mon Mar 25 19:01:24 2024
          +-----------------------------------------------------------------------------+
          | NVIDIA-SMI 550.54.16    Driver Version: 550.54.16   CUDA Version:  12.3     |
          |-------------------------------+----------------------+----------------------+
          | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
          | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
          |                               |                      |               MIG M. |
          |===============================+======================+======================|
          |   0  GRID A100X-2-10C     On  | 00000000:00:08.0 Off |                   On |
          | N/A   N/A    P0    N/A /  N/A |   1058MiB / 10235MiB |     N/A      Default |
          |                               |                      |              Enabled |
          +-------------------------------+----------------------+----------------------+

          +-----------------------------------------------------------------------------+
          | MIG devices:                                                                |
          +------------------+----------------------+-----------+-----------------------+
          | GPU  GI  CI  MIG |         Memory-Usage |        Vol|         Shared        |
          |      ID  ID  Dev |           BAR1-Usage | SM     Unc| CE  ENC  DEC  OFA  JPG|
          |                  |                      |        ECC|                       |
          |==================+======================+===========+=======================|
          |  0    0   0   0  |   1058MiB / 10235MiB | 14      0 |  2   0    1    0    0 |
          |                  |      0MiB /  4096MiB |           |                       |
          +------------------+                      +-----------+-----------------------+
          |  0    0   1   1  |                      | 14      0 |  2   0    1    0    0 |
          |                  |                      |           |                       |
          +------------------+----------------------+-----------+-----------------------+

          +-----------------------------------------------------------------------------+
          | Processes:                                                                  |
          |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
          |        ID   ID                                                   Usage      |
          |=============================================================================|
          |  No running processes found                                                 |
          +-----------------------------------------------------------------------------+

<a id="configuring-a-gpu-for-mig-backed-vgpus"></a>

##### Configuring a GPU for MIG-Backed vGPUs
To support GPU instances with NVIDIA vGPU, a GPU must be configured with MIG mode enabled, and GPU instances must be created and configured on the physical GPU. Optionally, you can create compute instances within the GPU instances. If you don’t create compute instances within the GPU instances, they can be added later for individual vGPUs from within the guest VMs.

Ensure that the following prerequisites are met:

- The NVIDIA Virtual GPU Manager is installed on the hypervisor host.

- You have root user privileges on your hypervisor host machine.

- You have determined which GPU instances correspond to the vGPU types of the MIG-backed vGPUs you will create.

- Other processes, such as CUDA applications, monitoring applications, or the `nvidia-smi` command, do not use the GPU.

To configure a GPU for MIG-backed vGPUs, follow these instructions:

1.  Enable MIG mode for a GPU.

    Note

    For VMware vSphere, only enabling MIG mode is required because VMware vSphere creates the GPU instances, and after the VM is booted and the guest driver is installed, one compute instance is automatically created in the VM.

2.  Create a GPU instance on a MIG-enabled GPU.

3.  **Optional**: Create a compute instance in a GPU instance.

After configuring a GPU for MIG-backed vGPUs, create the vGPUs you need and add them to their VMs.

<a id="enabling-mig-mode-for-a-gpu"></a>

###### Enabling MIG Mode for a GPU
Perform this task in your hypervisor command shell.

1.  Open a command shell as the root user on your hypervisor host machine. You can use a secure shell (SSH) on all supported hypervisors. Individual hypervisors may provide additional means for logging in. For details, refer to the documentation for your hypervisor.

2.  Determine whether MIG mode is enabled. Use the `nvidia-smi` command for this purpose. By default, MIG mode is disabled. This example shows that MIG mode is disabled on GPU 0.

    Note

    In the output from `nvidia-smi`, the NVIDIA A100 HGX 40GB GPU is referred to as A100-SXM4-40GB.

        $ nvidia-smi -i 0
            +-----------------------------------------------------------------------------+
            | NVIDIA-SMI 550.54.16   Driver Version: 550.54.16    CUDA Version:  12.3     |
            |-------------------------------+----------------------+----------------------+
            | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
            | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
            |                               |                      |               MIG M. |
            |===============================+======================+======================|
            |   0  A100-SXM4-40GB      On   | 00000000:36:00.0 Off |                    0 |
            | N/A   29C    P0    62W / 400W |      0MiB / 40537MiB |      6%      Default |
            |                               |                      |             Disabled |
            +-------------------------------+----------------------+----------------------+

3.  If MIG mode is disabled, enable it.

        $ nvidia-smi -i [gpu-ids] -mig 1

    `gpu-ids` - A comma-separated list of GPU indexes, PCI bus IDs, or UUIDs specifying the GPUs you want to enable MIG mode. If `gpu-ids` are omitted, MIG mode is enabled on all GPUs on the system.

    This example enables MIG mode on GPU 0.

        $ nvidia-smi -i 0 -mig 1
        Enabled MIG Mode for GPU 00000000:36:00.0
        All done.

    Note

    If another process is using the GPU, this command fails and displays a warning message that MIG mode for the GPU is in the pending enable state. In this situation, stop all GPU processes and retry the command.

4.  VMware vSphere ESXi with GPUs based only on the NVIDIA Ampere architecture: Reboot the hypervisor host. If you are using a different hypervisor or GPUs based on the NVIDIA Hopper GPU architecture or a later architecture, omit this step.

5.  Query the GPUs on which you enabled MIG mode to confirm that MIG mode is enabled. This example queries GPU 0 for the PCI bus ID and MIG mode in comma-separated values (CSV) format.

        $ nvidia-smi -i 0 --query-gpu=pci.bus_id,mig.mode.current --format=csv
        pci.bus_id, mig.mode.current
        00000000:36:00.0, Enabled

<a id="creating-gpu-instances-on-a-mig-enabled-gpu"></a>

###### Creating GPU Instances on a MIG-Enabled GPU
Note

If you are using VMware vSphere, omit this task. VMware vSphere creates the GPU instances automatically.

Perform this task in your hypervisor command shell.

1.  Open a command shell as the root user on your hypervisor host machine if necessary.

2.  List the GPU instance profiles that are available on your GPU. When you create a profile, you must specify the profiles by their IDs, not their names.

        $ nvidia-smi mig -lgip
          +--------------------------------------------------------------------------+
          | GPU instance profiles:                                                   |
          | GPU   Name          ID    Instances   Memory     P2P    SM    DEC   ENC  |
          |                           Free/Total   GiB              CE    JPEG  OFA  |
          |==========================================================================|
          |   0  MIG 1g.5gb     19     7/7        4.95       No     14     0     0   |
          |                                                          1     0     0   |
          +--------------------------------------------------------------------------+
          |   0  MIG 2g.10gb    14     3/3        9.90       No     28     1     0   |
          |                                                          2     0     0   |
          +--------------------------------------------------------------------------+
          |   0  MIG 3g.20gb     9     2/2        19.79      No     42     2     0   |
          |                                                          3     0     0   |
          +--------------------------------------------------------------------------+
          |   0  MIG 4g.20gb     5     1/1        19.79      No     56     2     0   |
          |                                                          4     0     0   |
          +--------------------------------------------------------------------------+
          |   0  MIG 7g.40gb     0     1/1        39.59      No     98     5     0   |
          |                                                          7     1     1   |
          +--------------------------------------------------------------------------+

3.  Create the GPU instances corresponding to the vGPU types of the MIG-backed vGPUs you will create.

    Note

    \$ nvidia-smi mig -cgi gpu-instance-profile-ids

    `gpu-instance-profile-ids` - A comma-separated list of GPU instance profile IDs specifying the GPU instances you want to create.

    This example creates two GPU instances of type `2g.10gb` with profile `ID`` ``14`.

        $ nvidia-smi mig -cgi 14,14
        Successfully created GPU instance ID  5 on GPU  2 using profile MIG 2g.10gb (ID 14)
        Successfully created GPU instance ID  3 on GPU  2 using profile MIG 2g.10gb (ID 14)

<a id="optional-creating-compute-instances-in-a-gpu-instance"></a>

###### Optional: Creating Compute Instances in a GPU Instance
Creating compute instances within GPU instances is optional. If you don’t create compute instances within the GPU instances, they can be added later for individual vGPUs from within the guest VMs.

Note

If you are using VMware vSphere, omit this task. One compute instance is automatically created after the VM is booted and the guest driver is installed.

Perform this task in your hypervisor command shell.

1.  Open a command shell as the root user on your hypervisor host machine if necessary.

2.  List the available GPU instances.

        $ nvidia-smi mig -lgi
          +----------------------------------------------------+
          | GPU instances:                                     |
          | GPU   Name          Profile  Instance   Placement  |
          |                       ID       ID       Start:Size |
          |====================================================|
          |   2  MIG 2g.10gb      14        3          0:2     |
          +----------------------------------------------------+
          |   2  MIG 2g.10gb      14        5          4:2     |
          +----------------------------------------------------+

3.  Create the compute instances that you need within each GPU instance.

        $ nvidia-smi mig -cci -gi gpu-instance-ids

    `gpu-instance-ids` - A comma-separated list of GPU instance IDs that specifies the GPU instances within which you want to create the compute instances.

    Caution

    To avoid an inconsistent state between a guest VM and the hypervisor host, do not create compute instances from the hypervisor on a GPU instance on which an active guest VM is running. Instead, create the compute instances from within the guest VM as explained in [Modifying a MIG-Backed vGPU’s Configuration](#modify-mig-backed-vgpus-config).

    This example creates a compute instance on each GPU instance 3 and 5.

        $ nvidia-smi mig -cci -gi 3,5
        Successfully created compute instance on GPU  0 GPU instance ID  1 using profile ID  2
        Successfully created compute instance on GPU  0 GPU instance ID  2 using profile ID  2

4.  Verify that the compute instances were created within each GPU instance.

        $ nvidia-smi
          +-----------------------------------------------------------------------------+
          | MIG devices:                                                                |
          +------------------+----------------------+-----------+-----------------------+
          | GPU  GI  CI  MIG |         Memory-Usage |        Vol|         Shared        |
          |      ID  ID  Dev |           BAR1-Usage | SM     Unc| CE  ENC  DEC  OFA  JPG|
          |                  |                      |        ECC|                       |
          |==================+======================+===========+=======================|
          |  2    3   0   0  |      0MiB /  9984MiB | 28      0 |  2   0    1    0    0 |
          |                  |      0MiB / 16383MiB |           |                       |
          +------------------+----------------------+-----------+-----------------------+
          |  2    5   0   1  |      0MiB /  9984MiB | 28      0 |  2   0    1    0    0 |
          |                  |      0MiB / 16383MiB |           |                       |
          +------------------+----------------------+-----------+-----------------------+

          +-----------------------------------------------------------------------------+
          | Processes:                                                                  |
          |  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
          |        ID   ID                                                   Usage      |
          |=============================================================================|

    Note

    Additional compute instances created in a VM are destroyed when the VM is shut down or rebooted. After the shutdown or reboot, only one compute instance remains in the VM. This compute instance is created automatically after installing the NVIDIA vGPU (C-Series) Driver.

<a id="disabling-mig-mode-for-one-or-more-gpus"></a>

###### Disabling MIG Mode for one or more GPUs
If a GPU you want to use for time-sliced vGPUs or GPU passthrough has previously been configured for MIG-backed vGPUs, disable MIG mode on the GPU.

Ensure that the following prerequisites are met:

- The NVIDIA Virtual GPU Manager is installed on the hypervisor host.

- You have root user privileges on your hypervisor host machine.

- Other processes, such as CUDA applications, monitoring applications, or the `nvidia-smi` command, do not use the GPU.

Perform this task in your hypervisor command shell.

1.  Open a command shell as the root user on your hypervisor host machine. You can use a secure shell (SSH) on all supported hypervisors. Individual hypervisors may provide additional means for logging in. For details, refer to the documentation for your hypervisor.

2.  Determine whether MIG mode is disabled. Use the `nvidia-smi` command for this purpose. By default, MIG mode is disabled but might have previously been enabled. This example shows that MIG mode is enabled on GPU 0.

    Note

    In the output from `nvidia-smi`, the NVIDIA A100 HGX 40GB GPU is referred to as A100-SXM4-40GB.

        $ nvidia-smi -i 0
          +-----------------------------------------------------------------------------+
          | NVIDIA-SMI 550.54.16    Driver Version: 550.54.16   CUDA Version:  12.3     |
          |-------------------------------+----------------------+----------------------+
          | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
          | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
          |                               |                      |               MIG M. |
          |===============================+======================+======================|
          |   0  A100-SXM4-40GB      Off  | 00000000:36:00.0 Off |                    0 |
          | N/A   29C    P0    62W / 400W |      0MiB / 40537MiB |      6%      Default |
          |                               |                      |              Enabled |
          +-------------------------------+----------------------+----------------------+

3.  If MIG mode is enabled, disable it.

        $ nvidia-smi -i [gpu-ids] -mig 0

    `gpu-ids` - A comma-separated list of GPU indexes, PCI bus IDs, or UUIDs specifying the GPUs you want to disable MIG mode. If `gpu-ids` are omitted, MIG mode is disabled for all GPUs in the system.

    This example disables MIG Mode on GPU 0.

        $ sudo nvidia-smi -i 0 -mig 0
        Disabled MIG Mode for GPU 00000000:36:00.0
        All done.

4.  Confirm that MIG mode was disabled. Use the `nvidia-smi` command for this purpose. This example shows that MIG mode is disabled on GPU 0.

        $ nvidia-smi -i 0
          +-----------------------------------------------------------------------------+
          | NVIDIA-SMI 550.54.16    Driver Version: 550.54.16   CUDA Version:  12.3     |
          |-------------------------------+----------------------+----------------------+
          | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
          | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
          |                               |                      |               MIG M. |
          |===============================+======================+======================|
          |   0  A100-SXM4-40GB      Off  | 00000000:36:00.0 Off |                    0 |
          | N/A   29C    P0    62W / 400W |      0MiB / 40537MiB |      6%      Default |
          |                               |                      |             Disabled |
          +-------------------------------+----------------------+----------------------+

<a id="monitoring-mig-backed-vgpu-activity"></a>

#### Monitoring MIG-backed vGPU Activity
Note

MIG-backed vGPU activity cannot be monitored on GPUs based on the NVIDIA Ampere GPU architecture because the required hardware feature is absent.

To monitor MIG-backed vGPU activity across multiple vGPUs, run `nvidia-smi`` ``vgpu` with the `--gpm-metrics`` ``ID-list` option.

`ID-list` - A comma-separated list of integer IDs that specify the statistics to monitor, as shown in the following table. The table also shows the column’s name in the command output under which the statistic is reported.

| Statistic | ID | Column |
|----|----|----|
| Graphics activity | 1 | `gract` |
| Streaming multiprocessor (SM) activity | 2 | `smutil` |
| SM occupancy | 3 | `smocc` |
| Integer activity | 4 | `intutil` |
| Tensor activity | 5 | `mmaact` |
| Double-precision fused multiply-add (DFMA) tensor activity | 6 | `dfmat` |
| Half matrix multiplication and accumulation (HMMA) tensor activity | 7 | `hmmat` |
| Integer matrix multiplication and accumulation (IMMA) tensor activity | 9 | `immat` |
| Dynamic random-access memory (DRAM) activity | 10 | `dram` |
| Double-precision 64-bit floating-point (FP64) activity | 11 | `fp64` |
| Single-precision 32-bit floating-point (FP32) activity | 12 | `fp32` |
| Half-precision 16-bit FP16 activity | 13 | `fp16` |

Table 37 Monitoring MIG-backed vGPU Activity[\#](#id172 "Link to this table") {#id172}

Each reported percentage is the percentage of the physical GPU’s capacity that a vGPU is using. For example, a vGPU that uses 20% of the GPU’s DRAM capacity will report 20%.

For each vGPU, the specified statistics are reported once every second.

To modify the reporting frequency, use the `-l` or `--loop` option.

To limit monitoring to a subset of the platform’s GPUs, use the `-i` or `--id` option to select one or more GPUs.

The following example reports graphics activity, SM activity, SM occupancy, and integer activity for one vGPU VM powered on and within which one application runs.

    [root@vgpu ~]# nvidia-smi vgpu --gpm-metrics 1,2,3,4
         # gpu        vgpu    mig_id       gi_id        ci_id       gract    smutil      smocc    intutil
         # Idx          Id       Idx         Idx          Idx           %         %          %          %
             0  3251634249          0           2            0           -         -          -          -
             0  3251634249          0           2            0          99        97         26         13
             0  3251634249          0           2            0          99        96         23         13
             0  3251634249          0           2            0          99        97         27         13

No activity is reported when no vGPUs are active on the hypervisor host.

    [root@vgpu ~]# nvidia-smi vgpu --gpm-metrics 1,2,3,4
         # gpu        vgpu    mig_id       gi_id        ci_id       gract    smutil      smocc    intutil
         # Idx          Id       Idx         Idx          Idx           %         %          %          %
             0            -         -           -            -           -         -          -          -
             0            -         -           -            -           -         -          -          -
             0            -         -           -            -           -         -          -          -

<a id="installing-nvidia-ai-enterprise-software-components"></a>

### Installing NVIDIA AI Enterprise Software Components
<a id="installing-the-nvidia-ai-enterprise-software-components-using-kubernetes"></a>

#### Installing the NVIDIA AI Enterprise Software Components Using Kubernetes
Perform this task if you are using one of the following combinations of guest operating system and container platform:

- Ubuntu with Kubernetes

Ensure that the following prerequisites are met:

1.  If you are using Kubernetes, ensure that:

    1.  [Kubernetes is installed](https://docs.nvidia.com/datacenter/cloud-native/index.html) in the VM.

    2.  [NVIDIA vGPU (C-Series) Virtual GPU Manager](https://docs.nvidia.com/vgpu/latest/grid-software-quick-start-guide/index.html#installing-configuring-vgpu-manager-guest-driver) is installed.

    3.  [NVIDIA vGPU License Server](https://docs.nvidia.com/vgpu/ls/latest/grid-license-server-user-guide/index.html) with licenses is installed.

2.  [Helm is installed](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/getting-started.html).

3.  You have [generated your NGC API key](https://docs.nvidia.com/ngc/gpu-cloud/ngc-user-guide/index.html#generating-api-key) to access the NVIDIA AI Enterprise Software on NGC Catalog using the URL provided to you by NVIDIA.

<a id="transforming-container-images-for-ai-and-data-science-applications-and-frameworks-into-kubernetes-pods"></a>

##### Transforming Container Images for AI and Data Science Applications and Frameworks into Kubernetes Pods
The AI and data science applications and frameworks are distributed as NGC container images through the NGC private registry. If you are using Kubernetes or Red Hat OpenShift, you must transform each image that you want to use into a Kubernetes pod. Each container image contains the entire user-space software stack required to run the application or framework: the CUDA libraries, cuDNN, any required Magnum IO components, TensorRT, and the framework.

<a id="installing-the-nvidia-ai-enterprise-application-software-and-deep-learning-framework-components-using-docker"></a>

#### Installing the NVIDIA AI Enterprise Application Software and Deep Learning Framework Components Using Docker
NVIDIA AI Enterprise Application Software is available through the [NGC Catalog](https://catalog.ngc.nvidia.com/?filters=productNames%7CNVIDIA+AI+Enterprise+Supported%7Cnvaie_supported&orderBy=weightPopularDESC&query=&page=&pageSize=) and identifiable by the NVIDIA AI Enterprise Supported label.

The container image for each application or framework contains the entire user-space software stack required to run it, namely, the CUDA libraries, cuDNN, any required Magnum IO components, TensorRT, and the framework.

Ensure that you have completed the following tasks in the NGC Private Registry User Guide:

- [Generating Your NGC API Key](https://docs.nvidia.com/ngc/gpu-cloud/ngc-private-registry-user-guide/index.html#generating-ngc-api-keys)

- [Accessing software on the NGC Catalog](https://docs.nvidia.com/ngc/gpu-cloud/ngc-catalog-user-guide/index.html#intro-to-ngc-cli)

Perform this task from the VM.

Obtain the Docker pull command to download the NVIDIA AI Enterprise Application Software you like to leverage from the [NGC Catalog](https://catalog.ngc.nvidia.com/?filters=productNames%7CNVIDIA+AI+Enterprise+Supported%7Cnvaie_supported&orderBy=weightPopularDESC&query=&page=&pageSize=).

<a id="installing-the-nvidia-gpu-operator-using-a-bash-shell-script"></a>

#### Installing the NVIDIA GPU Operator Using a Bash Shell Script
A bash shell script for installing the NVIDIA GPU Operator with the NVIDIA vGPU (C-Series) Driver is available for download from NVIDIA NGC.

Before performing this task, ensure that the following prerequisites are met:

- A [client configuration token](https://docs.nvidia.com/license-system/latest/nvidia-license-system-user-guide/index.html#generating-client-configuration-token) has been generated for the client on which the script will install the NVIDIA vGPU (C-Series) Driver.

- The NVIDIA NGC user’s [API key](https://docs.nvidia.com/ngc/gpu-cloud/ngc-private-registry-user-guide/index.html#generating-ngc-api-keys) to create the image pull secret has been generated.

- The following environment variables are set:

  - `NGC_API_KEY` - The NVIDIA NGC user’s API key to create the image pull secret. For example:

        export NGC_API_KEY="RLh1zerCiG4wPGWWt4Tyj2VMyd7T8MnDyCT95pygP5VJFv8en4eLvdXVZzjm"

  - `NGC_USER_EMAIL` - The email address of the NVIDIA NGC user to be used for creating the image pull secret. For example:

        export NGC_USER_EMAIL="ada.lovelace@example.com"

1.  Download the [NVIDIA GPU Operator - Deploy Installer Script](https://catalog.ngc.nvidia.com/orgs/nvidia/teams/vgpu/resources/gpu-operator-installer-5) from NVIDIA NGC.

2.  Ensure that the file access modes of the script allow the owner to execute the script.

    1.  Change to the directory that contains the script.

            # cd script-directory

        `script-directory` - The directory to which you downloaded the script in the previous step.

    2.  Determine the current file access modes of the script.

            # ls -l gpu-operator-nvaie.sh

    3.  If necessary, grant execute permission to the owner of the script.

            # chmod u+x gpu-operator-nvaie.sh

3.  Copy the client configuration token to the directory that contains the script.

4.  Rename the client configuration token to `client_configuration_token.tok`. The client configuration token is generated with a file name and a time stamp: `client_configuration_token_mm-dd-yyy-hh-mm-ss.tok`.

5.  Start the script from the directory that contains it, specifying the option to install the NVIDIA vGPU (C-Series) Driver.

        # bash gpu-operator-nvaie.sh install

<a id="virtual-gpu-types-for-supported-gpus"></a>

## Virtual GPU Types for Supported GPUs
<a id="nvidia-ada-lovelace-gpu-architecture"></a>

### NVIDIA Ada Lovelace GPU Architecture
Physical GPUs per board: 1

The maximum number of vGPUs per board is the product of the maximum number of vGPUs per GPU and the number of physical GPUs per board.

Required license edition: NVIDIA vGPU (C-Series)

Intended use cases:

- vGPUs with more than 4096 MB of frame buffer: Training Workloads

- vGPUs with 4096 MB of frame buffer: Inference Workloads

These vGPU types support a single display with a fixed maximum resolution.

NVIDIA L40

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^9] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| L40-48C | 49152 | 1 | 1 | 3840x2400 | 1 |
| L40-24C | 24576 | 2 | 2 | 3840x2400 | 1 |
| L40-16C | 16384 | 3 | 2 | 3840x2400 | 1 |
| L40-12C | 12288 | 4 | 4 | 3840x2400 | 1 |
| L40-8C | 8192 | 6 | 4 | 3840x2400 | 1 |
| L40-6C | 6144 | 8 | 8 | 3840x2400 | 1 |
| L40-4C | 4096 | 12 [^10] | 8 | 3840x2400 | 1 |

Table 38 NVIDIA vGPU (C-Series) for NVIDIA L40[\#](#id173 "Link to this table") {#id173}

NVIDIA L40S

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^11] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| L40S-48C | 49152 | 1 | 1 | 3840x2400 | 1 |
| L40S-24C | 24576 | 2 | 2 | 3840x2400 | 1 |
| L40S-16C | 16384 | 3 | 2 | 3840x2400 | 1 |
| L40S-12C | 12288 | 4 | 4 | 3840x2400 | 1 |
| L40S-8C | 8192 | 6 | 4 | 3840x2400 | 1 |
| L40S-6C | 6144 | 8 | 8 | 3840x2400 | 1 |
| L40S-4C | 4096 | 12 [^12] | 8 | 3840x2400 | 1 |

Table 39 NVIDIA vGPU (C-Series) for NVIDIA L40S[\#](#id174 "Link to this table") {#id174}

NVIDIA L20

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^13] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| L20-48C | 49152 | 1 | 1 | 3840x2400 | 1 |
| L20-24C | 24576 | 2 | 2 | 3840x2400 | 1 |
| L20-16C | 16384 | 3 | 2 | 3840x2400 | 1 |
| L20-12C | 12288 | 4 | 4 | 3840x2400 | 1 |
| L20-8C | 8192 | 6 | 4 | 3840x2400 | 1 |
| L20-6C | 6144 | 8 | 8 | 3840x2400 | 1 |
| L20-4C | 4096 | 12 [^14] | 8 | 3840x2400 | 1 |

Table 40 NVIDIA vGPU (C-Series) for NVIDIA L20[\#](#id175 "Link to this table") {#id175}

NVIDIA L20 Liquid-Cooled

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^15] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| L20-48C | 49152 | 1 | 1 | 3840x2400 | 1 |
| L20-24C | 24576 | 2 | 2 | 3840x2400 | 1 |
| L20-16C | 16384 | 3 | 2 | 3840x2400 | 1 |
| L20-12C | 12288 | 4 | 4 | 3840x2400 | 1 |
| L20-8C | 8192 | 6 | 4 | 3840x2400 | 1 |
| L20-6C | 6144 | 8 | 8 | 3840x2400 | 1 |
| L20-4C | 4096 | 12 [^16] | 8 | 3840x2400 | 1 |

Table 41 NVIDIA vGPU (C-Series) for NVIDIA L20 Liquid-Cooled[\#](#id176 "Link to this table") {#id176}

NVIDIA L4

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^17] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| L4-24C | 24576 | 1 | 1 | 3840x2400 | 1 |
| L4-12C | 12288 | 2 | 2 | 3840x2400 | 1 |
| L4-8C | 8192 | 3 | 2 | 3840x2400 | 1 |
| L4-6C | 6144 | 4 | 4 | 3840x2400 | 1 |
| L4-4C | 4096 | 6 | 4 | 3840x2400 | 1 |

Table 42 NVIDIA vGPU (C-Series) for NVIDIA L4[\#](#id177 "Link to this table") {#id177}

NVIDIA L2

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^18] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| L2-24C | 24576 | 1 | 1 | 3840x2400 | 1 |
| L2-12C | 12288 | 2 | 2 | 3840x2400 | 1 |
| L2-8C | 8192 | 3 | 2 | 3840x2400 | 1 |
| L2-6C | 6144 | 4 | 4 | 3840x2400 | 1 |
| L2-4C | 4096 | 6 | 4 | 3840x2400 | 1 |

Table 43 NVIDIA vGPU (C-Series) for NVIDIA L2[\#](#id178 "Link to this table") {#id178}

NVIDIA RTX 6000 Ada

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^19] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| RTX 6000 Ada-48C | 49152 | 1 | 1 | 3840x2400 | 1 |
| RTX 6000 Ada-24C | 24576 | 2 | 2 | 3840x2400 | 1 |
| RTX 6000 Ada-16C | 16384 | 3 | 2 | 3840x2400 | 1 |
| RTX 6000 Ada-12C | 12288 | 4 | 4 | 3840x2400 | 1 |
| RTX 6000 Ada-8C | 8192 | 6 | 4 | 3840x2400 | 1 |
| RTX 6000 Ada-6C | 6144 | 8 | 8 | 3840x2400 | 1 |
| RTX 6000 Ada-4C | 4096 | 12 [^20] | 8 | 3840x2400 | 1 |

Table 44 NVIDIA vGPU (C-Series) for NVIDIA RTX 6000 Ada[\#](#id179 "Link to this table") {#id179}

NVIDIA RTX 5880 Ada

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^21] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| RTX 5880 Ada-48C | 49152 | 1 | 1 | 3840x2400 | 1 |
| RTX 5880 Ada-24C | 24576 | 2 | 2 | 3840x2400 | 1 |
| RTX 5880 Ada-16C | 16384 | 3 | 2 | 3840x2400 | 1 |
| RTX 5880 Ada-12C | 12288 | 4 | 4 | 3840x2400 | 1 |
| RTX 5880 Ada-8C | 8192 | 6 | 4 | 3840x2400 | 1 |
| RTX 5880 Ada-6C | 6144 | 8 | 8 | 3840x2400 | 1 |
| RTX 5880 Ada-4C | 4096 | 12 [^22] | 8 | 3840x2400 | 1 |

Table 45 NVIDIA vGPU (C-Series) for NVIDIA RTX 5880 Ada[\#](#id180 "Link to this table") {#id180}

NVIDIA RTX 5000 Ada

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^23] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| RTX 5000 Ada-32C | 32768 | 1 | 1 | 3840x2400 | 1 |
| RTX 5000 Ada-16C | 16384 | 2 | 2 | 3840x2400 | 1 |
| RTX 5000 Ada-8C | 8192 | 4 | 4 | 3840x2400 | 1 |
| RTX 5000 Ada-4C | 4096 | 8 | 8 | 3840x2400 | 1 |

Table 46 NVIDIA vGPU (C-Series) for NVIDIA RTX 5000 Ada[\#](#id181 "Link to this table") {#id181}

<a id="nvidia-ampere-gpu-architecture"></a>

### NVIDIA Ampere GPU Architecture
Physical GPUs per board: 1 (with the exception of NVIDIA A16)

The maximum number of vGPUs per board is the product of the maximum number of vGPUs per GPU and the number of physical GPUs per board.

Required license edition: NVIDIA vGPU (C-Series)

Intended use cases:

- vGPUs with more than 4096 MB of frame buffer: Training Workloads

- vGPUs with 4096 MB of frame buffer: Inference Workloads

These vGPU types support a single display with a fixed maximum resolution.

NVIDIA A40

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^24] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A40-48C | 49152 | 1 | 1 | 3840x2400 | 1 |
| A40-24C | 24576 | 2 | 2 | 3840x2400 | 1 |
| A40-16C | 16384 | 3 | 2 | 3840x2400 | 1 |
| A40-12C | 12288 | 4 | 4 | 3840x2400 | 1 |
| A40-8C | 8192 | 6 | 4 | 3840x2400 | 1 |
| A40-6C | 6144 | 8 | 8 | 3840x2400 | 1 |
| A40-4C | 4096 | 12 [^25] | 8 | 3840x2400 | 1 |

Table 47 NVIDIA vGPU (C-Series) for NVIDIA A40[\#](#id182 "Link to this table") {#id182}

NVIDIA A16

Physical GPUs per board: 4

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^26] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A16-16C | 16384 | 1 | 1 | 3840x2400 | 1 |
| A16-8C | 8192 | 2 | 2 | 3840x2400 | 1 |
| A16-4C | 4096 | 4 | 4 | 3840x2400 | 1 |

Table 48 NVIDIA vGPU (C-Series) for NVIDIA A16[\#](#id183 "Link to this table") {#id183}

NVIDIA A10

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^27] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A10-24C | 24576 | 1 | 1 | 3840x2400 | 1 |
| A10-12C | 12288 | 2 | 2 | 3840x2400 | 1 |
| A10-8C | 8192 | 3 | 2 | 3840x2400 | 1 |
| A10-6C | 6144 | 4 | 4 | 3840x2400 | 1 |
| A10-4C | 4096 | 6 | 4 | 3840x2400 | 1 |

Table 49 NVIDIA vGPU (C-Series) for NVIDIA A10[\#](#id184 "Link to this table") {#id184}

NVIDIA RTX A6000

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^28] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| RTXA6000-48C | 49152 | 1 | 1 | 3840x2400 | 1 |
| RTXA6000-24C | 24576 | 2 | 2 | 3840x2400 | 1 |
| RTXA6000-16C | 16384 | 3 | 2 | 3840x2400 | 1 |
| RTXA6000-12C | 12288 | 4 | 4 | 3840x2400 | 1 |
| RTXA6000-8C | 8192 | 6 | 4 | 3840x2400 | 1 |
| RTXA6000-6C | 6144 | 8 | 8 | 3840x2400 | 1 |
| RTXA6000-4C | 4096 | 12 [^29] | 8 | 3840x2400 | 1 |

Table 50 NVIDIA vGPU (C-Series) for NVIDIA RTX A6000[\#](#id185 "Link to this table") {#id185}

NVIDIA RTX A5500

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^30] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| RTXA5500-24C | 24576 | 1 | 1 | 3840x2400 | 1 |
| RTXA5500-12C | 12288 | 2 | 2 | 3840x2400 | 1 |
| RTXA5500-8C | 8192 | 3 | 2 | 3840x2400 | 1 |
| RTXA5500-6C | 6144 | 4 | 4 | 3840x2400 | 1 |
| RTXA5500-4C | 4096 | 6 | 4 | 3840x2400 | 1 |

Table 51 NVIDIA vGPU (C-Series) for NVIDIA RTX A5500[\#](#id186 "Link to this table") {#id186}

NVIDIA RTX A5000

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^31] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| RTXA5000-24 | 24576 | 1 | 1 | 3840x2400 | 1 |
| RTXA5000-12C | 12288 | 2 | 2 | 3840x2400 | 1 |
| RTXA5000-8C | 8192 | 3 | 2 | 3840x2400 | 1 |
| RTXA5000-6C | 6144 | 4 | 4 | 3840x2400 | 1 |
| RTXA5000-4C | 4096 | 6 | 4 | 3840x2400 | 1 |

Table 52 NVIDIA vGPU (C-Series) for NVIDIA RTX A5000[\#](#id187 "Link to this table") {#id187}

<a id="mig-backed-and-time-sliced-nvidia-vgpu-c-series-for-the-nvidia-ampere-gpu-architecture"></a>

#### MIG-Backed and Time-Sliced NVIDIA vGPU (C-Series) for the NVIDIA Ampere GPU Architecture
Physical GPUs per board: 1

The maximum number of vGPUs per board is the product of the maximum number of vGPUs per GPU and the number of physical GPUs per board.

Required license edition: NVIDIA vGPU (C-Series)

**MIG-Backed NVIDIA vGPU (C-Series)**

For details on GPU instance profiles, refer to the [NVIDIA Multi-Instance GPU User Guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/).

**Time-Sliced NVIDIA vGPU (C-Series)**

Intended use cases:

- vGPUs with more than 4096 MB of frame buffer: Training Workloads

- vGPUs with 4096 MB of frame buffer: Inference Workloads

These vGPU types support a single display with a fixed maximum resolution.

NVIDIA A800 PCIe 80GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A800D-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| A800D-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| A800D-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| A800D-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| A800D-1-20C [^32] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| A800D-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| A800D-1-10CME [^33] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 53 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A800 PCIe 80GB[\#](#id188 "Link to this table") {#id188}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^34] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A800D-80C | 81920 | 1 | 1 | 3840x2400 | 1 |
| A800D-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| A800D-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| A800D-16C | 16384 | 5 | 4 | 3840x2400 | 1 |
| A800D-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| A800D-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| A800D-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 54 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A800 PCIe 80GB[\#](#id189 "Link to this table") {#id189}

NVIDIA A800 PCIe 80GB Liquid Cooled

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A800D-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| A800D-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| A800D-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| A800D-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| A800D-1-20C [^35] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| A800D-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| A800D-1-10CME [^36] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 55 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A800 PCIe 80GB Liquid-Cooled[\#](#id190 "Link to this table") {#id190}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^37] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A800D-80C | 81920 | 1 | 1 | 3840x2400 | 1 |
| A800D-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| A800D-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| A800D-16C | 16384 | 5 | 4 | 3840x2400 | 1 |
| A800D-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| A800D-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| A800D-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 56 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A800 PCIe 80GB Liquid-Cooled[\#](#id191 "Link to this table") {#id191}

NVIDIA AX800

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A800D-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| A800D-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| A800D-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| A800D-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| A800D-1-20C [^38] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| A800D-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| A800D-1-10CME [^39] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 57 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA AX800[\#](#id192 "Link to this table") {#id192}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^40] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A800D-80C | 81920 | 1 | 1 | 3840x2400 | 1 |
| A800D-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| A800D-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| A800D-16C | 16384 | 5 | 4 | 3840x2400 | 1 |
| A800D-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| A800D-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| A800D-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 58 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA AX800[\#](#id193 "Link to this table") {#id193}

NVIDIA A800 PCIe 40GB Active Cooled

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A800-7-40C | 40960 | 1 | 7 | 7 | MIG 7g.40gb |
| A800-4-20C | 20480 | 1 | 4 | 4 | MIG 4g.20gb |
| A800-3-20C | 20480 | 2 | 3 | 3 | MIG 3g.20gb |
| A800-2-10C | 10240 | 3 | 2 | 2 | MIG 2g.10gb |
| A800-1-10C [^41] | 10240 | 4 | 1 | 1 | MIG 1g.10gb |
| A800-1-5C | 5120 | 7 | 1 | 1 | MIG 1g.5gb |
| A800-1-5CME [^42] | 5120 | 1 | 1 | 1 | MIG 1g.5gb+me |

Table 59 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A800 PCIe 40GB Active Cooled[\#](#id194 "Link to this table") {#id194}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^43] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A800-40C | 40960 | 1 | 1 | 3840x2400 | 1 |
| A800-20C | 20480 | 2 | 2 | 3840x2400 | 1 |
| A800-10C | 10240 | 4 | 4 | 3840x2400 | 1 |
| A800-8C | 8192 | 5 | 4 | 3840x2400 | 1 |
| A800-5C | 5120 | 8 | 8 | 3840x2400 | 1 |
| A800-4C | 4096 | 10 | 8 | 3840x2400 | 1 |

Table 60 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A800 PCIe 40GB Active Cooled[\#](#id195 "Link to this table") {#id195}

NVIDIA A800 HGX 80GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A800DX-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| A800DX-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| A800DX-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| A800DX-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| A800DX-1-20C [^44] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| A800DX-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| A800DX-1-10CME [^45] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 61 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A800 HGX 80GB[\#](#id196 "Link to this table") {#id196}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^46] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A800DX-80C | 81920 | 1 | 1 | 3840x2400 | 1 |
| A800DX-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| A800DX-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| A800DX-16C | 16384 | 5 | 4 | 3840x2400 | 1 |
| A800DX-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| A800DX-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| A800DX-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 62 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A800 HGX 80GB[\#](#id197 "Link to this table") {#id197}

NVIDIA A100 PCIe 80GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A100D-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| A100D-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| A100D-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| A100D-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| A100D-1-20C [^47] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| A100D-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| A100D-1-10CME [^48] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 63 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A100 PCIe 80GB[\#](#id198 "Link to this table") {#id198}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^49] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A100D-80C | 81920 | 1 | 1 | 3840x2400 | 1 |
| A100D-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| A100D-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| A100D-16C | 16384 | 5 | 4 | 3840x2400 | 1 |
| A100D-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| A100D-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| A100D-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 64 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A100 PCIe 80GB[\#](#id199 "Link to this table") {#id199}

NVIDIA A100 PCIe 80GB Liquid-Cooled

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A100D-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| A100D-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| A100D-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| A100D-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| A100D-1-20C [^50] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| A100D-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| A100D-1-10CME [^51] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 65 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A100 PCIe 80GB Liquid-Cooled[\#](#id200 "Link to this table") {#id200}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^52] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A100D-80C | 81920 | 1 | 1 | 3840x2400 | 1 |
| A100D-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| A100D-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| A100D-16C | 16384 | 5 | 4 | 3840x2400 | 1 |
| A100D-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| A100D-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| A100D-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 66 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A100 PCIe 80GB Liquid-Cooled[\#](#id201 "Link to this table") {#id201}

NVIDIA A100X

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A100D-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| A100D-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| A100D-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| A100D-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| A100D-1-20C [^53] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| A100D-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| A100D-1-10CME [^54] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 67 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A100X[\#](#id202 "Link to this table") {#id202}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^55] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A100D-80C | 81920 | 1 | 1 | 3840x2400 | 1 |
| A100D-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| A100D-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| A100D-16C | 16384 | 5 | 4 | 3840x2400 | 1 |
| A100D-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| A100D-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| A100D-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 68 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A100X[\#](#id203 "Link to this table") {#id203}

NVIDIA A100 HGX 80GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A100DX-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| A100DX-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| A100DX-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| A100DX-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| A100DX-1-20C [^56] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| A100DX-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| A100DX-1-10CME [^57] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 69 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A100 HGX 80GB[\#](#id204 "Link to this table") {#id204}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^58] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A100DX-80C | 81920 | 1 | 1 | 3840x2400 | 1 |
| A100DX-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| A100DX-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| A100DX-16C | 16384 | 5 | 4 | 3840x2400 | 1 |
| A100DX-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| A100DX-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| A100DX-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 70 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A100 HGX 80GB[\#](#id205 "Link to this table") {#id205}

NVIDIA A100 PCIe 40GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A100-7-40C | 40960 | 1 | 7 | 7 | MIG 7g.40gb |
| A100-4-20C | 20480 | 1 | 4 | 4 | MIG 4g.20gb |
| A100-3-20C | 20480 | 2 | 3 | 3 | MIG 3g.20gb |
| A100-2-10C | 10240 | 3 | 2 | 2 | MIG 2g.10gb |
| A100-1-10C [^59] | 10240 | 4 | 1 | 1 | MIG 1g.10gb |
| A100-1-5C | 5120 | 7 | 1 | 1 | MIG 1g.5gb |
| A100-1-5CME [^60] | 5120 | 1 | 1 | 1 | MIG 1g.5gb+me |

Table 71 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A100 PCIe 40GB[\#](#id206 "Link to this table") {#id206}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^61] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A100-40C | 40960 | 1 | 1 | 3840x2400 | 1 |
| A100-20C | 20480 | 2 | 2 | 3840x2400 | 1 |
| A100-10C | 10240 | 4 | 4 | 3840x2400 | 1 |
| A100-8C | 8192 | 5 | 4 | 3840x2400 | 1 |
| A100-5C | 5120 | 8 | 8 | 3840x2400 | 1 |
| A100-4C | 4096 | 10 | 8 | 3840x2400 | 1 |

Table 72 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A100 PCIe 40GB[\#](#id207 "Link to this table") {#id207}

NVIDIA A100 HGX 40GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A100X-7-40C | 40960 | 1 | 7 | 7 | MIG 7g.40gb |
| A100X-4-20C | 20480 | 1 | 4 | 4 | MIG 4g.20gb |
| A100X-3-20C | 20480 | 2 | 3 | 3 | MIG 3g.20gb |
| A100X-2-10C | 10240 | 3 | 2 | 2 | MIG 2g.10gb |
| A100X-1-10C [^62] | 10240 | 4 | 1 | 1 | MIG 1g.10gb |
| A100X-1-5C | 5120 | 7 | 1 | 1 | MIG 1g.5gb |
| A100X-1-5CME [^63] | 5120 | 1 | 1 | 1 | MIG 1g.5gb+me |

Table 73 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A100 HGX 40GB[\#](#id208 "Link to this table") {#id208}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^64] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A100X-40C | 40960 | 1 | 1 | 3840x2400 | 1 |
| A100X-20C | 20480 | 2 | 2 | 3840x2400 | 1 |
| A100X-10C | 10240 | 4 | 4 | 3840x2400 | 1 |
| A100X-8C | 8192 | 5 | 4 | 3840x2400 | 1 |
| A100X-5C | 5120 | 8 | 8 | 3840x2400 | 1 |
| A100X-4C | 4096 | 10 | 8 | 3840x2400 | 1 |

Table 74 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A100 HGX 40GB[\#](#id209 "Link to this table") {#id209}

NVIDIA A30

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A30-4-24C | 24576 | 1 | 4 | 4 | MIG 4g.24gb |
| A30-2-12C | 12288 | 2 | 2 | 2 | MIG 2g.12gb |
| A30-2-12CME [^65] | 12288 | 1 | 2 | 2 | MIG 2g.12gb+me |
| A30-1-6C | 6144 | 4 | 1 | 1 | MIG 1g.6gb |
| A30-1-6CME [^66] | 6144 | 1 | 1 | 1 | MIG 1g.6gb+me |

Table 75 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A30[\#](#id210 "Link to this table") {#id210}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^67] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A30-24C | 24576 | 1 | 1 | 3840x2400 | 1 |
| A30-12C | 12288 | 2 | 2 | 3840x2400 | 1 |
| A30-8C | 8192 | 3 | 2 | 3840x2400 | 1 |
| A30-6C | 6144 | 4 | 4 | 3840x2400 | 1 |
| A30-4C | 4096 | 6 | 4 | 3840x2400 | 1 |

Table 76 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A30[\#](#id211 "Link to this table") {#id211}

NVIDIA A30X

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A30-4-24C | 24576 | 1 | 4 | 4 | MIG 4g.24gb |
| A30-2-12C | 12288 | 2 | 2 | 2 | MIG 2g.12gb |
| A30-2-12CME [^68] | 12288 | 1 | 2 | 2 | MIG 2g.12gb+me |
| A30-1-6C | 6144 | 4 | 1 | 1 | MIG 1g.6gb |
| A30-1-6CME [^69] | 6144 | 1 | 1 | 1 | MIG 1g.6gb+me |

Table 77 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A30X[\#](#id212 "Link to this table") {#id212}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^70] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A30-24C | 24576 | 1 | 1 | 3840x2400 | 1 |
| A30-12C | 12288 | 2 | 2 | 3840x2400 | 1 |
| A30-8C | 8192 | 3 | 2 | 3840x2400 | 1 |
| A30-6C | 6144 | 4 | 4 | 3840x2400 | 1 |
| A30-4C | 4096 | 6 | 4 | 3840x2400 | 1 |

Table 78 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A30X[\#](#id213 "Link to this table") {#id213}

NVIDIA A30 Liquid-Cooled

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| A30-4-24C | 24576 | 1 | 4 | 4 | MIG 4g.24gb |
| A30-2-12C | 12288 | 2 | 2 | 2 | MIG 2g.12gb |
| A30-2-12CME [^71] | 12288 | 1 | 2 | 2 | MIG 2g.12gb+me |
| A30-1-6C | 6144 | 4 | 1 | 1 | MIG 1g.6gb |
| A30-1-6CME [^72] | 6144 | 1 | 1 | 1 | MIG 1g.6gb+me |

Table 79 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA A30 Liquid-Cooled[\#](#id214 "Link to this table") {#id214}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^73] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| A30-24C | 24576 | 1 | 1 | 3840x2400 | 1 |
| A30-12C | 12288 | 2 | 2 | 3840x2400 | 1 |
| A30-8C | 8192 | 3 | 2 | 3840x2400 | 1 |
| A30-6C | 6144 | 4 | 4 | 3840x2400 | 1 |
| A30-4C | 4096 | 6 | 4 | 3840x2400 | 1 |

Table 80 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA A30 Liquid-Cooled[\#](#id215 "Link to this table") {#id215}

<a id="nvidia-hopper-gpu-architecture"></a>

### NVIDIA Hopper GPU Architecture
<a id="mig-backed-and-time-sliced-nvidia-vgpu-c-series-for-the-nvidia-hopper-gpu-architecture"></a>

#### MIG-Backed and Time-Sliced NVIDIA vGPU (C-Series) for the NVIDIA Hopper GPU Architecture
Physical GPUs per board: 1

The maximum number of vGPUs per board is the product of the maximum number of vGPUs per GPU and the number of physical GPUs per board.

Required license edition: NVIDIA vGPU (C-Series)

**MIG-Backed NVIDIA vGPU (C-Series)**

For details on GPU instance profiles, refer to the [NVIDIA Multi-Instance GPU User Guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/).

**Time-Sliced NVIDIA vGPU (C-Series)**

Intended use cases:

- vGPUs with more than 4096 MB of frame buffer: Training Workloads

- vGPUs with 4096 MB of frame buffer: Inference Workloads

These vGPU types support a single display with a fixed maximum resolution.

NVIDIA H800 PCIe 94GB (H800 NVL)

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H800L-7-94C | 96246 | 1 | 7 | 7 | MIG 7g.94gb |
| H800L-4-47C | 48128 | 1 | 4 | 4 | MIG 4g.47gb |
| H800L-3-47C | 48128 | 2 | 3 | 3 | MIG 3g.47gb |
| H800L-2-24C | 24672 | 3 | 2 | 2 | MIG 2g.24gb |
| H800L-1-24C | 24672 | 4 | 1 | 1 | MIG 1g.24gb |
| H800L-1-12C | 12288 | 7 | 1 | 1 | MIG 1g.12gb |
| H800L-1-12CME [^74] | 12288 | 1 | 1 | 1 | MIG 1g.12gb+me |

Table 81 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H800 PCIe 94GB (H800 NVL)[\#](#id216 "Link to this table") {#id216}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^75] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H800L-94C | 96246 | 1 | 1 | 3840x2400 | 1 |
| H800L-47C | 48128 | 2 | 2 | 3840x2400 | 1 |
| H800L-23C | 23552 | 4 | 4 | 3840x2400 | 1 |
| H800L-15C | 15360 | 6 | 4 | 3840x2400 | 1 |
| H800L-11C | 11264 | 8 | 8 | 3840x2400 | 1 |
| H800L-6C | 6144 | 15 | 8 | 3840x2400 | 1 |
| H800L-4C | 4096 | 23 | 16 | 3840x2400 | 1 |

Table 82 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H800 PCIe 94GB (H800 NVL)[\#](#id217 "Link to this table") {#id217}

NVIDIA H800 PCIe 80GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H800-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| H800-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| H800-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| H800-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| H800-1-20C [^76] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| H800-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| H800-1-10CME [^77] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 83 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H800 PCIe 80GB[\#](#id218 "Link to this table") {#id218}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^78] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H800-80C | 81920 | 1 | 1 | 3840x2400 | 1 |
| H800-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| H800-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| H800-16C | 16384 | 5 | 4 | 3840x2400 | 1 |
| H800-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| H800-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| H800-5C | 5120 | 16 | 16 | 3840x2400 | 1 |
| H800-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 84 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H800 PCIe 80GB[\#](#id219 "Link to this table") {#id219}

NVIDIA H800 SXM5 80GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H800XM-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| H800XM-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| H800XM-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| H800XM-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| H800XM-1-20C [^79] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| H800XM-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| H800XM-1-10CME [^80] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 85 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H800 SXM5 80GB[\#](#id220 "Link to this table") {#id220}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^81] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H800XM-80C | 81920 | 1 | 1 | 3840x2400 | 1 |
| H800XM-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| H800XM-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| H800XM-16C | 16384 | 5 | 4 | 3840x2400 | 1 |
| H800XM-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| H800XM-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| H800XM-5C | 5120 | 16 | 16 | 3840x2400 | 1 |
| H800XM-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 86 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H800 SXM5 80GB[\#](#id221 "Link to this table") {#id221}

NVIDIA H200 PCIe 141GB (H200 NVL)

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H200-7-141C | 144384 | 1 | 7 | 7 | MIG 7g.141gb |
| H200-4-71C | 72704 | 1 | 4 | 4 | MIG 4g.71gb |
| H200-3-71C | 72704 | 2 | 3 | 3 | MIG 3g.71gb |
| H200-2-35C | 35840 | 3 | 2 | 2 | MIG 2g.35gb |
| H200-1-35C [^82] | 35840 | 4 | 1 | 1 | MIG 1g.35gb |
| H200-1-18C | 18432 | 7 | 1 | 1 | MIG 1g.18gb |
| H200-1-18CME [^83] | 18432 | 1 | 1 | 1 | MIG 1g.18gb+me |

Table 87 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H200 PCIe 141GB (H200 NVL)[\#](#id222 "Link to this table") {#id222}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^84] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H200-141C | 144384 | 1 | 1 | 3840x2400 | 1 |
| H200-70C | 71680 | 2 | 2 | 3840x2400 | 1 |
| H200-35C | 35840 | 4 | 4 | 3840x2400 | 1 |
| H200-28C | 28672 | 5 | 5 | 3840x2400 | 1 |
| H200-17C | 17408 | 8 | 8 | 3840x2400 | 1 |
| H200-14C | 14336 | 10 | 10 | 3840x2400 | 1 |
| H200-8C | 8192 | 16 | 16 | 3840x2400 | 1 |
| H200-7C | 7168 | 20 | 20 | 3840x2400 | 1 |
| H200-4C | 4096 | 32 | 32 | 3840x2400 | 1 |

Table 88 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H200 PCIe 141GB (H200 NVL)[\#](#id223 "Link to this table") {#id223}

NVIDIA H200 SXM5 141GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H200X-7-141C | 144384 | 1 | 7 | 7 | MIG 7g.141gb |
| H200X-4-71C | 72704 | 1 | 4 | 4 | MIG 4g.71gb |
| H200X-3-71C | 72704 | 2 | 3 | 3 | MIG 3g.71gb |
| H200X-2-35C | 35840 | 3 | 2 | 2 | MIG 2g.35gb |
| H200X-1-35C [^85] | 35840 | 4 | 1 | 1 | MIG 1g.35gb |
| H200X-1-18C | 18432 | 7 | 1 | 1 | MIG 1g.18gb |
| H200X-1-18CME [^86] | 18432 | 1 | 1 | 1 | MIG 1g.18gb+me |

Table 89 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H200 SXM5 141GB[\#](#id224 "Link to this table") {#id224}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^87] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H200X-141C | 144384 | 1 | 1 | 3840x2400 | 1 |
| H200X-70C | 71680 | 2 | 2 | 3840x2400 | 1 |
| H200X-35C | 35840 | 4 | 4 | 3840x2400 | 1 |
| H200X-28C | 28672 | 5 | 5 | 3840x2400 | 1 |
| H200X-17C | 17408 | 8 | 8 | 3840x2400 | 1 |
| H200X-14C | 14336 | 10 | 10 | 3840x2400 | 1 |
| H200X-8C | 8192 | 16 | 16 | 3840x2400 | 1 |
| H200X-7C | 7168 | 20 | 20 | 3840x2400 | 1 |
| H200X-4C | 4096 | 32 | 32 | 3840x2400 | 1 |

Table 90 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H200 SXM5 141GB[\#](#id225 "Link to this table") {#id225}

NVIDIA H100 PCIe 94GB (H100 NVL)

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H100L-7-94C | 96246 | 1 | 7 | 7 | MIG 7g.94gb |
| H100L-4-47C | 48128 | 1 | 4 | 4 | MIG 4g.47gb |
| H100L-3-47C | 48128 | 2 | 3 | 3 | MIG 3g.47gb |
| H100L-2-24C | 24672 | 3 | 2 | 2 | MIG 2g.24gb |
| H100L-1-24C [^88] | 24672 | 4 | 1 | 1 | MIG 1g.24gb |
| H100L-1-12C | 12288 | 7 | 1 | 1 | MIG 1g.12gb |
| H100L-1-12CME [^89] | 12288 | 1 | 1 | 1 | MIG 1g.12gb+me |

Table 91 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H100 PCIe 94GB (H100 NVL)[\#](#id226 "Link to this table") {#id226}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^90] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H100L-94C | 96246 | 1 | 1 | 3840x2400 | 1 |
| H100L-47C | 48128 | 2 | 2 | 3840x2400 | 1 |
| H100L-23C | 23552 | 4 | 4 | 3840x2400 | 1 |
| H100L-15C | 15360 | 6 | 4 | 3840x2400 | 1 |
| H100L-11C | 11264 | 8 | 8 | 3840x2400 | 1 |
| H100L-6C | 6144 | 15 | 8 | 3840x2400 | 1 |
| H100L-4C | 4096 | 23 | 16 | 3840x2400 | 1 |

Table 92 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H100 PCIe 94GB (H100 NVL)[\#](#id227 "Link to this table") {#id227}

NVIDIA H100 SXM5 94GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H100XL-7-94C | 96246 | 1 | 7 | 7 | MIG 7g.94gb |
| H100XL-4-47C | 48128 | 1 | 4 | 4 | MIG 4g.47gb |
| H100XL-3-47C | 48128 | 2 | 3 | 3 | MIG 3g.47gb |
| H100XL-2-24C | 24672 | 3 | 2 | 2 | MIG 2g.24gb |
| H100XL-1-24C [^91] | 24672 | 4 | 1 | 1 | MIG 1g.24gb |
| H100XL-1-12C | 12288 | 7 | 1 | 1 | MIG 1g.12gb |
| H100XL-1-12CME [^92] | 12288 | 1 | 1 | 1 | MIG 1g.12gb+me |

Table 93 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H100 SXM5 94GB[\#](#id228 "Link to this table") {#id228}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^93] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H100XL-94C | 96246 | 1 | 1 | 3840x2400 | 1 |
| H100XL-47C | 48128 | 2 | 2 | 3840x2400 | 1 |
| H100XL-23C | 23552 | 4 | 4 | 3840x2400 | 1 |
| H100XL-15C | 15360 | 6 | 4 | 3840x2400 | 1 |
| H100XL-11C | 11264 | 8 | 8 | 3840x2400 | 1 |
| H100XL-6C | 6144 | 15 | 8 | 3840x2400 | 1 |
| H100XL-4C | 4096 | 23 | 16 | 3840x2400 | 1 |

Table 94 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H100 SXM5 94GB[\#](#id229 "Link to this table") {#id229}

NVIDIA H100 PCIe 80GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H100-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| H100-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| H100-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| H100-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| H100-1-20C [^94] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| H100-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| H100-1-10CME [^95] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 95 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H100 PCIe 80GB[\#](#id230 "Link to this table") {#id230}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^96] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H100-80 | 81920 | 1 | 1 | 3840x2400 | 1 |
| H100-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| H100-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| H100-16C | 16384 | 6 | 4 | 3840x2400 | 1 |
| H100-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| H100-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| H100-5C | 5120 | 16 | 16 | 3840x2400 | 1 |
| H100-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 96 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H100 PCIe 80GB[\#](#id231 "Link to this table") {#id231}

NVIDIA H100 SXM5 80GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H100XM-7-80C | 81920 | 1 | 7 | 7 | MIG 7g.80gb |
| H100XM-4-40C | 40960 | 1 | 4 | 4 | MIG 4g.40gb |
| H100XM-3-40C | 40960 | 2 | 3 | 3 | MIG 3g.40gb |
| H100XM-2-20C | 20480 | 3 | 2 | 2 | MIG 2g.20gb |
| H100XM-1-20C [^97] | 20480 | 4 | 1 | 1 | MIG 1g.20gb |
| H100XM-1-10C | 10240 | 7 | 1 | 1 | MIG 1g.10gb |
| H100XM-1-10CME [^98] | 10240 | 1 | 1 | 1 | MIG 1g.10gb+me |

Table 97 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H100 SXM5 80GB[\#](#id232 "Link to this table") {#id232}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^99] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H100XM-80C | 81920 | 1 | 1 | 3840x2400 | 1 |
| H100XM-40C | 40960 | 2 | 2 | 3840x2400 | 1 |
| H100XM-20C | 20480 | 4 | 4 | 3840x2400 | 1 |
| H100XM-16C | 16384 | 6 | 4 | 3840x2400 | 1 |
| H100XM-10C | 10240 | 8 | 8 | 3840x2400 | 1 |
| H100XM-8C | 8192 | 10 | 8 | 3840x2400 | 1 |
| H100XM-5C | 5120 | 16 | 16 | 3840x2400 | 1 |
| H100XM-4C | 4096 | 20 | 16 | 3840x2400 | 1 |

Table 98 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H100 SXM5 80GB[\#](#id233 "Link to this table") {#id233}

NVIDIA H100 SXM5 64GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H100XS-7-64C | 65536 | 1 | 7 | 7 | MIG 7g.64gb |
| H100XS-4-32C | 32768 | 1 | 4 | 4 | MIG 4g.32gb |
| H100XS-3-32C | 32768 | 2 | 3 | 3 | MIG 3g.32gb |
| H100XS-2-16C | 16384 | 3 | 2 | 2 | MIG 2g.16gb |
| H100XS-1-16C [^100] | 16384 | 4 | 1 | 1 | MIG 1g.16gb |
| H100XS-1-8C | 8192 | 7 | 1 | 1 | MIG 1g.8gb |
| H100XS-1-8CME [^101] | 8192 | 1 | 1 | 1 | MIG 1g.8gb+me |

Table 99 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H100 SXM5 64GB[\#](#id234 "Link to this table") {#id234}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^102] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H100XS-64C | 65536 | 1 | 1 | 3840x2400 | 1 |
| H100XS-32C | 32768 | 2 | 2 | 3840x2400 | 1 |
| H100XS-16C | 16384 | 4 | 4 | 3840x2400 | 1 |
| H100XS-8C | 8192 | 8 | 8 | 3840x2400 | 1 |
| H100XS-4C | 4096 | 16 | 16 | 3840x2400 | 1 |

Table 100 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H100 SXM5 64GB[\#](#id235 "Link to this table") {#id235}

NVIDIA H20 SXM5 141GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H20X-7-141C | 144384 | 1 | 7 | 7 | MIG 7g.141gb |
| H20X-4-71C | 72704 | 1 | 4 | 4 | MIG 4g.71gb |
| H20X-3-71C | 72704 | 2 | 3 | 3 | MIG 3g.71gb |
| H20X-2-35C | 35840 | 3 | 2 | 2 | MIG 2g.35gb |
| H20X-1-35C [^103] | 35840 | 4 | 1 | 1 | MIG 1g.35gb |
| H20X-1-18C | 18432 | 7 | 1 | 1 | MIG 1g.18gb |
| H20X-1-18CME [^104] | 18432 | 1 | 1 | 1 | MIG 1g.18gb+me |

Table 101 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H20 SXM5 141GB[\#](#id236 "Link to this table") {#id236}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^105] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H20X-141C | 144384 | 1 | 1 | 3840x2400 | 1 |
| H20X-70C | 71680 | 2 | 2 | 3840x2400 | 1 |
| H20X-35C | 35840 | 4 | 4 | 3840x2400 | 1 |
| H20X-28C | 28672 | 5 | 5 | 3840x2400 | 1 |
| H20X-17C | 17408 | 8 | 8 | 3840x2400 | 1 |
| H20X-14C | 14336 | 10 | 10 | 3840x2400 | 1 |
| H20X-8C | 8192 | 16 | 16 | 3840x2400 | 1 |
| H20X-7C | 7168 | 20 | 20 | 3840x2400 | 1 |
| H20X-4C | 4096 | 32 | 32 | 3840x2400 | 1 |

Table 102 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H20 SXM5 141GB[\#](#id237 "Link to this table") {#id237}

NVIDIA H20 SXM5 96GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Slices per vGPU | Compute Instances per vGPU | Corresponding GPU Instance Profile |
|----|----|----|----|----|----|
| H20-7-96C | 98304 | 1 | 7 | 7 | MIG 7g.96gb |
| H20-4-48C | 49152 | 1 | 4 | 4 | MIG 4g.48gb |
| H20-3-48C | 49152 | 2 | 3 | 3 | MIG 3g.48gb |
| H20-2-24C | 24576 | 3 | 2 | 2 | MIG 2g.24gb |
| H20-1-24C [^106] | 24576 | 4 | 1 | 1 | MIG 1g.24gb |
| H20-1-12C | 12288 | 7 | 1 | 1 | MIG 1g.12gb |
| H20-1-12CME [^107] | 12288 | 1 | 1 | 1 | MIG 1g.12gb+me |

Table 103 MIG-Backed NVIDIA vGPU (C-Series) for NVIDIA H20 SXM5 96GB[\#](#id238 "Link to this table") {#id238}

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU in Equal-Size Mode | Maximum vGPUs per GPU in Mixed-Size Mode | Maximum Display Resolution [^108] | Virtual Displays per vGPU |
|----|----|----|----|----|----|
| H20-96C | 98304 | 1 | 1 | 3840x2400 | 1 |
| H20-48C | 49152 | 2 | 2 | 3840x2400 | 1 |
| H20-24C | 24576 | 4 | 2 | 3840x2400 | 1 |
| H20-16C | 16384 | 6 | 4 | 3840x2400 | 1 |
| H20-12C | 12288 | 8 | 4 | 3840x2400 | 1 |
| H20-6C | 6144 | 16 | 8 | 3840x2400 | 1 |
| H20-4C | 4096 | 24 | 8 | 3840x2400 | 1 |

Table 104 Time-Sliced NVIDIA vGPU (C-Series) for NVIDIA H20 SXM5 96GB[\#](#id239 "Link to this table") {#id239}

<a id="nvidia-turing-gpu-architecture"></a>

### NVIDIA Turing GPU Architecture
Physical GPUs per board: 1

The maximum number of vGPUs per board is the product of the maximum number of vGPUs per GPU and the number of physical GPUs per board.

This GPU does **not** support mixed-size mode.

Intended use cases:

- vGPUs with more than 4096 MB of frame buffer: Training Workloads

- vGPUs with 4096 MB of frame buffer: Inference Workloads

Required license edition: NVIDIA vGPU (C-Series)

These vGPU types support a single display with a fixed maximum resolution.

NVIDIA Tesla T4

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Maximum Display Resolution [^109] | Virtual Displays per vGPU |
|----|----|----|----|----|
| T4-16C | 16384 | 1 | 3840x2400 | 1 |
| T4-8C | 8192 | 2 | 3840x2400 | 1 |
| T4-4C | 4096 | 4 | 3840x2400 | 1 |

Table 105 NVIDIA vGPU (C-Series) for NVIDIA Tesla T4[\#](#id240 "Link to this table") {#id240}

NVIDIA Quadro RTX 6000 Passive

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Maximum Display Resolution [^110] | Virtual Displays per vGPU |
|----|----|----|----|----|
| RTX6000P-24C | 24576 | 1 | 3840x2400 | 1 |
| RTX6000P-12C | 12288 | 2 | 3840x2400 | 1 |
| RTX6000P-8C | 8192 | 3 | 3840x2400 | 1 |
| RTX6000P-6C | 6144 | 4 | 3840x2400 | 1 |
| RTX6000P-4C | 4096 | 6 | 3840x2400 | 1 |

Table 106 NVIDIA vGPU (C-Series) for NVIDIA Quadro RTX 6000 Passive[\#](#id241 "Link to this table") {#id241}

NVIDIA Quadro RTX 8000 Passive

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Maximum Display Resolution [^111] | Virtual Displays per vGPU |
|----|----|----|----|----|
| RTX8000P-48C | 49152 | 1 | 3840x2400 | 1 |
| RTX8000P-24C | 24576 | 2 | 3840x2400 | 1 |
| RTX8000P-16C | 16384 | 3 | 3840x2400 | 1 |
| RTX8000P-12C | 12288 | 4 | 3840x2400 | 1 |
| RTX8000P-8C | 8192 | 6 | 3840x2400 | 1 |
| RTX8000P-6C | 6144 | 8 | 3840x2400 | 1 |
| RTX8000P-4C | 4096 | 8 [^112] | 3840x2400 | 1 |

Table 107 NVIDIA vGPU (C-Series) for NVIDIA Quadro RTX 8000 Passive[\#](#id242 "Link to this table") {#id242}

<a id="nvidia-volta-gpu-architecture"></a>

### NVIDIA Volta GPU Architecture
Physical GPUs per board: 1

The maximum number of vGPUs per board is the product of the maximum number of vGPUs per GPU and the number of physical GPUs per board.

This GPU does **not** support mixed-size mode.

Intended use cases:

- vGPUs with more than 4096 MB of frame buffer: Training Workloads

- vGPUs with 4096 MB of frame buffer: Inference Workloads

Required license edition: NVIDIA vGPU (C-Series)

These vGPU types support a single display with a fixed maximum resolution.

NVIDIA Tesla V100 SXM2

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Maximum Display Resolution [^113] | Virtual Displays per vGPU |
|----|----|----|----|----|
| V100X-16C | 16384 | 1 | 3840x2400 | 1 |
| V100X-8C | 8192 | 2 | 3840x2400 | 1 |
| V100X-4C | 4096 | 4 | 3840x2400 | 1 |

Table 108 NVIDIA vGPU (C-Series) for NVIDIA Tesla V100 SXM2[\#](#id243 "Link to this table") {#id243}

NVIDIA Tesla V100 SXM2 32GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Maximum Display Resolution [^114] | Virtual Displays per vGPU |
|----|----|----|----|----|
| V100DX-32C | 32768 | 1 | 3840x2400 | 1 |
| V100DX-16C | 16384 | 2 | 3840x2400 | 1 |
| V100DX-8C | 8192 | 4 | 3840x2400 | 1 |
| V100DX-4C | 6144 | 8 | 3840x2400 | 1 |

Table 109 NVIDIA vGPU (C-Series) for NVIDIA Tesla V100 SXM2 32GB[\#](#id244 "Link to this table") {#id244}

NVIDIA Tesla V100 PCIe 32GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Maximum Display Resolution [^115] | Virtual Displays per vGPU |
|----|----|----|----|----|
| V100D-32C | 32768 | 1 | 3840x2400 | 1 |
| V100D-16C | 16384 | 2 | 3840x2400 | 1 |
| V100D-8C | 8192 | 4 | 3840x2400 | 1 |
| V100D-4C | 4096 | 8 | 3840x2400 | 1 |

Table 110 NVIDIA vGPU (C-Series) for NVIDIA Tesla V100 PCIe 32GB[\#](#id245 "Link to this table") {#id245}

NVIDIA Tesla V100S PCIe 32GB

| Virtual GPU Type | Frame Buffer (MB) | Maximum vGPUs per GPU | Maximum Display Resolution [^116] | Virtual Displays per vGPU |
|----|----|----|----|----|
| V100S-32C | 32768 | 1 | 3840x2400 | 1 |
| V100S-16C | 16384 | 2 | 3840x2400 | 1 |
| V100S-8C | 8192 | 4 | 3840x2400 | 1 |
| V100S-4C | 4096 | 8 | 3840x2400 | 1 |

Table 111 NVIDIA vGPU (C-Series) for NVIDIA Tesla V100S PCIe 32GB[\#](#id246 "Link to this table") {#id246}

NVIDIA Tesla V100 FHHL

| Virtual GPU Type | Intended Use Case | Frame Buffer (MB) | Maximum vGPUs per GPU | Maximum vGPUs per Board | Maximum Display Resolution [^117] | Virtual Displays per vGPU |
|----|----|----|----|----|----|----|
| V100L-16C | Training Workloads | 16384 | 1 | 1 | 3840x2400 | 1 |
| V100L-8C | Training Workloads | 8192 | 2 | 2 | 3840x2400 | 1 |
| V100L-4C | Inference Workloads | 4096 | 4 | 4 | 3840x2400 | 1 |

Table 112 NVIDIA vGPU (C-Series) for NVIDIA Tesla V100 FHHL[\#](#id247 "Link to this table") {#id247}

Footnotes

\[1\] ([1](#id10),[2](#id22))

This type of vGPU cannot be assigned to the same VM as other types of vGPU.

\[2\] ([1](#id37),[2](#id38),[3](#id39))

Supported only on the following hardware:

- NVIDIA HGX A100 4-GPU baseboard with four fully connected GPUs

- NVIDIA HGX A100 8-GPU baseboards with eight fully connected GPUs

Fully connected means that each GPU is connected to every other GPU on the baseboard.

\[3\] ([1](#id65),[2](#id66),[3](#id68),[4](#id69),[5](#id71),[6](#id72),[7](#id74),[8](#id75),[9](#id77),[10](#id78),[11](#id80),[12](#id81),[13](#id83),[14](#id84),[15](#id86),[16](#id87),[17](#id89),[18](#id90),[19](#id92),[20](#id93),[21](#id95),[22](#id96),[23](#id98),[24](#id99),[25](#id101),[26](#id102),[27](#id104),[28](#id105),[29](#id108),[30](#id110),[31](#id111),[32](#id113),[33](#id114),[34](#id116),[35](#id117),[36](#id119),[37](#id120),[38](#id122),[39](#id123),[40](#id125),[41](#id126),[42](#id128),[43](#id129),[44](#id131),[45](#id132),[46](#id134),[47](#id135),[48](#id137),[49](#id138),[50](#id140),[51](#id141))

These vGPU types are supported on ESXi, starting with vSphere 8.0 update 3.

\[4\] ([1](#id42),[2](#id44),[3](#id46),[4](#id48),[5](#id50),[6](#id51),[7](#id52),[8](#id54),[9](#id56),[10](#id57),[11](#id59),[12](#id60),[13](#id61),[14](#id63),[15](#id64),[16](#id67),[17](#id70),[18](#id73),[19](#id76),[20](#id79),[21](#id82),[22](#id85),[23](#id88),[24](#id91),[25](#id94),[26](#id97),[27](#id100),[28](#id103),[29](#id106),[30](#id109),[31](#id112),[32](#id115),[33](#id118),[34](#id121),[35](#id124),[36](#id127),[37](#id130),[38](#id133),[39](#id136),[40](#id139),[41](#id142),[42](#id143),[43](#id144),[44](#id145),[45](#id147),[46](#id148),[47](#id149),[48](#id150),[49](#id151))

NVIDIA vGPU(C-Series) is optimized for compute-intensive workloads. As a result, they support only a single display head and do not provide Quadro graphics acceleration.

\[5\] ([1](#id43),[2](#id45),[3](#id47),[4](#id49),[5](#id53),[6](#id55),[7](#id58),[8](#id62),[9](#id146))

The maximum number of NVIDIA Virtual Compute Server vGPUs is limited to 12 vGPUs per physical GPU, irrespective of the available hardware resources of the physical GPU.

\[6\] ([1](#id23),[2](#id24),[3](#id25),[4](#id26),[5](#id27),[6](#id28),[7](#id29))

The SXM GPU Boards listed are supported only on VMware vSphere 7.x and 8.x.

\[7\] ([1](#id2),[2](#id3),[3](#id4),[4](#id5),[5](#id6),[6](#id7),[7](#id8),[8](#id9),[9](#id11),[10](#id12),[11](#id13),[12](#id14),[13](#id15),[14](#id16),[15](#id17),[16](#id18),[17](#id19),[18](#id20),[19](#id21),[20](#id30),[21](#id31),[22](#id32),[23](#id33),[24](#id34),[25](#id35),[26](#id36))

Refers to Linux with KVM hypervisors listed in the [NVIDIA AI Enterprise Infrastructure Support Matrix](../support/support-matrix.html#support-matrix).

[](../getting-started/deployment-guide.html "previous page")

previous

Deployment Guide

On this page

- [Key Concepts](#key-concepts)
  - [vGPU (C-Series)](#vgpu-c-series)
  - [NVIDIA vGPU (C-Series) Virtual GPU Manager](#nvidia-vgpu-c-series-virtual-gpu-manager)
  - [NVIDIA vGPU (C-Series) Driver](#nvidia-vgpu-c-series-driver)
- [Features](#features)
- [FAQs](#faqs)
- [Release Notes](#release-notes)
  - [Prerequisites](#prerequisites)
    - [Using NVIDIA vGPU (C-Series)](#using-nvidia-vgpu-c-series)
    - [Using NVIDIA vGPU (C-Series) on GPUs Requiring 64GB or More of MMIO Space with Large-Memory VMs](#using-nvidia-vgpu-c-series-on-gpus-requiring-64gb-or-more-of-mmio-space-with-large-memory-vms)
  - [Platform Support](#platform-support)
    - [Microsoft Windows Guest Operating Systems](#microsoft-windows-guest-operating-systems)
    - [NVIDIA vGPU (C-Series) Migration](#nvidia-vgpu-c-series-migration)
      - [vGPUs that Support Multiple vGPUs Assigned to a VM](#vgpus-that-support-multiple-vgpus-assigned-to-a-vm)
      - [vGPUs that Support Peer-to-Peer CUDA Transfers](#vgpus-that-support-peer-to-peer-cuda-transfers)
    - [GPUDirect Technology](#gpudirect-technology)
    - [NVIDIA NVSwitch On-Chip Memory Fabric](#nvidia-nvswitch-on-chip-memory-fabric)
    - [NVLink Multicast](#nvlink-multicast)
    - [vGPUs that Support Unified Memory](#vgpus-that-support-unified-memory)
  - [Limitations](#limitations)
    - [Total Frame Buffer for vGPUs is Less Than the Total Frame Buffer on the Physical GPU](#total-frame-buffer-for-vgpus-is-less-than-the-total-frame-buffer-on-the-physical-gpu)
    - [Single vGPU Benchmark Scores are Lower Than Passthrough GPU](#single-vgpu-benchmark-scores-are-lower-than-passthrough-gpu)
- [User Guide](#user-guide)
  - [Installing the NVIDIA Virtual GPU Manager](#installing-the-nvidia-virtual-gpu-manager)
    - [NVIDIA Virtual GPU Manager for Red Hat Enterprise Linux KVM](#nvidia-virtual-gpu-manager-for-red-hat-enterprise-linux-kvm)
    - [NVIDIA Virtual GPU Manager for Ubuntu](#nvidia-virtual-gpu-manager-for-ubuntu)
    - [NVIDIA Virtual GPU Manager for VMware vSphere](#nvidia-virtual-gpu-manager-for-vmware-vsphere)
  - [Administering MIG-Backed NVIDIA vGPUs](#administering-mig-backed-nvidia-vgpus)
    - [Architecture](#architecture)
    - [Configurations on a Single GPU](#configurations-on-a-single-gpu)
    - [Configuring the NVIDIA Virtual GPU Manager](#configuring-the-nvidia-virtual-gpu-manager)
      - [Modifying a MIG-Backed vGPU’s Configuration](#modifying-a-mig-backed-vgpu-s-configuration)
      - [Configuring a GPU for MIG-Backed vGPUs](#configuring-a-gpu-for-mig-backed-vgpus)
        - [Enabling MIG Mode for a GPU](#enabling-mig-mode-for-a-gpu)
        - [Creating GPU Instances on a MIG-Enabled GPU](#creating-gpu-instances-on-a-mig-enabled-gpu)
        - [Optional: Creating Compute Instances in a GPU Instance](#optional-creating-compute-instances-in-a-gpu-instance)
        - [Disabling MIG Mode for one or more GPUs](#disabling-mig-mode-for-one-or-more-gpus)
    - [Monitoring MIG-backed vGPU Activity](#monitoring-mig-backed-vgpu-activity)
  - [Installing NVIDIA AI Enterprise Software Components](#installing-nvidia-ai-enterprise-software-components)
    - [Installing the NVIDIA AI Enterprise Software Components Using Kubernetes](#installing-the-nvidia-ai-enterprise-software-components-using-kubernetes)
      - [Transforming Container Images for AI and Data Science Applications and Frameworks into Kubernetes Pods](#transforming-container-images-for-ai-and-data-science-applications-and-frameworks-into-kubernetes-pods)
    - [Installing the NVIDIA AI Enterprise Application Software and Deep Learning Framework Components Using Docker](#installing-the-nvidia-ai-enterprise-application-software-and-deep-learning-framework-components-using-docker)
    - [Installing the NVIDIA GPU Operator Using a Bash Shell Script](#installing-the-nvidia-gpu-operator-using-a-bash-shell-script)
- [Virtual GPU Types for Supported GPUs](#virtual-gpu-types-for-supported-gpus)
  - [NVIDIA Ada Lovelace GPU Architecture](#nvidia-ada-lovelace-gpu-architecture)
  - [NVIDIA Ampere GPU Architecture](#nvidia-ampere-gpu-architecture)
    - [MIG-Backed and Time-Sliced NVIDIA vGPU (C-Series) for the NVIDIA Ampere GPU Architecture](#mig-backed-and-time-sliced-nvidia-vgpu-c-series-for-the-nvidia-ampere-gpu-architecture)
  - [NVIDIA Hopper GPU Architecture](#nvidia-hopper-gpu-architecture)
    - [MIG-Backed and Time-Sliced NVIDIA vGPU (C-Series) for the NVIDIA Hopper GPU Architecture](#mig-backed-and-time-sliced-nvidia-vgpu-c-series-for-the-nvidia-hopper-gpu-architecture)
  - [NVIDIA Turing GPU Architecture](#nvidia-turing-gpu-architecture)
  - [NVIDIA Volta GPU Architecture](#nvidia-volta-gpu-architecture)

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

[^36]:

[^37]:

[^38]:

[^39]:

[^40]:

[^41]:

[^42]:

[^43]:

[^44]:

[^45]:

[^46]:

[^47]:

[^48]:

[^49]:

[^50]:

[^51]:

[^52]:

[^53]:

[^54]:

[^55]:

[^56]:

[^57]:

[^58]:

[^59]:

[^60]:

[^61]:

[^62]:

[^63]:

[^64]:

[^65]:

[^66]:

[^67]:

[^68]:

[^69]:

[^70]:

[^71]:

[^72]:

[^73]:

[^74]:

[^75]:

[^76]:

[^77]:

[^78]:

[^79]:

[^80]:

[^81]:

[^82]:

[^83]:

[^84]:

[^85]:

[^86]:

[^87]:

[^88]:

[^89]:

[^90]:

[^91]:

[^92]:

[^93]:

[^94]:

[^95]:

[^96]:

[^97]:

[^98]:

[^99]:

[^100]:

[^101]:

[^102]:

[^103]:

[^104]:

[^105]:

[^106]:

[^107]:

[^108]:

[^109]:

[^110]:

[^111]:

[^112]:

[^113]:

[^114]:

[^115]:

[^116]:

[^117]:
