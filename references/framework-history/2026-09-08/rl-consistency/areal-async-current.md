<!-- 从 areal-async-current.html 迁移的资料快照；原始 HTML SHA-256: 31af46c71e0282b3979e464af56c96ed9b0600484813119efebf76858d15f08e。 -->

- [ Repository](https://github.com/areal-project/AReaL "Source repository")
- [ Open issue](https://github.com/areal-project/AReaL/issues/new?title=Issue%20on%20page%20%2Falgorithms/async.html&body=Your%20issue%20content%20here. "Open an issue")

- [ .md](../_sources/algorithms/async.md "Download source file")
-  .pdf

# Asynchronous RL

## Contents

- [Overview](#overview)
- [Key Techniques](#key-techniques)
  - [1. Off-Policyness Control](#off-policyness-control)
  - [2. Decoupled PPO Objective](#decoupled-ppo-objective)
- [References](#references)

<a id="asynchronous-rl"></a>

# Asynchronous RL
AReaL natively supports asynchronous RL training, enabling overlapped rollout generation and model training on disaggregated GPUs. This architecture maximizes GPU utilization by running inference and training concurrently.

> **Note:** This guide applies to all algorithms when asynchronous training is enabled (i.e., `rollout.max_head_offpolicyness`` ``>`` ``0`). Setting `rollout.max_head_offpolicyness=0` reverts AReaL to synchronous RL. The synchronous setting is useful for debugging but is typically 2x slower than asynchronous training.

<a id="overview"></a>

## Overview
Traditional online RL algorithms assume synchronous execution: the model generates rollouts, trains on them, and repeats. While simple, this approach leaves GPUs idle during long rollouts and does not scale well.

Asynchronous RL breaks this constraint by overlapping rollout generation and training. However, this introduces **off-policyness**: the policy version generating rollouts may lag behind the training version. To maximize inference throughput, AReaL also supports **partial rollouts**, where a single trajectory can be segmented across multiple policy versions.

<a id="key-techniques"></a>

## Key Techniques
AReaL addresses the aforementioned algorithmic challenges with two complementary techniques:

<a id="off-policyness-control"></a>

### 1. Off-Policyness Control
Limit how stale rollouts can be relative to the current training policy:

    rollout:
      max_head_offpolicyness: 4  # Allow up to 4 version steps behind

**Configuration tips:**

- Set to `0` for synchronous RL (useful for debugging or baseline comparisons)

- Higher values increase throughput but may reduce training stability

- Typical range: 2-8 depending on model size and update frequency

<a id="decoupled-ppo-objective"></a>

### 2. Decoupled PPO Objective
Handle off-policy data with modified loss computation:

    actor:
      use_decoupled_loss: true     # Enable decoupled PPO objective
      recompute_logprobs: true     # Recompute logprobs during training

**Configuration options:**

- `use_decoupled_loss`: When `false`, uses standard PPO/GRPO objectives

- `recompute_logprobs`: When `false`, reuses logprobs from inference backend

  - **Note:** Must be `true` when `use_decoupled_loss` is enabled

> **Note:** The decoupled PPO loss may conflict with certain algorithm configurations (e.g., SAPO). The effects of asynchrony on these newer algorithms remain largely understudied.

<a id="references"></a>

## References
For a practical walkthrough of asynchronous training, see our [GSM8K GRPO example](../tutorial/gsm8k_grpo.html).

For algorithmic details and empirical analysis, refer to the [AReaL paper](https://arxiv.org/pdf/2505.24298).

[](../customization/agent.html "previous page")

previous

Custom Agent Workflows

[](distillation.html "next page")

next

On-Policy Distillation

Contents

- [Overview](#overview)
- [Key Techniques](#key-techniques)
  - [1. Off-Policyness Control](#off-policyness-control)
  - [2. Decoupled PPO Objective](#decoupled-ppo-objective)
- [References](#references)

By AReaL Team

© Copyright 2026.  
