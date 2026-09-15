# Actual RAW development and final-image transfer

The pinned10,656,312-byte RAW was developed into a full-resolution4284×2844 sRGB JPEG on Mac and RTX CPU. This is a specified conventional RAW-development pipeline, not neural image editing. It supplies an actual original/final-image pair for the transport experiment; no general aesthetic improvement or AI speedup is claimed.

![Developed aurora preview; full-resolution JPEG is retained separately](mac-results/preview.png)

The display preview was visually inspected: the auroral scene is intact. It is not used as the network response. The client receives and fully decodes the4,556,971-byte RTX JPEG, checking its full-resolution RGB identity.

## Actual processing

| Platform | Formal processing seconds | JPEG bytes | JPEG PSNR against developed RGB |
|---|---|---:|---:|
| mac | 0.502830 / 0.496538 / 0.497168 | 4,557,008 | 41.8046 dB |
| rtx | 0.483963 / 0.500246 / 0.477382 | 4,556,971 | 41.8046 dB |

Each platform ran one warmup and three formal complete RAW-read/develop/JPEG-encode/write iterations. PNG/preview generation and quality checks are outside the timed processing interval. Hashes are identical across repetitions on each platform. Writes were not fsynced; this is not a power-loss persistence benchmark.

Mac and RTX output pixels are not exactly equal:195 channel values differ, with maximum absolute difference7/255; JPEG sizes differ by37 bytes. Both originals and every produced JPEG remain intact. Mac LibRaw reports OPENMP=false, while RTX reports OPENMP=true with OMP_NUM_THREADS=2 and Docker2CPU quota. Consequently these similar elapsed times are not a controlled two-thread hardware comparison. Both paths are CPU processing; the RTX GPU is not used.

Parameters are fixed in [protocol](PROTOCOL.md): AHD,camera white balance,sRGB,gamma(2.222,4.5),exposure1.25,no auto-brightening,no rotation,JPEGquality95/4:4:4. The first launch on both platforms rejected a list-valued gamma argument before any image result; attempt-gamma preserves the source and errors. The successful correction changes the container type to the required tuple, not the numerical setting.

## Controlled-network result delivery

One Docker network-none netem profile configures80ms RTT,20Mbit/s and0.1% random loss. Three shuffled repetitions compare protocol×connection reuse off/on, two sequential requests per cell, plus one warmup per protocol:26 total. Each uploads the complete RAW, replays the measured median RTX CPU service, and returns the actual finished JPEG. The client fully decodes and hashes its pixels before declaring validation complete. Processing replay starts after upload; no partial-RAW overlap or26 new developments are claimed.

| Protocol | Reuse | Median complete validated request ms |
|---|---|---:|
| h1 | False | 7548.529 |
| h1 | True | 7300.420 |
| h3 | False | 17414.692 |
| h3 | True | 22037.389 |

Every table cell has six formal requests. Reuse-on includes each pair's first fresh connection and second reused request. Network time includes actual upload/download and client image decoding, plus an explicitly replayed0.483963046s processing interval. It is not a new GPU inference time. Short calibrated RTT/goodput, protocol versions and image identities are archived; random drop positions and host scheduling can differ.

The final common120s-deadline batch passed all26 RAW/JPEG hashes, complete RGB hashes, TLS/ALPN, reuse, qlogs, service timing, netem settings and queue-drain checks. Processing and network container absence are recorded. The network fixture selects the RTX formal-run JPEG; it does not silently substitute the nearly-equal Mac result.

The entire initial batch is retained in network-results:17/26 validated,9 HTTP3 timeouts. Its inherited20s whole-response timeout for HTTP3 versus20s per-read timeout for HTTP1 was asymmetric, and late HTTP3 results triggered InvalidStateError after the future was cancelled. Qlogs show several late responses around24–29s. That batch is a deadline/handler diagnostic, not a fair protocol ranking. The final batch in network120-results uses a common120s body-request deadline, guards completed futures and closes failed connections; all26 requests were rerun, not only the failed samples. Initial and final timings are not pooled.

Revalidate with the NumPy/Pillow environment: `python analyze_image.py`, then `python analyze_network120.py loss0.1`. run_image.py requires rawpy0.27.1/Pillow12.1.1 and the pinned RAW. Source provenance, actual package/build identities and processing environment are retained. Use fresh result directories for reruns.

This completes the specified image-processing and original/final-image network-record workload. Computer Use, window sizing, interrupted recovery and final cross-workload integration remain outstanding in12-4. No physical acoustic experiment is implied by these records.
