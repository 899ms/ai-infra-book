<!-- 从 nsdi24-hou-page.html 迁移的资料快照；原始 HTML SHA-256: 8e80fcb9a3610effdfd0438d61953855b22a4cf071e048401434eed73246c3e2。 -->

# Understanding Routable PCIe Performance for Composable Infrastructures

Wentao Hou, *University of Wisconsin-Madison;* Jie Zhang and Zeke Wang, *Zhejiang University;* Ming Liu, *University of Wisconsin-Madison*

Routable PCIe has become the predominant cluster interconnect to build emerging composable infrastructures. Empowered by PCIe non-transparent bridge devices, PCIe transactions can traverse multiple switching domains, enabling a server to elastically integrate a number of remote PCIe devices as local ones. However, it is unclear how to move data or perform communication efficiently over the routable PCIe fabric without understanding its capabilities and limitations.

This paper presents the design and implementation of **rPCIeBench**, a software-hardware co-designed benchmarking framework to systematically characterize the routable PCIe fabric. rPCIeBench provides flexible data communication primitives, exposes end-to-end PCIe transaction observability, and enables reconfigurable experiment deployment. Using rPCIeBench, we first analyze the communication characteristics of a routable PCIe path, quantify its performance tax, and compare it with the local PCIe link. We then use it to dissect in-fabric traffic orchestration behaviors and draw three interesting findings: approximate max-min bandwidth partition, fast end-to-end bandwidth synchronization, and interference-free among orthogonal data paths. Finally, we encode gathered characterization insights as traffic orchestration rules and develop an *edge constraints relaxing* algorithm to estimate PCIe flow transmission performance over a shared fabric. We validate its accuracy and demonstrate its potential to provide an optimization guide to design efficient flow schedulers.

NSDI '24 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {295503,  
author = {Wentao Hou and Jie Zhang and Zeke Wang and Ming Liu},  
title = {Understanding Routable {PCIe} Performance for Composable Infrastructures},  
booktitle = {21st USENIX Symposium on Networked Systems Design and Implementation (NSDI 24)},  
year = {2024},  
isbn = {978-1-939133-39-7},  
address = {Santa Clara, CA},  
pages = {297--312},  
url = {https://www.usenix.org/conference/nsdi24/presentation/hou},  
publisher = {USENIX Association},  
month = apr  
}  

[Download](/biblio/export/bibtex/295503)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Hou PDF](https://www.usenix.org/system/files/nsdi24-hou.pdf "nsdi24-hou.pdf")

## Presentation Video  
