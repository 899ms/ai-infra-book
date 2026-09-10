<!-- 从 mlsys2025-e01c431bbb83153632c0dcfaf8ccda0a.html 迁移的资料快照；原始 HTML SHA-256: c6ad004b1e62563463353f848604b34c77a23bf3f6b332449cced4b1ff31b956。 -->

[MLSys Proceedings](/)

- [](/admin/login/?next=/admin/)
- [](/admin/logout/?nextp=/admin)

Search

# A Bring-Your-Own-Model Approach for ML-Driven Storage Placement in Warehouse-Scale Computers

Chenxi Yang, Yan Li, Martin Maas, Mustafa Uysal, Ubaid Ullah Hafeez, Arif Merchant, Richard McDougall

[Proceedings of Machine Learning and Systems 7 (MLSys 2025)](/paper_files/paper/2025) Conference

[Bibtex](/paper_files/paper/655-/bibtex) [Paper](/paper_files/paper/2025/file/e01c431bbb83153632c0dcfaf8ccda0a-Paper-Conference.pdf) [Supplemental](/paper_files/paper/2025/file/e01c431bbb83153632c0dcfaf8ccda0a-Supplemental-Conference.pdf)

## Abstract

Storage systems account for a major portion of the total cost of ownership (TCO) of warehouse-scale computers, and thus have a major impact on the overall system's efficiency. Machine learning (ML)-based methods for solving key problems in storage system efficiency, such as data placement, have shown significant promise. However, there are few known practical deployments of such methods. Studying this problem in the context of real-world hyperscale data centers at Google, we identify a number of challenges that we believe cause this lack of practical adoption. Specifically, prior work assumes a monolithic model that resides entirely within the storage layer, an unrealistic assumption in real-world deployments with frequently changing workloads. To address this problem, we introduce a cross-layer approach where workloads instead “bring their own model”. This strategy moves ML out of the storage system and instead allows each workload to train its own lightweight model at the application layer, capturing the workload's specific characteristics. These small, interpretable models generate predictions that guide a co-designed scheduling heuristic at the storage layer, enabling adaptation to diverse online environments. We build a proof-of-concept of this approach in a production distributed computation framework at Google. Evaluations in a test deployment and large-scale simulation studies using production traces show improvements of as much as 3.47\$\times\$ in TCO savings compared to state-of-the-art baselines.

  

#### Name Change Policy

×

Requests for name changes in the electronic proceedings will be accepted with no questions asked. However name changes may cause bibliographic tracking issues. Authors are asked to consider this carefully and discuss it with their co-authors prior to requesting a name change in the electronic proceedings.

Use the "Report an Issue" link to request a name change.

[Report an Issue](https://mlsys.org/Help/Contact?select=Conference)    \|    [Name Change Policy](#)

Do not remove: This comment is monitored to verify that the site is working properly
