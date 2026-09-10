<!-- 从 aws-trainium3.html 迁移的资料快照；原始 HTML SHA-256: 347085a8a077cb7295e6c06683f8d866ab4919bfea590ac3f5c9878bc5f0d55b。 -->

- [ Repository](https://github.com/aws-neuron/aws-neuron-sdk "Source repository")
- [ Suggest edit](https://github.com/aws-neuron/aws-neuron-sdk/edit/master/about-neuron/arch/neuron-hardware/trainium3.rst "Suggest edit")
- [ Open issue](https://github.com/aws-neuron/aws-neuron-sdk/issues/new?title=Issue%20on%20page%20%2Fabout-neuron/arch/neuron-hardware/trainium3.html&body=Your%20issue%20content%20here. "Open an issue")

- [ .rst](../../../_sources/about-neuron/arch/neuron-hardware/trainium3.rst "Download source file")
-  .pdf

# Trainium3 Architecture

## Contents

- [NeuronCore-v4](#neuroncore-v4)
- [Trainium3 performance improvements](#trainium3-performance-improvements)
  - [Compute](#compute)
  - [Memory](#memory)
  - [Interconnect](#interconnect)
  - [Data movement](#data-movement)
- [Additional resources](#additional-resources)

**This document is relevant for**: `Trn3`

<a id="trainium3-architecture"></a>

# Trainium3 Architecture
Trainium3 is the fourth-generation purpose-built Machine Learning chip from AWS. A Trainium3 device contains eight NeuronCore-v4 cores. Similar to Trainium2, AWS Neuron adds support for Logical NeuronCore Configuration (LNC), which lets you combine the compute and memory resources of multiple physical NeuronCores into a single logical NeuronCore. The following diagram shows the architecture overview of a Trainium3 chip.

![](../../../_images/neuroncore-v4-overview.png)

<a id="neuroncore-v4"></a>

## NeuronCore-v4
Each Trainium3 chip consists of the following components:

[TABLE]

<a id="trainium3-performance-improvements"></a>

## Trainium3 performance improvements
The following set of tables offer a comparison between Trainium2 and Trainium3 chips.

<a id="compute"></a>

### Compute
[TABLE]

<a id="memory"></a>

### Memory
|                        | Trainium2 | Trainium3 | Improvement factor |
|------------------------|-----------|-----------|--------------------|
| HBM Capacity (GiB)     | 96        | 144       | 1.5x               |
| HBM Bandwidth (TB/sec) | 2.9       | 4.9       | 1.7x               |
| SBUF Capacity (MiB)    | 224       | 256       | 1.14x              |

<a id="interconnect"></a>

### Interconnect
|  | Trainium2 | Trainium3 | Improvement factor |
|----|----|----|----|
| Inter-chip Interconnect (GB/sec/chip) | 1280 | 2560 | 2x |

<a id="data-movement"></a>

### Data movement
|                        | Trainium2 | Trainium3 | Improvement factor |
|------------------------|-----------|-----------|--------------------|
| DMA Bandwidth (TB/sec) | 3.5       | 4.9       | 1.4x               |

<a id="additional-resources"></a>

## Additional resources
For a detailed description of NeuronCore-v4 hardware engines, instances powered by AWS Trainium3, and Logical NeuronCore configuration, see the following resources:

- [NeuronCore-v4 architecture](neuron-core-v4.html#neuroncores-v4-arch)

**This document is relevant for**: `Trn3`

[](trainium2.html "previous page")

previous

Trainium2 Architecture

[](neuron-core-v1.html "next page")

next

NeuronCore-v1 Architecture

Contents

- [NeuronCore-v4](#neuroncore-v4)
- [Trainium3 performance improvements](#trainium3-performance-improvements)
  - [Compute](#compute)
  - [Memory](#memory)
  - [Interconnect](#interconnect)
  - [Data movement](#data-movement)
- [Additional resources](#additional-resources)

By AWS

© Copyright 2026, Amazon.com.  
