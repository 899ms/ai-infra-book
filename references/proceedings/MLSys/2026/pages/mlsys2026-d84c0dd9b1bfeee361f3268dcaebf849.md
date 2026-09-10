<!-- 从 mlsys2026-d84c0dd9b1bfeee361f3268dcaebf849.html 迁移的资料快照；原始 HTML SHA-256: 92e64b1e46c0ba29ada0a7c4ec2da7c9aa6f1aafdc95720675f157bcc6d6bc4e。 -->

[MLSys Proceedings](/)

- [](/admin/login/?next=/admin/)
- [](/admin/logout/?nextp=/admin)

Search

# Cost-aware Duration Prediction for Software Upgrades in Datacenters

Yi Ding, Aijia Gao, Thibaud Ryden, Michal Sedlak, Essam Ewaisha, Igor Marnat, Henry Hoffmann

[Proceedings of Machine Learning and Systems 8 (MLSys 2026)](/paper_files/paper/2026) Conference

[Bibtex](/paper_files/paper/789-/bibtex) [Paper](/paper_files/paper/2026/file/d84c0dd9b1bfeee361f3268dcaebf849-Paper-Conference.pdf) [Supplemental](/paper_files/paper/2026/file/d84c0dd9b1bfeee361f3268dcaebf849-Supplemental-Conference.pdf)

## Abstract

Software upgrades are critical to maintaining server reliability in datacenters. While job duration prediction and scheduling have been extensively studied, the unique challenges posed by software upgrades remain largely under-explored. This paper presents the first in-depth investigation into software upgrade scheduling at datacenter scale. We begin by characterizing various types of upgrades and then frame the scheduling task as a constrained optimization problem. To address this problem, we introduce Acela, a cost-aware duration prediction framework designed to improve upgrade scheduling efficiency and throughput while meeting service-level objectives (SLOs). Acela accounts for asymmetric misprediction costs, strategically selects the best predictive models, and mitigates straggler-induced overestimations. Evaluations on Meta's production datacenter systems demonstrate that Acela significantly outperforms the existing upgrade scheduler by improving upgrade window utilization by 1.25x, increasing the number of scheduled and completed upgrades by 33% and 41%, and reducing cancellation rates by 2.4x. The code and data sets will be released after paper acceptance.

  

#### Name Change Policy

×

Requests for name changes in the electronic proceedings will be accepted with no questions asked. However name changes may cause bibliographic tracking issues. Authors are asked to consider this carefully and discuss it with their co-authors prior to requesting a name change in the electronic proceedings.

Use the "Report an Issue" link to request a name change.

[Report an Issue](https://mlsys.org/Help/Contact?select=Conference)    \|    [Name Change Policy](#)

Do not remove: This comment is monitored to verify that the site is working properly
