<!-- 从 paper-089-author-detail.html 迁移的资料快照；原始 HTML SHA-256: 359a97212856c56e9a14bcc4502b16ca00921c32526b824865b28d8358d79858。 -->

![Cong Li](https://leesou.github.io/images/avatar.jpg)

### Cong Li

Ph.D. Candidate

Follow

- Beijing, China
- Peking University
- [Email](mailto:leesou@pku.edu.cn)
- [Google Scholar](https://scholar.google.com/citations?user=x_cc57EAAAAJ)
- [ORCID](http://orcid.org/0000-0001-7760-3254)
- [Github](https://github.com/leesou)

# CTXNL: A Software-Hardware Co-designed Solution for Efficient CXL-Based Transaction Processing

Published in *International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS)*, 2025

Transaction processing systems are the crux for modern data-center applications, yet current multi-node systems are slow due to network overheads. This paper advocates for Compute Express Link (CXL) as a network alternative, which enables low-latency and cache-coherent shared memory accesses. However, directly adopting standard CXL primitives leads to performance degradation due to the high cost of maintaining cross-node cache coherence. To address the CXL challenges, this paper introduces CTXNL, a software-hardware co-designed system that implements a novel hybrid coherence primitive tailored to the loosely coherent nature of transactional data. The core innovation of CTXNL is empowering transaction system developers with the ability to selectively achieve data coherence. Our evaluations on OLTP workloads demonstrate that CTXNL enhances performance, outperforming current network-based systems and achieves up to 2.08x greater throughput than vanilla CXL memory sharing architectures across universal transaction processing policies.

[Download paper here](https://dl.acm.org/doi/abs/10.1145/3676641.3716244)

``` highlight
@inproceedings{wang2025ctxnl,
  title={CTXNL: A software-hardware co-designed solution for efficient cxl-based transaction processing},
  author={Wang, Zhao and Chen, Yiqi and Li, Cong and Guan, Yijin and Niu, Dimin and Guan, Tianchan and Du, Zhaoyang and Wei, Xingda and Sun, Guangyu},
  booktitle={Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 2},
  pages={192--209},
  year={2025}
}
```

[ X (formerly Twitter)](https://x.com/intent/post?text=https://leesou.github.io/publications/2025-2-ctxnl "Share on X") [ Facebook](https://www.facebook.com/sharer/sharer.php?u=https://leesou.github.io/publications/2025-2-ctxnl "Share on Facebook") [ LinkedIn](https://www.linkedin.com/shareArticle?mini=true&url=https://leesou.github.io/publications/2025-2-ctxnl "Share on LinkedIn")

[Previous](https://leesou.github.io/publications/2025-1-unindp "UniNDP: A Unified Compilation and Simulation Tool for Near DRAM Processing Architectures ") [Next](https://leesou.github.io/publications/2025-3-aim "AIM: Software and Hardware Co-design for Architecture-level IR-drop Mitigation in High-performance PIM ")
