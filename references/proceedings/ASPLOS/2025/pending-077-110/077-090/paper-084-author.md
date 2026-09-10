<!-- 从 paper-084-author.html 迁移的资料快照；原始 HTML SHA-256: c85bf78b7fe8c26d1d47f6655bd426a4e8f109cc03d3f356538c9b44661b4cc5。 -->

[Lukas Gerlach](/)

[Lukas Gerlach](/)

- [About](/#about)
- [Blog](/#blog)
- [Publications](/#publication)
- [Talks](/#talks)

# ShadowLoad: Injecting State into Hardware Prefetchers

Lorenz Hetterich, Fabian Thomas, Lukas Gerlach, Ruiyi Zhang, Nils Bernsdorf, Eduard Ebert, Michael Schwarz

January, 2025

[PDF](/publication/2025-shadowload-injecting-state-into-hardware-prefetchers/shadowload_asplos25.pdf) [Cite](#) [Code](https://github.com/cispa/ShadowLoad/)

### Abstract

Hardware prefetchers are an optimization in modern CPUs that predict memory accesses and preemptively load the corresponding value into the cache. Previous work showed that the internal state of hardware prefetchers can act as a side channel, leaking information across security boundaries such as processes, user and kernel space, and even trusted execution environments. In this paper, we present ShadowLoad, a new attack primitive to bring inaccessible victim data into the cache by injecting state into the hardware prefetcher. ShadowLoad relies on the inner workings of the hardware stride prefetchers, which we automatically reverse-engineer using our tool StrideRE. We illustrate how ShadowLoad extends the attack surface of existing microarchitectural attacks such as Meltdown and software-based power analysis attacks like Collide+Power and how it can partially bypass L1TF mitigations on clouds, such as AWS. We further demonstrate FetchProbe, a stride prefetcher side-channel attack leaking offsets of memory accesses with sub-cache-line granularity, extending previous work on control-flow leakage. We demonstrate FetchProbe on the side-channel hardened Base64 implementation of WolfSSL, showing that even real-world side-channel-hardened implementations can be attacked with our new attack.

Type

[Conference paper](/publication/#paper-conference)

Publication

30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems

- [](https://twitter.com/intent/tweet?url=https%3A%2F%2Flukasgerlach.me%2Fpublication%2F2025-shadowload-injecting-state-into-hardware-prefetchers%2F&text=ShadowLoad%3A+Injecting+State+into+Hardware+Prefetchers)
- [](https://www.facebook.com/sharer.php?u=https%3A%2F%2Flukasgerlach.me%2Fpublication%2F2025-shadowload-injecting-state-into-hardware-prefetchers%2F&t=ShadowLoad%3A+Injecting+State+into+Hardware+Prefetchers)
- [](mailto:?subject=ShadowLoad%3A%20Injecting%20State%20into%20Hardware%20Prefetchers&body=https%3A%2F%2Flukasgerlach.me%2Fpublication%2F2025-shadowload-injecting-state-into-hardware-prefetchers%2F)
- [](https://www.linkedin.com/shareArticle?url=https%3A%2F%2Flukasgerlach.me%2Fpublication%2F2025-shadowload-injecting-state-into-hardware-prefetchers%2F&title=ShadowLoad%3A+Injecting+State+into+Hardware+Prefetchers)

© 2026 Lukas Gerlach.

##### Cite

×

[ Copy](#) [ Download](#)
