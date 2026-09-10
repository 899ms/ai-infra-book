<!-- 从 167-iacr.html 迁移的资料快照；原始 HTML SHA-256: 10f99f9dab9587cea934fb139456518c087d85880aadd8c0038196ef8926ef06。 -->

#### Paper 2024/1862

### [BatchZK: A Fully Pipelined GPU-Accelerated System for Batch Generation of Zero-Knowledge Proofs](/2024/1862.pdf)

Tao Lu, Zhejiang University & National University of Singapore

Yuxun Chen, Zhejiang University

Zonghui Wang, Zhejiang University

Xiaohang Wang, Zhejiang University

Wenzhi Chen, Zhejiang University

Jiaheng Zhang, National University of Singapore

##### Abstract

Zero-knowledge proof (ZKP) is a cryptographic primitive that enables one party to prove the validity of a statement to other parties without disclosing any secret information. With its widespread adoption in applications such as blockchain and verifiable machine learning, the demand for generating zero-knowledge proofs has increased dramatically. In recent years, considerable efforts have been directed toward developing GPU-accelerated systems for proof generation. However, these previous systems only explored efficiently generating a single proof by reducing latency rather than batch generation to provide high throughput. We propose a fully pipelined GPU-accelerated system for batch generation of zero-knowledge proofs. Our system has three features to improve throughput. First, we design a pipelined approach that enables each GPU thread to continuously execute its designated proof generation task without being idle. Second, our system supports recent efficient ZKP protocols with their computational modules: sum-check protocol, Merkle tree, and linear-time encoder. We customize these modules to fit our pipelined execution. Third, we adopt a dynamic loading method for the data required for proof generation, reducing the required device memory. Moreover, multi-stream technology enables the overlap of data transfers and GPU computations, reducing overhead caused by data exchanges between host and device memory. We implement our system and evaluate it on various GPU cards. The results show that our system achieves more than 259.5× higher throughput compared to state-of-the-art GPU-accelerated systems. Moreover, we deploy our system in the verifiable machine learning application, where our system generates 9.52 proofs per second, successfully achieving sub-second proof generation for the first time in this field.

##### Metadata

Available format(s)  
[![](/img/file-pdf.svg)PDF](/2024/1862.pdf)

Category  
[Implementation](/search?category=IMPLEMENTATION)

Publication info  
Published elsewhere. Minor revision. ASPLOS 2025

Keywords  
[GPU](/search?q=GPU)[zero-knowledge proof](/search?q=zero-knowledge%20proof)[pipeline](/search?q=pipeline)[sumcheck protocol](/search?q=sumcheck%20protocol)[Merkle tree](/search?q=Merkle%20tree)[linear-time encoder](/search?q=linear-time%20encoder)

Contact author(s)  
lutao2020 @ zju edu cn  
chenyuxunzju @ zju edu cn  
zhwang @ zju edu cn  
xiaohangwang @ zju edu cn  
chenwz @ zju edu cn  
jhzhang @ nus edu sg

History  
2024-11-15: approved

2024-11-14: received

[See all versions](/archive/versions/2024/1862)

Short URL  
[https://ia.cr/2024/1862](https://ia.cr/2024/1862)

License  
[![Creative Commons Attribution](/img/license/CC_BY.svg "Creative Commons Attribution")  
CC BY](https://creativecommons.org/licenses/by/4.0/)

**BibTeX** ![](/img/copy-outline.svg)Copy to clipboard

```
@misc{cryptoeprint:2024/1862,
      author = {Tao Lu and Yuxun Chen and Zonghui Wang and Xiaohang Wang and Wenzhi Chen and Jiaheng Zhang},
      title = {{BatchZK}: A Fully Pipelined {GPU}-Accelerated System for Batch Generation of Zero-Knowledge Proofs},
      howpublished = {Cryptology {ePrint} Archive, Paper 2024/1862},
      year = {2024},
      url = {https://eprint.iacr.org/2024/1862}
}
```
