<!-- 从 mlsys2025-cbc4ab80cd77aa0eb87da062fbcddb46.html 迁移的资料快照；原始 HTML SHA-256: 4ace6e4e671f598be5566efb8f798ec098bfe03ecfd1f6ebf690bb6f1f1e8c7d。 -->

[MLSys Proceedings](/)

- [](/admin/login/?next=/admin/)
- [](/admin/logout/?nextp=/admin)

Search

# Seesaw: High-throughput LLM Inference via Model Re-sharding

Qidong Su, Wei Zhao, Xin Li, Muralidhar Andoorveedu, Chenhao Jiang, Zhanda Zhu, Kevin Song, Christina Giannoula, Gennady Pekhimenko

[Proceedings of Machine Learning and Systems 7 (MLSys 2025)](/paper_files/paper/2025) Conference

[Bibtex](/paper_files/paper/637-/bibtex) [Paper](/paper_files/paper/2025/file/cbc4ab80cd77aa0eb87da062fbcddb46-Paper-Conference.pdf) [Supplemental](/paper_files/paper/2025/file/cbc4ab80cd77aa0eb87da062fbcddb46-Supplemental-Conference.pdf)

## Abstract

To improve the efficiency of distributed large language model (LLM) inference, various parallelization strategies, such as tensor and pipeline parallelism, have been proposed. However, the distinct computational characteristics inherent in the two stages of LLM inference—prefilling and decoding—render a single static parallelization strategy insufficient for the effective optimization of both stages. In this work, we present Seesaw, an LLM inference engine optimized for throughput-oriented tasks. The key idea behind Seesaw is dynamic model re-sharding, a technique that facilitates the dynamic reconfiguration of parallelization strategies across stages, thereby maximizing throughput at both phases. To mitigate re-sharing overhead and optimize computational efficiency, we employ tiered KV cache buffering and transition-minimizing scheduling. These approaches work synergistically to reduce the overhead caused by frequent stage transitions while ensuring maximum batching efficiency. Our evaluation demonstrates that Seesaw achieves a throughput increase of up to 1.78\$\times\$ (1.36\$\times\$ on average) compared to vLLM, the most widely used state-of-the-art LLM inference engine.

  

#### Name Change Policy

×

Requests for name changes in the electronic proceedings will be accepted with no questions asked. However name changes may cause bibliographic tracking issues. Authors are asked to consider this carefully and discuss it with their co-authors prior to requesting a name change in the electronic proceedings.

Use the "Report an Issue" link to request a name change.

[Report an Issue](https://mlsys.org/Help/Contact?select=Conference)    \|    [Name Change Policy](#)

Do not remove: This comment is monitored to verify that the site is working properly
