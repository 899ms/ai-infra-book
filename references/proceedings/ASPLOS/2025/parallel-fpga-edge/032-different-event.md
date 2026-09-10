<!-- 从 032-different-event.html 迁移的资料快照；原始 HTML SHA-256: 676eb823a3febe2a49da65910dc9459ddfb756a1c2e4cb948b976a2c91148f3e。 -->

# Posters

**Notes for poster presenters**

Preparation before the conference:

- Posters shall be printed in **A0 format in portrait mode**.
- Each presenter shall bring their own poster on site.
- There is no template for posters.
- Make sure that the poster is easy to read from distance and attracts people, use QR codes to link to more content.
- At least one author of the poster must register for the core conference (Tuesday 13 to Thursday 15).

Local print shop:

- For authors that would like to print their poster in Paris, there is a print shop named “[Au Print](https://auprint.fr)” located [14 rue Rouvet, 75019 Paris](https://maps.app.goo.gl/FZZuos9y2NQEyHv77). It is close to the metro station “[Corentin Cariou](https://www.bonjour-ratp.fr/en/stations-metro/corentin-cariou/)”, one stop away from the venue. The web site is in French, but they accept orders in English at <contact@auprint.fr> – price is about 40 € for an A0 print on 120 g/m² paper.

At the conference:

- You will mount your own poster, no own tape allowed, you will get some.
- Each poster will be displayed for a full day.
- Presenters are expected to stand next to their posters during breaks and lunches.
- The exhibition and poster area will be open only during breaks and lunches.

# More than 180 posters over 3 days!

More than 60 posters per day are dispatched over a dozen of posters islands spread over the 3 levels of the expo area

To the lists of posters on display, per day and per island:

- Tuesday 13. At S1: islands [P1.1](#P1.1-Tue), [P1.2](#P1.2-Tue), [P1.3](#P1.3-Tue), [P1.4](#P1.4-Tue). At S2: islands [P2.1](#P2.1-Tue), [P2.2](#P2.2-Tue), [P2.3](#P2.3-Tue). At S3: islands [P3.1](#P3.1-Tue), [P3.2](#P3.2-Tue).

- Wednesday 14. At S1: islands [P1.1](#P1.1-Wed), [P1.2](#P1.2-Wed), [P1.3](#P1.3-Wed), [P1.4](#P1.4-Wed). At S2: islands [P2.1](#P2.1-Wed), [P2.2](#P2.2-Wed), [P2.3](#P2.3-Wed). At S3: islands [P3.1](#P3.1-Wed), [P3.2](#P3.2-Wed).

- Thursday 15. At S1: islands [P1.1](#P1.1-Thu), [P1.2](#P1.2-Thu), [P1.3](#P1.3-Thu), [P1.4](#P1.4-Thu). At S2: islands [P2.1](#P2.1-Thu), [P2.2](#P2.2-Thu), [P2.3](#P2.3-Thu). At S3: islands [P3.1](#P3.1-Thu).

# Tuesday 13 Posters

Sorted by expo level, poster island, and stand.

------------------------------------------------------------------------

On Tuesday 13, at island P1.1 (S1)

------------------------------------------------------------------------

### Benchmarking TinyML CNN Kernels on RVV 1.0 Hardware: GCC 14 vs. LLVM 19

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.01-VAN-KEMPEN-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.01-VAN-KEMPEN-abstract.pdf). Sub. \#101. Tuesday 13, at island 1.1 on S1. ([P1.1.01-Tue](#P1.1.01-Tue)).

**Philipp van Kempen**, Technical University of Munich. **Benedikt Witteler**, Technical University of Munich. **Jefferson Parker Jones**, TU Wien. **Daniel Mueller-Gritschneder**, TU Wien. **Ulf Schlichtmann**, Technical University of Munich.

**Abstract**: This paper evaluates CNN workloads on the RISC-V Vector Extension (RVV) 1.0 using GCC 14 and LLVM 19. We benchmark auto-vectorized and manually optimized TinyML kernels on a hardware platform, analyzing runtime and code size trade-offs. Results show that LLVM 19 provides a better balance between both metrics, while GCC 14 exhibits greater variability.

[To page top](#summary) — [To posters at P1.1 (S1) on Tuesday 13](#P1.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### ProbRVCIM : Integrating Compute-in-Memory to RISC-V ISA for Probabilistic Learning and Inference at the Edge

Sub. \#161. Tuesday 13, at island 1.1 on S1. ([P1.1.02-Tue](#P1.1.02-Tue)).

**Priyesh Shukla**, Samsung Research / IIIT Hyderabad. **Amit Ranjan Trivedi**, University of Illinois at Chicago.

**Abstract**: We present the integration of probabilistic compute-in-memory (CIM) module on the RISC-V ISA. The proposed system is aimed towards robust (uncertainty-aware) yet low-power Bayesian edge intelligence. Using Bayesian inference, not only the prediction itself, but the prediction confidence can also be extracted for planning risk-aware actions. However, Bayesian inference of a deep neural network (DNN) is computationally expensive, ill-suited for real-time and/or edge deployment. An approximation to Bayesian DNN using Monte Carlo Dropout (MC-Dropout) has shown high robustness along with low computational complexity. The novel CIM module can perform in-memory probabilistic dropout in addition to in-memory weight-input scalar product. Application of the proposed CIM-based MC-Dropout execution using RISC-V ISA is discussed for visual odometry (VO) of autonomous drones.

[To page top](#summary) — [To posters at P1.1 (S1) on Tuesday 13](#P1.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### RISC-V ISA Extensions with Hardware Acceleration for Hyperdimensional Computing

[Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.03-MARTINO-abstract.pdf). Sub. \#109. Tuesday 13, at island 1.1 on S1. ([P1.1.03-Tue](#P1.1.03-Tue)).

**Rocco Martino**, Sapienza University of Rome. **Marco Angioli**, Sapienza University of Rome. **Antonello Rosato**, Sapienza University of Rome. **Marcello Barbirotta**, Sapienza University of Rome. **Abdallah Cheikh**, Sapienza University of Rome. **Mauro Olivieri**, Sapienza University of Rome.

**Abstract**: Hyperdimensional Computing (HDC) leverages high-dimensional distributed representations called hypervectors (HVs) and simple arithmetic operations, making it an ideal paradigm for learning tasks on resource-constrained devices. This work introduces the first RISC-V Instruction Set Architecture (ISA) extension specifically designed to execute all fundamental arithmetic operations of HDC directly through dedicated instructions, which, when appropriately combined, enable a variety of learning tasks by efficiently encoding and processing information. This extension is coupled with a specialized hardware acceleration unit, integrated into the Klessydra-T03 RISC-V core, to perform computations on binary HVs efficiently. The proposed solution enables a seamless trade-off between execution time and hardware resource utilization through both synthesis-time configurability and runtime programmability. The custom ISA extension is fully integrated into the RISC-V GCC toolchain, allowing software developers to exploit its capabilities via intrinsic function calls. Benchmarking on an FPGA platform demonstrates significant performance improvements across a wide range of HDC tasks, from basic arithmetic operations to real-world classification problems.

[To page top](#summary) — [To posters at P1.1 (S1) on Tuesday 13](#P1.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Energy & Latency Efficient Dual-Mode AI Accelerator - AGNI Neural Inference Engine

Sub. \#125. Tuesday 13, at island 1.1 on S1. ([P1.1.04-Tue](#P1.1.04-Tue)).

**Naman Kalra**, IIT Tirupati. **Jaynarayan T. Tudu**, IIT Tirupati.

**Abstract**: AI Acceleration at the edge demands a balance between energy efficiency and low-latency inference. This paper introduces Project AGNI, a Dual-Mode AI Accelerator designed to dynamically adapt to workload variations through its integration with Tejas, A Transformative Energy Efficient Joint Scalable CPU Architecture. Unlike existing monolithic AI Accelerators that struggle with heterogeneous workloads, AGNI leverages layer-aware execution to achieve optimal latency and power efficiency across diverse AI tasks. The architecture is particularly suited for edge AI applications including drone-based machine learning, IoT devices, autonomous robotics, and mobile AI workloads, where traditional GPUs are impractical due to power and area constraints. The proposed dual-mode execution model enables High-Performance Mode for computationally intensive workloads such as CNNs and real-time AI inference, while the Low-Workload Mode optimizes efficiency for lighter tasks, including Pooling, Fully Connected (FC) layers and small-scale AI computations. Our preliminary results showed a 10–15% improvement in performance across all layers of ResNet-50 compared to existing AI accelerators. By dynamically switching modes, AGNI ensures superior inference speed and energy efficiency, addressing the growing demand for adaptive and scalable AI solutions in edge computing.

[To page top](#summary) — [To posters at P1.1 (S1) on Tuesday 13](#P1.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### A Unified AI Accelerator Interface for Scalable RISC-V Architectures

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.05-QIU-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.05-QIU-abstract.pdf). Sub. \#220. Tuesday 13, at island 1.1 on S1. ([P1.1.05-Tue](#P1.1.05-Tue)).

**Fucong Qiu**, Institute of Computing Technology, Chinese Academy of Sciences. **Mingjin Gao**, ICT. **Dan Tang**, Institute of Computing Technology, Chinese Academy of Sciences. **Yungang Bao**, ICT, CAS. **Tao Xie**, Beijing Institute of Open Source Chip, BOSC.

**Abstract**: Various general-purpose accelerator interfaces proposed by the industry struggle to meet AI workloads’ demands. Thus specialized interface solutions have emerged to address AI-specific challenges but suffer from limited adaptability and expandability. To address the issue, in this paper, we propose a flexible, open AI accelerator interface for the RISC-V architecture, natively supporting AI-oriented extensions—including vector, matrix, and tensor operations. The interface integrates diverse data access mechanisms—L1 cache access, bus access, coprocessor extension access, and inter-coprocessor data movement, to accommodate various AI dataflow scenarios. In addition, the interface provides a robust virtual memory mechanism that enables accelerators to obtain physical addresses from the processor via private TLBs or direct MMU access for efficient address translation. By supporting multiple decoupled microarchitectural designs through flexible accelerator decoding schemes and various accelerator CSR management approaches, the interface enhances system scalability, versatility, and performance. Together, these features form a scalable and robust solution for future AI accelerator applications based on RISC-V architectures.

[To page top](#summary) — [To posters at P1.1 (S1) on Tuesday 13](#P1.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Optimizing Hardware for Neural Network Inference using Virtual Prototypes

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.07-ZIELASKO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.07-ZIELASKO-abstract.pdf). Sub. \#159. Tuesday 13, at island 1.1 on S1. ([P1.1.07-Tue](#P1.1.07-Tue)).

**Jan Zielasko**, Cyber-Physical Systems, DFKI GmbH. **Rolf Drechsler**, University of Bremen/DFKI.

**Abstract**: Identifying the optimal hardware configuration for running inference of Neural Networks on ultra-low-power edge devices is crucial to reduce costs and improve performance of smart applications.Tailoring hardware designs to the application can drastically increase resource utilization, which is important for meeting the strict requirements. Tools like Virtual Prototypes enable early design space exploration before any actual hardware is build, thus shortening time-to-market. Previous works have shown, that virtual prototypes can also be used as an analysis platform to identify promising hardware optimizations for a wide range of applications. In this work, we extend the approach and demonstrate its impact and practicality for the field of edge AI by analyzing a set of typical machine learning benchmark applications such as MLPerf Tiny. Our results show, that the tool can locate previously unknown optimizations.

[To page top](#summary) — [To posters at P1.1 (S1) on Tuesday 13](#P1.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Accelerating Quantized LLM Inference for Embedded RISC-V CPUs with Vector Extension (RVV)

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.08-LEE-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.08-LEE-abstract.pdf). Sub. \#17. Tuesday 13, at island 1.1 on S1. ([P1.1.08-Tue](#P1.1.08-Tue)).

**Yueh-Feng Lee**, Andes Technology. **Yi-Jui Chu**, Andes Technology. **Chih-Chung Huang**, Andes Technology. **Heng-Kuan Lee**, Andes Technology.

**Abstract**: This presentation focuses on optimizing the open-source llama.cpp project for the RISC-V vector extension. Specifically, we evaluate the performance of the LLM models running on an Andes AX45MPV RVV core implemented on FPGA. With VLEN 512, the 4-bit TinyLlama 1.1B model achieves a 21.7x speedup, and scaling results suggest that a single RVV core can achieve near real-time inference. Additionally, ongoing efforts are focused on optimizing smaller DeepSeek-related models to enhance efficiency on RISC-V hardware.

[To page top](#summary) — [To posters at P1.1 (S1) on Tuesday 13](#P1.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Supporting Sparse Inference in XNNPACK with RISC-V Vector Extension

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.09-CHEN-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.09-CHEN-abstract.pdf). Sub. \#77. Tuesday 13, at island 1.1 on S1. ([P1.1.09-Tue](#P1.1.09-Tue)).

**Gary Yi-Hung Chen**, Andes Technology. **Eric Hung-Yuan Chang**, Andes Technology. **Alan Quey-Liang Kao**, Andes Technology.

**Abstract**: Leveraging sparsity in neural network weights can significantly enhance efficiency when deploying models on mobile and edge devices. However, within the RISC-V ecosystem, a complete solution for sparse inference remains unavailable. This proposal identifies the challenges in enabling sparse inference for the RISC-V Vector Extension (RVV) and presents preliminary experimental findings that highlight existing gaps. While implementation and optimization efforts are ongoing, our goal is to contribute to both the RISC-V community and the XNNPACK project.

[To page top](#summary) — [To posters at P1.1 (S1) on Tuesday 13](#P1.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Accelerating AI Models with Andes Matrix Multiplication (AMM) and RISC-V Vector (RVV) extensions: From CNNs to LLMs

[Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.10-HUNG-abstract.pdf). Sub. \#86. Tuesday 13, at island 1.1 on S1. ([P1.1.10-Tue](#P1.1.10-Tue)).

**Pei-Hsiang Hung**, Andes Technology. **Chung-Hua Yen**, Andes Technology. **I-WEI WU**, Andes Technology.

**Abstract**: Matrix multiplication is a critical operation in a wide range of compute-intensive applications, including machine learning, image processing, and scientific computing. The computational demands of large-scale matrix operations necessitate specialized hardware acceleration to improve efficiency and performance. To address this challenge, RISC-V International (RVI) formed the Integrated Matrix Extension (IME) Task Group. To serve immediate market demands, Andes Technology implements the Andes Matrix Multiplication (AMM) instruction set, an extension to the RISC-V Vector Extension (RVV), which Andes presented in IME meetings. The AMM instruction set introduces two primary enhancements:

1.  Matrix operations optimized for 8-bit integers, specifically targeting AI and deep learning applications
2.  Advanced 2D load/store instructions that minimize memory access overhead

To assess AMM’s capabilities, we integrated it into the Intermediate Representation Execution Environment (IREE) for efficient compilation and execution on AMM-enabled RISC-V systems. A key aspect of this implementation involved extending IREE’s compilation infrastructure, which included:

1.  Developing a new MLIR pass to tensorize matrix multiplication and tensor data load/store operations
2.  Designing a custom MLIR dialect tailored for AMM to support all its instructions.
3.  Implementing conversion passes to lower matrix multiplication and tensor operations from the vector dialect to AMM one

Our evaluation covered a broad spectrum of AI models, ranging from convolutional neural networks (CNNs) to large language models (LLMs), to measure performance improvements. This presentation explores the integration process, shares benchmark results, and discusses strategies for optimizing AI workloads using AMM and RISC-V Vector Extensions. We also examine the challenges encountered during AI model compilation and consider future developments in RISC-V-based AI acceleration.

[To page top](#summary) — [To posters at P1.1 (S1) on Tuesday 13](#P1.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### V-Seek: Accelerating LLM Reasoning on Open-hardware Server-class RISC-V Platforms

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.11-POVEDA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.11-POVEDA-abstract.pdf). Sub. \#157. Tuesday 13, at island 1.1 on S1. ([P1.1.11-Tue](#P1.1.11-Tue)).

**Javier Poveda**, Politecnico di Torino. **Mohamed Amine Hamdi**, Politecnico di Torino. **Alessio Burrello**, Politecnico di Torino and UniversitÃ  di Bologna. **Daniele Jahier Pagliari**, Politecnico di Torino. **Luca Benini**, Università di Bologna and ETH Zurich.

**Abstract**: The recent exponential growth of Large Language Models (LLMs) has relied on GPU-based systems. However, CPUs are emerging as a flexible and lower-cost alternative, especially when targeting inference and reasoning workloads. RISC-V is rapidly gaining traction in this area, given its open and vendor-neutral ISA. However, the RISC-V hardware for LLM workloads and the corresponding software ecosystem are not fully mature and streamlined, given the requirement of domain-specific tuning. This paper aims at filling this gap, focusing on optimizing LLM inference on the Sophon SG2042, the first commercially available many-core RISC-V CPU with vector processing capabilities. On two recent state-of-the-art LLMs optimized for reasoning, DeepSeek R1 Distill Llama 8B and DeepSeek R1 Distill QWEN 14B, we achieve 4.32/2.29 token/s for token generation and 6.54/3.68 token/s for prompt processing, with a speed up of up 2.9X/3.0X compared to our baseline.

[To page top](#summary) — [To posters at P1.1 (S1) on Tuesday 13](#P1.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Enabling High Performance RISC-V Software for AI in the Real World

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.12-MURRAY-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.1.12-MURRAY-abstract.pdf). Sub. \#232. Tuesday 13, at island 1.1 on S1. ([P1.1.12-Tue](#P1.1.12-Tue)).

**Alastair Murray**, Codeplay. **Jeremy Bennett**, Embecosm.

**Abstract**: The first part of this talk presents SYCL from the Khronos Group, an open, cross-platform abstraction layer parallel to C++ which enables heterogeneous computing. Alongside this we present oneAPI, a set of heterogeneous libraries for performance across a variety of AI workloads, and recently contributed to the Unified Acceleration(UXL) Foundation. The UXL Foundation is a cross-industry effort led by Arm, Broadcom, Fujitsu, GE Healthcare, Google Cloud, Imagination, Intel, Samsung and Qualcomm.

The second part of this talk presents a real-world example of bringing up an AI system (PyTorch) on a RISC-V based accelerator. The example is entirely open source and uses a widely available FPGA board on which to run both the host and the RISC-V based accelerator. It is available as an application note to help others achieve high performance with RISC-V based AI systems. We present data to show the performance of the system.

[To page top](#summary) — [To posters at P1.1 (S1) on Tuesday 13](#P1.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

On Tuesday 13, at island P1.2 (S1)

------------------------------------------------------------------------

### RISC-V Cloud Computing Open Experimental Platform

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.2.01-WU-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.2.01-WU-abstract.pdf). Sub. \#83. Tuesday 13, at island 1.2 on S1. ([P1.2.01-Tue](#P1.2.01-Tue)).

**yuting wu**, ChinaTelecom. **Enfang Cui**, Chinatelecom. **Tianzheng Li**, China Telecom Corporation Limited Research Institute. **Qian Wei**, China Telecom Research Institute. **Rui She**, China Telecom Research Institute. **Jin Diao**, China Telecom Research Institute. **Zhiyuan Liang**, China Telecom Research Institute. **Yue GAO**, China Telecom Corporation Limited Research Institute. **Shulin Xu**, China Telecom Research Institute. **Minxin Guo**, Reseach Institute of China Telecom.

**Abstract**: This paper introduces the construction of a RISC-V cloud computing platform, addressing the shortfall of large-scale experimental environments for RISC-V. The platform integrates RISC-V customized hardware, Kubernetes-based cloud management, and optimized applications, forming a three-layer architecture consisting of heterogeneous computing infrastructure, a cloud-native management platform, and a container image repository. It manages a RISC-V cluster with over several thousand cores, adapts core cloud-native components, and completes end-to-end recompilation, fostering the development of the RISC-V cloud computing ecosystem and providing support for related research and practice.

[To page top](#summary) — [To posters at P1.2 (S1) on Tuesday 13](#P1.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### A cloud first: Scaleway's RISC-V servers

Sub. \#107. Tuesday 13, at island 1.2 on S1. ([P1.2.02-Tue](#P1.2.02-Tue)).

**Fabien Piuzzi**, Scaleway.

**Abstract**: This presentation outlines the motivation, challenges, and technical efforts behind the launch of Scaleway’s RISC-V cloud servers, detailing the process from research to deployment and the lessons learned.

We also discuss the future of RISC-V in datacenters and our expectations from hardware manufacturers to accelerate RISC-V adoption.

[To page top](#summary) — [To posters at P1.2 (S1) on Tuesday 13](#P1.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Open Challenges for a Production-ready Cloud Environment on top of RISC-V hardware

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.2.03-PRADES-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.2.03-PRADES-abstract.pdf). Sub. \#114. Tuesday 13, at island 1.2 on S1. ([P1.2.03-Tue](#P1.2.03-Tue)).

**Guillem Senabre Prades**, Barcelona Supercomputing Center. **Aaron Call**, Barcleona Supercomputing Center. **Ramon Nou Castell**, Barcelona Supercomputing Center.

**Abstract**: As part of the Vitamin-V European project, we have built a prototype of a RISC-V cluster managed by OpenStack, with the goal of realizing a functional RISC-V cloud ecosystem. In this poster we explain the hardware and software challenges encountered while porting some elements of OpenStack. We also discuss the current performance gaps that challenge a performance-ready cloud environment over such new ISA, an essential element to fulfill in order to achieve european technological sovereignty.

[To page top](#summary) — [To posters at P1.2 (S1) on Tuesday 13](#P1.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### High Performance RISC-V Processor for Application in Harsh Environments

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.2.04-HAWICH-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.2.04-HAWICH-abstract.pdf). Sub. \#20. Tuesday 13, at island 1.2 on S1. ([P1.2.04-Tue](#P1.2.04-Tue)).

**Malte G. Hawich**, Leibniz Universitaet Hannover, Institute of Microelectronic Systems. **Tobias Stuckenberg**, Leibniz Universitaet Hannover, Institute of Microelectronic Systems. **Malte Rücker**, Baker Hughes, Drilling Services. **Holger Blume**, Leibniz Universitaet Hannover.

**Abstract**: This work introduces a RISC-V processor designed for high-temperature environments, operating reliably at over 100 MHz and peaking at 180 MHz up to 175�C. Built using X-FAB XT018 180nm SOI technology, it addresses performance issues from thermal stress with a deeply pipelined architecture and modular execution pipelines.

Key features include out-of-order write-backs, efficient branch prediction, and tightly coupled SRAM caches. Reliability is enhanced through error correction. Thermal testing confirms stable performance, making it suitable for aerospace, energy, and industrial applications.

[To page top](#summary) — [To posters at P1.2 (S1) on Tuesday 13](#P1.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

On Tuesday 13, at island P1.3 (S1)

------------------------------------------------------------------------

### Programming and Modeling RISC-V on RISC-V architecture with ChatGPT assistance

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.01-BAKOWSKI-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.01-BAKOWSKI-abstract.pdf). Sub. \#21. Tuesday 13, at island 1.3 on S1. ([P1.3.01-Tue](#P1.3.01-Tue)).

**Przemyslaw Andrzej Bakowski**, Nantes University.

**Abstract**: This article presents the didactic and development platform to teach and model RISC-V ISA. Our method is two-fold (software/hardware) and self-contained (modeling RISC-V on RISC-V). The platform itself is largely affordable and running exclusively on open source software, modeling tools included. The initial didactical content is built from four Programming Labs – Plabs, and five Modeling Labs – MLabs.

PLabs start with simple examples involving arithmetical instructions and input/output operations. We also delve, with the help of the debugger, into the binary representations to understand the instruction formats and build binary code snippets.

MLabs start with a short introduction to Verilog HDL. With the following MLabs we study simple RISC-V architecture, first to model RV32I-subset with R-type instructions then to model full RV32I plus M subsets. Then, running on the RISC-V platform, we inject the generated binaries into the Verilog model.

As such the platform is open for further experimentation with RISC-V ISA based programming and modeling. Along with the programming and the modeling processes we specify ChatGPT prompts to generate the test bench codes.

[To page top](#summary) — [To posters at P1.3 (S1) on Tuesday 13](#P1.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### The RISE Project: Advancing AI on RISC-V

Sub. \#172. Tuesday 13, at island 1.3 on S1. ([P1.3.02-Tue](#P1.3.02-Tue)).

**Ludovic Henry**, Rivos. **Barna Ibrahim**, Member.

**Abstract**: This talk will explore how RISC-V is uniquely positioned to meet the demands of AI through a robust and flexible software ecosystem. We will examine the strength of RVV and Matrix extensions in accelerating AI workloads, alongside the numerous hardware offerings supporting AI development. The discussion will highlight ongoing contributions that enhance the RISC-V software stack, including optimized libraries, tools, and frameworks, and how the software ecosystem is getting ready. Key developments include Llama.cpp, GGML, PyTorch CPU, LiteRT, OpenBLAS, and more. Attendees will gain insights into practical implementations and collaborative efforts shaping the future of AI on RISC-V, equipping them with actionable knowledge to leverage RISC-V in their AI applications.

[To page top](#summary) — [To posters at P1.3 (S1) on Tuesday 13](#P1.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### GaZmusino: An extended edge RISC-V core with support for Bayesian Neural Networks

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.03-PEREZ-PEDRAJAS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.03-PEREZ-PEDRAJAS-abstract.pdf). Sub. \#31. Tuesday 13, at island 1.3 on S1. ([P1.3.03-Tue](#P1.3.03-Tue)).

**Samuel Perez Pedrajas**, University of Zaragoza. **Javier Resano**, University of Zaragoza. **Dario Suarez Gracia**, University of Zaragoza.

**Abstract**: As the demand for more transparent artificial intelligence models grows, Bayesian Neural Networks (BNN) offer a solution by enabling prediction uncertainty estimation. However, their computational requirements exceed those of traditional neural networks. This work introduces GaZmusino, a low-cost RISC-V core extended with instructions to accelerate 8.93x BNN inference.

[To page top](#summary) — [To posters at P1.3 (S1) on Tuesday 13](#P1.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### The REBECCA Hardware/Software Edge AI platform

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.04-MAVROIDIS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.04-MAVROIDIS-abstract.pdf). Sub. \#122. Tuesday 13, at island 1.3 on S1. ([P1.3.04-Tue](#P1.3.04-Tue)).

**Iakovos Mavroidis**, Technical University of Crete. **Holger Blasum**, SYSGO. **Ioannis Papaefstathiou**, EXAPSYS. **Konstantinos Georgopoulos**, Techincal University of Crete. **Pavlos Malakonakis**, EXAPSYS.

**Abstract**: The REBECCA project is pioneering advancements in edge AI systems using RISC-V technology, emphasizing power efficiency, scalability, and open-source accessibility. It integrates a multicore RISC-V-based architecture with AI-specific accelerators, neuromorphic computing, and security features to deliver a high-performance, cost-effective AI platform. The core of REBECCA is the CVA6 processor, leveraging a chiplet-based design and shared memory architecture to optimize real-time AI processing. The platform incorporates HyperRAM for high-speed data access and a custom software stack to maximize efficiency and security. Initial prototypes using U55C development boards and FPGA-based testing validate the feasibility of RISC-V for AI-driven applications. Future research will enhance neuromorphic computing, AI framework integration, and real-time performance optimization. With strong industry and academic collaboration, REBECCA is shaping the future of AI at the edge, positioning RISC-V as a compelling alternative to proprietary AI solutions.

[To page top](#summary) — [To posters at P1.3 (S1) on Tuesday 13](#P1.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### On-Device Federated Continual Learning on RISC-V-based Ultra-Low-Power SoC for Intelligent Nano-Drone Swarms

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.05-KRÖGER-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.05-KRÖGER-abstract.pdf). Sub. \#212. Tuesday 13, at island 1.3 on S1. ([P1.3.05-Tue](#P1.3.05-Tue)).

**Lars Kröger**, ETH Zurich. **Cristian Cioflan**, ETH Zurich. **Victor Kartsch**, ETH Zurich. **Luca Benini**, ETH Zurich; University of Bologna.

**Abstract**: RISC-V-based architectures are paving the way for efficient On-Device Learning (ODL) in smart edge devices. When applied across multiple nodes, ODL enables the creation of intelligent sensor networks that preserve data privacy. However, developing ODL-capable, battery-operated embedded platforms presents significant challenges due to constrained computational resources and limited device lifetime, besides intrinsic learning issues such as catastrophic forgetting. We face these challenges by proposing a regularization-based On-Device Federated Continual Learning algorithm tailored for multiple nano-drones performing face recognition tasks. We demonstrate our approach on a RISC-V-based 10-core ultra-low-power SoC, optimizing the ODL computational requirements. We improve the classification accuracy by 24% over naive fine-tuning, requiring 178 ms per local epoch and 10.5 s per global epoch, demonstrating the effectiveness of the architecture for this task.

[To page top](#summary) — [To posters at P1.3 (S1) on Tuesday 13](#P1.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Unlocking Performance, Profit, and Compliance: The RISC-V Approach to Medical AI

Sub. \#170. Tuesday 13, at island 1.3 on S1. ([P1.3.06-Tue](#P1.3.06-Tue)).

**Raja Gopal Hari Vijay Sitharaman**, Zoho Corporation.

**Abstract**: Medical AI applications—including diagnostics, predictive analytics, and robotic surgery—demand specialized processing capabilities and must meet stringent performance requirements. However, in medical AI commercialization, meeting these demands is only part of the challenge. A critical hurdle is ensuring compliance with stringent regulatory standards such as FDA (U.S.), CE (Europe), and MDR (Medical Device Regulation), while maintaining innovation, efficiency, and cost-effectiveness. Traditional, some proprietary architecture often present significant barriers to achieving this balance. In contrast, RISC-V, with its open-source, modular ISA design, offers a key to unlocking this potential and fosters open collaboration, accelerating AI-specific optimizations across diverse applications. Its flexibility allows for tailored AI acceleration and secure computing – leading to, for example, significantly faster image processing times in diagnostic imaging or lower latency in real-time. This and verifiable regulatory compliance across hardware, operating systems, and software stacks of the RISC-V ecosystem, lower entry barriers and increase profitability by reducing development costs and speeding up time-to-market. This paper explores how RISC-V’s open ecosystem supports regulatory adherence, drives AI-optimized medical solutions, and unlocks new opportunities for scalable, secure, and cost-effective AI-driven healthcare innovations.

[To page top](#summary) — [To posters at P1.3 (S1) on Tuesday 13](#P1.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### LLMPoint: A Fast Sampling and Performance Analysis Framework for LLM Inference on RISC-V

Sub. \#117. Tuesday 13, at island 1.3 on S1. ([P1.3.07-Tue](#P1.3.07-Tue)).

**Luoshan Cai**, Beijing Institute of Open Source Chip.

**Abstract**: Large language models (LLMs) are emerging as a critical application scenario for RISC-V architecture, driving significant demands for software and hardware performance optimization. Efficient design of RISC-V systems requires a fast and accurate performance evaluation methodology. However, current approaches for LLM inference on RISC-V platforms primarily focus on basic operators like GEMM rather than full workloads. It neglects some software-hardware co-optimization effects such as speculative decoding, resulting in inaccurate performance evaluation. To fill this gap, we propose a framework for running and analyzing LLM workloads on RISC-V platforms. We further observe that executing full workloads incurs prohibitive time costs. To overcome the problem, we propose a novel sampling workflow which extracts representative program segments that dominate the performance. This tool enables efficient and precise evaluation, facilitating optimization on both RISC-V software and hardware.

[To page top](#summary) — [To posters at P1.3 (S1) on Tuesday 13](#P1.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Performance and Co-Design Evaluation of RISC-V and Xilinx MicroBlaze V on ArtyA7-100T FPGA

Sub. \#153. Tuesday 13, at island 1.3 on S1. ([P1.3.08-Tue](#P1.3.08-Tue)).

**Sravani Thota**, guest. **Deepak V Katkoria**, Guest.

**Abstract**: This study compares the performance, power efficiency, and hardware/software co-design of open-source RISC-V soft-cores (VexRiscv, PicoRV32) with Xilinx’s proprietary MicroBlaze V on the Arty A7-100T FPGA. Using Xilinx Vivado and Vitis toolchains, we evaluate resource utilization (LUTs, FFs, BRAM), execution speed, power consumption, and debugging frameworks. Our findings highlight trade-offs in flexibility, ecosystem support, and integration, offering insights for embedded system designers selecting FPGA-based processors.

“We would like to present this work as a poster only.”

[To page top](#summary) — [To posters at P1.3 (S1) on Tuesday 13](#P1.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### ACE: Atomic Cryptography Extension for RISC-V

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.09-AVANZI-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.09-AVANZI-abstract.pdf). Sub. \#74. Tuesday 13, at island 1.3 on S1. ([P1.3.09-Tue](#P1.3.09-Tue)).

**Roberto Avanzi**, Qualcomm, and University of Haifa. **Ruud Derwig**, Synopsys. **Luis Fiolhais**, Independent Researcher. **Richard Newell**, Microchip. **Barry Spinney**, Independent Researcher. **Tolga Yalcin**, Qualcomm.

**Abstract**: We propose the Atomic Cryptographic Extension (ACE), an ISA extension to enable the secure implementation of cryptographic operations.

ACE separates programming a key in the system for use by software from the actual use of the key, allowing separated environments to perform these functions. For instance, setting the key can be delegated to a secure TEE applet. ACE also provides instructions to perform cryptographic operations in an atomic fashion, in contrast to current round-based AES extensions, that by their nature cannot conceal the key.

This is achieved by configuring new architectural registers, called the Context Holding Registers (CHR), with the value of a key together with metadata that determines its usage and lifecycle management settings. The contents of these registers can then only be exported in an encrypted and authenticated format which can be later reimported.

This allows software to securely use multiple keys, and the system stack to support context switching and even preservation of keys during process or VM migration.

ACE is work in progress of the High Assurance Cryptography (HAC) TG of RISC-V International.

[To page top](#summary) — [To posters at P1.3 (S1) on Tuesday 13](#P1.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### RISC-V Vector Extension. A Case Study on Time Series Analysis

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.10-SANCHEZ-YUN-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.3.10-SANCHEZ-YUN-abstract.pdf). Sub. \#111. Tuesday 13, at island 1.3 on S1. ([P1.3.10-Tue](#P1.3.10-Tue)).

**Jose Sanchez-Yun**, University of Málaga. **Ivan Fernandez**, Computer Sciences Department, Barcelona Supercomputing Center. **Eladio Gutierrez**, University of Málaga. **Ricardo Quislant**, University of Málaga. **Oscar Plata**, University of Málaga.

**Abstract**: Time series analysis is a topic of great interest, as it enables modeling, prediction, and understanding of sequential events across various domains. One of the most powerful tools in this field is Matrix Profile, which allows for scalable and accurate detection of anomalies and repetitive patterns. Specifically, SCAMP has emerged as one of the most efficient methods for computing the Matrix Profile due to its robustness, efficiency, and high parallelization capability. Vectorization is a powerful optimization technique for these algorithms, as it exploits SIMD instructions in modern CPUs to enhance computational efficiency. In this context, the RISC-V Vector Extension (RVV) introduces a flexible vector model with dynamic lengths. This enables algorithm optimization across different hardware platforms without requiring source code modifications. In this paper, we vectorize the SCAMP algorithm using the RISC-V Vector Extension and analyze the achieved speedup compared to the non-vectorized baseline. Additionally, we explore the benefits of dynamic vectors and compare them with alternative implementations. The results show speedup improvements of up to 94× over the sequential version of the algorithm using vectors of 8K bits and floating-point data of 64 bits.

[To page top](#summary) — [To posters at P1.3 (S1) on Tuesday 13](#P1.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

On Tuesday 13, at island P1.4 (S1)

------------------------------------------------------------------------

### Enabling Front-End SoC Integration Automation Flows for Large RISC-V Designs

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.4.01-AKTOUF-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.4.01-AKTOUF-abstract.pdf). Sub. \#129. Tuesday 13, at island 1.4 on S1. ([P1.4.01-Tue](#P1.4.01-Tue)).

**Chouki Aktouf**, Defacto Technologies. **Allen Muuwil**, Defacto Technologies. **Adrien Lecardonnel**, Defacto Technologies.

**Abstract**: This paper presents a front-end design framework for RISC V system on chip designs. The framework manages RTL and design collaterals pre synthesis and provides design engineers with a high level of automation to build and restructure subsystems and full chip. A focus is given to the enablement of RTL design restructuring to cover physically and power aware RTL design requirements.

[To page top](#summary) — [To posters at P1.4 (S1) on Tuesday 13](#P1.4-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### RISC-V as an ASIP Platform for Portable Hearing Aid Devices

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.4.02-SCHÖNEWALD-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P1.4.02-SCHÖNEWALD-abstract.pdf). Sub. \#70. Tuesday 13, at island 1.4 on S1. ([P1.4.02-Tue](#P1.4.02-Tue)).

**Sven Schönewald**, Leibniz University Hanover - Institute of Microelectronic Systems. **Viktor Schneider**, Leibniz University Hanover - Institute of Microelectronic Systems. **Simon Klein**, Leibniz University Hanover - Institute of Microelectronic Systems. **Holger Blume**, Leibniz University Hanover - Institute of Microelectronic Systems.

**Abstract**: Hearing loss is one of the most prevalent sensory impairments. The use of hearing aids with adaptable personalized signal processing has the potential to further enhance the social lives of those affected. To investigate the extent of possible improvements, high-level programmable, low-power, and portable behind-the-ear (BTE) research platforms are required to conduct studies in real-world settings, not just in laboratory environments. However, the market for hearing aid processors is highly restrictive and often relies on proprietary and closed source signal processors. As a key component towards an open source hearing aid, this paper presents an overview of the performance of two different state-of-the-art hearing aid algorithms on a RISC-V based application-specific instruction set processor (ASIP). A number of standard instructions set extensions (ISEs) are profiled and synthesized for a 22nm technology. A systematic survey of the performance reveals a requirement for specialised, custom hardware. The processor is further optimised using a custom coordinate rotation digital computer (CORDIC) unit for non-linear calculations.

[To page top](#summary) — [To posters at P1.4 (S1) on Tuesday 13](#P1.4-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Utilising RISC-V to reduce data centre CPU energy consumption by up to 80% by delivering five fold application performance in general purpose compute.

Sub. \#168. Tuesday 13, at island 1.4 on S1. ([P1.4.03-Tue](#P1.4.03-Tue)).

**Ed Nutting**, CTO Vypercore.

**Abstract**: The open standard RISC-V ISA has enabled greater innovation in processor architecture than has ever been possible before. With RISC-V flexibility and extensibility it’s possible to reimagine and redefine traditional processor architecture where, in a world beyond Moore’s Law, compute-intensive, managed-language applications are reaching the limits of traditional efficient general-purpose compute capability.

By moving the memory allocation management complexity from software to hardware, many of the processor cycles needed to execute typical allocation functions of software objects in memory can be avoided, delivering significant performance advantages and energy savings.

This session will detail the concepts and techniques fundamental to the adoption of a new object memory model, enabling full memory safety at gate level within the processor, as well as enhancing cache utilisation, minimising event processing latency, and reducing overall memory heap requirements. It will show how these significant optimisations can be brought to modern power efficiency sensitive, compute-intensive, applications, include large-scale web enterprises, high volume data analytics, bioinformatics, and the complex data processing needs of compute intensive applications.

[To page top](#summary) — [To posters at P1.4 (S1) on Tuesday 13](#P1.4-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### RISC-V Certification Program Status

Sub. \#25. Tuesday 13, at island 1.4 on S1. ([P1.4.04-Tue](#P1.4.04-Tue)).

**Larry Lapides**, Synopsys.

**Abstract**: RISC-V International has developed a certification program – the RISC-V Certification Program or RVCP – to enable portability of software across various implementations of specified RISC-V profiles and platforms and to accelerate growth of the RISC-V ecosystem. RVCP is developing certification tests plans, including coverage models, for those profiles and platforms. Tests may come from a variety of sources, and may be either open source or proprietary. Those tests will be delivered to RVCP customers, who will then deliver test logs/reports to RVI to confirm and award certification. RVCP will launch in 2025 with full certification support for a microcontroller profile and the beta release of the test suite for the RVA23 applications processor profile. Interested parties should reach out to RVI for more information at certification@riscv.org.

[To page top](#summary) — [To posters at P1.4 (S1) on Tuesday 13](#P1.4-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

On Tuesday 13, at island P2.1 (S2)

------------------------------------------------------------------------

### Customized RISC-V In a Simple Game Console

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.01-PRIKRYL-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.01-PRIKRYL-abstract.pdf). Sub. \#97. Tuesday 13, at island 2.1 on S2. ([P2.1.01-Tue](#P2.1.01-Tue)).

**Zdenek Prikryl**, Codasip. **Pavel Snobl**, Codasip.

**Abstract**: RISC-V processors have found their way into products already. The openness of the RISC-V ISA, the strong ecosystem, and, more importantly, the ability to innovate through custom extensions have made this possible. Custom extensions can target any domain including game consoles. This paper will focus on the NES emulator and how it can be accelerated on RISC-V processors. Firstly, we will create a virtual platform with the standard RISC-V processor in a RV32IMCBZc configuration. Then, we will explore different instruction set extensions that help with performance. The virtual platform and the design space exploration will be done using a set of EDA tools focused on (not only) RISC-V customization. The process contains software profiling, looking at the instruction set sequences, creating new instructions in the processor description language that allows regeneration of the programming and simulation tools, and implementing the processor in RTL. Once the performance of the virtual platform is at an acceptable level, we will perform PPA analysis to understand the impact of the added instructions in processor implementation.

[To page top](#summary) — [To posters at P2.1 (S2) on Tuesday 13](#P2.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### FPHUB-RISCV: HUB Floating-Point Unit in RISC-V Platform -- Format definition

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.02-HORMIGO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.02-HORMIGO-abstract.pdf). Sub. \#26. Tuesday 13, at island 2.1 on S2. ([P2.1.02-Tue](#P2.1.02-Tue)).

**Javier Hormigo**, Universidad de Malaga. **Julio Villalba**, Universidad de Malaga. **Gerardo Bandera**, Universidad de Malaga. **Sonia Gonzalez-Navarro**, Universidad de Malaga. **Alfonso Martinez-Conejo**, Universidad de Malaga. **Alejandro Fuster**, Universidad de Malaga. **Jesus Lastre**, Universidad de Malaga. **Oscar Plata**, University of Malaga. **Emilio Lopez Zapata**, Universidad de Malaga.

**Abstract**: FPHUB-RISCV is a 2-year “proof of concept” project within the Spanish PERTE chip. It aims to implement a new floating-point arithmetic unit for RISC-V targeting low-resource applications. The unit will use a new floating-point format called FPHUB, which allows us to simplify the implementation logic while keeping the same precision as the IEEE 754 standard.

[To page top](#summary) — [To posters at P2.1 (S2) on Tuesday 13](#P2.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Implementing Runtime-Configurable Endianness in RISC-V: Challenges and Solutions

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.03-HUNTER-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.03-HUNTER-abstract.pdf). Sub. \#105. Tuesday 13, at island 2.1 on S2. ([P2.1.03-Tue](#P2.1.03-Tue)).

**Lawrence Hunter**, Codethink. **Roan Richmond**, Codethink. **Ben Dooks**, Codethink.

**Abstract**: The RISC-V Privileged Specification introduced dynamic endianness switching in version 1.12, though no commercial hardware yet supports it. This work extends QEMU to enable big-endian execution, allowing the booting of a big-endian Linux system with OpenSBI. Modifications were required across QEMU, OpenSBI, the Linux kernel, and supporting libraries to ensure correct memory operations, instruction encoding, and runtime patching. The project demonstrates the feasibility of big-endian support for RISC-V, providing a foundation for future hardware and software development.

[To page top](#summary) — [To posters at P2.1 (S2) on Tuesday 13](#P2.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Vaquita: A Portable Four Stage Pipeline RISC-V Vector Co Processor

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.04-LATIF-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.04-LATIF-abstract.pdf). Sub. \#126. Tuesday 13, at island 2.1 on S2. ([P2.1.04-Tue](#P2.1.04-Tue)).

**Muhammad Latif**, Usman Institute of Technology. **Shahzaib Kashif**, Usman Institute of Technology. **Dr. Farhan Ahmed Karim**, Usman Institute of Technology. **Dr. Ali Ahmed**, Usman Institute of Technology.

**Abstract**: This paper introduces a CHISEL based RISC-V Vector (RVV) v1.0 coprocessor, named Vaquita, designed to enhance vector processing performance. The architecture features a meticulously optimized 4-stage pipeline that maximizes computational throughput and minimizes latency, enabling efficient handling of complex vector operations. Built on a portable coprocessor paradigm, The solution facilitates easy integration with a variety of RISC-V-based systems using its plug and play compatible interface, ensuring reliable interoperability with RISC- V cores.

[To page top](#summary) — [To posters at P2.1 (S2) on Tuesday 13](#P2.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Vicuna 2.0 : A Configurable RISC-V Embedded Vector Hardware Platform

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.05-JONES-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.05-JONES-abstract.pdf). Sub. \#178. Tuesday 13, at island 2.1 on S2. ([P2.1.05-Tue](#P2.1.05-Tue)).

**Jefferson Parker Jones**, Technical University of Vienna. **Philipp van Kempen**, Technical University of Munich. **Daniel Mueller-Gritschneder**, TU Wien.

**Abstract**: Vicuna 2.0 is an open-source SystemVerilog implementation of the Zve32x, Zve32f, and Zvfh extensions built upon the previous work of the Vicuna project. Vicuna 2.0 is extremely configurable, allowing for detailed analysis and evaluation of vector unit configurations targeted for specific workloads as demonstrated by a design space exploration in this work.

[To page top](#summary) — [To posters at P2.1 (S2) on Tuesday 13](#P2.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### XiangShan Kunminghu V2: Architectural Innovations and Ecosystem Development of an Open-Source High-Performance RISC-V Processor

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.06-TANG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.06-TANG-abstract.pdf). Sub. \#225. Tuesday 13, at island 2.1 on S2. ([P2.1.06-Tue](#P2.1.06-Tue)).

**Haojin Tang**, State Key Lab of Processors, Institute of Computing Technology, Chinese Academy of Sciences. **Haoyuan Feng**, University of Chinese Academy of Sciences. **Yungang Bao**, Beijing Institute of Open Source Chip.

**Abstract**: XiangShan Kunminghu V2, an open-source RISC-V processor achieving 45 SPEC06 at 3GHz, implements RVA23 Profile with hardware virtualization and 1024-bit vector processingin a single instruction, supported by an agile development ecosystem attracting 6k GitHub stars. The industry-academia co-design mechanism through BOSC innovation consortium has enabled 24 industrial partnerships, providing open source and shared base technical support for advanced computing ecosystem.

[To page top](#summary) — [To posters at P2.1 (S2) on Tuesday 13](#P2.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Implementing out-of-order issue in CVA6 for efficient support of long variable latency instructions

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.07-GUTHMULLER-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.07-GUTHMULLER-abstract.pdf). Sub. \#34. Tuesday 13, at island 2.1 on S2. ([P2.1.07-Tue](#P2.1.07-Tue)).

**Eric Guthmuller**, Univ. Grenoble Alpes, CEA, List. **Tanuj Khandelwal**, Univ. Grenoble Alpes, CEA, List.

**Abstract**: OpenHW Group’s RISC-V CVA6 core, while being heavily configurable, even supporting superscalar execution, is still limited to in-order issue. Out-of-order execution allows for more efficient instruction scheduling in the case of non-predictable latency, such as memory accesses for example. We propose adaptations to the CVA6 core pipeline by adding one pipeline stage and reorder queues to issue most instructions out-of-order. Our work is also superscalar-ready as multiple instruction queues are instantiated in parallel. We measured a 10% performance increase on Coremark with our modifications.

[To page top](#summary) — [To posters at P2.1 (S2) on Tuesday 13](#P2.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Automating RISC-V Custom Instruction Integration leveraging High-Level Synthesis

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.08-EGERT-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.1.08-EGERT-abstract.pdf). Sub. \#95. Tuesday 13, at island 2.1 on S2. ([P2.1.08-Tue](#P2.1.08-Tue)).

**Florian Egert**, Siemens AG Austria. **Bernhard Fischer**, Siemens AG Austria.

**Abstract**: Adapting and optimizing systems for maximum performance under tight area and power constraints in a cost-effective way requires design flows that are flexible, provide quick results, and offer automation support to reduce time-intensive and error-prone manual coding. High-Level Synthesis (HLS) is a design process that transforms high-level software algorithms into hardware descriptions on RTL, enabling design exploration and optimization of stringent design constraints. This work presents an automated methodology leveraging HLS for hardware acceleration in RISC-V based open-source cores supporting CV-X-IF, an interface enabling extension of RISC-V cores by custom instructions. This approach, combining hardware synthesis with a processor-agnostic extension interface, enables designers to efficiently accelerate and optimize their diverse applications.

[To page top](#summary) — [To posters at P2.1 (S2) on Tuesday 13](#P2.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

On Tuesday 13, at island P2.2 (S2)

------------------------------------------------------------------------

### RISC-V VPU: A High-Performance Video Transcoding Card

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.01-WU-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.01-WU-abstract.pdf). Sub. \#98. Tuesday 13, at island 2.2 on S2. ([P2.2.01-Tue](#P2.2.01-Tue)).

**yuting wu**, ChinaTelecom. **Enfang Cui**, Chinatelecom. **Tianzheng Li**, China Telecom Corporation Limited Research Institute. **Qian Wei**, China Telecom Research Institute. **Rui She**, China Telecom Research Institute. **Yue GAO**, China Telecom Corporation Limited Research Institute. **Zhiyuan Liang**, China Telecom Research Institute. **Jin Diao**, China Telecom Research Institute. **Shulin Xu**, China Telecom Research Institute. **Minxin Guo**, Reseach Institute of China Telecom.

**Abstract**: With the rapid growth of the video surveillance and streaming media markets, traditional video processing solutions are facing challenges such as inefficiency, high costs, and poor flexibility. To address these issues, we have developed RISC-V VPU, a video transcoding card based on the RISC-V architecture. RISC-V VPU employs a Multi-SoC RISC-V architecture, supports 40 channels 1080P@25fps parallel processing of real-time video streams, and equips with 20 TOPS AI computing power, achieving deep integration of video compression and AI analysis. The accompanying OpenVPU SDK and VPU Server engine provide efficient management interfaces and multi-card collaboration capabilities, significantly enhancing VPU cluster resource utilization. Verification tests have demonstrated that RISC-V VPU excels in various application scenarios, offering an efficient and cost-effective solution for large-scale video processing and laying the foundation for the construction of intelligent video processing infrastructure.

[To page top](#summary) — [To posters at P2.2 (S2) on Tuesday 13](#P2.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### RISC-V Heterogeneous Programming Paradigm: Atomic IO Enqueue (AIOE) Extension and AIOE with Virtualization

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.02-GUO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.02-GUO-abstract.pdf). Sub. \#148. Tuesday 13, at island 2.2 on S2. ([P2.2.02-Tue](#P2.2.02-Tue)).

**Ren Guo**, Alibaba Damo Academy.

**Abstract**: With the increasing diversification of intelligent computing workloads, traditional programming paradigms face multidimensional challenges driven by architectural innovations. Addressing the concurrent demands of heterogeneous tasks, including AI inference, real-time graphics rendering, and high-performance signal processing, this presentation focuses on atomic IO enqueue instructions - the core technology enabling hardware accelerator interactions in heterogeneous computing architectures. This approach establishes efficient accelerator communication mechanisms through hardware primitives such as 64-byte atomic enqueue transfers and queue status feedback. At the protocol level, PCIe specifications define DMWr TLP (Transaction Layer Packet) for non-post write operations, while Armv8.7/9.2 implements 64-byte atomic enqueue operations via ST64BV instructions, and x86 architectures provide comparable functionality through MOVDIR64B and ENQCMD(S) instructions.

This presentation introduces RISC-V’s Atomic IO Enqueue Extension (AIOE) and its virtualization enhancements: the G-stage Page Table In-Process Context (GIPC) mechanism for RISC-V IOMMU, which improves accelerator sharing work queue in multi-tenant environments. In addition, we will share AIOE’s latency mitigation approach for PCI-e.

[To page top](#summary) — [To posters at P2.2 (S2) on Tuesday 13](#P2.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### RIVeT-Co: Time-Predictable RISC-V based Vector Co-processor for High-Performance Computing

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.03-SINGH-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.03-SINGH-abstract.pdf). Sub. \#151. Tuesday 13, at island 2.2 on S2. ([P2.2.03-Tue](#P2.2.03-Tue)).

**SONAM SINGH**, Indraprastha Institute of Information Technology Delhi. **Seetharaman Raja**, Thales India Private Limited, Bangalore. **Subhra Kanti Das**, Thales India Private Limited, Bangalore. **Sujay Deb**, IIIT Delhi.

**Abstract**: High-Performance Computing (HPC) is becoming increasingly important as the demand for more computational power grows across various domains like artificial intelligence, embedded systems, and medical research. The applications in these domains often involve complex simulations, large-scale data analysis, and advanced modeling, which require potent hardware and software to process data efficiently. Modern real-time embedded systems utilize various timing-aware scheduling strategies for the efficient execution of such high-performance applications. However, in the absence of a specified worst-case execution time (WCET), it is difficult to provide a predictable execution time for applications running on these systems. WCET is essential for real-time systems where timely responses to events are critical for correct system operation, especially in safety-critical applications like medical devices or automotive control systems. In this article, we propose a RISC-V-based vector co-processor that has consistent, repeatable timing behavior with no timing anomalies, which allows for precise and efficient WCET analysis while maintaining the efficiency and performance often found in other vector processors.

[To page top](#summary) — [To posters at P2.2 (S2) on Tuesday 13](#P2.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### The Eruption of RISC-V in HPC: Earth Sciences Codes on Long Vector Architectures

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.05-VIZCAINO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.05-VIZCAINO-abstract.pdf). Sub. \#219. Tuesday 13, at island 2.2 on S2. ([P2.2.05-Tue](#P2.2.05-Tue)).

**Pablo Vizcaino**, Barcelona Supercomputing Center. **Fabio Banchelli**, Barcelona Supercomputing Center. **David Jurado**, Barcelona Supercomputing Center. **Marta Garcia-Gasulla**, Barcelona Supercomputing Center. **Filippo Mantovani**, Barcelona Supercomputing Center.

**Abstract**: In this research poster, we present the performance study and optimization of two solid earth physics applications, namely Seissol and Fall3D, on a long vector architecture RISC-V chip. We focus our optimizations on increasing the vectorization of the applications and taking advantage of the full vector length of the machine. The techniques used in our research include merging multiple small instances of linear algebra kernels to expose more data-level parallelism (batching), redefining data structures, and rewriting loops to facilitate the vectorization done by the compiler. We highlight the portability of our solutions, making them architecture-agnostic which granted us performance speedups among different machines. We present speedups ranging from 6x to 30x in the RISC-V prototype, but also substantial speedups on an Intel supercomputer (Marenostrum4) and the NEC SX-Aurora architecture.

[To page top](#summary) — [To posters at P2.2 (S2) on Tuesday 13](#P2.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### LEN5: an Out-Of-Order, Modular, Edge-Oriented RISC-V CPU

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.06-PETROLO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.06-PETROLO-abstract.pdf). Sub. \#176. Tuesday 13, at island 2.2 on S2. ([P2.2.06-Tue](#P2.2.06-Tue)).

**Vincenzo Petrolo**, Politecnico di Torino. **Flavia Guella**, Politecnico di Torino. **Michele Caon**, Politecnico di Torino, EPFL. **Mattia Mirigaldi**, Politecnico di Torino. **Guido Masera**, Politecnico di Torino. **Maurizio Martina**, Politecnico di Torino.

**Abstract**: This work presents LEN5, a modular 64-bit RISC-V processor featuring an Out-of-Order (OoO) execution pipeline. By efficiently handling dependencies and masking latency, LEN5 achieves over 20% higher Instructions Per Cycle (IPC) than in-order designs and up to a 20% frequency boost. The architecture employs speculative execution, dynamic scheduling, and an optimized commit strategy to enhance performance while maintaining scalability. Benchmark results demonstrate LEN5’s efficiency, particularly in precision-sensitive workloads, with up to a 2.4× reduction in instruction count.

[To page top](#summary) — [To posters at P2.2 (S2) on Tuesday 13](#P2.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### CVA6S+: A Superscalar RISC-V Core with High-Throughput Memory Architecture

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.07-TEDESCHI-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.07-TEDESCHI-abstract.pdf). Sub. \#186. Tuesday 13, at island 2.2 on S2. ([P2.2.07-Tue](#P2.2.07-Tue)).

**Riccardo Tedeschi**, University of Bologna. **Gianmarco Ottavi**, University of Bologna. **Nils Wistoff**, ETH Zurich. **Zexin Fu**, ETH Zurich. **Filippo Grillotti**, STMicroelectronics. **Fabio De Ambroggi**, STMicroelectronics. **Elio Guidetti**, STMicroelectronics. **César Fuguet**, Univ. Grenoble Alpes, Inria. **Luca Benini**, ETH Zurich, University of Bologna. **Davide Rossi**, University of Bologna.

**Abstract**: Open-source RISC-V cores are increasingly adopted in high-end embedded domains such as automotive, where maximizing instructions per cycle (IPC) is becoming critical. Building on the industry-supported open-source CVA6 core and its superscalar variant, CVA6S, we introduce CVA6S+, an enhanced version incorporating improved branch prediction, register renaming and enhanced operand forwarding. These optimizations enable CVA6S+ to achieve a 43.5% performance improvement over the scalar configuration and 10.9% over CVA6S, with an area overhead of just 9.30% over the scalar core (CVA6). Furthermore, we integrate CVA6S+ with the OpenHW Core-V High-Performance L1 Dcache (HPDCache) and report a 74.1% bandwidth improvement over the legacy CVA6 cache subsystem.

[To page top](#summary) — [To posters at P2.2 (S2) on Tuesday 13](#P2.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Enabling Reconfigurable High-Throughput RISC-V Systems through Barrel-Processing

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.08-ABDELHAMID-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.2.08-ABDELHAMID-abstract.pdf). Sub. \#224. Tuesday 13, at island 2.2 on S2. ([P2.2.08-Tue](#P2.2.08-Tue)).

**Riadh Ben Abdelhamid**, Heidelberg University. **Dirk Koch**, Heidelberg University.

**Abstract**: Traditional optimization techniques for higher-speed operation of CPU cores don’t work well, when targeting FPGAs. his mostly holds with one exception: barrel processing, which is a technique that uses aggressive pipelining together with multithreading such that any pipeline related conflicts will be resolved before a thread is restarted again. This article will outline the advantages of barrel processing for both CPU implementations on ASICs and FPGA targets.

[To page top](#summary) — [To posters at P2.2 (S2) on Tuesday 13](#P2.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

On Tuesday 13, at island P2.3 (S2)

------------------------------------------------------------------------

### FGMT-RiscV: A fine grained multi threading processor for FPGA systems

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.01-LANG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.01-LANG-abstract.pdf). Sub. \#19. Tuesday 13, at island 2.3 on S2. ([P2.3.01-Tue](#P2.3.01-Tue)).

**Bernhard Lang**, Hochschule Osnabrück, University of Applied Sciences.

**Abstract**: A special RiscV variant, a fine-grained multi-threaded processor designed for FPGA applications, is presented. Heart of this processor is a processing pipeline which is realized via AXI streaming. It is able to process multiple instruction streams, each of which is represented by a thread token containing a program counter and a thread identifier which selects the associated register set. Thread tokens enter the pipeline at the input and are emitted at the output with modified program counter. Instruction and data memories are accessed via streaming interfaces at the side of the pipeline. Inside the processor the processing pipeline, thread handling infrastructure and a token fifo form a closed ring in which the thread tokens circulate. The ring enables monitoring and manipulation of the thread tokens and provides resources for connecting high-level debuggers. An example system even suited for small FPGAs is presented that consists of the processor with block ram, Wishbone bus and some peripherals. A GDB server runs as thread 0, which is directly connected to the GNU debugger via serial interface and enables debugging the other threads of the processor.

[To page top](#summary) — [To posters at P2.3 (S2) on Tuesday 13](#P2.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Learning Computer Architecture with a Visual Simulation of RISC-V Processors

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.02-STAFFORD-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.02-STAFFORD-abstract.pdf). Sub. \#87. Tuesday 13, at island 2.3 on S2. ([P2.3.02-Tue](#P2.3.02-Tue)).

**Esteban Stafford**, Universidad de Cantabria. **Borja Perez**, Universidad de Cantabria. **Jose Luis Bosque**, Universidad de Cantabria.

**Abstract**: Teaching computer architecture is challenging due to its abstract concepts and complexity. Visual learning tools help reinforce key ideas but often lack flexibility for direct architectural modifications. This work presents an enhanced visual simulation approach using Logisim Evolution, allowing students to implement and debug monocycle and pipelined RISC-V processors. New programmable components enable students to modify functionality dynamically, improving comprehension. The methodology has been successfully integrated into computer architecture courses, demonstrating effectiveness in laboratory assignments and exams. The results indicate that interactive visual tools significantly enhance learning outcomes for students and teaching efficiency for instructors.

[To page top](#summary) — [To posters at P2.3 (S2) on Tuesday 13](#P2.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### The Bicameral Cache: a split cache for RISC-V vector architectures

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.03-REBOLLEDO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.03-REBOLLEDO-abstract.pdf). Sub. \#30. Tuesday 13, at island 2.3 on S2. ([P2.3.03-Tue](#P2.3.03-Tue)).

**Susana Rebolledo**, Universidad de Cantabria. **Borja Perez**, Universidad de Cantabria. **Jose Luis Bosque**, Universidad de Cantabria. **Peter Hsu**, Peter Hsu Consulting.

**Abstract**: This paper presents the design and evaluation of the Bicameral Cache, a memory hierarchy for vector processors that separates scalar and vector references into distinct partitions. This design aims to enhance vector application performance by reducing scalar instruction interference and ensuring the continuity of vector elements. Additionally, a prefetching option is included to improve performance by exploiting spatial locality in vector references. The Cavatools simulator, supporting the RISC-V vector extension, was used for evaluation. Simulations of eight benchmark types across various architectural vector lengths show that the proposed cache significantly benefits sequential memory access patterns while having minimal impact on non-contiguous ones. Moreover, the prefetching feature consistently enhances performance.

[To page top](#summary) — [To posters at P2.3 (S2) on Tuesday 13](#P2.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### RISC-V ISA with In-Memory Co-Processing Architecture for General-Purpose Computing

Sub. \#75. Tuesday 13, at island 2.3 on S2. ([P2.3.04-Tue](#P2.3.04-Tue)).

**Tianyang Yu**, Nanjing University of Aeronautics and Astronautics. **Bi Wu**, Nanjing University of Aeronautics and Astronautics. **Kai Tian**, Nanjing University of Aeronautics and Astronautics. **Yijun Cui**, NUAA. **Weiqiang Liu**, Nanjing University of Aeronautics and Astronautics.

**Abstract**: Despite its compact characteristic that simplifies CPU’s complexity and reduces power consumption, RISC-V falls behind highly optimized ARM/x86-based CPUs at present, in terms of performance for general-purpose computing (GPC) tasks. In this paper, we propose to enhance the performance of RISC-V CPUs through in-memory computing (IMC) technology. Specifically, we employ the main memory based on non-volatile SOT-MRAM that supports IMC as a coprocessor to execute some operations in GPC tasks with high parallelism, while reducing data transfer overhead between memory and CPU.

[To page top](#summary) — [To posters at P2.3 (S2) on Tuesday 13](#P2.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### REPTILES: Repeated Tiles of Sargantana, a RISC-V multicore based on OpenPiton

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.06-OLIETE-ESCUÍN-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.06-OLIETE-ESCUÍN-abstract.pdf). Sub. \#120. Tuesday 13, at island 2.3 on S2. ([P2.3.06-Tue](#P2.3.06-Tue)).

**Noelia Oliete-Escuín**, BSC. **Arnau Bigas**, BSC. **Narcís Rodas**, BSC. **Albert Aguilera**, BSC. **Sajjad Ahmad**, BSC. **Jonathan Balkind**, UCSB. **Xavier Carril**, BSC. **Max Doblas**, BSC. **Ivan Díaz**, BSC. **Roger Figueras**, BSC. **Alireza Foroodnia**, BSC. **Cesar Fuguet**, INRIA. **Ignacio Genovese**, BSC. **Raúl Gilabert**, BSC. **Abbas Haghi**, BSC. **Alexander Kropotov**, BSC. **Neiel Leyva**, BSC. **Oscar Lostes-Cazorla**, UPC. **Lorién López-Villellas**, UZ. **Davy Million**, CEA. **Alireza Monemi**, BSC. **Sérik Pérez**, BSC. **Juan Antonio Rodríguez**, BSC. **Víctor Soria-Pardos**, BSC. **Behzad Salami**, BSC. **Francesc Moll**, BSC. **Oscar Palomar**, BSC. **Miquel Moretó**, BSC. **Lluc Alvarez**, BSC.

**Abstract**: Chip industry continues advancing and expanding modern computing systems, resulting in more complex multi-core processors. Conversely, academic projects face scalability challenges due to limited resources, highlighting the need for open-source frameworks that enable innovation and knowledge sharing. Recently, several open-source proposals have emerged, offering flexible and scalable designs, but fail to meet the performance demands of modern High-Performance Computing (HPC) applications. In this project, we present REPTILES, an open-source RISC-V multicore framework based on OpenPiton. REPTILES interconnects multiple Sargantana cores with the memory hierarchy of OpenPiton. Moreover, we present the new features incorporated in Sargantana and OpenPiton designs to improve the performance of HPC applications. We demonstrate that REPTILES presents suitable scalability, achieving a speedup of 3.1× on average with 4 cores. Additionally, we show that Sargantana’s new features increase the performance of vector addition benchmark in a 9.3×.

[To page top](#summary) — [To posters at P2.3 (S2) on Tuesday 13](#P2.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Virtual memory for real-time systems using hPMP

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.07-WALLUSZIK-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.07-WALLUSZIK-abstract.pdf). Sub. \#137. Tuesday 13, at island 2.3 on S2. ([P2.3.07-Tue](#P2.3.07-Tue)).

**Konrad Walluszik**, Infineon Technologies AG. **Daniel Auge**, Infineon Technologies AG. **Gerhard Wirrer**, Infineon Technologies AG. **Holm Rauchfuss**, Infineon Technologies AG. **Thomas Roecker**, Infineon Technologies AG.

**Abstract**: To satisfy automotive safety and security requirements, memory protection mechanisms are an essential component of automotive microcontrollers. In today’s available systems, either a fully physical address-based protection is implemented utilizing a memory protection unit, or a memory management unit takes care of memory protection while also mapping virtual addresses to physical addresses. The possibility to develop software using a large virtual address space, which is agnostic to the underlying physical address space, allows for easier software development and integration, especially in the context of virtualization. In this work, we showcase an extension to the current RISC-V SPMP proposal that enables address redirection for selected address regions, while maintaining the fully deterministic behavior of a memory protection unit.

[To page top](#summary) — [To posters at P2.3 (S2) on Tuesday 13](#P2.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Integration of a CGRA Accelerator with a CVA6 RISC-V Core for the Cloud-edge

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.08-GRANJA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P2.3.08-GRANJA-abstract.pdf). Sub. \#48. Tuesday 13, at island 2.3 on S2. ([P2.3.08-Tue](#P2.3.08-Tue)).

**Juan Granja**, Universidad Politécnica de Madrid. **Andres Otero**, Universidad Politecnica de Madrid.

**Abstract**: In the context of the development of adaptable nodes for the cloud-edge continuum, this work integrates a Coarse-Grain Reconfigurable Array (CGRA) accelerator with an application-class RISC-V processor on a System on Chip. To do so, a DMA interface is devised to provide the CGRA with its configuration data and to manage the transfer of input and output data between the CGRA and memory, all under the control of the RISC-V CPU via memory-mapped registers. The resulting platform is deployed on an FPGA, and its performance is evaluated when accelerating a set of relevant tasks, both in a bare-metal environment and under a Linux operating system. A kernel module is written for the latter, allowing the use of the CGRA accelerator from a Linux user process.

[To page top](#summary) — [To posters at P2.3 (S2) on Tuesday 13](#P2.3-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

On Tuesday 13, at island P3.1 (S3)

------------------------------------------------------------------------

### Toward industrial grade CHERI enhanced cores

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.1.01-JOANNOU-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.1.01-JOANNOU-abstract.pdf). Sub. \#92. Tuesday 13, at island 3.1 on S3. ([P3.1.01-Tue](#P3.1.01-Tue)).

**Alexandre Joannou**, University of Cambridge. **Jonathan Woodruff**, University of Cambridge. **Peter Rugg**, University of Cambridge. **Matthew Naylor**, University of Cambridge. **Franz Fuchs**, University of Cambridge. **Simon Moore**, University of Cambridge.

**Abstract**: CHERI-cap-lib is an RTL library implementing the core functionality necessary to extend CPU implementations with CHERI. We updated CHERI-cap-lib to the proposed ‘Zcheri‘ CHERI RISC-V standard. We also enrich CHERI-cap-lib with formal property verification using SymbiYosys and develop a flow for formal equivalence checking between SystemVerilog implementations and the mature Bluespec SystemVerilog implementation.

[To page top](#summary) — [To posters at P3.1 (S3) on Tuesday 13](#P3.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Towards an Industrial-Grade Open-Source FPU for RISC-V Vector Processors

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.1.02-MUSTAFA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.1.02-MUSTAFA-abstract.pdf). Sub. \#181. Tuesday 13, at island 3.1 on S3. ([P3.1.02-Tue](#P3.1.02-Tue)).

**Enis Mustafa**, Axelera AI. **Michael Platzer**, Axelera AI. **Domenic Wüthrich**, Axelera AI. **Florian Zaruba**, Axelera AI.

**Abstract**: Hardware floating-point units (FPUs) are crucial for HPC, ML, and embedded applications, yet no stand-alone RISC-V FPU fully supports vector extensions. We have enhanced CVFPU into a production-ready solution by optimizing timing and power (31% leakage reduction, up to 48% peak power savings), adding vfrec7/vfrsqrt7 and symmetrical widening adds, and improving verification by fixing seven bugs. These contributions make CVFPU a more viable choice for performance-critical applications while strengthening the overall open-source RISC-V ecosystem.

[To page top](#summary) — [To posters at P3.1 (S3) on Tuesday 13](#P3.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Monte Cimone v2: Down the Road of RISC-V High-Performance Computers

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.1.03-VENIERI-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.1.03-VENIERI-abstract.pdf). Sub. \#177. Tuesday 13, at island 3.1 on S3. ([P3.1.03-Tue](#P3.1.03-Tue)).

**Emanuele Venieri**, University of Bologna. **Simone Manoni**, University of Bologna. **Giacomo Madella**, University of Bologna. **Federico Ficarelli**, CINECA. **Daniele Gregori**, E4 Computer Engineering SpA. **Daniele Cesarini**, CINECA. **Luca Benini**, University of Bologna. **Andrea Bartolini**, University of Bologna.

**Abstract**: Many RISC-V platforms and SoCs have been announced in recent years targeting the HPC sector, but only a few of them are commercially available and engineered to fit the HPC requirements. The Monte Cimone project targeted assessing their capabilities and maturity, aiming to make RISC-V a competitive choice when building a datacenter. Nowadays, RV SoCs with vector extension, form factor and memory capacity suitable for HPC applications are available in the market, but it is unclear how compilers and open-source libraries can take advantage of its performance. In this paper, we describe the performance assessment of the upgrade of the Monte Cimone (MCv2) cluster with the Sophgo SG2042 processor’s HPC operations. The upgrade increases the attained node’s performance by 127x on HPL DP FLOP/s and 69x on Stream Memory Bandwidth.

[To page top](#summary) — [To posters at P3.1 (S3) on Tuesday 13](#P3.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### RISC-V for HPC: An update of where we are and main action points

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.1.04-BROWN-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.1.04-BROWN-abstract.pdf). Sub. \#223. Tuesday 13, at island 3.1 on S3. ([P3.1.04-Tue](#P3.1.04-Tue)).

**Nick Brown**, EPCC at the University of Edinburgh.

**Abstract**: This extended abstract is submitted on behalf of the RISC-V HPC SIG who have been undertaking an analysis to explore the current state and limitations of the RISC-V ecosystem for HPC. Whilst it is right to celebrate that there has been great progress made in recent years, we also highlight limitations and where effort should be focussed.

[To page top](#summary) — [To posters at P3.1 (S3) on Tuesday 13](#P3.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Evaluating SYCL Support on RISC-V Multicore Architectures: A First Approach

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.1.05-DE-LA-CALLE-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.1.05-DE-LA-CALLE-abstract.pdf). Sub. \#149. Tuesday 13, at island 3.1 on S3. ([P3.1.05-Tue](#P3.1.05-Tue)).

**Enrique de la Calle**, Fac. Informatica. Complutense University of Madrid. **Carlos Garcia**, Complutense University of Madrid.

**Abstract**: The increasing adoption of RISC-V architectures calls for the development of a robust parallel programming infrastructure. However, the feasibility of SYCL on RISC-V multicore systems remains largely unexplored. This ongoing study evaluates the compatibility and performance of multiple open-source SYCL implementations on RISC-V multicore architectures. Preliminary performance and compatibility testing using the SYCL-Bench suite showed that most benchmarks have been successfully executed on RISC-V multicore architectures.

[To page top](#summary) — [To posters at P3.1 (S3) on Tuesday 13](#P3.1-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

On Tuesday 13, at island P3.2 (S3)

------------------------------------------------------------------------

### How well does RISC-V Perform? Recent comparison data against other architectures

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.2.01-BENNETT-poster.pdf). Sub. \#158. Tuesday 13, at island 3.2 on S3. ([P3.2.01-Tue](#P3.2.01-Tue)).

**Jeremy Bennett**, Embecosm. **Craig Blackmore**, Embecosm. **Paolo Savini**, Embecosm. **Hugh O’Keeffe**, Ashling.

**Abstract**: RISC-V lives in a competitive market and must demonstrate its worth against competing architectures. In this talk we present the latest data comparing RISC-V performance to other architectures, particularly those from Arm, and Intel/AMD.

We consider 4 areas: i) the execution performance of application class cores; ii) the execution performance and code size of embedded cores; iii) the speed of simulators that are used to develop code pre-silicon; and iv) the performance of the open source communities maintaining and developing the tools used on RISC-V.

Within this context, we pay particular attention to the performance of the RISC-V Vector (RVV) ISA extension both on physical hardware and in simulation. We place results in a historical context, so that we can see how performance has changed over time, and what this might predict for the future.

[To page top](#summary) — [To posters at P3.2 (S3) on Tuesday 13](#P3.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Improving RISC-V TLB Shootdown Performance

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.2.02-DEPPE-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.2.02-DEPPE-abstract.pdf). Sub. \#211. Tuesday 13, at island 3.2 on S3. ([P3.2.02-Tue](#P3.2.02-Tue)).

**John Deppe**, The University of British Columbia. **Steven Yeung**, Andes Technology. **Guy Lemieux**, The University of British Columbia.

**Abstract**: Most popular ISAs have recently added new instructions to assist TLB shootdown, a software task performed by the OS to ensure that writes to the page table are seen by all address translation caches (TLBs). RISC-V currently uses a much slower traditional approach where TLB shootdown is done by broadcasting an inter-processor interrupt (IPI) to all affected harts. The sender of an IPI must stall until it collects acknowledgments from all target harts; each target hart is normally running some other software but it must take an exception to run a trap handler that evicts the specified TLB entry or entries and sends back an acknowledgment. In this early-stage research, we are reviewing the state-of-the-art in hardware and software techniques to accelerate TLB shootdown, and instrumenting the Linux kernel to help develop a new RISC-V mechanism that can accelerate remote TLB invalidations. The most promising techniques in research utilize a familiar hardware feature: cache coherence.

[To page top](#summary) — [To posters at P3.2 (S3) on Tuesday 13](#P3.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### A Deep Dive into Integration Methodologies in RISC-V

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.2.03-DOLMETA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.2.03-DOLMETA-abstract.pdf). Sub. \#59. Tuesday 13, at island 3.2 on S3. ([P3.2.03-Tue](#P3.2.03-Tue)).

**Alessandra Dolmeta**, Politecnico di Torino. **Valeria Piscopo**, Politecnico di Torino. **Maurizio Martina**, Politecnico di Torino. **Guido Masera**, Politecnico di Torino.

**Abstract**: The integration methodology can significantly affect the performance of dedicated accelerators. This work undertakes an exploration of this aspect, considering Keccak, a pivotal hashing standard in Post Quantum Cryptography (PQC), as a case of study. The paper presents three versions of KRONOS (Keccak RISC-V Optimized eNgine fOr haShing): a loosely-coupled memory-mapped accelerator, a tightly-coupled approach, and a coprocessor. The latter two versions leverage the CV-X-IF interface, with and without, respectively, an additional register file to store the Keccak state. Results show that the tightly approach is the most efficient integration method, achieving a balance between resource consumption and throughput.

[To page top](#summary) — [To posters at P3.2 (S3) on Tuesday 13](#P3.2-Tue) — [To all posters of Tuesday 13](#Tue)

------------------------------------------------------------------------

### Towards a Base-Station-on-Chip for 6G Networks: RISC-V Hardware Acceleration of the LOW PHY wireless communication kernels

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.2.04-ACEVEDO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-13-RISC-V-Summit-Europe-P3.2.04-ACEVEDO-abstract.pdf). Sub. \#228. Tuesday 13, at island 3.2 on S3. ([P3.2.04-Tue](#P3.2.04-Tue)).

**Javier Riccardo Acevedo**, TU Dresden. **Frank H. P. Fitzek**, TU Dresden.

**Abstract**: The current 5G and future 6G Generation of wireless communication systems will bring higher demands for computing capabilities and lower power consumption in the front end and processing ircuitry. Furthermore, the integration of AI/ML capabilities for network control will require a new hardware/software-codesign to accelerate both signal processing kernels and the computation of neural networks in a single chip. Therefore, the optimization of base band signal processing kernels in conjunction with powerful hardware architectures have a crucial role in the performance, latency and power consumption of the LOW PHY (Physical Layer). In this work, we explore how the kernels for channel estimation, beamforming, massive MIMO and FFT/iFFT can be efficiently implemented on a state-of-the-art RISC-V vector DSP (Digital Signal Processor) in order to exploit DLP (Data Level Parallelism). Furthermore, we explore how vector extensions (RVV) altogether with Custom Instructions on the RISC-V processor could be the correct approach in order to compute the LOW PHY algorithms, fulfilling throughput and latency requirements.

[To page top](#summary) — [To posters at P3.2 (S3) on Tuesday 13](#P3.2-Tue) — [To all posters of Tuesday 13](#Tue)

# Wednesday 14 Posters

Sorted by expo level, poster island, and stand.

------------------------------------------------------------------------

On Wednesday 14, at island P1.1 (S1)

------------------------------------------------------------------------

### Reliability in High-Performance Computing: Insights from a RISC-V Vector Processor

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.01-BARBIROTTA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.01-BARBIROTTA-abstract.pdf). Sub. \#102. Wednesday 14, at island 1.1 on S1. ([P1.1.01-Wed](#P1.1.01-Wed)).

**Marcello Barbirotta**, Sapienza University of Rome. **Francesco Minervini**, Barcelona Supercomputing Center. **Carlos Rojas Morales**, Barcelona Supercomputing Center. **Adrian Cristal**, Barcelona Supercomputing Center. **Osman Unsal**, Barcelona supercomputing center. **Mauro Olivieri**, Sapienza University of Rome.

**Abstract**: High-Performance Computing (HPC) systems are designed for large-scale processing and complex data analysis, utilizing scalability, efficiency, and parallelism, often with specialized hardware like Vector Processing Units (VPUs). RISC-V plays an interesting role in this context for its inherent extendability and the availability of open-source microarchitecture designs. Still, as these systems become more complex, their susceptibility to errors and failures poses significant challenges. Our research addresses this by implementing advanced fault tolerance techniques in the Vitruvius+ architecture, a partial out-of-order RISC-V VPU. Notably, we present the first full RTL-level implementation of instruction replication in an HPC-class vector processor for reliability. We explore redundancy mechanisms in critical architectural units, achieving a 75\\ reduction in non-silent faults leading to system failure, supported by extensive fault injection simulations, with only a 7.5\\ hardware overhead and minimal clock frequency variation.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### CVA6 RISC-V PMP Vulnerabilities against FIA

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.02-QUENEHERVE-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.02-QUENEHERVE-abstract.pdf). Sub. \#7. Wednesday 14, at island 1.1 on S1. ([P1.1.02-Wed](#P1.1.02-Wed)).

**Kevin KQ QUENEHERVE**, Université Bretagne Sud - Lab-STICC**, UMR 6285.. \*\*Philippe PT TANGUY**, Université Bretagne Sud - Lab-STICC**, UMR 6285.. \*\*Rachid RD DAFALI**, DGA MI. **Vianney VL LAPÔTRE**, Université Bretagne Sud - Lab-STICC\*\*, UMR 6285..

**Abstract**: Fault Injection Attacks (FIA) present a considerable threat to the security and reliability of embedded systems. FIAs can compromise an embedded processor by altering its clock signal, power supply or by using electromagnetic pulses. This study focuses on analyzing the impact of FIA on the Physical Memory Protection (PMP) configuration flow within a CVA6 RISC-V core. We conducted fault injection campaigns on an FPGA implementation using an ARTY A7-100T board to characterize the resulting fault effects.  
To achieve this, we utilized clock glitches as the primary method of fault injection.  
Our experimental findings reveal that FIAs can induce various effects on PMP configuration registers.  
By categorizing these effects according to the injection parameters, we demonstrate that specific effects can be reliably achieved under varying injection conditions, often with a high probability of success for an attacker.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### AIA User Priority Mask Extension: Minimizing Critical Sections Side-Effects on Real-Time Automotive Systems

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.03-PINTO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.03-PINTO-abstract.pdf). Sub. \#175. Wednesday 14, at island 1.1 on S1. ([P1.1.03-Wed](#P1.1.03-Wed)).

**Sandro Pinto**, University of Minho. **Thomas Roecker**, Infineon.

**Abstract**: Critical sections are widely used in many real-time automotive scenarios; however, if not adequately supported at the ISA level, it can lead to unintended performance overhead, which studies within the AUTOSAR community point to nearly 30% CPU-load. In this work, we advocate that the RISC-V ISA (and related specifications) cannot efficiently support critical sections for real-time automotive systems. To address that, we propose a novel AIA extension. We implemented the proposed extension on a CVA6-based SoC endowed with an Advanced Interrupt Architecture (AIA) IP and functionally validated the intended behavior. We are now collecting empirical evidence to support the discussion of the current proposal at RISC-V International. We are going to open-source all artifacts to promote collaboration within the RISC-V community.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### A Safe and Secure Platform for Autonomous Driving

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.04-KOSMIDIS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.04-KOSMIDIS-abstract.pdf). Sub. \#182. Wednesday 14, at island 1.1 on S1. ([P1.1.04-Wed](#P1.1.04-Wed)).

**Leonidas Kosmidis**, Barcelona Supercomputing Center**, BSC. and Universitat PolitÃ¨cnica de Catalunya**, UPC.. **Eric Rufart Blasco**, Universitat Politècnica de Catalunya**, UPC. and Barcelona Supercomputing Center**, BSC.. **Jannis Wolf**, Barcelona Supercomputing Center. **Guillermo Vidal**, Universitat Politècnica de Catalunya**, UPC. and Barcelona Supercomputing Center**, BSC.. **Marc Solé Bonet**, Barcelona Supercomputing Center**, BSC.. \*\*Juan Carlos Rodriguez**, Barcelona Supercomputing Center**, BSC.. \*\*Matina Maria Trompouki**, Barcelona Supercomputing Center**, BSC.. \*\*Sergi Alcaide**, Barcelona Supercomputing Center**, BSC.. \*\*Jeremy Jens Giesen León**, Barcelona Supercomputing Center and Universitat Politècnica de Catalunya.

**Abstract**: In the context of the SMARTY EU project, at BSC we develop a safe and secure RISC-V platform for autonomous driving. The developed System-on-Chip platform is similar to existing MPSoC-GPU architectures for high performance automotive systems, consisting of Safety, Application, GPU and security IPs.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Real-Time Extension to the RISC-V Advanced Interrupt Architecture

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.05-KHOMICH-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.05-KHOMICH-abstract.pdf). Sub. \#206. Wednesday 14, at island 1.1 on S1. ([P1.1.05-Wed](#P1.1.05-Wed)).

**Alexey Khomich**, Synopsys Inc. **Evgenii Paltsev**, Synopsys. **Paul Stravers**, Synopsys Inc.

**Abstract**: The Real-Time Interrupt Architecture (RTIA) is the evolution of RISC-V Advanced Interrupt Architecture (AIA) targeted to extend use cases to real-time latency critical scenarios and/or to resource constrained designs. The RTIA defines necessary mechanisms for interrupt nesting and low latency fixed overhead interrupt handling. Keeping compatibility with RISC-V Privileged ISA and RISC-V AIA, the RTIA provides the same programming model for light weight embedded applications and heavy feature rich systems allowing mixing it in virtual environments.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Designing a RISC-V Platform for the HIGHER project based on current and upcoming extensions

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.06-MARAZAKIS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.06-MARAZAKIS-abstract.pdf). Sub. \#127. Wednesday 14, at island 1.1 on S1. ([P1.1.06-Wed](#P1.1.06-Wed)).

**Manolis Marazakis**, FORTH. **Nick Kossifidis**, FORTH.

**Abstract**: The demand for secure and modular server architectures is driving interest in RISC-V as a foundation for scalable cloud and edge computing, based on open standards. In the context of the HIGHER project, an initiative focused on developing open-source, high-density rack-scale systems for cloud and edge services, this presentation introduces a reference design for RISC-V-based server platforms designed for Open Compute Project (OCP) compatibility, structured around two distinct security domains to enforce strong system integrity and workload: System Management and Main CPU Cluster. By leveraging recently ratified non-ISA RISC-V extensions, the Caliptra root-of-trust open-source module, and upcoming architectural advancements, we explore key security and system features, including memory isolation, confidential computing, and hardware-backed attestation, ensuring trustworthy functionality for managing, securing, and controlling modular server infrastructures. The isolation mechanisms recently introduced in RISC-V standards and incorporated in this reference design are of broad applicability, fitting also the automotive, mobile, and desktop environments.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Reliable Hardware Trojan Formal Verification

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.07-CHUAH-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.07-CHUAH-abstract.pdf). Sub. \#58. Wednesday 14, at island 1.1 on S1. ([P1.1.07-Wed](#P1.1.07-Wed)).

**Czea Sie Chuah**, Technical University of Munich. **Christian Appold**, DENSO AUTOMOTIVE Deutschland GmbH. **Tim Leinmüller**, DENSO AUTOMOTIVE Deutschland GmbH.

**Abstract**: Due to cost and time reasons, hardware development is currently often done using IP of external vendors and outsourcing of fabrication to third parties. The globalization of the hardware supply chain, which is inherent in the RISC-V ecosystem, increases the risk of malicious insertions of Hardware Trojans (HTs) into the design. HTs are malicious modifications of hardware to change functionality or to leak secret data. Especially in safety- and security-critical areas like autonomous driving, HTs can cause severe consequences and endanger even human lives. We research how model checking based formal verification can be used in a systematic way to detect each HT inserted during hardware design reliably. We are the first to use signal connection properties on top of design functionality properties for more reliable HT detection. To reduce verification time and strongly increase HT detection coverage, we developed a tool to generate a high number of properties fully automatically. Additionally, we will publish a large set of specification and microarchitecture intent derived properties important for HT detection in processors and show how these properties have to be combined with connection properties for HT detection. Our work results in a guideline for reliable HT detection in processors using formal verification.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### A Fine-Grained Dynamic Partitioning Against Cache-Based Timing Attacks via Cache Locking

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.08-GAUDIN-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.08-GAUDIN-abstract.pdf). Sub. \#43. Wednesday 14, at island 1.1 on S1. ([P1.1.08-Wed](#P1.1.08-Wed)).

**Nicolas Gaudin**, Univ. Bretagne Sud, UMR CNRS 6285, Lab-STICC. **Jeremy Guillaume**, UBS. **Pascal Cotret**, ENSTA Bretagne / Lab-STICC. **Guy Gogniat**, Université Bretagne Sud. **Vianney Lapotre**, Univ. Bretagne Sud, UMR CNRS 6285, Lab-STICC.

**Abstract**: Cache-based timing side-channel attacks represent a security threat for both high-end and embedded processors. As countermeasure to these attacks, previous works intoduced the lock and unlock instructions allowing a program to ensure constant-time accesses to cache. However, their implementation was still subject to cache-based attacks. In this paper, we propose a new implementation of these instructions, and experimentally demonstrate that our proposed solution defeats contention-based cache side-channel attacks such as Prime+Probe, while leading to a low impact on area overhead and performance efficiency of processes.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Side-channel attack hardware detection module added to RISC-V core

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.09-POTTIER-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.09-POTTIER-abstract.pdf). Sub. \#100. Wednesday 14, at island 1.1 on S1. ([P1.1.09-Wed](#P1.1.09-Wed)).

**Juliette Pottier**, Nantes Université-IETR. **Bertrand Le Gal**, Université de Rennes, IRISA/INRIA lab.. **Maria Mendez Real**, Lab-STICC CNRS UMR 6285. **Sebastien Pillement**, Polytech Nantes - IETR.

**Abstract**: Processor performance optimizations such as Out-of-Order or speculative execution are known to be exploited by attackers for malicious purposes. Numerous side-channel attacks have been developed over decades and more recently transient attacks are considered as serious threats. As a countermeasure, previous works offered detection methods monitoring hardware performance counters (HPC). In this work we propose to take advantage of dynamic instructions insertion to monitor HPCs and detect side-channel attacks. This approach offers flexibility as it allows to dynamically adapt the events monitored by HPCs to the state of the system. We present our light-weight hardware micro-decoding unit used to insert monitoring instructions in the execution flow of a RISC-V core and detect side-channel attacks.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### A RISC-V based accelerator for Post Quantum Cryptography

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.10-SURESH-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.10-SURESH-abstract.pdf). Sub. \#112. Wednesday 14, at island 1.1 on S1. ([P1.1.10-Wed](#P1.1.10-Wed)).

**Ambily Suresh**, Silicon Austria Labs. **Andrew Wilson**, Silicon Austria Labs. **Diego Gigena-Ivanovich**, Silicon Austria Labs. **Manuel Freiberger**, Silicon Austria Labs. **Willibald Krenn**, Silicon Austria Labs.

**Abstract**: Post-Quantum Cryptography (PQC) is a topic of increased interest in the past decade, both with regards to the cryptosystem definition and the hardware and software implementations to perform at optimum efficiency. We present our ongoing work on the implementation of RISC-V based accelerators for PQC algorithms, in particular the Classic McEliece Key Encapsulation Mechanism. Our system includes a PQC accelerator and an Open-HW Group CVA-6 core along with a PQC-specific instruction set. This presentation describes the architecture, performance estimates, and demonstration plans in the future.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### CIAMH : Confidentiality, Integrity and Authentication across the Memory Hierarchy

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.11-AIT-LAHSSAINE-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.11-AIT-LAHSSAINE-abstract.pdf). Sub. \#131. Wednesday 14, at island 1.1 on S1. ([P1.1.11-Wed](#P1.1.11-Wed)).

**KARIM AIT LAHSSAINE**, CEA-LETI. **Olivier Savry**, CEA LETI.

**Abstract**: In this paper, we propose CIAMH, a hardware countermeasure that ensures the confidentiality, integrity and authenticity of data from DRAM to CPU registers, via L1D and L1I cache memories. Data confidentiality is ensured through encryption in DRAM and masking in caches. Integrity is guaranteed by associating integrity tags with data and by checking these tags at each level of the hierarchy to detect data corruption. The authentication of data is facilitated by authenticated encryption in DRAM and by the presence of integrity tags that are dependent on a unique key. These mechanisms have been designed to mitigate attacks such as RowHammer, fault injection and side-channel attacks throughout the memory hierarchy. The CIAMH has been implemented in relation to the NaxRiscv core, thus enabling it to be modular for the user. The RTL generated can easily incorporate part or all of the countermeasure, depending on the specific use case.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Advancing Confidential Computing on RISC-V with the Memory Protection Table

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.12-MERCOGLIANO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.1.12-MERCOGLIANO-abstract.pdf). Sub. \#141. Wednesday 14, at island 1.1 on S1. ([P1.1.12-Wed](#P1.1.12-Wed)).

