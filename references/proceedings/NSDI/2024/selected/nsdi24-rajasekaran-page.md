<!-- 从 nsdi24-rajasekaran-page.html 迁移的资料快照；原始 HTML SHA-256: b5bb2e3429f479072ff9f308a34902012bec2ba27a0d53f0c57bd9427f3d9f2d。 -->

# CASSINI: Network-Aware Job Scheduling in Machine Learning Clusters

Sudarsanan Rajasekaran and Manya Ghobadi, *Massachusetts Institute of Technology;* Aditya Akella, *UT Austin*

We present CASSINI, a network-aware job scheduler for machine learning (ML) clusters. CASSINI introduces a novel geometric abstraction to consider the communication pattern of different jobs while placing them on network links. To do so, CASSINI uses an Affinity graph that finds a series of time-shift values to adjust the communication phases of a subset of jobs, such that the communication patterns of jobs sharing the same network link are interleaved with each other. Experiments with 13 common ML models on a 24-server testbed demonstrate that compared to the state-of-the-art ML schedulers, CASSINI improves the average and tail completion time of jobs by up to 1.6x and 2.5x, respectively. Moreover, we show that CASSINI reduces the number of ECN marked packets in the cluster by up to 33x.

NSDI '24 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

BibTeX

@inproceedings {295625,  
author = {Sudarsanan Rajasekaran and Manya Ghobadi and Aditya Akella},  
title = {{CASSINI}: {Network-Aware} Job Scheduling in Machine Learning Clusters},  
booktitle = {21st USENIX Symposium on Networked Systems Design and Implementation (NSDI 24)},  
year = {2024},  
isbn = {978-1-939133-39-7},  
address = {Santa Clara, CA},  
pages = {1403--1420},  
url = {https://www.usenix.org/conference/nsdi24/presentation/rajasekaran},  
publisher = {USENIX Association},  
month = apr  
}  

[Download](/biblio/export/bibtex/295625)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Rajasekaran PDF](https://www.usenix.org/system/files/nsdi24-rajasekaran.pdf "nsdi24-rajasekaran.pdf")

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Rajasekaran Paper (Prepublication) PDF](https://www.usenix.org/system/files/nsdi24spring_prepub_rajasekaran.pdf "nsdi24spring_prepub_rajasekaran.pdf")

## Presentation Video  
