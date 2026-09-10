<!-- 从 index.html 迁移的资料快照；原始 HTML SHA-256: ad09796ee92b3120865c775ff2dba0c92e6956eaabc8934468a35d04035774ba。 -->

# NSDI '26 Technical Sessions

### Papers and Proceedings

The full Proceedings published by USENIX for the symposium are available for download below. Individual papers can also be downloaded from their respective presentation pages. Copyright to the individual works is retained by the author\[s\].

**Proceedings Front Matter**  
[Proceedings Cover](https://www.usenix.org/sites/default/files/nsdi26-cover.pdf) \| [Title Page and List of Organizers](https://www.usenix.org/sites/default/files/nsdi26-title_organizers.pdf) \| [Message from the Program Co-Chairs](https://www.usenix.org/sites/default/files/nsdi26-message.pdf) \| [Table of Contents](https://www.usenix.org/sites/default/files/nsdi26-contents.pdf)

**Full Proceedings PDFs**  
![](/core/modules/file/icons/application-pdf.png) [NSDI '26 Full Proceedings (PDF, 351 MB)](/sites/default/files/nsdi26_full_proceedings.pdf)  
![](/core/modules/file/icons/application-pdf.png) [NSDI '26 Proceedings Interior (PDF, 351 MB, best for mobile devices)](/sites/default/files/nsdi26_proceedings_interior.pdf)  
![](/core/modules/file/icons/application-pdf.png) [NSDI '26 Errata Slip \#1 (PDF)](/system/files/nsdi26-errata-zhang-zhihao.pdf)  

Attendee Files 

(Registered attendees: [Sign in](/user/login?destination=node/316820) to your USENIX account to download these files.)

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

![](/core/modules/file/icons/application-pdf.png "application/pdf") NSDI '26 Attendee List (PDF)

![](/core/modules/file/icons/package-x-generic.png "application/zip") NSDI '26 Monday Paper Archive (157 MB ZIP, includes Proceedings front matter, errata, and attendee lists)

![](/core/modules/file/icons/package-x-generic.png "application/zip") NSDI '26 Tuesday Paper Archive (122 MB ZIP)

![](/core/modules/file/icons/package-x-generic.png "application/zip") NSDI '26 Wednesday Paper Archive (135 MB ZIP)

**Display:**

- [Column](#switcher)
- [List](#switcher)

**View mode:**

- [condensed](#switcher)
- [Standard](#switcher)
- [Expanded](#switcher)

## Monday, May 4

### 7:30 am–8:45 am

## Continental Breakfast

Grand Pre-Function Area

### 8:45 am–9:00 am

## Opening Remarks and Awards

Grand Ballroom I–VI

Program Co-Chairs: Srikanth Kandula, *Amazon Web Services;* Hakim Weatherspoon, *Cornell University*

### 9:00 am–10:00 am

## Keynote Address

Grand Ballroom I–VI

## [The Physics of Thought and the Architecture of Intelligence](/conference/nsdi26/presentation/keynote-vahdat)

Amin Vahdat, *Google*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/keynote-vahdat)

We are in a time of massive transition across technology and society. This talk explores key lessons and insights that we can learn from history as we stand at the precipice of a new epoch of computing, the era of intelligence. To prepare for this future, we first start with a historical view for parallels to inform both what we work on but also how we do so. Building on this historical perspective, we delve into the architecture of intelligence, showing that efficient scaling of compute is central to advances in the field. This scaling will come from advances in many fields, though we focus on the central role networked systems play in scaling intelligence, from TPU on-chip networks to rack-scale serving, to ML training supercomputers, to distributed control and transport over Gigawatt-scale regional computing hubs. We conclude the talk with research opportunities for the future, again drawing lessons from history to ensure that we as technologists also focus on addressing the costs of scaling intelligence, from sustainability to safety to security to societal policy.

![](https://www.usenix.org/sites/default/files/styles/speaker_photo/public/nsdi26_vahdat_amin_200x230.png)

Amin Vahdat is a Fellow and Chief Technologist for AI Infrastructure at Google, where his team is responsible for delivering industry-leading infrastructure which spans custom silicon, data centers, network, and supply chain and operations. This infrastructure serves Alphabet, Google and the world, and Artificial Intelligence technologies that empower ML developers and solve customers’ most pressing business challenges. In the past, he was Vice President and General Manager for Google's compute, storage, and network hardware and software infrastructure. Until 2019, he was the Technical Lead and Vice President for the Networking organization at Google.

Before joining Google, Amin was the Science Applications International Corporation (SAIC) Professor of Computer Science and Engineering at UC San Diego (UCSD). He received his doctorate from the University of California Berkeley in computer science, and is a Fellow of the Association for Computing Machinery (ACM).

Amin has been recognized with a number of awards, including the National Science Foundation (NSF) CAREER award, the UC Berkeley Distinguished EECS Alumni Award, the Alfred P. Sloan Fellowship, the Association for Computing Machinery's SIGCOMM Networking Systems Award, and the Duke University David and Janet Vaughn Teaching Award. Amin was awarded the SIGCOMM lifetime achievement award for his contributions to data center and wide area networks. He was inducted into the [National Academy of Engineering](https://www.nae.edu/290930/Dr-Amin-Vahdat) in 2023 for his contributions to the design and implementation of datacenter and planet-scale networks that power cloud computer systems.

### 10:00 am–10:30 am

## Coffee and Tea Break

Grand Pre-Function Area

### 10:30 am–12:10 pm

Track 1

## All Your Networks Are Belong to ML

Session Chair: Dave Maltz, *Microsoft*

Grand Ballroom I–VI

## [UNUM: A New Framework for Network Control](/conference/nsdi26/presentation/chen-jiayi)

Jiayi Chen, *UT Austin;* Nihal Sharma, *Capital One;* Debajit Chakraborty, Saurabh Agarwal, Jeffrey Zhou, Aditya Akella, and Sanjay Shakkottai, *UT Austin*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/chen-jiayi)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/chen-jiayi)

Modern network control tasks, such as congestion control and adaptive bitrate streaming, require accurate state estimation to adapt to heterogeneous and dynamic network conditions. Current approaches, whether manually engineered or machine learning (ML)-based, often rely on instantaneous or running-average metrics, resulting in imprecise approximations of the true network state. This hinders their ability to capture latent factors, such as application workloads or path dynamics, and adapt to non-stationary environments.

We present Unum, a new framework powered by a unified network state embedder leveraging Transformers' self-attention mechanism and diverse training datasets to learn rich, latent state representations. Unum processes historical RTT-timescale network statistics, models complete current state, and predicts future states using pre-trained embeddings from diverse network scenarios. We develop techniques to augment state-of-the-art controllers with Unum embeddings. Through experiments over real and synthetic settings, we show that using Unum state embeddings improves control performance across tasks, including congestion control and adaptive bitrate streaming.

## [BURST: Seeking High-performance, Interoperability and Scalability in Soft-RDMA](/conference/nsdi26/presentation/shen)

Huijun Shen, *Hunan University;* Zelong Yue, Jian Yang, Zhuo Jiang, Lang An, Yulin Chen, Yong Zhang, Luochangqi Ding, Xiaolong Zhong, Zhihong Wang, Jie Ding, Hongyu Wu, and Jianxi Ye, *ByteDance Inc.;* Xijin Yin, Xingyu Zhang, Xingyu Guo, and Guo Chen, *Hunan University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/shen)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/shen)

Modern data centers deploy heterogeneous server pods, including a mix of commercial RDMA NICs (RNICs), legacy Ethernet NICs, and custom in-house hardware. This diversity creates significant interoperability challenges, particularly for Non-RNIC-to-RNIC (NR2R) communication, a scenario driven by emerging disaggregated workloads like LLM inference, large-scale infrastructure upgrades, and the integration of novel network protocols. Due to strict hardware dependencies, RNICs discard packets from non-compliant packets, forcing a costly fallback to TCP/IP and limiting RDMA network scaling. Existing software RDMA solutions, RXE (SoftRoCE implementation in Linux kernel), suffer from prohibitive CPU overhead, making them unsuitable for high-speed networks.

To address this, we present BURST, a high-performance, user-space software RDMA stack designed for high-speed networks. BURST operates as an independent process that maintains full compatibility with the standard RDMA Verbs API, allowing unmodified applications to run on Ethernet NICs. It integrates a lock-free DPDK data plane for line-rate packet processing, leverages Intel's DSA for reducing CPU, and features a kernel-bypass connection manager to accelerate setup. Experimental results show that BURST achieves 98.7% line-rate bandwidth on 400G NICs, delivering a 3.2-6.3x throughput improvement over kernel RXE. In production workloads, BURST accelerates LLM inference latency to 25.2% of TCP's and increases connection setup speeds by 12x compared to native RDMA CM, demonstrating its benefits for unifying communication in heterogeneous environments.

## [PolicyCache: Intra-flow Learning in Congestion Control](/conference/nsdi26/presentation/tian)

Han Tian, Han Wang, and Wenbo Li, *University of Science and Technology of China;* Xudong Liao, Decang Sun, and Wenxue Li, *Hong Kong University of Science and Technology;* Donghui Chen, Bin Huang, and Senbo Fu, *Huawei Technologies Co., Ltd.;* Junxue Zhang, *University of Science and Technology of China;* Dian Shen, *Southeast University;* Kai Chen, *Hong Kong University of Science and Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/tian)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/tian)

TCP congestion control (CC) schemes must balance fast responsiveness, adaptability to diverse network conditions, and low computational overhead. Existing approaches fall short: heuristic-based algorithms are lightweight but brittle, learning-based schemes provide high responsiveness yet struggle with generalization, and exploration-based methods adapt well but converge slowly. We present PolicyCache, the first CC algorithm based on *intra-flow learning*, where both training and execution of the policy are confined to a single flow. Unlike prior inter-flow learning, this paradigm avoids cross-environment generalization pitfalls while maintaining high responsiveness. PolicyCache leverages a lightweight, non-parametric tree-based model coupled with online exploration and dynamic model switching to enable rapid and robust adaptation. We provide convergence analysis of PolicyCache and have built a fully functional Linux prototype. Extensive evaluations demonstrate that PolicyCache consistently achieves high throughput, low latency, and fairness across diverse emulated and real-world networks, while incurring minimal overhead. These results establish intra-flow learning as a practical and effective new direction for congestion control.

## [FastServe: Iteration-Level Preemptive Scheduling for Large Language Model Inference](/conference/nsdi26/presentation/wu-bingyang)

Bingyang Wu, Yinmin Zhong, Zili Zhang, Shengyu Liu, Fangyue Liu, Yuanhang Sun, Gang Huang, Xuanzhe Liu, and Xin Jin, *School of Computer Science, Peking University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wu-bingyang)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wu-bingyang)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wu-bingyang)

Large language models (LLMs) power a new generation of interactive AI applications exemplified by ChatGPT. The interactive nature of these applications demands low latency for LLM inference. Existing LLM serving systems use run-tocompletion processing for inference jobs, which suffers from head-of-line blocking and long latency.

We present FastServe, a distributed LLM serving system which exploits the autoregressive pattern of LLM inference to enable preemption at the granularity of each output token. FastServe uses preemptive scheduling to minimize latency with a novel skip-join Multi-Level Feedback Queue scheduler. Based on the new semi information-agnostic setting of LLM inference, the scheduler leverages the input length information to assign an appropriate initial queue for each arrival job to join. Queues with higher priority than the one the job joins are skipped to reduce demotions. We design an efficient GPU memory management mechanism that proactively offloads and uploads intermediate state between GPU memory and host memory for LLM inference. Evaluation shows that compared to the state-of-the-art solution vLLM, FastServe improves the throughput by up to 6.1×.

## [SYMI: Efficient Mixture-of-Experts Training via Model and Optimizer State Decoupling](/conference/nsdi26/presentation/skiadopoulos)

Athinagoras Skiadopoulos, *Stanford University;* Mark Zhao, *University of Colorado Boulder;* Swapnil Gandhi, *Stanford University and NVIDIA;* Thomas Norrie, *OpenAI;* Shrijeet Mukherjee, *NVIDIA;* Christos Kozyrakis, *Stanford University and NVIDIA*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/skiadopoulos)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/skiadopoulos)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/skiadopoulos)

Mixture-of-Experts (MoE) models have become a widely-adopted solution to continue scaling model sizes without a corresponding linear increase in compute. During MoE model training, each input token is dynamically routed to a subset of experts—sparsely-activated feed-forward networks—within each transformer layer. The distribution of tokens assigned to each expert varies widely and rapidly over the course of training. To handle the wide load imbalance across experts, current systems are forced to either drop tokens assigned to popular experts, degrading convergence, or frequently rebalance resources allocated to each expert based on popularity, incurring high state migration overheads.

To break this performance-accuracy tradeoff, we introduce SYMI, an adaptive MoE training system. The key insight of SYMI is to decouple the placement of expert parameters from their large optimizer state. SYMI statically partitions the optimizer of each expert across all training nodes. Meanwhile, SYMI dynamically adjusts the placement of expert parameters by repurposing existing weight updates, avoiding migration overheads. In doing so, SYMI right-sizes the GPU resources allocated to each expert, on a *per-iteration* basis, with minimal overhead. Compared to state-of-the-art MoE training systems, DeepSpeed and FlexMoE, SYMI is able to achieve a 30.5% and 25.9% faster time-to-convergence, respectively.

Track 2

## The Care and Feeding of Networked Systems

Session Chair: Daehyeok Kim, *The University of Texas at Austin*

Grand Ballroom VII–IX

## [Towards Performance Robustness for Microservices](/conference/nsdi26/presentation/saxena)

Divyanshu Saxena and Gaurav Vipat, *UT Austin;* Jiaxin Lin, *Cornell University;* Jingbo Wang, *Purdue University;* Isil Dillig, Sanjay Shakkottai, and Aditya Akella, *UT Austin*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/saxena)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/saxena)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/saxena)

Microservices are foundational to modern distributed applications, enabling modular design and scalability. However, they face performance variability due to environmental factors like workload burstiness, resource contention, and shared dependencies. Existing microservice controllers, such as autoscalers and admission controllers, struggle to ensure good performance, often causing several Service Level Objective (SLO) violations. We argue that this is because controller decision-making is uninformed, lacking guidance about robustness to environmental factors.

We propose the concept of run-time "performance robustness certificates" (PERCs) to address this limitation. A PERC provides statistical bounds on tail latencies of specific request types under a range of environmental perturbations. We show how to leverage a queueing-theoretic model of microservice performance to quickly derive actionable {PeRC}s. We introduce Galileo, a framework that integrates PERCs with two state-of-the-art learned controllers to guide robust actions toward meeting SLOs. Experimental results with real-world benchmarks validate the effectiveness of PERCs in ensuring robust microservice performance.

## [Pilot Execution: Simulating Failure Recovery In Situ for Production Distributed Systems](/conference/nsdi26/presentation/li-zhenyu)

Zhenyu Li, *University of Virginia;* Angting Cai, *University of California San Diego;* Chang Lou, *University of Virginia*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/li-zhenyu)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/li-zhenyu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/li-zhenyu)

Modern distributed systems rely on failure recovery to ensure availability and correctness—ironically, recovery itself often introduces severe and irreversible failures. In this paper, we first study 75 real-world recovery failures to understand common pitfalls in the recovery mechanisms. We find that the challenges primarily arise from cross-component interactions, which are difficult to expose in traditional approaches.

To address this gap, we introduce pilot execution, a new execution model that simulates dry-runs of recovery actions in production distributed systems to enable safe and predictable failure recovery. It enables systems and operators to observe recovery action effects before applying them, reducing the risk of cascading failures and unintended side effects.

We realize pilot execution with PILOT, an analysis framework with a runtime library that makes pilot execution easy to adopt. We evaluate PILOT on five large-scale distributed systems and show that PILOT uncovers 17 out of 20 recovery failures with modest overhead. Our use of PILOT also exposes an unknown recovery bug in the latest version of HBase.

## [BLADE: Adaptive Wi-Fi Contention Control for Next-Generation Real-Time Communication](/conference/nsdi26/presentation/guo-fengqian)

Fengqian Guo, *Tencent;* Yuhan Zhou, *Peking University and Tencent;* Longwei Jiang and Congcong Miao, *Tencent;* Yuxin Liu, *University at Buffalo, SUNY;* Chenren Xu, *Peking University;* Hancheng Lu, *Institute of Artificial Intelligence, China;* Chang Wen Chen, *The Hong Kong Polytechnic University;* Yaxiong Xie, *University at Buffalo, SUNY;* Honghao Liu, *Tencent*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/guo-fengqian)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/guo-fengqian)

Next-generation real-time communication (NGRTC) applications, such as cloud gaming and XR, demand consistently ultra-low latency. However, through our first large-scale measurement, we find that despite the deployment of edge servers, dedicated congestion control, and loss recovery mechanisms, cloud gaming users still experience long-tail latency in Wi-Fi networks. We further identify that Wi-Fi last-mile access points (APs) serve as the primary latency bottleneck. Specifically, short-term packet delivery droughts, caused by fundamental limitations in Wi-Fi contention control standards, are the root cause. To address this issue, we propose BLADE, an adaptive contention control algorithm that dynamically adjusts the contention windows (CW) of all Wi-Fi transmitters based on the channel contention level in a fully distributed manner. Our NS3 simulations and real-world evaluations with commercial Wi-Fi APs demonstrate that, compared to standard contention control, BLADE reduces Wi-Fi packet transmission tail latency by over 5× under heavy channel contention and significantly stabilizes MAC throughput while ensuring fast and fair convergence. Consequently, BLADE reduces the video stall rate in cloud gaming by over 90%.

## [Observability Is Eating Your Cores: Fine-Grained Analysis of Microservice Metrics with IPU-Hosted Sketches](/conference/nsdi26/presentation/cornacchia)

Alessandro Cornacchia, *King Abdullah University of Science and Technology;* Theophilus A. Benson, *Carnegie Mellon University;* Muhammad Bilal and Marco Canini, *King Abdullah University of Science and Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/cornacchia)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/cornacchia)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/cornacchia)

Observability has become mission-critical for troubleshooting cloud-native technology. However, today's observability fails to meet the demands of cloud-native environments, either resulting in crippling complexity and high costs for collecting and storing huge data volumes, or sacrificing events coverage by sampling at coarse time granularity. We present μView, which stands out from conventional cloud monitors by incorporating a lightweight observability data-plane on Infrastructure Processing Units (IPUs). Our novel architecture leverages the proximity of IPUs to the monitored services to tackle observability bloat. Crucially, μView's data-plane applies streaming data sketching techniques to continuously process and analyze microservice's metrics at fine time resolution, without hurting application performance. We show for several use cases that by anticipating SLO violations μView can help *(i)* narrow the focus on informative observability data, and *(ii)* trigger useful signals about service performance, thus enabling timely proactive actions. Our code and artifacts are available at: <https://github.com/sands-lab/uview>.

## [MirrorNet: High-fidelity and Scalable Network Emulation for Software-defined WAN](/conference/nsdi26/presentation/miao)

Congcong Miao, *Tencent;* Yuejie Wang, *Peking University;* Jianming Wang, Xuefeng Ji, Guozhi Shan, Sirui Li, Pan Fang, and Yanke Zhang, *Tencent;* Jialin Li, *National University of Singapore;* Xianneng Zou, *Tencent;* Guyue Liu, *Peking University*

Operational Systems Paper

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/miao)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/miao)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/miao)

Operating a large-scale WAN reliably is becoming increasingly challenging due to the surge in traffic volumes, and the growing complexity of both software and hardware. In this paper, we introduce MirrorNet, our production-grade emulation framework designed to mirror a software-based WAN. Unlike traditional emulators and simulators that access only a partial set of network information, MirrorNet functions as a comprehensive twin of the production network, encompassing the controller, data plane, and network traffic. Our key challenge lies in striking a balance between the requirements for a fine-grained and high-fidelity emulation, scalability, and resource efficiency. To address these, we have developed a multi-faceted approach: i) we employ an incremental storage and replay method to reconstruct the historical production network at a second-by-second level; ii) we propose a network update strategy that maintains consistent alignment between the emulation and production networks; and iii) we design a custom orchestrator capable of rapidly deploying one or more large-scale emulation networks, which can operate concurrently to expedite testing. MirrorNet has been deployed in TWAN for over 2 years and integral in our daily WAN management tasks, aiding in troubleshooting, parameter tuning, testing, and capacity assessment.

Track 3

## Mobile and Embedded Systems

Session Chair: Lili Qiu, *Microsoft Research*

Bellevue Room

## [From Bits to Tokens: Knowledge-Driven Generative Communication of Multimodal Data](/conference/nsdi26/presentation/chen-xingyu)

Xingyu Chen, *University of California San Diego;* Zihao Feng, *University of Southern California;* Wuqiong Zhao, *University of California San Diego;* Jianrong Ding, *Chinese University of Hong Kong;* Ke Sun, *University of Michigan Ann Arbor;* Xinyu Zhang, *University of California San Diego*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/chen-xingyu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/chen-xingyu)

Classical communication systems strive for bit-by-bit reconstruction, yet this objective often misaligns with downstream application tasks, such as perception and decision-making with sensor data. Strict bit-fidelity is especially problematic in wireless settings, where packet losses and channel dynamics undermine both efficiency and resilience. In this paper, we introduce Knowledge-Driven Communication (KDC), a framework that transmits semantic knowledge rather than raw bits by leveraging pretrained knowledge bases. KDC features a task-aware transmitter, which uses multimodal foundation models to abstract source data into tokenized embeddings and prioritize semantically critical content, enabling zero-shot adaptation without task-specific retraining. On the receiver side, KDC employs pretrained knowledge bases and incrementally updated context to reconstruct task-relevant information, enabling graceful degradation even under data loss. We implement a full KDC prototype and evaluate it over diverse data modalities and wireless networks. Experiments show that KDC consistently outperforms state-of-the-art codecs and learned baselines, achieving high task accuracy with a fraction of the transmitted data, while maintaining robustness under challenging wireless conditions.

## [KeepON: Supporting Deterministic Traffic on Standard NICs](/conference/nsdi26/presentation/xue-chuanyu)

Chuanyu Xue, *University of Connecticut;* Tianyu Zhang, *University of Iowa;* Andrew Loveless, *NASA Johnson Space Center;* Song Han, *University of Connecticut*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xue-chuanyu)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/xue-chuanyu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/xue-chuanyu)

Networked mission-critical applications (e.g., avionics control and industrial automation) demand deterministic packet transmissions to meet stringent sensing and control timing requirements. While specialized infrastructures such as TimeTriggered Ethernet and Time-Sensitive Networking (TSN) ensure deterministic data delivery across switches, end devices still require specialized NICs (e.g., TSN NICs or NVIDIA Mellanox) to eliminate endpoint indeterminism. However, deploying such NICs at every endpoint is costly and hinders compatibility with legacy systems. To address this challenge, we propose KeepON, a novel software-based driver model that enables deterministic packet transmission on commodity NICs. The core idea is to continuously transmit fixed-size placeholder packets, establishing a predictable transmission pattern. Mission-critical packets are then precisely inserted into this stream by replacing placeholders at their scheduled transmission slots, ensuring timing accuracy. The placeholder packets are efficiently dropped at the first-hop switch, avoiding negative impacts on network performance. We prototype KeepON by modifying the standard NIC driver of a Raspberry Pi, and integrate it into a real-world TSN testbed. Experimental results show that KeepON achieves up to 130× improvement in scheduling accuracy compared to the default driver, and 2.1× improvement over a hardware-based solution.

## [RASC: Enhancing Observability & Programmability in Smart Spaces](/conference/nsdi26/presentation/karanika)

Anna Karanika, Kai-Siang Wang, Han-Ting Liang, Shalni Sundram, and Indranil Gupta, *University of Illinois Urbana-Champaign*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/karanika)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/karanika)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/karanika)

While RPCs form the bedrock of systems stacks, we posit that IoT device collections in smart spaces like homes, warehouses, and office buildings—which are all “user-facing”—require a more expressive abstraction. Orthogonal to prior work, which improved the reliability of IoT communication, our work focuses on improving the *observability* and *programmability* of IoT actions. We present the RASC (Request-Acknowledge-Start-Complete) abstraction, which provides acknowledgments at critical points after an IoT device action is initiated. RASC is a better fit for IoT actions, which naturally vary in length *spatially* (across devices) and *temporally* (across time, for a given device). RASC also enables the design of several new features: predicting action completion times accurately, detecting failures of actions faster, allowing fine-grained dependencies in programming, and scheduling. RASC is intended to be implemented atop today’s available RPC mechanisms, rather than as a replacement. We integrated RASC into a popular and open-source IoT framework called Home Assistant. Our trace-driven evaluation finds that RASC meets latency SLOs, especially for long actions that last O(mins), which are common in smart spaces. Our scheduling policies for home automations (e.g., routines) outperform state-of-the-art counterparts by 10%-55%.

## [Decoding RSSI Compression in RFID: Dynamic RCS Modeling and Tag-Intrinsic Power Metrics for Reliable Backscatter Networks](/conference/nsdi26/presentation/liu-jia)

Jia Liu, Yifei Ma, Xingyu Chen, and Haipeng Dai, *Nanjing University;* He Huang, *Soochow University;* Zihao Lin and Wei Zheng, *Nanjing University;* Junzhao Du, *Xidian University;* Guihai Chen, *Nanjing University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/liu-jia)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/liu-jia)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/liu-jia)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/liu-jia)

Radio Frequency Identification (RFID) is a foundational element of modern IoT and backscatter networks, powering inventory, localization, and battery-free sensing at scale. In this paper, we uncover *RSSI compression*, a power-dependent bias in reader-measured RSSI, as a critical physical-layer problem that propagates upward in the network stack, degrading MAC-layer collision resolution, network-layer link estimation, and application-layer reliability. Through carefully designed experiments, we trace this distortion to dynamic tag Radar Cross Section (RCS) behavior and introduce two novel physical-layer metrics: *Interrogation Threshold Power* (ITP), a channel-specific metric for accurate link-quality estimation, and *Backscatter Power Index* (BPI), a tag-intrinsic, environment-agnostic signature. These metrics provide high-fidelity signal information that higher layers can directly exploit for more robust collision detection, power control, localization and sensing tasks. Finally, an in-situ single-query method further reduces measurement overhead by 99.8%, while cutting channel-estimation error by 64.7%, delivering significant cross-layer performance gains in real-world backscatter networks.

## [BBC: Enabling BLE to Support Bluetooth Classic](/conference/nsdi26/presentation/cho)

Hsun-Wei Cho and Kang G. Shin, *University of Michigan*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/cho)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/cho)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/cho)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/cho)

Bluetooth Classic has been the technology used by the overwhelming majority of wireless headphones. However, Bluetooth Classic is incompatible with Bluetooth Low Energy (BLE), and hence cannot directly communicate with BLE devices. With the recent shift toward BLE, this incompatibility prevents using simple, energy-efficient BLE chips with Bluetooth headphones, and requires using more complex dual-mode chips to support both Bluetooth Classic and BLE.

To overcome this incompatibility, we present BBC, which enables Bluetooth-Classic connectivity on BLE chips. BBC sends and receives raw FSK bits using BLE hardware while emulating all other Bluetooth-Classic operations in the driver. By eliminating the need for Bluetooth-Classic hardware, BBC enables future devices to use BLE-only chips while maintaining the Bluetooth-Classic compatibility via emulation. It also enables new connectivity for current BLE devices to directly stream audio to Bluetooth-Classic headphones. BBC achieves a throughput of 557kbps and a packet error rate (PER) of 4.86% at the distance of 10m, and provides the same audio quality as off-the-shelf Bluetooth-Classic chips.

### 12:10 pm–2:00 pm

## Symposium Luncheon and Test of Time Award Presentation

Lake Washington Ballroom

[Network Virtualization in Multi-tenant Datacenters](https://www.usenix.org/conference/nsdi14/technical-sessions/presentation/koponen)  
Teemu Koponen, Keith Amidon, Peter Balland, Martín Casado, Anupam Chanda, Bryan Fulton, Igor Ganichev, Jesse Gross, Natasha Gude, Paul Ingram, Ethan Jackson, Andrew Lambeth, Romain Lenglet, Shih-Hao Li, Amar Padmanabhan, Justin Pettit, Ben Pfaff, Rajiv Ramanathan, Scott Shenker, Alan Shieh, Jeremy Stribling, Pankaj Thakkar, Dan Wendlandt, Alexander Yip, and Ronghua Zhang  
*Published in the Proceedings of the 11th USENIX Symposium on Networked Systems Design and Implementation (NSDI '14)*

### 2:00 pm–3:20 pm

Track 1

## Overfitting the Internet

Session Chair: Rachee Singh, *Cornell University*

Grand Ballroom I–VI

## [SPLIDT: Partitioned Decision Trees for Scalable Stateful Inference at Line Rate](/conference/nsdi26/presentation/parvez)

Murayyiam Parvez, *Purdue University;* Annus Zulfiqar, *University of Michigan;* Roman Beltiukov, *UCSB;* Shir Landau Feibish, *University of Haifa;* Walter Willinger, *Northwestern University;* Arpit Gupta, *UCSB;* Muhammad Shahbaz, *University of Michigan*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/parvez)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/parvez)

Machine learning (ML) is increasingly being deployed in programmable data planes (switches and SmartNICs) to enable real-time traffic analysis, security monitoring, and in-network decision-making. Decision trees (DTs) are particularly well-suited for these tasks due to their interpretability and compatibility with data-plane architectures, i.e., match-action tables (MATs). However, existing in-network DT implementations are constrained by the need to compute all input features upfront, forcing models to rely on a small, fixed set of features per flow. This significantly limits model accuracy and scalability under stringent hardware resource constraints.

We present SPLIDT, a system that rethinks DT deployment in the data plane by enabling partitioned inference over sliding windows of packets. SPLIDT introduces two key innovations: (1) it groups individual subtrees of a DT into partitions and allows each subtree to have its own feature set, and (2) it leverages an in-band control channel (via recirculation) to reuse data-plane resources (both stateful registers and match keys) across partitions at line rate. These insights allow SPLIDT to scale the number of stateful features a model can use without exceeding hardware limits. To support this architecture, SPLIDT incorporates a custom training and design-space exploration (DSE) framework that jointly optimizes feature allocation, tree partitioning, and DT model depth. Evaluation across multiple real-world datasets shows that SPLIDT achieves higher accuracy while supporting up to 5x more stateful features than prior approaches (e.g., NetBeacon and Leo). It maintains the same low time-to-detection (TTD) as these systems, while scaling to millions of flows with minimal recirculation overhead (≤ 0.05%).

