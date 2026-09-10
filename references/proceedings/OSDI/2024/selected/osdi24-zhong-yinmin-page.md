<!-- 从 osdi24-zhong-yinmin-page.html 迁移的资料快照；原始 HTML SHA-256: 369a902d19df5655e48f2c51c90a94cf9311c6017a8ac2814bba843f1af47bfb。 -->

# DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving

Yinmin Zhong and Shengyu Liu, *Peking University;* Junda Chen, *UC San Diego;* Jianbo Hu, *Peking University;* Yibo Zhu, *StepFun;* Xuanzhe Liu and Xin Jin, *Peking University;* Hao Zhang, *UC San Diego*

DistServe improves the performance of large language models (LLMs) serving by disaggregating the prefill and decoding computation. Existing LLM serving systems colocate the two phases and batch the computation of prefill and decoding across all users and requests. We find that this strategy not only leads to strong prefill-decoding interferences but also couples the resource allocation and parallelism plans for both phases. LLM applications often emphasize individual latency for each phase: time to first token (TTFT) for the prefill phase and time per output token (TPOT) of each request for the decoding phase. In the presence of stringent latency requirements, existing systems have to prioritize one latency over the other, or over-provision compute resources to meet both.

DistServe assigns prefill and decoding computation to different GPUs, hence eliminating prefill-decoding interferences. Given the application's TTFT and TPOT requirements, DistServe co-optimizes the resource allocation and parallelism strategy tailored for each phase. DistServe also places the two phases according to the serving cluster's bandwidth to minimize the communication caused by disaggregation. As a result, DistServe significantly improves LLM serving performance in terms of the maximum rate that can be served within both TTFT and TPOT constraints on each GPU. Our evaluations show that on various popular LLMs, applications, and latency requirements, DistServe can serve 7.4× more requests or 12.6× tighter SLO, compared to state-of-the-art systems, while staying within latency constraints for \> 90% of requests.

OSDI '24 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

BibTeX

@inproceedings {298687,  
author = {Yinmin Zhong and Shengyu Liu and Junda Chen and Jianbo Hu and Yibo Zhu and Xuanzhe Liu and Xin Jin and Hao Zhang},  
title = {{DistServe}: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving},  
booktitle = {18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24)},  
year = {2024},  
isbn = {978-1-939133-40-3},  
address = {Santa Clara, CA},  
pages = {193--210},  
url = {https://www.usenix.org/conference/osdi24/presentation/zhong-yinmin},  
publisher = {USENIX Association},  
month = jul  
}  

[Download](/biblio/export/bibtex/298687)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Zhong PDF](https://www.usenix.org/system/files/osdi24-zhong-yinmin.pdf "osdi24-zhong-yinmin.pdf")

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-unlocked.png)

[View the slides](https://www.usenix.org/system/files/osdi24_slides-zhong-yinmin.pdf)

![](https://www.usenix.org/sites/default/files/usenix_artifact_evaluation_available_125_update.png)

![](https://www.usenix.org/sites/default/files/usenix_artifact_evaluation_functional_125.png)

![](https://www.usenix.org/sites/default/files/usenix_artifact_evaluation_reproduced_125.png)

## Presentation Video  
