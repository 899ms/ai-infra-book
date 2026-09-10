<!-- 从 mlsys2026-42a452cbafa9dd64e9ba4aa95cc1ef21.html 迁移的资料快照；原始 HTML SHA-256: 02d08d25def1c9722cb930f602b7fc0ff975bdbb8587e373905012aee0826f57。 -->

[MLSys Proceedings](/)

- [](/admin/login/?next=/admin/)
- [](/admin/logout/?nextp=/admin)

Search

# Demystifying the Mixture of Experts Serving Tax

Pratyush Patel, Dayeol Lee, Shintaro Iwasaki, Arvind Krishnamurthy

[Proceedings of Machine Learning and Systems 8 (MLSys 2026)](/paper_files/paper/2026) Conference

[Bibtex](/paper_files/paper/734-/bibtex) [Paper](/paper_files/paper/2026/file/42a452cbafa9dd64e9ba4aa95cc1ef21-Paper-Conference.pdf)

## Abstract

Mixture-of-Experts (MoEs) enable massive model sizes but incur higher serving overheads than dense models at the same per-token compute cost. This MoE tax varies with the model architecture, inference phase, and parallelism strategy. We comprehensively study the tax for different MoE models, finding that they perform 2–3× worse than FLOP-equivalent dense models. Using microbenchmarks, we analyze and categorize the underlying tax sources and show how they manifest differently under different configurations. Our key result is that prefill and decode phases incur vastly different taxes; counterintuitively, load imbalance across experts that harms prefill performance can benefit decode by activating fewer experts. We decompose the tax into analytically separable components and propose a balls-bins-buckets framework to study recent MoE developments like fine-grained experts and data parallel attention. We conclude by discussing existing and new techniques to reduce the MoE tax and their associated trade-offs.

  

#### Name Change Policy

×

Requests for name changes in the electronic proceedings will be accepted with no questions asked. However name changes may cause bibliographic tracking issues. Authors are asked to consider this carefully and discuss it with their co-authors prior to requesting a name change in the electronic proceedings.

Use the "Report an Issue" link to request a name change.

[Report an Issue](https://mlsys.org/Help/Contact?select=Conference)    \|    [Name Change Policy](#)

Do not remove: This comment is monitored to verify that the site is working properly
