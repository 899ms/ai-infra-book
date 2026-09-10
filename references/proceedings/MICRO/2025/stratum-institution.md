<!-- 从 stratum-institution.html 迁移的资料快照；原始 HTML SHA-256: 54d4d10edefff22b8fe4f58dd5f1cad7673ab76ee1d69eda4d11465fa83f469e。 -->

# Stratum: System-Hardware Co-Design with Tiered Monolithic 3D-Stackable DRAM for Efficient MoE Serving

Yue Pan

, Zihan Xia

, Po Kai Hsu

, Lanxiang Hu

, Hyungyo Kim

, Janak Sharda

, Minxuan Zhou

, [Nam Sung Kim](https://experts.illinois.edu/en/persons/nam-sung-kim/)

, Shimeng Yu

, Tajana Rosing

, Mingu Kang

- [Electrical and Computer Engineering](https://experts.illinois.edu/en/organisations/electrical-and-computer-engineering/)
- [Siebel School of Computing and Data Science](https://experts.illinois.edu/en/organisations/siebel-school-of-computing-and-data-science-2/)
- [Coordinated Science Lab](https://experts.illinois.edu/en/organisations/coordinated-science-lab/)
- [National Center for Supercomputing Applications (NCSA)](https://experts.illinois.edu/en/organisations/national-center-for-supercomputing-applications-ncsa/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

- [ Overview ](/en/publications/stratum-system-hardware-co-design-with-tiered-monolithic-3d-stack/)
- [ Fingerprint ](/en/publications/stratum-system-hardware-co-design-with-tiered-monolithic-3d-stack/fingerprints/)

## Abstract

As Large Language Models (LLMs) continue to evolve, Mixture of Experts (MoE) architecture has emerged as a prevailing design for achieving state-of-the-art performance across a wide range of tasks. MoE models use sparse gating to activate only a handful of expert sub-networks per input, achieving billion-parameter capacity with inference costs akin to much smaller models. However, such models often pose challenges for hardware deployment due to the massive data volume introduced by the MoE layers. To address the challenges of serving MoE models, we propose Stratum, a system-hardware co-design approach that combines the novel memory technology Monolithic 3D-Stackable DRAM (Mono3D DRAM), near-memory processing (NMP), and GPU acceleration. The logic and Mono3D DRAM dies are connected through hybrid bonding, whereas the Mono3D DRAM stack and GPU are interconnected via silicon interposer. Mono3D DRAM offers higher internal bandwidth than HBM thanks to the dense vertical interconnect pitch enabled by its monolithic structure, which supports implementations of higher-performance near-memory processing. Furthermore, we tackle the latency differences introduced by aggressive vertical scaling of Mono3D DRAM along the z-dimension by constructing internal memory tiers and assigning data across layers based on access likelihood, guided by topic-based expert usage prediction to boost NMP throughput. The Stratum system achieves up to 8.29 × improvement in decoding throughput and 7.66 × better energy efficiency across various benchmarks compared to GPU baselines.

[TABLE]

### Publication series

|  |  |
|----|----|
| Name | Proceedings of the Annual International Symposium on Microarchitecture, MICRO |
| Volume | Part of 213862 |
| ISSN (Print) | 1072-4451 |

### Conference

|  |  |
|----|----|
| Conference | 58th IEEE/ACM International Symposium on Microarchitecture , MICRO 2025 |
| Country/Territory | Korea, Republic of |
| City | Seoul |
| Period | 10/18/25 → 10/22/25 |

## Keywords

- Mixture-of-Experts
- Monolithic 3D DRAM
- Processing Near Memory
- System-Hardware Co-Design

## ASJC Scopus subject areas

- Hardware and Architecture

## Online availability

- [10.1145/3725843.3756043](https://doi.org/10.1145/3725843.3756043)

## Library availability

[Discover UIUC Full Text](https://i-share-uiu.primo.exlibrisgroup.com/openurl/01CARLI_UIU/01CARLI_UIU:CARLI_UIU?ctx_ver=Z39.88-2004&ctx_tim=2026-09-04T06%3A09%3A30UTC&ctx_enc=info%3Aofi%2FencUTF-8&url_ver=Z39.88-2004&url_ctx_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Actx&rft.genre=bookitem&rft_val_fmt=info%3Aofi%2Fkev%3Afmt%3Abook&rfr_id=info%3Asid%2Fpure.atira.dk%3Apure&rft.atitle=Stratum&rft_id=info%3Adoi%2F10.1145%2F3725843.3756043&rft.aulast=Pan&rft.aufirst=Yue&rft.auinit=Y&rft.date=2025-10-17&rft.pages=1-17&rft.btitle=MICRO%202025%20-%2058th%20IEEE%2FACM%20International%20Symposium%20on%20Microarchitecture&rft.pub=IEEE%20Computer%20Society)

## Related links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/105021335073)

- [Link to the citations in Scopus](https://www.scopus.com/pages/publications/105021335073#tab=citedBy)

##  Fingerprint

Dive into the research topics of 'Stratum: System-Hardware Co-Design with Tiered Monolithic 3D-Stackable DRAM for Efficient MoE Serving'. Together they form a unique fingerprint.

-  Stacked DRAM Keyphrases 100%
-  Hardware-software Co-design Keyphrases 100%
-  Mixture-of-Experts Keyphrases 100%
-  Monolithic 3D Keyphrases 100%
-  Hardware Co-Design Computer Science 100%
-  Graphics Processing Unit Computer Science 100%
-  Near-memory Computing Keyphrases 50%
-  GPU Keyphrases 33%

[ View full fingerprint ](/en/publications/stratum-system-hardware-co-design-with-tiered-monolithic-3d-stack/fingerprints/)

## Cite this

- APA
- Standard
- Harvard
- Vancouver
- Author
- BIBTEX
- RIS

Pan, Y., Xia, Z., Hsu, P. K., Hu, L., Kim, H., Sharda, J., Zhou, M.[, Kim, N. S.](https://experts.illinois.edu/en/persons/nam-sung-kim/), Yu, S., Rosing, T., & Kang, M. (2025). [Stratum: System-Hardware Co-Design with Tiered Monolithic 3D-Stackable DRAM for Efficient MoE Serving](https://experts.illinois.edu/en/publications/stratum-system-hardware-co-design-with-tiered-monolithic-3d-stack/). In *MICRO 2025 - 58th IEEE/ACM International Symposium on Microarchitecture* (pp. 1-17). (Proceedings of the Annual International Symposium on Microarchitecture, MICRO; Vol. Part of 213862). IEEE Computer Society. [https://doi.org/10.1145/3725843.3756043](https://doi.org/10.1145/3725843.3756043)

[**Stratum: System-Hardware Co-Design with Tiered Monolithic 3D-Stackable DRAM for Efficient MoE Serving.**](https://experts.illinois.edu/en/publications/stratum-system-hardware-co-design-with-tiered-monolithic-3d-stack/) / Pan, Yue; Xia, Zihan; Hsu, Po Kai et al.  
MICRO 2025 - 58th IEEE/ACM International Symposium on Microarchitecture. IEEE Computer Society, 2025. p. 1-17 (Proceedings of the Annual International Symposium on Microarchitecture, MICRO; Vol. Part of 213862).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

Pan, Y, Xia, Z, Hsu, PK, Hu, L, Kim, H, Sharda, J, Zhou, M[, Kim, NS](https://experts.illinois.edu/en/persons/nam-sung-kim/), Yu, S, Rosing, T & Kang, M 2025, [Stratum: System-Hardware Co-Design with Tiered Monolithic 3D-Stackable DRAM for Efficient MoE Serving](https://experts.illinois.edu/en/publications/stratum-system-hardware-co-design-with-tiered-monolithic-3d-stack/). in *MICRO 2025 - 58th IEEE/ACM International Symposium on Microarchitecture.* Proceedings of the Annual International Symposium on Microarchitecture, MICRO, vol. Part of 213862, IEEE Computer Society, pp. 1-17, 58th IEEE/ACM International Symposium on Microarchitecture , MICRO 2025, Seoul, Korea, Republic of, 10/18/25. [https://doi.org/10.1145/3725843.3756043](https://doi.org/10.1145/3725843.3756043)

Pan Y, Xia Z, Hsu PK, Hu L, Kim H, Sharda J et al. [Stratum: System-Hardware Co-Design with Tiered Monolithic 3D-Stackable DRAM for Efficient MoE Serving](https://experts.illinois.edu/en/publications/stratum-system-hardware-co-design-with-tiered-monolithic-3d-stack/). In MICRO 2025 - 58th IEEE/ACM International Symposium on Microarchitecture. IEEE Computer Society. 2025. p. 1-17. (Proceedings of the Annual International Symposium on Microarchitecture, MICRO). Epub 2025 Oct 17. doi: 10.1145/3725843.3756043

Pan, Yue ; Xia, Zihan ; Hsu, Po Kai et al. / [**Stratum : System-Hardware Co-Design with Tiered Monolithic 3D-Stackable DRAM for Efficient MoE Serving**](https://experts.illinois.edu/en/publications/stratum-system-hardware-co-design-with-tiered-monolithic-3d-stack/). MICRO 2025 - 58th IEEE/ACM International Symposium on Microarchitecture. IEEE Computer Society, 2025. pp. 1-17 (Proceedings of the Annual International Symposium on Microarchitecture, MICRO).

@inproceedings{9c95e846deab47ddae6e09e9e1ad89f2,

title = "Stratum: System-Hardware Co-Design with Tiered Monolithic 3D-Stackable DRAM for Efficient MoE Serving",

abstract = "As Large Language Models (LLMs) continue to evolve, Mixture of Experts (MoE) architecture has emerged as a prevailing design for achieving state-of-the-art performance across a wide range of tasks. MoE models use sparse gating to activate only a handful of expert sub-networks per input, achieving billion-parameter capacity with inference costs akin to much smaller models. However, such models often pose challenges for hardware deployment due to the massive data volume introduced by the MoE layers. To address the challenges of serving MoE models, we propose Stratum, a system-hardware co-design approach that combines the novel memory technology Monolithic 3D-Stackable DRAM (Mono3D DRAM), near-memory processing (NMP), and GPU acceleration. The logic and Mono3D DRAM dies are connected through hybrid bonding, whereas the Mono3D DRAM stack and GPU are interconnected via silicon interposer. Mono3D DRAM offers higher internal bandwidth than HBM thanks to the dense vertical interconnect pitch enabled by its monolithic structure, which supports implementations of higher-performance near-memory processing. Furthermore, we tackle the latency differences introduced by aggressive vertical scaling of Mono3D DRAM along the z-dimension by constructing internal memory tiers and assigning data across layers based on access likelihood, guided by topic-based expert usage prediction to boost NMP throughput. The Stratum system achieves up to 8.29 {\texttimes} improvement in decoding throughput and 7.66 {\texttimes} better energy efficiency across various benchmarks compared to GPU baselines.",

keywords = "Mixture-of-Experts, Monolithic 3D DRAM, Processing Near Memory, System-Hardware Co-Design",

author = "Yue Pan and Zihan Xia and Hsu, \\Po Kai\\ and Lanxiang Hu and Hyungyo Kim and Janak Sharda and Minxuan Zhou and Kim, \\Nam Sung\\ and Shimeng Yu and Tajana Rosing and Mingu Kang",

note = "This work was supported in part by PRISM and CoCoSys, centers in JUMP 2.0, an SRC program sponsored by DARPA. This research is also supported by National Science Foundation (NSF) grants 2112665, 2112167, 2003279, 2120019, and 2211386.; 58th IEEE/ACM International Symposium on Microarchitecture , MICRO 2025 ; Conference date: 18-10-2025 Through 22-10-2025",

year = "2025",

month = oct,

day = "17",

doi = "10.1145/3725843.3756043",

language = "English (US)",

series = "Proceedings of the Annual International Symposium on Microarchitecture, MICRO",

publisher = "IEEE Computer Society",

pages = "1--17",

booktitle = "MICRO 2025 - 58th IEEE/ACM International Symposium on Microarchitecture",

}

TY - GEN

T1 - Stratum

T2 - 58th IEEE/ACM International Symposium on Microarchitecture , MICRO 2025

AU - Pan, Yue

AU - Xia, Zihan

AU - Hsu, Po Kai

AU - Hu, Lanxiang

AU - Kim, Hyungyo

AU - Sharda, Janak

AU - Zhou, Minxuan

AU - Kim, Nam Sung

AU - Yu, Shimeng

AU - Rosing, Tajana

AU - Kang, Mingu

N1 - This work was supported in part by PRISM and CoCoSys, centers in JUMP 2.0, an SRC program sponsored by DARPA. This research is also supported by National Science Foundation (NSF) grants 2112665, 2112167, 2003279, 2120019, and 2211386.

PY - 2025/10/17

Y1 - 2025/10/17

N2 - As Large Language Models (LLMs) continue to evolve, Mixture of Experts (MoE) architecture has emerged as a prevailing design for achieving state-of-the-art performance across a wide range of tasks. MoE models use sparse gating to activate only a handful of expert sub-networks per input, achieving billion-parameter capacity with inference costs akin to much smaller models. However, such models often pose challenges for hardware deployment due to the massive data volume introduced by the MoE layers. To address the challenges of serving MoE models, we propose Stratum, a system-hardware co-design approach that combines the novel memory technology Monolithic 3D-Stackable DRAM (Mono3D DRAM), near-memory processing (NMP), and GPU acceleration. The logic and Mono3D DRAM dies are connected through hybrid bonding, whereas the Mono3D DRAM stack and GPU are interconnected via silicon interposer. Mono3D DRAM offers higher internal bandwidth than HBM thanks to the dense vertical interconnect pitch enabled by its monolithic structure, which supports implementations of higher-performance near-memory processing. Furthermore, we tackle the latency differences introduced by aggressive vertical scaling of Mono3D DRAM along the z-dimension by constructing internal memory tiers and assigning data across layers based on access likelihood, guided by topic-based expert usage prediction to boost NMP throughput. The Stratum system achieves up to 8.29 × improvement in decoding throughput and 7.66 × better energy efficiency across various benchmarks compared to GPU baselines.

AB - As Large Language Models (LLMs) continue to evolve, Mixture of Experts (MoE) architecture has emerged as a prevailing design for achieving state-of-the-art performance across a wide range of tasks. MoE models use sparse gating to activate only a handful of expert sub-networks per input, achieving billion-parameter capacity with inference costs akin to much smaller models. However, such models often pose challenges for hardware deployment due to the massive data volume introduced by the MoE layers. To address the challenges of serving MoE models, we propose Stratum, a system-hardware co-design approach that combines the novel memory technology Monolithic 3D-Stackable DRAM (Mono3D DRAM), near-memory processing (NMP), and GPU acceleration. The logic and Mono3D DRAM dies are connected through hybrid bonding, whereas the Mono3D DRAM stack and GPU are interconnected via silicon interposer. Mono3D DRAM offers higher internal bandwidth than HBM thanks to the dense vertical interconnect pitch enabled by its monolithic structure, which supports implementations of higher-performance near-memory processing. Furthermore, we tackle the latency differences introduced by aggressive vertical scaling of Mono3D DRAM along the z-dimension by constructing internal memory tiers and assigning data across layers based on access likelihood, guided by topic-based expert usage prediction to boost NMP throughput. The Stratum system achieves up to 8.29 × improvement in decoding throughput and 7.66 × better energy efficiency across various benchmarks compared to GPU baselines.

KW - Mixture-of-Experts

KW - Monolithic 3D DRAM

KW - Processing Near Memory

KW - System-Hardware Co-Design

UR - https://www.scopus.com/pages/publications/105021335073

UR - https://www.scopus.com/pages/publications/105021335073#tab=citedBy

U2 - 10.1145/3725843.3756043

DO - 10.1145/3725843.3756043

M3 - Conference contribution

AN - SCOPUS:105021335073

T3 - Proceedings of the Annual International Symposium on Microarchitecture, MICRO

SP - 1

EP - 17

BT - MICRO 2025 - 58th IEEE/ACM International Symposium on Microarchitecture

PB - IEEE Computer Society

Y2 - 18 October 2025 through 22 October 2025

ER -

- 
- [](https://www.facebook.com/sharer.php?u=https://experts.illinois.edu/en/publications/stratum-system-hardware-co-design-with-tiered-monolithic-3d-stack/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3725843.3756043&p%5Bsummary%5D=Check+out+this+research+output+at+Illinois+Experts%3A+Stratum%3A+System-Hardware+Co-Design+with+Tiered+Monolithic+3D-Stackable+DRAM+for+Efficient+MoE+Serving)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://experts.illinois.edu/en/publications/stratum-system-hardware-co-design-with-tiered-monolithic-3d-stack/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3725843.3756043&text=Check+out+this+research+output+at+Illinois+Experts%3A+Stratum%3A+System-Hardware+Co-Design+with+Tiered+Monolithic+3D-Stackable+DRAM+for+Efficient+MoE+Serving)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://experts.illinois.edu/en/publications/stratum-system-hardware-co-design-with-tiered-monolithic-3d-stack/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1145%2F3725843.3756043&summary=Check+out+this+research+output+at+Illinois+Experts%3A+Stratum%3A+System-Hardware+Co-Design+with+Tiered+Monolithic+3D-Stackable+DRAM+for+Efficient+MoE+Serving)
- [](/cdn-cgi/l/email-protection#a798d4d2c5cdc2c4d39af4d3d5c6d3d2ca8294e6829597f4ded4d3c2ca8aefc6d5c3d0c6d5c2829597e4c88ae3c2d4cec0c9829597d0ced3cf829597f3cec2d5c2c3829597eac8c9c8cbced3cfcec482959794e38af4d3c6c4ccc6c5cbc2829597e3f5e6ea829597c1c8d5829597e2c1c1cec4cec2c9d3829597eac8e2829597f4c2d5d1cec9c081c5c8c3de9ae4cfc2c4cc829597c8d2d3829597d3cfced4829597d5c2d4c2c6d5c4cf829597c8d2d3d7d2d3829597c6d3829597eecbcbcec9c8ced4829597e2dfd7c2d5d3d48294e6829597f4d3d5c6d3d2ca8294e6829597f4ded4d3c2ca8aefc6d5c3d0c6d5c2829597e4c88ae3c2d4cec0c9829597d0ced3cf829597f3cec2d5c2c3829597eac8c9c8cbced3cfcec482959794e38af4d3c6c4ccc6c5cbc2829597e3f5e6ea829597c1c8d5829597e2c1c1cec4cec2c9d3829597eac8e2829597f4c2d5d1cec9c087db87cfd3d3d7d49d8888c2dfd7c2d5d3d489cecbcbcec9c8ced489c2c3d288c2c988d7d2c5cbcec4c6d3cec8c9d488d4d3d5c6d3d2ca8ad4ded4d3c2ca8acfc6d5c3d0c6d5c28ac4c88ac3c2d4cec0c98ad0ced3cf8ad3cec2d5c2c38acac8c9c8cbced3cfcec48a94c38ad4d3c6c4cc8898d2d3caf8d4c8d2d5c4c29ac2cac6cecb81c6cad79cd2d3caf8cac2c3ced2ca9ac2cac6cecb81c6cad79cd2d3caf8c4c6cad7c6cec0c99ad4cfc6d5c2cbcec9cc)
