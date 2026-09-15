# ASR,TTS and Computer Use recovery contracts

Preparation only. Run after receive-windows and transfer-chunks finish,without another own benchmark container. Preserve their explicit TCP_NODELAY1 checks,default receive limits,pinned Docker2CPU/2GiB and netem80ms RTT/20Mbit/s/0.1% loss. These are actual transport/application recovery tests around fixed model-result/time records,not new GPU inference. Server source jobs survive client disconnection in memory; server crash/durable storage/GPU checkpoint recovery are not covered.

Compare uninterrupted,full request restart,and retrieval/continuation of the original operation. Each workload has three shuffled protocol×policy repetitions plus one warmup per protocol. Every recovery uses a new connection. Preserve original operations and all failed attempts; never count an empty or truncated result as usable. Log request identities,prompt/input hashes,operation creation,producer/service timing,client close/reconnect,result headers,all received bytes and final result validation. The server starts source production once per operation after complete upload. A full restart creates a new operation and repeats the source wait/release schedule. A retrieval uses the original operation without rerunning source service.

## ASR

Use the existing actual WAV/transcript pair and0.622926892s measured model-service wait. Inject failure after the server has received the complete WAV,created its operation,and returned response headers,but before the transcript is delivered. Verify the close begins before that operation's source-service completion. Restart reuploads the WAV to a new operation; retrieval reconnects with the old operation ID and no repeated audio body,awaiting or fetching its exact transcript. This does not claim byte-range resumption of a partial audio upload or streaming ASR.

20 tasks including2 warmups yield32 exchanges,12 intentional failures and26 source jobs. All complete UTF8/transcript hashes must pass. A surviving in-memory pending/completed result is an explicit prerequisite,not free durable recovery.

## TTS

Use the exact WAV/PCM and294-part source client-read availability trace. An independent producer advances the original operation's available byte range at the recorded release times even if one response connection closes. Inject failure after the first complete20ms PCM frame is retained by the client,including real read-chunk overshoot. Restart creates a new operation and replaces the retained prefix with a full fresh replay. Continuation requests the suffix of the old operation at the exact retained byte offset and may wait for remaining original releases. Never expose a byte before its original operation's release time merely because the fixture is already on disk.

20 tasks/32 exchanges/12 failures/26 source jobs. Verify complete WAV and PCM identity,all producer release times,exact suffix range/ETag/operation identity,and no missing or duplicated bytes in final reconstruction. Count discarded/retransmitted prefix bytes separately. This measures retained-byte continuity and available frames,not glitch-free acoustic playback; a full restart cannot undo audio a real speaker has already played.

## Computer Use

Use the complete8-round source screenshot/instruction/action trace. Inject one failure at round3 after full request receipt/response headers,during the recorded model-service interval and before action JSON is delivered. Resume retrieves the same operation; restart resubmits only that round with a new operation ID. Preserve already-delivered earlier rounds and continue later rounds only after exact current action validation. The client must deliver exactly one action per round ID in order.

18 formal traces×8 original exchanges plus12 recovery exchanges and2 one-round warmups=158 exchanges,with152 source jobs (144 original formal+6 restart duplicates+2 warmups). This tests before-action-delivery failure; it does not establish safe retries after a browser/tool effect happened but its acknowledgement was lost. Source live-browser success remains in computer-use; a stored-action delivery ledger is not a new browser/model task.

## Reporting boundary

Completion includes connection cleanup,response persistence and final client validation,as in the earlier image-recovery experiment. Per-stage counters distinguish source jobs from network exchanges and server-prepared/available bytes from client-retained or wire bytes. HTTP3 close/drain/qlog work is included and disclosed. A small median from a different random-loss realization is not a negative fault cost or general recovery speedup. Full result and source identity,model-job counts,transport negotiation,explicit socket options,netem queues and cleanup must verify before updating completion status.
