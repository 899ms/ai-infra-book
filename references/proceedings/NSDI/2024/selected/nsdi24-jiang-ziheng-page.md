<!-- 从 nsdi24-jiang-ziheng-page.html 迁移的资料快照；原始 HTML SHA-256: 33e0a5c4eccbfd8911b3dc1da4208c602f60726ba854c247eab4c85a91d17f6f。 -->

# MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs

Ziheng Jiang and Haibin Lin, *ByteDance;* Yinmin Zhong, *Peking University;* Qi Huang, Yangrui Chen, Zhi Zhang, Yanghua Peng, Xiang Li, Cong Xie, Shibiao Nong, Yulu Jia, Sun He, Hongmin Chen, Zhihao Bai, Qi Hou, Shipeng Yan, Ding Zhou, Yiyao Sheng, Zhuo Jiang, Haohan Xu, Haoran Wei, Zhang Zhang, Pengfei Nie, Leqi Zou, Sida Zhao, Liang Xiang, Zherui Liu, Zhe Li, Xiaoying Jia, and Jianxi Ye, *ByteDance;* Xin Jin, *Peking University;* Xin Liu, *ByteDance*

We present the design, implementation and engineering experience in building and deploying MegaScale, a production system for training large language models (LLMs) at the scale of more than 10,000 GPUs. Training LLMs at this scale brings unprecedented challenges to training efficiency and stability. We take a full-stack approach that co-designs the algorithmic and system components across model block and optimizer design, computation and communication overlapping, operator optimization, data pipeline, and network performance tuning. Maintaining high efficiency throughout the training process (i.e., stability) is an important consideration in production given the long extent of LLM training jobs. Many hard stability issues only emerge at large scale, and in-depth observability is the key to address them. We develop a set of diagnosis tools to monitor system components and events deep in the stack, identify root causes, and derive effective techniques to achieve fault tolerance and mitigate stragglers. MegaScale achieves 55.2% Model FLOPs Utilization (MFU) when training a 175B LLM model on 12,288 GPUs, improving the MFU by 1.34x compared to Megatron-LM. We share our operational experience in identifying and fixing failures and stragglers. We hope by articulating the problems and sharing our experience from a systems perspective, this work can inspire future LLM systems research.

NSDI '24 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {295549,  
author = {Ziheng Jiang and Haibin Lin and Yinmin Zhong and Qi Huang and Yangrui Chen and Zhi Zhang and Yanghua Peng and Xiang Li and Cong Xie and Shibiao Nong and Yulu Jia and Sun He and Hongmin Chen and Zhihao Bai and Qi Hou and Shipeng Yan and Ding Zhou and Yiyao Sheng and Zhuo Jiang and Haohan Xu and Haoran Wei and Zhang Zhang and Pengfei Nie and Leqi Zou and Sida Zhao and Liang Xiang and Zherui Liu and Zhe Li and Xiaoying Jia and Jianxi Ye and Xin Jin and Xin Liu},  
title = {{MegaScale}: Scaling Large Language Model Training to More Than 10,000 {GPUs}},  
booktitle = {21st USENIX Symposium on Networked Systems Design and Implementation (NSDI 24)},  
year = {2024},  
isbn = {978-1-939133-39-7},  
address = {Santa Clara, CA},  
pages = {745--760},  
url = {https://www.usenix.org/conference/nsdi24/presentation/jiang-ziheng},  
publisher = {USENIX Association},  
month = apr  
}  

[Download](/biblio/export/bibtex/295549)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Jiang PDF](https://www.usenix.org/system/files/nsdi24-jiang-ziheng.pdf "nsdi24-jiang-ziheng.pdf")

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-unlocked.png)

[View the slides](https://www.usenix.org/system/files/nsdi24_slides-jiang_ziheng.pdf)

## Presentation Video  
