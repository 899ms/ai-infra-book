# Understanding AI Infra: Quantitative Analysis and System Design

**Data movement shapes the architecture of AI infrastructure.** Starting from a single model execution, see how chips, networks, and inference and training systems change how data is reused, placed, and waited on.

[Download PDF](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book-EN.pdf) · [EPUB](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book-EN.epub) · [Preface](../book-en/introduction.md) · [GitHub repository](https://github.com/bojieli/ai-infra-book)

This is the community English translation (by [@tg1482](https://github.com/tg1482)) of the Chinese original and may lag behind it. The Chinese edition is the authoritative source for numbers, formulas and citations.

## What this book covers

*Understanding AI Infra* is the companion volume to [*Understanding AI Agents: Design Principles and Engineering Practice*](https://github.com/bojieli/ai-agent-book), which has 45k+ stars on GitHub.

Building good model-based applications also requires understanding the infrastructure they run on. Most software engineers never write an operating system, a compiler or a chip, yet they still study operating systems, compilers and computer architecture, because allocating memory, reading a file and calling a function all carry resource and time costs. Model-based applications are no different. A few times more latency can change the product experience entirely; an order of magnitude in cost changes which business models are viable.

The deeper change is that **the programming abstraction has moved up, from the operating system to the model context**. Traditional operating systems, compilers and hardware must serve programs they cannot anticipate, so system optimization always trades programmability against performance. Now that LLMs are the most important application, everything from operator execution to distributed scheduling can be optimized for specific models and accelerator architectures, and model design has started to adapt to hardware in turn. In a sense, **the model is the operating system of the LLM era, and AI infrastructure is its computer architecture**.

The method throughout is **deriving design from constraints**: state the task and its quality requirements, list the compute, storage, communication and dependencies, and estimate orders of magnitude against the capacity, bandwidth and compute of the hardware. People get these estimates wrong, and so does AI: counting weight reads but forgetting the KV cache, projecting speed from peak compute without checking whether bandwidth can keep up, splitting work evenly across devices but omitting the communication between them. Missing any one term can push a conclusion off by several times or several orders of magnitude. From FPGA-accelerated Bing ranking and Ascend AKG operator generation to UB interconnect at the scale of ten thousand accelerators, the same thread keeps appearing: **data movement**. The book therefore keeps asking five questions: **what is moved, how much, how many times, through where, and who must wait for it.**

More background is in the [Preface](../book-en/introduction.md). The book is still a first draft under active revision.

## The twelve chapters

The book starts from the resource budget of a single model execution, moves through model architecture and workloads, accelerators and operators, supernodes and networks, and inference and training systems, and ends with scheduling and the choice between device, edge and cloud.

| Ch. | Topic | Key question |
| :--: | --- | --- |
| 1 | [First Encounter with AI Infrastructure](../book-en/chapter01.md) | How much memory, compute and data traffic does one generation need? |
| 2 | [Model Architecture](../book-en/chapter02.md) | How do attention, history state and expert structure change system requirements? |
| 3 | [Inference and Training Workloads](../book-en/chapter03.md) | How do task phases, arrival patterns and state lifetimes shape resource demand? |
| 4 | [Accelerator Architecture](../book-en/chapter04.md) | How to trade off compute, memory, bandwidth, power and cost? |
| 5 | [Operators and Runtime](../book-en/chapter05.md) | How do fusion, reuse, concurrency and scheduling cut execution overhead? |
| 6 | [Supernodes](../book-en/chapter06.md) | How do cooperating devices balance capacity, throughput and synchronization cost? |
| 7 | [Datacenter Networks](../book-en/chapter07.md) | How do bandwidth, communication patterns and congestion affect compute efficiency? |
| 8 | [Inference Optimization](../book-en/chapter08.md) | When do batching, KV management, offloading and speculative decoding pay off? |
| 9 | [Distributed Inference](../book-en/chapter09.md) | Where to place compute and state, and how to handle scaling and recovery? |
| 10 | [Training Systems](../book-en/chapter10.md) | How to arrange memory, communication and recomputation for efficient training? |
| 11 | [Resource Scheduling and Execution Environments](../book-en/chapter11.md) | How can model serving and tool environments share resources and wait less? |
| 12 | [Edge-Cloud Coordination](../book-en/chapter12.md) | Local, edge or cloud: how to balance quality, latency and cost? |

## How to read

Reading in order from the [Preface](../book-en/introduction.md) and Chapter 1 is easiest: later chapters keep reusing the models, hardware and workload settings built up early on. You can also search directly for a model, operator or system mechanism. Each chapter has a section outline, formulas, figures, footnotes, and links to the previous and next chapter.

The book is full of formulas, tables and cross-references; the [PDF edition](https://github.com/bojieli/ai-infra-book/releases/latest/download/AI-Infra-Book-EN.pdf) has the complete typesetting.

## Companion material

Most numbers in the book can be recomputed. The calculation tools, experiment records and figure scripts are all in the GitHub repository:

- [Quantitative calculations](../calculations/README.md): tools and fixed inputs for the book's recomputable numbers
- [Experiments](../experiments/README.md): experiments and run records organized by chapter
- [Chapters and figures](../manuscripts/README.md): figure lists and plotting scripts for each chapter (Chinese source)
