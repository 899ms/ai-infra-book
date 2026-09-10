<!-- 从 nsdi26-gao-wei-page.html 迁移的资料快照；原始 HTML SHA-256: 18ed4c7840924de2af67febbea586be48a9ddf983d146e3fbf0a285fc1212b21。 -->

# RollPacker: Taming Long-Tail Rollouts for RL Post-Training with Tail Batching

Wei Gao, Yuheng Zhao, Dakai An, Tianyuan Wu, and Lunxi Cao, *Hong Kong University of Science and Technology;* Shaopan Xiong, Ju Huang, Weixun Wang, Siran Yang, Wenbo Su, Jiamang Wang, Lin Qu, and Bo Zheng, *Alibaba Group;* Wei Wang, *Hong Kong University of Science and Technology*

Reinforcement Learning (RL) is a pivotal post-training technique for enhancing the reasoning capabilities of Large Language Models (LLMs). However, synchronous RL post‑training frequently suffers from significant GPU underutilization—often referred to as pipeline "bubbles"—caused by imbalanced response lengths within rollout steps. Many RL systems attempt to alleviate this problem by relaxing synchronization, but this can compromise training accuracy.

In this paper, we introduce tail batching, a novel rollout scheduling strategy for synchronous RL. Tail batching systematically consolidates prompts leading to long-tail responses into a few designated "long rounds", ensuring that the majority of rollout steps ("short rounds") contain only balanced, short responses. By strategically reordering execution, this approach dramatically reduces GPU idle time and accelerates RL training without sacrificing on-policy accuracy. We present RollPacker, a system that fully harnesses the benefits of tail batching through holistic optimizations across all three RL stages: elastic parallelism adaptation for rollout, dynamic resource allocation and scheduling for reward, and stream-based training. Cluster deployment on up to 128 H800 GPUs demonstrates that RollPacker achieves an end-to-end training speedup of 2.03× to 2.56× over veRL, and up to 2.24× speedup compared to RLHFuse across the Qwen2.5 family of LLMs. The code is available at [](https://github.com/Farrrrland/RollPacker)<https://github.com/Farrrrland/RollPacker>.

NSDI '26 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

BibTeX

@inproceedings {316604,  
author = {Wei Gao and Yuheng Zhao and Dakai An and Tianyuan Wu and Lunxi Cao and Shaopan Xiong and Ju Huang and Weixun Wang and Siran Yang and Wenbo Su and Jiamang Wang and Lin Qu and Bo Zheng and Wei Wang},  
title = {{RollPacker}: Taming {Long-Tail} Rollouts for {RL} {Post-Training} with Tail Batching},  
booktitle = {23rd USENIX Symposium on Networked Systems Design and Implementation (NSDI 26)},  
year = {2026},  
isbn = {978-1-939133-54-0},  
address = {Renton, WA},  
pages = {849--866},  
url = {https://www.usenix.org/conference/nsdi26/presentation/gao-wei},  
publisher = {USENIX Association},  
month = may  
}  

[Download](/biblio/export/bibtex/316604)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Gao PDF](https://www.usenix.org/system/files/nsdi26-gao-wei.pdf "nsdi26-gao-wei.pdf")

![](https://www.usenix.org/sites/default/files/usenix_2025_artifact_evaluation_available_125.png)

![](https://www.usenix.org/sites/default/files/usenix_2025_artifact_evaluation_functional_125.png)

## Presentation Video  
