<!-- 从 google-v5p.html 迁移的资料快照；原始 HTML SHA-256: 7906292afbdeedbfdf343b7d998f97e1ec69c2eedd6d02ab9a99542fe91d5576。 -->

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

# TPU v5p

This document describes the architecture and supported configurations of Cloud TPU v5p.

## System architecture

This section describes the system architecture specific to the v5p version. Each TensorCore has four Matrix Multiply Units (MXU), a vector unit, and a scalar unit.

There are 8960 chips in a v5p Pod. The largest job that can be scheduled is a 96 cube (6144 chip) job.

The following table shows the key specifications for TPU v5p.

Specification
