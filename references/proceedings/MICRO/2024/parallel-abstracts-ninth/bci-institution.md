<!-- 从 bci-institution.html 迁移的资料快照；原始 HTML SHA-256: 62a28f114b2f6d3022eaa32da802705258ded0ab376c5254dcff6d4117d7e7f5。 -->

# Rearchitecting a Neuromorphic Processor for Spike-Driven Brain-Computer Interfacing

Hunjun Lee

, Yeongwoo Jang

, Daye Jung

, Seunghyun Song

, [Jangwoo Kim](https://snu.elsevierpure.com/en/persons/jangwoo-kim/)

- [College of Engineering](https://snu.elsevierpure.com/en/organisations/college-of-engineering/)
- [Department of Electrical and Computer Engineering](https://snu.elsevierpure.com/en/organisations/department-of-electrical-and-computer-engineering/)

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

[3   Link opens in a new tab](https://www.scopus.com/pages/publications/85213303624#tab=citedBy) Scopus citations

[](https://plu.mx/plum/a/?doi=10.1109/MICRO61859.2024.00082)

- [ Overview ](/en/publications/rearchitecting-a-neuromorphic-processor-for-spike-driven-brain-co/)
- [ Fingerprint ](/en/publications/rearchitecting-a-neuromorphic-processor-for-spike-driven-brain-co/fingerprints/)

## Abstract

Brain-computer interfaces (BCIs) are electrophysiological devices (e.g., electrode arrays) that connect the brain to a computer. They offer neuroscientific and neurological innovations by utilizing a dedicated processor for continuous BCI signal processing. Recent studies propose a scaled-up BCI that adopts an order of magnitude larger number of electrodes to more precisely interface with the brain. As the BCI scales, utilizing a spike-driven processor emerges as an alternative processing method, where the BCI offloads computations to the processor upon detecting spikes. However, the processor design for spike-driven processing has been relatively unexplored compared to that of the continuous processor. In this work, we propose NeuroLobe, a flexible and efficient processor design for spike-driven processing. The key idea is to utilize a neuromorphic processor to take advantage of its event-driven computing nature. We carefully rearchitect the existing neuromorphic system for the purpose of flexibly and efficiently deploying the BCI algorithms. First, we extend the instruction set architecture of the existing neuromorphic processor to flexibly deploy representative spike-driven BCI algorithms. Second, we redesign the connection controller and execution path to improve the performance. Third, we design a custom synchronization unit for scalable processing. Fourth, we implement a custom software stack to minimize load imbalance among the cores. Lastly, we design a multitask controller to simultaneously process multiple algorithms. We evaluate NeuroLobe on four representative BCI algorithms with 11 configurations. Evaluation results show that NeuroLobe surpasses CPU and GPU in terms of speed and energy efficiency.

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

### Bibliographical note

Publisher Copyright:  
© 2024 IEEE.

## UN SDGs

This output contributes to the following UN [Sustainable Development Goals (SDGs)](https://www.un.org/sustainabledevelopment/sustainable-development-goals/)

1.  ![SDG 7 - Affordable and Clean Energy](/assets/sdg_icons/affordable_and_clean_energy-b8e39c169139faf6df7199566119c3c0.svg "SDG 7 - Affordable and Clean Energy")
    SDG 7 Affordable and Clean Energy

## Keywords

- Brain-Computer Interface
- Flexibility
- Neuromorphic Processor
- Spike

## Access to Document

- [10.1109/MICRO61859.2024.00082](https://doi.org/10.1109/MICRO61859.2024.00082)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/85213303624)

##  Fingerprint

Dive into the research topics of 'Rearchitecting a Neuromorphic Processor for Spike-Driven Brain-Computer Interfacing'. Together they form a unique fingerprint.

-  Computer Interface Computer Science 100%
-  Processor Design Computer Science 25%
-  Evaluation Result Computer Science 12%
-  Graphics Processing Unit Computer Science 12%
-  Processing Method Computer Science 12%
-  Energy Efficiency Computer Science 12%
-  Load Imbalance Computer Science 12%
-  Multiple Process Computer Science 12%

[ View full fingerprint ](/en/publications/rearchitecting-a-neuromorphic-processor-for-spike-driven-brain-co/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Lee, H., Jang, Y., Jung, D., Song, S.[, & Kim, J.](https://snu.elsevierpure.com/en/persons/jangwoo-kim/) (2024). [Rearchitecting a Neuromorphic Processor for Spike-Driven Brain-Computer Interfacing](https://snu.elsevierpure.com/en/publications/rearchitecting-a-neuromorphic-processor-for-spike-driven-brain-co/). In *Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024* (pp. 1073-1089). (Proceedings of the Annual International Symposium on Microarchitecture, MICRO). IEEE Computer Society. [https://doi.org/10.1109/MICRO61859.2024.00082](https://doi.org/10.1109/MICRO61859.2024.00082)

Lee, Hunjun ; Jang, Yeongwoo ; Jung, Daye et al. / [**Rearchitecting a Neuromorphic Processor for Spike-Driven Brain-Computer Interfacing**](https://snu.elsevierpure.com/en/publications/rearchitecting-a-neuromorphic-processor-for-spike-driven-brain-co/). Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society, 2024. pp. 1073-1089 (Proceedings of the Annual International Symposium on Microarchitecture, MICRO).

@inproceedings{cce47adbf65b40deba82fc9536ab2d87,

title = "Rearchitecting a Neuromorphic Processor for Spike-Driven Brain-Computer Interfacing",

abstract = "Brain-computer interfaces (BCIs) are electrophysiological devices (e.g., electrode arrays) that connect the brain to a computer. They offer neuroscientific and neurological innovations by utilizing a dedicated processor for continuous BCI signal processing. Recent studies propose a scaled-up BCI that adopts an order of magnitude larger number of electrodes to more precisely interface with the brain. As the BCI scales, utilizing a spike-driven processor emerges as an alternative processing method, where the BCI offloads computations to the processor upon detecting spikes. However, the processor design for spike-driven processing has been relatively unexplored compared to that of the continuous processor. In this work, we propose NeuroLobe, a flexible and efficient processor design for spike-driven processing. The key idea is to utilize a neuromorphic processor to take advantage of its event-driven computing nature. We carefully rearchitect the existing neuromorphic system for the purpose of flexibly and efficiently deploying the BCI algorithms. First, we extend the instruction set architecture of the existing neuromorphic processor to flexibly deploy representative spike-driven BCI algorithms. Second, we redesign the connection controller and execution path to improve the performance. Third, we design a custom synchronization unit for scalable processing. Fourth, we implement a custom software stack to minimize load imbalance among the cores. Lastly, we design a multitask controller to simultaneously process multiple algorithms. We evaluate NeuroLobe on four representative BCI algorithms with 11 configurations. Evaluation results show that NeuroLobe surpasses CPU and GPU in terms of speed and energy efficiency.",

keywords = "Brain-Computer Interface, Flexibility, Neuromorphic Processor, Spike",

author = "Hunjun Lee and Yeongwoo Jang and Daye Jung and Seunghyun Song and Jangwoo Kim",

note = "Publisher Copyright: {\textcopyright} 2024 IEEE.; 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024 ; Conference date: 02-11-2024 Through 06-11-2024",

year = "2024",

doi = "10.1109/MICRO61859.2024.00082",

language = "English",

series = "Proceedings of the Annual International Symposium on Microarchitecture, MICRO",

publisher = "IEEE Computer Society",

pages = "1073--1089",

booktitle = "Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024",

}

Lee, H, Jang, Y, Jung, D, Song, S[ & Kim, J](https://snu.elsevierpure.com/en/persons/jangwoo-kim/) 2024, [Rearchitecting a Neuromorphic Processor for Spike-Driven Brain-Computer Interfacing](https://snu.elsevierpure.com/en/publications/rearchitecting-a-neuromorphic-processor-for-spike-driven-brain-co/). in *Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024.* Proceedings of the Annual International Symposium on Microarchitecture, MICRO, IEEE Computer Society, pp. 1073-1089, 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024, Austin, United States, 2/11/24. [https://doi.org/10.1109/MICRO61859.2024.00082](https://doi.org/10.1109/MICRO61859.2024.00082)

[**Rearchitecting a Neuromorphic Processor for Spike-Driven Brain-Computer Interfacing.**](https://snu.elsevierpure.com/en/publications/rearchitecting-a-neuromorphic-processor-for-spike-driven-brain-co/) / Lee, Hunjun; Jang, Yeongwoo; Jung, Daye et al.  
Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society, 2024. p. 1073-1089 (Proceedings of the Annual International Symposium on Microarchitecture, MICRO).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

TY - GEN

T1 - Rearchitecting a Neuromorphic Processor for Spike-Driven Brain-Computer Interfacing

AU - Lee, Hunjun

AU - Jang, Yeongwoo

AU - Jung, Daye

AU - Song, Seunghyun

AU - Kim, Jangwoo

N1 - Publisher Copyright: © 2024 IEEE.

PY - 2024

Y1 - 2024

N2 - Brain-computer interfaces (BCIs) are electrophysiological devices (e.g., electrode arrays) that connect the brain to a computer. They offer neuroscientific and neurological innovations by utilizing a dedicated processor for continuous BCI signal processing. Recent studies propose a scaled-up BCI that adopts an order of magnitude larger number of electrodes to more precisely interface with the brain. As the BCI scales, utilizing a spike-driven processor emerges as an alternative processing method, where the BCI offloads computations to the processor upon detecting spikes. However, the processor design for spike-driven processing has been relatively unexplored compared to that of the continuous processor. In this work, we propose NeuroLobe, a flexible and efficient processor design for spike-driven processing. The key idea is to utilize a neuromorphic processor to take advantage of its event-driven computing nature. We carefully rearchitect the existing neuromorphic system for the purpose of flexibly and efficiently deploying the BCI algorithms. First, we extend the instruction set architecture of the existing neuromorphic processor to flexibly deploy representative spike-driven BCI algorithms. Second, we redesign the connection controller and execution path to improve the performance. Third, we design a custom synchronization unit for scalable processing. Fourth, we implement a custom software stack to minimize load imbalance among the cores. Lastly, we design a multitask controller to simultaneously process multiple algorithms. We evaluate NeuroLobe on four representative BCI algorithms with 11 configurations. Evaluation results show that NeuroLobe surpasses CPU and GPU in terms of speed and energy efficiency.

AB - Brain-computer interfaces (BCIs) are electrophysiological devices (e.g., electrode arrays) that connect the brain to a computer. They offer neuroscientific and neurological innovations by utilizing a dedicated processor for continuous BCI signal processing. Recent studies propose a scaled-up BCI that adopts an order of magnitude larger number of electrodes to more precisely interface with the brain. As the BCI scales, utilizing a spike-driven processor emerges as an alternative processing method, where the BCI offloads computations to the processor upon detecting spikes. However, the processor design for spike-driven processing has been relatively unexplored compared to that of the continuous processor. In this work, we propose NeuroLobe, a flexible and efficient processor design for spike-driven processing. The key idea is to utilize a neuromorphic processor to take advantage of its event-driven computing nature. We carefully rearchitect the existing neuromorphic system for the purpose of flexibly and efficiently deploying the BCI algorithms. First, we extend the instruction set architecture of the existing neuromorphic processor to flexibly deploy representative spike-driven BCI algorithms. Second, we redesign the connection controller and execution path to improve the performance. Third, we design a custom synchronization unit for scalable processing. Fourth, we implement a custom software stack to minimize load imbalance among the cores. Lastly, we design a multitask controller to simultaneously process multiple algorithms. We evaluate NeuroLobe on four representative BCI algorithms with 11 configurations. Evaluation results show that NeuroLobe surpasses CPU and GPU in terms of speed and energy efficiency.

KW - Brain-Computer Interface

KW - Flexibility

KW - Neuromorphic Processor

KW - Spike

UR - https://www.scopus.com/pages/publications/85213303624

U2 - 10.1109/MICRO61859.2024.00082

DO - 10.1109/MICRO61859.2024.00082

M3 - Conference contribution

AN - SCOPUS:85213303624

T3 - Proceedings of the Annual International Symposium on Microarchitecture, MICRO

SP - 1073

EP - 1089

BT - Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024

PB - IEEE Computer Society

T2 - 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024

Y2 - 2 November 2024 through 6 November 2024

ER -

Lee H, Jang Y, Jung D, Song S[, Kim J](https://snu.elsevierpure.com/en/persons/jangwoo-kim/). [Rearchitecting a Neuromorphic Processor for Spike-Driven Brain-Computer Interfacing](https://snu.elsevierpure.com/en/publications/rearchitecting-a-neuromorphic-processor-for-spike-driven-brain-co/). In Proceedings - 2024 57th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO 2024. IEEE Computer Society. 2024. p. 1073-1089. (Proceedings of the Annual International Symposium on Microarchitecture, MICRO). doi: 10.1109/MICRO61859.2024.00082

- 
- [](https://www.facebook.com/sharer.php?u=https://snu.elsevierpure.com/en/publications/rearchitecting-a-neuromorphic-processor-for-spike-driven-brain-co/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00082&p%5Bsummary%5D=Check+out+this+research+output+at+Seoul+National+University%3A+Rearchitecting+a+Neuromorphic+Processor+for+Spike-Driven+Brain-Computer+Interfacing)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://snu.elsevierpure.com/en/publications/rearchitecting-a-neuromorphic-processor-for-spike-driven-brain-co/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00082&text=Check+out+this+research+output+at+Seoul+National+University%3A+Rearchitecting+a+Neuromorphic+Processor+for+Spike-Driven+Brain-Computer+Interfacing)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://snu.elsevierpure.com/en/publications/rearchitecting-a-neuromorphic-processor-for-spike-driven-brain-co/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FMICRO61859.2024.00082&summary=Check+out+this+research+output+at+Seoul+National+University%3A+Rearchitecting+a+Neuromorphic+Processor+for+Spike-Driven+Brain-Computer+Interfacing)
- [](/cdn-cgi/l/email-protection#f4cb8781969e919780c9a6919586979c9d809197809d9a93d1c6c495d1c6c4ba9181869b999b86849c9d97d1c6c4a4869b979187879b86d1c6c4929b86d1c6c4a7849d9f91d9b0869d82919ad1c6c4b686959d9ad9b79b998481809186d1c6c4bd9a8091869295979d9a93d2969b908dc9b79c91979fd1c6c49b8180d1c6c4809c9d87d1c6c4869187919586979cd1c6c49b8180848180d1c6c49580d1c6c4a7919b8198d1c6c4ba95809d9b9a9598d1c6c4a19a9d829186879d808dd1c7b5d1c6c4a6919586979c9d809197809d9a93d1c6c495d1c6c4ba9181869b999b86849c9d97d1c6c4a4869b979187879b86d1c6c4929b86d1c6c4a7849d9f91d9b0869d82919ad1c6c4b686959d9ad9b79b998481809186d1c6c4bd9a8091869295979d9a93d488d49c80808487cedbdb879a81da91988791829d918684818691da979b99db919adb848196989d9795809d9b9a87db86919586979c9d809197809d9a93d995d99a9181869b999b86849c9d97d984869b979187879b86d9929b86d987849d9f91d990869d82919ad99686959d9ad9979bdbcb818099ab879b81869791c99199959d98d2959984cf818099ab9991909d8199c99199959d98d2959984cf818099ab97959984959d939ac9879c958691989d9a9f)
