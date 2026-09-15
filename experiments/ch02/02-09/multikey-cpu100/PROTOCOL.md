# V4 multikey retry with less host offload

The first exclusive-device run in ../multikey/runs/multikey-exclusive-001 returned two responses, then the resource watchdog stopped it during the third because global available RAM crossed the fixed 24 GiB floor. All partial responses and telemetry are retained.

This retry uses the same full 43-layer fixed V4 checkpoint, private runtime, four 4148-token inputs, sampling, order, seed and correctness scorer. CPU offload changes from 110 to 100 GiB, using the author's exclusive GPU to reduce host memory pressure. The GPU process cap changes from 78 to 88 GiB; physical GPU-free floor remains 4 GiB, global available-RAM floor remains 24 GiB, start gates remain 140 GiB RAM and 80 GiB GPU, and all time/RSS limits remain fixed. Placement changes are not model identity or numerical clearance. No timing ranking against the earlier placement is claimed.

Fresh four-case execution is required, including the two previously returned cases. Negative outputs and interruptions count as observations; no case selection. Prior version and fixed model metadata checks remain in reproduce.py; source code and resource records are saved in the fresh run directory.
