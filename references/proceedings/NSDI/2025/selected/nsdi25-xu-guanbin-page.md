<!-- 从 nsdi25-xu-guanbin-page.html 迁移的资料快照；原始 HTML SHA-256: da5ce3597a16b36e48b2c156b9df065088232a6a0a26f557b0a31fb033c8a356。 -->

# AutoCCL: Automated Collective Communication Tuning for Accelerating Distributed and Parallel DNN Training

Guanbin Xu, Zhihao Le, Yinhe Chen, Zhiqi Lin, and Zewen Jin, *University of Science and Technology of China;* Youshan Miao, *Microsoft Research;* Cheng Li, *University of Science and Technology of China; Anhui Province Key Laboratory of Biomedical Imaging and Intelligent Processing; Institute of Artificial Intelligence, Hefei Comprehensive National Science Center*

The collective communication libraries are pivotal in optimizing the performance of distributed and parallel deep neural network (DNN) training. Most network optimizations are under the assumption that these libraries are well-tuned, ignoring their low-level parameter selection. In this paper, we present a novel automated tuning method AutoCCL that significantly improves communication performance without incurring additional costs. One of the primary challenges we tackle is the state explosion in searching for the optimal configuration. To overcome this, we decouple implementation-related parameters from those sensitive to the search space size and propose a divide-and-conquer algorithm, minimizing the requirement for exhaustive trials. We further propose an online tuning approach that accounts for communication-computation interference to enhance accuracy in finding optimal configurations, while hiding tuning overhead within early iterations of training jobs. We implement AutoCCL atop NCCL, a leading and widely-used communication library provided by NVIDIA. Our evaluation on both a 2-node cluster (16 A40 GPUs, intra-node NVLink, inter-node 2× 400Gbps InfiniBand) and a 4-node cluster (32 A40 GPUs, intra-node PCIe, inter-node 100Gbps InfiniBand) demonstrates that AutoCCL achieves 1.24-1.29× and 1.15-1.22× speedups on microbenchmarks compared to NCCL and another SOTA NCCL tuner, respectively, and up to 1.80× and 1.49× with concurrent computation. End-to-end evaluations on three large language models and one vision model show 1.07-1.32× improvements in periteration training time.

NSDI '25 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {305967,  
author = {Guanbin Xu and Zhihao Le and Yinhe Chen and Zhiqi Lin and Zewen Jin and Youshan Miao and Cheng Li},  
title = {{AutoCCL}: Automated Collective Communication Tuning for Accelerating Distributed and Parallel {DNN} Training},  
booktitle = {22nd USENIX Symposium on Networked Systems Design and Implementation (NSDI 25)},  
year = {2025},  
isbn = {978-1-939133-46-5},  
address = {Philadelphia, PA},  
pages = {667--683},  
url = {https://www.usenix.org/conference/nsdi25/presentation/xu-guanbin},  
publisher = {USENIX Association},  
month = apr  
}  

[Download](/biblio/export/bibtex/305967)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Xu PDF](https://www.usenix.org/system/files/nsdi25-xu-guanbin.pdf "nsdi25-xu-guanbin.pdf")

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-unlocked.png)

[View the slides](https://www.usenix.org/system/files/nsdi25_slides-xu-guanbin.pdf)

## Presentation Video  
