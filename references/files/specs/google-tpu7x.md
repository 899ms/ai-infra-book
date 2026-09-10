<!-- 从 google-tpu7x.html 迁移的资料快照；原始 HTML SHA-256: 016293a3405cc36e03c1269cdc0220603c0a29ed916ca5750b6e813d1f7e9a03。 -->

- [Home](https://docs.cloud.google.com/)

- 

  [Documentation](https://docs.cloud.google.com/docs)

- 

  [AI and ML](https://docs.cloud.google.com/docs/ai-ml)

- 

  [Cloud TPU](https://docs.cloud.google.com/tpu/docs)

- 

  [Guides](https://docs.cloud.google.com/tpu/docs/intro-to-tpu)

Send feedback

Stay organized with collections Save and categorize content based on your preferences.

# TPU7x (Ironwood)

This page describes the architecture and available configurations for TPU7x, the latest TPU available on Google Cloud. TPU7x is the first release within the Ironwood family, Google Cloud's seventh generation TPU. The Ironwood generation is designed for large-scale AI training and inference.

With a 9,216-chip footprint per Pod, TPU7x shares many similarities with [TPU v5p](/tpu/docs/v5p). TPU7x provides high performance for large scale dense and MoE models, pre-training, sampling and decode-heavy inference.

To use TPU7x, you can use Google Kubernetes Engine (GKE) or Compute Engine. For more information about using TPUs with GKE, see [About TPUs in GKE](/kubernetes-engine/docs/concepts/tpus).

You can also use TPU7x and GKE with All Capacity mode. All Capacity mode is available through an All Capacity mode reservation, which gives you full access to all of your reserved capacity (no hold-backs) and full visibility into the TPU hardware topology, utilization status, and health status. For more information, see [All Capacity mode overview](/tpu/docs/all-capacity-overview).

**Note:** You can use the JAX and PyTorch frameworks on TPU7x. TensorFlow is not supported.

## System architecture

Each TPU7x chip contains two TensorCores and four SparseCores. The following table shows the key specifications and their values for TPU7x compared to prior generations.

Specification
