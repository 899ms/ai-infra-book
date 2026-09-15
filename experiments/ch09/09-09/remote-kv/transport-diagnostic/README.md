# Mac–RTX transport diagnostic

Four direct SSH upload/return probes passed byte and SHA-256 checks. The 1 MiB payload in each direction took 2.759 s with default options and 2.597 s with the throughput option; these durations include SSH startup.

The actual HTTP framing protocol then transferred one 2,359,296-byte random page from RTX to the Mac store and back through SSH reverse forwarding. PUT took 1.532 s and GET 0.696 s on the same remote monotonic clock. The returned SHA-256 matched. The complete command took 4.142 s including connection setup; the Mac store was stopped afterward.

This verifies transport feasibility at this time, not model cache recovery or representative network throughput. Earlier failed transfers remain retained in the parent directory. See the scripts and JSON records for commands and timings.