**Stefano Mercogliano**, University of Naples Federico II. **Valerio Di Domenico**, University of Naples Federico II. **Alessandro Cilardo**, University of Naples Federico II.

**Abstract**: Cloud computing presents significant security challenges, especially in multi-tenant environments where ensuring data confidentiality and integrity is crucial. To address this, commercial architectures like Intel SGX, AMD SEV, and ARM TrustZone have introduced Confidential Virtual Machine (CVM) technologies to enable trusted execution. Similarly, RISC-V is developing its own confidential computing framework, the Confidential Virtualization Extension (CoVE). To accelerate the growth of a trusted computing ecosystem on RISC-V, we introduce an open-source implementation of the Memory Protection Table (MPT); a key hardware component that enforces secure supervisor domain isolation. Designed as a stand-alone module, the MPT has been tested both in isolation and integrated into the CVA6 processor’s MMU.

[To page top](#summary) — [To posters at P1.1 (S1) on Wednesday 14](#P1.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

On Wednesday 14, at island P1.2 (S1)

------------------------------------------------------------------------

### Evaluation of Optimized PQC Standards ML-KEM and ML-DSA on Sargantana RV64GBV core

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.2.01-CARRIL-GIL-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.2.01-CARRIL-GIL-abstract.pdf). Sub. \#152. Wednesday 14, at island 1.2 on S1. ([P1.2.01-Wed](#P1.2.01-Wed)).