## [Morphe: High-Fidelity Generative Video Streaming with Vision Foundation Model](/conference/nsdi26/presentation/gong)

Tianyi Gong, Zijian Cao, and Zixing Zhang, *The Chinese University of Hong Kong, Shenzhen, and Shenzhen Future Network of Intelligence Institute;* Jiangkai Wu and Xinggong Zhang, *Peking University;* Shuguang Cui and Fangxin Wang, *The Chinese University of Hong Kong, Shenzhen, and Shenzhen Future Network of Intelligence Institute*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/gong)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/gong)

Video streaming is a fundamental Internet service, while the quality still cannot be guaranteed especially in poor network conditions such as bandwidth-constrained and remote areas. Existing works mainly work towards two directions: traditional pixel-codec streaming nearly approaches its limit and is hard to step further in compression; the emerging neural-enhanced or generative streaming usually fall short in latency and visual fidelity, hindering their practical deployment.

Inspired by the recent success of vision foundation model (VFM), we strive to *harness the powerful video understanding and processing capacities of VFM to achieve generalization, high fidelity and loss resilience for real-time video streaming with even higher compression rate.* We present Morphe, the first revolutionized paradigm that enables VFM-based end-to-end generative video streaming towards this goal. Specifically, Morphe employs joint training of visual tokenizers and variable-resolution spatiotemporal optimization under simulated network constraints. Additionally, a robust streaming system is constructed that leverages intelligent packet dropping to resist real-world network perturbations. Extensive evaluation demonstrates that Morphe achieves comparable visual quality while saving 62.5% bandwidth compared to H.265, and accomplishes real-time, loss-resilient video delivery in challenging network environments, representing a milestone in VFM-enabled multimedia streaming solutions.

## [DroidSpeak: KV Cache Sharing Across Fine-tuned Model Variants](/conference/nsdi26/presentation/liu-yuhan)

Yuhan Liu, Yuyang Huang, Jiayi Yao, Shaoting Feng, Zhuohan Gu, Kuntai Du, Hanchen Li, Yihua Cheng, and Junchen Jiang, *University of Chicago;* Shan Lu, Madan Musuvathi, and Esha Choukse, *Microsoft*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/liu-yuhan)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/liu-yuhan)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/liu-yuhan)

*Compound AI systems*, such as agentic systems, are an emerging trend in large-scale enterprise settings, with multiple LLMs specialized for different users, tasks, and/or roles working together. In these scenarios, different models often process inputs that share the same context prefix. Although much work was done in the past to enable the reuse of prefix KV caches across inputs for a single model, how to enable one model to reuse the prefix KV caches of a different model remains an open question.

We introduce DroidSpeak, the first distributed LLM inference system that enables KV cache reuse across distributed nodes running inference of different LLMs, so long as the LLMs have the same architecture. We present the first study that aims at understanding the impact of sharing KV caches across different LLMs, and if/when such sharing affects quality. Inspired by the findings, we present DroidSpeak, which selectively recomputes a few layers of the KV cache produced by another LLM and reuses the remaining layers, with negligible quality loss. Moreover, carefully pipelining the layer-wise re-computation and the loading of reused KV cache further improves the inference performance. Experiments on diverse datasets and model pairs demonstrate that DroidSpeak achieves up to 4x throughput improvement and about 3.1× faster prefill (time to first token), with negligible loss of quality in F1 scores, Rouge-L or code similarity score, compared to the baseline which does not allow any sharing across models.

## [Checkmate: Zero Performance Overhead Model Checkpointing via Network Gradient Replication](/conference/nsdi26/presentation/bhardwaj)

Ankit Bhardwaj, *Tufts University;* Weiyang Wang, Jeremy Carin, Adam Belay, and Manya Ghobadi, *Massachusetts Institute of Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/bhardwaj)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/bhardwaj)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/bhardwaj)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/bhardwaj)

This paper presents Checkmate, a system that enables per-iteration checkpointing in DNN training without any training slowdown. The traditional approach to checkpointing requires a pause in training to copy model states to a separate location, allowing the state to be restored in the event of failure. This approach fundamentally has a tradeoff between the frequency of checkpoints and the cost of a failure. We avoid this tradeoff; our key insight is that in data-parallel training, all information necessary to create a checkpoint already exists in the network as gradients. Our core contribution is a new multicast abstraction that simultaneously delivers gradients to a separate CPU-based shadow cluster. The shadow maintains a checkpoint by applying those gradients to a copy of the model. Our evaluation shows that Checkmate performs per-iteration checkpointing with training throughput comparable to an ideal no-checkpoint baseline. Checkmate achieves 5 to 34.5× more frequent checkpointing compared to state-of-the-art checkpointing systems, resulting in 80% to 97.1% reduction in repeated work per failure. At the same checkpointing frequency, Checkmate delivers 1.3× to 6.5× throughput compared to other systems.

Track 2

## Cloudy with a Chance of Tenants

Session Chair: Seojin Park, *University of Southern California*

Grand Ballroom VII–IX

## [HybridMesh: A Hardware-software Hybrid Approach for Accelerating Service Mesh Ingress](/conference/nsdi26/presentation/you)

Myoungsung You, *University of Seoul;* Jaehyun Nam, *Dankook University;* Minjae Seo, *ETRI;* Taejune Park, *Chonnam National University;* Seungwon Shin, *KAIST*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/you)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/you)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/you)

Service meshes have become essential for enabling microservice communication in cloud environments. Despite their benefits, they impose significant network overhead. We identify the ingress gateway, a main entry point for external traffic, has emerged as a major performance bottleneck. This overhead stems from two key limitations of current ingress gateways: (1) CPU-intensive traffic analysis and (2) a complex packet forwarding path. Our analysis shows that these inefficiencies can reduce network throughput by up to 4× while substantially increasing CPU utilization. In response, we propose HybridMesh, a hardware-software hybrid ingress gateway that leverages a SmartNIC for high-performance traffic analysis and efficient traffic routing. This process is augmented by a lightweight CPU-side proxy that provides various traffic management features not suitable for SmartNIC execution. Evaluations show that HybridMesh outperforms existing ingress gateways, achieving a 4.4× increase in HTTP throughput. Furthermore, compared to software-only and hardware-only designs, our hybrid design delivers 2.3× higher cost-effectiveness and 2.8× better power-efficiency.

## [Di-PS: System-Algorithm Co-Design for Asynchronous and Heterogeneous Cross-cluster LLM Training at Scale](/conference/nsdi26/presentation/li-shengwei)

Shengwei Li, *National Key Laboratory of Parallel and Distributed Computing;* Qiaoling Chen, *Shanghai Artificial Intelligence Laboratory and Nanyang Technology University;* Zhiquan Lai, *National Key Laboratory of Parallel and Distributed Computing;* Penglong Jiao, Wenwen Qu, Kun Cai, Jiaxing Li, Peng Sun, and Xingcheng Zhang, *Shanghai Artificial Intelligence Laboratory;* Xiaoge Deng, Dongsheng Li, and Kai Lu, *National Key Laboratory of Parallel and Distributed Computing;* Tianwei Zhang, *Nanyang Technological University*

Operational Systems Paper

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/li-shengwei)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/li-shengwei)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/li-shengwei)

Large language models (LLMs) have revolutionized artificial intelligence, exhibiting remarkable performance in various tasks. Training these models demands extensive computational resources, which are often economically and physically prohibitive. *Cross-cluster training* can balance infrastructure costs, alleviate physical and resource constraints, better match workload demands, and sustain higher efficiency through geo-distributed deployment. However, challenges arise from network variability, heterogeneous computational resources, and intrinsic training instability.

To address these issues, we present Di-PS, a novel framework for cross-cluster LLM training at scale. The core of Di-PS is the system-algorithm co-design of a parameter server paradigm, to achieve heterogeneous, asynchronous, and resilient training across decentralized clusters. We make several innovative contributions in Di-PS, including (i) an efficient parameter server design for cross-cluster communication of LLM parameters, (ii) a pseudo-gradient penalty strategy for convergence stability enhancement of asynchronous two-stage optimization, and (iii) a resilience mechanism for fault tolerance in cross-cluster training. Results from the controlled experimental setting demonstrate that Di-PS improves training efficiency by up to 4.67× over synchronous cross-cluster approaches while maintaining model quality, and achieving near-linear scalability in heterogeneous training resources. Di-PS has been deployed in the production environment, involving dynamic training scales with up to 9 clusters and more than 10,000 NPUs. At this scale, Di-PS enables successful cross-cluster training of a 100B-parameter LLM with only 6% overhead compared to single-cluster training, and effectively handles frequent failures and resource changes.

## [Stimpack: An Adaptive Rendering Optimization System for Scalable Cloud Gaming](/conference/nsdi26/presentation/heo)

Jin Heo, *Dolby Laboratories;* Vic Wang, Ketan Bhardwaj, and Ada Gavrilovska, *Georgia Institute of Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/heo)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/heo)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/heo)

In distributed multimedia applications, content is often delivered to users in a degraded form due to network-induced lossy compression. Real-time and interactive use cases like cloud gaming, which render content on the fly, require low latency and are hosted at resource-constrained edge servers. We present a new insight: when rendered content is delivered over a network with lossy compression, high-quality rendering can be ineffective in improving user-perceived quality, leading to a poor return on computing resources. Leveraging this observation, we built Stimpack, a novel system that adaptively optimizes game rendering quality by balancing server-side rendering costs against user-perceived quality. The system uses a mechanism that quantifies the efficiency of resource usage to maximize overall system utility in multi-user scenarios. Our open-sourced implementation and extensive evaluations show that Stimpack achieves up to 24% higher service quality and serves twice as many users with the same resources compared to baselines. A user study further validates that Stimpack provides a measurably better user experience.

## [HydraServe: Minimizing Cold Start Latency for Serverless LLM Serving in Public Clouds](/conference/nsdi26/presentation/lou)

Chiheng Lou, Sheng Qi, and Chao Jin, *School of Computer Science, Peking University;* Dapeng Nie, Haoran Yang, and Yu Ding, *Alibaba Group;* Xuanzhe Liu and Xin Jin, *School of Computer Science, Peking University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lou)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lou)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/lou)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/lou)

With the proliferation of large language model (LLM) variants, developers are turning to serverless computing for cost-efficient LLM deployment. However, public cloud providers often struggle to provide performance guarantees for serverless LLM serving due to significant cold start latency caused by substantial model sizes and complex runtime dependencies. To address this problem, we present HydraServe, a serverless LLM serving system designed to minimize cold start latency in public clouds. HydraServe proactively distributes models across servers to quickly fetch them, and overlaps cold-start stages within workers to reduce startup latency. Additionally, HydraServe strategically places workers across GPUs to avoid network contention among cold-start instances. To minimize resource consumption during cold starts, HydraServe further introduces pipeline consolidation that can merge groups of workers into individual serving endpoints. Our comprehensive evaluations under diverse settings demonstrate that HydraServe reduces the cold start latency by 1.7×–4.7× and improves service level objective attainment by 1.43×–1.74× compared to baselines.

Track 3

## Storage Systems and Architecture

Session Chair: Jonathan Mace, *Microsoft Research*

Bellevue Room

## [FalconFS: Distributed File System for Large-Scale Deep Learning Pipeline](/conference/nsdi26/presentation/xu)

Jingwei Xu, *Shanghai Jiao Tong University and Huawei Technologies;* Junbin Kang, *Huawei Technologies;* Mingkai Dong, *Shanghai Jiao Tong University;* Mingyu Liu, Lu Zhang, Shaohong Guo, and Ziyan Qiu, *Huawei Technologies;* Mingzhen You and Ziyi Tian, *Shanghai Jiao Tong University;* Anqi Yu, Tianhong Ding, and Xinwei Hu, *Huawei Technologies;* Haibo Chen, *Shanghai Jiao Tong University and Huawei Technologies*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xu)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xu)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/xu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/xu)

Client-side metadata caching has long been considered an effective method for accelerating metadata operations in distributed file systems (DFSs). However, we have found that client-side state (e.g., caching) is not only ineffective but also consumes valuable memory resources in the deep learning pipelines. We thus propose FalconFS, a DFS optimized for deep learning pipelines with the stateless-client architecture. Specifically, instead of performing client-side path resolution and caching, FalconFS efficiently resolves paths on the server side using *hybrid metadata indexing* and *lazy namespace replication*. FalconFS also boosts server concurrency with *concurrent request merging* and provides easy deployment with *VFS shortcut*. Evaluations against CephFS and Lustre show that FalconFS achieves up to 5.72× throughput for small file read/write and up to 12.81× throughput for deep learning model training. FalconFS has been running in Huawei autonomous driving system's production environment with 10,000 NPUs for one year and has been open-sourced.

## [DistVS: Large-scale Vector Search with Compute-Memory Disaggregation](/conference/nsdi26/presentation/yin)

Peiqi Yin, *The Chinese University of Hong Kong;* Xiao Yan, *Wuhan University;* Shiyuan Deng, *Huawei Cloud;* Hui Li, Yifan Zhu, and Xiangyu Zhi, *The Chinese University of Hong Kong;* Jingqi Mao, Ran Xu, and Wenliang Zhang, *Huawei Cloud;* James Cheng, *The Chinese University of Hong Kong*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/yin)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/yin)

Similarity-based vector search, also known as ANNS, underlies many important applications such as content search, recommender system, and retrieval-augmented generation (RAG). However, vector search has a high storage demand due to large datasets and incurs costly IOs for its fine-grained access to the vectors and index. We observe that a compute-memory disaggregation architecture can tackle these challenges and design the DistVS system with a three-tier storage layout. In particular, the compute servers keep the small but low-precision compressed vectors, a more capacious memory server stores larger high-precision compressed vectors along with the index, while the full-precision exact vectors are kept on SSDs. The idea is to progressively prune the vector accesses along the low-high-full precisions from the compute servers to the SSDs, aligning with the storage hierarchy of memory-network-disk with gradually larger capacity but higher IO cost. To effectively utilize the three vector previsions, we design an algorithm called PRESS to conduct vector search. To improve performance, DistVS incorporates system optimizations including asynchronous execution, RDMA IO batching, and decoupled re-ranking. We compare DistVS with state-of-the-art disk-based and distributed vector search systems and show that DistVS consistently outperforms them and usually improves their query throughput by over 40%.

## [Lemonshark: Asynchronous DAG-BFT With Early Finality](/conference/nsdi26/presentation/hu-michael)

Michael Yiqing Hu, Alvin Hong Yao Yan, Yihan Yang, Xiang Liu, and Jialin Li, *National University of Singapore*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/hu-michael)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/hu-michael)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/hu-michael)

DAG-Rider popularized a new paradigm of DAG-BFT protocols, separating dissemination from consensus: all nodes disseminate transactions as blocks that reference previously known blocks, while consensus is reached by electing certain blocks as leaders. This design yields high throughput but confers optimal latency only to leader blocks; non-leader blocks cannot be committed independently.

We present Lemonshark, an asynchronous DAG-BFT protocol that reinterprets the DAG at a transactional level and identifies conditions where commitment is sufficient—but not necessary—for safe results, enabling nodes to finalize transactions before official commitment, without compromising correctness. Compared to the state-of-the-art asynchronous BFT protocol, Lemonshark reduces latency by up to 65%.

## [CacheCatalyst: Enhancing Web Caching for the Latency-Constrained Internet](/conference/nsdi26/presentation/hosseini)

Mohammad Hosseini, *Shahid Beheshti University;* Sina Darabi, *Università della Svizzera italiana;* Hannaneh B. Pasandi, *University of California, Berkeley;* Patrick Eugster, *Università della Svizzera italiana;* Mahmood Choopani, *Shahid Beheshti University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/hosseini)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/hosseini)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/hosseini)

Caching is a fundamental technique for improving web performance, particularly by reducing page load time through the reuse of previously fetched resources. In this paper, we highlight the drawbacks of the current caching approach, especially in the context of high-speed networks where latency, rather than bandwidth, has become the main bottleneck for web performance. We discuss how the current design of web caching suffers from inefficiencies, particularly due to the latency involved in re-validation requests, which diminishes the potential benefits of caching. To address this inefficiency, we present CacheCatalyst, a novel solution that introduces an early cache validation procedure during the initial step of page loading. This updates the state of cached resources, enabling browsers to utilize unchanged cached content without unnecessary round trips. In addition, our approach enables an optimized form of Server Push that avoids the typical drawbacks of this mechanism. Our evaluations demonstrate that this method improves key performance metrics of page loading by an average of 40%.

### 3:20 pm–3:50 pm

## Coffee and Tea Break

Grand Pre-Function Area

### 3:50 pm–5:30 pm

Track 1

## Clouds with Benefits

Session Chair: Maria Apostolaki, *Princeton University*

Grand Ballroom I–VI

## [ZooRoute: Enhancing Cloud-Scale Network Reliability via Candidate Path Provisioning and Overlay Proactive Rerouting](/conference/nsdi26/presentation/sun)

Xiaoqing Sun, *Alibaba Cloud;* Xing Li, *Zhejiang University and Alibaba Cloud;* Xionglie Wei, Tian Pan, Ju Zhang, Bowen Yang, Yi Wang, Ye Yang, Yu Qi, Le Yu, Chenhao Jia, Zhanlong Zhang, Xinyu Chen, Xiaobo Xue, Jianyuan Lu, Shize Zhang, Enge Song, and Yang Song, *Alibaba Cloud;* Rong Wen, *Fudan University and Alibaba Cloud;* Biao Lyu, *Alibaba Cloud and Hangzhou Alibaba Cloud Feitian Information Technology and Hangzhou Alibaba Feitian Information Technology;* Yang Xu, *Fudan University;* Shunmin Zhu, *Alibaba Cloud and Hangzhou Feitian Cloud*

Operational Systems Paper

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/sun)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/sun)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/sun)

Failures are inevitable in production-scale cloud networks, making reliability a critical concern for both cloud service providers (CSPs) and their tenants. Existing network failure recovery solutions either fail to provide timely failover or require underlay upgrades, forcing tenants to deploy their own high availability systems with additional CapEX & OpEx. However, most tenants lack the expertise or willingness to invest in such systems but are highly sensitive to service disruptions. This motivates CSPs to assume the responsibility of fast and deterministic failure recovery as a cloud service.

In this work, we present ZooRoute, a tenant-transparent, underlay-agnostic network failure recovery service in Alibaba Cloud. ZooRoute leverages the overlay layer and enables failure bypass by modifying outer source ports during VXLAN tunnel encapsulation. A set of source port candidates per destination IP are maintained by proactive probing between tunnel endpoints to guarantee one-shot deterministic traffic reroute onto healthy paths. However, scaling such design at planet-scale cloud infra brings challenges such as probing overhead at hypervisors, memory consumption at Tofino gateways, and service disruptions at stateful middleboxes, which we address with a range of novel techniques. Deployed in Alibaba Cloud for 26 months, ZooRoute has significantly improved network reliability, reducing cumulative outage time by 93.19% and masking 98.21% of failures from tenant awareness.

## [Remote TCP Connection Offload and Applications](/conference/nsdi26/presentation/li-shuo)

Shuo Li, Steven Chien, Tianyi Gao, and Michio Honda, *University of Edinburgh*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/li-shuo)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/li-shuo)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/li-shuo)

Layer 7 load balancers (L7LBs) play an important role in per-request server selection within long-lived connections and transport- or application-layer protocol translation. However, L7LBs introduce substantial CPU and network overhead.

We present XO, which enables an L7LB to *offload* transport-layer and application request processing to backend servers at request granularity. XO outperforms conventional L7LBs by 27–365% in throughput through efficient utilization of server CPU and network resources. We apply XO to two real-world applications, Ceph and nginx, improving throughput by up to 135% and 300%, respectively.

## [OSCAR: O(1)-Step Convergence and Readily-deployable Congestion Control](/conference/nsdi26/presentation/zhang-zhaochen)

Zhaochen Zhang, Feiyang Xue, and Rui Ning, *Nanjing University;* Keqiang He, *Shanghai Jiao Tong University;* Gianni Antichi, *Politecnico di Milano & Queen Mary University of London;* Jiaqi Gao, *unaffiliated;* Zhimeng Yin, *City University of Hong Kong;* Kexin Liu, Rui Li, Zhengqi Cui, Zhehao Lin, Peirui Cao, Guihai Chen, and Chen Tian, *Nanjing University*

***Awarded Outstanding Paper!***

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhang-zhaochen)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhang-zhaochen)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhang-zhaochen)

Datacenter CCs typically target full bandwidth utilization and minimal queueing delay and strive to converge to these targets as quickly as possible. State-of-the-art CCs exhibit different convergence speeds, with the fastest ones converging in *O*(1) steps, which means reaching the target in constant time regardless of network conditions. However, their reliance on network features makes them not readily deployable. For instance, precise-INT-based CCs, such as HPCC and PowerTCP, achieve *O*(1)-step convergence through MIMD operations based on precise congestion information from the lengthy INT header, which is challenging to support for high-speed commodity hardware. Our key insight is that delay and delay gradient can exhibit precision comparable to INT, enabling *O*(1)-step convergence without specialized network features. Based on this insight, we propose OSCAR, the first *O*(1)-Step Convergence And Readily-deployable CC. OSCAR introduces novel techniques to accurately estimate the delay gradient with minimal overhead, eliminate overreaction in MIMD updates, and coordinate independent control loops to converge to one target. Testbed evaluations demonstrate OSCAR can rapidly converge to the fair share under real-world noise. In large-scale simulations with realistic workloads, OSCAR consistently outperforms precise-INT-based CCs by 12%-48% on average FCT and 40%-74% on tail FCT.

## [Bifrost: Alibaba's Next-Generation VPC Network with High-Performance Multipath Reliable Transport](/conference/nsdi26/presentation/fan)

Zihao Fan, *Shanghai Jiao Tong University and Alibaba Cloud;* Xing Li, *Zhejiang University and Alibaba Cloud;* Ye Yang, *Alibaba Cloud;* Bo Jiang, *Shanghai Jiao Tong University;* Bowen Yang, Yilong Lv, Yuke Hong, Yinian Zhou, Junnan Cai, Jiayue Xu, Yunrui Hu, Zhao Gao, Ke Sun, Yimin Liu, Xiangdong Zhang, Enge Song, Jianyuan Lu, Xiaoqing Sun, Shize Zhang, Haonan Li, Mingxin Li, Changgang Zheng, Yang Song, Jun Liang, and Biao Lyu, *Alibaba Cloud;* Rong Wen, *Fudan University and Alibaba Cloud;* Zhigang Zong and Shunmin Zhu, *Alibaba Cloud*

Operational Systems Paper

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/fan)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/fan)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/fan)

Virtual Private Cloud (VPC) has become an increasingly important infrastructure-level service that provides isolated virtual networking environments for cloud tenants. In Alibaba Cloud, over 80% of tenant applications require reliable data transport, which is currently implemented in VPC networks through guest-side TCP. However, TCP often suffers significant performance degradation when facing network instabilities in production clouds, especially for tail-latency sensitive applications such as Redis and Nginx. In this paper, we present Bifrost, the next-generation VPC network in Alibaba Cloud that provides high-performance multipath reliable transport. Bifrost employs RTT-aware multipath packet spraying to bypass failures and mitigate elephant flows, ensures in-order delivery via in-place guest reordering, achieves end-to-end reliability with delayed bitmap ACKs, and performs efficient reliability state management to support large-scale deployment. Extensive evaluation shows that Bifrost reduces tail latency by up to 307× for Redis and 66× for Nginx, achieves millisecond-level failure recovery, and supports O(100k) concurrent connections per SmartNIC.

## [Attack of the Bubbles: Straggler-Resilient Pipeline Parallelism for Large Model Training](/conference/nsdi26/presentation/wu-tianyuan)

Tianyuan Wu, Lunxi Cao, Hanfeng Lu, and Xiaoxiao Jiang, *Hong Kong University of Science and Technology;* Yinghao Yu, Siran Yang, Guodong Yang, Jiamang Wang, Lin Qu, and Liping Zhang, *Alibaba Group;* Wei Wang, *Hong Kong University of Science and Technology*

***Awarded Outstanding Paper!***

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wu-tianyuan)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wu-tianyuan)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wu-tianyuan)

Training large Deep Neural Network (DNN) models at scale often encounters straggler issues, mostly in communications due to network congestion, RNIC/switch defects, or topological asymmetry. Under advanced pipeline parallelism, even minor communication delays can induce significant training slowdowns. This occurs because (1) slow communication disrupts the pipeline schedule, creating cascading “bubbles” in a domino effect, and (2) current GPU kernel scheduling is susceptible to head-of-line blocking, where slow communication blocks subsequent computations, further adding to these bubbles. To address these challenges, we present PIPEMORPH, a straggler-resilient training system with two key optimizations. First, it optimally adapts the pipeline schedule in the presence of stragglers to absorb communication delays without inducing cascading bubbles, using a simple yet effective algorithm guided by an analytical model. Second, upon detecting slow communication, PIPEMORPH offloads communication operations from GPU to host memory and utilizes CPU-side RDMA for data transfer. This eliminates head-of-line blocking as subsequent computation kernels can be scheduled immediately on GPUs. Together, these optimizations effectively reduce pipeline stalls in the presence of communication stragglers, improving the training iteration time by 1.2-3.5× in our experiments under various settings.

Track 2

## Managing Complexity at Scale

Session Chair: Qizhe Cai, *University of Virginia and Enfabrica*

Grand Ballroom VII–IX

## [R-TCP: A Framework to Optimize TCP Performance Over Rate-Limiting Networks](/conference/nsdi26/presentation/zhu)

Shengtong Zhu, *The Chinese University of Hong Kong;* Yan Liu and Lingfeng Guo, *Independent Researcher;* Jack Yiu Bun Lee, *The Chinese University of Hong Kong*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhu)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhu)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhu)

Many mobile operators provide subscription plans that include a data quota for full-speed access, beyond which the service will be throttled to a low data rate — rate-limited service. This is designed to control costs and to motivate users to upgrade. Our recent measurements in a country-scale service suggested that the proportion of TCP flows subjected to rate limiting can be as high as 28%. More importantly, TCP flows under rate limiting can exhibit excessive retransmission rates, exceeding 20% in many cases. The extra bandwidth costs incurred by the retransmissions for large service providers are very significant, not to mention bandwidth wastage. This work develops a novel R-TCP framework to mitigate the excessive retransmissions problems in various TCP designs (e.g., Cubic and BBR) under rate limiting networks. R-TCP is specifically designed and optimized for sender-side kernel implementation with minimal overheads. It has been implemented into Linux where extensive experiments in real-world networks and applications show that it can substantially reduce excessive retransmissions by up to 88% with negligible tradeoff in goodput and application-layer performance.

## [Slowpoke: End-to-end Throughput Optimization Modeling for Microservice Applications](/conference/nsdi26/presentation/xie)

Yizheng Xie, Di Jin, and Oğuzhan Çölkesen, *Brown University;* Vasiliki Kalavri and John Liagouris, *Boston University;* Nikos Vasilakis, *Brown University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xie)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xie)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/xie)

Slowpoke is a new system to accurately quantify the effects of hypothetical optimizations on end-to-end throughput for microservice applications, without relying on tracing or a priori knowledge of the call graph. Microservice operators can use Slowpoke to ask what-if performance analysis questions of the form *"What throughput could my retail application sustain if I optimized the shopping cart service from 10K req/s to 20K req/s?"*. Given a target service and its hypothetical optimization, Slowpoke employs a performance model that determines how to selectively slow down non-target services to preserve the relative effect of the optimization. It then performs profiling experiments to predict the end-to-end throughput, as if the optimization had been implemented. Applied to four real-world microservice applications, Slowpoke accurately quantifies optimization effects with a root mean squared error of only 2.07%. It is also effective in more complex scenarios, e.g., predicting throughput after scaling optimizations or when bottlenecks arise from mutex contention. Evaluated in large-scale deployments of 45 nodes and 108 synthetic benchmarks, Slowpoke further demonstrates its scalability and coverage of a wide range of microservice characteristics.

## [CrossCheck: Input Validation for WAN Control Systems](/conference/nsdi26/presentation/krentsel)

Alexander Krentsel, *UC Berkeley and Google;* Rishabh Iyer, *UC Berkeley;* Isaac Keslassy, *Technion and UC Berkeley;* Bharath Modhipalli, *Google;* Sylvia Ratnasamy, *UC Berkeley and Google;* Anees Shaikh and Rob Shakir, *Google*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/krentsel)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/krentsel)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/krentsel)

We present CrossCheck, a system that validates inputs to the Software-Defined Networking (SDN) controller in a Wide Area Network (WAN). By detecting incorrect inputs—often stemming from bugs in the SDN control infrastructure—CrossCheck alerts operators before they trigger network outages.

Our analysis at a large-scale WAN operator identifies invalid inputs as a leading cause of major outages, and we show how CrossCheck would have prevented those incidents. We deployed CrossCheck as a shadow validation system for four weeks in a production WAN, during which it accurately detected the single incident of invalid inputs that occurred while sustaining a 0% false positive rate under normal operation, hence imposing little additional burden on operators. In addition, we show through simulation that CrossCheck reliably detects a wide range of invalid inputs (e.g., detecting demand perturbations as small as 5% with 100% accuracy) and maintains a near-zero false positive rate for realistic levels of noisy, missing, or buggy telemetry data (e.g., sustaining zero false positives with up to 30% of corrupted telemetry data).

## [Detecting and Diagnosing Errors in Serving Archived Web Pages](/conference/nsdi26/presentation/zhu-jingyuan)

Jingyuan Zhu, *University of Michigan;* Huanchen Sun and Harsha V. Madhyastha, *University of Southern California*

***Community Award Winner!***

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhu-jingyuan)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhu-jingyuan)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhu-jingyuan)

Web archives crawl and save copies of pages from the web, enabling users to interact with web pages in the form they existed in the past. Prior to serving any archived page, an archive rewrites the page’s source so that users’ browsers fetch the page’s resources from the archive, not from the servers which originally hosted them. But, on many modern pages, an archive’s edits to crawled scripts result in a loss of fidelity, i.e., an archived copy fails to accurately mimic the original page even when the archive had crawled all resources on the page.

