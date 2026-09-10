<!-- 从 offn-institution.html 迁移的资料快照；原始 HTML SHA-256: 18e83d03db6b77dce855078471814825e7ba1c590909580ea6c3e550fa3412fb。 -->

## 상세 보기

# oFFN: Outlier and Neuron-aware Structured FFN for Fast yet Accurate LLM Inference

- Song, Geunsoo; 
- Yang, Hoeseok; 
- [Yi, Youngmin](../researcher/7e04ef3f-2d33-4a49-ba2b-cb29f884efce)

Citations

WEB OF SCIENCE

*0*

Citation

- APA
- CHICAGO
- MLA
- VANCOUVER
- IEEE
- HARVARD

Export

- XML (DC)
- EXCEL

[](https://www.addtoany.com/share "공유")

[](https://plu.mx/plum/a/?doi=10.1145/3779212.3790194)

## 초록

With the advent of large-scale language models (LLMs), various optimization techniques have been proposed to enable efficient inference. Among these, methods that aggressively exploit output activation sparsity have attracted significant attention, which leverage ReLU-fied LLMs and skip the entire memory accesses as well as the computation for the output element if it was predicted as sparse. Achieving fast and accurate prediction of output activation sparsity is crucial to enhancing inference efficiency. However, in practice, phenomena such as activation outliers and hot and cold neurons, which significantly affect the exploitation of sparsity during LLM inference, have either been addressed individually or not structurally integrated in existing work. In this paper, we reveal that these two phenomena are closely related and propose a novel FFN architecture called oFFN (Outlier-aware Structured FFN) that effectively exploits them simultaneously. The proposed method rearranges the FFN weights in both row and column dimensions to enable efficient and accurate prediction of output sparsity, considering outliers, and to enable separation of hot and cold neurons, computing them with respective optimal operations. The proposed method allows for the optimal computation path for each neuron, even when the batch size dynamically changes. Compared to existing sparsity prediction techniques, our method achieves the fastest speed with negligible accuracy loss. Experimental results show that it delivers up to 2.01x faster end-to-end inference speed compared to dense inference, and up to 5.46x acceleration in FFN layers under autoregressive decoding in ReLU-fied LLMs.

## 키워드

Activation Sparsity Prediction; Structured Sparsity; Large Language Models

제목  
oFFN: Outlier and Neuron-aware Structured FFN for Fast yet Accurate LLM Inference

&nbsp;

저자  
Song, Geunsoo; Yang, Hoeseok; Yi, Youngmin

&nbsp;

DOI  
[10.1145/3779212.3790194](https://doi.org/10.1145/3779212.3790194)

&nbsp;

발행일  
2026

&nbsp;

유형  
Proceedings Paper

&nbsp;

저널명  
PROCEEDINGS OF THE 31ST ACM INTERNATIONAL CONFERENCE ON ARCHITECTURAL SUPPORT FOR PROGRAMMING LANGUAGES AND OPERATING SYSTEMS, VOL 2, ASPLOS 2026

&nbsp;

페이지  
1301 ~ 1315

더보기
