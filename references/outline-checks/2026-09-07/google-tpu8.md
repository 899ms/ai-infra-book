<!-- 从 google-tpu8.html 迁移的资料快照；原始 HTML SHA-256: 38a52bf975382c84eeb0375f10e45bcbcdcfa1049d80e2dc80e6c981efe2cda2。 -->

Compute

# 

Inside the eighth-generation TPU: An architecture deep dive

April 22, 2026

- [![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS1EWDJCNiBuUmhpSmItQnoxMTJjLU9XWEVYZS1uU3VRZiIgdmlld2JveD0iMCAwIDI0IDI0IiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNMTMuOSwxMC41TDIxLjEsMmgtMS43bC02LjMsNy40TDgsMkgyLjJsNy42LDExLjFMMi4yLDIyaDEuN2w2LjctNy44TDE2LDIyaDUuOEwxMy45LDEwLjVMMTMuOSwxMC41eiBNMTEuNSwxMy4ybC0wLjgtMS4xIEw0LjYsMy4zaDIuN2w1LDcuMWwwLjgsMS4xbDYuNSw5LjJoLTIuN0wxMS41LDEzLjJMMTEuNSwxMy4yeiIgLz48L3N2Zz4=)](https://x.com/intent/tweet?text=Inside%20the%20eighth-generation%20TPU:%20An%20architecture%20deep%20dive%20@googlecloud&url=https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive)
- [![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS1EWDJCNiBuUmhpSmItQnoxMTJjLU9XWEVYZS1uU3VRZiIgdmlld2JveD0iMCAwIDI0IDI0IiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNMjAgMkg0Yy0xLjEgMC0xLjk5LjktMS45OSAyTDIgMjBjMCAxLjEuOSAyIDIgMmgxNmMxLjEgMCAyLS45IDItMlY0YzAtMS4xLS45LTItMi0yek04IDE5SDV2LTloM3Y5ek02LjUgOC4zMWMtMSAwLTEuODEtLjgxLTEuODEtMS44MVM1LjUgNC42OSA2LjUgNC42OXMxLjgxLjgxIDEuODEgMS44MVM3LjUgOC4zMSA2LjUgOC4zMXpNMTkgMTloLTN2LTUuM2MwLS44My0uNjctMS41LTEuNS0xLjVzLTEuNS42Ny0xLjUgMS41VjE5aC0zdi05aDN2MS4yYy41Mi0uODQgMS41OS0xLjQgMi41LTEuNCAxLjkzIDAgMy41IDEuNTcgMy41IDMuNVYxOXoiIC8+PC9zdmc+)](https://www.linkedin.com/shareArticle?mini=true&url=https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive&title=Inside%20the%20eighth-generation%20TPU:%20An%20architecture%20deep%20dive)
- [![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS1EWDJCNiBuUmhpSmItQnoxMTJjLU9XWEVYZS1uU3VRZiIgdmlld2JveD0iMCAwIDI0IDI0IiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNMjAgMkg0Yy0xLjEgMC0xLjk5LjktMS45OSAyTDIgMjBjMCAxLjEuOSAyIDIgMmgxNmMxLjEgMCAyLS45IDItMlY0YzAtMS4xLS45LTItMi0yem0tMSAydjNoLTJjLS41NSAwLTEgLjQ1LTEgMXYyaDN2M2gtM3Y3aC0zdi03aC0ydi0zaDJWNy41QzEzIDUuNTcgMTQuNTcgNCAxNi41IDRIMTl6IiAvPjwvc3ZnPg==)](https://www.facebook.com/sharer/sharer.php?caption=Inside%20the%20eighth-generation%20TPU:%20An%20architecture%20deep%20dive&u=https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive)
- [![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS1EWDJCNiBuUmhpSmItQnoxMTJjLU9XWEVYZS1uU3VRZiIgdmlld2JveD0iMCAwIDI0IDI0IiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNMjAgNEg0Yy0xLjEgMC0yIC45LTIgMnYxMmMwIDEuMS45IDIgMiAyaDE2YzEuMSAwIDItLjkgMi0yVjZjMC0xLjEtLjktMi0yLTJ6bS0uOCAyTDEyIDEwLjggNC44IDZoMTQuNHpNNCAxOFY3Ljg3bDggNS4zMyA4LTUuMzNWMThINHoiIC8+PC9zdmc+)](mailto:?subject=Inside%20the%20eighth-generation%20TPU:%20An%20architecture%20deep%20dive&body=Check%20out%20this%20article%20on%20the%20Cloud%20Blog:%0A%0AInside%20the%20eighth-generation%20TPU:%20An%20architecture%20deep%20dive%0A%0AThe%208th%20generation%20TPUs%20are%20engineered%20with%20%20system-level%20co-design%20to%20accelerate%20the%20AI%20lifecycle.%20TPU%208t%20is%20built%20for%20frontier-model%20training%20and%20TPU%208i%20is%20built%20for%20large-scale%20inference%20and%20reinforcement%20learning.%0A%0Ahttps://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive)

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/eighth-generation_TPU.max-2000x2000.jpg)

##### Diwakar Gupta

Distinguished Engineer, Google Cloud

##### Sabastian Mugazambi

Group Product Manager, Google Cloud

##### Try Gemini Enterprise today

The front door to AI in the workplace

[Try now](https://business.gemini.google/?utm_source=cloud.google.com/blog&utm_medium=et&utm_campaign=FY26-Q2-GLOBAL-GLO27877-physicalevent-er-next26-mc-105752)

At Google, our TPU design philosophy has always been centered on three pillars: scalability, reliability, and efficiency. As AI models evolve from dense large language models (LLMs) to massive Mixture-of-Experts (MoEs) and reasoning-heavy architectures, the hardware must do more than just add floating point operations per second (FLOPS); it must evolve to meet the specific operational intensities of the latest workloads.

The rise of agentic AI requires infrastructure that can handle long context windows and complex sequential logic. At the same time, world models have emerged as a necessary evolution from current next-sequence-of-data architectures, which means newer agents are simulating future scenarios, anticipating consequences, and learning through "imagination" rather than risky trial-and-error. The eighth-generation TPUs (TPU 8t and TPU 8i) are our answer to these challenges, ensuring that every workload, from the first token of training to the final step of a multi-turn reasoning chain, is running on the most efficient path possible. They are built to efficiently train and serve world models like Google DeepMind’s Genie 3, enabling millions of agents to practice and refine their reasoning in diverse simulated environments.

### **TPU 8: Specialized by design**

Recognizing that the infrastructure requirements for pre-training, post-training, and real-time serving have diverged, our eighth-generation TPUs introduce two distinct systems: TPU 8t and TPU 8i. These new systems are key components of Google Cloud's AI Hypercomputer, an integrated supercomputing architecture that combines hardware, software, and networking to power the full AI lifecycle. While both systems share the core DNA of Google’s AI stack and support the full AI lifecycle, each is built to address distinct bottlenecks and optimize efficiency for critical stages of development. Additionally, by integrating Arm-based Axion CPU headers across our eighth-generation TPU system, we’ve removed the host bottleneck caused by data preparation latency. Axion provides the compute headroom to handle complex data preprocessing and orchestration, so that TPUs stay fed and don’t stall.

### TPU 8t: The pre-training powerhouse

Optimized for massive-scale pre-training and embedding-heavy workloads, TPU 8t utilizes our proven 3D torus network topology at an even larger scale of 9,600 chips in a single superpod. TPU 8t is designed for maximum throughput across hundreds of superpods, ensuring that training runs stay on schedule.

Here are some key advancements of TPU 8t over prior-generation TPUs:

- **The SparseCore advantage**: Central to TPU 8t is the SparseCore, a specialized accelerator designed to handle the irregular memory access patterns of embedding lookups. While the Matrix Multiply Unit (MXU) handles matrix math, the SparseCore offloads data-dependent all-gather operations, amongst other collectives, preventing the zero-op bottlenecks that often plague general-purpose chips.
- **VPU/MXU overlap and balanced scaling**: TPU 8t is designed to maximize provisioned FLOPs utilization. By implementing more balanced Vector Processing Unit (VPU) scaling, the architecture minimizes exposed vector operation time. This allows for better overlapping of quantization, softmax, and layernorms with the matrix multiplications in the MXU, helping the chip stay busy rather than waiting on sequential vector tasks.
- **Native FP4**: TPU 8t introduces native 4-bit floating point (FP4) to overcome memory bandwidth bottlenecks, doubling MXU throughput while maintaining accuracy for large models even at lower-precision quantization. By reducing the bits per parameter, the platform minimizes energy-intensive data movement and allows larger model layers to fit within local hardware buffers for peak compute utilization.

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/1_v4.max-1600x1600.png)

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/1_v4.max-1600x1600.png)

Figure 1: TPU 8t ASIC block diagram

- **Virgo Network topology and up to 4x data center network increase**: To support the massive data requirements of TPU 8t, [we introduced Virgo Network](https://cloud.google.com/blog/products/networking/introducing-virgo-megascale-data-center-fabric). This new networking architecture enables up to 4x increased data center network (DCN) bandwidth on TPU 8t training over DCN. Virgo Network is a scale-out fabric designed for the extreme requirements of modern AI workloads. Built on high-radix switches that reduce network layers by allowing more ports per switch, it employs a flat, two-layer non-blocking topology. Compared with traditional datacenter networks, this significantly reduces latency by minimizing network tiers. It features a multi-planar design with independent control domains to connect TPU 8t chips. The TPU 8t racks also connect with the Jupiter north-south fabric to access compute and storage services. Together, this streamlined architecture delivers the massive bisection bandwidth and deterministic low latency necessary for enabling the world's largest training clusters with high availability. 

With 2x scale-up bandwidth on the inter-chip interconnect (ICI) and up to 4x raw scale-out DCN bandwidth compared to the previous generation, TPU 8t drastically reduces data bottlenecks. Then, to further accelerate the development of frontier models, we scale distributed training beyond a single cluster. With [JAX](https://docs.jax.dev/en/latest/index.html) and [Pathways](https://docs.cloud.google.com/ai-hypercomputer/docs/workloads/pathways-on-cloud/pathways-intro), **we can now** [**scale**](https://jax-ml.github.io/scaling-book/) **to more than 1 million TPU chips in a single training cluster**. Virgo Network can link over 134,000 TPU 8t chips with up to 47 petabits/sec of non-blocking bi-sectional bandwidth in a single fabric. This fabric delivers over 1.7K ExaFlops with near-linear scaling performance.

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/2_TPU_8t_rack_level_connectivity_to_Virgo_.max-2000x2000.png)

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/2_TPU_8t_rack_level_connectivity_to_Virgo_.max-2000x2000.png)

Figure 2: TPU 8t rack level connectivity to Virgo fabric

- **Faster storage access:** We are introducing **TPUDirect RDMA** and **TPU Direct Storage** in TPU 8t. TPU Direct RDMA enables direct data transfers between the TPU's memory (HBM) and the Network Interface Cards (NICs), bypassing the host CPU and DRAM. This reduces latency and host system bottlenecks, increasing the effective bandwidth for TPU-to-TPU communication. Similarly, TPUDirect Storage bypasses CPU host bottlenecks by enabling direct memory access between the TPU and high-speed managed storage like 10T Lustre, effectively doubling the bandwidth for massive data transfers. This architecture allows the silicon to ingest training data at line rate, ensuring that the MXUs stay fully saturated even when processing large multimodal datasets. 

By combining [Managed Lustre 10T](https://cloud.google.com/blog/products/storage-data-transfer/next26-storage-announcements) and TPUDirect Storage to route hundred-petabyte datasets directly to the silicon, TPU 8t prevents training delays caused by data ingestion bottlenecks. This delivers 10x faster storage access compared to training on seventh-generation Ironwood TPUs.

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/3_rq0yjyX.max-2000x2000.png)

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/3_rq0yjyX.max-2000x2000.png)

Figure 3: The top diagram shows the data transfer path without TPUDirect Storage. The bottom diagram shows TPU 8t data transfer with TPUDirect Storage between 2 TPU 8t chips and TPUDirect Storage with Managed 10T Lustre storage.

### TPU 8i: The sampling and serving specialist

Optimized for post-training and high-concurrency reasoning, we designed TPU 8i with our highest on-chip SRAM, a new Collectives Acceleration Engine (CAE), and a new serving-optimized network topology called Boardfly. 

- **Large on-chip SRAM:** With 3x more on-chip SRAM over the previous generation, TPU 8i can host a larger KV Cache entirely on silicon, significantly reducing the idle time of the cores during long-context decoding.

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/4_v1_nUZDsJM.max-1800x1800.png)

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/4_v1_nUZDsJM.max-1800x1800.png)

