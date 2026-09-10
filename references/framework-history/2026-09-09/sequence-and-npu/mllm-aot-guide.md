<!-- 从 mllm-aot-guide.html 迁移的资料快照；原始 HTML SHA-256: 03f3ee9119ec9c2cc3bfe7a5e7487d856e6feb7aa2bf5c39dcfdb7e5ea0a2ac5。 -->

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHN0eWxlPSJkaXNwbGF5OiBub25lOyI+CiAgPHN5bWJvbCBpZD0ic3ZnLXRvYyIgdmlld2JveD0iMCAwIDI0IDI0Ij4KICAgIDx0aXRsZT5Db250ZW50czwvdGl0bGU+CiAgICA8c3ZnIHN0cm9rZT0iY3VycmVudENvbG9yIiBmaWxsPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMCIgdmlld2JveD0iMCAwIDEwMjQgMTAyNCI+CiAgICAgIDxwYXRoIGQ9Ik00MDggNDQyaDQ4MGM0LjQgMCA4LTMuNiA4LTh2LTU2YzAtNC40LTMuNi04LTgtOEg0MDhjLTQuNCAwLTggMy42LTggOHY1NmMwIDQuNCAzLjYgOCA4IDh6bS04IDIwNGMwIDQuNCAzLjYgOCA4IDhoNDgwYzQuNCAwIDgtMy42IDgtOHYtNTZjMC00LjQtMy42LTgtOC04SDQwOGMtNC40IDAtOCAzLjYtOCA4djU2em01MDQtNDg2SDEyMGMtNC40IDAtOCAzLjYtOCA4djU2YzAgNC40IDMuNiA4IDggOGg3ODRjNC40IDAgOC0zLjYgOC04di01NmMwLTQuNC0zLjYtOC04LTh6bTAgNjMySDEyMGMtNC40IDAtOCAzLjYtOCA4djU2YzAgNC40IDMuNiA4IDggOGg3ODRjNC40IDAgOC0zLjYgOC04di01NmMwLTQuNC0zLjYtOC04LTh6TTExNS40IDUxOC45TDI3MS43IDY0MmM1LjggNC42IDE0LjQuNSAxNC40LTYuOVYzODguOWMwLTcuNC04LjUtMTEuNS0xNC40LTYuOUwxMTUuNCA1MDUuMWE4Ljc0IDguNzQgMCAwIDAgMCAxMy44eiIgLz4KICAgIDwvc3ZnPg==)

Menu

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iZmVhdGhlci1tZW51Ij4KICAgICAgPGxpbmUgeDE9IjMiIHkxPSIxMiIgeDI9IjIxIiB5Mj0iMTIiPjwvbGluZT4KICAgICAgPGxpbmUgeDE9IjMiIHkxPSI2IiB4Mj0iMjEiIHkyPSI2Ij48L2xpbmU+CiAgICAgIDxsaW5lIHgxPSIzIiB5MT0iMTgiIHgyPSIyMSIgeTI9IjE4Ij48L2xpbmU+CiAgICA8L3N2Zz4=)

Expand

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iZmVhdGhlci1jaGV2cm9uLXJpZ2h0Ij4KICAgICAgPHBvbHlsaW5lIHBvaW50cz0iOSAxOCAxNSAxMiA5IDYiPjwvcG9seWxpbmU+CiAgICA8L3N2Zz4=)

Light mode

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iZmVhdGhlci1zdW4iPgogICAgICA8Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSI1Ij48L2NpcmNsZT4KICAgICAgPGxpbmUgeDE9IjEyIiB5MT0iMSIgeDI9IjEyIiB5Mj0iMyI+PC9saW5lPgogICAgICA8bGluZSB4MT0iMTIiIHkxPSIyMSIgeDI9IjEyIiB5Mj0iMjMiPjwvbGluZT4KICAgICAgPGxpbmUgeDE9IjQuMjIiIHkxPSI0LjIyIiB4Mj0iNS42NCIgeTI9IjUuNjQiPjwvbGluZT4KICAgICAgPGxpbmUgeDE9IjE4LjM2IiB5MT0iMTguMzYiIHgyPSIxOS43OCIgeTI9IjE5Ljc4Ij48L2xpbmU+CiAgICAgIDxsaW5lIHgxPSIxIiB5MT0iMTIiIHgyPSIzIiB5Mj0iMTIiPjwvbGluZT4KICAgICAgPGxpbmUgeDE9IjIxIiB5MT0iMTIiIHgyPSIyMyIgeTI9IjEyIj48L2xpbmU+CiAgICAgIDxsaW5lIHgxPSI0LjIyIiB5MT0iMTkuNzgiIHgyPSI1LjY0IiB5Mj0iMTguMzYiPjwvbGluZT4KICAgICAgPGxpbmUgeDE9IjE4LjM2IiB5MT0iNS42NCIgeDI9IjE5Ljc4IiB5Mj0iNC4yMiI+PC9saW5lPgogICAgPC9zdmc+)

