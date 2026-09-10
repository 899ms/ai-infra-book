<!-- 从 lns-institution.html 迁移的资料快照；原始 HTML SHA-256: c2b9948f86d698c1280875c753421883bc94da628afe5969def0bb57d3af7df4。 -->

## Breadcrumb

1.  [Home](/)
2.  [Publications & Reports](/publications-reports)

January 8, 2025

Conference Paper

## Bridging the Gap Between LLMs and LNS with Dynamic Data Format and Architecture Codesign

Share: [Share on Facebook](https://www.facebook.com/dialog/share?app_id=269100523864066&display=popup&href=https%3A%2F%2Fwww.pnnl.gov%2Fpublications%2Fbridging-gap-between-llms-and-lns-dynamic-data-format-and-architecture-codesign) [Share on X (formerly Twitter)](http://twitter.com/share?url=https%3A%2F%2Fwww.pnnl.gov%2Fpublications%2Fbridging-gap-between-llms-and-lns-dynamic-data-format-and-architecture-codesign&text=Bridging%20the%20Gap%20Between%20LLMs%20and%20LNS%20with%20Dynamic%20Data%20Format%20and%20Architecture%20Codesign) [Share on LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fwww.pnnl.gov%2Fpublications%2Fbridging-gap-between-llms-and-lns-dynamic-data-format-and-architecture-codesign&text=Bridging%20the%20Gap%20Between%20LLMs%20and%20LNS%20with%20Dynamic%20Data%20Format%20and%20Architecture%20Codesign) [Email To:](mailto:?&subject=Bridging%20the%20Gap%20Between%20LLMs%20and%20LNS%20with%20Dynamic%20Data%20Format%20and%20Architecture%20Codesign&body=https%3A%2F%2Fwww.pnnl.gov%2Fpublications%2Fbridging-gap-between-llms-and-lns-dynamic-data-format-and-architecture-codesign)

## Abstract

Deep neural networks (DNNs) have achieved tremendous success in the past few years. However, their training and inference demand exceptional computational and memory resources. Quantization has been shown as an effective approach to mitigate the cost, with the mainstream data types reduced from FP32 to FP16/BF16 and recently FP8 in the latest NVIDIA H100 GPUs. With increasingly aggressive quantization, however, the conventional floating-point formats suffer from limited precision in representing numbers around zero. Recently, NVIDIA demonstrated the potential of using a Logarithmic Number System (LNS) for the next generation of tensor cores. While LNS mitigates the hurdles in representing small numbers, in this work we observed a mismatch between LNS and the emerging Large Language Models (LLM), where LLM exhibits significant outliers when directly adopting the LNS format. In this paper, we present a data-format/architecture codesign to bright this gap. On the format side, we propose a dynamic LNS format to flexibly represent outliers at a higher precision, by exploiting asymmetry in the LNS representation and identifying outliers through a per-vector basis. On the architecture side, for demonstration, we realize the dynamic LNS format in a systolic array, which can handle the irregularity of the outliers at runtime. We implement our approach on an Alveo U280 FPGA as a prototype. Experimental results show that our design can effectively handle the outliers and resolve the mismatch between LNS and LLM, contributing to an accuracy improvement of 15.4% and 16% over the floating-point and the original LNS baselines, using four state-of-the-art LLM models. Our observation and design lay a solid foundation for the large-scale adoption of the LNS format in the next-generation deep learning hardware.

*Published: January 8, 2025*

## Citation

Haghi P., C. Wu, Z. Azad, Y. Li, A. Gui, Y. Hao, and A. Li, et al. 2024. Bridging the Gap Between LLMs and LNS with Dynamic Data Format and Architecture Codesign. In *Proceedings of the 57th IEEE/ACM International Symposium on Microarchitecture (MICRO 2024), November 2-6, 2024, Austin, TX*, 1617-1631. Los Alamitos, California:IEEE Computer Society. PNNL-SA-192868. [doi:10.1109/MICRO61859.2024.00118](https://www.doi.org/10.1109/MICRO61859.2024.00118)

### Research topics

[High-Performance Computing](/high-performance-computing)

[Artificial Intelligence](/artificial-intelligence)

#### Related Content

AUGUST 20, 2026

Article

### [Improving the Prediction Ability of Spiking Neural Networks](/publications/improving-prediction-ability-spiking-neural-networks)

[Read](/publications/improving-prediction-ability-spiking-neural-networks)

[](/publications/improving-prediction-ability-spiking-neural-networks)

![Illustration of a starburst like network and multicolored wave](/sites/default/files/styles/thumbnail/public/media/image/IDSD_0067_WEB_SNN-NeuralNetwork_v1.jpg?h=b4f59d0b&itok=DWhP2zhF)

AUGUST 7, 2026

Article

### [PNNL Contributes to a Safe World Cup](/publications/pnnl-contributes-safe-world-cup)

[Read](/publications/pnnl-contributes-safe-world-cup)

[](/publications/pnnl-contributes-safe-world-cup)

![This photo shows scientist Nick Betzsold, sitting, looking at a monitor on a desk. A large screen to his right shows Super Bowl action.](/sites/default/files/styles/thumbnail/public/media/image/Betzsold%20Super%20Bowl_0.jpg?h=71976bb4&itok=iDXE1nZy)

JUNE 9, 2026

Article

### [New PNNL-OSU Partnership Expands on Years of Collaboration](/publications/new-pnnl-osu-partnership-expands-years-collaboration)

[Read](/publications/new-pnnl-osu-partnership-expands-years-collaboration)

[](/publications/new-pnnl-osu-partnership-expands-years-collaboration)

![PNNL and OSU sign MOU](/sites/default/files/styles/thumbnail/public/media/image/20260504%20URM%20PNNL%20Visit-65.jpg?h=e45be382&itok=risZRYfv)

[See All Publications & Reports](/publications-reports)
