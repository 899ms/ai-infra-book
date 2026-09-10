<!-- 从 paper-102-institution.html 迁移的资料快照；原始 HTML SHA-256: e2f842efb7b7b7609d44fe505dcbc0ec3281af1648c2e0b6e451e9a498cfecc0。 -->

# Load and MLP-Aware Thread Orchestration for Recommendation Systems Inference on CPUs

Rishabh Jain

, Teyuh Chou

, Onur Kayiran

, John Kalamatianos

, Gabriel H. Loh

, [Mahmut T. Kandemir](https://pure.psu.edu/en/persons/mahmut-kandemir/)

, [Chita R. Das](https://pure.psu.edu/en/persons/chitaranjan-das/)

- [Computer Science and Engineering](https://pure.psu.edu/en/organisations/computer-science-and-engineering/)
- [Institute for Computational and Data Sciences (ICDS)](https://pure.psu.edu/en/organisations/httpsicspsuedu/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

[3   Link opens in a new tab](https://www.scopus.com/pages/publications/105002573741#tab=citedBy) Scopus citations

- [ Overview ](/en/publications/load-and-mlp-aware-thread-orchestration-for-recommendation-system/)
- [ Fingerprint ](/en/publications/load-and-mlp-aware-thread-orchestration-for-recommendation-system/fingerprints/)

## Abstract

Recommendation models can enhance consumer experiences and are one of the most frequently used machine learning models in data centers. The deep learning recommendation model (DLRM) is one such key workload. While DLRMs are often trained using GPUs, CPUs can be a cost-effective solution for inference. Therefore, optimizing DLRM inference for CPUs is an important research problem with significant business value. In this work, we identify several shortcomings of existing DLRM parallelization techniques, which can include load imbalance across CPU chiplets, suboptimal core allocation for embedding tables, and inefficient utilization of memory- level parallelism (MLP) resources. We propose a novel thread scheduler, called ''Balance,'' that addresses those shortcomings by (1) minimizing core allocation per embedding table to maximize core utilization, (2) using MLP-aware task scheduling based on the characteristics of the embedding tables to better utilize memory bandwidth, and (3) combining work stealing and table reordering mechanisms to reduce load imbalance across CPU chiplets. We evaluate Balance on real hardware with production DLRM traces and demonstrate up to a 1.67× higher speedup over prior state-of-the-art DLRM parallelization techniques with 96 cores. Further, Balance consistently achieves 1.22× higher performance over a range of batch sizes.

[TABLE]

### Publication series

|  |  |
|----|----|
| Name | International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS |
| Volume | 2 |

### Conference

|  |  |
|----|----|
| Conference | 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025 |
| Country/Territory | Netherlands |
| City | Rotterdam |
| Period | 3/30/25 → 4/3/25 |

## All Science Journal Classification (ASJC) codes

- Software
- Information Systems
- Hardware and Architecture

## Access to Document

- [10.1145/3676641.3716003](https://doi.org/10.1145/3676641.3716003)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/105002573741)

- [Link to the citations in Scopus](https://www.scopus.com/pages/publications/105002573741#tab=citedBy)

##  Fingerprint

Dive into the research topics of 'Load and MLP-Aware Thread Orchestration for Recommendation Systems Inference on CPUs'. Together they form a unique fingerprint.

-  Recommendation System Keyphrases 100%
-  System Inference Keyphrases 100%
-  Shared-memory Parallelism Keyphrases 100%
-  Deep Recommendation Model Keyphrases 100%
-  Inference System Computer Science 100%
-  Level Parallelism Computer Science 100%
-  Deep Learning Method Computer Science 100%
-  Embedding Tables Keyphrases 60%

[ View full fingerprint ](/en/publications/load-and-mlp-aware-thread-orchestration-for-recommendation-system/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Jain, R., Chou, T., Kayiran, O., Kalamatianos, J., Loh, G. H.[, Kandemir, M. T.](https://pure.psu.edu/en/persons/mahmut-kandemir/)[, & Das, C. R.](https://pure.psu.edu/en/persons/chitaranjan-das/) (2025). [Load and MLP-Aware Thread Orchestration for Recommendation Systems Inference on CPUs](https://pure.psu.edu/en/publications/load-and-mlp-aware-thread-orchestration-for-recommendation-system/). In *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems* (pp. 589-603). (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 2). Association for Computing Machinery. [https://doi.org/10.1145/3676641.3716003](https://doi.org/10.1145/3676641.3716003)

Jain, Rishabh ; Chou, Teyuh ; Kayiran, Onur et al. / [**Load and MLP-Aware Thread Orchestration for Recommendation Systems Inference on CPUs**](https://pure.psu.edu/en/publications/load-and-mlp-aware-thread-orchestration-for-recommendation-system/). ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery, 2025. pp. 589-603 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS).

@inproceedings{ec7599793329404ca4a8797d2e21d5b1,

title = "Load and MLP-Aware Thread Orchestration for Recommendation Systems Inference on CPUs",

abstract = "Recommendation models can enhance consumer experiences and are one of the most frequently used machine learning models in data centers. The deep learning recommendation model (DLRM) is one such key workload. While DLRMs are often trained using GPUs, CPUs can be a cost-effective solution for inference. Therefore, optimizing DLRM inference for CPUs is an important research problem with significant business value. In this work, we identify several shortcomings of existing DLRM parallelization techniques, which can include load imbalance across CPU chiplets, suboptimal core allocation for embedding tables, and inefficient utilization of memory- level parallelism (MLP) resources. We propose a novel thread scheduler, called ''Balance,'' that addresses those shortcomings by (1) minimizing core allocation per embedding table to maximize core utilization, (2) using MLP-aware task scheduling based on the characteristics of the embedding tables to better utilize memory bandwidth, and (3) combining work stealing and table reordering mechanisms to reduce load imbalance across CPU chiplets. We evaluate Balance on real hardware with production DLRM traces and demonstrate up to a 1.67{\texttimes} higher speedup over prior state-of-the-art DLRM parallelization techniques with 96 cores. Further, Balance consistently achieves 1.22{\texttimes} higher performance over a range of batch sizes.",

author = "Rishabh Jain and Teyuh Chou and Onur Kayiran and John Kalamatianos and Loh, \\Gabriel H.\\ and Kandemir, \\Mahmut T.\\ and Das, \\Chita R.\\",

note = "Publisher Copyright: {\textcopyright} 2025 ACM.; 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025 ; Conference date: 30-03-2025 Through 03-04-2025",

year = "2025",

month = mar,

day = "30",

doi = "10.1145/3676641.3716003",

language = "English (US)",

series = "International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS",

publisher = "Association for Computing Machinery",

pages = "589--603",

booktitle = "ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems",

}

Jain, R, Chou, T, Kayiran, O, Kalamatianos, J, Loh, GH[, Kandemir, MT](https://pure.psu.edu/en/persons/mahmut-kandemir/)[ & Das, CR](https://pure.psu.edu/en/persons/chitaranjan-das/) 2025, [Load and MLP-Aware Thread Orchestration for Recommendation Systems Inference on CPUs](https://pure.psu.edu/en/publications/load-and-mlp-aware-thread-orchestration-for-recommendation-system/). in *ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems.* International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS, vol. 2, Association for Computing Machinery, pp. 589-603, 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025, Rotterdam, Netherlands, 3/30/25. [https://doi.org/10.1145/3676641.3716003](https://doi.org/10.1145/3676641.3716003)

[**Load and MLP-Aware Thread Orchestration for Recommendation Systems Inference on CPUs.**](https://pure.psu.edu/en/publications/load-and-mlp-aware-thread-orchestration-for-recommendation-system/) / Jain, Rishabh; Chou, Teyuh; Kayiran, Onur et al.  
ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery, 2025. p. 589-603 (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS; Vol. 2).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

TY - GEN

T1 - Load and MLP-Aware Thread Orchestration for Recommendation Systems Inference on CPUs

AU - Jain, Rishabh

AU - Chou, Teyuh

AU - Kayiran, Onur

AU - Kalamatianos, John

AU - Loh, Gabriel H.

AU - Kandemir, Mahmut T.

AU - Das, Chita R.

N1 - Publisher Copyright: © 2025 ACM.

PY - 2025/3/30

Y1 - 2025/3/30

N2 - Recommendation models can enhance consumer experiences and are one of the most frequently used machine learning models in data centers. The deep learning recommendation model (DLRM) is one such key workload. While DLRMs are often trained using GPUs, CPUs can be a cost-effective solution for inference. Therefore, optimizing DLRM inference for CPUs is an important research problem with significant business value. In this work, we identify several shortcomings of existing DLRM parallelization techniques, which can include load imbalance across CPU chiplets, suboptimal core allocation for embedding tables, and inefficient utilization of memory- level parallelism (MLP) resources. We propose a novel thread scheduler, called ''Balance,'' that addresses those shortcomings by (1) minimizing core allocation per embedding table to maximize core utilization, (2) using MLP-aware task scheduling based on the characteristics of the embedding tables to better utilize memory bandwidth, and (3) combining work stealing and table reordering mechanisms to reduce load imbalance across CPU chiplets. We evaluate Balance on real hardware with production DLRM traces and demonstrate up to a 1.67× higher speedup over prior state-of-the-art DLRM parallelization techniques with 96 cores. Further, Balance consistently achieves 1.22× higher performance over a range of batch sizes.

AB - Recommendation models can enhance consumer experiences and are one of the most frequently used machine learning models in data centers. The deep learning recommendation model (DLRM) is one such key workload. While DLRMs are often trained using GPUs, CPUs can be a cost-effective solution for inference. Therefore, optimizing DLRM inference for CPUs is an important research problem with significant business value. In this work, we identify several shortcomings of existing DLRM parallelization techniques, which can include load imbalance across CPU chiplets, suboptimal core allocation for embedding tables, and inefficient utilization of memory- level parallelism (MLP) resources. We propose a novel thread scheduler, called ''Balance,'' that addresses those shortcomings by (1) minimizing core allocation per embedding table to maximize core utilization, (2) using MLP-aware task scheduling based on the characteristics of the embedding tables to better utilize memory bandwidth, and (3) combining work stealing and table reordering mechanisms to reduce load imbalance across CPU chiplets. We evaluate Balance on real hardware with production DLRM traces and demonstrate up to a 1.67× higher speedup over prior state-of-the-art DLRM parallelization techniques with 96 cores. Further, Balance consistently achieves 1.22× higher performance over a range of batch sizes.

UR - https://www.scopus.com/pages/publications/105002573741

UR - https://www.scopus.com/pages/publications/105002573741#tab=citedBy

U2 - 10.1145/3676641.3716003

DO - 10.1145/3676641.3716003

M3 - Conference contribution

AN - SCOPUS:105002573741

T3 - International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS

SP - 589

EP - 603

BT - ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems

PB - Association for Computing Machinery

T2 - 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems, ASPLOS 2025

Y2 - 30 March 2025 through 3 April 2025

ER -

Jain R, Chou T, Kayiran O, Kalamatianos J, Loh GH[, Kandemir MT](https://pure.psu.edu/en/persons/mahmut-kandemir/) et al. [Load and MLP-Aware Thread Orchestration for Recommendation Systems Inference on CPUs](https://pure.psu.edu/en/publications/load-and-mlp-aware-thread-orchestration-for-recommendation-system/). In ASPLOS 2025 - Proceedings of the 30th ACM International Conference on Architectural Support for Programming Languages and Operating Systems. Association for Computing Machinery. 2025. p. 589-603. (International Conference on Architectural Support for Programming Languages and Operating Systems - ASPLOS). doi: 10.1145/3676641.3716003
