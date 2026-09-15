# Agent KV local direct-I/O measurement

197 actual native Agent KV pages (443.25MiB) were copied into a fresh RTX directory and checked against their original Mac SHA-256 values. The benchmark completed197 O_DIRECT writes with file+directory fsync and591 O_DIRECT reads across three shuffled passes. Every read returned the full page and passed SHA verification.

| Operation | Count | Median page time | Sample p95 page time | Sum of timed operations |
|---|---:|---:|---:|---:|
| direct_write_fsync | 197 | 6.765547ms | 11.745311ms | 1.485388s |
| direct_read | 591 | 0.832117ms | 1.074384ms | 0.536213s |

Each page is2359296bytes (2.25MiB). The measured filesystem is ext4 on /dev/md0p1; it is not labeled as a single NVMe drive. O_DIRECT bypasses kernel data page cache, not hardware/controller caches. Source read, aligned-buffer fill and checksum work are outside the timed write; checksums are outside read timing. File open/close are included. The write contract includes fsync and is stronger than the existing remote HTTP store's non-fsynced publication.

The remote source and written copies are retained under /home/ubuntu/ai-infra-book-experiments/ch09/09-08/agent-storage-io; original payloads already exist locally in the source cross-Mac store. Per-operation records and source hashes are local. No GPU engine, global cache drop, other files or model cache were modified. These are actual storage primitives, not complete model-recovery requests or a stable request p95 estimate.

Run `python3 experiments/ch09/09-08/agent-storage-io/analyze.py` to recheck original page identities, all788 operations, seeded ordering and summaries.
