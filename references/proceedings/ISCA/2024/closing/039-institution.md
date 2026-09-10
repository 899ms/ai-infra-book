<!-- 从 039-institution.html 迁移的资料快照；原始 HTML SHA-256: c2a7567042480dd49b8a84c47ae849a3956b5e8ee0712edad94e2c67e7f11135。 -->

# BLESS: Bandwidth and Locality Enhanced SMEM Seeding Acceleration for DNA Sequencing

Seunghee Han

, Seungjae Moon

, Teokkyu Suh

, Jae Hoon Heo

, [Joo Young Kim](https://pure.kaist.ac.kr/en/persons/joo-young-kim/)

- [School of Electrical Engineering](https://pure.kaist.ac.kr/en/organisations/school-of-electrical-engineering/)

- Korea Advanced Institute of Science and Technology

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

6 Scopus citations

- [ Overview ](/en/publications/bless-bandwidth-and-locality-enhanced-smem-seeding-acceleration-f/)
- [ Fingerprint ](/en/publications/bless-bandwidth-and-locality-enhanced-smem-seeding-acceleration-f/fingerprints/)

## Abstract

In an era marked by the pervasive spread of harmful viruses like COVID-19, the importance of DNA sequencing has grown significantly, given its crucial role in devising effective countermeasures. The seeding process, which aims to find locations of super-maximal exact matches (SMEM) between the DNA samples and reference genome for comparative analysis, has emerged as a major bottleneck due to its memory-intensive characteristics. The learned index approach has been developed that uses machine learning model to partially predict the location of the exact matches, which has effectively reduced the memory access. However, the lack of locality in the current in dexing structure and randomness at runtime of the seeding workload have constrained the memory bandwidth usage and have limited further performance advantage. In this paper, we propose BLESS, a bandwidth and locality enhanced SMEM seeding accelerator for learned-index-based DNA sequence alignment. BLESS is the first domain-specific seeding accelerator to maximize the potential hardware advantage of the learned index approach. We introduce coarse-fine (CF) block data structure, a novel memory mapping of seeding parameters to exploit spatial locality and increase effective bandwidth usage for any memory type, including high bandwidth memory (HBM). We also develop guaranteed search range update (GSRU) algorithm, a method that exploits caching in the search procedure to enable temporal locality and data reuse. Utilizing the CF block and GSRU algorithm, we develop a multi-core seeding accelerator using HBM with context switching and runtime scheduling for maximum core and memory bandwidth utilization. With these improvements, BLESS achieves 35.65 × and 15.49 × speedup over the state-of-the-art seeding system BWA-MEME and ERT-ASIC, respectively, in raw system performance.

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
| Period | 29/06/24 → 3/07/24 |

## Keywords

- DNA Sequencing
- Data Locality
- Genomics
- Hardware Accelerator
- Read Alignment
- SMEM Seeding
- Software-Hardware Co-design

## Access to Document

- [10.1109/ISCA59077.2024.00049](https://doi.org/10.1109/ISCA59077.2024.00049)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/85201162893)

##  Fingerprint

Dive into the research topics of 'BLESS: Bandwidth and Locality Enhanced SMEM Seeding Acceleration for DNA Sequencing'. Together they form a unique fingerprint.

-  Memory Bandwidth Computer Science 100%
-  Bandwidth Memory Computer Science 100%
-  Update Algorithm Computer Science 100%
-  Data Structure Computer Science 50%
-  Effective Bandwidth Computer Science 50%
-  Comparative Analysis Computer Science 50%
-  Multicore Computer Science 50%
-  Memory Access Computer Science 50%

[ View full fingerprint ](/en/publications/bless-bandwidth-and-locality-enhanced-smem-seeding-acceleration-f/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Han, S., Moon, S., Suh, T., Heo, J. H.[, & Kim, J. Y.](https://pure.kaist.ac.kr/en/persons/joo-young-kim/) (2024). [BLESS: Bandwidth and Locality Enhanced SMEM Seeding Acceleration for DNA Sequencing](https://pure.kaist.ac.kr/en/publications/bless-bandwidth-and-locality-enhanced-smem-seeding-acceleration-f/). In *Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024* (pp. 582-596). (Proceedings - International Symposium on Computer Architecture). Institute of Electrical and Electronics Engineers Inc.. [https://doi.org/10.1109/ISCA59077.2024.00049](https://doi.org/10.1109/ISCA59077.2024.00049)

Han, Seunghee ; Moon, Seungjae ; Suh, Teokkyu et al. / [**BLESS : Bandwidth and Locality Enhanced SMEM Seeding Acceleration for DNA Sequencing**](https://pure.kaist.ac.kr/en/publications/bless-bandwidth-and-locality-enhanced-smem-seeding-acceleration-f/). Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc., 2024. pp. 582-596 (Proceedings - International Symposium on Computer Architecture).

@inproceedings{5e7604f1213241cca1bf130f448c219e,

title = "BLESS: Bandwidth and Locality Enhanced SMEM Seeding Acceleration for DNA Sequencing",

abstract = "In an era marked by the pervasive spread of harmful viruses like COVID-19, the importance of DNA sequencing has grown significantly, given its crucial role in devising effective countermeasures. The seeding process, which aims to find locations of super-maximal exact matches (SMEM) between the DNA samples and reference genome for comparative analysis, has emerged as a major bottleneck due to its memory-intensive characteristics. The learned index approach has been developed that uses machine learning model to partially predict the location of the exact matches, which has effectively reduced the memory access. However, the lack of locality in the current in dexing structure and randomness at runtime of the seeding workload have constrained the memory bandwidth usage and have limited further performance advantage. In this paper, we propose BLESS, a bandwidth and locality enhanced SMEM seeding accelerator for learned-index-based DNA sequence alignment. BLESS is the first domain-specific seeding accelerator to maximize the potential hardware advantage of the learned index approach. We introduce coarse-fine (CF) block data structure, a novel memory mapping of seeding parameters to exploit spatial locality and increase effective bandwidth usage for any memory type, including high bandwidth memory (HBM). We also develop guaranteed search range update (GSRU) algorithm, a method that exploits caching in the search procedure to enable temporal locality and data reuse. Utilizing the CF block and GSRU algorithm, we develop a multi-core seeding accelerator using HBM with context switching and runtime scheduling for maximum core and memory bandwidth utilization. With these improvements, BLESS achieves 35.65 {\texttimes} and 15.49 {\texttimes} speedup over the state-of-the-art seeding system BWA-MEME and ERT-ASIC, respectively, in raw system performance.",

keywords = "DNA Sequencing, Data Locality, Genomics, Hardware Accelerator, Read Alignment, SMEM Seeding, Software-Hardware Co-design",

author = "Seunghee Han and Seungjae Moon and Teokkyu Suh and Heo, \\Jae Hoon\\ and Kim, \\Joo Young\\",

note = "Publisher Copyright: {\textcopyright} 2024 IEEE.; 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024 ; Conference date: 29-06-2024 Through 03-07-2024",

year = "2024",

doi = "10.1109/ISCA59077.2024.00049",

language = "English",

series = "Proceedings - International Symposium on Computer Architecture",

publisher = "Institute of Electrical and Electronics Engineers Inc.",

pages = "582--596",

booktitle = "Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024",

}

Han, S, Moon, S, Suh, T, Heo, JH[ & Kim, JY](https://pure.kaist.ac.kr/en/persons/joo-young-kim/) 2024, [BLESS: Bandwidth and Locality Enhanced SMEM Seeding Acceleration for DNA Sequencing](https://pure.kaist.ac.kr/en/publications/bless-bandwidth-and-locality-enhanced-smem-seeding-acceleration-f/). in *Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024.* Proceedings - International Symposium on Computer Architecture, Institute of Electrical and Electronics Engineers Inc., pp. 582-596, 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024, Buenos Aires, Argentina, 29/06/24. [https://doi.org/10.1109/ISCA59077.2024.00049](https://doi.org/10.1109/ISCA59077.2024.00049)

[**BLESS: Bandwidth and Locality Enhanced SMEM Seeding Acceleration for DNA Sequencing.**](https://pure.kaist.ac.kr/en/publications/bless-bandwidth-and-locality-enhanced-smem-seeding-acceleration-f/) / Han, Seunghee; Moon, Seungjae; Suh, Teokkyu et al.  
Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc., 2024. p. 582-596 (Proceedings - International Symposium on Computer Architecture).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

TY - GEN

T1 - BLESS

T2 - 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024

AU - Han, Seunghee

AU - Moon, Seungjae

AU - Suh, Teokkyu

AU - Heo, Jae Hoon

AU - Kim, Joo Young

N1 - Publisher Copyright: © 2024 IEEE.

PY - 2024

Y1 - 2024

N2 - In an era marked by the pervasive spread of harmful viruses like COVID-19, the importance of DNA sequencing has grown significantly, given its crucial role in devising effective countermeasures. The seeding process, which aims to find locations of super-maximal exact matches (SMEM) between the DNA samples and reference genome for comparative analysis, has emerged as a major bottleneck due to its memory-intensive characteristics. The learned index approach has been developed that uses machine learning model to partially predict the location of the exact matches, which has effectively reduced the memory access. However, the lack of locality in the current in dexing structure and randomness at runtime of the seeding workload have constrained the memory bandwidth usage and have limited further performance advantage. In this paper, we propose BLESS, a bandwidth and locality enhanced SMEM seeding accelerator for learned-index-based DNA sequence alignment. BLESS is the first domain-specific seeding accelerator to maximize the potential hardware advantage of the learned index approach. We introduce coarse-fine (CF) block data structure, a novel memory mapping of seeding parameters to exploit spatial locality and increase effective bandwidth usage for any memory type, including high bandwidth memory (HBM). We also develop guaranteed search range update (GSRU) algorithm, a method that exploits caching in the search procedure to enable temporal locality and data reuse. Utilizing the CF block and GSRU algorithm, we develop a multi-core seeding accelerator using HBM with context switching and runtime scheduling for maximum core and memory bandwidth utilization. With these improvements, BLESS achieves 35.65 × and 15.49 × speedup over the state-of-the-art seeding system BWA-MEME and ERT-ASIC, respectively, in raw system performance.

AB - In an era marked by the pervasive spread of harmful viruses like COVID-19, the importance of DNA sequencing has grown significantly, given its crucial role in devising effective countermeasures. The seeding process, which aims to find locations of super-maximal exact matches (SMEM) between the DNA samples and reference genome for comparative analysis, has emerged as a major bottleneck due to its memory-intensive characteristics. The learned index approach has been developed that uses machine learning model to partially predict the location of the exact matches, which has effectively reduced the memory access. However, the lack of locality in the current in dexing structure and randomness at runtime of the seeding workload have constrained the memory bandwidth usage and have limited further performance advantage. In this paper, we propose BLESS, a bandwidth and locality enhanced SMEM seeding accelerator for learned-index-based DNA sequence alignment. BLESS is the first domain-specific seeding accelerator to maximize the potential hardware advantage of the learned index approach. We introduce coarse-fine (CF) block data structure, a novel memory mapping of seeding parameters to exploit spatial locality and increase effective bandwidth usage for any memory type, including high bandwidth memory (HBM). We also develop guaranteed search range update (GSRU) algorithm, a method that exploits caching in the search procedure to enable temporal locality and data reuse. Utilizing the CF block and GSRU algorithm, we develop a multi-core seeding accelerator using HBM with context switching and runtime scheduling for maximum core and memory bandwidth utilization. With these improvements, BLESS achieves 35.65 × and 15.49 × speedup over the state-of-the-art seeding system BWA-MEME and ERT-ASIC, respectively, in raw system performance.

KW - DNA Sequencing

KW - Data Locality

KW - Genomics

KW - Hardware Accelerator

KW - Read Alignment

KW - SMEM Seeding

KW - Software-Hardware Co-design

UR - https://www.scopus.com/pages/publications/85201162893

U2 - 10.1109/ISCA59077.2024.00049

DO - 10.1109/ISCA59077.2024.00049

M3 - Conference contribution

AN - SCOPUS:85201162893

T3 - Proceedings - International Symposium on Computer Architecture

SP - 582

EP - 596

BT - Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024

PB - Institute of Electrical and Electronics Engineers Inc.

Y2 - 29 June 2024 through 3 July 2024

ER -

Han S, Moon S, Suh T, Heo JH[, Kim JY](https://pure.kaist.ac.kr/en/persons/joo-young-kim/). [BLESS: Bandwidth and Locality Enhanced SMEM Seeding Acceleration for DNA Sequencing](https://pure.kaist.ac.kr/en/publications/bless-bandwidth-and-locality-enhanced-smem-seeding-acceleration-f/). In Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc. 2024. p. 582-596. (Proceedings - International Symposium on Computer Architecture). doi: 10.1109/ISCA59077.2024.00049

- 
- [](https://www.facebook.com/sharer.php?u=https://pure.kaist.ac.kr/en/publications/bless-bandwidth-and-locality-enhanced-smem-seeding-acceleration-f/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FISCA59077.2024.00049&p%5Bsummary%5D=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+BLESS%3A+Bandwidth+and+Locality+Enhanced+SMEM+Seeding+Acceleration+for+DNA+Sequencing)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://pure.kaist.ac.kr/en/publications/bless-bandwidth-and-locality-enhanced-smem-seeding-acceleration-f/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FISCA59077.2024.00049&text=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+BLESS%3A+Bandwidth+and+Locality+Enhanced+SMEM+Seeding+Acceleration+for+DNA+Sequencing)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://pure.kaist.ac.kr/en/publications/bless-bandwidth-and-locality-enhanced-smem-seeding-acceleration-f/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FISCA59077.2024.00049&summary=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+BLESS%3A+Bandwidth+and+Locality+Enhanced+SMEM+Seeding+Acceleration+for+DNA+Sequencing)
- [](/cdn-cgi/l/email-protection#625d111700080701165f202e27313147512347505220030c06150b06160a475052030c064750522e0d01030e0b161b475052270c0a030c010706475052312f272f475052310707060b0c05475052230101070e071003160b0d0c475052040d10475052262c2347505231071317070c010b0c0544000d061b5f210a0701094750520d1716475052160a0b11475052100711070310010a4750520d17161217164750520316475052290d100703475052230614030c0107064750522b0c11160b161716074750520d0447505231010b070c0107475052030c064750523607010a0c0d0e0d051b475123475052202e27313147512347505220030c06150b06160a475052030c064750522e0d01030e0b161b475052270c0a030c010706475052312f272f475052310707060b0c05475052230101070e071003160b0d0c475052040d10475052262c2347505231071317070c010b0c05421e420a16161211584d4d121710074c09030b11164c03014c09104d070c4d1217000e0b0103160b0d0c114d000e0711114f00030c06150b06160a4f030c064f0e0d01030e0b161b4f070c0a030c0107064f110f070f4f110707060b0c054f030101070e071003160b0d0c4f044d5d17160f3d110d171001075f070f030b0e44030f125917160f3d0f07060b170f5f070f030b0e44030f125917160f3d01030f12030b050c5f110a0310070e0b0c09)
