<!-- 从 saha24a.html 迁移的资料快照；原始 HTML SHA-256: 896bf905f1af2a16b5a9e5e41cce938c6ceadb38d180987b4c18e2cad5da5621。 -->

\[[edit](https://github.com/mlresearch/v235/edit/gh-pages/_posts/2024-07-08-saha24a.md)\]

# I/O Complexity of Attention, or How Optimal is FlashAttention?

Barna Saha, Christopher Ye

*Proceedings of the 41st International Conference on Machine Learning*, PMLR 235:43024-43042, 2024.

#### Abstract

Attention is at the heart of the popular Transformer architecture, yet suffers from quadratic time and memory complexity. In a recent significant development, FlashAttention shows that the I/O complexity of attention is the true bottleneck in scaling Transformers. Given two levels of memory hierarchy, a fast cache (e.g. GPU on-chip SRAM) where computation happens and a slow memory (e.g. GPU high-bandwidth memory) where the data resides, the I/O complexity measures the number of accesses to the slow memory. FlashAttention is an I/O-aware algorithm for self-attention that requires \$\frac{N^2d^2}{M}\$ I/O operations where \$N\$ is the dimension of the attention matrix, \$d\$ is the head-dimension and \$M\$ is the size of cache. Naturally, to further reduce the computational costs of Attention, the authors ask the question: is FlashAttention’s I/O complexity optimal for every value of \$M\$? We resolve the above question in its full generality by showing an I/O complexity lower bound that matches the upper bound provided by FlashAttention for any values of \$M \geq d^2\$ within any constant factors. Moreover, our lower bounds do not rely on using combinatorial matrix multiplication for computing the attention matrix: even if one uses fast matrix multiplication, the above I/O complexity bounds cannot be improved. Further, we give a better algorithm with lower I/O complexity for \$M \< d^2\$, and show that it is optimal for combinatorial algorithms. We do so by introducing a new communication complexity protocol for matrix compression, and connecting communication complexity to I/O complexity. We believe this connection could be of independent interest and will find more applications in proving I/O complexity lower bounds in future.

#### Cite this Paper

------------------------------------------------------------------------

BibTeX

`@InProceedings{pmlr-v235-saha24a, title = {{I}/{O} Complexity of Attention, or How Optimal is {F}lash{A}ttention?}, author = {Saha, Barna and Ye, Christopher}, booktitle = {Proceedings of the 41st International Conference on Machine Learning}, pages = {43024--43042}, year = {2024}, editor = {Salakhutdinov, Ruslan and Kolter, Zico and Heller, Katherine and Weller, Adrian and Oliver, Nuria and Scarlett, Jonathan and Berkenkamp, Felix}, volume = {235}, series = {Proceedings of Machine Learning Research}, month = {21--27 Jul}, publisher = {PMLR}, pdf = {https://raw.githubusercontent.com/mlresearch/v235/main/assets/saha24a/saha24a.pdf}, url = {https://proceedings.mlr.press/v235/saha24a.html}, abstract = {Attention is at the heart of the popular Transformer architecture, yet suffers from quadratic time and memory complexity. In a recent significant development, FlashAttention shows that the I/O complexity of attention is the true bottleneck in scaling Transformers. Given two levels of memory hierarchy, a fast cache (e.g. GPU on-chip SRAM) where computation happens and a slow memory (e.g. GPU high-bandwidth memory) where the data resides, the I/O complexity measures the number of accesses to the slow memory. FlashAttention is an I/O-aware algorithm for self-attention that requires $\frac{N^2d^2}{M}$ I/O operations where $N$ is the dimension of the attention matrix, $d$ is the head-dimension and $M$ is the size of cache. Naturally, to further reduce the computational costs of Attention, the authors ask the question: is FlashAttention’s I/O complexity optimal for every value of $M$? We resolve the above question in its full generality by showing an I/O complexity lower bound that matches the upper bound provided by FlashAttention for any values of $M \geq d^2$ within any constant factors. Moreover, our lower bounds do not rely on using combinatorial matrix multiplication for computing the attention matrix: even if one uses fast matrix multiplication, the above I/O complexity bounds cannot be improved. Further, we give a better algorithm with lower I/O complexity for $M < d^2$, and show that it is optimal for combinatorial algorithms. We do so by introducing a new communication complexity protocol for matrix compression, and connecting communication complexity to I/O complexity. We believe this connection could be of independent interest and will find more applications in proving I/O complexity lower bounds in future.} } `

Copy to Clipboard

Download

Endnote

`%0 Conference Paper %T I/O Complexity of Attention, or How Optimal is FlashAttention? %A Barna Saha %A Christopher Ye %B Proceedings of the 41st International Conference on Machine Learning %C Proceedings of Machine Learning Research %D 2024 %E Ruslan Salakhutdinov %E Zico Kolter %E Katherine Heller %E Adrian Weller %E Nuria Oliver %E Jonathan Scarlett %E Felix Berkenkamp %F pmlr-v235-saha24a %I PMLR %P 43024--43042 %U https://proceedings.mlr.press/v235/saha24a.html %V 235 %X Attention is at the heart of the popular Transformer architecture, yet suffers from quadratic time and memory complexity. In a recent significant development, FlashAttention shows that the I/O complexity of attention is the true bottleneck in scaling Transformers. Given two levels of memory hierarchy, a fast cache (e.g. GPU on-chip SRAM) where computation happens and a slow memory (e.g. GPU high-bandwidth memory) where the data resides, the I/O complexity measures the number of accesses to the slow memory. FlashAttention is an I/O-aware algorithm for self-attention that requires $\frac{N^2d^2}{M}$ I/O operations where $N$ is the dimension of the attention matrix, $d$ is the head-dimension and $M$ is the size of cache. Naturally, to further reduce the computational costs of Attention, the authors ask the question: is FlashAttention’s I/O complexity optimal for every value of $M$? We resolve the above question in its full generality by showing an I/O complexity lower bound that matches the upper bound provided by FlashAttention for any values of $M \geq d^2$ within any constant factors. Moreover, our lower bounds do not rely on using combinatorial matrix multiplication for computing the attention matrix: even if one uses fast matrix multiplication, the above I/O complexity bounds cannot be improved. Further, we give a better algorithm with lower I/O complexity for $M < d^2$, and show that it is optimal for combinatorial algorithms. We do so by introducing a new communication complexity protocol for matrix compression, and connecting communication complexity to I/O complexity. We believe this connection could be of independent interest and will find more applications in proving I/O complexity lower bounds in future. `

Copy to Clipboard

Download

APA

`Saha, B. & Ye, C.. (2024). I/O Complexity of Attention, or How Optimal is FlashAttention?. `*`Proceedings of the 41st International Conference on Machine Learning`*`, in `*`Proceedings of Machine Learning Research`*` 235:43024-43042 Available from https://proceedings.mlr.press/v235/saha24a.html. `

Copy to Clipboard

Download

------------------------------------------------------------------------

#### Related Material

- [Download PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/saha24a/saha24a.pdf)
- [OpenReview](https://openreview.net/forum?id=MdPBVWTfwG)
