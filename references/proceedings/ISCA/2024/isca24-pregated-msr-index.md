<!-- 从 isca24-pregated-msr-index.html 迁移的资料快照；原始 HTML SHA-256: 1876137cd8305ea9607eb07752246a42ab297601a82f4893ba6272844df7c136。 -->

# Pre-gated MoE: An Algorithm-System Co-Design for Fast and Scalable Mixture-of-Expert Inference

- Ranggi Hwang ,
- Jianyu Wei ,
- Shijie Cao ,
- [Changho Hwang](https://www.microsoft.com/en-us/research/people/changhohwang/) ,
- Xiaohu Tang ,
- Ting Cao ,
- Mao Yang

***ISCA 2024*** \| July 2024

Microsoft Research Focus https://www.microsoft.com/en-us/research/blog/research-focus-week-of-july-15-2024/

[Download BibTex](https://www.microsoft.com/en-us/research/publication/pre-gated-moe-an-algorithm-system-co-design-for-fast-and-scalable-mixture-of-expert-inference/bibtex/)

Large language models (LLMs) based on transformers have made significant strides in recent years, the success of which is driven by scaling up their model size. Despite their high algorithmic performance, the computational and memory requirements of LLMs present unprecedented challenges. To tackle the high compute requirements of LLMs, the Mixture-of-Experts (MoE) architecture was introduced which is able to scale its model size without proportionally scaling up its computational requirements. Unfortunately, MoE’s high memory demands and dynamic activation of sparse experts restrict its applicability to real-world problems. Previous solutions that offload MoE’s memory-hungry expert parameters to CPU memory fall short because the latency to migrate activated experts from CPU to GPU incurs high performance overhead. Our proposed Pre-gated MoE system effectively tackles the compute and memory challenges of conventional MoE architectures using our algorithm-system co-design. Pre-gated MoE employs our novel pre-gating function which alleviates the dynamic nature of sparse expert activation, allowing our proposed system to address the large memory footprint of MoEs while also achieving high performance. We demonstrate that Pre-gated MoE is able to improve performance, reduce GPU memory consumption, while also maintaining the same level of model quality. These features allow our Pre-gated MoE system to cost-effectively deploy large-scale LLMs using just a single GPU with high performance.

Opens in a new tab

[Publication](https://www.microsoft.com/en-us/research/wp-content/uploads/2024/05/isca24_pregated_moe_camera_ready.pdf)

## Blog & Podcasts

- [Research Focus: Week of July 15, 2024](https://www.microsoft.com/en-us/research/blog/research-focus-week-of-july-15-2024/)

## Groups

- [Systems and Networking Research Group (Asia)](https://www.microsoft.com/en-us/research/group/systems-and-networking-research-group-asia/)
- [Microsoft Research Asia – Vancouver](https://www.microsoft.com/en-us/research/group/microsoft-research-asia-vancouver/)

## Research Areas

- [Systems and networking](https://www.microsoft.com/en-us/research/research-area/systems-and-networking/)

## Research Labs

- [Microsoft Research Lab - Asia](https://www.microsoft.com/en-us/research/lab/microsoft-research-asia/)
- [微软亚洲研究院](https://www.microsoft.com/en-us/research/lab/microsoft-research-asia-zh-cn/)
