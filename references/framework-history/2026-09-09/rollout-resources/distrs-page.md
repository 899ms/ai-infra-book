<!-- 从 distrs-page.html 迁移的资料快照；原始 HTML SHA-256: d344033637fbb43d58c44c218edacce2a3a3bcbac7920693c71c830b73abe316。 -->

# DistRS: Disaggregated Reward Service for RLVR with Batch-Level Constraint

Ruidong Zhu, *School of Computer Science, Peking University;* Mingcong Han, *ByteDance Seed;* Yinmin Zhong, *School of Computer Science, Peking University;* Wencong Xiao, *ByteDance Seed;* Xuanzhe Liu and Xin Jin, *School of Computer Science, Peking University*

Reinforcement Learning with Verifiable Rewards (RLVR) has emerged as a key post-training paradigm for enhancing the capabilities of large language models (LLMs). As the complexity increases and resource consumption grows, reward computation is becoming a critical workload in the RLVR training process.

We present DistRS, a disaggregated reward service framework designed to provide resource-efficient reward computation for RLVR training. Through the analysis of a real RLVR training task, we observe that the reward service faces a highly dynamic workload, motivating the need for elasticity and multi-tenancy. DistRS leverages request-level flexibility from the *request-in, batch-out* characteristic of reward computation to design more resource-efficient scaling and scheduling policies. Specifically, DistRS establishes a batch-level constraint for each training task that relaxes latency requirements at the request level. Building on this foundation, we design a history-based resource scaling policy and a batch-level priority-based request scheduling policy. In addition, DistRS incorporates a timeout-aware mechanism to adjust resource allocation, thereby mitigating the impact of deviations between history and actual execution. We evaluate DistRS with real-world RLVR training tasks and the results demonstrate that DistRS reduces resource consumption by up to 3.79× while incurring minimal overhead on training progress.

NSDI '26 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {316770,  
author = {Ruidong Zhu and Mingcong Han and Yinmin Zhong and Wencong Xiao and Xuanzhe Liu and Xin Jin},  
title = {{DistRS}: Disaggregated Reward Service for {RLVR} with {Batch-Level} Constraint},  
booktitle = {23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI 26)},  
year = {2026},  
isbn = {978-1-939133-54-0},  
address = {Renton, WA},  
pages = {1517--1531},  
url = {https://www.usenix.org/conference/nsdi26/presentation/zhu-ruidong},  
publisher = {USENIX Association},  
month = may  
}  

[Download](/biblio/export/bibtex/316770)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Zhu PDF](https://www.usenix.org/system/files/nsdi26-zhu-ruidong.pdf "nsdi26-zhu-ruidong.pdf")

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-unlocked.png)

[View the slides](https://www.usenix.org/system/files/nsdi26_slides-zhu-ruidong.pdf)

## Presentation Video  
