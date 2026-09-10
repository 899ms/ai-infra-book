<!-- 从 061-institution.html 迁移的资料快照；原始 HTML SHA-256: d6a43863ae5c7dc730104c4ee7aae2ecb456ec8b88dbf6db824a5b8372abafe7。 -->

# Flagger: Cooperative Acceleration for Large-Scale Cross-Silo Federated Learning Aggregation

Xiurui Pan

, Yuda An

, Shengwen Liang

, Bo Mao

, Mingzhe Zhang

, Qiao Li

, [Myoungsoo Jung](https://pure.kaist.ac.kr/en/persons/myoungsoo-jung/)

, Jie Zhang

- [School of Electrical Engineering](https://pure.kaist.ac.kr/en/organisations/school-of-electrical-engineering/)

- Peking University
- CAS - Institute of Computing Technology
- Xiamen University
- CAS - Institute of Information Engineering

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

7 Scopus citations

[](https://plu.mx/plum/a/?doi=10.1109/ISCA59077.2024.00071)

- [ Overview ](/en/publications/flagger-cooperative-acceleration-for-large-scale-cross-silo-feder/)
- [ Fingerprint ](/en/publications/flagger-cooperative-acceleration-for-large-scale-cross-silo-feder/fingerprints/)

## Abstract

Cross-silo federated learning (FL) leverages homomorphic encryption (HE) to obscure the model updates from the clients. However, HE poses the challenges of complex cryptographic computations and inflated ciphertext sizes. As cross-silo FL scales to accommodate larger models and more clients, the overheads of HE can overwhelm a CPU-centric aggregator architecture, including excessive network traffic, enormous data volume, intricate computations, and redundant data movements. Tackling these issues, we propose Flagger, an efficient and high-performance FL aggregator. Flagger meticulously integrates the data processing unit (DPU) with computational storage drives (CSD), employing these two distinct near-data processing (NDP) accelerators as a holistic architecture to collaboratively enhance FL aggregation. With the delicate delegation of complex FL aggregation tasks, we build Flagger-DPU and Flagger-CSD to exploit both in-network and in-storage HE acceleration to streamline FL aggregation. We also implement Flagger-Runtime, a dedicated software layer, to coordinate NDP accelerators and enable direct peer-to-peer data exchanges, markedly reducing data migration burdens. Our evaluation results reveal that Flagger expedites the aggregation in FL training iterations by {436\\}\$ on average, compared with traditional CPU-centric aggregators.

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

## Access to Document

- [10.1109/ISCA59077.2024.00071](https://doi.org/10.1109/ISCA59077.2024.00071)

## Other files and links

- [Link to publication in Scopus](https://www.scopus.com/pages/publications/85201158693)

##  Fingerprint

Dive into the research topics of 'Flagger: Cooperative Acceleration for Large-Scale Cross-Silo Federated Learning Aggregation'. Together they form a unique fingerprint.

-  Federated machine learning Computer Science 100%
-  Homomorphic Encryption Computer Science 50%
-  Data Processing Computer Science 50%
-  Processing Unit Computer Science 25%
-  Evaluation Result Computer Science 12%
-  Ciphertext Computer Science 12%
-  Network Traffic Computer Science 12%
-  Data Migration Computer Science 12%

[ View full fingerprint ](/en/publications/flagger-cooperative-acceleration-for-large-scale-cross-silo-feder/fingerprints/)

## Cite this

- APA
- Author
- BIBTEX
- Harvard
- Standard
- RIS
- Vancouver

Pan, X., An, Y., Liang, S., Mao, B., Zhang, M., Li, Q.[, Jung, M.](https://pure.kaist.ac.kr/en/persons/myoungsoo-jung/), & Zhang, J. (2024). [Flagger: Cooperative Acceleration for Large-Scale Cross-Silo Federated Learning Aggregation](https://pure.kaist.ac.kr/en/publications/flagger-cooperative-acceleration-for-large-scale-cross-silo-feder/). In *Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024* (pp. 915-930). (Proceedings - International Symposium on Computer Architecture). Institute of Electrical and Electronics Engineers Inc.. [https://doi.org/10.1109/ISCA59077.2024.00071](https://doi.org/10.1109/ISCA59077.2024.00071)

Pan, Xiurui ; An, Yuda ; Liang, Shengwen et al. / [**Flagger : Cooperative Acceleration for Large-Scale Cross-Silo Federated Learning Aggregation**](https://pure.kaist.ac.kr/en/publications/flagger-cooperative-acceleration-for-large-scale-cross-silo-feder/). Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc., 2024. pp. 915-930 (Proceedings - International Symposium on Computer Architecture).

@inproceedings{aa7750141a10404fa36fe96ee2d7bb2f,

title = "Flagger: Cooperative Acceleration for Large-Scale Cross-Silo Federated Learning Aggregation",

abstract = "Cross-silo federated learning (FL) leverages homomorphic encryption (HE) to obscure the model updates from the clients. However, HE poses the challenges of complex cryptographic computations and inflated ciphertext sizes. As cross-silo FL scales to accommodate larger models and more clients, the overheads of HE can overwhelm a CPU-centric aggregator architecture, including excessive network traffic, enormous data volume, intricate computations, and redundant data movements. Tackling these issues, we propose Flagger, an efficient and high-performance FL aggregator. Flagger meticulously integrates the data processing unit (DPU) with computational storage drives (CSD), employing these two distinct near-data processing (NDP) accelerators as a holistic architecture to collaboratively enhance FL aggregation. With the delicate delegation of complex FL aggregation tasks, we build Flagger-DPU and Flagger-CSD to exploit both in-network and in-storage HE acceleration to streamline FL aggregation. We also implement Flagger-Runtime, a dedicated software layer, to coordinate NDP accelerators and enable direct peer-to-peer data exchanges, markedly reducing data migration burdens. Our evaluation results reveal that Flagger expedites the aggregation in FL training iterations by \\436\textbackslash{}\\\\\\ on average, compared with traditional CPU-centric aggregators.",

author = "Xiurui Pan and Yuda An and Shengwen Liang and Bo Mao and Mingzhe Zhang and Qiao Li and Myoungsoo Jung and Jie Zhang",

note = "Publisher Copyright: {\textcopyright} 2024 IEEE.; 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024 ; Conference date: 29-06-2024 Through 03-07-2024",

year = "2024",

doi = "10.1109/ISCA59077.2024.00071",

language = "English",

series = "Proceedings - International Symposium on Computer Architecture",

publisher = "Institute of Electrical and Electronics Engineers Inc.",

pages = "915--930",

booktitle = "Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024",

}

Pan, X, An, Y, Liang, S, Mao, B, Zhang, M, Li, Q[, Jung, M](https://pure.kaist.ac.kr/en/persons/myoungsoo-jung/) & Zhang, J 2024, [Flagger: Cooperative Acceleration for Large-Scale Cross-Silo Federated Learning Aggregation](https://pure.kaist.ac.kr/en/publications/flagger-cooperative-acceleration-for-large-scale-cross-silo-feder/). in *Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024.* Proceedings - International Symposium on Computer Architecture, Institute of Electrical and Electronics Engineers Inc., pp. 915-930, 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024, Buenos Aires, Argentina, 29/06/24. [https://doi.org/10.1109/ISCA59077.2024.00071](https://doi.org/10.1109/ISCA59077.2024.00071)

[**Flagger: Cooperative Acceleration for Large-Scale Cross-Silo Federated Learning Aggregation.**](https://pure.kaist.ac.kr/en/publications/flagger-cooperative-acceleration-for-large-scale-cross-silo-feder/) / Pan, Xiurui; An, Yuda; Liang, Shengwen et al.  
Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc., 2024. p. 915-930 (Proceedings - International Symposium on Computer Architecture).

Research output: Chapter in Book/Report/Conference proceeding › Conference contribution › peer-review

TY - GEN

T1 - Flagger

T2 - 51st ACM/IEEE Annual International Symposium on Computer Architecture, ISCA 2024

AU - Pan, Xiurui

AU - An, Yuda

AU - Liang, Shengwen

AU - Mao, Bo

AU - Zhang, Mingzhe

AU - Li, Qiao

AU - Jung, Myoungsoo

AU - Zhang, Jie

N1 - Publisher Copyright: © 2024 IEEE.

PY - 2024

Y1 - 2024

N2 - Cross-silo federated learning (FL) leverages homomorphic encryption (HE) to obscure the model updates from the clients. However, HE poses the challenges of complex cryptographic computations and inflated ciphertext sizes. As cross-silo FL scales to accommodate larger models and more clients, the overheads of HE can overwhelm a CPU-centric aggregator architecture, including excessive network traffic, enormous data volume, intricate computations, and redundant data movements. Tackling these issues, we propose Flagger, an efficient and high-performance FL aggregator. Flagger meticulously integrates the data processing unit (DPU) with computational storage drives (CSD), employing these two distinct near-data processing (NDP) accelerators as a holistic architecture to collaboratively enhance FL aggregation. With the delicate delegation of complex FL aggregation tasks, we build Flagger-DPU and Flagger-CSD to exploit both in-network and in-storage HE acceleration to streamline FL aggregation. We also implement Flagger-Runtime, a dedicated software layer, to coordinate NDP accelerators and enable direct peer-to-peer data exchanges, markedly reducing data migration burdens. Our evaluation results reveal that Flagger expedites the aggregation in FL training iterations by {436\\}\$ on average, compared with traditional CPU-centric aggregators.

AB - Cross-silo federated learning (FL) leverages homomorphic encryption (HE) to obscure the model updates from the clients. However, HE poses the challenges of complex cryptographic computations and inflated ciphertext sizes. As cross-silo FL scales to accommodate larger models and more clients, the overheads of HE can overwhelm a CPU-centric aggregator architecture, including excessive network traffic, enormous data volume, intricate computations, and redundant data movements. Tackling these issues, we propose Flagger, an efficient and high-performance FL aggregator. Flagger meticulously integrates the data processing unit (DPU) with computational storage drives (CSD), employing these two distinct near-data processing (NDP) accelerators as a holistic architecture to collaboratively enhance FL aggregation. With the delicate delegation of complex FL aggregation tasks, we build Flagger-DPU and Flagger-CSD to exploit both in-network and in-storage HE acceleration to streamline FL aggregation. We also implement Flagger-Runtime, a dedicated software layer, to coordinate NDP accelerators and enable direct peer-to-peer data exchanges, markedly reducing data migration burdens. Our evaluation results reveal that Flagger expedites the aggregation in FL training iterations by {436\\}\$ on average, compared with traditional CPU-centric aggregators.

UR - https://www.scopus.com/pages/publications/85201158693

U2 - 10.1109/ISCA59077.2024.00071

DO - 10.1109/ISCA59077.2024.00071

M3 - Conference contribution

AN - SCOPUS:85201158693

T3 - Proceedings - International Symposium on Computer Architecture

SP - 915

EP - 930

BT - Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024

PB - Institute of Electrical and Electronics Engineers Inc.

Y2 - 29 June 2024 through 3 July 2024

ER -

Pan X, An Y, Liang S, Mao B, Zhang M, Li Q et al. [Flagger: Cooperative Acceleration for Large-Scale Cross-Silo Federated Learning Aggregation](https://pure.kaist.ac.kr/en/publications/flagger-cooperative-acceleration-for-large-scale-cross-silo-feder/). In Proceeding - 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture, ISCA 2024. Institute of Electrical and Electronics Engineers Inc. 2024. p. 915-930. (Proceedings - International Symposium on Computer Architecture). doi: 10.1109/ISCA59077.2024.00071

- 
- [](https://www.facebook.com/sharer.php?u=https://pure.kaist.ac.kr/en/publications/flagger-cooperative-acceleration-for-large-scale-cross-silo-feder/%3Futm_source%3Dfacebook%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FISCA59077.2024.00071&p%5Bsummary%5D=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+Flagger%3A+Cooperative+Acceleration+for+Large-Scale+Cross-Silo+Federated+Learning+Aggregation)
- [![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMiIgaGVpZ2h0PSIyMiIgdmlld2JveD0iMCAwIDMwMCAyNzEiPgogICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgIDxwYXRoIGQ9Im0yMzYgMGg0NmwtMTAxIDExNSAxMTggMTU2aC05Mi42bC03Mi41LTk0LjgtODMgOTQuOGgtNDZsMTA3LTEyMy0xMTMtMTQ4aDk0LjlsNjUuNSA4Ni42em0tMTYuMSAyNDRoMjUuNWwtMTY1LTIxOGgtMjcuNHoiIC8+CiAgICAgICAgICAgICAgICA8L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://pure.kaist.ac.kr/en/publications/flagger-cooperative-acceleration-for-large-scale-cross-silo-feder/%3Futm_source%3Dtwitter%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FISCA59077.2024.00071&text=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+Flagger%3A+Cooperative+Acceleration+for+Large-Scale+Cross-Silo+Federated+Learning+Aggregation)
- [](https://www.linkedin.com/shareArticle?mini=true&url=https://pure.kaist.ac.kr/en/publications/flagger-cooperative-acceleration-for-large-scale-cross-silo-feder/%3Futm_source%3Dlinkedin%26utm_medium%3Dsocial%26utm_campaign%3Dsharelink%26doi%3D10.1109%2FISCA59077.2024.00071&summary=Check+out+this+research+output+at+Korea+Advanced+Institute+of+Science+and+Technology%3A+Flagger%3A+Cooperative+Acceleration+for+Large-Scale+Cross-Silo+Federated+Learning+Aggregation)
- [](/cdn-cgi/l/email-protection#ebd4989e89818e889fd6ad878a8c8c8e99ced8aaced9dba884849b8e998a9f829d8eced9dbaa88888e878e998a9f828485ced9db8d8499ced9dba78a998c8ec6b8888a878eced9dba899849898c6b8828784ced9dbad8e8f8e998a9f8e8fced9dba78e8a998582858cced9dbaa8c8c998e8c8a9f828485cd89848f92d6a8838e8880ced9db849e9fced9db9f838298ced9db998e988e8a998883ced9db849e9f9b9e9fced9db8a9fced9dba084998e8aced9dbaa8f9d8a85888e8fced9dba285989f829f9e9f8eced9db848dced9dbb888828e85888eced9db8a858fced9dbbf8e8883858487848c92ced8aaced9dbad878a8c8c8e99ced8aaced9dba884849b8e998a9f829d8eced9dbaa88888e878e998a9f828485ced9db8d8499ced9dba78a998c8ec6b8888a878eced9dba899849898c6b8828784ced9dbad8e8f8e998a9f8e8fced9dba78e8a998582858cced9dbaa8c8c998e8c8a9f828485cb97cb839f9f9b98d1c4c49b9e998ec5808a82989fc58a88c58099c48e85c49b9e898782888a9f82848598c48d878a8c8c8e99c68884849b8e998a9f829d8ec68a88888e878e998a9f828485c68d8499c6878a998c8ec698888a878ec68899849898c698828784c68d8e8f8e99c4d49e9f86b498849e99888ed68e868a8287cd8a869bd09e9f86b4868e8f829e86d68e868a8287cd8a869bd09e9f86b4888a869b8a828c85d698838a998e87828580)
