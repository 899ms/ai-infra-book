<!-- 从 aws-neuroncore-v3.html 迁移的资料快照；原始 HTML SHA-256: ecb34ad595c5e36843a1ba66b88c015a61f8b515e6110f26c98632b4f211fdb4。 -->

- [ Repository](https://github.com/aws-neuron/aws-neuron-sdk "Source repository")
- [ Suggest edit](https://github.com/aws-neuron/aws-neuron-sdk/edit/master/about-neuron/arch/neuron-hardware/neuron-core-v3.rst "Suggest edit")
- [ Open issue](https://github.com/aws-neuron/aws-neuron-sdk/issues/new?title=Issue%20on%20page%20%2Fabout-neuron/arch/neuron-hardware/neuron-core-v3.html&body=Your%20issue%20content%20here. "Open an issue")

- [ .rst](../../../_sources/about-neuron/arch/neuron-hardware/neuron-core-v3.rst "Download source file")
-  .pdf

# NeuronCore-v3 Architecture

## Contents

- [On-chip SRAM](#on-chip-sram)
- [Tensor Engine](#tensor-engine)
- [Vector Engine](#vector-engine)
- [Scalar engine](#scalar-engine)
- [GPSIMD engine](#gpsimd-engine)

**This document is relevant for**: `Trn2`

<a id="neuroncore-v3-architecture"></a>

# NeuronCore-v3 Architecture
NeuronCore-v3 is the third-generation NeuronCore that powers Trainium2 chips. It is a fully-independent heterogenous compute unit consisting of 4 main engines: Tensor, Vector, Scalar, and GPSIMD, with on-chip software-managed SRAM memory to maximize data locality and optimize data prefetch. The following diagram shows a high-level overview of the NeuronCore-V3 architecture.

[![](../../../_images/nc-v3.png)](../../../_images/nc-v3.png)

  

NeuronCore-v3 is made up of the following components:

<a id="on-chip-sram"></a>

## On-chip SRAM
Each NeuronCore-v3 has a total of 28MB of on-chip SRAM. NeuronCore-v3 on-chip SRAM is software-managed to maximize data locality and optimize data prefetch.

<a id="tensor-engine"></a>

## Tensor Engine
Tensor engines are based on a power-optimized systolic array. They are highly optimized for tensor computations such as GEMM, CONV, and Transpose. Tensor Engines support mixed-precision computations, including cFP8, FP16, BF16, TF32, and FP32 inputs and outputs. A NeuronCore-v3 Tensor Engine delivers 158 cFP8 TFLOPS, and 79 BF16/FP16/TF32 TFLOPS of tensor computations.

Like NeuronCore-v2, NeuronCore-v3 supports control flow, dynamic shapes, and programmable rounding mode (RNE & Stochastic-rounding). NeuronCore-v3 also supports adjustable exponent biasing for the cFP8 data type.

The NeuronCore-v3 Tensor Engine also supports Structured Sparsity, delivering up to 316 TFLOPS of cFP8/FP16/BF16/TF32 compute. This is useful when one of the input tensors to matrix multiplication exhibits a M:N sparsity pattern, where only M elements out of every N contiguous elements are non-zero. NeuronCore-v3 supports several sparsity patterns, including 4:16, 4:12, 4:8, 2:8, 2:4, 1:4, and 1:2.

<a id="vector-engine"></a>

## Vector Engine
Optimized for vector computations, in which every element of the output is dependent on multiple input elements. Examples include axpi operations (Z=aX+Y), Layer Normalization, and Pooling operations.

Vector Engines are highly parallelized, and deliver a total of 1 TFLOPS of FP32 computations. NeuronCore-v3 Vector Engines can handle various data-types, including cFP8, FP16, BF16, TF32, FP32, INT8, INT16, and INT32.

<a id="scalar-engine"></a>

## Scalar engine
Optimized for scalar computations in which every element of the output is dependent on one element of the input. Scalar Engines are highly parallelized, and deliver a total of 1.2 TFLOPS of FP32 computations. NeuronCore-v3 Scalar Engines support multiple data types, including cFP8, FP16, BF16, TF32, FP32, INT8, INT16, and INT32.

<a id="gpsimd-engine"></a>

## GPSIMD engine
Each GPSIMD engine consists of eight fully-programmable 512-bit wide vector processors. They can execute general purpose C-code and access the embedded on-chip SRAM, allowing you to implement custom operators and execute them directly on the NeuronCores.

**This document is relevant for**: `Trn2`

[](neuron-core-v2.html "previous page")

previous

NeuronCore-v2 Architecture

[](neuron-core-v4.html "next page")

next

NeuronCore-v4 Architecture

Contents

- [On-chip SRAM](#on-chip-sram)
- [Tensor Engine](#tensor-engine)
- [Vector Engine](#vector-engine)
- [Scalar engine](#scalar-engine)
- [GPSIMD engine](#gpsimd-engine)

By AWS

© Copyright 2026, Amazon.com.  
