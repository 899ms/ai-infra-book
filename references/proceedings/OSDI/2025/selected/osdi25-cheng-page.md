<!-- 从 osdi25-cheng-page.html 迁移的资料快照；原始 HTML SHA-256: 2544184073485c209b4ac00ed47465f80ac3a32359b96198e6d9295bc9e6be6d。 -->

# PipeThreader: Software-Defined Pipelining for Efficient DNN Execution

Yu Cheng, Lei Wang, and Yining Shi, *School of Computer Science, Peking University;* Yuqing Xia, Lingxiao Ma, Jilong Xue, and Yang Wang, *Microsoft Research;* Zhiwen Mo, *Imperial College London and Microsoft Research;* Feiyang Chen, *Shanghai Jiao Tong University and Microsoft Research;* Fan Yang and Mao Yang, *Microsoft Research;* Zhi Yang, *School of Computer Science, Peking University*

To effectively utilize heterogeneous specialized hardware units in modern GPUs, such as TensorCores and Tensor Memory Accelerators, this paper introduces PipeThreader, a new DNN compiler. PipeThreader proposes shifting scheduling functionality from hardware to software so as to enable more efficient and sophisticated computation pipelining with minimal manual effort. This is achieved through sTask-graph, a new DNN computation abstraction, a hierarchical hardware abstraction that captures the capabilities of specialized units, and new scheduling primitives. As a result, PipeThreader can discover efficient pipeline scheduling for well-studied DNN architectures like FlashAttention, achieving comparable or even superior performance. Additionally, it can uncover novel pipeline schemes for emerging models like Mamba2, delivering significantly better performance compared to state-of-the-art hand-crafted implementations. The code is open-sourced at <https://github.com/tile-ai/tilelang>.

OSDI '25 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {308778,  
author = {Yu Cheng and Lei Wang and Yining Shi and Yuqing Xia and Lingxiao Ma and Jilong Xue and Yang Wang and Zhiwen Mo and Feiyang Chen and Fan Yang and Mao Yang and Zhi Yang},  
title = {{PipeThreader}: {Software-Defined} Pipelining for Efficient {DNN} Execution},  
booktitle = {19th USENIX Symposium on Operating Systems Design and Implementation (OSDI 25)},  
year = {2025},  
isbn = {978-1-939133-47-2},  
address = {Boston, MA},  
pages = {767--783},  
url = {https://www.usenix.org/conference/osdi25/presentation/cheng},  
publisher = {USENIX Association},  
month = jul  
}  

[Download](/biblio/export/bibtex/308778)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Cheng PDF](https://www.usenix.org/system/files/osdi25-cheng.pdf "osdi25-cheng.pdf")

[View the slides](https://www.usenix.org/sites/default/files/conference/protected-files/osdi25_slides_cheng_yu.pdf)

## Presentation Video  