To help the developers of archival systems identify and fix the bugs which result in incorrect rewrites of crawled pages, we present FidEx. First, FidEx enables accurate identification of the pages on which an archive violates fidelity. It does so by tracking and comparing the execution of scripts between when a page is crawled and when its copy is loaded. In comparison to existing methods which compare the two loads using either screenshots or the errors reported by the browser, FidEx reduces the false positive rate from around 70% to less than 10%. Second, on every page on which it identifies a loss of fidelity, FidEx pinpoints which subset of the archive’s edits to the page are erroneous. Leveraging this input to fix bugs in the most widely used archival system, we reduced the fraction of archived pages which violate fidelity from 15% to 9%.

## [Skyline: A Cloud Centric Internet Monitoring Engine](/conference/nsdi26/presentation/guo-shixian)

Shixian Guo, *ByteDance;* Ziqian Liu, *The University of Hong Kong;* Yangyang Bai, Yuan Chen, Kefei Liu, Qi Zhang, Songlin Liu, Yang Lv, Jianwei Hu, Gen Li, Zhenyang Zhong, Sisi Wen, Yongbin Dong, Feng Luo, Anjian Chen, Rui Han, Jiale Feng, Lingpei Meng, Siwan Chen, Hang Li, Shuai Xu, Juntao Zhong, and Chaoran Hu, *ByteDance;* Yibo Huang, *University of Michigan;* Yiming Qiu, *The University of Hong Kong*

Operational Systems Paper

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/guo-shixian)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/guo-shixian)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/guo-shixian)

Cloud providers depend on the public Internet to connect tenants and their clients, yet Internet faults are a leading cause of cloud outages: in our organization, more than 60% of network incidents happen in the Internet and account for close to 80% of user-impacting events. Effectively monitoring the Internet is challenging for cloud providers because they lack direct control and visibility into Internet internals. Our key insight is to treat coverage as a first-class goal and decompose the monitoring requirements into three *coverage dimensions*—*traffic direction*, *incident lifecycle*, and *tenant granularity*—then resolve each independently. We present Skyline, a cloud-centric Internet monitoring system that addresses all coverage dimensions at scale by combining purpose-built dataplane hooks with lightweight software control to minimize resource overhead, shorten reaction time, and preserve non-intrusiveness. Skyline has been deployed for more than two years. In 2025, it identified over 2,000 incidents with very high precision and recall over confirmed issues, thereby significantly improving the reliability of our cloud network.

Track 3

## Trust but Verify

Session Chair: Ryan Beckett, *Microsoft*

Bellevue Room

## [Feedback-guided Adaptive Testing of Distributed Systems Designs](/conference/nsdi26/presentation/li)

Ao Li, *Carnegie Mellon University;* Ankush Desai, *Amazon Web Services;* Rohan Padhye, *Carnegie Mellon University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/li)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/li)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/li)

Validating distributed systems for correctness poses significant challenges. Practitioners often rely on formal models of core system designs, which are then tested by exploring possible component interactions. Unfortunately, standard testing approaches based on random sampling of the state space are inefficient and prone to missing subtle bugs, as they lack guidance from the system's behavior.

To address this, we present Fest, a new testing system for formal models of distributed systems. Fest incorporates feedback-guided adaptive schedule generation, drawing inspiration from grey-box fuzzing, to steer exploration towards maximizing behavioral coverage and uncovering bugs more effectively. Our implementation in the P programming framework demonstrates significant improvements across 94 distributed system model configurations: up to 41× (1.5× average) improvement in behavioral coverage, 278× (15× average) improvement in scenario coverage, and 33% more bugs detected compared to existing methods. These results highlight Fest's effectiveness in ensuring the robustness of distributed systems through improved testing efficiency.

## [From Intention to Practice: Towards Systematic Validation of NIDS Rule Enforcement](/conference/nsdi26/presentation/liu-huan)

Huan Liu, *Huazhong University of Science and Technology;* Haoyu Chen, *Zhejiang Lab;* Biang Xu, *Huazhong University of Science and Technology and Jinyinhu Laboratory;* Jingyao Zhou, *Huazhong University of Science and Technology;* Bin Yuan, *Huazhong University of Science and Technology and Songshan Laboratory;* Qiankun Zhang, *Huazhong University of Science and Technology;* Deqing Zou, *Huazhong University of Science and Technology and Jinyinhu Laboratory;* Hai Jin, *Huazhong University of Science and Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/liu-huan)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/liu-huan)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/liu-huan)

Rule-based Network Intrusion Detection Systems (NIDS) are integral to contemporary cybersecurity, relying on the rule matching mechanism to identify malicious activities within network traffic. However, there is no inherent assurance that the deployed rules are enforced as intended due to factors regarding the composition of the rules and implementation flaws of NIDS. Unfortunately, administrators lack appropriate means to validate the gap between rule definition and enforcement as existing testing approaches towards NIDS are often rule irrelevant and lack systematic methodologies. To address this issue, this paper presents **NIDSFuzz**, a systematic fuzzing approach designed to validate the enforcement of rules within NIDS, which is rule-oriented so that it employs tailored mutation strategies to generate test traffic based on the very ruleset deployed. In this manner, it becomes feasible to validate the targeted rulesets with guarantee of coverage. An NIDS-specific fuzzing framework is proposed, incorporating an appropriate test traffic injection method to perform fuzzing and carefully designed approaches of sanitization and analysis to effectively identify rule enforcement issues. Experimental results show that **NIDSFuzz** is able to uncover over 10,000 rule enforcement issues. We classified the discovered issues into different categories and explored corresponding countermeasures in terms of both rules and NIDS implementation. Moreover, performance evaluation confirms the efficiency of **NIDSFuzz** and comparison to other tools highlights the significant advantage of **NIDSFuzz** in evaluating rules of NIDS. We have made our code publicly available.

## [Count-Based Abstractions for Performance Verification of Contention Points](/conference/nsdi26/presentation/seyhani)

Amir Seyhani, *University of Waterloo;* Aarti Gupta and David Walker, *Princeton University;* Mina Tahmasbi Arashloo, *University of Waterloo*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/seyhani)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/seyhani)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/seyhani)

Networking researchers and engineers spend much of their time trying to understand the performance of *contention points* – network components where multiple incoming packet streams share the same outgoing link(s). Recently, researchers have developed new logical models for analyzing such contention points, but unfortunately, such models are expensive: They do not scale well as buffer capacities increase beyond 10s of packets, making it difficult or impossible to reason about real-world systems faithfully. In this paper, we develop a suite of effective, new abstractions for reasoning about buffers and their performance characteristics. We also show how to architect a performance analysis framework for contention points in a modular way so it can take advantage of a range of abstractions that trade performance off against precision. We evaluate our abstractions against a collection of benchmarks and demonstrate their scaling benefits.

## [Iceberg: Automated Verification of DNS Authoritative Engines via Just-in-Time Summarization](/conference/nsdi26/presentation/xiang-iceberg)

Yuxing Xiang, Rilin Huang, Naiqian Zheng, and Xin Jin, *Peking University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xiang-iceberg)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/xiang-iceberg)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/xiang-iceberg)

As the core of DNS services, DNS authoritative engines are responsible for answering DNS queries with DNS responses, where any bugs may lead to severe consequences. While it is critical to ensure the correctness of the engine, existing solutions fail to deliver both correctness guarantees and low manual effort when applied to large and complex implementations in use. The state-of-the-art solution, DNS-V, relies on extra manual specifications for scaling verification, which still incurs a prohibitive cost.

In this paper, we present Iceberg, an automated verification framework for DNS authoritative engines that holistically reduces manual effort. To achieve this, we propose *just-in-time (JIT) summarization*, a refinement-proof approach that utilizes invariants from DNS zones to enable the use of automated summaries throughout verification, especially for domain-specific DNS operations. In addition, we employ a set of techniques to further scale automation, including symbolic regions, summary optimization, and stub function interposing. We apply Iceberg to four open-source DNS engines, identifying 12 new bugs while keeping manual effort low.

## [Eywa: Automating Model-Based Testing using LLMs](/conference/nsdi26/presentation/mondal)

Rajdeep Mondal, Rathin Singha, Todd Millstein, and George Varghese, *UCLA;* Ryan Beckett and Siva Kesava Reddy Kakarla, *Microsoft Research*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/mondal)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/mondal)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/mondal)

Model-based testing (MBT), whereby a model of the system under test is analyzed to generate high-coverage test cases, has been used to test protocol implementations. A key barrier to the use of MBT is the need for users to understand protocol RFCs in detail to create a compliant model.

Our new approach to MBT uses LLMs to automatically build rich models of intended protocol behavior from knowledge embedded in Request for Comments documents (RFCs), blogs, and other natural language sources. Our approach addresses key challenges with using LLMs, including hallucinations and their inability to monolithically generate complex protocol models. We realize our approach through a novel protocol testing framework EYWA, and demonstrate its effectiveness through extensive case studies of DNS and BGP, and a smaller study of SMTP. Despite minimal user effort, applying EYWA enabled the discovery of 33 unique bugs across widely used DNS, BGP, and SMTP implementations, 16 of which were previously undiscovered despite extensive prior testing with manually crafted models.

## Tuesday, May 5

### 8:00 am–9:00 am

## Continental Breakfast

Grand Pre-Function Area

### 9:00 am–10:20 am

Track 1

## Learning at Line Rate

Session Chair: Kevin Hsieh, *Microsoft*

Grand Ballroom I–VI

## [Making Logic a First-Class Citizen in Generative ML for Networking](/conference/nsdi26/presentation/he)

Hongyu Hè, Minhao Jin, and Maria Apostolaki, *Princeton University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/he)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/he)

Generative ML models are increasingly popular in networking for tasks such as telemetry imputation, prediction, and synthetic trace generation. Despite their capabilities, they suffer from two shortcomings: *(i)* their output is often visibly violating well-known networking rules, which undermines their trustworthiness; and *(ii)* they are difficult to control, frequently requiring retraining even for minor changes.

To address these limitations and unlock the benefits of generative models for networking, we propose a new paradigm for integrating explicit network knowledge, in the form of first-order logic rules, into ML models used for networking tasks. Rules capture well-known relationships among observed signals, e.g., that increased latency precedes packet loss. While the idea is conceptually straightforward, its realization is challenging: networking knowledge is rarely formalized into rules, and naively injecting rules into ML models often hampers their effectiveness. This paper introduces NetNomos, a multi-stage framework that *(i)* learns rules directly from data (e.g., measurements); *(ii)* filters them to select semantically meaningful ones; and *(iii)* enforces them through collaborative generation between an ML model and a Satisfiability Modulo Theories (SMT) solver.

We show that NetNomos learns diverse, meaningful rules from four real-world datasets and is 1.6–6.5× more scalable than DuoAI, a state-of-the-art (SOTA) rule-learning method. By enforcing these rules on a generic GPT-2 model, NetNomos achieves performance on par with or even surpassing specialized SOTA systems such as Zoom2Net and NetShare across three networking tasks: telemetry imputation, traffic forecasting, and synthetic data generation.

## [JITServe: SLO-aware LLM Serving with Imprecise Request Information](/conference/nsdi26/presentation/zhang-wei)

Wei Zhang, Zhiyu Wu, and Yi Mu, *University of Illinois, Urbana-Champaign;* Rui Ning, *unaffiliated;* Banruo Liu, *University of Illinois Urbana-Champaign;* Nikhil Sarda, *Google;* Myungjin Lee, *Cisco Research;* Fan Lai, *University of Illinois Urbana-Champaign*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhang-wei)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhang-wei)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhang-wei)

The integration of Large Language Models (LLMs) into applications ranging from interactive chatbots to multi-agent systems has introduced a wide spectrum of service-level objectives (SLOs) for responsiveness. These include latency-sensitive requests emphasizing per-token latency in streaming chat, deadline-sensitive requests requiring rapid full responses to trigger external tools, and compound requests with evolving dependencies across multiple LLM calls. Despite—or perhaps, because of—this workload diversity and unpredictable request information (e.g., response lengths and dependencies), existing request schedulers have focused on aggregate performance, unable to ensure application-level SLO needs.

This paper presents JITServe, the first SLO-aware LLM serving system designed to maximize *service goodput* (e.g., the number of tokens meeting request SLOs) *across diverse workloads*. JITServe novelly schedules requests using imprecise request information and gradually relaxes this conservatism by refining request information estimates as generation progresses. It applies a *grouped margin goodput maximization* algorithm to allocate just enough serving bandwidth to satisfy each request's SLO *just-in-time* (JIT), maximizing residual capacity for others, while deciding the composition of requests in a batch to maximize efficiency and goodput with provable guarantees. Our evaluation across diverse realistic workloads, including chat, deep research, and agentic pipelines, shows that JITServe improves service goodput by 1.4×–6.3×, alternatively achieving 28.5%–83.2% resource savings, compared to state-of-the-art designs.

## [RollPacker: Taming Long-Tail Rollouts for RL Post-Training with Tail Batching](/conference/nsdi26/presentation/gao-wei)

Wei Gao, Yuheng Zhao, Dakai An, Tianyuan Wu, and Lunxi Cao, *Hong Kong University of Science and Technology;* Shaopan Xiong, Ju Huang, Weixun Wang, Siran Yang, Wenbo Su, Jiamang Wang, Lin Qu, and Bo Zheng, *Alibaba Group;* Wei Wang, *Hong Kong University of Science and Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/gao-wei)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/gao-wei)

Reinforcement Learning (RL) is a pivotal post-training technique for enhancing the reasoning capabilities of Large Language Models (LLMs). However, synchronous RL post‑training frequently suffers from significant GPU underutilization—often referred to as pipeline "bubbles"—caused by imbalanced response lengths within rollout steps. Many RL systems attempt to alleviate this problem by relaxing synchronization, but this can compromise training accuracy.

In this paper, we introduce tail batching, a novel rollout scheduling strategy for synchronous RL. Tail batching systematically consolidates prompts leading to long-tail responses into a few designated "long rounds", ensuring that the majority of rollout steps ("short rounds") contain only balanced, short responses. By strategically reordering execution, this approach dramatically reduces GPU idle time and accelerates RL training without sacrificing on-policy accuracy. We present RollPacker, a system that fully harnesses the benefits of tail batching through holistic optimizations across all three RL stages: elastic parallelism adaptation for rollout, dynamic resource allocation and scheduling for reward, and stream-based training. Cluster deployment on up to 128 H800 GPUs demonstrates that RollPacker achieves an end-to-end training speedup of 2.03× to 2.56× over veRL, and up to 2.24× speedup compared to RLHFuse across the Qwen2.5 family of LLMs. The code is available at [](https://github.com/Farrrrland/RollPacker)<https://github.com/Farrrrland/RollPacker>.

## [FENIX: Enabling In-Network DNN Inference with FPGA-Enhanced Programmable Switches](/conference/nsdi26/presentation/gao)

Xiangyu Gao, *Tsinghua University;* Tong Li, *Renmin University of China;* Yinchao Zhang, *Tsinghua University;* Ziqiang Wang, *Southeast University and Tsinghua University;* Xiangsheng Zeng, *Huazhong University of Science and Technology;* Su Yao, *Tsinghua University and BNRist;* Ke Xu, *Tsinghua University and Zhongguancun Laboratory*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/gao)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/gao)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/gao)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/gao)

Machine learning (ML) is increasingly used in network data planes for advanced traffic analysis, but existing solutions (such as FlowLens, N3IC, BoS) still struggle to simultaneously achieve low latency, high throughput, and high accuracy. To address these challenges, we present FENIX, a hybrid in-network ML system that performs feature extraction on programmable switch ASICs and deep neural network inference on FPGAs. FENIX introduces a Data Engine that leverages a probabilistic token bucket algorithm to control the sending rate of feature streams, effectively addressing the throughput gap between programmable switch ASICs and FPGAs. In addition, FENIX designs a Model Engine to enable high-accuracy deep neural network inference in the network, overcoming the difficulty of deploying complex models on resource-constrained switch chips. We implement FENIX on a programmable switch platform that integrates a Tofino ASIC and a ZU19EG FPGA directly, and evaluate it on real-world network traffic datasets. Our results show that FENIX achieves microsecond-level inference latency and multi-terabit throughput with low hardware overhead, and delivers over 90% accuracy on mainstream network traffic classification tasks, outperforming the state of the art.

Track 2

## Measuring at Scale

Session Chair: Kurtis Heimerl, *University of Washington*

Grand Ballroom VII–IX

## [DDoS Detection at the Scale of One Hundred Tbps](/conference/nsdi26/presentation/xiao)

Yunming Xiao, *The Chinese University of Hong Kong, Shenzhen, and Tencent;* Xijun Luo, Youliang Jiang, Aike Wang, Hu Chen, and Zhibin Zhou, *Tencent;* Heng Yu and Jiahao Cao, *Tsinghua University;* Yong Jiang, *Tsinghua Shenzhen International Graduate School;* Jilong Wang and Mingwei Xu, *Tsinghua University;* Yan Chen, *Northwestern University;* Congcong Miao, *Tencent*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xiao)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/xiao)

Defending against Distributed Denial-of-Service (DDoS) attacks is a critical priority for cloud providers, who must manage ever-growing volumes of both benign and malicious traffic. While state-of-the-art DDoS detection systems leverage programmable devices to process traffic at hundreds of Gbps to Tbps on a single machine, large-scale cloud providers often handle traffic at scales approaching 100 Tbps. This massive volume—two orders of magnitude higher than the traffic handled by existing systems—motivates us to implement distributed processing across multiple servers, where new challenges are present. Specifically, naive load-balancing strategies lead to imbalanced traffic distribution and severe performance bottlenecks, while function offloading to programmable devices must balance flexibility and adaptability. In this paper, we present Canopy, a scalable DDoS detection system designed to overcome these challenges. Canopy features a dynamic load-balancing mechanism that adapts to fluctuating traffic patterns, ensuring balanced distribution across detection servers despite the mix of mice and elephant flows. Additionally, it employs a traffic compression technique at the programmable switch to significantly reduce per-server workload. These innovations enable Canopy to scale to over 100 Tbps in real-world deployments. Successfully deployed in production, Canopy has demonstrated its effectiveness in mitigating large-scale DDoS attacks.

## [SketchPipe: Toward Accurate Sketch-based Network Measurement on Multi-Pipeline Switches with Splitless Sketch Placement](/conference/nsdi26/presentation/chen-xiang)

Xiang Chen, Longlong Zhu, and Linying Zheng, *Zhejiang University;* Hongyang Du, *The University of Hong Kong;* Dong Zhang, *Fuzhou University;* Jianshan Zhang, *Minjiang University;* Xuan Liu, *Yangzhou University;* Qun Huang, *Peking University;* Dusit Niyato, *Nanyang Technological University;* Haifeng Zhou and Chunming Wu, *Zhejiang University;* Hongyan Liu, *Fuzhou University;* Kui Ren, *Zhejiang University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/chen-xiang)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/chen-xiang)

Sketches compactly measure traffic statistics with limited resource usage and are compatible with high-speed multi-pipeline switches. Existing solutions place sketches on multi-pipeline switches via *array-split placement* that splits each sketch array into several identical slices and places each slice on a specific pipeline. However, they incur two issues that drop measurement accuracy: (1) Different slices in different pipelines redundantly measure the same flows, wasting scarce switch resources. (2) Some slices receive much higher traffic loads than other slices. Hence, the data of different slices are highly varied, making their analysis inaccurate. We propose SketchPipe, a framework that offers accurate sketch-based measurement for multi-pipeline switches. The key ideas are two-fold. First, SketchPipe places each sketch array *exclusively* on a pipeline. Second, it caches the flow keys of normal packets while using synthetic state packets to *asynchronously* transfer cached keys to sketch arrays. As such, it avoids splitting arrays to enable accurate measurement while avoiding affecting normal packet processing. Our experiments on 12.8 Tbps Tofino2 switches show that SketchPipe improves accuracy by up to two orders of magnitude for various sketches and network monitoring applications.

## [MORP4: A Dynamic Network Telescope](/conference/nsdi26/presentation/xygkou)

Iliana Xygkou, Jithin K. Sojan, Dhruv Rauthan, and Feng Zhu, *Georgia Institute of Technology;* Thomas Holterbach, *Georgia Institute of Technology and University of Strasbourg;* Shane Alcock, *Alcock Network Intelligence Ltd;* Brian Flanagan, Ahmed Saeed, and Alberto Dainotti, *Georgia Institute of Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xygkou)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/xygkou)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/xygkou)

A *network telescope* passively monitors traffic reaching Internet address space that is not assigned to any hosts but is advertised to the global routing system. This traffic is by definition *unsolicited*. For more than two decades, network telescopes have enabled research breakthroughs by allowing global visibility into a wide range of Internet phenomena. However, telescopes are afflicted by two main issues: progressive erosion, due to the increasing scarcity and commercial value of address space, and blacklisting. To overcome these issues, we propose MORP4, a programmable data-plane framework implementing a “dynamic” network telescope. MORP4 accurately and adaptively tracks unused space of an organization’s network with configurable time and space granularity and captures only traffic directed towards unused addresses at line rate. We provide an implementation in P4 and Python/C++, and deploy it on a Tofino switch. We show that it can detect unused IPv4 address space at the finest granularity (/32) while operating at line rate as well as providing an effective approach for operating a telescope in the IPv6 domain.

## [BayWatch: Practical Internet-Scale Topology Monitoring with Dynamic Bayesian Estimation](/conference/nsdi26/presentation/guan-zhongxu)

Zhongxu Guan, *Tsinghua University and Tsinghua Shenzhen International Graduate School;* Shuai Wang, Li Chen, and Zhaoteng Yan, *Zhongguancun Laboratory;* Jiaye Lin and Dan Li, *Tsinghua University;* Yong Jiang, *Tsinghua Shenzhen International Graduate School;* Yingxin Wang and Ziqian Liu, *China Telecom Cybersecurity Technology Co.,Ltd.*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/guan-zhongxu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/guan-zhongxu)

Internet topology monitoring is important for understanding topology dynamics. While a few commercial services have been provided to monitor the specified topology, academic research on Internet-scale topology monitoring still lags behind with two key limitations: 1) topology incompleteness caused by simplified assumption of uniform load-balancing responses (LBR) distribution; 2) low probing efficiency due to the lack of temporal awareness.

In this paper, we introduce BayWatch, a practical Internet-scale topology monitoring system that overcomes these limitations based on a Dynamic Bayesian Network (DBN). Leveraging the Markov property of packet forwarding, BayWatch models it as a sequence of state transitions over time within the DBN, so as to estimate the true LBR distribution and predict its temporal evolution. Internet-wide measurement results demonstrate that benefiting from the estimated LBR distribution, BayWatch can discover 2.4×/2.8× more nodes/links than the state-of-the-art algorithm, D-Miner, while the temporal awareness reduces the number of probes by 6.3× with negligible topology completeness loss. Moreover, we demonstrate that BayWatch can help detect anomalies using a real-world network outage event.

Track 3

## From Silicon to Networked Systems

Session Chair: Kai Chen, *The Hong Kong University of Science and Technology*

Bellevue Room

## [SyncWise: Error-Aware Time Synchronization for Reconfigurable Data Center Networks](/conference/nsdi26/presentation/lei-syncwise)

Yiming Lei, *Max Planck Institute for Informatics;* Jialong Li, *Shenzhen University of Advanced Technology;* Zhengqing Liu, *Imperial College London;* Raj Joshi, *Harvard University;* Yiting Xia, *Max Planck Institute for Informatics*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lei-syncwise)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/lei-syncwise)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/lei-syncwise)

Time synchronization is critical for emerging reconfigurable data center networks (RDCNs) built on optical circuit switches (OCSes), where accurate identification of dynamic optical circuits is required for reliable data transmission. As circuit durations shrink to the microsecond and sub-microsecond range, sync accuracy demands become increasingly stringent. Yet, this problem has been largely overlooked, both practically and theoretically, with no general, easily integrable solutions or established accuracy limits. We present SyncWise, the first sync protocol customized for RDCNs that closes these gaps. SyncWise formalizes the synchronization problem for RDCNs, models errors through an RDCN-specific analysis of error sources, and leverages this error model to guide the “wise” selection of optimal sync parents. SyncWise achieves provably optimal performance and is prototyped on a testbed with an OCS and Intel Tofino2 switches. Large-scale simulations demonstrate that SyncWise is the first protocol to attain sub-10 ns maximum sync error, ensuring reliable RDCN fabrics and outperforming the most accurate protocols in traditional DCNs by a large margin.

## [Building A CSFQ-Inspired Transport for Switched CXL Memory Pooling](/conference/nsdi26/presentation/guo-zerui)

Zerui Guo, *University of Wisconsin-Madison;* Emily Shriver, *Intel;* Ming Liu, *University of Wisconsin-Madison*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/guo-zerui)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/guo-zerui)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/guo-zerui)

Emerging switched CXL memory pooling systems, albeit promising, suffer from significant performance interference due to the shared but performance-uncontrolled data path among concurrent memory streams between a host core and a remote DIMM. We systematically characterize a memory pooling appliance based on the XConn’s Apollo CXL switch, and identify three issues: intra-host contention, in-fabric congestion, and unmanaged host-remote DIMM interaction.

This paper presents a new transport layer, **MemChannel**, which provides the `mchannel` abstraction to manage end-to-end fabric bandwidth among competing memory flows and enable application-specific traffic for switched CXL memory pooling. Under the hood, our key idea is to build a *Sender-Driven Fabric-Informed* transport protocol—inspired by Core-Stateless Fair Queueing (CSFQ)—that admits just the right amount of CXL requests to each `mchannel` based on the estimated Core ↔ DIMM_(CXL) bandwidth availability. To grapple with the ramifications of CXL-induced idiosyncrasies, MemChannel introduces a couple of techniques: time-based rate control, host-side admission control, cross-host bookkeeping, new congestion signals, rate estimation based on the fluid model, and delay-based link capacity adjustment. We build MemChannel from scratch and support unmodified applications. Our evaluations over switched memory pooling demonstrate the effectiveness of MemChannel from performance isolation, scalability, and multi-tenancy perspectives.

## [OpenOptics: Enabling Open Research and Implementation of Optical Data Center Networks](/conference/nsdi26/presentation/lei-optical)

Yiming Lei and Federico De Marchi, *Max Planck Institute for Informatics;* Jialong Li, *Shenzhen University of Advanced Technology;* Raj Joshi, *Harvard University;* Shu-Ting Wang, *UC San Diego;* Xiaoqi Chen, *Purdue University;* Balakrishnan Chandrasekaran, *Vrije Universiteit Amsterdam;* Yiting Xia, *Max Planck Institute for Informatics*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lei-optical)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/lei-optical)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/lei-optical)

Optical data center networks (DCNs) are emerging as a promising design for cloud infrastructure. However, existing optical DCN architectures operate as closed ecosystems, tying software solutions to specific optical hardware. We introduce OpenOptics, an open research and development framework that decouples software from hardware, allowing them to evolve independently. OpenOptics features: (1) a time-flow table abstraction as a common interface between optical hardware and software, (2) a unified workflow and user-friendly API for implementing various optical DCNs with simple Python scripts, and (3) a backend system that re-architects queue management to support the time-flow tables and provides rich infrastructure services for diverse applications. Built on programmable switches, OpenOptics achieves a record-breaking minimum optical circuit duration of 2 µs using commodity devices. We validate OpenOptics’ generality by implementing six optical architectures and seven routing schemes on an optical testbed and conducting benchmarks on a 108-ToR setup, showcasing its efficiency. Additionally, case studies highlight novel research opportunities enabled by OpenOptics.

## [PlanB: Efficient Software IPv6 Lookup with Linearized B+-Tree](/conference/nsdi26/presentation/zhang-zhihao)

Zhihao Zhang, *Alibaba Cloud, NICE Lab, XMU, and Tsinghua University;* Lanzheng Liu, Chen Chen, and Huiba Li, *Alibaba Cloud;* Jiwu Shu, *Tsinghua University;* Windsor Hsu, *Alibaba Cloud;* Yiming Zhang, *NICE Lab, SJTU, and NICE Lab, XMU*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhang-zhihao)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhang-zhihao)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhang-zhihao)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhang-zhihao)

IP lookup via Longest Prefix Match (LPM) is critical for packet forwarding. Unfortunately, conventional lookup algorithms are inefficient for IPv6 Forwarding Information Bases (FIBs), which are characterized by a set of long prefixes with diverse lengths. We observe that LPM inherently represents a two-dimensional (2D) search problem over both prefix values and prefix lengths, but existing algorithms mostly treat LPM as two separate levels of one-dimensional (1D) searches, causing poor lookup performance and high memory overhead.

This paper presents PlanB, a novel scheme for high-speed IPv6 lookup. We transform the 2D LPM into an equivalent 1D search problem over elementary intervals, unifying the search across prefix value and lengths. We then adapt the flat-array B-tree structure to the needs of LPM to propose *linearized B+-tree*, based on which we introduce an efficient search algorithm tailored to the properties of the transformed space. To maximize performance, we integrate PlanB with vectorization, batching, branch-free logic, and loop unrolling to fully exploit CPU parallelism. Extensive evaluation shows that PlanB achieves single-core performance of 390 Million Lookups Per Sec (MLPS) with real-world IPv6 FIBs on AMD processor, and scales to full-12-core performance of 3.4 Billion Lookups Per Sec (BLPS). This is 1.6×∼14× higher than state-of-the-art software-based schemes (PopTrie, CP-Trie, Neurotrie and HBS).

### 10:20 am–10:50 am

## Coffee and Tea Break

Grand Pre-Function Area

### 10:50 am–12:30 pm

Track 1

## Smart Pipes, Smarter Learning

Session Chair: Xiaoqi Chen, *Purdue University*

Grand Ballroom I–VI

## [FLARE: Anomaly Diagnostics for Divergent LLM Training in GPU Clusters of Thousand-Plus Scale](/conference/nsdi26/presentation/cui)

Weihao Cui, *Shanghai Jiao Tong University and National University of Singapore;* Ji Zhang, *Independent Researcher;* Han Zhao, *Shanghai Jiao Tong University;* Chao Liu, *Independent Researcher;* Jian Sha, *Tsinghua University;* Bo Sang, *Ant Group;* Bingsheng He, *National University of Singapore;* Minyi Guo and Quan Chen, *Shanghai Jiao Tong University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/cui)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/cui)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/cui)

