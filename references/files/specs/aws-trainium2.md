<!-- 从 aws-trainium2.html 迁移的资料快照；原始 HTML SHA-256: 9afd23f3a56d0c1d9a88fbb69693a452c0cfaf904393abf01aec96b0f081c337。 -->

- [ Repository](https://github.com/aws-neuron/aws-neuron-sdk "Source repository")
- [ Suggest edit](https://github.com/aws-neuron/aws-neuron-sdk/edit/master/about-neuron/arch/neuron-hardware/trainium2.rst "Suggest edit")
- [ Open issue](https://github.com/aws-neuron/aws-neuron-sdk/issues/new?title=Issue%20on%20page%20%2Fabout-neuron/arch/neuron-hardware/trainium2.html&body=Your%20issue%20content%20here. "Open an issue")

- [ .rst](../../../_sources/about-neuron/arch/neuron-hardware/trainium2.rst "Download source file")
-  .pdf

# Trainium2 Architecture

## Contents

- [Trainium2 chip components](#trainium2-chip-components)
- [Trainium2 performance improvements](#trainium2-performance-improvements)
  - [Compute](#compute)
  - [Memory](#memory)
  - [Interconnect](#interconnect)
  - [Data movement](#data-movement)
- [Additional resources](#additional-resources)

**This document is relevant for**: `Trn2`

<a id="trainium2-architecture"></a>

# Trainium2 Architecture
Trainium2 is the third generation, purpose-built Machine Learning chip from AWS. Every Trainium2 chip contains eight NeuronCore-V3 cores. Beginning with Trainium2, AWS Neuron adds support for Logical NeuronCore Configuration (LNC), which lets you combine the compute and memory resources of multiple physical NeuronCores into a single logical NeuronCore. The following diagram shows the architecture overview of a Trainium2 chip.

[![](../../../_images/trainium2.png)](../../../_images/trainium2.png)

<a id="trainium2-chip-components"></a>

## Trainium2 chip components
Each Trainium2 chip consists of the following components:

[TABLE]

<a id="trainium2-performance-improvements"></a>

## Trainium2 performance improvements
The following set of tables offer a comparison between Trainium and Trainium2 chips.

<a id="compute"></a>

### Compute
|  | Trainium | Trainium2 | Improvement factor |
|----|----|----|----|
| FP8 (TFLOPS) | 191 | 1299 | 6.7x |
| BF16/FP16/TF32 (TFLOPS) | 191 | 667 | 3.4x |
| FP32 (TFLOPS) | 48 | 181 | 3.7x |
| FP8/FP16/BF16/TF32 Sparse (TFLOPS) | Not applicable | 2563 | Not applicable |

<a id="memory"></a>

### Memory
|                        | Trainium       | Trainium2      | Improvement factor |
|------------------------|----------------|----------------|--------------------|
| HBM Capacity (GiB)     | 32             | 96             | 3x                 |
| HBM Bandwidth (TB/sec) | 0.8            | 2.9            | 3.6x               |
| SBUF Capacity (MiB)    | 48             | 224            | 4.7x               |
| Memory Pool Size       | Up to 16 chips | Up to 64 chips | 4x                 |

<a id="interconnect"></a>

### Interconnect
|                                       | Trainium | Trainium2 | Improvement factor |
|---------------------------------------|----------|-----------|--------------------|
| Inter-chip Interconnect (GB/sec/chip) | 384      | 1280      | 3.3x               |

<a id="data-movement"></a>

### Data movement
|  | Trainium | Trainium2 | Improvement factor |
|----|----|----|----|
| CC Cores | 6 | 16 | 3.3x |
| DMA barriers | Write-after-write | Strong-order-write | \>1x (Benefit DMA-size dependent) |
| SBUF memory layout | Row-major | Row-major, Col-major-2B, Col-major-4B | Not applicable |

<a id="additional-resources"></a>

## Additional resources
For a detailed description of NeuronCore-v3 hardware engines, instances powered by AWS Trainium2, and Logical NeuronCore configuration, see the following resources:

- [NeuronCore-v3 architecture](neuron-core-v3.html#neuroncores-v3-arch)

- [Amazon EC2 Trn2 architecture](trn2-arch.html#aws-trn2-arch)

- [Logical NeuronCore configuration](../neuron-features/logical-neuroncore-config.html#logical-neuroncore-config)

**This document is relevant for**: `Trn2`

[](trainium.html "previous page")

previous

Trainium Architecture

[](trainium3.html "next page")

next

Trainium3 Architecture

Contents

- [Trainium2 chip components](#trainium2-chip-components)
- [Trainium2 performance improvements](#trainium2-performance-improvements)
  - [Compute](#compute)
  - [Memory](#memory)
  - [Interconnect](#interconnect)
  - [Data movement](#data-movement)
- [Additional resources](#additional-resources)

By AWS

© Copyright 2026, Amazon.com.  