**Xavier Carril Gil**, Barcelona Supercomputing Center. **Emanuele Parisi**, Barcelona Supercomputing Center. **Narcís Rodas Quiroga**, Barcelona Supercomputing Center. **Raúl Gilabert Gámez**, Barcelona Supercomputing Center. **Juan Antonio Rodríguez Gracia**, Barcelona Supercomputing Center. **Oriol Farràs Ventura**, Universitat Rovira i Virgili. **Miquel Moreto**, BSC.

**Abstract**: The advent of quantum computing threatens the security of traditional cryptographic schemes, making the development of post-quantum algorithms crucial. The Module Lattice Key Encapsulation Mechanisms (ML-KEM) and the Digital Signature Algorithm (ML-DSA) are the two main NIST standards. This work addresses the acceleration of ML-KEM and ML-DSA on the Sargantana RV64GBV core using the standard bit manipulation (B) and vector (V) extensions. We compare the performance of the reference implementations with a recently proposed version in which the most computationally intensive operations of module lattice cryptography are optimized through carefully crafted assembly routines. In addition, we compare the hand-optimized vectorized speedup with the performance of code produced by a recent RISC-V compiler through auto-vectorization and insertion of bit manipulation operations. Our results demonstrate that standard BV extensions significantly improve performance, providing speedups ranging from 3.18× to 4.59× for ML-KEM and ML-DSA. With hand-tuned assembly routines, RV64 cores lacking BV extensions can achieve up to 3.29× speedup over the reference implementation. Lastly, compiler-emitted code lags behind hand-optimized kernels, with auto-bit manipulation showing better results than auto-vectorization in accelerating these schemes.

