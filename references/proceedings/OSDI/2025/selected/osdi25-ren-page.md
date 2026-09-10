<!-- 从 osdi25-ren-page.html 迁移的资料快照；原始 HTML SHA-256: b0f51bdc816d8cd5a29b058ae7cd00d98800d2b950f877d1ee606073c3aaf5d2。 -->

# Enabling Efficient GPU Communication over Multiple NICs with FuseLink

Zhenghang Ren, Yuxuan Li, Zilong Wang, Xinyang Huang, Wenxue Li, Kaiqiang Xu, Xudong Liao, Yijun Sun, and Bowen Liu, *Hong Kong University of Science and Technology;* Han Tian, *University of Science and Technology of China;* Junxue Zhang, *Hong Kong University of Science and Technology;* Mingfei Wang, *MetaX Integrated Circuits;* Zhizhen Zhong, *Massachusetts Institute of Technology;* Guyue Liu, *Peking University;* Ying Zhang, *Meta;* Kai Chen, *Hong Kong University of Science and Technology*

Machine learning (ML) clusters stack multiple network interface cards (NICs) within each server to improve inter-server GPU communication bandwidth. However, existing systems fall short in fully utilizing NICs because of static GPU-NIC bindings. This leads to bottlenecks at hot-spot NICs when handling imbalanced communication in ML tasks. For example, large language model serving instances may have different communication demands across NICs; expert-parallel training tasks have imbalanced all-to-all traffic; and the embedding transmission volumes during recommendation model training vary across GPUs. To fully utilize all NICs, we propose FuseLink to enable efficient GPU communication over multiple NICs. FuseLink extends inter-server network by integrating high-speed intra-server connections, and leverages GPUs to efficiently relay traffic to idle NICs. We implement FuseLink and integrate it into NCCL, so that ML applications can benefit from FuseLink seamlessly without code modifications. Compared to NCCL, we demonstrate that FuseLink achieves up to 212GBps bandwidth between two inter-server GPUs and accelerates ML tasks with dynamic traffic patterns. Specifically, it reduces the latencies of first-token generation in LLM model servings by 1.04-2.73×, improves the training throughput of mixture-of-experts model by up to 1.3×, and accelerates deep learning recommendation model training by up to 1.2×.

OSDI '25 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {308750,  
author = {Zhenghang Ren and Yuxuan Li and Zilong Wang and Xinyang Huang and Wenxue Li and Kaiqiang Xu and Xudong Liao and Yijun Sun and Bowen Liu and Han Tian and Junxue Zhang and Mingfei Wang and Zhizhen Zhong and Guyue Liu and Ying Zhang and Kai Chen},  
title = {Enabling Efficient {GPU} Communication over Multiple {NICs} with {FuseLink}},  
booktitle = {19th USENIX Symposium on Operating Systems Design and Implementation (OSDI 25)},  
year = {2025},  
isbn = {978-1-939133-47-2},  
address = {Boston, MA},  
pages = {91--108},  
url = {https://www.usenix.org/conference/osdi25/presentation/ren},  
publisher = {USENIX Association},  
month = jul  
}  

[Download](/biblio/export/bibtex/308750)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Ren PDF](https://www.usenix.org/system/files/osdi25-ren.pdf "osdi25-ren.pdf")

![](https://www.usenix.org/sites/default/files/usenix_artifact_evaluation_available_125_update.png)

## Presentation Video  
