<!-- 从 isca24-llmcompass-institution.html 迁移的资料快照；原始 HTML SHA-256: 818fb135210fabe1ec682cce4173809faa7c1999e75238bf7f18b4805712d210。 -->

# LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference

Hengrui Zhang

, August Ning

, Rohan Baskar Prabhakar

, [David Wentzlaff](https://collaborate.princeton.edu/en/persons/david-wentzlaff/)

- [Electrical and Computer Engineering](https://collaborate.princeton.edu/en/organisations/electrical-and-computer-engineering/)
- [Princeton Language and Intelligence (PLI)](https://collaborate.princeton.edu/en/organisations/princeton-language-and-intelligence-pli/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

[67   Link opens in a new tab](https://www.scopus.com/pages/publications/85201142444#tab=citedBy) Scopus citations

- [ Overview ](/en/publications/llmcompass-enabling-efficient-hardware-design-for-large-language-/)
- [ Fingerprint ](/en/publications/llmcompass-enabling-efficient-hardware-design-for-large-language-/fingerprints/)

## Abstract

The past year has witnessed the increasing popularity of Large Language Models (LLMs). Their unprecedented scale and associated high hardware cost have impeded their broader adoption, calling for efficient hardware designs. With the large hardware needed to simply run LLM inference, evaluating different hardware designs becomes a new bottleneck. This work introduces LLMCompass¹, a hardware evaluation framework for LLM inference workloads. LLMCompass is fast, accurate, versatile, and able to describe and evaluate different hardware designs. LLMCompass includes a mapper to automatically find performance-optimal mapping and scheduling. It also incorporates an area-based cost model to help architects reason about their design choices. Compared to real-world hardware, LLMCompass' estimated latency achieves an average 10.9% error rate across various operators with various input sizes and an average 4.1% error rate for LLM inference. With LLMCompass, simulating a 4-NVIDIA A100 GPU node running GPT-3 175B inference can be done within 16 minutes on commodity hardware, including 26,400 rounds of the mapper's parameter search. With the aid of LLMCompass, this work draws architectural implications and explores new cost-effective hardware designs. By reducing the compute capability or replacing High Bandwidth Memory (HBM) with traditional DRAM, these new designs can achieve as much as 3.41x improvement in performance/cost compared to an NVIDIA A100, making them promising choices for democratizing LLMs.¹Available at https://github.com/PrincetonUniversity/LLMCompass.

[TABLE]

### Publication series

|  |  |
|----|----|
| Name | Proceedings - International Symposium on Computer Architecture |
| ISSN (Print) | 1063-6897 |
| ISSN (Electronic) | 2575-713X |

### Conference

|  |  |
|----|----|
| Conference | 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024 |
| Country/Territory | Argentina |
| City | Buenos Aires |
| Period | 6/29/24 → 7/3/24 |

## All Science Journal Classification (ASJC) codes

- Hardware and Architecture

## Keywords

- Large language model
- accelerator
- area model
- cost model
- performance model

## Access to Document

- [10.1109/ISCA59077.2024.00082](https://doi.org/10.1109/ISCA59077.2024.00082)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/85201142444)

- [Link to the citations in Scopus](https://www.scopus.com/pages/publications/85201142444#tab=citedBy)

##  Fingerprint

Dive into the research topics of 'LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference'. Together they form a unique fingerprint.

-  Efficient Hardware Keyphrases 100%
-  Hardware Design Keyphrases 100%
-  Large Language Model Inference Keyphrases 100%
-  Large Language Model Computer Science 100%
-  Error Rate Keyphrases 40%
-  Mapper Keyphrases 40%
-  Latency Keyphrases 20%
-  Optimal Scheduling Keyphrases 20%

[ View full fingerprint ](/en/publications/llmcompass-enabling-efficient-hardware-design-for-large-language-/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Zhang, H., Ning, A., Prabhakar, R. B.[, & Wentzlaff, D.](https://collaborate.princeton.edu/en/persons/david-wentzlaff/) (2024). [LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference](https://collaborate.princeton.edu/en/publications/llmcompass-enabling-efficient-hardware-design-for-large-language-/). In *Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024* (pp. 1080-1096). (Proceedings - International Symposium on Computer Architecture). Institute of Electrical and Electronics Engineers Inc.. [https://doi.org/10.1109/ISCA59077.2024.00082](https://doi.org/10.1109/ISCA59077.2024.00082)

Zhang, Hengrui ; Ning, August ; Prabhakar, Rohan Baskar et al. / [**LLMCompass : Enabling Efficient Hardware Design for Large Language Model Inference**](https://collaborate.princeton.edu/en/publications/llmcompass-enabling-efficient-hardware-design-for-large-language-/). Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc., 2024. pp. 1080-1096 (Proceedings - International Symposium on Computer Architecture).

@inproceedings{472f107924d5465c86137efc05ba9cdf,

title = "LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference",

abstract = "The past year has witnessed the increasing popularity of Large Language Models (LLMs). Their unprecedented scale and associated high hardware cost have impeded their broader adoption, calling for efficient hardware designs. With the large hardware needed to simply run LLM inference, evaluating different hardware designs becomes a new bottleneck. This work introduces LLMCompass1, a hardware evaluation framework for LLM inference workloads. LLMCompass is fast, accurate, versatile, and able to describe and evaluate different hardware designs. LLMCompass includes a mapper to automatically find performance-optimal mapping and scheduling. It also incorporates an area-based cost model to help architects reason about their design choices. Compared to real-world hardware, LLMCompass' estimated latency achieves an average 10.9\\ error rate across various operators with various input sizes and an average 4.1\\ error rate for LLM inference. With LLMCompass, simulating a 4-NVIDIA A100 GPU node running GPT-3 175B inference can be done within 16 minutes on commodity hardware, including 26,400 rounds of the mapper's parameter search. With the aid of LLMCompass, this work draws architectural implications and explores new cost-effective hardware designs. By reducing the compute capability or replacing High Bandwidth Memory (HBM) with traditional DRAM, these new designs can achieve as much as 3.41x improvement in performance/cost compared to an NVIDIA A100, making them promising choices for democratizing LLMs.1Available at https://github.com/PrincetonUniversity/LLMCompass.",

keywords = "Large language model, accelerator, area model, cost model, performance model",

author = "Hengrui Zhang and August Ning and Prabhakar, \\Rohan Baskar\\ and David Wentzlaff",

note = "Publisher Copyright: {\textcopyright} 2024 IEEE.; 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024 ; Conference date: 29-06-2024 Through 03-07-2024",

year = "2024",

doi = "10.1109/ISCA59077.2024.00082",

language = "English (US)",

series = "Proceedings - International Symposium on Computer Architecture",

publisher = "Institute of Electrical and Electronics Engineers Inc.",

pages = "1080--1096",

booktitle = "Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024",

address = "United States",

}

Zhang, H, Ning, A, Prabhakar, RB[ & Wentzlaff, D](https://collaborate.princeton.edu/en/persons/david-wentzlaff/) 2024, [LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference](https://collaborate.princeton.edu/en/publications/llmcompass-enabling-efficient-hardware-design-for-large-language-/). in *Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024.* Proceedings - International Symposium on Computer Architecture, Institute of Electrical and Electronics Engineers Inc., pp. 1080-1096, 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024, Buenos Aires, Argentina, 6/29/24. [https://doi.org/10.1109/ISCA59077.2024.00082](https://doi.org/10.1109/ISCA59077.2024.00082)

[**LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference.**](https://collaborate.princeton.edu/en/publications/llmcompass-enabling-efficient-hardware-design-for-large-language-/) / Zhang, Hengrui; Ning, August; Prabhakar, Rohan Baskar et al.  
Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc., 2024. p. 1080-1096 (Proceedings - International Symposium on Computer Architecture).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

TY - GEN

T1 - LLMCompass

T2 - 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024

AU - Zhang, Hengrui

AU - Ning, August

AU - Prabhakar, Rohan Baskar

AU - Wentzlaff, David

N1 - Publisher Copyright: © 2024 IEEE.

PY - 2024

Y1 - 2024

N2 - The past year has witnessed the increasing popularity of Large Language Models (LLMs). Their unprecedented scale and associated high hardware cost have impeded their broader adoption, calling for efficient hardware designs. With the large hardware needed to simply run LLM inference, evaluating different hardware designs becomes a new bottleneck. This work introduces LLMCompass1, a hardware evaluation framework for LLM inference workloads. LLMCompass is fast, accurate, versatile, and able to describe and evaluate different hardware designs. LLMCompass includes a mapper to automatically find performance-optimal mapping and scheduling. It also incorporates an area-based cost model to help architects reason about their design choices. Compared to real-world hardware, LLMCompass' estimated latency achieves an average 10.9% error rate across various operators with various input sizes and an average 4.1% error rate for LLM inference. With LLMCompass, simulating a 4-NVIDIA A100 GPU node running GPT-3 175B inference can be done within 16 minutes on commodity hardware, including 26,400 rounds of the mapper's parameter search. With the aid of LLMCompass, this work draws architectural implications and explores new cost-effective hardware designs. By reducing the compute capability or replacing High Bandwidth Memory (HBM) with traditional DRAM, these new designs can achieve as much as 3.41x improvement in performance/cost compared to an NVIDIA A100, making them promising choices for democratizing LLMs.1Available at https://github.com/PrincetonUniversity/LLMCompass.

AB - The past year has witnessed the increasing popularity of Large Language Models (LLMs). Their unprecedented scale and associated high hardware cost have impeded their broader adoption, calling for efficient hardware designs. With the large hardware needed to simply run LLM inference, evaluating different hardware designs becomes a new bottleneck. This work introduces LLMCompass1, a hardware evaluation framework for LLM inference workloads. LLMCompass is fast, accurate, versatile, and able to describe and evaluate different hardware designs. LLMCompass includes a mapper to automatically find performance-optimal mapping and scheduling. It also incorporates an area-based cost model to help architects reason about their design choices. Compared to real-world hardware, LLMCompass' estimated latency achieves an average 10.9% error rate across various operators with various input sizes and an average 4.1% error rate for LLM inference. With LLMCompass, simulating a 4-NVIDIA A100 GPU node running GPT-3 175B inference can be done within 16 minutes on commodity hardware, including 26,400 rounds of the mapper's parameter search. With the aid of LLMCompass, this work draws architectural implications and explores new cost-effective hardware designs. By reducing the compute capability or replacing High Bandwidth Memory (HBM) with traditional DRAM, these new designs can achieve as much as 3.41x improvement in performance/cost compared to an NVIDIA A100, making them promising choices for democratizing LLMs.1Available at https://github.com/PrincetonUniversity/LLMCompass.

KW - Large language model

KW - accelerator

KW - area model

KW - cost model

KW - performance model

UR - https://www.scopus.com/pages/publications/85201142444

UR - https://www.scopus.com/pages/publications/85201142444#tab=citedBy

U2 - 10.1109/ISCA59077.2024.00082

DO - 10.1109/ISCA59077.2024.00082

M3 - Conference contribution

AN - SCOPUS:85201142444

T3 - Proceedings - International Symposium on Computer Architecture

SP - 1080

EP - 1096

BT - Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024

PB - Institute of Electrical and Electronics Engineers Inc.

Y2 - 29 June 2024 through 3 July 2024

ER -

Zhang H, Ning A, Prabhakar RB[, Wentzlaff D](https://collaborate.princeton.edu/en/persons/david-wentzlaff/). [LLMCompass: Enabling Efficient Hardware Design for Large Language Model Inference](https://collaborate.princeton.edu/en/publications/llmcompass-enabling-efficient-hardware-design-for-large-language-/). In Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc. 2024. p. 1080-1096. (Proceedings - International Symposium on Computer Architecture). doi: 10.1109/ISCA59077.2024.00082