[To page top](#summary) — [To posters at P1.2 (S1) on Wednesday 14](#P1.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### RISC-V MPU - Address Space Isolation for Latency Critical and/or Resource Constrained Systems

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.2.02-KHOMICH-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.2.02-KHOMICH-abstract.pdf). Sub. \#209. Wednesday 14, at island 1.2 on S1. ([P1.2.02-Wed](#P1.2.02-Wed)).

**Alexey Khomich**, Synopsys Inc. **Nigel Topham**, Synopsys Inc. **Paul Stravers**, Synopsys Inc.

**Abstract**: The Memory Protection Unit (MPU) provides efficient address protection and address translation capabilities for RISC-V cores. It is designed to replace a traditional MMU in resource constrained and/or latency critical systems. The MPU allows multiple stages of operation required for virtualization use cases and compatibility with the RISC-V Hypervisor Extension. Efficient operation is achieved by replacing the memory-based address translation table of an MMU with core local configuration storage allowing flexible definition of memory region boundaries and fixed, low-latency address lookup.

[To page top](#summary) — [To posters at P1.2 (S1) on Wednesday 14](#P1.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Agile Formal Verification with Symbolic Quick Error Detection by Semantically Equivalent Program Execution

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.2.03-LI-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.2.03-LI-abstract.pdf). Sub. \#3. Wednesday 14, at island 1.2 on S1. ([P1.2.03-Wed](#P1.2.03-Wed)).

**Yufeng Li**, Institute of Computing Technology, Chinese Academy of Sciences. **Qiusong Yang**, Institute of Software, Chinese Academy of Sciences. **Yiwei Ci**, Institute of Software, Chinese Academy of Sciences. **Enyuan Tian**, Institute of Software, Chinese Academy of Sciences. **Yungang Bao**, Institute of Computing Technology, Chinese Academy of Sciences. **Kan Shi**, Institute of Computing Technology, Chinese Academy of Sciences.

**Abstract**: As processor complexity continues to grow and development cycles shorten, agile development becomes essential. Formal verification ensures design correctness but is labor-intensive and error-prone due to design-specific properties. Symbolic Quick Error Detection (SQED) avoids manually writing many properties by checking the design-independent, self-consistency universal property, thereby facilitating agile verification. However, since self-consistency is based on assertions that expect the processor to produce consistent results between the original and duplicate instructions, it fails to cover bugs that affect both the original and duplicate instructions, leading to false positives. To address this, we propose Symbolic Quick Error Detection by Semantically Equivalent Program Execution (SEPE-SQED), which utilizes program synthesis to find programs (instruction sequences) with equivalent meanings to original instructions. SEPE-SQED effectively detects the bugs missed by SQED by differentiating their impact on the original instruction and its semantically equivalent program. In the case study of a RISC-V processor, agile formal verification can improve productivity by approximately 60 times compared to conventional Formal Property Verification (FPV).

[To page top](#summary) — [To posters at P1.2 (S1) on Wednesday 14](#P1.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Poster: RISC-V system prototyping in the RISER project

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.2.04-MARAZAKIS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.2.04-MARAZAKIS-abstract.pdf). Sub. \#179. Wednesday 14, at island 1.2 on S1. ([P1.2.04-Wed](#P1.2.04-Wed)).

**Manolis Marazakis**, FORTH.

**Abstract**: Can we design and build data-center system platforms based on open standards in Europe today? This poster will outline the experiences and roadmap of an ongoing research and innovation project that has taken up this challenge. RISER (started in Jan’23) is progressing towards a first-generation of all-European RISC-V cloud accelerator and cloud server stand-alone prototypes, operating with fully-featured operating systems and runtimes. Building on top of outcomes from the EPI and EUPILOT projects, RISER aims to develop the first all-European RISC-V cloud server infrastructure, aiming to enhance Europe’s open strategic autonomy. This poster will summarize the progress of prototyping effort by the project consortium.

[To page top](#summary) — [To posters at P1.2 (S1) on Wednesday 14](#P1.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

On Wednesday 14, at island P1.3 (S1)

------------------------------------------------------------------------

### An interleaved multi-thread RISC-V design for SMP with dual core lockstep to support ASIL-D functional safety requirements

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.01-WEI-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.01-WEI-abstract.pdf). Sub. \#28. Wednesday 14, at island 1.3 on S1. ([P1.3.01-Wed](#P1.3.01-Wed)).

**Jian Wei**, ecarx. **yixuan zhao**, ecarx.

**Abstract**: We design an interleaved two-thread RISC-V, which deliver much higher performance efficiency with smaller silicon area and consuming much less power, to support SMP with lock step functional safety. This work is certified by Exdia to qualify ASIL-D requirements. This design is implemented inside an automotive MCU product. We further extend this interleaved multi-thread design to support advanced operating system, with more flexible functional safety requirements

[To page top](#summary) — [To posters at P1.3 (S1) on Wednesday 14](#P1.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Tackling Hardware Trojan Horses via Hardware-based Methodologies

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.02-PALUMBO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.02-PALUMBO-abstract.pdf). Sub. \#33. Wednesday 14, at island 1.3 on S1. ([P1.3.02-Wed](#P1.3.02-Wed)).

**Alessandro Palumbo**, CentraleSupÃ©lec, Inria, CNRS, IRISA.

**Abstract**: Hardware Trojan Horses represent significant challenges to the security and reliability of modern microprocessor-based systems. This manuscript introduces two complementary approaches to enhance hardware security. First, programmable Hardware Security Modules are proposed to detect Hardware Trojan Horses by monitoring instruction-fetch activities, identifying malicious interferences, and preventing software-exploitable Hardware Trojan Horse activations. Second, a methodology based on side-channel analysis is proposed to verify the integrity of FPGA bitstreams, allowing the identification of tampered configurations through the extraction and classification of both high- and low-level features.

[To page top](#summary) — [To posters at P1.3 (S1) on Wednesday 14](#P1.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Detecting Microarchitectural Side-Channel Attacks via Hardware Security Checkers

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.03-PALUMBO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.03-PALUMBO-abstract.pdf). Sub. \#36. Wednesday 14, at island 1.3 on S1. ([P1.3.03-Wed](#P1.3.03-Wed)).

**Alessandro Palumbo**, CentraleSupÃ©lec, Inria, CNRS, IRISA.

**Abstract**: Microarchitectural Side-Channel Attacks represent significant challenges to the security and reliability of modern microprocessor-based systems. This manuscript introduces an approach to enhance hardware security. A programmable Hardware Security Checker is proposed to detect Microarchitectural Side-Channel Attacks by employing hash functions and Machine Learning algorithms to analyze runtime features, such as performance counters, enabling the real-time detection of attack patterns.

[To page top](#summary) — [To posters at P1.3 (S1) on Wednesday 14](#P1.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### RISC-V Architectural Functional Verification

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.04-HARRIS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.04-HARRIS-abstract.pdf). Sub. \#80. Wednesday 14, at island 1.3 on S1. ([P1.3.04-Wed](#P1.3.04-Wed)).

**David Harris**, Harvey Mudd College. **Jordan Carlin**, Harvey Mudd College. **Corey Hickson**, Harvey Mudd College. **Larry Lapides**, Synopsys. **Lee Moore**, Synopsys. **Huda Sajjad**, 10xEngineers. **Umer Shahid**, 10xEngineers. **Aimee Sutton**, Synopsys. **Mike Thompson**, OpenHW Foundation. **Rose Thompson**, Oklahoma State University. **Muhammad Zain**, UET.

**Abstract**: This work describes a comprehensive open functional verification suite for RVA22S64. The tests run on a Device Under Test (DUT) communicating with the ImperasDV reference model via the RISC-V Verification Interface (RVVI). The testbench collects functional coverage while the reference model checks that the DUT demonstrates correct behavior Lockstep eliminates the burden of generating signatures and the risk of incomplete signatures. The suite contains manually-written privileged coverpoints for virtual memory, CSRs, traps, and PMP as well as automatically-generated coverpoints for all unprivileged instructions.

[To page top](#summary) — [To posters at P1.3 (S1) on Wednesday 14](#P1.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Exploring the Security of an Accelerator integrated with Core-V eXtention InterFace (CV-X-IF)

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.05-DOLMETA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.05-DOLMETA-abstract.pdf). Sub. \#85. Wednesday 14, at island 1.3 on S1. ([P1.3.05-Wed](#P1.3.05-Wed)).

**Alessandra Dolmeta**, Politecnico di Torino. **Davide Bellizia**, Telsy. **Guido Masera**, Politecnico di Torino. **Maurizio Martina**, Politecnico di Torino. **Behnam Farnaghinejad**, Politecnico di Torino. **Ernesto Sanchez**, Politecnico di Torino.

**Abstract**: The adoption of hardware accelerators in embedded systems enhances performance but raises security concerns, particularly regarding side-channel leakage. The Core-V eXtension Interface (CV-X-IF) simplifies accelerator integration in RISC-V, yet its security remains unexplored. This study presents the first side-channel analysis of CV-X-IF, comparing a native XOR instruction to a custom accelerator using Test Vector Leakage Assessment (TVLA). Power trace analysis reveals measurable differences, highlighting potential vulnerabilities. These findings underscore the need for secure accelerator design in RISC-V microcontrollers.

[To page top](#summary) — [To posters at P1.3 (S1) on Wednesday 14](#P1.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Microarchitectural signals analysis platform for the implementation of Hardware Security Counters

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.06-GEORGET-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.06-GEORGET-abstract.pdf). Sub. \#134. Wednesday 14, at island 1.3 on S1. ([P1.3.06-Wed](#P1.3.06-Wed)).

**Lucas Georget**, EDF R&D / LAAS-CNRS. **Vincent Migliore**, LAAS-CNRS. **Vincent Nicomette**, LAAS-CNRS. **Frédéric Silvi**, EDF R&D. **Arthur Villard**, EDF R&D.

**Abstract**: Detecting malicious software or hardware behavior during the operation of a computer system requires observables from one or more abstraction layers of the system. This abstraction, however, tends to limit the ability to detect behavioral deviations, especially for attack classes that exploit vulnerabilities very close to the target hardware. Conversely, too low a level of abstraction tends to significantly increase the complexity of the system model, and therefore poses a number of difficulties for the extraction and selection of relevant observables for a given class of attack.

Hardware performance counters in particular have been used as an indirect means of observing micro-architecture behavior and detecting software attempting to exploit hardware vulnerabilities. In order to improve the various detection methods, we propose the construction of hardware metrics designed from the outset for security, by studying the correlation between signals from the micro-architecture and the various classes of attack in the literature, targeting both conventional IT and industrial OT systems. By extension, this work aims to detect attacks originating from hardware Trojans, the latter having the effect of changing the behavior of a given micro-architecture.

[To page top](#summary) — [To posters at P1.3 (S1) on Wednesday 14](#P1.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### A Hardware-Based Cache Side Channel Attack Detection Mechanism for RISC-V Processors

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.07-BROKALAKIS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.07-BROKALAKIS-abstract.pdf). Sub. \#164. Wednesday 14, at island 1.3 on S1. ([P1.3.07-Wed](#P1.3.07-Wed)).

**Andreas Brokalakis**, Technical University of Crete. **Alexandros Skyvalos**, Technical University of Crete. **Ioannis Papaefstathiou**, Exascale Performance Systems.

**Abstract**: Side-channel attacks rely on information that can be gathered (or leaked) by the fundamental way a computer system operates. For CPU-based systems, a prominent number of these attacks target the caches aiming at gaining unauthorised access to sensitive data. Proposed solutions provide limited remedies and come at great costs, especially associated with the difficulty to reliably identify such attacks. In this work, we analyse cache-based side channel attacks on RISC-V processors and demonstrate that they all depend on accessing specific architectural registers to successfully complete. We present a detection mechanism implemented at the hardware level that is able to detect all such attacks, without producing false negative detections and without requiring any software assistance or modifications.

[To page top](#summary) — [To posters at P1.3 (S1) on Wednesday 14](#P1.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Comparing Voltage and Clock Glitch Attacks on a RISC-V implementation on FPGA

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.08-BOULIFA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.08-BOULIFA-abstract.pdf). Sub. \#184. Wednesday 14, at island 1.3 on S1. ([P1.3.08-Wed](#P1.3.08-Wed)).

**Roua Boulifa**, TIMA. **Giorgio Di Natale**, TIMA - CNRS. **Paolo Maistri**, TIMA Laboratory.

**Abstract**: Embedded systems are ubiquitous to our daily lives, making them attractive targets for malicious actors. Ensuring their security is crucial. One significant threat is fault injection attacks on microprocessors. Understanding how these attacks affect a system’s internal design is essential for assessing their overall security impact. In this paper, voltage glitch and clock glitch campaigns have been carried out on RISC-V processor that is used by researcher community and start to gain popularity in embedded system market. As a result, we provide comprehensive analysis for the glitch set up. We show that some of these models are applicable to both glitch methods. The presented fault models enable better understating of the fault injection effects, and thus, easing the process of analyzing vulnerabilities, and developing cost-effective countermeasures against fault attacks.

[To page top](#summary) — [To posters at P1.3 (S1) on Wednesday 14](#P1.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### SCAR: Selective Cache Address Remapping for Mitigating Cache Side-Channel Attacks

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.09-BHADE-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.09-BHADE-abstract.pdf). Sub. \#201. Wednesday 14, at island 1.3 on S1. ([P1.3.09-Wed](#P1.3.09-Wed)).

**Pavitra Prakash Bhade**, Indian Institute of Technology. **Olivier Sentieys**, INRIA. **Sharad Sinha**, Indian Institute of Technology\*\*, IIT. Goa.

**Abstract**: Cache side channel attacks (CSCA) that exploit cache conflicts pose a significant threat to the security of shared caches. To counter these attacks, cache designs incorporating cache randomization have emerged as a highly effective solution. However, these techniques rely on address remapping for all instructions, thus introducing performance drawbacks and risks of breaking remapping within the rekeying interval. We propose a novel cache architecture and control mechanism called SCAR that performs selective remapping of instructions, thus enhancing security while minimizing performance overhead. SCAR uses modified cache search and replacement algorithms, along with minimal addition to the cache hardware architecture.

