<!-- 从 adaptiv-institution.html 迁移的资料快照；原始 HTML SHA-256: 8fc3317221d2cd118322541aa4a64d7688a83fb3c855007ff3e6fd198425c3fa。 -->

# AdapTiV: Sign-Similarity Based Image-Adaptive Token Merging for Vision Transformer Acceleration

Seungjae Yoo

, Hangyeol Kim

, [Joo Young Kim](https://pure.kaist.ac.kr/en/persons/joo-young-kim/)

- [School of Electrical Engineering](https://pure.kaist.ac.kr/en/organisations/school-of-electrical-engineering/)

- Korea Advanced Institute of Science and Technology

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

11 Scopus citations

- [ Overview ](/en/publications/adaptiv-sign-similarity-based-image-adaptive-token-merging-for-vi/)
- [ Fingerprint ](/en/publications/adaptiv-sign-similarity-based-image-adaptive-token-merging-for-vi/fingerprints/)

## Abstract

The advent of Vision Transformers (ViT) has set a new performance leap in computer vision by leveraging self-Attention mechanisms. However, the computational efficiency of ViTs is limited by the quadratic complexity of self-Attention and redundancy among image tokens. To address these issues, token merging strategies have been explored to reduce input size by merging similar tokens. Nonetheless, implementing token merging presents a degradation of latency performance due to its two factors: inefficient computations and fixed merge rate nature. This paper introduces AdapTiV, a novel hardware-software co-designed accelerator that accelerates ViTs through image-Adaptive token merging, effectively addressing the afore-mentioned challenges. Under the design philosophy of reducing the overhead of token merging and concealing its latency within the Layer Normalization (LN) process, AdapTiV incorporates algorithmic innovations such as Local Matching, which restricts the search space for token merging, thereby reducing the computational complexity; Sign Similarity, which simplifies the calculation of similarity between tokens; and Dynamic Merge Rate, which enables image-Adaptive token merging. Additionally, the hardware component that supports AdapTiV's algorithms, named the Adaptive Token Merging Engine, employs Sign-Driven Scheduling to conceal the overhead of token merging effectively. This engine integrates submodules such as a Sign Similarity Computing Unit, which calculates the similarity between tokens using a newly introduced similarity metric; a Sign Scratchpad, which is a lightweight, image-width-sized memory that stores previous tokens; a Sign Scratchpad Managing Unit, which controls the Sign Scratchpad; and a Token Integration Map to facilitate efficient, image-Adaptive token merging. Our evaluations demonstrate that AdapTiV achieves, on average, 309.4 ×, 18.4×, 89.8×, 6.3× speedups and 262.1×, 21.5×, 496.6×, 11.2× improvements in energy efficiency over edge CPUs, edge GPUs, server CPUs, and server GPUs, while maintaining an accuracy loss below 1 % without additional training.

[TABLE]

### Publication series

|  |  |
|----|----|
| Name | Proceedings of the Annual International Symposium on Microarchitecture, MICRO |
| ISSN (Print) | 1072-4451 |

### Conference

|  |  |
|----|----|
| Conference | 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024 |
| Country/Territory | United States |
| City | Austin |
| Period | 2/11/24 → 6/11/24 |

## UN SDGs

This output contributes to the following UN [Sustainable Development Goals (SDGs)](https://www.un.org/sustainabledevelopment/sustainable-development-goals/)

1.  ![SDG 7 - Affordable and Clean Energy](/assets/sdg_icons/affordable_and_clean_energy-b8e39c169139faf6df7199566119c3c0.svg "SDG 7 - Affordable and Clean Energy")
    SDG 7 Affordable and Clean Energy

## Access to Document

- [10.1109/MICRO61859.2024.00015](https://doi.org/10.1109/MICRO61859.2024.00015)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/85213310284)

##  Fingerprint

Dive into the research topics of 'AdapTiV: Sign-Similarity Based Image-Adaptive Token Merging for Vision Transformer Acceleration'. Together they form a unique fingerprint.

-  Vision Transformer Computer Science 100%
-  Graphics Processing Unit Computer Science 100%
-  Energy Efficiency Computer Science 50%
-  Self-Attention Mechanism Computer Science 50%
-  Search Space Computer Science 50%
-  Computational Complexity Computer Science 50%
-  Computational Efficiency Computer Science 50%
-  Hardware Component Computer Science 50%

[ View full fingerprint ](/en/publications/adaptiv-sign-similarity-based-image-adaptive-token-merging-for-vi/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Yoo, S., Kim, H.[, & Kim, J. Y.](https://pure.kaist.ac.kr/en/persons/joo-young-kim/) (2024). [AdapTiV: Sign-Similarity Based Image-Adaptive Token Merging for Vision Transformer Acceleration](https://pure.kaist.ac.kr/en/publications/adaptiv-sign-similarity-based-image-adaptive-token-merging-for-vi/). In *Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024* (pp. 64-77). (Proceedings of the Annual International Symposium on Microarchitecture, MICRO). IEEE Computer Society. [https://doi.org/10.1109/MICRO61859.2024.00015](https://doi.org/10.1109/MICRO61859.2024.00015)

Yoo, Seungjae ; Kim, Hangyeol [ ; Kim, Joo Young](https://pure.kaist.ac.kr/en/persons/joo-young-kim/). / [**AdapTiV : Sign-Similarity Based Image-Adaptive Token Merging for Vision Transformer Acceleration**](https://pure.kaist.ac.kr/en/publications/adaptiv-sign-similarity-based-image-adaptive-token-merging-for-vi/). Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society, 2024. pp. 64-77 (Proceedings of the Annual International Symposium on Microarchitecture, MICRO).

@inproceedings{13c138490e2249498d1afa57fbf3ff61,

title = "AdapTiV: Sign-Similarity Based Image-Adaptive Token Merging for Vision Transformer Acceleration",

abstract = "The advent of Vision Transformers (ViT) has set a new performance leap in computer vision by leveraging self-Attention mechanisms. However, the computational efficiency of ViTs is limited by the quadratic complexity of self-Attention and redundancy among image tokens. To address these issues, token merging strategies have been explored to reduce input size by merging similar tokens. Nonetheless, implementing token merging presents a degradation of latency performance due to its two factors: inefficient computations and fixed merge rate nature. This paper introduces AdapTiV, a novel hardware-software co-designed accelerator that accelerates ViTs through image-Adaptive token merging, effectively addressing the afore-mentioned challenges. Under the design philosophy of reducing the overhead of token merging and concealing its latency within the Layer Normalization (LN) process, AdapTiV incorporates algorithmic innovations such as Local Matching, which restricts the search space for token merging, thereby reducing the computational complexity; Sign Similarity, which simplifies the calculation of similarity between tokens; and Dynamic Merge Rate, which enables image-Adaptive token merging. Additionally, the hardware component that supports AdapTiV's algorithms, named the Adaptive Token Merging Engine, employs Sign-Driven Scheduling to conceal the overhead of token merging effectively. This engine integrates submodules such as a Sign Similarity Computing Unit, which calculates the similarity between tokens using a newly introduced similarity metric; a Sign Scratchpad, which is a lightweight, image-width-sized memory that stores previous tokens; a Sign Scratchpad Managing Unit, which controls the Sign Scratchpad; and a Token Integration Map to facilitate efficient, image-Adaptive token merging. Our evaluations demonstrate that AdapTiV achieves, on average, 309.4 {\texttimes}, 18.4{\texttimes}, 89.8{\texttimes}, 6.3{\texttimes} speedups and 262.1{\texttimes}, 21.5{\texttimes}, 496.6{\texttimes}, 11.2{\texttimes} improvements in energy efficiency over edge CPUs, edge GPUs, server CPUs, and server GPUs, while maintaining an accuracy loss below 1 \\ without additional training.",

author = "Seungjae Yoo and Hangyeol Kim and Kim, \\Joo Young\\",

note = "Publisher Copyright: {\textcopyright} 2024 IEEE.; 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024 ; Conference date: 02-11-2024 Through 06-11-2024",

year = "2024",

doi = "10.1109/MICRO61859.2024.00015",

language = "English",

series = "Proceedings of the Annual International Symposium on Microarchitecture, MICRO",

publisher = "IEEE Computer Society",

pages = "64--77",

booktitle = "Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024",

}

Yoo, S, Kim, H[ & Kim, JY](https://pure.kaist.ac.kr/en/persons/joo-young-kim/) 2024, [AdapTiV: Sign-Similarity Based Image-Adaptive Token Merging for Vision Transformer Acceleration](https://pure.kaist.ac.kr/en/publications/adaptiv-sign-similarity-based-image-adaptive-token-merging-for-vi/). in *Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024.* Proceedings of the Annual International Symposium on Microarchitecture, MICRO, IEEE Computer Society, pp. 64-77, 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024, Austin, United States, 2/11/24. [https://doi.org/10.1109/MICRO61859.2024.00015](https://doi.org/10.1109/MICRO61859.2024.00015)

[**AdapTiV: Sign-Similarity Based Image-Adaptive Token Merging for Vision Transformer Acceleration.**](https://pure.kaist.ac.kr/en/publications/adaptiv-sign-similarity-based-image-adaptive-token-merging-for-vi/) / Yoo, Seungjae; Kim, Hangyeol[; Kim, Joo Young](https://pure.kaist.ac.kr/en/persons/joo-young-kim/).  
Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society, 2024. p. 64-77 (Proceedings of the Annual International Symposium on Microarchitecture, MICRO).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

TY - GEN

T1 - AdapTiV

T2 - 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024

AU - Yoo, Seungjae

AU - Kim, Hangyeol

AU - Kim, Joo Young

N1 - Publisher Copyright: © 2024 IEEE.

PY - 2024

Y1 - 2024

N2 - The advent of Vision Transformers (ViT) has set a new performance leap in computer vision by leveraging self-Attention mechanisms. However, the computational efficiency of ViTs is limited by the quadratic complexity of self-Attention and redundancy among image tokens. To address these issues, token merging strategies have been explored to reduce input size by merging similar tokens. Nonetheless, implementing token merging presents a degradation of latency performance due to its two factors: inefficient computations and fixed merge rate nature. This paper introduces AdapTiV, a novel hardware-software co-designed accelerator that accelerates ViTs through image-Adaptive token merging, effectively addressing the afore-mentioned challenges. Under the design philosophy of reducing the overhead of token merging and concealing its latency within the Layer Normalization (LN) process, AdapTiV incorporates algorithmic innovations such as Local Matching, which restricts the search space for token merging, thereby reducing the computational complexity; Sign Similarity, which simplifies the calculation of similarity between tokens; and Dynamic Merge Rate, which enables image-Adaptive token merging. Additionally, the hardware component that supports AdapTiV's algorithms, named the Adaptive Token Merging Engine, employs Sign-Driven Scheduling to conceal the overhead of token merging effectively. This engine integrates submodules such as a Sign Similarity Computing Unit, which calculates the similarity between tokens using a newly introduced similarity metric; a Sign Scratchpad, which is a lightweight, image-width-sized memory that stores previous tokens; a Sign Scratchpad Managing Unit, which controls the Sign Scratchpad; and a Token Integration Map to facilitate efficient, image-Adaptive token merging. Our evaluations demonstrate that AdapTiV achieves, on average, 309.4 ×, 18.4×, 89.8×, 6.3× speedups and 262.1×, 21.5×, 496.6×, 11.2× improvements in energy efficiency over edge CPUs, edge GPUs, server CPUs, and server GPUs, while maintaining an accuracy loss below 1 % without additional training.

AB - The advent of Vision Transformers (ViT) has set a new performance leap in computer vision by leveraging self-Attention mechanisms. However, the computational efficiency of ViTs is limited by the quadratic complexity of self-Attention and redundancy among image tokens. To address these issues, token merging strategies have been explored to reduce input size by merging similar tokens. Nonetheless, implementing token merging presents a degradation of latency performance due to its two factors: inefficient computations and fixed merge rate nature. This paper introduces AdapTiV, a novel hardware-software co-designed accelerator that accelerates ViTs through image-Adaptive token merging, effectively addressing the afore-mentioned challenges. Under the design philosophy of reducing the overhead of token merging and concealing its latency within the Layer Normalization (LN) process, AdapTiV incorporates algorithmic innovations such as Local Matching, which restricts the search space for token merging, thereby reducing the computational complexity; Sign Similarity, which simplifies the calculation of similarity between tokens; and Dynamic Merge Rate, which enables image-Adaptive token merging. Additionally, the hardware component that supports AdapTiV's algorithms, named the Adaptive Token Merging Engine, employs Sign-Driven Scheduling to conceal the overhead of token merging effectively. This engine integrates submodules such as a Sign Similarity Computing Unit, which calculates the similarity between tokens using a newly introduced similarity metric; a Sign Scratchpad, which is a lightweight, image-width-sized memory that stores previous tokens; a Sign Scratchpad Managing Unit, which controls the Sign Scratchpad; and a Token Integration Map to facilitate efficient, image-Adaptive token merging. Our evaluations demonstrate that AdapTiV achieves, on average, 309.4 ×, 18.4×, 89.8×, 6.3× speedups and 262.1×, 21.5×, 496.6×, 11.2× improvements in energy efficiency over edge CPUs, edge GPUs, server CPUs, and server GPUs, while maintaining an accuracy loss below 1 % without additional training.

UR - https://www.scopus.com/pages/publications/85213310284

U2 - 10.1109/MICRO61859.2024.00015

DO - 10.1109/MICRO61859.2024.00015

M3 - Conference contribution

AN - SCOPUS:85213310284

T3 - Proceedings of the Annual International Symposium on Microarchitecture, MICRO

SP - 64

EP - 77

BT - Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024

PB - IEEE Computer Society

Y2 - 2 November 2024 through 6 November 2024

ER -

Yoo S, Kim H[, Kim JY](https://pure.kaist.ac.kr/en/persons/joo-young-kim/). [AdapTiV: Sign-Similarity Based Image-Adaptive Token Merging for Vision Transformer Acceleration](https://pure.kaist.ac.kr/en/publications/adaptiv-sign-similarity-based-image-adaptive-token-merging-for-vi/). In Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society. 2024. p. 64-77. (Proceedings of the Annual International Symposium on Microarchitecture, MICRO). doi: 10.1109/MICRO61859.2024.00015

- 
- [](https://www.facebook.com/sharer.php?u=https://pure.kaist.ac.kr/en/publications/adaptiv-sign-similarity-based-image-adaptive-token-merging-for-vi/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00015&p%5Bsummary%5D=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+AdapTiV%3A+Sign-Similarity+Based+Image-Adaptive+Token+Merging+for+Vision+Transformer+Acceleration)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://pure.kaist.ac.kr/en/publications/adaptiv-sign-similarity-based-image-adaptive-token-merging-for-vi/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00015&text=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+AdapTiV%3A+Sign-Similarity+Based+Image-Adaptive+Token+Merging+for+Vision+Transformer+Acceleration)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://pure.kaist.ac.kr/en/publications/adaptiv-sign-similarity-based-image-adaptive-token-merging-for-vi/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00015&summary=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+AdapTiV%3A+Sign-Similarity+Based+Image-Adaptive+Token+Merging+for+Vision+Transformer+Acceleration)
- [](/cdn-cgi/l/email-protection#69561a1c0b030c0a1d54280d08193d003f4c5a284c5b593a000e07443a00040005081b001d104c5b592b081a0c0d4c5b592004080e0c44280d08191d001f0c4c5b593d06020c074c5b59240c1b0e00070e4c5b590f061b4c5b593f001a0006074c5b593d1b08071a0f061b040c1b4c5b59280a0a0c050c1b081d0006074f0b060d10542a010c0a024c5b59061c1d4c5b591d01001a4c5b591b0c1a0c081b0a014c5b59061c1d191c1d4c5b59081d4c5b5922061b0c084c5b59280d1f08070a0c0d4c5b5920071a1d001d1c1d0c4c5b59060f4c5b593a0a000c070a0c4c5b5908070d4c5b593d0c0a01070605060e104c5a284c5b59280d08193d003f4c5a284c5b593a000e07443a00040005081b001d104c5b592b081a0c0d4c5b592004080e0c44280d08191d001f0c4c5b593d06020c074c5b59240c1b0e00070e4c5b590f061b4c5b593f001a0006074c5b593d1b08071a0f061b040c1b4c5b59280a0a0c050c1b081d000607491549011d1d191a534646191c1b0c470208001a1d47080a47021b460c0746191c0b05000a081d0006071a46080d08191d001f441a000e07441a00040005081b001d10440b081a0c0d440004080e0c44080d08191d001f0c441d06020c0744040c1b0e00070e440f061b441f0046561c1d04361a061c1b0a0c540c040800054f080419521c1d0436040c0d001c04540c040800054f080419521c1d04360a08041908000e07541a01081b0c05000702)
