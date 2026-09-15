# Two-worker native router lifecycle

Three trials executed; observations independently verified. SGLang 0.5.13.post1 and Router 0.3.2 use two fully resident BF16 Qwen3-8B workers on the author's exclusive RTX PRO 6000. The fixed archived Agent prefix contains 3136 tokens. Each request forces 16 output tokens at temperature zero; this measures cache and routing behavior, not full Agent task quality.

Three independent trials each contain 18 requests. First cold/warm target requests go through the native cache-aware router. Four unrelated 1627-token requests then pressure each worker's 4096-token pool directly, without flushing the router or worker caches. Two further routed target requests observe natural eviction and rewarming. The serving worker is killed; native health checks must mark it unhealthy before the failover requests. A fresh worker starts at the same address, and requests resume after native health checks report recovery. Direct requests finally inspect the restarted worker even if the router continues selecting the survivor. All request IDs are reconciled against native worker received/finished logs.

The router disables retries and uses a two-second health-check interval and five-second timeout. Detection timing is conditional on that configuration; this protocol does not measure in-flight request loss or retries. Worker selection after restart is an observation, not a forced success criterion. Driver 595.91.07 is used consistently; the earlier NVML override must not be injected.

Run `run.py` with the fixed server environment only after the preceding GPU experiment has exited. It requires at least 60 GiB free GPU memory and fresh results. Then copy the complete results including native request logs to the Mac and run `python3 analyze.py`. It preserves observations and hashes. Remote KV retrieval is a separate remaining experiment.

Startup attempt 001 used a one-second health-check timeout and was refused at worker registration: native /health responses take about one second. The formal run uses five seconds, with the same two-second poll interval; no inference requests were issued in the refused startup.

The first analyzer assumed fillers reached the 1800-token slicing cap; their actual encoded length was 1627. The saved input IDs and all response counts agree at 1627. The analyzer now checks the saved IDs directly. Capacity eviction still occurred on both workers; the observed input lengths are reported, not relabeled as 1800.

## Verified observations

All 54 requests completed and matched unique native received/finished records; all 30 target outputs were identical. In all three trials, cold/after-pressure/failover/direct-restart target requests reported zero cached tokens. Their repeated requests reported 3135/3136 cached input tokens. After native health recovery, cache-aware routing retained the warm survivor; the restarted worker remained cold until the explicit direct request. Worker identity varied across trials, and the same behavior occurred with either worker as the failed instance.

This completes native two-worker natural eviction and process-restart/failover observations for 9-9. The experiment does not include remote KV retrieval or in-flight request retry; those claims remain outside this result. The saved protocol had 16 forced output tokens and three trials, not a full Agent success evaluation.
