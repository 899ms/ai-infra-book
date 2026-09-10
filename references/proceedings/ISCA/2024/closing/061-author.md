<!-- 从 061-author.html 迁移的资料快照；原始 HTML SHA-256: b65f5558b6dc2385a352fb4da9792015ba3afe56882929e1f0eb22c82791dc58。 -->

![Dr. Jie Zhang](https://jiezhang-camel.github.io/images/jie_img2.png)

### Dr. Jie Zhang

Assistant professor @ PKU  
A designer of storage system and computer architecture in era of BigData and AI.

Follow

-  Beijing, China
- [ Email](mailto:jiez@pku.edu.cn)
- [ ResearchGate](https://www.researchgate.net/profile/Jie_Zhang460)
- [ LinkedIn](https://www.linkedin.com/in/jie-zhang-42b9a957)
- [ Instagram](https://instagram.com/camelab_members)
- [ Github](https://github.com/jiezhang-camel)
- [ Google Scholar](https://scholar.google.com/citations?user=I5Zv078AAAAJ&hl=en)

# Flagger: Cooperative Acceleration for Large-Scale Cross-Silo Federated Learning Aggregation

Published in *IEEE/ACM International Symposium on Computer Architecture (ISCA)*, 2024

Cross-silo federated learning (FL) leverages homomorphic encryption (HE) to obscure the model updates from the clients. However, HE poses the challenges of complex cryptographic computations and inflated ciphertext sizes. As cross-silo FL scales to accommodate larger models and more clients, the overheads of HE can overwhelm a CPU-centric aggregator architecture, including excessive network traffic, enormous data volume, intricate computations, and redundant data movements. Tackling these issues, we propose Flagger, an efficient and high-performance FL aggregator. Flagger meticulously integrates the data processing unit (DPU) with computational storage drives (CSD), employing these two distinct near-data processing (NDP) accelerators as a holistic architecture to collaboratively enhance FL aggregation. With the delicate delegation of complex FL aggregation tasks, we build Flagger-DPU and Flagger-CSD to exploit both in-network and in-storage HE acceleration to streamline FL aggregation. We also implement Flagger-Runtime, a dedicated software layer, to coordinate NDP accelerators and enable direct peer-to-peer data exchanges, markedly reducing data migration burdens. Our evaluation results reveal that Flagger expedites the aggregation in FL training iterations by 436% on average, compared with traditional CPU-centric aggregators.

[Paper download](https://ieeexplore.ieee.org/abstract/document/10609633)

Recommended citation: Pan, Xiurui, Yuda An, Shengwen Liang, Bo Mao, Mingzhe Zhang, Qiao Li, Myoungsoo Jung, and Jie Zhang. “Flagger: Cooperative Acceleration for Large-Scale Cross-Silo Federated Learning Aggregation.” In 2024 ACM/IEEE 51st Annual International Symposium on Computer Architecture (ISCA), pp. 915-930. IEEE, 2024.

#### Share on

[ Twitter](https://twitter.com/intent/tweet?text=https://jiezhang-camel.github.io/publication/2024-flagger "Share on Twitter") [ Facebook](https://www.facebook.com/sharer/sharer.php?u=https://jiezhang-camel.github.io/publication/2024-flagger "Share on Facebook") [ LinkedIn](https://www.linkedin.com/shareArticle?mini=true&url=https://jiezhang-camel.github.io/publication/2024-flagger "Share on LinkedIn")

[Previous](https://jiezhang-camel.github.io/publication/2024-readretry "Achieving Near-Zero Read Retry for 3D NAND Flash Memory ") [Next](https://jiezhang-camel.github.io/publication/2024-scalaafa "ScalaAFA: Constructing User-Space All-Flash Array Engine with Holistic Designs ")