Dark mode

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iaWNvbi10YWJsZXItbW9vbiI+CiAgICAgIDxwYXRoIHN0cm9rZT0ibm9uZSIgZD0iTTAgMGgyNHYyNEgweiIgZmlsbD0ibm9uZSIgLz4KICAgICAgPHBhdGggZD0iTTEyIDNjLjEzMiAwIC4yNjMgMCAuMzkzIDBhNy41IDcuNSAwIDAgMCA3LjkyIDEyLjQ0NmE5IDkgMCAxIDEgLTguMzEzIC0xMi40NTR6IiAvPgogICAgPC9zdmc+)

Auto light/dark, in light mode

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iaWNvbi1jdXN0b20tZGVyaXZlZC1mcm9tLWZlYXRoZXItc3VuLWFuZC10YWJsZXItbW9vbiI+CiAgICAgIDxwYXRoIHN0eWxlPSJvcGFjaXR5OiA1MCUiIGQ9Ik0gNS40MTEgMTQuNTA0IEMgNS40NzEgMTQuNTA0IDUuNTMyIDE0LjUwNCA1LjU5MSAxNC41MDQgQyAzLjYzOSAxNi4zMTkgNC4zODMgMTkuNTY5IDYuOTMxIDIwLjM1MiBDIDcuNjkzIDIwLjU4NiA4LjUxMiAyMC41NTEgOS4yNSAyMC4yNTIgQyA4LjAyMyAyMy4yMDcgNC4wNTYgMjMuNzI1IDIuMTEgMjEuMTg0IEMgMC4xNjYgMTguNjQyIDEuNzAyIDE0Ljk0OSA0Ljg3NCAxNC41MzYgQyA1LjA1MSAxNC41MTIgNS4yMzEgMTQuNSA1LjQxMSAxNC41IEwgNS40MTEgMTQuNTA0IFoiIC8+CiAgICAgIDxsaW5lIHgxPSIxNC41IiB5MT0iMy4yNSIgeDI9IjE0LjUiIHkyPSIxLjI1Ij48L2xpbmU+CiAgICAgIDxsaW5lIHgxPSIxNC41IiB5MT0iMTUuODUiIHgyPSIxNC41IiB5Mj0iMTcuODUiPjwvbGluZT4KICAgICAgPGxpbmUgeDE9IjEwLjA0NCIgeTE9IjUuMDk0IiB4Mj0iOC42MyIgeTI9IjMuNjgiPjwvbGluZT4KICAgICAgPGxpbmUgeDE9IjE5IiB5MT0iMTQuMDUiIHgyPSIyMC40MTQiIHkyPSIxNS40NjQiPjwvbGluZT4KICAgICAgPGxpbmUgeDE9IjguMiIgeTE9IjkuNTUiIHgyPSI2LjIiIHkyPSI5LjU1Ij48L2xpbmU+CiAgICAgIDxsaW5lIHgxPSIyMC44IiB5MT0iOS41NSIgeDI9IjIyLjgiIHkyPSI5LjU1Ij48L2xpbmU+CiAgICAgIDxsaW5lIHgxPSIxMC4wNDQiIHkxPSIxNC4wMDYiIHgyPSI4LjYzIiB5Mj0iMTUuNDIiPjwvbGluZT4KICAgICAgPGxpbmUgeDE9IjE5IiB5MT0iNS4wNSIgeDI9IjIwLjQxNCIgeTI9IjMuNjM2Ij48L2xpbmU+CiAgICAgIDxjaXJjbGUgY3g9IjE0LjUiIGN5PSI5LjU1IiByPSIzLjYiPjwvY2lyY2xlPgogICAgPC9zdmc+)

Auto light/dark, in dark mode