Figure 4: TPU 8i ASIC block diagram

- **The Collectives Acceleration Engine (CAE)**: To solve the sampling bottleneck, TPU 8i uses the CAE, which aggregates results across cores with near-zero latency, specifically accelerating the reduction and synchronization steps required during auto-regressive decoding and "chain-of-thought" processing. For each TPU 8i chip, there are two Tensor Cores (TC) on-core dies and one CAE on the chiplet die, replacing four SparseCores (SCs) on core dies in previous-generation Ironwood TPU. By integrating a specialized CAE, TPU 8i further reduces the on-chip latency of collectives by 5x. Lower latency per collective operation means less time spent waiting, directly contributing to higher throughput required to run millions of agents concurrently.

- **Boardfly ICI topology**: While the 3D torus allows connecting thousands of chips to be used in cohesion, a large mesh does have more hops between chips and higher all-to-all latencies. For 8i, we changed how the chips connect together in fully connected boards that are then aggregated into groups. Utilizing a high-radix design, we connect up-to 1,152 of these chips together, reducing the network diameter and the number of hops a data packet must take to cross the system. By slashing the hops required for all-to-all communication (the heart of MoE and reasoning models), Boardfly achieves up to a 50% improvement in latency for communication-intensive workloads.

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/5_I1mUzjb.max-1300x1300.png)

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/5_I1mUzjb.max-1300x1300.png)