The rapid proliferation of large language models has driven the need for efficient GPU training clusters. However, it is challenging due to the frequent occurrence of training anomalies. Since existing diagnostic tools are narrowly tailored to specific issues, there are gaps in their ability to address anomalies spanning the entire training stack. In response, we introduce FLARE, a diagnostic framework designed for distributed LLM training at scale. FLARE first integrates a lightweight tracing daemon for full-stack and backend-extensible tracing. Additionally, it features a diagnostic engine that automatically diagnoses anomalies, with a focus on performance regressions. The deployment of FLARE across 6,000 GPUs has demonstrated significant improvements in pinpointing deficiencies in real-world scenarios, with continuous operation for over eight months.

## [TurboTest: Learning When Less is Enough through Early Termination of Internet Speed Tests](/conference/nsdi26/presentation/manda)

Haarika Manda, *UC Santa Barbara;* Manshi Sagar, Yogesh, and Kartikay Singh, *IIT Delhi;* Cindy Zhao, *UC Santa Barbara;* Tarun Mangla, *IIT Delhi;* Phillipa Gill, *Google;* Elizabeth Belding and Arpit Gupta, *UC Santa Barbara*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/manda)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/manda)

Internet speed tests are indispensable for users, ISPs, and policymakers, but their static flooding-based design imposes growing costs: a single high-speed test can transfer hundreds of MB, and collectively, platforms like Ookla, M-Lab, and Fast.com generate petabytes of traffic each month. Reducing this burden requires deciding when a test can be stopped early without sacrificing accuracy. We frame this as an optimal stopping problem and show that existing heuristics—static thresholds, BBR pipe-full signals, or throughput stability rules from Fast.com and FastBTS—capture only a narrow slice of the achievable accuracy—savings trade-off. This paper introduces TURBOTEST, a systematic framework for speed test termination that sits atop existing platforms. The key idea is to decouple throughput prediction (Stage~1) from test termination (Stage~2): Stage~1 trains a regressor to estimate final throughput from partial measurements, while Stage~2 trains a classifier to decide when sufficient evidence has accumulated to stop. Leveraging richer transport-level features (RTT, retransmissions, congestion window) alongside throughput, TURBOTEST exposes a single tunable parameter ε for accuracy tolerance and includes a fallback mechanism for high-variability cases. Evaluation on 1 million M-Lab NDT speed tests (2024–2025) shows that TURBOTEST achieves 1.8-4.4× higher data savings than an approach based on BBR signals while reducing median error. These results demonstrate that adaptive ML-based termination can deliver accurate, efficient, and deployable speed tests at scale.

## [Defeating Slow-and-Low Threats via Diffusion Model-based Generative Inference](/conference/nsdi26/presentation/mirnajafizadeh)

Seyed Mohammad Mehdi Mirnajafizadeh and Prashant Khanduri, *Wayne State University;* DaeHun Nyang, *Ewha Womans University;* Rhongho Jang, *Wayne State University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/mirnajafizadeh)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/mirnajafizadeh)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/mirnajafizadeh)

Content Delivery Networks (CDNs) are known to be vulnerable to slow-and-low threats that exploit trusted protocols while evading threshold-based defense at the edge. Our work addresses three limitations at edge defense: constrained resources, absence of a behavior monitor, and impractical assumptions for online detection. To defeat slow-and-low threats, we propose *SketchVision*, a vision-inspired detection framework that redefines flow behavior monitoring and attack detection under resource-constrained settings. We introduce a vision-inspired sketch that encodes packet-level temporal patterns of all flows into a compact image, a diffusion model tailored for sketch denoising, and a generative inference pipeline to forecast mature flow states from partial observations for early detection. Implemented with eBPF-enabled data planes and diffusion-based control, *SketchVision* achieves robust accuracy across 19 types of slow-and-low attacks, reaching an average AUC of 0.982 and F1 score of 0.913, improving detection by up to 29% over the state-of-the-art methods, while remaining efficient for large-scale CDN edge deployment.

## [SwiftEP: Accelerating MoE Inference with Buffer Fusion and TMA Offloading](/conference/nsdi26/presentation/li-xingyi)

Xingyi Li, *unaffiliated;* Yadong Liu and Xiaojie Huang, *Tencent;* Yiran Zhang, Shuai Wang, and Shangguang Wang, *unaffiliated;* Zhehao Lin and Yinben Xia, *Tencent;* Chang Yu, *Nanjing University;* Qihang Liu, Xuan Zhang, Hao Lu, Xiang Li, Zekun He, Yachen Wang, and Xianneng Zou, *Tencent*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/li-xingyi)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/li-xingyi)

Large Language Models (LLMs) increasingly rely on Mixture-of-Experts (MoE) architectures to scale computation efficiently. Expert Parallelism (EP), which distributes experts across GPUs, introduces all-to-all communication overhead during the *dispatch* and *combine* phases, especially in the prefill stage, which dominates the inference performance. Existing communication libraries, such as DeepEP, suffer from *excessive* GPU SM utilization and underutilized interconnect bandwidth, limiting prefill performance.

In this paper, we identify two root causes: redundant buffer copies and inefficient intra-server transfers over NVLink. To address these, we propose SwiftEP, an all-to-all communication library tailored for MoE prefill, combining *buffer fusion* and *Tensor Memory Accelerator (TMA) offloading*. Buffer fusion eliminates redundant staging copies, enabling true zero-copy communication, while TMA offloading maximizes NVLink utilization and supports efficient multicast/reduce operations. SwiftEP further incorporates RDMA scatter-gather lists, QP transmission parallelization, and CUDA IPC to handle dynamic token placement and inter-GPU memory access. Evaluation on 16- and 32-GPU clusters shows that SwiftEP achieves up to 119.7% higher algorithm bandwidth, reduces SM occupancy by up to 66.7%, and improves request serving capacity by 21.2% compared to DeepEP.

## [Geminet: Learning the Duality-based Topology-Agnostic Update Operator for Lightweight Traffic Engineering in Changing Topologies](/conference/nsdi26/presentation/liu-ximeng)

Ximeng Liu, *Shanghai Jiao Tong University and Zhongguancun Academy;* Zhuoran Liu, *Shanghai Jiao Tong University;* Yingming Mao, *Xi'an Jiaotong University and Shanghai Innovation Institute;* Yatao Li, *Zhongguancun Academy and Zhongguancun Institute of Artificial Intelligence;* Shizhen Zhao and Xinbing Wang, *Shanghai Jiao Tong University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/liu-ximeng)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/liu-ximeng)

Recently, researchers have explored ML-based Traffic Engineering (TE), leveraging neural networks to solve TE problems traditionally addressed by optimization. However, existing ML-based TE schemes remain impractical: they either fail to handle topology changes or suffer from poor scalability due to excessive computational and memory overhead. To overcome these limitations, we propose Geminet, a lightweight and scalable ML-based TE framework that can handle changing topologies. Geminet is built upon two key insights: (i) decoupling neural networks from topology by learning a topology-agnostic update operator inspired by classical iterative optimization methods (e.g., gradient descent), which depend only on a few gradient-related quantities; (ii) shifting optimization from path-level routing weights to edge-level dual variables, reducing memory consumption by leveraging the fact that edges are far fewer than paths. Evaluations on WAN and data center datasets show that Geminet significantly improves scalability. Its neural network size is only 0.04%-7% of existing schemes, while handling topology variations as effectively as HARP, a state-of-the-art ML-based TE approach, without performance degradation. When trained on large-scale topologies, Geminet consumes less than 10 GiB of memory compared to more than 80 GiB required by HARP, while achieving 18× faster convergence, demonstrating its potential for large-scale deployment.

Track 2

## Debugging Distributed Systems

Session Chair: Chang Lou, *University of Virginia*

Grand Ballroom VII–IX

## [EROICA: Online Performance Troubleshooting for Large-scale Model Training](/conference/nsdi26/presentation/guan-yu)

Yu Guan, Zhiyu Yin, Haoyu Chen, Sheng Cheng, Chaojie Yang, and Kun Qian, *Alibaba Group;* Tianyin Xu, *University of Illinois Urbana-Champaign;* Pengcheng Zhang, Yang Zhang, Hanyu Zhao, Yong Li, Dennis Cai, and Ennan Zhai, *Alibaba Group*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/guan-yu)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/guan-yu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/guan-yu)

Troubleshooting performance problems of large model training (LMT) is immensely challenging, due to unprecedented scales of modern GPU clusters, the complexity of software-hardware interactions, and the data intensity of the training process. Existing troubleshooting approaches designed for traditional distributed systems or datacenter networks fall short and can hardly apply to real-world training systems. In this paper, we present EROICA, the first online troubleshooting system that provides both fine-grained observation based on profiling, and coverage of all machines in GPU clusters, to diagnose performance issues in production, including both hardware and software problems (or the mixture of both). EROICA effectively summarizes runtime behavior patterns of LMT function executions via online profiling, and leverages differential observability to localize the root cause with minimal production impact. EROICA has been deployed as a production service for large-scale GPU clusters of ~100,000 GPUs for 1.5 years. It has diagnosed a variety of difficult performance issues with 97.5% success.

## [Supercharging Packet-level Network Simulation of Large Model Training via Memoization and Fast-Forwarding](/conference/nsdi26/presentation/long)

Fei Long, *Tsinghua University;* Kaihui Gao and Li Chen, *Zhongguancun Laboratory;* Dan Li and Yiwei Zhang, *Tsinghua University;* Fei Gui, *Zhongguancun Laboratory;* Yitao Xing, Wenjia Wei, and Bingyang Liu, *Huawei*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/long)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/long)

Packet-level discrete-event simulation (PLDES) is a prevalent tool for evaluating detailed performance of large model training. Although PLDES offers high fidelity and generality, its slow performance has plagued networking practitioners. Existing optimization techniques either simplify the network model, resulting in large errors; or execute it in parallel using multiple processors, with an upper bound on speedup.

This paper explores an alternative optimization direction that reduces the computational loads of PLDES while maintaining high fidelity. Our key insight is that, in distributed LLM training, packet-level traffic behaviors often exhibit *repetitive contention patterns* and *steady-states* where flow rates stabilize, ignoring these redundant discrete events speeds up the simulation considerably and the error is negligible. We realize this idea by proposing Wormhole, a user-transparent PLDES kernel capable of automatically memoization for unsteady-states and skipping for steady-states. Wormhole adopts network partitioning, state memoization and reuse, and rate-based steady-state identification to accurately determine the periods of each flow’s steady-state, while maintaining simulation consistency after fast-forwarding. Experiments demonstrate that Wormhole can achieve a 744× speedup over the original ns-3 (510× for MoE workload), with a bounded error of \<1%. Applying current multithreading parallel techniques and Wormhole together allows a 1012× speedup, reducing the simulation time for one GPT-13B training under 128 GPUs from 9 hours to 5 minutes.

## [Iris: Expressive Traffic Analysis for the Modern Internet](/conference/nsdi26/presentation/rossman)

Thea Rossman, Diana Qing, Gerry Wan, and Zakir Durumeric, *Stanford University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/rossman)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/rossman)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/rossman)

In this work, we investigate the needs of modern traffic analysis, and we introduce Iris, a framework for efficiently building complex, high-performance traffic analysis applications. Iris's key contribution is a compiler that transforms user-defined traffic filters, stream transformations, and computation written in Rust into an optimized processing pipeline. The Iris compiler eliminates redundant logic across analysis tasks to generate a unified runtime that minimizes aggregate work, allowing it to scale to hundreds of concurrent workloads. Rather than restricting users to a domain-specific query language, Iris provides a flexible development environment by exposing connection- and application-layer semantics as Rust data types to user-defined functions. We show that Iris can execute hundreds of analysis tasks concurrently at 100Gbps+ on a single commodity server, and we demonstrate its flexibility through three use cases drawn from prior work.

## [Who Watches the Watchers? On the Reliability of Softwarizing Cloud Application Management](/conference/nsdi26/presentation/gu)

Jiawei Tyler Gu, Zhen Tang, Yiming Su, Bogdan Alexandru Stoica, Xudong Sun, and William X. Zheng, *University of Illinois Urbana-Champaign;* Yue Zhang and Akond Rahman, *Auburn University;* Chen Wang, *IBM Research;* Tianyin Xu, *University of Illinois Urbana-Champaign*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/gu)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/gu)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/gu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/gu)

Modern cloud applications are increasingly managed by software programs, often named “operators,” which automate laborious, human-based operations. While operator programs largely prevent human mistakes, their own reliability has unprecedented impact on managed applications. This paper discusses the emerging challenges of operator program reliability on cloud-native platforms like Kubernetes. Our work is grounded in a rigorous analysis of 412 real-world failures of thirteen Kubernetes operators. We find that challenges of operator reliability come from the multifold complexity of an operator’s interactions with its managed applications, environment, and user interface. Among these, operators’ interactions with managed applications are the largest contributor to real-world operator failures, but they are largely overlooked—these interactions are often ad hoc and lack well-defined interfaces. We advocate to rethink the management interface of cloud applications and demonstrate this urgent need by showing the prevalence of defects in existing operators. Specifically, we develop a simple testing tool to exercise interactions between operators and the managed cloud applications, which discovered 86 new bugs in six popular Kubernetes operators.

## [From Source to Solution: Tackling Packet Losses in Large-scale Cloud Gaming Systematically and Precisely](/conference/nsdi26/presentation/wang-jing)

Jing Wang, Xiao Kong, Yunzhe Ni, Nian Wen, Jiaxing Zhang, Congcong Miao, and Honghao Liu, *Tencent Inc.*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-jing)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-jing)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/wang-jing)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wang-jing)

Cloud gaming requires all video frames to be delivered before a stringent delay deadline to ensure seamless gaming experience. However, meeting this requirement is challenging due to packet losses, which greatly magnifies the frame delay. Various FEC-based loss recovery schemes were recently proposed to address the packet loss issue. However, the source of such packet losses remains unrevealed. Our production measurement results from Tencent START cloud gaming platform have shown that 66.5% of packet losses are caused by network infrastructure’s preferences against UDP and network congestion. Moreover, off-the-shelf video streaming systems like WebRTC could not detect retransmission loss efficiently. These issues completely nullified the performance gain of loss recovery schemes. To address this, we design and implement LADR, which combines loss avoidance, detection, and recovery to tackle packet losses. LADR incorporates the loss-based and delay-based congestion control algorithms and adopts RACK-TLP for loss avoidance and detection. Furthermore, LADR adopts an opportunistic FEC scheme to perform loss recovery. LADR has been rolled out at Tencent START cloud gaming platform, a large-scale cloud gaming provider, for one year. Production measurement results show that LADR only suffers from 0.049% packet loss rate (-59.8% vs. existing solutions) and delivers 99.87% of video frames within 100 milliseconds.

Track 3

## Scalable Storage Systems

Session Chair: Zili Meng, *The Hong Kong University of Science and Technology*

Bellevue Room

## [PD3: Prefetching Data with DPUs for Disaggregated Memory](/conference/nsdi26/presentation/sankhe)

Sidharth Sankhe, Felix Zhang, and Umayrah Chonee, *University of Toronto;* Sherman Lim, *National University of Singapore;* Jiasheng Hu, *University of Toronto;* Jialin Li, *National University of Singapore;* Qizhen Zhang, *University of Toronto*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/sankhe)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/sankhe)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/sankhe)

We introduce PD3, a memory disaggregation solution that "avoids" cache misses, via prefetching, on compute servers and thus all their associated overhead. Unlike a traditional prefetcher that may pollute the cache or miss preloading opportunities due to false positives and false negatives, PD3 prevents mis-predictions with network support and minimal yet critical application information. Enabling PD3 is data processing units or DPUs, which allow (1) parsing user requests before they are processed by the compute server, (2) fetching data from remote memory on the shortest path, (3) offloading expensive RDMA and DMA operations from the host, and (4) incorporating application knowledge to faithfully predict cache misses and take actions accordingly. Designing PD3 requires reconciling DPU resource constraints and scaling requirements of cloud data systems, as well as achieving high efficiency with a myriad of performance optimizations. Our experimental results on real hardware, applications, and workloads show that with nominal compute-local memory, PD3 eliminates the performance gap between memory-disaggregated applications and their monolithic counterparts.

## [UpFuzz: Detecting Data Format Incompatibility Bugs during Distributed Storage System Upgrade](/conference/nsdi26/presentation/han)

Ke Han and Sruthi P C, *Purdue University;* Yayu Wang, *The University of British Columbia;* Yaoxu Song and Bishal Basak Papan, *Purdue University;* Junwen Yang, *Meta;* Pedro Fonseca and Yongle Zhang, *Purdue University*

***Community Award Winner!***

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/han)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/han)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/han)

Data format incompatibility is a significant cause of cloud incidents during distributed system upgrades, often resulting in severe consequences such as data corruption and service unavailability. A majority of such bugs are only discovered post-release, largely due to the lack of automated testing techniques tailored specifically for the upgrade process. Traditional automated test generation methods face a unique challenge when applied to upgrade testing: the high cost associated with upgrading distributed storage systems due to system initialization. Therefore, the accurate selection of potential failure-inducing tests from the extensive pool of automatically generated tests becomes critical.

In this work, we address this problem by proposing a novel approach to prioritize upgrade tests through analyzing data format properties over *transitively persisted states*: program states that are persisted to disk, directly or indirectly, through chains of memory copies by the old version, and eventually read by the new version after upgrade. Because data format incompatibility bugs happen due to translation errors of such states across versions, *transitively persisted states* satisfying unique *data format properties* related to *changed data formats* are particularly essential for testing.

We build a likely invariant analysis engine that captures such properties as feedback for seed test selection in UPFUZZ, the automated testing engine for the distributed storage system upgrade procedure. UPFUZZ has detected 15 previously unknown upgrade failures caused by data format incompatibilities in the latest stable versions of Cassandra, HBase, and HDFS; developers have confirmed 8 of them. 7 are triggered exclusively with UPFUZZ’s data format analysis. The detected bugs have severe consequences, with 6 crashing the cluster and 4 causing data loss or corruption.

## [Libra: Flexible Request Partitioning and Scheduling for Serving Unbalanced and Dynamic LLM Workloads](/conference/nsdi26/presentation/ruan-libra)

Chaoyi Ruan, *National University of Singapore;* Yinhe Chen, Dongqi Tian, and Yandong Shi, *University of Science and Technology of China;* Yongji Wu, *UC Berkeley;* Jialin Li, *National University of Singapore;* Cheng Li, *University of Science and Technology of China and Institute of Artificial Intelligence, Hefei Comprehensive National Science Center*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/ruan-libra)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/ruan-libra)

LLM inference must meet strict latency SLOs while maximizing throughput. Yet, real-world variability in prompt and response lengths skews compute-intensive prefill and memory-bound decode phases, making both colocated (even with chunked prefill) and disaggregated deployments unable to simultaneously deliver low tail latency and high throughput.

We introduce Libra, a high performance LLM serving system that maximizes goodput under SLO constraints even when handling imbalanced and dynamic workloads. At the core of Libra is a *micro-request* based *flexible partitioning and scheduling* (FPS) abstraction. The abstraction splits each request at any token boundary into multiple cooperating segments. Libra then designs a *two-level scheduling* framework that balances micro-request load across unified GPU instances. The framework consists of a global scheduler that selects per-request split points, and a local scheduler on each GPU instance to form SLO-aware batches. Finally, Libra uses chunked KV cache transfers to support cross-instance micro-request execution. On real-world traces, Libra improves goodput by up to 1.91× and 1.61×, increases serving capacity from 1.15× to 3.07×, and improves serving performance by up to 74.2% in a hybrid workload under strict SLOs and A100/H100 GPUs compared to state-of-the-art colocated and disaggregated baselines.

## [Come Hell or Still Water: Alleviating Tail Latency in Cloud Block Store](/conference/nsdi26/presentation/hu-chaolei)

Chaolei Hu, *Tsinghua University and Alibaba Cloud;* Kun Qian, Erci Xu, Yifan Shen, Haoran Zhang, Xue Li, Yuesheng Gu, and Lingjun Zhu, *Alibaba Cloud;* Fengyuan Ren, *Tsinghua University;* Ennan Zhai, *Alibaba Cloud*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/hu-chaolei)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/hu-chaolei)

Maintaining low tail latency is crucial for cloud storage services. In ALIBABA CLOUD, our Elastic Block Storage (EBS), like many others, adopts layers of load balancing to avoid hot-spot I/Os, a dominant contributor to tail latency.

However, in the field, EBS has still been suffering from tail latency spikes. Through extensive analysis of production workloads, we have identified the root cause: the workload bursts caused by a small group of Virtual Disks (VDs), which fundamentally influence the tail latency of the entire cluster. We hence propose a lightweight dual-bucket throttling mechanism to effectively mitigate the issue while maintaining fairness. In addition, we discover that, even under underloaded scenarios, the tail latency remains suboptimal due to the event-loop thread model. We propose a priority-based scheduling mechanism to separate I/O-related tasks from I/O-unrelated ones. Our evaluation shows that the proposed mechanisms can reduce the tail latency by up to 97% in burst and 43% in underloaded scenarios. Our mechanisms have been deployed across dozens of clusters for more than three months, and have served hundreds of trillions of I/O requests. They reduce the P99999 tail latency of steady segments by 59.7% under burst scenarios and of all I/Os by 22% in underloaded scenarios.

## [Wallet: Confidential Serverless Computing](/conference/nsdi26/presentation/sabanic)

Patrick Sabanic, Masanori Misono, Teofil Bodea, Julian Pritzi, Michael Hackl, Dimitrios Stavrakakis, and Pramod Bhatotia, *Technical University of Munich*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/sabanic)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/sabanic)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/sabanic)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/sabanic)

Although serverless computing offers compelling cost and deployment simplicity advantages, a significant challenge remains in securely managing sensitive data as it flows through *the network of ephemeral function executions* in serverless computing environments within untrusted clouds. While Confidential Virtual Machines (CVMs) offer a promising secure execution environment, their integration with serverless architectures currently faces fundamental limitations in key areas: *security*, *performance*, and *resource efficiency*.

We present WALLET, a lightweight confidential computing system for secure serverless deployments. By employing nested confidential execution and a decoupled guest OS within CVMs, WALLET runs each function in a minimal "trustlet", significantly improving security through a reduced Trusted Computing Base (TCB). Furthermore, by leveraging a data-centric I/O architecture built upon a lightweight LibOS, WALLET optimizes network communication to address performance and resource efficiency challenges.

Our evaluation shows that compared to CVM-based deployments, WALLET has a 4.3× smaller TCB, improves end-to-end latency (15–93%), achieves higher function density (up to 907×), and reduces inter-function communication (up to 27×) and function chaining latency (16.7-30.2×); thus, WALLET offers a practical system design for confidential serverless computing.

### 12:30 pm–2:00 pm

## Lunch (on your own)

### 2:00 pm–3:20 pm

Track 1

## Living Large in Shared Clouds

Session Chair: Venkat Arun, *The University of Texas at Austin*

Grand Ballroom I–VI

## [Octopus: Enhancing CXL Memory Pods via Sparse Topology](/conference/nsdi26/presentation/zhong)

Yuhong Zhong, *Columbia University;* Fiodar Kazhamiaka, Pantea Zardoshti, Shuwei Teng, and Rodrigo Fonseca, *Microsoft Azure;* Mark D. Hill, *University of Wisconsin–Madison;* Daniel S. Berger, *Microsoft Azure and University of Washington*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhong)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhong)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhong)

The Compute Express Link (CXL) interconnect enables compute "pods" that pool memory across servers to reduce cost and improve efficiency. These pods also facilitate pairwise communication whose needs conflict with pooling. Importantly, existing pod designs are small or require indirection through expensive switches. These conventional designs implicitly assume that pods must fully connect all servers to all CXL pooling devices.

This paper breaks with this conventional wisdom by introducing *Octopus* pods. Octopus directly connects servers to low-port-count CXL pooling devices (e.g., 4 ports) yet scales to large pods without switches by constructing a sparse CXL topology in which each pooling device connects to a carefully chosen subset of servers. Octopus explicitly balances "overlap", where two servers connect to the same pooling device: overlap reduces pooling efficiency but enables low-latency communication. Octopus resolves this tension by grouping servers into "islands" with low-latency intra-island communication and interconnecting islands to favor pooling.

We build a three-server CXL pod prototype and simulate scaled pods with 96 servers under measured device characteristics and physical constraints (1.5m copper cables). On hardware, Octopus RPCs are 3.2× faster than in-rack RDMA and 2.4× faster than CXL switches. In simulation, Octopus achieves net server cost savings of 3–5.4% whereas CXL switches result in a net cost increase.

## [RLBoost: Harvesting Preemptible Cloud Resources for Cost-Efficient Reinforcement Learning on LLMs](/conference/nsdi26/presentation/wu-yongji)

Yongji Wu, *UC Berkeley;* Xueshen Liu, *University of Michigan;* Haizhong Zheng, *Carnegie Mellon University;* Juncheng Gu, *Google;* Beidi Chen, *Carnegie Mellon University;* Z. Morley Mao, *University of Michigan;* Arvind Krishnamurthy, *Google and University of Washington;* Ion Stoica, *UC Berkeley*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wu-yongji)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/wu-yongji)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wu-yongji)

Reinforcement learning (RL) has become essential for unlocking advanced reasoning capabilities in large language models (LLMs). RL workflows involve interleaving rollout and training stages with fundamentally different resource requirements. Rollout typically dominates overall execution time, yet scales efficiently through multiple independent instances. In contrast, training requires tightly-coupled GPUs with full-mesh communication. Existing RL frameworks fall into two categories: co-located and disaggregated architectures. Co-located frameworks fail to address this resource tension by forcing both stages to share the same GPUs. Disaggregated architectures, without modifications of well-established RL algorithms, suffer from resource under-utilization. Meanwhile, preemptible GPU resources, i.e., spot instances on public clouds and spare capacity in production clusters, present significant cost-saving opportunities for accelerating RL workflows, if efficiently harvested for rollout.

In this paper, we present RLBoost, a framework for cost-efficient RL training that harvests preemptible GPU resources. Our key insight is that rollout's stateless and embarrassingly parallel nature aligns perfectly with preemptible and often fragmented resources. To efficiently utilize these resources despite frequent and unpredictable availability changes, RLBoost adopts a hybrid architecture with three key techniques: (1) adaptive rollout offload to dynamically adjust workloads on the reserved (on-demand) cluster, (2) pull-based weight transfer that quickly provisions newly available instances, and (3) token-level response collection and migration for efficient preemption handling and continuous load balancing. Extensive experiments show RLBoost increases training throughput by 1.51x-1.97x while improving cost efficiency by 28%-49% compared to using only on-demand GPU resources. RLBoost is open-sourced at <https://github.com/Terra-Flux/PolyRL>.

## [KUBEDIRECT: Unleashing the Full Power of the Cluster Manager for Serverless Computing](/conference/nsdi26/presentation/qi)

Sheng Qi, Zhiquan Zhang, Xuanzhe Liu, and Xin Jin, *Peking University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/qi)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/qi)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/qi)

FaaS platforms rely on cluster managers like Kubernetes for resource management. Kubernetes is popular due to its extensible state-centric APIs and modular architecture. However, to scale out a burst of FaaS instances, message passing becomes the primary bottleneck as controllers have to exchange extensive state through the API Server. Existing solutions opt for a clean-slate redesign of cluster managers, at the expense of ecosystem compatibility and substantial engineering effort.

We present KUBEDIRECT, a Kubernetes-based cluster manager for FaaS. We find that there exists a common *narrow waist* across FaaS platforms that allows us to achieve both efficiency and external compatibility. The narrow waist has a sequential structure that obviates the need for a single source of truth, allowing us to bypass the API Server and perform lightweight direct message passing. However, our approach introduces distributed and ephemeral state across controllers, making it challenging to enforce end-to-end semantics without centralized coordination. KUBEDIRECT performs novel state management that leverages the narrow waist as a *hierarchical write-back cache*, ensuring consistency and convergence to the desired state. KUBEDIRECT can seamlessly integrate with Kubernetes, adding ~150 LoC per controller. KUBEDIRECT can reduce serving latency by 26.7× over Knative, and has similar performance as the state-of-the-art clean-slate platform Dirigent.

## [FlexLLM: Token-Level Co-Serving of LLM Inference and Finetuning with SLO Guarantees](/conference/nsdi26/presentation/oliaro)

Gabriele Oliaro, *Carnegie Mellon University;* Xupeng Miao, *Purdue University;* Xinhao Cheng, *Carnegie Mellon University;* Vineeth Kada, *Anthropic PBC;* Mengdi Wu, Ruohan Gao, and Yingyi Huang, *Carnegie Mellon University;* Remi Delacourt, *Mistral AI;* April Yang, *Carnegie Mellon University;* Yingcheng Wang, *Purdue University;* Colin Unger, *Stanford University;* Zhihao Jia, *Carnegie Mellon University and Amazon Web Services*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/oliaro)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/oliaro)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/oliaro)

Finetuning large language models (LLMs) is essential for task adaptation, yet today's serving stacks isolate inference and finetuning on separate GPU clusters—wasting resources and under-utilizing hardware. We introduce FlexLLM, the first system to *co-serve* LLM inference and PEFT-based finetuning on shared GPUs by fusing computation at the token level. FlexLLM's static compilation optimizations—*dependent parallelization* and *graph pruning* significantly shrink activation memory, leading to end-to-end GPU memory savings by up to 80%. At runtime, a novel *token-level finetuning* mechanism paired with a hybrid token scheduler dynamically interleaves inference and training tokens within each co-serving iteration, meeting strict latency SLOs while maximizing utilization. In end-to-end benchmarks on LLaMA-3.1-8B, Qwen-2.5-14B, and Qwen-2.5-32B, FlexLLM maintains inference SLO compliance at up to 20 req/s, and improves finetuning throughput by 1.9-4.8× under heavy inference workloads and 2.5-6.8× under light loads, preserving over 76% of peak finetuning progress even at peak demand. FlexLLM is publicly available at <https://flexllm.github.io>.

Track 2

## Reliability Through Verification