![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iaWNvbi1jdXN0b20tZGVyaXZlZC1mcm9tLWZlYXRoZXItc3VuLWFuZC10YWJsZXItbW9vbiI+CiAgICAgIDxwYXRoIGQ9Ik0gOC4yODIgNy4wMDcgQyA4LjM4NSA3LjAwNyA4LjQ5NCA3LjAwNyA4LjU5NSA3LjAwNyBDIDUuMTggMTAuMTg0IDYuNDgxIDE1Ljg2OSAxMC45NDIgMTcuMjQgQyAxMi4yNzUgMTcuNjQ4IDEzLjcwNiAxNy41ODkgMTUgMTcuMDY2IEMgMTIuODUxIDIyLjIzNiA1LjkxIDIzLjE0MyAyLjUwNSAxOC42OTYgQyAtMC44OTcgMTQuMjQ5IDEuNzkxIDcuNzg2IDcuMzQyIDcuMDYzIEMgNy42NTIgNy4wMjEgNy45NjUgNyA4LjI4MiA3IEwgOC4yODIgNy4wMDcgWiIgLz4KICAgICAgPGxpbmUgc3R5bGU9Im9wYWNpdHk6IDUwJSIgeDE9IjE4IiB5MT0iMy43MDUiIHgyPSIxOCIgeTI9IjIuNSI+PC9saW5lPgogICAgICA8bGluZSBzdHlsZT0ib3BhY2l0eTogNTAlIiB4MT0iMTgiIHkxPSIxMS4yOTUiIHgyPSIxOCIgeTI9IjEyLjUiPjwvbGluZT4KICAgICAgPGxpbmUgc3R5bGU9Im9wYWNpdHk6IDUwJSIgeDE9IjE1LjMxNiIgeTE9IjQuODE2IiB4Mj0iMTQuNDY0IiB5Mj0iMy45NjQiPjwvbGluZT4KICAgICAgPGxpbmUgc3R5bGU9Im9wYWNpdHk6IDUwJSIgeDE9IjIwLjcxMSIgeTE9IjEwLjIxMiIgeDI9IjIxLjU2MyIgeTI9IjExLjA2MyI+PC9saW5lPgogICAgICA8bGluZSBzdHlsZT0ib3BhY2l0eTogNTAlIiB4MT0iMTQuMjA1IiB5MT0iNy41IiB4Mj0iMTMuMDAxIiB5Mj0iNy41Ij48L2xpbmU+CiAgICAgIDxsaW5lIHN0eWxlPSJvcGFjaXR5OiA1MCUiIHgxPSIyMS43OTUiIHkxPSI3LjUiIHgyPSIyMyIgeTI9IjcuNSI+PC9saW5lPgogICAgICA8bGluZSBzdHlsZT0ib3BhY2l0eTogNTAlIiB4MT0iMTUuMzE2IiB5MT0iMTAuMTg0IiB4Mj0iMTQuNDY0IiB5Mj0iMTEuMDM2Ij48L2xpbmU+CiAgICAgIDxsaW5lIHN0eWxlPSJvcGFjaXR5OiA1MCUiIHgxPSIyMC43MTEiIHkxPSI0Ljc4OSIgeDI9IjIxLjU2MyIgeTI9IjMuOTM3Ij48L2xpbmU+CiAgICAgIDxjaXJjbGUgc3R5bGU9Im9wYWNpdHk6IDUwJSIgY3g9IjE4IiBjeT0iNy41IiByPSIyLjE2OSI+PC9jaXJjbGU+CiAgICA8L3N2Zz4=) ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iaWNvbi10YWJsZXItcGVuY2lsLWNvZGUiPgogICAgICA8cGF0aCBkPSJNNCAyMGg0bDEwLjUgLTEwLjVhMi44MjggMi44MjggMCAxIDAgLTQgLTRsLTEwLjUgMTAuNXY0IiAvPgogICAgICA8cGF0aCBkPSJNMTMuNSA2LjVsNCA0IiAvPgogICAgICA8cGF0aCBkPSJNMjAgMjFsMiAtMmwtMiAtMiIgLz4KICAgICAgPHBhdGggZD0iTTE3IDE3bC0yIDJsMiAyIiAvPgogICAgPC9zdmc+) ![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIHN0cm9rZS13aWR0aD0iMSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBjbGFzcz0iaWNvbi10YWJsZXItZXllLWNvZGUiPgogICAgICA8cGF0aCBzdHJva2U9Im5vbmUiIGQ9Ik0wIDBoMjR2MjRIMHoiIGZpbGw9Im5vbmUiIC8+CiAgICAgIDxwYXRoIGQ9Ik0xMCAxMmEyIDIgMCAxIDAgNCAwYTIgMiAwIDAgMCAtNCAwIiAvPgogICAgICA8cGF0aCBkPSJNMTEuMTEgMTcuOTU4Yy0zLjIwOSAtLjMwNyAtNS45MSAtMi4yOTMgLTguMTEgLTUuOTU4YzIuNCAtNCA1LjQgLTYgOSAtNmMzLjYgMCA2LjYgMiA5IDZjLS4yMSAuMzUyIC0uNDI3IC42ODggLS42NDcgMS4wMDgiIC8+CiAgICAgIDxwYXRoIGQ9Ik0yMCAyMWwyIC0ybC0yIC0yIiAvPgogICAgICA8cGF0aCBkPSJNMTcgMTdsLTIgMmwyIDIiIC8+CiAgICA8L3N2Zz4=)

[Skip to content](#furo-main-content)

![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctbWVudSIgLz48L3N2Zz4=)

[](../index.html)

MLLM  
2.0.0 documentation

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0idGhlbWUtaWNvbi13aGVuLWF1dG8tbGlnaHQiPjx1c2UgaHJlZj0iI3N2Zy1zdW4td2l0aC1tb29uIiAvPjwvc3ZnPg==) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0idGhlbWUtaWNvbi13aGVuLWF1dG8tZGFyayI+PHVzZSBocmVmPSIjc3ZnLW1vb24td2l0aC1zdW4iIC8+PC9zdmc+) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0idGhlbWUtaWNvbi13aGVuLWRhcmsiPjx1c2UgaHJlZj0iI3N2Zy1tb29uIiAvPjwvc3ZnPg==) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0idGhlbWUtaWNvbi13aGVuLWxpZ2h0Ij48dXNlIGhyZWY9IiNzdmctc3VuIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctdG9jIiAvPjwvc3ZnPg==)

[MLLM  
2.0.0 documentation](../index.html)

