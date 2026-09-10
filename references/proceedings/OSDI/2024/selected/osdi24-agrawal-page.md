<!-- 从 osdi24-agrawal-page.html 迁移的资料快照；原始 HTML SHA-256: bcf45bed5db54225305d085cffc1f9949197c8bf394069c6a7546c2a372e2ada。 -->

# Taming Throughput-Latency Tradeoff in LLM Inference with Sarathi-Serve

Amey Agrawal, *Georgia Institute of Technology;* Nitin Kedia, Ashish Panwar, Jayashree Mohan, Nipun Kwatra, and Bhargav Gulavani, *Microsoft Research India;* Alexey Tumanov, *Georgia Institute of Technology;* Ramachandran Ramjee, *Microsoft Research India*

Each LLM serving request goes through two phases. The first is prefill which processes the entire input prompt and produces the first output token and the second is decode which generates the rest of output tokens, one-at-a-time. Prefill iterations have high latency but saturate GPU compute due to parallel processing of the input prompt. In contrast, decode iterations have low latency but also low compute utilization because a decode iteration processes only a single token per request. This makes batching highly effective for decodes and consequently for overall throughput. However, batching multiple requests leads to an interleaving of prefill and decode iterations which makes it challenging to achieve both high throughput and low latency.

We introduce an efficient LLM inference scheduler, Sarathi-Serve, to address this throughput-latency tradeoff. Sarathi-Serve introduces chunked-prefills which splits a prefill request into near equal sized chunks and creates stall-free schedules that adds new requests in a batch without pausing ongoing decodes. Stall-free scheduling unlocks the opportunity to improve throughput with large batch sizes while minimizing the effect of batching on latency. Furthermore, uniform batches in Sarathi-Serve ameliorate the imbalance between iterations resulting in minimal pipeline bubbles.

Our techniques yield significant improvements in inference performance across models and hardware under tail latency constraints. For Mistral-7B on single A100 GPUs, we achieve 2.6x higher serving capacity and up to 3.7x higher serving capacity for the Yi-34B model on two A100 GPUs as compared to vLLM. When used with pipeline parallelism on Falcon-180B, Sarathi-Serve provides up to 5.6× gain in the end-to-end serving capacity. The source code for Sarathi-Serve is available at <https://github.com/microsoft/sarathi-serve>.

OSDI '24 Open Access Sponsored by  
King Abdullah University of Science and Technology (KAUST)

## Open Access Media

USENIX is committed to Open Access to the research presented at our events. Papers and proceedings are freely available to everyone once the event begins. Any video, audio, and/or slides that are posted after the event are also free and open to everyone. [Support USENIX](/annual-fund) and our commitment to Open Access.

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-locked.png)

### This content is available to:

- [Conference attendees](/conference/279015/registration/form)

BibTeX

@inproceedings {298679,  
author = {Amey Agrawal and Nitin Kedia and Ashish Panwar and Jayashree Mohan and Nipun Kwatra and Bhargav Gulavani and Alexey Tumanov and Ramachandran Ramjee},  
title = {Taming {Throughput-Latency} Tradeoff in {LLM} Inference with {Sarathi-Serve}},  
booktitle = {18th USENIX Symposium on Operating Systems Design and Implementation (OSDI 24)},  
year = {2024},  
isbn = {978-1-939133-40-3},  
address = {Santa Clara, CA},  
pages = {117--134},  
url = {https://www.usenix.org/conference/osdi24/presentation/agrawal},  
publisher = {USENIX Association},  
month = jul  
}  

[Download](/biblio/export/bibtex/298679)

![PDF icon](/core/modules/file/icons/application-pdf.png "application/pdf") [Agrawal PDF](https://www.usenix.org/system/files/osdi24-agrawal.pdf "osdi24-agrawal.pdf")

![](https://www.usenix.org/modules/custom/usenix_files/images/usenix-unlocked.png)

[View the slides](https://www.usenix.org/system/files/osdi24_slides-agrawal.pdf)

![](https://www.usenix.org/sites/default/files/usenix_artifact_evaluation_available_125_update.png)

![](https://www.usenix.org/sites/default/files/usenix_artifact_evaluation_functional_125.png)

![](https://www.usenix.org/sites/default/files/usenix_artifact_evaluation_reproduced_125.png)

## Presentation Video  
