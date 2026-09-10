<!-- 从 hybe-kaist-index.html 迁移的资料快照；原始 HTML SHA-256: da57c00ab698fe0a62b92dc0abda6803322ecfa50020b3e8cacfd2439345f259。 -->

# Hybe: GPU-NPU Hybrid System for Efficient LLM Inference with Million-Token Context Window

Seungjae Moon

, Junseo Cha

, Hyunjun Park

, [Joo Young Kim](https://pure.kaist.ac.kr/en/persons/joo-young-kim/)

- [School of Electrical Engineering](https://pure.kaist.ac.kr/en/organisations/school-of-electrical-engineering/)

- HyperAccel

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

11 Scopus citations

[](https://plu.mx/plum/a/?doi=10.1145/3695053.3731051)

- [ Overview ](/en/publications/hybe-gpu-npu-hybrid-system-for-efficient-llm-inference-with-milli/)
- [ Fingerprint ](/en/publications/hybe-gpu-npu-hybrid-system-for-efficient-llm-inference-with-milli/fingerprints/)

## Abstract

The growth of context window size in large language model (LLM) inference poses a very distinct computational challenge of hardware inefficiency. The inefficiency arises from the computational imbalance during LLM inference between the compute-intensive prefill stage, and memory-intensive decode stage. The predominant inference hardware, GPU, boasts large number of cores to excel in the prefill stage, which processes the entire input context at once, but suffers from hardware underutilization in the decode stage, which iteratively generates one output token at a time. In conventional LLM, batching has been able to alleviate the underutilization by generating multiple tokens of different requests. However, batching becomes infeasible in models with large context windows over 100K tokens because the Key-Value (KV) activations dominate the physical memory capacity, surpassing the entire model size. In this paper, we propose Hybe, a GPU-NPU hybrid system for efficient LLM inference with a million-token context window. Hybe utilizes the preexisting GPU for the prefill stage and employs lightweight NPUs during the decode stage. Each NPU includes only the necessary computing resources to fully utilize the given memory bandwidth, thereby achieving maximum hardware efficiency. Furthermore, Hybe introduces fine-grained KV transmission, a kernel scheduling method that immediately offloads partial KV produced from the GPU to the NPU, which significantly reduces the KV memory required in the GPU. Lastly, Hybe scheduler applies stage-wise pipelining that dynamically assigns queued requests to idle hardware to minimize stalls. Hybe utilizes NVIDIA H100 GPU with inference-optimized vLLM library and implement Hybe NPU in 4nm process with equal HBM specification. Hybe achieves 2.1× speedup for Phi-3 with 100K-token context window and 3.9× energy efficiency for Llama-3 with 1M-token context window, over H100 GPUs with equal total device count.

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
| Conference | 52nd Annual International Symposium on Computer Architecture, ISCA 2025 |
| Country/Territory | Japan |
| City | Tokyo |
| Period | 21/06/25 → 25/06/25 |

## UN SDGs

This output contributes to the following UN [Sustainable Development Goals (SDGs)](https://www.un.org/sustainabledevelopment/sustainable-development-goals/)

1.  ![SDG 7 - Affordable and Clean Energy](/assets/sdg_icons/affordable_and_clean_energy-b8e39c169139faf6df7199566119c3c0.svg "SDG 7 - Affordable and Clean Energy")
    SDG 7 Affordable and Clean Energy

## Keywords

- Context window
- Heterogeneous (hybrid) system
- Large language model (LLM)
- Neural processing unit (NPU)
- Scheduling

## Access to Document

- [10.1145/3695053.3731051](https://doi.org/10.1145/3695053.3731051)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/105009590277)

##  Fingerprint

Dive into the research topics of 'Hybe: GPU-NPU Hybrid System for Efficient LLM Inference with Million-Token Context Window'. Together they form a unique fingerprint.

-  Large Language Model Computer Science 100%
-  Graphics Processing Unit Computer Science 100%
-  Decode Stage Computer Science 37%
-  Energy Efficiency Computer Science 12%
-  Memory Capacity Computer Science 12%
-  Memory Bandwidth Computer Science 12%
-  Computing Resource Computer Science 12%
-  Physical Memory Computer Science 12%

[ View full fingerprint ](/en/publications/hybe-gpu-npu-hybrid-system-for-efficient-llm-inference-with-milli/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Moon, S., Cha, J., Park, H.[, & Kim, J. Y.](https://pure.kaist.ac.kr/en/persons/joo-young-kim/) (2025). [Hybe: GPU-NPU Hybrid System for Efficient LLM Inference with Million-Token Context Window](https://pure.kaist.ac.kr/en/publications/hybe-gpu-npu-hybrid-system-for-efficient-llm-inference-with-milli/). In *ISCA 2025 - Proceedings of the 52nd Annual International Symposium on Computer Architecture* (pp. 808-820). (Proceedings - International Symposium on Computer Architecture). Institute of Electrical and Electronics Engineers Inc.. [https://doi.org/10.1145/3695053.3731051](https://doi.org/10.1145/3695053.3731051)

Moon, Seungjae ; Cha, Junseo ; Park, Hyunjun et al. / [**Hybe : GPU-NPU Hybrid System for Efficient LLM Inference with Million-Token Context Window**](https://pure.kaist.ac.kr/en/publications/hybe-gpu-npu-hybrid-system-for-efficient-llm-inference-with-milli/). ISCA 2025 - Proceedings of the 52nd Annual International Symposium on Computer Architecture. Institute of Electrical and Electronics Engineers Inc., 2025. pp. 808-820 (Proceedings - International Symposium on Computer Architecture).

@inproceedings{34e2e0566b0c4c7489ac5d19f2c1f00c,

title = "Hybe: GPU-NPU Hybrid System for Efficient LLM Inference with Million-Token Context Window",

abstract = "The growth of context window size in large language model (LLM) inference poses a very distinct computational challenge of hardware inefficiency. The inefficiency arises from the computational imbalance during LLM inference between the compute-intensive prefill stage, and memory-intensive decode stage. The predominant inference hardware, GPU, boasts large number of cores to excel in the prefill stage, which processes the entire input context at once, but suffers from hardware underutilization in the decode stage, which iteratively generates one output token at a time. In conventional LLM, batching has been able to alleviate the underutilization by generating multiple tokens of different requests. However, batching becomes infeasible in models with large context windows over 100K tokens because the Key-Value (KV) activations dominate the physical memory capacity, surpassing the entire model size. In this paper, we propose Hybe, a GPU-NPU hybrid system for efficient LLM inference with a million-token context window. Hybe utilizes the preexisting GPU for the prefill stage and employs lightweight NPUs during the decode stage. Each NPU includes only the necessary computing resources to fully utilize the given memory bandwidth, thereby achieving maximum hardware efficiency. Furthermore, Hybe introduces fine-grained KV transmission, a kernel scheduling method that immediately offloads partial KV produced from the GPU to the NPU, which significantly reduces the KV memory required in the GPU. Lastly, Hybe scheduler applies stage-wise pipelining that dynamically assigns queued requests to idle hardware to minimize stalls. Hybe utilizes NVIDIA H100 GPU with inference-optimized vLLM library and implement Hybe NPU in 4nm process with equal HBM specification. Hybe achieves 2.1{\texttimes} speedup for Phi-3 with 100K-token context window and 3.9{\texttimes} energy efficiency for Llama-3 with 1M-token context window, over H100 GPUs with equal total device count.",

keywords = "Context window, Heterogeneous (hybrid) system, Large language model (LLM), Neural processing unit (NPU), Scheduling",

author = "Seungjae Moon and Junseo Cha and Hyunjun Park and Kim, \\Joo Young\\",

note = "Publisher Copyright: {\textcopyright} 2025 Copyright held by the owner/author(s).; 52nd Annual International Symposium on Computer Architecture, ISCA 2025 ; Conference date: 21-06-2025 Through 25-06-2025",

year = "2025",

month = jun,

day = "21",

doi = "10.1145/3695053.3731051",

language = "English",

series = "Proceedings - International Symposium on Computer Architecture",

publisher = "Institute of Electrical and Electronics Engineers Inc.",

pages = "808--820",

booktitle = "ISCA 2025 - Proceedings of the 52nd Annual International Symposium on Computer Architecture",

}

Moon, S, Cha, J, Park, H[ & Kim, JY](https://pure.kaist.ac.kr/en/persons/joo-young-kim/) 2025, [Hybe: GPU-NPU Hybrid System for Efficient LLM Inference with Million-Token Context Window](https://pure.kaist.ac.kr/en/publications/hybe-gpu-npu-hybrid-system-for-efficient-llm-inference-with-milli/). in *ISCA 2025 - Proceedings of the 52nd Annual International Symposium on Computer Architecture.* Proceedings - International Symposium on Computer Architecture, Institute of Electrical and Electronics Engineers Inc., pp. 808-820, 52nd Annual International Symposium on Computer Architecture, ISCA 2025, Tokyo, Japan, 21/06/25. [https://doi.org/10.1145/3695053.3731051](https://doi.org/10.1145/3695053.3731051)

[**Hybe: GPU-NPU Hybrid System for Efficient LLM Inference with Million-Token Context Window.**](https://pure.kaist.ac.kr/en/publications/hybe-gpu-npu-hybrid-system-for-efficient-llm-inference-with-milli/) / Moon, Seungjae; Cha, Junseo; Park, Hyunjun et al.  
ISCA 2025 - Proceedings of the 52nd Annual International Symposium on Computer Architecture. Institute of Electrical and Electronics Engineers Inc., 2025. p. 808-820 (Proceedings - International Symposium on Computer Architecture).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

TY - GEN

T1 - Hybe

T2 - 52nd Annual International Symposium on Computer Architecture, ISCA 2025

AU - Moon, Seungjae

AU - Cha, Junseo

AU - Park, Hyunjun

AU - Kim, Joo Young

N1 - Publisher Copyright: © 2025 Copyright held by the owner/author(s).

PY - 2025/6/21

Y1 - 2025/6/21

N2 - The growth of context window size in large language model (LLM) inference poses a very distinct computational challenge of hardware inefficiency. The inefficiency arises from the computational imbalance during LLM inference between the compute-intensive prefill stage, and memory-intensive decode stage. The predominant inference hardware, GPU, boasts large number of cores to excel in the prefill stage, which processes the entire input context at once, but suffers from hardware underutilization in the decode stage, which iteratively generates one output token at a time. In conventional LLM, batching has been able to alleviate the underutilization by generating multiple tokens of different requests. However, batching becomes infeasible in models with large context windows over 100K tokens because the Key-Value (KV) activations dominate the physical memory capacity, surpassing the entire model size. In this paper, we propose Hybe, a GPU-NPU hybrid system for efficient LLM inference with a million-token context window. Hybe utilizes the preexisting GPU for the prefill stage and employs lightweight NPUs during the decode stage. Each NPU includes only the necessary computing resources to fully utilize the given memory bandwidth, thereby achieving maximum hardware efficiency. Furthermore, Hybe introduces fine-grained KV transmission, a kernel scheduling method that immediately offloads partial KV produced from the GPU to the NPU, which significantly reduces the KV memory required in the GPU. Lastly, Hybe scheduler applies stage-wise pipelining that dynamically assigns queued requests to idle hardware to minimize stalls. Hybe utilizes NVIDIA H100 GPU with inference-optimized vLLM library and implement Hybe NPU in 4nm process with equal HBM specification. Hybe achieves 2.1× speedup for Phi-3 with 100K-token context window and 3.9× energy efficiency for Llama-3 with 1M-token context window, over H100 GPUs with equal total device count.

AB - The growth of context window size in large language model (LLM) inference poses a very distinct computational challenge of hardware inefficiency. The inefficiency arises from the computational imbalance during LLM inference between the compute-intensive prefill stage, and memory-intensive decode stage. The predominant inference hardware, GPU, boasts large number of cores to excel in the prefill stage, which processes the entire input context at once, but suffers from hardware underutilization in the decode stage, which iteratively generates one output token at a time. In conventional LLM, batching has been able to alleviate the underutilization by generating multiple tokens of different requests. However, batching becomes infeasible in models with large context windows over 100K tokens because the Key-Value (KV) activations dominate the physical memory capacity, surpassing the entire model size. In this paper, we propose Hybe, a GPU-NPU hybrid system for efficient LLM inference with a million-token context window. Hybe utilizes the preexisting GPU for the prefill stage and employs lightweight NPUs during the decode stage. Each NPU includes only the necessary computing resources to fully utilize the given memory bandwidth, thereby achieving maximum hardware efficiency. Furthermore, Hybe introduces fine-grained KV transmission, a kernel scheduling method that immediately offloads partial KV produced from the GPU to the NPU, which significantly reduces the KV memory required in the GPU. Lastly, Hybe scheduler applies stage-wise pipelining that dynamically assigns queued requests to idle hardware to minimize stalls. Hybe utilizes NVIDIA H100 GPU with inference-optimized vLLM library and implement Hybe NPU in 4nm process with equal HBM specification. Hybe achieves 2.1× speedup for Phi-3 with 100K-token context window and 3.9× energy efficiency for Llama-3 with 1M-token context window, over H100 GPUs with equal total device count.

KW - Context window

KW - Heterogeneous (hybrid) system

KW - Large language model (LLM)

KW - Neural processing unit (NPU)

KW - Scheduling

UR - https://www.scopus.com/pages/publications/105009590277

U2 - 10.1145/3695053.3731051

DO - 10.1145/3695053.3731051

M3 - Conference contribution

AN - SCOPUS:105009590277

T3 - Proceedings - International Symposium on Computer Architecture

SP - 808

EP - 820

BT - ISCA 2025 - Proceedings of the 52nd Annual International Symposium on Computer Architecture

PB - Institute of Electrical and Electronics Engineers Inc.

Y2 - 21 June 2025 through 25 June 2025

ER -

Moon S, Cha J, Park H[, Kim JY](https://pure.kaist.ac.kr/en/persons/joo-young-kim/). [Hybe: GPU-NPU Hybrid System for Efficient LLM Inference with Million-Token Context Window](https://pure.kaist.ac.kr/en/publications/hybe-gpu-npu-hybrid-system-for-efficient-llm-inference-with-milli/). In ISCA 2025 - Proceedings of the 52nd Annual International Symposium on Computer Architecture. Institute of Electrical and Electronics Engineers Inc. 2025. p. 808-820. (Proceedings - International Symposium on Computer Architecture). doi: 10.1145/3695053.3731051

- 
- [](https://www.facebook.com/sharer.php?u=https://pure.kaist.ac.kr/en/publications/hybe-gpu-npu-hybrid-system-for-efficient-llm-inference-with-milli/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3695053.3731051&p%5Bsummary%5D=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+Hybe%3A+GPU-NPU+Hybrid+System+for+Efficient+LLM+Inference+with+Million-Token+Context+Window)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://pure.kaist.ac.kr/en/publications/hybe-gpu-npu-hybrid-system-for-efficient-llm-inference-with-milli/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3695053.3731051&text=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+Hybe%3A+GPU-NPU+Hybrid+System+for+Efficient+LLM+Inference+with+Million-Token+Context+Window)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://pure.kaist.ac.kr/en/publications/hybe-gpu-npu-hybrid-system-for-efficient-llm-inference-with-milli/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3695053.3731051&summary=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+Hybe%3A+GPU-NPU+Hybrid+System+for+Efficient+LLM+Inference+with+Million-Token+Context+Window)
- [](/cdn-cgi/l/email-protection#122d616770787771662f5a6b70773721533720225542473f5c42473720225a6b70607b76372022416b6166777f372022747d603720225774747b717b777c663720225e5e5f3720225b7c747760777c7177372022657b667a3720225f7b7e7e7b7d7c3f467d79777c372022517d7c66776a66372022457b7c767d6534707d766b2f517a7771793720227d6766372022667a7b61372022607761777360717a3720227d67666267663720227366372022597d607773372022537664737c7177763720225b7c61667b666766773720227d7437202241717b777c7177372022737c763720224677717a7c7d7e7d756b3721533720225a6b70773721533720225542473f5c42473720225a6b70607b76372022416b6166777f372022747d603720225774747b717b777c663720225e5e5f3720225b7c747760777c7177372022657b667a3720225f7b7e7e7b7d7c3f467d79777c372022517d7c66776a66372022457b7c767d65326e327a66666261283d3d626760773c79737b61663c73713c79603d777c3d6267707e7b7173667b7d7c613d7a6b70773f7562673f7c62673f7a6b70607b763f616b6166777f3f747d603f7774747b717b777c663f7e7e7f3f7b7c747760777c71773f657b667a3f7f7b7e7e7b3d2d67667f4d617d676071772f777f737b7e34737f622967667f4d7f77767b677f2f777f737b7e34737f622967667f4d71737f62737b757c2f617a7360777e7b7c79)