[To page top](#summary) — [To posters at P1.3 (S1) on Wednesday 14](#P1.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Pre-silicon Security Analysis of\\ RISC-V Processors to Fault Injection Attacks

[Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.3.10-COUROUSSÉ-abstract.pdf). Sub. \#214. Wednesday 14, at island 1.3 on S1. ([P1.3.10-Wed](#P1.3.10-Wed)).

**Damien Couroussé**, Univ. Grenoble Alpes, CEA, LIST. **Mathieu Jan**, CEA LIST.

**Abstract**: This talk proposal showcases the sensitivity of processor microarchitectures to fault injection attacks, which threat hardware and software security. As a consequence, security analysis must take into account both the hardware and software models of system under analysis. Furthermore, fault injection requires to consider exhaustively all the possible injection locations, resulting in unprecedented complexity. We present our methodology and two tools developed for this purpose.  
In particular, our approach has enabled us to identify a new vulnerability in the OpenTitan secure core.

[To page top](#summary) — [To posters at P1.3 (S1) on Wednesday 14](#P1.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

On Wednesday 14, at island P1.4 (S1)

------------------------------------------------------------------------

### Call Rewinding Towards RISC-V Specification

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.4.01-BITON-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.4.01-BITON-abstract.pdf). Sub. \#226. Wednesday 14, at island 1.4 on S1. ([P1.4.01-Wed](#P1.4.01-Wed)).

**Téo Biton**, Thales cortAIx Labs. **Olivier Gilles**, Thales cortAIx Labs. **Daniel Gracia Pérez**, Thales cortAIx Labs. **Nikolai Kosmatov**, Thales cortAIx Labs. **Sébastien Pillement**, Nantes Université.

**Abstract**: Memory vulnerabilities are still being exploited today to perform code-reuse attacks by overwriting the return address. Recently, call rewinding has been introduced as a security countermeasure to mitigate this type of abuse, placing itself on the same perimeter as the Zcfiss extension. We propose a thorough comparison of call rewinding with the Zcfiss extension and discuss on its viability for adoption in industrial systems.

[To page top](#summary) — [To posters at P1.4 (S1) on Wednesday 14](#P1.4-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### RISC-V CoVE implementation in priviliged firmware

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.4.02-XIAOXIA-poster.pdf). Sub. \#15. Wednesday 14, at island 1.4 on S1. ([P1.4.02-Wed](#P1.4.02-Wed)).

**Cui Xiaoxia**, Alibaba.

**Abstract**: As similiar to ARM’s security monitor and Intel’s TDX module firmware to have control of Trusted VMs in confidential computing platform, RISC-V also provides a type of privileged firmware runing in highest Machine privilege mode, as refered to RDSM. This presentation primparily introduces all security implementation required in RISC-V CoVE specification, especially those security premitives defined in SoC level. Aim to be top security level, we have a built-in RoT with security sub-system which can offer security volatile memory to store CoVE measurement used in platform remote attesation and save local attestation certificate for TSM vendor as choice. To enhance speed in bootstrap, it provides a new cryptographic library which is optimized by using RISC-V cryptographic vector instructions. Those optimized algorithms can be used to authenticate firmware image and entity measurememt. To support management lifecycle of TVM, it needs to handle TEE ecall from Host OS/VMM or TSM and response in asynchronously. We extend a new ECALL type dedicated for CoVE. Most requests must be delivered forward to opposite OS to handle, which result in supervisor domain context switch sequently. Except to save/restore supervisor domain context, it also enforces to update MTT table before execution next. Take note that the MTT driver and other security primitive is programmed by RUST language which is popular recent years. To better utilize MTT memory, we import new memory management alogrithms for MTT memory allocation. For server platform, we might support other functionality which shall stay in machine mode to be alive at runtime, such as RAS/SCP service and other runtime service from UEFI BIOS.

[To page top](#summary) — [To posters at P1.4 (S1) on Wednesday 14](#P1.4-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Comprehensive Verification of the RISC-V Memory Management Unit: Challenges and Solutions

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.4.03-SAJJAD-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P1.4.03-SAJJAD-abstract.pdf). Sub. \#108. Wednesday 14, at island 1.4 on S1. ([P1.4.03-Wed](#P1.4.03-Wed)).

**Huda Sajjad**, 10xEngineers. **Muhammad Hammad Bashir**, Verification Engineer. **Yazan Hussnain**, 10xEngineers. **Fatima Saleem**, 10xEngineers.

**Abstract**: The Memory Management Unit (MMU), critical for virtual memory translation and protection, demands rigorous verification due to its inherent complexity. This work details a two-step methodology to ensure MMU compliance with RISC-V Privileged ISA specification. First, a test suite was developed using the RISCOF framework, leveraging RISC-V ISAC for coverage analysis. Second, the suite was executed on the OpenHW Core-V Wally processor, employing ImperasDV as a reference model and riscvISACOV for functional coverage development. This approach identified a critical architectural bug in Core-V Wally’s MMU implementation, demonstrating the methodology’s effectiveness in validating memory management units.

[To page top](#summary) — [To posters at P1.4 (S1) on Wednesday 14](#P1.4-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Vyond: Flexible and Rapid WorldGuard-Based Security Prototyping using Chipyard

Sub. \#27. Wednesday 14, at island 1.4 on S1. ([P1.4.04-Wed](#P1.4.04-Wed)).

**Sungkeun Kim**, Samsung Research.

**Abstract**: Hardware isolation is a critical security feature in systems ranging from cloud computing to embedded devices. The WorldGuard security model offers a promising approach, yet few SoCs currently implement it. Fixed WorldGuard implementations in off-the-shelf SoCs, however, lack the flexibility needed for security designers to prototype and customize architectures. To address this, we open-sourced Vyond, a configurable WorldGuard implementation within Chipyard, enabling agile and adaptable security prototyping. We demonstrate how WorldGuard components integrate seamlessly into a Rocket SoC using Chipyard’s parameterized framework. Additionally, Vyond provides three WorldGuard-enabled hardware implementations (Simulation, FPGA, and QEMU) and a baseline security monitor, allowing designers to rapidly implement a secure OS, test functionalities, and evaluate hardware costs. We anticipate that Vyond will accelerate RISC-V security research and drive innovation in hardware security architectures.

[To page top](#summary) — [To posters at P1.4 (S1) on Wednesday 14](#P1.4-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

On Wednesday 14, at island P2.1 (S2)

------------------------------------------------------------------------

### Hassert: Hardware Assertion-Based Agile Verification Framework with FPGA Acceleration

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.01-ZHANG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.01-ZHANG-abstract.pdf). Sub. \#119. Wednesday 14, at island 2.1 on S2. ([P2.1.01-Wed](#P2.1.01-Wed)).

**Ziqing Zhang**, Institute of Computing Technology, CAS. **Weijie Weng**, Institute of Computing Technology, CAS. **Yungang Bao**, ICT, CAS. **Kan Shi**, Chinese Academy of Sciences.

**Abstract**: Functional verification is typically the bottleneck of the chip development cycle, mainly due to the burdensome simulation and debugging process using software simulators. For RISC-V, verification becomes even more critical to support a wide range of applications and extensions. Assertion-Based Verification (ABV) has been widely adopted to provide better visibility and detect unexpected behaviors. While ABV enhances efficiency but is limited to slow software simulations. FPGA prototyping offers faster alternatives but lacks fine-grained debugging for error analysis. To address these challenges, we present Hassert, an efficient ABV framework that combines high-performance verification on FPGAs with fine-grained debugging in software. Hassert automates the scheduling and mapping of SystemVerilog Assertions (SVAs) to the FPGA, allowing for extensive hardware testing. To further improve debugging efficiency, Hassert enables dynamic switching of assertions and uArch-guided snapshots based on the assertion. We demonstrate that these contributions significantly enhance verification efficiency over software simulations for various designs, with minimal area overhead and full debugging visibility.

[To page top](#summary) — [To posters at P2.1 (S2) on Wednesday 14](#P2.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Secure Domain-Specific Debugging on an MCU

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.02-CHANG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.02-CHANG-abstract.pdf). Sub. \#47. Wednesday 14, at island 2.1 on S2. ([P2.1.02-Wed](#P2.1.02-Wed)).

**Alvin Che-Chia Chang**, Andes Technology. **Paul Shan-Chyun Ku**, Andes Technology.

**Abstract**: A modern embedded system involves multiple developers with varying security requirements, often leading to trust issues and the need for isolated proprietary assets. A secure monitor addresses this by providing multiple logically isolated execution environments (EEs), each maintaining its own state, ensuring invisibility between EEs. Traditional debugging mechanisms in RISC-V allow unrestricted access, compromising security by bypassing runtime isolation measures. Existing secure debugging methods authenticate debuggers but grant full access upon successful authentication, undermining the intended isolation. This talk presents a domain-specific debugging approach that restricts debugger access to predefined assets based on authentication, maintaining security and isolation during debugging. The solution is implemented into our secure monitor without using the RISC-V Debug Module, resulting in a low-cost, highly secure, and flexible debugging environment.

[To page top](#summary) — [To posters at P2.1 (S2) on Wednesday 14](#P2.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Comprehensive Lockstep Verification for NaxRiscv SoC integrating RISCV DV, RVLS, and Questa/UVM

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.03-IGHILAHRIZ-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.03-IGHILAHRIZ-abstract.pdf). Sub. \#136. Wednesday 14, at island 2.1 on S2. ([P2.1.03-Wed](#P2.1.03-Wed)).

**Billal IGHILAHRIZ**, CEA-LETI. **Olivier Savry**, CEA LETI.

**Abstract**: This paper presents a robust lockstep verification framework for the NaxRiscv System-on-Chip (SoC) —a flexible, open-source, out-of-order, and superscalar RISC-V core. Our methodology integrates cycle-accurate RTL simulation using Verilator, functional co-simulation with the Spike golden model, and constrained-random test generation via RISCV-DV to achieve a comprehensive verification framework. Functional coverage metrics are collected through a Questa/UVM-based verification environment, enabling early detection of subtle behavioral mismatches and corner-case failures. Our methodology rigorously validates ISA compliance but also significantly enhancing the overall verification process.

[To page top](#summary) — [To posters at P2.1 (S2) on Wednesday 14](#P2.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### From RustVMM to Kata-Containers: Securing Container Workloads with H-ext Based Virtualization Software

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.04-HE-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.04-HE-abstract.pdf). Sub. \#79. Wednesday 14, at island 2.1 on S2. ([P2.1.04-Wed](#P2.1.04-Wed)).

**Ruoqing He**, ISCAS. **Sheng Qu**, ISCAS. **Yanjun Wu**, ISCAS.

**Abstract**: The work we are doing is critical for laying the foundation of a Confidential Computing software stack that will fully support the RISC-V architecture, equipped with H Extensions, AIA, and IOMMU capabilities. As the computing industry moves toward more secure infrastructures, RISC-V presents a unique opportunity with its open-source instruction set architecture (ISA) and its potential to be tailored for security-sensitive applications. Our Rust-based software stack, built around rust-vmm, is designed to capitalize on the RISC-V platform’s extensibility, offering lightweight virtualization solutions such as Dragonball, StratoVirt, Cloud-Hypervisor, and Firecracker. These hypervisors, coupled with container runtimes like Kata Containers, provide the required isolation and performance needed in confidential computing environments, where the stakes for data privacy and security are higher than ever. By proactively developing this stack ahead of hardware availability, we ensure that once RISC-V chips with hardware extensions for virtualization and secure memory management hit the market, the ecosystem is “plug-and-play” ready. Furthermore, by aiming to meet the RISC-V Server Platform Specification, our stack positions itself as an integral piece in the adoption and standardization of Confidential Computing across RISC-V-based server environments. We are creating an ecosystem that integrates secure VM isolation, efficient interrupt and I/O management, and flexible orchestration, all within a cloud-native framework. Our approach, reliant on Rust’s inherent safety guarantees, provides a secure-by-design foundation that mitigates common vulnerabilities seen in traditional programming languages. This early work ensures that we are not just aligning with future hardware but actively shaping the software landscape required for secure, scalable, and robust RISC-V server platforms—empowering cloud providers, enterprises, and developers worldwide to leverage RISC-V’s full potential.

PRs accepted in Rust-VMM: <https://github.com/search?q=is%3Amerged+author%3ATimePrinciple+org%3Arust-vmm&type=pullrequests>

PRs accepted in Cloud-Hypervisor: <https://github.com/search?q=is%3Amerged+author%3ATimePrinciple+org%3Acloud-hypervisor&type=pullrequests>

PRs in Kata-Containers: <https://github.com/search?q=author%3ATimePrinciple+org%3Akata-containers+is%3Aopen&type=pullrequests>

[To page top](#summary) — [To posters at P2.1 (S2) on Wednesday 14](#P2.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Verification of a RISC-V system with multiple cores

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.05-GENOVESE-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.05-GENOVESE-abstract.pdf). Sub. \#144. Wednesday 14, at island 2.1 on S2. ([P2.1.05-Wed](#P2.1.05-Wed)).

**Ignacio Genovese**, Barcelona Supercomputing Center. **Ivan Diaz**, Barcelona Supercomputing Center. **Albert Aguilera**, Barcelona Supercomputing Center. **Abdul Rauf**, Barcelona Supercomputing Center**, but currently at ARM.. \*\*Oscar Palomar**, Barcelona Supercomputing Center.

**Abstract**: Verifying complex RISC-V systems, particularly out-of-order cores and their cache hierarchies, presents significant challenges due to the need for thorough functional coverage and reference model validation. This paper presents the verification strategy for a RISC-V system composed of an out-of-order core and its cache hierarchy. We have implemented a stand-alone UVM environment at the core-level that is then reused at the system-level testbench. Our approach employs a modified version of Spike ISS as a reference model to ensure correct execution and validation of test cases. We use multiple directed tests (riscv-tests, compliance), along with randomly generated binaries using riscv-dv. This work contributes a reusable UVM testbench, an enhanced reference model, and a set of directed and randomized tests that significantly improve coverage and bug detection in RISC-V system verification.

[To page top](#summary) — [To posters at P2.1 (S2) on Wednesday 14](#P2.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### An Architecture Design for Expressive Security

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.06-YU-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.06-YU-abstract.pdf). Sub. \#89. Wednesday 14, at island 2.1 on S2. ([P2.1.06-Wed](#P2.1.06-Wed)).

**Jason Zhijingcheng Yu**, National University of Singapore. **Prateek Saxena**, National University of Singapore.

**Abstract**: Today’s computer systems face many security challenges such as memory safety violations, pressing need for fine-grained isolation, and growing demand for support of non-traditional trust models (e.g., confidential computing). The prevalent approach to those challenges at the architecture level is security extensions designed to address individual security requirements. This patchwork of special-purpose security extensions has two main problems. Firstly, it is difficult for software to rely on them because of varying support in hardware implementations. The hardware vendors can also modify or even deprecate security extensions at any time. Secondly, when software desires multiple security goals, it has to compose multiple security extensions, which is often difficult or even impossible. In light of this, we create Capstone, a new architecture design that provides a unified foundation for achieving expressive security goals. Capstone adopts a capability-based model and extends it further to support exclusive memory ownership, revocable access delegation, and extensible privilege hierarchies. We show that Capstone enables various use cases such as two-way isolation as required by confidential computing that is arbitrarily nestable, full memory safety, and detection of Rust principle violations, all through a single uniform capability-based abstraction. We also present our design of a matching modular software system with finely isolated components as well as our hardware implementation of a concrete RISC-V-based version of Capstone.

[To page top](#summary) — [To posters at P2.1 (S2) on Wednesday 14](#P2.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Verification of CoreSwap: Replacing ARM Cortex-A5 with RISC-V CVA6 in ARM SoC Environment

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.07-BASHIR-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.07-BASHIR-abstract.pdf). Sub. \#189. Wednesday 14, at island 2.1 on S2. ([P2.1.07-Wed](#P2.1.07-Wed)).

**Muhammad Hammad Bashir**, Department of Electrical Engineering, U.E.T Lahore. **Umer Shahid**, UET Lahore. **Muhammad Tahir**, Department of Electrical Engineering, U.E.T Lahore. **Yazan Hussnain**, 10xEngineers. **Fatima Saleem**, 10xEngineers.

**Abstract**: This paper presents the verification methodology and results of the CoreSwap project, where the ARM Cortex-A5 core in ARM Educational Kit SoC was replaced with the open-source RISC-V OpenHW CVA6 core. The project demonstrates the feasibility of integrating a RISC-V core into an existing SoC ecosystem while maintaining functionality and system stability. We detail the comprehensive verification process, including core-level Architecture Compliance Tests (ACTs), manually written system-level tests, FPGA synthesis on a Kintex-7 platform, and running performance benchmarks. The verification strategy highlights the challenges and solutions to validate such a large-scale System on Chip (SoC). This seamless integration and verification of the CoreSwap underscores the potential of RISC-V in proprietary SoC environments.

[To page top](#summary) — [To posters at P2.1 (S2) on Wednesday 14](#P2.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Ahead of Time Generation for GPSA Protection in RISC-V Embedded Cores

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.08-SAVARY-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.1.08-SAVARY-abstract.pdf). Sub. \#124. Wednesday 14, at island 2.1 on S2. ([P2.1.08-Wed](#P2.1.08-Wed)).

**Louis Savary**, Inria. **Simon Rokicki**, Irisa. **Steven Derrien**, UniversitÃ© de Bretagne Occidentale/Lab-STICC. **Erven Rohou**, Inria.

**Abstract**: State-of-the-art hardware countermeasures against fault attacks are based, among others, on control flow and code integrity checking. These integrities can be asserted by Generalized Path Signature Analysis and Continuous Signature Monitoring. However, supporting such mechanisms requires a dedicated compiler flow and does not support indirect jumps. In this work we propose a technique based on a hardware/software runtime to generate those signatures while executing unmodified COTS RISC-V binaries. The proposed approach has been implemented on a pipelined rv32i processor, and experimental results show an average slowdown of x1.82 compared to unprotected implementations while being completely compiler independent.

[To page top](#summary) — [To posters at P2.1 (S2) on Wednesday 14](#P2.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

On Wednesday 14, at island P2.2 (S2)

------------------------------------------------------------------------

### Finding More Bugs in Your RISC-V CPUs with DiffTest and XFUZZ

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.01-XU-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.01-XU-abstract.pdf). Sub. \#200. Wednesday 14, at island 2.2 on S2. ([P2.2.01-Wed](#P2.2.01-Wed)).

**Yinan Xu**, State Key Lab of Processors, Institute of Computing Technology, Chinese Academy of Sciences.

**Abstract**: Ensuring the functional correctness of RISC-V processors is increasingly challenging due to complex designs and non-deterministic behaviors. This work presents an automated verification framework that integrates DiffTest, a co-simulation platform for precise discrepancy detection, with XFUZZ, a coverage-guided fuzzer leveraging footprint memory-based mutations. Our approach enhances test efficiency, broadens state space exploration, and uncovers subtle processor bugs missed by traditional verification methods. Evaluation on open-source RISC-V processors demonstrates 95.3% coverage in less than 10 hours and the detection of four long-standing functional bugs, including one persisting for nearly 10 years. Both tools are open-source and welcome contributions from the research and industrial communities to further advance RISC-V verification.

[To page top](#summary) — [To posters at P2.2 (S2) on Wednesday 14](#P2.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### HW-extended Containers on FPGA-based RISC-V SoC.

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.02-AMPLIANITIS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.02-AMPLIANITIS-abstract.pdf). Sub. \#130. Wednesday 14, at island 2.2 on S2. ([P2.2.02-Wed](#P2.2.02-Wed)).

**Konstantinos Amplianitis**, School of Electrical and Computer Engineering, Technical University of Crete. **Katerina Tsimpirdoni**, School of Electrical and Computer Engineering, Technical University of Crete. **Andreas Brokalakis**, School of Electrical and Computer Engineering, Technical University of Crete. **George Christou**, Technical University of Crete. **Konstantinos Georgopoulos**, Telecommunication Systems Institute, Technical University of Crete. **Sotiris Ioannidis**, School of Electrical and Computer Engineering, Technical University of Crete.

**Abstract**: This paper describes a technology that brings together three key elements of reconfigurable hardware (FPGAs) prototyping, namely, Docker containers, RISC-V architectures, and runtime (dynamic) partial reconfiguration. The work envisaged serves the purpose of further expanding FPGA capabilities by allowing these processing platforms to support state-of-the-art development of prototypes with RISC-V soft-cores at their centre. The RISC-V processor features an Operating System (OS) that fully supports the execution of HW-extended Docker containers, which in turn contain all the necessary libraries, software, firmware and bitstreams for the implementation and utilisation of accelerator cores/modules within the reconfigurable fabric of the FPGA. Hence, different Docker containers, representing separate services and clients, will be able to deploy on-demand part of their functionality directly into the FPGA fabric benefiting from the parallel execution capabilities that this type of technology has to offer while the overall system will be based on a soft instance of a RISC-V processor core.

[To page top](#summary) — [To posters at P2.2 (S2) on Wednesday 14](#P2.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### AccUnit: Accelerating Unit Level Verification for RISC-V Processors Using FPGA

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.03-ZHU-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.03-ZHU-abstract.pdf). Sub. \#203. Wednesday 14, at island 2.2 on S2. ([P2.2.03-Wed](#P2.2.03-Wed)).

**Chenang Zhu**, Institute of Computing Technology Chinese Academy of Sciences, China. **Weidong Li**, Shanghaitech University, China. **YunGang Bao**, Institute of Computing Technology Chinese Academy of Sciences, China. **Kan Shi**, Institute of Computing Technology Chinese Academy of Sciences, China.

**Abstract**: Verification consumes up to 70% of the entire chip development cycle, creating a critical efficiency bottleneck—especially when developing complex chips such as RISC-V processors. However, current research on agile verification primarily focuses on system-level verification. As chip development progresses, the cost of fixing bugs may increase exponentially. To enable a shift-left verification effort, we propose AccUnit: an end-to-end tool flow for efficient unit-level verification of RISC-V processors using heterogeneous hardware acceleration. AccUnit automatically duplicates the design-under-test (DUT) to fit the FPGA alongside software reference models running on the host, while generating distinct input stimulus sets for each DUT and reference model pair. The proposed system monitors and compares key I/O ports between the DUT and reference model, enabling massive parallel execution of automated unit-level self-checking for RISC-V processor modules. We also integrate a coverage collection scheme where synthesizable coverpoints are automatically created and inserted into the DUT during compile time. This allows coverage information to be collected on the FPGA during operation, enabling comprehensive evaluation of functional verification quality. The results demonstrate that our approach achieves up to a 75× performance improvement compared to software simulation using Verilator

[To page top](#summary) — [To posters at P2.2 (S2) on Wednesday 14](#P2.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### HWFuzz: An FPGA-Accelerated Fuzzing Framework for Efficient RISC-V Verification

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.04-ZHONG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.04-ZHONG-abstract.pdf). Sub. \#133. Wednesday 14, at island 2.2 on S2. ([P2.2.04-Wed](#P2.2.04-Wed)).

**Yang Zhong**, Institute of Computing Technology Chinese Academy of Sciences, China. **Haoran Wu**, University of Cambridge, United Kingdom. **Yungang Bao**, Institute of Computing Technology Chinese Academy of Sciences, China. **Kan Shi**, Institute of Computing Technology Chinese Academy of Sciences, China.

**Abstract**: In this study, we introduce a high-performance fuzzing-based verification framework that automatically detects potential vulnerabilities in RISC-V processors. The framework tackles the challenge of lengthy verification cycles required to achieve hard-to-reach coverage points, particularly in complex processors.

Our solution enhances verification efficiency through two key components.

First, we implement a hardware fuzzer that rapidly generates large-scale RISC-V instruction sequences. Instead of simply using random instructions, the fuzzing-based instructions are specifically designed to achieve better coverage while exploring hard-to-reach states during RISC-V processor verification.

Second, we develop an end-to-end verification framework that iteratively generates coverage-directed stimuli using the hardware fuzzer, applies them to the design-under-test (DUT), collects coverage data, and identifies uncovered states for further fuzzing iterations. Through FPGA acceleration, our framework achieves 2.03× speedup against conventional software approaches.

[To page top](#summary) — [To posters at P2.2 (S2) on Wednesday 14](#P2.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### UnityChip Verification: Scaling Out Hardware Verification with Software Testing Developers

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.05-XIE-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.05-XIE-abstract.pdf). Sub. \#204. Wednesday 14, at island 2.2 on S2. ([P2.2.05-Wed](#P2.2.05-Wed)).

**Yunlong Xie**, Institute of Computing Technology, CAS. **Zhicheng Yao**, Institute of Computing Technology, CAS. **Sa Wang**, Institute of Computing Technology, CAS. **Yungang Bao**, ICT, CAS.

**Abstract**: The growing open-source hardware ecosystem presents a new opportunity to enhance hardware verification efficiency by involving a broader range of verification participants. As the software testing ecosystem has benefited from various tools and methods developed by its large community, this success offers a promising future for scaling out hardware verification by incorporating software testing developers.  
To support software developers in hardware verification, we propose three techniques to facilitate this integration: (1) providing state machine abstractions (cycle-accurate and loosely-timed), (2) encapsulating hardware designs into software packages in multiple programming languages, and (3) introducing socket data transport and bidirectional direct function calls. These techniques are implemented on the UnityChip Verification(UCV) platform, enabling software developers and tools to engage in hardware verification workflows and collaborate with hardware engineers using hardware frameworks.  
We evaluate our methods on the XiangShan processor, demonstrating UCV’s effectiveness through case studies: software developers without hardware backgrounds uncover 11 bugs in two months. Zero-experience developers submit valid verification cases in 20 hours, and reducing average initiation time by 77% and enhancing existing verification environment with Python, accelerating the process by 16.6% and reducing lines of code by 12%.

[To page top](#summary) — [To posters at P2.2 (S2) on Wednesday 14](#P2.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Security assessment methodology for RISC-V cores

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.06-KARMARKAR-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.06-KARMARKAR-abstract.pdf). Sub. \#143. Wednesday 14, at island 2.2 on S2. ([P2.2.06-Wed](#P2.2.06-Wed)).

**Apurba Karmarkar**, Instituto de Microelectronica de Sevilla**, IMSE-CNM., CSIC, US. \*\*Pablo Navarro-Tornero**, Instituto de Microelectronica de Sevilla**, IMSE-CNM., CSIC, US. \*\*Eros Camacho-Ruiz**, Instituto de Microelectronica de Sevilla**, IMSE-CNM., CSIC, US. \*\*Macarena C. Martinez-Rodriguez**, Instituto de Microelectronica de Sevilla**, IMSE-CNM., CSIC, US. \*\*Piedad Brox**, Instituto de Microelectronica de Sevilla\*\*, IMSE-CNM., CSIC, US.

**Abstract**:

[To page top](#summary) — [To posters at P2.2 (S2) on Wednesday 14](#P2.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Reconfigurable Processor-Centric Accelerators for Safety-Critical Applications

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.07-WAUCQUEZ-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.2.07-WAUCQUEZ-abstract.pdf). Sub. \#217. Wednesday 14, at island 2.2 on S2. ([P2.2.07-Wed](#P2.2.07-Wed)).

**Luis Waucquez**, Centro Electronica Industrial - Universidad Politécnica de Madrid. **Alfonso Rodriguez**, Centro Electronica Industrial - Universidad Politécnica de Madrid.

**Abstract**: The growing complexity of modern electronic systems operating in harsh environments with strict safety requirements necessitates robust mechanisms to ensure reliability and fault tolerance. These systems must function efficiently under challenging conditions, addressing issues such as single-event upsets and common mode failures in applications including IoT, aerospace, and the automotive industry. This paper introduces a versatile processor-centric accelerator platform designed for safety-critical applications. Built on the RISC-V ISA architecture, the platform’s cores support four operational modes: Single, Triple-Core LockStep (TCLS), Dual-Core LockStep (DCLS), and DCLS with classic staggering. These modes allow for flexible, safety-oriented configurations tailored to various critical application needs. To evaluate the platform’s performance and fault tolerance, a small fault injection campaign was conducted, demonstrating its capability to maintain reliable operation while delivering the necessary computational power.

[To page top](#summary) — [To posters at P2.2 (S2) on Wednesday 14](#P2.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

On Wednesday 14, at island P2.3 (S2)

------------------------------------------------------------------------

### Open-source SPMP-based CVA6 Virtualization

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.01-RODRÍGUEZ-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.01-RODRÍGUEZ-abstract.pdf). Sub. \#190. Wednesday 14, at island 2.3 on S2. ([P2.3.01-Wed](#P2.3.01-Wed)).

**Manuel Alejandro Rodríguez**, Centro ALGORITMI/LASI. **Jose Martins**, University of Minho. **Bruno Sa**, University of Minho - Centro ALGORITMI/LASI. **Sandro Pinto**, University of Minho.

**Abstract**: This work presents the first open-source design and implementation of the RISC-V SPMP for hypervisor. We integrated the dual-stage SPMP implementation into an MMU-less 64-bit CVA6 core with the Hypervisor extension enabled. The modified core was functionally validated using a software stack built around the Bao hypervisor. Preliminary results regarding FPGA resource utilization are also provided. Future work includes benchmarking the SPMP-based platform and comparing its performance with conventional MMU-based virtualization. Additionally, we plan to contribute to the RISC-V community by developing a QEMU implementation of the dual-stage SPMP.

Thanks for considering this submission! Hope it is relevant for RISC-V

[To page top](#summary) — [To posters at P2.3 (S2) on Wednesday 14](#P2.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### OpenTitan Integrated: A RISC-V Open-Source Silicon Root-of-Trust for large SoCs

[Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.02-SCHILLING-abstract.pdf). Sub. \#221. Wednesday 14, at island 2.3 on S2. ([P2.3.02-Wed](#P2.3.02-Wed)).

**Robert Schilling**, Rivos Inc.. **Samuel Ortiz**, Rivos Inc.. **Ravi Sahita**, Rivos Inc.. **Andreas Kurth**, Lowrisc CIC.

**Abstract**: Modern System-on-Chips (SoCs) rely on a secure Root of Trust (RoT) as the foundation for all security services. Compromise of the RoT can have catastrophic consequences, undermining the security of the entire system.

This paper presents OpenTitan Integrated, an open-source silicon RoT based on RISC-V specifically tailored for integration into the complex security subsystems of large SoCs. OpenTitan Integrated extends the functionality of the discrete OpenTitan implementation by addressing the specific needs of integrated deployments. Key contributions include: 1) a clear interface trust boundary, defining secure communication paths and preventing privilege escalation; 2) a robust and standardized communication interface, enabling seamless interaction with other SoC components; and 3) a flexible register isolation mechanism, protecting sensitive registers in the system from unauthorized access and modification. These additions enable secure interaction with other SoC components and prevent unauthorized access, enhancing the overall security posture of the SoC.

Furthermore, OpenTitan Integrated’s open-source nature, available on GitHub under a permissive license, facilitates community review, independent verification, and enhances the overall security and trustworthiness of the design. This collaborative approach allows for rapid identification and mitigation of potential vulnerabilities, leading to a more robust and secure RoT.

[To page top](#summary) — [To posters at P2.3 (S2) on Wednesday 14](#P2.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Safe Speculation for CHERI

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.03-FUCHS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.03-FUCHS-abstract.pdf). Sub. \#16. Wednesday 14, at island 2.3 on S2. ([P2.3.03-Wed](#P2.3.03-Wed)).

**Franz A. Fuchs**, University of Cambridge. **Jonathan Woodruff**, University of Cambridge. **Peter Rugg**, University of Cambridge. **Alexandre Joannou**, University of Cambridge. **Simon W. Moore**, University of Cambridge.

**Abstract**: Transient-execution attacks continue to plague the computer hardware industry. Recent attacks show that they can leak sensitive information on many processors of Apple’s M chip series. These attacks cannot only target conventional systems, but also secure architectures, e.g., CHERI-enhanced processors. The CHERI capability instruction-set extension promises proven architectural guarantees for memory safety and pointer provenance. However, superscalar and out-of-order CHERI implementations will need to contend with microarchitectural transient-execution side-channel attacks. To ensure the safety of all CHERI implementations, we articulate CSC: a universal architectural speculation contract for the CHERI architecture that maintains key capability invariants in speculation. We then develop tests against sub-classes of CSC, and discover violations in CHERI-Toooba that lead to a new class of transient-execution attacks. We then develop strategies to fully enforce CSC in CHERI-Toooba. We find that simplistic, strong enforcement incurs a low performance overhead of only 3.43\\ in SPECint2006 benchmarks, with promise for more optimal designs in the future.

[To page top](#summary) — [To posters at P2.3 (S2) on Wednesday 14](#P2.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Exhaustive Security Verification of CHERI Processors

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.04-DUQUE-ANTÓN-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.04-DUQUE-ANTÓN-abstract.pdf). Sub. \#63. Wednesday 14, at island 2.3 on S2. ([P2.3.04-Wed](#P2.3.04-Wed)).

**Anna Lena Duque Antón**, RPTU Kaiserslautern-Landau. **Johannes Müller**, RPTU Kaiserslautern-Landau. **Philipp Schmitz**, RPTU Kaiserslautern-Landau. **Tobias Jauch**, RPTU Kaiserslautern-Landau. **Alex Wezel**, RPTU Kaiserslautern-Landau. **Lucas Deutschmann**, RPTU Kaiserslautern-Landau. **Mohammed R. Fadiheh**, Stanford University. **Dominik Stoffel**, RPTU Kaiserslautern-Landau. **Wolfgang Kunz**, RPTU Kaiserslautern-Landau.

**Abstract**: CHERI is a promising approach to safeguarding data in memory by providing and enforcing fine-grained memory protection directly in hardware. The recently published VeriCHERI verification flow can verify global confidentiality and integrity properties for CHERI systems “spec-free”, i.e., without relying on a golden ISA model. We present a case study to demonstrate the effectiveness and scalability of VeriCHERI on the CHERIoT Ibex RISC-V processor.

[To page top](#summary) — [To posters at P2.3 (S2) on Wednesday 14](#P2.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### CHERI extended Muntjac SoC

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.06-WANG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.06-WANG-abstract.pdf). Sub. \#118. Wednesday 14, at island 2.3 on S2. ([P2.3.06-Wed](#P2.3.06-Wed)).

**Yuecheng Wang**, University of Cambridge. **Jonathan Woodruff**, University of Cambridge. **Peter Rugg**, University of Cambridge. **Alexandre Joannou**, University of Cambridge. **Samuel W. Stark**, University of Cambridge. **Simon W. Moore**, University of Cambridge.

**Abstract**: The research interest in CHERI has been increasing over the past decade. Various research projects have been conducted on commercial Morello and CHERI-Toooba \[1\] over the years, a high parameterisable core written in BlueSpec SystemVerilog. There is an ongoing research need of more diverse CHERI systems to evaluate and utilize CHERI more extensively. Moreover, there is a need for more commercial grade cores written in SystemVerilog to aim commercial adoption. While CHERIoT from Microsoft and SCI Semi demonstrates CHERI for microcontrollers, we demonstrate CHERI for a commercial application-class scalar core by extending Muntjac from lowRISC.

[To page top](#summary) — [To posters at P2.3 (S2) on Wednesday 14](#P2.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Commercial Poster: Codasip's X730 core, the word's first commercially available CHERI-RISC-V Application Core

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.07-KURD-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.07-KURD-abstract.pdf). Sub. \#121. Wednesday 14, at island 2.3 on S2. ([P2.3.07-Wed](#P2.3.07-Wed)).

**Tariq Kurd**, Codasip.

**Abstract**: This is a commercial poster presentation about the Codasip X730 core. It discusses the benefits of CHERI, how the addition of CHERI effects the pipeline and the PPA impact of adding CHERI.

