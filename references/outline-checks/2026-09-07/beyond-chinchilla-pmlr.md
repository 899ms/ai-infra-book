<!-- 从 beyond-chinchilla-pmlr.html 迁移的资料快照；原始 HTML SHA-256: 2071e632227b84c538fcd3fb52ef26a492fe822197fde998cc20cd8e4c261629。 -->

\[[edit](https://github.com/mlresearch/v235/edit/gh-pages/_posts/2024-07-08-sardana24a.md)\]

# Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws

Nikhil Sardana, Jacob Portes, Sasha Doubov, Jonathan Frankle

*Proceedings of the 41st International Conference on Machine Learning*, PMLR 235:43445-43460, 2024.

#### Abstract

Large language model (LLM) scaling laws are empirical formulas that estimate changes in model quality as a result of increasing parameter count and training data. However, these formulas, including the popular Deepmind Chinchilla scaling laws, neglect to include the cost of inference. We modify the Chinchilla scaling laws to calculate the optimal LLM parameter count and pre-training data size to train and deploy a model of a given quality and inference demand. We conduct our analysis both in terms of a compute budget and real-world costs and find that LLM researchers expecting reasonably large inference demand (\$\sim\$1B requests) should train models smaller and longer than Chinchilla-optimal. Furthermore, we train 47 models of varying sizes and parameter counts to validate our formula and find that model quality continues to improve as we scale tokens per parameter to extreme ranges (up to 10,000). Finally, we ablate the procedure used to fit the Chinchilla scaling law coefficients and find that developing scaling laws only from data collected at typical token/parameter ratios overestimates the impact of additional tokens at these extreme ranges.

#### Cite this Paper

------------------------------------------------------------------------

BibTeX

`@InProceedings{pmlr-v235-sardana24a, title = {Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws}, author = {Sardana, Nikhil and Portes, Jacob and Doubov, Sasha and Frankle, Jonathan}, booktitle = {Proceedings of the 41st International Conference on Machine Learning}, pages = {43445--43460}, year = {2024}, editor = {Salakhutdinov, Ruslan and Kolter, Zico and Heller, Katherine and Weller, Adrian and Oliver, Nuria and Scarlett, Jonathan and Berkenkamp, Felix}, volume = {235}, series = {Proceedings of Machine Learning Research}, month = {21--27 Jul}, publisher = {PMLR}, pdf = {https://raw.githubusercontent.com/mlresearch/v235/main/assets/sardana24a/sardana24a.pdf}, url = {https://proceedings.mlr.press/v235/sardana24a.html}, abstract = {Large language model (LLM) scaling laws are empirical formulas that estimate changes in model quality as a result of increasing parameter count and training data. However, these formulas, including the popular Deepmind Chinchilla scaling laws, neglect to include the cost of inference. We modify the Chinchilla scaling laws to calculate the optimal LLM parameter count and pre-training data size to train and deploy a model of a given quality and inference demand. We conduct our analysis both in terms of a compute budget and real-world costs and find that LLM researchers expecting reasonably large inference demand ($\sim$1B requests) should train models smaller and longer than Chinchilla-optimal. Furthermore, we train 47 models of varying sizes and parameter counts to validate our formula and find that model quality continues to improve as we scale tokens per parameter to extreme ranges (up to 10,000). Finally, we ablate the procedure used to fit the Chinchilla scaling law coefficients and find that developing scaling laws only from data collected at typical token/parameter ratios overestimates the impact of additional tokens at these extreme ranges.} } `

Copy to Clipboard

Download

Endnote

`%0 Conference Paper %T Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws %A Nikhil Sardana %A Jacob Portes %A Sasha Doubov %A Jonathan Frankle %B Proceedings of the 41st International Conference on Machine Learning %C Proceedings of Machine Learning Research %D 2024 %E Ruslan Salakhutdinov %E Zico Kolter %E Katherine Heller %E Adrian Weller %E Nuria Oliver %E Jonathan Scarlett %E Felix Berkenkamp %F pmlr-v235-sardana24a %I PMLR %P 43445--43460 %U https://proceedings.mlr.press/v235/sardana24a.html %V 235 %X Large language model (LLM) scaling laws are empirical formulas that estimate changes in model quality as a result of increasing parameter count and training data. However, these formulas, including the popular Deepmind Chinchilla scaling laws, neglect to include the cost of inference. We modify the Chinchilla scaling laws to calculate the optimal LLM parameter count and pre-training data size to train and deploy a model of a given quality and inference demand. We conduct our analysis both in terms of a compute budget and real-world costs and find that LLM researchers expecting reasonably large inference demand ($\sim$1B requests) should train models smaller and longer than Chinchilla-optimal. Furthermore, we train 47 models of varying sizes and parameter counts to validate our formula and find that model quality continues to improve as we scale tokens per parameter to extreme ranges (up to 10,000). Finally, we ablate the procedure used to fit the Chinchilla scaling law coefficients and find that developing scaling laws only from data collected at typical token/parameter ratios overestimates the impact of additional tokens at these extreme ranges. `

Copy to Clipboard

Download

APA

`Sardana, N., Portes, J., Doubov, S. & Frankle, J.. (2024). Beyond Chinchilla-Optimal: Accounting for Inference in Language Model Scaling Laws. `*`Proceedings of the 41st International Conference on Machine Learning`*`, in `*`Proceedings of Machine Learning Research`*` 235:43445-43460 Available from https://proceedings.mlr.press/v235/sardana24a.html. `

Copy to Clipboard

Download

------------------------------------------------------------------------

#### Related Material

- [Download PDF](https://raw.githubusercontent.com/mlresearch/v235/main/assets/sardana24a/sardana24a.pdf)
- [OpenReview](https://openreview.net/forum?id=0bmXrtTDUu)
