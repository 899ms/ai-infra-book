<!-- 从 osdi26-wu-tianyuan-page.html 迁移的资料快照；原始 HTML SHA-256: dd1381596035b8195702d039d31fe72775e588206d7c7be32d7e210c5b915f4f。 -->

# Weave: Efficient Co-Scheduling for Disaggregated RL Post-Training

Tianyuan Wu and Lunxi Cao, *Hong Kong University of Science and Technology;* Yining Wei, *University of Illinois Urbana–Champaign;* Wei Gao, Yuheng Zhao, and Dakai An, *Hong Kong University of Science and Technology;* Shaopan Xiong, Zhiqiang Lv, Ju Huang, Siran Yang, Yinghao Yu, Jiamang Wang, and Lin Qu, *Alibaba Group;* Wei Wang, *Hong Kong University of Science and Technology*

Rollout–training disaggregation is emerging as the standard architecture for Reinforcement Learning (RL) post-training, where memory-bound rollout and compute-bound training are physically disaggregated onto purpose-built clusters to maximize hardware efficiency. However, the strict synchronization required by on-policy algorithms introduces severe dependency bubbles, forcing one cluster to idle while the dependent phase is running on the other. We present WEAVE, a cluster scheduling framework that reclaims these bubbles through cross-cluster orchestration. WEAVE is built on the insight that the structural idleness of one job can be effectively utilized by the active phase of another. To realize this, we introduce the co-execution group abstraction, which partitions the cluster into isolated locality domains. This abstraction enables a two-tier scheduling architecture: an inter-group scheduler that optimizes job placement using conservative stochastic planning, and an intra-group scheduler that orchestrates a provably optimal round-robin schedule. The group abstraction also imposes a residency constraint, ensuring that massive model states remain cached in host memory to enable “warm-start” context switching. We evaluate WEAVE on a production-scale testbed with 328 H20 and 328 H800 GPUs. WEAVE improves cost efficiency by 1.84× over standard disaggregation and 1.38× over state-of-the-art co-located baselines, all while achieving 100% SLO attainment.

OSDI '26 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {318469,  
author = {Tianyuan Wu and Lunxi Cao and Yining Wei and Wei Gao and Yuheng Zhao and Dakai An and Shaopan Xiong and Zhiqiang Lv and Ju Huang and Siran Yang and Yinghao Yu and Jiamang Wang and Lin Qu and Wei Wang},  
title = {Weave: Efficient {Co-Scheduling} for Disaggregated {RL} {Post-Training}},  
booktitle = {20th USENIX Symposium on Operating Systems Design and Implementation (OSDI 26)},  
year = {2026},  
isbn = {978-1-939133-55-7},  
address = {Seattle, WA},  
pages = {809--827},  
url = {https://www.usenix.org/conference/osdi26/presentation/wu-tianyuan},  
publisher = {USENIX Association},  
month = jul  
}  

[Download](/biblio/export/bibtex/318469)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Wu PDF](https://www.usenix.org/system/files/osdi26-wu-tianyuan.pdf "osdi26-wu-tianyuan.pdf")

![](https://www.usenix.org/sites/default/files/usenix_2025_artifact_evaluation_available_125.png)
