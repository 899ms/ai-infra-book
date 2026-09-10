<!-- 从 osdi26-ghosh-page.html 迁移的资料快照；原始 HTML SHA-256: 332e0363124e77004d77653820842d124c52f0401adceaabd37b78716716ec41。 -->

# GraCE: Unlocking CUDA Graphs with Compiler Support for ML Workloads

Abhishek Ghosh and Ajay Nayak, *Indian Institute of Science;* Ashish Panwar, *Microsoft Research;* Arkaprava Basu, *Indian Institute of Science*

Machine learning (ML) workloads launch hundreds of short-running GPU kernels per iteration. With GPU compute throughput growing rapidly, CPU-side launch latency of kernels is emerging as a bottleneck. CUDA Graphs promise to address this by replaying a set of kernels with a single dispatch of the graph, removing per-kernel launch costs. However, CUDA Graphs remain surprisingly difficult to deploy correctly and efficiently.

We present GraCE—a compiler framework to maximize the coverage and benefits of CUDA Graphs for ML workloads. It introduces three novel optimizations: it applies automatic code transformations to make ML applications amenable for CUDA Graphs; it eliminates the parameter copy overheads for kernels executing in CUDA Graphs, and it selectively deploys CUDA Graphs guided by a cost–benefit analysis. For 25 ML workloads from TorchBench, HuggingFace and TIMM, GraCE more than doubles the benefit from deploying CUDA Graph compared to the most popular and widely used ML compiler PyTorch2. GraCE is built atop PyTorch2’s compilation framework and requires no programmer intervention.

OSDI '26 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {318587,  
author = {Abhishek Ghosh and Ajay Nayak and Ashish Panwar and Arkaprava Basu},  
title = {{GraCE}: Unlocking {CUDA} Graphs with Compiler Support for {ML} Workloads},  
booktitle = {20th USENIX Symposium on Operating Systems Design and Implementation (OSDI 26)},  
year = {2026},  
isbn = {978-1-939133-55-7},  
address = {Seattle, WA},  
pages = {1927--1947},  
url = {https://www.usenix.org/conference/osdi26/presentation/ghosh},  
publisher = {USENIX Association},  
month = jul  
}  

[Download](/biblio/export/bibtex/318587)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Ghosh PDF](https://www.usenix.org/system/files/osdi26-ghosh.pdf "osdi26-ghosh.pdf")

![](https://www.usenix.org/sites/default/files/usenix_2025_artifact_evaluation_available_125.png)
