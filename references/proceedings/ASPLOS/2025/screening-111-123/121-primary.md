<!-- 从 121-primary.html 迁移的资料快照；原始 HTML SHA-256: dd6e3829d6625dc3b4b1a0a8e3196eabcd0445c283d0c0377e450150c200ba2e。 -->

April 1, 2025

# Effective Kernel Fuzzing with Learned White-box Test Mutators

[](https://sishuaigong.github.io/pdf/asplos25-snowplow.pdf)

View publication

![](data:image/svg+xml;base64,PHN2ZyB2aWV3Ym94PSIwIC05NjAgOTYwIDk2MCIgYXJpYS1oaWRkZW49InRydWUiIGZpbGw9ImN1cnJlbnRDb2xvciIgaGVpZ2h0PSIyNHB4IiByb2xlPSJwcmVzZW50YXRpb24iIHdpZHRoPSIyNHB4IiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciPjxwYXRoIGQ9Ik0yMzcuNjktMTAwcS0yMy41MyAwLTQwLjYxLTE3LjA4VDE4MC0xNTcuNjl2LTQyNS45MnEwLTIzLjUzIDE3LjA4LTQwLjYxIDE3LjA4LTE3LjA5IDQwLjYxLTE3LjA5aDEzOC4yM3Y0NS4zOUgyMzcuNjlxLTQuNjEgMC04LjQ2IDMuODQtMy44NCAzLjg1LTMuODQgOC40N3Y0MjUuOTJxMCA0LjYxIDMuODQgOC40NiAzLjg1IDMuODQgOC40NiAzLjg0aDQ4NC42MnE0LjYxIDAgOC40Ni0zLjg0IDMuODQtMy44NSAzLjg0LTguNDZ2LTQyNS45MnEwLTQuNjItMy44NC04LjQ3LTMuODUtMy44NC04LjQ2LTMuODRINTgyLjg1di00NS4zOWgxMzkuNDZxMjMuNTMgMCA0MC42MSAxNy4wOVE3ODAtNjA3LjE0IDc4MC01ODMuNjF2NDI1LjkycTAgMjMuNTMtMTcuMDggNDAuNjFUNzIyLjMxLTEwMEgyMzcuNjlabTIxOS0yNDkuNjl2LTQ0OC41NGwtOTEuNDYgOTEuNDYtMzMtMzIuNjEgMTQ3LjE1LTE0Ni43NyAxNDYuNzcgMTQ2Ljc3LTMyLjYxIDMyLjYxLTkxLjQ2LTkxLjQ2djQ0OC41NGgtNDUuMzlaIiAvPjwvc3ZnPg==)

Share

[![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWxhYmVsPSJYIGxvZ28iIGNsYXNzPSJzaGFyZS1saXN0X19pY29uIiBmb2N1c2FibGU9ImZhbHNlIiBoZWlnaHQ9IjI0IiByb2xlPSJpbWciIHdpZHRoPSIyNCI+PHVzZSBocmVmPSIjeCIgLz48L3N2Zz4=)](https://twitter.com/intent/tweet?url=https://deepmind.google/research/publications/127036/&text=Effective%20Kernel%20Fuzzing%20with%20Learned%20White-box%20Test%20Mutators) [![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWxhYmVsPSJGYWNlYm9vayBsb2dvIiBjbGFzcz0ic2hhcmUtbGlzdF9faWNvbiIgZm9jdXNhYmxlPSJmYWxzZSIgaGVpZ2h0PSIyNCIgcm9sZT0iaW1nIiB3aWR0aD0iMjQiPjx1c2UgaHJlZj0iI2ZhY2Vib29rIiAvPjwvc3ZnPg==)](https://www.facebook.com/sharer/sharer.php?u=https://deepmind.google/research/publications/127036/) [![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWxhYmVsPSJMaW5rZWRJbiBsb2dvIiBjbGFzcz0ic2hhcmUtbGlzdF9faWNvbiIgZm9jdXNhYmxlPSJmYWxzZSIgaGVpZ2h0PSIyNCIgcm9sZT0iaW1nIiB3aWR0aD0iMjQiPjx1c2UgaHJlZj0iI2xpbmtlZGluIiAvPjwvc3ZnPg==)](https://www.linkedin.com/sharing/share-offsite/?url=https://deepmind.google/research/publications/127036/) [![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWxhYmVsPSJFbWFpbCBpY29uIiBjbGFzcz0ic2hhcmUtbGlzdF9faWNvbiIgZm9jdXNhYmxlPSJmYWxzZSIgaGVpZ2h0PSIyNCIgcm9sZT0iaW1nIiB3aWR0aD0iMjQiPjx1c2UgaHJlZj0iI2VtYWlsIiAvPjwvc3ZnPg==)](mailto:?subject=Effective%20Kernel%20Fuzzing%20with%20Learned%20White-box%20Test%20Mutators&body=https://deepmind.google/research/publications/127036/)

![](data:image/svg+xml;base64,PHN2ZyBhcmlhLWxhYmVsPSJMaW5rIGljb24iIGNsYXNzPSJzaGFyZS1saXN0X19pY29uIiBmb2N1c2FibGU9ImZhbHNlIiBoZWlnaHQ9IjI0IiByb2xlPSJpbWciIHdpZHRoPSIyNCI+PHVzZSBocmVmPSIjbGluayIgLz48L3N2Zz4=) Copied

## Abstract

Kernel fuzzers rely heavily on program mutation to automatically generate new test programs based on existing ones. In particular, program mutation can alter the test’s control and data flow inside the kernel by inserting new system calls, changing the values of call arguments, or performing other program mutations. However, due to the complexity of the kernel code and its user-space interface, finding the effective mutation that can lead to the desired outcome such as increasing the coverage and reaching a target code location is extremely difficult, even with the widespread use of manually-crafted heuristics.

This work proposes Snowplow, a kernel fuzzer that uses a learned white-box test mutator to enhance test mutation. The core of Snowplow is an efficient machine learning model that can learn to predict promising mutations given the test program to mutate, its kernel code coverage, and the desired coverage. Snowplow is demonstrated on argument mutations of the kernel tests, and evaluated on recent Linux kernel releases. When fuzzing the kernels for 24 hours, Snowplow shows a significant speedup of discovering new coverage (4.8×∼5.2×) and achieves higher overall coverage (7.0%∼8.6%). In a 7-day fuzzing campaign, Snowplow discovers 86 previously-unknown crashes. Furthermore, the learned mutator is shown to accelerate directed kernel fuzzing by reaching 19 target code locations 8.5× faster and two additional locations that are missed by the state-of-the-art directed kernel fuzzer.

## Authors

Sishuai Gong, Wang Rui, Deniz Altinbüken, Pedro Fonseca, Petros Maniatis

## Venue

ASPLOS 2025 (Fall Cycle)
