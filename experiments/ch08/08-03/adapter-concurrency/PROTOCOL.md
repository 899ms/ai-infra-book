# Two identities competing for one/two GPU LoRA slots

Reuse frozen nonzero control adapters A/B and same1536-token input. One engine with max_loras1, another with max_loras2; otherwise identical maxseq4,1GiBKV,APCon,eager. Warm A and B with1 token each, then3 barrier-separated waves of four concurrent requests A/B/A/B,64 forced outputs. Fixed one-slot then two-slot, no quality or general performance ranking from this fixed pair.

Read-only native scheduler observes actual request identity, status, blocks and scheduled tokens. Count distinct LoRA IDs among RUNNING requests, waiting and preemptions. Retain per-request start/first-token/end and per-identity observations; six formal requests per identity per condition are not a production tail distribution. Require complete lengths and compare outputs by identity/reference. No sleeps or artificial adapter queue simulation.
