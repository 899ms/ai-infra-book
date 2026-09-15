# Validator development notes

The first local ASR analysis reached the container-resource check after passing source, result, recovery, release, transport and fault checks, then rejected the capability spelling. Docker inspect records `CAP_NET_ADMIN`, while the analyzer expected `NET_ADMIN`. The analyzer now removes an optional `CAP_` prefix before checking the capability identity; the network mode, CPU, memory and actual netem checks remain unchanged. ASR then passed fully. This was an analyzer correction, not a rerun or changed measurement.

An initial local rsync failed because the local results parent directory did not yet exist. Creating it and repeating the copy succeeded; remote experiment execution was unaffected.
