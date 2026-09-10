<!-- 从 cambricon-c-author.html 迁移的资料快照；原始 HTML SHA-256: 16e31f9799c4a96ff72c86b23541b017f5db6849d64b5e19e643e99a8b2e8ad9。 -->

[Home](/en/) [Archives](/en/archives) [Tags](/en/tags) [About](/en/about/) [🌐中文](#)

[🌐中文](#)

-  [Home](/en/)
-  [Archives](/en/archives)
-  [Tags](/en/tags)
-  [About](/en/about/)

## Cambricon-C: Efficient 4-Bit Matrix Unit via Primitivization

2024-11-02 [paper](/en/categories/paper/) [conference](/en/categories/paper/conference/) [micro](/en/categories/paper/conference/micro/)

**目录**

[回到顶部](javascript:void(0);)

(ZH-EN Translation by DeepSeek-V3-0324)

With the rise of large language models, 4-bit quantized models have become the preferred choice for deployment due to computational and storage budget constraints. However, we observe that traditional computing architectures suffer from significant computational redundancy when handling low-precision matrix multiplication.  
We propose the Cambricon-C architecture, which aims to revolutionize the implementation of 4-bit matrix computation through an innovative **Primitivized Matrix Multiplication (PMM)** algorithm.

[![](/zh/images/10764444-fig-1-source-large.gif)](/zh/images/10764444-fig-1-source-large.gif)

An in-depth analysis of 4-bit matrix multiplication reveals astonishing redundancy: in the 4-bit quantized version of Llama2-7B, computing the activation value of a single output neuron requires 11,008 4-bit multiplications followed by accumulation. Since 4-bit data has at most 16 possible values, the pigeonhole principle dictates that over 97% of these multiplications must be repeated. Traditional matrix processors based on MAC units redundantly compute these identical products, resulting in enormous energy waste.

The PMM algorithm proposes: **By leveraging the inverse distributive property of multiply-accumulate operations, we first count the occurrences of each multiplication and then perform a unified weighted summation, significantly reducing computational intensity.**

1.  **Precomputation to Eliminate Redundant Multiplications**: Precompute all possible 4-bit product combinations (256 in total) as a lookup table. During actual computation, only table lookup is required instead of repeated calculations.
2.  **Reduced Addition Intensity**: Transform accumulation operations into incremental updates of 256 counters, replacing traditional adder trees with unary successor operations (i.e., counting), drastically cutting addition overhead.

[![](/zh/images/10764444-fig-4-source-large.gif)](/zh/images/10764444-fig-4-source-large.gif)

Based on the PMM algorithm, we designed the Cambricon-C architecture:

- **Quarter-Square Multiplication (QSM)**: We revisited the 19th-century quarter-square multiplication technique, reducing the number of counters from 256 to 29 (referred to as the “R29 scheme”), achieving an 8.6× improvement in area efficiency.
- **Ripple Counters**: Implemented counters using self-timed D flip-flop chains, reducing dynamic power by 51% compared to SRAM-based solutions.

[![](/zh/images/10764444-fig-5-source-large.gif)](/zh/images/10764444-fig-5-source-large.gif)

Experimental results show:

- A single PE achieves 1.97× higher energy efficiency than traditional MAC units.
- A full 32×32 array accelerator delivers a 1.25× end-to-end energy efficiency improvement for LLaMA2 inference.
- Performance advantages scale with matrix size.

[![](/zh/images/10764444-table-5-source-large.gif)](/zh/images/10764444-table-5-source-large.gif)

Cambricon-C pioneers a new paradigm of “primitivized computation”. By decomposing complex operations into fundamental counting operations, we redefine the efficiency limits of low-precision computing:  
The future efficiency of accelerators will no longer depend on intricate MAC unit designs but rather on holistic optimization of entire matrix operations.  
In the near future, we will publish more work on “primitivized computation”, continuing to drive innovation in the microarchitecture of deep learning processors. We welcome attention and collaboration from peers.

Published at MICRO 2024. \[[DOI](https://doi.org/10.1109/MICRO61859.2024.00047)\] \[[PDF](https://dl.yongwei.site/C.pdf)\]

[accelerator](/en/tags/accelerator/ "accelerator") [primitivization](/en/tags/primitivization/ "primitivization") [cambricon-family](/en/tags/cambricon-family/ "cambricon-family")

[ Automated Placement and Routing Tool for Standard CMOS Circuit Schematics Prev](/en/pnr-circuit-schematic/) [The Application of Skew Ternary Numbers in Gomoku AI Programs Next ](/en/applying-skew-numbers-in-gomoku/)

![Page Counter](/counter.png)

© [2026](https://github.com/cheesewafer)    [Yongwei](https://yongwei.site)   
[京ICP备2021029228号](https://beian.miit.gov.cn/) [![](/images/beian.png)京公网安备11010802037348号](http://www.beian.gov.cn/portal/registerSystemInfo?recordcode=11010802037348)

Powered by [Hexo](https://hexo.io) \| Theme - [Sky](https://github.com/iJinxin/hexo-theme-sky)
