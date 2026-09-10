<!-- 从 osdi26-chen-zhenqian-page.html 迁移的资料快照；原始 HTML SHA-256: fdebc50b06d43f9f3121800764a02d688f5d05a8e96e83b7ac6838713940c0a5。 -->

# RobustRL: Role-Based Fault Tolerance System for RL Post-Training

Zhenqian Chen and Baoquan Zhong, *Zhejiang University;* Xiang Li, *unaffiliated;* Qing Dai, Xinkui Zhao, and Miao Ye, *Zhejiang University;* Ren Cheng, *unaffiliated;* Lufei Zhang, *State Key Laboratory of Mathematical Engineering and Advanced Computing, China;* Jianwei Yin, *Zhejiang University*

RL post-training for LLMs has been widely scaled to enhance reasoning and tool-using capabilities. However, RL post-training interleaves training and inference workloads, exposing the system to faults from both sides. Existing fault tolerance frameworks for LLMs target either training or inference, leaving the optimization potential in the asynchronous execution unexplored for RL. Our key insight is role-based fault isolation so the failure in one machine does not affect the others. We treat trainer, rollout, and other management roles in RL training as distinct distributed sub-tasks. Instead of restarting the entire task in pretrain robust system ByteRobust, we recover only the failed role and reconnect it to living ones, thereby eliminating the full-restart overhead including rollout replay and initialization delay.

We present RobustRL, the first comprehensive robust system to handle GPU machine errors for RL post-training ETTR (Effective Training Time Ratio) improvement via a *Detect-Restart-Reconnect* paradigm. (1) *Detect*. We implement role-aware monitoring to distinguish actual failures from role-specific behaviors to avoid the false positive and delayed detection. (2) *Restart*. For trainers, we implement a non-disruptive recovery where rollouts persist state and continue trajectory generation, while the trainer is rapidly restored via rollout warm standbys. For rollout, we perform isolated machine replacement without interrupting the RL task. (3) *Reconnect*. We replace static collective communication with dynamic, UCX-based (Unified Communication X) point-to-point communication, enabling immediate weight synchronization between recovered roles. In an RL training task on a 256-GPU cluster with Qwen3-8B-Math workload under 10% failure injection frequency, RobustRL can achieve an ETTR of over 80% compared with the 60% in ByteRobust and achieves 8.4%-17.4% faster in end-to-end training time.

OSDI '26 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {318529,  
author = {Zhenqian Chen and Baoquan Zhong and Xiang Li and Qing Dai and Xinkui Zhao and Miao Ye and Ren Cheng and Lufei Zhang and Jianwei Yin},  
title = {{RobustRL}: {Role-Based} Fault Tolerance System for {RL} {Post-Training}},  
booktitle = {20th USENIX Symposium on Operating Systems Design and Implementation (OSDI 26)},  
year = {2026},  
isbn = {978-1-939133-55-7},  
address = {Seattle, WA},  
pages = {1407--1424},  
url = {https://www.usenix.org/conference/osdi26/presentation/chen-zhenqian},  
publisher = {USENIX Association},  
month = jul  
}  

[Download](/biblio/export/bibtex/318529)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Chen PDF](https://www.usenix.org/system/files/osdi26-chen-zhenqian.pdf "osdi26-chen-zhenqian.pdf")