[To page top](#summary) — [To posters at P2.3 (S2) on Wednesday 14](#P2.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### On a Static Analysis Methodology for Confidentiality and Security Signoff of RISC-V Crypto Core

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.08-SHARMA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P2.3.08-SHARMA-abstract.pdf). Sub. \#14. Wednesday 14, at island 2.3 on S2. ([P2.3.08-Wed](#P2.3.08-Wed)).

**Varun Sharma**, Real Intent Inc.. **Vikas Sachdeva**, Real Intent. **Vinod Viswanath**, Real Intent, Inc..

**Abstract**: Confidentiality is a fundamental pillar of the security triad, alongside Integrity and Availability. Spectre-like vulnerabilities, often observed in RISC-V architectures, stem from improper implementation and transient execution, while flawed AES implementations in RISC-V systems can expose critical signals. The industry’s lack of a reliable single sign-off method complicates the verification process, requiring multiple stages such as Simulation, Formal methods, and post-Silicon validation. Signing off on confidentiality is particularly challenging without verification in unknown scenarios, and early detection at the RTL stage remains elusive.

This innovative technology addresses these challenges by capturing Secure Data Transaction Intent across user-defined signals within RISC-V designs and performing static analysis to identify illegal data flows that cause security violations. By enabling early detection with minimal constraints during the RTL design phase, this approach is scalable to full SoC-sized RISC-V designs, significantly saving time and effort.

[To page top](#summary) — [To posters at P2.3 (S2) on Wednesday 14](#P2.3-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

On Wednesday 14, at island P3.1 (S3)

------------------------------------------------------------------------

### TYRCA: A RISC-V Tightly-coupled accelerator for Code-based Cryptography

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.1.01-DOLMETA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.1.01-DOLMETA-abstract.pdf). Sub. \#52. Wednesday 14, at island 3.1 on S3. ([P3.1.01-Wed](#P3.1.01-Wed)).

**Alessandra Dolmeta**, Politecnico di Torino. **Stefano Di Matteo**, CEA-Leti. **Emanuele Valea**, CEA LIST. **Mikael Carmona**, CEA-Leti. **Antoine Loiseau**, CEA-Leti. **Maurizio Martina**, Politecnico di Torino. **Guido Masera**, Politecnico di Torino.

**Abstract**: Post-quantum cryptography (PQC) has garnered significant attention across various communities, particularly with the National Institute of Standards and Technology (NIST) advancing to the fourth round of PQC standardization. One of the leading candidates is Hamming Quasi-Cyclic (HQC), which received a significant update on February 23, 2024. This update, which introduces a classical dense-dense multiplication approach, has no known dedicated hardware implementations yet. The innovative Core-V eXtension InterFace (CV-X-IF) is a communication interface for RISC-V processors that significantly facilitates the integration of new instructions to the Instruction Set Architecture (ISA), through tightly connected accelerators. In this paper, we present a TightlY-coupled accelerator for RISC-V for Code-based cryptogrAphy (TYRCA), proposing the first fully tightly-coupled hardware implementation of the HQC-PQC algorithm, leveraging the CV-X-IF. The proposed architecture is implemented on the Xilinx Kintex-7 FPGA. Experimental results demonstrate that TYRCAr educes the execution time by 94% to 96% for HQC-128, HQC-192, and HQC-256, showcasing its potential for efficient HQC code-based cryptography.

[To page top](#summary) — [To posters at P3.1 (S3) on Wednesday 14](#P3.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### RISC-V-based Acceleration Strategies for Post-Quantum Cryptography

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.1.02-SARNO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.1.02-SARNO-abstract.pdf). Sub. \#56. Wednesday 14, at island 3.1 on S3. ([P3.1.02-Wed](#P3.1.02-Wed)).

**Ivan Sarno**, CEA-List. **Stefano Di Matteo**, CEA-Leti. **Emanuele Valea**, CEA LIST. **Cyrille Chavet**, Universitè de Grenoble - TIMA.

**Abstract**: In this paper, we explore the main existing approaches to accelerate Post-Quantum Cryptography (PQC) algorithms taking advantages of the flexibility offered by the RISC-V platforms. Tightly-coupled accelerators reside inside the CPU pipeline enabling fast execution of custom instructions. Coprocessors are connected directly to the CPU to execute more complex tasks. Loosely-coupled accelerators are accessed through the bus, offering flexibility and high performance. We show a synthetic comparison among these acceleration strategies for Number Theoretic Transform (NTT) and SHA-3, evaluating performance and area overhead on FPGA.

[To page top](#summary) — [To posters at P3.1 (S3) on Wednesday 14](#P3.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Efficient system-level support for CHERI Capabilities

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.1.03-HILL-poster.pdf). Sub. \#146. Wednesday 14, at island 3.1 on S3. ([P3.1.03-Wed](#P3.1.03-Wed)).

**Mark Bowen Hill**, Codasip.

**Abstract**: Memory safety is by far the most common source of security vulnerabilities in computer systems, for example, both Microsoft and Google Chromium estimate that, year-on-year, around 70% of the critical security issues they encounter are in this class. This issue is being addressed by the CHERI (Capability Hardware Enhanced RISC Instructions) technology developed by University of Cambridge and which, with the formation of the CHERI TG/SIG, RISC-V developers now have a fantastic opportunity to take to market.

When the RISC-V CHERI Extension is enabled in a hart all memory accesses are made via capabilities rather than pointers. These capabilities incorporate bounds and permission which are checked on every single memory access, thus providing fine grained memory protection

To ensure that capabilities cannot be forged or manipulated by an adversary, CHERI requires that the system implements an out-of-band tag bit for every element of memory storage that can hold a capability. This tag and the data it protects must appear by all observers in the system to be updated atomically.

The presentation will describe the challenges associated with efficient handling of tags at a system level and how Codasip has met them in the development of the first commercially available System IP to solve this issue: the Capability Management Unit (CMU) which we will be demonstrating at the Summit.

[To page top](#summary) — [To posters at P3.1 (S3) on Wednesday 14](#P3.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### RISC-V Solutions for Post Quantum Computing for Machine Readable Travel Documents

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.1.04-KOSMIDIS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.1.04-KOSMIDIS-abstract.pdf). Sub. \#187. Wednesday 14, at island 3.1 on S3. ([P3.1.04-Wed](#P3.1.04-Wed)).

**Leonidas Kosmidis**, Barcelona Supercomputing Center**, BSC. and Universitat PolitÃ¨cnica de Catalunya**, UPC.. **Matina Maria Trompouki**, Barcelona Supercomputing Center**, BSC.. \*\*Eric Rufart Blasco**, Universitat Politècnica de Catalunya**, UPC. and Barcelona Supercomputing Center**, BSC.. **Jannis Wolf**, Barcelona Supercomputing Center. **Guillermo Vidal**, Universitat Politècnica de Catalunya**, UPC. and Barcelona Supercomputing Center**, BSC.. **Marc Solé Bonet**, Barcelona Supercomputing Center\*\*, BSC..

**Abstract**: The PQC4eMRTD (Post-Quantum Cryptography for electronic Machine-Readable Travel Documents) European Project has started in January 2025. The purpose of this Coordination and Support Action (CSA) project is to monitor and influence Post Quantum Computing solutions related to the security of identity documents with biometric data. RISC-V is the perfect candidate for the exploration of these solutions, therefore in addition to the standardisation involvement, we are working towards various implementations related to this domain.

[To page top](#summary) — [To posters at P3.1 (S3) on Wednesday 14](#P3.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### RISC-V based GPGPU on FPGA: A Competitive Approach for Scientific Computing ?

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.1.05-GUTHMULLER-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.1.05-GUTHMULLER-abstract.pdf). Sub. \#35. Wednesday 14, at island 3.1 on S3. ([P3.1.05-Wed](#P3.1.05-Wed)).

**Eric Guthmuller**, Univ. Grenoble Alpes, CEA, List. **Jérôme Fereyre**, Univ. Grenoble Alpes, CEA, List.

**Abstract**: FPGA architectures include increasingly complex arithmetic operators and optimized hard IPs, such as memory subsystems and Networks-on-Chip (NoC). This evolution leads to higher compute density also linked with high memory bandwidth. It represents an opportunity to tailor an architecture to niche application needs while being competitive with a costly ASIC implementation. More specifically, scientific computing requires high precision (\$\>\$~32 bits) floating point computation. However, GPU vendors are progressively favoring low precision performance for AI needs, and are even phasing out support for 64-bit floating point compute. We present an analytical study motivating the need to investigate the implementation of an open source 64-bit GPGPU architecture on a state of the art FPGA, as an alternative to GPUs for scientific computing.

[To page top](#summary) — [To posters at P3.1 (S3) on Wednesday 14](#P3.1-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

On Wednesday 14, at island P3.2 (S3)

------------------------------------------------------------------------

### Optimizing TLS Cryptographic Operations on RISC-V SoC with OpenTitan RoT

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.2.01-MUSA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.2.01-MUSA-abstract.pdf). Sub. \#222. Wednesday 14, at island 3.2 on S3. ([P3.2.01-Wed](#P3.2.01-Wed)).

**Alberto Musa**, University of Bologna. **Emanuele Parisi**, Universita’ di Bologna. **Luca Barbierato**, Politecnico di Torino. **Edoardo Patti**, Politecnico di Torino. **Andrea Bartolini**, University of Bologna. **Andrea Acquaviva**, University of Bologna. **Francesco Barchi**, Università di Bologna.

**Abstract**: This work presents a preliminary evaluation of a cryptographic software stack leveraging OpenTitan as a hardware security module within a RISC-V-based system-on-chip. The current implementation supports the TLS_RSA_WITH_AES_256_CBC_SHA256 cipher suite, integrating hardware-accelerated cryptographic operations to enhance security and performance. Through detailed benchmarking, we demonstrate up to 82x speedup for AES-256-CBC and 39x for SHA-256 on larger payload sizes compared to software-only implementations.

[To page top](#summary) — [To posters at P3.2 (S3) on Wednesday 14](#P3.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### CHERI performance optimization

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.2.02-SHAW-poster.pdf). Sub. \#192. Wednesday 14, at island 3.2 on S3. ([P3.2.02-Wed](#P3.2.02-Wed)).

**Carl R. Shaw**, Codasip.

**Abstract**: CHERI is a cross-architecture, fine-grained memory access control mechanism that can be used to address memory safety problems in software. It has recently been specified as a proposed extension to the RISC-V ISA and is currently going through the RISC-V International standardization process. Traditional approaches to fine-grained memory protection have often resulted in significant performance penalties and/or incomplete security coverage. Unlike traditional approaches, CHERI claims to provide robust, deterministic security with minimal performance loss. As CHERI takes a hardware/software co-design approach, hardware, software and compilers need to be optimized to realize good performance. In this talk we will describe the work being done to optimize CHERI and provide the most recent results.

[To page top](#summary) — [To posters at P3.2 (S3) on Wednesday 14](#P3.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Standardizing CHERI-RISC-V, CHERI TG specification and status update

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.2.03-KURD-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.2.03-KURD-abstract.pdf). Sub. \#115. Wednesday 14, at island 3.2 on S3. ([P3.2.03-Wed](#P3.2.03-Wed)).

**Tariq Kurd**, Codasip. **Ben Laurie**, Google.

**Abstract**: The CHERI TG was officially formed in October 2024. This talk is giving an up to date status of the CHERI-RISC-V specification, and so will be updated shortly before the actual presentation is given. Ratification is planned for August 2025, and so this talk is sheduled to be close to the freeze date, which is currently due in June 2025.

[To page top](#summary) — [To posters at P3.2 (S3) on Wednesday 14](#P3.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### An Open-Source Trusted Execution Environment for Resource-Constrained RISC-V MCUs

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.2.04-CUNHA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.2.04-CUNHA-abstract.pdf). Sub. \#154. Wednesday 14, at island 3.2 on S3. ([P3.2.04-Wed](#P3.2.04-Wed)).

**Luis Cunha**, University of Minho. **Daniel Oliveira**, University of Minho. **João Sousa**, University of Minho. **Tiago Gomes**, Centro Algoritmi. **Sandro Pinto**, University of Minho.

**Abstract**: This work presents the design and implementation of REDACTED\* Baremetal TEE, an open-source Trusted Execution Environment (TEE) targeting resource-constrained RISC-V-based MCUs with support for Machine, (Supervisor,) and User modes. The REDACTED Baremetal TEE leverages RISC-V’s privilege levels and memory isolation primitives to enable multi-world execution while maintaining strong security guarantees at the least privileged level. So far, we have implemented and validated the system on Machine and User mode-enabled cores, running a set of low-level benchmarks and test applications. Future plans include extending the support to the Supervisor mode and open-sourcing all artifacts to foster collaboration within the RISC-V community.

\*Project Name. Omitted due to blind review

[To page top](#summary) — [To posters at P3.2 (S3) on Wednesday 14](#P3.2-Wed) — [To all posters of Wednesday 14](#Wed)

------------------------------------------------------------------------

### Unified Emulation and Simulation Debug Environment for RISC-V Devices to Reduce Cost and Turnaround Time

[Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-14-RISC-V-Summit-Europe-P3.2.05-SHAJI-BABU-abstract.pdf). Sub. \#103. Wednesday 14, at island 3.2 on S3. ([P3.2.05-Wed](#P3.2.05-Wed)).

**Rejeesh Shaji Babu**, Ashling Microsystems.

**Abstract**: With increasing design complexity, validating hardware design and software debugger well before tape-out is essential. Traditional methods for hardware verification, software debugger bring-up, and hardware-software debugger compatibility are performed on emulation platforms such as Zebu from Synopsys or Palladium from Cadence using JTAG debuggers. Emulation, while effective for bug discovery with high turnaround time, offers limited debug visibility compared to simulation. Dependency on physical JTAG debugger caps the number of users to hardware availability. This paper describes mechanism to use the same software debugger on the simulation environment too and remove the use of physical JTAG debugger. The hardware to software communication utilizes a synthesizable JTAG transactor integrated into the Emulation environment, which interfaces seamlessly with the software debugger via TCP/IP sockets (or any other interprocess communication protocol). This enables issue of software debugger commands to hardware, as part of use-case stimuli. The collaterals for communication and stimuli are used in the simulation environment too, facilitating the rerun of emulation failures in simulation platform for bug resolution.

[To page top](#summary) — [To posters at P3.2 (S3) on Wednesday 14](#P3.2-Wed) — [To all posters of Wednesday 14](#Wed)

# Thursday 15 Posters

Sorted by expo level, poster island, and stand.

------------------------------------------------------------------------

On Thursday 15, at island P1.1 (S1)

------------------------------------------------------------------------

### Enabling Syscall Interception on RISC-V.

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.01-ANDRIĆ-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.01-ANDRIĆ-abstract.pdf). Sub. \#18. Thursday 15, at island 1.1 on S1. ([P1.1.01-Thu](#P1.1.01-Thu)).

**Petar Andrić**, Barcelona Supercomputing Center. **Aaron Call**, Barcleona Supercomputing Center. **Ramon Nou Castell**, Barcelona Supercomputing Center.

**Abstract**: The European Union’s technological sovereignty strategy centers around the RISC-V Instruction Set Architec- ture, with the European Processor Initiative leading efforts to build production-ready processors. Focusing on realizing a functional RISC-V ecosystem, in this poster, we detail the efforts made in porting a widely used syscall interception library, mainly used on Adhoc FS (i.e., DAOS, GekkoFS), to RISC-V and how we overcame some limitations encountered.

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Challenge Accepted: Python Packaging Infrastructure for the RISCV64 Ecosystem

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.02-GAMBLIN-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.02-GAMBLIN-abstract.pdf). Sub. \#62. Thursday 15, at island 1.1 on S1. ([P1.1.02-Thu](#P1.1.02-Thu)).

**Trevor Gamblin**, BayLibre Inc. **Mark D. Ryan**, Rivos Inc. **Julien Stephan**, BayLibre Inc..

**Abstract**: As the RISC-V ecosystem grows with new platforms and higher performance, a key area of interest is its applicability towards scientific computing, data analysis, and machine learning. On other architectures such as ARM, these areas are already well-supported thanks to broad availability of binaries for critical packages such as NumPy, pandas, and PyTorch, but with RISC-V these are largely unavailable. The problem is further compounded by the challenge of building such packages manually, where even foundational examples such as NumPy take a prohibitively long time to build from source on commonly-available hardware, in addition to being prone to build errors and dependency chains that lead to long hours of sorting through confusing stack traces. The RISE project is tackling this problem by building, testing, deploying, and maintaining binaries for a selection of these packages. This creates a path forward for developers that wish to leverage current and upcoming RISC-V platforms for specialized research and industry applications

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Enterprise Linux Enablement On RISC-V

Sub. \#67. Thursday 15, at island 1.1 on S1. ([P1.1.03-Thu](#P1.1.03-Thu)).

**Isaac Chute**, RISC-V International.

**Abstract**: This proposal is for a panel type conversation on the topic of Enterprise Distribution enablement on RISC-V, which is in essence the core software foundation for future Enterprise software workloads.

Productization Methodologies Each of the major Enterprise Linux Distributions will share an overview of their productization methodologies with regards to enabling RISC-V as a bona fide server platform.

Discussion The proposed session will begin with the host giving and overview of the current state of software ecosystem enablement pursuant to RISC-V platform support. This will be followed by a conversation with each of the other panelists around their respective companies investment into RISC-V.

The major takeaways from this session will be:

1.  A deeper understanding of how far the Enterprise Linux distribution enablement journey has come in anticipation of facilitating Enterprise software ecosystem workloads on RISC-V platforms.
2.  This should in turn help attendees understand the development chain of events that occur in order for RISC-V to become fully supported at the Enterprise level.
3.  The current status of RISC-V enablement on Open Distributions such as OpenSUSE, Fedora, and CentOS Stream.
4.  The status of each of the major Enterprise Linux distributions with regard to their investment in RISC-V.

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### The Road to Making openEuler a RISC-V Server Platform Distro

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.04-WU-poster.pdf). Sub. \#72. Thursday 15, at island 1.1 on S1. ([P1.1.04-Thu](#P1.1.04-Thu)).

**Yanjun Wu**, Institute of Software, Chinese Academy of Sciences. **Sheng Qu**, Institute of Software, Chinese Academy of Sciences. **Jingwei Wang**, Institute of Software, Chinese Academy of Sciences.

**Abstract**: With the release of the RISC-V Server Platform SPEC—and with strong backing from RISC-V International, RISE, and other leading industry players—standardized RISC-V servers, featuring cutting-edge IP such as SiFive’s P870 and Xiangshan’s Kunminghu, are set to debut around 2025 and 2026. As a dedicated server operating system, openEuler is ideally positioned to capitalize on this momentum. In our upcoming 26.03 release, openEuler will offer comprehensive support for the RISC-V Server Platform SPEC. Our clearly defined roadmap takes a phased approach to addressing both kernel and userspace requirements—beginning with robust kernel support by enabling the 6.6 LTS kernel to integrate ServerPlatform Generic Drivers and validating the rva23 standard, followed by targeted userspace enhancements. In this initial phase, our optimization efforts will focus on enhancing performance for compile and storage servers, while we actively collaborate with hardware vendors to establish a robust, unified kernel foundation.

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Towards Open-Source and Automatic Performance Characterization Hardware

[Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.05-WEINGARTEN-abstract.pdf). Sub. \#78. Thursday 15, at island 1.1 on S1. ([P1.1.05-Thu](#P1.1.05-Thu)).

**Matthew E. Weingarten**, Columbia University in the City of New York. **Tanvir Ahmed Khan**, University of Michigan.

**Abstract**: Performance characterization is the key to unlocking efficient utilization of the underlying processing system. Rapid developments in specialized computing and hardware/software co-design make performance characterization more challenging—as the underlying hardware changes, so must the performance monitoring hardware and the accompanying performance models. CPU vendors have successfully popularized the top-down micro-architectural analysis (TMA) methodology that is effective in identifying true bottlenecks in a processor while abstracting away the hardware implementation. Unfortunately, researchers and practitioners are often limited to open-source RISC-V processors that lack hardware support for TMA or any other systematic performance characterization methodology. Even the simple scalar in-order RocketCore has not implemented performance hardware capable of providing enough information to support TMA, let alone more complex Out-of-Order (OoO) and super scalar SonicBOOM core. Furthermore, the challenges of performance characterization are compounded by the ever-increasing heterogeneity and specialization of hardware, and a wholistic performance characterization methodology for an entire System-on-Chip (SoC) remains open-ended. Overall, the lack of hardware-supported performance characterization hamstrings the ability to evaluate new hardware designs, for performance tooling to adapt to modern hardware, or even programmers efficiently exploit the target hardware.

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### A Flexible and Portable Performance Evaluation Framework for Instruction Set Simulations

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.06-FOIK-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.06-FOIK-abstract.pdf). Sub. \#155. Thursday 15, at island 1.1 on S1. ([P1.1.06-Thu](#P1.1.06-Thu)).

**Conrad Foik**, Technische Universität München. **Karan Deepak Kedia**, Technische Universität München. **Robert Kunzelmann**, Infineon Technologies AG. **Daniel Mueller-Gritschneder**, TU Wien. **Ulf Schlichtmann**, Technical University of Munich.

**Abstract**: Simulation-based design space exploration plays a crucial part in the development of efficient processors for modern embedded systems. Common tools in this context are performance simulators, but these usually inflexibly target a single processor variant and cannot easily be combined with established simulation environments.

This paper presents a performance simulation framework that combines high accuracy and simulation speed with high flexibility and quick integration into existing simulation environments. It consists of a trace-based performance estimator, which can be adapted to new processor variants through code generation based on a simple structural description of the microarchitecture.

Applying our approach to the state-of-the-art CVA6 RISC-V application class processor shows an average relative error of 3.88% and an average simulation speed of 15 million instructions per second (MIPS) over the Embench benchmark suite.

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### The RISE Project: Advancing RISC-V Software

Sub. \#171. Thursday 15, at island 1.1 on S1. ([P1.1.07-Thu](#P1.1.07-Thu)).

**Nathan Egge**, Google. **Ludovic Henry**, Rivos.

**Abstract**: The RISC-V Software Ecosystem (RISE) Project is in high gear investing time and money on software to support RISC-V, including more than \$500K on contracts for further enhancements. This talk will highlight the way RISE prioritizes projects, and will outline some of our key achievements in the past year.

We have many ideas for further development and investments in 2025. Please join us for a deep dive into the latest developments shaping the RISC-V software ecosystem.

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Cloud-Based Binary Artifactory for RISC-V Software

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.08-TARIQ-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.08-TARIQ-abstract.pdf). Sub. \#174. Thursday 15, at island 1.1 on S1. ([P1.1.08-Thu](#P1.1.08-Thu)).

**Ali Mr. Tariq**, 10xEngineers. **Bilal Zafar**, 10xEngineers.

**Abstract**: A cloud-based application store for RISC-V can address the lack of precompiled binaries by providing up-to-date software. Using RISC-V cloud platforms like Cloud-V, automated CI pipelines ensure regular builds of essential applications, compilers, and CI tools. This reduces the need for developers to compile software, streamlining the ecosystem manually.

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Efficient debug and trace of RISC-V systems: a hardware/software co-design approach

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.09-LAZAR-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.09-LAZAR-abstract.pdf). Sub. \#180. Thursday 15, at island 1.1 on S1. ([P1.1.09-Thu](#P1.1.09-Thu)).

**Oana Alexandra Lazar**, Tessent Embedded Analytics. **Henrique Mendes**, Tessent Embedded Analytics. **Angelo Maldonado-Liu**, Tessent Embedded Analytics.

**Abstract**: The development risks of novel RISC-V solutions are exacerbated by bugs which are increasingly complicated to root-cause in ever-larger and more complex systems. Current debugging solutions are intrusive, impacting program execution timing and potentially hiding Heisenbugs. Run-stop-step debuggers alone lack the depth of visibility needed to root-cause complex and timing-sensitive bugs. We propose a complete end-to-end solution for highly efficient tracing, minimally invasive logging, and accelerated run-stop-step debugging of any RISC-V system, with out-of-the-box support for custom instructions. We demonstrate that an approach using both hardware and software to their full extent increases the efficiency of RISC-V debug and trace.

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Using trace based performance models to accelerate customer evaluations

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.10-GROVE-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.10-GROVE-abstract.pdf). Sub. \#194. Thursday 15, at island 1.1 on S1. ([P1.1.10-Thu](#P1.1.10-Thu)).

**SAMUEL Grove**, MIPS Tech LLC. **Jon Taylor**, Synopsys.

**Abstract**: Abstract Trace based models are higher levels of abstraction than true design data but incorporate descriptions of micro architectural features such as pipeline, bus or memory system behavior. They typically cannot execute code directly but take an execution trace from a model such as an ISS (which is architecturally accurate but does not have timing information). Together they can be used to estimate application performance before the design is complete. These complimentary technologies are extremely important in their own right, however, when used together create a powerful system that facilitates hardware-software co-design bringing software engineers and micro-architects together using the same technology that each discipline is already familiar with. Both the ISS and trace-based models are commonly developed ahead of RTL. In the context of IP licensing, customers can provide an execution trace to the IP company; the IP company does not need to share or productize the trace-based model, while the customer doesn’t need to share the software or source code for workloads. RISC-V international has a working group developing the STF trace format designed for exactly this use case.

This paper describes how MIPS and Synopsys have developed a flow that can easily be deployed and scaled to support customer evaluation of MIPS processors.

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### RISC-V Platform Firmware Implementation with UEFI and Its Future

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.11-YUAN-poster.pdf). Sub. \#197. Thursday 15, at island 1.1 on S1. ([P1.1.11-Thu](#P1.1.11-Thu)).

**Spike Yuan**, Alibaba Damo Academy. **Esther Zhang**, Alibaba Damo Academy. **Evan Chai**, Alibaba Damo Academy. **David Lee**, DAMO.

**Abstract**: RISC-V is facing the difficulty when entering the laptop or server market, where exists a set of mature standards, ACPI and UEFI for example. Unified Extensible Firmware Interface (UEFI) had been introduced for more than 20 years and was widely used in the laptop and server segment. This paper shows an implementation of UEFI in a RISC-V laptop product, The RuyiBook (JiaChen Version) powered by the TH1520 platform, which boots to Linux using a simplified UEFI solution. Also, it discusses the future firmware implementation in server segment, not only with UEFI solution, also the next generation firmware architecture, including Cloud Firmware or Universal Scalable Firmware (USF) or Universal Payload (UPL) Specification. These results and discussions pave the way for future RISC-V implementation and production in laptop and server markets.

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Development of Fedora Linux Distribution for RISC-V (RV64G) Architecture

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.12-SURENDRA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.1.12-SURENDRA-abstract.pdf). Sub. \#213. Thursday 15, at island 1.1 on S1. ([P1.1.12-Thu](#P1.1.12-Thu)).

**Billa Surendra**, Centre For Development of Advanced Computing.

**Abstract**: The continuous advancement of the RISC-V architecture introduces both opportunities and challenges, particularly for systems that do not include compressed instruction support (RV64G). Current Fedora Linux distributions predominantly target the RV64GC variant, leaving a significant gap in support for RV64G-based systems, which are essential for various research and development applications. The RISC-V community actively contributes to system software development, particularly in the Linux ecosystem. While much of the existing work is focused on enabling Fedora for the RV64GC profile, our research extends this effort by developing Fedora for sub-set profiles like RV64G. Many startups, academic researchers, and independent developers encounter difficulties in adopting mandated RISC-V profiles such as RV22 due to the complexity and cost associated with designing processors that incorporate multiple extensions. As hardware constraints and development costs rise, access to a functional Linux distribution across all RISC-V variants becomes increasingly critical. Our work addresses this need by delivering a Fedora version optimized for RV64G, facilitating broader adoption among those unable to develop or afford processors with mandatory extension support. Key aspects of this work involve building a scalable and reliable filesystem hierarchy, creating a cross-compilation toolchain, preparing and bootstrapping the target image, integrating a native GCC compiler, and utilizing the Koji build system to streamline package rebuilding. Additionally, we introduce a custom Python-based tool to enhance automation and reproducibility by efficiently managing Koji builds, ensuring uniformity in package deployment. Beyond addressing immediate software enablement challenges, this work establishes a solid foundation for advancing High-Performance Computing (HPC) on the RISC-V platform. By enabling a fully operational Fedora Server edition for RISC-V, our contributions support the widespread adoption of RISC-V in both research and enterprise domains. Furthermore, our development methodology follows the upstream-first policy, ensuring long-term maintainability and seamless integration into the Fedora ecosystem. This research not only expands Linux distribution support for various RISC-V profiles but also strengthens the RISC-V community by making Fedora more accessible across diverse hardware configurations.

[To page top](#summary) — [To posters at P1.1 (S1) on Thursday 15](#P1.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

On Thursday 15, at island P1.2 (S1)

------------------------------------------------------------------------

### Status of Fedora's RISC-V Porting Efforts

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.2.01-ABDURACHMANV-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.2.01-ABDURACHMANV-abstract.pdf). Sub. \#229. Thursday 15, at island 1.2 on S1. ([P1.2.01-Thu](#P1.2.01-Thu)).

**David Abdurachmanv**, Rivos Inc.. **Richard W.M. Jones**, Red Hat. **Andrea Bolognani**, Red Hat. **Kashyap Chamarthy**, Red Hat.

