<!-- 从 mlsys2026-bfa6dd59c1d7f7c785909f9ff7cffe67.html 迁移的资料快照；原始 HTML SHA-256: d7c633a72379f19529913880c936dc76607e1214a2621131401ad42bfd3a1b41。 -->

[MLSys Proceedings](/)

- [](/admin/login/?next=/admin/)
- [](/admin/logout/?nextp=/admin)

Search

# Zorse: Optimizing LLM Training Efficiency on Heterogeneous GPU Clusters

Runsheng Guo, Utkarsh Anand, Khuzaima Daudjee, Rathijit Sen

[Proceedings of Machine Learning and Systems 8 (MLSys 2026)](/paper_files/paper/2026) Conference

[Bibtex](/paper_files/paper/714-/bibtex) [Paper](/paper_files/paper/2026/file/bfa6dd59c1d7f7c785909f9ff7cffe67-Paper-Conference.pdf) [Supplemental](/paper_files/paper/2026/file/bfa6dd59c1d7f7c785909f9ff7cffe67-Supplemental-Conference.pdf)

## Abstract

Large language models (LLMs) require vast amounts of GPU compute to train, but limited availability and high costs of GPUs make homogeneous clusters impractical for many organizations. Instead, assembling heterogeneous clusters by pooling together GPUs of different generations allows them to achieve higher aggregate compute and make use of all available GPUs. However, training on heterogeneous clusters presents significant challenges. The workload must be carefully partitioned such that GPUs in the cluster with limited compute, memory, or network bandwidth do not bottleneck the training process. Existing heterogeneous training systems cannot do so efficiently since they integrate data, pipeline, and tensor parallelism in a way that trades off communication for memory overhead. Combining vanilla data parallelism with pipeline parallelism is communication-efficient but results in high memory overhead from replicating model parameters. Alternatively, using sharded data parallelism or tensor parallelism reduces memory overhead but increases communication overhead when combined with pipeline parallelism. To address this problem, we designed Zorse, a system that uses Pipeline-Efficient ZeRO DP, a novel integration of pipeline parallelism and data parallelism that is both communication- and memory-efficient. Zorse uses a planner to automatically find an optimized training configuration from the vast search space of possibilities on heterogeneous clusters, and our evaluation shows that Zorse achieves up to 3× higher training throughput than state-of-the-art systems across representative heterogeneous training scenarios.

  

#### Name Change Policy

×

Requests for name changes in the electronic proceedings will be accepted with no questions asked. However name changes may cause bibliographic tracking issues. Authors are asked to consider this carefully and discuss it with their co-authors prior to requesting a name change in the electronic proceedings.

Use the "Report an Issue" link to request a name change.

[Report an Issue](https://mlsys.org/Help/Contact?select=Conference)    \|    [Name Change Policy](#)

Do not remove: This comment is monitored to verify that the site is working properly
