# Actual LoRA projection check

Reuse frozen nonzero A/B control adapters. New base/A/B requests, same first512 prompt tokens, APC off, one forced output token (not task quality). Capture full first-layer QKV input/output and runtime stacked LoRA A/B tensors once per request with a read-only forward hook.

Require exact input equality, exact K/V output equality, nonzero Q changes for adapters. Independently compare Q delta with CPU FP64 (X A^T) B^T, using original safetensors, alpha/r=1. Report relative delta error; pre-fixed audit bound2% accommodates implementation BF16 output/intermediate rounding; this is numerical path validation, not task-quality threshold. Verify runtime Q tensors match adapter values and K/V LoRA tensors remain zero. Preserve any negative result; no tuning the threshold after output.