Session Chair: Hongqiang Liu, *Uber*

Grand Ballroom VII–IX

## [Express Lane to Efficiency and Reliability: Multi-Dimensional Control in Meta’s Express Backbone Network](/conference/nsdi26/presentation/iqbal)

Faisal Iqbal, Vitaly Neganov, Brian Chang, Rong Rong, Yuanjun Yao, Marek Denis, Qin Zhang, Alexandru Manea, Anton Marchenko, and Ulas Kozat, *Meta;* Aditya Akella, *The University of Texas at Austin;* Ying Zhang, *Meta*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/iqbal)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/iqbal)

Meta’s Express Backbone (EBB) network interconnects data centers across the globe. As such, it is one of the largest WANs in terms of capacity, traffic and global reach. EBB’s unique multi-plane Software Defined Network (SDN) architecture has passed the test of time with its flexibility, reliability and performance. Nonetheless, in parallel to its success, it has also seen an unprecedented growth in traffic demand and capacity footprint. Along with the rapid rise of AI workloads, challenges in resource utilization and failure recovery started to emerge, driving us to enhance and evolve EBB’s control design to increase its efficiency and resiliency. From our operational experiences, we realize that while foundational per-plane Traffic Engineering (TE) control offers simplicity, there still exists a gap to support the above two goals. We propose to introduce control in two additional dimensions: globally across planes and locally at individual device. Specifically, Unequal Cost Multi-Path (UCMP) enables control across planes for efficient load balancing, and Fast Re-Route (FRR) provides control across time slices for facilitating rapid detection and recovery from failures. We present the design, implementation, and production results of UCMP and FRR, demonstrating how EBB can adapt to AI-era demands rapidly without fundamental architectural changes.

## [Sparse Checkpointing for Fast and Reliable MoE Training](/conference/nsdi26/presentation/gandhi)

Swapnil Gandhi, *Stanford University;* Christos Kozyrakis, *Stanford University and NVIDIA*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/gandhi)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/gandhi)

As large language models scale, training them requires thousands of GPUs over extended durations—making frequent failures an inevitable reality. While checkpointing remains the primary fault-tolerance mechanism, existing methods fall short when applied to Mixture-of-Experts (MoE) models. Due to their substantially larger training state, MoE models exacerbate checkpointing overheads, often causing costly stalls or prolonged recovery that severely degrade training efficiency.

We present MoEvement, a distributed, in-memory checkpointing system tailored for MoE models. MoEvement is built on three key ideas: (1) *sparse checkpointing*, which incrementally snapshots subsets of experts across iterations to reduce overhead; (2) a *sparse-to-dense checkpoint conversion* mechanism that incrementally reconstructs consistent dense checkpoints from sparse snapshots; and (3) *upstream logging* of activations and gradients at pipeline-stage boundaries, enabling localized recovery without re-executing unaffected workers. Evaluations across diverse MoE models with up to 64 experts show that MoEvement reduces checkpointing overhead by up to 4× and recovery overhead by up to 31× compared to state-of-the-art approaches, sustaining ETTR ≥ 0.94 even under frequent failures (MTBF as low as 10 minutes) and delivering up to 8× overall training speedup, all without compromising synchronous training semantics. Overall, MoEvement offers a scalable, practical fault-tolerance solution for the next generation of sparsely activated models.

## [MAE: More Adaptive Video Encoder for Consistent Low Latency in High-Quality Real-Time Communication](/conference/nsdi26/presentation/meng)

Hua Meng, Yufan Zhuang, Yasna Noushirvani, Xiangjie Huang, and Zili Meng, *Hong Kong University of Science and Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/meng)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/meng)

Real-time communication (RTC) is integral to modern digital life. However, high-quality RTC services still experience tail latency spikes. A primary cause of this issue is the sender’s slow adaptation to network fluctuations—when network bandwidth drops, the sender needs to quickly reduce the sending rate to avoid bufferbloat. Existing solutions focus on accelerating reactions in the network, transport layer, or sender-side buffer management, but often overlook a critical component: the reaction of the video encoder. The encoder serves as the content source, where slow convergence to new bitrates can still result in bufferbloat after the encoder. With the increasing video bitrate in high-quality RTC, our measurement shows that the encoder’s reaction is critical. To address this limitation, we propose **M**ore **A**daptive **E**ncoder (MAE), a framework that enables encoders to dynamically adapt to network changes with finer-grained network information. On the encoder side, MAE adaptively adjusts the internal encoding parameters to quickly converge to the target bitrate without affecting the video quality. On the network side, MAE probes the internal state of current congestion control algorithms to preemptively react to potential bandwidth drops, without waiting for the late, backpressured bitrate updates. Trace-driven emulation and real-world experiments demonstrate that our solution, MAE, reduces stall rates by 86.2% while maintaining superior visual quality compared to the state of the art.

## [In Link We Trust: BFT at the Speed of CFT using Switches](/conference/nsdi26/presentation/zeno)

Lior Zeno, Naama Ben-David, and Mark Silberstein, *Technion – Israel Institute of Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zeno)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zeno)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zeno)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zeno)

We introduce *SwitchBFT*, a novel BFT consensus protocol for data centers that matches the performance and fault tolerance guarantees of the fastest Crash Fault Tolerance (CFT) protocols. We take advantage of several unique properties of the trusted network that have emerged in modern data centers. SwitchBFT leverages *packet source authentication* to eliminate the overheads of cryptographic signatures, thus speeding up the fault-free scenario, and utilizes *network switch programmability* to enforce agreement decisions and to verify that safety is not violated, thereby offering robust performance even when some replicas are faulty. Designing a practical BFT that makes the most of these properties requires solving several challenges, such as packet losses and switch crash faults, all within the tight switch resource budget. We show that SwitchBFT outperforms state-of-the-art BFTs in scalability and performance, attaining the speed of NOPaxos, an in-switch CFT implementation.

Track 3

## Virtualization Meets the Network

Session Chair: Maria Apostolaki, *Princeton University*

Bellevue Room

## [Controlling Arbitrary Internet Queues with Titrate](/conference/nsdi26/presentation/zhou-titrate)

Anchengcheng Zhou and Joshua Lau, *Princeton University;* P. Brighten Godfrey, *University of Illinois Urbana–Champaign and Broadcom;* Maria Apostolaki, *Princeton University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhou-titrate)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhou-titrate)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhou-titrate)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhou-titrate)

Router buffers are critical to networks for absorbing short-lived congestion and allowing full throughput. However, excessive buffering can lead to high queuing delay, poor burst absorption, and even low throughput for queues sharing the buffer memory. Existing queue management schemes designed for Internet routers (e.g., CoDel, PIE) prevent such excessive buffering only under stringent assumptions about the queue composition (flows in the queue), while more recent approaches (e.g., L4S) require end-host collaboration. In this work, we revisit queue management for Internet routers from first principles and introduce Titrate, a closed-loop controller that senses queue dynamics and adjusts thresholds for any given queue to achieve high throughput, low latency and effective burst absorption. To balance convergence speed and stability, Titrate draws inspiration from TCP’s control loop, combining a multiplicative-increase-additive-decrease approach with an ssthresh-like variable.

We evaluate Titrate’s performance via simulation and Internet experiments. Across a wide range of realistic traffic mixes, Titrate increases minimum throughput by 39%, 14% compared to CoDel, PIE, while keeping 59% lower queuing latency compared to static-threshold baselines of on-par throughput. It also improves end-user quality of experience over static-threshold baselines. We further show that Titrate reacts swiftly to bandwidth and traffic changes and offers device-wide benefits.

## [Managing Congestion Control Heterogeneity on the Internet with Approximate Performance Isolation](/conference/nsdi26/presentation/mishra)

Ayush Mishra, *ETH Zurich;* Archit Bhatnagar, *University of Michigan;* Yixuan Zhang, *Tsinghua University;* Ben Leong, *National University of Singapore;* Ya Gao, *Wuxi Institute of Technology;* Raj Joshi, *Harvard University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/mishra)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/mishra)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/mishra)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/mishra)

The Internet hosts a diverse mix of congestion control algorithms (CCAs) optimized for specific throughput-delay tradeoffs. However, traditional queuing disciplines and AQMs struggle to manage this heterogeneity and often lead to unfairness and suboptimal performance. In this paper, we explore isolation techniques that can allow competing CCAs to make their desired throughput-delay trade-offs independent of who they compete with. More specifically, we motivate Approximate Performance Isolation between competing flows by grouping flows with similar desired throughput-delay trade-offs in the same queue. We also present Santa, a new practical and scalable multi-queue AQM built on the principles of approximate performance isolation. Santa infers each flow’s throughput-delay preferences by comparing their buffer occupancy, and shuffles aggressive ("naughty") and passive ("nice") flows into appropriate queues over time. We prototype Santa on a programmable switch to demonstrate that it is practical, scalable, and can approximate the isolation benefits of Fair Queuing (FQ) with a handful of of queues.

## [The GOODPUT System: A Machine Learning-Driven Optimization Framework for Dynamic Spectrum Control in Heterogeneous WLANs](/conference/nsdi26/presentation/wang-yu)

Yu Wang and Robert Dick, *University of Michigan*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-yu)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/wang-yu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wang-yu)

Rapid proliferation of wireless devices is leading to spectrum scarcity, particularly in the unlicensed 2.4 GHz and 5 GHz bands. This paper describes a method to optimize goodput (useful communication throughput) in spectrum-constrained scenarios via access point (AP) channel assignments, channel bonding decisions, and wireless device (station) to AP mappings. Goodput demand prediction and real-time spectrum sensing are used to formulate goodput-maximizing mixed-integer linear programming (MILP) problem instances, which are optimally and efficiently solved to produce network configuration decisions. Our approach is compatible with existing IEEE 802.11 protocols (with primary emphasis on IEEE 802.11ax), commercial access points, modern wireless stations, and legacy infrastructures. A prototype of the system was evaluated and compared with the best existing solutions; it increases goodput by 17.1% relative to multi-AP loadbalancing, by 19.3% compared to a machine-learning-based AP selection, and by 47.9% relative to the static RSSI-based methods widely used in existing systems.

## [CStar Gateway: Augmenting Public Cloud Infrastructure for Heterogeneous Network Function Virtualization](/conference/nsdi26/presentation/li-haonan)

Haonan Li, Tian Pan, Jin Ke, Baohai Hu, Changgang Zheng, Enge Song, Zhi Xu, Ye Yang, Bowen Yang, Donglin Lai, Yisong Qiao, Bengbeng Xue, Jianyuan Lu, Xiaoqing Sun, Shize Zhang, Zihao Fan, Mingxin Li, Yang Song, Jun Liang, Xionglie Wei, and Biao Lyu, *Alibaba Cloud;* Rong Wen, *Fudan University and Alibaba Cloud;* Zhigang Zong, *Alibaba Cloud;* Jiao Zhang and Tao Huang, *Purple Mountain Laboratories;* Shunmin Zhu, *Alibaba Cloud*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/li-haonan)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/li-haonan)

Major cloud providers often build NFV products by reusing existing architectures. These designs were originally developed and optimized for tenant virtual machines (VMs) that operate at network endpoints. In contrast, network function (NF) VMs function as intermediate forwarding nodes shared by multiple tenants, which have very different resource demands. Directly applying tenant-oriented designs creates mismatches between infrastructure capabilities and NF requirements. A common case arises when NF VMs serve many tenants: they typically exhaust vNIC and sessions on vSwitches well before CPU resources are saturated. At this point, NF VMs cannot accept additional traffic despite having idle CPU cycles. Providers usually address this by scaling out or scaling up NF VMs, which wastes resources and increases cost. This is just one example, where numerous other mismatches remain. To address these, we present CStar Gateway. CStar Gateway shifts NF VM multi-tenancy support from vSwitches into NF VMs, which reduces vNIC and session bottlenecks with minimal changes to the existing cloud infrastructure. CStar Gateway also identifies and redirects I/O- or CPU-intensive flows to FPGA-based NFs, increasing the service capacity. In addition, CStar Gateway takes over NF VM elasticity support from vSwitch, simplifying and accelerating the scaling process, and thereby enhancing overall system flexibility. Deployment results show that the design improves CPU and I/O utilization of NF VMs by at least 5x and reduces NF cluster capital expenditure by 71.91% to 88.57%.

### 3:20 pm–3:50 pm

## Coffee and Tea Break

Grand Pre-Function Area

### 3:50 pm–5:30 pm

Track 1

## Clouds, Carefully Engineered

Session Char: Seojin Park, *University of Southern California*

Grand Ballroom I–VI

## [DistRS: Disaggregated Reward Service for RLVR with Batch-Level Constraint](/conference/nsdi26/presentation/zhu-ruidong)

Ruidong Zhu, *School of Computer Science, Peking University;* Mingcong Han, *ByteDance Seed;* Yinmin Zhong, *School of Computer Science, Peking University;* Wencong Xiao, *ByteDance Seed;* Xuanzhe Liu and Xin Jin, *School of Computer Science, Peking University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhu-ruidong)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhu-ruidong)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhu-ruidong)

Reinforcement Learning with Verifiable Rewards (RLVR) has emerged as a key post-training paradigm for enhancing the capabilities of large language models (LLMs). As the complexity increases and resource consumption grows, reward computation is becoming a critical workload in the RLVR training process.

We present DistRS, a disaggregated reward service framework designed to provide resource-efficient reward computation for RLVR training. Through the analysis of a real RLVR training task, we observe that the reward service faces a highly dynamic workload, motivating the need for elasticity and multi-tenancy. DistRS leverages request-level flexibility from the *request-in, batch-out* characteristic of reward computation to design more resource-efficient scaling and scheduling policies. Specifically, DistRS establishes a batch-level constraint for each training task that relaxes latency requirements at the request level. Building on this foundation, we design a history-based resource scaling policy and a batch-level priority-based request scheduling policy. In addition, DistRS incorporates a timeout-aware mechanism to adjust resource allocation, thereby mitigating the impact of deviations between history and actual execution. We evaluate DistRS with real-world RLVR training tasks and the results demonstrate that DistRS reduces resource consumption by up to 3.79× while incurring minimal overhead on training progress.

## [MuxTune: Efficient Multi-Task LLM Fine-Tuning in Multi-Tenant Datacenters via Spatial-Temporal Backbone Multiplexing](/conference/nsdi26/presentation/xue-chunyu)

Chunyu Xue and Yi Pan, *Shanghai Jiao Tong University;* Weihao Cui, *Shanghai Jiao Tong University and National University of Singapore;* Quan Chen and Shulai Zhang, *Shanghai Jiao Tong University;* Bingsheng He, *National University of Singapore;* Minyi Guo, *Shanghai Jiao Tong University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xue-chunyu)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/xue-chunyu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/xue-chunyu)

Parameter-Efficient Fine-Tuning (PEFT) is widely applied as the backend of fine-tuning APIs for large language model (LLM) customization in datacenters. Service providers deploy separate instances for individual PEFT tasks, giving rise to prominent resource inefficiencies, including (1) GPU underutilization from small-scale, PEFT-native operators and (2) device stalls from communication delays and data dependencies in parallelized execution. To address these issues, this paper presents MuxTune, a fine-tuning system that enables resource-efficient concurrent execution of multiple PEFT tasks. The key idea is to multiplex the backbone across independent tasks in a spatial-temporal manner for improved utilization and reduced stalls. Building on flexible, modularized backbone sharing via unified PEFT representations, MuxTune proposes hierarchical co-scheduling scheme with task, operator, and data-level optimizations. Specifically, it fuses tasks through a hybrid of spatial and temporal multiplexing, and orchestrates multi-task operator execution in two-tiered hybrid parallelism. Additionally, MuxTune employs chunk-based data alignment to mitigate inter-task ineffective tokens. Experimental results demonstrate that MuxTune achieves up to 2.33× higher throughput and 5.29× memory reduction compared to three state-of-the-art baselines.

## [CCC: Re-architecting Delay-based Congestion Control in Datacenter Networks](/conference/nsdi26/presentation/jiang)

Wanchun Jiang, Haoyang Li, Kai Wang, Yujie Hu, and Xiao Han, *Central South University;* Danfeng Shan, *Xi'an Jiaotong University;* Fengyuan Ren, *Tsinghua University;* Jiawei Huang and Jianxin Wang, *Central South University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/jiang)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/jiang)

In datacenter networks, delay-based congestion control (CC) algorithms are popular and protocols such as TIMELY and SWIFT are employed in production. However, even if delay signals are precisely measured, the congestion information deduction (CiD) may be incorrect under certain conditions, degrading the performance of CC. To address this problem, we re-architect the delay-based CC to make rate adjustments based not only on the congestion states but also the CiD trustworthiness. Based on this architecture, the CiD-sensitive congestion control (CCC) is developed. Specifically, CCC demarcates the regions, where the CiD from delay signals is untrustworthy, with the assistance of well-designed congestion criteria and inherent system inertia. When the CiD is untrustworthy, CCC constructs the probing rate adjustment rules for both the rapid response to congestion and the subsequent trustworthy CiD. Otherwise, CCC conducts the analytical rate adjustment to both reach the expected congestion state and keep the trustworthy CiD, fully leveraging the abundant information in delay signals. DPDK-based experiments and large-scale simulations confirm that CCC achieves similar good performance as INT-based CCs, including HPCC and PowerTCP, by using only delay signals, outperforming DCQCN, TIMELY, and SWIFT.

## [Starfish: A Topology-Routing Co-Design for Small-Scale Data Centers](/conference/nsdi26/presentation/zhou-starfish)

Anchengcheng Zhou, *Princeton University;* Vipul Harsh, *Conviva;* Sangeetha Abdu Jyothi, *UC Irvine;* Maria Apostolaki, *Princeton University;* Brighten Godfrey, *UIUC*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhou-starfish)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhou-starfish)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhou-starfish)

Most data centers today operate at scales much smaller than hyperscalers, i.e., hosting only hundreds to a few thousand servers, yet their design has received disproportionately little attention in the literature. Leaf-spine is nearly ubiquitous in small-scale data centers, but presents a fundamental tradeoff: provisioning full non-blocking capacity is costly, while oversubscription reduces cost but under-serves bursty, skewed workloads. Recent expander-based designs could, in theory, offer better performance but face substantial deployment hurdles, including lacking a practical routing scheme.

We introduce Starfish, a topology-routing co-design tailored to small-scale data centers, that delivers high performance, fault tolerance, and ease of deployment. Starfish’s topology, DRing, increases per-server egress capacity by spreading servers across all switches, reduces latency–even under failure scenarios–by exposing diverse near-shortest paths, and eases deployment by organizing switches into uniform blocks. Starfish’s routing leverages structural properties of DRing and effectively adapts to traffic patterns using standard hardware and protocols. Notably, Starfish’s routing also generalizes to expander-based topologies.

Evaluation shows that Starfish supports 56% more traffic on average than leaf-spine built with the same equipment across real-world traces. This demonstrates that small-scale data centers today can realistically achieve higher performance with their existing equipment. Starfish’s routing also enables an expander-based design to support 52% more traffic on average than leaf-spine. More broadly, this work takes a first step towards a distinct design space for small-scale data centers.

## [HEDGE: Traffic Engineering with Probabilistic Link Capacities](/conference/nsdi26/presentation/devraj)

Arjun Devraj, *Cornell University;* Bill Owens, *NYSERNet;* Umesh Krishnaswamy, *Microsoft;* Ying Zhang, *Meta;* Rachee Singh, *Cornell University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/devraj)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/devraj)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/devraj)

Cloud providers have adopted higher modulation formats to achieve higher data-rate wavelengths in their optical wide-area networks. However, higher modulation formats reduce signal quality margins, making wavelengths more susceptible to wavelength-specific faults (WSFs)—temporary faults that selectively affect certain wavelengths while others remain unaffected, even though they all share the same optical fiber and equipment. WSFs cause the capacity of inter-datacenter links to fluctuate, frequently disrupting traffic engineering systems. We propose HEDGE, a system that mitigates the effects of WSFs by implementing link-local resilience and global network-wide resilience against WSFs. For local resilience, HEDGE provisions inter-datacenter links with a guaranteed minimum capacity and availability target, in spite of WSFs, while using the fewest possible constituent wavelengths. For global resilience, HEDGE optimally balances throughput and availability while allocating flows on a stochastic wide-area network with fluctuating link capacities. HEDGE sustains equivalent throughput with state-of-the-art traffic engineering systems, while dropping 12.2× less network flow in worst-case scenarios and reducing disruptions to tunnel allocations by 622× in spite of a rapidly changing topology.

Track 2

## When Systems Run Themselves

Session Chair: Muhammad Shahbaz, *University of Michigan*

Grand Ballroom VII–IX

## [CascadeNet: Generating Network Traffic with High-Fidelity Temporal Patterns](/conference/nsdi26/presentation/lu-runwei)

Runwei Lu, Yanran Deng, Ruixuan Li, and Jinting Liu, *New York University Shanghai;* Yuejie Wang, *Peking University;* Xinyu Li, *Carnegie Mellon University;* Deming Xu, *New York University Shanghai;* Han Tian, *University of Science and Technology of China;* Kai Chen, *Hong Kong University of Science and Technology;* Guyue Liu, *Peking University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lu-runwei)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lu-runwei)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/lu-runwei)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/lu-runwei)

Facing the challenge of limited network trace access, the exploration of synthetic trace generation has become crucial for research. Although current methods manage to replicate the statistical characteristics of network traffic accurately, they fail to capture the temporal dynamics of network activities. This gap stems primarily from their approach to data representation. To address this issue, we propose a novel representation of network traces by aggregating network flows into time series. Built upon this data representation, we propose CascadeNet, an end-to-end framework embedded with CascadeGAN—a hierarchical generative model—to generate network traffic with high-fidelity temporal patterns while learning complex flow structures and dependencies. We also develop several techniques to facilitate the transformation from aggregated time series to timestamps. Our evaluations across four diverse IPv4 header traces show (1) CascadeNet surpasses baselines by 41%~76% on temporal distance metrics; (2) CascadeNet outperforms baselines in downstream tasks; (3) it offers remarkable scalability, reducing training time by 7.3×~25× compared to state-of-the-art method.

## [Diagnosing and Repairing Distributed Routing Configurations Using Selective Symbolic Simulation](/conference/nsdi26/presentation/yang)

Rulan Yang, Gao Han, Hanyang Shao, Xiaoqiang Zheng, Xing Fang, Ziyi Wang, and Lizhao You, *Xiamen University;* Ruiting Zhou, *Southeast University;* Linghe Kong, *Shanghai Jiao Tong University;* Ennan Zhai, *Alibaba Cloud;* Qiao Xiang and Jiwu Shu, *Xiamen University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/yang)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/yang)

Although substantial progress has been made in automatically verifying whether distributed routing configurations comply with certain intents, diagnosing and repairing configuration errors remains manual and time-consuming. To fill this gap, we propose S2Sim, a novel system for automatic routing configuration diagnosis and repair. Our key insight is that by deriving a set of contracts that guarantees an intent-compliant variant of the erroneous configuration, we can systematically check for all contract violations in the configuration via symbolic simulation to pinpoint and repair the errors. S2Sim also introduces a series of extensions to support complex configurations (e.g., ACL, route aggregation and multi-path routing), networks (e.g., underlay and overlay networks), and intents (e.g., k-link failure tolerance). We fully implement S2Sim and evaluate its performance using real configurations from two major providers and synthesized configurations composed from their real errors and real-world topologies with different scales O(10) to O(1000). Results show that S2Sim accurately and efficiently diagnoses and repairs real configuration errors (i.e., up to 20 seconds in real networks of O(100) nodes and up to 15 minutes in synthesized networks of O(1000) nodes).

## [A Composable Emulation Framework for Whitebox Switches](/conference/nsdi26/presentation/miao-whitebox)

Congcong Miao, *Tencent;* Xianneng Zou, *Tencent and Tsinghua Shenzhen International Graduate School;* Chuwen Zhang, *Tsinghua University;* Shiping Yang, Qihang Liu, Zhijie Yan, and Yanke Zhang, *Tencent;* Yong Jiang, *Tsinghua Shenzhen International Graduate School;* Qiao Xiang, *Xiamen University;* Xin Jin, *Peking University;* Zili Meng, *Hong Kong University of Science and Technology;* Ang Chen, *University of Michigan*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/miao-whitebox)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/miao-whitebox)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/miao-whitebox)

High-fidelity network emulation is indispensable for reliable operation at scale. While existing emulators are built for monolithic, blackbox switches, emerging switch architectures are chipping away at this assumption. Cloud providers routinely source device modules from different vendors and compose them together to construct disaggregated, whitebox switches. This raises novel challenges in network emulation, as we must move from building bespoke firmware-based emulators to a composable emulation framework where diverse emulators can be stitched together for high-fidelity emulation: whether for data plane, control plane, or peripheral modules (e.g., optical components). We have designed the first such framework, MirSwitch, addressing key challenges in reconciling interface contract differences across emulator modules using an adaptor-centric approach. MirSwitch can faithfully emulate a wide range of functionalities of whitebox switches, while achieving 2.2× forwarding performance improvements which are critical for forwarding emulation. We have deployed MirSwitch in our production network, which our operators have used to troubleshoot 97.5% of a total of 203 issues in a recent year.

## [Harp: Improving VPC Network Availability via Efficient Failure Detection and Rerouting in Tencent Cloud](/conference/nsdi26/presentation/hu-jiayu)

Jiayu Hu, Feng Jin, and Xianping Zhou, *Tencent;* Kai Zhang, *Fudan University;* Zhen Shen and Yongkang Luo, *Tencent*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/hu-jiayu)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/hu-jiayu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/hu-jiayu)

We present Harp, a mechanism for efficient and robust failure detection and recovery for VPC networks. Unlike previous approaches, Harp does not rely on specific hardware features or transport protocols. Instead, Harp is a lightweight software implementation that identifies feasible physical paths between each pair of communicating hosts and monitors their health states. When network failures occur, Harp can swiftly switch influenced flows from a failed path to a healthy path within a short interval. Harp has been deployed in Tencent Cloud for more than two years and has proven its effectiveness in handling network failures. According to the results from production systems, Harp can significantly reduce the VPC network's outage time by 78.71%-99.97% and essentially bypass failed paths on a sub-second timescale. We also share our experiences of how Harp efficiently detects and handles network failures when deployed in Tencent Cloud.

## [Themis: Detecting Distributed Concurrency Bugs through RPC-Driven Race-Directed Test Generation and Fuzzing](/conference/nsdi26/presentation/cao)

Hongchen Cao and Jingzhu He, *ShanghaiTech University;* Ting Dai, *InsightFinder AI;* Guoliang Jin, *North Carolina State University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/cao)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/cao)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/cao)

Distributed concurrency bugs occur when concurrent execution flows, at least one of which is triggered by inter-node communication such as remote procedure calls (RPCs), access the same shared variable or object in conflicting ways, causing incorrect behavior under certain interleavings. Existing work for detecting distributed concurrency bugs focuses on dynamic approaches, thus suffering from limited coverage. This paper proposes Themis, a novel approach that uses static analysis to detect potential races, applies LLM-based test generation, and employs directed fuzzing to refine input parameters for detecting distributed concurrency bugs. We have implemented a prototype of Themis and evaluated it on eight real-world distributed systems. Themis detects 198 new violations corresponding to 52 new bugs.

Track 3

## From Fiber to Radio

Session Chair: Lili Qiu, *Microsoft Research*

Bellevue Room

## [Bridging Storage and Execution: A Semantic Virtual Bus for On-Demand Application Streaming](/conference/nsdi26/presentation/lu-jun)

Jun Lu, *Central South University;* Jialin Li, *National University of Singapore;* Yaoxue Zhang and Ju Ren, *Tsinghua University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lu-jun)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lu-jun)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/lu-jun)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/lu-jun)

Traditional application delivery requires full local installation, incurring persistent security risks from outdated versions, significant download delays. Despite advances in network throughput and latency, existing dynamic loading solutions such as Web applications and network filesystems like NFS suffer from performance degradation, functionality limitations, and intrusive application modifications. We introduce STREAMBUS, a transparent application streaming system that redefines the network as a semantic-aware virtual storage bus beneath the file system layer. Supporting deployment across diverse environments, including WiFi-dependent mobile devices, it addresses two key challenges: maintaining microsecond-level latency comparable to local storage and bridging the semantic gap between stateless remote storage and stateful execution. To achieve this, STREAMBUS combines a dual-mode transmission mechanism that synchronously serves requested blocks and asynchronously prefetches predicted blocks, with a thread-aware Markov-chain model that captures fine-grained access patterns. Evaluation shows STREAMBUS delivers near-native performance across diverse networks. On desktops, it achieves 15–40% better per-page access latency than local NVMe in common cases. On mobile devices, it typically sustains startup overheads below 40% relative to local storage, even over variable Wi-Fi connectivity. Robustness experiments demonstrate stable performance under emulated network conditions with realistic delay patterns, supporting intra-city deployments.

## [QCON: Seamless QoE-Aware 5G Streaming via Multi-Connectivity](/conference/nsdi26/presentation/lee)

Goodsol Lee, *Seoul National University;* Junhong Min, *University of Colorado Boulder;* Seyeon Kim, *Korea University;* Juheon Yi, *Seoul National University;* Kwang Taik Kim and Mung Chiang, *Purdue University;* Sangtae Ha, *University of Colorado Boulder;* Kyunghan Lee and Saewoong Bahk, *Seoul National University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lee)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lee)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/lee)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/lee)

Mobile real-time video streaming (RTS) applications—cloud gaming and AR/VR—require consistent high throughput and low latency to satisfy user Quality of Experience (QoE), yet today’s wireless links fluctuate wildly. While multi-path solutions seem promising to tackle such single-link fluctuations, existing transport-level solutions require multiple cellular subscriptions, which most users don’t have. In this paper, we leverage 5G multi-connectivity, which allows simultaneous connection to multiple base stations (e.g., 5G and 4G) and is already deployed in commercial networks. However, our measurements show RTS applications still suffer from single-link fluctuations due to operators’ deliberate policies restricting multi-connectivity to conserve 4G backup links regardless of application demands. To optimize application QoE while respecting operator policies, we present QCON, a QoE-driven multi-connectivity solution that efficiently utilizes backup links based on precise application QoE. For practical deployment, we design QoE Monitor to infer application QoE within the RAN and develop multi-link scheduling to optimize both QoE and radio resource efficiency. We also design priority-based re-injection utilizing RAN link recovery mechanism to prevent video stalls. Our prototype implementation of QCON on a RAN intelligent controller within an Open-RAN testbed demonstrates 2.1× improvements of bitrates, enhancing tail frame rates by 4-5× with efficient backup link use compared to existing multi-link scheduling schemes.

