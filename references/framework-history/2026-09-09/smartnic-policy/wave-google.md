<!-- 从 wave-google.html 迁移的资料快照；原始 HTML SHA-256: 4fef30b8c56c8a7afc5756d916b93bb69cd8d0abe6ca60d68b8fc7b86dfc58a0。 -->

1.  [Home](/) ![](data:image/svg+xml;base64,PHN2ZyByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0iZ2x1ZS1pY29uICAiPgogIDx1c2UgaHJlZj0iL2dyL3N0YXRpYy9hc3NldHMvaWNvbnMvZ2x1ZS1pY29ucy5zdmcjY2hldnJvbi1yaWdodCIgLz4KPC9zdmc+)
2.  [Publications](/pubs/) ![](data:image/svg+xml;base64,PHN2ZyByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0iZ2x1ZS1pY29uICAiPgogIDx1c2UgaHJlZj0iL2dyL3N0YXRpYy9hc3NldHMvaWNvbnMvZ2x1ZS1pY29ucy5zdmcjY2hldnJvbi1yaWdodCIgLz4KPC9zdmc+)

# Wave: Offloading Resource Management to SmartNIC Cores

Jack Humphries

Neel Natu

Kostis Kaffes

[Stanko Novakovic](/people/267776/)

[Paul Turner](/people/author31565/)

Hank Levy

[David Culler](/people/davidculler/)

Christos Kozyrakis

2025

[![](data:image/svg+xml;base64,PHN2ZyByb2xlPSJwcmVzZW50YXRpb24iIGFyaWEtaGlkZGVuPSJ0cnVlIiBjbGFzcz0iZ2x1ZS1pY29uICAiPgogIDx1c2UgaHJlZj0iL2dyL3N0YXRpYy9hc3NldHMvaWNvbnMvZ2x1ZS1pY29ucy5zdmcjZmlsZS1kb3dubG9hZCIgLz4KPC9zdmc+) Download](https://dl.acm.org/doi/abs/10.1145/3676642.3736113) [Google Scholar](https://scholar.google.com/scholar?lr&ie=UTF-8&oe=UTF-8&q=Wave:%20Offloading%20Resource%20Management%20to%20SmartNIC%20Cores%20David%20Culler%20Stanko%20Novakovic%20Paul%20Turner%20Christos%20Kozyrakis%20Jack%20Humphries%20Kostis%20Kaffes%20Neel%20Natu%20Hank%20Levy)

Copy Bibtex

## Abstract

SmartNICs are increasingly deployed in datacenters to offload tasks from server CPUs, improving the efficiency and flexibility of datacenter security, networking and storage. Optimizing cloud server efficiency in this way is critically important to ensure that virtually all server resources are available to paying customers. Userspace system software, specifically, decision-making tasks performed by various operating system subsystems, is particularly well suited for execution on mid-tier SmartNIC ARM cores. To this end, we introduce Wave, a framework for offloading userspace system software to processes/agents running on the SmartNIC. Wave uses Linux userspace systems to better align system functionality with SmartNIC capabilities. It also introduces a new host-SmartNIC communication API that enables offloading of even μs-scale system software. To evaluate Wave, we offloaded preexisting userspace system software including kernel thread scheduling, memory management, and an RPC stack to SmartNIC ARM cores, which showed a performance degradation of 1.1%-7.4% in an apples-to-apples comparison with on-host implementations. Wave recovered host resources consumed by on-host system software for memory management (saving 16 host cores), RPCs (saving 8 host cores), and virtual machines (an 11.2% performance improvement). Wave highlights the potential for rethinking system software placement in modern datacenters, unlocking new opportunities for efficiency and scalability.

## Meet the teams driving innovation

Our teams advance the state of the art through research, systems engineering, and collaboration across Google.

[See our teams](https://research.google/teams/)

![ResearchPhilosophyBanner](https://storage.googleapis.com/gweb-research2023-media/images/ResearchPhilosophyBanner.original.png)
