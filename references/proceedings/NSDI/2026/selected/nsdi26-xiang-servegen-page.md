<!-- 从 nsdi26-xiang-servegen-page.html 迁移的资料快照；原始 HTML SHA-256: b35bf147121d596e4b7ad3b29e4246284fc25185ca188cf341808f4ad96464d3。 -->

# ServeGen: Workload Characterization and Generation of Large Language Model Serving in Production

Yuxing Xiang, *Peking University and Alibaba Group;* Xue Li and Kun Qian, *Alibaba Group;* Yan Zhang, *Peking University;* Wenyuan Yu and Ennan Zhai, *Alibaba Group;* Xin Jin, *Peking University;* Jingren Zhou, *Alibaba Group*

With the widespread adoption of Large Language Models (LLMs), serving LLM inference requests has become an increasingly important task, attracting active research advancements. Practical workloads play an essential role in this process: they are critical for motivating and benchmarking serving techniques and systems. However, the existing understanding of real-world LLM serving workloads is limited due to the lack of a comprehensive workload characterization. Prior analyses remain insufficient in scale and scope, thus failing to fully capture intricate workload characteristics.

In this paper, we fill the gap with an in-depth characterization of LLM serving workloads collected from our worldwide cloud LLM serving service, covering not only language models but also emerging *multimodal* and *reasoning* models, unveiling important *new* findings in each case. Moreover, based on our findings, we propose ServeGen, a principled framework for generating realistic LLM serving workloads by composing them on a per-client basis. Practical use cases validate that ServeGen achieves more accurate performance benchmarking compared to naive workload generation, and reveals new design implications that could otherwise be overlooked. ServeGen is open-sourced at <https://github.com/alibaba/ServeGen>.

NSDI '26 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {316730,  
author = {Yuxing Xiang and Xue Li and Kun Qian and Yan Zhang and Wenyuan Yu and Ennan Zhai and Xin Jin and Jingren Zhou},  
title = {{ServeGen}: Workload Characterization and Generation of Large Language Model Serving in Production},  
booktitle = {23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI 26)},  
year = {2026},  
isbn = {978-1-939133-54-0},  
address = {Renton, WA},  
pages = {1845--1859},  
url = {https://www.usenix.org/conference/nsdi26/presentation/xiang-servegen},  
publisher = {USENIX Association},  
month = may  
}  

[Download](/biblio/export/bibtex/316730)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Xiang PDF](https://www.usenix.org/system/files/nsdi26-xiang-servegen.pdf "nsdi26-xiang-servegen.pdf")

![](https://www.usenix.org/sites/default/files/usenix_2025_artifact_evaluation_available_125.png)

![](https://www.usenix.org/sites/default/files/usenix_2025_artifact_evaluation_functional_125.png)

![](https://www.usenix.org/sites/default/files/usenix_2025_artifact_evaluation_reproduced_125.png)

## Presentation Video  
