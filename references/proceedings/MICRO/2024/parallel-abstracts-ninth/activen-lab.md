<!-- 从 activen-lab.html 迁移的资料快照；原始 HTML SHA-256: a50e4f15c8726d0624863bb51a62352464a00e39f1fdbc3d9c02f5bf760d2704。 -->

# Search

[](#)

[CRAFT Lab](/)

[CRAFT Lab](/)

- [Home](/#lab)
- [People](/people)
- [Publications](/publication)
- [Patent](/patent)
- [Contact](/contact)

- [](#)
- [](#)
  [Light](#) [Dark](#) [Automatic](#)
- [](#)
  English

  [中文 (简体)](//craft.cs.tsinghua.edu.cn/zh/publication/activen-a-scalable-and-flexibly-programmable-event-driven-neuromorphic-processor/)

# ActiveN: A Scalable and Flexibly-programmable Event-driven Neuromorphic Processor

[Xiaoyi Liu](/author/xiaoyi-liu/), [Zhongzhu Pu](/author/zhongzhu-pu/), [Peng Qu](/author/peng-qu/), [Weimin Zheng](/author/weimin-zheng/), [Youhui Zhang](/author/youhui-zhang/)

July, 2024

### Abstract

At present, most neuromorphic chips utilize custom circuits and/or on-chip memory to achieve neural computations and parameter storage. However, with the diversified development of brain-inspired applications, this approach faces significant challenges regarding programming flexibility and scalability. To address these issues, we propose a RISC-V-based many-core neuromorphic architecture, ActiveN. Each neuro-core is equipped with an active-message-enabled micro-architecture to support the event-driven programming model of Spiking Neural Networks (SNNs), and the memory subsystem is enhanced to identify sparse data and forward them directly. These mechanisms significantly mitigate the impact of memory latency on performance, enabling the storage of synapse data in off-chip (or off-die) bulk storages (e.g., DRAMs, HBMs). This enhancement not only improves storage scalability but also increases computing density. Furthermore, the core’s instruction set is customized to include a compact and complete set of fixed- and floating-point computing instructions, supporting various neural models and SNN computation algorithms flexibly. End-to-end prototype testing demonstrates that, compared to a state-of-the-art chip based on custom circuitry and on-chip SRAM that also supports event-driven operations, ActiveN can integrate over 10x more processing units (512) with strong scalability to fully utilize memory bandwidth. Additionally, it achieves 7.9 times the performance of this counterpart and 96.6 times the performance of an NVIDIA A100 GPU, while maintaining flexible programmability.

Publication

*In 57th Annual IEEE/ACM International Symposium on Microarchitecture (MICRO’24)*

- [](https://twitter.com/intent/tweet?url=%2F%2Fcraft.cs.tsinghua.edu.cn%2Fpublication%2Factiven-a-scalable-and-flexibly-programmable-event-driven-neuromorphic-processor%2F&text=ActiveN%3A+A+Scalable+and+Flexibly-programmable+Event-driven+Neuromorphic+Processor)
- [](https://www.facebook.com/sharer.php?u=%2F%2Fcraft.cs.tsinghua.edu.cn%2Fpublication%2Factiven-a-scalable-and-flexibly-programmable-event-driven-neuromorphic-processor%2F&t=ActiveN%3A+A+Scalable+and+Flexibly-programmable+Event-driven+Neuromorphic+Processor)
- [](mailto:?subject=ActiveN%3A%20A%20Scalable%20and%20Flexibly-programmable%20Event-driven%20Neuromorphic%20Processor&body=%2F%2Fcraft.cs.tsinghua.edu.cn%2Fpublication%2Factiven-a-scalable-and-flexibly-programmable-event-driven-neuromorphic-processor%2F)
- [](https://www.linkedin.com/shareArticle?url=%2F%2Fcraft.cs.tsinghua.edu.cn%2Fpublication%2Factiven-a-scalable-and-flexibly-programmable-event-driven-neuromorphic-processor%2F&title=ActiveN%3A+A+Scalable+and+Flexibly-programmable+Event-driven+Neuromorphic+Processor)
- [](whatsapp://send?text=ActiveN%3A+A+Scalable+and+Flexibly-programmable+Event-driven+Neuromorphic+Processor%20%2F%2Fcraft.cs.tsinghua.edu.cn%2Fpublication%2Factiven-a-scalable-and-flexibly-programmable-event-driven-neuromorphic-processor%2F)
- [](https://service.weibo.com/share/share.php?url=%2F%2Fcraft.cs.tsinghua.edu.cn%2Fpublication%2Factiven-a-scalable-and-flexibly-programmable-event-driven-neuromorphic-processor%2F&title=ActiveN%3A+A+Scalable+and+Flexibly-programmable+Event-driven+Neuromorphic+Processor)

[![Xiaoyi Liu](/author/xiaoyi-liu/avatar_huf5cbae54102930969875e87967da8f7a_19909_270x270_fill_q75_lanczos_center.jpg)](/author/xiaoyi-liu/)

##### [Xiaoyi Liu](/author/xiaoyi-liu/)

- [](https://orcid.org/0009-0007-5045-7884)

[![Zhongzhu Pu](/author/zhongzhu-pu/avatar_hu14a89deae323b8c6d83e2fc6de6dc649_62789_270x270_fill_q75_lanczos_center.jpg)](/author/zhongzhu-pu/)

##### [Zhongzhu Pu](/author/zhongzhu-pu/)

[![Peng Qu](/author/peng-qu/avatar_hu6fa0700afe8f2affdf58d23a1fd818bf_40524_270x270_fill_q75_lanczos_center.jpg)](/author/peng-qu/)

##### [Peng Qu](/author/peng-qu/)

- [](https://orcid.org/0000-0002-1786-5372)
- [](https://ieeexplore.ieee.org/author/37085766801)
- [](https://scholar.google.com/citations?user=zNKRgWEAAAAJ)
- [](https://www.scopus.com/authid/detail.uri?authorId=57202670864)

[![Weimin Zheng](/author/weimin-zheng/avatar_hu96e209798b993355a0f889e00d50ff2b_93692_270x270_fill_q75_lanczos_center.jpg)](/author/weimin-zheng/)

##### [Weimin Zheng](/author/weimin-zheng/)

###### Professor

- [](mailto:zwm-dcs@mail.tsinghua.edu.cn)
- [](https://scholar.google.com/citations?user=3GO5nkEAAAAJ)

[![Youhui Zhang](/author/youhui-zhang/avatar_hu7a95e4d2eea5def9cc6bf2851d052d89_10045_270x270_fill_q75_lanczos_center.jpg)](/author/youhui-zhang/)

##### [Youhui Zhang](/author/youhui-zhang/)

###### Professor

- [](mailto:zyh02@tsinghua.edu.cn)
- [](https://orcid.org/0000-0003-2333-3580)
- [](https://ieeexplore.ieee.org/author/37656215000)
- [](https://dblp.org/pid/00/5995.html)
- [](https://scholar.google.com/citations?hl=zh-CN&user=ZlYjCsAAAAAJ)

© 2026 CRAFT Lab. This work is licensed under [CC BY NC ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0)

[ ](https://creativecommons.org/licenses/by-nc-nd/4.0)

Published with [Hugo Blox Builder](https://hugoblox.com/?utm_campaign=poweredby) — the free, [open source](https://github.com/HugoBlox/hugo-blox-builder) website builder that empowers creators.

##### Cite

×

[ Copy](#) [ Download](#)
