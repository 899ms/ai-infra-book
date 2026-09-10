# Shared-airtime observation-horizon review

Run from the repository root:

```sh
python3 calculations/research/shared-airtime-root-review/check-prefix.py
```

The checker executes each of the nine enabled wireless small workloads to its
original horizon, then executes the same input at event boundaries and between
them. Only `network.until` changes. The current report records 196 actual cutoff
runs and 980 comparisons, with source hashes checked before and after execution.
Zero is excluded because the public network contract requires a positive horizon.

The comparisons cover actual wireless events, each endpoint's sender events,
endpoint packet receipts, and the integral of reserved channel time clipped at
the observation horizon. Future planned arrival and feedback timestamps may
remain in a trace, but must not become actual receives, acknowledgments, or
retries before their events occur. A reservation that has started but whose DATA
has not started still consumes observed channel time under the declared model.

This is a causality consistency check against a longer actual run, not an
independent PHY or congestion-control implementation. The separate
`../shared-airtime-review/NETWORK-REVIEW.md` binds hand-derived small examples to
the current candidate. Neither report proves large-workload results or production
Wi-Fi behavior.

The operative ACK snapshot contract is source-dependent: a client-origin ACK
freezes when its first wireless DATA transmission starts; a server-origin ACK
freezes when its WAN transmission starts. Forwarding an ACK at the AP does not
authorize refreshing it with the server's later receive state. Earlier input
preparation prose that says all ACKs freeze at wireless start is superseded by
`../shared-airtime-loop/INTERFACE-CONTRACT.md` and this explicit topology rule.

All evidence remains research-only. The book has twelve current chapters;
historical `ch13` evidence identities do not authorize recreating a chapter.