Figure 5: TPU 8i hierarchical Boardfly topology building up from a building block of four fully connected chips into a fully connected group of eight boards, with 36 of such groups fully connected into a TPU 8i pod

Boardfly consists of the following elements, and its topology is hierarchical by nature:

- **Building Block (BB):** Each tray forms a four-chip ring using internal ICI links, providing 16 external connections for broader networking.
- **Group (G):** Eight boards are fully connected via copper cabling to create a localized group, utilizing 11 of the available external links for intra-group communication.
- **Pod structure:** The final architecture scales to 36 groups (up to 1,024 active chips) linked through Optical Circuit Switches (OCS), ensuring a maximum latency of seven hops for any chip-to-chip communication.

### Deep dive: The Boardfly vs. torus math

Why move away from the torus for TPU 8i? It comes down to network diameter.

In a 3D torus, nodes are arranged in a grid where each dimension wraps around like a ring. To reach the furthest possible chip in a 8 x 8 x 16 (1024-chip) configuration, a packet must traverse half the distance of each ring:

3D torus = 8/2(X) + 8/2(Y) + 16/2(Z) = 16 hops

While the torus is highly efficient for the neighbor-to-neighbor communication typical of dense training, it creates a latency tax for all-to-all communication patterns. In the era of reasoning models and MoE, where any chip may need to talk to any other chip to route a token, this hop count matters.

