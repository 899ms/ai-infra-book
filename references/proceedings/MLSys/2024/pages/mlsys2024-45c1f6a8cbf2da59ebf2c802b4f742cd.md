<!-- 从 mlsys2024-45c1f6a8cbf2da59ebf2c802b4f742cd.html 迁移的资料快照；原始 HTML SHA-256: e7300e675743bdb81397c9a64806ed65015ca0fe8c43cbed07b8dc161554cc7a。 -->

[MLSys Proceedings](/)

- [](/admin/login/?next=/admin/)
- [](/admin/logout/?nextp=/admin)

Search

# DiffusionPipe: Training Large Diffusion Models with Efficient Pipelines

Ye Tian, Zhen Jia, Ziyue Luo, Yida Wang, Chuan Wu

[Proceedings of Machine Learning and Systems 6 (MLSys 2024)](/paper_files/paper/2024) Conference

[Bibtex](/paper_files/paper/598-/bibtex) [Paper](/paper_files/paper/2024/file/45c1f6a8cbf2da59ebf2c802b4f742cd-Paper-Conference.pdf) [Supplemental](/paper_files/paper/2024/file/45c1f6a8cbf2da59ebf2c802b4f742cd-Supplemental-Conference.pdf)

## Abstract

Diffusion models have emerged as dominant performers for image generation. To support training large diffusion models, this paper studies pipeline parallel training of diffusion models and proposes DiffusionPipe, a synchronous pipeline training system that advocates innovative pipeline bubble filling technique, catering to structural characteristics of diffusion models. State-of-the-art diffusion models typically include trainable (the backbone) and non-trainable (e.g., frozen input encoders) parts. We first unify optimal stage partitioning and pipeline scheduling of single and multiple backbones in representative diffusion models with a dynamic programming approach. We then propose to fill the computation of non-trainable model parts into idle periods of the pipeline training of the backbones by an efficient greedy algorithm, thus achieving high training throughput. Extensive experiments show that DiffusionPipe can achieve up to 1.41x speedup over pipeline parallel methods and 1.28x speedup over data parallel training on popular diffusion models.

  

#### Name Change Policy

×

Requests for name changes in the electronic proceedings will be accepted with no questions asked. However name changes may cause bibliographic tracking issues. Authors are asked to consider this carefully and discuss it with their co-authors prior to requesting a name change in the electronic proceedings.

Use the "Report an Issue" link to request a name change.

[Report an Issue](https://mlsys.org/Help/Contact?select=Conference)    \|    [Name Change Policy](#)

Do not remove: This comment is monitored to verify that the site is working properly
