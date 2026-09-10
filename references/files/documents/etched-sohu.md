<!-- 从 etched-sohu.html 迁移的资料快照；原始 HTML SHA-256: 49be23a7e800615dceeb2b3b1d444f6b73b83e008f49f4e990bf79205abab6a8。 -->

![Etched inference rack](https://cdn.sanity.io/images/rwbees58/production/ecfe2c98b278a716b87fcd2c529792bda7ea2e86-4288x2041.png?auto=format&fit=max&w=4096&q=90)

# Frontier Inference ClustersFrontier Inference Clusters

![Etched inference rack](https://cdn.sanity.io/images/rwbees58/production/3fd972c6f27740350ad15cbaedec4f7f2c5ecd2c-568x990.png?auto=format&fit=max&w=4096&q=90)

![Inside an Etched rack — liquid-cooled compute](https://cdn.sanity.io/images/rwbees58/production/61890722a989529e1231bee50b2a8227587e8897-496x694.png?auto=format&fit=max&w=4096&q=90)

![Etched inference card](https://cdn.sanity.io/images/rwbees58/production/855a967160c9ace718481069901b4284aa9482f2-354x514.png?auto=format&fit=max&w=4096&q=90)

![An Etched inference chip](https://cdn.sanity.io/images/rwbees58/production/f840aa6e8c6458d74cd2d05b32fa74ad58936774-344x410.png?auto=format&fit=max&w=4096&q=90)

![Etched inference rack](https://cdn.sanity.io/images/rwbees58/production/3fd972c6f27740350ad15cbaedec4f7f2c5ecd2c-568x990.png?auto=format&fit=max&w=4096&q=90)

![Inside an Etched rack — liquid-cooled compute](https://cdn.sanity.io/images/rwbees58/production/61890722a989529e1231bee50b2a8227587e8897-496x694.png?auto=format&fit=max&w=4096&q=90)

![Etched inference card](https://cdn.sanity.io/images/rwbees58/production/855a967160c9ace718481069901b4284aa9482f2-354x514.png?auto=format&fit=max&w=4096&q=90)

![An Etched inference chip](https://cdn.sanity.io/images/rwbees58/production/f840aa6e8c6458d74cd2d05b32fa74ad58936774-344x410.png?auto=format&fit=max&w=4096&q=90)

## We're building a new category of AI hardware: frontier inference clusters.

We co-design chips, racks, software, and manufacturing methods so frontier models can run with best-in-class throughput, latency, cost, and power efficiency for both prefill and decode workloads.

Earlier this year our **A0 silicon** came back from TSMC N4P, and today we are busy validating our first rack-scale product with customers to fulfill \$1B in demand.

We're a team of 400+ engineers from NVIDIA, Google TPUs, Broadcom, SK Hynix, TSMC, and more. We've raised \$800M across four unannounced financings, including a strategic investment from VentureTech Alliance. We're excited to deepen our partnership with the world's leading semiconductor manufacturer.

## Designing a New Pareto Frontier

Our inference systems are built to push the entire pareto curve on frontier models, including many-trillion-parameter MoEs, long context, and agentic workloads. This required intense co-design, from new chips, packages, PCBs, cold plates, interconnects, and more. Today, we're sharing two breakthroughs to make this happen:

### Low Voltage Inference (LVI) for high throughput workloads

Today, AI chips can't scale FLOPs without thermal throttling. As FLOPs utilization increases, AI chips draw more power and downregulate clock speed. This often results in sustained inference throughput under half of Peak FLOPs.

We've designed a new architecture to run our chip's math blocks at under half the voltage of most AI chips. This enables multiple times the FLOPs density of AI chips today. We can run trillion-parameter sparse MoEs at 80%+ Peak FLOPs without thermal throttling.

Running LVI requires co-designing the entire cluster from the transistor to the token: new splittable math arrays, circuit techniques, novel tiling and scheduling algorithms, power delivery networks, VRM architectures, advanced packaging, cold plate designs, and more.

### Cluster Scale Memory (CSM) for low-latency workloads

Today's AI chips using HBM can't achieve SRAM-level decode speeds due to memory subsystem and interconnect bottlenecks. SRAM-only chips have lower FLOPs density and memory capacity, sacrificing throughput.

We created a much lower-latency shared memory pool across our scale-up domain. We use a proprietary ultra-low-latency, high-bandwidth interconnect to enable dramatically faster memory access across chips.

Our HBM/SRAM hybrid design solves both memory capacity and mem2mem latency, enabling high throughput and interactivity simultaneously. CSM improves latency and avoids today's cost, reliability, yield, thermal, and compute tradeoffs of SRAM-only chips, 3D DRAM chips, or optics.

We've made co-design decisions hand-in-hand with leading AI companies, cloud providers, and hyperscalers. We've tested racks in representative data center deployments, run terabytes of production traffic patterns through our simulator, and had dozens of engineers live overseas for months to co-design deeply with our supply-chain partners. If this sounds exciting, you should [join us](/join).

## Getting to Gigawatt Scale

Early customer tests show us achieving SOTA throughput, latency, and power efficiency on inference workloads. We'll be sharing more updates on our performance and roadmap this summer.

Our first racks ship this summer, and we've kicked off production to fulfill over \$1B in customer contracts. To enable 24/7 engineering cycles, we've opened a Taiwan factory and built a data center, test house, and NPI prototyping lab in our San Jose office.

We are vertically integrated to get to Gigawatt scale as quickly as possible. Math block designers sit next to inference engineers, thermal experts next to GSMs.

Get Access![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI3IiBoZWlnaHQ9IjciIHZpZXdib3g9IjAgMCA3IDciIGZpbGw9Im5vbmUiIGFyaWEtaGlkZGVuPSJ0cnVlIiBmb2N1c2FibGU9ImZhbHNlIiBjbGFzcz0idy03IGgtNyBzaHJpbmstMCB0ZXh0LWluaGVyaXQiPjxwYXRoIGQ9Ik0zIDZMNC45MiAzLjlIMFYyLjgySDQuOTJMMyAwLjcyTDMuNzggMEw2Ljg0IDMuMzZMMy43OCA2LjcyTDMgNloiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48L3N2Zz4=)

![Portrait of Gavin Uberti](https://cdn.sanity.io/images/rwbees58/production/287a5976589953f4f8bdb80c260fb5b41663580d-800x800.png?auto=format&fit=max&w=4096&q=85)

### Gavin Uberti

Co-Founder & CEO

Harvard Thiel Fellow. World math champion, Math 55 alumnus, expert in AI compilers, developed the Cortex-M backend for TVM.

![Portrait of Robert Wachen](https://cdn.sanity.io/images/rwbees58/production/4b397d71a70d770848c6f31782cc0f547cd27e37-724x590.png?auto=format&fit=max&w=4096&q=85)

### Robert Wachen

Co-Founder & President

Harvard Thiel Fellow. Co-founded Prod (\$100B+ cohort valuation) and Mentor Labs (acq. by Crimson Education).

![Portrait of Mark Ross](https://cdn.sanity.io/images/rwbees58/production/bda312e3b49abe4351ed8acfbfc0634f2dfee60f-720x587.png?auto=format&fit=max&w=4096&q=85)

### Mark Ross

CTO

Ex-CTO of Cypress (acquired for \$9.4B). Shipped 5 systems generating \>\$1B in revenue, all on A0 silicon.

![Portrait of Brian Loiler](https://cdn.sanity.io/images/rwbees58/production/64bb8f09af42543cba91de373eb41f72928ef101-640x640.png?auto=format&fit=max&w=4096&q=85)

### Brian Loiler

VP of Platform

Ex-NVIDIA for 22 years. Led platform engineering teams across NVIDIA. Built the HGX and DGX systems from scratch.

![Portrait of Wayne Cao](https://cdn.sanity.io/images/rwbees58/production/d480bed7a51a95887f239ed0e3aacd540eeeced0-4911x4911.png?auto=format&fit=max&w=4096&q=85)

### Wayne Cao

VP of Production

Led 0-1 production & supply chain ramps for 24 products including the original iPhone, MacBook Air, Pixel, and Chromebook.

![Portrait of Saptadeep Pal](https://cdn.sanity.io/images/rwbees58/production/9b47f31be784dfee760b3e8791ffd07dacf1cc58-800x800.png?auto=format&fit=max&w=4096&q=85)

### Saptadeep Pal

VP of ASIC & Architecture

Co-founded Auradine. NVIDIA H100/A100/V100 architecture team. Qualcomm award for research on waferscale SRAM & DRAM stacking.

![Portrait of David Munday](https://cdn.sanity.io/images/rwbees58/production/12e80793e88cae89944179ddb82ff4db5bb07745-800x800.png?auto=format&fit=max&w=4096&q=85)

### David Munday

VP of Software

Built the TPU software team (TPU v1-v5) and led research for Project Astra at Deepmind.

![Portrait of Tim Perevozchikov](https://cdn.sanity.io/images/rwbees58/production/97597273dfec500af86a0be6bfb649b0d1b9337c-639x640.png?auto=format&fit=max&w=4096&q=85)

### Tim Perevozchikov

VP of Finance

Ex-VP Quant Trading & Chief of Staff to CEO at Two Sigma Securities. Built multiple new trading desks from scratch.

![Portrait of Ajat Hukkoo](https://cdn.sanity.io/images/rwbees58/production/7f30d709addc0ee14fc51bcb7557bfcd6c3fc190-1600x1303.png?auto=format&fit=max&w=4096&q=85)

### Ajat Hukkoo

 

Distinguished Engineer at Broadcom & VP of Intel's Custom Silicon Group. Shipped 300 million chips across nine A0 products.

![Portrait of Chris Zhu](https://cdn.sanity.io/images/rwbees58/production/fa430b72e285007cf681f1f02480a8a2b711021a-1600x1298.png?auto=format&fit=max&w=4096&q=85)

### Chris Zhu

Co-Founder

Harvard Thiel Fellow. Math and high performance computing researcher, Math 55 alumnus. Published novel combinatorics work.

[Build the future of inference →Build the future of inference →](/join)

We’re grateful for the support of our investors and angels, *including:*

![Sequoia](https://cdn.sanity.io/images/rwbees58/production/8114328ed3df544fc3423dede4b60f8711da8fef-404x150.png?auto=format&fit=max&w=4096&q=85)

![Andreessen Horowitz](https://cdn.sanity.io/images/rwbees58/production/b4e6d9e1a42784d25f6c6a40d9e3f77524e8d705-404x150.png?auto=format&fit=max&w=4096&q=85)

![SK hynix](https://cdn.sanity.io/images/rwbees58/production/ca10b871138cba183296d8ba034f341eb2c4c2c0-404x150.png?auto=format&fit=max&w=4096&q=85)

![VentureTech Alliance](https://cdn.sanity.io/images/rwbees58/production/3ba0990c04c028e0e0172dc5de7eee8d154616fb-404x150.png?auto=format&fit=max&w=4096&q=85)

![Jane Street](https://cdn.sanity.io/images/rwbees58/production/5f20860bcc0a5db7d7875e93ef7166cfae3eea1e-404x150.png?auto=format&fit=max&w=4096&q=85)

![Two Sigma](https://cdn.sanity.io/images/rwbees58/production/e9c5f3e29e26b6dc0f2f39e7df20b91f758d0bba-404x150.png?auto=format&fit=max&w=4096&q=85)

![Blackstone](https://cdn.sanity.io/images/rwbees58/production/6a2505803c8529941262e2f6213343c8471be7c5-404x150.png?auto=format&fit=max&w=4096&q=85)

![](https://cdn.sanity.io/images/rwbees58/production/4e95f4d3a498de02de084b0d61adddcf5a4603b4-1561x780.png?auto=format&fit=max&w=4096&q=85)

![Tiger Global](https://cdn.sanity.io/images/rwbees58/production/e3d5840216245d0f979bcf21d5e7f5a588db5932-404x150.png?auto=format&fit=max&w=4096&q=85)

![Jump Trading](https://cdn.sanity.io/images/rwbees58/production/764bc67c46e7c320c67b4689471e8ad505299ace-404x150.png?auto=format&fit=max&w=4096&q=85)

![HRT](https://cdn.sanity.io/images/rwbees58/production/9d0fca8a8d7fb865a997069c9e02afd937d6ba5b-404x150.png?auto=format&fit=max&w=4096&q=85)

![Thiel](https://cdn.sanity.io/images/rwbees58/production/1de941e5c061e069679fbc2edecc3f7a62932233-404x150.png?auto=format&fit=max&w=4096&q=85)

![Ribbit](https://cdn.sanity.io/images/rwbees58/production/95a27c9ae1ee7d9b457f5692f08df6a78f03a5b5-404x150.png?auto=format&fit=max&w=4096&q=85)

![Stripes](https://cdn.sanity.io/images/rwbees58/production/5654df6f353480e8fca59a55fbdc1b98e70716fa-404x150.png?auto=format&fit=max&w=4096&q=85)

![BCV](https://cdn.sanity.io/images/rwbees58/production/e865ee73cc166f7f48fe20f99b88459611aefbe6-404x150.png?auto=format&fit=max&w=4096&q=85)

![](https://cdn.sanity.io/images/rwbees58/production/11c0fa4cb844746fa54babbc500b02b5556ae115-404x152.png?auto=format&fit=max&w=4096&q=85)

Tri Dao

FlashAttention

Geoffrey Hinton

Godfather of AI

Peter Thiel

Thiel Capital

Jerry Tworek

OpenAI

Andrej Karpathy

Anthropic

Aidan Gomez

Cohere

Arthur Mensch

Mistral

Noam Brown

OpenAI

Scott Wu

Cognition

Fei-Fei Li

World Labs

Tal Broda

OpenAI

Stanley Druckenmiller

Duquesne

Ben Spector

Flapping Airplanes

Irwan Bello

Reflection AI

Pieter Abbeel

Covariant

Shivon Zilis

Neuralink

Amjad Masad

Replit

Jason Warner

Poolside

Zach Dell

Base Power

Kyle Vogt

The Bot Company

Scott Belsky

A24

Lachy Groom

Physical Intelligence

Nikesh Arora

Palo Alto Networks

Bryan Johnson

Blueprint

Karim Atiyeh

Ramp

Dylan Field

Figma

Stefano Ermon

Inception

Yash Patil

Applied Compute

Jesse Zhang

Decagon

Nikita Bier

X
