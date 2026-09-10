<!-- 从 paper-091-author.html 迁移的资料快照；原始 HTML SHA-256: 6a32507bf6a4d9d57c20862b7df3ab6ddf9545890f5ee251449d0b7f35c6ecfa。 -->

# Search

[](#)

[Siyuan Chai](/)

[Siyuan Chai](/)

- [Home](/#about)
- [Publications](/#featured)
- [Teaching](/#teaching)
- [CV](/files/Siyuan_CV.pdf)
- [Misc](/#misc)

- [](#)
- [](#)
  [Light](#) [Dark](#) [Automatic](#)

# M5: Mastering Page Migration and Memory Management for CXL-based Tiered Memory Systems

Yan Sun, Jongyul Kim, Zeduo Yu, Jiyuan Zhang, [Siyuan Chai](/author/siyuan-chai/), Michael Jaemin Kim, Hwayong Nam, Jaehyun Park, Eojin Na, Yifan Yuan, Ren Wang, Jung Ho Ahn, Tianyin Xu, Nam Sung Kim

March 2025 [Memory system](/category/memory-system/)

[PDF](/files/publications/m5.pdf) [Code](https://github.com/ece-fast-lab/ASPLOS-2025-M5) [Slides](/files/publications/m5.pptx) [ASPLOS](https://dl.acm.org/doi/10.1145/3676641.3711999)

### Abstract

CXL has emerged as a promising memory interface that can cost-effectively expand the capacity and bandwidth of a memory system, complementing the traditional DDR interface. However, CXL DRAM presents 2–3× longer access latency than DDR DRAM, forming a tiered-memory system that demands an effective and efficient page-migration solution. Although many page-migration solutions have been proposed for past tiered-Memory system, they have achieved limited success. To tackle the challenge of managing tiered-memory systems, this work first presents a CXL-driven profiling solution to precisely and transparently count the number of accesses to every 4KB page and 64B word in CXL DRAM. Second, using the profiling solution, this work uncovers that (1) widely used CPU-driven page-migration solutions often identify warm pages as hot pages, and (2) certain applications have sparse hot pages, where only a small percentage of words in each of these pages are frequently accessed. Besides, this work demonstrates that the performance overhead of identifying hot pages is sometimes high enough to degrade application performance. Lastly, this work presents M5, a platform designed to facilitate the development of effective CXL-driven page-migration solutions, providing hardware-based hot-page and hot-word trackers in the CXL controller. On average, M5 can identify 47% hotter pages and offer 14% higher performance than the best CPU-driven page-migration solution, even with a simple policy.

Type

[Conference paper](/publication/#1)

Publication

Architectural Support for Programming Languages and Operating Systems

[Operating systems](/tag/operating-systems/) [Memory system](/tag/memory-system/)

- [](https://twitter.com/intent/tweet?url=https://schai.me/publication/m5/&text=M5:%20Mastering%20Page%20Migration%20and%20Memory%20Management%20for%20CXL-based%20Tiered%20Memory%20Systems)
- [](https://www.facebook.com/sharer.php?u=https://schai.me/publication/m5/&t=M5:%20Mastering%20Page%20Migration%20and%20Memory%20Management%20for%20CXL-based%20Tiered%20Memory%20Systems)
- [](mailto:?subject=M5:%20Mastering%20Page%20Migration%20and%20Memory%20Management%20for%20CXL-based%20Tiered%20Memory%20Systems&body=https://schai.me/publication/m5/)
- [](https://www.linkedin.com/shareArticle?url=https://schai.me/publication/m5/&title=M5:%20Mastering%20Page%20Migration%20and%20Memory%20Management%20for%20CXL-based%20Tiered%20Memory%20Systems)
- [](whatsapp://send?text=M5:%20Mastering%20Page%20Migration%20and%20Memory%20Management%20for%20CXL-based%20Tiered%20Memory%20Systems%20https://schai.me/publication/m5/)
- [](https://service.weibo.com/share/share.php?url=https://schai.me/publication/m5/&title=M5:%20Mastering%20Page%20Migration%20and%20Memory%20Management%20for%20CXL-based%20Tiered%20Memory%20Systems)

![Siyuan Chai](/author/siyuan-chai/avatar_huef588365b4002331fca8bcb1ae07649a_37203_270x270_fill_q90_lanczos_center.jpg)

##### [Siyuan Chai](https://schai.me)

###### CS PhD

- [](mailto:siyuanc3@illinois.edu)
- [](https://github.com/siyuanchai1999)
- [](https://scholar.google.com/citations?user=WL6lRZQAAAAJ&hl=en)
- [](https://www.linkedin.com/in/siyuan-chai/)
- [](https://x.com/SiyuanChai_)

### Related

- [Direct Memory Translation for Virtualized Clouds](/publication/dmt/)
- [EMT: An OS Framework for New Memory Translation Architectures](/publication/emt/)
- [CARAT CAKE: Replacing Paging via Compiler/Kernel Cooperation](/publication/karat/)

Last Updated on October 4, 2025

##### Cite

×

``` tex
```

[Copy](#) [Download](#)
