<!-- 从 aws-trn2-system.html 迁移的资料快照；原始 HTML SHA-256: 35be1ecee93a3919db0f13dd348815aac45e91769b63fa8218e760034f23bea0。 -->

- [ Repository](https://github.com/aws-neuron/aws-neuron-sdk "Source repository")
- [ Suggest edit](https://github.com/aws-neuron/aws-neuron-sdk/edit/master/about-neuron/arch/neuron-hardware/trn2-arch.rst "Suggest edit")
- [ Open issue](https://github.com/aws-neuron/aws-neuron-sdk/issues/new?title=Issue%20on%20page%20%2Fabout-neuron/arch/neuron-hardware/trn2-arch.html&body=Your%20issue%20content%20here. "Open an issue")

- [ .rst](../../../_sources/about-neuron/arch/neuron-hardware/trn2-arch.rst "Download source file")
-  .pdf

# Amazon EC2 Trn2 Architecture

## Contents

- [Trn2 instance sizes](#trn2-instance-sizes)
  - [trn2.48xlarge / trn2u.48xlarge](#trn2-48xlarge-trn2u-48xlarge)
  - [Trn2 UltraServer](#trn2-ultraserver)
- [Trn2 instance specifications](#trn2-instance-specifications)

**This document is relevant for**: `Trn2`

<a id="amazon-ec2-trn2-architecture"></a>

# Amazon EC2 Trn2 Architecture
Trn2 is an Amazon EC2 accelerated computing instance, purpose built for high-performance deep learning training and inference. This page provides an architecture overview of the trn2.48xlarge and trn2u.48xlarge instances, and Trn2 UltraServer.

Topics

- [Trn2 instance sizes](#trn2-instance-sizes)

  - [trn2.48xlarge / trn2u.48xlarge](#trn2-48xlarge-trn2u-48xlarge)

  - [Trn2 UltraServer](#trn2-ultraserver)

- [Trn2 instance specifications](#trn2-instance-specifications)

<a id="trn2-instance-sizes"></a>

## [Trn2 instance sizes](#id2)
Trn2 instances and UltraServers are available in the following sizes and configurations:

- trn2.48xlarge

- trn2u.48xlarge

- Trn2 UltraServer

<a id="trn2-48xlarge-trn2u-48xlarge"></a>

### [trn2.48xlarge / trn2u.48xlarge](#id3)
Trn2 instances are powered by 16 Trainium2 chips connected using a high-bandwidth, low-latency NeuronLink-v3 chip-to-chip interconnect. The NeuronLink-v3 chip-to-chip interconnect enables collective communication between Trainium2 chips during distributed training and inference. It also allows for the pooling of memory resources from all 16 Trainium2 chips.

In a trn2.48xlarge or trn2u.48xlarge instance, 16 Trainium2 chips are connected using a 4x4, 2D Torus topology. The following diagram shows the intra-instance connections of a trn2.48xlarge or trn2u.48xlarge instance

[![](../../../_images/trn2.48xlarge.png)](../../../_images/trn2.48xlarge.png)

  

<a id="trn2-ultraserver"></a>

### [Trn2 UltraServer](#id4)
A Trn2 UltraServer comprises four trn2u.48xlarge instances connected together via the NeuronLink-v3 chip-to-chip interconnect. This allows for a total of 64 Trainium2 chips to be interconnected within a Trn2 UltraServer. Trainium2 chips with the same coordinates in each Trn2 instance are connected in a ring topology. The following figure shows the inter-instance ring connection between Trainium2 chips.

[![](../../../_images/u-trn2x64.png)](../../../_images/u-trn2x64.png)

  

<a id="trn2-instance-specifications"></a>

## [Trn2 instance specifications](#id5)
The following table shows the performance metrics for Trainium2 based instances.

| Perfomance specification | trn2.48xlarge / trn2u.48xlarge | Trn2 UltraServer |
|----|----|----|
| \# of Trainium2 chips | 16 | 64 |
| vCPUs | 192 | 768 |
| Host Memory (GiB) | 2,048 | 8,192 |
| FP8 PFLOPS | 20.8 | 83.2 |
| FP16/BF16/TF32 PFLOPS | 10.7 | 42.8 |
| FP8/FP16/BF16/TF32 Sparse PFLOPS | 41 | 164 |
| FP32 PFLOPS | 2.9 | 11.6 |
| Device Memory (GiB) | 1,536 | 6,144 |
| Device Memory Bandwidth (TB/sec) | 46.4 | 185.6 |
| Intra-instance NeuronLink-v3 bandwidth (GB/sec/chip) | 1,024 | 1,024 |
| Inter-instance NeuronLink-v3 bandwidth (GB/sec/chip) | Not applicable | 256 |
| EFAv3 bandwidth (Gbps) | 3,200 | 3,200 |

**This document is relevant for**: `Trn2`

[](trn1-arch.html "previous page")

previous

Amazon EC2 Trn1/Trn1n Architecture

[](trn3-arch.html "next page")

next

Amazon EC2 Trn3 Architecture

Contents

- [Trn2 instance sizes](#trn2-instance-sizes)
  - [trn2.48xlarge / trn2u.48xlarge](#trn2-48xlarge-trn2u-48xlarge)
  - [Trn2 UltraServer](#trn2-ultraserver)
- [Trn2 instance specifications](#trn2-instance-specifications)

By AWS

© Copyright 2026, Amazon.com.  
