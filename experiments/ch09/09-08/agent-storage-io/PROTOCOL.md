# Actual Agent KV page local-storage timing

197 reusable native Qwen3-8B KV pages, each2359296bytes, selected from the same12 Agent input prefixes used in the verified cross-Mac run. Preserve source names, byte sizes and SHA-256. Copy into a new isolated RTX directory; copying itself is not counted as model recovery.

Linux ext4 O_DIRECT with anonymous mmap-aligned buffers. One new file per page: open exclusive, direct write, file fsync, close, parent-directory fsync; timing covers those calls, not source read/hash/buffer fill. Three direct-read passes with seeded shuffled order; timing covers open/readv/close, then SHA verified outside timed interval. Reject unavailable O_DIRECT or any short operation; no silent buffered fallback. O_DIRECT bypasses kernel data page cache, not necessarily hardware/controller caches. Device is the actual /dev/md0p1 mount, not assumed single-NVMe media.

Keep all source pages and timed copies; no global page-cache drop or unrelated file removal. Record filesystem/device metadata, source hashes, per-page times and terminal status. These are storage primitives on real KV payloads, not an SGLang request, production p95 or power-loss test. Subsequent policy/capacity replay must label timing composition and preserve this boundary.
