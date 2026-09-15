import hashlib,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parent;S=json.loads((R/'summary.json').read_text())
fig,axes=plt.subplots(1,2,figsize=(10,4.5),sharey=True);top=max(max(c['samples_s']) for c in S['conditions'])*1.12
for ax,proto,title in zip(axes,['h1','h3'],['HTTP/1.1 + TLS 1.3','HTTP/3']):
 for i,policy in enumerate(['uninterrupted','restart','resume']):
  c=next(c for c in S['conditions'] if c['protocol']==proto and c['policy']==policy)
  ax.scatter([i-.1,i,i+.1],c['samples_s'],s=35,color='#167d9a',zorder=3);ax.plot([i-.25,i+.25],[c['median_s']]*2,color='#bc5739',linewidth=2.5)
 ax.set_xticks(range(3),['Uninterrupted','Full restart','Range resume']);ax.set_title(title);ax.set_ylim(0,top);ax.grid(axis='y',alpha=.2)
axes[0].set_ylabel('Complete verified image (seconds)');fig.suptitle('Image transfer after client connection interruption')
fig.text(.5,.015,'Three formal tasks per cell; dots = samples, line = median. Includes recorded CPU service and connection cleanup.',ha='center',fontsize=9)
fig.tight_layout(rect=[0,.045,1,.94])
for ext in ['png','svg','pdf']:fig.savefig(R/f'recovery-results.{ext}',dpi=160)
plt.close(fig)
s='''# Interrupted image transfer: restart versus retained-output continuation

All20 tasks passed independent complete-image verification:18 formal tasks and2 protocol warmups,32 real connection exchanges,12 injected client connection interruptions. The source is the same10,656,312-byte RAW and4,556,971-byte developed JPEG used in the image experiment. Each original/full-restart request uploads the complete RAW and replays0.483963046s measured CPU development time before returning the actual image. No new RAW development or GPU inference is claimed.

![All formal recovery timings](recovery-results.png)

| Protocol | Policy | Three completion times, seconds | Median seconds | Median post-interruption recovery seconds |
|---|---|---|---:|---:|
'''
for c in S['conditions']:
 recovery='—' if c['median_recovery_s'] is None else f"{c['median_recovery_s']:.3f}"
 s+=f"| {c['protocol']} | {c['policy']} | "+' / '.join(f'{v:.3f}' for v in c['samples_s'])+f" | {c['median_s']:.3f} | {recovery} |\n"
s+='''
There are only three formal samples per cell. HTTP/3 continuation was faster than the uninterrupted median in this batch; these are separate stochastic network realizations, not paired identical-loss runs, and this is not evidence of a negative fault penalty or that injecting a failure generally accelerates transfer. Preserve that observation without inventing a congestion explanation.

For each interrupted case, the client receives at least1MiB of JPEG, retains the exact prefix including read-chunk overshoot, and closes that connection. Full restart discards the prefix and repeats the complete RAW upload, processing wait and image download on a new connection. Range continuation reconnects, names the already materialized output and requests the suffix from the retained offset. It verifies206 status,Content-Range,ETag and complete reconstructed JPEG/RGB. Connection identities/ports are different across both recovery phases. HTTP/3 qlogs contain the actual close frames and response headers.

The continuation endpoint is an explicit test application route `/resume/{offset}` returning206 metadata; it is not a claim that an unmodified default browser or arbitrary server automatically supports HTTP Range recovery. The server retains an immutable finished JPEG in memory under an operation ID. This is output-byte recovery with a surviving server and retained client prefix. It does not recover server-process loss, incomplete RAW uploads, lost GPU state or a changed output version.

## Time and byte boundaries

Completion starts before the first connection and ends after connection cleanup, response-file writes and full RGB validation. The QUIC client also serializes its qlog during cleanup. Consequently these task times include different housekeeping boundaries from the earlier image-records request-only table and must not be pooled with it. Recovery time starts at the first connection-close call, so it includes closing that connection, opening the replacement, retry/suffix work and final validation. No artificial backoff is configured, but close/drain and local persistence work happen before reconnecting.

| Protocol | Policy | RAW upload bytes per task | Client-retained response bytes, three trials | Median connection-close duration seconds |
|---|---|---:|---|---:|
'''
for c in S['conditions']:s+=f"| {c['protocol']} | {c['policy']} | {c['upload_bytes'][0]:,} | {c['client_retained_bytes']} | {c['median_close_s']:.3f} |\n"
s+='''
Restart reuploads21,312,624 RAW bytes per task; continuation uploads10,656,312 and uses an empty suffix-request body. Restart retains the discarded prefix plus the full replacement image; continuation retains exactly one complete image across both exchanges. Retained application bytes are not network wire bytes. In particular, the original server may already have queued the full JPEG when the client closes; prepared_response_bytes records that output size but does not claim every queued byte crossed the network or reached the client. There were26 processing waits, including warmups and restart duplicates; resume does not repeat that wait.

## Verification and scope

Every stored prefix/full/suffix was reread and hashed. All20 final images were reconstructed and fully decoded again in the independent analyzer. It checks source identity, task order, all32 server request/response records, exact service counts/waits, timeline ordering, fresh recovery connections, TLS/ALPN/ETag/range metadata,16 HTTP/3 response headers and close frames. Server close errors, if present, are retained and allowed only for the deliberately interrupted original-image operations. They are not hidden as unrelated successful server work.

Three repetitions shuffle protocol×policy with defaults held fixed. The actual transport runs in one Docker network-none namespace:netem40ms per traversal/20Mbit/s/0.1% random loss,2CPU/2GiB. Container identity/resources and before/after drained queues are verified; the own container was removed. CPU scheduling, stochastic loss and shared client/server event loop limit generalization. A close is deliberately injected after a payload threshold, rather than an uncontrolled physical link outage. Neither acoustic playback nor recovery of another workload is established by this image result.

Revalidate with the Pillow environment: `python analyze.py`; generate the figure/report with `python report.py`. run.sh launches the isolated experiment and cleans its container on exit. PROTOCOL.md retains the original preparation wording as a dated design artifact; the completed result is this report and summary.json. The remaining12-4 work is the cross-workload coverage/contribution review and any measurements that review identifies, plus the separately unmeasured acoustic boundary.
'''
(R/'README.md').write_text(s)
files={str(p.relative_to(R)):dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in R.rglob('*') if p.is_file() and p.name!='manifest.json' and '__pycache__' not in p.parts}
(R/'manifest.json').write_text(json.dumps(dict(scope='Actual image connection interruption and retained-output recovery; parent incomplete',files=files),indent=2)+'\n')
