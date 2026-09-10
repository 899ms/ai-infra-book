<!-- 从 mosaic-institution.html 迁移的资料快照；原始 HTML SHA-256: a37fe97ebd61d5cca2349ad4f6fa36a18047af705c39cd0f08f516426196aa29。 -->

# Mosaic: Harnessing the Micro-Architectural Resources of Servers in Serverless Environments

Jovan Stojkovic

, Esha Choukse

, Enrique Saurez

, Inigo Goiri

, [Josep Torrellas](https://experts.illinois.edu/en/persons/josep-torrellas/)

- [Siebel School of Computing and Data Science](https://experts.illinois.edu/en/organisations/siebel-school-of-computing-and-data-science-2/)
- [Electrical and Computer Engineering](https://experts.illinois.edu/en/organisations/electrical-and-computer-engineering/)
- [Information Trust Institute](https://experts.illinois.edu/en/organisations/information-trust-institute/)
- [Coordinated Science Lab](https://experts.illinois.edu/en/organisations/coordinated-science-lab/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

[](https://plu.mx/plum/a/?doi=10.1109/MICRO61859.2024.00103)

- [ Overview ](/en/publications/mosaic-harnessing-the-micro-architectural-resources-of-servers-in/)
- [ Fingerprint ](/en/publications/mosaic-harnessing-the-micro-architectural-resources-of-servers-in/fingerprints/)

## Abstract

With serverless computing, users develop scalable applications using lightweight functions as building blocks, while cloud providers own most of the computing stack, allowing for better resource optimizations. In this paper, we observe that modern server-class processors are inefficiently utilized in serverless environments. Cores perform frequent context switches within function invocations and have a high degree of oversubscription. In such an environment, functions frequently lose their micro-architectural state in stateful hardware structures like caches, TLBs, and branch predictors, causing performance degradation. At the same time, modern processors are dimensioned for the needs of a broad set of applications, rendering them suboptimal for serverless workloads. Based on these insights, we propose Mosaic, an architecture optimized for serverless environments that maintains generality to efficiently support other workloads. Mosaic has two components: (1) MosaicCPU, a processor architecture that efficiently runs both serverless workloads and traditional monolithic applications, and (2) MosaicScheduler, a software stack for serverless systems that maximizes the benefits of MosaicCPU. MosaicCPU slices micro-architectural structures into small chunks and assigns tiles of such chunks to functions. The processor retains the state of functions in their tiles across context switches, thereby improving performance. Furthermore, currently-inactive tiles are set to a low power mode, thereby reducing energy consumption. In addition, MosaicScheduler maximizes efficiency by introducing predictive right-sizing of the per-function tiles, alongside with smart scheduling based on the state of the tiles. Overall, compared to conventional server-class processors, Mosaic improves the throughput of serverless workloads by 225% while using 22% less power.

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
| Period | 11/2/24 → 11/6/24 |

## Keywords

- Cloud computing
- Hardware partitioning
- Serverless computing

## ASJC Scopus subject areas

- Hardware and Architecture

## Online availability

- [10.1109/MICRO61859.2024.00103](https://doi.org/10.1109/MICRO61859.2024.00103)

## Library availability

[Discover UIUC Full Text](https://i-share-uiu.primo.exlibrisgroup.com/openurl/01CARLI_UIU/01CARLI_UIU:CARLI_UIU?ctx_ver=Z39.88-2004&ctx_tim=2026-09-01T06%3A42%3A32UTC&ctx_enc=info%3Aofi%2FencUTF-8&url_ver=Z39.88-2004&url_ctx_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Actx&rft.genre=bookitem&rft_val_fmt=info%3Aofi%2Fkev%3Afmt%3Abook&rfr_id=info%3Asid%2Fpure.atira.dk%3Apure&rft.atitle=Mosaic&rft_id=info%3Adoi%2F10.1109%2FMICRO61859.2024.00103&rft.aulast=Stojkovic&rft.aufirst=Jovan&rft.auinit=J&rft.date=2024&rft.pages=1397-1412&rft.btitle=Proceedings%20-%202024%2057th%20Annual%20IEEE%2FACM%20International%20Symposium%20on%20Microarchitecture%2C%20MICRO%202024&rft.pub=IEEE%20Computer%20Society)

## Related links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/85213367985)

- [Link to the citations in Scopus](https://www.scopus.com/pages/publications/85213367985#tab=citedBy)

##  Fingerprint

Dive into the research topics of 'Mosaic: Harnessing the Micro-Architectural Resources of Servers in Serverless Environments'. Together they form a unique fingerprint.

-  Server-Class Computer Science 100%
-  Microarchitecture Keyphrases 100%
-  Serverless Computing Keyphrases 100%
-  Building-Blocks Computer Science 50%
-  Energy Consumption Computer Science 50%
-  Performance Degradation Computer Science 50%
-  Software Stack Computer Science 50%
-  Modern Processor Computer Science 50%

[ View full fingerprint ](/en/publications/mosaic-harnessing-the-micro-architectural-resources-of-servers-in/fingerprints/)

## Cite this

- APA
- Standard
- Harvard
- Vancouver
- Author
- BIBTEX
- RIS

Stojkovic, J., Choukse, E., Saurez, E., Goiri, I.[, & Torrellas, J.](https://experts.illinois.edu/en/persons/josep-torrellas/) (2024). [Mosaic: Harnessing the Micro-Architectural Resources of Servers in Serverless Environments](https://experts.illinois.edu/en/publications/mosaic-harnessing-the-micro-architectural-resources-of-servers-in/). In *Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024* (pp. 1397-1412). (Proceedings of the Annual International Symposium on Microarchitecture, MICRO). IEEE Computer Society. [https://doi.org/10.1109/MICRO61859.2024.00103](https://doi.org/10.1109/MICRO61859.2024.00103)

[**Mosaic: Harnessing the Micro-Architectural Resources of Servers in Serverless Environments.**](https://experts.illinois.edu/en/publications/mosaic-harnessing-the-micro-architectural-resources-of-servers-in/) / Stojkovic, Jovan; Choukse, Esha; Saurez, Enrique et al.  
Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society, 2024. p. 1397-1412 (Proceedings of the Annual International Symposium on Microarchitecture, MICRO).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution

Stojkovic, J, Choukse, E, Saurez, E, Goiri, I[ & Torrellas, J](https://experts.illinois.edu/en/persons/josep-torrellas/) 2024, [Mosaic: Harnessing the Micro-Architectural Resources of Servers in Serverless Environments](https://experts.illinois.edu/en/publications/mosaic-harnessing-the-micro-architectural-resources-of-servers-in/). in *Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024.* Proceedings of the Annual International Symposium on Microarchitecture, MICRO, IEEE Computer Society, pp. 1397-1412, 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024, Austin, United States, 11/2/24. [https://doi.org/10.1109/MICRO61859.2024.00103](https://doi.org/10.1109/MICRO61859.2024.00103)

Stojkovic J, Choukse E, Saurez E, Goiri I[, Torrellas J](https://experts.illinois.edu/en/persons/josep-torrellas/). [Mosaic: Harnessing the Micro-Architectural Resources of Servers in Serverless Environments](https://experts.illinois.edu/en/publications/mosaic-harnessing-the-micro-architectural-resources-of-servers-in/). In Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society. 2024. p. 1397-1412. (Proceedings of the Annual International Symposium on Microarchitecture, MICRO). doi: 10.1109/MICRO61859.2024.00103

Stojkovic, Jovan ; Choukse, Esha ; Saurez, Enrique et al. / [**Mosaic : Harnessing the Micro-Architectural Resources of Servers in Serverless Environments**](https://experts.illinois.edu/en/publications/mosaic-harnessing-the-micro-architectural-resources-of-servers-in/). Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society, 2024. pp. 1397-1412 (Proceedings of the Annual International Symposium on Microarchitecture, MICRO).

@inproceedings{d7cf3ca0ced5436cb99c54ee077c2c28,

title = "Mosaic: Harnessing the Micro-Architectural Resources of Servers in Serverless Environments",

abstract = "With serverless computing, users develop scalable applications using lightweight functions as building blocks, while cloud providers own most of the computing stack, allowing for better resource optimizations. In this paper, we observe that modern server-class processors are inefficiently utilized in serverless environments. Cores perform frequent context switches within function invocations and have a high degree of oversubscription. In such an environment, functions frequently lose their micro-architectural state in stateful hardware structures like caches, TLBs, and branch predictors, causing performance degradation. At the same time, modern processors are dimensioned for the needs of a broad set of applications, rendering them suboptimal for serverless workloads. Based on these insights, we propose Mosaic, an architecture optimized for serverless environments that maintains generality to efficiently support other workloads. Mosaic has two components: (1) MosaicCPU, a processor architecture that efficiently runs both serverless workloads and traditional monolithic applications, and (2) MosaicScheduler, a software stack for serverless systems that maximizes the benefits of MosaicCPU. MosaicCPU slices micro-architectural structures into small chunks and assigns tiles of such chunks to functions. The processor retains the state of functions in their tiles across context switches, thereby improving performance. Furthermore, currently-inactive tiles are set to a low power mode, thereby reducing energy consumption. In addition, MosaicScheduler maximizes efficiency by introducing predictive right-sizing of the per-function tiles, alongside with smart scheduling based on the state of the tiles. Overall, compared to conventional server-class processors, Mosaic improves the throughput of serverless workloads by 225\\ while using 22\\ less power.",

keywords = "Cloud computing, Hardware partitioning, Serverless computing",

author = "Jovan Stojkovic and Esha Choukse and Enrique Saurez and Inigo Goiri and Josep Torrellas",

note = "This work was supported in part by NSF under grants CNS 1956007, CCF 2107470 and CCF 2316233; and by ACE, one of the seven centers in JUMP 2.0, a Semiconductor Research Corporation (SRC) program sponsored by DARPA.; 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024 ; Conference date: 02-11-2024 Through 06-11-2024",

year = "2024",

doi = "10.1109/MICRO61859.2024.00103",

language = "English (US)",

series = "Proceedings of the Annual International Symposium on Microarchitecture, MICRO",

publisher = "IEEE Computer Society",

pages = "1397--1412",

booktitle = "Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024",

}

TY - GEN

T1 - Mosaic

T2 - 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024

AU - Stojkovic, Jovan

AU - Choukse, Esha

AU - Saurez, Enrique

AU - Goiri, Inigo

AU - Torrellas, Josep

N1 - This work was supported in part by NSF under grants CNS 1956007, CCF 2107470 and CCF 2316233; and by ACE, one of the seven centers in JUMP 2.0, a Semiconductor Research Corporation (SRC) program sponsored by DARPA.

PY - 2024

Y1 - 2024

N2 - With serverless computing, users develop scalable applications using lightweight functions as building blocks, while cloud providers own most of the computing stack, allowing for better resource optimizations. In this paper, we observe that modern server-class processors are inefficiently utilized in serverless environments. Cores perform frequent context switches within function invocations and have a high degree of oversubscription. In such an environment, functions frequently lose their micro-architectural state in stateful hardware structures like caches, TLBs, and branch predictors, causing performance degradation. At the same time, modern processors are dimensioned for the needs of a broad set of applications, rendering them suboptimal for serverless workloads. Based on these insights, we propose Mosaic, an architecture optimized for serverless environments that maintains generality to efficiently support other workloads. Mosaic has two components: (1) MosaicCPU, a processor architecture that efficiently runs both serverless workloads and traditional monolithic applications, and (2) MosaicScheduler, a software stack for serverless systems that maximizes the benefits of MosaicCPU. MosaicCPU slices micro-architectural structures into small chunks and assigns tiles of such chunks to functions. The processor retains the state of functions in their tiles across context switches, thereby improving performance. Furthermore, currently-inactive tiles are set to a low power mode, thereby reducing energy consumption. In addition, MosaicScheduler maximizes efficiency by introducing predictive right-sizing of the per-function tiles, alongside with smart scheduling based on the state of the tiles. Overall, compared to conventional server-class processors, Mosaic improves the throughput of serverless workloads by 225% while using 22% less power.

AB - With serverless computing, users develop scalable applications using lightweight functions as building blocks, while cloud providers own most of the computing stack, allowing for better resource optimizations. In this paper, we observe that modern server-class processors are inefficiently utilized in serverless environments. Cores perform frequent context switches within function invocations and have a high degree of oversubscription. In such an environment, functions frequently lose their micro-architectural state in stateful hardware structures like caches, TLBs, and branch predictors, causing performance degradation. At the same time, modern processors are dimensioned for the needs of a broad set of applications, rendering them suboptimal for serverless workloads. Based on these insights, we propose Mosaic, an architecture optimized for serverless environments that maintains generality to efficiently support other workloads. Mosaic has two components: (1) MosaicCPU, a processor architecture that efficiently runs both serverless workloads and traditional monolithic applications, and (2) MosaicScheduler, a software stack for serverless systems that maximizes the benefits of MosaicCPU. MosaicCPU slices micro-architectural structures into small chunks and assigns tiles of such chunks to functions. The processor retains the state of functions in their tiles across context switches, thereby improving performance. Furthermore, currently-inactive tiles are set to a low power mode, thereby reducing energy consumption. In addition, MosaicScheduler maximizes efficiency by introducing predictive right-sizing of the per-function tiles, alongside with smart scheduling based on the state of the tiles. Overall, compared to conventional server-class processors, Mosaic improves the throughput of serverless workloads by 225% while using 22% less power.

KW - Cloud computing

KW - Hardware partitioning

KW - Serverless computing

UR - https://www.scopus.com/pages/publications/85213367985

UR - https://www.scopus.com/pages/publications/85213367985#tab=citedBy

U2 - 10.1109/MICRO61859.2024.00103

DO - 10.1109/MICRO61859.2024.00103

M3 - Conference contribution

AN - SCOPUS:85213367985

T3 - Proceedings of the Annual International Symposium on Microarchitecture, MICRO

SP - 1397

EP - 1412

BT - Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024

PB - IEEE Computer Society

Y2 - 2 November 2024 through 6 November 2024

ER -

- 
- [](https://www.facebook.com/sharer.php?u=https://experts.illinois.edu/en/publications/mosaic-harnessing-the-micro-architectural-resources-of-servers-in/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00103&p%5Bsummary%5D=Check+out+this+research+output+at+Illinois+Experts%3A+Mosaic%3A+Harnessing+the+Micro-Architectural+Resources+of+Servers+in+Serverless+Environments)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://experts.illinois.edu/en/publications/mosaic-harnessing-the-micro-architectural-resources-of-servers-in/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00103&text=Check+out+this+research+output+at+Illinois+Experts%3A+Mosaic%3A+Harnessing+the+Micro-Architectural+Resources+of+Servers+in+Serverless+Environments)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://experts.illinois.edu/en/publications/mosaic-harnessing-the-micro-architectural-resources-of-servers-in/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00103&summary=Check+out+this+research+output+at+Illinois+Experts%3A+Mosaic%3A+Harnessing+the+Micro-Architectural+Resources+of+Servers+in+Serverless+Environments)
- [](/cdn-cgi/l/email-protection#83bcf0f6e1e9e6e0f7beceecf0e2eae0a6b0c2a6b1b3cbe2f1ede6f0f0eaede4a6b1b3f7ebe6a6b1b3ceeae0f1ecaec2f1e0ebeaf7e6e0f7f6f1e2efa6b1b3d1e6f0ecf6f1e0e6f0a6b1b3ece5a6b1b3d0e6f1f5e6f1f0a6b1b3eaeda6b1b3d0e6f1f5e6f1efe6f0f0a6b1b3c6edf5eaf1ecedeee6edf7f0a5e1ece7fabec0ebe6e0e8a6b1b3ecf6f7a6b1b3f7ebeaf0a6b1b3f1e6f0e6e2f1e0eba6b1b3ecf6f7f3f6f7a6b1b3e2f7a6b1b3caefefeaedeceaf0a6b1b3c6fbf3e6f1f7f0a6b0c2a6b1b3ceecf0e2eae0a6b0c2a6b1b3cbe2f1ede6f0f0eaede4a6b1b3f7ebe6a6b1b3ceeae0f1ecaec2f1e0ebeaf7e6e0f7f6f1e2efa6b1b3d1e6f0ecf6f1e0e6f0a6b1b3ece5a6b1b3d0e6f1f5e6f1f0a6b1b3eaeda6b1b3d0e6f1f5e6f1efe6f0f0a6b1b3c6edf5eaf1ecedeee6edf7f0a3ffa3ebf7f7f3f0b9acace6fbf3e6f1f7f0adeaefefeaedeceaf0ade6e7f6ace6edacf3f6e1efeae0e2f7eaecedf0aceeecf0e2eae0aeebe2f1ede6f0f0eaede4aef7ebe6aeeeeae0f1ecaee2f1e0ebeaf7e6e0f7f6f1e2efaef1e6f0ecf6f1e0e6f0aeece5aef0e6f1f5e6f1f0aeeaedacbcf6f7eedcf0ecf6f1e0e6bee6eee2eaefa5e2eef3b8f6f7eedceee6e7eaf6eebee6eee2eaefa5e2eef3b8f6f7eedce0e2eef3e2eae4edbef0ebe2f1e6efeaede8)