Boardfly’s high-radix topology is inspired by [Dragonfly](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/34926.pdf) topology principles. By increasing the number of direct optical long-haul links between groups of boards, we flatten the network. For that same 1024-chip pod, Boardfly reduces the network diameter from 16 hops down to just seven.

This 56% reduction in network diameter translates directly to lower tail latency, so that the TPU 8i CAE isn't left waiting for data to arrive from across the pod.

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/6_Qu7H2lI.max-1300x1300.png)

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/6_Qu7H2lI.max-1300x1300.png)

Figure 6: A visual representation of the maximum seven-hop ICI network diameter via optical circuit switch on TPU 8i pod

### TPU 8t and TPU 8i at a glance

|  |  |  |
|----|----|----|
| **Feature** | **TPU 8t** | **TPU 8i** |
| **Primary Workload** | Large-scale pre-training | Sampling, serving, and reasoning |
| **Network Topology** | 3D torus | Boardfly  |
| **Specialized Chip Features** | SparseCore (Embeddings) & LLM Decoder Engine | CAE (Collectives Acceleration Engine) |
| **HBM Capacity** | 216 GB | 288 GB |
| **On-Chip SRAM (Vmem)** | 128 MB | 384 MB |
| **Peak FP4 PFLOPs** | 12.6 | 10.1 |
| **HBM Bandwidth** | 6,528 GB/s | 8,601 GB/s (~1.3x of TPU 8t) |
| **CPU Header** | **Arm Axion** | **Arm Axion** |

