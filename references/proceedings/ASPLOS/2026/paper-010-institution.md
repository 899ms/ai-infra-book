<!-- 从 paper-010-institution.html 迁移的资料快照；原始 HTML SHA-256: dddab02ca25290b617f5ff0b8ddff8cdac6e5f4970fa920f70cb28ce6ee7883c。 -->

# MoE-APEX: An Efficient MoE Inference System with Adaptive Precision Expert Offloading

Peng Tang

, Jiacheng Liu

, Xiaofeng Hou

, Yifei Pu

, Jing Wang

, [Pheng Ann Heng](https://research.cuhk.edu.hk/en/persons/pheng-ann-heng/)

, Chao Li

, Minyi Guo

- [Department of Computer Science and Engineering](https://research.cuhk.edu.hk/en/organisations/department-of-computer-science-and-engineering/)

- Shanghai Jiaotong University, Shanghai
- Shanghai Jiao Tong University
- Shanghai Jiao Tong University
- Shanghai Jiaotong University, Shanghai

Research output: Chapters and Conference Papers with Proceedings › Conference paper published in conference proceedings › Academic research › peer-review

- [ Overview ](/en/publications/moe-apex-an-efficient-moe-inference-system-with-adaptive-precisio/)
- [ Projects (1) ](/en/publications/moe-apex-an-efficient-moe-inference-system-with-adaptive-precisio/projects/)

## Abstract

Mixture-of-experts (MoE) architectures enable scalable Large Language Models (LLMs) with reduced computational overhead, yet their deployment on memory-constrained edge devices is hindered by substantial memory demands. Traditional expert-offloading techniques mitigate memory constraints but often significantly increase inference latency. We introduce MoE-APEX, an Adaptive Precision EXpert offloading system that optimizes MoE inference for edge architectures by dynamically managing expert precision. Our core innovation is to replace less critical cache-miss experts with low-precision variants, reducing loading latency while maintaining accuracy. MoE-APEX introduces three innovative techniques that map the natural hierarchy of MoE computation: (1) a token-level dynamic expert loading mechanism, (2) a layer-level adaptive expert prefetching technique, and (3) a sequence-level cost-aware expert caching policy. These innovations enable MoE-APEX to leverage the benefits of mixed-precision expert inference fully. Implemented atop Llama.cpp, MoE-APEX achieves decoding speedups ranging from 1.34x to 9.75x compared to state-of-the-art MoE offloading systems across diverse edge devices, offering a robust solution for efficient MoE deployment in resource-constrained environments.

[TABLE]

### Conference

|  |  |
|----|----|
| Conference | ASPLOS '26: 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systems |
| Country/Territory | United States |
| City | Pittsburgh |
| Period | 22/03/26 → 26/03/26 |

## Access to Document

- [10.1145/3779212.3790187](https://doi.org/10.1145/3779212.3790187)Licence: [CC BY](http://creativecommons.org/licenses/by/4.0/)

##   Projects 

- [ 1 ](/en/publications/moe-apex-an-efficient-moe-inference-system-with-adaptive-precisio/projects/?status=RUNNING) Active

Projects per year

- ### [Institute of Medical Intelligence and XR](https://research.cuhk.edu.hk/en/projects/institute-of-medical-intelligence-and-xr/)

  Zhou, J. (Collaborator), YU, C. H. (CoPI), [DOU, Q.](https://research.cuhk.edu.hk/en/persons/qi-dou/) (CoPI), [FU, C. W.](https://research.cuhk.edu.hk/en/persons/chi-wing-fu/) (CoPI), [WANG, L.](https://research.cuhk.edu.hk/en/persons/liwei-wang/) (CoPI), WONG, T. T. (CoPI), [CHAN, L. S.](https://research.cuhk.edu.hk/en/persons/lam-stephen-chan/) (CoPI), [CHENG, S. S.](https://research.cuhk.edu.hk/en/persons/shing-shin-cheng/) (CoPI), SHI, L. (CoPI), [SO, T. Y. T.](https://research.cuhk.edu.hk/en/persons/tiffany-yuen-tung-so/) (CoPI), CHIU, K. F. P. (CoPI), [NG, C. F.](https://research.cuhk.edu.hk/en/persons/chi-fai-ng/) (CoPI), NG, K. C. K. (CoPI), [TEOH, Y. C. J.](https://research.cuhk.edu.hk/en/persons/yuen-chun-jeremy-teoh/) (CoPI), [LI, H.](https://research.cuhk.edu.hk/en/persons/hongsheng-li/) (CoPI), [CHEN, W.](https://research.cuhk.edu.hk/en/persons/weitian-chen/) (CoPI), GU, J. (CoPI), [CHU, C. W. W.](https://research.cuhk.edu.hk/en/persons/chiu-wing-winnie-chu/) (CoPI), [HENG, P. A.](https://research.cuhk.edu.hk/en/persons/pheng-ann-heng/) (PC), CHEN, H. (CoPI), Cheng, T. K. T. (CoPI), Chung, A.C.-S. (CoPI), Li, X. (CoPI), QIN, J. (CoPI), Shum, D. (CoPI), Yin, G. (CoPI), YU, L. (CoPI), HSIAO, J.H.-W. (CoPI), Xing, L. (Collaborator), Rueckert, D. (Collaborator), Glocker, B. (Collaborator), Jannin, P. (Collaborator), Cai, W. (Collaborator), Zhou, J. (Collaborator), Si, W. (Collaborator), ZHAO, S. (Collaborator), CHO, C. M. C. (CoPI), CAI, J. (CoPI) & Ni, D. (Collaborator)

  [Research Grants Council (RGC)](#), [CUHK Matching Fund](#)

  1/01/23 → 31/12/27

  Project: Research

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Tang, P., Liu, J., Hou, X., Pu, Y., Wang, J.[, Heng, P. A.](https://research.cuhk.edu.hk/en/persons/pheng-ann-heng/), Li, C., & Guo, M. (2026). [MoE-APEX: An Efficient MoE Inference System with Adaptive Precision Expert Offloading](https://research.cuhk.edu.hk/en/publications/moe-apex-an-efficient-moe-inference-system-with-adaptive-precisio/). In *ASPLOS '26: Proceedings of the 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systemsctural Support for Programming Languages and Operating Systems* (Vol. 2, pp. 1185-1200). Association for Computing Machinery. [https://doi.org/10.1145/3779212.3790187](https://doi.org/10.1145/3779212.3790187)

Tang, Peng ; Liu, Jiacheng ; Hou, Xiaofeng et al. / [**MoE-APEX : An Efficient MoE Inference System with Adaptive Precision Expert Offloading**](https://research.cuhk.edu.hk/en/publications/moe-apex-an-efficient-moe-inference-system-with-adaptive-precisio/). ASPLOS '26: Proceedings of the 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systemsctural Support for Programming Languages and Operating Systems. Vol. 2 Association for Computing Machinery, 2026. pp. 1185-1200

@inproceedings{1aa2462718544c8c8a87ef6d3fe86372,

title = "MoE-APEX: An Efficient MoE Inference System with Adaptive Precision Expert Offloading",

abstract = "Mixture-of-experts (MoE) architectures enable scalable Large Language Models (LLMs) with reduced computational overhead, yet their deployment on memory-constrained edge devices is hindered by substantial memory demands. Traditional expert-offloading techniques mitigate memory constraints but often significantly increase inference latency. We introduce MoE-APEX, an Adaptive Precision EXpert offloading system that optimizes MoE inference for edge architectures by dynamically managing expert precision. Our core innovation is to replace less critical cache-miss experts with low-precision variants, reducing loading latency while maintaining accuracy. MoE-APEX introduces three innovative techniques that map the natural hierarchy of MoE computation: (1) a token-level dynamic expert loading mechanism, (2) a layer-level adaptive expert prefetching technique, and (3) a sequence-level cost-aware expert caching policy. These innovations enable MoE-APEX to leverage the benefits of mixed-precision expert inference fully. Implemented atop Llama.cpp, MoE-APEX achieves decoding speedups ranging from 1.34x to 9.75x compared to state-of-the-art MoE offloading systems across diverse edge devices, offering a robust solution for efficient MoE deployment in resource-constrained environments.",

author = "Peng Tang and Jiacheng Liu and Xiaofeng Hou and Yifei Pu and Jing Wang and Heng, \\Pheng Ann\\ and Chao Li and Minyi Guo",

year = "2026",

month = mar,

day = "22",

doi = "10.1145/3779212.3790187",

language = "English",

volume = "2",

pages = "1185--1200",

booktitle = "ASPLOS '26: Proceedings of the 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systemsctural Support for Programming Languages and Operating Systems",

publisher = "Association for Computing Machinery",

address = "United States",

note = "ASPLOS '26: 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systems ; Conference date: 22-03-2026 Through 26-03-2026",

}

Tang, P, Liu, J, Hou, X, Pu, Y, Wang, J[, Heng, PA](https://research.cuhk.edu.hk/en/persons/pheng-ann-heng/), Li, C & Guo, M 2026, [MoE-APEX: An Efficient MoE Inference System with Adaptive Precision Expert Offloading](https://research.cuhk.edu.hk/en/publications/moe-apex-an-efficient-moe-inference-system-with-adaptive-precisio/). in *ASPLOS '26: Proceedings of the 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systemsctural Support for Programming Languages and Operating Systems.* vol. 2, Association for Computing Machinery, pp. 1185-1200, ASPLOS '26: 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Pittsburgh, Pennsylvania, United States, 22/03/26. [https://doi.org/10.1145/3779212.3790187](https://doi.org/10.1145/3779212.3790187)

[**MoE-APEX: An Efficient MoE Inference System with Adaptive Precision Expert Offloading.**](https://research.cuhk.edu.hk/en/publications/moe-apex-an-efficient-moe-inference-system-with-adaptive-precisio/) / Tang, Peng; Liu, Jiacheng; Hou, Xiaofeng et al.  
ASPLOS '26: Proceedings of the 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systemsctural Support for Programming Languages and Operating Systems. Vol. 2 Association for Computing Machinery, 2026. p. 1185-1200.

Research output: Chapters and Conference Papers with Proceedings › Conference paper published in conference proceedings › Academic research › peer-review

TY - GEN

T1 - MoE-APEX

T2 - ASPLOS '26: 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systems

AU - Tang, Peng

AU - Liu, Jiacheng

AU - Hou, Xiaofeng

AU - Pu, Yifei

AU - Wang, Jing

AU - Heng, Pheng Ann

AU - Li, Chao

AU - Guo, Minyi

PY - 2026/3/22

Y1 - 2026/3/22

N2 - Mixture-of-experts (MoE) architectures enable scalable Large Language Models (LLMs) with reduced computational overhead, yet their deployment on memory-constrained edge devices is hindered by substantial memory demands. Traditional expert-offloading techniques mitigate memory constraints but often significantly increase inference latency. We introduce MoE-APEX, an Adaptive Precision EXpert offloading system that optimizes MoE inference for edge architectures by dynamically managing expert precision. Our core innovation is to replace less critical cache-miss experts with low-precision variants, reducing loading latency while maintaining accuracy. MoE-APEX introduces three innovative techniques that map the natural hierarchy of MoE computation: (1) a token-level dynamic expert loading mechanism, (2) a layer-level adaptive expert prefetching technique, and (3) a sequence-level cost-aware expert caching policy. These innovations enable MoE-APEX to leverage the benefits of mixed-precision expert inference fully. Implemented atop Llama.cpp, MoE-APEX achieves decoding speedups ranging from 1.34x to 9.75x compared to state-of-the-art MoE offloading systems across diverse edge devices, offering a robust solution for efficient MoE deployment in resource-constrained environments.

AB - Mixture-of-experts (MoE) architectures enable scalable Large Language Models (LLMs) with reduced computational overhead, yet their deployment on memory-constrained edge devices is hindered by substantial memory demands. Traditional expert-offloading techniques mitigate memory constraints but often significantly increase inference latency. We introduce MoE-APEX, an Adaptive Precision EXpert offloading system that optimizes MoE inference for edge architectures by dynamically managing expert precision. Our core innovation is to replace less critical cache-miss experts with low-precision variants, reducing loading latency while maintaining accuracy. MoE-APEX introduces three innovative techniques that map the natural hierarchy of MoE computation: (1) a token-level dynamic expert loading mechanism, (2) a layer-level adaptive expert prefetching technique, and (3) a sequence-level cost-aware expert caching policy. These innovations enable MoE-APEX to leverage the benefits of mixed-precision expert inference fully. Implemented atop Llama.cpp, MoE-APEX achieves decoding speedups ranging from 1.34x to 9.75x compared to state-of-the-art MoE offloading systems across diverse edge devices, offering a robust solution for efficient MoE deployment in resource-constrained environments.

U2 - 10.1145/3779212.3790187

DO - 10.1145/3779212.3790187

M3 - Conference paper published in conference proceedings

VL - 2

SP - 1185

EP - 1200

BT - ASPLOS '26: Proceedings of the 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systemsctural Support for Programming Languages and Operating Systems

PB - Association for Computing Machinery

Y2 - 22 March 2026 through 26 March 2026

ER -

Tang P, Liu J, Hou X, Pu Y, Wang J[, Heng PA](https://research.cuhk.edu.hk/en/persons/pheng-ann-heng/) et al. [MoE-APEX: An Efficient MoE Inference System with Adaptive Precision Expert Offloading](https://research.cuhk.edu.hk/en/publications/moe-apex-an-efficient-moe-inference-system-with-adaptive-precisio/). In ASPLOS '26: Proceedings of the 31st ACM International Conference on Architectural Support for Programming Languages and Operating Systemsctural Support for Programming Languages and Operating Systems. Vol. 2. Association for Computing Machinery. 2026. p. 1185-1200 doi: 10.1145/3779212.3790187
