# Reproduced asyncio TCP_NODELAY default difference

A fresh TLS echo probe in the same ai-infra-book-net1204 Docker image reproduced:

| Socket creation | Python proto metadata | Client TCP_NODELAY | Accepted server TCP_NODELAY |
|---|---:|---:|---:|
| Implicit asyncio host/port |6|1|1|
| Manual socket.socket() |0|0|0|
| Manual explicit IPPROTO_TCP |6|1|1|

The archived Python3.11.16 asyncio._set_nodelay source checks sock.proto==IPPROTO_TCP before applying NODELAY. Kernel transport is TCP in all three cases; the difference is Python socket metadata and resulting option application. All three actual TLS echoes completed with identical4-byte payloads and closed sockets. This is a fresh reproduction of the source construction paths, not retrospective getsockopt reads of completed historical benchmark sockets.

The receive-window runners used manual proto0 sockets to set buffers before connect/accept, while the earlier reuse runners used implicit asyncio creation. Within each old window matrix this setting stayed fixed, so those measurements remain conditional evidence; cross-batch TCP absolute comparisons need the mismatch disclosed. receive-windows reruns all four workloads with explicit proto6 and NODELAY1 assertions/readbacks. Keep both batches separate, including the unchanged QUIC reruns.

The first probe launch used the filename inspect.py,which shadowed the standard-library inspect module and failed before measurement. Its source/log are retained in attempt-import. Renaming it probe.py resolved the import; this did not change socket policy. The successful probe source hash is bound in results/summary.json. No GPU,host network shaping,volume change or external service was used.
