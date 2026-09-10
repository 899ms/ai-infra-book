<!-- 从 mlsys2025-af2d9fb5bcee19ef2dfa70d843520c97.html 迁移的资料快照；原始 HTML SHA-256: 9fbc472decd235b211970b73d7ff45f5f64a89be62eb384052c970b8525a86ba。 -->

[MLSys Proceedings](/)

- [](/admin/login/?next=/admin/)
- [](/admin/logout/?nextp=/admin)

Search

# Self-Data Distillation for Recovering Quality in Pruned Large Language Models

Vithursan Thangarasa, Ganesh Venkatesh, Mike Lasby, Nish Sinnadurai, Sean Lie

[Proceedings of Machine Learning and Systems 7 (MLSys 2025)](/paper_files/paper/2025) Conference

[Bibtex](/paper_files/paper/631-/bibtex) [Paper](/paper_files/paper/2025/file/af2d9fb5bcee19ef2dfa70d843520c97-Paper-Conference.pdf) [Supplemental](/paper_files/paper/2025/file/af2d9fb5bcee19ef2dfa70d843520c97-Supplemental-Conference.pdf)

## Abstract

Large language models have driven significant progress in natural language processing, but their deployment requires substantial compute and memory resources. As models scale, compression techniques become essential for balancing model quality with computational efficiency. Structured pruning, which removes less critical components of the model, is a promising strategy for reducing complexity. However, one-shot pruning often results in significant quality degradation, particularly in tasks requiring multi-step reasoning. To recover lost quality, supervised fine-tuning (SFT) is commonly applied, but it can lead to catastrophic forgetting by shifting the model's learned data distribution. Therefore, addressing the degradation from both pruning and SFT is essential to preserve the original model's quality. In this work, we utilize self-data distilled fine-tuning to address these challenges. Our approach leverages the original, unpruned model to generate a distilled dataset that preserves semantic richness and mitigates catastrophic forgetting by maintaining alignment with the base model's knowledge. Empirically, we demonstrate that self-data distillation consistently outperforms standard SFT, improving average accuracy by up to 8% on the HuggingFace OpenLLM Leaderboard v1. Specifically, when pruning six decoder blocks on Llama3.1-8B Instruct (i.e., 32 to 26 layers, reducing the model size from 8.03B to 6.72B parameters), our method retains 91.2% of the original model's accuracy compared to 81.7% with SFT, while reducing real-world FLOPs by 16.30%. Furthermore, combining self-data distilled models through model merging yields enhanced quality retention. Additionally, leveraging these pruned models in speculative decoding increases token acceptance rates, thereby improving inference efficiency in applied settings.

  

#### Name Change Policy

×

Requests for name changes in the electronic proceedings will be accepted with no questions asked. However name changes may cause bibliographic tracking issues. Authors are asked to consider this carefully and discuss it with their co-authors prior to requesting a name change in the electronic proceedings.

Use the "Report an Issue" link to request a name change.

[Report an Issue](https://mlsys.org/Help/Contact?select=Conference)    \|    [Name Change Policy](#)

Do not remove: This comment is monitored to verify that the site is working properly
