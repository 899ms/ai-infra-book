# Two nonzero control LoRAs

Prepare two deterministic, untrained BF16 rank8 q_proj adapters for all36 Qwen3-8B layers, seeds80301/80302, entries N(0,.05). Names and IDs distinct/immutable. No fine-tuning or quality claim.

Same1536-token synthetic input, greedy64 forced outputs; sequence base/base/A/A/B/B/A/base. One GPU adapter slot,2 CPU adapters,1GiBKV,APC on. Record actual requests/blocks with adapter names/IDs, cache counts, worker registered adapter IDs and GPU slot occupancy. Verify first use cold versus subsequent same-identity reuse, switching back, output stability; preserve differences without quality retries. Does not test name collisions, security/authentication, trained-adapter quality or concurrent tenant latency.
