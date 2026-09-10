# Five completed media trace audits

The root confirmed all five replacement runs exited successfully after the runner source lock was extended to include network_validation.py. Each completed result was then independently read and audited; no candidate code was imported. All five audit processes exited0. The earlier baseline report is retained separately; this report does not treat manifest presence as execution proof.

| Scenario | Packets | Data packets | Wire bytes | Offered bytes | Delivered bytes | Audio played / missing | Screenshot usable |
| --- | ---: | ---: | ---: | ---: | ---: | --- | --- |
| book-image-baseline | 61600 | 30800 | 40656000 | 35000000 | 35000000 | — | — |
| book-mixed-fifo-immediate | 61626 | 30813 | 40673160 | 35016403 | 35008659 | 0 / 4/25 s | false (action incomplete) |
| book-mixed-fifo-aggregate | 46226 | 30813 | 39256360 | 35016403 | 35008659 | 0 / 4/25 s | false (action incomplete) |
| book-mixed-priority-immediate | 61642 | 30821 | 40683720 | 35016403 | 35016339 | 4/25 / 0 s | false (action incomplete) |
| book-mixed-priority-aggregate | 46237 | 30821 | 39266460 | 35016403 | 35016339 | 4/25 / 0 s | false (action incomplete) |

The isolated image keeps30800 data slices and35000000 delivered application bytes. All mixed inputs offer35016403B. FIFO sends/delivers35008659B: its7680B audio is not transmitted before expiry and the64B screenshot action is suppressed. Priority sends/delivers35016339B: audio plays all4/25s, while the64B screenshot action remains suppressed. Queue emptiness is not used as a success criterion.

For each FIFO/immediate pair the ACK aggregation choice changes network feedback and physical volume under the declared conditions; no universal protocol or controller performance claim follows. The two aggregate traces required checking3,928,719 and3,928,472 ACK-covered PN references respectively, including repeated historical ACK ranges. Those checks require every covered PN to have physically arrived before the ACK began serialization.

Exact report/result/checker hashes are in full-five-independent.json and the five per-result reports. The independent checks cover serialization, propagation, PN/frame identity, ACK causality, bytes, receive memory, compute dependencies, STREAM highest offsets, screenshot version/use and audio slot quality. They do not independently replay controller floating/integer state or extend to router-enabled scenarios.