## [Law: Towards Consistent Low Latency in 802.11 Home Networks](/conference/nsdi26/presentation/shen-yibin)

Yibin Shen and Zili Meng, *Hong Kong University of Science and Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/shen-yibin)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/shen-yibin)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/shen-yibin)

Wireless ultra-low-latency video streaming over 802.11 WiFi networks is increasingly popular, but the latency on the Wi-Fi link is always fluctuating. With the development of CDNs and edge servers, the fluctuation of the wireless lasthop is increasingly dominating the fluctuation of the end-toend latency. In this paper, we investigate the reasons why the existing Wi-Fi link layer will have a fluctuating latency from a systematic perspective. We find that the hierarchical queueing structure, queue-agnostic rate adaptation, and delay-insensitive retry management of the existing link layer design are the main reasons to a latency spike when channel fluctuates. Thus, we propose LAtency-bounded Wi-Fi (Law), an 802.11 link layer architecture to provide a consistent low latency for the application. Law exploits the loss tolerance ability from the upper layer video streaming application and significantly avoids the latency spikes caused by the blockage in the link layer at the cost of acceptably additional packet loss. Law maintains a high goodput by carefully redesigning the queueing structure and introducing fine-grained control for each transmission opportunity. We implement the prototype of Law on OpenWiFi and test it with WebRTC – both the tail frame latency and stall rate can be significantly reduced over existing baselines.

## [Enabling SLO-Aware 5G Multi-Access Edge Computing with SMEC](/conference/nsdi26/presentation/zhang-xiao)

Xiao Zhang and Daehyeok Kim, *University of Texas at Austin*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhang-xiao)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhang-xiao)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhang-xiao)

5G Multi-access edge computing (MEC) promises to enable latency-critical applications by bringing computational power closer to mobile devices, but our measurements on commercial MEC deployments reveal frequent SLO violations due to high tail latencies. We identify resource contention at the RAN and the edge server as the root cause, compounded by SLO-unaware schedulers. Existing SLO-aware MEC schedulers require RAN-edge coordination, making them impractical for deployment and prone to poor performance due to coordination delays, limited heterogeneous application support, and ignoring edge resource contention. This paper introduces MEC, a practical, SLO-aware resource management framework that facilitates deadline-aware scheduling through fully decoupled operations at the RAN and edge servers. Our key insight is that standard 5G protocols and application behaviors naturally provide information exploitable for SLO-aware management without extensive infrastructure or application changes. Evaluation on our 5G testbed shows that MEC achieves 90–96% SLO satisfaction versus under 6% for existing approaches, while reducing tail latency by up to 122×.

## [Learning to Tune Optical WANs: A Field Deployment of Noise Models in Optical Networks](/conference/nsdi26/presentation/kataria)

Bhaskar Kataria and Howard Hua, *Cornell University;* Andrea D Amico, *NEC Labs;* Bill Owens, *NYSERNet;* Rachee Singh, *Cornell University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/kataria)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/kataria)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/kataria)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/kataria)

Accurately modeling optical signal transmission is critical for optimizing network performance, particularly in large-scale fiber optic networks operated by Internet Service Providers. In this work, we develop a Gaussian Noise model for a New York state ISP's optical backbone. Our model accounts for all major network components, including amplifiers, fiber spans, reconfigurable optical add-drop multiplexers, and transceivers. By accurately predicting end-to-end signal-to-noise ratio, our model provides a foundation for network performance analysis and optimization.  
Then, we leverage hyperparameter search techniques—commonly used in machine learning—to identify amplifier gain settings that improve signal quality. By treating the model as an opaque box, we systematically search for amplifier configurations that maximize the predicted end-to-end SNR while maintaining practical network constraints. We validate our approach through a field deployment by applying optimized amplifier gain settings in a live ISP network. Our results show a significant improvement in optical signal quality, achieving a 2 dB increase in SNR on a single wavelength.

### 6:00 pm–7:30 pm

## NSDI '26 Poster Session and Reception

Lake Washington Ballroom

*Sponsored by Amazon*

Check out the cool new ideas and the latest preliminary research on display at the Poster Session and Reception. Enjoy dinner, drinks, and the chance to connect with other attendees, authors, and symposium organizers. View the list of [accepted posters](/conference/nsdi26/poster-session).

## Wednesday, May 6

### 8:00 am–9:00 am

## Continental Breakfast

Grand Pre-Function Area

### 9:00 am–10:20 am

Track 1

## When ML Meets Its Network

Session Chair: Francis Yan, *University of Illinois at Urbana–Champaign*

Grand Ballroom I–VI

## [Enabling AI Network Cross-Layer Design and Operations with Arcadia: A Simulation Platform at Scale](/conference/nsdi26/presentation/wang-zhaodong)

Zhaodong Wang, Satyajeet Singh Ahuja, Xu Zhang, Yuhui Zhang, Max Noormohammadpour, Gregory R. Steinbrecher, Thomas Fuller, Xin Liu, Kevin Quirk, Mikel Jimenez Fernandez, Abhinav Triguna, Yan Cai, and Steve Politis, *Meta Platforms;* Petr Lapukhov and Naader Hasani, *Nvidia;* Ying Zhang, *Meta Platforms*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-zhaodong)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wang-zhaodong)

The rapid evolution of Artificial Intelligence (AI) technology is fueling significant investments by hyperscalers, making AI networks crucial for large-scale training. Understanding the design impacts on AI training requires systematic, cross-layer evaluation. Production experience highlights the need for a robust simulation platform to guide network design and operations. This paper defines the platform requirements, addresses complex design challenges, and shares our experience building Arcadia, a scalable, high-fidelity simulation platform for AI Networks. It operates at the cluster level, focusing on overall cluster performance rather than individual job performance. By using our fast-forwarding, lock free, and synchronization-cost reduction mechanisms, Arcadia achieves scalability and speed, allowing us to faithfully simulate real-world-scale training clusters and plays an important role in guiding Meta's AI network evolution.

## [Phantora: Maximizing Code Reuse in Simulation-based Machine Learning System Performance Estimation](/conference/nsdi26/presentation/qin)

Jianxing Qin, *Duke University;* Jingrong Chen, *Uber;* Xinhao Kong, *NVIDIA;* Yongji Wu, *University of California, Berkeley;* Tianjun Yuan, *Duke University;* Liang Luo, Zhaodong Wang, and Ying Zhang, *Meta;* Tingjun Chen, Alvin R. Lebeck, and Danyang Zhuo, *Duke University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/qin)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/qin)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/qin)

Modern machine learning (ML) training workloads place substantial demands on both computational and communication resources. Consequently, accurate performance estimation has become increasingly critical for guiding system design decisions, such as the selection of parallelization strategies, cluster configurations, and hardware provisioning. Existing simulation-based performance estimation requires reimplementing the ML framework in a simulator, which demands significant manual effort and is hard to maintain as ML frameworks evolve rapidly.

This paper introduces Phantora, a hybrid GPU cluster simulator designed for performance estimation of ML training workloads. Phantora executes unmodified ML frameworks as is within a distributed, containerized environment. Each container emulates the behavior of a GPU server in a large-scale cluster, while Phantora intercepts and simulates GPU- and communication-related operations to provide high-fidelity performance estimation. We call this approach hybrid simulation of ML systems, in contrast to traditional methods that simulate static workloads. The primary advantage of hybrid simulation is that it allows direct reuse of ML framework source code in simulation, avoiding the need for reimplementation. Our evaluation shows that Phantora provides accuracy comparable to static workload simulation while supporting three state-of-the-art LLM training frameworks out-of-the-box. In addition, Phantora operates on a single GPU, eliminating the need for the resource-intensive trace collection and workload extraction steps required by traditional trace-based simulators. Phantora is open-sourced at <https://github.com/QDelta/Phantora>.

## [PrvTel: Lightweight Models for Private and Accurate Telemetry Data Retention](/conference/nsdi26/presentation/zhou-yajie)

Yajie Zhou, *University of Maryland;* Fuheng Zhao, *University of Utah;* Eric Wang, *University of Maryland;* Ayse K. Coskun, *Boston University;* Divyakant Agrawal and Amr El Abbadi, *University of California, Santa Barbara;* Zaoxing Liu, *University of Maryland*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhou-yajie)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhou-yajie)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhou-yajie)

Network operators rely on telemetry for performance and security analysis, but long-term retention at scale remains difficult due to privacy requirements, resource constraints, and the need for high-fidelity query answers. We present PrvTel, a framework for privacy-preserving telemetry retention. Instead of storing raw records, PrvTel learns a compact generative model using a domain-specialized variational autoencoder. It combines field-aware encodings for NetFlow and cloud telemetry with a correlation-aware objective to preserve cross-field dependencies. To enforce differential privacy (DP) without sacrificing utility, PrvTel injects structure-aware noise before training, rather than during gradient updates. We prove that PrvTel satisfies DP based on post-processing theorem. Across six real-world datasets and one synthetic workload, PrvTel improves query accuracy by up to 60% over prior DP-compliant generative baselines and reduces ownership cost by up to 50× compared to lossless retention.

## [ServeGen: Workload Characterization and Generation of Large Language Model Serving in Production](/conference/nsdi26/presentation/xiang-servegen)

Yuxing Xiang, *Peking University and Alibaba Group;* Xue Li and Kun Qian, *Alibaba Group;* Yan Zhang, *Peking University;* Wenyuan Yu and Ennan Zhai, *Alibaba Group;* Xin Jin, *Peking University;* Jingren Zhou, *Alibaba Group*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xiang-servegen)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/xiang-servegen)

With the widespread adoption of Large Language Models (LLMs), serving LLM inference requests has become an increasingly important task, attracting active research advancements. Practical workloads play an essential role in this process: they are critical for motivating and benchmarking serving techniques and systems. However, the existing understanding of real-world LLM serving workloads is limited due to the lack of a comprehensive workload characterization. Prior analyses remain insufficient in scale and scope, thus failing to fully capture intricate workload characteristics.

In this paper, we fill the gap with an in-depth characterization of LLM serving workloads collected from our worldwide cloud LLM serving service, covering not only language models but also emerging *multimodal* and *reasoning* models, unveiling important *new* findings in each case. Moreover, based on our findings, we propose ServeGen, a principled framework for generating realistic LLM serving workloads by composing them on a per-client basis. Practical use cases validate that ServeGen achieves more accurate performance benchmarking compared to naive workload generation, and reveals new design implications that could otherwise be overlooked. ServeGen is open-sourced at <https://github.com/alibaba/ServeGen>.

Track 2

## Networked Resources, Virtualized

Session Chair: Anu Mercian, *Google*

Grand Ballroom VII–IX

## [REAL: Emulating Control Plane at Simulator’s Cost](/conference/nsdi26/presentation/xia)

Ze Xia, Hao Li, Jinyu Fu, Xin Wan, Yihan Dang, and Danfeng Shan, *Xi'an Jiaotong University;* Li Chen, *harnets.ai;* Peng Zhang, *Xi'an Jiaotong University*

***Community Award Winner!***

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xia)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/xia)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/xia)

Validating control plane behavior and ensuring policy compliance in modern, large-scale networks is a critical challenge. Simulation-based approaches offer low computational and memory costs, but their level of abstraction fails to capture vendor-specific device behaviors, limiting their accuracy for real-world validation. In contrast, control plane emulation provides high fidelity by using unmodified router containers that preserve these vendor-specific details, but its excessive computational and memory requirements make it impractical for large networks. In this paper, we present REAL, a lightweight runtime that emulates control planes using unmodified router containers but at the cost of simulation-based approaches. REAL achieves this by simulating a lightweight data plane to accelerate boot-up, employing a two-phase scheduling policy to minimize cache inefficiencies during convergence, and enabling iterative convergence to reduce peak memory usage by partitioning the network. Our evaluation shows that REAL emulates a 1,000-node network 4× faster than state-of-the-art simulation while preserving vendor-specific behaviors, and can scale to 4,500 nodes on four commodity servers by shaving 8.3× memory.

## [ZOC: Elastic and Cost-Efficient Virtual SmartNIC Architecture for Cloud Physical Machines](/conference/nsdi26/presentation/guan-naixuan)

Naixuan Guan, Xiaokang Hu, Yisheng Xie, Xishi Qiu, Chaojie Liu, Yuchao Cao, Banghao Ying, Dianchen Tian, Yu Zhou, Yangzeyu Zhang, Hujun Ge, Yibin Shen, and Jiesheng Wu, *Alibaba Cloud Computing*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/guan-naixuan)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/guan-naixuan)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/guan-naixuan)

DPU-based SmartNICs are reshaping cloud infrastructure by offloading core I/O functions, enabling cloud physical machines that support both bare-metal and virtualized environments. However, large-scale deployments face practical challenges—including operational inconsistency across heterogeneous fleets, limited resource elasticity, and performance bottlenecks caused by slow-path processing. We present ZOC, a software-defined virtual SmartNIC architecture that transforms general-purpose servers equipped with commodity NICs into full-featured cloud physical machines. ZOC delivers compatibility with existing infrastructure and provides a user experience on par with DPU-based nodes—without requiring any specialized hardware. At its core, ZOC integrates a passthrough NIC and dynamically provisioned host resources into a dedicated service VM, forming an elastic and programmable acceleration platform. Built upon this foundation, it introduces an efficient cross-domain device abstraction that exposes standardized I/O devices to the host, enabling seamless access to cloud storage and VPC networks. Extensive evaluation shows that ZOC achieves superior cost efficiency, eliminates slow-path bottlenecks, and provides high maintainability. Deployed in a major cloud, ZOC serves diverse public and private cloud services as a production-ready complement to existing DPU-based solutions.

## [SLATE: Service Layer Traffic Engineering](/conference/nsdi26/presentation/lim)

Gangmuk Lim, *University of Illinois Urbana–Champaign;* Aditya Prerepa, *University of Illinois Urbana–Champaign and xAI;* Brighten Godfrey and Radhika Mittal, *University of Illinois Urbana–Champaign*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lim)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lim)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/lim)

In microservice-based applications, requests flow between many microservice instances across potentially multiple geodistributed clusters. Today, the routing of requests is limited to simple load balancing, or extensions that spill requests to nearby clusters. We argue that the problem is more subtle, and that there are significant opportunities for improvement by viewing microservice request routing as a global traffic engineering problem. We present Service Layer Traffic Engineering (SLATE), a system that optimizes request routing in microservice deployments that span multiple clusters to minimize average latency and bandwidth cost. SLATE tackles challenges unique to the service layer, including multiple request traffic classes, multi-hop call trees, and service latency profiles. To achieve this, SLATE takes a unique hybrid approach combining global optimization and local exploration. SLATE outperforms state-of-the-art global load balancing by up to 18.3× in average latency and reduces egress bandwidth cost by up to 2.64× in a Kubernetes deployment of an open-source benchmark application, and shows resilient performance against dynamic changes due to its hybrid optimization approach. Our system is completely transparent to the application and can be seamlessly plugged into existing L7 proxy deployments, specifically Envoy.

## [A Fast Solver-Free Algorithm for Traffic Engineering in Large-Scale Data Center Network](/conference/nsdi26/presentation/mao)

Yingming Mao, *Xi'an Jiaotong University and Shanghai Innovation Institute;* Qiaozhu Zhai, *Xi'an Jiaotong University;* Ximeng Liu, *Shanghai Jiao Tong University;* Zhen Yao and Xia Zhu, *Huawei;* Yuzhou Zhou, *Xi'an Jiaotong University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/mao)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/mao)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/mao)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/mao)

Rapid growth of data center networks (DCNs) poses significant challenges for large-scale traffic engineering (TE). Existing acceleration strategies, which rely on commercial solvers or deep learning, face scalability issues and struggle with degrading performance or long computational time.

Unlike existing algorithms adopting parallel strategies, we propose Sequential Source-Destination Optimization (SSDO), a sequential solver-free algorithm for intra-DCN TE. SSDO decomposes the problem into subproblems, each focused on adjusting the split ratios for a specific source-destination (SD) demand while keeping others fixed. To enhance the efficiency of subproblem optimization, we design a Balanced Binary Search Method (BBSM), which identifies the most balanced split ratios among multiple solutions that minimize Maximum Link Utilization (MLU). SSDO dynamically updates the sequence of SDs based on real-time utilization, which accelerates convergence and enhances solution quality.

We evaluate SSDO primarily on Meta DCNs, and additionally on two WAN topologies as auxiliary demonstrations of generality. In a Meta topology, SSDO achieves a 65% and 60% reduction in normalized MLU compared to TEAL and POP, two state-of-the-art TE acceleration methods, while delivering a 12× speedup over POP. These results demonstrate the superior performance of SSDO in large-scale TE.

Track 3

## Hardware, Mobility, and Systems

Session Chair: Yuanchao Shu, *Zhejiang University*

Bellevue Room

## [AVA: Towards Agentic Video Analytics with Vision Language Models](/conference/nsdi26/presentation/yan)

Yuxuan Yan, *Zhejiang University;* Shiqi Jiang, *Microsoft Research;* Ting Cao, *Tsinghua University;* Yifan Yang, *Microsoft Research;* Qianqian Yang and Yuanchao Shu, *Zhejiang University;* Yuqing Yang and Lili Qiu, *Microsoft Research*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/yan)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/yan)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/yan)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/yan)

AI-driven video analytics has become increasingly important across diverse domains. However, existing systems are often constrained to specific, predefined tasks, limiting their adaptability in open-ended analytical scenarios. The recent emergence of Vision Language Models (VLMs) as transformative technologies offers significant potential for enabling open-ended video understanding, reasoning, and analytics. Nevertheless, their limited context windows present challenges when processing ultra-long video content, which is prevalent in real-world applications. To address this, we introduce AVA, a VLM-powered system designed for open-ended, advanced video analytics. AVA incorporates two key innovations: (1) the near real-time construction of Event Knowledge Graphs (EKGs) for efficient indexing of long or continuous video streams, and (2) an agentic retrieval-generation mechanism that leverages EKGs to handle complex and diverse queries. Comprehensive evaluations on public benchmarks, LVBench and VideoMME-Long, demonstrate that AVA achieves state-of-the-art performance, attaining 62.3% and 64.1% accuracy, respectively, significantly surpassing existing VLM and video Retrieval-Augmented Generation (RAG) systems. Furthermore, to evaluate video analytics in ultra-long and open-world video scenarios, we introduce a new benchmark, AVA-100. This benchmark comprises 8 videos, each exceeding 10 hours in duration, along with 120 manually annotated, diverse, and complex question-answer pairs. On AVA-100, AVA achieves top-tier performance with an accuracy of 75.8%.

The source code of AVA is available at <https://github.com/I-ESC/Project-Ava>. The AVA-100 benchmark could be accessed at <https://huggingface.co/datasets/iesc/Ava-100>.

## [Remembrall: Leaning into Memory for Accurate Video Analytics on System-on-Chip GPUs](/conference/nsdi26/presentation/ramanujam)

Murali Ramanujam, Yinwei Dai, Kyle Jamieson, and Ravi Netravali, *Princeton University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/ramanujam)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/ramanujam)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/ramanujam)

Continually retraining models has emerged as a primary technique to enable high-accuracy video analytics on edge devices. Yet, existing systems employ such adaptation by relying on the spare compute resources that traditional (memory-constrained) edge servers afford. In contrast, mobile edge devices such as drones and dashcams offer a fundamentally different resource profile: weak(er) compute with abundant unified memory pools. We present Remembrall, a continuous learning system for the mobile edge's System-on-Chip GPUs. Our driving insight is that visually distinct scenes that require retraining exhibit substantial overlap in model embeddings; if captured into a base model on device memory, specializing to each new scene can become lightweight, requiring very few samples. To practically realize this approach, Remembrall presents new, compute-efficient techniques to (1) select high-utility data samples for retraining specialized models, (2) update the base model without complete retraining, and (3) time-share compute resources between retraining and live inference for maximal accuracy. Across diverse workloads, Remembrall lowers retraining costs by 2.8-10× compared to existing systems, resulting in 18-45% higher accuracies.

## [Themis: Scheduling-Aware Buffer Management for HBM-Based Hybrid Buffers](/conference/nsdi26/presentation/zhang-zhiyu)

Zhiyu Zhang, Minkun Xue, Kan Yu, Ruyi Yao, Shili Chen, and Hao Mei, *Fudan University;* Zixuan Chen, *China Telecom;* Weiyi Chen, Yibo Fan, and Yang Xu, *Fudan University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhang-zhiyu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhang-zhiyu)

Packet buffers are critical for absorbing congestion and sustaining throughput in high-speed routers. As link rates escalate, on-chip SRAM alone can no longer provide sufficient capacity. To address this, modern routers widely adopt hybrid buffer architectures that augment limited on-chip SRAM with large off-chip DRAM. Despite this architectural promise, existing hybrid Buffer Management (BM) schemes severely undermine router performance. They simply redirect packets that would otherwise be dropped into DRAM, which leads to priority inversion and head-of-line blocking: as packets buffered in DRAM age into the highest-priority packets, SRAM must stall until they are retrieved, wasting bandwidth and degrading throughput. Worse still, existing BM schemes ignore DRAM's access characteristics, further constraining its limited bandwidth and reducing overall performance dramatically.

We present Themis, a hybrid buffer management scheme that fully exploits SRAM's high bandwidth and DRAM's large capacity. Its core principle is scheduling-aware packet placement, which ensures packets with the earliest departure time are preferentially stored in SRAM to maximize its bandwidth utilization. To achieve this, Themis proactively migrates buffered packets between SRAM and DRAM, reserving SRAM space for imminent, high-priority traffic. Themis is compatible with diverse scheduling algorithms and supports dynamic changes to the scheduling policy. It also organizes DRAM storage according to scheduling order, mapping consecutively departing packets to contiguous addresses. This unlocks effective off-chip bandwidth, and accelerates packet migration. Themis is hardware-friendly and its FPGA and ASIC prototypes achieve low overhead and high frequency. Large-scale simulations show that Themis improves end-to-end performance by up to 2.8×.

## [SmartNIC-Enabled Live Migration for Storage-Optimized VMs with PYROCUMULUS](/conference/nsdi26/presentation/zhao-jiechen)

Jiechen Zhao, *University of Toronto and Microsoft Research Asia;* Ran Shu, Lei Qu, Ziyue Yang, and Rui Ma, *Microsoft Research Asia;* Derek Chiou, *Microsoft and UT Austin;* Natalie Enright Jerger, *University of Toronto;* Peng Cheng and Yongqiang Xiong, *Microsoft Research Asia*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhao-jiechen)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhao-jiechen)

Cloud providers offer storage-optimized VMs equipped with locally attached storage to meet the high performance requirements of cloud users. Live migration (LM) is crucial for such VMs to improve availability and manageability. However, providers do not enable LM for storage-optimized VMs. Host-managed LM suffers from high resource overheads and varied user performance, while offloading LM to SoC SmartNICs or disks cannot reliably accomplish LM in a reasonable time. The fundamental challenges are (1) consistency, demanding a high resource budget, and (2) network contention, preventing LM from converging. We propose *Pyrocumulus*, an LM approach on FPGA SmartNICs, enabling SLA-aware, fast, and low-overhead LM for storage-optimized VMs. We exploit hardware customizability and efficient network accessibility of the FPGA SmartNIC with LM protocol, architecture, and algorithm designs. Results from our FPGA SmartNIC prototype show that *Pyrocumulus* reduces user latency variances during LM up to 12.4×, lowers LM time by up to 19.6×, and saves cost up to 3×, while only taking 0.9%/3.8% compute/memory overhead of a mid-end FPGA SmartNIC.

### 10:20 am–10:50 am

## Coffee and Tea Break

Grand Pre-Function Area

### 10:50 am–12:30 pm

Track 1

## Neurons Meet Routers

Session Chair: Hong Xu, *The Chinese University of Hong Kong*

Grand Ballroom I–VI

## [Uber's Failover Architecture: Reconciling Reliability and Efficiency in Hyperscale Microservice Infrastructure](/conference/nsdi26/presentation/bansal)

Mayank Bansal, Milind Chabbi, Kenneth Bøgh, Srikanth Prodduturi, Kevin Xu, Amit Kumar, David Bell, Ranjib Dey, Yufei Ren, Sachin Sharma, Juan Marcano, Shriniket Kale, and Subhav Pradhan, *Uber Technologies;* Ivan Beschastnikh, *University of British Columbia;* Miguel Covarrubias, Chien-Chih Liao, Sandeep Koushik Sheshadri, Wen Luo, Kai Song, Ashish Samant, Sahil Rihan, Nimish Sheth, Albert Greenberg, and Uday Kiran Medisetty, *Uber Technologies*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/bansal)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/bansal)

Operating a global, real-time platform at Uber’s scale requires infrastructure that is both resilient and cost-efficient. Historically, reliability was ensured through a costly 2× capacity model—each service provisioned to handle global traffic independently across two regions—leaving half the fleet idle. We present Uber’s Failover Architecture (UFA), which replaces the uniform 2× model with a differentiated architecture aligned to business criticality. Critical services retain failover guarantees, while non-critical services opportunistically use failover buffer capacity reserved for critical services during steady state. During rare “full-peak” failovers, non-critical services are selectively preempted and rapidly restored, with differentiated Service-Level Agreements (SLAs) using on-demand capacity. Automated safeguards, including dependency analysis and regression gates, ensure critical services continue to function even while non-critical services are unavailable. The quantitative impact is significant: UFA reduces steady-state provisioning from 2× to 1.3×, raising utilization from 20% toward 30% while sustaining 99.97% availability. To date, UFA has hardened over 4,000 unsafe dependencies, eliminated 575K CPU cores, and projected to reduce over one million cores from a baseline of about 4 million cores.

## [SYMPHONY: Enabling Compute-Memory Disaggregation in LLM Serving Systems](/conference/nsdi26/presentation/agarwal)

Saurabh Agarwal and Bodun Hu, *UT-Austin;* Anyong Mao, *UW-Madison;* Aditya Akella, *UT-Austin;* Shivaram Venkataraman, *UW-Madison*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/agarwal)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/agarwal)

Large Language Models (LLMs) power AI applications such as chatbots and agents, which maintain conversational state across multiple turns. Serving these workloads is inherently stateful: each request generates a KV cache storing token-level state. Existing systems either recompute caches or offload them to host memory—both approaches incur high latency, cause load imbalance, and limit scalability. We present SYMPHONY, a disaggregated memory management layer that decouples compute from KV cache storage while meeting strict latency requirements. To enable disaggregation, SYMPHONY employs advisory requests—prefetching hints derived from user interactions or workload structure—to move caches off the critical path and enable fine-grained, request-level load balancing. Since these predictive signals are often unreliable, SYMPHONY introduces two key techniques: priority-based KV cache management, which allocates memory based on neural network structure and request priority, and cooperative memory management, which dynamically coordinates GPU memory with the serving framework. Evaluations on LLaMA models with ShareGPT and Burst-GPT workloads show that SYMPHONY reduces end-to-end latency by 2.4× over vLLM and serves 4× more requests with minimal latency increase.

## [Defending against Traffic Analysis Attacks with Flexible In-Network Obfuscation](/conference/nsdi26/presentation/xie-guorui)

Guorui Xie and Qing Li, *Pengcheng Laboratory;* Zhenning Shi, *Tsinghua Shenzhen International Graduate School;* Gianni Antichi, *Politecnico di Milano;* Yijia Zhu, *Xidian University;* Kejun Li and Changxing Weng, *Pengcheng Laboratory;* Sebastiano Miano, *Politecnico di Milano;* Yong Jiang, *Tsinghua Shenzhen International Graduate School and Pengcheng Laboratory;* Mingwei Xu, *Tsinghua University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/xie-guorui)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/xie-guorui)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/xie-guorui)

Traffic analysis attacks can exploit side channels in encrypted traffic (e.g., packet sizes) to infer user activities. Existing defenses provide weak protection, impose excessive bandwidth overhead, or require hard-to-deploy coordination. We present Securitas, a novel network traffic obfuscation framework that protects from side-channel attacks using a learning-guided mix of packet fragmentation and insertion. We implemented Securitas on a number of different data planes: Tofino switch, AMD/Xilinx FPGA, eBPF, and BMv2. Experiments show that Securitas reduces attack accuracy by up to 95.89%, while consuming 42.69× less bandwidth than prior defenses. Real-world Internet tests confirm minimal performance impact, e.g., adding 0.15s to the web page load.

## [ForestColl: Throughput-Optimal Collective Communications on Heterogeneous Network Fabrics](/conference/nsdi26/presentation/zhao-liangyu)

Liangyu Zhao, *University of Washington;* Saeed Maleki, *Independent Researcher;* Yuanhong Wang, *Tsinghua University;* Zezhou Wang, *University of Washington;* Ziyue Yang, *Microsoft Research;* Hossein Pourreza, *Microsoft;* Arvind Krishnamurthy, *University of Washington*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhao-liangyu)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/zhao-liangyu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhao-liangyu)

As modern DNN models grow ever larger, collective communications between the accelerators (allreduce, etc.) emerge as a significant performance bottleneck. Designing efficient communication schedules is challenging, given today's heterogeneous and diverse network fabrics. We present ForestColl, a tool that generates throughput-optimal schedules for any network topology. ForestColl constructs broadcast/aggregation spanning trees as the communication schedule, achieving theoretical optimality. Its schedule generation runs in polynomial time and is highly scalable. ForestColl supports any network fabric, including both switching fabrics and direct accelerator connections. We evaluated ForestColl on AMD MI250 and NVIDIA DGX A100 & H100 clusters. ForestColl shows significant improvements over the vendors' own optimized communication libraries across various settings and in LLM training. ForestColl also outperforms other state-of-the-art schedule generation techniques with both more efficient generated schedules and substantially faster generation speed.

## [Matryoshka: Realizing Hyperscale Data Center Network Design for the AI Era](/conference/nsdi26/presentation/cai)