**Abstract**: Fedora Linux is a distribution known for its speed,wide content set, and support for multiple architectures. Efforts to enable RISC-V date to 2016, before physical hardware was available. At that time developers needed to run RISC-V on an FPGA or use emulation via software such as QEMU. Fedora contains tens of thousands of open source packages, many of which require architecture-specific code to perform optimally. The term “porting” here refers to building standard Fedora packages from their upstream sources for RISC-V, without custom patches. Today, at the start of 2025, a range of development boards are available. Fedora made significant leaps in its RISC-V enablement. In Jan 2025, Fedora 41 images were released, just 2 months after the official architectures (x86, Arm, et al) launched. This talks aims to give an update on a few topics: -What is the progress of porting Fedora’s packages for RISC-V (64 bit, RV64GC)? What are the challenges so far? • What does the future look like in terms of making RISC-V a primary architecture on Fedora? How complete and stable is the distribution? • What can you do when you don’t have hardware? What’s possible with QEMU’s emulated RISC-V, and wht are the supported “targets”, i.e. boards?

[To page top](#summary) — [To posters at P1.2 (S1) on Thursday 15](#P1.2-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### RISC-V Unified Database

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.2.02-HOWER-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.2.02-HOWER-abstract.pdf). Sub. \#173. Thursday 15, at island 1.2 on S1. ([P1.2.02-Thu](#P1.2.02-Thu)).

**Derek R. Hower**, Qualcomm. **Afonso Oliveira**, Synopsys.

**Abstract**: This work presents the RISC-V Unified Database (UDB), a step towards a unified, machine-readable source of truth for the RISC-V Specification. Currently, the RISC-V specification (including both ratified and de-facto parts) is scattered across multiple repositories and cloud storage files. Little of it is machine-readable, and in many cases information is duplicated in error-prone ways. This presents a barrier to further RISC-V growth as it is increasingly difficult to understand (and especially verify) the complex and growing specification. By gathering the specification in a single database, UDB provides the means to quickly find information and to generate artifacts directly from an authority. Towards that end, UDB currently includes over ten generators, including ones that produce ISA manuals, instruction and CSR indices, and an Instruction Set Simulator (ISS) – all from the same source. Though tremendous progress has been made in the last year, UDB is still a work in progress, and we are actively looking for increased community participation.