- [Quick Start](../quick_start/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [How to Support a New LLM: Step-by-Step](../quick_start/how_to_model.html)
  - [How to Add a New Operator in MLLM](../quick_start/how_to_add_op.html)
  - [How to run modules async](../quick_start/how_to_async.html)
  - [How to perf modules](../quick_start/how_to_perf.html)

&nbsp;

- [Mllm API Service](../service/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [MLLM CLI](../service/mllm_cli.html)

&nbsp;

- [Architectures](../arch/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [MLLM Framework Core Architecture](../arch/arch.html)
  - [Tensor](../arch/tensor.html)
  - [Supported MLLM aops Operations](../arch/support_ops.html)
  - [Op Plugin System](../arch/op_plugin_system.html)

&nbsp;

- [Compile](../compile/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [MLLM IR](../compile/ir.html)

&nbsp;

- [Quantization](../quantization/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [Data Types in MLLM](../quantization/data_types.html)
  - [How to Add New Data Types](../quantization/how_to_add_new_dtype.html)

&nbsp;

- [MLLM LM Cache](../cache/index.html)

&nbsp;

- [pymllm Runtime](../pymllm_runtime/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [pymllm Setup and Usage](../pymllm_runtime/setup_and_usage.html)
  - [pymllm Runtime Design](../pymllm_runtime/runtime_design.html)
  - [pymllm Models and Quantization](../pymllm_runtime/models_and_quantization.html)
  - [pymllm Kernels and Acceleration](../pymllm_runtime/kernels_and_acceleration.html)
  - [pymllm Developer Guide](../pymllm_runtime/developer_guide.html)

&nbsp;

- [CPU Backend](../cpu_backend/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [Parallel API and Thread Configuration in MLLM](../cpu_backend/threads.html)
  - [FA2, Radix, Paged](../cpu_backend/fa2_radix_paged.html)
  - [CPU ARM Backend](../cpu_backend/arm/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [MLLM Self Hosted BLAS](../cpu_backend/arm/mllm_blas.html)
    - [Multithread Behaviors in CPU Backend](../cpu_backend/arm/multithread_behaviors.html)
  - [CPU X86 Backend](../cpu_backend/x86/index.html)

&nbsp;

- [Ascend Backend](../ascend_backend/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [Ascend Setup and Usage](../ascend_backend/setup_and_usage.html)
  - [Ascend Backend Design](../ascend_backend/core_design.html)
  - [Qwen Ascend](../ascend_backend/qwen_ascend.html)

&nbsp;

- [QNN Backend](index.html)☒ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [QNN Environment Setup](setup_env.html)
  - [QNN Backend Design](core_design.html)
  - [QNN AOT Execution Flow](#)

&nbsp;

- [OpenCL Backend](../opencl_backend/index.html)

&nbsp;

- [MLLM C++ API](../api/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [mllm API](../api/mllm.html)
  - [Neural Network Layers API](../api/nn.html)
  - [Functional API](../api/functional.html)
  - [Tensor API](../api/tensor.html)
  - [ARGeneration API](../api/argeneration.html)
  - [Module API](../api/module.html)
  - [Layer API](../api/layer.html)

&nbsp;

- [Contribute](../contribute/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [Roadmap & Help wanted!](../contribute/roadmap.html)
  - [Guidelines](../contribute/guidelines.html)
  - [Model Supports](../contribute/model_supports.html)

&nbsp;

- [Talks](../talks/index.html)

&nbsp;

- [Algorithm](../algorithms/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [Pruning](../algorithms/pruning.html)

&nbsp;

- [FAQ](../qa/index.html)

Pymllm API

- [pymllm](../autoapi/pymllm/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
  - [pymllm.\_\_main\_\_](../autoapi/pymllm/__main__/index.html)
  - [pymllm.bench_one_batch](../autoapi/pymllm/bench_one_batch/index.html)
  - [pymllm.bench_serve](../autoapi/pymllm/bench_serve/index.html)
  - [pymllm.configs](../autoapi/pymllm/configs/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [pymllm.configs.global_config](../autoapi/pymllm/configs/global_config/index.html)
    - [pymllm.configs.model_config](../autoapi/pymllm/configs/model_config/index.html)
    - [pymllm.configs.quantization_config](../autoapi/pymllm/configs/quantization_config/index.html)
    - [pymllm.configs.server_config](../autoapi/pymllm/configs/server_config/index.html)
  - [pymllm.engine](../autoapi/pymllm/engine/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [pymllm.engine.forward_batch](../autoapi/pymllm/engine/forward_batch/index.html)
    - [pymllm.engine.io_struct](../autoapi/pymllm/engine/io_struct/index.html)
    - [pymllm.engine.launch](../autoapi/pymllm/engine/launch/index.html)
  - [pymllm.executor](../autoapi/pymllm/executor/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [pymllm.executor.cuda_graph_runner](../autoapi/pymllm/executor/cuda_graph_runner/index.html)
    - [pymllm.executor.model_runner](../autoapi/pymllm/executor/model_runner/index.html)
  - [pymllm.layers](../autoapi/pymllm/layers/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [pymllm.layers.attention](../autoapi/pymllm/layers/attention/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
      - [pymllm.layers.attention.attention_backend](../autoapi/pymllm/layers/attention/attention_backend/index.html)
      - [pymllm.layers.attention.flashinfer_backend](../autoapi/pymllm/layers/attention/flashinfer_backend/index.html)
      - [pymllm.layers.attention.gdn](../autoapi/pymllm/layers/attention/gdn/index.html)
      - [pymllm.layers.attention.gdn_backend](../autoapi/pymllm/layers/attention/gdn_backend/index.html)
      - [pymllm.layers.attention.gdn_chunkwise](../autoapi/pymllm/layers/attention/gdn_chunkwise/index.html)
      - [pymllm.layers.attention.hybrid_backend](../autoapi/pymllm/layers/attention/hybrid_backend/index.html)
      - [pymllm.layers.attention.radix_attention](../autoapi/pymllm/layers/attention/radix_attention/index.html)
      - [pymllm.layers.attention.radix_linear_attention](../autoapi/pymllm/layers/attention/radix_linear_attention/index.html)
    - [pymllm.layers.base](../autoapi/pymllm/layers/base/index.html)
    - [pymllm.layers.custom_event](../autoapi/pymllm/layers/custom_event/index.html)
    - [pymllm.layers.embedding](../autoapi/pymllm/layers/embedding/index.html)
    - [pymllm.layers.gated_delta_net](../autoapi/pymllm/layers/gated_delta_net/index.html)
    - [pymllm.layers.layer_norm](../autoapi/pymllm/layers/layer_norm/index.html)
    - [pymllm.layers.linear](../autoapi/pymllm/layers/linear/index.html)
    - [pymllm.layers.mlp](../autoapi/pymllm/layers/mlp/index.html)
    - [pymllm.layers.quantize_base](../autoapi/pymllm/layers/quantize_base/index.html)
    - [pymllm.layers.rms_norm](../autoapi/pymllm/layers/rms_norm/index.html)
    - [pymllm.layers.rms_norm_gated](../autoapi/pymllm/layers/rms_norm_gated/index.html)
    - [pymllm.layers.rope](../autoapi/pymllm/layers/rope/index.html)
    - [pymllm.layers.sampling](../autoapi/pymllm/layers/sampling/index.html)
    - [pymllm.layers.utils](../autoapi/pymllm/layers/utils/index.html)
  - [pymllm.mem_cache](../autoapi/pymllm/mem_cache/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [pymllm.mem_cache.base_prefix_cache](../autoapi/pymllm/mem_cache/base_prefix_cache/index.html)
    - [pymllm.mem_cache.chunk_cache](../autoapi/pymllm/mem_cache/chunk_cache/index.html)
    - [pymllm.mem_cache.mamba_radix_cache](../autoapi/pymllm/mem_cache/mamba_radix_cache/index.html)
    - [pymllm.mem_cache.memory_pool](../autoapi/pymllm/mem_cache/memory_pool/index.html)
    - [pymllm.mem_cache.radix_cache](../autoapi/pymllm/mem_cache/radix_cache/index.html)
  - [pymllm.mobile](../autoapi/pymllm/mobile/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [pymllm.mobile.backends](../autoapi/pymllm/mobile/backends/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
      - [pymllm.mobile.backends.qualcomm](../autoapi/pymllm/mobile/backends/qualcomm/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
        - [pymllm.mobile.backends.qualcomm.nn](../autoapi/pymllm/mobile/backends/qualcomm/nn/index.html)
        - [pymllm.mobile.backends.qualcomm.qnn_aot_env](../autoapi/pymllm/mobile/backends/qualcomm/qnn_aot_env/index.html)
        - [pymllm.mobile.backends.qualcomm.transformers](../autoapi/pymllm/mobile/backends/qualcomm/transformers/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
          - [pymllm.mobile.backends.qualcomm.transformers.core](../autoapi/pymllm/mobile/backends/qualcomm/transformers/core/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
            - [pymllm.mobile.backends.qualcomm.transformers.core.embedding](../autoapi/pymllm/mobile/backends/qualcomm/transformers/core/embedding/index.html)
            - [pymllm.mobile.backends.qualcomm.transformers.core.observer](../autoapi/pymllm/mobile/backends/qualcomm/transformers/core/observer/index.html)
            - [pymllm.mobile.backends.qualcomm.transformers.core.qdq](../autoapi/pymllm/mobile/backends/qualcomm/transformers/core/qdq/index.html)
            - [pymllm.mobile.backends.qualcomm.transformers.core.qlinear](../autoapi/pymllm/mobile/backends/qualcomm/transformers/core/qlinear/index.html)
            - [pymllm.mobile.backends.qualcomm.transformers.core.rms_norm](../autoapi/pymllm/mobile/backends/qualcomm/transformers/core/rms_norm/index.html)
    - [pymllm.mobile.convertor](../autoapi/pymllm/mobile/convertor/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
      - [pymllm.mobile.convertor.mllm_type_mapping](../autoapi/pymllm/mobile/convertor/mllm_type_mapping/index.html)
      - [pymllm.mobile.convertor.model_file_v1](../autoapi/pymllm/mobile/convertor/model_file_v1/index.html)
      - [pymllm.mobile.convertor.model_file_v2](../autoapi/pymllm/mobile/convertor/model_file_v2/index.html)
    - [pymllm.mobile.ffi](../autoapi/pymllm/mobile/ffi/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
      - [pymllm.mobile.ffi.base](../autoapi/pymllm/mobile/ffi/base/index.html)
    - [pymllm.mobile.nn](../autoapi/pymllm/mobile/nn/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
      - [pymllm.mobile.nn.functional](../autoapi/pymllm/mobile/nn/functional/index.html)
    - [pymllm.mobile.quantize](../autoapi/pymllm/mobile/quantize/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
      - [pymllm.mobile.quantize.cast2fp32_pass](../autoapi/pymllm/mobile/quantize/cast2fp32_pass/index.html)
      - [pymllm.mobile.quantize.gguf](../autoapi/pymllm/mobile/quantize/gguf/index.html)
      - [pymllm.mobile.quantize.kai](../autoapi/pymllm/mobile/quantize/kai/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
        - [pymllm.mobile.quantize.kai.w4a32](../autoapi/pymllm/mobile/quantize/kai/w4a32/index.html)
      - [pymllm.mobile.quantize.pipeline](../autoapi/pymllm/mobile/quantize/pipeline/index.html)
      - [pymllm.mobile.quantize.quantize_pass](../autoapi/pymllm/mobile/quantize/quantize_pass/index.html)
      - [pymllm.mobile.quantize.solver](../autoapi/pymllm/mobile/quantize/solver/index.html)
      - [pymllm.mobile.quantize.spinquant](../autoapi/pymllm/mobile/quantize/spinquant/index.html)
    - [pymllm.mobile.service](../autoapi/pymllm/mobile/service/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
      - [pymllm.mobile.service.models_hub](../autoapi/pymllm/mobile/service/models_hub/index.html)
      - [pymllm.mobile.service.network](../autoapi/pymllm/mobile/service/network/index.html)
      - [pymllm.mobile.service.rr_process](../autoapi/pymllm/mobile/service/rr_process/index.html)
      - [pymllm.mobile.service.tools](../autoapi/pymllm/mobile/service/tools/index.html)
    - [pymllm.mobile.utils](../autoapi/pymllm/mobile/utils/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
      - [pymllm.mobile.utils.adb](../autoapi/pymllm/mobile/utils/adb/index.html)
      - [pymllm.mobile.utils.error_handler](../autoapi/pymllm/mobile/utils/error_handler/index.html)
      - [pymllm.mobile.utils.mllm_convertor](../autoapi/pymllm/mobile/utils/mllm_convertor/index.html)
  - [pymllm.models](../autoapi/pymllm/models/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [pymllm.models.qwen3](../autoapi/pymllm/models/qwen3/index.html)
    - [pymllm.models.qwen3_5](../autoapi/pymllm/models/qwen3_5/index.html)
    - [pymllm.models.qwen3_moe](../autoapi/pymllm/models/qwen3_moe/index.html)
    - [pymllm.models.qwen3_vl](../autoapi/pymllm/models/qwen3_vl/index.html)
  - [pymllm.orchestrator](../autoapi/pymllm/orchestrator/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [pymllm.orchestrator.cuda_ipc_transport](../autoapi/pymllm/orchestrator/cuda_ipc_transport/index.html)
    - [pymllm.orchestrator.detokenizer_process](../autoapi/pymllm/orchestrator/detokenizer_process/index.html)
    - [pymllm.orchestrator.group_coordinator](../autoapi/pymllm/orchestrator/group_coordinator/index.html)
    - [pymllm.orchestrator.ipc_utils](../autoapi/pymllm/orchestrator/ipc_utils/index.html)
    - [pymllm.orchestrator.model_runner_process](../autoapi/pymllm/orchestrator/model_runner_process/index.html)
    - [pymllm.orchestrator.parallel_state](../autoapi/pymllm/orchestrator/parallel_state/index.html)
    - [pymllm.orchestrator.request_response_process](../autoapi/pymllm/orchestrator/request_response_process/index.html)
    - [pymllm.orchestrator.scheduler_process](../autoapi/pymllm/orchestrator/scheduler_process/index.html)
    - [pymllm.orchestrator.shared_memory_queue](../autoapi/pymllm/orchestrator/shared_memory_queue/index.html)
    - [pymllm.orchestrator.tokenizer_process](../autoapi/pymllm/orchestrator/tokenizer_process/index.html)
  - [pymllm.parsers](../autoapi/pymllm/parsers/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [pymllm.parsers.reasoning_parser](../autoapi/pymllm/parsers/reasoning_parser/index.html)
    - [pymllm.parsers.tool_call_parser](../autoapi/pymllm/parsers/tool_call_parser/index.html)
  - [pymllm.quantization](../autoapi/pymllm/quantization/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [pymllm.quantization.kernels](../autoapi/pymllm/quantization/kernels/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
      - [pymllm.quantization.kernels.int8_activation_triton](../autoapi/pymllm/quantization/kernels/int8_activation_triton/index.html)
    - [pymllm.quantization.methods](../autoapi/pymllm/quantization/methods/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
      - [pymllm.quantization.methods.awq_marlin](../autoapi/pymllm/quantization/methods/awq_marlin/index.html)
      - [pymllm.quantization.methods.compressed_tensors](../autoapi/pymllm/quantization/methods/compressed_tensors/index.html)
    - [pymllm.quantization.quant_config](../autoapi/pymllm/quantization/quant_config/index.html)
  - [pymllm.server](../autoapi/pymllm/server/index.html)☐ ![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctYXJyb3ctcmlnaHQiIC8+PC9zdmc+)
    - [pymllm.server.launch](../autoapi/pymllm/server/launch/index.html)

[![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdib3g9IjAgMCAyNCAyNCI+CiAgICAgICAgICAgIDxwYXRoIGQ9Ik0xMyAyMGgtMlY4bC01LjUgNS41LTEuNDItMS40MkwxMiA0LjE2bDcuOTIgNy45Mi0xLjQyIDEuNDJMMTMgOHYxMnoiIC8+CiAgICAgICAgICA8L3N2Zz4=) Back to top](#)

[![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctZXllIiAvPjwvc3ZnPg==) View this page](../_sources/qnn_backend/aot_execute.rst.txt "View this page")

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0idGhlbWUtaWNvbi13aGVuLWF1dG8tbGlnaHQiPjx1c2UgaHJlZj0iI3N2Zy1zdW4td2l0aC1tb29uIiAvPjwvc3ZnPg==) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0idGhlbWUtaWNvbi13aGVuLWF1dG8tZGFyayI+PHVzZSBocmVmPSIjc3ZnLW1vb24td2l0aC1zdW4iIC8+PC9zdmc+) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0idGhlbWUtaWNvbi13aGVuLWRhcmsiPjx1c2UgaHJlZj0iI3N2Zy1tb29uIiAvPjwvc3ZnPg==) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0idGhlbWUtaWNvbi13aGVuLWxpZ2h0Ij48dXNlIGhyZWY9IiNzdmctc3VuIiAvPjwvc3ZnPg==)

![](data:image/svg+xml;base64,PHN2Zz48dXNlIGhyZWY9IiNzdmctdG9jIiAvPjwvc3ZnPg==)

# QNN AOT Execution Flow[¶](#qnn-aot-execution-flow "Link to this heading")

Note

Please refer to the [Environment Setup](setup_env.html) documentation to configure the QNN and Hexagon SDK environments before proceeding.

This document aims to explain the main execution flow of QNN AOT (Ahead-of-Time). This implementation is designed to fully leverage the offline compilation capabilities of the Qualcomm QNN framework to achieve efficient inference of fully integer-quantized Large Language Models (LLMs) on mobile devices, which is the de facto workflow for LLM execution on the Hexagon NPU.

Specifically, our implementation employs a W4A16 quantization scheme. The Key-Value (KV) Cache is quantized to `uint8`, and the linear weights are quantized using Low-Power Blockwise Quantization (LPBQ).

The implementation of this module was inspired by the [PyTorch ExecuTorch](https://pytorch.org/executorch/) project, especially its [Hybrid Execution Mode](https://github.com/pytorch/executorch/blob/main/examples/qualcomm/oss_scripts/llama/README.md) designed for the Qualcomm backend, for which we are grateful.

## Overall Flow[¶](#overall-flow "Link to this heading")

The QNN AOT execution flow is mainly divided into three stages:

1.  **Model Quantization and Export (Python)**: On the host machine, a Python script is used to quantize the pre-trained floating-point model and export it to `.safetensor` file. The `.safetensor` is then converted to `.mllm` file using mllm-convertor.

2.  **Offline Compilation (C++)**: On the host machine, a C++ compiler program loads the `.mllm` file, invokes the QNN toolchain for model compilation, graph optimization, and quantization parameter adjustment, and finally generates a QNN Context Binary.

3.  **On-Device Execution (C++)**: On the target device (e.g., a mobile phone), the AOT runner program loads the pre-compiled context binary and executes inference.

## Detailed Steps[¶](#detailed-steps "Link to this heading")

Taking `qwen3_qnn_aot` as an example, the detailed steps are as follows.

1.  **Model Quantization and Export**

    First, we need to run a Python script on the host to quantize the model and export it as a `.safetensors` file.

        cd ./pymllm/backends/qualcomm/transformers/qwen3
        python train.py --model_path "/your/qwen3/model/path/" --max_length 1024 --num_samples 128 --output_dir "/path/to/output"

    This step generates a key file:

    - `model.safetensors`: The quantized model file, saved in the specified output directory.

    Next, convert the exported `.safetensors` model to the MLLM format (`.mllm`) using the `mllm-convertor` script.

    Note

    Before using `mllm-convertor`, you need to install the `pymllm` package. You can install it using one of the following methods:

    **Standard Installation:**

        bash ./scripts/install_pymllm.sh

    **Editable Installation (for development):**

        # In the mllm project root directory
        pip install -e .

        # link lib to pymllm's dir, so that tvm ffi can find the lib
        #
        # NOTE:! build x86 qualcomm aot first !
        source <absolute path to where you install qnn>/bin/envsetup.sh
        python task.py tasks/build_x86_qnn_aot.yaml
        ln -s <absolute path to where you build mllm>/bin/ mllm/pymllm/lib

    Note

    1.  The `--pipeline` option is not required for converting models in this document.

    2.  The `--verbose` option is used to print verbose output. It is recommended to use it for debugging.

        mllm-convertor --input_path /path/to/output/model.safetensors --output_path /path/to/output/qwen3_1.7b.mllm --verbose

    This will generate the `qwen3_1.7b.mllm` file, which will be used in the subsequent compilation step.

2.  **Offline Compilation to Generate QNN Context**

    Next, we use a C++ compiler program (`compile.cpp`) on the host to generate the QNN context. This process invokes the QNN SDK to convert the MLLM IR into a QNN-supported format and performs optimizations.

    Compile and run the `compile` program:

        # In the mllm-v2 project root directory
        source <absolute path to where you install qnn>/bin/envsetup.sh
        python task.py tasks/build_x86_qnn_aot.yaml

        # Run the compiler program
        ./build-qnn-aot/bin/mllm-qwen3-aot-sha-c \
        -m /path/to/output/qwen3_1.7b.mllm \
        -c ./examples/qwen3_qnn_aot/config_1.7B.json \
        --aot_config ./examples/qwen3_qnn_aot/qnn_aot_cfg_1.7B.json
        # Optional, default value is /opt/qcom/aistack/qairt/2.41.0.251128/lib/x86_64-linux-clang/
        # --qnn_env_path path/to/qnn_sdk.

    This program reads the `.mllm` model file and the quantization recipe, and finally generates a QNN context binary file named `qwen3-1.7B-lpbq-sha.bin`. This file contains all the information needed to execute inference on the target device.

    Note

    The `HtpSignedPd` config in qnn_aot_cfg_1.7B.json will specify `QNN_HTP_DEVICE_CONFIG_OPTION_SIGNEDPD` during QNN initialization, which may cause an “Unsupported config option 2” error in older QNN versions. It is recommended to change the config in the json file to `HtpUnsignedPd`.

3.  **On-Device AOT Inference**

    Finally, we push the generated `qwen3-1.7B-lpbq-sha.bin` file and other resources like the tokenizer to the target device. The on-device AOT runner program (`aot_run.cpp`) will load this binary file and execute inference.

    Compile and run the `aot_run` program:

        # Cross-compile the aot_run program for the target device (e.g., Android)
        python task.py tasks/build_android_qnn.yaml

        # Push compiled context file to the device
        adb push qwen3-1.7B-lpbq-sha.bin /data/local/tmp/

        # Push QNN libraries and Op Packages
        ANDR_LIB=$QNN_SDK_ROOT/lib/aarch64-android
        OP_PATH=mllm/backends/qnn/custom-op-package/LLaMAPackage/build

        adb push $ANDR_LIB/libQnnHtp.so /data/local/tmp
        adb push $ANDR_LIB/libQnnHtpV75Stub.so /data/local/tmp
        adb push $ANDR_LIB/libQnnHtpPrepare.so /data/local/tmp
        adb push $ANDR_LIB/libQnnHtpProfilingReader.so /data/local/tmp
        adb push $ANDR_LIB/libQnnHtpOptraceProfilingReader.so /data/local/tmp
        adb push $ANDR_LIB/libQnnHtpV75CalculatorStub.so /data/local/tmp
        adb push $QNN_SDK_ROOT/lib/hexagon-v75/unsigned/libQnnHtpV75Skel.so /data/local/tmp
        adb push $QNN_SDK_ROOT/lib/aarch64-android/libQnnSystem.so /data/local/tmp

        adb push $OP_PATH/aarch64-android/libQnnLLaMAPackage.so /data/local/tmp/libQnnLLaMAPackage_CPU.so
        adb push $OP_PATH/hexagon-v75/libQnnLLaMAPackage.so /data/local/tmp/libQnnLLaMAPackage_HTP.so

        # Push mllm runner and libs to device
        adb push build-android-arm64-v8a-qnn/bin/*.so /data/local/tmp
        adb push build-android-arm64-v8a-qnn/bin/mllm-qwen3-aot-runner /data/local/tmp

        # Execute on the device
        adb shell "cd /data/local/tmp && export LD_LIBRARY_PATH=. &&
        ./mllm-qwen3-aot-runner -m qwen3-1.7B-lpbq-sha.bin
        -t qwen3-tokenizer.json -c config_1.7B.json --ar_len 32"

    The AOT runner program loads the `.bin` file to initialize the QNN context, then receives input tokens, performs model inference, and outputs the next token, thus realizing the language model generation process.

## Hybrid Mode Explanation[¶](#hybrid-mode-explanation "Link to this heading")

Our QNN AOT implementation adopts a Hybrid mode similar to executorch to optimize the efficiency of Prompt processing and Token generation.

- **Prefill Phase**: When processing the user’s input (Prompt) for the first time, the model calculates and caches the Key-Value (KV) states for all input tokens at once. This phase is computationally intensive but is performed only once.

- **Decode Phase**: When generating subsequent tokens, the model takes only the previously generated token as input and uses the cached KV state for computation. This process is computationally light and fast, suitable for token-by-token generation.

In this way, we combine the advantages of batch processing and stream processing to improve overall throughput while ensuring low latency.

[](../opencl_backend/index.html)

Next

OpenCL Backend

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZnVyby1yZWxhdGVkLWljb24iPjx1c2UgaHJlZj0iI3N2Zy1hcnJvdy1yaWdodCIgLz48L3N2Zz4=) [![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iZnVyby1yZWxhdGVkLWljb24iPjx1c2UgaHJlZj0iI3N2Zy1hcnJvdy1yaWdodCIgLz48L3N2Zz4=)](core_design.html)

Previous

QNN Backend Design

Copyright © 2024-2025, MLLM Contributors

Made with [Sphinx](https://www.sphinx-doc.org/) and [@pradyunsg](https://pradyunsg.me)'s [Furo](https://github.com/pradyunsg/furo)

On this page

- [QNN AOT Execution Flow](#)
  - [Overall Flow](#overall-flow)
  - [Detailed Steps](#detailed-steps)
  - [Hybrid Mode Explanation](#hybrid-mode-explanation)