Yan Cai, *Meta;* Jialong Li, *Max Planck Institute for Informatics;* Kutalmis Akpinar, Tianxiang Li, Hany Morsy, Jason Wilson, and Sunil Khaunte, *Meta;* Yiting Xia, *Max Planck Institute for Informatics;* Ying Zhang, *Meta*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/cai)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/cai)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/cai)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/cai)

Over the past decade, data center networking (DCN) has undergone substantial transformation in terms of both scale and complexity. Developing a DCN entails multiple intricate steps, such as establishing physical connections, configuring logical network addressing, and defining high-level routing policies. While extensive work has focused on logical DCN design and physical deployment, a critical gap remains: materializing these designs into concrete switch configurations—a necessary step to realize the development procedure. This problem is especially acute in the AI era, as hyperscale, rapidly evolving, and highly heterogeneous AI-driven clusters place unprecedented demands on DCN design and implementation.

This paper presents Matryoshka, Meta’s production-scale DCN design system that bridges this gap. Matryoshka employs an intent-based, model-driven approach to systematically compile high-level DCN design intents into working switch configurations. Operational for over six years, Matryoshka has supported orders-of-magnitude growth in Meta’s DCN infrastructure, guiding the design nearly 900 DCNs across 18 distinct types, including the latest 100K-GPU supercluster for AI training. We share our experience in building and operating Matryoshka, highlighting how it empowers the rapid design and evolution of AI clusters nowadays.

Track 2

## Self-Managing Networks

Session Chair: Arpit Gupta, *University of California, Santa Barbara*

Grand Ballroom VII–IX

## [PlanetServe: A Decentralized, Scalable, and Privacy-Preserving Overlay for Democratizing Large Language Model Serving](/conference/nsdi26/presentation/fang)

Fei Fang, Yifan Hua, Shengze Wang, Ruilin Zhou, Yi Liu, and Chen Qian, *University of California, Santa Cruz;* Xiaoxue Zhang, *University of Nevada, Reno*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/fang)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/fang)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/fang)

While significant progress has been made in research and development on open-source and cost-efficient large-language models (LLMs), serving scalability remains a critical challenge, particularly for small organizations and individuals seeking to deploy and test their LLM innovations. Inspired by peer-to-peer networks that leverage decentralized overlay nodes to increase throughput and availability, we propose PlanetServe, an LLM serving overlay that harnesses computing resources from decentralized contributors. We identify four key research problems inherent to enabling such a decentralized infrastructure: 1) overlay network organization; 2) LLM communication privacy; 3) overlay forwarding for resource efficiency; and 4) verification of serving quality. This work presents the first systematic study of these fundamental problems in the context of decentralized LLM serving. Evaluation results from a prototype implemented on a set of decentralized nodes demonstrate that PlanetServe achieves a latency reduction of over 50% compared to the baseline design without overlay forwarding. Furthermore, the security features introduce minimal overhead to serving latency and throughput. We believe this work pioneers a new direction for democratizing and scaling future AI serving capabilities.

## [MoCE: A Mixture-of-Context Aware Experts Framework for Troubleshooting Internet-scale Services](/conference/nsdi26/presentation/harsh)

Vipul Harsh, *Conviva and Carnegie Mellon University;* Sayan Sinha, *Conviva and Georgia Tech;* Henry Milner, *Conviva;* B. Aditya Prakash, *Conviva and Georgia Tech;* Vyas Sekar and Hui Zhang, *Conviva and Carnegie Mellon University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/harsh)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/harsh)

Modern Internet-scale services need to rapidly identify root causes of customer impacting incidents and remediate them. While there are many algorithms (including LLM-assisted solutions) for root cause analysis, these have significant limitations in terms of *coverage*, *extensibility*, and *scalability* due to the diversity of incidents that can occur at Internet-scale and the complexity of telemetry analysis. We argue the need for a paradigm shift in root cause analysis to depart from algorithm development to a systems approach.

To this end, we introduce a *mixture of context-aware experts* framework where each “expert” represents a root-cause hypothesis exploration. To enable rapid development of new experts and allow computational reuse across the ensemble for scalability, we design an abstraction that allows us to express an expert as a dataflow DAG combining relational, stateful and statistical operations. To ensure scalability and extensibility, we develop a *lazy* DAG runtime system that lazily schedules execution of DAG nodes. We implement this idea in MoCE and demonstrate its value using a mix of real-world incident data from four large application analytics providers and synthetically generated incidents. We show many existing and novel approaches can be expressed succinctly in our framework. We find that MoCE achieves high RCA accuracy (\>95%) across diverse incidents compared to 34% for the closest single expert (including prior works) achieving high coverage. We also show the value of the mixture paradigm and the lazy DAG runtime using controlled experiments.

## [Heuristic Analysis from Source Code via Symbolic-Guided Optimization](/conference/nsdi26/presentation/karimi)

Pantea Karimi, *MIT;* Siva Kesava Reddy Kakarla and Ryan Beckett, *Microsoft Research;* Santiago Segarra, *Rice University;* Pooria Namyar, *Microsoft Research;* Mohammad Alizadeh, *MIT;* Behnaz Arzani, *Microsoft Research*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/karimi)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/karimi)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/karimi)

Large-scale systems rely on heuristics to tackle NP-hard problems such as traffic engineering, virtual machine placement, and packet scheduling. While these heuristics are efficient, they can exhibit severe performance gaps under certain workloads, which leads to outages or costly over-provisioning. This risk has motivated tools that attempt to find inputs that cause worst-case underperformance. But, to use these tools in practice, heuristic developers need to rewrite heuristics as formal mathematical models—a process that is time-consuming, error-prone, and excludes many real-world algorithms.

We introduce MetaEase, a practical general-domain analyzer that directly analyzes a heuristic’s source code and eliminates the need for formal modeling. MetaEase combines code-aware input generation with guided search to uncover worst-case scenarios efficiently, even for heuristics with randomness (e.g., various traffic engineering schemes) or non-convex behavior (e.g., bin packing for virtual machine placement).

In most cases, across five problem domains, and eight heuristics, MetaEase matched or exceeded MetaOpt, a state-of-the-art optimization-based heuristic analyzer; in the remainder, it remained competitive and often ran faster. Against black-box optimization baselines, it won in 88% of settings and ranked in the top two otherwise. MetaEase analyzed Arrow, a recent networking heuristic that none of the state-of-the-art heuristic analyzers can analyze. We revealed previously unknown performance gaps in Arrow.

## [CCEval: Accurately and Confidently Evaluating Performance Metrics of Congestion Control Algorithms for Datacenter Networks](/conference/nsdi26/presentation/liu-tianfeng)

Tianfeng Liu, Kaihui Gao, and Li Chen, *Zhongguancun Laboratory;* Dan Li, *Tsinghua University;* Jin Guang and Xinyun Chen, *The Chinese University of Hong Kong, Shenzhen;* Vincent Liu, *University of Pennsylvania;* Zhiyong Chen and Yiwei Zhang, *Tsinghua University;* Ni Jin, *Zhongguancun Laboratory and Beijing University of Posts and Telecommunications;* Ran Zhang, *Zhongguancun Laboratory*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/liu-tianfeng)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/liu-tianfeng)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/liu-tianfeng)

Congestion control in datacenter networks (DCNs) is a highly active research area. Typical CCA evaluation workflows contain three steps: generate experimental configurations, execute the experiments, and estimate performance metrics using results from multiple trials. However, due to variability brought by random traffic workloads and single-digit trial counts, common experimental methodologies fail to provide enough confidence to properly evaluate CCA performance.

We propose CCEval, an evaluation framework for accurately and confidently estimating performance metrics of CCAs in DCNs. The key idea is using *confidence intervals* and more trials to quantify and improve the accuracy and confidence of performance metrics. To this end, we propose a model-free estimation algorithm to calculate the confidence intervals and forecast the required trial count for a given accuracy, confidence level, metric, and CCA. We further design a model-based tail quantile estimation algorithm to reduce the needed trial counts significantly without losing accuracy and confidence. Extensive experiments on simulators and real-world testbeds with four CCAs on typical topologies and flow distributions show that CCEval can produce estimations of performance metrics accurately and confidently, with 1% relative margin of error and 95% confidence level, and can reduce trial counts by 75%~80% for tail quantile estimation.

## [Predict, Prune, Play: Efficient Video Playback Optimization Under Device Diversity and Drift](/conference/nsdi26/presentation/sharma)

Harsha Sharma, *Massachusetts Institute of Technology and Amazon;* Pouya Hamadanian and Arash Nasr-Esfahany, *Massachusetts Institute of Technology;* Zahaib Akhtar, *Amazon and North Carolina State University;* Mohammad Alizadeh, *Massachusetts Institute of Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/sharma)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/sharma)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/sharma)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/sharma)

Video-streaming platforms tune dozens of playback parameters across thousands of client devices. Our measurements from Amazon Prime Video show that device-specific tuning can enhance stream quality. Yet traditional tuning techniques like Bayesian optimization become prohibitively expensive due to the large configuration space and the constant emergence of new device types.

We introduce AZEEM, a scalable recommendation system leveraging *few-shot prediction* to rapidly identify promising configurations for new devices. The key insight behind AZEEM is that devices exhibit performance similarities that enable predictions from limited observations. Trained on offline data of device-playback configuration interactions, AZEEM efficiently narrows down the search space to a small set of configurations likely to contain optimal or near-optimal candidates. Additionally, AZEEM addresses temporal distribution shift—where the best-performing configurations change over time—by recommending a small, robust set of candidates rather than a single configuration. Evaluations using large-scale real-world datasets show that AZEEM reduces exploration cost by 5.8−13.6× and improves stream quality compared to state-of-the-art Bayesian optimization and multi-armed bandit approaches, enabling effective device-specific optimization at scale. We deploy AZEEM on a subset of Amazon Prime Video’s production traffic, where it achieved a relative QoE improvement of 2.7% on average and 10.6% at the 90th percentile over an existing treatment tuning system.

Track 3

## Security in Networked Systems

Session Chair: Vasiliki Kalavri, *Boston University*

Bellevue Room

## [Over-Threshold Multiparty Private Set Intersection for Collaborative Network Intrusion Detection](/conference/nsdi26/presentation/arpaci)

Onur Eren Arpaci, Raouf Boutaba, and Florian Kerschbaum, *University of Waterloo*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/arpaci)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/arpaci)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/arpaci)

An important function of collaborative network intrusion detection is to analyze the network logs of the collaborators for joint IP addresses. However, sharing IP addresses in plain is sensitive and may be even subject to privacy legislation as it is personally identifiable information. In this paper, we present the privacy-preserving collection of IP addresses. We propose a single collector, over-threshold private set intersection protocol. In this protocol N participants identify the IP addresses that appear in at least t participant's sets without revealing any information about other IP addresses. Using a novel hashing scheme, we reduce the computational complexity of the previous state-of-the-art solution from O(M(N logM/t)^(2t)) to O(t²M(binomNt)), where M denotes the dataset size. This reduction makes it practically feasible to apply our protocol to real network logs. We test our protocol using joint networks logs of multiple institutions. Additionally, we present two deployment options: a collusion-safe deployment, which provides stronger security guarantees at the cost of increased communication overhead, and a non-interactive deployment, which assumes a non-colluding collector but offers significantly lower communication costs and applicable to many use cases of collaborative network intrusion detection similar to ours.

## [Secure Vickrey Auctions for Online Advertising](/conference/nsdi26/presentation/bhatnagar)

Archit Bhatnagar, *University of Michigan;* Yunming Xiao, *The Chinese University of Hong Kong, Shenzhen;* Ang Chen and Amrita Roy Chowdhury, *University of Michigan*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/bhatnagar)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/bhatnagar)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/bhatnagar)

Online advertising is an essential part of the web ecosystem. When a user’s browser lands on a webpage, advertisers bid for the ad space. An auction algorithm (e.g., Vickrey/second-price auction) is executed to determine the winner and the price; ideally, only this information is revealed, and everything else (i.e., the losing bids and the bidder identities) is kept private. However, achieving these privacy goals under a malicious security model, while operating under stringent performance requirements for online advertising, is challenging.

Obsidian enables secure Vickrey auctions for online advertising with three ideas: a new Multiparty Computation (MPC)-friendly encoding scheme that decouples bid values from bidders’ identities; a novel use of function secret sharing to shift the cost of encoding validation to an offline phase; and a lightweight ring signature scheme to anonymously verify bidders. Obsidian outperforms generic MPC and homomorphic encryption approaches by orders of magnitude. Moreover, it also surpasses the state-of-the-art system, Addax, which is tailored to ad auctions under a weaker (covert) threat model and leaks more information.

## [EZ-SAVE: Evaluation of Easy-to-Deploy Source Address Validation Policies](/conference/nsdi26/presentation/scaglione)

Nicholas Scaglione and Justin Furuness, *University of Connecticut;* Yossi Gilad, *Hebrew University of Jerusalem;* Hemi Leibowitz, *The College of Management Academic Studies;* Cameron Morris and Bing Wang, *University of Connecticut;* Kotikalapudi Sriram, *National Institute of Standards and Technology (NIST);* Amir Herzberg, *University of Connecticut*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/scaglione)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/scaglione)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/scaglione)

The lack of Source Address Validation (SAV) is a significant vulnerability of the Internet, which is abused in many Denial-of-Service (DoS) and other attacks. Several IETF RFCs define *easy-to-deploy, non-interactive SAV designs*; the IETF is currently developing another SAV mechanism, BAR-SAV, which, as its name suggests, uses *B*GP, *A*SPA (Autonomous System Provider Authorization), and *R*OA (Route Origin Authorization) data. However, no comparative evaluation of the potential impact of their large-scale deployment has been done. A recent survey of network vendors and operators indicates that more efficacy data and usage guidelines are necessary to motivate their adoption.

We present *EZ-SAVE*, the first simulation-based analysis evaluating easy-to-deploy SAV policies. We measure both the spoofed traffic detection rates and the legitimate traffic filtering (false-positive) rates for each standard and proposed design at different adoption rates, using a realistic Internet topology and traffic engineering policies. Our results reveal several significant insights that may assist and guide the standardization process as well as developers and operators. In particular, we find that BAR-SAV proves to be the most effective design that features high spoof detection rates and low (or even zero) false-positive rates, motivating its standardization and deployment. Our results also provide operators with guidance on other SAV mechanisms that are effective for specific scenarios. In addition, our results highlight the importance of using realistic export policies for SAV evaluation.

## [cc-pipe: Breaking Systemic Bottlenecks in RPKI Data Supply Chain with Concurrent and Conflict-Free Pipelines](/conference/nsdi26/presentation/yu)

Chenhui Yu, *Computer Network Information Center, Chinese Academy of Sciences; School of Computer Science and Technology, University of Chinese Academy of Sciences;* Yanbiao Li, *Computer Network Information Center, Chinese Academy of Sciences; School of Computer Science and Technology, University of Chinese Academy of Sciences; Hangzhou Institute for Advanced Study, University of Chinese Academy of Sciences;* Hui Zou, Yuxuan Chen, Shiyi Liu, and Gaogang Xie, *Computer Network Information Center, Chinese Academy of Sciences; School of Computer Science and Technology, University of Chinese Academy of Sciences*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/yu)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/yu)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/yu)

While the Resource Public Key Infrastructure (RPKI) is essential for securing BGP, the high latency, limited scalability, and vulnerabilities in the data supply chain severely undermine its security guarantees and impede network operations. Within this supply chain, existing research identifies the Relying Party (RP) validation process as the primary performance bottleneck. This bottleneck originates from the standard monolithic architecture, which enforces strong consistency but incurs high latency. Previous work has pursued incremental optimizations within this architecture, yet achieving substantial gains remains difficult.

Based on extensive measurements, we identify inherent blocking within the paradigm as the root cause. To address this, we propose cc-pipe, a novel pipeline architecture that breaks the fundamental consistency—latency trade-off. By leveraging a predictive conflict graph, cc-pipe enables low-latency incremental data dissemination while preserving strong consistency guarantees. Evaluation with real-world deployment demonstrates that cc-pipe reduces average latency by up to 73.3% across all data with negligible router overhead. It also delivers significant scalability under projected future workloads, as well as robust resilience to misbehaving publication points.

## [A Systematic Threat Analysis and Practical Attacks on Automated Frequency Coordination Systems](/conference/nsdi26/presentation/dong)

Yilu Dong and Tianchang Yang, *The Pennsylvania State University;* Arupjyoti Bhuyan, *Idaho National Laboratory;* Syed Rafiul Hussain, *The Pennsylvania State University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/dong)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/dong)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/dong)

The 6 GHz band, traditionally reserved for mission-critical incumbent systems such as public safety communications, utility infrastructure, and fixed satellite services, has recently been opened for Wi-Fi devices. This expansion introduces a critical coexistence challenge of ensuring that unlicensed Wi-Fi Access Points (APs) do not interfere with incumbent operations. To manage this risk, regulators mandated the use of Automated Frequency Coordination (AFC) systems that assign spectrum access to Wi-Fi APs based on their locations. In this work, we present the first systematic security analysis of AFC systems. In particular, we analyze the trust assumptions of AFC systems and uncover design lapses and deployment mishaps in this model. Our analysis reveals that the AFC's dependence on unauthenticated data sources, including GNSS/GPS and Wi-Fi-based localization (for location), DNS (for service discovery), and NTP (for time synchronization), creates practical off-path attack vectors that allow adversaries to manipulate control-plane parameters without breaking cryptographic protections between APs and AFC servers. For example, using inexpensive, off-the-shelf software-defined radios, an off-path adversary can spoof the GPS signals received by an AP, falsifying its reported location to either disable 6 GHz transmissions or cause harmful interference with incumbent services. We validate these vectors empirically on commercial APs from four major vendors and evaluate four commercial and one open-source AFC servers to measure real-world impact. We also propose potential mitigations and analyze the trade-offs between usability and security to formulate our recommendations to harden AFC deployments and 6 GHz APs.

### 12:30 pm–2:00 pm

## Lunch (on your own)

### 2:00 pm–3:20 pm

Track 1

## Designing Robust Networked Systems

Session Chair: Behnaz Arzani, *Microsoft*

Grand Ballroom I–VI

## [Mortise: Auto-tuning Congestion Control to Optimize QoE via Network-Aware Parameter Optimization](/conference/nsdi26/presentation/shen-yixin)

Yixin Shen, *Tsinghua University, Bytedance Inc., and Zhongguancun Laboratory;* Ruihua Chen, *Tsinghua University;* Bo Wang, *Tsinghua University and Zhongguancun Laboratory;* Jing Chen, Haochen Zhang, and Minhu Wang, *Tsinghua University;* Yan Liu, *Bytedance Inc.;* Mingwei Xu, *Tsinghua University and Zhongguancun Laboratory;* Zili Meng, *Hong Kong University of Science and Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/shen-yixin)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/shen-yixin)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/shen-yixin)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/shen-yixin)

Congestion control algorithms (CCAs) critically shape the tradeoff among throughput, latency, and loss, directly impacting user Quality of Experience (QoE).  
However, most existing CCAs use static, heuristically chosen parameter settings that fail to adapt to dynamic network states, resulting in suboptimal QoE. Our key observation is that the optimal CCA parameter configuration depends on real-time network states.  
To bridge this gap, we propose Mortise, a real-time, network-aware adaptation framework that dynamically tunes rule-based CCA parameters to maximize QoE.  
To address the challenges in modeling the complex parameter-QoE relationship, Mortise introduces a QoS tradeoff proxy to decompose parameter optimization into two steps: it first infers the application's preferred QoS tradeoff from real-time QoE gradients and then derives the corresponding parameter settings via control-theoretic analysis.  
Implemented atop TCP and evaluated in both emulated and production environments, Mortise outperforms state-of-the-art solutions, enhancing the QoE of file downloading service by up to 73% and QoE of video streaming service by up to 167% in real-world scenarios, with minimal deployment overhead.

## [Harvesting Spare CPU Resources in Container Systems](/conference/nsdi26/presentation/hall)

Adam Hall and Anirudh Sarma, *Georgia Institute of Technology;* Esha Choukse, *Microsoft Azure Research;* Umakishore Ramachandran, *Georgia Institute of Technology;* Sameh Elnikety, *Microsoft Research*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/hall)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/hall)

Platforms like Kubernetes are widely adopted for deploying latency-sensitive cloud services in containers, and CPU resources for these containers are over-provisioned to ensure low 99th percentile tail latency under peak load. At the same time, cloud services exhibit bursty traffic patterns resulting in CPU usage variability that creates opportunity to harvest ephemerally unused CPU cores to run latency-tolerant containers. However, existing resource controls do not allow latency-sensitive containers to share unused cores without compromising their low tail latency objectives. Prior research on performance isolation is inadequate for container systems because it requires modifying applications and system software, employs offline profiling, and does not account for interference from processing container networking interrupts. We present *HarvestContainers*, a system that protects latency-sensitive containers from all sources of interference while harvesting their spare CPU cores to run latency-tolerant containers. Our solution dynamically determines the safe number of CPU cores to harvest and does not require rewriting applications or OS. We implement *HarvestContainers* integrated with Kubernetes and evaluate it experimentally. Our evaluation shows that latency-sensitive containers with microsecond-scale service level objectives can share up to 75% of their unused CPU cores while maintaining tail latency within 4% of standalone operation.

## [Fractal: Fault-Tolerant Shell-Script Distribution](/conference/nsdi26/presentation/huang)

Zhicheng Huang, Ramiz Dundar, and Yizheng Xie, *Brown University;* Konstantinos Kallas, *University of California, Los Angeles;* Nikos Vasilakis, *Brown University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/huang)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/huang)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/huang)

This paper presents FRACTAL, a new system that offers fault tolerant distributed shell script execution for unmodified scripts. FRACTAL first distinguishes recoverable regions from side-effectful ones, and augments them with additional runtime support aimed at fault recovery. It employs precise dependency and progress tracking at the subgraph level to offer sound and efficient fault recovery. It minimizes the number of upstream regions that are re-executed during recovery and ensures exactly-once semantics upon recovery for downstream regions. Evaluation on 4- and 30-node clusters indicates average fault-free speedups of (1) \>9.6x over Bash, a single-node shell-interpreter baseline, (2) \>5.5x over Hadoop Streaming, a MapReduce system that supports language-agnostic third-party components, and (3) 17% over DiSh, a state-of-the-art fault-intolerant shell-script distribution system—all while recovering 7.8–16.4x faster than Hadoop Streaming in cases of faults.

## [eXpressSFU: Toward Super-Scalable Video Conferencing with SmartNICs](/conference/nsdi26/presentation/tran)

Tuan Tran and S. M. H. Hosseini, *University of Colorado Boulder;* Seyeon Kim, *Korea University;* Kyunghan Lee, *Seoul National University;* Nam Bui, *University of Colorado Denver;* Dirk Grunwald and Sangtae Ha, *University of Colorado Boulder*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/tran)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/tran)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/tran)

Video conferencing has emerged as a critical Internet application. Unlike video-on-demand services, high-quality video conferencing necessitates minimal latency, as media streams are generated, transmitted, processed, forwarded and received in real time. Our empirical analysis reveals that processing latency at the media server, particularly Selective Forwarding Units (SFUs), is the dominant barrier to scalability. Notably, cryptography, memory, and I/O operations account for approximately 79% of the media packet processing latency.

In this paper, we introduce *eXpressSFU*, a re-architected video conferencing system designed to significantly enhance scalability for large-scale and high-quality video conferences. By decoupling the fast-control and data planes from the slow-control plane, *eXpressSFU* accelerates the media packet processing pipeline through the use of emerging network technologies, such as Smart Network Interface Cards (SmartNICs). Experimental results show that our system reduces packet processing latency by a factor of 8. This improvement allows it to support 3× more concurrent users while cutting computational power consumption by up to 60%.

Track 2

## Hot Data, Cold Data

Session Chair: Danyang Zhuo, *Duke University*

Grand Ballroom VII–IX

## [ZipLLM: Efficient LLM Storage via Model-Aware Synergistic Data Deduplication and Compression](/conference/nsdi26/presentation/wang-zirui)

Zirui Wang, Tingfeng Lan, and Zhaoyuan Su, *University of Virginia;* Juncheng Yang, *Harvard University;* Yue Cheng, *University of Virginia*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-zirui)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-zirui)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/wang-zirui)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wang-zirui)

Modern model hubs, such as Hugging Face, store tens of petabytes of LLMs, with fine-tuned variants vastly outnumbering base models and dominating storage consumption. Existing storage reduction techniques—such as deduplication and compression—are either LLM-oblivious or not compatible with each other, limiting data reduction effectiveness.

Our large-scale characterization study across all publicly available Hugging Face LLM repositories reveals several key insights: (1) fine-tuned models within the same family exhibit highly structured, sparse parameter differences suitable for delta compression; (2) bitwise similarity enables LLM family clustering; and (3) tensor-level deduplication is better aligned with model storage workloads, achieving high data reduction with low metadata overhead. Building on these insights, we design BitX, an effective, fast, lossless delta compression algorithm that compresses the XORed difference between fine-tuned and base LLMs. We build ZipLLM, a model storage reduction pipeline that unifies tensor-level deduplication and lossless BitX compression. By synergizing deduplication and compression around LLM family clustering, ZipLLM reduces model storage consumption by 54%, over 20% higher than state-of-the-art deduplication and compression approaches.

## [Latency-Aware Caching with Delayed Hits: From Bursty Traffic to Pipeline Architectures](/conference/nsdi26/presentation/keren)

Nadav Keren, Gil Einziger, and Gabriel Scalosub, *Ben Gurion University of The Negev*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/keren)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/keren)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/keren)

Modern computing systems rely on caching to reduce access latency and optimize resource utilization. However, in heterogeneous storage and cloud environments, non-uniform access latencies across storage tiers, network locations, and intermediary caches undermine traditional caching. Moreover, modern cache algorithms that attempt to capture multiple access patterns, recency, frequency, and burstiness, often become complex and difficult to maintain.

As a key contribution, we propose an adaptive caching architecture that treats caching strategies as a pipeline of simple, orthogonal policies, each focused on a distinct access bias. This modular design is easier to expand, debug, and integrate, and it self-adjusts the memory resources allocated to each stage to optimize overall workload performance. New heuristics can be introduced dynamically without disrupting existing behaviors.

In addition, in latency-aware caching, one often encounters the phenomenon of delayed hits, where items not yet available in the cache are requested repeatedly. We introduce the Least Bursty Used (LBU) heuristic, which retains items exhibiting high burstiness even when they are neither recent nor frequent, thereby mitigating delayed hits that degrade request latency. We embed LBU within our pipeline and derive the Recency–Frequency–Burstiness (RFB) policy, which balances resources among recency, frequency, and burstiness. Evaluations on thirteen real-world storage traces from IBM, Twitter and Meta using latencies drawn from real-life deployments show that RFB reduces average request latency by 10% compared to the best state-of-the-art alternative, while maintaining consistent performance, with a low standard deviation across bursty and non-bursty workloads.

## [Cortex: Achieving Low-Latency, Cost-Efficient Remote Data Access For LLM via Semantic-Aware Knowledge Caching](/conference/nsdi26/presentation/ruan-cortex)

Chaoyi Ruan, *National University of Singapore;* Chao Bi, *University of Science and Technology of China;* Kaiwen Zheng, *University of Toronto;* Ziji Shi, *National University of Singapore;* Xinyi Wan, *Sea AI Lab and National University of Singapore;* Jialin Li, *National University of Singapore*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/ruan-cortex)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/ruan-cortex)

Large Language Model (LLM) agents tackle data-intensive tasks such as deep research and code generation. However, their effectiveness depends on frequent interactions with knowledge sources across remote clouds or regions. Such interactions can create non-trivial latency and cost bottlenecks. Existing caching solutions focus on exact-match queries, limiting their effectiveness for semantic knowledge reuse.

To address this challenge, we introduce Cortex, a novel cross-region knowledge caching architecture for LLM agents. At its core are two abstractions: *Semantic Element* (SE) and *Semantic Retrieval Index* (Seri). A semantic element captures the semantic embedding representation of an LLM query together with performance-aware metadata such as latency, cost, and staticity. Seri then provides two-stage retrieval: a vector similar index with semantic embedding for fast candidate selection and a lightweight LLM-powered *semantic judger* for precise validation. Atop these primitives, Cortex builds a new cache interface that includes a new semantic-aware cache hit definition, a cost-efficient eviction policy, and proactive prefetching. To reduce overhead, Cortex co-locates the small LLM judger with the main LLM using adaptive scheduling and resource sharing. Our evaluation demonstrates that Cortex delivers substantial performance improvements without compromising correctness. On representative search workloads, Cortex achieves up to a 3.6× increase in throughput by maintaining cache hit rates of over 85×, while preserving accuracy virtually identical to non-cached baselines. Cortex also improves throughput for coding tasks by 20×, showcasing its versatility across diverse agentic workloads.

## [Unleashing The Potential of Datacenter SSDs by Taming Performance Variability](/conference/nsdi26/presentation/chaudhry)

Gohar Irfan Chaudhry, *MIT CSAIL;* Ankit Bhardwaj, *Tufts University;* Zhenyuan (Zain) Ruan and Adam Belay, *MIT CSAIL*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/chaudhry)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/chaudhry)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/chaudhry)

Storage disaggregation is widely adopted in today's datacenters to improve disk utilization. However, efficiently disaggregating SSDs remains a challenge because of their high performance variability. This is due to differences in flash characteristics, such as wear and model version; read/write interference; and SSD-internal operations like garbage collection. Existing systems can only manage these types of variability in isolation. We propose Sandook, a rack-scale block storage system that instead holistically manages them together to unlock higher performance. Sandook achieves this through a logically centralized architecture that can integrate multiple scheduling policies and respond effectively at both short and long timescales. It adaptively steers I/O to the best available SSDs, using techniques that enable greater routing flexibility for both reads and writes. Sandook does not require any special storage or network hardware. Our evaluation demonstrates that Sandook is capable of delivering the full performance potential of SSDs. It achieves a 30%–82% raw I/O throughput improvement over existing systems that tackle a single source of performance variability while maintaining sub-millisecond tail latency. For unmodified applications sharing a pool of SSDs, Sandook achieves a 12–94% improvement in end-to-end performance.

Track 3

## Virtualization Revisited

Session Chair: Rodrigo Fonseca, *Microsoft Research*

Bellevue Room