[To page top](#summary) — [To posters at P1.2 (S1) on Thursday 15](#P1.2-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Requirement of SPIKE API To Interact SPIKE data with SV/SUM Simulators For RISC-V Verification

Sub. \#106. Thursday 15, at island 1.2 on S1. ([P1.2.03-Thu](#P1.2.03-Thu)).

**Ranganath Kempanahally**, ChiplogicTech. **Shailesh D. Vasekar**, Chiplogictech.

**Abstract**: RISC-V IP verification with UVM/SV testbench with SPIKE to use as reference model to compare results against DUT output, requires to retrieve information from SPIKE such as resultant GPR, CSR, exceptions, interrupts and likewise for every instruction executed. There is requirement of SPIKE based API which uses SPIKE internal functions and interact with SV/UVM simulators using API and ultimately in SV/UVM testbenches. This article proposes to build SPIKE AND Systemverilog simulators data exchange API open source to boost RISC-V verification faster. T his will speed RISC-V verification and allow viability of SPIKE as reference model apart form simulator. Please find extended abstract pdf. Thanks

[To page top](#summary) — [To posters at P1.2 (S1) on Thursday 15](#P1.2-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

On Thursday 15, at island P1.3 (S1)

------------------------------------------------------------------------

### Building the RISC-V Education Ecosystem: A Systematic Educational Contents Design, Remote Laboratories, and Community-Driven Learning

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.01-LUO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.01-LUO-abstract.pdf). Sub. \#235. Thursday 15, at island 1.3 on S1. ([P1.3.01-Thu](#P1.3.01-Thu)).

**Yunxiang Luo**, The Institute of Software, Chinese Academy of Sciences**, ISCAS.. \*\*Fuyuan Zhang**, Programming Language and Compiler Technology Lab, Institute of Software, Chinese Academy of Sciences\*\*, ISCAS..

**Abstract**: The widespread adoption of RISC-V technology is facing with significant challenges, particularly the deficient talent cultivation system, which severely restricts its ecosystem growth. This paper investigates core issues in RISC-V education within China, including a shortage of skilled professionals, fragmented curriculum resources leading to low learning efficiency, scarcity of high-quality educational content, insufficient experimental equipment hindering programming capabilities growth, and a dispersed technical community with weak collaboration. To address these challenges, a systematic educational solution is proposed, encompassing tree dimensions: curriculum development, experiment environment support, and community engagement. In curriculum design, collaboration occurs with our laboratory, community developers, and university teachers to construct a multi-tiered course system spanning from foundational theories to cutting-edge technologies. A quality assurance mechanism is established through weekly technical seminars to form a course quality grading methodology ensuring continuous refinement of educational content. In order to address the challenge posed by hardware resource limitations, a strategy of integrating laboratory facilities across multiple regions in China has been adopted, with the aim of establishing a remote experimental environment that supports diverse RISC-V boards. This approach has the effect of significantly lowering barriers to RISC-V experimental environment access. Furthermore, an active community is cultivated, reaching over 30,000 participants through Bilibili and WeChat communities, regular offline technical workshops, and RISC-V programming competitions, fostering learner engagement and technical identity. The results demonstrate that this solution has produced over 1,000 original instructional videos, which have accumulated more than 1.3 million views. This systematic approach not only addresses critical educational gaps but also provides a scalable model for nurturing talent in emerging technologies, thereby accelerating the integration of RISC-V into innovation landscape.

[To page top](#summary) — [To posters at P1.3 (S1) on Thursday 15](#P1.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Learning by Puzzling: A Modular Approach to RISC-V Processor Design Education

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.02-SCHEIPEL-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.02-SCHEIPEL-abstract.pdf). Sub. \#6. Thursday 15, at island 1.3 on S1. ([P1.3.02-Thu](#P1.3.02-Thu)).

**Tobias Scheipel**, Graz University of Technology. **David Beikircher**, Graz University of Technology. **Florian Riedl**, Graz University of Technology.

**Abstract**: BlindReviewCPU is an innovative Open Educational Resource designed to teach RISC-V microcontroller design through a hands-on, modular approach. It consists of an extensive Instruction Guide document alongside an open-source template repository. This paper explores the didactic principles, technical foundation, and educational impact of BlindReviewCPU, emphasizing its open-source ethos and community contributions. We discuss the course design, evaluation framework, and student feedback, highlighting the jigsaw puzzle learning methodology with precompiled golden references. The work concludes with lessons learned and insights for future improvements and scalability in processor design education.

[To page top](#summary) — [To posters at P1.3 (S1) on Thursday 15](#P1.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### "One Student One Chip" Initiative: Learn to Build RISC-V Chips from Scratch with MOOC

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.03-YU-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.03-YU-abstract.pdf). Sub. \#50. Thursday 15, at island 1.3 on S1. ([P1.3.03-Thu](#P1.3.03-Thu)).

**Zihao Yu**, ICT, CAS. **Zeyu Gao**, ICT, CAS. **Xiaoke Su**, ICT, CAS.

**Abstract**: The “One Student One Chip” initiative has gone through six seasons. The initiative will guide students to design a RISC-V processor chip that can be taped out from scratch, run a simple operating system written by themselves and the real game “Legend of Sword and Fairy” on it and then complete the physical design process through open-sourced EDA tools. This helps students learn the entire process of processor chip design. This report will introduce the implementation of the “ One Student One Chip “ initiative and the results of open-source chip talent training.

[To page top](#summary) — [To posters at P1.3 (S1) on Thursday 15](#P1.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### WebRISC-V: A 64-bit RISC-V Pipeline Simulator for Computer Architecture Classes

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.04-GIORGI-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.04-GIORGI-abstract.pdf). Sub. \#215. Thursday 15, at island 1.3 on S1. ([P1.3.04-Thu](#P1.3.04-Thu)).

**Roberto Giorgi**, University of Siena. **Gianfranco Mariotti**, University of Siena.

**Abstract**: WebRISC-V is a web-based educational tool designed to simulate the pipelined execution of assembly programs according to the RV64IM specifications (64-bit RISC-V processor). The tool allows users to investigate pipeline stalls, understand the internal state of pipeline architectural blocks, and visualize the cycle-by-cycle execution of instructions. WebRISC-V is the first tool that executes directly in a web browser, providing a detailed pipeline execution for RISC-V processors. This paper describes the features of WebRISC-V, compares it with similar tools, and provides an example of its usage in investigating pipeline behavior.

[To page top](#summary) — [To posters at P1.3 (S1) on Thursday 15](#P1.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Leveraging RISC-V Vectorization: Accelerating Java Programs with TornadoVM and OCK

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.06-FUMERO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.06-FUMERO-abstract.pdf). Sub. \#29. Thursday 15, at island 1.3 on S1. ([P1.3.06-Thu](#P1.3.06-Thu)).

**Juan Fumero**, The University of Manchester. **Athanasios Stratikopoulos**, The University of Manchester. **Colin Davidson**, Codeplay Software Ltd.. **Harald van Dijk**, Codeplay Software Ltd.. **Uwe Dolinsky**, Codeplay Software Ltd.. **Michail Papadimitriou**, The University of Manchester. **Maria Xekalaki**, The University of Manchester. **Christos Kotselidis**, The University of Manchester.

**Abstract**: This paper presents an approach to accelerate Java applications on RISC-V processors equipped with vector extensions. The proposed approach utilizes a two-stage compilation chain composed of two open-source compilation frameworks.

The first compilation is performed by TornadoVM, a Java Framework that includes a Just-In-Time (JIT) compiler and a runtime system that translate Java Bytecode into OpenCL and SPIR-V and optimise runtime parameters. The second compilation is operated by the oneAPI Construction Kit (OCK), a programming framework that translates OpenCL and SPIR-V code into an efficient binary augmented with vector instructions for RISC-V CPUs.

Finally, we present a preliminary performance evaluation using matrix multiplication as a representative application. Results demonstrate a substantial performance improvement in the code generated when compared against functionally equivalent single-threaded and multi-threaded Java implementations, achieving speedups up to 33x and 4.6x respectively.

[To page top](#summary) — [To posters at P1.3 (S1) on Thursday 15](#P1.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Auto-re-vectorization into RISCV Vector Code, from Vector/SIMD Intrinsics Code Written for Other Architectures like x86 AVX or ARM Vector/Neon, Using LLVM Infrastructure

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.07-MATHILAKATH-PADINHAREPATT-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.07-MATHILAKATH-PADINHAREPATT-abstract.pdf). Sub. \#81. Thursday 15, at island 1.3 on S1. ([P1.3.07-Thu](#P1.3.07-Thu)).

**Nisanth Mathilakath Padinharepatt**, MIPS. **Sanket Lonkar**, MIPS.

**Abstract**: A RISCV processor with vector extensions demands efficient workload execution. Conventional approaches include: (1) compiling high-level C/C++ code using auto-vectorizing compilers (e.g., LLVM or GCC), (2) hand-optimizing performance-critical kernels using intrinsics or assembly, or (3) a hybrid of both—yielding the best binaries but requiring significant manual effort. Although auto-vectorization is fast, it often produces suboptimal code compared to what hand optimization can achieve. We propose an alternative: leverage existing hand-optimized kernels (originally developed for x86 AVX, ARM Neon, and other RISCV architectures) by generating compiler IR (e.g., LLVM IR) from these vector codes and then re-vectorizing it for the target processor using a tool like LLVM. This approach produces more optimal machine code than compiling high-level language code and yields structures that are easier to further hand-optimize. This also makes quick enablement of existing code bases in other ISA intrinsics on RISCV Vector Processors possible. In this paper, we detail our auto-re-vectorization method, its implementation, and present cycle-based performance comparisons against vector code generated from high-level language compilations and other existing approaches.

[To page top](#summary) — [To posters at P1.3 (S1) on Thursday 15](#P1.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Vectorization and Optimization of Gradient Boost Libraries for EUPilot VEC Chiplet

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.08-ATALAY-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.08-ATALAY-abstract.pdf). Sub. \#163. Thursday 15, at island 1.3 on S1. ([P1.3.08-Thu](#P1.3.08-Thu)).

**Ali Serdar Atalay**, AI4SEC OÜ. **Orkun Hasekioğlu**, TUBITAK Fundamental Sciences Research Institute. **Muhammed Enis Sen**, AI4SEC OÜ. **Şener Özönder**, Boğaziçi University.

**Abstract**: The increasing demand for efficient and accurate machine learning algorithms in various fields, including drug discovery, has led to a growing interest in optimizing gradient boost libraries for specialized hardware architectures. Various vectorization techniques, including loop unrolling to reduce overhead, data parallelism for simultaneous processing of multiple data elements, and instruction-level parallelism to execute multiple instructions per clock cycle, along with SIMD and SIMT, can be employed to enhance performance. By leveraging these vectorization techniques, XGBoost - CatBoost libraries are optimized to achieve significant performance gains on the EUPilot VEC chiplet, a cutting-edge, low-power, and highly scalable vector processing unit designed to accelerate machine learning workloads, which is a key component of the EUPilot Horizon Europe project, aiming to develop a scalable and energy-efficient computing platform. The optimized libraries are evaluated on a molecular binding dataset, where the goal is to predict the binding affinity of small molecules to target proteins. The optimized libraries demonstrate significant improvements in computational efficiency, enabling faster and more accurate predictions. Specifically, manual vectorization using intrinsics, as well as automated vectorization tools and techniques, are employed to optimize the computationally intensive loops in Gradient Boosting Algorithms. The optimized libraries for the EUPilot chiplet are compared to non-optimized versions, and the results are analyzed in terms of performance gain, accuracy, and computational efficiency.

[To page top](#summary) — [To posters at P1.3 (S1) on Thursday 15](#P1.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Powering Plasma-Physics with RISC-V vector extension: the case of Vlasiator

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.09-OLIVA-VIÑAS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.3.09-OLIVA-VIÑAS-abstract.pdf). Sub. \#64. Thursday 15, at island 1.3 on S1. ([P1.3.09-Thu](#P1.3.09-Thu)).

**Gerard Oliva Viñas**, Barcelona Supercomputing Center. **Pablo Vizcaino**, Barcelona Supercomputing Center. **Urs Ganse**, University of Helsinki. **Marta Garcia-Gasulla**, Barcelona Supercomputing Center. **Filippo Mantovani**, Barcelona Supercomputing Center.

**Abstract**: In this talk we will present the performance study and optimization of the Vlasiator plasma physics simulation on a RISC-V vector CPU. We aimed to improve computational efficiency by increasing vector length (VL) and refining memory access strategies. Initial adjustments expanded the loop size from 8 to 64 elements, enhancing performance but still far from the accelerator’s maximum potential of 256-element VL. We examined the challenges of adapting the GPU-optimized vlasiator_gpu branch for CPUs, where vectorization is constrained by the Vectorclass’s 64-element limit. Our benchmarking showed that unit-strided loads outperform indexed loads, providing a 2.5 X performance gain for larger cell sizes. Additional optimizations, including loop fusion and array reference passing, led to a 2.14 X speedup. This study offers key insights into optimizing scientific simulations on RISC-V, with an emphasis on maintaining portability.

[To page top](#summary) — [To posters at P1.3 (S1) on Thursday 15](#P1.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

On Thursday 15, at island P1.4 (S1)

------------------------------------------------------------------------

### Accelerating GenAI Workloads by Enabling RISC-V Microkernel Support in IREE

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.4.01-AHMAD-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.4.01-AHMAD-abstract.pdf). Sub. \#99. Thursday 15, at island 1.4 on S1. ([P1.4.01-Thu](#P1.4.01-Thu)).

**Adeel Ahmad**, 10xEngineers. **Nouman Amir**, 10xEngineers. **Ahmad Tameem Kamal**, 10xEngineers. **Bilal Zafar**, 10xEngineers. **Saad Bin Nasir**, 10xEngineers.

**Abstract**: This project aims to enable RISC-V microkernel support in the IREE Machine Learning Compiler. It includes enabling the lowering of the MLIR operations to IREE microkernel calls and implementing microkernel functions for RISC-V. A comprehensive analysis of RISC-V ISA would also be provided as part of the project to identify areas where it lags behind x86 and ARM when targeting GenAI models. This project is a work in progress, and hence, the proposed methodology is discussed in the extended abstract. We aim to improve the RISC-V software ecosystem and spark community interest in expanding RISC-V support in ML compilers and kernel libraries.

[To page top](#summary) — [To posters at P1.4 (S1) on Thursday 15](#P1.4-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### LLM-assisted Methodology for Embedded Software Performance Estimation on RISC-V

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.4.02-ZHANG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.4.02-ZHANG-abstract.pdf). Sub. \#49. Thursday 15, at island 1.4 on S1. ([P1.4.02-Thu](#P1.4.02-Thu)).

**Weiyan Zhang**, Researcher. **Muhammad Hassan**, University of Bremen/Cyber Physical Systems, DFKI. **Rolf Drechsler**, University of Bremen/DFKI.

**Abstract**: In this extended abstract, we present a methodology that combines a Large Language Model (LLM) with a traditional Machine Learning (ML) technique to estimate the performance of embedded software on RISC-V processors across different microarchitectures. In particular, we leverage a Retrieval-Augmented Generation (RAG)-based LLM to extract performance-related information from processor specifications and source code, while utilizing the predictive capabilities of ML models to create Predictive Models (PMs) for RISC-V processors. To demonstrate the effectiveness of our hybrid approach, we present results on the performance estimation of open-source benchmarks using the generated PMs, with open-source RISC-V-based Register Transfer Level (RTL) implementations as reference models. Our results demonstrate that our proposed LLM-assisted methodology provides highly accurate predictions in comparison with the state-of-the-art methodology.

[To page top](#summary) — [To posters at P1.4 (S1) on Thursday 15](#P1.4-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Improvements to RISC-V Vector code generation in LLVM

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.4.03-LAU-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P1.4.03-LAU-abstract.pdf). Sub. \#199. Thursday 15, at island 1.4 on S1. ([P1.4.03-Thu](#P1.4.03-Thu)).

**Luke Lau**, Igalia. **Alex Bradbury**, Igalia.

**Abstract**: LLVM has had stable support for the RISC-V vector extension for the past several releases, with both forms of autovectorization – the loop vectorizer and the SLP (superword-level-parallelism) vectorizer – enabled by default, as well as a rich set of C intrinsics for the RVV programming model. A key focus since then has been on improving generated code performance. This submission explains the changes made in the middle-end and backend that have delivered these gains and looks ahead to future work.

[To page top](#summary) — [To posters at P1.4 (S1) on Thursday 15](#P1.4-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

On Thursday 15, at island P2.1 (S2)

------------------------------------------------------------------------

### The Simulation-based Gold-Standard framework for verifying HDL branch predictors

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.01-THACKRAY-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.01-THACKRAY-abstract.pdf). Sub. \#37. Thursday 15, at island 2.1 on S2. ([P2.1.01-Thu](#P2.1.01-Thu)).

**Katy Thackray**, University of Cambridge. **Karl Mose**, Department of Computer Science and Technology, University of Cambridge.

**Abstract**: Faults in a branch predictor’s programming will not cause ISA tests to fail or the processor to deadlock, instead they are likely to cause subtle effects, such as underperformance. Exhaustive testing is near infeasible and low impact deviations from the desired functionality are likely to go undetected. Extremely rare cases could cause a context-sensitive branch predictor to strongly underperform. This paper presents a framework for testing branch predictors written in optimized HDL for RISC-V processors. The SGV framework can functionally verify a HDL branch predictor against a high level gold standard branch predictor efficiently using billions of trace instructions. A deviation from the outputs of the two models allow for an instant halt and internal state can be logged to trace the deviation. Verifying on a diverse set of traces can ensure with high confidence that the HDL model is functionally equivalent to the gold standard model. The framework is used to verify a TAGE based based branch predictor in Bluespec SystemVerilog.

[To page top](#summary) — [To posters at P2.1 (S2) on Thursday 15](#P2.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### FastISS RISC-V VP++: A Simulation Performance Evaluation of RVV Workloads

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.02-SCHLAEGL-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.02-SCHLAEGL-abstract.pdf). Sub. \#54. Thursday 15, at island 2.1 on S2. ([P2.1.02-Thu](#P2.1.02-Thu)).

**Manfred Schlaegl**, Johannes Kepler University. **Daniel Grosse**, Johannes Kepler University Linz.

**Abstract**: In this paper, we consider the SystemC-based open-source RISC-V VP++ with support for the RISC-V “V” Vector Extension (RVV), whose interpreter-based Instruction Set Simulator (ISS) has recently been significantly optimized (FastISS). While the original paper examined simulation performance gains using classical, non-vectorized workloads, this paper focuses on the gains on a workload vectorized using RVV. The experiments in this paper show a significant improvement in simulation performance by a factor of 2.65 for a vectorized workload. However, it is also shown that non-vectorized workloads can generally benefit more from the FastISS optimizations than vectorized workloads.

[To page top](#summary) — [To posters at P2.1 (S2) on Thursday 15](#P2.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Advanced Verification Suite for RISC-V Cores

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.03-TOKEZ-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.03-TOKEZ-abstract.pdf). Sub. \#57. Thursday 15, at island 2.1 on S2. ([P2.1.03-Thu](#P2.1.03-Thu)).

**Murat Tokez**, ELECTRAIC. **Merve Eyuboglu**, ELECTRAIC. **Ibrahim Ali Ahmed Mouamar**, ELECTRAIC. **Berna Ors**, ELECTRAIC. **Melike Atay Karabalkan**, ELECTRAIC.

**Abstract**: We have developed a verification enviroment called ElectraIC Advanced Verification Suite (EAVS) for verification of any RISC-V core. EAVS includes an Instruction Set Simulator (ISS), YAML configuration files, and a RISC-V Core UVM Testbench. The RISC-V Core UVM Testbench contains a RISC-V Core, referred to as the Design Under Test (DUT), along with an Instruction Generator, Compiler, and a RISC-V Core Base Test.

[To page top](#summary) — [To posters at P2.1 (S2) on Thursday 15](#P2.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Implementation of Branch Treatment Strategies in the Ripes RISC-V Simulator

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.04-ALFARO-CORTÉS-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.04-ALFARO-CORTÉS-abstract.pdf). Sub. \#61. Thursday 15, at island 2.1 on S2. ([P2.1.04-Thu](#P2.1.04-Thu)).

**Francisco J. Alfaro-Cortés**, Universidad de Castilla-La Mancha. **Silvia González-Rodríguez**, Universidad de Castilla-La Mancha. **Jesús Escudero-Sahuquillo**, Universidad de Castilla-La Mancha. **Rafael Rodríguez-Sánchez**, Universidad de Castilla-La Mancha.

**Abstract**: RISC-V is an open standard instruction set architecture (ISA) developed at the University of Berkeley as an alternative to proprietary ISAs, like x86 and ARM. Its main goal is to provide a flexible and cost-effective platform for companies, universities, and developers to design processors without licensing fees. Additionally, it supports customization and performance optimization through specialized instructions.

In education, simulators are key tools for understanding processor operation, showing details of instruction cycles and memory. The Ripes simulator, being open source, encourages customization and collaboration.

This work enhances Ripes by adding a branch implementation and new branch resolution strategies. The interface has also been improved to simplify option selection, making it a complete and more useful tool for teaching.

[To page top](#summary) — [To posters at P2.1 (S2) on Thursday 15](#P2.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### RISCV-PySim: A Modular and Flexible Python-Based RISC-V Simulator

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.05-ROJAS-MORALES-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.05-ROJAS-MORALES-abstract.pdf). Sub. \#69. Thursday 15, at island 2.1 on S2. ([P2.1.05-Thu](#P2.1.05-Thu)).

**Carlos Rojas Morales**, Barcelona Supercomputing Center. **Víctor Asanza**, Barcelona Supercomputing Center. **Julian Pavon**, Barcelona Supercomputing Center. **Ivan Vargas Valdivieso**, Barcelona Supercomputing Center. **Erick Brandon Cureño Contreras**, Centro de Investigación en Computación, Instituto Politécnico Nacional. **Adrian Cristal**, Barcelona Supercomputing Center.

**Abstract**: This work presents RISCV-PySim, a Python-based simulator for RISC-V processors, designed to incorporate and evaluate custom instructions, facilitating the development of Domain-Specific Hardware Accelerator (DSHA) accelerators. As a case study, matrix multiplication kernels were implemented using scalar, vectorized, and systolic array approaches with custom instructions. To estimate the speed-up between these three implementations, we implemented a simplified model of a in-order CPU and compared the efforts to do the same using the state-of-the-art gem5 simulator. RISCV-PySim simulator is particularly useful for verifying the correctness and semantics of new custom instructions, a task that would otherwise require significant overhead in the state-of-the-art simulators. Additionally, its modular architecture also enables seamless integration with various performance models, allowing adapting to specific design needs.

[To page top](#summary) — [To posters at P2.1 (S2) on Thursday 15](#P2.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Co-simulation and architectural exploration with PolarFire SoC and Renode

Sub. \#210. Thursday 15, at island 2.1 on S2. ([P2.1.07-Thu](#P2.1.07-Thu)).

**Piotr Zierhoffer**, Antmicro. **Cyril Jean**, Microchip Technology.

**Abstract**: Since its release in 2020, Microchip PolarFire SoC, the first widely available Linux-capable multicore RISC-V platform, has been supported by a wide variety of open-source efforts aimed to make it more accessible and versatile in critical industries such as space, automotive and industrial applications. Even before it reached the global market, developers were able to use Renode, Antmicro’s open-source simulation framework, to develop, debug and test software targeting PolarFire SoC. With a capable FPGA on board, PolarFire SoC opens a range of possibilities for system designers and engineers, but it also calls for versatile tools that would support development and making architectural choices. In this joint talk Microchip and Antmicro will present the latest open-source developments in co-simulation support, combining the functional Renode simulation and cycle-accurate RTL simulation. We will focus on the newly added support for the popular DPI interface, and will present live how to create a simple co-simulation setup.

[To page top](#summary) — [To posters at P2.1 (S2) on Thursday 15](#P2.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### RISC-V support implementation for ORC (Oil Runtime Compiler)

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.08-WASIL-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.1.08-WASIL-abstract.pdf). Sub. \#44. Thursday 15, at island 2.1 on S2. ([P2.1.08-Thu](#P2.1.08-Thu)).

**Filip Wasil**, Samsung. **Maksymilian Knust**, Samsung.

**Abstract**: Adding efficient RVV-based implementation for dynamic code generation in ORC (Optimized Inner Loops Runtime Compiler) project. That includes assembly code generation along with raw byte stream generation from ORC assembly source code.

[To page top](#summary) — [To posters at P2.1 (S2) on Thursday 15](#P2.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

On Thursday 15, at island P2.2 (S2)

------------------------------------------------------------------------

### Snooper: A Flexible Tracing Solution for Fast Simulation and Analysis in RISC-V

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.01-MONSERRAT-CAMPANELLO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.01-MONSERRAT-CAMPANELLO-abstract.pdf). Sub. \#66. Thursday 15, at island 2.2 on S2. ([P2.2.01-Thu](#P2.2.01-Thu)).

**Santiago Monserrat Campanello**, Barcelona Supercomputing Center. **Julian Pavon Rivera**, Barcelona Supercomputing Center. **Adrian Cristal**, Barcelona Supercomputing Center.

**Abstract**: Hardware simulation and modeling are essential for computer architecture research, enabling early-stage evaluation without full hardware implementation. Trace-based simulation tools are advantageous for quickly modeling CPU and memory system performance. However, a proper instruction tracing tool for the RISC-V ISA is currently missing. We present Snooper, a fast and flexible RISC-V instruction tracer built as a QEMU TCG plugin. Snooper extracts information (e.g., source/destination registers) per executed instruction and generates customizable trace files, making it compatible with state-of-the-art trace-based CPU simulators. Supporting both user-mode and full-system execution, Snooper enables in-depth RISC-V analysis, including OS-level evaluation. We validate the traces generated by Snooper using ChampSim. On average, Snooper+ChampSim achieves an average 9% modeling error compared to a RTL Out-of-order CPU running in an FPGA.

[To page top](#summary) — [To posters at P2.2 (S2) on Thursday 15](#P2.2-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Software-Hardware Co-Verification for Traditional Verification Frameworks

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.02-SONG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.02-SONG-abstract.pdf). Sub. \#73. Thursday 15, at island 2.2 on S2. ([P2.2.02-Thu](#P2.2.02-Thu)).

**Fangyuan Song**, Institute of Computing Technology, Chinese Academy of Sciences. **Yunlong Xie**, Institute of Computing Technology, CAS. **Jincheng Liu**, Institute of Computing Technology, Chinese Academy of Sciences.

**Abstract**: The Universal Verification Methodology (UVM) dominates hardware verification workflows, yet its dependency on SystemVerilog (SV) inherently isolates it from modern software ecosystems—such as Python-based AI/ML tools (e.g., PyTorch), DevOps frameworks (e.g., pytest for automated testing), and cloud platforms for distributed simulation. This isolation restricts the adoption of advanced methodologies, creating inefficiencies in collaborative RISC-V SoC validation. This paper proposes a novel methodology that encapsulates UVM environments and RTL designs as reusable software packages, By integrating Transaction-Level Modeling (TLM), UVM Connect (UVMC), and SWIG, we provide control and data pathways for cross-language verification. The data pathway serializes UVM transactions into byte streams for transmission to SystemVerilog (SV), while SWIG enables parsing and reconstruction in high-level languages (e.g., Python). The control pathway exposes a step() method to drive UVM clocks programmatically. Experimental results on RISC-V cores demonstrate 45% fewer verification code lines, 50% faster debug cycles, and seamless bidirectional transaction flows between UVM and Python. This approach bridges hardware verification and software-driven workflows, aligning with RISC-V’s open-source ecosystem goals.

[To page top](#summary) — [To posters at P2.2 (S2) on Thursday 15](#P2.2-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### On Benefits of Modeling the HPDcache in LNT

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.03-ASSOUMANI-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.03-ASSOUMANI-abstract.pdf). Sub. \#104. Thursday 15, at island 2.2 on S2. ([P2.2.03-Thu](#P2.2.03-Thu)).

**Zachary Assoumani**, INRIA. **César Fuguet**, INRIA. **Radu Mateescu**, INRIA. **Wendelin Serwe**, INRIA.

**Abstract**: Stepping from natural language towards modern formal languages such as LNT is beneficial for specifying hardware architectures. We illustrate this on the HPDcache, the informal specification of which contains numerous fragments in pseudo-code. Due to the syntactical similarities between the latter and LNT, modeling the HPDcache’s informal specification in LNT was greatly facilitated. The CADP tools supporting LNT enabled us to spot an error in the informal specification of the HPDcache, which might have led to a violation of the memory consistency rules of the RISC-V.

[To page top](#summary) — [To posters at P2.2 (S2) on Thursday 15](#P2.2-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Unleashing the Power of RISC-V E-Trace with a Highly Efficient Software Decoder

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.04-ZAK-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.04-ZAK-abstract.pdf). Sub. \#128. Thursday 15, at island 2.2 on S2. ([P2.2.04-Thu](#P2.2.04-Thu)).

**Marcel Zak**, Siemens EDA. **Mat O’Donnell**, Siemens EDA. **Vivek Chickermane**, Siemens EDA.

**Abstract**: Debugging program misbehaviour that impacts large scale deployment of highly connected systems requires a robust debug infrastructure to monitor the instructions, data, and transactions between system components. The rapid adoption of RISC-V processors in mission critical applications has compelled system designers to rely on embedded trace monitors based on the RISC-V E-Trace specification to collect instruction trace data to analyse the trajectory of the transactions involving the CPU, memory, I/Os, peripherals, and other sub-systems. In this paper we describe a highly efficient software E-Trace Decoder that allows trace data to be non-intrusively captured at-speed. We describe two case studies to highlight the power of this implementation and provide quantitative data to show the efficiency of this implementation.

[To page top](#summary) — [To posters at P2.2 (S2) on Thursday 15](#P2.2-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Modular SAIL: dream or reality?

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.05-KOURZANOV-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.05-KOURZANOV-abstract.pdf). Sub. \#167. Thursday 15, at island 2.2 on S2. ([P2.2.05-Thu](#P2.2.05-Thu)).

**Peter Kourzanov**, IMEC. **Anmol Anmol**, imec, Kapeldreef 75, 3001, Leuven, Belgium.

**Abstract**: In order to truly benefit from RISC-V ISA modularity, the community has to address the issue of compositionality, going beyond modules at the specification level covering larger subsets of the RISC-V development flow including emulation, simulation and verification. In this paper we introduce modular SAIL, an experiment to inject compositionality into the SAIL-RISCV golden model. We show that it is, in principle, not difficult to adapt the SAIL-RISCV flow (and ideally the SAIL compiler itself ) to support modules at the emulator level. We back our findings by a comparative study of the resulting pluggable emulator’s performance using both static and dynamic binding, which both exhibit same functional behavior as the original monolithic emulator (aka \[ISS\]).

[To page top](#summary) — [To posters at P2.2 (S2) on Thursday 15](#P2.2-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Who tests the TestRIG? Tooling for randomised tandem verification

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.06-RUGG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.06-RUGG-abstract.pdf). Sub. \#193. Thursday 15, at island 2.2 on S2. ([P2.2.06-Thu](#P2.2.06-Thu)).

**Peter Rugg**, University of Cambridge. **Alexandre Joannou**, University of Cambridge. **Jonathan Woodruff**, University of Cambridge. **Franz A. Fuchs**, University of Cambridge. **Simon W. Moore**, University of Cambridge.

**Abstract**: TestRIG is a framework to test RISC-V implementations first presented at the RISC-V Summit in Zurich in

1.  Since then, the ecosystem has grown, with multiple new implementations integrated and industrial interest. This presentation discusses some improvements to the ecosystem, including mutation-based coverage tooling, features for generating static test suites, and a single-implementation mode that enables more traditional fuzzing. The developments are motivated by testing the Toooba processor, including the CHERI security extensions. This work helps to evolve TestRIG into a tool suite that can increasingly improve assurance in RISC-V designs.

[To page top](#summary) — [To posters at P2.2 (S2) on Thursday 15](#P2.2-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Toffee: an Efficient and Flexible Python Testing Framework for Chip Verification

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.07-LIU-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.2.07-LIU-abstract.pdf). Sub. \#208. Thursday 15, at island 2.2 on S2. ([P2.2.07-Thu](#P2.2.07-Thu)).

**Jincheng Liu**, Institute of Computing Technology, Chinese Academy of Sciences. **Zhicheng Yao**, Institute of Computing Technology, Chinese Academy of Sciences. **Yunlong Xie**, Institute of Computing Technology, Chinese Academy of Sciences. **Zechen Yang**, University of Chinese Academy of Sciences. **Junyue Wang**, Institute of Computing Technology, Chinese Academy of Sciences. **Xiao Chen**, Institute of Computing Technology, Chinese Academy of Sciences. **Kan Shi**, Institute of Computing Technology, Chinese Academy of Sciences. **Sa Wang**, Institute of Computing Technology, Chinese Academy of Sciences. **Yungang Bao**, Institute of Computing Technology, Chinese Academy of Sciences.

**Abstract**: Chip verification accounts for up to 60% of development efforts, mainly due to time-consuming simulation and debugging. Furthermore, traditional chip verification methodologies are typically disconnected from modern software testing tools, limiting efficiency and flexibility. This paper proposes a Python testing framework called Toffee, which incorporates core technological solutions such as the async-discrete model, asynchronous function modeling, and the hook-enabled reference model mechanisms. Experimental results demonstrate that, compared to traditional verification frameworks, tasks completed with Toffee can reduce the LOC by up to 86.3%, cut execution time by up to 92.58%, and integrate more effectively with modern software testing tools

[To page top](#summary) — [To posters at P2.2 (S2) on Thursday 15](#P2.2-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

On Thursday 15, at island P2.3 (S2)

------------------------------------------------------------------------

### RuyiSDK - A Integrated and Customizable Toolkit for RISC-V Software Development

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.01-CAI-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.01-CAI-abstract.pdf). Sub. \#12. Thursday 15, at island 2.3 on S2. ([P2.3.01-Thu](#P2.3.01-Thu)).

**Weilin Cai**, Institute of Software, Chinese Academy of Sciences**, ISCAS.. \*\*Chen Yi Ling**, Southwest University of Science and Technology. **Yunxiang Luo**, The Institute of Software, Chinese Academy of Sciences\*\*, ISCAS..

**Abstract**: The RISC-V instruction set’s design has given rise to a highly diverse ecosystem. However, the introduction of vendor-defined extensions has the potential to lead to fragmentation, creating challenges for developers in managing toolchains and adapting software. This paper presents RuyiSDK which is a comprehensive solution tailored for RISC-V developers. It is designed to address these challenges by integrating existing foundational software, promoting the adaptation of unsupported applications, and cultivating a vibrant developer community. RuyiSDK offers a package index that consolidates toolchains, emulators, and more, along with profile files that describe how to perform cross-platform builds, as well as software and RISC-V boards co-development. A key component of RuyiSDK is the Package Manager, which not only inherits the capabilities of traditional package managers but also incorporates advanced features such as virtual environment creation, device provisioning, and plugin support. The Package Manager transparently applies virtual environment profiles to the corresponding toolchains by reading the package index. Users only need to specify the target development board, without needing to manage toolchain differences manually. The device provisioning feature provides interactive guidance for keeping system images up to date for specific development boards, while test reports offer a certain level of quality assurance. The plugin system enables vendors and users to extend the Package Manager with custom features, thereby making it adaptable to various workflows. By providing a flexible, efficient, and transparent cross-platform development environment, RuyiSDK empowers developers to focus on innovation, thereby unlocking the full potential of RISC-V hardware while mitigating ecosystem fragmentation.

[To page top](#summary) — [To posters at P2.3 (S2) on Thursday 15](#P2.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Enabling RISC-V CI in Open-Source Projects: Challenges and Solutions

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.02-PIKULA-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.02-PIKULA-abstract.pdf). Sub. \#24. Thursday 15, at island 2.3 on S2. ([P2.3.02-Thu](#P2.3.02-Thu)).

**Marek Pikula**, Samsung R&D Institute Poland.

**Abstract**: The adoption of RISC-V as a viable architecture for open-source software development is gaining traction. However, a major challenge remains: ensuring continuous integration (CI) support for RISC-V in upstream projects. At (redacted), we addressed this issue by enabling RISC-V CI for several Freedesktop.org (FDO) projects, including Pixman and GStreamer Orc, and we are currently extending our work to the Opus codec. This work presents our approach to enabling RISC-V CI in FDO projects, addressing the challenges of testing architecture-specific optimizations without native hardware support. We detail our implementation of Docker-based GitLab runners with QEMU emulation, enabling automated multi-architecture testing while minimizing infrastructure overhead. Our work not only enhances software quality by enabling automated testing for RISC-V but also provides a framework for future contributions to seamlessly integrate RISC-V into open-source CI ecosystems.

[To page top](#summary) — [To posters at P2.3 (S2) on Thursday 15](#P2.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Enhancing EDA Physical Synthesis Workflows with najaeda for the RISC-V Ecosystem

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.03-ALEXANDRE-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.03-ALEXANDRE-abstract.pdf). Sub. \#132. Thursday 15, at island 2.3 on S2. ([P2.3.03-Thu](#P2.3.03-Thu)).

**Christophe Alexandre**, keplertech.io. **Noam Cohen**, keplertech.io.

**Abstract**: The RISC-V open-source hardware movement has created new opportunities for small and medium-sized businesses, removing traditional barriers to entry in the semiconductor industry. However, the high cost of proprietary EDA tools remains a significant challenge, limiting access for both industry and academia. To fully unlock the potential of open-source hardware, the RISC-V ecosystem requires open-source EDA solutions that are scalable and efficient. najaeda is a robust framework designed for post-synthesis EDA algorithm development, offering high-capacity hierarchical netlist processing and seamless integration into the open-source EDA ecosystem. This presentation explores najaeda’s data structures, Python-based APIs, and practical applications, demonstrating how it enhances netlist exploration, Engineering Change Order (ECO) transformations, and EDA prototyping. We will showcase an example of najaeda’s netlist optimization techniques, specifically Constant Propagation and Dead Logic Elimination, applied to medium-to-large RISC-V designs. Unlike traditional flat synthesis approaches, which dominate open-source workflows, najaeda preserves design hierarchy, ensuring better algorithmic performance, improved user guidance in downstream tools, and enhanced data fidelity. Additionally, by maintaining structural integrity, najaeda enables integration with Python-based data science frameworks like Pandas and PyTorch, paving the way for AI-driven EDA optimizations. This work highlights najaeda as a key enabler of scalable, industrial-grade open-source EDA, helping the RISC-V community develop high-performance designs without reliance on proprietary tools.

[To page top](#summary) — [To posters at P2.3 (S2) on Thursday 15](#P2.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### SoC Studio: A User-Centric Framework for Custom System-on-Chip Design, Emulation, and AI Integration

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.04-BAIG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.04-BAIG-abstract.pdf). Sub. \#138. Thursday 15, at island 2.3 on S2. ([P2.3.04-Thu](#P2.3.04-Thu)).

**Shayan Hassan Baig**, Usman Institute of Technology. **Shahzaib Kashif**, Usman Institute of Technology. **Dr. Ali Ahmed**, Usman Institute of Technology. **Dr. Farhan Ahmed Karim**, Usman Institute of Technology.

**Abstract**: Modern System-on-Chip (SoC) design demands flexible tools to bridge the gap between conceptualization and implementation. This paper introduces SoC Studio, an innovative application enabling users to configure, simulate, and emulate custom SoC designs through an intuitive interface. SoC Studio automates customized SoC Register-Transfer Level (RTL) code generation, simulator generation, FPGA bitstream compilation, and simulation workflows. Unique to SoC Studio is its support for both bare-metal software execution and ONNX-based AI model deployment on accelerator-enabled designs on the cloud. The framework further provides FPGA emulation on cloud or local hardware, alongside real-time power-performance-area (PPA) metrics and resource utilization analysis. By democratizing SoC development, SoC Studio reduces design cycles and empowers non-experts to prototype heterogeneous architectures efficiently.

[To page top](#summary) — [To posters at P2.3 (S2) on Thursday 15](#P2.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Croc: An End-to-End Open-Source Extensible RISC-V MCU Platform to Democratize Silicon

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.05-SAUTER-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.05-SAUTER-abstract.pdf). Sub. \#142. Thursday 15, at island 2.3 on S2. ([P2.3.05-Thu](#P2.3.05-Thu)).

**Philippe Sauter**, IIS, ETH Zürich. **Thomas Emanuel Benz**, ETH Zurich. **Paul Scheffler**, Integrated Systems Laboratory, ETH Zurich. **Hannah Pochert**, IIS, ETH Zürich. **Luisa Wüthrich**, IIS, ETH Zürich. **Martin Povišer**, Indepdent Contractor. **Beat Muheim**, DZ, ETH Zürich. **Frank Gurkaynak**, ETH Zurich. **Luca Benini**, Università di Bologna and ETH Zurich.

**Abstract**: Ensuring a continuous and growing influx of skilled chip designers and a smooth path from education to innovation are key goals for several national and international “Chips Acts”. Silicon democratization can greatly benefit from end-to-end (from silicon technology to software) free and open-source (OS) platforms. We present Croc, an extensible RISC-V microcontroller platform explicitly targeted at hands-on teaching and innovation. Croc features a streamlined OS synthesis and an end-to-end OS implementation flow, ensuring full, unconstrained access to the design, the design automation tools, and the implementation technology. Croc uses the industry-proven, open-source CVE2 core, implementing the RV32I(EMC) instruction set architecture (ISA), enabling students to define and implement their own ISA extensions. MLEM, a tapeout of Croc in IHP’s open 130 nm node completed in 8 weeks by a team of just two students, demonstrates the platform’s viability for hands-on teaching in schools, universities, or even on a self-education path. In spring 2025, ETH Zurich will utilize Croc for its curricular VLSI class, involving up to 80 students, producing up to 40 OS application-specific integrated circuit layouts, and completing up to five student-led system-on-chip tapeouts. The lecture notes and exercises are already available under a Creative Commons license.

[To page top](#summary) — [To posters at P2.3 (S2) on Thursday 15](#P2.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Towards Efficient Modeling and Validation of Scalable Chiplet-based Platforms

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.06-MOUHAGIR-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P2.3.06-MOUHAGIR-abstract.pdf). Sub. \#185. Thursday 15, at island 2.3 on S2. ([P2.3.06-Thu](#P2.3.06-Thu)).

**Ayoub Mouhagir**, CEA LIST. **Fatma Jebali**, CEA LIST. **Oumaima Matoussi**, CEA LIST. **Caaliph Andriamisaina**, CEA, LIST. **Anthony Philippe**, CEA LIST.

**Abstract**: Chiplet-based architectures offer a scalable and modular approach to SoC design. However, ensuring system modeling, validation, and performance assessment remains a challenge. To address this, a high-level modeling approach is being developed, combining QEMU-based functional modeling with ML-driven performance analysis and formal timing validation. This hybrid virtual prototyping method enables efficient design exploration andHW/SW co-validation.

[To page top](#summary) — [To posters at P2.3 (S2) on Thursday 15](#P2.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Developing RISC-V Cores with Python

Sub. \#231. Thursday 15, at island 2.3 on S2. ([P2.3.07-Thu](#P2.3.07-Thu)).

**Rob Taylor**, ChipFlow.

**Abstract**: In this talk I will give an overview of Amaranth, a Python-embedded HDL, and demonstrate some of the latest developments and their use, including:

- The new core library: datatypes, interface definition, streaming abstractions, and metadata
- VSCode based debugger and waveform viewer”

[To page top](#summary) — [To posters at P2.3 (S2) on Thursday 15](#P2.3-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

On Thursday 15, at island P3.1 (S3)

------------------------------------------------------------------------

### Design Exploration of RISC-V Soft-Cores through Speculative High-Level Synthesis

[Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.01-LEOTHAUD-abstract.pdf). Sub. \#42. Thursday 15, at island 3.1 on S3. ([P3.1.01-Thu](#P3.1.01-Thu)).

**Dylan Leothaud**, Univ Rennes, IRISA. **Jean-Michel Gorius**, Univ Rennes, CNRS, Inria, IRISA. **Simon Rokicki**, Irisa. **Steven Derrien**, UniversitÃ© de Bretagne Occidentale/Lab-STICC.

**Abstract**: The RISC-V ecosystem is quickly growing and has gained a lot of traction in the FPGA community, as it permits free customization of both ISA and micro-architectural features. However, the design of the corresponding micro-architecture is costly and error-prone. We address this issue by providing a flow capable of automatically synthesizing pipelined micro-architectures directly from an Instruction Set Simulator in C/C++. Our flow is based on HLS technology and bridges part of the gap between Instruction Set Processor design flows and High-Level Synthesis tools by taking advantage of speculative loop pipelining. Our results show that our flow is general enough to support a variety of ISA and micro-architectural extensions, and is capable of producing circuits that are competitive with manually designed cores.

[To page top](#summary) — [To posters at P3.1 (S3) on Thursday 15](#P3.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Work-In-Progress: Accelerating Numpy With OpenBLAS For Open-Source RISC-V Chips

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.01-KOENIG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.01-KOENIG-abstract.pdf). Sub. \#160. Thursday 15, at island 3.1 on S3. ([P3.1.01-Thu](#P3.1.01-Thu)).

**Cyril Koenig**, ETH Zurich. **Enrico Zelioli**, ETH Zurich. **Frank Gurkaynak**, ETH Zurich. **Luca Benini**, Università di Bologna and ETH Zurich.

**Abstract**: RISC-V allows for building general-purpose computing platforms with programmable accelerators around a single open-source ISA. However, leveraging heterogeneous SoCs within high-level applications is a tedious task. In this preliminary work, we modify the OpenBLAS library to offload selected linear kernels to a programmable manycore accelerator (PMCA) using OpenMP. By linking the Python package Numpy against this library, we enable acceleration of high-level applications. We target an open-source heterogeneous System-on-Chip with a rv64g Linux capable host and a rv32imafd PMCA. Using this platform emulated on FPGA, and the presented software stack, we can accelerate Phyton applications with linear algebra operators like matrix multiplication.

[To page top](#summary) — [To posters at P3.1 (S3) on Thursday 15](#P3.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### CVA6 Design Space Exploration on Agilex 7 FPGA

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.02-GONZALEZ-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.02-GONZALEZ-abstract.pdf). Sub. \#45. Thursday 15, at island 3.1 on S3. ([P3.1.02-Thu](#P3.1.02-Thu)).

**Angela Gonzalez**, PlanV. **Mustafa Karadayi**, PlanV. **Franck Jeulin**, Thales Group. **Christophe Biquard**, Thales Research & Technology. **Jerome Quevremont**, Thales Research & Technology.

**Abstract**: CVA6 offers a wide range of configuration parameters that permit to tailor the core to different applications. However, the vast number of existing parameters can be overwhelming, making it difficult to know where to start from, or which are the right choices to make. This work presents the results of design space exploration of CVA6 focusing on FPGA targets, in particular, on the Agilex 7 platform from Altera. Starting from the existing FPGA configuration from OpenHW, we explore two orthogonal directions: (i) maximizing performance and (ii) minimizing resources. We show the results achieved for different configurations, providing insights on the impact of different parameters (e.g. memory architecture, extensions, etc.) Among a variety of combinations, we find a sweet-spot that permits to achieve 30% performance improvement together with 50% reduction of registers, compared to the existing FPGA configuration which is primarily optimized for Xilinx. With this example and other exploratory results, this work aims at simplifying the initial choices in the configuration of new designs based on CVA6.

[To page top](#summary) — [To posters at P3.1 (S3) on Thursday 15](#P3.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Fused-Tiled Layers: Minimizing Data Movement on RISC-V SoCs with Software-Managed Caches

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.02-JUNG-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.02-JUNG-abstract.pdf). Sub. \#94. Thursday 15, at island 3.1 on S3. ([P3.1.02-Thu](#P3.1.02-Thu)).

**Victor J. B. Jung**, ETH Zurich. **Alessio Burrello**, Politecnico di Torino and UniversitÃ  di Bologna. **Francesco Conti**, University of Bologna. **Luca Benini**, Università di Bologna and ETH Zurich.

**Abstract**: The success of Deep Neural Networks (DNNs) and their high computational requirements pushed for large codesign efforts aiming at DNN acceleration. Since DNNs can be represented as static computational graphs, static memory allocation and tiling are two crucial optimizations. Hence, System-on-chips (SoCs) specialized for DNN acceleration commonly features a multi-level software-managed memory hierarchy. In such architecture, layer-wise tiling, i.e., splitting each layer into multiple sub-nodes, is commonly used; however, while reducing memory occupation, it can increase the total memory transfer, ultimately causing costly off-chip memory copies, which impact energy efficiency and create memory bottlenecks. This work proposes Fused-Tiled Layers (FTL), a novel algorithm for automatic fusion between tiled layers. We leverage the flexibility and efficiency of a RISC-V (RV32) heterogeneous SoC to integrate FTL in an open-source deployment framework, which we tune for RISC-V targets. We demonstrate that FTL brings up to 60.1% runtime reduction for a typical Multi-Layer Perceptron (MLP) stage of Vision Transformers (ViTs) due to the reduction of off-chip transfer and on-chip data movement by 47.1 %.

[To page top](#summary) — [To posters at P3.1 (S3) on Thursday 15](#P3.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Instruction Fusion Limit Study for RISC-V

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.03-HO-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.03-HO-abstract.pdf). Sub. \#65. Thursday 15, at island 3.1 on S3. ([P3.1.03-Thu](#P3.1.03-Thu)).

**Elizabeth Ho**, University of Cambridge. **Jonathan Woodruff**, University of Cambridge.

**Abstract**: This paper explores the limits of instruction fusion for RISC-V. We characterise instruction fusion rules and algorithms in a general framework, demonstrating a reduction in effective instruction count by over 50%.

[To page top](#summary) — [To posters at P3.1 (S3) on Thursday 15](#P3.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Programming RISC-V accelerators via Fortran

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.03-BROWN-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.03-BROWN-abstract.pdf). Sub. \#166. Thursday 15, at island 3.1 on S3. ([P3.1.03-Thu](#P3.1.03-Thu)).

**Nick Brown**, EPCC at the University of Edinburgh.

**Abstract**: A range of RISC-V based accelerators are available and coming to market, and there is strong potential for these to be used for High Performance Computing (HPC) workloads. However, such accelerators tend to provide bespoke programming models and APIs that require codes to be rewritten. In scientific computing, where many of the simulation code are highly complex, extensive, and written in Fortran, this is not realistic. In this extended abstract we present an approach that enables driving such architectures via Fortran, avoiding code redevelopment.

[To page top](#summary) — [To posters at P3.1 (S3) on Thursday 15](#P3.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Efficient Trace for RISC-V: Design, Evaluation, and Integration in CVA6

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.04-LAGHI-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.04-LAGHI-abstract.pdf). Sub. \#165. Thursday 15, at island 3.1 on S3. ([P3.1.04-Thu](#P3.1.04-Thu)).

**Umberto Laghi**, University of Bologna. **Simone Manoni**, University of Bologna. **Emanuele Parisi**, Universita’ di Bologna. **Andrea Bartolini**, University of Bologna.

**Abstract**: In this work, we present the design and evaluation of a Processor Tracing System compliant with the RISC-V Efficient Trace specification for Instruction Branch Tracing. We integrate our system into the host domain of a state-of-the-art edge architecture based on CVA6. The proposed Tracing System introduces a total overhead of 9.2% in terms of resource utilization on a Xilinx VCU118 FPGA on the CVA6 subsystem while achieving an average compression rate of 95.1\\ on platform-specific tests, compared to tracing each full opcode instruction.

[To page top](#summary) — [To posters at P3.1 (S3) on Thursday 15](#P3.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Prototyping custom RISC-V instructions with Seal5 and CoreDSL

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.04-SCHLAMELCHER-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.04-SCHLAMELCHER-abstract.pdf). Sub. \#188. Thursday 15, at island 3.1 on S3. ([P3.1.04-Thu](#P3.1.04-Thu)).

**Jan Schlamelcher**, German Aerospace Center - Institute of Systems Engineering for Future Mobility. **Thomas Goodfellow**, German Aerospace Center - Institute of Systems Engineering for Future Mobility. **Bewoayia Kebianyor**, German Aerospace Center - Institute of Systems Engineering for Future Mobility. **Gregor Nitsche**, German Aerospace Center - Institute of Systems Engineering for Future Mobility. **Philipp van Kempen**, Technical University of Munich. **Kim Grüttner**, German Aerospace Center - Institute of Systems Engineering for Future Mobility.

**Abstract**: Seal5 provides the efficient transformation of custom RISC-V instructions defined in CoreDSL into the LLVM toolchain and the ETISS instruction set simulator. This paper evaluates this approach by implementing an extension for the ChaCha20 cipher, achieving a substantial performance improvement in the test case without any change to its source code and a tiny increase in core size. The results demonstrate the potential of this approach for rapid exploration of customising a RISC-V-based product through extension instructions.

[To page top](#summary) — [To posters at P3.1 (S3) on Thursday 15](#P3.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Accelerating software development for high performance compute using VDKs

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.05-KUMAR-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.05-KUMAR-abstract.pdf). Sub. \#196. Thursday 15, at island 3.1 on S3. ([P3.1.05-Thu](#P3.1.05-Thu)).

**Ravi Kumar**, Tenstorrent. **Alex Nageswaran**, Tenstorrent. **Rae Parnmukh**, Tenstorrent. **Troy Jones**, Tenstorrent. **Jon Taylor**, Synopsys.

**Abstract**: This presentation discusses how Tenstorrent and Synopsys co-developed virtual design kits to accelerate software development for high performance compute. It will describe the steps taken to virtualize the Tenstorrent design and ultimately achieve Linux boot to enable further testing of compute peripherals. The work provides a proven reference flow for software development that will benefit the RISC-V ecosystem.

[To page top](#summary) — [To posters at P3.1 (S3) on Thursday 15](#P3.1-Thu) — [To all posters of Thursday 15](#Thu)

------------------------------------------------------------------------

### Embedded FPGA-Shell: Emulating RISC-V Architectures at FPGA

[Poster  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.05-AHMED-poster.pdf). [Extended abstract  ![PDF icon](media/logos/inline-pdf-logo.svg)](media/proceedings/2025-05-15-RISC-V-Summit-Europe-P3.1.05-AHMED-abstract.pdf). Sub. \#218. Thursday 15, at island 3.1 on S3. ([P3.1.05-Thu](#P3.1.05-Thu)).

**Sajjad Ahmed**, Barcelona Supercomputing Center. **Elias Perdomo**, Universitat Politècnica de Catalunya UPC, Barcelona Supercomputing Center. **Joan Teruel**, Barcelona Supercomputing Center. **Mostafa Mojahed**, Barcelona Supercomputing Center. **Alexander Kropotov**, Barcelona Supercomputing Center. **Teresa Cervero**, Barcelona Supercomputing Center. **Xavier Martorell**, Barcelona SUpercomputing Center. **Miquel Moreto**, BSC. **Behzad Salami**, Barcelona Supercomputing Center.

**Abstract**: FPGA-level pre-silicon validation of RISC-V-based architectures is crucial; however, it remains a complex and challenging process. FPGA emulation can potentially become a design bottleneck due to the lack of efficient and user-friendly toolsets. To address this challenge, this paper introduces our Embedded FPGA-Shell, a highly customizable, automated, and open-source toolset that effectively facilitates FPGA-level prototyping of RISC-V architectures. Our proposal is built on AMD technology and designed for Alveo accelerator cards, supporting both UltraScale+ and Versal architectures. The fundamental idea behind this tool is simple yet effective: it automatically enables the most common peripherals out of the box, making them readily available for RISC-V cores. Additionally, the tool includes essential components for automatically generating FPGA projects with minimal user intervention. As a demonstration of its capabilities, we integrate Embedded FPGA-Shell with OpenPiton and evaluate its efficiency using multiple in-house and open-source RISC-V cores.

[To page top](#summary) — [To posters at P3.1 (S3) on Thursday 15](#P3.1-Thu) — [To all posters of Thursday 15](#Thu)