### Software enablement: A performance-first AI stack

Hardware is only as powerful as the software that drives it. The eighth generation of TPUs are built on the same performance-first stack we pioneered with the seventh-generation Ironwood TPUs, designed to make custom kernel development accessible without sacrificing the abstraction of high-level frameworks. This stack includes:

- **Pallas and Mosaic**: We provide first-class support for [Pallas](https://docs.jax.dev/en/latest/pallas/tpu/), our custom kernel language that lets you write hardware-aware kernels in Python. This enables you to squeeze every drop of performance out of the TPU 8i CAE and the TPU 8t SparseCore.

- **Native PyTorch experience:** We're thrilled to share that [native PyTorch support for TPUs](https://developers.googleblog.com/torchtpu-running-pytorch-natively-on-tpus-at-google-scale/) is now in preview. If you're currently building and serving models on PyTorch, we've made it easier than ever to start using TPUs. You can bring your existing models to our TPUs just as they are, complete with full support for the native features you rely on, such as Eager Mode.

- **Portability**: The same JAX, PyTorch, or Keras code that runs on Ironwood scales to this generation. Accelerated Linear Algebra (XLA) handles the complex translation of the Boardfly topology and CAE synchronization behind the scenes, allowing you to focus on your model, not the interconnect.

### Generation over generation: The performance leap

Our commitment to co-designing hardware and software continues to pay dividends. When compared to seventh-generation Ironwood TPU, the eighthgeneration TPUs deliver massive gains:

- **Training price-performance**: TPU 8t delivers up to 2.7x performance-per-dollar improvement over Ironwood TPU for large-scale training.

- **Inference price-performance**: TPU 8i delivers up to 80% performance-per-dollar improvement over Ironwood TPU, particularly at low-latency targets for large MoE models.

- **Energy efficiency**: Both chips deliver up to 2x better performance-per-watt, critical for scaling the next generation of AI sustainably.

### Looking ahead

To empower Google Cloud customers pioneering the next wave of innovation, we designed TPU 8t and TPU 8i as two distinct, specialized systems tailored to the multifaceted future demands of the AI lifecycle. TPU 8t and 8i are both purpose-built for the most demanding serving and training workloads, fully integrating with the AI Hypercomputer software stack: JAX, PyTorch, vLLM, XLA, and Pathways. This specialization and ground-up redesign, all in deep collaboration with Google Deepmind, delivers exceptional price-performance and power efficiency.

The modularity of our eighth-generation architecture provides a clear and unique roadmap for the future. Just as every major shift in the computing landscape has required infrastructure breakthroughs, so does the agentic era. Reasoning agents that plan, execute, and learn within continuous feedback loops cannot operate at peak efficiency on hardware that was originally optimized for traditional training or transactional inference; their operational intensity are fundamentally distinct. Our eighth-generation TPU infrastructure has evolved to meet these specific requirements head-on.

To learn more about the eighth-generation TPU family:

- [**Submit an interest form for eighth-generation TPUs**](https://cloud.google.com/resources/tpu-interest?e=48754805)
- [**Get involved in the community forums**](https://discuss.google.dev/c/google-cloud/cloud-ai-infrastructure/ai-infrastructure-tpus/247)
- [**Check out the eighth-generation TPU announcement video**](https://youtu.be/wOVtSeP4aAM)
- [**Visit our TPU website**](https://cloud.google.com/tpu)

 

Posted in

- [Compute](https://cloud.google.com/blog/products/compute)
- [AI & Machine Learning](https://cloud.google.com/blog/products/ai-machine-learning)
- [Google Cloud Next](https://cloud.google.com/blog/topics/google-cloud-next)
- [TPUs](https://cloud.google.com/blog/topics/tpus)
- [AI infrastructure](https://cloud.google.com/blog/topics/ai-infrastructure)

##### Related articles

[](https://cloud.google.com/blog/products/compute/google-named-a-leader-in-2026-gartner-magic-quadrant-for-scps)

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/05_-_Compute.max-700x700.jpg)

Compute

### Google named a Leader in 2026 Gartner® Magic Quadrant™ for Strategic Cloud Platform Services

By Brad Calder • 5-minute read

[](https://cloud.google.com/blog/topics/ai-infrastructure/whats-new-in-ai-infrastructure-this-month)

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/Whats_new_in_AI_infrastructure.max-700x700.jpg)

AI infrastructure

### What’s new in AI infrastructure and orchestration in August

By Alex Barrett • 13-minute read

[](https://cloud.google.com/blog/topics/ai-infrastructure/best-practices-for-dynamic-capacity-management)

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/AI_infrastructure_default.max-700x700.jpg)

AI infrastructure

### Dynamic capacity management for AI infrastructure

By Drew Bradstock • 7-minute read

[](https://cloud.google.com/blog/products/identity-security/pqc-in-plaintext-google-clouds-post-quantum-cryptography-roadmap)

![](https://storage.googleapis.com/gweb-cloudblog-publish/images/17_-_Security__Identity_NrORvDT.max-700x700.jpg)

Security & Identity

### PQC in Plaintext: Google Cloud’s post-quantum cryptography roadmap

By Jai Haridas • 14-minute read

### Footer Links

#### Follow us

- [![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUtRFgyQjYiIHZpZXdib3g9IjAgMCAyNCAyNCIgcm9sZT0icHJlc2VudGF0aW9uIiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTEzLjksMTAuNUwyMS4xLDJoLTEuN2wtNi4zLDcuNEw4LDJIMi4ybDcuNiwxMS4xTDIuMiwyMmgxLjdsNi43LTcuOEwxNiwyMmg1LjhMMTMuOSwxMC41TDEzLjksMTAuNXogTTExLjUsMTMuMmwtMC44LTEuMSBMNC42LDMuM2gyLjdsNSw3LjFsMC44LDEuMWw2LjUsOS4yaC0yLjdMMTEuNSwxMy4yTDExLjUsMTMuMnoiIC8+PC9zdmc+)](https://www.x.com/googlecloud)
- [![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUtRFgyQjYiIHZpZXdib3g9IjAgMCAyNCAyNCIgcm9sZT0icHJlc2VudGF0aW9uIiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTIzLjc0IDcuMXMtLjIzLTEuNjUtLjk1LTIuMzdjLS45MS0uOTYtMS45My0uOTYtMi40LTEuMDJDMTcuMDQgMy40NyAxMiAzLjUgMTIgMy41cy01LjAyLS4wMy04LjM3LjIxYy0uNDYuMDYtMS40OC4wNi0yLjM5IDEuMDJDLjUyIDUuNDUuMjggNy4xLjI4IDcuMVMuMDQgOS4wNSAwIDEwLjk4VjEzYy4wNCAxLjk0LjI4IDMuODcuMjggMy44N3MuMjQgMS42NS45NiAyLjM4Yy45MS45NSAyLjEuOTIgMi42NCAxLjAyIDEuODguMTggNy45MS4yMiA4LjEyLjIyIDAgMCA1LjA1LjAxIDguNC0uMjMuNDYtLjA2IDEuNDgtLjA2IDIuMzktMS4wMi43Mi0uNzIuOTYtMi4zNy45Ni0yLjM3cy4yNC0xLjk0LjI1LTMuODd2LTIuMDJjLS4wMi0xLjkzLS4yNi0zLjg4LS4yNi0zLjg4ek05LjU3IDE1LjVWOC40OUwxNiAxMi4xMyA5LjU3IDE1LjV6IiAvPjwvc3ZnPg==)](https://www.youtube.com/googlecloud)
- [![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUtRFgyQjYiIHZpZXdib3g9IjAgMCAyNCAyNCIgcm9sZT0icHJlc2VudGF0aW9uIiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTIwIDJINGMtMS4xIDAtMS45OS45LTEuOTkgMkwyIDIwYzAgMS4xLjkgMiAyIDJoMTZjMS4xIDAgMi0uOSAyLTJWNGMwLTEuMS0uOS0yLTItMnpNOCAxOUg1di05aDN2OXpNNi41IDguMzFjLTEgMC0xLjgxLS44MS0xLjgxLTEuODFTNS41IDQuNjkgNi41IDQuNjlzMS44MS44MSAxLjgxIDEuODFTNy41IDguMzEgNi41IDguMzF6TTE5IDE5aC0zdi01LjNjMC0uODMtLjY3LTEuNS0xLjUtMS41cy0xLjUuNjctMS41IDEuNVYxOWgtM3YtOWgzdjEuMmMuNTItLjg0IDEuNTktMS40IDIuNS0xLjQgMS45MyAwIDMuNSAxLjU3IDMuNSAzLjVWMTl6IiAvPjwvc3ZnPg==)](https://www.linkedin.com/showcase/google-cloud)
- [![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUtRFgyQjYiIHZpZXdib3g9IjAgMCAyNCAyNCIgcm9sZT0icHJlc2VudGF0aW9uIiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTEyLDAgQzE1LjMsMCAxNS43LDAgMTcsMCBDMTguMywwLjEgMTkuMSwwLjMgMTkuOSwwLjYgQzIwLjcsMC45IDIxLjMsMS4zIDIyLDIgQzIyLjcsMi43IDIzLjEsMy40IDIzLjMsNC4yIEMyMy42LDUgMjMuOCw1LjggMjMuOSw3LjEgQzI0LDguMyAyNCw4LjcgMjQsMTIgQzI0LDE1LjMgMjQsMTUuNyAyMy45LDE2LjkgQzIzLjgsMTguMiAyMy42LDE5IDIzLjMsMTkuOCBDMjMsMjAuNiAyMi42LDIxLjIgMjEuOSwyMS45IEMyMS4zLDIyLjYgMjAuNiwyMyAxOS44LDIzLjMgQzE5LDIzLjYgMTguMiwyMy44IDE2LjksMjMuOSBDMTUuNywyNCAxNS4zLDI0IDEyLDI0IEM4LjcsMjQgOC4zLDI0IDcsMjQgQzUuNywyMy45IDQuOSwyMy43IDQuMSwyMy40IEMzLjMsMjMuMSAyLjcsMjIuNyAyLDIyIEMxLjMsMjEuMyAwLjksMjAuNiAwLjcsMTkuOCBDMC40LDE5IDAuMiwxOC4yIDAuMSwxNi45IEMwLDE1LjcgMCwxNS4zIDAsMTIgQzAsOC43IDAsOC4zIDAuMSw3LjEgQzAuMSw1LjggMC4zLDQuOSAwLjYsNC4xIEMwLjksMy40IDEuMywyLjcgMiwyIEMyLjcsMS4zIDMuNCwwLjkgNC4xLDAuNiBDNC45LDAuMyA1LjgsMC4xIDcuMSwwLjEgQzguMywwIDguNywwIDEyLDAgWiBNMTIsMi4yIEM4LjgsMi4yIDguNCwyLjIgNy4yLDIuMiBDNiwyLjMgNS4zLDIuNSA0LjksMi42IEM0LjQsMi45IDQsMy4xIDMuNSwzLjUgQzMuMSwzLjkgMi44LDQuMyAyLjYsNC45IEMyLjUsNS4zIDIuMyw2IDIuMyw3LjIgQzIuMiw4LjQgMi4yLDguOCAyLjIsMTIgQzIuMiwxNS4yIDIuMiwxNS41IDIuMywxNi44IEMyLjMsMTcuOSAyLjUsMTguNiAyLjcsMTkgQzIuOSwxOS42IDMuMiwyMCAzLjYsMjAuNCBDNCwyMC44IDQuNCwyMS4xIDUsMjEuMyBDNS40LDIxLjUgNiwyMS42IDcuMiwyMS43IEM4LjQsMjEuOCA4LjgsMjEuOCAxMiwyMS44IEMxNS4yLDIxLjggMTUuNSwyMS44IDE2LjgsMjEuNyBDMTcuOSwyMS43IDE4LjYsMjEuNSAxOSwyMS4zIEMxOS42LDIxLjEgMjAsMjAuOCAyMC40LDIwLjQgQzIwLjgsMjAgMjEuMSwxOS42IDIxLjMsMTkgQzIxLjUsMTguNiAyMS42LDE4IDIxLjcsMTYuOCBDMjEuOCwxNS42IDIxLjgsMTUuMiAyMS44LDEyIEMyMS44LDguOCAyMS44LDguNSAyMS43LDcuMiBDMjEuNyw2LjEgMjEuNSw1LjQgMjEuMyw1IEMyMS4xLDQuNCAyMC44LDQgMjAuNCwzLjYgQzIwLDMuMiAxOS42LDIuOSAxOSwyLjcgQzE4LjYsMi41IDE4LDIuNCAxNi44LDIuMyBDMTUuNiwyLjIgMTUuMiwyLjIgMTIsMi4yIFogTTEyLDUuOCBDMTUuNCw1LjggMTguMiw4LjYgMTguMiwxMiBDMTguMiwxNS40IDE1LjQsMTguMiAxMiwxOC4yIEM4LjYsMTguMiA1LjgsMTUuNCA1LjgsMTIgQzUuOCw4LjYgOC42LDUuOCAxMiw1LjggWiBNMTIsMTYgQzE0LjIsMTYgMTYsMTQuMiAxNiwxMiBDMTYsOS44IDE0LjIsOCAxMiw4IEM5LjgsOCA4LDkuOCA4LDEyIEM4LDE0LjIgOS44LDE2IDEyLDE2IFogTTE4LjQsNyBDMTcuNjI2ODAxNCw3IDE3LDYuMzczMTk4NjUgMTcsNS42IEMxNyw0LjgyNjgwMTM1IDE3LjYyNjgwMTQsNC4yIDE4LjQsNC4yIEMxOS4xNzMxOTg2LDQuMiAxOS44LDQuODI2ODAxMzUgMTkuOCw1LjYgQzE5LjgsNi4zNzMxOTg2NSAxOS4xNzMxOTg2LDcgMTguNCw3IFoiIC8+PC9zdmc+)](https://www.instagram.com/googlecloud/)
- [![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUtRFgyQjYiIHZpZXdib3g9IjAgMCAyNCAyNCIgcm9sZT0icHJlc2VudGF0aW9uIiBhcmlhLWhpZGRlbj0idHJ1ZSI+PHBhdGggZD0iTTIwIDJINGMtMS4xIDAtMS45OS45LTEuOTkgMkwyIDIwYzAgMS4xLjkgMiAyIDJoMTZjMS4xIDAgMi0uOSAyLTJWNGMwLTEuMS0uOS0yLTItMnptLTEgMnYzaC0yYy0uNTUgMC0xIC40NS0xIDF2MmgzdjNoLTN2N2gtM3YtN2gtMnYtM2gyVjcuNUMxMyA1LjU3IDE0LjU3IDQgMTYuNSA0SDE5eiIgLz48L3N2Zz4=)](https://www.facebook.com/googlecloud/)

[![Cloud logo](https://www.gstatic.com/cgc/super_cloud_gradient.png)](https://cloud.google.com/ "Google Cloud")

- [Google Cloud](https://cloud.google.com/)
- [Google Cloud Products](https://cloud.google.com/products/)
- [Privacy](https://myaccount.google.com/privacypolicy?hl=en-US)
- [Terms](https://myaccount.google.com/termsofservice?hl=en-US)
- [Cookies management controls](https://cloud.google.com/blog/#)

&nbsp;

- [![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iblJoaUpiLUJ6MTEyYyBuUmhpSmItQnoxMTJjLU9XWEVYZS14Z1plM2MgblJoaUpiLUJ6MTEyYy1PV1hFWGUteWVQZTVjLWg5ZDNoZCIgdmlld2JveD0iMCAwIDI0IDI0IiByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNMTIgMkM2LjQ4IDIgMiA2LjQ4IDIgMTJzNC40OCAxMCAxMCAxMCAxMC00LjQ4IDEwLTEwUzE3LjUyIDIgMTIgMnptMSAxN2gtMnYtMmgydjJ6bTIuMDctNy43NWwtLjkuOTJDMTMuNDUgMTIuOSAxMyAxMy41IDEzIDE1aC0ydi0uNWMwLTEuMS40NS0yLjEgMS4xNy0yLjgzbDEuMjQtMS4yNmMuMzctLjM2LjU5LS44Ni41OS0xLjQxIDAtMS4xLS45LTItMi0ycy0yIC45LTIgMkg4YzAtMi4yMSAxLjc5LTQgNC00czQgMS43OSA0IDRjMCAuODgtLjM2IDEuNjgtLjkzIDIuMjV6IiAvPjwvc3ZnPg==)Help](https://support.google.com)
- Language‪English‬‪Deutsch‬‪Français‬‪한국어‬‪日本語‬
