<!-- 从 mlsys2026-ed1d3d4c64dc1b95332a8cde3f2a0bdf.html 迁移的资料快照；原始 HTML SHA-256: 91cebf187c381ffbacc608975400973121852247c524d3dd07aa524d7f0106f1。 -->

[MLSys Proceedings](/)

- [](/admin/login/?next=/admin/)
- [](/admin/logout/?nextp=/admin)

Search

# BOute: Cost-Efficient LLM Serving with Heterogeneous LLMs and GPUs via Multi-Objective Bayesian Optimization

YOUHE JIANG, Fangcheng Fu, Eiko Yoneki

[Proceedings of Machine Learning and Systems 8 (MLSys 2026)](/paper_files/paper/2026) Conference

[Bibtex](/paper_files/paper/764-/bibtex) [Paper](/paper_files/paper/2026/file/ed1d3d4c64dc1b95332a8cde3f2a0bdf-Paper-Conference.pdf)

## Abstract

The rapid growth of large language model (LLM) deployments has made cost-efficient serving systems essential. Recent efforts to enhance system cost-efficiency adopt two main perspectives: (\textbf{\underline{i}}) An \textit{algorithmic} perspective that exploits heterogeneous model capabilities to route simpler queries to lower-cost models and complex queries to higher-cost models (i.e., heterogeneous query routing); and (\textbf{\underline{ii}}) a \textit{systems} perspective that utilizes heterogeneous GPU resources as cost-effective alternatives to homogeneous high-end GPUs (i.e., heterogeneous model deployment). However, algorithm-system co-design for cost-efficient LLM serving necessitates sophisticated management: (\textbf{\underline{i}}) Determining optimal query routing strategies under latency and quality requirements, (\textbf{\underline{ii}}) configuring model deployment across heterogeneous GPUs with appropriate resource allocation and parallelism strategies, and (\textbf{\underline{iii}}) co-optimizing routing and deployment decisions to maximize overall system performance. To address these challenges, we present BOute, a \textit{quality-aware scheduling system} that jointly exploits heterogeneous model and GPU capabilities for cost-efficient LLM serving. BOute employs a \textit{multi-objective Bayesian optimization (MOBO) framework} to co-optimize the routing strategy and model deployment, thereby maximizing the cost-efficiency of the serving system while guaranteeing response quality. Evaluation results demonstrate that \sys outperforms state-of-the-art LLM serving systems by up to 157\\ and 59\\ on average under \textit{identical} cost budgets and quality requirements, or reducing serving costs by 15\\-61\\ (38\\ on average) while maintaining the \textit{same} performance targets, validating its effectiveness in achieving cost-efficient LLM serving.

  

#### Name Change Policy

×

Requests for name changes in the electronic proceedings will be accepted with no questions asked. However name changes may cause bibliographic tracking issues. Authors are asked to consider this carefully and discuss it with their co-authors prior to requesting a name change in the electronic proceedings.

Use the "Report an Issue" link to request a name change.

[Report an Issue](https://mlsys.org/Help/Contact?select=Conference)    \|    [Name Change Policy](#)

Do not remove: This comment is monitored to verify that the site is working properly
