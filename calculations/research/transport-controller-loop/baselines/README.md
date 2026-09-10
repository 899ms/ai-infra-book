# Historical performance baseline

`bbr_adapter_c410_before_active_index.py` is the exact pre-index adapter (SHA256 `c4101a79a516d66f6ea002593b1f3e67e2e84d8dd5fe6372ef97d39a7049dc56`). It preserves the already-fixed idle epoch and persistent-congestion behavior, while scanning historical records for active flight.

It exists only for `../check-bbr-active-index.py` to execute both versions on identical callbacks and compare every returned event and snapshot. The checker gives the baseline the current adapter location for its unchanged frozen-core dependency lookup. Neither the network nor the production candidate imports this file. Do not migrate this historical duplicate into the public runtime package.

Run from the repository root:

```sh
python3 calculations/research/transport-controller-loop/check-bbr-active-index.py
```

The output records the current adapter, baseline, and checker SHA256, as well as callback count and event digest. Assertions compare full values before computing the digest.
