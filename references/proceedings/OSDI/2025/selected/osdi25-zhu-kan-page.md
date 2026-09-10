<!-- 从 osdi25-zhu-kan-page.html 迁移的资料快照；原始 HTML SHA-256: 286c1530b5cb67d9b3ae03a50e05dcb72fe065f67d4a0a4a0119dc63581771c2。 -->

# NanoFlow: Towards Optimal Large Language Model Serving Throughput

Kan Zhu, *University of Washington;* Yufei Gao, *Tsinghua University and University of Washington;* Yilong Zhao, *University of Washington and University of California, Berkeley;* Liangyu Zhao, *University of Washington;* Gefei Zuo, *University of Michigan;* Yile Gu and Dedong Xie, *University of Washington;* Tian Tang and Qinyu Xu, *Tsinghua University and University of Washington;* Zihao Ye, Keisuke Kamahori, and Chien-Yu Lin, *University of Washington;* Ziren Wang, *Tsinghua University and University of Washington;* Stephanie Wang, Arvind Krishnamurthy, and Baris Kasikci, *University of Washington*

Large Language Models (LLMs) have resulted in a surging demand for planet-scale serving systems, where tens of thousands of GPUs continuously serve hundreds of millions of users. Consequently, throughput has emerged as a key metric that determines serving systems’ performance. Due to large model sizes and memory-intensive self-attention, LLM serving has been commonly assumed to be memory-bound. Through a detailed analysis, we show that despite having memory-intensive components, end-to-end LLM serving is compute bound for most common workloads and LLMs. Alas, most existing serving engines fall short from optimal compute utilization, because the heterogeneous operations that comprise LLM serving—compute, memory, networking—are executed sequentially within a device.

We propose NanoFlow, a novel serving framework that exploits intra-device parallelism, which overlaps the usage of heterogeneous resources within a single device. NanoFlow splits inputs into smaller nano-batches and duplicates operations to operate on each portion independently, enabling overlapping. NanoFlow automatically identifies the number, size, ordering, and GPU resource allocation of nano-batches to minimize the execution time, while considering the interference of concurrent operations. We evaluate NanoFlow's end-to-end serving throughput on several popular models such as LLaMA-2-70B, Mixtral 8×7B, LLaMA-3-8B, etc. With practical workloads, NanoFlow provides 1.91× throughput boost compared to state-of-the-art serving systems achieving 50% to 72 % of optimal throughput across popular models.

OSDI '25 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {308776,  
author = {Kan Zhu and Yufei Gao and Yilong Zhao and Liangyu Zhao and Gefei Zuo and Yile Gu and Dedong Xie and Zihao Ye and Keisuke Kamahori and Chien-Yu Lin and Ziren Wang and Stephanie Wang and Arvind Krishnamurthy and Baris Kasikci},  
title = {{NanoFlow}: Towards Optimal Large Language Model Serving Throughput},  
booktitle = {19th USENIX Symposium on Operating Systems Design and Implementation (OSDI 25)},  
year = {2025},  
isbn = {978-1-939133-47-2},  
address = {Boston, MA},  
pages = {749--765},  
url = {https://www.usenix.org/conference/osdi25/presentation/zhu-kan},  
publisher = {USENIX Association},  
month = jul  
}  

[Download](/biblio/export/bibtex/308776)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Zhu PDF](https://www.usenix.org/system/files/osdi25-zhu-kan.pdf "osdi25-zhu-kan.pdf")

![](https://www.usenix.org/sites/default/files/usenix_artifact_evaluation_available_125_update.png)

![](https://www.usenix.org/sites/default/files/usenix_artifact_evaluation_functional_125.png)

![](https://www.usenix.org/sites/default/files/usenix_artifact_evaluation_reproduced_125.png)

## Presentation Video  