## [Agentix: An Efficient Serving Engine for LLM Agents as General Programs](/conference/nsdi26/presentation/luo)

Michael Luo, *University of California, Berkeley, and Google DeepMind;* Xiaoxiang Shi, *Shanghai Jiao Tong University;* Colin Cai, Tianjun Zhang, Justin Wong, and Yichuan Wang, *University of California, Berkeley;* Chi Wang, Yanping Huang, and Zhifeng Chen, *Google DeepMind;* Joseph E. Gonzalez and Ion Stoica, *University of California, Berkeley*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/luo)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/luo)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/luo)

Large language model (LLM) applications are evolving beyond simple chatbots into dynamic, general-purpose agentic programs, which scale LLM calls and output tokens to help AI agents reason, explore, and solve complex tasks. However, existing LLM serving systems ignore dependencies between programs and calls, missing significant opportunities for optimization. Our analysis reveals that programs submitted to LLM serving engines experience long cumulative wait times, primarily due to head-of-line blocking at both the individual LLM request and the program.

To address this, we introduce Agentix, an LLM serving system that treats programs as first-class citizens to minimize their end-to-end latencies. Agentix intercepts LLM calls submitted by programs, enriching schedulers with program-level context. We propose two scheduling algorithms—for single-threaded and distributed programs—that preempt and prioritize LLM calls based on their programs' previously completed calls. Our evaluation demonstrates that across diverse LLMs and agentic workloads, Agentix improves throughput of programs by 4-15× at the same latency compared to state-of-the-art systems, such as vLLM.

## [Queue-Mem: Energy-Efficient Hardware Storage for Advanced Network Function Acceleration](/conference/nsdi26/presentation/scazzariello)

Mariano Scazzariello, *RISE Research Institutes of Sweden;* Tommaso Caiazzi, *Roma Tre University;* Hamid Ghasemirahni, Dejan Kostić, and Marco Chiesa, *KTH Royal Institute of Technology*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/scazzariello)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/scazzariello)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/scazzariello)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/scazzariello)

General-purpose CPU servers have been widely used to deploy Network Functions (NFs) thanks to their high flexibility and simplicity of deployment. Due to their high energy consumption, best practices advocate for only processing packet *headers* on CPU cores while temporary storing the corresponding packet *payloads* on either network interface cards or external RDMA-enabled memory.

We show that the seemingly minor decision of *where* to store a packet payload *greatly impacts* overall energy consumption in state-of-the-art NF systems operating at terabit-per-second speeds. In fact, we show that if one could *ideally* store packet payloads on today's *hardware switches*, while processing headers externally, one could reduce energy use by 1.8× to 10.9× compared to current practices.

In this paper, we introduce Queue-Mem, a general-purpose, energy-efficient storage solution to enhance NF deployment that is amenable for implementation with various existing hardware switches. Building Queue-Mem involves addressing significant challenges associated with payload storage, as hardware switches lack such functionality. By carefully exploiting the *buffer queues* of existing switches, we are the first ones to build and showcase a robust, energy-efficient packet processing pipeline capable of handling terabit-per-second speeds and supporting advanced per-flow network functions, all while using just a *single* commodity server connected to an ASIC switch.

## [Hierarchical Integration of WebAssembly in Serverless for Efficiency and Interoperability](/conference/nsdi26/presentation/baqershahi)

Mohammadamin Baqershahi, Changyuan Lin, and Visal Saosuo, *University of British Columbia;* Paul Chen, *Huawei Technologies Canada;* Mohammad Shahrad, *University of British Columbia*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/baqershahi)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/baqershahi)

Modern serverless systems suffer from low resource efficiency, which maps to high per-unit costs. This comes from the high isolation overhead (e.g., low resource sharing, slow startup, etc.), as well as resource wastage incurred by conservative resource scaling (e.g., keep-alive). Language runtimes such as WebAssembly (Wasm) can reduce isolation overhead without compromising security. Existing Wasm-based serverless approaches fall into one of these categories: supporting only Wasm workloads, failing to leverage existing capabilities of modern serverless and cloud platforms, or falling short of leveraging Wasm’s true potential. This work introduces a dense hierarchical architecture to securely co-locate Wasm-based applications from different customers within the same container sandbox. We show how this design preserves the container-based serving model, which allows leveraging existing platform capabilities and supporting non-Wasm-based workloads. Our system, Wasabi, leverages this architecture alongside resource-aware scaling, queuing, and overbooking to offer much higher density than state-of-the-art serverless systems with similar or better performance.

## [Mitigating CPU Frontend for Complex Data Plane Applications](/conference/nsdi26/presentation/dang)

Yihan Dang, Hao Li, Ze Xia, Jiajun Luan, and Peng Zhang, *Xi'an Jiaotong University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/dang)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/dang)

The functionality and requirement of modern networks are becoming increasingly complex, giving rise to Complex Data Plane Applications (CDPA) with rich semantics but often limited performance. However, many existing optimizations fail to improve the performance of CDPAs. This is because CDPAs usually come with excessively large code size, which is often two orders of magnitude larger than today's L1 instruction cache (I-cache) size, causing the CPU to frequently stall on accessing instructions, thus presenting a distinct performance profile that bounds on CPU frontend. This paper proposes NanoPL, an I-cache-friendly new execution model that shuffles the packet processing logic to efficiently mitigate CPU frontend for CDPAs. Stemming from the common execution pattern of CDPAs, NanoPL analyzes its code to ensure semantic consistency after shuffling. By collecting performance profile of CDPAs over underlying traffic, NanoPL partitions CDPAs into execution stages and conducts I-cache-friendly shuffling policy. Experiments show that NanoPL can achieve 17.2%~30.2% higher throughput over real world CDPAs due to the reduction of I-cache misses by up to 86.4%.

### 3:20 pm–3:50 pm

## Coffee and Tea Break

Grand Pre-Function Area

### 3:50 pm–5:30 pm

Track 1

## Cloud Systems, Shared and Scalable

Session Chair: Ahmed Saeed, *Georgia Institute of Technology*

Grand Ballroom I–VI

## [FAST: An Efficient Scheduler for All-to-All GPU Communication](/conference/nsdi26/presentation/lei-yiran)

Yiran Lei, *Carnegie Mellon University and MangoBoost;* Dongjoo Lee, *MangoBoost;* Liangyu Zhao, *University of Washington;* Daniar Kurniawan, Chanmyeong Kim, Heetaek Jeong, Changsu Kim, and Hyeonseong Choi, *MangoBoost;* Liangcheng Yu, *University of Pennsylvania;* Arvind Krishnamurthy, *University of Washington;* Justine Sherry, *Carnegie Mellon University;* Eriko Nurvitadhi, *MangoBoost*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/lei-yiran)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/lei-yiran)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/lei-yiran)

All-to-All(v) communication is a critical primitive in modern machine learning workloads, particularly mixture-of-experts (MoE) models. Unfortunately, efficient scheduling is challenging due to workload skew, heterogeneous two-tier fabrics, and incast congestion, compounded by the dynamic nature of MoE workloads, where traffic shifts every few hundred milliseconds. Existing schedulers are hardly scalable, incurring seconds to hours of synthesis time, making them impractical.

We present FAST, an efficient All-to-All(v) scheduler. FAST addresses skew through intra-server rebalancing and enforces balanced, one-to-one scale-out transfers that avoid incast. Evaluated extensively on both NVIDIA H200 and AMD MI300X clusters, FAST consistently outperforms state-of-the-art solutions on skewed workloads while reducing synthesis time by orders of magnitude.

## [HeteCCL: Synthesizing Near-Optimal Collective Communication Schedules for Heterogeneous GPU Clusters](/conference/nsdi26/presentation/hei)

Chenyang Hei, Fuliang Li, and Jiayi Li, *Northeastern University;* Jiamin Cao, *Alibaba Cloud;* Chengxi Gao, *Shenzhen Institutes of Advanced Technology, Chinese Academy of Sciences;* Xiuzhu Sha, Tongrui Liu, and Dengke Zhang, *Northeastern University;* Ennan Zhai, *Alibaba Cloud;* Xingwei Wang, *Northeastern University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/hei)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/hei)

Training large language models demands massive computing and networking resources. However, existing clusters often face shortages of homogeneous resources and vendor lock-in, forcing the use of heterogeneous hardware, which makes synchronizing training across nodes highly challenging. Current solutions to cluster heterogeneity suffer from low collective communication efficiency, with suboptimal scheduling and slow algorithm synthesis. We present HeteCCL, a unified method for generating near-optimal collective communication schedules on heterogeneous clusters. HeteCCL models the cluster topology and link bandwidth in detail, quantizes data chunks at the schedule-step level, and formulates the scheduling problem as a maximum parallel transfer problem on a weighted directed graph. To accelerate synthesis, HeteCCL encodes bandwidth and routing constraints as SMT formulas and applies counterexample-guided inductive synthesis to refine constraints and prune the search space iteratively. Experiments on heterogeneous testbeds, each consisting of 32 H20 and V100 GPUs, show that HeteCCL outperforms NCCL, TACCL, and TE-CCL, achieving up to 2.8×, 4.4×, and 2.6× higher bandwidth. It also accelerates synthesis by up to 2 orders of magnitude compared to state-of-the-art efforts, and improves end-to-end training efficiency by 23%–37%.

## [Medley: Optimizing Midgress Bandwidth for Commercial Live Streaming CDNs](/conference/nsdi26/presentation/wang-haiping)

Haiping Wang, *Fudan University and ByteDance;* Wanxin Shi, *Fudan University;* Sandesh Dhawaskar Sathyanarayana, Shu Shi, and Feng Qian, *ByteDance;* Yinghao Yang and La Zuo, *Fudan University and ByteDance;* Hebin Yu and Ruixiao Zhang, *ByteDance;* Ruoshi Sun, *Fudan University;* Yajie Peng, Xiaofei Pang, Ruili Fang, Zhenpeng Zhu, and Weiqi Chen, *ByteDance;* Yang Xu, *Fudan University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-haiping)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wang-haiping)

The rapid expansion of live streaming services in recent years has introduced new cost challenges for Content Delivery Networks (CDNs). Unlike conventional Video on Demand (VoD) streaming, where CDNs can utilize the off-peak hours to preload video content on edge nodes, live streaming requires real-time delivery across CDN nodes before reaching end users, significantly increasing midgress bandwidth costs for service providers. Characteristics such as real-time content generation and consumption, strict requirements for service quality, and systems that need to scale with diverse resources to support the increase in large-scale users, make it difficult to optimize live-streaming midgress traffic with traditional DNS-based and redirection-based methods.

At ByteDance, we have successfully implemented a substream-based CDN architecture to minimize midgress bandwidth for our commercial live streaming services. By dividing a video stream into multiple sub-streams and assigning each to a different edge node, the system can substantially reduce midgress traffic while adapting to the increasing scale of the system and live-stream users. We present Medley, a production-grade substream delivery system, and validate its efficacy through a large-scale, real-world deployment. Running on one of the largest live streaming platforms, Medley handled up to 0.85 million concurrent viewing requests per minute during peak hours. Our evaluations show that Medley reduces midgress costs by 76.83%, while maintaining consistent Quality of Experience (QoE).

## [Offloading Cloud Network Services at Production Scale with SONiC DASH SmartSwitch](/conference/nsdi26/presentation/wu-shaofeng)

Shaofeng Wu, *The Chinese University of Hong Kong and Microsoft Research Asia;* Zhixiong Niu, *Microsoft Research Asia;* Riff Jiang, Lawrence Lee, Junhua Zhai, Ze Gan, Vasundhara Volam, Prabhat Aravind, Prince Sunny, Prince George, Qi Luo, Evan Langlais, Soumya Tiwari, Venkat Satish Katta, Weixi Chen, Rishiraj Hazarika, Sachin Jain, Deven Jagasia, Michal Zygmunt, Avijit Gupta, Neeraj Motwani, and Pranjal Shrivastava, *Microsoft;* Qiang Su, *The Chinese University of Hong Kong;* Anil Reddy Pannala, Kristina Moore, James Grantham, Anupam Pandey, Xin Liu, Guohan Lu, Gerald De Grace, Rishabh Tewari, Lihua Yuan, Erica Lan, Deepak Bansal, and Dave Maltz, *Microsoft;* Yongqiang Xiong, *Microsoft Research Asia;* Hong Xu, *The Chinese University of Hong Kong*

***Community Award Winner!***

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wu-shaofeng)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/wu-shaofeng)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wu-shaofeng)

To support stateful cloud network services, Microsoft Azure has operated several generations of offloading solutions over the past decade. While these systems improved performance, operating them at hyperscale revealed three persistent lessons: (i) overly flexible programming models hinder hardware acceleration, (ii) appliance-style DPU pools inflate physical footprint and complicate deployment, and (iii) vendor-specific SDKs slow down service iteration.

We present SONiC DASH SmartSwitch that addresses these lessons with three key designs: (1) the DASH pipeline as an immutable and hardware-friendly programming model; (2) the uni-box SmartSwitch that converges NPU and DPU resources within a single T1 switch; and (3) a community-driven development model with P4 behavior specifications. SONiC DASH SmartSwitch has been deployed in Microsoft Azure at scale. It achieves 1.53Tbps throughput, 19.2M CPS, and 256M concurrent connections for network services, while improving power efficiency by ~1.8× and space efficiency by ~2.7× compared to the previous generation.

## [AnyPro: Preference-Preserving Anycast Optimization based on Strategic AS-Path Prepending](/conference/nsdi26/presentation/zhou-minyuan)

Minyuan Zhou, *Nanjing University and Alibaba Cloud;* Yuning Chen, *University of California, Merced, and Alibaba Cloud;* Jiaqi Zheng, *Nanjing University;* Yifei Xu, *University of California, Los Angeles, and Alibaba Cloud;* Pan Hu, Yongping Tang, Wendong Yin, Jie Lin, Qingyan Yu, and Yuanchao Su, *Alibaba Group;* Guihai Chen and Wanchun Dou, *Nanjing University;* Songwu Lu, *University of California, Los Angeles;* Wan Du, *University of California, Merced*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/zhou-minyuan)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/zhou-minyuan)

Operating large-scale anycast networks is challenging because client-to-site mappings often misalign with operator’s expectation due to opaque inter-domain routing. We present AnyPro, the first system to unlock the full potential of AS-path prepending (ASPP), efficiently deriving globally optimal configurations to steer clients toward performance-optimal sites at scale. AnyPro first employs an efficient polling mechanism to identify all clients sensitive to ASPP. By analyzing the routing changes during the process, the system derives a set of ASPP constraints that guide client traffic toward the desired sites. We then formulate the anycast optimization problem as a constraint-based program and compute optimal ASPP configurations. Extensive evaluation on a global testbed with 20 PoPs demonstrates the effectiveness of AnyPro: it reduces the 90th percentile latency by 37.7% compared to baseline configurations without ASPP. Furthermore, we show that AnyPro can be integrated with PoP-level anycast optimization techniques to achieve additional performance gains.

Track 2

## Distributed Data Systems

Session Chair: Zahaib Akhtar, *Amazon and North Carolina State University*

Grand Ballroom VII–IX

## [HCDN: Coordinated Stream Scheduling for Cost-Effective Live Video Delivery](/conference/nsdi26/presentation/wang-liying)

Liying Wang, *Peking University;* Jing Liu, *ByteDance;* Yuhan Zhou and Chengke Wang, *Peking University;* Mingming Lu, Qingyue Li, Song Geng, Linsen Wang, Kaida Hu, Haoyuan Huang, Shimao Tian, Ri Lu, and Mingfei Hao, *ByteDance;* Chenren Xu, *Peking University; and Key Laboratory of High Confidence Software Technologies, Ministry of Education (PKU);* Shu Shi, *ByteDance*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-liying)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wang-liying)

Live video streaming is a major source of today's Internet traffic, yet its delivery through CDNs incurs massive bandwidth costs from both CDN edge traffic (to users) and internal traffic (between CDN nodes). To understand these costs, we conduct a large-scale measurement study of ByteDance’s global in-production live CDN. It reveals two opportunities to reduce CDN bandwidth cost: *(i)* lowering average edge price by incorporating cost-effective best-effort infrastructure into the CDN edge, and *(ii)* improving CDN tree efficiency via finer-grained stream scheduling, accounting for detailed stream characteristics such as non-uniform popularity, heterogeneous stream formats, which amplify internal traffic on cache misses in our prior CDN. To exploit these opportunities into a practical system while addressing challenges in scheduling strategy management and user quality of experience, we design, implement, and deploy HCDN. It comprises *(i)* an augmented CDN edge with cost-effective *best-effort nodes* and *multihomed nodes*, *(ii)* the OpenTiga scheduling framework, which coordinates strategies through modular orchestration and proactive client-side Quality-of-Experience (QoE) assurance, and *(iii)* a set of redirection-based stream scheduling strategies. Over four years of incremental deployment across more than 500 edge clusters, HCDN reduces relative bandwidth cost by 36% while incurring modest overhead and preserving QoE. We further report the deployment experience of HCDN.

## [XLL: Cross-Layer Logging for Data Deduplication in Consensus-Based Storage](/conference/nsdi26/presentation/shawger)

John Shawger, Arnav Jhingran, Andrea Arpaci-Dusseau, and Remzi Arpaci-Dusseau, *University of Wisconsin – Madison*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/shawger)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/shawger)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/shawger)

Modern distributed storage systems exhibit cross-layer data duplication, writing data to disk once during a consensus phase and again during a local database logging phase. The result is poor performance and significant write amplification. To remedy this cross-layer redundancy, we design and implement Cross-Layer Log (XLL), a shared log built upon the principle of key-value separation. We use XLL to deduplicate updates within a distributed key-value store (TiKV), leading to a 5.5x increase in write throughput while reducing write amplification by 73%. We also demonstrate the effectiveness of our crash recovery protocol in maintaining data integrity.

## [HyperEdge: An Edge CDN Infrastructure for Cost Efficient Video Streaming](/conference/nsdi26/presentation/wei)

Dehui Wei, *National University of Singapore;* Jiao Zhang, *Beijing University of Posts and Telecommunications, and Purple Mountain Laboratories;* Haozhe Li, Rui Han, Zhichen Xue, Yajie Peng, Xiaofei Pang, and Yan Ma, *ByteDance;* Jialin Li, *National University of Singapore*

***Awarded Outstanding Paper!***

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wei)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wei)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wei)

As ByteDance’s business expands, the cost of video streaming using content delivery networks (CDN) has become prohibitively high. We have discovered a sea of under-utilized edge devices with the potential to reduce content distribution cost. The unreliable performance of an edge network, however, presents deep challenges to video streaming services. In this work, we introduce HyperEdge, an edge-assisted content delivery system for video streaming. HyperEdge seamlessly integrates the robustness of a conventional CDN with the cost-efficiency of an edge network. It offers dependable streaming quality to users while minimizing traffic expenses. HyperEdge employs a centralized tracker cluster to optimize content distribution to a pool of edge devices, based on real-time monitoring. To ensure satisfactory video playback quality, we develop a novel multi-path protocol for client-edge video transmission. Having been in stable operation for six years, HyperEdge manages over a hundred thousand edge devices, serving about a hundred million users daily, and saving hundreds of millions of dollars in content delivery cost annually.

## [Co-Designing Traffic Control with NVMe-oF for Disaggregated Storage: A Comparative Study of Switched and Switchless SAN Architectures](/conference/nsdi26/presentation/wang-chendong)

Chendong Wang, Joontaek Oh, and Ming Liu, *University of Wisconsin–Madison*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-chendong)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-chendong)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/wang-chendong)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wang-chendong)

Disaggregated storage is a pivotal component of today’s cluster infrastructures. With the advent of high-bandwidth server interconnects and new NVMe form factors, commodity storage appliances are becoming denser, delivering tens of millions of IOPS. This calls for today’s storage area network (SAN) fabric to expand the bandwidth capacity drastically. Industry practices tackle this issue via either (i) a scale-up approach, upgrading the per-port bandwidth in a switched SAN, or (ii) a scale-out strategy, integrating more paths in a switchless SAN. However, it is unclear which network architecture is more suitable for scaling storage disaggregation.

This paper presents a comparative study of switched and switchless SAN architectures from several angles. We begin by developing an experimental methodology that integrates both small-scale real-system prototypes and large-scale simulations, providing the flexibility needed to explore architectural trade-offs. We then characterize NVMe-oF I/O flows and co-design SAN traffic control mechanisms around these characteristics to improve I/O transmission efficiency in both settings. Our evaluation yields several key findings. First, the switchless SAN achieves throughput comparable to that of the switched SAN, despite involving additional routing hops, while simultaneously reducing latency through the use of multiple load-aware I/O paths that mitigate interference. Second, the switchless SAN reduces capital costs by obviating the need for expensive high-radix switches, scales effectively under heterogeneous I/O workloads, and avoids the single point of failure associated with top-of-rack (ToR) switches. Collectively, these results demonstrate that switchless SANs provide a compelling alternative to traditional switched designs for disaggregated storage environments.

## [Cost-effective and Reliable Global Internet Peering with Programmable Switches](/conference/nsdi26/presentation/miao-peering)

Congcong Miao, *Tencent and National University of Singapore;* Zhiyi Yao, Jianchao Lv, and Jinglin Wang, *Tencent;* Shihan Lin, *University of Michigan;* Xinyi Zhang, *CNIC CAS, China;* Yunming Xiao, *The Chinese University of Hong Kong, Shenzhen;* Wei Guo, Jiwu Bu, Yachen Wang, and Xianneng Zou, *Tencent;* Yong Jiang, *Tsinghua Shenzhen International Graduate School;* Marco Canini, *KAUST;* Gaogang Xie, *CNIC CAS, China*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/miao-peering)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/miao-peering)

Large-scale cloud providers always deploy peering routing system at the Internet’s peering edge to route traffic between the cloud and the Internet. Traditional router-based peering systems fail to pace up to the fast-changing application requirements, while the recent host-based approach is not cost-effective and struggles to address malicious traffic from the Internet. In this paper, we advocate for a radical new peering architecture to introduce programmable switches at the peering edge. We propose and implement a first-of-its-kind system, called Janus, to simultaneously handle inbound and outbound network traffic and significantly reduce network hardware cost. The core of Janus’s approach is to leverage a traffic dispatch module to offload most of the outbound traffic to switches to enhance system’s scalability. Janus offloads all inbound traffic to switches and redirects potential malicious traffic to the anti-DDoS service to enhance system reliability. Furthermore, Janus introduces a fast route convergence mechanism to effectively handle Internet-scale route updates. We have gradually deployed Janus at the edge of our production network over the past years. Evaluation results show that Janus can reduce the average hardware cost by 78%, as compared to existing systems while gracefully handling DDoS issues. Meanwhile, Janus can reduce the route convergence within seconds under failure scenarios, which is orders of magnitude faster than existing approaches.

Track 3

## Sandboxes, Containers, and Beyond

Session Chair: Eric Eide, *University of Utah*

Bellevue Room

## [KRAKENGUARD: Towards Fine-Grained eBPF Isolation](/conference/nsdi26/presentation/patel)

Jainil Patel, *IIT Roorkee;* Lucas Graeff Buhl-Nielsen, *Quantco;* Adrien Ghosn, *Microsoft;* Marios Kogias, *Imperial College London*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/patel)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/patel)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/patel)

eBPF is a powerful in-kernel virtual machine that enables dynamic, safe extensions to operating system kernels. Despite the guarantees provided by its in-kernel verifier, eBPF’s access control model remains coarse-grained, relying on broad Linux capabilities, such as CAP_BPF. Once granted, these allow unrestricted loading of eBPF programs to different kernel hooks. This poses serious security risks in multi-tenant or untrusted environments, where a compromised or malicious process can misuse eBPF to trace sensitive activity, access kernel memory, or disrupt system behavior. While existing verification ensures safety properties, it cannot enforce fine-grained constraints on what programs can do.

We present KRAKENGUARD, a trusted user-space manager that enforces fine-grained, policy-driven constraints on eBPF bytecode at load time. Using symbolic execution, it checks all program paths for compliance with policies on helper usage, memory accesses, and return values. It enables safe delegation of program loading by unprivileged processes and detects cross-program interference to ensure safe co-location of eBPF programs on the same host.

We show that KRAKENGUARD can block the misuse of restricted helpers, unauthorized memory and map access, and unsafe packet modifications in real-world eBPF programs, while also being able to detect existing CVEs. As a use case, we implement an XDP-as-a-Service application that securely runs XDP programs belonging to different tenants directly on the host interface after guaranteeing they cannot do anything malicious and that they do not interfere with each other.

## [OneSidedMW: Managing Disaggregated Memory Efficiently, Flexibly, and Securely with RNIC Offloading](/conference/nsdi26/presentation/wang-zixuan)

Zixuan Wang, Jinyu Gu, Xingda Wei, and Yubin Xia, *Shanghai Jiao Tong University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-zixuan)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/wang-zixuan)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/wang-zixuan)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/wang-zixuan)

RDMA-based memory disaggregation is gaining popularity in modern datacenters to improve memory efficiency. However, existing memory management approaches for the disaggregated memory (DM) architecture face a critical tradeoff: they either suffer from poor memory utilization due to coarse-grained allocation, or encounter significant challenges in terms of performance, memory node CPU overhead, security vulnerabilities, and limited flexibility.

In this paper, we present OneSidedMW, a novel system that combines two advanced RDMA features—RDMA NIC (RNIC) offloading and memory windows—to provide fine-grained and highly efficient one-sided memory management primitives for DM. Specifically, it leverages RNIC offloading to perform MW binding and unbinding operations, achieving remote memory allocation and deallocation without involving the memory node’s CPU. To demonstrate the efficiency of OneSidedMW, we evaluate it over two representative DM systems: swap-based systems and disaggregated key-value stores. OneSidedMW achieves up to 10.6× better performance in disaggregated key-value stores and up to 32.3% performance improvement in swap-based systems, compared with the state-of-the-art approaches.

## [Syntra: Synthesizing Cross-Layer Controllers for Low-Latency Video Streaming](/conference/nsdi26/presentation/pan)

Jia Pan, *The University of Texas at Austin;* Anup Agarwal, *Carnegie Mellon University;* Işıl Dillig and Venkat Arun, *The University of Texas at Austin*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/pan)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/pan)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/pan)

Modern applications such as low-latency video streaming demand tight coordination across multiple control dimensions, including bitrate selection, congestion control, frame skipping, and forward error correction (FEC). These dimensions interact in complex ways, making existing heuristic approaches difficult to design, tune, and generalize. This paper presents Syntra, an automated tool that synthesizes joint controllers from a symbolic model of the system and a declarative performance objective. Syntra formulates control as a partially observable game, performs bounded-horizon minimax search (similar to Chess engines) to synthesize strategies, and distills them into an efficient, interpretable policy via imitation learning. Synthesized controllers incorporate novel strategies that exploit the synergy between control dimensions to consistently outperform existing designs in our evaluation.

## [Net-P4ct: Enhanced WAN Bandwidth Fair Sharing Using P4 Programmable Switches](/conference/nsdi26/presentation/chen)

Haoran Chen and Mingwei Cui, *Bytedance;* Yihan Zou, Yihang Miao, Suhan Jiang, Damu Ding, Lirong Lai, Ming Gao, Rui Jiang, Shengyuan He, Anjian Chen, Jiaming Shi, Junjie Wan, Yandong Duan, Ruomin Fang, Hongyu Wu, and Yongping Tang, *ByteDance;* Qiao Kang, *unaffiliated;* Guangrui Wu and Xiyun Xu, *ByteDance*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/chen)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/chen)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/chen)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/chen)

At growing internet companies like ByteDance, Wide Area Network (WAN) bandwidth sharing across diverse services with varying SLO requirements is a fundamental challenge. Conventional host-based enforcement systems, where agents identify and throttle traffic at the server end, face practical challenges such as "blind spot" traffic, kernel-dependent operational complexity, and significant server resource overhead. To address these issues, we present Net-P4ct, an in-network bandwidth enforcement system using P4 programmable switches. Net-P4ct improves both bandwidth guarantees and fair sharing by shifting dynamic QoS control into the switch data plane. Specifically, it achieves broader traffic coverage by combining host-side traffic tagging with a P4-switch pipeline, where service classification and QoS class assignment are performed. Based on observed traffic metrics, a centralized control plane determines real-time policy updates according to the max-min fair bandwidth allocation. We demonstrate the system's benefits including improved bandwidth utilization, reduced operational complexity, and lower per-byte processing cost. Net-P4ct has been deployed in ByteDance's production WAN for nearly a year, and we hope to share our experience with the community.

## [FRCC: Towards Provably Fair and Robust Congestion Control](/conference/nsdi26/presentation/agarwal-anup)

Anup Agarwal, *Carnegie Mellon University;* Venkat Arun, *University of Texas at Austin;* Srinivasan Seshan, *Carnegie Mellon University*

Available Media

[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/agarwal-anup)[![](https://www.usenix.org/themes/neat_conference/images/icons/pdf.svg)](/conference/nsdi26/presentation/agarwal-anup)[![](https://www.usenix.org/themes/neat_conference/images/icons/slides.svg)](/conference/nsdi26/presentation/agarwal-anup)[![](https://www.usenix.org/themes/neat_conference/images/icons/video.svg)](/conference/nsdi26/presentation/agarwal-anup)

Congestion control algorithms (CCAs) play a critical role in network bandwidth allocation. Recent work (from SIGCOMM 2022) showed that a large class of CCAs, including BBR, Copa, and Reno, starve flows in the presence of network jitter. Starvation occurs because CCAs coordinate fairness by encoding fair rates into congestion signals. For example, Reno's throughput scales as 1/√loss rate. Even a small amount of noise in these signals leads to large errors in inferring fair rates.

We present FRCC (Fair and Robust Congestion Controller), the first CCA that provably bounds unfairness (avoids starvation) even under network jitter. Our key insight is to encode only the flow count (or equivalently, the fair link fraction) into the congestion signals, and independently estimate the link capacity to calculate the fair rate. In this way, we bound jitter's impact on fairness. We implement FRCC in the Linux kernel and evaluate it in a variety of network conditions, including synthetic jitter, heterogeneous RTTs, and multi-bottleneck settings. FRCC closely matches the bounds predicted by our theoretical analysis, and consistently achieves fairness, even when state-of-the-art CCAs exhibit starvation.
