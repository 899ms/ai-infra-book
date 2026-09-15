# Agent trace: native HBM / host capacity pressure

Twelve fixed recorded Agent inputs from the existing source-hashed trace. Qwen3-8B BF16 SGLang0.5.13.post1,16-token pages, native HiCache host memory, write_through, host ratio2, no storage backend. Three fresh engines at max_total_tokens4096/8192/16384, fixed order; observe effective pool via server info. This is a GPU/host capacity intervention, not independent hardware bandwidth benchmarking.

For every Agent turn: generate one forced token from the target input; generate one forced token from an unrelated3584-token pressure input; repeat target input with one forced token. Pressure IDs are uniformly sampled1000..9999 with seed908, one fixed input per turn shared across capacity settings. All target output IDs must be compared before/after pressure and across capacities. Retain any mismatch rather than assuming cache equivalence. No tools executed, no Agent quality claim.

Record native device/host/storage hit counters, total request times, input IDs, server configuration and GPU usage. Host recovery expected under4096 pressure; larger pools may retain target on device. Storage must remain0. No explicit cache flush, no fabricated host hit. One pass per capacity; no statistically established tail claim. Each engine shuts down before the next starts.
