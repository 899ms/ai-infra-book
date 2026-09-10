# Shared component public migration checkpoint

This checkpoint migrates nine shared modules into `calculations/src/infra_calc/transport/`. It does not claim that the public network, CLI, reproduction manifest, figures, or book registration is complete.

`migration-manifest.json` records each exact research/public Python SHA256, unified wrapper diff, support-module hash and eight newly registered official sources. Existing RFC9000/9002/5681 and RFC9002 Errata7539 bytes are reused through the existing public lock. New RFC9438, RFC9406 and its dated errata-query snapshot, and five Linux v6.6 source/dependency files are copied from already sealed official originals and verified by bytes and SHA256. Linux remains pinned to commit `ffc253263a1375a65fa6c9f62a893e9767fbebfa`.

All research dynamic path loading and BBR `sys.path` mutation are replaced with static relative imports. `reference_sources(group)` accepts `quic`, `cubic`, `hystart`, or `bbr`; it uses the public `read_source` verifier and returns exact source metadata. The public BBR constructor verifies official BBR sources instead of looking for a research Python lock. Public Python is covered by the normal `reproduce.input_hashes()` code recursion; the parent integration must add the new official source directory to its source input list. Source provenance is separate from mathematical payload.

The selected BBR research adapter baseline is `606b263d23d8c7917fd6deab94378a4639b343c43bf35087937eb9eebe7d66ba`, with incremental active-flight bookkeeping. The earlier c410 adapter is retained only under the research `baselines/` directory for optimization regression; it is not a public runtime dependency.

Run this bounded migration check from the checkout root:

```sh
python3 calculations/research/transport-controller-loop/integration/check-components.py
```

The check verifies all research/public hashes in the manifest, compares function/method ASTs and class/module constant fields across nine modules, compares all 16 CUBIC and 13 HyStart scenario mathematical payloads, and compares the BBR local hook regression's complete returned payload. Source-verification functions and independent CLI `main()` wrappers are explicitly excluded from AST comparison; BBR constructor comparison starts at the unchanged `config` parsing statement, and persistent-congestion evaluation comparison starts after its docstring/source check. Those exact wrapper changes remain visible in the saved patches. Formatting changes are allowed only because AST comparison verifies that they do not alter the mathematical body.

`component-check.json` contains the successful run and checker SHA256. This is migration parity evidence, not a new independent Linux or RFC oracle and not a whole-network validation. Existing independent controller/source evidence remains in the original research folders. No full public reproduce or full test suite was run by this subtask.

## Complete public network parity

`check-network-public.py` actually recomputes all six explicit book/router scenarios through the public `infra_calc.topics.transport_closed_loop.calculate` API. It compares every mathematical field against the complete sealed research result, excluding only the two top-level source-reference metadata fields. Lists are checked item by item, including typed JSON equality of all nested records; object keys and scalar types must also agree. The checker streams the research file while retaining only one public scenario at a time. It verifies each research result against its generation manifest and all tracked public/research Python hashes before and after the comparisons. `network-public-check.json` records the actual execution outcome, per-scenario counts, elapsed time, business outcomes and source/result hashes. This is full mathematical migration parity, not another independent RFC derivation and not a full reproduction-pipeline run.

```sh
python3 calculations/research/transport-controller-loop/integration/check-network-public.py
```
