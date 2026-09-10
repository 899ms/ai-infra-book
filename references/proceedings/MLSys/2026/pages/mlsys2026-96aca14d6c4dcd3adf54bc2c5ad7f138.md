<!-- 从 mlsys2026-96aca14d6c4dcd3adf54bc2c5ad7f138.html 迁移的资料快照；原始 HTML SHA-256: d071395db2ec0b2189478a2e26b56edb72e45ac02e12c5df8b60ea4d0a3afc68。 -->

[MLSys Proceedings](/)

- [](/admin/login/?next=/admin/)
- [](/admin/logout/?nextp=/admin)

Search

# When Machine Learning Isn’t Sure: Building Resilient ML-Based Computer Systems by Embracing Uncertainty

Varun Gohil, Nevena Stojkovic, Noman Bashir, Sundar Dev, Gaurang Upasani, David Lo, Parthasarathy Ranganathan, Christina Delimitrou

[Proceedings of Machine Learning and Systems 8 (MLSys 2026)](/paper_files/paper/2026) Conference

[Bibtex](/paper_files/paper/777-/bibtex) [Paper](/paper_files/paper/2026/file/96aca14d6c4dcd3adf54bc2c5ad7f138-Paper-Conference.pdf)

## Abstract

Machine learning (ML) models are increasingly used in computer systems but often suffer from poor generalizability, leading to costly failures on out-of-distribution (OOD) data. We propose an uncertainty-aware framework that improves system resilience by quantifying prediction uncertainty at runtime and rejecting unreliable outputs before they cause harm. When a prediction is uncertain, the system gracefully degrades to a safe fallback strategy. We evaluate the framework across three case studies, server provisioning, cluster management, and storage I/O admission, and find that the best uncertainty estimator is not universal but depends on how its properties align with each task’s design and resource constraints. Similarly, the optimal fallback workflow (e.g., a lightweight and parallel vs. resource-intensive and sequential ) depends on task’s runtime latency constraints. Together, these findings offer a practical path towards building more reliable ML-driven computer systems.

  

#### Name Change Policy

×

Requests for name changes in the electronic proceedings will be accepted with no questions asked. However name changes may cause bibliographic tracking issues. Authors are asked to consider this carefully and discuss it with their co-authors prior to requesting a name change in the electronic proceedings.

Use the "Report an Issue" link to request a name change.

[Report an Issue](https://mlsys.org/Help/Contact?select=Conference)    \|    [Name Change Policy](#)

Do not remove: This comment is monitored to verify that the site is working properly
