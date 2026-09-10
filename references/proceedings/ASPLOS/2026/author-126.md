<!-- 从 author-126.html 迁移的资料快照；原始 HTML SHA-256: 737b46af8766e0dd221cd82ef39cbe8851174312ead6970c4ae02e2ce1dcc8e3。 -->

# APS - Agile Processor Specialization

Open-Source Hardware-Software Co-Design Framework for RISC-V ISAXs

## News

- 2026-03-22 — [**ISAMORE receives ASPLOS 2026 Best Paper Award**](/publications/)  
  Our work on finding reusable instructions via e-graph anti-unification received the Best Paper Award at ASPLOS 2026.
- 2026-01-19 — [**APS tutorial presented at ASP-DAC 2026**](/tutorials/)  
  We presented a tutorial covering the innovative components of our APS ecosystem.

------------------------------------------------------------------------

## What is APS?

**APS (Agile Processor Specialization)** is an open-source framework for agile hardware-software co-design of domain-specific processors. It provides both hardware synthesis and compiler infrastructure to facilitate the development of instruction extensions (ISAXs) for domain acceleration on RISC-V platforms.

![alt text](assets/images/position.png) *APS is both open-source and fully integrated, enhancing productivity across all audiences in hardware design and adoption for domain-specific acceleration.*

### APS’s Ecosystem

APS aims to build a comprehensive ecosystem based on the **MLIR** infrastructure, covering the entire hardware-software co-design flow. Our ultimate vision is to only take applications in the target domain as the inputs, and automatically generate the complete solution artifacts comprising optimized ISAXs, architecture designs, hardware implementation, and software stacks without any manual intervention.

![alt text](assets/images/vision.png) *APS is an innovative practice of MLIR-based, automated hardware-software co-design.*

![ISAMORE and APS overview](assets/images/aps-isamore.png) *ISAMORE discovers reusable instructions from domain applications and connects them with the APS hardware-software co-design flow.*

### Current Status

We are actively evolving the APS ecosystem in line with our vision. We have released two versions of APS so far:

- **APS (ICCAD 2025)**: The first public appearance of APS as a small prototype developed in Rust to showcase the idea of automated hardware-software co-design.
- **APS 2.0 (Aquas)**: The first MLIR-integrated version of APS, which provides the complete flow around MLIR dialects for both hardware synthesis and compiler generation.

### Get Started

``` highlight
# Clone the repository
git clone https://github.com/pku-liang/aps-mlir.git
cd aps-mlir

# Follow the documentation for setup and usage
```

Visit our [GitHub repository](https://github.com/pku-liang/aps-mlir) for more information, documentation, and examples.

We hold tutorials to help new users get started with APS. See the [Tutorial](/tutorials/) page for materials and event details.
