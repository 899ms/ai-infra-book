<!-- 从 nsdi24-de-sensi-page.html 迁移的资料快照；原始 HTML SHA-256: 5208bcca5b52bb48e4e5b47ea76ad15083980d62239b70c6aa5e34c83c2e4bc3。 -->

# Swing: Short-cutting Rings for Higher Bandwidth Allreduce

Daniele De Sensi, *Sapienza University of Rome;* Tommaso Bonato, *ETH Zurich;* David Saam, *RWTH Aachen University;* Torsten Hoefler, *ETH Zurich*

The allreduce collective operation accounts for a significant fraction of the runtime of workloads running on distributed systems. One factor determining its performance is the number of hops between communicating nodes, especially on networks like torus, where a higher number of hops implies multiple messages being forwarded on the same link, thus reducing the allreduce bandwidth. Torus networks are widely used on systems optimized for machine learning workloads (e.g., Google TPUs and Amazon Trainium devices), as well as on some of the Top500 supercomputers. To improve allreduce performance on torus networks we introduce Swing, a new algorithm that reduces the number of hops between communicating nodes by swinging between torus directions. Our analysis and experimental evaluation show that Swing outperforms by up to 3x existing allreduce algorithms for vectors ranging from 32B to 128MiB, on different types of torus and torus-like topologies, regardless of their shape and size.

NSDI '24 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {295653,  
author = {Daniele De Sensi and Tommaso Bonato and David Saam and Torsten Hoefler},  
title = {Swing: Short-cutting Rings for Higher Bandwidth Allreduce},  
booktitle = {21st USENIX Symposium on Networked Systems Design and Implementation (NSDI 24)},  
year = {2024},  
isbn = {978-1-939133-39-7},  
address = {Santa Clara, CA},  
pages = {1445--1462},  
url = {https://www.usenix.org/conference/nsdi24/presentation/de-sensi},  
publisher = {USENIX Association},  
month = apr  
}  

[Download](/biblio/export/bibtex/295653)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [De Sensi PDF](https://www.usenix.org/system/files/nsdi24-de-sensi.pdf "nsdi24-de-sensi.pdf")

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-unlocked.png)

[View the slides](https://www.usenix.org/system/files/nsdi24_slides-de_sensi.pdf)

## Presentation Video  
