<!-- 从 verl-overview.html 迁移的资料快照；原始 HTML SHA-256: 68bf535d3f0b041f926183e3c158d4fe7b1ca56b6449a85adb5b2d9f871c8e28。 -->

# Welcome to verl’s documentation\![](#welcome-to-verl-s-documentation "Link to this heading")

verl is a flexible, efficient and production-ready RL training framework designed for large language models (LLMs) post-training. It is an open source implementation of the [HybridFlow](https://arxiv.org/pdf/2409.19256) paper.

verl is flexible and easy to use with:

- **Easy extension of diverse RL algorithms**: The hybrid programming model combines the strengths of single-controller and multi-controller paradigms to enable flexible representation and efficient execution of complex Post-Training dataflows. Allowing users to build RL dataflows in a few lines of code.

- **Seamless integration of existing LLM infra with modular APIs**: Decouples computation and data dependencies, enabling seamless integration with existing LLM frameworks, such as PyTorch FSDP, Megatron-LM, vLLM and SGLang. Moreover, users can easily extend to other LLM training and inference frameworks.

- **Flexible device mapping and parallelism**: Supports various placement of models onto different sets of GPUs for efficient resource utilization and scalability across different cluster sizes.

- Ready integration with popular HuggingFace models

verl is fast with:

- **State-of-the-art throughput**: By seamlessly integrating existing SOTA LLM training and inference frameworks, verl achieves high generation and training throughput.

- **Efficient actor model resharding with 3D-HybridEngine**: Eliminates memory redundancy and significantly reduces communication overhead during transitions between training and generation phases.

------------------------------------------------------------------------

Quickstart

- [Installation](start/install.html)
  - [Requirements](start/install.html#requirements)
  - [Choices of Backend Engines](start/install.html#choices-of-backend-engines)
  - [Install with uv](start/install.html#install-with-uv)
  - [Install with uv in a custom environment](start/install.html#install-with-uv-in-a-custom-environment)
  - [Managing environments explicitly](start/install.html#managing-environments-explicitly)
  - [uv troubleshooting](start/install.html#uv-troubleshooting)
  - [Install from docker image](start/install.html#install-from-docker-image)
  - [Install with AMD GPUs - ROCM kernel support](start/install.html#install-with-amd-gpus-rocm-kernel-support)
- [Quickstart: PPO training on GSM8K dataset](start/quickstart.html)
  - [Introduction](start/quickstart.html#introduction)
  - [Dataset Introduction](start/quickstart.html#dataset-introduction)
  - [Step 1: Prepare the dataset](start/quickstart.html#step-1-prepare-the-dataset)
  - [Step 2: Download a model for post-training](start/quickstart.html#step-2-download-a-model-for-post-training)
  - [Step 3: Perform PPO training with the instruct model](start/quickstart.html#step-3-perform-ppo-training-with-the-instruct-model)
- [Multinode Training](start/multinode.html)
  - [Option 1: Launch Manually](start/multinode.html#option-1-launch-manually)
  - [Option 2: Launch via SkyPilot on Kubernetes or clouds](start/multinode.html#option-2-launch-via-skypilot-on-kubernetes-or-clouds)
  - [Option 3: Launch via Slurm](start/multinode.html#option-3-launch-via-slurm)
  - [Option 4: Launch via dstack](start/multinode.html#option-4-launch-via-dstack)
  - [How to debug?](start/multinode.html#how-to-debug)
  - [Multi-node training on AMD clusters](start/multinode.html#multi-node-training-on-amd-clusters)
- [Ray Debug Tutorial](start/ray_debug_tutorial.html)
  - [How to debug?](start/ray_debug_tutorial.html#how-to-debug)
- [More Resources](start/more_resources.html)
- [Agentic RL Training](start/agentic_rl.html)
  - [Overview](start/agentic_rl.html#overview)
  - [Server-based Asynchronous Rollout](start/agentic_rl.html#server-based-asynchronous-rollout)
  - [Multi-turn Conversations and Tool Calls](start/agentic_rl.html#multi-turn-conversations-and-tool-calls)
  - [Agent Framework](start/agentic_rl.html#agent-framework)

Programming guide

- [How to Extend verl](extend_guide.html)
  - [RL Researcher](extend_guide.html#rl-researcher)
  - [Agent Framework Developer](extend_guide.html#agent-framework-developer)
  - [Training/Inference Framework Developer](extend_guide.html#training-inference-framework-developer)
- [HybridFlow Programming Guide](hybrid_flow.html)
  - [Motivation and Design](hybrid_flow.html#motivation-and-design)
  - [Codebase walkthrough (PPO)](hybrid_flow.html#codebase-walkthrough-ppo)
  - [Repository organization](hybrid_flow.html#repository-organization)
- [The Design of `verl.single_controller`](single_controller.html)
  - [Preface](single_controller.html#preface)
  - [Origin](single_controller.html#origin)
  - [A Running Example: `generate_sequences`](single_controller.html#a-running-example-generate-sequences)
  - [Beyond RL Post-Training: Generalizing `verl.single_controller`](single_controller.html#beyond-rl-post-training-generalizing-verl-single-controller)

Data Preparation

- [Prepare Data for Post-Training](preparation/prepare_data.html)
- [Implement Reward Function for Dataset](preparation/reward_function.html)

Configurations

- [Config Explanation](examples/config.html)
  - [ppo_trainer.yaml for RL FSDP Backend](examples/config.html#ppo-trainer-yaml-for-rl-fsdp-backend)
  - [evaluation.yaml](examples/config.html#evaluation-yaml)
  - [sft_trainer.yaml for SFT FSDP Backend](examples/config.html#sft-trainer-yaml-for-sft-fsdp-backend)

PPO Example

- [PPO Example Architecture](examples/ppo_code_architecture.html)
- [GSM8K Example](examples/gsm8k_example.html)
- [Megatron-FSDP Example](examples/megatron_fsdp_example.html)
- [Multi-Modal Example Architecture](examples/multi_modal_example.html)
- [SkyPilot Examples](examples/skypilot_examples.html)

Algorithms

- [Proximal Policy Optimization (PPO)](algo/ppo.html)
- [Group Relative Policy Optimization (GRPO)](algo/grpo.html)
- [Recipe: Decoupled Clip and Dynamic Sampling Policy Optimization (DAPO)](algo/dapo.html)
- [Recipe: Self-Play Fine-Tuning (SPIN)](algo/spin.html)
- [Recipe: Self-Play Preference Optimization (SPPO)](algo/sppo.html)
- [Recipe: Entropy Mechanism](algo/entropy.html)
- [On-Policy RL with Optimal Reward Baseline (OPO)](algo/opo.html)
- [Algorithm Baselines](algo/baseline.html)
- [GPG: Group Policy Gradient](algo/gpg.html)
- [Rollout Correction](algo/rollout_corr.html)
- [Mathematical Formulations of Rollout Correction Methods in `verl`](algo/rollout_corr_math.html)
- [Optimal Token Baseline (OTB)](algo/otb.html)
- [Divergence Proximal Policy Optimization (DPPO)](algo/dppo.html)
- [On-Policy Distillation (OPD)](algo/opd.html)
- [Direct Reward Optimization](algo/dro.html)

PPO Trainer and Workers

- [PPO Ray Trainer](workers/ray_trainer.html)
- [Model Engine](workers/model_engine.html)
- [Engine Workers](workers/engine_workers.html)
- [Automodel Backend](workers/automodel_workers.html)
- [TorchTitan Backend](workers/torchtitan_workers.html)
- [SGLang Backend](workers/sglang_worker.html)
- [TensorRT-LLM Backend](workers/trtllm_worker.html)

Performance Tuning Guide

- [Training DeepSeek 671b](perf/dpsk.html)
- [Dynamic Context Parallelism](advance/dynamic_context_parallel.html)
- [Verl LLM Best Practices (DAPO + Qwen3-235B)](perf/best_practices.html)
- [Performance Tuning Guide](perf/perf_tuning.html)
- [Rollout KV Cache Offload via Mooncake-Store](perf/rollout_kv_offload.html)
- [Upgrading to vLLM \>= 0.8](README_vllm0.8.html)
- [Hardware Resource Needed for RL](perf/device_tuning.html)
- [verl Profiler System](perf/verl_profiler_system.html)
- [NVIDIA Nsight Systems profiling in verl](perf/nsight_profiling.html)
- [PyTorch Profiling in verl](perf/torch_profiling.html)

Adding new models

- [Add models with the FSDP backend](advance/fsdp_extension.html)
- [Add models with the Megatron-LM backend](advance/megatron_extension.html)
- [Adding DeepSeek V4 support](advance/deepseek_v4_integration.html)
- [Experimental Megatron Agent Compose preview](advance/megatron_lite_backend.html)

Async Training

- [Recipe: One Step Off Policy Async Trainer](advance/one_step_off.html)
- [Delta Weight Sync](advance/delta_weight_sync.html)
- [V1 Async Trainer](advance/v1_async_trainer.html)
- [Recipe: Fully Async Policy Trainer](advance/fully_async.html)
- [Recipe: Async On-Policy Knowledge Distillation Trainer](advance/async-on-policy-distill.html)
- [Dynamic Resource Scheduling for Fully-Async Training](advance/dynamic_schedule.html)

Low Precision

- [FP8 RL in verl](low_precision/fp8.html)
- [NVFP4 QAT (Quantization-Aware Training) in verl](low_precision/nvfp4_qat.html)

Advanced Features

- [Using Checkpoints to Support Fault Tolerance Training](advance/checkpoint.html)
- [RoPE Scaling override](advance/rope.html)
- [Attention Implementation Override](advance/attention_implementation.html)
- [RL(HF) algorithms with LoRA Support](advance/ppo_lora.html)
- [Multi-turn Rollout Support](sglang_multiturn/multiturn.html)
- [Ray API Design Tutorial](advance/placement.html)
- [Extend to other RL(HF) algorithms](advance/dpo_extension.html)
- [Sandbox Fusion Example](examples/sandbox_fusion_example.html)
- [Trace Function Usage Instructions](advance/rollout_trace.html)
- [Use RL-Insight to Monitor Training](advance/rl_insight.html)
- [SkipManager: Skip everything in the RL pipeline.](advance/skip_manager.html)
- [Agent Loop](advance/agent_loop.html)
- [Reward Loop](advance/reward_loop.html)
- [TransferQueue Data System](data/transfer_queue.html)
- [Use Prometheus and Grafana to Monitor Rollout](advance/grafana_prometheus.html)
- [Guide to Using MTP in SFT/RL Training and Inference](advance/mtp.html)
- [Full Determinism for Reproducible RL Training](advance/determinism.html)
- [FSDP-Turbo backend](advance/fsdp_turbo_backend.html)

Hardware Support

- [Multi-Chip Support](hardware/multi_chip_support.html)
- [AMD (ROCm) Tutorial](amd_tutorial/index.html)
- [Ascend (NPU) Tutorial](ascend_tutorial/index.html)

API References

- [Data interface](api/data.html)
- [Single Controller interface](api/single_controller.html)
- [Trainer Interface](api/trainer.html)
- [Utilities](api/utils.html)

Blog

- [verl 0.7 release blog](blog/v0.7.html)

FAQ

- [Frequently Asked Questions](faq/faq.html)
  - [Ray related](faq/faq.html#ray-related)
  - [Distributed training](faq/faq.html#distributed-training)
  - [Install related](faq/faq.html#install-related)
  - [Illegal memory access](faq/faq.html#illegal-memory-access)
  - [Checkpoints](faq/faq.html#checkpoints)
  - [Triton `compile_module_from_src` error](faq/faq.html#triton-compile-module-from-src-error)
  - [What is the meaning of train batch size, mini batch size, and micro batch size?](faq/faq.html#what-is-the-meaning-of-train-batch-size-mini-batch-size-and-micro-batch-size)
  - [How to generate ray timeline to analyse performance of a training job?](faq/faq.html#how-to-generate-ray-timeline-to-analyse-performance-of-a-training-job)
  - [How to set proxy only for wandb?](faq/faq.html#how-to-set-proxy-only-for-wandb)
  - [Missmatch between inference and training sequence (high actor/grad_norm)](faq/faq.html#missmatch-between-inference-and-training-sequence-high-actor-grad-norm)

Contributing

- [Editing Agent Instructions](contributing/editing-agent-instructions.html)

Development Notes

- [Sandbox Fusion Tool Integration](sglang_multiturn/sandbox_fusion.html)

## Contribution[](#contribution "Link to this heading")

verl is free software; you can redistribute it and/or modify it under the terms of the Apache License 2.0. We welcome contributions. Join us on [GitHub](https://github.com/verl-project/verl), [Slack](https://join.slack.com/t/verlgroup/shared_invite/zt-2w5p9o4c3-yy0x2Q56s_VlGLsJ93A6vA) and [Wechat](https://raw.githubusercontent.com/eric-haibin-lin/verl-community/refs/heads/main/WeChat.JPG) for discussions.

Contributions from the community are welcome! Please check out our [project roadmap](https://github.com/verl-project/verl/issues/710) and [good first issues](https://github.com/verl-project/verl/issues?q=is%3Aissue%20state%3Aopen%20label%3A%22good%20first%20issue%22) to see where you can contribute.

### Code Linting and Formatting[](#code-linting-and-formatting "Link to this heading")

We use pre-commit to help improve code quality. To initialize pre-commit, run:

    pip install pre-commit
    pre-commit install

To resolve CI errors locally, you can also manually run pre-commit by:

    pre-commit run

### Adding CI tests[](#adding-ci-tests "Link to this heading")

If possible, please add CI test(s) for your new feature:

1.  Find the most relevant workflow yml file, which usually corresponds to a `hydra` default config (e.g. `ppo_trainer`, `ppo_megatron_trainer`, `sft_trainer`, etc).

2.  Add related path patterns to the `paths` section if not already included.

3.  Minimize the workload of the test script(s) (see existing scripts for examples).

We are HIRING! Send us an [email](mailto:haibin.lin%40bytedance.com) if you are interested in internship/FTE opportunities in MLSys/LLM reasoning/multimodal alignment.
