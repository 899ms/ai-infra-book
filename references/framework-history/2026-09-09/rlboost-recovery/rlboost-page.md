<!-- 从 rlboost-page.html 迁移的资料快照；原始 HTML SHA-256: 1e742636f399dc58f5d52a3b69f405118935601de422101539fbeb70920c0f7c。 -->

# RLBoost: Harvesting Preemptible Cloud Resources for Cost-Efficient Reinforcement Learning on LLMs

Yongji Wu, *UC Berkeley;* Xueshen Liu, *University of Michigan;* Haizhong Zheng, *Carnegie Mellon University;* Juncheng Gu, *Google;* Beidi Chen, *Carnegie Mellon University;* Z. Morley Mao, *University of Michigan;* Arvind Krishnamurthy, *Google and University of Washington;* Ion Stoica, *UC Berkeley*

Reinforcement learning (RL) has become essential for unlocking advanced reasoning capabilities in large language models (LLMs). RL workflows involve interleaving rollout and training stages with fundamentally different resource requirements. Rollout typically dominates overall execution time, yet scales efficiently through multiple independent instances. In contrast, training requires tightly-coupled GPUs with full-mesh communication. Existing RL frameworks fall into two categories: co-located and disaggregated architectures. Co-located frameworks fail to address this resource tension by forcing both stages to share the same GPUs. Disaggregated architectures, without modifications of well-established RL algorithms, suffer from resource under-utilization. Meanwhile, preemptible GPU resources, i.e., spot instances on public clouds and spare capacity in production clusters, present significant cost-saving opportunities for accelerating RL workflows, if efficiently harvested for rollout.

In this paper, we present RLBoost, a framework for cost-efficient RL training that harvests preemptible GPU resources. Our key insight is that rollout's stateless and embarrassingly parallel nature aligns perfectly with preemptible and often fragmented resources. To efficiently utilize these resources despite frequent and unpredictable availability changes, RLBoost adopts a hybrid architecture with three key techniques: (1) adaptive rollout offload to dynamically adjust workloads on the reserved (on-demand) cluster, (2) pull-based weight transfer that quickly provisions newly available instances, and (3) token-level response collection and migration for efficient preemption handling and continuous load balancing. Extensive experiments show RLBoost increases training throughput by 1.51x-1.97x while improving cost efficiency by 28%-49% compared to using only on-demand GPU resources. RLBoost is open-sourced at <https://github.com/Terra-Flux/PolyRL>.

NSDI '26 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {316724,  
author = {Yongji Wu and Xueshen Liu and Haizhong Zheng and Juncheng Gu and Beidi Chen and Z. Morley Mao and Arvind Krishnamurthy and Ion Stoica},  
title = {{RLBoost}: Harvesting Preemptible Cloud Resources for {Cost-Efficient} Reinforcement Learning on {LLMs}},  
booktitle = {23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI 26)},  
year = {2026},  
isbn = {978-1-939133-54-0},  
address = {Renton, WA},  
pages = {1323--1339},  
url = {https://www.usenix.org/conference/nsdi26/presentation/wu-yongji},  
publisher = {USENIX Association},  
month = may  
}  

[Download](/biblio/export/bibtex/316724)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Wu PDF](https://www.usenix.org/system/files/nsdi26-wu-yongji.pdf "nsdi26-wu-yongji.pdf")

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-unlocked.png)

[View the slides](https://www.usenix.org/system/files/nsdi26_slides-wu-yongji.pdf)

![](https://www.usenix.org/sites/default/files/usenix_2025_artifact_evaluation_available_125.png)

![](https://www.usenix.org/sites/default/files/usenix_2025_artifact_evaluation_functional_125.png)

## Presentation Video  
