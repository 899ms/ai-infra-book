# Nineteen media scenario CLI verification

The script is prepared but must not run actual CLI comparisons until root confirms the new unified reproduction has finished.

```sh
python3 calculations/research/media-feedback-public-integration/check-cli.py --ready
python3 calculations/research/media-feedback-public-integration/check-cli.py
```

`--ready` reads the nineteen `media-feedback-*` IDs from the official `scenarios/book.json` transport_closed_loop group and verifies the ID set against `scenario-mapping.json`. It requires the38 JSON/Markdown artifact entries and corresponding files in the official results manifest, rejects duplicate manifest entries or unexpected media artifact names, and reports missing artifacts without invoking a calculator.

The actual run performs exactly38 subprocess calls to the unified `calc.py transport-closed-loop` command. Each call uses the exact registered application/network input written to a temporary file. Actual JSON/Markdown output is streamed in1MiB chunks against the corresponding official artifact; both complete bytes and SHA256 are checked, with the expected artifact hash also checked against the official manifest. Inputs and outputs live in TemporaryDirectory contexts and are deleted even on failure.

Before/after every call, the source fingerprint includes every public transport module (including all new media modules and media_report), public transport topic/sender, CLI, report, paths, calc.py, sources.py, source lock, book scenarios, scenario mapping, and fixed transport/RFC9221 original inputs. The results manifest must stay byte-identical throughout. Reports include exact temporary input hashes, source fingerprints, manifest hashes, artifact bytes/hash and elapsed time. A running progress JSON cannot be mistaken for the final passed report.

The script does not reproduce official results, edit public inputs or rerun the old26 transport scenarios. It checks the new media artifacts through actual user-facing CLI execution only. The final report is cli-check.json; an unfinished run retains cli-check-progress.json as explicitly running evidence.
